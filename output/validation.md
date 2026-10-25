# Validation report

Generated 2026-10-25. Methodology v0.1 prototype.

## 1. Face validity

Does the index read tense when everyone remembers tension, and calm when they remember calm?

| Period | Expected | Mean | Max | Weeks ≥80 | Weeks | Verdict |
|---|---|---|---|---|---|---|
| 9/11 and aftermath | tense | 79.9 | 97.7 | 8 | 11 | pass |
| Iraq invasion | tense | 81.5 | 85.7 | 5 | 7 | pass |
| Mid-2000s calm | calm | 21.8 | 68.8 | 0 | 131 | pass |
| Financial crisis | tense | 88.3 | 98.3 | 23 | 29 | pass |
| Debt-ceiling summer | tense | 70.5 | 82.3 | 2 | 7 | pass |
| 2013-2015 calm | calm | 19.2 | 70.7 | 0 | 156 | pass |
| COVID onset | tense | 80.3 | 89.6 | 6 | 8 | pass |
| Summer 2020 | tense | 96.3 | 98.7 | 7 | 7 | pass |
| Jan 6 week | tense | 70.1 | 80.8 | 1 | 3 | pass |
| Ukraine invasion | tense | 99.3 | 99.8 | 5 | 5 | pass |
| Inflation peak | tense | 96.0 | 98.5 | 6 | 6 | pass |
| Spring 2025 tariffs | tense | 97.8 | 98.1 | 4 | 4 | pass |

## 2. External series

Correlation of the weekly headline with series that should track public anxiety but are not inputs to the headline (detrended with a 52-week rolling median). 'lead+k' means the index this week vs. the series k weeks later.

| Series | Weeks | Level | Detrended | lead−4 | lead−2 | lead−1 | lead+1 | lead+2 | lead+4 |
|---|---|---|---|---|---|---|---|---|---|
| Wikipedia views: Anxiety | 591 | -0.332 | -0.295 | -0.291 | -0.291 | -0.285 | -0.31 | -0.316 | -0.316 |
| Wikipedia views: Anxiety disorder | 591 | -0.428 | -0.199 | -0.162 | -0.19 | -0.186 | -0.211 | -0.208 | -0.198 |
| Wikipedia views: Panic attack | 591 | -0.362 | -0.149 | -0.125 | -0.135 | -0.133 | -0.164 | -0.175 | -0.182 |
| News share: boycotts | 608 | -0.121 | -0.022 | -0.025 | -0.027 | -0.031 | -0.034 | -0.047 | -0.042 |
| Average tone of all US news (sign flipped) | 608 | -0.136 | 0.101 | 0.114 | 0.159 | 0.166 | 0.044 | 0.02 | -0.036 |
| Share of US event coverage: conflict | 1400 | -0.07 | 0.071 | 0.036 | 0.08 | 0.105 | 0.052 | 0.046 | 0.037 |

## 3. Corporate backlash events (curated outcome log)

119 dated backlash episodes since 2015-03-17. The reading a planner would have seen the week before an episode averaged **61.8**, against **59.0** for all weeks in the same span.

By severity (1 = brief viral moment, 5 = sustained national controversy):

| Severity | Episodes | Mean reading the week before |
|---|---|---|
| 1 | 2 | 16.0 |
| 2 | 39 | 57.0 |
| 3 | 44 | 69.6 |
| 4 | 23 | 60.9 |
| 5 | 11 | 57.9 |

Episodes in the following two weeks, per 100 weeks, by the band shown that week:

| Band | Weeks | Any episode | Severity ≥3 |
|---|---|---|---|
| Low | 61 | 34.4 | 23.0 |
| Moderate | 159 | 41.5 | 25.2 |
| Elevated | 208 | 41.8 | 36.5 |
| High | 139 | 46.0 | 33.8 |
| Severe | 39 | 59.0 | 46.2 |

Dimension readings the week before episodes vs. all weeks:

| Dimension | Before episodes | All weeks | Difference |
|---|---|---|---|
| Political and institutional | 65.3 | 57.2 | +8.1 |
| Jobs and financial security | 62.7 | 57.7 | +5.0 |
| Cost of living | 62.2 | 60.0 | +2.2 |
| Disasters, climate and health | 53.3 | 50.1 | +3.2 |
| Geopolitical | 50.4 | 53.6 | -3.2 |
| Public safety and unrest | 46.4 | 44.5 | +1.9 |

Caveats: the log is curated and incomplete, episodes cluster in recent years when the log is richer, and the index was not tuned to this log. A clean result here is encouraging, not proof; a null result means the structure needs work.
