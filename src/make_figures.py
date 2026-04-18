"""
make_figures.py
---------------
Generates static figures for the Process Book PDF from
`data/cargo_theft_surprise_2024.csv`.

Figures produced (saved to ../assets/):
    fig1_funnel.png               - de Moivre funnel of per-capita incident
                                    rate vs population with 95% bands.
    fig2_surprise_ranked.png      - Horizontal bar chart of signed surprise
                                    per state (ranked).
    fig3_value_vs_rate.png        - Scatter: z-value vs z-rate surprise, per
                                    state. Identifies states that are
                                    distinctive on different axes.
    fig4_rate_distribution.png    - Histogram of incidents/100k with
                                    national mean overlaid.
    fig5_top_value_states.png     - Bar chart of top-10 states by stolen value.
"""

import csv
import math
import os
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "#333333",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.dpi": 180,
    "figure.dpi": 180,
})

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "cargo_theft_surprise_2024.csv")
ASSETS = os.path.join(HERE, "..", "assets")
os.makedirs(ASSETS, exist_ok=True)


def load():
    with open(DATA) as f:
        return list(csv.DictReader(f))


def to_float(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def figure_funnel(rows):
    pops = [to_float(r["population_2024"]) for r in rows]
    rates = [to_float(r["incidents_per_100k"]) / 100_000 for r in rows]
    labels = [r["state_abbr"] for r in rows]
    p_hat = sum(to_float(r["incidents"]) for r in rows) / sum(pops)

    fig, ax = plt.subplots(figsize=(9.2, 5.4))
    # 95% funnel bands.
    xs = sorted(pops)
    ses = [math.sqrt(p_hat * (1 - p_hat) / n) for n in xs]
    upper = [p_hat + 1.96 * s for s in ses]
    lower = [max(0, p_hat - 1.96 * s) for s in ses]
    upper99 = [p_hat + 3.0 * s for s in ses]
    lower99 = [max(0, p_hat - 3.0 * s) for s in ses]
    ax.fill_between(xs, [l * 100_000 for l in lower99], [u * 100_000 for u in upper99],
                    color="#d7d3ee", alpha=0.6, label="±3 SE band")
    ax.fill_between(xs, [l * 100_000 for l in lower], [u * 100_000 for u in upper],
                    color="#a89cd6", alpha=0.7, label="±1.96 SE (95%)")
    ax.axhline(p_hat * 100_000, color="#3b2e7e", linestyle="--", linewidth=1.2,
               label=f"National rate p̂ = {p_hat*100_000:.2f} / 100k")

    # Points.
    ax.scatter(pops, [r * 100_000 for r in rates], s=28, color="#ff6f3c",
               edgecolor="#3b2e7e", linewidth=0.6, zorder=4)
    # Label the outliers.
    pairs = sorted(zip(rates, pops, labels), key=lambda t: -t[0] * 100_000)
    for rate, pop, abbr in pairs[:6]:
        ax.annotate(abbr, (pop, rate * 100_000),
                    textcoords="offset points", xytext=(5, 4), fontsize=9,
                    color="#3b2e7e", fontweight="bold")
    for rate, pop, abbr in pairs[-3:]:
        ax.annotate(abbr, (pop, rate * 100_000),
                    textcoords="offset points", xytext=(5, -10), fontsize=9,
                    color="#444444")

    ax.set_xscale("log")
    ax.set_xlabel("State population (log scale, 2024 incorporated-places estimate)")
    ax.set_ylabel("Cargo theft incidents per 100,000 residents")
    ax.set_title("de Moivre funnel: per-capita cargo theft incident rate vs. population",
                 loc="left", fontsize=12, fontweight="bold", color="#1b1f24")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(axis="y", linewidth=0.4, alpha=0.35)

    out = os.path.join(ASSETS, "fig1_funnel.png")
    plt.tight_layout(); plt.savefig(out); plt.close(fig)
    return out


def figure_surprise_ranked(rows):
    items = sorted(((r["state_abbr"], to_float(r["surprise_display"]))
                    for r in rows), key=lambda t: t[1])
    labels = [t[0] for t in items]
    vals = [t[1] for t in items]
    colors = ["#2166ac" if v < 0 else "#b2182b" for v in vals]

    fig, ax = plt.subplots(figsize=(7.5, 9.5))
    ax.barh(range(len(vals)), vals, color=colors, edgecolor="white", linewidth=0.4)
    ax.set_yticks(range(len(vals)))
    ax.set_yticklabels(labels, fontsize=8.4)
    ax.axvline(0, color="#333", linewidth=0.6)
    ax.set_xlabel("sign(z) · √|z|  (signed surprise on incident rate)")
    ax.set_title("States ranked by Bayesian surprise on the per-capita\ncargo theft incident rate (2024)",
                 loc="left", fontsize=12, fontweight="bold", color="#1b1f24")
    ax.grid(axis="x", linewidth=0.4, alpha=0.35)
    for i, (lbl, v) in enumerate(zip(labels, vals)):
        if abs(v) > 0.3:
            ax.text(v + (0.08 if v > 0 else -0.08), i, f"{v:+.2f}",
                    va="center", ha="left" if v > 0 else "right",
                    fontsize=7.5, color="#333")
    out = os.path.join(ASSETS, "fig2_surprise_ranked.png")
    plt.tight_layout(); plt.savefig(out); plt.close(fig)
    return out


def figure_value_vs_rate(rows):
    xs = [to_float(r["surprise_display"]) for r in rows]
    ys = [to_float(r["value_surprise"]) for r in rows]
    labels = [r["state_abbr"] for r in rows]
    fig, ax = plt.subplots(figsize=(8.4, 6.2))
    ax.scatter(xs, ys, s=40, color="#3b2e7e", alpha=0.7, edgecolor="white", linewidth=0.8)
    ax.axhline(0, color="#777", linewidth=0.5); ax.axvline(0, color="#777", linewidth=0.5)
    # Highlight interesting outliers.
    for x, y, abbr in zip(xs, ys, labels):
        if abs(x) > 3.5 or abs(y) > 1.2:
            ax.annotate(abbr, (x, y), textcoords="offset points", xytext=(5, 4),
                        fontsize=9, color="#b2182b", fontweight="bold")
    ax.set_xlabel("Surprise on incident rate (per-capita)")
    ax.set_ylabel("Surprise on stolen value per capita")
    ax.set_title("States distinctive on rate vs. states distinctive on value",
                 loc="left", fontsize=12, fontweight="bold", color="#1b1f24")
    ax.grid(True, linewidth=0.35, alpha=0.4)
    out = os.path.join(ASSETS, "fig3_value_vs_rate.png")
    plt.tight_layout(); plt.savefig(out); plt.close(fig)
    return out


def figure_rate_distribution(rows):
    rates = [to_float(r["incidents_per_100k"]) for r in rows]
    pops = [to_float(r["population_2024"]) for r in rows]
    incidents = [to_float(r["incidents"]) for r in rows]
    p_hat = sum(incidents) / sum(pops) * 100_000
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.hist(rates, bins=18, color="#a89cd6", edgecolor="white")
    ax.axvline(p_hat, color="#b2182b", linewidth=1.4, linestyle="--",
               label=f"National rate = {p_hat:.2f} / 100k")
    ax.set_xlabel("Cargo theft incidents per 100,000 residents")
    ax.set_ylabel("Number of states")
    ax.set_title("Distribution of per-capita cargo theft rates across U.S. states (2024)",
                 loc="left", fontsize=12, fontweight="bold", color="#1b1f24")
    ax.legend(frameon=False)
    out = os.path.join(ASSETS, "fig4_rate_distribution.png")
    plt.tight_layout(); plt.savefig(out); plt.close(fig)
    return out


def figure_top_value(rows):
    items = sorted(((r["state_abbr"], to_float(r["stolen_value_usd"])) for r in rows),
                   key=lambda t: -t[1])[:12]
    labels = [t[0] for t in items]
    vals = [t[1] / 1_000_000 for t in items]
    fig, ax = plt.subplots(figsize=(8.4, 5))
    bars = ax.bar(labels, vals, color="#ff6f3c", edgecolor="white", linewidth=0.6)
    bars[0].set_color("#3b2e7e")  # Kentucky in accent
    ax.set_ylabel("Stolen value ($ millions)")
    ax.set_title("Kentucky reports 31% of all 2024 cargo theft value from only 70 incidents",
                 loc="left", fontsize=12, fontweight="bold", color="#1b1f24")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 2, f"${v:,.0f}M",
                ha="center", fontsize=8, color="#333")
    ax.grid(axis="y", linewidth=0.4, alpha=0.35)
    out = os.path.join(ASSETS, "fig5_top_value_states.png")
    plt.tight_layout(); plt.savefig(out); plt.close(fig)
    return out


if __name__ == "__main__":
    rows = load()
    print("Generating figures for", len(rows), "states...")
    for fn in (figure_funnel, figure_surprise_ranked, figure_value_vs_rate,
               figure_rate_distribution, figure_top_value):
        p = fn(rows); print("  wrote", os.path.basename(p))
