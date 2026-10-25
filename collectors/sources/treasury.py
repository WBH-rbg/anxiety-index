"""US Treasury daily yield curves: nominal and real (TIPS). Public domain.

Breakeven inflation (market-implied inflation expectations) is derived later
as nominal minus real yield for the same maturity. Nominal from 1990, real from 2003.
"""
from __future__ import annotations

import datetime as dt
import io

import pandas as pd

from collectors.core import to_date

URL = ("https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
       "daily-treasury-rates.csv/all/{year}?type={kind}&field_tdr_date_value={year}&page&_format=csv")
KINDS = {"nominal": "daily_treasury_yield_curve", "real": "daily_treasury_real_yield_curve"}
START_YEAR = {"nominal": 2000, "real": 2003}


def parse_curve(content: bytes) -> pd.DataFrame:
    frame = pd.read_csv(io.BytesIO(content))
    frame.columns = [str(c).strip() for c in frame.columns]
    frame["date"] = [to_date(v) for v in frame.iloc[:, 0]]
    return frame[frame["date"].notna()]


def collect(col, series: list[dict]) -> None:
    by_kind: dict[str, dict[str, str]] = {}
    for s in series:
        kind, _, column = s["code"].partition(":")
        by_kind.setdefault(kind, {})[s["id"]] = column
    this_year = col.snapshot_at.year
    for kind, wanted in by_kind.items():
        if kind not in KINDS:
            col.warn(f"unknown curve kind {kind!r}")
            continue
        years = range(START_YEAR[kind], this_year + 1) if col.mode == "backfill" else range(this_year - 1, this_year + 1)
        counts = {sid: 0 for sid in wanted}
        for year in years:
            try:
                content, uri = col.fetch(URL.format(year=year, kind=KINDS[kind]), name=f"{kind}_{year}", ext="csv")
                frame = parse_curve(content)
            except Exception as exc:
                col.warn(f"{kind} {year}: {type(exc).__name__}: {str(exc)[:200]}")
                continue
            for sid, column in wanted.items():
                matches = [c for c in frame.columns if c.strip().lower() == column.strip().lower()]
                if not matches:
                    if year == years[-1]:
                        col.warn(f"{sid}: column {column!r} not in {list(frame.columns)}")
                    continue
                counts[sid] += sum(col.add_obs(sid, d, v, uri) for d, v in zip(frame["date"], frame[matches[0]]))
        for sid, n in counts.items():
            col.info(f"{sid}: {n} days loaded")
