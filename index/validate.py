"""Validation: does the index line up with things it should line up with?

    python -m index.validate      # writes output/validation.md and ai_index.validation_* tables

Tests
  1. Face validity: readings in known tense and calm periods.
  2. External series: correlation with Wikipedia views of anxiety articles, GDELT boycott
     coverage share, and overall news tone, contemporaneous and at leads/lags.
  3. Outcome log: the curated backlash events in docs/outcomes/backlash_events.csv.
     Relative frequency of backlash events in the two weeks after each band, and the
     average reading before events versus all weeks. Point-in-time by construction.
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path

import numpy as np
import pandas as pd

from index.run import DIM_LABELS, ROOT, OUT

OUTCOMES_CSV = ROOT / "docs" / "outcomes" / "backlash_events.csv"
PERIODS = [
    ("9/11 and aftermath", "2001-09-15", "2001-11-30", "tense"),
    ("Iraq invasion", "2003-03-15", "2003-04-30", "tense"),
    ("Mid-2000s calm", "2005-01-01", "2007-06-30", "calm"),
    ("Financial crisis", "2008-09-13", "2009-03-31", "tense"),
    ("Debt-ceiling summer", "2011-07-15", "2011-08-31", "tense"),
    ("2013-2015 calm", "2013-01-01", "2015-12-31", "calm"),
    ("COVID onset", "2020-03-07", "2020-04-30", "tense"),
    ("Summer 2020", "2020-05-30", "2020-07-15", "tense"),
    ("Jan 6 week", "2021-01-09", "2021-01-23", "tense"),
    ("Ukraine invasion", "2022-02-26", "2022-03-31", "tense"),
    ("Inflation peak", "2022-06-04", "2022-07-15", "tense"),
    ("Spring 2025 tariffs", "2025-04-05", "2025-04-30", "tense"),
]
EXTERNAL = {
    "wiki_anxiety": "Wikipedia views: Anxiety",
    "wiki_anxiety_disorder": "Wikipedia views: Anxiety disorder",
    "wiki_panic_attack": "Wikipedia views: Panic attack",
    "gkg_share_boycott": "News share: boycotts",
    "gkg_tone_us_all": "Average tone of all US news (sign flipped)",
    "gdelt_ev_conflict_share": "Share of US event coverage: conflict",
}


def load(client):
    head = client.query("SELECT week, score, band, z FROM `ai_index.headline_weekly` WHERE score IS NOT NULL ORDER BY week").to_dataframe()
    head["week"] = naive(head["week"])
    dims = client.query("SELECT week, dimension, score FROM `ai_index.dimension_weekly` WHERE score IS NOT NULL").to_dataframe()
    dims["week"] = naive(dims["week"])
    ext = client.query(f"""SELECT series_id, obs_date, value FROM `ai_clean.observations_latest`
                           WHERE series_id IN ({','.join("'" + s + "'" for s in EXTERNAL)}) AND value IS NOT NULL""").to_dataframe()
    ext["obs_date"] = naive(ext["obs_date"])
    return head, dims, ext


def naive(col: pd.Series) -> pd.Series:
    """Timestamps without a time zone (BigQuery TIMESTAMP columns arrive as UTC-aware)."""
    out = pd.to_datetime(col)
    return out.dt.tz_localize(None) if getattr(out.dt, "tz", None) is not None else out


def weekly(ext: pd.DataFrame, sid: str) -> pd.Series:
    s = ext[ext["series_id"] == sid].set_index("obs_date")["value"].sort_index()
    w = s.resample("W-SAT").mean()
    return w


def face_validity(head: pd.DataFrame) -> pd.DataFrame:
    rows = []
    h = head.set_index("week")["score"]
    for name, a, b, kind in PERIODS:
        seg = h[a:b]
        if seg.empty:
            continue
        rows.append({"period": name, "expected": kind, "mean_score": round(seg.mean(), 1), "max_score": round(seg.max(), 1),
                     "weeks_high_or_severe": int((seg >= 80).sum()), "weeks": len(seg),
                     "verdict": ("pass" if (kind == "tense" and seg.max() >= 80) or (kind == "calm" and seg.mean() <= 40) else "check")})
    return pd.DataFrame(rows)


def external_correlations(head: pd.DataFrame, ext: pd.DataFrame) -> pd.DataFrame:
    h = head.set_index("week")["score"]
    rows = []
    for sid, label in EXTERNAL.items():
        w = weekly(ext, sid)
        if w.empty:
            continue
        if sid == "gkg_tone_us_all":
            w = -w
        x = np.log(w.where(w > 0)) if sid.startswith("wiki") or sid.startswith("gkg_share") else w
        joined = pd.concat([h, x.rename("x")], axis=1).dropna()
        if len(joined) < 52:
            continue
        # detrend the external series lightly (52-week rolling median) so slow drifts don't dominate
        xd = joined["x"] - joined["x"].rolling(52, min_periods=26).median()
        row = {"series": label, "weeks": len(joined), "corr_level": round(joined["score"].corr(joined["x"]), 3),
               "corr_detrended": round(joined["score"].corr(xd), 3)}
        for lag in (-4, -2, -1, 1, 2, 4):
            row[f"corr_lead{lag:+d}"] = round(joined["score"].corr(xd.shift(-lag)), 3)  # positive lag: index leads series
        rows.append(row)
    return pd.DataFrame(rows)


def load_outcomes() -> pd.DataFrame:
    if not OUTCOMES_CSV.exists():
        return pd.DataFrame()
    ev = pd.read_csv(OUTCOMES_CSV)
    ev["event_date"] = pd.to_datetime(ev["event_date"], errors="coerce")
    ev = ev.dropna(subset=["event_date"])
    ev["severity"] = pd.to_numeric(ev["severity"], errors="coerce").fillna(1)
    return ev


def outcome_tests(head: pd.DataFrame, dims: pd.DataFrame, ev: pd.DataFrame) -> dict:
    if ev.empty:
        return {}
    h = head.set_index("week")
    ev = ev[ev["event_date"] >= h.index.min()].copy()
    ev["week"] = ev["event_date"] + pd.to_timedelta((5 - ev["event_date"].dt.weekday) % 7, unit="D")
    # reading in the week before each event (what a planner would have seen)
    ev["score_before"] = ev["week"].map(lambda w: h["score"].get(w - pd.Timedelta(days=7), np.nan))
    ev["band_before"] = ev["week"].map(lambda w: h["band"].get(w - pd.Timedelta(days=7), None))
    base_mean = h.loc[h.index >= ev["event_date"].min(), "score"].mean()
    by_sev = ev.groupby(ev["severity"].clip(upper=5).astype(int))["score_before"].agg(["count", "mean"]).round(1)
    # relative frequency: events per 100 weeks following each band
    weeks = h.loc[h.index >= ev["event_date"].min()].copy()
    event_weeks = set(ev["week"]) | set(ev["week"] + pd.Timedelta(days=7))
    weeks["event_next_2w"] = [((w + pd.Timedelta(days=7)) in event_weeks) or ((w + pd.Timedelta(days=14)) in event_weeks) for w in weeks.index]
    sev3 = set(ev.loc[ev["severity"] >= 3, "week"]) | set(ev.loc[ev["severity"] >= 3, "week"] + pd.Timedelta(days=7))
    weeks["major_next_2w"] = [((w + pd.Timedelta(days=7)) in sev3) or ((w + pd.Timedelta(days=14)) in sev3) for w in weeks.index]
    by_band = weeks.groupby("band").agg(weeks=("score", "size"), any_event_rate=("event_next_2w", "mean"), major_event_rate=("major_next_2w", "mean"))
    order = ["Low", "Moderate", "Elevated", "High", "Severe"]
    by_band = by_band.reindex([b for b in order if b in by_band.index])
    by_band["any_event_rate"] = (100 * by_band["any_event_rate"]).round(1)
    by_band["major_event_rate"] = (100 * by_band["major_event_rate"]).round(1)
    # which dimension is most elevated before events
    d = dims.pivot(index="week", columns="dimension", values="score")
    before = ev["week"].map(lambda w: d.loc[w - pd.Timedelta(days=7)] if (w - pd.Timedelta(days=7)) in d.index else None)
    dim_before = pd.DataFrame([b for b in before if b is not None]).mean().round(1).sort_values(ascending=False)
    dim_all = d.loc[d.index >= ev["event_date"].min()].mean().round(1)
    dim_table = pd.DataFrame({"before_events": dim_before, "all_weeks": dim_all.reindex(dim_before.index)})
    dim_table["difference"] = (dim_table["before_events"] - dim_table["all_weeks"]).round(1)
    return {"events": ev, "base_mean": round(base_mean, 1), "by_severity": by_sev, "by_band": by_band, "dim_table": dim_table,
            "mean_before": round(ev["score_before"].mean(), 1), "n": int(ev["score_before"].notna().sum())}


def report(face: pd.DataFrame, corr: pd.DataFrame, oc: dict) -> str:
    L = ["# Validation report", "", f"Generated {dt.date.today()}. Methodology v0.1 prototype.", "",
         "## 1. Face validity", "", "Does the index read tense when everyone remembers tension, and calm when they remember calm?", "",
         "| Period | Expected | Mean | Max | Weeks ≥80 | Weeks | Verdict |", "|---|---|---|---|---|---|---|"]
    for _, r in face.iterrows():
        L.append(f"| {r['period']} | {r['expected']} | {r['mean_score']} | {r['max_score']} | {r['weeks_high_or_severe']} | {r['weeks']} | {r['verdict']} |")
    L += ["", "## 2. External series", "", "Correlation of the weekly headline with series that should track public anxiety but are not inputs to the headline "
          "(detrended with a 52-week rolling median). 'lead+k' means the index this week vs. the series k weeks later.", "",
          "| Series | Weeks | Level | Detrended | lead−4 | lead−2 | lead−1 | lead+1 | lead+2 | lead+4 |", "|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in corr.iterrows():
        L.append(f"| {r['series']} | {r['weeks']} | {r['corr_level']} | {r['corr_detrended']} | {r['corr_lead-4']} | {r['corr_lead-2']} | {r['corr_lead-1']} | {r['corr_lead+1']} | {r['corr_lead+2']} | {r['corr_lead+4']} |")
    L += ["", "## 3. Corporate backlash events (curated outcome log)", ""]
    if not oc:
        L.append("No outcome log loaded yet.")
    else:
        L += [f"{oc['n']} dated backlash episodes since {oc['events']['event_date'].min().date()}. The reading a planner would have seen the week before an episode averaged **{oc['mean_before']}**, against **{oc['base_mean']}** for all weeks in the same span.", "",
              "By severity (1 = brief viral moment, 5 = sustained national controversy):", "", "| Severity | Episodes | Mean reading the week before |", "|---|---|---|"]
        for sev, r in oc["by_severity"].iterrows():
            L.append(f"| {sev} | {int(r['count'])} | {r['mean']} |")
        L += ["", "Episodes in the following two weeks, per 100 weeks, by the band shown that week:", "", "| Band | Weeks | Any episode | Severity ≥3 |", "|---|---|---|---|"]
        for band, r in oc["by_band"].iterrows():
            L.append(f"| {band} | {int(r['weeks'])} | {r['any_event_rate']} | {r['major_event_rate']} |")
        L += ["", "Dimension readings the week before episodes vs. all weeks:", "", "| Dimension | Before episodes | All weeks | Difference |", "|---|---|---|---|"]
        for dim, r in oc["dim_table"].iterrows():
            L.append(f"| {DIM_LABELS.get(dim, dim)} | {r['before_events']} | {r['all_weeks']} | {r['difference']:+.1f} |")
        L += ["", "Caveats: the log is curated and incomplete, episodes cluster in recent years when the log is richer, and the index was not tuned to this log. "
              "A clean result here is encouraging, not proof; a null result means the structure needs work."]
    return "\n".join(L) + "\n"


def main() -> int:
    from google.cloud import bigquery
    client = bigquery.Client(project="anxiety-index")
    head, dims, ext = load(client)
    face = face_validity(head)
    corr = external_correlations(head, ext)
    ev = load_outcomes()
    if not ev.empty:
        client.load_table_from_dataframe(ev, "anxiety-index.ai_outcomes.backlash_events",
                                         job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")).result()
    oc = outcome_tests(head, dims, ev)
    OUT.mkdir(exist_ok=True)
    (OUT / "validation.md").write_text(report(face, corr, oc))
    face.to_csv(OUT / "validation_face.csv", index=False)
    corr.to_csv(OUT / "validation_external.csv", index=False)
    print(report(face, corr, oc)[:3000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
