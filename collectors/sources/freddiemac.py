"""Freddie Mac Primary Mortgage Market Survey: weekly 30-year and 15-year fixed rates since 1971.

Codes: 'pmms:pmms30', 'pmms:pmms15'.
"""
from collectors.sources.tables import collect_files

FILES = {
    "pmms": ("https://www.freddiemac.com/pmms/docs/PMMS_history.csv", "csv", None),
}


def collect(col, series):
    collect_files(col, series, FILES)
