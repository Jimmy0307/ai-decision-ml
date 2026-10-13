# 12 — Stale Status Cleanup: 128 / 131 / 133 / 137 (V1.8.1, sub-agent H, Tasks B + C)

Date: 2026-10-14. Historical files in `W\01_ALL_OUTPUTS\AI_DECISION_THESIS_ALL_OUTPUTS\r14_merge_v1_7\` were read only and are unchanged. Each current copy in `current_artifacts/` carries a header with the source path, the sha256 and "current copy; history preserved".

## Files

| Historical file | sha256 (historical) | Current copy | sha256 (current) | Edits |
|---|---|---|---|---|
| `128_CANONICAL_STATE.md` | `4d807997232858c6930c78f8cc8b1c2738bc0f7a16ebd89528e497aa99d7a698` | `current_artifacts/128_CANONICAL_STATE_v1_8_1.md` | `9ade926fcf8777e1f5a38e21c97612ba9670cb8c6fcb9a6b192f3a3406e76dde` | 23 |
| `131_HUMAN_VALIDATION_INTEGRATION_REPORT.md` | `d47ee7632758a66571d498a6b350892aaac28ca3e7d97d34157c99bce30db891` | `current_artifacts/131_HUMAN_VALIDATION_INTEGRATION_REPORT_v1_8_1.md` | `b8a7adda3355a9815f7f1af53e7f59a46d12055d4909cd2e091b02df6b434592` | 17 |
| `133_V0_V7_VALIDATION_LEDGER.md` | `5440c66e91f522577bece150262d82ef1ec05d2de36432911de397f6f9fbf018` | `current_artifacts/133_V0_V7_VALIDATION_LEDGER_v1_8_1.md` | `880607a3101d20dbddff4682b68961dfdf9cf6e9a25b230e1b462227ad8ea185` | 3 |
| `137_NEXT_ACTIONS.md` | `94f15cb4da23b4fbf6556cc82c06eb94948eac72333697b82d6dc38b95b07f54` | `current_artifacts/137_NEXT_ACTIONS_v1_8_1.md` | `56c644cc36a77ea827abf4b5732980d55129fdba07ecda217c812570e8ac3726` | 9 |

## Method and rules

- **Search.** Patterns: V9 absent / not in environment or workspace / unavailable / artifact pending / 缺件 / 待核 / 待以原始檔案 / 依作者回報 / 使用者陳述 / 使用者稱 / 作者陳述 / USER-REPORTED / 2026-09-29 / 09-29 / FULL_REANALYSIS* / 完整重分析 / 未回報.
- **Classification.** Every hit was classified by hand.
  - **HISTORICAL_ENV.** The sentence describes the execution environment or the evidence available at the time of v1.7. It is kept verbatim, with the marker `〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕` appended.
  - **CURRENT_STATUS.** The sentence states present status. It is updated to say that the V9 source package was recovered and partially verified in V1.8, citing the V1.8 file. Non-V9 items that are still open are annotated with their V1.8 status and are not closed.
- **Full-reanalysis wording.** Current-status lines use the triplet `FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION; FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET; FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED`.
  - The forbidden `…_NOT_REQUIRED` variant appears nowhere in the current copies (verified by grep).
  - The V9 package's own label `FULL_REANALYSIS_REQUIRED` is kept wherever it is quoted as the package's label.
- **Mechanics.** Edits are exact-substring replacements on named lines. Each `old` occurs exactly once on its line (`task_b_stale.py` asserts this).
- **Verification.** `verify_b.py` confirmed that the set of changed lines equals the planned set for all four files, and that the body line count equals the historical file's.
- **137.**
  - P0-1 is marked **[PARTIALLY DONE — V1.8]**. The V9 part is DONE; Drive reconciliation is OPEN.
  - P0-3 carries the triplet and stays an open P0 researcher decision.
  - Nothing is marked submission-ready, and `SUBMISSION_READY = NO` is kept.

Line numbers below are the historical files' line numbers. In the current copy, add 7 for the header.

## Edit table (52 edits: 10 HISTORICAL_ENV, 42 CURRENT_STATUS)

| # | file | line | old | classification | new |
|---|---|---|---|---|---|
| 1 | 128 | 10 | 使用者列出的優先來源中，以下 **不在本工作環境中**（uploads 目錄為空，全檔系統搜尋無結果）： | HISTORICAL_ENV | 使用者列出的優先來源中，以下 **不在本工作環境中**（uploads 目錄為空，全檔系統搜尋無結果）：〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕 |
| 2 | 128 | 14 | \| `20260929_V9_HUMAN_VALIDATION.zip` \| **ABSENT** \| | CURRENT_STATUS | \| `20260929_V9_HUMAN_VALIDATION.zip` \| **RECOVERED；V9_SOURCE_VERIFIED=PARTIAL（V1.8）**（v1.7 時記為 ABSENT） \| |
| 3 | 128 | 14 | 人工標籤替換的局部敏感度結果（+人機增能 × 風險評估；−協調與執行 × 一般決策流程）與 `HUMAN_AUDIT_CONVERGED / LOCAL_SENSITIVITY_CHANGED / FULL_REANALYSIS_REQUIRED` 狀態，在本環境中**唯一來源是使用者 2026-10-13 的指示文字**。 | HISTORICAL_ENV | 人工標籤替換的局部敏感度結果（+人機增能 × 風險評估；−協調與執行 × 一般決策流程）與 `HUMAN_AUDIT_CONVERGED / LOCAL_SENSITIVITY_CHANGED / FULL_REANALYSIS_REQUIRED` 狀態，在本環境中**唯一來源是使用者 2026-10-13 的指示文字**。〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕 |
| 4 | 128 | 14 | κ 值、50/20/19 筆數可由 R14 定稿獨立核對（相符）。 | CURRENT_STATUS | κ 值、50/20/19 筆數可由 R14 定稿獨立核對（相符）。現況：V9 source package recovered and partially verified in V1.8——zip sha256 `8f63e88e…`；替換結果與狀態旗標已由 `ROBUST_CORE_LOCAL_SENSITIVITY.csv`（`e3166ee1…`）與 `FINAL_STATUS.json`（`d9226d31…`，verified_at 2026-10-03T12:23:44Z）逐列核對（`02_V9_AUTHORITY_MAP.md`、`04_LOCAL_SENSITIVITY_REPRODUCTION.md`）；12/37 受保護輸入仍未尋回。完整重分析現行狀態：FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET；FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED（`07_FULL_REANALYSIS_DECISION_MEMO.md` §8）。 |
| 5 | 128 | 15 | \| `完整資料來源.zip` \| **ABSENT** \| | CURRENT_STATUS | \| `完整資料來源.zip` \| **PRESENT IN V1.8 INPUTS（sha256 `138dbeac…`）— LEGACY_HISTORICAL_PROVENANCE**（v1.7 時記為 ABSENT） \| |
| 6 | 128 | 15 | V5 Manuscript Data Pack 本體未在環境中； | CURRENT_STATUS | `LEGACY_HISTORICAL_PROVENANCE — STRUCTURAL-HOLE / CITATION-NETWORK STUDY PACKAGE (NOT THE V5 DATA PACK); REAL_V5_DATA_PACK=NOT_RECOVERED`（`05_LEGACY_SOURCE_BOUNDARY.md` §1、§3.4，sha256 `03205f44…`；v1.7 誤稱為「V5 Manuscript Data Pack 本體」）； |
| 7 | 128 | 16 | \| `投稿格式.pdf`、`投稿範例.pdf`、`全文投稿樣板 windows (2).docx` \| **ABSENT** \| | CURRENT_STATUS | \| `投稿格式.pdf`、`投稿範例.pdf`、`全文投稿樣板 windows (2).docx` \| **ABSENT**（V1.8 仍為 OPEN_SOURCE_NOT_FOUND：`06_SOURCE_FLAG_CLOSURE.csv` 128 L16） \| |
| 8 | 128 | 17 | \| Google Drive 版本 \| **無法存取**（本工作階段無 Drive 連接器） \| | CURRENT_STATUS | \| Google Drive 版本 \| **無法存取**（本工作階段無 Drive 連接器；V1.8 仍未核對：`06_SOURCE_FLAG_CLOSURE.csv` 137 L10 OPEN_SOURCE_NOT_FOUND） \| |
| 9 | 128 | 29 | (b) 人工標籤替換局部敏感度與稽核狀態：V9 套件（2026-09-29）——**artifact 不在環境中，僅使用者陳述**。 | CURRENT_STATUS | (b) 人工標籤替換局部敏感度與稽核狀態：V9 套件（資料夾 `20260929_V9_HUMAN_VALIDATION`；`FINAL_STATUS.json` 驗證時間 2026-10-03T12:23:44Z）——**V9 source package recovered and partially verified in V1.8**（`02_V9_AUTHORITY_MAP.md` §7 權威檔案集；`04_LOCAL_SENSITIVITY_REPRODUCTION.md`）。 |
| 10 | 128 | 29 | (b) **USER-REPORTED, ARTIFACT PENDING** | CURRENT_STATUS | (b) **V9_SOURCE_VERIFIED=PARTIAL（V1.8；50/20/19、κ、局部敏感度成員由原始列重現）** |
| 11 | 128 | 29 | R14 02:218, 361, 365–375；使用者指示 §4–5 \| | CURRENT_STATUS | R14 02:218, 361, 365–375；使用者指示 §4–5；V1.8 `02`／`03`／`04` \| |
| 12 | 128 | 44 | 目標式人工標籤替換後核心仍為 32 格，但 +人機增能 × 風險評估（不足）、−協調與執行 × 一般決策流程（過度）；`FULL_REANALYSIS_REQUIRED` | HISTORICAL_ENV | 目標式人工標籤替換後核心仍為 32 格，但 +人機增能 × 風險評估（不足）、−協調與執行 × 一般決策流程（過度）；`FULL_REANALYSIS_REQUIRED`〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕 |
| 13 | 128 | 44 | B 較新（09-29 > R14 docx 09-20） | CURRENT_STATUS | B 較新（V9 `FINAL_STATUS.json` 2026-10-03 > R14 docx 09-20；v1.7 原記 09-29） |
| 14 | 128 | 44 | 但 B 的原始 artifact 不在環境中 | HISTORICAL_ENV | 但 B 的原始 artifact 不在環境中〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕 |
| 15 | 128 | 44 | 所有 B 的數字加 `[SOURCE: V9 human-validation state, 2026-09-29 — artifact not in workspace; verify before submission]`。 | HISTORICAL_ENV | 所有 B 的數字加 `[SOURCE: V9 human-validation state, 2026-09-29 — artifact not in workspace; verify before submission]`。〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕 |
| 16 | 128 | 44 | **作者須提供 V9 套件以核對**（137 P0-1）。 | CURRENT_STATUS | **V9 套件已取得並於 V1.8 逐列核對**：32 = 15／17、+1／−1、其餘 31 組不變、G01–G16 未移除（`04_LOCAL_SENSITIVITY_REPRODUCTION.md` T1–T3）；v1.8 稿件已將 V9 出處旗標改為來源引用（`06_SOURCE_FLAG_CLOSURE_NOTES.md` §3；`08_PATCH_LOG.md`）；137 P0-1 = PARTIALLY DONE。 |
| 17 | 128 | 46 | 並註明 Data Pack 原檔待核。 | CURRENT_STATUS | 並註明 Data Pack 原檔待核（V1.8：REAL_V5_DATA_PACK=NOT_RECOVERED；`完整資料來源.zip` 不是 Data Pack，見 `05_LEGACY_SOURCE_BOUNDARY.md` §3.4；同一模型摘要值另見 V9.1 `SEGMENT_STAGE2_MODEL_VERIFICATION.json`，`06_SOURCE_FLAG_CLOSURE.csv` 128 L46）。 |
| 18 | 128 | 53 | 不適用（缺 2026-09-29 原始紀錄） | HISTORICAL_ENV | 不適用（缺 2026-09-29 原始紀錄）〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕 |
| 19 | 128 | 53 | v1.7 改寫為「不同的測量操作；範圍可能部分重疊，待核」（E49） | CURRENT_STATUS | v1.7 改寫為「不同的測量操作；範圍可能部分重疊，待核」（E49）；V1.8 已核（`04_LOCAL_SENSITIVITY_REPRODUCTION.md` §3b）：標籤處理不重疊（V9.1 重切分未傳播任何人工標籤），記錄樣本部分重疊（50 筆受稽核記錄中 28 筆亦被重切分；其中 11 筆因人工錯誤標記被強制納入候選） |
| 20 | 128 | 64 | **未觸發，但 artifact 缺件** | CURRENT_STATUS | **未觸發**（v1.7 時 artifact 缺件；V1.8 已取得並核對） |
| 21 | 128 | 64 | 替換結果只見於使用者指示（CF-01）。 | HISTORICAL_ENV | 替換結果只見於使用者指示（CF-01）。〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕 |
| 22 | 128 | 64 | 替換結果只見於使用者指示（CF-01）。〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕 | CURRENT_STATUS | 替換結果只見於使用者指示（CF-01）。〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕 V1.8：50/20/19 與 κ 由原始列重現（`03_HUMAN_AUDIT_REPRODUCTION.md`；無 HUMAN_RELIABILITY_CONFLICT），替換結果由 `ROBUST_CORE_LOCAL_SENSITIVITY.csv` 逐列重現（`04`）。 |
| 23 | 128 | 73 | 觸發的兩項（CF-01 缺件、CF-02 證據不足）已以「不猜、加出處旗標、改寫為可支持表述」處理，並列入 OPEN BLOCKERS。 | HISTORICAL_ENV | 觸發的兩項（CF-01 缺件、CF-02 證據不足）已以「不猜、加出處旗標、改寫為可支持表述」處理，並列入 OPEN BLOCKERS。〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕 |
| 24 | 131 | 14 | \| 後續要求 \| `FULL_REANALYSIS_REQUIRED` \| | CURRENT_STATUS | \| 後續要求 \| V9 套件狀態標籤 `FULL_REANALYSIS_REQUIRED`（`FINAL_STATUS.json`；需研究者核准）；現行：FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET；FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED（`07_FULL_REANALYSIS_DECISION_MEMO.md` §8） \| |
| 25 | 131 | 28 | \| R14 定稿 §3.7.1、§4.6.1、表 5；V9 狀態紀錄 \| 收斂；局部敏感；須完整重分析 \| | CURRENT_STATUS | \| R14 定稿 §3.7.1、§4.6.1、表 5；V9 人工驗證套件（V1.8 已取得並部分核對：`02_V9_AUTHORITY_MAP.md`） \| 收斂；局部敏感；完整重分析：FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET；FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED \| |
| 26 | 131 | 40 | \| R14 02:218、357 \| ✔ 與使用者陳述一致 \| | CURRENT_STATUS | \| R14 02:218、357；V9 `FIRST_CODER_50_FINAL_FROZEN.csv`（`dd332dd8…`） \| ✔ 與 V9 原始列一致（V1.8 `03_HUMAN_AUDIT_REPRODUCTION.md`） \| |
| 27 | 131 | 42 | ✔（使用者稱 19/19 reconciliation） | CURRENT_STATUS | ✔（V9 `HUMAN_RECONCILED_20.csv`（`4b7ceac2…`）＋調和事件雜湊鏈 19/19；V1.8 `02` §2、`03` 重現） |
| 28 | 131 | 44 | \| R14 表 5、02:361 \| ✔ 與使用者陳述一致 \| | CURRENT_STATUS | \| R14 表 5、02:361；V9 `HUMAN_RELIABILITY_FINAL.csv`（`ef7e5544…`） \| ✔ 與 V9 原始列重算一致（V1.8 `03`：.5614／.1798／.0476／.1398／.3162） \| |
| 29 | 131 | 51 | \| 使用者陳述（V9，2026-09-29） \| ✖ 原始檔案不在環境中 \| | CURRENT_STATUS | \| V9 `FINAL_STATUS.json`（`d9226d31…`；verified_at 2026-10-03T12:23:44Z）；完整重分析現行三元組：FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET；FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED \| ✔ V1.8 已核（`02_V9_AUTHORITY_MAP.md` §4、§7）；V9_SOURCE_VERIFIED=PARTIAL \| |
| 30 | 131 | 52 | \| 使用者陳述（V9） \| ✖ 原始檔案不在環境中；兩個配對在 R14 中的位置已核（下節） \| | CURRENT_STATUS | \| V9 `ROBUST_CORE_LOCAL_SENSITIVITY.csv`（`e3166ee1…`）／`_DIFF.csv`（`f6607aae…`） \| ✔ V1.8 逐列核對（`04_LOCAL_SENSITIVITY_REPRODUCTION.md` T1、T3）；兩個配對在 R14 中的位置已核（下節） \| |
| 31 | 131 | 53 | \| 使用者陳述；R14 02:361 | CURRENT_STATUS | \| V9 `FINAL_ERROR_TAXONOMY.csv`（`68e97c01…`）／`.md`（`33044106…`）；R14 02:361 |
| 32 | 131 | 53 | 作為四分類的整理來自 2026-09-29 紀錄； | CURRENT_STATUS | 作為四分類的整理來自 V9 錯誤型態表（V1.8 部分核對，`06_SOURCE_FLAG_CLOSURE_NOTES.md` §4）：V9 將其列為模型標籤與人工標籤差異的詮釋性假說（非裁決），並另列第五類 `TRUE_CONCEPTUAL_AMBIGUITY`，不是對 19 筆編碼者間分歧的歸類； |
| 33 | 131 | 90 | **表 H-2：成員變動（V9；待以原始檔案核對）** | CURRENT_STATUS | **表 H-2：成員變動（V9 `ROBUST_CORE_LOCAL_SENSITIVITY.csv`；V1.8 已逐列核對，`04` T1）** |
| 34 | 131 | 97 | 推得（不是新的觀察）：若無其他未回報的變動，凍結核心其餘 31 組不變，替換後集合為 15 過度／17 不足；G01–G16 全部保留；新增的不足呈現不屬 G01–G16。稿件以「依回報的變動推得」標示，並列入附錄 E39 待核。 | CURRENT_STATUS | V1.8 逐列核對（`04_LOCAL_SENSITIVITY_REPRODUCTION.md` Q1–Q3、T1–T3）：核心成員沒有其他變動，凍結核心其餘 31 組成員與方向不變，替換後集合為 15 過度／17 不足；G01–G16 全部保留；新增的不足呈現不屬 G01–G16。核心以外，120 格中共 33 格有計數或非核心方向差異（不影響核心成員）。v1.7 原以「依回報的變動推得」標示並列入附錄 E39 待核；v1.8 已改以 V9 逐列結果表述（E39 已核）。 |
| 35 | 131 | 103 | 3. 成員有變 → 須完整重分析；不以替換後集合取代凍結結果。 | CURRENT_STATUS | 3. 成員有變 → 完整重分析列為 V9 的開放驗證行動（FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET；FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED；`07` §8）；不以替換後集合取代凍結結果。 |
| 36 | 131 | 104 | R14 註明重切分設定中「人工調和標籤不傳播至未稽核記錄」，受稽核記錄在重切分中是否已使用人工標籤待核（E49），因此兩者的處理範圍可能部分重疊。 | CURRENT_STATUS | R14 註明重切分設定中「人工調和標籤不傳播至未稽核記錄」；V1.8 已核（`04` §3b，E49）：重切分未傳播任何人工標籤（受稽核但未被重切分的 22 筆在 S1／S2 中 22/22 保留模型家族），因此標籤處理不重疊；但記錄樣本部分重疊（50 筆中 28 筆亦被重切分，其中 11 筆因人工錯誤標記被強制納入候選）。 |
| 37 | 131 | 145 | 1. **V9 原始檔案缺件**：替換清單、替換後矩陣、變動配對、是否有其他未回報的變動、「凍結核心其餘 31 組不變」皆待核（E39）。 | CURRENT_STATUS | 1. **V9 原始檔案：已取得並於 V1.8 部分核對**：替換清單（`04` T4）、變動配對、無其他核心成員變動、「凍結核心其餘 31 組不變」皆已逐列核對（E39）。殘留：替換後 q 值的產生腳本與 sidecar 核心檔 NOT_RECOVERED（只重現成員與判準，未重跑零模型）；12/37 受保護輸入未尋回；`HUMAN_AUDIT_APPEND_ONLY_LOG.csv` 受保護雜湊不符（UNVERIFIED，無竄改證據）（`02` §5）。 |
| 38 | 131 | 146 | 2. **完整重分析的時點與範圍**， | CURRENT_STATUS | 2. **完整重分析的時點與範圍**（現行：FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET；FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED；`07` §8；是否重跑仍屬研究者決定）， |
| 39 | 131 | 147 | 矩陣重建方式、檢定組合、隨機種子。 | CURRENT_STATUS | 矩陣重建方式、檢定組合、隨機種子。V1.8 部分解答：50 筆皆替換（20 筆用調和 FINAL 標籤、30 筆用第一位編碼者標籤；未稽核記錄不變，`04` Q4）；依 V9 `ROBUST_CORE_LOCAL_SENSITIVITY.md` 摘要（未逐列重現）：主零模型 10,000 次、seed 20260918；文獻內部結構保持零模型 5,000 次、seed 20260919；產生腳本 NOT_RECOVERED，標籤→納入資格的傳播規則 UNRESOLVED。 |
| 40 | 131 | 148 | 4. **兩種敏感度的處理範圍是否重疊**（E49）。 | CURRENT_STATUS | 4. **兩種敏感度的處理範圍是否重疊**（E49）。V1.8 已核：標籤處理不重疊；記錄樣本 28/50 重疊（`04` §3b）。 |
| 41 | 133 | 34 | \| LOCAL_SENSITIVITY_CHANGED；FULL_REANALYSIS_REQUIRED \| | CURRENT_STATUS | \| LOCAL_SENSITIVITY_CHANGED；V9 標籤 FULL_REANALYSIS_REQUIRED → 現行 FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET；FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED \| |
| 42 | 133 | 34 | \| 2026-09-29 人工驗證紀錄（檔名含 V9；不是驗證閘門；原始檔案缺件） \| | CURRENT_STATUS | \| V9 人工驗證套件（資料夾 20260929_V9_HUMAN_VALIDATION；V9 是檔案版本名，不是驗證閘門）之 `FINAL_STATUS.json`（2026-10-03）與 `ROBUST_CORE_LOCAL_SENSITIVITY.csv`（`e3166ee1…`）；V9 source package recovered and partially verified in V1.8（`02`、`04`） \| |
| 43 | 133 | 34 | \| 格數 32；±1 成員（依作者回報） \| | CURRENT_STATUS | \| 格數 32（15／17）；±1 成員（V1.8 逐列核對，`04` T1）；G01–G16 未移除 \| |
| 44 | 137 | 10 | \| P0-1 \| P0 \| **canonical source conflict：取得 V9 人工驗證原始檔案**（`20260929_V9_HUMAN_VALIDATION.zip`），並確認 Drive 上沒有比 R14／V9 更新的版本 \| | CURRENT_STATUS | \| P0-1 \| P0 \| **[PARTIALLY DONE — V1.8]** **canonical source conflict：取得 V9 人工驗證原始檔案**（`20260929_V9_HUMAN_VALIDATION.zip`）＝**DONE**（已取得，zip sha256 `8f63e88e…`；於 V1.8 部分核對：`02_V9_AUTHORITY_MAP.md` V9_SOURCE_VERIFIED=PARTIAL），並確認 Drive 上沒有比 R14／V9 更新的版本＝**OPEN**（作者確認；`06_SOURCE_FLAG_CLOSURE.csv` 137 L10） \| |
| 45 | 137 | 10 | 稽核狀態旗標與標籤替換結果在本環境只有作者陳述； | HISTORICAL_ENV | 稽核狀態旗標與標籤替換結果在本環境只有作者陳述；〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕 |
| 46 | 137 | 10 | 以原始檔案核對：替換清單、替換後矩陣、兩個變動配對、凍結核心其餘 31 組不變、是否有其他未回報的變動、15／17；不一致時以原始檔案重寫各處；移除 V9 旗標 | CURRENT_STATUS | 以原始檔案核對——V1.8 結果：✔ 替換清單（50 筆，`04` T4）；✔ 兩個變動配對；✔ 凍結核心其餘 31 組不變；✔ 無其他核心成員變動（另有 33/120 格計數或非核心方向差異）；✔ 15／17；✔ 無數值不一致，無須重寫數值；✔ v1.8 稿件移除 V9 旗標（`08_PATCH_LOG.md`）；✔ 132 於 V1.8.1 重新產生（`11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md`）。殘留：替換後矩陣的產生腳本與 sidecar 核心檔 NOT_RECOVERED（q 值未重算）；12/37 受保護輸入 NOT_RECOVERED |
| 47 | 137 | 12 | **文獻層完整重分析的決策**（FULL_REANALYSIS_REQUIRED；含 E49：兩種敏感度的處理範圍是否重疊） | CURRENT_STATUS | **文獻層完整重分析的決策**（V9 標籤 FULL_REANALYSIS_REQUIRED；現行：FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET；FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED；E49 已於 V1.8 核定：標籤處理不重疊、記錄樣本 28/50 重疊） |
| 48 | 137 | 12 | 作者決定「投稿前重分析」或「投稿稿明載凍結基準＋局部敏感度」； | CURRENT_STATUS | 作者決定「投稿前重分析」或「投稿稿明載凍結基準＋局部敏感度」；V1.8 建議為後者（`07_FULL_REANALYSIS_DECISION_MEMO.md` §8），但仍屬研究者決定；若選擇重跑，須先通過 `07` §4 閘門（受保護輸入回復並雜湊比對），標籤輸入只能用 `04` T4，傳播規則須事前宣告（`15_REANALYSIS_INPUT_GOVERNANCE.md`）； |
| 49 | 137 | 12 | \| 作者；重分析需 V5 pipeline \| P0-1 \| | CURRENT_STATUS | \| 作者；重分析需 V5 pipeline \| P0-1（V9 部分已完成） \| |
| 50 | 137 | 22 | 格式檔案不在環境中； | CURRENT_STATUS | 格式檔案不在環境中（V1.8 仍為 OPEN_SOURCE_NOT_FOUND，`06_SOURCE_FLAG_CLOSURE.csv` 137 L22）； |
| 51 | 137 | 35 | P0-1 只需要作者把 `20260929_V9_HUMAN_VALIDATION.zip`（以及若有更新的 R14／Drive 版本）放進這個工作階段；核對與重寫可在同一輪完成。 | HISTORICAL_ENV | P0-1 只需要作者把 `20260929_V9_HUMAN_VALIDATION.zip`（以及若有更新的 R14／Drive 版本）放進這個工作階段；核對與重寫可在同一輪完成。〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕 |
| 52 | 137 | 35 | 核對與重寫可在同一輪完成。〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕 | CURRENT_STATUS | 核對與重寫可在同一輪完成。〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕 現況：V9 部分已於 V1.8 完成；P0-1 只剩 Drive 對帳（作者確認）。不需要外部資料的下一步：依 `15_REANALYSIS_INPUT_GOVERNANCE.md` 事前宣告 UNCERTAIN／AMBIGUOUS／UNMAPPED 的傳播規則（P0-3 的前置條件；不執行重分析）。 |

Per file:

- 128: 23 edits (8 HISTORICAL_ENV, 15 CURRENT_STATUS) on lines [10, 14, 15, 16, 17, 29, 44, 46, 53, 64, 73]
- 131: 17 edits (0 HISTORICAL_ENV, 17 CURRENT_STATUS) on lines [14, 28, 40, 42, 44, 51, 52, 53, 90, 97, 103, 104, 145, 146, 147, 148]
- 133: 3 edits (0 HISTORICAL_ENV, 3 CURRENT_STATUS) on lines [34]
- 137: 9 edits (2 HISTORICAL_ENV, 7 CURRENT_STATUS) on lines [10, 12, 22, 35]

### Hits reviewed and deliberately left unchanged

| file | line | text (excerpt) | reason |
|---|---|---|---|
| 131 | 126 | 「1.4、表 1-1、1.5、1.6 … 完整重分析」 | Topic label in the v1.7 manuscript-integration map (§7). It records where v1.7 placed content and makes no status claim. |
| 131 | 138 | 「5.8.2、5.8.9（新）、5.9、5.10 … 效度邊界、完整重分析」 | Same: topic label, not a status claim. |
| 131 | 129 | 「程序細節 `[AUTHOR TO CONFIRM]`」 | Describes v1.7 manuscript content (historical integration map). The current state of E48 is given at L147 in the current copy. |
| 128 | 28, 45–48, 97 | 「專案指示／使用者指示 …」 | User-instruction provenance for CF-02–CF-05 and the V5 numbers. Not V9 availability; out of scope. |
| 128 | 34; 131 L16–17, 29–30, 115, 117; 133 L13, 37, 48, 51 | `PENDING` (V1 / EA-X / ORG-V / enterprise data) | Genuinely pending, outside V9 (`06` KEEP_AS_LIMITATION / NOT_A_FLAG). Kept. |
| 133 | 33 | 「HUMAN_AUDIT_CONVERGED … R14 表 5；V9」 | Already correct. No stale availability claim. |

## Task C — Legacy mislabel `完整資料來源.zip` ≠ V5 Data Pack

### Fix applied (128 current copy, historical L15)

- The status cell `**ABSENT**` now reads `**PRESENT IN V1.8 INPUTS（sha256 138dbeac…）— LEGACY_HISTORICAL_PROVENANCE**（v1.7 時記為 ABSENT）`.
- The description `V5 Manuscript Data Pack 本體未在環境中；` is replaced by `LEGACY_HISTORICAL_PROVENANCE — STRUCTURAL-HOLE / CITATION-NETWORK STUDY PACKAGE (NOT THE V5 DATA PACK); REAL_V5_DATA_PACK=NOT_RECOVERED`. It cites `05_LEGACY_SOURCE_BOUNDARY.md` §1 and §3.4 (sha256 `03205f4422cce5cf2937fb7f4a2f35fd98ac2bf65732115a379af35e05b7b14c`) and notes the v1.7 mislabel.
- The rest of the line ("本輪以 R14 定稿 + 04_G01_G16_FROZEN.csv + 專案指示所列 V5 數字交叉核對") is unchanged. Per `05` §3.4, no canonical number depends on this zip.
- 128 L46 (CF-03, "Data Pack 原檔待核") is annotated `REAL_V5_DATA_PACK=NOT_RECOVERED; 完整資料來源.zip 不是 Data Pack`.

### Search

- **Script.** `task_c_search.py`. Pattern `完整資料來源|Data[ _]?Pack`, case-insensitive. It covers "V5 Data Pack", "V5 Manuscript Data Pack" and "Data Pack".
- **Scope.** Three sets:
  - All text files under `W\01_ALL_OUTPUTS` (md/txt/csv/json/py…, plus docx/xlsx/pptx XML).
  - All 226 git-tracked files of the repo (text plus Office XML), which include the V1.8 folder and the v1.8 manuscript `08_…v1_8_SOURCE_VERIFIED.md`.
  - The new files in OUT, which are untracked and were checked separately.
- **Hits.** 23 in W/01 and 140 in the repo. Most repo hits are inventory or tool rows listing the legacy package's own file names.

### Every co-occurrence or binding of `完整資料來源` with "Data Pack" / V5

| # | Location | Text (excerpt) | Binding? | Action |
|---|---|---|---|---|
| 1 | W `r14_merge_v1_7/128_CANONICAL_STATE.md` L15 | `完整資料來源.zip` \| **ABSENT** \| V5 Manuscript Data Pack 本體未在環境中 | **MIS-BINDING** (the known one) | Historical: recorded only. **Fixed in `current_artifacts/128_CANONICAL_STATE_v1_8_1.md`.** |
| 2 | W `r14_merge_v1_7/work_v17/adversarial_review_v17.md` L85 | "128 §0 records the V5 Data Pack (`完整資料來源.zip`) as **ABSENT**." | **MIS-BINDING (second, not previously listed)**. It repeats 128 L15. | Historical (v1.7 work file): recorded only. |
| 3 | Repo `claude/r14_merge_v1_8_source_closure/06_SOURCE_FLAG_CLOSURE.csv` row for 128 L15 (and `tools/E/build.py` L65, `tools/E/flags*.csv/txt`) | needed_evidence = "V5 Manuscript Data Pack"; source_artifact = `W/03_LEGACY_FULL_SOURCE/完整資料來源`; source_found = PARTIAL; verified = NO; OPEN_SOURCE_NOT_FOUND | **Weak co-binding.** `source_found=PARTIAL` could be read as the legacy zip partly supplying the V5 Data Pack. Its own notes say "not checked by E". Superseded by `05` §3.4 and `10` item 1 (REAL_V5_DATA_PACK=NOT_RECOVERED). | Historical, frozen V1.8 file: recorded only. |
| 4 | Repo `05_LEGACY_SOURCE_BOUNDARY.md` L176/184/204, `10_FINAL_STATUS.md` L93, `tools/D/footer.md`, `tools/D/legacy_audit_result.json` L1227 | Quote 128 L15 in order to refute it | Correct (refutation or quotation) | None. |
| 5 | W `r14_merge_v1_3/tools/build94.py` L294 | "No local PDFs exist; '完整資料來源' = files in this environment." | Not a Data Pack binding. It uses the phrase to mean "full sources", in a different sense. | None. |

### "Data Pack" mentions without `完整資料來源` (abstract V5 export; no binding to the legacy zip)

- **W historical.**
  - 128 L28, L46.
  - 129 L60, L181.
  - 130 .md L651, L3036, and .docx (the same two passages).
  - `tools_v17/build130.py` L165, L403; `tools_v17/fix_v17_review.py` L36–37; `work_v17/adversarial_review_v17.md` L83, L90.
  - `r14_merge/69_…AUDIT_v1_0.md` L106; `r14_merge/tools/audit69.py` L85.
  - `v2_1/44_…v2_1.md` L41, L880; `v2_1/48_…STATUS.md` L35.
- **Repo.**
  - `01_CANONICAL_MODEL_v1_0.md` L19; `08_16Depletion_Quantification_v1_0.xlsx` (sheets 12 and 14).
  - V1.8 `06_SOURCE_FLAG_CLOSURE.csv` rows 17/48/78 and `_NOTES.md` L43/L97; `08_PATCH_LOG.md` L388/441/462; `10_FINAL_STATUS.md` L80.
- **V1.8 manuscript `08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md`.** L651 ("依專案紀錄的 V5 Manuscript Data Pack 模型資訊；Data Pack 原檔不在本稿工作環境中") and L3036 (E12). It **never names `完整資料來源`**, so there is no mis-binding. L651 is an open non-V9 provenance item (OPEN_SOURCE_NOT_FOUND, `08_PATCH_LOG.md` L441) and is consistent with REAL_V5_DATA_PACK=NOT_RECOVERED.

### Files created this round (OUT)

- `完整資料來源` occurs only in:
  - `current_artifacts/128_CANONICAL_STATE_v1_8_1.md` historical L15 and L46 (current-copy L22 and L53), with the corrected wording;
  - this report.
- The 131/133/137 current copies and `15_REANALYSIS_INPUT_GOVERNANCE.md` do not contain it.
- No created file binds it to the V5 Data Pack.

**Task C result.**

- Mis-bindings found: 2 historical, namely 128 L15 and `adversarial_review_v17.md` L85. The first is fixed in the 128 current copy; both are recorded.
- 1 weak co-binding in the frozen V1.8 `06` CSV row is recorded and superseded by `05`/`10`.
- Mis-bindings in created files: 0.
- `REAL_V5_DATA_PACK=NOT_RECOVERED`.
