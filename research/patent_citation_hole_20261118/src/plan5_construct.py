"""Preregistration 5: construct-validity checks (DEC06-only; subgroup-family reference set).

Step 1 (slow, ~10 min, cached): read g_cpc_current once and keep only what is needed:
    - flags AI, DEC, DEC06, DEC04, BIZ
    - reference memberships at main-group level ('all') and subgroup-family level ('sub2')
  -> outputs/plan5_cpc_LOCAL.npz
Step 2 (fast): run patent_hole.run_spec for P5a-P5d using the cached citations.

Usage:
    python src/plan5_construct.py --inputs inputs_LOCAL --out outputs [--n-boot 2000]
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import patent_hole as ph  # noqa: E402

REF_CLASSES = ("G06", "G16", "H04")


def family_key(sym: str) -> str:
    """Main group + '/' + first two characters of the subgroup (G06F16/2457 -> G06F16/24)."""
    main, _, sub = sym.partition("/")
    return f"{main}/{sub[:2]}" if sub else main


def build_cache(u, cpc_path, out):
    n = len(u.pid)
    flags = {k: np.zeros(n, bool) for k in ("AI", "DEC", "DEC06", "DEC04", "BIZ")}
    idx_all, key_all = [], []
    for ch in ph.read_tsv(cpc_path, ph.REQUIRED["g_cpc_current"], chunksize=5_000_000):
        s = ch.cpc_group.str.strip('"').str.replace(" ", "", regex=False)
        idx = u.index(ph.numeric_ids(ch.patent_id))
        keep = idx >= 0
        s, idx = s[keep].reset_index(drop=True), idx[keep]
        flags["AI"][idx[s.str.startswith("G06N").to_numpy()]] = True
        flags["DEC"][idx[s.str.match(r"^G06Q10/0[46]").to_numpy()]] = True
        flags["DEC06"][idx[s.str.match(r"^G06Q10/06").to_numpy()]] = True
        flags["DEC04"][idx[s.str.match(r"^G06Q10/04").to_numpy()]] = True
        flags["BIZ"][idx[(s.str.startswith("G06Q") & ~s.str.startswith("G06Q10/")).to_numpy()]] = True
        ref = s.str.startswith(REF_CLASSES).to_numpy()
        idx_all.append(idx[ref].astype(np.int32))
        key_all.append(s[ref].to_numpy())
        ph.log(f"cpc chunk; ref rows so far {sum(map(len, idx_all)):,}")
    idx = np.concatenate(idx_all)
    sym = np.concatenate(key_all)
    main = pd.Series(sym, dtype=object).str.split("/", n=1).str[0].to_numpy()
    fam = np.array([family_key(x) for x in sym], dtype=object)
    np.savez(out, idx=idx, main=main.astype(str), fam=fam.astype(str), **{f"flag_{k}": v for k, v in flags.items()})
    ph.log("cache written", out)


def csr_from(n, idx, keys):
    codes, names = pd.factorize(pd.Series(keys, dtype=object), sort=True)
    G = len(names)
    pairs = np.unique(idx.astype(np.int64) * G + codes)
    p, g = pairs // G, (pairs % G).astype(np.int32)
    indptr = np.zeros(n + 1, np.int64)
    indptr[1:] = np.cumsum(np.bincount(p, minlength=n))
    return (indptr, g), [str(x) for x in names]


SPECS = {
    "P5a_DEC06_maingroup": dict(dec="DEC06", ref="all"),
    "P5b_DEC_subfamily": dict(dec="DEC", ref="sub2"),
    "P5c_DEC06_subfamily": dict(dec="DEC06", ref="sub2"),
    "P5d_DEC04_maingroup_descriptive": dict(dec="DEC04", ref="all"),
}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--n-boot", type=int, default=ph.N_BOOT)
    a = ap.parse_args(argv)
    t0 = time.time()
    u = ph.load_patents(ph.find_input(a.inputs, "g_patent"))
    cache = a.out / "plan5_cpc_LOCAL.npz"
    if not cache.exists():
        build_cache(u, ph.find_input(a.inputs, "g_cpc_current"), cache)
    z = np.load(cache, allow_pickle=False)
    n = len(u.pid)
    u.flags = {k[5:]: z[k] for k in z.files if k.startswith("flag_")}
    csr_all, names_all = csr_from(n, z["idx"], z["main"])
    csr_sub, names_sub = csr_from(n, z["idx"], z["fam"])
    ph.log("groups: main", len(names_all), "sub2", len(names_sub),
           "flags", {k: int(v.sum()) for k, v in u.flags.items()})
    cz = np.load(a.out / "cache_citations_LOCAL.npz")
    ci, cj, cat = cz["i"], cz["j"], cz["c"]
    keep = u.year[ci] <= 2025
    ci, cj, cat = ci[keep], cj[keep], cat[keep]
    out_file = a.out / "PLAN5_CONSTRUCT_RESULTS.json"
    R = json.loads(out_file.read_text(encoding="utf-8")) if out_file.exists() else {}
    R["preregistration"] = "PREREGISTRATION_CONSTRUCT_VALIDITY.md v1.0"
    R.setdefault("specs", {})
    for name, s in SPECS.items():
        if name in R["specs"]:
            continue
        uu = ph.Universe(pid=u.pid, year=u.year, flags=u.flags,
                         ref_csr={"x": csr_all if s["ref"] == "all" else csr_sub},
                         group_names=names_all if s["ref"] == "all" else names_sub)
        spec = dict(applicant_only=True, ai="AI", dec=s["dec"], biz="BIZ", ref="x", y0=2010, bridge="exclude")
        ph.log("spec", name)
        r, _, _ = ph.run_spec(uu, ci, cj, cat, spec, n_boot=a.n_boot)
        r.pop("H2", None)
        r["reference_set"] = s["ref"]
        R["specs"][name] = r
        out_file.write_text(json.dumps(R, indent=2, default=float), encoding="utf-8")
        ph.log(name, r["verdict"], "OE", round(r["AI_DEC"]["OE"], 3), "pct", r["reference"]["percentile_rank_in_AI_ref"],
               r["reference"]["percentile_rank_in_DEC_ref"], "ratio", round(r["ratio_point"], 3), "nref", r["reference"]["n_fields"])
    v = [R["specs"][k]["verdict"] for k in ("P5a_DEC06_maingroup", "P5b_DEC_subfamily", "P5c_DEC06_subfamily")]
    R["construct_verdict"] = "ROBUST_TO_CONSTRUCT" if all(x == "HOLE_NOT_SUPPORTED" for x in v) else "CONSTRUCT_SENSITIVE"
    R["seconds"] = round(time.time() - t0)
    out_file.write_text(json.dumps(R, indent=2, default=float), encoding="utf-8")
    ph.log("done", R["construct_verdict"])


if __name__ == "__main__":
    sys.exit(main())
