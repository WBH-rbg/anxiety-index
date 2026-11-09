# Validation report

Generated 2026-11-09. Methodology v0.1 prototype.

## 1. Face validity

Does the index read tense when everyone remembers tension, and calm when they remember calm?

| Period | Expected | Mean | Max | Weeks ≥80 | Weeks | Verdict |
|---|---|---|---|---|---|---|
| 9/11 and aftermath | tense | 86.8 | 99.9 | 8 | 11 | pass |
| Iraq invasion | tense | 87.4 | 94.0 | 6 | 7 | pass |
| Mid-2000s calm | calm | 21.7 | 69.1 | 0 | 131 | pass |
| Financial crisis | tense | 86.4 | 99.8 | 20 | 29 | pass |
| Debt-ceiling summer | tense | 70.0 | 83.1 | 1 | 7 | pass |
| 2013-2015 calm | calm | 19.9 | 76.7 | 0 | 156 | pass |
| COVID onset | tense | 81.8 | 88.0 | 6 | 8 | pass |
| Summer 2020 | tense | 98.1 | 100.0 | 7 | 7 | pass |
| Jan 6 week | tense | 86.0 | 90.6 | 2 | 3 | pass |
| Ukraine invasion | tense | 98.3 | 99.1 | 5 | 5 | pass |
| Inflation peak | tense | 97.1 | 99.4 | 6 | 6 | pass |
| Spring 2025 tariffs | tense | 95.8 | 98.6 | 4 | 4 | pass |

## 2. External series

Correlation of the weekly headline with series that should track public anxiety but are not inputs to the headline (detrended with a 52-week rolling median). 'lead+k' means the index this week vs. the series k weeks later.

| Series | Weeks | Level | Detrended | lead−4 | lead−2 | lead−1 | lead+1 | lead+2 | lead+4 |
|---|---|---|---|---|---|---|---|---|---|
| Wikipedia views: Anxiety | 593 | -0.261 | -0.311 | -0.309 | -0.31 | -0.31 | -0.319 | -0.319 | -0.309 |
| Wikipedia views: Anxiety disorder | 593 | -0.375 | -0.275 | -0.242 | -0.265 | -0.269 | -0.275 | -0.269 | -0.243 |
| Wikipedia views: Panic attack | 593 | -0.295 | -0.165 | -0.144 | -0.159 | -0.159 | -0.178 | -0.187 | -0.19 |
| News share: boycotts | 610 | -0.139 | -0.077 | -0.061 | -0.058 | -0.07 | -0.071 | -0.093 | -0.074 |
| Average tone of all US news (sign flipped) | 610 | 0.026 | 0.145 | 0.078 | 0.115 | 0.143 | 0.043 | -0.003 | -0.056 |
| Share of US event coverage: conflict | 1349 | -0.016 | 0.133 | 0.038 | 0.083 | 0.113 | 0.09 | 0.07 | 0.049 |
| Hostile acts toward businesses, share of US event coverage | 1349 | 0.038 | -0.051 | -0.044 | -0.045 | -0.046 | -0.042 | -0.035 | -0.041 |
| Hostile share of business-related coverage | 1349 | -0.082 | 0.014 | 0.008 | 0.019 | 0.021 | 0.001 | 0.01 | 0.006 |

## 3. Corporate backlash events (curated outcome log)

119 dated backlash episodes since 2015-03-17. The reading a planner would have seen the week before an episode averaged **59.2**, against **58.5** for all weeks in the same span.

By severity (1 = brief viral moment, 5 = sustained national controversy):

| Severity | Episodes | Mean reading the week before |
|---|---|---|
| 1 | 2 | 24.7 |
| 2 | 39 | 53.9 |
| 3 | 44 | 66.4 |
| 4 | 23 | 58.8 |
| 5 | 11 | 56.0 |

Episodes in the following two weeks, per 100 weeks, by the band shown that week:

| Band | Weeks | Any episode | Severity ≥3 |
|---|---|---|---|
| Low | 57 | 28.1 | 21.1 |
| Moderate | 170 | 43.5 | 27.6 |
| Elevated | 218 | 42.2 | 34.4 |
| High | 125 | 50.4 | 38.4 |
| Severe | 38 | 42.1 | 34.2 |

Same test split by era (the log is denser after 2023, and those years were tenser, so each era is checked on its own):

| Era | Reading | Weeks | Severity ≥3 episodes in next two weeks, per 100 weeks |
|---|---|---|---|
| 2015-2023 | Low/Moderate | 169 | 20.1 |
| 2015-2023 | Elevated | 153 | 27.5 |
| 2015-2023 | High/Severe | 137 | 39.4 |
| 2024-2026 | Low/Moderate | 58 | 43.1 |
| 2024-2026 | Elevated | 65 | 50.8 |
| 2024-2026 | High/Severe | 26 | 26.9 |

Dimension readings the week before episodes vs. all weeks:

| Dimension | Before episodes | All weeks | Difference |
|---|---|---|---|
| Jobs and financial security | 65.5 | 59.1 | +6.4 |
| Political and institutional | 62.9 | 56.6 | +6.3 |
| Cost of living | 62.2 | 60.3 | +1.9 |
| Disasters, climate and health | 54.4 | 51.5 | +2.9 |
| Geopolitical | 51.3 | 53.8 | -2.5 |
| Public safety and unrest | 47.0 | 46.3 | +0.7 |

Does the hot dimension predict the *kind* of episode? Each trigger type is paired with the dimension it should feed on; the table compares that dimension's reading the week before episodes of that type with its reading before other types and in all weeks, and how often it was the hottest dimension.

| Trigger type | Dimension | Episodes | Dim. before this type | Before other types | All weeks | Hottest dim. before this type | Before other types |
|---|---|---|---|---|---|---|---|
| political_stance | Political and institutional | 35 | 68.1 | 60.7 | 56.6 | 20% | 17% |
| executive_statement | Political and institutional | 11 | 62.6 | 62.9 | 56.6 | 18% | 18% |
| pricing | Cost of living | 9 | 60.5 | 62.4 | 60.3 | 22% | 20% |
| labor_layoffs | Jobs and financial security | 9 | 62.9 | 65.7 | 59.1 | 33% | 25% |
| product_safety | Disasters, climate and health | 13 | 55.0 | 54.4 | 51.5 | 15% | 12% |
| service_incident | Disasters, climate and health | 8 | 39.8 | 55.5 | 51.5 | 0% | 14% |
| data_privacy | Political and institutional | 6 | 60.4 | 63.0 | 56.6 | 17% | 18% |
| marketing_misstep | Public safety and unrest | 16 | 35.8 | 48.7 | 46.3 | 6% | 11% |

Caveats: the log is curated and incomplete, episodes cluster in recent years when the log is richer, and the index was not tuned to this log. A clean result here is encouraging, not proof; a null result means the structure needs work.
