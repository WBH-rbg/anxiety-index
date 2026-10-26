"""Run collectors.

    python -m collectors.run --sources all --mode incremental
    python -m collectors.run --sources bls,eia --mode backfill
    python -m collectors.run --sources wikipedia --dry-run      # no cloud writes

Each collector is independent: one failing doesn't stop the others. Results,
warnings and errors are recorded in BigQuery table ai_raw.runs.
"""
from __future__ import annotations

import argparse
import importlib
import sys
import traceback

from collectors import core

SOURCES = ["bls", "eia", "usgs", "fema", "gpr", "epu", "wikipedia",
           "gdelt_gkg", "gdelt_events", "dol", "treasury", "fedreg", "markets", "umich", "freddiemac", "nyfed", "tpu", "approval", "shootings", "silverbulletin"]
RETIRED = ["gdelt"]  # DOC API collector: throttled too hard for daily use; runnable by name only


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sources", default="all", help="comma-separated collectors, or 'all'")
    parser.add_argument("--mode", default="incremental", choices=["incremental", "backfill"])
    parser.add_argument("--dry-run", action="store_true", help="fetch and parse only; write nothing to the cloud")
    args = parser.parse_args(argv)

    selected = SOURCES if args.sources.strip() in {"", "all"} else [s.strip() for s in args.sources.split(",") if s.strip()]
    unknown = [s for s in selected if s not in SOURCES + RETIRED]
    if unknown:
        parser.error(f"unknown sources {unknown}; choose from {SOURCES}")

    catalog = core.load_catalog()
    if not args.dry_run:
        core.write_catalog(catalog)

    failures = 0
    for name in selected:
        col = core.Collection(name, args.mode, dry_run=args.dry_run)
        try:
            module = importlib.import_module(f"collectors.sources.{name}")
            module.collect(col, [s for s in catalog if s["source"] == name])
            status = "partial" if col.warnings else "success"
            nothing = not (col.observations or col.events or col.flushed_observations or col.flushed_events)
            if nothing and col.mode == "backfill":
                status = "failed"
                col.messages.append("ERROR no rows collected")
        except Exception:
            status = "failed"
            col.messages.append("ERROR " + traceback.format_exc()[-4000:])
            print(traceback.format_exc(), file=sys.stderr, flush=True)
        try:
            status = col.finish(status)
        except Exception:
            status = "failed"
            print(f"[{name}] could not record results:\n{traceback.format_exc()}", file=sys.stderr, flush=True)
        failures += status == "failed"

    print(f"Done: {len(selected) - failures} of {len(selected)} collectors succeeded", flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
