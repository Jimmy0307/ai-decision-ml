# 37 — Protected Input Recovery (V1.8.3, sub-agent Q, Task 1)

Date: 2026-10-14. Mode: read-only search and hashing. No frozen status was changed, and no pipeline code was executed. Row-level results are in `37_PROTECTED_INPUT_RECOVERY.csv` (sha256 `7b9723f7776fc1c31f43b9c91730b80b11fb0865a48a7af72912ad04ca4dc653`; 37 baseline rows plus 1 supplementary row, S1, for the sidecar core).

**Result: all 37/37 protected baseline rows are CONFIRMED.**
- 36 rows match as whole files by full SHA-256.
- 1 row (`HUMAN_AUDIT_APPEND_ONLY_LOG.csv`) matches as a byte-exact 355-byte prefix of the current log. That is also a full SHA-256 match.
- The sidecar core `4e412a07…` (S1) is also CONFIRMED.
- PROBABLE: 0. NOT_RECOVERED: 0. No STOP condition was triggered.

## 1. Baseline and the "37th entry"

- **Baseline file.** `W\02_V9_HUMAN_VALIDATION\20260929_V9_HUMAN_VALIDATION\PROTECTED_ARTIFACTS_BASELINE_20261003.csv` has **37 rows. Every row has a sha256 and a byte size.**
- **Why there are only 36 distinct hashes.** Two rows share sha256 `8b1bc2cc…`:
  - row 3, `…/20260920_V5_METHOD_HARDENING/04_HUMAN_VALIDATION/SAMPLING_MANIFEST.md`;
  - row 35, `…/20260929_V9_HUMAN_VALIDATION/SAMPLING_MANIFEST_SOURCE.md`.
  So V1.8.2a's `V5_PROTECTED_INPUT_MATCH.csv` lists 36 hashed baseline entries. Its 37th line is not a baseline row: it is the V9 sidecar core (`4e412a07…`), which is pinned in V9 `FINAL_STATUS.json` and has no path. Here that line is reported as supplementary row S1.
- **The 12 rows V1.8 recorded as NOT_RECOVERED** (`02_V9_AUTHORITY_MAP.md` §5 item 10, which counts the FSC stage files as 4):
  - `HUMAN_VALIDATION_400.csv`, `SECOND_CODER_120.csv`, `workbench.sqlite`;
  - `FSC_V5_STAGE1_ON_V4_RECORDS.csv`, `FSC_V5_USER_RATIFIED_DEFINITIONS.json`, `FSC_STAGE2_RESULTS_v1_0_2.sqlite`, `LATEST_STAGE3_RESIDUAL_CLOSURE.txt`;
  - `FINAL_RESULTS_FREEZE_MANIFEST.json`, `FREEZE_ROOT_SHA256.txt`, the V9 camera-ready docx, the V9 camera-ready PDF, `SHA256SUMS.csv`.
- **How the 37 rows add up in V1.8.** 11 in-package rows (10 MATCH and 1 MISMATCH) + 14 external rows with identical copies + 12 absent = 37.

## 2. Method

- **Script.** `tools\Q\protected_input_search.py` (sha256 `f37922430f3bf876e1eb568a7c5f3ec6dafd25d182171be2cce5ba78b83e2bae`). Its output is `tools\Q\search_result.json`.
- **Scope.**
  - The whole `C:\NTUST_PAPER` tree: 391,988 files and 293 `.zip` archives holding 252,605 members. 0 read errors.
  - `C:\Users\user\Downloads`, matched by basename only.
- **Candidate selection.** A file is a candidate if its basename matches a baseline basename (case-insensitive), or its byte size exactly equals a baseline size. Files with "sidecar" or "robust_core" in a `.csv` name are also candidates, for the S1 hash.
- **Hashing.** 673 candidates were hashed with full SHA-256. Zip members were hashed in memory and never extracted.
- **Classification.**
  - **CONFIRMED** = full SHA-256 equality.
  - For the append-only log, the first `bytes` = 355 bytes of each name candidate were hashed as well. This is the protected size taken from the baseline.

## 3. The 7 entries V1.8.2a did not find — all CONFIRMED

| # | Protected entry | sha256 (prefix) | Primary path (full-hash match) | Identical copies |
|---|---|---|---|---:|
| 37 | `SHA256SUMS.csv` | `a63a9d8e` | `C:\NTUST_PAPER\FREEZE\AI_DECISION_V9_SUBMISSION_FREEZE_20260923\00_README_AND_MANIFEST\SHA256SUMS.csv` | 1 |
| 33 | V9 camera-ready PDF | `75db5775` | `C:\NTUST_PAPER\FREEZE\AI_DECISION_V9_SUBMISSION_FREEZE_20260923\01_MANUSCRIPT\V9_CONFERENCE_CAMERA_READY_FULL_CHINESE_BODY_20260921.pdf` | 2 (+ `C:\Users\user\Downloads\`) |
| 31 | `FREEZE_ROOT_SHA256.txt` | `ca85a7e4` | `C:\NTUST_PAPER\FREEZE\AI_DECISION_V9_SUBMISSION_FREEZE_20260923\FREEZE_ROOT_SHA256.txt` | 1 |
| 4 | `workbench.sqlite` (521,801,728 B) | `367e588c` | `C:\NTUST_PAPER\LocalCorpusWorkbench\v5_production_app\data\workbench.sqlite` (the original lineage path) | 2 (+ `FREEZE\…\02_SOURCE_CORPUS_LINEAGE\workbench.sqlite`) |
| 1 | `HUMAN_VALIDATION_400.csv` | `dc242f8d` | `C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\02_V5_METHOD\20260920_V5_METHOD_HARDENING\04_HUMAN_VALIDATION\HUMAN_VALIDATION_400.csv` | 5 (FREEZE ×3, plus a member of `20260920_V5_METHOD_HARDENING.zip`) |
| 2 | `SECOND_CODER_120.csv` | `cc68a1ea` | `…\02_V5_METHOD\20260920_V5_METHOD_HARDENING\04_HUMAN_VALIDATION\SECOND_CODER_120.csv` | 5 (same pattern) |
| 26 | `HUMAN_AUDIT_APPEND_ONLY_LOG.csv` at the protected hash | `c958f807` | **No standalone file.** Bytes 0–354 of the current 625-byte log `W\02_V9_HUMAN_VALIDATION\20260929_V9_HUMAN_VALIDATION\HUMAN_AUDIT_APPEND_ONLY_LOG.csv` (`151cf3d0…`) hash exactly to `c958f8072c38…eca1` | 0 files / 6 logs carrying the prefix |

### The append-only log in detail

- **Copies of the log.** All 6 copies anywhere in the tree have sha256 `151cf3d0…` and are 625 bytes:
  - the V1.8 W package;
  - `10_CANONICAL_EVIDENCE\01_V9_HUMAN_VALIDATION\20260929_V9_HUMAN_VALIDATION\` and its `.zip`;
  - 3 `80_HISTORY_2026\10_OCT\…20261003T05…` recovery/bug-repro snapshots.
- **No standalone file has the protected hash.**
- **Prefix match.** In every copy, the 355-byte prefix (the protected size) hashes to the protected value. The prefix is the header plus event 1 (`FIRST_CODER_50_FROZEN`, 2026-10-02T19:49:38Z).
- **What this means.** The protected state is byte-identical to the start of the current log. Every later byte is appended content, which is what an append-only log should show.
- **Recommendation, not applied.** This evidence would support moving V9's `LEGACY_AUDIT_LOG_INTEGRITY=UNVERIFIED` to "protected prefix verified; growth is append-only". The frozen V1.8 wording ("UNRESOLVED, not evidence of tampering") remains until the integrator adopts this.

## 4. Manifest-chain check of the FREEZE (supports rows 31, 37 and the FREEZE copies)

- **Root hash recomputed.** `FREEZE_ROOT_SHA256.txt` = `4b9180dd…ce34`. This is recomputed exactly as SHA-256 over the rows of `SHA256SUMS.csv` (35,134 rows), each written as `relative_path + sha256` and joined with `\n`, with no trailing newline. The result is the same in file order and in sorted order.
- **Chain.** FREEZE_ROOT → SHA256SUMS (`a63a9d8e`, protected) → files.
- **Targeted file verification.** 51 FREEZE files were re-hashed against `SHA256SUMS.csv` and all 51 MATCH:
  - workbench.sqlite;
  - the 400/120 samples in 3 locations;
  - the docx and PDF;
  - the stage-2 sqlite in 2 locations;
  - the analytical freeze canonical;
  - the official core;
  - all `work/stage2_strict_v102/*.py`.
  Results are in `tools\Q\feasibility_evidence.json`.
- **Not re-hashed.** The full 37.06 GB FREEZE was not re-hashed.
- **FREEZE origin.** `FREEZE_MANIFEST.json` dates the FREEZE to 2026-09-24T03:39:52+08:00 and records the same counts: 6,499 / 3,125 / 2,180 / 32 = 16+16.

## 5. Other 30 rows

- **18 V5-production rows (rows 5–21 and 36).** All are CONFIRMED in `10_CANONICAL_EVIDENCE\04_V5_PRODUCTION_FREEZE\20260911_AI_DECISION_V5_PRODUCTION\`, with 2–16 identical copies each. The copies include the FREEZE `02_SOURCE_CORPUS_LINEAGE\V5_PRODUCTION`, the two V5 data packs and the sidecar `REFERENCE_OFFICIAL`.
- **Row 3, `SAMPLING_MANIFEST.md`.** CONFIRMED in `02_V5_METHOD\20260920_V5_METHOD_HARDENING\04_HUMAN_VALIDATION\`, with 11 copies.
- **10 V9-package rows (rows 22–25, 27–30, 34 and 35).** All are CONFIRMED in the V9 package, with 6–11 copies each.
- **V9 camera-ready docx (row 32).** CONFIRMED in the FREEZE `01_MANUSCRIPT` folder, `80_HISTORY_2026\09_SEP\ROOT_CAMERA_READY_DOCX_20260921\` and `Downloads`.
- **Where to look.** The CSV `all_locations` column lists every copy.

## 6. Supplementary S1 — sidecar core `4e412a07…`

- **Status: CONFIRMED.** Path: `C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\01_V9_HUMAN_VALIDATION\20261003_V9_HUMAN_AUDIT_FINAL_CONVERGENCE_SIDECAR_20261003T192417\V5_CORRECTED\13_RESULTS_FREEZE\results_freeze_v1_20261003T115651Z\FINAL_ROBUST_CORE_32.csv`. There is 1 copy.
- **Contents match the sensitivity CSV.**
  - 32 cells: 15 ENRICHED, 17 DEPLETED.
  - The set equals the `sidecar_core_member=YES` set in the pinned `ROBUST_CORE_LOCAL_SENSITIVITY.csv`.
  - Gained vs official: `HUMAN_AUGMENTATION × RISK_ASSESSMENT` (DEPLETED).
  - Lost vs official: `COORDINATION_EXECUTION × GENERAL_DECISION_PROCESS` (ENRICHED).
- **Why earlier rounds missed it.** The same folder holds the sidecar generator and the propagation policy, which were previously NOT_RECOVERED (see `38` §2e–f). V1.8 searched only the extracted V9 package, and V1.8.2a searched only V5, `80_HISTORY` and the V9 package. Neither looked at `C:\NTUST_PAPER\FREEZE\` or `10_CANONICAL_EVIDENCE\01_V9_HUMAN_VALIDATION\20261003_…SIDECAR…`.

## 7. Recommended (not applied) status changes

```
PROTECTED_INPUTS_RECOVERED=37/37 (36 FULL_FILE_SHA256 + 1 FULL_SHA256_OF_355_BYTE_PREFIX)
PROTECTED_INPUTS_NOT_RECOVERED=0  (was 12/37 in V1.8 02 §5; 7 after V1.8.2a)
FREEZE_MANIFEST_CHAIN=ROOT_RECOMPUTED_MATCH; 51/51 targeted files MATCH
OFFICIAL_CORE a43b4b58…=CONFIRMED (V5 13_RESULTS_FREEZE; FREEZE 02_SOURCE_CORPUS_LINEAGE; 16 copies)
SIDECAR_CORE 4e412a07…=CONFIRMED (was NOT_SHIPPED)
LEGACY_APPEND_ONLY_LOG protected state=CONFIRMED_AS_BYTE_PREFIX of current log (recommendation only)
STOP=NONE
```
