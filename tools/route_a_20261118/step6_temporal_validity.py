"""Step 6: temporal (predictive) validity of functional under-integration — EXPLORATORY on frozen labels.

Split (fixed before looking at outcomes): EARLY = publication year <= 2023, LATE = >= 2024.
Statistic per cell: L = log2((O+0.5)/(E+0.5)) within a period (E = independence expectation of that period).
Test 1 (persistence of the 16 frozen depleted cells): mean over the 16 cells of L_late - L_early.
Test 2 (prediction): cells depleted in EARLY (L_early < 0 and early exact q <= .10) -> mean change in LATE.
Null: permute document years across documents (period sizes fixed), recompute everything including the
early-period selection in Test 2, so regression to the mean is reproduced by the null. 2,000 permutations.
"""
import os, json
import numpy as np
import ra_lib as L

OUTD = os.path.join(L.OUT, "06_temporal_validity")
P = 2000


def lmat(edges_idx, n_ai, n_de, mask):
    m = np.bincount(edges_idx[mask], minlength=n_ai * n_de).reshape(n_ai, n_de).astype(float)
    exp = np.outer(m.sum(1), m.sum(0)) / m.sum()
    return m, exp, np.log2((m + 0.5) / (exp + 0.5))


def early_selection(m, exp, qthr=0.10):
    _, p = L.exact_hyper(m.astype(int))
    q = L.bh(p.ravel()).reshape(m.shape)
    return (m < exp) & (q <= qthr)


def main():
    docs = {r["document_id"]: r for r in L.read_csv(os.path.join(L.INP, "DOCS_2118_from_private_snapshot.csv"))}
    edges = L.load_official_edges()
    rc = {(r["ai_family"], r["decision_family"]): r for r in L.read_csv(os.path.join(L.INP, "ROBUSTNESS_COMPARISON_120.csv"))}
    ai_i = {a: i for i, a in enumerate(L.AI_FAMS)}; de_i = {d: j for j, d in enumerate(L.DEC_FAMS)}
    k = len(L.DEC_FAMS)
    idx = np.array([ai_i[a] * k + de_i[d] for _, a, d in edges])
    doc_list = sorted({d for d, _, _ in edges})
    dpos = {d: i for i, d in enumerate(doc_list)}
    edge_doc = np.array([dpos[d] for d, _, _ in edges])
    year = np.array([int(docs[d]["year"]) for d in doc_list])
    early_doc = year <= 2023
    dep = np.zeros((len(L.AI_FAMS), k), bool)
    for (a, d), r in rc.items():
        if r["full_sensitivity_robust"] == "True" and r["main_mc_direction"] == "DEPLETED":
            dep[ai_i[a], de_i[d]] = True

    def stats(edoc_early):
        e_mask = edoc_early[edge_doc]
        me, ee, le = lmat(idx, len(L.AI_FAMS), k, e_mask)
        ml, el, ll = lmat(idx, len(L.AI_FAMS), k, ~e_mask)
        t1 = float((ll - le)[dep].mean())
        sel = early_selection(me, ee)
        t2 = float((ll - le)[sel].mean()) if sel.any() else float("nan")
        return t1, t2, int(sel.sum()), (me, ee, le, ml, el, ll, sel)

    t1, t2, nsel, (me, ee, le, ml, el, ll, sel) = stats(early_doc)
    rng = np.random.default_rng(20261206)
    n1 = []; n2 = []
    for _ in range(P):
        perm = rng.permutation(early_doc)
        a, b, _, _ = stats(perm)
        n1.append(a); n2.append(b)
    n1 = np.array(n1); n2 = np.array(n2)
    n2v = n2[~np.isnan(n2)]
    p1_two = float(min(1, 2 * min((1 + (n1 >= t1).sum()) / (P + 1), (1 + (n1 <= t1).sum()) / (P + 1))))
    p2_up = float((1 + (n2v >= t2).sum()) / (len(n2v) + 1)) if t2 == t2 else float("nan")
    rows = []
    for (a, d), r in rc.items():
        i, j = ai_i[a], de_i[d]
        rows.append({"ai_family": a, "decision_family": d, "frozen_core": r["full_sensitivity_robust"] == "True" and r["main_mc_direction"],
                     "early_observed": int(me[i, j]), "early_expected": round(float(ee[i, j]), 3), "early_log2_oe": round(float(le[i, j]), 3),
                     "late_observed": int(ml[i, j]), "late_expected": round(float(el[i, j]), 3), "late_log2_oe": round(float(ll[i, j]), 3),
                     "change": round(float(ll[i, j] - le[i, j]), 3), "early_selected_depleted": bool(sel[i, j])})
    rep = {
        "split": "EARLY <= 2023, LATE >= 2024 (publication year from document metadata)",
        "documents": {"early": int(early_doc.sum()), "late": int((~early_doc).sum())},
        "edges": {"early": int(early_doc[edge_doc].sum()), "late": int((~early_doc[edge_doc]).sum())},
        "test1_frozen_16_depleted": {"mean_change_log2_oe": round(t1, 4), "null_mean": round(float(n1.mean()), 4),
                                     "null_sd": round(float(n1.std()), 4), "p_two_sided": p1_two,
                                     "early_still_depleted": int(((le < 0) & dep).sum()), "late_still_depleted": int(((ll < 0) & dep).sum())},
        "test2_early_selected_depleted": {"cells_selected": nsel, "mean_change_log2_oe": round(t2, 4) if t2 == t2 else None,
                                          "null_mean": round(float(n2v.mean()), 4), "null_sd": round(float(n2v.std()), 4),
                                          "p_upper_convergence": p2_up, "permutations_with_selection": int(len(n2v))},
        "interpretation_guard": "Exploratory on frozen (unreliable) labels; convergence would not by itself show that gaps were 'filled by research'.",
    }
    L.write_csv(os.path.join(OUTD, "TEMPORAL_CELLS_120.csv"), rows)
    L.write_json(os.path.join(OUTD, "TEMPORAL_VALIDITY_REPORT.json"), rep)
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
