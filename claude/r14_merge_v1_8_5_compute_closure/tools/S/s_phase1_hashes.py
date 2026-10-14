"""Write 45_PROPAGATION_RULE_HASHES.csv. Usage: python -I s_phase1_hashes.py <rpt_dir> <inputs_dir> <out_csv>"""
import csv
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    rpt, inp, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    fz = r"V5\09_ANALYTICAL_FREEZE\analytical_freeze_v2_20260918T132206Z"
    items = [
        ("LABEL_INPUT_RECONCILED", inp / r"V9\HUMAN_RECONCILED_20.csv"),
        ("LABEL_INPUT_FIRST_CODER", inp / r"V9\FIRST_CODER_50_FINAL_FROZEN.csv"),
        ("LABEL_VERIFICATION_EVENTS", inp / r"V9\HUMAN_RECONCILIATION_EVENTS.jsonl"),
        ("GENESIS_INPUT_QUEUE", inp / r"V9\HUMAN_DISAGREEMENT_QUEUE_20.csv"),
        ("GENESIS_INPUT_BLIND", inp / r"V9\BLIND_REPEAT_20_FINAL_FROZEN.csv"),
        ("GENESIS_INPUT_BLIND_MANIFEST", inp / r"V9\SECOND_CODER_BLIND_20_MANIFEST.csv"),
        ("TRANSLATION_REFERENCE_CODE", inp / r"SIDECAR\prepare_and_run_corrected_sidecar.py"),
        ("TRANSLATION_POLICY_TEXT", inp / r"SIDECAR\LOCAL_HUMAN_CORRECTION_POLICY.md"),
        ("TRANSLATION_CROSSCHECK_MAP", inp / r"SIDECAR\HUMAN_AUDIT_LOCAL_CORRECTION_MAP.csv"),
        ("TAXONOMY_SOURCE", inp / r"V5\10_DOCUMENT_DEDUP_MATRIX\matrix_v1_20260918T132505Z\DOCUMENT_DEDUP_MATRIX_CANONICAL.json"),
        ("V5_FREEZE_RECORD_LEVEL", inp / fz / "ANALYTICAL_FREEZE_RECORD_LEVEL.csv"),
        ("V5_FREEZE_PAIR_ELIGIBLE", inp / fz / "ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv"),
        ("V5_FREEZE_CANONICAL", inp / fz / "ANALYTICAL_FREEZE_CANONICAL.json"),
        ("V5_FREEZE_MANIFEST", inp / fz / "ANALYTICAL_FREEZE_MANIFEST_V2.json"),
        ("V5_FREEZE_SIDE_LEVEL", inp / fz / "ANALYTICAL_FREEZE_SIDE_LEVEL.csv"),
        ("V5_STAGE10_CODE", inp / r"V5\work\stage2_strict_v102\DOCUMENT_DEDUP_10X12_MATRIX_ACCEPTED.py"),
        ("PREREGISTRATION_DOC_43", rpt / "43_PROPAGATION_RULE_PREREGISTRATION.md"),
        ("RECORD_MANIFEST_44", rpt / "44_PROPAGATION_RECORD_MANIFEST.csv"),
        ("APPLIER_CODE", rpt / r"tools\S\s_apply_propagation.py"),
        ("MANIFEST_BUILDER_CODE", rpt / r"tools\S\s_phase1_propagation_manifest.py"),
        ("MANIFEST_BUILDER_CHECKS", rpt / r"tools\S\phase1_checks.json"),
        ("INPUT_COPY_SCRIPT", rpt / r"tools\S\s_copy_inputs.py"),
        ("INPUT_COPY_MANIFEST", inp / "INPUT_COPY_MANIFEST.csv"),
    ]
    rows = [{"item": k, "path": str(p), "bytes": p.stat().st_size, "sha256": sha(p)} for k, p in items]
    rows.append({"item": "FREEZE_TIMESTAMP_UTC", "path": "", "bytes": "",
                 "sha256": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
    rows.append({"item": "INTENDED_OUTPUT_DIR", "bytes": "", "sha256": "",
                 "path": r"C:\NTUST_PAPER\outputs\00_CURRENT\06_COMPUTE_CLOSURE_V1_8_5\compute_closure\revised_audited_label_analysis\<UTC timestamp>\ (new dated subdir; not created in Phase 1-3)"})
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["item", "path", "bytes", "sha256"], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"rows={len(rows)}")


if __name__ == "__main__":
    main()
