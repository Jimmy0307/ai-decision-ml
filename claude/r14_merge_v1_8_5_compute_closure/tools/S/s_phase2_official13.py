"""V1.8.5 sub-agent S, Phase 2: write 46_OFFICIAL_13_OUTPUT_MANIFEST.csv from the WORK copies.

Usage: python -I s_phase2_official13.py <inputs_dir> <out_csv>
The list of 13 is taken from the authorities named in the `authority` column (not guessed);
each current V5 copy is re-hashed and must equal the pinned historical sha256 (exit 2 otherwise).
"""
import csv
import hashlib
import sys
from pathlib import Path

HIST = r"C:\NTUST_PAPER\outputs\20260911_AI_DECISION_V5_PRODUCTION"
CUR = r"C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\04_V5_PRODUCTION_FREEZE\20260911_AI_DECISION_V5_PRODUCTION"
D10 = r"10_DOCUMENT_DEDUP_MATRIX\matrix_v1_20260918T132505Z"
D11 = r"11_NULL_MODEL_NETWORK\null_model_v1_20260918T132933Z"
D12 = r"12_ROBUSTNESS_SENSITIVITY\robustness_v1_20260918T133618Z"
D13 = r"13_RESULTS_FREEZE\results_freeze_v1_20260919T080120Z"
FZ = r"09_ANALYTICAL_FREEZE\analytical_freeze_v2_20260918T132206Z"
S10 = "DOCUMENT_DEDUP_10X12_MATRIX_ACCEPTED.py (a3892528ecac135839681429916d8d6607f1ef4685456d9663373b49a1175cd7)"
S11 = "NULL_MODEL_NETWORK_ANALYSIS_ACCEPTED.py (cd96c48d685fe05d23d526638bf3d0ab7201a115f3c9cab0d908277c1d0b12e3)"
S12 = "ROBUSTNESS_SENSITIVITY_ACCEPTED.py (7700d98c934db95ff28dc7aba19be1ce6558fff2957bc79bff54f63a63087c19)"
S13 = "FINAL_RESULTS_FREEZE_ACCEPTED.py (9af8c4393fec761d0104562d6de0086a4d577e395cdcb965e3f5a2d4495fc303)"
DEP10 = (f"{FZ}\\ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv (9ee5fd53); ANALYTICAL_FREEZE_RECORD_LEVEL.csv (fbb5f592); "
         "ANALYTICAL_FREEZE_SIDE_LEVEL.csv (7704e743); ANALYTICAL_FREEZE_CANONICAL.json (9a4e8fc2, sha gate); "
         "ANALYTICAL_FREEZE_MANIFEST_V2.json (69c7a7df, verdict gate)")
DEP11 = f"{D10}\\DOCUMENT_DEDUP_MATRIX_CANONICAL.json (d816f34a); DOCUMENT_DEDUP_MATRIX_MANIFEST.json (verdict); seed 20260918, N_NULL 10000"
DEP12 = (f"{D10}\\DOCUMENT_DEDUP_MATRIX_CANONICAL.json (d816f34a), DOCUMENT_DEDUP_MATRIX_MANIFEST.json, MATRIX_RAW_RECORD_COUNTS_10X12.csv (e5883e51); "
         f"{D11}\\NULL_MODEL_NETWORK_CANONICAL.json (682a58f7), NULL_MODEL_NETWORK_MANIFEST.json, CELL_NULL_MODEL_RESULTS_120.csv (e7019dfe); "
         "document-null seed 20260919, 5000 replicates")
DEP13 = (f"{D12}\\ROBUSTNESS_SENSITIVITY_CANONICAL.json (8c0441ce), ROBUSTNESS_SENSITIVITY_MANIFEST.json, STRUCTURALLY_ROBUST_CELLS.csv, "
         f"FULL_SENSITIVITY_ROBUST_CELLS.csv, ROBUSTNESS_COMPARISON_120.csv (1e30bf06); {D11}\\NULL_MODEL_NETWORK_CANONICAL.json (682a58f7), "
         "NULL_MODEL_NETWORK_MANIFEST.json, CELL_NULL_MODEL_RESULTS_120.csv (e7019dfe)")
AUTH = ("SIDECAR\\BASELINE_REPRODUCTION_VERIFICATION.md L{md}; SIDECAR\\verify_baseline_reproduction.py L{vb}; "
        "SIDECAR\\prepare_and_run_corrected_sidecar.py L{pg} (EXPECTED_OFFICIAL_HASHES); "
        "V9\\ROBUST_CORE_LOCAL_SENSITIVITY.md L9 (count '13 hash-pinned official outputs'); "
        "REPO claude\\r14_merge_v1_8_3_v5_recovery\\38_FULL_REANALYSIS_FEASIBILITY.md L150-153; 39 L146-149")
OUT = [
    ("OFF13-01", "matrix canonical", D10, "DOCUMENT_DEDUP_MATRIX_CANONICAL.json", "d816f34aef49b893ab7583662ac2db65640ea4cf2916fca583b1350aa04371b5", S10, "10", DEP10, 9, 23, 37, "; V5 10 manifest lineage.dedup_canonical_sha256"),
    ("OFF13-02", "dedup edges", D10, "DOCUMENT_PAIR_EDGES_DEDUP.csv", "3ba370c1804960ed35880f87172114e2c14af98e2691848f6306f5fe5b1715a2", S10, "10", DEP10, 10, 24, 38, ""),
    ("OFF13-03", "document count matrix", D10, "MATRIX_DOCUMENT_DEDUP_COUNTS_10X12.csv", "ebac2b6615d037ffea541d34a180c17677343237e7dd395db1278f9aba69ec46", S10, "10", DEP10, 11, 25, 39, ""),
    ("OFF13-04", "raw count matrix", D10, "MATRIX_RAW_RECORD_COUNTS_10X12.csv", "e5883e510a00ceee57bba141777ef9a59b1abe41d7f8a56caaaaa80a9de7a938", S10, "10", DEP10, 12, 26, 40, ""),
    ("OFF13-05", "null canonical", D11, "NULL_MODEL_NETWORK_CANONICAL.json", "682a58f71595836cf4a297357e49c863625e38424d690a298105c792fd789b66", S11, "11", DEP11, 13, 27, 41, "; V5 11 manifest lineage.null_model_sha256"),
    ("OFF13-06", "main null 120", D11, "CELL_NULL_MODEL_RESULTS_120.csv", "e7019dfe1fe594034c2783187208def545fd4432b4bb01113648e94065a34d1f", S11, "11", DEP11, 14, 28, 42, ""),
    ("OFF13-07", "robustness canonical", D12, "ROBUSTNESS_SENSITIVITY_CANONICAL.json", "8c0441cee3777dc9284e106579b5a1a8d9811c7aaa7c9c770ede8cb6ab639993", S12, "12", DEP12, 15, 29, 43, "; V5 12 manifest robustness_sha256"),
    ("OFF13-08", "exact 120", D12, "EXACT_HYPERGEOMETRIC_RESULTS_120.csv", "8538fc82447aaaed6d850954c5b1fb272a8f767183162e92a55a5327d66f2516", S12, "12", DEP12, 16, 30, 44, ""),
    ("OFF13-09", "document null 120", D12, "DOCUMENT_PRESERVING_NULL_RESULTS_120.csv", "6b7c6e2941f37a5fe6f394003a19682c39465c4b31b3323ad728fdbe57d80f0b", S12, "12", DEP12, 17, 31, 45, ""),
    ("OFF13-10", "raw-record exact 120", D12, "RAW_RECORD_EXACT_SENSITIVITY_120.csv", "12e8b7e324635fe7067ef38625d7f3b2931ad5f5a3fb23e636d481d029735051", S12, "12", DEP12, 18, 32, 46, ""),
    ("OFF13-11", "comparison 120", D12, "ROBUSTNESS_COMPARISON_120.csv", "1e30bf064887950ca9eef360b3c050c8d4db2b681dd163e607901872acdbfcb5", S12, "12", DEP12, 19, 33, 47, ""),
    ("OFF13-12", "results canonical", D13, "FINAL_RESULTS_FREEZE_CANONICAL.json", "b1d8b5ee325e72441fb2a4dcab24cd42137be8a9092d7796e3438ebf92dd74d0", S13, "13", DEP13, 20, 34, 48, "; V5 13 manifest results_freeze_sha256"),
    ("OFF13-13", "official final core", D13, "FINAL_ROBUST_CORE_32.csv", "a43b4b5897bb8b1dabfe251aa52b95da8f35b6951c98ada7c92663291770bd50", S13, "13", DEP13, 21, 35, 49, "; V5 13 FINAL_RESULTS_FREEZE_MANIFEST.json"),
]


def main():
    inp, out = Path(sys.argv[1]), Path(sys.argv[2])
    rows, bad = [], 0
    for oid, label, d, fn, pin, scr, stg, dep, md, vb, pg, extra in OUT:
        cur = Path(CUR) / d / fn
        cp = inp / "V5" / d / fn
        h = hashlib.sha256(cp.read_bytes()).hexdigest()
        bad += h != pin
        rows.append({"output_id": oid, "label": label, "filename": fn, "historical_path": f"{HIST}\\{d}\\{fn}",
                     "current_source_path": str(cur), "historical_sha256": pin, "current_copy_sha256": h,
                     "current_matches_pin": h == pin, "producer_script": f"V5\\work\\stage2_strict_v102\\{scr}",
                     "producer_stage": stg, "dependency_inputs": dep,
                     "authority": AUTH.format(md=md, vb=vb, pg=pg) + extra})
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"rows={len(rows)} pin_mismatches={bad}")
    if bad or len(rows) != 13:
        sys.exit(2)


if __name__ == "__main__":
    main()
