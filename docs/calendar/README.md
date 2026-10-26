# Calendars

Two hand-compiled calendars feed the look-ahead and the calendar tests (`index/calendar.py`). Neither is an input to the index itself.

## catalysts.csv

Scheduled and unscheduled events that tend to move specific dimensions, 2015–2027: FOMC decisions (scheduled meetings and emergency actions), CPI and jobs-report release days, election days, States of the Union, Supreme Court term-end and major decision days, debt-limit X-dates, funding deadlines, shutdown starts and ends, tax day, and the start and end of Atlantic hurricane season.

Columns: `date, category, label, scheduled, notes, source`. `scheduled=false` marks events nobody could have put on a calendar in advance (emergency Fed cuts, shutdown starts, debt-limit resolutions); the tests treat those as separate categories. Releases cancelled during the fall-2025 shutdown are kept with `CANCELLED` in the label and ignored by the tests. Every row carries the source it was checked against; `build_catalysts.py` regenerates the file.

## cultural_events.csv

Shared cultural moments 2015–2026 (Super Bowls, Olympics, July 4, Thanksgiving, Christmas, eclipses, major finals, record tours, royal and national ceremonies), each with a `scale` from 1 to 3. Scale 3 means most of the country was aware of it the same day. The distraction-window test uses scale-3 events.
