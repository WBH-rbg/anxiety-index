# Validation report

Generated 2026-10-30. Methodology v0.1 prototype.

## 1. Face validity

Does the index read tense when everyone remembers tension, and calm when they remember calm?

| Period | Expected | Mean | Max | Weeks ≥80 | Weeks | Verdict |
|---|---|---|---|---|---|---|
| 9/11 and aftermath | tense | 86.8 | 99.9 | 8 | 11 | pass |
| Iraq invasion | tense | 87.4 | 94.0 | 6 | 7 | pass |
| Mid-2000s calm | calm | 21.7 | 69.1 | 0 | 131 | pass |
| Financial crisis | tense | 86.4 | 99.8 | 20 | 29 | pass |
| Debt-ceiling summer | tense | 70.1 | 83.1 | 1 | 7 | pass |
| 2013-2015 calm | calm | 19.9 | 76.7 | 0 | 156 | pass |
| COVID onset | tense | 81.9 | 88.0 | 6 | 8 | pass |
| Summer 2020 | tense | 98.1 | 100.0 | 7 | 7 | pass |
| Jan 6 week | tense | 86.0 | 90.5 | 2 | 3 | pass |
| Ukraine invasion | tense | 98.3 | 99.1 | 5 | 5 | pass |
| Inflation peak | tense | 97.1 | 99.4 | 6 | 6 | pass |
| Spring 2025 tariffs | tense | 95.5 | 98.5 | 4 | 4 | pass |

## 2. External series

Correlation of the weekly headline with series that should track public anxiety but are not inputs to the headline (detrended with a 52-week rolling median). 'lead+k' means the index this week vs. the series k weeks later.

| Series | Weeks | Level | Detrended | lead−4 | lead−2 | lead−1 | lead+1 | lead+2 | lead+4 |
|---|---|---|---|---|---|---|---|---|---|
| Wikipedia views: Anxiety | 591 | -0.25 | -0.302 | -0.297 | -0.3 | -0.3 | -0.311 | -0.312 | -0.304 |
| Wikipedia views: Anxiety disorder | 591 | -0.366 | -0.272 | -0.238 | -0.262 | -0.266 | -0.272 | -0.267 | -0.241 |
| Wikipedia views: Panic attack | 591 | -0.286 | -0.162 | -0.14 | -0.155 | -0.155 | -0.175 | -0.184 | -0.187 |
| News share: boycotts | 608 | -0.137 | -0.077 | -0.056 | -0.056 | -0.067 | -0.072 | -0.092 | -0.074 |
| Average tone of all US news (sign flipped) | 608 | 0.03 | 0.144 | 0.08 | 0.115 | 0.144 | 0.042 | -0.003 | -0.06 |
| Share of US event coverage: conflict | 1347 | -0.015 | 0.135 | 0.04 | 0.083 | 0.115 | 0.092 | 0.071 | 0.05 |
| Hostile acts toward businesses, share of US event coverage | 1347 | 0.039 | -0.05 | -0.044 | -0.045 | -0.044 | -0.041 | -0.034 | -0.04 |
| Hostile share of business-related coverage | 1347 | -0.081 | 0.014 | 0.009 | 0.019 | 0.022 | 0.002 | 0.011 | 0.007 |

## 3. Corporate backlash events (curated outcome log)

119 dated backlash episodes since 2015-03-17. The reading a planner would have seen the week before an episode averaged **58.9**, against **58.4** for all weeks in the same span.

By severity (1 = brief viral moment, 5 = sustained national controversy):

| Severity | Episodes | Mean reading the week before |
|---|---|---|
| 1 | 2 | 21.4 |
| 2 | 39 | 53.6 |
| 3 | 44 | 66.2 |
| 4 | 23 | 58.7 |
| 5 | 11 | 56.0 |

Episodes in the following two weeks, per 100 weeks, by the band shown that week:

| Band | Weeks | Any episode | Severity ≥3 |
|---|---|---|---|
| Low | 59 | 30.5 | 23.7 |
| Moderate | 168 | 42.9 | 26.2 |
| Elevated | 216 | 42.6 | 35.2 |
| High | 125 | 50.4 | 38.4 |
| Severe | 38 | 42.1 | 34.2 |

Same test split by era (the log is denser after 2023, and those years were tenser, so each era is checked on its own):

| Era | Reading | Weeks | Severity ≥3 episodes in next two weeks, per 100 weeks |
|---|---|---|---|
| 2015-2023 | Low/Moderate | 169 | 19.5 |
| 2015-2023 | Elevated | 153 | 28.1 |
| 2015-2023 | High/Severe | 137 | 39.4 |
| 2024-2026 | Low/Moderate | 58 | 43.1 |
| 2024-2026 | Elevated | 63 | 52.4 |
| 2024-2026 | High/Severe | 26 | 26.9 |

Dimension readings the week before episodes vs. all weeks:

| Dimension | Before episodes | All weeks | Difference |
|---|---|---|---|
| Jobs and financial security | 65.5 | 59.1 | +6.4 |
| Political and institutional | 62.9 | 56.5 | +6.4 |
| Cost of living | 62.2 | 60.2 | +2.0 |
| Disasters, climate and health | 53.9 | 51.0 | +2.9 |
| Geopolitical | 51.3 | 53.7 | -2.4 |
| Public safety and unrest | 47.0 | 46.4 | +0.6 |

Does the hot dimension predict the *kind* of episode? Each trigger type is paired with the dimension it should feed on; the table compares that dimension's reading the week before episodes of that type with its reading before other types and in all weeks, and how often it was the hottest dimension.

| Trigger type | Dimension | Episodes | Dim. before this type | Before other types | All weeks | Hottest dim. before this type | Before other types |
|---|---|---|---|---|---|---|---|
| political_stance | Political and institutional | 35 | 68.0 | 60.8 | 56.5 | 17% | 17% |
| executive_statement | Political and institutional | 11 | 63.1 | 62.9 | 56.5 | 18% | 17% |
| pricing | Cost of living | 9 | 60.5 | 62.4 | 60.2 | 22% | 21% |
| labor_layoffs | Jobs and financial security | 9 | 62.9 | 65.7 | 59.1 | 33% | 25% |
| product_safety | Disasters, climate and health | 13 | 55.0 | 53.8 | 51.0 | 15% | 9% |
| service_incident | Disasters, climate and health | 8 | 39.8 | 54.9 | 51.0 | 0% | 11% |
| data_privacy | Political and institutional | 6 | 60.3 | 63.0 | 56.5 | 17% | 17% |
| marketing_misstep | Public safety and unrest | 16 | 35.8 | 48.7 | 46.4 | 6% | 11% |

Caveats: the log is curated and incomplete, episodes cluster in recent years when the log is richer, and the index was not tuned to this log. A clean result here is encouraging, not proof; a null result means the structure needs work.
