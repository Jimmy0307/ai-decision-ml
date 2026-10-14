"""V1.8.3 sub-agent Q: descriptive evidence for full-reanalysis feasibility.

Read-only. Hashes files and counts rows; never executes pipeline code.
Usage: python -I feasibility_evidence.py OUT_JSON
"""
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\NTUST_PAPER")
V5 = ROOT / r"outputs\10_CANONICAL_EVIDENCE\04_V5_PRODUCTION_FREEZE\20260911_AI_DECISION_V5_PRODUCTION"
FREEZE = ROOT / r"FREEZE\AI_DECISION_V9_SUBMISSION_FREEZE_20260923"
SIDECAR = ROOT / r"outputs\10_CANONICAL_EVIDENCE\01_V9_HUMAN_VALIDATION\20261003_V9_HUMAN_AUDIT_FINAL_CONVERGENCE_SIDECAR_20261003T192417"
V9 = ROOT / r"outputs\10_CANONICAL_EVIDENCE\03_R14_STUDY1\01_SOURCE_CLOSURE_V1_8\02_V9_HUMAN_VALIDATION\20260929_V9_HUMAN_VALIDATION"
REPO = ROOT / r"outputs\00_CURRENT\02_STUDY1_FREEZE\02_STUDY1_FREEZE_V1_8_1\repo"
CODE = "work/stage2_strict_v102"

# 13 hash-pinned official outputs (sidecar BASELINE_REPRODUCTION_VERIFICATION.md / 07 section 5)
OFFICIAL_13 = {
    "10_DOCUMENT_DEDUP_MATRIX/matrix_v1_20260918T132505Z/DOCUMENT_DEDUP_MATRIX_CANONICAL.json": "d816f34aef49b893ab7583662ac2db65640ea4cf2916fca583b1350aa04371b5",
    "10_DOCUMENT_DEDUP_MATRIX/matrix_v1_20260918T132505Z/DOCUMENT_PAIR_EDGES_DEDUP.csv": "3ba370c1804960ed35880f87172114e2c14af98e2691848f6306f5fe5b1715a2",
    "10_DOCUMENT_DEDUP_MATRIX/matrix_v1_20260918T132505Z/MATRIX_DOCUMENT_DEDUP_COUNTS_10X12.csv": "ebac2b6615d037ffea541d34a180c17677343237e7dd395db1278f9aba69ec46",
    "10_DOCUMENT_DEDUP_MATRIX/matrix_v1_20260918T132505Z/MATRIX_RAW_RECORD_COUNTS_10X12.csv": "e5883e510a00ceee57bba141777ef9a59b1abe41d7f8a56caaaaa80a9de7a938",
    "11_NULL_MODEL_NETWORK/null_model_v1_20260918T132933Z/NULL_MODEL_NETWORK_CANONICAL.json": "682a58f71595836cf4a297357e49c863625e38424d690a298105c792fd789b66",
    "11_NULL_MODEL_NETWORK/null_model_v1_20260918T132933Z/CELL_NULL_MODEL_RESULTS_120.csv": "e7019dfe1fe594034c2783187208def545fd4432b4bb01113648e94065a34d1f",
    "12_ROBUSTNESS_SENSITIVITY/robustness_v1_20260918T133618Z/ROBUSTNESS_SENSITIVITY_CANONICAL.json": "8c0441cee3777dc9284e106579b5a1a8d9811c7aaa7c9c770ede8cb6ab639993",
    "12_ROBUSTNESS_SENSITIVITY/robustness_v1_20260918T133618Z/EXACT_HYPERGEOMETRIC_RESULTS_120.csv": "8538fc82447aaaed6d850954c5b1fb272a8f767183162e92a55a5327d66f2516",
    "12_ROBUSTNESS_SENSITIVITY/robustness_v1_20260918T133618Z/DOCUMENT_PRESERVING_NULL_RESULTS_120.csv": "6b7c6e2941f37a5fe6f394003a19682c39465c4b31b3323ad728fdbe57d80f0b",
    "12_ROBUSTNESS_SENSITIVITY/robustness_v1_20260918T133618Z/RAW_RECORD_EXACT_SENSITIVITY_120.csv": "12e8b7e324635fe7067ef38625d7f3b2931ad5f5a3fb23e636d481d029735051",
    "12_ROBUSTNESS_SENSITIVITY/robustness_v1_20260918T133618Z/ROBUSTNESS_COMPARISON_120.csv": "1e30bf064887950ca9eef360b3c050c8d4db2b681dd163e607901872acdbfcb5",
    "13_RESULTS_FREEZE/results_freeze_v1_20260919T080120Z/FINAL_RESULTS_FREEZE_CANONICAL.json": "b1d8b5ee325e72441fb2a4dcab24cd42137be8a9092d7796e3438ebf92dd74d0",
    "13_RESULTS_FREEZE/results_freeze_v1_20260919T080120Z/FINAL_ROBUST_CORE_32.csv": "a43b4b5897bb8b1dabfe251aa52b95da8f35b6951c98ada7c92663291770bd50",
}
STAGE_CODE = [
    "build_analytical_freeze_v2.py", "analytical_downstream_contract.py", "stage2_common.py",
    "STAGE3_RESIDUAL_CLOSURE_ACCEPTED.py", "DOCUMENT_DEDUP_10X12_MATRIX_ACCEPTED.py",
    "NULL_MODEL_NETWORK_ANALYSIS_ACCEPTED.py", "ROBUSTNESS_SENSITIVITY_ACCEPTED.py",
    "FINAL_RESULTS_FREEZE_ACCEPTED.py",
]
SIDECAR_CODE = ["prepare_and_run_corrected_sidecar.py", "run_baseline_reproduction.py",
                "continue_baseline_reproduction.py", "verify_baseline_reproduction.py"]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def read_csv(p):
    with open(p, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def freeze_root():
    rows = read_csv(FREEZE / "00_README_AND_MANIFEST" / "SHA256SUMS.csv")
    expected = (FREEZE / "FREEZE_ROOT_SHA256.txt").read_text(encoding="utf-8-sig").strip().lower()
    ordered = sorted(rows, key=lambda r: r["relative_path"])
    variants = {}
    for name, rs in (("file_order", rows), ("sorted", ordered)):
        for sep in ("\n", "\r\n"):
            for fmt in ("{p},{h}", "{p}  {h}", "{p} {h}", "{p}\t{h}", "{h}  {p}", "{p}{h}"):
                body = sep.join(fmt.format(p=r["relative_path"], h=r["sha256"]) for r in rs)
                for tail in ("", sep):
                    key = f"{name}|{fmt}|{sep!r}|tail={bool(tail)}"
                    variants[key] = hashlib.sha256((body + tail).encode("utf-8")).hexdigest()
    hit = [k for k, v in variants.items() if v == expected]
    return {"rows": len(rows), "expected_root": expected, "matching_variants": hit}, {r["relative_path"]: r for r in rows}


def freeze_targets(sums):
    out = []
    keys = [k for k in sums if (k.startswith("02_SOURCE_CORPUS_LINEAGE/V5_PRODUCTION/" + CODE + "/") and k.endswith(".py")
                                and "/" not in k[len("02_SOURCE_CORPUS_LINEAGE/V5_PRODUCTION/" + CODE + "/"):])]
    named = ("SHA256SUMS.csv", "FREEZE_ROOT_SHA256.txt", "workbench.sqlite", "HUMAN_VALIDATION_400.csv",
             "SECOND_CODER_120.csv", "V9_CONFERENCE_CAMERA_READY_FULL_CHINESE_BODY_20260921.pdf",
             "V9_CONFERENCE_CAMERA_READY_FULL_CHINESE_BODY_20260921.docx", "FSC_STAGE2_RESULTS_v1_0_2.sqlite",
             "ANALYTICAL_FREEZE_CANONICAL.json", "FINAL_ROBUST_CORE_32.csv")
    keys += [k for k in sums if k.rsplit("/", 1)[-1] in named]
    for k in sorted(set(keys)):
        p = FREEZE / k
        actual = sha(p) if p.exists() else None
        out.append({"path": k, "manifest_sha256": sums[k]["sha256"], "actual_sha256": actual,
                    "match": actual == sums[k]["sha256"]})
    return out


def code_table():
    rows = []
    for n in STAGE_CODE:
        rec = {"script": n}
        for label, base in (("v5", V5), ("freeze", FREEZE / "02_SOURCE_CORPUS_LINEAGE" / "V5_PRODUCTION"),
                            ("sidecar_v5_production", SIDECAR / "V5_PRODUCTION"),
                            ("sidecar_v5_corrected", SIDECAR / "V5_CORRECTED")):
            p = base / CODE / n
            rec[label] = sha(p) if p.exists() else None
        rows.append(rec)
    for n in SIDECAR_CODE:
        rows.append({"script": n, "sidecar_root": sha(SIDECAR / n)})
    return rows


def official_13():
    return [{"path": k, "pinned": v, "actual": sha(V5 / k), "match": sha(V5 / k) == v} for k, v in OFFICIAL_13.items()]


def correction_map():
    rows = read_csv(SIDECAR / "HUMAN_AUDIT_LOCAL_CORRECTION_MAP.csv")
    actions = Counter(r["action"] for r in rows)
    sources = Counter(r["label_source"] for r in rows)
    before = sum(r["baseline_eligible"] == "True" for r in rows)
    after = sum(r["sidecar_eligible"] == "True" for r in rows)
    by_c5 = Counter((r["human_C5"].strip().upper(), r["human_C1"].strip().upper(), r["action"]) for r in rows)
    return {"rows": len(rows), "actions": dict(actions), "label_sources": dict(sources),
            "eligible_before_in_50": before, "eligible_after_in_50": after, "delta": after - before,
            "c5_c1_action": {"|".join(k): v for k, v in sorted(by_c5.items())}}


def core_set(p, key_ai="ai_family", key_d="decision_family"):
    return {(r[key_ai], r[key_d], r["direction"]) for r in read_csv(p)}


def sidecar_core_check():
    core_file = SIDECAR / r"V5_CORRECTED\13_RESULTS_FREEZE\results_freeze_v1_20261003T115651Z\FINAL_ROBUST_CORE_32.csv"
    sidecar = core_set(core_file)
    sens = read_csv(V9 / "ROBUST_CORE_LOCAL_SENSITIVITY.csv")
    sens_core = {(r["ai_family"], r["decision_family"], r["sidecar_core_direction"]) for r in sens
                 if r["sidecar_core_member"] == "YES"}
    official = core_set(V5 / OFFICIAL_ROOT_CORE)
    dirs = Counter(d for _, _, d in sidecar)
    return {"sidecar_core_sha256": sha(core_file), "sidecar_core_n": len(sidecar),
            "sidecar_direction_counts": dict(dirs),
            "sensitivity_csv_sidecar_core_n": len(sens_core), "sets_equal": sidecar == sens_core,
            "gained_vs_official": sorted(map(list, sidecar - official)),
            "lost_vs_official": sorted(map(list, official - sidecar))}


OFFICIAL_ROOT_CORE = "13_RESULTS_FREEZE/results_freeze_v1_20260919T080120Z/FINAL_ROBUST_CORE_32.csv"


def stop_checks():
    official = core_set(V5 / OFFICIAL_ROOT_CORE)
    g = read_csv(REPO / "11_Priority_Gaps_Frozen_Export_G01_G16_v1_0_20261009.csv")
    g_set = {(r["AI_Family"], r["Decision_Family"], "DEPLETED") for r in g}
    m = json.loads((V5 / "09_ANALYTICAL_FREEZE/analytical_freeze_v2_20260918T132206Z/ANALYTICAL_FREEZE_MANIFEST_V2.json").read_text(encoding="utf-8"))
    d = json.loads((V5 / "10_DOCUMENT_DEDUP_MATRIX/matrix_v1_20260918T132505Z/DOCUMENT_DEDUP_MATRIX_MANIFEST.json").read_text(encoding="utf-8"))
    n = json.loads((V5 / "11_NULL_MODEL_NETWORK/null_model_v1_20260918T132933Z/NULL_MODEL_NETWORK_MANIFEST.json").read_text(encoding="utf-8"))
    r = json.loads((V5 / "12_ROBUSTNESS_SENSITIVITY/robustness_v1_20260918T133618Z/ROBUSTNESS_SENSITIVITY_MANIFEST.json").read_text(encoding="utf-8"))
    dirs = Counter(x for _, _, x in official)
    return {"strict_records": m["counts"]["strict_records"], "pair_eligible": m["counts"]["pair_eligible_records"],
            "eligible_docs": m["counts"]["pair_eligible_unique_documents"], "M": d["counts"]["document_dedup_edges_M"],
            "cells": n["observed_network"]["cells"], "main_q05": n["significance"]["q05_cells"],
            "main_seed": n["null_model"]["seed"], "main_reps": n["null_model"]["replicates"],
            "doc_null_reps": r["document_null_diagnostics"]["replicates"],
            "core_n": len(official), "core_dirs": dict(dirs), "g_n": len(g_set),
            "g_subset_of_core_depleted": g_set <= official}


def main(out):
    root, sums = freeze_root()
    res = {"freeze_root": root, "freeze_targets": freeze_targets(sums), "code": code_table(),
           "official_13": official_13(), "correction_map": correction_map(),
           "sidecar_core": sidecar_core_check(), "stop_checks": stop_checks()}
    Path(out).write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps({k: res[k] for k in ("freeze_root", "correction_map", "sidecar_core", "stop_checks")}, indent=1))
    print("freeze_targets mismatches:", [t["path"] for t in res["freeze_targets"] if not t["match"]])
    print("official_13 mismatches:", [t["path"] for t in res["official_13"] if not t["match"]])


if __name__ == "__main__":
    main(sys.argv[1])
