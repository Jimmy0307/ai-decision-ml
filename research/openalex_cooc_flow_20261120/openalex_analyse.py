"""Plan 10 analysis (PREREGISTRATION_OPENALEX.md): L7 (Plan 7 rules), L9 (neighbour hypothesis), L8 (divergence by level)
and the AI x decision location, from the aggregates written by openalex_fetch.py. Needs numpy and scipy only.

Usage:
    python openalex_analyse.py --work <dir with subfields.json, cooccurrence.npz, flow_aggregates.npz> --out PLAN10_RESULTS.json
    python openalex_analyse.py --selftest
"""
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.stats import rankdata, spearmanr

SEED, B = 20261119, 1000
AI_NAME = "Artificial Intelligence"
DEC_NAMES = ["Management Science and Operations Research", "Strategy and Management",
             "Information Systems and Management", "Management Information Systems"]


def expected_flow(agg, G):
    """E_AB = sum_s Mi(s) (out_A(s) - out_AB(s)) (in_B(s) - in_AB(s)); identical to Plan 7, sparse corrections."""
    M = agg["M"].astype(float)
    Mi = np.where(M > 0, 1 / np.maximum(M, 1), 0)
    outF, inF = agg["outF"].astype(float), agg["inF"].astype(float)
    E = (outF * Mi[:, None]).T @ inF
    ok, ov = agg["outFF_keys"], agg["outFF_vals"].astype(float)
    ik, iv = agg["inFF_keys"], agg["inFF_vals"].astype(float)
    if len(ok):
        s, a, b = ok.T
        np.subtract.at(E, (a, b), Mi[s] * ov * inF[s, b])
    if len(ik):
        s, a, b = ik.T
        np.subtract.at(E, (a, b), Mi[s] * outF[s, a] * iv)
    if len(ok) and len(ik):
        GG = G * G
        k1 = ok[:, 0] * GG + ok[:, 1] * G + ok[:, 2]
        k2 = ik[:, 0] * GG + ik[:, 1] * G + ik[:, 2]
        com, i1, i2 = np.intersect1d(k1, k2, return_indices=True)
        s, ab = com // GG, com % GG
        np.add.at(E, (ab // G, ab % G), Mi[s] * ov[i1] * iv[i2])
    np.fill_diagonal(E, 0)
    O = agg["O"].astype(float)
    return O + O.T, E + E.T


def evaluate(OEc, OEf, Ec, Ef, iu, emin, cut, G, boot=0):
    el = (Ec[iu] >= emin) & (Ef[iu] >= emin)
    oc, of = OEc[iu][el], OEf[iu][el]
    tc, tf = (np.quantile(oc, .25), np.quantile(of, .25)) if cut == "quartile" else (0.5, 0.5)
    cg, fg, over = oc <= tc, of <= tf, of >= 1
    r = {"eligible_pairs": int(el.sum()), "threshold_co": float(tc), "threshold_flow": float(tf),
         "c_gaps": int(cg.sum()), "PPV": float((cg & fg).sum() / cg.sum()), "reversal_rate": float((cg & over).sum() / cg.sum()),
         "spearman": float(spearmanr(oc, of).correlation), "base_rate_f_gap": float(fg.mean())}
    if boot:
        rng = np.random.default_rng(SEED)
        a_i, b_i = iu[0][el], iu[1][el]
        ppv, rr, rho = [], [], []
        for _ in range(boot):
            c = np.bincount(rng.integers(0, G, G), minlength=G)
            w = c[a_i] * c[b_i]
            m = w > 0
            ww = w[m]
            den = (ww * cg[m]).sum()
            ppv.append((ww * (cg & fg)[m]).sum() / den if den else np.nan)
            rr.append((ww * (cg & over)[m]).sum() / den if den else np.nan)
            rho.append(spearmanr(np.repeat(oc[m], ww), np.repeat(of[m], ww)).correlation)
        q = lambda v: [float(np.nanpercentile(v, 2.5)), float(np.nanpercentile(v, 97.5))]
        r["PPV_ci95"], r["reversal_ci95"], r["spearman_ci95"] = q(ppv), q(rr), q(rho)
    r["label"] = ("RELIABLE" if r["PPV"] >= .8 and r["reversal_rate"] <= .05 else
                  "UNRELIABLE" if r["PPV"] < .5 or r["reversal_rate"] >= .2 else "MODERATE")
    return r, el, (cg, fg, over, oc, of)


def neighbour(sf, iu, el, flags, nS, C, Ef, G):
    cg, fg, over, oc, of = flags
    fa, fb = iu[0][el], iu[1][el]
    field = np.array([s["field"] for s in sf])
    dom = np.array([s["domain"] for s in sf])
    lev = np.where(field[fa] == field[fb], 2, np.where(dom[fa] == dom[fb], 31, 32))
    n = len(oc)
    delta = rankdata(of) / n - rankdata(oc) / n
    na, nb, ef = nS[fa].astype(float), nS[fb].astype(float), Ef[iu][el]
    X = np.c_[np.ones(n), lev == 31, lev == 32, np.log(na * nb), np.abs(np.log(na) - np.log(nb)), np.log(ef)].astype(float)

    def st(w):
        rate = lambda sel, ev: float((w * (sel & ev)).sum() / (w * sel).sum()) if (w * sel).sum() else np.nan
        L3 = lev > 3
        o = {"PPV_L2": rate(cg & (lev == 2), fg), "PPV_L3": rate(cg & L3, fg),
             "REV_L2": rate(cg & (lev == 2), over), "REV_L3": rate(cg & L3, over),
             "PPV_L3a": rate(cg & (lev == 31), fg), "PPV_L3b": rate(cg & (lev == 32), fg),
             "mean_delta_L2": float((w * delta)[lev == 2].sum() / w[lev == 2].sum()),
             "mean_delta_L3a": float((w * delta)[lev == 31].sum() / w[lev == 31].sum()),
             "mean_delta_L3b": float((w * delta)[lev == 32].sum() / w[lev == 32].sum())}
        sw = np.sqrt(w)
        b, *_ = np.linalg.lstsq(X * sw[:, None], delta * sw, rcond=None)
        o["b_level3a_vs_2"], o["b_level3b_vs_2"] = float(b[1]), float(b[2])
        o["L9a_diff"], o["L9b_diff"] = o["PPV_L2"] - o["PPV_L3"], o["REV_L2"] - o["REV_L3"]
        return o
    obs = st(np.ones(n))
    rng = np.random.default_rng(SEED)
    bs = []
    for _ in range(B):
        c = np.bincount(rng.integers(0, G, G), minlength=G)
        bs.append(st((c[fa] * c[fb]).astype(float)))
    ci = {k: [float(np.nanpercentile([x[k] for x in bs], 2.5)), float(np.nanpercentile([x[k] for x in bs], 97.5))] for k in obs}
    a_lo, a_hi = ci["L9a_diff"]
    b_lo, b_hi = ci["L9b_diff"]
    h9a, h9b = a_hi < 0, b_lo > 0
    lab = ("REVERSED" if (a_lo > 0 or b_hi < 0) else "SUPPORTED" if h9a and h9b else "PARTIAL" if h9a or h9b else "NOT_SUPPORTED")
    return {"pairs_by_level": {"L2": int((lev == 2).sum()), "L3a": int((lev == 31).sum()), "L3b": int((lev == 32).sum())},
            "c_gaps_by_level": {"L2": int((cg & (lev == 2)).sum()), "L3": int((cg & (lev > 3)).sum())},
            "observed": obs, "ci95": ci, "L9a": bool(h9a), "L9b": bool(h9b), "L9": lab}


def analyse(work: Path):
    sf = json.loads((work / "subfields.json").read_text(encoding="utf-8"))
    G = len(sf)
    co = np.load(work / "cooccurrence.npz")
    C, N = co["C"].astype(float), float(co["N"])
    C = (C + C.T) / 2                         # group_by counts are symmetric up to retrieval timing; average
    nS = np.diag(C).copy()
    Ec = np.outer(nS, nS) / N
    OEc = np.where(Ec > 0, C / np.where(Ec > 0, Ec, 1), np.nan)
    agg = dict(np.load(work / "flow_aggregates.npz"))
    Os, Ef = expected_flow(agg, G)
    OEf = np.where(Ef > 0, Os / np.where(Ef > 0, Ef, 1), np.nan)
    iu = np.triu_indices(G, 1)
    R = {"preregistration": "PREREGISTRATION_OPENALEX.md", "subfields": G, "pairs": len(iu[0]),
         "cooccurrence_universe": N, "citations": int(agg["M"].sum())}
    R["L7_primary"], el, flags = evaluate(OEc, OEf, Ec, Ef, iu, 5, "quartile", G, boot=B)
    R["L7_S1_absolute"], _, _ = evaluate(OEc, OEf, Ec, Ef, iu, 5, "fixed", G)
    R["L7_S3_E20"], _, _ = evaluate(OEc, OEf, Ec, Ef, iu, 20, "quartile", G)
    R["L8_L9"] = neighbour(sf, iu, el, flags, nS, C, Ef, G)
    name = {s["name"]: i for i, s in enumerate(sf)}
    tc, tf = R["L7_primary"]["threshold_co"], R["L7_primary"]["threshold_flow"]
    loc = []
    for d in DEC_NAMES:
        if AI_NAME not in name or d not in name:
            loc.append({"pair": f"{AI_NAME}~{d}", "missing": True})
            continue
        a, b = name[AI_NAME], name[d]
        loc.append({"pair": f"{AI_NAME}~{d}", "E_co": float(Ec[a, b]), "OE_co": float(OEc[a, b]), "E_flow": float(Ef[a, b]),
                    "OE_flow": float(OEf[a, b]), "c_gap": bool(OEc[a, b] <= tc), "f_gap": bool(OEf[a, b] <= tf)})
    R["ai_decision_pairs"] = loc
    return R


def selftest():
    """Sparse E equals brute-force E on random synthetic citations with multi-membership."""
    rng = np.random.default_rng(0)
    G, S, n = 6, 4, 3000
    mem_i = [sorted(set(rng.integers(0, G, rng.integers(1, 4)))) for _ in range(n)]
    mem_j = [sorted(set(rng.integers(0, G, rng.integers(1, 4)))) for _ in range(n)]
    s = rng.integers(0, S, n)
    M = np.bincount(s, minlength=S)
    outF, inF, O = np.zeros((S, G)), np.zeros((S, G)), np.zeros((G, G))
    ok, ik = {}, {}
    for t in range(n):
        for a in mem_i[t]:
            outF[s[t], a] += 1
            for a2 in mem_i[t]:
                if a2 != a:
                    ok[(s[t], a, a2)] = ok.get((s[t], a, a2), 0) + 1
        for b in mem_j[t]:
            inF[s[t], b] += 1
            for b2 in mem_j[t]:
                if b2 != b:
                    ik[(s[t], b, b2)] = ik.get((s[t], b, b2), 0) + 1
        for a in set(mem_i[t]) - set(mem_j[t]):
            for b in set(mem_j[t]) - set(mem_i[t]):
                O[a, b] += 1
    agg = dict(M=M, outF=outF, inF=inF, O=O, outFF_keys=np.array(list(ok), np.int64), outFF_vals=np.array(list(ok.values())),
               inFF_keys=np.array(list(ik), np.int64), inFF_vals=np.array(list(ik.values())))
    _, Es = expected_flow(agg, G)
    Eb = np.zeros((G, G))
    for A in range(G):
        for Bb in range(G):
            if A == Bb:
                continue
            for k in range(S):
                oA = sum(1 for t in range(n) if s[t] == k and A in mem_i[t] and Bb not in mem_i[t])
                iB = sum(1 for t in range(n) if s[t] == k and Bb in mem_j[t] and A not in mem_j[t])
                Eb[A, Bb] += oA * iB / M[k]
    Eb = Eb + Eb.T
    print("selftest max abs diff", float(np.abs(Es - Eb).max()))
    assert np.allclose(Es, Eb)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    R = analyse(a.work)
    a.out.write_text(json.dumps(R, indent=1), encoding="utf-8")
    print(json.dumps({"L7": R["L7_primary"]["label"], "PPV": R["L7_primary"]["PPV"], "reversal": R["L7_primary"]["reversal_rate"],
                      "L9": R["L8_L9"]["L9"]}, indent=1))


if __name__ == "__main__":
    main()
