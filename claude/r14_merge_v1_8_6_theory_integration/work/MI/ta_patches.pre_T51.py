TA = "auditor TA (OUT 05 / OUT 11 §B, audited sha 4d480a3e…)"
add("T29", "1.3 研究目的 3", "TA MAJOR-1 (05 O-1) l.113",
    "一組在本研究既定企業 AI 決策問題範圍內、操作上可區辨且在型別定義 T1–T4 下非冗餘的企業機制分解",
    "一組在本研究既定企業 AI 決策問題範圍內、以決策對象判準界定（其操作上的可區辨性待 V1 人類編碼檢驗）、且在型別定義 T1–T4 下對 v2.2 屬性結構非冗餘的企業機制分解",
    TA + " MAJOR-1 l.113")
add("T30", "3.9.6 定位", "TA MAJOR-1 (05 O-1) l.775",
    "操作上可區辨且在 T1–T4 型別定義下非冗餘的 mechanism decomposition",
    "以決策對象判準界定、且在 T1–T4 型別定義下對 v2.2 屬性結構非冗餘的 mechanism decomposition（操作上的可區辨性由 V1 檢驗，尚未執行）",
    TA + " MAJOR-1 l.775")
add("T31", "3.9.6 輔助類別", "TA MAJOR-2 (05 O-2) l.779",
    "NONE 是涵蓋缺口的訊號：存在可辨識的企業決策介面，但不在 M1–M4 工作集合內",
    "NONE 是涵蓋缺口的訊號：存在可辨識的企業決策過程（S1e 編碼者材料的用語；第 3.9.3 節沿用 S1d 的「企業決策介面」，兩者指同一判斷，S1e 只改編碼者用語與答案表版面，不改類別定義），但不在 M1–M4 工作集合內",
    TA + " MAJOR-2 l.779")
add("T32", "3.13 頂點精確性範圍", "TA m1 (05 O-3) l.1295 R4 converse",
    "只有在恰一個候選 portfolio 含該元素值時，頂點檢查才同時是必要條件（Prop R4）",
    "若恰一個候選 portfolio 含該元素值，頂點檢查同時也是必要條件（Prop R4；此為充分條件下的特例，不表示其他情形必不精確）",
    TA + " m1")
add("T33", "1.7.2 一般形式貢獻", "TA m2 l.182 generality qualifier",
    "對任何共用平台的資訊科技 portfolio 都成立",
    "對任何共用平台的資訊科技 portfolio 都成立（指具相同模型結構者的形式適用範圍，不是經驗上的可推廣性）",
    TA + " m2 (l.182)")
add("T34", "5.7 一般形式貢獻", "TA m2 l.2397 generality qualifier",
    "對任何共用平台的資訊科技 portfolio 皆成立",
    "對任何共用平台的資訊科技 portfolio 皆成立（指具相同模型結構者的形式適用範圍，不是經驗上的可推廣性）",
    TA + " m2 (l.2397, analogous clause)")
add("T35", "1.7.2 一般形式貢獻", "TA m3 l.182 V7 not run",
    "AI 特定的實證參數化（V7）",
    "AI 特定的實證參數化（V7，尚未執行）",
    TA + " m3")
add("T36", "5.6 理論補充的條件性意涵", "TA m4 l.2383 opt/pess index",
    "DL 為零若且唯若至少一個集中最適解可在雙層中自我實施",
    "樂觀（悲觀）DL 為零，若且唯若至少一個集中最適解在雙層中可樂觀（悲觀）自我實施",
    TA + " m4")
add("T37", "3.12.4 分類段 (A)", "TA m5 l.1161 complexity wording",
    "與求解 B 同樣困難",
    "因此至少需先求解 B 並取得全部首佳解",
    TA + " m5")
add("T38", "3.9.6 已建立與未建立", "TA m6 l.777 time residual",
    "，以及 AI 對 AI 的輸出鏈。",
    "，以及 AI 對 AI 的輸出鏈，以及時間（跨期）維度（由 LONGITUDINAL／M5 處理，不屬靜態 M1–M4）。",
    TA + " m6 (l.777)")
add("T39", "C.10.1 全域充分性", "TA m6 l.3035 time residual",
    "、AI 對 AI 的輸出鏈。M1–M4 的充分性狀態",
    "、AI 對 AI 的輸出鏈，以及時間（跨期）維度（由 LONGITUDINAL／M5 處理，不屬靜態 M1–M4）。M1–M4 的充分性狀態",
    TA + " m6 (l.3035)")
add("T40", "稿件狀態 (L5)", "TA m7 + m13 status-line disclosures",
    "附錄 C.10.9 另記一項 Lemma E′ 證明用語的勘誤（只改證明用語，不改任何數值）。",
    "附錄 C.10.9 另記一項 Lemma E′ 證明用語的勘誤（只改證明用語，不改任何數值）。P2 的備註用語依 Lemma S 精確化（P2 陳述不變）。"
    "理論補充包的整體判定為 PARTIAL（Q1_THEORY_UPGRADE_VERDICT = PARTIAL；附錄 D）。",
    TA + " m7, m13")
add("T41", "稿件狀態 (L5)", "TA m8 l.5 restatements not labelled TYPE C",
    "新增的形式結果皆為本研究的模型內結果（TYPE C）",
    "新增的形式結果（含以明確前提重寫的 v2.2 重述）皆為本研究的模型內結果",
    TA + " m8 (l.5)")
add("T42", "3.12.4 分類段標題", "TA m8 l.1159 header tag",
    "（v1.8.6；TYPE C；證明與構造例見附錄 C.10）",
    "（v1.8.6；重述與 TYPE C；證明與構造例見附錄 C.10）",
    TA + " m8 (l.1159)")
add("T43", "4.9.1 表 4-20D W7", "TA m9 l.2034",
    "Thm R1（正向對照）",
    "Thm R1（重述；正向對照）",
    TA + " m9 (l.2034)")
add("T44", "5.7 形式理論貢獻 (4)", "TA m9 l.2395(4)",
    "Prop E.1–E.7",
    "Prop E.1、E.4–E.6 與 Thm E.7（E.2、E.3 為重述）",
    TA + " m9 (l.2395)")
add("T45", "C.10.2 與 v2.2 的關係", "TA m10 C.6 P2 remark supersession note",
    "平手容差：有條件成立（只限精確可負擔）。",
    "平手容差：有條件成立（只限精確可負擔）。\n"
    "- **與 v2.2 的關係。** C.6 的 P2 備註（「需要池化資源」）依逐字原則保留；其精確條件為 Lemma S，第 3.12.4、5.6 節已改用此精確用語。",
    TA + " m10")
add("T46", "摘要", "TA m11 Abstract bounded screening wording",
    "但在雙層且帳本不對齊時可藉由篩除部門的不利選擇而提高企業價值。",
    "但在雙層且帳本不對齊時，在特定的錯位與可分離性條件下，可藉由篩除部門的不利選擇而提高企業價值（不是一般性質）。",
    TA + " m11 (Abstract l.15)")
add("T47", "Abstract", "TA m11 English Abstract matching edit (TA gave no EN text; minimal mirror)",
    "but can raise enterprise value by screening out harmful unit choices in the bilevel setting with misaligned ledgers.",
    "but can, under specific misalignment and separability conditions (not as a general property), raise enterprise value by screening out "
    "harmful unit choices in the bilevel setting with misaligned ledgers.",
    TA + " m11 (English Abstract l.31; wording by MI mirroring TA's zh text)")
add("T48", "3.12.4 治理篩選段", "TA m12 forward-reference order",
    "在下述分解中",
    "在本節稍後的治理價值分解中",
    TA + " m12 (second option)")
add("T49", "C.10.2 Cor DL-2p", "TA m14 exact ties",
    "**Cor DL-2p（推論；AL3）。**",
    "**Cor DL-2p（推論；AL3；精確平手）。**",
    TA + " m14")
add("T50", "C.10.3 Prop GS-1", "TA m15 near-definitional note",
    "則 `GSV^m = DL^m(Req_l)`。",
    "則 `GSV^m = DL^m(Req_l)`（經由 Lemma DL-1，近乎定義性；唯一首佳下為原始條件形式）。",
    TA + " m15")
