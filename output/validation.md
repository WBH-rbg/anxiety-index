# Validation report

Generated 2026-10-26. Methodology v0.1 prototype.

## 1. Face validity

Does the index read tense when everyone remembers tension, and calm when they remember calm?

| Period | Expected | Mean | Max | Weeks ≥80 | Weeks | Verdict |
|---|---|---|---|---|---|---|
| 9/11 and aftermath | tense | 87.4 | 100.0 | 8 | 11 | pass |
| Iraq invasion | tense | 88.0 | 94.9 | 6 | 7 | pass |
| Mid-2000s calm | calm | 22.3 | 70.2 | 0 | 131 | pass |
| Financial crisis | tense | 87.0 | 100.0 | 20 | 29 | pass |
| Debt-ceiling summer | tense | 71.0 | 84.3 | 1 | 7 | pass |
| 2013-2015 calm | calm | 20.6 | 75.9 | 0 | 156 | pass |
| COVID onset | tense | 81.4 | 88.9 | 6 | 8 | pass |
| Summer 2020 | tense | 96.8 | 99.5 | 7 | 7 | pass |
| Jan 6 week | tense | 80.5 | 86.3 | 2 | 3 | pass |
| Ukraine invasion | tense | 98.8 | 99.2 | 5 | 5 | pass |
| Inflation peak | tense | 96.6 | 99.3 | 6 | 6 | pass |
| Spring 2025 tariffs | tense | 93.7 | 97.6 | 4 | 4 | pass |

## 2. External series

Correlation of the weekly headline with series that should track public anxiety but are not inputs to the headline (detrended with a 52-week rolling median). 'lead+k' means the index this week vs. the series k weeks later.

| Series | Weeks | Level | Detrended | lead−4 | lead−2 | lead−1 | lead+1 | lead+2 | lead+4 |
|---|---|---|---|---|---|---|---|---|---|
| Wikipedia views: Anxiety | 591 | -0.293 | -0.254 | -0.256 | -0.258 | -0.253 | -0.265 | -0.267 | -0.257 |
| Wikipedia views: Anxiety disorder | 591 | -0.387 | -0.148 | -0.127 | -0.145 | -0.144 | -0.155 | -0.155 | -0.135 |
| Wikipedia views: Panic attack | 591 | -0.313 | -0.12 | -0.107 | -0.116 | -0.113 | -0.135 | -0.146 | -0.148 |
| News share: boycotts | 608 | -0.167 | -0.057 | -0.053 | -0.045 | -0.054 | -0.052 | -0.067 | -0.047 |
| Average tone of all US news (sign flipped) | 608 | -0.067 | 0.135 | 0.076 | 0.116 | 0.138 | 0.034 | -0.009 | -0.061 |
| Share of US event coverage: conflict | 1347 | -0.02 | 0.139 | 0.043 | 0.088 | 0.117 | 0.097 | 0.076 | 0.055 |
| Hostile acts toward businesses, share of US event coverage | 1347 | 0.052 | -0.049 | -0.045 | -0.048 | -0.047 | -0.038 | -0.035 | -0.039 |
| Hostile share of business-related coverage | 1347 | -0.073 | 0.02 | 0.01 | 0.02 | 0.024 | 0.008 | 0.017 | 0.013 |

## 3. Corporate backlash events (curated outcome log)

119 dated backlash episodes since 2015-03-17. The reading a planner would have seen the week before an episode averaged **58.0**, against **57.3** for all weeks in the same span.

By severity (1 = brief viral moment, 5 = sustained national controversy):

| Severity | Episodes | Mean reading the week before |
|---|---|---|
| 1 | 2 | 18.2 |
| 2 | 39 | 52.2 |
| 3 | 44 | 65.1 |
| 4 | 23 | 58.5 |
| 5 | 11 | 56.9 |

Episodes in the following two weeks, per 100 weeks, by the band shown that week:

| Band | Weeks | Any episode | Severity ≥3 |
|---|---|---|---|
| Low | 71 | 38.0 | 28.2 |
| Moderate | 167 | 41.9 | 26.9 |
| Elevated | 206 | 42.2 | 34.0 |
| High | 125 | 48.0 | 36.0 |
| Severe | 37 | 45.9 | 40.5 |

Same test split by era (the log is denser after 2023, and those years were tenser, so each era is checked on its own):

| Era | Reading | Weeks | Severity ≥3 episodes in next two weeks, per 100 weeks |
|---|---|---|---|
| 2015-2023 | Low/Moderate | 184 | 21.2 |
| 2015-2023 | Elevated | 137 | 27.0 |
| 2015-2023 | High/Severe | 138 | 39.1 |
| 2024-2026 | Low/Moderate | 54 | 48.1 |
| 2024-2026 | Elevated | 69 | 47.8 |
| 2024-2026 | High/Severe | 24 | 25.0 |

Dimension readings the week before episodes vs. all weeks:

| Dimension | Before episodes | All weeks | Difference |
|---|---|---|---|
| Political and institutional | 63.4 | 56.4 | +7.0 |
| Jobs and financial security | 62.4 | 57.8 | +4.6 |
| Cost of living | 62.1 | 60.0 | +2.1 |
| Disasters, climate and health | 53.1 | 49.9 | +3.2 |
| Geopolitical | 50.8 | 53.4 | -2.6 |
| Public safety and unrest | 46.4 | 44.7 | +1.7 |

Does the hot dimension predict the *kind* of episode? Each trigger type is paired with the dimension it should feed on; the table compares that dimension's reading the week before episodes of that type with its reading before other types and in all weeks, and how often it was the hottest dimension.

| Trigger type | Dimension | Episodes | Dim. before this type | Before other types | All weeks | Hottest dim. before this type | Before other types |
|---|---|---|---|---|---|---|---|
| political_stance | Political and institutional | 35 | 68.4 | 61.3 | 56.4 | 31% | 19% |
| executive_statement | Political and institutional | 11 | 64.1 | 63.4 | 56.4 | 27% | 22% |
| pricing | Cost of living | 9 | 61.6 | 62.2 | 60.0 | 22% | 21% |
| labor_layoffs | Jobs and financial security | 9 | 57.2 | 62.8 | 57.8 | 33% | 21% |
| product_safety | Disasters, climate and health | 13 | 55.5 | 52.8 | 49.9 | 15% | 9% |
| service_incident | Disasters, climate and health | 8 | 40.0 | 54.0 | 49.9 | 0% | 11% |
| data_privacy | Political and institutional | 6 | 59.5 | 63.6 | 56.4 | 33% | 22% |
| marketing_misstep | Public safety and unrest | 16 | 33.2 | 48.4 | 44.7 | 6% | 9% |

Caveats: the log is curated and incomplete, episodes cluster in recent years when the log is richer, and the index was not tuned to this log. A clean result here is encouraging, not proof; a null result means the structure needs work.
