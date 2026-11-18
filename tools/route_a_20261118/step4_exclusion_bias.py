"""Step 4: exclusion bias, deterministic-anchor triangulation and lexical self-pairing.

(a) Is the strict filter (26,501 -> 6,499) selective by rule-based stage-1 family?
(b) Within strict records, is reaching FULLY_MAPPED (6,499 -> 3,125) selective by family?
(c) Do the 16 depleted core cells already appear depleted in a matrix built only from deterministic
    stage-1 anchors over ALL 26,501 candidates (no LLM, no strict filter)?  -> method triangulation
(d) Lexical self-pairing: share of a cell's records whose AI and Decision anchors are the same term.
"""
import os, re, json
from collections import Counter, defaultdict
import numpy as np
from scipy.stats import chi2_contingency, fisher_exact
import ra_lib as L

OUTD = os.path.join(L.OUT, "04_exclusion_bias")
NONFAM = {"", "UNRESOLVED_NO_ANCHOR", "COLLISION_UNRESOLVED"}


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"),) * 2
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return round(c - h, 4), round(c + h, 4)


def cramers_v(table):
    t = np.asarray(table, float)
    t = t[t.sum(1) > 0][:, t.sum(0) > 0]
    chi2, p, dof, _ = chi2_contingency(t)
    v = np.sqrt(chi2 / (t.sum() * (min(t.shape) - 1)))
    return float(chi2), float(p), int(dof), float(v)


def rate_table(records, key, flag):
    g = defaultdict(lambda: [0, 0])
    for r in records:
        g[key(r)][0] += flag(r)
        g[key(r)][1] += 1
    rows = []
    for k, (a, n) in sorted(g.items(), key=lambda x: -x[1][1]):
        lo, hi = wilson(a, n)
        rows.append({"group": k, "n": n, "included": a, "rate": round(a / n, 4), "ci95_lo": lo, "ci95_hi": hi})
    chi2, p, dof, v = cramers_v([[a, n - a] for a, n in g.values()])
    return rows, {"chi2": round(chi2, 2), "p": p, "dof": dof, "cramers_v": round(v, 4)}


def terms(basis):
    """stage1_basis like 'stage1_anchor:FAM#term|stage1_anchor:FAM#term' -> (left_term, right_term)."""
    parts = basis.split("|")
    get = lambda s: s.split("#", 1)[1] if s.startswith("stage1_anchor:") and "#" in s else None
    return (get(parts[0]) if parts else None, get(parts[1]) if len(parts) > 1 else None)


def main():
    allr = L.read_csv(os.path.join(L.INP, "RECORDS_ALL_26501_from_private_snapshot.csv"))
    strict = {r["record_id"]: r for r in L.read_csv(os.path.join(L.INP, "ANALYTICAL_FREEZE_RECORD_LEVEL.csv"))}
    core = {(r["ai_family"], r["decision_family"]): r["full_sensitivity_robust"] == "True" and r["main_mc_direction"]
            for r in L.read_csv(os.path.join(L.INP, "ROBUSTNESS_COMPARISON_120.csv"))}
    dep = {k for k, v in core.items() if v == "DEPLETED"}
    enr = {k for k, v in core.items() if v == "ENRICHED"}
    inc = lambda r: r["passed_strict_filter"] in ("1", "True", "true")
    rep = {}

    # (a) strict-filter selectivity
    t_ai, s_ai = rate_table(allr, lambda r: r["stage1_left_family"] or "BLANK", inc)
    t_de, s_de = rate_table(allr, lambda r: r["stage1_right_family"] or "BLANK", inc)
    t_sec, s_sec = rate_table(allr, lambda r: r["section_kind"], inc)
    L.write_csv(os.path.join(OUTD, "A_STRICT_INCLUSION_BY_STAGE1_AI_FAMILY.csv"), t_ai)
    L.write_csv(os.path.join(OUTD, "A_STRICT_INCLUSION_BY_STAGE1_DECISION_FAMILY.csv"), t_de)
    L.write_csv(os.path.join(OUTD, "A_STRICT_INCLUSION_BY_SECTION.csv"), t_sec)
    rep["a_strict_filter"] = {"overall_rate": round(sum(map(inc, allr)) / len(allr), 4),
                              "by_ai_family": s_ai, "by_decision_family": s_de, "by_section": s_sec}

    both = [r for r in allr if r["stage1_left_family"] not in NONFAM and r["stage1_right_family"] not in NONFAM]
    grp = lambda r: "DEPLETED_CORE" if (r["stage1_left_family"], r["stage1_right_family"]) in dep else (
        "ENRICHED_CORE" if (r["stage1_left_family"], r["stage1_right_family"]) in enr else "OTHER")
    t_grp, s_grp = rate_table(both, grp, inc)
    L.write_csv(os.path.join(OUTD, "A_STRICT_INCLUSION_BY_CORE_GROUP_BOTH_ANCHORED.csv"), t_grp)
    rep["a_both_anchored_by_core_group"] = {"n": len(both), "table": t_grp, "test": s_grp}

    # (b) full-mapping selectivity inside strict, by stage-1 family of the anchored side
    sm = []
    for r in allr:
        if r["record_id"] in strict:
            sm.append({**r, "full": strict[r["record_id"]]["mapping_completeness"] == "FULLY_MAPPED"})
    t_bai, s_bai = rate_table(sm, lambda r: r["stage1_left_family"] or "BLANK", lambda r: r["full"])
    t_bde, s_bde = rate_table(sm, lambda r: r["stage1_right_family"] or "BLANK", lambda r: r["full"])
    L.write_csv(os.path.join(OUTD, "B_FULL_MAPPING_BY_STAGE1_AI_FAMILY.csv"), t_bai)
    L.write_csv(os.path.join(OUTD, "B_FULL_MAPPING_BY_STAGE1_DECISION_FAMILY.csv"), t_bde)
    rep["b_full_mapping_within_strict"] = {"n": len(sm), "overall_rate": round(sum(r["full"] for r in sm) / len(sm), 4),
                                           "by_ai_family": s_bai, "by_decision_family": s_bde}

    # (c) deterministic-anchor matrix over all candidates (document-deduplicated), exact test
    pairs = L.dedup([(r["document_id"], r["stage1_left_family"], r["stage1_right_family"]) for r in both])
    m = L.matrix(pairs, L.AI_FAMS, L.DEC_FAMS)
    exp, p = L.exact_hyper(m)
    q = L.bh(p.ravel()).reshape(m.shape)
    rows_c, agree = [], Counter()
    for i, a in enumerate(L.AI_FAMS):
        for j, d in enumerate(L.DEC_FAMS):
            oe = m[i, j] / exp[i, j] if exp[i, j] > 0 else float("nan")
            k = (a, d)
            status = "DEPLETED_CORE" if k in dep else "ENRICHED_CORE" if k in enr else "OTHER"
            sdir = "ENRICHED" if m[i, j] > exp[i, j] else "DEPLETED" if m[i, j] < exp[i, j] else "NEUTRAL"
            rows_c.append({"ai_family": a, "decision_family": d, "v9_core_status": status, "stage1_doc_edges": int(m[i, j]),
                           "stage1_expected": round(float(exp[i, j]), 3), "stage1_oe": round(float(oe), 3) if oe == oe else "",
                           "stage1_direction": sdir, "stage1_exact_q": float(q[i, j]), "stage1_q05": bool(q[i, j] <= .05)})
            if status != "OTHER":
                want = status.split("_")[0]
                agree[(status, "same_direction")] += sdir == want
                agree[(status, "same_direction_and_q05")] += (sdir == want and q[i, j] <= .05)
                agree[(status, "opposite_direction_q05")] += (sdir not in (want, "NEUTRAL") and q[i, j] <= .05)
                agree[(status, "zero_expected_or_untestable")] += exp[i, j] < 1
    L.write_csv(os.path.join(OUTD, "C_STAGE1_DETERMINISTIC_MATRIX_120.csv"), rows_c)
    rep["c_stage1_triangulation"] = {"records_both_anchored": len(both), "document_edges": int(m.sum()),
                                     "nonzero_cells": int((m > 0).sum()),
                                     "agreement_with_v9_core": {f"{a}|{b}": v for (a, b), v in sorted(agree.items())},
                                     "note": "Stage-1 anchors are a keyword lexicon applied before the LLM; coverage is partial (many families rarely anchored)."}

    # (d) lexical self-pairing: same matched term anchors both sides
    basis = {r["record_id"]: r["stage1_basis"] for r in allr}
    elig = [r for r in strict.values() if r["mapping_completeness"] == "FULLY_MAPPED"]
    cell = defaultdict(lambda: [0, 0, 0])
    for r in elig:
        k = (r["left_final_family"], r["right_final_family"])
        lt, rt = terms(basis.get(r["record_id"], ""))
        both_s1 = r["left_resolution_stage"] == "STAGE1_DETERMINISTIC_ANCHOR" and r["right_resolution_stage"] == "STAGE1_DETERMINISTIC_ANCHOR"
        cell[k][0] += 1
        cell[k][1] += bool(lt and rt and lt.lower() == rt.lower())
        cell[k][2] += both_s1
    rows_d = []
    for (a, d), (n, same, s1) in sorted(cell.items(), key=lambda x: -x[1][1]):
        st = "DEPLETED_CORE" if (a, d) in dep else "ENRICHED_CORE" if (a, d) in enr else "OTHER"
        rows_d.append({"ai_family": a, "decision_family": d, "v9_core_status": st, "pair_eligible_records": n,
                       "same_term_both_sides": same, "same_term_share": round(same / n, 4),
                       "both_sides_stage1_deterministic": s1, "both_stage1_share": round(s1 / n, 4)})
    L.write_csv(os.path.join(OUTD, "D_LEXICAL_SELF_PAIRING_BY_CELL.csv"), rows_d)
    tot_same = sum(v[1] for v in cell.values())
    rep["d_lexical_self_pairing"] = {
        "pair_eligible_records": len(elig), "records_same_term_both_sides": tot_same,
        "cells_with_any_same_term": sum(1 for v in cell.values() if v[1]),
        "top_cells": [(r["ai_family"] + " x " + r["decision_family"], r["v9_core_status"], r["same_term_both_sides"], r["same_term_share"]) for r in rows_d[:8]],
        "enriched_core_records_same_term": sum(r["same_term_both_sides"] for r in rows_d if r["v9_core_status"] == "ENRICHED_CORE"),
        "enriched_core_records": sum(r["pair_eligible_records"] for r in rows_d if r["v9_core_status"] == "ENRICHED_CORE"),
    }
    L.write_json(os.path.join(OUTD, "EXCLUSION_BIAS_REPORT.json"), rep)
    print(json.dumps(rep, indent=1, ensure_ascii=False, default=str)[:6000])


if __name__ == "__main__":
    main()
