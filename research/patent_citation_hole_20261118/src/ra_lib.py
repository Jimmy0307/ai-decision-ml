"""Route A analysis engine: independent re-implementation of the V9 functional-matrix tests.

Four analyses on a document-deduplicated bipartite family matrix (AI family x Decision family):
  main   fixed-degree bipartite configuration null (stub shuffling), R Monte Carlo replicates
  exact  analytic hypergeometric test conditional on the global margins
  doc    document-preserving null: within-document decision-endpoint swaps (MCMC), thinned samples
  raw    hypergeometric test on non-deduplicated pair-eligible records
Two-sided p = min(1, 2*min(p_upper, p_lower)); Monte Carlo tails use (1+b)/(R+1).
Benjamini–Hochberg within each 120-cell (or k-cell) family of tests.
Structural core: q<=.05 in main, exact and doc with one shared direction; full core adds raw.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from collections import Counter, defaultdict

import numpy as np
from scipy.stats import hypergeom

csv.field_size_limit(2**31 - 1)

AI_FAMS = ["COORDINATION_EXECUTION", "EVALUATION_ASSESSMENT", "EXPLANATION_ASSURANCE", "GENERAL_REASONING_SYSTEMS",
           "GENERATION_SYNTHESIS", "HUMAN_AUGMENTATION", "PERCEPTION_EXTRACTION", "PREDICTION_RISK_ESTIMATION",
           "RECOMMENDATION_OPTIMIZATION", "RETRIEVAL_SYNTHESIS"]
DEC_FAMS = ["ALLOCATION_PLANNING", "EVALUATION_SELECTION", "EXECUTION_COORDINATION", "GENERAL_DECISION_PROCESS",
            "GOVERNANCE_OVERSIGHT", "HUMAN_REVIEW_ACCOUNTABILITY", "INFORMATION_ACQUISITION", "INFORMATION_SYNTHESIS",
            "OPTION_GENERATION", "PREDICTION_DIAGNOSIS", "PROBLEM_FRAMING", "RISK_ASSESSMENT"]

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INP = os.path.join(ROOT, "inputs_LOCAL_ONLY")
OUT = os.path.join(ROOT, "outputs")


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fields = fields or list(rows[0].keys())
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o))
        f.write("\n")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def bh(p):
    p = np.asarray(p, dtype=float)
    n = len(p)
    order = np.argsort(p, kind="mergesort")
    ranked = p[order] * n / np.arange(1, n + 1)
    q = np.minimum.accumulate(ranked[::-1])[::-1]
    out = np.empty(n)
    out[order] = np.minimum(q, 1.0)
    return out


def load_official_edges():
    """Document-level edges (doc, ai, dec) of the frozen V9 matrix (2,180 rows)."""
    return [(r["document_id"], r["ai_family"], r["decision_family"]) for r in read_csv(os.path.join(INP, "DOCUMENT_PAIR_EDGES_DEDUP.csv"))]


def load_official_raw_pairs():
    """Non-deduplicated pair-eligible records (doc, ai, dec) (3,125 rows)."""
    return [(r["document_id"], r["left_final_family"], r["right_final_family"])
            for r in read_csv(os.path.join(INP, "ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv"))]


def dedup(pairs):
    seen, out = set(), []
    for t in pairs:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def matrix(pairs, ai, dec):
    ai_i = {a: i for i, a in enumerate(ai)}
    de_i = {d: j for j, d in enumerate(dec)}
    m = np.zeros((len(ai), len(dec)), dtype=np.int64)
    for _, a, d in pairs:
        m[ai_i[a], de_i[d]] += 1
    return m


def two_sided(p_up, p_low):
    return np.minimum(1.0, 2.0 * np.minimum(p_up, p_low))


def main_mc(pairs, ai, dec, R=10_000, seed=20260918):
    ai_i = {a: i for i, a in enumerate(ai)}
    de_i = {d: j for j, d in enumerate(dec)}
    A = np.array([ai_i[a] for _, a, _ in pairs])
    D = np.array([de_i[d] for _, _, d in pairs])
    k = len(dec)
    obs = np.bincount(A * k + D, minlength=len(ai) * k)
    rng = np.random.default_rng(seed)
    ge = np.zeros_like(obs)
    le = np.zeros_like(obs)
    s = np.zeros(obs.shape, dtype=float)
    for _ in range(R):
        c = np.bincount(A * k + rng.permutation(D), minlength=len(ai) * k)
        ge += c >= obs
        le += c <= obs
        s += c
    p_up = (1 + ge) / (R + 1)
    p_low = (1 + le) / (R + 1)
    mean = s / R
    return obs.reshape(len(ai), k), mean.reshape(len(ai), k), two_sided(p_up, p_low).reshape(len(ai), k)


def exact_hyper(m):
    M = int(m.sum())
    ra, cd = m.sum(1), m.sum(0)
    p = np.ones(m.shape)
    exp = np.outer(ra, cd) / M if M else np.zeros(m.shape)
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            x = int(m[i, j])
            rv = hypergeom(M, int(cd[j]), int(ra[i]))
            p[i, j] = min(1.0, 2.0 * min(rv.cdf(x), rv.sf(x - 1)))
    return exp, p


def doc_null(pairs, ai, dec, samples=5000, burn=43_600, thin=4_360, seed=20260919):
    """Within-document decision-endpoint swaps. Documents drawn with probability proportional to
    their edge count among documents with >=2 edges; two distinct edges drawn uniformly; the swap
    (a1,d1),(a2,d2) -> (a1,d2),(a2,d1) is rejected if a1==a2, d1==d2, or a new edge already exists."""
    ai_i = {a: i for i, a in enumerate(ai)}
    de_i = {d: j for j, d in enumerate(dec)}
    k = len(dec)
    by_doc = defaultdict(list)
    for doc, a, d in pairs:
        by_doc[doc].append((ai_i[a], de_i[d]))
    docs = [e for e in by_doc.values() if len(e) >= 2]
    sets = [set(e) for e in docs]
    w = np.array([len(e) for e in docs], dtype=float)
    cum = np.cumsum(w / w.sum())
    m = matrix(pairs, ai, dec).ravel().astype(np.int64)
    obs = m.copy()
    rng = np.random.default_rng(seed)
    total = burn + samples * thin
    out = np.empty((samples, len(m)), dtype=np.int32)
    accepted, touched = 0, set()
    chunk = 1_000_000
    t, si = 0, 0
    while t < total:
        n = min(chunk, total - t)
        di = np.searchsorted(cum, rng.random(n), side="right")
        di = np.minimum(di, len(docs) - 1)
        u1 = rng.random(n)
        u2 = rng.random(n)
        for x in range(n):
            t += 1
            dj = int(di[x])
            e = docs[dj]
            L = len(e)
            i1 = int(u1[x] * L)
            i2 = int(u2[x] * (L - 1))
            if i2 >= i1:
                i2 += 1
            a1, d1 = e[i1]
            a2, d2 = e[i2]
            if a1 != a2 and d1 != d2:
                s = sets[dj]
                n1, n2 = (a1, d2), (a2, d1)
                if n1 not in s and n2 not in s:
                    s.discard((a1, d1)); s.discard((a2, d2)); s.add(n1); s.add(n2)
                    e[i1], e[i2] = n1, n2
                    m[a1 * k + d1] -= 1; m[a2 * k + d2] -= 1; m[a1 * k + d2] += 1; m[a2 * k + d1] += 1
                    accepted += 1
                    touched.add(dj)
            if t > burn and (t - burn) % thin == 0:
                out[si] = m
                si += 1
    ge = (out >= obs).sum(0)
    le = (out <= obs).sum(0)
    p = two_sided((1 + ge) / (samples + 1), (1 + le) / (samples + 1))
    diag = {"attempts": total, "accepted": accepted, "acceptance_rate": accepted / total,
            "documents_touched": len(touched), "exchangeable_documents": len(docs),
            "degrees_preserved": bool((out.reshape(samples, len(ai), k).sum(2) == obs.reshape(len(ai), k).sum(1)).all()
                                      and (out.reshape(samples, len(ai), k).sum(1) == obs.reshape(len(ai), k).sum(0)).all())}
    return out.mean(0).reshape(len(ai), k), p.reshape(len(ai), k), diag


def direction(obs, ref):
    return np.where(obs > ref, "ENRICHED", np.where(obs < ref, "DEPLETED", "NEUTRAL"))


def analyze(pairs_dedup, raw_pairs, ai, dec, R=10_000, doc_samples=5000, seeds=(20260918, 20260919), run_doc=True):
    obs, mc_mean, p_main = main_mc(pairs_dedup, ai, dec, R=R, seed=seeds[0])
    exp, p_exact = exact_hyper(obs)
    raw_m = matrix(raw_pairs, ai, dec)
    raw_exp, p_raw = exact_hyper(raw_m)
    q = {"main": bh(p_main.ravel()).reshape(obs.shape), "exact": bh(p_exact.ravel()).reshape(obs.shape),
         "raw": bh(p_raw.ravel()).reshape(obs.shape)}
    dirs = {"main": direction(obs, mc_mean), "exact": direction(obs, exp), "raw": direction(raw_m, raw_exp)}
    diag = {}
    if run_doc:
        doc_mean, p_doc, diag = doc_null(pairs_dedup, ai, dec, samples=doc_samples, seed=seeds[1])
        q["doc"] = bh(p_doc.ravel()).reshape(obs.shape)
        dirs["doc"] = direction(obs, doc_mean)
    rows = []
    for i, a in enumerate(ai):
        for j, d in enumerate(dec):
            r = {"ai_family": a, "decision_family": d, "observed": int(obs[i, j]), "raw_observed": int(raw_m[i, j]),
                 "expected_independence": round(float(exp[i, j]), 6),
                 "oe_ratio": round(float(obs[i, j] / exp[i, j]), 6) if exp[i, j] > 0 else "",
                 "main_null_mean": round(float(mc_mean[i, j]), 4)}
            for t in q:
                r[f"{t}_q"] = float(q[t][i, j])
                r[f"{t}_dir"] = str(dirs[t][i, j])
                r[f"{t}_q05"] = bool(q[t][i, j] <= 0.05)
            tests = ["main", "exact", "doc"] if run_doc else ["main", "exact"]
            same = len({r[f"{t}_dir"] for t in tests}) == 1
            r["structural_core"] = bool(same and all(r[f"{t}_q05"] for t in tests))
            r["full_core"] = bool(r["structural_core"] and r["raw_q05"] and r["raw_dir"] == r["main_dir"])
            r["core_direction"] = r["main_dir"] if r["full_core"] else ""
            rows.append(r)
    summary = {
        "cells": len(rows), "edges": int(obs.sum()), "raw_records": int(raw_m.sum()),
        "observed_nonzero": int((obs > 0).sum()),
        **{f"{t}_q05": int(sum(r[f"{t}_q05"] for r in rows)) for t in q},
        "structural_core": int(sum(r["structural_core"] for r in rows)),
        "full_core": int(sum(r["full_core"] for r in rows)),
        "full_core_by_direction": dict(Counter(r["core_direction"] for r in rows if r["full_core"])),
        "doc_null_diagnostics": diag,
    }
    return rows, summary
