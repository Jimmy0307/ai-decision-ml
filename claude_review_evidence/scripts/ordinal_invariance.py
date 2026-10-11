"""Ordinal-invariance diagnostic on the frozen v1.0 toy (SIMULATED).
Re-codes ordinal levels with order-preserving maps *only inside the continuous objective formulas*
(feasibility thresholds left untouched) and counts how many of the nine selected optima change.
If optima change, the objective is using the 0-3 / kappa codes as interval-scale numbers.
"""
import sys, importlib.util, io, contextlib, json
repo = sys.argv[1]
src = open(f"{repo}/04_solver_v1_0.py", encoding="utf-8").read()
base = json.load(open(f"{repo}/05_solver_results_v1_0.json"))
basemap = {(r["budget"], r["governance"]): (r["F1_best"], r["L1_allocation_vector"],
           [(p["A"], p["H"], p["WI"], p["EA"], p["configuration"]) for p in r["processes"]]) for r in base["results"]}

def variant(name, zk=None, zl=None):
    s = src
    hdr = f"ZK={zk!r}\nZL={zl!r}\n"
    if zk:
        s = s.replace('p["risk"] * qd["autonomy"]', 'ZK[p["risk"]] * qd["autonomy"]')
        s = s.replace('- 0.030*A*p["risk"]', '- 0.030*A*ZK[p["risk"]]')
        s = s.replace('0.08*p["risk"]*A/', '0.08*ZK[p["risk"]]*A/')
    if zl:  # H, EA, WI recoded inside risk / burden / psi / reliability / capuse formulas only
        s = s.replace("/ (1.0 + 0.45*H + 0.45*EA)", "/ (1.0 + 0.45*ZL[H] + 0.45*ZL[EA])")
        s = s.replace("burden = qd[\"burden\"] + 0.03*H + 0.02*EA + 0.02*WI", "burden = qd[\"burden\"] + 0.03*ZL[H] + 0.02*ZL[EA] + 0.02*ZL[WI]")
        s = s.replace("0.45 + 0.10*EA + 0.06*H + 0.04*WI", "0.45 + 0.10*ZL[EA] + 0.06*ZL[H] + 0.04*ZL[WI]")
        s = s.replace("/(1.0+0.4*H+0.4*EA)", "/(1.0+0.4*ZL[H]+0.4*ZL[EA])")
    s = s.replace("from functools import lru_cache", "from functools import lru_cache\n" + hdr, 1) if "from functools import lru_cache" in s else hdr + s
    path = f"/tmp/variant_{name}.py"; open(path, "w", encoding="utf-8").write(s)
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp)
    with contextlib.redirect_stdout(io.StringIO()): sp.loader.exec_module(m)
    changed = []
    for B in (3, 5, 7):
        for g in "CFD":
            r = m.public_result(m.solve(g, B))
            now = (r["L1_allocation_vector"], [(p["A"], p["H"], p["WI"], p["EA"], p["configuration"]) for p in r["processes"]])
            if now != basemap[(B, g)][1:]: changed.append((B, g, now))
    return changed

for name, zk, zl in [("kappa_convex", {1: 1, 2: 2, 3: 4}, None),
                     ("kappa_concave", {1: 1, 2: 2.5, 3: 3}, None),
                     ("levels_concave", None, {0: 0, 1: 1, 2: 1.5, 3: 1.8}),
                     ("levels_convex", None, {0: 0, 1: 1, 2: 2.5, 3: 4.5})]:
    ch = variant(name, zk, zl)
    print(f"{name}: {len(ch)}/9 selected optima change")
    for c in ch: print("   ", c)
