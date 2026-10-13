# 08 — Patch log: v1.7 → v1.8 SOURCE-VERIFIED (Phase 9, sub-agent F)

Date: 2026-10-14.
- **Input:** `W/01_ALL_OUTPUTS/AI_DECISION_THESIS_ALL_OUTPUTS/r14_merge_v1_7/130_MERGED_MASTER_THESIS_R14_TO_ENTERPRISE_v1_7_EVIDENCE_CONVERGED_CANDIDATE.md` (sha256 `c28ecb3a315bc53e4acef63014599ba7d83ed563355532a2c57f474961295b97`, unchanged by this run).
- **Output:** `W/08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md` (sha256 `1515b0f241846b98a16bea7b13f07d1f82fa9199e1331c2228ffce1d04f7ad58`). 3,081 lines, as in v1.7. UTF-8, LF line endings, no BOM.
- **Method:** the v1.8 file is a copy of v1.7 patched by 41 exact old→new string replacements. Each `old` string was asserted to occur exactly once, both in v1.7 and at the moment it was applied. No newline was added or removed, so v1.7 and v1.8 line numbers coincide.
- **Authority used** (not re-derived): `02_V9_AUTHORITY_MAP.md`, `03_HUMAN_AUDIT_REPRODUCTION.md`, `04_LOCAL_SENSITIVITY_REPRODUCTION.md`, `05_LEGACY_SOURCE_BOUNDARY.md`, `06_SOURCE_FLAG_CLOSURE.csv` / `_NOTES.md` and `07_FULL_REANALYSIS_DECISION_MEMO.md`. I also read one package file directly: V9 `FINAL_ERROR_TAXONOMY.md`, to word the four-source hypothesis accurately.
- **Scripts** (run with `python -I`):
  - `C:\Users\user\AppData\Local\Temp\claude\C--NTUST-PAPER\b2185478-fbc8-4bee-8105-bb5557dd964b\scratchpad\v18\F\patch_v18.py` (`<v1.7> <v1.8 out> <patches.json>`) applies the replacements.
  - `C:\Users\user\AppData\Local\Temp\claude\C--NTUST-PAPER\b2185478-fbc8-4bee-8105-bb5557dd964b\scratchpad\v18\F\verify_v18.py` (`<v1.7> <v1.8> <verify_out.json>`) runs the checks in §2.
  - `C:\Users\user\AppData\Local\Temp\claude\C--NTUST-PAPER\b2185478-fbc8-4bee-8105-bb5557dd964b\scratchpad\v18\F\build_log.py` builds this file.
  - Intermediate outputs: `C:\Users\user\AppData\Local\Temp\claude\C--NTUST-PAPER\b2185478-fbc8-4bee-8105-bb5557dd964b\scratchpad\v18\F\patches.json` and `C:\Users\user\AppData\Local\Temp\claude\C--NTUST-PAPER\b2185478-fbc8-4bee-8105-bb5557dd964b\scratchpad\v18\F\verify_out.json`.

## 1. Change list

Every v1.7 line number below equals the v1.8 line number. Categories use the allowed-change list.

### F01 — v1.7 L5 — 稿件狀態
- **Category:** source provenance (version label)
- **Source artifact:** 02 §7-8; this round
- **Old:**
  > 合併碩士論文 v1.7 EVIDENCE-CONVERGED CANDIDATE（由 v1.6 修訂；v1.0–v1.6 保留、未覆寫；歷次版本說明移至附錄 F）。本版不新增任何分析，也不改變任何方程、模型元素、R14 數值或 G01–G16 凍結值；只把既有證據的狀態收斂為一致的寫法。
- **New:**
  > 合併碩士論文 v1.8 SOURCE-VERIFIED CANDIDATE（由 v1.7 修訂；v1.0–v1.7 保留、未覆寫；歷次版本說明移至附錄 F）。本版不新增任何分析，也不改變任何方程、模型元素、R14 數值或 G01–G16 凍結值；v1.7 已把既有證據的狀態收斂為一致的寫法，v1.8 再以 V9 人工驗證套件的原始檔案逐列核對其來源，只更新來源標示、日期與相應措辭。

### F02 — v1.7 L5 — 稿件狀態
- **Category:** obsolete flag closed + local sensitivity wording + V9 final vs historical
- **Source artifact:** V9/FINAL_STATUS.json (d9226d31…, verified_at 2026-10-03T12:23:44Z) + 02_V9_AUTHORITY_MAP.md §3/§7; 07_FULL_REANALYSIS_DECISION_MEMO.md §8 conditions (a)(b)
- **Old:**
  > 完整重分析尚待執行；凍結的 32 組（16 過度、16 不足）仍為正式推論基準（第 3.7.4、4.5.5 節）〔來源：2026-09-29 人工驗證狀態紀錄（檔名 20260929_V9_HUMAN_VALIDATION；V9 是檔案版本名，不是驗證閘門）；原始檔案未在本稿工作環境中，投稿前須逐項核對；附錄 E39〕。
- **New:**
  > 此替換只重算 50 筆受稽核記錄的標籤（局部附屬重算，不是完整重分析）；V9 套件標記的完整重分析（FULL_REANALYSIS_REQUIRED）是否執行，仍為研究者待決事項（附錄 E40）；凍結的 32 組（16 過度、16 不足）仍為正式推論基準，人工稽核並未確認 32 組的個別成員（第 3.7.4、4.5.5 節）〔來源：V9 人工驗證套件（資料夾 20260929_V9_HUMAN_VALIDATION；V9 是檔案版本名，不是驗證閘門）之 FINAL_STATUS.json（驗證時間 2026-10-03）與 ROBUST_CORE_LOCAL_SENSITIVITY.csv；已逐列核對；附錄 E39〕。

### F03 — v1.7 L13 — 摘要
- **Category:** human-validation wording (four-source as hypothesis; low agreement plain)
- **Source artifact:** V9/FINAL_ERROR_TAXONOMY.csv/.md (68e97c01…) + 06 rows L591/L1559/L2262/L2376
- **Old:**
  > 高於對關係類型與單一功能家族的一致度（κ = .048–.180）；分歧可能同時來自模型映射、分類架構邊界、證據片段切分與全文擷取品質，不能單獨歸因於語言模型。
- **New:**
  > 高於對關係類型與單一功能家族的一致度（κ = .048–.180，屬低度一致）；依人工稽核錯誤型態表的詮釋性假設（非裁決），模型標籤與人工標籤的差異可能同時來自模型映射、分類架構邊界、證據片段切分與全文擷取品質，不能單獨歸因於語言模型。

### F04 — v1.7 L13 — 摘要
- **Category:** obsolete flag closed + local sensitivity wording
- **Source artifact:** V9/ROBUST_CORE_LOCAL_SENSITIVITY.csv (e3166ee1…) + 04_LOCAL_SENSITIVITY_REPRODUCTION.md; 07_FULL_REANALYSIS_DECISION_MEMO.md §8 conditions (a)(b)
- **Old:**
  > （新增一組不足呈現、移出一組過度呈現）〔2026-09-29 紀錄，待核〕；凍結的 32 組仍為正式推論基準，完整重分析尚待執行。
- **New:**
  > （新增一組不足呈現、移出一組過度呈現）〔V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv，已逐列核對〕；此替換只重算 50 筆受稽核記錄的標籤，屬局部敏感度，不是完整重分析，也不表示人工稽核確認了 32 組的成員；凍結的 32 組仍為正式推論基準，完整重分析是否執行仍待研究者決定。

### F05 — v1.7 L15 — 摘要
- **Category:** obsolete flag closed
- **Source artifact:** V9/ROBUST_CORE_LOCAL_SENSITIVITY.csv (e3166ee1…) + 04_LOCAL_SENSITIVITY_REPRODUCTION.md T2
- **Old:**
  > 未移除其中任何一組〔2026-09-29 紀錄，待核〕）只作為
- **New:**
  > 未移除其中任何一組〔V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv，已逐列核對〕）只作為

### F06 — v1.7 L29 — Abstract
- **Category:** human-validation wording (four-source as hypothesis; low agreement plain)
- **Source artifact:** V9/FINAL_ERROR_TAXONOMY.csv/.md (68e97c01…) + 06 rows L591/L1559/L2262/L2376
- **Old:**
  > than on relation type and single-family assignments (κ = .048–.180); the disagreements are consistent with several possible sources—
- **New:**
  > than on relation type and single-family assignments (κ = .048–.180, i.e., low agreement); an interpretive error-taxonomy hypothesis in the validation package (not an adjudication) suggests that differences between model and human labels are consistent with several possible sources—

### F07 — v1.7 L29 — Abstract
- **Category:** obsolete flag closed + local sensitivity wording
- **Source artifact:** V9/ROBUST_CORE_LOCAL_SENSITIVITY.csv (e3166ee1…) + 04_LOCAL_SENSITIVITY_REPRODUCTION.md; 07_FULL_REANALYSIS_DECISION_MEMO.md §8 conditions (a)(b)
- **Old:**
  > (one depletion entered and one enrichment left; as reported in the 2026-09-29 validation record, pending verification); the frozen 32-pairing core remains the official inferential baseline, and a full reanalysis is pending.
- **New:**
  > (one depletion entered and one enrichment left; verified row by row against the V9 validation package). This substitution relabelled only the 50 audited records; it is a local sensitivity check, not a full reanalysis, and it does not show that human validation confirmed the 32-pairing membership. The frozen 32-pairing core remains the official inferential baseline, and whether to run the full reanalysis flagged by the validation package remains an open researcher decision.

### F08 — v1.7 L158 — 1.5 研究設計概覽
- **Category:** obsolete flag closed + local sensitivity wording
- **Source artifact:** V9/FINAL_STATUS.json (d9226d31…, verified_at 2026-10-03T12:23:44Z) + 02_V9_AUTHORITY_MAP.md §3/§7; 07_FULL_REANALYSIS_DECISION_MEMO.md §8 conditions (a)(b)
- **Old:**
  > 完整重分析尚待執行（第 4.5.5 節）〔來源：2026-09-29 人工驗證狀態紀錄（檔名 20260929_V9_HUMAN_VALIDATION；V9 是檔案版本名，不是驗證閘門）；原始檔案未在本稿工作環境中，投稿前須逐項核對；附錄 E39〕。
- **New:**
  > 此替換只重算受稽核記錄的標籤，完整重分析是否執行仍待研究者決定（第 4.5.5 節）〔來源：V9 人工驗證套件（資料夾 20260929_V9_HUMAN_VALIDATION；V9 是檔案版本名，不是驗證閘門）之 FINAL_STATUS.json（驗證時間 2026-10-03）與 ROBUST_CORE_LOCAL_SENSITIVITY.csv；已逐列核對；附錄 E39〕。

### F09 — v1.7 L591 — 3.7.1 研究者目標稽核與盲式第二編碼
- **Category:** V9 final vs historical (re-date) + human-validation wording + integrity disclosure
- **Source artifact:** V9/FINAL_STATUS.json (d9226d31…, verified_at 2026-10-03T12:23:44Z) + 02_V9_AUTHORITY_MAP.md §3/§7; 03 Phase 3/4; V9/FINAL_ERROR_TAXONOMY.csv/.md (68e97c01…) + 06 rows L591/L1559/L2262/L2376; 02 §5 item 9
- **Old:**
  > （人工稽核已收斂；狀態紀錄日期 2026-09-29）。依該紀錄的整理，分歧可能來自四類來源：模型映射歧義、分類架構邊界歧義、證據片段切分歧義（多功能或過寬的片段），以及 PDF／全文擷取品質（抽取破碎的片段）〔2026-09-29 紀錄，待核〕；因此本研究不把分歧單獨歸因於語言模型不準確。19 筆分歧尚未逐筆依這四類來源歸類。
- **New:**
  > （人工稽核已收斂；V9 套件 FINAL_STATUS.json，驗證時間 2026-10-03；三項筆數與五欄 κ 已由原始編碼列重算一致）。調和前，關係類型、人工智慧家族與決策家族三欄的編碼者間一致度偏低（表 4-6），因此單一家族標籤不能視為已獲人工確認。另依 V9 錯誤型態表（FINAL_ERROR_TAXONOMY.csv）對受稽核記錄中模型標籤與人工標籤差異所作的詮釋性整理（非裁決），差異可能來自四類主要來源：模型映射歧義、分類架構邊界歧義、證據片段切分歧義（多功能或過寬的片段），以及 PDF／全文擷取品質（抽取破碎的片段）；該表另列少數真正的概念歧義案例，且各類來源可並存〔V9 套件 FINAL_ERROR_TAXONOMY.csv，已核對〕；因此本研究不把分歧單獨歸因於語言模型不準確。這項整理針對模型與人工標籤的差異，不是對兩位編碼者 19 筆分歧的分類；19 筆分歧尚未逐筆依這四類來源歸類。V9 套件的完整性紀錄另顯示，早期稽核日誌 HUMAN_AUDIT_APPEND_ONLY_LOG.csv 的現行雜湊與受保護基準不符（套件記為 LEGACY_AUDIT_LOG_INTEGRITY = UNVERIFIED，未發現竄改證據）；凍結的第一位編碼者檔、盲式第二編碼檔與調和檔的雜湊均與套件雜湊清單相符。此為來源完整性的限制（附錄 E39）。

### F10 — v1.7 L605 — 3.7.4 目標式人工標籤替換敏感度
- **Category:** obsolete '依作者回報' closed + human-validation wording (20+30) + local sensitivity wording
- **Source artifact:** V9/ROBUST_CORE_LOCAL_SENSITIVITY.md (b25b9a84…), FINAL_STATUS.json; 04 §2 Q4, T4
- **Old:**
  > 依作者回報，此檢查以人工標籤（研究者審閱或調和後的標籤）替換受稽核記錄的模型標籤後，重新判定穩健集合。替換涵蓋的記錄（50 筆研究者審閱記錄，或其中 20 筆經第二編碼調和的記錄）、矩陣重建方式、未稽核記錄的處理、重算時採用的檢定組合與隨機種子，本稿無法由原始紀錄核對 `[AUTHOR TO CONFIRM：2026-09-29 人工驗證紀錄；附錄 E48]`。
- **New:**
  > 依 V9 套件紀錄（ROBUST_CORE_LOCAL_SENSITIVITY.md、FINAL_STATUS.json），此檢查只替換 50 筆受稽核記錄的標籤：其中 20 筆盲式第二編碼子樣本採研究者調和後的最終標籤，其餘 30 筆採第一位編碼者（研究者審閱）的標籤；未稽核記錄維持模型標籤；之後重建 120 格功能矩陣，以主要分析的四項統計／計數分析重新判定穩健集合（依套件摘要檔，沿用主要分析的隨機種子與重複次數）。這是局部附屬重算，不是全語料的完整重分析。替換標籤的來源（20 筆調和＋30 筆第一位編碼者）已與原始編碼檔逐列對照，替換前後的穩健集合成員也已由敏感度表逐列重現；但產生敏感度表的程式未隨套件保存，人工標籤中的「不確定」「模糊」「無法對應」如何轉為配對資格，無法由套件重現 `[AUTHOR TO CONFIRM：標籤至配對資格的傳播規則與重算程式；附錄 E48]`。

### F11 — v1.7 L607 — 3.7.4 目標式人工標籤替換敏感度
- **Category:** obsolete flag closed (E49 resolved)
- **Source artifact:** 04 §3b; 06 row L607; V9/V9_1_SEGMENTATION_SENSITIVITY final report l.7
- **Old:**
  > 兩者的處理範圍可能部分重疊——R14 註明重切分設定中「人工調和標籤不傳播至未稽核記錄」，受稽核記錄在重切分設定中是否已使用人工標籤，須以補充資料 S10 與 2026-09-29 紀錄核對（附錄 E49）。
- **New:**
  > 兩者的標籤來源不重疊：R14 註明重切分設定中「人工調和標籤不傳播至未稽核記錄」，V9 套件內的重切分紀錄（V9_1_SEGMENTATION_SENSITIVITY）進一步註明沒有任何調和或最終人工標籤傳播至候選或未稽核記錄，受稽核記錄在重切分設定中仍使用模型映射（未重切分的 22 筆經記錄層級檔逐列核對，皆沿用原模型家族；重切分者由模型重新映射）；人工稽核只以錯誤標記強制部分記錄進入重切分候選。兩者的記錄範圍則部分重疊：50 筆受稽核記錄中有 28 筆也是重切分候選（附錄 E49）。

### F12 — v1.7 L609 — 3.7.4 目標式人工標籤替換敏感度
- **Category:** V9 final vs historical (re-date) + obsolete flag closed + full-reanalysis open decision
- **Source artifact:** V9/FINAL_STATUS.json (d9226d31…, verified_at 2026-10-03T12:23:44Z) + 02_V9_AUTHORITY_MAP.md §3/§7; 07_FULL_REANALYSIS_DECISION_MEMO.md §8 conditions (a)(b)
- **Old:**
  > 來自 2026-09-29 的人工驗證狀態紀錄〔來源：2026-09-29 人工驗證狀態紀錄（檔名 20260929_V9_HUMAN_VALIDATION；V9 是檔案版本名，不是驗證閘門）；原始檔案未在本稿工作環境中，投稿前須逐項核對；附錄 E39〕。
- **New:**
  > 來自 V9 人工驗證套件的 FINAL_STATUS.json（驗證時間 2026-10-03），並已與原始編碼列及敏感度表逐列核對〔來源：V9 人工驗證套件（資料夾 20260929_V9_HUMAN_VALIDATION；V9 是檔案版本名，不是驗證閘門）之 FINAL_STATUS.json（驗證時間 2026-10-03）與 ROBUST_CORE_LOCAL_SENSITIVITY.csv；已逐列核對；附錄 E39〕。依該檔，完整重分析須經研究者核准；是否在投稿前執行，仍為研究者待決事項（附錄 E40）。替換結果不表示人工稽核確認了 32 組的成員。

### F13 — v1.7 L619 — 3.8.1 結果分層
- **Category:** obsolete '依作者回報…待核' closed
- **Source artifact:** V9/ROBUST_CORE_LOCAL_SENSITIVITY.csv (e3166ee1…) + 04_LOCAL_SENSITIVITY_REPRODUCTION.md
- **Old:**
  > L2′ 依作者回報推得，待核。
- **New:**
  > L2′ 取自 V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv（已逐列核對；屬局部附屬重算，不是完整重分析）。

### F14 — v1.7 L630 — 3.8.1 結果分層（表 3-3）
- **Category:** obsolete flags closed + local sensitivity wording
- **Source artifact:** V9/ROBUST_CORE_LOCAL_SENSITIVITY.csv (e3166ee1…) + 04_LOCAL_SENSITIVITY_REPRODUCTION.md (promotion rule recomputed, 0 mismatches)
- **Old:**
  > | 以人工標籤替換受稽核記錄後重新判定（依作者回報；判準待核） | 32（若無其他未回報的變動，推得 15／17：+1 不足、−1 過度） | 局部成員敏感度；不取代 L2；完整重分析待執行〔2026-09-29 紀錄，待核〕 |
- **New:**
  > | 以人工標籤替換 50 筆受稽核記錄後重新判定（判準同 L2） | 32（15／17：+1 不足、−1 過度） | 局部成員敏感度；不取代 L2；完整重分析待研究者決定〔V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv，已逐列核對〕 |

### F15 — v1.7 L645 — 3.8.2 規則 6
- **Category:** obsolete flag closed
- **Source artifact:** V9/ROBUST_CORE_LOCAL_SENSITIVITY.csv (e3166ee1…) + 04_LOCAL_SENSITIVITY_REPRODUCTION.md T2
- **Old:**
  > 不增列這一組（附錄 E40）〔2026-09-29 紀錄，待核〕。
- **New:**
  > 不增列這一組（附錄 E40）〔V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv，已逐列核對〕。

### F16 — v1.7 L716 — 3.9.2 表註
- **Category:** obsolete flag closed
- **Source artifact:** V9/ROBUST_CORE_LOCAL_SENSITIVITY.csv (e3166ee1…) + 04_LOCAL_SENSITIVITY_REPRODUCTION.md T2
- **Old:**
  > 未移除其中任何一格〔2026-09-29 紀錄，待核〕。
- **New:**
  > 未移除其中任何一格〔V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv，已逐列核對〕。

### F17 — v1.7 L1559 — 4.5.1 人工稽核揭示的測量問題
- **Category:** human-validation wording (low agreement plain)
- **Source artifact:** 03 Phase 4; V9/HUMAN_RELIABILITY_FINAL.csv
- **Old:**
  > 、.140 與 .316。
- **New:**
  > 、.140 與 .316；其中關係類型、人工智慧家族與決策家族三欄屬低度一致。

### F18 — v1.7 L1559 — 4.5.1 人工稽核揭示的測量問題
- **Category:** human-validation wording (four-source as hypothesis) + obsolete flag closed
- **Source artifact:** V9/FINAL_ERROR_TAXONOMY.csv/.md (68e97c01…) + 06 rows L591/L1559/L2262/L2376
- **Old:**
  > 依 2026-09-29 紀錄的整理，分歧可能來自四類來源：模型映射歧義、分類架構邊界歧義、證據片段切分歧義（多功能或過寬的片段），以及 PDF／全文擷取品質（抽取破碎的片段）〔2026-09-29 紀錄，待核〕；19 筆分歧尚未逐筆依這四類歸類。
- **New:**
  > V9 錯誤型態表（FINAL_ERROR_TAXONOMY.csv）對受稽核記錄中模型標籤與人工標籤差異所作的詮釋性整理（非裁決）指出，差異可能來自四類主要來源：模型映射歧義、分類架構邊界歧義、證據片段切分歧義（多功能或過寬的片段），以及 PDF／全文擷取品質（抽取破碎的片段），另有少數真正的概念歧義，且各類來源可並存〔V9 套件 FINAL_ERROR_TAXONOMY.csv，已核對〕；這項整理針對模型與人工標籤的差異，不是對兩位編碼者 19 筆分歧的分類，19 筆分歧尚未逐筆依這四類歸類。

### F19 — v1.7 L1573 — 4.5.1 表 4-6 表註
- **Category:** source provenance (cite HUMAN_RELIABILITY_FINAL.csv explicitly)
- **Source artifact:** 03 Phase 4 CI observation; 02 §5 item 7
- **Old:**
  > 表註：n = 20，均為人工調和前之探索性編碼者間一致度。
- **New:**
  > 表註：n = 20，均為人工調和前之探索性編碼者間一致度。點估計與信賴區間取自 V9 套件的 HUMAN_RELIABILITY_FINAL.csv；點估計已由原始編碼列重算一致，自助法信賴區間未重跑（套件中較早的 HUMAN_RELIABILITY_20.csv 因種子設定不同，後四欄的區間略有差異，本稿不引用）。

### F20 — v1.7 L1629 — 4.5.5 目標式人工標籤替換的局部敏感度
- **Category:** human-validation wording (20+30) + obsolete flag closed + full-reanalysis open decision
- **Source artifact:** V9/FINAL_STATUS.json (d9226d31…, verified_at 2026-10-03T12:23:44Z) + 02_V9_AUTHORITY_MAP.md §3/§7; V9/ROBUST_CORE_LOCAL_SENSITIVITY.md (b25b9a84…), FINAL_STATUS.json; 04 §2 Q4, T4; 07_FULL_REANALYSIS_DECISION_MEMO.md §8 conditions (a)(b)
- **Old:**
  > 依第 3.7.4 節，以人工調和後的標籤替換受稽核記錄的模型標籤並重新判定穩健集合後，穩健集合的格數仍為 32，但成員出現局部變動（表 4-9A）〔來源：2026-09-29 人工驗證狀態紀錄（檔名 20260929_V9_HUMAN_VALIDATION；V9 是檔案版本名，不是驗證閘門）；原始檔案未在本稿工作環境中，投稿前須逐項核對；附錄 E39〕。人工稽核的狀態因此記為：人工稽核已收斂（HUMAN_AUDIT_CONVERGED）；局部敏感度改變成員（LOCAL_SENSITIVITY_CHANGED）；須完整重分析（FULL_REANALYSIS_REQUIRED）。
- **New:**
  > 依第 3.7.4 節，以人工標籤（20 筆採調和後的最終標籤、其餘 30 筆採第一位編碼者標籤）替換 50 筆受稽核記錄的模型標籤並重新判定穩健集合後，穩健集合的格數仍為 32，但成員出現局部變動（表 4-9A）〔來源：V9 人工驗證套件（資料夾 20260929_V9_HUMAN_VALIDATION；V9 是檔案版本名，不是驗證閘門）之 FINAL_STATUS.json（驗證時間 2026-10-03）與 ROBUST_CORE_LOCAL_SENSITIVITY.csv；已逐列核對；附錄 E39〕。V9 套件據此把人工稽核的狀態記為：人工稽核已收斂（HUMAN_AUDIT_CONVERGED）；局部敏感度改變成員（LOCAL_SENSITIVITY_CHANGED）；須完整重分析（FULL_REANALYSIS_REQUIRED）。最後一項是套件的狀態標記；依 FINAL_STATUS.json，完整重分析須經研究者核准，是否執行仍為研究者待決事項（附錄 E40）。本節的替換只重算受稽核記錄的標籤，其餘記錄維持模型標籤，屬局部附屬重算，不是完整重分析。

### F21 — v1.7 L1638 — 4.5.5 表 4-9A 表註
- **Category:** obsolete '作者回報/推得/待核' closed + local sensitivity wording (q=.05 boundary)
- **Source artifact:** V9/ROBUST_CORE_LOCAL_SENSITIVITY.csv (e3166ee1…) + 04_LOCAL_SENSITIVITY_REPRODUCTION.md §1 mechanism, §2 Q1/Q3
- **Old:**
  > 表註：✓ 表示進入該設定的穩健集合。表中只列作者回報發生變動的配對；若無其他未回報的變動，替換後集合推得為 15 組過度呈現與 17 組不足呈現，凍結核心其餘 31 組不變〔2026-09-29 紀錄，待核〕。
- **New:**
  > 表註：✓ 表示進入該設定的穩健集合。表中列出 120 格逐列比對下全部發生成員變動的配對；替換後集合為 15 組過度呈現與 17 組不足呈現，凍結核心其餘 31 組的成員與方向皆不變〔V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv，已逐列核對〕。兩組變動都來自文獻內部結構保持零模型在 .05 判定門檻上的跨越，兩格本身的觀察次數均未改變；因此確切成員對標籤在判定門檻附近敏感。

### F22 — v1.7 L1640 — 4.5.5 目標式人工標籤替換的局部敏感度
- **Category:** obsolete '依作者回報' closed + local sensitivity wording
- **Source artifact:** V9/ROBUST_CORE_LOCAL_SENSITIVITY.csv (e3166ee1…) + 04_LOCAL_SENSITIVITY_REPRODUCTION.md §1 mechanism
- **Old:**
  > R14 沒有報告這兩格在文獻內部結構保持零模型下的 p_BH，因此本稿不推論它們距離判定門檻多近。依作者回報的變動（若無其他未回報的變動），
- **New:**
  > R14 定稿沒有報告這兩格在文獻內部結構保持零模型下的 p_BH；V9 敏感度表顯示兩格的成員變動都是該零模型在 .05 判定門檻上的跨越，本稿不另引入其數值。依 V9 套件的逐列結果，

### F23 — v1.7 L2183 — 4.11 研究問題的整合回答（表）
- **Category:** obsolete flag closed
- **Source artifact:** V9/ROBUST_CORE_LOCAL_SENSITIVITY.csv (e3166ee1…) + 04_LOCAL_SENSITIVITY_REPRODUCTION.md; 07_FULL_REANALYSIS_DECISION_MEMO.md §8 conditions (a)(b)
- **Old:**
  > 凍結的 32 組仍為推論基準，完整重分析待執行〔2026-09-29 紀錄，待核〕 |
- **New:**
  > 凍結的 32 組仍為推論基準，完整重分析待研究者決定〔V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv，已逐列核對〕 |

### F24 — v1.7 L2206 — 5.1
- **Category:** obsolete flag closed
- **Source artifact:** V9/ROBUST_CORE_LOCAL_SENSITIVITY.csv (e3166ee1…) + 04_LOCAL_SENSITIVITY_REPRODUCTION.md
- **Old:**
  > 退出穩健集合（第 4.5.5 節）〔2026-09-29 紀錄，待核〕，
- **New:**
  > 退出穩健集合（第 4.5.5 節）〔V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv，已逐列核對〕，

### F25 — v1.7 L2262 — 5.4.2
- **Category:** human-validation wording (four-source as hypothesis) + obsolete flag closed
- **Source artifact:** V9/FINAL_ERROR_TAXONOMY.csv/.md (68e97c01…) + 06 rows L591/L1559/L2262/L2376
- **Old:**
  > 依 2026-09-29 紀錄的整理，分歧可能來自四個可區分的來源——模型映射歧義、分類架構邊界歧義、證據片段切分歧義，以及 PDF／全文擷取品質〔2026-09-29 紀錄，待核〕；19 筆分歧尚未逐筆依這四類歸類，因此四類來源是待檢驗的分類，而不是已估計的比例。
- **New:**
  > V9 錯誤型態表對受稽核記錄中模型與人工標籤差異所提出的詮釋性假設（非裁決）認為，差異可能來自四個可區分的來源——模型映射歧義、分類架構邊界歧義、證據片段切分歧義，以及 PDF／全文擷取品質（另有少數真正的概念歧義）〔V9 套件 FINAL_ERROR_TAXONOMY.csv，已核對〕；這項假設針對模型與人工標籤的差異，19 筆編碼者間分歧尚未逐筆依這四類歸類，因此四類來源是待檢驗的分類，而不是已估計的比例。

### F26 — v1.7 L2268 — 5.4.2
- **Category:** human-validation wording (20+30)
- **Source artifact:** V9/ROBUST_CORE_LOCAL_SENSITIVITY.md (b25b9a84…), FINAL_STATUS.json; 04 §2 Q4, T4; 04 §3a
- **Old:**
  > 以人工調和標籤替換受稽核記錄後，
- **New:**
  > 以人工標籤（20 筆調和後標籤、30 筆第一位編碼者標籤）替換 50 筆受稽核記錄後，

### F27 — v1.7 L2268 — 5.4.2
- **Category:** obsolete flag closed + local sensitivity wording (q boundary)
- **Source artifact:** V9/ROBUST_CORE_LOCAL_SENSITIVITY.csv (e3166ee1…) + 04_LOCAL_SENSITIVITY_REPRODUCTION.md §1 mechanism
- **Old:**
  > 只有 19 筆文獻層級邊〔變動依 2026-09-29 紀錄，待核〕。
- **New:**
  > 只有 19 筆文獻層級邊〔V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv，已逐列核對〕。兩者的變動都發生在文獻內部結構保持零模型的判定門檻上。

### F28 — v1.7 L2362 — 5.8.9
- **Category:** full-reanalysis open decision
- **Source artifact:** V9/FINAL_STATUS.json (d9226d31…, verified_at 2026-10-03T12:23:44Z) + 02_V9_AUTHORITY_MAP.md §3/§7; 07_FULL_REANALYSIS_DECISION_MEMO.md §8 conditions (a)(b)
- **Old:**
  > 局部敏感度的存在使完整重分析成為必要的後續步驟：
- **New:**
  > 局部敏感度的存在使完整重分析成為必要的後續步驟（V9 套件標記為 FULL_REANALYSIS_REQUIRED；是否及何時執行仍待研究者決定，附錄 E40）：

### F29 — v1.7 L2362 — 5.8.9
- **Category:** obsolete flag closed (E49 resolved)
- **Source artifact:** 04 §3b; V9/ROBUST_CORE_LOCAL_SENSITIVITY.csv (e3166ee1…) + 04_LOCAL_SENSITIVITY_REPRODUCTION.md
- **Old:**
  > 卻在標籤替換下退出〔2026-09-29 紀錄，待核〕，顯示兩種操作可能對同一配對給出不同結果；兩者的處理範圍是否部分重疊，待核（附錄 E49）。
- **New:**
  > 卻在標籤替換下退出〔V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv，已逐列核對〕，顯示兩種操作可能對同一配對給出不同結果；兩者的標籤來源不重疊（重切分不使用人工標籤），記錄範圍則部分重疊（附錄 E49）。

### F30 — v1.7 L2376 — 5.10 結論
- **Category:** human-validation wording (four-source as hypothesis)
- **Source artifact:** V9/FINAL_ERROR_TAXONOMY.csv/.md (68e97c01…) + 06 rows L591/L1559/L2262/L2376; 06 row L2376
- **Old:**
  > 人工稽核再指出，編碼分歧同時來自模型映射、分類邊界、證據切分與全文擷取品質，因而引出
- **New:**
  > 人工稽核則提示，模型與人工標籤的差異可能同時來自模型映射、分類邊界、證據切分與全文擷取品質（詮釋性假設，非裁決），因而引出

### F31 — v1.7 L2378 — 5.10 結論
- **Category:** obsolete flag closed
- **Source artifact:** V9/ROBUST_CORE_LOCAL_SENSITIVITY.csv (e3166ee1…) + 04_LOCAL_SENSITIVITY_REPRODUCTION.md
- **Old:**
  > 一組過度呈現退出〔2026-09-29 紀錄，待核〕；
- **New:**
  > 一組過度呈現退出〔V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv，已逐列核對〕；

### F32 — v1.7 L2664 — 附錄 A S8
- **Category:** obsolete flag closed
- **Source artifact:** V9/ROBUST_CORE_LOCAL_SENSITIVITY.csv (e3166ee1…) + 04_LOCAL_SENSITIVITY_REPRODUCTION.md §0 (manifest-matched hashes)
- **Old:**
  > （V9，2026-09-29；待以原始檔案核對，附錄 E39）
- **New:**
  > （V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv／_DIFF.csv／.md；已核對，附錄 E39）

### F33 — v1.7 L3008 — 附錄 D V9 列
- **Category:** obsolete 'not in workspace' closed + V9 final vs historical (re-date)
- **Source artifact:** W/00_INPUT_MANIFEST.csv (zip sha 8f63e88e…); 02 §3 timeline
- **Old:**
  > | `20260929_V9_HUMAN_VALIDATION.zip`（不在本稿工作環境中） | 文獻層人工驗證狀態紀錄：稽核收斂、目標式人工標籤替換的局部敏感度 | 第 3.7.4、4.5.5、5.4.2、5.8.9 節；待核對（附錄 E39） |
- **New:**
  > | `20260929_V9_HUMAN_VALIDATION.zip`（已納入工作環境；SHA-256 8f63e88e…；資料夾名中的日期為工作站建立日，狀態檔驗證時間為 2026-10-03） | 文獻層人工驗證套件：原始編碼檔、稽核收斂狀態、目標式人工標籤替換的局部敏感度 | 第 3.7.4、4.5.5、5.4.2、5.8.9 節；已逐列核對（附錄 E39） |

### F34 — v1.7 L3010 — 附錄 D 128 列
- **Category:** source provenance (superseded ABSENT claim)
- **Source artifact:** 02 §4 last row; §5 item 12
- **Old:**
  > | `128_CANONICAL_STATE.md` | 權威來源、衝突與停止條件的盤點 | 本稿的來源裁定 |
- **New:**
  > | `128_CANONICAL_STATE.md` | 權威來源、衝突與停止條件的盤點 | v1.7 的來源裁定（其中 V9 套件「ABSENT」的判定已由 v1.8 的來源核對取代） |

### F35 — v1.7 L3012 — 附錄 D 130 列
- **Category:** source provenance (version)
- **Source artifact:** this round
- **Old:**
  > | 合併論文 v1.7 | 本稿 |
- **New:**
  > | 合併論文 v1.7 | v1.8 的修訂底稿（已保存；未覆寫） |

### F36 — v1.7 L3063 — 附錄 E E39
- **Category:** obsolete 'not in workspace / 作者陳述' closed + integrity disclosure + V9 final vs historical
- **Source artifact:** 02 §2,§3,§5,§8; 03 verdict; 04 §1; 06 rows L3063
- **Old:**
  > | E39 | V9 人工驗證狀態紀錄（`20260929_V9_HUMAN_VALIDATION.zip`）不在本稿工作環境中。本稿中「19/19 調和完成」以外的稽核狀態（HUMAN_AUDIT_CONVERGED、LOCAL_SENSITIVITY_CHANGED、FULL_REANALYSIS_REQUIRED）與目標式人工標籤替換的結果，只來自作者 2026-10-13 的陳述；κ 值與 50／20／19 筆數已與 R14 定稿核對一致 |
- **New:**
  > | E39 | 已解決（v1.8）：V9 人工驗證套件（`20260929_V9_HUMAN_VALIDATION.zip`；資料夾名中的日期為工作站建立日，第一位編碼者檔凍結於 2026-10-02，調和與狀態檔為 2026-10-03）已納入工作環境並逐列核對。50／20／19 筆數、五欄 κ、替換後的兩組變動配對、替換後集合 32（15／17）、凍結核心其餘 31 組不變、無其他成員變動，以及狀態標記（HUMAN_AUDIT_CONVERGED、LOCAL_SENSITIVITY_CHANGED、FULL_REANALYSIS_REQUIRED；SUBMISSION_READY = NO）皆與原始檔案一致。殘餘的來源限制：（a）FINAL_STATUS.json 記錄一項受保護雜湊不符（HUMAN_AUDIT_APPEND_ONLY_LOG.csv；LEGACY_AUDIT_LOG_INTEGRITY = UNVERIFIED，未發現竄改證據），凍結的編碼檔與調和檔雜湊完好；（b）套件受保護基準所列 37 項輸入中有 12 項（含原始 400／120 抽樣檔、V9 原稿、凍結資料庫與凍結清單）不在套件中，正式凍結核心檔只以套件內位元組相同的重現檔佐證；（c）替換後的核心檔與產生敏感度表的程式未隨套件保存，替換後成員係由敏感度表逐列重現；（d）κ 的自助法信賴區間取自 HUMAN_RELIABILITY_FINAL.csv，未重跑 |

### F37 — v1.7 L3063 — 附錄 E E39
- **Category:** obsolete pending action closed
- **Source artifact:** 06 row L3063
- **Old:**
  > | 投稿前以原始檔案逐項核對替換清單、替換後矩陣、變動配對、是否有其他未回報的變動，以及「凍結核心其餘 31 組不變」；不一致時以原始檔案為準並重寫上述各處 |
- **New:**
  > | 已依原始檔案改寫上述各處的來源標示；殘餘限制（a）–（d）保留，傳播規則見 E48，完整重分析見 E40 |

### F38 — v1.7 L3064 — 附錄 E E40
- **Category:** full-reanalysis open decision (KEEP_AS_LIMITATION wording made accurate)
- **Source artifact:** V9/FINAL_STATUS.json (d9226d31…, verified_at 2026-10-03T12:23:44Z) + 02_V9_AUTHORITY_MAP.md §3/§7; 07 §4,§7,§8
- **Old:**
  > | 作者決定在投稿前或投稿後執行；
- **New:**
  > | V9 套件記為須經研究者核准；作者決定在投稿前或投稿後執行；重跑前須先補回缺件的受保護輸入（E39（b））並事先登記標籤傳播規則（E48）；

### F39 — v1.7 L3068 — 附錄 E E44
- **Category:** obsolete pending flag closed
- **Source artifact:** 06 row L3068
- **Old:**
  > 2026-09-29 人工驗證原始檔案待核（E39）、
- **New:**
  > (deleted; empty string)

### F40 — v1.7 L3072 — 附錄 E E48
- **Category:** obsolete pending flag closed; residual kept open (Phase-4 resolution)
- **Source artifact:** V9/ROBUST_CORE_LOCAL_SENSITIVITY.md (b25b9a84…), FINAL_STATUS.json; 04 §2 Q4, T4; 04 §2 Q4 (rule UNRESOLVED, generator NOT_RECOVERED)
- **Old:**
  > | E48 | 目標式人工標籤替換的程序細節（替換涵蓋 50 筆或其中 20 筆、矩陣重建方式、未稽核記錄的處理、重算的檢定組合與隨機種子）未在本稿中列出；三項判讀規則於 v1.7 撰寫時訂定，非事前登記 | 第 3.7.4 節 | 依 2026-09-29 原始紀錄逐項填入 `[AUTHOR TO CONFIRM]` |
- **New:**
  > | E48 | 目標式人工標籤替換的程序細節：替換範圍（50 筆受稽核記錄；20 筆採調和標籤、30 筆採第一位編碼者標籤；未稽核記錄不變）與檢定組合已依 V9 套件紀錄列於第 3.7.4 節，替換後集合已由敏感度表逐列重現；人工標籤中「不確定」「模糊」「無法對應」轉為配對資格的規則，以及產生敏感度表的程式，未隨套件保存而無法重現；三項判讀規則於 v1.7 撰寫時訂定，非事前登記 | 第 3.7.4 節 | 由作者補述傳播規則並提供重算程式後，移除第 3.7.4 節的 `[AUTHOR TO CONFIRM]`；若執行完整重分析（E40），須事先登記此規則 |

### F41 — v1.7 L3073 — 附錄 E E49
- **Category:** obsolete pending flag closed (E49 resolved)
- **Source artifact:** 04 §3b; 06 rows L3073
- **Old:**
  > | E49 | 證據單元重切分設定中，受稽核記錄是否已使用人工調和標籤（R14：人工調和標籤不傳播至未稽核記錄）；若是，標籤替換與重切分兩種敏感度的處理範圍部分重疊 | 第 3.7.4、5.8.9 節 | 以補充資料 S10 與 2026-09-29 紀錄核對後改寫兩節的比較語句 |
- **New:**
  > | E49 | 已解決（v1.8）：V9 套件內的證據單元重切分紀錄（V9_1_SEGMENTATION_SENSITIVITY）註明沒有任何調和或最終人工標籤傳播至候選或未稽核記錄；記錄層級檔顯示未重切分的受稽核記錄皆沿用原模型家族，重切分者由模型重新映射，人工稽核只以錯誤標記強制部分記錄進入重切分候選。兩種敏感度的標籤來源不重疊，記錄範圍部分重疊（50 筆受稽核記錄中 28 筆亦為重切分候選） | 第 3.7.4、5.8.9 節 | 已依此改寫兩節的比較語句 |

## 2. Verification results (from `verify_out.json`)

34 lines changed: 5, 13, 15, 29, 158, 591, 605, 607, 609, 619, 630, 645, 716, 1559, 1573, 1629, 1638, 1640, 2183, 2206, 2262, 2268, 2362, 2376, 2378, 2664, 3008, 3010, 3012, 3063, 3064, 3068, 3072, 3073. Line count: 3081 → 3081.

### 2.1 Math and equations
**PASS.**
- **Display and inline math:** all `$$…$$` blocks (18), inline `$…$` spans (31), `\begin…\end` environments (0) and `\[…\]` spans (7) are identical as multisets: True.
- **Fenced code blocks:** 4 blocks, identical: True.
- **Math-marker lines:** 136 lines of v1.7 contain a math or code marker (`$`, `\(`, `\[`, `\begin`, `\frac`, `\sum`, `_{`, `^{`, fences). Changed: none. Changed lines containing any such marker: none.
- **Definitions:** VCP / VSC / DL / NEV token counts are unchanged (VCP [28, 28], VSC [26, 26], DL [59, 59], NEV [28, 28]).
- **`=` tokens in changed lines:** the only ones are status labels, `SUBMISSION_READY = NO` and `LEGACY_AUDIT_LOG_INTEGRITY = UNVERIFIED`, plus the unchanged string `κ = .048–.180` in L29, which now has a suffix. None is an equation.

### 2.2 Numeric tokens (whole-document multiset)
**Removed:**
- `{"19/19": 1, "2026-09-29": 29, "2026-10-13": 1}`
- `2026-09-29` ×29: every status or reconciliation date. It is re-dated to 2026-10-03 or replaced by a file citation. The folder name `20260929_V9_HUMAN_VALIDATION` is kept.
- `2026-10-13`: E39's "作者 2026-10-13 的陳述". It is superseded because the raw files are now present.
- `19/19`: E39's "「19/19 調和完成」以外的稽核狀態". The sentence was rewritten as resolved. 19/19 still appears unchanged at L5 and L591.

**Added:**
- `{"32": 5, "50": 8, "3.7.4": 2, "2026-10-03": 8, "12": 1, "120": 3, "20": 3, "19": 2, "30": 5, ".05": 2, "8": 1, "22": 1, "15": 1, "28": 2, "37": 1, "400": 1, "4-6": 1, "17": 1, "256": 1, "2026-10-02": 1}`

Justification by token. No frozen R14 empirical value (O, E, O/E, q, κ, CI, 32/16/16, 29/30, 47, 2,180, 3,125, …) changed.
- **Dates.** `2026-10-03` ×8 is the FINAL_STATUS verified_at date and the reconciliation date (02 §3). `2026-10-02` ×1 is the first-coder freeze (02 §3 #9).
- **Restatements of numbers already reported in v1.7:**
  - `32`, `50`, `20`, `19`, `120`, `15`, `17`: the 32-cell core, the 50 audited records, the 20-record blind subset, the 19 disagreements, the 120 cells and 15/17.
  - `4-6` is a table reference (表 4-6), and `3.7.4` is a section reference.
- **`30`** is the number of first-coder-labelled records in the sidecar: 50 − 20. Source: ROBUST_CORE_LOCAL_SENSITIVITY.md and FINAL_STATUS.json. The per-record label source is confirmed from rows in 04 T4. This is source-verified provenance, not a result.
- **`28`** is the number of the 50 audited records that are also re-segmentation candidates (04 §3b, row-level). **`22`** is the number of audited records not re-segmented that keep model families, 22/22 (04 §3b and 06 row L607). These are E49 resolution facts. No reported segmentation result was changed.
- **`37`, `12`, `400`** are provenance-limitation counts: 12 of 37 protected inputs are absent, including the original 400/120 samples (02 §5 item 10 and §8). They are disclosed in E39(b).
- **`.05`** ×2 is the existing BH promotion threshold. It is used to state that both membership changes cross the q = .05 line of the document-preserving null (04 §1). No q-value was added.
- **`8`, `256`** are not numbers: they come from `SHA-256 8f63e88e…`, the V9 zip hash prefix in W/00_INPUT_MANIFEST.csv.

### 2.3 G01–G16 and G→M
- 122 v1.7 lines contain a G01–G16 token.
- G table rows changed: **none**.
- Prose lines containing G tokens that were edited: [5, 15, 158, 645, 716, 1638]. In these only flag or provenance text changed. The G-token multiset per changed line is identical (True), and the whole-document G-token count is 288 → 288.
- `G## → M#` arrow tokens are identical: True. No G list, taxonomy, G→M mapping or solver text was touched.

### 2.4 Remaining flags in v1.8 (all intentionally kept)
- **`20260929`** at L5, 158, 609, 1629, 3008 and 3063: this is only the package or folder name, which the instructions say to keep. Every one of these occurrences now carries the 2026-10-03 status date.
- **`待核` at L3045 (E25/E34/E36, "Vial, 2019 的內容待核對"):** OPEN_SOURCE_NOT_FOUND. It is a reference-verification item outside the V9 scope.
- **`工作環境中` at L651 (V5 Data Pack original not in workspace):** OPEN_SOURCE_NOT_FOUND. The V9.1 Stage-2 verification corroborates the digest and settings, but it is not the main-run Data Pack. Left open; see §4.
- **`工作環境中` at L3070 (E46, submission-format files):** OPEN_SOURCE_NOT_FOUND, outside the V9 scope.
- **`AUTHOR TO CONFIRM` at L605 and L3072:** the E48 residual. The label→pair-eligibility propagation rule is UNRESOLVED (04 §2 Q4) and the sidecar generator is NOT_RECOVERED. The marker is kept, but its content was corrected: the obsolete "2026-09-29 人工驗證紀錄" was removed and the marker now names the actually missing item.
- **`推得` at L847 and L1827:** this is not a V9 flag. These are model-definition sentences in §3.10 and §3.12 and were not touched.
- **Absent from v1.8:** `2026-09-29`, `依作者回報`, `作者回報`, `pending verification`, `原始檔案未在`, `只來自作者`, `人工調和後的標籤替換` and `人工調和標籤替換` all have 0 hits.
- **Other KEEP_AS_LIMITATION markers** (`[EMPIRICAL RESULT PENDING]`, `[HUMAN RESULT PENDING]`, the `[VERIFY` at L2594, and the UNVERIFIED references N6, N35 and N66) are untouched.

### 2.5 Headings
182 headings in v1.7 and 182 in v1.8. The lists are identical in order and text: True.

### 2.6 Coverage-asymmetry check (abstract vs full text)
- The v1.7 body contains no abstract/full-text coverage-asymmetry claim.
- The phrase occurs only in Appendix E. **E1 (L3025)** records it as a RETIRED CLAIM. **E41 (L3065)** records that the author's request is not supported by R14, which says all candidates came from 1,729 parseable full texts.
- L334 ("核對層級（全文或摘要）") refers to the reference-verification level, not corpus coverage.
- Nothing to remove; E1 and E41 are kept as the record of retirement.

### 2.7 Ethics wording
- **§3.14.7 (L1364–1366) and E50 (L3074):** these already state that only a DRAFT protocol exists and that no company authorization, individual consent or institutional review/exemption has been obtained. They also state that the conditions must be met before any V0/V2/V7 data collection.
- There is no consent or IRB claim beyond this, so nothing was changed.

### 2.8 Legacy source boundary
- v1.7 never names `完整資料來源`.
- 05 found 0 improper merges. Its 結構洞 / Burt hits are theory or boundary text and are already framed as not tested.
- The only wrong description of the legacy zip is in 128 L15, an artifact and not the manuscript. v1.8 therefore has no legacy edit. The 128 row of Appendix D (F34) now notes only that 128's V9-ABSENT verdict is superseded.

## 3. Phase-4 resolution of the six OPEN_NEEDS_PHASE4 rows in 06

The 06 CSV itself was not modified. Evidence comes from 03 (Phase 3/4 recomputation) and 04 (local sensitivity reproduction).

| # | 06 row (file, line, flag) | Needed evidence | Resolution with 03/04 | New status | v1.8 action |
|---|---|---|---|---|---|
| 1 | 130 L605 `[AUTHOR TO CONFIRM：2026-09-29 人工驗證紀錄；附錄 E48]` | replacement scope, matrix rebuild, untouched records, test set, seeds | **Scope CONFIRMED.** 04 T4 rebuilds the 50 audited records' human labels from raw rows: 20 RECONCILED_FINAL from HUMAN_RECONCILED_20 (4b7ceac2…) and 30 FIRST_CODER from FIRST_CODER_50_FINAL_FROZEN (dd332dd8…). Unaudited records are unchanged, and STATUS.json reports 6,499 strict records unchanged and model_calls 0. Membership and the promotion rule were reproduced from 120 CSV rows with 0 mismatches. **Seeds and reps** (10,000 / 20260918; 5,000 / 20260919) appear only in the summary md/json, because the generator is NOT_RECOVERED. **The eligibility propagation rule is UNRESOLVED**: none of 5 candidate rules gives the −18 delta. | PARTIALLY CLOSED: scope and membership CONFIRMED; seeds PROBABLE (summary only); propagation rule UNRESOLVED | F10: 「依作者回報」 replaced by a V9 file citation; 20+30 scope stated; seeds attributed to the package summary file. The marker is kept with its content corrected to the rule and generator. |
| 2 | 130 L605 「依作者回報…人工標籤（研究者審閱或調和後的標籤）」 | replacement label source | CONFIRMED at row level (04 T4/T5). In 18/20 reconciled records the FINAL label differs from the first-coder label, so the sidecar input really is mixed-source. | CLOSED_SOURCE_VERIFIED | F10 (and F20, F26 for L1629 and L2268) |
| 3 | 130 L3072 E48 `[AUTHOR TO CONFIRM]` | same as #1 | same as #1 | PARTIALLY CLOSED (residual = propagation rule + generator) | F40: E48 rewritten. The residual stays open as an author action. |
| 4 | 130 L3072 E48 「依 2026-09-29 原始紀錄逐項填入」 | same as #1 | The obsolete date and the "fill from the original record" action are superseded. The record has been consulted; what remains is not in the record. | CLOSED (date/action); residual as #3 | F40 |
| 5 | 131 L129 `[AUTHOR TO CONFIRM]` | same as #1 | same as #1 | PARTIALLY CLOSED (artifact 131 not edited; it is a v1.7 artifact superseded by 02) | none in manuscript |
| 6 | 136 L53 `[AUTHOR TO CONFIRM]` (removal of internal flags before submission) | E48 row-level reproduction | E39 is closed in v1.8. E48 keeps one corrected marker until the author supplies the propagation rule and script. | PARTIALLY CLOSED | none in manuscript (artifact 136 not edited) |

Related PENDING_PHASE4 note in 06 (not one of the six rows): the Table 4-6 bootstrap CIs.
- 03 reproduced the κ point estimates within 0.0005. The CIs equal HUMAN_RELIABILITY_FINAL.csv but were not re-run.
- `_20` CIs differ for C2–C5 by ≤ .006 because of the seed scheme.
- F19 now cites HUMAN_RELIABILITY_FINAL.csv explicitly and says the CIs were not re-run. **Status: CLOSED as provenance; CI bootstrap UNRESOLVED as to canonical seed scheme (no number changed).**

## 4. Deliberately NOT changed (and why)

1. **Equations and models.** No equation, LaTeX or math block, VCP/VSC/DL/NEV definition, solver semantics, taxonomy, G01–G16 list or content, G→M mapping or Table 3-4A row was touched (FORBIDDEN list; verified in §2.1 and §2.3).
2. **Empirical numbers.** None changed: κ, CIs, agreement rates, 14/19/9/33-of-42, O/E, q tiers, 32/16/16, 29/30, 15/17, 47, 2,180, 3,125 and so on.
   - 06 notes that V9 rows hold the document-null q for the two changed pairs (.0567 / .0435). L1640 still declines to introduce them.
   - It now says only that both cross the .05 threshold (04 §1). Adding the q-values themselves is left to the author.
3. **Generic "完整重分析尚待執行／待執行" wording** at L105, 112, 122, 147, 168, 405, 412, 1625, 2190, 2238 and 2366 is left as is.
   - These lines agree with the package status FULL_REANALYSIS_REQUIRED (06 §4 rates them consistent).
   - The open-researcher-decision qualification was added at the main locations: L5, 13, 29, 158, 609, 630, 1629, 2183, 2362 and E40.
   - Rewriting every occurrence would go beyond the minimal-edit scope.
4. **L651, the V5 Data Pack provenance.** It stays OPEN_SOURCE_NOT_FOUND. The optional corroboration sentence from 06 (V9.1 Stage-2 verification with the same digest, Q4_K_M, temperature 0, seed 20260909 and num_ctx 8192) was not added. It would add numeric tokens, and it corroborates the settings but does not close the original-file gap.
5. **Segmentation-sensitivity numbers and attribution** (L13 "29 與 30", L601, §3.7.3, §4.5.2–4.5.4, S10) are unchanged.
   - v1.7 already marks G07 and G15 as evidence-unit boundary-sensitive, which agrees with 04 §3b: segmentation drops G15 in S1 and S2 and G07 in S1.
   - The claim "G01–G16 none removed" is already scoped to the label-replacement sidecar in every location (L15, 31, 356, 645, 716, 1638, 2238), so no edit was needed.
   - 02 §6 notes that the 84–85/120 re-segmentation figures come from the V9.1 sidecar. v1.7 attributes the segmentation analysis to R14. That attribution was not changed because no v1.8 evidence round audited it. **Flag for the next round.**
6. **Generic human-validation lines** L254, L529, L1015, L2354, E15 and E24 refer to generic or other validation (ORG-V, v2.4 candidates), not V9.
7. **The `[AUTHOR TO CONFIRM]` placeholders** were kept as placeholders. Only their obsolete content was corrected (L605). No author-name or byline placeholder was touched.
8. **Appendix F and its heading** ("v1.0–v1.6") are unchanged, because the heading list must stay identical. The v1.7 status paragraph was not copied into F. L5 now names v1.8 and states that v1.7 is preserved; F35 records 130 as the base copy.
9. **E1 and E41 (coverage-asymmetry retirement) and E50 / §3.14.7 (ethics)** were already accurate and were left unchanged.
10. **The artifacts 128, 129, 131, 132 (.csv/.xlsx), 133, 136, 137 and the 130 .docx** were not edited (manuscript-only scope).
    - **Packaging follow-up:** 132 still carries 16× `〔2026-09-29 紀錄，待核〕` (06 §3). The .docx must be regenerated from the v1.8 md. Per the task, no docx was produced.
11. **E44 (L3068).** Only the obsolete component "2026-09-29 人工驗證原始檔案待核（E39）" was deleted. SUBMISSION_READY = NO remains, consistent with V9 FINAL_STATUS submission_ready = false.
12. **`SUBMISSION_READY = NO；理由見附錄 E39–E46` (L5)** is kept. E39 still carries the residual provenance limitations (a)–(d).

## 5. STOP / conflict conditions
- **No STOP condition.** All 41 replacements matched exactly once.
- No empirical number conflicts with the raw-row evidence in 03 and 04.
- **Residual open items:**
  - E48: propagation rule and generator.
  - E40: full reanalysis, an open researcher decision; 07 recommends NO before v1.
  - E39(a)–(d): provenance limitations, with V9_SOURCE_VERIFIED = PARTIAL.
  - L651: Data Pack.
  - The non-V9 reference flags.
