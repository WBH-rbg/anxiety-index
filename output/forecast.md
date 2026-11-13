# Outlook from the week ending 2026-11-07

Current reading: **66 (Elevated)**. The table shows where a small statistical model expects the headline to be, with ranges taken from the model's own historical errors. Treat it as tendency, not prediction: at these horizons the model beats "no change" only modestly (see the track record below), and scheduled catalysts in `lookahead.md` can override any of it.

| Weeks ahead | Week ending | Expected | 50% range | 80% range | Chance up 5+ | Chance down 5+ | Chance High or Severe | Chance below 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-11-14 | 66 (Elevated) | 62–69 | 57–76 | 19% | 21% | 6% | 2% |
| 2 | 2026-11-21 | 67 (Elevated) | 60–72 | 52–82 | 31% | 29% | 12% | 8% |
| 4 | 2026-12-05 | 66 (Elevated) | 56–75 | 46–88 | 36% | 36% | 18% | 15% |
| 8 | 2027-01-02 | 63 (Elevated) | 50–79 | 33–92 | 39% | 43% | 23% | 26% |

## Why (four-week horizon)

Expected change in points, by what is driving it:

- Where the reading sits relative to normal, and its recent momentum: **-3.5**
- How much of it is shock-driven (safety, geopolitics, disasters), which fades faster: **+0.5**
- How much of it is background pressure (cost of living, jobs, politics), which persists: **+2.6**

Largest single factors: the quarter's move (-2.1); political and institutional reading (+1.6); public safety and unrest reading (+1.3); the headline level (-1.2).

## What has usually happened from here

Weeks since 2010 that showed the same band, and where the headline was afterwards:

| Band now | Weeks ahead | Weeks | Average then | Average later | Higher by 5+ | Lower by 5+ | High or Severe later | Below 50 later |
|---|---|---|---|---|---|---|---|---|
| Low | 2 | 142 | 9.9 | 17.1 | 36% | 12% | 1% | 93% |
| Moderate | 2 | 258 | 35.6 | 37.1 | 39% | 35% | 0% | 77% |
| **Elevated** | 2 | 295 | 64.7 | 61.1 | 23% | 40% | 9% | 23% |
| High | 2 | 145 | 87.7 | 85.9 | 12% | 30% | 81% | 0% |
| Severe | 2 | 38 | 97.7 | 96.1 | 0% | 11% | 100% | 0% |
| Low | 4 | 142 | 9.9 | 21.7 | 51% | 11% | 0% | 88% |
| Moderate | 4 | 258 | 35.6 | 39.1 | 44% | 36% | 2% | 68% |
| **Elevated** | 4 | 293 | 64.7 | 58.6 | 27% | 48% | 14% | 33% |
| High | 4 | 145 | 87.7 | 83.5 | 16% | 43% | 69% | 1% |
| Severe | 4 | 38 | 97.7 | 93.5 | 0% | 29% | 95% | 0% |
| Low | 8 | 142 | 9.9 | 31.1 | 67% | 11% | 0% | 75% |
| Moderate | 8 | 256 | 35.6 | 41.0 | 54% | 35% | 4% | 59% |
| **Elevated** | 8 | 291 | 64.7 | 55.7 | 31% | 54% | 20% | 42% |
| High | 8 | 145 | 87.7 | 77.0 | 21% | 54% | 55% | 12% |
| Severe | 8 | 38 | 97.7 | 91.2 | 0% | 53% | 92% | 0% |

## Track record (yearly-refit backtest, no look-ahead)

Mean absolute error in percentile points, 2010 onward. "Persistence" is the forecast that nothing changes.

| Weeks ahead | Weeks tested | Persistence error | Model error | Improvement | Direction right | Direction right when confident | Weeks that rose 5+ | Weeks that fell 5+ |
|---|---|---|---|---|---|---|---|---|
| 1.0 | 879.0 | 6.21 | 6.14 | +1% | 58% | 67% | 19% | 24% |
| 2.0 | 878.0 | 9.47 | 9.25 | +2% | 60% | 70% | 27% | 32% |
| 4.0 | 876.0 | 13.54 | 12.95 | +4% | 65% | 76% | 33% | 37% |
| 8.0 | 872.0 | 19.66 | 17.85 | +9% | 68% | 76% | 41% | 41% |

How to read this: the index is persistent, so the best one- or two-week forecast is close to the current reading. The model's edge grows with the horizon because it knows two things persistence doesn't: readings far above normal ease back, and anxiety driven by shocks fades faster than anxiety driven by background pressure. "Confident" means the quarter of weeks where the model expected the largest moves.

The model is half-weight ridge regression on the current level, recent momentum, and the six dimension readings with their four-week changes; it is refit every year on data up to that year. Forecasts are stored in `ai_index.forecasts` so they can be scored against what actually happened.

## Forecasts issued so far, scored

| Weeks ahead | Forecasts scored | Model error | Persistence error | Inside 80% range |
|---|---|---|---|---|
| 1 | 2 | 8.3 | 3.0 | 50% |
| 2 | 1 | 8.2 | 5.9 | 100% |

Most recent scored forecasts:

| Issued for week | Weeks ahead | Target week | Forecast | Actual | Error |
|---|---|---|---|---|---|
| 2026-10-24 | 1 | 2026-10-31 | 58 | 69 | -11.0 |
| 2026-10-24 | 2 | 2026-11-07 | 58 | 66 | -8.2 |
| 2026-10-31 | 1 | 2026-11-07 | 60 | 66 | -5.6 |
