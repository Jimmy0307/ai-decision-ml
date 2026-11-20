"""Figures for the manuscript, drawn only from files in paper/data (the PaperOrchestra plotting stage, done in code).

Palette: dataviz reference palette (categorical slots 1-3 validated for light surface; diverging blue<->red, gray mid).
Run: python paper/scripts/make_figures.py
"""
import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
DATA, FIG = HERE / "data", HERE / "figures"
FIG.mkdir(exist_ok=True)
BLUE, ORANGE, AQUA, RED = "#2a78d6", "#eb6834", "#1baf7a", "#e34948"
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df", "#fcfcfb"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
                     "axes.titlesize": 10, "axes.titleweight": "bold", "axes.titlecolor": INK})
DIVERGING = LinearSegmentedColormap.from_list("rb", [RED, "#f0efec", BLUE])


def save(fig, name):
    fig.savefig(FIG / f"{name}.png", dpi=220, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


def grid(ax, axis="y"):
    ax.grid(axis=axis, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


# 1 ---------------------------------------------------------------- research design diagram
def fig_research_design():
    fig, ax = plt.subplots(figsize=(8.2, 3.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis("off")

    def box(x, y, w, h, title, body, edge):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                                    linewidth=1.2, edgecolor=edge, facecolor="white"))
        ax.text(x + w / 2, y + h - 2.2, title, ha="center", va="top", fontsize=8.5, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 6.6, body, ha="center", va="top", fontsize=6.8, color=INK2, linespacing=1.35)

    box(1, 27, 26.5, 21, "Study 1  Literature", "V5-V11.1: function\nco-occurrence and\nnetwork searches\n\nDirection descriptive only;\nsignificance not robust", MUTED)
    box(36.75, 27, 26.5, 21, "Study 2  Patents", "8.5M US patents; 8 preregistered\nanalyses (1 confirmatory)\n+ exploratory Plan C\n\nDomain: hole not supported\nFirm: unresolved (PARTIAL)", BLUE)
    box(72.5, 27, 26.5, 21, "Study 3  Enterprise", "Plan: discriminates\ncompeting explanations\n(allocation and decision\nrights, data, cost,\nregulation, task fit)", ORANGE)
    box(1, 4, 30, 14, "Systematic review + R1", "204 indexed studies, model-coded\nfrom abstracts; R1: open\nboard data re-analysed", AQUA)
    ax.annotate("", xy=(14.25, 26.4), xytext=(14.25, 18.6), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1))
    ax.text(15.5, 22.5, "how common\nis the inference?", ha="left", va="center", fontsize=5.8, color=INK2, linespacing=1.2)
    box(38, 4, 61, 14, "Multi-level programming model (simulated)", "Formalises only the organisational candidate\nCalibrated only if Study 3 supports that candidate", INK2)
    for x0, x1, lab in ((28.4, 36.3, "co-\noccurrence\nis not flow"), (64.1, 72.0, "which\nconstraint\nbinds?")):
        ax.annotate("", xy=(x1, 34.5), xytext=(x0, 34.5), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1))
        ax.text((x0 + x1) / 2, 36.2, lab, ha="center", va="bottom", fontsize=5.8, color=INK2, linespacing=1.2)
    ax.annotate("", xy=(72, 18.6), xytext=(85.5, 26.4),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.1, ls=(0, (4, 3))))
    ax.text(87, 21.5, "only if\nsupported", ha="left", fontsize=6, color=INK2)
    save(fig, "fig_research_design")


def fig_research_design_en():
    """Journal (English) version of Figure 1: no MLP box; Plans 7-8 shown inside Study 2; Study 3 as a planned box."""
    fig, ax = plt.subplots(figsize=(8.2, 3.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis("off")

    def box(x, y, w, h, title, body, edge, ls="-", tfs=8.5, bfs=6.8):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                                    linewidth=1.2, edgecolor=edge, facecolor="white", linestyle=ls))
        ax.text(x + w / 2, y + h - 2.2, title, ha="center", va="top", fontsize=tfs, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 6.6, body, ha="center", va="top", fontsize=bfs, color=INK2, linespacing=1.35)

    box(1, 27, 26.5, 21, "Study 1  Literature", "V5-V11.1: function\nco-occurrence and\nnetwork searches\n\nDirection descriptive only;\nsignificance not robust", MUTED)
    # Study 2 spans both rows; Plans 7-8 sit inside it as a nested box
    box(35.5, 1.5, 37, 46.5, "Study 2  Patents", "8.5M US patents; 8 preregistered analyses\n(1 confirmatory) + exploratory Plan C\n\nRQ1 domain: hole not supported\nRQ2 firm: unresolved (PARTIAL)", BLUE)
    box(38.5, 4, 31, 15, "Plans 7-8  Co-occurrence vs flow", "16,703 field pairs: co-occurrence gaps\nare flow gaps in 66.8%\nTaxonomy hypothesis not supported", BLUE, tfs=7.6, bfs=6.4)
    box(1, 4, 27, 14, "Systematic review + R1", "204 indexed studies, model-coded\nfrom abstracts; R1: open\nboard data re-analysed", AQUA)
    box(80, 30, 19, 15, "Study 3  Enterprise", "planned; separate\nstudy, no results", ORANGE, ls=(0, (4, 3)), tfs=7.2, bfs=6.4)
    ax.annotate("", xy=(14.25, 26.4), xytext=(14.25, 18.6), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1))
    ax.text(15.5, 22.5, "how common\nis the inference?", ha="left", va="center", fontsize=5.8, color=INK2, linespacing=1.2)
    ax.annotate("", xy=(34.9, 36.5), xytext=(28.4, 36.5), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1))
    ax.text(31.6, 38.2, "co-\noccurrence\nis not flow", ha="center", va="bottom", fontsize=5.8, color=INK2, linespacing=1.2)
    ax.annotate("", xy=(37.9, 11), xytext=(28.9, 11), arrowprops=dict(arrowstyle="-|>", color=AQUA, lw=1.1))
    ax.text(33.4, 12.6, "RQ3", ha="center", va="bottom", fontsize=6.4, fontweight="bold", color=INK2)
    ax.text(33.4, 9.4, "how often,\nand when?", ha="center", va="top", fontsize=5.6, color=INK2, linespacing=1.2)
    ax.annotate("", xy=(79.4, 37.5), xytext=(73.4, 37.5),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.1, ls=(0, (4, 3))))
    ax.text(76.4, 39.2, "which\nconstraint\nbinds?", ha="center", va="bottom", fontsize=5.4, color=INK2, linespacing=1.2)
    save(fig, "fig_research_design_en")


# 2 ---------------------------------------------------------------- Study 1 direction persistence
def fig_study1_direction():
    rows = [r for r in csv.DictReader(open(DATA / "V9_ROBUSTNESS_MASTER_TABLE.csv", encoding="utf-8-sig"))
            if r["direction"] == "DEPLETED" and r["frozen_core"] == "True"]
    rows.sort(key=lambda r: float(r["late_log2_oe"]))
    lab = [f'{r["ai_family"].replace("_", " ").title()} x {r["decision_family"].replace("_", " ").title()}' for r in rows]
    e = np.array([float(r["early_log2_oe"]) for r in rows])
    l = np.array([float(r["late_log2_oe"]) for r in rows])
    y = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    for k in y:
        ax.plot([e[k], l[k]], [k, k], color=GRID, lw=2, zorder=1)
    ax.scatter(e, y, s=34, color=BLUE, zorder=3, label="2023 or earlier", edgecolor=SURF, linewidth=1.2)
    ax.scatter(l, y, s=34, color=ORANGE, zorder=3, label="2024 or later", edgecolor=SURF, linewidth=1.2)
    ax.axvline(0, color=MUTED, lw=0.9)
    ax.text(0.05, len(rows) - 0.4, "O = E", fontsize=7, color=INK2, va="center")
    ax.set_yticks(y, lab, fontsize=6.6)
    ax.set_xlabel("log2(observed / expected)  — left of 0 = under-represented")
    ax.set_title("Study 1: all 16 depleted V9 cells stay depleted in both periods")
    ax.legend(frameon=False, loc="lower right", fontsize=7.5)
    grid(ax, "x")
    save(fig, "fig_study1_direction")


# 3 ---------------------------------------------------------------- patent trend
def fig_patent_trend():
    p = json.load(open(DATA / "PATENT_HOLE_RESULTS.json", encoding="utf-8"))["specs"]["primary"]
    by = [b for b in p["H2"]["by_year"] if b["O"] > 0 and b["year"] >= 2013]
    yr = np.array([b["year"] for b in by])
    oe = np.array([b["OE"] for b in by])
    lo = np.array([b["CI95"][0] for b in by])
    hi = np.array([b["CI95"][1] for b in by])
    med = p["reference"]["median_AI"], p["reference"]["median_DEC"]
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    ax.fill_between(yr, lo, hi, color=BLUE, alpha=0.16, linewidth=0)
    ax.plot(yr, oe, color=BLUE, lw=2, marker="o", ms=4.5, markeredgecolor=SURF, markeredgewidth=1)
    ax.axhline(1, color=MUTED, lw=0.9, ls=(0, (3, 3)))
    ax.axhline(min(med), color=ORANGE, lw=1.2, ls=(0, (5, 3)))
    ax.text(yr[-1], 1.0 - 0.12, "no association (O = E)", fontsize=7, color=INK2, ha="right", va="top")
    ax.text(yr[-1], min(med) + 0.1, f"median OE(DEC, X) over 179 comparable fields ({min(med):.3f}; AI side {max(med):.3f})", fontsize=7, color=INK2, ha="right")
    ax.text(yr[-1] + 0.15, oe[-1], f"{oe[-1]:.2f}", fontsize=7.5, color=INK, va="center")
    ax.text(yr[0] - 0.15, oe[0], f"{oe[0]:.2f}", fontsize=7.5, color=INK, va="center", ha="right")
    ax.set_ylim(0, 5.2)
    ax.set_xticks(yr)
    ax.set_ylabel("OE(AI, Decision)")
    ax.set_xlabel("Citing grant year (applicant citations)")
    ax.set_title("AI and decision patents cite each other 2-4 times the null expectation")
    grid(ax)
    save(fig, "fig_patent_trend")


# 4 ---------------------------------------------------------------- sensitivity forest (H1b ratio)
def fig_patent_sensitivity():
    specs = json.load(open(DATA / "PATENT_HOLE_RESULTS.json", encoding="utf-8"))["specs"]
    names = {"primary": "Primary (applicant citations)", "s1_all_categories": "S1 all citation categories",
             "s2_dec_all_G06Q10": "S2 decision = all G06Q10", "s3_ai_broad": "S3 broadened AI",
             "s4_inventive_only": "S4 inventive codes only", "s5_window_2015": "S5 citing 2015+",
             "s6_bridge_both": "S6 bridge patents on both sides"}
    keys = list(names)[::-1]
    pt = np.array([specs[k]["ratio_point"] for k in keys])
    lo = np.array([specs[k]["ratio_CI95"][0] for k in keys])
    hi = np.array([specs[k]["ratio_CI95"][1] for k in keys])
    y = np.arange(len(keys))
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    ax.hlines(y, lo, hi, color=BLUE, lw=2)
    ax.scatter(pt, y, s=40, color=BLUE, zorder=3, edgecolor=SURF, linewidth=1.2)
    for k in range(len(keys)):
        ax.text(hi[k] + 0.04, y[k], f"{pt[k]:.2f}", va="center", fontsize=7.5, color=INK)
    ax.axvline(1, color=RED, lw=1.2, ls=(0, (4, 3)))
    ax.text(0.98, 0.0, "a hole requires the\nwhole interval < 1", ha="right", va="center", fontsize=7, color=INK2)
    ax.set_yticks(y, [names[k] for k in keys])
    ax.set_xlim(0.5, 2.7)
    ax.set_xlabel("OE(AI, Decision) / OE(AI, other business-method patents), 95% bootstrap CI")
    ax.set_title("H1b fails in every preregistered specification")
    grid(ax, "x")
    save(fig, "fig_patent_sensitivity")


# 5 ---------------------------------------------------------------- CPC matrix heatmaps
def fig_cpc_heatmap():
    rows = ["G06N3", "G06N5", "G06N7", "G06N10", "G06N20", "G06N_OTHER"]
    rlab = ["Neural (G06N3)", "Knowledge (G06N5)", "Probabilistic (G06N7)", "Quantum (G06N10)", "ML (G06N20)", "Other G06N"]
    cols = ["FORECAST_OPTIMISE", "RESOURCE_SCHEDULING", "WORKFLOW", "RISK", "STRATEGY", "PERFORMANCE", "MGMT_GENERAL"]
    clab = ["Forecast", "Resource", "Workflow", "Risk", "Strategy", "Perform.", "Gen. mgmt"]
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.9), sharey=True)
    for ax, part, title in zip(axes, ("A", "B"), ("A  Co-classification (5,316 patents)", "B  Citation flow (30,843 citations)")):
        cells = {(r["ai_family"], r["decision_family"]): r for r in csv.DictReader(open(DATA / f"SUITE_P1_{part}_CELLS.csv", encoding="utf-8-sig"))}
        M = np.full((len(rows), len(cols)), np.nan)
        for i, a in enumerate(rows):
            for j, c in enumerate(cols):
                v = cells[(a, c)]["oe_ratio"]
                M[i, j] = np.log2(max(float(v), 1 / 16)) if v not in ("", None) else np.nan
        im = ax.imshow(M, cmap=DIVERGING, norm=TwoSlopeNorm(vmin=-2, vcenter=0, vmax=2), aspect="auto")
        for i, a in enumerate(rows):
            for j, c in enumerate(cols):
                r = cells[(a, c)]
                txt = f'{float(r["oe_ratio"]):.2f}' if r["oe_ratio"] not in ("", None) else "–"
                core = r["adapted_full_core"] in ("True", True)
                mark = ("▼" if r["main_dir"] == "DEPLETED" else "▲") if core else ""
                small = float(r["expected_independence"]) < 10
                if small:
                    ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor=SURF, edgecolor=MUTED,
                                               hatch="////", linewidth=0))
                ax.text(j, i, f"{txt}\n{mark}" if mark else txt, ha="center", va="center", fontsize=6.2,
                        color=MUTED if small else INK, fontweight="bold" if core else "normal")
        ax.set_xticks(range(len(cols)), clab, fontsize=6.4, rotation=35, ha="right", rotation_mode="anchor")
        ax.set_yticks(range(len(rows)), rlab, fontsize=7)
        ax.set_title(title, fontsize=8.5)
        ax.tick_params(length=0)
        for s in ax.spines.values():
            s.set_visible(False)
    cb = fig.colorbar(im, ax=axes, fraction=0.025, pad=0.02)
    cb.set_label("log2 O/E (red = under, blue = over)", fontsize=7)
    cb.ax.tick_params(labelsize=7)
    fig.suptitle("Within AI x Decision: small cell-level deviations (▼/▲ = adapted full core, BH q ≤ .05)",
                 fontsize=9, fontweight="bold", color=INK, y=1.02)
    fig.text(0.5, -0.04, "Hatched cells: expected count < 10 (small sample; shown, marked and counted, but not interpreted).",
             ha="center", fontsize=7, color=INK2)
    save(fig, "fig_cpc_heatmap")


# 6 ---------------------------------------------------------------- firm-level portfolio null
def fig_firm_null():
    rep = list(csv.DictReader(open(DATA / "FIRM_NULL_REPLICATES.csv", encoding="utf-8")))
    res = json.load(open(DATA / "FIRM_NULL_RESULTS.json", encoding="utf-8"))
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9))
    for ax, key, col, title, xl in (
            (axes[0], "T1", "T1_OE_AI_DEC", "Specialist AI ↔ decision firms", "O/E of ties between specialist firms"),
            (axes[1], "T2", "T2_MIXED_median_constraint", "Mixed-portfolio firms", "Median Burt constraint")):
        for scheme, color, lab in (("primary", BLUE, "null: type × year"), ("S_tech", ORANGE, "null: + technology mix")):
            v = np.array([float(r[col]) for r in rep if r["scheme"] == scheme])
            ax.hist(v, bins=30, color=color, alpha=0.75, label=lab, edgecolor=SURF, linewidth=0.4)
        obs = res["observed"][key]
        ax.axvline(obs, color=INK, lw=1.6)
        ax.text(obs, ax.get_ylim()[1] * 0.92, f" observed {obs:.2f}", fontsize=7.2, color=INK, ha="left" if key == "T2" else "left")
        ax.set_title(title)
        ax.set_xlabel(xl)
        ax.set_ylabel("Replicates (of 1,000)")
        grid(ax)
    axes[0].legend(frameon=False, fontsize=7, loc="upper right")
    s1 = res["primary"]["share_of_T1_gap_reproduced_by_null"]
    s2 = res["S_tech"]["share_of_T1_gap_reproduced_by_null"]
    fig.suptitle(f"Portfolio-preserving null: it reproduces {s1:.0%}–{s2:.0%} of the specialist separation; no brokerage advantage established",
                 fontsize=9, fontweight="bold", color=INK, y=1.03)
    fig.tight_layout()
    save(fig, "fig_firm_null")


# 7 ---------------------------------------------------------------- MLP simulated scenarios
def fig_mlp_scenarios():
    res = json.load(open(DATA / "MLP_SOLVER_RESULTS_v1_0.json", encoding="utf-8"))["results"]
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.6))
    gov = {"C": ("Regime C (K 5.5, risk ×0.85)", BLUE), "F": ("Regime F (K 6.0, risk ×1.00)", ORANGE),
           "D": ("Regime D (K 6.5, risk ×1.15)", AQUA)}
    for ax, key, title in zip(axes, ("F1_best", "realized_value", "residual_risk"),
                              ("Level-1 objective F1", "Realised value", "Residual risk")):
        for g, (lab, color) in gov.items():
            pts = sorted((r["budget"], r[key]) for r in res if r["governance"] == g)
            ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=2, marker="o", ms=4.5,
                    markeredgecolor=SURF, markeredgewidth=1, label=lab)
            ax.text(pts[-1][0] + 0.15, pts[-1][1], g, color=INK2, fontsize=7.5, va="center")
        ax.set_title(title)
        ax.set_xlabel("Budget B_tot")
        ax.set_xticks([3, 5, 7])
        ax.set_xlim(2.6, 7.7)
        grid(ax)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.suptitle("Simulated tri-level prototype (all coefficients synthetic; no firm data)", fontsize=9,
                 fontweight="bold", color=INK, y=1.04)
    fig.tight_layout()
    fig.legend(handles, labels, frameon=False, fontsize=7, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.1))
    save(fig, "fig_mlp_scenarios")


# 8 ---------------------------------------------------------------- Plan C: where the connection runs (exploratory)
def fig_plan_c_locus():
    r = json.load(open(DATA / "PLAN_C_RESULTS.json", encoding="utf-8"))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.2, 3.0), gridspec_kw={"width_ratios": [1, 1.25]})
    yrs = sorted(r["C1_bridge_by_year"], key=int)
    sh = [100 * r["C1_bridge_by_year"][y]["share"] for y in yrs]
    a1.plot([int(y) for y in yrs], sh, color=BLUE, lw=2, marker="o", ms=4)
    for y, v in zip(yrs, sh):
        if y in ("2010", "2023", "2025"):
            a1.annotate(f"{v:.1f}%", (int(y), v), textcoords="offset points", xytext=(0, -12 if y == "2025" else 6),
                        ha="center", fontsize=7, color=INK2)
    a1.set_xticks([2010, 2013, 2016, 2019, 2022, 2025])
    a1.set_ylim(0, 6.5)
    a1.set_ylabel("BRIDGE patents (% of in-scope)")
    a1.set_title("Co-classified in AI and DEC (not flow)", fontsize=9)
    grid(a1)
    cats = [("within_firm", "Within firm"), ("between_mixed_citing", "Between firms,\nMIXED firm citing"),
            ("between_specialist_citing", "Between firms,\nspecialists citing"), ("unowned_end", "Unowned end")]
    yy = np.arange(len(cats))[::-1]
    h = 0.36
    cross = [100 * r["C2_locus_cross"][k]["share"] for k, _ in cats]
    allc = [100 * r["C2_locus_all"][k]["share"] for k, _ in cats]
    b1 = a2.barh(yy + h / 2, cross, h, color=BLUE, label="AI↔DEC cross citations")
    b2 = a2.barh(yy - h / 2, allc, h, color=ORANGE, label="All in-scope citations")
    for bars in (b1, b2):
        for b in bars:
            a2.text(b.get_width() + 1, b.get_y() + b.get_height() / 2, f"{b.get_width():.1f}%", va="center", fontsize=7, color=INK2)
    a2.set_yticks(yy)
    a2.set_yticklabels([l for _, l in cats], fontsize=7.5)
    a2.set_xlim(0, 80)
    a2.set_xlabel("Share of applicant citations (%)")
    a2.set_title("Where citations run (2013–2025)", fontsize=9)
    a2.legend(frameon=False, fontsize=7, loc="lower right")
    grid(a2, "x")
    fig.tight_layout()
    save(fig, "fig_plan_c_locus")


# 9 ---------------------------------------------------------------- Plan 7: co-occurrence vs flow across field pairs
def fig_plan7_cooc_flow():
    r = json.load(open(DATA / "PLAN7_RESULTS.json", encoding="utf-8"))
    p = r["specs"]["primary"]
    rows = [x for x in csv.DictReader(open(DATA / "PLAN7_PAIRS_primary.csv", encoding="utf-8")) if x["eligible"] == "True"]
    oc = np.array([float(x["OE_co"]) for x in rows])
    of = np.array([float(x["OE_flow"]) for x in rows])
    floor_c, floor_f = 2e-3, 1e-2
    xc = np.log10(np.where(oc > 0, oc, floor_c))
    yf = np.log10(np.where(of > 0, of, floor_f))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.2, 3.4), gridspec_kw={"width_ratios": [1.25, 1]})
    hb = a1.hexbin(xc, yf, gridsize=45, bins="log", cmap=LinearSegmentedColormap.from_list("b", ["#e9f1fb", BLUE, "#123e75"]),
                   mincnt=1, linewidths=0)
    tc, tf = np.log10(p["threshold_co"]), np.log10(p["threshold_flow"])
    a1.axvline(tc, color=INK2, lw=1, ls="--")
    a1.axhline(tf, color=INK2, lw=1, ls="--")
    a1.axhline(0, color=MUTED, lw=0.8)
    for x in r["ai_dec_pairs"]:
        a1.plot(np.log10(max(x["OE_co"], floor_c)), np.log10(max(x["OE_flow"], floor_f)), "o", ms=6, color=ORANGE,
                markeredgecolor="white", markeredgewidth=1.2)
    a1.annotate("AI × DEC pairs", xy=(np.log10(2.7), np.log10(2.9)), xytext=(np.log10(40), np.log10(1.5)),
                fontsize=7, color=INK2, ha="center", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    a1.text(tc - 0.05, 1.05, "co-occurrence\ngap ←", fontsize=7, color=INK2, ha="right", va="top")
    a1.text(1.15, tf - 0.08, "flow gap", fontsize=7, color=INK2, ha="right", va="top")
    a1.set_xticks([np.log10(floor_c), -2, -1, 0, 1])
    a1.set_xticklabels(["0", "0.01", "0.1", "1", "10"])
    a1.set_yticks([-2, -1, 0, 1])
    a1.set_yticklabels(["0.01", "0.1", "1", "10"])
    a1.set_xlabel("Co-classification O/E (co-occurrence)")
    a1.set_ylabel("Citation O/E (flow)")
    a1.set_title(f"{p['eligible_pairs']:,} field pairs", fontsize=9)
    cb = fig.colorbar(hb, ax=a1, fraction=0.04, pad=0.02)
    cb.set_label("pairs", fontsize=7)
    cb.ax.tick_params(labelsize=6)
    specs = [("primary", "Primary (quartile)"), ("S2_all_categories", "All citation types"), ("S3_E20", "E ≥ 20"),
             ("S5_2013_2018", "2013–2018"), ("S5_2019_2025", "2019–2025"), ("S1_strict", "O/E ≤ 0.5 rule")]
    yy = np.arange(len(specs))[::-1]
    ppv = [100 * r["specs"][k]["PPV"] for k, _ in specs]
    rr = [100 * r["specs"][k]["reversal_rate"] for k, _ in specs]
    h = 0.36
    a2.barh(yy + h / 2, ppv, h, color=BLUE, label="Co-occurrence gap is also a flow gap")
    a2.barh(yy - h / 2, rr, h, color=ORANGE, label="Reversal: flow above expectation")
    lo, hi = (100 * v for v in p["PPV_ci95"])
    a2.plot([lo, hi], [yy[0] + h / 2] * 2, color=INK, lw=1.2)
    for k, (y, v) in enumerate(zip(yy, ppv)):
        a2.text((hi if k == 0 else v) + 1, y + h / 2, f"{v:.0f}%", va="center", fontsize=7, color=INK2)
    for y, v in zip(yy, rr):
        a2.text(v + 1, y - h / 2, f"{v:.0f}%", va="center", fontsize=7, color=INK2)
    a2.axvline(25, color=MUTED, lw=0.8, ls=":")
    a2.text(25.5, yy[-1] - 0.75, "chance 25%", fontsize=6.5, color=MUTED)
    a2.set_yticks(yy)
    a2.set_yticklabels([l for _, l in specs], fontsize=7.5)
    a2.set_xlim(0, 100)
    a2.set_ylim(-1.1, len(specs) - 0.4)
    a2.set_xlabel("Share of co-occurrence gaps (%)")
    a2.set_title("How often the inference holds", fontsize=9)
    a2.legend(frameon=False, fontsize=6.5, loc="upper center", bbox_to_anchor=(0.45, -0.2), ncol=1)
    grid(a2, "x")
    fig.tight_layout()
    save(fig, "fig_plan7_cooc_flow")


if __name__ == "__main__":
    fig_research_design()      # Chinese thesis (keeps the MLP box)
    fig_research_design_en()   # English journal version (no MLP box)
    fig_study1_direction()
    fig_patent_trend()
    fig_patent_sensitivity()
    fig_cpc_heatmap()
    fig_firm_null()
    fig_mlp_scenarios()
    fig_plan_c_locus()
    fig_plan7_cooc_flow()
