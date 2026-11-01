# Outlook from the week ending 2026-10-31

Current reading: **61 (Elevated)**. The table shows where a small statistical model expects the headline to be, with ranges taken from the model's own historical errors. Treat it as tendency, not prediction: at these horizons the model beats "no change" only modestly (see the track record below), and scheduled catalysts in `lookahead.md` can override any of it.

| Weeks ahead | Week ending | Expected | 50% range | 80% range | Chance up 5+ | Chance down 5+ | Chance High or Severe | Chance below 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-11-07 | 60 (Elevated) | 56–63 | 51–70 | 18% | 24% | 4% | 9% |
| 2 | 2026-11-14 | 60 (Elevated) | 54–66 | 45–76 | 27% | 31% | 6% | 17% |
| 4 | 2026-11-28 | 59 (Elevated) | 50–69 | 39–82 | 32% | 38% | 12% | 26% |
| 8 | 2026-12-26 | 58 (Elevated) | 44–74 | 28–86 | 39% | 43% | 17% | 33% |

## Why (four-week horizon)

Expected change in points, by what is driving it:

- Where the reading sits relative to normal, and its recent momentum: **-2.7**
- How much of it is shock-driven (safety, geopolitics, disasters), which fades faster: **-0.9**
- How much of it is background pressure (cost of living, jobs, politics), which persists: **+2.3**

Largest single factors: the quarter's move (-2.0); geopolitical reading (-1.0); political and institutional reading (+1.0); the headline level (-0.8).

## What has usually happened from here

Weeks since 2010 that showed the same band, and where the headline was afterwards:

| Band now | Weeks ahead | Weeks | Average then | Average later | Higher by 5+ | Lower by 5+ | High or Severe later | Below 50 later |
|---|---|---|---|---|---|---|---|---|
| Low | 2 | 145 | 10.0 | 17.2 | 37% | 12% | 1% | 93% |
| Moderate | 2 | 255 | 35.6 | 37.3 | 38% | 36% | 1% | 77% |
| **Elevated** | 2 | 294 | 64.7 | 60.7 | 22% | 40% | 9% | 23% |
| High | 2 | 145 | 87.6 | 85.9 | 12% | 30% | 81% | 0% |
| Severe | 2 | 38 | 97.7 | 96.1 | 0% | 11% | 100% | 0% |
| Low | 4 | 145 | 10.0 | 22.0 | 52% | 10% | 0% | 88% |
| Moderate | 4 | 255 | 35.6 | 39.0 | 44% | 36% | 2% | 67% |
| **Elevated** | 4 | 292 | 64.7 | 58.4 | 26% | 48% | 14% | 33% |
| High | 4 | 145 | 87.6 | 83.5 | 17% | 43% | 69% | 1% |
| Severe | 4 | 38 | 97.7 | 93.5 | 0% | 32% | 95% | 0% |
| Low | 8 | 145 | 10.0 | 31.7 | 68% | 10% | 0% | 74% |
| Moderate | 8 | 252 | 35.6 | 40.5 | 54% | 35% | 4% | 60% |
| **Elevated** | 8 | 291 | 64.7 | 55.6 | 31% | 54% | 20% | 42% |
| High | 8 | 145 | 87.6 | 76.9 | 21% | 56% | 55% | 11% |
| Severe | 8 | 38 | 97.7 | 91.1 | 0% | 53% | 92% | 0% |

## Track record (yearly-refit backtest, no look-ahead)

Mean absolute error in percentile points, 2010 onward. "Persistence" is the forecast that nothing changes.

| Weeks ahead | Weeks tested | Persistence error | Model error | Improvement | Direction right | Direction right when confident | Weeks that rose 5+ | Weeks that fell 5+ |
|---|---|---|---|---|---|---|---|---|
| 1.0 | 878.0 | 6.24 | 6.17 | +1% | 58% | 64% | 19% | 25% |
| 2.0 | 877.0 | 9.51 | 9.29 | +2% | 60% | 69% | 27% | 32% |
| 4.0 | 875.0 | 13.58 | 12.99 | +4% | 66% | 76% | 33% | 37% |
| 8.0 | 871.0 | 19.69 | 17.88 | +9% | 68% | 75% | 41% | 42% |

How to read this: the index is persistent, so the best one- or two-week forecast is close to the current reading. The model's edge grows with the horizon because it knows two things persistence doesn't: readings far above normal ease back, and anxiety driven by shocks fades faster than anxiety driven by background pressure. "Confident" means the quarter of weeks where the model expected the largest moves.

The model is half-weight ridge regression on the current level, recent momentum, and the six dimension readings with their four-week changes; it is refit every year on data up to that year. Forecasts are stored in `ai_index.forecasts` so they can be scored against what actually happened.

## Forecasts issued so far, scored

| Weeks ahead | Forecasts scored | Model error | Persistence error | Inside 80% range |
|---|---|---|---|---|
| 1 | 1 | 2.3 | 4.2 | 100% |

Most recent scored forecasts:

| Issued for week | Weeks ahead | Target week | Forecast | Actual | Error |
|---|---|---|---|---|---|
| 2026-10-24 | 1 | 2026-10-31 | 58 | 61 | -2.3 |
