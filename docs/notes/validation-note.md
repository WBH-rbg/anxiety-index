# Anxiety Index: First Validation Note

*October 25–26, 2026. Methodology v0.3 prototype with the attention-budget headline. Nothing in the model was tuned to these tests, with one exception noted in section 1. Figures were refreshed after a timing correction on October 26 that aligned news-coverage signals with the week they occurred in (they had been entering one week late); the correction left every conclusion intact and made the outcome gradient in section 2 cleaner.*

## 1. Face validity: 12 of 12

| Period | Expected | Mean | Max | Verdict |
|---|---|---|---|---|
| 9/11 and aftermath | tense | 82 | 100 | pass |
| Iraq invasion | tense | 85 | 95 | pass |
| Mid-2000s calm (2005–mid-2007) | calm | 22 | 69 | pass |
| Financial crisis | tense | 89 | 100 | pass |
| Debt-ceiling summer 2011 | tense | 76 | 94 | pass |
| 2013–2015 calm | calm | 20 | 73 | pass |
| COVID onset | tense | 76 | 86 | pass |
| Summer 2020 | tense | 98 | 100 | pass |
| January 6 week | tense | 81 | 85 | pass |
| Ukraine invasion | tense | 98 | 98 | pass |
| Inflation peak 2022 | tense | 94 | 98 | pass |
| Spring 2025 tariffs | tense | 99 | 100 | pass |

"Pass" for a tense period means the index reached High or Severe; for a calm period, that the average stayed under 40. The one deliberate adjustment: the political dimension's prior weight was raised from 15 to 20 (jobs lowered from 20 to 15) after the outcome test below showed political anxiety is the strongest precursor of backlash; this is also what lets the January 6 week reach High.

## 2. Corporate backlash episodes (curated outcome log, 119 episodes, 2015–2026)

The question a planner cares about: when the index is high, are backlash episodes more likely in the weeks that follow?

**Major episodes (severity 3 or higher) in the following two weeks, per 100 weeks:**

| Band shown that week | Weeks | Rate |
|---|---|---|
| Low | 63 | 24 |
| Moderate | 163 | 28 |
| Elevated | 214 | 32 |
| High | 125 | 38 |
| Severe | 41 | 44 |

The gradient is now monotonic from Low to Severe. **Checked within eras**, because the log is denser after 2023 and those years were tenser: within 2015–2023 the rate runs 22 (Low/Moderate) → 26 (Elevated) → 42 (High/Severe). The 2024–2026 slice is too small to read.

**Which dimensions run hot before episodes:** political and institutional +8, jobs and financial +5, disasters +3, cost of living +2, safety +2, geopolitical −3.

### 2b. Does the hot dimension predict the *kind* of episode?

Each trigger type in the log was paired with the dimension it should feed on, and that dimension's reading the week before was compared with its reading before other kinds of episode and in all weeks.

| Trigger type | Dimension | Episodes | Before this type | Before other types | All weeks | Was the hottest dimension (this type / other types) |
|---|---|---|---|---|---|---|
| Political stance | Political | 35 | **71** | 62 | 57 | 43% / 32% |
| Executive statement | Political | 11 | 67 | 65 | 57 | 36% / 35% |
| Data privacy | Political | 6 | 61 | 65 | 57 | 50% / 35% |
| Pricing | Cost of living | 9 | 62 | 62 | 60 | 22% / 20% |
| Layoffs and labor | Jobs | 9 | 57 | 63 | 58 | 22% / 19% |
| Product safety | Disasters and health | 13 | 56 | 53 | 50 | 8% / 5% |
| Service incident | Disasters and health | 8 | 40 | 54 | 50 | 0% / 5% |
| Marketing misstep | Public safety | 16 | **33** | 48 | 45 | 6% / 6% |

Two results stand out. **Political-stance backlash follows politically hot weeks**: the political dimension averaged 71 before those 35 episodes, against 62 before other kinds and 57 in general, and it was the hottest dimension before 43% of them. **Marketing missteps land in calm weeks**: the safety dimension averaged 33 before those 16 episodes, well below its norm, and service-incident backlash shows the same pattern (40 against 50). That is the crowding-out effect from section 3 seen from the other side: a tone-deaf campaign becomes the story when nothing else is. Pricing and layoff episodes show no dimension signal, but there are only nine of each; this is where a larger log is needed.

**For planners:** the dimension readings are not interchangeable. A hot political reading is the specific warning for stance-related decisions; a quiet week is when a marketing misjudgment is most exposed.

## 3. A systematic check that disagrees, and what it means

To avoid relying only on a hand-curated log, a systematic measure was built from GDELT's events table: weeks in which a named company's hostile coverage (demands, disapproval, threats, protests, coercion aimed at it) spikes to at least four times its own norm. The detector picks out the right episodes (Starbucks in April 2018, Wells Fargo in fall 2016, Boeing in March 2019 and 2024, Netflix in October 2021, Disney in February 2024).

But its relationship with the index runs the **opposite** way: a company spike followed 52% of Low weeks and only 24% of Severe weeks. Spikes after tense weeks are no larger, but they are angrier (average tone −4.2 versus −3.6).

The most plausible reading is crowding-out: when the national news hole is full of war, pandemic, or political crisis, company stories don't break through. The curated log, which records major episodes whether or not they dominated coverage, shows the priming effect; the coverage-spike measure shows the attention effect.

**The refined thesis:** a tense week makes a company story *less likely to land* and *more hostile when it does*. For planners, this is more useful than "high anxiety means more backlash." It argues for the index eventually publishing two readings: how full the news hole is (attention availability) and how hot a reaction will be if a story lands (priming). The present headline measures priming; news concentration (now reported with each reading) is the first measure of availability.

## 4. Shared cultural events: quiet windows, but not safe harbors

A calendar of 201 shared cultural moments 2015–2026 (Super Bowls, Olympics, July 4, Thanksgiving, Christmas, eclipses, major finals, record tours) was built, each scored 1–3 for how much of the country was aware of it the same day. Weeks overlapping a scale-3 event (62 of 617 weeks since 2015) were compared with all other weeks.

| Measure | In windows | Other weeks |
|---|---|---|
| Mean headline | 50.7 | 58.5 |
| Mean week-over-week headline change | −1.3 | +0.2 |
| Attention-lens reading (z) | +0.04 | +0.10 |
| Attention-lens change | −0.03 | +0.00 |

So the distraction effect is real: shared cultural moments are quieter weeks, and the index drifts down during them. The expected next finding did not appear, though. Major backlash episodes in the two weeks *after* a window week are **more** common (31 per 100 weeks versus 22), and that holds within band groups (Low/Moderate: 35 versus 14; High/Severe: 44 versus 26). Looking at the week itself, a major episode lands in 10% of window weeks, 16% of the first weeks after a window closes, and 12% of all other weeks.

The specific cases explain it. Within 14 days after a Super Bowl: Uber (2017), Norfolk Southern's East Palestine derailment (2023), Google's Gemini image controversy (2024), Meta/YouTube (2026). Within 14 days after Christmas: H&M (2018), Southwest's meltdown (2022), Boeing's door plug (2024), Meta's fact-checking reversal (2025), Paramount Skydance and xAI (2026). Several of these are announcements or decisions held through the holiday and released as soon as attention returned; others are failures that happened to land then.

**For planners:** a shared cultural moment is a genuine lull, but the week it ends is a landing zone, both because audiences are paying attention again and because competitors hold their own announcements for it. The look-ahead now says this explicitly whenever a scale-3 event falls in the next three weeks.

## 5. Scheduled catalysts: build-up and release

A second calendar of 545 dated catalysts 2015–2027 (FOMC decisions, CPI and jobs-report days, elections, States of the Union, Supreme Court term ends and major decision days, debt-limit and funding deadlines, shutdown starts and ends, tax day, hurricane season) was compiled from primary sources, each row carrying the source it was checked against. Effects are mean week-over-week changes in percentile points for weeks containing the catalyst, with the two weeks before and the week after.

| Catalyst | Cases | Headline: two weeks before | In the week | Week after | Dimension in the week |
|---|---|---|---|---|---|
| Election day | 14 | −4.4 | **+2.9** | −6.0 | Political +5.4 |
| Tax day | 12 | +1.4 | +2.5 | −1.2 | Cost of living +2.5 |
| Debt-limit or funding deadline | 13 | −2.0 | −2.3 | −2.5 | Political **−10.7** |
| Shutdown start/end, debt-limit resolution | 25 | +2.8 | +1.9 | +0.2 | Political −1.2 |
| Supreme Court term-end decisions | 12 | −1.9 | −1.9 | −6.8 | Political +5.2 |
| State of the Union | 12 | −0.4 | −2.5 | −0.8 | Political +1.4 |
| CPI release | 140 | −0.3 | +0.5 | +0.7 | Cost of living +0.3 |
| Jobs report | 140 | −1.1 | +0.2 | +1.5 | Jobs +0.9 |
| Fed decision (scheduled) | 93 | 0.0 | −0.1 | −0.5 | Jobs −0.7 |
| Fed emergency action | 3 | +18.8 | +2.3 | +9.1 | Jobs +1.5 |

Other weeks average −0.1 to 0.0. What the table says, with the caution that most categories have 12–25 cases:

- **Elections and Supreme Court term ends spike the political dimension in the week and release it hard the week after.** The political reading rises 5 points in election week and the headline falls 6 the week after; the same shape appears after the Court's June decisions.
- **Deadlines resolve.** The political dimension drops 11 points in the week of a debt-limit or funding deadline, because that is usually when the deal lands; the build-up shows in the preceding weeks' political reading. Shutdown starts and resolutions, which are unscheduled, add about 2 points in the week.
- **Scheduled data days barely register** on the headline, which is correct: the index reacts to what the numbers say, not to the fact of their release. CPI days nudge cost of living by 0.3, jobs days nudge jobs by 0.9.
- **Fed emergency actions (three cases, all March 2020)** sit in the middle of the largest moves in the series; they are markers of a crisis, not causes of the reading.

These effect sizes feed the daily look-ahead, which lists the catalysts in the next three weeks with their histories. For the week ending October 24, 2026, that is the October 28 FOMC decision (no typical effect), the November 3 midterm election (political +5 in the week, headline −6 the week after), and the October jobs report and CPI (small).

## 6. External series

Correlations of the weekly headline with continuous series that are not headline inputs are near zero or weak (news tone inverted +0.18 at short leads; hostile-toward-business coverage share ~0; Wikipedia anxiety-article views negative). The continuous business-hostility measures appear to track routine conflict (strikes, lawsuits, regulatory disputes), which is roughly constant. Episodic measures (sections 2 and 3) are the informative ones.

## 7. Scenario sensitivity (week ending October 24, 2026, reading 59)

Geopolitical flare-up → 73; government shutdown → 64; gasoline up 10% → 63; hot CPI print → 62; jobless-claims spike → 62; a mass shooting dominating the week → 62; major hurricane landfall → 62; magnitude 7.0 earthquake near Los Angeles → 61; Fed surprise → 60. Under the attention-budget rule, a second hot dimension adds to the headline at half the rate of the first, which was the behavior asked for.

## 8. How predictable is the headline? (first forecast baseline)

A small, explainable model was backtested with yearly refits from 2010 (no look-ahead): half-weight on a ridge regression of future change on the current level, recent momentum, and the six dimension readings with their four-week changes; half-weight on "no change." Mean absolute error in percentile points:

| Weeks ahead | "No change" error | Model error | Improvement | Direction right | Direction right when the model is confident |
|---|---|---|---|---|---|
| 1 | 6.7 | 6.6 | +1% | 57% | 65% |
| 2 | 9.9 | 9.7 | +2% | 60% | 68% |
| 4 | 13.9 | 13.3 | +4% | 63% | 76% |
| 8 | 19.9 | 18.1 | +9% | 68% | 76% |

Two honest conclusions. First, the headline is persistent: the best one- or two-week forecast is close to today's reading, and anyone claiming precision at those horizons is overselling. Second, the model's edge grows with horizon because it learns two things that match the thesis: readings far above normal ease back, and anxiety driven by shocks (safety, geopolitics, disasters) fades faster than anxiety driven by background pressure (cost of living, politics), which persists. The published outlook shows central paths with 50% and 80% ranges taken from the model's own backtest errors, the band-conditional "what has usually happened from here" table, and the track record itself, so the claim stays checkable. Every forecast is stored and scored automatically as its target week arrives.

From the week ending October 24, 2026 (58, Elevated): expected 56 in four weeks (80% range 35–78), 54 in eight weeks (25–83); a 9% chance of High or Severe and a 33% chance of dropping below 50 within four weeks.

## 9. Next validation steps

- A larger outcome log built from the systematic detector and hand-checked, so the priming effect and the type-of-episode effect can be measured on hundreds of episodes rather than 119.
- Adding scheduled catalysts (election weeks, deadline weeks) as inputs to the forecast model, now that their effects are measured.
- Reading the forecast scorecard as weeks arrive.
