#!/usr/bin/env python3
"""q1_theory_witnesses.py -- Q1 THEORY UPGRADE: consolidated computational witnesses (integrator T5).

STANDALONE, deterministic, pure Python standard library. SIMULATED_ONLY.
Assembled from the four witness parts written by theory agents T1-T4
(witness_parts/w_dl_gov.py, w_mono_rob_miss.py, w_voi.py, w_mech.py); their code is copied in below
verbatim except for (i) removal of each part's __main__ block and ALL_* list and (ii) the rename of T1's
witness_W5 -> witness_W_DL_AL3 (id clash with T2's delta witness). Part T7 (W5_WIDE) was appended by the
red-team response agent T7 (2026-10-15). Nothing is imported from witness_parts
or from 51_enterprise_portfolio_solver_v2_2.py; every witness re-implements the minimal v2.2 logic it needs
from the definitions in 42_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md.

STATUS OF EVERY RESULT PRINTED HERE: computational witnesses / constructive examples on hand-built algebraic
instances. A witness establishes existence or refutes a universal claim; it is NOT a proof of a general
theorem (the proofs, where they exist, are in Q/01-08). No enterprise data, no human coder data, no V7 claim.

Randomness: only W5_WIDE (part T7, added after the red-team review Q/11) draws random numbers, from a
PRIVATE random.Random(20261015 + stream) instance (fixed seed; the module-level random state is not used).
All other witnesses are exhaustive over fixed finite grids. The module-level fixed seed below is declared for
the contract only. Hashed data are canonicalised (sorted keys, sorted set elements), so results do not
depend on PYTHONHASHSEED.
Tie handling: witness engines use absolute 1e-9 ties; 51 uses a relative tie rule (51 l.673). On the
integer/decimal data used here this makes no difference (Q/11 sec. 2.13 item 4).

Usage:  python q1_theory_witnesses.py            (full report + summary + verdict)
        python q1_theory_witnesses.py --hashes   (one line per witness: id sha256 PASS/FAIL)
"""
import hashlib as _q1_hashlib
import json as _q1_json
import os as _q1_os
import random as _q1_random
import sys as _q1_sys
from fractions import Fraction as _Q1Fr

Q1_FIXED_SEED = 20261014
_q1_random.seed(Q1_FIXED_SEED)

# ====================================================================================================
# PART T1 -- copied verbatim from witness_parts/w_dl_gov.py (main block and ALL_* list removed; witness_W5 renamed witness_W_DL_AL3)
# ====================================================================================================

_DOC_T1 = """w_dl_gov.py -- Q1 theory witnesses for Task B (delegation loss) and Task C (governance screening).

Pure stdlib, deterministic. Independent re-implementation from the 42 v2.2 *definitions*
(sec. 4.1 leader b=(y,gamma,e); sec. 8.1 X_u; sec. 11.1 DL = F_E^B - F_E^C; sec. 12.3 follower argmax and
opt/pess contribution bounds; sec. 12.4 Lemma E'; sec. 12.5 leader knapsack; sec. 12.6 Model B). Nothing is
imported from 51. Every number here is an algebraic, SIMULATED_ONLY witness -- not enterprise data, not V7.

A witness is a *constructive example*: it shows existence (or refutes a universal claim). It is never used as a
proof of a universal statement (see Q/02 and Q/03 for the proofs).

Contract: each `witness_<id>() -> dict` with keys
  id, title, source_test, inputs, rankings, choices, outputs, expected, pass, minimality.
Helpers are module-level and prefixed `_wdg_`.
"""
import itertools

_WDG_TOL = 1e-9


# ----------------------------------------------------------------------------------------------------------
# Generic finite bilevel engine (exact ties: epsilon_tie = 1e-9 absolute on integer-valued data)
# ----------------------------------------------------------------------------------------------------------
def _wdg_subsets(items):
    items = sorted(items)
    out = []
    for r in range(len(items) + 1):
        for comb in itertools.combinations(items, r):
            out.append(frozenset(comb))
    return out


def _wdg_le(a, b):
    return all(x <= y + _WDG_TOL for x, y in zip(a, b))


def _wdg_vadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def _wdg_vsub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def _wdg_zero(dim):
    return tuple(0.0 for _ in range(dim))


def _wdg_cap_use(inst, y):
    dim = len(inst["Abar"])
    use, cost = _wdg_zero(dim), 0.0
    for c in sorted(y):
        use = _wdg_vadd(use, inst["caps"][c]["a"])
        cost += inst["caps"][c]["F"]
    return use, cost


def _wdg_leader_budget(inst, y, g):
    """(R1') leader part: Abar - sum_c a_c y_c - 1[h=BUD] DeltaC_gov(gamma). BUD is coordinate 0."""
    use, fcost = _wdg_cap_use(inst, y)
    gov = inst["policies"][g]["cost"]
    rem = _wdg_vsub(inst["Abar"], use)
    rem = (rem[0] - gov,) + tuple(rem[1:])
    return rem, fcost, gov


def _wdg_plans(inst, u, y, g, model):
    """Plans of unit u under (y, gamma). Model 'C' drops plans violating unit-only constraints (AL3 channel)."""
    plans = inst["plans"](u, y, g)
    if model == "C":
        plans = [p for p in plans if p.get("unit_ok", True)]
    return plans


def _wdg_br(plans, e):
    """Follower best-response set X*_u(e) (42 sec. 12.3) and the opt/pess enterprise contribution bounds."""
    aff = [p for p in plans if _wdg_le(p["a"], e)]
    if not aff:
        return None
    m = max(p["FU"] for p in aff)
    tied = [p for p in aff if p["FU"] >= m - _WDG_TOL]
    return {"opt": max(p["FE"] for p in tied), "pess": min(p["FE"] for p in tied),
            "br": sorted(p["name"] for p in tied)}


def _wdg_solve_B(inst, gammas, ys=None):
    """Model B (centralized): enumerate (y, gamma, plan profile). Returns value and ALL optima."""
    units = inst["units"]
    best, optima = None, []
    for y in (ys if ys is not None else _wdg_subsets(inst["caps"])):
        for g in gammas:
            rem, fcost, gov = _wdg_leader_budget(inst, y, g)
            per_u = [_wdg_plans(inst, u, y, g, "B") for u in units]
            if any(not p for p in per_u):
                continue
            for prof in itertools.product(*per_u):
                tot = _wdg_zero(len(rem))
                for p in prof:
                    tot = _wdg_vadd(tot, p["a"])
                if not _wdg_le(tot, rem):
                    continue
                val = sum(p["FE"] for p in prof) - fcost - gov
                optima.append((val, y, g, prof))
                if best is None or val > best + _WDG_TOL:
                    best = val
    if best is None:
        return None
    top = [(y, g, prof) for v, y, g, prof in optima if v >= best - _WDG_TOL]
    return {"F": best, "optima": top}


def _wdg_envelopes(plans, kind):
    vecs = sorted({p["a"] for p in plans})
    if kind == "lemmaE":
        return vecs
    dim = len(vecs[0])
    coords = [sorted({v[i] for v in vecs}) for i in range(dim)]
    return [tuple(t) for t in itertools.product(*coords)]


def _wdg_solve_C(inst, gammas, ys=None, kind="lemmaE"):
    """Model C (bilevel): leader picks (y, gamma, e); follower best-responds; opt and pess leader values."""
    units = inst["units"]
    best = {"opt": None, "pess": None}
    for y in (ys if ys is not None else _wdg_subsets(inst["caps"])):
        for g in gammas:
            rem, fcost, gov = _wdg_leader_budget(inst, y, g)
            groups = []
            for u in units:
                plans = _wdg_plans(inst, u, y, g, "C")
                if not plans:
                    groups = None
                    break
                cands = []
                for e in _wdg_envelopes(plans, kind):
                    r = _wdg_br(plans, e)
                    if r is not None:
                        cands.append((e, r))
                groups.append(cands)
            if not groups:
                continue
            for mode in ("opt", "pess"):
                for combo in itertools.product(*groups):
                    tot = _wdg_zero(len(rem))
                    for e, _ in combo:
                        tot = _wdg_vadd(tot, e)
                    if not _wdg_le(tot, rem):
                        continue
                    val = sum(r[mode] for _, r in combo) - fcost - gov
                    if best[mode] is None or val > best[mode]["F"] + _WDG_TOL:
                        best[mode] = {"F": val, "y": sorted(y), "gamma": g,
                                      "envelopes": {u: e for u, (e, _) in zip(units, combo)},
                                      "best_responses": {u: r["br"] for u, (_, r) in zip(units, combo)}}
    return best


def _wdg_solve_A(inst, g):
    """Model A: y = empty, gamma fixed, envelope = status-quo B0_u; enterprise value of the unit choices."""
    lo = hi = -inst["policies"][g]["cost"]
    for u in inst["units"]:
        r = _wdg_br(_wdg_plans(inst, u, frozenset(), g, "C"), inst["B0"][u])
        lo += r["pess"]
        hi += r["opt"]
    return {"opt": hi, "pess": lo}


def _wdg_self_enforcing(inst, y, g, prof, mode):
    """Lemma DL-1 (first-best-relative characterization) predicate: every unit's first-best plan is (opt) a best response / (pess) a best response
    whose whole tie set is no worse for the enterprise, at envelope a(x*_u)."""
    for u, x in zip(inst["units"], prof):
        plans_c = _wdg_plans(inst, u, y, g, "C")
        if x["name"] not in {p["name"] for p in plans_c}:
            return False
        r = _wdg_br(plans_c, x["a"])
        if mode == "opt" and x["name"] not in r["br"]:
            return False
        if mode == "pess" and r["pess"] < x["FE"] - _WDG_TOL:
            return False
    return True


def _wdg_unblockable_deviations(inst, y, g, prof):
    """For a first-best profile: plans x^H with a(x^H) <= a(x*_u) and F_u(x^H) >= F_u(x*_u), x^H != x*_u."""
    out = {}
    for u, x in zip(inst["units"], prof):
        devs = []
        for p in _wdg_plans(inst, u, y, g, "C"):
            if p["name"] != x["name"] and _wdg_le(p["a"], x["a"]) and p["FU"] >= x["FU"] - _WDG_TOL:
                devs.append({"plan": p["name"], "dFU": p["FU"] - x["FU"], "dFE": p["FE"] - x["FE"],
                             "strict_pref": p["FU"] > x["FU"] + _WDG_TOL})
        out[u] = devs
    return out


def _wdg_analyse(inst, gammas, with_A=None):
    """Solve B, C (opt/pess), cross-check Lemma E' vs product envelopes, and check Lemma DL-1's (first-best-relative characterization) iff."""
    B = _wdg_solve_B(inst, gammas)
    C = _wdg_solve_C(inst, gammas, kind="lemmaE")
    Cp = _wdg_solve_C(inst, gammas, kind="product")
    lemma_ok = all(abs(C[m]["F"] - Cp[m]["F"]) <= 1e-7 for m in ("opt", "pess"))
    DL = {m: B["F"] - C[m]["F"] for m in ("opt", "pess")}
    pred = {}
    for m in ("opt", "pess"):
        se = any(_wdg_self_enforcing(inst, y, g, prof, m) for y, g, prof in B["optima"])
        pred[m] = not se                     # Lemma DL-1 (first-best-relative characterization): DL_m > 0  <=>  no first-best is m-self-enforcing
    iff_ok = all((DL[m] > 1e-7) == pred[m] for m in ("opt", "pess"))
    res = {"B": B["F"], "C_opt": C["opt"]["F"], "C_pess": C["pess"]["F"], "DL_opt": DL["opt"],
           "DL_pess": DL["pess"], "n_B_optima": len(B["optima"]),
           "B_optima": [{"y": sorted(y), "gamma": g, "plans": [p["name"] for p in prof],
                         "unblockable_deviations": _wdg_unblockable_deviations(inst, y, g, prof)}
                        for y, g, prof in B["optima"]],
           "C_choice": {m: C[m] for m in ("opt", "pess")},
           "lemmaE_equals_product_envelopes": lemma_ok,
           "theorem_DL1_prediction_DLpos": pred, "theorem_DL1_consistent": iff_ok}
    if with_A is not None:
        res["Aplus"] = _wdg_solve_B(inst, gammas, ys=[frozenset()])["F"]
        c0 = _wdg_solve_C(inst, gammas, ys=[frozenset()])
        res["C0_opt"], res["C0_pess"] = c0["opt"]["F"], c0["pess"]["F"]
        res["A"] = _wdg_solve_A(inst, with_A)
    return res


def _wdg_rankings(inst, y, g):
    out = {}
    for u in inst["units"]:
        ps = inst["plans"](u, y, g)
        out[u] = {"by_F_u": [(p["name"], p["FU"]) for p in sorted(ps, key=lambda p: (-p["FU"], p["name"]))],
                  "by_F_E": [(p["name"], p["FE"]) for p in sorted(ps, key=lambda p: (-p["FE"], p["name"]))],
                  "a(x)": {p["name"]: p["a"] for p in ps}}
    return out


# ----------------------------------------------------------------------------------------------------------
# Hand fixture re-derived from the 45/51 T-ORC-8 text (two BUs, one initiative each, one shared capability c)
#   phi_E(j,k) = N (v^u - l^x) - C_impl ;  phi^u(j,k) = N v^u - C_impl  (v^x=c=t=0, lambda=0, tau=0, C_impl,x=0)
#   a(j,k) = (a^BUD, a^ENG) = (C_impl, 0)   (no incremental opex, no engineering hours)
#   AI configs (A=1) need c (F4) and EA_k >= EA_req(gamma) (F5d); status quo k0 always feasible, phi=0, a=0.
# ----------------------------------------------------------------------------------------------------------
def _wdg_hand(units_cfg, F_c=10.0, ea_req=None, gov=None, Abar=(100.0, 100.0), B0=(50.0, 50.0)):
    ea_req = ea_req or {"g": 0}
    gov = gov or {g: 0.0 for g in ea_req}

    def plans(u, y, g):
        out = [{"name": u + ":k0", "a": (0.0, 0.0), "FU": 0.0, "FE": 0.0}]
        for k, cf in sorted(units_cfg[u].items()):
            if "c" not in y or cf["EA"] < ea_req[g]:
                continue
            N = cf.get("N", 10.0)
            out.append({"name": u + ":" + k, "a": (float(cf["impl"]), 0.0),
                        "FU": N * cf["v_u"] - cf["impl"], "FE": N * (cf["v_u"] - cf["l_x"]) - cf["impl"]})
        return out

    return {"units": sorted(units_cfg), "caps": {"c": {"F": F_c, "a": (F_c, 0.0)}},
            "policies": {g: {"cost": gov[g]} for g in ea_req}, "Abar": Abar,
            "B0": {u: B0 for u in units_cfg}, "plans": plans}


def _wdg_orc8(u2_impl, u2_lx, ea=(1, 1), ea_req=None):
    cfg = {"U1": {"k1": dict(v_u=3.0, l_x=0.0, impl=5.0, EA=ea[0])},
           "U2": {"k1": dict(v_u=2.0, l_x=u2_lx, impl=u2_impl, EA=ea[1])}}
    return cfg, _wdg_hand(cfg, ea_req=ea_req)


def _wdg_close(a, b):
    return abs(a - b) <= 1e-7


def _wdg_orc8_witness(wid, title, u2_impl, u2_lx, exp):
    cfg, inst = _wdg_orc8(u2_impl, u2_lx)
    r = _wdg_analyse(inst, ["g"], with_A="g")
    got = {"A_opt": r["A"]["opt"], "A_pess": r["A"]["pess"], "C0_opt": r["C0_opt"], "C0_pess": r["C0_pess"],
           "Aplus": r["Aplus"], "B": r["B"], "C_opt": r["C_opt"], "C_pess": r["C_pess"],
           "DL_opt": r["DL_opt"], "DL_pess": r["DL_pess"], "VSC": r["B"] - r["Aplus"],
           "NEV_opt": r["C_opt"] - r["A"]["opt"], "NEV_pess": r["C_pess"] - r["A"]["pess"]}
    ok = all(_wdg_close(got[k], v) for k, v in exp.items()) and r["lemmaE_equals_product_envelopes"] \
        and r["theorem_DL1_consistent"]
    return {"id": wid, "title": title,
            "source_test": "51 t_orc8_independent_hand / hand_instance(%s, %s) (read-only mapping)" % (u2_impl, u2_lx),
            "inputs": {"units_configs": cfg, "N": 10, "F_c": 10, "Abar(BUD,ENG)": (100, 100), "B0_u": (50, 50),
                       "Gamma": ["g (no EA requirement, DeltaC_gov=0)"],
                       "formulas": "phi_E=N(v_u-l_x)-impl; F_u=N v_u-impl; a=(impl,0); AI config needs y_c=1"},
            "rankings": _wdg_rankings(inst, frozenset({"c"}), "g"),
            "choices": {"B_optima": r["B_optima"], "C": r["C_choice"]},
            "outputs": dict(got, n_B_optima=r["n_B_optima"],
                            lemmaE_equals_product_envelopes=r["lemmaE_equals_product_envelopes"],
                            theorem_DL1_prediction_DLpos=r["theorem_DL1_prediction_DLpos"]),
            "expected": exp, "pass": ok}


# ----------------------------------------------------------------------------------------------------------
# Task B witnesses
# ----------------------------------------------------------------------------------------------------------
def witness_W1():
    d = _wdg_orc8_witness("W1", "Aligned ledgers: B = C = 30, DL = 0 (opt = pess)", 5.0, 0.0,
                          dict(A_opt=0, A_pess=0, C0_opt=0, C0_pess=0, Aplus=0, B=30, C_opt=30, C_pess=30,
                               DL_opt=0, DL_pess=0, VSC=30, NEV_opt=30, NEV_pess=30))
    d["minimality"] = ("Not minimal for 'DL=0' (any aligned instance has DL=0 by P2/Cor. DL-2). Kept with the "
                       "T-ORC-8 dimensions (2 BUs, 1 capability, |Gamma|=1) so that W1-W3 differ only in U2's "
                       "(impl, l_x).")
    return d


def witness_W2():
    d = _wdg_orc8_witness("W2", "Misaligned but envelope-blockable: B = C = 15, DL = 0", 5.0, 2.5,
                          dict(A_opt=0, A_pess=0, C0_opt=0, C0_pess=0, Aplus=0, B=15, C_opt=15, C_pess=15,
                               DL_opt=0, DL_pess=0, VSC=15, NEV_opt=15, NEV_pess=15))
    d["minimality"] = ("Refutes 'misalignment (even strict preference reversal) => DL>0'. Smallest form: 1 BU, "
                       "1 resource, plans x^G=(a=0,F_u=0,F_E=0), x^H=(a=1,F_u=1,F_E=-1): envelope e=0 blocks "
                       "x^H. The capability layer here is inherited from T-ORC-8 and is not needed.")
    return d


def witness_W3():
    d = _wdg_orc8_witness("W3", "Misaligned and envelope-unblockable: B = 15, C = 10, DL = 5", 0.0, 2.5,
                          dict(A_opt=0, A_pess=0, C0_opt=0, C0_pess=0, Aplus=0, B=15, C_opt=10, C_pess=10,
                               DL_opt=5, DL_pess=5, VSC=15, NEV_opt=10, NEV_pess=10))
    d["minimality"] = ("Unique first best (y_c=1, U1:k1, U2:k0); U2:k1 has a(x^H)=(0,0)<=a(x^G)=(0,0) and "
                       "F_u 20>0 while F_E -5<0 -> Cor. DL-2 gives DL>0. The second BU and the capability are "
                       "needed only for the T-ORC-8 'capability coupling' reading (blocking U2 via y_c=0 costs "
                       "U1's 25); the minimal single-BU DL>0 instance is W3m.")
    return d


def witness_W3m():
    plans = {"U": [{"name": "U:xG", "a": (1.0,), "FU": 0.0, "FE": 2.0},
                   {"name": "U:xH", "a": (0.0,), "FU": 1.0, "FE": 0.0}]}
    inst = {"units": ["U"], "caps": {}, "policies": {"g": {"cost": 0.0}}, "Abar": (1.0,),
            "plans": lambda u, y, g: plans[u]}
    r = _wdg_analyse(inst, ["g"])
    exp = dict(B=2.0, C_opt=0.0, C_pess=0.0, DL_opt=2.0, DL_pess=2.0)
    got = {k: r[k] for k in exp}
    return {"id": "W3m", "title": "Minimal DL>0: one BU, one resource, two plans (under-adoption)",
            "source_test": "none in 51 (new constructive example); reading of 42 P2 remark",
            "inputs": {"plans": plans, "Abar": 1, "Gamma": ["g"], "capabilities": "none",
                       "v2.2 reading": "x^G = AI config with external value v^x>0 the unit does not book (AL1 "
                                       "fails); x^H = status quo. Envelopes cap but never compel adoption."},
            "rankings": {"U": {"by_F_u": ["xH(1)", "xG(0)"], "by_F_E": ["xG(2)", "xH(0)"]}},
            "choices": {"B_optima": r["B_optima"], "C": r["C_choice"]},
            "outputs": dict(got, theorem_DL1_prediction_DLpos=r["theorem_DL1_prediction_DLpos"]),
            "expected": exp,
            "pass": all(_wdg_close(got[k], v) for k, v in exp.items()) and r["theorem_DL1_consistent"],
            "minimality": ("Minimal: with one plan the best response is unique and equals the first best; with "
                           "one BU, 0 capabilities, |Gamma|=1 and 1 resource every dimension is at its floor. "
                           "Shows that neither capability coupling nor cross-BU resource coupling is necessary "
                           "for DL>0.")}


def witness_W3b():
    plans = {"U": [{"name": "U:xG", "a": (0.0,), "FU": 0.0, "FE": 1.0},
                   {"name": "U:xH", "a": (0.0,), "FU": 0.0, "FE": 0.0}]}
    inst = {"units": ["U"], "caps": {}, "policies": {"g": {"cost": 0.0}}, "Abar": (0.0,),
            "plans": lambda u, y, g: plans[u]}
    r = _wdg_analyse(inst, ["g"])
    exp = dict(B=1.0, C_opt=1.0, C_pess=0.0, DL_opt=0.0, DL_pess=1.0)
    got = {k: r[k] for k in exp}
    return {"id": "W3b", "title": "DL_opt = 0 < DL_pess = 1 (follower tie, no strict reversal)",
            "source_test": "none in 51 directly; related: T-ORC-9 tie_instance (C_opt > C_pess)",
            "inputs": {"plans": plans, "Abar": 0, "Gamma": ["g"],
                       "v2.2 reading": "two configs with equal unit ledger value; x^G carries enterprise-only "
                                       "value (v^x or avoided l^x) -> AL1 fails only through a tie"},
            "rankings": {"U": {"by_F_u": ["xG(0) = xH(0)"], "by_F_E": ["xG(1)", "xH(0)"]}},
            "choices": {"B_optima": r["B_optima"], "C": r["C_choice"]},
            "outputs": dict(got, theorem_DL1_prediction_DLpos=r["theorem_DL1_prediction_DLpos"]),
            "expected": exp,
            "pass": all(_wdg_close(got[k], v) for k, v in exp.items()) and r["theorem_DL1_consistent"],
            "minimality": ("Minimal: a tie needs >=2 plans; 1 BU, 0 capabilities, |Gamma|=1, 1 resource. "
                           "Shows strict preference reversal is NOT necessary for DL_pess>0 (Lemma DL-1p, first-best-relative characterization).")}


def witness_W3c():
    """Pairwise (reversal + envelope non-separability) does not determine the sign of DL."""
    base = [{"name": "U:xG", "a": (1.0,), "FU": 0.0, "FE": 2.0},
            {"name": "U:xH", "a": (0.0,), "FU": 1.0, "FE": 0.0}]
    extra = base + [{"name": "U:xM", "a": (1.0,), "FU": 2.0, "FE": 2.0}]
    i1 = {"units": ["U"], "caps": {}, "policies": {"g": {"cost": 0.0}}, "Abar": (1.0,),
          "plans": lambda u, y, g: base}
    i2 = {"units": ["U"], "caps": {}, "policies": {"g": {"cost": 0.0}}, "Abar": (1.0,),
          "plans": lambda u, y, g: extra}
    r1, r2 = _wdg_analyse(i1, ["g"]), _wdg_analyse(i2, ["g"])
    got = {"I1_DL_opt": r1["DL_opt"], "I1_DL_pess": r1["DL_pess"], "I2_DL_opt": r2["DL_opt"],
           "I2_DL_pess": r2["DL_pess"], "I2_n_B_optima": r2["n_B_optima"]}
    exp = {"I1_DL_opt": 2.0, "I1_DL_pess": 2.0, "I2_DL_opt": 0.0, "I2_DL_pess": 0.0, "I2_n_B_optima": 2}
    return {"id": "W3c", "title": "Same reversing, envelope-non-separable pair (xH,xG); DL=2 vs DL=0",
            "source_test": "none in 51 (new constructive counterexample)",
            "inputs": {"I1": base, "I2": extra, "Abar": 1},
            "rankings": {"I2": {"by_F_u": ["xM(2)", "xH(1)", "xG(0)"], "by_F_E": ["xG(2)=xM(2)", "xH(0)"]}},
            "choices": {"I1": r1["C_choice"], "I2": r2["C_choice"]},
            "outputs": got, "expected": exp,
            "pass": all(_wdg_close(got[k], v) for k, v in exp.items()) and r1["theorem_DL1_consistent"]
            and r2["theorem_DL1_consistent"],
            "minimality": ("I2 adds one plan to W3m. Any pairwise primitive that holds for (xH,xG) holds in both "
                           "instances, yet DL differs: an iff for DL in pairwise primitives (A)-(F) alone is "
                           "impossible; the correct iff (Lemma DL-1, first-best-relative characterization) quantifies over all first-best solutions.")}


def witness_W_DL_AL3():
    """AL3 channel: identical ledgers, but a unit-only constraint (absent from B) excludes the first-best plan."""
    plans = [{"name": "U:xG", "a": (0.0,), "FU": 1.0, "FE": 1.0, "unit_ok": False},
             {"name": "U:x0", "a": (0.0,), "FU": 0.0, "FE": 0.0}]
    inst = {"units": ["U"], "caps": {}, "policies": {"g": {"cost": 0.0}}, "Abar": (0.0,),
            "plans": lambda u, y, g: plans}
    r = _wdg_analyse(inst, ["g"])
    exp = dict(B=1.0, C_opt=0.0, C_pess=0.0, DL_opt=1.0, DL_pess=1.0)
    got = {k: r[k] for k in exp}
    return {"id": "W5", "title": "DL>0 with F_u == F_E: unit-only constraint (AL3 fails, AL1/2/4 hold)",
            "source_test": "none in 51 (51 implements no unit-only constraints; 42 sec. 8.1-8.2 AL3)",
            "inputs": {"plans": plans, "note": "unit_ok=False: violates a unit-only constraint (e.g. s_min or "
                                                "e^u_j) that is not in the enterprise problem"},
            "rankings": {"U": {"by_F_u": ["xG(1)", "x0(0)"], "by_F_E": ["xG(1)", "x0(0)"]}},
            "choices": {"B_optima": r["B_optima"], "C": r["C_choice"]},
            "outputs": dict(got, theorem_DL1_prediction_DLpos=r["theorem_DL1_prediction_DLpos"]),
            "expected": exp,
            "pass": all(_wdg_close(got[k], v) for k, v in exp.items()) and r["theorem_DL1_consistent"],
            "minimality": "Minimal (1 BU, 2 plans). Ledger misalignment is not necessary once AL3 fails."}


# ----------------------------------------------------------------------------------------------------------
# Task C witnesses (governance screening). GSV = F_C*(strict) - F_C*(loose), same Allow, same DeltaC_gov.
# Identity checked in every witness: GSV_m = DL_m(loose) - DL_m(strict) - PR_B, PR_B = F_B(loose) - F_B(strict).
# ----------------------------------------------------------------------------------------------------------
def _wdg_gov(cfg, ea_req_strict):
    inst = _wdg_hand(cfg, ea_req={"loose": 0, "strict": ea_req_strict})
    lo, st = _wdg_analyse(inst, ["loose"]), _wdg_analyse(inst, ["strict"])
    both = _wdg_analyse(inst, ["loose", "strict"])
    out = {"B_loose": lo["B"], "B_strict": st["B"], "C_opt_loose": lo["C_opt"], "C_opt_strict": st["C_opt"],
           "C_pess_loose": lo["C_pess"], "C_pess_strict": st["C_pess"],
           "DL_opt_loose": lo["DL_opt"], "DL_opt_strict": st["DL_opt"],
           "DL_pess_loose": lo["DL_pess"], "DL_pess_strict": st["DL_pess"],
           "PR_B": lo["B"] - st["B"],
           "GSV_opt": st["C_opt"] - lo["C_opt"], "GSV_pess": st["C_pess"] - lo["C_pess"],
           "C_opt_leader_chooses_policy": both["C_opt"], "chosen_policy_opt": both["C_choice"]["opt"]["gamma"]}
    ident = all(_wdg_close(out["GSV_" + m], out["DL_%s_loose" % m] - out["DL_%s_strict" % m] - out["PR_B"])
                for m in ("opt", "pess"))
    sane = ident and all(r["lemmaE_equals_product_envelopes"] and r["theorem_DL1_consistent"]
                         for r in (lo, st, both)) and out["B_strict"] <= out["B_loose"] + 1e-7
    return inst, lo, st, out, sane


def _wdg_gov_witness(wid, title, cfg, ea_strict, exp, source, minimality, reading):
    inst, lo, st, out, sane = _wdg_gov(cfg, ea_strict)
    ok = sane and all(_wdg_close(out[k], v) for k, v in exp.items())
    return {"id": wid, "title": title, "source_test": source,
            "inputs": {"units_configs": cfg, "N": 10, "F_c": 10, "Abar": (100, 100),
                       "requirement": "EA_k >= EA_req for A>=1; loose EA_req=0, strict EA_req=%d" % ea_strict,
                       "DeltaC_gov": "0 in both (so Direct Governance Cost = 0, Net = Gross)",
                       "reading": reading},
            "rankings": {"loose": _wdg_rankings(inst, frozenset({"c"}), "loose"),
                         "strict": _wdg_rankings(inst, frozenset({"c"}), "strict")},
            "choices": {"loose_C": lo["C_choice"], "strict_C": st["C_choice"],
                        "loose_B_optima": lo["B_optima"], "strict_B_optima": st["B_optima"]},
            "outputs": dict(out, identity_GSV_eq_dDL_minus_PR=sane), "expected": exp, "pass": ok,
            "minimality": minimality}


def witness_W4():
    cfg = {"U1": {"k1": dict(v_u=3.0, l_x=0.0, impl=5.0, EA=2)},
           "U2": {"k1": dict(v_u=2.0, l_x=2.5, impl=0.0, EA=1)}}
    return _wdg_gov_witness(
        "W4", "P8 screening 10 -> 15 (GSV = DL_loose = 5, PR_B = 0)", cfg, 2,
        dict(B_loose=15, B_strict=15, C_opt_loose=10, C_opt_strict=15, C_pess_loose=10, C_pess_strict=15,
             GSV_opt=5, GSV_pess=5, PR_B=0, DL_opt_loose=5, DL_opt_strict=0, C_opt_leader_chooses_policy=15),
        "51 t_regression_v21: hand_instance(0.0, 2.5, ea_levels=(2,1), ea_req=2): C(g)=10, C(g_req)=15",
        ("Minimal algebraic core: 1 BU, plans xG=(a=0,F_u=0,F_E=1,EA=2), xH=(a=0,F_u=1,F_E=0,EA=1); "
         "strict EA>=2 removes xH: C 0 -> 1 = B. The second BU and capability c reproduce P8's 10->15 and "
         "show the requirement acts where the capability instrument (y_c=0) is too blunt."),
        "U2:k1 is the unblockable reversal of W3; strict EA removes exactly it and keeps U1:k1 (EA=2).")


def witness_W4b():
    cfg = {"U1": {"k1": dict(v_u=3.0, l_x=0.0, impl=5.0, EA=1), "k2": dict(v_u=2.5, l_x=0.0, impl=5.0, EA=2)},
           "U2": {"k1": dict(v_u=2.0, l_x=2.5, impl=5.0, EA=1)}}
    return _wdg_gov_witness(
        "W4b", "Opposite direction 15 -> 10: strict requirement excludes x^H AND the better x^G", cfg, 2,
        dict(B_loose=15, B_strict=10, C_opt_loose=15, C_opt_strict=10, C_pess_loose=15, C_pess_strict=10,
             GSV_opt=-5, GSV_pess=-5, PR_B=5, DL_opt_loose=0, DL_opt_strict=0, C_opt_leader_chooses_policy=15),
        "constructed variant of the REG/T-ORC-8 fixture (not in 51): U2 blockable (impl 5), U1 gets EA=2 "
        "alternative k2 worth 20",
        ("Minimal core: 1 BU, plans xG=(F_u=F_E=2,EA=1), xG'=(F_u=F_E=1,EA=2), x0; strict removes xG: "
         "C 2 -> 1. Two BUs kept to show the requirement also removes U2:k1 (the reversal) at no gain because "
         "the envelope already blocks it."),
        "Screening is worthless when the envelope already separates; the requirement only prices U1 out of k1.")


def witness_W4c():
    cfg = {"U1": {"k1": dict(v_u=3.0, l_x=0.0, impl=5.0, EA=1), "k2": dict(v_u=2.2, l_x=0.0, impl=5.0, EA=2)},
           "U2": {"k1": dict(v_u=2.0, l_x=2.5, impl=0.0, EA=1)}}
    return _wdg_gov_witness(
        "W4c", "Screening vs price of requirement: removes DL=5 but costs PR_B=8 (10 -> 7)", cfg, 2,
        dict(B_loose=15, B_strict=7, C_opt_loose=10, C_opt_strict=7, GSV_opt=-3, GSV_pess=-3, PR_B=8,
             DL_opt_loose=5, DL_opt_strict=0, C_opt_leader_chooses_policy=10),
        "constructed variant (not in 51)",
        "Two BUs needed: the screened reversal (U2) and the priced-out first-best config (U1) sit in different "
        "units, which is the policy-coupling channel (one gamma for all units).",
        "Reversal + envelope non-separability + requirement separating x^H are present, yet GSV < 0.")


def witness_W4d():
    cfg = {"U1": {"k1": dict(v_u=3.0, l_x=0.0, impl=5.0, EA=2)},
           "U2": {"k1": dict(v_u=2.0, l_x=2.5, impl=0.0, EA=1), "k2": dict(v_u=1.9, l_x=2.5, impl=0.0, EA=2)}}
    return _wdg_gov_witness(
        "W4d", "Pairwise screening insufficient: removing x^H lets a worse x^M become the best response",
        cfg, 2,
        dict(B_loose=15, B_strict=15, C_opt_loose=10, C_opt_strict=9, GSV_opt=-1, GSV_pess=-1, PR_B=0,
             DL_opt_loose=5, DL_opt_strict=6, C_opt_leader_chooses_policy=10),
        "constructed variant (not in 51)",
        "Minimal core: 1 BU, x0=(F_u 0,F_E 0), xH=(20,-5,EA1), xM=(19,-6,EA2), all a=0.",
        "Screening must remove every unblockable deviation, not a single reversing plan (Prop. GS-2).")


def witness_W4e():
    """Pessimistic-only screening from a tie: requirement removes the tied enterprise-worse plan."""
    plans_all = [{"name": "U:xG", "a": (0.0,), "FU": 0.0, "FE": 1.0, "EA": 2},
                 {"name": "U:xH", "a": (0.0,), "FU": 0.0, "FE": 0.0, "EA": 1}]
    req = {"loose": 0, "strict": 2}
    inst = {"units": ["U"], "caps": {}, "policies": {"loose": {"cost": 0.0}, "strict": {"cost": 0.0}},
            "Abar": (0.0,), "plans": lambda u, y, g: [p for p in plans_all if p["EA"] >= req[g]]}
    lo, st = _wdg_analyse(inst, ["loose"]), _wdg_analyse(inst, ["strict"])
    got = {"GSV_opt": st["C_opt"] - lo["C_opt"], "GSV_pess": st["C_pess"] - lo["C_pess"],
           "DL_opt_loose": lo["DL_opt"], "DL_pess_loose": lo["DL_pess"], "PR_B": lo["B"] - st["B"]}
    exp = {"GSV_opt": 0.0, "GSV_pess": 1.0, "DL_opt_loose": 0.0, "DL_pess_loose": 1.0, "PR_B": 0.0}
    return {"id": "W4e", "title": "GSV_pess = 1 > 0 = GSV_opt without any strict preference reversal",
            "source_test": "none in 51 (extends W3b)",
            "inputs": {"plans": plans_all, "requirement": req},
            "rankings": {"U": {"by_F_u": ["xG(0)=xH(0)"], "by_F_E": ["xG(1)", "xH(0)"]}},
            "choices": {"loose": lo["C_choice"], "strict": st["C_choice"]},
            "outputs": got, "expected": exp,
            "pass": all(_wdg_close(got[k], v) for k, v in exp.items()),
            "minimality": ("Minimal (1 BU, 2 plans). Shows 'aligned preferences => GSV<=0' must be stated "
                           "for strict alignment incl. ties: positive pessimistic screening can come from "
                           "follower indifference alone.")}





# ====================================================================================================
# PART T2 -- copied verbatim from witness_parts/w_mono_rob_miss.py (main block and ALL_* list removed)
# ====================================================================================================

_DOC_T2 = """Witness parts (theory agent T2): W5, W5b, W7, W8a, W8b, W8c.

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


# ====================================================================================================
# PART T3 -- copied verbatim from witness_parts/w_voi.py (main block and ALL_* list removed)
# ====================================================================================================

_DOC_T3 = """Q1 theory upgrade -- witness part w_voi (agent T3, Task E: sequential identification / VOI).

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



# ====================================================================================================
# PART T4 -- copied verbatim from witness_parts/w_mech.py (main block and ALL_* list removed)
# ====================================================================================================

_DOC_T4 = """T4 witness part: mechanism ablation fibres (M1-M4) and an information-asymmetry sign example.

Purely structural, pure stdlib, deterministic. No human data, no enterprise parameters.
All numbers are SIMULATED_ONLY illustrative values. No import from 51; the minimal
feasibility logic (F5a, F5b, F5d, F6, F7, F8 of 42 v2.2 Sec. 5) and the expectation
operator (X1, Sec. 6) are re-implemented independently from the definitions.

Contract: each witness_<id>() -> dict with keys
id, title, source_test, inputs, rankings, choices, outputs, expected, pass, minimality.
"""


def _mech_feasible(cfg, req, kappa):
    """Feasibility flags of 42 v2.2 (F5a, F5b, F5d, F6, F7, F8) for one (j,k).

    Ordinal values are only compared with >= or used as lookup keys (P5)."""
    a = cfg["M3"]["A"]
    h_req = req["H"][(a, kappa)]
    flags = {
        "F5a_H": cfg["M1"]["H"] >= h_req,
        "F6_EffH": True if h_req < 2 else bool(cfg["M1"]["EffH"]),
        "F5b_WI": cfg["M2"]["WI"] >= req["WI"][(a, kappa)],
        "F7_FB": True if a <= 1 else bool(cfg["M2"]["FB"]),
        "F8_Cons": (a, cfg["M3"]["m"]) in req["Cons"],
        "F5d_EA": cfg["M4"]["EA"] >= req["EA"][(a, kappa)],
    }
    return all(flags.values()), flags


def _mech_value(cfg, path):
    """(X1) with one role, one visible signal; rho is the design response of m (Sec. 9.1)."""
    total = 0.0
    for omega, p in path["P"].items():
        for r, pr in cfg["M3"]["rho"].items():
            total += p * pr * path["f"][(r, omega)]
    return total


def _mech_projection(cfg, removed):
    """Projection pi_S onto the components of the remaining mechanisms S = {M1..M4} minus removed."""
    keep = [m for m in ("M1", "M2", "M3", "M4") if m != removed]
    return tuple((m, tuple(sorted((k, str(v)) for k, v in cfg[m].items()))) for m in keep)


def witness_mech_ablation():
    kappa = "high"
    levels = (0, 1, 2, 3)
    req = {
        # H^req(A,kappa), WI^req, EA^req: same-construct ordinal requirement tables
        "H": {(a, kappa): (2 if a >= 2 else 0) for a in levels},
        "WI": {(a, kappa): (2 if a >= 2 else 0) for a in levels},
        "EA": {(a, kappa): (2 if a >= 2 else 0) for a in levels},
        # Cons(A,m): definitional consistency set (A=3 contradicts AI->Human)
        "Cons": {(0, "HumanOnly"), (2, "AI->Human"), (2, "Aggregation"),
                 (3, "BoundedExecution"), (3, "Delegated")},
    }
    verify = {"Verify": 1.0}
    use = {"Use": 1.0}
    path = {
        "P": {"correct": 0.9, "wrong": 0.1},
        # f = v - l - c - lambda*t per (r, omega); Verify costs 3 hours-equivalent, catches errors
        "f": {("Verify", "correct"): 7.0, ("Verify", "wrong"): -3.0,
              ("Use", "correct"): 10.0, ("Use", "wrong"): -50.0},
    }

    def cfg(H=3, EffH=1, WI=3, FB=1, m="AI->Human", A=2, rho=None, EA=3):
        return {"M1": {"H": H, "EffH": EffH}, "M2": {"WI": WI, "FB": FB},
                "M3": {"m": m, "A": A, "rho": rho or verify}, "M4": {"EA": EA}}

    cases = {
        # removed mechanism -> (k1 acceptable, k2 differs only in the removed mechanism)
        "M1": (cfg(), cfg(EffH=0)),                        # nominal sign-off without real veto
        "M2": (cfg(), cfg(FB=0)),                          # same rights/roles/evidence, no rollback path
        "M3_feas": (cfg(m="BoundedExecution", A=3, rho=use),
                    cfg(m="AI->Human", A=3, rho=use)),     # Cons(A,m) violated
        "M3_value": (cfg(m="AI->Human", rho=verify), cfg(m="Aggregation", rho=use)),
        "M4": (cfg(), cfg(EA=1)),                          # same outcome law P, weaker validation evidence
    }
    outputs, ok = {}, True
    for name, (k1, k2) in cases.items():
        removed = name.split("_")[0]
        f1, fl1 = _mech_feasible(k1, req, kappa)
        f2, fl2 = _mech_feasible(k2, req, kappa)
        v1, v2 = _mech_value(k1, path), _mech_value(k2, path)
        same_proj = _mech_projection(k1, removed) == _mech_projection(k2, removed)
        if name == "M3_value":
            pi_differs = f1 and f2 and v1 != v2
            chosen = "k1" if v1 > v2 else "k2"
        else:
            pi_differs = f1 != f2
            chosen = "k1" if f1 and not f2 else "k2"
        case_ok = same_proj and pi_differs
        ok = ok and case_ok
        outputs[name] = {"removed": removed, "same_projection_on_remaining": same_proj,
                         "feasible": (f1, f2), "failed_flags_k2": [k for k, v in fl2.items() if not v],
                         "value": (v1, v2), "problem_distinguishes": pi_differs,
                         "not_representable_without_removed": case_ok}
        outputs[name]["choice"] = chosen
    return {
        "id": "mech_ablation",
        "title": "M1-M4 irreducibility fibres: each removal leaves two alternatives indistinguishable "
                 "to the remaining three mechanisms but distinguished by a v2.2 decision problem",
        "source_test": "Q/01 Sec. 5 (Proposition IRR); 42 v2.2 Sec. 5 (F5a,F5b,F5d,F6,F7,F8), Sec. 6 (X1)",
        "inputs": {"kappa": kappa, "requirements": {k: (sorted(v.items()) if isinstance(v, dict) else sorted(v))
                                                    for k, v in req.items()},
                   "P": path["P"], "f": sorted(path["f"].items()),
                   "pairs": {n: (c[0], c[1]) for n, c in cases.items()}},
        "rankings": {n: ("k1 > k2" if o["choice"] == "k1" else "k2 > k1") for n, o in outputs.items()},
        "choices": {n: o["choice"] for n, o in outputs.items()},
        "outputs": outputs,
        "expected": "For every removal: identical projection on remaining mechanisms AND different "
                    "feasibility (or value, M3_value: 6.0 vs 4.0) => no model measurable in the remaining "
                    "components represents the problem.",
        "pass": ok,
        "minimality": "One initiative, one role, one visible signal, two outcomes, two alternatives per "
                      "removal; each pair differs in exactly one mechanism component. Fewer alternatives "
                      "cannot exhibit a non-injective projection.",
    }


def witness_ia_ndv_sign():
    """Sidecar (NOT canonical): with I_E coarser than I_u, delegation can beat centralized planning."""
    thetas = ("a", "b")
    phi = {("k0", "a"): 0.0, ("k0", "b"): 0.0, ("k1", "a"): 10.0, ("k1", "b"): 1.0,
           ("k2", "a"): 4.0, ("k2", "b"): 8.0}
    ks = ("k0", "k1", "k2")
    prior = {"a": 0.5, "b": 0.5}

    def b_info_choice():
        # plug-in prior-mean planner; ties -> lowest index (stated convention, both shown equal here)
        ev = {k: sum(prior[t] * phi[(k, t)] for t in thetas) for k in ks}
        return max(ks, key=lambda k: (ev[k], -ks.index(k))), ev

    def minimax_regret_choice():
        reg = {k: max(max(phi[(kk, t)] for kk in ks) - phi[(k, t)] for t in thetas) for k in ks}
        return min(ks, key=lambda k: (reg[k], ks.index(k))), reg

    kb, ev = b_info_choice()
    kr, reg = minimax_regret_choice()
    out = {}
    ok = kb == kr == "k2"
    for scen, phi_u_shift in (("aligned", {}), ("misaligned", {("k1", "b"): 9.0})):
        for t in thetas:
            phi_u = {k: phi_u_shift.get((k, t), phi[(k, t)]) for k in ks}
            follower = max(ks, key=lambda k: (phi_u[k], -ks.index(k)))  # unique argmax in this instance
            b_full = max(phi[(k, t)] for k in ks)
            b_info = phi[(kb, t)]
            c_info = phi[(follower, t)]  # equal resource use a(k1)=a(k2): envelope cannot separate
            lia = b_full - b_info
            dl_info = b_full - c_info
            ndv = c_info - b_info
            out[(scen, t)] = {"B_full": b_full, "B_info": b_info, "C_info": c_info,
                              "LIA": lia, "DL_info": dl_info, "NDV": ndv,
                              "identity_NDV_eq_LIA_minus_DLinfo": ndv == lia - dl_info}
            ok = ok and out[(scen, t)]["identity_NDV_eq_LIA_minus_DLinfo"]
    ok = ok and out[("aligned", "a")]["NDV"] > 0 and out[("misaligned", "b")]["NDV"] < 0
    return {
        "id": "ia_ndv_sign",
        "title": "Information-asymmetry sidecar: NDV = LIA - DL_info can be positive or negative "
                 "(P3 ordering B>=C is an artifact of full information)",
        "source_test": "Q/08 Sec. 4-5 (sidecar design only); 42 v2.2 Sec. 15 P3",
        "inputs": {"Theta_u": thetas, "prior_I_E": prior, "phi_E(k,theta)": sorted(phi.items()),
                   "misalignment": {"phi_u(k1,b)": 9.0}, "resource": "a(k1)=a(k2), envelope non-separating"},
        "rankings": {"prior_mean": ev, "max_regret": reg},
        "choices": {"B_info_prior_mean": kb, "B_info_minimax_regret": kr},
        "outputs": {f"{s}|theta={t}": v for (s, t), v in out.items()},
        "expected": "aligned, theta=a: NDV=+6 (=LIA, DL_info=0); misaligned, theta=b: NDV=-7 (LIA=0, DL_info=7)",
        "pass": ok,
        "minimality": "One unit, one initiative, two types, three configs; constructive example only, "
                      "SIMULATED_ONLY, not a theorem and not a v2.2 result.",
    }




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


# ====================================================================================================
# INTEGRATOR HARNESS (T5)
# ====================================================================================================
# (namespaced id, function, part, original part id, canonical?, demonstrates)
Q1_REGISTRY = [
    # ---------------- required canonical set ----------------
    ("W1", witness_W1, "T1", "W1", True, "aligned ledgers: B = C = 30, DL = 0 (T-ORC-8 aligned)"),
    ("W2", witness_W2, "T1", "W2", True, "misaligned but envelope-blockable: B = C = 15, DL = 0"),
    ("W3", witness_W3, "T1", "W3", True, "misaligned and envelope-unblockable: B = 15, C = 10, DL = 5"),
    ("W4", witness_W4, "T1", "W4", True, "P8 governance screening 10 -> 15"),
    ("W5", witness_W5_delta, "T2", "W5", True, "Model C build decision non-monotone in reuse delta (1 -> 0 -> 1)"),
    ("W6", witness_W6, "T3", "W6", True, "vertex-conditioned VOI overstatement (vertex 1, true 1/2)"),
    ("W7", witness_W7, "T2", "W7", True, "element-level robustness counterexample (vertex ROBUST, interior FRAGILE)"),
    # ---------------- supplementary ----------------
    ("W3m", witness_W3m, "T1", "W3m", False, "minimal DL > 0 (1 BU, 1 resource, 2 plans)"),
    ("W3b", witness_W3b, "T1", "W3b", False, "DL_opt = 0 < DL_pess = 1 from a follower tie"),
    ("W3c", witness_W3c, "T1", "W3c", False, "pairwise primitives do not determine the sign of DL"),
    ("W4b", witness_W4b, "T1", "W4b", False, "screening in the opposite direction 15 -> 10"),
    ("W4c", witness_W4c, "T1", "W4c", False, "screening removes DL = 5 but price of requirement PR_B = 8"),
    ("W4d", witness_W4d, "T1", "W4d", False, "pairwise screening insufficient (worse x^M becomes best response)"),
    ("W4e", witness_W4e, "T1", "W4e", False, "GSV_pess > 0 = GSV_opt without strict reversal"),
    ("W_DL_AL3", witness_W_DL_AL3, "T1", "W5", False, "DL > 0 with F_u == F_E via a unit-only constraint (AL3)"),
    ("W5b", witness_W5b_delta, "T2", "W5b", False, "Model B monotone in delta; source-indexing assumption load-bearing"),
    ("W5_WIDE", witness_W5_WIDE, "T7", "W5_WIDE", False, "wide-margin W5 supplement: region [0,4) U (7,inf), +-5% perturbation survivors"),
    ("W6b", witness_W6b, "T3", "W6b", False, "adaptive candidate set: Theta shrinkage raises MMR, VOI = -1"),
    ("W6c", witness_W6c, "T3", "W6c", False, "grid refinement: nested monotone, non-nested / edge-only not"),
    ("W6d", witness_W6d, "T3", "W6d", False, "Theta-independent benchmark: monotone but not vertex-exact"),
    ("W6e", witness_W6e, "T3", "W6e", False, "myopic VOI complementarity (single VOIs 0, joint removes regret)"),
    ("W6f", witness_W6f, "T3", "W6f", False, "no termination guarantee without discretised evidence"),
    ("W8a", witness_W8a, "T2", "W8a", False, "feasibility-changing missingness (zero-fill fabricates feasibility)"),
    ("W8b", witness_W8b, "T2", "W8b", False, "decision-changing missingness via objective (lambda, ledger split, status-quo cell)"),
    ("W8c", witness_W8c, "T2", "W8c", False, "decision-invariant but epistemically relevant missingness"),
    ("W_MECH_ABL", witness_mech_ablation, "T4", "mech_ablation", False, "M1-M4 ablation fibres (each mechanism separately decision-relevant)"),
    ("W_IA_NDV", witness_ia_ndv_sign, "T4", "ia_ndv_sign", False, "information-asymmetry sidecar: NDV sign can be + or - (NOT canonical v2.2)"),
]

# Embedded canonical anchors: exact substrings of Q/baseline/BASELINE_V2_2_RUN_STDOUT.txt (51 run, VERDICT PASS)
Q1_BASELINE_ANCHORS = {
    "T-ORC-8": "PASS T-ORC-8: aligned B=C=30; blockable B=C=15, DL=0; unblockable B=15, C=10, DL=5, VSC=15, NEV=10",
    "REG-P8": "P8 screening (10->15)",
    "T-SEN-8": "C: y_c* sequence ['1', '1', '1', '1', '0', '0', '0', '1'] over delta [0.0, 1.0, 2.0, 2.9, 3.0, 3.5, 4.0, 5.0]",
    "T-SEN-7": "vertex-conditioned VOI_v = 1 (overstated), grid VOI_v = 0.5 = true value",
    "T-SEN-3": "element-level counterexample: vertex-only classification says ROBUST, adding interior points gives FRAGILE",
}


def _q1_dumps(obj):
    return _q1_json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def _q1_canon(x):
    """Canonical JSON-serialisable form: sorted dict keys (non-str keys -> canonical JSON text), tuples -> lists,
    sets sorted by canonical text, Fraction -> 'p/q' string; rejects callables and non-finite floats."""
    if isinstance(x, bool) or x is None or isinstance(x, (int, str)):
        return x
    if isinstance(x, float):
        if x != x or x in (float("inf"), float("-inf")):
            raise ValueError("non-finite float in witness data")
        return x
    if isinstance(x, _Q1Fr):
        return "%d/%d" % (x.numerator, x.denominator) if x.denominator != 1 else "%d" % x.numerator
    if isinstance(x, dict):
        out = {}
        for k, v in x.items():
            ks = k if isinstance(k, str) else _q1_dumps(_q1_canon(k))
            if ks in out:
                raise ValueError("canonical key collision: %r" % ks)
            out[ks] = _q1_canon(v)
        return out
    if isinstance(x, (list, tuple)):
        return [_q1_canon(v) for v in x]
    if isinstance(x, (set, frozenset)):
        return sorted((_q1_canon(v) for v in x), key=_q1_dumps)
    raise TypeError("non-canonical object in witness data: %r" % type(x))


def _q1_run_one(nid, fn, part, orig, canonical):
    raw = fn()
    if raw.get("id") != orig:
        raise AssertionError("part id mismatch for %s: %r != %r" % (nid, raw.get("id"), orig))
    for key in ("id", "title", "source_test", "inputs", "rankings", "choices", "outputs", "expected", "pass",
                "minimality"):
        if key not in raw:
            raise AssertionError("%s: contract key %r missing" % (nid, key))
    data = dict(raw)
    data["id"] = nid
    data["part"] = part
    data["part_id"] = orig
    data["set"] = "CANONICAL" if canonical else "SUPPLEMENTARY"
    data["status"] = "SIMULATED_ONLY computational witness / constructive example (not a proof)"
    canon = _q1_canon(data)
    sha = _q1_hashlib.sha256(_q1_dumps(canon).encode("ascii")).hexdigest()
    return canon, sha


def _q1_run_all():
    return [(nid, part, canonical, demo) + _q1_run_one(nid, fn, part, orig, canonical)
            for nid, fn, part, orig, canonical, demo in Q1_REGISTRY]


def _q1_cross_checks(res):
    by = {r[0]: r[4] for r in res}
    w1, w2, w3, w4 = (by[k]["outputs"] for k in ("W1", "W2", "W3", "W4"))
    w5, w6, w7 = by["W5"], by["W6"]["outputs"], by["W7"]["outputs"]
    return [
        ("T-ORC-8 aligned B=C=30, DL=0 (W1)",
         w1["B"] == 30 and w1["C_opt"] == 30 and w1["C_pess"] == 30 and w1["DL_opt"] == 0 and w1["DL_pess"] == 0),
        ("T-ORC-8 blockable B=C=15, DL=0 (W2)",
         w2["B"] == 15 and w2["C_opt"] == 15 and w2["C_pess"] == 15 and w2["DL_opt"] == 0 and w2["DL_pess"] == 0),
        ("T-ORC-8 unblockable B=15, C=10, DL=5, VSC=15, NEV=10 (W3)",
         w3["B"] == 15 and w3["C_opt"] == 10 and w3["C_pess"] == 10 and w3["DL_opt"] == 5 and w3["DL_pess"] == 5
         and w3["VSC"] == 15 and w3["NEV_opt"] == 10 and w3["NEV_pess"] == 10),
        ("REG P8 screening 10 -> 15 (W4)",
         w4["C_opt_loose"] == 10 and w4["C_opt_strict"] == 15 and w4["C_pess_loose"] == 10
         and w4["C_pess_strict"] == 15),
        ("T-SEN-8 C sequence 1,1,1,1,0,0,0,1 over delta [0,1,2,2.9,3,3.5,4,5] (W5)",
         w5["outputs"]["seq_pess_strict"] == ["1", "1", "1", "1", "0", "0", "0", "1"]
         and w5["inputs"]["delta_grid"] == [0.0, 1.0, 2.0, 2.9, 3.0, 3.5, 4.0, 5.0]),
        ("T-SEN-7 vertex VOI_v = 1, true VOI_v = 1/2 (W6)",
         w6["VOI_v vertex"] == "1" and w6["VOI_v exact"] == "1/2"),
        ("T-SEN-3 element-level vertex ROBUST / interior FRAGILE (W7)",
         w7["B_element_vertex_class"] == "ROBUST" and w7["B_element_grid_class"] == "FRAGILE"),
    ]


def _q1_baseline_file_check():
    here = _q1_os.path.dirname(_q1_os.path.abspath(__file__))
    p = _q1_os.path.join(here, "baseline", "BASELINE_V2_2_RUN_STDOUT.txt")
    if not _q1_os.path.exists(p):
        return "NOT_FOUND (embedded anchors used; not counted as FAIL)", True
    with open(p, encoding="utf-8") as fh:
        txt = fh.read()
    missing = [k for k, s in Q1_BASELINE_ANCHORS.items() if s not in txt]
    if missing:
        return "MISMATCH: anchors not found verbatim: %s" % missing, False
    return "MATCH: all %d anchors found verbatim in baseline/BASELINE_V2_2_RUN_STDOUT.txt" % len(Q1_BASELINE_ANCHORS), True


def _q1_block(label, obj):
    txt = _q1_json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False)
    return "  %s:\n" % label + "\n".join("    " + line for line in txt.splitlines())


def _q1_print_witness(nid, part, demo, canon, sha):
    print("")
    print("-" * 110)
    print("[%s] %s   (%s; part %s, part id %s)" % (nid, canon["title"], canon["set"], part, canon["part_id"]))
    print("-" * 110)
    print("  demonstrates: " + demo)
    print("  source test mapping: " + str(canon["source_test"]))
    for label, key in (("inputs (algebraic)", "inputs"), ("rankings", "rankings"), ("choices", "choices"),
                       ("outputs", "outputs"), ("expected", "expected")):
        print(_q1_block(label, canon[key]))
    print("  minimality: " + str(canon["minimality"]))
    print("  result: " + ("PASS" if canon["pass"] else "FAIL"))
    print("  witness_sha256: " + sha)


def main(argv):
    res1 = _q1_run_all()
    res2 = _q1_run_all()       # second in-process run (determinism)
    det_ok = [(r[0], r[5]) for r in res1] == [(r[0], r[5]) for r in res2]
    if "--hashes" in argv:
        for nid, part, canonical, demo, canon, sha in res1:
            print("%-11s %s %s" % (nid, sha, "PASS" if canon["pass"] else "FAIL"))
        print("IN_PROCESS_DETERMINISM:", "PASS" if det_ok else "FAIL")
        return 0
    print("=" * 110)
    print("Q1 THEORY WITNESSES -- consolidated computational witnesses (integrator T5)")
    print("SIMULATED_ONLY. Constructive examples / computational witnesses on algebraic instances; NOT proofs of")
    print("general theorems; no enterprise data, no human coder data, no V7 / empirical validity claim. Model: 42 v2.2.")
    print("Fixed seed (declared): %d; only W5_WIDE draws random numbers, from a private Random(20261015 + stream)" % Q1_FIXED_SEED)
    print("Hash = SHA-256 of canonical JSON (sorted keys, separators (',',':'), ASCII) of the full witness record.")
    print("Bounded search inside W5: 3 exhaustive single-follower families (sizes printed in W5 outputs.search).")
    print("=" * 110)
    for nid, part, canonical, demo, canon, sha in res1:
        _q1_print_witness(nid, part, demo, canon, sha)
    checks = _q1_cross_checks(res1)
    bstat, bok = _q1_baseline_file_check()
    print("")
    print("=" * 110)
    print("CROSS-CHECK AGAINST CANONICAL 51 BASELINE (Q/baseline/BASELINE_V2_2_RUN_STDOUT.txt)")
    for k, s in Q1_BASELINE_ANCHORS.items():
        print("  anchor %-8s %s" % (k, s))
    for name, ok in checks:
        print("  %-4s %s" % ("PASS" if ok else "FAIL", name))
    print("  baseline file: " + bstat)
    print("")
    print("SUMMARY TABLE")
    print("  %-11s %-13s %-4s %-6s %-64s %s" % ("id", "set", "part", "result", "sha256", "demonstrates"))
    for nid, part, canonical, demo, canon, sha in res1:
        print("  %-11s %-13s %-4s %-6s %-64s %s" % (nid, canon["set"], part, "PASS" if canon["pass"] else "FAIL",
                                                   sha, demo))
    n = len(res1)
    npass = sum(1 for r in res1 if r[4]["pass"])
    ncan = sum(1 for r in res1 if r[2])
    setsha = _q1_hashlib.sha256("".join(r[0] + ":" + r[5] + "\n" for r in res1).encode("ascii")).hexdigest()
    print("")
    print("  witnesses: %d (canonical %d, supplementary %d); PASS %d / FAIL %d" % (n, ncan, n - ncan, npass, n - npass))
    print("  cross-checks: %d/%d PASS" % (sum(1 for c in checks if c[1]), len(checks)))
    print("  IN_PROCESS_DETERMINISM (2 runs, identical per-witness hashes): " + ("PASS" if det_ok else "FAIL"))
    print("  witness_set_sha256: " + setsha)
    verdict = npass == n and all(c[1] for c in checks) and bok and det_ok
    print("Q1_WITNESS_VERDICT: " + ("PASS" if verdict else "FAIL"))
    return 0 if verdict else 1


if __name__ == "__main__":
    _q1_sys.exit(main(_q1_sys.argv[1:]))
