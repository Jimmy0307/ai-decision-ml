"""Enterprise AI Portfolio solver v2.2 — SYNTHETIC ENGINEERING ONLY.

Supersedes 46 (kept for provenance) as the reference implementation of
42_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md. Adds, relative to 46:
  * typed units (T-SCH-5), explicit omega-leakage guard (T-SCH-6), NaN/inf rejection (T-SCH-7)
  * (F5e) data/interface thresholds R_j(s) >= R^req(A), D_j(s) >= D^req(A)          (T-ALG-1)
  * portfolio_result output contract + missing-data state machine            (T-MIS-3/4/6)
  * multiple-choice knapsack DP with explicit quanta and error bound           (T-ORC-9)
  * shared-capability limit test, Model D gate                                 (T-ORC-10/12)
  * reproducibility hashing and label-permutation invariance                   (T-ORC-13, T-INV-4)
  * Lemma R vertex check (scope-guarded), robust feasibility, scenario-registry
    hashing, MaxRegret and value-of-identification                             (T-SEN-3/4/6/7)
  * delta threshold scan in B and a Model C non-monotonic counterexample       (T-SEN-8)
  * independent hand-oracle comparison                                          (T-ORC-8)

Every number produced here is SIMULATED_ONLY. No enterprise observation appears in this file.
Run:  python 51_enterprise_portfolio_solver_v2_2.py          (all tests; prints verdict)
      python 51_enterprise_portfolio_solver_v2_2.py --repro-hash   (prints a result hash)
"""
from __future__ import annotations

import copy
import hashlib
import itertools
import json
import math
import random
import subprocess
import sys
from dataclasses import dataclass

SOLVER_VERSION = "51_enterprise_portfolio_solver_v2_2"
TOL = 1e-9
RESPONSES = ("Use", "Verify", "Modify", "Escalate", "Reject", "Bypass", "NA")

# =============================================================================
# 1. Exceptions and statuses
# =============================================================================
STATUS_ORDER = [
    "INVALID_SCHEMA_OR_UNITS", "REJECT_INSUFFICIENT_IDENTIFIED_INPUTS", "NOT_COMPARABLE",
    "FOLLOWER_LEDGER_UNIDENTIFIED", "INFEASIBLE", "THRESHOLD_MODE", "PARTIAL_OBJECTIVE",
    "UNEVALUABLE_INITIATIVE", "RESTRICTED_SOLVE", "STATUS_QUO_NONCOMPLIANT",
    "DESIGN_INFEASIBLE_UNDER_RESPONSE", "OK_INTERVAL", "OK_POINT",
]


class InvalidInput(ValueError):
    """INVALID_SCHEMA_OR_UNITS"""


class MissingInput(ValueError):
    """A required lookup cell is UNIDENTIFIED."""


class FollowerLedgerUnidentified(MissingInput):
    pass


class NotComparable(ValueError):
    pass


class ScopeError(ValueError):
    """A theorem is being applied outside the scope in which it is proven."""


def strict(d, key, what):
    if d is None or key not in d or d[key] is None:
        raise MissingInput(f"{what} UNIDENTIFIED: {key!r}")
    return d[key]


# =============================================================================
# 2. Typed units (T-SCH-5) and finiteness (T-SCH-7)
# =============================================================================
BASE = ("TWD", "hour", "event", "period", "incident")
UNIT_TABLE = {
    "TWD/event": {"TWD": 1, "event": -1},
    "TWD/period": {"TWD": 1, "period": -1},
    "hours/event": {"hour": 1, "event": -1},
    "hours/period": {"hour": 1, "period": -1},
    "TWD/hour": {"TWD": 1, "hour": -1},
    "events/period": {"event": 1, "period": -1},
    "incidents/period": {"incident": 1, "period": -1},
    "probability": {},
    "1/period": {"period": -1},
}


def _dims(d):
    return tuple(sorted((k, v) for k, v in d.items() if v))


@dataclass(frozen=True)
class Q:
    """A dimensioned scalar. Construction rejects NaN/inf; + and - require identical dimensions."""
    value: float
    dims: tuple

    def __post_init__(self):
        if isinstance(self.value, bool) or not isinstance(self.value, (int, float)):
            raise InvalidInput(f"non-numeric quantity {self.value!r}")
        if not math.isfinite(self.value):
            raise InvalidInput(f"non-finite quantity {self.value!r}")

    @staticmethod
    def of(value, unit):
        if unit not in UNIT_TABLE:
            raise InvalidInput(f"unknown unit {unit}")
        q = Q(value, _dims(UNIT_TABLE[unit]))
        if unit == "probability" and not (-TOL <= value <= 1 + TOL):
            raise InvalidInput("probability outside [0,1]")
        return q

    def _same(self, o):
        if not isinstance(o, Q) or o.dims != self.dims:
            raise InvalidInput(f"dimension mismatch: {self.dims} vs {getattr(o, 'dims', type(o))}")

    def __add__(self, o):
        self._same(o)
        return Q(self.value + o.value, self.dims)

    def __sub__(self, o):
        self._same(o)
        return Q(self.value - o.value, self.dims)

    def __mul__(self, o):
        if not isinstance(o, Q):
            raise InvalidInput("multiply only by typed quantities")
        d = dict(self.dims)
        for k, v in o.dims:
            d[k] = d.get(k, 0) + v
        return Q(self.value * o.value, _dims(d))

    def __truediv__(self, o):
        if not isinstance(o, Q):
            raise InvalidInput("divide only by typed quantities")
        d = dict(self.dims)
        for k, v in o.dims:
            d[k] = d.get(k, 0) - v
        return Q(self.value / o.value, _dims(d))

    def __le__(self, o):
        self._same(o)
        return self.value <= o.value + TOL

    def unit_is(self, unit):
        return self.dims == _dims(UNIT_TABLE[unit])


# =============================================================================
# 3. Ordinal guard
# =============================================================================
@dataclass(frozen=True)
class Ord:
    construct: str
    code: float

    def _check(self, other):
        if not isinstance(other, Ord) or other.construct != self.construct:
            raise TypeError("ordinal comparison across constructs is forbidden")

    def __ge__(self, other):
        self._check(other)
        return self.code >= other.code

    def __lt__(self, other):
        self._check(other)
        return self.code < other.code

    def _no_arith(self, *_):
        raise TypeError("ordinal arithmetic is forbidden (42 §1.3)")

    __add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = _no_arith
    __truediv__ = __rtruediv__ = __float__ = __int__ = _no_arith


DEFAULT_CODES = {k: {0: 0, 1: 1, 2: 2, 3: 3} for k in ("A", "H", "WI", "EA", "G", "K", "R", "D")}


def O(construct, level, codes=None):
    codes = codes or DEFAULT_CODES
    return Ord(construct, codes[construct][level])


# =============================================================================
# 4. Schema validation (T-SCH-5/6/7)
# =============================================================================
PATH_UNITS = {"v_u": "TWD/event", "v_x": "TWD/event", "l_u": "TWD/event", "l_x": "TWD/event",
              "c_u": "TWD/event", "c_x": "TWD/event", "t": "hours/event", "t_rev": "hours/event",
              "I_sev": "probability"}


def _num(value, unit, where, allow_none):
    if value is None:
        if allow_none:
            return
        raise InvalidInput(f"required numeric missing at {where}")
    Q.of(value, unit)  # rejects non-numeric, NaN, inf, out-of-range probability


def _prob_row(row, where):
    if not isinstance(row, dict):
        raise InvalidInput(f"probability row expected at {where}")
    for k, p in row.items():
        _num(p, "probability", f"{where}[{k}]", allow_none=True)
    if all(p is not None for p in row.values()) and not math.isclose(sum(row.values()), 1.0, abs_tol=1e-9):
        raise InvalidInput(f"probability row at {where} does not sum to 1")


def validate_instance(inst):
    """Raises InvalidInput on any schema/unit/finite violation. None (UNIDENTIFIED) is allowed
    where the state machine handles it; it is never converted to a number here."""
    for c, d in inst["caps"].items():
        _num(d["F"], "TWD/period", f"caps.{c}.F", True)
        _num(d["eng"], "hours/period", f"caps.{c}.eng", True)
    for key, d in inst["loc_caps"].items():
        _num(d["F"], "TWD/period", f"loc_caps.{key}.F", True)
        _num(d["eng"], "hours/period", f"loc_caps.{key}.eng", True)
    for h, unit in (("BUD", "TWD/period"), ("ENG", "hours/period")):
        _num(inst["A_bar"].get(h), unit, f"A_bar.{h}", True)
    for u in inst["units"]:
        _num(inst["rev_cap"].get(u), "hours/period", f"rev_cap.{u}", True)
        b0 = inst.get("B0", {}).get(u)
        if b0 is not None:
            _num(b0["BUD"], "TWD/period", f"B0.{u}.BUD", True)
            _num(b0["ENG"], "hours/period", f"B0.{u}.ENG", True)
    for lamkey in ("lam", "lam_u", "lam_U"):
        for role, v in inst.get(lamkey, {}).items():
            _num(v, "TWD/hour", f"{lamkey}.{role}", True)
    for g, pol in inst["policies"].items():
        _num(pol["gov_cost"], "TWD/period", f"policies.{g}.gov_cost", True)
        for j, v in pol["G"].items():
            if v is not None and not (isinstance(v, Ord) and v.construct == "G"):
                raise InvalidInput(f"policies.{g}.G.{j} must be Ord('G')")
        for tbl in ("allow", "allow_loc"):
            for key, v in pol[tbl].items():
                if v not in (0, 1, None) or isinstance(v, float):
                    raise InvalidInput(f"policies.{g}.{tbl}{key} must be binary")
        for j, e in pol["ebar"].items():
            _num(e, "incidents/period", f"policies.{g}.ebar.{j}", True)
        for tname in ("H_req", "WI_req", "EA_req", "G_req"):
            for (a, kk), v in pol[tname].items():
                if not (isinstance(a, Ord) and isinstance(kk, Ord)) or (v is not None and not isinstance(v, Ord)):
                    raise InvalidInput(f"{tname} must be keyed and valued by ordinal keys")
    for tname in ("R_req", "D_req"):
        for a, v in inst[tname].items():
            if not isinstance(a, Ord) or (v is not None and not isinstance(v, Ord)):
                raise InvalidInput(f"{tname} must use ordinal keys")
    for j, ini in inst["initiatives"].items():
        for k, n in ini["N"].items():
            _num(n, "events/period", f"{j}.N.{k}", True)
        for c, tau in ini["tau"].items():
            _num(tau, "TWD/period", f"{j}.tau.{c}", True)
        for k, cfg in ini["configs"].items():
            where = f"{j}.{k}"
            for name in ("A", "H", "WI", "EA"):
                if not isinstance(cfg[name], Ord) or cfg[name].construct != name:
                    raise InvalidInput(f"{where}.{name} must be Ord('{name}')")
            for tbl, unit in (("impl", "TWD/period"), ("eng", "hours/period")):
                for key, v in cfg[tbl].items():
                    _num(v, unit, f"{where}.{tbl}.{sorted(key)}", True)
            _num(cfg.get("impl_x"), "TWD/period", f"{where}.impl_x", True)
            _prob_row(cfg["pi"], f"{where}.pi")
            _prob_row(cfg["P"], f"{where}.P")
            Z = {z for (z, _) in cfg["P"]}
            W = {w for (_, w) in cfg["P"]}
            if Z & W:
                raise InvalidInput(f"{where}: visible-signal and hidden-outcome labels must be disjoint")
            roles = set(cfg["pi"])
            for rk in list(cfg["rho"]) + list(cfg.get("rho_design", {})):
                # T-SCH-6: rho(r | k, z, role[, capability state]) -- omega may never condition rho
                if not isinstance(rk, tuple) or len(rk) not in (2, 3):
                    raise InvalidInput(f"{where}: rho key must be (z, role) or (z, role, capstate)")
                if any(x in W for x in rk):
                    raise InvalidInput(f"{where}: hidden outcome omega appears in rho conditioning key {rk}")
                if rk[0] not in Z or rk[1] not in roles:
                    raise InvalidInput(f"{where}: rho key {rk} must start with a visible signal and a role")
            for rows_name in ("rho", "rho_design"):
                for rk, row in cfg.get(rows_name, {}).items():
                    _prob_row(row, f"{where}.{rows_name}[{rk}]")
            for pk, cell in cfg["path"].items():
                for f, unit in PATH_UNITS.items():
                    _num(cell.get(f), unit, f"{where}.path[{pk}].{f}", True)
        for tbl in ("R_state", "D_state"):
            for key, v in ini[tbl].items():
                if v is not None and not isinstance(v, Ord):
                    raise InvalidInput(f"{j}.{tbl} must hold ordinal values")
    return True


# =============================================================================
# 5. Expectation (X1) and per-(j,k) evaluation
# =============================================================================
def _normalized(dist, what):
    if any(p is None for p in dist.values()):
        raise MissingInput(f"{what} contains UNIDENTIFIED probability")
    if any(p < -TOL for p in dist.values()) or not math.isclose(sum(dist.values()), 1.0, abs_tol=1e-9):
        raise InvalidInput(f"{what} must be nonnegative and normalized")


def expect(cfg, fn, rho_key="rho"):
    _normalized(cfg["pi"], "pi")
    _normalized(cfg["P"], "P")
    total = 0.0
    rho_tab = cfg[rho_key]
    for role, p_role in cfg["pi"].items():
        for (z, w), p_zw in cfg["P"].items():
            rho = rho_tab.get((z, role))
            if rho is None:
                raise MissingInput("rho row missing")
            _normalized(rho, "rho")
            for r, p_r in rho.items():
                if p_r <= 0:
                    continue
                if r not in cfg["allowed_r"]:
                    raise InvalidInput("forbidden response has positive probability")
                cell = cfg["path"].get((role, z, w, r))
                if cell is None or any(v is None for v in cell.values()):
                    raise MissingInput("outcome lookup UNIDENTIFIED")
                total += p_role * p_zw * p_r * fn(cell, role)
    return total


def source_key(rel, y_shared, loc):
    return frozenset((c, "L" if c in loc else "S") for c in rel if c in loc or c in y_shared)


def lam_of(inst, key, role):
    v = inst[key].get(role)
    if v is None:
        raise MissingInput(f"{key}.{role} UNIDENTIFIED")
    return v


def jk_eval(inst, j, k, y_shared, loc, gamma_name, rho_key="rho"):
    ini = inst["initiatives"][j]
    pol = inst["policies"][gamma_name]
    cfg, cfg0 = ini["configs"][k], ini["configs"][0]
    avail = set(y_shared) | set(loc)
    key = source_key(ini["rel"], y_shared, loc)
    lam_override = inst.get("_lam_override", {})

    def lam(role, which="lam"):
        if role in lam_override:
            return lam_override[role]
        return lam_of(inst, which, role)

    def g_E(c):
        return expect(c, lambda x, role: x["v_u"] + x["v_x"] - x["l_u"] - x["l_x"] - x["c_u"] - x["c_x"] - lam(role) * x["t"], rho_key)

    def opc(c):
        return expect(c, lambda x, role: x["c_u"] + x["c_x"], rho_key)

    N_k, N_0 = strict(ini["N"], k, "N"), strict(ini["N"], 0, "N")
    impl = 0.0 if k == 0 else strict(cfg["impl"], key, "implementation cost")
    eng = 0.0 if k == 0 else strict(cfg["eng"], key, "engineering hours")
    phiE = 0.0 if k == 0 else N_k * g_E(cfg) - N_0 * g_E(cfg0)
    phiE = phiE - impl
    bud = 0.0 if k == 0 else impl + N_k * opc(cfg) - N_0 * opc(cfg0)
    rev = 0.0 if k == 0 else N_k * expect(cfg, lambda x, r: x["t_rev"], rho_key) - N_0 * expect(cfg0, lambda x, r: x["t_rev"], rho_key)
    sev = N_k * expect(cfg, lambda x, r: x["I_sev"], rho_key)
    hours = 0.0 if k == 0 else N_k * expect(cfg, lambda x, r: x["t"], rho_key) - N_0 * expect(cfg0, lambda x, r: x["t"], rho_key)
    try:
        def g_U(c):
            return expect(c, lambda x, role: x["v_u"] - x["l_u"] - x["c_u"] - lam(role, "lam_u") * x["t"], rho_key)
        impl_x = 0.0 if k == 0 else strict(cfg, "impl_x", "central-funded implementation share")
        tau = 0.0 if k == 0 else sum(strict(ini["tau"], c, "chargeback rule")
                                     for c in cfg["pre"] if c in y_shared and c not in loc)
        phiU = 0.0 if k == 0 else N_k * g_U(cfg) - N_0 * g_U(cfg0) - (impl - impl_x) - tau
    except MissingInput:
        phiU = None

    kap, A = ini["kappa"], cfg["A"]
    req = lambda table: strict(table, (A, kap), "requirement table cell")
    # F5e state: configuration k>0 at the capability-source pattern it would run on; the status quo k=0 at
    # the CURRENT capability state (consistent with the status-quo baseline of (V2)).
    f5e_key = key if k != 0 else source_key(ini["rel"], inst.get("y_cur", frozenset()), set())
    codes = inst["codes"]
    static_ok = (
        cfg["legal"] == 1                                                              # F2
        and strict(pol["allow"], (j, k), "Allow") == 1                                 # F3
        and (j not in pol["forbid"] or k == 0)
        and all(c in avail for c in cfg["pre"])                                        # F4
        and cfg["H"] >= req(pol["H_req"])                                              # F5a
        and cfg["WI"] >= req(pol["WI_req"])                                            # F5b
        and strict(pol["G"], j, "G_j(gamma)") >= req(pol["G_req"])                     # F5c
        and cfg["EA"] >= req(pol["EA_req"])                                            # F5d
        and strict(ini["R_state"], f5e_key, "R_j(s)") >= strict(inst["R_req"], A, "R^req(A)")   # F5e
        and strict(ini["D_state"], f5e_key, "D_j(s)") >= strict(inst["D_req"], A, "D^req(A)")   # F5e
        and (not (req(pol["H_req"]) >= O("H", 2, codes)) or cfg["effH"] == 1)          # F6
        and (cfg["A"] < O("A", 2, codes) or cfg["FB"] == 1)                            # F7
        and cfg["cons"] == 1                                                           # F8
    )
    f9 = sev <= strict(pol["ebar"], j, "incident tolerance") + TOL                     # F9
    return dict(feasible=static_ok and f9, static_ok=static_ok, f9=f9, legal=cfg["legal"] == 1,
                phiE=phiE, phiU=phiU, bud=bud, eng=eng, rev=rev, sev=sev, hours=hours)


# =============================================================================
# 6. Unit plans
# =============================================================================
def _subsets(items):
    items = list(items)
    for r in range(len(items) + 1):
        yield from itertools.combinations(items, r)


def unit_plans(inst, u, y_shared, gamma_name, allow_local=True, log=None, rho_key="rho"):
    pol = inst["policies"][gamma_name]
    js = sorted(j for j, ini in inst["initiatives"].items() if ini["unit"] == u)
    loc_caps = []
    for (uu, c) in sorted(inst["loc_caps"]):
        if uu != u or not allow_local:
            continue
        flag = pol["allow_loc"].get((u, c))
        if flag is None:
            if log is not None:
                log.add(("allow_loc", u, c))   # UNIDENTIFIED permission: option excluded and reported
            continue
        if flag == 1:
            loc_caps.append(c)
    plans = []
    for loc in _subsets(loc_caps):
        loc_bud = sum(strict(inst["loc_caps"][(u, c)], "F", "local capability cost") for c in loc)
        loc_eng = sum(strict(inst["loc_caps"][(u, c)], "eng", "local capability hours") for c in loc)
        per_j = []
        for j in js:
            opts = []
            for k in sorted(inst["initiatives"][j]["configs"]):
                if j in pol["must"] and k == 0:
                    continue
                try:
                    ev = jk_eval(inst, j, k, set(y_shared), set(loc), gamma_name, rho_key)
                except MissingInput:
                    if k == 0:
                        raise
                    if log is not None:
                        log.add((j, k))
                    continue
                if ev["feasible"]:
                    opts.append((k, ev))
            per_j.append(opts)
        for combo in itertools.product(*per_j):
            if sum(ev["rev"] for _, ev in combo) > strict(inst["rev_cap"], u, "rev_cap") + TOL:
                continue
            fU = None if any(ev["phiU"] is None for _, ev in combo) else sum(ev["phiU"] for _, ev in combo) - loc_bud
            plans.append(dict(configs=tuple((j, k) for j, (k, _) in zip(js, combo)), loc=tuple(loc),
                              bud=sum(ev["bud"] for _, ev in combo) + loc_bud,
                              eng=sum(ev["eng"] for _, ev in combo) + loc_eng,
                              fE=sum(ev["phiE"] for _, ev in combo) - loc_bud, fU=fU,
                              hours=sum(ev["hours"] for _, ev in combo)))
    return plans


def shared_terms(inst, y, gamma_name):
    y_cur = inst.get("y_cur", frozenset())
    F = {c: strict(inst["caps"][c], "F", "shared capability cost") for c in inst["caps"] if c in y or c in y_cur}
    bud = sum(F[c] for c in y)
    eng = sum(strict(inst["caps"][c], "eng", "shared capability hours") for c in y)
    charge = sum(F[c] * ((c in y) - (c in y_cur)) for c in F)
    gov = strict(inst["policies"][gamma_name], "gov_cost", "governance cost")
    return bud, eng, charge, gov


# =============================================================================
# 7. Multiple-choice knapsack: exhaustive and DP (T-ORC-9)
# =============================================================================
def mck_enum(groups, cap_b, cap_e):
    best, arg = None, None
    for combo in itertools.product(*groups):
        if sum(c[0] for c in combo) > cap_b + TOL or sum(c[1] for c in combo) > cap_e + TOL:
            continue
        v = sum(c[2] for c in combo)
        if best is None or v > best + TOL:
            best, arg = v, combo
    return best, arg


def _mck_dp_core(groups, cap_b, cap_e, beta_b, beta_e, rnd):
    mins_b = [min(c[0] for c in g) for g in groups]
    mins_e = [min(c[1] for c in g) for g in groups]
    rb, re_ = cap_b - sum(mins_b), cap_e - sum(mins_e)
    if rb < -TOL or re_ < -TOL:
        return None, None
    Cb, Ce = int(math.floor(rb / beta_b + 1e-9)), int(math.floor(re_ / beta_e + 1e-9))
    states = {(0, 0): (0.0, ())}
    for gi, g in enumerate(groups):
        new = {}
        for (qb, qe), (val, path) in states.items():
            for ci, c in enumerate(g):
                wb, we = rnd((c[0] - mins_b[gi]) / beta_b), rnd((c[1] - mins_e[gi]) / beta_e)
                nb, ne = qb + wb, qe + we
                if nb > Cb or ne > Ce:
                    continue
                v = val + c[2]
                cur = new.get((nb, ne))
                if cur is None or v > cur[0] + TOL:
                    new[(nb, ne)] = (v, path + (ci,))
        states = new
        if not states:
            return None, None
    val, path = max(states.values(), key=lambda t: t[0])
    return val, tuple(groups[i][ci] for i, ci in enumerate(path))


def mck_dp(groups, cap_b, cap_e, beta_b=1.0, beta_e=1.0):
    """Returns (value, combo, exact, bound). Ceil-rounded weights give a feasible lower bound; floor-rounded
    weights give a relaxation upper bound. exact=True iff all weights are integer multiples of the quanta."""
    def integral(x, beta):
        q = x / beta
        return abs(q - round(q)) < 1e-9
    exact = all(integral(c[0] - min(cc[0] for cc in g), beta_b) and integral(c[1] - min(cc[1] for cc in g), beta_e)
                for g in groups for c in g)
    lo_v, lo_c = _mck_dp_core(groups, cap_b, cap_e, beta_b, beta_e, lambda q: int(math.ceil(q - 1e-9)))
    if exact:
        return lo_v, lo_c, True, 0.0
    hi_v, _ = _mck_dp_core(groups, cap_b, cap_e, beta_b, beta_e, lambda q: int(math.floor(q + 1e-9)))
    bound = None if lo_v is None or hi_v is None else hi_v - lo_v
    return lo_v, lo_c, False, bound


# =============================================================================
# 8. Models
# =============================================================================
def _pareto(cands):
    cands = sorted(cands, key=lambda c: (-c[2], c[0], c[1]))
    kept = []
    for eb, ee, v, *rest in cands:
        if any(kb <= eb + TOL and ke <= ee + TOL and kv >= v - TOL for kb, ke, kv, *_ in kept):
            continue
        kept.append((eb, ee, v, *rest))
    return kept


def _caps_list(inst, allow_shared):
    return sorted(inst["caps"]) if allow_shared else []


def solve_central(inst, gammas=None, allow_shared=True, method="enum", beta=(1.0, 1.0),
                  all_optima=False, forced=None, rho_key="rho", log=None):
    """Model B (allow_shared) or A+ (no sharing). forced: {c: True/False} restricts y."""
    gammas = sorted(gammas or inst["policies"])
    best, optima, dp_exact, dp_bound = None, [], True, 0.0
    for y in _subsets(_caps_list(inst, allow_shared)):
        if forced and any((c in y) != on for c, on in forced.items()):
            continue
        for g in gammas:
            sb, se, charge, gov = shared_terms(inst, y, g)
            rb, re_ = inst["A_bar"]["BUD"] - sb - gov, inst["A_bar"]["ENG"] - se
            if rb < -TOL or re_ < -TOL:
                continue
            per_u = [unit_plans(inst, u, y, g, rho_key=rho_key, log=log) for u in sorted(inst["units"])]
            if any(not p for p in per_u):
                continue
            groups = [[(p["bud"], p["eng"], p["fE"], p) for p in plans] for plans in per_u]
            if all_optima:
                for combo in itertools.product(*groups):
                    if sum(c[0] for c in combo) > rb + TOL or sum(c[1] for c in combo) > re_ + TOL:
                        continue
                    val = sum(c[2] for c in combo) - charge - gov
                    sig = (tuple(sorted(y)), g, tuple(sorted((c[3]["configs"], c[3]["loc"]) for c in combo)))
                    optima.append((val, sig))
                continue
            if method == "dp":
                v, combo, ex, bd = mck_dp(groups, rb, re_, *beta)
                dp_exact &= ex
                dp_bound = max(dp_bound, bd or 0.0) if not ex else dp_bound
            else:
                v, combo = mck_enum(groups, rb, re_)
            if v is None:
                continue
            val = v - charge - gov
            if best is None or val > best["F"] + TOL:
                best = dict(F=val, y=frozenset(y), gamma=g, plans=tuple(c[3] for c in combo))
    if all_optima:
        if not optima:
            return None
        top = max(v for v, _ in optima)
        return dict(F=top, optima=frozenset(s for v, s in optima if v >= top - 1e-7 * max(1, abs(top))))
    if best is not None and method == "dp":
        best.update(dp_exact=dp_exact, dp_bound=dp_bound)
    return best


def unit_response(plans, e_bud, e_eng):
    aff = [p for p in plans if p["bud"] <= e_bud + TOL and p["eng"] <= e_eng + TOL]
    if not aff:
        return None
    if any(p["fU"] is None for p in aff):
        raise FollowerLedgerUnidentified("unit ledger split UNIDENTIFIED")
    m = max(p["fU"] for p in aff)
    tied = [p for p in aff if p["fU"] >= m - TOL * max(1.0, abs(m))]
    return dict(opt=max(p["fE"] for p in tied), pess=min(p["fE"] for p in tied), n_tied=len(tied))


def envelopes_product(plans):
    """Lemma E (v2.1): joins of plan resource vectors are contained in this product set (exact, larger)."""
    return [(b, e) for b in sorted({p["bud"] for p in plans}) for e in sorted({p["eng"] for p in plans})]


def envelopes_lemmaE(plans):
    """Lemma E' (v2.2): it suffices to offer each unit an envelope equal to the resource vector a(x) of one of
    its own plans. For any envelope e with affordable set S and tie set T, every x in T has
    S' = {p : a(p) <= a(x)} subset of S, x stays a follower optimum on S', and the tie set on S' is a subset of
    T: the optimistic value is unchanged (take x optimistic-best in T) and the pessimistic value weakly
    improves, while resource use does not increase."""
    return sorted({(p["bud"], p["eng"]) for p in plans})


def solve_bilevel(inst, gammas=None, envelope_fn=envelopes_lemmaE, allow_shared=True, method="enum",
                  beta=(1.0, 1.0), forced=None, rho_key="rho", log=None):
    """Model C (allow_shared) or C0. Returns {'opt': {...}, 'pess': {...}}."""
    gammas = sorted(gammas or inst["policies"])
    best = {"opt": None, "pess": None}
    exact_all = True
    for y in _subsets(_caps_list(inst, allow_shared)):
        if forced and any((c in y) != on for c, on in forced.items()):
            continue
        for g in gammas:
            sb, se, charge, gov = shared_terms(inst, y, g)
            rb, re_ = inst["A_bar"]["BUD"] - sb - gov, inst["A_bar"]["ENG"] - se
            if rb < -TOL or re_ < -TOL:
                continue
            raw = []
            for u in sorted(inst["units"]):
                plans = unit_plans(inst, u, y, g, rho_key=rho_key, log=log)
                cands = []
                for (eb, ee) in envelope_fn(plans):
                    resp = unit_response(plans, eb, ee)
                    if resp is not None:
                        cands.append((eb, ee, resp))
                raw.append(cands)
            if any(not c for c in raw):
                continue
            for mode in ("opt", "pess"):
                groups = [_pareto([(eb, ee, r[mode]) for eb, ee, r in cands]) for cands in raw]
                if method == "dp":
                    v, combo, ex, _ = mck_dp(groups, rb, re_, *beta)
                    exact_all &= ex
                else:
                    v, combo = mck_enum(groups, rb, re_)
                if v is None:
                    continue
                val = v - charge - gov
                if best[mode] is None or val > best[mode]["F"] + TOL:
                    best[mode] = dict(F=val, y=frozenset(y), gamma=g, env=tuple((c[0], c[1]) for c in combo))
    if method == "dp":
        for mode in best:
            if best[mode]:
                best[mode]["dp_exact"] = exact_all
    return best


def check_comparable(inst, gamma):
    gov = strict(inst["policies"][gamma], "gov_cost", "governance cost")
    b0 = inst.get("B0")
    if not b0 or any(b0.get(u) is None for u in inst["units"]):
        raise MissingInput("B0 UNIDENTIFIED")
    if sum(b0[u]["BUD"] for u in inst["units"]) + gov > inst["A_bar"]["BUD"] + TOL or \
       sum(b0[u]["ENG"] for u in inst["units"]) > inst["A_bar"]["ENG"] + TOL:
        raise NotComparable("sum of status-quo envelopes + governance cost exceeds pooled totals")


def solve_independent(inst, gamma):
    check_comparable(inst, gamma)
    _, _, charge, gov = shared_terms(inst, (), gamma)
    lo = hi = -gov - charge
    for u in sorted(inst["units"]):
        plans = unit_plans(inst, u, (), gamma)
        resp = unit_response(plans, inst["B0"][u]["BUD"], inst["B0"][u]["ENG"])
        if resp is None:
            raise InvalidInput("Model A infeasible for unit " + u)
        lo += resp["pess"]
        hi += resp["opt"]
    return dict(opt=hi, pess=lo)


def architecture_metrics(inst, gamma):
    A = solve_independent(inst, gamma)
    C0 = solve_bilevel(inst, [gamma], allow_shared=False)
    Ap = solve_central(inst, [gamma], allow_shared=False)["F"]
    B = solve_central(inst, [gamma], allow_shared=True)["F"]
    C = solve_bilevel(inst, [gamma], allow_shared=True)
    m = {"A": A, "C0": {k: C0[k]["F"] for k in C0}, "Aplus": Ap, "B": B, "C": {k: C[k]["F"] for k in C}}
    m["VRA"] = {k: m["C0"][k] - A[k] for k in ("opt", "pess")}
    m["DL0"] = {k: Ap - m["C0"][k] for k in ("opt", "pess")}
    m["VCP"] = {k: Ap - A[k] for k in ("opt", "pess")}
    m["VSC"] = B - Ap
    m["DL"] = {k: B - m["C"][k] for k in ("opt", "pess")}
    m["NEV"] = {k: m["C"][k] - A[k] for k in ("opt", "pess")}
    return m


# =============================================================================
# 9. Output contract + missing-data state machine (42 §18; T-MIS-3/4/6)
# =============================================================================
def _canon(x):
    if isinstance(x, float):
        return float(f"{x:.9g}")
    if isinstance(x, (frozenset, set)):
        return sorted((_canon(v) for v in x), key=lambda v: json.dumps(v, sort_keys=True, default=str))
    if isinstance(x, tuple) or isinstance(x, list):
        return [_canon(v) for v in x]
    if isinstance(x, dict):
        return {str(k): _canon(v) for k, v in x.items()}
    if isinstance(x, Ord):
        return f"{x.construct}:{x.code}"
    return x


def result_hash(res):
    return hashlib.sha256(json.dumps(_canon(res), sort_keys=True, default=str).encode()).hexdigest()


def _provenance_summary(inst):
    prov = inst.get("provenance", {})
    counts = {}
    for v in prov.values():
        counts[v] = counts.get(v, 0) + 1
    return counts or {"SIMULATED_ONLY": "all"}


def _drop_unevaluable(inst, flags, details):
    work = copy.deepcopy(inst)
    for j in sorted(work["initiatives"]):
        try:
            for g in work["policies"]:
                if work["policies"][g].get("gov_cost") is None:
                    continue
                ev = jk_eval(work, j, 0, set(), set(), g)
                if not ev["legal"] or not ev["f9"]:
                    flags.add("STATUS_QUO_NONCOMPLIANT")
                    details.setdefault("status_quo_noncompliant", []).append((j, g))
        except MissingInput as e:
            flags.add("UNEVALUABLE_INITIATIVE")
            details.setdefault("unevaluable_initiatives", []).append((j, str(e)))
            del work["initiatives"][j]
            for pol in work["policies"].values():
                for key in [kk for kk in pol["allow"] if kk[0] == j]:
                    del pol["allow"][key]
    return work


def _restricted_log(inst, gammas):
    log = set()
    for g in gammas:
        for y in _subsets(sorted(inst["caps"])):
            for u in inst["units"]:
                try:
                    unit_plans(inst, u, y, g, log=log)
                except MissingInput:
                    pass
    return sorted(log)


def solve(inst, model="B", gammas=None, method="enum", beta=(1.0, 1.0), registry=None):
    """Never raises for data problems: returns a portfolio_result dict with a status from STATUS_ORDER."""
    res = dict(solver_version=SOLVER_VERSION, model=model, status=None, flags=[], details={},
               provenance_summary=_provenance_summary(inst))
    if registry is not None:
        res["scenario_registry_hash"] = registry_hash(registry)
        res["parameter_ranges_hash"] = parameter_ranges_hash(registry)
    flags = set()
    try:
        validate_instance(inst)
    except (InvalidInput, TypeError, KeyError) as e:
        res["status"], res["flags"], res["details"]["error"] = "INVALID_SCHEMA_OR_UNITS", ["INVALID_SCHEMA_OR_UNITS"], str(e)
        return res
    if inst["A_bar"].get("BUD") is None or inst["A_bar"].get("ENG") is None or \
       any(inst["rev_cap"].get(u) is None for u in inst["units"]):
        res["status"] = "REJECT_INSUFFICIENT_IDENTIFIED_INPUTS"
        res["flags"] = [res["status"]]
        return res
    usable = [g for g in sorted(gammas or inst["policies"]) if inst["policies"][g].get("gov_cost") is not None]
    if len(usable) < len(gammas or inst["policies"]):
        flags.add("RESTRICTED_SOLVE")
        res["details"]["excluded_policies"] = sorted(set(gammas or inst["policies"]) - set(usable))
    if not usable:
        res["status"] = "REJECT_INSUFFICIENT_IDENTIFIED_INPUTS"
        res["flags"] = [res["status"]]
        return res
    roles_missing = sorted(r for r, v in inst["lam"].items() if v is None)
    pre = copy.deepcopy(inst)
    if roles_missing:
        pre["_lam_override"] = {r: 0.0 for r in roles_missing}
    work = _drop_unevaluable(pre, flags, res["details"])
    if not work["initiatives"]:
        res["status"] = "REJECT_INSUFFICIENT_IDENTIFIED_INPUTS"
        res["flags"] = sorted(flags | {res["status"]}, key=STATUS_ORDER.index)
        return res
    # lambda missing -> PARTIAL_OBJECTIVE (never a silent zero): the objective is reported WITHOUT the time
    # term as F_E_minus_time together with delta_hours, and the decision is scanned over [0, lambda^U].
    if roles_missing:
        flags.add("PARTIAL_OBJECTIVE")
        res["details"]["lambda_unidentified_roles"] = roles_missing
    # F_c missing -> THRESHOLD_MODE (never F_c = 0, never y_c = 0)
    caps_missing = sorted(c for c, d in work["caps"].items() if d["F"] is None)
    restr = set()
    try:
        if caps_missing:
            flags.add("THRESHOLD_MODE")
            res["details"]["threshold"] = threshold_mode(work, caps_missing, model, usable, method, beta)
        else:
            core = _solve_core(work, model, usable, method, beta, log=restr)
            res.update(core)
            if core.get("infeasible"):
                flags.add("INFEASIBLE")
        if "PARTIAL_OBJECTIVE" in flags and not caps_missing and not res.get("infeasible"):
            res["F_E_minus_time"] = res.pop("F_E", None)
            res["delta_hours"] = res.get("delta_hours")
            res["details"]["lambda_scan"] = lambda_scan(work, model, usable, roles_missing, method, beta)
    except FollowerLedgerUnidentified as e:
        flags.add("FOLLOWER_LEDGER_UNIDENTIFIED")
        res["details"]["error"] = str(e)
    except NotComparable as e:
        flags.add("NOT_COMPARABLE")
        res["details"]["error"] = str(e)
    except MissingInput as e:
        flags.add("REJECT_INSUFFICIENT_IDENTIFIED_INPUTS")
        res["details"]["error"] = str(e)
    except (InvalidInput, TypeError) as e:
        res["status"], res["flags"], res["details"]["error"] = "INVALID_SCHEMA_OR_UNITS", ["INVALID_SCHEMA_OR_UNITS"], str(e)
        return res
    if caps_missing or model == "A":
        restr |= set(_restricted_log(work, usable))
    excluded = sorted(restr, key=str)
    if excluded:
        flags.add("RESTRICTED_SOLVE")
        res["details"]["excluded_configs"] = excluded
    if model in ("B", "Aplus"):
        unused = []
        for j, ini in work["initiatives"].items():
            for k, cfg in ini["configs"].items():
                if k != 0 and cfg.get("impl_x") is None:
                    unused.append((j, k, "impl_x"))
            unused += [(j, c, "tau") for c in ini["rel"] if ini["tau"].get(c) is None]
        unused += [("lam_u", r) for r, v in work["lam_u"].items() if v is None]
        if unused:
            res["details"]["unidentified_inputs_not_used_by_this_model"] = sorted(unused, key=str)
    if not flags:
        flags.add("OK_POINT")
    res["flags"] = sorted(flags, key=STATUS_ORDER.index)
    res["status"] = res["flags"][0]
    res.pop("infeasible", None)
    return res


def _portfolio_hours(inst, sol, gamma):
    total = 0.0
    for p in sol.get("plans", ()):
        total += p["hours"]
    return total


def _solve_core(inst, model, gammas, method, beta, log=None):
    if model == "B" or model == "Aplus":
        sol = solve_central(inst, gammas, allow_shared=(model == "B"), method=method, beta=beta, log=log)
        if sol is None:
            return {"infeasible": True}
        out = dict(F_E=sol["F"], y=sorted(sol["y"]), gamma=sol["gamma"],
                   configs=sorted(jk for p in sol["plans"] for jk in p["configs"]),
                   y_loc=sorted((inst["initiatives"][p["configs"][0][0]]["unit"], c) for p in sol["plans"] for c in p["loc"]),
                   delta_hours=_portfolio_hours(inst, sol, sol["gamma"]))
        if method == "dp":
            out.update(dp_exact=sol["dp_exact"], dp_bound=sol["dp_bound"])
        return out
    if model in ("C", "C0"):
        sol = solve_bilevel(inst, gammas, allow_shared=(model == "C"), method=method, beta=beta, log=log)
        if sol["opt"] is None:
            return {"infeasible": True}
        return dict(F_E={"opt": sol["opt"]["F"], "pess": sol["pess"]["F"]},
                    y={"opt": sorted(sol["opt"]["y"]), "pess": sorted(sol["pess"]["y"])},
                    gamma={"opt": sol["opt"]["gamma"], "pess": sol["pess"]["gamma"]},
                    envelopes={"opt": sol["opt"]["env"], "pess": sol["pess"]["env"]})
    if model == "A":
        if len(gammas) != 1:
            raise InvalidInput("Model A requires exactly one policy")
        a = solve_independent(inst, gammas[0])
        return dict(F_E=a)
    raise InvalidInput(f"unknown model {model}")


def threshold_mode(inst, caps_missing, model, gammas, method, beta):
    """F_c UNIDENTIFIED: report F_c^dagger = sup{F : building c is optimal}, with other missing caps
    forced off (reported as such). Never sets F_c = 0 in the reported solution, never forces y_c = 0."""
    out = {}
    hi_b = inst["A_bar"]["BUD"]
    for c in caps_missing:
        def built(F):
            i = copy.deepcopy(inst)
            i["caps"][c]["F"] = F
            for o in caps_missing:
                if o != c:
                    i["caps"][o]["F"] = 0.0
            forced = {o: False for o in caps_missing if o != c}
            if model in ("C", "C0"):
                s = solve_bilevel(i, gammas, forced=forced, method=method, beta=beta)["pess"]
            else:
                s = solve_central(i, gammas, forced=forced, method=method, beta=beta)
            return s is not None and c in s["y"]
        lo, hi = 0.0, hi_b
        if not built(lo):
            out[c] = dict(F_dagger=None, statement=f"{c} is not built even at F_c=0; F_c^dagger undefined (<0)")
            continue
        if built(hi):
            out[c] = dict(F_dagger=hi, statement=f"{c} built for every F_c <= pooled budget")
            continue
        for _ in range(50):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if built(mid) else (lo, mid)
        out[c] = dict(F_dagger=0.5 * (lo + hi),
                      statement=f"y_{c}* = 1 iff F_{c} <= F_dagger (other missing capabilities forced off)",
                      joint_threshold_computed=len(caps_missing) == 1)
    return out


def lambda_scan(inst, model, gammas, roles, method, beta, grid=5):
    lamU = inst.get("lam_U", {})
    if any(lamU.get(r) is None for r in roles):
        return dict(classification="UNIDENTIFIED", reason="no upper bound lambda^U for some role")
    decisions = []
    for t in range(grid + 1):
        i = copy.deepcopy(inst)
        i["_lam_override"] = {r: lamU[r] * t / grid for r in roles}
        s = _solve_core(i, model, gammas, method, beta)
        decisions.append(json.dumps(_canon({k: s.get(k) for k in ("y", "gamma", "configs", "envelopes")}), sort_keys=True))
    return dict(classification="ROBUST" if len(set(decisions)) == 1 else "FRAGILE",
                distinct_decisions=len(set(decisions)), grid_points=grid + 1,
                note="single pre-registered interval [0, lambda^U]; a change inside it is FRAGILE")


# =============================================================================
# 10. Model D gate (T-ORC-12)
# =============================================================================
TRI_LEVEL_CALLS = {"n": 0}


def best_response_rho(cfg):
    rho = {}
    for key, utils in cfg["U"].items():
        m = max(utils.values())
        arg = [r for r, v in utils.items() if v >= m - TOL]
        rho[key] = {r: (1.0 / len(arg) if r in arg else 0.0) for r in utils}
    return rho


def solve_model_D(inst, evidence, gammas=None):
    """evidence: dict T1..T4 -> bool (documentary evidence). T5 is computed. Any FAIL -> not identified."""
    gate = {t: bool(evidence.get(t, False)) for t in ("T1", "T2", "T3", "T4")}
    if not all(gate.values()):
        return dict(status="MODEL_D_NOT_IDENTIFIED", gate=gate, T5=None)
    br = copy.deepcopy(inst)
    for ini in br["initiatives"].values():
        for k, cfg in ini["configs"].items():
            if "U" in cfg:
                cfg["rho_BR"] = best_response_rho(cfg)
            else:
                cfg["rho_BR"] = cfg["rho"]
    base = solve_bilevel(inst, gammas)
    alt = solve_bilevel(br, gammas, rho_key="rho_BR")
    sig = lambda s: (sorted(s["y"]), s["gamma"], s["env"])
    gate["T5"] = sig(base["pess"]) != sig(alt["pess"]) or sig(base["opt"]) != sig(alt["opt"])
    if not gate["T5"]:
        return dict(status="MODEL_D_NOT_IDENTIFIED", gate=gate, T5=False)
    TRI_LEVEL_CALLS["n"] += 1
    return dict(status="MODEL_D_EXECUTED", gate=gate, result={m: alt[m]["F"] for m in alt})


# =============================================================================
# 11. Robustness: registry, Lemma R, robust feasibility, MaxRegret, VOI (T-SEN-3/4/6/7)
# =============================================================================
def registry_hash(reg):
    return hashlib.sha256(json.dumps(_canon(reg), sort_keys=True, default=str).encode()).hexdigest()


def parameter_ranges_hash(reg):
    ranges = {g: [b for b in grp["blocks"]] for g, grp in reg["groups"].items()}
    return hashlib.sha256(json.dumps(_canon(ranges), sort_keys=True, default=str).encode()).hexdigest()


def verify_registry(result, reg):
    return result.get("scenario_registry_hash") == registry_hash(reg) and \
        result.get("parameter_ranges_hash") == parameter_ranges_hash(reg)


def _get(inst, path):
    x = inst
    for p in path:
        x = x[p]
    return x


def block_vertices(block):
    if block["kind"] == "scale":
        return [("scale", block["L"]), ("scale", block["U"])]
    if block["kind"] == "prob":
        return [("vertex", i) for i in range(len(block["vertices"]))]
    raise InvalidInput("unknown block kind")


def block_sample(block, rng):
    if block["kind"] == "scale":
        return ("scale", rng.uniform(block["L"], block["U"]))
    w = [rng.expovariate(1.0) for _ in block["vertices"]]
    s = sum(w)
    return ("mix", tuple(wi / s for wi in w))


def apply_theta(inst, blocks, values):
    i = copy.deepcopy(inst)
    for b, (kind, val) in zip(blocks, values):
        if kind == "scale":
            for path, field in b["targets"]:
                cell = _get(i, path)
                cell[field] = _get(inst, path)[field] * val
        else:
            weights = [1.0 if n == val else 0.0 for n in range(len(b["vertices"]))] if kind == "vertex" else list(val)
            keys = b["vertices"][0].keys()
            parent = _get(i, b["path"][:-1])
            parent[b["path"][-1]] = {k: sum(w * v[k] for w, v in zip(weights, b["vertices"])) for k in keys}
    return i


def theta_grid(blocks):
    return [tuple(v) for v in itertools.product(*[block_vertices(b) for b in blocks])]


def enumerate_portfolios(inst, gamma, allow_shared=True):
    """All feasible fixed portfolios (y, gamma, plans) for Model B at the given instance."""
    out = []
    for y in _subsets(_caps_list(inst, allow_shared)):
        sb, se, charge, gov = shared_terms(inst, y, gamma)
        rb, re_ = inst["A_bar"]["BUD"] - sb - gov, inst["A_bar"]["ENG"] - se
        per_u = [unit_plans(inst, u, y, gamma) for u in sorted(inst["units"])]
        for combo in itertools.product(*per_u):
            if sum(p["bud"] for p in combo) <= rb + TOL and sum(p["eng"] for p in combo) <= re_ + TOL:
                out.append((tuple(sorted(y)), tuple((p["configs"], p["loc"]) for p in combo)))
    return out


def portfolio_slacks(inst, gamma, d, rho_key="rho"):
    """Static feasibility flag and constraint slacks (>= 0 feasible) of a FIXED portfolio. Each slack is
    multilinear in the theta blocks, so its worst case over a product polytope is attained at a vertex."""
    y, units = d
    sb, se, charge, gov = shared_terms(inst, y, gamma)
    total, bud, eng, static_ok, sl = -charge - gov, sb + gov, se, True, {}
    for configs, loc in units:
        u = inst["initiatives"][configs[0][0]]["unit"]
        rev = 0.0
        for j, k in configs:
            ev = jk_eval(inst, j, k, set(y), set(loc), gamma, rho_key)
            static_ok &= ev["static_ok"]
            sl[("F9", j)] = inst["policies"][gamma]["ebar"][j] - ev["sev"]
            total += ev["phiE"]; bud += ev["bud"]; eng += ev["eng"]; rev += ev["rev"]
        loc_b = sum(inst["loc_caps"][(u, c)]["F"] for c in loc)
        total -= loc_b; bud += loc_b; eng += sum(inst["loc_caps"][(u, c)]["eng"] for c in loc)
        sl[("REV", u)] = inst["rev_cap"][u] - rev
    sl[("BUD",)] = inst["A_bar"]["BUD"] - bud
    sl[("ENG",)] = inst["A_bar"]["ENG"] - eng
    return static_ok, sl, total


def evaluate_portfolio(inst, gamma, d, rho_key="rho"):
    """Value of a FIXED portfolio d at instance inst (Model B); None if infeasible there."""
    static_ok, sl, total = portfolio_slacks(inst, gamma, d, rho_key)
    if not static_ok or min(sl.values()) < -TOL:
        return None
    return total


def theta_instances(inst, blocks):
    return [(th, apply_theta(inst, blocks, th)) for th in theta_grid(blocks)]


def robust_feasibility(inst, gamma, d, blocks, tinst=None):
    """ROBUSTLY_FEASIBLE: every constraint holds at every vertex (worst case of a multilinear slack is a
    vertex, so this certifies all theta). INFEASIBLE: statically infeasible, or some single constraint is
    violated at every vertex (its best case is also a vertex, so it is violated for all theta).
    Otherwise CONDITIONALLY_FEASIBLE (feasible for some theta only; excluded from ROBUST candidate sets)."""
    tinst = tinst or theta_instances(inst, blocks)
    per = [portfolio_slacks(i, gamma, d) for _, i in tinst]
    if not all(p[0] for p in per):
        return "INFEASIBLE"
    keys = per[0][1].keys()
    if all(min(p[1].values()) >= -TOL for p in per):
        return "ROBUSTLY_FEASIBLE"
    if any(all(p[1][k] < -TOL for p in per) for k in keys):
        return "INFEASIBLE"
    return "CONDITIONALLY_FEASIBLE"


def design_response_analysis(inst, gamma):
    """Q6: d^D chosen under rho_design; evaluated under actual rho (42 §14 Q6)."""
    dD = solve_central(inst, [gamma], rho_key="rho_design")
    dR = solve_central(inst, [gamma])
    if dD is None or dR is None:
        return dict(status="INFEASIBLE")
    port = (tuple(sorted(dD["y"])), tuple((p["configs"], p["loc"]) for p in dD["plans"]))
    real = evaluate_portfolio(inst, gamma, port)
    if real is None:
        return dict(status="DESIGN_INFEASIBLE_UNDER_RESPONSE", design_value=dD["F"])
    return dict(status="OK_POINT", VRG=dD["F"] - real, design_response_regret=dR["F"] - real)


def solve_robust(inst, gamma, registry, group):
    """Model B robust solve over one registered group: candidate set = robustly feasible portfolios;
    returns minimax-regret decision, its MaxRegret and the whole-portfolio Lemma R certificate."""
    blocks = registry["groups"][group]["blocks"]
    tinst = theta_instances(inst, blocks)
    cands = [d for d in enumerate_portfolios(inst, gamma)
             if robust_feasibility(inst, gamma, d, blocks, tinst) == "ROBUSTLY_FEASIBLE"]
    if not cands:
        return dict(status="INFEASIBLE", solver_version=SOLVER_VERSION,
                    scenario_registry_hash=registry_hash(registry), parameter_ranges_hash=parameter_ranges_hash(registry))
    thetas = theta_grid(blocks)
    vals = regret_table(inst, gamma, cands, thetas, blocks)
    mr = {d: max_regret(vals, d) for d in cands}
    dstar = min(cands, key=lambda d: (mr[d], json.dumps(_canon(d))))
    cert = lemma_r_check(inst, gamma, dstar, cands, blocks)
    return dict(status="OK_INTERVAL", solver_version=SOLVER_VERSION, decision=dstar, max_regret=mr[dstar],
                whole_portfolio_robust=cert["robust"], n_candidates=len(cands),
                scenario_registry_hash=registry_hash(registry), parameter_ranges_hash=parameter_ranges_hash(registry),
                provenance_summary=_provenance_summary(inst))


def lemma_r_check(inst, gamma, d_star, competitors, blocks, model="B", scope="whole_portfolio"):
    """Exact vertex check of 'd_star is optimal for every theta in the product polytope' (42 §13.3).
    Scope-guarded: only Model B, only a fixed whole portfolio."""
    if model != "B" or scope != "whole_portfolio":
        raise ScopeError("Lemma R is proven only for Model B and fixed whole portfolios")
    worst = []
    for th in theta_grid(blocks):
        i = apply_theta(inst, blocks, th)
        fs = evaluate_portfolio(i, gamma, d_star)
        for d in competitors:
            fd = evaluate_portfolio(i, gamma, d)
            if fs is None or fd is None:
                raise ScopeError("Lemma R requires a robustly feasible candidate set")
            worst.append((fs - fd, d, th))
    m = min(worst, key=lambda t: t[0])
    return dict(robust=m[0] >= -1e-7, min_gap=m[0], witness=m[1:] if m[0] < -1e-7 else None)


def regret_table(inst, gamma, candidates, thetas, blocks):
    vals = {}
    for th in thetas:
        i = apply_theta(inst, blocks, th)
        row = {d: evaluate_portfolio(i, gamma, d) for d in candidates}
        if any(v is None for v in row.values()):
            raise ScopeError("candidate set must be robustly feasible over the registered thetas")
        vals[th] = row
    return vals


def max_regret(vals, d, thetas=None):
    thetas = thetas or list(vals)
    return max(max(vals[th].values()) - vals[th][d] for th in thetas)


def minimax_regret(vals, candidates, thetas=None):
    return min(max_regret(vals, d, thetas) for d in candidates)


def voi_table(vals, candidates, blocks):
    """Value of identification per block: MMR(all) - max_v MMR(theta restricted to block value v)."""
    thetas = list(vals)
    mmr_all = minimax_regret(vals, candidates, thetas)
    out = {}
    for bi, b in enumerate(blocks):
        per_v = {}
        for v in block_vertices(b):
            sub = [th for th in thetas if th[bi] == v]
            per_v[json.dumps(_canon(v), sort_keys=True)] = minimax_regret(vals, candidates, sub)
        out[b["name"]] = dict(mmr_all=mmr_all, mmr_given_value=per_v, voi=mmr_all - max(per_v.values()))
    return out


def robustness_class(groups, element):
    per_g = {g: set.intersection(*[{element(s) for s in theta_sols} for theta_sols in sols])
             for g, sols in groups.items()}
    if set.intersection(*per_g.values()):
        return "ROBUST"
    if all(per_g.values()):
        return "CONDITIONAL"
    return "FRAGILE"


# =============================================================================
# 12. Governance decomposition (42 §14 Q3)
# =============================================================================
ENABLE_KEYS = ("allow", "allow_loc", "G", "must", "forbid")
REQ_KEYS = ("H_req", "WI_req", "EA_req", "G_req", "ebar")


def hybrid_policy(inst, name, allow_from, req_from, cost_from):
    pols = inst["policies"]
    h = {k: copy.deepcopy(pols[allow_from][k]) for k in ENABLE_KEYS}
    h.update({k: copy.deepcopy(pols[req_from][k]) for k in REQ_KEYS})
    h["gov_cost"] = pols[cost_from]["gov_cost"]
    new = copy.deepcopy(inst)
    new["policies"][name] = h
    return new


def governance_decomposition(inst, gamma, gamma0):
    F = lambda i, g: solve_central(i, [g])["F"]
    base = F(inst, gamma0)
    f1 = F(hybrid_policy(inst, "_EE", gamma, gamma0, gamma0), "_EE")
    f2 = F(hybrid_policy(inst, "_RE", gamma, gamma, gamma0), "_RE")
    full = F(inst, gamma)
    return dict(VG=full - base, EE=f1 - base, RE=f2 - f1, CE=full - f2)


# =============================================================================
# 13. Synthetic instances (SIMULATED_ONLY)
# =============================================================================
def make_instance(seed, aligned=True, codes=None, money=1.0, period=1.0, delta_shared=None, n_units=2,
                  n_init=2, integer=False):
    rng = random.Random(seed)
    codes = codes or DEFAULT_CODES
    o = lambda c, l: O(c, l, codes)
    rnd = (lambda x: float(round(x))) if integer else (lambda x: x)
    roles, Z, W = ("junior", "senior"), ("flag", "noflag"), ("ok", "err")
    caps = {"c_model": dict(F=rnd(money * period * rng.uniform(20, 60)), eng=rnd(period * rng.uniform(5, 15))),
            "c_eval": dict(F=rnd(money * period * rng.uniform(10, 40)), eng=rnd(period * rng.uniform(3, 10)))}
    units = [f"U{i+1}" for i in range(n_units)]
    loc_caps = {(u, c): dict(F=rnd(caps[c]["F"] * rng.uniform(0.6, 0.9)), eng=rnd(caps[c]["eng"] * rng.uniform(0.6, 0.9)))
                for u in units for c in caps}
    dS = {c: money * period * rng.uniform(0, 6) for c in caps}
    if delta_shared:
        dS.update({c: money * period * v for c, v in delta_shared.items()})
    dL = {c: money * period * rng.uniform(0, 3) for c in caps}
    lvl = lambda a, h, wi, ea, m: dict(A=o("A", a), H=o("H", h), WI=o("WI", wi), EA=o("EA", ea), m=m)
    cfg_specs = {0: (lvl(0, 3, 0, 0, "HumanOnly"), set()),
                 1: (lvl(2, 2, 2, 1, "AI->Human"), {"c_model"}),
                 2: (lvl(3, 3, 3, 2, "BoundedExecution"), {"c_model", "c_eval"})}
    patterns = [frozenset(p) for p in itertools.chain.from_iterable(
        itertools.product(*[[(c, s) for s in ("S", "L")] for c in sub]) for sub in _subsets(sorted(caps)))]
    initiatives = {}
    for u in units:
        for jj in range(n_init):
            j = f"{u}_j{jj}"
            kap = o("K", rng.choice([0, 1, 2]))
            N = period * rng.choice([50, 80, 120])
            configs = {}
            for k, (attrs, pre) in cfg_specs.items():
                err = {0: 0.10, 1: rng.uniform(0.04, 0.12), 2: rng.uniform(0.02, 0.15)}[k]
                P = {("flag", "err"): err * 0.7, ("noflag", "err"): err * 0.3,
                     ("flag", "ok"): 0.5 - err * 0.7, ("noflag", "ok"): 0.5 - err * 0.3}
                if k == 0:
                    rho = {(z, r): {"NA": 1.0} for z in Z for r in roles}
                    allowed = {"NA"}
                    rho_design = rho
                else:
                    rho, rho_design = {}, {}
                    for z in Z:
                        for r in roles:
                            a = rng.uniform(0.3, 0.7)
                            b = rng.uniform(0.0, 1 - a)
                            rho[(z, r)] = {"Use": a, "Verify": b, "Reject": 1 - a - b}
                            rho_design[(z, r)] = {"Use": 0.0, "Verify": 1.0, "Reject": 0.0} if k == 1 else {"Use": 1.0, "Verify": 0.0, "Reject": 0.0}
                    allowed = set(RESPONSES) - {"NA"}
                path = {}
                for r in roles:
                    for z in Z:
                        for w in W:
                            for resp in (["NA"] if k == 0 else ["Use", "Verify", "Reject"]):
                                bad = (w == "err") and resp in ("Use", "NA")
                                caught = (w == "err") and resp == "Verify"
                                loss = money * rng.uniform(5, 15) if bad else (money * 1.0 if caught else 0.0)
                                ext = money * rng.uniform(0, 4) if (bad and not aligned) else 0.0
                                tt = {"NA": 1.0, "Use": 0.2, "Verify": 0.6, "Reject": 1.1}[resp]
                                path[(r, z, w, resp)] = dict(
                                    v_u=money * rng.uniform(0, 2) * (k > 0), v_x=0.0, l_u=loss, l_x=ext,
                                    c_u=(0.0 if integer else money * 0.1) * (k > 0), c_x=0.0,
                                    t=tt, t_rev=tt * 0.5, I_sev=0.02 if bad else 0.0)
                base_impl = money * period * rng.uniform(12, 25) * k
                base_eng = period * rng.uniform(2, 8) * k
                impl, engt = {}, {}
                for pat in patterns:
                    red = sum(dS[c] if s == "S" else dL[c] for c, s in pat)
                    impl[pat] = rnd(max(0.0, base_impl - red * k))
                    engt[pat] = rnd(base_eng)
                configs[k] = dict(attrs, pre=pre, legal=1, effH=1, FB=1, cons=1, impl=impl, eng=engt, impl_x=0.0,
                                  pi={"junior": 0.6, "senior": 0.4}, P=P, rho=rho, rho_design=rho_design,
                                  allowed_r=allowed, path=path)
            initiatives[j] = dict(unit=u, kappa=kap, N={k: N for k in cfg_specs}, rel=sorted(caps), configs=configs,
                                  tau={c: 0.0 for c in caps},
                                  R_state={pat: o("R", 3) for pat in patterns},
                                  D_state={pat: o("D", 3) for pat in patterns})

    def req_table(level_fn, construct):
        return {(o("A", a), o("K", kk)): o(construct, level_fn(a, kk)) for a in range(4) for kk in range(3)}

    allow_all = {(j, k): 1 for j in initiatives for k in cfg_specs}
    base_pol = dict(
        gov_cost=money * period * 5.0, allow=allow_all, allow_loc={(u, c): 1 for u in units for c in caps},
        G={j: o("G", 2) for j in initiatives},
        H_req=req_table(lambda a, kk: 2 if a >= 2 else 0, "H"),
        WI_req=req_table(lambda a, kk: 2 if a >= 2 else 0, "WI"),
        EA_req=req_table(lambda a, kk: 1 if a >= 2 else 0, "EA"),
        G_req=req_table(lambda a, kk: 2 if a >= 3 else 1, "G"),
        ebar={j: period * 10.0 for j in initiatives}, must=set(), forbid=set())
    strict_pol = copy.deepcopy(base_pol)
    strict_pol["gov_cost"] = money * period * 12.0
    strict_pol["EA_req"] = req_table(lambda a, kk: 2 if a >= 2 else 0, "EA")
    g0 = copy.deepcopy(base_pol)
    g0["gov_cost"] = 0.0
    g0["allow"] = {(j, k): (0 if k == 2 else 1) for j in initiatives for k in cfg_specs}
    return dict(units=units, caps=caps, loc_caps=loc_caps, initiatives=initiatives,
                policies={"g0": g0, "g_base": base_pol, "g_strict": strict_pol}, y_cur=frozenset(),
                A_bar={"BUD": money * period * 260.0 * n_units / 2, "ENG": period * 70.0 * n_units / 2},
                B0={u: {"BUD": money * period * 100.0, "ENG": period * 30.0} for u in units},
                rev_cap={u: period * 1e6 for u in units},
                lam={"junior": money * 0.8, "senior": money * 1.5},
                lam_u={"junior": money * 0.8, "senior": money * 1.5},
                lam_U={"junior": money * 3.0, "senior": money * 4.0},
                R_req={o("A", a): o("R", min(a, 2)) for a in range(4)},
                D_req={o("A", a): o("D", min(a, 2)) for a in range(4)},
                codes=codes, provenance={})


def hand_instance(u2_impl, u2_lx, ea_levels=(1, 1), ea_req=0, delta=0.0, u1_base=5.0, u2_base=None):
    """Hand-computable fixture (45 T-ORC-8). SIMULATED_ONLY."""
    def cell(v_u=0.0, l_x=0.0):
        return dict(v_u=v_u, v_x=0.0, l_u=0.0, l_x=l_x, c_u=0.0, c_x=0.0, t=0.0, t_rev=0.0, I_sev=0.0)

    def cfg(k, v_u, l_x, impl, ea):
        resp = "NA" if k == 0 else "Use"
        return dict(A=O("A", 0 if k == 0 else 1), H=O("H", 3), WI=O("WI", 0 if k == 0 else 1),
                    EA=O("EA", 0 if k == 0 else ea), m="HumanOnly" if k == 0 else "AI->Human",
                    pre=set() if k == 0 else {"c"}, legal=1, effH=1, FB=1, cons=1,
                    impl={frozenset(): impl, frozenset({("c", "S")}): impl},
                    eng={frozenset(): 0.0, frozenset({("c", "S")}): 0.0}, impl_x=0.0,
                    pi={"r": 1.0}, P={("n", "ok"): 1.0}, rho={("n", "r"): {resp: 1.0}},
                    allowed_r={resp}, path={("r", "n", "ok", resp): cell(v_u, l_x)})
    u1_impl = max(0.0, u1_base - delta)
    u2i = u2_impl if u2_base is None else max(0.0, u2_base - delta)
    pats = [frozenset(), frozenset({("c", "S")})]
    ini = {
        "U1_j": dict(unit="U1", kappa=O("K", 0), N={0: 10.0, 1: 10.0}, rel=["c"], tau={"c": 0.0},
                     configs={0: cfg(0, 0.0, 0.0, 0.0, 0), 1: cfg(1, 3.0, 0.0, u1_impl, ea_levels[0])},
                     R_state={p: O("R", 3) for p in pats}, D_state={p: O("D", 3) for p in pats}),
        "U2_j": dict(unit="U2", kappa=O("K", 0), N={0: 10.0, 1: 10.0}, rel=["c"], tau={"c": 0.0},
                     configs={0: cfg(0, 0.0, 0.0, 0.0, 0), 1: cfg(1, 2.0, u2_lx, u2i, ea_levels[1])},
                     R_state={p: O("R", 3) for p in pats}, D_state={p: O("D", 3) for p in pats}),
    }

    def req(lvl_fn, c):
        return {(O("A", a), O("K", kk)): O(c, lvl_fn(a)) for a in range(4) for kk in range(3)}

    def pol(ea):
        return dict(gov_cost=0.0, allow={(j, k): 1 for j in ini for k in (0, 1)}, allow_loc={},
                    G={j: O("G", 3) for j in ini}, H_req=req(lambda a: 0, "H"), WI_req=req(lambda a: 0, "WI"),
                    EA_req=req(lambda a: ea if a >= 1 else 0, "EA"), G_req=req(lambda a: 0, "G"),
                    ebar={j: 1.0 for j in ini}, must=set(), forbid=set())

    return dict(units=["U1", "U2"], caps={"c": dict(F=10.0, eng=0.0)}, loc_caps={}, initiatives=ini,
                policies={"g": pol(0), "g_req": pol(ea_req)}, y_cur=frozenset(),
                A_bar={"BUD": 100.0, "ENG": 100.0},
                B0={"U1": {"BUD": 50.0, "ENG": 50.0}, "U2": {"BUD": 50.0, "ENG": 50.0}},
                rev_cap={"U1": 1.0, "U2": 1.0}, lam={"r": 0.0}, lam_u={"r": 0.0}, lam_U={"r": 0.0},
                R_req={O("A", a): O("R", 0) for a in range(4)}, D_req={O("A", a): O("D", 0) for a in range(4)},
                codes=DEFAULT_CODES, provenance={})


# =============================================================================
# 14. Tests (45 v2.2 inventory). Each returns (test_id, verdict_key, message) or raises AssertionError.
# =============================================================================
def close(a, b, tol=1e-7):
    return math.isclose(a, b, rel_tol=tol, abs_tol=tol)


def le(a, b):
    return a <= b + 1e-7


def _expect_status(res, status):
    assert res["status"] == status, (res["status"], res.get("flags"), res.get("details"))


# ---- V3: schema / units --------------------------------------------------------------------
def t_sch5_typed_units():
    te, ep, he, th = Q.of(2.0, "TWD/event"), Q.of(10.0, "events/period"), Q.of(0.5, "hours/event"), Q.of(4.0, "TWD/hour")
    assert (te * ep).unit_is("TWD/period") and close((te * ep).value, 20.0)
    assert (he * ep).unit_is("hours/period")
    assert (he * th).unit_is("TWD/event")
    for bad in (lambda: te + Q.of(1.0, "TWD/period"), lambda: he + te, lambda: ep - Q.of(1.0, "incidents/period"),
                lambda: Q.of(1.0, "hours/period") <= Q.of(1.0, "TWD/period")):
        try:
            bad()
            raise AssertionError("dimension mismatch not rejected")
        except InvalidInput:
            pass
    # typed recomputation of phi_E equals the float path; a mis-typed formula is rejected
    inst = make_instance(3)
    for j in sorted(inst["initiatives"])[:2]:
        for k in (1, 2):
            ini, cfg, cfg0 = inst["initiatives"][j], inst["initiatives"][j]["configs"][k], inst["initiatives"][j]["configs"][0]
            ys = {"c_model", "c_eval"}

            def gq(c):
                tot = Q.of(0.0, "TWD/event")
                for role, pr in c["pi"].items():
                    for (z, w), pz in c["P"].items():
                        for r, pr_r in c["rho"][(z, role)].items():
                            if pr_r <= 0:
                                continue
                            x = c["path"][(role, z, w, r)]
                            f = (Q.of(x["v_u"], "TWD/event") + Q.of(x["v_x"], "TWD/event") - Q.of(x["l_u"], "TWD/event")
                                 - Q.of(x["l_x"], "TWD/event") - Q.of(x["c_u"], "TWD/event") - Q.of(x["c_x"], "TWD/event")
                                 - Q.of(inst["lam"][role], "TWD/hour") * Q.of(x["t"], "hours/event"))
                            tot = tot + Q.of(pr * pz * pr_r, "probability") * f
                return tot
            key = source_key(ini["rel"], ys, set())
            phi_q = Q.of(ini["N"][k], "events/period") * gq(cfg) - Q.of(ini["N"][0], "events/period") * gq(cfg0) \
                - Q.of(cfg["impl"][key], "TWD/period")
            assert phi_q.unit_is("TWD/period")
            assert close(phi_q.value, jk_eval(inst, j, k, ys, set(), "g_base")["phiE"])
            try:
                gq(cfg) - Q.of(cfg["impl"][key], "TWD/period")      # per-event minus per-period: must fail
                raise AssertionError("mis-typed formula accepted")
            except InvalidInput:
                pass
    return ("T-SCH-5", "typed units PASS",
            "TWD/event x events/period = TWD/period; hours/event x events/period = hours/period; hours/event x TWD/hour = TWD/event; "
            "4 mismatches rejected; typed phi_E == float phi_E on 4 (j,k); per-event minus per-period rejected")


def t_sch6_omega_guard():
    inst = make_instance(2)
    j = sorted(inst["initiatives"])[0]
    cfg = inst["initiatives"][j]["configs"][1]
    ok = copy.deepcopy(inst)
    ok["initiatives"][j]["configs"][1]["rho"][("flag", "junior", "S")] = {"Use": 1.0}  # capability-state key is legal
    assert validate_instance(ok)
    bad_keys = [("flag", "err", "junior"), ("err", "junior"), ("flag", "junior", "err")]
    for bk in bad_keys:
        b = copy.deepcopy(inst)
        b["initiatives"][j]["configs"][1]["rho"][bk] = {"Use": 1.0}
        _expect_status(solve(b, "B", ["g_base"]), "INVALID_SCHEMA_OR_UNITS")
    b = copy.deepcopy(inst)
    b["initiatives"][j]["configs"][1]["P"] = {("flag", "flag"): 1.0}            # signal/outcome labels collide
    _expect_status(solve(b, "B", ["g_base"]), "INVALID_SCHEMA_OR_UNITS")
    return ("T-SCH-6", "explicit omega leakage guard PASS",
            "rho(r|k,z,role[,capstate]) accepted; 3 keys containing omega and 1 label collision rejected as INVALID_SCHEMA_OR_UNITS")


NUMERIC_SITES = [
    ("caps.F", lambda i: (i["caps"]["c_model"], "F")),
    ("loc_caps.F", lambda i: (i["loc_caps"][("U1", "c_model")], "F")),
    ("A_bar.BUD", lambda i: (i["A_bar"], "BUD")),
    ("rev_cap", lambda i: (i["rev_cap"], "U1")),
    ("B0.BUD", lambda i: (i["B0"]["U1"], "BUD")),
    ("lam", lambda i: (i["lam"], "junior")),
    ("gov_cost", lambda i: (i["policies"]["g_base"], "gov_cost")),
    ("ebar", lambda i: (i["policies"]["g_base"]["ebar"], "U1_j0")),
    ("N", lambda i: (i["initiatives"]["U1_j0"]["N"], 1)),
    ("tau", lambda i: (i["initiatives"]["U1_j0"]["tau"], "c_model")),
    ("impl", lambda i: (i["initiatives"]["U1_j0"]["configs"][1]["impl"], frozenset({("c_model", "S")}))),
    ("eng", lambda i: (i["initiatives"]["U1_j0"]["configs"][1]["eng"], frozenset({("c_model", "S")}))),
    ("impl_x", lambda i: (i["initiatives"]["U1_j0"]["configs"][1], "impl_x")),
    ("pi", lambda i: (i["initiatives"]["U1_j0"]["configs"][1]["pi"], "junior")),
    ("P", lambda i: (i["initiatives"]["U1_j0"]["configs"][1]["P"], ("flag", "ok"))),
    ("rho", lambda i: (i["initiatives"]["U1_j0"]["configs"][1]["rho"][("flag", "junior")], "Use")),
    ("path.v_u", lambda i: (next(iter(i["initiatives"]["U1_j0"]["configs"][1]["path"].values())), "v_u")),
    ("path.t", lambda i: (next(iter(i["initiatives"]["U1_j0"]["configs"][1]["path"].values())), "t")),
    ("path.I_sev", lambda i: (next(iter(i["initiatives"]["U1_j0"]["configs"][1]["path"].values())), "I_sev")),
]


def t_sch7_nonfinite():
    n = 0
    for name, site in NUMERIC_SITES:
        for bad in (float("nan"), float("inf"), float("-inf")):
            inst = make_instance(4)
            d, k = site(inst)
            d[k] = bad
            _expect_status(solve(inst, "B", ["g_base"]), "INVALID_SCHEMA_OR_UNITS")
            n += 1
    inst = make_instance(4)
    inst["initiatives"]["U1_j0"]["configs"][1]["P"][("flag", "ok")] = 1.5
    _expect_status(solve(inst, "B", ["g_base"]), "INVALID_SCHEMA_OR_UNITS")
    return ("T-SCH-7", "NaN/inf rejection PASS", f"{n} mutations (NaN, +inf, -inf x {len(NUMERIC_SITES)} numeric classes) and 1 out-of-range probability rejected")


# ---- F5e ------------------------------------------------------------------------------------
def t_alg1_f5e():
    def setup(r_lvl=3, d_lvl=3, codes=None):
        inst = make_instance(6, codes=codes)
        j = "U1_j0"
        key = frozenset({("c_model", "S")})
        inst["initiatives"][j]["R_state"][key] = O("R", r_lvl, inst["codes"])
        inst["initiatives"][j]["D_state"][key] = O("D", d_lvl, inst["codes"])
        return inst, j, key

    def feas(inst, j):
        return jk_eval(inst, j, 1, {"c_model"}, set(), "g_base")["feasible"]
    inst, j, _ = setup(3, 3)
    assert feas(inst, j)                                                    # R pass / D pass (A=2 needs >=2)
    inst, j, _ = setup(1, 3)
    assert not feas(inst, j)                                                # R fail
    inst, j, _ = setup(3, 1)
    assert not feas(inst, j)                                                # D fail
    inst, j, key = setup(3, 3)
    inst["initiatives"][j]["R_state"][key] = None
    res = solve(inst, "B", ["g_base"])
    assert "RESTRICTED_SOLVE" in res["flags"] and any(e[:2] == (j, 1) for e in res["details"]["excluded_configs"])
    inst2, j2, _ = setup(3, 3)
    inst2["initiatives"][j2]["D_state"][frozenset()] = None                 # status-quo pattern missing
    res2 = solve(inst2, "B", ["g_base"])
    assert "UNEVALUABLE_INITIATIVE" in res2["flags"]
    inst3, j3, key3 = setup(3, 3)
    del inst3["initiatives"][j3]["R_state"][key3]                           # absent cell, not just None
    assert "RESTRICTED_SOLVE" in solve(inst3, "B", ["g_base"])["flags"]
    # relabel R/D (and every other ordinal) by a strictly increasing map: same feasibility and same solution
    codes = {k: {0: -5.0, 1: 0.1, 2: 0.11, 3: 77.0} for k in DEFAULT_CODES}
    for lv in ((3, 3), (1, 3), (3, 1)):
        a, ja, _ = setup(*lv)
        b, jb, _ = setup(*lv, codes=codes)
        assert feas(a, ja) == feas(b, jb)
        sa, sb = solve(a, "B", ["g_base"]), solve(b, "B", ["g_base"])
        assert sa["configs"] == sb["configs"] and close(sa["F_E"], sb["F_E"])
    return ("T-ALG-1", "F5e PASS", "R pass/D pass feasible; R fail and D fail infeasible; missing R -> RESTRICTED_SOLVE; "
            "missing D on status-quo pattern -> UNEVALUABLE_INITIATIVE; absent cell not defaulted; relabel-invariant")


# ---- State machine / output contract -------------------------------------------------------
def t_state_machine():
    seen = {}
    base = make_instance(5)
    r = solve(base, "B", ["g_base"]); _expect_status(r, "OK_POINT"); seen["OK_POINT"] = 1
    for key in ("status", "flags", "model", "solver_version", "provenance_summary", "F_E", "y", "configs", "delta_hours"):
        assert key in r, key
    i = copy.deepcopy(base); i["A_bar"]["BUD"] = None
    _expect_status(solve(i, "B", ["g_base"]), "REJECT_INSUFFICIENT_IDENTIFIED_INPUTS"); seen["REJECT_INSUFFICIENT_IDENTIFIED_INPUTS"] = 1
    i = copy.deepcopy(base); i["caps"]["c_model"]["F"] = float("nan")
    _expect_status(solve(i, "B", ["g_base"]), "INVALID_SCHEMA_OR_UNITS"); seen["INVALID_SCHEMA_OR_UNITS"] = 1
    i = copy.deepcopy(base); i["B0"]["U1"]["BUD"] = 1e6
    _expect_status(solve(i, "A", ["g_base"]), "NOT_COMPARABLE"); seen["NOT_COMPARABLE"] = 1
    i = copy.deepcopy(base); i["initiatives"]["U1_j0"]["configs"][1]["impl_x"] = None
    assert solve(i, "B", ["g_base"])["status"] in ("OK_POINT",)
    _expect_status(solve(i, "C", ["g_base"]), "FOLLOWER_LEDGER_UNIDENTIFIED"); seen["FOLLOWER_LEDGER_UNIDENTIFIED"] = 1
    i = copy.deepcopy(base); i["policies"]["g_base"]["must"] = set(i["initiatives"]); i["A_bar"]["BUD"] = 1.0
    _expect_status(solve(i, "B", ["g_base"]), "INFEASIBLE"); seen["INFEASIBLE"] = 1
    i = copy.deepcopy(base); i["caps"]["c_model"]["F"] = None
    _expect_status(solve(i, "B", ["g_base"]), "THRESHOLD_MODE"); seen["THRESHOLD_MODE"] = 1
    i = copy.deepcopy(base); i["lam"]["senior"] = None
    _expect_status(solve(i, "B", ["g_base"]), "PARTIAL_OBJECTIVE"); seen["PARTIAL_OBJECTIVE"] = 1
    i = copy.deepcopy(base); next(iter(i["initiatives"]["U2_j1"]["configs"][0]["path"].values()))["v_u"] = None
    _expect_status(solve(i, "B", ["g_base"]), "UNEVALUABLE_INITIATIVE"); seen["UNEVALUABLE_INITIATIVE"] = 1
    i = copy.deepcopy(base); next(iter(i["initiatives"]["U2_j1"]["configs"][2]["path"].values()))["l_u"] = None
    _expect_status(solve(i, "B", ["g_base"]), "RESTRICTED_SOLVE"); seen["RESTRICTED_SOLVE"] = 1
    i = copy.deepcopy(base)
    sq = i["initiatives"]["U1_j0"]["N"][0] * expect(i["initiatives"]["U1_j0"]["configs"][0], lambda x, r: x["I_sev"])
    i["policies"]["g_base"]["ebar"]["U1_j0"] = sq * 0.5
    r = solve(i, "B", ["g_base"])
    assert "STATUS_QUO_NONCOMPLIANT" in r["flags"]; seen["STATUS_QUO_NONCOMPLIANT"] = 1
    i = copy.deepcopy(base)
    for j, ini in i["initiatives"].items():                                # design says Verify (catches errors);
        ini["configs"][1]["rho_design"] = {kk: {"Use": 0.0, "Verify": 1.0, "Reject": 0.0} for kk in ini["configs"][1]["rho"]}
        for cell in ini["configs"][1]["path"].values():                      # actual Use lets severe errors pass
            cell["I_sev"] = 0.3 if cell["I_sev"] > 0 else 0.0
        ini["configs"][2]["allowed_r"] = ini["configs"][2]["allowed_r"]
        i["policies"]["g_base"]["allow"][(j, 2)] = 0
        i["policies"]["g_base"]["ebar"][j] = ini["N"][0] * expect(ini["configs"][0], lambda x, r: x["I_sev"]) + 0.5
    dr = design_response_analysis(i, "g_base")
    assert dr["status"] == "DESIGN_INFEASIBLE_UNDER_RESPONSE", dr; seen["DESIGN_INFEASIBLE_UNDER_RESPONSE"] = 1
    small = make_instance(5, n_init=1)
    rr = solve_robust(small, "g_base", make_registry(small), "g1")
    assert rr["status"] == "OK_INTERVAL"; seen["OK_INTERVAL"] = 1
    missing = set(STATUS_ORDER) - set(seen)
    assert not missing, missing
    return ("STATE", "state-machine/output-contract PASS", f"all {len(STATUS_ORDER)} statuses reachable and returned as results (no exception path)")


def t_mis3_threshold():
    inst = make_instance(5)
    inst["A_bar"]["BUD"] = 1e6
    explicit = []
    for F in (0.0, 20.0, 40.0, 60.0, 80.0, 100.0, 140.0, 200.0):
        i = copy.deepcopy(inst); i["caps"]["c_model"]["F"] = F
        explicit.append((F, "c_model" in solve_central(i, ["g_base"])["y"]))
    i = copy.deepcopy(inst); i["caps"]["c_model"]["F"] = None
    r = solve(i, "B", ["g_base"])
    _expect_status(r, "THRESHOLD_MODE")
    assert "y" not in r and "F_E" not in r                    # no point decision is reported
    Fd = r["details"]["threshold"]["c_model"]["F_dagger"]
    for F, built in explicit:
        if abs(F - Fd) > 1e-3:
            assert built == (F <= Fd), (F, Fd, built)
    zero = copy.deepcopy(inst); zero["caps"]["c_model"]["F"] = 0.0
    rz = solve(zero, "B", ["g_base"])
    assert rz["status"] == "OK_POINT" and r["status"] != rz["status"]
    return ("T-MIS-3", "missing F_c threshold mode PASS", f"THRESHOLD_MODE with F_c^dagger={Fd:.3f} consistent with 8 explicit F_c solves; no point decision; differs from F_c=0")


def t_mis4_partial():
    inst = make_instance(5)
    i = copy.deepcopy(inst); i["lam"]["senior"] = None
    r = solve(i, "B", ["g_base"])
    _expect_status(r, "PARTIAL_OBJECTIVE")
    assert "F_E_minus_time" in r and "F_E" not in r and "delta_hours" in r
    assert r["details"]["lambda_scan"]["classification"] in ("ROBUST", "FRAGILE")
    z = copy.deepcopy(inst); z["lam"]["senior"] = 0.0
    rz = solve(z, "B", ["g_base"])
    assert rz["status"] == "OK_POINT" and "F_E" in rz
    i2 = copy.deepcopy(i); i2["lam_U"]["senior"] = None
    assert solve(i2, "B", ["g_base"])["details"]["lambda_scan"]["classification"] == "UNIDENTIFIED"
    return ("T-MIS-4", "missing lambda partial objective PASS",
            f"PARTIAL_OBJECTIVE with (F_E^-time, delta_hours={r['delta_hours']:.2f}); lambda in [0,lambda^U] scan = {r['details']['lambda_scan']['classification']}; no lambda^U -> UNIDENTIFIED")


MISSING_SITES = [
    ("F_c", lambda i: (i["caps"]["c_model"], "F")),
    ("lambda", lambda i: (i["lam"], "senior")),
    ("impl cell", lambda i: (i["initiatives"]["U1_j0"]["configs"][1]["impl"], frozenset({("c_model", "S")}))),
    ("eng cell", lambda i: (i["initiatives"]["U1_j0"]["configs"][1]["eng"], frozenset({("c_model", "S")}))),
    ("outcome cell (k>0)", lambda i: (next(iter(i["initiatives"]["U1_j0"]["configs"][1]["path"].values())), "l_u")),
    ("outcome cell (status quo)", lambda i: (next(iter(i["initiatives"]["U1_j0"]["configs"][0]["path"].values())), "l_u")),
    ("Allow", lambda i: (i["policies"]["g_base"]["allow"], ("U1_j0", 1))),
    ("Allow_loc", lambda i: (i["policies"]["g_base"]["allow_loc"], ("U1", "c_model"))),
    ("G_j", lambda i: (i["policies"]["g_base"]["G"], "U1_j0")),
    ("requirement cell", lambda i: (i["policies"]["g_base"]["H_req"], (O("A", 2), i["initiatives"]["U1_j0"]["kappa"]))),
    ("ebar", lambda i: (i["policies"]["g_base"]["ebar"], "U1_j0")),
    ("R_state", lambda i: (i["initiatives"]["U1_j0"]["R_state"], frozenset({("c_model", "S")}))),
    ("D_state", lambda i: (i["initiatives"]["U1_j0"]["D_state"], frozenset({("c_model", "S")}))),
    ("impl_x (ledger)", lambda i: (i["initiatives"]["U1_j0"]["configs"][1], "impl_x")),
    ("tau (ledger)", lambda i: (i["initiatives"]["U1_j0"]["tau"], "c_model")),
    ("N", lambda i: (i["initiatives"]["U1_j0"]["N"], 1)),
    ("A_bar", lambda i: (i["A_bar"], "BUD")),
    ("rho prob", lambda i: (i["initiatives"]["U1_j0"]["configs"][1]["rho"][("flag", "junior")], "Use")),
    ("gov_cost", lambda i: (i["policies"]["g_base"], "gov_cost")),
    ("rev_cap", lambda i: (i["rev_cap"], "U1")),
]


def t_mis6_no_silent_zero():
    rows = []
    for name, site in MISSING_SITES:
        for model in ("B", "C"):
            m, z = make_instance(5), make_instance(5)
            d, k = site(m); d[k] = None
            d2, k2 = site(z); d2[k2] = 0
            rm, rz = solve(m, model, ["g_base"]), solve(z, model, ["g_base"])
            if model == "B" and "ledger" in name:
                # the follower ledger split is not in B's identification set (43 §2): B is solved, and the
                # result records the input as UNIDENTIFIED-but-unused instead of treating it as zero
                assert rm["status"] == "OK_POINT" and rm["details"].get("unidentified_inputs_not_used_by_this_model")
                assert not rz["details"].get("unidentified_inputs_not_used_by_this_model")
                rows.append(f"{name}/B->OK_POINT(recorded unused)")
                continue
            assert rm["status"] != "OK_POINT", (name, model, rm["status"])
            same = (rm["status"] == rz["status"] and rm.get("F_E") == rz.get("F_E") and rm.get("configs") == rz.get("configs"))
            assert not same, (name, model)
            rows.append(f"{name}/{model}->{rm['status']}")
    nB = sum("recorded unused" in r for r in rows)
    return ("T-MIS-6", "no silent zero fill PASS",
            f"{len(rows)} mutations ({len(MISSING_SITES)} missing classes x models B and C): every missing input either yields a non-OK_POINT "
            f"status distinct from zero-fill, or ({nB} cases: follower-ledger fields under B, which B does not use) an OK_POINT that records "
            "the input as UNIDENTIFIED-unused while the zero-filled run does not")


# ---- V5: DP, limits, gate, reproducibility --------------------------------------------------
def t_orc9_dp():
    n = 0
    for s in range(1, 21):
        inst = make_instance(100 + s, aligned=(s % 2 == 0), integer=True)
        e, d = solve_central(inst, ["g_base"]), solve_central(inst, ["g_base"], method="dp")
        assert close(e["F"], d["F"]) and d["dp_exact"], (s, e["F"], d["F"])
        ce, cd = solve_bilevel(inst, ["g_base"]), solve_bilevel(inst, ["g_base"], method="dp")
        for mode in ("opt", "pess"):
            assert close(ce[mode]["F"], cd[mode]["F"]) and cd[mode]["dp_exact"], (s, mode)
        for forced in ({"c_model": True}, {"c_model": False}):
            fe = solve_central(inst, ["g_base"], forced=forced)
            fd = solve_central(inst, ["g_base"], forced=forced, method="dp")
            assert (fe is None and fd is None) or close(fe["F"], fd["F"])
        n += 1
    tie = tie_instance()
    te, td = solve_bilevel(tie, ["g_base"]), solve_bilevel(tie, ["g_base"], method="dp", beta=(1e-3, 1e-3))
    assert te["opt"]["F"] > te["pess"]["F"] + 1e-6
    for mode in ("opt", "pess"):
        lo = td[mode]["F"]
        assert lo <= te[mode]["F"] + 1e-7
    inst = make_instance(7)                                                # non-integer: not exact, bound reported
    e, d = solve_central(inst, ["g_base"]), solve_central(inst, ["g_base"], method="dp", beta=(1.0, 1.0))
    assert not d["dp_exact"] and d["F"] <= e["F"] + 1e-7 and e["F"] <= d["F"] + d["dp_bound"] + 1e-7
    return ("T-ORC-9", "DP == exhaustive PASS",
            f"{n} integer seeds: B, C-opt, C-pess, capability forced on/off all equal and flagged exact; ties respected; "
            f"non-integer case flagged inexact with bound {d['dp_bound']:.3f} containing the exhaustive optimum")


def tie_instance():
    inst = make_instance(7, aligned=False)
    j = "U1_j0"
    for k in (1, 2):
        cfg = inst["initiatives"][j]["configs"][k]
        for cell in cfg["path"].values():
            cell["v_u"], cell["l_u"], cell["c_u"], cell["t"] = 0.0, 0.0, 0.0, 0.0
            cell["l_x"] = 3.0 if k == 2 else 0.0
        for kk in cfg["impl"]:
            cfg["impl"][kk], cfg["eng"][kk] = 0.0, 0.0
    for cell in inst["initiatives"][j]["configs"][0]["path"].values():
        cell["v_u"], cell["l_u"], cell["c_u"], cell["t"] = 0.0, 0.0, 0.0, 0.0
    return inst


def t_orc10_shared_limit():
    for s in range(1, 9):
        inst = make_instance(s, aligned=(s % 2 == 0))
        B, Ap = solve_central(inst, ["g_base"]), solve_central(inst, ["g_base"], allow_shared=False)
        assert B["F"] >= Ap["F"] - 1e-7
        big = copy.deepcopy(inst)
        for c in big["caps"]:
            big["caps"][c]["F"] *= 1e4
        Bb, Apb = solve_central(big, ["g_base"]), solve_central(big, ["g_base"], allow_shared=False)
        assert not Bb["y"] and close(Bb["F"], Apb["F"])
    return ("T-ORC-10", "high-F_c shared limit PASS",
            "VSC >= 0 on 8 seeds (sharing enlarges B's feasible set); with F_c x 1e4 no shared capability is chosen and VSC = 0")


def t_orc12_model_d_gate():
    inst = hand_instance(0.0, 2.5)
    for ini in inst["initiatives"].values():
        cfg = ini["configs"][1]
        cfg["allowed_r"] = {"Use", "Reject"}
        cfg["rho"] = {("n", "r"): {"Use": 1.0, "Reject": 0.0}}
        cfg["path"][("r", "n", "ok", "Reject")] = dict(v_u=0.0, v_x=0.0, l_u=0.0, l_x=0.0, c_u=0.0, c_x=0.0, t=0.0, t_rev=0.0, I_sev=0.0)
    inst["initiatives"]["U2_j"]["configs"][1]["U"] = {("n", "r"): {"Use": 0.0, "Reject": 1.0}}   # users reject U2's AI
    inst["initiatives"]["U1_j"]["configs"][1]["U"] = {("n", "r"): {"Use": 1.0, "Reject": 0.0}}
    inst["caps"]["c"]["F"] = 24.0          # bilevel: building c is not worth it while U2 adopts harmful AI
    full = {"T1": True, "T2": True, "T3": True, "T4": True}
    before = TRI_LEVEL_CALLS["n"]
    for t in full:
        ev = dict(full); ev[t] = False
        r = solve_model_D(inst, ev, ["g"])
        assert r["status"] == "MODEL_D_NOT_IDENTIFIED" and TRI_LEVEL_CALLS["n"] == before
    agree = copy.deepcopy(inst)
    agree["initiatives"]["U2_j"]["configs"][1]["U"] = {("n", "r"): {"Use": 1.0, "Reject": 0.0}}
    r = solve_model_D(agree, full, ["g"])
    assert r["status"] == "MODEL_D_NOT_IDENTIFIED" and r["gate"]["T5"] is False and TRI_LEVEL_CALLS["n"] == before
    r = solve_model_D(inst, full, ["g"])
    assert r["status"] == "MODEL_D_EXECUTED" and TRI_LEVEL_CALLS["n"] == before + 1
    return ("T-ORC-12", "Model D gate PASS",
            "each single T1-T4 failure and a T5 failure (no upstream change) -> MODEL_D_NOT_IDENTIFIED with zero tri-level calls; "
            f"all five true -> executed: users' rejection of U2's AI makes building c worthwhile (tri-level pess value {r['result']['pess']:.1f} vs bilevel 0.0)")


def _repro_payload():
    inst = make_instance(42, aligned=False)
    small = make_instance(42, aligned=False, n_init=1)
    out = [solve(inst, "B", ["g_base", "g_strict"]), solve(inst, "C", ["g_base"]),
           solve(inst, "B", ["g_base"], method="dp", beta=(1.0, 1.0))]
    reg = make_registry(small)
    out.append(solve_robust(small, "g_base", reg, "g1"))
    return out


def t_orc13_repro():
    a, b = _repro_payload(), _repro_payload()
    assert [result_hash(x) for x in a] == [result_hash(x) for x in b]
    for x, y in zip(a, b):
        assert x["status"] == y["status"]
    h1 = subprocess.run([sys.executable, __file__, "--repro-hash"], capture_output=True, text=True, check=True).stdout.strip()
    h2 = subprocess.run([sys.executable, __file__, "--repro-hash"], capture_output=True, text=True, check=True).stdout.strip()
    assert h1 == h2 == hashlib.sha256("".join(result_hash(x) for x in a).encode()).hexdigest()
    return ("T-ORC-13", "reproducibility PASS", f"identical decisions, statuses, objectives and SHA-256 across 2 in-process and 2 fresh-process runs ({h1[:16]}...)")


def relabel(inst, maps):
    """Rename units, initiatives, roles and capabilities everywhere. maps: dict kind -> {old: new}."""
    U, J, R, C = maps["unit"], maps["init"], maps["role"], maps["cap"]
    pat = lambda key: frozenset((C[c], s) for c, s in key)
    n = dict(inst)
    n["units"] = [U[u] for u in inst["units"]]
    n["caps"] = {C[c]: copy.deepcopy(v) for c, v in inst["caps"].items()}
    n["loc_caps"] = {(U[u], C[c]): copy.deepcopy(v) for (u, c), v in inst["loc_caps"].items()}
    n["B0"] = {U[u]: copy.deepcopy(v) for u, v in inst["B0"].items()}
    n["rev_cap"] = {U[u]: v for u, v in inst["rev_cap"].items()}
    for key in ("lam", "lam_u", "lam_U"):
        n[key] = {R[r]: v for r, v in inst[key].items()}
    n["y_cur"] = frozenset(C[c] for c in inst["y_cur"])
    n["initiatives"] = {}
    for j, ini in inst["initiatives"].items():
        ni = dict(unit=U[ini["unit"]], kappa=ini["kappa"], N=dict(ini["N"]), rel=sorted(C[c] for c in ini["rel"]),
                  tau={C[c]: v for c, v in ini["tau"].items()},
                  R_state={pat(k): v for k, v in ini["R_state"].items()}, D_state={pat(k): v for k, v in ini["D_state"].items()},
                  configs={})
        for k, cfg in ini["configs"].items():
            nc = {kk: copy.deepcopy(vv) for kk, vv in cfg.items() if kk not in ("pre", "impl", "eng", "pi", "rho", "rho_design", "path")}
            nc["pre"] = {C[c] for c in cfg["pre"]}
            nc["impl"] = {pat(kk): v for kk, v in cfg["impl"].items()}
            nc["eng"] = {pat(kk): v for kk, v in cfg["eng"].items()}
            nc["pi"] = {R[r]: v for r, v in cfg["pi"].items()}
            nc["rho"] = {(z, R[r]): dict(v) for (z, r), v in cfg["rho"].items()}
            nc["rho_design"] = {(z, R[r]): dict(v) for (z, r), v in cfg.get("rho_design", {}).items()}
            nc["path"] = {(R[r], z, w, resp): dict(v) for (r, z, w, resp), v in cfg["path"].items()}
            ni["configs"][k] = nc
        n["initiatives"][J[j]] = ni
    n["policies"] = {}
    for g, pol in inst["policies"].items():
        np_ = {kk: copy.deepcopy(vv) for kk, vv in pol.items()}
        np_["allow"] = {(J[j], k): v for (j, k), v in pol["allow"].items()}
        np_["allow_loc"] = {(U[u], C[c]): v for (u, c), v in pol["allow_loc"].items()}
        np_["G"] = {J[j]: v for j, v in pol["G"].items()}
        np_["ebar"] = {J[j]: v for j, v in pol["ebar"].items()}
        np_["must"] = {J[j] for j in pol["must"]}
        np_["forbid"] = {J[j] for j in pol["forbid"]}
        n["policies"][g] = np_
    return n


def t_inv4_permutation():
    for seed in (11, 12, 13):
        inst = make_instance(seed, aligned=False)
        rng = random.Random(seed)
        def perm(items, prefix):
            new = [f"{prefix}{i}" for i in range(len(items))]
            rng.shuffle(new)
            return dict(zip(items, new))
        maps = {"unit": perm(inst["units"], "BU_"), "init": perm(sorted(inst["initiatives"]), "INI_"),
                "role": perm(["junior", "senior"], "ROLE_"), "cap": perm(sorted(inst["caps"]), "CAP_")}
        inv = {k: {v: kk for kk, v in m.items()} for k, m in maps.items()}
        a = solve_central(inst, ["g_base", "g_strict"], all_optima=True)
        b = solve_central(relabel(inst, maps), ["g_base", "g_strict"], all_optima=True)
        assert close(a["F"], b["F"])
        def back(sig):
            y, g, units = sig
            yy = tuple(sorted(inv["cap"][c] for c in y))
            uu = []
            for configs, loc in units:
                uu.append((tuple(sorted((inv["init"][j], k) for j, k in configs)), tuple(sorted(inv["cap"][c] for c in loc))))
            return (yy, g, tuple(sorted(uu)))
        norm = lambda sig: (sig[0], sig[1], tuple(sorted((tuple(sorted(c)), tuple(sorted(l))) for c, l in sig[2])))
        assert {norm(s) for s in a["optima"]} == {back(s) for s in b["optima"]}
        ca, cb = solve_bilevel(inst, ["g_base"]), solve_bilevel(relabel(inst, maps), ["g_base"])
        for mode in ("opt", "pess"):
            assert close(ca[mode]["F"], cb[mode]["F"])
    return ("T-INV-4", "label permutation invariance PASS",
            "3 seeds: random renaming of units, initiatives, roles and capabilities; full optimal sets equal after inverse mapping (B); C opt/pess values equal")


# ---- V6: robustness ------------------------------------------------------------------------
def make_registry(inst, scale=(0.6, 1.6)):
    j = "U1_j0"
    cells = [(("initiatives", j, "configs", k, "path", key), "l_u")
             for k in (1, 2) for key in inst["initiatives"][j]["configs"][k]["path"]]
    P = inst["initiatives"]["U2_j0"]["configs"][1]["P"]
    alt = {("flag", "err"): 0.12 * 0.7, ("noflag", "err"): 0.12 * 0.3, ("flag", "ok"): 0.5 - 0.12 * 0.7, ("noflag", "ok"): 0.5 - 0.12 * 0.3}
    return {"groups": {"g1": {"meaning": "loss scale and error-rate uncertainty",
                              "blocks": [dict(name="loss_scale_U1_j0", kind="scale", targets=cells, L=scale[0], U=scale[1]),
                                         dict(name="P_U2_j0_k1", kind="prob", path=("initiatives", "U2_j0", "configs", 1, "P"),
                                              vertices=[dict(P), alt])]}},
            "eps_R": 0.0, "tie_tol": 1e-9, "seed": 20261011}


def t_sen3_lemma_r():
    rng = random.Random(5)
    certified, violated = 0, 0
    for seed in (21, 22, 23, 24):
        inst = make_instance(seed, aligned=False, n_init=1)
        reg = make_registry(inst, scale=(0.2, 3.0))
        blocks = reg["groups"]["g1"]["blocks"]
        tinst = theta_instances(inst, blocks)
        cands = [d for d in enumerate_portfolios(inst, "g_base") if robust_feasibility(inst, "g_base", d, blocks, tinst) == "ROBUSTLY_FEASIBLE"]
        vert = {th: {d: evaluate_portfolio(i, "g_base", d) for d in cands} for th, i in tinst}
        samples = []
        for _ in range(60):
            th = tuple(block_sample(b, rng) for b in blocks)
            i = apply_theta(inst, blocks, th)
            samples.append({d: evaluate_portfolio(i, "g_base", d) for d in cands})
        nominal = max(cands, key=lambda d: evaluate_portfolio(inst, "g_base", d))
        vertex_best = [max(row, key=row.get) for row in vert.values()]
        picks = list(dict.fromkeys([nominal] + vertex_best + cands[:: max(1, len(cands) // 6)]))
        for d_star in picks:
            vgap = min(row[d_star] - max(row.values()) for row in vert.values())
            sgap = min(row[d_star] - max(row.values()) for row in samples)
            if vgap >= -1e-7:
                certified += 1
                assert sgap >= -1e-6, ("sampling found a violation the vertex check missed", seed, sgap)
            else:
                violated += 1
                assert vgap <= sgap + 1e-9          # vertices are at least as extreme as interior samples
        cert = lemma_r_check(inst, "g_base", picks[0], cands, blocks)
        assert cert["robust"] == (min(row[picks[0]] - max(row.values()) for row in vert.values()) >= -1e-7)
    assert certified >= 1 and violated >= 1, (certified, violated)
    for model, scope in (("C", "whole_portfolio"), ("B", "element")):
        try:
            lemma_r_check(inst, "g_base", cands[0], cands, blocks, model=model, scope=scope)
            raise AssertionError("scope guard failed")
        except ScopeError:
            pass
    vals = lambda th: {"y1_a": th, "y1_b": 1 - th, "y0": 0.6}
    at_vertices = all(max(vals(t)["y1_a"], vals(t)["y1_b"]) >= vals(t)["y0"] for t in (0.0, 1.0))
    interior = max(vals(0.5)["y1_a"], vals(0.5)["y1_b"]) >= vals(0.5)["y0"]
    assert at_vertices and not interior
    return ("T-SEN-3", "Lemma R scope test PASS",
            f"{certified} certified whole portfolios: 60 interior samples per seed found no violation; {violated} uncertified: "
            "vertex gap <= sampled gap; ScopeError for Model C and element scope; element-level counterexample reproduced")


def t_sen4_robust_feasibility():
    inst = make_instance(31, n_init=1)
    j = "U1_j0"
    sq = inst["initiatives"][j]["N"][0] * expect(inst["initiatives"][j]["configs"][0], lambda x, r: x["I_sev"])
    inst["policies"]["g_base"]["ebar"][j] = sq * 1.05
    cells = [(("initiatives", j, "configs", 1, "path", key), "I_sev") for key in inst["initiatives"][j]["configs"][1]["path"]]
    blocks = [dict(name="Isev_scale", kind="scale", targets=cells, L=0.5, U=6.0)]
    ports = enumerate_portfolios(inst, "g_base")
    classes = {}
    for d in ports:
        classes.setdefault(robust_feasibility(inst, "g_base", d, blocks), []).append(d)
    assert classes.get("CONDITIONALLY_FEASIBLE") and classes.get("ROBUSTLY_FEASIBLE")
    uses = lambda d: any((j, 1) in configs for configs, _ in d[1])
    assert all(uses(d) for d in classes["CONDITIONALLY_FEASIBLE"])
    assert not any(uses(d) for d in classes["ROBUSTLY_FEASIBLE"])
    big = [dict(name="Isev_scale", kind="scale", targets=cells, L=50.0, U=60.0)]
    assert any(robust_feasibility(inst, "g_base", d, big) == "INFEASIBLE" for d in ports if uses(d))
    reg = {"groups": {"g1": {"blocks": blocks}}, "eps_R": 0.0, "tie_tol": 1e-9, "seed": 1}
    rr = solve_robust(inst, "g_base", reg, "g1")
    assert not uses(rr["decision"])
    return ("T-SEN-4", "robust feasibility PASS",
            f"{len(classes['ROBUSTLY_FEASIBLE'])} robust / {len(classes['CONDITIONALLY_FEASIBLE'])} conditional portfolios; "
            "conditional ones (all using the risk-sensitive config) excluded from the robust candidate set; INFEASIBLE detected when violated at every vertex")


def t_sen6_registry():
    inst = make_instance(8, n_init=1)
    reg = make_registry(inst)
    r = solve_robust(inst, "g_base", reg, "g1")
    r2 = solve(inst, "B", ["g_base"], registry=reg)
    for x in (r, r2):
        assert len(x["scenario_registry_hash"]) == 64 and len(x["parameter_ranges_hash"]) == 64
        assert x["solver_version"] == SOLVER_VERSION and "provenance_summary" in x
        assert verify_registry(x, reg)
    tampered = copy.deepcopy(reg)
    tampered["groups"]["g1"]["blocks"][0]["U"] = 9.9
    assert not verify_registry(r, tampered)
    tampered2 = copy.deepcopy(reg); tampered2["eps_R"] = 1.0
    assert not verify_registry(r, tampered2)
    return ("T-SEN-6", "scenario registry hashing PASS",
            "registry and parameter-range SHA-256, solver version and provenance summary emitted; post-hoc change of a range or of eps_R detected")


def t_sen7_regret_voi():
    informative = None
    for seed in range(9, 30):
        inst = make_instance(seed, aligned=False, n_init=1)
        reg = make_registry(inst, scale=(0.05, 6.0))
        blocks = reg["groups"]["g1"]["blocks"]
        tinst = theta_instances(inst, blocks)
        cands = [d for d in enumerate_portfolios(inst, "g_base") if robust_feasibility(inst, "g_base", d, blocks, tinst) == "ROBUSTLY_FEASIBLE"]
        thetas = theta_grid(blocks)
        vals = regret_table(inst, "g_base", cands, thetas, blocks)
        mmr = minimax_regret(vals, cands)
        voi = voi_table(vals, cands, blocks)
        for name, row in voi.items():
            assert all(v <= mmr + 1e-9 for v in row["mmr_given_value"].values()), name   # more information never raises MMR
            assert row["voi"] >= -1e-9
        # information = restricting theta to a subset of the registered grid (same candidate set, same feasibility)
        common = [th for th in thetas if th[0] == ("scale", blocks[0]["L"])]
        assert minimax_regret(vals, cands, common) <= mmr + 1e-9
        assert all(max_regret(vals, d) >= -1e-9 for d in cands)
        if mmr > 1e-6 and informative is None:
            informative = (seed, mmr, sorted(((round(r["voi"], 3), n) for n, r in voi.items()), reverse=True), len(cands), len(thetas))
            break
    assert informative is not None, "no informative instance found"
    seed, mmr, ranking, nc, nt = informative
    return ("T-SEN-7", "MaxRegret PASS / VOI monotonic information test PASS",
            f"seed {seed}: minimax regret {mmr:.3f} over {nt} vertices and {nc} robust candidates; conditioning on any block value never "
            f"raised it; VOI ranking {ranking}")


def t_sen8_delta():
    switched = 0
    for s in range(1, 9):
        seq = []
        for dlt in (0, 1, 2, 3, 4, 6, 8, 10, 14, 20):
            inst = make_instance(s, delta_shared={"c_model": dlt})
            inst["caps"]["c_model"]["F"] = 90.0
            seq.append("c_model" in solve_central(inst, ["g_base"])["y"])
        sw = sum(a != b for a, b in zip(seq, seq[1:]))
        assert sw <= 1 and (sw == 0 or seq[0] is False), (s, seq)
        switched += sw
    assert switched >= 1
    # Model C counterexample: misaligned U2 becomes unblockable once reuse drives its implementation cost to 0
    scan = []
    for dlt in (0.0, 1.0, 2.0, 2.9, 3.0, 3.5, 4.0, 5.0):
        h = hand_instance(None, 2.5, delta=dlt, u1_base=5.0, u2_base=3.0)
        h["caps"]["c"]["F"] = 24.0
        c = solve_bilevel(h, ["g"])["pess"]
        scan.append((dlt, "c" in c["y"], round(c["F"], 6)))
    built = [b for _, b, _ in scan]
    changes = sum(a != b for a, b in zip(built, built[1:]))
    assert changes >= 2, scan
    values = [v for _, _, v in scan]
    assert any(b < a - 1e-9 for a, b in zip(values, values[1:]))   # leader value falls as reuse improves
    build_set = [d for d, b, _ in scan if b]
    return ("T-SEN-8", "Model C delta nonmonotonic counterexample PASS",
            f"B: delta^dagger single 0->1 switch on 8 seeds ({switched} switched). C: y_c* sequence {['1' if b else '0' for b in built]} "
            f"over delta {[d for d, _, _ in scan]} -> set-valued build region {build_set}; no unique delta^dagger in C")


def t_orc8_independent_hand():
    """Expected values from an independent hand derivation by a separate agent that had no access to 46/47
    (see 50 §8); compared here after the derivation was recorded."""
    expect_tbl = {
        "aligned": dict(A=0, C0=0, Aplus=0, B=30, C=30, VRA=0, DL0=0, VCP=0, VSC=30, DL=0, NEV=30, args=(5.0, 0.0)),
        "blockable": dict(A=0, C0=0, Aplus=0, B=15, C=15, VRA=0, DL0=0, VCP=0, VSC=15, DL=0, NEV=15, args=(5.0, 2.5)),
        "unblockable": dict(A=0, C0=0, Aplus=0, B=15, C=10, VRA=0, DL0=0, VCP=0, VSC=15, DL=5, NEV=10, args=(0.0, 2.5)),
    }
    for name, e in expect_tbl.items():
        m = architecture_metrics(hand_instance(*e["args"]), "g")
        for mode in ("opt", "pess"):
            got = dict(A=m["A"][mode], C0=m["C0"][mode], Aplus=m["Aplus"], B=m["B"], C=m["C"][mode], VRA=m["VRA"][mode],
                       DL0=m["DL0"][mode], VCP=m["VCP"][mode], VSC=m["VSC"], DL=m["DL"][mode], NEV=m["NEV"][mode])
            for k, v in got.items():
                assert close(v, e[k]), (name, mode, k, v, e[k])
    return ("T-ORC-8", "independent hand-oracle rederivation PASS (INDEPENDENT_COMPUTATIONAL_REDERIVATION_PASS)",
            "aligned B=C=30; blockable B=C=15, DL=0; unblockable B=15, C=10, DL=5, VSC=15, NEV=10; A=C0=A+=0, VRA=DL0=VCP=0 in all three; opt=pess")


# ---- regression of v2.1 propositions ------------------------------------------------------
def t_regression_v21():
    for s in range(1, 7):
        for aligned in (True, False):
            m = architecture_metrics(make_instance(s, aligned), "g_base")
            for mode in ("opt", "pess"):
                assert le(m["A"][mode], m["C0"][mode]) and le(m["C0"][mode], m["Aplus"]) and le(m["C0"][mode], m["C"][mode]) and le(m["C"][mode], m["B"])
                assert close(m["NEV"][mode], m["VCP"][mode] + m["VSC"] - m["DL"][mode]) and close(m["VCP"][mode], m["VRA"][mode] + m["DL0"][mode])
                if aligned:
                    assert close(m["DL"][mode], 0.0) and close(m["DL0"][mode], 0.0)
    h = hand_instance(0.0, 2.5, ea_levels=(2, 1), ea_req=2)
    assert close(solve_bilevel(h, ["g"])["pess"]["F"], 10.0) and close(solve_bilevel(h, ["g_req"])["pess"]["F"], 15.0)
    inst = make_instance(9, aligned=False)
    d = governance_decomposition(inst, "g_strict", "g0")
    assert close(d["VG"], d["EE"] + d["RE"] + d["CE"]) and le(d["RE"], 0.0)
    a = solve_central(make_instance(4), ["g_base"]); b = solve_central(make_instance(4, money=1000.0), ["g_base"])
    assert close(b["F"], 1000 * a["F"]) and a["y"] == b["y"]
    return ("REG", "v2.1 regression PASS", "P1 (with C0), P2, identities, P8 screening (10->15), P7 in B, P6 money scaling")


TESTS = [t_sch5_typed_units, t_sch6_omega_guard, t_sch7_nonfinite, t_alg1_f5e, t_state_machine, t_mis3_threshold,
         t_mis4_partial, t_mis6_no_silent_zero, t_orc9_dp, t_orc10_shared_limit, t_orc12_model_d_gate, t_orc13_repro,
         t_inv4_permutation, t_sen3_lemma_r, t_sen4_robust_feasibility, t_sen6_registry, t_sen7_regret_voi,
         t_sen8_delta, t_orc8_independent_hand, t_regression_v21]

REQUIRED = ["typed units PASS", "explicit omega leakage guard PASS", "NaN/inf rejection PASS", "F5e PASS",
            "state-machine/output-contract PASS", "missing F_c threshold mode PASS", "missing lambda partial objective PASS",
            "no silent zero fill PASS", "DP == exhaustive PASS", "high-F_c shared limit PASS", "Model D gate PASS",
            "reproducibility PASS", "label permutation invariance PASS", "Lemma R scope test PASS", "robust feasibility PASS",
            "scenario registry hashing PASS", "MaxRegret PASS", "VOI monotonic information test PASS",
            "Model C delta nonmonotonic counterexample PASS", "independent hand-oracle rederivation PASS"]


if __name__ == "__main__":
    if "--repro-hash" in sys.argv:
        print(hashlib.sha256("".join(result_hash(x) for x in _repro_payload()).encode()).hexdigest())
        sys.exit(0)
    passed, failed = [], []
    for t in TESTS:
        try:
            tid, key, msg = t()
            passed.append(key)
            print(f"PASS {tid}: {msg}")
        except Exception as e:  # report and continue; any failure blocks the verdict
            failed.append((t.__name__, repr(e)[:300]))
            print(f"FAIL {t.__name__}: {repr(e)[:300]}")
    joined = " | ".join(passed)
    missing = [r for r in REQUIRED if r not in joined]
    print()
    if failed or missing:
        print("V2_2_SYNTHETIC_ENGINEERING_VERDICT: PARTIAL")
        for f in failed:
            print("  blocker:", f)
        for m in missing:
            print("  missing:", m)
    else:
        print("V2_2_SYNTHETIC_ENGINEERING_VERDICT: PASS  (synthetic engineering validation only; SIMULATED_ONLY; not empirical, not enterprise, not V7)")
