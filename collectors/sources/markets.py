"""Market fear and drawdowns: Cboe VIX (Cboe's public history file) and the S&P 500
(Stooq daily history). Open access; both need licenses before commercial publication.

Codes: 'vix:CLOSE', 'spx:Close'.
"""
from collectors.sources.tables import collect_files

FILES = {
    "vix": ("https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv", "csv", None),
    "spx": ("https://stooq.com/q/d/l/?s=^spx&i=d", "csv", None),
}


def collect(col, series):
    collect_files(col, series, FILES)
