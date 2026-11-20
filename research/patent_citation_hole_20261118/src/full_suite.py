"""Preregistration 3: full patent replication suite (P1-P10). See PREREGISTRATION_FULL_SUITE.md.

Usage:
    python src/full_suite.py --inputs inputs_LOCAL --out outputs [--quick]
Needs outputs/cache_citations_LOCAL.npz (from patent_hole.py). Raw inputs stay local;
outputs are aggregate tables plus public organisation names of candidate brokers.
"""
from __future__ import annotations

import argparse
import json
import pickle
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import scipy.sparse as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import patent_hole as ph  # noqa: E402
import ra_lib  # noqa: E402
from cpc_matrix_v9 import COLS, ROWS, assign_col, assign_row  # noqa: E402

SEED = 20261118
INDIVIDUAL_TYPES = {"4", "5", "14", "15"}
KEYWORDS = {
    "G06N3": r"neural|deep|network", "G06N5": r"knowledge|rule|inference|reasoning|ontolog|expert",
    "G06N7": r"probabil|bayes|fuzzy|stochastic|markov", "G06N10": r"quantum|qubit",
    "G06N20": r"machine learning|learning|training|model",
    "FORECAST_OPTIMISE": r"forecast|predict|optimi|route", "RESOURCE_SCHEDULING": r"resource|schedul|allocat|plan",
    "WORKFLOW": r"workflow|process", "RISK": r"risk", "STRATEGY": r"strateg|goal|decision",
    "PERFORMANCE": r"performance|evaluat|assess|productiv",
}
log = ph.log


# ============================================================================ data
def load_all(inputs: Path, out: Path):
    cache = out / "suite_cache_LOCAL.pkl"
    if cache.exists():
        with open(cache, "rb") as f:
            return pickle.load(f)
    files = {k: ph.find_input(inputs, k) for k in ("g_patent", "g_cpc_current", "g_assignee_disambiguated")}
    u = ph.load_patents(files["g_patent"])
    ai, dec = defaultdict(list), defaultdict(list)          # p -> [(sym, inventive)]
    for ch in ph.read_tsv(files["g_cpc_current"], ph.REQUIRED["g_cpc_current"], chunksize=5_000_000):
        s = ch.cpc_group.str.strip('"').str.replace(" ", "", regex=False)
        m = (s.str.startswith("G06N") | s.str.match(r"^G06Q10/0[46]")).to_numpy()
        if not m.any():
            continue
        idx = u.index(ph.numeric_ids(ch.patent_id[m]))
        inv = ch.cpc_type[m].str.strip('"').str.lower().isin(["inventive", "inventional"]).to_numpy()
        for p, sym, iv in zip(idx, s[m], inv):
            if p >= 0:
                (ai if sym.startswith("G06N") else dec)[int(p)].append((sym, bool(iv)))
    S = set(ai) | set(dec)
    log(f"AI patents {len(ai):,} DEC patents {len(dec):,}")
    titles = {}
    for ch in ph.read_tsv(files["g_patent"], ["patent_id", "patent_title"], chunksize=2_000_000):
        idx = u.index(ph.numeric_ids(ch.patent_id))
        for p, t in zip(idx, ch.patent_title):
            if p >= 0 and int(p) in S:
                titles[int(p)] = t.strip('"').lower()
    owners = defaultdict(set)
    names = {}
    cols = ["patent_id", "assignee_id", "disambig_assignee_organization", "assignee_type"]
    for ch in ph.read_tsv(files["g_assignee_disambiguated"], cols, chunksize=3_000_000):
        idx = u.index(ph.numeric_ids(ch.patent_id))
        typ = ch.assignee_type.str.strip('"').to_numpy()
        for p, a, n, t in zip(idx, ch.assignee_id, ch.disambig_assignee_organization, typ):
            if p >= 0 and int(p) in S and t not in INDIVIDUAL_TYPES and n.strip('"'):
                a = a.strip('"')
                owners[int(p)].add(a)
                names.setdefault(a, n.strip('"'))
    z = np.load(out / "cache_citations_LOCAL.npz")
    data = dict(year=u.year, ai=dict(ai), dec=dict(dec), titles=titles, owners=dict(owners), names=names,
                ci=z["i"], cj=z["j"], cat=z["c"])
    with open(cache, "wb") as f:
        pickle.dump(data, f, protocol=4)
    return data


# ============================================================================ documents
def doc_sets(ai_codes, dec_codes, inventive_only=False):
    a = [s for s, iv in ai_codes if iv or not inventive_only]
    d = [s for s, iv in dec_codes if iv or not inventive_only]
    rows = frozenset(assign_row(s) for s in a)
    cols = frozenset(c for c in (assign_col(s) for s in d) if c)
    raw = [(assign_row(x), assign_col(y)) for x in a for y in d if assign_col(y)]
    return rows, cols, raw


def documents_a(D, y0, y1, inventive_only=False):
    out = []
    for p in sorted(set(D["ai"]) & set(D["dec"])):
        if y0 <= D["year"][p] <= y1:
            r, c, raw = doc_sets(D["ai"][p], D["dec"][p], inventive_only)
            if r and c:
                out.append((f"P{p}", r, c, raw))
    return out


def documents_b(D, y0, y1, applicant=True, inventive_only=False):
    ci, cj, cat, year = D["ci"], D["cj"], D["cat"], D["year"]
    n = len(year)
    is_ai, is_dec = np.zeros(n, bool), np.zeros(n, bool)
    is_ai[list(D["ai"])] = True
    is_dec[list(D["dec"])] = True
    a_only, d_only = is_ai & ~is_dec, is_dec & ~is_ai
    yr = year[ci]
    m = ((a_only[ci] & d_only[cj]) | (d_only[ci] & a_only[cj])) & (yr >= y0) & (yr <= y1)
    if applicant:
        m &= cat
    out = []
    for k in np.flatnonzero(m).tolist():
        i, j = int(ci[k]), int(cj[k])
        a, d = (i, j) if a_only[i] else (j, i)
        r, c, raw = doc_sets(D["ai"][a], D["dec"][d], inventive_only)
        if r and c:
            out.append((f"C{k}", r, c, raw))
    return out


def edges_of(docs):
    E = [(d, r, c) for d, R, C, _ in docs for r in sorted(R) for c in sorted(C)]
    Rw = [(d, r, c) for d, _, _, raw in docs for r, c in raw]
    return E, Rw


# ============================================================================ P1: adapted document-preserving null
def m06p(docs, samples=5000, seed=20260919):
    """Permute column sets among documents within (|rows|,|cols|) strata; margins and block structure kept."""
    n = len(docs)
    Rm = np.zeros((n, len(ROWS)), np.float32)
    Cm = np.zeros((n, len(COLS)), np.float32)
    ri = {r: k for k, r in enumerate(ROWS)}
    cix = {c: k for k, c in enumerate(COLS)}
    strata = defaultdict(list)
    for k, (_, R, C, _) in enumerate(docs):
        for r in R:
            Rm[k, ri[r]] = 1
        for c in C:
            Cm[k, cix[c]] = 1
        strata[(len(R), len(C))].append(k)
    groups = [np.array(v) for v in strata.values() if len(v) > 1]
    obs = Rm.T @ Cm
    rng = np.random.default_rng(seed)
    ge = np.zeros_like(obs)
    le = np.zeros_like(obs)
    tot = np.zeros_like(obs)
    perm = np.arange(n)
    for _ in range(samples):
        for g in groups:
            perm[g] = rng.permutation(g)
        m = Rm.T @ Cm[perm]
        ge += m >= obs - 1e-9
        le += m <= obs + 1e-9
        tot += m
    p = ra_lib.two_sided((1 + ge) / (samples + 1), (1 + le) / (samples + 1))
    assert np.allclose((Rm.T @ Cm[perm]).sum(1), obs.sum(1)) and np.allclose((Rm.T @ Cm[perm]).sum(0), obs.sum(0))
    return tot / samples, p, {"documents": n, "strata": len(strata), "exchangeable_strata": len(groups),
                              "exchangeable_documents": int(sum(len(g) for g in groups))}


def three_test(r):
    ok = all(r[f"{t}_q05"] for t in ("main", "exact", "raw")) and len({r["main_dir"], r["exact_dir"], r["raw_dir"]}) == 1
    return r["main_dir"] if ok else ""


def analyse(docs, quick=False, seed_main=20260918, R=None, samples=None):
    E, Rw = edges_of(docs)
    R = R or (300 if quick else 10_000)
    samples = samples or (200 if quick else 5000)
    rows, summ = ra_lib.analyze(E, Rw, ROWS, COLS, R=R, run_doc=False, seeds=(seed_main, 20260919))
    mean, p, diag = m06p(docs, samples=samples)
    q = ra_lib.bh(p.ravel()).reshape(p.shape)
    for r in rows:
        i, j = ROWS.index(r["ai_family"]), COLS.index(r["decision_family"])
        r["m06p_q"] = float(q[i, j])
        r["m06p_dir"] = "ENRICHED" if r["observed"] > mean[i, j] else "DEPLETED" if r["observed"] < mean[i, j] else "NEUTRAL"
        r["m06p_q05"] = bool(q[i, j] <= .05)
        same = len({r["main_dir"], r["exact_dir"], r["m06p_dir"]}) == 1
        r["adapted_core"] = bool(same and r["main_q05"] and r["exact_q05"] and r["m06p_q05"])
        r["adapted_full_core"] = bool(r["adapted_core"] and r["raw_q05"] and r["raw_dir"] == r["main_dir"])
        r["three_test"] = three_test(r)
    cnt = lambda key, d: sum(1 for r in rows if r[key] and r["main_dir"] == d)  # noqa: E731
    summ.update(documents=len(docs), m06p=diag, m06p_q05=int(sum(r["m06p_q05"] for r in rows)),
                adapted_full_core_depleted=cnt("adapted_full_core", "DEPLETED"),
                adapted_full_core_enriched=cnt("adapted_full_core", "ENRICHED"),
                three_test_depleted=sum(r["three_test"] == "DEPLETED" for r in rows),
                three_test_enriched=sum(r["three_test"] == "ENRICHED" for r in rows))
    for k in ("structural_core", "full_core", "full_core_by_direction", "doc_null_diagnostics"):
        summ.pop(k, None)
    return rows, summ


def cellset(rows, key, direction="DEPLETED"):
    if key == "three_test":
        return {(r["ai_family"], r["decision_family"]) for r in rows if r["three_test"] == direction}
    return {(r["ai_family"], r["decision_family"]) for r in rows if r[key] and r["main_dir"] == direction}


# ============================================================================ P2
def seed_stability(docs, n=20, R=10_000):
    E, _ = edges_of(docs)
    hits = Counter()
    for k in range(n):
        _, mean, p = ra_lib.main_mc(E, ROWS, COLS, R=R, seed=20260918 + k)
        obs = ra_lib.matrix(E, ROWS, COLS)
        q = ra_lib.bh(p.ravel()).reshape(p.shape)
        for i, a in enumerate(ROWS):
            for j, c in enumerate(COLS):
                if q[i, j] <= .05:
                    hits[(a, c, "DEPLETED" if obs[i, j] < mean[i, j] else "ENRICHED")] += 1
    always = sum(v == n for v in hits.values())
    boundary = sorted([list(k) + [v] for k, v in hits.items() if v < n], key=lambda x: x[3])
    return {"seeds": n, "cells_always_q05": always, "boundary_cells": boundary}


def exact_bh(m):
    _, p = ra_lib.exact_hyper(m)
    return ra_lib.bh(p.ravel()).reshape(m.shape)


def fpr_power(docs, reps=1000, seed=SEED):
    E, _ = edges_of(docs)
    obs = ra_lib.matrix(E, ROWS, COLS)
    A = np.array([ROWS.index(r) for _, r, _ in E])
    Dd = np.array([COLS.index(c) for _, _, c in E])
    rng = np.random.default_rng(seed)
    false_cells = []
    for _ in range(reps):
        m = np.bincount(A * len(COLS) + rng.permutation(Dd), minlength=obs.size).reshape(obs.shape)
        false_cells.append(int((exact_bh(m) <= .05).sum()))
    exp = np.outer(obs.sum(1), obs.sum(0)) / obs.sum()
    detected, tested = 0, 0
    for i in range(obs.shape[0]):
        for j in range(obs.shape[1]):
            if exp[i, j] < 100:
                continue
            m = obs.astype(float).copy()
            cut = 0.2 * m[i, j]
            m[i, j] -= cut
            others = [k for k in range(obs.shape[1]) if k != j]
            m[i, others] += cut / len(others)
            m = np.rint(m).astype(int)
            q = exact_bh(m)
            e2 = np.outer(m.sum(1), m.sum(0)) / m.sum()
            tested += 1
            detected += int(q[i, j] <= .05 and m[i, j] < e2[i, j])
    fc = np.array(false_cells)
    return {"null_reps": reps, "mean_false_cells": float(fc.mean()), "share_any_false": float((fc > 0).mean()),
            "power_cells_tested": tested, "power_detected_20pct": detected,
            "power": detected / tested if tested else None}


# ============================================================================ P4
def label_audit(D):
    S = sorted(set(D["ai"]) | set(D["dec"]))
    S = [p for p in S if 2010 <= D["year"][p] and p in D["titles"]]
    lab = {}
    for p in S:
        ls = {assign_row(s) for s, _ in D["ai"].get(p, [])} | {assign_col(s) for s, _ in D["dec"].get(p, [])}
        lab[p] = ls - {None}
    out = {}
    for label, rx in KEYWORDS.items():
        r = re.compile(rx)
        inn = [p for p in S if label in lab[p]]
        outn = [p for p in S if label not in lab[p]]
        a = np.mean([bool(r.search(D["titles"][p])) for p in inn]) if inn else float("nan")
        b = np.mean([bool(r.search(D["titles"][p])) for p in outn]) if outn else float("nan")
        out[label] = {"n": len(inn), "hit_rate": float(a), "base_rate": float(b),
                      "lift": float(a / b) if b > 0 else None, "pass": bool(b > 0 and a / b >= 1.5)}
    return out


# ============================================================================ P5-P8 firm network
def constraint_sparse(W: sp.csr_matrix, block=2000):
    """Burt constraint for every node of a symmetric weighted graph (no self loops)."""
    s = np.asarray(W.sum(1)).ravel()
    inv = np.where(s > 0, 1 / np.where(s > 0, s, 1), 0)
    P = sp.diags(inv) @ W
    P = P.tocsr()
    c = np.zeros(W.shape[0])
    for b in range(0, W.shape[0], block):
        Pb = P[b:b + block]
        PPb = (Pb @ P).tocsr()
        mask = Pb.copy()
        mask.data[:] = 1
        tot = Pb + PPb.multiply(mask)
        c[b:b + block] = np.asarray(tot.power(2).sum(1)).ravel()
    return c, s


def firm_network(D):
    year = D["year"]
    ai, dec = D["ai"], D["dec"]
    S = {p for p in set(ai) | set(dec) if 2010 <= year[p]}
    ptype = {p: ("BRIDGE" if p in ai and p in dec else "AI" if p in ai else "DEC") for p in S}
    kinds = defaultdict(set)
    for p in S:
        for f in D["owners"].get(p, ()):
            kinds[f].add(ptype[p])
    group = {f: ("MIXED" if ("BRIDGE" in k or k >= {"AI", "DEC"}) else "AI_FIRM" if "AI" in k else "DEC_FIRM")
             for f, k in kinds.items()}
    firms = sorted(group)
    fi = {f: k for k, f in enumerate(firms)}
    ci, cj, cat = D["ci"], D["cj"], D["cat"]
    inS = np.zeros(len(year), bool)
    inS[list(S)] = True
    m = inS[ci] & inS[cj] & cat
    w = Counter()
    for i, j in zip(ci[m].tolist(), cj[m].tolist()):
        for a in D["owners"].get(i, ()):
            for b in D["owners"].get(j, ()):
                if a != b:
                    w[(min(fi[a], fi[b]), max(fi[a], fi[b]))] += 1
    r = np.array([k[0] for k in w], dtype=np.int64)
    c = np.array([k[1] for k in w], dtype=np.int64)
    v = np.array(list(w.values()), dtype=float)
    n = len(firms)
    W = sp.coo_matrix((np.r_[v, v], (np.r_[r, c], np.r_[c, r])), shape=(n, n)).tocsr()
    g = np.array([group[f] for f in firms])
    return firms, g, W


def firm_modules(D, firms, g, W, reps=1000, seed=SEED):
    con, s = constraint_sparse(W)
    deg = np.diff(W.indptr)
    act = s > 0
    out = {"firms_with_ties": int(act.sum()), "ties": int(W.nnz // 2), "tie_weight": float(W.sum() / 2),
           "groups": {k: int(((g == k) & act).sum()) for k in ("AI_FIRM", "DEC_FIRM", "MIXED")}}
    # (a) firm-level hole
    tot = W.sum() / 2
    Sg = {k: s[g == k].sum() for k in ("AI_FIRM", "DEC_FIRM", "MIXED")}
    Wc = W.tocoo()
    oe = {}
    for a, b in (("AI_FIRM", "DEC_FIRM"), ("AI_FIRM", "MIXED"), ("DEC_FIRM", "MIXED")):
        mask = ((g[Wc.row] == a) & (g[Wc.col] == b))
        O = float(Wc.data[mask].sum())
        E = Sg[a] * Sg[b] / (2 * tot)
        oe[f"{a}~{b}"] = {"O": O, "E": float(E), "OE": O / E if E else None}
    out["group_OE"] = oe
    x = oe["AI_FIRM~DEC_FIRM"]["OE"]
    out["firm_level_hole"] = bool(x is not None and x < 1 and x < oe["AI_FIRM~MIXED"]["OE"] and x < oe["DEC_FIRM~MIXED"]["OE"])
    # (b) broker test
    idx = np.flatnonzero(act)
    dec_bins = np.searchsorted(np.quantile(s[idx], np.linspace(0, 1, 11)[1:-1]), s[idx])
    obs_med = float(np.median(con[idx][g[idx] == "MIXED"]))
    rng = np.random.default_rng(seed)
    lab = g[idx].copy()
    null = []
    for _ in range(reps):
        perm = lab.copy()
        for b in np.unique(dec_bins):
            k = np.flatnonzero(dec_bins == b)
            perm[k] = rng.permutation(lab[k])
        null.append(np.median(con[idx][perm == "MIXED"]))
    null = np.array(null)
    p = float((1 + (null <= obs_med).sum()) / (reps + 1))
    out["broker_test"] = {"mixed_median_constraint": obs_med, "null_median": float(np.median(null)),
                          "p_one_sided_lower": p, "verdict": "MIXED_LOWER_CONSTRAINT" if p < .05 else "NOT_LOWER_THAN_DEGREE_MATCHED"}
    out["median_constraint_by_group"] = {k: float(np.median(con[idx][g[idx] == k])) for k in ("AI_FIRM", "DEC_FIRM", "MIXED")}
    cand = [k for k in np.argsort(con) if act[k] and g[k] == "MIXED" and deg[k] >= 5][:10]
    out["candidates"] = [{"firm": D["names"].get(firms[k], firms[k]), "constraint": float(con[k]), "degree": int(deg[k]),
                          "strength": float(s[k])} for k in cand]
    return out, con, s, cand


def removal_test(g, W, cand):
    import networkx as nx
    G = nx.from_scipy_sparse_array(W)
    ai = {k for k in G if g[k] == "AI_FIRM"}
    de = {k for k in G if g[k] == "DEC_FIRM"}
    Wc = W.tocoo()
    cross = (g[Wc.row] == "AI_FIRM") & (g[Wc.col] == "DEC_FIRM")
    base_cross = float(Wc.data[cross].sum())

    def check(removed):
        H = G.copy()
        H.remove_nodes_from(removed)
        comps = list(nx.connected_components(H))
        both = [c for c in comps if c & ai and c & de]
        keep = ~(np.isin(Wc.row, list(removed)) | np.isin(Wc.col, list(removed)))
        return {"connected": bool(both), "largest_component_with_both": max((len(c) for c in both), default=0),
                "cross_weight_retained": float(Wc.data[cross & keep].sum() / base_cross) if base_cross else None}
    res = {"all_10_removed": check(set(cand)), "baseline": check(set())}
    res["one_at_a_time_refuted"] = int(sum(check({k})["connected"] for k in cand))
    return res


def coassignment(D, firms, g):
    fi = {f: k for k, f in enumerate(firms)}
    sizes, comp = Counter(), Counter()
    for p, own in D["owners"].items():
        if D["year"][p] < 2010 or len(own) < 2:
            continue
        sizes[len(own)] += 1
        groups = frozenset(g[fi[f]] for f in own if f in fi)
        comp["+".join(sorted(groups))] += 1
    n = sum(sizes.values())
    joins = sum(v for k, v in comp.items() if "AI_FIRM" in k and ("DEC_FIRM" in k or "MIXED" in k))
    return {"hyperedges": n, "size_distribution": dict(sorted(sizes.items())), "group_composition": dict(comp),
            "share_joining_AI_FIRM_with_DEC_or_MIXED": joins / n if n else None}


def alias_check(D, firms, s, cand):
    def norm(x):
        x = re.sub(r"[^a-z0-9 ]", " ", x.lower())
        x = re.sub(r"\b(inc|corp|corporation|co|ltd|llc|limited|gmbh|ag|sa|plc|company|kk|bv|nv)\b", " ", x)
        return " ".join(x.split())
    by = defaultdict(set)
    for k, f in enumerate(firms):
        by[norm(D["names"].get(f, ""))].add(k)
    top = set(np.argsort(-s)[:50].tolist()) | set(cand)
    coll = [{"firm": D["names"].get(firms[k], firms[k]), "ids_sharing_name": len(by[norm(D["names"].get(firms[k], ""))])}
            for k in top if len(by[norm(D["names"].get(firms[k], ""))]) > 1]
    return {"checked": len(top), "with_possible_alias": len(coll), "examples": coll[:15]}


# ============================================================================ P9
def gap_validity(rows):
    m = np.zeros((len(ROWS), len(COLS)))
    q = np.ones_like(m)
    for r in rows:
        i, j = ROWS.index(r["ai_family"]), COLS.index(r["decision_family"])
        m[i, j] = r["observed"]
    W = np.block([[np.zeros((len(ROWS), len(ROWS))), m], [m.T, np.zeros((len(COLS), len(COLS)))]])
    con, _ = constraint_sparse(sp.csr_matrix(W))
    s = W.sum(1)
    P = W / np.where(s[:, None] > 0, s[:, None], 1)
    dyadic = (P ** 2).sum(1)
    key = "adapted_full_core" if any(r["adapted_full_core"] for r in rows) else "three_test"
    dep = cellset(rows, key)
    alt = {}
    for a, c in dep:
        i, j = ROWS.index(a), COLS.index(c)
        alt[f"{a}x{c}"] = int(sum(m[i, j2] > 0 and m[i2, j2] > 0 and m[i2, j] > 0
                                  for i2 in range(len(ROWS)) for j2 in range(len(COLS)) if i2 != i and j2 != j))
    thr = {}
    for t in (.01, .05):
        thr[str(t)] = sum(1 for r in rows if r["main_dir"] == "DEPLETED" and r["main_q"] <= t and r["exact_q"] <= t
                          and r["raw_q"] <= t and r["raw_dir"] == "DEPLETED" and r["exact_dir"] == "DEPLETED")
    return {"M16_constraint": {n: {"constraint": float(con[k]), "dyadic": float(dyadic[k]),
                                   "indirect": float(con[k] - dyadic[k])} for k, n in enumerate(ROWS + COLS)},
            "M17_alt_routes_for_depleted": alt, "depleted_set_used": key,
            "M18_three_test_depleted_by_threshold": thr}


# ============================================================================ main
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args(argv)
    t0 = time.time()
    D = load_all(a.inputs, a.out)
    y1 = 2025
    res_file = a.out / "FULL_SUITE_RESULTS.json"
    R = json.loads(res_file.read_text(encoding="utf-8")) if res_file.exists() else {}
    R["preregistration"] = "PREREGISTRATION_FULL_SUITE.md v1.0"

    def save():
        res_file.write_text(json.dumps(R, indent=2, default=str), encoding="utf-8")

    def cells_out(name, rows):
        import csv
        with open(a.out / f"SUITE_{name}_CELLS.csv", "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)

    parts = {"A": documents_a(D, 2010, y1), "B": documents_b(D, 2010, y1, True),
             "B_all": documents_b(D, 2010, y1, False)}
    log({k: len(v) for k, v in parts.items()})
    P1rows = {}
    if "P1" not in R:
        R["P1"] = {}
        for k, docs in parts.items():
            rows, summ = analyse(docs, a.quick)
            R["P1"][k] = summ
            P1rows[k] = rows
            cells_out(f"P1_{k}", rows)
            log("P1", k, summ["adapted_full_core_depleted"], summ["adapted_full_core_enriched"], summ["m06p"])
        conv = cellset(P1rows["A"], "adapted_full_core") & cellset(P1rows["B"], "adapted_full_core")
        R["P1"]["convergent_adapted_full_core_depleted"] = sorted(map(list, conv))
        conv3 = cellset(P1rows["A"], "three_test") & cellset(P1rows["B"], "three_test")
        R["P1"]["convergent_three_test_depleted"] = sorted(map(list, conv3))
        with open(a.out / "suite_p1rows_LOCAL.pkl", "wb") as f:
            pickle.dump(P1rows, f)
        save()
    else:
        with open(a.out / "suite_p1rows_LOCAL.pkl", "rb") as f:
            P1rows = pickle.load(f)
    if "P2" not in R:
        R["P2"] = {}
        for k in ("A", "B"):
            R["P2"][f"seed_{k}"] = seed_stability(parts[k], n=3 if a.quick else 20, R=300 if a.quick else 10_000)
            R["P2"][f"fpr_power_{k}"] = fpr_power(parts[k], reps=50 if a.quick else 1000)
            log("P2", k, R["P2"][f"fpr_power_{k}"])
        for seg, (fa, fb) in {"S1_inventive": (documents_a(D, 2010, y1, True), documents_b(D, 2010, y1, True, True)),
                              "S2_single_code": ([d for d in parts["A"] if len(d[1]) == 1 and len(d[2]) == 1],
                                                 [d for d in parts["B"] if len(d[1]) == 1 and len(d[2]) == 1])}.items():
            for k, docs in (("A", fa), ("B", fb)):
                rows, summ = analyse(docs, a.quick)
                dep = cellset(rows, "adapted_full_core")
                summ["overlap_with_P1_depleted"] = len(dep & cellset(P1rows[k], "adapted_full_core"))
                summ["three_test_overlap_with_P1"] = len(cellset(rows, "three_test") & cellset(P1rows[k], "three_test"))
                R["P2"][f"{seg}_{k}"] = summ
                log("P2", seg, k, summ["adapted_full_core_depleted"], summ["three_test_depleted"])
        save()
    if "P3" not in R:
        R["P3"] = {}
        halves = {"A": ((2010, 2017), (2018, 2025)), "B": ((2013, 2018), (2019, 2025))}
        for k, (h1, h2) in halves.items():
            sets = []
            for h in (h1, h2):
                docs = documents_a(D, *h) if k == "A" else documents_b(D, *h, True)
                rows, summ = analyse(docs, a.quick)
                R["P3"][f"{k}_{h[0]}_{h[1]}"] = summ
                sets.append((cellset(rows, "three_test"), cellset(rows, "adapted_full_core")))
            R["P3"][f"{k}_replicated_three_test_depleted"] = sorted(map(list, sets[0][0] & sets[1][0]))
            R["P3"][f"{k}_replicated_adapted_core_depleted"] = sorted(map(list, sets[0][1] & sets[1][1]))
            R["P3"][f"{k}_discovery_three_test_depleted"] = len(sets[0][0])
            log("P3", k, R["P3"][f"{k}_replicated_three_test_depleted"])
        save()
    if "P4" not in R:
        R["P4"] = label_audit(D)
        save()
    if "P5" not in R:
        firms, g, W = firm_network(D)
        R["P5"], con, s, cand = firm_modules(D, firms, g, W, reps=100 if a.quick else 1000)
        log("P5", R["P5"]["group_OE"], R["P5"]["broker_test"])
        R["P6"] = removal_test(g, W, cand)
        R["P7"] = coassignment(D, firms, g)
        R["P8"] = alias_check(D, firms, s, cand)
        save()
    if "P9" not in R:
        R["P9"] = {k: gap_validity(P1rows[k]) for k in ("A", "B")}
        save()
    R["P10"] = {"status": "NOT_APPLICABLE", "reason": "patents have no limitation/future-work section; full texts not downloaded"}
    R["seconds"] = round(time.time() - t0)
    save()
    log("suite done", R["seconds"], "s")


if __name__ == "__main__":
    sys.exit(main())
