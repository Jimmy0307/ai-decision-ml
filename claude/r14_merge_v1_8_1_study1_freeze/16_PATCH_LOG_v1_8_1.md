# 16 — Patch log: v1.8 → v1.8.1 CLEANUP CANDIDATE (sub-agent J)

Date: 2026-10-14. No new analysis; no network, empirical, taxonomy, G01–G16, G→M, Enterprise-model or equation change. `SUBMISSION_READY = NO` is kept. No DOCX was built.

- **Input:** `claude/r14_merge_v1_8_source_closure/08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md`, sha256 `1515b0f241846b98a16bea7b13f07d1f82fa9199e1331c2228ffce1d04f7ad58` (asserted equal to the expected `1515b0f2…7ad58` before patching; unchanged).
- **Output:** `claude/r14_merge_v1_8_1_study1_freeze/16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.md`, sha256 `cddeb89b07439ff2bba9af1ba119824cb1cf815c4fc8a78e084900cd24e06bda`. Lines 3081 → 3086 (5 rows inserted in the Appendix D table after the 137 row; no line deleted). UTF-8, LF, no BOM.
- **Method:** 30 exact old→new replacements, each asserted to occur exactly once in v1.8 and at apply time (`tools/J/patch_v181.py`). Verification: `tools/J/verify_v181.py` → `tools/J/verify_out.json`. This log and 16b: `tools/J/build_log.py`. Run with `python -I`.
- **Authorities used:** 13 (segmentation attribution, §4 wording), 14 (G07/G15 WORDING_CONFIRMED), 12 (stale status), 15 (reanalysis governance), 17 (Study 1 freeze), 19 (V1 status READY_TO_RUN), V1.8 08_PATCH_LOG / 02 / 07.

## 1. Change list

| id | v1.8 line | v1.8.1 line | section | category | source |
|---|---|---|---|---|---|
| J01 | 5 | 5 | 稿件狀態 | status line (version label; Study 1 freeze; V1 packet READY_TO_RUN) | V1.8.1 17 §G; 19 L389 (V1_HUMAN_CONSTRUCT_VALIDATION_STATUS=READY_TO_RUN); this round |
| J02 | 5 | 5 | 稿件狀態 | FULL_REANALYSIS status wording | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology |
| J03 | 13 | 13 | 摘要 | FULL_REANALYSIS status wording | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology |
| J04 | 29 | 29 | Abstract | FULL_REANALYSIS status wording | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology |
| J05 | 122 | 122 | 1.4 研究問題 | FULL_REANALYSIS status wording | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology |
| J06 | 147 | 147 | 表 1-1 研究問題二 | FULL_REANALYSIS status wording | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology |
| J07 | 158 | 158 | 1.5 研究設計概覽 | FULL_REANALYSIS status pointer (provenance bracket only; G-token line) | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology |
| J08 | 168 | 168 | 1.6 推論邊界 | FULL_REANALYSIS status wording | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology |
| J09 | 405 | 405 | 3.1 研究設計 | FULL_REANALYSIS status wording | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology |
| J10 | 412 | 412 | 3.1 研究流程圖（文字流程） | FULL_REANALYSIS status wording | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology |
| J11 | 609 | 609 | 3.7.4 | FULL_REANALYSIS status wording | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology |
| J12 | 630 | 630 | 3.8.1 表 3-3（L2′ 列） | FULL_REANALYSIS status wording | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology |
| J13 | 1629 | 1629 | 4.5.5 | FULL_REANALYSIS status wording (status codes) | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology |
| J14 | 2183 | 2183 | 4.11 表（研究問題二） | FULL_REANALYSIS status wording | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology |
| J15 | 2190 | 2190 | 4.11 整合回答 | FULL_REANALYSIS status wording | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology |
| J16 | 2238 | 2238 | 5.3 表（功能低整合列） | FULL_REANALYSIS status wording | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology |
| J17 | 2362 | 2362 | 5.8.9 | FULL_REANALYSIS status wording (status codes) | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology |
| J18 | 2366 | 2366 | 5.9 後續研究 | FULL_REANALYSIS status wording (priority/executability qualifier) | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology |
| J19 | 2378 | 2378 | 5.10 結論 | FULL_REANALYSIS status wording | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology |
| J20 | 3064 | 3069 | 附錄 E E40 | FULL_REANALYSIS status wording (status codes) + input governance | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology; 15 §1-§2 (T4 only valid propagation source) |
| J21 | 3068 | 3073 | 附錄 E E44 | FULL_REANALYSIS status wording | V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology |
| J22 | 1577 | 1577 | 4.5.2 | source attribution (re-segmentation figures) | V1.8.1 13_SEGMENTATION_ATTRIBUTION_FORENSIC.md §0, §2 (recomputed from raw rows), §3, §4 proposed wording; V9/V9_1_SEGMENTATION_SENSITIVITY/SEGMENTATION_SENSITIVITY_FINAL_REPORT.md (2026-10-03T16:41:45Z) |
| J23 | 1603 | 1603 | 4.5.3 表 4-8 表註 | source attribution (re-segmentation figures) | V1.8.1 13_SEGMENTATION_ATTRIBUTION_FORENSIC.md §0, §2 (recomputed from raw rows), §3, §4 proposed wording; V9/V9_1_SEGMENTATION_SENSITIVITY/SEGMENTATION_SENSITIVITY_FINAL_REPORT.md (2026-10-03T16:41:45Z) |
| J24 | 1605 | 1605 | 4.5.3 | source pointer (G07/G15 boundary wording; WORDING_CONFIRMED, not changed) | V1.8.1 14_G07_G15_BOUNDARY_SENSITIVITY_AUDIT.md §0 (WORDING_CONFIRMED), §5 L1605, §6 |
| J25 | 2264 | 2264 | 5.4.2 | source attribution (re-segmentation figures) | V1.8.1 13_SEGMENTATION_ATTRIBUTION_FORENSIC.md §0, §2 (recomputed from raw rows), §3, §4 proposed wording; V9/V9_1_SEGMENTATION_SENSITIVITY/SEGMENTATION_SENSITIVITY_FINAL_REPORT.md (2026-10-03T16:41:45Z) |
| J26 | 2334 | 2334 | 5.8.3 | source attribution (re-segmentation figures) | V1.8.1 13_SEGMENTATION_ATTRIBUTION_FORENSIC.md §0, §2 (recomputed from raw rows), §3, §4 proposed wording; V9/V9_1_SEGMENTATION_SENSITIVITY/SEGMENTATION_SENSITIVITY_FINAL_REPORT.md (2026-10-03T16:41:45Z) |
| J27 | 2939 | 2939 | 附錄 D R14 列 | source attribution (re-segmentation figures) + stale R14 date provenance | V1.8.1 13_SEGMENTATION_ATTRIBUTION_FORENSIC.md §0, §2 (recomputed from raw rows), §3, §4 proposed wording; V9/V9_1_SEGMENTATION_SENSITIVITY/SEGMENTATION_SENSITIVITY_FINAL_REPORT.md (2026-10-03T16:41:45Z) §1.4 (inherited docProps timestamp) |
| J28 | 3008 | 3008 | 附錄 D V9 列 | source attribution (V9.1 availability) | V1.8.1 13_SEGMENTATION_ATTRIBUTION_FORENSIC.md §0, §2 (recomputed from raw rows), §3, §4 proposed wording; V9/V9_1_SEGMENTATION_SENSITIVITY/SEGMENTATION_SENSITIVITY_FINAL_REPORT.md (2026-10-03T16:41:45Z) |
| J29 | 3019 | 3019 | 附錄 D（版本與 V1.8.1 檔案列） | version history rows (v1.8, v1.8.1) | V1.8.1 OUT file list; 17; 19 L389 |
| J30 | 869 | 869 | 3.10.5 表（D07 列） | typo (missing closing parenthesis) | incidental typo scan (tools/J/typo_scan.py): unbalanced （ on v1.8 L869 |

### J01 — v1.8 L5 (v1.8.1 L5) — 稿件狀態
- **Category:** status line (version label; Study 1 freeze; V1 packet READY_TO_RUN)
- **Source:** V1.8.1 17 §G; 19 L389 (V1_HUMAN_CONSTRUCT_VALIDATION_STATUS=READY_TO_RUN); this round
- **Old:**
  > 合併碩士論文 v1.8 SOURCE-VERIFIED CANDIDATE（由 v1.7 修訂；v1.0–v1.7 保留、未覆寫；歷次版本說明移至附錄 F）。本版不新增任何分析，也不改變任何方程、模型元素、R14 數值或 G01–G16 凍結值；v1.7 已把既有證據的狀態收斂為一致的寫法，v1.8 再以 V9 人工驗證套件的原始檔案逐列核對其來源，只更新來源標示、日期與相應措辭。
- **New:**
  > 合併碩士論文 v1.8.1 CLEANUP CANDIDATE（由 v1.8 修訂；v1.0–v1.8 保留、未覆寫；v1.6 以前的版本說明見附錄 F，v1.7 以後的版本檔案見附錄 D）。本版不新增任何分析，也不改變任何方程、模型元素、R14 數值或 G01–G16 凍結值；v1.7 已把既有證據的狀態收斂為一致的寫法，v1.8 再以 V9 人工驗證套件的原始檔案逐列核對其來源；v1.8.1 只做清理：補上證據單元重切分數值的來源標示（V9.1 證據單元重切分敏感度側車分析，R14 轉述）、統一完整重分析的狀態寫法，並修正一處排版錯誤。同一輪另凍結文獻層（Study 1）的證據狀態（V1.8.1 檔案 17_STUDY1_EVIDENCE_FREEZE_v1.md），並備妥 V1 人類構念效度驗證封包（V1.8.1 檔案 19–21；狀態 READY_TO_RUN：已備妥、尚未執行，沒有任何人類編碼結果）。

### J02 — v1.8 L5 (v1.8.1 L5) — 稿件狀態
- **Category:** FULL_REANALYSIS status wording
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology
- **Old:**
  > V9 套件標記的完整重分析（FULL_REANALYSIS_REQUIRED）是否執行，仍為研究者待決事項（附錄 E40）；
- **New:**
  > V9 套件標記的完整重分析（FULL_REANALYSIS_REQUIRED）在方法上列為開放的驗證行動（REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION），但以目前的來源集無法執行（37 項受保護輸入中 12 項未尋回；NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET），在 V1 人類構念效度驗證之前不建議優先執行（NOT_RECOMMENDED）；日後是否重跑仍由研究者決定（附錄 E40）；

### J03 — v1.8 L13 (v1.8.1 L13) — 摘要
- **Category:** FULL_REANALYSIS status wording
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology
- **Old:**
  > 凍結的 32 組仍為正式推論基準，完整重分析是否執行仍待研究者決定。
- **New:**
  > 凍結的 32 組仍為正式推論基準；完整重分析列為開放的驗證行動，但以目前的來源集無法執行，在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定。

### J04 — v1.8 L29 (v1.8.1 L29) — Abstract
- **Category:** FULL_REANALYSIS status wording
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology
- **Old:**
  > and whether to run the full reanalysis flagged by the validation package remains an open researcher decision.
- **New:**
  > and the full reanalysis flagged by the validation package remains an open validation action: it cannot be executed with the currently recovered source set (12 of 37 protected inputs are missing), it is not recommended as a priority before the V1 human construct validation, and whether to rerun it later remains a researcher decision.

### J05 — v1.8 L122 (v1.8.1 L122) — 1.4 研究問題
- **Category:** FULL_REANALYSIS status wording
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology
- **Old:**
  > 局部敏感，完整重分析尚待執行（第 4.5.5 節）。
- **New:**
  > 局部敏感；完整重分析列為開放的驗證行動，但以目前的來源集無法執行，在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（第 4.5.5 節；附錄 E40）。

### J06 — v1.8 L147 (v1.8.1 L147) — 表 1-1 研究問題二
- **Category:** FULL_REANALYSIS status wording
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology
- **Old:**
  > 局部成員變動，完整重分析待執行 |
- **New:**
  > 局部成員變動；完整重分析為開放驗證行動，以目前來源集無法執行，V1 前不建議優先執行（附錄 E40） |

### J07 — v1.8 L158 (v1.8.1 L158) — 1.5 研究設計概覽
- **Category:** FULL_REANALYSIS status pointer (provenance bracket only; G-token line)
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology
- **Old:**
  > 完整重分析是否執行仍待研究者決定（第 4.5.5 節）〔來源：V9 人工驗證套件（資料夾 20260929_V9_HUMAN_VALIDATION；V9 是檔案版本名，不是驗證閘門）之 FINAL_STATUS.json（驗證時間 2026-10-03）與 ROBUST_CORE_LOCAL_SENSITIVITY.csv；已逐列核對；附錄 E39〕
- **New:**
  > 完整重分析是否執行仍待研究者決定（第 4.5.5 節）〔來源：V9 人工驗證套件（資料夾 20260929_V9_HUMAN_VALIDATION；V9 是檔案版本名，不是驗證閘門）之 FINAL_STATUS.json（驗證時間 2026-10-03）與 ROBUST_CORE_LOCAL_SENSITIVITY.csv；已逐列核對；附錄 E39；完整重分析的現行狀態（開放驗證行動、以目前來源集無法執行、V1 前不建議優先執行）見附錄 E40〕

### J08 — v1.8 L168 (v1.8.1 L168) — 1.6 推論邊界
- **Category:** FULL_REANALYSIS status wording
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology
- **Old:**
  > 完整重分析尚待執行（第 4.5.5 節），逐格解讀因此依證據強度分層。
- **New:**
  > 完整重分析列為開放的驗證行動，但以目前的來源集無法執行，在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（第 4.5.5 節；附錄 E40）；逐格解讀因此依證據強度分層。

### J09 — v1.8 L405 (v1.8.1 L405) — 3.1 研究設計
- **Category:** FULL_REANALYSIS status wording
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology
- **Old:**
  > 完整重分析尚待執行（第 3.7.4、4.5.5 節）。
- **New:**
  > 完整重分析列為開放的驗證行動，但以目前的來源集無法執行，在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（第 3.7.4、4.5.5 節；附錄 E40）。

### J10 — v1.8 L412 (v1.8.1 L412) — 3.1 研究流程圖（文字流程）
- **Category:** FULL_REANALYSIS status wording
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology
- **Old:**
  > 凍結核心仍為推論基準；完整重分析待執行）
- **New:**
  > 凍結核心仍為推論基準；完整重分析為開放驗證行動，目前無法執行）

### J11 — v1.8 L609 (v1.8.1 L609) — 3.7.4
- **Category:** FULL_REANALYSIS status wording
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology
- **Old:**
  > 依該檔，完整重分析須經研究者核准；是否在投稿前執行，仍為研究者待決事項（附錄 E40）。
- **New:**
  > 依該檔，完整重分析須經研究者核准；其現行狀態為：方法上列為 V9 的開放驗證行動，以目前的來源集無法執行（37 項受保護輸入中 12 項未尋回），在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（附錄 E40）。

### J12 — v1.8 L630 (v1.8.1 L630) — 3.8.1 表 3-3（L2′ 列）
- **Category:** FULL_REANALYSIS status wording
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology
- **Old:**
  > 不取代 L2；完整重分析待研究者決定〔
- **New:**
  > 不取代 L2；完整重分析為開放驗證行動，以目前來源集無法執行，V1 前不建議優先執行（附錄 E40）〔

### J13 — v1.8 L1629 (v1.8.1 L1629) — 4.5.5
- **Category:** FULL_REANALYSIS status wording (status codes)
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology
- **Old:**
  > 最後一項是套件的狀態標記；依 FINAL_STATUS.json，完整重分析須經研究者核准，是否執行仍為研究者待決事項（附錄 E40）。
- **New:**
  > 最後一項是套件的狀態標記；依 FINAL_STATUS.json，完整重分析須經研究者核准。其現行狀態為：方法上列為 V9 的開放驗證行動（FULL_REANALYSIS_METHOD_STATUS = REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION）；以目前的來源集無法執行（37 項受保護輸入中 12 項未尋回；FULL_REANALYSIS_EXECUTION_STATUS = NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET）；在 V1 人類構念效度驗證之前不建議優先執行（FULL_REANALYSIS_PRIORITY_BEFORE_V1 = NOT_RECOMMENDED）；日後是否重跑仍由研究者決定（附錄 E40）。

### J14 — v1.8 L2183 (v1.8.1 L2183) — 4.11 表（研究問題二）
- **Category:** FULL_REANALYSIS status wording
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology
- **Old:**
  > 凍結的 32 組仍為推論基準，完整重分析待研究者決定〔
- **New:**
  > 凍結的 32 組仍為推論基準；完整重分析為開放驗證行動，以目前來源集無法執行，V1 前不建議優先執行（附錄 E40）〔

### J15 — v1.8 L2190 (v1.8.1 L2190) — 4.11 整合回答
- **Category:** FULL_REANALYSIS status wording
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology
- **Old:**
  > （人工標籤替換顯示局部成員敏感，完整重分析待執行）
- **New:**
  > （人工標籤替換顯示局部成員敏感；完整重分析為開放驗證行動，以目前來源集無法執行，見附錄 E40）

### J16 — v1.8 L2238 (v1.8.1 L2238) — 5.3 表（功能低整合列）
- **Category:** FULL_REANALYSIS status wording
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology
- **Old:**
  > 另新增一組不足呈現，待完整重分析 |
- **New:**
  > 另新增一組不足呈現；完整重分析為開放驗證行動，以目前來源集無法執行（附錄 E40） |

### J17 — v1.8 L2362 (v1.8.1 L2362) — 5.8.9
- **Category:** FULL_REANALYSIS status wording (status codes)
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology
- **Old:**
  > （V9 套件標記為 FULL_REANALYSIS_REQUIRED；是否及何時執行仍待研究者決定，附錄 E40）
- **New:**
  > （V9 套件標記為 FULL_REANALYSIS_REQUIRED；現行狀態：FULL_REANALYSIS_METHOD_STATUS = REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION，FULL_REANALYSIS_EXECUTION_STATUS = NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET，FULL_REANALYSIS_PRIORITY_BEFORE_V1 = NOT_RECOMMENDED；日後是否及何時重跑仍由研究者決定，附錄 E40）

### J18 — v1.8 L2366 (v1.8.1 L2366) — 5.9 後續研究
- **Category:** FULL_REANALYSIS status wording (priority/executability qualifier)
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology
- **Old:**
  > 以一致的標籤完成文獻層的完整重分析（第 5.8.9 節）
- **New:**
  > 以一致的標籤完成文獻層的完整重分析（第 5.8.9 節；執行前須先尋回缺件的受保護輸入，時程排在 V1 人類構念效度驗證之後，見附錄 E40）

### J19 — v1.8 L2378 (v1.8.1 L2378) — 5.10 結論
- **Category:** FULL_REANALYSIS status wording
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology
- **Old:**
  > ，完整重分析尚待執行。
- **New:**
  > ；完整重分析列為開放的驗證行動，但以目前的來源集無法執行（附錄 E40）。

### J20 — v1.8 L3064 (v1.8.1 L3069) — 附錄 E E40
- **Category:** FULL_REANALYSIS status wording (status codes) + input governance
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology; 15 §1-§2 (T4 only valid propagation source)
- **Old:**
  > | V9 套件記為須經研究者核准；作者決定在投稿前或投稿後執行；
- **New:**
  > | 現行狀態：FULL_REANALYSIS_METHOD_STATUS = REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；FULL_REANALYSIS_EXECUTION_STATUS = NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET（套件受保護基準 37 項輸入中 12 項未尋回，E39（b））；FULL_REANALYSIS_PRIORITY_BEFORE_V1 = NOT_RECOMMENDED（V1.8 檔案 07 §8；V1.8.1 檔案 15、17）。V9 套件記為須經研究者核准；日後是否及何時重跑仍由研究者決定；重跑時的標籤輸入只能取自 V1.8 檔案 04 表 T4（V1.8.1 檔案 15）；

### J21 — v1.8 L3068 (v1.8.1 L3073) — 附錄 E E44
- **Category:** FULL_REANALYSIS status wording
- **Source:** V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology
- **Old:**
  > 完整重分析待決（E40）
- **New:**
  > 完整重分析為開放驗證行動且以目前來源集無法執行（E40）

### J22 — v1.8 L1577 (v1.8.1 L1577) — 4.5.2
- **Category:** source attribution (re-segmentation figures)
- **Source:** V1.8.1 13_SEGMENTATION_ATTRIBUTION_FORENSIC.md §0, §2 (recomputed from raw rows), §3, §4 proposed wording; V9/V9_1_SEGMENTATION_SENSITIVITY/SEGMENTATION_SENSITIVITY_FINAL_REPORT.md (2026-10-03T16:41:45Z)
- **Old:**
  > 主要零模型的高於／低於期望方向分別有 12 與 11 格改變。
- **New:**
  > 主要零模型的高於／低於期望方向分別有 12 與 11 格改變〔來源：V9.1 證據單元重切分敏感度側車分析（V9 套件 `V9_1_SEGMENTATION_SENSITIVITY`，2026-10-03 產生；以凍結之主要分析為比較基準），R14 定稿第 4.6.2–4.6.3 節轉述；觀察值改變與方向改變格數已由兩種設定之文獻層級邊逐列重算核對〕。

### J23 — v1.8 L1603 (v1.8.1 L1603) — 4.5.3 表 4-8 表註
- **Category:** source attribution (re-segmentation figures)
- **Source:** V1.8.1 13_SEGMENTATION_ATTRIBUTION_FORENSIC.md §0, §2 (recomputed from raw rows), §3, §4 proposed wording; V9/V9_1_SEGMENTATION_SENSITIVITY/SEGMENTATION_SENSITIVITY_FINAL_REPORT.md (2026-10-03T16:41:45Z)
- **Old:**
  > 三種設定共同保留的穩健配對沒有方向反轉。
- **New:**
  > 三種設定共同保留的穩健配對沒有方向反轉。句層級與句與子句層級兩列（含觀察值改變 84/120、85/120 與主測方向改變 12/120、11/120）取自 V9.1 證據單元重切分敏感度側車分析（V9 套件 `V9_1_SEGMENTATION_SENSITIVITY` 之 `S1_120_CELL_RESULTS.csv`、`S2_120_CELL_RESULTS.csv` 與 `SEGMENTATION_CELL_COUNT_DIFF.csv`；2026-10-03），以凍結之主要分析為比較基準；R14 定稿表 7 轉述。

### J24 — v1.8 L1605 (v1.8.1 L1605) — 4.5.3
- **Category:** source pointer (G07/G15 boundary wording; WORDING_CONFIRMED, not changed)
- **Source:** V1.8.1 14_G07_G15_BOUNDARY_SENSITIVITY_AUDIT.md §0 (WORDING_CONFIRMED), §5 L1605, §6
- **Old:**
  > 五個變動位置列於表 4-9。
- **New:**
  > 五個變動位置列於表 4-9（成員判定的來源同表 4-8 表註）。

### J25 — v1.8 L2264 (v1.8.1 L2264) — 5.4.2
- **Category:** source attribution (re-segmentation figures)
- **Source:** V1.8.1 13_SEGMENTATION_ATTRIBUTION_FORENSIC.md §0, §2 (recomputed from raw rows), §3, §4 proposed wording; V9/V9_1_SEGMENTATION_SENSITIVITY/SEGMENTATION_SENSITIVITY_FINAL_REPORT.md (2026-10-03T16:41:45Z)
- **Old:**
  > 84–85/120 格的觀察值發生變化，
- **New:**
  > 84–85/120 格的觀察值發生變化（V9.1 證據單元重切分敏感度側車分析；見第 4.5.2–4.5.3 節），

### J26 — v1.8 L2334 (v1.8.1 L2334) — 5.8.3
- **Category:** source attribution (re-segmentation figures)
- **Source:** V1.8.1 13_SEGMENTATION_ATTRIBUTION_FORENSIC.md §0, §2 (recomputed from raw rows), §3, §4 proposed wording; V9/V9_1_SEGMENTATION_SENSITIVITY/SEGMENTATION_SENSITIVITY_FINAL_REPORT.md (2026-10-03T16:41:45Z)
- **Old:**
  > 12 與 11 格的主要零模型方向改變，
- **New:**
  > 12 與 11 格的主要零模型方向改變（V9.1 側車分析，見第 4.5.2 節），

### J27 — v1.8 L2939 (v1.8.1 L2939) — 附錄 D R14 列
- **Category:** source attribution (re-segmentation figures) + stale R14 date provenance
- **Source:** V1.8.1 13_SEGMENTATION_ATTRIBUTION_FORENSIC.md §0, §2 (recomputed from raw rows), §3, §4 proposed wording; V9/V9_1_SEGMENTATION_SENSITIVITY/SEGMENTATION_SENSITIVITY_FINAL_REPORT.md (2026-10-03T16:41:45Z) §1.4 (inherited docProps timestamp)
- **Old:**
  > 全部文獻層數值的權威來源 |
- **New:**
  > 全部文獻層數值的權威來源；其中第 3.7.3 節與第 4.5 節之證據單元重切分數值，原始分析出處為 V9.1 證據單元重切分敏感度側車分析（2026-10-03），R14 定稿（2026-10-04 起之修訂）其後納入並轉述。R14 docx 中繼資料之 2026-09-20 修改時間為範本沿用值，不代表成稿日期 |

### J28 — v1.8 L3008 (v1.8.1 L3008) — 附錄 D V9 列
- **Category:** source attribution (V9.1 availability)
- **Source:** V1.8.1 13_SEGMENTATION_ATTRIBUTION_FORENSIC.md §0, §2 (recomputed from raw rows), §3, §4 proposed wording; V9/V9_1_SEGMENTATION_SENSITIVITY/SEGMENTATION_SENSITIVITY_FINAL_REPORT.md (2026-10-03T16:41:45Z)
- **Old:**
  > 第 3.7.4、4.5.5、5.4.2、5.8.9 節；已逐列核對（附錄 E39） |
- **New:**
  > 第 3.7.4、4.5.5、5.4.2、5.8.9 節；已逐列核對（附錄 E39）；套件內 `V9_1_SEGMENTATION_SENSITIVITY` 為證據單元重切分敏感度側車分析之機器可讀來源（第 3.7.3、4.5 節） |

### J29 — v1.8 L3019 (v1.8.1 L3019) — 附錄 D（版本與 V1.8.1 檔案列）
- **Category:** version history rows (v1.8, v1.8.1)
- **Source:** V1.8.1 OUT file list; 17; 19 L389
- **Old:**
  > | 137 | — | `137_NEXT_ACTIONS.md` | 投稿前的關鍵路徑 | 附錄 E39–E48 |
- **New:**
  > | 137 | — | `137_NEXT_ACTIONS.md` | 投稿前的關鍵路徑 | 附錄 E39–E48 |
  > | v1.8／08 | — | `08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md` | 合併論文 v1.8（V9 來源核對版） | v1.8.1 的修訂底稿（已保存；未覆寫） |
  > | v1.8.1／13 | — | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 證據單元重切分數值的出處鑑識（由原始列重算） | 第 4.5.2–4.5.3、5.4.2、5.8.3 節的來源標示 |
  > | v1.8.1／16 | — | `16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.md` | 合併論文 v1.8.1（清理版） | 本稿 |
  > | v1.8.1／17 | — | `17_STUDY1_EVIDENCE_FREEZE_v1.md` | 文獻層（Study 1）證據凍結 | 稿件狀態；附錄 E40 |
  > | v1.8.1／19–21 | — | `19_V1_HUMAN_CONSTRUCT_VALIDATION_PROTOCOL.md`、`20_V1_HUMAN_CONSTRUCT_VALIDATION_PACKET.xlsx`、`21_V1_HUMAN_CONSTRUCT_VALIDATION_CODEBOOK.md` | V1 人類構念效度驗證協定、封包與編碼手冊（READY_TO_RUN；尚未執行） | 稿件狀態；第 4.7.3 節 |

### J30 — v1.8 L869 (v1.8.1 L869) — 3.10.5 表（D07 列）
- **Category:** typo (missing closing parenthesis)
- **Source:** incidental typo scan (tools/J/typo_scan.py): unbalanced （ on v1.8 L869
- **Old:**
  > **決定工程資源的結構**（與 D06 合併判定 |
- **New:**
  > **決定工程資源的結構**（與 D06 合併判定） |

## 2. Verification (script output: `tools/J/verify_out.json`)

### 2.1 Math, fences, headings
- `$$` blocks 18 → 18; inline `$…$` 31 → 31; `\[…\]` 7 → 7. Byte-identical in order: {'$$': True, '$inline': True, '\\[\\]': True, 'begin_env': True}.
- Changed lines containing math markers: none.
- Fenced blocks 4 → 4; changed fence index [1] = the text flow chart at v1.8 L407–418 (J10, L412, status words only; no equation). All other fences identical.
- Headings: 182 → 182, identical in order and text: True.

### 2.2 G01–G16 lines
- v1.8 lines containing a G01–G16 token: 122. Whole-document G-token count 288 → 288. `G## → M#` tokens identical: True. Inserted Appendix D rows contain no G token: True.
- `VCP` count 28 → 28
- `VSC` count 26 → 26
- `DL` count 59 → 59
- `NEV` count 28 → 28
- `SIMULATED_ONLY` count 31 → 31
- `EMPIRICAL RESULT PENDING` count 69 → 69
- `HUMAN RESULT PENDING` count 46 → 46
- `UNIDENTIFIED` count 44 → 44
- Changed G-token lines (segment diff):
  - **v1.8 L5** — G tokens identical: True; all changes inside a provenance bracket 〔…〕: False.
    - L5 is the manuscript status line, which the task mandates rewriting (allowed changes 2 and 3: version label, FULL_REANALYSIS status, Study 1 freeze, V1 READY_TO_RUN). Its G-token segment 「或 G01–G16 凍結值」 is byte-identical; no G content, membership or assignment is touched. This is the only G-line change outside a provenance bracket. Merged segments:
    - OLD: 「 SOURCE-VERIFIED」 → NEW: 「.1 CLEANUP」
    - OLD: 「7」 → NEW: 「8」
    - OLD: 「7」 → NEW: 「8」
    - OLD: 「歷次版本說明移至附錄 F」 → NEW: 「v1.6 以前的版本說明見附錄 F，v1.7 以後的版本檔案見附錄 D」
    - OLD: 「，只更新來源標示、日期與相應措辭」 → NEW: 「；v1.8.1 只做清理：補上證據單元重切分數值的來源標示（V9.1 證據單元重切分敏感度側車分析，R14 轉述）、統一完整重分析的狀態寫法，並修正一處排版錯誤。同一輪另凍結文獻層（Study 1）的證據狀態（V1.8.1 檔案 17_STUDY1_EVIDENCE_FREEZE_v1.md），並備妥 V1 人類構念效度驗證封包（V1.8.1 檔案 19–21；狀態 READY_TO_RUN：已備妥、尚未執行，沒有任何人類編碼結果）」
    - OLD: 「是否執行，仍為研究者待決事項」 → NEW: 「在方法上列為開放的驗證行動（REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION），但以目前的來源集無法執行（37 項受保護輸入中 12 項未尋回；NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET），在 V1 人類構念效度驗證之前不建議優先執行（NOT_RECOMMENDED）；日後是否重跑仍由研究者決定」
  - **v1.8 L158** — G tokens identical: True; all changes inside a provenance bracket 〔…〕: True.
    - OLD: 「」 → NEW: 「；完整重分析的現行狀態（開放驗證行動、以目前來源集無法執行、V1 前不建議優先執行）見附錄 E40」

### 2.3 Numeric tokens
- Removed from the document: none.
- Added to the document (multiset): `{"04": 1, "07": 1, "08": 2, "1": 2, "11/120": 1, "12": 5, "12/120": 1, "13": 2, "15": 2, "16": 2, "17": 4, "19": 3, "20": 1, "2026-09-20": 1, "2026-10-03": 3, "2026-10-04": 1, "21": 3, "3.7.3": 2, "37": 5, "4-8": 1, "4.5": 2, "4.5.2": 3, "4.5.3": 2, "4.6.2": 1, "4.6.3": 1, "4.7.3": 1, "5.4.2": 1, "5.8.3": 1, "7": 1, "8": 1, "84/120": 1, "85/120": 1}`. Per-patch sum equals document delta: True.
- Justification per patch (no network or empirical number was added, removed or changed):
  - **J01** +{"1": 1, "17": 1, "19": 1, "21": 1} −{}: "1" = Study 1; "17", "19", "21" = V1.8.1 file numbers (17 evidence freeze; 19–21 V1 packet). Labels, not network/empirical values.
  - **J02** +{"37": 1, "12": 1} −{}: "12", "37" = 12 of 37 protected V9 inputs not recovered (V1.8 02 §5; already stated in v1.8 E39(b)). Provenance count, not a network/empirical value.
  - **J04** +{"12": 1, "37": 1} −{}: same as J02 (12 of 37 protected inputs).
  - **J11** +{"37": 1, "12": 1} −{}: same as J02.
  - **J13** +{"37": 1, "12": 1} −{}: same as J02.
  - **J20** +{"37": 1, "12": 1, "07": 1, "8": 1, "15": 2, "17": 1, "04": 1} −{}: "12", "37" as J02; "04", "07", "15", "17" = file numbers; "8" = memo §8.
  - **J22** +{"2026-10-03": 1, "4.6.2": 1, "4.6.3": 1} −{}: "2026-10-03" = V9.1 run date (13 §3); "4.6.2", "4.6.3" = R14 section numbers.
  - **J23** +{"84/120": 1, "85/120": 1, "12/120": 1, "11/120": 1, "2026-10-03": 1, "7": 1} −{}: "84/120", "85/120", "12/120", "11/120" repeat the unchanged Table 4-8 values on the same table (v1.8 L1600–1601; recomputed from raw rows in 13 §2); "2026-10-03" = V9.1 date; "7" = R14 Table 7.
  - **J24** +{"4-8": 1} −{}: "4-8" = table reference.
  - **J25** +{"4.5.2": 1, "4.5.3": 1} −{}: "4.5.2", "4.5.3" = section references.
  - **J26** +{"4.5.2": 1} −{}: "4.5.2" = section reference.
  - **J27** +{"3.7.3": 1, "4.5": 1, "2026-10-03": 1, "2026-10-04": 1, "2026-09-20": 1} −{}: "3.7.3", "4.5" = section references; "2026-10-03" V9.1 date; "2026-10-04" first manuscript import of V9.1 (13 §3); "2026-09-20" = inherited docProps timestamp (13 §1.4).
  - **J28** +{"3.7.3": 1, "4.5": 1} −{}: "3.7.3", "4.5" = section references.
  - **J29** +{"08": 2, "13": 2, "4.5.2": 1, "4.5.3": 1, "5.4.2": 1, "5.8.3": 1, "16": 2, "17": 2, "1": 1, "19": 2, "21": 2, "20": 1, "4.7.3": 1} −{}: File numbers 08/13/16/17/19/20/21, "1" (Study 1), section references 4.5.2/4.5.3/5.4.2/5.8.3/4.7.3.

### 2.4 Forbidden and remaining strings (v1.8.1)
- `2026-09-29 紀錄，待核`: 0 hits 
- `FULL_REANALYSIS_NOT_REQUIRED`: 0 hits 
- `not required`: 0 hits 
- `Not required`: 0 hits 
- `NOT_REQUIRED`: 0 hits 
- `不需要完整重分析`: 0 hits 
- `無需完整重分析`: 0 hits 
- `不須完整重分析`: 0 hits 
- `2026-09-29`: 0 hits 
- `完整資料來源` (legacy zip): v1.8 0, v1.8.1 0 — the manuscript never names the legacy zip (confirms V1.8 §2.8 and 12 Task C), so no legacy-identity edit.
- Full-reanalysis codes in v1.8.1: {'REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION': 4, 'NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET': 4, 'NOT_RECOMMENDED': 4, 'FULL_REANALYSIS_REQUIRED': 5}. `FULL_REANALYSIS_REQUIRED` is kept only as the V9 package's own label (L5, L1629, L2362, E39, E40).
- Remaining `待核` and related markers:
  - `待核`: 1 hits at v1.8.1 lines [3050] — 「Vial, 2019 的內容待核對」 (E21; reference verification, outside V9/segmentation scope; OPEN_SOURCE_NOT_FOUND in V1.8). Kept.
  - `研究者待決事項`: 0 hits at v1.8.1 lines []
  - `尚待執行`: 0 hits at v1.8.1 lines []
  - `待執行`: 0 hits at v1.8.1 lines []
  - `AUTHOR TO CONFIRM`: 2 hits at v1.8.1 lines [605, 3077] — E48 residual: label→pair-eligibility propagation rule UNRESOLVED and sidecar generator NOT_RECOVERED (V1.8 04 Q4; 15 §3 PROPAGATION_RULE_STATUS=UNRESOLVED_MUST_BE_PREDECLARED). Kept.
  - `工作環境中`: 2 hits at v1.8.1 lines [651, 3075] — L651 V5 Data Pack original (REAL_V5_DATA_PACK=NOT_RECOVERED, 12 Task C) and E46 submission-format files (OPEN_SOURCE_NOT_FOUND). Both still true; kept.

## 3. Deliberately not changed
1. **L158 body text** (「完整重分析是否執行仍待研究者決定」) is on a G-token line; only its provenance bracket was extended with a pointer to E40 (J07), per the G-line rule. The body clause is not contradicted by the current status (future rerun remains a researcher decision).
2. **Conditional / methodological uses** of 完整重分析 (v1.8 L605, L607, L619, L645, L1638, L1640, L2268, L3063, L3072) describe what the full reanalysis is or what holds *until* it is done; they state no execution status and are consistent with METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION. L645 and L1638 also carry G tokens.
3. **Re-segmentation numbers**: 84/85 of 120, 12/11, 29/32, 30/32, 31 (15/16), 3,112/6,499, 742/765, q-counts — unchanged. Only attribution was added (J22, J23, J25, J26, J27, J28). 742/765 are not recomputed (13 §5); the tag at J22 claims verification only for the observed- and direction-change counts.
4. **G07/G15** (14: both WORDING_CONFIRMED): no wording change; one source pointer added next to the Table 4-9 reference (J24). The optional precision sentence in 14 §5 was not added (it would add new numeric tokens).
5. **Appendix F** is a block of preserved status paragraphs for v1.0–v1.6, not a version table, and its heading 「v1.0–v1.6」 must stay identical. Following the V1.8 precedent (08_PATCH_LOG §4 item 8), F is unchanged; v1.8 and v1.8.1 were added as rows in the Appendix D artifact/version table (J29), and the status line now says where v1.7+ versions are listed.
6. **L651** (V5 Data Pack provenance) stays OPEN; consistent with REAL_V5_DATA_PACK=NOT_RECOVERED. No `完整資料來源` mention exists.
7. **Typos**: the scan (`tools/J/typo_scan.py`: doubled characters, doubled punctuation, unbalanced brackets) found one real typo, v1.8 L869 missing 「）」 (J30). Other hits were false positives (e.g., 直接接口, 驗證證據, 出版版本, interval notation `(0, 1]`, wrapped ASCII diagram brackets).
8. 132 / 128 / 131 / 133 / 137 artifacts and the V1.8 folder are not edited.

## 4. STOP conditions
None triggered: all replacements matched exactly once; no 84–85/120 number-vs-source conflict (13 §2); no G07/G15 or G01–G16 conflict (14); no κ or enterprise-model change.
