"""SIMULATED_ONLY sidecar for Q1 Task E (sequential identification protocol, 05_Q1_SEQUENTIAL_IDENTIFICATION_VOI.md §6.3(6)).

Fully synthetic abstract instances (no enterprise parameters, no 51 import):
  K scale blocks theta_p in [0,1]; N candidate portfolios with multilinear value
  F(d,theta) = a_d + sum_p b_dp theta_p + sum_{p<r} c_dpr theta_p theta_r   (integer coefficients in [-5,5]);
  fixed candidate set (every candidate robustly feasible) -> MMR monotone and VOI >= 0 (Prop. E.1/E.2).
Evidence model: measuring block p reveals theta*_p exactly (theta* on the 1/8 lattice, i.e. finite evidence states).
Policies: FULL (measure all blocks in index order), VOI_VERTEX, VOI_GRID8, VOI_EXACT (1-D line-arrangement sup),
RANDOM (seeded order). Stopping rule A: MMR_t <= eps_R (eps_R = 0 is rule B).
Usage: python -I voi_sidecar_sim.py [n_instances] [out_json]
"""
import itertools
import json
import random
import sys
from fractions import Fraction as Fr

K, N = 4, 6


def make_instance(rng):
    pairs = list(itertools.combinations(range(K), 2))
    cands = {}
    for i in range(N):
        a = rng.randint(-5, 5)
        b = [rng.randint(-5, 5) for _ in range(K)]
        c = {pr: rng.randint(-5, 5) for pr in pairs}
        cands[f"d{i}"] = (a, b, c)
    theta_star = tuple(Fr(rng.randint(0, 8), 8) for _ in range(K))
    return cands, theta_star


def value(cand, th):
    a, b, c = cand
    return a + sum(bp * t for bp, t in zip(b, th)) + sum(cv * th[p] * th[r] for (p, r), cv in c.items())


class Counter:
    def __init__(self):
        self.mmr_evals = 0


def mmr(cands, box, ctr):
    ctr.mmr_evals += 1
    verts = list(itertools.product(*[sorted({lo, hi}) for lo, hi in box]))
    best = {th: max(value(f, th) for f in cands.values()) for th in verts}
    mr = {d: max(best[th] - value(f, th) for th in verts) for d, f in cands.items()}
    m = min(mr.values())
    return m, min(d for d in mr if mr[d] == m)


def fix(box, p, v):
    return [(v, v) if i == p else b for i, b in enumerate(box)]


def sup_values(cands, box, p, mode, ctr):
    lo, hi = box[p]
    if mode == "vertex":
        pts = [lo, hi]
    elif mode == "grid8":
        pts = [lo + (hi - lo) * Fr(t, 8) for t in range(9)]
    else:  # exact: endpoints + all pairwise intersections of affine pieces
        taus = list(itertools.product(*[sorted({a, b}) if i != p else [lo] for i, (a, b) in enumerate(box)]))
        lines = set()
        for tau in taus:
            at = lambda v: tuple(v if i == p else x for i, x in enumerate(tau))
            for f in cands.values():
                for g in cands.values():
                    a0, a1 = value(g, at(lo)) - value(f, at(lo)), value(g, at(hi)) - value(f, at(hi))
                    s = (a1 - a0) / (hi - lo)
                    lines.add((a0 - s * lo, s))
        pts = {lo, hi}
        for (c1, s1), (c2, s2) in itertools.combinations(sorted(lines), 2):
            if s1 != s2:
                x = (c2 - c1) / (s1 - s2)
                if lo <= x <= hi:
                    pts.add(x)
    return max(mmr(cands, fix(box, p, v), ctr)[0] for v in pts)


def run_policy(cands, theta_star, policy, eps_rel, rng):
    ctr = Counter()
    box = [(Fr(0), Fr(1))] * K
    m0, d = mmr(cands, box, ctr)
    eps = eps_rel * m0
    m, measured, order = m0, [], list(range(K))
    if policy == "RANDOM":
        rng.shuffle(order)
    while True:
        if policy != "FULL" and m <= eps:
            break
        open_blocks = [p for p in range(K) if box[p][0] != box[p][1]]
        if not open_blocks:
            break
        if policy in ("FULL", "RANDOM"):
            p = next(q for q in order if q in open_blocks)
        else:
            mode = {"VOI_VERTEX": "vertex", "VOI_GRID8": "grid8", "VOI_EXACT": "exact"}[policy]
            voi = {q: m - sup_values(cands, box, q, mode, ctr) for q in open_blocks}
            p = max(open_blocks, key=lambda q: (voi[q], -q))
        box = fix(box, p, theta_star[p])
        measured.append(p)
        m_new, d = mmr(cands, box, ctr)
        assert m_new <= m, "fixed-candidate MMR must be non-increasing (Prop. E.1)"
        m = m_new
    best = max(value(f, theta_star) for f in cands.values())
    realised = best - value(cands[d], theta_star)
    assert realised <= m, "realised regret at theta* must not exceed the final MMR (theta* in Theta^(T))"
    return dict(blocks=len(measured), mmr_evals=ctr.mmr_evals, final_mmr=float(m), realised_regret=float(realised),
                decision=d, mmr0=float(m0))


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    out = sys.argv[2] if len(sys.argv) > 2 else None
    policies = ["FULL", "VOI_VERTEX", "VOI_GRID8", "VOI_EXACT", "RANDOM"]
    summary = {}
    for eps_rel in (Fr(0), Fr(1, 10)):
        agg = {p: [] for p in policies}
        for s in range(n):
            cands, ts = make_instance(random.Random(1000 + s))
            for p in policies:
                agg[p].append(run_policy(cands, ts, p, eps_rel, random.Random(5000 + s)))
        key = f"eps_R={float(eps_rel)}*MMR0"
        summary[key] = {}
        for p, rows in agg.items():
            full = agg["FULL"]
            summary[key][p] = dict(
                mean_blocks=sum(r["blocks"] for r in rows) / n,
                mean_mmr_evals=sum(r["mmr_evals"] for r in rows) / n,
                mean_final_mmr=sum(r["final_mmr"] for r in rows) / n,
                mean_realised_regret=sum(r["realised_regret"] for r in rows) / n,
                max_realised_regret=max(r["realised_regret"] for r in rows),
                decision_value_equals_full=sum(1 for r, f in zip(rows, full) if r["realised_regret"] == f["realised_regret"]) / n)
    res = {"label": "SIMULATED_ONLY", "n_instances": n, "K_blocks": K, "N_candidates": N,
           "generator": "integer multilinear coefficients in [-5,5], theta* on 1/8 lattice, seeds 1000+s / 5000+s",
           "candidate_set": "fixed (all robustly feasible); evidence reveals theta*_p exactly", "summary": summary}
    txt = json.dumps(res, indent=2)
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(txt)
    print(txt)


if __name__ == "__main__":
    main()
