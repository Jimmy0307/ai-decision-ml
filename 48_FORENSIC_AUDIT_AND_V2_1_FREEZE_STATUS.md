# Phase F Forensic Audit and v2.1 Candidate Freeze Status

**日期：2026-10-10。** 對象：`41`–`47`。稽核方式：(i) 腳本化的引文、數字與方程標籤核對；(ii) 一位獨立的對抗式審查者（OR／IS 背景設定）全文審閱 41、42、44、46 並以反例檢驗命題；(iii) 修正後重跑 46 全部斷言。本檔記錄每項稽核的發現、處置與剩餘缺口。

---

## 1. Reference Forensics

| 檢查 | 方法 | 結果 | 處置 |
|---|---|---|---|
| 新增來源是否存在 | 兩個獨立檢索代理以出版者頁、DOI、Crossref、RePEc、作者機構庫逐筆核對 38 個候選 | 書目全部存在；Berente et al. 為編輯評論；Mäntymäki et al. 被機構登錄為非同儕審查（**未採用**）；Fountaine et al.（HBR）卷期頁未確認（**未採用**）；Bard (1998)、Fortuny-Amat & McCarl (1981) 未取得主張原文（**未採用**） | 正文只採用 34 項；未取得主張者不引用 |
| 主張是否被來源支持 | 每筆取摘要或出版者摘要短摘，對照正文用語 | 9 項為 PARTIAL（Mikalef & Gupta、Sculley et al.、McFarlan、Teece DOI、EU AI Act 鏡像、Kleinert et al.、Ben-Tal et al.、Dempe、Savage） | 正文加 `[VERIFY]` 或改寫為研究者推論；附錄 A 逐筆標示 |
| 參考文獻與內文互相對應 | 腳本比對（姓氏＋年份） | 初版缺 Wiesemann et al. (2013) 條目 | 已補 |
| 出版者行銷數字 | 人工檢查 | Weill & Ross (2004) 出版者頁有獲利差異數字 | 正文不引用該數字，只用書名層級概念 |
| 既有引文 | 沿用 `29_CLAIM_LEVEL_SOURCE_AUDIT_v1_5.md` | Shrestha et al. (2019) 卷期頁缺 | 附錄 B3 待補 |

## 2. Provenance Audit

| 檢查 | 結果 |
|---|---|
| 正文是否有任何企業數值 | 無。4.6–4.10 只有 `[EMPIRICAL RESULT PENDING]`（腳本確認該區段無 TWD 或百分比數值） |
| SIMULATED_ONLY 數值是否被誤置 | 只出現在 4.5 節與 47 號紀錄，並逐處標示 |
| 外部效果量（handoff 05 §B 的約 15%、約 37%） | 未在 41–46 任何處使用；43 只規定其可作 `PUB` 區間端點 |
| G01–G16 統計是否進入模型 | 否；只出現在 41 的 `Network_Evidence` 欄與 44 的 1.2 節 |
| 缺值是否補 0 | 規格禁止；46 原版有預設值補缺（Allow、chargeback、中央出資比例），已改為嚴格查表 |
| 外部評估者 | 只作參數界定與 face-validity 挑戰；不是決策者（42 §1.2、43 §4、44 4.9） |

## 3. Numerical Reproduction Audit

| 數字 | 來源 | 核對 |
|---|---|---|
| 41 表中 16 格的 Observed、E、O/E、四個 q 值、AI／Decision family | `02_G01_G16_FROZEN.csv`（handoff） | 腳本逐格比對，全部一致（G07 的 q_raw `.0290` 與 CSV `0.029` 僅格式差） |
| handoff CSV vs repo `11_…csv` | 數值欄逐格比對 | 無差異 |
| 120 格、M = 2,180、47 → 32、16／16、3,125 vs 2,180 | 專案 V5 規則 | 44 1.2 節一致 |
| 語料 lineage（handoff 01 §3） | **已調和** | V5 正式鏈為 6,499 strict-frame records → 3,125 fully mapped / pair-eligible semantic records → 2,180 document-level deduplicated edges；V5 Stage 2 使用 `qwen2.5:14b` constrained double-pass。handoff 的 404／2,425／GPT-5.6 Sol 保留為 predecessor provenance，不作 V5 network denominator。 |
| 4.5 節合成結果 | 47 號紀錄 | 與重跑輸出一致 |

**未來可重算性：** 所有 headline 量（VRA、DL0、VCP、VSC、DL、NEV、VG 分解、`F_c^†`、PR_X、VRG）皆由 42 的方程與 43 的參數表唯一決定，並由 46 的同名函數計算；任何實證值必須附 `Θ_g` 登記雜湊與參數 provenance 摘要（42 §18）。

## 4. Model Semantics Audit

對抗式審查列出 15 項發現；腳本與 46 的反例重現了其中 4 項。全部處置如下（細節見 42 §19）。

| # | 發現 | 嚴重度 | 狀態 |
|---|---|---|---|
| 1 | P7（`RE ≤ 0`）在 Model C 不成立（要求可篩選不對齊部門） | HIGH | **已修**：P7 限於 B；新增 P8；46 加反例測試（`F^C` 10 → 15） |
| 2 | Lemma R 對決策元素與 Model C 不精確 | HIGH | **已修**：限定適用範圍；元素層級改為充分條件＋列舉 |
| 3 | 以可用與否為索引的重用表使 `δ^†` 非唯一 | HIGH | **已修**：改以來源為索引；46 掃描 8 seeds 單調 |
| 4 | P1 漏治理成本條件 | MEDIUM | **已修**；46 強制 `NOT_COMPARABLE` |
| 5 | 現況基準移動；既有能力成本處理 | MEDIUM | **已修**：`ȳ^cur` 基準、`y − y^cur` 增量 |
| 6 | `G_j(γ)` 誤列為要求 | MEDIUM | **已修**：歸賦能區塊 |
| 7 | 設計 portfolio 在實際反應下不可行 | MEDIUM | **已修**：新狀態碼 |
| 8 | 營運支出不在預算內 | MEDIUM | **已修**：`a^BUD` 含增量營運支出 |
| 9 | VCP 語義混合重分配與對齊 | MEDIUM | **已修**：新增 C0、VRA、DL0 |
| 10 | 實作以預設值補缺 | MEDIUM | **已修** |
| 11 | 正文過度宣稱（收斂結果、證明、「破碎」） | MEDIUM | **已修**：摘要與 1.3 改寫 |
| 12 | `k=0` 處理不一致 | LOW | **已修** |
| 13 | P6 期間敘述錯 | LOW | **已修** |
| 14 | 「唯一根」、Lemma E「等於」 | LOW | **已修** |
| 15 | 文獻強度超過附錄 A | LOW | **已修**：`[VERIFY]` 與改寫 |

其他語義檢查（腳本）：41–45 無 `0.4A`、`κ×A`、`/(1+H…)`、跨構念加總等禁用式；無「證明了企業…」「導致…」等因果用語。

## 5. Method Chain Audit（Gap → construct → parameter → equation）

| 檢查 | 結果 |
|---|---|
| 41 §6 每個 gap 的方程標籤是否存在於 42 | F1–F10、R1、R2、X1、V1、V2、OBJ-E、OBJ-U、D1、D2 皆存在；原 `(OUT)` 標籤不存在，已改指向 42 §18 |
| `EA^cap` 是否在 42 定義 | 原未定義，已在 `Pre(j,k)` 說明中定義 |
| 每個 42 參數是否在 43 有識別列 | 是；新增 `y^cur` 與以來源為索引的 `δ` |
| 16 個 gap 是否都有明確命運 | 是：12 static（含 bridge／conditional）、1 optional、2 dynamic、1 evidence-only、0 excluded |
| 機制支持與模型元素存在理由是否分開陳述 | 是（41 §7、44 3.4） |

## 6. Algorithm Consistency Audit（42 ↔ 44 第三章 ↔ 46）

| 項目 | 狀態 |
|---|---|
| (F2)–(F4)、(F5a–d)、(F6)–(F10)、(R1′)、(R2)、(X1)、(V1)、(V2)、(OBJ-E)、(OBJ-U) | 46 與 42 逐條一致（含 `k=0`） |
| (F5e) 資料／介面門檻 | **46 未實作**（45 T-ALG-1 PENDING） |
| Model A、C0、A+、B、C 與比較量 | 一致；Model D 未實作（預設不執行） |
| Lemma E | 一致（含 Pareto 篩選）；以整數網格對照通過 |
| Lemma R、robust feasibility、MaxRegret、VOI、DP 背包 | **46 未實作**（45 PENDING） |
| 44 第三章與 42 的符號 | 修訂後一致；44 為 42 的摘要版，衝突時以 42 為準 |

---

## 7. v2.1 Candidate Freeze 狀態

### 7.1 可凍結（v2.1 candidate）

- G01–G16 → I1–I4（M1–M4）＋ M5 ＋ optional ＋ evidence-only 的收斂（研究者裁決；V1 待驗）。
- 五族構念架構；不新增 S、C；D、R、G 改為由企業決策決定的門檻鍵；`G_j(γ)` 為 permission level。
- Enterprise–Business Unit 雙層、envelope 協調、帳本界定的部門目標、`ρ` 內嵌的使用者層與第三層觸發測試。
- 帳本單一歸屬規則、增量目標、共享成本只計一次、來源索引的重用表、預算含營運支出。
- 組織型態 A、C0、A+、B、C（D 條件）與比較量 VRA、DL0、VCP、VSC、DL、NEV、VG（EE／RE／CE）、`F_c^†`、`δ^†`、PR_X、VRG。
- 命題 P1–P8、Lemma E；Lemma R 的限定版本。
- 缺值狀態碼與 `Θ_adm` 分類規則。

### 7.1a 本輪已額外解除的 blocker

- **Corpus lineage reconciliation：RESOLVED。** V5 正式 methods denominator 分層固定為 6,499 → 3,125 → 2,180；`qwen2.5:14b` 為 V5 Stage 2 constrained double-pass mapping model。早期 404／2,425／GPT-5.6 Sol lineage 僅作 predecessor provenance，不再標 `[AUTHOR DECISION REQUIRED]`。
- corpus-parity 限制仍保留：AI 與 Decision 兩軌的全文覆蓋不對稱，因此 network depletion 只作 research lead，不能把其幅度當 enterprise coefficient。

### 7.2 不可凍結

- V1 盲編與 EA-X 內容效度；任何企業參數；`Γ` 的實際替代方案；帳本拆分；V0、V2、V7。
- 46 的 PENDING 項（Lemma R、robust feasibility、MaxRegret、VOI、DP、(F5e)、typed units、狀態碼輸出）。
- 附錄 A 中 PARTIAL 引文的原文核對。

### 7.3 模型目前已能給出的條件性回答（非實證）

| 研究命題 | 模型內的條件性回答 |
|---|---|
| Q1 | 企業協調架構的淨價值 `NEV = VRA + DL0 + VSC − DL`；前三項恆非負，只有 DL 可使 NEV 為負，而 DL 只在帳本不對齊且 envelope 無法分離時為正。 |
| Q2 | 每項共享能力有唯一的損益兩平固定成本 `F_c^†`；在集中規劃下，以來源為索引的共享重用效果也有唯一門檻。共享不預設較便宜。 |
| Q3 | 治理的模型內正價值只來自賦能、穩健可行，以及雙層不對齊時的篩選；在集中規劃下，要求本身只有成本。 |
| Q4 | 局部最適只在 (AL1)–(AL4) 至少一項不成立時偏離企業最適，且需 envelope 無法阻擋該偏離。 |
| Q5 | H、WI、EA 高於要求只在查表顯示淨效益時被選；要求是否必要，以 robustness-protective 或 screening 判定，而不是「越多越好」。 |
| Q6 | 設計反應與實際反應的價值差（VRG）可正可負；以設計假設做決策的代價恆非負；設計可能在實際反應下不可行。 |
| Q7 | 只能在企業參數與 `𝒢` 登記後回答。 |
| Q8 | 一個 gap 是否「成為企業決策問題」取決於其介面元素在最適解中是否綁住或改變；這是實證結果，不由網絡統計推定。 |

**結論：** 41–47 達到 v2.1 candidate freeze 的標準（理論收斂、構念、模型、識別規格、正文前三章與結果骨架、合成實作一致性）；實證層級（V0、V1、V2、V7）全部 OPEN，任何 Chapter 4 實證段落都尚不能撰寫。
