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
    "bls": 14, "bls_jolts": 35, "eia": 2, "dol": 5, "umich": -7, "nyfed": 10, "gpr": 2,   # Michigan's final reading is out before month end
    "epu": 1, "fedreg": 0, "wikipedia": 1, "gdelt": 1, "gdelt_gkg": 1, "gdelt_events": 1, "treasury": 0, "markets": 0,
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
def weekly_series(obs: pd.DataFrame, catalog: pd.DataFrame, weeks: pd.DatetimeIndex,
                  today: pd.Timestamp | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (values, age_weeks): DataFrames indexed by week, one column per series.

    values[w, s] is the latest value of series s that was public by the end of week w.
    age_weeks[w, s] is how many weeks ago that value became public.
    Daily series are averaged within the week they refer to. If the last week in the grid is still
    in progress (its Saturday is after `today`), daily series take the trailing seven days of data
    instead of the partial week, so a Monday nowcast isn't built from Sunday's news alone.
    """
    values, ages = {}, {}
    meta = catalog.set_index("series_id")
    in_progress = today is not None and len(weeks) > 0 and weeks[-1] > today
    for sid, g in obs.groupby("series_id"):
        if sid not in meta.index:
            continue
        freq = meta.loc[sid, "frequency"]
        source = meta.loc[sid, "source"]
        g = g.sort_values("obs_date")
        if freq == "daily":
            wk = week_end(g["obs_date"])
            per_week = g.groupby(wk)["value"].mean()
            lag = release_lag(sid, source)
            if lag <= 2:  # published within a couple of days: the week's average is known by week end
                s = pd.Series(per_week.values, index=per_week.index)
                if in_progress:
                    recent = g[(g["obs_date"] > today - pd.Timedelta(days=7)) & (g["obs_date"] <= today)]["value"]
                    if len(recent):
                        s[weeks[-1]] = recent.mean()
            else:
                avail_week = week_end(pd.Series(per_week.index + pd.to_timedelta(lag, unit="D")))
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
    if source == "shootings":
        # fatalities, with a floor of 3 so every qualifying incident registers; a 20-death event counts ~7x a 3-death one
        fat = pd.to_numeric(e["magnitude"], errors="coerce").fillna(3).clip(lower=3)
        return pd.Series(fat.values, index=e["week"].values).groupby(level=0).sum()
    if source == "fema":
        # One unit per declared county for major disasters and emergencies
        kind = e["attributes"].apply(lambda a: (a or {}).get("declarationType") if isinstance(a, dict) else None)
        weight = kind.map({"DR": 1.0, "EM": 0.7, "FM": 0.3}).fillna(0.5)
        return pd.Series(weight.values, index=e["week"].values).groupby(level=0).sum()
    return e.groupby("week").size().astype(float)


def event_impulses(events: pd.DataFrame, specs: list[dict], weeks: pd.DatetimeIndex, half_life: float,
                   today: pd.Timestamp | None = None) -> pd.DataFrame:
    """Weekly event severity with exponential decay. If the last week is still in progress, its decay
    step covers only the days elapsed so far, so a Monday nowcast doesn't fade last week's events by a
    full week before the new week's events have had time to happen."""
    decay = 0.5 ** (1.0 / half_life)
    last_decay = decay
    if today is not None and len(weeks) and weeks[-1] > today:
        elapsed_days = max(0.0, 7.0 - (weeks[-1] - today).days)
        last_decay = 0.5 ** ((elapsed_days / 7.0) / half_life)
    out = {}
    for spec in specs:
        sev = event_severity(events, spec["source"]).reindex(weeks).fillna(0.0)
        imp = np.zeros(len(weeks))
        acc = 0.0
        n = len(sev)
        for i, v in enumerate(sev.values):
            acc = acc * (last_decay if i == n - 1 else decay) + v
            imp[i] = acc
        out[spec["id"]] = imp
    return pd.DataFrame(out, index=weeks)


def approval_average(events: pd.DataFrame, weeks: pd.DatetimeIndex, window_days: int = 14) -> pd.DataFrame:
    """Weekly presidential approval average from individual polls.

    For each week, polls whose fieldwork ended within the trailing window, one per
    pollster (the latest), averaged. Falls back to 28- and then 42-day windows when fewer
    than three polls are available; with fewer than three even then, the week is left
    empty and the staleness rule carries the last good average. Returns columns
    approval_net, disapprove_avg, poll_count.
    """
    if "event_type" not in events.columns:
        return pd.DataFrame(index=weeks)
    polls = events[events["event_type"] == "approval_poll"].copy()
    if polls.empty:
        return pd.DataFrame(index=weeks)
    attrs = polls["attributes"].apply(lambda a: a if isinstance(a, dict) else {})
    polls["approve"] = attrs.apply(lambda a: a.get("approve")).astype(float)
    polls["disapprove"] = attrs.apply(lambda a: a.get("disapprove")).astype(float)
    polls["pollster"] = polls["title"].fillna("unknown")
    polls = polls.dropna(subset=["approve", "disapprove", "event_date"]).sort_values("event_date")
    net, dis, cnt = [], [], []
    for w in weeks:
        chosen = pd.DataFrame()
        for days in (window_days, 28, 42):
            recent = polls[(polls["event_date"] > w - pd.Timedelta(days=days)) & (polls["event_date"] <= w)]
            chosen = recent.groupby("pollster").tail(1)
            if len(chosen) >= 3:
                break
        if len(chosen) < 3:
            net.append(np.nan); dis.append(np.nan); cnt.append(0)
        else:
            net.append((chosen["approve"] - chosen["disapprove"]).mean())
            dis.append(chosen["disapprove"].mean()); cnt.append(len(chosen))
    return pd.DataFrame({"approval_net": net, "disapprove_avg": dis, "poll_count": cnt}, index=weeks)


# Presidential terms, for the "own baseline" transform (a new president resets the baseline)
TERM_STARTS = [pd.Timestamp(d) for d in ("1993-01-20", "2001-01-20", "2009-01-20", "2017-01-20", "2021-01-20", "2025-01-20")]


# ----------------------------------------------------------------------------- step 3: transforms
DEFAULT_SMOOTH = {"daily": 3, "weekly": 1, "monthly": 1}


def smooth(x: pd.Series, half_life_weeks: float) -> pd.Series:
    """Fast-attack, slow-release smoothing of an anxiety-oriented signal (up = more anxiety).

    A rise enters in full immediately; a fall fades with the given half-life.
    Fear arrives at once and subsides gradually. Point-in-time: uses only past
    and current values. half_life_weeks <= 1 means no smoothing.
    """
    if half_life_weeks <= 1:
        return x
    decay = 0.5 ** (1.0 / half_life_weeks)
    out = np.full(len(x), np.nan)
    prev = np.nan
    for i, v in enumerate(x.values):
        if np.isnan(v):
            out[i] = prev if not np.isnan(prev) else np.nan
            continue
        if np.isnan(prev):
            prev = v
        else:
            released = prev * decay + v * (1 - decay)
            prev = v if v >= released else released
        out[i] = prev
    return pd.Series(out, index=x.index)


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
    if kind == "dev156":
        return x - x.rolling(156, min_periods=26).mean().shift(1)
    if kind == "cum3y":
        return x / x.shift(156) - 1
    if kind == "log_att":
        # attention vs. a three-year norm, so a year-long crisis doesn't become "normal" within a year
        base = x.rolling(156, min_periods=26).median().shift(1)
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.log(x.where(x > 0) / base.where(base > 0))
    if kind == "dev_term":
        # deviation from the mean since the current presidential term began (at least 8 weeks in)
        term = pd.Series(np.searchsorted(np.array(TERM_STARTS, dtype="datetime64[ns]"), x.index.values, side="right"), index=x.index)
        base = x.groupby(term).transform(lambda g: g.expanding(min_periods=8).mean().shift(1))
        return x - base
    raise ValueError(f"unknown transform {kind}")


# ----------------------------------------------------------------------------- step 4: standardization
WARMUP_WEEKS = 520  # a series' first ten years serve as its base period


def standardize(x: pd.Series, min_history: int, cap: float, warmup: int = WARMUP_WEEKS, cap_low: float | None = None) -> pd.Series:
    """Robust z-score (median, interquartile range) against the series' own history.

    Point-in-time once a series has `warmup` weeks of history: each week is
    compared only with its past. Before that, the series' first `warmup` weeks
    serve as a fixed base period (so early years aren't judged against two or
    three calm years alone). `min_history` valid weeks are needed before any
    score is produced.
    """
    valid = x.dropna()
    if len(valid) < min_history:
        return pd.Series(np.nan, index=x.index)
    base = valid.iloc[:warmup]
    med0, q1, q3 = base.median(), base.quantile(0.25), base.quantile(0.75)
    scale0 = (q3 - q1) / 1.349
    past = x.shift(1)
    n_past = past.notna().cumsum()
    med = past.expanding(min_periods=warmup).median()
    iqr = past.expanding(min_periods=warmup).quantile(0.75) - past.expanding(min_periods=warmup).quantile(0.25)
    scale = iqr / 1.349
    use_base = n_past < warmup
    med = med.where(~use_base, med0)
    scale = scale.where(~use_base, scale0)
    scale = scale.where(scale > 1e-12)
    z = (x - med) / scale
    return z.clip(lower=-(cap if cap_low is None else cap_low), upper=cap)


def staleness_weight(age: pd.Series, freq_class: str, rules: dict) -> pd.Series:
    r = rules[freq_class]
    full, zero = r["full"], r["zero"]
    w = 1 - (age - full) / (zero - full)
    return w.clip(lower=0, upper=1).fillna(0)


def soft_max(cols: dict[str, pd.Series], weights: dict[str, float], temperature: float = 1.0):
    """Weighted soft maximum: log(sum_d w_d exp(z_d / T)) * T, with weights renormalized over
    available dimensions. Equal inputs give that value back; the hottest dimensions dominate.
    Returns (combined, shares) where shares[d] = w_d exp(z_d/T) / sum, the dimension's share of
    the week's anxiety. Anxiety is driven by the worst thing happening, not the average thing."""
    keys = list(cols)
    frame = pd.DataFrame({k: cols[k] for k in keys})
    w = pd.DataFrame({k: float(weights[k]) for k in keys}, index=frame.index).where(frame.notna(), 0.0)
    w = w.div(w.sum(axis=1).where(w.sum(axis=1) > 0), axis=0)
    ex = np.exp(frame.fillna(0.0) / temperature) * w
    total = ex.sum(axis=1)
    combined = (np.log(total.where(total > 0)) * temperature).where(frame.notna().any(axis=1))
    shares = {k: (ex[k] / total.where(total > 0)).fillna(0.0) for k in keys}
    return combined, shares


def rank_decay(cols: dict[str, pd.Series], weights: dict[str, float], decay: float = 0.5):
    """Attention-budget aggregation: the hottest dimension counts in full, the next at `decay`,
    the next at decay^2, and so on, each also scaled by its prior weight; weights are renormalized
    each week. Two pieces of bad news add, but the second adds less than the first.
    Returns (combined, shares) where shares[d] is the dimension's share of the week's attention budget."""
    keys = list(cols)
    frame = pd.DataFrame({k: cols[k] for k in keys})
    ranks = frame.rank(axis=1, ascending=False, method="first")  # 1 = hottest
    eff = pd.DataFrame({k: float(weights[k]) for k in keys}, index=frame.index) * (decay ** (ranks - 1))
    eff = eff.where(frame.notna(), 0.0)
    total = eff.sum(axis=1)
    norm = eff.div(total.where(total > 0), axis=0)
    combined = (frame.fillna(0.0) * norm).sum(axis=1).where(frame.notna().any(axis=1))
    shares = {k: norm[k].fillna(0.0) for k in keys}
    return combined, shares


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
    cap_low = float(weights_cfg.get("z_cap_relief", cap))

    # --- weekly point-in-time values
    values, ages = weekly_series(obs, catalog, weeks, today=pd.Timestamp(dt.date.today()))
    add_derived(values, ages, signals_cfg.get("derived", []))
    imp = event_impulses(events, signals_cfg.get("events", []), weeks, float(weights_cfg["event_half_life_weeks"]),
                         today=pd.Timestamp(dt.date.today()))
    for c in imp.columns:
        values[c] = imp[c]
        ages[c] = 0.0
    appr = approval_average(events, weeks)
    for c in ("approval_net", "disapprove_avg"):
        if c in appr.columns:
            values[c] = appr[c]
            ages[c] = 0.0

    # --- series metadata (catalog + derived + events)
    meta = {r["series_id"]: {"dimension": r["dimension"], "lens": r["lens"], "frequency": r["frequency"], "name": r["name"]}
            for _, r in catalog.iterrows()}
    for d in signals_cfg.get("derived", []):
        meta[d["id"]] = {"dimension": d["dimension"], "lens": d["lens"], "frequency": d["frequency"], "name": d["name"]}
    for e in signals_cfg.get("events", []):
        meta[e["id"]] = {"dimension": e["dimension"], "lens": e["lens"], "frequency": "weekly", "name": e["name"]}
    for pseries in signals_cfg.get("poll_series", []):
        meta[pseries["id"]] = {"dimension": pseries["dimension"], "lens": pseries["lens"], "frequency": "weekly", "name": pseries["name"]}

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
        sm = float(spec.get("smooth", DEFAULT_SMOOTH[fclass]))
        raw = transform(values[sid].astype(float), spec["transform"])
        if spec.get("invert"):
            raw = -raw
        raw = smooth(raw, sm)  # after orientation, so "up" always means more anxiety
        z = standardize(raw, min_hist, cap, cap_low=cap_low)
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
        z = standardize(combined, min_hist_agg, cap, cap_low=cap_low)
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
        z = standardize(combined, min_hist_agg, cap, cap_low=cap_low)
        dim_z[dim] = z
        dim_rows.append(pd.DataFrame({"week": weeks, "dimension": dim, "combined": combined.values, "z": z.values,
                                      "lenses_available": sum(c.notna().astype(int) for c in cols.values()).values}))
    dimensions = pd.concat(dim_rows, ignore_index=True)

    # --- headline
    dw = weights_cfg["dimensions"]
    aggregation = weights_cfg.get("headline_aggregation", "rank_decay")
    if aggregation == "rank_decay":
        combined, shares = rank_decay(dim_z, {d: float(dw[d]) for d in dim_z}, float(weights_cfg.get("rank_decay", 0.5)))
    elif aggregation == "softmax":
        combined, shares = soft_max(dim_z, {d: float(dw[d]) for d in dim_z}, float(weights_cfg.get("softmax_temperature", 1.0)))
    else:
        combined = weighted_mean(dim_z, {d: float(dw[d]) for d in dim_z})
        shares = None
    # The headline is the combined score itself, ranked against the reference period below.
    # Re-standardizing here would let the drifting "normal" level penalize later weeks.
    head_z = combined.clip(lower=-cap_low, upper=cap)

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
    # News concentration: how much one story dominates coverage across the dimensions this week
    # (Herfindahl index of the six dimension article counts, smoothed over the week's data as collected).
    count_cols = [c for c in values.columns if c.startswith("gkg_count_") or c == "gkg_share_geopolitical"]
    if count_cols:
        cnt = values[count_cols].copy()
        if "gkg_share_geopolitical" in cnt.columns and "gkg_base_us" in values.columns:
            cnt["gkg_share_geopolitical"] = values["gkg_share_geopolitical"] * values["gkg_base_us"] / 100
        shares_c = cnt.div(cnt.sum(axis=1).where(cnt.sum(axis=1) > 0), axis=0)
        hhi = (shares_c ** 2).sum(axis=1).where(cnt.notna().all(axis=1))
        concentration = to_percentile(hhi)
    else:
        concentration = pd.Series(np.nan, index=weeks)
    headline = pd.DataFrame({"week": weeks, "combined": combined.values, "z": head_z.values, "score": head_pct.round(1).values,
                             "news_concentration": concentration.round(1).values,
                             "dimensions_available": sum(c.notna().astype(int) for c in dim_z.values()).values})
    # Before the publication start, too few signals have the history standardization needs (most series
    # begin in 2000, so 2000 itself is a warm-up year): the headline is withheld, dimensions are kept.
    publish_from = pd.Timestamp(weights_cfg.get("publish_from", "2001-01-01"))
    headline.loc[headline["week"] < publish_from, ["score", "z", "combined"]] = np.nan
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
    if shares is not None:
        for dim, z in dim_z.items():
            contrib_rows.append(pd.DataFrame({"week": weeks, "dimension": dim, "share": shares[dim].values,
                                              "contribution": (shares[dim] * combined).values}))
    else:
        wsum = sum((pd.Series(float(dw[d]), index=weeks)).where(dim_z[d].notna(), 0.0) for d in dim_z)
        for dim, z in dim_z.items():
            share = (float(dw[dim]) / wsum.where(wsum > 0)).where(z.notna(), 0.0)
            contrib_rows.append(pd.DataFrame({"week": weeks, "dimension": dim, "share": share.values, "contribution": (z.fillna(0) * share).values}))
    contributions = pd.concat(contrib_rows, ignore_index=True)

    return {"weekly_values": values, "signals": signals, "lenses": lenses, "dimensions": dimensions,
            "headline": headline, "contributions": contributions}
