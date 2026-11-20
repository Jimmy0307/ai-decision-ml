"""Plan 9 (PREREGISTRATION_OUT_OF_SAMPLE.md): out-of-sample replication of Plans 7 and 8 in all CPC fields
outside G06/G16/H04 (and outside section Y), plus the confirmatory neighbour hypothesis H9.

Usage:
    python src/oos_replication.py --inputs inputs_LOCAL --out outputs [--boot 1000]
Steps: (0) verify the sparse expected-flow code reproduces Plan 7 on G06/G16/H04; (1) extract held-out memberships
from g_cpc_current (cached); (2) Plan 7 battery; (3) Plan 8 battery + H9. Writes outputs/PLAN9_RESULTS.json.
"""
import argparse
import csv
import gc
import json
import re
import sys
import time
from pathlib import Path

import numpy as np
from scipy.stats import rankdata, spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parent))
import patent_hole as ph  # noqa: E402
import cooc_vs_flow as cf  # noqa: E402

SEED, Y0, Y1, MIN_PAT, CH = 20261119, 2010, 2025, 2000, 2_000_000
EXCL_CLASSES = ("G06", "G16", "H04")
FLOW_CACHE_DIR = None          # set in main(); per-specification flow matrices are cached so an interrupted run resumes


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


# ------------------------------------------------------------------ memberships
def heldout_memberships(inputs, year, cache):
    if cache.exists():
        z = np.load(cache, allow_pickle=False)
        names = [str(x) for x in z["names"]]
        return names, (z["indptr"], z["grp"])
    ids_sorted = cf_ids(inputs)
    gid, names_list = {}, []
    idx_all, code_all = [], []
    for k, ch in enumerate(ph.read_tsv(ph.find_input(inputs, "g_cpc_current"), ph.REQUIRED["g_cpc_current"], chunksize=5_000_000)):
        s = ch.cpc_group.str.strip('"').str.replace(" ", "", regex=False)
        main = s.str.split("/", n=1).str[0]
        cls = main.str[:3]
        keep = (~main.str.startswith("Y") & ~cls.isin(EXCL_CLASSES)).to_numpy()
        pid = ph.numeric_ids(ch.patent_id[keep])
        pos = np.searchsorted(ids_sorted, pid)
        pos = np.clip(pos, 0, len(ids_sorted) - 1)
        ok = ids_sorted[pos] == pid
        codes, uniq = ph.pd.factorize(main[keep])
        gmap = np.array([gid.setdefault(x, len(gid)) for x in uniq], np.int32)
        idx_all.append(pos[ok].astype(np.int32))
        code_all.append(gmap[codes[ok]])
        log("cpc chunk", k, "kept rows", sum(map(len, idx_all)))
    names_all = np.array(sorted(gid, key=gid.get))
    idx = np.concatenate(idx_all).astype(np.int64)
    code = np.concatenate(code_all).astype(np.int64)
    del idx_all, code_all
    G0 = len(names_all)
    pairs = np.unique(idx * G0 + code)
    p, g = pairs // G0, pairs % G0
    inwin = (year >= Y0) & (year <= Y1)
    cnt = np.bincount(g[inwin[p]], minlength=G0)
    sel = np.flatnonzero(cnt >= MIN_PAT)
    order_names = np.argsort(names_all[sel])
    sel = sel[order_names]
    remap = -np.ones(G0, np.int64)
    remap[sel] = np.arange(len(sel))
    m = remap[g] >= 0
    p, g = p[m], remap[g[m]]
    n = len(year)
    indptr = np.zeros(n + 1, np.int64)
    indptr[1:] = np.cumsum(np.bincount(p, minlength=n))
    o = np.lexsort((g, p))
    grp = g[o].astype(np.int32)
    names = [str(x) for x in names_all[sel]]
    np.savez(cache, names=np.array(names), indptr=indptr, grp=grp)
    return names, (indptr, grp)


def cf_ids(inputs):
    ids = []
    for ch in ph.read_tsv(ph.find_input(inputs, "g_patent"), ph.REQUIRED["g_patent"], chunksize=1_000_000):
        ch = ch[(ch.patent_type.str.strip('"').str.lower() == "utility")
                & (~ch.withdrawn.str.strip('"').isin(["1", "true", "True"]))]
        i = ph.numeric_ids(ch.patent_id)
        y = ph.pd.to_numeric(ch.patent_date.str.strip('"').str[:4], errors="coerce").to_numpy()
        ok = ~np.isnan(i) & ~np.isnan(y)
        ids.append(i[ok].astype(np.int64))
    return np.sort(np.concatenate(ids))


# ------------------------------------------------------------------ sparse expected flow (identical formula)
def _merge(keys_list, cnt_list):
    k = np.concatenate(keys_list)
    c = np.concatenate(cnt_list)
    u, inv = np.unique(k, return_inverse=True)
    return u, np.bincount(inv, weights=c).astype(np.int64)


def flow_sparse(year, csr, G, ci, cj, keep):
    ymin = int(year.min())
    ny = int(year.max()) - ymin + 1
    ci, cj = ci[keep], cj[keep]
    s = (year[ci].astype(np.int64) - Y0) * ny + (year[cj].astype(np.int64) - ymin)
    S = (Y1 - Y0 + 1) * ny
    M = np.bincount(s, minlength=S).astype(float)
    Mi = np.where(M > 0, 1 / np.maximum(M, 1), 0)
    lens = np.diff(csr[0])
    inU_i, inU_j = lens[ci] > 0, lens[cj] > 0
    outF = np.zeros((S, G), np.int64)
    inF = np.zeros((S, G), np.int64)
    ok_keys, ok_cnt, ik_keys, ik_cnt = [], [], [], []
    O = np.zeros(G * G, np.int64)
    GG = G * G
    for b in range(0, len(ci), CH):
        sl = slice(b, b + CH)
        a_i, a_j, a_s = ci[sl], cj[sl], s[sl]
        for which in ("out", "in"):
            rows = np.flatnonzero((inU_i if which == "out" else inU_j)[sl])
            pat = (a_i if which == "out" else a_j)[rows]
            pos, g = ph.explode(pat, csr)
            st = a_s[rows][pos]
            single = np.bincount(st * G + g, minlength=S * G).reshape(S, G)
            cnt = np.bincount(pos, minlength=len(rows))
            multi = np.flatnonzero(cnt > 1)
            pp, gg = ph.explode(pat[multi], csr)
            c2 = np.bincount(pp, minlength=len(multi))
            start = np.r_[0, np.cumsum(c2)[:-1]]
            rep = np.repeat(np.arange(len(pp)), c2[pp])
            off = np.arange(len(rep)) - np.repeat(np.cumsum(c2[pp]) - c2[pp], c2[pp])
            partner = gg[start[pp[rep]] + off]
            mine = gg[rep]
            okm = mine != partner
            sst = a_s[rows][multi][pp[rep][okm]]
            keys = sst * GG + mine[okm].astype(np.int64) * G + partner[okm]
            u, c = np.unique(keys, return_counts=True)
            if which == "out":
                outF += single
                ok_keys.append(u)
                ok_cnt.append(c)
            else:
                inF += single
                ik_keys.append(u)
                ik_cnt.append(c)
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
        A = gi[si[rep] + t // nj[rep]].astype(np.int64)
        Bb = gj[sj[rep] + t % nj[rep]].astype(np.int64)
        okA = ~ph.member(a_j[both][rep], A, csr, G)
        okB = ~ph.member(a_i[both][rep], Bb, csr, G)
        sel = okA & okB & (A != Bb)
        O += np.bincount(A[sel] * G + Bb[sel], minlength=GG)
        del pi, gi, pj, gj, rep, t, A, Bb
        if len(ok_keys) > 8:
            u, c = _merge(ok_keys, ok_cnt); ok_keys, ok_cnt = [u], [c]
            u, c = _merge(ik_keys, ik_cnt); ik_keys, ik_cnt = [u], [c]
        gc.collect()
        log("citations", min(b + CH, len(ci)), "of", len(ci))
    okk, okc = _merge(ok_keys, ok_cnt)
    ikk, ikc = _merge(ik_keys, ik_cnt)
    # E_ab = sum_s Mi (oA - oAB)(iB - iAB)
    E = (outF * Mi[:, None]).T @ inF.astype(float)
    ss, ab = okk // GG, okk % GG
    aa, bb = ab // G, ab % G
    np.subtract.at(E, (aa, bb), Mi[ss] * okc * inF[ss, bb])
    ss2, ab2 = ikk // GG, ikk % GG
    aa2, bb2 = ab2 // G, ab2 % G
    np.subtract.at(E, (aa2, bb2), Mi[ss2] * outF[ss2, aa2] * ikc)
    common, i1, i2 = np.intersect1d(okk, ikk, return_indices=True)
    sc, abc = common // GG, common % GG
    np.add.at(E, (abc // G, abc % G), Mi[sc] * okc[i1] * ikc[i2])
    np.fill_diagonal(E, 0)
    O = O.reshape(G, G)
    return O + O.T, E + E.T


# ------------------------------------------------------------------ Plan 8 battery (identical rules) + H9
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


def plan8_battery(names, iu, el, OEc, OEf, nA, C, Ef, tc, tf, boot):
    fa = [names[x] for x in iu[0][el]]
    fb = [names[x] for x in iu[1][el]]
    ia, ib = iu[0][el], iu[1][el]
    oc, of = OEc[iu][el], OEf[iu][el]
    na, nb, nab, ef = nA[ia].astype(float), nA[ib].astype(float), C[iu][el], Ef[iu][el]
    lev = np.array([level(x, y) for x, y in zip(fa, fb)])
    sect = np.array([x[0] == y[0] for x, y in zip(fa, fb)])
    n = len(oc)
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
        out["S2_b_level3"] = float(b0[2])
        b1 = wls(dlog, X, w * pos)
        out["S1_b_level2"], out["S1_b_level3"] = float(b1[1]), float(b1[2])
        for L in (1, 2, 3):
            m = lev == L
            out[f"mean_delta_L{L}"] = float((w * delta)[m].sum() / w[m].sum())
        rate = lambda sel, ev: float((w * (sel & ev)).sum() / (w * sel).sum()) if (w * sel).sum() else float("nan")
        g3, g12, g2 = cg & (lev == 3), cg & (lev < 3), cg & (lev == 2)
        out["false_gap_L3"], out["false_gap_L12"] = rate(g3, ~fg), rate(g12, ~fg)
        out["false_gap_diff"] = out["false_gap_L3"] - out["false_gap_L12"]
        out["reversal_L3"], out["reversal_L12"] = rate(g3, over), rate(g12, over)
        out["reversal_diff"] = out["reversal_L3"] - out["reversal_L12"]
        out["PPV_L1"], out["PPV_L2"], out["PPV_L3"] = rate(cg & (lev == 1), fg), rate(g2, fg), rate(g3, fg)
        out["REV_L1"], out["REV_L2"], out["REV_L3"] = rate(cg & (lev == 1), over), rate(g2, over), rate(g3, over)
        out["H9a_diff_PPV_L2_minus_L3"] = out["PPV_L2"] - out["PPV_L3"]
        out["H9b_diff_REV_L2_minus_L3"] = out["REV_L2"] - out["REV_L3"]
        out["PPV_L3a_same_section"] = rate(g3 & sect, fg)
        out["PPV_L3b_cross_section"] = rate(g3 & ~sect, fg)
        out["REV_L3a_same_section"] = rate(g3 & sect, over)
        out["REV_L3b_cross_section"] = rate(g3 & ~sect, over)
        return out

    obs = stats(np.ones(n))
    rng = np.random.default_rng(SEED)
    G = len(names)
    bs = []
    for r in range(boot):
        c = np.bincount(rng.integers(0, G, G), minlength=G)
        bs.append(stats((c[ia] * c[ib]).astype(float)))
    ci = {k: [float(np.nanpercentile([x[k] for x in bs], 2.5)), float(np.nanpercentile([x[k] for x in bs], 97.5))] for k in obs}
    order = obs["mean_delta_L1"] < obs["mean_delta_L2"] < obs["mean_delta_L3"]
    lo3, hi3 = ci["b_level3"]
    h8a = "SUPPORTED" if lo3 > 0 and order else "REVERSED" if hi3 < 0 else "NOT_SUPPORTED"
    h8b = "SUPPORTED" if ci["false_gap_diff"][0] > 0 else "NOT_SUPPORTED"
    a_lo, a_hi = ci["H9a_diff_PPV_L2_minus_L3"]
    b_lo, b_hi = ci["H9b_diff_REV_L2_minus_L3"]
    h9a, h9b = a_hi < 0, b_lo > 0
    rev = a_lo > 0 or b_hi < 0
    h9 = "REVERSED" if rev else "SUPPORTED" if h9a and h9b else "PARTIAL" if h9a or h9b else "NOT_SUPPORTED"
    return {"pairs_by_level": {f"L{L}": int((lev == L).sum()) for L in (1, 2, 3)},
            "c_gaps_by_level": {f"L{L}": int((cg & (lev == L)).sum()) for L in (1, 2, 3)},
            "c_gaps_L3_same_section": int((cg & (lev == 3) & sect).sum()),
            "c_gaps_L3_cross_section": int((cg & (lev == 3) & ~sect).sum()),
            "observed": obs, "ci95": ci, "mean_delta_ordered": bool(order),
            "H8a_replication": h8a, "H8b_replication": h8b, "H9a": bool(h9a), "H9b": bool(h9b), "H9": h9}


# ------------------------------------------------------------------ main
def battery(year, csr, G, ci, cj, cat, yi, base, names, boot, out_csv=None):
    iu = np.triu_indices(G, 1)
    rng = np.random.default_rng(SEED)
    specs = {"primary": dict(cit=base & cat, py=(Y0, Y1), emin=5, cut="quartile", boot=boot),
             "S1_strict": dict(same="primary", emin=5, cut="fixed"),
             "S2_all_categories": dict(cit=base, py=(Y0, Y1), emin=5, cut="quartile"),
             "S3_E20": dict(same="primary", emin=20, cut="quartile"),
             "S4_decile": dict(same="primary", emin=5, cut="decile"),
             "S5_2013_2018": dict(cit=base & cat & (yi >= 2013) & (yi <= 2018), py=(2013, 2018), emin=5, cut="quartile"),
             "S5_2019_2025": dict(cit=base & cat & (yi >= 2019) & (yi <= 2025), py=(2019, 2025), emin=5, cut="quartile")}
    R, cache = {}, {}
    for name, sp_ in specs.items():
        key = sp_.get("same", name)
        if key not in cache:
            spc = specs[key]
            C, nA, N, Ec = cf.cooccurrence(year, csr, G, *spc["py"])
            OEc = np.where(Ec > 0, C / np.where(Ec > 0, Ec, 1), np.nan)
            fc = FLOW_CACHE_DIR / f"plan9_flow_{key}_LOCAL.npz" if FLOW_CACHE_DIR else None
            if fc is not None and fc.exists():
                zf = np.load(fc)
                Os, Ef = zf["Os"], zf["Ef"]
                log("flow cache hit", key)
            else:
                Os, Ef = flow_sparse(year, csr, G, ci, cj, spc["cit"])
                if fc is not None:
                    np.savez(fc, Os=Os, Ef=Ef)
            OEf = np.where(Ef > 0, Os / np.where(Ef > 0, Ef, 1), np.nan)
            cache[key] = (OEc, OEf, Ec, Ef, C, nA, N, Os)
            log("computed", key)
        OEc, OEf, Ec, Ef, C, nA, N, Os = cache[key]
        res, el = cf.evaluate(OEc, OEf, Ec, Ef, C, sp_["emin"], sp_["cut"], iu, rng, sp_.get("boot", 0), G)
        res["label"] = cf.label(res)
        res["N_cooccurrence_universe"] = int(N)
        R[name] = res
        log(name, json.dumps({k: res[k] for k in ("eligible_pairs", "PPV", "reversal_rate", "spearman", "label")}))
        if name == "primary":
            prim = (iu, el, OEc, OEf, nA, C, Ef, res["threshold_co"], res["threshold_flow"])
            if out_csv:
                with open(out_csv, "w", newline="", encoding="utf-8") as f:
                    w = csv.writer(f)
                    w.writerow(["field_a", "field_b", "n_a", "n_b", "n_ab", "E_co", "OE_co", "O_flow", "E_flow", "OE_flow", "eligible"])
                    for k, (x, y) in enumerate(zip(*iu)):
                        if el[k]:
                            w.writerow([names[x], names[y], int(nA[x]), int(nA[y]), int(C[x, y]), round(float(Ec[x, y]), 4),
                                        round(float(OEc[x, y]), 6), int(Os[x, y]), round(float(Ef[x, y]), 4),
                                        round(float(OEf[x, y]), 6), bool(el[k])])
        if name.startswith("S5") or name == "S2_all_categories":
            cache.pop(key, None)
        gc.collect()
    return R, prim


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--years", type=Path, help="int16 grant-year array in universe order (instead of reading g_patent)")
    ap.add_argument("--verified-log", type=Path, help="log containing the passed verification line from an earlier run")
    a = ap.parse_args()
    global FLOW_CACHE_DIR
    FLOW_CACHE_DIR = a.out
    t0 = time.time()
    year = np.load(a.years) if a.years else cf.load_years(a.inputs)
    cz = np.load(a.out / "cache_citations_LOCAL.npz")
    ci, cj, cat = cz["i"], cz["j"], cz["c"]
    yi = year[ci]
    base = (yi >= Y0) & (yi <= Y1)
    out = {"preregistration": "PREREGISTRATION_OUT_OF_SAMPLE.md"}
    p7 = json.load(open(a.out / "PLAN7_RESULTS.json", encoding="utf-8"))["specs"]["primary"]
    if a.verified_log:
        line = [l for l in a.verified_log.read_text(encoding="utf-8").splitlines() if " verification " in l][0]
        out["verification_vs_plan7"] = json.loads(line.split(" verification ", 1)[1])
        out["verification_vs_plan7"]["source"] = "earlier run on the original machine (log line reproduced)"
        assert out["verification_vs_plan7"]["passed"]
        return run_heldout(a, year, ci, cj, cat, yi, base, out, p7, t0)
    # (0) verification on G06/G16/H04 against Plan 7
    z = np.load(a.out / "plan5_cpc_LOCAL.npz", allow_pickle=False)
    names7, csr7 = cf.memberships(year, z)
    del z
    G7 = len(names7)
    C7, nA7, N7, Ec7 = cf.cooccurrence(year, csr7, G7, Y0, Y1)
    Os7, Ef7 = flow_sparse(year, csr7, G7, ci, cj, base & cat)
    OEc7 = np.where(Ec7 > 0, C7 / np.where(Ec7 > 0, Ec7, 1), np.nan)
    OEf7 = np.where(Ef7 > 0, Os7 / np.where(Ef7 > 0, Ef7, 1), np.nan)
    v, _ = cf.evaluate(OEc7, OEf7, Ec7, Ef7, C7, 5, "quartile", np.triu_indices(G7, 1))
    diffs = {k: abs(v[k] - p7[k]) for k in ("PPV", "reversal_rate", "spearman")}
    out["verification_vs_plan7"] = {"diffs": diffs, "eligible_pairs": v["eligible_pairs"], "passed": all(d < 1e-9 for d in diffs.values())}
    log("verification", json.dumps(out["verification_vs_plan7"]))
    assert out["verification_vs_plan7"]["passed"], "sparse expected-flow code does not reproduce Plan 7"
    del C7, Ec7, Os7, Ef7, OEc7, OEf7
    gc.collect()
    return run_heldout(a, year, ci, cj, cat, yi, base, out, p7, t0)


def run_heldout(a, year, ci, cj, cat, yi, base, out, p7, t0):
    # (1) held-out memberships
    names, csr = heldout_memberships(a.inputs, year, a.out / "plan9_cpc_LOCAL.npz")
    G = len(names)
    out.update({"fields": G, "pairs": G * (G - 1) // 2, "field_names": names,
                "fields_by_section": {s: sum(x.startswith(s) for x in names) for s in "ABCDEFGH"}})
    log("held-out fields", G)
    # (2) Plan 7 battery
    R, prim = battery(year, csr, G, ci, cj, cat, yi, base, names, a.boot, a.out / "PLAN9_PAIRS_primary.csv")
    out["plan7_battery"] = R
    out["R7_replicates"] = R["primary"]["label"] == p7["label"] if "label" in p7 else R["primary"]["label"] == "MODERATE"
    (a.out / "PLAN9_RESULTS.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    # (3) Plan 8 battery + H9
    iu, el, OEc, OEf, nA, C, Ef, tc, tf = prim
    out["plan8_battery_and_H9"] = plan8_battery(names, iu, el, OEc, OEf, nA, C, Ef, tc, tf, a.boot)
    out["seconds"] = round(time.time() - t0)
    (a.out / "PLAN9_RESULTS.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    p8 = out["plan8_battery_and_H9"]
    log("done", R["primary"]["label"], p8["H8a_replication"], p8["H8b_replication"], p8["H9"])


if __name__ == "__main__":
    main()
