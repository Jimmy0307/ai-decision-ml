# 04 — Local Robust-Core Sensitivity: Source Reproduction (Phase 5, sub-agent C)

Run: V1.8 source-verified evidence closure, 2026-10-14. Workspace W = `C:\NTUST_PAPER\outputs\20261014_AI_DECISION_V1_8_SOURCE_CLOSURE`.
Source package: `W\02_V9_HUMAN_VALIDATION\20260929_V9_HUMAN_VALIDATION\` (all files read-only; nothing in W was executed).

Helper scripts (reproducible, run with `python -I`):
- `C:\Users\user\AppData\Local\Temp\claude\C--NTUST-PAPER\b2185478-fbc8-4bee-8105-bb5557dd964b\scratchpad\v18\C\phase5_local_sensitivity.py <W>` -> `phase5_out.json`
- `...\v18\C\phase5_part2.py <W> phase5_out.json` -> `phase5_part2_out.json`
- `...\v18\C\phase5_tables.py phase5_out.json phase5_part2_out.json <W>` -> tables T1–T5 below

## 0. Inputs and hashes (SHA-256, computed this run)

| File | SHA-256 | Matches V9 `FINAL_ARTIFACT_HASH_MANIFEST.csv` |
|---|---|---|
| ROBUST_CORE_LOCAL_SENSITIVITY.csv (120 data rows, 120 unique cells) | e3166ee183e18f340c539b983108e2c972d18b916672a62510a25638db8b5b59 | YES |
| ROBUST_CORE_LOCAL_SENSITIVITY_DIFF.csv (33 data rows) | f6607aaee5c6381361209d1c9cbb7a92b1350a82d583427441a70a029398de62 | YES |
| ROBUST_CORE_LOCAL_SENSITIVITY.md | b25b9a84b42b34f089e3d59ba440e879159a117d31b70ea935ea06642eb71049 | YES |
| ROBUST_CORE_LOCAL_SENSITIVITY_STATUS.json | efc63b5b8841c72e75f7ffaf917d266504ec757ee32ca5ff1fa0200ffc136778 | (not listed) |
| ROBUST_CORE_IMPACT_SCREEN_50.csv | 03caebae8c126048489cb9c4176acc89b38a7746e6dbf3137bd6a3a9a89b7711 | — |
| REANALYSIS_CANDIDATES_FROM_HUMAN_AUDIT.csv (44 rows / 44 unique records) | 489a1af42eacf3b495c99643026cbb5b691d8664cb0a821e48121caae976c1ba | — |
| HUMAN_RECONCILED_20.csv (20 records) | 4b7ceac2c8c8bf2912ea542d88a1b887a42ed450aa248dce371525c25bb5bda0 | = FINAL_STATUS.json reconciliation.sha256 |
| FIRST_CODER_50_FINAL_FROZEN.csv (50 records) | dd332dd8cfecf7dde9a29d32bca654b7c04c49f499c3e6213cd4d9a2ed157400 | = FINAL_STATUS.json first_coder.snapshot_sha256 |

Rows in the DIFF CSV are byte-identical (field-by-field) to the corresponding rows of the full CSV.

## 1. Verification of the two reported changes (recomputed from CSV rows, not from the .md)

Membership sets were rebuilt from `official_core_member` / `sidecar_core_member` columns. Independently, the promotion rule (q <= .05 in main, exact, document-preserving AND raw-record, same direction in all four) was re-applied to the per-method q and direction columns for both sides of all 120 cells: **0 mismatches** with the member flags (so structural core = full-sensitivity core = 32 on both sides, as STATUS.json states).

| Check | Result | State |
|---|---|---|
| Official core size | 32 (16 ENRICHED / 16 DEPLETED) | CONFIRMED |
| Sidecar core size | 32 (**15 ENRICHED / 17 DEPLETED**) | CONFIRMED |
| GAINED | `HUMAN_AUGMENTATION x RISK_ASSESSMENT`, sidecar direction **DEPLETED** | CONFIRMED |
| LOST | `COORDINATION_EXECUTION x GENERAL_DECISION_PROCESS`, official direction **ENRICHED** | CONFIRMED |
| Shared cells | 31, direction changes among shared = 0 | CONFIRMED |
| Any other membership change | none (core_membership_changed = YES in exactly 2 of 120 rows) | CONFIRMED |
| Core SHA-256 in STATUS.json (a43b4b58… / 4e412a07…) | could not be reproduced with ~100 tried serialisations (no generating script in package) | UNRESOLVED (does not affect set membership, which is recomputed from rows) |

Mechanism (from the q columns): both swaps are driven by the **document-preserving null**, at the q = .05 boundary.
- LOST `COORDINATION_EXECUTION x GENERAL_DECISION_PROCESS`: main O 19 -> 19 (unchanged); document q .0435 -> .0611 (fails); main q .0167 -> .0251, exact .0168 -> .0237, raw .0087 -> .0138 (still pass).
- GAINED `HUMAN_AUGMENTATION x RISK_ASSESSMENT`: main O 1 -> 1 (unchanged); document q .0567 -> .0325 (now passes); main/exact/raw already passed officially (main q .00092 -> .00089).
- Neither swapped cell had its own observed count changed; the swaps come from marginal/degree shifts produced by relabelling other records. This matches the v1.7 prose (line 1635: gained cell "主要零模型顯著…但未通過文獻內部結構保持零模型"; lost cell O = 19).

## 2. Answers

### Q1. Does the 32-cell exact robust-core membership change?
**YES.** Size stays 32 but membership changes by exactly one in / one out (Jaccard 31/33 = 0.939). Direction split changes from 16/16 to **15/17** (enriched/depleted). The other **31 frozen pairs are unchanged in membership and direction** — this verifies the v1.7 claims in 128 CF-01, 137 P0-1 and manuscript line 630 ("32（…推得 15／17：+1 不足、−1 過度）"); the "若無其他未回報的變動" condition is satisfied (no other unreported change).

Baseline-vs-canonical check: the CSV's official 32-cell set (T1) contains exactly 16 DEPLETED cells, and that set is **identical, by exact pair-name string, to the G01–G16 list in `r14_merge_v1_7\132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX.csv`** (set difference empty both ways; no naming differences — both use the uppercase FSC family codes, e.g. `PREDICTION_RISK_ESTIMATION`, `HUMAN_REVIEW_ACCOUNTABILITY`). The 132 column "O (doc-level edges)" equals the CSV `official_observed` (= `official_document_observed`) for all 16 G cells. The CSV official main observed column sums to 2,180 (= frozen document-level edges) and the raw column to 3,125 (= frozen fully mapped records). The 16 enriched cells cannot be matched to a machine-readable list in 128/132 (132 covers G01–G16 only; 128 refers to R14 tables 9–10 and r14/04, which are not in this run's r14_merge_v1_7 folder); they are taken from the CSV and agree with the 16/16 count in 128 and the V9 forensic audit (`V9_FINAL_FORENSIC_AUDIT.md` line 38). Enriched-list match to R14 Table 9 = UNRESOLVED here (not checked against a table file).

### Q2. Is any G01–G16 depletion cell removed?
**NO.** All 16 G cells remain sidecar core members with direction DEPLETED (T2). Several G cells' observed counts moved (G02 6->7, G06 9->10, G09 26->25, G10 8->9, G13 15->14, G14 8->10) without losing membership. Closest to the boundary in the sidecar: G07 (doc q .0405), G14 (doc q .0298), G16 (doc q .0223). Confirms manuscript line 645 ("未移除任何 G01–G16") — CONFIRMED.

### Q3. Is the only change one added depleted pair plus one lost enriched pair? Count all diffs.
For **core membership: yes** — exactly +1 DEPLETED, −1 ENRICHED, 0 shared-direction changes. But the sidecar is not otherwise identical: the DIFF CSV has **33 changed cells of 120**:

| Change class (mutually exclusive, priority as listed) | Cells |
|---|---:|
| Core membership change (the two cells above; own counts unchanged) | 2 |
| Main observed count changed (and raw count changed) | 24 |
| Main-null direction flip, non-core, own count unchanged (`EVALUATION_ASSESSMENT x INFORMATION_SYNTHESIS`, `GENERATION_SYNTHESIS x ALLOCATION_PLANNING`, `RECOMMENDATION_OPTIMIZATION x EXECUTION_COORDINATION`; all q = 1.0) | 3 |
| Raw-record count only (main count unchanged) | 4 |
| **Total diff rows** | **33** |

Global counts (recomputed from rows, all match STATUS.json/.md): main observed changed 24/120; main direction changed 3/120; pair-eligible records 3,125 -> 3,107 (−18, sum of raw column); document edges 2,180 -> 2,181 (+1); main q<=.05 47 -> 47; main q<=.01 34 -> 32. Largest count shift: `PREDICTION_RISK_ESTIMATION x PREDICTION_DIAGNOSIS` 226 -> 220 (raw 547 -> 533), still core ENRICHED.

### Q4. Was the full corpus actually rerun?
**NO — this is a local sidecar recomputation, not a full reanalysis.** Evidence:
- `ROBUST_CORE_LOCAL_SENSITIVITY.md`, `REANALYSIS_PROPOSAL.md`, `FINAL_HUMAN_AUDIT_REPORT.md` l.61, `V9_FINAL_FORENSIC_AUDIT.md` l.42: "applies reconciled final labels to the 20 overlap records and first-coder labels to the other 30 audited records; unaudited records remain unchanged"; "This is not a full-corpus correction"; status `FULL_REANALYSIS_REQUIRES_RESEARCHER_APPROVAL`.
- STATUS.json: `model_calls: 0`, `official_results_modified: false`, `human_answers_modified: false`, `reanalysis_requires_researcher_approval: true`. Strict records 6,499 unchanged; only the 50 audited records (all Robust-A, all in the 3,125 / 2,180 / final-32 frames per the impact screen) were relabelled.
- What *was* recomputed: the full statistical stack (120 cells × 4 methods; main null 10,000 reps seed 20260918, document null 5,000 reps seed 20260919, BH within method) on the corpus with 50 records substituted; the uncorrected sidecar reportedly reproduced 13 hash-pinned official outputs byte-for-byte (claim in the .md; the reproduction artifacts/script are not in the package — NOT_RECOVERED).
- No script generating `ROBUST_CORE_LOCAL_SENSITIVITY*.csv` exists anywhere in W (grep for `sidecar_core_member` / filename across all *.py: none). The q-values themselves therefore cannot be re-derived here; only set membership and rule-consistency were reproduced.
- The exact label→eligibility propagation rule is not recoverable: none of five plausible rules applied to the 50 human labels reproduces the −18 pair-eligible delta (they give −13, −17, −21, −24, −25, −27). Status of the rule: UNRESOLVED.
- Timing: the label inputs (reconciliation events) are timestamped **2026-10-03T07:45–11:09Z** and `FINAL_STATUS.json` `verified_at_utc` = 2026-10-03T12:23:44Z, with decision `HUMAN_AUDIT_CONVERGED / LOCAL_SENSITIVITY_CHANGED / FULL_REANALYSIS_REQUIRED`. So the sidecar was produced on or after 2026-10-03, not on 2026-09-29; "20260929" is the package/folder name. v1.7 citations "〔2026-09-29 紀錄〕" should be re-dated (2026-10-03 artifacts inside the 20260929_V9 package). File mtimes (2026-10-14 02:06) reflect extraction only.

## 3. Additional checks requested by orchestrator

### 3a. v1.7 "15／17 and the other 31 frozen pairs unchanged" (128 CF-01, 137 P0-1, manuscript l.630)
CONFIRMED from raw rows: sidecar 15 enriched / 17 depleted; 31 shared pairs, all same direction. v1.7 wording that the sidecar uses "人工調和標籤替換受稽核記錄" (manuscript l.2268) is imprecise: only 20 records use reconciled labels; 30 use single first-coder labels (with 19 of the 20 human-adjudicated, 1 unanimous). Recommend rewording.

### 3b. CF-11 / E49 — scope overlap between label-replacement sensitivity and evidence-unit re-segmentation sensitivity (`V9_1_SEGMENTATION_SENSITIVITY\`)
- Label treatment: **no overlap.** Segmentation protocol l.45: "Human labels are examples/motivation only and are never propagated to unaudited records"; final report l.7: "no final/reconciled human label was propagated to candidate or unaudited records, so this experiment does not estimate the effect of human corrections"; l.67: "human labels were used only as predeclared error-example candidate flags". Row check: for the 22 audited records **not** re-segmented, S1 and S2 record-level freeze rows carry the **model** families in 22/22 cases and the human-only family in 0/22. The 28 audited records that were re-segmented were re-mapped by Stage-1/Stage-2 model mapping, not human labels.
- Record scope: **partial overlap of the record set.** All 50 audited records are in the 6,499-row segmentation manifest; 28/50 were selected as segmentation candidates (11 carry `HUMAN_AUDIT_ERROR_TAG` among their reasons; the other 17 were selected by structural rules alone); 3,112/6,499 records were candidates overall.
- Conclusion: the R14 phrase "人工調和標籤不傳播至未稽核記錄" does **not** mean audited records used human labels in the re-segmentation; they used model mappings. The two sensitivities are distinct measurement operations that share input records (28 of the 50 audited records are also re-segmented) but **not** label sources. Human audit influenced segmentation only through candidate selection (11 error-tagged records). v1.7 E49 "範圍可能部分重疊，待核" can be resolved as: overlap in record selection (28/50; human error tags force 11 into the candidate set), no overlap in labels; "independent" is defensible for label treatment, not for the record sample.
- Note: the segmentation sensitivity uses a different promotion rule (four analyses, sizes 31/31) and its own lost cells include G15 `EXPLANATION_ASSURANCE x EVALUATION_SELECTION` (S1, S2) and G07 `HUMAN_AUGMENTATION x EVALUATION_SELECTION` (S1) (`ROBUST_CORE_COMPARISON.md`). That is outside this phase (segmentation, not label replacement) but means "no G01–G16 removed" holds only for the label-replacement sidecar.

## 4. Label changes that a full reanalysis would need to propagate

Derivable from the package: YES for the 50 audited records' model vs human labels (T4); the exact propagation rule the sidecar applied (handling of UNCERTAIN / AMBIGUOUS / UNMAPPED) is UNRESOLVED. Of 50 audited records, **46 have at least one field differing from the model label** (17 of the 20 reconciled, 29 of the 30 first-coder-only), **91 field changes** in total (inclusion, AI family, decision family). Model-side all 50 were pair-eligible; human C5 = INCLUDE 30, EXCLUDE 13, UNCERTAIN 7. The 44 records listed in `REANALYSIS_CANDIDATES_FROM_HUMAN_AUDIT.csv` are based on first-coder labels for all 50 (impact screen: NO_IMPACT 6, POTENTIAL_EXCLUSION 11, POTENTIAL_FAMILY_REASSIGNMENT 19, UNDETERMINED 14); for the 20 reconciled records the FINAL labels differ from the first-coder frozen labels in 18/20 (T5), so the candidate list ≠ the sidecar input for those records. A full reanalysis must use T4 (reconciled where available), not the impact-screen pair columns.

## 5. Tables

### T1. Official (frozen) 32-cell core recomputed from CSV rows, with sidecar status

| # | AI family x Decision family | Official dir | Sidecar member | Sidecar dir | G ID | main O off->sc | doc q off / sc |
|---|---|---|---|---|---|---|---|
| 1 | COORDINATION_EXECUTION x ALLOCATION_PLANNING | ENRICHED | YES | ENRICHED |  | 67->67 | 0.0024 / 0.0022 |
| 2 | COORDINATION_EXECUTION x GENERAL_DECISION_PROCESS | ENRICHED | NO | - |  | 19->19 | 0.0435 / 0.0611 |
| 3 | COORDINATION_EXECUTION x HUMAN_REVIEW_ACCOUNTABILITY | DEPLETED | YES | DEPLETED | G16 | 10->10 | 0.0137 / 0.0223 |
| 4 | COORDINATION_EXECUTION x RISK_ASSESSMENT | DEPLETED | YES | DEPLETED | G03 | 3->3 | 0.0024 / 0.0022 |
| 5 | EVALUATION_ASSESSMENT x ALLOCATION_PLANNING | DEPLETED | YES | DEPLETED | G11 | 12->12 | 0.0024 / 0.0022 |
| 6 | EVALUATION_ASSESSMENT x EVALUATION_SELECTION | ENRICHED | YES | ENRICHED |  | 45->44 | 0.0024 / 0.0022 |
| 7 | EVALUATION_ASSESSMENT x GOVERNANCE_OVERSIGHT | ENRICHED | YES | ENRICHED |  | 93->91 | 0.0024 / 0.0022 |
| 8 | EVALUATION_ASSESSMENT x PREDICTION_DIAGNOSIS | DEPLETED | YES | DEPLETED | G06 | 9->10 | 0.0024 / 0.0022 |
| 9 | EXPLANATION_ASSURANCE x ALLOCATION_PLANNING | DEPLETED | YES | DEPLETED | G05 | 7->7 | 0.0024 / 0.0022 |
| 10 | EXPLANATION_ASSURANCE x EVALUATION_SELECTION | DEPLETED | YES | DEPLETED | G15 | 7->7 | 0.0387 / 0.0178 |
| 11 | EXPLANATION_ASSURANCE x GOVERNANCE_OVERSIGHT | ENRICHED | YES | ENRICHED |  | 101->100 | 0.0024 / 0.0022 |
| 12 | EXPLANATION_ASSURANCE x HUMAN_REVIEW_ACCOUNTABILITY | ENRICHED | YES | ENRICHED |  | 75->74 | 0.0024 / 0.0022 |
| 13 | EXPLANATION_ASSURANCE x PREDICTION_DIAGNOSIS | DEPLETED | YES | DEPLETED | G13 | 15->14 | 0.0024 / 0.0022 |
| 14 | GENERATION_SYNTHESIS x INFORMATION_ACQUISITION | ENRICHED | YES | ENRICHED |  | 53->52 | 0.0058 / 0.0134 |
| 15 | GENERATION_SYNTHESIS x PREDICTION_DIAGNOSIS | DEPLETED | YES | DEPLETED | G04 | 7->7 | 0.0042 / 0.0022 |
| 16 | HUMAN_AUGMENTATION x EVALUATION_SELECTION | DEPLETED | YES | DEPLETED | G07 | 2->2 | 0.0304 / 0.0405 |
| 17 | HUMAN_AUGMENTATION x HUMAN_REVIEW_ACCOUNTABILITY | ENRICHED | YES | ENRICHED |  | 58->57 | 0.0024 / 0.0022 |
| 18 | HUMAN_AUGMENTATION x INFORMATION_ACQUISITION | ENRICHED | YES | ENRICHED |  | 38->38 | 0.0215 / 0.0325 |
| 19 | HUMAN_AUGMENTATION x PREDICTION_DIAGNOSIS | DEPLETED | YES | DEPLETED | G01 | 3->3 | 0.0024 / 0.0022 |
| 20 | HUMAN_AUGMENTATION x RISK_ASSESSMENT | -(not member) | YES | DEPLETED |  | 1->1 | 0.0567 / 0.0325 |
| 21 | PREDICTION_RISK_ESTIMATION x EVALUATION_SELECTION | DEPLETED | YES | DEPLETED | G10 | 8->9 | 0.0058 / 0.0042 |
| 22 | PREDICTION_RISK_ESTIMATION x GENERAL_DECISION_PROCESS | DEPLETED | YES | DEPLETED | G14 | 8->10 | 0.0089 / 0.0298 |
| 23 | PREDICTION_RISK_ESTIMATION x GOVERNANCE_OVERSIGHT | DEPLETED | YES | DEPLETED | G09 | 26->25 | 0.0024 / 0.0022 |
| 24 | PREDICTION_RISK_ESTIMATION x HUMAN_REVIEW_ACCOUNTABILITY | DEPLETED | YES | DEPLETED | G02 | 6->7 | 0.0024 / 0.0022 |
| 25 | PREDICTION_RISK_ESTIMATION x INFORMATION_ACQUISITION | DEPLETED | YES | DEPLETED | G12 | 21->21 | 0.0024 / 0.0022 |
| 26 | PREDICTION_RISK_ESTIMATION x PREDICTION_DIAGNOSIS | ENRICHED | YES | ENRICHED |  | 226->220 | 0.0024 / 0.0022 |
| 27 | PREDICTION_RISK_ESTIMATION x RISK_ASSESSMENT | ENRICHED | YES | ENRICHED |  | 82->82 | 0.0024 / 0.0022 |
| 28 | RECOMMENDATION_OPTIMIZATION x ALLOCATION_PLANNING | ENRICHED | YES | ENRICHED |  | 86->86 | 0.0024 / 0.0022 |
| 29 | RECOMMENDATION_OPTIMIZATION x EVALUATION_SELECTION | ENRICHED | YES | ENRICHED |  | 34->34 | 0.0089 / 0.0080 |
| 30 | RECOMMENDATION_OPTIMIZATION x GENERAL_DECISION_PROCESS | ENRICHED | YES | ENRICHED |  | 41->40 | 0.0024 / 0.0022 |
| 31 | RECOMMENDATION_OPTIMIZATION x HUMAN_REVIEW_ACCOUNTABILITY | DEPLETED | YES | DEPLETED | G08 | 8->8 | 0.0024 / 0.0022 |
| 32 | RETRIEVAL_SYNTHESIS x INFORMATION_ACQUISITION | ENRICHED | YES | ENRICHED |  | 21->21 | 0.0042 / 0.0022 |
| 33 | RETRIEVAL_SYNTHESIS x INFORMATION_SYNTHESIS | ENRICHED | YES | ENRICHED |  | 6->7 | 0.0042 / 0.0166 |

### T2. G01-G16 mapping (132 matrix) vs official/sidecar core

| G | AI family x Decision family | O (132) | O main official (CSV) | official core | sidecar core | sidecar main O |
|---|---|---|---|---|---|---|
| G01 | HUMAN_AUGMENTATION x PREDICTION_DIAGNOSIS | 3 | 3 | DEPLETED | DEPLETED | 3 |
| G02 | PREDICTION_RISK_ESTIMATION x HUMAN_REVIEW_ACCOUNTABILITY | 6 | 6 | DEPLETED | DEPLETED | 7 |
| G03 | COORDINATION_EXECUTION x RISK_ASSESSMENT | 3 | 3 | DEPLETED | DEPLETED | 3 |
| G04 | GENERATION_SYNTHESIS x PREDICTION_DIAGNOSIS | 7 | 7 | DEPLETED | DEPLETED | 7 |
| G05 | EXPLANATION_ASSURANCE x ALLOCATION_PLANNING | 7 | 7 | DEPLETED | DEPLETED | 7 |
| G06 | EVALUATION_ASSESSMENT x PREDICTION_DIAGNOSIS | 9 | 9 | DEPLETED | DEPLETED | 10 |
| G07 | HUMAN_AUGMENTATION x EVALUATION_SELECTION | 2 | 2 | DEPLETED | DEPLETED | 2 |
| G08 | RECOMMENDATION_OPTIMIZATION x HUMAN_REVIEW_ACCOUNTABILITY | 8 | 8 | DEPLETED | DEPLETED | 8 |
| G09 | PREDICTION_RISK_ESTIMATION x GOVERNANCE_OVERSIGHT | 26 | 26 | DEPLETED | DEPLETED | 25 |
| G10 | PREDICTION_RISK_ESTIMATION x EVALUATION_SELECTION | 8 | 8 | DEPLETED | DEPLETED | 9 |
| G11 | EVALUATION_ASSESSMENT x ALLOCATION_PLANNING | 12 | 12 | DEPLETED | DEPLETED | 12 |
| G12 | PREDICTION_RISK_ESTIMATION x INFORMATION_ACQUISITION | 21 | 21 | DEPLETED | DEPLETED | 21 |
| G13 | EXPLANATION_ASSURANCE x PREDICTION_DIAGNOSIS | 15 | 15 | DEPLETED | DEPLETED | 14 |
| G14 | PREDICTION_RISK_ESTIMATION x GENERAL_DECISION_PROCESS | 8 | 8 | DEPLETED | DEPLETED | 10 |
| G15 | EXPLANATION_ASSURANCE x EVALUATION_SELECTION | 7 | 7 | DEPLETED | DEPLETED | 7 |
| G16 | COORDINATION_EXECUTION x HUMAN_REVIEW_ACCOUNTABILITY | 10 | 10 | DEPLETED | DEPLETED | 10 |

### T3. All 33 rows of ROBUST_CORE_LOCAL_SENSITIVITY_DIFF.csv classified

| Cell | main O delta | raw O delta | main dir off->sc | core off->sc | change class |
|---|---|---|---|---|---|
| COORDINATION_EXECUTION x ALLOCATION_PLANNING | 0 | -1 | ENRICHED->ENRICHED | YES->YES | RAW_COUNT |
| COORDINATION_EXECUTION x EXECUTION_COORDINATION | 1 | 1 | ENRICHED->ENRICHED | NO->NO | MAIN_COUNT+RAW_COUNT |
| COORDINATION_EXECUTION x GENERAL_DECISION_PROCESS | 0 | 0 | ENRICHED->ENRICHED | YES->NO | CORE_MEMBERSHIP |
| COORDINATION_EXECUTION x INFORMATION_SYNTHESIS | 1 | 1 | DEPLETED->DEPLETED | NO->NO | MAIN_COUNT+RAW_COUNT |
| EVALUATION_ASSESSMENT x EVALUATION_SELECTION | -1 | -1 | ENRICHED->ENRICHED | YES->YES | MAIN_COUNT+RAW_COUNT |
| EVALUATION_ASSESSMENT x GOVERNANCE_OVERSIGHT | -2 | -3 | ENRICHED->ENRICHED | YES->YES | MAIN_COUNT+RAW_COUNT |
| EVALUATION_ASSESSMENT x INFORMATION_SYNTHESIS | 0 | 0 | ENRICHED->DEPLETED | NO->NO | MAIN_DIRECTION(non-core) |
| EVALUATION_ASSESSMENT x PREDICTION_DIAGNOSIS | 1 | 1 | DEPLETED->DEPLETED | YES->YES | MAIN_COUNT+RAW_COUNT |
| EXPLANATION_ASSURANCE x EXECUTION_COORDINATION | 1 | 1 | DEPLETED->DEPLETED | NO->NO | MAIN_COUNT+RAW_COUNT |
| EXPLANATION_ASSURANCE x GOVERNANCE_OVERSIGHT | -1 | -4 | ENRICHED->ENRICHED | YES->YES | MAIN_COUNT+RAW_COUNT |
| EXPLANATION_ASSURANCE x HUMAN_REVIEW_ACCOUNTABILITY | -1 | -1 | ENRICHED->ENRICHED | YES->YES | MAIN_COUNT+RAW_COUNT |
| EXPLANATION_ASSURANCE x PREDICTION_DIAGNOSIS | -1 | -1 | DEPLETED->DEPLETED | YES->YES | MAIN_COUNT+RAW_COUNT |
| GENERAL_REASONING_SYSTEMS x EVALUATION_SELECTION | 1 | 1 | DEPLETED->DEPLETED | NO->NO | MAIN_COUNT+RAW_COUNT |
| GENERAL_REASONING_SYSTEMS x GENERAL_DECISION_PROCESS | 1 | 1 | DEPLETED->DEPLETED | NO->NO | MAIN_COUNT+RAW_COUNT |
| GENERATION_SYNTHESIS x ALLOCATION_PLANNING | 0 | 0 | ENRICHED->DEPLETED | NO->NO | MAIN_DIRECTION(non-core) |
| GENERATION_SYNTHESIS x INFORMATION_ACQUISITION | -1 | -2 | ENRICHED->ENRICHED | YES->YES | MAIN_COUNT+RAW_COUNT |
| GENERATION_SYNTHESIS x OPTION_GENERATION | 1 | 1 | ENRICHED->ENRICHED | NO->NO | MAIN_COUNT+RAW_COUNT |
| HUMAN_AUGMENTATION x GENERAL_DECISION_PROCESS | 1 | 1 | DEPLETED->DEPLETED | NO->NO | MAIN_COUNT+RAW_COUNT |
| HUMAN_AUGMENTATION x HUMAN_REVIEW_ACCOUNTABILITY | -1 | -2 | ENRICHED->ENRICHED | YES->YES | MAIN_COUNT+RAW_COUNT |
| HUMAN_AUGMENTATION x RISK_ASSESSMENT | 0 | 0 | DEPLETED->DEPLETED | NO->YES | CORE_MEMBERSHIP |
| PREDICTION_RISK_ESTIMATION x ALLOCATION_PLANNING | 3 | 3 | ENRICHED->ENRICHED | NO->NO | MAIN_COUNT+RAW_COUNT |
| PREDICTION_RISK_ESTIMATION x EVALUATION_SELECTION | 1 | 1 | DEPLETED->DEPLETED | YES->YES | MAIN_COUNT+RAW_COUNT |
| PREDICTION_RISK_ESTIMATION x GENERAL_DECISION_PROCESS | 2 | 2 | DEPLETED->DEPLETED | YES->YES | MAIN_COUNT+RAW_COUNT |
| PREDICTION_RISK_ESTIMATION x GOVERNANCE_OVERSIGHT | -1 | -1 | DEPLETED->DEPLETED | YES->YES | MAIN_COUNT+RAW_COUNT |
| PREDICTION_RISK_ESTIMATION x HUMAN_REVIEW_ACCOUNTABILITY | 1 | 1 | DEPLETED->DEPLETED | YES->YES | MAIN_COUNT+RAW_COUNT |
| PREDICTION_RISK_ESTIMATION x INFORMATION_ACQUISITION | 0 | -1 | DEPLETED->DEPLETED | YES->YES | RAW_COUNT |
| PREDICTION_RISK_ESTIMATION x PREDICTION_DIAGNOSIS | -6 | -14 | ENRICHED->ENRICHED | YES->YES | MAIN_COUNT+RAW_COUNT |
| PREDICTION_RISK_ESTIMATION x RISK_ASSESSMENT | 0 | -2 | ENRICHED->ENRICHED | YES->YES | RAW_COUNT |
| RECOMMENDATION_OPTIMIZATION x ALLOCATION_PLANNING | 0 | -1 | ENRICHED->ENRICHED | YES->YES | RAW_COUNT |
| RECOMMENDATION_OPTIMIZATION x EXECUTION_COORDINATION | 0 | 0 | ENRICHED->DEPLETED | NO->NO | MAIN_DIRECTION(non-core) |
| RECOMMENDATION_OPTIMIZATION x GENERAL_DECISION_PROCESS | -1 | -1 | ENRICHED->ENRICHED | YES->YES | MAIN_COUNT+RAW_COUNT |
| RECOMMENDATION_OPTIMIZATION x INFORMATION_SYNTHESIS | 1 | 1 | DEPLETED->DEPLETED | NO->NO | MAIN_COUNT+RAW_COUNT |
| RETRIEVAL_SYNTHESIS x INFORMATION_SYNTHESIS | 1 | 1 | ENRICHED->ENRICHED | YES->YES | MAIN_COUNT+RAW_COUNT |

### T4. Audited-record label changes that a full reanalysis would need to propagate (model label -> human label used by sidecar)

Source = RECONCILED_FINAL (HUMAN_RECONCILED_20.csv FINAL_C*) for the 20 blind-subset records, FIRST_CODER (FIRST_CODER_50_FINAL_FROZEN.csv human_*) for the other 30. Model side = current_ai_family / current_decision_family / model_analytical_pair_eligible in FIRST_CODER_50_FINAL_FROZEN.csv. Human C1 = evidence validity, C5 = analytical inclusion.

| # | record_id | validation_id | source | C1 | inclusion: model -> human C5 | AI family: model -> human | Decision family: model -> human |
|---|---|---|---|---|---|---|---|
| 1 | REC-A51A4D85E6A1A0AF | V5HV-0001 | FIRST_CODER | VALID | unchanged (INCLUDE) | PREDICTION_RISK_ESTIMATION -> GENERAL_REASONING_SYSTEMS | PREDICTION_DIAGNOSIS -> GENERAL_DECISION_PROCESS |
| 2 | REC-1C9D71BB7E968457 | V5HV-0002 | FIRST_CODER | VALID | unchanged (INCLUDE) | GENERATION_SYNTHESIS -> RECOMMENDATION_OPTIMIZATION | INFORMATION_ACQUISITION -> INFORMATION_SYNTHESIS |
| 3 | REC-3C503D6C847A0DD0 | V5HV-0003 | RECONCILED_FINAL | INVALID | ELIGIBLE -> EXCLUDE | HUMAN_AUGMENTATION -> UNMAPPED | HUMAN_REVIEW_ACCOUNTABILITY -> UNMAPPED |
| 4 | REC-9A32A2E4E36852A5 | V5HV-0004 | FIRST_CODER | UNCERTAIN | ELIGIBLE -> UNCERTAIN | COORDINATION_EXECUTION -> GENERAL_REASONING_SYSTEMS | unchanged (ALLOCATION_PLANNING) |
| 5 | REC-B3CDA030F0C9A616 | V5HV-0005 | RECONCILED_FINAL | VALID | unchanged (INCLUDE) | unchanged (PREDICTION_RISK_ESTIMATION) | unchanged (RISK_ASSESSMENT) |
| 6 | REC-B7630B94D9F15A51 | V5HV-0006 | RECONCILED_FINAL | VALID | unchanged (INCLUDE) | RECOMMENDATION_OPTIMIZATION -> PREDICTION_RISK_ESTIMATION | unchanged (ALLOCATION_PLANNING) |
| 7 | REC-B8D55C37D31125C1 | V5HV-0007 | RECONCILED_FINAL | VALID | ELIGIBLE -> EXCLUDE | EVALUATION_ASSESSMENT -> GENERATION_SYNTHESIS | unchanged (GOVERNANCE_OVERSIGHT) |
| 8 | REC-7693BA4D088450A6 | V5HV-0008 | FIRST_CODER | VALID | unchanged (INCLUDE) | unchanged (EXPLANATION_ASSURANCE) | unchanged (HUMAN_REVIEW_ACCOUNTABILITY) |
| 9 | REC-CD936FA07B55A64A | V5HV-0009 | RECONCILED_FINAL | UNCERTAIN | ELIGIBLE -> UNCERTAIN | unchanged (PREDICTION_RISK_ESTIMATION) | PREDICTION_DIAGNOSIS -> AMBIGUOUS |
| 10 | REC-2A911B2E56CEDE77 | V5HV-0010 | RECONCILED_FINAL | VALID | unchanged (INCLUDE) | unchanged (PREDICTION_RISK_ESTIMATION) | PREDICTION_DIAGNOSIS -> ALLOCATION_PLANNING |
| 11 | REC-8EDDBB84B724E332 | V5HV-0011 | RECONCILED_FINAL | VALID | unchanged (INCLUDE) | unchanged (PREDICTION_RISK_ESTIMATION) | unchanged (RISK_ASSESSMENT) |
| 12 | REC-BCAAD1A4EAF15072 | V5HV-0012 | FIRST_CODER | UNCERTAIN | ELIGIBLE -> UNCERTAIN | unchanged (PREDICTION_RISK_ESTIMATION) | PREDICTION_DIAGNOSIS -> AMBIGUOUS |
| 13 | REC-4956C4EEA1C34263 | V5HV-0013 | RECONCILED_FINAL | INVALID | ELIGIBLE -> EXCLUDE | PREDICTION_RISK_ESTIMATION -> UNMAPPED | unchanged (PREDICTION_DIAGNOSIS) |
| 14 | REC-5A018A194F5F6FE7 | V5HV-0014 | RECONCILED_FINAL | VALID | unchanged (INCLUDE) | PREDICTION_RISK_ESTIMATION -> HUMAN_AUGMENTATION | PREDICTION_DIAGNOSIS -> GENERAL_DECISION_PROCESS |
| 15 | REC-2DA085E8689DA4D7 | V5HV-0015 | FIRST_CODER | VALID | unchanged (INCLUDE) | unchanged (EXPLANATION_ASSURANCE) | PREDICTION_DIAGNOSIS -> EXECUTION_COORDINATION |
| 16 | REC-F4F9FD42810BB264 | V5HV-0016 | FIRST_CODER | INVALID | unchanged (INCLUDE) | EVALUATION_ASSESSMENT -> UNMAPPED | ALLOCATION_PLANNING -> GENERAL_DECISION_PROCESS |
| 17 | REC-20D02FC45BA3EBC9 | V5HV-0017 | FIRST_CODER | VALID | unchanged (INCLUDE) | PREDICTION_RISK_ESTIMATION -> RETRIEVAL_SYNTHESIS | PREDICTION_DIAGNOSIS -> INFORMATION_SYNTHESIS |
| 18 | REC-B01E29C3AE62CF49 | V5HV-0018 | RECONCILED_FINAL | INVALID | ELIGIBLE -> EXCLUDE | EXPLANATION_ASSURANCE -> UNMAPPED | HUMAN_REVIEW_ACCOUNTABILITY -> GOVERNANCE_OVERSIGHT |
| 19 | REC-B669CF799DCF5071 | V5HV-0019 | FIRST_CODER | UNCERTAIN | unchanged (INCLUDE) | EXPLANATION_ASSURANCE -> AMBIGUOUS | HUMAN_REVIEW_ACCOUNTABILITY -> UNMAPPED |
| 20 | REC-28FFF07C96F00DC6 | V5HV-0020 | RECONCILED_FINAL | UNCERTAIN | ELIGIBLE -> EXCLUDE | RECOMMENDATION_OPTIMIZATION -> UNMAPPED | GENERAL_DECISION_PROCESS -> UNMAPPED |
| 21 | REC-7A57BDABC8CFAAB0 | V5HV-0021 | FIRST_CODER | VALID | unchanged (INCLUDE) | PREDICTION_RISK_ESTIMATION -> EVALUATION_ASSESSMENT | RISK_ASSESSMENT -> PREDICTION_DIAGNOSIS |
| 22 | REC-D1918AC31B4298B7 | V5HV-0022 | RECONCILED_FINAL | UNCERTAIN | ELIGIBLE -> UNCERTAIN | unchanged (PREDICTION_RISK_ESTIMATION) | PREDICTION_DIAGNOSIS -> UNMAPPED |
| 23 | REC-1117261404B32531 | V5HV-0023 | FIRST_CODER | VALID | ELIGIBLE -> EXCLUDE | EVALUATION_ASSESSMENT -> AMBIGUOUS | GOVERNANCE_OVERSIGHT -> AMBIGUOUS |
| 24 | REC-E1CB08ED16F39BDA | V5HV-0024 | FIRST_CODER | VALID | unchanged (INCLUDE) | EXPLANATION_ASSURANCE -> GENERAL_REASONING_SYSTEMS | GOVERNANCE_OVERSIGHT -> EVALUATION_SELECTION |
| 25 | REC-ED4E3AF2744C2487 | V5HV-0025 | RECONCILED_FINAL | VALID | unchanged (INCLUDE) | unchanged (PREDICTION_RISK_ESTIMATION) | PREDICTION_DIAGNOSIS -> ALLOCATION_PLANNING |
| 26 | REC-CF2D5A712BD003B8 | V5HV-0026 | FIRST_CODER | VALID | unchanged (INCLUDE) | unchanged (PREDICTION_RISK_ESTIMATION) | RISK_ASSESSMENT -> PREDICTION_DIAGNOSIS |
| 27 | REC-55077784A7EF8572 | V5HV-0027 | FIRST_CODER | VALID | unchanged (INCLUDE) | unchanged (EXPLANATION_ASSURANCE) | GOVERNANCE_OVERSIGHT -> AMBIGUOUS |
| 28 | REC-ADEE530821FA395F | V5HV-0028 | FIRST_CODER | VALID | unchanged (INCLUDE) | PREDICTION_RISK_ESTIMATION -> COORDINATION_EXECUTION | PREDICTION_DIAGNOSIS -> INFORMATION_SYNTHESIS |
| 29 | REC-707582C33C994C97 | V5HV-0029 | FIRST_CODER | VALID | ELIGIBLE -> UNCERTAIN | COORDINATION_EXECUTION -> UNMAPPED | HUMAN_REVIEW_ACCOUNTABILITY -> EXECUTION_COORDINATION |
| 30 | REC-76C34BE83FB2B462 | V5HV-0030 | FIRST_CODER | INVALID | ELIGIBLE -> EXCLUDE | GENERATION_SYNTHESIS -> UNMAPPED | INFORMATION_ACQUISITION -> AMBIGUOUS |
| 31 | REC-96129FE2C2F7AD3C | V5HV-0031 | RECONCILED_FINAL | INVALID | ELIGIBLE -> EXCLUDE | PREDICTION_RISK_ESTIMATION -> UNMAPPED | unchanged (GOVERNANCE_OVERSIGHT) |
| 32 | REC-35EE38A942604940 | V5HV-0032 | FIRST_CODER | UNCERTAIN | ELIGIBLE -> UNCERTAIN | EVALUATION_ASSESSMENT -> AMBIGUOUS | EVALUATION_SELECTION -> INFORMATION_SYNTHESIS |
| 33 | REC-5DDC840F2BFCA0E1 | V5HV-0033 | FIRST_CODER | VALID | unchanged (INCLUDE) | unchanged (PREDICTION_RISK_ESTIMATION) | PREDICTION_DIAGNOSIS -> GENERAL_DECISION_PROCESS |
| 34 | REC-E646563D0E26CAEB | V5HV-0034 | FIRST_CODER | VALID | unchanged (INCLUDE) | unchanged (PREDICTION_RISK_ESTIMATION) | INFORMATION_ACQUISITION -> GENERAL_DECISION_PROCESS |
| 35 | REC-9760E2C3ABFFA5E2 | V5HV-0035 | FIRST_CODER | VALID | unchanged (INCLUDE) | PREDICTION_RISK_ESTIMATION -> AMBIGUOUS | PREDICTION_DIAGNOSIS -> GENERAL_DECISION_PROCESS |
| 36 | REC-86FBD6BDB51BF4AE | V5HV-0036 | RECONCILED_FINAL | INVALID | ELIGIBLE -> EXCLUDE | EXPLANATION_ASSURANCE -> UNMAPPED | GOVERNANCE_OVERSIGHT -> UNMAPPED |
| 37 | REC-40D604B0C4354B6E | V5HV-0037 | RECONCILED_FINAL | VALID | unchanged (INCLUDE) | PREDICTION_RISK_ESTIMATION -> AMBIGUOUS | PREDICTION_DIAGNOSIS -> EVALUATION_SELECTION |
| 38 | REC-4CAE4F76C91DA9B9 | V5HV-0038 | FIRST_CODER | INVALID | ELIGIBLE -> EXCLUDE | unchanged (EXPLANATION_ASSURANCE) | GOVERNANCE_OVERSIGHT -> AMBIGUOUS |
| 39 | REC-3722D0E89E3133AA | V5HV-0039 | RECONCILED_FINAL | VALID | unchanged (INCLUDE) | PREDICTION_RISK_ESTIMATION -> GENERATION_SYNTHESIS | PREDICTION_DIAGNOSIS -> OPTION_GENERATION |
| 40 | REC-AFE822A05CB7DA08 | V5HV-0040 | FIRST_CODER | VALID | unchanged (INCLUDE) | unchanged (PREDICTION_RISK_ESTIMATION) | PREDICTION_DIAGNOSIS -> EVALUATION_SELECTION |
| 41 | REC-750CB326F2DF2F99 | V5HV-0041 | RECONCILED_FINAL | VALID | unchanged (INCLUDE) | PREDICTION_RISK_ESTIMATION -> RECOMMENDATION_OPTIMIZATION | PREDICTION_DIAGNOSIS -> ALLOCATION_PLANNING |
| 42 | REC-747EC11D1298B80F | V5HV-0042 | FIRST_CODER | VALID | unchanged (INCLUDE) | EVALUATION_ASSESSMENT -> AMBIGUOUS | unchanged (GOVERNANCE_OVERSIGHT) |
| 43 | REC-0D720884574345B4 | V5HV-0043 | RECONCILED_FINAL | VALID | unchanged (INCLUDE) | unchanged (PREDICTION_RISK_ESTIMATION) | unchanged (RISK_ASSESSMENT) |
| 44 | REC-F5E7A89410E348AC | V5HV-0044 | FIRST_CODER | VALID | unchanged (INCLUDE) | unchanged (HUMAN_AUGMENTATION) | HUMAN_REVIEW_ACCOUNTABILITY -> AMBIGUOUS |
| 45 | REC-FA66625E3CADA17E | V5HV-0045 | FIRST_CODER | VALID | unchanged (INCLUDE) | unchanged (PREDICTION_RISK_ESTIMATION) | PREDICTION_DIAGNOSIS -> HUMAN_REVIEW_ACCOUNTABILITY |
| 46 | REC-E113A499A73FE8E7 | V5HV-0046 | RECONCILED_FINAL | INVALID | ELIGIBLE -> EXCLUDE | EVALUATION_ASSESSMENT -> PERCEPTION_EXTRACTION | EVALUATION_SELECTION -> UNMAPPED |
| 47 | REC-E2F91EEBD91DE5B9 | V5HV-0047 | FIRST_CODER | UNCERTAIN | ELIGIBLE -> UNCERTAIN | EXPLANATION_ASSURANCE -> COORDINATION_EXECUTION | GOVERNANCE_OVERSIGHT -> GENERAL_DECISION_PROCESS |
| 48 | REC-623C537A0844C12C | V5HV-0048 | FIRST_CODER | VALID | unchanged (INCLUDE) | unchanged (COORDINATION_EXECUTION) | ALLOCATION_PLANNING -> EXECUTION_COORDINATION |
| 49 | REC-05E380076B764F4D | V5HV-0049 | FIRST_CODER | VALID | ELIGIBLE -> EXCLUDE | PREDICTION_RISK_ESTIMATION -> AMBIGUOUS | PREDICTION_DIAGNOSIS -> AMBIGUOUS |
| 50 | REC-F08FD98EECDCDCC2 | V5HV-0050 | FIRST_CODER | INVALID | ELIGIBLE -> EXCLUDE | RECOMMENDATION_OPTIMIZATION -> AMBIGUOUS | ALLOCATION_PLANNING -> AMBIGUOUS |

### T5. First-coder frozen label vs reconciled FINAL label for the 20 blind-subset records

| record_id | resolution basis | reconciliation UTC | first-coder -> FINAL differences |
|---|---|---|---|
| REC-0D720884574345B4 | UNANIMOUS_PRE_ADJUDICATION | - | none |
| REC-28FFF07C96F00DC6 | HUMAN_ADJUDICATION | 2026-10-03T07:45:24.075240+00:00 | C3_ai: AMBIGUOUS -> UNMAPPED; C4_dec: AMBIGUOUS -> UNMAPPED |
| REC-2A911B2E56CEDE77 | HUMAN_ADJUDICATION | 2026-10-03T07:51:28.237980+00:00 | C4_dec: PREDICTION_DIAGNOSIS -> ALLOCATION_PLANNING |
| REC-3722D0E89E3133AA | HUMAN_ADJUDICATION | 2026-10-03T07:52:43.108609+00:00 | C3_ai: EVALUATION_ASSESSMENT -> GENERATION_SYNTHESIS; C4_dec: EXECUTION_COORDINATION -> OPTION_GENERATION |
| REC-3C503D6C847A0DD0 | HUMAN_ADJUDICATION | 2026-10-03T08:00:50.087250+00:00 | C1: VALID -> INVALID; C3_ai: COORDINATION_EXECUTION -> UNMAPPED; C4_dec: GENERAL_DECISION_PROCESS -> UNMAPPED; C5_incl: INCLUDE -> EXCLUDE |
| REC-40D604B0C4354B6E | HUMAN_ADJUDICATION | 2026-10-03T08:03:46.878164+00:00 | C4_dec: GENERAL_DECISION_PROCESS -> EVALUATION_SELECTION |
| REC-4956C4EEA1C34263 | HUMAN_ADJUDICATION | 2026-10-03T08:07:18.754861+00:00 | C1: UNCERTAIN -> INVALID; C3_ai: EVALUATION_ASSESSMENT -> UNMAPPED; C4_dec: INFORMATION_SYNTHESIS -> PREDICTION_DIAGNOSIS; C5_incl: UNCERTAIN -> EXCLUDE |
| REC-5A018A194F5F6FE7 | HUMAN_ADJUDICATION | 2026-10-03T08:10:10.152653+00:00 | C3_ai: PREDICTION_RISK_ESTIMATION -> HUMAN_AUGMENTATION; C4_dec: PREDICTION_DIAGNOSIS -> GENERAL_DECISION_PROCESS |
| REC-750CB326F2DF2F99 | HUMAN_ADJUDICATION | 2026-10-03T08:11:54.541326+00:00 | C3_ai: PREDICTION_RISK_ESTIMATION -> RECOMMENDATION_OPTIMIZATION; C4_dec: AMBIGUOUS -> ALLOCATION_PLANNING; C5_incl: UNCERTAIN -> INCLUDE |
| REC-86FBD6BDB51BF4AE | HUMAN_ADJUDICATION | 2026-10-03T08:12:49.509217+00:00 | C3_ai: AMBIGUOUS -> UNMAPPED; C4_dec: AMBIGUOUS -> UNMAPPED |
| REC-8EDDBB84B724E332 | HUMAN_ADJUDICATION | 2026-10-03T08:14:20.488476+00:00 | none |
| REC-96129FE2C2F7AD3C | HUMAN_ADJUDICATION | 2026-10-03T08:16:29.746133+00:00 | C1: VALID -> INVALID; C3_ai: AMBIGUOUS -> UNMAPPED; C5_incl: INCLUDE -> EXCLUDE |
| REC-B01E29C3AE62CF49 | HUMAN_ADJUDICATION | 2026-10-03T11:01:38.807529+00:00 | C4_dec: AMBIGUOUS -> GOVERNANCE_OVERSIGHT |
| REC-B3CDA030F0C9A616 | HUMAN_ADJUDICATION | 2026-10-03T11:02:36.723773+00:00 | C4_dec: PREDICTION_DIAGNOSIS -> RISK_ASSESSMENT |
| REC-B7630B94D9F15A51 | HUMAN_ADJUDICATION | 2026-10-03T11:03:52.856596+00:00 | C3_ai: RECOMMENDATION_OPTIMIZATION -> PREDICTION_RISK_ESTIMATION |
| REC-B8D55C37D31125C1 | HUMAN_ADJUDICATION | 2026-10-03T11:04:51.606680+00:00 | C1: INVALID -> VALID; C3_ai: EXPLANATION_ASSURANCE -> GENERATION_SYNTHESIS; C4_dec: AMBIGUOUS -> GOVERNANCE_OVERSIGHT; C5_incl: UNCERTAIN -> EXCLUDE |
| REC-CD936FA07B55A64A | HUMAN_ADJUDICATION | 2026-10-03T11:06:02.168805+00:00 | C1: VALID -> UNCERTAIN; C3_ai: COORDINATION_EXECUTION -> PREDICTION_RISK_ESTIMATION; C4_dec: EXECUTION_COORDINATION -> AMBIGUOUS; C5_incl: INCLUDE -> UNCERTAIN |
| REC-D1918AC31B4298B7 | HUMAN_ADJUDICATION | 2026-10-03T11:06:59.427196+00:00 | C1: VALID -> UNCERTAIN; C3_ai: HUMAN_AUGMENTATION -> PREDICTION_RISK_ESTIMATION; C4_dec: INFORMATION_ACQUISITION -> UNMAPPED; C5_incl: INCLUDE -> UNCERTAIN |
| REC-E113A499A73FE8E7 | HUMAN_ADJUDICATION | 2026-10-03T11:07:54.476288+00:00 | C3_ai: AMBIGUOUS -> PERCEPTION_EXTRACTION; C4_dec: AMBIGUOUS -> UNMAPPED |
| REC-ED4E3AF2744C2487 | HUMAN_ADJUDICATION | 2026-10-03T11:09:05.968909+00:00 | C3_ai: COORDINATION_EXECUTION -> PREDICTION_RISK_ESTIMATION; C4_dec: GENERAL_DECISION_PROCESS -> ALLOCATION_PLANNING |

## 6. Final status

Reproduction scope: membership sets, gained/lost cells, directions, 15/17 split, diff counts and G01–G16 status were reproduced from raw CSV rows and rule-checked against per-method q columns (CONFIRMED). The underlying q-values / null-model runs were not re-executed (no generating script in package; NOT_RECOVERED). STOP/conflict: none blocking; dating conflict (2026-09-29 label vs 2026-10-03 artifacts) and l.2268 wording flagged for v1.8.

LOCAL_SENSITIVITY_REPRODUCED=YES
G01_G16_REMOVAL_IN_LOCAL_SIDECAR=NONE
FULL_CORPUS_RERUN=NO
