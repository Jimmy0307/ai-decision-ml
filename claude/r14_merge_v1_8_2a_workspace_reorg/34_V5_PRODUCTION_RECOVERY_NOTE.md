# 34 — V5 Production Folder: Recovery Candidate for "NOT_RECOVERED" Inputs (2026-10-14)

**Status: `RECOVERY_CANDIDATE_REQUIRES_FORMAL_VERIFICATION`.**

This note records a finding. It does **not** change any frozen status in V1.8, V1.8.1 or V1.8.2. The full-reanalysis triplet, `STUDY1_EVIDENCE_FREEZE` and the 18 ledger remain as committed until a dedicated verification round re-derives them.

## Finding

During the workspace reorganization, the local folder `20260911_AI_DECISION_V5_PRODUCTION` was found. It now sits at `outputs\10_CANONICAL_EVIDENCE\04_V5_PRODUCTION_FREEZE\`, holds 1,217 files and has stages 01_FSC through 14_MANUSCRIPT_DATA_PACK. Its contents were matched by **full SHA-256** against the V9 protected baseline (`PROTECTED_ARTIFACTS_BASELINE_20261003.csv`, 36 hashed entries) and against the hashes that V1.8/V1.8.1 recorded as missing.

Script: `v5_recovery/v5_protected_match.py`. Result: `v5_recovery/V5_PROTECTED_INPUT_MATCH.csv`.

| Location of the matching file | Protected entries |
|---|---:|
| V5 production folder | **18** |
| V9 package (already in V1.8 inputs) | 10 |
| `80_HISTORY_2026\09_SEP\ROOT_CAMERA_READY_DOCX_20260921\` (V9 camera-ready docx) | 1 |
| Not found in these locations | 7 |

**Newly located in V5 production** (full-hash identical to the protected baseline):
- `FSC_STAGE2_RESULTS_v1_0_2.sqlite` (strict-record results DB)
- `FSC_V5_STAGE1_ON_V4_RECORDS.csv`
- `FSC_V5_USER_RATIFIED_DEFINITIONS.json`
- `LATEST_STAGE3_RESIDUAL_CLOSURE.txt`
- the analytical freeze v2 (`ANALYTICAL_FREEZE_CANONICAL.json`, `_MANIFEST_V2.json`, `_RECORD_LEVEL.csv`, `ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv`)
- `DOCUMENT_PAIR_EDGES_DEDUP.csv`
- `NULL_MODEL_NETWORK_CANONICAL.json`
- `ROBUSTNESS_SENSITIVITY_CANONICAL.json`
- the results freeze (`FINAL_RESULTS_FREEZE_CANONICAL.json`, `_MANIFEST.json`, `FINAL_ROBUST_CORE_32.csv`, `FINAL_ROBUST_DEPLETED.csv`, `FINAL_ROBUST_ENRICHED.csv`, `FINAL_ROBUST_STATUS_MATRIX_10X12.csv`, `MANUSCRIPT_TABLE_ROBUST_CORE.csv`)

**Official final core.** `13_RESULTS_FREEZE\results_freeze_v1_20260919T080120Z\FINAL_ROBUST_CORE_32.csv` has SHA-256 `a43b4b5897bb8b1dabfe251aa52b95da8f35b6951c98ada7c92663291770bd50`, identical to the official core that V1.8 rated PROBABLE (reproduction only) and that the 18 ledger records as NOT_RECOVERED. Identical copies also exist in both `14_MANUSCRIPT_DATA_PACK` snapshots.

**V5 Manuscript Data Pack.** `14_MANUSCRIPT_DATA_PACK\data_pack_v1_20260919T081003Z` and `data_pack_v1_20260922T010012Z` exist. V1.8.1 recorded `REAL_V5_DATA_PACK=NOT_RECOVERED`, and this folder is the candidate for it.

**Still not found in the searched locations (7):**
- `SHA256SUMS.csv`
- `FREEZE_ROOT_SHA256.txt`
- `workbench.sqlite`
- `HUMAN_VALIDATION_400.csv`
- `SECOND_CODER_120.csv`
- the V9 camera-ready PDF
- `HUMAN_AUDIT_APPEND_ONLY_LOG.csv` at its protected hash; its current hash differs, as already disclosed in V9

Not searched: `C:\NTUST_PAPER\FREEZE\`, `backup\` and other root directories.

**Sidecar core** (`4e412a07…`): not found. The sidecar generator script is also not found.

## Implications (to be decided in a dedicated round, not here)

1. **Provenance upgrades.** These require a dedicated round that also confirms each file against its stage manifest.
   - The official-core provenance could be upgraded from PROBABLE to CONFIRMED.
   - `REAL_V5_DATA_PACK` could move from NOT_RECOVERED to RECOVERED.
2. **Reanalysis feasibility.** The basis of `FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET` (12/37 protected inputs missing) may no longer hold. Most analysis-stage inputs (strict DB, analytical freeze, document edges, null model) are now local. Execution feasibility must be re-assessed against the 07 §4 gate.
   - The method status (`REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION`) is unaffected.
   - The priority before V1 is unaffected, and remains a researcher decision.
3. **Unchanged by this finding.** The V1 human construct-validation packet and S1 freeze are independent of this finding and remain valid.
