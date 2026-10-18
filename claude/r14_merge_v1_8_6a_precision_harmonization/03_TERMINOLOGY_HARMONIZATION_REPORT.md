# 03 — V1.8.6a Terminology Harmonization Report (RD-1)

- **Base:** V1.8.6 `01_V1_8_6_THEORY_INTEGRATED_MANUSCRIPT.md`, sha256 `94d41d5682818953912784d0e870d58d1e4c418e7261b619d5c73485dfee82f4` (asserted before patching).
- **Output:** `01_V1_8_6A_MANUSCRIPT.md`, sha256 `12eee36a8c1a762a16603deb4f46d2962cc4019a62e443241c082629546d9517`.
- **Method:** `work/PH/patch_v186a.py` (exact, asserted-once replacements; no global replace) and `work/PH/verify_v186a.py` (52/52 hard checks PASS). Line numbers below are V1.8.6 01 lines.
- **Decision applied:** theoretical term = 「企業決策機制」 (「組織決策安排」 where organisational configuration is emphasised). S1e coder-facing wording stays 「企業決策過程」; the S1e packets were not touched (sha256 cbbbaa0a… / 5925ead5… / 50d8c818…, re-hashed after the build).

## 1. Verbatim S1e sentence (first mention of the V1 instrument)

Inserted once, at §3.9.3 item (4) 「編碼工具（Q1–Q5）」, the first place in the body where the V1 instrument (questionnaire) is described (patch H19):

> 為降低獨立編碼者的理解負擔，S1e 問卷採用『企業決策過程』作為 coder-facing wording；其所對應的理論構念仍為本文所稱之企業決策機制／組織決策安排，並不構成另一個不同構念。

Verification: the sentence occurs exactly once; it lies inside §3.9.3 item (4); it is the first body mention of 「S1e」 (the only earlier mention is the L5 version/status meta-line, which describes this V1.8.6a pass). §3.9.3 now contains 0 × 「企業決策介面」 and 4 × 「企業決策過程」.

## 2. V1-design locations synchronised

| Location | Patch | Change |
|---|---|---|
| §3.9.3 (4) Q1 | H19 | (4) **編碼工具（Q1–Q5）。** 為降低獨立編碼者的理解負擔，S1e 問卷採用『企業決策過程』作為 coder-facing wording；其所對應的理論構念仍為本文所稱之企業決策機制／組織決策安排，並不構成另一個不同構念。Q1 判斷該配對是否呈現可辨識的企業決策過程（YES、NO、UNCERTAIN）； |
| §3.9.3 (4) NONE | H20 | NONE 的定義是：存在可辨識的企業決策過程，但 M1–M4 |
| §3.9.3 (4) EVIDENCE_ONLY rule | H21 | 沒有可辨識的企業決策過程時也不使用 NONE（改用 EVIDENCE_ONLY） |
| §3.9.3 目前狀態 (S1e packet version) | H22 | 目前狀態：協定已於 S1 凍結（人類編碼前）；編碼者封包其後改為 S1e 版（2026-10-14 以 SHA-256 凍結，經審閱核可、可發送；只改編碼者用語與答案表版面，16 個項目、各編碼者的隨機順序、類別定義、Q1／Q2 一致性規則與 Q3–Q5 的語意不變，Q1 的判斷內容不變；S1d 保留為歷史版本，不覆寫），人類編碼尚未執行，結果待完成。 ⏎  ⏎ EA-X（解釋可用性） |
| §3.9.6 輔助類別 (sentence about §3.9.3) | H23 | 存在可辨識的企業決策過程（S1e 編碼者材料的用語，第 3.9.3 節已同步；S1d 與本稿先前版本使用「企業決策介面」，兩者指同一判斷，對應的理論構念都是企業決策機制；S1e 只改編碼者用語與答案表版面，不改類別定義） |
| Table 3-14 V1 row status | H24 | 協定與封包已於 S1 凍結；現行編碼者封包為 S1e 版〔編碼者用語「企業決策過程」，只改用語與答案表版面，類別定義不變〕，人類編碼尚未執行） |
| Table 4-13 Q1 row | H25 | ¦ Q1 企業決策過程（S1e 編碼者用語；理論構念為企業決策機制） ¦ |
| Appendix E6 | H32 | 編碼者只收到遮蔽 G 編號的盲編封包（現行為 S1e 版；編碼者用語「企業決策過程」，對應理論構念企業決策機制；S1d 保留為歷史版本）並填寫七項聲明；封包直接寄送，不經公開儲存庫 ¦ |
| §3.9.1 terminology note | H18 | **一個缺口是否指向一個企業必須做出的配置決策（企業決策機制）**。若多個缺口指向同一介面，就合併；若沒有介面，就留在證據層。本稿的理論構念統一稱為企業決策機制（強調組織配置時稱組織決策安排）；先前版本與表 3-4A 欄名所用的「企業決策介面」是較早的理論用語，與企業決策機制指同一構念，不是第三個構念。下表、表 3-4 與表 3-4A 的「介面 I1–I5」，以及第 3.12.5 節的「介面活化檢驗」，沿用構念凍結文件與 v2.2 模型的標籤：介面 I1–I5 依序對應機制 M1–M5，標示各機制在模型中的位置，也不是另一個構念；它們與第 3.10.3 節資料門檻中的「共用介面」，以及使用者介… |

S1e facts used (all from the S1e records, `V1_S1E_CURRENT_STATUS.md`, `S1E_PROCESS_WORDING_CHANGELOG.md`, `FREEZE_MANIFEST_V1_S1E_PROCESS_WORDING.txt`, and the CODER_1 packet text read read-only): coder-facing term 企業決策介面 → 企業決策過程; scope = wording + answer-sheet layout; 16 items, per-coder random order, category semantics, Q1/Q2 consistency rules and Q3–Q5 semantics preserved; S1d preserved; teacher review APPROVED_TO_RUN; READY_TO_DISTRIBUTE = YES; HUMAN_RESULTS = NONE. Not changed: protocol, codebook semantics, categories, analysis plan, any number.

## 3. Classes

- **a** = construct term → changed to 企業決策機制 (EN: enterprise decision mechanism).
- **a-kept** = construct term kept as a quoted historical / protected-table label; the §3.9.1 note (H18) states that 「企業決策介面」 was the earlier theoretical wording of 企業決策機制, not a third construct.
- **b-sync** = coder-facing description of the S1d/S1e instrument → synced to the S1e wording 「企業決策過程」 (packets untouched).
- **b-kept** = coder-facing quotation kept (historical S1d wording), sentence updated.
- **c** = technical interface or v2.2 model term/label (I1–I5, 介面活化檢驗, 資料／介面門檻, (F5e), R_j/D_j 共用介面, 使用者介面, platform interfaces, code keys) → kept; changing it would alter model-term semantics.
- **d** = other (literature-level functional interface 接口 in EN/zh prose, quoted rollback-rule label from document 41, organisational 外部評估介面) → kept.

## 4. Counts

| Term | Class | Count (V1.8.6) |
|---|---|---|
| EN interface | a | 2 |
| EN interface | c | 4 |
| EN interface | d | 3 |
| 介面 (bare) | a | 10 |
| 介面 (bare) | b-sync | 1 |
| 介面 (bare) | c | 35 |
| 介面 (bare) | d | 6 |
| 企業決策介面 | a | 11 |
| 企業決策介面 | a-kept | 2 |
| 企業決策介面 | b-kept | 1 |
| 企業決策介面 | b-sync | 3 |

Whole-document string counts V1.8.6 → V1.8.6a: 企業決策介面 17 → 5; 企業決策過程 1 → 9; 企業決策機制 1 → 25; 組織決策安排 0 → 3; 介面 (all, incl. inside 企業決策介面) 69 → 58.

The 5 remaining 「企業決策介面」 in V1.8.6a: L5 (version note naming it as the earlier wording), L667 (the §3.9.1 terminology note), L699 and L703 (Table 3-4 lead-in naming the Table 3-4A column, and the protected Table 3-4A header; class a-kept), L779 (historical S1d quotation, class b-kept).

Technical / model-term counts (V1.8.6 → V1.8.6a; none decreased): 使用者介面 0→1; API 1→2; 系統串接介面 0→1; 介面活化 9→11; 資料／介面門檻 2→3; 共用介面 1→2; 介面 I1 3→7; 平台介面 2→2; platform interfaces 1→1; interface activation 1→1; Interface activation 1→1; 外部評估介面 1→1; 技術—治理介面 1→1; 轉譯介面 1→1; 未獲獨立支持的介面 3→3.

## 5. Full inventory (every 「企業決策介面」, bare 「介面」 and EN interface occurrence in V1.8.6 01)

| # | Line | Term | Before (context) | After | Class | Reason |
|---|---|---|---|---|---|---|
| 1 | 11 | 介面 | …整合，再把低整合接口轉譯為企業必須做出的決策介面，最後將企業人工智慧導入形式… | CHANGED (H03): 再把低整合接口轉譯為企業必須做出配置決策的企業決策機制， | a | construct term (enterprise decision the enterprise must make) |
| 2 | 15 | 企業決策介面 | …人類構念效度驗證待完成），12 個對應到四個企業決策介面——授權與問責（M1）、流程… | CHANGED (H04): 12 個對應到四個企業決策機制—— | a | construct term (four M1–M4 decision mechanisms) |
| 3 | 27 | interface | …integrated functional interface in the litera… | KEPT: unchanged | d | EN "functional interface in the literature" = literature-level AI × decision functional interface (接口), not the V1 construct |
| 4 | 27 | interfaces | …stly under-integrated interfaces into decision… | KEPT: unchanged | d | EN "under-integrated interfaces" = literature-level functional interfaces (接口) |
| 5 | 27 | interfaces | …erfaces into decision interfaces that an enter… | CHANGED (H05): into enterprise decision mechanisms that an enterprise must configure, | a | EN construct term |
| 6 | 31 | interfaces | …r enterprise decision interfaces—authority and… | CHANGED (H06): map onto four enterprise decision mechanisms— | a | EN construct term (four enterprise decision mechanisms M1–M4) |
| 7 | 37 | interface | …problem. A literature interface becomes an en… | KEPT: unchanged | d | EN "A literature interface" = literature-level functional interface |
| 8 | 89 | 介面 | …判斷，需要獨立編碼者驗證；而轉譯成立之後，該介面是否真的在某一企業中改變決策… | CHANGED (H07): 而轉譯成立之後，該企業決策機制是否真的在某一企業中改變決策 | a | construct term (the translated decision element) |
| 9 | 93 | 企業決策介面 | …**第一，文獻低整合配對可收斂為少數企業決策介面。** 研究者的逐格轉譯（第… | CHANGED (H08): **第一，文獻低整合配對可收斂為少數企業決策機制。** | a | construct term |
| 10 | 95 | 介面 | …**第二，這四個介面在企業中不是彼此獨立的部門問… | CHANGED (H09): **第二，這四個機制在企業中不是彼此獨立的部門問題 | a | construct term (the four M1–M4) |
| 11 | 105 | 企業決策介面 | …局部敏感度另行報告）→ 缺口—機制轉譯 → 企業決策介面 M1–M4（M5 為跨期擴… | CHANGED (H10): → 企業決策機制 M1–M4（M5 為跨期擴充） | a | construct term in the evidence chain |
| 12 | 122 | 介面 | …完成（理論收斂），人類構念效度驗證與企業層的介面活化檢驗尚待完成；研究問題四… | KEPT: unchanged | c | v2.2 model term: Q8 interface activation test (介面活化檢驗) |
| 13 | 130 | 介面 | …01–G16）分別指向哪些企業必須做出的決策介面與模型元素？此一轉譯在獨立編… | CHANGED (H11): 分別指向哪些企業必須做出配置決策的企業決策機制與模型元素？此一轉譯在獨立編碼下是否成立？在企業證據下，哪些轉譯後的機制真正形成企業決策問題？ | a | construct term in RQ3 |
| 14 | 130 | 介面 | …轉譯在獨立編碼下是否成立？在企業證據下，哪些介面真正形成企業決策問題？… | CHANGED (H11): 分別指向哪些企業必須做出配置決策的企業決策機制與模型元素？此一轉譯在獨立編碼下是否成立？在企業證據下，哪些轉譯後的機制真正形成企業決策問題？ | a | construct term in RQ3 (→ 轉譯後的機制, matching the Abstract/§1.4 integrated claim) |
| 15 | 149 | 介面 | … ¦ G→M 研究者轉譯；V1 盲編；Q8 介面活化檢驗 ¦ 3.8、3.9… | KEPT: unchanged | c | v2.2 model term: Q8 介面活化檢驗 (Table 1-1) |
| 16 | 160 | 企業決策介面 | …上。16 組穩健不足呈現先經研究者逐格轉譯為企業決策介面與模型元素（第 3.9 節）… | CHANGED (H12): 先經研究者逐格轉譯為企業決策機制與模型元素 | a | construct term |
| 17 | 180 | 企業決策介面 | …貢獻。** 第一，本研究建立文獻網絡低連結與企業決策介面之間的中介層，使 bibli… | CHANGED (H13): 本研究建立文獻網絡低連結與企業決策機制之間的中介層 | a | construct term |
| 18 | 190 | 企業決策介面 | …項統計／計數分析判定為穩健低整合、也被轉譯為企業決策介面，它仍只有在企業證據下改變可… | CHANGED (H14): 也被轉譯為企業決策機制，它仍只有 | a | construct term |
| 19 | 214 | 介面 | …；準備度中與配置直接相關的部分（資料可得性、介面、決策權）被表達為由企業決策… | KEPT: unchanged | c | technical readiness term: data availability / interface → model threshold keys R_j(s), D_j(s) |
| 20 | 222 | 介面 | …。因此，第 3.9 節把文獻低整合轉譯為企業介面時，以決策端家族所代表的決策… | CHANGED (H15): 第 3.9 節把文獻低整合轉譯為企業決策機制時 | a | construct term (企業介面 = translated enterprise decision element) |
| 21 | 248 | 介面 | …不同於現況，由第 3.12.5 節的 Q8 介面活化檢驗判定；可行性與價值的… | KEPT: unchanged | c | v2.2 model term: Q8 介面活化檢驗 |
| 22 | 345 | 介面 | …班加羅爾一家公司的 28 次訪談區分嵌入平台介面的 AI 功能與獨立的提示式… | KEPT: unchanged | c | technical interface: AI features embedded in platform interfaces (Edwards & Murthy, 2026) |
| 23 | 399 | 介面 | …構有三個要點。第一，G01–G16 透過四個介面進入模型，但**任何 gap… | CHANGED (H16): 第一，G01–G16 透過四個企業決策機制（M1–M4；模型標籤為介面 I1–I4）進入模型 | a | construct term; the model label I1–I4 is retained in parentheses |
| 24 | 407 | 介面 | …：把穩健的功能低整合轉譯為企業必須做出的決策介面，建立企業—事業單位雙層配置… | CHANGED (H17): 把穩健的功能低整合轉譯為企業必須做出配置決策的企業決策機制，建立 | a | construct term |
| 25 | 667 | 企業決策介面 | …一個缺口是否指向一個企業必須做出的配置決策（企業決策介面）**。若多個缺口指向同一介… | CHANGED (H18): **一個缺口是否指向一個企業必須做出的配置決策（企業決策機制）**。若多個缺口指向同一介面，就合併；若沒有介面，就留在證據層。本稿的理論構念統一稱為企業決策機制（強調組織配置時稱組織決策安排）；先前版本與表 3-4A 欄名所用的「企業決策介面」是較早的理論用語，與企業決策機制指同一構念，不是第三個構念。下表、表 3-4 與表 3-4A 的「介面 I1–I5」，以及第 3.12.5 節的「介面活化檢驗」，沿用構念凍結文件與 v2.2 模型的標籤：介面 I1–I5 依序對應機制 … | a | construct DEFINITION; terminology note added here (企業決策介面 = earlier wording, same construct; I1–I5 = model labels) |
| 26 | 667 | 介面 | …決策（企業決策介面）**。若多個缺口指向同一介面，就合併；若沒有介面，就留在… | KEPT: unchanged | c | model label: the I1–I5 structure of the following table (同一介面 = same I_k); covered by the §3.9.1 note |
| 27 | 667 | 介面 | …**。若多個缺口指向同一介面，就合併；若沒有介面，就留在證據層。… | KEPT: unchanged | c | model label: no I_k → evidence layer |
| 28 | 669 | 介面 | …S2 的企業介面以決策端家族所代表的「組織決… | KEPT: unchanged | c | model label: 企業介面 = I1–I5 structure (S2) |
| 29 | 669 | 介面 | …企業層面面對的是同一組配置選擇。收斂後的企業介面有五個：… | KEPT: unchanged | c | model label: 收斂後的企業介面有五個 (I1–I5) |
| 30 | 671 | 介面 | …¦ 介面 ¦ 企業必須決定的問題 ¦… | KEPT: unchanged | c | model label: header of the I1–I5 table (Table in §3.9.1) |
| 31 | 687 | 介面 | …¦ 企業介面 ¦ 機制 ¦ 缺口（證據單… | KEPT: unchanged | c | model label: Table 3-4 header 企業介面 (protected table; byte-identical) |
| 32 | 699 | 介面 | …表 3-4 以介面彙整；為使審查者能逐格追溯「… | KEPT: unchanged | c | model label: Table 3-4 is organised by I_k |
| 33 | 699 | 企業決策介面 | …查者能逐格追溯「文獻型態 → 缺口候選 → 企業決策介面 → 可觀察機制 → 變數 … | KEPT: unchanged | a-kept | construct term kept as historical label: names the Table 3-4A column 「企業決策介面」 (Table 3-4A is protected); the §3.9.1 note states it is the earlier wording of 企業決策機制, not a third construct |
| 34 | 699 | 介面 | …格列出每一組缺口的家族、網路狀態、文獻解讀、介面、機制、可觀察證據、模型變數… | KEPT: unchanged | c | model label: lists the Table 3-4A columns (介面 = the I_k column) |
| 35 | 703 | 企業決策介面 | …元） ¦ 文獻解讀（相對於零模型基準） ¦ 企業決策介面 ¦ 機制（主／次；狀態） … | KEPT: unchanged | a-kept | Table 3-4A column header (protected, byte-identical); historical wording covered by the §3.9.1 note |
| 36 | 708 | 介面 | …用前沿，未指向獨立的組織配置決策 ¦ 無獨立介面 ¦ —／—；evidenc… | KEPT: unchanged | c | Table 3-4A cell (protected): 無獨立介面 = no separate I_k |
| 37 | 755 | 企業決策介面 | …5）。** Q1 判斷該配對是否對應可辨識的企業決策介面（YES、NO、UNCERT… | CHANGED (H19): (4) **編碼工具（Q1–Q5）。** 為降低獨立編碼者的理解負擔，S1e 問卷採用『企業決策過程』作為 coder-facing wording；其所對應的理論構念仍為本文所稱之企業決策機制／組織決策安排，並不構成另一個不同構念。Q1 判斷該配對是否呈現可辨識的企業決策過程（YES、NO、UNCERTAIN）； | b-sync | coder-facing description of Q1: synced to the S1e wording 企業決策過程 (S1e Q1: 「這段內容是否呈現一個可辨識的企業決策過程？」); verbatim S1e sentence inserted before it |
| 38 | 755 | 企業決策介面 | …三句的理由。NONE 的定義是：存在可辨識的企業決策介面，但 M1–M4、LONGI… | CHANGED (H20): NONE 的定義是：存在可辨識的企業決策過程，但 M1–M4 | b-sync | coder-facing NONE definition: synced to S1e (「只有在存在企業決策過程…」) |
| 39 | 755 | 介面 | … Q1 = UNCERTAIN），沒有獨立的介面時也不使用 NONE（改用 … | CHANGED (H21): 沒有可辨識的企業決策過程時也不使用 NONE（改用 EVIDENCE_ONLY） | b-sync | coder-facing EVIDENCE_ONLY rule: synced to S1e (「沒有可辨識的決策過程時，請選『僅屬證據層』」) |
| 40 | 769 | 介面 | …機制在討論中降為「研究者提出、未獲獨立支持的介面」，但其方程元素可因企業架構… | KEPT: unchanged | d | quoted rollback-rule label 「研究者提出、未獲獨立支持的介面」 from the frozen construct-freeze document 41 (§3.9.5); refers to the I_k of a rejected mechanism; kept verbatim |
| 41 | 771 | 介面 | …機制在討論中降為「研究者提出、未獲獨立支持的介面」，但其方程元素仍可因企業架… | KEPT: unchanged | d | same quoted rollback-rule label (§3.9.5 rule (2)) |
| 42 | 771 | 介面 | …理由保留。(3) 若盲編主張 G04 有獨立介面，需提出 I1–I4 無法表… | KEPT: unchanged | c | model label: rollback rule (3) 「G04 有獨立介面」 = an I_k outside I1–I4 |
| 43 | 779 | 企業決策介面 | …的用語；第 3.9.3 節沿用 S1d 的「企業決策介面」，兩者指同一判斷，S1e … | KEPT; sentence edited (H23): 存在可辨識的企業決策過程（S1e 編碼者材料的用語，第 3.9.3 節已同步；S1d 與本稿先前版本使用「企業決策介面」，兩者指同一判斷，對應的理論構念都是企業決策機制；S1e 只改編碼者用語與答案表版面，不改類別定義） | b-kept | historical quotation of the S1d coder-facing wording; the sentence is updated because §3.9.3 is now synced (it no longer says §3.9.3 uses 企業決策介面) |
| 44 | 825 | 介面 | …s)`, `D_j(s)` 資料可得性、共用介面（`s` 為能力來源狀態） … | KEPT: unchanged | c | v2.2 model term: F5 R_j(s), D_j(s) 資料可得性、共用介面 (data/interface threshold keys) |
| 45 | 1190 | 介面 | …整合，最後有哪些真正形成企業決策問題？ ¦ 介面活化檢驗（interface… | KEPT: unchanged | c | v2.2 model term: 介面活化檢驗 (Table 3-10 Q8) |
| 46 | 1190 | interface | …些真正形成企業決策問題？ ¦ 介面活化檢驗（interface activation te… | KEPT: unchanged | c | v2.2 model term: interface activation test (EN gloss) |
| 47 | 1192 | 介面 | …Q8 是連接兩個分析層的實證檢驗：介面 I1–I4 的模型元素若在… | KEPT: unchanged | c | v2.2 model term: 介面 I1–I4 (Q8) |
| 48 | 1192 | 介面 | …R_X > 0`），或其變數值不同於現況，該介面即被分類為 ACTIVE-R… | KEPT: unchanged | c | v2.2 model term: interface classified ACTIVE/INACTIVE (Q8) |
| 49 | 1192 | 介面 | …定的是要求是否綁住、配置是否不同於現況；一個介面是否改變可行性與企業價值（授… | KEPT: unchanged | c | v2.2 model term: Q8 interface vs Q1–Q6 quantities |
| 50 | 1222 | 介面 | …k)` 與能力來源狀態檢查所需查表格，資料／介面門檻 (F5e) 在實際選定… | KEPT: unchanged | c | v2.2 model term: (F5e) 資料／介面門檻 |
| 51 | 1376 | 介面 | …### 3.14.5 外部評估介面… | KEPT: unchanged | d | section title 3.14.5 外部評估介面 = organisational interface with external evaluators; not the construct |
| 52 | 1797 | 企業決策介面 | …¦ Q1 企業決策介面 ¦ 三位編碼者與兩兩配對 … | CHANGED (H25): ¦ Q1 企業決策過程（S1e 編碼者用語；理論構念為企業決策機制） ¦ | b-sync | coder-facing Q1 row of Table 4-13: synced to S1e (企業決策過程) with the construct named |
| 53 | 1937 | 介面 | …¦ v2.2：(F5e) 資料／介面門檻 ¦ 在所選能力狀態下求… | KEPT: unchanged | c | v2.2 model term: (F5e) 資料／介面門檻 (Table 4-20, SIMULATED_ONLY) |
| 54 | 2148 | 介面 | …¦ Q8 形成企業決策問題的 gaps ¦ 介面活化 → gaps（需要 V… | KEPT: unchanged | c | v2.2 model term: 介面活化 (Table 4-28) |
| 55 | 2148 | interface | …aps（需要 V1） ¦ `derived.interface_activation` ＋… | KEPT: unchanged | c | code key derived.interface_activation |
| 56 | 2177 | 介面 | …**表 4-32：介面活化（Q8）**… | KEPT: unchanged | c | v2.2 model term: Table 4-32 title 介面活化（Q8） |
| 57 | 2179 | 介面 | …¦ 介面 ¦ 綁住的元素（`PR_X… | KEPT: unchanged | c | model label: Table 4-32 header (I1–I4) |
| 58 | 2266 | 介面 | …N RESULT PENDING]`；Q8 介面活化：`[EMPIRICAL… | KEPT: unchanged | c | v2.2 model term: Q8 介面活化 (Table 4-33) |
| 59 | 2277 | 企業決策介面 | … 5.1–5.4 節），再討論從文獻低整合到企業決策介面的轉譯（第 5.5 節）與企… | CHANGED (H26): 再討論從文獻低整合到企業決策機制的轉譯（第 5.5 節） | a | construct term |
| 60 | 2305 | 介面 | …最清楚的一類是技術—治理介面。「預測與風險估計 × 人工… | KEPT: unchanged | d | literature-level functional interface (技術—治理介面 between two AI × decision family regions) |
| 61 | 2305 | 介面 | …廊。低整合因此落在兩個成熟區域之間的直接轉譯介面上。由此可提出幾個可檢驗的機… | KEPT: unchanged | d | literature-level functional interface (直接轉譯介面) |
| 62 | 2322 | 企業決策介面 | …¦ 企業決策介面 ¦ 研究者轉譯經獨立的人類… | CHANGED (H27): ¦ 企業決策機制 ¦ 研究者轉譯經獨立的人類編碼驗證 ¦ | a | construct term (Table 5-1 claim row) |
| 63 | 2323 | 介面 | …、治理價值或實現價值 ¦ 待企業資料（Q8 介面活化檢驗與 Q1–Q6 的計… | KEPT: unchanged | c | v2.2 model term: Q8 介面活化檢驗 (Table 5-1) |
| 64 | 2325 | 介面 | …。最後一種結果不表示文獻分析錯誤，也不表示該介面不重要；它只表示在該企業、該… | KEPT: unchanged | c | model term: the I_k classified INACTIVE by Q8 |
| 65 | 2325 | 介面 | …；它只表示在該企業、該登記的參數集合下，這個介面沒有改變決策。模型也允許「企… | KEPT: unchanged | c | model term: the I_k classified INACTIVE by Q8 |
| 66 | 2327 | 介面 | …少包含由 12 組缺口轉譯出的 I1–I4 介面（G04 留在證據層；G11… | KEPT: unchanged | c | model label: I1–I4 介面 |
| 67 | 2351 | 企業決策介面 | …## 5.5 從低整合接口到企業決策介面… | CHANGED (H28): ## 5.5 從低整合接口到企業決策機制 | a | construct term (heading §5.5) |
| 68 | 2357 | 介面 | …論是：文獻分析所說的「權限耦合」大致對應企業介面 I1（M1：誰可以讓人工智… | KEPT: unchanged | c | model label: 企業介面 I1 (M1 named in the same sentence) |
| 69 | 2429 | 介面 | …制在討論中須降為「研究者提出、未獲獨立支持的介面」（第 3.9.5 節）。文… | KEPT: unchanged | d | quoted rollback-rule label from §3.9.5 / document 41 (kept verbatim) |
| 70 | 2461 | 介面 | …是求解並回填第 4.10 節，包括 Q8 的介面活化檢驗：哪些由文獻低整合轉… | KEPT: unchanged | c | v2.2 model term: Q8 介面活化檢驗 |
| 71 | 2461 | 介面 | … 的介面活化檢驗：哪些由文獻低整合轉譯而來的介面，在企業證據下真的改變了決策… | KEPT: unchanged | c | model term: object of the Q8 test (轉譯而來的介面) |
| 72 | 2461 | 介面 | …否具有決策編排特徵，後者在企業中檢驗轉譯後的介面是否改變決策。… | CHANGED (H29): 後者在企業中檢驗轉譯後的機制是否改變決策。 | a | construct term outside the Q8 sentence (→ 轉譯後的機制) |
| 73 | 2475 | 企業決策介面 | …後，本論文把 16 組主要穩健不足呈現轉譯為企業決策介面，並建立企業—事業單位雙層 … | CHANGED (H30): 本論文把 16 組主要穩健不足呈現轉譯為企業決策機制， | a | construct term |
| 74 | 2475 | 介面 | …程路由與回復、人機配置與反應、評估與保證四個介面，2 組歸入跨期學習擴充，1… | CHANGED (H31): 評估與保證四個機制，2 組歸入 | a | construct term (four M1–M4) |
| 75 | 2850 | interfaces | …rated within platform interfaces"（Introduction… | KEPT: unchanged | c | technical interface: verbatim source quote "platform interfaces" (Appendix B N82) |
| 76 | 2850 | 介面 | …neFirst PDF)） ¦ 區分嵌入平台介面的 AI 與獨立 GenAI… | KEPT: unchanged | c | technical interface: 嵌入平台介面 (Appendix B N82) |
| 77 | 2943 | Interface | …–G16 哪些真正形成企業決策問題 ¦ **Interface activation te… | KEPT: unchanged | c | v2.2 model term: Interface activation test (Appendix C.5, verbatim v2.2) |
| 78 | 2943 | 介面 | …ace activation test**：介面 I1–I4 的模型元素在 … | KEPT: unchanged | c | v2.2 model term: 介面 I1–I4 (Appendix C.5, verbatim v2.2) |

## 6. Kept on purpose (math / model semantics)

- No math span, equation tag, G row, Table 3-4/3-4A row or note, or Appendix C.1–C.9 text was edited (hard checks). The v2.2 model terms 「介面 I1–I5」, 「介面活化檢驗」/interface activation test, `derived.interface_activation`, 「資料／介面門檻」(F5e) and 「共用介面」 (R_j, D_j) are model terms, not the V1 construct, and are kept. Renaming them would alter model-term semantics, so they are reported here and left unchanged.
- Literature-level 「接口」/EN "interface" (functional AI × decision pairing) and 「技術—治理介面」「直接轉譯介面」 in §5.3.1 are literature-structure terms and are kept.
- The rollback-rule label 「研究者提出、未獲獨立支持的介面」 (§3.9.5 ×2, §5.8.4) is quoted from the frozen construct-freeze document 41 and refers to the I_k of a rejected mechanism; kept verbatim (class d).

```
ENTERPRISE_DECISION_INTERFACE_BEFORE=17
ENTERPRISE_DECISION_INTERFACE_AFTER=5
CHANGED_TO_MECHANISM=11 (zh) + 2 EN
SYNCED_TO_S1E_PROCESS=3 (+ 1 bare 介面 in the EVIDENCE_ONLY rule)
KEPT_HISTORICAL_OR_PROTECTED=3
BARE_介面_CHANGED=11
BARE_介面_KEPT=41
GLOBAL_REPLACE=NO
S1E_PACKETS_CHANGED=NO
VERBATIM_S1E_SENTENCE_INSERTED=YES (§3.9.3 (4), once)
```
