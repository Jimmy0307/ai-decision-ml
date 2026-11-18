"""One row per frozen core cell (plus the boundary cells) with its status under every route-A check."""
import os
import ra_lib as L

O = L.OUT
k = lambda r: (r["ai_family"], r["decision_family"])
rc = {k(r): r for r in L.read_csv(os.path.join(L.INP, "ROBUSTNESS_COMPARISON_120.csv"))}
seed = {k(r): r for r in L.read_csv(os.path.join(O, "03_pipeline_validation", "SEED_STABILITY_120.csv"))}
tri = {k(r): r for r in L.read_csv(os.path.join(O, "04_exclusion_bias", "C_STAGE1_DETERMINISTIC_MATRIX_120.csv"))}
st = {k(r): r for r in L.read_csv(os.path.join(O, "04_exclusion_bias", "E_SAME_TERM_REMOVED_RESULTS_120.csv"))}
tr = {k(r): r for r in L.read_csv(os.path.join(O, "05_track_sensitivity", "TRACK_SENSITIVITY_120.csv"))}
tm = {k(r): r for r in L.read_csv(os.path.join(O, "06_temporal_validity", "TEMPORAL_CELLS_120.csv"))}
rows = []
for c, r in rc.items():
    frozen = r["full_sensitivity_robust"] == "True"
    s = seed[c]
    if not frozen and float(s["core_frequency"]) == 0:
        continue
    d = r["main_mc_direction"]
    q05 = lambda x: float(x) <= .05
    rows.append({
        "ai_family": c[0], "decision_family": c[1], "frozen_core": frozen, "direction": d,
        "observed": int(r["dedup_observed"]),
        "seed_core_frequency_20": s["core_frequency"],
        "stage1_keyword_same_direction": tri[c]["stage1_direction"] == d, "stage1_keyword_q05": tri[c]["stage1_q05"] == "True",
        "same_term_removed_full_core": st[c]["full_core"] == "True",
        "track_stratified_q05_same_dir": tr[c]["stratified_dir"] == d and q05(tr[c]["stratified_q"]),
        "ai_track_same_dir": tr[c]["AI_track_dir"] == d, "decision_track_same_dir": tr[c]["DECISION_track_dir"] == d,
        "early_log2_oe": tm[c]["early_log2_oe"], "late_log2_oe": tm[c]["late_log2_oe"],
    })
for r in rows:
    e, l = float(r["early_log2_oe"]), float(r["late_log2_oe"])
    persists = (e < 0 and l < 0) if r["direction"] == "DEPLETED" else (e > 0 and l > 0)
    r["same_sign_both_periods"] = persists
    checks = [r["stage1_keyword_same_direction"], r["same_term_removed_full_core"], r["track_stratified_q05_same_dir"], persists]
    r["checks_passed_of_4"] = sum(bool(x) for x in checks)
    f = float(r["seed_core_frequency_20"])
    r["classification"] = ("STABLE_CORE" if f >= 0.95 and r["checks_passed_of_4"] >= 3 else
                           "BOUNDARY_MC" if 0 < f < 0.95 else "CORE_BUT_FRAGILE" if f >= 0.95 else "NOT_CORE")
rows.sort(key=lambda r: (r["direction"], -float(r["seed_core_frequency_20"]), r["ai_family"]))
L.write_csv(os.path.join(O, "ROBUSTNESS_MASTER_TABLE.csv"), rows)
from collections import Counter
print(Counter((r["direction"], r["classification"]) for r in rows))
for r in rows:
    print(r["direction"][:3], r["classification"].ljust(16), r["seed_core_frequency_20"], r["checks_passed_of_4"], r["ai_family"], "x", r["decision_family"])
