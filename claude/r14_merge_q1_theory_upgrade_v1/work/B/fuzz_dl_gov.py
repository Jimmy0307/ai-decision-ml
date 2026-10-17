"""Falsification search (not a proof) for Thm DL-1 (opt/pess iff), Cor DL-3 (unique first best),
GS identity and GS-N necessary condition. Random small instances, exact integer data."""
import random, sys, itertools
sys.path.insert(0, r"C:/NTUST_PAPER/outputs/00_CURRENT/Q1_THEORY_UPGRADE_V1_20261014/witness_parts")
import w_dl_gov as W

def rand_inst(rng):
    units = ["U%d" % i for i in range(rng.choice([1, 2]))]
    caps = {"c": {"F": rng.randint(0, 3), "a": (rng.randint(0, 2), 0)}} if rng.random() < .5 else {}
    tab = {}
    for u in units:
        ps = [{"name": u+":k0", "a": (0, 0), "FU": 0, "FE": 0, "EA": 0, "need": False}]
        for k in range(rng.randint(1, 3)):
            ps.append({"name": u+":k%d" % (k+1), "a": (rng.randint(-1, 2), rng.randint(0, 2)),
                       "FU": rng.randint(-3, 3), "FE": rng.randint(-3, 3), "EA": rng.randint(0, 2),
                       "need": bool(caps) and rng.random() < .5, "unit_ok": rng.random() < .9})
        tab[u] = ps
    req = {"loose": 0, "strict": rng.randint(1, 2)}
    def plans(u, y, g):
        return [dict(p) for p in tab[u] if (not p["need"] or "c" in y) and p["EA"] >= req[g]]
    return {"units": units, "caps": caps, "policies": {"loose": {"cost": 0}, "strict": {"cost": 0}},
            "Abar": (rng.randint(0, 4), rng.randint(0, 4)), "plans": plans}, tab, req

rng = random.Random(20261014)
n = viol = gsn_checked = uniq_checked = 0
for it in range(4000):
    inst, tab, req = rand_inst(rng)
    try:
        lo = W._wdg_analyse(inst, ["loose"]); st = W._wdg_analyse(inst, ["strict"])
        W._wdg_analyse(inst, ["loose", "strict"])
    except (TypeError, AttributeError):
        continue  # infeasible branch (no B or C solution)
    n += 1
    for r in (lo, st):
        if not (r["theorem_DL1_consistent"] and r["lemmaE_equals_product_envelopes"]):
            viol += 1; print("DL1 VIOLATION", it)
        # Cor DL-3 (unique first best): DL_opt>0 <=> exists strict unblockable deviation
        if r["n_B_optima"] == 1:
            uniq_checked += 1
            devs = r["B_optima"][0]["unblockable_deviations"]
            fb = r["B_optima"][0]
            outC = any(nm not in {p["name"] for p in W._wdg_plans(inst, nm.split(":")[0], frozenset(fb["y"]), fb["gamma"], "C")}
                       for nm in fb["plans"])
            pred_o = outC or any(d["strict_pref"] for ds in devs.values() for d in ds)
            pred_p = outC or any(True for ds in devs.values() for d in ds)
            if pred_o != (r["DL_opt"] > 1e-7) or pred_p != (r["DL_pess"] > 1e-7):
                viol += 1; print("COR DL3 VIOLATION", it)
    for m in ("opt", "pess"):
        gsv = st["C_" + m] - lo["C_" + m]
        if abs(gsv - (lo["DL_" + m] - st["DL_" + m] - (lo["B"] - st["B"]))) > 1e-7:
            viol += 1; print("IDENTITY VIOLATION", it)
        if gsv > 1e-7:
            gsn_checked += 1
            # GS-N: DL_loose >= GSV and some y,u, xG in strict, xH in loose\strict, a(xH)<=a(xG),
            # FU(xH) > (opt) / >= (pess) FU(xG), FE(xH) < FE(xG)
            ok = lo["DL_" + m] >= gsv - 1e-7
            found = False
            for y in W._wdg_subsets(inst["caps"]):
                for u in inst["units"]:
                    Ls = W._wdg_plans(inst, u, y, "loose", "C"); Ss = W._wdg_plans(inst, u, y, "strict", "C")
                    sn = {p["name"] for p in Ss}
                    for xg in Ss:
                        for xh in Ls:
                            if xh["name"] in sn: continue
                            pref = xh["FU"] > xg["FU"] if m == "opt" else xh["FU"] >= xg["FU"]
                            if W._wdg_le(xh["a"], xg["a"]) and pref and xh["FE"] < xg["FE"]:
                                found = True
            if not (ok and found):
                viol += 1; print("GS-N VIOLATION", it, m)
print("instances", n, "unique-first-best checks", uniq_checked, "GSV>0 cases checked", gsn_checked, "violations", viol)
