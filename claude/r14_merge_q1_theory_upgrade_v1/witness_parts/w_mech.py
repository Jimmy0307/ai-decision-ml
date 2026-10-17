"""T4 witness part: mechanism ablation fibres (M1-M4) and an information-asymmetry sign example.

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


if __name__ == "__main__":
    import json
    for w in (witness_mech_ablation(), witness_ia_ndv_sign()):
        print(json.dumps({"id": w["id"], "pass": w["pass"], "choices": w["choices"]}, default=str))
        print(json.dumps(w["outputs"], default=str, indent=1))
