"""Step 7: probabilistic misclassification sensitivity (no new human coding).

Question: if the family labels are as error-prone as the existing human audits suggest, would the 16
depleted (and 16 enriched) core cells still appear?

For every simulated draw, each of the 3,125 pair-eligible records gets a "true" label pair drawn from an
error model conditioned on its model label; records whose true AI or Decision side is NONE (human
AMBIGUOUS/UNMAPPED) or that a human would EXCLUDE are dropped. The matrix is rebuilt (document-level
dedup) and tested with the exact hypergeometric test (BH, 120 cells) and the raw-record exact test.
The exact test reproduces the main Monte Carlo q<=.05 set at Jaccard .98 (step 3), so it is used as the
fast stand-in; the document-preserving null is run on a subset of draws.

Scenarios
  E1  first coder (n=50) treated as truth — row-smoothed P(human | model)
  E2  reconciled final labels (n=20) treated as truth — row-smoothed
  E3  non-differential random misclassification grid: error 20/40/60% per side, 20% record drop
Smoothing: posterior mean with k pseudo-counts toward the pooled profile
  P(keep)=pooled agreement, P(NONE)=pooled none-rate, rest spread over other families by human marginal.
"""
import os, sys, json
from collections import Counter, defaultdict
import numpy as np
import ra_lib as L

OUTD = os.path.join(L.OUT, "07_misclassification")
NONE_LABELS = {"AMBIGUOUS", "UNMAPPED", "", "NONE"}
N_DRAWS = int(sys.argv[1]) if len(sys.argv) > 1 else 400
K_SMOOTH = 5.0


def error_model(pairs, fams, k=K_SMOOTH):
    """pairs: (model_label, human_label). Returns {model_label: (labels, probs)} over fams + NONE."""
    labels = fams + ["NONE"]
    hm = Counter("NONE" if h in NONE_LABELS else h for _, h in pairs)
    n = len(pairs)
    keep = sum(m == h for m, h in pairs) / n
    none = hm["NONE"] / n
    other = max(0.0, 1 - keep - none)
    sub = {f: hm[f] + 0.5 for f in fams}
    rows = {}
    for m in fams:
        prof = np.array([keep if f == m else 0.0 for f in fams] + [none])
        o = np.array([0.0 if f == m else sub[f] for f in fams] + [0.0])
        prof = prof + other * o / o.sum()
        c = Counter("NONE" if h in NONE_LABELS else h for mm, h in pairs if mm == m)
        cnt = np.array([c[f] for f in fams] + [c["NONE"]], float)
        post = (cnt + k * prof) / (cnt.sum() + k)
        rows[m] = (labels, post / post.sum())
    return rows, {"n": n, "pooled_keep": round(keep, 3), "pooled_none": round(none, 3), "pooled_other": round(other, 3)}


def random_model(fams, marg, err, none_rate=0.0):
    labels = fams + ["NONE"]
    rows = {}
    for m in fams:
        p = np.array([(1 - err) if f == m else 0.0 for f in fams] + [none_rate])
        o = np.array([0.0 if f == m else marg[f] for f in fams] + [0.0])
        p = p + max(0.0, err - none_rate) * o / o.sum()
        rows[m] = (labels, p / p.sum())
    return rows


def simulate(recs, em_ai, em_de, drop_p, draws, rng, base_dep, base_enr):
    ai_i = {a: i for i, a in enumerate(L.AI_FAMS)}; de_i = {d: j for j, d in enumerate(L.DEC_FAMS)}
    keep_dep = Counter(); keep_enr = Counter(); new_dep = []; new_enr = []; n_dep = []; n_enr = []; sizes = []; oe_dep = []; dir_dep = []
    for _ in range(draws):
        out = []
        for doc, a, d in recs:
            if rng.random() < drop_p:
                continue
            la, pa = em_ai[a]; ld, pd = em_de[d]
            ta = la[rng.choice(len(la), p=pa)]; td = ld[rng.choice(len(ld), p=pd)]
            if ta == "NONE" or td == "NONE":
                continue
            out.append((doc, ta, td))
        edges = L.dedup(out)
        m = L.matrix(edges, L.AI_FAMS, L.DEC_FAMS)
        exp, p = L.exact_hyper(m)
        q = L.bh(p.ravel()).reshape(m.shape)
        dep = {(a, d) for a in L.AI_FAMS for d in L.DEC_FAMS if q[ai_i[a], de_i[d]] <= .05 and m[ai_i[a], de_i[d]] < exp[ai_i[a], de_i[d]]}
        enr = {(a, d) for a in L.AI_FAMS for d in L.DEC_FAMS if q[ai_i[a], de_i[d]] <= .05 and m[ai_i[a], de_i[d]] > exp[ai_i[a], de_i[d]]}
        for c in dep & base_dep: keep_dep[c] += 1
        for c in enr & base_enr: keep_enr[c] += 1
        n_dep.append(len(dep & base_dep)); n_enr.append(len(enr & base_enr))
        dir_dep.append(sum(m[ai_i[a], de_i[d]] < exp[ai_i[a], de_i[d]] for a, d in base_dep))
        new_dep.append(len(dep - base_dep)); new_enr.append(len(enr - base_enr)); sizes.append(len(edges))
        with np.errstate(divide="ignore", invalid="ignore"):
            oe_dep.append(float(np.mean([m[ai_i[a], de_i[d]] / exp[ai_i[a], de_i[d]] for a, d in base_dep])))
    pct = lambda v: [int(np.percentile(v, 5)), int(np.median(v)), int(np.percentile(v, 95))]
    return {"draws": draws, "edges_p5_median_p95": pct(sizes),
            "depleted_core_retained_p5_median_p95": pct(n_dep), "enriched_core_retained_p5_median_p95": pct(n_enr),
            "P_at_least_12_of_16_depleted_retained": round(float(np.mean(np.array(n_dep) >= 12)), 3),
            "depleted_core_same_direction_p5_median_p95": pct(dir_dep),
            "new_depleted_cells_median": float(np.median(new_dep)), "new_enriched_cells_median": float(np.median(new_enr)),
            "mean_oe_of_16_depleted_cells_median": round(float(np.median(oe_dep)), 3),
            "per_cell_depleted_retention": {f"{a} x {d}": round(keep_dep[(a, d)] / draws, 3) for a, d in sorted(base_dep)},
            "per_cell_enriched_retention": {f"{a} x {d}": round(keep_enr[(a, d)] / draws, 3) for a, d in sorted(base_enr)}}


def main():
    rng = np.random.default_rng(20261207)
    rc = L.read_csv(os.path.join(L.INP, "ROBUSTNESS_COMPARISON_120.csv"))
    base_dep = {(r["ai_family"], r["decision_family"]) for r in rc if r["full_sensitivity_robust"] == "True" and r["main_mc_direction"] == "DEPLETED"}
    base_enr = {(r["ai_family"], r["decision_family"]) for r in rc if r["full_sensitivity_robust"] == "True" and r["main_mc_direction"] == "ENRICHED"}
    recs = L.load_official_raw_pairs()
    first = L.read_csv(os.path.join(L.INP, "FIRST_CODER_50_FINAL_FROZEN.csv"))
    recon = {r["record_id"]: r for r in L.read_csv(os.path.join(L.INP, "HUMAN_RECONCILED_20.csv"))}
    mai = lambda r: r["source_model_family_canonical_AI"]; mde = lambda r: r["source_model_family_canonical_DECISION"]
    excl1 = sum(r["human_include"] == "EXCLUDE" for r in first) / len(first)
    e1_ai, d1a = error_model([(mai(r), r["human_ai_family"]) for r in first], L.AI_FAMS)
    e1_de, d1d = error_model([(mde(r), r["human_decision_family"]) for r in first], L.DEC_FAMS)
    rr = [r for r in first if r["record_id"] in recon]
    excl2 = sum(recon[r["record_id"]]["FINAL_C5"] == "EXCLUDE" for r in rr) / len(rr)
    e2_ai, d2a = error_model([(mai(r), recon[r["record_id"]]["FINAL_C3"]) for r in rr], L.AI_FAMS)
    e2_de, d2d = error_model([(mde(r), recon[r["record_id"]]["FINAL_C4"]) for r in rr], L.DEC_FAMS)
    marg_ai = Counter(a for _, a, _ in recs); marg_de = Counter(d for _, _, d in recs)
    rep = {"baseline": {"depleted_core": len(base_dep), "enriched_core": len(base_enr), "records": len(recs)},
           "error_models": {"E1_first_coder": {"ai": d1a, "decision": d1d, "record_exclude_rate": round(excl1, 3)},
                            "E2_reconciled": {"ai": d2a, "decision": d2d, "record_exclude_rate": round(excl2, 3)}},
           "scenarios": {}}
    # Analytic bound. Under non-differential misclassification to the marginal (side error rates e_a, e_d):
    #   O_obs/E - 1 = (1-e_a)(1-e_d) * (T/E - 1),  and T/E >= 0  =>  (1-e_a)(1-e_d) >= 1 - O_obs/E.
    # Use the upper 95% Poisson bound of O_obs so sampling noise cannot tighten the bound spuriously.
    from scipy.stats import chi2
    m0 = L.matrix(L.load_official_edges(), L.AI_FAMS, L.DEC_FAMS)
    e0, _ = L.exact_hyper(m0)
    ai_i = {a: i for i, a in enumerate(L.AI_FAMS)}; de_i = {d: j for j, d in enumerate(L.DEC_FAMS)}
    bound_rows = []
    for a, d in sorted(base_dep):
        o, e = int(m0[ai_i[a], de_i[d]]), float(e0[ai_i[a], de_i[d]])
        o_hi = chi2.ppf(0.975, 2 * (o + 1)) / 2
        need = max(0.0, 1 - o_hi / e)
        bound_rows.append({"cell": f"{a} x {d}", "observed": o, "expected": round(e, 2), "oe": round(o / e, 3),
                           "oe_upper95": round(o_hi / e, 3), "min_accuracy_product_required": round(need, 3),
                           "max_symmetric_error_rate": round(1 - np.sqrt(need), 3) if need > 0 else 1.0})
    bound_rows.sort(key=lambda r: -r["min_accuracy_product_required"])
    L.write_csv(os.path.join(OUTD, "ANALYTIC_ERROR_BOUND_16_DEPLETED.csv"), bound_rows)
    acc_ai1 = d1a["pooled_keep"]; acc_de1 = d1d["pooled_keep"]
    acc_ai2 = d2a["pooled_keep"]; acc_de2 = d2d["pooled_keep"]
    rep_bound = {"most_restrictive_cell": bound_rows[0],
                 "required_accuracy_product": bound_rows[0]["min_accuracy_product_required"],
                 "implied_by_first_coder_audit": round(acc_ai1 * acc_de1, 3),
                 "implied_by_reconciled_audit": round(acc_ai2 * acc_de2, 3),
                 "cells_requiring_product_gt_0.5": sum(r["min_accuracy_product_required"] > 0.5 for r in bound_rows),
                 "logic": "If the audit-implied accuracy product is below the required product, the observed depletion cannot be "
                          "produced from any true matrix under non-differential error: either the audit labels are not a valid "
                          "truth, or errors are differential (structured)."}
    rep["analytic_bound"] = rep_bound
    rep_bound["cells_requiring_product_gt_0.5"] = int(rep_bound["cells_requiring_product_gt_0.5"])
    print(json.dumps(rep_bound, indent=1, default=float), flush=True)
    sc = {"E1_first_coder_as_truth": (e1_ai, e1_de, excl1), "E2_reconciled_as_truth": (e2_ai, e2_de, excl2)}
    for err in (0.2, 0.4, 0.6):
        sc[f"E3_random_err{int(err * 100)}_drop20"] = (random_model(L.AI_FAMS, marg_ai, err), random_model(L.DEC_FAMS, marg_de, err), 0.2)
    for name, (ea, ed, dp) in sc.items():
        res = simulate(recs, ea, ed, dp, N_DRAWS, rng, base_dep, base_enr)
        rep["scenarios"][name] = res
        print(name, {k: v for k, v in res.items() if not k.startswith("per_cell")}, flush=True)
    rows = []
    for name, res in rep["scenarios"].items():
        for cell, v in res["per_cell_depleted_retention"].items():
            rows.append({"scenario": name, "direction": "DEPLETED", "cell": cell, "retention": v})
        for cell, v in res["per_cell_enriched_retention"].items():
            rows.append({"scenario": name, "direction": "ENRICHED", "cell": cell, "retention": v})
    L.write_csv(os.path.join(OUTD, "PER_CELL_RETENTION.csv"), rows)
    L.write_json(os.path.join(OUTD, "MISCLASSIFICATION_REPORT.json"), rep)


if __name__ == "__main__":
    main()
