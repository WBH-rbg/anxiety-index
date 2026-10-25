"""Economic Policy Uncertainty Index (Baker, Bloom and Davis): US monthly, daily, and by category.

Catalog codes are '<file>:<column>', e.g. 'monthly:Three_Component_Index'.
"""
from collectors.sources.tables import collect_files

FILES = {
    "monthly": ("https://www.policyuncertainty.com/media/US_Policy_Uncertainty_Data.xlsx", "xlsx", 0),
    "daily": ("https://www.policyuncertainty.com/media/All_Daily_Policy_Data.csv", "csv", None),
    "categorical": ("https://www.policyuncertainty.com/media/Categorical_EPU_Data.xlsx", "xlsx", 0),
}


def collect(col, series):
    collect_files(col, series, FILES)
