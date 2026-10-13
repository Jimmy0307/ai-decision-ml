"""Build v1.8 from v1.7 by exact old->new replacements (each must match exactly once).
Usage: python -I patch_v18.py <v1.7 md> <v1.8 md out> <patches json out>"""
import sys, json, hashlib

SRC, DST, JOUT = sys.argv[1], sys.argv[2], sys.argv[3]

FA_OLD = "〔來源：2026-09-29 人工驗證狀態紀錄（檔名 20260929_V9_HUMAN_VALIDATION；V9 是檔案版本名，不是驗證閘門）；原始檔案未在本稿工作環境中，投稿前須逐項核對；附錄 E39〕"
FA_NEW = "〔來源：V9 人工驗證套件（資料夾 20260929_V9_HUMAN_VALIDATION；V9 是檔案版本名，不是驗證閘門）之 FINAL_STATUS.json（驗證時間 2026-10-03）與 ROBUST_CORE_LOCAL_SENSITIVITY.csv；已逐列核對；附錄 E39〕"
FB_OLD = "〔2026-09-29 紀錄，待核〕"
FB_NEW = "〔V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv，已逐列核對〕"
FT_NEW = "〔V9 套件 FINAL_ERROR_TAXONOMY.csv，已核對〕"

P = []


def add(pid, sec, cat, old, new, src):
    P.append(dict(id=pid, section=sec, category=cat, old=old, new=new, source=src))


SENS = "V9/ROBUST_CORE_LOCAL_SENSITIVITY.csv (e3166ee1…) + 04_LOCAL_SENSITIVITY_REPRODUCTION.md"
STAT = "V9/FINAL_STATUS.json (d9226d31…, verified_at 2026-10-03T12:23:44Z) + 02_V9_AUTHORITY_MAP.md §3/§7"
TAX = "V9/FINAL_ERROR_TAXONOMY.csv/.md (68e97c01…) + 06 rows L591/L1559/L2262/L2376"
MEMO = "07_FULL_REANALYSIS_DECISION_MEMO.md §8 conditions (a)(b)"
SCOPE = "V9/ROBUST_CORE_LOCAL_SENSITIVITY.md (b25b9a84…), FINAL_STATUS.json; 04 §2 Q4, T4"

add("F01", "稿件狀態", "source provenance (version label)",
    "合併碩士論文 v1.7 EVIDENCE-CONVERGED CANDIDATE（由 v1.6 修訂；v1.0–v1.6 保留、未覆寫；歷次版本說明移至附錄 F）。本版不新增任何分析，也不改變任何方程、模型元素、R14 數值或 G01–G16 凍結值；只把既有證據的狀態收斂為一致的寫法。",
    "合併碩士論文 v1.8 SOURCE-VERIFIED CANDIDATE（由 v1.7 修訂；v1.0–v1.7 保留、未覆寫；歷次版本說明移至附錄 F）。本版不新增任何分析，也不改變任何方程、模型元素、R14 數值或 G01–G16 凍結值；v1.7 已把既有證據的狀態收斂為一致的寫法，v1.8 再以 V9 人工驗證套件的原始檔案逐列核對其來源，只更新來源標示、日期與相應措辭。",
    "02 §7-8; this round")
add("F02", "稿件狀態", "obsolete flag closed + local sensitivity wording + V9 final vs historical",
    "完整重分析尚待執行；凍結的 32 組（16 過度、16 不足）仍為正式推論基準（第 3.7.4、4.5.5 節）" + FA_OLD + "。",
    "此替換只重算 50 筆受稽核記錄的標籤（局部附屬重算，不是完整重分析）；V9 套件標記的完整重分析（FULL_REANALYSIS_REQUIRED）是否執行，仍為研究者待決事項（附錄 E40）；凍結的 32 組（16 過度、16 不足）仍為正式推論基準，人工稽核並未確認 32 組的個別成員（第 3.7.4、4.5.5 節）" + FA_NEW + "。",
    STAT + "; " + MEMO)
add("F03", "摘要", "human-validation wording (four-source as hypothesis; low agreement plain)",
    "高於對關係類型與單一功能家族的一致度（κ = .048–.180）；分歧可能同時來自模型映射、分類架構邊界、證據片段切分與全文擷取品質，不能單獨歸因於語言模型。",
    "高於對關係類型與單一功能家族的一致度（κ = .048–.180，屬低度一致）；依人工稽核錯誤型態表的詮釋性假設（非裁決），模型標籤與人工標籤的差異可能同時來自模型映射、分類架構邊界、證據片段切分與全文擷取品質，不能單獨歸因於語言模型。",
    TAX)
add("F04", "摘要", "obsolete flag closed + local sensitivity wording",
    "（新增一組不足呈現、移出一組過度呈現）" + FB_OLD + "；凍結的 32 組仍為正式推論基準，完整重分析尚待執行。",
    "（新增一組不足呈現、移出一組過度呈現）" + FB_NEW + "；此替換只重算 50 筆受稽核記錄的標籤，屬局部敏感度，不是完整重分析，也不表示人工稽核確認了 32 組的成員；凍結的 32 組仍為正式推論基準，完整重分析是否執行仍待研究者決定。",
    SENS + "; " + MEMO)
add("F05", "摘要", "obsolete flag closed",
    "未移除其中任何一組" + FB_OLD + "）只作為",
    "未移除其中任何一組" + FB_NEW + "）只作為", SENS + " T2")
add("F06", "Abstract", "human-validation wording (four-source as hypothesis; low agreement plain)",
    "than on relation type and single-family assignments (κ = .048–.180); the disagreements are consistent with several possible sources—",
    "than on relation type and single-family assignments (κ = .048–.180, i.e., low agreement); an interpretive error-taxonomy hypothesis in the validation package (not an adjudication) suggests that differences between model and human labels are consistent with several possible sources—",
    TAX)
add("F07", "Abstract", "obsolete flag closed + local sensitivity wording",
    "(one depletion entered and one enrichment left; as reported in the 2026-09-29 validation record, pending verification); the frozen 32-pairing core remains the official inferential baseline, and a full reanalysis is pending.",
    "(one depletion entered and one enrichment left; verified row by row against the V9 validation package). This substitution relabelled only the 50 audited records; it is a local sensitivity check, not a full reanalysis, and it does not show that human validation confirmed the 32-pairing membership. The frozen 32-pairing core remains the official inferential baseline, and whether to run the full reanalysis flagged by the validation package remains an open researcher decision.",
    SENS + "; " + MEMO)
add("F08", "1.5 研究設計概覽", "obsolete flag closed + local sensitivity wording",
    "完整重分析尚待執行（第 4.5.5 節）" + FA_OLD + "。",
    "此替換只重算受稽核記錄的標籤，完整重分析是否執行仍待研究者決定（第 4.5.5 節）" + FA_NEW + "。",
    STAT + "; " + MEMO)
add("F09", "3.7.1 研究者目標稽核與盲式第二編碼", "V9 final vs historical (re-date) + human-validation wording + integrity disclosure",
    "（人工稽核已收斂；狀態紀錄日期 2026-09-29）。依該紀錄的整理，分歧可能來自四類來源：模型映射歧義、分類架構邊界歧義、證據片段切分歧義（多功能或過寬的片段），以及 PDF／全文擷取品質（抽取破碎的片段）" + FB_OLD + "；因此本研究不把分歧單獨歸因於語言模型不準確。19 筆分歧尚未逐筆依這四類來源歸類。",
    "（人工稽核已收斂；V9 套件 FINAL_STATUS.json，驗證時間 2026-10-03；三項筆數與五欄 κ 已由原始編碼列重算一致）。調和前，關係類型、人工智慧家族與決策家族三欄的編碼者間一致度偏低（表 4-6），因此單一家族標籤不能視為已獲人工確認。另依 V9 錯誤型態表（FINAL_ERROR_TAXONOMY.csv）對受稽核記錄中模型標籤與人工標籤差異所作的詮釋性整理（非裁決），差異可能來自四類主要來源：模型映射歧義、分類架構邊界歧義、證據片段切分歧義（多功能或過寬的片段），以及 PDF／全文擷取品質（抽取破碎的片段）；該表另列少數真正的概念歧義案例，且各類來源可並存" + FT_NEW + "；因此本研究不把分歧單獨歸因於語言模型不準確。這項整理針對模型與人工標籤的差異，不是對兩位編碼者 19 筆分歧的分類；19 筆分歧尚未逐筆依這四類來源歸類。V9 套件的完整性紀錄另顯示，早期稽核日誌 HUMAN_AUDIT_APPEND_ONLY_LOG.csv 的現行雜湊與受保護基準不符（套件記為 LEGACY_AUDIT_LOG_INTEGRITY = UNVERIFIED，未發現竄改證據）；凍結的第一位編碼者檔、盲式第二編碼檔與調和檔的雜湊均與套件雜湊清單相符。此為來源完整性的限制（附錄 E39）。",
    STAT + "; 03 Phase 3/4; " + TAX + "; 02 §5 item 9")
add("F10", "3.7.4 目標式人工標籤替換敏感度", "obsolete '依作者回報' closed + human-validation wording (20+30) + local sensitivity wording",
    "依作者回報，此檢查以人工標籤（研究者審閱或調和後的標籤）替換受稽核記錄的模型標籤後，重新判定穩健集合。替換涵蓋的記錄（50 筆研究者審閱記錄，或其中 20 筆經第二編碼調和的記錄）、矩陣重建方式、未稽核記錄的處理、重算時採用的檢定組合與隨機種子，本稿無法由原始紀錄核對 `[AUTHOR TO CONFIRM：2026-09-29 人工驗證紀錄；附錄 E48]`。",
    "依 V9 套件紀錄（ROBUST_CORE_LOCAL_SENSITIVITY.md、FINAL_STATUS.json），此檢查只替換 50 筆受稽核記錄的標籤：其中 20 筆盲式第二編碼子樣本採研究者調和後的最終標籤，其餘 30 筆採第一位編碼者（研究者審閱）的標籤；未稽核記錄維持模型標籤；之後重建 120 格功能矩陣，以主要分析的四項統計／計數分析重新判定穩健集合（依套件摘要檔，沿用主要分析的隨機種子與重複次數）。這是局部附屬重算，不是全語料的完整重分析。替換標籤的來源（20 筆調和＋30 筆第一位編碼者）已與原始編碼檔逐列對照，替換前後的穩健集合成員也已由敏感度表逐列重現；但產生敏感度表的程式未隨套件保存，人工標籤中的「不確定」「模糊」「無法對應」如何轉為配對資格，無法由套件重現 `[AUTHOR TO CONFIRM：標籤至配對資格的傳播規則與重算程式；附錄 E48]`。",
    SCOPE)
add("F11", "3.7.4 目標式人工標籤替換敏感度", "obsolete flag closed (E49 resolved)",
    "兩者的處理範圍可能部分重疊——R14 註明重切分設定中「人工調和標籤不傳播至未稽核記錄」，受稽核記錄在重切分設定中是否已使用人工標籤，須以補充資料 S10 與 2026-09-29 紀錄核對（附錄 E49）。",
    "兩者的標籤來源不重疊：R14 註明重切分設定中「人工調和標籤不傳播至未稽核記錄」，V9 套件內的重切分紀錄（V9_1_SEGMENTATION_SENSITIVITY）進一步註明沒有任何調和或最終人工標籤傳播至候選或未稽核記錄，受稽核記錄在重切分設定中仍使用模型映射（未重切分的 22 筆經記錄層級檔逐列核對，皆沿用原模型家族；重切分者由模型重新映射）；人工稽核只以錯誤標記強制部分記錄進入重切分候選。兩者的記錄範圍則部分重疊：50 筆受稽核記錄中有 28 筆也是重切分候選（附錄 E49）。",
    "04 §3b; 06 row L607; V9/V9_1_SEGMENTATION_SENSITIVITY final report l.7")
add("F12", "3.7.4 目標式人工標籤替換敏感度", "V9 final vs historical (re-date) + obsolete flag closed + full-reanalysis open decision",
    "來自 2026-09-29 的人工驗證狀態紀錄" + FA_OLD + "。",
    "來自 V9 人工驗證套件的 FINAL_STATUS.json（驗證時間 2026-10-03），並已與原始編碼列及敏感度表逐列核對" + FA_NEW + "。依該檔，完整重分析須經研究者核准；是否在投稿前執行，仍為研究者待決事項（附錄 E40）。替換結果不表示人工稽核確認了 32 組的成員。",
    STAT + "; " + MEMO)
add("F13", "3.8.1 結果分層", "obsolete '依作者回報…待核' closed",
    "L2′ 依作者回報推得，待核。",
    "L2′ 取自 V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv（已逐列核對；屬局部附屬重算，不是完整重分析）。",
    SENS)
add("F14", "3.8.1 結果分層（表 3-3）", "obsolete flags closed + local sensitivity wording",
    "| 以人工標籤替換受稽核記錄後重新判定（依作者回報；判準待核） | 32（若無其他未回報的變動，推得 15／17：+1 不足、−1 過度） | 局部成員敏感度；不取代 L2；完整重分析待執行" + FB_OLD + " |",
    "| 以人工標籤替換 50 筆受稽核記錄後重新判定（判準同 L2） | 32（15／17：+1 不足、−1 過度） | 局部成員敏感度；不取代 L2；完整重分析待研究者決定" + FB_NEW + " |",
    SENS + " (promotion rule recomputed, 0 mismatches)")
add("F15", "3.8.2 規則 6", "obsolete flag closed",
    "不增列這一組（附錄 E40）" + FB_OLD + "。",
    "不增列這一組（附錄 E40）" + FB_NEW + "。", SENS + " T2")
add("F16", "3.9.2 表註", "obsolete flag closed",
    "未移除其中任何一格" + FB_OLD + "。",
    "未移除其中任何一格" + FB_NEW + "。", SENS + " T2")
add("F17", "4.5.1 人工稽核揭示的測量問題", "human-validation wording (low agreement plain)",
    "、.140 與 .316。",
    "、.140 與 .316；其中關係類型、人工智慧家族與決策家族三欄屬低度一致。",
    "03 Phase 4; V9/HUMAN_RELIABILITY_FINAL.csv")
add("F18", "4.5.1 人工稽核揭示的測量問題", "human-validation wording (four-source as hypothesis) + obsolete flag closed",
    "依 2026-09-29 紀錄的整理，分歧可能來自四類來源：模型映射歧義、分類架構邊界歧義、證據片段切分歧義（多功能或過寬的片段），以及 PDF／全文擷取品質（抽取破碎的片段）" + FB_OLD + "；19 筆分歧尚未逐筆依這四類歸類。",
    "V9 錯誤型態表（FINAL_ERROR_TAXONOMY.csv）對受稽核記錄中模型標籤與人工標籤差異所作的詮釋性整理（非裁決）指出，差異可能來自四類主要來源：模型映射歧義、分類架構邊界歧義、證據片段切分歧義（多功能或過寬的片段），以及 PDF／全文擷取品質（抽取破碎的片段），另有少數真正的概念歧義，且各類來源可並存" + FT_NEW + "；這項整理針對模型與人工標籤的差異，不是對兩位編碼者 19 筆分歧的分類，19 筆分歧尚未逐筆依這四類歸類。",
    TAX)
add("F19", "4.5.1 表 4-6 表註", "source provenance (cite HUMAN_RELIABILITY_FINAL.csv explicitly)",
    "表註：n = 20，均為人工調和前之探索性編碼者間一致度。",
    "表註：n = 20，均為人工調和前之探索性編碼者間一致度。點估計與信賴區間取自 V9 套件的 HUMAN_RELIABILITY_FINAL.csv；點估計已由原始編碼列重算一致，自助法信賴區間未重跑（套件中較早的 HUMAN_RELIABILITY_20.csv 因種子設定不同，後四欄的區間略有差異，本稿不引用）。",
    "03 Phase 4 CI observation; 02 §5 item 7")
add("F20", "4.5.5 目標式人工標籤替換的局部敏感度", "human-validation wording (20+30) + obsolete flag closed + full-reanalysis open decision",
    "依第 3.7.4 節，以人工調和後的標籤替換受稽核記錄的模型標籤並重新判定穩健集合後，穩健集合的格數仍為 32，但成員出現局部變動（表 4-9A）" + FA_OLD + "。人工稽核的狀態因此記為：人工稽核已收斂（HUMAN_AUDIT_CONVERGED）；局部敏感度改變成員（LOCAL_SENSITIVITY_CHANGED）；須完整重分析（FULL_REANALYSIS_REQUIRED）。",
    "依第 3.7.4 節，以人工標籤（20 筆採調和後的最終標籤、其餘 30 筆採第一位編碼者標籤）替換 50 筆受稽核記錄的模型標籤並重新判定穩健集合後，穩健集合的格數仍為 32，但成員出現局部變動（表 4-9A）" + FA_NEW + "。V9 套件據此把人工稽核的狀態記為：人工稽核已收斂（HUMAN_AUDIT_CONVERGED）；局部敏感度改變成員（LOCAL_SENSITIVITY_CHANGED）；須完整重分析（FULL_REANALYSIS_REQUIRED）。最後一項是套件的狀態標記；依 FINAL_STATUS.json，完整重分析須經研究者核准，是否執行仍為研究者待決事項（附錄 E40）。本節的替換只重算受稽核記錄的標籤，其餘記錄維持模型標籤，屬局部附屬重算，不是完整重分析。",
    STAT + "; " + SCOPE + "; " + MEMO)
add("F21", "4.5.5 表 4-9A 表註", "obsolete '作者回報/推得/待核' closed + local sensitivity wording (q=.05 boundary)",
    "表註：✓ 表示進入該設定的穩健集合。表中只列作者回報發生變動的配對；若無其他未回報的變動，替換後集合推得為 15 組過度呈現與 17 組不足呈現，凍結核心其餘 31 組不變" + FB_OLD + "。",
    "表註：✓ 表示進入該設定的穩健集合。表中列出 120 格逐列比對下全部發生成員變動的配對；替換後集合為 15 組過度呈現與 17 組不足呈現，凍結核心其餘 31 組的成員與方向皆不變" + FB_NEW + "。兩組變動都來自文獻內部結構保持零模型在 .05 判定門檻上的跨越，兩格本身的觀察次數均未改變；因此確切成員對標籤在判定門檻附近敏感。",
    SENS + " §1 mechanism, §2 Q1/Q3")
add("F22", "4.5.5 目標式人工標籤替換的局部敏感度", "obsolete '依作者回報' closed + local sensitivity wording",
    "R14 沒有報告這兩格在文獻內部結構保持零模型下的 p_BH，因此本稿不推論它們距離判定門檻多近。依作者回報的變動（若無其他未回報的變動），",
    "R14 定稿沒有報告這兩格在文獻內部結構保持零模型下的 p_BH；V9 敏感度表顯示兩格的成員變動都是該零模型在 .05 判定門檻上的跨越，本稿不另引入其數值。依 V9 套件的逐列結果，",
    SENS + " §1 mechanism")
add("F23", "4.11 研究問題的整合回答（表）", "obsolete flag closed",
    "凍結的 32 組仍為推論基準，完整重分析待執行" + FB_OLD + " |",
    "凍結的 32 組仍為推論基準，完整重分析待研究者決定" + FB_NEW + " |", SENS + "; " + MEMO)
add("F24", "5.1", "obsolete flag closed",
    "退出穩健集合（第 4.5.5 節）" + FB_OLD + "，",
    "退出穩健集合（第 4.5.5 節）" + FB_NEW + "，", SENS)
add("F25", "5.4.2", "human-validation wording (four-source as hypothesis) + obsolete flag closed",
    "依 2026-09-29 紀錄的整理，分歧可能來自四個可區分的來源——模型映射歧義、分類架構邊界歧義、證據片段切分歧義，以及 PDF／全文擷取品質" + FB_OLD + "；19 筆分歧尚未逐筆依這四類歸類，因此四類來源是待檢驗的分類，而不是已估計的比例。",
    "V9 錯誤型態表對受稽核記錄中模型與人工標籤差異所提出的詮釋性假設（非裁決）認為，差異可能來自四個可區分的來源——模型映射歧義、分類架構邊界歧義、證據片段切分歧義，以及 PDF／全文擷取品質（另有少數真正的概念歧義）" + FT_NEW + "；這項假設針對模型與人工標籤的差異，19 筆編碼者間分歧尚未逐筆依這四類歸類，因此四類來源是待檢驗的分類，而不是已估計的比例。",
    TAX)
add("F26", "5.4.2", "human-validation wording (20+30)",
    "以人工調和標籤替換受稽核記錄後，",
    "以人工標籤（20 筆調和後標籤、30 筆第一位編碼者標籤）替換 50 筆受稽核記錄後，",
    SCOPE + "; 04 §3a")
add("F27", "5.4.2", "obsolete flag closed + local sensitivity wording (q boundary)",
    "只有 19 筆文獻層級邊〔變動依 2026-09-29 紀錄，待核〕。",
    "只有 19 筆文獻層級邊" + FB_NEW + "。兩者的變動都發生在文獻內部結構保持零模型的判定門檻上。",
    SENS + " §1 mechanism")
add("F28", "5.8.9", "full-reanalysis open decision",
    "局部敏感度的存在使完整重分析成為必要的後續步驟：",
    "局部敏感度的存在使完整重分析成為必要的後續步驟（V9 套件標記為 FULL_REANALYSIS_REQUIRED；是否及何時執行仍待研究者決定，附錄 E40）：",
    STAT + "; " + MEMO)
add("F29", "5.8.9", "obsolete flag closed (E49 resolved)",
    "卻在標籤替換下退出" + FB_OLD + "，顯示兩種操作可能對同一配對給出不同結果；兩者的處理範圍是否部分重疊，待核（附錄 E49）。",
    "卻在標籤替換下退出" + FB_NEW + "，顯示兩種操作可能對同一配對給出不同結果；兩者的標籤來源不重疊（重切分不使用人工標籤），記錄範圍則部分重疊（附錄 E49）。",
    "04 §3b; " + SENS)
add("F30", "5.10 結論", "human-validation wording (four-source as hypothesis)",
    "人工稽核再指出，編碼分歧同時來自模型映射、分類邊界、證據切分與全文擷取品質，因而引出",
    "人工稽核則提示，模型與人工標籤的差異可能同時來自模型映射、分類邊界、證據切分與全文擷取品質（詮釋性假設，非裁決），因而引出",
    TAX + "; 06 row L2376")
add("F31", "5.10 結論", "obsolete flag closed",
    "一組過度呈現退出" + FB_OLD + "；",
    "一組過度呈現退出" + FB_NEW + "；", SENS)
add("F32", "附錄 A S8", "obsolete flag closed",
    "（V9，2026-09-29；待以原始檔案核對，附錄 E39）",
    "（V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv／_DIFF.csv／.md；已核對，附錄 E39）",
    SENS + " §0 (manifest-matched hashes)")
add("F33", "附錄 D V9 列", "obsolete 'not in workspace' closed + V9 final vs historical (re-date)",
    "| `20260929_V9_HUMAN_VALIDATION.zip`（不在本稿工作環境中） | 文獻層人工驗證狀態紀錄：稽核收斂、目標式人工標籤替換的局部敏感度 | 第 3.7.4、4.5.5、5.4.2、5.8.9 節；待核對（附錄 E39） |",
    "| `20260929_V9_HUMAN_VALIDATION.zip`（已納入工作環境；SHA-256 8f63e88e…；資料夾名中的日期為工作站建立日，狀態檔驗證時間為 2026-10-03） | 文獻層人工驗證套件：原始編碼檔、稽核收斂狀態、目標式人工標籤替換的局部敏感度 | 第 3.7.4、4.5.5、5.4.2、5.8.9 節；已逐列核對（附錄 E39） |",
    "W/00_INPUT_MANIFEST.csv (zip sha 8f63e88e…); 02 §3 timeline")
add("F34", "附錄 D 128 列", "source provenance (superseded ABSENT claim)",
    "| `128_CANONICAL_STATE.md` | 權威來源、衝突與停止條件的盤點 | 本稿的來源裁定 |",
    "| `128_CANONICAL_STATE.md` | 權威來源、衝突與停止條件的盤點 | v1.7 的來源裁定（其中 V9 套件「ABSENT」的判定已由 v1.8 的來源核對取代） |",
    "02 §4 last row; §5 item 12")
add("F35", "附錄 D 130 列", "source provenance (version)",
    "| 合併論文 v1.7 | 本稿 |",
    "| 合併論文 v1.7 | v1.8 的修訂底稿（已保存；未覆寫） |",
    "this round")
add("F36", "附錄 E E39", "obsolete 'not in workspace / 作者陳述' closed + integrity disclosure + V9 final vs historical",
    "| E39 | V9 人工驗證狀態紀錄（`20260929_V9_HUMAN_VALIDATION.zip`）不在本稿工作環境中。本稿中「19/19 調和完成」以外的稽核狀態（HUMAN_AUDIT_CONVERGED、LOCAL_SENSITIVITY_CHANGED、FULL_REANALYSIS_REQUIRED）與目標式人工標籤替換的結果，只來自作者 2026-10-13 的陳述；κ 值與 50／20／19 筆數已與 R14 定稿核對一致 |",
    "| E39 | 已解決（v1.8）：V9 人工驗證套件（`20260929_V9_HUMAN_VALIDATION.zip`；資料夾名中的日期為工作站建立日，第一位編碼者檔凍結於 2026-10-02，調和與狀態檔為 2026-10-03）已納入工作環境並逐列核對。50／20／19 筆數、五欄 κ、替換後的兩組變動配對、替換後集合 32（15／17）、凍結核心其餘 31 組不變、無其他成員變動，以及狀態標記（HUMAN_AUDIT_CONVERGED、LOCAL_SENSITIVITY_CHANGED、FULL_REANALYSIS_REQUIRED；SUBMISSION_READY = NO）皆與原始檔案一致。殘餘的來源限制：（a）FINAL_STATUS.json 記錄一項受保護雜湊不符（HUMAN_AUDIT_APPEND_ONLY_LOG.csv；LEGACY_AUDIT_LOG_INTEGRITY = UNVERIFIED，未發現竄改證據），凍結的編碼檔與調和檔雜湊完好；（b）套件受保護基準所列 37 項輸入中有 12 項（含原始 400／120 抽樣檔、V9 原稿、凍結資料庫與凍結清單）不在套件中，正式凍結核心檔只以套件內位元組相同的重現檔佐證；（c）替換後的核心檔與產生敏感度表的程式未隨套件保存，替換後成員係由敏感度表逐列重現；（d）κ 的自助法信賴區間取自 HUMAN_RELIABILITY_FINAL.csv，未重跑 |",
    "02 §2,§3,§5,§8; 03 verdict; 04 §1; 06 rows L3063")
add("F37", "附錄 E E39", "obsolete pending action closed",
    "| 投稿前以原始檔案逐項核對替換清單、替換後矩陣、變動配對、是否有其他未回報的變動，以及「凍結核心其餘 31 組不變」；不一致時以原始檔案為準並重寫上述各處 |",
    "| 已依原始檔案改寫上述各處的來源標示；殘餘限制（a）–（d）保留，傳播規則見 E48，完整重分析見 E40 |",
    "06 row L3063")
add("F38", "附錄 E E40", "full-reanalysis open decision (KEEP_AS_LIMITATION wording made accurate)",
    "| 作者決定在投稿前或投稿後執行；",
    "| V9 套件記為須經研究者核准；作者決定在投稿前或投稿後執行；重跑前須先補回缺件的受保護輸入（E39（b））並事先登記標籤傳播規則（E48）；",
    STAT + "; 07 §4,§7,§8")
add("F39", "附錄 E E44", "obsolete pending flag closed",
    "2026-09-29 人工驗證原始檔案待核（E39）、",
    "",
    "06 row L3068")
add("F40", "附錄 E E48", "obsolete pending flag closed; residual kept open (Phase-4 resolution)",
    "| E48 | 目標式人工標籤替換的程序細節（替換涵蓋 50 筆或其中 20 筆、矩陣重建方式、未稽核記錄的處理、重算的檢定組合與隨機種子）未在本稿中列出；三項判讀規則於 v1.7 撰寫時訂定，非事前登記 | 第 3.7.4 節 | 依 2026-09-29 原始紀錄逐項填入 `[AUTHOR TO CONFIRM]` |",
    "| E48 | 目標式人工標籤替換的程序細節：替換範圍（50 筆受稽核記錄；20 筆採調和標籤、30 筆採第一位編碼者標籤；未稽核記錄不變）與檢定組合已依 V9 套件紀錄列於第 3.7.4 節，替換後集合已由敏感度表逐列重現；人工標籤中「不確定」「模糊」「無法對應」轉為配對資格的規則，以及產生敏感度表的程式，未隨套件保存而無法重現；三項判讀規則於 v1.7 撰寫時訂定，非事前登記 | 第 3.7.4 節 | 由作者補述傳播規則並提供重算程式後，移除第 3.7.4 節的 `[AUTHOR TO CONFIRM]`；若執行完整重分析（E40），須事先登記此規則 |",
    SCOPE + "; 04 §2 Q4 (rule UNRESOLVED, generator NOT_RECOVERED)")
add("F41", "附錄 E E49", "obsolete pending flag closed (E49 resolved)",
    "| E49 | 證據單元重切分設定中，受稽核記錄是否已使用人工調和標籤（R14：人工調和標籤不傳播至未稽核記錄）；若是，標籤替換與重切分兩種敏感度的處理範圍部分重疊 | 第 3.7.4、5.8.9 節 | 以補充資料 S10 與 2026-09-29 紀錄核對後改寫兩節的比較語句 |",
    "| E49 | 已解決（v1.8）：V9 套件內的證據單元重切分紀錄（V9_1_SEGMENTATION_SENSITIVITY）註明沒有任何調和或最終人工標籤傳播至候選或未稽核記錄；記錄層級檔顯示未重切分的受稽核記錄皆沿用原模型家族，重切分者由模型重新映射，人工稽核只以錯誤標記強制部分記錄進入重切分候選。兩種敏感度的標籤來源不重疊，記錄範圍部分重疊（50 筆受稽核記錄中 28 筆亦為重切分候選） | 第 3.7.4、5.8.9 節 | 已依此改寫兩節的比較語句 |",
    "04 §3b; 06 rows L3073")

raw = open(SRC, 'rb').read()
orig = raw.decode('utf-8')
text = orig
for p in P:
    pos = orig.find(p['old'])
    p['count_in_v17'] = orig.count(p['old'])
    p['v17_line'] = orig[:pos].count('\n') + 1 if pos >= 0 else None
    c = text.count(p['old'])
    assert c == 1, f"{p['id']}: old string matched {c} times at apply time"
    text = text.replace(p['old'], p['new'], 1)
assert '\r' not in text
open(DST, 'wb').write(text.encode('utf-8'))
json.dump(P, open(JOUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('patches', len(P))
print('src sha', hashlib.sha256(raw).hexdigest())
print('dst sha', hashlib.sha256(text.encode('utf-8')).hexdigest())
for p in P:
    print(p['id'], 'v17 line', p['v17_line'], 'count_in_v17', p['count_in_v17'])
