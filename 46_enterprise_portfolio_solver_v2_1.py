"""Enterprise AI Portfolio reference solver v2.1 (rev. after Phase F audit) — SYNTHETIC ONLY.

Implements 42_ENTERPRISE_PORTFOLIO_MODEL_v2_1.md by finite exhaustive enumeration:
  Model A  (independent local), C0 (bilevel, no sharing), A+ (central, no sharing),
  B (centralized planner), C (enterprise–business-unit bilevel, optimistic / pessimistic);
  metrics VRA, DL0, VCP, VSC, DL, NEV; governance decomposition EE/RE/CE;
  capability break-even threshold; robustness-class logic.

No enterprise observation, calibrated parameter, or empirical result appears in this file.
All instances are generated from a seeded RNG or written by hand and are SIMULATED_ONLY.

Run:  python 46_enterprise_portfolio_solver_v2_1.py
"""

from __future__ import annotations

import copy
import itertools
import math
import random
from dataclasses import dataclass

TOL = 1e-9
RESPONSES = ("Use", "Verify", "Modify", "Escalate", "Reject", "Bypass", "NA")


class InvalidInput(ValueError):
    """INVALID_SCHEMA_OR_UNITS"""


class MissingInput(ValueError):
    """A required lookup cell is UNIDENTIFIED."""


class FollowerLedgerUnidentified(MissingInput):
    """FOLLOWER_LEDGER_UNIDENTIFIED: Model C must not be solved."""


class NotComparable(ValueError):
    """NOT_COMPARABLE: Model A resource base exceeds pooled totals."""


def strict(d, key, what):
    if key not in d or d[key] is None:
        raise MissingInput(f"{what} UNIDENTIFIED: {key!r}")
    return d[key]


# ---------------------------------------------------------------------------
# Ordinal guard: ordinal keys only support comparison and hashing (42 §1.1).
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Ord:
    construct: str
    code: float  # any strictly increasing code; only order matters

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


DEFAULT_CODES = {k: {0: 0, 1: 1, 2: 2, 3: 3} for k in ("A", "H", "WI", "EA", "G", "K")}


def O(construct, level, codes=None):
    codes = codes or DEFAULT_CODES
    table = codes[construct] if construct in codes else codes
    return Ord(construct, table[level])


# ---------------------------------------------------------------------------
# Expectation operator (X1)
# ---------------------------------------------------------------------------
def _normalized(dist, what):
    if any(p is None for p in dist.values()):
        raise MissingInput(f"{what} contains UNIDENTIFIED probability")
    if any(p < -TOL for p in dist.values()) or not math.isclose(sum(dist.values()), 1.0, abs_tol=1e-9):
        raise InvalidInput(f"{what} must be nonnegative and normalized")


def expect(cfg, fn):
    """E_jk[f] = sum_l pi sum_{z,w} P sum_r rho f  (omega never conditions rho)."""
    _normalized(cfg["pi"], "pi")
    _normalized(cfg["P"], "P")
    total = 0.0
    for role, p_role in cfg["pi"].items():
        for (z, w), p_zw in cfg["P"].items():
            rho = cfg["rho"].get((z, role))
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


# ---------------------------------------------------------------------------
# Per-(j,k) precomputation
# ---------------------------------------------------------------------------
def source_key(rel, y_shared, loc):
    """Reuse tables are indexed by capability SOURCE (42 §10): ('c','S') shared, ('c','L') local."""
    return frozenset((c, "L" if c in loc else "S") for c in rel if c in loc or c in y_shared)


def jk_eval(inst, j, k, y_shared, loc, gamma_name):
    """Return dict(feasible, phiE, phiU, bud, eng, rev) for initiative j, configuration k.

    phi is incremental relative to the status quo k=0 evaluated at the current capability
    state; in these fixtures rho does not depend on capability state, so g_j0 is constant.
    """
    ini = inst["initiatives"][j]
    pol = inst["policies"][gamma_name]
    cfg, cfg0 = ini["configs"][k], ini["configs"][0]
    lam, lam_u = inst["lam"], inst["lam_u"]
    avail = set(y_shared) | set(loc)
    key = source_key(ini["rel"], y_shared, loc)

    def g_E(c):
        return expect(c, lambda x, role: x["v_u"] + x["v_x"] - x["l_u"] - x["l_x"] - x["c_u"] - x["c_x"] - lam[role] * x["t"])

    def g_U(c):
        return expect(c, lambda x, role: x["v_u"] - x["l_u"] - x["c_u"] - lam_u[role] * x["t"])

    def opc(c):
        return expect(c, lambda x, role: x["c_u"] + x["c_x"])

    N_k, N_0 = ini["N"][k], ini["N"][0]
    impl = 0.0 if k == 0 else strict(cfg["impl"], key, "implementation cost")
    eng = 0.0 if k == 0 else strict(cfg["eng"], key, "engineering hours")
    gE_k, gE_0 = g_E(cfg), g_E(cfg0)
    phiE = 0.0 if k == 0 else N_k * gE_k - N_0 * gE_0 - impl
    # Budget use = implementation + incremental per-event operating spend (42 §5.1, audit fix #8)
    bud = 0.0 if k == 0 else impl + N_k * opc(cfg) - N_0 * opc(cfg0)
    rev = 0.0 if k == 0 else N_k * expect(cfg, lambda x, r: x["t_rev"]) - N_0 * expect(cfg0, lambda x, r: x["t_rev"])
    sev = N_k * expect(cfg, lambda x, r: x["I_sev"])

    # Follower ledger split (42 §8.1). Missing split -> phiU None -> Model C refuses.
    try:
        impl_x = 0.0 if k == 0 else strict(cfg, "impl_x", "central-funded implementation share")
        tau = 0.0 if k == 0 else sum(strict(ini["tau"], c, "chargeback rule")
                                     for c in cfg["pre"] if c in y_shared and c not in loc)
        phiU = 0.0 if k == 0 else N_k * g_U(cfg) - N_0 * g_U(cfg0) - (impl - impl_x) - tau
    except MissingInput:
        phiU = None

    kap, A = ini["kappa"], cfg["A"]
    req = lambda table: strict(table, (A, kap), "requirement table cell")
    codes = inst["codes"]
    feas = (
        cfg["legal"] == 1                                                             # F2
        and strict(pol["allow"], (j, k), "Allow") == 1                                # F3
        and (j not in pol["forbid"] or k == 0)
        and all(c in avail for c in cfg["pre"])                                       # F4 (all k)
        and cfg["H"] >= req(pol["H_req"])                                             # F5a
        and cfg["WI"] >= req(pol["WI_req"])                                           # F5b
        and strict(pol["G"], j, "G_j(gamma)") >= req(pol["G_req"])                   # F5c
        and cfg["EA"] >= req(pol["EA_req"])                                           # F5d
        and (not (req(pol["H_req"]) >= O("H", 2, codes)) or cfg["effH"] == 1)         # F6
        and (cfg["A"] < O("A", 2, codes) or cfg["FB"] == 1)                           # F7
        and cfg["cons"] == 1                                                          # F8
        and sev <= strict(pol["ebar"], j, "incident tolerance") + TOL                 # F9
    )
    return dict(feasible=feas, phiE=phiE, phiU=phiU, bud=bud, eng=eng, rev=rev)


# ---------------------------------------------------------------------------
# Unit plans
# ---------------------------------------------------------------------------
def unit_plans(inst, u, y_shared, gamma_name, allow_local=True, log=None):
    pol = inst["policies"][gamma_name]
    js = [j for j, ini in inst["initiatives"].items() if ini["unit"] == u]
    loc_caps = [c for (uu, c) in inst["loc_caps"] if uu == u and allow_local
                and strict(pol["allow_loc"], (u, c), "Allow_loc") == 1]
    plans = []
    for loc in _subsets(loc_caps):
        loc_bud = sum(inst["loc_caps"][(u, c)]["F"] for c in loc)
        loc_eng = sum(inst["loc_caps"][(u, c)]["eng"] for c in loc)
        per_j = []
        for j in js:
            opts = []
            for k in inst["initiatives"][j]["configs"]:
                if j in pol["must"] and k == 0:
                    continue                                                          # F10
                try:
                    ev = jk_eval(inst, j, k, set(y_shared), set(loc), gamma_name)
                except MissingInput:
                    if k == 0:
                        raise                                                         # UNEVALUABLE_INITIATIVE
                    if log is not None:
                        log.add((j, k))                                               # RESTRICTED_SOLVE
                    continue
                if ev["feasible"]:
                    opts.append((k, ev))
            per_j.append(opts)
        for combo in itertools.product(*per_j):                                       # empty if any j has no option
            if sum(ev["rev"] for _, ev in combo) > inst["rev_cap"][u] + TOL:           # R2
                continue
            fU = None if any(ev["phiU"] is None for _, ev in combo) else sum(ev["phiU"] for _, ev in combo) - loc_bud
            plans.append(dict(
                configs={j: k for j, (k, _) in zip(js, combo)},
                loc=frozenset(loc),
                bud=sum(ev["bud"] for _, ev in combo) + loc_bud,
                eng=sum(ev["eng"] for _, ev in combo) + loc_eng,
                fE=sum(ev["phiE"] for _, ev in combo) - loc_bud,
                fU=fU,
            ))
    return plans


def shared_terms(inst, y, gamma_name):
    """Pooled use (absolute) and objective charge (incremental vs y_cur, 42 §7.4)."""
    y_cur = inst.get("y_cur", frozenset())
    bud = sum(inst["caps"][c]["F"] for c in y)
    eng = sum(inst["caps"][c]["eng"] for c in y)
    charge = sum(inst["caps"][c]["F"] * ((c in y) - (c in y_cur)) for c in inst["caps"])
    gov = inst["policies"][gamma_name]["gov_cost"]
    return bud, eng, charge, gov


def _subsets(items):
    items = list(items)
    for r in range(len(items) + 1):
        yield from itertools.combinations(items, r)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
def solve_central(inst, gammas=None, allow_shared=True):
    """Model B (allow_shared) or A+ (no sharing). Returns None if INFEASIBLE."""
    gammas = gammas or list(inst["policies"])
    best = None
    for y in _subsets(inst["caps"] if allow_shared else []):
        for g in gammas:
            sb, se, charge, gov = shared_terms(inst, y, g)
            rb, re_ = inst["A_bar"]["BUD"] - sb - gov, inst["A_bar"]["ENG"] - se
            if rb < -TOL or re_ < -TOL:
                continue
            per_u = [unit_plans(inst, u, y, g) for u in inst["units"]]
            for combo in itertools.product(*per_u):
                if sum(p["bud"] for p in combo) > rb + TOL or sum(p["eng"] for p in combo) > re_ + TOL:
                    continue
                val = sum(p["fE"] for p in combo) - charge - gov
                if best is None or val > best["F"] + TOL:
                    best = dict(F=val, y=frozenset(y), gamma=g, plans=combo)
    return best


def unit_response(plans, e_bud, e_eng):
    aff = [p for p in plans if p["bud"] <= e_bud + TOL and p["eng"] <= e_eng + TOL]
    if not aff:
        return None
    if any(p["fU"] is None for p in aff):
        raise FollowerLedgerUnidentified("unit ledger split UNIDENTIFIED; Model C not solved")
    m = max(p["fU"] for p in aff)
    tied = [p for p in aff if p["fU"] >= m - TOL * max(1.0, abs(m))]
    return dict(opt=max(p["fE"] for p in tied), pess=min(p["fE"] for p in tied), n_tied=len(tied))


def envelopes_lemmaE(plans):
    """Lemma E: candidate envelopes ⊆ {(a_BUD(x), a_ENG(x'))}; enumerating this product set is exact."""
    buds = sorted({p["bud"] for p in plans})
    engs = sorted({p["eng"] for p in plans})
    return [(b, e) for b in buds for e in engs]


def _pareto(cands):
    """Drop envelopes dominated in (more resource, no more value)."""
    cands = sorted(cands, key=lambda c: (-c[2], c[0], c[1]))
    kept = []
    for eb, ee, v in cands:
        if any(kb <= eb + TOL and ke <= ee + TOL and kv >= v - TOL for kb, ke, kv in kept):
            continue
        kept.append((eb, ee, v))
    return kept


def solve_bilevel(inst, gammas=None, envelope_fn=envelopes_lemmaE, allow_shared=True):
    """Model C (allow_shared) or C0 (no sharing): optimistic and pessimistic leader values."""
    gammas = gammas or list(inst["policies"])
    best = {"opt": None, "pess": None}
    for y in _subsets(inst["caps"] if allow_shared else []):
        for g in gammas:
            sb, se, charge, gov = shared_terms(inst, y, g)
            rb, re_ = inst["A_bar"]["BUD"] - sb - gov, inst["A_bar"]["ENG"] - se
            if rb < -TOL or re_ < -TOL:
                continue
            raw = []
            for u in inst["units"]:
                plans = unit_plans(inst, u, y, g)
                cands = []
                for (eb, ee) in envelope_fn(plans):
                    resp = unit_response(plans, eb, ee)
                    if resp is not None:
                        cands.append((eb, ee, resp))
                raw.append(cands)
            for mode in ("opt", "pess"):
                per_u = [_pareto([(eb, ee, r[mode]) for eb, ee, r in cands]) for cands in raw]
                for combo in itertools.product(*per_u):
                    if sum(c[0] for c in combo) > rb + TOL or sum(c[1] for c in combo) > re_ + TOL:
                        continue
                    val = sum(c[2] for c in combo) - charge - gov
                    if best[mode] is None or val > best[mode]["F"] + TOL:
                        best[mode] = dict(F=val, y=frozenset(y), gamma=g, env=[(c[0], c[1]) for c in combo])
    return best


def check_comparable(inst, gamma):
    gov = inst["policies"][gamma]["gov_cost"]
    if sum(inst["B0"][u]["BUD"] for u in inst["units"]) + gov > inst["A_bar"]["BUD"] + TOL or \
       sum(inst["B0"][u]["ENG"] for u in inst["units"]) > inst["A_bar"]["ENG"] + TOL:
        raise NotComparable("sum of status-quo envelopes + governance cost exceeds pooled totals")


def solve_independent(inst, gamma):
    """Model A: units decide with fixed status-quo envelopes, no shared capability."""
    check_comparable(inst, gamma)
    _, _, charge, gov = shared_terms(inst, (), gamma)
    lo = hi = -gov - charge
    for u in inst["units"]:
        plans = unit_plans(inst, u, (), gamma)
        resp = unit_response(plans, inst["B0"][u]["BUD"], inst["B0"][u]["ENG"])
        if resp is None:
            raise InvalidInput("Model A infeasible for unit " + u)
        lo += resp["pess"]
        hi += resp["opt"]
    return dict(opt=hi, pess=lo)


def architecture_metrics(inst, gamma):
    """Conditional on a fixed policy gamma (42 §11). Returns all forms and metrics."""
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


# ---------------------------------------------------------------------------
# Governance decomposition and thresholds (42 §14)
# ---------------------------------------------------------------------------
ENABLE_KEYS = ("allow", "allow_loc", "G", "must", "forbid")       # permissions (G_j is a permission level)
REQ_KEYS = ("H_req", "WI_req", "EA_req", "G_req", "ebar")         # requirements


def hybrid_policy(inst, name, allow_from, req_from, cost_from):
    pols = inst["policies"]
    h = {}
    for key in ENABLE_KEYS:
        h[key] = copy.deepcopy(pols[allow_from][key])
    for key in REQ_KEYS:
        h[key] = copy.deepcopy(pols[req_from][key])
    h["gov_cost"] = pols[cost_from]["gov_cost"]
    new = copy.deepcopy(inst)
    new["policies"][name] = h
    return new


def governance_decomposition(inst, gamma, gamma0, solver="B", mode="opt"):
    if solver == "B":
        F = lambda i, g: solve_central(i, [g])["F"]
    else:
        F = lambda i, g: solve_bilevel(i, [g])[mode]["F"]
    base = F(inst, gamma0)
    i1 = hybrid_policy(inst, "_EE", gamma, gamma0, gamma0)
    i2 = hybrid_policy(inst, "_RE", gamma, gamma, gamma0)
    f1, f2, full = F(i1, "_EE"), F(i2, "_RE"), F(inst, gamma)
    return dict(VG=full - base, EE=f1 - base, RE=f2 - f1, CE=full - f2)


def capability_threshold(inst, c, gamma, lo=0.0, hi=None, iters=60):
    """Break-even F_c^† = sup{F : building c is optimal} for Model B (bisection; P4)."""
    hi = hi if hi is not None else inst["A_bar"]["BUD"]

    def built(Fc):
        i = copy.deepcopy(inst)
        i["caps"][c]["F"] = Fc
        return c in solve_central(i, [gamma])["y"]

    if not built(lo):
        return lo
    if built(hi):
        return hi
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if built(mid) else (lo, mid)
    return 0.5 * (lo + hi)


def robustness_class(groups, element):
    """groups: {g: [optimal-solution sets per theta]}; element maps a solution to a value."""
    per_g = {g: set.intersection(*[{element(s) for s in theta_sols} for theta_sols in sols])
             for g, sols in groups.items()}
    if set.intersection(*per_g.values()):
        return "ROBUST"
    if all(per_g.values()):
        return "CONDITIONAL"
    return "FRAGILE"


# ---------------------------------------------------------------------------
# Synthetic instance generator (SIMULATED_ONLY)
# ---------------------------------------------------------------------------
def make_instance(seed, aligned=True, codes=None, money=1.0, period=1.0, delta_shared=None):
    rng = random.Random(seed)
    codes = codes or DEFAULT_CODES
    o = lambda c, l: O(c, l, codes)
    roles, Z, W = ("junior", "senior"), ("flag", "noflag"), ("ok", "err")
    caps = {"c_model": dict(F=money * period * rng.uniform(20, 60), eng=period * rng.uniform(5, 15)),
            "c_eval": dict(F=money * period * rng.uniform(10, 40), eng=period * rng.uniform(3, 10))}
    units = ["U1", "U2"]
    loc_caps = {(u, c): dict(F=caps[c]["F"] * rng.uniform(0.6, 0.9), eng=caps[c]["eng"] * rng.uniform(0.6, 0.9))
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
        itertools.product(*[[(c, s) for s in ("S", "L")] for c in sub]) for sub in _subsets(caps))]
    initiatives = {}
    for u in units:
        for jj in range(2):
            j = f"{u}_j{jj}"
            kap = o("K", rng.choice([0, 1, 2]))
            N = period * rng.choice([50, 80, 120])
            configs = {}
            for k, (attrs, pre) in cfg_specs.items():
                err = {0: 0.10, 1: rng.uniform(0.04, 0.12), 2: rng.uniform(0.02, 0.15)}[k]
                pflag = 0.5
                P = {("flag", "err"): err * 0.7, ("noflag", "err"): err * 0.3,
                     ("flag", "ok"): pflag - err * 0.7, ("noflag", "ok"): 1 - pflag - err * 0.3}
                if k == 0:
                    rho = {(z, r): {"NA": 1.0} for z in Z for r in roles}
                    allowed = {"NA"}
                else:
                    rho = {}
                    for z in Z:
                        for r in roles:
                            a = rng.uniform(0.3, 0.7)
                            b = rng.uniform(0.0, 1 - a)
                            rho[(z, r)] = {"Use": a, "Verify": b, "Reject": 1 - a - b}
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
                                    v_u=money * rng.uniform(0, 2) * (k > 0), v_x=0.0,
                                    l_u=loss, l_x=ext, c_u=money * 0.1 * (k > 0), c_x=0.0,
                                    t=tt, t_rev=tt * 0.5, I_sev=0.02 if bad else 0.0)
                base_impl = money * period * rng.uniform(12, 25) * k
                base_eng = period * rng.uniform(2, 8) * k
                impl, engt = {}, {}
                for pat in patterns:
                    red = sum(dS[c] if s == "S" else dL[c] for c, s in pat)
                    impl[pat] = max(0.0, base_impl - red * k)                 # reuse effect by source
                    engt[pat] = base_eng
                configs[k] = dict(attrs, pre=pre, legal=1, effH=1, FB=1, cons=1,
                                  impl=impl, eng=engt, impl_x=0.0,
                                  pi={"junior": 0.6, "senior": 0.4}, P=P, rho=rho,
                                  allowed_r=allowed, path=path)
            initiatives[j] = dict(unit=u, kappa=kap, N={k: N for k in cfg_specs},
                                  rel=list(caps), configs=configs, tau={c: 0.0 for c in caps})

    def req_table(level_fn, construct):
        return {(o("A", a), o("K", kk)): o(construct, level_fn(a, kk)) for a in range(4) for kk in range(3)}

    allow_all = {(j, k): 1 for j in initiatives for k in cfg_specs}
    allow_loc_all = {(u, c): 1 for u in units for c in caps}
    base_pol = dict(
        gov_cost=money * period * 5.0, allow=allow_all, allow_loc=allow_loc_all,
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
    g0["allow"] = {(j, k): (0 if k == 2 else 1) for j in initiatives for k in cfg_specs}  # legal-minimum
    return dict(units=units, caps=caps, loc_caps=loc_caps, initiatives=initiatives,
                policies={"g0": g0, "g_base": base_pol, "g_strict": strict_pol}, y_cur=frozenset(),
                A_bar={"BUD": money * period * 260.0, "ENG": period * 70.0},
                B0={u: {"BUD": money * period * 100.0, "ENG": period * 30.0} for u in units},
                rev_cap={u: period * 1e6 for u in units},
                lam={"junior": money * 0.8, "senior": money * 1.5},
                lam_u={"junior": money * 0.8, "senior": money * 1.5},
                codes=codes)


def hand_instance(u2_impl, u2_lx, ea_levels=(1, 1), ea_req=0):
    """Hand-computable fixture (45 T-ORC-8). Values are SIMULATED_ONLY."""
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

    ini = {
        "U1_j": dict(unit="U1", kappa=O("K", 0), N={0: 10.0, 1: 10.0}, rel=["c"], tau={"c": 0.0},
                     configs={0: cfg(0, 0.0, 0.0, 0.0, 0), 1: cfg(1, 3.0, 0.0, 5.0, ea_levels[0])}),
        "U2_j": dict(unit="U2", kappa=O("K", 0), N={0: 10.0, 1: 10.0}, rel=["c"], tau={"c": 0.0},
                     configs={0: cfg(0, 0.0, 0.0, 0.0, 0), 1: cfg(1, 2.0, u2_lx, u2_impl, ea_levels[1])}),
    }

    def req(lvl_fn, c):
        return {(O("A", a), O("K", kk)): O(c, lvl_fn(a)) for a in range(4) for kk in range(3)}

    def pol(ea):
        return dict(gov_cost=0.0, allow={(j, k): 1 for j in ini for k in (0, 1)}, allow_loc={},
                    G={j: O("G", 3) for j in ini}, H_req=req(lambda a: 0, "H"), WI_req=req(lambda a: 0, "WI"),
                    EA_req=req(lambda a: ea if a >= 1 else 0, "EA"), G_req=req(lambda a: 0, "G"),
                    ebar={j: 1.0 for j in ini}, must=set(), forbid=set())

    return dict(units=["U1", "U2"], caps={"c": dict(F=10.0, eng=0.0)}, loc_caps={},
                initiatives=ini, policies={"g": pol(0), "g_req": pol(ea_req)}, y_cur=frozenset(),
                A_bar={"BUD": 100.0, "ENG": 100.0},
                B0={"U1": {"BUD": 50.0, "ENG": 50.0}, "U2": {"BUD": 50.0, "ENG": 50.0}},
                rev_cap={"U1": 1.0, "U2": 1.0}, lam={"r": 0.0}, lam_u={"r": 0.0}, codes=DEFAULT_CODES)


# ---------------------------------------------------------------------------
# Tests (45 T-series). Each returns a PASS line or raises AssertionError.
# ---------------------------------------------------------------------------
def close(a, b, rel=1e-7):
    return math.isclose(a, b, rel_tol=rel, abs_tol=1e-7)


def le(a, b):
    return a <= b + 1e-7


def test_P1_ordering(seeds):
    for s in seeds:
        for aligned in (True, False):
            m = architecture_metrics(make_instance(s, aligned), "g_base")
            for mode in ("opt", "pess"):
                assert le(m["A"][mode], m["C0"][mode]) and le(m["C0"][mode], m["Aplus"])
                assert le(m["C0"][mode], m["C"][mode]) and le(m["C"][mode], m["B"])
            assert le(m["A"]["pess"], m["A"]["opt"]) and le(m["C"]["pess"], m["C"]["opt"])
            assert le(m["Aplus"], m["B"])
    return "PASS P1 ordering: A <= C0 <= A+ <= B and C0 <= C <= B (opt and pess); P1 precondition checked"


def test_not_comparable():
    inst = make_instance(1)
    inst["B0"]["U1"]["BUD"] = inst["A_bar"]["BUD"]
    try:
        architecture_metrics(inst, "g_base")
        raise AssertionError("expected NOT_COMPARABLE")
    except NotComparable:
        pass
    return "PASS NOT_COMPARABLE raised when sum(B0)+gov exceeds pooled budget"


def test_P2_alignment(seeds):
    pos = 0
    for s in seeds:
        m = architecture_metrics(make_instance(s, aligned=True), "g_base")
        assert close(m["DL"]["opt"], 0.0) and close(m["DL"]["pess"], 0.0), (s, m["DL"])
        assert close(m["DL0"]["opt"], 0.0) and close(m["DL0"]["pess"], 0.0)
        pos += architecture_metrics(make_instance(s, aligned=False), "g_base")["DL"]["pess"] > 1e-6
    return f"PASS P2 aligned => DL = DL0 = 0 on {len(seeds)} seeds; misaligned DL>0 on {pos}/{len(seeds)}"


def test_decomposition_identity(seeds):
    for s in seeds:
        m = architecture_metrics(make_instance(s, aligned=False), "g_base")
        for mode in ("opt", "pess"):
            assert close(m["NEV"][mode], m["VCP"][mode] + m["VSC"] - m["DL"][mode])
            assert close(m["VCP"][mode], m["VRA"][mode] + m["DL0"][mode])
    return "PASS NEV = VCP + VSC - DL and VCP = VRA + DL0"


def _integerize(inst):
    for c in inst["caps"].values():
        c["F"], c["eng"] = float(round(c["F"])), float(round(c["eng"]))
    for lc in inst["loc_caps"].values():
        lc["F"], lc["eng"] = float(round(lc["F"])), float(round(lc["eng"]))
    for ini in inst["initiatives"].values():
        for cfg in ini["configs"].values():
            cfg["impl"] = {kk: float(round(v)) for kk, v in cfg["impl"].items()}
            cfg["eng"] = {kk: float(round(v)) for kk, v in cfg["eng"].items()}
            for cell in cfg["path"].values():
                cell["c_u"] = 0.0                       # keeps budget use integer
    return inst


def test_lemmaE_vs_grid(seed):
    inst = _integerize(make_instance(seed, aligned=False))

    def grid(plans):
        mb = int(max(p["bud"] for p in plans)) + 1
        me = int(max(p["eng"] for p in plans)) + 1
        return [(b, e) for b in range(0, mb + 1) for e in range(0, me + 1)]

    a = solve_bilevel(inst, ["g_base"])
    b = solve_bilevel(inst, ["g_base"], envelope_fn=grid)
    assert close(a["opt"]["F"], b["opt"]["F"]) and close(a["pess"]["F"], b["pess"]["F"])
    return "PASS Lemma E finite envelopes == integer-grid envelopes (opt and pess)"


def solve_central_forced(inst, c, on, gamma="g_base"):
    i = copy.deepcopy(inst)
    best = None
    for y in _subsets(i["caps"]):
        if (c in y) != on:
            continue
        sb, se, charge, gov = shared_terms(i, y, gamma)
        rb, re_ = i["A_bar"]["BUD"] - sb - gov, i["A_bar"]["ENG"] - se
        if rb < -TOL or re_ < -TOL:
            continue
        per_u = [unit_plans(i, u, y, gamma) for u in i["units"]]
        for combo in itertools.product(*per_u):
            if sum(p["bud"] for p in combo) > rb + TOL or sum(p["eng"] for p in combo) > re_ + TOL:
                continue
            v = sum(p["fE"] for p in combo) - charge - gov
            best = v if best is None or v > best else best
    return best


def test_P4_threshold(seed):
    inst = make_instance(seed)
    inst["A_bar"]["BUD"] = 1e6                     # slack budget: threshold = G1 - G0
    th = capability_threshold(inst, "c_model", "g_base", hi=5000.0)
    prev, switches = None, 0
    for Fc in [th * f for f in (0.0, 0.5, 0.9, 0.99, 1.01, 1.1, 2.0)] + [4999.0]:
        i = copy.deepcopy(inst)
        i["caps"]["c_model"]["F"] = Fc
        built = "c_model" in solve_central(i, ["g_base"])["y"]
        switches += prev is not None and built != prev
        prev = built
    assert switches <= 1
    i1 = copy.deepcopy(inst)
    i1["caps"]["c_model"]["F"] = 0.0
    G1, G0 = solve_central_forced(i1, "c_model", True), solve_central_forced(inst, "c_model", False)
    if th > 0:
        assert abs(th - (G1 - G0)) < 1e-6 * max(1.0, abs(th)), (th, G1 - G0)
    return f"PASS P4 F_c: single switch; F_c^dagger={th:.4f} == G1-G0={G1 - G0:.4f} (SIMULATED_ONLY)"


def test_P4_delta(seeds):
    tested = 0
    for s in seeds:
        seq = []
        for d in [0.0, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 10.0, 14.0, 20.0]:
            inst = make_instance(s, delta_shared={"c_model": d})
            inst["caps"]["c_model"]["F"] = 90.0       # so that the build decision is not trivial
            seq.append("c_model" in solve_central(inst, ["g_base"])["y"])
        switches = sum(a != b for a, b in zip(seq, seq[1:]))
        assert switches <= 1 and (not switches or seq[0] is False), (s, seq)
        tested += switches
    assert tested >= 1
    return f"PASS P4 delta (source-indexed reuse, local builds allowed): monotone 0->1 at most once; {tested} seeds switched"


def test_P5_relabel(seed):
    a = solve_central(make_instance(seed, aligned=False), ["g_base", "g_strict"])
    codes = {k: {0: -7.0, 1: 0.5, 2: 0.51, 3: 1000.0} for k in ("A", "H", "WI", "EA", "G", "K")}
    b = solve_central(make_instance(seed, aligned=False, codes=codes), ["g_base", "g_strict"])
    assert close(a["F"], b["F"]) and a["y"] == b["y"] and a["gamma"] == b["gamma"]
    assert [p["configs"] for p in a["plans"]] == [p["configs"] for p in b["plans"]]
    return "PASS P5 strictly increasing ordinal relabeling leaves solution unchanged"


def test_P6_scaling(seed):
    a = solve_central(make_instance(seed), ["g_base"])
    b = solve_central(make_instance(seed, money=1000.0), ["g_base"])
    c = solve_central(make_instance(seed, period=2.0), ["g_base"])
    assert close(b["F"], 1000.0 * a["F"]) and a["y"] == b["y"]
    assert close(c["F"], 2.0 * a["F"]) and a["y"] == c["y"]
    assert [p["configs"] for p in a["plans"]] == [p["configs"] for p in b["plans"]] == [p["configs"] for p in c["plans"]]
    return "PASS P6 money x1000 and all per-period parameters x2 invariance"


def evaluate_fixed(inst, y, gamma, plans):
    """Independent re-evaluation of a fixed portfolio from raw lookups (ledger audit)."""
    _, _, charge, gov = shared_terms(inst, y, gamma)
    total = -charge - gov
    for p in plans:
        for j, k in p["configs"].items():
            total += jk_eval(inst, j, k, set(y), set(p["loc"]), gamma)["phiE"]
        total -= sum(inst["loc_caps"][(inst["initiatives"][j]["unit"], c)]["F"]
                     for j in list(p["configs"])[:1] for c in p["loc"])
    return total


def test_shared_cost_once(seeds):
    for s in seeds:
        inst = make_instance(s)
        inst["caps"]["c_model"]["F"] = 1.0           # cheap: shared c_model will be used widely
        sol = solve_central(inst, ["g_base"])
        users = sum(1 for p in sol["plans"] for j, k in p["configs"].items()
                    if "c_model" in inst["initiatives"][j]["configs"][k]["pre"] and "c_model" not in p["loc"])
        if "c_model" not in sol["y"] or users < 2:
            continue
        v0 = evaluate_fixed(inst, sol["y"], sol["gamma"], sol["plans"])
        assert close(v0, sol["F"])
        inst["caps"]["c_model"]["F"] += 1.0
        v1 = evaluate_fixed(inst, sol["y"], sol["gamma"], sol["plans"])
        assert close(v0 - v1, 1.0), (v0 - v1, users)
        return f"PASS shared fixed cost: independent re-evaluation equals solver value; +1 TWD on F_c lowers F_E by exactly 1 with {users} initiatives using it"
    raise AssertionError("no seed produced a shared capability used by >=2 initiatives")


def test_ties():
    inst = make_instance(7, aligned=False)
    j = "U1_j0"
    for cfg_k in (1, 2):
        cfg = inst["initiatives"][j]["configs"][cfg_k]
        for cell in cfg["path"].values():
            cell["v_u"], cell["l_u"], cell["c_u"], cell["t"] = 0.0, 0.0, 0.0, 0.0
            cell["l_x"] = 3.0 if cfg_k == 2 else 0.0
        for kk in cfg["impl"]:
            cfg["impl"][kk], cfg["eng"][kk] = 0.0, 0.0
    for cell in inst["initiatives"][j]["configs"][0]["path"].values():
        cell["v_u"], cell["l_u"], cell["c_u"], cell["t"] = 0.0, 0.0, 0.0, 0.0
    res = solve_bilevel(inst, ["g_base"])
    assert res["opt"]["F"] > res["pess"]["F"] + 1e-6
    return f"PASS ties: optimistic {res['opt']['F']:.3f} > pessimistic {res['pess']['F']:.3f} (SIMULATED_ONLY)"


def test_missing_and_invalid():
    j = "U1_j0"
    inst = make_instance(3)
    key = next(iter(inst["initiatives"][j]["configs"][2]["path"]))
    inst["initiatives"][j]["configs"][2]["path"][key]["l_u"] = None
    log = set()
    plans = unit_plans(inst, "U1", ("c_model", "c_eval"), "g_base", log=log)
    assert all(p["configs"][j] != 2 for p in plans) and (j, 2) in log          # RESTRICTED_SOLVE
    inst2 = make_instance(3)
    key0 = next(iter(inst2["initiatives"][j]["configs"][0]["path"]))
    inst2["initiatives"][j]["configs"][0]["path"][key0]["v_u"] = None
    try:
        unit_plans(inst2, "U1", (), "g_base")
        raise AssertionError("status-quo missing must not be solved")
    except MissingInput:
        pass                                                                    # UNEVALUABLE_INITIATIVE
    inst3 = make_instance(3)
    inst3["initiatives"][j]["configs"][1]["rho"][("flag", "junior")]["Use"] += 0.2
    try:
        unit_plans(inst3, "U1", ("c_model",), "g_base")
        raise AssertionError("non-normalized rho must be rejected")
    except InvalidInput:
        pass
    inst4 = make_instance(3)
    inst4["initiatives"][j]["configs"][1]["allowed_r"] = {"Use", "Verify"}
    try:
        unit_plans(inst4, "U1", ("c_model",), "g_base")
        raise AssertionError("forbidden response with positive mass must be rejected")
    except InvalidInput:
        pass
    inst5 = make_instance(3)
    del inst5["policies"]["g_base"]["allow"][(j, 1)]
    log5 = set()
    unit_plans(inst5, "U1", ("c_model",), "g_base", log=log5)
    assert (j, 1) in log5                                                       # missing Allow is not filled with 1
    inst6 = make_instance(3)
    inst6["initiatives"][j]["configs"][1]["impl_x"] = None
    assert solve_central(inst6, ["g_base"]) is not None                         # B still solvable
    try:
        solve_bilevel(inst6, ["g_base"])
        raise AssertionError("Model C must refuse when the follower ledger split is missing")
    except FollowerLedgerUnidentified:
        pass
    for bad in (lambda: O("H", 2) + O("H", 1), lambda: O("H", 2) >= O("EA", 1)):
        try:
            bad()
            raise AssertionError("ordinal misuse must raise")
        except TypeError:
            pass
    return ("PASS missing config -> RESTRICTED; missing status quo -> rejected; missing Allow not defaulted; "
            "missing ledger split -> B solved, C refused; bad rho, forbidden response, ordinal arithmetic, "
            "cross-construct comparison rejected")


def test_P7_B_and_screening_in_C(seed):
    inst = make_instance(seed, aligned=False)
    relaxed = hybrid_policy(inst, "_relaxed", "g_strict", "g_base", "g_strict")
    assert le(solve_central(inst, ["g_strict"])["F"], solve_central(relaxed, ["_relaxed"])["F"])
    d = governance_decomposition(inst, "g_strict", "g0", solver="B")
    assert close(d["VG"], d["EE"] + d["RE"] + d["CE"]) and le(d["RE"], 0.0)
    # Screening channel in C (audit finding #1): a requirement can RAISE the leader's value.
    h = hand_instance(0.0, 2.5, ea_levels=(2, 1), ea_req=2)
    c_free = solve_bilevel(h, ["g"])["pess"]["F"]
    c_req = solve_bilevel(h, ["g_req"])["pess"]["F"]
    b_free, b_req = solve_central(h, ["g"])["F"], solve_central(h, ["g_req"])["F"]
    assert close(c_free, 10.0) and close(c_req, 15.0) and close(b_free, 15.0) and close(b_req, 15.0)
    return (f"PASS P7 in B (RE={d['RE']:.3f} <= 0; VG=EE+RE+CE); requirement screening in C raises "
            f"F_C from {c_free:.0f} to {c_req:.0f} while B is unchanged at {b_req:.0f} (SIMULATED_ONLY)")


def test_F9_hard_constraint(seed):
    inst = make_instance(seed)
    for ini in inst["initiatives"].values():
        for cell in ini["configs"][2]["path"].values():
            cell["I_sev"] = 0.5 if cell["I_sev"] > 0 else 0.0
    sq = {}
    for j, ini in inst["initiatives"].items():
        sq[j] = ini["N"][0] * expect(ini["configs"][0], lambda x, r: x["I_sev"])
        inst["policies"]["g_base"]["ebar"][j] = sq[j]
    sol = solve_central(inst, ["g_base"])
    excluded = sum(1 for j, ini in inst["initiatives"].items() for k, cfg in ini["configs"].items()
                   if ini["N"][k] * expect(cfg, lambda x, r: x["I_sev"]) > sq[j] + 1e-12)
    for p in sol["plans"]:
        for j, k in p["configs"].items():
            cfg = inst["initiatives"][j]["configs"][k]
            assert inst["initiatives"][j]["N"][k] * expect(cfg, lambda x, r: x["I_sev"]) <= sq[j] + 1e-9
    assert excluded > 0
    return f"PASS F9 hard incident tolerance enforced without monetization ({excluded} configs excluded)"


def test_robustness_classes():
    sol = lambda y: {"y": y}
    el = lambda s: s["y"]
    assert robustness_class({"g1": [[sol("A"), sol("B")], [sol("A")]], "g2": [[sol("A")]]}, el) == "ROBUST"
    assert robustness_class({"g1": [[sol("A")], [sol("A")]], "g2": [[sol("B")], [sol("B")]]}, el) == "CONDITIONAL"
    assert robustness_class({"g1": [[sol("A")], [sol("B")]], "g2": [[sol("A")]]}, el) == "FRAGILE"
    return "PASS ROBUST / CONDITIONAL / FRAGILE classification logic"


def test_hand_oracle():
    """Hand table (opcost = 0 because c = 0 on every path):
    Aligned (U2 impl 5): phi_E(U1,k1)=10*3-5=25, phi_E(U2,k1)=10*2-5=15. B: y={c} -> 30. A, C0, A+: 0. C=30.
    Misaligned, blockable (U2 impl 5, l_x=2.5): phi_E(U2,k1)=-10, phi_U(U2,k1)=15.
      B: U1 k1 only -> 15.  C: leader gives U2 envelope 0 -> 15.  DL=0.
    Misaligned, unblockable (U2 impl 0, l_x=2.5): phi_E(U2,k1)=-5, phi_U(U2,k1)=20.
      B=15.  C: U2 picks k1 whenever c exists -> 25-5-10=10 > 0 -> C=10.  DL=5, VSC=15, NEV=10.
    """
    m1 = architecture_metrics(hand_instance(5.0, 0.0), "g")
    assert close(m1["B"], 30.0) and close(m1["C"]["opt"], 30.0) and close(m1["C"]["pess"], 30.0)
    assert close(m1["A"]["opt"], 0.0) and close(m1["Aplus"], 0.0) and close(m1["C0"]["pess"], 0.0)
    m2 = architecture_metrics(hand_instance(5.0, 2.5), "g")
    assert close(m2["B"], 15.0) and close(m2["C"]["opt"], 15.0) and close(m2["C"]["pess"], 15.0)
    m3 = architecture_metrics(hand_instance(0.0, 2.5), "g")
    assert close(m3["B"], 15.0) and close(m3["C"]["opt"], 10.0) and close(m3["C"]["pess"], 10.0)
    assert close(m3["VCP"]["opt"], 0.0) and close(m3["VSC"], 15.0) and close(m3["DL"]["opt"], 5.0)
    assert close(m3["NEV"]["opt"], 10.0) and close(m3["NEV"]["pess"], 10.0)
    return ("PASS hand oracle: aligned B=C=30; misaligned-blockable DL=0 (envelope blocks); "
            "misaligned-unblockable B=15, C=10, DL=5, VSC=15, NEV=10")


if __name__ == "__main__":
    seeds = list(range(1, 7))
    for line in (
        test_P1_ordering(seeds),
        test_not_comparable(),
        test_P2_alignment(seeds),
        test_decomposition_identity(seeds),
        test_lemmaE_vs_grid(11),
        test_P4_threshold(5),
        test_P4_delta(list(range(1, 9))),
        test_P5_relabel(4),
        test_P6_scaling(2),
        test_shared_cost_once(list(range(1, 30))),
        test_ties(),
        test_missing_and_invalid(),
        test_P7_B_and_screening_in_C(9),
        test_F9_hard_constraint(6),
        test_robustness_classes(),
        test_hand_oracle(),
    ):
        print(line)
    print("SYNTHETIC_ORACLE_PASS: all assertions hold on SIMULATED_ONLY instances; no empirical claim.")
