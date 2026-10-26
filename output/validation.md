# Validation report

Generated 2026-10-26. Methodology v0.1 prototype.

## 1. Face validity

Does the index read tense when everyone remembers tension, and calm when they remember calm?

| Period | Expected | Mean | Max | Weeks ≥80 | Weeks | Verdict |
|---|---|---|---|---|---|---|
| 9/11 and aftermath | tense | 82.0 | 99.8 | 8 | 11 | pass |
| Iraq invasion | tense | 85.4 | 93.5 | 5 | 7 | pass |
| Mid-2000s calm | calm | 22.6 | 68.2 | 0 | 131 | pass |
| Financial crisis | tense | 89.0 | 99.6 | 22 | 29 | pass |
| Debt-ceiling summer | tense | 76.3 | 91.1 | 4 | 7 | pass |
| 2013-2015 calm | calm | 19.5 | 72.5 | 0 | 156 | pass |
| COVID onset | tense | 75.2 | 85.7 | 4 | 8 | pass |
| Summer 2020 | tense | 97.0 | 100.0 | 7 | 7 | pass |
| Jan 6 week | tense | 76.7 | 86.3 | 2 | 3 | pass |
| Ukraine invasion | tense | 97.7 | 98.5 | 5 | 5 | pass |
| Inflation peak | tense | 94.9 | 98.6 | 6 | 6 | pass |
| Spring 2025 tariffs | tense | 99.3 | 99.5 | 4 | 4 | pass |

## 2. External series

Correlation of the weekly headline with series that should track public anxiety but are not inputs to the headline (detrended with a 52-week rolling median). 'lead+k' means the index this week vs. the series k weeks later.

| Series | Weeks | Level | Detrended | lead−4 | lead−2 | lead−1 | lead+1 | lead+2 | lead+4 |
|---|---|---|---|---|---|---|---|---|---|
| Wikipedia views: Anxiety | 591 | -0.337 | -0.299 | -0.299 | -0.297 | -0.29 | -0.309 | -0.311 | -0.308 |
| Wikipedia views: Anxiety disorder | 591 | -0.429 | -0.205 | -0.177 | -0.201 | -0.194 | -0.214 | -0.208 | -0.194 |
| Wikipedia views: Panic attack | 591 | -0.355 | -0.142 | -0.121 | -0.129 | -0.127 | -0.156 | -0.168 | -0.178 |
| News share: boycotts | 608 | -0.106 | -0.002 | -0.011 | -0.008 | -0.016 | -0.019 | -0.032 | -0.033 |
| Average tone of all US news (sign flipped) | 608 | -0.127 | 0.114 | 0.125 | 0.174 | 0.18 | 0.06 | 0.034 | -0.027 |
| Share of US event coverage: conflict | 1400 | -0.069 | 0.079 | 0.039 | 0.085 | 0.109 | 0.061 | 0.056 | 0.039 |

## 3. Corporate backlash events (curated outcome log)

119 dated backlash episodes since 2015-03-17. The reading a planner would have seen the week before an episode averaged **61.7**, against **58.5** for all weeks in the same span.

By severity (1 = brief viral moment, 5 = sustained national controversy):

| Severity | Episodes | Mean reading the week before |
|---|---|---|
| 1 | 2 | 17.6 |
| 2 | 39 | 56.5 |
| 3 | 44 | 69.6 |
| 4 | 23 | 60.6 |
| 5 | 11 | 59.2 |

Episodes in the following two weeks, per 100 weeks, by the band shown that week:

| Band | Weeks | Any episode | Severity ≥3 |
|---|---|---|---|
| Low | 67 | 32.8 | 20.9 |
| Moderate | 160 | 43.8 | 28.1 |
| Elevated | 213 | 39.0 | 34.3 |
| High | 125 | 48.0 | 35.2 |
| Severe | 41 | 63.4 | 46.3 |

Same test split by era (the log is denser after 2023, and those years were tenser, so each era is checked on its own):

| Era | Reading | Weeks | Severity ≥3 episodes in next two weeks, per 100 weeks |
|---|---|---|---|
| 2015-2023 | Low/Moderate | 181 | 21.5 |
| 2015-2023 | Elevated | 153 | 26.8 |
| 2015-2023 | High/Severe | 125 | 40.0 |
| 2024-2026 | Low/Moderate | 46 | 43.5 |
| 2024-2026 | Elevated | 60 | 53.3 |
| 2024-2026 | High/Severe | 41 | 31.7 |

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
