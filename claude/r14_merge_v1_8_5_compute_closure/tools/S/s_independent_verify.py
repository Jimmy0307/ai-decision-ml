"""Independent verification of the revised run (stdlib only; imports no pipeline, applier or comparison code).

Re-reads output files and recomputes: global counts, edges, 120-cell observed/k_a/k_d/E, raw counts,
exact hypergeometric p (math.comb), BH q for all four methods, robust predicate + direction, G01-G16,
and the 50 label applications. Usage: python -I -B s_independent_verify.py <out_json>
"""
import csv
import json
import math
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(r"C:\NTUST_PAPER\outputs\00_CURRENT\06_COMPUTE_CLOSURE_V1_8_5")
REV = ROOT / r"compute_closure\revised_audited_label_analysis\20261014T042729Z"
BFZ = ROOT / r"work\run_inputs_baseline_20261014T041645Z\09_ANALYTICAL_FREEZE\analytical_freeze_v2_20260918T132206Z"
RFZ = REV / r"09_ANALYTICAL_FREEZE\analytical_freeze_v2_BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1"
MAN = Path(r"C:\NTUST_PAPER\outputs\00_CURRENT\02_STUDY1_FREEZE\02_STUDY1_FREEZE_V1_8_1\repo\claude\r14_merge_v1_8_5_compute_closure\44_PROPAGATION_RECORD_MANIFEST.csv")
GCSV = ROOT / r"work\inputs_S_sidecar_corrected_20261014\11_Priority_Gaps_Frozen_Export_G01_G16_v1_0_20261009.csv"
FIELDS = ["analytical_pair_eligible", "left_final_family", "right_final_family", "left_final_status", "right_final_status",
          "mapping_completeness", "analytical_exclusion_reason"]


def rows(p):
    with Path(p).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def latest(sd):
    return Path(next((REV / sd).glob("LATEST_*.txt")).read_text(encoding="utf-8").strip())


def bh(ps):
    n = len(ps)
    order = sorted(range(n), key=lambda i: ps[i])
    q = [0.0] * n
    prev = 1.0
    for rank in range(n, 0, -1):
        i = order[rank - 1]
        prev = min(prev, ps[i] * n / rank)
        q[i] = min(prev, 1.0)
    return q


def hyper(O, ka, kd, M):
    tot = math.comb(M, kd)
    lo, hi = max(0, kd - (M - ka)), min(ka, kd)
    pmf = {x: Fraction(math.comb(ka, x) * math.comb(M - ka, kd - x), tot) for x in range(lo, hi + 1)}
    up = float(sum(v for x, v in pmf.items() if x >= O))
    low = float(sum(v for x, v in pmf.items() if x <= O))
    return up, low, min(1.0, 2 * min(up, low))


def rel(a, b):
    return abs(a - b) / max(abs(a), abs(b), 1e-300)


def main():
    out = {}
    d10, d11, d12, d13 = (latest(s) for s in ("10_DOCUMENT_DEDUP_MATRIX", "11_NULL_MODEL_NETWORK", "12_ROBUSTNESS_SENSITIVITY", "13_RESULTS_FREEZE"))
    rec, eli = rows(RFZ / "ANALYTICAL_FREEZE_RECORD_LEVEL.csv"), rows(RFZ / "ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv")
    flag = [r for r in rec if r["analytical_pair_eligible"].strip().lower() in ("true", "1", "yes")]
    edges = {(r["document_id"], r["left_final_family"].upper(), r["right_final_family"].upper()) for r in flag}
    efile = {(r["document_id"], r["ai_family"], r["decision_family"]) for r in rows(d10 / "DOCUMENT_PAIR_EDGES_DEDUP.csv")}
    out["global"] = {"strict_records": len(rec), "pair_eligible_flag": len(flag), "pair_eligible_file": len(eli),
                     "unique_documents": len({r["document_id"] for r in flag}), "document_edges_recomputed": len(edges),
                     "edge_set_equals_file": edges == efile}
    M = len(edges)
    O = Counter((a, d) for _, a, d in edges)
    raw = Counter((r["left_final_family"].upper(), r["right_final_family"].upper()) for r in flag)
    ka = Counter(a for _, a, _ in edges)
    kd = Counter(d for _, _, d in edges)
    rka = Counter(r["left_final_family"].upper() for r in flag)
    rkd = Counter(r["right_final_family"].upper() for r in flag)
    main_ = rows(d11 / "CELL_NULL_MODEL_RESULTS_120.csv")
    ex, dn, rw, cmp_ = (rows(d12 / f) for f in ("EXACT_HYPERGEOMETRIC_RESULTS_120.csv", "DOCUMENT_PRESERVING_NULL_RESULTS_120.csv",
                                                 "RAW_RECORD_EXACT_SENSITIVITY_120.csv", "ROBUSTNESS_COMPARISON_120.csv"))
    cells = {(r["ai_family"], r["decision_family"]) for r in main_}
    c = {"cells": len(cells), "ai_families": len({a for a, _ in cells}), "decision_families": len({d for _, d in cells})}
    c["observed_mismatch"] = sum(int(r["observed"]) != O[(r["ai_family"], r["decision_family"])] for r in main_)
    c["degree_mismatch"] = sum(int(r["ai_degree"]) != ka[r["ai_family"]] or int(r["decision_degree"]) != kd[r["decision_family"]] for r in main_)
    c["E_max_rel_diff"] = max(rel(float(r["independence_expected"]), ka[r["ai_family"]] * kd[r["decision_family"]] / M) for r in main_)
    c["raw_observed_mismatch"] = sum(int(r["observed"]) != raw[(r["ai_family"], r["decision_family"])] for r in rw)
    # exact hypergeometric (dedup) and raw-record exact recomputed with math.comb
    for name, tab, cnt, A, D, MM in (("exact", ex, O, ka, kd, M), ("raw", rw, raw, rka, rkd, len(flag))):
        mx = 0.0
        for r in tab:
            k = (r["ai_family"], r["decision_family"])
            up, lo, two = hyper(cnt[k], A[k[0]], D[k[1]], MM)
            mx = max(mx, rel(up, float(r["p_upper"])), rel(lo, float(r["p_lower"])), rel(two, float(r["p_two_sided"])))
        c[f"{name}_p_max_rel_diff"] = mx
    # BH re-adjustment for all four methods
    for name, tab in (("main", main_), ("exact", ex), ("document_null", dn), ("raw", rw)):
        q = bh([float(r["p_two_sided"]) for r in tab])
        c[f"{name}_bh_max_abs_diff"] = max(abs(a - float(r["q_bh_two_sided"])) for a, r in zip(q, tab))
    out["cells"] = c
    out["counts"] = {"primary_q05": sum(float(r["q_bh_two_sided"]) <= .05 for r in main_),
                     "primary_q01": sum(float(r["q_bh_two_sided"]) <= .01 for r in main_)}
    # robust predicate re-applied from q/direction columns
    pred = {}
    for r in cmp_:
        dirs = {r["main_mc_direction"], r["exact_direction"], r["document_null_direction"], r["raw_direction"]}
        if all(float(r[q]) <= .05 for q in ("main_mc_q", "exact_q", "document_null_q", "raw_q")) and len(dirs) == 1 and dirs <= {"ENRICHED", "DEPLETED"}:
            pred[(r["ai_family"], r["decision_family"])] = dirs.pop()
    core = {(r["ai_family"], r["decision_family"]): r["direction"] for r in rows(d13 / "FINAL_ROBUST_CORE_32.csv")}
    stat = {}
    for r in rows(d13 / "FINAL_ROBUST_STATUS_MATRIX_10X12.csv"):
        for k, v in r.items():
            if k != "AI_FAMILY" and v != "NOT_ROBUST":
                stat[(r["AI_FAMILY"], k)] = v
    # cross-source check of directions in comparison vs per-method files
    out["robust"] = {"predicate_core": len(pred), "enriched": sum(v == "ENRICHED" for v in pred.values()),
                     "depleted": sum(v == "DEPLETED" for v in pred.values()), "predicate_eq_core_file": pred == core,
                     "predicate_eq_status_matrix": pred == stat}
    G = []
    for r in rows(GCSV):
        k = (r["AI_Family"], r["Decision_Family"])
        G.append({"G": r["Gap_ID"], "in_core": k in pred, "direction": pred.get(k, "")})
    out["G01_G16"] = {"members": sum(g["in_core"] for g in G), "depleted": sum(g["direction"] == "DEPLETED" for g in G),
                      "removed": sum(not g["in_core"] for g in G), "direction_changed": sum(g["in_core"] and g["direction"] != "DEPLETED" for g in G)}
    # 50 applications
    man = rows(MAN)
    rb = {r["record_id"]: r for r in rows(BFZ / "ANALYTICAL_FREEZE_RECORD_LEVEL.csv")}
    rr = {r["record_id"]: r for r in rec}
    tgt = {m["record_id"] for m in man}
    out["applications"] = {"targets": len(man), "matched": sum(m["record_id"] in rr for m in man),
                           "final_values_applied": sum(all(rr[m["record_id"]][f] == m[f"final_{f}"] for f in FIELDS) for m in man),
                           "field_changing": sum(any(rr[k][f] != rb[k][f] for f in FIELDS) for k in tgt),
                           "non_target_rows_changed": sum(rr[k] != rb[k] for k in rb if k not in tgt),
                           "record_sets_equal": set(rr) == set(rb)}
    ok = (out["global"]["strict_records"] == 6499 and out["global"]["edge_set_equals_file"] and c["cells"] == 120 and c["ai_families"] == 10
          and c["decision_families"] == 12 and c["observed_mismatch"] == 0 and c["degree_mismatch"] == 0 and c["raw_observed_mismatch"] == 0
          and c["E_max_rel_diff"] < 1e-12 and c["exact_p_max_rel_diff"] < 1e-9 and c["raw_p_max_rel_diff"] < 1e-9
          and max(c[f"{n}_bh_max_abs_diff"] for n in ("main", "exact", "document_null", "raw")) < 1e-12
          and out["robust"]["predicate_eq_core_file"] and out["robust"]["predicate_eq_status_matrix"]
          and out["applications"]["targets"] == out["applications"]["matched"] == out["applications"]["final_values_applied"] == 50
          and out["applications"]["non_target_rows_changed"] == 0)
    out["INDEPENDENT_VERIFICATION"] = "PASS" if ok else "FAIL"
    Path(sys.argv[1]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
