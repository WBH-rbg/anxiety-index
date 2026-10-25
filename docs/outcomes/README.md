# Outcome log

`backlash_events.csv` is the curated log of US corporate backlash episodes used to validate the index:
moments when a company's action or statement triggered widespread public outrage, boycott calls, viral
criticism, or demands for accountability. One row per episode.

Columns: event_date (the day the backlash broke), company, sector, trigger_type, description, reaction,
severity (1 = brief viral moment, 3 = multi-week national story with measurable impact, 5 = sustained
national controversy with major financial or leadership consequences), business_impact, duration_weeks, sources.

Seed version: 119 episodes, January 2015 to September 2026, compiled October 25, 2026. Every date was
anchored to a dated source; business-impact phrases were not individually source-checked. The log is
loaded into BigQuery (`ai_outcomes.backlash_events`) by the index workflow and is meant to grow: add rows,
keep the header, keep descriptions neutral.
