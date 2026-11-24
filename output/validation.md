# Validation report

Generated 2026-11-24. Methodology v0.1 prototype.

## 1. Face validity

Does the index read tense when everyone remembers tension, and calm when they remember calm?

| Period | Expected | Mean | Max | Weeks ≥80 | Weeks | Verdict |
|---|---|---|---|---|---|---|
| 9/11 and aftermath | tense | 86.8 | 99.9 | 8 | 11 | pass |
| Iraq invasion | tense | 87.4 | 94.0 | 6 | 7 | pass |
| Mid-2000s calm | calm | 21.7 | 69.1 | 0 | 131 | pass |
| Financial crisis | tense | 86.4 | 99.8 | 20 | 29 | pass |
| Debt-ceiling summer | tense | 70.0 | 83.1 | 1 | 7 | pass |
| 2013-2015 calm | calm | 19.9 | 76.8 | 0 | 156 | pass |
| COVID onset | tense | 81.9 | 88.1 | 6 | 8 | pass |
| Summer 2020 | tense | 98.1 | 100.0 | 7 | 7 | pass |
| Jan 6 week | tense | 86.1 | 90.6 | 2 | 3 | pass |
| Ukraine invasion | tense | 98.4 | 99.1 | 5 | 5 | pass |
| Inflation peak | tense | 97.1 | 99.4 | 6 | 6 | pass |
| Spring 2025 tariffs | tense | 95.7 | 98.3 | 4 | 4 | pass |

## 2. External series

Correlation of the weekly headline with series that should track public anxiety but are not inputs to the headline (detrended with a 52-week rolling median). 'lead+k' means the index this week vs. the series k weeks later.

| Series | Weeks | Level | Detrended | lead−4 | lead−2 | lead−1 | lead+1 | lead+2 | lead+4 |
|---|---|---|---|---|---|---|---|---|---|
| Wikipedia views: Anxiety | 595 | -0.26 | -0.304 | -0.305 | -0.304 | -0.303 | -0.312 | -0.312 | -0.302 |
| Wikipedia views: Anxiety disorder | 595 | -0.375 | -0.271 | -0.238 | -0.259 | -0.262 | -0.27 | -0.265 | -0.24 |
| Wikipedia views: Panic attack | 595 | -0.296 | -0.166 | -0.147 | -0.16 | -0.159 | -0.179 | -0.189 | -0.193 |
| News share: boycotts | 612 | -0.14 | -0.078 | -0.062 | -0.061 | -0.072 | -0.073 | -0.093 | -0.075 |
| Average tone of all US news (sign flipped) | 612 | 0.025 | 0.146 | 0.075 | 0.113 | 0.144 | 0.044 | -0.002 | -0.059 |
| Share of US event coverage: conflict | 1351 | -0.017 | 0.132 | 0.038 | 0.082 | 0.113 | 0.089 | 0.068 | 0.047 |
| Hostile acts toward businesses, share of US event coverage | 1351 | 0.036 | -0.052 | -0.044 | -0.046 | -0.046 | -0.043 | -0.035 | -0.039 |
| Hostile share of business-related coverage | 1351 | -0.083 | 0.013 | 0.008 | 0.018 | 0.021 | 0.001 | 0.01 | 0.007 |

## 3. Corporate backlash events (curated outcome log)

119 dated backlash episodes since 2015-03-17. The reading a planner would have seen the week before an episode averaged **59.2**, against **58.5** for all weeks in the same span.

By severity (1 = brief viral moment, 5 = sustained national controversy):

| Severity | Episodes | Mean reading the week before |
|---|---|---|
| 1 | 2 | 25.8 |
| 2 | 39 | 54.0 |
| 3 | 44 | 66.4 |
| 4 | 23 | 58.7 |
| 5 | 11 | 56.0 |

Episodes in the following two weeks, per 100 weeks, by the band shown that week:

| Band | Weeks | Any episode | Severity ≥3 |
|---|---|---|---|
| Low | 57 | 28.1 | 21.1 |
| Moderate | 171 | 43.3 | 26.9 |
| Elevated | 218 | 42.2 | 34.9 |
| High | 126 | 50.0 | 38.1 |
| Severe | 38 | 42.1 | 34.2 |

Same test split by era (the log is denser after 2023, and those years were tenser, so each era is checked on its own):

| Era | Reading | Weeks | Severity ≥3 episodes in next two weeks, per 100 weeks |
|---|---|---|---|
| 2015-2023 | Low/Moderate | 169 | 19.5 |
| 2015-2023 | Elevated | 153 | 28.1 |
| 2015-2023 | High/Severe | 137 | 39.4 |
| 2024-2026 | Low/Moderate | 59 | 42.4 |
| 2024-2026 | Elevated | 65 | 50.8 |
| 2024-2026 | High/Severe | 27 | 25.9 |

Dimension readings the week before episodes vs. all weeks:

| Dimension | Before episodes | All weeks | Difference |
|---|---|---|---|
| Jobs and financial security | 65.5 | 59.1 | +6.4 |
| Political and institutional | 62.8 | 56.5 | +6.3 |
| Cost of living | 62.2 | 60.3 | +1.9 |
| Disasters, climate and health | 54.5 | 51.7 | +2.8 |
| Geopolitical | 51.3 | 53.9 | -2.6 |
| Public safety and unrest | 47.0 | 46.3 | +0.7 |

Does the hot dimension predict the *kind* of episode? Each trigger type is paired with the dimension it should feed on; the table compares that dimension's reading the week before episodes of that type with its reading before other types and in all weeks, and how often it was the hottest dimension.

| Trigger type | Dimension | Episodes | Dim. before this type | Before other types | All weeks | Hottest dim. before this type | Before other types |
|---|---|---|---|---|---|---|---|
| political_stance | Political and institutional | 35 | 68.1 | 60.7 | 56.5 | 17% | 20% |
| executive_statement | Political and institutional | 11 | 63.0 | 62.8 | 56.5 | 18% | 19% |
| pricing | Cost of living | 9 | 60.5 | 62.4 | 60.3 | 22% | 20% |
| labor_layoffs | Jobs and financial security | 9 | 62.9 | 65.7 | 59.1 | 33% | 25% |
| product_safety | Disasters, climate and health | 13 | 55.0 | 54.4 | 51.7 | 8% | 10% |
| service_incident | Disasters, climate and health | 8 | 39.8 | 55.5 | 51.7 | 0% | 11% |
| data_privacy | Political and institutional | 6 | 60.4 | 63.0 | 56.5 | 17% | 19% |
| marketing_misstep | Public safety and unrest | 16 | 36.0 | 48.7 | 46.3 | 6% | 11% |

Caveats: the log is curated and incomplete, episodes cluster in recent years when the log is richer, and the index was not tuned to this log. A clean result here is encouraging, not proof; a null result means the structure needs work.
