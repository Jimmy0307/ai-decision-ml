"""Write 18_STUDY1_FREEZE_HASHES.csv: SHA-256 ledger for the artifacts the Study 1 freeze depends on.

Usage: python -I freeze_hashes.py <repo_root> <W_extract_root> <out.csv>
Hashes are computed from the bytes on disk now. Upstream sources that are not available are listed with
status NOT_RECOVERED and an empty sha256 (a recorded prefix is quoted only as 'recorded_prefix').
"""
import csv
import hashlib
import os
import sys

V18 = "claude/r14_merge_v1_8_source_closure/"
V181 = "claude/r14_merge_v1_8_1_study1_freeze/"
V9 = "02_V9_HUMAN_VALIDATION/20260929_V9_HUMAN_VALIDATION/"
V17 = "01_ALL_OUTPUTS/AI_DECISION_THESIS_ALL_OUTPUTS/r14_merge_v1_7/"

REPO_ITEMS = [
    ("Study 1 evidence freeze", V181 + "17_STUDY1_EVIDENCE_FREEZE_v1.md", "CURRENT"),
    ("v1.8.1 manuscript (canonical text)", V181 + "16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.md", "CURRENT"),
    ("v1.8.1 manuscript DOCX (rendered from canonical md)", V181 + "16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.docx", "CURRENT"),
    ("v1.8.1 patch log", V181 + "16_PATCH_LOG_v1_8_1.md", "CURRENT"),
    ("Artifact 132 source closure report", V181 + "11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md", "CURRENT"),
    ("Stale status cleanup report", V181 + "12_STALE_STATUS_CLEANUP_REPORT.md", "CURRENT"),
    ("Segmentation attribution forensic", V181 + "13_SEGMENTATION_ATTRIBUTION_FORENSIC.md", "CURRENT"),
    ("G07/G15 boundary sensitivity audit", V181 + "14_G07_G15_BOUNDARY_SENSITIVITY_AUDIT.md", "CURRENT"),
    ("Reanalysis input governance", V181 + "15_REANALYSIS_INPUT_GOVERNANCE.md", "CURRENT"),
    ("Gap->mechanism matrix 132 (current CSV)", V181 + "current_artifacts/132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX_v1_8_1.csv", "CURRENT"),
    ("Gap->mechanism matrix 132 (current XLSX)", V181 + "current_artifacts/132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX_v1_8_1.xlsx", "CURRENT"),
    ("V1 protocol", V181 + "19_V1_HUMAN_CONSTRUCT_VALIDATION_PROTOCOL.md", "CURRENT"),
    ("V1 packet master", V181 + "20_V1_HUMAN_CONSTRUCT_VALIDATION_PACKET.xlsx", "CURRENT"),
    ("V1 codebook", V181 + "21_V1_HUMAN_CONSTRUCT_VALIDATION_CODEBOOK.md", "CURRENT"),
    ("V1 sealed commitment", V181 + "V1_SEALED/RESEARCHER_ASSIGNMENT_COMMITMENT.md", "CURRENT"),
    ("V1 frozen analyzer", V181 + "tools/I/v1_construct_analyzer.py", "CURRENT"),
    ("Baseline recomputation script", V181 + "tools/O/baseline_check.py", "CURRENT"),
    ("Baseline recomputation output", V181 + "tools/O/baseline_check.json", "CURRENT"),
    ("G01-G16 current table (frozen export)", "11_Priority_Gaps_Frozen_Export_G01_G16_v1_0_20261009.csv", "FROZEN_UPSTREAM_IN_REPO"),
    ("G01-G16 convergence & construct freeze", "41_G01_G16_CONVERGENCE_AND_CONSTRUCT_FREEZE_v2_1.md", "FROZEN_UPSTREAM_IN_REPO"),
    ("Enterprise model v2.2 (unchanged)", "42_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md", "FROZEN_UPSTREAM_IN_REPO"),
    ("Solver v2.2 (unchanged)", "51_enterprise_portfolio_solver_v2_2.py", "FROZEN_UPSTREAM_IN_REPO"),
    ("V1.8 manuscript", V18 + "08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md", "V1_8_AUTHORITY"),
    ("V1.8 V9 authority map", V18 + "02_V9_AUTHORITY_MAP.md", "V1_8_AUTHORITY"),
    ("V1.8 human-audit reproduction", V18 + "03_HUMAN_AUDIT_REPRODUCTION.md", "V1_8_AUTHORITY"),
    ("V1.8 local sensitivity reproduction", V18 + "04_LOCAL_SENSITIVITY_REPRODUCTION.md", "V1_8_AUTHORITY"),
    ("V1.8 legacy source boundary", V18 + "05_LEGACY_SOURCE_BOUNDARY.md", "V1_8_AUTHORITY"),
    ("V1.8 reanalysis decision memo (historical terminology)", V18 + "07_FULL_REANALYSIS_DECISION_MEMO.md", "V1_8_AUTHORITY"),
    ("V1.8 input manifest (raw zip hashes)", V18 + "00_INPUT_MANIFEST.csv", "V1_8_AUTHORITY"),
]
W_ITEMS = [
    ("V9 local sensitivity CSV", V9 + "ROBUST_CORE_LOCAL_SENSITIVITY.csv"),
    ("V9 local sensitivity DIFF CSV", V9 + "ROBUST_CORE_LOCAL_SENSITIVITY_DIFF.csv"),
    ("V9 first coder 50 frozen", V9 + "FIRST_CODER_50_FINAL_FROZEN.csv"),
    ("V9 blind second coder 20 frozen", V9 + "BLIND_REPEAT_20_FINAL_FROZEN.csv"),
    ("V9 reconciled 20", V9 + "HUMAN_RECONCILED_20.csv"),
    ("V9 reconciliation events", V9 + "HUMAN_RECONCILIATION_EVENTS.jsonl"),
    ("V9 reliability FINAL", V9 + "HUMAN_RELIABILITY_FINAL.csv"),
    ("V9 FINAL_STATUS.json", V9 + "FINAL_STATUS.json"),
    ("V9 artifact hash manifest", V9 + "FINAL_ARTIFACT_HASH_MANIFEST.csv"),
    ("V9 error taxonomy (taxonomy authority)", V9 + "FINAL_ERROR_TAXONOMY.csv"),
    ("V9.1 segmentation final report", V9 + "V9_1_SEGMENTATION_SENSITIVITY/SEGMENTATION_SENSITIVITY_FINAL_REPORT.md"),
    ("Historical 132 CSV (v1.7)", V17 + "132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX.csv"),
    ("Historical 132 XLSX (v1.7)", V17 + "132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX.xlsx"),
]
EXTERNAL = [
    ("R14 identity candidate (read by 13; external to repo)", r"C:\NTUST_PAPER\V9_FINAL_SUBMISSION_CANDIDATE_20261004.docx"),
]
NOT_RECOVERED = [
    ("Official final core file (R14/V9 freeze)", "a43b4b5897bb8b1dabfe251aa52b95da8f35b6951c98ada7c92663291770bd50",
     "PROBABLE: only a byte-identical reproduction exists inside V9.1 _baseline_reproduction; original freeze file not shipped"),
    ("r14/04_G01_G16_FROZEN.csv", "ace53a780434c309", "NOT_RECOVERED: 16-hex prefix recorded in v1.7 128; file not in any package"),
    ("R14 canonical docx r14/01_R14_..._CANONICAL.docx", "f4252f765c4294fe", "NOT_RECOVERED as named file; 13 reports a PROBABLE identity match"),
    ("Frozen strict-record database / freeze manifests (12/37 protected inputs)", "", "NOT_RECOVERED: listed in V9 PROTECTED_ARTIFACTS_BASELINE_20261003.csv"),
    ("Sidecar core file", "4e412a07af1f5c9e2f304408875fc1fc47018c9ff501a17dee437bea880e95a0", "NOT_SHIPPED: membership confirmed from sensitivity CSV"),
    ("Sidecar generator script", "", "NOT_RECOVERED"),
]


def sha(path: str) -> tuple:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest(), os.path.getsize(path)


def main() -> None:
    repo, wroot, out = sys.argv[1:4]
    rows = []
    for label, rel, layer in REPO_ITEMS:
        p = os.path.join(repo, rel)
        if os.path.isfile(p):
            d, n = sha(p)
            rows.append([label, "repo:" + rel, layer, "PRESENT", d, n, ""])
        else:
            rows.append([label, "repo:" + rel, layer, "MISSING", "", "", ""])
    for label, rel in W_ITEMS:
        p = os.path.join(wroot, rel)
        st = "PRESENT_OUTSIDE_GIT" if os.path.isfile(p) else "MISSING"
        d, n = sha(p) if os.path.isfile(p) else ("", "")
        rows.append([label, "W:" + rel, "RAW_SOURCE_NOT_IN_GIT", st, d, n, "extracted from V9/ALL_OUTPUTS zips (see V1.8 00_INPUT_MANIFEST.csv)"])
    for label, p in EXTERNAL:
        st = "PRESENT_OUTSIDE_GIT" if os.path.isfile(p) else "NOT_RECOVERED"
        d, n = sha(p) if os.path.isfile(p) else ("", "")
        rows.append([label, p, "EXTERNAL_LOCAL", st, d, n, "read-only evidence used by 13"])
    for label, prefix, note in NOT_RECOVERED:
        rows.append([label, "", "UPSTREAM_CANONICAL", "NOT_RECOVERED", "", "", f"recorded_value={prefix}; {note}" if prefix else note])
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["artifact", "path", "layer", "status", "sha256", "bytes", "note"])
        w.writerows(rows)
    print(len(rows), sum(r[3] == "MISSING" for r in rows), "missing")


if __name__ == "__main__":
    main()
