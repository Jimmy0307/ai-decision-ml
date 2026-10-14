"""V1.8.5 sub-agent S: copy every read-only input into WORK and verify copy hash == source hash.

Usage: python -I s_copy_inputs.py <dest_dir>
Writes <dest_dir>/INPUT_COPY_MANIFEST.csv (role, source, copy, bytes, source_sha256, copy_sha256, match).
Never writes into any source tree. Exits 2 on any mismatch or if dest already exists.
"""
import csv
import hashlib
import shutil
import sys
from pathlib import Path

V5 = Path(r"C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\04_V5_PRODUCTION_FREEZE\20260911_AI_DECISION_V5_PRODUCTION")
V9 = Path(r"C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\03_R14_STUDY1\01_SOURCE_CLOSURE_V1_8\02_V9_HUMAN_VALIDATION\20260929_V9_HUMAN_VALIDATION")
SIDECAR = Path(r"C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\01_V9_HUMAN_VALIDATION\20261003_V9_HUMAN_AUDIT_FINAL_CONVERGENCE_SIDECAR_20261003T192417")
FREEZE = Path(r"C:\NTUST_PAPER\FREEZE\AI_DECISION_V9_SUBMISSION_FREEZE_20260923")

V9_FILES = [
    "FIRST_CODER_50_FINAL_FROZEN.csv", "FIRST_CODER_50_FROZEN.csv", "HUMAN_RECONCILED_20.csv",
    "HUMAN_RECONCILIATION_EVENTS.jsonl", "BLIND_REPEAT_20_FINAL_FROZEN.csv", "HUMAN_DISAGREEMENT_QUEUE_20.csv",
    "SECOND_CODER_BLIND_20_MANIFEST.csv", "MODEL_FAMILY_CODEBOOK_CROSSWALK.csv", "FINAL_STATUS.json",
    "ROBUST_CORE_LOCAL_SENSITIVITY.md", "ROBUST_CORE_LOCAL_SENSITIVITY.csv", "FINAL_ARTIFACT_HASH_MANIFEST.csv",
    "REANALYSIS_CANDIDATES_FROM_HUMAN_AUDIT.csv",
    r"V9_1_SEGMENTATION_SENSITIVITY\BASELINE_REPRODUCTION_VERIFICATION.md",
    r"V9_1_SEGMENTATION_SENSITIVITY\BASELINE_SOURCE_HASHES.csv",
]
SIDECAR_FILES = [
    "prepare_and_run_corrected_sidecar.py", "run_baseline_reproduction.py", "continue_baseline_reproduction.py",
    "verify_baseline_reproduction.py", "LOCAL_HUMAN_CORRECTION_POLICY.md", "HUMAN_AUDIT_LOCAL_CORRECTION_MAP.csv",
    "LOCAL_HUMAN_CORRECTION_MANIFEST.json", "CORRECTED_SIDECAR_OUTPUTS.json", "BASELINE_REPRODUCTION_VERIFICATION.md",
    "BASELINE_REPRODUCTION_VERIFICATION.json", "BASELINE_REPRODUCTION_OUTPUTS.json", "BASELINE_REPRODUCTION_LOG.txt",
    r"V5_PRODUCTION\work\stage2_strict_v102\DOCUMENT_DEDUP_10X12_MATRIX_ACCEPTED.py",
    r"V5_PRODUCTION\work\stage2_strict_v102\NULL_MODEL_NETWORK_ANALYSIS_ACCEPTED.py",
    r"V5_PRODUCTION\work\stage2_strict_v102\ROBUSTNESS_SENSITIVITY_ACCEPTED.py",
    r"V5_PRODUCTION\work\stage2_strict_v102\FINAL_RESULTS_FREEZE_ACCEPTED.py",
]
V5_DIRS = [
    r"09_ANALYTICAL_FREEZE\analytical_freeze_v2_20260918T132206Z",
    r"10_DOCUMENT_DEDUP_MATRIX\matrix_v1_20260918T132505Z",
    r"11_NULL_MODEL_NETWORK\null_model_v1_20260918T132933Z",
    r"12_ROBUSTNESS_SENSITIVITY\robustness_v1_20260918T133618Z",
    r"13_RESULTS_FREEZE\results_freeze_v1_20260919T080120Z",
]
V5_FILES = [
    r"09_ANALYTICAL_FREEZE\LATEST_ANALYTICAL_FREEZE_V2.txt",
    r"10_DOCUMENT_DEDUP_MATRIX\LATEST_DOCUMENT_DEDUP_MATRIX.txt",
    r"11_NULL_MODEL_NETWORK\LATEST_NULL_MODEL_NETWORK.txt",
    r"12_ROBUSTNESS_SENSITIVITY\LATEST_ROBUSTNESS_SENSITIVITY.txt",
    r"13_RESULTS_FREEZE\LATEST_FINAL_RESULTS_FREEZE.txt",
] + [rf"work\stage2_strict_v102\{n}" for n in (
    "DOCUMENT_DEDUP_10X12_MATRIX_ACCEPTED.py", "NULL_MODEL_NETWORK_ANALYSIS_ACCEPTED.py",
    "ROBUSTNESS_SENSITIVITY_ACCEPTED.py", "FINAL_RESULTS_FREEZE_ACCEPTED.py", "build_analytical_freeze_v2.py",
    "analytical_downstream_contract.py", "stage2_common.py")]
FREEZE_FILES = [
    r"08_STATISTICAL_ANALYSIS\DOCUMENT_NULL_CHAIN_PARAMETERS.json",
    r"00_README_AND_MANIFEST\SHA256SUMS.csv",
]


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def plan():
    items = [("V9", V9, r) for r in V9_FILES] + [("SIDECAR", SIDECAR, r) for r in SIDECAR_FILES]
    items += [("FREEZE", FREEZE, r) for r in FREEZE_FILES] + [("V5", V5, r) for r in V5_FILES]
    for d in V5_DIRS:
        for p in sorted((V5 / d).iterdir()):
            if p.is_file():
                items.append(("V5", V5, str(p.relative_to(V5))))
    return items


def main():
    dest = Path(sys.argv[1])
    if dest.exists():
        sys.exit(f"destination exists, refusing to overwrite: {dest}")
    rows = []
    for role, root, rel in plan():
        src = root / rel
        dst = dest / role / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        s_before = sha(src)
        shutil.copyfile(src, dst)
        c = sha(dst)
        rows.append({"role": role, "source": str(src), "copy": str(dst), "bytes": dst.stat().st_size,
                     "source_sha256": s_before, "copy_sha256": c, "match": s_before == c == sha(src)})
    with (dest / "INPUT_COPY_MANIFEST.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    bad = [r for r in rows if not r["match"]]
    print(f"copied={len(rows)} mismatches={len(bad)}")
    if bad:
        sys.exit(2)


if __name__ == "__main__":
    main()
