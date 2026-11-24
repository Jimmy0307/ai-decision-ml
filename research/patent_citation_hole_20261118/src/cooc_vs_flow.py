"""Plan 7 (PREREGISTRATION_COOCCURRENCE_VS_FLOW.md): co-occurrence (co-classification) vs flow (citations)
for all pairs of CPC main groups in G06/G16/H04 with >= 2,000 patents granted 2010-2025.

Usage:
    python src/cooc_vs_flow.py --inputs inputs_LOCAL --out outputs
Needs outputs/cache_citations_LOCAL.npz and outputs/plan5_cpc_LOCAL.npz; reads g_patent in chunks for grant years.
Writes outputs/PLAN7_RESULTS.json and outputs/PLAN7_PAIRS_primary.csv.
"""
import argparse
import csv
import gc
import json
import sys
import time
from pathlib import Path

import numpy as np
import scipy.sparse as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import patent_hole as ph  # noqa: E402

SEED = 20261119
Y0, Y1 = 2010, 2025
MIN_PAT = 2000
CH = 3_000_000


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def load_years(inputs: Path) -> np.ndarray:
    """Same filter as patent_hole.load_patents, read in chunks; returns int16 years in sorted-id order."""
    ids, yrs = [], []
    for ch in ph.read_tsv(ph.find_input(inputs, "g_patent"), ph.REQUIRED["g_patent"], chunksize=1_000_000):
        ch = ch[(ch.patent_type.str.strip('"').str.lower() == "utility")
                & (~ch.withdrawn.str.strip('"').isin(["1", "true", "True"]))]
        i = ph.numeric_ids(ch.patent_id)
        y = ph.pd.to_numeric(ch.patent_date.str.strip('"').str[:4], errors="coerce").to_numpy()
        ok = ~np.isnan(i) & ~np.isnan(y)
        ids.append(i[ok].astype(np.int64))
        yrs.append(y[ok].astype(np.int16))
    ids, yrs = np.concatenate(ids), np.concatenate(yrs)
    return yrs[np.argsort(ids, kind="stable")]


def memberships(year, z):
    idx = z["idx"].astype(np.int64)
    main = z["main"]
    names, codes = np.unique(main, return_inverse=True)
    n = len(year)
    inwin = (year >= Y0) & (year <= Y1)
    pairs = np.unique(idx * len(names) + codes)
    p, g = pairs // len(names), pairs % len(names)
    cnt = np.bincount(g[inwin[p]], minlength=len(names))
    sel = np.flatnonzero(cnt >= MIN_PAT)
    remap = -np.ones(len(names), np.int64)
    remap[sel] = np.arange(len(sel))
    keep = remap[g] >= 0
    p, g = p[keep], remap[g[keep]]
    indptr = np.zeros(n + 1, np.int64)
    indptr[1:] = np.cumsum(np.bincount(p, minlength=n))
    order = np.lexsort((g, p))
    return [str(x) for x in names[sel]], (indptr, g[order].astype(np.int32))


def cooccurrence(year, csr, G, y0, y1):
    indptr, grp = csr
    n = len(year)
    lens = np.diff(indptr)
    U = np.flatnonzero((lens > 0) & (year >= y0) & (year <= y1))
    pos, g = ph.explode(U, csr)
    X = sp.csr_matrix((np.ones(len(g)), (pos, g)), shape=(len(U), G))
    C = (X.T @ X).toarray()
    nA = np.diag(C).copy()
    N = len(U)
    E = np.outer(nA, nA) / N
    return C, nA, N, E


def flow(year, csr, G, ci, cj, keep):
    """Symmetric OE components for all field pairs (Plan 1 method; strata = citing year x cited year)."""
    ymin = int(year.min())
    ny = int(year.max()) - ymin + 1
    ci, cj = ci[keep], cj[keep]
    s = (year[ci].astype(np.int64) - Y0) * ny + (year[cj].astype(np.int64) - ymin)
    S = (Y1 - Y0 + 1) * ny
    M = np.bincount(s, minlength=S).astype(float)
    lens = np.diff(csr[0])
    inU_i, inU_j = lens[ci] > 0, lens[cj] > 0
    outF = np.zeros((S, G), np.int64)
    inF = np.zeros((S, G), np.int64)
    outFF = np.zeros(S * G * G, np.int64)
    inFF = np.zeros(S * G * G, np.int64)
    O = np.zeros(G * G, np.int64)
    for b in range(0, len(ci), CH):
        sl = slice(b, b + CH)
        a_i, a_j, a_s = ci[sl], cj[sl], s[sl]
        for rows, mats in ((np.flatnonzero(inU_i[sl]), "out"), (np.flatnonzero(inU_j[sl]), "in")):
            pat = a_i[rows] if mats == "out" else a_j[rows]
            pos, g = ph.explode(pat, csr)
            st = a_s[rows][pos]
            single = np.bincount(st * G + g, minlength=S * G).reshape(S, G)
            # pairs within the same patent: (a, b) both memberships of the patent
            cnt = np.bincount(pos, minlength=len(rows))
            multi = np.flatnonzero(cnt > 1)
            pp, gg = ph.explode(pat[multi], csr)
            # cartesian within each patent
            c2 = np.bincount(pp, minlength=len(multi))
            start = np.r_[0, np.cumsum(c2)[:-1]]
            rep = np.repeat(np.arange(len(pp)), c2[pp])
            off = np.arange(len(rep)) - np.repeat(np.cumsum(c2[pp]) - c2[pp], c2[pp])
            partner = gg[start[pp[rep]] + off]
            mine = gg[rep]
            ok = mine != partner
            sst = a_s[rows][multi][pp[rep][ok]]
            pair = np.bincount((sst * G + mine[ok]) * G + partner[ok], minlength=S * G * G)
            if mats == "out":
                outF += single
                outFF += pair
            else:
                inF += single
                inFF += pair
        # observed: citing in a\b, cited in b\a
        both = np.flatnonzero(inU_i[sl] & inU_j[sl])
        pi, gi = ph.explode(a_i[both], csr)
        pj, gj = ph.explode(a_j[both], csr)
        ni = np.bincount(pi, minlength=len(both))
        nj = np.bincount(pj, minlength=len(both))
        tot = ni * nj
        rep = np.repeat(np.arange(len(both)), tot)
        t = np.arange(tot.sum()) - np.repeat(np.cumsum(tot) - tot, tot)
        si = np.r_[0, np.cumsum(ni)[:-1]]
        sj = np.r_[0, np.cumsum(nj)[:-1]]
        A = gi[si[rep] + t // nj[rep]]
        B = gj[sj[rep] + t % nj[rep]]
        okA = ~ph.member(a_j[both][rep], A, csr, G)     # cited not in A
        okB = ~ph.member(a_i[both][rep], B, csr, G)     # citing not in B
        ok = okA & okB & (A != B)
        O += np.bincount(A[ok] * G + B[ok], minlength=G * G)
        del pi, gi, pj, gj, rep, t, A, B
        gc.collect()
        log("citations", min(b + CH, len(ci)), "of", len(ci))
    outFF = outFF.reshape(S, G, G)
    inFF = inFF.reshape(S, G, G)
    Mi = np.where(M > 0, 1 / np.maximum(M, 1), 0)
    E = np.zeros((G, G))
    for k in np.flatnonzero(M > 0):
        E += Mi[k] * (outF[k][:, None] - outFF[k]) * (inF[k][None, :] - inFF[k].T)
    O = O.reshape(G, G)
    Os, Es = O + O.T, E + E.T
    return Os, Es


def evaluate(OEc, OEf, Ec, Ef, nAB, emin, cut, iu, rng=None, boot=0, G=None):
    el = (Ec[iu] >= emin) & (Ef[iu] >= emin)
    oc, of = OEc[iu][el], OEf[iu][el]
    if cut == "quartile":
        tc, tf = np.quantile(oc, .25), np.quantile(of, .25)
    elif cut == "decile":
        tc, tf = np.quantile(oc, .10), np.quantile(of, .10)
    else:
        tc, tf = 0.5, 0.5
    cg, fg, over = oc <= tc, of <= tf, of >= 1
    from scipy.stats import spearmanr
    absent = nAB[iu][el] == 0
    res = {"eligible_pairs": int(el.sum()), "threshold_co": float(tc), "threshold_flow": float(tf),
           "c_gaps": int(cg.sum()), "f_gaps": int(fg.sum()),
           "PPV": float((cg & fg).sum() / cg.sum()) if cg.sum() else None,
           "base_rate_f_gap": float(fg.mean()),
           "reversal_rate": float((cg & over).sum() / cg.sum()) if cg.sum() else None,
           "spearman": float(spearmanr(oc, of).correlation),
           "absent_pairs": int(absent.sum()),
           "absent_f_gap_share": float(fg[absent].mean()) if absent.any() else None,
           "absent_over_share": float(over[absent].mean()) if absent.any() else None,
           "share_pairs_flow_over_1": float(over.mean())}
    if boot:
        a_idx, b_idx = iu[0][el], iu[1][el]
        ppv, rr, rho = [], [], []
        for r in range(boot):
            c = np.bincount(rng.integers(0, G, G), minlength=G)
            w = c[a_idx] * c[b_idx]
            m = w > 0
            ww = w[m]
            den = (ww * cg[m]).sum()
            ppv.append((ww * (cg & fg)[m]).sum() / den if den else np.nan)
            rr.append((ww * (cg & over)[m]).sum() / den if den else np.nan)
            rho.append(spearmanr(np.repeat(oc[m], ww), np.repeat(of[m], ww)).correlation)
        q = lambda v: [float(np.nanpercentile(v, 2.5)), float(np.nanpercentile(v, 97.5))]
        res["PPV_ci95"], res["reversal_ci95"], res["spearman_ci95"] = q(ppv), q(rr), q(rho)
    return res, el


def label(r):
    if r["PPV"] >= 0.80 and r["reversal_rate"] <= 0.05:
        return "RELIABLE"
    if r["PPV"] < 0.50 or r["reversal_rate"] >= 0.20:
        return "UNRELIABLE"
    return "MODERATE"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--boot", type=int, default=1000)
    a = ap.parse_args()
    t0 = time.time()
    year = load_years(a.inputs)
    z = np.load(a.out / "plan5_cpc_LOCAL.npz", allow_pickle=False)
    assert len(year) == len(z["flag_AI"]), "patent universe does not match the Plan 5 cache"
    names, csr = memberships(year, z)
    del z
    G = len(names)
    log("patents", len(year), "fields", G)
    iu = np.triu_indices(G, 1)
    cz = np.load(a.out / "cache_citations_LOCAL.npz")
    ci, cj, cat = cz["i"], cz["j"], cz["c"]
    yi = year[ci]
    base = (yi >= Y0) & (yi <= Y1)
    R = {"preregistration": "PREREGISTRATION_COOCCURRENCE_VS_FLOW.md", "fields": G, "pairs": len(iu[0]),
         "field_names": names, "specs": {}}
    rng = np.random.default_rng(SEED)
    specs = {"primary": dict(cit=base & cat, py=(Y0, Y1), emin=5, cut="quartile", boot=a.boot),
             "S1_strict": dict(same="primary", emin=5, cut="fixed"),
             "S2_all_categories": dict(cit=base, py=(Y0, Y1), emin=5, cut="quartile"),
             "S3_E20": dict(same="primary", emin=20, cut="quartile"),
             "S4_decile": dict(same="primary", emin=5, cut="decile"),
             "S5_2013_2018": dict(cit=base & cat & (yi >= 2013) & (yi <= 2018), py=(2013, 2018), emin=5, cut="quartile"),
             "S5_2019_2025": dict(cit=base & cat & (yi >= 2019) & (yi <= 2025), py=(2019, 2025), emin=5, cut="quartile")}
    cache = {}
    for name, sp_ in specs.items():
        key = sp_.get("same", name)
        if key not in cache:
            spc = specs[key]
            C, nA, N, Ec = cooccurrence(year, csr, G, *spc["py"])
            OEc = np.where(Ec > 0, C / np.where(Ec > 0, Ec, 1), np.nan)
            Os, Ef = flow(year, csr, G, ci, cj, spc["cit"])
            OEf = np.where(Ef > 0, Os / np.where(Ef > 0, Ef, 1), np.nan)
            cache[key] = (OEc, OEf, Ec, Ef, C, nA, N, Os)
            log("computed", key)
        OEc, OEf, Ec, Ef, C, nA, N, Os = cache[key]
        res, el = evaluate(OEc, OEf, Ec, Ef, C, sp_["emin"], sp_["cut"], iu, rng, sp_.get("boot", 0), G)
        res["label"] = label(res)
        res["N_cooccurrence_universe"] = int(N)
        R["specs"][name] = res
        log(name, json.dumps({k: res[k] for k in ("eligible_pairs", "PPV", "reversal_rate", "spearman", "label")}))
        if name == "primary":
            with open(a.out / "PLAN7_PAIRS_primary.csv", "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["field_a", "field_b", "n_a", "n_b", "n_ab", "E_co", "OE_co", "O_flow", "E_flow", "OE_flow", "eligible"])
                for k, (x, y) in enumerate(zip(*iu)):
                    w.writerow([names[x], names[y], int(nA[x]), int(nA[y]), int(C[x, y]), round(float(Ec[x, y]), 4),
                                round(float(OEc[x, y]), 6), int(Os[x, y]), round(float(Ef[x, y]), 4),
                                round(float(OEf[x, y]), 6), bool(el[k])])
            ai = [k for k, s in enumerate(names) if s.startswith("G06N")]
            dq = [k for k, s in enumerate(names) if s.startswith("G06Q10")]
            tc, tf = res["threshold_co"], res["threshold_flow"]
            R["ai_dec_pairs"] = [{"pair": f"{names[x]}~{names[y]}", "E_co": float(Ec[x, y]), "OE_co": float(OEc[x, y]),
                                  "E_flow": float(Ef[x, y]), "OE_flow": float(OEf[x, y]),
                                  "c_gap": bool(OEc[x, y] <= tc), "f_gap": bool(OEf[x, y] <= tf)}
                                 for x in ai for y in dq]
        if key == name and name.startswith("S5"):
            cache.pop(key)
        (a.out / "PLAN7_RESULTS.json").write_text(json.dumps(R, indent=1), encoding="utf-8")
    R["seconds"] = round(time.time() - t0)
    (a.out / "PLAN7_RESULTS.json").write_text(json.dumps(R, indent=1), encoding="utf-8")
    log("done", R["specs"]["primary"]["label"])


if __name__ == "__main__":
    main()
