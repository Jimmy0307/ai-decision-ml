# 22 — V1.8.1 Final Forensic Grep Report

Script: `tools/O/final_grep.py` (run with `python -I` on the working tree before commit); raw hits: `tools/O/final_grep_hits.tsv`; report generator: `tools/O/write_grep_report.py`.

Layers: **CURRENT** = new v1.8.1 artifacts (this folder, excluding tools); **CURRENT_TOOLS** = scripts/JSON in this folder's tools (contain the search patterns themselves); **HISTORICAL** = every other tracked file (V1.8 folder, earlier checkpoints, root files) — frozen by policy, not edited; their stale wording is superseded by the current copies and by 12/15/17.

## Counts by pattern and layer

| Pattern | CURRENT | CURRENT_TOOLS | HISTORICAL |
|---|---:|---:|---:|
| structural holes | 5 | 1 | 35 |
| 2026-09-29 紀錄，待核 | 35 | 39 | 296 |
| 完整資料來源.zip + V5 Data Pack (same line) | 9 | 19 | 9 |
| 84–85/120 | 16 | 23 | 7 |
| 84/120 | 24 | 24 | 2 |
| 85/120 | 22 | 22 | 2 |
| {taxblock} | 7 | 1 | 5 |
| human validation confirmed | 3 | 1 | 9 |
| V9 not available | 0 | 1 | 0 |
| V9 不在 | 0 | 1 | 0 |
| FULL_REANALYSIS_RECOMMENDED=NO | 0 | 1 | 2 |
| 32 pairs were confirmed | 0 | 1 | 4 |
| enterprise ROI demonstrated | 0 | 1 | 4 |
| V7 complete | 0 | 1 | 4 |

## Verdict

- CURRENT hits: 121; UNCLASSIFIED / substantive forbidden claims: **0**.
- In the v1.8.1 manuscript: `2026-09-29 紀錄，待核` = 0; `FULL_REANALYSIS_RECOMMENDED=NO` = 0; `{taxblock}` = 0; `V9 not available`/`V9 不在` = 0; legacy-zip/V5 co-binding = 0; `32 pairs were confirmed` = 0; `enterprise ROI demonstrated` = 0; `V7 complete` = 0. Remaining hits are negations, reference entries, or 84/85/120 values whose provenance is now tagged as V9.1.
- `FULL_REANALYSIS_RECOMMENDED=NO` survives only in HISTORICAL V1.8 files (07, 10) and is superseded by the triplet in 15/17/23.

## CURRENT hits (file, line, classification, action)

| Pattern | File | Line | Classification | Action |
|---|---|---:|---|---|
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 3 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 33 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 47 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 48 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 49 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 50 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 51 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 52 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 53 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 54 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 55 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 56 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 57 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 58 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 59 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 60 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 61 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 62 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 63 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 64 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 65 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 66 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 67 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 68 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 69 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 70 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 71 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 72 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 73 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 74 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 75 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 76 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 77 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 2026-09-29 紀錄，待核 | `11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md` | 78 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 完整資料來源.zip + V5 Data Pack (same line) | `12_STALE_STATUS_CLEANUP_REPORT.md` | 107 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 完整資料來源.zip + V5 Data Pack (same line) | `12_STALE_STATUS_CLEANUP_REPORT.md` | 118 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 完整資料來源.zip + V5 Data Pack (same line) | `12_STALE_STATUS_CLEANUP_REPORT.md` | 129 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 完整資料來源.zip + V5 Data Pack (same line) | `12_STALE_STATUS_CLEANUP_REPORT.md` | 130 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 完整資料來源.zip + V5 Data Pack (same line) | `12_STALE_STATUS_CLEANUP_REPORT.md` | 131 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 完整資料來源.zip + V5 Data Pack (same line) | `12_STALE_STATUS_CLEANUP_REPORT.md` | 147 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84–85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 1 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84–85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 36 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84–85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 53 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84–85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 62 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84–85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 63 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84–85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 64 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84–85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 71 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84–85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 182 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84–85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 186 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84–85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 189 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 4 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 14 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 25 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 36 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 51 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 60 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 67 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 68 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 69 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 79 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 81 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 82 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 83 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 91 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 93 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 103 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 155 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 181 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 4 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 14 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 25 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 36 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 52 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 60 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 67 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 68 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 69 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 80 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 81 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 91 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 93 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 138 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 155 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 181 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| {taxblock} | `15_REANALYSIS_INPUT_GOVERNANCE.md` | 97 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| {taxblock} | `15_REANALYSIS_INPUT_GOVERNANCE.md` | 102 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| {taxblock} | `15_REANALYSIS_INPUT_GOVERNANCE.md` | 106 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| {taxblock} | `15_REANALYSIS_INPUT_GOVERNANCE.md` | 108 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| {taxblock} | `15_REANALYSIS_INPUT_GOVERNANCE.md` | 111 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| {taxblock} | `15_REANALYSIS_INPUT_GOVERNANCE.md` | 116 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| {taxblock} | `15_REANALYSIS_INPUT_GOVERNANCE.md` | 129 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `16b_V18_TO_V181_SEGMENT_DIFF.md` | 77 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `16b_V18_TO_V181_SEGMENT_DIFF.md` | 77 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84–85/120 | `16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.md` | 2264 | NUMBER_UNCHANGED_PROVENANCE_V9_1_ATTRIBUTED (table note L1603 / L2264 tag) | provenance tag added (J22–J28) |
| 84/120 | `16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.md` | 1600 | NUMBER_UNCHANGED_PROVENANCE_V9_1_ATTRIBUTED (table note L1603 / L2264 tag) | provenance tag added (J22–J28) |
| 84/120 | `16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.md` | 1603 | NUMBER_UNCHANGED_PROVENANCE_V9_1_ATTRIBUTED (table note L1603 / L2264 tag) | provenance tag added (J22–J28) |
| 85/120 | `16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.md` | 1601 | NUMBER_UNCHANGED_PROVENANCE_V9_1_ATTRIBUTED (table note L1603 / L2264 tag) | provenance tag added (J22–J28) |
| 85/120 | `16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.md` | 1603 | NUMBER_UNCHANGED_PROVENANCE_V9_1_ATTRIBUTED (table note L1603 / L2264 tag) | provenance tag added (J22–J28) |
| human validation confirmed | `16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.md` | 29 | NEGATED (does not show that human validation confirmed) | none |
| structural holes | `16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.md` | 37 | NEGATED_THEORY_BOUNDARY (not automatically a structural hole) | none |
| structural holes | `16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.md` | 2396 | REFERENCE_LIST_ENTRY | none |
| structural holes | `16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.md` | 2436 | REFERENCE_LIST_ENTRY | none |
| structural holes | `16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.md` | 2438 | REFERENCE_LIST_ENTRY | none |
| 2026-09-29 紀錄，待核 | `16_PATCH_LOG_v1_8_1.md` | 340 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 完整資料來源.zip + V5 Data Pack (same line) | `16_PATCH_LOG_v1_8_1.md` | 365 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84–85/120 | `16_PATCH_LOG_v1_8_1.md` | 241 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84–85/120 | `16_PATCH_LOG_v1_8_1.md` | 243 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84–85/120 | `16_PATCH_LOG_v1_8_1.md` | 370 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `16_PATCH_LOG_v1_8_1.md` | 227 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `16_PATCH_LOG_v1_8_1.md` | 322 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 84/120 | `16_PATCH_LOG_v1_8_1.md` | 331 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `16_PATCH_LOG_v1_8_1.md` | 227 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `16_PATCH_LOG_v1_8_1.md` | 322 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 85/120 | `16_PATCH_LOG_v1_8_1.md` | 331 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| human validation confirmed | `17_STUDY1_EVIDENCE_FREEZE_v1.md` | 107 | INVALID_CLAIM_LIST (negated) | none |
| human validation confirmed | `17_STUDY1_EVIDENCE_FREEZE_v1.md` | 108 | INVALID_CLAIM_LIST (negated) | none |
| structural holes | `17_STUDY1_EVIDENCE_FREEZE_v1.md` | 110 | INVALID_CLAIM_LIST (negated) | none |
| 84–85/120 | `19_V1_HUMAN_CONSTRUCT_VALIDATION_PROTOCOL.md` | 291 | QUOTED_IN_AUDIT_EVIDENCE | none (report quotes old wording or the search pattern itself) |
| 完整資料來源.zip + V5 Data Pack (same line) | `128_CANONICAL_STATE_v1_8_1.md` | 22 | CORRECTED_LABEL (NOT THE V5 DATA PACK; REAL_V5_DATA_PACK=NOT_RECOVERED) | none |
| 完整資料來源.zip + V5 Data Pack (same line) | `128_CANONICAL_STATE_v1_8_1.md` | 53 | CORRECTED_LABEL (NOT THE V5 DATA PACK; REAL_V5_DATA_PACK=NOT_RECOVERED) | none |
| 84–85/120 | `131_HUMAN_VALIDATION_INTEGRATION_REPORT_v1_8_1.md` | 90 | PROVENANCE_ADDED_V181 (V9.1 segmentation sensitivity tag) | tag added in current copy |

## HISTORICAL hits (frozen; classification FROZEN_HISTORICAL; action: none — superseded)

| Pattern | File | Hits |
|---|---|---:|
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/06_SOURCE_FLAG_CLOSURE.csv` | 30 |
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/06_SOURCE_FLAG_CLOSURE_NOTES.md` | 6 |
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/08_PATCH_LOG.md` | 15 |
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/08b_V17_TO_V18_SEGMENT_DIFF.md` | 1 |
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/10_FINAL_STATUS.md` | 1 |
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/tools/D/legacy_audit_result.json` | 2 |
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/tools/E/dupcheck.py` | 1 |
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/tools/E/final_view.txt` | 30 |
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/tools/E/flags.csv` | 30 |
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/tools/E/flags_view.txt` | 30 |
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/tools/E/hits_raw.csv` | 68 |
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/tools/E/hits_view.txt` | 30 |
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/tools/E/v9claims.txt` | 6 |
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/tools/E/v9lines.txt` | 14 |
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/tools/F/build_log.py` | 1 |
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/tools/F/d1.txt` | 6 |
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/tools/F/d2.txt` | 8 |
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/tools/F/patch_v18.py` | 2 |
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/tools/F/patches.json` | 14 |
| 2026-09-29 紀錄，待核 | `claude/r14_merge_v1_8_source_closure/tools/F/rows.txt` | 1 |
| 32 pairs were confirmed | `claude/r14_merge_v1_8_source_closure/09_FINAL_GREP_REPORT.md` | 2 |
| 32 pairs were confirmed | `claude/r14_merge_v1_8_source_closure/tools/p10.py` | 1 |
| 32 pairs were confirmed | `claude/r14_merge_v1_8_source_closure/tools/p10hits.txt` | 1 |
| 84/120 | `claude/r14_merge_v1_8_source_closure/02_V9_AUTHORITY_MAP.md` | 1 |
| 84/120 | `claude/r14_merge_v1_8_source_closure/08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md` | 1 |
| 84–85/120 | `claude/r14_merge_v1_8_source_closure/02_V9_AUTHORITY_MAP.md` | 1 |
| 84–85/120 | `claude/r14_merge_v1_8_source_closure/08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md` | 1 |
| 84–85/120 | `claude/r14_merge_v1_8_source_closure/08_PATCH_LOG.md` | 1 |
| 84–85/120 | `claude/r14_merge_v1_8_source_closure/10_FINAL_STATUS.md` | 1 |
| 84–85/120 | `claude/r14_merge_v1_8_source_closure/tools/E/v9claims.txt` | 1 |
| 84–85/120 | `claude/r14_merge_v1_8_source_closure/tools/E/v9lines.txt` | 1 |
| 84–85/120 | `claude/r14_merge_v1_8_source_closure/tools/F/build_log.py` | 1 |
| 85/120 | `claude/r14_merge_v1_8_source_closure/02_V9_AUTHORITY_MAP.md` | 1 |
| 85/120 | `claude/r14_merge_v1_8_source_closure/08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md` | 1 |
| FULL_REANALYSIS_RECOMMENDED=NO | `claude/r14_merge_v1_8_source_closure/10_FINAL_STATUS.md` | 2 |
| V7 complete | `claude/r14_merge_v1_8_source_closure/09_FINAL_GREP_REPORT.md` | 2 |
| V7 complete | `claude/r14_merge_v1_8_source_closure/tools/p10.py` | 1 |
| V7 complete | `claude/r14_merge_v1_8_source_closure/tools/p10hits.txt` | 1 |
| enterprise ROI demonstrated | `claude/r14_merge_v1_8_source_closure/09_FINAL_GREP_REPORT.md` | 2 |
| enterprise ROI demonstrated | `claude/r14_merge_v1_8_source_closure/tools/p10.py` | 1 |
| enterprise ROI demonstrated | `claude/r14_merge_v1_8_source_closure/tools/p10hits.txt` | 1 |
| human validation confirmed | `claude/r14_merge_v1_8_source_closure/07_FULL_REANALYSIS_DECISION_MEMO.md` | 1 |
| human validation confirmed | `claude/r14_merge_v1_8_source_closure/08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md` | 1 |
| human validation confirmed | `claude/r14_merge_v1_8_source_closure/08_PATCH_LOG.md` | 1 |
| human validation confirmed | `claude/r14_merge_v1_8_source_closure/09_FINAL_GREP_REPORT.md` | 2 |
| human validation confirmed | `claude/r14_merge_v1_8_source_closure/tools/F/patch_v18.py` | 1 |
| human validation confirmed | `claude/r14_merge_v1_8_source_closure/tools/F/patches.json` | 1 |
| human validation confirmed | `claude/r14_merge_v1_8_source_closure/tools/p10.py` | 1 |
| human validation confirmed | `claude/r14_merge_v1_8_source_closure/tools/p10hits.txt` | 1 |
| structural holes | `20_CLAUDE_REVIEW_PACKET_GAP_TO_CONSTRUCT_MODEL_v1_1.md` | 1 |
| structural holes | `claude/r14_merge_v1_8_source_closure/05_LEGACY_SOURCE_BOUNDARY.md` | 4 |
| structural holes | `claude/r14_merge_v1_8_source_closure/08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md` | 4 |
| structural holes | `claude/r14_merge_v1_8_source_closure/09_FINAL_GREP_REPORT.md` | 6 |
| structural holes | `claude/r14_merge_v1_8_source_closure/tools/D/footer.md` | 3 |
| structural holes | `claude/r14_merge_v1_8_source_closure/tools/D/header.md` | 1 |
| structural holes | `claude/r14_merge_v1_8_source_closure/tools/D/legacy_audit.py` | 1 |
| structural holes | `claude/r14_merge_v1_8_source_closure/tools/D/legacy_audit_result.json` | 9 |
| structural holes | `claude/r14_merge_v1_8_source_closure/tools/p10.py` | 1 |
| structural holes | `claude/r14_merge_v1_8_source_closure/tools/p10hits.txt` | 5 |
| {taxblock} | `claude/r14_merge_v1_8_source_closure/02_V9_AUTHORITY_MAP.md` | 4 |
| {taxblock} | `claude/r14_merge_v1_8_source_closure/10_FINAL_STATUS.md` | 1 |
| 完整資料來源.zip + V5 Data Pack (same line) | `claude/r14_merge_v1_8_source_closure/05_LEGACY_SOURCE_BOUNDARY.md` | 1 |
| 完整資料來源.zip + V5 Data Pack (same line) | `claude/r14_merge_v1_8_source_closure/06_SOURCE_FLAG_CLOSURE.csv` | 1 |
| 完整資料來源.zip + V5 Data Pack (same line) | `claude/r14_merge_v1_8_source_closure/10_FINAL_STATUS.md` | 1 |
| 完整資料來源.zip + V5 Data Pack (same line) | `claude/r14_merge_v1_8_source_closure/tools/D/footer.md` | 1 |
| 完整資料來源.zip + V5 Data Pack (same line) | `claude/r14_merge_v1_8_source_closure/tools/D/legacy_audit_result.json` | 1 |
| 完整資料來源.zip + V5 Data Pack (same line) | `claude/r14_merge_v1_8_source_closure/tools/E/build.py` | 1 |
| 完整資料來源.zip + V5 Data Pack (same line) | `claude/r14_merge_v1_8_source_closure/tools/E/final_view.txt` | 1 |
| 完整資料來源.zip + V5 Data Pack (same line) | `claude/r14_merge_v1_8_source_closure/tools/E/flags.csv` | 1 |
| 完整資料來源.zip + V5 Data Pack (same line) | `claude/r14_merge_v1_8_source_closure/tools/E/flags_view.txt` | 1 |
