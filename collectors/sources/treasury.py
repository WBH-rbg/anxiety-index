"""US Treasury daily yield curves: nominal and real (TIPS). Public domain.

Uses Treasury's XML data feed, one request per year. Breakeven inflation
(market-implied inflation expectations) is derived later as nominal minus
real yield for the same maturity. Nominal from 1990, real from 2003.
"""
from __future__ import annotations

import datetime as dt
import xml.etree.ElementTree as ET

URL = ("https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xml"
       "?data={kind}&field_tdr_date_value={year}")
KINDS = {"nominal": "daily_treasury_yield_curve", "real": "daily_treasury_real_yield_curve"}
START_YEAR = {"nominal": 2000, "real": 2003}
NS = {"a": "http://www.w3.org/2005/Atom", "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata",
      "d": "http://schemas.microsoft.com/ado/2007/08/dataservices"}


def parse_feed(content: bytes) -> list[dict]:
    """Each entry becomes {'date': date, '<field>': value, ...} with Treasury's own field names."""
    root = ET.fromstring(content)
    rows = []
    for entry in root.findall("a:entry", NS):
        props = entry.find("a:content/m:properties", NS)
        if props is None:
            continue
        row = {}
        for child in props:
            tag = child.tag.split("}")[-1]
            row[tag] = child.text
        date_text = row.get("NEW_DATE") or row.get("DATE") or ""
        try:
            row["date"] = dt.date.fromisoformat(date_text[:10])
        except ValueError:
            continue
        rows.append(row)
    return rows


def collect(col, series: list[dict]) -> None:
    by_kind: dict[str, dict[str, str]] = {}
    for s in series:
        kind, _, field = s["code"].partition(":")
        by_kind.setdefault(kind, {})[s["id"]] = field
    this_year = col.snapshot_at.year
    for kind, wanted in by_kind.items():
        if kind not in KINDS:
            col.warn(f"unknown curve kind {kind!r}")
            continue
        years = list(range(START_YEAR[kind], this_year + 1)) if col.mode == "backfill" else [this_year - 1, this_year]
        counts = {sid: 0 for sid in wanted}
        for year in years:
            try:
                content, uri = col.fetch(URL.format(year=year, kind=KINDS[kind]), name=f"{kind}_{year}", ext="xml")
                rows = parse_feed(content)
            except Exception as exc:
                col.warn(f"{kind} {year}: {type(exc).__name__}: {str(exc)[:200]}")
                continue
            if not rows:
                col.warn(f"{kind} {year}: no entries; starts {content[:200]!r}")
                continue
            for sid, field in wanted.items():
                if field not in rows[0] and year == years[-1]:
                    col.warn(f"{sid}: field {field!r} not among {sorted(rows[0])[:30]}")
                counts[sid] += sum(col.add_obs(sid, r["date"], r.get(field), uri) for r in rows)
        for sid, n in counts.items():
            col.info(f"{sid}: {n} days loaded")
