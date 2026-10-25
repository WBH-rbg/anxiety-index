"""Shared plumbing for every collector: fetching, archiving, loading, and run logging.

Each collector receives a `Collection`, calls `fetch()` for every file it needs
(each response is archived unchanged to Cloud Storage before parsing), adds
parsed rows with `add_obs()` / `add_event()`, and the runner calls `finish()`
to load rows into BigQuery and record the run in `ai_raw.runs`.
"""
from __future__ import annotations

import datetime as dt
import json
import math
import os
import re
import time
import uuid
from pathlib import Path

import requests
import yaml

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "anxiety-index")
BUCKET = os.environ.get("GCS_RAW_BUCKET", "anxiety-index-raw-archive")
USER_AGENT = "AnxietyIndex/0.1 (research index; +https://github.com/WBH-rbg/anxiety-index)"
RETRY_STATUS = {429, 500, 502, 503, 504}
INCREMENTAL_DAYS = 180          # incremental runs reload this much recent history
LOAD_CHUNK = 50_000
CATALOG_PATH = Path(__file__).resolve().parent.parent / "config" / "series.yaml"


class FetchError(RuntimeError):
    """A source could not be retrieved after retries."""


def utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def clean_number(value):
    """Return a float, or None for blanks, dashes, NaN and other non-numbers."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return None if (isinstance(value, float) and math.isnan(value)) else float(value)
    text = str(value).strip().replace(",", "")
    if text in {"", "-", ".", "NA", "N/A", "nan", "NaN"}:
        return None
    try:
        out = float(text)
    except ValueError:
        return None
    return None if math.isnan(out) else out


def load_catalog(path: Path = CATALOG_PATH) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    series = data["series"]
    ids = [s["id"] for s in series]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"Duplicate series ids in catalog: {sorted(dupes)}")
    return series


class Collection:
    """One collector's work for one run."""

    def __init__(self, source: str, mode: str = "incremental", dry_run: bool = False,
                 snapshot_at: dt.datetime | None = None):
        if mode not in {"incremental", "backfill"}:
            raise ValueError(f"Unknown mode {mode!r}")
        self.source = source
        self.mode = mode
        self.dry_run = dry_run
        self.snapshot_at = snapshot_at or utcnow()
        self.started_at = utcnow()
        self.run_id = uuid.uuid4().hex
        self.observations: list[dict] = []
        self.events: list[dict] = []
        self.uris: list[str] = []
        self.messages: list[str] = []
        self.warnings = 0
        self._storage_bucket = None

    # ---- time window -------------------------------------------------------
    @property
    def window_start(self) -> dt.date | None:
        """Earliest date to load. None means everything (backfill)."""
        if self.mode == "backfill":
            return None
        return self.snapshot_at.date() - dt.timedelta(days=INCREMENTAL_DAYS)

    def in_window(self, d: dt.date) -> bool:
        start = self.window_start
        return start is None or d >= start

    # ---- messages ----------------------------------------------------------
    def info(self, msg: str) -> None:
        self.messages.append(f"INFO {msg}")
        print(f"[{self.source}] {msg}", flush=True)

    def warn(self, msg: str) -> None:
        self.warnings += 1
        self.messages.append(f"WARN {msg}")
        print(f"[{self.source}] WARNING: {msg}", flush=True)

    # ---- fetching and archiving --------------------------------------------
    def fetch(self, url: str, *, name: str, ext: str, method: str = "GET",
              params: dict | None = None, json_body: dict | None = None,
              timeout: int = 120, retries: int = 4, accept_status: tuple = (200,)) -> tuple[bytes, str | None]:
        """Download a URL, archive the raw bytes, and return (content, archive_uri)."""
        last_error = "no attempt made"
        for attempt in range(retries):
            try:
                resp = requests.request(method, url, params=params, json=json_body,
                                        headers={"User-Agent": USER_AGENT}, timeout=timeout)
            except requests.RequestException as exc:
                last_error = f"{type(exc).__name__}: {exc}"
            else:
                if resp.status_code in accept_status:
                    uri = self.archive(resp.content, name, ext, resp.headers.get("Content-Type"))
                    return resp.content, uri
                last_error = f"HTTP {resp.status_code}: {resp.text[:300]!r}"
                if resp.status_code not in RETRY_STATUS:
                    break
            if attempt < retries - 1:
                time.sleep(min(60, 5 * 2 ** attempt))
        raise FetchError(f"{url} -> {last_error}")

    def archive(self, content: bytes, name: str, ext: str, content_type: str | None = None) -> str | None:
        safe = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_")[:120] or "file"
        path = (f"{self.source}/{self.snapshot_at:%Y/%m/%d}/"
                f"{self.snapshot_at:%H%M%SZ}_{self.run_id[:8]}_{safe}.{ext}")
        if self.dry_run:
            return None
        if self._storage_bucket is None:
            from google.cloud import storage  # imported lazily so parsers test without it
            self._storage_bucket = storage.Client(project=PROJECT_ID).bucket(BUCKET)
        blob = self._storage_bucket.blob(path)
        blob.upload_from_string(content, content_type=content_type or "application/octet-stream",
                                if_generation_match=0)  # never overwrite an archived file
        uri = f"gs://{BUCKET}/{path}"
        self.uris.append(uri)
        return uri

    # ---- rows --------------------------------------------------------------
    def add_obs(self, series_id: str, obs_date: dt.date, value, uri: str | None,
                extra: dict | None = None) -> bool:
        num = clean_number(value)
        if num is None or not self.in_window(obs_date):
            return False
        self.observations.append({
            "source": self.source,
            "series_id": series_id,
            "obs_date": obs_date.isoformat(),
            "value": num,
            "snapshot_at": self.snapshot_at.isoformat(),
            "snapshot_uri": uri,
            "extra": extra or None,
        })
        return True

    def add_event(self, *, event_id: str, uri: str | None, event_time: dt.datetime | None = None,
                  event_date: dt.date | None = None, event_type: str | None = None,
                  state: str | None = None, area: str | None = None, magnitude=None,
                  title: str | None = None, latitude=None, longitude=None,
                  attributes: dict | None = None) -> bool:
        day = event_date or (event_time.date() if event_time else None)
        if day is not None and not self.in_window(day):
            return False
        self.events.append({
            "source": self.source,
            "event_id": str(event_id),
            "event_time": event_time.isoformat() if event_time else None,
            "event_date": day.isoformat() if day else None,
            "event_type": event_type,
            "state": state,
            "area": area,
            "magnitude": clean_number(magnitude),
            "title": title,
            "latitude": clean_number(latitude),
            "longitude": clean_number(longitude),
            "attributes": attributes or None,
            "snapshot_at": self.snapshot_at.isoformat(),
            "snapshot_uri": uri,
        })
        return True

    # ---- finishing ---------------------------------------------------------
    def summary(self) -> str:
        return (f"{self.source}: {len(self.observations)} observations, {len(self.events)} events, "
                f"{len(self.uris)} files archived, {self.warnings} warnings")

    def finish(self, status: str) -> str:
        """Load rows into BigQuery and record the run. Returns the final status."""
        if self.dry_run:
            print(self.summary())
            return status
        from google.cloud import bigquery
        client = bigquery.Client(project=PROJECT_ID)
        try:
            load_rows(client, "ai_raw.observations", self.observations)
            load_rows(client, "ai_raw.events", self.events)
        except Exception as exc:  # record the failure, then re-raise after logging
            status = "failed"
            self.messages.append(f"ERROR loading to BigQuery: {type(exc).__name__}: {str(exc)[:2000]}")
        record = {
            "run_id": self.run_id,
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
            "source": self.source,
            "mode": self.mode,
            "started_at": self.started_at.isoformat(),
            "finished_at": utcnow().isoformat(),
            "status": status,
            "observation_rows": len(self.observations) if status != "failed" else 0,
            "event_rows": len(self.events) if status != "failed" else 0,
            "snapshot_uris": self.uris[:500],
            "message": "\n".join(self.messages)[-20000:] or None,
        }
        load_rows(client, "ai_raw.runs", [record])
        print(self.summary(), f"status={status}", flush=True)
        return status


def load_rows(client, table: str, rows: list[dict], write_disposition: str = "WRITE_APPEND") -> None:
    if not rows and write_disposition == "WRITE_APPEND":
        return
    from google.cloud import bigquery
    tbl = client.get_table(f"{PROJECT_ID}.{table}")
    config = bigquery.LoadJobConfig(
        schema=tbl.schema,
        write_disposition=write_disposition,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )
    for i in range(0, max(len(rows), 1), LOAD_CHUNK):
        chunk = rows[i:i + LOAD_CHUNK]
        client.load_table_from_json(chunk, tbl, job_config=config).result()
        config.write_disposition = "WRITE_APPEND"  # only the first chunk truncates


def write_catalog(series: list[dict]) -> None:
    from google.cloud import bigquery
    client = bigquery.Client(project=PROJECT_ID)
    now = utcnow().isoformat()
    rows = [{
        "series_id": s["id"],
        "source": s["source"],
        "source_series_code": s.get("code"),
        "name": s.get("name"),
        "dimension": s.get("dimension"),
        "lens": s.get("lens"),
        "unit": s.get("unit"),
        "frequency": s.get("frequency"),
        "seasonal_adjustment": s.get("sa"),
        "notes": s.get("notes"),
        "updated_at": now,
    } for s in series]
    load_rows(client, "ai_raw.series_catalog", rows, write_disposition="WRITE_TRUNCATE")


def to_date(value) -> dt.date | None:
    """Parse common date representations (datetime, Timestamp, YYYYMMDD, ISO strings)."""
    if value is None:
        return None
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if hasattr(value, "to_pydatetime"):
        try:
            return value.to_pydatetime().date()
        except (ValueError, TypeError):
            return None
    if isinstance(value, (int, float)):
        if isinstance(value, float) and math.isnan(value):
            return None
        text = str(int(value))
    else:
        text = str(value).strip()
    for fmt in ("%Y%m%d", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%m/%d/%Y", "%Y-%m", "%YM%m", "%Y%m"):
        try:
            return dt.datetime.strptime(text[:len(dt.datetime(2000, 1, 1).strftime(fmt))], fmt).date()
        except ValueError:
            continue
    return None
