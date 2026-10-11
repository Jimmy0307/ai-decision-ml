# Parameter Identification and Quantification v2.1

**狀態：v2.1 candidate，2026-10-10。** 本檔回答「模型要成立，需要量到什麼」，而非「找誰回答」。結構依 `42_ENTERPRISE_PORTFOLIO_MODEL_v2_1.md` 的方程區塊組織。所有參數目前的 provenance 均為 `UNIDENTIFIED`；本檔只界定識別要求、單位與缺值後果。

---

## 0. 識別判準

| 代碼 | 意義 | 可進 point solve | 可進 interval solve |
|---|---|---|---|
| **OBS** | 可由企業文件、系統紀錄、會計／預算紀錄直接觀察 | 是 | 是 |
| **EXP** | 可由具相關職責者以區間引出（內部；或外部評估者 `source_scope=external`） | 否（除非區間退化且有理由） | 是 |
| **PUB** | 可由公開資料界定上下界（薪資、雲端價格、法規、文獻效果量） | 否 | 是（僅作界） |
| **SCN** | 只能作預先登記的情境值 | 否 | 是（標 SCENARIO_SENSITIVITY） |
| **DEF** | 定義性（由模型或程序文件決定，非估計） | 是 | 是 |

**外部效果量規則：** 文獻或產業報告的生產力效果（例如客服、寫作實驗中的時間節省）只可作 `t`、`v` 的 `PUB` 區間端點，且必須另附「任務相似性」說明；永遠不得標為 `OBSERVED`，也不得作為 point value。

---

## 1. Parameter Identification Matrix

欄位：Parameter｜Meaning｜Equation（42）｜Required Unit｜Minimum Evidence Needed｜Can Be Observed?｜Can Be Expert-Bounded?｜Can Be Publicly Bounded?｜Scenario-only?｜If Missing → Model consequence

### 1.1 Block E — 企業資源與共享能力（F5）

| Parameter | Meaning | Equation | Required Unit | Minimum Evidence Needed | Can Be Observed? | Can Be Expert-Bounded? | Can Be Publicly Bounded? | Scenario-only? | If Missing → Model consequence |
|---|---|---|---|---|---|---|---|---|---|
| `B̄` (`Ā^BUD`) | 期間 AI 相關可支配預算 | (R1)(R1′) | TWD/period | 核定預算文件或預算區間 | Yes | Yes | No | No | `REJECT_INSUFFICIENT_IDENTIFIED_INPUTS`；可改報「預算—價值前緣」 |
| `Ā^ENG` | 可投入的工程／資料／整合工時 | (R1)(R1′) | hours/period | 人力配置表與既有承諾工時 | Yes | Yes | No | No | 同上 |
| `F_c`, `y^cur_c` | 共享能力 `c` 的期間成本（含攤提）；現況是否已啟用 | (OBJ-E)(R1) | TWD/period；binary | 報價、合約、雲端帳單、內部成本紀錄；一次性與持續分開 | Yes | Yes | Yes（雲端／授權公開價） | No | `THRESHOLD_MODE`：不強制 `y_c=0`；報 `F_c^†` 及 `F_c` 需落在何處才值得建 |
| `a^ENG_c` | 建置／維運 `c` 的工程工時 | (R1) | hours/period | 專案計畫或歷史類似專案工時 | Partly | Yes | No | No | 以區間進 Θ；全無 → `c` 的決策 UNIDENTIFIED |
| `F^loc_{uc}`, `a^{h,loc}_{uc}` | 部門自建本地版成本 | (OBJ-E)(OBJ-U)；Model A/A+ | TWD/period；hours/period | 部門既有或報價的獨立方案成本 | Partly | Yes | Yes | No | Model A／A+ 不可解 → VCP、VSC、NEV 為 UNIDENTIFIED；B、C 照解 |
| `Pre(j,k)` | 配置所需能力前提 | (F4) | relation | 架構文件、IT 依賴圖 | Yes | Yes | No | No | 該 `(j,k)` 不可評估 → `RESTRICTED_SOLVE` |
| `R_j(y)`, `D(y)` | 能力狀態下的資料可得性、介面等級 | (F5e) | ordinal key | 依 41 錨點的文件／系統檢查 | Yes | Yes | No | No | 該 `(j,k)` 可行性未知 → `RESTRICTED_SOLVE` |
| `δ_{jkc}`（由以來源為索引的 `C^impl(s)` 推得） | 共享版能力對局部導入成本的重用效果（本地版另以 `s=L` 的格表示） | (§10) | TWD/period | 有／無共享能力時的導入估算，最好來自已完成專案的對照 | Partly | Yes | No | Often | 以 `[0, δ^U]` 進 Θ；`δ^U` 也無 → 報 break-even `δ^†`；**不得假設 δ>0** |
| `B^0_u`, `K^{ENG,0}_u` | 現況部門 AI 預算與工程容量 | Model A | TWD/period；hours/period | 預算紀錄 | Yes | Yes | No | No | Model A 不可解；`NOT_COMPARABLE` 若總和超過 `Ā` |
| `r_d`, `H_j` | 折現率、攤提期 | (§3.4) | 1/period；periods | 財務政策 | Yes | Yes | Yes | No | 以區間進 Θ；影響所有攤提成本 |

### 1.2 Block G — Policy 與治理（F1／M1）

| Parameter | Meaning | Equation | Required Unit | Minimum Evidence Needed | Can Be Observed? | Can Be Expert-Bounded? | Can Be Publicly Bounded? | Scenario-only? | If Missing → Model consequence |
|---|---|---|---|---|---|---|---|---|---|
| `Γ`（policy 選單） | 企業可選的有限治理方案 | §4.1 | set | 現行政策＋至少一個實際被討論的替代方案；`γ^0` 依法規最低要求界定 | Partly（現行） | Yes | Partly（法規、NIST AI RMF、ISO/IEC 42001 作結構參照） | 替代方案常為 SCN | 只有 `γ^cur` 時，VG 只能報 `γ^cur` vs `γ^0` |
| `Allow_γ(j,k)` | policy 是否允許該配置 | (F3) | binary | 政策條文、授權矩陣 | Yes | Yes | No | 替代方案為 SCN | 該 `(j,k)` 移除 → `RESTRICTED_SOLVE` |
| `Allow^loc_γ(u,c)` | 是否允許部門自建 | §4.2 | binary | IT 採購／架構政策 | Yes | Yes | No | No | 預設不允許會偏向集中；**必須明示**，否則 Model C 標 UNIDENTIFIED |
| `G_j(γ)` | 正式決策權等級 | (F5c) | ordinal key | 授權文件依 41 錨點編碼 | Yes | Yes | No | No | 同 Allow |
| `H^req_γ`, `WI^req_γ`, `EA^req_γ`, `G^req` | `A × κ` 要求表 | (F5a–d) | ordinal key table | 政策條文；若無明文，由治理、IT、流程負責人引出，記錄理由 | Partly | Yes | Partly（法規對高風險系統的人類監督要求可作下界參照，需逐條核對） | No | 缺格的 `(A,κ)` 組合 → 該等級的配置不可評估；**不得以最高或最低要求補值** |
| `ē_j^γ` | 嚴重事件容忍上限 | (F9) | incidents/period | 風險胃納聲明、品質／合規政策 | Partly | Yes（外部評估者可挑戰） | No | Often | (F9) 無法判定 → 相關配置 `RESTRICTED_SOLVE`；不得以 TWD 罰款替代 |
| `J^must_γ`, `J^forbid_γ` | 策略強制／禁止 | (F10)(F3) | set | 董事會或高階決議 | Yes | Yes（外部評估者） | No | 替代方案為 SCN | 視為空集合並**明示**；這是「無策略強制」的情境，不是補值 |
| `Legal_{jk}` | 法規、權利、隱私、安全硬限制 | (F2) | binary | 法務／資安意見、法規條文 | Yes | Yes | Yes（法規文本） | No | 該 `(j,k)` 不可評估 |
| `ΔC^gov(γ)` | 治理營運成本差 | (OBJ-E)(R1) | TWD/period | 委員會工時、稽核成本、文件成本 | Partly | Yes | No | Often | 以區間進 Θ；全無 → VG 的 CE 分量 UNIDENTIFIED，EE 與 RE 照報 |

### 1.3 Block X — 配置空間與流程（M2／M3／M4）

| Parameter | Meaning | Equation | Required Unit | Minimum Evidence Needed | Can Be Observed? | Can Be Expert-Bounded? | Can Be Publicly Bounded? | Scenario-only? | If Missing → Model consequence |
|---|---|---|---|---|---|---|---|---|---|
| `M_j` 與屬性 `(A,H,WI,EA,EAX,m)` | 候選配置列舉 | §2 | ordinal keys + nominal | 現況配置（OBS）＋具技術可行性的替代配置（由 IT 與部門共同列舉） | Partly | Yes | No | 替代配置可為 SCN | 只有現況 → 只能評估 status quo，無最適化可言 |
| `κ_j` | 後果類別 | (F5)(F9) | ordinal class | 依 41 錨點編碼（可逆局部／需跨部門修復／重大客戶、品質或法規後果） | Yes | Yes | No | No | 所有以 `κ` 為鍵的要求無法查 → 該 initiative 不可評估 |
| `Eff_H(j,k)` | 有效控制 | (F6) | binary | 行動前資訊可見性、反應時間、真實否決權的紀錄或觀察 | Yes | Yes | No | No | `H_req ≥ 2` 的配置 `RESTRICTED_SOLVE`；**不得由名義 H 推定** |
| `FB_{jk}` | fallback／rollback | (F7) | binary | 回復程序文件與演練紀錄 | Yes | Yes | No | No | `A ≥ 2` 配置 `RESTRICTED_SOLVE` |
| `O_{jk}`, `Rec_{jk}(ȳ)` | 導入一次性與持續成本 | (V2)(R1) | TWD；TWD/period | 專案估算、合約、內部工時 × 內部費率 | Partly | Yes | Partly | No | 該 `(j,k)` `RESTRICTED_SOLVE` |
| `a^ENG_{jk}(ȳ)` | 工程工時 | (R1) | hours/period | 專案估算 | Partly | Yes | No | No | 同上 |
| `C^{impl,x}_{jk}` | 中央出資部分 | (OBJ-U) | TWD/period | 預算歸屬規則 | Yes | Yes | No | No | `FOLLOWER_LEDGER_UNIDENTIFIED` → Model C 不解 |
| `τ_{jc}` | chargeback | (OBJ-U) | TWD/period | 內部計價規則 | Yes | No | No | No | 若確定無 chargeback，記為「無」（DEF），不是補 0 |
| `N_j`, `N_{jk}` | 事件量；配置相依事件量 | (V2) | events/period | 系統交易／案件紀錄；`N_{jk}≠N_j` 需 throughput 與需求證據 | Yes | Yes | No | `N_{jk}` 常為 SCN | `N_j` 缺 → 該 initiative 不可評估；`N_{jk}` 缺 → 設 `N_{jk}=N_j` 並**明示為假設**（DEF，非補值），另做 sensitivity |

### 1.4 Block R — 角色反應與訊號（M3）

| Parameter | Meaning | Equation | Required Unit | Minimum Evidence Needed | Can Be Observed? | Can Be Expert-Bounded? | Can Be Publicly Bounded? | Scenario-only? | If Missing → Model consequence |
|---|---|---|---|---|---|---|---|---|---|
| `π_j(ℓ|k)` | 角色暴露權重 | (X1) | probability | 工作分派紀錄、案件經手人紀錄 | Yes | Yes | No | No | (X1) 無法計算 → 該 initiative 不可評估 |
| `P_j(z,ω|k)` | 可見訊號 × 隱藏結果 | (X1) | probability | 已部署：系統輸出與事後真值對照（需標記資料）；未部署：基準測試、供應商驗證報告（需任務相似性） | Partly | Yes | Partly | 未部署配置常為 SCN | 該 `(j,k)` `RESTRICTED_SOLVE`；G10 module 不可啟用 |
| `ρ^obs_j(r|k,z,ℓ)` | 已部署配置的實際反應 | (X1) | probability | 系統操作紀錄（接受、修改、退回、升級、繞過）或抽樣觀察；需能對應到可見訊號 `z` | Yes | — | No | No | 以 `ρ^cf` 區間代替並標記 |
| `ρ^cf_j` | 未部署配置的反應 | (X1) | probability（區間） | 盲真值題卡：受測者只看 `z`，不看 `ω`；每列區間正規化可行 | No | Yes | Partly（演算法迴避／偏好文獻只作方向參照，不作數值） | Often | 該 `(j,k)` `RESTRICTED_SOLVE` |
| `ρ^design_j` | 程序設計的反應 | §9.1 | degenerate probability | 作業程序文件 | Yes | — | No | No | Q6（VRG）不可算；若設計 portfolio 在實際反應下不可行 → `DESIGN_INFEASIBLE_UNDER_RESPONSE` |
| `R_k^γ` | 允許反應集合 | (X1) | set | 政策與系統權限 | Yes | Yes | No | No | 預設全允許並明示 |
| `U_ℓ`（Model D） | 角色效用查表 | §9.2 | TWD/event 或序數偏好 | 只在 T1–T5 全過時才需要 | Partly | Yes | No | Often | Model D 不執行（預設） |

### 1.5 Block V — 結果、損失、時間（帳本）

| Parameter | Meaning | Equation | Required Unit | Minimum Evidence Needed | Can Be Observed? | Can Be Expert-Bounded? | Can Be Publicly Bounded? | Scenario-only? | If Missing → Model consequence |
|---|---|---|---|---|---|---|---|---|---|
| `v^u_j`, `v^x_j` | 每事件營收／機會價值（部門帳本／帳本外） | (V1)(OBJ-U) | TWD/event | 交易紀錄、毛利、轉換率；帳本歸屬依 KPI／P&L 文件 | Partly | Yes（外部評估者可挑戰策略價值） | Partly | Often | 該路徑格 UNIDENTIFIED → `RESTRICTED_SOLVE`；若對所有配置相同可作 DEF「不隨配置變」並明示 |
| `l^u_j`, `l^x_j` | 每事件損失（錯誤、重工、延誤、客戶影響） | (V1)(OBJ-U) | TWD/event | 品質成本、退貨、重工紀錄；帳本歸屬 | Partly | Yes | Partly | Often | 同上 |
| `c^u_j`, `c^x_j` | 非人工營運成本（亦進入預算使用 `a^BUD`） | (V1)(R1) | TWD/event | 推論帳單、外部服務費 | Yes | Yes | Yes（公開價格） | No | 同上 |
| `t_j`, `t^REV_j` | 每事件角色工時、審查工時 | (V1)(R2) | hours/event | 工時紀錄、時間抽樣；未部署配置以題卡區間 | Partly | Yes | Partly（外部效果量只作端點） | Often | 同上 |
| `λ_ℓ`, `λ^u_ℓ` | 角色時間的可實現機會價值 | (V1) | TWD/hour | 上界：含負擔薪資（公開或內部薪資級距）；下界 0；中間需證據說明釋出時間的去向 | Partly | Yes | Yes（上界） | No | `PARTIAL_OBJECTIVE`：報 `(F_E^{−time}, ΔHours)`，以 `[0, λ^U]` 分類 |
| `I^sev_j` | 路徑產生嚴重事件的機率 | (F9) | probability | 事故紀錄、品質／合規事件紀錄；未部署以區間 | Partly | Yes | Partly | Often | (F9) 不可判定 → `RESTRICTED_SOLVE` |
| `ΔK̄^REV_u` | 部門可增加的審查工時 | (R2) | hours/period | 排班與人力配置 | Yes | Yes | No | No | (R2) 不可判定 → 以區間或 `RESTRICTED_SOLVE` |
| `s_j`, `s^min_j` | 服務／品質指標與下限 | §8.1 | 指標單位 | 部門 KPI 文件 | Yes | Yes | No | No | 不加入（部門專屬限制必須有證據才加入） |
| `ē^u_j` | 部門問責上限 | §8.1 | incidents/period | 部門績效或問責制度文件 | Partly | Yes | No | No | 不加入 |

### 1.6 Block U — 不確定性設定

| Parameter | Meaning | Equation | Required Unit | Minimum Evidence Needed | Can Be Observed? | Can Be Expert-Bounded? | Can Be Publicly Bounded? | Scenario-only? | If Missing → Model consequence |
|---|---|---|---|---|---|---|---|---|---|
| `𝒢`, `Θ_g` | scenario groups 與可接受集合 | §13 | — | 求解前登記：每組的語義、每參數的區間來源、相依限制 | — | Yes | Partly | Yes | 不登記 → 不得報 ROBUST／CONDITIONAL／FRAGILE |
| `ε_R` | regret 容差 | §13.2 | TWD/period | 預先登記 | — | Yes | No | Yes | 只報 exact（ε=0）分類 |
| `ε_tie` | tie 容差 | §12.3 | relative | 預先登記 | — | — | No | DEF | 預設 `1e-9` 相對 |

---

## 2. 分析別的最小識別集合

並非每個研究問題都需要全部參數。下表列出每個 headline quantity 的**最小**識別需求；不在表中的參數可為 UNIDENTIFIED 而不影響該量。

| 研究問題／計算量 | 必須識別（OBS 或 EXP 區間） | 可為 SCN | 不需要 |
|---|---|---|---|
| Q1 NEV、VCP、VSC | Block E 全部、Block X 全部、Block R 的 `π, P, ρ`、Block V 的 `v, l, c, t`（企業帳本總和即可）、`λ` 區間 | `N_{jk}`、`ρ^cf` | 帳本拆分（只影響 DL） |
| Q1 DL、DL0（含於 NEV、VCP） | 上列 ＋ 帳本拆分 `v^u/v^x, l^u/l^x, c^u/c^x`、`C^{impl,x}`、`τ`、`λ^u`、部門專屬限制 | — | — |
| Q2 `F_c^†`、`δ^†` | 不需要 `F_c` 本身；需要 Block X、R、V 中所有使用 `c` 的 initiative，以及 `C^impl(ȳ)` 在 `c` 有／無時的值 | `δ` | 與 `c` 無關的 initiative 的細節（但其資源使用需要，若預算綁住） |
| Q3 VG、EE／RE／CE | 至少兩個 `γ` 的 Block G、全部 Block X、R、V | 替代 `γ` | 帳本拆分（若只報 B） |
| Q4 DL 來源分解 | 同 Q1 DL | — | — |
| Q5 PR_X、AT／ABOVE 狀態 | 要求表、配置空間、`I^sev`、`ē`、相關結果查表 | — | 其他 initiative 的細節（若資源不綁） |
| Q6 VRG、design-response regret | `ρ^design`（OBS）、`ρ^obs` 或 `ρ^cf` 區間 | `ρ^cf` | — |
| Q7 穩健性分類 | `𝒢`、`Θ_g` 的事前登記 | 全部 SCN 參數 | — |
| Q8 Interface activation | 同 Q5 ＋ 各介面元素的觀察值 | — | — |

---

## 3. 量測優先序（由模型決定，不由受訪者決定）

1. **定義性與文件可觀察項先行**：`M_j` 屬性、`κ`、`Pre`、`Allow`、要求表、`Legal`、`Eff_H`、`FB`、`ρ^design`、帳本歸屬規則。這些多為 OBS，且決定可行集合；可行集合錯了，所有數值都無意義。
2. **資源與共享成本**：`B̄`、`Ā^ENG`、`F_c`、`a_c`、`C^impl(ȳ)`。決定 Q1、Q2 是否可算。
3. **事件量與結果查表**：`N`、`π`、`P`、`v/l/c/t`、`I^sev`。
4. **反應分布**：`ρ^obs` 先於 `ρ^cf`。
5. **以 value-of-identification 診斷（42 §13.5）決定第 3–4 項中哪些格要縮小區間**：先跑一次以寬區間為主的 `Θ_adm`，找出對 regret 貢獻最大的參數區塊，再投入量測資源。

---

## 4. 外部評估介面（不是決策者）

董事端（含董事所屬公司或治理端）、合作商／策略夥伴、投資端可提供 `source_scope = external` 的 `EXPERT_ELICITED` 區間，或對結果做 face-validity 挑戰。他們**不是**任何層級的 optimization player；除非取得其正式決策權的證據，否則不改變 42 的層級結構。

| 可挑戰／界定的對象 | 參數或輸出 | 進入方式 |
|---|---|---|
| 企業價值假設 | `v^u, v^x` 的區間；`N_{jk}` throughput 情境 | 擴大或收窄 `Θ_g`；必須記錄理由 |
| 策略價值 | `J^must_γ`、`J^forbid_γ` 的替代方案 | 新增 `γ` 選項（SCN） |
| 風險邊界 | `κ_j` 的類別判定、`ē_j^γ` | 新增情境組；不得把外部意見直接改為 OBS |
| 共享能力投資邏輯 | `F_c`、`δ` 的區間；`Allow^loc` | 擴大 `Θ_g`；檢驗 `F_c^†` 是否落在可接受範圍 |
| Portfolio 優先序 | 模型輸出的 portfolio、ROBUST／FRAGILE 標記 | Chapter 4.9 的 face-validity 紀錄；分歧不覆寫模型結果 |

---

## 5. 缺值處理總表（與 42 §13.4 一致）

| 狀態碼 | 觸發 | 仍可報告 |
|---|---|---|
| `INVALID_SCHEMA_OR_UNITS` | 型別、單位、正規化錯誤 | 無 |
| `UNEVALUABLE_INITIATIVE` | status quo 查表缺 | 其他 initiative |
| `RESTRICTED_SOLVE` | 某配置查表缺 | 受限最適解＋被排除配置清單；受影響元素標 UNIDENTIFIED |
| `THRESHOLD_MODE` | `F_c` 缺 | `F_c^†` 區間 |
| `PARTIAL_OBJECTIVE` | `λ` 缺 | `(F_E^{−time}, ΔHours)` |
| `FOLLOWER_LEDGER_UNIDENTIFIED` | 帳本拆分缺 | B、A+、VSC；A、C0、C 及 VRA、DL0、VCP、DL、NEV 標 UNIDENTIFIED |
| `REJECT_INSUFFICIENT_IDENTIFIED_INPUTS` | `B̄` 或 `Ā^ENG` 缺 | 資源—價值前緣（若可） |
| `STATUS_QUO_NONCOMPLIANT` | 現況違反 (F2)(F9) | 違反清單 |

**任何狀態下都不得以 0、平均值、v1.0 synthetic 係數、或外部效果量補值。**
