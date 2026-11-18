"""Step 5: is the functional (under-)integration pattern an artifact of the two-track retrieval design?

(1) Track-stratified configuration null: decision stubs are permuted only within the source track
    (AI-track documents vs DECISION-track documents), so track composition is held fixed.
(2) Per-track exact tests (AI track; DECISION track) and direction agreement with the frozen core.
The document-preserving null already conditions on documents (hence on track) and is not repeated.
"""
import os, json
from collections import Counter
import numpy as np
import ra_lib as L

OUTD = os.path.join(L.OUT, "05_track_sensitivity")


def stratified_mc(pairs, strata, ai, dec, R=10_000, seed=20261205):
    ai_i = {a: i for i, a in enumerate(ai)}; de_i = {d: j for j, d in enumerate(dec)}
    A = np.array([ai_i[a] for _, a, _ in pairs]); D = np.array([de_i[d] for _, _, d in pairs])
    S = np.array(strata)
    k = len(dec)
    obs = np.bincount(A * k + D, minlength=len(ai) * k)
    groups = [np.where(S == s)[0] for s in np.unique(S)]
    rng = np.random.default_rng(seed)
    ge = np.zeros_like(obs); le = np.zeros_like(obs); tot = np.zeros(obs.shape)
    Dp = D.copy()
    for _ in range(R):
        for g in groups:
            Dp[g] = D[g][rng.permutation(len(g))]
        c = np.bincount(A * k + Dp, minlength=len(ai) * k)
        ge += c >= obs; le += c <= obs; tot += c
    p = L.two_sided((1 + ge) / (R + 1), (1 + le) / (R + 1))
    return obs.reshape(len(ai), k), (tot / R).reshape(len(ai), k), L.bh(p).reshape(len(ai), k)


def main():
    docs = {r["document_id"]: r for r in L.read_csv(os.path.join(L.INP, "DOCS_2118_from_private_snapshot.csv"))}
    edges = L.load_official_edges()
    rc = {(r["ai_family"], r["decision_family"]): r for r in L.read_csv(os.path.join(L.INP, "ROBUSTNESS_COMPARISON_120.csv"))}
    core = {k: r["main_mc_direction"] for k, r in rc.items() if r["full_sensitivity_robust"] == "True"}
    track = [docs[d]["track"] for d, _, _ in edges]
    obs, mean, q_str = stratified_mc(edges, track, L.AI_FAMS, L.DEC_FAMS)
    per = {}
    for t in ("AI", "DECISION"):
        sub = [e for e, tr in zip(edges, track) if tr == t]
        m = L.matrix(sub, L.AI_FAMS, L.DEC_FAMS)
        exp, p = L.exact_hyper(m)
        per[t] = (m, exp, L.bh(p.ravel()).reshape(m.shape))
    rows, agg = [], Counter()
    for i, a in enumerate(L.AI_FAMS):
        for j, d in enumerate(L.DEC_FAMS):
            k = (a, d)
            sdir = "ENRICHED" if obs[i, j] > mean[i, j] else "DEPLETED" if obs[i, j] < mean[i, j] else "NEUTRAL"
            r = {"ai_family": a, "decision_family": d, "frozen_core_direction": core.get(k, ""), "observed": int(obs[i, j]),
                 "stratified_null_mean": round(float(mean[i, j]), 3), "stratified_q": float(q_str[i, j]), "stratified_dir": sdir,
                 "official_main_q": float(rc[k]["main_mc_q"])}
            for t, (m, exp, q) in per.items():
                r[f"{t}_track_observed"] = int(m[i, j]); r[f"{t}_track_expected"] = round(float(exp[i, j]), 3)
                r[f"{t}_track_oe"] = round(float(m[i, j] / exp[i, j]), 3) if exp[i, j] > 0 else ""
                r[f"{t}_track_q"] = float(q[i, j])
                r[f"{t}_track_dir"] = "ENRICHED" if m[i, j] > exp[i, j] else "DEPLETED" if m[i, j] < exp[i, j] else "NEUTRAL"
            rows.append(r)
            if k in core:
                g = core[k]
                agg[f"{g}|stratified_same_dir_q05"] += sdir == g and q_str[i, j] <= .05
                for t in per:
                    agg[f"{g}|{t}_same_dir"] += r[f"{t}_track_dir"] == g
                    agg[f"{g}|{t}_same_dir_q05"] += r[f"{t}_track_dir"] == g and r[f"{t}_track_q"] <= .05
                    agg[f"{g}|{t}_opposite_dir_q05"] += r[f"{t}_track_dir"] not in (g, "NEUTRAL") and r[f"{t}_track_q"] <= .05
                    agg[f"{g}|{t}_expected_lt5"] += r[f"{t}_track_expected"] < 5
    rep = {"edges_by_track": dict(Counter(track)), "documents_by_track": dict(Counter(docs[d]["track"] for d in {e[0] for e in edges})),
           "stratified_null_q05_cells": int((q_str <= .05).sum()),
           "core_agreement": dict(sorted(agg.items())),
           "depleted_core_detail": [(r["ai_family"] + " x " + r["decision_family"], round(r["stratified_q"], 4), r["AI_track_oe"], r["DECISION_track_oe"], r["DECISION_track_expected"])
                                    for r in rows if r["frozen_core_direction"] == "DEPLETED"]}
    L.write_csv(os.path.join(OUTD, "TRACK_SENSITIVITY_120.csv"), rows)
    L.write_json(os.path.join(OUTD, "TRACK_SENSITIVITY_REPORT.json"), rep)
    print(json.dumps(rep, indent=1, default=str))


if __name__ == "__main__":
    main()
