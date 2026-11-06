# Outlook from the week ending 2026-10-31

Current reading: **62 (Elevated)**. The table shows where a small statistical model expects the headline to be, with ranges taken from the model's own historical errors. Treat it as tendency, not prediction: at these horizons the model beats "no change" only modestly (see the track record below), and scheduled catalysts in `lookahead.md` can override any of it.

| Weeks ahead | Week ending | Expected | 50% range | 80% range | Chance up 5+ | Chance down 5+ | Chance High or Severe | Chance below 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-11-07 | 62 (Elevated) | 58–65 | 52–72 | 18% | 23% | 4% | 6% |
| 2 | 2026-11-14 | 62 (Elevated) | 55–68 | 47–77 | 28% | 30% | 7% | 13% |
| 4 | 2026-11-28 | 61 (Elevated) | 51–71 | 41–84 | 34% | 38% | 13% | 22% |
| 8 | 2026-12-26 | 59 (Elevated) | 46–76 | 30–88 | 40% | 42% | 18% | 30% |

## Why (four-week horizon)

Expected change in points, by what is driving it:

- Where the reading sits relative to normal, and its recent momentum: **-2.9**
- How much of it is shock-driven (safety, geopolitics, disasters), which fades faster: **-0.4**
- How much of it is background pressure (cost of living, jobs, politics), which persists: **+2.5**

Largest single factors: the quarter's move (-2.0); geopolitical reading (-1.0); political and institutional reading (+1.0); the headline level (-0.9).

## What has usually happened from here

Weeks since 2010 that showed the same band, and where the headline was afterwards:

| Band now | Weeks ahead | Weeks | Average then | Average later | Higher by 5+ | Lower by 5+ | High or Severe later | Below 50 later |
|---|---|---|---|---|---|---|---|---|
| Low | 2 | 145 | 10.0 | 17.2 | 37% | 12% | 1% | 93% |
| Moderate | 2 | 255 | 35.6 | 37.0 | 38% | 36% | 0% | 77% |
| **Elevated** | 2 | 294 | 64.7 | 60.9 | 23% | 41% | 9% | 23% |
| High | 2 | 145 | 87.6 | 85.9 | 11% | 28% | 82% | 0% |
| Severe | 2 | 38 | 97.7 | 96.1 | 0% | 11% | 100% | 0% |
| Low | 4 | 145 | 10.0 | 22.0 | 52% | 10% | 0% | 88% |
| Moderate | 4 | 255 | 35.6 | 38.9 | 45% | 36% | 2% | 67% |
| **Elevated** | 4 | 292 | 64.7 | 58.4 | 26% | 48% | 14% | 33% |
| High | 4 | 145 | 87.6 | 83.5 | 16% | 43% | 69% | 1% |
| Severe | 4 | 38 | 97.7 | 93.5 | 0% | 29% | 95% | 0% |
| Low | 8 | 145 | 10.0 | 31.7 | 68% | 10% | 0% | 74% |
| Moderate | 8 | 252 | 35.6 | 40.4 | 54% | 35% | 4% | 60% |
| **Elevated** | 8 | 291 | 64.7 | 55.6 | 31% | 54% | 20% | 43% |
| High | 8 | 145 | 87.6 | 77.0 | 21% | 54% | 55% | 11% |
| Severe | 8 | 38 | 97.7 | 91.2 | 0% | 50% | 92% | 0% |

## Track record (yearly-refit backtest, no look-ahead)

Mean absolute error in percentile points, 2010 onward. "Persistence" is the forecast that nothing changes.

| Weeks ahead | Weeks tested | Persistence error | Model error | Improvement | Direction right | Direction right when confident | Weeks that rose 5+ | Weeks that fell 5+ |
|---|---|---|---|---|---|---|---|---|
| 1.0 | 878.0 | 6.21 | 6.14 | +1% | 58% | 66% | 19% | 25% |
| 2.0 | 877.0 | 9.45 | 9.25 | +2% | 60% | 69% | 26% | 32% |
| 4.0 | 875.0 | 13.56 | 12.99 | +4% | 65% | 75% | 33% | 37% |
| 8.0 | 871.0 | 19.69 | 17.88 | +9% | 68% | 76% | 41% | 41% |

How to read this: the index is persistent, so the best one- or two-week forecast is close to the current reading. The model's edge grows with the horizon because it knows two things persistence doesn't: readings far above normal ease back, and anxiety driven by shocks fades faster than anxiety driven by background pressure. "Confident" means the quarter of weeks where the model expected the largest moves.

The model is half-weight ridge regression on the current level, recent momentum, and the six dimension readings with their four-week changes; it is refit every year on data up to that year. Forecasts are stored in `ai_index.forecasts` so they can be scored against what actually happened.

## Forecasts issued so far, scored

| Weeks ahead | Forecasts scored | Model error | Persistence error | Inside 80% range |
|---|---|---|---|---|
| 1 | 1 | 3.7 | 2.7 | 100% |

Most recent scored forecasts:

| Issued for week | Weeks ahead | Target week | Forecast | Actual | Error |
|---|---|---|---|---|---|
| 2026-10-24 | 1 | 2026-10-31 | 58 | 62 | -3.7 |
