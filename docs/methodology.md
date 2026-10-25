# Anxiety Index methodology, v0.1 (prototype)

This is the working description of how the index is computed. The code in `index/compute.py`
implements exactly these steps; the numbers live in `config/weights.yaml` and `config/signals.yaml`.

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

## 2. Structure

```
Headline (0–100)
 ├── Cost of living (25)   ├── Jobs & financial security (20)   ├── Political & institutional (15)
 ├── Public safety & unrest (15)   ├── Geopolitical (15)   └── Disasters, climate & health (10)
       each dimension = conditions lens + sentiment lens + attention lens
             each lens = weighted average of standardized signals
```

Everything is additive, so every reading and every change decomposes exactly into dimension,
lens and signal contributions.

## 3. Steps

1. **Weekly, point-in-time series.** Weeks end on Saturday. Each series takes the latest value that
   was public by the end of the week (daily series are averaged within their week). For backfilled
   history, release timing follows each source's usual lag (`RELEASE_LAG_DAYS` in `index/compute.py`);
   from October 25, 2026 the archive records exact timing.
2. **Derived series and event impulses.** Breakeven inflation and the yield-curve spread are built
   from Treasury yields. Earthquakes and disaster declarations become weekly severity totals that
   decay with a two-week half-life.
3. **Signals.** Each series is transformed into one or more pressure measures (12-month change,
   3-month annualized change, deviation from a 12-month or 5-year average, log of coverage vs. the
   trailing-year median, or the level). See `config/signals.yaml`.
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
7. **Headline.** A weighted *soft maximum* of the six dimension scores (log of the weighted mean of
   exp(z)): the hottest dimensions dominate, but every dimension still counts, and each dimension's
   share of the week's anxiety is exact. Anxiety is driven by the worst thing happening, not the
   average thing; a weighted mean let calm dimensions cancel out the COVID onset. The headline is
   ranked directly against the reference period, with no further standardization.
8. **Percentiles and bands.** The headline and each dimension are ranked against the 2005–2025
   reference period.

## 4. Nonpartisanship

Presidential approval (when added) enters as change from the president's own trailing baseline,
never as a level. Political signals measure uncertainty, policy churn, coverage volume and tone,
all symmetric across administrations.

## 5. Face validity (prototype, October 25, 2026)

Reading as Severe or High: late 2001 (9/11), March 2003 (Iraq), autumn 2008 through 2009, 2011
(debt ceiling, gas prices, Arab Spring), early 2017, March 2020, summer 2020, January 2021, 2022
(Ukraine, inflation peak), spring 2025 (tariffs). Reading as Low: 2004–2007, 2012–2015. Cost of
living stays at the top from mid-2021 through 2023. Median week-to-week move: about 4 points.

## 6. What this version lacks

- Attention signals before 2015 (Wikipedia) and 2017 (GDELT). The GDELT events table (1979 onward)
  is the planned fix.
- Mass shooting and protest event data for the safety dimension's conditions lens.
- A presidential approval average and right-track polling.
- Learned weights and the attention-share tilt (both to be tested against the outcome log).
