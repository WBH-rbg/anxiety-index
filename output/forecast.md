# Outlook from the week ending 2026-10-24

Current reading: **58 (Elevated)**. The table shows where a small statistical model expects the headline to be, with ranges taken from the model's own historical errors. Treat it as tendency, not prediction: at these horizons the model beats "no change" only modestly (see the track record below), and scheduled catalysts in `lookahead.md` can override any of it.

| Weeks ahead | Week ending | Expected | 50% range | 80% range | Chance up 5+ | Chance down 5+ | Chance High or Severe | Chance below 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-31 | 58 (Elevated) | 54–61 | 49–69 | 18% | 23% | 3% | 13% |
| 2 | 2026-11-07 | 58 (Elevated) | 51–64 | 44–74 | 26% | 33% | 6% | 23% |
| 4 | 2026-11-21 | 57 (Elevated) | 47–68 | 38–80 | 33% | 40% | 10% | 31% |
| 8 | 2026-12-19 | 56 (Elevated) | 41–72 | 26–84 | 40% | 43% | 15% | 37% |

## Why (four-week horizon)

Expected change in points, by what is driving it:

- Where the reading sits relative to normal, and its recent momentum: **-2.2**
- How much of it is shock-driven (safety, geopolitics, disasters), which fades faster: **-0.4**
- How much of it is background pressure (cost of living, jobs, politics), which persists: **+1.6**

Largest single factors: the quarter's move (-2.2); distance from the 13-week average (+1.4); geopolitical reading (-0.9); the headline level (-0.7).

## What has usually happened from here

Weeks since 2010 that showed the same band, and where the headline was afterwards:

| Band now | Weeks ahead | Weeks | Average then | Average later | Higher by 5+ | Lower by 5+ | High or Severe later | Below 50 later |
|---|---|---|---|---|---|---|---|---|
| Low | 2 | 155 | 10.4 | 18.0 | 37% | 12% | 1% | 92% |
| Moderate | 2 | 252 | 35.8 | 36.5 | 39% | 41% | 1% | 79% |
| **Elevated** | 2 | 286 | 64.8 | 61.1 | 21% | 43% | 10% | 22% |
| High | 2 | 146 | 87.4 | 85.6 | 12% | 28% | 79% | 0% |
| Severe | 2 | 37 | 97.6 | 95.5 | 0% | 16% | 100% | 0% |
| Low | 4 | 155 | 10.4 | 22.9 | 52% | 12% | 0% | 86% |
| Moderate | 4 | 252 | 35.8 | 37.7 | 42% | 43% | 4% | 73% |
| **Elevated** | 4 | 284 | 64.8 | 59.3 | 28% | 47% | 16% | 30% |
| High | 4 | 146 | 87.4 | 82.7 | 14% | 47% | 64% | 1% |
| Severe | 4 | 37 | 97.6 | 92.7 | 0% | 41% | 95% | 0% |
| Low | 8 | 154 | 10.3 | 33.0 | 71% | 8% | 0% | 74% |
| Moderate | 8 | 249 | 35.9 | 39.2 | 48% | 41% | 7% | 65% |
| **Elevated** | 8 | 284 | 64.8 | 56.5 | 35% | 49% | 21% | 41% |
| High | 8 | 146 | 87.4 | 74.8 | 18% | 64% | 49% | 10% |
| Severe | 8 | 37 | 97.6 | 89.7 | 0% | 57% | 89% | 0% |

## Track record (yearly-refit backtest, no look-ahead)

Mean absolute error in percentile points, 2010 onward. "Persistence" is the forecast that nothing changes.

| Weeks ahead | Weeks tested | Persistence error | Model error | Improvement | Direction right | Direction right when confident | Weeks that rose 5+ | Weeks that fell 5+ |
|---|---|---|---|---|---|---|---|---|
| 1.0 | 877.0 | 6.34 | 6.27 | +1% | 58% | 63% | 18% | 24% |
| 2.0 | 876.0 | 9.72 | 9.51 | +2% | 58% | 66% | 27% | 34% |
| 4.0 | 874.0 | 13.91 | 13.3 | +4% | 63% | 74% | 33% | 40% |
| 8.0 | 870.0 | 20.16 | 18.32 | +9% | 68% | 78% | 41% | 42% |

How to read this: the index is persistent, so the best one- or two-week forecast is close to the current reading. The model's edge grows with the horizon because it knows two things persistence doesn't: readings far above normal ease back, and anxiety driven by shocks fades faster than anxiety driven by background pressure. "Confident" means the quarter of weeks where the model expected the largest moves.

The model is half-weight ridge regression on the current level, recent momentum, and the six dimension readings with their four-week changes; it is refit every year on data up to that year. Forecasts are stored in `ai_index.forecasts` so they can be scored against what actually happened.

## Forecasts issued so far, scored

The first forecasts were issued on October 26, 2026; the first can be scored a week later. This section fills in as weeks arrive.
