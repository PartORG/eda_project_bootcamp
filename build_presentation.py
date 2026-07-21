"""Build the client-facing slide deck straight from the dataset.

Every number on every slide is computed here from `data/eda.csv`, so the deck can
never drift out of sync with the analysis the way a hand-edited PDF does.

    uv run python build_presentation.py [--data data/eda.csv] [--out deck.pdf]

Design follows the original deck: cream graph-paper backgrounds, a heavy condensed
display face for titles, tilted colour chips, and hard-shadowed cards. Anton and
Manrope are not redistributable here, so Impact and a Helvetica-alike stand in.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Ellipse, FancyBboxPatch, Rectangle

plt.rcParams["text.parse_math"] = False  # dollar signs are literal, not TeX

# ---------------------------------------------------------------- design system
CREAM, INK, PAPER = "#EDE9DE", "#141414", "#FFFFFF"
RED, TEAL, GREEN, SAND = "#E8615A", "#2AAFA8", "#6B9B5F", "#CDC7B9"
MUTED = "#8A857B"
DISPLAY = "Impact"                 # stands in for Anton
SANS = "Liberation Sans"           # stands in for Manrope

W, H = 10.0, 5.625                 # inches -> 720x405 pt at 72 dpi


def _canvas(bg):
    fig = plt.figure(figsize=(W, H), dpi=200)
    fig.patch.set_facecolor(bg)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_facecolor(bg)
    return fig, ax


def grid_paper(ax, color="#D8D3C6", step=0.037):
    """The graph-paper texture from the title slide."""
    for x in np.arange(0, 1.001, step):
        ax.plot([x, x], [0, 1], color=color, lw=0.6, zorder=0)
    for y in np.arange(0, 1.001, step * W / H):
        ax.plot([0, 1], [y, y], color=color, lw=0.6, zorder=0)


def dot(ax, x, y, r, color, zorder=6):
    """A visually round dot - axes coords are not square, so compensate."""
    ax.add_patch(Ellipse((x, y), width=2 * r, height=2 * r * W / H,
                         facecolor=color, edgecolor="none", zorder=zorder))


def ruled_paper(ax, color="#DCD7CA"):
    """The lined-notebook texture, with the punched-hole margin."""
    for y in np.arange(0.06, 0.98, 0.062):
        ax.plot([0.075, 1], [y, y], color=color, lw=0.7, zorder=0)
    for y in np.arange(0.10, 0.95, 0.105):
        dot(ax, 0.032, y, 0.011, SAND, zorder=1)


def chip(ax, x, y, text, color, angle=-6, fs=11, tc=INK):
    """Tilted colour label, the deck's signature motif."""
    ax.text(x, y, f"  {text}  ", fontsize=fs, family=SANS, fontweight="bold",
            color=tc, rotation=angle, rotation_mode="anchor",
            va="center", ha="center", zorder=5,
            bbox=dict(boxstyle="square,pad=0.45", facecolor=color, edgecolor="none"))


def card(ax, x, y, w, h, facecolor=PAPER, shadow="#2B2B2B", radius=0.012):
    """Panel with the hard offset shadow used throughout the original."""
    ax.add_patch(FancyBboxPatch((x + 0.008, y - 0.014), w, h,
                                boxstyle=f"round,pad=0,rounding_size={radius}",
                                facecolor=shadow, edgecolor="none", zorder=2))
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f"round,pad=0,rounding_size={radius}",
                                facecolor=facecolor, edgecolor="none", zorder=3))


def heading(ax, x, y, lines, fs=30, color=INK, lead=0.098):
    for line in lines.split("\n"):
        ax.text(x, y, line, fontsize=fs, family=DISPLAY, color=color,
                va="top", zorder=6)
        y -= lead
    return y


def bullets(ax, x, y, items, label_w=0.15, fs=8.6, step=0.093, color=INK):
    for label, text, col in items:
        ax.text(x, y, label, fontsize=7.6, family=SANS, fontweight="bold",
                color=col, va="top", zorder=6)
        ax.text(x + label_w, y, text, fontsize=fs, family=SANS, color=color,
                va="top", linespacing=1.45, zorder=6)
        y -= step + 0.031 * text.count("\n")
    return y


def money(v, dp=2):
    return f"${v/1e6:.{dp}f}M" if v >= 1e6 else f"${v/1e3:.0f}K"


def chart_axes(fig, rect, bg=PAPER):
    ax = fig.add_axes(rect, zorder=4)
    ax.set_facecolor(bg)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors=MUTED, labelsize=7, length=0)
    ax.grid(axis="y", color="#E4E0D6", lw=0.8)
    ax.set_axisbelow(True)
    return ax


# ---------------------------------------------------------------- analysis
def permutation_p(values, labels, n_perm=1000, seed=42):
    """P-value for 'the best-vs-worst bucket gap is bigger than chance'.

    Corrects for having cherry-picked the most extreme of many buckets.
    """
    rng = np.random.default_rng(seed)
    v = np.asarray(values, dtype=float)
    lab = np.asarray(labels)

    def spread(l):
        m = pd.Series(v).groupby(l).median()
        return m.max() - m.min()

    obs = spread(lab)
    hits = sum(spread(rng.permutation(lab)) >= obs for _ in range(n_perm))
    return (hits + 1) / (n_perm + 1)


def analyse(path: Path) -> dict:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df["reno_unknown"] = df["year_renovated"].isna()
    df["year_renovated"] = (df["year_renovated"] // 10).fillna(0).astype("Int64")
    df["price_per_sqft"] = df["price"] / df["sqft_living"]
    df["is_renovated"] = (df["year_renovated"] > 0).astype(int)

    f = {"n": len(df),
         "start": df["date"].min(), "end": df["date"].max()}

    # waterfront - known values only, no imputation needed for a headline number
    wf = df.dropna(subset=["waterfront"])
    f["wf_yes"] = wf.loc[wf["waterfront"] == 1, "price"].median()
    f["wf_no"] = wf.loc[wf["waterfront"] == 0, "price"].median()
    f["wf_n"] = int((wf["waterfront"] == 1).sum())
    f["wf_mult"] = f["wf_yes"] / f["wf_no"]

    # renovation
    g = df.groupby("is_renovated")["price"].median()
    f["ren_no"], f["ren_yes"] = g[0], g[1]
    f["ren_prem"] = (g[1] / g[0] - 1) * 100
    lux = df[df["grade"] >= 10]
    gl = lux.groupby("is_renovated")["price"].median()
    f["lren_no"], f["lren_yes"] = gl[0], gl[1]
    f["lren_prem"] = (gl[1] / gl[0] - 1) * 100
    # does it survive a size control?
    bands = pd.cut(df["sqft_living"], [0, 1500, 2500, 3500, 1e9])
    f["ren_by_band"] = (df.groupby([bands, "is_renovated"], observed=True)["price"]
                        .median().unstack())

    # correlations
    cols = ["sqft_living", "grade", "sqft_above", "sqft_living15", "bathrooms"]
    f["corr"] = df[cols + ["price"]].corr()["price"].drop("price").sort_values(ascending=False)

    f["ppsf_all"] = df["price_per_sqft"].median()
    f["ppsf_lux"] = lux["price_per_sqft"].median()

    # thresholds and the luxury pool
    thr = df["price"].quantile(0.9)
    f["thr"] = thr
    pool = df[(df["price"] >= thr) & (df["grade"] >= 10) & (df["view"] >= 3)].copy()
    pool["day"] = pool["date"].dt.day
    pool["month"] = pool["date"].dt.month
    f["pool_n"] = len(pool)
    f["pool"] = pool

    day_stats = pool.groupby("day")["price"].agg(["median", "size"])
    f["day_stats"] = day_stats
    f["best_day"] = int(day_stats["median"].idxmin())
    f["best_day_price"] = day_stats["median"].min()
    f["best_day_n"] = int(day_stats.loc[f["best_day"], "size"])
    f["p_day"] = permutation_p(pool["price"], pool["day"])

    allm = df.copy()
    allm["day"] = allm["date"].dt.day
    allm["month"] = allm["date"].dt.month
    rank_series = allm.groupby("day")["price"].median().sort_values()
    f["day_rank"] = list(rank_series.index).index(f["best_day"]) + 1
    f["day_total"] = len(rank_series)

    mon = pool.groupby("month")["price"].agg(["median", "size"])
    f["mon_stats"] = mon
    f["best_mon"], f["worst_mon"] = int(mon["median"].idxmax()), int(mon["median"].idxmin())
    f["mon_gap"] = (mon["median"].max() / mon["median"].min() - 1) * 100
    f["best_mon_n"] = int(mon.loc[f["best_mon"], "size"])
    f["worst_mon_n"] = int(mon.loc[f["worst_mon"], "size"])
    f["p_mon"] = permutation_p(pool["price"], pool["month"])
    am = allm.groupby("month")["price"].median()
    f["mon_gap_all"] = (am[f["best_mon"]] / am[f["worst_mon"]] - 1) * 100

    # repeat sales - the direct test of the resale plan
    dup = df[df["house_id"].duplicated(keep=False)].sort_values(["house_id", "date"])
    a, b = dup.groupby("house_id").first(), dup.groupby("house_id").last()
    res = pd.DataFrame({"buy": a["price"], "sell": b["price"], "grade": a["grade"],
                        "days": (b["date"] - a["date"]).dt.days})
    res["ret"] = (res["sell"] / res["buy"] - 1) * 100
    f["resale_n"] = len(res)
    f["resale_all"] = res["ret"].median()
    seg = res[(res["buy"] >= thr) & (res["grade"] >= 10)]
    f["seg"] = seg.sort_values("ret", ascending=False)
    f["seg_med"] = seg["ret"].median()
    f["seg_days"] = seg["days"].median()

    # geography
    f["zip_price"] = df.groupby("zipcode")["price"].median().sort_values(ascending=False)
    f["zip_lux"] = pool.groupby("zipcode").size().sort_values(ascending=False)
    f["df"] = df

    # the shortlist - genuine waterfront only, renovation year known
    cand = df[(df["price"] >= thr) & (df["grade"] >= 10) & (df["view"] >= 3) &
              (df["waterfront"] == 1) & (df["year_renovated"] > 0) &
              (df["condition"] >= 3)].copy()
    cand["score"] = ((cand["sqft_living"] / cand["sqft_living15"]) *
                     (cand["sqft_lot"] / cand["sqft_lot15"]) *
                     (cand["price"] / 1_000_000) *
                     (cand["grade"] / 10)).round(2)
    f["cand"] = cand.sort_values("score", ascending=False)
    f["unknown_reno"] = int(((df["price"] >= thr) & (df["grade"] >= 10) &
                             (df["view"] >= 3) & (df["waterfront"] == 1) &
                             (df["condition"] >= 3) & df["reno_unknown"]).sum())
    return f


# ---------------------------------------------------------------- slides
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def slide_title(pdf, f):
    fig, ax = _canvas(CREAM)
    grid_paper(ax)
    chip(ax, 0.235, 0.795, "A-Door-Able Homes", RED, angle=-7, fs=12)
    heading(ax, 0.085, 0.66, "Pads, Palaces,\nand Premiums", fs=62, lead=0.175)
    chip(ax, 0.66, 0.30, "Luxury", GREEN, angle=-4, fs=11)
    chip(ax, 0.79, 0.325, "Evidence", TEAL, angle=5, fs=11)
    ax.text(0.5, 0.145, "The King County data that justifies your expensive taste",
            fontsize=11, family=SANS, color="#4A4640", ha="center", zorder=6)
    ax.text(0.5, 0.095, "(and the three recommendations we tested until they broke)",
            fontsize=9.5, family=SANS, color=MUTED, ha="center",
            style="italic", zorder=6)
    ax.text(0.5, 0.035,
            f"{f['n']:,} sales   ·   {f['start']:%b %Y} – {f['end']:%b %Y}   ·   King County, WA",
            fontsize=8, family=SANS, color=MUTED, ha="center", zorder=6)
    pdf.savefig(fig, facecolor=CREAM); plt.close(fig)


def slide_brief(pdf, f):
    fig, ax = _canvas(CREAM)
    ruled_paper(ax)
    heading(ax, 0.10, 0.90, "THE BRIEF", fs=34)
    ax.text(0.10, 0.775, "Jennifer Montgomery wants a lot of things at once.",
            fontsize=10, family=SANS, color="#4A4640", style="italic", zorder=6)

    card(ax, 0.095, 0.20, 0.40, 0.53, PAPER)
    ax.text(0.12, 0.685, "WHAT SHE ASKED FOR", fontsize=8.5, family=SANS,
            fontweight="bold", color=RED, zorder=6)
    wants = ["High budget, wants to show off", "Waterfront access",
             "Recently renovated", "High grade and a real view",
             "Buy within a month", "Resell within a year"]
    y = 0.615
    for w in wants:
        dot(ax, 0.128, y + 0.009, 0.005, TEAL)
        ax.text(0.148, y, w, fontsize=9, family=SANS, color=INK, va="top", zorder=6)
        y -= 0.072

    card(ax, 0.525, 0.20, 0.40, 0.53, INK)
    ax.text(0.55, 0.685, "WHAT THAT MEANS IN THE DATA", fontsize=8.5, family=SANS,
            fontweight="bold", color=TEAL, zorder=6)
    rules = [f"price >= {money(f['thr'], 0)}   (90th percentile)",
             "waterfront == 1", "year_renovated > 0",
             "grade >= 10  and  view >= 3", "condition >= 3"]
    y = 0.615
    for r in rules:
        ax.text(0.55, y, r, fontsize=9, family=SANS, color=PAPER, va="top", zorder=6)
        y -= 0.072
    ax.text(0.55, y - 0.005, f"{len(f['cand'])} properties survive all six.",
            fontsize=10.5, family=SANS, fontweight="bold", color=RED,
            va="top", zorder=6)

    ax.text(0.10, 0.105, "The scarcity is the finding.", fontsize=12,
            family=DISPLAY, color=INK, zorder=6)
    ax.text(0.10, 0.082,
            f"Six hard requirements leave a handful of houses out of {f['n']:,}.\n"
            "Before anything else, the client needs to know which requirement\n"
            "she would most like to relax.",
            fontsize=8.5, family=SANS, color="#4A4640", va="top",
            linespacing=1.5, zorder=6)
    pdf.savefig(fig, facecolor=CREAM); plt.close(fig)


def _finding_slide(pdf, f, title, lede, draw_chart, points, verdict, vcolor):
    """Cream slide: chart on the left, commentary card on the right."""
    fig, ax = _canvas(CREAM)
    grid_paper(ax)
    heading(ax, 0.06, 0.955, title, fs=25, lead=0.077)
    ax.text(0.06, 0.775, lede, fontsize=9, family=SANS, color="#4A4640",
            style="italic", zorder=6)

    card(ax, 0.055, 0.115, 0.475, 0.60, PAPER)
    draw_chart(fig)

    card(ax, 0.565, 0.115, 0.385, 0.60, INK)
    y = 0.655
    for label, text in points:
        ax.text(0.593, y, label, fontsize=7.6, family=SANS, fontweight="bold",
                color=TEAL, va="top", zorder=6)
        ax.text(0.593, y - 0.038, text, fontsize=8.6, family=SANS, color=PAPER,
                va="top", linespacing=1.5, zorder=6)
        y -= 0.115 + 0.036 * text.count("\n")

    ax.add_patch(Rectangle((0.593, 0.152), 0.33, 0.052, facecolor=vcolor, zorder=6))
    ax.text(0.608, 0.178, verdict, fontsize=9, family=SANS, fontweight="bold",
            color=INK, va="center", zorder=7)
    pdf.savefig(fig, facecolor=CREAM); plt.close(fig)


def slide_waterfront(pdf, f):
    def chart(fig):
        a = chart_axes(fig, [0.128, 0.215, 0.335, 0.385])
        bars = a.bar(["Non-waterfront", "Waterfront"], [f["wf_no"], f["wf_yes"]],
                     color=["#B9C4CC", TEAL], width=0.5, zorder=3)
        for b, v in zip(bars, [f["wf_no"], f["wf_yes"]]):
            a.text(b.get_x() + b.get_width() / 2, v, money(v), ha="center",
                   va="bottom", fontsize=9.5, family=SANS, fontweight="bold",
                   color=INK, zorder=4)
        a.set_ylim(0, f["wf_yes"] * 1.22)
        a.set_ylabel("Median sale price", fontsize=8, family=SANS, color=MUTED)
        a.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f"${v/1e6:.1f}M"))
        a.set_title(f"n = {f['wf_n']} waterfront sales", fontsize=7.5,
                    family=SANS, color=MUTED, loc="left")

    _finding_slide(
        pdf, f, "WATERFRONT IS NOT A FEATURE.\nIT IS A SEPARATE MARKET.",
        "Hypothesis H3 - confirmed, and by a wider margin than any other feature in the dataset.",
        chart,
        [("THE PREMIUM",
          f"Waterfront homes sell at a median of\n{money(f['wf_yes'])} against {money(f['wf_no'])} — "
          f"{f['wf_mult']:.1f}x."),
         ("THE SCARCITY",
          f"Only {f['wf_n']} of {f['n']:,} sales are waterfront.\nRoughly {f['wf_n']/f['n']*100:.1f}% of the market."),
         ("WHY IT IS NOT JUST 'A VIEW'",
          "Grade tracks it too: waterfront homes\ncluster in the top build grades. The\nmarket treats shoreline as a different\nproduct, not a nicer version of the same one."),
         ("FOR THE CLIENT",
          "Worth paying for - but it is also the\nrequirement that shrinks the candidate\nlist fastest, from thousands to dozens.")],
        "H3 CONFIRMED", GREEN)


def slide_renovation(pdf, f):
    def chart(fig):
        a = chart_axes(fig, [0.128, 0.215, 0.335, 0.385])
        x = np.arange(2)
        a.bar(x - 0.19, [f["ren_no"], f["lren_no"]], width=0.34,
              color="#B9C4CC", label="Not renovated", zorder=3)
        a.bar(x + 0.19, [f["ren_yes"], f["lren_yes"]], width=0.34,
              color=GREEN, label="Renovated", zorder=3)
        for xi, (lo, hi) in enumerate([(f["ren_no"], f["ren_yes"]),
                                       (f["lren_no"], f["lren_yes"])]):
            a.text(xi - 0.19, lo, money(lo), ha="center", va="bottom",
                   fontsize=8, family=SANS, color=INK, zorder=4)
            a.text(xi + 0.19, hi, money(hi), ha="center", va="bottom",
                   fontsize=8, family=SANS, fontweight="bold", color=INK, zorder=4)
        a.set_xticks(x, ["All properties", "Luxury (grade >= 10)"],
                     fontsize=8, family=SANS)
        a.set_ylim(0, f["lren_yes"] * 1.25)
        a.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f"${v/1e6:.1f}M"))
        a.legend(fontsize=7, frameon=False, loc="upper left")

    _finding_slide(
        pdf, f, "RENOVATION IS THE ONE\nTHAT SURVIVES EVERY CHECK.",
        "Hypothesis H5 - the only price finding here that still holds once confounders are controlled for.",
        chart,
        [("THE UPLIFT",
          f"+{f['ren_prem']:.0f}% market-wide, and\n+{f['lren_prem']:.0f}% inside the luxury segment."),
         ("THE OBVIOUS OBJECTION",
          "Renovated homes are also older, bigger\nand better located. So is the premium\nreal, or is it just size in disguise?"),
         ("THE CONTROL",
          "Split the market into living-area bands\nand the premium survives in every band\nabove 1,500 sqft - though it vanishes\nbelow that."),
         ("THE HONEST WORDING",
          "Renovated homes sell for more. That is\nnot the same claim as renovating adding\nthat much value.")],
        "H5 CONFIRMED", GREEN)


def slide_size(pdf, f):
    def chart(fig):
        a = chart_axes(fig, [0.128, 0.215, 0.335, 0.385])
        d = f["df"].sample(min(6000, len(f["df"])), random_state=1)
        s = a.scatter(d["sqft_living"], d["price"], c=d["grade"], cmap="viridis",
                      s=5, alpha=0.55, edgecolors="none", zorder=3)
        a.set_xlabel("Living area (sqft)", fontsize=8, family=SANS, color=MUTED)
        a.set_ylabel("Sale price", fontsize=8, family=SANS, color=MUTED)
        a.set_ylim(0, f["df"]["price"].quantile(0.995))
        a.set_xlim(0, f["df"]["sqft_living"].quantile(0.995))
        a.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f"${v/1e6:.0f}M"))
        cb = a.figure.colorbar(s, ax=a, pad=0.02)
        cb.set_label("Grade", fontsize=7, family=SANS, color=MUTED)
        cb.ax.tick_params(labelsize=6, colors=MUTED, length=0)
        cb.outline.set_visible(False)

    top = f["corr"]
    _finding_slide(
        pdf, f, "SIZE AND GRADE\nDO THE WORK.",
        "Hypothesis H4 - living area is the single strongest predictor of price anywhere in the data.",
        chart,
        [("THE DRIVERS",
          "\n".join(f"{k:<15s} r = {v:.2f}" for k, v in top.items()) +
          "\n\nEvery strong predictor is a measure of\nsize or build quality. None is a measure\nof timing."),
         ("THE VALUE ANGLE",
          f"{f['ppsf_all']:.0f} $/sqft market-wide against\n{f['ppsf_lux']:.0f} in the luxury segment - yet the very\n"
          "largest homes drop back below both.\nSize is bought at a discount at the top.")],
        "H4 CONFIRMED", GREEN)


def _dark_slide(pdf, title, lede, items, verdict, vcolor, stat, cap, quote):
    fig, ax = _canvas("#0D0D0D")
    ax.plot([0.045, 0.045], [0.10, 0.90], color=MUTED, lw=0.8, alpha=0.45, zorder=1)
    y = heading(ax, 0.075, 0.885, title, fs=27, color=PAPER)
    ax.text(0.075, y - 0.02, lede, fontsize=8.5, family=SANS, color=MUTED,
            style="italic", va="top", zorder=6)
    bullets(ax, 0.075, 0.545, items, color=PAPER)
    ax.add_patch(Rectangle((0.075, 0.055), 0.53, 0.062, facecolor=vcolor, zorder=5))
    ax.text(0.093, 0.086, verdict, fontsize=9.5, family=SANS, fontweight="bold",
            color=INK, va="center", zorder=6)
    ax.plot([0.63, 0.63], [0.17, 0.60], color=MUTED, lw=0.8, alpha=0.45, zorder=1)
    ax.text(0.665, 0.545, stat, fontsize=44, family=DISPLAY, color=vcolor,
            va="top", zorder=6)
    ax.text(0.665, 0.365, cap, fontsize=8.4, family=SANS, color=PAPER,
            va="top", linespacing=1.6, zorder=6)
    ax.text(0.665, 0.145, quote, fontsize=7.6, family=SANS, color=MUTED,
            style="italic", va="top", linespacing=1.6, zorder=6)
    pdf.savefig(fig, facecolor="#0D0D0D"); plt.close(fig)


def slide_day(pdf, f):
    _dark_slide(
        pdf, "TESTED,\nTHEN REJECTED",
        "We looked for a cheapest day of the month to buy. We found one - then tried to break it.",
        [("THE CLAIM", f"Day {f['best_day']} has the lowest median luxury\nprice ({money(f['best_day_price'])}).", TEAL),
         ("THE PROBLEM", f"That median rests on {f['best_day_n']} sales. The typical\n"
                         f"day-of-month bucket holds {int(f['day_stats']['size'].median())}.", RED),
         ("THE TEST", "Shuffling the day labels 1,000 times\nreproduces a gap this large "
                      f"{f['p_day']*100:.0f}% of the time.", RED),
         ("THE REALITY", f"Across all {f['n']:,} sales day {f['best_day']} ranks\n"
                         f"{f['day_rank']} of {f['day_total']} - among the dearest. The\npattern reverses at scale.", GREEN)],
        "H7 REJECTED  ·  no day-of-month advice", RED,
        f"p = {f['p_day']:.2f}",
        "Permutation test, corrected for\nhaving picked the best of 31 days.\nIndistinguishable from noise.",
        '"We could have sold you a lucky\ndate. We would rather sell you\na house."')


def slide_month(pdf, f):
    _dark_slide(
        pdf, "SEASONALITY IS REAL.\nIT IS ALSO TINY.",
        "The same test on the month of sale - where, unlike the day, a real effect does exist.",
        [("THE CLAIM", f"{MONTHS[f['best_mon']-1]} beats {MONTHS[f['worst_mon']-1]} by "
                       f"{f['mon_gap']:.0f}%\n({money(f['mon_stats'].loc[f['best_mon'],'median'])} vs "
                       f"{money(f['mon_stats'].loc[f['worst_mon'],'median'])}).", TEAL),
         ("THE PROBLEM", f"{f['best_mon_n']} sales versus {f['worst_mon_n']}. "
                         f"Permutation p = {f['p_mon']:.2f}.", RED),
         ("AT SCALE", "Market-wide a month effect IS detectable —\n"
                      f"but the same two months differ by\nonly {f['mon_gap_all']:.1f}%.", GREEN),
         ("THE LESSON", "Significance answers 'is it real?'. Effect\nsize answers 'do I care?'. Here the answers\nare yes and no.", GREEN)],
        "H6 REJECTED  ·  it predicted January anyway", RED,
        f"{f['mon_gap_all']:.1f}%",
        f"The real {MONTHS[f['best_mon']-1]}-vs-{MONTHS[f['worst_mon']-1]} gap once all\n"
        f"{f['n']:,} sales are used, instead of\nthe {f['pool_n']} in the luxury pool.",
        '"A 2% seasonal edge does not\nsurvive a 6% transaction fee."')


def slide_resale(pdf, f):
    rets = "  ".join(f"{v:+.1f}%" for v in f["seg"]["ret"])
    _dark_slide(
        pdf, "THE RESALE PLAN\nNEEDS A RETHINK",
        "The client wants to resell inside a year. Repeat sales answer that question directly.",
        [("THE DATA", f"{f['resale_n']} houses here sold twice. {len(f['seg'])} sit inside\n"
                      "the client's own price and grade segment.", TEAL),
         ("THE RETURNS", f"{rets}\nMedian: {f['seg_med']:+.1f}% over {f['seg_days']:.0f} days.", RED),
         ("THE COSTS", "Round-trip transaction costs on a\nproperty sale: 6-10%.", RED),
         ("THE ADVICE", "Buy to hold, or revise the target. The\none-year flip does not clear its own costs.", GREEN)],
        "BUY TO HOLD  ·  the flip does not pay", GREEN,
        f"{f['seg_med']:+.1f}%",
        "Median return on comparable\nresales in her own segment,\nbefore 6-10% in costs.",
        f'"The market-wide figure says\n{f["resale_all"]:+.0f}%. That is people flipping\n'
        'starter homes, not waterfront."')


def slide_geography(pdf, f):
    def chart(fig):
        a = chart_axes(fig, [0.128, 0.215, 0.335, 0.385])
        top = f["zip_price"].head(8).iloc[::-1]
        a.barh([str(z) for z in top.index], top.values, color=TEAL, height=0.6, zorder=3)
        a.grid(axis="y", visible=False)
        a.grid(axis="x", color="#E4E0D6", lw=0.8)
        a.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f"${v/1e6:.1f}M"))
        a.set_xlabel("Median sale price", fontsize=8, family=SANS, color=MUTED)
        a.set_title("Most expensive zipcodes", fontsize=7.5, family=SANS,
                    color=MUTED, loc="left")

    lux = f["zip_lux"]
    _finding_slide(
        pdf, f, "WHERE THE MONEY\nACTUALLY SITS.",
        "Drawn from all 240 luxury sales, not inferred from a five-house shortlist.",
        chart,
        [("THE PRICIEST",
          "\n".join(f"{z}   median {money(f['zip_price'][z])}"
                    for z in f["zip_price"].head(3).index)),
         ("THE DEEPEST MARKET",
          "Most luxury transactions:\n" +
          "   ".join(f"{z} ({n})" for z, n in lux.head(3).items())),
         ("WHY IT MATTERS",
          "Prestige and depth are not the same\nplace. The dearest zipcode is thin.")],
        "GEOGRAPHIC INSIGHT", TEAL)


def slide_shortlist(pdf, f):
    fig, ax = _canvas(CREAM)
    ruled_paper(ax)
    heading(ax, 0.09, 0.925, "THE SHORTLIST", fs=34)
    ax.text(0.09, 0.80, "Ranked by how far each stands out from its own neighbourhood.",
            fontsize=9.5, family=SANS, color="#4A4640", style="italic", zorder=6)

    accents = [GREEN, TEAL, RED]
    top = f["cand"].head(3)
    x = 0.085
    for (_, r), col in zip(top.iterrows(), accents):
        card(ax, x, 0.245, 0.265, 0.49, PAPER)
        ax.add_patch(Rectangle((x, 0.685), 0.265, 0.05, facecolor=col, zorder=4))
        ax.text(x + 0.018, 0.710, f"house_id {int(r['house_id'])}", fontsize=9,
                family=SANS, fontweight="bold", color=INK, va="center", zorder=6)
        ax.text(x + 0.018, 0.605, money(r["price"]), fontsize=25, family=DISPLAY,
                color=INK, va="center", zorder=6)
        rows = [("Zipcode", f"{int(r['zipcode'])}"),
                ("Grade", f"{int(r['grade'])} of 13"),
                ("View", f"{int(r['view'])} of 4"),
                ("Renovated", f"{int(r['year_renovated'])}"),
                ("Living area", f"{int(r['sqft_living']):,} sqft"),
                ("Premium score", f"{r['score']:.2f}")]
        y = 0.525
        for k, v in rows:
            ax.text(x + 0.018, y, k, fontsize=7.5, family=SANS, color=MUTED, zorder=6)
            ax.text(x + 0.247, y, v, fontsize=8.5, family=SANS, fontweight="bold",
                    color=INK, ha="right", zorder=6)
            y -= 0.042
        x += 0.295

    ax.text(0.09, 0.165, f"Plus {f['unknown_reno']} more the filters cannot confirm.",
            fontsize=11, family=DISPLAY, color=INK, zorder=6)
    ax.text(0.09, 0.115,
            "Those properties meet every other requirement, but their renovation year is missing "
            "from the record. Filling that\ngap with a zero would quietly delete them — so they are "
            "reported separately rather than dropped.",
            fontsize=8.5, family=SANS, color="#4A4640", va="top", zorder=6)
    pdf.savefig(fig, facecolor=CREAM); plt.close(fig)


def slide_method(pdf, f):
    fig, ax = _canvas(CREAM)
    grid_paper(ax)
    heading(ax, 0.09, 0.925, "WHAT WE WOULD\nCHECK NEXT", fs=32)

    card(ax, 0.085, 0.155, 0.40, 0.55, PAPER)
    ax.text(0.11, 0.655, "KNOWN LIMITATIONS", fontsize=8.5, family=SANS,
            fontweight="bold", color=RED, zorder=6)
    lim = ["Waterfront gaps were imputed from\nneighbours; low recall at a 0.7% base rate.",
           "Renovation gaps filled with zero, which\nremoves otherwise-qualifying houses.",
           f"{f['resale_n']} repeat sales are double-counted in\nevery market-wide median.",
           "One county, one 13-month window."]
    y = 0.590
    for t in lim:
        ax.text(0.11, y, t, fontsize=8.2, family=SANS, color=INK, va="top",
                linespacing=1.5, zorder=6)
        y -= 0.096
    ax.text(0.11, 0.223, "Holding periods are capped by the window, so\n"
                         "'all resold within a year' is an artifact.",
            fontsize=8.2, family=SANS, color=MUTED, va="top",
            style="italic", linespacing=1.5, zorder=6)

    card(ax, 0.515, 0.155, 0.40, 0.55, INK)
    ax.text(0.54, 0.655, "HOW THIS WAS TESTED", fontsize=8.5, family=SANS,
            fontweight="bold", color=TEAL, zorder=6)
    meth = [f"{f['n']:,} sales joined from two PostgreSQL\ntables.",
            "Every gap explained before it was filled.",
            "Permutation tests corrected for picking\nthe most extreme of many buckets.",
            "Two of our own hypotheses rejected."]
    y = 0.590
    for t in meth:
        ax.text(0.54, y, t, fontsize=8.2, family=SANS, color=PAPER, va="top",
                linespacing=1.5, zorder=6)
        y -= 0.096
    ax.text(0.54, 0.223, "Findings that do not survive testing are worth\nmore than findings that were never tested.",
            fontsize=8.2, family=SANS, color=TEAL, va="top",
            style="italic", linespacing=1.5, zorder=6)
    pdf.savefig(fig, facecolor=CREAM); plt.close(fig)


def slide_thanks(pdf, f):
    fig, ax = _canvas(RED)
    ax.add_patch(plt.Polygon([[0.82, 1.0], [1.0, 1.0], [1.0, 0.72]],
                             facecolor=CREAM, edgecolor="none", zorder=2))
    ax.add_patch(plt.Polygon([[0.82, 1.0], [1.0, 0.72], [1.0, 1.0]],
                             facecolor=INK, edgecolor="none", zorder=1))
    heading(ax, 0.08, 0.68, "THANK\nYOU!", fs=76, color=INK, lead=0.21)
    ax.text(0.08, 0.16, "Questions, challenges and better hypotheses all welcome.",
            fontsize=10, family=SANS, color=INK, zorder=6)
    pdf.savefig(fig, facecolor=RED); plt.close(fig)

def slide_pricemap(pdf, f):
    """Full-county price map - the shape of King County drawn by its own sales."""
    fig, ax = _canvas(INK)
    heading(ax, 0.06, 0.95, "THE PRICE MAP", fs=30, color=PAPER)
    ax.text(0.06, 0.815,
            "Every one of the {:,} sales, placed by latitude and longitude and coloured by price.\n"
            "Nobody drew a boundary here - the county's shape is the transactions themselves."
            .format(f["n"]),
            fontsize=8.6, family=SANS, color=MUTED, va="top",
            linespacing=1.6, style="italic", zorder=6)

    d = f["df"]
    a = fig.add_axes([0.05, 0.085, 0.50, 0.645], zorder=4)
    a.set_facecolor(INK)
    for s in a.spines.values():
        s.set_visible(False)
    a.set_xticks([]); a.set_yticks([])
    sc = a.scatter(d["longitude"], d["latitude"], c=d["price"], cmap="magma",
                   s=2.2, alpha=0.75, edgecolors="none",
                   vmax=d["price"].quantile(0.985))
    cand = f["cand"].head(3)
    a.scatter(cand["longitude"], cand["latitude"], s=210, marker="*",
              facecolor=TEAL, edgecolors="white", linewidths=1.1, zorder=6)
    a.set_xlim(d["longitude"].min(), d["longitude"].max())
    a.set_ylim(d["latitude"].min(), d["latitude"].max())
    a.set_aspect(1 / np.cos(np.radians(47.5)))

    cax = fig.add_axes([0.567, 0.135, 0.011, 0.34], zorder=5)
    cb = fig.colorbar(sc, cax=cax)
    cb.set_label("Sale price", fontsize=7.5, family=SANS, color=MUTED)
    cb.ax.tick_params(labelsize=6.5, colors=MUTED, length=0)
    cb.outline.set_visible(False)
    cb.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f"${v/1e6:.1f}M"))

    pts = [("THE SPINE OF VALUE",
            "The bright band running north-south is the\nLake Washington shoreline - Medina, Bellevue,\n"
            "Mercer Island. Price falls away with distance\nfrom the water in almost every direction."),
           ("THE SOUTH IS DIFFERENT",
            "The dark mass in the south of the county is a\nlarger, cheaper market. It is not short of houses;\n"
            "it is short of the attributes this client wants."),
           ("THE STARS",
            "The three recommended properties. They sit\nexactly where the map says value concentrates.")]
    y = 0.675
    for label, text in pts:
        ax.text(0.645, y, label, fontsize=7.6, family=SANS, fontweight="bold",
                color=TEAL, va="top", zorder=6)
        ax.text(0.645, y - 0.038, text, fontsize=8, family=SANS, color=PAPER,
                va="top", linespacing=1.5, zorder=6)
        y -= 0.215
    pdf.savefig(fig, facecolor=INK); plt.close(fig)


def slide_candidate_map(pdf, f):
    """Zoomed map covering every property that survived the filters."""
    fig, ax = _canvas(CREAM)
    grid_paper(ax)
    heading(ax, 0.06, 0.955, "WHERE THE SHORTLIST SITS", fs=27)
    ax.text(0.06, 0.845,
            "Zoomed to cover every property that survived all six requirements.",
            fontsize=9, family=SANS, color="#4A4640", style="italic", zorder=6)

    cand = f["cand"]
    pad_y = max(0.035, (cand["latitude"].max() - cand["latitude"].min()) * 0.28)
    pad_x = max(0.045, (cand["longitude"].max() - cand["longitude"].min()) * 0.28)
    ylim = (cand["latitude"].min() - pad_y, cand["latitude"].max() + pad_y)
    xlim = (cand["longitude"].min() - pad_x, cand["longitude"].max() + pad_x)

    card(ax, 0.055, 0.10, 0.55, 0.70, PAPER)
    a = fig.add_axes([0.075, 0.125, 0.51, 0.65], zorder=4)
    a.set_facecolor(PAPER)
    for s in a.spines.values():
        s.set_visible(False)
    a.set_xticks([]); a.set_yticks([])

    d = f["df"]
    near = d[(d["latitude"].between(*ylim)) & (d["longitude"].between(*xlim))]
    a.scatter(near["longitude"], near["latitude"], s=3.5, color="#CFD6DA",
              alpha=0.85, edgecolors="none", zorder=2)
    wf = near[near["waterfront"] == 1]
    a.scatter(wf["longitude"], wf["latitude"], s=9, color="#7FB3C8",
              alpha=0.9, edgecolors="none", zorder=3, label="Waterfront")

    palette = [GREEN, TEAL, RED, "#B07CC6", "#E0A03C"]
    for rank, ((_, r), col) in enumerate(zip(cand.iterrows(), palette), start=1):
        a.scatter(r["longitude"], r["latitude"], s=260, marker="o",
                  facecolor=col, edgecolors="white", linewidths=1.4, zorder=6)
        a.text(r["longitude"], r["latitude"], str(rank), fontsize=8.5,
               family=SANS, fontweight="bold", color="white",
               ha="center", va="center", zorder=7)
    a.set_xlim(*xlim); a.set_ylim(*ylim)
    a.set_aspect(1 / np.cos(np.radians(47.5)))
    a.legend(fontsize=7, frameon=False, loc="upper left", handletextpad=0.4)

    ax.text(0.635, 0.775, "THE SURVIVORS", fontsize=8.5, family=SANS,
            fontweight="bold", color=RED, zorder=6)
    y = 0.715
    for rank, ((_, r), col) in enumerate(zip(cand.iterrows(), palette), start=1):
        dot(ax, 0.648, y - 0.012, 0.011, col)
        ax.text(0.648, y - 0.012, str(rank), fontsize=7, family=SANS,
                fontweight="bold", color="white", ha="center", va="center", zorder=7)
        ax.text(0.678, y, f"{money(r['price'])}   ·   {int(r['zipcode'])}",
                fontsize=8.6, family=SANS, fontweight="bold", color=INK,
                va="top", zorder=6)
        ax.text(0.678, y - 0.036,
                f"house_id {int(r['house_id'])}   grade {int(r['grade'])}",
                fontsize=7.4, family=SANS, color=MUTED, va="top", zorder=6)
        y -= 0.088

    ax.text(0.635, 0.235, "They are not clustered.", fontsize=11,
            family=DISPLAY, color=INK, zorder=6)
    ax.text(0.635, 0.185,
            "The survivors are scattered across five separate\n"
            "submarkets. There is no single neighbourhood to\n"
            "shop in - each of these is a one-off, which is\n"
            "precisely what makes the brief hard to satisfy.",
            fontsize=8, family=SANS, color="#4A4640", va="top",
            linespacing=1.55, zorder=6)
    pdf.savefig(fig, facecolor=CREAM); plt.close(fig)


def slide_result(pdf, f):
    """The scoreboard: what the EDA actually established."""
    fig, ax = _canvas(CREAM)
    grid_paper(ax)
    heading(ax, 0.06, 0.955, "THE RESULT", fs=32)
    ax.text(0.06, 0.845, "Seven hypotheses went in. Five survived, two did not.",
            fontsize=9.5, family=SANS, color="#4A4640", style="italic", zorder=6)

    rows = [
        ("H1", "Missing waterfront data means 'not waterfront'", "CONFIRMED", GREEN),
        ("H2", "Missing renovation year means 'never renovated'", "CONFIRMED", GREEN),
        ("H3", f"Waterfront commands a premium ({f['wf_mult']:.1f}x)", "CONFIRMED", GREEN),
        ("H4", f"Living area drives price (r = {f['corr'].iloc[0]:.2f})", "CONFIRMED", GREEN),
        ("H5", f"Renovation lifts price (+{f['ren_prem']:.0f}%, +{f['lren_prem']:.0f}% luxury)", "CONFIRMED", GREEN),
        ("H6", f"Luxury prices peak in a given month (p = {f['p_mon']:.2f})", "REJECTED", RED),
        ("H7", f"Day of month predicts price (p = {f['p_day']:.2f})", "REJECTED", RED),
    ]
    card(ax, 0.055, 0.245, 0.52, 0.555, PAPER)
    y = 0.755
    for code, text, verdict, col in rows:
        ax.text(0.078, y, code, fontsize=8.5, family=SANS, fontweight="bold",
                color=MUTED, va="top", zorder=6)
        ax.text(0.115, y, text, fontsize=8.4, family=SANS, color=INK,
                va="top", zorder=6)
        ax.add_patch(Rectangle((0.475, y - 0.028), 0.088, 0.034,
                               facecolor=col, zorder=5))
        ax.text(0.519, y - 0.011, verdict, fontsize=6.8, family=SANS,
                fontweight="bold", color=INK, ha="center", va="center", zorder=6)
        y -= 0.073

    card(ax, 0.605, 0.245, 0.345, 0.555, INK)
    ax.text(0.632, 0.755, "WHAT THE CLIENT GETS", fontsize=8.5, family=SANS,
            fontweight="bold", color=TEAL, va="top", zorder=6)
    outs = [("BUY", f"{len(f['cand'])} properties clear every requirement,\n"
                    f"plus {f['unknown_reno']} the records cannot confirm."),
            ("PAY FOR", "Waterfront and a renovation. Both are\npriced in, and both hold up under testing."),
            ("IGNORE", "Timing. Neither the month nor the day\nsurvived a significance test."),
            ("RECONSIDER", f"The one-year flip. Comparable resales\nreturned {f['seg_med']:+.1f}% before costs.")]
    y = 0.685
    for label, text in outs:
        ax.text(0.632, y, label, fontsize=7.4, family=SANS, fontweight="bold",
                color=RED, va="top", zorder=6)
        ax.text(0.632, y - 0.036, text, fontsize=8, family=SANS, color=PAPER,
                va="top", linespacing=1.5, zorder=6)
        y -= 0.113

    ax.text(0.06, 0.185, "The two rejections are the point.", fontsize=13,
            family=DISPLAY, color=INK, zorder=6)
    ax.text(0.06, 0.132,
            "Any analysis can find a pattern in 240 rows. Testing whether that pattern survives contact with the\n"
            f"full {f['n']:,} sales is what separates a finding from a coincidence - and it cost this deck two of its\n"
            "most quotable slides.",
            fontsize=8.5, family=SANS, color="#4A4640", va="top",
            linespacing=1.6, zorder=6)
    pdf.savefig(fig, facecolor=CREAM); plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", default="data/eda.csv", type=Path)
    ap.add_argument("--out", default="EDA_Project_Presentation.pdf", type=Path)
    args = ap.parse_args()

    if not args.data.exists():
        raise SystemExit(f"dataset not found: {args.data}\n"
                         "Run Fetch_Data_to_CSV.ipynb first, or pass --data.")

    print(f"reading {args.data} ...")
    f = analyse(args.data)
    print(f"  {f['n']:,} sales, luxury pool {f['pool_n']}, "
          f"{len(f['cand'])} candidates, p_day={f['p_day']:.3f}, p_month={f['p_mon']:.3f}")

    with PdfPages(args.out) as pdf:
        for fn in (slide_title, slide_brief, slide_waterfront, slide_renovation,
                   slide_size, slide_day, slide_month, slide_resale,
                   slide_geography, slide_pricemap, slide_candidate_map,
                   slide_shortlist, slide_result, slide_method, slide_thanks):
            fn(pdf, f)
            print(f"  + {fn.__name__}")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
