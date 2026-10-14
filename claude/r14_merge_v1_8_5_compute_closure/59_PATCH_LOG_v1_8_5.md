# 59 — Patch log: v1.8.3 → v1.8.5 COMPUTE CLOSURE CANDIDATE (sub-agent U)

Date: 2026-10-14. Built by exact, asserted-once replacements (`tools\U\patch_v185.py`), verified by `tools\U\verify_v185.py`. No DOCX built. No commit.

| Item | Value |
|---|---|
| Source | `claude\r14_merge_v1_8_3_v5_recovery\41_MERGED_MASTER_THESIS_v1_8_3_V5_PROVENANCE_CANDIDATE.md` sha256 `0da8cec1521dbeff900ffa1fa9a1de0a31b0cdfa34b82c03531eba2111d7f740` (asserted) |
| Output | `59_MERGED_MASTER_THESIS_v1_8_5_COMPUTE_CLOSURE_CANDIDATE.md` sha256 `1812da36c8f045b8d5645a4241f8db138a00fc0b9a77522ac7f3c5c6fed01c35` |
| Lines | 3100 → 3136 |
| Patches | 37 (each `old` occurs exactly once in v1.8.3 and at apply time; reverse replay reproduces v1.8.3: True) |
| v1.8.3 lines touched | 31: 5, 13, 29, 122, 147, 158, 168, 405, 412, 605, 609, 619, 630, 645, 653, 1374, 1629, 1638, 1640, 2185, 2192, 2240, 2270, 2364, 2368, 2380, 3038, 3082, 3083, 3087, 3091 |
| Hard checks | 52/52 PASS → ALL_HARD_CHECKS_PASS = True |

## 1. Patches

| ID | Section | v1.8.3 line | Category | Evidence source |
|---|---|---:|---|---|
| U01 | 稿件狀態 | 5 | version label | orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line); Appendix D row U25 |
| U02 | 稿件狀態 | 5 | scope sentence (no new analysis -> one labelled sensitivity analysis) | orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line) |
| U03 | 稿件狀態 | 5 | v1.8.5 compute-closure summary | OUT 47 §2–§5; OUT 48; OUT 49; OUT 50; OUT 43 §1–§5; OUT 44; OUT 45; orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line) |
| U04 | 稿件狀態 | 5 | full-reanalysis status -> executed as sensitivity analysis | OUT 53 (table + gained/lost + flips); OUT 55; OUT 58 §1–§4; orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line) |
| U05 | 摘要 | 13 | full-reanalysis status -> executed as sensitivity analysis | OUT 43 §1–§5; OUT 44; OUT 45; OUT 47 §2–§5; OUT 48; OUT 49; OUT 50; OUT 53 (table + gained/lost + flips); OUT 55; OUT 58 §1–§4 |
| U06 | Abstract | 29 | full-reanalysis status -> executed as sensitivity analysis (English) | OUT 43 §1–§5; OUT 44; OUT 45; OUT 47 §2–§5; OUT 48; OUT 49; OUT 50; OUT 53 (table + gained/lost + flips); OUT 55; OUT 58 §1–§4 |
| U07 | 1.4 | 122 | full-reanalysis status | orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line); OUT 55 |
| U08 | 1.4 表 | 147 | full-reanalysis status | orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line); OUT 58 §1–§4 |
| U09 | 1.5 | 158 | full-reanalysis status | OUT 58 §1–§4; orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line) |
| U10 | 1.5 | 158 | full-reanalysis status (source note) | orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line) |
| U11 | 1.6 | 168 | full-reanalysis status | orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line); OUT 55 |
| U12 | 3.1.1 | 405 | full-reanalysis status | orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line); OUT 55 |
| U13 | 3.1.1 流程 | 412 | full-reanalysis status | orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line); OUT 58 §1–§4 |
| U14 | 3.7.4 | 605 | propagation rule preregistered + V1.8.5 procedure (new paragraph) | OUT 43 §1–§5; OUT 44; OUT 45; OUT 47 §2–§5; OUT 48; OUT 49; OUT 50; REVISED_GUARD_POLICY; REVISED_GUARD_SELF_AUDIT; REVISED_GUARD_DIFF.csv; OUT 49b; OUT 57 |
| U15 | 3.7.4 | 609 | full-reanalysis status + corpus-wide limitation | OUT 43 §1–§5; OUT 44; OUT 45; orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line) |
| U16 | 3.8.1 | 619 | L2' provenance | OUT 58 §1–§4 |
| U17 | 3.8.1 表 | 630 | L2' role column | OUT 53 (table + gained/lost + flips); OUT 58 §1–§4 |
| U18 | 3.8.2 規則 6 | 645 | handoff rule 6 (G list unchanged) | OUT 55 |
| U19 | 3.8.3 | 653 | baseline reproduction | OUT 47 §2–§5; OUT 48; OUT 49; OUT 50 |
| U20 | 第四章引言 | 1374 | chapter scope | orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line) |
| U21 | 4.5.5 | 1629 | full-reanalysis status | orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line) |
| U22 | 4.5.5 表註 | 1638 | handoff note | OUT 55 |
| U23 | 4.5.5 | 1640 | pointer to V1.8.5 values | OUT 53 (table + gained/lost + flips) |
| U24 | 4.5.5 | 1640 | interpretation sentence + NEW sensitivity block and Table 4-9B | OUT 53 (table + gained/lost + flips); OUT 54; OUT 55; OUT 57; OUT 58 §1–§4; OUT 52; OUT 44; OUT 51; OUT 47 |
| U26 | 4.11 表 | 2185 | full-reanalysis status | OUT 53 (table + gained/lost + flips); OUT 55; OUT 58 §1–§4 |
| U27 | 4.11 | 2192 | full-reanalysis status | OUT 58 §1–§4 |
| U28 | 5.3.2 表 | 2240 | full-reanalysis status | OUT 55 |
| U29 | 5.4.2 | 2270 | full-reanalysis status | OUT 58 §1–§4; orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line) |
| U30 | 5.8.9 | 2364 | full-reanalysis triplet + corpus-wide limitation | OUT 58 §1–§4; orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line) |
| U31 | 5.9 | 2368 | next-step wording | orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line) |
| U32 | 5.10 | 2380 | full-reanalysis status | OUT 58 §1–§4; orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line) |
| U25 | 附錄 D | 3038 | Appendix D rows 43–61 | RPT file list 43–58 (56 not written per OUT 55); this round (59); 60–61 reserved |
| U33 | 附錄 E39 | 3082 | residual limit (c) — sidecar reproduced | OUT 58 §1–§4 |
| U34 | 附錄 E40 | 3083 | full-reanalysis triplet (executed as sensitivity analysis) | OUT 43 §1–§5; OUT 44; OUT 45; OUT 47 §2–§5; OUT 48; OUT 49; OUT 50; REVISED_GUARD_POLICY; REVISED_GUARD_SELF_AUDIT; REVISED_GUARD_DIFF.csv; OUT 49b; OUT 53 (table + gained/lost + flips); OUT 55; OUT 57; OUT 58 §1–§4; orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line) |
| U35 | 附錄 E44 | 3087 | submission-readiness reason | orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line) |
| U36 | 附錄 E48 | 3091 | propagation rule status (resolved) | OUT 43 §1–§5; OUT 44; OUT 45 |
| U37 | 附錄 E48 | 3091 | propagation rule action (resolved) | OUT 43 §1–§5; OUT 44; OUT 45 |

Full old/new text of every patch: `59b_V183_TO_V185_SEGMENT_DIFF.md`.

## 2. Verification (hard checks)

| Check | Result |
|---|---|
| `source_sha_expected` | PASS |
| `changed_lines_subset_of_patched_lines` | PASS |
| `reverse_replay_reproduces_v183` | PASS |
| `math_identical_ordered` | PASS |
| `equation_tags_identical` | PASS |
| `no_math_markers_in_patch_text` | PASS |
| `fenced_blocks_identical_except_listed_status_patches` | PASS |
| `headings_identical_in_order_none_added` | PASS |
| `captions_only_4_9B_added` | PASS |
| `G_rows_identical_ordered` | PASS |
| `GM_arrow_tokens_identical` | PASS |
| `no_G17_or_new_G_code` | PASS |
| `section_3_9_1_identical` | PASS |
| `section_3_9_2_tables_3_4_3_4A_identical` | PASS |
| `section_3_9_3_V1_design_identical` | PASS |
| `section_3_9_4_identical` | PASS |
| `section_3_9_5_identical` | PASS |
| `section_3_10_to_3_14_enterprise_identical` | PASS |
| `section_4_1_to_4_4_primary_results_identical` | PASS |
| `section_4_5_1_to_4_5_4_identical` | PASS |
| `section_4_6_G_handoff_identical` | PASS |
| `section_4_7_to_4_10_V1_enterprise_identical` | PASS |
| `section_appendix_C_math_identical` | PASS |
| `count_unchanged_VCP` | PASS |
| `count_unchanged_VSC` | PASS |
| `count_unchanged_DL` | PASS |
| `count_unchanged_NEV` | PASS |
| `count_unchanged_Enterprise` | PASS |
| `count_unchanged_SIMULATED_ONLY` | PASS |
| `count_unchanged_EMPIRICAL RESULT PENDING` | PASS |
| `count_unchanged_SUBMISSION_READY` | PASS |
| `count_unchanged_UNIDENTIFIED` | PASS |
| `count_unchanged_M1` | PASS |
| `count_unchanged_M2` | PASS |
| `count_unchanged_M3` | PASS |
| `count_unchanged_M4` | PASS |
| `count_unchanged_M5` | PASS |
| `count_unchanged_REAL EVIDENCE` | PASS |
| `count_unchanged_HUMAN_RESULT_PENDING` | PASS |
| `SUBMISSION_READY_NO_kept` | PASS |
| `no_stale_pending_wording` | PASS |
| `status_line_L5_v185` | PASS |
| `corpus_wide_limitation_present` | PASS |
| `primary_baseline_replaced_NO_present` | PASS |
| `no_forbidden_claims` | PASS |
| `primary_phrases_unchanged` | PASS |
| `primary_tokens_not_removed` | PASS |
| `sensitivity_numbers_labelled` | PASS |
| `table_4_9B_columns_separate_primary_vs_sensitivity` | PASS |
| `numeric_patch_sum_matches_doc` | PASS |
| `numeric_added_all_traceable` | PASS |
| `numeric_removed_only_status_wording_tokens` | PASS |

## 3. Required verification items

- **Math identical:** True (counts v1.8.3/v1.8.5: {'$$': [18, 18], '$inline': [31, 31], '\\[\\]': [7, 7], 'begin_env': [0, 0]}); equation tags identical: True; no math markers in any patch: True.
- **Headings:** 182 → 182, identical and in the same order; **no heading added or changed** (True). The new content sits inside the existing §3.7.4 and §4.5.5 as paragraphs with bold run-in labels.
- **Captions:** one caption added — **表 4-9B：主要分析（凍結基準）與稽核標籤替代敏感度分析的比較** (in §4.5.5); none removed or reordered (True).
- **G table rows:** 36 → 36, identical and ordered (True); G→M arrow tokens identical (True); no new G code (True). G-token mentions in prose 291 → 324 (added by: {'U04': 2, 'U05': 2, 'U06': 2, 'U07': 2, 'U11': 2, 'U12': 2, 'U18': 2, 'U24': 7, 'U26': 2, 'U28': 2, 'U25': 4, 'U34': 4}); these are prose references ("G01–G16 移除 0" etc. and G07/G14/G16 boundary values), not numbering or row changes.
- **Protected sections identical:** 3_9_1=True; 3_9_2_tables_3_4_3_4A=True; 3_9_3_V1_design=True; 3_9_4=True; 3_9_5=True; 3_10_to_3_14_enterprise=True; 4_1_to_4_4_primary_results=True; 4_5_1_to_4_5_4=True; 4_6_G_handoff=True; 4_7_to_4_10_V1_enterprise=True; appendix_C_math=True.
- **Primary-baseline numbers unchanged:** fixed primary phrases (abstract, §1.5, Abstract, Table 3-3 L1/L2) all present with unchanged counts (True); primary tokens never removed {'6,499': [12, 14], '3,125': [17, 18], '783': [16, 17], '2,180': [20, 21]} (True); §4.1–§4.4 identical. The added occurrences of 6,499/3,125/783/2,180 are the primary column of the new Table 4-9B and E40/abstract labelling only.
- **Primary vs sensitivity separation:** Table 4-9B header separates the two columns (True); every sensitivity-only value (3,107 / 781 / 2,181 / 15／17 / q values) outside Table 4-9B sits in a sentence explicitly labelled 敏感度／sensitivity／替換 (True; violations: []).
- **Forbidden phrases:** {'human validation confirmed corpus taxonomy': 0, 'full reanalysis solved low kappa': 0, 'human labels validated all 6,499 records': 0, 'human labels validated all 6499 records': 0, 'FULLY_VALIDATED': 0, '人類驗證確認了語料分類': 0, '人工驗證確認全語料': 0, '完整重分析解決了低': 0, '人工標籤驗證了全部 6,499': 0} → none (True).
- **Stale pending wording removed:** `執行條件尚待滿足` 8→0, `執行條件待滿足` 8→0, `EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION` 4→0, `REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION` 4→0, `日後是否重跑` 7→0, `日後是否及何時重跑` 2→0, `PRIORITY_RATIONALE_REVIEW_REQUESTED` 1→0, `開放驗證行動` 10→0, `開放的驗證行動` 6→0.
- **New vocabulary counts (v1.8.3→v1.8.5):** `v1.8.5 COMPUTE CLOSURE CANDIDATE` 0→1, `COMPUTATIONAL_VALIDATION_STATUS = CLOSED_WITH_BOUNDED_HUMAN_VALIDITY` 0→1, `SATISFIED_AS_AUDITED_LABEL_SENSITIVITY_ANALYSIS` 0→4, `FULL_REANALYSIS_EXECUTED = YES` 0→5, `PRIMARY_BASELINE_REPLACED = NO` 0→6, `CORPUS_WIDE_HUMAN_VALIDITY = NOT_ESTABLISHED` 0→5, `BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1` 0→5, `STABLE_UNDER_FULL_AUDITED_LABEL_REANALYSIS` 0→2, `13/13 逐位元組相同` 0→6, `FULL_REANALYSIS_REQUIRED` 5→5, `NOT_RECOMMENDED` 4→1, `AUTHOR TO CONFIRM` 2→1, `SUBMISSION_READY = NO` 3→3.
  - `NOT_RECOMMENDED` 4→1: the priority flag survives only in E40 as the historical v1.8.3 judgement, superseded by researcher approval.
  - `AUTHOR TO CONFIRM` 2→1: the §3.7.4 tag was removed (E48 resolved); E48 still names it as removed.
  - The suggested semantics sentence appears 5 times (status line, abstract, §3.7.4, §4.5.5, §5.8.9).

## 4. Every added numeric token and its source

Net document token change = sum of per-patch changes: True. All added tokens mapped: True.

| Token | Net added | Source |
|---|---:|---|
| `.0223` | 1 | sensitivity: G16 revised document-null q — OUT 55 row G16 |
| `.0298` | 1 | sensitivity: G14 revised document-null q — OUT 55 row G14 |
| `.0325` | 1 | sensitivity: HUMAN_AUGMENTATION×RISK_ASSESSMENT revised document-null q — OUT 53 'GAINED'; OUT 54 |
| `.0405` | 1 | sensitivity: G07 revised document-null q — OUT 55 row G07 / boundary list |
| `.0434` | 1 | primary (reproduced baseline): COORDINATION_EXECUTION×GENERAL_DECISION_PROCESS baseline document-null q — OUT 53 'LOST'; OUT 54 (0.04349) |
| `.05` | 6 | BH threshold label p_BH ≤ .05 — OUT 53 table rows; robust predicate (OUT 57) |
| `.0567` | 1 | primary (reproduced baseline): HUMAN_AUGMENTATION×RISK_ASSESSMENT baseline document-null q — OUT 53 'GAINED'; OUT 54 |
| `.0610` | 1 | sensitivity: COORDINATION_EXECUTION×GENERAL_DECISION_PROCESS revised document-null q — OUT 53 'LOST'; OUT 54 (0.06108) |
| `0` | 16 | removed 0 / direction changed 0 (OUT 55); unauthorized replacements 0 (OUT 51/53); max abs diff 0 (OUT 58 §2) |
| `10` | 5 | stage 10 of stages 10–13 (OUT 47 §2; OUT 53); 10 × 12 taxonomy (OUT 43 §2; REVISED_GUARD_POLICY STRUCTURAL_INVARIANT) |
| `10,000` | 1 | main-null replicates 10,000 (OUT 47 §2; OUT 53) |
| `12` | 1 | 10 × 12 taxonomy (REVISED_GUARD_POLICY STRUCTURAL_INVARIANT) |
| `120` | 4 | 120 cells (10 × 12) — OUT 53; 120 × 4 methods (OUT 58 §2) |
| `13` | 7 | stage 13 / 13 official outputs (OUT 47 §2–§3) |
| `13/13` | 7 | BYTE_IDENTICAL=13/13 (OUT 47 §5) |
| `15` | 2 | revised enriched 15 (OUT 53 Enriched row) |
| `16` | 6 | baseline enriched/depleted 16/16 (OUT 53) and G01–G16 16/16 robust (OUT 55) |
| `17` | 3 | revised depleted 17 (OUT 53 Depleted row) |
| `19` | 1 | lost cell O = 19 unchanged (OUT 53) |
| `2,180` | 1 | primary baseline document edges (OUT 53 Baseline column = frozen primary value, unchanged) |
| `2,181` | 2 | sensitivity document edges (OUT 53) |
| `20` | 3 | 20 reconciled final labels (OUT 43 §1 clause A, §4) |
| `24` | 1 | cells with changed main observed count 24/120 (OUT 53) |
| `28` | 1 | cells with changed raw-record count 28/120 (OUT 53) |
| `3` | 1 | main-null direction flips 3/120, all non-core (OUT 53) |
| `3,107` | 2 | sensitivity pair-eligible records (OUT 53) |
| `3,125` | 1 | primary baseline pair-eligible (OUT 53 Baseline column = frozen primary value, unchanged) |
| `3.7.4` | 5 | section reference |
| `3.8.2` | 1 | section reference |
| `3.8.3` | 1 | section reference |
| `30` | 3 | 30 first-coder labels (OUT 43 §1 clause B, §4) |
| `31` | 1 | core members unchanged 31 (OUT 53) |
| `32` | 7 | robust core 32→32; document-null q≤.05 32→32 (OUT 53) |
| `4` | 1 | 4 methods × 120 cells (OUT 58 §2, §4) |
| `4-10` | 2 | table reference 表 4-10 |
| `4-4` | 1 | table reference 表 4-4 |
| `4-9` | 8 | table label 表 4-9B (new) / 4-9A |
| `4.1` | 1 | section reference |
| `4.4` | 2 | section reference |
| `4.5.1` | 1 | section reference |
| `4.5.5` | 10 | section reference |
| `43` | 6 | file number (RPT 43) |
| `44` | 2 | file number (RPT 44) |
| `45` | 6 | file number (RPT 45) |
| `46` | 7 | exact q≤.05 baseline 46 (OUT 53; = Table 4-2) and file number 46 |
| `47` | 6 | main q≤.05 47→47, exact revised 47 (OUT 53) and file number 47 |
| `48` | 1 | file number (RPT 48) |
| `49` | 3 | file number (RPT 49 / 49b) |
| `5,000` | 1 | document-null replicates 5,000 (OUT 47 §2; OUT 53) |
| `5.9` | 1 | section reference |
| `50` | 29 | 50 targeted audit records (OUT 43 §4; OUT 44; OUT 51) and file number 50 |
| `51` | 5 | file number (RPT 51) |
| `52` | 2 | file number (RPT 52) |
| `53` | 7 | file number (RPT 53) |
| `54` | 4 | raw-record q≤.05 baseline 54 (OUT 53; = Table 4-2) and file number 54 |
| `55` | 7 | raw-record q≤.05 revised 55 (OUT 53) and file number 55 |
| `56` | 1 | file number (RPT 56, not written per OUT 55) |
| `57` | 5 | file number (RPT 57) |
| `58` | 8 | file number (RPT 58) |
| `59` | 4 | file number (this manuscript, RPT 59) |
| `6,499` | 2 | strict records 6,499→6,499 (OUT 53) |
| `60` | 1 | file number reserved (RPT 60) |
| `61` | 1 | file number reserved (RPT 61) |
| `781` | 2 | sensitivity unique documents (OUT 53) |
| `783` | 1 | primary baseline unique documents (OUT 53 Baseline column = frozen primary value, unchanged) |

Removed numeric tokens (status wording only; no result value): `04`×1, `07`×1, `2`×1, `256`×4, `37`×4, `38`×1, `5`×1, `8`×1 — from the deleted v1.8.3 pending-status text (37 protected inputs; V1.8 檔案 04/07 §8; V1.8.1 檔案 15; 理由 2–5; SHA-256; V1.8.3 檔案 38).

Per-patch numeric changes:

| Patch | Added | Removed |
|---|---|---|
| U03 | {'10': 1, '13': 2, '13/13': 1, '46': 1, '50': 2, '43': 1, '45': 1, '51': 1, '58': 1, '3.7.4': 1, '4.5.5': 1} | {} |
| U04 | {'50': 1, '0': 2, '4.5.5': 1} | {'37': 1, '256': 1, '13': 1} |
| U05 | {'50': 2, '32': 1, '20': 1, '30': 1, '13/13': 1, '15': 1, '17': 1} | {} |
| U06 | {'50': 2, '32': 1, '20': 1, '30': 1, '13': 2, '15': 1, '17': 1} | {'37': 1} |
| U07 | {'50': 1} | {} |
| U11 | {'50': 1} | {} |
| U12 | {'50': 1} | {} |
| U14 | {'43': 2, '45': 2, '50': 3, '20': 1, '30': 1, '10': 2, '13': 2, '13/13': 1, '46': 1, '12': 1, '120': 1, '57': 1, '4.5.5': 1} | {} |
| U15 | {'50': 1} | {'37': 1, '256': 1} |
| U16 | {'4.5.5': 1} | {} |
| U17 | {'4-9': 1, '53': 1, '58': 1} | {} |
| U18 | {'0': 2} | {} |
| U19 | {'10': 1, '13': 2, '13/13': 1, '46': 1, '50': 1} | {} |
| U20 | {'4.5.5': 1} | {} |
| U21 | {'4-9': 2} | {'37': 1, '256': 1} |
| U24 | {'32': 4, '50': 5, '3.7.4': 1, '0': 6, '37': 1, '44': 1, '51': 1, '4-9': 3, '4.4': 2, '4-10': 2, '6,499': 2, '3,125': 1, '3,107': 1, '783': 1, '781': 1, '2,180': 1, '2,181': 1, '.05': 5, '47': 4, '46': 1, '54': 2, '55': 3, '16': 6, '15': 1, '17': 1, '4.1': 1, '13/13': 1, '53': 3, '57': 1, '10,000': 1, '5,000': 1, '120': 2, '24': 1, '28': 1, '3': 1, '52': 1, '31': 1, '.0567': 1, '.0325': 1, '1': 1, '.0434': 1, '.0610': 1, '19': 1, '4': 1, '58': 1, '.0405': 1, '.0298': 1, '.0223': 1, '4-4': 1, '4.5.1': 1} | {} |
| U26 | {'53': 1, '55': 1, '58': 1} | {} |
| U28 | {'0': 2} | {} |
| U29 | {'4.5.5': 1, '4-9': 1, '50': 1} | {} |
| U30 | {'50': 2, '4.5.5': 1} | {} |
| U31 | {'50': 1} | {} |
| U32 | {'50': 1} | {} |
| U25 | {'43': 2, '45': 2, '44': 1, '50': 3, '3.7.4': 3, '46': 2, '47': 1, '48': 1, '49': 3, '13/13': 1, '3.8.3': 1, '51': 2, '54': 2, '52': 1, '53': 1, '120': 1, '4.5.5': 3, '4-9': 1, '55': 2, '0': 2, '3.8.2': 1, '56': 1, '57': 2, '58': 2, '59': 4, '60': 1, '61': 1} | {} |
| U33 | {'58': 1} | {} |
| U34 | {'13/13': 1, '46': 1, '50': 1, '10': 1, '51': 1, '57': 1, '3,107': 1, '781': 1, '2,181': 1, '.05': 1, '47': 1, '32': 1, '53': 1, '58': 1, '0': 2, '55': 1, '5.9': 1} | {'37': 1, '256': 1, '38': 1, '07': 1, '8': 1, '15': 1, '1': 1, '2': 1, '5': 1, '04': 1} |
| U36 | {'43': 1, '45': 1} | {} |

## 5. Scope statement

- Changed: status line L5 (v1.8.5 label, compute-closure summary, COMPUTATIONAL_VALIDATION_STATUS, triplet), abstract/Abstract, §1.4/1.5/1.6, §3.1.1, §3.7.4 (rule preregistered; new procedure paragraph), §3.8.1 (L2′ provenance + Table 3-3 role cell), §3.8.2 rule 6 (wording only; G list unchanged), §3.8.3 (baseline reproduction sentence), ch.4 intro, §4.5.5 (status + new sensitivity block + Table 4-9B), §4.11 (two cells), §5.3.2 table cell, §5.4.2, §5.8.9, §5.9, §5.10, Appendix D (rows 43–61), Appendix E39(c)/E40/E44/E48.
- Unchanged (verified): all math, §3.9.1–§3.9.5 incl. Tables 3-4/3-4A and V1 design text, §3.10–§3.14 enterprise model, §4.1–§4.4 primary results, §4.5.1–§4.5.4, §4.6 G handoff table, §4.7–§4.10, Appendix C, all G rows, all headings.
- Appendix D: rows 60–61 are reserved placeholders (files do not exist at build time); row 56 records that no decision memo was required (OUT 55).

```
MANUSCRIPT=v1.8.5 COMPUTE CLOSURE CANDIDATE
SOURCE_SHA256=0da8cec1521dbeff900ffa1fa9a1de0a31b0cdfa34b82c03531eba2111d7f740
OUTPUT_SHA256=1812da36c8f045b8d5645a4241f8db138a00fc0b9a77522ac7f3c5c6fed01c35
PATCHES=37
HARD_CHECKS=52/52 PASS
HEADINGS_ADDED=0
CAPTIONS_ADDED=1 (表 4-9B)
PRIMARY_BASELINE_NUMBERS_CHANGED=0
FORBIDDEN_PHRASES=0
SUBMISSION_READY=NO
DOCX=NOT_BUILT
```
