"""Sidecar: endpoint bracketing (doc 07 Prop G3) on the T-MIS-6 seed-5 instance, using a COPY of 51."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s51_copy as S
names = {"impl cell", "eng cell", "outcome cell (k>0)", "Allow", "Allow_loc"}
payload = lambda x: json.dumps(S._canon({kk: x.get(kk) for kk in ("F_E", "configs", "y", "envelopes")}), sort_keys=True)
for name, site in S.MISSING_SITES:
    if name not in names:
        continue
    for model in ("B", "C"):
        m = S.make_instance(5); d, k = site(m); d[k] = None
        rm = S.solve(m, model, ["g_base"])
        out = []
        vals = (0, 1) if name.startswith("Allow") else (0.0, 1.0, 10.0, 100.0, 1e6)
        for v in vals:
            z = S.make_instance(5); d2, k2 = site(z); d2[k2] = v
            rz = S.solve(z, model, ["g_base"])
            out.append((v, rz["status"], payload(rz) == payload(rm)))
        print(name, model, rm["status"], out)
