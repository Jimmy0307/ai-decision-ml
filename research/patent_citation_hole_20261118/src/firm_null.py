"""Preregistration 4: portfolio-preserving null for the firm-level hole (see PREREGISTRATION_FIRM_NULL.md).

Usage:
    python src/firm_null.py --out outputs [--reps 1000]
Needs outputs/suite_cache_LOCAL.pkl (written by full_suite.py).
"""
from __future__ import annotations

import argparse
import json
import pickle
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import scipy.sparse as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import full_suite as fs  # noqa: E402
from cpc_matrix_v9 import assign_col, assign_row  # noqa: E402

SEED = 20261119
GROUPS = ("AI_FIRM", "DEC_FIRM", "MIXED")


class FirmModel:
    def __init__(self, D):
        year = D["year"]
        ai, dec = D["ai"], D["dec"]
        self.S = np.array(sorted(p for p in set(ai) | set(dec) if year[p] >= 2010), dtype=np.int64)
        S = self.S
        self.ptype = np.array([2 if (p in ai and p in dec) else 0 if p in ai else 1 for p in S.tolist()], np.int8)
        self.year = year[S]
        firms = sorted({f for p in S.tolist() for f in D["owners"].get(p, ())})
        self.firms = firms
        fi = {f: k for k, f in enumerate(firms)}
        lens = [len(D["owners"].get(p, ())) for p in S.tolist()]
        self.indptr = np.r_[0, np.cumsum(lens)].astype(np.int64)
        self.owner = np.array([fi[f] for p in S.tolist() for f in sorted(D["owners"].get(p, ()))], np.int64)
        kinds = defaultdict(set)
        names = ("AI", "DEC", "BRIDGE")
        for k in range(len(S)):
            for f in self.owner[self.indptr[k]:self.indptr[k + 1]]:
                kinds[int(f)].add(names[self.ptype[k]])
        self.group = np.array([("MIXED" if ("BRIDGE" in kinds[k] or kinds[k] >= {"AI", "DEC"})
                                else "AI_FIRM" if "AI" in kinds[k] else "DEC_FIRM") for k in range(len(firms))])
        inS = np.zeros(len(year), bool)
        inS[S] = True
        m = inS[D["ci"]] & inS[D["cj"]] & D["cat"]
        self.ca = np.searchsorted(S, D["ci"][m])
        self.cb = np.searchsorted(S, D["cj"][m])
        rows = [frozenset(assign_row(s) for s, _ in ai.get(p, [])) for p in S.tolist()]
        cols = [frozenset(c for c in (assign_col(s) for s, _ in dec.get(p, [])) if c) for p in S.tolist()]
        self.strata = {"primary": self._strata(list(zip(self.ptype.tolist(), self.year.tolist()))),
                       "S_tech": self._strata(list(zip(self.ptype.tolist(), self.year.tolist(),
                                                        map(lambda r: tuple(sorted(r)), rows),
                                                        map(lambda c: tuple(sorted(c)), cols))))}

    @staticmethod
    def _strata(keys):
        g = defaultdict(list)
        for k, key in enumerate(keys):
            g[key].append(k)
        return [np.array(v) for v in g.values() if len(v) > 1]

    def weights(self, perm=None):
        """Firm x firm symmetric tie weights when patent k carries the owner set of patent perm[k]."""
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
        n = len(self.firms)
        W = sp.coo_matrix((np.ones(len(lo)), (lo, hi)), shape=(n, n)).tocsr()
        W.sum_duplicates()
        return (W + W.T).tocsr()

    def stats(self, W):
        con, s = fs.constraint_sparse(W)
        g = self.group
        tot = W.sum() / 2
        Sg = {k: s[g == k].sum() for k in GROUPS}
        Wc = W.tocoo()
        oe = {}
        for a, b in (("AI_FIRM", "DEC_FIRM"), ("AI_FIRM", "MIXED"), ("DEC_FIRM", "MIXED")):
            O = float(Wc.data[(g[Wc.row] == a) & (g[Wc.col] == b)].sum())
            E = Sg[a] * Sg[b] / (2 * tot)
            oe[f"{a}~{b}"] = O / E if E else float("nan")
        act = s > 0
        return {"T1": oe["AI_FIRM~DEC_FIRM"], "T2": float(np.median(con[act & (g == "MIXED")])),
                "OE_AI_MIXED": oe["AI_FIRM~MIXED"], "OE_DEC_MIXED": oe["DEC_FIRM~MIXED"],
                "ties": int(W.nnz // 2), "weight": float(tot)}

    def null(self, scheme, reps, seed=SEED, done=None, checkpoint=None):
        """Replicate r uses its own seed sequence [seed, scheme, r], so interrupted runs resume exactly."""
        out = list(done or [])
        sid = ("primary", "S_tech").index(scheme)
        for r in range(len(out), reps):
            rng = np.random.default_rng([seed, sid, r])
            perm = np.arange(len(self.S))
            for g in self.strata[scheme]:
                perm[g] = rng.permutation(g)
            out.append(self.stats(self.weights(perm)))
            if checkpoint and (r + 1) % 100 == 0:
                checkpoint(out)
        return out

    def firm_counts(self, perm):
        """Per-firm (type, year) counts under perm; used to check the null preserves portfolios."""
        c = defaultdict(int)
        for k in range(len(self.S)):
            src = perm[k]
            for f in self.owner[self.indptr[src]:self.indptr[src + 1]]:
                c[(int(f), int(self.ptype[k]), int(self.year[k]))] += 1
        return c


def summarise(obs, null):
    res = {}
    for key in ("T1", "T2", "OE_AI_MIXED", "OE_DEC_MIXED"):
        v = np.array([x[key] for x in null])
        res[key] = {"observed": obs[key], "null_median": float(np.median(v)),
                    "null_2.5": float(np.percentile(v, 2.5)), "null_97.5": float(np.percentile(v, 97.5)),
                    "p_lower": float((1 + (v <= obs[key]).sum()) / (len(v) + 1))}
    t1 = res["T1"]
    res["share_of_T1_gap_reproduced_by_null"] = (1 - t1["null_median"]) / (1 - t1["observed"]) if t1["observed"] < 1 else None
    a, b = res["T1"]["p_lower"] < .05, res["T2"]["p_lower"] < .05
    res["verdict"] = "ORGANISATIONAL_HOLE_BEYOND_PORTFOLIO" if a and b else "PARTIAL" if a or b else "PORTFOLIO_ARTEFACT"
    return res


def build_or_load(out: Path):
    """Build the slim firm model once (needs the large suite cache), then reuse it."""
    slim = out / "firm_model_LOCAL.pkl"
    if slim.exists():
        with open(slim, "rb") as f:
            return pickle.load(f)
    import gc
    with open(out / "suite_cache_LOCAL.pkl", "rb") as f:
        D = pickle.load(f)
    M = FirmModel(D)
    del D
    gc.collect()
    with open(slim, "wb") as f:
        pickle.dump(M, f, protocol=4)
    return M


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--reps", type=int, default=1000)
    a = ap.parse_args(argv)
    t0 = time.time()
    M = build_or_load(a.out)
    obs = M.stats(M.weights())
    fs.log("observed", obs, "patents", len(M.S), "firms", len(M.firms), "citations", len(M.ca))
    p5 = json.loads((a.out / "FULL_SUITE_RESULTS.json").read_text(encoding="utf-8"))["P5"]
    assert abs(obs["T1"] - p5["group_OE"]["AI_FIRM~DEC_FIRM"]["OE"]) < 1e-9, "does not reproduce P5 T1"
    assert abs(obs["T2"] - p5["broker_test"]["mixed_median_constraint"]) < 1e-9, "does not reproduce P5 T2"
    assert obs["ties"] == p5["ties"], "does not reproduce P5 ties"
    rng = np.random.default_rng(1)
    perm = np.arange(len(M.S))
    for g in M.strata["primary"]:
        perm[g] = rng.permutation(g)
    assert M.firm_counts(perm) == M.firm_counts(np.arange(len(M.S))), "portfolio not preserved"
    R = {"preregistration": "PREREGISTRATION_FIRM_NULL.md v1.0", "observed": obs, "reps": a.reps,
         "seeding": "replicate r of scheme s uses default_rng([20261119, s, r])",
         "n_patents": int(len(M.S)), "n_firms": len(M.firms), "n_citations": int(len(M.ca)),
         "reproduces_P5": True, "portfolio_preserved_check": True}
    for scheme in ("primary", "S_tech"):
        part = a.out / f"FIRM_NULL_PARTIAL_{scheme}_LOCAL.json"
        done = json.loads(part.read_text(encoding="utf-8")) if part.exists() else []
        if done:
            fs.log(scheme, "resuming at", len(done))

        def ckpt(rows, part=part, scheme=scheme):
            part.write_text(json.dumps(rows, default=float), encoding="utf-8")
            fs.log(scheme, "checkpoint", len(rows))
        null = M.null(scheme, a.reps, done=done, checkpoint=ckpt)
        ckpt(null)
        R[scheme] = summarise(obs, null)
        R[scheme]["strata"] = len(M.strata[scheme])
        fs.log(scheme, R[scheme]["verdict"], R[scheme]["T1"], R[scheme]["T2"])
        (a.out / "FIRM_NULL_RESULTS.json").write_text(json.dumps(R, indent=2, default=float), encoding="utf-8")
    R["tech_mix_sensitive"] = R["primary"]["verdict"] != R["S_tech"]["verdict"]
    R["seconds"] = round(time.time() - t0)
    (a.out / "FIRM_NULL_RESULTS.json").write_text(json.dumps(R, indent=2, default=float), encoding="utf-8")
    fs.log("done", R["primary"]["verdict"], "S_tech", R["S_tech"]["verdict"])


if __name__ == "__main__":
    sys.exit(main())
