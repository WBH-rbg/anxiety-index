#!/usr/bin/env python3
"""Build catalysts.csv from verified source data (all dates pulled from fetched sources in-session)."""
import csv
from datetime import date

rows = []

def add(d, cat, label, scheduled, notes, source):
    rows.append({
        "date": d, "category": cat, "label": label,
        "scheduled": "true" if scheduled else "false",
        "notes": notes, "source": source,
    })

# ---------------------------------------------------------------------------
# 1. FOMC decision days
# ---------------------------------------------------------------------------
FRASER = "https://fraser.stlouisfed.org/title/federal-open-market-committee-meeting-minutes-transcripts-documents-677?browse=2010s"
FEDCAL = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
FED2020 = "https://www.federalreserve.gov/newsevents/pressreleases/2020-press-fomc.htm"
OMO = "https://www.federalreserve.gov/monetarypolicy/openmarket.htm"

# decision day -> rate change note (from Fed Open Market Operations table; that table lists the
# effective date, which is the business day after the decision)
rate_changes = {
    "2015-12-16": "+25bp to 0.25-0.50% (first hike since 2006)",
    "2016-12-14": "+25bp to 0.50-0.75%",
    "2017-03-15": "+25bp to 0.75-1.00%",
    "2017-06-14": "+25bp to 1.00-1.25%",
    "2017-12-13": "+25bp to 1.25-1.50%",
    "2018-03-21": "+25bp to 1.50-1.75%",
    "2018-06-13": "+25bp to 1.75-2.00%",
    "2018-09-26": "+25bp to 2.00-2.25%",
    "2018-12-19": "+25bp to 2.25-2.50%",
    "2019-07-31": "-25bp to 2.00-2.25% (first cut since 2008)",
    "2019-09-18": "-25bp to 1.75-2.00%",
    "2019-10-30": "-25bp to 1.50-1.75%",
    "2020-03-03": "-50bp to 1.00-1.25% (emergency, unscheduled)",
    "2020-03-15": "-100bp to 0-0.25% (emergency, Sunday; replaced the scheduled Mar 17-18 meeting)",
    "2022-03-16": "+25bp to 0.25-0.50% (first hike of 2022-23 cycle)",
    "2022-05-04": "+50bp to 0.75-1.00%",
    "2022-06-15": "+75bp to 1.50-1.75%",
    "2022-07-27": "+75bp to 2.25-2.50%",
    "2022-09-21": "+75bp to 3.00-3.25%",
    "2022-11-02": "+75bp to 3.75-4.00%",
    "2022-12-14": "+50bp to 4.25-4.50%",
    "2023-02-01": "+25bp to 4.50-4.75%",
    "2023-03-22": "+25bp to 4.75-5.00%",
    "2023-05-03": "+25bp to 5.00-5.25%",
    "2023-07-26": "+25bp to 5.25-5.50% (cycle peak)",
    "2024-09-18": "-50bp to 4.75-5.00% (first cut of easing cycle)",
    "2024-11-07": "-25bp to 4.50-4.75%",
    "2024-12-18": "-25bp to 4.25-4.50%",
    "2025-09-17": "-25bp to 4.00-4.25%",
    "2025-10-29": "-25bp to 3.75-4.00%",
    "2025-12-10": "-25bp to 3.50-3.75%",
    "2026-09-16": "+25bp to 3.75-4.00% (per Sep 16 2026 FOMC statement)",
}

fomc = {
    2015: (["01-28","03-18","04-29","06-17","07-29","09-17","10-28","12-16"], FRASER),
    2016: (["01-27","03-16","04-27","06-15","07-27","09-21","11-02","12-14"], FRASER),
    2017: (["02-01","03-15","05-03","06-14","07-26","09-20","11-01","12-13"], FRASER),
    2018: (["01-31","03-21","05-02","06-13","08-01","09-26","11-08","12-19"], FRASER),
    2019: (["01-30","03-20","05-01","06-19","07-31","09-18","10-30","12-11"], FRASER),
    2020: (["01-29","04-29","06-10","07-29","09-16","11-05","12-16"], FED2020),
    2021: (["01-27","03-17","04-28","06-16","07-28","09-22","11-03","12-15"], FEDCAL),
    2022: (["01-26","03-16","05-04","06-15","07-27","09-21","11-02","12-14"], FEDCAL),
    2023: (["02-01","03-22","05-03","06-14","07-26","09-20","11-01","12-13"], FEDCAL),
    2024: (["01-31","03-20","05-01","06-12","07-31","09-18","11-07","12-18"], FEDCAL),
    2025: (["01-29","03-19","05-07","06-18","07-30","09-17","10-29","12-10"], FEDCAL),
    2026: (["01-28","03-18","04-29","06-17","07-29","09-16","10-28","12-09"], FEDCAL),
    2027: (["01-27","03-17","04-28","06-09","07-28","09-15","10-27","12-08"], FEDCAL),
}
sep_meetings = {  # meetings with Summary of Economic Projections + (pre-2019) press conference
    "03","06","09","12"
}
for yr, (days, src) in fomc.items():
    for md in days:
        d = f"{yr}-{md}"
        note_parts = []
        if d in rate_changes:
            note_parts.append("Rate change: " + rate_changes[d])
        else:
            note_parts.append("No rate change")
        if yr == 2027:
            note_parts.append("2027 schedule published by Fed, tentative until confirmed at preceding meeting")
        if yr >= 2026 and date.fromisoformat(d) > date(2026,10,25):
            note_parts.append("future")
        add(d, "fomc_decision", "FOMC decision", True, "; ".join(note_parts),
            src if d not in rate_changes else src + " ; " + OMO)

# 2020 unscheduled/emergency FOMC actions
add("2020-03-03", "fomc_decision", "FOMC emergency rate cut", False,
    "Rate change: " + rate_changes["2020-03-03"], FED2020 + " ; " + OMO)
add("2020-03-15", "fomc_decision", "FOMC emergency rate cut", False,
    "Rate change: " + rate_changes["2020-03-15"], FED2020 + " ; " + OMO)
add("2020-03-23", "fomc_decision", "FOMC unscheduled statement (open-ended QE)", False,
    "Unscheduled statement; no rate change; announced unlimited Treasury/MBS purchases", FED2020)

# ---------------------------------------------------------------------------
# 2. CPI releases
# ---------------------------------------------------------------------------
CPI_ARCH = "https://www.bls.gov/bls/news-release/cpi.htm"
CPI_SCHED = "https://www.bls.gov/schedule/news_release/cpi.htm"
BLS2027 = "https://www.bls.gov/schedule/2027/home.htm"
BLS_LAPSE = "https://www.bls.gov/bls/2025-lapse-revised-release-dates.htm"
MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]

# (reference year, reference month index 1-12) -> release date
cpi = {
 (2015,1):"2015-02-26",(2015,2):"2015-03-24",(2015,3):"2015-04-17",(2015,4):"2015-05-22",(2015,5):"2015-06-18",(2015,6):"2015-07-17",
 (2015,7):"2015-08-19",(2015,8):"2015-09-16",(2015,9):"2015-10-15",(2015,10):"2015-11-17",(2015,11):"2015-12-15",(2015,12):"2016-01-20",
 (2016,1):"2016-02-19",(2016,2):"2016-03-16",(2016,3):"2016-04-14",(2016,4):"2016-05-17",(2016,5):"2016-06-16",(2016,6):"2016-07-15",
 (2016,7):"2016-08-16",(2016,8):"2016-09-16",(2016,9):"2016-10-18",(2016,10):"2016-11-17",(2016,11):"2016-12-15",(2016,12):"2017-01-18",
 (2017,1):"2017-02-15",(2017,2):"2017-03-15",(2017,3):"2017-04-14",(2017,4):"2017-05-12",(2017,5):"2017-06-14",(2017,6):"2017-07-14",
 (2017,7):"2017-08-11",(2017,8):"2017-09-14",(2017,9):"2017-10-13",(2017,10):"2017-11-15",(2017,11):"2017-12-13",(2017,12):"2018-01-12",
 (2018,1):"2018-02-14",(2018,2):"2018-03-13",(2018,3):"2018-04-11",(2018,4):"2018-05-10",(2018,5):"2018-06-12",(2018,6):"2018-07-12",
 (2018,7):"2018-08-10",(2018,8):"2018-09-13",(2018,9):"2018-10-11",(2018,10):"2018-11-14",(2018,11):"2018-12-12",(2018,12):"2019-01-11",
 (2019,1):"2019-02-13",(2019,2):"2019-03-12",(2019,3):"2019-04-10",(2019,4):"2019-05-10",(2019,5):"2019-06-12",(2019,6):"2019-07-11",
 (2019,7):"2019-08-13",(2019,8):"2019-09-12",(2019,9):"2019-10-10",(2019,10):"2019-11-13",(2019,11):"2019-12-11",(2019,12):"2020-01-14",
 (2020,1):"2020-02-13",(2020,2):"2020-03-11",(2020,3):"2020-04-10",(2020,4):"2020-05-12",(2020,5):"2020-06-10",(2020,6):"2020-07-14",
 (2020,7):"2020-08-12",(2020,8):"2020-09-11",(2020,9):"2020-10-13",(2020,10):"2020-11-12",(2020,11):"2020-12-10",(2020,12):"2021-01-13",
 (2021,1):"2021-02-10",(2021,2):"2021-03-10",(2021,3):"2021-04-13",(2021,4):"2021-05-12",(2021,5):"2021-06-10",(2021,6):"2021-07-13",
 (2021,7):"2021-08-11",(2021,8):"2021-09-14",(2021,9):"2021-10-13",(2021,10):"2021-11-10",(2021,11):"2021-12-10",(2021,12):"2022-01-12",
 (2022,1):"2022-02-10",(2022,2):"2022-03-10",(2022,3):"2022-04-12",(2022,4):"2022-05-11",(2022,5):"2022-06-10",(2022,6):"2022-07-13",
 (2022,7):"2022-08-10",(2022,8):"2022-09-13",(2022,9):"2022-10-13",(2022,10):"2022-11-10",(2022,11):"2022-12-13",(2022,12):"2023-01-12",
 (2023,1):"2023-02-14",(2023,2):"2023-03-14",(2023,3):"2023-04-12",(2023,4):"2023-05-10",(2023,5):"2023-06-13",(2023,6):"2023-07-12",
 (2023,7):"2023-08-10",(2023,8):"2023-09-13",(2023,9):"2023-10-12",(2023,10):"2023-11-14",(2023,11):"2023-12-12",(2023,12):"2024-01-11",
 (2024,1):"2024-02-13",(2024,2):"2024-03-12",(2024,3):"2024-04-10",(2024,4):"2024-05-15",(2024,5):"2024-06-12",(2024,6):"2024-07-11",
 (2024,7):"2024-08-14",(2024,8):"2024-09-11",(2024,9):"2024-10-10",(2024,10):"2024-11-13",(2024,11):"2024-12-11",(2024,12):"2025-01-15",
 (2025,1):"2025-02-12",(2025,2):"2025-03-12",(2025,3):"2025-04-10",(2025,4):"2025-05-13",(2025,5):"2025-06-11",(2025,6):"2025-07-15",
 (2025,7):"2025-08-12",(2025,8):"2025-09-11",(2025,9):"2025-10-24",(2025,11):"2025-12-18",(2025,12):"2026-01-13",
 (2026,1):"2026-02-13",(2026,2):"2026-03-11",(2026,3):"2026-04-10",(2026,4):"2026-05-12",(2026,5):"2026-06-10",(2026,6):"2026-07-14",
 (2026,7):"2026-08-12",(2026,8):"2026-09-11",(2026,9):"2026-10-14",(2026,10):"2026-11-10",(2026,11):"2026-12-10",(2026,12):"2027-01-13",
 (2027,1):"2027-02-11",(2027,2):"2027-03-10",(2027,3):"2027-04-13",(2027,4):"2027-05-12",(2027,5):"2027-06-10",(2027,6):"2027-07-14",
 (2027,7):"2027-08-11",(2027,8):"2027-09-14",(2027,9):"2027-10-14",(2027,10):"2027-11-10",(2027,11):"2027-12-10",
}
cpi_notes = {
    (2025,9): ("Delayed by Oct 1-Nov 12 2025 shutdown; originally scheduled Oct 15 2025; BLS recalled staff to publish for Social Security COLA",
               CPI_ARCH + " ; https://www.scotsmanguide.com/news/bls-recalls-workers-to-publish-september-cpi-report-but-thats-it/"),
    (2025,11): ("Delayed by 2025 shutdown; originally scheduled Dec 10 2025; omits 1-month changes because October data were not collected", CPI_ARCH + " ; " + BLS_LAPSE),
    (2026,1): ("Delayed by Jan 31-Feb 3 2026 partial shutdown; originally scheduled Feb 11 2026", CPI_ARCH + " ; " + BLS_LAPSE),
}
for (ry, rm), d in sorted(cpi.items(), key=lambda kv: kv[1]):
    label = f"CPI for {MONTHS[rm-1]} {ry}"
    if (ry, rm) in cpi_notes:
        note, src = cpi_notes[(ry, rm)]
    else:
        note = ""
        dd = date.fromisoformat(d)
        if dd > date(2026,10,25):
            note = "future; BLS published schedule"
            src = BLS2027 if dd.year == 2027 else CPI_SCHED
        else:
            src = CPI_ARCH
    add(d, "cpi_release", label, True, note, src)
# cancelled October 2025 CPI (originally scheduled date retained so it can be flagged/excluded)
add("2025-11-13", "cpi_release", "CPI for October 2025 - CANCELLED (not published)", True,
    "CANCELLED: scheduled release did not occur; BLS could not collect October 2025 data during the lapse in appropriations and never published an October 2025 CPI",
    BLS_LAPSE + " ; " + CPI_ARCH)

# ---------------------------------------------------------------------------
# 3. Employment Situation (jobs report)
# ---------------------------------------------------------------------------
EMP_ARCH = "https://www.bls.gov/bls/news-release/empsit.htm"
EMP_SCHED = "https://www.bls.gov/schedule/news_release/empsit.htm"
jobs = {
 (2015,1):"2015-02-06",(2015,2):"2015-03-06",(2015,3):"2015-04-03",(2015,4):"2015-05-08",(2015,5):"2015-06-05",(2015,6):"2015-07-02",
 (2015,7):"2015-08-07",(2015,8):"2015-09-04",(2015,9):"2015-10-02",(2015,10):"2015-11-06",(2015,11):"2015-12-04",(2015,12):"2016-01-08",
 (2016,1):"2016-02-05",(2016,2):"2016-03-04",(2016,3):"2016-04-01",(2016,4):"2016-05-06",(2016,5):"2016-06-03",(2016,6):"2016-07-08",
 (2016,7):"2016-08-05",(2016,8):"2016-09-02",(2016,9):"2016-10-07",(2016,10):"2016-11-04",(2016,11):"2016-12-02",(2016,12):"2017-01-06",
 (2017,1):"2017-02-03",(2017,2):"2017-03-10",(2017,3):"2017-04-07",(2017,4):"2017-05-05",(2017,5):"2017-06-02",(2017,6):"2017-07-07",
 (2017,7):"2017-08-04",(2017,8):"2017-09-01",(2017,9):"2017-10-06",(2017,10):"2017-11-03",(2017,11):"2017-12-08",(2017,12):"2018-01-05",
 (2018,1):"2018-02-02",(2018,2):"2018-03-09",(2018,3):"2018-04-06",(2018,4):"2018-05-04",(2018,5):"2018-06-01",(2018,6):"2018-07-06",
 (2018,7):"2018-08-03",(2018,8):"2018-09-07",(2018,9):"2018-10-05",(2018,10):"2018-11-02",(2018,11):"2018-12-07",(2018,12):"2019-01-04",
 (2019,1):"2019-02-01",(2019,2):"2019-03-08",(2019,3):"2019-04-05",(2019,4):"2019-05-03",(2019,5):"2019-06-07",(2019,6):"2019-07-05",
 (2019,7):"2019-08-02",(2019,8):"2019-09-06",(2019,9):"2019-10-04",(2019,10):"2019-11-01",(2019,11):"2019-12-06",(2019,12):"2020-01-10",
 (2020,1):"2020-02-07",(2020,2):"2020-03-06",(2020,3):"2020-04-03",(2020,4):"2020-05-08",(2020,5):"2020-06-05",(2020,6):"2020-07-02",
 (2020,7):"2020-08-07",(2020,8):"2020-09-04",(2020,9):"2020-10-02",(2020,10):"2020-11-06",(2020,11):"2020-12-04",(2020,12):"2021-01-08",
 (2021,1):"2021-02-05",(2021,2):"2021-03-05",(2021,3):"2021-04-02",(2021,4):"2021-05-07",(2021,5):"2021-06-04",(2021,6):"2021-07-02",
 (2021,7):"2021-08-06",(2021,8):"2021-09-03",(2021,9):"2021-10-08",(2021,10):"2021-11-05",(2021,11):"2021-12-03",(2021,12):"2022-01-07",
 (2022,1):"2022-02-04",(2022,2):"2022-03-04",(2022,3):"2022-04-01",(2022,4):"2022-05-06",(2022,5):"2022-06-03",(2022,6):"2022-07-08",
 (2022,7):"2022-08-05",(2022,8):"2022-09-02",(2022,9):"2022-10-07",(2022,10):"2022-11-04",(2022,11):"2022-12-02",(2022,12):"2023-01-06",
 (2023,1):"2023-02-03",(2023,2):"2023-03-10",(2023,3):"2023-04-07",(2023,4):"2023-05-05",(2023,5):"2023-06-02",(2023,6):"2023-07-07",
 (2023,7):"2023-08-04",(2023,8):"2023-09-01",(2023,9):"2023-10-06",(2023,10):"2023-11-03",(2023,11):"2023-12-08",(2023,12):"2024-01-05",
 (2024,1):"2024-02-02",(2024,2):"2024-03-08",(2024,3):"2024-04-05",(2024,4):"2024-05-03",(2024,5):"2024-06-07",(2024,6):"2024-07-05",
 (2024,7):"2024-08-02",(2024,8):"2024-09-06",(2024,9):"2024-10-04",(2024,10):"2024-11-01",(2024,11):"2024-12-06",(2024,12):"2025-01-10",
 (2025,1):"2025-02-07",(2025,2):"2025-03-07",(2025,3):"2025-04-04",(2025,4):"2025-05-02",(2025,5):"2025-06-06",(2025,6):"2025-07-03",
 (2025,7):"2025-08-01",(2025,8):"2025-09-05",(2025,9):"2025-11-20",(2025,11):"2025-12-16",(2025,12):"2026-01-09",
 (2026,1):"2026-02-11",(2026,2):"2026-03-06",(2026,3):"2026-04-03",(2026,4):"2026-05-08",(2026,5):"2026-06-05",(2026,6):"2026-07-02",
 (2026,7):"2026-08-07",(2026,8):"2026-09-04",(2026,9):"2026-10-02",(2026,10):"2026-11-06",(2026,11):"2026-12-04",(2026,12):"2027-01-08",
 (2027,1):"2027-02-05",(2027,2):"2027-03-05",(2027,3):"2027-04-02",(2027,4):"2027-05-07",(2027,5):"2027-06-04",(2027,6):"2027-07-02",
 (2027,7):"2027-08-06",(2027,8):"2027-09-03",(2027,9):"2027-10-08",(2027,10):"2027-11-05",(2027,11):"2027-12-03",
}
jobs_notes = {
    (2015,6): ("Released Thursday because July 3 was the observed Independence Day holiday", EMP_ARCH),
    (2020,6): ("Released Thursday because July 3 was the observed Independence Day holiday", EMP_ARCH),
    (2021,6): ("Released Friday July 2", EMP_ARCH),
    (2025,6): ("Released Thursday July 3 (July 4 holiday)", EMP_ARCH),
    (2025,9): ("Delayed by Oct 1-Nov 12 2025 shutdown; originally scheduled Oct 3 2025", EMP_ARCH + " ; " + BLS_LAPSE),
    (2025,11): ("Delayed by 2025 shutdown; originally scheduled Dec 5 2025; also carried October 2025 establishment (payroll) data; October household survey data never collected", EMP_ARCH + " ; " + BLS_LAPSE),
    (2026,1): ("Delayed by Jan 31-Feb 3 2026 partial shutdown; originally scheduled Feb 6 2026", EMP_ARCH + " ; " + BLS_LAPSE),
    (2026,6): ("Thursday release (July 3 observed holiday)", EMP_ARCH),
}
for (ry, rm), d in sorted(jobs.items(), key=lambda kv: kv[1]):
    label = f"Jobs report for {MONTHS[rm-1]} {ry}"
    if (ry, rm) in jobs_notes:
        note, src = jobs_notes[(ry, rm)]
    else:
        note = ""
        dd = date.fromisoformat(d)
        if dd > date(2026,10,25):
            note = "future; BLS published schedule"
            src = BLS2027 if dd.year == 2027 else EMP_SCHED
        else:
            src = EMP_ARCH
    add(d, "jobs_report", label, True, note, src)
add("2025-11-07", "jobs_report", "Jobs report for October 2025 - CANCELLED (not published)", True,
    "CANCELLED: scheduled release did not occur; BLS did not publish an October 2025 Employment Situation; October payroll data folded into the Dec 16 2025 release",
    BLS_LAPSE + " ; " + EMP_ARCH)

# ---------------------------------------------------------------------------
# 4. Elections
# ---------------------------------------------------------------------------
add("2016-02-01", "election", "Iowa caucuses (2016 primary season opens)", True,
    "First nominating contest of 2016; Cruz (R) and Clinton (D) wins", "https://www.wgbh.org/news/2016-02-02/6-headlines-that-tell-the-story-of-the-iowa-caucus-results")
add("2016-02-09", "election", "New Hampshire primary (2016)", True,
    "Trump (R) and Sanders (D) wins", "https://abc7chicago.com/politics/trump-sanders-win-new-hampshire-primaries/1193068/")
add("2016-11-08", "election", "General election (presidential)", True,
    "Trump defeats Clinton; Election Day", "https://results.vote.wa.gov/results/20161108/Federal.html")
add("2017-01-20", "election", "Presidential inauguration (Trump, 58th)", True, "", "https://www.inaugural.senate.gov/past-inaugural-ceremonies")
add("2018-11-06", "election", "General election (midterm)", True,
    "Democrats take House", "https://www.fec.gov/documents/2705/federalelections2018.pdf")
add("2020-02-03", "election", "Iowa caucuses (2020 primary season opens)", True,
    "Democratic caucus results delayed by app failure", "https://www.wqad.com/article/news/politics/heres-when-every-states-presidential-primary-or-caucus-will-be-held/526-3a7dd84d-a833-4c17-9d59-595474df40c2")
add("2020-02-11", "election", "New Hampshire primary (2020)", True,
    "Sanders (D) win", "https://lib.dogonews.com/2020/2/12/vermont-senator-bernie-sanders-ekes-out-a-narrow-victory-in-new-hampshire-primary")
add("2020-11-03", "election", "General election (presidential)", True,
    "Biden defeats Trump; result called Nov 7", "https://www.fec.gov/documents/4227/federalelections2020.pdf")
add("2021-01-20", "election", "Presidential inauguration (Biden, 59th)", True, "", "https://www.inaugural.senate.gov/past-inaugural-ceremonies")
add("2022-11-08", "election", "General election (midterm)", True,
    "Republicans narrowly take House", "https://www.fec.gov/documents/5675/federalelections2022.pdf")
add("2024-01-15", "election", "Iowa Republican caucuses (2024 primary season opens)", True,
    "Trump win; Democrats did not hold a competitive Iowa contest in 2024", "https://www.nhpr.org/2024-01-15/iowa-caucuses-ap-makes-call-for-trump-win-with-desantis-in-second")
add("2024-01-23", "election", "New Hampshire primary (2024)", True,
    "Trump (R) win; Biden write-in (D)", "https://www.dover.nh.gov/government/open-government/election-information/previous-elections/2024-presidential-primary/")
add("2024-11-05", "election", "General election (presidential)", True,
    "Trump defeats Harris", "https://www.fec.gov/updates/election-day-is-tuesday-november-5")
add("2025-01-20", "election", "Presidential inauguration (Trump, 60th)", True, "", "https://www.inaugural.senate.gov/past-inaugural-ceremonies")
add("2026-11-03", "election", "General election (midterm)", True,
    "future; next regularly scheduled federal general election", "https://www.fec.gov/introduction-campaign-finance/election-and-voting-information")

# ---------------------------------------------------------------------------
# 5. State of the Union / joint-session addresses
# ---------------------------------------------------------------------------
GOVINFO_SOTU = "https://www.govinfo.gov/features/state-of-the-union"
sotu = [
    ("2015-01-20", "State of the Union (Obama)", ""),
    ("2016-01-12", "State of the Union (Obama)", "Obama's final SOTU"),
    ("2017-02-28", "Address to joint session of Congress (Trump)", "First-year address; not formally a SOTU"),
    ("2018-01-30", "State of the Union (Trump)", ""),
    ("2019-02-05", "State of the Union (Trump)", "Postponed from Jan 29 by the Dec 2018-Jan 2019 shutdown"),
    ("2020-02-04", "State of the Union (Trump)", "Day after Iowa caucuses; day before Senate impeachment acquittal"),
    ("2021-04-28", "Address to joint session of Congress (Biden)", "First-year address; not formally a SOTU"),
    ("2022-03-01", "State of the Union (Biden)", "Days after Russia's invasion of Ukraine"),
    ("2023-02-07", "State of the Union (Biden)", ""),
    ("2024-03-07", "State of the Union (Biden)", ""),
    ("2025-03-04", "Address to joint session of Congress (Trump)", "First-year address; not formally a SOTU"),
    ("2026-02-24", "State of the Union (Trump)", "Delivered during DHS-only partial shutdown; longest SOTU on record"),
]
for d, label, note in sotu:
    add(d, "state_of_union", label, True, note, GOVINFO_SOTU)

# ---------------------------------------------------------------------------
# 6. Supreme Court: term-end opinion days + notable single decision days
# ---------------------------------------------------------------------------
SC = "https://www.supremecourt.gov/opinions/slipopinion/"
term_end = [
    ("2015-06-29", "SCOTUS final opinions of term (OT2014)", "Glossip v. Gross; Arizona State Legislature v. AIRC; Michigan v. EPA",
     "https://constitutioncenter.org/blog/supreme-court-down-to-final-three-decisions-on-monday"),
    ("2016-06-27", "SCOTUS final opinions of term (OT2015)", "Whole Woman's Health v. Hellerstedt; McDonnell v. United States; Voisine",
     "https://fedsoc.org/commentary/podcasts/supreme-court-concludes-2015-term-podcast"),
    ("2017-06-26", "SCOTUS final opinions of term (OT2016)", "Trinity Lutheran; travel-ban cert grant/partial stay; Pavan v. Smith",
     "https://blogs.kentlaw.iit.edu/iscotus/week-june-26-2017-court-end-term/"),
    ("2018-06-27", "SCOTUS final opinions of term (OT2017)", "Janus v. AFSCME; Florida v. Georgia; Kennedy retirement announced same day. Three per curiam clean-up opinions issued Jun 28",
     SC + "17"),
    ("2019-06-27", "SCOTUS final opinions of term (OT2018)", "Rucho v. Common Cause; Department of Commerce v. New York (census); Mitchell v. Wisconsin",
     SC + "18"),
    ("2020-07-09", "SCOTUS final opinions of term (OT2019)", "Trump v. Vance; Trump v. Mazars; McGirt v. Oklahoma. Term ran into July due to COVID",
     SC + "19"),
    ("2021-07-01", "SCOTUS final opinions of term (OT2020)", "Brnovich v. DNC; AFP v. Bonta. One per curiam (Dunn v. Reeves) issued Jul 2",
     SC + "20"),
    ("2022-06-30", "SCOTUS final opinions of term (OT2021)", "West Virginia v. EPA; Biden v. Texas",
     SC + "21"),
    ("2023-06-30", "SCOTUS final opinions of term (OT2022)", "Biden v. Nebraska (student loans); 303 Creative v. Elenis",
     SC + "22"),
    ("2024-07-01", "SCOTUS final opinions of term (OT2023)", "Trump v. United States (immunity); Moody v. NetChoice; Corner Post",
     SC + "23"),
    ("2025-06-27", "SCOTUS final opinions of term (OT2024)", "Trump v. CASA (universal injunctions); Mahmoud v. Taylor; FCC v. Consumers' Research. One per curiam (Goldey v. Fields) issued Jun 30",
     SC + "24"),
    ("2026-06-30", "SCOTUS final opinions of term (OT2025)", "Trump v. Barbara (birthright citizenship); West Virginia v. B.P.J.; NRSC v. FEC",
     SC + "25"),
]
for d, label, note, src in term_end:
    add(d, "scotus_term_end", label, True, note, src)

notable = [
    ("2015-06-25", "SCOTUS decision: King v. Burwell (ACA subsidies upheld)", "", "https://en.wikipedia.org/wiki/List_of_United_States_Supreme_Court_cases,_volume_576"),
    ("2015-06-26", "SCOTUS decision: Obergefell v. Hodges (same-sex marriage)", "", "https://en.wikipedia.org/wiki/List_of_United_States_Supreme_Court_cases,_volume_576"),
    ("2018-06-26", "SCOTUS decision: Trump v. Hawaii (travel ban upheld)", "", SC + "17"),
    ("2020-06-15", "SCOTUS decision: Bostock v. Clayton County (Title VII LGBT protection)", "", SC + "19"),
    ("2022-06-23", "SCOTUS decision: NYSRPA v. Bruen (gun carry)", "", SC + "21"),
    ("2022-06-24", "SCOTUS decision: Dobbs v. Jackson (Roe overturned)", "", SC + "21"),
    ("2023-06-29", "SCOTUS decision: SFFA v. Harvard (affirmative action)", "", SC + "22"),
    ("2024-03-04", "SCOTUS decision: Trump v. Anderson (ballot eligibility)", "", SC + "23"),
    ("2025-06-18", "SCOTUS decision: United States v. Skrmetti (gender-affirming care ban upheld)", "", SC + "24"),
    ("2026-02-20", "SCOTUS decision: Learning Resources v. Trump (IEEPA tariffs)", "", SC + "25"),
    ("2026-04-29", "SCOTUS decision: Louisiana v. Callais (Voting Rights Act)", "", SC + "25"),
    ("2026-06-29", "SCOTUS decisions: Trump v. Slaughter (FTC removal); Trump v. Cook (Fed governor)", "", SC + "25"),
]
for d, label, note, src in notable:
    add(d, "scotus_term_end", label, False, note or "Notable single decision day (opinion days are announced only days ahead)", src)

# ---------------------------------------------------------------------------
# 7. Debt ceiling X-dates/resolutions and government shutdowns
# ---------------------------------------------------------------------------
CRS_DL = "https://www.everycrsreport.com/files/20180329_R43389_2faa7753af59b41f58567e243d2544c8cbb88649.html"
CRS_DL22 = "https://www.everycrsreport.com/reports/R43389.html"
CRS_DL25 = "https://www.everycrsreport.com/files/2025-09-11_IN12045_f4898d1d7c03a85a4be548bff4f2bf61873cc374.html"
CRS_GAPS = "https://www.everycrsreport.com/files/2026-05-26_RS20348_d32c007fddd9fa64a4b1794c618da21a86c1e901.html"
debt = [
    # 2015
    ("2015-03-16", "Debt limit reinstated; extraordinary measures begin", True, "Suspension from BBA 2013/Temporary Debt Limit Extension Act lapsed Mar 15 2015; Lew declared a debt issuance suspension period", CRS_DL),
    ("2015-10-15", "Treasury letter: X-date moved up to Nov 3", False, "Lew letter revised exhaustion date from ~Nov 5 to no later than Nov 3 2015", "https://home.treasury.gov/system/files/276/Treasury-Letter-to-Congress-101515.pdf"),
    ("2015-11-02", "Debt limit resolved: Bipartisan Budget Act of 2015 signed", False, "P.L. 114-74 suspended the limit through Mar 15 2017", CRS_DL),
    ("2015-11-03", "Debt limit X-date (Treasury estimate)", True, "Treasury-projected exhaustion date; resolved one day earlier", "https://home.treasury.gov/system/files/276/Treasury-Letter-to-Congress-101515.pdf"),
    # 2017
    ("2017-03-16", "Debt limit reinstated; extraordinary measures begin", True, "Limit reset at $19,809B after BBA 2015 suspension lapsed", CRS_DL),
    ("2017-07-28", "Treasury letter: extraordinary measures last to Sept 29", False, "Mnuchin letter; outside estimates pointed to early October", CRS_DL),
    ("2017-09-08", "Debt limit resolved: P.L. 115-56 signed (Harvey aid/CR)", False, "Suspended the limit through Dec 8 2017; also averted an Oct 1 shutdown", CRS_DL),
    ("2017-09-29", "Debt limit X-date (Treasury estimate)", True, "Mnuchin's stated end of extraordinary measures; resolved Sept 8", CRS_DL),
    ("2017-12-08", "Debt limit suspension expired", True, "Extraordinary measures resumed; new limit $20,456B effective Dec 11 2017", CRS_DL),
    ("2018-02-09", "Debt limit resolved: Bipartisan Budget Act of 2018 signed", False, "P.L. 115-123 suspended the limit through Mar 1 2019; same bill ended a brief overnight funding lapse", CRS_DL),
    # 2019
    ("2019-03-02", "Debt limit reinstated", True, "BBA 2018 suspension expired Mar 1 2019; limit reset at $21.988T; extraordinary measures invoked Mar 4", CRS_DL22),
    ("2019-07-12", "Treasury letter: cash could run out in early September", False, "Mnuchin letter to Pelosi urging action before August recess", "https://home.treasury.gov/system/files/136/DL%20Letter%20to%20Congress%202019_07_12%20Pelosi.pdf"),
    ("2019-08-02", "Debt limit resolved: Bipartisan Budget Act of 2019 signed", False, "P.L. 116-37 suspended the limit through Jul 31 2021", CRS_DL22),
    # 2021
    ("2021-08-01", "Debt limit reinstated", True, "BBA 2019 suspension expired Jul 31 2021; extraordinary measures began Aug 2", CRS_DL22),
    ("2021-09-28", "Treasury letter: X-date Oct 18", False, "Yellen letter to Congress", "https://home.treasury.gov/news/press-releases/jy0377"),
    ("2021-10-14", "Debt limit resolved (short-term): $480B increase signed", False, "P.L. 117-50 (S. 1301)", "https://www.govinfo.gov/content/pkg/PLAW-117publ50/html/PLAW-117publ50.htm"),
    ("2021-10-18", "Debt limit X-date (Treasury estimate)", True, "Treasury-projected exhaustion date; resolved Oct 14", "https://home.treasury.gov/news/press-releases/jy0377"),
    ("2021-11-16", "Treasury letter: X-date Dec 15", False, "Yellen letter to Congress", "https://fraser.stlouisfed.org/files/docs/publications/treaspr/2021/2021-11-16_jy0488.pdf"),
    ("2021-12-15", "Debt limit X-date (Treasury estimate)", True, "Treasury-projected date; Congress cleared $2.5T increase Dec 14-15", "https://fraser.stlouisfed.org/files/docs/publications/treaspr/2021/2021-11-16_jy0488.pdf"),
    ("2021-12-16", "Debt limit resolved: $2.5T increase signed", False, "P.L. 117-73 (S.J. Res. 33); limit to ~$31.4T", "https://www.govinfo.gov/content/pkg/PLAW-117publ73/html/PLAW-117publ73.htm"),
    # 2023
    ("2023-01-19", "Debt limit reached; extraordinary measures begin", True, "Treasury began debt issuance suspension period Jan 19 2023, initially projected through Jun 5", "https://home.treasury.gov/news/press-releases/jy1196"),
    ("2023-05-26", "Treasury letter: X-date June 5", False, "Yellen letter; deal announced May 27", "https://fraser.stlouisfed.org/files/docs/publications/treaspr/2023/2023-05-26_jy1506.pdf"),
    ("2023-06-03", "Debt limit resolved: Fiscal Responsibility Act signed", False, "P.L. 118-5 (H.R. 3746) suspended the limit through Jan 1 2025", "https://bidenwhitehouse.archives.gov/briefing-room/legislation/2023/06/03/press-release-bills-signed-h-r-346-h-r-3746"),
    ("2023-06-05", "Debt limit X-date (Treasury estimate)", True, "Treasury-projected exhaustion date; resolved Jun 3", "https://fraser.stlouisfed.org/files/docs/publications/treaspr/2023/2023-05-26_jy1506.pdf"),
    # 2025
    ("2025-01-02", "Debt limit reinstated at $36.1T", True, "FRA 2023 suspension expired Jan 1 2025", CRS_DL25),
    ("2025-01-21", "Extraordinary measures begin", True, "Per Yellen letter of Jan 17 2025", "https://punchbowl.news/article/finance/economy/janet-yellen-extraordinary-measures-debt-limit/"),
    ("2025-05-09", "Treasury letter: X-date in August", False, "Bessent letter: reasonable probability measures exhausted in August; CBO range mid-Aug to late Sept", "https://fortune.com/2025/05/09/debt-limit-x-date-august-congress-extraordinary-measures-treasury-bonds-default"),
    ("2025-07-04", "Debt limit resolved: reconciliation act (P.L. 119-21) signed", False, "Raised the limit by $5.0T to $41.1T; outside projections put the next binding date in early-to-mid 2027", CRS_DL25 + " ; https://www.everycrsreport.com/files/2026-09-21_IF10292_c2e7be2cbda8c7c7acfafd40d64a2f6fc9b45aa8.html"),
    # shutdowns
    ("2018-01-20", "Government shutdown begins", False, "Funding lapsed at midnight Jan 19 2018 (P.L. 115-96 expired); 2 full days", CRS_GAPS),
    ("2018-01-22", "Government shutdown ends", False, "CR enacted Jan 22 2018", CRS_GAPS),
    ("2018-12-22", "Government shutdown begins (partial)", False, "Funding lapsed at midnight Dec 21 2018; 34 full days; longest to that point", CRS_GAPS),
    ("2019-01-25", "Government shutdown ends", False, "CR enacted Jan 25 2019", CRS_GAPS),
    ("2025-10-01", "Government shutdown begins", False, "FY2026 funding gap began at midnight Sept 30 2025; 42 full days; longest on record (full-government)", CRS_GAPS),
    ("2025-11-12", "Government shutdown ends", False, "CR (P.L. 119-37) signed Nov 12 2025, funding through Jan 30 2026", CRS_GAPS),
    ("2026-01-31", "Partial government shutdown begins", False, "CR expired Jan 30 2026; roughly half of agencies affected; 3 full days", CRS_GAPS + " ; https://www.chds.us/c/timeline/early-2026-government-shutdowns/"),
    ("2026-02-03", "Partial government shutdown ends", False, "P.L. 119-75 enacted Feb 3 2026 (five approps bills + two-week DHS CR)", CRS_GAPS),
    ("2026-02-14", "DHS-only shutdown begins", False, "DHS CR extension expired Feb 13 2026; 75 full days; affected TSA, FEMA, Coast Guard, CBP, ICE", CRS_GAPS + " ; https://www.everycrsreport.com/reports/R48874.html"),
    ("2026-04-30", "DHS-only shutdown ends", False, "DHS appropriations act (P.L. 119-86) signed Apr 30 2026; ICE/CBP funded separately Jun 10 2026 via reconciliation", CRS_GAPS + " ; https://www.everycrsreport.com/reports/R48874.html"),
    ("2026-12-11", "Government funding deadline (FY2027 CR expires)", True, "future; CR (P.L. 119-103) signed Sep 2 2026 runs through Dec 11 2026", "https://spacepolicyonline.com/news/house-clears-fy2027-cr-now-to-the-president/"),
]
for d, label, sch, note, src in debt:
    add(d, "debt_ceiling", label, sch, note, src)

# ---------------------------------------------------------------------------
# 8. Tax day
# ---------------------------------------------------------------------------
tax = [
    ("2015-04-15", "", "https://www.irs.gov/pub/irs-news/IR-15-059.pdf"),
    ("2016-04-18", "Shifted from Apr 15 by DC Emancipation Day (observed Fri Apr 15)", "https://taxfoundation.org/blog/why-are-taxes-due-after-april-15-year/"),
    ("2017-04-18", "Apr 15 was Saturday; Emancipation Day observed Mon Apr 17", "https://www.foxbusiness.com/features/why-the-2017-tax-deadline-was-moved-to-april-18"),
    ("2018-04-18", "Original deadline Apr 17 (Emancipation Day Apr 16); IRS granted one extra day after e-file system outage (IR-2018-100)", "https://www.irs.gov/newsroom/irs-provides-additional-day-to-file-and-pay-for-taxpayers-through-wednesday-april-18-irs-processing-systems-back-online"),
    ("2019-04-15", "", "https://www.irs.gov/newsroom/irs-kicks-off-2019-tax-filing-season-as-tax-agency-reopens-use-irsgov-to-avoid-phone-delays"),
    ("2020-07-15", "COVID extension from Apr 15 to Jul 15 2020 (announced Mar 20-21 2020)", "https://www.irs.gov/node/76741"),
    ("2021-05-17", "COVID-era extension from Apr 15 to May 17 2021 (IR-2021-59)", "https://content.govdelivery.com/accounts/USIRS/bulletins/2c7bb6f?reqfrom=share"),
    ("2022-04-18", "Emancipation Day observed Fri Apr 15", "https://abc10.com/article/news/verify/money-verify/tax-day-deadline-individual-filing-returns-not-extended-2022-currently-april-18/536-43fa1f39-136b-4afb-b45e-7687f0ba6821"),
    ("2023-04-18", "Apr 15 was Saturday; Emancipation Day observed Mon Apr 17", "https://news.yahoo.com/tax-day-april-18-why-154242531.html?fr=sycsrp_catchall"),
    ("2024-04-15", "IR-2024-04", "https://irs.gov/newsroom/2024-tax-filing-season-set-for-january-29-irs-continues-to-make-improvements-to-help-taxpayers"),
    ("2025-04-15", "IRS Jan 10 2025 filing-season release", "https://www.cpapracticeadvisor.com/2025/01/10/2025-filing-season-to-start-jan-27-irs-says/154337/"),
    ("2026-04-15", "IR-2026-02", "https://www.irs.gov/newsroom/irs-announces-first-day-of-2026-filing-season-online-tools-and-resources-help-with-tax-filing"),
    ("2027-04-15", "future; unverified - statutory default (Thursday; no DC holiday conflict); IRS has not yet announced the 2027 filing season", ""),
]
for d, note, src in tax:
    add(d, "tax_day", "Federal individual tax filing deadline", True, note, src)

# ---------------------------------------------------------------------------
# 9. Hurricane season (fixed dates)
# ---------------------------------------------------------------------------
for yr in range(2015, 2028):
    fut = "future; " if yr >= 2027 else ""
    add(f"{yr}-06-01", "hurricane_season", "Atlantic hurricane season begins", True, fut + "fixed date; no verification needed", "")
    add(f"{yr}-11-30", "hurricane_season", "Atlantic hurricane season ends", True, fut + "fixed date; no verification needed", "")

# ---------------------------------------------------------------------------
# write
# ---------------------------------------------------------------------------
rows.sort(key=lambda r: (r["date"], r["category"], r["label"]))
out = "/tmp/claude-0/-home-claude/f5a5ae15-c12e-5110-aba0-6fabf673c207/scratchpad/calendar/catalysts.csv"
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["date","category","label","scheduled","notes","source"], quoting=csv.QUOTE_ALL)
    w.writeheader()
    for r in rows:
        w.writerow(r)

from collections import Counter
c = Counter(r["category"] for r in rows)
print("total rows:", len(rows))
for k, v in sorted(c.items()):
    print(f"  {k}: {v}")
# sanity checks
for r in rows:
    date.fromisoformat(r["date"])
dups = Counter((r["date"], r["category"], r["label"]) for r in rows)
print("duplicates:", [k for k, v in dups.items() if v > 1])
print("unverified:", [(r["date"], r["label"]) for r in rows if "unverified" in r["notes"].lower()])
