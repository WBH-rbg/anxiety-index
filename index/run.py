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


def charts(headline: pd.DataFrame, dimensions: pd.DataFrame) -> None:
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
    ax.set_title("Anxiety Index, weekly, methodology v0.1 prototype", loc="left")
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


def explanation(out: dict, catalog: pd.DataFrame, signals_cfg: dict) -> str:
    """Structured explanation of the latest week: what moved and which signals drove it."""
    names = dict(zip(catalog["series_id"], catalog["name"]))
    for d in signals_cfg.get("derived", []) + signals_cfg.get("events", []) + signals_cfg.get("poll_series", []):
        names[d["id"]] = d["name"]
    h = out["headline"].dropna(subset=["score"])
    if h.empty:
        return "No scored weeks yet."
    last = h.iloc[-1]
    week = last["week"]
    lines = [f"# Anxiety Index: week ending {week.date()}", "",
             f"**{last['score']:.0f} ({last['band']})**, {last['change_1w']:+.1f} vs last week, {last['change_4w']:+.1f} vs four weeks ago.", ""]
    dims = out["dimensions"]
    contrib = out["contributions"]
    dc = contrib.pivot(index="week", columns="dimension", values="contribution")
    dchange = (dc.loc[week] - dc.shift(1).loc[week]).sort_values(key=abs, ascending=False)
    shares = contrib.pivot(index="week", columns="dimension", values="share").loc[week] if "share" in contrib.columns else None
    lines.append("## Dimensions")
    lines.append("")
    lines.append("| Dimension | Score | Band | Change (1w) | Share of this week's anxiety | Push on headline |")
    lines.append("|---|---|---|---|---|---|")
    for dim in dchange.index:
        d = dims[(dims["dimension"] == dim)].set_index("week")
        if week not in d.index or pd.isna(d.loc[week, "score"]):
            continue
        prev = d["score"].shift(1).loc[week]
        chg = d.loc[week, "score"] - prev if pd.notna(prev) else float("nan")
        share_txt = f"{100 * shares[dim]:.0f}%" if shares is not None and dim in shares.index else ""
        lines.append(f"| {DIM_LABELS.get(dim, dim)} | {d.loc[week, 'score']:.0f} | {d.loc[week, 'band']} | {chg:+.0f} | {share_txt} | {dchange[dim]:+.3f} |")
    sig = out["signals"]
    sig = sig[sig["week"].isin([week, week - pd.Timedelta(days=7)])].copy()
    piv = sig.pivot_table(index="signal", columns="week", values="z")
    if piv.shape[1] == 2:
        dz = (piv.iloc[:, 1] - piv.iloc[:, 0])
        wts = sig[sig["week"] == week].set_index("signal")["weight"]
        meta = sig[sig["week"] == week].set_index("signal")[["series", "transform", "dimension", "lens", "z"]]
        impact = (dz * wts).dropna().sort_values(key=abs, ascending=False)
        lines += ["", "## Biggest movers among signals", "",
                  "| Signal | Dimension | Lens | Now (z) | Change | Weight |", "|---|---|---|---|---|---|"]
        for key in impact.index[:12]:
            m = meta.loc[key]
            lines.append(f"| {names.get(m['series'], m['series'])} ({m['transform']}) | {DIM_LABELS.get(m['dimension'], m['dimension'])} | {m['lens']} | {m['z']:+.2f} | {dz[key]:+.2f} | {wts[key]:.2f} |")
        lines += ["", "## Most elevated signals right now", "", "| Signal | Dimension | Lens | z |", "|---|---|---|---|"]
        top = meta[meta["z"].notna()].sort_values("z", ascending=False).head(12)
        for key, m in top.iterrows():
            lines.append(f"| {names.get(m['series'], m['series'])} ({m['transform']}) | {DIM_LABELS.get(m['dimension'], m['dimension'])} | {m['lens']} | {m['z']:+.2f} |")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true", help="don't write BigQuery tables")
    parser.add_argument("--end", default=None, help="last week to compute (YYYY-MM-DD)")
    args = parser.parse_args(argv)

    from google.cloud import bigquery
    client = bigquery.Client(project=PROJECT_ID)
    obs, events, catalog = load_inputs(client)
    weights = yaml.safe_load(open(ROOT / "config" / "weights.yaml"))
    signals = yaml.safe_load(open(ROOT / "config" / "signals.yaml"))
    print(f"inputs: {len(obs):,} observations, {len(events):,} events, {len(catalog)} catalog series")

    out = compute.compute_index(obs, events, catalog, signals, weights, start="2000-01-01", end=args.end)
    computed_at = dt.datetime.now(dt.timezone.utc)
    for frame in out.values():
        if isinstance(frame, pd.DataFrame) and "week" in frame.columns:
            frame["methodology_version"] = str(weights["version"])
            frame["computed_at"] = computed_at

    OUT.mkdir(exist_ok=True)
    out["headline"].to_csv(OUT / "headline_weekly.csv", index=False)
    out["dimensions"].to_csv(OUT / "dimension_weekly.csv", index=False)
    latest = out["headline"].dropna(subset=["score"]).tail(1).iloc[0]
    (OUT / "latest.json").write_text(json.dumps({
        "week": str(latest["week"].date()), "score": float(latest["score"]), "band": latest["band"],
        "change_1w": None if pd.isna(latest["change_1w"]) else float(latest["change_1w"]),
        "methodology_version": str(weights["version"]), "computed_at": computed_at.isoformat()}, indent=2))
    charts(out["headline"], out["dimensions"])
    (OUT / "explanation.md").write_text(explanation(out, catalog, signals))
    print(f"latest: week {latest['week'].date()} score {latest['score']} ({latest['band']})")

    if not args.no_write:
        write_table(client, "headline_weekly", out["headline"])
        write_table(client, "dimension_weekly", out["dimensions"])
        write_table(client, "lens_weekly", out["lenses"])
        write_table(client, "signal_weekly", out["signals"])
        write_table(client, "contribution_weekly", out["contributions"])
        print("BigQuery tables written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
