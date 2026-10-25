"""Energy Information Administration: retail gasoline and diesel, crude oil, natural gas.

Uses EIA's public history spreadsheets, which need no API key. Each catalog
entry's `code` is the file path under https://www.eia.gov/dnav/, for example
`pet/hist_xls/EMM_EPMR_PTE_NUS_DPGw.xls`. The data sits on the "Data 1" sheet
under two header rows: a date column, then the value column.
"""
from __future__ import annotations

import io

import pandas as pd

from collectors.core import to_date

BASE = "https://www.eia.gov/dnav/"


def parse_history(content: bytes) -> list[tuple]:
    frame = pd.read_excel(io.BytesIO(content), sheet_name="Data 1", skiprows=2, header=0)
    if frame.shape[1] < 2:
        raise ValueError(f"expected a date and a value column, got {list(frame.columns)}")
    out = []
    for date_value, value in zip(frame.iloc[:, 0], frame.iloc[:, 1]):
        d = to_date(date_value)
        if d is not None:
            out.append((d, value))
    return out


def collect(col, series: list[dict]) -> None:
    for s in series:
        url = BASE + s["code"]
        try:
            content, uri = col.fetch(url, name=s["id"], ext="xls")
            rows = parse_history(content)
        except Exception as exc:
            col.warn(f"{s['id']}: {type(exc).__name__}: {str(exc)[:300]}")
            continue
        added = sum(col.add_obs(s["id"], d, v, uri) for d, v in rows)
        col.info(f"{s['id']}: {len(rows)} rows in file, {added} loaded, latest {rows[-1][0] if rows else 'n/a'}")
