"""Catalyst calendar, cultural windows, and the look-ahead.

    python -m index.calendar      # writes output/lookahead.md and output/calendar_tests.md

Inputs (in the repository):
  docs/calendar/catalysts.csv        date,category,label,scheduled,notes,source
  docs/calendar/cultural_events.csv  start_date,end_date,event,category,scale,notes,source

What it computes
  1. Historical effect of each catalyst category: the average change in the headline, in the most
     relevant dimension, and in the attention lens during weeks containing that catalyst, versus
     all other weeks, with the share of such weeks where the headline rose.
  2. Cultural "distraction windows": weeks overlapping a major shared cultural event. Are attention
     readings lower, and are backlash episodes rarer than the index alone would predict?
  3. The look-ahead: catalysts and cultural windows in the next three weeks, with historical effects.
"""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

from index.run import DIM_LABELS, ROOT, OUT
from index.validate import naive, load_outcomes

CATALYSTS_CSV = ROOT / "docs" / "calendar" / "catalysts.csv"
CULTURE_CSV = ROOT / "docs" / "calendar" / "cultural_events.csv"
LOOKAHEAD_DAYS = 21
CATEGORY_DIMENSION = {
    "fomc_decision": "jobs_financial", "cpi_release": "cost_of_living", "jobs_report": "jobs_financial",
    "election": "political_institutional", "state_of_union": "political_institutional",
    "scotus_term_end": "political_institutional", "debt_ceiling": "political_institutional",
    "tax_day": "cost_of_living", "hurricane_season": "disasters_health",
}
CATEGORY_LABELS = {
    "fomc_decision": "Fed decision", "cpi_release": "CPI release", "jobs_report": "Jobs report", "election": "Election",
    "state_of_union": "State of the Union", "scotus_term_end": "Supreme Court decisions", "debt_ceiling": "Debt limit / shutdown",
    "tax_day": "Tax day", "hurricane_season": "Hurricane season",
}


def week_end(d: pd.Series | pd.Timestamp):
    d = pd.to_datetime(d)
    if isinstance(d, pd.Timestamp):
        return d + pd.Timedelta(days=(5 - d.weekday()) % 7)
    return d + pd.to_timedelta((5 - d.dt.weekday) % 7, unit="D")


def load_index(client):
    head = client.query("SELECT week, score, band, z FROM `ai_index.headline_weekly` WHERE score IS NOT NULL ORDER BY week").to_dataframe()
    head["week"] = naive(head["week"])
    dims = client.query("SELECT week, dimension, score, z FROM `ai_index.dimension_weekly` WHERE score IS NOT NULL").to_dataframe()
    dims["week"] = naive(dims["week"])
    lenses = client.query("SELECT week, dimension, lens, z FROM `ai_index.lens_weekly` WHERE z IS NOT NULL").to_dataframe()
    lenses["week"] = naive(lenses["week"])
    return head, dims, lenses


def load_calendars():
    cats = pd.read_csv(CATALYSTS_CSV) if CATALYSTS_CSV.exists() else pd.DataFrame()
    if not cats.empty:
        cats["date"] = pd.to_datetime(cats["date"], errors="coerce")
        cats = cats.dropna(subset=["date"])
        cats["week"] = week_end(cats["date"])
    cult = pd.read_csv(CULTURE_CSV) if CULTURE_CSV.exists() else pd.DataFrame()
    if not cult.empty:
        cult["start_date"] = pd.to_datetime(cult["start_date"], errors="coerce")
        cult["end_date"] = pd.to_datetime(cult["end_date"], errors="coerce").fillna(cult["start_date"])
        cult = cult.dropna(subset=["start_date"])
        cult["scale"] = pd.to_numeric(cult["scale"], errors="coerce").fillna(1)
    return cats, cult


# ----------------------------------------------------------------------------- catalyst effects
def catalyst_effects(head: pd.DataFrame, dims: pd.DataFrame, lenses: pd.DataFrame, cats: pd.DataFrame) -> pd.DataFrame:
    h = head.set_index("week")["score"]
    dh = h.diff()
    d = dims.pivot(index="week", columns="dimension", values="score")
    dd = d.diff()
    att = lenses[lenses["lens"] == "attention"].groupby("week")["z"].mean()
    datt = att.diff()
    rows = []
    for cat, g in cats[cats["week"] <= h.index.max()].groupby("category"):
        weeks = sorted(set(g["week"]) & set(h.index))
        if len(weeks) < 3:
            continue
        others = h.index.difference(weeks)
        dim = CATEGORY_DIMENSION.get(cat)
        row = {"category": cat, "label": CATEGORY_LABELS.get(cat, cat), "weeks": len(weeks),
               "headline_change_mean": round(dh.reindex(weeks).mean(), 1), "headline_change_other_weeks": round(dh.reindex(others).mean(), 1),
               "share_headline_rose": round(100 * (dh.reindex(weeks) > 0).mean(), 0),
               "attention_change_mean": round(datt.reindex(weeks).mean(), 3), "attention_change_other_weeks": round(datt.reindex(others).mean(), 3),
               "dimension": dim,
               "dimension_change_mean": round(dd[dim].reindex(weeks).mean(), 1) if dim in dd.columns else np.nan,
               "dimension_change_other_weeks": round(dd[dim].reindex(others).mean(), 1) if dim in dd.columns else np.nan}
        rows.append(row)
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------- cultural windows
def cultural_flags(weeks: pd.DatetimeIndex, cult: pd.DataFrame, min_scale: int = 3) -> pd.Series:
    """True for weeks that overlap a cultural event of at least `min_scale`."""
    flags = pd.Series(False, index=weeks)
    for _, r in cult[cult["scale"] >= min_scale].iterrows():
        a, b = r["start_date"], r["end_date"]
        # a week (ending Saturday) overlaps the event if its Sunday..Saturday span intersects [a, b]
        mask = (weeks >= week_end(a)) & (weeks - pd.Timedelta(days=6) <= b)
        flags[mask] = True
    return flags


def cultural_test(head: pd.DataFrame, lenses: pd.DataFrame, cult: pd.DataFrame, outcomes: pd.DataFrame) -> dict:
    h = head.set_index("week")
    h = h[h.index >= pd.Timestamp("2015-01-01")]
    flags = cultural_flags(h.index, cult, 3)
    att = lenses[lenses["lens"] == "attention"].groupby("week")["z"].mean().reindex(h.index)
    out = {"weeks_in_windows": int(flags.sum()), "weeks_total": int(len(flags))}
    out["headline_in"] = round(h.loc[flags, "score"].mean(), 1)
    out["headline_out"] = round(h.loc[~flags, "score"].mean(), 1)
    out["headline_change_in"] = round(h["score"].diff()[flags].mean(), 1)
    out["headline_change_out"] = round(h["score"].diff()[~flags].mean(), 1)
    out["attention_in"] = round(att[flags].mean(), 3)
    out["attention_out"] = round(att[~flags].mean(), 3)
    out["attention_change_in"] = round(att.diff()[flags].mean(), 3)
    out["attention_change_out"] = round(att.diff()[~flags].mean(), 3)
    if not outcomes.empty:
        ev = outcomes[outcomes["severity"] >= 3].copy()
        ev["week"] = week_end(ev["event_date"])
        ev_weeks = set(ev["week"])
        nxt = pd.Series([(w + pd.Timedelta(days=7)) in ev_weeks or (w + pd.Timedelta(days=14)) in ev_weeks for w in h.index], index=h.index)
        # compare within band groups so the test isn't just "windows happen in calmer weeks"
        grp = pd.cut(h["score"], [-1, 50, 80, 101], labels=["Low/Moderate", "Elevated", "High/Severe"])
        table = pd.DataFrame({"group": grp, "in_window": flags, "major_next_2w": nxt}).groupby(["group", "in_window"], observed=True)["major_next_2w"].agg(["size", "mean"])
        table["mean"] = (100 * table["mean"]).round(1)
        out["backlash_by_group"] = table
        out["backlash_in"] = round(100 * nxt[flags].mean(), 1)
        out["backlash_out"] = round(100 * nxt[~flags].mean(), 1)
    return out


# ----------------------------------------------------------------------------- look-ahead
def lookahead(head: pd.DataFrame, cats: pd.DataFrame, cult: pd.DataFrame, effects: pd.DataFrame) -> str:
    last = head["week"].max()
    horizon = last + pd.Timedelta(days=LOOKAHEAD_DAYS)
    eff = effects.set_index("category") if not effects.empty else pd.DataFrame()
    L = [f"# Look-ahead from the week ending {last.date()}", "",
         f"Scheduled catalysts and shared cultural events in the next {LOOKAHEAD_DAYS} days, with what weeks like them have done to the index historically.", "",
         "## Catalysts", "", "| Date | Catalyst | Historical headline change in such weeks | Weeks rose | Typical dimension moved |", "|---|---|---|---|---|"]
    upcoming = cats[(cats["date"] > last) & (cats["date"] <= horizon)].sort_values("date") if not cats.empty else pd.DataFrame()
    if upcoming.empty:
        L.append("| | none in window | | | |")
    for _, r in upcoming.iterrows():
        e = eff.loc[r["category"]] if r["category"] in eff.index else None
        chg = f"{e['headline_change_mean']:+.1f} (others {e['headline_change_other_weeks']:+.1f})" if e is not None else "n/a"
        rose = f"{e['share_headline_rose']:.0f}%" if e is not None else ""
        dimtxt = f"{DIM_LABELS.get(e['dimension'], e['dimension'])} {e['dimension_change_mean']:+.1f}" if e is not None and pd.notna(e.get("dimension_change_mean")) else ""
        L.append(f"| {r['date'].date()} | {r['label']} | {chg} | {rose} | {dimtxt} |")
    L += ["", "## Shared cultural events (possible distraction windows)", "", "| Dates | Event | Scale |", "|---|---|---|"]
    upc = cult[(cult["end_date"] >= last) & (cult["start_date"] <= horizon)].sort_values("start_date") if not cult.empty else pd.DataFrame()
    if upc.empty:
        L.append("| | none in window | |")
    for _, r in upc.iterrows():
        span = f"{r['start_date'].date()}" + (f" to {r['end_date'].date()}" if r["end_date"] != r["start_date"] else "")
        L.append(f"| {span} | {r['event']} | {int(r['scale'])} |")
    L += ["", "Historical changes are averages of week-over-week moves in the headline (percentile points) during weeks containing that kind of catalyst, 2015 onward, against all other weeks. They describe tendency, not prediction."]
    return "\n".join(L) + "\n"


def tests_report(effects: pd.DataFrame, cult_out: dict) -> str:
    L = ["# Calendar tests", "", f"Generated {dt.date.today()}.", "", "## Catalyst effects (weeks containing the catalyst vs. all other weeks, 2015 onward where data allow)", "",
         "| Catalyst | Weeks | Headline change | Other weeks | Share rose | Attention-lens change | Other weeks | Dimension | Dim change | Other weeks |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in (effects.sort_values("weeks", ascending=False) if not effects.empty else effects).iterrows():
        L.append(f"| {r['label']} | {r['weeks']} | {r['headline_change_mean']:+.1f} | {r['headline_change_other_weeks']:+.1f} | {r['share_headline_rose']:.0f}% | "
                 f"{r['attention_change_mean']:+.3f} | {r['attention_change_other_weeks']:+.3f} | {DIM_LABELS.get(r['dimension'], r['dimension'])} | "
                 f"{r['dimension_change_mean']:+.1f} | {r['dimension_change_other_weeks']:+.1f} |")
    if effects.empty:
        L.append("| no catalyst calendar loaded | | | | | | | | | |")
    L += ["", "## Cultural distraction windows (weeks overlapping a scale-3 shared event: Super Bowl, Olympics opening, July 4, Thanksgiving, Christmas, eclipses, etc.)", ""]
    if not cult_out:
        L.append("No cultural calendar loaded.")
    else:
        c = cult_out
        L += [f"{c['weeks_in_windows']} of {c['weeks_total']} weeks since 2015 fall in a window.", "",
              "| Measure | In windows | Other weeks |", "|---|---|---|",
              f"| Mean headline | {c['headline_in']} | {c['headline_out']} |",
              f"| Mean week-over-week headline change | {c['headline_change_in']:+.1f} | {c['headline_change_out']:+.1f} |",
              f"| Mean attention-lens reading (z) | {c['attention_in']:+.3f} | {c['attention_out']:+.3f} |",
              f"| Mean attention-lens change | {c['attention_change_in']:+.3f} | {c['attention_change_out']:+.3f} |"]
        if "backlash_in" in c:
            L += [f"| Major backlash episode in next 2 weeks (per 100 weeks) | {c['backlash_in']} | {c['backlash_out']} |", "",
                  "Backlash rate within band groups (so the comparison isn't just that windows fall in calmer weeks):", "",
                  "| Reading | In window | Weeks | Rate per 100 |", "|---|---|---|---|"]
            for (grp, inw), r in c["backlash_by_group"].iterrows():
                L.append(f"| {grp} | {'yes' if inw else 'no'} | {int(r['size'])} | {r['mean']} |")
        L += ["", "Reading: if windows show lower attention readings and lower backlash rates within the same band, shared cultural events act as a damper worth modeling. If not, they are calendar noise."]
    return "\n".join(L) + "\n"


def main() -> int:
    from google.cloud import bigquery
    client = bigquery.Client(project="anxiety-index")
    head, dims, lenses = load_index(client)
    cats, cult = load_calendars()
    outcomes = load_outcomes()
    effects = catalyst_effects(head, dims, lenses, cats) if not cats.empty else pd.DataFrame()
    cult_out = cultural_test(head, lenses, cult, outcomes) if not cult.empty else {}
    OUT.mkdir(exist_ok=True)
    (OUT / "lookahead.md").write_text(lookahead(head, cats, cult, effects))
    (OUT / "calendar_tests.md").write_text(tests_report(effects, cult_out))
    if not effects.empty:
        client.load_table_from_dataframe(effects.assign(computed_at=dt.datetime.now(dt.timezone.utc)), "anxiety-index.ai_index.catalyst_effects",
                                         job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")).result()
    print((OUT / "lookahead.md").read_text()[:1500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
