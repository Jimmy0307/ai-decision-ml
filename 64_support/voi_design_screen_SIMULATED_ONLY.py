"""64 support — VOI design screen. SIMULATED_ONLY. Not an enterprise case, not evidence about any firm.
Purpose: show, on pilot-shaped synthetic instances from 51.make_instance (2 units x 1 initiative x 3 configurations,
2 shared capabilities), which parameter BLOCK carries the largest value of identification (51 voi_generic, vertex and
grid) when every block gets the SAME relative uncertainty (x0.5 to x1.5). It informs only the ORDER of data
collection in 64; real priorities are recomputed with 65 --make-registry / --robust on the first real batch.
"""
import importlib.util, json, sys, os, time
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("s51", os.path.join(HERE, "51_enterprise_portfolio_solver_v2_2.py"))
S = importlib.util.module_from_spec(spec); sys.modules["s51"] = S; spec.loader.exec_module(S)

def blocks_for(inst):
    cells = lambda field: [(("initiatives", j, "configs", k, "path", key), field)
                           for j, ini in inst["initiatives"].items() for k, cfg in ini["configs"].items() if k
                           for key in cfg["path"]]
    impl = [(("initiatives", j, "configs", k, "impl"), p) for j, ini in inst["initiatives"].items()
            for k, cfg in ini["configs"].items() if k for p in cfg["impl"]]
    j0 = sorted(inst["initiatives"])[0]
    P = inst["initiatives"][j0]["configs"][1]["P"]
    hiP = {("flag", "err"): P[("flag", "err")] * 2, ("noflag", "err"): P[("noflag", "err")] * 2}
    hiP[("flag", "ok")] = P[("flag", "ok")] - P[("flag", "err")]; hiP[("noflag", "ok")] = P[("noflag", "ok")] - P[("noflag", "err")]
    rho = inst["initiatives"][j0]["configs"][1]["rho"][("flag", "junior")]
    alt = {"Use": min(1.0, rho["Use"] + rho["Verify"]), "Verify": 0.0, "Reject": rho["Reject"]}
    alt["Use"] = 1 - alt["Reject"]
    return [dict(name="V:value v_u", kind="scale", targets=cells("v_u"), L=0.5, U=1.5),
            dict(name="V:loss l_u", kind="scale", targets=cells("l_u"), L=0.5, U=1.5),
            dict(name="V:time t", kind="scale", targets=cells("t"), L=0.5, U=1.5),
            dict(name="X:impl cost", kind="scale", targets=impl, L=0.5, U=1.5),
            dict(name="E:shared F_c", kind="scale", targets=[(("caps", c), "F") for c in inst["caps"]], L=0.5, U=1.5),
            dict(name="R:error rate P (one AI config)", kind="prob", path=("initiatives", j0, "configs", 1, "P"), vertices=[dict(P), hiP]),
            dict(name="R:response rho (one row: Verify->Use)", kind="prob", path=("initiatives", j0, "configs", 1, "rho", ("flag", "junior")),
                 vertices=[dict(rho), alt])]

out = []
for seed in range(40, 52):
    t0 = time.time()
    inst = S.make_instance(seed, aligned=False, n_init=1)
    bl = blocks_for(inst)
    reg = {"groups": {"g1": {"blocks": bl}}, "eps_R": 0.0, "tie_tol": 1e-9, "seed": 1}
    S.validate_registry(reg, inst)
    tinst = S.theta_instances(inst, bl)
    cands = [d for d in S.enumerate_portfolios(inst, "g_base", static_only=True)
             if S.robust_feasibility(inst, "g_base", d, bl, tinst, spts=[]) == "ROBUSTLY_FEASIBLE"]
    if not cands:
        continue
    f = S.portfolio_evalf(inst, "g_base", bl)
    vv = S.voi_generic(f, cands, bl, "vertex")
    vg = S.voi_generic(f, cands, bl, "grid", 2)
    rec = dict(seed=seed, n_candidates=len(cands), mmr=vv[bl[0]["name"]]["mmr_all"],
               voi_vertex={b["name"]: vv[b["name"]]["voi"] for b in bl}, voi_grid={b["name"]: vg[b["name"]]["voi"] for b in bl},
               seconds=round(time.time() - t0, 1))
    out.append(rec); print(json.dumps(rec), flush=True)
json.dump(dict(label="SIMULATED_ONLY design screen (64 appendix); not empirical", runs=out),
          open(os.path.join(HERE, "64_support", "voi_design_screen_SIMULATED_ONLY.json"), "w"), indent=1)
