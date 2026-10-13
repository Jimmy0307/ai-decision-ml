"""Correctness test for v1_construct_analyzer_v182.py (no files written; random vectors in memory only).

1. kappa: analyzer (unchanged 53B function) vs sklearn.metrics.cohen_kappa_score
2. alpha (nominal, 2-4 coders): analyzer vs krippendorff.alpha
3. declared classification rule (boundary numbers only)
4. OA-3 validation rule: NONE with Q1 != YES, and NONE with empty Q5, are rejected (single in-memory row)
Prints only PASS/FAIL and max abs differences.

Run: .venv_docx/Scripts/python.exe -E -P test_v1_construct_analyzer_v182.py --repo REPO
"""
from __future__ import annotations

import argparse
import os
import random
import sys

import numpy as np
import krippendorff
from sklearn.metrics import cohen_kappa_score

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v1_construct_analyzer_v182 as A  # noqa: E402

TOL = 1e-9


def stats_test(rel):
    rng = random.Random(1829374650)
    cats_all = sorted(A.Q2)
    dk = da = 0.0
    nk = na = 0
    for _ in range(300):
        n, k = rng.choice([8, 16, 30]), rng.choice([2, 3, 4])
        cats = cats_all[:rng.randint(2, len(cats_all))]
        data = [[rng.choice(cats) for _ in range(k)] for _ in range(n)]
        x, y = [u[0] for u in data], [u[1] for u in data]
        mk, _, _ = rel.cohen_kappa(x, y)
        rk = cohen_kappa_score(x, y)
        if mk == mk and rk == rk:
            dk, nk = max(dk, abs(mk - rk)), nk + 1
        if len({v for u in data for v in u}) > 1:
            enc = {c: j for j, c in enumerate(cats)}
            arr = np.array([[enc[v] for v in u] for u in data], dtype=float).T
            da = max(da, abs(rel.kripp_alpha_nominal(data)
                             - krippendorff.alpha(reliability_data=arr, level_of_measurement="nominal")))
            na += 1
    return dk, nk, da, na


def rule_test():
    c = A.classify_primary
    ok = (c(0.800, 0.667)["label"] == "RELIABLE" and not c(0.800, 0.667)["imprecise"]
          and c(0.7999, 0.70)["label"] == "TENTATIVE" and c(0.667, 0.667)["label"] == "TENTATIVE"
          and c(0.6669, 0.70)["label"] == "UNRESOLVED/NOT_ACCEPTABLE" and c(0.90, 0.6669)["imprecise"]
          and c(float("nan"), float("nan"))["label"] == "UNRESOLVED")
    return ok


def oa3_test():
    def one(q1, q2, q5):
        row = {A.RESP[0]: q1, A.RESP[1]: q2, A.RESP[2]: "LOW", A.RESP[3]: "", A.RESP[4]: q5}
        return A.validate(dict(sheet="T", rows={"ITEM-A01": row}, attestation=[]))
    e1 = one("UNCERTAIN", "NONE", "x")
    e2 = one("YES", "NONE", "")
    e3 = one("YES", "NONE", "x")
    return (any("NONE requires Q1=YES" in e for e in e1) and any("NONE requires Q5" in e for e in e2)
            and not any("NONE" in e for e in e3))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=None)
    a = ap.parse_args()
    rel = A.load_rel(a.repo or A.default_repo())
    dk, nk, da, na = stats_test(rel)
    r_ok, o_ok = rule_test(), oa3_test()
    ok = dk <= TOL and da <= TOL and nk > 0 and na > 0 and r_ok and o_ok
    print(f"{'PASS' if ok else 'FAIL'} kappa_vs_sklearn_max_abs_diff={dk:.3e} (n={nk}) "
          f"alpha_vs_krippendorff_max_abs_diff={da:.3e} (n={na}) classification_rule={'PASS' if r_ok else 'FAIL'} "
          f"oa3_none_validation={'PASS' if o_ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
