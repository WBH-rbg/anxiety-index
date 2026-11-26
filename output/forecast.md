# Outlook from the week ending 2026-11-21

Current reading: **41 (Moderate)**. The table shows where a small statistical model expects the headline to be, with ranges taken from the model's own historical errors. Treat it as tendency, not prediction: at these horizons the model beats "no change" only modestly (see the track record below), and scheduled catalysts in `lookahead.md` can override any of it.

| Weeks ahead | Week ending | Expected | 50% range | 80% range | Chance up 5+ | Chance down 5+ | Chance High or Severe | Chance below 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-11-28 | 42 (Moderate) | 38–45 | 33–52 | 21% | 19% | 1% | 88% |
| 2 | 2026-12-05 | 43 (Moderate) | 36–49 | 29–58 | 34% | 24% | 2% | 77% |
| 4 | 2026-12-19 | 44 (Moderate) | 34–54 | 24–66 | 43% | 30% | 3% | 67% |
| 8 | 2027-01-16 | 45 (Moderate) | 32–61 | 16–73 | 50% | 32% | 6% | 56% |

## Why (four-week horizon)

Expected change in points, by what is driving it:

- Where the reading sits relative to normal, and its recent momentum: **+0.8**
- How much of it is shock-driven (safety, geopolitics, disasters), which fades faster: **+1.0**
- How much of it is background pressure (cost of living, jobs, politics), which persists: **+0.9**

Largest single factors: public safety and unrest reading (+2.1); political and institutional reading (+0.7); geopolitical reading (-0.7); cost of living reading (+0.6).

## What has usually happened from here

Weeks since 2010 that showed the same band, and where the headline was afterwards:

| Band now | Weeks ahead | Weeks | Average then | Average later | Higher by 5+ | Lower by 5+ | High or Severe later | Below 50 later |
|---|---|---|---|---|---|---|---|---|
| Low | 2 | 142 | 9.9 | 17.1 | 36% | 13% | 1% | 93% |
| **Moderate** | 2 | 258 | 35.8 | 37.2 | 37% | 36% | 0% | 78% |
| Elevated | 2 | 296 | 64.6 | 60.9 | 23% | 42% | 9% | 23% |
| High | 2 | 146 | 87.6 | 85.8 | 12% | 29% | 82% | 0% |
| Severe | 2 | 38 | 97.7 | 96.1 | 0% | 11% | 100% | 0% |
| Low | 4 | 142 | 9.9 | 21.7 | 51% | 11% | 0% | 88% |
| **Moderate** | 4 | 258 | 35.8 | 39.2 | 45% | 36% | 2% | 68% |
| Elevated | 4 | 294 | 64.7 | 58.6 | 26% | 48% | 15% | 33% |
| High | 4 | 146 | 87.6 | 83.2 | 16% | 43% | 69% | 1% |
| Severe | 4 | 38 | 97.7 | 93.5 | 0% | 29% | 92% | 0% |
| Low | 8 | 142 | 9.9 | 31.1 | 67% | 11% | 0% | 75% |
| **Moderate** | 8 | 258 | 35.8 | 41.0 | 54% | 34% | 4% | 59% |
| Elevated | 8 | 290 | 64.7 | 55.8 | 31% | 53% | 21% | 42% |
| High | 8 | 146 | 87.6 | 76.9 | 22% | 55% | 55% | 12% |
| Severe | 8 | 38 | 97.7 | 91.1 | 0% | 53% | 92% | 0% |

## Track record (yearly-refit backtest, no look-ahead)

Mean absolute error in percentile points, 2010 onward. "Persistence" is the forecast that nothing changes.

| Weeks ahead | Weeks tested | Persistence error | Model error | Improvement | Direction right | Direction right when confident | Weeks that rose 5+ | Weeks that fell 5+ |
|---|---|---|---|---|---|---|---|---|
| 1.0 | 881.0 | 6.21 | 6.13 | +1% | 58% | 66% | 19% | 25% |
| 2.0 | 880.0 | 9.44 | 9.22 | +2% | 60% | 70% | 26% | 32% |
| 4.0 | 878.0 | 13.49 | 12.91 | +4% | 65% | 76% | 33% | 37% |
| 8.0 | 874.0 | 19.51 | 17.74 | +9% | 68% | 75% | 41% | 41% |

How to read this: the index is persistent, so the best one- or two-week forecast is close to the current reading. The model's edge grows with the horizon because it knows two things persistence doesn't: readings far above normal ease back, and anxiety driven by shocks fades faster than anxiety driven by background pressure. "Confident" means the quarter of weeks where the model expected the largest moves.

The model is half-weight ridge regression on the current level, recent momentum, and the six dimension readings with their four-week changes; it is refit every year on data up to that year. Forecasts are stored in `ai_index.forecasts` so they can be scored against what actually happened.

## Forecasts issued so far, scored

| Weeks ahead | Forecasts scored | Model error | Persistence error | Inside 80% range |
|---|---|---|---|---|
| 1 | 4 | 7.0 | 6.2 | 75% |
| 2 | 3 | 10.0 | 11.3 | 67% |
| 4 | 1 | 15.9 | 24.6 | 100% |

Most recent scored forecasts:

| Issued for week | Weeks ahead | Target week | Forecast | Actual | Error |
|---|---|---|---|---|---|
| 2026-10-24 | 1 | 2026-10-31 | 58 | 62 | -4.2 |
| 2026-10-24 | 2 | 2026-11-07 | 58 | 60 | -2.2 |
| 2026-10-24 | 4 | 2026-11-21 | 57 | 41 | +15.9 |
| 2026-10-31 | 1 | 2026-11-07 | 60 | 60 | +0.4 |
| 2026-10-31 | 2 | 2026-11-14 | 60 | 53 | +7.0 |
| 2026-11-07 | 1 | 2026-11-14 | 62 | 53 | +8.2 |
| 2026-11-07 | 2 | 2026-11-21 | 62 | 41 | +20.9 |
| 2026-11-14 | 1 | 2026-11-21 | 56 | 41 | +15.0 |
