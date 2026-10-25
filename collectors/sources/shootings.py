"""Mass shootings in the United States, 1982 to present (Mother Jones database).

An open spreadsheet of indiscriminate public mass shootings (the standard
research dataset for nationally salient incidents). Research use; cite Mother
Jones. Each incident becomes an event with fatalities as its magnitude.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import io

import pandas as pd

from collectors.core import to_date

SHEET_ID = "1b9o6uDO18sLxBqPwl_Gh9bnhW-ev_dABH83M5Vb5L8o"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"


def _col(frame: pd.DataFrame, *candidates: str) -> str | None:
    cols = {str(c).strip().lower(): c for c in frame.columns}
    for cand in candidates:
        for key, orig in cols.items():
            if key == cand or key.startswith(cand):
                return orig
    return None


def parse(content: bytes) -> list[dict]:
    frame = pd.read_csv(io.BytesIO(content), dtype=str, encoding_errors="replace")
    c_case, c_loc, c_date = _col(frame, "case"), _col(frame, "location"), _col(frame, "date")
    c_fat, c_inj, c_tot = _col(frame, "fatalities"), _col(frame, "injured"), _col(frame, "total_victims", "total victims")
    c_type, c_lat, c_lon = _col(frame, "location.1", "location_type", "type"), _col(frame, "latitude"), _col(frame, "longitude")
    if not (c_case and c_date and c_fat):
        raise ValueError(f"unexpected columns: {list(frame.columns)[:15]}")
    out = []
    for _, r in frame.iterrows():
        d = to_date(str(r[c_date]).strip())
        if d is None:
            # formats like 10/1/2017 without zero padding
            try:
                d = pd.to_datetime(str(r[c_date]).strip(), errors="coerce")
                d = None if pd.isna(d) else d.date()
            except Exception:
                d = None
        if d is None:
            continue
        fat = pd.to_numeric(str(r[c_fat]).replace(",", ""), errors="coerce")
        place = str(r[c_loc]) if c_loc else ""
        state = place.split(",")[-1].strip() if "," in place else None
        out.append({
            "event_id": hashlib.sha1(f"{r[c_case]}|{d}".encode()).hexdigest()[:16],
            "event_date": d, "event_type": "mass_shooting", "state": state, "area": place,
            "magnitude": None if pd.isna(fat) else float(fat), "title": str(r[c_case]),
            "latitude": pd.to_numeric(r[c_lat], errors="coerce") if c_lat else None,
            "longitude": pd.to_numeric(r[c_lon], errors="coerce") if c_lon else None,
            "attributes": {"injured": r[c_inj] if c_inj else None, "total_victims": r[c_tot] if c_tot else None,
                           "location_type": r[c_type] if c_type else None},
        })
    return out


def collect(col, series: list[dict]) -> None:
    content, uri = col.fetch(URL, name="mother_jones_mass_shootings", ext="csv")
    incidents = parse(content)
    n = sum(col.add_event(uri=uri, **e) for e in incidents)
    latest = max((e["event_date"] for e in incidents), default=None)
    col.info(f"{len(incidents)} incidents in file, {n} loaded, latest {latest}")
