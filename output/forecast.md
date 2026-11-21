# Outlook from the week ending 2026-11-21

Current reading: **41 (Moderate)**. The table shows where a small statistical model expects the headline to be, with ranges taken from the model's own historical errors. Treat it as tendency, not prediction: at these horizons the model beats "no change" only modestly (see the track record below), and scheduled catalysts in `lookahead.md` can override any of it.

| Weeks ahead | Week ending | Expected | 50% range | 80% range | Chance up 5+ | Chance down 5+ | Chance High or Severe | Chance below 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-11-28 | 42 (Moderate) | 38–45 | 33–52 | 22% | 19% | 1% | 88% |
| 2 | 2026-12-05 | 43 (Moderate) | 37–49 | 29–58 | 35% | 25% | 1% | 77% |
| 4 | 2026-12-19 | 44 (Moderate) | 34–54 | 24–66 | 43% | 30% | 3% | 66% |
| 8 | 2027-01-16 | 45 (Moderate) | 32–61 | 16–73 | 50% | 32% | 6% | 56% |

## Why (four-week horizon)

Expected change in points, by what is driving it:

- Where the reading sits relative to normal, and its recent momentum: **+1.0**
- How much of it is shock-driven (safety, geopolitics, disasters), which fades faster: **+0.8**
- How much of it is background pressure (cost of living, jobs, politics), which persists: **+1.0**

Largest single factors: public safety and unrest reading (+1.9); political and institutional reading (+0.8); geopolitical reading (-0.7); the hottest dimension (+0.6).

## What has usually happened from here

Weeks since 2010 that showed the same band, and where the headline was afterwards:

| Band now | Weeks ahead | Weeks | Average then | Average later | Higher by 5+ | Lower by 5+ | High or Severe later | Below 50 later |
|---|---|---|---|---|---|---|---|---|
| Low | 2 | 142 | 9.9 | 17.1 | 36% | 13% | 1% | 93% |
| **Moderate** | 2 | 258 | 35.8 | 37.4 | 38% | 35% | 1% | 77% |
| Elevated | 2 | 296 | 64.7 | 60.8 | 22% | 41% | 8% | 23% |
| High | 2 | 146 | 87.6 | 85.8 | 11% | 29% | 82% | 0% |
| Severe | 2 | 38 | 97.7 | 96.1 | 0% | 11% | 100% | 0% |
| Low | 4 | 142 | 9.9 | 21.7 | 51% | 11% | 0% | 88% |
| **Moderate** | 4 | 258 | 35.8 | 39.4 | 45% | 36% | 2% | 68% |
| Elevated | 4 | 294 | 64.7 | 58.5 | 26% | 48% | 15% | 33% |
| High | 4 | 146 | 87.6 | 83.3 | 16% | 43% | 69% | 1% |
| Severe | 4 | 38 | 97.7 | 93.5 | 0% | 32% | 92% | 0% |
| Low | 8 | 142 | 9.9 | 31.1 | 67% | 11% | 0% | 75% |
| **Moderate** | 8 | 258 | 35.8 | 41.1 | 54% | 34% | 4% | 59% |
| Elevated | 8 | 290 | 64.7 | 55.7 | 31% | 53% | 21% | 42% |
| High | 8 | 146 | 87.6 | 76.9 | 21% | 55% | 55% | 12% |
| Severe | 8 | 38 | 97.7 | 91.2 | 0% | 50% | 92% | 0% |

## Track record (yearly-refit backtest, no look-ahead)

Mean absolute error in percentile points, 2010 onward. "Persistence" is the forecast that nothing changes.

| Weeks ahead | Weeks tested | Persistence error | Model error | Improvement | Direction right | Direction right when confident | Weeks that rose 5+ | Weeks that fell 5+ |
|---|---|---|---|---|---|---|---|---|
| 1.0 | 881.0 | 6.22 | 6.14 | +1% | 58% | 67% | 19% | 25% |
| 2.0 | 880.0 | 9.44 | 9.22 | +2% | 60% | 70% | 26% | 32% |
| 4.0 | 878.0 | 13.49 | 12.91 | +4% | 65% | 76% | 33% | 37% |
| 8.0 | 874.0 | 19.52 | 17.76 | +9% | 68% | 75% | 41% | 41% |

How to read this: the index is persistent, so the best one- or two-week forecast is close to the current reading. The model's edge grows with the horizon because it knows two things persistence doesn't: readings far above normal ease back, and anxiety driven by shocks fades faster than anxiety driven by background pressure. "Confident" means the quarter of weeks where the model expected the largest moves.

The model is half-weight ridge regression on the current level, recent momentum, and the six dimension readings with their four-week changes; it is refit every year on data up to that year. Forecasts are stored in `ai_index.forecasts` so they can be scored against what actually happened.

## Forecasts issued so far, scored

| Weeks ahead | Forecasts scored | Model error | Persistence error | Inside 80% range |
|---|---|---|---|---|
| 1 | 4 | 7.4 | 6.8 | 75% |
| 2 | 3 | 10.2 | 12.1 | 67% |
| 4 | 1 | 15.8 | 27.3 | 100% |

Most recent scored forecasts:

| Issued for week | Weeks ahead | Target week | Forecast | Actual | Error |
|---|---|---|---|---|---|
| 2026-10-24 | 1 | 2026-10-31 | 58 | 65 | -6.5 |
| 2026-10-24 | 2 | 2026-11-07 | 58 | 63 | -5.1 |
| 2026-10-24 | 4 | 2026-11-21 | 57 | 41 | +15.8 |
| 2026-10-31 | 1 | 2026-11-07 | 60 | 63 | -2.5 |
| 2026-10-31 | 2 | 2026-11-14 | 60 | 56 | +4.6 |
| 2026-11-07 | 1 | 2026-11-14 | 62 | 56 | +5.8 |
| 2026-11-07 | 2 | 2026-11-21 | 62 | 41 | +20.8 |
| 2026-11-14 | 1 | 2026-11-21 | 56 | 41 | +14.9 |
