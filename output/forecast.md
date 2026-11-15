# Outlook from the week ending 2026-11-14

Current reading: **56 (Elevated)**. The table shows where a small statistical model expects the headline to be, with ranges taken from the model's own historical errors. Treat it as tendency, not prediction: at these horizons the model beats "no change" only modestly (see the track record below), and scheduled catalysts in `lookahead.md` can override any of it.

| Weeks ahead | Week ending | Expected | 50% range | 80% range | Chance up 5+ | Chance down 5+ | Chance High or Severe | Chance below 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-11-21 | 56 (Elevated) | 52–59 | 47–66 | 19% | 22% | 2% | 17% |
| 2 | 2026-11-28 | 57 (Elevated) | 50–62 | 42–72 | 29% | 29% | 5% | 25% |
| 4 | 2026-12-12 | 56 (Elevated) | 47–66 | 36–78 | 38% | 35% | 8% | 33% |
| 8 | 2027-01-09 | 55 (Elevated) | 41–71 | 26–84 | 42% | 41% | 13% | 39% |

## Why (four-week horizon)

Expected change in points, by what is driving it:

- Where the reading sits relative to normal, and its recent momentum: **-2.1**
- How much of it is shock-driven (safety, geopolitics, disasters), which fades faster: **+0.5**
- How much of it is background pressure (cost of living, jobs, politics), which persists: **+1.6**

Largest single factors: public safety and unrest reading (+1.6); the quarter's move (-1.3); political and institutional reading (+1.1); geopolitical reading (-1.0).

## What has usually happened from here

Weeks since 2010 that showed the same band, and where the headline was afterwards:

| Band now | Weeks ahead | Weeks | Average then | Average later | Higher by 5+ | Lower by 5+ | High or Severe later | Below 50 later |
|---|---|---|---|---|---|---|---|---|
| Low | 2 | 141 | 9.8 | 16.7 | 35% | 12% | 1% | 94% |
| Moderate | 2 | 259 | 35.7 | 37.4 | 37% | 35% | 1% | 77% |
| **Elevated** | 2 | 296 | 64.8 | 61.0 | 23% | 42% | 8% | 23% |
| High | 2 | 145 | 87.7 | 85.9 | 11% | 30% | 82% | 0% |
| Severe | 2 | 38 | 97.7 | 96.1 | 0% | 11% | 100% | 0% |
| Low | 4 | 141 | 9.8 | 21.5 | 51% | 11% | 0% | 88% |
| Moderate | 4 | 259 | 35.7 | 39.4 | 45% | 36% | 2% | 68% |
| **Elevated** | 4 | 294 | 64.7 | 58.5 | 26% | 48% | 14% | 33% |
| High | 4 | 145 | 87.7 | 83.6 | 17% | 43% | 70% | 1% |
| Severe | 4 | 38 | 97.7 | 93.5 | 0% | 29% | 95% | 0% |
| Low | 8 | 141 | 9.8 | 30.8 | 67% | 11% | 0% | 76% |
| Moderate | 8 | 258 | 35.7 | 41.3 | 55% | 34% | 4% | 59% |
| **Elevated** | 8 | 291 | 64.7 | 55.7 | 31% | 54% | 20% | 43% |
| High | 8 | 145 | 87.7 | 77.1 | 21% | 54% | 56% | 11% |
| Severe | 8 | 38 | 97.7 | 91.2 | 0% | 53% | 92% | 0% |

## Track record (yearly-refit backtest, no look-ahead)

Mean absolute error in percentile points, 2010 onward. "Persistence" is the forecast that nothing changes.

| Weeks ahead | Weeks tested | Persistence error | Model error | Improvement | Direction right | Direction right when confident | Weeks that rose 5+ | Weeks that fell 5+ |
|---|---|---|---|---|---|---|---|---|
| 1.0 | 880.0 | 6.21 | 6.13 | +1% | 59% | 67% | 19% | 24% |
| 2.0 | 879.0 | 9.43 | 9.22 | +2% | 60% | 71% | 26% | 32% |
| 4.0 | 877.0 | 13.51 | 12.92 | +4% | 65% | 76% | 33% | 37% |
| 8.0 | 873.0 | 19.56 | 17.79 | +9% | 68% | 74% | 41% | 41% |

How to read this: the index is persistent, so the best one- or two-week forecast is close to the current reading. The model's edge grows with the horizon because it knows two things persistence doesn't: readings far above normal ease back, and anxiety driven by shocks fades faster than anxiety driven by background pressure. "Confident" means the quarter of weeks where the model expected the largest moves.

The model is half-weight ridge regression on the current level, recent momentum, and the six dimension readings with their four-week changes; it is refit every year on data up to that year. Forecasts are stored in `ai_index.forecasts` so they can be scored against what actually happened.

## Forecasts issued so far, scored

| Weeks ahead | Forecasts scored | Model error | Persistence error | Inside 80% range |
|---|---|---|---|---|
| 1 | 3 | 7.7 | 5.3 | 67% |
| 2 | 2 | 6.2 | 10.1 | 100% |

Most recent scored forecasts:

| Issued for week | Weeks ahead | Target week | Forecast | Actual | Error |
|---|---|---|---|---|---|
| 2026-10-24 | 1 | 2026-10-31 | 58 | 70 | -12.0 |
| 2026-10-24 | 2 | 2026-11-07 | 58 | 66 | -8.4 |
| 2026-10-31 | 1 | 2026-11-07 | 60 | 66 | -5.8 |
| 2026-10-31 | 2 | 2026-11-14 | 60 | 56 | +4.1 |
| 2026-11-07 | 1 | 2026-11-14 | 62 | 56 | +5.3 |
