# Outlook from the week ending 2026-10-24

Current reading: **58 (Elevated)**. The table shows where a small statistical model expects the headline to be, with ranges taken from the model's own historical errors. Treat it as tendency, not prediction: at these horizons the model beats "no change" only modestly (see the track record below), and scheduled catalysts in `lookahead.md` can override any of it.

| Weeks ahead | Week ending | Expected | 50% range | 80% range | Chance up 5+ | Chance down 5+ | Chance High or Severe | Chance below 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-31 | 58 (Elevated) | 54–62 | 49–69 | 19% | 23% | 3% | 14% |
| 2 | 2026-11-07 | 58 (Elevated) | 51–64 | 43–74 | 28% | 32% | 6% | 23% |
| 4 | 2026-11-21 | 57 (Elevated) | 48–67 | 36–80 | 33% | 40% | 10% | 31% |
| 8 | 2026-12-19 | 56 (Elevated) | 42–72 | 26–85 | 41% | 43% | 16% | 37% |

## Why (four-week horizon)

Expected change in points, by what is driving it:

- Where the reading sits relative to normal, and its recent momentum: **-2.1**
- How much of it is shock-driven (safety, geopolitics, disasters), which fades faster: **-0.4**
- How much of it is background pressure (cost of living, jobs, politics), which persists: **+1.6**

Largest single factors: the quarter's move (-2.3); distance from the 13-week average (+1.4); geopolitical reading (-0.9); political and institutional reading (+0.7).

## What has usually happened from here

Weeks since 2010 that showed the same band, and where the headline was afterwards:

| Band now | Weeks ahead | Weeks | Average then | Average later | Higher by 5+ | Lower by 5+ | High or Severe later | Below 50 later |
|---|---|---|---|---|---|---|---|---|
| Low | 2 | 153 | 10.5 | 18.5 | 38% | 10% | 0% | 91% |
| Moderate | 2 | 251 | 35.7 | 35.8 | 39% | 41% | 1% | 80% |
| **Elevated** | 2 | 289 | 64.9 | 61.6 | 22% | 41% | 10% | 22% |
| High | 2 | 144 | 87.4 | 85.8 | 12% | 24% | 81% | 0% |
| Severe | 2 | 39 | 97.6 | 94.3 | 0% | 23% | 95% | 0% |
| Low | 4 | 153 | 10.5 | 22.7 | 52% | 12% | 0% | 88% |
| Moderate | 4 | 251 | 35.7 | 37.3 | 41% | 43% | 3% | 73% |
| **Elevated** | 4 | 287 | 64.9 | 60.0 | 26% | 46% | 17% | 29% |
| High | 4 | 144 | 87.4 | 82.6 | 13% | 45% | 63% | 1% |
| Severe | 4 | 39 | 97.6 | 92.2 | 0% | 44% | 95% | 0% |
| Low | 8 | 152 | 10.4 | 32.7 | 70% | 8% | 1% | 74% |
| Moderate | 8 | 248 | 35.7 | 39.0 | 49% | 41% | 6% | 64% |
| **Elevated** | 8 | 287 | 64.9 | 57.1 | 34% | 51% | 23% | 40% |
| High | 8 | 144 | 87.4 | 74.9 | 19% | 63% | 48% | 10% |
| Severe | 8 | 39 | 97.6 | 89.3 | 0% | 59% | 87% | 0% |

## Track record (yearly-refit backtest, no look-ahead)

Mean absolute error in percentile points, 2010 onward. "Persistence" is the forecast that nothing changes.

| Weeks ahead | Weeks tested | Persistence error | Model error | Improvement | Direction right | Direction right when confident | Weeks that rose 5+ | Weeks that fell 5+ |
|---|---|---|---|---|---|---|---|---|
| 1.0 | 877.0 | 6.38 | 6.32 | +1% | 57% | 61% | 19% | 25% |
| 2.0 | 876.0 | 9.76 | 9.52 | +2% | 59% | 70% | 28% | 33% |
| 4.0 | 874.0 | 13.83 | 13.23 | +4% | 64% | 75% | 32% | 39% |
| 8.0 | 870.0 | 20.19 | 18.34 | +9% | 68% | 76% | 41% | 43% |

How to read this: the index is persistent, so the best one- or two-week forecast is close to the current reading. The model's edge grows with the horizon because it knows two things persistence doesn't: readings far above normal ease back, and anxiety driven by shocks fades faster than anxiety driven by background pressure. "Confident" means the quarter of weeks where the model expected the largest moves.

The model is half-weight ridge regression on the current level, recent momentum, and the six dimension readings with their four-week changes; it is refit every year on data up to that year. Forecasts are stored in `ai_index.forecasts` so they can be scored against what actually happened.

## Forecasts issued so far, scored

The first forecasts were issued on October 26, 2026; the first can be scored a week later. This section fills in as weeks arrive.
