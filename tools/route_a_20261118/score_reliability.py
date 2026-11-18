"""Score the two-coder reliability study and apply the PRE-REGISTERED gate.

    python score_reliability.py CODING_SHEET_CODER_A.csv CODING_SHEET_CODER_B.csv KEY.csv OUTDIR

Gate (see docs/PREREGISTRATION_ROUTE_A.md):
  For C3 (AI family) and C4 (Decision family), Krippendorff's alpha (nominal) on all 200 items,
  with NONE / AMBIGUOUS treated as categories, item-level bootstrap 95% CI (5,000 resamples, seed fixed).
  GO_FIRM      : point alpha >= .80 and lower 95% bound >= .667 for BOTH C3 and C4
  GO_TENTATIVE : lower 95% bound >= .667 for BOTH (point < .80 for at least one)
  NO_GO        : otherwise -> do not re-run the matrix analysis; revise the coding unit/codebook or pivot.
The same statistics are reported for taxonomy T1 (secondary; it cannot rescue a NO_GO on T0 unless the
pre-registered decision rule in the protocol selects T1 a priori).
"""
import os, sys, json
from collections import Counter
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ra_lib as L
from step_common import alpha_nominal, kappa
from step1_taxonomy import T1_AI, T1_DE

FIELDS = {"C1_evidence_valid": None, "C2_relation_type": None, "C3_ai_family": T1_AI, "C4_decision_family": T1_DE}
NORMAL = {"": "MISSING", "UNMAPPED": "NONE", "NOT_PRESENT": "NONE", "N/A": "NONE"}


def norm(v):
    v = (v or "").strip().upper()
    return NORMAL.get(v, v)


def boot_alpha(pairs, B=5000, seed=20261118):
    rng = np.random.default_rng(seed)
    n = len(pairs)
    vals = []
    for _ in range(B):
        idx = rng.integers(0, n, n)
        vals.append(alpha_nominal([pairs[i] for i in idx]))
    vals = np.array([v for v in vals if v == v])
    if len(vals) < B * 0.5:  # alpha undefined (no variation) in most resamples
        return float("nan"), float("nan")
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def score(a_rows, b_rows, key_rows):
    a = {r["item_id"]: r for r in a_rows}; b = {r["item_id"]: r for r in b_rows}
    key = {r["item_id"]: r for r in key_rows}
    items = sorted(set(a) & set(b) & set(key))
    incomplete = [i for i in items if any(norm(a[i][f]) == "MISSING" or norm(b[i][f]) == "MISSING" for f in ("C3_ai_family", "C4_decision_family"))]
    same_coder = sorted({a[i]["coder_id"] for i in items} & {b[i]["coder_id"] for i in items} - {""})
    out = {"items_scored": len(items), "incomplete_family_items": len(incomplete), "coder_id_overlap": same_coder, "fields": {}}
    for f, t1 in FIELDS.items():
        pairs = [(norm(a[i][f]), norm(b[i][f])) for i in items if i not in incomplete]
        res = {"n": len(pairs), "exact": sum(x == y for x, y in pairs),
               "alpha": round(alpha_nominal(pairs), 4), "kappa": round(kappa([x for x, _ in pairs], [y for _, y in pairs]), 4)}
        res["alpha_ci95"] = [round(v, 4) for v in boot_alpha(pairs)]
        if t1:
            p1 = [(t1.get(x, x), t1.get(y, y)) for x, y in pairs]
            res["T1_alpha"] = round(alpha_nominal(p1), 4)
            res["T1_alpha_ci95"] = [round(v, 4) for v in boot_alpha(p1)]
            mk = "model_ai_family" if f.startswith("C3") else "model_decision_family"
            agree = [norm(key[i][mk]) == x for i, (x, y) in zip([i for i in items if i not in incomplete], pairs) if x == y]
            res["model_matches_human_consensus_when_coders_agree"] = {"n": len(agree), "matches": int(sum(agree))}
            res["confusions_top"] = Counter(tuple(sorted(p)) for p in pairs if p[0] != p[1]).most_common(8)
        out["fields"][f] = res
    c3, c4 = out["fields"]["C3_ai_family"], out["fields"]["C4_decision_family"]
    lo_ok = c3["alpha_ci95"][0] >= .667 and c4["alpha_ci95"][0] >= .667
    firm = lo_ok and c3["alpha"] >= .80 and c4["alpha"] >= .80
    out["gate"] = "GO_FIRM" if firm else "GO_TENTATIVE" if lo_ok else "NO_GO"
    if same_coder:
        out["gate"] = "INVALID_SAME_CODER"
    if len(items) < 200 or incomplete:
        out["gate_note"] = f"Pre-registered n=200 complete pairs; got {len(items) - len(incomplete)}. Gate is provisional until complete."
    return out


def main():
    a, b, k, outd = sys.argv[1:5]
    res = score(L.read_csv(a), L.read_csv(b), L.read_csv(k))
    L.write_json(os.path.join(outd, "RELIABILITY_RESULT.json"), res)
    print(json.dumps(res, indent=1, default=str))


if __name__ == "__main__":
    main()
