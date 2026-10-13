"""Correctness test of the kappa / alpha implementation used by v1_construct_analyzer.py.

Compares the analyzer's (unchanged 53B) functions with independent reference implementations
(sklearn.metrics.cohen_kappa_score; krippendorff.alpha, nominal) on random label vectors generated IN MEMORY
with a fixed seed. Nothing is written to disk; no fixture file, no workbook, no coder-like data is produced.
Prints only PASS/FAIL and the maximum absolute difference.

Run with the venv that has scikit-learn + krippendorff:
  .venv_docx/Scripts/python.exe -E -P test_v1_construct_analyzer.py [--repo REPO]
"""
from __future__ import annotations

import argparse
import os
import random
import sys

import numpy as np
import krippendorff
from sklearn.metrics import cohen_kappa_score

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v1_construct_analyzer as A  # noqa: E402

CATS = sorted(A.Q2)
TOL = 1e-9


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=None)
    a = ap.parse_args()
    rel = A.load_rel(a.repo or A.default_repo())
    rng = random.Random(987654321)
    dk = da = 0.0
    n_k = n_a = 0
    for _ in range(300):
        n = rng.choice([8, 16, 30])
        k = rng.choice([2, 3, 4])
        ncat = rng.randint(2, len(CATS))
        cats = CATS[:ncat]
        data = [[rng.choice(cats) for _ in range(k)] for _ in range(n)]
        x, y = [u[0] for u in data], [u[1] for u in data]
        mine, _, _ = rel.cohen_kappa(x, y)
        ref = cohen_kappa_score(x, y)
        if mine == mine and ref == ref:
            dk = max(dk, abs(mine - ref))
            n_k += 1
        enc = {c: i for i, c in enumerate(cats)}
        arr = np.array([[enc[v] for v in u] for u in data], dtype=float).T   # coders x units
        if len({v for u in data for v in u}) > 1:
            mine_a = rel.kripp_alpha_nominal(data)
            ref_a = krippendorff.alpha(reliability_data=arr, level_of_measurement="nominal")
            da = max(da, abs(mine_a - ref_a))
            n_a += 1
    # declared classification rule (protocol 19 section 10.3) on boundary numbers only
    cls_ok = (A.label_3(0.800, 0.667) == ("RELIABLE", "RELIABLE")
              and A.label_3(0.7999, 0.70) == ("TENTATIVE", "TENTATIVE")
              and A.label_3(0.667, 0.667) == ("TENTATIVE", "TENTATIVE")
              and A.label_3(0.90, 0.6669)[0] == "UNRESOLVED"
              and A.label_3(0.6669, 0.70)[0] == "UNRESOLVED"
              and A.label_3(float("nan"), float("nan"))[0] == "UNRESOLVED")
    ok = dk <= TOL and da <= TOL and cls_ok and n_k > 0 and n_a > 0
    print(f"{'PASS' if ok else 'FAIL'} kappa_max_abs_diff={dk:.3e} (n={n_k}) "
          f"alpha_max_abs_diff={da:.3e} (n={n_a}) classification_rule={'PASS' if cls_ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
