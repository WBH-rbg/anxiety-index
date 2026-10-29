# Outlook from the week ending 2026-10-24

Current reading: **61 (Elevated)**. The table shows where a small statistical model expects the headline to be, with ranges taken from the model's own historical errors. Treat it as tendency, not prediction: at these horizons the model beats "no change" only modestly (see the track record below), and scheduled catalysts in `lookahead.md` can override any of it.

| Weeks ahead | Week ending | Expected | 50% range | 80% range | Chance up 5+ | Chance down 5+ | Chance High or Severe | Chance below 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-31 | 61 (Elevated) | 56–64 | 52–72 | 19% | 24% | 4% | 7% |
| 2 | 2026-11-07 | 61 (Elevated) | 54–67 | 46–76 | 27% | 33% | 8% | 14% |
| 4 | 2026-11-21 | 60 (Elevated) | 50–70 | 40–83 | 33% | 40% | 13% | 26% |
| 8 | 2026-12-19 | 59 (Elevated) | 44–74 | 29–87 | 40% | 43% | 17% | 32% |

## Why (four-week horizon)

Expected change in points, by what is driving it:

- Where the reading sits relative to normal, and its recent momentum: **-2.5**
- How much of it is shock-driven (safety, geopolitics, disasters), which fades faster: **-0.4**
- How much of it is background pressure (cost of living, jobs, politics), which persists: **+1.9**

Largest single factors: the quarter's move (-2.3); distance from the 13-week average (+1.6); political and institutional reading (+1.0); geopolitical reading (-0.9).

## What has usually happened from here

Weeks since 2010 that showed the same band, and where the headline was afterwards:

| Band now | Weeks ahead | Weeks | Average then | Average later | Higher by 5+ | Lower by 5+ | High or Severe later | Below 50 later |
|---|---|---|---|---|---|---|---|---|
| Low | 2 | 154 | 10.3 | 18.2 | 36% | 11% | 1% | 92% |
| Moderate | 2 | 252 | 35.7 | 36.4 | 38% | 40% | 1% | 79% |
| **Elevated** | 2 | 287 | 64.7 | 61.0 | 21% | 43% | 10% | 22% |
| High | 2 | 146 | 87.4 | 85.8 | 12% | 25% | 80% | 0% |
| Severe | 2 | 37 | 97.6 | 95.0 | 0% | 19% | 97% | 0% |
| Low | 4 | 154 | 10.3 | 23.1 | 52% | 13% | 0% | 86% |
| Moderate | 4 | 252 | 35.7 | 37.7 | 42% | 42% | 4% | 73% |
| **Elevated** | 4 | 285 | 64.8 | 59.1 | 28% | 48% | 16% | 30% |
| High | 4 | 146 | 87.4 | 82.9 | 15% | 47% | 65% | 1% |
| Severe | 4 | 37 | 97.6 | 92.5 | 0% | 41% | 92% | 0% |
| Low | 8 | 153 | 10.3 | 33.3 | 72% | 8% | 0% | 73% |
| Moderate | 8 | 249 | 35.8 | 39.0 | 47% | 40% | 7% | 65% |
| **Elevated** | 8 | 285 | 64.8 | 56.4 | 35% | 49% | 21% | 41% |
| High | 8 | 146 | 87.4 | 74.8 | 19% | 66% | 49% | 10% |
| Severe | 8 | 37 | 97.6 | 90.5 | 0% | 51% | 92% | 0% |

## Track record (yearly-refit backtest, no look-ahead)

Mean absolute error in percentile points, 2010 onward. "Persistence" is the forecast that nothing changes.

| Weeks ahead | Weeks tested | Persistence error | Model error | Improvement | Direction right | Direction right when confident | Weeks that rose 5+ | Weeks that fell 5+ |
|---|---|---|---|---|---|---|---|---|
| 1.0 | 877.0 | 6.34 | 6.26 | +1% | 59% | 65% | 19% | 24% |
| 2.0 | 876.0 | 9.7 | 9.48 | +2% | 59% | 68% | 26% | 33% |
| 4.0 | 874.0 | 13.9 | 13.28 | +4% | 63% | 76% | 33% | 40% |
| 8.0 | 870.0 | 20.09 | 18.27 | +9% | 67% | 77% | 41% | 43% |

How to read this: the index is persistent, so the best one- or two-week forecast is close to the current reading. The model's edge grows with the horizon because it knows two things persistence doesn't: readings far above normal ease back, and anxiety driven by shocks fades faster than anxiety driven by background pressure. "Confident" means the quarter of weeks where the model expected the largest moves.

The model is half-weight ridge regression on the current level, recent momentum, and the six dimension readings with their four-week changes; it is refit every year on data up to that year. Forecasts are stored in `ai_index.forecasts` so they can be scored against what actually happened.

## Forecasts issued so far, scored

The first forecasts were issued on October 26, 2026; the first can be scored a week later. This section fills in as weeks arrive.
