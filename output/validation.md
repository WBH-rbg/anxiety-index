# Validation report

Generated 2026-11-13. Methodology v0.1 prototype.

## 1. Face validity

Does the index read tense when everyone remembers tension, and calm when they remember calm?

| Period | Expected | Mean | Max | Weeks ≥80 | Weeks | Verdict |
|---|---|---|---|---|---|---|
| 9/11 and aftermath | tense | 86.8 | 99.9 | 8 | 11 | pass |
| Iraq invasion | tense | 87.5 | 94.0 | 6 | 7 | pass |
| Mid-2000s calm | calm | 21.7 | 69.1 | 0 | 131 | pass |
| Financial crisis | tense | 86.4 | 99.8 | 20 | 29 | pass |
| Debt-ceiling summer | tense | 70.0 | 83.1 | 1 | 7 | pass |
| 2013-2015 calm | calm | 19.9 | 76.7 | 0 | 156 | pass |
| COVID onset | tense | 81.8 | 88.1 | 6 | 8 | pass |
| Summer 2020 | tense | 98.0 | 100.0 | 7 | 7 | pass |
| Jan 6 week | tense | 86.1 | 90.6 | 2 | 3 | pass |
| Ukraine invasion | tense | 98.3 | 99.1 | 5 | 5 | pass |
| Inflation peak | tense | 97.1 | 99.4 | 6 | 6 | pass |
| Spring 2025 tariffs | tense | 96.1 | 98.8 | 4 | 4 | pass |

## 2. External series

Correlation of the weekly headline with series that should track public anxiety but are not inputs to the headline (detrended with a 52-week rolling median). 'lead+k' means the index this week vs. the series k weeks later.

| Series | Weeks | Level | Detrended | lead−4 | lead−2 | lead−1 | lead+1 | lead+2 | lead+4 |
|---|---|---|---|---|---|---|---|---|---|
| Wikipedia views: Anxiety | 593 | -0.264 | -0.309 | -0.306 | -0.306 | -0.306 | -0.318 | -0.318 | -0.309 |
| Wikipedia views: Anxiety disorder | 593 | -0.377 | -0.274 | -0.24 | -0.263 | -0.267 | -0.275 | -0.269 | -0.243 |
| Wikipedia views: Panic attack | 593 | -0.297 | -0.165 | -0.144 | -0.158 | -0.158 | -0.178 | -0.187 | -0.189 |
| News share: boycotts | 610 | -0.14 | -0.078 | -0.061 | -0.059 | -0.071 | -0.072 | -0.093 | -0.075 |
| Average tone of all US news (sign flipped) | 610 | 0.026 | 0.146 | 0.08 | 0.117 | 0.146 | 0.043 | -0.002 | -0.059 |
| Share of US event coverage: conflict | 1349 | -0.016 | 0.134 | 0.038 | 0.083 | 0.114 | 0.091 | 0.07 | 0.048 |
| Hostile acts toward businesses, share of US event coverage | 1349 | 0.037 | -0.052 | -0.044 | -0.045 | -0.046 | -0.043 | -0.036 | -0.041 |
| Hostile share of business-related coverage | 1349 | -0.082 | 0.013 | 0.008 | 0.019 | 0.021 | 0.001 | 0.01 | 0.006 |

## 3. Corporate backlash events (curated outcome log)

119 dated backlash episodes since 2015-03-17. The reading a planner would have seen the week before an episode averaged **59.1**, against **58.5** for all weeks in the same span.

By severity (1 = brief viral moment, 5 = sustained national controversy):

| Severity | Episodes | Mean reading the week before |
|---|---|---|
| 1 | 2 | 24.1 |
| 2 | 39 | 54.0 |
| 3 | 44 | 66.4 |
| 4 | 23 | 58.6 |
| 5 | 11 | 55.9 |

Episodes in the following two weeks, per 100 weeks, by the band shown that week:

| Band | Weeks | Any episode | Severity ≥3 |
|---|---|---|---|
| Low | 57 | 28.1 | 21.1 |
| Moderate | 170 | 44.1 | 27.6 |
| Elevated | 218 | 41.3 | 34.4 |
| High | 125 | 51.2 | 38.4 |
| Severe | 38 | 42.1 | 34.2 |

Same test split by era (the log is denser after 2023, and those years were tenser, so each era is checked on its own):

| Era | Reading | Weeks | Severity ≥3 episodes in next two weeks, per 100 weeks |
|---|---|---|---|
| 2015-2023 | Low/Moderate | 169 | 20.1 |
| 2015-2023 | Elevated | 154 | 27.3 |
| 2015-2023 | High/Severe | 136 | 39.7 |
| 2024-2026 | Low/Moderate | 58 | 43.1 |
| 2024-2026 | Elevated | 64 | 51.6 |
| 2024-2026 | High/Severe | 27 | 25.9 |

Dimension readings the week before episodes vs. all weeks:

| Dimension | Before episodes | All weeks | Difference |
|---|---|---|---|
| Jobs and financial security | 65.5 | 59.1 | +6.4 |
| Political and institutional | 62.5 | 56.5 | +6.0 |
| Cost of living | 62.2 | 60.3 | +1.9 |
| Disasters, climate and health | 54.4 | 51.5 | +2.9 |
| Geopolitical | 51.3 | 53.8 | -2.5 |
| Public safety and unrest | 47.0 | 46.3 | +0.7 |

Does the hot dimension predict the *kind* of episode? Each trigger type is paired with the dimension it should feed on; the table compares that dimension's reading the week before episodes of that type with its reading before other types and in all weeks, and how often it was the hottest dimension.

| Trigger type | Dimension | Episodes | Dim. before this type | Before other types | All weeks | Hottest dim. before this type | Before other types |
|---|---|---|---|---|---|---|---|
| political_stance | Political and institutional | 35 | 67.9 | 60.3 | 56.5 | 17% | 17% |
| executive_statement | Political and institutional | 11 | 62.9 | 62.5 | 56.5 | 18% | 17% |
| pricing | Cost of living | 9 | 60.5 | 62.4 | 60.3 | 22% | 20% |
| labor_layoffs | Jobs and financial security | 9 | 62.9 | 65.7 | 59.1 | 33% | 25% |
| product_safety | Disasters, climate and health | 13 | 55.0 | 54.4 | 51.5 | 15% | 12% |
| service_incident | Disasters, climate and health | 8 | 39.8 | 55.5 | 51.5 | 0% | 14% |
| data_privacy | Political and institutional | 6 | 60.6 | 62.7 | 56.5 | 17% | 17% |
| marketing_misstep | Public safety and unrest | 16 | 35.8 | 48.7 | 46.3 | 6% | 11% |

Caveats: the log is curated and incomplete, episodes cluster in recent years when the log is richer, and the index was not tuned to this log. A clean result here is encouraging, not proof; a null result means the structure needs work.
