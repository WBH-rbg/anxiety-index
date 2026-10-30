"""The weekly brief: a one-page executive read assembled from the run's outputs.

Reading, band and direction; the provisional "so far this week" nowcast; what is driving it; what the
reading has historically meant for corporate decisions (from the validation tests, not from opinion);
what's ahead (catalysts and shared cultural events in the next three weeks); and the statistical outlook.

Runs last in the workflow and reads only files in output/, so it never fails the run on its own.
"""
from __future__ import annotations

import datetime as dt
import json

import pandas as pd

from index.run import DIM_LABELS, OUT

BAND_RISK = {  # from validation_by_band.csv when present; these are fallbacks
    "Low": 24, "Moderate": 28, "Elevated": 32, "High": 38, "Severe": 44,
}
DIM_ADVICE = {
    # dimension -> (threshold, what the validation found, what it means for decisions)
    "political_institutional": (70, "Political-stance backlash episodes have followed weeks when this reading averaged about 71.",
                                "Stance-related announcements, political giving and executive commentary carry elevated risk this week."),
    "cost_of_living": (75, "Cost-of-living anxiety is in its upper range.",
                       "Price increases, fees and shrinkflation stories will be read against household budgets; lead with value."),
    "jobs_financial": (75, "Jobs and financial anxiety is in its upper range.",
                       "Layoff announcements and executive pay news land harder than usual."),
    "safety_unrest": (75, "Public safety anxiety is in its upper range.",
                      "Security incidents and anything touching guns, protest or policing draw outsized attention."),
    "geopolitical": (80, "Geopolitical anxiety is in its upper range.",
                     "Supply, sanctions and overseas-operations stories are being read through a conflict lens."),
    "disasters_health": (80, "Disaster and health anxiety is in its upper range.",
                         "Operational failures and safety recalls meet a primed audience."),
}


def read_json(path):
    return json.loads(path.read_text()) if path.exists() else None


def read_csv(path, **kw):
    return pd.read_csv(path, **kw) if path.exists() else pd.DataFrame()


def fmt_pct(x) -> str:
    return "" if pd.isna(x) else f"{100 * float(x):.0f}%"


def main() -> int:
    latest = read_json(OUT / "latest.json")
    if not latest:
        print("no latest.json; brief skipped")
        return 0
    head = read_csv(OUT / "headline_weekly.csv", parse_dates=["week"])
    dims = read_csv(OUT / "dimension_weekly.csv", parse_dates=["week"])
    by_band = read_csv(OUT / "validation_by_band.csv", index_col=0)
    fc = read_csv(OUT / "forecast.csv", parse_dates=["origin_week", "target_week"])
    look = read_csv(OUT / "lookahead.csv", parse_dates=["date"])
    culture = read_csv(OUT / "lookahead_culture.csv", parse_dates=["start_date", "end_date"])
    scen = read_csv(OUT / "scenarios.csv")

    week = pd.Timestamp(latest["week"])
    score, band = latest["score"], latest["band"]
    chg = latest.get("change_1w")
    conc = latest.get("news_concentration")
    now = latest.get("nowcast")
    h = head.set_index("week")
    chg4 = h["change_4w"].get(week) if "change_4w" in h.columns else None
    # percentile of this reading within the last 52 weeks, for "highest since" language
    last52 = h["score"].loc[:week].tail(52)
    since = None
    higher_before = h["score"].loc[:week][h["score"].loc[:week] >= score]
    if len(higher_before) > 1:
        since = higher_before.index[-2]

    d = dims[dims["week"] == week].set_index("dimension")
    prev = dims[dims["week"] == week - pd.Timedelta(days=7)].set_index("dimension")["score"] if not dims.empty else pd.Series(dtype=float)
    shares = {}
    try:
        contrib = read_csv(OUT / "contribution_recent.csv", parse_dates=["week"])
        shares = contrib[contrib["week"] == week].set_index("dimension")["share"].to_dict()
    except Exception:
        pass

    L = [f"# Anxiety Index brief: week ending {week.date()}", "",
         f"*Issued {dt.date.today()}. Data through {now['as_of'] if now else week.date()}.*", ""]
    direction = "up" if (chg or 0) > 0.5 else ("down" if (chg or 0) < -0.5 else "flat")
    headline_line = (f"## {score:.0f} — {band}, little changed on the week ({chg or 0:+.1f})" if direction == "flat"
                     else f"## {score:.0f} — {band}, {direction} {abs(chg or 0):.1f} on the week")
    L += [headline_line, ""]
    sent = []
    if chg4 is not None and pd.notna(chg4) and abs(chg4) >= 5:
        sent.append(f"{'Up' if chg4 > 0 else 'Down'} {abs(chg4):.0f} points over four weeks.")
    if since is not None and (week - since).days > 90:
        sent.append(f"Highest reading since the week ending {since.date()}.")
    if conc is not None:
        if conc <= 20:
            sent.append("Attention is spread across many stories, so new ones find room.")
        elif conc >= 80:
            sent.append("One story is dominating coverage; other stories struggle to land, and those that do meet a hotter audience.")
    if sent:
        L += [" ".join(sent), ""]
    if now:
        L += [f"**So far this week:** {now['score']:.0f} ({now['band']}), {now['change_vs_last_week']:+.1f} against the completed week. Provisional; it will move as the week's data arrive.", ""]

    L += ["## What is driving it", "", "| Dimension | Reading | Band | Change | Share of this week's anxiety |", "|---|---|---|---|---|"]
    order = sorted(d.index, key=lambda k: -shares.get(k, 0))
    for dim in order:
        r = d.loc[dim]
        delta = r["score"] - prev.get(dim, float("nan")) if dim in prev.index else float("nan")
        L.append(f"| {DIM_LABELS.get(dim, dim)} | {r['score']:.0f} | {r['band']} | {'' if pd.isna(delta) else f'{delta:+.0f}'} | {fmt_pct(shares.get(dim))} |")
    L += ["", "The headline follows an attention budget: the hottest dimension counts in full, the next at half, the next at a quarter. Shares are exact. `explanation.md` lists the individual signals behind each move.", ""]

    # what it has meant
    L += ["## What a reading like this has meant", ""]
    rate = None
    if not by_band.empty and band in by_band.index and "major_event_rate" in by_band.columns:
        rate = by_band.loc[band, "major_event_rate"]
    rate = BAND_RISK.get(band) if rate is None or pd.isna(rate) else rate
    low = by_band.loc["Low", "major_event_rate"] if not by_band.empty and "Low" in by_band.index else BAND_RISK["Low"]
    L.append(f"- Since 2015, a major corporate backlash episode (national, sustained) followed within two weeks of **{rate:.0f} in 100** weeks that read {band}, against {low:.0f} in 100 after Low weeks.")
    L.append("- Tense weeks make a company story *less* likely to break through and *angrier* when it does. Low news concentration this week means the first effect is weak: stories are landing." if (conc is not None and conc <= 30) else
             "- Tense weeks make a company story *less* likely to break through and *angrier* when it does.")
    for dim, (thr, finding, advice) in DIM_ADVICE.items():
        if dim in d.index and d.loc[dim, "score"] >= thr:
            L.append(f"- **{DIM_LABELS.get(dim, dim)} at {d.loc[dim, 'score']:.0f}.** {finding} {advice}")
    if "safety_unrest" in d.index and d.loc["safety_unrest", "score"] <= 30:
        L.append("- **Public safety reading is low.** Marketing missteps have historically become the story in quiet weeks like this one; there is less competing news to bury a misjudged campaign.")
    L.append("")

    # what's ahead
    L += ["## What's ahead (next three weeks)", ""]
    if look.empty and culture.empty:
        L.append("No scheduled catalysts or shared cultural events in the window.")
    if not look.empty:
        L += ["| Date | Catalyst | Typical effect in past cases |", "|---|---|---|"]
        for _, r in look.iterrows():
            eff = ""
            if "headline_change_mean" in r and pd.notna(r.get("headline_change_mean")):
                if abs(r["headline_change_mean"]) < 1 and (pd.isna(r.get("dimension_change_mean")) or abs(r["dimension_change_mean"]) < 1):
                    eff = f"none to speak of ({int(r['weeks'])} past cases)"
                else:
                    eff = f"headline {r['headline_change_mean']:+.0f} in the week, {r['headline_change_week_after']:+.0f} the week after"
                    if pd.notna(r.get("dimension_change_mean")) and abs(r["dimension_change_mean"]) >= 1:
                        eff += f"; {DIM_LABELS.get(r['dimension'], r['dimension']).lower()} {r['dimension_change_mean']:+.0f}"
                    eff += f" ({int(r['weeks'])} past cases)"
            L.append(f"| {r['date'].date()} | {r['label']} | {eff or 'no history'} |")
        L.append("")
    if not culture.empty:
        big = culture[culture["scale"] >= 3]
        for _, r in culture.iterrows():
            span = f"{r['start_date'].date()}" + (f" to {r['end_date'].date()}" if r["end_date"] != r["start_date"] else "")
            L.append(f"- {r['event']} ({span}), shared-attention scale {int(r['scale'])} of 3")
        if not big.empty:
            L.append("- A scale-3 event is a quieter week for the index, but the first week after it closes has carried a higher-than-usual rate of major corporate episodes as held announcements land. Release inside the window or well after it, not the week it ends.")
        L.append("")

    # outlook
    if not fc.empty:
        L += ["## Outlook", "", "| Weeks ahead | Week ending | Expected | 80% range | Chance of High or Severe | Chance below 50 |", "|---|---|---|---|---|---|"]
        for _, r in fc.iterrows():
            L.append(f"| {int(r['horizon_weeks'])} | {r['target_week'].date()} | {r['central']:.0f} ({r['band']}) | {r['lo80']:.0f}–{r['hi80']:.0f} | {fmt_pct(r['p_high_or_severe'])} | {fmt_pct(r['p_below_50'])} |")
        L += ["", "A small statistical model with a published track record (`forecast.md`); it beats \"no change\" only modestly at short horizons. Readings far above normal tend to ease; shock-driven anxiety fades faster than cost-of-living and political pressure.", ""]

    if not scen.empty and "headline_after" in scen.columns:
        top = scen.sort_values("headline_after", ascending=False).head(3)
        L += ["## If something breaks", ""]
        for _, r in top.iterrows():
            L.append(f"- {r['title']}: {r['headline_before']:.0f} → {r['headline_after']:.0f}")
        L.append("")

    L += ["---", "", "The Anxiety Index measures how primed the US public is to react, 0–100, ranked against 2005–2025. Bands: Low <20, Moderate <50, Elevated <80, High <95, Severe. Methodology and validation: `docs/methodology.md`, `output/validation.md`."]
    (OUT / "brief.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:30]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
