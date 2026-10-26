# Outlook from the week ending 2026-10-24

Current reading: **58 (Elevated)**. The table shows where a small statistical model expects the headline to be, with ranges taken from the model's own historical errors. Treat it as tendency, not prediction: at these horizons the model beats "no change" only modestly (see the track record below), and scheduled catalysts in `lookahead.md` can override any of it.

| Weeks ahead | Week ending | Expected | 50% range | 80% range | Chance up 5+ | Chance down 5+ | Chance High or Severe | Chance below 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-31 | 57 (Elevated) | 53–61 | 47–68 | 20% | 25% | 4% | 16% |
| 2 | 2026-11-07 | 57 (Elevated) | 50–63 | 42–73 | 27% | 33% | 5% | 25% |
| 4 | 2026-11-21 | 56 (Elevated) | 46–67 | 35–78 | 34% | 39% | 9% | 33% |
| 8 | 2026-12-19 | 54 (Elevated) | 41–71 | 25–83 | 39% | 43% | 13% | 38% |

## Why (four-week horizon)

Expected change in points, by what is driving it:

- Where the reading sits relative to normal, and its recent momentum: **-2.7**
- How much of it is shock-driven (safety, geopolitics, disasters), which fades faster: **-0.1**
- How much of it is background pressure (cost of living, jobs, politics), which persists: **+1.4**

Largest single factors: the quarter's move (-2.1); the hottest dimension (-0.7); distance from the 13-week average (+0.7); cost of living reading (+0.7).

## What has usually happened from here

Weeks since 2010 that showed the same band, and where the headline was afterwards:

| Band now | Weeks ahead | Weeks | Average then | Average later | Higher by 5+ | Lower by 5+ | High or Severe later | Below 50 later |
|---|---|---|---|---|---|---|---|---|
| Low | 2 | 150 | 10.0 | 18.1 | 40% | 10% | 0% | 92% |
| Moderate | 2 | 251 | 35.5 | 35.9 | 39% | 41% | 0% | 79% |
| **Elevated** | 2 | 288 | 65.0 | 62.0 | 23% | 40% | 12% | 22% |
| High | 2 | 143 | 86.9 | 84.4 | 12% | 29% | 76% | 1% |
| Severe | 2 | 44 | 97.5 | 94.7 | 0% | 25% | 98% | 0% |
| Low | 4 | 150 | 10.0 | 22.9 | 55% | 14% | 0% | 86% |
| Moderate | 4 | 251 | 35.5 | 37.3 | 40% | 39% | 2% | 73% |
| **Elevated** | 4 | 286 | 65.0 | 60.3 | 29% | 42% | 18% | 29% |
| High | 4 | 143 | 86.9 | 81.7 | 19% | 45% | 66% | 3% |
| Severe | 4 | 44 | 97.5 | 90.6 | 0% | 52% | 86% | 0% |
| Low | 8 | 148 | 9.9 | 31.3 | 70% | 9% | 1% | 76% |
| Moderate | 8 | 249 | 35.5 | 39.9 | 50% | 39% | 6% | 63% |
| **Elevated** | 8 | 286 | 65.0 | 57.7 | 37% | 47% | 23% | 38% |
| High | 8 | 143 | 86.9 | 75.0 | 19% | 58% | 49% | 10% |
| Severe | 8 | 44 | 97.5 | 83.1 | 0% | 64% | 82% | 7% |

## Track record (yearly-refit backtest, no look-ahead)

Mean absolute error in percentile points, 2010 onward. "Persistence" is the forecast that nothing changes.

| Weeks ahead | Weeks tested | Persistence error | Model error | Improvement | Direction right | Direction right when confident | Weeks that rose 5+ | Weeks that fell 5+ |
|---|---|---|---|---|---|---|---|---|
| 1.0 | 877.0 | 6.71 | 6.63 | +1% | 57% | 65% | 20% | 25% |
| 2.0 | 876.0 | 9.86 | 9.68 | +2% | 60% | 68% | 28% | 33% |
| 4.0 | 874.0 | 13.88 | 13.26 | +4% | 63% | 76% | 34% | 38% |
| 8.0 | 870.0 | 19.91 | 18.12 | +9% | 68% | 76% | 41% | 41% |

How to read this: the index is persistent, so the best one- or two-week forecast is close to the current reading. The model's edge grows with the horizon because it knows two things persistence doesn't: readings far above normal ease back, and anxiety driven by shocks fades faster than anxiety driven by background pressure. "Confident" means the quarter of weeks where the model expected the largest moves.

The model is half-weight ridge regression on the current level, recent momentum, and the six dimension readings with their four-week changes; it is refit every year on data up to that year. Forecasts are stored in `ai_index.forecasts` so they can be scored against what actually happened.

## Forecasts issued so far, scored

The first forecasts were issued on October 26, 2026; the first can be scored a week later. This section fills in as weeks arrive.
