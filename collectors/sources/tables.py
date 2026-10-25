"""Helpers for sources published as spreadsheets or CSV files with one column per series."""
from __future__ import annotations

import datetime as dt
import io
import re

import pandas as pd

from collectors.core import to_date

DATE_COLUMNS = ("date", "month", "day", "period", "time")


def read_table(content: bytes, ext: str, sheet=0, **kwargs) -> pd.DataFrame:
    """Read a CSV or Excel file. `kwargs` (skiprows, header, ...) go to pandas."""
    if ext == "csv":
        return pd.read_csv(io.BytesIO(content), **kwargs)
    return pd.read_excel(io.BytesIO(content), sheet_name=sheet, **kwargs)


def _norm(name) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(name).lower()).strip()


def find_column(frame: pd.DataFrame, wanted: str) -> str | None:
    """Exact match first, then case/punctuation-insensitive, then 'contains'."""
    if wanted in frame.columns:
        return wanted
    target = _norm(wanted)
    normalized = {_norm(c): c for c in frame.columns}
    if target in normalized:
        return normalized[target]
    matches = [c for n, c in normalized.items() if target and target in n]
    return matches[0] if len(matches) == 1 else None


def _month_number(value):
    text = str(value).strip()[:3].lower()
    names = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    return names.index(text) + 1 if text in names else None


def row_dates(frame: pd.DataFrame) -> list[dt.date | None]:
    """Dates for each row: Year/Month(/Day) columns if present, otherwise a date-like column."""
    cols = {_norm(c): c for c in frame.columns}
    if "yyyy" in cols and "year" not in cols:
        cols["year"] = cols["yyyy"]
    if "year" in cols and "month" in cols:
        years = pd.to_numeric(frame[cols["year"]], errors="coerce")
        months = pd.to_numeric(frame[cols["month"]], errors="coerce")
        if months.isna().all():  # month names such as "January"
            months = pd.Series([_month_number(v) for v in frame[cols["month"]]], index=frame.index, dtype="float")
        days = pd.to_numeric(frame[cols["day"]], errors="coerce") if "day" in cols else None
        out = []
        for i in range(len(frame)):
            y, m = years.iloc[i], months.iloc[i]
            d = days.iloc[i] if days is not None else 1
            try:
                out.append(dt.date(int(y), int(m), int(d)))
            except (ValueError, TypeError):
                out.append(None)
        return out
    for key in DATE_COLUMNS:
        if key in cols:
            return [to_date(v) for v in frame[cols[key]]]
    return [to_date(v) for v in frame.iloc[:, 0]]


def extract_series(frame: pd.DataFrame, wanted: dict[str, str]) -> tuple[dict[str, list], list[str]]:
    """Map series_id -> [(date, value), ...] for each wanted column name. Also returns missing columns."""
    dates = row_dates(frame)
    out, missing = {}, []
    for series_id, column in wanted.items():
        col = find_column(frame, column)
        if col is None:
            missing.append(column)
            continue
        out[series_id] = [(d, v) for d, v in zip(dates, frame[col]) if d is not None]
    return out, missing


def describe(content: bytes, ext: str, frame: pd.DataFrame) -> str:
    """A short description of a file's layout, for the run log."""
    parts = []
    if ext != "csv":
        try:
            parts.append(f"sheets={pd.ExcelFile(io.BytesIO(content)).sheet_names}")
        except Exception as exc:
            parts.append(f"sheets unreadable ({type(exc).__name__})")
    parts.append("first rows=" + frame.head(4).to_string(max_cols=8, max_colwidth=24).replace("\n", " // ")[:600])
    return " ".join(parts)


def collect_files(col, series: list[dict], files: dict[str, tuple]) -> None:
    """Shared collect loop. `files` maps a file key to (url, ext, sheet) or
    (url, ext, sheet, pandas_kwargs). Catalog codes look like '<file key>:<column name>'."""
    by_file: dict[str, dict[str, str]] = {}
    for s in series:
        key, _, column = s["code"].partition(":")
        by_file.setdefault(key, {})[s["id"]] = column
    for key, wanted in by_file.items():
        if key not in files:
            col.warn(f"no file configured for '{key}'")
            continue
        url, ext, sheet, *rest = files[key]
        kwargs = rest[0] if rest else {}
        try:
            content, uri = col.fetch(url, name=key, ext=ext)
            frame = read_table(content, ext, sheet, **kwargs)
        except Exception as exc:
            detail = ""
            if ext != "csv" and "content" in locals():
                try:
                    detail = f"; sheets={pd.ExcelFile(io.BytesIO(content)).sheet_names}"
                except Exception:
                    pass
            col.warn(f"{key}: {type(exc).__name__}: {str(exc)[:300]}{detail}")
            continue
        found, missing = extract_series(frame, wanted)
        if missing:
            col.warn(f"{key}: columns not found {missing}; available: {[str(c) for c in frame.columns][:40]}")
        if missing or any(len(rows) == 0 for rows in found.values()):
            col.warn(f"{key}: layout: {describe(content, ext, frame)}")
        for series_id, rows in found.items():
            added = sum(col.add_obs(series_id, d, v, uri) for d, v in rows)
            latest = max((d for d, v in rows if v == v and v is not None), default=None)
            col.info(f"{series_id}: {len(rows)} rows, {added} loaded, latest {latest}")
