"""Silver Bulletin: every presidential approval poll in Nate Silver's database, as the free CSV the site
offers for download (a published Google Sheet). Second feed for the in-house approval average, next to
the American Presidency Project table.

Terms: the CSV is offered publicly for download, but no reuse license is stated; permission and
attribution are needed before publication. Development use only until then. The column layout is
not documented, so this collector detects columns by name, logs the layout, and fails loudly rather
than loading anything it does not understand.
"""
from __future__ import annotations

import hashlib
import io

import pandas as pd

URL = ("https://docs.google.com/spreadsheets/d/e/2PACX-1vS-FKWVTTFtJT6u56e0bqdfoMcXvDO1DUChsJ3jQAMB2lZk2SMqVfmg7dGjclTYkYWz-Pm5lfcLPjp4"
       "/pub?output=csv")


def _find(cols: list[str], *needles: str, exclude: tuple = ()) -> str | None:
    for c in cols:
        lc = c.lower()
        if any(n in lc for n in needles) and not any(x in lc for x in exclude):
            return c
    return None


def parse(content: bytes) -> tuple[list[dict], str]:
    text = content.decode("utf-8-sig", errors="replace")
    if text.lstrip().startswith("<"):
        raise ValueError("response is HTML, not CSV (sheet unpublished or moved)")
    frame = pd.read_csv(io.StringIO(text), dtype=str)
    cols = [str(c) for c in frame.columns]
    layout = f"{len(frame)} rows; columns: {cols}"
    c_poll = _find(cols, "pollster", "poll")
    c_end = _find(cols, "end", "enddate") or _find(cols, "date", exclude=("start", "created", "updated"))
    c_start = _find(cols, "start")
    c_app = _find(cols, "approve", "yes", exclude=("dis", "adj", "net", "weight"))
    c_dis = _find(cols, "disapprove", "no", exclude=("adj", "net", "weight", "notes"))
    c_n = _find(cols, "sample", "samplesize", " n")
    c_pop = _find(cols, "population", "pop")
    c_spon = _find(cols, "sponsor")
    if not (c_poll and c_end and c_app and c_dis):
        raise ValueError(f"could not identify columns; {layout}")
    polls = []
    for _, r in frame.iterrows():
        end = pd.to_datetime(str(r[c_end]).strip(), errors="coerce")
        app = pd.to_numeric(str(r[c_app]).replace("%", ""), errors="coerce")
        dis = pd.to_numeric(str(r[c_dis]).replace("%", ""), errors="coerce")
        if pd.isna(end) or pd.isna(app) or pd.isna(dis) or not (0 < app < 100 and 0 < dis < 100):
            continue
        pollster = " ".join(str(r[c_poll]).split()).strip()
        if not pollster or pollster.lower() == "nan":
            continue
        sample = pd.to_numeric(str(r[c_n]).replace(",", ""), errors="coerce") if c_n else None
        polls.append({"pollster": pollster, "end_date": end.date(),
                      "start_date": (lambda s: None if pd.isna(s) else str(s.date()))(pd.to_datetime(str(r[c_start]), errors="coerce")) if c_start else None,
                      "approve": float(app), "disapprove": float(dis),
                      "sample": None if sample is None or pd.isna(sample) else float(sample),
                      "population": str(r[c_pop]).strip() if c_pop else None,
                      "sponsor": str(r[c_spon]).strip() if c_spon and str(r[c_spon]) != "nan" else None,
                      "source_page": "Silver Bulletin"})
    return polls, layout


def poll_id(p: dict) -> str:
    key = f"{p['pollster']}|{p['end_date']}|{p['approve']}|{p['disapprove']}|{p.get('population')}"
    return hashlib.sha1(key.encode()).hexdigest()[:16]


def collect(col, series: list[dict]) -> None:
    content, uri = col.fetch(URL, name="silverbulletin_approval_polls", ext="csv")
    polls, layout = parse(content)
    col.info(f"layout: {layout[:400]}")
    if not polls:
        col.warn("no polls parsed")
        return
    cutoff = col.window_start if col.mode == "incremental" else None
    n = 0
    for p in polls:
        if cutoff is not None and p["end_date"] < cutoff:
            continue
        n += col.add_event(event_id=poll_id(p), uri=uri, event_date=p["end_date"], event_type="approval_poll",
                           title=p["pollster"], magnitude=p["approve"] - p["disapprove"],
                           attributes={k: (str(v) if hasattr(v, "isoformat") else v) for k, v in p.items()})
    pollsters = sorted({p["pollster"] for p in polls})
    col.info(f"{len(polls)} polls in file from {len(pollsters)} pollsters, {n} loaded, latest {max(p['end_date'] for p in polls)}")
