"""GDELT Global Knowledge Graph (BigQuery public table gdelt-bq.gdeltv2.gkg_partitioned, 2015 to present).

For each day: the share of English-language news coverage about the United
States that touches each dimension's themes, and the average tone of that
coverage. Replaces the throttled DOC API. The query runs inside BigQuery
(about 0.5 GB scanned per day); results are archived like any other pull.

Universe: articles written in English (not machine-translated) whose
locations mention the United States. The geopolitical set uses all English
articles, since its subjects are abroad.
"""
from __future__ import annotations

import datetime as dt
import json

from collectors.core import PROJECT_ID

# Theme codes verified against the live table on 2026-10-20. Matching is exact
# on theme boundaries ("...;THEME,offset;..."); NATURAL_DISASTER matches its subtypes.
THEMES = {
    "cost_of_living": ["ECON_INFLATION", "ECON_COST_OF_LIVING", "FUELPRICES", "ECON_HOUSING_PRICES", "ECON_TRADE_DISPUTE"],
    "jobs_financial": ["UNEMPLOYMENT", "WB_2670_JOBS", "ECON_STOCKMARKET", "ECON_INTEREST_RATES", "ECON_BANKRUPTCY", "ECON_DEBT", "STRIKE", "ECON_UNIONS"],
    "political": ["CORRUPTION", "IMPEACHMENT", "SCANDAL", "CONSTITUTIONAL", "POLITICAL_TURMOIL", "STATE_OF_EMERGENCY", "RESIGNATION", "SHUTDOWN", "DEBT_CEILING", "REBELLION"],
    "safety_unrest": ["PROTEST", "VIOLENT_UNREST", "KILL", "TAX_WEAPONS_GUNS", "EXTREMISM", "HATE_SPEECH", "TERRORISM", "ASSASSINATION", "WB_2462_POLITICAL_VIOLENCE_AND_WAR"],
    "disasters_health": ["NATURAL_DISASTER[^,;]*", "WB_2165_HEALTH_EMERGENCIES", "TAX_DISEASE_EPIDEMIC", "TAX_DISEASE_OUTBREAK", "PANDEMIC", "HEALTH_PANDEMIC", "EPIDEMIC", "EVACUATION", "POWER_OUTAGE", "DROUGHT"],
    "geopolitical": ["ARMEDCONFLICT", "WMD", "SANCTIONS", "NUCLEAR", "CYBER_ATTACK", "TERRORISM"],
    "boycott": ["ECON_BOYCOTT"],
}
GLOBAL_SETS = {"geopolitical"}  # no US-location filter


def regex_for(themes: list[str]) -> str:
    return r"(^|;)(" + "|".join(themes) + r"),"


def build_query() -> str:
    cols = []
    for name, themes in THEMES.items():
        base = "is_en" if name in GLOBAL_SETS else "is_us"
        cols.append(f"COUNTIF({base} AND REGEXP_CONTAINS(V2Themes, r'{regex_for(themes)}')) AS n_{name}")
        cols.append(f"AVG(IF({base} AND REGEXP_CONTAINS(V2Themes, r'{regex_for(themes)}'), tone, NULL)) AS tone_{name}")
    return f"""
    WITH articles AS (
      SELECT DATE(_PARTITIONTIME) AS day,
             (TranslationInfo IS NULL OR TranslationInfo = '') AS is_en,
             (TranslationInfo IS NULL OR TranslationInfo = '') AND V2Locations LIKE '%#US#%' AS is_us,
             V2Themes,
             SAFE_CAST(SPLIT(V2Tone, ',')[SAFE_OFFSET(0)] AS FLOAT64) AS tone
      FROM `gdelt-bq.gdeltv2.gkg_partitioned`
      WHERE _PARTITIONTIME >= TIMESTAMP(@start) AND _PARTITIONTIME < TIMESTAMP(@end)
    )
    SELECT day,
           COUNTIF(is_en) AS base_en,
           COUNTIF(is_us) AS base_us,
           AVG(IF(is_us, tone, NULL)) AS tone_us_all,
           {', '.join(cols)}
    FROM articles GROUP BY day ORDER BY day
    """


def series_value(row: dict, code: str):
    kind, _, name = code.partition(":")
    if kind == "share":
        base = row["base_en"] if name in GLOBAL_SETS else row["base_us"]
        return None if not base else 100.0 * float(row[f"n_{name}"] or 0) / float(base)
    if kind == "tone":
        return row.get(f"tone_{name}") if name != "us_all" else row.get("tone_us_all")
    if kind == "base":
        return row.get(f"base_{name}")
    return None


def chunks(start: dt.date, end: dt.date, days: int = 183):
    cur = start
    while cur < end:
        nxt = min(cur + dt.timedelta(days=days), end)
        yield cur, nxt
        cur = nxt


def collect(col, series: list[dict]) -> None:
    from google.cloud import bigquery
    client = bigquery.Client(project=PROJECT_ID)
    end = col.snapshot_at.date()  # partitions are complete up to yesterday
    start = dt.date(2015, 2, 19) if col.mode == "backfill" else end - dt.timedelta(days=7)
    query = build_query()
    total_gb = 0.0
    for a, b in chunks(start, end):
        job = client.query(query, job_config=bigquery.QueryJobConfig(query_parameters=[
            bigquery.ScalarQueryParameter("start", "DATE", a), bigquery.ScalarQueryParameter("end", "DATE", b)]))
        rows = [dict(r) for r in job.result()]
        gb = (job.total_bytes_processed or 0) / 1e9
        total_gb += gb
        uri = col.archive(json.dumps(rows, default=str).encode(), f"gkg_daily_{a}_{b}", "json", "application/json")
        for s in series:
            for r in rows:
                col.add_obs(s["id"], r["day"], series_value(r, s["code"]), uri)
        col.info(f"{a}..{b}: {len(rows)} days, {gb:.1f} GB scanned")
        col.flush()
    col.info(f"total {total_gb:.0f} GB scanned")
