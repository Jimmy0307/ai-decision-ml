# 05 — LEGACY SOURCE BOUNDARY (`完整資料來源.zip`)

Run: V1.8 SOURCE-VERIFIED EVIDENCE CLOSURE — Phase 6 (legacy zip quarantine), sub-agent D. Date: 2026-10-14.
Scope: read-only audit of `W\03_LEGACY_FULL_SOURCE\完整資料來源\` (69 files) against the v1.7 candidate manuscript
`r14_merge_v1_7\130_MERGED_MASTER_THESIS_R14_TO_ENTERPRISE_v1_7_EVIDENCE_CONVERGED_CANDIDATE.md` (3,080 lines) and
`r14_merge_v1_7\128_CANONICAL_STATE.md`. No extracted file was modified; no code from inside W was executed.

Reproducibility (helper scripts, run with `python -I`):
- `C:\Users\user\AppData\Local\Temp\claude\C--NTUST-PAPER\b2185478-fbc8-4bee-8105-bb5557dd964b\scratchpad\v18\D\legacy_audit.py` — hashes every file, joins `01_FILE_INVENTORY.csv` (zip entry mtimes), classifies analysis family, extracts 1,403 distinctive numeric tokens from legacy text (decimals with >= 3 places, comma-grouped integers, percentages) plus the 27 legacy concept names, and greps v1.7 / 128 for them and for 37 method terms. Raw output: `...\v18\D\legacy_audit_result.json`.
- `...\v18\D\assemble.py` — builds this file from the JSON.

Source zip: `C:\NTUST_PAPER\read\generated_v2\完整資料來源.zip`, sha256 `138dbeac661fb39a0ab7f3fe84f312e332a9d8b64b5b47c399034bffd4c0d283`, 13,143,635 B, mtime 2026-05-06T15:11:55 (`00_INPUT_MANIFEST.csv`). All 69 extracted files re-hashed: 69/69 match `01_FILE_INVENTORY.csv`.

---

## 1. Summary

**The package is an earlier, separate body of work — CONFIRMED.** It is the April–May 2026 project
"AI 治理結構洞的自動化識別與優先序排列 — 一個基於大規模文獻計量的機器驅動方法" (automated identification and prioritisation of
structural holes in AI governance literature), built on a **2,003-paper** corpus with the pre-R14 `read/generated_v2` pipeline.
Its README is dated 2026-04-22 17:00:40; zip entry mtimes: 55 files 2026-04-22, 9 files 2026-05-05, 5 files 2026-05-06.

Analysis families present (all confirmed by file content, not only filenames):

1. **Structural-hole "gap_priority" ranking** of 27 AI-governance concepts (info-gap matrix, four-dimension maturity score, Tier-A/B/C = rank 1–10/11–20/21–27) with a 50,000-run Monte Carlo tier-stability test (seed 20260422; Tier-A mean retention 84.92 %, Jaccard mean 0.7452).
2. **Classical network metrics vs gap_priority** on a 27-node / 72-edge concept k-NN graph — betweenness, **Burt constraint**, bridging centrality; all Spearman rho in [-0.2552, -0.0202], none significant; 5,000-resample bootstrap CIs all include 0.
3. **Citation network + main path analysis (SPLC / SPNP)**: 2,003 papers, 1,981 resolved via Crossref/DOI (98.90 %), 714 in-corpus citation edges, 8-node main path (SPLC = SPNP); multi-path robustness 15,000 runs.
4. **PCA + factor analysis (FA)** on 34 yearly observations x 7 features: PC1 29.90 %, PC2 27.40 %, cumulative 57.30 %; FA varimax, 3 factors (Kaiser > 1).
5. **External validation** (independent OpenAlex: 27 shared concepts, rho = -0.1413, p = 0.4821) and **ablation** of gap_priority signals.
6. **Concept co-occurrence backbone** (top-30 % weight edges; hub "Decision-making Algorithms" degree 36) — 2026-05-06.
7. **Old thesis drafts** (`FINAL_THESIS_FORMAL_VERSION_2026-04-12.md` 2,507 lines; `..._Q1_CLEAN_VERSION.md`; `..._WITH_DELETION_MARKS.md`) and Q1 revision plans/progress reports (TASK1/TASK2, 2026-05-05).

Legacy internal-quality defects observed (reasons, beyond lineage, why nothing here may be merged):
- The SPLC/SPNP main path consists of computer-vision papers (AlexNet NIPS-2012 → ResNet 1512.03385 → … → Swin Transformer → 2304.08069), not AI-governance literature — the citation layer does not describe the stated corpus topic.
- `q1_upgrade_citation_multisource_mapping_2026-04-22.csv`: 209 of 2,003 rows have year > 2026 (max 2200), min year 0.
- `q1_upgrade_citation_edges_in_corpus_2026-04-22.csv`: 9 of 714 edges are self-loops (e.g. `1412_3555v1 → 1412_3555v1`).
- Inconsistent external-validation numbers inside the package: closeout summary rho = -0.1413, top-10 overlap 0.20; `visualization_dashboard_metrics_2026-04-22.csv` rho = -0.218, top-10 overlap 0.1.
- Inconsistent tier assignment: `structural_hole_marked_list_2026-04-22.md` uses 10/10/7 (MCDM and Risk_assessment = Tier-A); `Enhanced_Concept_Statistics_2026-05-06.csv` uses 6/13/8 (both = Tier-B).
- The package's own closeout states the effect evidence is weak (all bootstrap CIs include 0; independent external consistency weak).

Relationship to other lineages: the legacy thesis is not the R14 corpus (R14/v1.7 report 47,402 pages, 9,984 section spans, 26,501 candidates, 6,499 retained records, 22 function families, G01–G16); no R14 / V5 / G01–G16 figures appear in any legacy text file (incidental string hits only inside PNG bytes and bibliographic titles in the 11 MB mapping CSVs). Whether this package is the "V4 structural-hole layer" named in 128 §4 is **UNRESOLVED** (the V4 manuscript was not examined in this phase); it is at least the same structural-hole research line.

### Analysis-family file counts

| Analysis family | Files |
|---|---:|
| Structural-hole tier ranking + Monte Carlo | 12 |
| PCA/FA (yearly temporal features) | 11 |
| Citation network / main path (SPLC/SPNP) | 10 |
| Old thesis draft / revision plans | 9 |
| External validation (OpenAlex/temporal holdout) | 8 |
| QA / closeout / manifest | 4 |
| Concept co-occurrence backbone network | 4 |
| Classical network metrics (betweenness/Burt constraint) vs gap_priority | 4 |
| Ablation sensitivity of gap_priority | 3 |
| Info-gap / structural-hole priority + expert question bank | 3 |
| Package README | 1 |

---

## 2. File-by-file table (69 files)

Dates: "Filename date" is the date embedded in the file name; "Zip entry mtime" is from `01_FILE_INVENTORY.csv` (local-time zip entry timestamp). Filename dates can be older than content (README notes `info_gap_matrix_2026-04-11.csv` was recomputed 2026-04-22).

| # | Relative path (under 完整資料來源/) | sha256[:16] | Type | Size (B) | Analysis family | Filename date | Zip entry mtime | Inventory sha match |
|---:|---|---|---|---:|---|---|---|---|
| 1 | `README_完整資料來源.md` | `613c3532b5ec8782` | Markdown text | 742 | Package README | — | 2026-04-22T17:09:16 | YES |
| 2 | `可視化/ablation_sensitivity_2026-04-22.png` | `37b52621866e0935` | PNG figure | 55904 | Ablation sensitivity of gap_priority | 2026-04-22 | 2026-04-22T17:13:34 | YES |
| 3 | `可視化/external_validation_metrics_2026-04-22.png` | `e36eac701cadf740` | PNG figure | 31963 | External validation (OpenAlex/temporal holdout) | 2026-04-22 | 2026-04-22T17:13:34 | YES |
| 4 | `可視化/main_path_definition_2026-04-22.md` | `3fe76d8b670ffb82` | Markdown text | 636 | Citation network / main path (SPLC/SPNP) | 2026-04-22 | 2026-04-22T17:13:34 | YES |
| 5 | `可視化/main_path_steps_2026-04-22.csv` | `cfff5a2649c7f527` | CSV data | 1828 | Citation network / main path (SPLC/SPNP) | 2026-04-22 | 2026-04-22T17:13:34 | YES |
| 6 | `可視化/main_path_visualization_2026-04-22.png` | `153a902f469c94df` | PNG figure | 17505 | Citation network / main path (SPLC/SPNP) | 2026-04-22 | 2026-04-22T17:13:34 | YES |
| 7 | `可視化/multi_path_robustness_2026-04-22.csv` | `5f102be8af8d8df2` | CSV data | 646 | Citation network / main path (SPLC/SPNP) | 2026-04-22 | 2026-04-22T17:13:36 | YES |
| 8 | `可視化/multi_path_robustness_2026-04-22.png` | `376ca86804472d4b` | PNG figure | 74549 | Citation network / main path (SPLC/SPNP) | 2026-04-22 | 2026-04-22T17:13:36 | YES |
| 9 | `可視化/tier_migration_heatmap_2026-04-22.png` | `0e728f2e7f9cc70a` | PNG figure | 42178 | Structural-hole tier ranking + Monte Carlo | 2026-04-22 | 2026-04-22T17:13:34 | YES |
| 10 | `可視化/tier_migration_matrix_2026-04-22.csv` | `d74434ac05e8a850` | CSV data | 141 | Structural-hole tier ranking + Monte Carlo | 2026-04-22 | 2026-04-22T17:13:34 | YES |
| 11 | `可視化/tier_stability_retention_jaccard_2026-04-22.png` | `787e2a7358632c7a` | PNG figure | 27855 | Structural-hole tier ranking + Monte Carlo | 2026-04-22 | 2026-04-22T17:13:34 | YES |
| 12 | `可視化/top15_gap_priority_2026-04-22.png` | `cd61a2e3041792af` | PNG figure | 77384 | Structural-hole tier ranking + Monte Carlo | 2026-04-22 | 2026-04-22T17:13:34 | YES |
| 13 | `可視化/visualization_dashboard_metrics_2026-04-22.csv` | `0e72233cc5edb9bc` | CSV data | 519 | QA / closeout / manifest | 2026-04-22 | 2026-04-22T17:13:36 | YES |
| 14 | `圖片/pca_cumulative_explained_2026-04-12.png` | `d86a3cf9436c33a5` | PNG figure | 73835 | PCA/FA (yearly temporal features) | 2026-04-12 | 2026-04-22T13:59:30 | YES |
| 15 | `圖片/pca_loadings_heatmap_2026-04-12.png` | `bf5e0a9f90de86eb` | PNG figure | 79192 | PCA/FA (yearly temporal features) | 2026-04-12 | 2026-04-22T13:59:32 | YES |
| 16 | `圖片/pca_pc1_pc2_phase_scatter_2026-04-12.png` | `2f9cba7ccdca7ffb` | PNG figure | 81361 | PCA/FA (yearly temporal features) | 2026-04-12 | 2026-04-22T13:59:32 | YES |
| 17 | `圖片/pca_scree_plot_2026-04-12.png` | `364e954868d2b786` | PNG figure | 67413 | PCA/FA (yearly temporal features) | 2026-04-12 | 2026-04-22T13:59:30 | YES |
| 18 | `論文/figures/AI_Governance_Concept_Network_Enhanced_2026-05-06.png` | `2c599dcee8bbce4e` | PNG figure | 3001462 | Concept co-occurrence backbone network | 2026-05-06 | 2026-05-06T13:58:46 | YES |
| 19 | `論文/figures/backbone_multibranch_structure_report_2026-05-06.md` | `63ac6174e168e8f7` | Markdown text | 1190 | Concept co-occurrence backbone network | 2026-05-06 | 2026-05-06T13:31:34 | YES |
| 20 | `論文/figures/backbone_multibranch_structure_top90_2026-04-17.png` | `b28de6400f62e4f7` | PNG figure | 2238233 | Concept co-occurrence backbone network | 2026-04-17 | 2026-05-06T13:31:34 | YES |
| 21 | `論文/figures/Enhanced_Concept_Statistics_2026-05-06.csv` | `a8c35bfa75180ef8` | CSV data | 962 | Concept co-occurrence backbone network | 2026-05-06 | 2026-05-06T13:58:46 | YES |
| 22 | `論文/figures/structural_hole_tier_mc_migration_heatmap_2026-04-22.png` | `b0f9fa650cb654bb` | PNG figure | 51995 | Structural-hole tier ranking + Monte Carlo | 2026-04-22 | 2026-04-22T20:55:02 | YES |
| 23 | `論文/figures/structural_hole_tier_mc_retention_2026-04-22.png` | `cb9422fa17bf7fae` | PNG figure | 35868 | Structural-hole tier ranking + Monte Carlo | 2026-04-22 | 2026-04-22T20:55:02 | YES |
| 24 | `論文/figures/structural_hole_tier_mc_top_concepts_2026-04-22.png` | `0d254d5471006c0f` | PNG figure | 85995 | Structural-hole tier ranking + Monte Carlo | 2026-04-22 | 2026-04-22T20:55:02 | YES |
| 25 | `論文/FINAL_THESIS_FORMAL_VERSION_2026-04-12.md` | `6928e3d3db943a39` | Markdown text | 133665 | Old thesis draft / revision plans | 2026-04-12 | 2026-05-06T15:10:12 | YES |
| 26 | `論文/FINAL_THESIS_Q1_CLEAN_VERSION.md` | `edf0b45ccd52b4bc` | Markdown text | 10288 | Old thesis draft / revision plans | — | 2026-05-05T04:08:08 | YES |
| 27 | `論文/FINAL_THESIS_WITH_DELETION_MARKS.md` | `c2e04a33c18e0b28` | Markdown text | 16039 | Old thesis draft / revision plans | — | 2026-05-05T04:08:08 | YES |
| 28 | `論文/Q1_IMPROVEMENT_CHECKLIST.md` | `02b804fdf16b9150` | Markdown text | 9447 | Old thesis draft / revision plans | — | 2026-05-05T04:08:08 | YES |
| 29 | `論文/TASK1_CLASSICAL_METRICS_REPORT.md` | `e5d0a2e5bdc36d07` | Markdown text | 6779 | Classical network metrics (betweenness/Burt constraint) vs gap_priority | — | 2026-05-05T04:30:46 | YES |
| 30 | `論文/TASK1_EXECUTION_SUMMARY.md` | `f651d72f54f72ffb` | Markdown text | 6593 | Old thesis draft / revision plans | — | 2026-05-05T04:30:46 | YES |
| 31 | `論文/TASK2_INTERNAL_VALIDATION.md` | `b682deaf26d20f67` | Markdown text | 1657 | Old thesis draft / revision plans | — | 2026-05-05T04:33:30 | YES |
| 32 | `論文/TASK2_PLAN.md` | `93704fc77e1ba684` | Markdown text | 8871 | Old thesis draft / revision plans | — | 2026-05-05T04:54:42 | YES |
| 33 | `論文/TASK2_PROGRESS_REPORT.md` | `44c873c925e4213e` | Markdown text | 6392 | Old thesis draft / revision plans | — | 2026-05-05T04:54:42 | YES |
| 34 | `論文/TASK2_QUICK_PLAN.md` | `e9d09d5c9bff567c` | Markdown text | 2363 | Old thesis draft / revision plans | — | 2026-05-05T04:54:42 | YES |
| 35 | `輸出/expert_question_bank_2026-04-11.csv` | `235548c4b4854573` | CSV data | 9007 | Info-gap / structural-hole priority + expert question bank | 2026-04-11 | 2026-04-22T16:56:46 | YES |
| 36 | `輸出/fa_communalities_2026-04-12.csv` | `64c76e7e32c08224` | CSV data | 435 | PCA/FA (yearly temporal features) | 2026-04-12 | 2026-04-22T14:01:02 | YES |
| 37 | `輸出/fa_varimax_loadings_2026-04-12.csv` | `23a3a84181df666a` | CSV data | 591 | PCA/FA (yearly temporal features) | 2026-04-12 | 2026-04-22T14:01:02 | YES |
| 38 | `輸出/FINAL_CLOSEOUT_SUMMARY_2026-04-22.md` | `386a811cd3cdc28f` | Markdown text | 2830 | QA / closeout / manifest | 2026-04-22 | 2026-04-22T16:46:58 | YES |
| 39 | `輸出/Info_Gap_and_Expert_Plan_2026-04-11.md` | `9ebbf416b7ae9329` | Markdown text | 1729 | Info-gap / structural-hole priority + expert question bank | 2026-04-11 | 2026-04-22T16:56:46 | YES |
| 40 | `輸出/info_gap_matrix_2026-04-11.csv` | `f193a08a1e3b559a` | CSV data | 4870 | Info-gap / structural-hole priority + expert question bank | 2026-04-11 | 2026-04-22T16:56:46 | YES |
| 41 | `輸出/pca_components_full_2026-04-12.csv` | `ab699d517218ffd6` | CSV data | 476 | PCA/FA (yearly temporal features) | 2026-04-12 | 2026-04-22T14:01:02 | YES |
| 42 | `輸出/pca_fa_summary_2026-04-12.md` | `938f5d943c5fbb2f` | Markdown text | 1331 | PCA/FA (yearly temporal features) | 2026-04-12 | 2026-04-22T14:01:02 | YES |
| 43 | `輸出/pca_loadings_full_2026-04-12.csv` | `c1e34fe4a95a9c29` | CSV data | 1157 | PCA/FA (yearly temporal features) | 2026-04-12 | 2026-04-22T14:01:02 | YES |
| 44 | `輸出/pca_table_for_thesis_2026-04-12.md` | `81ca45750494dbd8` | Markdown text | 683 | PCA/FA (yearly temporal features) | 2026-04-12 | 2026-04-22T13:59:32 | YES |
| 45 | `輸出/q1_upgrade_ablation_report.md` | `2e7c05b009e78d84` | Markdown text | 895 | Ablation sensitivity of gap_priority | — | 2026-04-22T16:59:08 | YES |
| 46 | `輸出/q1_upgrade_ablation_results.csv` | `54b67918fb4cec4f` | CSV data | 528 | Ablation sensitivity of gap_priority | — | 2026-04-22T16:59:08 | YES |
| 47 | `輸出/q1_upgrade_citation_edges_in_corpus_2026-04-22.csv` | `d16ada5e845cd24a` | CSV data | 82244 | Citation network / main path (SPLC/SPNP) | 2026-04-22 | 2026-04-22T05:45:40 | YES |
| 48 | `輸出/q1_upgrade_citation_multisource_mapping_2026-04-22.csv` | `487fc8f41cbb05e2` | CSV data | 11647873 | Citation network / main path (SPLC/SPNP) | 2026-04-22 | 2026-04-22T05:45:40 | YES |
| 49 | `輸出/q1_upgrade_citation_multisource_mapping_phase2_2026-04-22.csv` | `f295e19d10bb67d7` | CSV data | 11647523 | Citation network / main path (SPLC/SPNP) | 2026-04-22 | 2026-04-22T13:32:02 | YES |
| 50 | `輸出/q1_upgrade_citation_splc_spnp_report_2026-04-22.md` | `70e1f282a63d289e` | Markdown text | 1574 | Citation network / main path (SPLC/SPNP) | 2026-04-22 | 2026-04-22T05:45:40 | YES |
| 51 | `輸出/q1_upgrade_citation_splc_spnp_summary_2026-04-22.json` | `8bef6b61ffcbe00a` | JSON data | 1558 | Citation network / main path (SPLC/SPNP) | 2026-04-22 | 2026-04-22T05:45:40 | YES |
| 52 | `輸出/q1_upgrade_error_taxonomy.md` | `01cd75ef3021d043` | Markdown text | 1632 | QA / closeout / manifest | — | 2026-04-22T15:39:40 | YES |
| 53 | `輸出/q1_upgrade_external_independent_openalex_2026-04-22.csv` | `90a96d187eee7ae3` | CSV data | 1549 | External validation (OpenAlex/temporal holdout) | 2026-04-22 | 2026-04-22T16:59:46 | YES |
| 54 | `輸出/q1_upgrade_external_independent_openalex_raw_2026-04-22.json` | `992dc3b39ac01336` | JSON data | 595 | External validation (OpenAlex/temporal holdout) | 2026-04-22 | 2026-04-22T16:59:46 | YES |
| 55 | `輸出/q1_upgrade_external_independent_openalex_report_2026-04-22.md` | `d8a7680a4b4ddee1` | Markdown text | 1127 | External validation (OpenAlex/temporal holdout) | 2026-04-22 | 2026-04-22T16:59:46 | YES |
| 56 | `輸出/q1_upgrade_external_validation_all_sources.csv` | `66859f85e3d2146b` | CSV data | 2155 | External validation (OpenAlex/temporal holdout) | — | 2026-04-22T16:59:08 | YES |
| 57 | `輸出/q1_upgrade_external_validation_all_sources_report.md` | `b67c3d760002e026` | Markdown text | 1476 | External validation (OpenAlex/temporal holdout) | — | 2026-04-22T16:59:08 | YES |
| 58 | `輸出/q1_upgrade_external_validation_report_independent_openalex.md` | `a46496dd5d1d7346` | Markdown text | 764 | External validation (OpenAlex/temporal holdout) | — | 2026-04-22T16:59:48 | YES |
| 59 | `輸出/q1_upgrade_external_validation_temporal_holdout_input.csv` | `d7c19917c25134fb` | CSV data | 1161 | External validation (OpenAlex/temporal holdout) | — | 2026-04-22T15:39:14 | YES |
| 60 | `輸出/q1_upgrade_network_baseline_comparison.csv` | `334156852fac1c20` | CSV data | 3971 | Classical network metrics (betweenness/Burt constraint) vs gap_priority | — | 2026-04-22T16:59:06 | YES |
| 61 | `輸出/q1_upgrade_network_baseline_report.md` | `b1f8206c40036a54` | Markdown text | 989 | Classical network metrics (betweenness/Burt constraint) vs gap_priority | — | 2026-04-22T16:59:06 | YES |
| 62 | `輸出/q1_upgrade_reproducibility_manifest.md` | `34940fbd86d84af1` | Markdown text | 1619 | QA / closeout / manifest | — | 2026-04-22T15:39:42 | YES |
| 63 | `輸出/q1_upgrade_uncertainty_report.md` | `cacfdf8c8519e428` | Markdown text | 904 | Classical network metrics (betweenness/Burt constraint) vs gap_priority | — | 2026-04-22T16:59:26 | YES |
| 64 | `輸出/structural_hole_marked_list_2026-04-22.md` | `8448a207bc1407c4` | Markdown text | 2682 | Structural-hole tier ranking + Monte Carlo | 2026-04-22 | 2026-04-22T16:57:32 | YES |
| 65 | `輸出/structural_hole_tier_mc_concept_probs_2026-04-22.csv` | `f0dcc07a4b77305e` | CSV data | 2269 | Structural-hole tier ranking + Monte Carlo | 2026-04-22 | 2026-04-22T16:56:48 | YES |
| 66 | `輸出/structural_hole_tier_mc_migration_2026-04-22.csv` | `8f86a792c88ff0e7` | CSV data | 254 | Structural-hole tier ranking + Monte Carlo | 2026-04-22 | 2026-04-22T16:56:48 | YES |
| 67 | `輸出/structural_hole_tier_mc_tier_summary_2026-04-22.csv` | `38afd81b85ca65d0` | CSV data | 353 | Structural-hole tier ranking + Monte Carlo | 2026-04-22 | 2026-04-22T16:56:48 | YES |
| 68 | `輸出/structural_hole_tier_monte_carlo_summary_2026-04-22.md` | `3b92084a862b8356` | Markdown text | 2070 | Structural-hole tier ranking + Monte Carlo | 2026-04-22 | 2026-04-22T16:56:48 | YES |
| 69 | `輸出/temporal_phase_yearly_pca_2026-04-12.csv` | `6574b025246b6e38` | CSV data | 9091 | PCA/FA (yearly temporal features) | 2026-04-12 | 2026-04-22T13:59:26 | YES |

---

## 3. Overlap / contamination check against v1.7 (130, 3,080 lines) and 128

### 3.1 Zero-hit terms and numbers (no trace of legacy results)

In 130 **and** 128: `main path`, `主路徑`, `SPLC`, `SPNP`, `SPC`, `PCA`, `主成分`, `factor analysis`, `因素分析`, `varimax`, `Kaiser`,
`citation network`, `引用網路`, `citation edge`, `Monte Carlo`, `gap_priority`, `Tier-A`, `Tier-B`, `info_gap`, `2,003`, `1,981`, `98.90`,
`714` (as a token), `29.90`, `57.30`, `-0.1413`, `0.9734`, `0.6468`, `bridging`, `betweenness` — all **0 hits**.
Of 1,403 distinctive numeric tokens extracted from legacy text files, only the generic/coincidental ones in §3.3 appear in 130; **0** appear in 128.
None of the 27 legacy concept labels appears as an analysis object in 130 (only common English words inside reference titles, §3.3).

### 3.2 Term hits in 130 and their classification

| Term | 130 lines | What the hit is | Verdict |
|---|---|---|---|
| 結構洞 (29) / structural hole (4) / Burt (31) | 21, 37, 57, 83, 174, 186, 190, 196, 234, 236, 238, 240, 244, 270, 354, 579, 583, 641, 716, 1677, 1679, 1685, 2184, 2218, 2228, 2232, 2234, 2240, 2304, 2338, 2358, 2380, 2386; refs 2396, 2436, 2438, 2440, 2442, 2630, 2719, 2720; errata 3041, 3049, 3058 | v1.7's own theoretical framing (Burt 1992/2004; Ahuja 2000; Fleming et al. 2007): "functional under-integration ≠ Burt-type structural hole ≠ enterprise problem". Line 583 states Burt constraint was **not** applied to the function-family network; line 2240 (Table 5-1) marks Burt-type structural hole as "未檢驗"; line 2338 says no Burt algorithm was pre-specified. Some Burt hits are author-name substrings (Burton-Jones, 270/2358/2630/2719/2720/3041/3049). | LEGITIMATE — theory/boundary statements; no legacy number, corpus, concept or tier is imported. Not an improper merge. |
| 骨幹 / backbone (v1.7 lines 579, 1677, 1685, 2184, 2380) | — | v1.7's exploratory "operational integration skeleton" built from its 16 robust over-representations (10 cross-component / 6 within-component; 0–14 under alternative skeletons). Legacy "backbone" is a top-30 %-weight concept co-occurrence graph of 27 governance concepts. | Same word, different construct and data — LEGITIMATE, not a merge. |
| 制約 (583) / constraint (31, 381, 722) | 583: Burt constraint explicitly *not* used; 31: English abstract; 381, 722: enterprise-model "hard constraint" (incident tolerance ē). | Unrelated to legacy Burt-constraint correlation (rho = -0.1890). LEGITIMATE. |
| 約束 (51, 254, 284, 474, 484, 2204, 2912) | Relation label "constrain" in the R14 semantic coding scheme and governance prose. | Unrelated. LEGITIMATE. |
| OpenAlex (2668, 2684, 2750, 3054, 3056, 3059) | OpenAlex used only to reconstruct reference abstracts for quotation verification (Appendix B, errata E30/E32/E35). | Not the legacy OpenAlex external-validation result. LEGITIMATE. |
| Jaccard (640, 749, 1439, 1447, 1589, 1593, 1742, 1746) | Jaccard of robust-cell sets across null models / evidence-unit re-segmentation (e.g. .853 at 1593) and V1 secondary-mechanism Jaccard (pending). | Legacy Jaccard (tier stability 0.7452 etc.) absent. LEGITIMATE. |
| AI 治理 (282, 332, 940, 2682, 2684, 2734) | IT/AI governance literature review and expert-panel qualifications. | Topic overlap only; no legacy result. LEGITIMATE. |

### 3.3 Numeric-token hits in 130 (all coincidental)

| Token | 130 lines | Context in v1.7 | Legacy source | Verdict |
|---|---|---|---|---|
| `5,000` | 573, 749, 1336, 1443 | Number of retained null-model states / V1 bootstrap draws | Legacy `FINAL_CLOSEOUT_SUMMARY` (5,000 bootstrap of concept-network correlations) | Coincidental round number; different analysis. Not a merge. |
| `20,000` | 1561, 1573 | κ bootstrap resamples (R14 human audit) | Legacy formal thesis | Coincidental. |
| `1.000` | 1728 | κ = α = 1.000 (AI A vs AI B agreement, 16/16) | Legacy theses / info-gap | Coincidental. |
| `0.000` / `0.0000` | 1908, 2746 | MaxRegret vertex 0.0000; "P < 0.00001" in a Kawamoto quote | Legacy formal thesis | Coincidental. |
| `0.1186`, `10.6028`, `10.1016`, `0.125`, `10.125` | 2398–2652 | Fragments of DOIs in the reference list | Legacy formal thesis references | Coincidental (DOI substrings). |
| Accountability / Fairness / Ethics / Governance | 63, 2560, 2590, 2734, 2752 | Words inside reference titles / prose | Legacy concept list | Coincidental. |

### 3.4 Hits in 128_CANONICAL_STATE.md

| 128 line | Content | Verdict |
|---|---|---|
| 15 | `完整資料來源.zip` listed as **ABSENT** and described as "V5 Manuscript Data Pack 本體". | **CONFLICT (labeling, non-blocking):** the zip now present (`C:\NTUST_PAPER\read\generated_v2\完整資料來源.zip`, sha256 138dbeac…) is *not* a V5 data pack; it is the April–May 2026 legacy structural-hole / citation / PCA-FA package. 128 §3's V5 cross-check was done against R14 + `04_G01_G16_FROZEN.csv`, not this zip, so no canonical number depends on it. The 128 description of this zip should be corrected in the v1.8 canonical state; any "V5 Data Pack" provenance must be sought elsewhere (status of a true V5 data pack: NOT_RECOVERED from this zip). |
| 80 | "V4 稿件 … 與 V4 結構洞層（不得恢復）" listed as historical provenance only. | Consistent with this boundary (same structural-hole line; exact identity with V4 layer UNRESOLVED). |

### 3.5 Result

- Improper merges of legacy results into v1.7: **0**.
- Legitimate theory/boundary mentions of structural holes / Burt in v1.7: present (§3.2) and already framed as *not tested* by the thesis.
- Coincidental numeric collisions: 10 tokens, all explained (§3.3).
- v1.7 never names `完整資料來源`; 128 names it once (line 15) with a wrong description (§3.4).

---

## 4. Classification and boundary

Classification: **LEGACY_HISTORICAL_PROVENANCE** — an earlier, methodologically distinct study (2,003-paper AI-governance corpus; gap_priority structural-hole tiers; citation main path SPLC/SPNP; PCA/FA; OpenAlex external validation) that precedes the R14 corpus and the G01–G16 robust-depletion analysis. It may be cited only as project history (e.g. "an earlier structural-hole prototype was abandoned"), never as evidence.

Rules binding on v1.8 and later:

DO_NOT_OVERRIDE_R14
DO_NOT_OVERRIDE_V5
DO_NOT_OVERRIDE_G01_G16
DO_NOT_MERGE_STRUCTURAL_HOLE_RESULTS

Operational meaning:
- No number, table, figure, tier, concept ranking, main path, PCA/FA loading or validation statistic from this package may enter the manuscript, appendices, canonical state, or enterprise model.
- The legacy `FINAL_THESIS_*` drafts are not authoritative despite the "FINAL" name (audit protocol: name confers no authority).
- The legacy Burt-constraint / betweenness correlations must not be used to upgrade v1.7's "Burt-type structural hole = 未檢驗" status.
- Any future reference to this zip must cite sha256 `138dbeac661fb39a0ab7f3fe84f312e332a9d8b64b5b47c399034bffd4c0d283` and this boundary file.
- Required follow-up (outside this phase): correct 128 line 15's description of `完整資料來源.zip`.

LEGACY_ZIP_CLASSIFICATION=LEGACY_HISTORICAL_PROVENANCE
