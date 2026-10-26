"""GDELT 1.0 events (BigQuery public table gdelt-bq.full.events, 1979 to present).

Daily counts of news-reported events located in the United States, by CAMEO
root code, mention-weighted. Gives attention series back to 2000, before the
DOC API (2017) and Wikipedia (2015) begin:

  share of US event mentions that are protests (code 14), violence (18-20),
  threats and coercion (13, 17); the average tone of all US events; total mentions.

The query runs inside BigQuery (about 36 GB scanned for a full backfill; a
few hundred MB for an incremental run). Results are archived to Cloud Storage
like any other pull.
"""
from __future__ import annotations

import datetime as dt
import json

from collectors.core import PROJECT_ID

QUERY = """
SELECT SQLDATE AS day,
       SUM(NumMentions) AS mentions,
       SUM(IF(EventRootCode = '14', NumMentions, 0)) AS protest,
       SUM(IF(EventRootCode IN ('18', '19', '20'), NumMentions, 0)) AS violence,
       SUM(IF(EventRootCode IN ('13', '17'), NumMentions, 0)) AS coerce,
       SUM(IF(EventRootCode IN ('14', '15', '16', '17', '18', '19', '20'), NumMentions, 0)) AS conflict,
       SAFE_DIVIDE(SUM(AvgTone * NumMentions), SUM(NumMentions)) AS tone,
       SAFE_DIVIDE(SUM(GoldsteinScale * NumMentions), SUM(NumMentions)) AS goldstein,
       SUM(IF(Actor2Type1Code IN ('BUS', 'MNC') AND EventRootCode IN ('10', '11', '12', '13', '14', '17'), NumMentions, 0)) AS hostile_vs_business,
       SUM(IF(Actor2Type1Code IN ('BUS', 'MNC'), NumMentions, 0)) AS all_vs_business
FROM `gdelt-bq.full.events`
WHERE ActionGeo_CountryCode = 'US' AND SQLDATE >= @start AND SQLDATE <= @end
GROUP BY day ORDER BY day
"""

SERIES = {
    "protest_share": lambda r: _share(r["protest"], r["mentions"]),
    "violence_share": lambda r: _share(r["violence"], r["mentions"]),
    "coerce_share": lambda r: _share(r["coerce"], r["mentions"]),
    "conflict_share": lambda r: _share(r["conflict"], r["mentions"]),
    "tone": lambda r: r["tone"],
    "goldstein": lambda r: r["goldstein"],
    "mentions": lambda r: r["mentions"],
    "corp_pressure_share": lambda r: _share(r["hostile_vs_business"], r["mentions"]),
    "corp_hostile_ratio": lambda r: _share(r["hostile_vs_business"], r["all_vs_business"]),
}

# Weekly list of businesses on the receiving end of hostile events: the seed for the outcome log.
TARGETS_QUERY = """
CREATE OR REPLACE TABLE `anxiety-index.ai_outcomes.company_pressure_weekly`
OPTIONS(description='Businesses targeted by demands, disapproval, threats, protests or coercion in US-located GDELT events, by week. Systematic seed for the outcome log; not curated.')
AS
SELECT DATE_ADD(PARSE_DATE('%Y%m%d', CAST(SQLDATE AS STRING)), INTERVAL MOD(7 - EXTRACT(DAYOFWEEK FROM PARSE_DATE('%Y%m%d', CAST(SQLDATE AS STRING))), 7) DAY) AS week,
       Actor2Name AS target, COUNT(*) AS events, SUM(NumMentions) AS mentions,
       SAFE_DIVIDE(SUM(AvgTone * NumMentions), SUM(NumMentions)) AS tone, CURRENT_TIMESTAMP() AS loaded_at
FROM `gdelt-bq.full.events`
WHERE ActionGeo_CountryCode = 'US' AND SQLDATE >= 20150101 AND Actor2Type1Code IN ('BUS', 'MNC')
  AND EventRootCode IN ('10', '11', '12', '13', '14', '17') AND Actor2Name IS NOT NULL
GROUP BY 1, 2 HAVING mentions >= 100
"""


def _share(part, total):
    return None if not total else 100.0 * float(part) / float(total)


def collect(col, series: list[dict]) -> None:
    from google.cloud import bigquery
    if col.mode == "incremental" and col.snapshot_at.weekday() != 0:
        col.info("skipped: the events table isn't partitioned (every query scans ~30 GB), so this runs weekly on Mondays")
        return
    start = dt.date(2000, 1, 1) if col.mode == "backfill" else col.window_start
    end = col.snapshot_at.date()
    client = bigquery.Client(project=PROJECT_ID)
    job = client.query(QUERY, job_config=bigquery.QueryJobConfig(query_parameters=[
        bigquery.ScalarQueryParameter("start", "INT64", int(f"{start:%Y%m%d}")),
        bigquery.ScalarQueryParameter("end", "INT64", int(f"{end:%Y%m%d}")),
    ]))
    rows = [dict(r) for r in job.result()]
    col.info(f"{len(rows)} days from BigQuery, {job.total_bytes_processed / 1e9:.1f} GB scanned")
    uri = col.archive(json.dumps(rows, default=str).encode(), f"us_events_{start}_{end}", "json", "application/json")
    for s in series:
        fn = SERIES.get(s["code"])
        if fn is None:
            col.warn(f"{s['id']}: unknown code {s['code']!r}")
            continue
        added = 0
        for r in rows:
            d = dt.datetime.strptime(str(r["day"]), "%Y%m%d").date()
            added += col.add_obs(s["id"], d, fn(r), uri)
        col.info(f"{s['id']}: {added} days loaded")
    col.flush()
    targets = client.query(TARGETS_QUERY)
    targets.result()
    col.info(f"company_pressure_weekly rebuilt ({(targets.total_bytes_processed or 0) / 1e9:.1f} GB scanned)")
