"""Preregistered patent-citation test of a structural hole between AI and decision technologies.

Implements PREREGISTRATION.md v1.0. Raw PatentsView files are read from a local folder
and never written out; outputs are aggregate counts only.

Usage:
    python src/patent_hole.py --inputs inputs_LOCAL --out outputs [--chunksize 5000000]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261118
N_BOOT = 2000
REF_CLASSES = ("G06", "G16", "H04")
REF_MIN_PATENTS = 2000
DEC_RE = re.compile(r"^G06Q10/0[46]")          # G06Q10/04 and G06Q10/06 incl. subgroups
AI_BROAD_RE = re.compile(r"^(G06N|G06F18|G06V10/70)")
APPLICANT = "cited by applicant"

REQUIRED = {
    "g_patent": ["patent_id", "patent_type", "patent_date", "withdrawn"],
    "g_cpc_current": ["patent_id", "cpc_group", "cpc_type"],
    "g_us_patent_citation": ["patent_id", "citation_patent_id", "citation_category"],
}


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


# ----------------------------------------------------------------------------- IO
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def find_input(folder: Path, stem: str) -> Path:
    for cand in (folder / f"{stem}.tsv.zip", folder / f"{stem}.tsv"):
        if cand.exists():
            return cand
    raise FileNotFoundError(f"missing {stem}.tsv.zip in {folder}")


def read_tsv(path: Path, usecols, chunksize=None, dtype=str):
    kw = dict(sep="\t", usecols=usecols, dtype=dtype, na_filter=False,
              chunksize=chunksize, on_bad_lines="warn", encoding="utf-8")
    if path.suffix == ".zip":
        z = zipfile.ZipFile(path)
        members = [m for m in z.namelist() if m.endswith(".tsv")]
        assert len(members) == 1, members
        header = z.open(members[0]).readline().decode("utf-8").rstrip("\r\n").split("\t")
        header = [h.strip('"') for h in header]
        missing = [c for c in usecols if c not in header]
        if missing:
            raise ValueError(f"{path.name}: missing columns {missing}; header={header}")
        return pd.read_csv(z.open(members[0]), **kw)
    return pd.read_csv(path, **kw)


def numeric_ids(s: pd.Series) -> np.ndarray:
    return pd.to_numeric(s.str.strip('"'), errors="coerce").to_numpy()


# ----------------------------------------------------------------------------- tables
@dataclass
class Universe:
    pid: np.ndarray            # sorted int64 patent ids
    year: np.ndarray           # int16 grant year
    flags: dict = field(default_factory=dict)       # name -> bool array
    ref_csr: dict = field(default_factory=dict)      # scheme -> (indptr, groups)
    group_names: list = field(default_factory=list)

    def index(self, ids: np.ndarray) -> np.ndarray:
        """Map patent ids to positions; -1 if not in universe."""
        pos = np.searchsorted(self.pid, ids)
        pos = np.clip(pos, 0, len(self.pid) - 1)
        ok = self.pid[pos] == ids
        return np.where(ok, pos, -1)


def load_patents(path: Path) -> Universe:
    df = read_tsv(path, REQUIRED["g_patent"])
    df = df[(df.patent_type.str.strip('"').str.lower() == "utility")
            & (~df.withdrawn.str.strip('"').isin(["1", "true", "True"]))]
    ids = numeric_ids(df.patent_id)
    yr = pd.to_numeric(df.patent_date.str.strip('"').str[:4], errors="coerce").to_numpy()
    ok = ~np.isnan(ids) & ~np.isnan(yr)
    ids, yr = ids[ok].astype(np.int64), yr[ok].astype(np.int16)
    order = np.argsort(ids)
    return Universe(pid=ids[order], year=yr[order])


def build_memberships(u: Universe, cpc) -> None:
    """cpc: a DataFrame or an iterable of DataFrames with patent_id, cpc_group, cpc_type (str)."""
    chunks = [cpc] if isinstance(cpc, pd.DataFrame) else cpc
    n = len(u.pid)
    names_flags = ["AI", "DEC", "BIZ", "AI_inv", "DEC_inv", "BIZ_inv", "AI_BROAD", "DEC_ALL"]
    for k in names_flags:
        u.flags[k] = np.zeros(n, bool)
    ref_idx, ref_main, ref_inv = [], [], []
    rows = 0
    for ch in chunks:
        idx = u.index(numeric_ids(ch.patent_id))
        keep = idx >= 0
        s = ch.cpc_group.str.strip('"').str.replace(" ", "", regex=False)[keep].reset_index(drop=True)
        # PatentsView labels inventive codes "inventional" (amendment A1); accept both spellings.
        inv = ch.cpc_type.str.strip('"').str.lower().isin(["inventive", "inventional"]).to_numpy()[keep]
        idx = idx[keep]
        rows += len(ch)
        is_ai = s.str.startswith("G06N").to_numpy()
        is_dec = s.str.match(DEC_RE).to_numpy()
        is_biz = (s.str.startswith("G06Q") & ~s.str.startswith("G06Q10/")).to_numpy()
        for name, mask in (("AI", is_ai), ("DEC", is_dec), ("BIZ", is_biz),
                           ("AI_inv", is_ai & inv), ("DEC_inv", is_dec & inv), ("BIZ_inv", is_biz & inv),
                           ("AI_BROAD", s.str.match(AI_BROAD_RE).to_numpy()),
                           ("DEC_ALL", s.str.startswith("G06Q10/").to_numpy())):
            u.flags[name][idx[mask]] = True
        is_ref = s.str.startswith(REF_CLASSES).to_numpy()
        ref_idx.append(idx[is_ref].astype(np.int64))
        ref_main.append(s[is_ref].str.split("/", n=1).str[0].to_numpy())
        ref_inv.append(inv[is_ref])
        if not isinstance(cpc, pd.DataFrame):
            log(f"cpc rows {rows:,}")
    idx = np.concatenate(ref_idx)
    main = np.concatenate(ref_main) if ref_main else np.array([], object)
    inv = np.concatenate(ref_inv)
    codes, names = pd.factorize(pd.Series(main, dtype=object), sort=True)
    u.group_names = [str(x) for x in names]
    G = max(len(names), 1)
    for scheme, sel in (("all", np.ones(len(idx), bool)), ("inv", inv)):
        pairs = np.unique(idx[sel] * G + codes[sel])
        p, g = pairs // G, (pairs % G).astype(np.int32)
        indptr = np.zeros(n + 1, np.int64)
        indptr[1:] = np.cumsum(np.bincount(p, minlength=n))
        u.ref_csr[scheme] = (indptr, g)


def load_citations(path: Path, u: Universe, first_year: int, chunksize: int):
    out_i, out_j, out_c = [], [], []
    total = 0
    for k, ch in enumerate(read_tsv(path, REQUIRED["g_us_patent_citation"], chunksize=chunksize)):
        i = u.index(numeric_ids(ch.patent_id))
        j = u.index(numeric_ids(ch.citation_patent_id))
        ok = (i >= 0) & (j >= 0)
        ok[ok] &= u.year[i[ok]] >= first_year
        cat = (ch.citation_category.str.strip('"').str.lower() == APPLICANT).to_numpy()
        out_i.append(i[ok].astype(np.int32))
        out_j.append(j[ok].astype(np.int32))
        out_c.append(cat[ok])
        total += len(ch)
        log(f"citations chunk {k}: read {total:,} kept {sum(map(len, out_i)):,}")
    return np.concatenate(out_i), np.concatenate(out_j), np.concatenate(out_c), total


# ----------------------------------------------------------------------------- statistics
def explode(rows: np.ndarray, csr):
    """For each row (patent index) return (row_position, group) pairs."""
    indptr, groups = csr
    starts, ends = indptr[rows], indptr[rows + 1]
    lens = (ends - starts).astype(np.int64)
    pos = np.repeat(np.arange(len(rows)), lens)
    offs = np.arange(lens.sum()) - np.repeat(np.cumsum(lens) - lens, lens)
    return pos, groups[np.repeat(starts, lens) + offs]


@dataclass
class Cites:
    i: np.ndarray
    j: np.ndarray
    s: np.ndarray
    n_strata: int


def strata(u: Universe, i, j, y0: int) -> Cites:
    ymin = int(u.year.min())
    ny = int(u.year.max()) - ymin + 1
    s = (u.year[i].astype(np.int32) - y0) * ny + (u.year[j].astype(np.int32) - ymin)
    n_s = (int(u.year.max()) - y0 + 1) * ny
    return Cites(i, j, s, n_s)


def oe_pair(c: Cites, A: np.ndarray, B: np.ndarray, M: np.ndarray):
    """Symmetric O/E plus per-direction components for boolean patent sets A, B."""
    Mi = np.where(M > 0, 1.0 / np.maximum(M, 1), 0.0)
    out_a = np.bincount(c.s[A[c.i]], minlength=c.n_strata)
    out_b = np.bincount(c.s[B[c.i]], minlength=c.n_strata)
    in_a = np.bincount(c.s[A[c.j]], minlength=c.n_strata)
    in_b = np.bincount(c.s[B[c.j]], minlength=c.n_strata)
    o_ab = int(np.sum(A[c.i] & B[c.j]))
    o_ba = int(np.sum(B[c.i] & A[c.j]))
    e_ab = float(np.sum(out_a * in_b * Mi))
    e_ba = float(np.sum(out_b * in_a * Mi))
    return dict(O_ab=o_ab, O_ba=o_ba, E_ab=e_ab, E_ba=e_ba,
                OE=(o_ab + o_ba) / (e_ab + e_ba) if e_ab + e_ba > 0 else float("nan"),
                in_a=in_a, in_b=in_b)


BLOCK = 4_000_000
_KEYS = {}


def csr_keys(csr, n_groups):
    """Sorted (patent * G + group) keys of a membership CSR, cached per CSR object."""
    k = id(csr[1])
    if k not in _KEYS:
        indptr, groups = csr
        owner = np.repeat(np.arange(len(indptr) - 1, dtype=np.int64), np.diff(indptr))
        _KEYS[k] = owner * n_groups + groups
    return _KEYS[k]


def member(rows: np.ndarray, grp: np.ndarray, csr, n_groups: int) -> np.ndarray:
    keys = csr_keys(csr, n_groups)
    if not len(keys):
        return np.zeros(len(rows), bool)
    q = rows.astype(np.int64) * n_groups + grp
    pos = np.clip(np.searchsorted(keys, q), 0, len(keys) - 1)
    return keys[pos] == q


def _bc(s, g, S, G):
    return np.bincount(s.astype(np.int64) * G + g, minlength=S * G).reshape(S, G)


def ref_margins(c: Cites, csr, n_groups: int):
    """out_X(s), in_X(s) for all reference groups; computed in blocks to bound memory."""
    S, G = c.n_strata, n_groups
    out_X = np.zeros((S, G), np.int64)
    in_X = np.zeros((S, G), np.int64)
    for b in range(0, len(c.i), BLOCK):
        sl = slice(b, b + BLOCK)
        s = c.s[sl]
        p, g = explode(c.i[sl], csr)
        out_X += _bc(s[p], g, S, G)
        p, g = explode(c.j[sl], csr)
        in_X += _bc(s[p], g, S, G)
    return out_X, in_X


def oe_vs_reference(c: Cites, F: np.ndarray, csr, n_groups: int, M: np.ndarray, margins=None):
    """OE(F \ X, X \ F) for every reference group X (vectorised over groups, blocked over citations)."""
    S, G = c.n_strata, n_groups
    Mi = np.where(M > 0, 1.0 / np.maximum(M, 1), 0.0)
    out_X, in_X = margins if margins is not None else ref_margins(c, csr, G)
    out_FX = np.zeros((S, G), np.int64)
    in_FX = np.zeros((S, G), np.int64)
    O = np.zeros(G, np.int64)
    for b in range(0, len(c.i), BLOCK):
        sl = slice(b, b + BLOCK)
        ci, cj, s = c.i[sl], c.j[sl], c.s[sl]
        Fi, Fj = F[ci], F[cj]
        # citing in F: membership of citing (for out_FX) and of cited (for O1)
        rows = np.flatnonzero(Fi)
        p, g = explode(ci[rows], csr)
        out_FX += _bc(s[rows][p], g, S, G)
        p, g = explode(cj[rows], csr)                      # cited groups X
        r = rows[p]
        keep = ~Fj[r]
        r, g = r[keep], g[keep]
        ok = ~member(ci[r], g, csr, G)                      # citing not in X
        O += np.bincount(g[ok], minlength=G)
        # cited in F: membership of cited (for in_FX) and of citing (for O2)
        rows = np.flatnonzero(Fj)
        p, g = explode(cj[rows], csr)
        in_FX += _bc(s[rows][p], g, S, G)
        p, g = explode(ci[rows], csr)                      # citing groups X
        r = rows[p]
        keep = ~Fi[r]
        r, g = r[keep], g[keep]
        ok = ~member(cj[r], g, csr, G)                      # cited not in X
        O += np.bincount(g[ok], minlength=G)
    out_F = np.bincount(c.s[F[c.i]], minlength=S)
    in_F = np.bincount(c.s[F[c.j]], minlength=S)
    E = (((out_F[:, None] - out_FX) * (in_X - in_FX) + (out_X - out_FX) * (in_F[:, None] - in_FX))
         * Mi[:, None]).sum(0)
    with np.errstate(invalid="ignore", divide="ignore"):
        return O, E, np.where(E > 0, O / E, np.nan)


def per_patent_contrib(c: Cites, src: np.ndarray, dst: np.ndarray, in_dst: np.ndarray, M: np.ndarray, n: int):
    """o(p), e(p) for citing patents p in src, toward dst."""
    Mi = np.where(M > 0, 1.0 / np.maximum(M, 1), 0.0)
    m = src[c.i]
    o = np.bincount(c.i[m], weights=dst[c.j[m]].astype(float), minlength=n)
    e = np.bincount(c.i[m], weights=(in_dst * Mi)[c.s[m]], minlength=n)
    return o, e


def bootstrap(contribs: dict, years: np.ndarray, n_boot=N_BOOT, seed=SEED, batch=100):
    """contribs: name -> (o, e) arrays over patents. Poisson weights shared across names."""
    involved = np.flatnonzero(np.any([(o != 0) | (e != 0) for o, e in contribs.values()], axis=0))
    rng = np.random.default_rng(seed)
    yrs = years[involved]
    uy = np.unique(yrs)
    res = {k: [] for k in contribs}
    res_y = {k: [] for k in contribs}
    for b0 in range(0, n_boot, batch):
        W = rng.poisson(1.0, size=(min(batch, n_boot - b0), len(involved))).astype(np.float32)
        for k, (o, e) in contribs.items():
            O, E = W @ o[involved].astype(np.float32), W @ e[involved].astype(np.float32)
            res[k].append(np.column_stack([O, E]))
            Oy = np.column_stack([W[:, yrs == y] @ o[involved][yrs == y].astype(np.float32) for y in uy])
            Ey = np.column_stack([W[:, yrs == y] @ e[involved][yrs == y].astype(np.float32) for y in uy])
            res_y[k].append(np.stack([Oy, Ey], -1))
    return {k: np.vstack(v) for k, v in res.items()}, {k: np.vstack(v) for k, v in res_y.items()}, uy


def ci(x):
    x = x[np.isfinite(x)]
    return [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))] if len(x) else [None, None]


# ----------------------------------------------------------------------------- one specification
SPECS = {
    "primary":            dict(applicant_only=True,  ai="AI",       dec="DEC",     biz="BIZ",     ref="all", y0=2010, bridge="exclude"),
    "s1_all_categories":  dict(applicant_only=False, ai="AI",       dec="DEC",     biz="BIZ",     ref="all", y0=2010, bridge="exclude"),
    "s2_dec_all_G06Q10":  dict(applicant_only=True,  ai="AI",       dec="DEC_ALL", biz="BIZ",     ref="all", y0=2010, bridge="exclude"),
    "s3_ai_broad":        dict(applicant_only=True,  ai="AI_BROAD", dec="DEC",     biz="BIZ",     ref="all", y0=2010, bridge="exclude"),
    "s4_inventive_only":  dict(applicant_only=True,  ai="AI_inv",   dec="DEC_inv", biz="BIZ_inv", ref="inv", y0=2010, bridge="exclude"),
    "s5_window_2015":     dict(applicant_only=True,  ai="AI",       dec="DEC",     biz="BIZ",     ref="all", y0=2015, bridge="exclude"),
    "s6_bridge_both":     dict(applicant_only=True,  ai="AI",       dec="DEC",     biz="BIZ",     ref="all", y0=2010, bridge="both"),
}


def run_spec(u: Universe, ci_all, cj_all, ccat, spec: dict, n_boot=N_BOOT, boot=True):
    keep = (u.year[ci_all] >= spec["y0"])
    if spec["applicant_only"]:
        keep &= ccat
    c = strata(u, ci_all[keep], cj_all[keep], spec["y0"])
    M = np.bincount(c.s, minlength=c.n_strata)
    AI, DEC, BIZ = u.flags[spec["ai"]], u.flags[spec["dec"]], u.flags[spec["biz"]]
    if spec["bridge"] == "exclude":
        A, D = AI & ~DEC, DEC & ~AI
    else:
        A, D = AI, DEC
    A2, B2 = AI & ~BIZ, BIZ & ~AI
    pd_ = oe_pair(c, A, D, M)
    pb_ = oe_pair(c, A2, B2, M)

    csr = u.ref_csr[spec["ref"]]
    G = len(u.group_names)
    in_window = u.year >= spec["y0"]
    counts = np.bincount(explode(np.flatnonzero(in_window), csr)[1], minlength=G)
    ref = [g for g in range(G)
           if counts[g] >= REF_MIN_PATENTS
           and not u.group_names[g].startswith("G06N") and u.group_names[g] != "G06Q10"]
    margins = ref_margins(c, csr, G)
    _, _, oe_ai = oe_vs_reference(c, AI, csr, G, M, margins)
    _, _, oe_dec = oe_vs_reference(c, DEC, csr, G, M, margins)
    del margins
    ai_ref, dec_ref = oe_ai[ref], oe_dec[ref]
    q25_ai, q25_dec = float(np.nanpercentile(ai_ref, 25)), float(np.nanpercentile(dec_ref, 25))
    pr_ai = float(np.mean(ai_ref < pd_["OE"]))
    pr_dec = float(np.mean(dec_ref < pd_["OE"]))
    h1a = pd_["OE"] <= q25_ai and pd_["OE"] <= q25_dec

    out = dict(
        spec=spec, n_citations=int(len(c.i)),
        n_patents=dict(AI=int(AI[in_window].sum()), DEC=int(DEC[in_window].sum()),
                       BRIDGE=int((AI & DEC)[in_window].sum()), BIZ=int(BIZ[in_window].sum())),
        AI_DEC={k: v for k, v in pd_.items() if not isinstance(v, np.ndarray)},
        AI_BIZ={k: v for k, v in pb_.items() if not isinstance(v, np.ndarray)},
        reference=dict(n_fields=len(ref), q25_AI=q25_ai, q25_DEC=q25_dec,
                       median_AI=float(np.nanmedian(ai_ref)), median_DEC=float(np.nanmedian(dec_ref)),
                       percentile_rank_in_AI_ref=pr_ai, percentile_rank_in_DEC_ref=pr_dec,
                       lowest_AI=[(u.group_names[ref[k]], float(ai_ref[k])) for k in np.argsort(ai_ref)[:5]],
                       lowest_DEC=[(u.group_names[ref[k]], float(dec_ref[k])) for k in np.argsort(dec_ref)[:5]]),
        H1a=bool(h1a),
        ratio_point=pd_["OE"] / pb_["OE"] if pb_["OE"] > 0 else float("nan"),
    )
    if not boot:
        return out, c, M
    n = len(u.pid)
    o1, e1 = per_patent_contrib(c, A, D, pd_["in_b"], M, n)
    o2, e2 = per_patent_contrib(c, D, A, pd_["in_a"], M, n)
    o3, e3 = per_patent_contrib(c, A2, B2, pb_["in_b"], M, n)
    o4, e4 = per_patent_contrib(c, B2, A2, pb_["in_a"], M, n)
    B, By, uy = bootstrap({"dec": (o1 + o2, e1 + e2), "biz": (o3 + o4, e3 + e4)}, u.year, n_boot=n_boot)
    oe_dec_b = B["dec"][:, 0] / B["dec"][:, 1]
    oe_biz_b = B["biz"][:, 0] / B["biz"][:, 1]
    ratio_b = oe_dec_b / oe_biz_b
    out["AI_DEC"]["OE_CI95"] = ci(oe_dec_b)
    out["ratio_CI95"] = ci(ratio_b)
    out["H1b"] = bool(out["ratio_point"] < 1 and out["ratio_CI95"][1] is not None and out["ratio_CI95"][1] < 1)
    # H2: by citing year
    Oy, Ey = By["dec"][..., 0], By["dec"][..., 1]
    oe_y_b = Oy / np.where(Ey > 0, Ey, np.nan)
    o_pt = np.array([(o1 + o2)[(u.year == y)].sum() for y in uy])
    e_pt = np.array([(e1 + e2)[(u.year == y)].sum() for y in uy])
    oe_y = np.where(e_pt > 0, o_pt / np.where(e_pt > 0, e_pt, 1), np.nan)
    var = np.nanvar(oe_y_b, axis=0)
    w = np.where((var > 0) & np.isfinite(oe_y), 1 / np.where(var > 0, var, 1), 0)
    x = uy.astype(float)

    def wls(yv):
        ok = np.isfinite(yv) & (w > 0)
        if ok.sum() < 3:
            return np.nan
        xm = np.average(x[ok], weights=w[ok])
        ym = np.average(yv[ok], weights=w[ok])
        return float(np.sum(w[ok] * (x[ok] - xm) * (yv[ok] - ym)) / np.sum(w[ok] * (x[ok] - xm) ** 2))

    slope = wls(oe_y)
    slope_b = np.array([wls(r) for r in oe_y_b])
    last3 = float(np.nansum(o_pt[-3:]) / np.nansum(e_pt[-3:])) if np.nansum(e_pt[-3:]) > 0 else float("nan")
    s_ci = ci(slope_b)
    ref_med = min(out["reference"]["median_AI"], out["reference"]["median_DEC"])
    if s_ci[0] is not None and s_ci[0] > 0 and last3 >= ref_med:
        h2 = "CLOSING"
    elif s_ci[0] is None or s_ci[0] <= 0:
        h2 = "PERSISTENT"
    else:
        h2 = "NARROWING_BUT_OPEN"
    out["H2"] = dict(by_year=[dict(year=int(y), O=float(o), E=float(e), OE=float(r), CI95=ci(oe_y_b[:, k]))
                              for k, (y, o, e, r) in enumerate(zip(uy, o_pt, e_pt, oe_y))],
                     slope=slope, slope_CI95=s_ci, OE_last3=last3, reference_median=ref_med, verdict=h2)
    out["verdict"] = ("HOLE_SUPPORTED" if out["H1a"] and out["H1b"]
                      else "PARTIAL_NOT_CLAIMED" if out["H1a"] or out["H1b"] else "HOLE_NOT_SUPPORTED")
    return out, c, M


# ----------------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--chunksize", type=int, default=5_000_000)
    ap.add_argument("--n-boot", type=int, default=N_BOOT)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    files = {k: find_input(a.inputs, k) for k in REQUIRED}
    prov = {k: dict(file=p.name, bytes=p.stat().st_size, sha256=sha256(p)) for k, p in files.items()}
    log("provenance", json.dumps(prov))
    u = load_patents(files["g_patent"])
    log(f"utility patents {len(u.pid):,}, years {u.year.min()}-{u.year.max()}")
    build_memberships(u, read_tsv(files["g_cpc_current"], REQUIRED["g_cpc_current"], chunksize=a.chunksize))
    log("memberships", {k: int(v.sum()) for k, v in u.flags.items()}, "ref groups", len(u.group_names))
    y_end = int(u.year.max())
    if (u.year == y_end).sum() < 0.5 * (u.year == y_end - 1).sum():
        y_end -= 1                                   # last complete calendar year
    keep = u.year <= y_end
    log("Y_end", y_end)
    cache = a.out / "cache_citations_LOCAL.npz"
    if cache.exists() and json.loads(str(np.load(cache)["prov"])) == prov:
        z = np.load(cache)
        ci_all, cj_all, ccat, total = z["i"], z["j"], z["c"], int(z["total"])
        log(f"citations from cache {len(ci_all):,}")
    else:
        ci_all, cj_all, ccat, total = load_citations(files["g_us_patent_citation"], u, 2010, a.chunksize)
        np.savez(cache, i=ci_all, j=cj_all, c=ccat, total=total, prov=json.dumps(prov))
    m = keep[ci_all]
    ci_all, cj_all, ccat = ci_all[m], cj_all[m], ccat[m]
    out_file = a.out / "PATENT_HOLE_RESULTS.json"
    results = dict(preregistration="PREREGISTRATION.md v1.0 (+A1)", provenance=prov, Y_end=y_end,
                   citation_rows_read=int(total), citations_in_scope=int(len(ci_all)),
                   applicant_share=float(ccat.mean()), specs={})
    if out_file.exists():
        old = json.loads(out_file.read_text(encoding="utf-8"))
        if old.get("provenance") == prov:
            results["specs"] = {k: v for k, v in old.get("specs", {}).items() if "verdict" in v}
            log("resuming; done:", list(results["specs"]))
    for name, spec in SPECS.items():
        if name in results["specs"]:
            continue
        log("spec", name)
        r, _, _ = run_spec(u, ci_all, cj_all, ccat, spec, n_boot=a.n_boot)
        results["specs"][name] = r
        out_file.write_text(json.dumps(results, indent=2, default=float), encoding="utf-8")
        log(name, r["verdict"], "OE", round(r["AI_DEC"]["OE"], 4), "ratio", round(r["ratio_point"], 4))
    prim = results["specs"]["primary"]["verdict"]
    disagree = sum(results["specs"][k]["verdict"] != prim for k in SPECS if k != "primary")
    results["primary_verdict"] = prim
    results["sensitivity_disagreements"] = disagree
    results["fragile"] = disagree >= 4
    out_file.write_text(json.dumps(results, indent=2, default=float), encoding="utf-8")
    log("done", prim, "fragile" if results["fragile"] else "robust", f"{disagree}/6 disagree")


if __name__ == "__main__":
    sys.exit(main())
