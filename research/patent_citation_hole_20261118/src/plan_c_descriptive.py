"""Plan C (exploratory, descriptive): where does AI-decision integration occur?

Usage:
    python src/plan_c_descriptive.py --out outputs
Needs outputs/firm_model_LOCAL.pkl (src/firm_null.py), SUITE_P1_B_CELLS.csv, PATENT_HOLE_RESULTS.json,
PLAN5_CONSTRUCT_RESULTS.json. Writes outputs/PLAN_C_RESULTS.json. See PLAN_C_DESCRIPTIVE.md.
"""
import argparse
import csv
import json
import math
import pickle
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import firm_null  # noqa: E402

import __main__  # noqa: E402
__main__.FirmModel = firm_null.FirmModel          # the slim model was pickled from a script run

AI, DEC, BRIDGE = 0, 1, 2
CATS = ("within_firm", "between_mixed_citing", "between_specialist_citing", "unowned_end")


def wilson(k, n, z=1.96):
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [max(0.0, round((c - h) / d, 4)), min(1.0, round((c + h) / d, 4))]


def share(k, n):
    return {"count": int(k), "n": int(n), "share": round(k / n, 4) if n else None, "wilson95": wilson(k, n)}


def owners_of(M, k):
    return M.owner[M.indptr[k]:M.indptr[k + 1]]


def classify(M, a, b):
    oa, ob = owners_of(M, a), owners_of(M, b)
    if len(oa) == 0 or len(ob) == 0:
        return "unowned_end"
    if np.intersect1d(oa, ob).size:
        return "within_firm"
    if (M.group[oa] == "MIXED").any():
        return "between_mixed_citing"
    return "between_specialist_citing"


def locus(M, idx):
    c = Counter(classify(M, int(M.ca[t]), int(M.cb[t])) for t in idx)
    n = len(idx)
    return {k: share(c[k], n) for k in CATS}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("outputs"))
    a = ap.parse_args(argv)
    with open(a.out / "firm_model_LOCAL.pkl", "rb") as f:
        M = pickle.load(f)
    pt, yr = M.ptype, M.year
    res = {"plan": "PLAN_C_DESCRIPTIVE.md", "n_patents": int(len(M.S)), "n_citations": int(len(M.ca)),
           "n_firms": int(len(M.firms))}

    # C1 artefact-level integration (co-classification; not flow)
    years = list(range(2010, 2026))
    res["C1_bridge_by_year"] = {y: share(int(((yr == y) & (pt == BRIDGE)).sum()), int((yr == y).sum())) for y in years}
    res["C1_bridge_total"] = share(int((pt == BRIDGE).sum()), len(pt))
    res["C1_type_counts"] = {"AI_only": int((pt == AI).sum()), "DEC_only": int((pt == DEC).sum()),
                             "BRIDGE": int((pt == BRIDGE).sum())}

    # C2 locus of cross-domain flow
    pa, pb = pt[M.ca], pt[M.cb]
    cross = ((pa == AI) & (pb == DEC)) | ((pa == DEC) & (pb == AI))
    bridge = (pa == BRIDGE) | (pb == BRIDGE)
    allidx = np.arange(len(M.ca))
    cyear = yr[M.ca]
    res["C2_cross_share_of_all"] = share(int(cross.sum()), len(cross))
    res["C2_bridge_share_of_all"] = share(int(bridge.sum()), len(bridge))
    res["C2_cross_direction"] = {"AI_cites_DEC": int(((pa == AI) & (pb == DEC)).sum()),
                                 "DEC_cites_AI": int(((pa == DEC) & (pb == AI)).sum())}
    res["C2_locus_cross"] = locus(M, allidx[cross])
    res["C2_locus_all"] = locus(M, allidx)
    res["C2_locus_bridge"] = locus(M, allidx[bridge])
    per = {"2013-2018": (cyear >= 2013) & (cyear <= 2018), "2019-2025": (cyear >= 2019) & (cyear <= 2025)}
    res["C2_citing_year_before_2013"] = int((cyear < 2013).sum())
    res["C2_by_period"] = {p: {"cross_share_of_all": share(int((cross & m).sum()), int(m.sum())),
                               "bridge_share_of_all": share(int((bridge & m).sum()), int(m.sum())),
                               "locus_cross": locus(M, allidx[cross & m])} for p, m in per.items()}
    res["C1_bridge_by_period"] = {p: share(int(((yr >= lo) & (yr <= hi) & (pt == BRIDGE)).sum()),
                                           int(((yr >= lo) & (yr <= hi)).sum()))
                                  for p, (lo, hi) in {"2013-2018": (2013, 2018), "2019-2025": (2019, 2025)}.items()}

    # C3 who carries between-firm cross citations (credit to each citing owner)
    credit = Counter()
    for t in allidx[cross]:
        a_, b_ = int(M.ca[t]), int(M.cb[t])
        if classify(M, a_, b_).startswith("between"):
            for f in owners_of(M, a_):
                credit[int(f)] += 1
    tot = sum(credit.values())
    vals = sorted(credit.values(), reverse=True)
    k1 = max(1, math.ceil(0.01 * len(vals)))
    gcredit = Counter()
    for f, v in credit.items():
        gcredit[str(M.group[f])] += v
    pairs = Counter(str(M.group[f]) for f in M.owner)
    npairs = sum(pairs.values())
    res["C3"] = {"credit_total": tot, "firms_with_credit": len(vals),
                 "top10_share": round(sum(vals[:10]) / tot, 4) if tot else None,
                 "top1pct_firms": k1, "top1pct_share": round(sum(vals[:k1]) / tot, 4) if tot else None,
                 "credit_share_by_group": {g: round(gcredit[g] / tot, 4) for g in firm_null.GROUPS} if tot else None,
                 "patent_owner_pair_share_by_group": {g: round(pairs[g] / npairs, 4) for g in firm_null.GROUPS},
                 "patents_without_owner": share(int((np.diff(M.indptr) == 0).sum()), len(M.S)),
                 "firms_by_group": {g: int((M.group == g).sum()) for g in firm_null.GROUPS}}

    # C4 technology locus (summary of Plan 3 cells)
    with open(a.out / "SUITE_P1_B_CELLS.csv", encoding="utf-8-sig") as f:
        rows = [r for r in csv.DictReader(f) if float(r["expected_independence"]) >= 100]
    rows.sort(key=lambda r: float(r["oe_ratio"]))
    pick = lambda r: {k: r[k] for k in ("ai_family", "decision_family", "observed", "expected_independence", "oe_ratio", "three_test")}
    res["C4_cells_expected_ge_100"] = len(rows)
    res["C4_lowest3"] = [pick(r) for r in rows[:3]]
    res["C4_highest3"] = [pick(r) for r in rows[-3:][::-1]]

    with open(a.out / "FULL_SUITE_RESULTS.json", encoding="utf-8") as f:
        res["C4_note"] = "cells from SUITE_P1_B_CELLS.csv (Plan 3 P1, applicant citations, Part B)"
    json.dump(res, open(a.out / "PLAN_C_RESULTS.json", "w", encoding="utf-8"), indent=1, default=str)
    print(json.dumps({k: res[k] for k in ("n_patents", "n_citations", "C1_bridge_total", "C2_cross_share_of_all",
                                          "C2_locus_cross", "C2_locus_all", "C3")}, indent=1, default=str))


if __name__ == "__main__":
    main()
