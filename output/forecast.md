# Outlook from the week ending 2026-11-14

Current reading: **56 (Elevated)**. The table shows where a small statistical model expects the headline to be, with ranges taken from the model's own historical errors. Treat it as tendency, not prediction: at these horizons the model beats "no change" only modestly (see the track record below), and scheduled catalysts in `lookahead.md` can override any of it.

| Weeks ahead | Week ending | Expected | 50% range | 80% range | Chance up 5+ | Chance down 5+ | Chance High or Severe | Chance below 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-11-21 | 56 (Elevated) | 52–59 | 47–66 | 19% | 22% | 2% | 18% |
| 2 | 2026-11-28 | 57 (Elevated) | 50–62 | 42–72 | 30% | 29% | 5% | 25% |
| 4 | 2026-12-12 | 56 (Elevated) | 46–66 | 36–78 | 37% | 35% | 8% | 33% |
| 8 | 2027-01-09 | 55 (Elevated) | 41–71 | 25–84 | 42% | 40% | 13% | 39% |

## Why (four-week horizon)

Expected change in points, by what is driving it:

- Where the reading sits relative to normal, and its recent momentum: **-2.1**
- How much of it is shock-driven (safety, geopolitics, disasters), which fades faster: **+0.4**
- How much of it is background pressure (cost of living, jobs, politics), which persists: **+1.7**

Largest single factors: public safety and unrest reading (+1.5); the quarter's move (-1.3); political and institutional reading (+1.2); geopolitical reading (-1.0).

## What has usually happened from here

Weeks since 2010 that showed the same band, and where the headline was afterwards:

| Band now | Weeks ahead | Weeks | Average then | Average later | Higher by 5+ | Lower by 5+ | High or Severe later | Below 50 later |
|---|---|---|---|---|---|---|---|---|
| Low | 2 | 142 | 9.9 | 17.1 | 36% | 13% | 1% | 93% |
| Moderate | 2 | 258 | 35.8 | 37.3 | 38% | 35% | 1% | 78% |
| **Elevated** | 2 | 295 | 64.7 | 60.9 | 22% | 41% | 8% | 23% |
| High | 2 | 146 | 87.6 | 85.8 | 11% | 29% | 82% | 0% |
| Severe | 2 | 38 | 97.7 | 96.1 | 0% | 11% | 100% | 0% |
| Low | 4 | 142 | 9.9 | 21.7 | 51% | 11% | 0% | 88% |
| Moderate | 4 | 258 | 35.8 | 39.4 | 45% | 36% | 2% | 68% |
| **Elevated** | 4 | 293 | 64.7 | 58.6 | 26% | 47% | 15% | 33% |
| High | 4 | 146 | 87.6 | 83.2 | 16% | 43% | 69% | 1% |
| Severe | 4 | 38 | 97.7 | 93.5 | 0% | 32% | 92% | 0% |
| Low | 8 | 142 | 9.9 | 31.1 | 67% | 11% | 0% | 75% |
| Moderate | 8 | 257 | 35.8 | 41.2 | 54% | 34% | 4% | 59% |
| **Elevated** | 8 | 290 | 64.7 | 55.8 | 31% | 54% | 21% | 42% |
| High | 8 | 146 | 87.6 | 76.9 | 21% | 55% | 55% | 12% |
| Severe | 8 | 38 | 97.7 | 91.2 | 0% | 53% | 92% | 0% |

## Track record (yearly-refit backtest, no look-ahead)

Mean absolute error in percentile points, 2010 onward. "Persistence" is the forecast that nothing changes.

| Weeks ahead | Weeks tested | Persistence error | Model error | Improvement | Direction right | Direction right when confident | Weeks that rose 5+ | Weeks that fell 5+ |
|---|---|---|---|---|---|---|---|---|
| 1.0 | 880.0 | 6.24 | 6.16 | +1% | 58% | 67% | 19% | 24% |
| 2.0 | 879.0 | 9.44 | 9.22 | +2% | 60% | 70% | 26% | 32% |
| 4.0 | 877.0 | 13.51 | 12.92 | +4% | 66% | 78% | 33% | 37% |
| 8.0 | 873.0 | 19.58 | 17.79 | +9% | 68% | 75% | 41% | 41% |

How to read this: the index is persistent, so the best one- or two-week forecast is close to the current reading. The model's edge grows with the horizon because it knows two things persistence doesn't: readings far above normal ease back, and anxiety driven by shocks fades faster than anxiety driven by background pressure. "Confident" means the quarter of weeks where the model expected the largest moves.

The model is half-weight ridge regression on the current level, recent momentum, and the six dimension readings with their four-week changes; it is refit every year on data up to that year. Forecasts are stored in `ai_index.forecasts` so they can be scored against what actually happened.

## Forecasts issued so far, scored

| Weeks ahead | Forecasts scored | Model error | Persistence error | Inside 80% range |
|---|---|---|---|---|
| 1 | 3 | 7.9 | 5.3 | 67% |
| 2 | 2 | 6.5 | 9.9 | 100% |

Most recent scored forecasts:

| Issued for week | Weeks ahead | Target week | Forecast | Actual | Error |
|---|---|---|---|---|---|
| 2026-10-24 | 1 | 2026-10-31 | 58 | 70 | -12.0 |
| 2026-10-24 | 2 | 2026-11-07 | 58 | 66 | -8.8 |
| 2026-10-31 | 1 | 2026-11-07 | 60 | 66 | -6.2 |
| 2026-10-31 | 2 | 2026-11-14 | 60 | 56 | +4.2 |
| 2026-11-07 | 1 | 2026-11-14 | 62 | 56 | +5.4 |
