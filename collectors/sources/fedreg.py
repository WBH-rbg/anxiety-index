"""Federal Register: weekly counts of executive orders, presidential documents, and rules.

A measure of policy churn. Uses the public Federal Register API (no key).
Series codes: 'executive_orders', 'presidential_documents', 'rules', 'proposed_rules'.
"""
from __future__ import annotations

import datetime as dt
import json
from collections import Counter
from urllib.parse import urlencode

API = "https://www.federalregister.gov/api/v1/documents.json"
BACKFILL_START = dt.date(2000, 1, 1)
QUERIES = {
    "executive_orders": {"conditions[type][]": "PRESDOCU", "conditions[presidential_document_type][]": "executive_order"},
    "presidential_documents": {"conditions[type][]": "PRESDOCU"},
    "rules": {"conditions[type][]": "RULE"},
    "proposed_rules": {"conditions[type][]": "PRORULE"},
}


def week_start(d: dt.date) -> dt.date:
    return d - dt.timedelta(days=d.weekday())  # Monday


def count_by_week(col, code: str, start: dt.date, end: dt.date, label: str) -> Counter:
    """Page through documents published in [start, end] and count by week."""
    counts: Counter = Counter()
    page, total = 1, 0
    while True:
        params = {**QUERIES[code], "conditions[publication_date][gte]": start.isoformat(),
                  "conditions[publication_date][lte]": end.isoformat(),
                  "fields[]": "publication_date", "per_page": 1000, "page": page, "order": "oldest"}
        content, uri = col.fetch(f"{API}?{urlencode(params, doseq=True)}", name=f"{code}_{label}_p{page}", ext="json")
        payload = json.loads(content)
        docs = payload.get("results", [])
        for doc in docs:
            d = dt.date.fromisoformat(doc["publication_date"])
            counts[week_start(d)] += 1
        total += len(docs)
        if not payload.get("next_page_url") or not docs:
            break
        page += 1
        if page > 400:
            col.warn(f"{code} {label}: stopped after 400 pages")
            break
    return counts, uri


def collect(col, series: list[dict]) -> None:
    end = col.snapshot_at.date()
    for s in series:
        code = s["code"]
        if code not in QUERIES:
            col.warn(f"{s['id']}: unknown code {code!r}")
            continue
        start = BACKFILL_START if col.mode == "backfill" else col.window_start
        # Rules are voluminous (~4,000/yr): fetch year by year to keep paging bounded.
        chunks = []
        cur = start
        while cur <= end:
            nxt = min(dt.date(cur.year, 12, 31), end)
            chunks.append((cur, nxt))
            cur = nxt + dt.timedelta(days=1)
        weekly: Counter = Counter()
        uri = None
        for a, b in chunks:
            try:
                c, uri = count_by_week(col, code, a, b, str(a.year))
                weekly.update(c)
            except Exception as exc:
                col.warn(f"{s['id']} {a.year}: {str(exc)[:200]}")
        # Every week in range gets a value, including zero weeks; drop the current partial week.
        wk = week_start(start)
        last_full = week_start(end) - dt.timedelta(days=7)
        added = 0
        while wk <= last_full:
            added += col.add_obs(s["id"], wk, float(weekly.get(wk, 0)), uri)
            wk += dt.timedelta(days=7)
        col.info(f"{s['id']}: {added} weeks loaded, {sum(weekly.values())} documents counted")
