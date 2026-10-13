# V1.8 Source-Verified Evidence Closure (2026-10-14)

Status: **CANDIDATE — not FINAL, not submission-ready** (`SUBMISSION_READY=NO`; see `10_FINAL_STATUS.md`).
Base: branch `calibration/v1.1-variable-model` @ `ee750b1`. v1.7 base manuscript = `130_MERGED_MASTER_THESIS_R14_TO_ENTERPRISE_v1_7_EVIDENCE_CONVERGED_CANDIDATE.md` (sha256 `c28ecb3a315bc53e4acef63014599ba7d83ed563355532a2c57f474961295b97`, inside input package 1).

## Raw input packages (NOT tracked in git — provenance only)

| Package | Filename | Bytes | SHA-256 | Local provenance path | Zip mtime |
|---|---|---:|---|---|---|
| 01_ALL_OUTPUTS | AI_DECISION_THESIS_ALL_OUTPUTS_20261014.zip | 8,577,472 | 3af5626c038c494775033e4b74d282cec21f374210383276fef4d8ab5e2d61b2 | C:\Users\user\Downloads\ | 2026-10-14T01:46:15 |
| 02_V9_HUMAN_VALIDATION | 20260929_V9_HUMAN_VALIDATION.zip | 180,239,906 | 8f63e88e0cb8ed5f1d7081d9db613d8e4de7fea4896f1373057156500f3276ee | C:\NTUST_PAPER\outputs\ | 2026-10-04T02:09:38 |
| 03_LEGACY_FULL_SOURCE | 完整資料來源.zip | 13,143,635 | 138dbeac661fb39a0ab7f3fe84f312e332a9d8b64b5b47c399034bffd4c0d283 | C:\NTUST_PAPER\read\generated_v2\ | 2026-05-06T15:11:55 |

Classification: 01 = thesis artifact chain (r14_merge … v1_7); 02 = V9 human-validation authority package (see `02_V9_AUTHORITY_MAP.md`); 03 = `LEGACY_HISTORICAL_PROVENANCE` (earlier structural-hole study; see `05_LEGACY_SOURCE_BOUNDARY.md`). Per-file sha256 / size of all 1,295 extracted members: `01_FILE_INVENTORY.csv`. Same data machine-readable: `00_INPUT_MANIFEST.csv`, `00_INPUT_HASHES.txt`.

## Contents

| File | Phase |
|---|---|
| 00_INPUT_MANIFEST.csv, 00_INPUT_HASHES.txt, 01_FILE_INVENTORY.csv | 0–1 inventory & hashes |
| 02_V9_AUTHORITY_MAP.md | 2 authority map |
| 03_HUMAN_AUDIT_REPRODUCTION.md | 3–4 50/20/19 + kappa from raw rows |
| 04_LOCAL_SENSITIVITY_REPRODUCTION.md | 5 local robust-core sensitivity |
| 05_LEGACY_SOURCE_BOUNDARY.md | 6 legacy quarantine |
| 06_SOURCE_FLAG_CLOSURE.csv / _NOTES.md | 7 flag closure |
| 07_FULL_REANALYSIS_DECISION_MEMO.md | 8 (no reanalysis executed) |
| 08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md, 08_PATCH_LOG.md, 08b_V17_TO_V18_SEGMENT_DIFF.md | 9 manuscript v1.8 |
| 09_FINAL_GREP_REPORT.md | 10 forbidden-claim grep |
| 10_FINAL_STATUS.md | final status |
| tools/ | reproduction scripts (A authority, B kappa/counts, C sensitivity, D legacy, E flags, F patch; p01 extract/inventory; p10 grep) and their JSON outputs |

## Reproduce
Extract the three zips into `01_ALL_OUTPUTS/`, `02_V9_HUMAN_VALIDATION/`, `03_LEGACY_FULL_SOURCE/` of a workspace W (e.g. `python -I tools/p01.py <W>`, which re-hashes and re-extracts), then run each `tools/<X>/*.py` with `python -I` passing W as documented at the top of each report. Scripts contain absolute Windows paths from the original run; adjust W as needed.
