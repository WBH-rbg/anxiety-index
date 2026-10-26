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
| `index/` | The index computation (`compute.py`), its runner (`run.py`), scenarios (`scenario.py`), validation (`validate.py`), calendars and look-ahead (`calendar.py`), the statistical outlook (`forecast.py`) |
| `docs/methodology.md` | The methodology, in plain language |
| `docs/source_inventory.csv` | Every candidate source considered, with terms and status |
| `docs/outcomes/` | Curated corporate backlash log used to test the index |
| `docs/calendar/` | Catalyst calendar (Fed, CPI, jobs, elections, deadlines) and shared cultural events |
| `output/` | Latest computed index, written by the workflow (see below) |
| `scripts/setup_gcp.sh` | One-time Google Cloud setup |

## What the daily run publishes to `output/`

| File | What it is |
|---|---|
| `latest.json`, `explanation.md` | This week's reading, band, drivers and a plain-language explanation |
| `headline_weekly.csv`, `dimension_weekly.csv`, charts | Full weekly history |
| `scenarios.md` | What the reading would be under ten canned shocks |
| `validation_report.md` | Face validity, outcome tests, external series |
| `calendar_tests.md`, `lookahead.md` | Catalyst effects, cultural-window test, and the next three weeks |
| `forecast.md`, `forecast.csv` | Statistical outlook at 1–8 weeks with its backtest track record |
| `*.log` | Each step's log, for review without the Actions console |

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
| `ai_index` | Weekly signals, lenses, dimensions, headline, contributions, scenarios, catalyst effects, forecasts |
| `ai_outcomes` | Curated backlash log and the systematic company-pressure table |

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
