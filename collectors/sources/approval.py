"""Presidential approval polls, poll by poll, so the index computes its own average.

Two open sources:
  1. Wikipedia's "Opinion polling on the ... presidency" pages (2017 onward), which
     list individual polls from many pollsters (Economist/YouGov, Reuters/Ipsos,
     Morning Consult, Quinnipiac, CNN, AP-NORC and others). Fetched through the
     MediaWiki API as rendered HTML. Content is CC BY-SA.
  2. The American Presidency Project's "Presidential Job Approval, All Data"
     table (Gallup-based, 1941 to 2025) for history before 2017.

Each poll is stored as an event (event_date = last day of fieldwork) with
approve, disapprove, sample size and pollster in attributes. Research use for
now; rights to be confirmed before commercial publication.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import re
from urllib.parse import urlencode

import pandas as pd

WIKI_API = "https://en.wikipedia.org/w/api.php"
WIKI_PAGES = [
    "Opinion polling on the second Trump presidency",
    "2024–2025 opinion polling on the Biden administration",
    "2023 opinion polling on the Biden administration",
    "2022 opinion polling on the Biden administration",
    "2021 opinion polling on the Biden administration",
    "Opinion polling on the first Trump presidency",
    "2020 opinion polling on the Trump administration",
    "2019 opinion polling on the Trump administration",
    "2018 opinion polling on the Trump administration",
    "2017 opinion polling on the Trump administration",
]
APP_PAGES = {  # American Presidency Project, Gallup-based approval by president
    "George W. Bush": "https://www.presidency.ucsb.edu/statistics/data/george-w-bush-public-approval",
    "Barack Obama": "https://www.presidency.ucsb.edu/statistics/data/barack-obama-public-approval",
    "Donald J. Trump": "https://www.presidency.ucsb.edu/statistics/data/donald-j-trump-public-approval",
    "Joseph R. Biden": "https://www.presidency.ucsb.edu/statistics/data/joseph-r-biden-public-approval",
}

MONTHS = {m.lower(): i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], 1)}
MONTHS.update({k[:3]: v for k, v in list(MONTHS.items())})
MONTHS["sept"] = 9
DATE_TOKEN = re.compile(r"([A-Za-z]{3,9})\.?\s*(\d{1,2})(?:\s*[–\-−]\s*(?:([A-Za-z]{3,9})\.?\s*)?(\d{1,2}))?,?\s*(\d{4})?")
NUMBER = re.compile(r"(\d{1,6}(?:\.\d+)?)")


def parse_end_date(text: str, default_year: int | None) -> dt.date | None:
    """Last fieldwork day from strings like 'Oct 17–20, 2026', 'Oct 29 – Nov 1, 2026', 'January 5, 2025'."""
    text = str(text).replace("\xa0", " ")
    best = None
    for m in DATE_TOKEN.finditer(text):
        m1, d1, m2, d2, year = m.groups()
        month = MONTHS.get((m2 or m1).lower().rstrip("."))
        if month is None:
            continue
        day = int(d2 or d1)
        y = int(year) if year else default_year
        if y is None:
            continue
        try:
            best = dt.date(y, month, day)
        except ValueError:
            continue
    return best


def first_number(cell) -> float | None:
    m = NUMBER.search(str(cell).replace(",", ""))
    return float(m.group(1)) if m else None


def tables_with_headings(html: str) -> list[tuple[str, pd.DataFrame]]:
    """(nearest preceding heading, table) for every table in the page, in order."""
    from lxml import html as lh
    doc = lh.fromstring(html)
    out, heading = [], ""
    for el in doc.iter():
        if el.tag in ("h2", "h3", "h4"):
            heading = el.text_content().strip()
        elif el.tag == "table":
            try:
                frames = pd.read_html(io.StringIO(lh.tostring(el, encoding="unicode")))
            except ValueError:
                continue
            for f in frames:
                out.append((heading, f))
    return out


def flatten_columns(frame: pd.DataFrame) -> list[str]:
    cols = []
    for c in frame.columns:
        parts = [str(p) for p in (c if isinstance(c, tuple) else (c,)) if str(p) != "nan"]
        cols.append(" ".join(parts).strip().lower())
    return cols


def polls_from_wikipedia(html: str, page: str) -> list[dict]:
    polls = []
    for heading, frame in tables_with_headings(html):
        cols = flatten_columns(frame)
        try:
            i_app = next(i for i, c in enumerate(cols) if "approve" in c and "dis" not in c)
            i_dis = next(i for i, c in enumerate(cols) if "disapprove" in c)
            i_date = next(i for i, c in enumerate(cols) if "date" in c or "fieldwork" in c)
        except StopIteration:
            continue
        if any("aggregator" in c or "updated" in c for c in cols):
            continue  # polling averages, not polls
        i_src = next((i for i, c in enumerate(cols) if "poll" in c or "source" in c), 0)
        i_n = next((i for i, c in enumerate(cols) if "sample" in c), None)
        year_m = re.search(r"(20\d{2})", heading) or re.search(r"(20\d{2})", page)
        default_year = int(year_m.group(1)) if year_m else None
        for _, row in frame.iterrows():
            end = parse_end_date(row.iloc[i_date], default_year)
            app, dis = first_number(row.iloc[i_app]), first_number(row.iloc[i_dis])
            if end is None or app is None or dis is None or not (0 < app < 100 and 0 < dis < 100):
                continue
            pollster = re.sub(r"\[.*?\]", "", str(row.iloc[i_src])).strip()
            if not pollster or pollster.lower() in {"nan", "poll source"}:
                continue
            polls.append({"pollster": pollster, "end_date": end, "approve": app, "disapprove": dis,
                          "sample": first_number(row.iloc[i_n]) if i_n is not None else None,
                          "source_page": page})
    return polls


def polls_from_app(html: str) -> list[dict]:
    frames = pd.read_html(io.StringIO(html))
    polls = []
    for f in frames:
        cols = flatten_columns(f)
        try:
            i_end = next(i for i, c in enumerate(cols) if "end" in c)
            i_app = next(i for i, c in enumerate(cols) if "approv" in c and "dis" not in c)
            i_dis = next(i for i, c in enumerate(cols) if "disapprov" in c)
        except StopIteration:
            continue
        for _, row in f.iterrows():
            end = pd.to_datetime(str(row.iloc[i_end]), errors="coerce")
            app, dis = first_number(row.iloc[i_app]), first_number(row.iloc[i_dis])
            if pd.isna(end) or app is None or dis is None:
                continue
            polls.append({"pollster": "Gallup", "end_date": end.date(), "approve": app, "disapprove": dis,
                          "sample": None, "source_page": "American Presidency Project"})
    return polls


def poll_id(p: dict) -> str:
    key = f"{p['pollster']}|{p['end_date']}|{p['approve']}|{p['disapprove']}"
    return hashlib.sha1(key.encode()).hexdigest()[:16]


def collect(col, series: list[dict]) -> None:
    total = 0
    pages = WIKI_PAGES if col.mode == "backfill" else WIKI_PAGES[:1]
    for page in pages:
        params = {"action": "parse", "page": page, "prop": "text", "format": "json", "formatversion": 2, "redirects": 1}
        try:
            content, uri = col.fetch(f"{WIKI_API}?{urlencode(params)}", name=page, ext="json")
            payload = json.loads(content)
            if "parse" not in payload:
                col.warn(f"{page}: not found ({str(payload.get('error', {}).get('info', ''))[:120]})")
                continue
            html = payload["parse"]["text"]
            polls = polls_from_wikipedia(html, page)
        except Exception as exc:
            col.warn(f"{page}: {type(exc).__name__}: {str(exc)[:200]}")
            continue
        if not polls:
            heads = [flatten_columns(f)[:8] for _, f in tables_with_headings(html)[:6]]
            col.warn(f"{page}: no polls parsed; first table headers: {heads}")
        n = 0
        for p in polls:
            n += col.add_event(event_id=poll_id(p), uri=uri, event_date=p["end_date"], event_type="approval_poll",
                               title=p["pollster"], magnitude=p["approve"] - p["disapprove"],
                               attributes={k: (str(v) if isinstance(v, dt.date) else v) for k, v in p.items()})
        total += n
        col.info(f"{page}: {len(polls)} polls parsed, {n} in window")
    if col.mode == "backfill":
        for president, url in APP_PAGES.items():
            try:
                content, uri = col.fetch(url, name=f"app_{president}", ext="html")
                html = content.decode("utf-8", errors="replace")
                polls = polls_from_app(html)
                if not polls:
                    col.warn(f"APP {president}: no polls parsed; {len(html)} bytes; starts {html[:200]!r}")
                n = sum(col.add_event(event_id=poll_id(p), uri=uri, event_date=p["end_date"], event_type="approval_poll",
                                      title="Gallup", magnitude=p["approve"] - p["disapprove"],
                                      attributes={k: (str(v) if isinstance(v, dt.date) else v) for k, v in p.items()})
                        for p in polls if p["end_date"] >= dt.date(1999, 1, 1))
                total += n
                col.info(f"APP {president}: {len(polls)} Gallup readings parsed, {n} loaded")
            except Exception as exc:
                col.warn(f"APP {president}: {type(exc).__name__}: {str(exc)[:200]}")
    col.info(f"{total} polls loaded")
