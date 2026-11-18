"""Step 3: validate the independent re-implementation against the frozen official V9 outputs."""
import os, sys, json
import numpy as np
import ra_lib as L

OUTD = os.path.join(L.OUT, "03_pipeline_validation")


def official():
    key = lambda r: (r["ai_family"], r["decision_family"])
    main = {key(r): r for r in L.read_csv(os.path.join(L.INP, "CELL_NULL_MODEL_RESULTS_120.csv"))}
    ex = {key(r): r for r in L.read_csv(os.path.join(L.INP, "EXACT_HYPERGEOMETRIC_RESULTS_120.csv"))}
    doc = {key(r): r for r in L.read_csv(os.path.join(L.INP, "DOCUMENT_PRESERVING_NULL_RESULTS_120.csv"))}
    raw = {key(r): r for r in L.read_csv(os.path.join(L.INP, "RAW_RECORD_EXACT_SENSITIVITY_120.csv"))}
    comp = {key(r): r for r in L.read_csv(os.path.join(L.INP, "ROBUSTNESS_COMPARISON_120.csv"))}
    return main, ex, doc, raw, comp


def jaccard(a, b):
    return len(a & b) / len(a | b) if a | b else 1.0


def main():
    edges = L.load_official_edges()
    raw = L.load_official_raw_pairs()
    assert len(edges) == 2180 and len(raw) == 3125
    assert L.dedup(raw) and len({(d, a, x) for d, a, x in raw}) == 2180, "dedup of raw records must give the 2,180 edges"
    rows, summ = L.analyze(edges, raw, L.AI_FAMS, L.DEC_FAMS)
    om, oe, od, orw, oc = official()
    T = lambda x: str(x).strip().lower() == "true"
    cmp_rows, maxdiff = [], {"exact": 0.0, "raw": 0.0}
    sets = {t: (set(), set()) for t in ["main", "exact", "doc", "raw", "structural", "full"]}
    dir_agree = {t: 0 for t in ["main", "exact", "doc", "raw"]}
    for r in rows:
        k = (r["ai_family"], r["decision_family"])
        off = {"main": (float(om[k]["q_bh_two_sided"]), om[k]["direction"]),
               "exact": (float(oe[k]["q_bh_two_sided"]), oe[k]["direction"]),
               "doc": (float(od[k]["q_bh_two_sided"]), od[k]["direction"]),
               "raw": (float(orw[k]["q_bh_two_sided"]), orw[k]["direction"])}
        assert int(om[k]["observed"]) == r["observed"] and int(orw[k]["observed"]) == r["raw_observed"]
        c = {"ai_family": k[0], "decision_family": k[1], "observed": r["observed"]}
        for t in off:
            c[f"official_{t}_q"], c[f"reimpl_{t}_q"] = off[t][0], r[f"{t}_q"]
            c[f"{t}_dir_match"] = off[t][1] == r[f"{t}_dir"]
            dir_agree[t] += c[f"{t}_dir_match"]
            if off[t][0] <= .05: sets[t][0].add(k)
            if r[f"{t}_q05"]: sets[t][1].add(k)
            if t in maxdiff:
                maxdiff[t] = max(maxdiff[t], abs(off[t][0] - r[f"{t}_q"]))
        if T(oc[k]["structurally_robust"]): sets["structural"][0].add(k)
        if T(oc[k]["full_sensitivity_robust"]): sets["full"][0].add(k)
        if r["structural_core"]: sets["structural"][1].add(k)
        if r["full_core"]: sets["full"][1].add(k)
        cmp_rows.append(c)
    report = {
        "reimplementation_summary": summ,
        "official_q05_counts": {t: len(v[0]) for t, v in sets.items()},
        "reimpl_q05_counts": {t: len(v[1]) for t, v in sets.items()},
        "set_identical": {t: v[0] == v[1] for t, v in sets.items()},
        "jaccard": {t: round(jaccard(*v), 4) for t, v in sets.items()},
        "only_official": {t: sorted(" x ".join(x) for x in v[0] - v[1]) for t, v in sets.items()},
        "only_reimpl": {t: sorted(" x ".join(x) for x in v[1] - v[0]) for t, v in sets.items()},
        "max_abs_q_diff_deterministic_tests": maxdiff,
        "direction_agreement_120": dir_agree,
        "official_doc_null_reference": {"attempts": 21843600, "accepted": 11604932, "acceptance_rate": 0.531274, "documents_touched": 328},
    }
    L.write_csv(os.path.join(OUTD, "CELL_COMPARISON_OFFICIAL_VS_REIMPL_120.csv"), cmp_rows)
    L.write_csv(os.path.join(OUTD, "REIMPL_RESULTS_120.csv"), rows)
    L.write_json(os.path.join(OUTD, "VALIDATION_REPORT.json"), report)
    print(json.dumps({k: report[k] for k in ["official_q05_counts", "reimpl_q05_counts", "set_identical", "jaccard", "max_abs_q_diff_deterministic_tests", "direction_agreement_120", "only_official", "only_reimpl"]}, indent=1))
    print(json.dumps(summ["doc_null_diagnostics"]))


if __name__ == "__main__":
    main()
