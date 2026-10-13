"""Hierarchy diagnostic on the frozen v1.0 toy (SIMULATED inputs only).
Compares the tri-level selected solution with
  (J) a single-level 'joint planner' that chooses b, (A,H,WI,EA) and q for all processes to maximise F1 directly;
  (T) a two-level variant where Level 2 also chooses q to maximise F2 (Level 3 removed).
Usage: python3 hierarchy_diagnostic.py <repo_dir>
"""
import sys, importlib.util, io, contextlib, itertools, json
repo = sys.argv[1]
spec = importlib.util.spec_from_file_location("s", f"{repo}/04_solver_v1_0.py"); S = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(S)

def cfg_rows(i, A, H, WI, EA, gov):
    p = S.PROCESSES[i]; out = []
    for qn, qd in S.Q_DEFS.items():
        if not S.ALLOW_CONFIG[gov["name"]][qn]: continue
        if A < qd["A"] or H < qd["H"] or WI < qd["WI"] or EA < qd["EA"]: continue
        psi = S.psi_value(WI, EA, p)
        gain = qd["gain"][i]*p["value"]*psi*gov["flex_mult"]
        risk = p["risk"]*qd["autonomy"]*gov["risk_mult"]/(1+.45*H+.45*EA)
        bur = qd["burden"]+.03*H+.02*EA+.02*WI
        out.append((qn, gain, risk, gain-.45*bur-.75*risk))
    return out

def pareto(points):            # points: (capuse, value, label); keep max value for each capuse frontier
    pts = sorted(points, key=lambda x: (x[0], -x[1])); fr = []; best = -1e18
    for c, v, lab in pts:
        if v > best + 1e-12: fr.append((c, v, lab)); best = v
    return fr

cacheJ, cacheT = {}, {}
def frontier(i, caps, gname, mode):
    key = (i, caps, gname, mode); C = cacheJ if mode == "J" else cacheT
    if key in C: return C[key]
    gov = S.GOVERNANCE[gname]; pts = []
    for o in S.l2_options_for_proc(i, caps, gov):
        A, H, WI, EA = o["A"], o["H"], o["WI"], o["EA"]
        base_f2 = o["f2"] - .65*max(0, o["l3"]["utility"])
        for qn, gain, risk, U in cfg_rows(i, A, H, WI, EA, gov):
            if mode == "J":   val = 1.25*max(0, gain) + .20*(qn != "HumanOnly") - .75*risk
            else:             val = base_f2 + .65*max(0, U)
            pts.append((round(o["capuse"], 9), val, (A, H, WI, EA, qn)))
    C[key] = pareto(pts); return C[key]

def best_combo(caps, gname, mode):
    K = S.GOVERNANCE[gname]["K"]; fr = [frontier(i, caps[4*i:4*i+4], gname, mode) for i in range(3)]
    if any(not f for f in fr): return None
    best = None
    for a in fr[0]:
        for b in fr[1]:
            if a[0]+b[0] > K + 1e-9: continue
            for c in fr[2]:
                if a[0]+b[0]+c[0] > K + 1e-9: continue
                v = a[1]+b[1]+c[1]
                if best is None or v > best[0] + 1e-12: best = (v, (a[2], b[2], c[2]))
    return best

def f1_of(alloc, arch, gname):
    gov = S.GOVERNANCE[gname]; tot = -.22*sum(alloc)
    for i, (A, H, WI, EA, qn) in enumerate(arch):
        g, r = next((x[1], x[2]) for x in cfg_rows(i, A, H, WI, EA, gov) if x[0] == qn)
        tot += 1.25*max(0, g) + .20*(qn != "HumanOnly") - .75*r
    return tot

out = []
for B in (3, 5, 7):
    for g in "CFD":
        tri = S.solve(g, B)
        tri_arch = tuple((o["A"], o["H"], o["WI"], o["EA"], o["l3"]["q"]) for o in tri["l2"]["opts"])
        bestJ = None; capsdone = {}
        for al in S.generate_allocations(B):
            caps = S.caps_from_alloc(al)
            if caps not in capsdone: capsdone[caps] = best_combo(caps, g, "J")
            r = capsdone[caps]
            if r is None: continue
            v = r[0] - .22*sum(al)
            if bestJ is None or v > bestJ[0] + 1e-12: bestJ = (v, al, r[1])
        # two-level: L2 chooses q too (maximise F2), L1 maximises F1 given that response
        bestT = None; capsT = {}
        for al in S.generate_allocations(B):
            caps = S.caps_from_alloc(al)
            if caps not in capsT: capsT[caps] = best_combo(caps, g, "T")
            r = capsT[caps]
            if r is None: continue
            v = f1_of(al, r[1], g)
            if bestT is None or v > bestT[0] + 1e-12: bestT = (v, al, r[1])
        row = dict(B=B, G=g, F1_trilevel=round(tri["F1"], 6), F1_joint=round(bestJ[0], 6),
                   joint_minus_tri=round(bestJ[0]-tri["F1"], 6), tri_arch=tri_arch, joint_arch=bestJ[2],
                   tri_alloc=tri["alloc"], joint_alloc=bestJ[1],
                   F1_twolevel=round(bestT[0], 6), twolevel_arch=bestT[2])
        out.append(row); print(json.dumps(row, default=str))
