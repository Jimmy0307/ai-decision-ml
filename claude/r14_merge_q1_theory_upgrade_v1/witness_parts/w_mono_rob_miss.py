"""Witness parts (theory agent T2): W5, W5b, W7, W8a, W8b, W8c.

Pure stdlib, deterministic, SIMULATED_ONLY algebraic instances. No import from 51: every function
re-implements the minimal v2.2 logic it needs directly from the definitions in 42 v2.2:
  * Model C follower response: affordable plans a(x) <= e_u (R1'), argmax of OBJ-U, tie set with
    optimistic / pessimistic enterprise selection (42 §12.3); envelopes restricted to E'_u = {a(x)} (Lemma E', §12.4);
    leader picks the envelope profile by enumeration under the pooled budget (§12.5).
  * Model B: enumeration of plan profiles under the pooled budget, OBJ-E (§12.6).
  * Source-indexed reuse cost (§10): only S-cells move with delta.
Leader-tie convention: 'strict' = build only if G_1 - F_c > G_0 (51's enumeration order: y = {} first, replaced only if
strictly better); 'tie_build' = build if G_1 - F_c >= G_0. Both are reported.

Docs: Q/04_Q1_SHARED_CAPABILITY_NONMONOTONICITY.md (W5, W5b), Q/06_Q1_ROBUSTNESS_SCOPE.md (W7),
      Q/07_Q1_MISSINGNESS_PARTIAL_IDENTIFICATION.md (W8a-c).
"""
import itertools

_W5_TOL = 1e-9


# ----------------------------------------------------------------------------------------------------
# shared mini-solver for one shared capability c (all non-status-quo options require c; no local version)
# option = dict(k, W, V, base, w): follower gross W, enterprise gross V (TWD/period, before C^impl),
# S-cell implementation cost C^impl(S; delta) = max(0, base - w * delta) (also its pooled budget use a^BUD, D9 with
# zero opex difference); status quo k = 0 has W = V = cost = 0.
# ----------------------------------------------------------------------------------------------------
def _w5_cost(o, delta):
    return max(0.0, o["base"] - o["w"] * delta)


def _w5_plans(unit, delta):
    plans = [dict(k=0, fU=0.0, fE=0.0, a=0.0)]
    for o in unit["options"]:
        c = _w5_cost(o, delta)
        plans.append(dict(k=o["k"], fU=o["W"] - c, fE=o["V"] - c, a=c))
    return plans


def _w5_response(plans, e):
    aff = [p for p in plans if p["a"] <= e + _W5_TOL]
    m = max(p["fU"] for p in aff)
    tied = [p for p in aff if p["fU"] >= m - _W5_TOL]
    opt = max(tied, key=lambda p: p["fE"])
    pess = min(tied, key=lambda p: p["fE"])
    return dict(opt=opt, pess=pess, n_tied=len(tied))


def _w5_model_c_G1(units, delta, budget, mode):
    """Leader value with y_c = 1, EXCLUDING F_c (F_c is subtracted by the caller); envelopes E'_u = {a(x)}."""
    per_unit = []
    for u in units:
        plans = _w5_plans(u, delta)
        cands = []
        for e in sorted({p["a"] for p in plans}):
            r = _w5_response(plans, e)
            cands.append((e, r[mode], r["n_tied"]))
        per_unit.append(cands)
    best = None
    for combo in itertools.product(*per_unit):
        if sum(c[0] for c in combo) <= budget + _W5_TOL:
            v = sum(c[1]["fE"] for c in combo)
            if best is None or v > best[0] + _W5_TOL:
                best = (v, [(u["name"], c[0], c[1]["k"], c[2]) for u, c in zip(units, combo)])
    return best


def _w5_model_b_G1(units, delta, budget):
    best = None
    for combo in itertools.product(*[_w5_plans(u, delta) for u in units]):
        if sum(p["a"] for p in combo) <= budget + _W5_TOL:
            v = sum(p["fE"] for p in combo)
            if best is None or v > best[0] + _W5_TOL:
                best = (v, [(u["name"], p["k"]) for u, p in zip(units, combo)])
    return best


def _w5_build(D, convention):
    return (D > _W5_TOL) if convention == "strict" else (D >= -_W5_TOL)


def _w5_scan(units, Fc, Abar, grid):
    """Returns per-delta rows. G_0 = 0 (with y_c = 0 every non-status-quo option is infeasible by (F4))."""
    rows = []
    for d in grid:
        b = _w5_model_c_G1(units, d, Abar - Fc, "pess")
        o = _w5_model_c_G1(units, d, Abar - Fc, "opt")
        B = _w5_model_b_G1(units, d, Abar - Fc)
        rows.append(dict(delta=d, D_pess=round(b[0] - Fc, 9), D_opt=round(o[0] - Fc, 9), D_B=round(B[0] - Fc, 9),
                         choice_pess=b[1], choice_B=B[1],
                         build_pess_strict=_w5_build(b[0] - Fc, "strict"),
                         build_pess_tiebuild=_w5_build(b[0] - Fc, "tie_build"),
                         build_opt_strict=_w5_build(o[0] - Fc, "strict"),
                         build_B_strict=_w5_build(B[0] - Fc, "strict"),
                         max_follower_tie=max(t[3] for t in b[1])))
    return rows


def _w5_pattern_101(seq):
    """True iff the 0/1 sequence contains 1 ... 0 ... 1 (build -> no build -> build)."""
    s = "".join("1" if x else "0" for x in seq)
    i = s.find("1")
    if i < 0:
        return False
    j = s.find("0", i)
    return j >= 0 and s.find("1", j) >= 0


W5_TSEN8_UNITS = [
    dict(name="U1", options=[dict(k=1, W=30.0, V=30.0, base=5.0, w=1.0)]),    # aligned: N=10, v_u=3, l_x=0
    dict(name="U2", options=[dict(k=1, W=20.0, V=-5.0, base=3.0, w=1.0)]),    # misaligned: N=10, v_u=2, l_x=2.5
]
W5_MIN_UNITS = [
    dict(name="U", options=[dict(k=1, W=10.0, V=10.0, base=2.0, w=0.0),        # option a: enterprise-good, no reuse effect
                            dict(k=2, W=20.0, V=6.0, base=6.0, w=1.0)]),       # option b: follower-preferred, reuse lowers cost
]


def _w5_search_single_follower(n_options, weighted):
    """Bounded exhaustive search (support only, not a proof): single BU, single initiative, all options need c,
    integer data, delta grid 0..8 step 0.5. Returns the number of instances with a 1-0-1 pattern (strict convention)."""
    grid = [x / 2 for x in range(17)]
    Wv, Vv, bv, Fv = (2.0, 6.0, 10.0), (-4.0, 0.0, 4.0, 8.0), (0.0, 2.0, 4.0, 6.0), (1.0, 3.0, 5.0)
    wv = (0.0, 1.0) if weighted else (1.0,)
    found, n = 0, 0
    for F in Fv:
        for spec in itertools.product(*([Wv, Vv, bv, wv] * n_options)):
            opts = [dict(k=i + 1, W=spec[4 * i], V=spec[4 * i + 1], base=spec[4 * i + 2], w=spec[4 * i + 3])
                    for i in range(n_options)]
            units = [dict(name="U", options=opts)]
            seq = []
            for d in grid:
                g = _w5_model_c_G1(units, d, 100.0 - F, "pess")
                seq.append(g[0] - F > _W5_TOL)
            n += 1
            if _w5_pattern_101(seq):
                found += 1
    return dict(n_options=n_options, weighted_reuse=weighted, instances=n, found_101=found)


def witness_W5_delta() -> dict:
    grid = [0.0, 1.0, 2.0, 2.9, 3.0, 3.5, 4.0, 5.0]
    rows = _w5_scan(W5_TSEN8_UNITS, 24.0, 100.0, grid)
    seq_strict = ["1" if r["build_pess_strict"] else "0" for r in rows]
    seq_tie = ["1" if r["build_pess_tiebuild"] else "0" for r in rows]
    seq_opt = ["1" if r["build_opt_strict"] else "0" for r in rows]
    # switch points: just below 3 / at 3 (affordability with weak inequality), tie at 4
    edges = _w5_scan(W5_TSEN8_UNITS, 24.0, 100.0, [3.0 - 1e-6, 3.0, 4.0 - 1e-6, 4.0, 4.0 + 1e-6])
    # minimal single-follower instance (3 options, option-specific reuse path)
    grid_min = [0.0, 2.0, 3.9, 4.0, 5.0, 5.5, 6.0, 7.0]
    rows_min = _w5_scan(W5_MIN_UNITS, 5.0, 100.0, grid_min)
    seq_min = ["1" if r["build_pess_strict"] else "0" for r in rows_min]
    s2 = _w5_search_single_follower(1, weighted=True)      # Lemma M (proved) -> expect 0
    s3u = _w5_search_single_follower(2, weighted=False)    # uniform reuse, 3 options -> conjecture: 0
    s3w = _w5_search_single_follower(2, weighted=True)     # option-specific reuse -> >0 (W5-min family)
    expected = dict(seq_strict=list("11110001"), seq_tiebuild=list("11110011"),
                    D_pess=[1.0, 2.0, 3.0, 3.9, -1.0, -0.5, 0.0, 1.0], seq_min=list("11100111"))
    ok = (seq_strict == expected["seq_strict"] and seq_tie == expected["seq_tiebuild"] and seq_opt == seq_strict
          and [r["D_pess"] for r in rows] == expected["D_pess"]
          and all(r["max_follower_tie"] == 1 for r in rows + edges)
          and [e["build_pess_strict"] for e in edges] == [True, False, False, False, True]
          and [e["build_pess_tiebuild"] for e in edges] == [True, False, False, True, True]
          and seq_min == expected["seq_min"] and _w5_pattern_101([x == "1" for x in seq_min])
          and s2["found_101"] == 0 and s3u["found_101"] == 0 and s3w["found_101"] > 0)
    return dict(
        id="W5", title="Model C shared-capability build decision non-monotone in reuse delta (build -> no build -> build)",
        source_test="51 T-SEN-8 (same algebraic instance, independently re-implemented); 42 §15 P4 v2.2 counterexample",
        inputs=dict(
            capability="one shared c; F_c = 24; y_cur = {}; pooled BUD = 100 (ENG = 0 everywhere); no local version",
            U1="aligned; options {0, 1}; phi^u_1 = phi_1 = 30 - C1(delta); C1(delta) = max(0, 5 - delta) (S-cell); Pre(1) = {c}",
            U2="misaligned (l_x = 2.5/event); options {0, 1}; phi^u_1 = 20 - C2(delta); phi_1 = -5 - C2(delta); C2(delta) = max(0, 3 - delta)",
            envelopes="E'_u = {a(x)} = {0, C_u(delta)}; affordability a(x) <= e (weak)",
            delta_grid=grid,
            W5_min="single BU, options {0,a,b}: a: W=V=10, C_a=2 (no reuse effect); b: W=20, V=6, C_b=max(0, 6-delta); F_c=5; BUD=100",
        ),
        rankings=dict(U2_follower="k=1 strictly preferred for all delta (20 - C2 > 0)",
                      U1_follower="k=1 strictly preferred for all delta (30 - C1 > 0)",
                      U2_blockable="iff C2(delta) > 0 iff delta < 3"),
        choices=[dict(delta=r["delta"], pess=r["choice_pess"], B=r["choice_B"]) for r in rows],
        outputs=dict(D_pess=[r["D_pess"] for r in rows], D_opt=[r["D_opt"] for r in rows],
                     seq_pess_strict=seq_strict, seq_pess_tiebuild=seq_tie, seq_opt_strict=seq_opt,
                     edge_points=[(e["delta"], e["D_pess"], e["build_pess_strict"], e["build_pess_tiebuild"]) for e in edges],
                     build_region_strict="[0,3) U (4,inf)", build_region_tiebuild="[0,3) U [4,inf)",
                     W5_min_seq=seq_min, W5_min_D=[r["D_pess"] for r in rows_min],
                     W5_min_region_strict="[0,4) U (5,inf)",
                     search=[s2, s3u, s3w]),
        expected=expected,
        **{"pass": ok},
        minimality=("(i) T-SEN-8 analog: 1 capability, 2 BUs x 1 initiative x 2 options, 1 binding-free resource, no follower ties; "
                    "(ii) W5-min: 1 BU x 1 initiative x 3 options with an option-specific reuse path. Lemma M (doc 04 §4.2, proved): "
                    "a single follower with 2 options cannot produce 1-0-1 -- confirmed by bounded search (0 found). Bounded search "
                    "with 3 options and UNIFORM reuse found 0 (supports, does not prove, Conjecture M2: uniform reuse needs >= 2 "
                    "follower decision units); with option-specific reuse it found instances (W5-min family)."),
    )


# ----------------------------------------------------------------------------------------------------
# W5b: Model B monotone on the same instances + boundary test of the source-indexing assumption
# ----------------------------------------------------------------------------------------------------
def _w5b_availability_B(delta, indexing):
    """Two BUs; c shared (F_c = 5) or U1-local (F_loc = 1, U2 has no local permission); pooled BUD = 6.
    j1 (U1): V = 10, cost base 6; j2 (U2): V = 6.5, cost base 1.  indexing = 'source': S-cells move with delta,
    the L-cell of j1 stays at 6; 'availability': the cost moves with delta whenever c is available (shared or local)."""
    Fc, Floc, Abar = 5.0, 1.0, 6.0
    best = {0: None, 1: None}
    for yc in (0, 1):
        for yl in (0, 1):
            for q1 in (0, 1):
                for q2 in (0, 1):
                    avail1, avail2 = (yc or yl), yc
                    if (q1 and not avail1) or (q2 and not avail2):
                        continue
                    s1 = "L" if yl else ("S" if yc else None)
                    if indexing == "source":
                        c1 = max(0.0, 6.0 - delta) if s1 == "S" else 6.0
                    else:
                        c1 = max(0.0, 6.0 - delta)
                    c2 = max(0.0, 1.0 - delta)
                    use = Fc * yc + Floc * yl + q1 * c1 + q2 * c2
                    if use > Abar + _W5_TOL:
                        continue
                    val = q1 * (10.0 - c1) + q2 * (6.5 - c2) - Fc * yc - Floc * yl
                    if best[yc] is None or val > best[yc] + _W5_TOL:
                        best[yc] = val
    return best[1] - best[0]


def witness_W5b_delta() -> dict:
    grid = [0.0, 1.0, 2.0, 2.9, 3.0, 3.5, 4.0, 5.0]
    rowsB = _w5_scan(W5_TSEN8_UNITS, 24.0, 100.0, grid)
    DB = [r["D_B"] for r in rowsB]
    gm = [0.0, 2.0, 3.9, 4.0, 5.0, 5.5, 6.0, 7.0]
    DBm = [r["D_B"] for r in _w5_scan(W5_MIN_UNITS, 5.0, 100.0, gm)]
    nondecr = lambda xs: all(b >= a - 1e-9 for a, b in zip(xs, xs[1:]))
    g3 = [0.0, 1.0, 3.0, 5.0, 6.0]
    src = [_w5b_availability_B(d, "source") for d in g3]
    avl = [_w5b_availability_B(d, "availability") for d in g3]
    seq_src = ["1" if x > _W5_TOL else "0" for x in src]
    seq_avl = ["1" if x > _W5_TOL else "0" for x in avl]
    expected = dict(DB=[1.0, 2.0, 3.0, 3.9, 4.0, 4.5, 5.0, 6.0], DBm=[3.0] * 8,
                    src=[0.5, 1.5, 1.5, 10.5, 11.5], avl=[0.5, -2.5, -4.5, 2.5, 2.5],
                    seq_src=list("11111"), seq_avl=list("10011"))
    ok = (DB == expected["DB"] and nondecr(DB) and DBm == expected["DBm"] and nondecr(DBm)
          and [round(x, 9) for x in src] == expected["src"] and nondecr(src)
          and [round(x, 9) for x in avl] == expected["avl"] and seq_src == expected["seq_src"]
          and seq_avl == expected["seq_avl"])
    return dict(
        id="W5b", title="Model B monotone in delta on the W5 instances; source-indexing assumption is load-bearing",
        source_test="51 T-SEN-8 (B part: single 0->1 switch on 8 seeds); 42 §10 + D8 + §19 audit #3",
        inputs=dict(same_as="W5 (T-SEN-8 analog) and W5-min",
                    boundary_instance=("2 BUs; F_c=5; U1 may build local c (F_loc=1), U2 may not; pooled BUD=6 (binding); "
                                       "j1 (U1): V=10, cost base 6; j2 (U2): V=6.5, cost base 1; reuse path: cost = max(0, base - delta)"),
                    delta_grid_boundary=g3),
        rankings=dict(note="Model B: no follower; enterprise picks plans by OBJ-E"),
        choices=[dict(delta=r["delta"], B=r["choice_B"]) for r in rowsB],
        outputs=dict(D_B_TSEN8=DB, D_B_W5min=DBm, D_source=src, D_availability=avl,
                     seq_source=seq_src, seq_availability=seq_avl),
        expected=expected,
        **{"pass": ok},
        minimality=("Boundary instance uses 2 BUs x 1 initiative x 2 options and one local option; with source indexing "
                    "G_0 is constant (local L-cell fixed) and D is nondecreasing (budget binding does not matter); with "
                    "availability indexing delta also lowers the local-version cost, G_0 rises first and the B build "
                    "decision goes 1 -> 0 -> 1. Not claimed globally minimal."),
    )


# ----------------------------------------------------------------------------------------------------
# W7: robustness scope (element-level, Model C aligned, Model C misaligned)
# ----------------------------------------------------------------------------------------------------
def witness_W7() -> dict:
    grid = [t / 100 for t in range(101)]
    # (a) Model B, whole portfolios affine in one probability-mixture block theta in [0,1]
    port = {"y1_a": lambda th: th, "y1_b": lambda th: 1.0 - th, "y0": lambda th: 0.6}

    def optset(th):
        m = max(f(th) for f in port.values())
        return {d for d, f in port.items() if f(th) >= m - 1e-12}
    elem_ok = lambda pts: all(any(d.startswith("y1") for d in optset(t)) for t in pts)
    vertex_class = "ROBUST" if elem_ok([0.0, 1.0]) else "FRAGILE"
    grid_class = "ROBUST" if elem_ok(grid) else "FRAGILE"
    fail = [t for t in grid if not any(d.startswith("y1") for d in optset(t))]
    # positive control: Lemma R exactness for every whole-portfolio pair (affine gap => min at a vertex)
    lemma_r_exact = all(abs(min(port[a](t) - port[b](t) for t in grid) - min(port[a](t) - port[b](t) for t in (0.0, 1.0))) < 1e-12
                        for a in port for b in port)
    # MaxRegret exact at vertices (max of affine minus affine)
    mr = lambda d, pts: max(max(f(t) for f in port.values()) - port[d](t) for t in pts)
    maxregret_exact = all(abs(mr(d, grid) - mr(d, (0.0, 1.0))) < 1e-12 for d in port)
    # Lemma R sufficient condition (a): is any single y1 portfolio certified? (no -> sufficient condition silent)
    cert = {d: min(port[d](t) - max(f(t) for f in port.values()) for t in (0.0, 1.0)) >= -1e-12 for d in ("y1_a", "y1_b")}

    # (b) Model C, ALIGNED follower: build (F_c = 0.6) vs no build (0); follower options a, b need c, values theta, 1-theta
    def c_aligned(th):
        return max(th, 1.0 - th, 0.0) - 0.6
    cb_vertex = all(c_aligned(t) >= 0 for t in (0.0, 1.0))
    cb_fail = [t for t in grid if c_aligned(t) < -1e-12]

    # (c) Model C, MISALIGNED follower, all option costs 0 (no envelope can separate):
    #     follower u_a = 1 - theta, u_m = 0.6, u_b = theta; enterprise Psi_a = Psi_b = 1, Psi_m = 0; F_c = 0.5
    def c_mis(th, mode):
        u = {"a": 1.0 - th, "m": 0.6, "b": th, "0": 0.0}
        psi = {"a": 1.0, "m": 0.0, "b": 1.0, "0": 0.0}
        m = max(u.values())
        tied = [k for k in u if u[k] >= m - 1e-12]
        pick = max(tied, key=psi.get) if mode == "opt" else min(tied, key=psi.get)
        return psi[pick] - 0.5, pick
    cm_vertex = all(c_mis(t, "pess")[0] >= 0 for t in (0.0, 1.0))
    cm_fail = [t for t in grid if c_mis(t, "pess")[0] < 0]
    jumps = [(0.4, c_mis(0.4 - 1e-9, "pess")[0], c_mis(0.4 + 1e-9, "pess")[0]),
             (0.6, c_mis(0.6 - 1e-9, "pess")[0], c_mis(0.6 + 1e-9, "pess")[0])]
    ties = [(t, c_mis(t, "opt"), c_mis(t, "pess")) for t in (0.4, 0.6)]
    ok = (vertex_class == "ROBUST" and grid_class == "FRAGILE" and abs(fail[0] - 0.41) < 1e-12 and abs(fail[-1] - 0.59) < 1e-12
          and lemma_r_exact and maxregret_exact and not any(cert.values())
          and cb_vertex and cb_fail and abs(min(cb_fail) - 0.41) < 1e-12 and abs(max(cb_fail) - 0.59) < 1e-12
          and cm_vertex and cm_fail and jumps[0][1] == 0.5 and jumps[0][2] == -0.5 and jumps[1][1] == -0.5 and jumps[1][2] == 0.5
          and ties[0][1][0] == 0.5 and ties[0][2][0] == -0.5)
    return dict(
        id="W7", title="Element-level robustness counterexample (vertex-only ROBUST, interior FRAGILE) and Model C failure of vertex exactness",
        source_test="51 T-SEN-3 (element-level counterexample; ScopeError for Model C / element scope); 42 §13.3 items 1-2",
        inputs=dict(Theta="one block theta in [0,1] (two-vertex probability mixture; affine in every value)",
                    B_portfolios="F(y1_a)=theta, F(y1_b)=1-theta, F(y0)=0.6; element d = y_c, d0 = 1",
                    C_aligned="leader: build (F_c=0.6) or not (value 0); follower options a,b need c; u = Psi: a=theta, b=1-theta",
                    C_misaligned="leader: build (F_c=0.5) or not (0); options a,m,b need c, cost 0; u_a=1-theta, u_m=0.6, u_b=theta; Psi_a=Psi_b=1, Psi_m=0"),
        rankings=dict(B="y1_b best on [0,0.4), y0 best on (0.4,0.6), y1_a best on (0.6,1]",
                      C_misaligned="follower picks a on [0,0.4), m on (0.4,0.6), b on (0.6,1]; ties at 0.4 and 0.6"),
        choices=dict(C_misaligned_ties=ties),
        outputs=dict(B_element_vertex_class=vertex_class, B_element_grid_class=grid_class,
                     B_failure_interval_on_grid=(fail[0], fail[-1]), B_lemma_r_whole_portfolio_exact=lemma_r_exact,
                     B_maxregret_vertex_exact=maxregret_exact, B_single_portfolio_certificates=cert,
                     C_aligned_vertex_ok=cb_vertex, C_aligned_failure=(min(cb_fail), max(cb_fail)),
                     C_misaligned_vertex_ok=cm_vertex, C_misaligned_failure=(min(cm_fail), max(cm_fail)),
                     C_misaligned_jumps=jumps),
        expected=dict(B_element="vertex ROBUST, grid FRAGILE on (0.4,0.6)", whole_portfolio="exact at vertices",
                      C_aligned="build optimal at both vertices, not on (0.4,0.6)",
                      C_misaligned="build optimal at both vertices, leader value jumps 0.5 -> -0.5 -> 0.5"),
        **{"pass": ok},
        minimality=("Element level: >= 3 portfolios are necessary (with one portfolio containing d0 the element test IS the "
                    "whole-portfolio test, exact by Lemma R; with none lacking d0 it is trivial) and 1 scalar block suffices, so "
                    "the T-SEN-3 instance (3 portfolios, 1 block) is minimal in both counts. Model C misaligned: a follower with 3 "
                    "options is needed for a 1-0-1 pattern along one affine theta (two affine follower utilities cross once)."),
    )


# ----------------------------------------------------------------------------------------------------
# W8: missingness classes (Model B unless stated). Each instance: one initiative j, options {0, 1(, 2)}.
# ----------------------------------------------------------------------------------------------------
def witness_W8a() -> dict:
    """Feasibility-changing (and here also decision-changing): a^ENG_{j1} missing."""
    phi1, Aeng, Vp = 5.0, 10.0, (0.0, 30.0)
    feas = lambda v: [0] + ([1] if v <= Aeng + 1e-12 else [])
    best = lambda v: max(feas(v), key=lambda k: phi1 if k == 1 else 0.0)
    zero = dict(X=feas(0.0), decision=best(0.0), F=phi1, status="OK_POINT", disclosed=[])
    restricted = dict(X=[0], decision=0, F=0.0, status="RESTRICTED_SOLVE", excluded_configs=[("j", 1, "MissingStateLookup")],
                      element_q_j="UNIDENTIFIED")
    pts = [0.0, 5.0, 10.0, 10.5, 20.0, 30.0]
    ident = sorted({best(v) for v in pts})
    zero_infeasible_at = [v for v in pts if zero["decision"] not in feas(v)]
    lower_bound = all(restricted["F"] <= (phi1 if best(v) == 1 else 0.0) + 1e-12 for v in pts)
    # Model C: restricting the follower's option set can RAISE the leader value (P8 mechanism) -> not a lower bound
    def c_value(v, include_b=True):   # follower options: a (u=5, Psi=5), b (u=v missing, Psi=-3), all cost 0
        u = {"a": 5.0, "0": 0.0}
        psi = {"a": 5.0, "0": 0.0, "b": -3.0}
        if include_b:
            u["b"] = v
        m = max(u.values())
        return min(psi[k] for k in u if u[k] >= m - 1e-12)    # pessimistic
    FR_C = c_value(None, include_b=False)
    c_true = {v: c_value(v) for v in (0.0, 4.0, 5.0, 6.0, 10.0)}
    c_violations = [v for v, f in c_true.items() if FR_C > f + 1e-12]
    ok = (zero["decision"] == 1 and ident == [0, 1] and zero_infeasible_at == [10.5, 20.0, 30.0] and lower_bound
          and FR_C == 5.0 and c_violations == [5.0, 6.0, 10.0])
    return dict(
        id="W8a", title="Feasibility-changing missingness: zero-filled ENG use fabricates feasibility",
        source_test="51 T-MIS-6 site 'eng cell' (RESTRICTED_SOLVE, 'disclosed' bin on seed 5); 42 §13.4 rows 3-4; P8",
        inputs=dict(model="B", phi_j1=phi1, A_ENG=Aeng, missing="a^ENG_{j1}(S)", admissible_V_p=Vp, zero_fill=0.0,
                    model_C_part="follower options a (u=5, Psi=5), b (u=v MISSING in [0,10], Psi=-3), cost 0; pessimistic"),
        rankings=dict(B="phi_1 = 5 > phi_0 = 0 whenever k=1 is feasible"),
        choices=dict(zero_fill=zero, restricted=restricted),
        outputs=dict(identified_decision_set=ident, zero_fill_decision_infeasible_at=zero_infeasible_at,
                     restricted_value_is_lower_bound_B=lower_bound, model_C_restricted_value=FR_C,
                     model_C_true_values=c_true, model_C_lower_bound_violations=c_violations),
        expected=dict(identified=[0, 1], zero_fill="k=1, infeasible for v>10", C_restricted_not_lower_bound="violated for v>=5 (pess)"),
        **{"pass": ok},
        minimality="1 initiative, 2 options, 1 constraint; a 1-option instance has no decision. C part: 1 follower, 3 options.",
    )


def witness_W8b() -> dict:
    """Decision-changing via the objective ranking only (feasible set unchanged): lambda missing; plus the follower
    ledger split (Model C) and the status-quo outcome cell."""
    Fmt, dH, lamU = 10.0, 5.0, 4.0          # F_E^{-time}(k=1) = 10, DeltaHours = 5 h/period, lambda in [0, 4]
    F1 = lambda lam: Fmt - lam * dH
    dec = lambda lam: 1 if F1(lam) > 1e-12 else 0
    vertices = {0.0: dec(0.0), lamU: dec(lamU)}
    certified = len(set(vertices.values())) == 1
    lam_dagger = Fmt / dH
    # (ii) follower ledger split, Model C, W5 instance at delta = 3.5: U2 loss 2.5/event, s = l_x share in [0, 2.5]
    def c_build(s):
        d = 3.5
        W2 = 10.0 * (2.0 - (2.5 - s))      # follower gross: N (v_u - l_u)
        u2 = dict(name="U2", options=[dict(k=1, W=W2, V=-5.0, base=3.0, w=1.0)])
        g = _w5_model_c_G1([W5_TSEN8_UNITS[0], u2], d, 100.0 - 24.0, "pess")[0] - 24.0
        gB = _w5_model_b_G1([W5_TSEN8_UNITS[0], u2], d, 100.0 - 24.0)[0] - 24.0
        return g > _W5_TOL, gB > _W5_TOL
    split = {s: c_build(s) for s in (0.0, 0.4, 0.6, 2.5)}
    # (iii) status-quo outcome cell x (per-event value of k=0, N=1): phi_1 - phi_0 = (5 - 1) - x
    sq = {x: (1 if (5.0 - x - 1.0) > 1e-12 else 0) for x in (0.0, 3.0, 5.0)}
    ok = (vertices == {0.0: 1, 4.0: 0} and not certified and lam_dagger == 2.0
          and split == {0.0: (True, True), 0.4: (True, True), 0.6: (False, True), 2.5: (False, True)}
          and sq == {0.0: 1, 3.0: 1, 5.0: 0})
    return dict(
        id="W8b", title="Decision-changing missingness through the objective ranking (lambda; ledger split in C; status-quo cell)",
        source_test="51 T-MIS-6 sites 'lambda' (PARTIAL_OBJECTIVE), 'impl_x/tau (ledger)' (FOLLOWER_LEDGER_UNIDENTIFIED in C), "
                    "'outcome cell (status quo)' (UNEVALUABLE_INITIATIVE); 42 §7.4 (iii), §13.4",
        inputs=dict(lambda_case=dict(F_minus_time_k1=Fmt, delta_hours_k1=dH, lambda_box=(0.0, lamU), zero_fill=0.0),
                    ledger_case="W5 instance at delta=3.5; enterprise loss of U2 fixed at l = 2.5/event; ledger split "
                                "s = l_x in [0, 2.5] MISSING (l_u = 2.5 - s); follower gross = 10(2 - l_u)",
                    status_quo_case="phi_1 - phi_0 = N(g_1 - g_0) - C^impl = (5 - x) - 1, x = per-event status-quo value MISSING"),
        rankings=dict(lambda_case="k=1 iff lambda < 2 (tie at 2)", ledger_case="U2 picks k=1 iff 10(s - 0.5) > 0 iff s > 0.5",
                      status_quo_case="k=1 iff x < 4"),
        choices=dict(lambda_vertices=vertices, ledger_split_C_and_B=split, status_quo=sq),
        outputs=dict(zero_fill_lambda="k=1, F_E=10, OK_POINT (no disclosure)", honest_lambda="PARTIAL_OBJECTIVE, FRAGILE, no point decision",
                     lambda_dagger=lam_dagger, certified=certified,
                     ledger="C build decision changes with the unidentified split; B unaffected",
                     status_quo="decision changes with the status-quo cell"),
        expected=dict(lambda_vertices={0.0: 1, 4.0: 0}, ledger_switch="between s=0.4 and s=0.6", status_quo_switch="x=4"),
        **{"pass": ok},
        minimality="1 initiative x 2 options x 1 missing scalar (lambda); ledger part reuses the 2-BU W5 instance.",
    )


def witness_W8c() -> dict:
    """Decision-invariant but epistemically relevant: lambda missing with the decision certified on the whole box;
    Allow missing for a dominated option (feasibility channel)."""
    Fmt, dH, lamU = 10.0, 1.0, 4.0
    F1 = lambda lam: Fmt - lam * dH
    vertices = {lam: (1 if F1(lam) > 0 else 0) for lam in (0.0, lamU)}
    grid = [lamU * t / 40 for t in range(41)]
    invariant_grid = all((1 if F1(l) > 0 else 0) == 1 for l in grid)
    value_interval = (min(F1(0.0), F1(lamU)), max(F1(0.0), F1(lamU)))
    zero_fill = dict(decision=1, F_E=F1(0.0), status="OK_POINT", disclosed=[])
    honest = dict(decision=1, decision_valid_for_all_lambda_in_box=True, F_E_minus_time=Fmt, delta_hours=dH,
                  status="PARTIAL_OBJECTIVE", value_identified_set=value_interval)
    # Allow(j,2) missing; option 2 value phi_2 in [0, 3] if allowed, option 1 value 5 -> option 2 never optimal
    allow_dec = {(a, p2): max([0, 1] + ([2] if a else []), key=lambda k: {0: 0.0, 1: 5.0, 2: p2}[k])
                 for a in (0, 1) for p2 in (0.0, 3.0)}
    ok = (vertices == {0.0: 1, 4.0: 1} and invariant_grid and value_interval == (6.0, 10.0)
          and set(allow_dec.values()) == {1})
    return dict(
        id="W8c", title="Decision-invariant but epistemically relevant missingness (zero-fill overstates identification)",
        source_test="51 T-MIS-4 narrow-box case (certified PARTIAL_OBJECTIVE) and T-MIS-6 'disclosed' bin (site 'Allow'); 42 §7.4 (iii), §13.4 (c)",
        inputs=dict(lambda_case=dict(F_minus_time_k1=Fmt, delta_hours_k1=dH, lambda_box=(0.0, lamU)),
                    allow_case="options {0,1,2}: phi_1=5; Allow(j,2) MISSING in {0,1}; phi_2 in [0,3] if allowed"),
        rankings=dict(lambda_case="F(1;lambda) = 10 - lambda in [6,10] > 0 = F(0)", allow_case="phi_1 > phi_2 for every admissible value"),
        choices=dict(zero_fill=zero_fill, honest=honest, allow_decisions=allow_dec),
        outputs=dict(decision_invariant=invariant_grid, value_identified_set=value_interval,
                     zero_fill_reports_point_value=zero_fill["F_E"]),
        expected=dict(decision=1, value_interval=(6.0, 10.0), zero_fill="claims F_E = 10 as identified"),
        **{"pass": ok},
        minimality="1 initiative x 2 options x 1 missing scalar; Allow part 1 initiative x 3 options x 1 missing binary.",
    )


# NOTE for the integrator: ids "W5"/"W5b" were assigned to T2 by the caller; w_dl_gov.py (T1) also defines a
# witness_W5 (id "W5"). Function names here are suffixed (_delta) to avoid a name clash; ids may need renaming.
ALL_T2 = [witness_W5_delta, witness_W5b_delta, witness_W7, witness_W8a, witness_W8b, witness_W8c]

if __name__ == "__main__":
    for f in ALL_T2:
        r = f()
        print(("PASS" if r["pass"] else "FAIL"), r["id"], "-", r["title"])
