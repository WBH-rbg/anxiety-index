# Anxiety Index

A published, weekly index of public anxiety in the United States, built for senior decision makers at large companies and for communications and reputation professionals.

The index works like a fire-danger rating for public mood. It doesn't predict specific events; it measures how primed people are to react, so the same spark can fizzle in a calm period or catch fire in an anxious one.

## How it's built

- **GitHub (this repository):** code, methodology, and version history
- **GitHub Actions:** scheduled data collection and index calculation
- **Google Cloud project `anxiety-index`:** raw snapshot archive (Cloud Storage) and data warehouse (BigQuery)

## BigQuery datasets

| Dataset | Contents |
|---|---|
| `ai_raw` | Source data loaded exactly as collected, one load per snapshot |
| `ai_clean` | Standardized weekly series built from `ai_raw` |
| `ai_index` | Index readings, theme scores, driver attributions, release archive |
| `ai_outcomes` | Curated outcome log: backlash events, boycotts, protest escalation |

## One-time setup

Run `scripts/setup_gcp.sh` in Google Cloud Shell with the `anxiety-index` project selected and billing turned on. It's safe to re-run.

## Principles

1. Explainable: every move comes with a plain-language explanation of what drove it
2. Readable at a glance: score, band, direction, top drivers
3. Visibly nonpartisan
4. Built on durable public data, with a backup for every important input
5. Learns over time, tested honestly
6. Accountable record: every published reading is archived as released
