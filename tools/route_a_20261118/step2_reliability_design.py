"""Step 2: reliability study design — sample size by simulation, seeded stratified sample, blind coding sheets.

Sample size: two coders, nominal labels drawn from the observed family marginals (plus a NONE/AMBIGUOUS
category); coder accuracy tuned so the population alpha equals a target. For each n we simulate the
sampling distribution of Krippendorff's alpha and report the 95% interval half-width and the probability
that the lower 95% bootstrap-style bound clears the gate when the true alpha is at a given level.
"""
import os, json, random
from collections import Counter
import numpy as np
import ra_lib as L
from step_common import alpha_nominal

OUTD = os.path.join(L.OUT, "02_reliability_design")
SEED = 20261118
EXCLUDE_FILES = ["FIRST_CODER_50_FINAL_FROZEN.csv"]


def simulate(marg, accuracy, n, reps, rng):
    cats = np.arange(len(marg))
    out = []
    for _ in range(reps):
        truth = rng.choice(cats, size=n, p=marg)
        def code():
            ok = rng.random(n) < accuracy
            return np.where(ok, truth, rng.choice(cats, size=n, p=marg))
        a, b = code(), code()
        out.append(alpha_nominal(list(zip(a.tolist(), b.tolist()))))
    return np.array(out)


def calibrate(marg, target, rng):
    lo, hi = 0.0, 1.0
    for _ in range(18):
        mid = (lo + hi) / 2
        if np.mean(simulate(marg, mid, 2000, 3, rng)) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def power_table(marg, rng):
    rows = []
    for true_alpha in (0.60, 0.667, 0.75, 0.80, 0.85):
        acc = calibrate(marg, true_alpha, rng)
        for n in (100, 150, 200, 250, 300):
            s = simulate(marg, acc, n, 1000, rng)
            rows.append({"true_alpha": true_alpha, "n_items": n, "mean_alpha": round(float(s.mean()), 4),
                         "sd": round(float(s.std()), 4), "ci95_halfwidth": round(1.96 * float(s.std()), 4),
                         "P_estimate_ge_0.667": round(float((s >= 0.667).mean()), 3),
                         "P_estimate_ge_0.80": round(float((s >= 0.80).mean()), 3),
                         "P_lower95_ge_0.667": round(float(((s - 1.96 * s.std()) >= 0.667).mean()), 3)})
    return rows


def draw_sample(rng_py):
    rec = L.read_csv(os.path.join(L.INP, "ANALYTICAL_FREEZE_RECORD_LEVEL.csv"))
    excluded = set()
    for f in EXCLUDE_FILES:
        excluded |= {r["record_id"] for r in L.read_csv(os.path.join(L.INP, f))}
    pool = [r for r in rec if r["record_id"] not in excluded]
    plan = {"FULLY_MAPPED": 140, "PARTIALLY_MAPPED": 40, "FULLY_UNRESOLVED": 20}
    sample = []
    for stratum, n in plan.items():
        sub = [r for r in pool if r["mapping_completeness"] == stratum]
        if stratum == "FULLY_MAPPED":
            by = {}
            for r in sub:
                by.setdefault(r["left_final_family"], []).append(r)
            fams = sorted(by)
            floor = 8
            take = {f: min(floor, len(by[f])) for f in fams}
            rest = n - sum(take.values())
            tot = sum(len(by[f]) - take[f] for f in fams)
            alloc = {f: take[f] + int(round(rest * (len(by[f]) - take[f]) / tot)) for f in fams}
            diff = n - sum(alloc.values())
            for f in sorted(fams, key=lambda f: -len(by[f]))[:abs(diff)]:
                alloc[f] += 1 if diff > 0 else -1
            for f in fams:
                pick = rng_py.sample(by[f], alloc[f])
                sample += [(stratum, f, r) for r in pick]
        else:
            sample += [(stratum, "", r) for r in rng_py.sample(sub, n)]
    rng_py.shuffle(sample)
    return sample, len(pool), len(excluded)


def main():
    rng = np.random.default_rng(SEED)
    rng_py = random.Random(SEED)
    side = L.read_csv(os.path.join(L.INP, "ANALYTICAL_FREEZE_SIDE_LEVEL.csv"))
    rep = {}
    for s, fams in (("LEFT", L.AI_FAMS), ("RIGHT", L.DEC_FAMS)):
        c = Counter(r["final_family"] if r["final_family"] in fams else "NONE_OR_AMBIGUOUS" for r in side if r["side"] == s)
        marg = np.array([c[k] for k in sorted(c)], float); marg /= marg.sum()
        rows = power_table(marg, rng)
        L.write_csv(os.path.join(OUTD, f"SAMPLE_SIZE_SIMULATION_{'AI' if s == 'LEFT' else 'DECISION'}.csv"), rows)
        rep[f"marginals_{s}"] = {k: c[k] for k in sorted(c)}
        rep[f"key_rows_{s}"] = [r for r in rows if r["n_items"] in (150, 200, 250) and r["true_alpha"] in (0.667, 0.80)]
    sample, pool_n, excl_n = draw_sample(rng_py)
    key_rows, sheet = [], []
    for i, (stratum, fam, r) in enumerate(sample, 1):
        uid = f"RS-{i:03d}"
        key_rows.append({"item_id": uid, "record_id": r["record_id"], "document_id": r["document_id"], "stratum": stratum,
                         "stratum_ai_family": fam, "model_ai_family": r["left_final_family"] or "NONE",
                         "model_decision_family": r["right_final_family"] or "NONE", "model_relation_type": r["relation_type"],
                         "mapping_completeness": r["mapping_completeness"]})
        sheet.append({"item_id": uid, "evidence_text": r["evidence_text"], "C1_evidence_valid": "", "C2_relation_type": "",
                      "C3_ai_family": "", "C3_ai_quote": "", "C4_decision_family": "", "C4_decision_quote": "",
                      "confidence_LOW_MED_HIGH": "", "notes": "", "coder_id": "", "coded_at": ""})
    L.write_csv(os.path.join(OUTD, "RELIABILITY_SAMPLE_200_KEY_HIDDEN_FROM_CODERS.csv"), key_rows)
    for c in ("A", "B"):
        L.write_csv(os.path.join(OUTD, f"CODING_SHEET_CODER_{c}.csv"), sheet)
    rep["sample"] = {"seed": SEED, "pool_after_excluding_prior_audit": pool_n, "excluded_prior_audit_records": excl_n,
                     "n": len(key_rows), "by_stratum": dict(Counter(k["stratum"] for k in key_rows)),
                     "fully_mapped_by_ai_family": dict(Counter(k["stratum_ai_family"] for k in key_rows if k["stratum"] == "FULLY_MAPPED")),
                     "decision_families_covered": dict(Counter(k["model_decision_family"] for k in key_rows)),
                     "documents": len({k["document_id"] for k in key_rows})}
    L.write_json(os.path.join(OUTD, "RELIABILITY_DESIGN_REPORT.json"), rep)
    print(json.dumps(rep, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
