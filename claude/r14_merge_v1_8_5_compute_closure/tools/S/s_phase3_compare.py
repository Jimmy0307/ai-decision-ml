"""V1.8.5 sub-agent S, Phase 3: compare the baseline reproduction against the 13 official outputs.

Usage: python -I s_phase3_compare.py <official_13_manifest_csv> <inputs_dir> <run_dir> <out_csv> <out_json>
Per output: byte sha256, row count, schema (header / top-level keys), sort order (key sequence),
numeric values (parsed, exact), key membership. Also lists every other (non-pinned) file of each stage dir.
Classification for non-identical outputs is reported, never approved.
"""
import csv
import hashlib
import io
import json
import sys
from pathlib import Path

KEYS = {"DOCUMENT_PAIR_EDGES_DEDUP.csv": ("document_id", "ai_family", "decision_family"),
        "MATRIX_DOCUMENT_DEDUP_COUNTS_10X12.csv": ("AI_FAMILY",), "MATRIX_RAW_RECORD_COUNTS_10X12.csv": ("AI_FAMILY",)}
STAGE_DIR = {"10": "10_DOCUMENT_DEDUP_MATRIX", "11": "11_NULL_MODEL_NETWORK", "12": "12_ROBUSTNESS_SENSITIVITY", "13": "13_RESULTS_FREEZE"}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def latest(run: Path, stage: str) -> Path:
    root = run / STAGE_DIR[stage]
    ptr = next(root.glob("LATEST_*.txt"))
    return Path(ptr.read_text(encoding="utf-8").strip())


def csv_rows(b: bytes):
    return list(csv.reader(io.StringIO(b.decode("utf-8-sig"), newline="")))


def num(x):
    try:
        return float(x)
    except ValueError:
        return None


def compare_csv(ob, rb, fn):
    o, r = csv_rows(ob), csv_rows(rb)
    res = {"rows_official": len(o) - 1, "rows_repro": len(r) - 1, "schema_equal": o[:1] == r[:1]}
    hdr = o[0] if o else []
    kcols = KEYS.get(fn)
    if kcols is None:
        kcols = tuple(c for c in ("ai_family", "decision_family") if c in hdr) or (hdr[0],)
    idx = [hdr.index(c) for c in kcols if c in hdr]
    ok_ = [tuple(row[i] for i in idx) for row in o[1:]]
    rk_ = [tuple(row[i] for i in idx) for row in r[1:]] if r[:1] == o[:1] else []
    res["key_columns"] = "|".join(kcols)
    res["key_membership_equal"] = set(ok_) == set(rk_)
    res["sort_order_equal"] = ok_ == rk_
    ndiff, nmax, sdiff = 0, 0.0, 0
    if res["schema_equal"] and len(o) == len(r):
        for a, b in zip(o[1:], r[1:]):
            for x, y in zip(a, b):
                if x == y:
                    continue
                fx, fy = num(x), num(y)
                if fx is not None and fy is not None:
                    ndiff += fx != fy
                    nmax = max(nmax, abs(fx - fy))
                else:
                    sdiff += 1
    res["numeric_cells_differing"] = ndiff
    res["numeric_max_abs_diff"] = nmax
    res["text_cells_differing"] = sdiff
    return res


def flatten(x, p=""):
    if isinstance(x, dict):
        out = {}
        for k, v in x.items():
            out.update(flatten(v, f"{p}.{k}"))
        return out
    if isinstance(x, list):
        out = {}
        for i, v in enumerate(x):
            out.update(flatten(v, f"{p}[{i}]"))
        return out
    return {p: x}


def compare_json(ob, rb):
    o, r = json.loads(ob), json.loads(rb)
    fo, fr = flatten(o), flatten(r)
    nd = [k for k in fo if k in fr and fo[k] != fr[k]]
    return {"rows_official": len(fo), "rows_repro": len(fr), "schema_equal": sorted(o) == sorted(r),
            "key_columns": "flattened JSON paths", "key_membership_equal": set(fo) == set(fr),
            "sort_order_equal": list(fo) == list(fr), "numeric_cells_differing": sum(isinstance(fo[k], (int, float)) for k in nd),
            "numeric_max_abs_diff": max([abs(fo[k] - fr[k]) for k in nd if isinstance(fo[k], (int, float)) and isinstance(fr[k], (int, float))] or [0.0]),
            "text_cells_differing": sum(not isinstance(fo[k], (int, float)) for k in nd), "parsed_equal": o == r}


def main():
    man, inp, run, out_csv, out_json = (Path(a) for a in sys.argv[1:6])
    rows, extra = [], []
    for m in csv.DictReader(man.open(encoding="utf-8")):
        fn, stage = m["filename"], m["producer_stage"]
        rel = Path(m["historical_path"].split("20260911_AI_DECISION_V5_PRODUCTION\\", 1)[1])
        ob = (inp / "V5" / rel).read_bytes()
        rdir = latest(run, stage)
        rp = rdir / fn
        rb = rp.read_bytes()
        res = compare_json(ob, rb) if fn.endswith(".json") else compare_csv(ob, rb, fn)
        h = sha(rb)
        byte_id = h == m["historical_sha256"] and ob == rb
        cls = "BYTE_IDENTICAL" if byte_id else "UNCLASSIFIED_NEEDS_REVIEW"
        rows.append({"output_id": m["output_id"], "filename": fn, "stage": stage, "official_sha256": m["historical_sha256"],
                     "repro_sha256": h, "byte_identical": byte_id, "official_bytes": len(ob), "repro_bytes": len(rb),
                     **{k: res[k] for k in ("rows_official", "rows_repro", "schema_equal", "sort_order_equal",
                                             "key_columns", "key_membership_equal", "numeric_cells_differing",
                                             "numeric_max_abs_diff", "text_cells_differing")},
                     "classification": cls, "repro_path": str(rp)})
    # non-pinned side files (informational)
    seen_dirs = {}
    for m in csv.DictReader(man.open(encoding="utf-8")):
        rel_dir = Path(m["historical_path"].split("20260911_AI_DECISION_V5_PRODUCTION\\", 1)[1]).parent
        seen_dirs[rel_dir] = latest(run, m["producer_stage"])
    pinned = {r["filename"] for r in rows}
    for rel_dir, rdir in seen_dirs.items():
        for op in sorted((inp / "V5" / rel_dir).iterdir()):
            if op.name in pinned:
                continue
            rp = rdir / op.name
            rb = rp.read_bytes() if rp.exists() else b""
            extra.append({"file": f"{rel_dir}\\{op.name}", "official_sha256": sha(op.read_bytes()),
                          "repro_sha256": sha(rb) if rp.exists() else "MISSING", "byte_identical": rp.exists() and op.read_bytes() == rb})
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    n = sum(r["byte_identical"] for r in rows)
    summary = {"official_outputs": len(rows), "byte_identical": n, "non_pinned_side_files": extra,
               "BASELINE_REPRODUCTION": "PASS" if n == 13 and len(rows) == 13 else "FAIL"}
    out_json.write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "non_pinned_side_files"}))
    for e in extra:
        print(("SAME " if e["byte_identical"] else "DIFF ") + e["file"])


if __name__ == "__main__":
    main()
