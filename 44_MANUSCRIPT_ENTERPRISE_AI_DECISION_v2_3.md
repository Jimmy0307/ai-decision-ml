# 企業人工智慧導入作為多層級決策系統：治理、能力配置、組織採用與價值實現

**Enterprise AI Adoption as a Multilevel Decision System: Governance, Capability Allocation, Organizational Adoption, and Value Realization**

**稿件版本：v2.3 empirical-execution candidate（2026-10-11）。Supersedes `44_MANUSCRIPT_ENTERPRISE_AI_DECISION_v2_2.md`；除第肆章、參考文獻的 v2.3 核對結果與附錄 B／E 外，全文沿用 v2.2（含其 Drive reconciliation 註記）。第肆章改為可由真實資料直接回填的骨架（59–65），未填入任何結果。** `[DRIVE RECONCILIATION COMPLETE：v2.2 變更已以 Google Drive 權威 v2.1 全文（100,827 bytes）為 current、Claude 本機 v2.1（99,649 bytes）為 base、bundle v2.2 為 proposed change 完成三方合併；三處重疊文字已逐項裁決，保留 Drive 的 corpus-parity 限制並納入 v2.2 的 783-document lineage 與 reference-closure 更新。]` 本稿整合 `41`（G01–G16 收斂與構念凍結）、`42` v2.2（企業 AI portfolio 多層模型）、`43`（參數識別）、`45` v2.2（驗證計畫）、`50`–`52`（v2.2 求解器與 synthetic 驗證）、`53B`–`56`（V1 盲編與 EA-X 內容效度）、`57`（引文核對）。**本稿不報告任何企業實證效果、ROI、樣本結果或已校準的最適配置。** 第四章為結果骨架；凡尚無資料處標示 `[EMPIRICAL RESULT PENDING]`，凡參數尚未識別處標示 `UNIDENTIFIED`。第四章 4.5 節所報的 synthetic oracle 結果僅為實作一致性證據（`SIMULATED_ONLY`），不是企業結果；4.1 與 4.2 節的 AI 編碼與 AI 評分只是 pilot（`AI-BLIND-CODING PILOT`、`AI_CONTENT_VALIDITY_PILOT`），不是人類構念效度證據。

---

## 中文摘要

企業導入人工智慧已由單一工具採用，轉為在有限預算、工程容量、共享能力與治理限制下，對多個 AI initiatives 進行配置的決策問題。模型能力或局部生產力的改善，並不能直接回答企業應集中建置哪些共享能力、如何設定 AI 授權與人工介入的邊界、資源應如何在事業單位間分配，以及使用者的實際反應如何改變投資的實現價值。本研究將企業 AI 導入建構為多層級決策系統，並以前階段大規模 AI × Decision 文獻網絡中 16 個穩健低連結（robust depletion）功能配對（G01–G16）作為研究線索。經研究者逐格收斂（AI 盲編 pilot 已完成，對其中 G04、G10、G11 三格提出不同編碼；人類雙人盲編尚待完成），12 個配對對應到四個企業決策介面——授權與問責（M1）、流程路由與回復（M2）、人機配置與反應（M3）、評估與保證（M4）——另有 2 個屬跨期學習擴充、1 個為資料條件模組、1 個僅留於證據層；策略契合與吸收能力可由既有企業層變數表達，故不另立構念。在此基礎上，本研究建立 Enterprise–Business Unit 雙層 portfolio 模型：企業層選擇共享能力、治理方案與資源 envelope；事業單位依其被考核的帳本選擇各 initiative 的配置；角色別使用者反應以條件分布內嵌於期望結果中。所有序位構念只作同構念門檻或查表鍵；共享固定成本只在企業層計一次；不可貨幣化的法規與安全底線為硬限制；未識別參數不以零或任意係數補齊。模型定義了集中規劃價值（VCP，可再分為資源重分配與帳本對齊兩部分）、共享能力價值（VSC）、授權損失（DL）與淨企業架構價值（NEV = VCP + VSC − DL），並給出證明草稿：帳本對齊時授權損失為零；在集中規劃下治理要求本身不增加已定價的價值，但在雙層且帳本不對齊時，要求可藉由篩除部門的不利選擇而提高企業價值；共享能力投資具唯一的損益兩平固定成本，但共享重用效果在雙層且帳本不對齊時可使建置區域成為非單調的集合。模型以有限列舉求解，並以 ROBUST、CONDITIONAL、FRAGILE、UNIDENTIFIED 分類決策對參數不確定性的穩健性。合成資料的參考實作（v2.2）在 20 項 synthetic engineering 檢查中全部通過，包括一項由獨立代理者手算的 oracle，並經兩輪對抗式稽核修正；這只表示實作與方程一致、命題未被合成反例反駁。企業實證校準尚待完成。

**關鍵詞：** 企業人工智慧導入；多層級決策；雙層最佳化；AI 治理；共享能力；人機協作；價值實現

## Abstract

Enterprise adoption of artificial intelligence has shifted from adopting individual tools to configuring a portfolio of AI initiatives under limited budget, engineering capacity, shared capabilities, and governance constraints. Improvements in model capability or local productivity do not determine which capabilities an enterprise should build centrally, how it should bound AI authority and human intervention, how resources should be allocated across business units, or how users' actual responses alter realized investment value. This study conceptualizes enterprise AI adoption as a multilevel decision system and uses sixteen robustly depleted AI-family × decision-family pairings (G01–G16) from a prior large-scale AI × Decision literature network as research leads. In a researcher-adjudicated, cell-by-cell convergence that still awaits human blind coding (an AI blind-coding pilot diverged from the researcher on G04, G10, and G11), twelve pairings map onto four enterprise decision interfaces—authority and accountability (M1), workflow routing and recovery (M2), human–AI configuration and response (M3), and evaluation and assurance (M4); two belong to a longitudinal learning extension, one to a data-gated module, and one remains in the evidence layer. Strategic alignment and absorptive capacity can be expressed through existing enterprise-level variables and are therefore not added as separate constructs. On this basis, the study formulates an Enterprise–Business Unit bilevel portfolio model in which the enterprise selects shared capabilities, a governance profile, and resource envelopes; business units select initiative configurations according to the ledgers on which they are evaluated; and role-specific user responses enter expected outcomes as conditional distributions. Ordinal constructs serve only as within-construct thresholds or lookup keys, shared fixed costs are counted once at the enterprise level, non-monetizable legal and safety boundaries are hard constraints, and unidentified parameters are never replaced by zeros or arbitrary coefficients. The model defines the value of central planning (VCP, decomposable into reallocation and ledger-alignment components), the value of shared capability (VSC), delegation loss (DL), and net enterprise-architecture value (NEV = VCP + VSC − DL). Proof sketches indicate that delegation loss is zero when ledgers are aligned; that under central planning governance requirements cannot by themselves raise priced value, whereas in the bilevel setting with misaligned ledgers requirements can raise enterprise value by screening out harmful unit choices; and that each shared capability has a unique break-even fixed cost, whereas the reuse effect can make the build region non-monotonic in the bilevel setting with misaligned ledgers. The model is solved by finite enumeration, and decisions are classified as ROBUST, CONDITIONAL, FRAGILE, or UNIDENTIFIED under admissible parameter uncertainty. A synthetic reference implementation (v2.2) passed all twenty synthetic engineering checks, including an independently hand-derived oracle, after two rounds of adversarial review; this shows only that the implementation agrees with the equations and that the propositions were not refuted on synthetic instances. Enterprise empirical calibration remains pending.

**Keywords:** enterprise AI adoption; multilevel decision making; bilevel optimization; AI governance; shared capabilities; human–AI collaboration; value realization

---

# 壹、緒論

## 1.1 研究背景

人工智慧在企業中的角色，已由單一模型或單一任務自動化，轉為跨部門、跨系統的能力配置問題。當預測、建議、生成、協調執行與評估等 AI 能力同時進入財務、銷售、製造、研發、採購、品質與資訊等功能單位，企業面對的核心決策不再是「是否採用 AI」，而是：哪些能力應以企業共享平台建置、哪些應由部門自行處理；何種決策可以授權 AI 提出或執行、何種情境必須保留可行的人工否決與停止權；有限的工程、資料、運算與治理資源應如何在多個 initiatives 之間分配；以及這些安排如何透過使用者的實際反應轉化為企業價值。

這些問題具有三個共同特徵。第一，它們是**配置問題**：同一項共享能力可同時支援多個 initiatives，但各 initiative 的資料條件、錯誤後果、流程整合需求與價值來源不同，因此企業決策是在可行配置集合中進行選擇，而不是對單一系統做採用與否的判斷。第二，它們是**多層問題**：企業層設定政策、共享能力與資源上限，事業單位在其限制下選擇局部配置；兩層的目標是否一致，取決於事業單位被考核的帳本是否涵蓋其配置對企業其他部分造成的後果。第三，它們受**組織反應**中介：管理層設計的配置不等於組織實際的使用；使用者可能採用、查核、修改、升級、拒用或繞過 AI 輸出（Dietvorst, Simmons, & Massey, 2015；Logg, Minson, & Moore, 2019；Kellogg, Valentine, & Christin, 2020），而這些反應決定了實際的成本、風險與價值。

因此，本研究把企業 AI 導入界定為一個**在治理、共享能力、資源與組織反應共同限制下的多層 portfolio 決策問題**。研究的核心不是「AI 有沒有用」，也不是「某一個 AI project 的 ROI 是多少」，而是：

> 當企業全面導入 AI 時，企業應如何在治理、共享能力、資料、預算、人力、風險、事業單位需求與組織採用的共同限制下，配置一組 AI initiatives，使企業整體可實現價值最大，並辨識此配置對不確定參數是否穩健？

## 1.2 前階段文獻網絡證據

本研究的問題來源是前階段的大規模 AI × Decision 文獻網絡分析（V5）。該分析將文獻中的語意證據紀錄映射到 10 個 AI 功能族與 12 個決策功能族，形成 10 × 12 = 120 個可能的功能配對格；經文件層級去重後，正式網絡為 M = 2,180 條 document-level AI-family × Decision-family edges（注意：此數不同於去重前的 3,125 筆 fully mapped semantic records）。以固定度數二部網絡零模型（10,000 次複製、BH-FDR）推論，47 格在 q ≤ .05 下顯著；再經 exact hypergeometric 驗證、document-preserving 結構零模型與 raw-record 敏感度分析，32 格在所有必要檢定中皆顯著且方向一致，構成最終 robust core：16 個 enrichment 與 16 個 depletion。

本研究以這 16 個 robust depletion 格（G01–G16）作為研究線索。Depletion 在此只表示：**在指定的零模型結構與觀察邊際下，該 AI 功能族與決策功能族的配對在文獻中相對低度出現。** 它不表示企業中存在 16 個問題，不表示相應功能無效、不相容或不重要，也不提供任何模型權重。網絡證據另有一項幅度解讀上的限制：AI 側證據有相當比例來自摘要層級，決策側則以全文為主；因此本研究只使用 depletion 的方向作為研究線索，而不使用其幅度。

**語料 lineage（v2.1 已調和；見 49 號文件）。** V5 網絡建構的分析單位依序為：6,499 筆 strict analytical records → 3,125 筆 fully mapped（pair-eligible）semantic records → 783 篇 pair-eligible unique documents → M = 2,180 條 document-level AI-family × Decision-family edges；3,125 與 2,180 之差（945）是文件層級去重時合併的重複紀錄，不是兩個互相競爭的語料規模。V5 Stage 2 的受限雙 pass 語意映射模型為 `qwen2.5:14b`。較早的 two-track 語料線（404 篇最終文獻、2,425 筆 strict records、GPT-5.6 Sol 語意編碼）屬前階段的語料與證據產生紀錄，只作歷史 provenance 保留，**不是** G01–G16 凍結網絡的分母，也不寫入定義 M = 2,180 的方法敘述。AI 側摘要／Decision 側全文的不對稱仍是 corpus-parity 限制，因此本研究只使用 robust depletion 的方向作為 research lead，不把幅度、O/E 或 q 值帶入企業模型。

## 1.3 研究缺口

既有研究分別提供了理解企業 AI 導入的重要片段，但這些片段之間的連接正是本研究要處理的缺口。

**第一，相對於零模型，文獻中若干 AI—決策功能配對的連結明顯偏低。** G01–G16 顯示，風險估計類 AI 與審查問責、治理監督、評選、資訊取得及一般決策流程之間（G02、G09、G10、G12、G14），協調執行類 AI 與風險評估及人工審查之間（G03、G16），解釋與評估類 AI 與預測、配置及評選決策之間（G05、G06、G11、G13、G15），以及增強人類判斷的 AI 與預測及評選之間（G01、G07），在文獻中都相對少被連結。

**第二，這些低連結配對可收斂為少數企業決策介面。** 研究者的逐格收斂（第四章 4.1 節、41 號文件；尚待 V1 雙人盲編）指出，12 個配對共同指向四個企業必須做出的配置決策：誰可以讓 AI 輸出成為行動並承擔責任（授權與問責，M1）；AI 輸出如何進入下一個決策節點、例外與失敗如何回復（流程路由與回復，M2）；人與 AI 的順序、最終權與實際反應（人機配置與反應，M3）；以及何種驗證、監控與可用解釋是某一授權深度的前提（評估與保證，M4）。

**第三，這四個介面在企業中不是彼此獨立的部門問題，而是透過共享能力、共同預算、共同工程容量與共同政策耦合在一起。** 治理研究說明了決策權配置的重要性（Sambamurthy & Zmud, 1999；Weill & Ross, 2004；Papagiannidis, Mikalef, & Conboy, 2025），人機協作研究說明了配置與相對能力的重要性（Shrestha, Ben-Menahem, & von Krogh, 2019；Vaccaro, Almaatouq, & Malone, 2024），組織準備度研究說明了多面向前提條件（Jöhnk, Weißert, & Wyrtki, 2021），IT portfolio 研究說明了在相依專案間進行選擇的需要（McFarlan, 1981；Archer & Ghasemzadeh, 1999）。然而，這些研究並未共同提供一個能同時處理「企業共享能力與政策如何限制多個事業單位」、「事業單位配置如何透過角色別反應轉化為結果」，以及「共享成本、局部成本、風險與價值如何在不重複計算、不把序位量表當基數效用的前提下比較」的正式架構。

**第四，因此需要數學模型。** 一旦問題被界定為在耦合限制下的多層配置，口語化的框架就不足以回答「企業協調架構是否比各部門自行導入更有價值」、「共享能力在什麼成本下值得集中投資」、「治理在什麼條件下增加價值而非只增加官僚成本」等問題；這些問題需要可計算的目標、限制、層級結構，以及對未識別參數的明確處理規則。

由此形成本研究的證據鏈：

`大規模 AI × Decision 文獻網絡 → G01–G16 結構性低連結 → 四個企業決策介面（M1–M4）→ 企業 AI 架構（共享能力、治理、資源）→ 多層配置（企業—事業單位）→ 組織反應 → 企業 AI portfolio → 價值實現與穩健性`

## 1.4 研究目的

1. 將 G01–G16 收斂為最小充分的企業機制與構念架構，並建立 gap → 機制 → 可觀察狀態 → 變數 → 方程的可追溯鏈。
2. 將企業 AI 導入形式化為可求解的 Enterprise–Business Unit 雙層 portfolio 模型，同時處理共享能力、共享與局部成本分離、資源耦合、政策耦合、硬性風險限制與角色別使用者反應。
3. 定義可回答「企業協調是否值得」的比較量，並以模型命題釐清這些比較量的符號、來源與判讀界線。
4. 建立以模型識別需求為結構的參數識別規格，使資料缺口本身成為可報告的研究結果。
5. 建立有限列舉求解程序與不確定性分類，並以合成 oracle 驗證實作與方程一致。
6. 在企業實證校準完成後，回答下列研究問題並報告其穩健性。

## 1.5 研究問題

**RQ1（企業治理）** 企業層級的治理方案、共享能力與資源配置如何改變各事業單位的可行配置與實際選擇？

**RQ2（跨層對齊）** 在何種帳本與限制條件下，事業單位的局部最適偏離企業最適？偏離造成多少企業價值損失？

**RQ3（組織採用）** 授權深度、人工介入、流程整合與評估保證的配置，如何對應到角色別的使用、查核、修改、升級、拒用與繞過反應？這些反應如何改變投資的實現價值？

**RQ4（企業 portfolio 配置）** 在有限預算、工程容量、共享能力、治理要求與異質事業單位需求下，企業應如何選擇共享能力、治理方案與 initiative 配置？

**RQ5（價值實現與穩健性）** 哪些 portfolio 決策在可接受的參數不確定性下穩健，哪些僅在特定情境下成立或對小幅參數變動脆弱？

五個研究問題對應到八個可計算的研究命題（第三章 3.7、3.10 與第四章各節）：

| # | 命題 | 計算量 | RQ |
|---|---|---|---|
| Q1 | 各部門自行導入 AI 與企業協調的 portfolio，何者產生較高企業價值？ | NEV = VCP + VSC − DL；VCP = VRA + DL0 | RQ1, RQ4 |
| Q2 | 共享能力在什麼條件下值得集中投資？ | 損益兩平固定成本 `F_c^†`、重用門檻 `δ^†` | RQ4 |
| Q3 | 治理在什麼條件下提高價值，而不是只增加官僚成本？ | VG = EE + RE + CE | RQ1 |
| Q4 | 事業單位局部最適何時偏離企業最適？ | DL 及其來源分解 | RQ2 |
| Q5 | 人工監督、流程整合與評估保證在什麼條件下是必要限制，而非越多越好？ | 要求代價 `PR_X`、AT／ABOVE 狀態、robustness-protective 判定 | RQ1, RQ3 |
| Q6 | 使用者的採用、查核、拒用行為如何改變 AI 投資的實現價值？ | VRG、design-response regret | RQ3 |
| Q7 | 哪些 portfolio 決策 ROBUST，哪些 FRAGILE？ | 元素層級穩健性分類、MaxRegret | RQ5 |
| Q8 | G01–G16 揭露的文獻斷裂，最後有哪些真正形成企業決策問題？ | Interface activation test | RQ1–RQ3 |

## 1.6 預期貢獻

**理論貢獻。** 第一，本研究建立文獻網絡低連結與企業決策介面之間的中介層，使 bibliometric depletion 不會被誤寫成企業事實，也不會被當成模型權重。第二，本研究把企業 AI 導入由採用分數或成熟度評估，轉為一個具明確層級、帳本與限制的 portfolio 決策架構。第三，本研究以帳本對齊條件說明跨層衝突何時存在：跨層衝突不是由模型形式假設而來，而是可由會計、預算與考核文件檢驗的實證命題。

**方法貢獻。** 第一，本研究提供一套同時處理共享固定成本、能力前提、資源 envelope 與政策耦合的有限離散雙層模型，並證明 envelope 的有限化（Lemma E′：只需以部門自身可行計畫的資源向量作為候選 envelope），使模型可精確求解。第二，本研究嚴格區分序位與基數、名義權限與有效控制、設計反應與實際反應，並給出缺值的拒算與部分輸出規則。第三，本研究以集合式不確定性與 regret 進行決策元素層級的穩健性分類，避免以單一最有利情境作為結論。

**實務貢獻。** 模型的輸出不是單一「最佳 AI 方案」，而是：在什麼成本以下值得建置某項共享能力、哪一個帳本安排會讓部門偏離企業利益、哪些治理要求只增加成本、哪些決策在合理不確定性內不會改變，以及哪些參數最值得優先量測。

## 1.7 章節安排

第貳章回顧企業 AI 導入、治理與決策權、流程整合、人機配置與組織採用、評估保證、共享能力與 portfolio 邏輯、多層與雙層決策等文獻，並逐節說明其支持與不支持的主張及對模型的意涵。第參章提出研究設計、構念操作化、gap-to-mechanism 轉譯與完整的數學模型、求解程序、不確定性分析與 V0–V7 驗證流程。第肆章為結果骨架。第伍章為討論骨架，第陸章為結論骨架。

---

# 貳、文獻回顧與理論架構

本章每一節依相同順序撰寫：文獻主張 → 支持什麼 → 不支持什麼 → 對模型的意涵。逐篇引文的精確主張、驗證狀態與對應模型元素列於附錄 A。

## 2.1 企業 AI 導入與 AI 準備度

**文獻主張。** Berente、Gu、Recker 與 Santhanam（2021）在 *MIS Quarterly* 管理 AI 特刊的編輯評論中，將「管理 AI」界定為資訊科技管理的新階段。Jöhnk、Weißert 與 Wyrtki（2021）以訪談與文獻歸納出五類、18 項組織 AI 準備度因素，涵蓋策略契合、資源、知識、文化與資料等面向。Mikalef 與 Gupta（2021）發展衡量企業 AI capability 的工具，並報告其與組織創造力及企業績效相關（本稿不採用原文的因果措辭）。Enholm、Papagiannidis、Mikalef 與 Krogstie（2022）回顧 AI 創造企業價值的文獻，整理促成與阻礙因素，以及第一序與第二序效果。Brynjolfsson、Rock 與 Syverson（2021）指出，像 AI 這類通用技術需要大量難以衡量的無形互補投資，使量測到的生產力可能先下降後上升（productivity J-curve）。

**支持什麼。** 企業 AI 導入是多面向的組織能力問題，而不只是技術問題；價值實現需要互補投資，且其時間型態可能延遲。

**不支持什麼。** 這些研究不提供在多個 initiatives 之間配置有限資源的決策規則；能力與績效的相關不能被解讀為特定企業中某項投資的因果效果；準備度因素也不能被加總為可直接最佳化的成熟度分數。

**對模型的意涵。** (i) 本研究不以成熟度總分作為模型本體；準備度中與配置直接相關的部分（資料可得性、介面、決策權）被表達為由企業決策決定的門檻鍵 `R_j(y)`、`D(y)`、`G_j(γ)`，其餘因素作為情境描述。(ii) 互補投資必須明確出現在成本中——共享能力成本 `F_c` 與局部導入成本 `C^impl`——而不是隱含在「AI 效益」裡。(iii) J-curve 意味靜態單期模型可能低估或高估長期價值；跨期效果歸入 M5 動態擴充，而不是在靜態模型中以假設的成長率補足。

## 2.2 AI 治理與決策權

**文獻主張。** Sambamurthy 與 Zmud（1999）將 IT 治理安排界定為企業中關鍵 IT 活動的權威配置模式，並主張其型態受多重情境因素共同決定。Weill 與 Ross（2004）以決策權的配置作為 IT 治理的核心。Papagiannidis、Mikalef 與 Conboy（2025）回顧負責任 AI 治理文獻，提出由結構性、關係性與程序性實務構成的框架。Aghion 與 Tirole（1997）區分正式權威（決定的權利）與實質權威（有效控制），並指出實質權威由資訊結構決定。Elish（2019）指出在複雜自動化系統中，控制能力有限的操作者可能承擔被錯置的責任。NIST（2023）的 AI 風險管理框架與 ISO/IEC 42001:2023 的 AI 管理系統標準，分別提供自願性的風險管理結構與組織管理系統要求；歐盟《人工智慧法》（Regulation (EU) 2024/1689）則建立具法律拘束力的統一規則（該規則已由 Regulation (EU) 2026/1744 修正；本稿不依賴該修正後新增的任何條文）。

**支持什麼。** (i) 治理是決策權的配置，且沒有單一最佳形式；(ii) 名義上的權限與實際上的控制能力可能不一致；(iii) 部分 AI 使用受外部法規與標準的硬性約束。

**不支持什麼。** 這些文獻不提供 AI 授權深度與人工介入的具體門檻值；不證明任何特定治理方案會提高企業價值；也不支持「有人簽核」即等於有效控制。NIST 與 ISO 是結構參照，不是本企業的參數來源；法規條文的適用須逐條核對，不能以框架的存在推論特定要求。

**對模型的意涵。** (i) 治理以有限的 policy profile 選單 `γ ∈ Γ` 表示，每個 `γ` 決定允許集合 `Allow_γ`、正式決策權 `G_j(γ)`、`A × κ` 的同構念要求表與嚴重事件容忍上限 `ē_j^γ`。(ii) 名義介入權 `H` 與有效控制 `Eff_H` 分開；當要求行動前否決權時，必須同時具備有效控制（42 F6）。(iii) 法規、權利、隱私與安全底線以 `Legal_jk` 與 (F9) 硬限制表示，不換算成金額。(iv) 治理的價值不預設為正；第三章以 VG 的分解檢驗治理究竟是賦能還是只增加成本。

## 2.3 流程整合與跨功能協調

**文獻主張。** Amershi 等人（2019）觀察 Microsoft 團隊開發 AI 應用，指出機器學習被納入類敏捷工作流程時，在資料管理、技能與模組化方面面臨特有挑戰。Sculley 等人（2015）指出，機器學習系統雖可快速建置，卻伴隨隱藏的技術債。Raisch 與 Krakowski（2021）指出在管理情境中，自動化與增強無法被整齊地永久分離。Kellogg、Valentine 與 Christin（2020）將工作場所中的演算法控制歸納為六種機制，並描述工作者的抵抗方式。

**支持什麼。** AI 輸出進入組織流程需要實質的整合、資料管理與維護投入；同一能力在一個流程步驟可能是自動化，在另一個步驟可能增加人工協調與監督負擔；流程設計會引發使用者的調適與抵抗。

**不支持什麼。** 這些研究不提供本企業的整合成本或維護成本大小，也不支持「整合程度越高越好」。技術債的論點說明維護成本不可忽略，但不提供其量級。

**對模型的意涵。** (i) 流程整合以同構念門檻 `WI_k ≥ WI^req_γ(A_k, κ_j)` 表示；授權深度提高時，fallback／rollback 路徑 `FB_jk` 是可行性的前提（F7）。(ii) 整合、維護、監控與 rollback 準備是期間化的局部導入成本 `C^impl`，且消耗工程容量；這些成本必須逐項識別。(iii) 自動化與增強不被寫成二元選擇，而是由配置型態 `m_k` 與授權深度 `A_k` 的組合表示。

## 2.4 人機決策配置與組織採用

**文獻主張。** Shrestha、Ben-Menahem 與 von Krogh（2019）指出組織中人與 AI 的決策可採完全委託、兩種方向的序列式安排與聚合等結構。Vaccaro、Almaatouq 與 Malone（2024）對 106 項實驗、370 個效果量進行統合分析，發現人機組合平均而言不優於人或 AI 單獨表現中較佳者，且決策任務與表現損失相關、效果隨任務型態與相對表現而異。Bansal 等人（2021）發現解釋會提高使用者接受 AI 建議的可能，不論建議是否正確。Dietvorst、Simmons 與 Massey（2015）發現人們在看到演算法出錯後，比看到人類出錯更快失去信心而迴避演算法；Logg、Minson 與 Moore（2019）則發現一般人在認為建議來自演算法時更願意採納。Lebovitz、Lifshitz-Assaf 與 Levina（2022）發現專業人員在 AI 結果與其初始判斷分歧且工具不透明時，不確定性上升，並以此決定是否投入使用。

**支持什麼。** (i) 人機配置有多種結構，必須記錄順序、最終權與是否聚合；(ii) 人機組合不必然產生互補效益；(iii) 使用者反應的方向不固定——可能過度採用，也可能迴避或拒用——且受可見訊號（例如與自身判斷是否分歧）影響。

**不支持什麼。** 這些研究不提供任何企業中角色別反應的機率；實驗室或特定專業情境的效果不能外推為本企業效果；文獻中的平均效果量也不能作為本企業的 `OBSERVED` 值。

**對模型的意涵。** (i) 配置型態 `m_k ∈ {HumanOnly, AI→Human, Human→AI, Aggregation, Delegated, BoundedExecution}` 為名義變數，與授權深度 `A_k` 的一致性由 `Cons(A,m)` 檢查。(ii) 使用者反應以 `ρ_j(r | k, z, ℓ)` 表示，條件於行動當下可見的訊號 `z`，不含隱藏結果 `ω`；反應集合包含拒用與繞過。(iii) 區分程序設計的反應 `ρ^design`、已部署配置的實際反應 `ρ^obs` 與未部署配置的引出反應 `ρ^cf`；兩者之差定義價值實現落差（VRG）。(iv) 不預設使用者為第三層最佳化者；只有在五項條件全部成立時才建立第三層（3.9 節）。

## 2.5 評估、保證與可信任使用

**文獻主張。** Breck、Cai、Nielsen、Salib 與 Sculley（2017）提出 28 項測試與監控需求作為機器學習系統生產就緒度的評量準則。Raji 等人（2020）提出支援 AI 系統端到端開發的內部演算法稽核框架。Bansal 等人（2021）的發現（2.4 節）同時意味：提供解釋與降低風險是兩個不同的問題。

**支持什麼。** 驗證、監控、重驗證與稽核是可被記錄、可被分級的實質活動，且有成本；解釋的可用性需要與驗證證據分開衡量。

**不支持什麼。** 這些研究不支持「評估保證越多，損失必然越低」，也不支持解釋必然改善決策。

**對模型的意涵。** (i) 評估保證證據 `EA_k`（EA-V）以同構念門檻 `EA_k ≥ EA^req_γ(A_k, κ_j)` 進入可行性，其成本進 `C^impl`；它對結果的影響只透過有證據的結果查表 `P(z, ω | k)`，不是單調的風險降低項。(ii) 解釋可用性 `EAX_k` 在通過內容效度前，只作反應分布 `ρ` 的分組鍵（G13、G15）。(iii) 企業層的共享評估基礎設施 `y_EVAL` 是較高評估等級的能力前提（G05）；模型輸出本身附帶 provenance 與穩健性等級，作為企業配置決策的保證。

## 2.6 共享 AI 能力與企業 portfolio 邏輯

**文獻主張。** McFarlan（1981）以資訊系統專案失敗仍屢見不鮮為起點，主張在導入前同時評估資訊系統專案的個別風險與 portfolio 層級風險。Archer 與 Ghasemzadeh（1999）提出將專案組合選擇分為不同階段的整合框架。Teece（1986）指出創新者常無法從創新取得顯著經濟報酬，價值歸屬取決於模仿難易與互補資產的取得。Brynjolfsson 等人（2021）強調無形互補投資（2.1 節）。Benaroch 與 Kauffman（1999）主張選擇權定價分析適用於不可逆且不確定的 IT 投資評估。Sculley 等人（2015）指出，真實世界的 ML 系統常伴隨大量持續維護成本（隱藏技術債）；本研究據此推論，**共享** ML 基礎設施的持續維運成本不可忽略——「共享」這一延伸是研究者的推論，不是原文主張。Cohen 與 Levinthal（1990）將吸收能力界定為企業辨識、吸收與應用外部新知識的能力，並指出其依賴先前相關知識的累積。

**支持什麼。** (i) 多個 initiatives 之間存在相依性，必須在 portfolio 層而非逐案層級做選擇；(ii) 能否實現價值取決於互補能力；(iii) IT 投資具有選擇權價值；(iv) 組織吸收新能力的程度是跨期累積的。

**不支持什麼。** 這些研究不支持「共享能力一定比部門自建便宜」，不提供重用效果的大小，不提供本企業的選擇權價值，也不支持把吸收能力當成靜態分數。

**對模型的意涵。** (i) 共享能力以二元決策 `y_c` 表示，其固定成本 `F_c` 只在企業層計一次（OBJ-E）；能力前提以 `q_jk ≤ ȳ_jc` 表示（F4）。(ii) 重用效果 `δ` 是局部導入成本隨能力狀態變化的查表差額，沒有證據時不假設為正，而以損益兩平 `δ^†` 報告；在雙層且帳本不對齊時，建置區域可能不是單一門檻而是集合（3.10 節 P4）。(iii) 共享能力是否值得集中投資，以唯一門檻 `F_c^†` 回答（命題 P4）。(iv) 選擇權價值不進靜態目標，歸入 M5。(v) 吸收能力不作靜態構念：其靜態部分以共享的變革／訓練能力 `y_CHG` 表達（僅在有證據時改變 `ρ`），累積部分歸 M5。

## 2.7 多層與雙層決策

**文獻主張。** Kozlowski 與 Klein（2000）綜整組織多層次理論，強調跨層次的情境、時間與湧現過程。Colson、Marcotte 與 Savard（2007）回顧雙層最佳化的形式、應用與解法；Dempe（2002）提供雙層規劃的理論基礎。Moore 與 Bard（1990）指出依序行動的非合作賽局可建模為雙層問題，並為混合整數線性雙層問題發展列舉式分枝定界方法。Wiesemann、Tsoukalas、Kleniati 與 Rustem（2013）研究悲觀雙層最佳化的存在性、複雜度與解法。Kleinert、Labbé、Ljubić 與 Schmidt（2021）回顧以混合整數規劃技術求解雙層問題的方法。Alonso、Dessein 與 Matouschek（2008）證明，即使協調相對於調適極為重要，分權仍可能優於集權，原因在於資訊如何被傳遞。在不確定性下的決策方面，Ben-Tal、El Ghaoui 與 Nemirovski（2009）系統化了穩健最佳化，Lempert、Popper 與 Bankes（2003）主張以電腦輔助、跨大量可能未來的穩健決策方法取代對單一預測的依賴，regret 為基礎的決策準則一般溯源至 Savage（1951）`[VERIFY：歸屬待以原文核對]`。

**支持什麼。** (i) 企業與事業單位依序決策、各有目標的結構可用雙層模型表示；(ii) 下層有多個最適解時，必須區分樂觀與悲觀的上層界；(iii) 下層為整數問題時，需要專門方法；(iv) 集中不必然優於分權；(v) 在參數無法以機率分布識別時，可用集合式穩健性與 regret 判讀決策。

**不支持什麼。** 這些文獻不證明任何企業中企業層與事業單位的目標實際不一致；雙層數學形式的存在不等於真實的跨層衝突；也不支持在沒有使用者獨立裁量證據時建立第三層。

**對模型的意涵。** (i) 基線為 Enterprise–Business Unit 雙層：企業選 `(y, γ, e)`，事業單位在 envelope `e_u` 內依其帳本選配置；使用者反應內嵌於 `ρ`。(ii) 因下層為整數選擇，KKT 單層重構不成立；在已識別規模下採有限列舉，並證明 envelope 只需考慮有限集合（Lemma E）。(iii) 樂觀與悲觀界分別報告。(iv) 跨層衝突以帳本對齊條件 (AL1)–(AL4) 檢驗；對齊時授權損失為零（P2）。(v) 本模型為完全資訊模型，因此在模型內集中規劃必然弱優於雙層（P3）；Alonso 等人（2008）所示的分權資訊優勢不在本模型內，這是本研究的明確界線。(vi) 不確定性以預先登記的情境組與 regret 處理，輸出 ROBUST／CONDITIONAL／FRAGILE／UNIDENTIFIED。

## 2.8 研究缺口與整合架構

綜合 2.1–2.7 節與 G01–G16 的收斂結果（41 號文件；第四章 4.1 節），本研究提出以下整合架構：

```
                     ┌──────────────── Enterprise (Leader) ─────────────────┐
                     │ shared capabilities y_c   governance profile γ ∈ Γ   │
                     │ resource envelopes e_u    [F5]          [M1: G09]     │
                     └───────────────┬───────────────────────────┬──────────┘
            capability prerequisites │ policy: Allow, G(γ),       │ budget / ENG
            reuse table C^impl(ȳ)    │ H/WI/EA/G requirements,    │ envelopes
                                     │ incident tolerance ē       │
                     ┌───────────────▼───────────────────────────▼──────────┐
                     │ Business Unit (Follower): one configuration per       │
                     │ initiative k = (A, H, WI, EA, EAX, m), local builds   │
                     │ M1 [G02,G08,G16]  M2 [G03,G14]  M3 [G01,G07]  M4 [G06,│
                     │ G13,G15]   objective = accountability ledger (OBJ-U)  │
                     └───────────────┬──────────────────────────────────────┘
                                     │ visible signal z (hidden ω)
                     ┌───────────────▼──────────────────────────────────────┐
                     │ Role-specific response ρ(r | k, z, ℓ)                  │
                     │ Use · Verify · Modify · Escalate · Reject · Bypass     │
                     └───────────────┬──────────────────────────────────────┘
                                     ▼
       Ledger: value v, loss l, operating cost c, time λt, implementation C^impl,
       shared F_c (once), governance ΔC^gov → enterprise value F_E (TWD/period)
       Hard constraints: Legal, incident tolerance ē (not monetized)
                                     ▼
       Comparisons: VRA, DL0, VCP, VSC, DL, NEV, VG (EE/RE/CE), F_c^†, PR_X, VRG
       Robustness: ROBUST / CONDITIONAL / FRAGILE / UNIDENTIFIED
                                     ┊
       M5 (dynamic, G11, G12): outcomes_t → allocation_t+1; pilots → narrower Θ
```

此架構有三個要點。第一，G01–G16 透過四個介面進入模型，但**任何 gap 的網絡統計都不進入模型參數**；gap 只決定「哪些企業決策元素必須存在於模型中」。第二，共享能力與資源架構（F5）不是由 gap 推導，而是企業層級導入的結構性特徵；它是本研究與單一 use case 研究的根本差異。第三，跨層衝突、治理的價值與共享能力的價值都不是假設，而是模型可計算、資料可檢驗的量；模型也允許「企業與事業單位高度一致、多層衝突很弱」這一結果。


---

# 參、研究方法

本章的目標是：讀者讀完本章即可依公式實作求解器。完整規格與證明見 `42_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md`；本章方程編號與其一致。

## 3.1 研究設計

本研究採**嵌入式企業個案設計結合規範性決策模型**。企業為主要分析單位；事業單位／功能、AI initiatives 與共享能力為嵌入單位；角色別使用者提供反應與控制的證據。研究分三個部分：

1. **理論收斂**（已完成 candidate freeze）：將 G01–G16 收斂為企業決策介面與最小構念架構（3.4 節）。
2. **模型建構與實作驗證**（已完成 candidate；synthetic 驗證部分完成）：建立 Enterprise–Business Unit 雙層 portfolio 模型、識別規格與求解器（3.5–3.12 節）。
3. **企業實證校準**（待完成）：依 43 號識別規格取得參數或區間，求解並分類穩健性（3.13 節 V0–V7）。

研究不要求任何特定功能單位作為核心案例。任何單一 application、流程或部門只作為嵌入的實作實例；嵌入單位的選擇目的在於取得異質的治理、流程、授權深度、後果類別與價值結構，以檢驗企業架構能否跨單位成立。

## 3.2 分析層級

| 層級 | 分析單位 | 決策或反應 | 模型角色 |
|---|---|---|---|
| L1 Enterprise | 企業 | 共享能力 `y`、治理方案 `γ`、資源 envelope `e` | Leader |
| L2 Business Unit / Function | 事業單位 `u` | 各 initiative 的配置 `q_jk`、本地自建 `y^loc_uc` | Follower |
| L3 Initiative / Shared Capability | initiative `j`、能力 `c` | 無獨立決策；承載配置空間、成本、前提與結果查表 | 資料結構 |
| L4 Role-specific Users | 角色群 `ℓ` | 反應 `r` | 條件分布 `ρ`（預設）；第三層僅在 3.9 節條件下 |

Initiative 與共享能力分表保存，避免把平台能力誤記為單一部門的觀察。

## 3.3 構念操作化

構念依 41 號文件凍結為五族。序位構念的錨點沿用既有候選錨點（41 §5；待 V1 內容效度）：

| 族 | 構念 | 型別 | 錨點（0／1／2／3） | 模型中的唯一用途 |
|---|---|---|---|---|
| F1 | `G_j(γ)` 正式決策權 | ordinal | 無指定權責人／指定責任人／書面批准否決權／明示授權變更權 | `G_j(γ) ≥ G^req(A,κ)` |
| F1 | `H_k` 人工介入權 | ordinal | 無／結果後異議／行動前否決／執行中止或回復 | `H_k ≥ H^req_γ(A,κ)`；查表鍵 |
| F1 | `Eff_H(j,k)` 有效控制 | binary | 行動前可見資訊、足夠時間、真實否決皆成立 | (F6) |
| F1 | `κ_j` 後果類別 | ordinal class | 可逆局部／需跨部門修復／重大客戶、品質或法規後果 | 查表鍵 |
| F1 | `ē_j^γ` 嚴重事件容忍上限 | incidents/period | — | (F9) |
| F2 | `WI_k` 流程整合 | ordinal | 不入流程／人工轉入／系統送至決策節點／系統送至授權行動節點 | `WI_k ≥ WI^req_γ(A,κ)`；查表鍵 |
| F2 | `FB_jk` fallback／rollback | binary | — | (F7) |
| F3 | `A_k` AI 授權深度 | ordinal | 人獨立決定／AI 僅提供資訊／AI 提案人批准／AI 在授權邊界內最後決定 | 要求表索引；`Cons(A,m)` |
| F3 | `m_k` 配置型態 | nominal | HumanOnly、AI→Human、Human→AI、Aggregation、Delegated、BoundedExecution | 索引 |
| F3 | `ρ, P, π` | probability | — | (X1) |
| F4 | `EA_k`（EA-V）評估保證 | ordinal | 無驗證紀錄／上線前測試／運作中性能量測／觸發式重驗證 | `EA_k ≥ EA^req_γ(A,κ)`；查表鍵 |
| F4 | `EAX_k` 解釋可用性（條件） | ordinal | 無可用理由／可閱讀／可形成可檢驗查核問題／可在盲題中辨識理由不足 | 僅 `ρ` 分組鍵 |
| F5 | `y_c` 共享能力 | binary | — | Leader 決策 |
| F5 | `R_j(y)`, `D(y)` 資料可得性、共用介面 | ordinal | 41 §5 錨點 | `≥` 門檻 |

**尺度規則。** 序位值只在同構念 `≥` 比較、查表索引與可行性旗標中出現；任何序位值不得進入加、減、乘、除、加權總分或分母。對任一序位構念施加嚴格遞增重標，可行集合與最適解不變（命題 P5）。

**方向性 gap。** 對同一構念 `X`：`Gap_X(j,k,s) = 1[X_obs(j) < X^req_γ(A_k, κ_j)]`，只表示可行性被觸發，不表示損失幅度；`A_k = A_obs` 為現況檢查，`A_k = A^*` 為條件性反事實。缺值時 gap 為 UNIDENTIFIED。

## 3.4 Gap-to-Mechanism 轉譯

每一 gap 依序回答：(S1) 文獻低連結代表哪一個「AI 輸出 → 組織行動」的連接；(S2) 企業中誰在哪一層、對什麼做決定時會碰到這個連接；(S3) 企業中可觀察的狀態為何；(S4) 它成為決策變數、可行性限制、期望結果查表、成本項，或不進模型。收斂結果（研究者裁決；待 V1 雙人盲編）：

| 企業介面 | 機制 | Gaps | 模型元素 |
|---|---|---|---|
| I1 Authority-to-act | M1 | G09（L1）、G02、G08、G16 | `γ`、`Allow_γ`、`G_j(γ)`、`H ≥ H^req`、`Eff_H`、`ē`、`ΔC^gov` |
| I2 Routing & recovery | M2 | G03、G14 | `WI ≥ WI^req`、`FB`、`C^impl`、工程容量 |
| I3 Configuration & response | M3 | G01、G07 | `m`、`A`、`Cons(A,m)`、`ρ, P, π` |
| I4 Assurance | M4 | G06、G05（L1）、G13、G15（EA-X 條件） | `EA ≥ EA^req`、`y_EVAL`、`EAX` 作 `ρ` 鍵 |
| I5 Learning & reallocation | M5（動態） | G11、G12 | 跨期轉移；靜態僅 value-of-identification 診斷 |
| Optional | M3／M4 | G10 | 有真實分數與標記時，以離散門檻變體進 `M_j` |
| Evidence-only | — | G04 | 不建模 |

**V1 AI pilot 的爭議格（v2.2）。** 兩個 AI 盲編者（同一模型家族、互相隔離）在 16 格中與研究者裁決的主機制一致 14 格、狀態一致 13 格；分歧集中在三格：G04（AI：M4／static；研究者：evidence-only）、G11（AI：M4／static，M5 為次要；研究者：M5／dynamic）、G10（AI：static；研究者：optional）。依預先登記的 mapping-sensitivity 規則（53B §11），三者皆為 **mapping-only**：42 的方程不依賴這三格採用哪一種編碼，只有 4.1 節的計數與收斂敘述會改變。在人類盲編完成前，三格均標示為「研究者裁決、具爭議」；若人類編碼與 AI pilot 一致，M5 將只由 G12 支持，G04 的證據層計數由 1 變 0，G10 的「optional」改述為識別條件而非機制差異（54C §5）。

Strategic Alignment 與 Change／Absorptive Capability 不新增為構念：前者以 policy 強制／禁止集合 `J^must_γ, J^forbid_γ` 與可貨幣化的策略價值 `v` 表達；後者以共享變革能力 `y_CHG`（靜態）與 M5（累積）表達。

若 V1 盲編否決某一對應，該 gap 改掛裁決後的機制；若否決整個機制，該機制在討論中降為「研究者提出、未獲獨立支持的介面」，但其方程元素可因企業架構的理由保留——模型元素的存在理由與 gap 的支持分開陳述。

## 3.5 企業 AI Portfolio 模型：集合、參數與決策變數

**集合。** 事業單位 `u ∈ U`；initiatives `j ∈ J`，`u(j)` 為其擁有者，`J_u = {j : u(j) = u}`；共享能力 `c ∈ C`；initiative `j` 的候選配置 `k ∈ K_j = {0} ∪ M_j`，`k = 0` 為現況；policy profiles `γ ∈ Γ`（`γ^0` 為法規最低方案，`γ^cur` 為現行方案）；反應 `r ∈ R ∪ {NA}`，`R = {Use, Verify, Modify, Escalate, Reject, Bypass}`；角色 `ℓ ∈ Λ_j`；可見訊號 `z ∈ Z_j`；隱藏結果 `ω ∈ Ω_j`；池化資源 `h ∈ {BUD, ENG}`；部門自有資源 `REV`；情境組 `g ∈ 𝒢`。

每個配置 `k ∈ M_j` 為屬性組 `k ≡ (A_k, H_k, WI_k, EA_k, EAX_k, m_k)`。

**主要參數與單位**（完整識別規格見 43 號文件）：

| 類別 | 參數 | 單位 |
|---|---|---|
| 企業資源 | `Ā^BUD = B̄`、`Ā^ENG` | TWD/period；hours/period |
| 共享能力 | `F_c`、`a^ENG_c`、`Pre(j,k)`、`R_j(ȳ)`、`D(ȳ)` | TWD/period；hours/period；relation；ordinal |
| 本地自建 | `F^loc_uc`、`a^{ENG,loc}_uc` | TWD/period；hours/period |
| 治理 | `Allow_γ`、`Allow^loc_γ`、`G_j(γ)`、要求表、`ē_j^γ`、`J^must_γ`、`J^forbid_γ`、`ΔC^gov(γ)`、`Legal_jk` | binary；ordinal；incidents/period；set；TWD/period |
| Initiative | `κ_j`、`N_jk`、`Eff_H`、`FB`、`Cons`、`C^impl_jk(s)`、`a^ENG_jk(s)`（`s` 為能力來源狀態：無／共享／本地）、`C^{impl,x}_jk`、`τ_jc` | ordinal；events/period；binary；TWD/period；hours/period |
| 反應與結果 | `π_j(ℓ\|k)`、`P_j(z,ω\|k)`、`ρ_j(r\|k,z,ℓ,ȳ)`、`v`、`l`、`c`（各拆部門／帳本外）、`t`、`t^REV`、`λ_ℓ`、`I^sev` | probability；TWD/event；hours/event；TWD/hour |

一次性成本以年金因子期間化：`C^impl_jk = O_jk · AF(r_d, H_j) + Rec_jk`，`AF(r_d, H) = r_d / (1 − (1 + r_d)^{−H})`。

**決策變數。** 企業：`y ∈ {0,1}^{|C|}`、`γ ∈ Γ`、`e = (e^h_u)`。事業單位 `u`：`q_jk ∈ {0,1}`（`j ∈ J_u`）、`y^loc_uc ∈ {0,1}`（僅 `Allow^loc_γ(u,c) = 1` 時可為 1）。令 `ȳ_jc = max(y_c, y^loc_{u(j)c})` 為 initiative `j` 可用的能力狀態。

## 3.6 可行集合與限制

對每個 `(j,k)` 計算布林可行旗標 `Φ_jk = ∏ Φ^{(F2..F9)}_jk`，並要求 `q_jk ≤ Φ_jk`：

| 編號 | 限制 | 形式 |
|---|---|---|
| (F1) | 每個 initiative 恰選一個配置 | $\sum_{k\in K_j} q_{jk}=1$ |
| (F2) | 法規、權利、隱私、安全 | $Legal_{jk}=1$ |
| (F3) | policy 允許 | $Allow_\gamma(j,k)=1$；$j\in J^{forbid}_\gamma \Rightarrow k=0$ |
| (F4) | 能力前提 | $\bar y_{jc}=1\ \ \forall c\in Pre(j,k)$ |
| (F5a–e) | 同構念要求 | $H_k\ge H^{req}_\gamma(A_k,\kappa_j)$；$WI_k\ge WI^{req}_\gamma(\cdot)$；$G_j(\gamma)\ge G^{req}(\cdot)$；$EA_k\ge EA^{req}_\gamma(\cdot)$；$R_j(\bar y)\ge R^{req}(A_k)$、$D(\bar y)\ge D^{req}(A_k)$ |
| (F6) | 有效控制 | $H^{req}_\gamma(A_k,\kappa_j)\ge 2 \Rightarrow Eff_H(j,k)=1$ |
| (F7) | fallback／rollback | $A_k\ge 2 \Rightarrow FB_{jk}=1$ |
| (F8) | 授權—配置一致 | $Cons(A_k,m_k)=1$ |
| (F9) | 嚴重事件硬上限 | $N_{jk}\,\mathbb E_{jk}[I^{sev}]\le \bar e^\gamma_j$ |
| (F10) | 策略強制 | $j\in J^{must}_\gamma \Rightarrow \sum_{k\neq 0} q_{jk}=1$ |

(F2)–(F9) 對所有配置（含現況 `k = 0`）一律適用：新 policy 可能使現況配置不可行，此時該 initiative 必須改選其他可行配置，故每個 `K_j` 應包含不依賴新能力的 fallback 配置。某 `(y, γ)` 下若有 initiative 無任何可行配置，該 `(y, γ)` 不可行並列入報告；現況違反 (F2) 或 (F9) 另輸出 `STATUS_QUO_NONCOMPLIANT`（作為結果，不中止求解）。

**資源限制。** 配置的池化資源使用為 `a^BUD_jk = C^impl_jk(s) + (N_jk E_jk[c] − N_j0 E_j0[c])`（導入成本加增量每事件營運支出，可為負）、`a^ENG_jk(s)`；審查工時增量 `a^REV_jk = N_jk E_jk[t^REV] − N_j0 E_j0[t^REV]`。

集中形式：

$$
\sum_c a^h_c y_c + \sum_{u,c} a^{h,loc}_{uc} y^{loc}_{uc} + \sum_{j,k} q_{jk} a^h_{jk} + \mathbb 1[h=BUD]\,\Delta C^{gov}(\gamma) \le \bar A^h \tag{R1}
$$

雙層形式：企業 $\sum_c a^h_c y_c + \sum_u e^h_u + \mathbb 1[h=BUD]\Delta C^{gov}(\gamma) \le \bar A^h$；部門 $\sum_c a^{h,loc}_{uc} y^{loc}_{uc} + \sum_{j\in J_u,k} q_{jk} a^h_{jk} \le e^h_u$。（R1′）

部門自有審查容量：$\sum_{j\in J_u,k} q_{jk}\,a^{REV}_{jk} \le \Delta\bar K^{REV}_u$。（R2）

## 3.7 企業目標

**期望算子。** 對任一路徑函數 `f`：

$$
\mathbb E_{jk}[f] = \sum_{\ell}\pi_j(\ell\mid k)\sum_{z,\omega}P_j(z,\omega\mid k)\sum_{r}\rho_j(r\mid k,z,\ell,\bar y)\,f_j(k,\ell,z,\omega,r) \tag{X1}
$$

隱藏結果 `ω` 不在 `ρ` 的條件中。(X1) 對 `π`、`P`、每一列 `ρ` 與 `f` 各為線性（block-multilinear）。

**路徑淨貢獻與帳本。**

$$
f_j = v_j - l_j - c_j - \lambda_\ell\, t_j \tag{V1}
$$

每一經濟後果只能落在一個項目：人工時間的增減只在 `−λt` 與容量限制；錯誤減少只在損失 `l`；營收與機會價值只在 `v`；推論與外部服務只在 `c`；整合、在地訓練、監控、維護與 rollback 準備只在 `C^impl`；共享平台、模型服務、資料層、資安、評估平台與共用訓練只在 `F_c`；重用效果只透過 `C^impl(ȳ)` 隨能力狀態的差異；chargeback 只在部門帳本；法規與安全底線只在硬限制；選擇權價值不進靜態目標。

**Initiative 增量貢獻與企業目標。**

$$
\varphi_{jk} = N_{jk}\,\mathbb E_{jk}[f\mid\bar y] - N_{j0}\,\mathbb E_{j0}[f\mid\bar y^{cur}] - C^{impl}_{jk}(s),\qquad C^{impl}_{j0}\equiv 0 \tag{V2}
$$

$$
F_E = \sum_{j,k} q_{jk}\,\varphi_{jk} - \sum_c F_c\,(y_c - y^{cur}_c) - \sum_{u,c} F^{loc}_{uc}\,y^{loc}_{uc} - \Delta C^{gov}(\gamma) \tag{OBJ-E}
$$

`F_E` 的單位為 TWD/period，意義為相對於現況 portfolio（現況配置在現況能力狀態 `ȳ^cur` 下）的企業增量價值：保留既有能力的增量成本為 0，停用既有能力節省 `F_c`；資源限制仍以絕對值計。若時間價值 `λ_ℓ` 未識別，不以 0 代入，而改報兩分量 `(F_E^{−time}, ΔHours)` 並以 `λ_ℓ ∈ [0, λ^U_ℓ]` 進行穩健性分類。

## 3.8 事業單位反應模型

事業單位的目標由其**被考核的帳本**界定，而非研究者設定的偏好權重。將 `v, l, c` 拆為記入部門帳本的部分（上標 `u`）與帳本外的部分（上標 `x`），則

$$
\varphi^u_{jk} = N_{jk}\,\mathbb E_{jk}[f^u] - N_{j0}\,\mathbb E_{j0}[f^u] - \big(C^{impl}_{jk} - C^{impl,x}_{jk}\big) - \sum_{c\in Pre(j,k)}\tau_{jc}\,y_c(1-y^{loc}_{u(j)c})
$$

$$
F_u = \sum_{j\in J_u,k} q_{jk}\,\varphi^u_{jk} - \sum_c F^{loc}_{uc}\,y^{loc}_{uc} \tag{OBJ-U}
$$

其中 $f^u = v^u - l^u - c^u - \lambda^u_\ell t$。部門專屬的服務下限 `E_jk[s_j] ≥ s^min_j` 或問責上限 `N_jk E_jk[I^sev] ≤ ē^u_j` 只在有文件或行為證據時加入。

**帳本對齊條件。** (AL1) 無帳本外項：`v^x = l^x = c^x = 0` 且 `C^{impl,x} = 0`；(AL2) 無 chargeback；(AL3) 無部門專屬限制，或其亦在企業問題中；(AL4) `λ^u = λ`。四者皆成立時 `φ^u_jk = φ_jk`。

既有規格中部門只最小化損失與成本的目標（不計價值），是 (OBJ-U) 在 `v^u = 0` 時的特例；它只在帳本證據顯示部門不以價值考核時才適用，否則會在模型中製造部門必然偏向現況的假衝突。

## 3.9 使用者反應分布

使用者層預設不是最佳化者，而以三種反應分布表示：已部署配置的實際反應 `ρ^obs`（系統紀錄或抽樣觀察，OBSERVED）；未部署配置的反應 `ρ^cf`（以只呈現可見訊號、遮蔽真值的題卡引出區間，EXPERT_ELICITED）；以及程序文件所設計的反應 `ρ^design`（退化分布，OBSERVED）。反應集合含拒用與繞過；policy 禁止的反應機率為 0。

只有下列五項**全部**成立時，才以角色效用 `U_ℓ` 的最佳反應取代 `ρ`，建立第三層（Model D）：(T1) 使用者可在無事前核准下選擇反應；(T2) 至少兩個具不同後果的可行反應；(T3) 使用者有不同於部門的目標或限制；(T4) 部門在選擇配置時預期使用者反應；(T5) 以結構化反應取代 `ρ` 會在可接受參數範圍內改變上游最適配置。未通過時不執行第三層。

## 3.10 共享能力耦合與組織型態比較

**耦合。** 共享能力透過五個管道耦合各 initiative：(1) 固定成本 `F_c y_c` 只在企業層計一次；(2) 能力前提 (F4)；(3) 池化工程容量 (R1)；(4) 同一 `γ` 對所有部門設定允許集合、要求與容忍上限；(5) 重用效果——局部導入成本是以**能力來源**（無／共享／本地）為索引的查表 `C^impl_jk(s_{Rel(j)})`，共享重用效果定義為 `δ_jkc = C^impl_jk(s_c = ∅) − C^impl_jk(s_c = S)`；本地版另以其自身格表示。以來源為索引，是因為本地版與共享版的成本與品質可能不同，且若 `δ` 同時作用於本地版，共享能力的投資門檻會失去唯一性。沒有證據時不假設 `δ > 0`。啟動順序屬 M5。

**組織型態。** 所有比較在同一參數 `θ` 與同一 policy 方案下進行：

| 型態 | 決策者 | 目標 | 能力 | 資源 |
|---|---|---|---|---|
| A 各部門獨立 | 各部門 | (OBJ-U) | 僅本地自建 | 固定現況預算 `B^0_u, K^{ENG,0}_u` |
| C0 雙層、不共享 | 企業 `(γ,e)`；部門 `(q,y^loc)` | (OBJ-E)；(OBJ-U) | 僅本地版 | envelope |
| A+ 集中、不共享 | 企業 | (OBJ-E) | 僅本地版 | 池化 |
| B 集中規劃 | 企業 | (OBJ-E) | 共享與本地 | 池化 |
| C 企業—事業單位雙層 | 企業 `(y,γ,e)`；部門 `(q,y^loc)` | (OBJ-E)；(OBJ-U) | 共享＋（允許時）本地 | envelope |
| D 三層（條件） | C ＋ 使用者 | 同 C ＋ `U_ℓ` | 同 C | 同 C |

**比較量。**

$$
VRA = F_E^{C0} - F_E^{A},\quad DL0 = F_E^{A+} - F_E^{C0},\quad VCP = F_E^{A+} - F_E^{A} = VRA + DL0,\\ VSC = F_E^{B} - F_E^{A+},\quad DL = F_E^{B} - F_E^{C},\quad NEV = F_E^{C} - F_E^{A} = VCP + VSC - DL
$$

VRA 為不共享能力、部門仍自主時，企業重新分配 envelope 的價值；DL0 為不共享能力時部門帳本不對齊造成的損失；VCP 為兩者之和，即不共享能力時集中規劃的總價值（**不是**純重分配價值）；VSC 為在集中規劃下允許共享能力的價值；DL（delegation loss）為把配置選擇交給事業單位造成的企業價值損失，報樂觀與悲觀兩界；NEV 為「企業協調架構＋事業單位自主」相對於「各部門自行導入」的淨價值。

**命題**（證明見 42 §15）：

- **P1** 在 A 的現況資源加上治理成本不超過池化總量、且 A 所用 `γ` 在其他型態中可選時，對樂觀與悲觀兩界皆有 $F_E^{A} \le F_E^{C0} \le F_E^{A+} \le F_E^{B}$ 與 $F_E^{C0} \le F_E^{C} \le F_E^{B}$。故 VRA、DL0、VCP、VSC、DL 皆非負，NEV 的符號不由模型決定。
- **P2** 若 (AL1)–(AL4) 成立且池化資源以 envelope 分配，則 $F_E^{C,opt} = F_E^{C,pess} = F_E^{B}$，即 DL = 0。不對齊是 DL > 0 的必要而非充分條件：若不利企業的配置需要池化資源，企業可以 envelope 阻止。
- **P3** 本模型為完全資訊模型，故模型內 $F_E^B \ge F_E^C$ 恆成立；模型不能顯示分權的資訊優勢。
- **P4** 對每項共享能力，定義 `F_c^† = sup{F : G_1(F) − F ≥ G_0}`，則 `y_c^* = 1 ⇔ F_c ≤ F_c^†`；預算不綁時 `F_c^† = G_1 − G_0`（強制建置且不計 `F_c` 的最適值減去強制不建置的最適值）。在 B 中，以來源為索引的共享重用效果亦有唯一門檻 `δ^†`；在 C 中只有帳本對齊時才保證。v2.2 的合成反例顯示，帳本不對齊時，C 的建置決策可隨 `δ` 由建置轉為不建置再轉回建置（序列 1,1,1,1,0,0,0,1），故 C 中只報告集合值的建置區域，不宣稱唯一的 `δ^†`。`F_c^†` 在 C 中仍為單調門檻，因 `F_c` 不進部門帳本。
- **P5** 序位重標不變；**P6** 金額尺度不變，且所有每期參數同乘一常數時不變（這不等於改變期間長度，因年金因子非線性）。
- **P7** 在集中規劃（B）中，放寬任一要求只會擴大可行集合，故在固定參數下要求代價 `PR_X ≥ 0`；在雙層（C）中只有帳本對齊時才保證。
- **P8** 在雙層且帳本不對齊時，收緊要求可能嚴格提高企業價值：要求可篩除部門偏好、對企業不利、且無法以 envelope 阻擋的配置。

**治理價值分解。** 以法規最低方案 `γ^0` 為基準：

$$
VG(\gamma) = \underbrace{F^*(Allow_\gamma, Req_{\gamma^0}, C_{\gamma^0}) - F^*(\gamma^0)}_{EE\ \text{賦能}} + \underbrace{F^*(Allow_\gamma, Req_\gamma, C_{\gamma^0}) - F^*(Allow_\gamma, Req_{\gamma^0}, C_{\gamma^0})}_{RE\ \text{要求}\ \le 0} + \underbrace{F^*(\gamma) - F^*(Allow_\gamma, Req_\gamma, C_{\gamma^0})}_{CE\ \text{營運成本}}
$$

賦能區塊包含 `Allow_γ`、`Allow^loc_γ`、正式決策權 `G_j(γ)`（為 permission level，數值越高越寬鬆）與策略強制／禁止集合；要求區塊包含 `H^req, WI^req, EA^req, G^req, ē`。在 B 中，由 P7 得 `RE ≤ 0`：治理要求本身不會增加已被定價的價值。治理在模型內的正價值因此只有三個管道：**賦能**（使原本不被允許的較高授權配置成為可行）、**穩健可行**（使 portfolio 在整個不確定集合上仍滿足硬限制，3.12 節），以及僅在雙層且帳本不對齊時出現的**篩選**（P8：以規則替代無法以預算達成的協調）。

## 3.11 求解程序

下層為整數選擇；KKT 條件對整數下層不是最適性的充分必要條件，故不採 KKT／MPEC 單層重構。在已識別規模下採精確的有限列舉；規模更大時可採混合整數雙層方法（Moore & Bard, 1990；Kleinert et al., 2021），並報告所用近似。

**Lemma E′（envelope 有限化，v2.2）。** 企業只需提供每個部門「等於其某個可行計畫資源向量」的 envelope：$E'_u = \{a(x_u) : x_u \in \mathcal P_u\}$。理由：對任一 envelope，取部門最適集合中的一個計畫 `x`，把 envelope 縮為 `a(x)`；新的可負擔集合包含 `x` 且是原集合的子集合，故 `x` 仍為部門最適，最適集合只會縮小——樂觀值不變（取 `x` 為樂觀最佳者），悲觀值不減，而資源使用不增（42 §12.4）。此集合不大於計畫數，小於 v2.1 的乘積集合（至多計畫數平方）；兩者在合成實例上給出相同的樂觀與悲觀值。

**演算法（Model C）。**

```
for each shared-capability set y ⊆ C and policy γ ∈ Γ:
    remaining ← Ā − shared use(y) − ΔC^gov(γ)          # skip if negative
    for each unit u:
        P_u ← all feasible plans (q_u, y^loc_u) under (y, γ)   # Φ_jk, (R2), (F10)
        for each envelope e ∈ E'_u (Lemma E′):
            X*_u(e) ← argmax_{x ∈ P_u, a(x) ≤ e} F_u(x)   (tolerance ε_tie)
            φ^opt_u(e) ← max_{x ∈ X*_u(e)} enterprise contribution(x)
            φ^pess_u(e) ← min_{x ∈ X*_u(e)} enterprise contribution(x)
        drop envelopes dominated in (resource ≥, value ≤)
    for mode in {opt, pess}:
        solve multiple-choice knapsack: max Σ_u φ^mode_u(e_u) s.t. Σ_u e_u ≤ remaining
        F^{C,mode}(y, γ) ← knapsack value − Σ_c F_c y_c − ΔC^gov(γ)
return max over (y, γ) for each mode
```

Model B 與 A+ 以相同結構求解，但部門計畫以企業貢獻選擇；A+ 固定 `y = 0`。C0 即上述演算法固定 `y = 0`。Model A 以固定現況 envelope、`y = 0` 與 (OBJ-U) 求解，再以 (OBJ-E) 評估。

**前處理與缺值。** 求解前執行 schema 與單位檢查（typed units、NaN／inf、`ω` 不得出現在 `ρ` 的條件鍵）；對每個 `(j, k)` 與能力來源狀態檢查所需查表格，資料／介面門檻 (F5e) 在實際選定的能力狀態下求值（含現況配置）。缺值處理：現況在目前能力狀態下的非局部查表缺 → `UNEVALUABLE_INITIATIVE`；某配置（或某配置在某一能力狀態）的查表、`Allow` 或 (F5e) 狀態查表缺 → 只移除該配置並輸出 `RESTRICTED_SOLVE`；`F_c` 缺 → 只在有共享能力的 B、C 進入 `THRESHOLD_MODE`（C 同時報樂觀與悲觀門檻）；`λ` 缺 → `PARTIAL_OBJECTIVE`，報不含任何時間項的 `F_E^{−time}` 與依角色的工時變化，並在預先界定的 `[0, λ^U]` 盒上檢查決策是否不變——集中規劃（B、A+）可在盒的頂點上精確判定，雙層只能以網格檢查，故不輸出點決策；帳本拆分缺 → Model C 不解（`FOLLOWER_LEDGER_UNIDENTIFIED`）；總資源缺 → 拒算。求解器對任何格式錯誤一律回傳狀態，不以例外中止。**任何情況均不以 0、平均值、歷史合成係數或外部效果量補值。**

**複雜度。** 約為 `|Γ| · 2^{|C|} · Σ_u |P_u| · |E_u|` 次部門評估加多選擇背包；在 `|C| ≤ 8`、`|Γ| ≤ 4`、`|U| ≤ 8`、每部門 ≤ 4 initiatives × ≤ 6 配置的規模下可精確求解；更大規模以量子 `β` 的動態規劃求解：權重無條件進位得可行下界、無條件捨去得鬆弛上界，報告兩者之差作為誤差界；進位版無解而鬆弛版有解時退回完整列舉，從不把量化造成的不可行當成真實不可行。

## 3.12 不確定性與敏感度

**可接受參數集合。** `Θ_adm = ∪_{g∈𝒢} Θ_g`，每個 `Θ_g` 由貨幣與數量參數的區間積、各機率列的「單純形 ∩ 區間盒」多面體，以及預先登記的相依限制構成。情境組 `𝒢` 在看到求解結果前登記，並以 SHA-256 承諾（registry 全文與每個被縮放之參數的名目值，浮點數不做四捨五入）寫入結果；事後改動區間或名目值都可被偵測。每個參數區塊只能作用於同一類乘數因子、且區塊之間不得重疊——這是下述所有頂點論證所需之 block-multilinear 結構的可檢查版本。

**決策元素層級分類。** 對決策元素 `d`（某 `y_c`、某 initiative 的配置、某 envelope、`γ` 或整個 portfolio）：

| 類別 | 定義 |
|---|---|
| ROBUST | 存在單一值在所有 `θ ∈ Θ_adm` 下皆屬最適集合 |
| CONDITIONAL | 非 ROBUST，但在每一情境組內各有單一值恆屬最適 |
| FRAGILE | 某一情境組內沒有恆屬最適的單一值 |
| UNIDENTIFIED | 影響 `d` 的必要參數無可接受界，或缺值排除了可能最適的配置 |

另報最大 regret $\max_\theta [F^*(\theta) - F(d,\theta)]$ 與預先登記容差 `ε_R` 下的 ε-ROBUST。在 B 中、對固定候選集合，regret 是 multilinear 函數的最大值減去 multilinear 函數，其最大值在頂點達成，故 MaxRegret 可精確計算。

**Lemma R（精確檢查，僅限 Model B 的整個 portfolio）。** 兩個固定 portfolio 的價值差在 (X1) 各參數區塊上 block-multilinear；若 `Θ_g` 為各區塊多面體之乘積，其最小值在乘積的某頂點達成，貨幣區塊可直接依係數符號取端點。因此在 B 中，「整個 portfolio 在 `Θ_g` 內恆為最適」可精確判定。此結論**不能**直接用於單一決策元素：含某元素值的最佳 portfolio 會隨 `θ` 改變，其最大值的最小值不保證在頂點（例：兩個含 `y_c = 1` 的 portfolio 價值為 `θ` 與 `1 − θ`、不含者為 0.6，兩頂點上 `y_c = 1` 皆最適，`θ = 0.5` 時則否）。元素層級因此以「存在單一 robust portfolio 含該值」為充分條件，否則以列舉或抽樣判定；Model C 的 leader 價值經由隨 `θ` 改變的部門最佳回應決定，亦一律以列舉或抽樣判定。為使候選集合不隨 `θ` 改變，候選 portfolio 先依與 `θ` 無關的條件列舉（不以名目參數下的預算、容量或 (F9) 先行篩選，因名目點不必在登記集合內），再分為四類：`ROBUSTLY_FEASIBLE`（每個限制在每個頂點成立，為證書）、`INFEASIBLE`（某一限制在每個頂點皆不成立，為證書）、`CONDITIONALLY_FEASIBLE`（找到一個使所有限制同時成立的 `θ`，並回報該見證點）、`FEASIBILITY_UNDETERMINED`（以上皆非）。只有第一類進入分類用的候選集合。元素層級與 Model C 的分類以頂點、網格與隨機樣本上的完整最適集合判定，報告涵蓋點數，不得宣稱「對所有 θ」。

**要求的保護功能。** 對每項綁住的要求 `X`，若放寬後的最適解在 `Θ_g` 中某些 `θ` 違反 (F9)，該要求為 **robustness-protective**；若放寬後仍 robustly feasible 且 `PR_X > 0`，則為「模型內無保護功能的要求」——這是官僚成本的候選，但不是定論，因為要求可能防範模型未涵蓋的風險。在雙層中若放寬反而降低企業價值（`PR_X < 0`），該要求承擔了**篩選**功能。

**設計反應的可行性。** (F9) 與 (R2) 依賴 `ρ`；以設計反應選出的 portfolio 在實際反應下可能違反硬限制或容量，此時 VRG 與 design-response regret 不定義，輸出 `DESIGN_INFEASIBLE_UNDER_RESPONSE`——這本身是重要結果。

**Value-of-identification 診斷。** $VOI_p = MMR(\Theta_g) - \sup_v MMR(\Theta_g \mid \theta_p = v)$，用以排序最值得優先量測的參數。`sup` 只取區塊頂點時可能高估（解析例：頂點版為 1、真值為 0.5），故同時報告只取頂點與加入內點網格的兩個版本；兩者皆為真值的上界，網格版不大於頂點版。此診斷只決定資料蒐集優先序，不進目標（G12 的靜態影子）。

**不得挑選最有利的情境作為結論。** 外部效果量只可作區間端點，並附任務相似性說明。

## 3.13 驗證流程 V0–V7

| Gate | 內容 | 通過證據 | 不通過的輸出 | 目前狀態 |
|---|---|---|---|---|
| V0 Source & Authority | 權限、共享資源、initiative 邊界、授權範圍 | 文件與角色交叉核對 | 保留為情境，不稱企業現況 | OPEN |
| V1 Construct Validity | G→M 雙人盲編；錨點內容效度 | 預先登記判準（53B §9）：Krippendorff's α（名目；Krippendorff, 2004）與 Cohen's κ（Cohen, 1960）、5,000 次 bootstrap 區間；α ≥ .800 為 RELIABLE、.667 ≤ α < .800 為 TENTATIVE（預先登記的研究慣例門檻 `[VERIFY：門檻出處僅見二手來源]`）；至少兩位人類編碼者；EA-X 錨點以 I-CVI ≥ .78 為保留門檻（Polit, Beck, & Owen, 2007） | 依 3.4 節回退規則 | `V1_AI_PILOT_COMPLETE`；`V1_HUMAN_BLIND_CODING_PENDING` |
| V2 Cross-functional Pilot | 至少兩種功能脈絡試用 | 題卡理解、缺格、非單調、角色差異、負擔 | 修改錨點或改逐格查表 | OPEN |
| V3 Schema & Units | 型別、機率正規化、單位守恆 | 型別檢查與反例拒絕 | `INVALID_SCHEMA_OR_UNITS` | COMPLETE（僅合成） |
| V4 Lookup Completeness | 每個求解所需格有來源或區間 | 缺格拒算或狀態碼；無靜默補零 | `RESTRICTED_SOLVE` 等 | COMPLETE（僅合成） |
| V5 Portfolio Solver | oracle、集中 vs 雙層、ties、共享成本只計一次 | 獨立手算 oracle、DP 對列舉、命題檢查 | 修正實作 | COMPLETE（僅合成） |
| V6 Invariance & Sensitivity | 尺度、期間、序位與標籤重排不變；`Θ_adm` 分類 | 斷言與涵蓋率報告 | 報 UNIDENTIFIED 或涵蓋率 | COMPLETE（僅合成；元素層級與 C 的分類只以涵蓋率報告） |
| V7 Enterprise Empirical Calibration | 政策、配置、反應與結果交叉核對 | 跨來源一致 | 僅條件性情境支援 | OPEN |

「COMPLETE（僅合成）」表示該 gate 的工程檢查已在合成實例上完成，不是企業層級的通過。v2.3 起，V1（人類盲編）、EA-X 內容效度與企業資料各有固定的匯入與計算程式（`60`、`61`、`65`；資料契約 `62`、最小 pilot `63`、量測優先序 `64`），第肆章各表直接由其輸出回填。在 V7 完成前，本研究只能宣稱研究架構、模型規格與合成實作的有效性；不能宣稱任何企業已達成特定 ROI、AI 已改善績效、某部門為最佳導入點，或結果可外推至其他企業。


---

# 肆、研究結果（可執行回填骨架，v2.3）

**本章規則：**

1. 本章每一張表都標明五項：**來源資料**（哪個檔案或樣板區塊）、**計算程式**（哪個指令）、**輸出變數**（結果檔中的欄位）、**判讀規則**、**待決條件**（何時才能填入）。未取得真實資料的格一律為 `[EMPIRICAL RESULT PENDING]`；V1 與 EA-X 的人類結果格為 `[HUMAN RESULT PENDING]`。
2. 數值只能由下列程式的輸出檔複製，不得手算或改寫：
   - `60_v1_human_validation_analyzer_v2_3.py` → `v1_human_results/`
   - `61_EAX_HUMAN_CVI_ANALYZER_v2_3.py` → `eax_cvi_results/`
   - `65_enterprise_data_loader_v2_3.py` → `enterprise_results/`（內部呼叫 51）
3. 4.5 節是唯一的 `SIMULATED_ONLY` 內容，任何合成數值不得移入 4.6–4.10。AI pilot（54C、56 §8）只可作為對照脈絡，不得填入人類結果欄。
4. 外部評估者（董事端、合作商、投資端）只出現在 4.9，且只改變區間或情境，不是決策層級。

---

## 4.1 G→M 人類盲編驗證（V1）

**表 4.1　G01–G16 收斂結果（研究者裁決；人類 V1 待完成）**

| 命運 | Gaps | 數量 |
|---|---|---|
| Static core／bridge → M1（I1 授權與問責） | G09（企業層）、G02、G08、G16 | 4 |
| Static core／bridge → M2（I2 路由與回復） | G03、G14 | 2 |
| Static core → M3（I3 人機配置與反應） | G01、G07 | 2 |
| Static core／bridge／conditional → M4（I4 評估保證） | G06、G05（企業層）、G13、G15 | 4 |
| Optional module | G10（爭議，見表 4.2d） | 1 |
| Dynamic extension M5 | G11（爭議）、G12 | 2 |
| Evidence-only | G04（爭議） | 1 |
| Excluded | — | 0 |

**表 4.2a　AI-BLIND-CODING PILOT（診斷用；不是人類盲編，不是 V1 通過；保留自 v2.2）**

| 指標 | 主機制 | 狀態 |
|---|---|---|
| AI A 對 AI B 一致 | 16／16（κ = α = 1.000） | 16／16（κ = α = 1.000） |
| 每位 AI 編碼者對研究者裁決一致 | 14／16 | 13／16 |
| 分歧格 | G04、G11 | G04、G11、G10 |

同一模型家族的兩個編碼者完全一致，這是預期中的結果，不提供人類信度的資訊。

**表 4.2b　人類編碼者間信度**

| 欄位 | 編碼者配對 | 一致數（/16） | Cohen's κ [95% CI] | Krippendorff's α [95% CI] | 53B 分類 |
|---|---|---|---|---|---|
| 主機制 | A vs B | `[HUMAN RESULT PENDING]` | `[HUMAN RESULT PENDING]` | `[HUMAN RESULT PENDING]` | `[HUMAN RESULT PENDING]` |
| 狀態 | A vs B | `[HUMAN RESULT PENDING]` | `[HUMAN RESULT PENDING]` | `[HUMAN RESULT PENDING]` | `[HUMAN RESULT PENDING]` |
| 次機制 Jaccard（平均） | — | `[HUMAN RESULT PENDING]` | | | |

- 來源資料：`v1_human_import/coders.csv`，以及凍結於 manifest stage 3 的人類 response sheets。
- 計算程式：`python 60_v1_human_validation_analyzer_v2_3.py --coders v1_human_import/coders.csv`。
- 輸出變數：`reliability.fields.{primary_code,status}.{alpha, alpha_ci95, c1_c3_class, pairs[].{agreements, kappa, kappa_ci95}}`、`secondary_jaccard_mean`。
- 判讀規則（53B C1–C3）：決策依 α——α ≥ .800 為 RELIABLE，.667 ≤ α < .800 為 TENTATIVE；α 的 CI 下界 < .667 為 IMPRECISE，須加編碼者。κ 與其區間並列報告；Landis & Koch 標籤不報告（57 v2.3）。
- 待決條件：至少兩位人類編碼者的已凍結 sheets。

**表 4.2c　分歧矩陣與裁決**

| 個案 | 編碼者 A | 編碼者 B | 分歧類型 | 最終碼 | 裁決路徑 |
|---|---|---|---|---|---|
| `[HUMAN RESULT PENDING]` | | | | | |

- 來源資料：同上，另加 `v1_human_import/adjudication.csv`（凍結於 manifest stage 4）。
- 計算程式：`60 … --adjudication …`。
- 輸出變數：`reliability.disagreements`、`reliability.fields.*.pairs[].disagreement_matrix`、`final_codes`。
- 判讀規則：分歧先由編碼者在不看答案鍵的情況下討論，再交由非 41 作者的裁決者；若由 41 作者裁決，列為研究限制（53B C5）。
- 待決條件：表 4.2b 已完成且裁決檔已凍結。

**表 4.2d　與研究者裁決比較、mapping sensitivity，以及 G04／G10／G11 追蹤**

| Gap | 最終碼 | 研究者答案鍵 | 主機制相同 | 狀態相同 | 暫定分類（60） | 確認分類 | AI pilot（僅脈絡） |
|---|---|---|---|---|---|---|---|
| G04 | `[HUMAN RESULT PENDING]` | EVIDENCE_ONLY／evidence-only | | | | | M4／static |
| G10 | `[HUMAN RESULT PENDING]` | M3／optional | | | | | M3／static |
| G11 | `[HUMAN RESULT PENDING]` | M5／dynamic | | | | | M4／static |
| 其餘 13 格 | `[HUMAN RESULT PENDING]` | 41 | | | | | |

- 來源資料：同上，另加 sealed key（雜湊須等於 53A 承諾 `d1702188…`）。
- 計算程式：`60 … --adjudication … --key <sealed_key.json>`；改變的個案另以凍結的 `classes.csv` 提供 53B §11 分類（`--classes`）。第一次開啟答案鍵時，裁決檔即被綁定，之後不得修改最終碼。
- 輸出變數：`key_comparison[]`、`mechanisms_without_primary_support`、`decision`。
- 判讀規則：
  - V1 判定依 53B C6：至少兩位人類編碼者、C1 ≥ TENTATIVE 且非 IMPRECISE、C3 ≥ TENTATIVE、沒有未解的 model-structural 變更，才得到 `V1_PASS_HUMAN_C6`。
  - 任何改變都要經 53B §11 確認分類。`model-structural` 一律先修改 42／44。
  - 若某機制失去所有主碼支持，依 41 §7 規則 2 下調 44 的主張。
- 待決條件：裁決已凍結。**目前狀態：`V1_HUMAN_BLIND_CODING_PENDING`。**

## 4.2 EA-X 內容效度

**表 4.3　EA-X 錨點 v2.2.1 的人類內容效度**

| 項目 | 評分者數 | I-CVI [Wilson 95%] | 修正 kappa k* | 清晰度 3–4 比例 | 歸入其他構念的旗標 | 上一級更嚴格（是／否／不確定） | 處置 |
|---|---|---|---|---|---|---|---|
| 定義 | `[HUMAN RESULT PENDING]` | | | | | — | |
| 等級 0 | `[HUMAN RESULT PENDING]` | | | | | | |
| 等級 1 | `[HUMAN RESULT PENDING]` | | | | | | |
| 等級 2 | `[HUMAN RESULT PENDING]` | | | | | | |
| 等級 3 | `[HUMAN RESULT PENDING]` | | | | | — | |
| S-CVI/Ave；S-CVI/UA；代表性 | `[HUMAN RESULT PENDING]` | | | | | | |
| 構念分類題（8 句）正確率 | `[HUMAN RESULT PENDING]` | | | | | | |

- 來源資料：`eax_cvi_import/{reviewers, ratings, set_ratings, sort}.csv`。評分者須為人類、簽署獨立聲明、使用錨點 v2.2.1，且所有檔案已凍結於 `eax_cvi_import/FREEZE_MANIFEST.txt`。
- 計算程式：`python 61_EAX_HUMAN_CVI_ANALYZER_v2_3.py --in eax_cvi_import`。
- 輸出變數：`items.{DEF,L0..L3}.{I_CVI, I_CVI_wilson95, modified_kappa, clarity_share_3_4, ambiguity_flags, next_level_more_demanding, decision}`、`S_CVI_Ave`、`S_CVI_UA`、`representativeness`、`confusion_sort`、`eax_status`。
- 判讀規則：
  - 至少 3 位評分者時，I-CVI ≥ .78 且至多一位評分者把該項歸到其他構念，才保留（Polit, Beck, & Owen, 2007；56 §6）。
  - 量表層級同時報告「普遍一致」與「平均」兩種 S-CVI，並說明採用哪一種（Polit & Beck, 2006）。
  - 即使五項全部保留，EA-X 仍是 `CONDITIONAL_CANDIDATE`，直到 V2 兩輪 pilot 確認各等級可區分；等級 3 的累積性未確認前，不使用序位假設。
- 待決條件：預計 6–8 位人類評分者（研究慣例），至少 3 位。**目前狀態：`CONDITIONAL_CANDIDATE`**。AI 評分 pilot（56 §8）只用來修訂措辭，不是 CVI。

其他構念（`G, H, WI, A, EA, R, D, κ`）沿用 41 的錨點。本版沒有為它們建立內容效度包；若審稿要求，比照 56 與 61 的程序建立，其結果不得以 AI 評分代替。

## 4.3 企業與事業單位的配置空間

**表 4.4　企業 AI portfolio 盤點**

| 項目 | 數量／內容 |
|---|---|
| 事業單位 `|U|` | `[EMPIRICAL RESULT PENDING]` |
| AI initiatives `|J|` | `[EMPIRICAL RESULT PENDING]` |
| 共享能力 `|C|`（既有 `y^cur`／候選）；有本地替代方案的 `(u,c)` | `[EMPIRICAL RESULT PENDING]` |
| Policy profiles（CURRENT／LEGAL_MINIMUM／ALTERNATIVE） | `[EMPIRICAL RESULT PENDING]` |
| 每個 initiative 的候選配置數 `|K_j|` | `[EMPIRICAL RESULT PENDING]` |
| 被排除的配置與原因（屬性、查表、權限、狀態查表 UNIDENTIFIED；F2–F10 不可行） | `[EMPIRICAL RESULT PENDING]` |
| 無法評估的 initiatives（`UNEVALUABLE_INITIATIVE`） | `[EMPIRICAL RESULT PENDING]` |
| 現況違規（`STATUS_QUO_NONCOMPLIANT`） | `[EMPIRICAL RESULT PENDING]` |

- 來源資料：62 樣板的 X 區塊（`X_initiatives`、`X_configurations`、`X_config_costs`、`X_capability_state`）、G 區塊與 E 區塊。
- 計算程式：`python 65_enterprise_data_loader_v2_3.py --run <DATA> --out enterprise_results/`。
- 輸出變數：`ENTERPRISE_RESULTS.json` 中的 `loader_log`（loader 層級的排除）、`runs[*].details.excluded_configs`、`runs[*].details.unevaluable_initiatives`、`runs[*].details.status_quo_noncompliant`、`assumptions`。
- 判讀規則：每一個被排除的配置都要列出原因類型；不得以預設值讓它「可行」。`assumptions` 中的 DEF 假設（例如 `J^must` 為空集合、`Rel(j)` 由前提推得）必須逐條寫進正文。
- 待決條件：X 區塊至少有一個 status quo 與一個替代配置被識別。

## 4.4 參數識別覆蓋率

**表 4.5　參數識別覆蓋率（依 43 號文件區塊）**

| 區塊 | 格數 | OBSERVED | EXP 內部 | EXP 外部 | PUBLIC 界 | SCENARIO | DEFINITIONAL | UNIDENTIFIED |
|---|---|---|---|---|---|---|---|---|
| E 企業資源與共享能力 | `[EMPIRICAL RESULT PENDING]` | | | | | | | |
| G Policy 與治理 | `[EMPIRICAL RESULT PENDING]` | | | | | | | |
| X 配置空間與流程 | `[EMPIRICAL RESULT PENDING]` | | | | | | | |
| R 角色反應與訊號 | `[EMPIRICAL RESULT PENDING]` | | | | | | | |
| V 結果、損失、時間 | `[EMPIRICAL RESULT PENDING]` | | | | | | | |
| U 不確定性設定（事前登記列數） | `[EMPIRICAL RESULT PENDING]` | | | | | | | |

**表 4.5b　Q1–Q8 的最小識別集合是否滿足**

| 研究問題 | 所需 51 求解 | 狀態（51 state machine） | 可回答／部分／UNIDENTIFIED | 缺少的區塊 |
|---|---|---|---|---|
| Q1–Q8 | 依 63 §2 | `[EMPIRICAL RESULT PENDING]` | | |

- 來源資料：62 樣板全部區塊。
- 計算程式：`65 --validate <DATA>` 產生表 4.5；`65 --run <DATA>` 產生表 4.5b（`runs[*].status`、`derived.*.status`）。
- 輸出變數：`VALIDATION.json.coverage`、`CH4_FRAGMENTS.md`、`ENTERPRISE_RESULTS.json.runs`。
- 判讀規則：一題的最小集合不滿足時，該題在 4.6–4.10 標 UNIDENTIFIED，並寫出缺少的格；不得以情境值冒充識別值。`SCENARIO` 與 `PUBLIC` 格只進區間分析，不進 point solve。
- 待決條件：65 `--validate` 的錯誤數為 0。

## 4.5 Portfolio 求解器驗證（SIMULATED_ONLY）

v2.1 的 46 號參考實作在隨機產生的合成實例與一個手算實例上執行（47 號執行紀錄）；v2.2 以 51 號實作取代（52 號執行紀錄，`V2_2_SYNTHETIC_ENGINEERING_VERDICT: PASS`，20 項必要檢查全部通過）。**下表只證明實作與第三章方程一致、命題未被合成反例反駁；不構成任何企業結論。**

**表 4.6　合成 oracle 檢查**

| 檢查 | 結果（SIMULATED_ONLY） |
|---|---|
| P1 排序 `A ≤ C0 ≤ A+ ≤ B`、`C0 ≤ C ≤ B`（6 個隨機種子 × 對齊／不對齊，樂觀與悲觀） | 未被反駁；資源基礎超出時正確輸出 `NOT_COMPARABLE` |
| P2 對齊 ⇒ DL = DL0 = 0（樂觀與悲觀） | 6／6 未被反駁；隨機不對齊實例中 DL > 0 為 0／6，DL > 0 只在手算實例中出現——不對齊不必然造成授權損失 |
| 恆等式 NEV = VCP + VSC − DL、VCP = VRA + DL0 | 成立 |
| Lemma E／E′（有限 envelope = 整數網格 envelope；只用部門自身計畫資源向量） | 樂觀與悲觀皆相等 |
| P4 能力門檻唯一，且預算寬鬆時 `F_c^† = G_1 − G_0`；以來源為索引的共享重用 `δ`（允許本地自建）在 8 個種子中至多由不建置切換為建置一次 | 未被反駁 |
| P5 序位重標（含非等距與負值編碼） | 解完全不變 |
| P6 金額 ×1000、期間 ×2 | 決策不變，價值等比例 |
| 共享固定成本只計一次 | 以原始查表獨立重算的 portfolio 價值等於求解值；`F_c` 加 1 TWD 時，在 4 個 initiatives 共用該能力下企業價值恰減 1 |
| Ties：樂觀界 > 悲觀界 | 構造實例成立 |
| 缺值與無效輸入 | 缺配置格 → 排除並記錄（RESTRICTED）；缺現況格 → 拒算；缺 Allow 不以預設值補；缺帳本拆分 → B 可解、C 拒算；`ρ` 不正規化、禁止反應正機率、序位算術、跨構念比較 → 拒絕 |
| P7（B）放寬要求單調；`VG = EE + RE + CE`，`RE ≤ 0` | 未被反駁 |
| P8（C）要求的篩選作用 | 手算實例中加上評估門檻使 `F^C` 由 10 升至 15（等於 `F^B`），`F^B` 不變 |
| (F9) 硬上限 | 構造實例中 4 個配置被排除，未貨幣化 |
| 手算 oracle（三情境；v2.2 由未接觸程式碼的獨立代理者依文字規格重新手算） | 對齊：B = C = 30；不對齊但可由 envelope 阻擋：B = C = 15（DL = 0）；不對齊且不可阻擋：B = 15、C = 10、DL = 5、VSC = 15、NEV = 10；求解器 66 個值全部相符 |
| v2.2：型別單位、`ω` 洩漏、NaN／inf | 單位代數成立；4 種不相容運算、4 種含 `ω` 的鍵與 57 種非有限值突變全部被拒 |
| v2.2：(F5e) 資料／介面門檻 | 在所選能力狀態下求值（含現況）；缺查表只排除該配置；序位重標不變 |
| v2.2：13 種輸出狀態與缺值 | 全部可達且以結果回傳；20 類缺值 × B、C 均可與「補 0」區分 |
| v2.2：`F_c` 缺（門檻模式） | 合成例 `F_c^† = 82.497`，與 8 次顯式求解一致 |
| v2.2：`λ` 缺 | 寬區間：決策改變，不輸出點決策；窄區間：頂點證書成立並經網格確認 |
| v2.2：動態規劃 = 完整列舉 | 20 個整數種子（預算綁住）、400 個隨機整數背包完全相等；400 個非整數背包的最適值皆在誤差界內 |
| v2.2：Model D 閘門 | T1–T5 任一不成立時 0 次三層求解 |
| v2.2：重現性與標籤重排 | 4 次執行雜湊相同；重新命名後完整最適集合同構 |
| v2.2：Lemma R 範圍、穩健可行性、registry 承諾 | 證書與內部抽樣一致；元素層級與 C 使用時拋出範圍錯誤；可行性四類；名目值相對變動 1e-12 即被偵測 |
| v2.2：MaxRegret 與 VOI | 頂點 MaxRegret 未被 49 點內部網格超過；解析例中頂點 VOI = 1（高估）、網格 VOI = 0.5（真值） |
| v2.2：C 中 `δ` 的非單調反例 | 建置序列 1,1,1,1,0,0,0,1；建置區域為集合值 |

本表的實作於 Phase F 對抗式稽核後修訂（42 §19）：稽核以反例指出原版 P7 在 C 不成立、Lemma R 對元素層級不精確、以可用與否為索引的重用表破壞 P4、P1 漏掉治理成本條件等問題，均已修正並加入對應測試。v2.1 列為尚未完成的項目（Lemma R 頂點檢查、robust feasibility、MaxRegret、value-of-identification、DP 背包、(F5e)、typed units 與狀態碼輸出）已於 v2.2 完成，並再經兩輪對抗式稽核（13 項與 7 項發現）修正，所有修正皆有回歸測試（50 號文件 §7）。兩輪稽核與實作者屬同一模型家族，建議在企業使用前另做人工 code review。

## 4.6 集中規劃（B）與雙層（C）

**表 4.7　B vs C（每個 policy 一列）**

| `γ` | `F_E^B` | `F_E^{C,opt}` | `F_E^{C,pess}` | DL（opt, pess） | 關閉 AL1 後的 DL | 關閉 AL2 後的 DL | 關閉 AL4 後的 DL | 全部關閉後的 DL |
|---|---|---|---|---|---|---|---|---|
| `γ…` | `[EMPIRICAL RESULT PENDING]` | | | | | | | |

- 來源資料：62 全部區塊；DL 另需帳本拆分（`v_x, l_x, c_x, impl_x, tau, lam_u`）。
- 計算程式：`65 --run`。
- 輸出變數：`runs["B|γ"].F_E`、`runs["C|γ"].F_E.{opt,pess}`、`derived.dl_sources.{AL1,AL2,AL4,ALL}.DL`。
- 判讀規則：
  - DL = 0 且 (AL) 都成立 → 報告「此帳本安排下跨層一致」。
  - DL > 0 → 報告哪一個 (AL) 被關閉後 DL 消失或下降。單一關閉的 DL 不可相加。
  - (AL3) 部門專屬限制不在 51 baseline，只有在有文件證據時才另外建模。
  - 這是在完全資訊假設下的模型內比較（P3），不證明分權較差。
- 待決條件：`C|γ` 的狀態不是 `FOLLOWER_LEDGER_UNIDENTIFIED`。

## 4.7 組織型態比較（A／C0／A+／B／C）與共享能力

**表 4.8　組織型態比較（current policy）**

| `F_E^A` (opt, pess) | `F_E^{C0}` (opt, pess) | `F_E^{A+}` | `F_E^B` | `F_E^C` (opt, pess) | VRA | DL0 | VCP | VSC | DL | NEV (opt, pess) |
|---|---|---|---|---|---|---|---|---|---|---|
| `[EMPIRICAL RESULT PENDING]` | | | | | | | | | | |

- 來源資料：同 4.6，另加 `B0_BUD`、`B0_ENG`（Model A）與本地替代方案（`E_capabilities` scope=LOCAL）。
- 計算程式：`65 --run`。
- 輸出變數：`derived.architecture.{A,C0,Aplus,B,C,VRA,DL0,VCP,VSC,DL,NEV}`；若有任一型態不可解，則報告 `derived.architecture.{status, available, partial}`。
- 判讀規則：
  - P1 排序是模型性質；實證上只報告 NEV 的符號與區間，以及它在 4.8 中是否穩健。
  - 任一型態不可解時，只報告可算的分量（例如只報 VSC），其餘標 UNIDENTIFIED。
- 待決條件：Model A 需要 `B^0_u`，且其總和加上 `ΔC^gov` 不超過 `Ā`（否則為 `NOT_COMPARABLE`）。

**表 4.9　共享能力損益兩平**

| 能力 `c` | 已識別的 `F_c`（或區間） | `F_c^†`（B） | `F_c^†`（C opt, pess） | `F_c ≤ F_c^†`？ | `δ` 掃描（C 中為集合值） |
|---|---|---|---|---|---|
| `c…` | `[EMPIRICAL RESULT PENDING]` | | | | |

- 來源資料：同 4.7。
- 計算程式：`65 --run`。loader 會在副本中把 `F_c` 設為 UNIDENTIFIED，交由 51 的 THRESHOLD_MODE 求門檻。
- 輸出變數：`derived.capability_thresholds["c|B"/"c|C"].{threshold, F_c_identified}`。
- 判讀規則：`F_c` 的可接受區間完全落在 `F_c^†` 之下 → 集中建置穩健；區間跨越 `F_c^†` → CONDITIONAL，且 `F_c` 為高價值的量測項目（64）。
- 待決條件：Model B 可解。

## 4.8 穩健性、MaxRegret 與 VOI

**表 4.10　事前登記的 scenario registry**

| 群組 | 區塊數 | 頂點數 | 登記日期 | `registry_commitment`（SHA-256） |
|---|---|---|---|---|
| `g1…` | `[EMPIRICAL RESULT PENDING]` | | | |

**表 4.11　穩健決策與 regret**

| 決策 | minimax-regret portfolio | MaxRegret | Lemma R 整體 portfolio 證書 | `y` 元素層級分類（涵蓋點數） | 可行性類別計數 |
|---|---|---|---|---|---|
| `γ_current` | `[EMPIRICAL RESULT PENDING]` | | | | |

**表 4.12　Value of identification（各區塊）**

| 參數區塊 | VOI（頂點） | VOI（網格） | 最壞值 | 64 的層級 |
|---|---|---|---|---|
| `…` | `[EMPIRICAL RESULT PENDING]` | | | |

- 來源資料：62 中以區間識別的格（`INTERVAL`），以及 `U_registry`。
- 計算程式：
  1. `65 --make-registry <DATA> --out registry_vN/`，然後**先 commit** `REGISTRY_DRAFT.json` 與 `REGISTRY_COMMITMENT.txt`。
  2. `65 --robust <DATA> --registry registry_vN/ --out enterprise_results/`。
- 輸出變數：`ROBUST_RESULTS.json.robust.{decision, max_regret, whole_portfolio_robust, n_candidates, feasibility_classes, registry_commitment}`、`voi.{vertex,grid}`、`element_y.{classification, coverage}`。
- 判讀規則：
  - 只有 Model B 的整體 portfolio 有精確證書（Lemma R）。元素層級與 Model C 只報涵蓋率，不稱「對所有 θ」。
  - VOI 同時報頂點版（可能高估）與網格版。
  - registry 在看到結果後不得更改；若必須更改，重新登記並揭露兩版。
- 待決條件：至少一個區間格；頂點數 ≤ 4096，否則先登記分組規則。

## 4.9 外部挑戰

外部評估者（董事端或其所屬公司、合作商／策略供應商、投資端）只作為參數界定與結果挑戰的來源，不是模型中的決策者。

**表 4.13　外部挑戰紀錄**

| 挑戰對象 | 評估者類型（`external_role`） | 原區間 | 挑戰後區間或替代方案 | 理由 | 對 4.7／4.8 分類的影響 |
|---|---|---|---|---|---|
| `v`、`J^must`、`κ`、`ē`、`F_c`、`δ`、portfolio 優先序 | `[EMPIRICAL RESULT PENDING]` | | | | |

- 來源資料：62 `S_sources`（`source_scope=external`）以及標為 `EXPERT_ELICITED_EXTERNAL` 的格。
- 計算程式：以挑戰後的區間另建一個 registry 群組（`65 --make-registry`，新的 commitment），與原群組並列執行 `--robust`。
- 輸出變數：兩個群組的 `robust.decision`、`max_regret`、分類。
- 判讀規則：外部意見只能擴大或收窄 `Θ_g`、新增 `γ` 選項或情境組。不得改標為 OBSERVED（65 validator 會拒絕），不得覆寫模型結果，也不得成為 optimizer。
- 待決條件：至少一個外部來源的區間。

## 4.10 Q1–Q8 主要發現

**表 4.14　研究問題總表**

| 研究問題 | 回答形式 | 輸出變數（65 / 60 / 61） | 結果 |
|---|---|---|---|
| Q1 企業協調 vs 各部門獨立 | NEV 的區間與分類 | `derived.architecture.NEV`；4.8 的分類 | `[EMPIRICAL RESULT PENDING]` |
| Q2 共享能力投資條件 | `F_c^†`、`δ` 掃描與分類 | `derived.capability_thresholds` | `[EMPIRICAL RESULT PENDING]` |
| Q3 治理 vs 官僚 | VG = EE + RE + CE | `derived.governance` | `[EMPIRICAL RESULT PENDING]` |
| Q4 局部最適偏離 | DL 與 (AL) 來源 | `derived.dl_sources` | `[EMPIRICAL RESULT PENDING]` |
| Q5 H／WI／EA 是否為必要限制 | AT／ABOVE、`PR_X`、保護功能 | `derived.price_of_requirement`、`derived.requirement_status` | `[EMPIRICAL RESULT PENDING]` |
| Q6 使用者反應的影響 | VRG、design-response regret | `derived.design_response` | `[EMPIRICAL RESULT PENDING]` |
| Q7 穩健與脆弱的決策 | 整體 portfolio 證書；元素層級（涵蓋率） | `ROBUST_RESULTS.json` | `[EMPIRICAL RESULT PENDING]` |
| Q8 形成企業決策問題的 gaps | 介面活化 → gaps（需要 V1） | `derived.interface_activation` ＋ 表 4.2d | `[EMPIRICAL RESULT PENDING]` |

**表 4.15　治理價值分解（Q3）**

| `γ` vs `γ^0` | VG | EE | RE | CE |
|---|---|---|---|---|
| | `[EMPIRICAL RESULT PENDING]` | | | |

判讀：在 B 中 RE ≤ 0 是模型性質（P7）。治理的正價值只能來自賦能、穩健可行，或（只在 C 中）篩選。

**表 4.16　要求代價與狀態（Q5）**

| 要求 `X` | `PR_X`（放寬一級，B） | 放寬後配置 | 保護功能（需要 4.8） | 各 initiative 的 AT／ABOVE |
|---|---|---|---|---|
| H／WI／EA／G | `[EMPIRICAL RESULT PENDING]` | | | |

判讀：
- `PR_X > 0`，且放寬後仍 robustly feasible → 模型內沒有保護功能的要求。這是官僚成本的候選，不是定論。
- 放寬後失去 robust feasibility → robustness-protective。
- C 中 `PR_X < 0` → 篩選。

**表 4.17　使用者反應（Q6）**

| 狀態 | VRG | Design-response regret |
|---|---|---|
| `[EMPIRICAL RESULT PENDING]` | | |

判讀：若設計 portfolio 在實際反應下不可行，輸出 `DESIGN_INFEASIBLE_UNDER_RESPONSE`，這本身就是正式結果。

**表 4.18　介面活化（Q8）**

| 介面 | 綁住的元素（`PR_X > 0`） | 與現況不同的配置 | 分類 | 對應的 gaps（依表 4.2d 的最終碼） |
|---|---|---|---|---|
| I1–I4 | `[EMPIRICAL RESULT PENDING]` | | | `[HUMAN RESULT PENDING]` |

本節的每一項結論都必須同時寫出其分類（ROBUST、CONDITIONAL、FRAGILE 或 UNIDENTIFIED），以及仍未識別的參數。文獻網絡的 depletion 不得以因果語言描述。

---

# 伍、討論（骨架）

本章在實證結果完成後撰寫。以下列出各節要處理的問題，以及目前**已可由模型命題陳述的條件性意涵**（這些是模型內的邏輯結果，不是實證發現）與**不得宣稱的內容**。

## 5.1 對企業 AI 導入研究的貢獻

- 待寫：實證結果是否支持「企業 AI 導入是 portfolio 配置問題」而非採用分數問題。`[EMPIRICAL RESULT PENDING]`
- 不得宣稱：任何能力或成熟度構念與企業績效的因果關係。

## 5.2 對 AI 治理的貢獻

- 模型內意涵：在集中規劃下（P7），治理要求本身不增加已定價的價值；治理的正價值來自賦能、在不確定性下維持硬限制，以及在雙層且帳本不對齊時的篩選（P8）。因此「治理是否值得」應以 EE、robustness-protective 與 screening 判定回答，而不是以「有沒有治理」回答。P8 也提供一個可檢驗的實務命題：當預算 envelope 無法阻擋部門的不利選擇時，規則型治理可替代預算型協調。
- 待寫：表 4.11 的實證分解。`[EMPIRICAL RESULT PENDING]`
- 不得宣稱：特定治理框架（NIST、ISO）對本企業價值的效果。

## 5.3 對人機決策配置的貢獻

- 模型內意涵：設計反應與實際反應的差（VRG）可正可負；以設計假設做決策的代價（design-response regret）恆非負。
- 待寫：表 4.12。`[EMPIRICAL RESULT PENDING]`
- 不得宣稱：外部實驗的效果量代表本企業的人機互補程度。

## 5.4 對企業 portfolio 與多層決策模型的貢獻

- 模型內意涵：跨層衝突可由帳本對齊條件檢驗；Lemma E′ 使 envelope 雙層問題可精確有限求解；KKT 重構不適用於整數下層。
- 不得宣稱：模型形式的存在即代表企業內有真實衝突。

## 5.5 企業協調創造價值的條件

- 模型內意涵：NEV = VCP + VSC − DL，且 VCP = VRA + DL0。企業協調的價值來自資源重分配（VRA）、不共享時的帳本對齊（DL0）與共享能力（VSC），被授權損失（DL）抵減；DL 只在帳本不對齊且 envelope 無法分離時為正。
- 待寫：表 4.8。`[EMPIRICAL RESULT PENDING]`

## 5.6 局部自主占優的條件

- 模型界線：本模型為完全資訊，模型內集中規劃必然弱優於雙層（P3）；局部資訊優勢（Alonso et al., 2008）不在模型內。因此本研究**不能**以模型結果主張分權較差；若 NEV 在某情境為負，其原因只能是 DL 大於 VCP + VSC，而不是資訊因素。
- 待寫：若取得「企業與部門知道不同參數」的證據，報告附錄 B^info sensitivity。`[EMPIRICAL RESULT PENDING]`

## 5.7 治理作為價值賦能限制 vs 官僚

- 待寫：依表 4.11，區分 robustness-protective、screening 與模型內無保護功能的要求；後者只是官僚成本的候選，需討論模型未涵蓋的風險。`[EMPIRICAL RESULT PENDING]`

## 5.8 共享能力經濟學的理論地位

- 模型內意涵：共享能力的投資決策具唯一門檻 `F_c^†`（P4）；以來源為索引時，共享重用效果在集中規劃下亦有唯一門檻，在雙層中只有在帳本對齊時才保證單調，否則建置區域可為集合值（合成反例，4.5 節）。
- 不得宣稱：「共享一定比自建便宜」。

## 5.9 單一企業／嵌入式個案推論的界線

- 結果只對所研究企業、所登記的 `Θ_adm` 與 `𝒢` 成立；不外推至其他企業或產業。

## 5.10 語料 parity 限制

- V5 的正式方法鏈已調和為 `6,499 analytical strict-frame records → 3,125 fully mapped / pair-eligible semantic records → 783 pair-eligible unique documents → M = 2,180 document-level edges`；V5 Stage 2 使用 `qwen2.5:14b` constrained double-pass mapping。較早的 404 publications／2,425 strict records／GPT-5.6 Sol lineage 僅保留為 predecessor provenance，不作本版 network denominator。
- Corpus parity 的限制仍存在：AI 軌有較高比例的 abstract-level evidence，Decision 軌主要由 full-text evidence 構成。因此 G01–G16 僅以 robust depletion 的方向作研究線索，其幅度、O/E 或 q 值不得被解讀為企業 effect size 或模型係數。
- Depletion 不等於企業中的缺口或不重要性。

## 5.11 M5 縱向擴充

- G11、G12 需要至少兩期的配置與結果紀錄；J-curve（Brynjolfsson et al., 2021）與吸收能力（Cohen & Levinthal, 1990）的跨期性質只能在 M5 中檢驗；選擇權價值（Benaroch & Kauffman, 1999）同屬此層。

---

# 陸、結論（骨架）

`[EMPIRICAL RESULT PENDING]`——結論在 4.10 完成後撰寫，必須：(i) 以 Q1–Q8 的分類結果回答 RQ1–RQ5；(ii) 區分 ROBUST、CONDITIONAL、FRAGILE 與 UNIDENTIFIED 的發現；(iii) 列出未識別參數與其對結論的影響；(iv) 不使用因果語言描述文獻網絡的 depletion。

---

# 參考文獻

Aghion, P., & Tirole, J. (1997). Formal and real authority in organizations. *Journal of Political Economy, 105*(1), 1–29. https://doi.org/10.1086/262063

Alonso, R., Dessein, W., & Matouschek, N. (2008). When does coordination require centralization? *American Economic Review, 98*(1), 145–179. https://doi.org/10.1257/aer.98.1.145

Amershi, S., Begel, A., Bird, C., DeLine, R., Gall, H., Kamar, E., Nagappan, N., Nushi, B., & Zimmermann, T. (2019). Software engineering for machine learning: A case study. In *2019 IEEE/ACM 41st International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP)* (pp. 291–300). IEEE. https://doi.org/10.1109/ICSE-SEIP.2019.00042

Archer, N. P., & Ghasemzadeh, F. (1999). An integrated framework for project portfolio selection. *International Journal of Project Management, 17*(4), 207–216. https://doi.org/10.1016/S0263-7863(98)00032-5

Bansal, G., Wu, T., Zhou, J., Fok, R., Nushi, B., Kamar, E., Ribeiro, M. T., & Weld, D. S. (2021). Does the whole exceed its parts? The effect of AI explanations on complementary team performance. In *Proceedings of the 2021 CHI Conference on Human Factors in Computing Systems*. https://doi.org/10.1145/3411764.3445717

Ben-Tal, A., El Ghaoui, L., & Nemirovski, A. (2009). *Robust optimization*. Princeton University Press. ISBN 9780691143682

Benaroch, M., & Kauffman, R. J. (1999). A case for using real options pricing analysis to evaluate information technology project investments. *Information Systems Research, 10*(1), 70–86. https://doi.org/10.1287/isre.10.1.70

Berente, N., Gu, B., Recker, J., & Santhanam, R. (2021). Special issue editor's comments: Managing artificial intelligence. *MIS Quarterly, 45*(3), 1433–1450. https://doi.org/10.25300/MISQ/2021/16274

Breck, E., Cai, S., Nielsen, E., Salib, M., & Sculley, D. (2017). The ML test score: A rubric for ML production readiness and technical debt reduction. In *2017 IEEE International Conference on Big Data* (pp. 1123–1132). IEEE. https://doi.org/10.1109/BigData.2017.8258038

Brynjolfsson, E., Rock, D., & Syverson, C. (2021). The productivity J-curve: How intangibles complement general purpose technologies. *American Economic Journal: Macroeconomics, 13*(1), 333–372. https://doi.org/10.1257/mac.20180386

Cohen, W. M., & Levinthal, D. A. (1990). Absorptive capacity: A new perspective on learning and innovation. *Administrative Science Quarterly, 35*(1), 128–152. https://doi.org/10.2307/2393553

Colson, B., Marcotte, P., & Savard, G. (2007). An overview of bilevel optimization. *Annals of Operations Research, 153*(1), 235–256. https://doi.org/10.1007/s10479-007-0176-2

Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement, 20*(1), 37–46. https://doi.org/10.1177/001316446002000104

Dempe, S. (2002). *Foundations of bilevel programming* (Nonconvex Optimization and Its Applications, Vol. 61). Kluwer Academic Publishers. https://doi.org/10.1007/b101970

Dietvorst, B. J., Simmons, J. P., & Massey, C. (2015). Algorithm aversion: People erroneously avoid algorithms after seeing them err. *Journal of Experimental Psychology: General, 144*(1), 114–126. https://doi.org/10.1037/xge0000033

Elish, M. C. (2019). Moral crumple zones: Cautionary tales in human-robot interaction. *Engaging Science, Technology, and Society, 5*, 40–60. https://doi.org/10.17351/ests2019.260

Enholm, I. M., Papagiannidis, E., Mikalef, P., & Krogstie, J. (2022). Artificial intelligence and business value: A literature review. *Information Systems Frontiers, 24*(5), 1709–1734. https://doi.org/10.1007/s10796-021-10186-w

European Union. (2024). Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act). *Official Journal of the European Union*, L, 2024/1689, 12.7.2024. http://data.europa.eu/eli/reg/2024/1689/oj (Amended by Regulation (EU) 2026/1744, OJ L 2026/1744, 24.7.2026; consolidated version 27.7.2026. This manuscript relies on no provision introduced by that amendment.)

International Organization for Standardization & International Electrotechnical Commission. (2023). *Information technology — Artificial intelligence — Management system* (ISO/IEC Standard No. 42001:2023).

Jöhnk, J., Weißert, M., & Wyrtki, K. (2021). Ready or not, AI comes—An interview study of organizational AI readiness factors. *Business & Information Systems Engineering, 63*, 5–20. https://doi.org/10.1007/s12599-020-00676-7

Kellogg, K. C., Valentine, M. A., & Christin, A. (2020). Algorithms at work: The new contested terrain of control. *Academy of Management Annals, 14*(1), 366–410. https://doi.org/10.5465/annals.2018.0174

Kleinert, T., Labbé, M., Ljubić, I., & Schmidt, M. (2021). A survey on mixed-integer programming techniques in bilevel optimization. *EURO Journal on Computational Optimization, 9*, Article 100007. https://doi.org/10.1016/j.ejco.2021.100007

Krippendorff, K. (2004). Reliability in content analysis: Some common misconceptions and recommendations. *Human Communication Research, 30*(3), 411–433. https://doi.org/10.1111/j.1468-2958.2004.tb00738.x

Kozlowski, S. W. J., & Klein, K. J. (2000). A multilevel approach to theory and research in organizations: Contextual, temporal, and emergent processes. In K. J. Klein & S. W. J. Kozlowski (Eds.), *Multilevel theory, research, and methods in organizations: Foundations, extensions, and new directions* (pp. 3–90). Jossey-Bass.

Lebovitz, S., Lifshitz-Assaf, H., & Levina, N. (2022). To engage or not to engage with AI for critical judgments: How professionals deal with opacity when using AI for medical diagnosis. *Organization Science, 33*(1), 126–148. https://doi.org/10.1287/orsc.2021.1549

Lempert, R. J., Popper, S. W., & Bankes, S. C. (2003). *Shaping the next one hundred years: New methods for quantitative, long-term policy analysis* (MR-1626-RPC). RAND Corporation. https://doi.org/10.7249/MR1626

Logg, J. M., Minson, J. A., & Moore, D. A. (2019). Algorithm appreciation: People prefer algorithmic to human judgment. *Organizational Behavior and Human Decision Processes, 151*, 90–103. https://doi.org/10.1016/j.obhdp.2018.12.005

McFarlan, F. W. (1981, September). Portfolio approach to information systems. *Harvard Business Review* (Product No. 81510). https://hbr.org/1981/09/portfolio-approach-to-information-systems

Mikalef, P., & Gupta, M. (2021). Artificial intelligence capability: Conceptualization, measurement calibration, and empirical study on its impact on organizational creativity and firm performance. *Information & Management, 58*(3), Article 103434. https://doi.org/10.1016/j.im.2021.103434

Moore, J. T., & Bard, J. F. (1990). The mixed integer linear bilevel programming problem. *Operations Research, 38*(5), 911–921. https://doi.org/10.1287/opre.38.5.911

National Institute of Standards and Technology. (2023). *Artificial intelligence risk management framework (AI RMF 1.0)* (NIST AI 100-1). U.S. Department of Commerce. https://doi.org/10.6028/NIST.AI.100-1

Papagiannidis, E., Mikalef, P., & Conboy, K. (2025). Responsible artificial intelligence governance: A review and research framework. *Journal of Strategic Information Systems, 34*(2), Article 101885. https://doi.org/10.1016/j.jsis.2024.101885

Polit, D. F., & Beck, C. T. (2006). The content validity index: Are you sure you know what's being reported? Critique and recommendations. *Research in Nursing & Health, 29*(5), 489–497. https://doi.org/10.1002/nur.20147

Polit, D. F., Beck, C. T., & Owen, S. V. (2007). Is the CVI an acceptable indicator of content validity? Appraisal and recommendations. *Research in Nursing & Health, 30*(4), 459–467. https://doi.org/10.1002/nur.20199

Raisch, S., & Krakowski, S. (2021). Artificial intelligence and management: The automation–augmentation paradox. *Academy of Management Review, 46*(1), 192–210. https://doi.org/10.5465/amr.2018.0072

Raji, I. D., Smart, A., White, R. N., Mitchell, M., Gebru, T., Hutchinson, B., Smith-Loud, J., Theron, D., & Barnes, P. (2020). Closing the AI accountability gap: Defining an end-to-end framework for internal algorithmic auditing. In *Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency* (pp. 33–44). ACM. https://doi.org/10.1145/3351095.3372873

Sambamurthy, V., & Zmud, R. W. (1999). Arrangements for information technology governance: A theory of multiple contingencies. *MIS Quarterly, 23*(2), 261–290. https://doi.org/10.2307/249754

Savage, L. J. (1951). The theory of statistical decision. *Journal of the American Statistical Association, 46*(253), 55–67. https://doi.org/10.1080/01621459.1951.10500768 `[VERIFY: attribution of minimax regret not confirmed at the primary text; the criterion is used as this study's operational definition]`

Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., Chaudhary, V., Young, M., Crespo, J.-F., & Dennison, D. (2015). Hidden technical debt in machine learning systems. *Advances in Neural Information Processing Systems, 28*, 2503–2511.

Shrestha, Y. R., Ben-Menahem, S. M., & von Krogh, G. (2019). Organizational decision-making structures in the age of artificial intelligence. *California Management Review, 61*(4), 66–83. https://doi.org/10.1177/0008125619862257

Teece, D. J. (1986). Profiting from technological innovation: Implications for integration, collaboration, licensing and public policy. *Research Policy, 15*(6), 285–305. https://doi.org/10.1016/0048-7333(86)90027-2

Vaccaro, M., Almaatouq, A., & Malone, T. (2024). When combinations of humans and AI are useful: A systematic review and meta-analysis. *Nature Human Behaviour, 8*, 2293–2303. https://doi.org/10.1038/s41562-024-02024-1

Weill, P., & Ross, J. W. (2004). *IT governance: How top performers manage IT decision rights for superior results*. Harvard Business School Press.

Wiesemann, W., Tsoukalas, A., Kleniati, P.-M., & Rustem, B. (2013). Pessimistic bilevel optimization. *SIAM Journal on Optimization, 23*(1), 353–380. https://doi.org/10.1137/120864015

---

# 附錄 A　引文主張稽核（claim-level audit）

驗證狀態：`YES` = 書目與摘要層級主張已核對；`PARTIAL` = 書目已核對，但主張只核到標題、摘要首句或二手來源；既有 S1–S6 沿用 `29_CLAIM_LEVEL_SOURCE_AUDIT_v1_5.md`。短摘為摘要或出版者摘要中的原文片段。

| ID | Source | 驗證 | Exact Claim（短摘） | What It Supports | What It Does NOT Support | Model Element | Section |
|---|---|---|---|---|---|---|---|
| S1 | Shrestha et al. (2019) | YES（29） | "full human to AI delegation" | 決策結構可分委託、序列、聚合 | 本研究 A0–A3 或配置清單是原文分類 | `m_k`、`Cons(A,m)` | 2.4 |
| S2 | Raisch & Krakowski (2021) | PARTIAL（29：作者機構摘要） | "augmentation cannot be neatly separated from automation" | 自動化與增強相互依賴 | 全文細節；跨期效果量 | `m_k` 與 `A_k` 組合；M5 | 2.3 |
| S3 | Vaccaro et al. (2024) | YES（29） | "decision tasks were associated with performance losses" | 人機組合不必然互補；異質性 | 本企業效果；人機協作必然有害 | `P, ρ` 須查表；禁止固定 adoption bonus | 2.4 |
| S4 | Bansal et al. (2021) | YES（29） | "regardless of its correctness" | 解釋提高接受，包括錯誤建議 | 解釋降低風險 | `EAX` 只作 `ρ` 鍵 | 2.4, 2.5 |
| S5 | Elish (2019) | YES（29） | "limited control over the behavior" | 責任與控制可能錯置 | 本企業已發生錯置 | `Eff_H`、(F6) | 2.2 |
| S6 | Jöhnk et al. (2021) | YES（29） | "18 readiness factors along five categories" | 準備度多面向 | D/R/G 涵蓋完整準備度 | 準備度作情境；F5 門檻鍵 | 2.1 |
| N1 | Berente et al. (2021) | YES（編輯評論） | "Managing artificial intelligence (AI) marks the dawn of a new age of information technology management." | 管理 AI 為 IT 管理新階段的框架定位 | 任何實證效果（此為編輯評論） | 研究定位 | 2.1 |
| N2 | Mikalef & Gupta (2021) | YES（v2.2；出版者摘要經 OpenAlex 取得，見 57 R1） | "develops an instrument to capture the AI capability in firms"；作者報告 "AI capability results in increased organizational creativity and performance"（本稿改述為「相關」） | AI capability 可被概念化與測量，並與績效相關 | 特定投資的因果效果；成熟度分數作決策模型 | 不以能力分數作目標 | 2.1 |
| N3 | Enholm et al. (2022) | YES | "Artificial Intelligence (AI) are a wide-ranging set of technologies that promise several advantages for organizations." | 價值實現有促成／阻礙因素與第一、二序效果 | 價值大小；配置規則 | 帳本（V1）分項 | 2.1 |
| N4 | Brynjolfsson et al. (2021) | YES | "These investments are often intangible and poorly measured in national accounts." | 互補無形投資；J-curve | 本企業時間型態 | `F_c`、`C^impl` 必須明列；M5 | 2.1, 2.6, 5.11 |
| N5 | Sambamurthy & Zmud (1999) | YES | "IT governance arrangements refers to the patterns of authority for key IT activities in business firms" | 治理為權威配置模式，依多重情境 | 特定 AI 治理方案的價值 | `Γ` 為有限選單 | 2.2, 2.7 |
| N6 | Weill & Ross (2004) | YES（書目；**僅用書名層級概念**） | 書名："How top performers manage IT decision rights" | 治理以決策權配置為核心 | 出版者行銷文字中的獲利差異數字（不得引用） | `γ`、`G_j(γ)` | 2.2 |
| N7 | Papagiannidis et al. (2025) | YES | 摘要首句："The widespread and rapid diffusion of artificial intelligence (AI) into all types of organizational activities" | 負責任 AI 治理的結構性、關係性、程序性實務 | 任何治理實務的效果大小 | `γ` 的組成（Allow、要求表、程序成本） | 2.2 |
| N8 | Aghion & Tirole (1997) | YES | "Real authority is determined by the structure of information." | 正式權威與實質權威分離 | AI 特定門檻 | `G_j(γ)` vs `Eff_H` | 2.2 |
| N9 | NIST (2023) | YES | "to help manage the many risks of AI and promote trustworthy and responsible development and use of AI systems" | 自願性 AI 風險管理結構 | 本企業的要求值；強制性 | `γ` 的結構參照 | 2.2, 2.5 |
| N10 | ISO/IEC 42001:2023 | YES | "This document specifies the requirements and provides guidance for establishing, implementing, maintaining and continually…" | 組織 AI 管理系統要求存在 | 本企業是否採用或其效果 | `γ` 的結構參照 | 2.2 |
| N11 | Regulation (EU) 2024/1689 | YES（v2.2；EUR-Lex；已由 Reg (EU) 2026/1744 修正，見 57 R5） | "The purpose of this Regulation is to improve the functioning of the internal market and promote the uptake" | 存在具拘束力的 AI 統一規則 | 特定條文對本企業的適用（須逐條法律核對） | `Legal_jk` | 2.2 |
| N12 | Amershi et al. (2019) | YES | "We report on a study that we conducted on observing software teams at Microsoft as they develop AI-based applications." | ML 納入工作流程有特有挑戰 | 本企業整合成本 | `WI`、`C^impl`、`a^ENG` | 2.3 |
| N13 | Sculley et al. (2015) | YES（v2.2；proceedings.neurips.cc，見 57 R2） | "it is common to incur massive ongoing maintenance costs in real-world ML systems" | ML 系統伴隨持續維護成本 | 技術債量級 | `Rec_jk`、`F_c` 持續成本 | 2.3, 2.6 |
| N14 | Kellogg et al. (2020) | YES | "algorithmic control in the workplace operates through six main mechanisms" | 演算法控制機制與工作者抵抗 | 本企業反應機率 | `R` 含 Reject、Bypass | 2.3, 1.1 |
| N15 | Dietvorst et al. (2015) | YES | "people more quickly lose confidence in algorithmic than human forecasters" | 演算法迴避 | 本企業拒用率 | `ρ` 方向不預設 | 2.4 |
| N16 | Logg et al. (2019) | YES | "lay people adhere more to advice when they think it comes from an algorithm than from a person" | 演算法偏好 | 本企業採用率 | `ρ` 方向不預設 | 2.4 |
| N17 | Lebovitz et al. (2022) | YES | "professionals experiencing increased uncertainty because AI tool results often diverged from their initial judgment" | 反應受分歧訊號與不透明影響 | 醫療以外的外推 | `z`（可見訊號）作 `ρ` 條件 | 2.4 |
| N18 | Breck et al. (2017) | YES | "In this paper, we present 28 specific tests and monitoring needs" | 測試與監控可分級 | EA 單調降低損失 | `EA` 錨點與成本 | 2.5 |
| N19 | Raji et al. (2020) | YES | "we introduce a framework for algorithmic auditing that supports artificial intelligence system development end-to-end" | 內部稽核框架 | 稽核效果大小 | `EA`、`y_EVAL`、輸出 provenance | 2.5 |
| N20 | McFarlan (1981) | YES（v2.3：引用改為 hbr.org 可核對的書目元素〔1981 年 9 月、Product No. 81510〕；未核對的卷期頁已移除，見 57 v2.3） | "assessing the risks—singly and as a portfolio—in advance of implementation" | 專案層與 portfolio 層風險評估 | AI 特定 portfolio 規則 | portfolio 層求解 | 1.3, 2.6 |
| N21 | Archer & Ghasemzadeh (1999) | YES | "developing a framework which separates the work into distinct stages" | 分階段 portfolio 選擇 | 本研究的目標函數 | 前處理（可行性篩選）→ 選擇 | 1.3, 2.6 |
| N22 | Teece (1986) | YES（v2.2；DOI 經 Crossref 解析，見 57 R4） | "innovating firms often fail to obtain significant economic returns from an innovation" | 價值歸屬依互補資產 | 共享能力必然有價值 | `Pre(j,k)` 能力前提 | 2.6 |
| N23 | Benaroch & Kauffman (1999) | YES | "it provides a formal theoretical grounding for the validity of the Black-Scholes option pricing model" | IT 投資的選擇權價值 | 本企業選擇權價值 | 選擇權價值排除於靜態目標；M5 | 2.6, 3.7 |
| N24 | Cohen & Levinthal (1990) | YES（卷期頁 DOI 取自二手頁面） | "the ability of a firm to recognize the value of new, external information" | 吸收能力依先前知識累積 | 靜態分數 | C 不作構念；`y_CHG`；M5 | 2.6 |
| N25 | Kozlowski & Klein (2000) | YES | "Our goal in this chapter is to help resolve this confusion by synthesizing and extending prior work" | 多層次理論 | 本模型的層級數 | 3.2 層級 | 2.7 |
| N26 | Colson et al. (2007) | YES | "This paper is devoted to bilevel optimization, a branch of mathematical programming" | 雙層最佳化形式與解法 | 企業內衝突存在 | Model C | 2.7 |
| N27 | Dempe (2002) | YES（書目；描述片段） | "If the lower level problem has a unique optimal solution for all parameter values" | 雙層理論基礎；下層唯一解與否的區分 | — | 樂觀／悲觀界 | 2.7 |
| N28 | Moore & Bard (1990) | YES | "A two-person, noncooperative game in which the players move in sequence can be modeled as a bilevel optimization problem." | 依序賽局可為雙層；整數雙層需專門方法 | — | 3.11 不採 KKT | 2.7, 3.11 |
| N29 | Wiesemann et al. (2013) | YES | "We study a variant of the pessimistic bilevel optimization problem" | 悲觀雙層 | — | 悲觀界 | 2.7, 3.11 |
| N30 | Kleinert et al. (2021) | YES（v2.2；Crossref＋摘要，見 57 R6） | "Bilevel optimization is a field of mathematical programming in which some variables are constrained to be the solution" | MIP 雙層技術 | — | 大規模求解備案 | 2.7, 3.11 |
| N31 | Alonso et al. (2008) | YES | "decentralization can dominate centralization even when coordination is extremely important relative to adaptation." | 集權不必然優於分權 | 本企業分權較佳 | P3 模型界線；5.6 | 2.7, 5.6 |
| N32 | Ben-Tal et al. (2009) | YES（v2.2；出版者頁，見 57 R7） | "Robust optimization is still a relatively new approach to optimization problems affected by uncertainty" | 集合式不確定性 | 本研究分類的具體定義 | `Θ_g` | 2.7, 3.12 |
| N33 | Lempert et al. (2003) | YES | "Robust decision methods enable decisionmakers to examine a vast range of plausible futures" | 跨可能未來的穩健決策 | — | `𝒢` 情境組 | 2.7, 3.12 |
| N34 | Savage (1951) | PARTIAL（書目已核；regret 歸屬僅二手；57 R9） | 未取得摘要；minimax regret 歸屬待以原文核對 | regret 準則 | — | MaxRegret | 2.7, 3.12 |

| N35 | Cohen (1960) | YES（v2.2；Crossref，57 R13） | — | κ 統計量 | — | V1 一致性統計 | 3.13 |
| N36 | Krippendorff (2004) | PARTIAL（書目已核；.800／.667 門檻僅二手，57 R12a） | — | α 與其使用 | 門檻的普遍性（本研究將門檻作為預先登記的研究慣例） | V1 判準 | 3.13 |
| N37 | Polit, Beck, & Owen (2007) | YES（v2.2；Crossref＋PubMed，57 R15） | "items with an I-CVI of .78 or higher for three or more experts could be considered evidence of good content validity" | I-CVI ≥ .78 規則 | — | EA-X 錨點保留門檻 | 3.13 |
| N38 | Polit & Beck (2006) | YES（v2.3；以摘要核對方法主張；S-CVI/UA、S-CVI/Ave 等標籤與 .90 標準未以原文核對，故正文不歸屬於本文，見 57 v2.3） | "One method requires universal agreement among experts, but a less conservative method averages the item-level CVIs." | 量表層級 CVI 有兩種算法，應說明採用何者 | 標籤名稱與數值標準 | 4.2 | 4.2 |

---

# 附錄 B　作者待決事項與未解決的引文需求

| # | 事項 | 影響 | 建議 |
|---|---|---|---|
| B1 | ~~two-track corpus lineage 與 V5 計數不一致~~ **已解決（49）** | 1.2、5.10 已依 `6,499 → 3,125 → 783 → 2,180` 改寫 | 前階段 404／2,425 線只作 provenance |
| B2 | ~~語意編碼模型描述不一致~~ **已解決（49）** | V5 Stage 2 為 `qwen2.5:14b` | GPT-5.6 Sol 屬前階段 |
| B3 | ~~Shrestha et al. (2019) 卷期頁~~ **已解決（57 R10）** | 61(4), 66–83 | — |
| B4 | v2.3 後尚餘（57 v2.3）：Savage (1951) 的 regret 歸屬（保留 `[VERIFY]`）、Krippendorff 門檻出處（保留 `[VERIFY]`；門檻本身是預先登記的研究慣例）、Lynn (1986) 頁碼（Crossref 382–386 vs PubMed 382–385；本稿未引用）。已關閉：McFarlan（改為只引可核對元素）、Landis & Koch 標籤（不再報告）、Polit & Beck (2006) 標籤（不再歸屬）、Krippendorff 第 4 版年份（2018）。Teece DOI、Mikalef & Gupta 摘要已解決 | 附錄 A 中 PARTIAL 項 | 以原文核對；不能核對者改引其他已核來源或刪除 |
| B5 | V1 人類雙人盲編與 EA-X 人類內容效度（AI pilot 已完成：54C、56 §8） | 41 的收斂仍只是研究者裁決；G04、G10、G11 具爭議 | 依 53B、v1_human_packet、56 v2.2.1 執行；至少兩位人類編碼者 |
| B6 | `Γ` 的實際替代方案 | VG 只能比較現行與法規最低 | 確認企業是否真的在考慮其他治理方案 |
| B7 | 部門帳本拆分、chargeback 規則、中央出資規則 | DL、NEV 能否計算 | 屬 OBS 文件，應最早取得 |
| B8 | Model A 的現況部門預算是否可得，且總和不超過池化總量 | VCP、NEV 可比性 | 若不可得，只報 B、C、VSC、DL |
| B9 | 歐盟 AI 法之適用性 | `Legal_jk` | 視企業市場與產品逐條法律核對；未核對前不在正文主張其適用 |
| B10 | 本稿與專案中 V5 會議稿的關係（是否為同一研究的延伸論文或學位論文） | 稿件定位與格式 | 由作者決定投稿或學位論文格式 |
| B11 | **RESOLVED — Drive v2.1 → v2.2 reconciliation** | v2.2 已重新套用至 100,827-byte Drive 權威底稿；三處重疊已裁決 | 不再構成同步 blocker；本檔可作 v2.2 Drive/GitHub canonical manuscript |

---

# 附錄 C　v2.0 → v2.1 修訂紀錄

| 部分 | 處理 | 說明 |
|---|---|---|
| 題名、研究邊界（企業層級） | A 保留 | 沿用 v2.0 |
| 摘要 | C 取代 | 加入收斂結果、模型比較量與命題 |
| 1.2 前階段證據 | B 修訂 | 加入 V5 網絡計數（120 格、M = 2,180、47 → 32、16／16），並完成 `6,499 → 3,125 → 783 → 2,180` lineage reconciliation；移除舊版作者待決標記 |
| 1.3 研究缺口 | C 取代 | 改為「文獻破碎 → G01–G16 → 介面 → 企業耦合 → 數學模型需要」四步論證 |
| 1.4–1.5 目的與 RQ | B 修訂 | RQ 改寫為五題並對應 Q1–Q8 |
| 第貳章 | C 取代 | 由 7 節改為 8 節，每節採「主張／支持／不支持／意涵」結構；新增治理、流程、評估、共享能力、多層決策文獻 |
| 第參章 | C 取代 | 由質性設計擴充為完整數學模型、求解程序與不確定性分類 |
| 構念 D、R、G | B 修訂 | 改為由企業決策 `y`、`γ` 決定的門檻鍵 |
| 構念 S、C | 不新增 | 見 3.4 |
| 部門目標 | C 取代 | 由成本最小化改為帳本界定的 (OBJ-U)；舊式為特例 |
| VoC、ReuseValue | C 取代 | 改為 DL、VSC，並新增 VCP、NEV、VG |
| 第肆–陸章 | 新增 | 結果、討論、結論骨架 |
| 參考文獻 | B 修訂 | 保留 6 篇既有引文；新增 34 項來源，書目已核對，但 Teece (1986) 的 DOI 為推定、McFarlan (1981) 卷期頁僅見於二手來源，主張層級的驗證狀態見附錄 A |
| Phase F 稽核修訂 | B 修訂 | 依對抗式稽核修正 P1、P4、P6、P7（新增 P8）、Lemma R 適用範圍、重用表索引、預算含營運支出、現況基準、新增 Model C0 與 VRA／DL0、設計反應不可行狀態，以及摘要與文獻敘述的強度（42 §19） |


---

# 附錄 D　v2.1 → v2.2 修訂紀錄

分類：A 保留、B 修訂、C 取代。

| 部分 | 處理 | 說明 |
|---|---|---|
| 題名、研究問題、第貳章理論架構 | A 保留 | 未變；2.1、2.2、2.6 只依 57 更新引文強度 |
| 摘要（中、英） | B 修訂 | 加入 AI pilot 爭議格、C 中 `δ` 非單調、v2.2 synthetic 驗證的界線 |
| 1.2 前階段證據 | B 修訂 | 以 49 號文件的 lineage（`6,499 → 3,125 → 783 → 2,180`、`qwen2.5:14b`）取代待決註記 |
| 3.4 Gap-to-Mechanism | B 修訂 | 新增 G04、G10、G11 的爭議與 mapping-only 判定 |
| 3.10 P4 | B 修訂 | C 中 `δ` 的集合值建置區域 |
| 3.11 求解程序 | B 修訂 | Lemma E′；(F5e)；缺值作用範圍；`λ` 盒檢查；DP 上下界與退回列舉 |
| 3.12 不確定性 | B 修訂 | registry 驗證與承諾；四類可行性；MaxRegret 精確性；VOI 雙版本；元素層級涵蓋率 |
| 3.13 V0–V7 | B 修訂 | V1 預先登記判準與 pilot 狀態；V3–V6 改為「COMPLETE（僅合成）」 |
| 4.1、4.2 | B 修訂 | 新增 AI pilot（標示為 pilot）；人類結果仍為 `[EMPIRICAL RESULT PENDING]` |
| 4.5 | B 修訂 | 加入 v2.2 合成檢查；移除「尚未完成」清單 |
| 4.3、4.4、4.6–4.10、第伍–陸章 | A 保留 | 仍為骨架；無任何虛構結果 |
| 5.10 | B 修訂 | 以 parity 敘述取代待決註記 |
| 參考文獻、附錄 A | B 修訂 | 依 57 更新：Mikalef & Gupta、Sculley、Teece、Shrestha、Kleinert、Ben-Tal、Dempe 改為已核；EU AI 法加註 2026/1744 修正；新增 Cohen (1960)、Krippendorff (2004)、Polit et al. (2007) |
| 附錄 B | B 修訂 | B1–B3 已解決；B4、B5 更新；B11 已完成 Drive 三方 reconciliation，不再是 blocker |


---

# 附錄 E　v2.2 → v2.3 修訂紀錄

| 部分 | 處理 | 說明 |
|---|---|---|
| 第壹–參章、第伍–陸章、摘要 | A 保留 | 未變；3.13 只加一句指向 59–65 的說明 |
| 第肆章 | C 取代 | 改為可執行的回填骨架：每張表都標明來源資料、計算程式、輸出變數、判讀規則與待決條件。4.1、4.2 改為人類 V1 與 EA-X CVI 的格式（AI pilot 保留為對照，不填入人類欄）；4.3、4.4 由 65 的 loader 產出；4.5 原文保留（SIMULATED_ONLY）；4.6、4.7 加入 (AL) 來源分解與 THRESHOLD_MODE 門檻；4.8 加入事前登記的 registry、MaxRegret 與雙版本 VOI；4.9 外部挑戰以另一個登記群組處理；4.10 加入 Q3、Q5、Q6、Q8 子表。沒有填入任何結果 |
| 參考文獻、附錄 A | B 修訂 | McFarlan 改為只引 hbr.org 可核對的元素；新增 Polit & Beck (2006)，只用其方法主張；Landis & Koch 標籤不再報告 |
| 附錄 B | B 修訂 | B4 更新為 v2.3 殘餘清單 |
