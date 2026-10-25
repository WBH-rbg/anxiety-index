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
   range) using only its own past, with at least two years of history, capped at ±3. Signals whose
   higher values mean less anxiety are inverted.
5. **Staleness.** A value that hasn't updated keeps contributing at full weight for a while
   (monthly: 6 weeks), then fades to zero (monthly: 16 weeks). Other signals renormalize.
6. **Lenses, dimensions, headline.** Weighted averages at each level, each re-standardized against
   its own past (at least one year) so levels with many signals aren't quieter than levels with few.
7. **Percentiles and bands.** The headline and each dimension are ranked against the 2005–2025
   reference period.

## 4. Nonpartisanship

Presidential approval (when added) enters as change from the president's own trailing baseline,
never as a level. Political signals measure uncertainty, policy churn, coverage volume and tone,
all symmetric across administrations.

## 5. What this version lacks

- Attention signals before 2015 (Wikipedia) and 2017 (GDELT). The GDELT events table (1979 onward)
  is the planned fix.
- Mass shooting and protest event data for the safety dimension's conditions lens.
- A presidential approval average and right-track polling.
- Learned weights and the attention-share tilt (both to be tested against the outcome log).
