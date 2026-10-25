"""University of Michigan Surveys of Consumers: sentiment and inflation expectations.
Open data tables; CC BY-NC-ND, so a license is needed before commercial publication.

Codes: 'ics:ICS', 'px:PX_MD' (1-year expected inflation, median), 'px:PX5_MD' (5-year).
Files have Month, Year columns.
"""
from collectors.sources.tables import collect_files

FILES = {
    "ics": ("https://www.sca.isr.umich.edu/files/tbmics.csv", "csv", None),
    "px": ("https://www.sca.isr.umich.edu/files/tbmpx1px5.csv", "csv", None),
}


def collect(col, series):
    collect_files(col, series, FILES)
