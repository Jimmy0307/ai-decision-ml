> **CURRENT COPY (V1.8.1, 2026-10-14) — current copy; history preserved.**
> Historical source: `W\01_ALL_OUTPUTS\AI_DECISION_THESIS_ALL_OUTPUTS\r14_merge_v1_7\131_HUMAN_VALIDATION_INTEGRATION_REPORT.md` (sha256 `d47ee7632758a66571d498a6b350892aaac28ca3e7d97d34157c99bce30db891`), left unchanged.
> Changed: only stale V9-availability / 2026-09-29 / 依作者回報 / full-reanalysis status spans (17 edits; line-by-line log in `claude/r14_merge_v1_8_1_study1_freeze/12_STALE_STATUS_CLEANUP_REPORT.md`, line numbers = historical file).
> Sentences describing the execution environment at that time are kept verbatim with the marker `〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：…〕`; current-status sentences are updated with citations.
> File names 02–10 refer to `claude/r14_merge_v1_8_source_closure/`; 11/12/15 refer to `claude/r14_merge_v1_8_1_study1_freeze/`.
> No number, G01–G16 content, taxonomy, G→M assignment, model, solver, schema or empirical result was changed. `SUBMISSION_READY = NO`.

# 131 — HUMAN_VALIDATION_INTEGRATION_REPORT（v1.7）

日期：2026-10-14　｜　對應稿件：130（v1.7）第 3.7、4.5、5.4.2、5.8.2、5.8.9 節；表 3-3、4-6、4-9A
本報告不做新分析，只整合既有證據，並標明每一項的出處與核對狀態。

---

## 0. 結論先行

| 項目 | 狀態 |
|---|---|
| 文獻層人工稽核 | `HUMAN_AUDIT_CONVERGED`（50/50、20/20、19/19） |
| 目標式人工標籤替換 | `LOCAL_SENSITIVITY_CHANGED`：核心格數 32 不變；+人機增能 × 風險評估（不足），−協調與執行 × 一般決策流程（過度） |
| 後續要求 | V9 套件狀態標籤 `FULL_REANALYSIS_REQUIRED`（`FINAL_STATUS.json`；需研究者核准）；現行：FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET；FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED（`07_FULL_REANALYSIS_DECISION_MEMO.md` §8） |
| 正式推論基準 | 凍結的主要穩健集合：32 組（16 過度、16 不足） |
| 企業 G→M 構念效度（V1） | THEORETICAL CONVERGENCE COMPLETE（研究者裁決）；AI PILOT COMPLETE；HUMAN BLIND CODING PENDING |
| 組織編碼驗證（ORG-V1–V5） | PENDING |
| 可以寫的話 | 「凍結的主要穩健集合仍是正式推論基準；目標式人工裁決顯示，少數配對的成員資格對編碼與分類邊界敏感。」 |
| 不可以寫的話 | 把人工稽核寫成已驗證全部 32 組；沿用「人工驗證支持 V9」類敘事；「錯誤來自 LLM 不準」「人工稽核驗證了分類架構」「AI pilot／研究者裁決完成了構念效度」 |
| 投稿就緒 | `SUBMISSION_READY = NO` |

---

## 1. 三種「人類驗證」不能混用

| 對象 | 問的是什麼 | 證據 | 狀態 | 在稿件中的位置 |
|---|---|---|---|---|
| (A) 文獻語意證據與功能分類的人工稽核 | 證據是否有效、關係與家族是否被正確判定、證據切分與標籤是否改變結構 | R14 定稿 §3.7.1、§4.6.1、表 5；V9 人工驗證套件（V1.8 已取得並部分核對：`02_V9_AUTHORITY_MAP.md`） | 收斂；局部敏感；完整重分析：FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET；FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED | 3.7.1–3.7.5、4.5.1、4.5.5、5.4.2、5.8.2、5.8.9 |
| (B) 企業缺口—機制轉譯的構念效度（V1） | G01–G16 → M1–M5／狀態的對應是否能被獨立編碼者重現 | 53B 協定、54A/B 封包、54C AI pilot、60 分析器；人類結果 PENDING | AI pilot 完成；人類待完成 | 3.9.3–3.9.5、4.7 |
| (C) 組織導入架構的編碼驗證（ORG-V1–V5） | 組織決策權與資源結構的編碼與正式模型映射能否被重現 | 107–117 | 全部 PENDING | 3.10.7、表 4-32F |

(A) 的結果不能被引用為 (B) 或 (C) 的通過證據；(B) 的 AI pilot 也不能被引用為 (A) 的證據（127 第 3.7.3 節末段已載明，130 第 3.7.5 節重申）。

---

## 2. 來源與核對狀態

| 數據 | 數值 | 來源 | 核對 |
|---|---|---|---|
| 研究者目標稽核筆數 | 50 | R14 02:218、357；V9 `FIRST_CODER_50_FINAL_FROZEN.csv`（`dd332dd8…`） | ✔ 與 V9 原始列一致（V1.8 `03_HUMAN_AUDIT_REPRODUCTION.md`） |
| 盲式第二編碼筆數 | 20 | R14 02:218、361 | ✔ |
| 至少一欄分歧並經調和 | 19 | R14 02:218、609 | ✔（V9 `HUMAN_RECONCILED_20.csv`（`4b7ceac2…`）＋調和事件雜湊鏈 19/19；V1.8 `02` §2、`03` 重現） |
| 調和前一致率 | 75%／35%／20%／20%／60% | R14 表 5 | ✔ |
| 調和前 Cohen's κ | .561／.180／.048／.140／.316 | R14 表 5、02:361；V9 `HUMAN_RELIABILITY_FINAL.csv`（`ef7e5544…`） | ✔ 與 V9 原始列重算一致（V1.8 `03`：.5614／.1798／.0476／.1398／.3162） |
| κ 95% 自助法 CI | [.242, .841]／[-.081, .429]／[-.081, .176]／[-.027, .314]／[.015, .623] | R14 表 5（20,000 次記錄層級成對自助法） | ✔ |
| 首輪模型 vs 人工 | 關係 14/50、AI 家族 19/50、決策家族 9/50、納入 33/42（9 筆模型納入、人工排除，無反向） | R14 02:359 | ✔ |
| AI 端補充三角檢查 | 60 筆，41 一致（68.3%），κ = .647，CI [.511, .773]；第二組為獨立模型預編碼，**不是**真人 | R14 02:363 | ✔ |
| 稽核方案變更 | 原規劃 400 首輪／120 第二編碼 → 50／20；**不是**預先註冊的停止規則 | R14 02:218 | ✔ |
| 非完全 AI 盲 | 首輪部分困難邊界案例曾以外部 AI 討論編碼規則 | R14 02:218、609 | ✔ |
| 人工調和標籤是否傳播至未稽核記錄（重切分分析中） | 不傳播 | R14 02:258 | ✔ |
| 稽核狀態旗標 | HUMAN_AUDIT_CONVERGED；LOCAL_SENSITIVITY_CHANGED；FULL_REANALYSIS_REQUIRED；SUBMISSION_READY=NO | V9 `FINAL_STATUS.json`（`d9226d31…`；verified_at 2026-10-03T12:23:44Z）；完整重分析現行三元組：FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET；FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED | ✔ V1.8 已核（`02_V9_AUTHORITY_MAP.md` §4、§7）；V9_SOURCE_VERIFIED=PARTIAL |
| 標籤替換的成員變動 | +人機增能 × 風險評估（不足）；−協調與執行 × 一般決策流程（過度）；格數 32 | V9 `ROBUST_CORE_LOCAL_SENSITIVITY.csv`（`e3166ee1…`）／`_DIFF.csv`（`f6607aae…`） | ✔ V1.8 逐列核對（`04_LOCAL_SENSITIVITY_REPRODUCTION.md` T1、T3）；兩個配對在 R14 中的位置已核（下節） |
| 四類分歧來源 | 模型映射、分類邊界、證據切分、PDF／擷取品質 | V9 `FINAL_ERROR_TAXONOMY.csv`（`68e97c01…`）／`.md`（`33044106…`）；R14 02:361（分類邊界、證據單元過寬）、02:256（「多功能、過寬與抽取破碎的證據片段」；127:594） | △ 四類皆可在 R14 文字中找到對應現象；作為四分類的整理來自 V9 錯誤型態表（V1.8 部分核對，`06_SOURCE_FLAG_CLOSURE_NOTES.md` §4）：V9 將其列為模型標籤與人工標籤差異的詮釋性假說（非裁決），並另列第五類 `TRUE_CONCEPTUAL_AMBIGUITY`，不是對 19 筆編碼者間分歧的歸類；19 筆分歧尚未逐筆依四類歸類，稿件以「可能來自」表述 |

---

## 3. 一致度結果與其意義

**表 H-1：20 筆盲式第二編碼的調和前一致度（R14 表 5）**

| 欄位 | 完全一致 | κ | 95% CI |
|---|---|---|---|
| 證據有效性 | 15/20（75%） | .561 | [.242, .841] |
| 關係類型 | 7/20（35%） | .180 | [-.081, .429] |
| 人工智慧功能家族 | 4/20（20%） | .048 | [-.081, .176] |
| 決策功能家族 | 4/20（20%） | .140 | [-.027, .314] |
| 分析納入 | 12/20（60%） | .316 | [.015, .623] |

判讀（與稿件第 5.4.2 節一致）：

1. 編碼者較常同意「這段文字是否支持一個人工智慧 × 決策功能關係」，較少同意「應被壓成哪一個單一關係類型與單一家族」。
2. 家族欄位的 κ 區間都包含 0，n = 20；這只能作目標式診斷，不能估計全語料或 22 個家族的分類效能，也不報告文字強度標籤（R14 表 5 註；稿件不引用 Landis & Koch 的分級）。
3. 稿件不計算單一總體 κ，也不把 κ 換算成全語料錯誤率。

---

## 4. 分歧分析：四類來源（方法學發現）

| 來源 | 可觀察的現象（R14 文字證據） | 為什麼不能只歸因於 LLM | 對應的改進方向 |
|---|---|---|---|
| 1. 模型映射歧義 | 首輪模型與人工在家族上 19/50、9/50 一致 | 兩位真人之間的家族一致度也只有 20%（κ = .048／.140） | 雙次判定與證據對回已在主要流程中限制此來源，但不能消除 |
| 2. 分類架構邊界歧義 | 分歧集中於一般推理系統、人機增能、檢索與統整等較廣或殘餘性家族（60 筆三角檢查） | 邊界模糊時，真人之間也不一致 | 修訂家族定義、典型詞與排除規則（補充表 S6） |
| 3. 證據片段切分歧義 | 多功能、過寬的片段；重切分使 84–85/120 格觀察值改變（V9.1 證據單元重切分敏感度，2026-10-03，以凍結主要基準為對照；出處見 v1.8.1 `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md`） | 一段文字含多個功能命題時，「單一家族」本身就不是良定義 | 最小實質單元；允許多配對表示（稿件 5.4.2、5.9） |
| 4. PDF／全文擷取品質 | 抽取破碎的片段；正式流程無 OCR（PdfPig） | 擷取錯誤在模型與人之前就已發生 | 回到來源文件；逐頁擷取品質檢查（目前未做，稿件 5.8.2 列為效度邊界） |

---

## 5. 目標式人工標籤替換的局部敏感度

**表 H-2：成員變動（V9 `ROBUST_CORE_LOCAL_SENSITIVITY.csv`；V1.8 已逐列核對，`04` T1）**

| 配對 | 方向 | 凍結核心 | 替換後 | 在 R14／127 主要分析中的位置（已核） |
|---|---|---|---|---|
| 人機增能 × 風險評估（HUMAN_AUGMENTATION × RISK_ASSESSMENT） | 不足 | — | ✓ | R14 表 11 第 7 列（127 表 4-5）：O/E = 0.08，主要零模型 \*\*\*，只因文獻內部結構保持零模型未通過；R14 表 8 未列 → 三種證據單元設定皆未進入穩健集合 |
| 協調與執行 × 一般決策流程（COORDINATION_EXECUTION × GENERAL_DECISION_PROCESS） | 過度 | ✓ | — | R14 表 9 第 10 列（127 表 4-3）：O = 19，E = 9.74，O/E = 1.95，主要模型 \*（最低一級），證據單元「持續」 |

V1.8 逐列核對（`04_LOCAL_SENSITIVITY_REPRODUCTION.md` Q1–Q3、T1–T3）：核心成員沒有其他變動，凍結核心其餘 31 組成員與方向不變，替換後集合為 15 過度／17 不足；G01–G16 全部保留；新增的不足呈現不屬 G01–G16。核心以外，120 格中共 33 格有計數或非核心方向差異（不影響核心成員）。v1.7 原以「依回報的變動推得」標示並列入附錄 E39 待核；v1.8 已改以 V9 逐列結果表述（E39 已核）。

判讀規則（寫入稿件 3.7.4 與 4.5.5；於結果回報後、撰寫 v1.7 時訂定，不是事前登記的規則）：

1. 凍結的 32 組是正式推論基準；替換結果不回寫第 4.4 節。
2. 50 筆是目標樣本，替換只能指出邊界附近配對的成員敏感，不能估計全語料重編後的穩健集合。
3. 成員有變 → 完整重分析列為 V9 的開放驗證行動（FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET；FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED；`07` §8）；不以替換後集合取代凍結結果。
4. 標籤替換與證據單元重切分是不同的測量操作：協調與執行 × 一般決策流程在三種證據單元設定中皆持續，卻在標籤替換下退出。R14 註明重切分設定中「人工調和標籤不傳播至未稽核記錄」；V1.8 已核（`04` §3b，E49）：重切分未傳播任何人工標籤（受稽核但未被重切分的 22 筆在 S1／S2 中 22/22 保留模型家族），因此標籤處理不重疊；但記錄樣本部分重疊（50 筆中 28 筆亦被重切分，其中 11 筆因人工錯誤標記被強制納入候選）。
5. 稿件不推論兩個變動配對距離判定門檻多近（R14 沒有報告它們在文獻內部結構保持零模型下的 p_BH）。

---

## 6. 構念效度（V1）的現況

| 項目 | 內容 | 來源 |
|---|---|---|
| 研究者裁決 | 12 → M1–M4；G10 data-gated；G11、G12 → M5；G04 evidence-only | r14/05 §3 |
| AI 盲編 pilot | 兩個同家族 AI 編碼者彼此完全一致（預期中，不提供人類信度資訊）；與研究者主機制 14/16、狀態 13/16 一致；分歧 G04、G10、G11，皆 mapping-only | 54C |
| 人類雙盲 | `V1_HUMAN_BLIND_CODING_PENDING`；V1 通過條件：≥ 2 位人類、主碼與狀態信度至少 TENTATIVE 且非 IMPRECISE、無未解的模型結構性變更 | 60 輸出；127/130 §3.9.3 |
| EA-X 內容效度 | `CONDITIONAL_CANDIDATE`；人類 CVI 待完成 | 61 輸出；130 §4.7.4 |
| 統一狀態語句 | THEORETICAL CONVERGENCE COMPLETE；HUMAN CONSTRUCT VALIDATION PENDING | 130 §3.9.2、§4.7 |

---

## 7. 稿件整合位置

| 稿件位置 | 整合內容 |
|---|---|
| 稿件狀態說明、摘要、Abstract | 稽核狀態、κ 對比、四來源、替換結果、凍結基準 |
| 1.4、表 1-1、1.5、1.6 | 「凍結主要結果」；替換的局部變動；完整重分析 |
| 3.1.1 流程圖 | 新增替換節點 |
| 3.7.1 | 50/50、20/20、19/19；四來源 |
| 3.7.4（新） | 替換檢查的設計與三項判讀規則；程序細節 `[AUTHOR TO CONFIRM]` |
| 3.7.5（新標題） | 測量檢查與構念驗證的分界 |
| 3.8.1 表 3-3 | 新增 L2′ 層 |
| 3.8.2 規則 6（新） | 交接清單維持凍結 |
| 4.5.1 | 19/19、非 AI 盲、四來源 |
| 4.5.5（新）、表 4-9A | 替換結果與判讀 |
| 4.11 表 4-33 | RQ2 補替換結果 |
| 5.1、5.3.2 表 5-1 | 協調與執行 × 一般決策流程的敏感度；「已辨識」 |
| 5.4.2 | κ 與四來源作為方法學發現；替換段 |
| 5.8.2、5.8.9（新）、5.9、5.10 | 效度邊界、完整重分析 |
| 附錄 A、D、E39–E48 | S8 擴充、V9 來源列、待決事項 |

---

## 8. 未解事項

1. **V9 原始檔案：已取得並於 V1.8 部分核對**：替換清單（`04` T4）、變動配對、無其他核心成員變動、「凍結核心其餘 31 組不變」皆已逐列核對（E39）。殘留：替換後 q 值的產生腳本與 sidecar 核心檔 NOT_RECOVERED（只重現成員與判準，未重跑零模型）；12/37 受保護輸入未尋回；`HUMAN_AUDIT_APPEND_ONLY_LOG.csv` 受保護雜湊不符（UNVERIFIED，無竄改證據）（`02` §5）。
2. **完整重分析的時點與範圍**（現行：FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET；FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED；`07` §8；是否重跑仍屬研究者決定），以及人機增能 × 風險評估是否在重分析後進入交接清單（E40）。若重分析改變 L2，須依凍結程序重新產生 G 清單並重跑 V1 封包。
3. **3.7.4 的程序細節**（E48）：替換涵蓋 50 筆或其中 20 筆、矩陣重建方式、檢定組合、隨機種子。V1.8 部分解答：50 筆皆替換（20 筆用調和 FINAL 標籤、30 筆用第一位編碼者標籤；未稽核記錄不變，`04` Q4）；依 V9 `ROBUST_CORE_LOCAL_SENSITIVITY.md` 摘要（未逐列重現）：主零模型 10,000 次、seed 20260918；文獻內部結構保持零模型 5,000 次、seed 20260919；產生腳本 NOT_RECOVERED，標籤→納入資格的傳播規則 UNRESOLVED。
4. **兩種敏感度的處理範圍是否重疊**（E49）。V1.8 已核：標籤處理不重疊；記錄樣本 28/50 重疊（`04` §3b）。
5. **人類 V1 雙盲、EA-X CVI、ORG-V1–V5**（E6、E20）。
