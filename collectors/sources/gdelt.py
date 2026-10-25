"""GDELT news attention: share of US coverage, and its tone, for each dimension's topics.

Uses the GDELT DOC 2.0 API in timeline mode, which returns, per day, the
percentage of all monitored articles matching a query (mind share), or their
average tone. Coverage starts January 2017. The API allows one request every
five seconds, so this collector paces itself. Free for commercial use with
citation.

Catalog codes are '<query key>:<vol|tone>'. Queries are defined below.
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import time
from urllib.parse import urlencode

from collectors.core import to_date

API = "https://api.gdeltproject.org/api/v2/doc/doc"
DATA_START = dt.date(2017, 1, 1)
PAUSE_SECONDS = 8.0

# Each query is restricted to US-based outlets (sourcecountry:US) so the series
# measure what Americans are reading, not world coverage.
QUERIES = {
    "cost_of_living": '(inflation OR "cost of living" OR "grocery prices" OR "food prices" OR "gas prices" OR "rent prices" OR tariffs OR "price increases") sourcecountry:US',
    "jobs_financial": '(layoffs OR "job cuts" OR unemployment OR recession OR "stock market" OR "interest rates" OR "Federal Reserve" OR "credit card debt") sourcecountry:US',
    "political": '("government shutdown" OR impeachment OR "executive order" OR "constitutional crisis" OR "Supreme Court" OR "martial law" OR "election fraud" OR "political crisis") sourcecountry:US',
    "safety_unrest": '("mass shooting" OR "school shooting" OR protests OR riot OR "political violence" OR "hate crime" OR "domestic terrorism" OR "violent crime") sourcecountry:US',
    "disasters_health": '(hurricane OR wildfire OR earthquake OR tornado OR flooding OR "heat wave" OR outbreak OR pandemic OR measles OR "bird flu") sourcecountry:US',
    "geopolitical": '(war OR "nuclear weapons" OR Iran OR Russia OR Ukraine OR Taiwan OR "Middle East" OR terrorism OR "military strike" OR sanctions) sourcecountry:US',
    "anxiety": '(anxiety OR "mental health" OR "panic" OR "stress levels" OR "burnout") sourcecountry:US',
    "boycott": '(boycott OR backlash OR "public outrage" OR "calls for resignation" OR "faces criticism") sourcecountry:US',
}


def year_chunks(start: dt.date, end: dt.date):
    cur = start
    while cur <= end:
        nxt = min(dt.date(cur.year + 1, 1, 1) - dt.timedelta(days=1), end)
        yield cur, nxt
        cur = nxt + dt.timedelta(days=1)


def parse_timeline(content: bytes) -> list[tuple[dt.date, float]]:
    """Timeline CSV: Date,Series,Value (one row per day)."""
    text = content.decode("utf-8-sig", errors="replace")  # strips the byte-order mark
    rows = []
    for rec in csv.DictReader(io.StringIO(text)):
        d = to_date((rec.get("Date") or "").strip())
        v = rec.get("Value")
        if d is not None and v not in (None, ""):
            try:
                rows.append((d, float(v)))
            except ValueError:
                continue
    return rows


def collect(col, series: list[dict]) -> None:
    start = DATA_START if col.mode == "backfill" else max(DATA_START, col.window_start)
    end = col.snapshot_at.date() - dt.timedelta(days=1)
    for s in series:
        key, _, kind = s["code"].partition(":")
        if key not in QUERIES or kind not in {"vol", "tone"}:
            col.warn(f"{s['id']}: unknown code {s['code']!r}")
            continue
        mode = "timelinevol" if kind == "vol" else "timelinetone"
        total = 0
        for a, b in year_chunks(start, end):
            params = {"query": QUERIES[key], "mode": mode, "format": "csv",
                      "startdatetime": f"{a:%Y%m%d}000000", "enddatetime": f"{b:%Y%m%d}235959"}
            url = f"{API}?{urlencode(params)}"
            content = None
            for attempt in range(6):
                try:
                    content, uri = col.fetch(url, name=f"{s['id']}_{a.year}", ext="csv", retries=1)
                    break
                except Exception as exc:
                    if "429" in str(exc) or "limit requests" in str(exc):
                        time.sleep(45)  # the API's limiter wants a real pause, not a quick retry
                        continue
                    col.warn(f"{s['id']} {a.year}: {str(exc)[-300:]}")
                    break
            if content is None:
                col.warn(f"{s['id']} {a.year}: still rate-limited after 6 attempts")
                time.sleep(PAUSE_SECONDS)
                continue
            rows = parse_timeline(content)
            if not rows:
                col.warn(f"{s['id']} {a.year}: empty response: {content[:120]!r}")
            total += sum(col.add_obs(s["id"], d, v, uri) for d, v in rows)
            time.sleep(PAUSE_SECONDS)
        col.info(f"{s['id']}: {total} days loaded")
        col.flush()  # save each series as it completes
