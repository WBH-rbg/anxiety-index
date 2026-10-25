#!/usr/bin/env bash
#
# Anxiety Index: one-time Google Cloud setup
# ------------------------------------------
# Run this in Google Cloud Shell with the anxiety-index project selected:
#
#     bash setup_gcp.sh
#
# Or name the project explicitly:
#
#     bash setup_gcp.sh YOUR-PROJECT-ID
#
# It is safe to run more than once. Anything that already exists is left alone.
#
# What it creates:
#   - Cloud Storage bucket for the raw snapshot archive (private, versioned,
#     and append-only for the pipeline, so history can't be overwritten)
#   - BigQuery datasets: ai_raw, ai_clean, ai_index, ai_outcomes
#   - A service account the pipeline runs as, with only the access it needs
#   - Keyless sign-in for GitHub Actions (Workload Identity Federation),
#     restricted to the GitHub repository below
#   - A monthly budget alert

set -euo pipefail

# ---- Settings ---------------------------------------------------------------
GITHUB_REPO="WBH-rbg/anxiety-index"
LOCATION="US"
BUDGET_USD="25"

SA_NAME="anxiety-index-pipeline"
POOL_ID="github"
PROVIDER_ID="anxiety-index-repo"
DATASETS=("ai_raw" "ai_clean" "ai_index" "ai_outcomes")
BUDGET_NAME="Anxiety Index monthly budget"

# ---- Helpers ----------------------------------------------------------------
step() { printf '\n\033[1m==> %s\033[0m\n' "$1"; }
ok()   { printf '    \033[32mdone:\033[0m %s\n' "$1"; }
skip() { printf '    already set up: %s\n' "$1"; }
fail() { printf '\n\033[31mSTOPPED:\033[0m %s\n' "$1" >&2; exit 1; }
trap 'fail "Something went wrong on line ${LINENO}. Copy the messages above and send them to Claude."' ERR

# ---- Project ----------------------------------------------------------------
if [[ $# -ge 1 && -n "$1" ]]; then
  gcloud config set project "$1" >/dev/null
fi
PROJECT_ID="$(gcloud config get-value project 2>/dev/null || true)"
[[ -n "$PROJECT_ID" ]] || fail "No project is selected. Pick the anxiety-index project in the console's project picker, reopen Cloud Shell, and run this again."

PROJECT_NUMBER="$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
BUCKET="${PROJECT_ID}-raw-archive"
PROVIDER_RESOURCE="projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_ID}/providers/${PROVIDER_ID}"

step "Using project ${PROJECT_ID} (number ${PROJECT_NUMBER})"

# ---- Billing check ----------------------------------------------------------
step "Checking that billing is on"
gcloud services enable cloudbilling.googleapis.com --quiet
BILLING_ENABLED="$(gcloud billing projects describe "$PROJECT_ID" --format='value(billingEnabled)')"
if [[ "${BILLING_ENABLED,,}" != "true" ]]; then
  fail "Billing isn't turned on for ${PROJECT_ID}. In the console, open Billing, link a billing account to this project, then run this again. (Without billing, BigQuery deletes tables after 60 days.)"
fi
BILLING_ACCOUNT="$(gcloud billing projects describe "$PROJECT_ID" --format='value(billingAccountName)')"
BILLING_ACCOUNT="${BILLING_ACCOUNT#billingAccounts/}"
ok "billing account ${BILLING_ACCOUNT}"

# ---- APIs -------------------------------------------------------------------
step "Turning on the Google Cloud services the pipeline uses (about a minute)"
gcloud services enable \
  storage.googleapis.com \
  bigquery.googleapis.com \
  iam.googleapis.com \
  iamcredentials.googleapis.com \
  sts.googleapis.com \
  cloudresourcemanager.googleapis.com \
  billingbudgets.googleapis.com \
  --quiet
ok "services enabled"

# ---- Raw archive bucket -----------------------------------------------------
step "Creating the raw archive bucket gs://${BUCKET}"
if gcloud storage buckets describe "gs://${BUCKET}" >/dev/null 2>&1; then
  skip "bucket exists"
else
  gcloud storage buckets create "gs://${BUCKET}" \
    --location="$LOCATION" \
    --uniform-bucket-level-access \
    --public-access-prevention \
    --quiet
  ok "bucket created"
fi
gcloud storage buckets update "gs://${BUCKET}" --versioning --quiet >/dev/null
ok "versioning on"

# ---- BigQuery datasets ------------------------------------------------------
step "Creating BigQuery datasets"
declare -A DESCRIPTIONS=(
  [ai_raw]="Source data loaded exactly as collected, one load per snapshot"
  [ai_clean]="Standardized weekly series built from ai_raw"
  [ai_index]="Index readings, theme scores, driver attributions, release archive"
  [ai_outcomes]="Curated outcome log (backlash events, boycotts, protest escalation)"
)
for ds in "${DATASETS[@]}"; do
  if bq --location="$LOCATION" show --dataset "${PROJECT_ID}:${ds}" >/dev/null 2>&1; then
    skip "${ds}"
  else
    bq --location="$LOCATION" mk --dataset --description "${DESCRIPTIONS[$ds]}" "${PROJECT_ID}:${ds}" >/dev/null
    ok "${ds}"
  fi
  # Datasets created before billing was on carry BigQuery's 60-day auto-delete.
  # Clear it so the archive is kept permanently.
  bq update --default_table_expiration 0 --default_partition_expiration 0 \
    "${PROJECT_ID}:${ds}" >/dev/null
done
ok "auto-delete turned off on all datasets"

# ---- Service account --------------------------------------------------------
step "Creating the pipeline's service account"
if gcloud iam service-accounts describe "$SA_EMAIL" >/dev/null 2>&1; then
  skip "$SA_EMAIL"
else
  gcloud iam service-accounts create "$SA_NAME" \
    --display-name="Anxiety Index pipeline" \
    --description="Used by GitHub Actions in ${GITHUB_REPO}" \
    --quiet
  ok "$SA_EMAIL"
  sleep 10   # give the new account a moment to become visible to IAM
fi

step "Granting the service account only the access it needs"
# Append-only on the archive: it can add and read snapshots, never overwrite or delete them.
gcloud storage buckets add-iam-policy-binding "gs://${BUCKET}" \
  --member="serviceAccount:${SA_EMAIL}" --role="roles/storage.objectCreator" --quiet >/dev/null
gcloud storage buckets add-iam-policy-binding "gs://${BUCKET}" \
  --member="serviceAccount:${SA_EMAIL}" --role="roles/storage.objectViewer" --quiet >/dev/null
ok "archive: add and read only"
# BigQuery: run queries (including against GDELT's public data) and write our tables.
for role in roles/bigquery.jobUser roles/bigquery.dataEditor; do
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:${SA_EMAIL}" --role="$role" --condition=None --quiet >/dev/null
done
ok "BigQuery: run queries, write tables"

# ---- Keyless GitHub connection ----------------------------------------------
step "Connecting GitHub Actions without keys (only ${GITHUB_REPO} is allowed in)"
if gcloud iam workload-identity-pools describe "$POOL_ID" --location=global >/dev/null 2>&1; then
  skip "identity pool ${POOL_ID}"
else
  gcloud iam workload-identity-pools create "$POOL_ID" \
    --location=global --display-name="GitHub Actions" --quiet
  ok "identity pool ${POOL_ID}"
fi

if gcloud iam workload-identity-pools providers describe "$PROVIDER_ID" \
     --location=global --workload-identity-pool="$POOL_ID" >/dev/null 2>&1; then
  skip "provider ${PROVIDER_ID}"
else
  gcloud iam workload-identity-pools providers create-oidc "$PROVIDER_ID" \
    --location=global \
    --workload-identity-pool="$POOL_ID" \
    --display-name="anxiety-index repository" \
    --issuer-uri="https://token.actions.githubusercontent.com" \
    --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" \
    --attribute-condition="assertion.repository == '${GITHUB_REPO}'" \
    --quiet
  ok "provider ${PROVIDER_ID}"
fi

gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_ID}/attribute.repository/${GITHUB_REPO}" \
  --quiet >/dev/null
ok "GitHub repository can act as the pipeline service account"

# ---- Budget alert -----------------------------------------------------------
step "Setting a \$${BUDGET_USD}/month budget alert"
BUDGET_STATUS="created"
if gcloud billing budgets list --billing-account="$BILLING_ACCOUNT" \
     --billing-project="$PROJECT_ID" --format='value(displayName)' 2>/dev/null \
     | grep -qxF "$BUDGET_NAME"; then
  skip "budget"
  BUDGET_STATUS="already existed"
elif gcloud billing budgets create \
       --billing-account="$BILLING_ACCOUNT" \
       --billing-project="$PROJECT_ID" \
       --display-name="$BUDGET_NAME" \
       --budget-amount="${BUDGET_USD}USD" \
       --filter-projects="projects/${PROJECT_ID}" \
       --threshold-rule=percent=0.5 \
       --threshold-rule=percent=0.9 \
       --threshold-rule=percent=1.0 \
       --quiet >/dev/null 2>&1; then
  ok "alerts at 50%, 90% and 100% of \$${BUDGET_USD}"
else
  BUDGET_STATUS="not created - set it manually under Billing > Budgets & alerts"
  printf '    \033[33mnote:\033[0m could not create the budget automatically.\n'
  printf '    Set one by hand: Billing > Budgets & alerts > Create budget (%s USD/month).\n' "$BUDGET_USD"
fi

# ---- Summary ----------------------------------------------------------------
trap - ERR
cat <<EOF

$(printf '\033[1m')Setup complete.$(printf '\033[0m') Copy everything between the lines below and paste it to Claude.
None of these values are passwords or keys.

---------------------------------------------------------------------------
ANXIETY INDEX CLOUD SETUP
GCP_PROJECT_ID=${PROJECT_ID}
GCP_PROJECT_NUMBER=${PROJECT_NUMBER}
GCP_LOCATION=${LOCATION}
GCS_RAW_BUCKET=${BUCKET}
BQ_DATASETS=$(IFS=,; echo "${DATASETS[*]}")
GCP_SERVICE_ACCOUNT=${SA_EMAIL}
GCP_WORKLOAD_IDENTITY_PROVIDER=${PROVIDER_RESOURCE}
GITHUB_REPO=${GITHUB_REPO}
BUDGET=${BUDGET_STATUS}
---------------------------------------------------------------------------
EOF
