"""Preregistration 2: the V9 test battery (ra_lib, unchanged) on a patent AI-method x decision-function matrix.

Usage:
    python src/cpc_matrix_v9.py --inputs inputs_LOCAL --out outputs [--quick]
Needs outputs/cache_citations_LOCAL.npz produced by patent_hole.py (same inputs).
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import patent_hole as ph  # noqa: E402  (loaders only)
import ra_lib  # noqa: E402            (V9 engine, byte-identical to PR #4)

ROWS = ["G06N3", "G06N5", "G06N7", "G06N10", "G06N20", "G06N_OTHER"]
COLS = ["FORECAST_OPTIMISE", "RESOURCE_SCHEDULING", "WORKFLOW", "RISK", "STRATEGY", "PERFORMANCE", "MGMT_GENERAL"]
_COL_RULES = [("FORECAST_OPTIMISE", r"^G06Q10/04"), ("RESOURCE_SCHEDULING", r"^G06Q10/0631"),
              ("WORKFLOW", r"^G06Q10/0633"), ("RISK", r"^G06Q10/0635"), ("STRATEGY", r"^G06Q10/0637"),
              ("PERFORMANCE", r"^G06Q10/0639"), ("MGMT_GENERAL", r"^G06Q10/06")]
_COL_RULES = [(n, re.compile(p)) for n, p in _COL_RULES]
_ROW_RE = re.compile(r"^(G06N\d+)/")


def assign_row(sym: str):
    if not sym.startswith("G06N"):
        return None
    m = _ROW_RE.match(sym)
    g = m.group(1) if m else "G06N_OTHER"
    return g if g in ROWS else "G06N_OTHER"


def assign_col(sym: str):
    for name, rx in _COL_RULES:
        if rx.match(sym):
            return name
    return None


def collect_codes(u, chunks):
    """patent index -> list of AI symbols, list of DEC symbols (only G06N / G06Q10/04,06 codes)."""
    ai, dec = defaultdict(list), defaultdict(list)
    for ch in chunks:
        s = ch.cpc_group.str.strip('"').str.replace(" ", "", regex=False)
        m = s.str.startswith("G06N") | s.str.match(r"^G06Q10/0[46]")
        if not m.any():
            continue
        idx = u.index(ph.numeric_ids(ch.patent_id[m]))
        for p, sym in zip(idx, s[m]):
            if p < 0:
                continue
            if sym.startswith("G06N"):
                ai[int(p)].append(sym)
            else:
                dec[int(p)].append(sym)
    return ai, dec


def pairs_for(doc, ai_syms, dec_syms):
    """Deduplicated (doc,row,col) edges and raw code-level records for one document."""
    rows = {assign_row(a) for a in ai_syms}
    cols = {assign_col(d) for d in dec_syms} - {None}
    edges = [(doc, r, c) for r in sorted(rows) for c in sorted(cols)]
    raw = [(doc, assign_row(a), assign_col(d)) for a in ai_syms for d in dec_syms if assign_col(d)]
    return edges, raw


def build_part_a(ai, dec, year, y0, y1):
    E, R = [], []
    for p in sorted(set(ai) & set(dec)):
        if y0 <= year[p] <= y1:
            e, r = pairs_for(f"P{p}", ai[p], dec[p])
            E += e
            R += r
    return E, R


def build_part_b(ai, dec, ci, cj):
    """Citations between AI-only and DEC-only patents, either direction."""
    E, R = [], []
    n = int(max(ci.max(initial=0), cj.max(initial=0), max(ai, default=0), max(dec, default=0))) + 1
    is_ai, is_dec = np.zeros(n, bool), np.zeros(n, bool)
    is_ai[list(ai)] = True
    is_dec[list(dec)] = True
    a_only, d_only = is_ai & ~is_dec, is_dec & ~is_ai
    cand = np.flatnonzero((a_only[ci] & d_only[cj]) | (d_only[ci] & a_only[cj]))
    for k in cand.tolist():
        i, j = int(ci[k]), int(cj[k])
        if a_only[i] and d_only[j]:
            a, d = i, j
        elif d_only[i] and a_only[j]:
            a, d = j, i
        else:
            continue
        e, r = pairs_for(f"C{k}", ai[a], dec[d])
        E += e
        R += r
    return E, R


def run_matrix(name, edges, raw, out, quick=False):
    t = time.time()
    kw = dict(R=200, doc_samples=200) if quick else {}
    rows, summary = ra_lib.analyze(edges, raw, ROWS, COLS, **kw)
    summary["documents"] = len({d for d, _, _ in edges})
    summary["seconds"] = round(time.time() - t, 1)
    with open(out / f"V9_MATRIX_{name}_CELLS.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    ph.log(name, json.dumps({k: v for k, v in summary.items() if k != "doc_null_diagnostics"}))
    return rows, summary


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--quick", action="store_true", help="reduced replicates for a smoke test")
    a = ap.parse_args(argv)
    files = {k: ph.find_input(a.inputs, k) for k in ("g_patent", "g_cpc_current")}
    u = ph.load_patents(files["g_patent"])
    y1 = int(u.year.max())
    if (u.year == y1).sum() < 0.5 * (u.year == y1 - 1).sum():
        y1 -= 1
    ai, dec = collect_codes(u, ph.read_tsv(files["g_cpc_current"], ph.REQUIRED["g_cpc_current"], chunksize=5_000_000))
    ph.log(f"patents with AI codes {len(ai):,}, DEC codes {len(dec):,}")
    z = np.load(a.out / "cache_citations_LOCAL.npz")
    ci, cj, cat = z["i"], z["j"], z["c"]
    keep = (u.year[ci] >= 2010) & (u.year[ci] <= y1)
    ci, cj, cat = ci[keep], cj[keep], cat[keep]
    results = {"preregistration": "PREREGISTRATION_V9_MATRIX.md v1.0", "engine_sha256": ra_lib.sha256(ra_lib.__file__),
               "rows": ROWS, "cols": COLS, "window": [2010, y1], "parts": {}}
    plan = [("A_coclassification", build_part_a(ai, dec, u.year, 2010, y1)),
            ("B_citation_applicant", build_part_b(ai, dec, ci[cat], cj[cat])),
            ("B_citation_all_categories", build_part_b(ai, dec, ci, cj))]
    cells = {}
    for name, (E, R) in plan:
        ph.log(f"{name}: edges {len(E):,}, raw {len(R):,}")
        rows, summary = run_matrix(name, E, R, a.out, quick=a.quick)
        results["parts"][name] = summary
        cells[name] = rows
        (a.out / "V9_MATRIX_RESULTS.json").write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")

    def depleted(name):
        return {(r["ai_family"], r["decision_family"]) for r in cells[name]
                if r["full_core"] and r["core_direction"] == "DEPLETED"}
    conv = sorted(depleted("A_coclassification") & depleted("B_citation_applicant"))
    results["convergent_depleted_cells"] = [list(x) for x in conv]
    results["convergent_depleted_count"] = len(conv)
    (a.out / "V9_MATRIX_RESULTS.json").write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    ph.log("done; convergent depleted cells:", conv)


if __name__ == "__main__":
    sys.exit(main())
