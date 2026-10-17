"""Q1 theory upgrade -- witness part w_voi (agent T3, Task E: sequential identification / VOI).

Pure stdlib, deterministic, exact rational arithmetic (fractions.Fraction). No imports from 51.
All functions re-implement the minimal v2.2 logic independently from the definitions in
42_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md:
  * regret benchmark (42 §13.2):  R_d(theta) = max_{d' in C} F(d',theta) - F(d,theta)
  * MaxRegret(d) = max_theta R_d(theta);  MMR(Theta) = min_{d in C} MaxRegret(d)
    (exact on the vertices of a product of boxes for multilinear F, 42 §13.2 / §13.3)
  * VOI_p = MMR(Theta) - sup_{v in V_p} MMR(Theta | theta_p = v)          (42 §13.5)
  * candidate set C = ROBUSTLY_FEASIBLE portfolios over the registered box (42 §13.3; 51 solve_robust)

Witnesses (all SIMULATED_ONLY constructive examples; none uses enterprise data):
  W6   vertex-conditioned VOI overstatement (T-SEN-7 oracle): vertex VOI_v = 1, exact VOI_v = 1/2
  W6b  candidate-set adaptivity: Theta shrinkage can RAISE MMR (0 -> 1) and give VOI_q = -1
  W6c  grid refinement: nested grids monotone; non-nested (4 -> 5) not; edge-only prob grid does not converge
  W6d  Theta-independent pointwise-feasible benchmark restores monotonicity but loses vertex exactness
  W6e  myopic VOI complementarity: VOI_v = VOI_q = 0 while joint identification removes all regret
  W6f  non-termination without discretised evidence: strictly shrinking boxes, MMR stays >= 1/4
"""
from fractions import Fraction as _W6Fr
import itertools as _w6_it

_W6_H = _W6Fr(1, 2)


# ----------------------------------------------------------------------------- helpers (prefixed _w6_)
def _w6_vertices(box):
    """box: list of (L, U) per scale block -> list of vertex tuples (deduplicated when L == U)."""
    return [tuple(v) for v in _w6_it.product(*[sorted({lo, hi}) for lo, hi in box])]


def _w6_mmr_on(cands, thetas):
    """cands: {name: f(theta)->Fraction}. Exact minimax regret over the finite theta list.
    Returns (mmr, sorted list of minimisers, {name: MaxRegret})."""
    if not cands:
        return None, [], {}
    best = {th: max(f(th) for f in cands.values()) for th in thetas}
    mr = {d: max(best[th] - f(th) for th in thetas) for d, f in cands.items()}
    m = min(mr.values())
    return m, sorted(d for d in mr if mr[d] == m), mr


def _w6_mmr_box(cands, box):
    """MMR over a product of boxes; exact for multilinear F because each R_d is blockwise convex (42 §13.2)."""
    return _w6_mmr_on(cands, _w6_vertices(box))[0]


def _w6_fix(box, p, v):
    return [(v, v) if i == p else b for i, b in enumerate(box)]


def _w6_voi(cands, box, p, values):
    """v2.2 VOI_p with sup over the supplied value set (fixed candidate set)."""
    per_v = {v: _w6_mmr_box(cands, _w6_fix(box, p, v)) for v in values}
    worst = max(per_v.values())
    return _w6_mmr_box(cands, box) - worst, per_v


def _w6_grid(lo, hi, n):
    return [lo + (hi - lo) * _W6Fr(t, n) for t in range(n + 1)]


def _w6_exact_sup_1d(cands, box, p):
    """Exact sup_{v in [L,U]} MMR(box | theta_p = v) for a scale block p.
    With the other blocks at vertices tau, every F(d', v, tau) - F(d, v, tau) is affine in v; MMR(v) is a
    min of maxima of these lines, hence piecewise linear with kinks only at pairwise intersections.
    Evaluating at the endpoints and all intersections in [L, U] gives the exact supremum."""
    lo, hi = box[p]
    taus = _w6_vertices([b if i != p else (lo, lo) for i, b in enumerate(box)])
    lines = set()
    for tau in taus:
        at = lambda v: tuple(v if i == p else x for i, x in enumerate(tau))
        for d, f in cands.items():
            for d2, g in cands.items():
                a0 = g(at(lo)) - f(at(lo))
                a1 = g(at(hi)) - f(at(hi))
                slope = (a1 - a0) / (hi - lo)
                lines.add((a0 - slope * lo, slope))
    pts = {lo, hi}
    lines = sorted(lines)
    for (c1, s1), (c2, s2) in _w6_it.combinations(lines, 2):
        if s1 != s2:
            x = (c2 - c1) / (s1 - s2)
            if lo <= x <= hi:
                pts.add(x)
    vals = {x: _w6_mmr_box(cands, _w6_fix(box, p, x)) for x in pts}
    arg = max(vals, key=lambda x: (vals[x], -x))
    return vals[arg], arg, len(pts)


def _w6_robust_cands(portfolios, box):
    """portfolios: {name: (value_fn, slack_fn)}; ROBUSTLY_FEASIBLE iff slack >= 0 at every vertex (slack affine
    per block, so exact; 42 §13.3 feasibility classes)."""
    vs = _w6_vertices(box)
    return {d: vf for d, (vf, sf) in portfolios.items() if all(sf(th) >= 0 for th in vs)}


def _w6_s(x):
    return str(x) if isinstance(x, _W6Fr) else x


# ----------------------------------------------------------------------------- W6
def witness_W6() -> dict:
    box = [(_W6Fr(0), _W6Fr(1)), (_W6Fr(0), _W6Fr(1))]          # theta = (v, q)
    F = {"A": lambda t: 1 - t[0], "B": lambda t: t[0], "D": lambda t: t[1], "E": lambda t: 1 - t[1]}
    mmr_all = _w6_mmr_box(F, box)
    voi_vert, per_vert = _w6_voi(F, box, 0, [_W6Fr(0), _W6Fr(1)])
    voi_g4, per_g4 = _w6_voi(F, box, 0, _w6_grid(_W6Fr(0), _W6Fr(1), 4))
    sup_exact, arg_exact, n_bp = _w6_exact_sup_1d(F, box, 0)
    voi_true = mmr_all - sup_exact
    voi_q_true = mmr_all - _w6_exact_sup_1d(F, box, 1)[0]
    # closed form MMR(v) = min(v, 1 - v) checked on a 24-point grid
    closed_ok = all(_w6_mmr_box(F, _w6_fix(box, 0, v)) == min(v, 1 - v) for v in _w6_grid(_W6Fr(0), _W6Fr(1), 24))
    # guarantee failure: vertex VOI promises MMR_{t+1} <= 1 - 1 = 0, realised at v_obs = 1/2 is 1/2
    realised_after = _w6_mmr_box(F, _w6_fix(box, 0, _W6_H))
    # minimality search: 2 candidates X = v, Y = q (2 blocks) already overstates; 1 block cannot (point -> MMR 0)
    Fmin = {"X": lambda t: t[0], "Y": lambda t: t[1]}
    m_all = _w6_mmr_box(Fmin, box)
    m_vert = m_all - max(_w6_mmr_box(Fmin, _w6_fix(box, 0, v)) for v in (_W6Fr(0), _W6Fr(1)))
    m_true = m_all - _w6_exact_sup_1d(Fmin, box, 0)[0]
    one_block = {"A": lambda t: 1 - t[0], "B": lambda t: t[0]}
    ob_box = [(_W6Fr(0), _W6Fr(1))]
    ob_vert = _w6_mmr_box(one_block, ob_box) - max(_w6_mmr_box(one_block, [(v, v)]) for v in (_W6Fr(0), _W6Fr(1)))
    ob_true = _w6_mmr_box(one_block, ob_box) - _w6_exact_sup_1d(one_block, ob_box, 0)[0]
    ok = (mmr_all == 1 and voi_vert == 1 and voi_g4 == _W6_H and voi_true == _W6_H and arg_exact == _W6_H
          and voi_q_true == _W6_H and closed_ok and realised_after == _W6_H
          and m_all == 1 and m_vert == 1 and m_true == _W6_H and ob_vert == ob_true)
    return {
        "id": "W6", "title": "Vertex-conditioned VOI overstates the v2.2 VOI (T-SEN-7 analytic oracle)",
        "source_test": "51 t_sen7_regret_voi part (1); 42 §13.5 vertex/grid VOI; 59a §3.13 VOI paragraph",
        "inputs": {"blocks": "v in [0,1], q in [0,1] (scale blocks, product box Theta)",
                   "candidates": "F_A = 1 - v, F_B = v, F_D = q, F_E = 1 - q (fixed candidate set)",
                   "VOI": "VOI_v = MMR(Theta) - sup_{v' in V} MMR(Theta | v = v')",
                   "V": "vertex {0,1}; grid {0,1/4,1/2,3/4,1}; exact = [0,1] via line-arrangement breakpoints"},
        "rankings": {"MMR(v) closed form": "min(v, 1 - v), maximised at v = 1/2"},
        "choices": {"vertex sup attained at": "v in {0,1} (MMR 0)", "exact sup attained at": _w6_s(arg_exact)},
        "outputs": {"MMR(Theta)": _w6_s(mmr_all), "VOI_v vertex": _w6_s(voi_vert), "VOI_v grid4": _w6_s(voi_g4),
                    "VOI_v exact": _w6_s(voi_true), "VOI_q exact": _w6_s(voi_q_true), "breakpoints evaluated": n_bp,
                    "MMR after observing v = 1/2": _w6_s(realised_after),
                    "promised by vertex VOI": "0", "minimal (X=v, Y=q): vertex/exact": [_w6_s(m_vert), _w6_s(m_true)],
                    "one-block (A=1-v,B=v): vertex/exact": [_w6_s(ob_vert), _w6_s(ob_true)]},
        "expected": {"MMR(Theta)": "1", "VOI_v vertex": "1", "VOI_v grid4": "1/2", "VOI_v exact": "1/2",
                     "MMR after v=1/2": "1/2 (vertex VOI's implied guarantee 0 is violated)"},
        "pass": ok,
        "minimality": ("Minimal size is 2 candidates x 2 scale blocks: (X = v, Y = q) gives vertex VOI_v = 1 vs exact 1/2. "
                       "One candidate: MMR = 0 identically. One block: conditioning on theta_p = v makes Theta a point, "
                       "MMR(point) = 0 for every v, so vertex and exact VOI coincide (= MMR(Theta)); checked for A=1-v, B=v."),
    }


# ----------------------------------------------------------------------------- W6b
def witness_W6b() -> dict:
    one = _W6Fr(1)
    port = {"A": (lambda t: t[0], lambda t: one),                     # always feasible
            "B": (lambda t: 1 - t[0], lambda t: _W6_H - t[1])}         # slack 1/2 - q, affine in q
    box0 = [(_W6Fr(0), one), (_W6Fr(0), one)]
    box1 = [(_W6Fr(0), one), (_W6Fr(0), _W6_H)]                         # evidence narrows q to [0, 1/2]
    C0, C1 = _w6_robust_cands(port, box0), _w6_robust_cands(port, box1)
    mmr0, arg0, _ = _w6_mmr_on(C0, _w6_vertices(box0))
    mmr1, arg1, _ = _w6_mmr_on(C1, _w6_vertices(box1))
    # fixed-candidate MMR on Theta^(1) (C frozen at C(Theta^(0)))
    mmr1_fixed = _w6_mmr_box(C0, box1)
    # adaptive VOI_q (candidate set recomputed on the conditioned set), vertex values of q
    per_q = {}
    for qv in (_W6Fr(0), one):
        bq = _w6_fix(box0, 1, qv)
        per_q[qv] = _w6_mmr_box(_w6_robust_cands(port, bq), bq)
    voi_q_adaptive = mmr0 - max(per_q.values())
    voi_q_fixed = mmr0 - max(_w6_mmr_box(C0, _w6_fix(box0, 1, qv)) for qv in (_W6Fr(0), one))
    # one-block variant for the MMR increase: B slack 4/5 - v
    p1 = {"A": (lambda t: t[0], lambda t: one), "B": (lambda t: 1 - t[0], lambda t: _W6Fr(4, 5) - t[0])}
    b0, b1 = [(_W6Fr(0), one)], [(_W6Fr(0), _W6Fr(4, 5))]
    ob0 = _w6_mmr_box(_w6_robust_cands(p1, b0), b0)
    ob1 = _w6_mmr_box(_w6_robust_cands(p1, b1), b1)
    ok = (sorted(C0) == ["A"] and sorted(C1) == ["A", "B"] and mmr0 == 0 and mmr1 == 1 and mmr1_fixed == 0
          and voi_q_adaptive == -1 and voi_q_fixed == 0 and ob0 == 0 and ob1 == _W6Fr(3, 5))
    return {
        "id": "W6b", "title": "Adaptive robust candidate set: Theta shrinkage raises MMR and makes VOI negative",
        "source_test": "51 solve_robust (candidates = ROBUSTLY_FEASIBLE on the group box), T-SEN-4 feasibility classes; 42 §13.3",
        "inputs": {"blocks": "v in [0,1], q in [0,1]",
                   "portfolios": "A: F = v, slack 1 (robustly feasible); B: F = 1 - v, slack 1/2 - q (feasible iff q <= 1/2)",
                   "Theta^(0)": "[0,1] x [0,1]", "Theta^(1)": "[0,1] x [0,1/2]  (block-wise shrinkage of q)",
                   "one-block variant": "v in [0,1]; A: F = v; B: F = 1 - v, slack 4/5 - v; Theta^(1) = [0, 4/5]"},
        "rankings": {"Theta^(1)": "A best for v >= 1/2, B best for v <= 1/2 (crossing inside the box)"},
        "choices": {"d*_0": arg0, "d*_1": arg1},
        "outputs": {"C(Theta^(0))": sorted(C0), "C(Theta^(1))": sorted(C1), "MMR_0": _w6_s(mmr0),
                    "MMR_1 adaptive": _w6_s(mmr1), "MMR_1 with C frozen at C(Theta^(0))": _w6_s(mmr1_fixed),
                    "MMR(Theta|q) adaptive, q in {0,1}": {str(k): _w6_s(v) for k, v in per_q.items()},
                    "VOI_q adaptive": _w6_s(voi_q_adaptive), "VOI_q fixed candidates": _w6_s(voi_q_fixed),
                    "one-block MMR_0 -> MMR_1": [_w6_s(ob0), _w6_s(ob1)]},
        "expected": {"MMR_0": "0", "MMR_1 adaptive": "1 (increase)", "VOI_q adaptive": "-1", "VOI_q fixed": "0",
                     "one-block": "0 -> 3/5"},
        "pass": ok,
        "minimality": ("2 portfolios is minimal (one candidate has zero regret). The MMR increase needs only one block "
                       "(one-block variant 0 -> 3/5). A negative adaptive VOI needs >= 2 blocks: with one block the conditioned "
                       "set is a point, adaptive MMR(point) = 0 <= MMR(Theta), so VOI >= 0."),
    }


# ----------------------------------------------------------------------------- W6c
def witness_W6c() -> dict:
    box = [(_W6Fr(0), _W6Fr(1)), (_W6Fr(0), _W6Fr(1))]
    F = {"A": lambda t: 1 - t[0], "B": lambda t: t[0], "D": lambda t: t[1], "E": lambda t: 1 - t[1]}
    voi_n = {n: _w6_voi(F, box, 0, _w6_grid(_W6Fr(0), _W6Fr(1), n))[0] for n in (1, 2, 3, 4, 5, 8, 9, 16)}
    nested_chain = [1, 2, 4, 8, 16]
    nested_ok = all(voi_n[a] >= voi_n[b] for a, b in zip(nested_chain, nested_chain[1:]))
    true_v = 1 - _w6_exact_sup_1d(F, box, 0)[0]
    upper_ok = all(voi_n[n] >= true_v for n in voi_n)
    non_nested_increase = voi_n[5] > voi_n[4]
    # (iii) probability block with 3 vertices: 51 block_values adds only 2-vertex mixtures (edges of the simplex).
    # Candidates W_i = w_i (i = 1..3), D = q, E = 1 - q; MMR(w) = 1 - max_i w_i.
    def mmr_w(w):
        c = {"W1": lambda t: t[0][0], "W2": lambda t: t[0][1], "W3": lambda t: t[0][2],
             "D": lambda t: t[1], "E": lambda t: 1 - t[1]}
        return _w6_mmr_on(c, [(w, _W6Fr(0)), (w, _W6Fr(1))])[0]
    verts = [(_W6Fr(1), _W6Fr(0), _W6Fr(0)), (_W6Fr(0), _W6Fr(1), _W6Fr(0)), (_W6Fr(0), _W6Fr(0), _W6Fr(1))]
    cands_all = {"W1": lambda t: t[0][0], "W2": lambda t: t[0][1], "W3": lambda t: t[0][2],
                 "D": lambda t: t[1], "E": lambda t: 1 - t[1]}
    mmr_all = _w6_mmr_on(cands_all, [(w, q) for w in verts for q in (_W6Fr(0), _W6Fr(1))])[0]

    def edge_grid(n):
        pts = list(verts)
        for a, b in _w6_it.combinations(range(3), 2):
            for t in range(1, n):
                w = [_W6Fr(0)] * 3
                w[a], w[b] = 1 - _W6Fr(t, n), _W6Fr(t, n)
                pts.append(tuple(w))
        return pts
    edge_voi = {n: mmr_all - max(mmr_w(w) for w in edge_grid(n)) for n in (2, 3, 4, 6, 8, 12)}
    lattice = [(_W6Fr(i, 12), _W6Fr(j, 12), _W6Fr(12 - i - j, 12)) for i in range(13) for j in range(13 - i)]
    sup_lat = max(mmr_w(w) for w in lattice)
    true_simplex_voi = mmr_all - sup_lat
    ok = (nested_ok and upper_ok and non_nested_increase and voi_n[4] == _W6_H and voi_n[5] == _W6Fr(3, 5)
          and voi_n[9] == _W6Fr(5, 9) and mmr_all == 1 and sup_lat == _W6Fr(2, 3) and true_simplex_voi == _W6Fr(1, 3)
          and all(v >= _W6_H for v in edge_voi.values()))
    return {
        "id": "W6c", "title": "Grid refinement of VOI: nested grids monotone; non-nested and edge-only grids are not",
        "source_test": "51 block_values (scale: t/grid; prob: vertices + 2-vertex mixtures), t_sen7 vg9 check; 42 §13.5",
        "inputs": {"scale oracle": "T-SEN-7: F_A=1-v, F_B=v, F_D=q, F_E=1-q; grids t/n on [0,1]",
                   "prob oracle": "block w in simplex conv{e1,e2,e3} (3 vertices), block q in [0,1]; "
                                  "candidates W_i = w_i, D = q, E = 1 - q"},
        "rankings": {"grid VOI_v by n": {str(n): _w6_s(v) for n, v in sorted(voi_n.items())}},
        "choices": {"nested chain": nested_chain, "non-nested pair": [4, 5]},
        "outputs": {"exact VOI_v": _w6_s(true_v), "nested chain monotone non-increasing": nested_ok,
                    "all grids >= exact": upper_ok, "grid4 -> grid5": [_w6_s(voi_n[4]), _w6_s(voi_n[5])],
                    "prob block MMR(Theta)": _w6_s(mmr_all), "prob block edge-grid VOI_w by n":
                    {str(n): _w6_s(v) for n, v in sorted(edge_voi.items())},
                    "sup MMR(w) on simplex (lattice 1/12, contains barycentre)": _w6_s(sup_lat),
                    "exact VOI_w": _w6_s(true_simplex_voi)},
        "expected": {"nested": "1 >= 1/2 >= 1/2 >= 1/2 >= 1/2", "grid4 -> grid5": "1/2 -> 3/5 (bound worsens)",
                     "edge-grid VOI_w": ">= 1/2 for every n (does not converge)", "exact VOI_w": "1/3 (barycentre)"},
        "pass": ok,
        "minimality": ("Scale case uses the 2-block T-SEN-7 oracle (2 blocks needed, see W6). Non-nestedness needs only grids "
                       "n=4 (contains 1/2) and n=5 (does not). Edge-only non-convergence needs a probability block with >= 3 "
                       "vertices (a 2-vertex block is a segment, fully covered by its edge grid)."),
    }


# ----------------------------------------------------------------------------- W6d
def witness_W6d() -> dict:
    one = _W6Fr(1)
    # pointwise-feasible benchmark F#(theta) = max over portfolios feasible AT theta (Theta-independent)
    port = {"A": (lambda t: _W6Fr(0), lambda t: one), "B": (lambda t: t[0], lambda t: _W6_H - t[0])}
    box = [(_W6Fr(0), one)]

    def regret_sharp(d, th):
        feas = [vf(th) for vf, sf in port.values() if sf(th) >= 0]
        return max(feas) - port[d][0](th)
    vert = max(regret_sharp("A", th) for th in _w6_vertices(box))
    dense = max(regret_sharp("A", (x,)) for x in _w6_grid(_W6Fr(0), one, 8))
    # monotonicity under the sharp benchmark on W6b's instance
    p2 = {"A": (lambda t: t[0], lambda t: one), "B": (lambda t: 1 - t[0], lambda t: _W6_H - t[1])}

    def mmr_sharp(bx, pts):
        C = _w6_robust_cands(p2, bx)
        best = lambda th: max(vf(th) for vf, sf in p2.values() if sf(th) >= 0)
        return min(max(best(th) - C[d](th) for th in pts) for d in C)
    g = lambda bx: [tuple(x) for x in _w6_it.product(*[_w6_grid(lo, hi, 8) for lo, hi in bx])]
    b0 = [(_W6Fr(0), one), (_W6Fr(0), one)]
    b1 = [(_W6Fr(0), one), (_W6Fr(0), _W6_H)]
    s0, s1 = mmr_sharp(b0, g(b0)), mmr_sharp(b1, g(b1))
    ok = vert == 0 and dense == _W6_H and s0 == 1 and s1 == 1 and s1 <= s0
    return {
        "id": "W6d", "title": "Theta-independent (pointwise-feasible) regret benchmark: monotone but not vertex-exact",
        "source_test": "42 §13.2 MaxRegret vertex exactness 'for a fixed candidate set'; 51 regret_table ScopeError guard",
        "inputs": {"block": "q in [0,1]", "portfolios": "A: F = 0, always feasible; B: F = q, slack 1/2 - q",
                   "benchmark": "F#(q) = max over portfolios feasible at q"},
        "rankings": {"F#": "q on [0,1/2], 0 on (1/2,1]"},
        "choices": {"decision": "A (only robustly feasible portfolio)"},
        "outputs": {"MaxRegret#(A) at vertices": _w6_s(vert), "MaxRegret#(A) on 9-point grid": _w6_s(dense),
                    "W6b instance MMR# Theta^(0) -> Theta^(1) (9x9 grid evaluation)": [_w6_s(s0), _w6_s(s1)]},
        "expected": {"vertex": "0", "true (q = 1/2)": "1/2", "W6b instance": "1 -> 1 (non-increasing)"},
        "pass": ok,
        "minimality": "One block, two portfolios; the benchmark jump at q = 1/2 is the minimal non-multilinearity.",
    }


# ----------------------------------------------------------------------------- W6e
def witness_W6e() -> dict:
    box = [(_W6Fr(0), _W6Fr(1)), (_W6Fr(0), _W6Fr(1))]
    g = lambda t: (2 * t[0] - 1) * (2 * t[1] - 1)
    F = {"X": lambda t: g(t), "Y": lambda t: _W6Fr(0)}                 # X - Y bilinear, sign pattern XOR
    mmr_all = _w6_mmr_box(F, box)
    voi_v = mmr_all - _w6_exact_sup_1d(F, box, 0)[0]
    voi_q = mmr_all - _w6_exact_sup_1d(F, box, 1)[0]
    voi_v_vert = _w6_voi(F, box, 0, [_W6Fr(0), _W6Fr(1)])[0]
    joint = max(_w6_mmr_box(F, [(a, a), (b, b)]) for a in _w6_grid(_W6Fr(0), _W6Fr(1), 4) for b in _w6_grid(_W6Fr(0), _W6Fr(1), 4))
    realised = {str(v): _w6_s(_w6_mmr_box(F, _w6_fix(box, 0, v))) for v in _w6_grid(_W6Fr(0), _W6Fr(1), 4)}
    ok = mmr_all == 1 and voi_v == 0 and voi_q == 0 and voi_v_vert == 0 and joint == 0
    return {
        "id": "W6e", "title": "Myopic VOI complementarity: every single-block VOI is 0, joint identification removes all regret",
        "source_test": "42 §13.5 VOI_p (one block at a time); no 51 test (new)",
        "inputs": {"blocks": "v, q in [0,1]", "candidates": "X: F = (2v-1)(2q-1); Y: F = 0"},
        "rankings": {"MMR(Theta | v)": "|2v - 1| (maximal 1 at the vertices)"},
        "choices": {"greedy argmax VOI": "tie at 0; stopping rule D (any cost > 0) stops with MMR = 1"},
        "outputs": {"MMR(Theta)": _w6_s(mmr_all), "VOI_v exact": _w6_s(voi_v), "VOI_q exact": _w6_s(voi_q),
                    "VOI_v vertex": _w6_s(voi_v_vert), "max MMR after identifying both (grid of points)": _w6_s(joint),
                    "realised MMR after observing v": realised},
        "expected": {"MMR(Theta)": "1", "VOI_v = VOI_q": "0", "joint": "0"},
        "pass": ok,
        "minimality": "2 candidates and 2 blocks (one block: identification is complete, VOI = MMR(Theta)).",
    }


# ----------------------------------------------------------------------------- W6f
def witness_W6f() -> dict:
    F = {"A": lambda t: 1 - t[0], "B": lambda t: t[0], "D": lambda t: t[1], "E": lambda t: 1 - t[1]}
    q0 = _W6_H
    rows = []
    for t in range(1, 9):
        e = _W6Fr(1, 2 ** (t + 2))
        bx = [(_W6Fr(1, 4) - e, _W6Fr(3, 4) + e), (q0, q0)]           # strictly shrinking, limit [1/4, 3/4]
        m_t, args_t, _ = _w6_mmr_on(F, _w6_vertices(bx))
        rows.append((t, _w6_s(bx[0][0]), _w6_s(bx[0][1]), _w6_s(m_t), args_t))
    lim = _w6_mmr_box(F, [(_W6Fr(1, 4), _W6Fr(3, 4)), (q0, q0)])
    ok = (lim == _W6Fr(1, 4) and all(_W6Fr(r[3]) == _W6Fr(1, 4) + _W6Fr(1, 2 ** (r[0] + 2)) for r in rows)
          and all(r[4] == ["D", "E"] for r in rows))
    return {
        "id": "W6f", "title": "No termination guarantee without discretised evidence (strictly nested boxes, MMR >= 1/4)",
        "source_test": "42 §16 (D2) Theta_{t+1} subset Theta_t (dynamic extension); no 51 test (new)",
        "inputs": {"candidates": "T-SEN-7 oracle", "q": "identified at 1/2",
                   "v-boxes": "[1/4 - 2^-(t+2), 3/4 + 2^-(t+2)], t = 1, 2, ... (strictly decreasing)"},
        "rankings": {}, "choices": {"eps_R": "any eps_R < 1/4"},
        "outputs": {"(t, L, U, MMR_t, argmin set M_t)": rows, "limit MMR": _w6_s(lim)},
        "expected": {"MMR_t": "1/4 + 2^-(t+2) > 1/4 for all t; rule A never fires for eps_R < 1/4",
                     "M_t": "{D, E} for every t: rule C (weak / element stability) fires although MMR_t > 1/4"},
        "pass": ok,
        "minimality": "Single unresolved block; any non-degenerate limit box with positive MMR suffices.",
    }


if __name__ == "__main__":
    import json
    for fn in (witness_W6, witness_W6b, witness_W6c, witness_W6d, witness_W6e, witness_W6f):
        r = fn()
        print(r["id"], "PASS" if r["pass"] else "FAIL", json.dumps(r["outputs"], default=str)[:400])
