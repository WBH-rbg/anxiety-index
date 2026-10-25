"""Department of Labor weekly unemployment insurance claims (ETA 539 state report).

The state-level file lists, for every state and week, initial claims (c3) and
continued weeks claimed (c8). Summing across states gives national,
not-seasonally-adjusted initial and continued claims back to 1987. Public domain.
"""
from __future__ import annotations

import datetime as dt
import io

import pandas as pd

from collectors.core import to_date

URL = "https://oui.doleta.gov/unemploy/csv/ar539.csv"


def parse_national(content: bytes) -> dict[str, list[tuple[dt.date, float]]]:
    frame = pd.read_csv(io.BytesIO(content), dtype=str, encoding_errors="replace")
    frame.columns = [c.strip().lower() for c in frame.columns]
    needed = {"st", "c2", "c3", "c8"}
    if not needed.issubset(frame.columns):
        raise ValueError(f"unexpected columns: {list(frame.columns)[:12]}")
    # c2 = week ending date the claims reflect; c3 = initial claims; c8 = continued weeks claimed
    frame = frame[~frame["st"].isin(["PR", "VI"])]  # national figures exclude territories
    frame["week"] = [to_date(v) for v in frame["c2"]]
    frame = frame[frame["week"].notna()]
    for c in ("c3", "c8"):
        frame[c] = pd.to_numeric(frame[c].str.replace(",", ""), errors="coerce")
    grouped = frame.groupby("week")[["c3", "c8"]].sum(min_count=1)
    counts = frame.groupby("week")["st"].nunique()
    complete = grouped[counts >= 50]  # skip weeks where some states haven't reported yet
    return {
        "initial": [(d, v) for d, v in complete["c3"].items()],
        "continued": [(d, v) for d, v in complete["c8"].items()],
    }


def collect(col, series: list[dict]) -> None:
    content, uri = col.fetch(URL, name="ar539", ext="csv", timeout=300)
    data = parse_national(content)
    for s in series:
        rows = data.get(s["code"])
        if rows is None:
            col.warn(f"{s['id']}: unknown code {s['code']!r}")
            continue
        added = sum(col.add_obs(s["id"], d, v, uri) for d, v in rows)
        col.info(f"{s['id']}: {len(rows)} weeks in file, {added} loaded, latest {rows[-1][0] if rows else 'n/a'}")
