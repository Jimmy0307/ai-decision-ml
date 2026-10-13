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
  * fixes for the two adversarial reviews recorded in 50 §7 (robust candidates from the theta-independent
    superset; lambda box scan with exact vertex certificate for B/A+; DP enumeration fallback; config-local
    missing inputs; joint-witness feasibility classes; vertex vs grid VOI; exact-float registry commitment
    including nominal values; registry block validation; element-level classification)  (AUDIT)

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


class MissingPermission(MissingInput):
    """A policy permission (Allow) is UNIDENTIFIED: the configuration is excluded, the initiative is kept."""


class MissingStateLookup(MissingInput):
    """A capability-state lookup (R_j(s), D_j(s)) is UNIDENTIFIED for this state only."""


class ModelAInfeasible(ValueError):
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
        for tname, cons in (("H_req", "H"), ("WI_req", "WI"), ("EA_req", "EA"), ("G_req", "G")):
            for (a, kk), v in pol[tname].items():
                if not (isinstance(a, Ord) and a.construct == "A" and isinstance(kk, Ord) and kk.construct == "K"):
                    raise InvalidInput(f"{tname} must be keyed by (Ord('A'), Ord('K'))")
                if v is not None and not (isinstance(v, Ord) and v.construct == cons):
                    raise InvalidInput(f"{tname} values must be Ord('{cons}')")
    for tname, cons in (("R_req", "R"), ("D_req", "D")):
        for a, v in inst[tname].items():
            if not isinstance(a, Ord) or (v is not None and not (isinstance(v, Ord) and v.construct == cons)):
                raise InvalidInput(f"{tname} must map Ord('A') to Ord('{cons}')")
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
            for pk in cfg["P"]:
                if not isinstance(pk, tuple) or len(pk) != 2:
                    raise InvalidInput(f"{where}: P keys must be (z, omega)")
            for rows_name in ("rho", "rho_design"):
                for rk, row in cfg.get(rows_name, {}).items():
                    for r, pr in row.items():
                        if pr is not None and pr > 0 and r not in cfg["allowed_r"]:
                            raise InvalidInput(f"{where}: response {r} has positive probability but is not allowed")
            for pk, cell in cfg["path"].items():
                if not isinstance(pk, tuple) or len(pk) != 4:
                    raise InvalidInput(f"{where}: path keys must be (role, z, omega, r)")
                if set(cell) != set(PATH_UNITS):
                    raise InvalidInput(f"{where}: path cell {pk} must have exactly the fields {sorted(PATH_UNITS)}")
                for f, unit in PATH_UNITS.items():
                    _num(cell.get(f), unit, f"{where}.path[{pk}].{f}", True)
        for tbl, cons in (("R_state", "R"), ("D_state", "D")):
            for key, v in ini[tbl].items():
                if v is not None and not (isinstance(v, Ord) and v.construct == cons):
                    raise InvalidInput(f"{j}.{tbl} must hold Ord('{cons}') values")
    return True


# =============================================================================
# 5. Expectation (X1) and per-(j,k) evaluation
# =============================================================================
def _normalized(dist, what):
    if any(p is None for p in dist.values()):
        raise MissingInput(f"{what} contains UNIDENTIFIED probability")
    if any(p < -TOL for p in dist.values()) or not math.isclose(sum(dist.values()), 1.0, abs_tol=1e-9):
        raise InvalidInput(f"{what} must be nonnegative and normalized")


def expect(cfg, fn, rho_key="rho", capkey=None):
    """E_jk[f]. rho rows may be keyed (z, role) or (z, role, capability-source key); a capability-state row,
    when present for the current state, takes precedence. omega never appears in a rho key (T-SCH-6)."""
    _normalized(cfg["pi"], "pi")
    _normalized(cfg["P"], "P")
    total = 0.0
    rho_tab = cfg[rho_key]
    for role, p_role in cfg["pi"].items():
        for (z, w), p_zw in cfg["P"].items():
            rho = rho_tab.get((z, role, capkey)) if capkey is not None else None
            if rho is None:
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


def _is_min_level(inst, ordv):
    return ordv.code == min(inst["codes"][ordv.construct].values())


def jk_eval(inst, j, k, y_shared, loc, gamma_name, rho_key="rho"):
    ini = inst["initiatives"][j]
    pol = inst["policies"][gamma_name]
    cfg, cfg0 = ini["configs"][k], ini["configs"][0]
    avail = set(y_shared) | set(loc)
    key = source_key(ini["rel"], y_shared, loc)
    key_cur = source_key(ini["rel"], inst.get("y_cur", frozenset()), set())
    lam_override = inst.get("_lam_override", {})

    def lam(role, which="lam"):
        if which == "lam" and role in lam_override:      # override applies to the ENTERPRISE ledger only
            return lam_override[role]
        return lam_of(inst, which, role)

    def g_E(c, ck):
        return expect(c, lambda x, role: x["v_u"] + x["v_x"] - x["l_u"] - x["l_x"] - x["c_u"] - x["c_x"] - lam(role) * x["t"], rho_key, ck)

    def g_E_notime(c, ck):
        return expect(c, lambda x, role: x["v_u"] + x["v_x"] - x["l_u"] - x["l_x"] - x["c_u"] - x["c_x"], rho_key, ck)

    def opc(c, ck):
        return expect(c, lambda x, role: x["c_u"] + x["c_x"], rho_key, ck)

    N_k, N_0 = strict(ini["N"], k, "N"), strict(ini["N"], 0, "N")
    impl = 0.0 if k == 0 else strict(cfg["impl"], key, "implementation cost")
    eng = 0.0 if k == 0 else strict(cfg["eng"], key, "engineering hours")
    # incremental contribution vs the status quo at the CURRENT capability state (V2)
    phi_nt = N_k * g_E_notime(cfg, key) - N_0 * g_E_notime(cfg0, key_cur) - impl
    roles = sorted(cfg["pi"])
    hours_by_role = {r: N_k * expect(cfg, lambda x, rr, r=r: x["t"] if rr == r else 0.0, rho_key, key)
                     - N_0 * expect(cfg0, lambda x, rr, r=r: x["t"] if rr == r else 0.0, rho_key, key_cur) for r in roles}
    phiE = N_k * g_E(cfg, key) - N_0 * g_E(cfg0, key_cur) - impl   # k=0: N_0[g_j0(state) - g_j0(current)]
    bud = impl + N_k * opc(cfg, key) - N_0 * opc(cfg0, key_cur)
    rev = N_k * expect(cfg, lambda x, r: x["t_rev"], rho_key, key) - N_0 * expect(cfg0, lambda x, r: x["t_rev"], rho_key, key_cur)
    sev = N_k * expect(cfg, lambda x, r: x["I_sev"], rho_key, key)
    hours = sum(hours_by_role.values())
    try:
        def g_U(c, ck):
            return expect(c, lambda x, role: x["v_u"] - x["l_u"] - x["c_u"] - lam(role, "lam_u") * x["t"], rho_key, ck)
        impl_x = 0.0 if k == 0 else strict(cfg, "impl_x", "central-funded implementation share")
        tau = 0.0 if k == 0 else sum(strict(ini["tau"], c, "chargeback rule")
                                     for c in cfg["pre"] if c in y_shared and c not in loc)
        phiU = N_k * g_U(cfg, key) - N_0 * g_U(cfg0, key_cur) - (impl - impl_x) - tau
    except MissingInput:
        phiU = None

    kap, A = ini["kappa"], cfg["A"]
    req = lambda table: strict(table, (A, kap), "requirement table cell")
    allow = pol["allow"].get((j, k))
    if allow is None:
        raise MissingPermission(f"Allow UNIDENTIFIED: {(j, k)}")

    def f5e(tbl, req_tbl, label):
        # F5e at the capability state the configuration actually runs on (all k, including the status quo).
        r_req = strict(inst[req_tbl], A, f"{label}^req(A)")
        if _is_min_level(inst, r_req):
            return True                       # any level satisfies the scale minimum; no lookup needed
        v = ini[tbl].get(key)
        if v is None:
            raise MissingStateLookup(f"{label}_j(s) UNIDENTIFIED: {sorted(key)}")
        return v >= r_req

    codes = inst["codes"]
    static_ok = (
        cfg["legal"] == 1                                                              # F2
        and allow == 1                                                                 # F3
        and (j not in pol["forbid"] or k == 0)
        and all(c in avail for c in cfg["pre"])                                        # F4
        and cfg["H"] >= req(pol["H_req"])                                              # F5a
        and cfg["WI"] >= req(pol["WI_req"])                                            # F5b
        and strict(pol["G"], j, "G_j(gamma)") >= req(pol["G_req"])                     # F5c
        and cfg["EA"] >= req(pol["EA_req"])                                            # F5d
        and f5e("R_state", "R_req", "R") and f5e("D_state", "D_req", "D")              # F5e
        and (not (req(pol["H_req"]) >= O("H", 2, codes)) or cfg["effH"] == 1)          # F6
        and (cfg["A"] < O("A", 2, codes) or cfg["FB"] == 1)                            # F7
        and cfg["cons"] == 1                                                           # F8
    )
    f9 = sev <= strict(pol["ebar"], j, "incident tolerance") + TOL                     # F9
    return dict(feasible=static_ok and f9, static_ok=static_ok, f9=f9, legal=cfg["legal"] == 1,
                phiE=phiE, phiE_notime=phi_nt, phiU=phiU, bud=bud, eng=eng, rev=rev, sev=sev, hours=hours,
                hours_by_role=hours_by_role)


# =============================================================================
# 6. Unit plans
# =============================================================================
def _subsets(items):
    items = list(items)
    for r in range(len(items) + 1):
        yield from itertools.combinations(items, r)


def unit_plans(inst, u, y_shared, gamma_name, allow_local=True, log=None, rho_key="rho", static_only=False):
    """Feasible plans of unit u. static_only=True keeps theta-independent feasibility only (F2-F8) and skips
    the theta-dependent checks (F9, R2) -- used to build candidate sets for robust analysis."""
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
                except (MissingPermission, MissingStateLookup) as e:
                    if log is not None:
                        log.add((j, k, type(e).__name__))
                    continue
                except MissingInput:
                    # local to this (j, k, capability state): the configuration is excluded in this state only.
                    # An initiative whose status quo cannot be evaluated at the current state is removed earlier
                    # by _drop_unevaluable (UNEVALUABLE_INITIATIVE).
                    if log is not None:
                        log.add((j, k, "MissingInput"))
                    continue
                if (ev["static_ok"] if static_only else ev["feasible"]):
                    opts.append((k, ev))
            per_j.append(opts)
        for combo in itertools.product(*per_j):
            if not static_only and sum(ev["rev"] for _, ev in combo) > strict(inst["rev_cap"], u, "rev_cap") + TOL:
                continue
            fU = None if any(ev["phiU"] is None for _, ev in combo) else sum(ev["phiU"] for _, ev in combo) - loc_bud
            hb = {}
            for _, ev in combo:
                for r, h in ev["hours_by_role"].items():
                    hb[r] = hb.get(r, 0.0) + h
            plans.append(dict(configs=tuple((j, k) for j, (k, _) in zip(js, combo)), loc=tuple(loc),
                              bud=sum(ev["bud"] for _, ev in combo) + loc_bud,
                              eng=sum(ev["eng"] for _, ev in combo) + loc_eng,
                              fE=sum(ev["phiE"] for _, ev in combo) - loc_bud, fU=fU,
                              fE_notime=sum(ev["phiE_notime"] for _, ev in combo) - loc_bud,
                              hours=sum(ev["hours"] for _, ev in combo), hours_by_role=hb))
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


DP_STATS = {"fallback_enum": 0}


def mck_dp(groups, cap_b, cap_e, beta_b=1.0, beta_e=1.0):
    """Returns (value, combo, exact, bound).
    Ceil-rounded weights give a feasible lower bound (lo); floor-rounded weights give a relaxation upper bound
    (hi), so OPT is in [lo, hi] and bound = hi - lo. exact=True iff all shifted weights are integer multiples of
    the quanta, OR the branch fell back to exhaustive enumeration because ceil-rounding found no feasible
    combination while the relaxation did (counted in DP_STATS)."""
    def integral(x, beta):
        q = x / beta
        return abs(q - round(q)) < 1e-9
    exact = all(integral(c[0] - min(cc[0] for cc in g), beta_b) and integral(c[1] - min(cc[1] for cc in g), beta_e)
                for g in groups for c in g)
    lo_v, lo_c = _mck_dp_core(groups, cap_b, cap_e, beta_b, beta_e, lambda q: int(math.ceil(q - 1e-9)))
    if exact:
        return lo_v, lo_c, True, 0.0
    hi_v, _ = _mck_dp_core(groups, cap_b, cap_e, beta_b, beta_e, lambda q: int(math.floor(q + 1e-9)))
    if hi_v is None:
        return None, None, True, 0.0               # relaxation infeasible => truly infeasible
    if lo_v is None:
        DP_STATS["fallback_enum"] += 1
        v, c = mck_enum(groups, cap_b, cap_e)
        return v, c, True, 0.0
    return lo_v, lo_c, False, hi_v - lo_v


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
                dp_bound = max(dp_bound, bd)
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
    exact_all, bound_all = True, 0.0
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
                    v, combo, ex, bd = mck_dp(groups, rb, re_, *beta)
                    exact_all &= ex
                    bound_all = max(bound_all, bd)
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
                best[mode]["dp_bound"] = bound_all
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
            raise ModelAInfeasible("Model A infeasible for unit " + u)
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


def _drop_unevaluable(inst, gammas, flags, details):
    """Drop an initiative only if its status quo cannot be evaluated for a REASON THAT IS NOT LOCAL TO ONE
    CONFIGURATION. Only requested, usable policies are checked. A missing permission Allow(j,0) or a missing
    state lookup excludes that configuration only (logged by unit_plans), never the whole initiative."""
    work = copy.deepcopy(inst)
    for j in sorted(work["initiatives"]):
        try:
            for g in gammas:
                try:
                    ev = jk_eval(work, j, 0, set(), set(), g)
                except (MissingPermission, MissingStateLookup):
                    continue
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


def _restricted_log(inst, gammas, allow_shared=True):
    log = set()
    for g in gammas:
        for y in _subsets(sorted(inst["caps"]) if allow_shared else []):
            for u in inst["units"]:
                try:
                    unit_plans(inst, u, y, g, log=log)
                except MissingInput:
                    pass
    return sorted(log, key=str)


def _roles_in_use(inst):
    return sorted({r for ini in inst["initiatives"].values() for cfg in ini["configs"].values() for r in cfg["pi"]})


SHARED_MODELS = ("B", "C")


def solve(inst, model="B", gammas=None, method="enum", beta=(1.0, 1.0), registry=None):
    """Never raises for data problems: returns a portfolio_result dict with a status from STATUS_ORDER."""
    res = dict(solver_version=SOLVER_VERSION, model=model, status=None, flags=[], details={},
               provenance_summary=_provenance_summary(inst) if isinstance(inst, dict) else {})
    try:
        return _solve_guarded(inst, model, gammas, method, beta, registry, res)
    except (MissingInput, NotComparable, ModelAInfeasible) as e:     # data problems outside the core solve
        st = ("FOLLOWER_LEDGER_UNIDENTIFIED" if isinstance(e, FollowerLedgerUnidentified) else
              "REJECT_INSUFFICIENT_IDENTIFIED_INPUTS" if isinstance(e, MissingInput) else
              "NOT_COMPARABLE" if isinstance(e, NotComparable) else "INFEASIBLE")
        res.update(status=st, flags=[st])
        res["details"]["error"] = f"{type(e).__name__}: {e}"
        return res
    except (InvalidInput, TypeError, KeyError, ValueError, AttributeError, IndexError, ArithmeticError) as e:
        res.update(status="INVALID_SCHEMA_OR_UNITS", flags=["INVALID_SCHEMA_OR_UNITS"])
        res["details"]["error"] = f"{type(e).__name__}: {e}"
        for k in ("F_E", "y", "configs", "gamma", "envelopes"):
            res.pop(k, None)
        return res


def _finish(res, flags):
    res["flags"] = sorted(flags, key=STATUS_ORDER.index)
    res["status"] = res["flags"][0]
    res.pop("infeasible", None)
    return res


def _solve_guarded(inst, model, gammas, method, beta, registry, res):
    if model not in ("A", "Aplus", "B", "C0", "C"):
        raise InvalidInput(f"unknown model {model}")
    if method not in ("enum", "dp"):
        raise InvalidInput(f"unknown method {method}")
    if method == "dp" and not (len(beta) == 2 and all(isinstance(b, (int, float)) and not isinstance(b, bool)
                                                       and math.isfinite(b) and b >= 1e-6 for b in beta)):
        raise InvalidInput("DP quanta beta must be two finite numbers >= 1e-6")
    flags = set()
    validate_instance(inst)
    if registry is not None:
        validate_registry(registry, inst)
        res["scenario_registry_hash"] = registry_hash(registry)
        res["parameter_ranges_hash"] = parameter_ranges_hash(registry)
        res["registry_commitment"] = registry_commitment(registry, inst)
    if inst["A_bar"].get("BUD") is None or inst["A_bar"].get("ENG") is None or \
       any(inst["rev_cap"].get(u) is None for u in inst["units"]):
        return _finish(res, {"REJECT_INSUFFICIENT_IDENTIFIED_INPUTS"})
    requested = sorted(gammas or inst["policies"])
    usable = [g for g in requested if inst["policies"][g].get("gov_cost") is not None]
    if len(usable) < len(requested):
        flags.add("RESTRICTED_SOLVE")
        res["details"]["excluded_policies"] = sorted(set(requested) - set(usable))
    if not usable:
        return _finish(res, flags | {"REJECT_INSUFFICIENT_IDENTIFIED_INPUTS"})
    if model == "A" and len(usable) != 1:
        raise InvalidInput("Model A requires exactly one usable policy")
    # lambda: a role is missing if it appears in any pi but has no identified enterprise lambda
    roles_missing = [r for r in _roles_in_use(inst) if inst["lam"].get(r) is None]
    probe = copy.deepcopy(inst)
    if roles_missing:            # values irrelevant here: used only to find non-lambda missing inputs
        probe["_lam_override"] = {r: 0.0 for r in roles_missing}
    probe = _drop_unevaluable(probe, usable, flags, res["details"])
    if not probe["initiatives"]:
        return _finish(res, flags | {"REJECT_INSUFFICIENT_IDENTIFIED_INPUTS"})
    work = copy.deepcopy(probe)
    work.pop("_lam_override", None)
    allow_shared = model in SHARED_MODELS
    caps_missing = sorted(c for c, d in work["caps"].items() if d["F"] is None)
    if caps_missing and not allow_shared:
        # without sharing F_c enters only through the status-quo charge of capabilities already in y_cur
        unused_caps = [c for c in caps_missing if c not in work.get("y_cur", frozenset())]
        if unused_caps:
            res["details"].setdefault("unidentified_inputs_not_used_by_this_model", []).extend(("caps.F", c) for c in unused_caps)
        caps_missing = []
    try:
        if roles_missing:
            # PARTIAL_OBJECTIVE: never a silent zero. No point decision unless the decision is invariant over
            # the pre-registered box [0, lambda^U]^m (exact vertex check for B/A+; grid for C/C0/A).
            flags.add("PARTIAL_OBJECTIVE")
            res["details"]["lambda_unidentified_roles"] = roles_missing
            scan = lambda_scan(work, model, usable, roles_missing, method, beta, caps_missing=caps_missing)
            res["details"]["lambda_scan"] = scan
            if caps_missing:
                flags.add("THRESHOLD_MODE")
                res["details"]["threshold"] = scan.get("thresholds")
            elif scan["classification"] == "INFEASIBLE_AT_ALL_POINTS":
                flags.add("INFEASIBLE")
            elif scan["classification"] == "ROBUST" and scan.get("certified"):
                res.update(scan["decision"])
                res["decision_valid_for_all_lambda_in_box"] = True
            else:
                res["point_decision"] = None
        elif caps_missing:
            flags.add("THRESHOLD_MODE")
            res["details"]["threshold"] = threshold_mode(work, caps_missing, model, usable, method, beta)
        else:
            core = _solve_core(work, model, usable, method, beta)
            res.update(core)
            if core.get("infeasible"):
                flags.add("INFEASIBLE")
    except FollowerLedgerUnidentified as e:
        flags.add("FOLLOWER_LEDGER_UNIDENTIFIED")
        res["details"]["error"] = str(e)
    except NotComparable as e:
        flags.add("NOT_COMPARABLE")
        res["details"]["error"] = str(e)
    except ModelAInfeasible as e:
        flags.add("INFEASIBLE")
        res["details"]["error"] = str(e)
    except MissingInput as e:
        flags.add("REJECT_INSUFFICIENT_IDENTIFIED_INPUTS")
        res["details"]["error"] = str(e)
    excluded = _restricted_log(probe, usable, allow_shared)
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
        unused += [("lam_u", r) for r in _roles_in_use(work) if work["lam_u"].get(r) is None]
        if unused:
            res["details"].setdefault("unidentified_inputs_not_used_by_this_model", []).extend(sorted(unused, key=str))
    if not flags:
        flags.add("OK_POINT")
    return _finish(res, flags)


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
        _, _, charge, gov = shared_terms(inst, sol["y"], sol["gamma"])
        hb = {}
        for p in sol["plans"]:
            for r, h in p["hours_by_role"].items():
                hb[r] = hb.get(r, 0.0) + h
        out = dict(F_E=sol["F"], y=sorted(sol["y"]), gamma=sol["gamma"],
                   configs=sorted(jk for p in sol["plans"] for jk in p["configs"]),
                   y_loc=sorted((inst["initiatives"][p["configs"][0][0]]["unit"], c) for p in sol["plans"] for c in p["loc"]),
                   delta_hours=_portfolio_hours(inst, sol, sol["gamma"]), delta_hours_by_role=hb,
                   F_E_minus_time=sum(p["fE_notime"] for p in sol["plans"]) - charge - gov)
        if method == "dp":
            out.update(dp_exact=sol["dp_exact"], dp_bound=sol["dp_bound"])
        return out
    if model in ("C", "C0"):
        sol = solve_bilevel(inst, gammas, allow_shared=(model == "C"), method=method, beta=beta, log=log)
        if sol["opt"] is None:
            return {"infeasible": True}
        out = dict(F_E={"opt": sol["opt"]["F"], "pess": sol["pess"]["F"] if sol["pess"] else None},
                   y={m: sorted(sol[m]["y"]) for m in sol if sol[m]},
                   gamma={m: sol[m]["gamma"] for m in sol if sol[m]},
                   envelopes={m: sol[m]["env"] for m in sol if sol[m]})
        if method == "dp":
            out.update(dp_exact=sol["opt"]["dp_exact"], dp_bound=sol["opt"]["dp_bound"])
        return out
    if model == "A":
        if len(gammas) != 1:
            raise InvalidInput("Model A requires exactly one policy")
        a = solve_independent(inst, gammas[0])
        return dict(F_E=a)
    raise InvalidInput(f"unknown model {model}")


def threshold_mode(inst, caps_missing, model, gammas, method, beta):
    """F_c UNIDENTIFIED (models B and C only): report F_c^dagger = sup{F : building c is optimal}, with other
    missing caps forced off. Never sets F_c = 0 in a reported solution, never forces y_c = 0. For C both the
    optimistic and the pessimistic threshold are reported. Bisection assumes 'built' is monotone in F_c, which
    holds in B (the value of every y containing c falls one-for-one in F_c, others unchanged) and in C for the
    same reason at fixed follower responses (responses do not depend on F_c)."""
    if model not in SHARED_MODELS:
        raise InvalidInput("THRESHOLD_MODE is defined only for models with shared capabilities (B, C)")
    out = {}
    hi_b = inst["A_bar"]["BUD"]
    modes = ("opt", "pess") if model == "C" else ("point",)
    for c in caps_missing:
        forced = {o: False for o in caps_missing if o != c}
        res_c = {}
        for mode in modes:
            def built(F):
                i = copy.deepcopy(inst)
                i["caps"][c]["F"] = F
                for o in caps_missing:
                    if o != c:
                        i["caps"][o]["F"] = 0.0          # never built (forced off); value irrelevant
                if model == "C":
                    s_ = solve_bilevel(i, gammas, forced=forced, method=method, beta=beta)[mode]
                else:
                    s_ = solve_central(i, gammas, forced=forced, method=method, beta=beta)
                return s_ is not None and c in s_["y"]
            lo, hi = 0.0, hi_b
            if not built(lo):
                res_c[mode] = dict(F_dagger=None, statement=f"{c} is not built even at F_c=0; F_c^dagger undefined (<0)")
                continue
            if built(hi):
                res_c[mode] = dict(F_dagger=hi, statement=f"{c} built for every F_c <= pooled budget")
                continue
            for _ in range(50):
                mid = 0.5 * (lo + hi)
                lo, hi = (mid, hi) if built(mid) else (lo, mid)
            res_c[mode] = dict(F_dagger=0.5 * (lo + hi),
                               statement=f"y_{c}* = 1 iff F_{c} <= F_dagger (other missing capabilities forced off)")
        out[c] = res_c["point"] if model != "C" else res_c
        if model != "C":
            out[c]["joint_threshold_computed"] = len(caps_missing) == 1
    return out


def _decision_sig(s):
    return json.dumps(_canon({k: s.get(k) for k in ("infeasible", "y", "gamma", "configs", "envelopes", "y_loc")}), sort_keys=True)


def lambda_scan(inst, model, gammas, roles, method, beta, grid=4, caps_missing=()):
    """Scan the pre-registered box [0, lambda^U]^m over the missing roles. Solves inside the scan are always
    exhaustive (exact), whatever method the caller asked for, so a certificate is never built on approximations.
    B / A+: for a fixed portfolio F_E is affine in lambda and feasibility does not depend on lambda, so a
    portfolio optimal at all 2^m vertices is optimal on the whole box -> 'certified'. C / C0: the pessimistic
    value is a minimum over follower tie sets, so a grid of (grid+1)^m points is used; a common decision on the
    grid is reported as ROBUST_ON_GRID and is NOT certified (no point decision is emitted). A: no leader decision."""
    lamU = inst.get("lam_U", {})
    if any(lamU.get(r) is None for r in roles):
        return dict(classification="UNIDENTIFIED", reason="no upper bound lambda^U for some role", certified=False)
    if model == "A":
        return dict(classification="NO_LEADER_DECISION", certified=False,
                    reason="Model A has no leader decision; its value is not identified without lambda")
    exact = model in ("B", "Aplus")
    pts = list(itertools.product(*[[0.0, lamU[r]] if exact else [lamU[r] * t / grid for t in range(grid + 1)]
                                   for r in roles]))
    decisions, sols, thresholds = {}, None, []
    for pt in pts:
        i = copy.deepcopy(inst)
        i["_lam_override"] = dict(zip(roles, pt))
        if caps_missing:
            thresholds.append((pt, threshold_mode(i, caps_missing, model, gammas, "enum", beta)))
            continue
        s = _solve_core(i, model, gammas, "enum", beta)
        sig = _decision_sig(s)
        decisions.setdefault(sig, []).append(pt)
        if sols is None:
            sols = s
    out = dict(method="vertex (exact)" if exact else f"grid {(grid + 1)}^{len(roles)} (coverage only)",
               points=len(pts), box={r: [0.0, lamU[r]] for r in roles}, solver_inside_scan="enum (exact)")
    if caps_missing:
        out.update(classification="THRESHOLD_BY_LAMBDA_POINT", thresholds=thresholds, certified=False)
        return out
    if len(decisions) == 1 and sols.get("infeasible"):
        out.update(classification="INFEASIBLE_AT_ALL_POINTS", certified=exact)
        return out
    if len(decisions) == 1:
        out["classification"] = "ROBUST" if exact else "ROBUST_ON_GRID"
        out["certified"] = exact
        out["decision"] = {k: sols[k] for k in ("y", "gamma", "configs", "y_loc", "envelopes", "delta_hours",
                                                "delta_hours_by_role", "F_E_minus_time") if k in sols}
    else:
        out.update(classification="FRAGILE", certified=False, distinct_decisions=len(decisions),
                   decision_regions={sig: pts_ for sig, pts_ in decisions.items()})
    return out


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
def _exact(x):
    """Canonical form with EXACT floats (float.hex), used for commitments (no rounding)."""
    if isinstance(x, bool) or x is None or isinstance(x, (int, str)):
        return x
    if isinstance(x, float):
        return {"float": x.hex()}
    if isinstance(x, (frozenset, set)):
        return sorted((_exact(v) for v in x), key=lambda v: json.dumps(v, sort_keys=True, default=str))
    if isinstance(x, (tuple, list)):
        return [_exact(v) for v in x]
    if isinstance(x, dict):
        return sorted([[_exact(k), _exact(v)] for k, v in x.items()], key=lambda kv: json.dumps(kv[0], sort_keys=True, default=str))
    if isinstance(x, Ord):
        return {"ord": [x.construct, _exact(float(x.code)) if isinstance(x.code, float) else x.code]}
    return repr(x)


def _sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()


def registry_hash(reg):
    return _sha(_exact(reg))


def parameter_ranges_hash(reg):
    ranges = {g: [b for b in grp["blocks"]] for g, grp in reg["groups"].items()}
    return _sha(_exact(ranges))


def registry_nominals(reg, inst):
    """Nominal values of every registered target, read from the instance (exact floats)."""
    out = []
    for g in sorted(reg["groups"]):
        for b in reg["groups"][g]["blocks"]:
            if b["kind"] == "scale":
                for path, field in b.get("targets", []):
                    out.append([g, b["name"], list(path), field, _exact(_get(inst, path)[field])])
            else:
                out.append([g, b["name"], list(b["path"]), None, _exact(_get(inst, b["path"]))])
    return out


def registry_commitment(reg, inst):
    """SHA-256 over the registry AND the nominal values it scales/mixes. Computed before a solve; a post-hoc
    change of a range, of eps_R or of any targeted nominal value changes the commitment."""
    return _sha({"registry": _exact(reg), "nominal": registry_nominals(reg, inst)})


def _factor_kind(path, field):
    """Factor kind of a registry target: the multiplicative role the cell plays in the value and slack formulas
    (N, path cell, P, pi, rho, impl, eng, ebar, caps, A_bar, ...). A block must stay inside one kind so that every
    value and slack is affine in each block separately (multilinear in theta) -- the assumption behind every
    vertex argument (Lemma R, MaxRegret, robust feasibility certificates). This is conservative: some
    multi-kind blocks would also be affine, but they are rejected."""
    path = tuple(path)
    if path[:1] == ("initiatives",):
        if len(path) >= 5 and path[2] == "configs":
            return path[4]
        if len(path) >= 4 and path[2] == "configs":
            return field
        return path[2] if len(path) > 2 else field
    return path[0]


def validate_registry(reg, inst):
    """Rejects (InvalidInput) registries whose blocks would break the multilinear structure or overwrite each
    other: unknown target, non-numeric target, a block spanning several factor classes, two blocks touching the
    same cell, a probability block whose vertices are not normalized, or a scale range with L > U."""
    for g, grp in reg["groups"].items():
        seen = {}
        for b in grp["blocks"]:
            if b["kind"] == "scale":
                if not (isinstance(b["L"], (int, float)) and isinstance(b["U"], (int, float)) and
                        math.isfinite(b["L"]) and math.isfinite(b["U"]) and b["L"] <= b["U"]):
                    raise InvalidInput(f"registry {g}.{b['name']}: scale range invalid")
                classes = set()
                for path, field in b["targets"]:
                    try:
                        v = _get(inst, path)[field]
                    except (KeyError, TypeError, IndexError):
                        raise InvalidInput(f"registry {g}.{b['name']}: unknown target {path}.{field}")
                    if not isinstance(v, (int, float)) or isinstance(v, bool):
                        raise InvalidInput(f"registry {g}.{b['name']}: target {path}.{field} is not numeric")
                    classes.add(_factor_kind(path, field))
                    cell = (tuple(path), field)
                    if cell in seen:
                        raise InvalidInput(f"registry {g}: blocks {seen[cell]} and {b['name']} target the same cell")
                    seen[cell] = b["name"]
                if len(classes) > 1:
                    raise InvalidInput(f"registry {g}.{b['name']}: one block spans several factor kinds {sorted(map(str, classes))}")
            elif b["kind"] == "prob":
                for vtx in b["vertices"]:
                    if any((p is None) or p < -TOL for p in vtx.values()) or not math.isclose(sum(vtx.values()), 1.0, abs_tol=1e-9):
                        raise InvalidInput(f"registry {g}.{b['name']}: vertex not a probability row")
                cell = (tuple(b["path"]), None)
                if any(c[0][:len(b["path"])] == tuple(b["path"]) for c in seen) or cell in seen:
                    raise InvalidInput(f"registry {g}: probability block {b['name']} overlaps another block")
                seen[cell] = b["name"]
            else:
                raise InvalidInput("unknown block kind")
    return True


def verify_registry(result, reg, inst=None):
    ok = result.get("scenario_registry_hash") == registry_hash(reg) and \
        result.get("parameter_ranges_hash") == parameter_ranges_hash(reg)
    if inst is not None:
        ok = ok and result.get("registry_commitment") == registry_commitment(reg, inst)
    return ok


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


def enumerate_portfolios(inst, gamma, allow_shared=True, static_only=False):
    """Fixed portfolios (y, gamma, plans) for Model B. static_only=False: feasible at this instance.
    static_only=True: theta-independent feasibility only (F2-F8; no budget, hours, review or F9 check) -- the
    candidate superset for robust analysis, which is then filtered by robust_feasibility. This avoids
    dropping portfolios that are infeasible at the nominal theta but feasible on the registered set."""
    out = []
    for y in _subsets(_caps_list(inst, allow_shared)):
        sb, se, charge, gov = shared_terms(inst, y, gamma)
        rb, re_ = inst["A_bar"]["BUD"] - sb - gov, inst["A_bar"]["ENG"] - se
        per_u = [unit_plans(inst, u, y, gamma, static_only=static_only) for u in sorted(inst["units"])]
        for combo in itertools.product(*per_u):
            if static_only or (sum(p["bud"] for p in combo) <= rb + TOL and sum(p["eng"] for p in combo) <= re_ + TOL):
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


def block_values(block, mode="grid", grid=4):
    """Values of one block. 'vertex': its vertices. 'grid': scale -> grid+1 equally spaced points;
    prob -> vertices plus 2-vertex mixtures at t/grid."""
    if mode == "vertex":
        return block_vertices(block)
    if block["kind"] == "scale":
        return [("scale", block["L"] + (block["U"] - block["L"]) * t / grid) for t in range(grid + 1)]
    n = len(block["vertices"])
    vals = [("vertex", i) for i in range(n)]
    for a, b in itertools.combinations(range(n), 2):
        for t in range(1, grid):
            w = [0.0] * n
            w[a], w[b] = 1 - t / grid, t / grid
            vals.append(("mix", tuple(w)))
    return vals


def search_points(inst, blocks, grid=3, n_samples=40, seed=20261011):
    """Theta points beyond the vertices (grid of block values and random interior samples), with instances."""
    rng = random.Random(seed)
    pts = [tuple(v) for v in itertools.product(*[block_values(b, "grid", grid) for b in blocks])]
    pts += [tuple(block_sample(b, rng) for b in blocks) for _ in range(n_samples)]
    return [(th, apply_theta(inst, blocks, th)) for th in pts]


def feasibility_class(vertex_rows, search_rows):
    """vertex_rows/search_rows: lists of (theta, static_ok, slacks). Each slack is assumed affine in every
    block separately (multilinear), so its minimum and its maximum over the product polytope are attained at
    vertices.
      ROBUSTLY_FEASIBLE       every slack >= 0 at every vertex (certificate for all theta);
      INFEASIBLE              statically infeasible everywhere, or one slack < 0 at every vertex (certificate);
      CONDITIONALLY_FEASIBLE  some searched theta satisfies ALL constraints jointly (witness reported);
      FEASIBILITY_UNDETERMINED no certificate either way and no joint witness found (the search is finite)."""
    ok = lambda r: r[1] and min(r[2].values()) >= -TOL
    if all(ok(r) for r in vertex_rows):
        return "ROBUSTLY_FEASIBLE", None
    if not any(r[1] for r in vertex_rows):
        return "INFEASIBLE", None
    keys = vertex_rows[0][2].keys()
    if any(all(r[2][k] < -TOL for r in vertex_rows) for k in keys):
        return "INFEASIBLE", None
    for r in list(vertex_rows) + list(search_rows):
        if ok(r):
            return "CONDITIONALLY_FEASIBLE", r[0]
    return "FEASIBILITY_UNDETERMINED", None


def robust_feasibility(inst, gamma, d, blocks, tinst=None, spts=None, witness=False):
    tinst = tinst if tinst is not None else theta_instances(inst, blocks)
    vrows = [(th, *portfolio_slacks(i, gamma, d)[:2]) for th, i in tinst]
    cls, w = feasibility_class(vrows, [])
    if cls == "CONDITIONALLY_FEASIBLE" or cls in ("ROBUSTLY_FEASIBLE", "INFEASIBLE"):
        return (cls, w) if witness else cls
    spts = spts if spts is not None else search_points(inst, blocks)
    srows = [(th, *portfolio_slacks(i, gamma, d)[:2]) for th, i in spts]
    cls, w = feasibility_class(vrows, srows)
    return (cls, w) if witness else cls


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
    """Model B robust solve over one registered group: candidate set = ROBUSTLY_FEASIBLE portfolios drawn from
    the theta-independent superset (not from the nominal-feasible set); returns the minimax-regret decision, its
    MaxRegret (exact: regret is a max of multilinear functions, so its maximum is at a vertex), the whole-portfolio
    Lemma R certificate, feasibility-class counts and the registry commitment."""
    try:
        validate_instance(inst)
        validate_registry(registry, inst)
    except (InvalidInput, TypeError, KeyError) as e:
        return dict(status="INVALID_SCHEMA_OR_UNITS", solver_version=SOLVER_VERSION, details={"error": str(e)})
    commitment = registry_commitment(registry, inst)
    blocks = registry["groups"][group]["blocks"]
    tinst = theta_instances(inst, blocks)
    classes, cands = {}, []
    for d in enumerate_portfolios(inst, gamma, static_only=True):
        tinst_cls = robust_feasibility(inst, gamma, d, blocks, tinst, spts=[])
        classes[tinst_cls] = classes.get(tinst_cls, 0) + 1
        if tinst_cls == "ROBUSTLY_FEASIBLE":
            cands.append(d)
    base = dict(solver_version=SOLVER_VERSION, scenario_registry_hash=registry_hash(registry),
                parameter_ranges_hash=parameter_ranges_hash(registry), registry_commitment=commitment,
                feasibility_classes=classes, provenance_summary=_provenance_summary(inst))
    if not cands:
        return dict(status="INFEASIBLE", **base)
    thetas = theta_grid(blocks)
    vals = regret_table(inst, gamma, cands, thetas, blocks)
    mr = {d: max_regret(vals, d) for d in cands}
    dstar = min(cands, key=lambda d: (mr[d], json.dumps(_canon(d))))
    cert = lemma_r_check(inst, gamma, dstar, cands, blocks)
    return dict(status="OK_INTERVAL", decision=dstar, max_regret=mr[dstar], whole_portfolio_robust=cert["robust"],
                n_candidates=len(cands), **base)


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


def voi_generic(evalf, candidates, blocks, mode="grid", grid=4):
    """Value of identification of each block b:
         VOI_b = MMR(all theta) - sup_v MMR(theta_b = v),
       where MMR over a set is the minimax regret over the candidate set. MMR(all) and each MMR(theta_b = v)
       are exact on vertices of the other blocks (regret is a max of multilinear functions). The sup over v is
       taken over block_values(b, mode): 'vertex' uses only the vertices of b (can overstate VOI because an
       interior v may have larger MMR), 'grid' adds interior values (still an upper bound on the true VOI, and
       never larger than the vertex version). evalf(d, theta) -> value."""
    cache = {}

    def row(th):
        if th not in cache:
            cache[th] = {d: evalf(d, th) for d in candidates}
        return cache[th]

    def mmr(ths):
        return min(max(max(row(t).values()) - row(t)[d] for t in ths) for d in candidates)
    verts = [block_vertices(b) for b in blocks]
    mmr_all = mmr([tuple(v) for v in itertools.product(*verts)])
    out = {}
    for bi, b in enumerate(blocks):
        per_v = {}
        for v in block_values(b, mode, grid):
            others = [verts[i] if i != bi else [v] for i in range(len(blocks))]
            per_v[json.dumps(_canon(v), sort_keys=True)] = mmr([tuple(x) for x in itertools.product(*others)])
        worst = max(per_v, key=per_v.get)
        out[b["name"]] = dict(mode=mode, mmr_all=mmr_all, mmr_given_value=per_v, voi=mmr_all - per_v[worst],
                              worst_value=worst, n_values=len(per_v))
    return out


def portfolio_evalf(inst, gamma, blocks):
    cache = {}

    vals = {}

    def f(d, th):
        if (d, th) in vals:
            return vals[(d, th)]
        if th not in cache:
            cache[th] = apply_theta(inst, blocks, th)
        v = evaluate_portfolio(cache[th], gamma, d)
        if v is None:
            raise ScopeError("candidate infeasible at a theta inside the registered set")
        vals[(d, th)] = v
        return v
    return f


def voi_table(inst, gamma, candidates, blocks, grid=4):
    f = portfolio_evalf(inst, gamma, blocks)
    return dict(vertex=voi_generic(f, candidates, blocks, "vertex"), grid=voi_generic(f, candidates, blocks, "grid", grid))


def robustness_class(groups, element):
    """groups: {group: [optimal-solution list at each theta]}. Element-level classification:
    ROBUST if some element value is optimal at every theta of every group; CONDITIONAL if each group has such a
    value but no common one; FRAGILE otherwise. With finitely many thetas this is a classification ON THE
    EVALUATED POINTS, not a certificate (Lemma R does not extend to elements)."""
    per_g = {g: set.intersection(*[{element(s) for s in theta_sols} for theta_sols in sols])
             for g, sols in groups.items()}
    if set.intersection(*per_g.values()):
        return "ROBUST"
    if all(per_g.values()):
        return "CONDITIONAL"
    return "FRAGILE"


def classify_element(inst, gamma, registry, element, grid=2, n_samples=20, seed=20261011):
    """Element-level classification for Model B over every registered group, using all optima at vertices,
    grid points and random samples. Reports coverage; never labelled a certificate."""
    validate_registry(registry, inst)
    groups, coverage = {}, {}
    for g, grp in sorted(registry["groups"].items()):
        blocks = grp["blocks"]
        pts = theta_grid(blocks)
        nv = len(pts)
        pts += [tuple(v) for v in itertools.product(*[block_values(b, "grid", grid) for b in blocks])]
        rng = random.Random(seed)
        pts += [tuple(block_sample(b, rng) for b in blocks) for _ in range(n_samples)]
        sols = []
        for th in pts:
            r = solve_central(apply_theta(inst, blocks, th), [gamma], all_optima=True)
            sols.append(sorted(r["optima"], key=str) if r else [None])
        groups[g] = sols
        coverage[g] = dict(vertices=nv, grid_and_samples=len(pts) - nv, total=len(pts))
    return dict(classification=robustness_class(groups, element), coverage=coverage,
                note="classification on evaluated points only; not a certificate")


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
    capkey = frozenset({("c_model", "S")})
    ok = copy.deepcopy(inst)
    ok["initiatives"][j]["configs"][1]["rho"][("flag", "junior", capkey)] = {"Use": 1.0}  # capability-state key is legal
    assert validate_instance(ok) and solve(ok, "B", ["g_base"])["status"] == "OK_POINT"
    bad_keys = [("flag", "err", "junior"), ("err", "junior"), ("flag", "junior", "err"), ("flag", "err")]
    for bk in bad_keys:
        b = copy.deepcopy(inst)
        b["initiatives"][j]["configs"][1]["rho"][bk] = {"Use": 1.0}
        _expect_status(solve(b, "B", ["g_base"]), "INVALID_SCHEMA_OR_UNITS")
    b = copy.deepcopy(inst)
    b["initiatives"][j]["configs"][1]["P"] = {("flag", "flag"): 1.0}            # signal/outcome labels collide
    _expect_status(solve(b, "B", ["g_base"]), "INVALID_SCHEMA_OR_UNITS")
    return ("T-SCH-6", "explicit omega leakage guard PASS",
            "rho(r|k,z,role) and rho(r|k,z,role,capability-state) accepted; 4 keys containing omega and 1 signal/outcome label collision "
            "rejected as INVALID_SCHEMA_OR_UNITS")


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

    def feas(inst, j, k=1, y=("c_model",)):
        return jk_eval(inst, j, k, set(y), set(), "g_base")["feasible"]
    inst, j, _ = setup(3, 3)
    assert feas(inst, j)                                                    # R pass / D pass (A=2 needs >=2)
    inst, j, _ = setup(1, 3)
    assert not feas(inst, j)                                                # R fail
    inst, j, _ = setup(3, 1)
    assert not feas(inst, j)                                                # D fail
    inst, j, key = setup(3, 3)
    inst["initiatives"][j]["R_state"][key] = None
    res = solve(inst, "B", ["g_base"])
    assert "RESTRICTED_SOLVE" in res["flags"] and (j, 1, "MissingStateLookup") in res["details"]["excluded_configs"]
    assert "UNEVALUABLE_INITIATIVE" not in res["flags"]
    inst3, j3, key3 = setup(3, 3)
    del inst3["initiatives"][j3]["R_state"][key3]                           # absent cell, not just None
    assert (j3, 1, "MissingStateLookup") in solve(inst3, "B", ["g_base"])["details"]["excluded_configs"]
    # status quo (k = 0): F5e is evaluated at the capability state actually chosen, for every k.
    # A requirement at the scale minimum needs no lookup; above it, a missing lookup excludes k = 0 in THAT state only.
    i4, j4, key4 = setup(3, 3)
    i4["initiatives"][j4]["D_state"][frozenset()] = None
    r4 = solve(i4, "B", ["g_base"])                                          # D_req(A=0) is the minimum: no lookup
    assert r4["status"] == "OK_POINT", r4["status"]
    i5 = copy.deepcopy(i4)
    i5["D_req"][O("A", 0)] = O("D", 1)
    r5 = solve(i5, "B", ["g_base"])
    assert (j4, 0, "MissingStateLookup") in r5["details"]["excluded_configs"] and "UNEVALUABLE_INITIATIVE" not in r5["flags"]
    i6 = copy.deepcopy(i5)
    i6["initiatives"][j4]["D_state"][frozenset()] = O("D", 3)
    i6["initiatives"][j4]["D_state"][key4] = O("D", 0)
    assert feas(i6, j4, 0, ()) and not jk_eval(i6, j4, 0, {"c_model"}, set(), "g_base")["static_ok"]
    # capability-state rho rows are used when the state matches, ignored otherwise
    i7, j7, key7 = setup(3, 3)
    i8 = copy.deepcopy(i7)
    for z in ("flag", "noflag"):
        for r in ("junior", "senior"):
            i7["initiatives"][j7]["configs"][1]["rho"][(z, r, key7)] = {"Use": 1.0, "Verify": 0.0, "Reject": 0.0}
            i8["initiatives"][j7]["configs"][1]["rho"][(z, r)] = {"Use": 1.0, "Verify": 0.0, "Reject": 0.0}
    a7 = jk_eval(i7, j7, 1, {"c_model"}, set(), "g_base")["phiE"]
    a8 = jk_eval(i8, j7, 1, {"c_model"}, set(), "g_base")["phiE"]
    base = jk_eval(setup(3, 3)[0], j7, 1, {"c_model"}, set(), "g_base")["phiE"]
    assert close(a7, a8) and not close(a7, base)
    loc = jk_eval(i7, j7, 1, set(), {"c_model"}, "g_base")["phiE"]          # state (c_model, L): base rows
    assert close(loc, jk_eval(setup(3, 3)[0], j7, 1, set(), {"c_model"}, "g_base")["phiE"])
    # relabel R/D (and every other ordinal) by a strictly increasing map: same feasibility and same solution
    codes = {k: {0: -5.0, 1: 0.1, 2: 0.11, 3: 77.0} for k in DEFAULT_CODES}
    for lv in ((3, 3), (1, 3), (3, 1)):
        a, ja, _ = setup(*lv)
        b, jb, _ = setup(*lv, codes=codes)
        assert feas(a, ja) == feas(b, jb)
        sa, sb = solve(a, "B", ["g_base"]), solve(b, "B", ["g_base"])
        assert sa["configs"] == sb["configs"] and close(sa["F_E"], sb["F_E"])
    return ("T-ALG-1", "F5e PASS", "R pass/D pass feasible; R fail and D fail infeasible; missing R(s) -> that (j,k) excluded, RESTRICTED_SOLVE, "
            "initiative kept; absent cell not defaulted; status quo checked at the chosen state (scale-minimum requirement needs no "
            "lookup; otherwise missing lookup excludes k=0 in that state only; same k=0 feasible in one state and not another); "
            "capability-state rho rows used only in their state; relabel-invariant")


def t_state_machine():
    seen = {}
    base = make_instance(5)
    r = solve(base, "B", ["g_base"]); _expect_status(r, "OK_POINT"); seen["OK_POINT"] = 1
    for key in ("status", "flags", "model", "solver_version", "provenance_summary", "F_E", "y", "configs", "delta_hours",
                "delta_hours_by_role", "F_E_minus_time"):
        assert key in r, key
    i = copy.deepcopy(base); i["A_bar"]["BUD"] = None
    _expect_status(solve(i, "B", ["g_base"]), "REJECT_INSUFFICIENT_IDENTIFIED_INPUTS"); seen["REJECT_INSUFFICIENT_IDENTIFIED_INPUTS"] = 1
    i = copy.deepcopy(base); i["caps"]["c_model"]["F"] = float("nan")
    _expect_status(solve(i, "B", ["g_base"]), "INVALID_SCHEMA_OR_UNITS"); seen["INVALID_SCHEMA_OR_UNITS"] = 1
    for garbage in ({}, {"units": ["U1"]}, None):                          # malformed objects never raise
        _expect_status(solve(garbage, "B"), "INVALID_SCHEMA_OR_UNITS")
    _expect_status(solve(base, "Z", ["g_base"]), "INVALID_SCHEMA_OR_UNITS")
    i = copy.deepcopy(base); i["B0"]["U1"]["BUD"] = 1e6
    _expect_status(solve(i, "A", ["g_base"]), "NOT_COMPARABLE"); seen["NOT_COMPARABLE"] = 1
    i = copy.deepcopy(base); i["initiatives"]["U1_j0"]["configs"][1]["impl_x"] = None
    assert solve(i, "B", ["g_base"])["status"] in ("OK_POINT",)
    _expect_status(solve(i, "C", ["g_base"]), "FOLLOWER_LEDGER_UNIDENTIFIED"); seen["FOLLOWER_LEDGER_UNIDENTIFIED"] = 1
    i = copy.deepcopy(base); i["policies"]["g_base"]["must"] = set(i["initiatives"]); i["A_bar"]["BUD"] = 1.0
    _expect_status(solve(i, "B", ["g_base"]), "INFEASIBLE"); seen["INFEASIBLE"] = 1
    i = copy.deepcopy(base); i["policies"]["g_base"]["must"] = set(i["initiatives"]); i["B0"]["U1"]["BUD"] = 0.0
    _expect_status(solve(i, "A", ["g_base"]), "INFEASIBLE")                 # Model A infeasible is INFEASIBLE, not INVALID
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
        i["policies"]["g_base"]["allow"][(j, 2)] = 0
        i["policies"]["g_base"]["ebar"][j] = ini["N"][0] * expect(ini["configs"][0], lambda x, r: x["I_sev"]) + 0.5
    dr = design_response_analysis(i, "g_base")
    assert dr["status"] == "DESIGN_INFEASIBLE_UNDER_RESPONSE", dr; seen["DESIGN_INFEASIBLE_UNDER_RESPONSE"] = 1
    small = make_instance(5, n_init=1)
    rr = solve_robust(small, "g_base", make_registry(small), "g1")
    assert rr["status"] == "OK_INTERVAL"; seen["OK_INTERVAL"] = 1
    missing = set(STATUS_ORDER) - set(seen)
    assert not missing, missing
    return ("STATE", "state-machine/output-contract PASS",
            f"all {len(STATUS_ORDER)} statuses reachable and returned as results; malformed objects and an unknown model return "
            "INVALID_SCHEMA_OR_UNITS; Model A infeasibility returns INFEASIBLE (no exception path)")


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
    # C reports optimistic AND pessimistic thresholds, each consistent with explicit solves
    rc = solve(i, "C", ["g_base"])
    _expect_status(rc, "THRESHOLD_MODE")
    tc = rc["details"]["threshold"]["c_model"]
    assert set(tc) == {"opt", "pess"}
    for mode in ("opt", "pess"):
        fd = tc[mode]["F_dagger"]
        if fd is not None:
            for F in (fd * 0.5, fd * 1.5 + 1.0):
                ii = copy.deepcopy(inst); ii["caps"]["c_model"]["F"] = F
                assert ("c_model" in solve_bilevel(ii, ["g_base"], forced={"c_eval": False})[mode]["y"]) == (F <= fd), (mode, F, fd)
    # models without shared capabilities do not use F_c: solved, and the missing input recorded as unused
    for m in ("Aplus", "C0"):
        ra = solve(i, m, ["g_base"])
        assert ra["status"] == "OK_POINT" and ("caps.F", "c_model") in ra["details"]["unidentified_inputs_not_used_by_this_model"], (m, ra["status"])
    return ("T-MIS-3", "missing F_c threshold mode PASS",
            f"B: THRESHOLD_MODE with F_c^dagger={Fd:.3f} consistent with 8 explicit F_c solves; no point decision; differs from F_c=0. "
            f"C: opt/pess thresholds ({tc['opt']['F_dagger']}, {tc['pess']['F_dagger']}) consistent with explicit solves. "
            "A+ and C0: solved, F_c recorded as UNIDENTIFIED-unused")


def t_mis4_partial():
    inst = make_instance(5)
    i = copy.deepcopy(inst); i["lam"]["senior"] = None
    r = solve(i, "B", ["g_base"])
    _expect_status(r, "PARTIAL_OBJECTIVE")
    scan = r["details"]["lambda_scan"]
    assert "F_E" not in r and scan["classification"] in ("ROBUST", "FRAGILE") and scan["method"] == "vertex (exact)"
    if scan["classification"] == "ROBUST":
        assert r["decision_valid_for_all_lambda_in_box"] and "F_E_minus_time" in r and "delta_hours_by_role" in r
        # exactness of the vertex check: a dense grid on [0, lambda^U] never finds another decision
        for t in range(11):
            g = copy.deepcopy(inst); g["lam"]["senior"] = inst["lam_U"]["senior"] * t / 10
            sg = solve_central(g, ["g_base"])
            assert sorted(sg["y"]) == r["y"] and sorted(jk for p in sg["plans"] for jk in p["configs"]) == r["configs"]
        # F_E^-time removes ALL lambda terms (also the identified junior one)
        z = copy.deepcopy(inst); z["lam"] = {"junior": 0.0, "senior": 0.0}
        zr = _solve_core(z, "B", ["g_base"], "enum", (1.0, 1.0))
        if zr["configs"] == r["configs"] and zr["y"] == r["y"]:
            assert close(zr["F_E"], r["F_E_minus_time"])
    else:
        assert r["point_decision"] is None and "y" not in r and len(scan["decision_regions"]) >= 2
    # a ROBUST case: a narrow box keeps the decision; the point decision is reported and checked on a grid
    n_ = copy.deepcopy(inst); n_["lam"]["senior"] = None; n_["lam_U"]["senior"] = 1e-3
    rn = solve(n_, "B", ["g_base"])
    assert rn["details"]["lambda_scan"]["classification"] == "ROBUST" and rn["decision_valid_for_all_lambda_in_box"]
    for t in range(6):
        g = copy.deepcopy(inst); g["lam"]["senior"] = 1e-3 * t / 5
        sg = solve_central(g, ["g_base"])
        assert sorted(sg["y"]) == rn["y"] and sorted(jk for p in sg["plans"] for jk in p["configs"]) == rn["configs"]
    zz = copy.deepcopy(inst); zz["lam"] = {"junior": 0.0, "senior": 0.0}
    zr = _solve_core(zz, "B", ["g_base"], "enum", (1.0, 1.0))
    if zr["configs"] == rn["configs"] and zr["y"] == rn["y"]:
        assert close(zr["F_E"], rn["F_E_minus_time"])
    assert set(rn["delta_hours_by_role"]) == {"junior", "senior"}
    # a FRAGILE case: a wide box over both roles changes the decision -> no point decision
    w = copy.deepcopy(inst); w["lam"] = {"junior": None, "senior": None}; w["lam_U"] = {"junior": 200.0, "senior": 200.0}
    rw = solve(w, "B", ["g_base"])
    assert rw["status"] == "PARTIAL_OBJECTIVE" and rw["details"]["lambda_scan"]["points"] == 4
    if rw["details"]["lambda_scan"]["classification"] == "FRAGILE":
        assert rw["point_decision"] is None and "configs" not in rw
    # absent key (not just None) is detected
    a = copy.deepcopy(inst); del a["lam"]["senior"]
    assert solve(a, "B", ["g_base"])["status"] == "PARTIAL_OBJECTIVE"
    # the override never touches the follower ledger lambda_u: C with lam_u.senior missing is LEDGER-UNIDENTIFIED
    c = copy.deepcopy(i); c["lam_u"]["senior"] = None
    assert solve(c, "C", ["g_base"])["status"] == "FOLLOWER_LEDGER_UNIDENTIFIED"
    z = copy.deepcopy(inst); z["lam"]["senior"] = 0.0
    rz = solve(z, "B", ["g_base"])
    assert rz["status"] == "OK_POINT" and "F_E" in rz
    i2 = copy.deepcopy(i); i2["lam_U"]["senior"] = None
    assert solve(i2, "B", ["g_base"])["details"]["lambda_scan"]["classification"] == "UNIDENTIFIED"
    return ("T-MIS-4", "missing lambda partial objective PASS",
            f"PARTIAL_OBJECTIVE; exact 2^m vertex scan of [0,lambda^U] -> {scan['classification']} (confirmed on an 11-point grid); "
            "narrow box -> ROBUST with point decision (confirmed on a grid; F_E^-time equals the lambda=0 objective); "
            f"point decision only when ROBUST, reported as F_E^-time (all lambda terms removed) with delta_hours by role; wide box -> "
            f"{rw['details']['lambda_scan']['classification']}; absent key detected; lambda_u untouched; no lambda^U -> UNIDENTIFIED")


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


DISCLOSURE_KEYS = ("excluded_configs", "unevaluable_initiatives", "lambda_unidentified_roles", "threshold",
                   "unidentified_inputs_not_used_by_this_model", "error", "excluded_policies")


def t_mis6_no_silent_zero():
    rows = {"no_point": 0, "payload_differs": 0, "disclosed": 0}
    for name, site in MISSING_SITES:
        for model in ("B", "C"):
            m, z = make_instance(5), make_instance(5)
            d, k = site(m); d[k] = None
            d2, k2 = site(z); d2[k2] = 0
            rm, rz = solve(m, model, ["g_base"]), solve(z, model, ["g_base"])
            point = rm.get("F_E") is not None or rm.get("configs") is not None or rm.get("y") is not None
            payload = lambda x: json.dumps(_canon({kk: x.get(kk) for kk in ("F_E", "configs", "y", "envelopes")}), sort_keys=True)
            disc_m = {kk: rm["details"].get(kk) for kk in DISCLOSURE_KEYS if rm["details"].get(kk)}
            disc_z = {kk: rz["details"].get(kk) for kk in DISCLOSURE_KEYS if rz["details"].get(kk)}
            if not point:
                rows["no_point"] += 1
            elif payload(rm) != payload(rz):
                rows["payload_differs"] += 1
            else:
                # same point decision as zero-fill (e.g. a missing permission treated as "not allowed"): only
                # acceptable if the missing input is DISCLOSED in the result and the zero-filled run discloses nothing
                assert disc_m and json.dumps(_canon(disc_m), sort_keys=True) != json.dumps(_canon(disc_z), sort_keys=True), (name, model)
                rows["disclosed"] += 1
            if not (model == "B" and "ledger" in name):
                assert rm["status"] != "OK_POINT", (name, model, rm["status"])
    n = sum(rows.values())
    return ("T-MIS-6", "no silent zero fill PASS",
            f"{n} mutations ({len(MISSING_SITES)} missing classes x models B and C) vs zero-fill: {rows['no_point']} emit no point decision, "
            f"{rows['payload_differs']} emit a different decision/objective, {rows['disclosed']} emit the zero-fill decision but disclose "
            "the UNIDENTIFIED input (excluded configuration or unused-by-model) while the zero-filled run discloses nothing")


def t_orc9_dp():
    n, binding = 0, 0
    for s_ in range(1, 21):
        inst = make_instance(100 + s_, aligned=(s_ % 2 == 0), integer=True)
        inst["A_bar"]["BUD"] = float(round(inst["A_bar"]["BUD"] * 0.3))
        unc = copy.deepcopy(inst); unc["A_bar"]["BUD"] = 1e9
        e, d = solve_central(inst, ["g_base"]), solve_central(inst, ["g_base"], method="dp")
        assert (e is None and d is None) or (close(e["F"], d["F"]) and d["dp_exact"]), (s_,)
        if e is not None and solve_central(unc, ["g_base"])["F"] > e["F"] + 1e-6:
            binding += 1
        ce, cd = solve_bilevel(inst, ["g_base"]), solve_bilevel(inst, ["g_base"], method="dp")
        for mode in ("opt", "pess"):
            assert (ce[mode] is None and cd[mode] is None) or (close(ce[mode]["F"], cd[mode]["F"]) and cd[mode]["dp_exact"]), (s_, mode)
        for forced in ({"c_model": True}, {"c_model": False}):
            fe = solve_central(inst, ["g_base"], forced=forced)
            fd = solve_central(inst, ["g_base"], forced=forced, method="dp")
            assert (fe is None and fd is None) or close(fe["F"], fd["F"])
        n += 1
    assert binding >= 5, binding
    # random multiple-choice knapsack fuzz against enumeration
    rng = random.Random(909)
    for _ in range(400):                                                   # integer weights, mixed signs
        G = [[(float(rng.randint(-5, 9)), float(rng.randint(-3, 6)), rng.uniform(-10, 10)) for _ in range(rng.randint(1, 4))]
             for _ in range(rng.randint(1, 4))]
        cb, ce_ = float(rng.randint(-4, 15)), float(rng.randint(-3, 10))
        ve, _ = mck_enum(G, cb, ce_)
        vd, _, ex, bd = mck_dp(G, cb, ce_)
        assert ex and bd == 0.0 and ((ve is None and vd is None) or close(ve, vd)), (G, cb, ce_, ve, vd)
    silent, inexact = 0, 0
    for _ in range(400):                                                   # non-integer weights, quantum 0.5
        G = [[(rng.uniform(-3, 6), rng.uniform(-2, 5), rng.uniform(-10, 10)) for _ in range(rng.randint(1, 4))]
             for _ in range(rng.randint(1, 4))]
        cb, ce_ = rng.uniform(-2, 10), rng.uniform(-2, 8)
        ve, _ = mck_enum(G, cb, ce_)
        vd, combo, ex, bd = mck_dp(G, cb, ce_, 0.5, 0.5)
        if ve is not None and vd is None:
            silent += 1
        if ve is not None:
            assert vd is not None and vd <= ve + 1e-7 and ve <= vd + bd + 1e-7, (ve, vd, bd)
            assert sum(c[0] for c in combo) <= cb + 1e-7 and sum(c[1] for c in combo) <= ce_ + 1e-7
            inexact += (not ex)
        else:
            assert vd is None
    assert silent == 0
    # forced fallback: ceil-rounding infeasible, relaxation feasible -> enumeration, exact
    G = [[(0.0, 0.5, 1.0), (0.5, 0.0, 1.0)], [(0.0, 0.5, 1.0), (0.5, 0.0, 1.0)]]
    before = DP_STATS["fallback_enum"]
    v, _, ex, bd = mck_dp(G, 0.5, 0.5)
    assert close(v, 2.0) and ex and DP_STATS["fallback_enum"] == before + 1
    tie = tie_instance()
    te, td = solve_bilevel(tie, ["g_base"]), solve_bilevel(tie, ["g_base"], method="dp", beta=(1e-3, 1e-3))
    assert te["opt"]["F"] > te["pess"]["F"] + 1e-6
    for mode in ("opt", "pess"):
        assert td[mode]["F"] <= te[mode]["F"] + 1e-7 and te[mode]["F"] <= td[mode]["F"] + td[mode]["dp_bound"] + 1e-7
    inst = make_instance(7)                                                # non-integer: not exact, bound reported
    e, d = solve_central(inst, ["g_base"]), solve_central(inst, ["g_base"], method="dp", beta=(1.0, 1.0))
    assert not d["dp_exact"] and d["F"] <= e["F"] + 1e-7 and e["F"] <= d["F"] + d["dp_bound"] + 1e-7
    return ("T-ORC-9", "DP == exhaustive PASS",
            f"{n} integer seeds with budget x0.3 (binding in {binding}): B, C-opt, C-pess, capability forced on/off equal and exact; "
            f"400 random integer MCK instances (mixed-sign weights) DP == enumeration; 400 non-integer instances: enumeration in "
            f"[DP, DP+bound], 0 silent infeasibilities ({inexact} inexact); ceil-infeasible branch falls back to enumeration; "
            f"ties respected; non-integer portfolio flagged inexact with bound {d['dp_bound']:.3f}")


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
    chosen_normal = 0
    for s_ in range(1, 9):
        inst = make_instance(s_, aligned=(s_ % 2 == 0))
        inst["A_bar"]["BUD"] = 1e9                                         # every option affordable
        B, Ap = solve_central(inst, ["g_base"]), solve_central(inst, ["g_base"], allow_shared=False)
        assert B["F"] >= Ap["F"] - 1e-7
        chosen_normal += bool(B["y"])
        big = copy.deepcopy(inst)
        for c in big["caps"]:
            big["caps"][c]["F"] *= 1e4
        Bb, Apb = solve_central(big, ["g_base"]), solve_central(big, ["g_base"], allow_shared=False)
        assert not Bb["y"] and close(Bb["F"], Apb["F"])
        # the large-F_c portfolio is affordable: it is rejected on value, not on the budget
        forced = solve_central(big, ["g_base"], forced={c: True for c in big["caps"]})
        assert forced is not None and forced["F"] < Bb["F"]
    assert chosen_normal >= 1
    return ("T-ORC-10", "high-F_c shared limit PASS",
            f"budget non-binding: VSC >= 0 on 8 seeds; shared capability chosen at normal F_c in {chosen_normal}/8 seeds; with F_c x 1e4 "
            "the all-shared portfolio is still affordable but has lower value, no shared capability is chosen and VSC = 0")


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
            rk_ = lambda rk: (rk[0], R[rk[1]]) + ((pat(rk[2]),) if len(rk) == 3 else ())
            nc["rho"] = {rk_(rk): dict(v) for rk, v in cfg["rho"].items()}
            nc["rho_design"] = {rk_(rk): dict(v) for rk, v in cfg.get("rho_design", {}).items()}
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
        allp = enumerate_portfolios(inst, "g_base", static_only=True)
        cls = {d: robust_feasibility(inst, "g_base", d, blocks, tinst, spts=[]) for d in allp}
        cands = [d for d in allp if cls[d] == "ROBUSTLY_FEASIBLE"]
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
        if cert["robust"] and all(c in ("ROBUSTLY_FEASIBLE", "INFEASIBLE") for c in cls.values()):
            # a certified whole portfolio implies its elements are ROBUST on every evaluated point -- valid only when
            # no portfolio is merely conditionally feasible (otherwise classify_element compares against portfolios
            # outside Lemma R's candidate set)
            y_star = tuple(picks[0][0])
            ce = classify_element(inst, "g_base", {"groups": {"g1": reg["groups"]["g1"]}}, lambda sig: tuple(sig[0]) if sig else None,
                                  grid=2, n_samples=8)
            assert ce["classification"] == "ROBUST", (seed, ce)
    assert certified >= 1 and violated >= 1, (certified, violated)
    for model, scope in (("C", "whole_portfolio"), ("B", "element")):
        try:
            lemma_r_check(inst, "g_base", cands[0], cands, blocks, model=model, scope=scope)
            raise AssertionError("scope guard failed")
        except ScopeError:
            pass
    # element-level counterexample (42 §13.3): y=1 via portfolio a or b at every vertex, but y=0 optimal inside
    vals = lambda th: {"y1_a": th, "y1_b": 1 - th, "y0": 0.6}
    at_vertices = all(max(vals(t)["y1_a"], vals(t)["y1_b"]) >= vals(t)["y0"] for t in (0.0, 1.0))
    interior = max(vals(0.5)["y1_a"], vals(0.5)["y1_b"]) >= vals(0.5)["y0"]
    assert at_vertices and not interior
    opt = lambda th: [d for d, v in vals(th).items() if v >= max(vals(th).values()) - 1e-12]
    elem = lambda d: d.startswith("y1")
    assert robustness_class({"g": [opt(0.0), opt(1.0)]}, elem) == "ROBUST"                   # vertices only: wrong
    assert robustness_class({"g": [opt(t / 4) for t in range(5)]}, elem) == "FRAGILE"         # with interior points
    assert robustness_class({"g1": [["a"], ["a", "b"]], "g2": [["a"]]}, lambda x: x) == "ROBUST"
    assert robustness_class({"g1": [["a"], ["a"]], "g2": [["b"], ["b"]]}, lambda x: x) == "CONDITIONAL"
    assert robustness_class({"g1": [["a"], ["b"]], "g2": [["a"]]}, lambda x: x) == "FRAGILE"
    return ("T-SEN-3", "Lemma R scope test PASS",
            f"{certified} certified whole portfolios: 60 interior samples per seed found no violation and element classification on "
            f"vertices+grid+samples agreed (ROBUST); {violated} uncertified: vertex gap <= sampled gap; ScopeError for Model C and "
            "element scope; element-level counterexample: vertex-only classification says ROBUST, adding interior points gives FRAGILE; "
            "robustness_class ROBUST/CONDITIONAL/FRAGILE unit cases")


def t_sen4_robust_feasibility():
    inst = make_instance(31, n_init=1)
    j = "U1_j0"
    sq = inst["initiatives"][j]["N"][0] * expect(inst["initiatives"][j]["configs"][0], lambda x, r: x["I_sev"])
    inst["policies"]["g_base"]["ebar"][j] = sq * 1.05
    cells = [(("initiatives", j, "configs", 1, "path", key), "I_sev") for key in inst["initiatives"][j]["configs"][1]["path"]]
    blocks = [dict(name="Isev_scale", kind="scale", targets=cells, L=0.5, U=6.0)]
    ports = enumerate_portfolios(inst, "g_base", static_only=True)
    classes, witnesses = {}, {}
    for d in ports:
        c, w = robust_feasibility(inst, "g_base", d, blocks, witness=True)
        classes.setdefault(c, []).append(d)
        if c == "CONDITIONALLY_FEASIBLE":
            witnesses[d] = w
    assert classes.get("CONDITIONALLY_FEASIBLE") and classes.get("ROBUSTLY_FEASIBLE")
    for d, w in witnesses.items():                                         # every witness is jointly feasible
        assert evaluate_portfolio(apply_theta(inst, blocks, w), "g_base", d) is not None
    uses = lambda d: any((j, 1) in configs for configs, _ in d[1])
    assert any(uses(d) for d in classes["CONDITIONALLY_FEASIBLE"])
    assert not any(uses(d) for d in classes["ROBUSTLY_FEASIBLE"])
    big = [dict(name="Isev_scale", kind="scale", targets=cells, L=50.0, U=60.0)]
    assert any(robust_feasibility(inst, "g_base", d, big) == "INFEASIBLE" for d in ports if uses(d))
    reg = {"groups": {"g1": {"blocks": blocks}}, "eps_R": 0.0, "tie_tol": 1e-9, "seed": 1}
    rr = solve_robust(inst, "g_base", reg, "g1")
    assert not uses(rr["decision"])
    # jointly infeasible everywhere although each constraint holds at some vertex: must NOT be CONDITIONAL
    rows = lambda ths: [(("scale", t), True, {"a": t - 0.6, "b": 0.4 - t}) for t in ths]
    assert feasibility_class(rows([0.0, 1.0]), rows([x / 20 for x in range(21)]))[0] == "FEASIBILITY_UNDETERMINED"
    ok_rows = lambda ths: [(("scale", t), True, {"a": t - 0.3, "b": 0.7 - t}) for t in ths]
    c, w = feasibility_class(ok_rows([0.0, 1.0]), ok_rows([x / 20 for x in range(21)]))
    assert c == "CONDITIONALLY_FEASIBLE" and 0.3 <= w[1] <= 0.7
    return ("T-SEN-4", "robust feasibility PASS",
            f"{len(classes['ROBUSTLY_FEASIBLE'])} robust / {len(classes['CONDITIONALLY_FEASIBLE'])} conditional (each with a jointly "
            f"feasible witness) / {len(classes.get('INFEASIBLE', []))} infeasible / {len(classes.get('FEASIBILITY_UNDETERMINED', []))} "
            "undetermined; the risk-sensitive config never robust and excluded from the robust candidate set; INFEASIBLE when violated "
            "at every vertex; jointly-infeasible-everywhere case -> FEASIBILITY_UNDETERMINED, not CONDITIONAL")


def t_sen6_registry():
    inst = make_instance(8, n_init=1)
    reg = make_registry(inst)
    pre = registry_commitment(reg, inst)                                   # committed BEFORE the solve
    r = solve_robust(inst, "g_base", reg, "g1")
    r2 = solve(inst, "B", ["g_base"], registry=reg)
    assert r["registry_commitment"] == pre and verify_registry(r, reg, inst)
    for x in (r, r2):
        assert len(x["scenario_registry_hash"]) == 64 and len(x["parameter_ranges_hash"]) == 64
        assert x["solver_version"] == SOLVER_VERSION and "provenance_summary" in x
        assert verify_registry(x, reg)
    tampered = copy.deepcopy(reg)
    tampered["groups"]["g1"]["blocks"][0]["U"] = 9.9
    assert not verify_registry(r, tampered)
    tampered2 = copy.deepcopy(reg); tampered2["eps_R"] = 1.0
    assert not verify_registry(r, tampered2)
    tiny = copy.deepcopy(reg); tiny["groups"]["g1"]["blocks"][0]["U"] = reg["groups"]["g1"]["blocks"][0]["U"] + 1e-12
    assert registry_hash(tiny) != registry_hash(reg)                         # no rounding in the commitment
    nom = copy.deepcopy(inst)
    path, field = next(t for t in reg["groups"]["g1"]["blocks"][0]["targets"] if _get(inst, t[0])[t[1]] != 0)
    _get(nom, path)[field] = _get(nom, path)[field] * (1 + 1e-12)            # tamper with a targeted NOMINAL value
    assert verify_registry(r, reg) and not verify_registry(r, reg, nom)
    nomP = copy.deepcopy(inst)
    _get(nomP, ("initiatives", "U2_j0", "configs", 1, "P"))[("flag", "ok")] += 0.0
    assert verify_registry(r, reg, nomP)
    return ("T-SEN-6", "scenario registry hashing PASS",
            "registry, parameter-range and registry-commitment SHA-256 (exact float.hex, registry + targeted nominal values) emitted "
            "and committed before solving; post-hoc change of a range, of eps_R, of a range by 1e-12, or of a targeted nominal value by "
            "a relative 1e-12 detected; an unchanged instance verifies")


def t_sen7_regret_voi():
    # (1) analytic oracle: F_A = 1-v, F_B = v, F_D = q, F_E = 1-q, v,q in [0,1].
    #     MMR(all) = 1; MMR(v fixed) = min(v, 1-v) is maximal at the interior point v = 1/2, so the true VOI_v = 0.5,
    #     while conditioning only on vertices of v gives 1.
    blocks = [dict(name="v", kind="scale", L=0.0, U=1.0), dict(name="q", kind="scale", L=0.0, U=1.0)]
    F = {"A": lambda v, q: 1 - v, "B": lambda v, q: v, "D": lambda v, q: q, "E": lambda v, q: 1 - q}
    ev = lambda d, th: F[d](th[0][1], th[1][1])
    vv, vg = voi_generic(ev, list(F), blocks, "vertex"), voi_generic(ev, list(F), blocks, "grid", 4)
    assert close(vv["v"]["mmr_all"], 1.0) and close(vv["v"]["voi"], 1.0) and close(vg["v"]["voi"], 0.5) and close(vg["q"]["voi"], 0.5)
    vg9 = voi_generic(ev, list(F), blocks, "grid", 9)                       # grid without the 1/2 point: upper bound
    assert vg9["v"]["voi"] >= 0.5 - 1e-12 and vg9["v"]["voi"] <= vv["v"]["voi"] + 1e-12
    # (2) MaxRegret: vertex maximum equals the maximum over a dense interior grid (regret is a max of multilinear functions)
    informative = None
    for seed in range(9, 30):
        inst = make_instance(seed, aligned=False, n_init=1)
        reg = make_registry(inst, scale=(0.05, 6.0))
        bl = reg["groups"]["g1"]["blocks"]
        tinst = theta_instances(inst, bl)
        cands = [d for d in enumerate_portfolios(inst, "g_base", static_only=True)
                 if robust_feasibility(inst, "g_base", d, bl, tinst, spts=[]) == "ROBUSTLY_FEASIBLE"]
        thetas = theta_grid(bl)
        vals = regret_table(inst, "g_base", cands, thetas, bl)
        mmr = minimax_regret(vals, cands)
        if mmr <= 1e-6:
            continue
        f = portfolio_evalf(inst, "g_base", bl)
        dense = [tuple(v) for v in itertools.product(*[block_values(b, "grid", 6) for b in bl])]
        best_at = {th: max(f(dd, th) for dd in cands) for th in dense}
        for d in cands:
            dense_mr = max(best_at[th] - f(d, th) for th in dense)
            assert dense_mr <= max_regret(vals, d) + 1e-7, (seed, d)
        voi = voi_table(inst, "g_base", cands, bl, grid=4)
        for name in voi["vertex"]:
            assert -1e-9 <= voi["grid"][name]["voi"] <= voi["vertex"][name]["voi"] + 1e-9
        informative = (seed, mmr, {n: (round(voi["vertex"][n]["voi"], 3), round(voi["grid"][n]["voi"], 3)) for n in voi["vertex"]},
                       len(cands), len(thetas), len(dense))
        break
    assert informative is not None, "no informative instance found"
    seed, mmr, ranking, nc, nt, nd = informative
    return ("T-SEN-7", "MaxRegret PASS / VOI monotonic information test PASS",
            "analytic oracle (F_A=1-v, F_B=v, F_D=q, F_E=1-q): vertex-conditioned VOI_v = 1 (overstated), grid VOI_v = 0.5 = true "
            f"value; portfolio seed {seed}: minimax regret {mmr:.3f} over {nt} vertices and {nc} robust candidates, vertex MaxRegret "
            f"never exceeded on a {nd}-point interior grid; VOI (vertex, grid) per block {ranking}; 0 <= grid VOI <= vertex VOI")


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



def t_audit_regressions():
    """Regression tests for adversarial-audit findings 1, 8 and 11 (50 §7)."""
    # finding 1: a portfolio infeasible at the nominal theta but robustly feasible on the registered set must be a
    # candidate (the nominal theta need not lie in the registered set)
    inst = make_instance(31, n_init=1)
    j = "U1_j0"
    sq = inst["initiatives"][j]["N"][0] * expect(inst["initiatives"][j]["configs"][0], lambda x, r: x["I_sev"])
    inst["policies"]["g_base"]["ebar"][j] = sq * 1.01
    cells = [(("initiatives", j, "configs", k, "path", key), "I_sev") for k in (1, 2) for key in inst["initiatives"][j]["configs"][k]["path"]]
    for path, field in cells:                                                # nominal severity far above tolerance
        _get(inst, path)[field] *= 30.0
    reg = {"groups": {"g1": {"blocks": [dict(name="Isev_low", kind="scale", targets=cells, L=0.01, U=0.03)]}},
           "eps_R": 0.0, "tie_tol": 1e-9, "seed": 1}
    uses = lambda d: any((j, k) in configs for configs, _ in d[1] for k in (1, 2))
    nominal_feasible = enumerate_portfolios(inst, "g_base")
    assert not any(uses(d) for d in nominal_feasible)                        # nominal: AI configs violate F9
    rr = solve_robust(inst, "g_base", reg, "g1")
    assert rr["status"] == "OK_INTERVAL", rr
    blocks = reg["groups"]["g1"]["blocks"]
    robust_using = [d for d in enumerate_portfolios(inst, "g_base", static_only=True)
                    if uses(d) and robust_feasibility(inst, "g_base", d, blocks, spts=[]) == "ROBUSTLY_FEASIBLE"]
    assert robust_using and rr["n_candidates"] > len([d for d in nominal_feasible
                                                      if robust_feasibility(inst, "g_base", d, blocks, spts=[]) == "ROBUSTLY_FEASIBLE"])
    # finding 8a: a missing input in an UNREQUESTED policy never drops an initiative
    i = make_instance(5)
    i["policies"]["g_strict"]["ebar"]["U1_j0"] = None
    r = solve(i, "B", ["g_base"])
    assert r["status"] == "OK_POINT" and "UNEVALUABLE_INITIATIVE" not in r["flags"]
    # finding 8b: missing Allow(j,0) excludes the status quo configuration only, never the initiative
    i = make_instance(5)
    i["policies"]["g_base"]["allow"][("U1_j0", 0)] = None
    r = solve(i, "B", ["g_base"])
    assert "UNEVALUABLE_INITIATIVE" not in r["flags"] and ("U1_j0", 0, "MissingPermission") in r["details"]["excluded_configs"]
    assert r.get("configs") and any(jk[0] == "U1_j0" and jk[1] != 0 for jk in r["configs"])
    # finding 11: covered in T-ALG-1 (k = 0 F5e at the chosen state; capability-state rho rows used)
    # ---- re-review round 2 ----
    base = make_instance(5)
    i = copy.deepcopy(base); i["lam"]["senior"] = None
    i["policies"]["g_base"]["must"] = set(i["initiatives"]); i["A_bar"]["BUD"] = 1.0
    r = solve(i, "B", ["g_base"])
    assert r["status"] == "INFEASIBLE" and "PARTIAL_OBJECTIVE" in r["flags"], r["flags"]       # (1) not INVALID
    i = copy.deepcopy(base); i["lam"]["senior"] = None
    rc = solve(i, "C", ["g_base"])
    assert not rc.get("decision_valid_for_all_lambda_in_box") and "envelopes" not in rc and \
        rc["details"]["lambda_scan"]["certified"] is False                                         # (2) C never certified
    ra = solve(i, "A", ["g_base"])
    assert ra["details"]["lambda_scan"]["classification"] == "NO_LEADER_DECISION" and "F_E" not in ra
    i7 = make_instance(7); i7["lam"]["senior"] = None; i7["lam_U"]["senior"] = 1e-3
    rd = solve(i7, "B", ["g_base"], method="dp", beta=(1.0, 1.0))
    assert rd["details"]["lambda_scan"]["solver_inside_scan"] == "enum (exact)"                     # (3)
    i = copy.deepcopy(base)
    i["initiatives"]["U1_j0"]["configs"][0]["rho"][("flag", "junior", frozenset({("c_model", "S")}))] = {"NA": None}
    r4 = solve(i, "B", ["g_base"])
    assert r4["status"] == "RESTRICTED_SOLVE" and ("U1_j0", 0, "MissingInput") in r4["details"]["excluded_configs"]  # (4)
    assert solve(base, "B", ["g_base"], method="dp", beta=(0.0, 1.0))["status"] == "INVALID_SCHEMA_OR_UNITS"        # (5)
    assert solve(base, "B", ["g_base"], method="dp", beta=(1e-300, 1.0))["status"] == "INVALID_SCHEMA_OR_UNITS"
    small = make_instance(8, n_init=1)
    reg = make_registry(small)
    rs = solve(small, "B", ["g_base"], registry=reg)
    assert verify_registry(rs, reg, small)                                                     # (6)
    bad = copy.deepcopy(reg)                                                                    # (7) overlapping blocks
    bad["groups"]["g1"]["blocks"].append(dict(bad["groups"]["g1"]["blocks"][0], name="dup"))
    assert solve_robust(small, "g_base", bad, "g1")["status"] == "INVALID_SCHEMA_OR_UNITS"
    mixed = copy.deepcopy(reg)                                                                  # one block on N and path
    mixed["groups"]["g1"]["blocks"][0]["targets"] = mixed["groups"]["g1"]["blocks"][0]["targets"] + [(("initiatives", "U1_j0", "N"), 1)]
    assert solve_robust(small, "g_base", mixed, "g1")["status"] == "INVALID_SCHEMA_OR_UNITS"
    assert solve(small, "B", ["g_base"], registry=mixed)["status"] == "INVALID_SCHEMA_OR_UNITS"
    i = copy.deepcopy(base); i["y_cur"] = frozenset({"c_model"}); i["caps"]["c_model"]["F"] = None
    rp = solve(i, "Aplus", ["g_base"])                                                          # F_c used via y_cur
    assert rp["status"] == "REJECT_INSUFFICIENT_IDENTIFIED_INPUTS" and \
        ("caps.F", "c_model") not in rp["details"].get("unidentified_inputs_not_used_by_this_model", [])
    return ("AUDIT", "audit regression PASS",
            f"finding 1: {len(robust_using)} robustly feasible AI portfolios that are infeasible at the nominal theta are now candidates; "
            "finding 8: unrequested-policy gap does not drop an initiative, missing Allow(j,0) excludes only k=0; finding 11 in T-ALG-1; "
            "re-review: missing lambda on an infeasible instance -> INFEASIBLE; C never lambda-certified, A has no leader decision; "
            "lambda scan always exact; status-quo state-local gap -> RESTRICTED_SOLVE; invalid DP quanta -> INVALID; solve(registry) "
            "commits; overlapping or multi-kind registry blocks rejected; A+ with F_c needed via y_cur -> REJECT")


TESTS = [t_sch5_typed_units, t_sch6_omega_guard, t_sch7_nonfinite, t_alg1_f5e, t_state_machine, t_mis3_threshold,
         t_mis4_partial, t_mis6_no_silent_zero, t_orc9_dp, t_orc10_shared_limit, t_orc12_model_d_gate, t_orc13_repro,
         t_inv4_permutation, t_sen3_lemma_r, t_sen4_robust_feasibility, t_sen6_registry, t_sen7_regret_voi,
         t_sen8_delta, t_orc8_independent_hand, t_regression_v21, t_audit_regressions]

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
