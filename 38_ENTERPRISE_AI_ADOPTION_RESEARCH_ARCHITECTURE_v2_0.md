# 企業人工智慧導入作為多層級決策系統｜研究架構 v2.0

**狀態：2026-10-10 scope correction 後的新 canonical research architecture。** 本研究不再以單一部門、流程或 use case 作為研究本體；研究主體改為 **enterprise-wide AI adoption**。既有文獻語料、G01–G16、M1–M4、尺度修正、來源追溯與驗證資產保留；任何舊的單一流程案例只能視為歷史開發材料，不再限制理論邊界。

## 1. 研究定位

本研究將企業 AI 導入視為一個跨層級、跨部門、共享資源與治理約束下的決策系統。核心證據鏈為：

`Large-scale AI × Decision corpus → G01–G16 structural gaps → M1–M4 organizational mechanisms → enterprise AI adoption architecture → multilevel configuration and organizational response → enterprise value realization`

G01–G16 是文獻網絡中的結構性低連結研究線索，不是企業已發生的 16 個問題，也不是模型權重。其作用是提供需要被組織層級研究檢驗的介面。

核心研究問題為：

> 當企業全面導入 AI 時，高階治理、共用 AI 能力與資源配置，如何透過不同事業／功能單位的部署設計與員工實際使用反應，形成可治理、可量測且可持續調整的企業價值？

## 2. 分析單位與嵌套結構

本研究採嵌入式企業個案邏輯。主要分析層級為：

1. `Enterprise`：企業整體 AI 戰略、治理、共用資源與投資組合。
2. `Business Unit / Function`：部門或功能單位對 AI initiative 的配置與導入。
3. `AI Initiative / Shared Capability`：可被部署、共用或組合的 AI 能力與工作安排。
4. `Role-specific Users`：不同角色在實際可見資訊與制度限制下的採用、查核、修改、升級、拒用或繞過反應。

因此，研究不再以「一個具名流程事件」作為整篇研究的唯一分析單位。流程或任務只作為 AI initiative 的局部觀察點；理論推論的核心是 **企業層與部門層之間的配置、治理、資源耦合與價值實現**。

## 3. 多層決策架構

### 3.1 Level 1 — Enterprise / Executive

企業層決定：

- AI strategy 與 strategic priorities
- 資本與營運預算
- shared infrastructure / platform
- data strategy 與資料存取原則
- governance policy 與 decision rights
- risk appetite 與禁止邊界
- centralized / federated / decentralized operating model
- 共用能力與跨部門資源配置

令企業層決策向量為：

`b = (B, Γ, Infrastructure, SharedCapability, Priority)`

其中 `B` 為資源／預算、`Γ` 為政策與授權集合，其餘元素必須由可觀察的企業制度或明示情境界定，不以抽象成熟度分數替代。

### 3.2 Level 2 — Business Unit / Functional Management

對每個 business unit 或 AI initiative `j`，管理者在企業層政策與共享資源限制下選擇：

`x_j = (A_aut,j, H_j, WI_j, EA-V_j, m_j)`

其中：

- `A_aut`：AI 對決策／行動的授權深度
- `H`：人工介入與控制權
- `WI`：工作流程整合與路由
- `EA-V`：evaluation / assurance / revalidation
- `m`：人機決策順序、最終權限、執行與復原模式

`j` 不綁定特定部門；可代表 Finance、Sales、Manufacturing、R&D、IT、QA、Procurement、HR 或其他功能，也可代表跨部門 shared capability。

### 3.3 Organizational User Response

第一線或專業使用者不預設為第三個效用最大化者。其行為以角色別條件反應表示：

`ρ_j(r | x_j, z, role, s)`

其中 `z` 是使用者在行動當下可見的訊號，`s` 是情境，`r` 可包含：

`{Use, Verify, Modify, Escalate, Reject, Bypass}`

只有在取得獨立裁量、不同目標／限制、上層預期其反應且該反應會反事實改變上游配置的證據後，才建立真正第三層 optimization。

## 4. 組織機制

### M1 — Governance & Decision Rights
研究誰可批准、拒絕、停止、變更授權、承擔責任，以及 enterprise policy 與部門實際控制是否一致。

### M2 — Workflow & Integration
研究 AI 輸出如何跨系統、跨部門與決策節點流動，包含正常路由、例外、handoff、rollback 與復原。

### M3 — Human–AI Work Configuration
研究 automation、augmentation、AI-first、human-first、aggregation、delegation、override 等配置如何影響組織採用與結果。

### M4 — Evaluation & Assurance
研究 pre-deployment validation、monitoring、revalidation、auditability、explanation usability、data/model drift 與 rollback。

### M5 — Learning & Resource Feedback（動態擴充）
只有在跨期資料成立時才建模：

`Outcome_t → Policy/ResourceAllocation_(t+1)`

M5 不進入靜態 baseline，也不由 G01–G16 的網絡位置直接推導時間因果。

## 5. 研究問題

**RQ1 — Enterprise Governance**  
企業層級的 AI 戰略、治理、共享能力與資源配置如何影響不同事業／功能單位的 AI 導入選擇？

**RQ2 — Cross-level Alignment**  
企業層設定的目標、政策與能力邊界，與各部門實際需求、配置及工作流程之間，在何種條件下形成一致、落差或衝突？

**RQ3 — Organizational Adoption**  
部門層級的 AI 配置、人工控制、工作流程整合與 assurance 機制，如何對應到不同角色的實際使用、查核、修改、升級、拒用與繞過行為？

**RQ4 — Enterprise Portfolio Configuration**  
在有限預算、共享 AI 能力、治理要求與異質部門需求下，企業應如何形成可行的 AI initiative portfolio 與資源配置？

**RQ5 — Value Realization**  
哪些 enterprise AI configurations 在成本、績效、風險、可擴展性與組織採用之間形成較穩健的價值實現？

## 6. 構念與尺度原則

保留既有核心構念，但改為 enterprise interpretation：

- `D`：共用數位系統／AI capability interoperability
- `R`：資料與 AI resource readiness / accessibility
- `G`：正式治理與 decision rights
- `A_aut`：AI autonomy / deployment depth
- `H`：human oversight / intervention right
- `WI`：workflow integration
- `EA-V`：evaluation & assurance evidence
- `EA-X`：explanation usability（若通過內容效度才納入）
- `κ`：後果類別，只作查表鍵，不是金額

`Strategic Alignment (S)` 與 `Change Capability (C)` 可作 enterprise-level 候選構念，但在完成文獻與內容效度前不凍結、不進目標函數。

**尺度鐵律：** 序位值只允許同構念門檻比較或查表索引；不得直接跨構念相加、乘法、除法或當成 TWD 效用。

## 7. Enterprise Gap 定義

Gap 不再被寫成一個部門流程的 Likert 距離。對 enterprise policy / capability requirement 與 business-unit observed state，可定義方向性條件：

`Gap_X(j,s) = 1[X_obs(j) < Req_X(A_target,j,s)]`

其中 `X` 必須是同一構念；`A_target=A_obs` 表示現況要求，`A_target=A*` 表示條件性反事實。Gap 為方向／約束觸發，不是損失幅度。

## 8. Enterprise AI Portfolio Economics

企業價值模型必須分開 shared cost 與 local cost：

`Enterprise Value = Σ_j LocalValue_j - SharedPlatformCost - SharedGovernanceCost - Σ_j LocalImplementationCost - Risk/ExceptionCost`

共同 AI platform、data layer、security、inference、evaluation、governance 與 training 具有共享與規模經濟；不得把每個部門的基礎設施成本重複計算。

可貨幣化項目以 TWD／期間、TWD／事件、小時／期間等明確單位登記。隱私、法規、權利與不可交換的政策界線保留為 constraints，不以主觀金額權重換算。

## 9. 證據與 provenance 原則

所有輸入明確分為：

- `OBSERVED`
- `EXPERT_ELICITED`
- `PUBLIC_OBSERVED`
- `SCENARIO_SENSITIVITY`
- `SIMULATED_ONLY`
- `UNIDENTIFIED`

`observed`、`elicited`、`simulated`、`optimized` 不得互相回填。空值不得用 0、平均值或歷史 v1.0 synthetic coefficients 補齊。

## 10. 現階段可凍結與不可凍結

### 可凍結
- corpus → G01–G16 → M1–M4 → enterprise adoption architecture 的證據鏈
- Enterprise > Business Unit > Initiative/Capability > Role 的嵌套層級
- Enterprise–Business Unit 為預設雙層；使用者為條件行為反應
- ordinal ≠ cardinal
- provenance 分層與 UNIDENTIFIED 規則
- shared cost / local cost 分離
- M5 僅作 longitudinal extension

### 尚不可凍結
- S/C 新構念
- 實際企業權限、偏好與目標衝突
- 部門權重與 initiative 優先序
- 任何 firm-specific ROI 或效果量
- 真正第三層 optimization
- 最終 questionnaire 與 empirical coefficients
- V0–V7 的 enterprise empirical pass

## 11. 下一個 critical path

1. 建立 enterprise AI adoption inventory：business units、AI initiatives、shared capabilities、owners、decision rights。
2. 建立 enterprise policy / capability register，分清 shared 與 local resources。
3. 將 G01–G16 重新對應到 enterprise interfaces，由至少兩位編碼者盲審。
4. 建立跨部門內容效度與 pilot，不綁單一流程。
5. 將 v1.6 schema validator 改為 business-unit / portfolio-neutral fixture。
6. 建立完整 enterprise portfolio bilevel solver，處理 shared budget、capacity、platform coupling、ties 與 UNIDENTIFIED inputs。
7. 執行 Θ_adm sensitivity，輸出 `ROBUST / CONDITIONAL / FRAGILE / UNIDENTIFIED`。
8. 完成 enterprise empirical calibration 後才寫實證 Results / Discussion。

**本檔自建立起取代以單一垂直流程作為研究主體的架構。**