# 36 — Recomputation of the frozen Study 1 baseline from raw V5 rows (sub-agent P, Task 2)

Date: 2026-10-14. All work here is descriptive recomputation from frozen rows: counts, set equality, within-document dedup, analytic E = k_a·k_d/M, and BH re-adjustment of the frozen p-values as a consistency check. I ran no null model, no resampling and no pipeline stage.

- Machine-readable output: `36_V5_BASELINE_RECOMPUTATION.json`, with 76 checks, per-G detail and W column diffs.
- Tool: `tools/P/p_task2_baseline_recompute.py` (`python -I`, stdlib, sqlite opened with `mode=ro&immutable=1`).
- V5 = `C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\04_V5_PRODUCTION_FREEZE\20260911_AI_DECISION_V5_PRODUCTION`.

**Result: 76/76 MATCH, 0 CONFLICT. There is no STOP.**

## Source files (sha256)

| Key | File | sha256 |
|---|---|---|
| REC | V5\09_ANALYTICAL_FREEZE\analytical_freeze_v2_20260918T132206Z\ANALYTICAL_FREEZE_RECORD_LEVEL.csv | fbb5f59286d308771d5db77b176abebab8ef851a896652a3807ebf6a4b335a8f |
| SIDE | …\ANALYTICAL_FREEZE_SIDE_LEVEL.csv | 7704e743610492961ee5e7342595096cc8bfaa500dbd1d9684e70c72a4d8574a |
| ELIG | …\ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv | 9ee5fd537fed2819c0ac7998d6a786cc8f90dd008ebc1758bb92c8e7487c2e92 |
| EXCL | …\ANALYTICAL_PAIR_EXCLUDED_RECORDS.csv | d53c5e955f4dec1e23a21250542a3879cd8a5fa1bb5109bfdedc12df615161f4 |
| CAN09 | …\ANALYTICAL_FREEZE_CANONICAL.json (manifest-verified) | 9a4e8fc2ca2a49642ac801888e571b44c157a6bd5b06fe5c1cbd9ff1a891867a |
| EDGES | V5\10_…\matrix_v1_20260918T132505Z\DOCUMENT_PAIR_EDGES_DEDUP.csv | 3ba370c1804960ed35880f87172114e2c14af98e2691848f6306f5fe5b1715a2 |
| CELLS | V5\14_…\data_pack_v1_20260922T010012Z\11_CELL_RESULTS_ALL_120.csv (manifest-verified) | b1f54c5684cca0ad9c688343ff8d5ccaef845d1f28b340fb773e82de64aed7b2 |
| OBS11 | V5\11_…\OBSERVED_MATRIX_10X12.csv | 8d71118e9aa32ee94c023019e04992b8f6ba28350961afc95febfb9c76a79b7a |
| CMP | V5\12_…\ROBUSTNESS_COMPARISON_120.csv | 1e30bf064887950ca9eef360b3c050c8d4db2b681dd163e607901872acdbfcb5 |
| CORE | V5\13_…\results_freeze_v1_20260919T080120Z\FINAL_ROBUST_CORE_32.csv | a43b4b5897bb8b1dabfe251aa52b95da8f35b6951c98ada7c92663291770bd50 |
| DEP | …\FINAL_ROBUST_DEPLETED.csv | 6e25d75c0504547e41871aad6b1927f6165856d5cb7ccb22321294e17ac10e6a |
| ENR | …\FINAL_ROBUST_ENRICHED.csv | 35be0dfb4cb5d936f0499bbc57a312567d22a4b83a5f376de15486178aee1349 |
| STAT | …\FINAL_ROBUST_STATUS_MATRIX_10X12.csv | 87febed538abc5dda6bccbdb7ea239ff8c8676cfc3620c082c0b4db1cf12ad84 |
| ATT | V5\14_…\data_pack_v1_20260922T010012Z\01_ATTRITION_AND_GATES.csv | 73a4391cc3def53080c3671ffeac90075c49fbbfac381bf50698a3387626a82b |
| GR | …\03_STAGE2_GROUNDING_DISTRIBUTION.csv | 14c593171d631ff3a6ff91e769dc5ff74539de3850227f01f7e26a1c31d94731 |
| DB | C:\NTUST_PAPER\LocalCorpusWorkbench\v5_production_app\data\workbench.sqlite (hash = V5 freeze report and all lineage) | 367e588ccf5a407c5d3e5ded474377cf3e0aa0fba693ad60f178174473b13cee |
| G | REPO\11_Priority_Gaps_Frozen_Export_G01_G16_v1_0_20261009.csv | 76a2a00c078ee10168e1f6aece6c26b7507cede0019045528f1fd8695d29209d |
| T132 | REPO\claude\r14_merge_v1_8_1_study1_freeze\current_artifacts\132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX_v1_8_1.csv | 6c7d350960a411be7e1e16d6f70c1ae25ea8f3af5c62035d3b2e2b7e4e35cf5c |
| WSENS | W\02_V9_HUMAN_VALIDATION\20260929_V9_HUMAN_VALIDATION\ROBUST_CORE_LOCAL_SENSITIVITY.csv | e3166ee183e18f340c539b983108e2c972d18b916672a62510a25638db8b5b59 |

## A. Core baseline numbers

| Number | Value recomputed | Source | Method | Status |
|---|---|---|---|---|
| Strict analytical records | **6,499** (6,499 unique record_id) | REC | row count / distinct | MATCH |
| Canonical JSON records = CSV records (doc, families, statuses per record) | 6,499, identical | CAN09 + REC | set and per-record compare | MATCH |
| Source-DB strict set (`passed_strict_filter=1`) = analytical-freeze record set | identical (6,499) | DB + REC | set equality | MATCH |
| Pair-eligible records | **3,125** (= FULLY_MAPPED set; both sides MAPPED) | REC; ELIG (3,125 rows, same set) | flag count, set equality | MATCH |
| Pair-excluded | 3,374 (EXCL rows; disjoint; union = 6,499); 51.9 % | REC, EXCL | partition | MATCH |
| Unique documents among pair-eligible | **783** | REC | distinct document_id | MATCH |
| Strict unique documents | 1,104 | REC | distinct document_id | MATCH |
| Document-level edges M | **2,180** (recomputed set equals the EDGES file set and the 10 canonical edge set; source_record_count sums to 3,125; collapsed 945) | REC → EDGES | distinct (doc, left/AI family, right/Decision family) | MATCH |
| Cells | **10 × 12 = 120** (left side ∈ AI families, right side ∈ Decision families for all 3,125 records) | REC, marginals | count | MATCH |
| Observed per cell, k_a, k_d, M | all 120 equal to recomputed values; OBS11 equal | CELLS, OBS11 | per-cell | MATCH |
| E = k_a·k_d/M, O/E | max abs diff 0 / 0 | CELLS | per-cell | MATCH |
| Primary q ≤ .05 | **47** | CELLS `q_bh_two_sided` | count | MATCH |
| Primary q ≤ .01 | **34** | CELLS | count | MATCH |
| BH(p_two_sided) vs frozen q | max abs diff 0 | CELLS | re-adjustment of frozen p | MATCH |
| Robust core | **32 = 16 enriched + 16 depleted** (rule: all of main_mc_q, exact_q, document_null_q, raw_q ≤ .05 and one direction) | CMP | rule applied | MATCH |
| Recomputed set = FINAL_ROBUST_CORE_32 (with direction) = DEP ∪ ENR = STAT = CELLS `final_result_class` | identical | CORE, DEP, ENR, STAT, CELLS | dict/set equality | MATCH |
| CMP `dedup_observed` / `raw_observed` vs recomputed (edges / raw eligible records) | all 120 equal | CMP | per-cell | MATCH |
| 13 run 075633Z core vs 080120Z | 32 rows, identical on all shared columns | 13 both | compare | MATCH |

## B. G01–G16 and O/E

| Check | Result | Status |
|---|---|---|
| G01–G16 set (REPO G csv) = V5 16 robust depleted (DEP) | 16 = 16, identical set | MATCH |
| Per-G Observed, k_a, k_d, M, E_analytic, O/E (4 dp), Null_Mean, and the 4 q values (4 dp, or `<0.0001` checked as an inequality) vs V5 | 16/16 rows equal | MATCH |
| 132 CSV `O (doc-level edges)`, `E analytic`, `O/E` vs V5 recomputed | 16/16 rows equal; every G cell in the V5 depleted set | MATCH |

Per-G O and O/E: G01 3/0.1159, G02 6/0.1335, G03 3/0.1788, G04 7/0.1832, G05 7/0.1860, G06 9/0.1963, G07 2/0.2052, G08 8/0.2205, G09 26/0.2921, G10 8/0.2949, G11 12/0.3027, G12 21/0.3077, G13 15/0.3447, G14 8/0.3892, G15 7/0.4273, G16 10/0.4695.

## C. W `ROBUST_CORE_LOCAL_SENSITIVITY.csv`: `official_*` columns vs V5 (all 120 rows)

- **Categorical and count columns: 0 mismatches.** The 12 columns compared were `official_observed`, `official_exact_observed`, `official_document_observed`, `official_raw_observed`, the 4 `official_*_direction` columns, `official_main_q05`, `official_main_q01`, `official_core_member` and `official_core_direction`.
- **q columns, max abs diff vs V5: 0.0** for `official_main_q`, `official_exact_q`, `official_document_q` and `official_raw_q`.
- `official_core_member = YES`: 32 rows.

The "official" side of the V9 sidecar is therefore exactly the V5 frozen baseline.

## D. Lineage numbers quoted in the v1.8.2 manuscript (L13/L29, §3.1–3.3, §4.1–4.2)

| Number | Recomputed | Source | Status |
|---|---|---|---|
| 2,118 source documents; 1,199 AI / 919 DECISION source groups | 2,118; 1,199/919 | DB `documents` | MATCH |
| 1,729 parsed / 388 not entered / 1 parse failure | status Done 1,729 / Skipped 388 / Failed 1; 1,729 docs with semantic records | DB | MATCH |
| 47,402 pages; 9,984 section spans | 47,402; 9,984 | DB | MATCH |
| 26,501 candidates and semantic records | 26,501; 26,501 | DB | MATCH |
| 20,002 excluded = 19,942 requires-review + 60 ambiguous-relation | 20,002 = 19,942 + 60 | DB | MATCH |
| 5,858 reader outputs; 2,117 integrator outputs | 5,858; 2,117 | DB | MATCH |
| Source-group strict yield: AI 5,620/20,621; DECISION 879/5,880 | identical | DB join | MATCH |
| 12,998 sides; 4,079 stage-1; 8,919 stage-2; 4,672 accepted; 8,751 mapped (67.3 %); 4,247 unmapped = 3,862 + 164 + 221 | identical | SIDE | MATCH |
| 2,501 partially mapped / 873 fully unresolved | identical | REC | MATCH |
| Strict relation-type shares: ENABLES 37.70, SUPPORTS 34.33, CONSTRAINS 11.29, INFORMS 7.82, GOVERNS 6.60, TRANSFORMS 2.18, ASSOCIATED_WITH 0.08 % | identical | REC | MATCH |
| `01_ATTRITION_AND_GATES.csv` n values (26,501 / 6,499 / 12,998 / 4,079 / 8,919 / 4,672 / 3,125 / 1,104 / 783 / 2,180 / 120 / 47 / 34 / 32) | all equal to recomputed values | ATT | MATCH |
| Stage-2 grounding 6,916 / 6,818 / 2,811 / 1,087 / 349 | equal to data-pack values | GR (hash-verified) | MATCH as read. **Not recomputed** from the Stage-2 sidecar sqlite |

Not checked, because the numbers are outside V5: the κ values (.561, .048–.180), 50 audited and 20 second-coded records, 19 reconciled disagreements, the re-segmentation counts 29/30, the 3 boundary-sensitive cells, the human-label substitution membership change (+1 depletion, −1 enrichment), and "12 of 37 protected inputs missing". These belong to the V9 human-validation package and the source-closure reports.

## E. Side note (not a core conflict)

The superseded pack `data_pack_v1_20260919T081003Z` has two directory files re-saved by a spreadsheet tool:

- `26_*` is value-identical to the original.
- `33_*` matches the original within a max relative diff of 5.0e-8 (precision truncation). Categorical values are equal.

The files the core uses are the hash-verified ones in 010012Z and stages 11 and 12. See 35 §3.

## Recommended status (evidence only; frozen status unchanged)

- Every core number was recomputed from raw V5 rows and agrees exactly with the frozen baseline: 6,499 / 3,125 / 783 / 2,180 / 120 / 47 (34) / 32 = 16+16 / G01–G16.
- The chain from the hash-verified production DB through to the data pack is SHA-256- and manifest-verified (35).
- The W official columns equal V5 exactly.

V5_BASELINE_REPRODUCED=YES
OFFICIAL_CORE_PROVENANCE=CONFIRMED
V5_DATA_PACK=RECOVERED
STRICT_RECORDS_6499=RECOMPUTED
DOCUMENTS_783=RECOMPUTED
