# Anxiety Index methodology, v0.3 (prototype)

This is the working description of how the index is computed. The code in `index/compute.py`
implements exactly these steps; the numbers live in `config/weights.yaml` and `config/signals.yaml`.
The companion documents are `output/explanation.md` (this week's reading explained),
`output/validation_report.md` (tests), `output/lookahead.md` (the next three weeks) and
`output/forecast.md` (the statistical outlook and its track record).

## 1. What the number means

A weekly reading from 0 to 100 of how primed the US public is to react, built the way fire-danger
ratings are built: current conditions compared against their own history. A reading of 80 means
conditions are more tense than in about 80% of weeks in the reference period (2005–2025).

| Band | Percentile |
|---|---|
| Low | below 20th |
| Moderate | 20th–50th |
| Elevated | 50th–80th |
| High | 80th–95th |
| Severe | 95th and above |

The index measures *priming*: how hot a reaction will be if a story lands. A second reading, news
concentration (section 8), measures how full the news hole is, which governs whether a story lands
at all. The validation note explains why these two move differently.

## 2. Structure

```
Headline (0–100)
 ├── Cost of living (25)   ├── Political & institutional (20)   ├── Jobs & financial security (15)
 ├── Public safety & unrest (15)   ├── Geopolitical (15)   └── Disasters, climate & health (10)
       each dimension = conditions lens + sentiment & expectations lens + attention lens
             each lens = weighted average of standardized signals
```

Everything is additive within dimensions, so every dimension reading and every change decomposes
exactly into lens and signal contributions. The headline combines dimensions with the attention-budget
rule in section 7, whose shares are also exact.

## 3. Steps

1. **Weekly, point-in-time series.** Weeks end on Saturday. Each series takes the latest value that
   was public by the end of the week (daily series are averaged within their week; daily series that
   publish within two days count in their own week). For backfilled history, release timing follows
   each source's usual lag (`RELEASE_LAG_DAYS` in `index/compute.py`); from October 25, 2026 the
   archive records exact timing.
2. **Derived series and event impulses.** Breakeven inflation and the yield-curve spread are built
   from Treasury yields. Earthquakes (magnitude-weighted), disaster declarations and mass shootings
   (fatality-weighted) become weekly severity totals that decay with a two-week half-life.
   Presidential approval is averaged in-house from public poll tables (one poll per pollster in a
   14-day window) and enters as deviation from the sitting president's own term average.
3. **Signals.** Each series is transformed into one or more pressure measures (12-month change,
   3-month annualized change, deviation from a 12-month, 3-year or 5-year average, log of coverage
   against its three-year median, or the level). See `config/signals.yaml`.
4. **Standardization.** Each signal is converted to a robust z-score (median and interquartile
   range). A series' first ten years serve as its base period; after that, each week is compared
   only with its own past (point-in-time). Scores are capped asymmetrically: fear up to +3 spreads,
   relief only down to −1.5 (negativity bias: good news calms less than bad news alarms). Signals
   whose higher values mean less anxiety are inverted first.
   Fast inputs are smoothed with a fast-attack, slow-release rule applied after the signal is
   oriented so that "up" means more anxiety: a rise enters in full immediately, a fall fades with a
   three-week half-life (eight weeks for weekly counts). Fear arrives at once and subsides gradually,
   which keeps the index responsive to shocks without week-to-week whiplash.
   Attention and tone are measured against a three-year norm, so a year-long crisis doesn't become
   "normal" within a year. Prices also enter as their three-year cumulative change, since people
   compare prices with what they remember, not with last year alone.
5. **Staleness.** A value that hasn't updated keeps contributing at full weight for a while
   (monthly: 6 weeks), then fades to zero (monthly: 16 weeks). Other signals renormalize.
6. **Lenses and dimensions.** Weighted averages, each re-standardized against its own past (at least
   half a year) so levels with many signals aren't quieter than levels with few.
7. **Headline: an attention budget.** The six dimension scores are ranked each week; the hottest
   counts in full, the next at half, the next at a quarter, and so on, each also scaled by its prior
   weight, then renormalized. Two pieces of bad news add, but the second adds less than the first:
   people can hold only so much. Each dimension's share of the week's attention budget is exact and
   is what the weekly explanation reports. (A plain weighted mean let calm dimensions cancel out the
   COVID onset; a soft maximum fixed that but let a second crisis add almost nothing.) The headline is
   ranked directly against the reference period, with no further standardization.
8. **Percentiles, bands and news concentration.** The headline and each dimension are ranked
   against the 2005–2025 reference period. News concentration is the Herfindahl index of the six
   dimensions' article counts in US news that week, ranked the same way: a high value means one story
   dominates coverage and the news hole is full.

## 4. Nonpartisanship

Presidential approval enters as deviation from the sitting president's own term average and as its
13-week change, never as a level, so a popular and an unpopular president contribute the same
nothing at their own baselines. Political signals measure uncertainty, policy churn, coverage volume
and tone, all symmetric across administrations.

## 5. Calendars and the look-ahead

Two hand-compiled calendars (`docs/calendar/`) are tested against the index every day and feed
`output/lookahead.md`. They are not inputs to the headline.

- **Catalysts** (545 dated events 2015–2027): Fed decisions, CPI and jobs-report days, elections,
  States of the Union, Supreme Court term ends, debt-limit and funding deadlines, shutdowns, tax day,
  hurricane season. For each kind, the tests report the headline and dimension moves in the two weeks
  before, the week of, and the week after. Elections and Supreme Court term ends spike the political
  dimension in the week and release it the week after; deadline weeks are when deals land, so the
  political reading drops; scheduled data days barely register, because the index reacts to what
  numbers say, not to the fact of their release.
- **Shared cultural events** (201 entries 2015–2026, scored 1–3 for how widely shared): weeks
  overlapping a scale-3 event run about 8 points quieter with falling attention, but the first week
  after one closes carries a higher-than-usual rate of major corporate episodes, as held
  announcements land. The look-ahead says so whenever such an event is coming.

## 6. The outlook

`index/forecast.py` publishes a small statistical forecast at 1, 2, 4 and 8 weeks with its own track
record: half-weight on a ridge regression of future change on the current level, recent momentum and
the six dimension readings with their four-week changes, half-weight on "no change." It is refit
yearly in an expanding-window backtest from 2010, and its ranges are the empirical quantiles of its
backtest errors. It beats persistence modestly (1% at one week, 9% at eight) because it learns that
readings far above normal ease back and that shock-driven anxiety fades faster than background
pressure. Every forecast is stored in `ai_index.forecasts` to be scored against what happens.

## 7. Validation so far

Twelve historical periods read as expected (nine tense periods reach High or Severe; three calm
periods average under 40). Against a curated log of 119 corporate backlash episodes, major episodes
in the following two weeks run from 23 per 100 weeks after Low readings to 46 after Severe; political
and jobs anxiety run hottest before episodes. A systematic coverage-spike detector shows the
opposite relationship, which is the crowding-out effect: tense weeks make a company story less likely
to land and angrier when it does. Details in `output/validation_report.md` and the project's
validation note.

## 8. What this version lacks

- Attention signals before 2000 are absent and thin before 2015; readings before 2001 are not
  reliable and should not be published.
- Licensing: VIX, University of Michigan surveys and pollster trackers restrict commercial use and
  will be licensed before publication.
- A larger, hand-checked outcome log, so the priming effect can be measured on hundreds of episodes.
- Learned dimension weights (the priors above are judgment, tested but not fitted).
- A daily nowcast between weekly readings.
