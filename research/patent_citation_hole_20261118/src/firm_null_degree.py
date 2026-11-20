"""Plan 6 (PREREGISTRATION_FIRM_NULL_DEGREE.md): firm null preserving portfolio and degree (design A2).

Two steps:
    # on the machine that holds outputs/firm_model_LOCAL.pkl (needs firm_null.py and its imports)
    python src/firm_null_degree.py export --out outputs
    # anywhere with numpy + scipy (standalone; e.g. the Jetson)
    python firm_null_degree.py run --model firm_model_A2_LOCAL.npz --out out --reps 1000 --workers 6

The export writes only arrays (patent type, year, owner indices, citation index pairs, base strata, the
expected Plan 3/4 observed values). No names, no raw PatentsView rows.
"""
import argparse
import json
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import scipy.sparse as sp

SEED, PLAN = 20261119, 6
GROUPS = ("AI_FIRM", "DEC_FIRM", "MIXED")
SCHEMES = ("primary", "S_tech")


# ------------------------------------------------------------------ export (needs the original model)
def export(out: Path):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import pickle
    import __main__
    import firm_null
    __main__.FirmModel = firm_null.FirmModel
    M = pickle.load(open(out / "firm_model_LOCAL.pkl", "rb"))
    n = len(M.S)
    base = {}
    for s in SCHEMES:
        sid = -np.arange(1, n + 1, dtype=np.int64)        # singleton strata get unique negative ids
        for k, g in enumerate(M.strata[s]):
            sid[g] = k
        base[s] = sid
    p5 = json.loads((out / "FULL_SUITE_RESULTS.json").read_text(encoding="utf-8"))["P5"]
    np.savez_compressed(out / "firm_model_A2_LOCAL.npz", ptype=M.ptype, year=M.year, indptr=M.indptr, owner=M.owner,
                        group=np.array([GROUPS.index(x) for x in M.group], np.int8), ca=M.ca, cb=M.cb,
                        base_primary=base["primary"], base_S_tech=base["S_tech"],
                        exp_T1=p5["group_OE"]["AI_FIRM~DEC_FIRM"]["OE"], exp_T2=p5["broker_test"]["mixed_median_constraint"],
                        exp_ties=p5["ties"])
    print("exported", n, "patents", len(M.firms), "firms", len(M.ca), "citations")


# ------------------------------------------------------------------ model (same arithmetic as firm_null.FirmModel)
class Model:
    def __init__(self, z):
        self.__dict__.update({k: z[k] for k in z.files})
        self.nf = int(self.owner.max()) + 1
        self.g = np.array(GROUPS)[self.group]
        n = len(self.ptype)
        outd = np.bincount(self.ca, minlength=n)
        ind = np.bincount(self.cb, minlength=n)
        cls = lambda d: np.minimum(d, 10)
        self.strata = {}
        for s in SCHEMES:
            key = np.stack([self.__dict__[f"base_{s}"], cls(outd), cls(ind)], 1)
            _, lab = np.unique(key, axis=0, return_inverse=True)
            lab = lab.ravel()
            order = np.argsort(lab, kind="stable")
            cuts = np.flatnonzero(np.diff(lab[order])) + 1
            self.strata[s] = [g for g in np.split(order, cuts) if len(g) > 1]
            self.__dict__[f"singleton_share_{s}"] = 1 - sum(len(g) for g in self.strata[s]) / n

    def weights(self, perm=None):
        pa = self.ca if perm is None else perm[self.ca]
        pb = self.cb if perm is None else perm[self.cb]
        na = self.indptr[pa + 1] - self.indptr[pa]
        nb = self.indptr[pb + 1] - self.indptr[pb]
        tot = na * nb
        keep = tot > 0
        pa, pb, na, nb, tot = pa[keep], pb[keep], na[keep], nb[keep], tot[keep]
        rep = np.repeat(np.arange(len(tot)), tot)
        t = np.arange(tot.sum()) - np.repeat(np.cumsum(tot) - tot, tot)
        i = t // nb[rep]
        j = t % nb[rep]
        fa = self.owner[self.indptr[pa[rep]] + i]
        fb = self.owner[self.indptr[pb[rep]] + j]
        ok = fa != fb
        lo, hi = np.minimum(fa[ok], fb[ok]), np.maximum(fa[ok], fb[ok])
        W = sp.coo_matrix((np.ones(len(lo)), (lo, hi)), shape=(self.nf, self.nf)).tocsr()
        W.sum_duplicates()
        return (W + W.T).tocsr()

    @staticmethod
    def constraint(W, block=2000):
        s = np.asarray(W.sum(1)).ravel()
        inv = np.where(s > 0, 1 / np.where(s > 0, s, 1), 0)
        P = (sp.diags(inv) @ W).tocsr()
        c = np.zeros(W.shape[0])
        for b in range(0, W.shape[0], block):
            Pb = P[b:b + block]
            PPb = (Pb @ P).tocsr()
            mask = Pb.copy()
            mask.data[:] = 1
            c[b:b + block] = np.asarray((Pb + PPb.multiply(mask)).power(2).sum(1)).ravel()
        return c, s

    def stats(self, W):
        con, s = self.constraint(W)
        g = self.g
        tot = W.sum() / 2
        Sg = {k: s[g == k].sum() for k in GROUPS}
        Wc = W.tocoo()
        oe = {}
        for a, b in (("AI_FIRM", "DEC_FIRM"), ("AI_FIRM", "MIXED"), ("DEC_FIRM", "MIXED")):
            O = float(Wc.data[(g[Wc.row] == a) & (g[Wc.col] == b)].sum())
            E = Sg[a] * Sg[b] / (2 * tot)
            oe[f"{a}~{b}"] = O / E if E else float("nan")
        act = s > 0
        deg = np.diff(W.indptr)
        return {"T1": oe["AI_FIRM~DEC_FIRM"], "T2": float(np.median(con[act & (g == "MIXED")])),
                "OE_AI_MIXED": oe["AI_FIRM~MIXED"], "OE_DEC_MIXED": oe["DEC_FIRM~MIXED"],
                "ties": int(W.nnz // 2), "weight": float(tot)}, deg, s


_M = None


def _init(path):
    global _M
    _M = Model(np.load(path))


def _rep(args):
    scheme, r = args
    rng = np.random.default_rng([SEED, PLAN, SCHEMES.index(scheme), r])
    perm = np.arange(len(_M.ptype))
    for g in _M.strata[scheme]:
        perm[g] = rng.permutation(g)
    st, deg, s = _M.stats(_M.weights(perm))
    return r, st, deg.astype(np.int32), s.astype(np.float32)


def spearman(x, y):
    from scipy.stats import spearmanr
    return float(spearmanr(x, y).correlation)


def run(model: Path, out: Path, reps: int, workers: int):
    out.mkdir(parents=True, exist_ok=True)
    M = Model(np.load(model))
    obs, deg0, s0 = M.stats(M.weights())
    assert abs(obs["T1"] - float(M.exp_T1)) < 1e-9 and abs(obs["T2"] - float(M.exp_T2)) < 1e-9 \
        and obs["ties"] == int(M.exp_ties), "does not reproduce Plan 3 P5 / Plan 4 observed values"
    act = s0 > 0
    R = {"preregistration": "PREREGISTRATION_FIRM_NULL_DEGREE.md", "observed": obs, "reps": reps,
         "seeding": "default_rng([20261119, 6, scheme_index, r])", "active_firms": int(act.sum())}
    for scheme in SCHEMES:
        part = out / f"PLAN6_{scheme}_PARTIAL.json"
        degp = out / f"PLAN6_{scheme}_DEG_PARTIAL_LOCAL.npy"
        rows = json.loads(part.read_text()) if part.exists() else []
        degs = list(np.load(degp)) if degp.exists() and rows else []
        t0 = time.time()
        with Pool(workers, initializer=_init, initargs=(str(model),)) as pool:
            for r, st, deg, s in pool.imap(_rep, [(scheme, r) for r in range(len(rows), reps)], chunksize=2):
                st["rho_degree"] = spearman(deg0[act], deg[act])
                st["rho_strength"] = spearman(s0[act], s[act])
                rows.append(st)
                degs.append(deg[act])
                if len(rows) % 50 == 0:
                    part.write_text(json.dumps(rows))
                    np.save(degp, np.array(degs))
                    print(scheme, len(rows), "replicates", round(time.time() - t0), "s", flush=True)
        part.write_text(json.dumps(rows))
        np.save(degp, np.array(degs))
        res = {"strata_nonsingleton": len(M.strata[scheme]),
               "singleton_patent_share": float(M.__dict__[f"singleton_share_{scheme}"])}
        rd = np.array([x["rho_degree"] for x in rows])
        rs = np.array([x["rho_strength"] for x in rows])
        medd = np.median(np.array(degs), axis=0)
        within = np.abs(medd - deg0[act]) <= 0.2 * deg0[act]
        res["gate"] = {"median_rho_degree": float(np.median(rd)), "median_rho_strength": float(np.median(rs)),
                       "share_firms_null_median_degree_within_20pct": float(within.mean()),
                       "passed": bool(np.median(rd) >= 0.90 and np.median(rs) >= 0.95)}
        for key in ("T1", "T2", "OE_AI_MIXED", "OE_DEC_MIXED"):
            v = np.array([x[key] for x in rows])
            res[key] = {"observed": obs[key], "null_median": float(np.median(v)),
                        "null_2.5": float(np.percentile(v, 2.5)), "null_97.5": float(np.percentile(v, 97.5)),
                        "p_lower": float((1 + (v <= obs[key]).sum()) / (len(v) + 1))}
        t1 = res["T1"]
        res["share_of_T1_gap_reproduced_by_null"] = (1 - t1["null_median"]) / (1 - t1["observed"])
        a, b = res["T1"]["p_lower"] < .05, res["T2"]["p_lower"] < .05
        res["verdict"] = ("INVALID_NULL" if not res["gate"]["passed"] else
                          "HOLE_BEYOND_PORTFOLIO_AND_DEGREE" if a and b else "PARTIAL" if a or b else "PORTFOLIO_DEGREE_ARTEFACT")
        R[scheme] = res
        (out / "PLAN6_RESULTS.json").write_text(json.dumps(R, indent=1))
        print(scheme, res["verdict"], json.dumps(res["gate"]), flush=True)
    v = [R[s]["verdict"] for s in SCHEMES]
    R["tech_mix_sensitive"] = "INVALID_NULL" not in v and v[0] != v[1]
    (out / "PLAN6_RESULTS.json").write_text(json.dumps(R, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["export", "run"])
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--model", type=Path)
    ap.add_argument("--reps", type=int, default=1000)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    if a.mode == "export":
        export(a.out)
    else:
        run(a.model, a.out, a.reps, a.workers)


if __name__ == "__main__":
    main()
