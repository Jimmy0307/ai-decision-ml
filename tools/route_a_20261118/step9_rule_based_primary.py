"""Step 9: deterministic (rule/lexicon-based) matrix as a parallel primary analysis.

Measurement: stage-1 keyword anchors (applied before any LLM step) on BOTH sides, over all 26,501
candidate records; records whose two sides are anchored by the identical term are removed (codebook R2).
Deterministic coding is perfectly reproducible; its validity is argued by convergence with the LLM matrix.
Full four-test pipeline (ra_lib.analyze). Compared with the frozen LLM-based core.
"""
import os, json
from collections import Counter
import ra_lib as L
from step4_exclusion_bias import NONFAM, terms

OUTD = os.path.join(L.OUT, "09_rule_based_primary")


def main():
    allr = L.read_csv(os.path.join(L.INP, "RECORDS_ALL_26501_from_private_snapshot.csv"))
    both = [r for r in allr if r["stage1_left_family"] not in NONFAM and r["stage1_right_family"] not in NONFAM]
    def same(r):
        lt, rt = terms(r["stage1_basis"])
        return bool(lt and rt and lt.lower() == rt.lower())
    kept = [r for r in both if not same(r)]
    raw = [(r["document_id"], r["stage1_left_family"], r["stage1_right_family"]) for r in kept]
    edges = L.dedup(raw)
    rows, summ = L.analyze(edges, raw, L.AI_FAMS, L.DEC_FAMS, seeds=(20261209, 20261210))
    rc = L.read_csv(os.path.join(L.INP, "ROBUSTNESS_COMPARISON_120.csv"))
    llm = {(r["ai_family"], r["decision_family"]): r["main_mc_direction"] for r in rc if r["full_sensitivity_robust"] == "True"}
    rule = {(r["ai_family"], r["decision_family"]): r["core_direction"] for r in rows if r["full_core"]}
    shared = {k: v for k, v in rule.items() if llm.get(k) == v}
    opposite = {k: (v, llm[k]) for k, v in rule.items() if k in llm and llm[k] != v}
    testable = {k for k in llm if [r for r in rows if (r["ai_family"], r["decision_family"]) == k][0]["expected_independence"] >= 5}
    rep = {"records_both_anchored": len(both), "same_term_removed": len(both) - len(kept), "records_used": len(kept),
           "document_edges": len(edges), "documents": len({d for d, _, _ in edges}), "summary": summ,
           "rule_core": len(rule), "rule_core_by_direction": dict(Counter(rule.values())),
           "llm_core": len(llm), "shared_same_direction": len(shared),
           "shared_by_direction": dict(Counter(shared.values())), "opposite_direction": {" x ".join(k): v for k, v in opposite.items()},
           "llm_core_cells_testable_in_rule_matrix_(E>=5)": len(testable),
           "llm_depleted_recovered": sorted(" x ".join(k) for k, v in shared.items() if v == "DEPLETED"),
           "llm_depleted_not_recovered": sorted(" x ".join(k) for k, v in llm.items() if v == "DEPLETED" and k not in shared),
           "rule_only_core": sorted(" x ".join(k) + f" ({v})" for k, v in rule.items() if k not in llm),
           "jaccard_core": round(len(set(rule) & set(llm)) / len(set(rule) | set(llm)), 3)}
    L.write_csv(os.path.join(OUTD, "RULE_BASED_RESULTS_120.csv"), rows)
    L.write_json(os.path.join(OUTD, "RULE_BASED_REPORT.json"), rep)
    print(json.dumps(rep, indent=1, default=str))


if __name__ == "__main__":
    main()
