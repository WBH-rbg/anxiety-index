"""U.S. Geological Survey earthquake catalog (events).

Collects magnitude 4.0+ earthquakes in US regions and magnitude 6.5+ worldwide.
Backfill requests one year at a time per region to stay under the API's
20,000-event limit.
"""
from __future__ import annotations

import datetime as dt
import json

API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
BACKFILL_START_YEAR = 2000

# name: (min_lat, max_lat, min_lon, max_lon, min_magnitude)
REGIONS = {
    "us_lower48": (24.0, 50.0, -125.5, -66.0, 4.0),
    "us_alaska": (51.0, 72.0, -180.0, -129.0, 4.0),
    "us_hawaii": (18.0, 23.0, -161.0, -154.0, 4.0),
    "us_puerto_rico": (17.5, 18.8, -68.0, -65.0, 4.0),
    "global_major": (-90.0, 90.0, -180.0, 180.0, 6.5),
}


def time_windows(mode: str, now: dt.datetime, window_start: dt.date | None):
    if mode == "backfill":
        for year in range(BACKFILL_START_YEAR, now.year + 1):
            yield dt.date(year, 1, 1), min(dt.date(year + 1, 1, 1), now.date() + dt.timedelta(days=1))
    else:
        yield window_start, now.date() + dt.timedelta(days=1)


def parse_features(payload: dict, region: str) -> list[dict]:
    events = []
    for feat in payload.get("features", []):
        props = feat.get("properties") or {}
        coords = (feat.get("geometry") or {}).get("coordinates") or [None, None, None]
        ms = props.get("time")
        when = dt.datetime.fromtimestamp(ms / 1000, tz=dt.timezone.utc) if ms is not None else None
        events.append({
            "event_id": feat.get("id"),
            "event_time": when,
            "event_type": props.get("type"),
            "area": region,
            "magnitude": props.get("mag"),
            "title": props.get("title"),
            "longitude": coords[0] if len(coords) > 0 else None,
            "latitude": coords[1] if len(coords) > 1 else None,
            "attributes": {k: props.get(k) for k in
                           ("place", "magType", "felt", "cdi", "mmi", "alert", "tsunami", "sig", "status", "url")
                           if props.get(k) is not None} | {"depth_km": coords[2] if len(coords) > 2 else None},
        })
    return events


def collect(col, series: list[dict]) -> None:
    for region, (lat0, lat1, lon0, lon1, min_mag) in REGIONS.items():
        found = 0
        for start, end in time_windows(col.mode, col.snapshot_at, col.window_start):
            params = {
                "format": "geojson", "starttime": start.isoformat(), "endtime": end.isoformat(),
                "minlatitude": lat0, "maxlatitude": lat1, "minlongitude": lon0, "maxlongitude": lon1,
                "minmagnitude": min_mag, "orderby": "time-asc", "limit": 20000,
            }
            try:
                content, uri = col.fetch(API_URL, params=params, name=f"{region}_{start}_{end}", ext="json")
            except Exception as exc:
                col.warn(f"{region} {start}..{end}: {str(exc)[:300]}")
                continue
            events = parse_features(json.loads(content), region)
            if len(events) >= 20000:
                col.warn(f"{region} {start}..{end} hit the 20,000-event limit; narrow the window")
            for e in events:
                found += col.add_event(uri=uri, **e)
        col.info(f"{region}: {found} earthquakes loaded")
