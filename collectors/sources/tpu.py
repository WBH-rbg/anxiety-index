"""Trade Policy Uncertainty index (Caldara, Iacoviello, Molligo, Prestipino, Raffo). CC BY.

Codes: 'tpu:<column>'.
"""
from collectors.sources.tables import collect_files

FILES = {
    "tpu": ("https://www.matteoiacoviello.com/tpu_files/tpu_web_latest.xlsx", "xlsx", "TPU_MONTHLY"),
}


def collect(col, series):
    collect_files(col, series, FILES)
