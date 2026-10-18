"""Build V1.8.6a PRECISION HARMONIZATION + ERRATUM LINEAGE CLOSURE from V1.8.6 (01) by exact old->new replacements.
Each `old` must occur exactly once in V1.8.6 01 and exactly once at apply time (no layered patches).
Scope (common_v186a.txt + orchestrator brief PH): RD-1 terminology (企業決策機制; S1e coder-facing 企業決策過程),
RD-2 provenance phrase for P1-P8, RD-5 outer precision cleanup, claim-consistency sweep fix, version label (L5),
Appendix C.10.9 lineage bullet, Appendix D row.
No math blocks, no G rows, no Table 3-4/3-4A rows, no P1-P8 bullets, no Study 1 numbers, no new citations,
no global replace of 介面.
Usage: python -I patch_v186a.py <V1.8.6 01 md> <V1.8.6a 01 out md> <patches json out>"""
import sys, json, hashlib

SRC, DST, JOUT = sys.argv[1], sys.argv[2], sys.argv[3]
EXPECTED_SRC_SHA = "94d41d5682818953912784d0e870d58d1e4c418e7261b619d5c73485dfee82f4"

raw = open(SRC, 'rb').read()
if hashlib.sha256(raw).hexdigest() != EXPECTED_SRC_SHA:
    sys.exit("STOP: V1.8.6 01 manuscript hash unexpectedly changed")

P = []


def add(pid, sec, cat, old, new, src):
    P.append(dict(id=pid, section=sec, category=cat, old=old, new=new, source=src))


M06 = "V1.8.6 06 status matrix"
S1E = "S1e records (V1_S1E_CURRENT_STATUS.md; S1E_PROCESS_WORDING_CHANGELOG.md; FREEZE_MANIFEST_V1_S1E_PROCESS_WORDING.txt)"
CF = "common_v186a.txt / orchestrator brief PH"
STD_ZH = "P1–P8 的形式陳述與數學語意不變；說明性備註可能含非實質的精確化修訂。"

# ============================================================ VERSION (L5)
add("H01", "稿件狀態 (L5)", "VERSION label + RD-2 provenance phrase",
    "> **稿件狀態（供人工審閱，2026-10-18）：** 合併碩士論文 v1.8.6 THEORY INTEGRATION CANDIDATE（由 v1.8.5a 修訂；`SUBMISSION_READY = NO`）。v1.8.6 只整合",
    "> **稿件狀態（供人工審閱，2026-10-18）：** 合併碩士論文 V1.8.6a PRECISION HARMONIZATION + ERRATUM LINEAGE CLOSURE"
    "（由 v1.8.6 修訂；`SUBMISSION_READY = NO`；THEORY PARTIAL）。v1.8.6a 是用語、精確度與勘誤沿革的收斂，"
    "不是新的理論版本、不是實證版本，也不是模型修訂；理論補充包的整體判定維持 PARTIAL。v1.8.6a 只做三件事："
    "(i) 理論構念統一稱為企業決策機制（強調組織配置時稱組織決策安排），先前的「企業決策介面」是較早的理論用語，"
    "S1e 問卷的編碼者用語「企業決策過程」對應同一構念；第 3.9.3 節、表 3-14、表 4-13 與附錄 E6 的 V1 設計描述"
    "依 S1e 編碼者用語同步，不改變編碼者封包、類別定義或 V1 協定；v2.2 模型的「介面 I1–I5」「介面活化檢驗」"
    "「資料／介面門檻」等模型標籤與技術介面用語不變（逐處分類見交付檔 03_TERMINOLOGY_HARMONIZATION_REPORT.md）；"
    "(ii) 表 1-1、表 3-10、表 4-33，以及第 2.13、4.10.3、5.6、5.7、5.8.4、5.8.5 節的精確化：只縮小過度主張、補上範圍條件，"
    "不新增主張；(iii) Lemma E′ 證明用語勘誤的沿革紀錄（附錄 C.10.9；附錄 D）。v1.8.6a 不改變任何方程、G01–G16、"
    "表 3-4／3-4A、Study 1 數值、企業模型 v2.2、求解器 51 或 S1e 編碼者封包，也不新增任何引文；" + STD_ZH +
    "前一版為合併碩士論文 v1.8.6 THEORY INTEGRATION CANDIDATE（由 v1.8.5a 修訂）：v1.8.6 只整合",
    CF + " item 5; " + M06 + " (theory PARTIAL)")

add("H02", "稿件狀態 (L5) v1.8.6 sentence", "RD-2 provenance phrase",
    "不改變任何方程、命題 P1–P8 的陳述、G01–G16、表 3-4／3-4A、第 3.9.2–3.9.5 節的 V1 設計、Study 1 數值、企業模型 v2.2 或求解器 51，也不新增任何引文；",
    "不改變任何方程、G01–G16、表 3-4／3-4A、第 3.9.2–3.9.5 節的 V1 設計、Study 1 數值、企業模型 v2.2 或求解器 51，"
    "也不新增任何引文（P1–P8 的形式陳述與數學語意不變；說明性備註可能含非實質的精確化修訂）；",
    CF + " item 2 (RD-2)")

# ============================================================ RD-1 terminology
add("H03", "摘要 (L11)", "RD-1 construct term",
    "再把低整合接口轉譯為企業必須做出的決策介面，",
    "再把低整合接口轉譯為企業必須做出配置決策的企業決策機制，", CF + " item 1")
add("H04", "摘要 (L15)", "RD-1 construct term",
    "12 個對應到四個企業決策介面——", "12 個對應到四個企業決策機制——", CF + " item 1")
add("H05", "Abstract (L27)", "RD-1 construct term (EN)",
    "into decision interfaces that an enterprise must configure,",
    "into enterprise decision mechanisms that an enterprise must configure,", CF + " item 1")
add("H06", "Abstract (L31)", "RD-1 construct term (EN)",
    "map onto four enterprise decision interfaces—", "map onto four enterprise decision mechanisms—", CF + " item 1")
add("H07", "1.2.2 (L89)", "RD-1 construct term",
    "而轉譯成立之後，該介面是否真的在某一企業中改變決策",
    "而轉譯成立之後，該企業決策機制是否真的在某一企業中改變決策", CF + " item 1")
add("H08", "1.2.3 (L93)", "RD-1 construct term",
    "**第一，文獻低整合配對可收斂為少數企業決策介面。**",
    "**第一，文獻低整合配對可收斂為少數企業決策機制。**", CF + " item 1")
add("H09", "1.2.3 (L95)", "RD-1 construct term",
    "**第二，這四個介面在企業中不是彼此獨立的部門問題",
    "**第二，這四個機制在企業中不是彼此獨立的部門問題", CF + " item 1")
add("H10", "1.2.3 證據鏈 (L105)", "RD-1 construct term",
    "→ 企業決策介面 M1–M4（M5 為跨期擴充）", "→ 企業決策機制 M1–M4（M5 為跨期擴充）", CF + " item 1")
add("H11", "1.4 研究問題三 (L130)", "RD-1 construct term",
    "分別指向哪些企業必須做出的決策介面與模型元素？此一轉譯在獨立編碼下是否成立？在企業證據下，哪些介面真正形成企業決策問題？",
    "分別指向哪些企業必須做出配置決策的企業決策機制與模型元素？此一轉譯在獨立編碼下是否成立？在企業證據下，哪些轉譯後的機制真正形成企業決策問題？",
    CF + " item 1")
add("H12", "1.5 (L160)", "RD-1 construct term",
    "先經研究者逐格轉譯為企業決策介面與模型元素", "先經研究者逐格轉譯為企業決策機制與模型元素", CF + " item 1")
add("H13", "1.7.2 (L180)", "RD-1 construct term",
    "本研究建立文獻網絡低連結與企業決策介面之間的中介層", "本研究建立文獻網絡低連結與企業決策機制之間的中介層", CF + " item 1")
add("H14", "1.7.3 (L190)", "RD-1 construct term",
    "也被轉譯為企業決策介面，它仍只有", "也被轉譯為企業決策機制，它仍只有", CF + " item 1")
add("H15", "2.2 (L222)", "RD-1 construct term",
    "第 3.9 節把文獻低整合轉譯為企業介面時", "第 3.9 節把文獻低整合轉譯為企業決策機制時", CF + " item 1")
add("H16", "2.15 圖 2-1 說明 (L399)", "RD-1 construct term (I-label kept in parentheses)",
    "第一，G01–G16 透過四個介面進入模型", "第一，G01–G16 透過四個企業決策機制（M1–M4；模型標籤為介面 I1–I4）進入模型", CF + " item 1")
add("H17", "3.1.1 (L407)", "RD-1 construct term",
    "把穩健的功能低整合轉譯為企業必須做出的決策介面，建立", "把穩健的功能低整合轉譯為企業必須做出配置決策的企業決策機制，建立", CF + " item 1")
add("H18", "3.9.1 轉譯程序 (L667)", "RD-1 construct definition + terminology note",
    "**一個缺口是否指向一個企業必須做出的配置決策（企業決策介面）**。若多個缺口指向同一介面，就合併；若沒有介面，就留在證據層。",
    "**一個缺口是否指向一個企業必須做出的配置決策（企業決策機制）**。若多個缺口指向同一介面，就合併；若沒有介面，就留在證據層。"
    "本稿的理論構念統一稱為企業決策機制（強調組織配置時稱組織決策安排）；先前版本與表 3-4A 欄名所用的「企業決策介面」是較早的理論用語，"
    "與企業決策機制指同一構念，不是第三個構念。下表、表 3-4 與表 3-4A 的「介面 I1–I5」，以及第 3.12.5 節的「介面活化檢驗」，"
    "沿用構念凍結文件與 v2.2 模型的標籤：介面 I1–I5 依序對應機制 M1–M5，標示各機制在模型中的位置，也不是另一個構念；"
    "它們與第 3.10.3 節資料門檻中的「共用介面」，以及使用者介面、API 或系統串接介面等技術介面無關。",
    CF + " item 1; Table 3-3 (I1–I5 ↔ M1–M5, unchanged)")
add("H19", "3.9.3 (4) 編碼工具 (L755)", "RD-1 verbatim S1e sentence + coder-facing wording sync",
    "(4) **編碼工具（Q1–Q5）。** Q1 判斷該配對是否對應可辨識的企業決策介面（YES、NO、UNCERTAIN）；",
    "(4) **編碼工具（Q1–Q5）。** 為降低獨立編碼者的理解負擔，S1e 問卷採用『企業決策過程』作為 coder-facing wording；"
    "其所對應的理論構念仍為本文所稱之企業決策機制／組織決策安排，並不構成另一個不同構念。"
    "Q1 判斷該配對是否呈現可辨識的企業決策過程（YES、NO、UNCERTAIN）；",
    CF + " item 1 (verbatim sentence); " + S1E + "; S1e CODER_1 Q1 wording 「Q1 這段內容是否呈現一個可辨識的企業決策過程？」 (read-only)")
add("H20", "3.9.3 (4) NONE 定義 (L755)", "RD-1 coder-facing wording sync (S1e)",
    "NONE 的定義是：存在可辨識的企業決策介面，但 M1–M4", "NONE 的定義是：存在可辨識的企業決策過程，但 M1–M4",
    S1E + "; S1e 類別定義 「只有在存在企業決策過程，但其他所有機制…都不適用時才能選」")
add("H21", "3.9.3 (4) EVIDENCE_ONLY (L755)", "RD-1 coder-facing wording sync (S1e)",
    "沒有獨立的介面時也不使用 NONE（改用 EVIDENCE_ONLY）", "沒有可辨識的企業決策過程時也不使用 NONE（改用 EVIDENCE_ONLY）",
    S1E + "; S1e 「沒有可辨識的決策過程時，請選「僅屬證據層」」")
add("H22", "3.9.3 目前狀態 (L755)", "RD-1 V1-design status sync (S1e packet version)",
    "目前狀態：協定已於 S1 凍結（人類編碼前），封包已備妥待發送，人類編碼尚未執行，結果待完成。\n\nEA-X（解釋可用性）",
    "目前狀態：協定已於 S1 凍結（人類編碼前）；編碼者封包其後改為 S1e 版（2026-10-14 以 SHA-256 凍結，經審閱核可、可發送；"
    "只改編碼者用語與答案表版面，16 個項目、各編碼者的隨機順序、類別定義、Q1／Q2 一致性規則與 Q3–Q5 的語意不變，"
    "Q1 的判斷內容不變；S1d 保留為歷史版本，不覆寫），人類編碼尚未執行，結果待完成。\n\nEA-X（解釋可用性）",
    S1E)
add("H23", "3.9.6 輔助類別 (L779)", "RD-1 description sync (§3.9.3 now synced)",
    "存在可辨識的企業決策過程（S1e 編碼者材料的用語；第 3.9.3 節沿用 S1d 的「企業決策介面」，兩者指同一判斷，S1e 只改編碼者用語與答案表版面，不改類別定義）",
    "存在可辨識的企業決策過程（S1e 編碼者材料的用語，第 3.9.3 節已同步；S1d 與本稿先前版本使用「企業決策介面」，兩者指同一判斷，"
    "對應的理論構念都是企業決策機制；S1e 只改編碼者用語與答案表版面，不改類別定義）",
    S1E + "; V1.8.6 05 O-2 / 12 RD-1")
add("H24", "表 3-14 V1 列 (L1366)", "RD-1 V1-design status sync (S1e)",
    "協定與封包已於 S1 凍結，人類編碼尚未執行）",
    "協定與封包已於 S1 凍結；現行編碼者封包為 S1e 版〔編碼者用語「企業決策過程」，只改用語與答案表版面，類別定義不變〕，人類編碼尚未執行）",
    S1E)
add("H25", "表 4-13 Q1 列 (L1797)", "RD-1 coder-facing wording sync (S1e)",
    "| Q1 企業決策介面 |", "| Q1 企業決策過程（S1e 編碼者用語；理論構念為企業決策機制） |", S1E)
add("H26", "第五章導言 (L2277)", "RD-1 construct term",
    "再討論從文獻低整合到企業決策介面的轉譯（第 5.5 節）", "再討論從文獻低整合到企業決策機制的轉譯（第 5.5 節）", CF + " item 1")
add("H27", "表 5-1 (L2322)", "RD-1 construct term",
    "| 企業決策介面 | 研究者轉譯經獨立的人類編碼驗證 |", "| 企業決策機制 | 研究者轉譯經獨立的人類編碼驗證 |", CF + " item 1")
add("H28", "5.5 標題 (L2351)", "RD-1 construct term (heading)",
    "## 5.5 從低整合接口到企業決策介面", "## 5.5 從低整合接口到企業決策機制", CF + " item 1")
add("H29", "5.9 (L2461)", "RD-1 construct term",
    "後者在企業中檢驗轉譯後的介面是否改變決策。", "後者在企業中檢驗轉譯後的機制是否改變決策。", CF + " item 1")
add("H30", "5.10 (L2475)", "RD-1 construct term",
    "本論文把 16 組主要穩健不足呈現轉譯為企業決策介面，", "本論文把 16 組主要穩健不足呈現轉譯為企業決策機制，", CF + " item 1")
add("H31", "5.10 (L2475)", "RD-1 construct term",
    "評估與保證四個介面，2 組歸入", "評估與保證四個機制，2 組歸入", CF + " item 1")
add("H32", "附錄 E6 (L3252)", "RD-1 V1-design status sync (S1e)",
    "編碼者只收到遮蔽 G 編號的盲編封包並填寫七項聲明；封包直接寄送，不經公開儲存庫 |",
    "編碼者只收到遮蔽 G 編號的盲編封包（現行為 S1e 版；編碼者用語「企業決策過程」，對應理論構念企業決策機制；S1d 保留為歷史版本）並填寫七項聲明；封包直接寄送，不經公開儲存庫 |",
    S1E)

# ============================================================ RD-2 provenance phrase
add("H33", "3.12.4 分類段 (L1159)", "RD-2 provenance phrase",
    "上列 P1–P8 的陳述不變。", "上列 " + STD_ZH, CF + " item 2")
add("H34", "C.10.9 影響 (L3125)", "RD-2 provenance phrase",
    "Lemma E′ 的陳述、所有方程、目標、可行集合、P1–P8 與 51 的所有計算數值皆不變：",
    "Lemma E′ 的陳述、所有方程、目標、可行集合與 51 的所有計算數值皆不變（P1–P8 的形式陳述與數學語意不變；說明性備註可能含非實質的精確化修訂）：",
    CF + " item 2")

# ============================================================ RD-5 outer precision
add("H35", "表 1-1 研究問題四 (L150)", "RD-5 scope condition (DL)",
    "| 3.11、3.12 | 4.10 | 模型完成；合成驗證完成（僅合成）；實證待完成（V7） |",
    "| 3.11、3.12 | 4.10 | 模型完成；模型內形式結果（第 3.12.4 節；附錄 C.10）：DL 為零的首佳相對刻畫（Lemma DL-1，為 Lemma E′ 之重述）、"
    "DL 為正的必要條件（AL3 且精確平手下，Cor DL-2o／2p）與充分條件（唯一首佳下，Cor DL-3），沒有不依賴首佳解的充要刻畫；"
    "合成驗證完成（僅合成）；實證待完成（V7） |",
    M06 + " rows DL (characterization lemma / necessary / sufficient / primitive iff NOT_PROVEN); V1.8.6 12 RD-5")
add("H36", "表 1-1 研究問題五 (L151)", "RD-5 scope condition (screening; shared capability)",
    "| 3.10.4、3.11–3.13 | 4.10 | 模型完成；合成驗證完成（僅合成；v2.4 部分為候選）；實證待完成（V7） |",
    "| 3.10.4、3.11–3.13 | 4.10 | 模型完成；模型內形式結果：治理篩選為條件性結果（恆等式 GS-I、充分條件 Prop GS-1、精確平手下的必要條件 Thm GS-N；"
    "不是一般性質），共享能力重用在 B 中單調（Thm D1，P4 之重述）、在 C 中以帳本對齊為充分條件（Thm D3，重述），"
    "否則存在建置區域不是區間的實例（Prop D6，存在性結果）；合成驗證完成（僅合成；v2.4 部分為候選）；實證待完成（V7） |",
    M06 + " rows Screening (GS-I identity, GS-1 sufficient, GS-N necessary exact ties, never 'always'); Shared capability (D1/D3 restatement, D6 existence); V1.8.6 12 RD-5")
add("H37", "表 1-1 研究問題六 (L152)", "RD-5 scope condition (robustness; VOI)",
    "| 3.13、3.14 | 4.8、4.10 | 模型完成；合成驗證完成（僅合成）；實證待完成（V7） |",
    "| 3.13、3.14 | 4.8、4.10 | 模型完成；頂點精確性只限 Model B（及 A+）的整個 portfolio（Thm R1，為 Lemma R 之重述）；"
    "VOI 的次序只對固定候選集合成立（Prop E.1、E.2），序列識別性質為 PARTIAL；合成驗證完成（僅合成）；實證待完成（V7） |",
    M06 + " rows Robustness (vertex-exactness scope); VOI (sequential identification PARTIAL; fixed candidate set); V1.8.6 12 RD-5")
add("H38", "2.13 對模型的意涵 (iv) (L332)", "RD-5 separate necessary/sufficient",
    "(iv) 跨層衝突以帳本對齊條件 (AL1)–(AL4) 檢驗；對齊時授權損失為零（P2）。",
    "(iv) 跨層衝突以帳本對齊條件 (AL1)–(AL4) 檢驗；對齊時授權損失為零（P2）——對齊是授權損失為零的充分而非必要條件，"
    "不對齊也不足以使授權損失為正（第 3.12.4 節）。",
    M06 + " rows DL necessary / sufficient (W2: misaligned but blockable, DL = 0); V1.8.6 12 RD-5")
add("H39", "2.13 對模型的意涵 (vii) (L332)", "RD-5 attribution boundary (model-internal vs literature)",
    "輸出 ROBUST／CONDITIONAL／FRAGILE／UNIDENTIFIED。\n\n## 2.14",
    "輸出 ROBUST／CONDITIONAL／FRAGILE／UNIDENTIFIED。(vii) 第 3.12.4 節與附錄 C.10 的授權損失、治理篩選與共享能力重用結果，"
    "是本研究在完全資訊、固定參數下的模型內結果（其中 Lemma DL-1 為 Lemma E′ 於首佳解之重述），不是上述文獻的主張。\n\n## 2.14",
    M06 + " rows DL-1 RESTATEMENT, TYPE C labels; References row (0 new citations); theory pack 10 row 2.1 without the TO-VERIFY analogue clause")
add("H40", "表 3-10 Q2 (L1184)", "RD-5 scope condition (δ threshold)",
    "| 損益兩平固定成本 `F_c^†`、重用門檻 `δ^†` | 五 |",
    "| 損益兩平固定成本 `F_c^†`、重用門檻 `δ^†`（B 中唯一；C 中帳本對齊時唯一，否則報告集合值的建置區域與平手慣例） | 五 |",
    M06 + " rows Shared capability (D1 B monotone, D3 alignment, D6 existence); theory pack 10 §5 Q2")
add("H41", "表 3-10 Q4 (L1186)", "RD-5 separate necessary/sufficient (DL diagnosis)",
    "| DL 及其來源分解 | 四 |",
    "| DL 及其來源分解（報告不成立的對齊條件，以及存在不可阻擋偏離的首佳計畫；成對檢查不足以判定 DL 的正負，W3c） | 四 |",
    M06 + " rows DL characterization (first-best-relative), primitive iff NOT_PROVEN (W3c); theory pack 10 §5 Q4")
add("H42", "表 3-10 Q7 (L1189)", "RD-5 scope condition (vertex exactness)",
    "| 元素層級穩健性分類、MaxRegret | 六 |",
    "| 元素層級穩健性分類（以涵蓋率報告）、MaxRegret（頂點精確只限 Model B 及 A+ 的整個 portfolio） | 六 |",
    M06 + " row Robustness (vertex-exactness scope); theory pack 10 §5 Q7")
add("H43", "4.10.3 判讀規則 (L2114–2115)", "RD-5 scope condition (Lemma R; VOI fixed candidate set)",
    "  - 只有 Model B 的整體 portfolio 有精確證書（Lemma R）。元素層級與 Model C 只報涵蓋率，不稱「對所有 θ」。\n  - VOI 同時報頂點版（可能高估）與網格版。",
    "  - 只有 Model B（及 A+）的整體 portfolio 在第 3.13 節所列前提 (R-a)–(R-e) 下有精確證書（Lemma R）。元素層級（除 Prop R4 的情形）與 Model C 只報涵蓋率，不稱「對所有 θ」。\n"
    "  - VOI 同時報頂點版（可能高估）與網格版；兩者只在固定候選集合（第一批登記時的 ROBUSTLY_FEASIBLE 集合）下為真值的上界，"
    "重算候選集合只作次要診斷並標 `CANDIDATE_SET_EXPANDED`（第 3.14.3 節）。",
    M06 + " rows Robustness, VOI; V1.8.6 12 RD-5")
add("H44", "表 4-33 研究問題五 (L2268)", "RD-5 existence vs universal",
    "共享重用效果在雙層且帳本不對齊時可使建置區域為集合值；",
    "共享重用效果在雙層且帳本不對齊時可使建置區域為集合值（存在性結果，Prop D6）；",
    M06 + " row Prop D6 (existence only; never 'generally non-monotone')")
add("H45", "表 4-33 研究問題五 (L2268)", "RD-5 scope condition (screening)",
    "P8 在雙層且帳本不對齊時要求可具篩選價值；",
    "P8 在雙層且帳本不對齊時要求可具篩選價值（只在特定的錯位與可分離性條件下；篩選價值不超過較寬鬆要求下的授權損失，恆等式 GS-I）；",
    M06 + " rows Screening (GS-I identity; witnesses: 'may have positive screening value under specific…conditions'; never 'always')")
add("H46", "表 4-33 研究問題六 (L2269)", "RD-5 VOI qualifier",
    "研究設計：只有 Model B 的整體 portfolio 具精確穩健性證書（Lemma R）；元素層級與 Model C 只報涵蓋率；VOI 同時報頂點版與網格版。",
    "研究設計：只有 Model B（及 A+）的整體 portfolio 具精確穩健性證書（Lemma R；前提見第 3.13 節）；元素層級（除 Prop R4 的情形）與 Model C 只報涵蓋率；"
    "VOI 同時報頂點版（可能高估）與網格版，兩者只在固定候選集合下為真值的上界（Prop E.1、E.2），依 VOI 排序之量測順序的最適性未證明。",
    M06 + " rows Robustness, VOI (PARTIAL; VOI-greedy optimality open); V1.8.6 12 RD-5")
add("H47", "5.8.4 (L2429)", "RD-5 pointer (V1 does not test sufficiency; NONE/AMBIGUOUS)",
    "文獻分析的人工稽核（第 3.7 節）驗證的是語意證據與功能分類，不能替代 V1。",
    "文獻分析的人工稽核（第 3.7 節）驗證的是語意證據與功能分類，不能替代 V1。V1 檢驗的是 G→M 對應在凍結類別定義下的編碼者間可詮釋性，"
    "不檢驗 M1–M4 的非冗餘性或充分性；NONE 是涵蓋缺口的訊號，AMBIGUOUS 用於證據不足或兩類並列的類別邊界情形，"
    "兩者的有無都不能建立或否定 M1–M4 的充分性（第 3.9.6 節）。",
    M06 + " row M1–M4 (PARTIAL; minimal sufficiency NOT_PROVEN); theory pack 10 §10 'Also' §5.8.4; V1.8.6 12 RD-5")
add("H48", "5.8.5 (L2433)", "RD-5 pointer (information-asymmetry sidecar)",
    "只有取得「企業與部門知道不同參數」的證據，才執行資訊不對稱的敏感度分析。",
    "只有取得「企業與部門知道不同參數」的證據，才執行資訊不對稱的敏感度分析；資訊不對稱的側車目前只是設計（SIDECAR_DESIGN_ONLY），"
    "不修改 v2.2，其完全資訊特例重現 P3（第 5.8.10 節）。",
    M06 + " row Information asymmetry (SIDECAR_DESIGN_ONLY; limitations only); theory pack 10 §10 'Also' §5.8.5")

# ============================================================ claim-consistency sweep
add("H49", "5.6 企業協調的價值來源 (L2377)", "SWEEP necessary-condition precision (AL3 channel)",
    "DL 只在帳本不對齊且 envelope 無法分離不利配置時為正。",
    "DL 為正的必要條件是帳本不對齊：在 AL3 成立時，還須有 envelope 無法分離的不利配置（Cor DL-2o／2p），"
    "AL3 不成立時部門專屬限制本身即可使 DL 為正（第 3.12.4 節）；這些都只是必要條件，不是充分條件。",
    M06 + " row DL necessary conditions (DL-2o/2p under AL3, plus the AL3 channel)")

add("H52", "5.7 一般形式貢獻與 AI 特定部分 (L2397)", "SWEEP empirical-status qualifier (V7 not run)",
    "評估保證與 AI 治理的語意、AI 特定的實證參數化，以及後續的企業應用（第 1.7.2 節）。",
    "評估保證與 AI 治理的語意、AI 特定的實證參數化（V7，尚未執行），以及後續的企業應用（第 1.7.2 節）。",
    "V1.8.6 11 m3 (applied only at l.182); " + M06 + " row AI-specificity")

# ============================================================ lineage closure
add("H50", "C.10.9 沿革紀錄（新增 bullet）", "VERSION erratum lineage record",
    "不依賴證明中 `x` 的特定選法。\n",
    "不依賴證明中 `x` 的特定選法。\n"
    "- **沿革紀錄（v1.8.6a）。** 本勘誤的沿革紀錄為勘誤檔 `42a_CANONICAL_42_ERRATUM_V1_8_6.md`（v1.8.6a 交付檔 `04_42A_ERRATUM.md`）："
    "它只記錄上述悲觀情形的證明用語修正，不修改企業模型規格 v2.2（42）與求解器 51 本身，也不改變任何數值；"
    "是否在下一個正式版本納入此修正，仍由研究者決定（附錄 D）。\n",
    CF + " item 5; V1.8.6 12 RD-3; theory pack 13")
add("H51", "附錄 D v1.8.6 列 + v1.8.6a 列", "VERSION Appendix D row",
    "| 合併論文 v1.8.6（理論整合版；v1.8.5a 為修訂底稿） | 本稿 |",
    "| 合併論文 v1.8.6（理論整合版；v1.8.5a 為修訂底稿） | v1.8.6a 的修訂底稿（已保存；未覆寫） |\n"
    "| v1.8.6a／01–05 | — | `01_V1_8_6A_MANUSCRIPT.md`（另有 `02_V1_8_6A_CHANGELOG.md`、`03_TERMINOLOGY_HARMONIZATION_REPORT.md`、"
    "`04_42A_ERRATUM.md`、`05_OUTER_SECTION_PRECISION_AUDIT.md`）；勘誤沿革紀錄 `42a_CANONICAL_42_ERRATUM_V1_8_6.md` | "
    "合併論文 v1.8.6a（PRECISION HARMONIZATION + ERRATUM LINEAGE CLOSURE：用語、精確度與勘誤沿革的收斂；不是新的理論版本、實證版本或模型修訂；"
    "v1.8.6 為修訂底稿） | 本稿；附錄 C.10.9 |",
    CF + " item 5")

# ============================================================ apply
orig = raw.decode('utf-8')
assert '\r' not in orig
text = orig
for p in P:
    assert '$' not in p['new'], p['id'] + ': $ in new text'
    p['count_in_src'] = orig.count(p['old'])
    assert p['count_in_src'] == 1, f"{p['id']}: old matched {p['count_in_src']} times in V1.8.6 01"
    p['line_src'] = orig[:orig.find(p['old'])].count('\n') + 1
    c = text.count(p['old'])
    assert c == 1, f"{p['id']}: old matched {c} times at apply time"
    text = text.replace(p['old'], p['new'], 1)
# each new must be unique in output (needed for reverse replay)
for p in P:
    assert text.count(p['new']) == 1, f"{p['id']}: new not unique in output"
assert '\r' not in text
out = text.encode('utf-8')
open(DST, 'wb').write(out)
json.dump(P, open(JOUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('patches', len(P))
print('src sha', hashlib.sha256(raw).hexdigest())
print('dst sha', hashlib.sha256(out).hexdigest())
for p in P:
    print(p['id'], 'src line', p['line_src'], p['category'])
