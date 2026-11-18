"""Step 3b: Monte Carlo seed stability of the 32-cell core on the frozen official labels.

Runs the full four-test pipeline with K independent seed pairs and reports, per cell, how often it
is q<=.05 in each Monte Carlo test and how often it enters the full core.
"""
import os, sys, json
from collections import Counter
import numpy as np
import ra_lib as L

OUTD = os.path.join(L.OUT, "03_pipeline_validation")
K = int(sys.argv[1]) if len(sys.argv) > 1 else 20


def main():
    edges, raw = L.load_official_edges(), L.load_official_raw_pairs()
    off = {(r["ai_family"], r["decision_family"]): r for r in L.read_csv(os.path.join(L.INP, "ROBUSTNESS_COMPARISON_120.csv"))}
    freq = Counter(); main05 = Counter(); doc05 = Counter(); qs = {}
    sizes = []
    comp = []
    for s in range(K):
        seeds = (20261118 + 1000 * s, 20261119 + 1000 * s)
        rows, summ = L.analyze(edges, raw, L.AI_FAMS, L.DEC_FAMS, seeds=seeds)
        sizes.append(summ["full_core"])
        comp.append(summ["full_core_by_direction"])
        for r in rows:
            k = (r["ai_family"], r["decision_family"])
            freq[k] += r["full_core"]; main05[k] += r["main_q05"]; doc05[k] += r["doc_q05"]
            qs.setdefault(k, []).append(r["doc_q"])
        print(s, summ["full_core"], summ["full_core_by_direction"], flush=True)
    out = []
    for k in sorted(qs):
        o = off[k]
        out.append({"ai_family": k[0], "decision_family": k[1], "official_full_core": o["full_sensitivity_robust"],
                    "official_direction": o["main_mc_direction"], "core_frequency": freq[k] / K,
                    "main_q05_frequency": main05[k] / K, "doc_q05_frequency": doc05[k] / K,
                    "doc_q_min": round(min(qs[k]), 4), "doc_q_median": round(float(np.median(qs[k])), 4), "doc_q_max": round(max(qs[k]), 4)})
    unstable = [r for r in out if 0 < r["core_frequency"] < 1]
    always = [r for r in out if r["core_frequency"] == 1]
    report = {"seeds": K, "core_size_distribution": dict(Counter(sizes)),
              "core_composition_distribution": dict(Counter(json.dumps(c, sort_keys=True) for c in comp)),
              "cells_always_in_core": len(always),
              "always_in_core_by_direction": dict(Counter(r["official_direction"] for r in always)),
              "cells_sometimes_in_core": [(r["ai_family"] + " x " + r["decision_family"], r["core_frequency"], r["official_full_core"]) for r in unstable],
              "official_core_cells_not_always_in_core": [(r["ai_family"] + " x " + r["decision_family"], r["core_frequency"]) for r in out if r["official_full_core"] == "True" and r["core_frequency"] < 1]}
    L.write_csv(os.path.join(OUTD, "SEED_STABILITY_120.csv"), out)
    L.write_json(os.path.join(OUTD, "SEED_STABILITY_REPORT.json"), report)
    print(json.dumps(report, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
