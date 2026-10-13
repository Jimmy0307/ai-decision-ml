# 122 工程／外部採購模型規格 v1.1（ENGINEERING / SOURCING MODEL SPEC）

> 日期：2026-10-13｜狀態：SPEC CANDIDATE｜數學定義以 119 §11–§16 為準；本檔是操作規格與資料需求。
> 參考實作：`124_engineering_sourcing_model_reference.py`；執行紀錄：`125_ENGINEERING_SOURCING_MODEL_RUN_v1_1.txt`；數值例子：`123_ENGINEERING_SOURCING_SYNTHETIC_EXAMPLE_v1_1.xlsx`。
> **本檔所有數字均為 `SIMULATED_ONLY`**：手工設計的合成實例，不是企業資料，也不是實證結果。`ENTERPRISE_EMPIRICAL_STATUS = PENDING`。

## 1. 這個面回答什麼

1. 哪些 AI initiative／配置值得做？（portfolio 在工程稀缺下的最適解）
2. 哪些共享能力值得建？（共享能力本身的技能別工程需求已計入）
3. 工程工作由內部、外部或兩者承擔？（BUILD／BUY／HYBRID／NONE，由最適解推導）
4. 最適 AI 工程人數 `n^*`（`argmax F_E^*(n)`）。
5. 第幾位工程師的淨邊際價值開始為負？（只作診斷；不等於 `n^*`。報告「第一個使 `MV^{net}(n+1) < 0` 的 `n`」，也就是第 `n+1` 位工程師）
6. 外部顧問何時比增聘划算？（顧問費率、retainer 與需求量的掃描）
7. 中央池化工程相對部門分隔工程的價值 `V^{ENG_POOL}`。

## 2. 決策與參數一覽

| 元素 | 符號 | 型別／單位 | 決定者 |
|---|---|---|---|
| 內部 FTE（含現有） | `n_w ≥ n^{cur}_w` | 整數 | 企業（B、A+；C、C0 的 leader） |
| 外部有效工程容量 | `K^{ext}_w` | hours/period ≥ 0 | 企業 |
| retainer 啟用 | `χ_w` | binary | 企業 |
| 技能 | `w ∈ W^{ENG}` = AI_LLM、DATA、MLOPS_PLATFORM、INTEG | nominal（AUTHOR_DEFINED_OPERATIONAL_CATEGORY） | — |
| 有效容量 | `K^{int}_w(n)`；線性特例 `n Q^{nom}_w η_w` | hours/period | — |
| fully-loaded 成本 | `C^{int}_w(n)`；線性特例 `n ν^{FTE}_w` | TWD/period | — |
| 外部成本 | `F^{ext}_w χ_w + ν^{ext}_w K^{ext}_w`，`K^{ext}_w ≤ K̄^{ext}_w χ_w` | TWD/period | — |
| 工程預算 | `Σ_w [ΔC^{int}_w + C^{ext}_w] ≤ B̄^{ENG}` | TWD/period | — |
| 需求 | `a^{ENG,w}_{jk}(s)`、`a^{ENG,w}_c`、`a^{ENG,w,loc}_{uc}` | effective hours/period | — |

## 3. 有效容量

- **canonical：** `K^{int}_w(n)` 是 `n` 名內部人員每期可提供的**有效專案工時**，扣除休假、訓練、非專案工作與協調損耗；由 HR 紀錄、專案工時紀錄或專家引出估計。
- **LINEAR CAPACITY SPECIAL CASE：** `K^{int}_w(n) = n Q^{nom}_w η_w`。不是 canonical truth；`η_w` 不得任意指定實證值，只能由工時紀錄或引出取得，否則以區間表示。
- 工程需求必須以同一個「有效工時」單位表示，與容量一致。外部人員的有效工時若與內部不同（例如熟悉度差異），差異只能反映在 `a^{ENG,w}`（需求）或交付型價格中，不得加分。

## 3A. Planning-time regime（v1.1 RC）

- **`IMPLEMENTATION_YEAR` = canonical staffing baseline。** 容量需求用完整 BUILD 工時 + 當期 RUN 工時；一次性建置工時不因金融年金因子而縮小。它回答「導入年度需要幾位工程師／多少顧問容量？」
- **`STEADY_STATE_LEVELIZED` = sensitivity only。** BUILD 工時以 `AF(r_d,H)` levelize 後再加 RUN，只表示穩態專案流的長期平均容量；不得作為建置年尖峰或實體容量可行性的證據。
- **financial annualization ≠ physical capacity annualization。** 貨幣成本仍可年化；physical BUILD hours 在 canonical implementation-year constraint 中全額進入。

**單技能退化（single-skill collapse）。** 若 `|W^ENG|=1`，需求與容量與 06 單一 ENG 資源逐項一致且外部容量為 0，則 `SKILL_FIXED` 必須與 `PLANE_OFF` 完全一致；124 acceptance test 17 檢查 B、A+、C(opt/pess)、C0(opt/pess)、A(opt/pess)。

**比較量名稱鎖定：** `PLANE_OFF` 才可使用原 06 名稱（VSC、VCP、DL、NEV 等）；`SKILL_FIXED` 一律使用 `VSC^{W,fix}` 等技能別標記；`ENDOGENOUS` 一律使用 `VSC^{ENG}` 等 ENG 標記。跨 regime 不得直接把數值變化解讀為同一制度的 improvement。

## 4. fully-loaded 成本

`C^{int}_w(n)` 可包含：薪資、福利、招募、到職、設備與基礎設施、管理費攤提。只在有資料時填值；各項的唯一帳本位置見 121。目標函數只計增量 `ΔC^{int}_w = C^{int}_w(n_w) − C^{int}_w(n^{cur}_w)`：現有人員的成本在 06 中是沉沒成本，不在 OBJ-E 中。

## 5. 外部容量與 retainer

- 容量型外部採購（按人時、月租、dedicated external engineer、購買的工程容量）只出現在 `C^{ext}_w`，消耗 `B̄^{ENG}`，不得再進 `C^{impl}`。
- 交付型固定合約（SI 固定總價、vendor 固定專案費、一次性移轉套件）不記工時，只出現在 `C^{impl}_{jk}` 或 `F_c`，消耗 `B̄`。
- retainer `F^{ext}_w` 是啟用時的固定成本；分段價格保留下一階段。
- 外部夥伴不是 optimizer：模型沒有外部的目標函數；含外部目標的輸入（例如 `vendor_objective`）一律拒收（124 測試 10）。

## 6. 邊際成本與邊際價值

| 量 | 定義 | 注意 |
|---|---|---|
| `MC^{int}_w(n+1)` | `[C^{int}(n+1) − C^{int}(n)] / [K^{int}(n+1) − K^{int}(n)]` | 分母 0 → UNDEFINED |
| `MC^{ext}_w` | `ν^{ext}_w`（線性） | retainer 不是邊際成本 |
| `V^{gross}_w(n)` | `F_E^*(n) + ΔC^{int}_w(n_w)` | 其餘變數重新最適化 |
| `MV^{gross}_w(n+1)` | `V^{gross}_w(n+1) − V^{gross}_w(n)` | 容量解開的價值 |
| `MV^{net}_w(n+1)` | `F_E^*(n+1) − F_E^*(n) = MV^{gross} − ΔC^{int}_{step}` | 恆等式精確成立 |
| `n^*` | `argmax_n F_E^*(n)` | 整數 portfolio → 非凹；「第一個負 MV」只作診斷 |

## 7. BUILD／BUY／HYBRID／NONE

由最適解逐技能推導（相對 `n^{cur}_w`）：BUILD = 增聘且無外部；BUY = 不增聘且有外部；HYBRID = 兩者皆有；NONE = 兩者皆無。不是決策變數，不轉成分數。組織 archetype（O1–O5）與採購方式分開；O4 不等於 BUY。

## 8. 工程池化

`V^{ENG_POOL} = F^{B,ENG}(\text{pooled}) − F^{B,ENG}(\text{BU-separated})`。部門分隔的反事實：每個部門自己的人力（`n_{uw} ≥ n^{cur}_{uw}`）、自己的固定容量（`K^{fix}` 的分割）、自己的外部採購與 retainer、自己的容量限制；外部市場的可得容量全企業共用；共享能力的工程量由承載部門負擔（AUTHOR_DEFINED_HOSTING_RULE）。在線性容量與成本、現有人力與固定容量為分割、外部可得容量共用的條件下 `V^{ENG_POOL} ≥ 0`（119 P-POOL）；條件不成立時可能為負，不得一般化。不與 VCP、VSC、DL、NEV 合併或分解。

## 9. 求解（OPTION 2）

外層列舉人力向量 `n`（從 `n^{cur}` 到預算隱含的上界 `n^{cur}_w + ⌊B̄^{ENG}/ν^{FTE}_w⌋`，因此網格完整）；內層以既有的 portfolio 問題求解，外部採購取成本最小的 `max(0, D_w − K^{fix}_w − K^{int}_w(n_w))`。C、C0 中 Lemma E′ 在付費容量下仍成立（119 §14.2）。單一技能且工程面停用時，51 可作為內層求解器；多技能只在 124 實作。

## 10. 合成例子（SIMULATED_ONLY）

**實例：** 2 個事業單位（U1 業務、U2 營運）、4 個 initiative（J1 報價草稿助理、J2 客戶郵件分流、J3 需求預測、J4 供應商文件擷取）、每個 3 種配置（k0 現況、k1 輔助、k2 有界執行）、2 個共享能力（C_LLM 共用 LLM 服務、C_DATA 資料平台）、3 種技能（AI_LLM、DATA、INTEG）。現有人力 AI_LLM 0、DATA 1、INTEG 1；有效工時 1,350 h/FTE（1,800 × 0.75）。金額單位 kTWD/年。J2 的 k1 由 SI 固定總價交付（交付型，工時 0）。所有數值都是為了展示機制而手工設定的，**不是**任何企業的估計。

### 10.1 五個情境（Model B）

| 情境 | F_E^* | 選定的 AI 配置 | 共享能力 | n（AI_LLM／DATA／INTEG） | K^ext（同序，h） | ΔC^int | C^ext | 採購方式（同序） |
|---|---|---|---|---|---|---|---|---|
| 1a 只用現有人力（工程面停用，06：技能可互相替代） | 10,709.9 | J1:k1、J2:k1、J3:k1 | C_LLM | 0 / 1 / 1 | 0 / 0 / 0 | 0.0 | 0.0 | — / — / — |
| 1 只用現有人力（技能別、不可替代） | 6,982.8 | J2:k1、J3:k1 | — | 0 / 1 / 1 | 0 / 0 / 0 | 0.0 | 0.0 | NONE / NONE / NONE |
| 2 可增聘內部 | 9,848.4 | J1:k1、J2:k2、J3:k1、J4:k1 | C_LLM | 2 / 1 / 2 | 0 / 0 / 0 | 7,100.0 | 0.0 | BUILD / NONE / BUILD |
| 3 只用顧問 | 9,199.3 | J1:k1、J2:k1、J3:k1、J4:k1 | C_LLM | 0 / 1 / 1 | 1,600 / 0 / 0 | 0.0 | 5,270.0 | BUY / NONE / NONE |
| 4 混合（內部＋外部） | 11,367.2 | J1:k2、J2:k2、J3:k1、J4:k1 | C_LLM | 2 / 1 / 2 | 200 / 0 / 0 | 7,100.0 | 790.0 | HYBRID / NONE / BUILD |
| 5b 部門分隔工程（對照 5a = 情境 4 的中央池化） | 9,507.2 | J1:k2、J2:k2、J3:k1、J4:k1 | C_LLM | 2 / 1 / 2 | 400 / 200 / 150 | — | 工程成本合計 9,750.0 | — / — / — |


- `V^{EXT}`（混合 − 只能內部）= 1,518.8；人力固定在現況時 = 2,216.5。
- `V^{ENG_POOL}`（中央池化 − 部門分隔）= 1,860.0：部門分隔時，各部門的零碎需求要各自付 retainer 或各自聘人。
- 現有人力下 AI_LLM 為 0，所有需要共用 LLM 服務的配置都不可行；只有 J2:k1（交付型）與 J3:k1 被選上。

### 10.2 人數曲線：AI_LLM（其他技能固定在情境 4 的最適值）

| n_AI_LLM | 狀態 | F_E^* | V^gross | ΔC^int | C^ext | MV^gross | MV^net | MC^int（下一人，kTWD/h） | 使用率 | 選定配置 |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | OPTIMAL | 7,927.2 | 7,927.2 | 0.0 | 9,430.0 | — | — | 1.93 | 1.00 | J1:k2、J2:k2、J3:k1、J4:k1 |
| 1 | OPTIMAL | 9,647.2 | 12,247.2 | 2,600.0 | 5,110.0 | 4,320.0 | 1,720.0 | 1.93 | 1.00 | J1:k2、J2:k2、J3:k1、J4:k1 |
| 2 | OPTIMAL | 11,367.2 | 16,567.2 | 5,200.0 | 790.0 | 4,320.0 | 1,720.0 | 1.93 | 1.00 | J1:k2、J2:k2、J3:k1、J4:k1 |
| 3 | OPTIMAL | 9,557.2 | 17,357.2 | 7,800.0 | 0.0 | 790.0 | -1,810.0 | 1.93 | 0.72 | J1:k2、J2:k2、J3:k1、J4:k1 |
| 4 | INFEASIBLE (B-bar^ENG or capacity) | — | — | 10,400.0 | — | — | — | 1.93 | — | — |


`n^*` = 2；第一個使 `MV^{net}(n+1) < 0` 的 `n`（診斷）= 2，即第 3 位 AI_LLM 工程師的淨邊際價值為負。`n = 0` 時所有 AI_LLM 工時都向外採購；第 1、2 位內部工程師以較低的每工時成本取代外部工時（淨邊際價值為正）；第 3 位使容量閒置，淨邊際價值為負。預算 `B̄^{ENG}` 使更多人力不可行。

### 10.3 顧問費率掃描（所有技能的 `ν^{ext}` 同乘一個倍數）

| ν^ext 倍數 | F_E^* | n | AI_LLM | DATA | INTEG |
|---|---|---|---|---|---|
| 0.25 | 16,097.2 | 0 / 1 / 1 | BUY | NONE | BUY |
| 0.4 | 14,381.2 | 0 / 1 / 1 | BUY | NONE | BUY |
| 0.55 | 12,665.2 | 0 / 1 / 1 | BUY | NONE | BUY |
| 0.7 | 11,797.2 | 2 / 1 / 1 | HYBRID | NONE | BUY |
| 0.85 | 11,463.2 | 2 / 1 / 2 | HYBRID | NONE | BUILD |
| 1.0 | 11,367.2 | 2 / 1 / 2 | HYBRID | NONE | BUILD |
| 1.25 | 11,207.2 | 2 / 1 / 2 | HYBRID | NONE | BUILD |
| 1.5 | 11,047.2 | 2 / 1 / 2 | HYBRID | NONE | BUILD |
| 2.0 | 10,727.2 | 2 / 1 / 2 | HYBRID | NONE | BUILD |
| 3.0 | 10,087.2 | 2 / 1 / 2 | HYBRID | NONE | BUILD |


### 10.4 專案量掃描（「專案量到多少時，聘專職 AI 工程師才合理？」）

| pipeline（納入的 initiative） | 混合：n | 混合：採購方式（AI_LLM／DATA／INTEG） | 只能內部：n | 混合：選定配置 |
|---|---|---|---|---|
| J3 | 0 / 1 / 1 | NONE / NONE / NONE | 0 / 1 / 1 | J3:k1 |
| J3、J1 | 1 / 1 / 1 | HYBRID / NONE / NONE | 1 / 1 / 1 | J1:k2、J3:k1 |
| J3、J1、J4 | 1 / 1 / 1 | HYBRID / NONE / NONE | 2 / 1 / 2 | J1:k1、J3:k1、J4:k1 |
| J3、J1、J4、J2 | 2 / 1 / 2 | HYBRID / NONE / BUILD | 2 / 1 / 2 | J1:k2、J2:k2、J3:k1、J4:k1 |


（每一列只保留列出的 initiative；被移除部門的現有人力併入保留的部門。）只有 J3（資料類、不需 LLM）時不需要任何 AI_LLM 人力；加入 J1 後，最適解聘 1 位 AI_LLM 並向外補足；四個 initiative 全部納入時聘 2 位並少量外購。這些門檻只屬於這個合成實例。

### 10.5 A／B／C 的三種制度（SIMULATED_ONLY）

- PLANE_OFF（06：技能合併為單一池化工程資源）：B = 10,709.9、A+ = 6,982.8、C（opt／pess）= 10,709.9／10,709.9、C0 = 6,982.8、A = 6,982.8；06 比較量 VSC = 3,727.1、VCP = 0.0、DL = 0.0、NEV = 3,727.1。
- SKILL_FIXED（技能別、人力固定）：B = 6,982.8、A+ = 6,982.8、C = 6,982.8、A = 1,501.1；`VSC^{W,fix}` = 0.0、`VCP^{W,fix}` = 5,481.7。與 PLANE_OFF 的差異完全來自技能不可替代：現有人力沒有 AI_LLM，共享 LLM 服務在技能別限制下建不起來，但在 06 的合併限制下可以由資料與整合人員的工時「支付」。
- ENDOGENOUS：B^ENG = 11,367.2、A+^ENG = 6,982.8、C^ENG（opt／pess）= 11,367.2／11,367.2；`VSC^{ENG}` = 4,384.4、`DL^{ENG}` = 0.0；A：NOT_COMPARABLE。
- 本實例的帳本大致對齊（只有 J2:k2 有很小的外部帳本項），所以 C = B（P2／P2-ENG 的預期）。

## 11. 需要的企業資料

| 資料 | 欄位 | 來源 | provenance | 缺值規則 |
|---|---|---|---|---|
| 現有人力 | `n^{cur}_w`、`n^{cur}_{uw}`（依部門） | HR 名冊、組織圖 | OBSERVED | 缺 → 工程面不求解（`REJECT_INSUFFICIENT_IDENTIFIED_INPUTS`） |
| 有效容量 | `Q^{nom}_w`、`η_w` 或 `K^{int}_w(n)` | 工時紀錄、專案系統 | OBSERVED／EXPERT_ELICITED | 只有區間 → 區間求解；不得補預設 `η` |
| fully-loaded 成本 | 薪資、福利、招募、到職、設備、管理費 → `C^{int}_w(n)` | HR、財務 | OBSERVED | 缺 → 報人力的損益兩平成本，不輸出 `n^*` |
| 外部價格 | `ν^{ext}_w`、`F^{ext}_w`、價格分段 | 合約、報價 | OBSERVED／PUBLIC_OBSERVED | 缺 → 外部採購停用並註明，或報損益兩平費率 |
| 外部可得容量 | `K̄^{ext}_w` | 供應商回覆、市場詢價 | EXPERT_ELICITED | 缺 → 區間；不得以 big-M 代替 |
| 工程需求 | 每個 `(j,k,s)` 與每個能力的容量型工作包（技能別工時）；交付型工作包（固定價格） | 專案估算、過去專案紀錄 | EXPERT_ELICITED／OBSERVED | 缺 → 只排除該 `(j,k,s)`（`RESTRICTED_SOLVE`） |
| 工作包類型 | CAPACITY／DELIVERABLE | 合約條款 | OBSERVED | 不明 → 該工作包不得計價，配置排除並列出 |
| 工程預算 | `B̄^{ENG}`；並把 `B̄` 中的容量型工程費用移出（119 §11.6 預算資料規則） | 預算文件 | OBSERVED | 缺 → 報資源—價值前緣 |
| Planning-time inputs | BUILD／RUN 工時分開；`IMPLEMENTATION_YEAR` 用完整 BUILD+RUN；`H_j`、`H_c`、`r_d` 只供 `STEADY_STATE_LEVELIZED` 敏感度與貨幣年化，`H^{ten}_w` 供一次性人員成本年化 | 專案估算、HR、財務 | OBSERVED／ELICITED | canonical BUILD/RUN 缺 → 區間／排除；levelized 參數缺 → 不跑該敏感度 |
| 組織調度權 | `D07`、`D07a`（誰調度外部產能） | ORG-V 編碼（107–117） | AUTHOR_DEFINED（待人類驗證） | 事業單位調度 → C-ENG-LOCAL（未定義） |

## 12. 假設與限制

見 119 §17（A-ENG-01 至 A-ENG-12）與 §18。合成例子另有兩點限制：只有一個 policy `γ`，且沒有審查容量 (R2) 的資料，因此 (R2) 與治理選擇在 124 的合成例子中沒有被檢驗（124 的回溯一致性檢查使用 51 的實例，涵蓋多個 policy 與 (R2)）。需求規模掃描中 `B̄^{ENG}` 固定、`B̄` 隨規模放大，因此人數不必隨規模單調增加。尤其：技能不可替代、線性容量與成本只是特例、不允許減少既有人力、代表性年化期間、單期模型沒有招募延遲與學習、工程不確定因子尚未進入穩健性登錄表、所有例子 SIMULATED_ONLY。
