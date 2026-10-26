"""Outlook: a simple, honest statistical forecast of the headline 1 to 8 weeks ahead.

The index is a smoothed percentile, so the hardest benchmark to beat is "it stays where it
is" (persistence). The model here is deliberately small and explainable:

    expected change over h weeks = half-weight on a ridge regression of past h-week changes
    on (a) the current level and recent momentum and (b) the six dimension readings and their
    four-week changes, plus half-weight on no change.

It is refit every year on data up to that year in the backtest (no look-ahead), and the
prediction intervals are the empirical quantiles of its backtest errors, so they are as wide
as the model's actual track record says they should be. The backtest table is published with
every forecast; if the model ever stops beating persistence, the table will show it.

What the model learns is interpretable and matches the thesis: readings well above normal ease
back; anxiety driven by shocks (safety, geopolitics, disasters) fades faster than anxiety driven
by background pressure (cost of living, politics), which persists.

Outputs: output/forecast.md, output/forecast.csv, output/forecast_backtest.csv, and rows
appended to ai_index.forecasts (so forecasts can be scored later against what happened).
"""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

from index.run import DIM_LABELS, OUT, PROJECT_ID
from index.validate import naive

HORIZONS = [1, 2, 4, 8]
BACKTEST_START = 2010
FIT_START = pd.Timestamp("2003-01-01")   # skip the first years, where few signals have history
RIDGE_LAMBDA = 50.0
MODEL_WEIGHT = 0.5                        # half-weight on the model, half on persistence
DIMS = ["cost_of_living", "jobs_financial", "political_institutional", "safety_unrest", "geopolitical", "disasters_health"]
BAND_EDGES = [-1, 20, 50, 80, 95, 101]
BAND_NAMES = ["Low", "Moderate", "Elevated", "High", "Severe"]
GROUPS = {
    "level": ["score", "chg1", "chg4", "chg13", "ma13", "maxdim", "n_hot"],
    "shock": ["safety_unrest", "geopolitical", "disasters_health", "safety_unrest_c4", "geopolitical_c4", "disasters_health_c4"],
    "background": ["cost_of_living", "jobs_financial", "political_institutional", "cost_of_living_c4", "jobs_financial_c4", "political_institutional_c4"],
}
GROUP_TEXT = {
    "level": "Where the reading sits relative to normal, and its recent momentum",
    "shock": "How much of it is shock-driven (safety, geopolitics, disasters), which fades faster",
    "background": "How much of it is background pressure (cost of living, jobs, politics), which persists",
}


def load(client):
    head = client.query("SELECT week, score FROM `ai_index.headline_weekly` WHERE score IS NOT NULL ORDER BY week").to_dataframe()
    head["week"] = naive(head["week"])
    dims = client.query("SELECT week, dimension, score FROM `ai_index.dimension_weekly` WHERE score IS NOT NULL").to_dataframe()
    dims["week"] = naive(dims["week"])
    d = dims.pivot(index="week", columns="dimension", values="score")
    frame = head.set_index("week")[["score"]].join(d, how="left")
    return frame


def features(frame: pd.DataFrame) -> pd.DataFrame:
    s = frame["score"]
    X = pd.DataFrame({"score": s, "chg1": s.diff(), "chg4": s.diff(4), "chg13": s.diff(13), "ma13": s.rolling(13).mean() - s})
    for c in DIMS:
        col = frame[c] if c in frame.columns else pd.Series(np.nan, index=frame.index)
        X[c] = col
        X[c + "_c4"] = col.diff(4)
    present = [c for c in DIMS if c in frame.columns]
    X["maxdim"] = frame[present].max(axis=1)
    X["n_hot"] = (frame[present] > 80).sum(axis=1)
    return X


def ridge(A: np.ndarray, y: np.ndarray, lam: float) -> np.ndarray:
    A1 = np.c_[np.ones(len(A)), A]
    I = np.eye(A1.shape[1])
    I[0, 0] = 0
    return np.linalg.solve(A1.T @ A1 + lam * I, A1.T @ y)


class Model:
    def __init__(self, train: pd.DataFrame, y: pd.Series):
        self.cols = list(train.columns)
        self.mu = train.mean()
        self.sd = train.std().replace(0, 1)
        self.beta = ridge(((train - self.mu) / self.sd).values, y.values, RIDGE_LAMBDA)

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        Z = ((X[self.cols] - self.mu) / self.sd).values
        return MODEL_WEIGHT * (np.c_[np.ones(len(Z)), Z] @ self.beta)

    def contributions(self, x: pd.Series) -> pd.Series:
        z = ((x[self.cols] - self.mu) / self.sd).values
        return pd.Series(MODEL_WEIGHT * self.beta[1:] * z, index=self.cols)


def backtest(X: pd.DataFrame, s: pd.Series) -> tuple[pd.DataFrame, dict[int, pd.DataFrame]]:
    """Yearly-refit, expanding-window backtest from BACKTEST_START. Returns a metrics table and per-horizon residuals."""
    metrics, resid = [], {}
    for h in HORIZONS:
        D = X.copy()
        D["y"] = s.shift(-h) - s
        D = D.dropna()
        D = D[D.index >= FIT_START]
        preds, acts, idx = [], [], []
        for yr in sorted(set(D.index.year)):
            if yr < BACKTEST_START:
                continue
            tr, te = D[D.index.year < yr], D[D.index.year == yr]
            if len(tr) < 104 or te.empty:
                continue
            m = Model(tr.drop(columns="y"), tr["y"])
            preds += list(m.predict(te.drop(columns="y")))
            acts += list(te["y"].values)
            idx += list(te.index)
        p, a = np.array(preds), np.array(acts)
        r = pd.DataFrame({"origin": idx, "predicted_change": p, "actual_change": a})
        r["error"] = r["predicted_change"] - r["actual_change"]
        resid[h] = r
        # mean reversion alone, for comparison: AR(1) fitted on the same expanding windows is close to
        # the level-only part of the model; report persistence and the climatological mean instead
        confident = np.abs(p) >= np.quantile(np.abs(p), 0.75)
        nz = a != 0
        metrics.append({
            "horizon_weeks": h, "weeks": len(a),
            "mae_persistence": round(float(np.abs(a).mean()), 2),
            "mae_model": round(float(np.abs(p - a).mean()), 2),
            "improvement_pct": round(100 * (1 - np.abs(p - a).mean() / np.abs(a).mean()), 1),
            "direction_right_pct": round(100 * float((np.sign(p) == np.sign(a))[nz].mean()), 0),
            "direction_right_when_confident_pct": round(100 * float((np.sign(p) == np.sign(a))[confident & nz].mean()), 0),
            "share_rose_5plus_pct": round(100 * float((a >= 5).mean()), 0),
            "share_fell_5plus_pct": round(100 * float((a <= -5).mean()), 0),
        })
    return pd.DataFrame(metrics), resid


def from_here(s: pd.Series) -> pd.DataFrame:
    """What has usually happened next from each band, 2010 onward."""
    bands = pd.cut(s, BAND_EDGES, labels=BAND_NAMES)
    rows = []
    for h in [2, 4, 8]:
        t = pd.DataFrame({"band": bands, "now": s, "fut": s.shift(-h)}).dropna()
        t = t[t.index.year >= BACKTEST_START]
        for b, g in t.groupby("band", observed=True):
            rows.append({"band": b, "horizon_weeks": h, "weeks": len(g), "mean_now": round(g["now"].mean(), 1), "mean_later": round(g["fut"].mean(), 1),
                         "higher_5plus_pct": round(100 * (g["fut"] > g["now"] + 5).mean(), 0), "lower_5plus_pct": round(100 * (g["fut"] < g["now"] - 5).mean(), 0),
                         "high_or_severe_pct": round(100 * (g["fut"] >= 80).mean(), 0), "below_50_pct": round(100 * (g["fut"] < 50).mean(), 0)})
    return pd.DataFrame(rows)


def band_of(p: float) -> str:
    for edge, name in zip(BAND_EDGES[1:], BAND_NAMES):
        if p <= edge:
            return name
    return BAND_NAMES[-1]


def outlook(X: pd.DataFrame, s: pd.Series, resid: dict[int, pd.DataFrame]) -> tuple[pd.DataFrame, dict[int, pd.Series]]:
    last = s.index.max()
    x_now = X.loc[last]
    rows, contribs = [], {}
    for h in HORIZONS:
        D = X.copy()
        D["y"] = s.shift(-h) - s
        D = D.dropna()
        D = D[D.index >= FIT_START]
        m = Model(D.drop(columns="y"), D["y"])
        change = float(m.predict(x_now.to_frame().T)[0])
        contribs[h] = m.contributions(x_now)
        e = resid[h]["error"].values
        q = np.quantile(e, [0.10, 0.25, 0.75, 0.90])
        central = float(np.clip(s.loc[last] + change, 0, 100))
        rows.append({"origin_week": last, "horizon_weeks": h, "target_week": last + pd.Timedelta(weeks=h),
                     "current": float(s.loc[last]), "central": round(central, 1), "band": band_of(central),
                     "lo50": round(float(np.clip(central - q[2], 0, 100)), 1), "hi50": round(float(np.clip(central - q[1], 0, 100)), 1),
                     "lo80": round(float(np.clip(central - q[3], 0, 100)), 1), "hi80": round(float(np.clip(central - q[0], 0, 100)), 1),
                     "p_higher_5plus": round(float((change - e >= 5).mean()), 2), "p_lower_5plus": round(float((change - e <= -5).mean()), 2),
                     "p_high_or_severe": round(float((s.loc[last] + change - e >= 80).mean()), 2),
                     "p_below_50": round(float((s.loc[last] + change - e < 50).mean()), 2)})
    return pd.DataFrame(rows), contribs


def report(fc: pd.DataFrame, contribs: dict[int, pd.Series], metrics: pd.DataFrame, fh: pd.DataFrame) -> str:
    last = fc["origin_week"].iloc[0]
    cur = fc["current"].iloc[0]
    L = [f"# Outlook from the week ending {last.date()}", "",
         f"Current reading: **{cur:.0f} ({band_of(cur)})**. The table shows where a small statistical model expects the headline to be, with ranges taken from the model's own historical errors. Treat it as tendency, not prediction: at these horizons the model beats \"no change\" only modestly (see the track record below), and scheduled catalysts in `lookahead.md` can override any of it.", "",
         "| Weeks ahead | Week ending | Expected | 50% range | 80% range | Chance up 5+ | Chance down 5+ | Chance High or Severe | Chance below 50 |",
         "|---|---|---|---|---|---|---|---|---|"]
    for _, r in fc.iterrows():
        L.append(f"| {r['horizon_weeks']} | {r['target_week'].date()} | {r['central']:.0f} ({r['band']}) | {r['lo50']:.0f}–{r['hi50']:.0f} | {r['lo80']:.0f}–{r['hi80']:.0f} | "
                 f"{100*r['p_higher_5plus']:.0f}% | {100*r['p_lower_5plus']:.0f}% | {100*r['p_high_or_severe']:.0f}% | {100*r['p_below_50']:.0f}% |")
    c4 = contribs[4]
    L += ["", "## Why (four-week horizon)", "", "Expected change in points, by what is driving it:", ""]
    for g, cols in GROUPS.items():
        v = c4.reindex(cols).fillna(0).sum()
        L.append(f"- {GROUP_TEXT[g]}: **{v:+.1f}**")
    top = c4.abs().sort_values(ascending=False).head(4).index
    names = {"score": "the headline level", "chg1": "last week's move", "chg4": "the four-week move", "chg13": "the quarter's move", "ma13": "distance from the 13-week average",
             "maxdim": "the hottest dimension", "n_hot": "the number of dimensions above 80"}
    names.update({d: DIM_LABELS.get(d, d).lower() + " reading" for d in DIMS})
    names.update({d + "_c4": DIM_LABELS.get(d, d).lower() + " four-week change" for d in DIMS})
    L += ["", "Largest single factors: " + "; ".join(f"{names.get(k, k)} ({c4[k]:+.1f})" for k in top) + ".", ""]
    L += ["## What has usually happened from here", "", f"Weeks since {BACKTEST_START} that showed the same band, and where the headline was afterwards:", "",
          "| Band now | Weeks ahead | Weeks | Average then | Average later | Higher by 5+ | Lower by 5+ | High or Severe later | Below 50 later |", "|---|---|---|---|---|---|---|---|---|"]
    cur_band = band_of(cur)
    for _, r in fh.iterrows():
        mark = "**" if r["band"] == cur_band else ""
        L.append(f"| {mark}{r['band']}{mark} | {r['horizon_weeks']} | {r['weeks']} | {r['mean_now']} | {r['mean_later']} | {r['higher_5plus_pct']:.0f}% | {r['lower_5plus_pct']:.0f}% | {r['high_or_severe_pct']:.0f}% | {r['below_50_pct']:.0f}% |")
    L += ["", "## Track record (yearly-refit backtest, no look-ahead)", "",
          f"Mean absolute error in percentile points, {BACKTEST_START} onward. \"Persistence\" is the forecast that nothing changes.", "",
          "| Weeks ahead | Weeks tested | Persistence error | Model error | Improvement | Direction right | Direction right when confident | Weeks that rose 5+ | Weeks that fell 5+ |", "|---|---|---|---|---|---|---|---|---|"]
    for _, r in metrics.iterrows():
        L.append(f"| {r['horizon_weeks']} | {r['weeks']} | {r['mae_persistence']} | {r['mae_model']} | {r['improvement_pct']:+.0f}% | {r['direction_right_pct']:.0f}% | {r['direction_right_when_confident_pct']:.0f}% | {r['share_rose_5plus_pct']:.0f}% | {r['share_fell_5plus_pct']:.0f}% |")
    L += ["", "How to read this: the index is persistent, so the best one- or two-week forecast is close to the current reading. The model's edge grows with the horizon because it knows two things persistence doesn't: readings far above normal ease back, and anxiety driven by shocks fades faster than anxiety driven by background pressure. \"Confident\" means the quarter of weeks where the model expected the largest moves.",
          "", "The model is half-weight ridge regression on the current level, recent momentum, and the six dimension readings with their four-week changes; it is refit every year on data up to that year. Forecasts are stored in `ai_index.forecasts` so they can be scored against what actually happened."]
    return "\n".join(L) + "\n"


def main() -> int:
    from google.cloud import bigquery
    client = bigquery.Client(project=PROJECT_ID)
    frame = load(client)
    return run(frame, client)


def run(frame: pd.DataFrame, client=None) -> int:
    s = frame["score"]
    X = features(frame)
    metrics, resid = backtest(X, s)
    fh = from_here(s)
    fc, contribs = outlook(X, s, resid)
    OUT.mkdir(exist_ok=True)
    (OUT / "forecast.md").write_text(report(fc, contribs, metrics, fh))
    fc.to_csv(OUT / "forecast.csv", index=False)
    metrics.to_csv(OUT / "forecast_backtest.csv", index=False)
    fh.to_csv(OUT / "forecast_from_here.csv", index=False)
    if client is not None:
        from google.cloud import bigquery
        rows = fc.assign(computed_at=dt.datetime.now(dt.timezone.utc), model="ridge_half_v1")
        client.load_table_from_dataframe(rows, f"{PROJECT_ID}.ai_index.forecasts",
                                         job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")).result()
    print((OUT / "forecast.md").read_text()[:2500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
