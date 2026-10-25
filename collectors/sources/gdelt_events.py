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
       SAFE_DIVIDE(SUM(GoldsteinScale * NumMentions), SUM(NumMentions)) AS goldstein
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
}


def _share(part, total):
    return None if not total else 100.0 * float(part) / float(total)


def collect(col, series: list[dict]) -> None:
    from google.cloud import bigquery
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
