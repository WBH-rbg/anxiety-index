"""Geopolitical Risk Index (Caldara and Iacoviello), monthly and daily. License: CC BY.

Catalog codes are '<file>:<column>', e.g. 'monthly:GPR' or 'daily:GPRD'.
"""
from collectors.sources.tables import collect_files

FILES = {
    "monthly": ("https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xls", "xls", 0),
    "daily": ("https://www.matteoiacoviello.com/gpr_files/data_gpr_daily_recent.xls", "xls", 0),
}


def collect(col, series):
    collect_files(col, series, FILES)
