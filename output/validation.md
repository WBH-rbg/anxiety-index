# Validation report

Generated 2026-10-26. Methodology v0.1 prototype.

## 1. Face validity

Does the index read tense when everyone remembers tension, and calm when they remember calm?

| Period | Expected | Mean | Max | Weeks ≥80 | Weeks | Verdict |
|---|---|---|---|---|---|---|
| 9/11 and aftermath | tense | 82.0 | 99.5 | 8 | 11 | pass |
| Iraq invasion | tense | 85.5 | 93.6 | 5 | 7 | pass |
| Mid-2000s calm | calm | 22.4 | 69.3 | 0 | 131 | pass |
| Financial crisis | tense | 89.9 | 99.5 | 24 | 29 | pass |
| Debt-ceiling summer | tense | 72.9 | 85.6 | 4 | 7 | pass |
| 2013-2015 calm | calm | 19.2 | 72.6 | 0 | 156 | pass |
| COVID onset | tense | 82.6 | 92.8 | 6 | 8 | pass |
| Summer 2020 | tense | 98.5 | 100.0 | 7 | 7 | pass |
| Jan 6 week | tense | 68.3 | 77.2 | 0 | 3 | check |
| Ukraine invasion | tense | 97.8 | 99.0 | 5 | 5 | pass |
| Inflation peak | tense | 95.5 | 98.9 | 6 | 6 | pass |
| Spring 2025 tariffs | tense | 99.0 | 99.4 | 4 | 4 | pass |

## 2. External series

Correlation of the weekly headline with series that should track public anxiety but are not inputs to the headline (detrended with a 52-week rolling median). 'lead+k' means the index this week vs. the series k weeks later.

| Series | Weeks | Level | Detrended | lead−4 | lead−2 | lead−1 | lead+1 | lead+2 | lead+4 |
|---|---|---|---|---|---|---|---|---|---|
| Wikipedia views: Anxiety | 591 | -0.332 | -0.306 | -0.304 | -0.301 | -0.295 | -0.317 | -0.319 | -0.313 |
| Wikipedia views: Anxiety disorder | 591 | -0.427 | -0.222 | -0.191 | -0.216 | -0.211 | -0.232 | -0.227 | -0.212 |
| Wikipedia views: Panic attack | 591 | -0.356 | -0.148 | -0.123 | -0.134 | -0.133 | -0.162 | -0.173 | -0.18 |
| News share: boycotts | 608 | -0.12 | -0.018 | -0.026 | -0.021 | -0.027 | -0.036 | -0.05 | -0.049 |
| Average tone of all US news (sign flipped) | 608 | -0.113 | 0.109 | 0.121 | 0.166 | 0.171 | 0.053 | 0.025 | -0.029 |
| Share of US event coverage: conflict | 1400 | -0.071 | 0.071 | 0.034 | 0.077 | 0.101 | 0.054 | 0.049 | 0.035 |

## 3. Corporate backlash events (curated outcome log)

119 dated backlash episodes since 2015-03-17. The reading a planner would have seen the week before an episode averaged **61.0**, against **58.5** for all weeks in the same span.

By severity (1 = brief viral moment, 5 = sustained national controversy):

| Severity | Episodes | Mean reading the week before |
|---|---|---|
| 1 | 2 | 17.8 |
| 2 | 39 | 55.5 |
| 3 | 44 | 69.2 |
| 4 | 23 | 59.9 |
| 5 | 11 | 57.9 |

Episodes in the following two weeks, per 100 weeks, by the band shown that week:

| Band | Weeks | Any episode | Severity ≥3 |
|---|---|---|---|
| Low | 67 | 34.3 | 20.9 |
| Moderate | 160 | 43.1 | 27.5 |
| Elevated | 214 | 39.3 | 34.6 |
| High | 123 | 48.8 | 35.0 |
| Severe | 42 | 59.5 | 47.6 |

Same test split by era (the log is denser after 2023, and those years were tenser, so each era is checked on its own):

| Era | Reading | Weeks | Severity ≥3 episodes in next two weeks, per 100 weeks |
|---|---|---|---|
| 2015-2023 | Low/Moderate | 181 | 21.0 |
| 2015-2023 | Elevated | 149 | 26.2 |
| 2015-2023 | High/Severe | 129 | 41.1 |
| 2024-2026 | Low/Moderate | 46 | 43.5 |
| 2024-2026 | Elevated | 65 | 53.8 |
| 2024-2026 | High/Severe | 36 | 27.8 |

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
