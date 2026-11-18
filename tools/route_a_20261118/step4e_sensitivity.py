"""Step 4e: (1) stage-1 triangulation restricted to records NOT in the strict set (independent of final labels);
(2) matrix re-test after removing records whose two sides were anchored by the identical term."""
import os, json
from collections import Counter
import ra_lib as L
from step4_exclusion_bias import NONFAM, terms

OUTD = os.path.join(L.OUT, "04_exclusion_bias")


def core_sets():
    rc = L.read_csv(os.path.join(L.INP, "ROBUSTNESS_COMPARISON_120.csv"))
    dep = {(r["ai_family"], r["decision_family"]) for r in rc if r["full_sensitivity_robust"] == "True" and r["main_mc_direction"] == "DEPLETED"}
    enr = {(r["ai_family"], r["decision_family"]) for r in rc if r["full_sensitivity_robust"] == "True" and r["main_mc_direction"] == "ENRICHED"}
    return dep, enr


def tri(records, dep, enr):
    pairs = L.dedup([(r["document_id"], r["stage1_left_family"], r["stage1_right_family"]) for r in records])
    m = L.matrix(pairs, L.AI_FAMS, L.DEC_FAMS)
    exp, p = L.exact_hyper(m)
    q = L.bh(p.ravel()).reshape(m.shape)
    c = Counter()
    for i, a in enumerate(L.AI_FAMS):
        for j, d in enumerate(L.DEC_FAMS):
            for name, S, want in (("DEPLETED_CORE", dep, "DEP"), ("ENRICHED_CORE", enr, "ENR")):
                if (a, d) in S:
                    sd = "ENR" if m[i, j] > exp[i, j] else "DEP" if m[i, j] < exp[i, j] else "NEU"
                    c[f"{name}|same_direction"] += sd == want
                    c[f"{name}|same_direction_q05"] += sd == want and q[i, j] <= .05
                    c[f"{name}|opposite_direction_q05"] += sd not in (want, "NEU") and q[i, j] <= .05
    return {"records": len(records), "document_edges": int(m.sum()), **dict(sorted(c.items()))}


def main():
    dep, enr = core_sets()
    allr = L.read_csv(os.path.join(L.INP, "RECORDS_ALL_26501_from_private_snapshot.csv"))
    both = [r for r in allr if r["stage1_left_family"] not in NONFAM and r["stage1_right_family"] not in NONFAM]
    nonstrict = [r for r in both if r["passed_strict_filter"] not in ("1", "True", "true")]
    rep = {"triangulation_all_candidates": tri(both, dep, enr), "triangulation_non_strict_only": tri(nonstrict, dep, enr)}

    basis = {r["record_id"]: r["stage1_basis"] for r in allr}
    elig = L.read_csv(os.path.join(L.INP, "ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv"))
    def same(r):
        lt, rt = terms(basis.get(r["record_id"], ""))
        return bool(lt and rt and lt.lower() == rt.lower())
    kept = [r for r in elig if not same(r)]
    raw = [(r["document_id"], r["left_final_family"], r["right_final_family"]) for r in kept]
    edges = L.dedup(raw)
    rows, summ = L.analyze(edges, raw, L.AI_FAMS, L.DEC_FAMS)
    base = {(r["ai_family"], r["decision_family"]): r for r in L.read_csv(os.path.join(L.OUT, "03_pipeline_validation", "REIMPL_RESULTS_120.csv"))}
    newcore = {(r["ai_family"], r["decision_family"]): r["core_direction"] for r in rows if r["full_core"]}
    oldcore = {k: r["core_direction"] for k, r in base.items() if r["full_core"] == "True"}
    pp = ("PREDICTION_RISK_ESTIMATION", "PREDICTION_DIAGNOSIS")
    rp = [r for r in rows if (r["ai_family"], r["decision_family"]) == pp][0]
    rep["same_term_removed"] = {
        "records_removed": len(elig) - len(kept), "raw_records": len(raw), "document_edges": len(edges),
        "summary": summ, "core_vs_reimpl_baseline_same_seeds": {
            "gained": sorted(" x ".join(k) + f" ({v})" for k, v in newcore.items() if k not in oldcore),
            "lost": sorted(" x ".join(k) + f" ({v})" for k, v in oldcore.items() if k not in newcore)},
        "prediction_x_prediction": {k: rp[k] for k in ("observed", "oe_ratio", "main_q", "exact_q", "doc_q", "raw_q", "full_core", "core_direction")},
        "depleted_core_unchanged": {k for k, v in oldcore.items() if v == "DEPLETED"} == {k for k, v in newcore.items() if v == "DEPLETED"},
    }
    L.write_csv(os.path.join(OUTD, "E_SAME_TERM_REMOVED_RESULTS_120.csv"), rows)
    L.write_json(os.path.join(OUTD, "E_SENSITIVITY_REPORT.json"), rep)
    print(json.dumps(rep, indent=1, default=str))


if __name__ == "__main__":
    main()
