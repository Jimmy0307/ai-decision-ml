"""Independent recomputation of the AI x Decision V9 / sidecar headline numbers.

Standard library only. Raw research archives are NOT stored in this public repo;
pass the directories where the private archives were extracted:

    python tools/review_20261117/audit_recompute.py \
        --v9-dir   <extract>/20260929_V9_HUMAN_VALIDATION \
        --gap-dir  <extract>/AI_DECISION_GAP_VALIDITY_V1 \
        --scout-dir <extract>/AI_DECISION_LIMITATION_SCOUT_V0_1 \
        --out docs/review/20261117/RECOMPUTE_RESULTS.json

Only aggregate counts are written (no evidence text, no author data).
"""
from __future__ import annotations

import argparse
import collections
import csv
import glob
import hashlib
import json
import os
import re
import sys

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))


def read_text(path: str, **kw) -> str:
    with open(path, encoding="utf-8", **kw) as f:
        return f.read()

CODER_FIELDS = [
    ("C1", "human_evidence_valid"),
    ("C2", "human_relation_type"),
    ("C3", "human_ai_family"),
    ("C4", "human_decision_family"),
    ("C5", "human_include"),
]


def cohen_kappa(a: list[str], b: list[str]) -> float:
    """Unweighted Cohen's kappa for two raters over the same items."""
    if len(a) != len(b) or not a:
        raise ValueError("ratings must be non-empty and paired")
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = collections.Counter(a), collections.Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    if pe == 1:
        return float("nan")
    return (po - pe) / (1 - pe)


def structural_core_member(row: dict, prefix: str) -> bool:
    """V9 promotion rule: q<=.05 in main, exact and document-preserving nulls,
    with the same direction across those three analyses."""
    dirs = {row[f"{prefix}_{m}_direction"] for m in ("main", "exact", "document")}
    qs_ok = all(float(row[f"{prefix}_{m}_q"]) <= 0.05 for m in ("main", "exact", "document"))
    return qs_ok and len(dirs) == 1


def read_csv(path: str) -> list[dict]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def human_reliability(v9: str) -> dict:
    first = {r["record_id"]: r for r in read_csv(os.path.join(v9, "FIRST_CODER_50_FINAL_FROZEN.csv"))}
    blind = {r["record_id"]: r for r in read_csv(os.path.join(v9, "BLIND_REPEAT_20_FINAL_FROZEN.csv"))}
    if not set(blind) <= set(first):
        raise AssertionError("blind sample is not a subset of the first-coder sample")
    ids = sorted(blind)
    dims = {}
    for code, field in CODER_FIELDS:
        a = [first[i][field] for i in ids]
        b = [blind[i][field] for i in ids]
        dims[code] = {
            "field": field,
            "n": len(ids),
            "exact_agreement": sum(x == y for x, y in zip(a, b)),
            "cohen_kappa": round(cohen_kappa(a, b), 4),
        }
    any_disagree = sum(any(first[i][f] != blind[i][f] for _, f in CODER_FIELDS) for i in ids)
    return {
        "first_coder_records": len(first),
        "blind_second_coder_records": len(blind),
        "blind_is_subset_of_first": True,
        "blind_records_with_any_disagreement": any_disagree,
        "dimensions": dims,
    }


def cell_comparison(v9: str) -> dict:
    rows = read_csv(os.path.join(v9, "ROBUST_CORE_LOCAL_SENSITIVITY.csv"))
    key = lambda r: f"{r['ai_family']} x {r['decision_family']}"
    oc = [r for r in rows if r["official_core_member"] == "YES"]
    sc = [r for r in rows if r["sidecar_core_member"] == "YES"]
    dep = [r for r in oc if r["official_core_direction"] == "DEPLETED"]
    q05 = [r for r in rows if r["official_main_q05"] == "True"]
    q01 = [r for r in rows if r["official_main_q01"] == "True"]
    return {
        "cells": len(rows),
        "ai_families": len({r["ai_family"] for r in rows}),
        "decision_families": len({r["decision_family"] for r in rows}),
        "official_observed_nonzero_cells": sum(int(r["official_observed"]) > 0 for r in rows),
        "official_zero_cells": sum(int(r["official_observed"]) == 0 for r in rows),
        "official_document_level_edges_sum": sum(int(r["official_observed"]) for r in rows),
        "official_main_q05": len(q05),
        "official_main_q05_by_direction": dict(collections.Counter(r["official_main_direction"] for r in q05)),
        "official_main_q01": len(q01),
        "official_main_q01_by_direction": dict(collections.Counter(r["official_main_direction"] for r in q01)),
        "official_exact_q05": sum(float(r["official_exact_q"]) <= 0.05 for r in rows),
        "official_document_q05": sum(float(r["official_document_q"]) <= 0.05 for r in rows),
        "official_raw_q05": sum(float(r["official_raw_q"]) <= 0.05 for r in rows),
        "official_core": len(oc),
        "official_core_by_direction": dict(collections.Counter(r["official_core_direction"] for r in oc)),
        "official_core_rule_rederived": sum(structural_core_member(r, "official") for r in rows),
        "depleted_core_observed_counts": sorted(int(r["official_observed"]) for r in dep),
        "zero_cells_inside_core": sum(int(r["official_observed"]) == 0 for r in oc),
        "sidecar_observed_nonzero_cells": sum(int(r["sidecar_observed"]) > 0 for r in rows),
        "sidecar_document_level_edges_sum": sum(int(r["sidecar_observed"]) for r in rows),
        "sidecar_main_count_changed_cells": sum(r["official_observed"] != r["sidecar_observed"] for r in rows),
        "sidecar_main_direction_changed_cells": sum(r["main_direction_changed"] == "YES" for r in rows),
        "sidecar_core": len(sc),
        "sidecar_core_by_direction": dict(collections.Counter(r["sidecar_core_direction"] for r in sc)),
        "sidecar_core_rule_rederived": sum(structural_core_member(r, "sidecar") for r in rows),
        "sidecar_core_gained": sorted(set(map(key, sc)) - set(map(key, oc))),
        "sidecar_core_lost": sorted(set(map(key, oc)) - set(map(key, sc))),
        "rule_matches_published_flags": all(
            structural_core_member(r, "official") == (r["official_core_member"] == "YES")
            and structural_core_member(r, "sidecar") == (r["sidecar_core_member"] == "YES")
            for r in rows
        ),
    }


def segmentation(v9: str) -> dict:
    rows = read_csv(os.path.join(v9, "V9_1_SEGMENTATION_SENSITIVITY", "ROBUST_CORE_COMPARISON.csv"))
    t = lambda x: str(x).strip().lower() in ("true", "yes", "1")
    base = [r for r in rows if t(r["baseline_robust"])]
    dep = [r for r in base if r["baseline_robust_direction"] == "DEPLETED"]
    return {
        "baseline_core": len(base),
        "s1_core": sum(t(r["s1_robust"]) for r in rows),
        "s2_core": sum(t(r["s2_robust"]) for r in rows),
        "s1_retained_of_baseline": sum(t(r["s1_robust"]) for r in base),
        "s2_retained_of_baseline": sum(t(r["s2_robust"]) for r in base),
        "s1_retained_depleted": sum(t(r["s1_robust"]) for r in dep),
        "s2_retained_depleted": sum(t(r["s2_robust"]) for r in dep),
    }


def freeze_manifest(v9: str) -> dict:
    pat = os.path.join(v9, "V9_1_SEGMENTATION_SENSITIVITY", "_baseline_reproduction",
                       "09_ANALYTICAL_FREEZE", "*", "ANALYTICAL_FREEZE_MANIFEST_V2.json")
    files = glob.glob(pat)
    if len(files) != 1:
        raise AssertionError(f"expected one analytical-freeze manifest, found {len(files)}")
    text = read_text(files[0])
    out = {}
    for k in ("production_records", "strict_records", "strict_unique_documents",
              "fully_mapped_records", "partially_mapped_records", "fully_unresolved_records"):
        m = re.search(r'"%s"\s*:\s*(\d+)' % k, text)
        out[k] = int(m.group(1)) if m else None
    dm = glob.glob(os.path.join(v9, "V9_1_SEGMENTATION_SENSITIVITY", "_baseline_reproduction",
                                "10_DOCUMENT_DEDUP_MATRIX", "*", "DOCUMENT_DEDUP_MATRIX_MANIFEST.json"))
    m = re.search(r'"eligible_unique_documents"\s*:\s*(\d+)', read_text(dm[0]))
    out["eligible_unique_documents"] = int(m.group(1)) if m else None
    out["identity_strict_eq_mapped_partial_unresolved"] = (
        out["strict_records"] == out["fully_mapped_records"] + out["partially_mapped_records"] + out["fully_unresolved_records"])
    out["mapped_endpoints_2x_full_plus_partial"] = 2 * out["fully_mapped_records"] + out["partially_mapped_records"]
    return out


def limitation(v9: str, scout: str) -> dict:
    seg = read_csv(os.path.join(v9, "V9_1_SEGMENTATION_SENSITIVITY", "S1_SEGMENT_CORPUS.csv"))
    cand = read_csv(os.path.join(scout, "outputs", "v9_segment_candidates.csv"))
    return {
        "s1_segments": len(seg),
        "s1_document_ids": len({r["document_id"] for r in seg}),
        "s1_parent_strict_records": len({r["parent_record_id"] for r in seg}),
        "lexical_hit_segments": len(cand),
        "documents_with_hits": len({r["document_id"] for r in cand}),
        "hit_status_values": sorted({r["status"] for r in cand}),
    }


def gap_results(gap: str) -> dict:
    d = json.loads(read_text(os.path.join(gap, "outputs", "results.json")))
    return {
        "observed_edges": d["baseline_observed_edges"],
        "depleted_alt_connected": d["all_depleted_alt_connected"],
        "depleted_alt_len3": d["all_depleted_alt_len3"],
        "alt_disjoint_min_max": d["alt_disjoint_min_max"],
        "cross_component": {k: v["cross_depleted"] for k, v in d["backbone"].items()},
        "direct_bipartite_triangles": d["direct_bipartite_triangles"],
        "constraint_equals_dyadic_hhi": d["constraint_equals_dyadic_hhi"],
        "synthetic_K33_C": d["controlled_simulation"]["K3_3_triangle_free"]["C"],
        "synthetic_prism_C": d["controlled_simulation"]["triangular_prism"]["C"],
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--v9-dir", required=True)
    ap.add_argument("--gap-dir", required=True)
    ap.add_argument("--scout-dir", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    result = {
        "tool": "tools/review_20261117/audit_recompute.py",
        "inputs_sha256": {
            "ROBUST_CORE_LOCAL_SENSITIVITY.csv": sha256(os.path.join(a.v9_dir, "ROBUST_CORE_LOCAL_SENSITIVITY.csv")),
            "FIRST_CODER_50_FINAL_FROZEN.csv": sha256(os.path.join(a.v9_dir, "FIRST_CODER_50_FINAL_FROZEN.csv")),
            "BLIND_REPEAT_20_FINAL_FROZEN.csv": sha256(os.path.join(a.v9_dir, "BLIND_REPEAT_20_FINAL_FROZEN.csv")),
            "V9_1_SEGMENTATION_SENSITIVITY/ROBUST_CORE_COMPARISON.csv": sha256(os.path.join(a.v9_dir, "V9_1_SEGMENTATION_SENSITIVITY", "ROBUST_CORE_COMPARISON.csv")),
            "V9_1_SEGMENTATION_SENSITIVITY/S1_SEGMENT_CORPUS.csv": sha256(os.path.join(a.v9_dir, "V9_1_SEGMENTATION_SENSITIVITY", "S1_SEGMENT_CORPUS.csv")),
            "LIMITATION_SCOUT/outputs/v9_segment_candidates.csv": sha256(os.path.join(a.scout_dir, "outputs", "v9_segment_candidates.csv")),
            "GAP_VALIDITY/outputs/results.json": sha256(os.path.join(a.gap_dir, "outputs", "results.json")),
        },
        "funnel_machine_output": freeze_manifest(a.v9_dir),
        "cells_120": cell_comparison(a.v9_dir),
        "segmentation_s1_s2": segmentation(a.v9_dir),
        "human_reliability": human_reliability(a.v9_dir),
        "limitation_scout": limitation(a.v9_dir, a.scout_dir),
        "gap_validity_results_json": gap_results(a.gap_dir),
    }
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(json.dumps({k: v for k, v in result.items() if k != "inputs_sha256"}, ensure_ascii=False)[:2000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
