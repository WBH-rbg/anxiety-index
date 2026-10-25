"""Wikipedia daily pageviews (Wikimedia Analytics API, CC0), human traffic only.

A proxy for public attention to each dimension's topics. Catalog codes are
English Wikipedia article titles. Data begins July 2015.
"""
from __future__ import annotations

import datetime as dt
import json
from urllib.parse import quote

API = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{title}/daily/{start}/{end}"
DATA_START = dt.date(2015, 7, 1)


def parse_items(payload: dict) -> list[tuple[dt.date, int]]:
    out = []
    for item in payload.get("items", []):
        ts = item.get("timestamp", "")
        try:
            d = dt.date(int(ts[:4]), int(ts[4:6]), int(ts[6:8]))
        except ValueError:
            continue
        out.append((d, item.get("views")))
    return out


def collect(col, series: list[dict]) -> None:
    start = DATA_START if col.mode == "backfill" else max(DATA_START, col.window_start)
    end = col.snapshot_at.date() - dt.timedelta(days=1)
    for s in series:
        title = s["code"].replace(" ", "_")
        url = API.format(title=quote(title, safe=""), start=f"{start:%Y%m%d}00", end=f"{end:%Y%m%d}00")
        try:
            content, uri = col.fetch(url, name=s["id"], ext="json", retries=3)
        except Exception as exc:
            col.warn(f"{s['id']} ({title}): {str(exc)[:200]}")
            continue
        rows = parse_items(json.loads(content))
        added = sum(col.add_obs(s["id"], d, v, uri) for d, v in rows)
        if added == 0:
            col.warn(f"{s['id']} ({title}): no pageviews returned; check the article title")
    col.info(f"{len(series)} articles requested from {start} to {end}")
