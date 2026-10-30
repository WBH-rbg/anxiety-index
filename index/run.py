"""Compute the Anxiety Index from BigQuery data and write results back.

    python -m index.run                  # full history, writes ai_index.* tables and output/ files
    python -m index.run --no-write       # compute and write output/ files only

Tables written (replaced each run): ai_index.headline_weekly, ai_index.dimension_weekly,
ai_index.lens_weekly, ai_index.signal_weekly, ai_index.contribution_weekly.
Files written to output/: headline_weekly.csv, dimension_weekly.csv, headline.png, dimensions.png.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from index import compute

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "anxiety-index")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"


def load_inputs(client):
    obs = client.query("""
        SELECT series_id, obs_date, value FROM `ai_clean.observations_latest`
        WHERE value IS NOT NULL""").to_dataframe()
    obs["obs_date"] = pd.to_datetime(obs["obs_date"])
    events = client.query("""
        SELECT source, event_date, event_type, area, magnitude, title, attributes
        FROM `ai_clean.events_latest` WHERE event_date IS NOT NULL""").to_dataframe()
    events["event_date"] = pd.to_datetime(events["event_date"])
    events["attributes"] = events["attributes"].apply(lambda a: json.loads(a) if isinstance(a, str) else a)
    catalog = client.query("SELECT series_id, source, name, dimension, lens, frequency FROM `ai_raw.series_catalog`").to_dataframe()
    return obs, events, catalog


def write_table(client, name: str, frame: pd.DataFrame) -> None:
    from google.cloud import bigquery
    job = client.load_table_from_dataframe(
        frame, f"{PROJECT_ID}.ai_index.{name}",
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE"))
    job.result()


def charts(headline: pd.DataFrame, dimensions: pd.DataFrame, version: str = "") -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    h = headline.dropna(subset=["score"])
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(h["week"], h["score"], color="#1F2A44", linewidth=1)
    for y, c in [(20, "#DCEFD9"), (50, "#F3EEDC"), (80, "#F5D4B3"), (95, "#F6DEDB"), (100, "#E9B8B5")]:
        ax.axhspan(0 if y == 20 else {50: 20, 80: 50, 95: 80, 100: 95}[y], y, color=c, alpha=0.5, lw=0)
    for label, when in [("Lehman", "2008-09-15"), ("COVID", "2020-03-14"), ("Floyd protests", "2020-05-30"),
                        ("Jan 6", "2021-01-06"), ("Ukraine", "2022-02-24"), ("Inflation peak", "2022-06-15")]:
        ax.axvline(pd.Timestamp(when), color="#888", lw=0.6, ls="--")
        ax.text(pd.Timestamp(when), 101, label, rotation=90, va="bottom", ha="center", fontsize=7, color="#555")
    ax.set_ylim(0, 100); ax.set_ylabel("Anxiety Index (percentile, 2005–2025)")
    ax.set_title(f"Anxiety Index, weekly, methodology v{version} (prototype)" if version else "Anxiety Index, weekly", loc="left")
    fig.tight_layout(); fig.savefig(OUT / "headline.png", dpi=130); plt.close(fig)

    dims = dimensions.dropna(subset=["score"])
    names = list(dims["dimension"].unique())
    fig, axes = plt.subplots(len(names), 1, figsize=(14, 2.2 * len(names)), sharex=True)
    for ax, dim in zip(axes, names):
        d = dims[dims["dimension"] == dim]
        ax.plot(d["week"], d["score"], color="#534AB7", linewidth=0.9)
        ax.set_ylim(0, 100); ax.set_ylabel(dim, fontsize=8); ax.axhline(80, color="#C33", lw=0.5, ls=":")
    axes[0].set_title("Dimension scores (percentile, 2005–2025)", loc="left")
    fig.tight_layout(); fig.savefig(OUT / "dimensions.png", dpi=110); plt.close(fig)


DIM_LABELS = {"cost_of_living": "Cost of living", "jobs_financial": "Jobs and financial security",
              "political_institutional": "Political and institutional", "safety_unrest": "Public safety and unrest",
              "disasters_health": "Disasters, climate and health", "geopolitical": "Geopolitical"}


TRANSFORM_LABELS = {
    "log_att": "attention vs. 3-year norm", "dev260": "vs. 5-year average", "dev156": "vs. 3-year average", "dev12": "vs. 12-month average",
    "dev12_pct": "% vs. 12-month average", "chg13": "13-week change", "yoy": "12-month change", "q_ann": "3-month annualized",
    "cum3y": "3-year cumulative change", "dev_term": "vs. president's own average", "level": "level",
}
LENS_LABELS = {"conditions": "Conditions", "sentiment": "Sentiment", "attention": "Attention"}


def measure_name(series_name: str, transform: str) -> str:
    return f"{series_name}, {TRANSFORM_LABELS.get(transform, transform)}"


def z_words(z: float) -> str:
    """Plain words for a standardized reading."""
    if z >= 2.5:
        return "extreme"
    if z >= 1.5:
        return "very high"
    if z >= 0.75:
        return "high"
    if z > -0.75:
        return "normal"
    if z > -1.25:
        return "low"
    return "very low"


def explanation(out: dict, catalog: pd.DataFrame, signals_cfg: dict, nowcast: dict | None = None) -> str:
    """Structured explanation of the latest week: what moved and which signals drove it."""
    names = dict(zip(catalog["series_id"], catalog["name"]))
    for d in signals_cfg.get("derived", []) + signals_cfg.get("events", []) + signals_cfg.get("poll_series", []):
        names[d["id"]] = d["name"]
    h = out["headline"].dropna(subset=["score"])
    if h.empty:
        return "No scored weeks yet."
    last = h.iloc[-1]
    week = last["week"]
    conc = last.get("news_concentration")
    conc_txt = ""
    if conc is not None and pd.notna(conc):
        level = "one story dominates" if conc >= 80 else ("attention is spread out" if conc <= 20 else "attention is moderately concentrated")
        conc_txt = f" News concentration: {conc:.0f}th percentile ({level})."
    lines = [f"# Anxiety Index: week ending {week.date()}", "",
             f"**{last['score']:.0f} ({last['band']})**, {last['change_1w']:+.1f} vs last week, {last['change_4w']:+.1f} vs four weeks ago.{conc_txt}", ""]
    if nowcast:
        hot = sorted(((v, k) for k, v in nowcast["dimensions"].items() if v is not None), reverse=True)[:2]
        hot_txt = ", ".join(f"{DIM_LABELS.get(k, k).lower()} {v:.0f}" for v, k in hot)
        dims_last = out["dimensions"][out["dimensions"]["week"] == week].set_index("dimension")["score"]
        moves = sorted(((v - dims_last.get(k, np.nan), k) for k, v in nowcast["dimensions"].items() if v is not None and pd.notna(dims_last.get(k, np.nan))),
                       key=lambda t: -abs(t[0]))[:2]
        move_txt = "; ".join(f"{DIM_LABELS.get(k, k).lower()} {d:+.0f}" for d, k in moves if abs(d) >= 3)
        lines += [f"**So far this week** (ending {nowcast['week']}, data through {nowcast['as_of']}): **{nowcast['score']:.0f} ({nowcast['band']})**, "
                  f"{nowcast['change_vs_last_week']:+.1f} vs the completed week. Hottest: {hot_txt}." + (f" Moving: {move_txt}." if move_txt else "") +
                  " Provisional: daily inputs use the trailing seven days, and the reading will move as the week's data arrive.", ""]
    dims = out["dimensions"]
    contrib = out["contributions"]
    dc = contrib.pivot(index="week", columns="dimension", values="contribution")
    dchange = (dc.loc[week] - dc.shift(1).loc[week]).sort_values(key=abs, ascending=False)
    shares = contrib.pivot(index="week", columns="dimension", values="share").loc[week] if "share" in contrib.columns else None
    lines.append("## Dimensions")
    lines.append("")
    lines.append("| Dimension | Reading | Band | Change on the week | Share of this week's anxiety |")
    lines.append("|---|---|---|---|---|")
    order = shares.sort_values(ascending=False).index if shares is not None else dchange.index
    dim_changes = {}
    for dim in order:
        d = dims[(dims["dimension"] == dim)].set_index("week")
        if week not in d.index or pd.isna(d.loc[week, "score"]):
            continue
        prev = d["score"].shift(1).loc[week]
        chg = d.loc[week, "score"] - prev if pd.notna(prev) else float("nan")
        dim_changes[dim] = chg
        share_txt = f"{100 * shares[dim]:.0f}%" if shares is not None and dim in shares.index else ""
        lines.append(f"| {DIM_LABELS.get(dim, dim)} | {d.loc[week, 'score']:.0f} | {d.loc[week, 'band']} | {chg:+.0f} | {share_txt} |")
    # one sentence on what moved the headline
    movers = sorted(((v, k) for k, v in dim_changes.items() if pd.notna(v) and abs(v) >= 3), key=lambda t: -abs(t[0]))
    if movers:
        up = [f"{DIM_LABELS.get(k, k).lower()} (+{v:.0f})" for v, k in movers if v > 0]
        down = [f"{DIM_LABELS.get(k, k).lower()} ({v:.0f})" for v, k in movers if v < 0]
        parts = []
        if up:
            parts.append("up on " + ", ".join(up))
        if down:
            parts.append("down on " + ", ".join(down))
        lines += ["", f"On the week, dimensions moved {'; '.join(parts)}. The headline weights the hottest dimension most, so moves in the leading dimensions matter more than moves at the bottom of the table."]
    else:
        lines += ["", "No dimension moved more than a few points on the week."]
    sig = out["signals"]
    sig = sig[sig["week"].isin([week, week - pd.Timedelta(days=7)])].copy()
    piv = sig.pivot_table(index="signal", columns="week", values="z")
    if piv.shape[1] == 2:
        dz = (piv.iloc[:, 1] - piv.iloc[:, 0])
        wts = sig[sig["week"] == week].set_index("signal")["weight"]
        meta = sig[sig["week"] == week].set_index("signal")[["series", "transform", "dimension", "lens", "z"]]
        impact = (dz * wts).dropna().sort_values(key=abs, ascending=False)
        lines += ["", "## What changed since last week", "",
                  "The signals whose moves, times their weights, did most to change the reading. Readings are in standard units against each signal's own history; words translate them.", "",
                  "| Measure | Dimension | Lens | Now | Change | Weight |", "|---|---|---|---|---|---|"]
        for key in impact.index[:12]:
            m = meta.loc[key]
            lines.append(f"| {measure_name(names.get(m['series'], m['series']), m['transform'])} | {DIM_LABELS.get(m['dimension'], m['dimension'])} | {LENS_LABELS.get(m['lens'], m['lens'])} | "
                         f"{z_words(m['z'])} ({m['z']:+.1f}) | {dz[key]:+.1f} | {wts[key]:.1f} |")
        lines += ["", "## Most elevated right now", "", "| Measure | Dimension | Lens | Reading |", "|---|---|---|---|"]
        top = meta[meta["z"].notna()].sort_values("z", ascending=False).head(12)
        for key, m in top.iterrows():
            lines.append(f"| {measure_name(names.get(m['series'], m['series']), m['transform'])} | {DIM_LABELS.get(m['dimension'], m['dimension'])} | {LENS_LABELS.get(m['lens'], m['lens'])} | {z_words(m['z'])} ({m['z']:+.1f}) |")
    return "\n".join(lines) + "\n"


def split_nowcast(out: dict, today: pd.Timestamp, computed_at: dt.datetime) -> dict:
    """Pull the in-progress week out of every frame and summarize it. Mutates `out` in place."""
    head = out["headline"]
    prov = head["week"] > today
    if not prov.any():
        return {"summary": None, "rows": None}
    week = head.loc[prov, "week"].iloc[0]
    last_complete = head.loc[~prov].dropna(subset=["score"]).tail(1)
    row = head.loc[prov].iloc[0]
    dims = out["dimensions"]
    dprov = dims["week"] == week
    dim_scores = {r["dimension"]: (None if pd.isna(r["score"]) else float(r["score"])) for _, r in dims.loc[dprov].iterrows()}
    contrib = out["contributions"]
    shares = {r["dimension"]: round(float(r["share"]), 3) for _, r in contrib.loc[contrib["week"] == week].iterrows()}
    summary = None
    if pd.notna(row["score"]):
        prev = float(last_complete["score"].iloc[0]) if not last_complete.empty else None
        summary = {"week": str(week.date()), "as_of": str(today.date()), "score": float(row["score"]), "band": row["band"],
                   "change_vs_last_week": None if prev is None else round(float(row["score"]) - prev, 1),
                   "dimensions": dim_scores, "shares": shares, "provisional": True}
    rows = pd.DataFrame([{"week": week, "as_of": today, "computed_at": computed_at, "level": "headline", "score": row["score"], "band": row["band"], "share": None}] +
                        [{"week": week, "as_of": today, "computed_at": computed_at, "level": d, "score": sc,
                          "band": dims.loc[dprov & (dims["dimension"] == d), "band"].iloc[0] if (dprov & (dims["dimension"] == d)).any() else None,
                          "share": shares.get(d)} for d, sc in dim_scores.items()])
    # a diagnostic file: every signal and lens in the provisional week against the completed week
    try:
        last_week = last_complete["week"].iloc[0] if not last_complete.empty else None
        if last_week is not None:
            sig = out["signals"]
            a = sig[sig["week"] == last_week].set_index("signal")[["dimension", "lens", "raw", "z", "weight"]]
            b = sig[sig["week"] == week].set_index("signal")[["raw", "z", "weight"]]
            diag = a.join(b, rsuffix="_now", how="outer")
            diag["z_change"] = (diag["z_now"] - diag["z"]).round(3)
            diag["weight_change"] = (diag["weight_now"] - diag["weight"]).round(3)
            ln = out["lenses"]
            la = ln[ln["week"] == last_week].set_index(["dimension", "lens"])["z"]
            lb = ln[ln["week"] == week].set_index(["dimension", "lens"])["z"]
            lens_diag = pd.DataFrame({"z_completed": la, "z_now": lb})
            lens_diag["change"] = (lens_diag["z_now"] - lens_diag["z_completed"]).round(3)
            OUT.mkdir(exist_ok=True)
            diag.sort_values("z_change", key=lambda c: c.abs(), ascending=False).to_csv(OUT / "nowcast_signals.csv")
            lens_diag.to_csv(OUT / "nowcast_lenses.csv")
    except Exception as exc:  # diagnostics must never break the run
        print(f"nowcast diagnostics skipped: {exc}")
    # drop the provisional week from the official frames
    for key in ("headline", "dimensions", "lenses", "signals", "contributions", "weekly_values"):
        f = out.get(key)
        if isinstance(f, pd.DataFrame):
            if "week" in f.columns:
                out[key] = f[f["week"] <= today].reset_index(drop=True)
            elif isinstance(f.index, pd.DatetimeIndex):
                out[key] = f[f.index <= today]
    return {"summary": summary, "rows": rows}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true", help="don't write BigQuery tables")
    parser.add_argument("--end", default=None, help="last week to compute (YYYY-MM-DD)")
    parser.add_argument("--no-nowcast", action="store_true", help="don't compute the provisional reading for the week in progress")
    args = parser.parse_args(argv)

    from google.cloud import bigquery
    client = bigquery.Client(project=PROJECT_ID)
    obs, events, catalog = load_inputs(client)
    weights = yaml.safe_load(open(ROOT / "config" / "weights.yaml"))
    signals = yaml.safe_load(open(ROOT / "config" / "signals.yaml"))
    print(f"inputs: {len(obs):,} observations, {len(events):,} events, {len(catalog)} catalog series")

    # The grid runs through the Saturday that ends the current week, so the last row is the week in
    # progress: a provisional "so far this week" reading built from whatever has been published. It is
    # reported separately and kept out of the official weekly tables until the week completes.
    today = pd.Timestamp(dt.date.today())
    end = args.end
    if end is None and not args.no_nowcast:
        end = (today + pd.Timedelta(days=(5 - today.weekday()) % 7)).date().isoformat()
    out = compute.compute_index(obs, events, catalog, signals, weights, start="2000-01-01", end=end)
    computed_at = dt.datetime.now(dt.timezone.utc)
    nowcast = split_nowcast(out, today, computed_at)
    for frame in out.values():
        if isinstance(frame, pd.DataFrame) and "week" in frame.columns:
            frame["methodology_version"] = str(weights["version"])
            frame["computed_at"] = computed_at

    OUT.mkdir(exist_ok=True)
    out["headline"].to_csv(OUT / "headline_weekly.csv", index=False)
    out["dimensions"].to_csv(OUT / "dimension_weekly.csv", index=False)
    out["contributions"][out["contributions"]["week"] >= out["contributions"]["week"].max() - pd.Timedelta(weeks=8)].to_csv(OUT / "contribution_recent.csv", index=False)
    latest = out["headline"].dropna(subset=["score"]).tail(1).iloc[0]
    (OUT / "latest.json").write_text(json.dumps({
        "week": str(latest["week"].date()), "score": float(latest["score"]), "band": latest["band"],
        "news_concentration": None if pd.isna(latest.get("news_concentration")) else float(latest["news_concentration"]),
        "change_1w": None if pd.isna(latest["change_1w"]) else float(latest["change_1w"]),
        "nowcast": nowcast["summary"],
        "methodology_version": str(weights["version"]), "computed_at": computed_at.isoformat()}, indent=2))
    charts(out["headline"], out["dimensions"], str(weights["version"]))
    (OUT / "explanation.md").write_text(explanation(out, catalog, signals, nowcast["summary"]))
    print(f"latest: week {latest['week'].date()} score {latest['score']} ({latest['band']})")
    if nowcast["summary"]:
        n = nowcast["summary"]
        print(f"nowcast: week ending {n['week']} through {n['as_of']}: {n['score']} ({n['band']}), {n['change_vs_last_week']:+.1f} vs last week")

    if not args.no_write:
        write_table(client, "headline_weekly", out["headline"])
        write_table(client, "dimension_weekly", out["dimensions"])
        write_table(client, "lens_weekly", out["lenses"])
        write_table(client, "signal_weekly", out["signals"])
        write_table(client, "contribution_weekly", out["contributions"])
        if nowcast["rows"] is not None:
            from google.cloud import bigquery as bq
            client.load_table_from_dataframe(nowcast["rows"], f"{PROJECT_ID}.ai_index.nowcast",
                                             job_config=bq.LoadJobConfig(write_disposition="WRITE_APPEND")).result()
        print("BigQuery tables written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
