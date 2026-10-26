# Validation report

Generated 2026-10-26. Methodology v0.1 prototype.

## 1. Face validity

Does the index read tense when everyone remembers tension, and calm when they remember calm?

| Period | Expected | Mean | Max | Weeks ≥80 | Weeks | Verdict |
|---|---|---|---|---|---|---|
| 9/11 and aftermath | tense | 87.3 | 100.0 | 8 | 11 | pass |
| Iraq invasion | tense | 87.5 | 94.3 | 5 | 7 | pass |
| Mid-2000s calm | calm | 22.3 | 70.1 | 0 | 131 | pass |
| Financial crisis | tense | 86.7 | 100.0 | 20 | 29 | pass |
| Debt-ceiling summer | tense | 70.8 | 84.2 | 1 | 7 | pass |
| 2013-2015 calm | calm | 20.6 | 75.6 | 0 | 156 | pass |
| COVID onset | tense | 81.0 | 88.3 | 6 | 8 | pass |
| Summer 2020 | tense | 96.3 | 99.5 | 7 | 7 | pass |
| Jan 6 week | tense | 79.6 | 84.6 | 2 | 3 | pass |
| Ukraine invasion | tense | 98.4 | 99.1 | 5 | 5 | pass |
| Inflation peak | tense | 96.4 | 99.3 | 6 | 6 | pass |
| Spring 2025 tariffs | tense | 96.4 | 97.9 | 4 | 4 | pass |

## 2. External series

Correlation of the weekly headline with series that should track public anxiety but are not inputs to the headline (detrended with a 52-week rolling median). 'lead+k' means the index this week vs. the series k weeks later.

| Series | Weeks | Level | Detrended | lead−4 | lead−2 | lead−1 | lead+1 | lead+2 | lead+4 |
|---|---|---|---|---|---|---|---|---|---|
| Wikipedia views: Anxiety | 591 | -0.293 | -0.246 | -0.255 | -0.252 | -0.246 | -0.256 | -0.256 | -0.245 |
| Wikipedia views: Anxiety disorder | 591 | -0.385 | -0.135 | -0.117 | -0.139 | -0.133 | -0.14 | -0.136 | -0.117 |
| Wikipedia views: Panic attack | 591 | -0.315 | -0.122 | -0.101 | -0.114 | -0.113 | -0.137 | -0.149 | -0.149 |
| News share: boycotts | 608 | -0.156 | -0.041 | -0.041 | -0.035 | -0.041 | -0.029 | -0.047 | -0.028 |
| Average tone of all US news (sign flipped) | 608 | -0.076 | 0.139 | 0.087 | 0.122 | 0.142 | 0.038 | -0.003 | -0.055 |
| Share of US event coverage: conflict | 1347 | -0.021 | 0.136 | 0.044 | 0.086 | 0.115 | 0.092 | 0.071 | 0.05 |
| Hostile acts toward businesses, share of US event coverage | 1347 | 0.047 | -0.056 | -0.044 | -0.05 | -0.051 | -0.046 | -0.041 | -0.046 |
| Hostile share of business-related coverage | 1347 | -0.073 | 0.018 | 0.014 | 0.023 | 0.025 | 0.005 | 0.014 | 0.011 |

## 3. Corporate backlash events (curated outcome log)

119 dated backlash episodes since 2015-03-17. The reading a planner would have seen the week before an episode averaged **58.5**, against **57.4** for all weeks in the same span.

By severity (1 = brief viral moment, 5 = sustained national controversy):

| Severity | Episodes | Mean reading the week before |
|---|---|---|
| 1 | 2 | 16.8 |
| 2 | 39 | 52.6 |
| 3 | 44 | 65.6 |
| 4 | 23 | 58.4 |
| 5 | 11 | 59.3 |

Episodes in the following two weeks, per 100 weeks, by the band shown that week:

| Band | Weeks | Any episode | Severity ≥3 |
|---|---|---|---|
| Low | 70 | 40.0 | 28.6 |
| Moderate | 168 | 41.7 | 27.4 |
| Elevated | 205 | 39.5 | 32.2 |
| High | 123 | 48.8 | 38.2 |
| Severe | 40 | 55.0 | 40.0 |

Same test split by era (the log is denser after 2023, and those years were tenser, so each era is checked on its own):

| Era | Reading | Weeks | Severity ≥3 episodes in next two weeks, per 100 weeks |
|---|---|---|---|
| 2015-2023 | Low/Moderate | 183 | 21.3 |
| 2015-2023 | Elevated | 144 | 26.4 |
| 2015-2023 | High/Severe | 132 | 40.2 |
| 2024-2026 | Low/Moderate | 55 | 49.1 |
| 2024-2026 | Elevated | 61 | 45.9 |
| 2024-2026 | High/Severe | 31 | 32.3 |

Dimension readings the week before episodes vs. all weeks:

| Dimension | Before episodes | All weeks | Difference |
|---|---|---|---|
| Political and institutional | 63.4 | 56.2 | +7.2 |
| Jobs and financial security | 62.4 | 57.8 | +4.6 |
| Cost of living | 62.1 | 60.0 | +2.1 |
| Disasters, climate and health | 53.1 | 49.9 | +3.2 |
| Geopolitical | 50.8 | 53.4 | -2.6 |
| Public safety and unrest | 46.4 | 44.7 | +1.7 |

Does the hot dimension predict the *kind* of episode? Each trigger type is paired with the dimension it should feed on; the table compares that dimension's reading the week before episodes of that type with its reading before other types and in all weeks, and how often it was the hottest dimension.

| Trigger type | Dimension | Episodes | Dim. before this type | Before other types | All weeks | Hottest dim. before this type | Before other types |
|---|---|---|---|---|---|---|---|
| political_stance | Political and institutional | 35 | 69.6 | 60.8 | 56.2 | 29% | 26% |
| executive_statement | Political and institutional | 11 | 67.4 | 63.0 | 56.2 | 18% | 28% |
| pricing | Cost of living | 9 | 61.6 | 62.2 | 60.0 | 22% | 21% |
| labor_layoffs | Jobs and financial security | 9 | 57.2 | 62.8 | 57.8 | 33% | 22% |
| product_safety | Disasters, climate and health | 13 | 55.5 | 52.8 | 49.9 | 15% | 7% |
| service_incident | Disasters, climate and health | 8 | 40.0 | 54.0 | 49.9 | 0% | 8% |
| data_privacy | Political and institutional | 6 | 58.9 | 63.7 | 56.2 | 33% | 27% |
| marketing_misstep | Public safety and unrest | 16 | 33.2 | 48.4 | 44.7 | 6% | 9% |

Caveats: the log is curated and incomplete, episodes cluster in recent years when the log is richer, and the index was not tuned to this log. A clean result here is encouraging, not proof; a null result means the structure needs work.
