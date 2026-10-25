"""Anxiety Index computation, methodology v0.1.

Pure pandas: takes observation and event DataFrames, returns weekly tables.
No cloud access here, so it can be tested with synthetic data. See
docs/methodology.md for the reasoning behind each step.

Pipeline:
  observations ──> weekly, point-in-time series (value known by each week's end)
               ──> derived series, event impulses
               ──> signals (transforms) ──> standardized (expanding, robust)
               ──> lens scores ──> dimension scores ──> headline ──> percentiles and bands
"""
from __future__ import annotations

import datetime as dt
import math

import numpy as np
import pandas as pd

WEEK_ANCHOR = "W-SAT"  # weeks end on Saturday

# Days after the period ends before a value is public (used for backfilled history,
# where exact release times weren't captured). Monthly periods end at month end.
RELEASE_LAG_DAYS = {
    "bls": 14, "bls_jolts": 35, "eia": 2, "dol": 5, "umich": 0, "nyfed": 10, "gpr": 2,
    "epu": 1, "fedreg": 0, "wikipedia": 1, "gdelt": 1, "treasury": 0, "markets": 0,
    "freddiemac": 0, "tpu": 10, "derived": 0, "events": 0,
}
FREQ_CLASS = {"daily": "daily", "weekly": "weekly", "monthly": "monthly"}


# ----------------------------------------------------------------------------- helpers
def week_end(d: pd.Series) -> pd.Series:
    """Map dates to the Saturday ending their week."""
    d = pd.to_datetime(d)
    return d + pd.to_timedelta((5 - d.dt.weekday) % 7, unit="D")


def release_lag(series_id: str, source: str) -> int:
    if series_id.startswith("bls_jolts"):
        return RELEASE_LAG_DAYS["bls_jolts"]
    return RELEASE_LAG_DAYS.get(source, 7)


def available_date(obs_date: pd.Series, frequency: str, lag_days: int) -> pd.Series:
    obs = pd.to_datetime(obs_date)
    if frequency == "monthly":
        period_end = obs + pd.offsets.MonthEnd(0)
    else:
        period_end = obs
    return period_end + pd.to_timedelta(lag_days, unit="D")


# ----------------------------------------------------------------------------- step 1: weekly point-in-time series
def weekly_series(obs: pd.DataFrame, catalog: pd.DataFrame, weeks: pd.DatetimeIndex) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (values, age_weeks): DataFrames indexed by week, one column per series.

    values[w, s] is the latest value of series s that was public by the end of week w.
    age_weeks[w, s] is how many weeks ago that value became public.
    Daily series are averaged within the week they refer to.
    """
    values, ages = {}, {}
    meta = catalog.set_index("series_id")
    for sid, g in obs.groupby("series_id"):
        if sid not in meta.index:
            continue
        freq = meta.loc[sid, "frequency"]
        source = meta.loc[sid, "source"]
        g = g.sort_values("obs_date")
        if freq == "daily":
            wk = week_end(g["obs_date"])
            per_week = g.groupby(wk)["value"].mean()
            avail_week = per_week.index + pd.to_timedelta(release_lag(sid, source), unit="D")
            avail_week = week_end(pd.Series(avail_week))
            s = pd.Series(per_week.values, index=avail_week.values)
        else:
            avail = available_date(g["obs_date"], freq, release_lag(sid, source))
            aw = week_end(avail)
            s = pd.Series(g["value"].values, index=aw.values)
        # several values can become public the same week: keep the latest period
        s = s.groupby(level=0).last().sort_index()
        s = s[~s.index.duplicated()]
        aligned = s.reindex(weeks)
        known_week = pd.Series(np.where(aligned.notna(), weeks, pd.NaT), index=weeks).ffill()
        values[sid] = aligned.ffill()
        ages[sid] = (pd.Series(weeks, index=weeks) - pd.to_datetime(known_week)).dt.days / 7.0
    return pd.DataFrame(values, index=weeks), pd.DataFrame(ages, index=weeks)


# ----------------------------------------------------------------------------- step 2: derived and event series
def add_derived(values: pd.DataFrame, ages: pd.DataFrame, derived: list[dict]) -> None:
    for d in derived:
        expr = d["formula"]
        try:
            values[d["id"]] = values.eval(expr)
            parts = [p.strip() for p in expr.replace("-", "+").split("+") if p.strip() in values.columns]
            ages[d["id"]] = ages[parts].max(axis=1) if parts else 0.0
        except Exception as exc:  # a missing input leaves the derived series out
            print(f"derived {d['id']}: skipped ({exc})")


def event_severity(events: pd.DataFrame, source: str) -> pd.Series:
    """Weekly severity totals for one event source."""
    e = events[events["source"] == source].copy()
    if e.empty:
        return pd.Series(dtype=float)
    e["week"] = week_end(e["event_date"])
    if source == "usgs":
        # Magnitude 5 = 1 unit, each extra magnitude point x10; non-US quakes count 30%
        mag = pd.to_numeric(e["magnitude"], errors="coerce").fillna(0)
        sev = np.power(10.0, (mag - 5.0).clip(lower=-1, upper=3))
        sev = sev * np.where(e["area"].fillna("").str.startswith("us_"), 1.0, 0.3)
        return pd.Series(sev.values, index=e["week"].values).groupby(level=0).sum()
    if source == "fema":
        # One unit per declared county for major disasters and emergencies
        kind = e["attributes"].apply(lambda a: (a or {}).get("declarationType") if isinstance(a, dict) else None)
        weight = kind.map({"DR": 1.0, "EM": 0.7, "FM": 0.3}).fillna(0.5)
        return pd.Series(weight.values, index=e["week"].values).groupby(level=0).sum()
    return e.groupby("week").size().astype(float)


def event_impulses(events: pd.DataFrame, specs: list[dict], weeks: pd.DatetimeIndex, half_life: float) -> pd.DataFrame:
    decay = 0.5 ** (1.0 / half_life)
    out = {}
    for spec in specs:
        sev = event_severity(events, spec["source"]).reindex(weeks).fillna(0.0)
        imp = np.zeros(len(weeks))
        acc = 0.0
        for i, v in enumerate(sev.values):
            acc = acc * decay + v
            imp[i] = acc
        out[spec["id"]] = imp
    return pd.DataFrame(out, index=weeks)


# ----------------------------------------------------------------------------- step 3: transforms
DEFAULT_SMOOTH = {"daily": 4, "weekly": 1, "monthly": 1}


def smooth(x: pd.Series, weeks: int) -> pd.Series:
    """Trailing mean over `weeks` weeks (1 = no smoothing). Keeps the series point-in-time."""
    return x if weeks <= 1 else x.rolling(weeks, min_periods=max(1, weeks // 2)).mean()


def transform(x: pd.Series, kind: str) -> pd.Series:
    if kind == "level":
        return x
    if kind == "yoy":
        return x / x.shift(52) - 1
    if kind == "q_ann":
        r = x / x.shift(13)
        return np.sign(r) * np.abs(r) ** 4 - 1
    if kind == "dev12":
        return x - x.rolling(52, min_periods=26).mean().shift(1)
    if kind == "dev12_pct":
        return x / x.rolling(52, min_periods=26).mean().shift(1) - 1
    if kind == "chg13":
        return x - x.shift(13)
    if kind == "dev260":
        return x - x.rolling(260, min_periods=52).mean().shift(1)
    if kind == "log_att":
        base = x.rolling(52, min_periods=26).median().shift(1)
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.log(x.where(x > 0) / base.where(base > 0))
    raise ValueError(f"unknown transform {kind}")


# ----------------------------------------------------------------------------- step 4: standardization
def standardize(x: pd.Series, min_history: int, cap: float) -> pd.Series:
    """Robust z-score against the series' own PAST (expanding window, shifted one week)."""
    past = x.shift(1)
    med = past.expanding(min_periods=min_history).median()
    q1 = past.expanding(min_periods=min_history).quantile(0.25)
    q3 = past.expanding(min_periods=min_history).quantile(0.75)
    scale = (q3 - q1) / 1.349
    scale = scale.where(scale > 1e-12)
    z = (x - med) / scale
    return z.clip(lower=-cap, upper=cap)


def staleness_weight(age: pd.Series, freq_class: str, rules: dict) -> pd.Series:
    r = rules[freq_class]
    full, zero = r["full"], r["zero"]
    w = 1 - (age - full) / (zero - full)
    return w.clip(lower=0, upper=1).fillna(0)


def weighted_mean(cols: dict[str, pd.Series], weights: dict[str, pd.Series | float]) -> pd.Series:
    """Weighted mean across columns, ignoring missing values, renormalizing weights each week."""
    num, den = None, None
    for key, s in cols.items():
        w = weights[key]
        w = w if isinstance(w, pd.Series) else pd.Series(w, index=s.index)
        w = w.where(s.notna(), 0.0)
        term = (s.fillna(0.0) * w)
        num = term if num is None else num + term
        den = w if den is None else den + w
    if num is None:
        return pd.Series(dtype=float)
    return (num / den.where(den > 0))


# ----------------------------------------------------------------------------- step 5: full pipeline
def compute_index(obs: pd.DataFrame, events: pd.DataFrame, catalog: pd.DataFrame,
                  signals_cfg: dict, weights_cfg: dict,
                  start: str = "2000-01-01", end: str | None = None) -> dict[str, pd.DataFrame]:
    end = end or dt.date.today().isoformat()
    weeks = pd.date_range(pd.Timestamp(start), pd.Timestamp(end), freq=WEEK_ANCHOR)
    min_hist = int(weights_cfg["min_history_weeks"])
    min_hist_agg = int(weights_cfg.get("min_history_weeks_aggregate", 52))
    cap = float(weights_cfg["z_cap"])

    # --- weekly point-in-time values
    values, ages = weekly_series(obs, catalog, weeks)
    add_derived(values, ages, signals_cfg.get("derived", []))
    imp = event_impulses(events, signals_cfg.get("events", []), weeks, float(weights_cfg["event_half_life_weeks"]))
    for c in imp.columns:
        values[c] = imp[c]
        ages[c] = 0.0

    # --- series metadata (catalog + derived + events)
    meta = {r["series_id"]: {"dimension": r["dimension"], "lens": r["lens"], "frequency": r["frequency"], "name": r["name"]}
            for _, r in catalog.iterrows()}
    for d in signals_cfg.get("derived", []):
        meta[d["id"]] = {"dimension": d["dimension"], "lens": d["lens"], "frequency": d["frequency"], "name": d["name"]}
    for e in signals_cfg.get("events", []):
        meta[e["id"]] = {"dimension": e["dimension"], "lens": e["lens"], "frequency": "weekly", "name": e["name"]}

    # --- signals
    sig_rows = []
    sig_z: dict[str, pd.Series] = {}
    sig_w: dict[str, pd.Series] = {}
    sig_meta: dict[str, dict] = {}
    for spec in signals_cfg["signals"]:
        sid = spec["series"]
        if sid not in values.columns or sid not in meta:
            print(f"signal skipped, no data: {sid} {spec['transform']}")
            continue
        fclass = FREQ_CLASS.get(meta[sid]["frequency"], "monthly")
        sm = int(spec.get("smooth", DEFAULT_SMOOTH[fclass]))
        raw = transform(smooth(values[sid].astype(float), sm), spec["transform"])
        z = standardize(raw, min_hist, cap)
        if spec.get("invert"):
            z = -z
        w = staleness_weight(ages[sid], fclass, weights_cfg["staleness"]) * float(spec.get("weight", 1.0))
        key = f"{sid}|{spec['transform']}"
        sig_z[key], sig_w[key] = z, w
        sig_meta[key] = {"series": sid, "transform": spec["transform"], "dimension": meta[sid]["dimension"],
                         "lens": meta[sid]["lens"], "name": meta[sid]["name"], "invert": bool(spec.get("invert"))}
        sig_rows.append(pd.DataFrame({"week": weeks, "signal": key, "series": sid, "transform": spec["transform"],
                                      "dimension": meta[sid]["dimension"], "lens": meta[sid]["lens"],
                                      "raw": raw.values, "z": z.values, "weight": w.values}))
    signals = pd.concat(sig_rows, ignore_index=True)

    # --- lenses
    lens_z: dict[tuple[str, str], pd.Series] = {}
    lens_rows = []
    for (dim, lens), group in pd.DataFrame(sig_meta).T.groupby(["dimension", "lens"]):
        keys = list(group.index)
        combined = weighted_mean({k: sig_z[k] for k in keys}, {k: sig_w[k] for k in keys})
        n_avail = sum(sig_z[k].notna().astype(int) for k in keys)
        z = standardize(combined, min_hist_agg, cap)
        lens_z[(dim, lens)] = z
        lens_rows.append(pd.DataFrame({"week": weeks, "dimension": dim, "lens": lens, "combined": combined.values,
                                       "z": z.values, "signals_available": n_avail.values}))
    lenses = pd.concat(lens_rows, ignore_index=True)

    # --- dimensions
    dim_z: dict[str, pd.Series] = {}
    dim_rows = []
    for dim, lw in weights_cfg["lenses"].items():
        cols = {lens: lens_z[(dim, lens)] for lens in lw if (dim, lens) in lens_z}
        if not cols:
            continue
        combined = weighted_mean(cols, {lens: float(lw[lens]) for lens in cols})
        z = standardize(combined, min_hist_agg, cap)
        dim_z[dim] = z
        dim_rows.append(pd.DataFrame({"week": weeks, "dimension": dim, "combined": combined.values, "z": z.values,
                                      "lenses_available": sum(c.notna().astype(int) for c in cols.values()).values}))
    dimensions = pd.concat(dim_rows, ignore_index=True)

    # --- headline
    dw = weights_cfg["dimensions"]
    combined = weighted_mean(dim_z, {d: float(dw[d]) for d in dim_z})
    head_z = standardize(combined, min_hist_agg, cap)

    # --- percentiles against the reference period
    ref = weights_cfg["reference_period"]
    in_ref = (weeks >= pd.Timestamp(ref["start"])) & (weeks <= pd.Timestamp(ref["end"]))

    def to_percentile(z: pd.Series) -> pd.Series:
        ref_vals = np.sort(z[in_ref].dropna().values)
        if len(ref_vals) == 0:
            return pd.Series(np.nan, index=z.index)
        pct = np.searchsorted(ref_vals, z.values, side="right") / len(ref_vals) * 100
        return pd.Series(np.where(z.notna(), pct, np.nan), index=z.index)

    bands = weights_cfg["bands"]

    def band_of(p):
        if p is None or (isinstance(p, float) and math.isnan(p)):
            return None
        for b in bands:
            if p <= b["upto"]:
                return b["name"]
        return bands[-1]["name"]

    head_pct = to_percentile(head_z)
    headline = pd.DataFrame({"week": weeks, "combined": combined.values, "z": head_z.values, "score": head_pct.round(1).values,
                             "dimensions_available": sum(c.notna().astype(int) for c in dim_z.values()).values})
    headline["band"] = [band_of(p) for p in headline["score"]]
    headline["change_1w"] = headline["score"].diff().round(1)
    headline["change_4w"] = headline["score"].diff(4).round(1)
    dimensions["score"] = np.nan
    for dim in dim_z:
        m = dimensions["dimension"] == dim
        dimensions.loc[m, "score"] = to_percentile(dim_z[dim]).round(1).values
    dimensions["band"] = [band_of(p) for p in dimensions["score"]]

    # --- exact contributions to the headline's combined score (before re-standardization)
    contrib_rows = []
    wsum = sum((pd.Series(float(dw[d]), index=weeks)).where(dim_z[d].notna(), 0.0) for d in dim_z)
    for dim, z in dim_z.items():
        share = (float(dw[dim]) / wsum.where(wsum > 0)).where(z.notna(), 0.0)
        contrib_rows.append(pd.DataFrame({"week": weeks, "dimension": dim, "contribution": (z.fillna(0) * share).values}))
    contributions = pd.concat(contrib_rows, ignore_index=True)

    return {"weekly_values": values, "signals": signals, "lenses": lenses, "dimensions": dimensions,
            "headline": headline, "contributions": contributions}
