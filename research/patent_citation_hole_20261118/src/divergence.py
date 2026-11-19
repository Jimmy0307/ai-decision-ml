"""Plan 8 (PREREGISTRATION_DIVERGENCE.md): does the gap between flow and co-occurrence grow with taxonomic distance?

Usage:
    python src/divergence.py --pairs PLAN7_PAIRS_primary.csv --plan7 PLAN7_RESULTS.json --out PLAN8_RESULTS.json
"""
import argparse
import csv
import json
import re

import numpy as np
from scipy.stats import rankdata

SEED, B = 20261119, 1000


def parts(sym):
    m = re.match(r"^([A-H]\d\d)([A-Z])(\d+)$", sym)
    return m.group(1), m.group(1) + m.group(2)


def level(a, b):
    ca, sa = parts(a)
    cb, sb = parts(b)
    return 1 if sa == sb else 2 if ca == cb else 3


def wls(y, X, w):
    sw = np.sqrt(w)
    beta, *_ = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)
    return beta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", required=True)
    ap.add_argument("--plan7", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    p7 = json.load(open(a.plan7, encoding="utf-8"))["specs"]["primary"]
    tc, tf = p7["threshold_co"], p7["threshold_flow"]
    rows = [r for r in csv.DictReader(open(a.pairs, encoding="utf-8")) if r["eligible"] == "True"]
    fa = [r["field_a"] for r in rows]
    fb = [r["field_b"] for r in rows]
    fields = sorted(set(fa) | set(fb))
    fi = {f: k for k, f in enumerate(fields)}
    ia, ib = np.array([fi[x] for x in fa]), np.array([fi[x] for x in fb])
    num = lambda k: np.array([float(r[k]) for r in rows])
    oc, of, na, nb, nab, ef = num("OE_co"), num("OE_flow"), num("n_a"), num("n_b"), num("n_ab"), num("E_flow")
    lev = np.array([level(x, y) for x, y in zip(fa, fb)])
    n = len(rows)
    delta = rankdata(of) / n - rankdata(oc) / n
    ctrl = np.c_[np.log(na * nb), np.abs(np.log(na) - np.log(nb)), np.log(ef)]
    X = np.c_[np.ones(n), lev == 2, lev == 3, ctrl].astype(float)
    X0 = np.c_[np.ones(n), lev == 2, lev == 3].astype(float)
    cg, fg, over = oc <= tc, of <= tf, of >= 1
    pos = (nab > 0) & (of > 0)
    dlog = np.log(np.where(pos, of, 1)) - np.log(np.where(pos, oc, 1))

    def stats(w):
        out = {}
        b = wls(delta, X, w)
        out["b_level2"], out["b_level3"] = float(b[1]), float(b[2])
        b0 = wls(delta, X0, w)
        out["S2_b_level2"], out["S2_b_level3"] = float(b0[1]), float(b0[2])
        wp = w * pos
        b1 = wls(dlog, X, wp)
        out["S1_b_level2"], out["S1_b_level3"] = float(b1[1]), float(b1[2])
        for L in (1, 2, 3):
            m = lev == L
            out[f"mean_delta_L{L}"] = float((w * delta)[m].sum() / w[m].sum())
        g3, g12 = cg & (lev == 3), cg & (lev < 3)
        rate = lambda sel, ev: float((w * (sel & ev)).sum() / (w * sel).sum())
        out["false_gap_L3"], out["false_gap_L12"] = rate(g3, ~fg), rate(g12, ~fg)
        out["reversal_L3"], out["reversal_L12"] = rate(g3, over), rate(g12, over)
        out["false_gap_diff"] = out["false_gap_L3"] - out["false_gap_L12"]
        out["reversal_diff"] = out["reversal_L3"] - out["reversal_L12"]
        return out

    obs = stats(np.ones(n))
    rng = np.random.default_rng(SEED)
    G = len(fields)
    boot = []
    for _ in range(B):
        c = np.bincount(rng.integers(0, G, G), minlength=G)
        w = (c[ia] * c[ib]).astype(float)
        boot.append(stats(w))
    ci = {k: [float(np.percentile([x[k] for x in boot], 2.5)), float(np.percentile([x[k] for x in boot], 97.5))] for k in obs}
    order = obs["mean_delta_L1"] < obs["mean_delta_L2"] < obs["mean_delta_L3"]
    lo3, hi3 = ci["b_level3"]
    h8a = ("SUPPORTED" if lo3 > 0 and order else "REVERSED" if hi3 < 0 else "NOT_SUPPORTED")
    h8b = "SUPPORTED" if ci["false_gap_diff"][0] > 0 else "NOT_SUPPORTED"
    g16 = np.array([x.startswith("G16") or y.startswith("G16") for x, y in zip(fa, fb)])
    aidec = np.array([(x.startswith("G06N") and y.startswith("G06Q10")) or (y.startswith("G06N") and x.startswith("G06Q10"))
                      for x, y in zip(fa, fb)])
    rev = cg & over
    res = {"preregistration": "PREREGISTRATION_DIVERGENCE.md", "eligible_pairs": n, "fields": G,
           "pairs_by_level": {f"L{L}": int((lev == L).sum()) for L in (1, 2, 3)},
           "c_gaps_by_level": {f"L{L}": int((cg & (lev == L)).sum()) for L in (1, 2, 3)},
           "observed": obs, "ci95": ci, "mean_delta_ordered_L1_L2_L3": bool(order),
           "H8a": h8a, "H8b": h8b,
           "S1_pairs": int(pos.sum()),
           "S3": {"mean_delta_G16_pairs": float(delta[g16].mean()), "n_G16_pairs": int(g16.sum()),
                  "mean_delta_AIxDEC_pairs": float(delta[aidec].mean()) if aidec.any() else None,
                  "n_AIxDEC_pairs": int(aidec.sum()),
                  "c_gap_reversals": int(rev.sum()), "share_reversals_L3": float((rev & (lev == 3)).sum() / rev.sum())}}
    json.dump(res, open(a.out, "w", encoding="utf-8"), indent=1)
    print(json.dumps({k: res[k] for k in ("pairs_by_level", "c_gaps_by_level", "H8a", "H8b", "mean_delta_ordered_L1_L2_L3")}))
    print(json.dumps(obs, indent=0))
    print(json.dumps({k: [round(v, 4) for v in ci[k]] for k in ("b_level2", "b_level3", "false_gap_diff", "reversal_diff", "S1_b_level3", "S2_b_level3")}))
    print(json.dumps(res["S3"]))


if __name__ == "__main__":
    main()
