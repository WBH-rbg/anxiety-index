# Anxiety Index

A weekly index of US public anxiety, built for senior decision makers at large companies and for
communications and reputation professionals.

The index works like a fire-danger rating for public mood. It doesn't predict specific events; it
measures how primed people are to react, so the same spark can fizzle in a calm period or catch fire
in an anxious one.

## Layout

| Path | What it is |
|---|---|
| `collectors/` | Data collectors, one module per source, run daily by GitHub Actions |
| `config/series.yaml` | Every collected series, tagged with its dimension and lens |
| `config/signals.yaml` | How each series becomes an anxiety signal (transform, weight) |
| `config/weights.yaml` | Dimension and lens weights, bands, standardization settings |
| `index/` | The index computation (`compute.py`) and its runner (`run.py`) |
| `docs/methodology.md` | The methodology, in plain language |
| `docs/source_inventory.csv` | Every candidate source considered, with terms and status |
| `output/` | Latest computed index: CSVs, charts, `latest.json` (written by the workflow) |
| `scripts/setup_gcp.sh` | One-time Google Cloud setup |

## How it runs

- **Collect data** (`.github/workflows/collect.yml`): daily at 11:15 UTC. Every pull is archived unchanged
  to `gs://anxiety-index-raw-archive` and loaded into BigQuery (`ai_raw.observations`, `ai_raw.events`),
  so revisions are preserved and every value carries the time it became known.
- **Compute index** (`.github/workflows/index.yml`): daily at 12:45 UTC. Writes `ai_index.*` tables and
  commits charts and CSVs to `output/`.

Run either by hand from the Actions tab. `python -m collectors.run --help` and `python -m index.run --help`
describe the options.

## BigQuery

| Dataset | Contents |
|---|---|
| `ai_raw` | Source data exactly as collected (`observations`, `events`, `series_catalog`, `runs`) |
| `ai_clean` | Latest-value views and the `observations_as_of(timestamp)` function for point-in-time queries |
| `ai_index` | Weekly signals, lenses, dimensions, headline, contributions |
| `ai_outcomes` | Curated outcome log (to come) |

## Principles

1. Explainable: every move comes with a plain-language explanation of what drove it
2. Timely: fast signals carry the current reading; polls confirm and calibrate
3. Readable at a glance: score, band, direction, top drivers
4. Visibly nonpartisan
5. Multiple durable sources per dimension
6. Learns over time, tested honestly (point-in-time)
7. Accountable record: every published reading is archived as released

## Data terms

Open-access sources are used during model development. Several (VIX, University of Michigan surveys,
pollster trackers) restrict commercial use and will be licensed before anything is published.
Collectors pull from each primary publisher, not from FRED, whose terms forbid archiving.
