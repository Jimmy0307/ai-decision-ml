"""Sidecar (read-only use of a COPY of 51): per-site breakdown of T-MIS-6 bins. Not part of the canonical solver."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s51_copy as S
rows = []
for name, site in S.MISSING_SITES:
    for model in ("B", "C"):
        m, z = S.make_instance(5), S.make_instance(5)
        d, k = site(m); d[k] = None
        d2, k2 = site(z); d2[k2] = 0
        rm, rz = S.solve(m, model, ["g_base"]), S.solve(z, model, ["g_base"])
        point = rm.get("F_E") is not None or rm.get("configs") is not None or rm.get("y") is not None
        payload = lambda x: json.dumps(S._canon({kk: x.get(kk) for kk in ("F_E", "configs", "y", "envelopes")}), sort_keys=True)
        disc = sorted(kk for kk in S.DISCLOSURE_KEYS if rm["details"].get(kk))
        b = "no_point" if not point else ("payload_differs" if payload(rm) != payload(rz) else "disclosed")
        rows.append((name, model, b, rm["status"], ",".join(rm["flags"]), rz["status"], ";".join(disc)))
for r in rows:
    print(" | ".join(r))
from collections import Counter
print(Counter(r[2] for r in rows))
