"""Scenario analysis: how would the index move if X happened this week?

Because the index is additive and deterministic, a scenario is just a
perturbation of the latest week's inputs followed by a recompute. History is
untouched, so the difference isolates the shock.

    python -m index.scenario            # runs the canned scenarios, writes output/scenarios.md
    python -m index.scenario --list     # shows them

A scenario is a list of operations:
  {"series": "<id>", "op": "pct"|"add"|"set", "value": v, "weeks": n}  change recent observations
  {"event": {...}}                                                      add a synthetic event
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
from pathlib import Path

import pandas as pd
import yaml

from index import compute
from index.run import DIM_LABELS, ROOT, OUT, load_inputs

SCENARIOS = {
    "gas_up_10pct": {
        "title": "Gasoline up 10% this week",
        "ops": [{"series": "eia_gas_regular_weekly", "op": "pct", "value": 10, "weeks": 1},
                {"series": "eia_wti_daily", "op": "pct", "value": 10, "weeks": 1},
                {"series": "gkg_share_cost_of_living", "op": "pct", "value": 25, "weeks": 1}],
    },
    "hot_cpi_print": {
        "title": "CPI comes in 0.5 points hotter than last month's level implies",
        "ops": [{"series": "bls_cpi_all_sa", "op": "pct", "value": 0.5, "weeks": 6},
                {"series": "bls_cpi_all_nsa", "op": "pct", "value": 0.5, "weeks": 6},
                {"series": "bls_cpi_food_at_home", "op": "pct", "value": 0.7, "weeks": 6},
                {"series": "gkg_share_cost_of_living", "op": "pct", "value": 40, "weeks": 1}],
    },
    "fed_surprise_hike": {
        "title": "Fed surprise: 2-year yield jumps 50bp, VIX +8, markets coverage doubles",
        "ops": [{"series": "ust_2y", "op": "add", "value": 0.5, "weeks": 1},
                {"series": "vix_close", "op": "add", "value": 8, "weeks": 1},
                {"series": "gkg_share_jobs_financial", "op": "pct", "value": 100, "weeks": 1}],
    },
    "jobless_claims_spike": {
        "title": "Initial jobless claims jump 30% for the week",
        "ops": [{"series": "dol_initial_claims_nsa", "op": "pct", "value": 30, "weeks": 1},
                {"series": "gkg_share_jobs_financial", "op": "pct", "value": 50, "weeks": 1},
                {"series": "wiki_layoff", "op": "pct", "value": 100, "weeks": 1}],
    },
    "major_california_quake": {
        "title": "Magnitude 7.0 earthquake near Los Angeles",
        "ops": [{"event": {"source": "usgs", "event_type": "earthquake", "area": "us_lower48", "magnitude": 7.0,
                           "title": "M 7.0 - near Los Angeles, CA", "attributes": {}}},
                {"series": "gkg_share_disasters_health", "op": "pct", "value": 150, "weeks": 1},
                {"series": "wiki_earthquake", "op": "pct", "value": 2000, "weeks": 1}],
    },
    "gulf_hurricane_landfall": {
        "title": "Major hurricane landfall: 60 counties declared, disaster coverage triples",
        "ops": [{"event": {"source": "fema", "event_type": "Hurricane", "state": "FL", "area": "multiple",
                           "title": "HURRICANE (scenario)", "attributes": {"declarationType": "DR"}, "count": 60}},
                {"series": "gkg_share_disasters_health", "op": "pct", "value": 200, "weeks": 1},
                {"series": "wiki_hurricane", "op": "pct", "value": 1000, "weeks": 1}],
    },
    "war_coverage_doubles": {
        "title": "Geopolitical flare-up: conflict coverage doubles, GPR threats +50%, Brent +15%",
        "ops": [{"series": "gkg_share_geopolitical", "op": "pct", "value": 100, "weeks": 1},
                {"series": "gpr_daily_threats", "op": "pct", "value": 50, "weeks": 1},
                {"series": "gpr_daily", "op": "pct", "value": 40, "weeks": 1},
                {"series": "eia_brent_daily", "op": "pct", "value": 15, "weeks": 1},
                {"series": "wiki_world_war_3", "op": "pct", "value": 500, "weeks": 1}],
    },
    "mass_shooting_national": {
        "title": "Mass shooting dominates the week: violence coverage +80%, shooting pageviews x10",
        "ops": [{"series": "gkg_share_safety_unrest", "op": "pct", "value": 80, "weeks": 1},
                {"series": "gkg_tone_safety_unrest", "op": "add", "value": -1.5, "weeks": 1},
                {"series": "gdelt_ev_violence_share", "op": "pct", "value": 60, "weeks": 1},
                {"series": "wiki_mass_shooting", "op": "pct", "value": 900, "weeks": 1},
                {"series": "wiki_school_shooting", "op": "pct", "value": 900, "weeks": 1}],
    },
    "government_shutdown": {
        "title": "Government shutdown begins: political crisis coverage +120%, EPU +60%",
        "ops": [{"series": "gkg_share_political", "op": "pct", "value": 120, "weeks": 1},
                {"series": "epu_us_daily", "op": "pct", "value": 60, "weeks": 1},
                {"series": "wiki_government_shutdown", "op": "pct", "value": 3000, "weeks": 1}],
    },
    "calm_week": {
        "title": "Quiet week: coverage of every dimension 25% below current",
        "ops": [{"series": s, "op": "pct", "value": -25, "weeks": 1} for s in
                ["gkg_share_cost_of_living", "gkg_share_jobs_financial", "gkg_share_political",
                 "gkg_share_safety_unrest", "gkg_share_disasters_health", "gkg_share_geopolitical"]],
    },
}


def apply_ops(obs: pd.DataFrame, events: pd.DataFrame, ops: list[dict], as_of: pd.Timestamp):
    obs = obs.copy()
    extra_events = []
    for op in ops:
        if "event" in op:
            e = dict(op["event"])
            count = int(e.pop("count", 1))
            for i in range(count):
                extra_events.append({"source": e["source"], "event_date": as_of - pd.Timedelta(days=2), "event_type": e.get("event_type"),
                                     "area": e.get("area"), "magnitude": e.get("magnitude"), "title": e.get("title"),
                                     "attributes": e.get("attributes", {})})
            continue
        sid = op["series"]
        mask = (obs["series_id"] == sid) & (obs["obs_date"] > as_of - pd.Timedelta(weeks=op.get("weeks", 1)))
        if not mask.any():
            # monthly series: perturb the latest observation instead
            latest = obs.loc[obs["series_id"] == sid, "obs_date"].max()
            mask = (obs["series_id"] == sid) & (obs["obs_date"] == latest)
        if op["op"] == "pct":
            obs.loc[mask, "value"] = obs.loc[mask, "value"] * (1 + op["value"] / 100.0)
        elif op["op"] == "add":
            obs.loc[mask, "value"] = obs.loc[mask, "value"] + op["value"]
        elif op["op"] == "set":
            obs.loc[mask, "value"] = op["value"]
    if extra_events:
        events = pd.concat([events, pd.DataFrame(extra_events)], ignore_index=True)
    return obs, events


def latest_row(out: dict) -> tuple[pd.Series, pd.DataFrame]:
    h = out["headline"].dropna(subset=["score"]).iloc[-1]
    d = out["dimensions"][out["dimensions"]["week"] == h["week"]].set_index("dimension")
    return h, d


def run_scenarios(obs, events, catalog, signals, weights, names=None) -> tuple[pd.DataFrame, pd.Series]:
    base = compute.compute_index(obs, events, catalog, signals, weights, start="2000-01-01")
    h0, d0 = latest_row(base)
    as_of = pd.Timestamp(h0["week"])
    rows = []
    for key, sc in SCENARIOS.items():
        if names and key not in names:
            continue
        o2, e2 = apply_ops(obs, events, sc["ops"], as_of)
        out = compute.compute_index(o2, e2, catalog, signals, weights, start="2000-01-01")
        h1, d1 = latest_row(out)
        row = {"scenario": key, "title": sc["title"], "headline_before": h0["score"], "headline_after": h1["score"],
               "headline_change": round(h1["score"] - h0["score"], 1), "band_after": h1["band"],
               "z_change": round(h1["z"] - h0["z"], 3)}
        for dim in d0.index:
            row[f"{dim}_change"] = round(d1.loc[dim, "score"] - d0.loc[dim, "score"], 1) if dim in d1.index else None
        rows.append(row)
        print(f"{key}: {h0['score']:.0f} -> {h1['score']:.0f} ({row['headline_change']:+.1f}, {h1['band']})", flush=True)
    return pd.DataFrame(rows), h0


def write_report(table: pd.DataFrame, h0: pd.Series) -> str:
    dims = [c[:-7] for c in table.columns if c.endswith("_change") and c not in ("headline_change", "z_change")]
    lines = [f"# Scenarios for the week ending {pd.Timestamp(h0['week']).date()}", "",
             f"Current reading: **{h0['score']:.0f} ({h0['band']})**. Each row changes this week's inputs as described and recomputes the index; history is unchanged.", "",
             "| Scenario | Headline | Band | " + " | ".join(DIM_LABELS.get(d, d) for d in dims) + " |",
             "|---|---|---|" + "---|" * len(dims)]
    for _, r in table.sort_values("headline_change", ascending=False).iterrows():
        cells = [f"{r['title']}", f"{r['headline_before']:.0f} → {r['headline_after']:.0f} ({r['headline_change']:+.0f})", r["band_after"]]
        cells += [f"{r[f'{d}_change']:+.0f}" if pd.notna(r[f"{d}_change"]) else "" for d in dims]
        lines.append("| " + " | ".join(cells) + " |")
    lines += ["", "Changes are in percentile points. A scenario's effect depends on where the index already is: the same shock moves a calm week more than a week already near the top of its range."]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--only", default=None, help="comma-separated scenario keys")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args(argv)
    if args.list:
        for k, v in SCENARIOS.items():
            print(f"{k}: {v['title']}")
        return 0
    from google.cloud import bigquery
    client = bigquery.Client(project=compute.PROJECT_ID if hasattr(compute, "PROJECT_ID") else "anxiety-index")
    obs, events, catalog = load_inputs(client)
    weights = yaml.safe_load(open(ROOT / "config" / "weights.yaml"))
    signals = yaml.safe_load(open(ROOT / "config" / "signals.yaml"))
    names = [s.strip() for s in args.only.split(",")] if args.only else None
    table, h0 = run_scenarios(obs, events, catalog, signals, weights, names)
    OUT.mkdir(exist_ok=True)
    (OUT / "scenarios.md").write_text(write_report(table, h0))
    table.to_csv(OUT / "scenarios.csv", index=False)
    if not args.no_write:
        table["week"] = pd.Timestamp(h0["week"])
        table["computed_at"] = dt.datetime.now(dt.timezone.utc)
        client.load_table_from_dataframe(table, "anxiety-index.ai_index.scenarios",
                                         job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")).result()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
