"""Market fear: Cboe VIX, from Cboe's public history file. Open access; a Cboe
license is needed before commercial publication. (An S&P 500 drawdown series
needs a licensed feed; the financial stress index covers it for now.)

Codes: 'vix:CLOSE'.
"""
from collectors.sources.tables import collect_files

FILES = {
    "vix": ("https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv", "csv", None),
}


def collect(col, series):
    collect_files(col, series, FILES)
