# Validation report

Generated 2026-10-29. Methodology v0.1 prototype.

## 1. Face validity

Does the index read tense when everyone remembers tension, and calm when they remember calm?

| Period | Expected | Mean | Max | Weeks ≥80 | Weeks | Verdict |
|---|---|---|---|---|---|---|
| 9/11 and aftermath | tense | 87.4 | 100.0 | 8 | 11 | pass |
| Iraq invasion | tense | 87.9 | 94.7 | 6 | 7 | pass |
| Mid-2000s calm | calm | 22.3 | 70.1 | 0 | 131 | pass |
| Financial crisis | tense | 86.9 | 100.0 | 20 | 29 | pass |
| Debt-ceiling summer | tense | 70.9 | 83.2 | 1 | 7 | pass |
| 2013-2015 calm | calm | 20.6 | 75.9 | 0 | 156 | pass |
| COVID onset | tense | 81.3 | 89.2 | 6 | 8 | pass |
| Summer 2020 | tense | 96.8 | 99.5 | 7 | 7 | pass |
| Jan 6 week | tense | 80.5 | 86.3 | 2 | 3 | pass |
| Ukraine invasion | tense | 99.0 | 99.4 | 5 | 5 | pass |
| Inflation peak | tense | 96.6 | 99.2 | 6 | 6 | pass |
| Spring 2025 tariffs | tense | 93.9 | 97.9 | 4 | 4 | pass |

## 2. External series

Correlation of the weekly headline with series that should track public anxiety but are not inputs to the headline (detrended with a 52-week rolling median). 'lead+k' means the index this week vs. the series k weeks later.

| Series | Weeks | Level | Detrended | lead−4 | lead−2 | lead−1 | lead+1 | lead+2 | lead+4 |
|---|---|---|---|---|---|---|---|---|---|
| Wikipedia views: Anxiety | 591 | -0.295 | -0.255 | -0.256 | -0.258 | -0.254 | -0.267 | -0.268 | -0.26 |
| Wikipedia views: Anxiety disorder | 591 | -0.39 | -0.153 | -0.13 | -0.148 | -0.147 | -0.158 | -0.157 | -0.139 |
| Wikipedia views: Panic attack | 591 | -0.315 | -0.122 | -0.109 | -0.117 | -0.115 | -0.136 | -0.148 | -0.151 |
| News share: boycotts | 608 | -0.167 | -0.055 | -0.052 | -0.044 | -0.05 | -0.049 | -0.062 | -0.041 |
| Average tone of all US news (sign flipped) | 608 | -0.069 | 0.134 | 0.077 | 0.115 | 0.137 | 0.031 | -0.011 | -0.065 |
| Share of US event coverage: conflict | 1347 | -0.021 | 0.138 | 0.043 | 0.087 | 0.116 | 0.096 | 0.076 | 0.054 |
| Hostile acts toward businesses, share of US event coverage | 1347 | 0.051 | -0.05 | -0.045 | -0.048 | -0.047 | -0.039 | -0.035 | -0.039 |
| Hostile share of business-related coverage | 1347 | -0.074 | 0.019 | 0.011 | 0.02 | 0.024 | 0.008 | 0.017 | 0.014 |

## 3. Corporate backlash events (curated outcome log)

119 dated backlash episodes since 2015-03-17. The reading a planner would have seen the week before an episode averaged **58.2**, against **57.4** for all weeks in the same span.

By severity (1 = brief viral moment, 5 = sustained national controversy):

| Severity | Episodes | Mean reading the week before |
|---|---|---|
| 1 | 2 | 17.8 |
| 2 | 39 | 52.5 |
| 3 | 44 | 65.3 |
| 4 | 23 | 58.6 |
| 5 | 11 | 56.9 |

Episodes in the following two weeks, per 100 weeks, by the band shown that week:

| Band | Weeks | Any episode | Severity ≥3 |
|---|---|---|---|
| Low | 70 | 40.0 | 28.6 |
| Moderate | 167 | 41.3 | 26.9 |
| Elevated | 207 | 42.0 | 33.8 |
| High | 125 | 48.0 | 36.0 |
| Severe | 37 | 45.9 | 40.5 |

Same test split by era (the log is denser after 2023, and those years were tenser, so each era is checked on its own):

| Era | Reading | Weeks | Severity ≥3 episodes in next two weeks, per 100 weeks |
|---|---|---|---|
| 2015-2023 | Low/Moderate | 183 | 21.3 |
| 2015-2023 | Elevated | 138 | 26.8 |
| 2015-2023 | High/Severe | 138 | 39.1 |
| 2024-2026 | Low/Moderate | 54 | 48.1 |
| 2024-2026 | Elevated | 69 | 47.8 |
| 2024-2026 | High/Severe | 24 | 25.0 |

Dimension readings the week before episodes vs. all weeks:

| Dimension | Before episodes | All weeks | Difference |
|---|---|---|---|
| Political and institutional | 63.5 | 56.5 | +7.0 |
| Jobs and financial security | 62.4 | 57.8 | +4.6 |
| Cost of living | 62.1 | 60.0 | +2.1 |
| Disasters, climate and health | 53.4 | 50.1 | +3.3 |
| Geopolitical | 50.8 | 53.4 | -2.6 |
| Public safety and unrest | 46.4 | 44.7 | +1.7 |

Does the hot dimension predict the *kind* of episode? Each trigger type is paired with the dimension it should feed on; the table compares that dimension's reading the week before episodes of that type with its reading before other types and in all weeks, and how often it was the hottest dimension.

| Trigger type | Dimension | Episodes | Dim. before this type | Before other types | All weeks | Hottest dim. before this type | Before other types |
|---|---|---|---|---|---|---|---|
| political_stance | Political and institutional | 35 | 68.3 | 61.5 | 56.5 | 31% | 24% |
| executive_statement | Political and institutional | 11 | 64.1 | 63.4 | 56.5 | 27% | 26% |
| pricing | Cost of living | 9 | 61.6 | 62.2 | 60.0 | 22% | 21% |
| labor_layoffs | Jobs and financial security | 9 | 57.2 | 62.8 | 57.8 | 33% | 20% |
| product_safety | Disasters, climate and health | 13 | 55.8 | 53.1 | 50.1 | 8% | 8% |
| service_incident | Disasters, climate and health | 8 | 40.1 | 54.3 | 50.1 | 0% | 9% |
| data_privacy | Political and institutional | 6 | 59.8 | 63.7 | 56.5 | 33% | 26% |
| marketing_misstep | Public safety and unrest | 16 | 33.2 | 48.4 | 44.7 | 6% | 9% |

Caveats: the log is curated and incomplete, episodes cluster in recent years when the log is richer, and the index was not tuned to this log. A clean result here is encouraging, not proof; a null result means the structure needs work.
