"""w_dl_gov.py -- Q1 theory witnesses for Task B (delegation loss) and Task C (governance screening).

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


def witness_W5():
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


ALL_WDG = [witness_W1, witness_W2, witness_W3, witness_W3m, witness_W3b, witness_W3c, witness_W5,
           witness_W4, witness_W4b, witness_W4c, witness_W4d, witness_W4e]


if __name__ == "__main__":
    allok = True
    for f in ALL_WDG:
        d = f()
        allok &= d["pass"]
        keys = [k for k in d["expected"]]
        print("%-4s %-5s %s" % (d["id"], "PASS" if d["pass"] else "FAIL", d["title"]))
        print("      " + ", ".join("%s=%g" % (k, d["outputs"][k]) for k in keys))
    print("W_DL_GOV_VERDICT", "PASS" if allok else "FAIL")
