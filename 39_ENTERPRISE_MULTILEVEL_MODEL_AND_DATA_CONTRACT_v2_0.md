# Enterprise AI Adoption｜多層模型與資料契約 v2.0

**狀態：v2.0 enterprise-scope formal specification。** 本規格承接既有 ordinal/cardinal 修正、Boss–Manager bilevel、角色別 response distribution、typed monetary units、missing-as-UNIDENTIFIED 與 V0–V7 驗證原則，但將分析對象從單一流程改為 enterprise AI portfolio。

## 1. 索引與資料主鍵

最小主鍵：

`(enterprise_id, business_unit_id, initiative_id, role_group, period, scenario_id, source_id)`

每筆另存：

`provenance_type, source_date, evidence_status, uncertainty, collection_method, authorization_scope`

任何輸入都不得因方便求解而失去來源層級。

## 2. Enterprise-level variables

- `b`：企業層資源、政策、共用能力與優先序決策
- `Γ`：policy / permission / governance set
- `B_TWD(T)`：期間總預算，TWD／期間
- `K_hours(T)`：共用人力／工程容量，小時／期間
- `Infra`：可用平台／運算／整合基礎設施狀態
- `D_shared`：跨單位共用交換能力
- `R_shared`：共用資料／模型／工具資源可得性
- `C_shared(b,s)`：企業共用平台、治理、資安、training、evaluation 等成本，TWD／期間

企業層 ordinal 狀態只能作門檻鍵；成本與效益需有明確單位。

## 3. Business-unit / initiative variables

對每個 `j`：

`x_j=(A_aut,j,H_j,WI_j,EA-V_j,m_j)`

並分開保存：

- `A_aut_obs,j`：現況 AI 權限
- `A_cap0,j`：現有能力下可部署上限
- `A_target,j`：情境要求
- `A*_j`：模型條件性推薦
- `H_obs / H_req / H* / H_effective`
- `WI_obs / WI_req / WI*`
- `EA_V_obs / EA_V_req / EA_V*`
- `EA_X`：解釋可用性候選
- `κ_j`：後果類別，只作 lookup key
- `m_j`：human-only、delegated、AI→human、human→AI、aggregation、bounded execution 等配置屬性

Business unit、initiative 與 shared capability 必須分表，避免把平台能力誤寫成單一部門觀察。

## 4. User-response layer

令：

`ρ_j(r|x_j,z,role,s)`

為角色在可見訊號 `z`、配置 `x_j` 與情境 `s` 下的反應分布；`r` 可為：

`Use, Verify, Modify, Escalate, Reject, Bypass`

另有：

- `π_j(role|s)`：角色工作量／暴露權重，和為 1
- `P_j(z,ω|x_j,s)`：可見訊號與隱藏結果的聯合分布
- `ω`：行動當下不可見的真實結果，不得放入受訪者條件資訊

所有 probability tables 非負且正規化。沒有實證時只能使用明示的區間或 scenario sensitivity。

## 5. Feasible set

對每個 initiative：

`X_j(b,s)`

由以下條件共同決定：

- enterprise policy `Γ`
- business-unit decision rights
- shared infrastructure capability
- data access / governance
- `A × κ` 下的最低 H/WI/EA requirements
- budget / engineering capacity
- legal, privacy, security and rights constraints
- required fallback / rollback path

若任何必要門檻或 lookup 未識別，輸出 `UNIDENTIFIED` 或 `INSUFFICIENT_IDENTIFIED_INPUTS`，不得自動補值。

## 6. Value, loss and cost tables

對每個 `j`：

- `N_j(T)`：期間事件／工作量
- `V_j(x,r,ω;s)`：價值，TWD／事件或可追溯替代指標
- `L_j(κ,x,r,ω;s)`：企業損失，TWD／事件
- `L_oper,j(x,r,ω;s)`：business-unit 可控制的營運損失，TWD／事件
- `C_op,j(x,r,z;s)`：review / exception / operational cost，TWD／事件
- `C_impl,j(x,b,s)`：local implementation / maintenance，TWD／期間
- `CapHours_j(x,b,s)`：工程／人力容量需求，小時／期間
- `C_shared(b,s)`：共用平台與治理成本，TWD／期間

共同成本不得在每個部門重複扣除。若一個 shared capability 同時支援多個 initiative，其成本分攤規則需另有來源或只在 enterprise objective 計一次。

## 7. 條件期望

`E_j[f|x_j,s] = Σ_role π_j(role|s) Σ_(z,ω) P_j(z,ω|x_j,s) Σ_r ρ_j(r|x_j,z,role,s) f_j(x_j,r,z,ω;s)`

`ρ`、`P` 與 `π` 均須有 provenance；同一資料來源不可被重複包裝成看似獨立的多份證據。

## 8. Enterprise objective

企業層情境目標的候選形式：

`F_E(b,x;s) = Σ_j N_j(T)[E_j(V_j)-E_j(L_j)-E_j(C_op,j)] - C_shared(b,s) - Σ_j C_impl,j(x_j,b,s)`

單位為 TWD／期間。

如果 quality、rights、privacy、security 或 compliance 無法合理貨幣化，保留為 constraints 或分項報告，而不是任意加上金錢權重。

## 9. Business-unit objective

對 unit / initiative `j`，候選管理目標：

`F_M,j(x_j|b,s) = -N_j(T)[E_j(L_oper,j)+E_j(C_op,j)] - C_impl,j(x_j,b,s)`

並可另加具單位或硬性 service / quality constraints。

**注意：** `F_E` 與 `F_M,j` 的形式不同不等於實際利益衝突。只有企業與部門的責任範圍、偏好或取捨由文件／訪談／行為證據支持時，才能宣稱 multilevel conflict。

## 10. Shared-capability coupling

Enterprise scope 的核心新增點是跨 initiative coupling：

1. **Shared fixed cost**：平台、模型服務、治理、資安、evaluation 不隨單一部門重複建置。
2. **Capacity coupling**：多個 initiative 競爭同一 engineering / compute / review capacity。
3. **Data/network externality**：共用介面或治理投資可能降低後續 initiative 的邊際導入成本；只有有證據時才量化。
4. **Policy coupling**：enterprise policy 對所有 units 設共同下限或禁止集合。
5. **Portfolio sequencing**：initiative 啟動順序可能改變後續可行集合；靜態版先做單期 portfolio，跨期版再進 M5。

## 11. Solution concept

基線採 Enterprise–Business Unit bilevel / portfolio decision：

`x*_M(b,s;θ) ∈ argmax_x F_M(x|b,s;θ)`

`b*(s;θ) ∈ argmax_b F_E(b,x*_M(b,s;θ);s,θ)`

多 unit 時需明定各 unit 的 local response、跨 unit coupling、tie handling 與 enterprise optimistic/pessimistic bounds。

使用者層預設透過 `ρ` 內嵌；只有符合第三層證據門檻才加入 user optimizer。

## 12. Sensitivity and identification

`Θ_adm` 保存每個 lookup、成本、事件數、response distribution 與換算率的可接受區間及其相依限制。

每個 portfolio decision 報：

- `ROBUST`：在預先界定的 Θ_adm 範圍選擇不變
- `CONDITIONAL`：只在不同預先界定情境組間改變
- `FRAGILE`：同一合理情境組內就改變
- `UNIDENTIFIED`：資料不足以界定合理參數集合

不得挑選最有利的 sensitivity scenario 當成結果。

## 13. Enterprise validation gates V0–V7

- **V0 Source & Authority**：企業／部門權限、共享資源、AI initiative 邊界與可觀察證據有來源。
- **V1 Construct Validity**：構念內容效度；G01–G16→M1–M4 至少雙人盲編與裁決。
- **V2 Cross-functional Pilot**：跨至少兩種功能角色／單位測理解、缺格、非單調、角色差異與負擔；不預設任何特定部門是核心。
- **V3 Schema & Units**：ordinal keys、probabilities、one-hot、TWD/event、TWD/period、hours/period 型別守恆。
- **V4 Lookup Completeness**：每個求解所需 cell 有來源或 bounded scenario；缺格拒算。
- **V5 Enterprise Portfolio Solver**：以小型 synthetic oracle 驗證 shared budget、capacity、local response、ties、centralized vs bilevel。
- **V6 Invariance & Sensitivity**：單位換算、period conversion、ordinal relabeling、Θ_adm scans、coverage report。
- **V7 Enterprise Empirical Calibration**：企業層政策、部門配置、角色反應與 outcome/cost proxies 可交叉核對。

## 14. 最小企業資料表

### enterprise_policy
`enterprise_id, period, policy_id, right_owner, budget, capacity, shared_capability, forbidden_condition, source_id, provenance`

### business_unit
`business_unit_id, function_type, owner_role, local_constraints, source_id, provenance`

### ai_initiative
`initiative_id, business_unit_id, capability_id, task_family, A_aut_obs, A_cap0, H_obs, WI_obs, EA_V_obs, kappa_class, status, source_id`

### shared_capability
`capability_id, infrastructure_type, reusable_scope, fixed_cost, capacity, access_policy, version, source_id`

### user_response
`initiative_id, role_group, x, z, response_r, count_or_interval, provenance, uncertainty`

### outcome_lookup
`initiative_id, x, role, z, omega, response_r, metric, lower, upper, unit, period, source_id, admissibility`

### portfolio_result
`scenario_id, b, selected_initiatives, unit_configs, enterprise_value_range, local_value_ranges, feasibility, robustness_class, missing_inputs`

## 15. 不允許的捷徑

- 不以「AI 成熟度總分」直接替代 enterprise decision architecture。
- 不把 0–3 ordinal levels 當效用值。
- 不把 adoption rate 固定加分。
- 不把 shared cost 重複灌給每個 unit。
- 不把外部 productivity effect 當企業自身 effect。
- 不把單一部門的 case result 外推為 enterprise-wide evidence。
- 不把資料缺失填 0。
- 不因模型形式存在便宣稱企業具有真實多層利益衝突。

**本規格為 v2.0 之 canonical model/data contract；後續 solver、questionnaire 與 empirical collection 均應以此為上位約束。**