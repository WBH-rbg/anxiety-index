# Outlook from the week ending 2026-10-24

Current reading: **59 (Elevated)**. The table shows where a small statistical model expects the headline to be, with ranges taken from the model's own historical errors. Treat it as tendency, not prediction: at these horizons the model beats "no change" only modestly (see the track record below), and scheduled catalysts in `lookahead.md` can override any of it.

| Weeks ahead | Week ending | Expected | 50% range | 80% range | Chance up 5+ | Chance down 5+ | Chance High or Severe | Chance below 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-31 | 58 (Elevated) | 54–62 | 48–69 | 20% | 24% | 3% | 13% |
| 2 | 2026-11-07 | 58 (Elevated) | 51–64 | 43–73 | 25% | 32% | 5% | 22% |
| 4 | 2026-11-21 | 57 (Elevated) | 48–67 | 36–79 | 32% | 40% | 9% | 29% |
| 8 | 2026-12-19 | 55 (Elevated) | 40–72 | 26–83 | 38% | 44% | 14% | 38% |

## Why (four-week horizon)

Expected change in points, by what is driving it:

- Where the reading sits relative to normal, and its recent momentum: **-3.4**
- How much of it is shock-driven (safety, geopolitics, disasters), which fades faster: **+0.5**
- How much of it is background pressure (cost of living, jobs, politics), which persists: **+1.4**

Largest single factors: the quarter's move (-1.9); the headline level (-0.8); cost of living reading (+0.8); the hottest dimension (-0.7).

## What has usually happened from here

Weeks since 2010 that showed the same band, and where the headline was afterwards:

| Band now | Weeks ahead | Weeks | Average then | Average later | Higher by 5+ | Lower by 5+ | High or Severe later | Below 50 later |
|---|---|---|---|---|---|---|---|---|
| Low | 2 | 155 | 10.2 | 17.9 | 41% | 12% | 1% | 95% |
| Moderate | 2 | 247 | 35.6 | 36.1 | 36% | 36% | 0% | 78% |
| **Elevated** | 2 | 290 | 65.1 | 61.9 | 20% | 39% | 12% | 21% |
| High | 2 | 141 | 87.1 | 84.8 | 10% | 26% | 75% | 0% |
| Severe | 2 | 43 | 97.6 | 95.3 | 0% | 16% | 98% | 0% |
| Low | 4 | 155 | 10.2 | 23.5 | 54% | 13% | 1% | 86% |
| Moderate | 4 | 247 | 35.6 | 36.9 | 38% | 39% | 2% | 75% |
| **Elevated** | 4 | 288 | 65.1 | 60.2 | 31% | 44% | 18% | 27% |
| High | 4 | 141 | 87.1 | 82.3 | 20% | 48% | 65% | 3% |
| Severe | 4 | 43 | 97.6 | 90.6 | 0% | 47% | 84% | 0% |
| Low | 8 | 153 | 10.2 | 31.4 | 69% | 8% | 1% | 77% |
| Moderate | 8 | 245 | 35.6 | 40.3 | 49% | 41% | 6% | 62% |
| **Elevated** | 8 | 288 | 65.1 | 56.7 | 35% | 48% | 21% | 40% |
| High | 8 | 141 | 87.1 | 76.3 | 19% | 60% | 51% | 9% |
| Severe | 8 | 43 | 97.6 | 83.2 | 0% | 60% | 81% | 9% |

## Track record (yearly-refit backtest, no look-ahead)

Mean absolute error in percentile points, 2010 onward. "Persistence" is the forecast that nothing changes.

| Weeks ahead | Weeks tested | Persistence error | Model error | Improvement | Direction right | Direction right when confident | Weeks that rose 5+ | Weeks that fell 5+ |
|---|---|---|---|---|---|---|---|---|
| 1.0 | 877.0 | 6.48 | 6.41 | +1% | 57% | 60% | 20% | 23% |
| 2.0 | 876.0 | 9.49 | 9.32 | +2% | 57% | 65% | 26% | 31% |
| 4.0 | 874.0 | 13.79 | 13.28 | +4% | 61% | 69% | 34% | 38% |
| 8.0 | 870.0 | 20.04 | 18.31 | +9% | 68% | 73% | 41% | 42% |

How to read this: the index is persistent, so the best one- or two-week forecast is close to the current reading. The model's edge grows with the horizon because it knows two things persistence doesn't: readings far above normal ease back, and anxiety driven by shocks fades faster than anxiety driven by background pressure. "Confident" means the quarter of weeks where the model expected the largest moves.

The model is half-weight ridge regression on the current level, recent momentum, and the six dimension readings with their four-week changes; it is refit every year on data up to that year. Forecasts are stored in `ai_index.forecasts` so they can be scored against what actually happened.
