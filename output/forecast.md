# Outlook from the week ending 2026-10-24

Current reading: **58 (Elevated)**. The table shows where a small statistical model expects the headline to be, with ranges taken from the model's own historical errors. Treat it as tendency, not prediction: at these horizons the model beats "no change" only modestly (see the track record below), and scheduled catalysts in `lookahead.md` can override any of it.

| Weeks ahead | Week ending | Expected | 50% range | 80% range | Chance up 5+ | Chance down 5+ | Chance High or Severe | Chance below 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-31 | 58 (Elevated) | 53–61 | 48–69 | 19% | 22% | 3% | 15% |
| 2 | 2026-11-07 | 58 (Elevated) | 50–64 | 43–74 | 28% | 32% | 6% | 24% |
| 4 | 2026-11-21 | 57 (Elevated) | 47–67 | 36–80 | 34% | 39% | 10% | 32% |
| 8 | 2026-12-19 | 56 (Elevated) | 41–72 | 26–85 | 40% | 43% | 15% | 38% |

## Why (four-week horizon)

Expected change in points, by what is driving it:

- Where the reading sits relative to normal, and its recent momentum: **-2.1**
- How much of it is shock-driven (safety, geopolitics, disasters), which fades faster: **-0.2**
- How much of it is background pressure (cost of living, jobs, politics), which persists: **+1.6**

Largest single factors: the quarter's move (-2.3); distance from the 13-week average (+1.4); geopolitical reading (-0.8); political and institutional reading (+0.7).

## What has usually happened from here

Weeks since 2010 that showed the same band, and where the headline was afterwards:

| Band now | Weeks ahead | Weeks | Average then | Average later | Higher by 5+ | Lower by 5+ | High or Severe later | Below 50 later |
|---|---|---|---|---|---|---|---|---|
| Low | 2 | 153 | 10.4 | 18.7 | 38% | 10% | 0% | 91% |
| Moderate | 2 | 253 | 35.8 | 35.6 | 40% | 42% | 0% | 81% |
| **Elevated** | 2 | 286 | 64.7 | 61.7 | 22% | 42% | 10% | 21% |
| High | 2 | 147 | 87.3 | 85.5 | 13% | 27% | 80% | 0% |
| Severe | 2 | 37 | 97.6 | 94.9 | 0% | 19% | 97% | 0% |
| Low | 4 | 153 | 10.4 | 22.6 | 53% | 13% | 0% | 89% |
| Moderate | 4 | 253 | 35.8 | 37.3 | 42% | 42% | 2% | 72% |
| **Elevated** | 4 | 284 | 64.8 | 60.0 | 29% | 46% | 18% | 30% |
| High | 4 | 147 | 87.3 | 82.3 | 15% | 46% | 63% | 1% |
| Severe | 4 | 37 | 97.6 | 92.9 | 0% | 41% | 97% | 0% |
| Low | 8 | 152 | 10.4 | 32.8 | 70% | 9% | 1% | 74% |
| Moderate | 8 | 250 | 35.8 | 38.7 | 48% | 42% | 5% | 65% |
| **Elevated** | 8 | 284 | 64.8 | 57.2 | 35% | 51% | 24% | 40% |
| High | 8 | 147 | 87.3 | 74.8 | 18% | 61% | 48% | 11% |
| Severe | 8 | 37 | 97.6 | 89.5 | 0% | 57% | 92% | 0% |

## Track record (yearly-refit backtest, no look-ahead)

Mean absolute error in percentile points, 2010 onward. "Persistence" is the forecast that nothing changes.

| Weeks ahead | Weeks tested | Persistence error | Model error | Improvement | Direction right | Direction right when confident | Weeks that rose 5+ | Weeks that fell 5+ |
|---|---|---|---|---|---|---|---|---|
| 1.0 | 877.0 | 6.4 | 6.35 | +1% | 57% | 61% | 19% | 25% |
| 2.0 | 876.0 | 9.76 | 9.54 | +2% | 58% | 69% | 28% | 33% |
| 4.0 | 874.0 | 13.8 | 13.22 | +4% | 63% | 75% | 33% | 39% |
| 8.0 | 870.0 | 20.03 | 18.24 | +9% | 67% | 75% | 41% | 43% |

How to read this: the index is persistent, so the best one- or two-week forecast is close to the current reading. The model's edge grows with the horizon because it knows two things persistence doesn't: readings far above normal ease back, and anxiety driven by shocks fades faster than anxiety driven by background pressure. "Confident" means the quarter of weeks where the model expected the largest moves.

The model is half-weight ridge regression on the current level, recent momentum, and the six dimension readings with their four-week changes; it is refit every year on data up to that year. Forecasts are stored in `ai_index.forecasts` so they can be scored against what actually happened.

## Forecasts issued so far, scored

The first forecasts were issued on October 26, 2026; the first can be scored a week later. This section fills in as weeks arrive.
