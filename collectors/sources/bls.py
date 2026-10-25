"""Bureau of Labor Statistics: consumer prices, average retail prices, jobs, JOLTS.

Uses the public API v1, which needs no key: up to 25 series and 10 years per
request, and a limited number of requests per day. Backfill needs three
requests per 25 series; a daily incremental run needs one.
"""
from __future__ import annotations

import datetime as dt
import json

API_URL = "https://api.bls.gov/publicAPI/v1/timeseries/data/"
MAX_SERIES = 25
BACKFILL_START_YEAR = 2000


def year_windows(mode: str, this_year: int) -> list[tuple[int, int]]:
    if mode == "backfill":
        windows, start = [], BACKFILL_START_YEAR
        while start <= this_year:
            end = min(start + 9, this_year)
            windows.append((start, end))
            start = end + 1
        return windows
    return [(this_year - 2, this_year)]


def parse_response(payload: dict, code_to_id: dict[str, str]):
    """Yield (series_id, date, value, extra) and a list of messages from a v1 response."""
    messages = [m for m in payload.get("message", []) if m]
    rows = []
    status = payload.get("status")
    if status != "REQUEST_SUCCEEDED":
        messages.insert(0, f"BLS status {status}")
    for series in (payload.get("Results") or {}).get("series", []):
        code = series.get("seriesID")
        series_id = code_to_id.get(code)
        if series_id is None:
            messages.append(f"unexpected series {code}")
            continue
        for item in series.get("data", []):
            period = item.get("period", "")
            if not period.startswith("M") or period == "M13":  # skip annual averages
                continue
            try:
                obs_date = dt.date(int(item["year"]), int(period[1:]), 1)
            except (KeyError, ValueError):
                continue
            notes = [f.get("text") for f in item.get("footnotes", []) if f and f.get("text")]
            extra = {"period": period}
            if notes:
                extra["footnotes"] = notes
            if item.get("latest") == "true":
                extra["latest"] = True
            rows.append((series_id, obs_date, item.get("value"), extra))
    return rows, messages


def collect(col, series: list[dict]) -> None:
    code_to_id = {s["code"]: s["id"] for s in series}
    codes = list(code_to_id)
    this_year = col.snapshot_at.year
    missing_values = 0
    for i in range(0, len(codes), MAX_SERIES):
        chunk = codes[i:i + MAX_SERIES]
        for start, end in year_windows(col.mode, this_year):
            body = {"seriesid": chunk, "startyear": str(start), "endyear": str(end)}
            content, uri = col.fetch(API_URL, method="POST", json_body=body,
                                     name=f"bls_{start}_{end}_part{i // MAX_SERIES + 1}", ext="json")
            payload = json.loads(content)
            rows, messages = parse_response(payload, code_to_id)
            for msg in messages:
                (col.warn if "status" in msg.lower() or "invalid" in msg.lower() else col.info)(msg)
            if payload.get("status") == "REQUEST_NOT_PROCESSED":
                return  # daily limit reached; stop rather than burn more requests
            for series_id, obs_date, value, extra in rows:
                if not col.add_obs(series_id, obs_date, value, uri, extra):
                    if col.in_window(obs_date):
                        missing_values += 1
    if missing_values:
        col.info(f"{missing_values} values were blank or unavailable (for example, months skipped by the 2025 shutdown)")
