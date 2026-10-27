# Outlook from the week ending 2026-10-24

Current reading: **60 (Elevated)**. The table shows where a small statistical model expects the headline to be, with ranges taken from the model's own historical errors. Treat it as tendency, not prediction: at these horizons the model beats "no change" only modestly (see the track record below), and scheduled catalysts in `lookahead.md` can override any of it.

| Weeks ahead | Week ending | Expected | 50% range | 80% range | Chance up 5+ | Chance down 5+ | Chance High or Severe | Chance below 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-31 | 60 (Elevated) | 56–63 | 51–71 | 18% | 23% | 4% | 9% |
| 2 | 2026-11-07 | 60 (Elevated) | 53–66 | 45–76 | 27% | 33% | 6% | 18% |
| 4 | 2026-11-21 | 59 (Elevated) | 49–69 | 39–81 | 33% | 40% | 11% | 28% |
| 8 | 2026-12-19 | 58 (Elevated) | 43–73 | 28–86 | 40% | 43% | 16% | 34% |

## Why (four-week horizon)

Expected change in points, by what is driving it:

- Where the reading sits relative to normal, and its recent momentum: **-2.4**
- How much of it is shock-driven (safety, geopolitics, disasters), which fades faster: **-0.4**
- How much of it is background pressure (cost of living, jobs, politics), which persists: **+1.7**

Largest single factors: the quarter's move (-2.2); distance from the 13-week average (+1.5); geopolitical reading (-0.9); the headline level (-0.8).

## What has usually happened from here

Weeks since 2010 that showed the same band, and where the headline was afterwards:

| Band now | Weeks ahead | Weeks | Average then | Average later | Higher by 5+ | Lower by 5+ | High or Severe later | Below 50 later |
|---|---|---|---|---|---|---|---|---|
| Low | 2 | 155 | 10.3 | 18.2 | 37% | 11% | 1% | 92% |
| Moderate | 2 | 250 | 35.7 | 36.2 | 38% | 41% | 1% | 79% |
| **Elevated** | 2 | 288 | 64.7 | 61.1 | 22% | 43% | 10% | 22% |
| High | 2 | 146 | 87.4 | 85.6 | 13% | 28% | 79% | 0% |
| Severe | 2 | 37 | 97.6 | 95.3 | 0% | 16% | 100% | 0% |
| Low | 4 | 155 | 10.3 | 22.9 | 52% | 12% | 0% | 86% |
| Moderate | 4 | 250 | 35.7 | 37.7 | 42% | 42% | 3% | 72% |
| **Elevated** | 4 | 286 | 64.7 | 59.1 | 28% | 47% | 16% | 30% |
| High | 4 | 146 | 87.4 | 82.7 | 14% | 47% | 64% | 1% |
| Severe | 4 | 37 | 97.6 | 92.8 | 0% | 41% | 95% | 0% |
| Low | 8 | 154 | 10.3 | 32.9 | 71% | 8% | 0% | 74% |
| Moderate | 8 | 247 | 35.8 | 39.1 | 48% | 40% | 7% | 65% |
| **Elevated** | 8 | 286 | 64.7 | 56.5 | 35% | 49% | 22% | 40% |
| High | 8 | 146 | 87.4 | 74.8 | 19% | 64% | 49% | 10% |
| Severe | 8 | 37 | 97.6 | 90.0 | 0% | 57% | 92% | 0% |

## Track record (yearly-refit backtest, no look-ahead)

Mean absolute error in percentile points, 2010 onward. "Persistence" is the forecast that nothing changes.

| Weeks ahead | Weeks tested | Persistence error | Model error | Improvement | Direction right | Direction right when confident | Weeks that rose 5+ | Weeks that fell 5+ |
|---|---|---|---|---|---|---|---|---|
| 1.0 | 877.0 | 6.33 | 6.26 | +1% | 59% | 64% | 18% | 24% |
| 2.0 | 876.0 | 9.72 | 9.51 | +2% | 59% | 66% | 27% | 34% |
| 4.0 | 874.0 | 13.91 | 13.31 | +4% | 63% | 74% | 33% | 40% |
| 8.0 | 870.0 | 20.12 | 18.3 | +9% | 67% | 78% | 41% | 42% |

How to read this: the index is persistent, so the best one- or two-week forecast is close to the current reading. The model's edge grows with the horizon because it knows two things persistence doesn't: readings far above normal ease back, and anxiety driven by shocks fades faster than anxiety driven by background pressure. "Confident" means the quarter of weeks where the model expected the largest moves.

The model is half-weight ridge regression on the current level, recent momentum, and the six dimension readings with their four-week changes; it is refit every year on data up to that year. Forecasts are stored in `ai_index.forecasts` so they can be scored against what actually happened.

## Forecasts issued so far, scored

The first forecasts were issued on October 26, 2026; the first can be scored a week later. This section fills in as weeks arrive.
