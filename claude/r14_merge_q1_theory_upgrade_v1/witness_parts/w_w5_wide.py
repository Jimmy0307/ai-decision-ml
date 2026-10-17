# ====================================================================================================
# PART T7 -- W5_WIDE: wide-margin supplement to W5 (red-team response agent T7; instance from red team T6, Q/11 A6)
# Self-contained (helpers prefixed _w5w_); pure stdlib; uses only a PRIVATE random.Random(fixed seed) instance,
# never the module-level random state, so the result is deterministic and independent of call order.
# ====================================================================================================
import itertools as _w5w_itertools
import random as _w5w_random

_W5W_TOL = 1e-9
_W5W_SEED = 20261015
_W5W_KEYS = ("N1", "v1", "b1", "N2", "v2", "lx", "b2", "Fc")
W5W_CANONICAL = dict(N1=10.0, v1=3.0, b1=5.0, N2=10.0, v2=2.0, lx=2.5, b2=3.0, Fc=24.0)   # = W5 / T-SEN-8 analog
W5W_WIDE = dict(N1=10.0, v1=3.0, b1=10.0, N2=10.0, v2=2.0, lx=3.0, b2=4.0, Fc=17.0)       # red team T6 wide margin
_W5W_ABAR = 100.0


def _w5w_unit(N, vu, lx, base, delta, floor=0.0, eng=0.0, opex=0.0):
    """Status quo k0 (a = (0,0), F_u = phi = 0) and one AI config k1 needing c. Reused S-cell cost
    C(delta) = max(floor, base - delta); a(k1) = (C + opex, eng) over (BUD, ENG); F_u = N v_u - C; phi = N (v_u - l_x) - C."""
    C = max(floor, base - delta)
    return [dict(k=0, a=(0.0, 0.0), fU=0.0, fE=0.0),
            dict(k=1, a=(C + opex, eng), fU=N * vu - C, fE=N * (vu - lx) - C)]


def _w5w_response(plans, e, mode):
    aff = [p for p in plans if p["a"][0] <= e[0] + _W5W_TOL and p["a"][1] <= e[1] + _W5W_TOL]
    m = max(p["fU"] for p in aff)
    tied = [p["fE"] for p in aff if p["fU"] >= m - _W5W_TOL]           # exact ties on this data
    return max(tied) if mode == "opt" else min(tied)


def _w5w_units(par, delta, floor=0.0, eng=0.0, opex=0.0):
    return [_w5w_unit(par["N1"], par["v1"], 0.0, par["b1"], delta),
            _w5w_unit(par["N2"], par["v2"], par["lx"], par["b2"], delta, floor, eng, opex)]


def _w5w_D(par, delta, mode="pess", floor=0.0, eng=0.0, opex=0.0):
    """D(delta) = V_1 - V_0 in Model C (Lemma E' envelopes E'_u = {a(x)}), V_0 = 0 (y_c = 0: only k0 feasible)."""
    us = _w5w_units(par, delta, floor, eng, opex)
    budget = (_W5W_ABAR - par["Fc"], _W5W_ABAR)
    best = None
    for es in _w5w_itertools.product(*[[p["a"] for p in ps] for ps in us]):
        if sum(e[0] for e in es) > budget[0] + _W5W_TOL or sum(e[1] for e in es) > budget[1] + _W5W_TOL:
            continue
        v = sum(_w5w_response(ps, e, mode) for ps, e in zip(us, es))
        best = v if best is None else max(best, v)
    return best - par["Fc"]


def _w5w_DB(par, delta):
    """Model B (centralized) build advantage on the same instance."""
    us = _w5w_units(par, delta)
    best = max(sum(p["fE"] for p in combo) for combo in _w5w_itertools.product(*us)
               if sum(p["a"][0] for p in combo) <= _W5W_ABAR - par["Fc"] + _W5W_TOL)
    return best - par["Fc"]


def _w5w_components(par, grid, mode="pess", floor=0.0, eng=0.0, opex=0.0):
    """Number of maximal runs of the strict build region {D > 0} on the grid (>= 2 <=> not an interval on the grid)."""
    b = [_w5w_D(par, d, mode, floor, eng, opex) > _W5W_TOL for d in grid]
    return sum(1 for i in range(len(b)) if b[i] and (i == 0 or not b[i - 1]))


def _w5w_robustness(par, radius, n_draws, stream, grid):
    """Deterministic joint multiplicative perturbation of all 8 scalars, each by an independent factor
    U[1 - radius, 1 + radius]; private RNG seeded with _W5W_SEED + stream. Returns survivors (non-interval kept)."""
    rng = _w5w_random.Random(_W5W_SEED + stream)
    kept = 0
    for _ in range(n_draws):
        p = {k: par[k] * rng.uniform(1.0 - radius, 1.0 + radius) for k in _W5W_KEYS}
        kept += _w5w_components(p, grid) >= 2
    return kept


def witness_W5_WIDE() -> dict:
    grid = [0.0, 2.0, 3.9, 4.0, 5.0, 6.0, 7.0, 7.5, 9.0, 10.0, 12.0]
    D_pess = [round(_w5w_D(W5W_WIDE, d, "pess"), 9) for d in grid]
    D_opt = [round(_w5w_D(W5W_WIDE, d, "opt"), 9) for d in grid]
    D_B = [round(_w5w_DB(W5W_WIDE, d), 9) for d in grid]
    seq_strict = ["1" if x > _W5W_TOL else "0" for x in D_pess]
    seq_tie = ["1" if x >= -_W5W_TOL else "0" for x in D_pess]
    # engine check: the same engine reproduces canonical W5 / T-SEN-8 exactly
    tsen8_grid = [0.0, 1.0, 2.0, 2.9, 3.0, 3.5, 4.0, 5.0]
    canon_D = [round(_w5w_D(W5W_CANONICAL, d, "pess"), 9) for d in tsen8_grid]
    canon_seq = ["1" if x > _W5W_TOL else "0" for x in canon_D]
    # robustness: fine grid on [0, 12] (step 0.05, 241 points); 400 draws per radius
    fine = [i / 20.0 for i in range(241)]
    nominal_components = dict(wide=_w5w_components(W5W_WIDE, fine), canonical=_w5w_components(W5W_CANONICAL, fine))
    n = 400
    rob = dict(
        wide_pm5pct=_w5w_robustness(W5W_WIDE, 0.05, n, 1, fine),
        wide_pm10pct=_w5w_robustness(W5W_WIDE, 0.10, n, 2, fine),
        canonical_pm1pct=_w5w_robustness(W5W_CANONICAL, 0.01, n, 3, fine),
        canonical_pm5pct=_w5w_robustness(W5W_CANONICAL, 0.05, n, 4, fine),
    )
    # structural knife-edge: the mechanism needs the misaligned unit's reused AI config to use <= the status
    # quo's pooled resources in EVERY pooled resource (exact zero cost floor AND exact zero ENG footprint)
    knife = {}
    for name, par in (("canonical", W5W_CANONICAL), ("wide", W5W_WIDE)):
        knife[name] = dict(
            base=_w5w_components(par, fine),
            eng_footprint_1e_6=_w5w_components(par, fine, eng=1e-6),
            cost_floor_0_01=_w5w_components(par, fine, floor=0.01),
            floor_0_5_plus_negative_opex_minus_1=_w5w_components(par, fine, floor=0.5, opex=-1.0),
        )
    expected = dict(
        D_pess=[3.0, 5.0, 6.9, -3.0, -2.0, -1.0, 0.0, 0.5, 2.0, 3.0, 3.0],
        D_B=[3.0, 5.0, 6.9, 7.0, 8.0, 9.0, 10.0, 10.5, 12.0, 13.0, 13.0],
        seq_strict=list("11100001111"), seq_tiebuild=list("11100011111"),
        canonical_D_TSEN8=[1.0, 2.0, 3.0, 3.9, -1.0, -0.5, 0.0, 1.0], canonical_seq_TSEN8=list("11110001"),
        nominal_components=dict(wide=2, canonical=2),
        knife_edge_components_eng_or_floor=1,
        robustness_survivors=dict(wide_pm5pct=367, wide_pm10pct=256, canonical_pm1pct=398, canonical_pm5pct=162),
    )
    ok = (D_pess == expected["D_pess"] and D_opt == D_pess and D_B == expected["D_B"]
          and all(b >= a - 1e-9 for a, b in zip(D_B, D_B[1:]))
          and seq_strict == expected["seq_strict"] and seq_tie == expected["seq_tiebuild"]
          and canon_D == expected["canonical_D_TSEN8"] and canon_seq == expected["canonical_seq_TSEN8"]
          and nominal_components == expected["nominal_components"]
          and all(knife[k]["eng_footprint_1e_6"] == 1 and knife[k]["cost_floor_0_01"] == 1 for k in knife)
          and rob == expected["robustness_survivors"]
          and rob["wide_pm5pct"] >= 0.8 * n and rob["wide_pm5pct"] > rob["canonical_pm5pct"])
    return dict(
        id="W5_WIDE",
        title="Wide-margin supplement to W5: Model C build region [0,4) U (7,inf) with margins 3 (perturbation-robust)",
        source_test="none in 51 (supplement to T-SEN-8 / W5; instance from red-team report Q/11 A6, t6/w5_wide.py)",
        inputs=dict(
            capability="one shared c; y_cur = {}; pooled (BUD, ENG) = (100, 100) minus F_c on BUD; no local version",
            U1="aligned: N1=10, v1=3, l_x=0; k1: F_u = phi = 30 - C1, C1(delta) = max(0, 10 - delta) (S-cell); a(k1) = (C1, 0)",
            U2="misaligned: N2=10, v2=2, l_x=3; k1: F_u = 20 - C2, phi = -10 - C2, C2(delta) = max(0, 4 - delta); a(k1) = (C2, 0)",
            F_c=17, status_quo="k0: a = (0,0), F_u = phi = 0 for both units",
            envelopes="E'_u = {a(x)}; weak affordability a(x) <= e; exact ties (none occur)",
            delta_grid=grid,
            robustness=("all 8 scalars (N1, v1, b1, N2, v2, l_x, b2, F_c) multiplied by independent U[1-r, 1+r] "
                        "factors; %d draws per radius; private random.Random(%d + stream); region scanned on "
                        "delta in {0, 0.05, ..., 12} (241 points); 'kept' = strict region has >= 2 components"
                        % (n, _W5W_SEED)),
        ),
        rankings=dict(U1_follower="k1 strictly preferred for all delta (30 - C1 > 0)",
                      U2_follower="k1 strictly preferred for all delta (20 - C2 > 0)",
                      U2_blockable="iff C2(delta) > 0 iff delta < 4 (envelope e_U2 = (0,0) then excludes k1)"),
        choices=dict(delta_lt_4="leader admits U1:k1, blocks U2 (e_U2 = 0): D = 30 - (10 - delta) - 17 = 3 + delta",
                     delta_4_to_10="U2:k1 unblockable (a = (0,0)): D = 30 - (10 - delta) - 10 - 17 = delta - 7",
                     delta_ge_10="D = 30 - 10 - 17 = 3"),
        outputs=dict(D_pess=D_pess, D_opt=D_opt, D_B=D_B, seq_pess_strict=seq_strict, seq_pess_tiebuild=seq_tie,
                     build_region_strict="[0,4) U (7,inf)", build_region_tiebuild="[0,4) U [7,inf)",
                     margins="D(0) = 3, D(4) = -3, D(>=10) = 3 (W5: 1, -1, 1)",
                     engine_check_canonical_W5_D=canon_D, engine_check_canonical_W5_seq=canon_seq,
                     nominal_components=nominal_components,
                     robustness_survivors=dict(rob, total_per_radius=n),
                     knife_edge_components=knife),
        expected=expected,
        **{"pass": ok},
        minimality=("Same structure as W5 (2 BUs x 1 initiative x 2 options, uniform clipped reuse, no follower ties); "
                    "only the scalars differ, so the numeric margins are 3 instead of 1. NOT more robust structurally: "
                    "like W5 it needs the misaligned unit's reused AI configuration to reach a pooled footprint <= the "
                    "status quo's in EVERY pooled resource (exact zero cost floor and exact zero ENG footprint); with "
                    "ENG footprint 1e-6 or cost floor 0.01 the region is an interval (knife_edge_components). "
                    "A fixed-seed perturbation count is a synthetic regression, not a proof of robustness."),
    )
