"""Reliability statistics for V1 blind coding (53B §7). Used identically for AI pilot and human rounds.

Usage: python reliability_v2_2.py coderA.csv coderB.csv [coderC.csv ...] [--key sealed_key.json]
"""
from __future__ import annotations

import csv
import json
import random
import sys
from collections import Counter
from itertools import combinations

SEED, B = 20261011, 5000


def load(path):
    rows = {r["case_id"]: r for r in csv.DictReader(open(path, encoding="utf-8"))}
    assert len(rows) == 16, path
    return rows


def cohen_kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n ** 2
    return float("nan") if pe == 1 else (po - pe) / (1 - pe), po, pe


def kripp_alpha_nominal(data):
    """data: list of units, each a list of values (one per coder; None = missing)."""
    units = [[v for v in u if v is not None] for u in data]
    units = [u for u in units if len(u) >= 2]
    o = Counter()
    for u in units:
        m = len(u)
        for i, j in combinations(range(m), 2):
            for (x, y) in ((u[i], u[j]), (u[j], u[i])):
                o[(x, y)] += 1 / (m - 1)
    n_c = Counter()
    for (x, _), w in o.items():
        n_c[x] += w
    n = sum(n_c.values())
    do = sum(w for (x, y), w in o.items() if x != y)
    de = sum(n_c[x] * n_c[y] for x in n_c for y in n_c if x != y) / (n - 1)
    return float("nan") if de == 0 else 1 - do / de


def bootstrap_alpha(data):
    rng = random.Random(SEED)
    vals = []
    for _ in range(B):
        sample = [data[rng.randrange(len(data))] for _ in data]
        a = kripp_alpha_nominal(sample)
        if a == a:
            vals.append(a)
    vals.sort()
    if not vals:
        return (float("nan"), float("nan"), 0)
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1], len(vals)


def classify(alpha, lo):
    if alpha != alpha:
        return "UNDEFINED (no variance)"
    c = "RELIABLE" if alpha >= 0.800 else "TENTATIVE" if alpha >= 0.667 else "NOT_ACCEPTABLE"
    if lo != lo or lo < 0.667:
        c += "+IMPRECISE"
    return c


def report(paths, key=None):
    coders = [load(p) for p in paths]
    cases = sorted(coders[0])
    out = []
    for field in ("primary_code", "status"):
        data = [[c[k][field].strip() for c in coders] for k in cases]
        alpha = kripp_alpha_nominal(data)
        lo, hi, nb = bootstrap_alpha(data)
        line = {"field": field, "alpha": alpha, "ci95": (lo, hi), "boot_valid": nb, "class": classify(alpha, lo)}
        if len(coders) == 2:
            k, po, pe = cohen_kappa([d[0] for d in data], [d[1] for d in data])
            line.update(kappa=k, raw_agreement=po, expected_agreement=pe)
        out.append(line)
    jac = []
    for k in cases:
        sets = [{c[k]["primary_code"].strip()} | ({c[k]["secondary_code"].strip()} - {""}) for c in coders]
        for s1, s2 in combinations(sets, 2):
            jac.append(len(s1 & s2) / len(s1 | s2))
    disagreements = [(k, [(c[k]["primary_code"], c[k]["secondary_code"], c[k]["status"]) for c in coders])
                     for k in cases if len({(c[k]["primary_code"], c[k]["secondary_code"], c[k]["status"]) for c in coders}) > 1]
    conf = [sorted(int(c[k]["confidence"]) for k in cases) for c in coders]
    res = {"stats": out, "jaccard_mean": sum(jac) / len(jac), "disagreements_incl_secondary": disagreements,
           "median_confidence": [x[len(x) // 2] for x in conf]}
    if key:
        kj = json.load(open(key))
        inv = {v: g for g, v in kj["case"].items()}
        vs = []
        for k in cases:
            g = inv[k]
            p, s, st = kj["key"][g]
            for i, c in enumerate(coders):
                if c[k]["primary_code"].strip() != p or c[k]["status"].strip() != st:
                    vs.append((k, g, f"coder{i+1}", c[k]["primary_code"], c[k]["status"], p, st))
        res["vs_researcher_key"] = vs
    return res


if __name__ == "__main__":
    args = sys.argv[1:]
    key = None
    if "--key" in args:
        i = args.index("--key"); key = args[i + 1]; args = args[:i] + args[i + 2:]
    print(json.dumps(report(args, key), indent=1, default=str))
