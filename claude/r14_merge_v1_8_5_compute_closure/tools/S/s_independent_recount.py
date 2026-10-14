"""Independent recount for stage-handoff guards (stdlib only; imports NO pipeline code).

Usage:
  python -I -B s_independent_recount.py freeze <freeze_dir>
  python -I -B s_independent_recount.py matrix <stage10_dir> <freeze_dir>
  python -I -B s_independent_recount.py null <stage11_dir>
  python -I -B s_independent_recount.py robust <stage12_dir>
Prints one JSON object.
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

TRUE = {"1", "true", "t", "yes", "y"}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rows(p: Path):
    with p.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def freeze(d: Path):
    rec = rows(d / "ANALYTICAL_FREEZE_RECORD_LEVEL.csv")
    eli = rows(d / "ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv")
    side = rows(d / "ANALYTICAL_FREEZE_SIDE_LEVEL.csv")
    flag = [r for r in rec if r["analytical_pair_eligible"].strip().lower() in TRUE]
    fam = lambda s: {r["final_family"].strip().upper() for r in side
                     if r["side"].strip().upper() == s and r["mapped"].strip().lower() in TRUE and r["final_family"].strip()}
    return {"canonical_sha256": sha(d / "ANALYTICAL_FREEZE_CANONICAL.json"), "record_rows": len(rec),
            "record_unique_ids": len({r["record_id"] for r in rec}), "eligible_rows_file": len(eli),
            "eligible_rows_flag": len(flag), "eligible_ids_file_eq_flag": [r["record_id"] for r in eli] == [r["record_id"] for r in flag],
            "excluded": len(rec) - len(eli), "eligible_unique_documents": len({r["document_id"].strip() for r in eli if r["document_id"].strip()}),
            "strict_unique_documents": len({r["document_id"].strip() for r in rec if r["document_id"].strip()}),
            "eligible_all_fully_mapped": all(r["mapping_completeness"].strip().upper() == "FULLY_MAPPED" for r in eli),
            "ai_families": len(fam("LEFT")), "decision_families": len(fam("RIGHT"))}


def matrix(d: Path, fz: Path):
    man = json.loads((d / "DOCUMENT_DEDUP_MATRIX_MANIFEST.json").read_text(encoding="utf-8"))
    edges = rows(d / "DOCUMENT_PAIR_EDGES_DEDUP.csv")
    eli = rows(fz / "ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv")
    recount = {(r["document_id"].strip(), r["left_final_family"].strip().upper(), r["right_final_family"].strip().upper()) for r in eli}
    edge_keys = {(e["document_id"], e["ai_family"], e["decision_family"]) for e in edges}
    raw = rows(d / "MATRIX_RAW_RECORD_COUNTS_10X12.csv")
    raw_total = int([r for r in raw if r["AI_FAMILY"] == "COLUMN_TOTAL"][0]["ROW_TOTAL"])
    return {"canonical_sha256": sha(d / "DOCUMENT_DEDUP_MATRIX_CANONICAL.json"),
            "manifest_dedup_canonical_sha256": man["lineage"]["dedup_canonical_sha256"], "manifest_verdict": man["verdict"],
            "edges_file_rows": len(edges), "edges_recount_from_freeze": len(recount), "edge_set_equal": edge_keys == recount,
            "manifest_M": man["counts"]["document_dedup_edges_M"], "raw_matrix_total": raw_total,
            "manifest_raw_M": man["counts"]["pair_eligible_records_before_dedup"], "raw_recount_from_freeze": len(eli),
            "edge_unique_documents": len({e["document_id"] for e in edges}),
            "manifest_eligible_unique_documents": man["counts"]["eligible_unique_documents"],
            "sum_source_record_count": sum(int(e["source_record_count"]) for e in edges)}


def null(d: Path):
    man = json.loads((d / "NULL_MODEL_NETWORK_MANIFEST.json").read_text(encoding="utf-8"))
    res = rows(d / "CELL_NULL_MODEL_RESULTS_120.csv")
    return {"canonical_sha256": sha(d / "NULL_MODEL_NETWORK_CANONICAL.json"), "manifest_null_model_sha256": man["lineage"]["null_model_sha256"],
            "manifest_verdict": man["verdict"], "rows": len(res), "unique_cells": len({(r["ai_family"], r["decision_family"]) for r in res})}


def robust(d: Path):
    man = json.loads((d / "ROBUSTNESS_SENSITIVITY_MANIFEST.json").read_text(encoding="utf-8"))
    cmp_ = rows(d / "ROBUSTNESS_COMPARISON_120.csv")
    return {"canonical_sha256": sha(d / "ROBUSTNESS_SENSITIVITY_CANONICAL.json"), "manifest_robustness_sha256": man["lineage"]["robustness_sha256"],
            "manifest_null_sha256": man["lineage"]["null_sha256"], "manifest_verdict": man["verdict"], "comparison_rows": len(cmp_)}


if __name__ == "__main__":
    mode = sys.argv[1]
    a = [Path(x) for x in sys.argv[2:]]
    out = {"freeze": freeze, "matrix": matrix, "null": null, "robust": robust}[mode](*a)
    print(json.dumps(out))
