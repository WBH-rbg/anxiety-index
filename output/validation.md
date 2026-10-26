# Validation report

Generated 2026-10-26. Methodology v0.1 prototype.

## 1. Face validity

Does the index read tense when everyone remembers tension, and calm when they remember calm?

| Period | Expected | Mean | Max | Weeks ≥80 | Weeks | Verdict |
|---|---|---|---|---|---|---|
| 9/11 and aftermath | tense | 82.3 | 99.7 | 8 | 11 | pass |
| Iraq invasion | tense | 85.1 | 94.8 | 5 | 7 | pass |
| Mid-2000s calm | calm | 22.4 | 69.3 | 0 | 131 | pass |
| Financial crisis | tense | 89.0 | 99.5 | 21 | 29 | pass |
| Debt-ceiling summer | tense | 76.2 | 94.4 | 4 | 7 | pass |
| 2013-2015 calm | calm | 19.8 | 72.7 | 0 | 156 | pass |
| COVID onset | tense | 76.2 | 86.3 | 4 | 8 | pass |
| Summer 2020 | tense | 97.8 | 100.0 | 7 | 7 | pass |
| Jan 6 week | tense | 80.6 | 84.5 | 2 | 3 | pass |
| Ukraine invasion | tense | 97.7 | 98.4 | 5 | 5 | pass |
| Inflation peak | tense | 94.4 | 98.2 | 6 | 6 | pass |
| Spring 2025 tariffs | tense | 99.3 | 99.8 | 4 | 4 | pass |

## 2. External series

Correlation of the weekly headline with series that should track public anxiety but are not inputs to the headline (detrended with a 52-week rolling median). 'lead+k' means the index this week vs. the series k weeks later.

| Series | Weeks | Level | Detrended | lead−4 | lead−2 | lead−1 | lead+1 | lead+2 | lead+4 |
|---|---|---|---|---|---|---|---|---|---|
| Wikipedia views: Anxiety | 591 | -0.335 | -0.3 | -0.302 | -0.303 | -0.298 | -0.31 | -0.313 | -0.309 |
| Wikipedia views: Anxiety disorder | 591 | -0.426 | -0.206 | -0.175 | -0.206 | -0.197 | -0.217 | -0.215 | -0.2 |
| Wikipedia views: Panic attack | 591 | -0.351 | -0.138 | -0.123 | -0.135 | -0.129 | -0.156 | -0.17 | -0.175 |
| News share: boycotts | 608 | -0.116 | -0.012 | -0.011 | -0.002 | -0.017 | -0.01 | -0.038 | -0.036 |
| Average tone of all US news (sign flipped) | 608 | -0.079 | 0.178 | 0.108 | 0.158 | 0.176 | 0.091 | 0.052 | -0.018 |
| Share of US event coverage: conflict | 1347 | -0.015 | 0.13 | 0.029 | 0.074 | 0.106 | 0.089 | 0.071 | 0.046 |
| Hostile acts toward businesses, share of US event coverage | 1347 | 0.045 | -0.047 | -0.047 | -0.046 | -0.043 | -0.038 | -0.028 | -0.036 |
| Hostile share of business-related coverage | 1347 | -0.086 | 0.012 | 0.003 | 0.011 | 0.02 | 0.002 | 0.013 | 0.005 |

## 3. Corporate backlash events (curated outcome log)

119 dated backlash episodes since 2015-03-17. The reading a planner would have seen the week before an episode averaged **61.3**, against **58.6** for all weeks in the same span.

By severity (1 = brief viral moment, 5 = sustained national controversy):

| Severity | Episodes | Mean reading the week before |
|---|---|---|
| 1 | 2 | 16.0 |
| 2 | 39 | 56.2 |
| 3 | 44 | 68.9 |
| 4 | 23 | 60.4 |
| 5 | 11 | 59.4 |

Episodes in the following two weeks, per 100 weeks, by the band shown that week:

| Band | Weeks | Any episode | Severity ≥3 |
|---|---|---|---|
| Low | 63 | 36.5 | 23.8 |
| Moderate | 163 | 42.3 | 27.6 |
| Elevated | 214 | 36.9 | 32.2 |
| High | 125 | 51.2 | 38.4 |
| Severe | 41 | 63.4 | 43.9 |

Same test split by era (the log is denser after 2023, and those years were tenser, so each era is checked on its own):

| Era | Reading | Weeks | Severity ≥3 episodes in next two weeks, per 100 weeks |
|---|---|---|---|
| 2015-2023 | Low/Moderate | 179 | 21.8 |
| 2015-2023 | Elevated | 157 | 25.5 |
| 2015-2023 | High/Severe | 123 | 41.5 |
| 2024-2026 | Low/Moderate | 47 | 44.7 |
| 2024-2026 | Elevated | 57 | 50.9 |
| 2024-2026 | High/Severe | 43 | 34.9 |

Dimension readings the week before episodes vs. all weeks:

| Dimension | Before episodes | All weeks | Difference |
|---|---|---|---|
| Political and institutional | 64.9 | 57.3 | +7.6 |
| Jobs and financial security | 62.5 | 57.7 | +4.8 |
| Cost of living | 62.2 | 60.0 | +2.2 |
| Disasters, climate and health | 53.1 | 49.9 | +3.2 |
| Geopolitical | 50.8 | 53.4 | -2.6 |
| Public safety and unrest | 46.4 | 44.7 | +1.7 |

Does the hot dimension predict the *kind* of episode? Each trigger type is paired with the dimension it should feed on; the table compares that dimension's reading the week before episodes of that type with its reading before other types and in all weeks, and how often it was the hottest dimension.

| Trigger type | Dimension | Episodes | Dim. before this type | Before other types | All weeks | Hottest dim. before this type | Before other types |
|---|---|---|---|---|---|---|---|
| political_stance | Political and institutional | 35 | 70.9 | 62.4 | 57.3 | 43% | 32% |
| executive_statement | Political and institutional | 11 | 66.7 | 64.7 | 57.3 | 36% | 35% |
| pricing | Cost of living | 9 | 61.6 | 62.3 | 60.0 | 22% | 20% |
| labor_layoffs | Jobs and financial security | 9 | 57.3 | 62.9 | 57.7 | 22% | 19% |
| product_safety | Disasters, climate and health | 13 | 55.5 | 52.8 | 49.9 | 8% | 5% |
| service_incident | Disasters, climate and health | 8 | 40.0 | 54.0 | 49.9 | 0% | 5% |
| data_privacy | Political and institutional | 6 | 60.8 | 65.1 | 57.3 | 50% | 35% |
| marketing_misstep | Public safety and unrest | 16 | 33.2 | 48.4 | 44.7 | 6% | 6% |

Caveats: the log is curated and incomplete, episodes cluster in recent years when the log is richer, and the index was not tuned to this log. A clean result here is encouraging, not proof; a null result means the structure needs work.
