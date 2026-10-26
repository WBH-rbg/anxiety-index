# Outlook from the week ending 2026-10-24

Current reading: **57 (Elevated)**. The table shows where a small statistical model expects the headline to be, with ranges taken from the model's own historical errors. Treat it as tendency, not prediction: at these horizons the model beats "no change" only modestly (see the track record below), and scheduled catalysts in `lookahead.md` can override any of it.

| Weeks ahead | Week ending | Expected | 50% range | 80% range | Chance up 5+ | Chance down 5+ | Chance High or Severe | Chance below 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-31 | 57 (Elevated) | 53–60 | 48–68 | 19% | 24% | 3% | 16% |
| 2 | 2026-11-07 | 57 (Elevated) | 50–63 | 42–73 | 27% | 33% | 5% | 26% |
| 4 | 2026-11-21 | 56 (Elevated) | 46–66 | 36–79 | 33% | 40% | 9% | 34% |
| 8 | 2026-12-19 | 54 (Elevated) | 40–71 | 25–84 | 40% | 44% | 14% | 40% |

## Why (four-week horizon)

Expected change in points, by what is driving it:

- Where the reading sits relative to normal, and its recent momentum: **-1.9**
- How much of it is shock-driven (safety, geopolitics, disasters), which fades faster: **-0.3**
- How much of it is background pressure (cost of living, jobs, politics), which persists: **+1.3**

Largest single factors: the quarter's move (-2.1); distance from the 13-week average (+1.4); geopolitical reading (-0.9); the hottest dimension (-0.6).

## What has usually happened from here

Weeks since 2010 that showed the same band, and where the headline was afterwards:

| Band now | Weeks ahead | Weeks | Average then | Average later | Higher by 5+ | Lower by 5+ | High or Severe later | Below 50 later |
|---|---|---|---|---|---|---|---|---|
| Low | 2 | 154 | 10.3 | 18.4 | 36% | 10% | 0% | 91% |
| Moderate | 2 | 253 | 35.7 | 36.0 | 39% | 41% | 1% | 80% |
| **Elevated** | 2 | 287 | 64.9 | 61.4 | 22% | 44% | 10% | 22% |
| High | 2 | 142 | 87.3 | 85.5 | 11% | 25% | 79% | 0% |
| Severe | 2 | 40 | 97.5 | 95.1 | 0% | 20% | 100% | 0% |
| Low | 4 | 154 | 10.3 | 23.2 | 53% | 12% | 0% | 86% |
| Moderate | 4 | 253 | 35.7 | 37.3 | 42% | 43% | 3% | 74% |
| **Elevated** | 4 | 285 | 64.9 | 59.5 | 26% | 47% | 17% | 31% |
| High | 4 | 142 | 87.3 | 82.8 | 12% | 44% | 63% | 0% |
| Severe | 4 | 40 | 97.5 | 92.5 | 0% | 42% | 95% | 0% |
| Low | 8 | 153 | 10.3 | 33.0 | 71% | 8% | 1% | 74% |
| Moderate | 8 | 250 | 35.8 | 39.2 | 49% | 42% | 6% | 64% |
| **Elevated** | 8 | 285 | 64.9 | 56.4 | 34% | 51% | 22% | 41% |
| High | 8 | 142 | 87.3 | 74.9 | 18% | 63% | 47% | 10% |
| Severe | 8 | 40 | 97.5 | 89.4 | 0% | 57% | 90% | 0% |

## Track record (yearly-refit backtest, no look-ahead)

Mean absolute error in percentile points, 2010 onward. "Persistence" is the forecast that nothing changes.

| Weeks ahead | Weeks tested | Persistence error | Model error | Improvement | Direction right | Direction right when confident | Weeks that rose 5+ | Weeks that fell 5+ |
|---|---|---|---|---|---|---|---|---|
| 1.0 | 877.0 | 6.39 | 6.33 | +1% | 57% | 63% | 19% | 25% |
| 2.0 | 876.0 | 9.75 | 9.53 | +2% | 58% | 70% | 27% | 33% |
| 4.0 | 874.0 | 13.92 | 13.33 | +4% | 63% | 75% | 32% | 40% |
| 8.0 | 870.0 | 20.29 | 18.47 | +9% | 67% | 78% | 41% | 43% |

How to read this: the index is persistent, so the best one- or two-week forecast is close to the current reading. The model's edge grows with the horizon because it knows two things persistence doesn't: readings far above normal ease back, and anxiety driven by shocks fades faster than anxiety driven by background pressure. "Confident" means the quarter of weeks where the model expected the largest moves.

The model is half-weight ridge regression on the current level, recent momentum, and the six dimension readings with their four-week changes; it is refit every year on data up to that year. Forecasts are stored in `ai_index.forecasts` so they can be scored against what actually happened.

## Forecasts issued so far, scored

The first forecasts were issued on October 26, 2026; the first can be scored a week later. This section fills in as weeks arrive.
