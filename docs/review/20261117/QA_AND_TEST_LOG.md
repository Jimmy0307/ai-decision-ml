# QA_AND_TEST_LOG｜2026-11-18 指令與輸出

所有指令以 `python -I`（隔離模式）執行。原始研究 ZIP 以 Python 分批解壓至審查機器的暫存目錄（未進入 repo）；下列 `<extract>` 代表該目錄。

## 1. 審查包完整性

```text
$ python -I checks/verify_bundle.py
PACKAGE_INPUT_CHECKS_PASS: 7 required files, 12 references, 20 methods, 13 versions, repo identity guard
# LIGHT_MANIFEST.json: 40 entries, 40 SHA-256 match, 0 missing, 0 mismatch
# 6 source ZIPs: whole-file SHA-256 match SOURCE_ARCHIVE_MANIFEST.csv (6/6)
# member files: 920 + 25 + 9 + 7 + 69 = 1,030 (+32 master-audit members); 1,030/1,030 match ALL_ARCHIVE_MEMBERS_SHA256.csv
```

## 2. 獨立重算

```text
$ python -I tools/review_20261117/audit_recompute.py --v9-dir <extract>/20260929_V9_HUMAN_VALIDATION       --gap-dir <extract>/AI_DECISION_GAP_VALIDITY_V1 --scout-dir <extract>/AI_DECISION_LIMITATION_SCOUT_V0_1       --out docs/review/20261117/RECOMPUTE_RESULTS.json
# 輸出全文：RECOMPUTE_RESULTS.json（只含聚合計數與輸入檔 SHA-256）

$ python -I tools/review_20261117/build_metric_audit.py --repo .
grades {'DIRECT': 55, 'HISTORICAL': 16, 'USER_REPORTED': 17, 'SYNTHETIC': 2}
results {'CONFIRMED_IN_SOURCE_TEXT': 6, 'CONFIRMED': 51, 'NOT_INDEPENDENTLY_VERIFIABLE': 33}
mismatches []
```

## 3. 側車測試重跑（審查包原始程式，於隔離 venv 的複本中執行）

```text
$ cd <copy>/AI_DECISION_GAP_VALIDITY_V1/tests && python -m unittest -v test_gap_validity
test_104_observed (test_gap_validity.TestGapValidity.test_104_observed) ... ok
test_10x12 (test_gap_validity.TestGapValidity.test_10x12) ... ok
test_alt_paths (test_gap_validity.TestGapValidity.test_alt_paths) ... ok
test_backbone_cross_counts (test_gap_validity.TestGapValidity.test_backbone_cross_counts) ... ok
test_baseline_core_16_16 (test_gap_validity.TestGapValidity.test_baseline_core_16_16) ... ok
test_bipartite_no_triad_terms (test_gap_validity.TestGapValidity.test_bipartite_no_triad_terms) ... ok
test_bipartite_no_triangles (test_gap_validity.TestGapValidity.test_bipartite_no_triangles) ... ok
test_censoring_analytic_sensitivity (test_gap_validity.TestGapValidity.test_censoring_analytic_sensitivity) ... ok
test_censoring_toy_full_data_not_exclusive (test_gap_validity.TestGapValidity.test_censoring_toy_full_data_not_exclusive) ... ok
test_generated_report_reproducible (test_gap_validity.TestGapValidity.test_generated_report_reproducible) ... ok
test_projected_triangles_are_derived (test_gap_validity.TestGapValidity.test_projected_triangles_are_derived) ... ok
test_segmentation_retention (test_gap_validity.TestGapValidity.test_segmentation_retention) ... ok
test_source_integrity (test_gap_validity.TestGapValidity.test_source_integrity) ... ok
test_synthetic_degree_identical (test_gap_validity.TestGapValidity.test_synthetic_degree_identical) ... ok

----------------------------------------------------------------------
Ran 14 tests in 0.390s

OK

$ cd <copy>/AI_DECISION_LIMITATION_SCOUT_V0_1/tests && python -m unittest -v test_scout
# 第一次（未安裝 PyMuPDF）：Ran 8 tests ... OK (skipped=1)  — test_pdf_pages skipped 'PyMuPDF absent'
# 安裝 PyMuPDF 後重跑：
Ran 8 tests ... OK
```

註：Gap Validity 測試會重新產生 `outputs/results.json`；重產檔與原檔位元組不同但 **0 個欄位值差異**（逐欄比較）。

## 4. 審查工具單元測試

```text
$ python -I -W error::ResourceWarning -m unittest discover -s tools/review_20261117 -p "test_*.py" -v
test_all_significant_same_direction (test_review_tools.CoreRuleTests.test_all_significant_same_direction) ... ok
test_boundary_q_equal_005_counts (test_review_tools.CoreRuleTests.test_boundary_q_equal_005_counts) ... ok
test_direction_disagreement (test_review_tools.CoreRuleTests.test_direction_disagreement) ... ok
test_one_not_significant (test_review_tools.CoreRuleTests.test_one_not_significant) ... ok
test_hand_computed_example (test_review_tools.KappaTests.test_hand_computed_example) ... ok
test_perfect_and_degenerate (test_review_tools.KappaTests.test_perfect_and_degenerate) ... ok
test_metric_audit_has_no_mismatch (test_review_tools.PublishedArtifactTests.test_metric_audit_has_no_mismatch) ... ok
test_recompute_identities (test_review_tools.PublishedArtifactTests.test_recompute_identities) ... ok
test_duplicate_ids_and_unwrapped_table (test_review_tools.QaDetectorTests.test_duplicate_ids_and_unwrapped_table) ... ok
test_overclaim_negation_window (test_review_tools.QaDetectorTests.test_overclaim_negation_window) ... ok
test_secret_and_path_guards (test_review_tools.QaDetectorTests.test_secret_and_path_guards) ... ok
test_unclosed_div (test_review_tools.QaDetectorTests.test_unclosed_div) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.015s

OK
```

## 5. 網站 QA gate

```text
$ python -I tools/review_20261117/qa_site.py --repo . --base origin/main
PASS  docs/index.html: well-formed tags
PASS  docs/index.html: no duplicate id
PASS  docs/index.html: relative href/anchor targets exist
PASS  docs/index.html: lang+title+viewport                                                            lang=zh-Hant
PASS  docs/index.html: every table wrapped in .table-scroll (mobile)
PASS  docs/index.html: no affirmative overclaims
PASS  docs/THEORY_LITERATURE_COMPARISON_20261117.html: well-formed tags
PASS  docs/THEORY_LITERATURE_COMPARISON_20261117.html: no duplicate id
PASS  docs/THEORY_LITERATURE_COMPARISON_20261117.html: relative href/anchor targets exist
PASS  docs/THEORY_LITERATURE_COMPARISON_20261117.html: lang+title+viewport                            lang=zh-Hant
PASS  docs/THEORY_LITERATURE_COMPARISON_20261117.html: every table wrapped in .table-scroll (mobile)
PASS  docs/THEORY_LITERATURE_COMPARISON_20261117.html: no affirmative overclaims
PASS  index: responsive @media rule present
PASS  index: table#versions has 13 rows                                                               got 13
PASS  index: table#methods-table has 20 rows                                                          got 20
PASS  index: table#metrics has 90 rows                                                                got 90
PASS  index: table#core-table has 32 rows                                                             got 32
PASS  index: table#refs-table has 12 rows                                                             got 12
PASS  index: table#formula-table has 8 rows                                                           got 8
PASS  index: original sections preserved
PASS  index: search/filter function preserved
PASS  index: required status labels visible
PASS  theory: 12 references R01�VR12
PASS  theory: 8 equations E1�VE8
PASS  docs/data/VERSION_METHOD_REGISTER_20261117.csv: 13 rows                                         got 13
PASS  docs/data/METHOD_VALIDATION_MATRIX_20261117.csv: 20 rows                                        got 20
PASS  docs/data/ALL_METRICS_WITH_PROVENANCE_20261117.csv: 90 rows                                     got 90
PASS  docs/data/LITERATURE_METHODS_20261117.csv: 12 rows                                              got 12
PASS  docs/review/20261117/METRIC_AUDIT_90.csv: 90 rows                                               got 90
PASS  docs/review/20261117/BIBLIOGRAPHY_VERIFICATION.csv: 12 rows                                     got 12
PASS  review deliverables present
PASS  correction log: schema + before/after recorded                                                  62 rows
PASS  diff: no raw archives/fulltexts/binaries added
PASS  diff: no file > 1 MB
PASS  diff: no secrets / work email / local user paths
PASS  diff: no LEM2/DRSA/recruitment paths touched
PASS  git diff --check (whitespace)

37/37 gates PASS
```

## 6. 手機寬度實際渲染

以 headless Chrome 將 `docs/index.html` 與 `docs/THEORY_LITERATURE_COMPARISON_20261117.html` 嵌入 390px 寬 iframe 截圖檢視：文字正常換行、無頁面水平捲動；寬表格在 `.table-scroll` 容器內水平捲動。（註：headless Chrome 直接設定 390px 視窗時，實際 layout viewport 被限制為 504px，故改用 iframe 方式。）

## 7. 已知限制

- QA gate 為靜態檢查（HTML 結構、連結、計數、措辭、diff 範圍），不是 W3C validator；未在實體手機上測試。
- 側車測試只驗證方法與工具，不是 V11.1、V6–V10.1 或 V9 全量重跑。
