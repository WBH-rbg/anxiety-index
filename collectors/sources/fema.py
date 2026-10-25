"""FEMA disaster declarations (events), from the OpenFEMA API (no key).

One record per declared county or area. Backfill loads every declaration since
2000; incremental runs reload declarations from the recent window, so later
amendments are captured as new snapshots.
Required notice: this product uses FEMA's OpenFEMA API but is not endorsed by FEMA.
"""
from __future__ import annotations

import datetime as dt
import json
from urllib.parse import quote

API_URL = "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries"
PAGE = 10000
BACKFILL_START = dt.date(2000, 1, 1)


def page_url(since: dt.date, skip: int) -> str:
    flt = f"declarationDate ge '{since.isoformat()}T00:00:00.000Z'"
    return (f"{API_URL}?$filter={quote(flt)}&$orderby=id&$top={PAGE}&$skip={skip}")


def parse_records(payload: dict) -> list[dict]:
    out = []
    for r in payload.get("DisasterDeclarationsSummaries", []):
        declared = r.get("declarationDate")
        when = dt.datetime.fromisoformat(declared.replace("Z", "+00:00")) if declared else None
        out.append({
            "event_id": r.get("id"),
            "event_time": when,
            "event_type": r.get("incidentType"),
            "state": r.get("state"),
            "area": r.get("designatedArea"),
            "title": r.get("declarationTitle"),
            "attributes": {k: r.get(k) for k in (
                "femaDeclarationString", "disasterNumber", "declarationType", "incidentBeginDate",
                "incidentEndDate", "fipsStateCode", "fipsCountyCode", "ihProgramDeclared",
                "iaProgramDeclared", "paProgramDeclared", "hmProgramDeclared", "tribalRequest",
                "region", "designatedIncidentTypes", "lastRefresh") if r.get(k) is not None},
        })
    return out


def collect(col, series: list[dict]) -> None:
    since = BACKFILL_START if col.mode == "backfill" else col.window_start
    skip, total = 0, 0
    while True:
        content, uri = col.fetch(page_url(since, skip), name=f"declarations_since_{since}_skip{skip}", ext="json")
        records = parse_records(json.loads(content))
        for r in records:
            total += col.add_event(uri=uri, **r)
        if len(records) < PAGE:
            break
        skip += PAGE
    col.info(f"{total} county-level declaration records loaded since {since}")
