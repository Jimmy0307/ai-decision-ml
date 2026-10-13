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

