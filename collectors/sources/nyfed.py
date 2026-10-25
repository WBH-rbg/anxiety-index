"""Federal Reserve Bank of New York: Survey of Consumer Expectations and the
Global Supply Chain Pressure Index. Business use allowed with attribution.

Codes: 'sce:<column>' and 'gscpi:<column>'. Sheet names and header rows are
confirmed by the first run; adjust FILES if the warning lists other columns.
"""
from collectors.sources.tables import collect_files

FILES = {
    "sce": ("https://www.newyorkfed.org/medialibrary/interactives/sce/sce/downloads/data/frbny-sce-data.xlsx", "xlsx", "Inflation expectations", {"skiprows": 3}),
    "sce_labor": ("https://www.newyorkfed.org/medialibrary/interactives/sce/sce/downloads/data/frbny-sce-data.xlsx", "xlsx", "Labor market expectations", {"skiprows": 3}),
    "gscpi": ("https://www.newyorkfed.org/medialibrary/research/interactives/gscpi/downloads/gscpi_data.xlsx", "xlsx", "GSCPI Monthly Data", {"header": None}),
}


def collect(col, series):
    collect_files(col, series, FILES)
