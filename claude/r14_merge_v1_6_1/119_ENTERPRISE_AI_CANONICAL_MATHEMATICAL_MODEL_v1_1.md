# 119 企業 AI 決策模型：Canonical 數學形式 v1.1

> 日期：2026-10-13｜狀態：v1.6.1 MATH RC / CANONICAL FORMULATION CANDIDATE（數學整理與工程／外部採購面新增；無企業資料）
> 可執行基準仍為 06 v2.2／51／65；74 v2.4 為候選語意。本檔把 06、74、75、89 與 83–118 的模型收斂為單一形式，並新增第四個層面 ENGINEERING / SOURCING PLANE。
> 本檔不修改 06、74、75、89、51、65 或 `org_schema.py`。每一條方程都標示來源：`[06]`、`[74]` 表示沿用、語意不變；`[ENG]` 表示本輪新增；`[ENG-REF]` 表示只在工程面啟用時才適用的細化。
> `ORG_MAPPING_HUMAN_VALIDATION = PENDING`；`ENTERPRISE_EMPIRICAL_STATUS = PENDING`。所有數值例子見 123／125，皆為 `SIMULATED_ONLY`。

---

## 1. 研究問題

模型回答的不是「AI 值不值得導入」，而是：在不同的 AI initiative、能力、治理、實際使用、人員反應、工程人力稀缺與外部採購選項下，企業應如何**共同決定**

- project portfolio 與 AI 配置（`q`）；
- 共享能力（`y`）與本地能力（`y^loc`）；
- 治理 policy（`γ`）與資源 envelope（`e`）；
- 內部 AI 工程人力（`n_w`）；
- 外部工程產能（`K^{ext}_w`、`χ_w`），

使企業的實現價值（realized value）在既有限制下最大。AI 工程人數與顧問用量因此是 portfolio 決策的一部分，不是事後的管理建議。

模型分四個層面；四個層面共用同一組 `q, y, γ, α, ρ`，同一個經濟後果只計價一次：

| 層面 | 內容 | 來源 |
|---|---|---|
| 1 VALUE／REALIZATION PLANE | 路徑淨貢獻 `f`、AI／NOAI 分支、使用率 `α`、反應 `ρ` | 06 §6–§7、74 §2–§4 |
| 2 PORTFOLIO／CAPABILITY PLANE | 配置選擇、可行性、共享能力、預算與容量 | 06 §5、§10 |
| 3 GOVERNANCE／MULTILEVEL DECISION PLANE | `γ`、A／A+／B／C／C0／D、envelope、部門帳本 | 06 §8、§11、§12；85 |
| 4 ENGINEERING／SOURCING PLANE | 技能別工程需求、內部人力、外部產能、工程預算 | **本輪新增** |

---

## 2. 集合與索引

| 集合 | 元素 | 意義 | 來源 |
|---|---|---|---|
| `U` | `u` | 事業單位／功能 | [06] |
| `J`；`J_u = {j : u(j)=u}` | `j` | AI initiative／use case；`u(j)` 為擁有者 | [06] |
| `K_j = {0} ∪ M_j` | `k` | `j` 的候選配置；`k=0` 為 status quo（不新增 AI 部署）；`M_j` 為有限列舉的 AI 配置 | [06] |
| `C` | `c` | 共享能力 | [06] |
| `Λ_j` | `ℓ` | 與 `j` 相關的人員／組織角色（**只含業務流程角色，不含 AI 工程人員**，見 §11.7） | [06]；限制 [ENG-REF] |
| `𝓡 = R ∪ {NA}` | `r` | 人員反應：`Use, Verify, Modify, Escalate, Reject, Bypass`；`NA` 為無 AI 輸出。06 原寫 `R ∪ {NA}`；本檔記為 `𝓡` 以避免與資料等級 `R_j` 混淆（只是記號，集合不變） | [06] |
| `Z_j` | `z` | 行動當下可見的 AI 訊號 | [06] |
| `Ω_j` | `ω` | 行動當下不可見的實際結果 | [06] |
| `S_{jk}` | `s` | 能力來源狀態（`s_{jc} ∈ {L, S, ∅}`） | [06 §10] |
| `Γ` | `γ` | policy profile 選單；`γ^0` legal-minimum；`γ^cur` 現行 | [06] |
| `H^pool = {BUD, ENG}`；`H^own_u = {REV}` | `h` | 池化與部門自有資源類別 | [06] |
| `𝒢`；`Θ_g` | `g` | 預先登記的 scenario 組 | [06 §13] |
| **`W^{ENG}`** | **`w`** | **工程技能類別**（AUTHOR_DEFINED_OPERATIONAL_CATEGORY，不是文獻已驗證的構念）。候選：`AI_LLM`、`DATA`、`MLOPS_PLATFORM`、`INTEG`（INTEGRATION_APP） | [ENG] |

**記號紀錄。** 工程技能索引使用 `w`：`p` 已被 06 §13.5 的 VOI 參數區塊（`VOI_p`、`θ_p`）使用；`m` 是配置型態 `m_k`；`h` 是資源類別。完整的衝突稽核見 120 的 `Collision_Audit` 工作表。

---

## 3. 參數

### 3.1 沿用的參數（語意不變）

| 參數 | 意義 | 單位 | 來源 |
|---|---|---|---|
| `N_{jk}` | eligible events | events/period | [06]（74 確認 `α` 不改變 `N`） |
| `π_j(ℓ∣k)`、`P_j(z,ω∣k)`、`ρ_j(r∣k,z,ℓ,s)` | 角色暴露、訊號—結果聯合分布、反應分布；`ρ` 不以 `ω` 為條件 | probability | [06 §3.3、§6] |
| `v, l, c, t, t^{REV}, I^{sev}` | 路徑層級的價值、損失、非人工營運成本、業務人員工時、審查工時、嚴重事件機率 | TWD/event；hours/event | [06 §3.3] |
| `λ_ℓ`、`λ^u_ℓ` | 業務角色時間的可實現機會價值（企業／部門帳本） | TWD/hour | [06] |
| `α_{jk}(s)` | 實際使用率；HumanOnly 為 0（DEFINITIONAL） | probability | [74 U1] |
| `noai_route_k` | `STATUS_QUO`／`CONFIG_SPECIFIC` | nominal | [74 §6] |
| `O_{jk}`、`Rec_{jk}(s)`、`C^{impl}_{jk}(s)` | 一次性與持續導入成本；`C^{impl} = O·AF + Rec` | TWD；TWD/period | [06 §3.4] |
| `F_c`、`y^{cur}_c`、`a^h_c` | 共享能力期間成本、現況、資源使用（`a^{ENG}_c` 已存在） | TWD/period；hours/period | [06 §3.1] |
| `F^{loc}_{uc}`、`a^{h,loc}_{uc}` | 本地版本的成本與資源 | 同上 | [06] |
| `a^{ENG}_{jk}(s)` | 配置的工程工時（以能力來源為索引） | hours/period | [06 §3.2] |
| `Ā^{BUD} = B̄`、`Ā^{ENG}` | 池化預算與池化工程工時 | TWD/period；hours/period | [06 §3.1] |
| `B^0_u`、`K^{ENG,0}_u` | Model A 的部門固定預算與工程容量 | 同上 | [06] |
| `ΔC^{gov}(γ)`、`Allow_γ`、要求表、`ē^γ_j`、`Legal_{jk}` | 治理與硬限制 | 見 06 | [06] |
| `T1–T5` | 使用者層 optimizer 觸發測試 | boolean | [06 §9.2] |

### 3.2 新增參數（工程／外部採購面）

| 參數 | 意義 | 單位 | 備註 |
|---|---|---|---|
| `a^{ENG,w}_{jk}(s)` | 配置 `(j,k)` 在能力來源狀態 `s` 下所需的技能 `w` 有效工程工時 | effective hours/period | 由容量型工作包加總（§11.7）；`Σ_w a^{ENG,w}_{jk}` 對應 06 的 `a^{ENG}_{jk}`，但技能不可互相替代（§11.10），所以限制式逐技能分開 |
| `a^{ENG,w}_c`、`a^{ENG,w,loc}_{uc}` | 共享能力與本地能力本身所需的技能 `w` 工時 | effective hours/period | 共享能力的工程需求在 06 已以 `a^{ENG}_c` 存在；本輪只依技能拆分 |
| `n^{cur}_w` | 現有內部 `w` 類 FTE | FTE | OBSERVED（HR 資料） |
| `K^{int}_w(n)` | `n` 名內部人員每期可提供的有效工程容量 | effective hours/period | canonical 為一般函數；線性特例見 §11.3 |
| `C^{int}_w(n)` | `n` 名內部人員的 fully-loaded 成本 | TWD/period | 同上 |
| `Q^{nom}_w`、`η_w` | 每 FTE 名目可用工時、有效專案使用率 | hours/FTE/period；fraction | 只在 LINEAR CAPACITY SPECIAL CASE 使用；`η_w` 不得任意指定實證值 |
| `ν^{FTE}_w` | 每 FTE fully-loaded 成本 | TWD/FTE/period | 只在線性特例使用 |
| `K^{fix}_w` | 不屬於 FTE 的既有固定工程容量（例如已簽、不可調整的既有合約） | effective hours/period | 不得包含任何已計入 `n^{cur}_w` 的人員（§11.5） |
| `ν^{ext}_w` | 外部容量型工程的邊際價格 | TWD/effective hour | LINEAR_EXTERNAL_COST baseline |
| `F^{ext}_w` | 外部容量的固定 retainer／啟動成本 | TWD/period | 無固定費時為 0 |
| `K̄^{ext}_w` | 外部市場在本期可取得的最大容量 | effective hours/period | 取代 big-M；有經濟意義 |
| `B̄^{ENG}` | 工程／人力預算（增量內部人力＋容量型外部採購） | TWD/period | 與 06 的 `B̄` 分開（§11.6） |

---

## 4. 決策變數

| 變數 | 意義 | 型別 | 決定者（依模型） | 來源 |
|---|---|---|---|---|
| `q_{jk}` | `j` 是否採配置 `k`（one-hot） | binary | B／A+：企業；A／C／C0：部門 | [06] |
| `y_c` | 共享能力 | binary | 企業（B、C） | [06] |
| `y^{loc}_{uc}` | 本地能力 | binary | B／A+：企業；A／C／C0：部門 | [06] |
| `γ` | policy | element of `Γ` | 企業 | [06] |
| `e^h_u` | 池化資源 envelope | TWD/period；hours/period | 企業（C、C0） | [06] |
| **`n_w`** | 內部 `w` 類 FTE 總數（**含現有人員**），`n_w ≥ n^{cur}_w`，整數 | `Z_+` | 企業（B、A+、C、C0 的 leader） | [ENG] |
| **`K^{ext}_w`** | 本期購買的外部 `w` 類有效工程容量 | effective hours/period，≥ 0 | 同上 | [ENG] |
| **`χ_w`** | 外部 retainer 是否啟用 | binary | 同上 | [ENG] |
| `e^{ENG,w}_u` | 技能別工程 envelope（C、C0 中取代 `e^{ENG}_u`） | effective hours/period | 企業 | [ENG]（06 envelope 依技能拆分） |

**外部夥伴不是決策者。** `n_w`、`K^{ext}_w`、`χ_w` 都是企業的決策；外部顧問／SI／vendor 只提供工程產能、專業能力、導入服務、知識移轉與代管服務，沒有目標函數、不出現在任何 argmax（§11.8；85 A-ORG-05）。

**BUILD／BUY／HYBRID 不是決策變數。** 它們由最適解推導（§15.2）。

**使用者層。** 預設不是決策變數；`ρ` 內嵌。只有 T1–T5 全成立時才建立 Model D（[06 §9.2]）。工程面不改變這一點。

---

## 5. 事件價值帳本

$$
f_j(k,\ell,z,\omega,r) = v_j - l_j - c_j - \lambda_\ell\,t_j \tag{V1, [06]}
$$

- `v`：營收或機會價值；`l`：損失（錯誤、重工、延誤、客戶影響）；`c`：非人工的每事件營運成本（推論、API、外部服務）；`t`：**業務流程**人員工時；`λ_ℓ`：該角色時間的貨幣化價值。
- 每個經濟後果只能出現在一個位置（06 §7.2、74 §5 的歸屬表，語意不變）。不得新增 adoption bonus、effective-use bonus、AI score、innovation score、ConsultantBonus、KnowledgeRetention 或 InternalCapabilityBonus。
- **`λ_ℓ t` 不包含 AI 工程人力。** AI 工程人員的時間只以工程容量（§11）出現，其金錢成本只以 `C^{int}_w` 或 `C^{ext}_w` 計價一次（§11.7）。
- 帳本的部門版本 `f^u = v^u − l^u − c^u − λ^u_ℓ t`（[06 §8.1]）。

**一個經濟後果 → 一個貨幣帳本位置。** 工程工時可以同時出現在容量限制中，但它的金錢成本只能被計價一次。完整的成本歸屬見 121。

---

## 6. AI／NOAI 期望

**AI 分支**（角色 × 訊號／結果 × 反應）：

$$
\mathbb E^{AI}_{jk}[f\mid s] = \sum_{\ell\in\Lambda_j}\pi_j(\ell\mid k)\sum_{z\in Z_j}\sum_{\omega\in\Omega_j}P^{AI}_j(z,\omega\mid k)\sum_{r\in\mathcal R_k}\rho_j(r\mid k,z,\ell,s)\,f_j(k,\ell,z,\omega,r) \tag{X1, [06]}
$$

`ρ` 不以 `ω` 為條件（人員在行動當下看不到實際結果；任何以 `ω` 為鍵的 `ρ` 一律拒算）。`ρ` 只在有證據時才隨 `s` 改變。

**實際使用混合**（canonical 第一版採全 initiative 的 `α_{jk}(s)`；角色別 `α_{jkℓ}(s)` 保留為 future extension）：

$$
\tilde{\mathbb E}_{jk}[f\mid s] = \alpha_{jk}(s)\,\mathbb E^{AI}_{jk}[f\mid s] + \big(1-\alpha_{jk}(s)\big)\,\mathbb E^{NOAI}_{jk}[f\mid s] \tag{X1′, [74]}
$$

**NOAI 分支**由 `noai_route_k` 決定（[74 §2.3、§6]）：

| `noai_route` | `E^{NOAI}_{jk}` | 使用條件 |
|---|---|---|
| `STATUS_QUO` | 現況 `k=0` 的查表，在所選能力狀態下求值 | 須寫明 (C2)(C3) 的依據；有 shadow use、流程整體改造或選擇效果證據時不得使用 |
| `CONFIG_SPECIFIC` | `k` 自己的 NOAI 分支查表（反應恆為 `NA`） | 已部署者由未叫用事件觀察；未部署者引出或 scenario；**HumanOnly 配置一律屬此類，`α ≡ 0`（DEFINITIONAL）** |

**缺值語義（[74 §14]，不變）：** AI 配置缺 `α` 不得補 0；缺 `noai_route` 不得預設為 `STATUS_QUO`。

---

## 7. 配置貢獻

$$
\tilde g_{jk}(s) = \tilde{\mathbb E}_{jk}[f\mid s],\qquad
\varphi_{jk}(s) = N_{jk}\,\tilde g_{jk}(s) - N_{j0}\,\tilde g_{j0}(s^{cur}) - C^{impl}_{jk}(s),\qquad C^{impl}_{j0}\equiv 0 \tag{V2′, [74]}
$$

- `φ_{jk}` 是相對於「現況配置在現況能力狀態下」的增量貢獻（TWD/period），語意與 06 §7.3 相同。
- 部門版 `φ^u_{jk}`、chargeback `τ`、`C^{impl,x}` 沿用 [06 §8.1]。

**工程面啟用時的 `C^{impl}` 細化 [ENG-REF]：**

$$
C^{impl}_{jk}(s) = C^{noneng}_{jk}(s) + C^{eng,direct}_{jk}(s),\qquad
C^{eng,direct}_{jk}(s) = \sum_{\text{deliverable WP } b \text{ of } (j,k)} \text{Price}_b
$$

`C^{eng,direct}` 只包含**交付型**工作包（固定總價、不以工程工時記容量）；**容量型**工作包的人力費用不得留在 `C^{impl}`（§11.7）。工程面停用時，`C^{impl}` 照 06 原義，不拆分。

---

## 8. 企業目標

**沿用的企業目標（工程面停用；PLANE_OFF）：**

$$
F_E(y,y^{loc},\gamma,q) = \sum_{j}\sum_{k} q_{jk}\,\varphi_{jk}(s) - \sum_c F_c\,(y_c - y^{cur}_c) - \sum_u\sum_c F^{loc}_{uc}\,y^{loc}_{uc} - \Delta C^{gov}(\gamma) \tag{OBJ-E, [06]/[74]}
$$

**工程面啟用（ENDOGENOUS_ENGINEERING_REGIME）[ENG]：**

$$
F_E^{ENG}(y,y^{loc},\gamma,q,n,K^{ext},\chi) = F_E(y,y^{loc},\gamma,q) - \sum_{w\in W^{ENG}}\underbrace{\big[C^{int}_w(n_w) - C^{int}_w(n^{cur}_w)\big]}_{\Delta C^{int}_w} - \sum_{w\in W^{ENG}} C^{ext}_w(K^{ext}_w,\chi_w) \tag{OBJ-E-ENG}
$$

- `OBJ-E` 的形式、項目與語意不變；工程面只**附加**兩個增量成本項。
- 人力成本以相對現有人力的增量計價，與 06 把 `F_c` 以 `y − y^{cur}` 計價的「相對現況增量」語意一致。現有人員的成本在 06 中原本就是沉沒成本，不在 `F_E` 中；本輪不改變這一點。
- 不重複扣除：容量型工程人力不在 `φ_{jk}`（`C^{impl}`）中，也不在 `F_c` 中（§11.7），所以 `ΔC^{int}` 與 `C^{ext}` 是它們唯一的貨幣位置。
- 若 `λ_ℓ` 未識別，沿用 06 §7.4 的兩分量報告與 `λ` 盒掃描；工程成本項不受影響。

---

## 9. 限制式

### 9.1 沿用（[06 §5]、[74 §3]，語意不變）

- (F1) one-hot：`Σ_{k∈K_j} q_{jk} = 1  ∀j`（`k=0` 為 status quo，所以「不做新專案」就是 `q_{j0}=1`；06 不允許整個 initiative 都不選）。
- (F2)–(F10)：法規、policy 允許、能力前提、要求表、有效控制、fallback、權限—配置一致、嚴重事件上限（以 `Ẽ` 計，[74]）、策略強制。
- 連結：`q_{jk} ≤ Φ_{jk}(y, y^{loc}, γ; θ)`。

### 9.2 資源（[06 §5.1]、[74]）

$$
a^{BUD}_{jk}(s) = C^{impl}_{jk}(s) + N_{jk}\tilde{\mathbb E}_{jk}[c] - N_{j0}\tilde{\mathbb E}_{j0}[c],\qquad a^{REV}_{jk} = N_{jk}\tilde{\mathbb E}_{jk}[t^{REV}] - N_{j0}\tilde{\mathbb E}_{j0}[t^{REV}]
$$

$$
\sum_c a^{BUD}_c y_c + \sum_{u,c} a^{BUD,loc}_{uc}y^{loc}_{uc} + \sum_{j,k} q_{jk}a^{BUD}_{jk} + \Delta C^{gov}(\gamma) \le \bar B \tag{R1-BUD, [06]}
$$

$$
\sum_{j\in J_u}\sum_k q_{jk}\,a^{REV}_{jk} \le \Delta\bar K^{REV}_u \tag{R2, [06]}
$$

`B̄` 保留 06 的原語意（AI 導入現金預算：`C^{impl}`、`F_c`、增量 `c`、治理），**不包含**人力。

### 9.3 工程容量（工程面停用：沿用 06）

$$
\sum_c a^{ENG}_c y_c + \sum_{u,c} a^{ENG,loc}_{uc}y^{loc}_{uc} + \sum_{j,k} q_{jk}a^{ENG}_{jk} \le \bar A^{ENG} \tag{R1-ENG-06, [06]}
$$

### 9.4 工程容量（工程面啟用）[ENG]

$$
\underbrace{\sum_{j,k} a^{ENG,w}_{jk}(s)\,q_{jk} + \sum_c a^{ENG,w}_c\,y_c + \sum_{u,c}a^{ENG,w,loc}_{uc}\,y^{loc}_{uc}}_{Dem_w(q,y,y^{loc})}
\le K^{fix}_w + K^{int}_w(n_w) + K^{ext}_w,\qquad \forall w\in W^{ENG}. \tag{R1-ENG-W}
$$

共享／本地能力的工程量不是 0；這些項在 06 已存在，只是本輪拆成技能。

### 9.5 人力下限與外部可得性 [ENG]

$$
n_w \in \mathbb Z_+,\qquad n_w \ge n^{cur}_w \tag{N-LB}
$$

$$
0 \le K^{ext}_w \le \bar K^{ext}_w\,\chi_w,\qquad \chi_w\in\{0,1\}. \tag{X-CAP}
$$

不允許 `n_w < n^{cur}_w`：模型沒有資遣成本、重新配置、預告期與組織擾動，若允許裁員會變成免費調整。這一版回答「**在既有人力上還要增加多少**」。

### 9.6 工程／人力預算 [ENG]

$$
\sum_w \big[\Delta C^{int}_w(n_w) + C^{ext}_w(K^{ext}_w,\chi_w)\big] \le \bar B^{ENG}. \tag{R-BENG}
$$

`B̄` 與 `B̄^{ENG}` 是兩個不同的預算池。若企業只有單一現金 envelope，可另做 **UNIFIED_BUDGET_REGIME** 敏感度：`B̄^{TOTAL}` 同時約束兩組現金流；canonical baseline 是分開的兩個池。不同制度的結果不得混用。

---

## 10. 共享能力

共享能力成本仍由 `F_c(y_c-y^{cur}_c)` 計價一次（[06]），並耗用 `a^h_c y_c`。工程面啟用時分技能：

$$
Dem^{cap}_{cw} = a^{ENG,w}_c \,(y_c - y^{cur}_c)_+ \tag{CAP-ENG, [ENG]}
$$

既有共享能力不應再次產生一次性 BUILD 工時；只保留其維運 RUN 需求。若能力的工作包本身是固定總價交付而非容量型，則該工作包只進 `F_c`、工時為 0（§11.7）。本地能力同理。

共享能力重用（06 §10）的 `δ_{jkc} = C^{impl}_{jk}(s_c=∅) − C^{impl}_{jk}(s_c=S)` 照舊；外部顧問或內部人力不額外得到「重用獎勵」，重用只透過較低 `a^{ENG,w}_{jk}(s)`、`C^{impl}` 或能力狀態的可行性出現。

---

## 11. ENGINEERING / SOURCING PLANE

### 11.1 工程需求

`a^{ENG,w}_{jk}(s)` 是技能別的「有效工程工時」。它由 initiative/configuration 的工程工作包加總；共享能力由 `a^{ENG,w}_c` 加總，本地能力由 `a^{ENG,w,loc}_{uc}` 加總。第一版每個技能都有獨立限制，不做跨技能替代（A-ENG-02）。

### 11.2 BUILD / RUN 與 planning-time regime

第一版把工作包的工程量分成：

- `h^{build,w}`：一次性實體 BUILD 工時；
- `h^{run,w}`：每期 RUN／維運實體工時。

**時間基礎（A-ENG-TIME-v1.1，AUTHOR_DEFINED）。** 金錢的財務年化與工程工時的實體容量不可混為一談。第一版明確分成兩個 planning-time regime：

1. **`IMPLEMENTATION_YEAR`（canonical staffing regime）**：所有本期新建的 BUILD 工時完整進入工程容量限制，RUN 工時也照當期完整計入：

$$
a^{ENG,w,impl}_{jk}(s)=h^{build,w}_{jk}(s)+h^{run,w}_{jk}(s),
$$

$$
a^{ENG,w,impl}_c=h^{build,w}_c\,(y_c-y^{cur}_c)_+ + h^{run,w}_c\,y_c.
$$

這一 regime 回答「**在導入年度，公司實際需要多少工程容量／FTE／外部顧問時數？**」；一次性的 2,000 個 BUILD 小時就是本年 2,000 個小時，不能因成本攤提而只剩一部分。

2. **`STEADY_STATE_LEVELIZED`（sensitivity only）**：只有在研究者明確要表達「長期穩態、每期持續有相似專案流」時，才把 BUILD 工時 levelize：

$$
a^{ENG,w,lvl}_{jk}(s)=AF(r_d,H_j)\,h^{build,w}_{jk}(s)+h^{run,w}_{jk}(s),
$$

$$
a^{ENG,w,lvl}_c=AF(r_d,H_c)\,h^{build,w}_c\,(y_c-y^{cur}_c)_+ + h^{run,w}_c\,y_c.
$$

它只作 staffing sensitivity，**不得**被解讀為 implementation-year peak feasibility，也不得用來取代 canonical `IMPLEMENTATION_YEAR` 的人數結論。`AF` 只是把一次性 BUILD demand 轉成長期 levelized workload 的作者定義近似；不是把「時間」當成金錢。

**financial annualization ≠ physical capacity annualization。** `C^{impl}=O\cdot AF+Rec`、招募／到職等一次性**貨幣成本**仍可用年金因子作財務年化；但 canonical staffing feasibility 不可因此把一次性的 BUILD 實體工時攤薄。`STEADY_STATE_LEVELIZED` 只作敏感度檢視，任何由它得到的人數不得冒充 implementation-year headcount。06 對 `a^{ENG}` 只寫 `hours/period`；v1.1 將 BUILD/RUN 與這兩種 planning-time interpretation 顯式分開，而不修改 06 原式。

### 11.3 內部容量與成本

canonical 使用一般函數：

$$
K^{int}_w(n_w),\qquad C^{int}_w(n_w).
$$

它們可由 HR／專案工時／財務資料估計。模型不假設每名工程師都有相同產能，也不假設成本線性。線性特例（LINEAR CAPACITY SPECIAL CASE）才寫：

$$
K^{int}_w(n_w) = n_w\,Q^{nom}_w\,\eta_w,\qquad C^{int}_w(n_w) = n_w\,\nu^{FTE}_w.
$$

`η_w` 包括會議、文件、incident、支援、休假等造成的有效專案時間折減；**企業值不得填通用的 0.55–0.75 等「常識範圍」**，必須 OBSERVED／ELICITED／SCENARIO。

### 11.4 內部人員的一次性成本

若 `ν^{FTE}_w` 是每期 fully-loaded 成本，招募與到職的一次性成本可在**成本帳本**內依預期任期財務年化（與 physical hours 分開）：

$$
\nu^{FTE}_w = \nu^{run,FTE}_w + AF(r_d,H^{ten}_w)\,\nu^{once,FTE}_w.
$$

這仍是 single-period 的等值成本；**不代表**招募時間或到職期間的實體容量可以同樣年化。招募 lag 與 onboarding capacity ramp 仍屬多期擴充（§19）。

### 11.5 固定既有容量

`K^{fix}_w` 只放「不是 FTE 的既有容量」（例如已簽的不可調整合約）。現有 FTE 全部在 `n^{cur}_w`，它們的容量由 `K^{int}_w(n^{cur}_w)` 提供；不得又放進 `K^{fix}`。

### 11.6 兩個預算池

- `B̄`：保持 06 的導入現金預算（`C^{impl}`、`F_c`、增量 `c`、治理）；
- `B̄^{ENG}`：增量內部人力＋容量型外部採購。

若原始預算文件把容量型工程費用放在專案預算內，資料載入時必須先重編到 `B̄^{ENG}`；不重編會讓同一筆現金同時佔用兩個 budget pools（不是 objective double counting，但仍是 budget double consumption）。121 登記此規則。

SEPARATE_BUDGET_REGIME 與 UNIFIED_BUDGET_REGIME 的結果分開報告，不得混用。v1.0 只定義 UNIFIED，沒有在 123／125 中執行。

### 11.7 ENGINEERING COST OWNERSHIP RULE

每個工程工作包只有兩種互斥的經濟處理：

| 類型 | 實體／容量記錄 | 貨幣位置 | 不得出現 |
|---|---|---|---|
| **容量型 CAPACITY** | `a^{ENG,w}` 工時 | `ΔC^{int}_w` 或 `C^{ext}_w`（看容量來源） | `C^{impl}`、`F_c` 的人力費用、`λt` |
| **交付型 DELIVERABLE** | `a^{ENG,w}=0` | initiative → `C^{impl}`；shared capability → `F_c` | `C^{int}`／`C^{ext}` 的工程容量費用 |

同一工作包不可同時屬於兩類。`O_{jk}`、`Rec_{jk}`、`F_c` 在工程面啟用時須排除所有容量型人力費；API／inference 仍在 `c`；業務人員訓練（變更管理）可進共享 `F_CHG` 或部門 `Rec`；重工的結果損失仍在 `l`。監控與維護依工作包性質選一類。

**LEDGER_AMBIGUITY_06_ENG（解析方式）。** 06 的 `C^{impl}` 包含 integration／monitoring／maintenance 等，未說明其中是否含工程人力費；在 06 中內部人力是沉沒成本，所以沒有重複計價。工程面啟用後，本節只作**新增面的帳本細化**；工程面停用時 06 的原帳本完整保留，不回溯修改。

### 11.8 外部容量

LINEAR_EXTERNAL_COST baseline：

$$
C^{ext}_w(K^{ext}_w,\chi_w) = F^{ext}_w\chi_w + \nu^{ext}_w K^{ext}_w.
$$

`K^{ext}_w ≤ K̄^{ext}_w χ_w`。若採分段價格，未來以 piecewise linear 取代，不改其他方程。外部顧問的「較快」或「專長」若有資料，只能透過較高有效容量、較低 `a^{ENG,w}`、可行配置、工期或交付成本進入；不得新增 `ConsultantBonus`。

在 85 的組織映射中，`D07 = EXTERNAL_CAPACITY` 時由 `D07a` 判定外部產能由誰調度：企業／IT／AI 專責單位調度 → leader 決定 `K^{ext}_w`；事業單位調度 → 屬於 C-ENG-LOCAL（v1.0 未定義，§12.4）。

### 11.9 內部知識與長期價值

不得加 `KnowledgeRetention` 或 `InternalCapabilityBonus`。若內部團隊真的帶來長期優勢，只能在未來期間透過較低的維護／導入工時、能力重用、較低採購依賴等**可量化的後續項目**進模型（§19）。single-period v1.0 不加分。

### 11.10 技能不可替代

每個 `w` 都有獨立的 R1-ENG-W，不可用多出的 DATA 小時抵 AI_LLM 小時。這是 `AUTHOR_DEFINED_SKILL_NON_SUBSTITUTION_ASSUMPTION`（A-ENG-02），不是經驗事實。cross-skill productivity／substitution matrix 留給 future extension。

---

## 12. A／A+／B／C／C0／D

### 12.1 三種工程制度（必須分開報告）

| 制度 | 工程資源語意 | staffing/sourcing | 比較量名稱 |
|---|---|---|---|
| `PLANE_OFF` | 06 的單一池化工程資源 `Ā^{ENG}` | 外生固定 | **只在此制度**使用 06 的原始名稱 `VRA, VCP, VSC, DL, NEV...` |
| `SKILL_FIXED` | 按技能拆分；`n=n^{cur}`、外部停用 | 外生固定但技能不可替代 | 同樣差值一律加 `^{W,fix}`（例如 `VSC^{W,fix}`），不得冠 06 原名 |
| `ENDOGENOUS` | 按技能拆分 | 企業可增聘、買外部容量 | `^{ENG}`（例如 `VSC^{ENG}`）；若缺 A-ENG，涉及 A 的量為 `NOT_COMPARABLE` |

因此跨制度的數值變化只表示**資源制度改變**，不得寫成同一模型下的 improvement / deterioration。尤其 `VSC^{W,fix}` 不等於 06 的 `VSC`。

- **單技能退化（single-skill collapse）。** 若 `|W^{ENG}|=1`、該技能的需求與容量逐項等於 06 的單一 `ENG` 需求與 `Ā^{ENG}`，且外部容量停用，則 `SKILL_FIXED` 與 `PLANE_OFF` 的可行集合完全相同：`\mathcal F^{W,fix}=\mathcal F^{OFF}`，因此 B、A+、C、C0、A 的最適值以及 VRA、DL0、VCP、VSC、DL、NEV 對應值必須逐一相等。這是 v1.1 的 backward-refinement collapse test（124 acceptance test 17）。

### 12.2 Model A（不修改）

維持部門獨立決策：固定 `B^0_u`、固定 `K^{ENG,0}_u`（PLANE_OFF 下為合併的 `Σ_w [K^{fix}_{uw} + K^{int}_w(n^{cur}_{uw})]`；SKILL_FIXED 下依技能為 `K^{fix}_{uw} + K^{int}_w(n^{cur}_{uw})`）、`y ≡ 0`、`γ = γ^{cur}`，各部門解 OBJ-U，以 OBJ-E 評估。**不修改** A 的固定預算與固定工程資源假設。部門可自行聘人或簽約的版本另設 **A-ENG** extension，v1.0 只命名、不定義；在內生制度下 A 標 `NOT_COMPARABLE`，不得與 B、C 相減。

### 12.3 Model A+／B

- **A+**：中央規劃 `q, y^{loc}`、policy 固定，`y ≡ 0`；工程面啟用時企業也選 `n_w, K^{ext}_w, χ_w`。
- **B**：中央規劃 `q, y, y^{loc}, γ`；工程面啟用時再選 `n, K^{ext}, χ`，解 OBJ-E-ENG。

這符合 85 的集中決策語意；不新增外部 optimizer。

### 12.4 Model C／C0

leader 選：

$$
(y,\gamma,e^{BUD},e^{ENG,w},n,K^{ext},\chi)
$$

（C0 固定 `y ≡ 0`）。BU follower 仍只選 `(q_u, y^{loc}_u)`，遵守技能別 `e^{ENG,w}_u`。leader 的 envelope 維度由 `{BUD, ENG}` 擴為 `{BUD} ∪ W^{ENG}`；06 的 Lemma E′ 對 envelope 維度無關（§14.2 有付費容量下的延伸證明）。

BU 自行聘人或自行簽外部合約屬 **C-ENG-LOCAL** extension；本輪不加。

### 12.5 Model D

工程面本身不會創造 Model D。仍須 T1–T5 全成立，才把使用者視為第三層 optimizer；否則 `α／ρ` 仍是行為分布（06 §9.2、85 M-R15）。

### 12.6 比較的資源制度

06 §11 的 VRA／VCP／VSC／DL／NEV 要求可比較模型面對同一資源基礎：

- **FIXED_ENGINEERING_REGIME（PLANE_OFF）**：原比較量完全有效（§16.1）。
- **SKILL_FIXED**：以 `^{W,fix}` 另報，不能寫成 06 的 VSC/VCP/DL/NEV。
- **ENDOGENOUS_ENGINEERING_REGIME**：B／A+／C／C0 都可增聘／外購；使用帶 `^{ENG}` 的新比較量（§16.2）。A 在 A-ENG 定義前標 `NOT_COMPARABLE`，所以含 A 的 VRA／VCP／NEV 不報。

---

## 13. 邊際成本與邊際價值

### 13.1 內部工程邊際成本

$$
MC^{int}_w(n+1) = \frac{C^{int}_w(n+1)-C^{int}_w(n)}{K^{int}_w(n+1)-K^{int}_w(n)}.
$$

單位 TWD/effective engineering hour。分母 `≤ 0` 時標 `UNDEFINED`，不得除以 0 或把協調損失隱藏。線性特例才有 `MC^{int}_w = ν^{FTE}_w/(Q^{nom}_w η_w)`。

### 13.2 外部邊際成本

LINEAR_EXTERNAL_COST：`MC^{ext}_w = ν^{ext}_w`。retainer `F^{ext}_w` 是啟用時的固定成本，不是邊際成本。分段價格時 `MC^{ext}_w(x)` 為該段斜率。

### 13.3 一名工程師的邊際價值

令 `F_E^*(n)` 為固定人力向量 `n` 時，其餘所有變數（`y, y^{loc}, γ, q, K^{ext}, χ`；C 中含 envelope）最適化後的 OBJ-E-ENG 值。定義毛價值（不扣 `w` 類人力成本）：

$$
V^{gross}_w(n) = F_E^*(n) + \Delta C^{int}_w(n_w)
$$

$$
MV^{gross}_w(n+1) = V^{gross}_w(n+\mathbf 1_w) - V^{gross}_w(n),\qquad MV^{net}_w(n+1) = F_E^*(n+\mathbf 1_w) - F_E^*(n)
$$

**恆等式。** 由 `V^{gross}` 的定義（給定 `n` 時人力成本是常數），

$$
MV^{net}_w(n+1) = MV^{gross}_w(n+1) - \big[C^{int}_w(n_w+1) - C^{int}_w(n_w)\big]
$$

是定義上的恆等式（125 逐列列出以供核對，不作為經驗檢驗）。聘用的損益兩平條件 `MV^{net}_w(n+1) ≥ 0` 等價於 `MV^{gross}_w(n+1) ≥ ΔC^{int}_w(n_w → n_w+1)`。

**不要只比較「薪資÷工時」與「顧問時薪」。** 新增容量可能解開原本不可行的高價值專案或共享能力（例如共享 LLM 服務），使 `MV^{gross}` 遠大於該容量的替代成本；反過來，容量若用不完，`MV^{gross}` 可能為 0。

**多技能時的報法。** (i) 偏邊際：其他技能固定在最適值 `n^*_{−w}`；(ii) 重新最適化：其他技能同時重解。兩者分開報告。

---

## 14. 團隊規模最適化

### 14.1 定義

$$
\boxed{n^* \in \arg\max_{n\ge n^{cur}} F_E^*(n)}
$$

報告：最適人數、總有效容量、容量使用率、未使用容量、`MV^{gross}`、`ΔC^{int}`、`MV^{net}`、`MC^{int}`，以及 `n = n^{cur}, n^{cur}+1, …` 的敏感度表。

**報告規則。** 整數 portfolio 使 `F_E^*(n)` 一般不是凹函數，可能跳躍。「第一個 `MV^{net}(n+1) < 0` 的 `n`」只作診斷，**不得**宣稱為最適人數；最適人數一律以 `argmax` 定義。

### 14.2 求解架構：外層列舉人力，內層解 portfolio（OPTION 2）

```
for n in staffing grid (n ≥ n_cur):
    capacity_w = K_fix_w + K_int_w(n_w)
    inner: solve the existing portfolio problem (B / A+ by enumeration; C / C0 by follower enumeration + Lemma E′)
           with the cost-minimal external purchase K_ext_w = max(0, Dem_w − capacity_w)
    F*(n) = inner value − ΔC_int(n)
n* = argmax F*(n)
```

**為什麼不採 OPTION 1（內生整數人力的 MILP）。** (i) C／C0 的下層是整數雙層問題，KKT 單層化不成立（06 §12.1），需要重寫求解器；(ii) OPTION 2 不需要重寫 51，可保持 v2.2／v2.4 求解器的隔離；(iii) 邊際價值是相鄰 `n` 的直接差；(iv) 迴歸測試簡單。OPTION 1 保留為大規模時的未來選項。

**精確性。**

1. *外部採購的內層最佳化。* 給定 `n` 與 portfolio，`C^{ext}_w` 對 `K^{ext}_w` 非遞減（非負線性價格加啟用費），所以成本最小的購買量是 `K^{ext}_w = \max(0, Dem_w − K^{fix}_w − K^{int}_w(n_w))`，且 `χ_w = 1[K^{ext}_w > 0]`；購買更多不會改善目標。超過 `K̄^{ext}_w` 則該組合不可行。
2. *人力網格是完整的。* 在 `C^{int}_w` 非遞減、`ν^{FTE}_w > 0`、且 `C^{ext}_w ≥ 0` 的條件下，(R-BENG) 使 `ΔC^{int}_w(n_w) ≤ B̄^{ENG}`（其他技能的 `ΔC^{int}` 與外部成本都非負）；線性成本下 `Δn_w ≤ ⌊B̄^{ENG}/ν^{FTE}_w⌋`。若未來的外部價格有最低購買量，`\max(0,·)` 的規則須改為在可購買量集合上取最小成本。以此為上界列舉，網格涵蓋所有可行的 `n`，所以外層列舉是精確的（124 的預設）。若研究者另外截斷網格，最適解落在截斷邊界時輸出 `GRID_BOUNDARY_HIT`。
3. *Lemma E′ 在付費容量下仍成立（C、C0）。* 06 的 Lemma E′ 證明「把 envelope 換成部門最適計畫的資源向量 `a(x)`」不會使 leader 變差，因為資源使用不增加。工程面啟用後，leader 的外部採購成本 `Σ_w C^{ext}_w(\max(0, Σ_u e^{ENG,w}_u + … − capacity_w))` 以及 `B̄^{ENG}`、`K̄^{ext}_w` 兩個限制對 envelope 使用量都是非遞減的，所以資源使用不增加時成本不增加、可行性不變差；optimistic 值不變、pessimistic 值弱增的原論證照舊成立。證明與 envelope 的維度無關。124 的接受測試 13 以乘積 envelope 集合交叉檢查（SIMULATED_ONLY）。

### 14.3 與 51 的相容性

51 把 `H^pool` 寫死為 `{BUD, ENG}` 兩個維度，無法直接處理多技能。因此：

- 多技能的工程面只在 124（獨立參考實作）中實作；51、65 不修改。
- 單一技能（`|W^{ENG}| = 1`）且不允許外部採購時，51 可作為內層求解器：`F_E^*(n) = F_E^{51}(\bar A^{ENG} = K^{fix} + K^{int}(n)) − ΔC^{int}(n)`。
- 回溯一致性檢查（125 的 CROSSCHECK_51）：124 以唯讀 adapter 讀入 51 的實例與 51 自己的計畫表，再以 **124 自己的** `solve_B`、`solve_C`、`solve_A`（PLANE_OFF 制度）求解，與 51 的 B、A+、C（opt／pess）、C0（opt／pess）與每個 policy 下的 A（含 NotComparable／ModelAInfeasible 狀態）逐一比較；另以 124 的工程面（單一技能、外部停用）驗證上式對 B 與 C-pess 成立。14 個實例（10 個隨機實例、3 個 51 的手算 oracle 實例、1 個 opt ≠ pess 的 tie 實例），共 386 個比較，全部一致（SIMULATED_ONLY；此 51 crosscheck 為 v1.6 已認證快照，v1.6.1 的 Adapter51/load51/crosscheck51 路徑未修改；本輪 fresh regression 為 time-regime 與 single-skill collapse）。這個檢查涵蓋 124 的最適化與評估程式；計畫表本身由 51 產生，因此它不另外檢驗 124 的 (X1′) 期望計算（後者由接受測試 1 的恆等式檢查）。

---

## 15. 外部採購

### 15.1 外部採購價值

$$
V^{EXT} = F_E^*(\text{external sourcing allowed}) - F_E^*(K^{ext}_w \equiv 0\ \forall w)
$$

`V^{EXT} ≥ 0`（禁止外部只縮小可行集合）。它是「外部工程市場的可得性」對最佳企業價值的增量，**不是**顧問品質分數。可另報兩種條件版本：人力可調整時，以及人力固定在 `n^{cur}` 時。

### 15.2 BUILD／BUY／HYBRID／NONE（由最適解推導）

| 標籤 | 條件（相對現有人力） |
|---|---|
| BUILD | `n^*_w > n^{cur}_w`，`K^{ext*}_w = 0` |
| BUY | `n^*_w = n^{cur}_w`，`K^{ext*}_w > 0` |
| HYBRID | `n^*_w > n^{cur}_w`，`K^{ext*}_w > 0` |
| NONE | `n^*_w = n^{cur}_w`，`K^{ext*}_w = 0` |

標籤逐技能報告，不得轉成任意分數。顧問費率與 retainer 的損益兩平以網格掃描報告（123、125；SIMULATED_ONLY）。

### 15.3 組織型態與外部採購分開

組織導入 archetype（O1–O5）與外部採購方式是兩個不同的維度：IT 主導＋外部 SI、AI 專責單位＋混合採購、種子人員帶動＋中央 AI 工程團隊、聯邦式＋事業單位工程師都可能成立。不得把 O4（外部夥伴主導）等同於 BUY。archetype 不是任何方程的輸入（`org_schema.validate_codes` 拒收）。

---

## 16. 反事實比較量

### 16.1 PLANE_OFF（與 SKILL_FIXED）

PLANE_OFF 下，06 §11.1 的比較量名稱、定義與語意完全不變：`VRA = F^{C0} − F^{A}`、`DL0 = F^{A+} − F^{C0}`、`VCP = F^{A+} − F^{A} = VRA + DL0`、`VSC = F^{B} − F^{A+}`、`DL = F^{B} − F^{C}`、`NEV = F^{C} − F^{A}`、`VG(γ)`。P1–P8 照舊。SKILL_FIXED 下同一組差值加 `^{W,fix}` 標記另報；它與 PLANE_OFF 的差異完全來自技能不可替代的假設（A-ENG-02）。

### 16.2 ENDOGENOUS_ENGINEERING_REGIME

| 名稱 | 定義 | 備註 |
|---|---|---|
| `VSC^{ENG}` | `F^{B,ENG} − F^{A+,ENG}` | 兩者都可內生人力 |
| `DL^{ENG}` | `F^{B,ENG} − F^{C,ENG}`（opt／pess） | C 的 leader 決定中央人力與外部採購 |
| `DL0^{ENG}` | `F^{A+,ENG} − F^{C0,ENG}` | — |
| `VRA^{ENG}`、`VCP^{ENG}`、`NEV^{ENG}` | `NOT_COMPARABLE` | 需要 A-ENG；v1.0 未定義 |
| `V^{EXT}` | §15.1 | — |
| `V^{ENG\_POOL}` | `F^{B,ENG}(\text{pooled}) − F^{B,ENG}(\text{BU-separated})` | 見 §16.3 |

**P1-ENG（排序）。** 在內生制度下、各模型面對相同的人力與外部選項時：`F^{C0,ENG,mode} ≤ F^{A+,ENG} ≤ F^{B,ENG}`，`F^{C0,ENG,mode} ≤ F^{C,ENG,mode} ≤ F^{B,ENG}`。*證明：* 與 06 P1 相同：C0 的任何 (leader, follower) 組合連同其 `(n, K^{ext}, χ)` 在 A+ 中可行；A+ 的可行集合是 B 的子集合；C 的 leader 可選 `y = 0`；C 的任何組合在 B 中可行。人力與外部採購在各模型中都由企業層決定，不影響包含關係。∎

**P2-ENG（對齊 ⇒ 零授權損失）。** 若 (AL1)–(AL4) 成立，則 `F^{C,ENG,opt} = F^{C,ENG,pess} = F^{B,ENG}`。*證明：* 取 B 的最適 `(n^*, K^{ext*}, χ^*)` 與 portfolio；C 的 leader 採用同一 `(n^*, K^{ext*}, χ^*)`，並設 `e_u = a(x^*_u)`（含技能別工程分量），其餘同 06 P2。∎

**P-EXT。** `V^{EXT} ≥ 0`。∎

### 16.3 工程池化價值 `V^{ENG_POOL}`

兩個反事實必須明確定義：

- **pooled（中央池化工程）：** 單一組技能容量 `K^{fix}_w + K^{int}_w(n_w) + K^{ext}_w`，供所有部門與共享能力使用。
- **BU-separated（部門分隔工程）：** 每個部門 `u` 有自己的 `n_{uw} ≥ n^{cur}_{uw}`、自己的固定容量 `K^{fix}_{uw}`、自己的外部採購與 retainer，以及自己的容量限制 `Σ_{j∈J_u,k} a^{ENG,w}_{jk}q_{jk} + Σ_{c: host(c)=u} a^{ENG,w}_c y_c ≤ K^{fix}_{uw} + K^{int}_w(n_{uw}) + K^{ext}_{uw}`；外部市場的可得容量是全企業共用的 `Σ_u K^{ext}_{uw} ≤ K̄^{ext}_w`。共享能力的工程量由其**承載部門** `host(c)` 負擔（AUTHOR_DEFINED_HOSTING_RULE，只用於這個反事實）。人力成本與 `B̄^{ENG}` 是企業總額。

**P-POOL。** 在下列條件下 `V^{ENG_POOL} ≥ 0`：(a) 線性容量 `K^{int}_w(n) = n Q^{nom}_w η_w` 與線性人力成本；(b) 現有人力是部門現有人力的分割，`Σ_u n^{cur}_{uw} = n^{cur}_w`；(c) 既有固定容量也是分割，`Σ_u K^{fix}_{uw} = K^{fix}_w`；(d) 外部市場對每個技能只有一個可得容量上限，部門分隔時 `Σ_u K^{ext}_{uw} ≤ K̄^{ext}_w`；(e) 兩個反事實的 portfolio、能力與預算限制相同。*證明：* 任一部門分隔方案 `(n_{uw}, K^{ext}_{uw})` 可由池化方案 `n_w = Σ_u n_{uw} ≥ n^{cur}_w`、`K^{ext}_w = Σ_u K^{ext}_{uw} ≤ K̄^{ext}_w` 複製：由 (a)(c) 池化容量等於分隔容量之和，人力成本相同，外部變動成本相同，retainer 只付一次（≤ 分隔下的總額）。∎ 若 (b)–(d) 不成立，差值可能為負（例如部門各自擁有完整的外部可得容量），或把固定容量的價值錯記為池化價值；非線性容量（例如團隊規模的協調損失）下也不保證，需另行掃描。124 的接受測試 14 在基準實例、審查者提出的區辨案例（若錯把外部可得容量給每個部門各一份，部門分隔的價值會被高估；該測試確認共用上限在此案例中確實綁住）與固定容量分割案例上檢查此性質（SIMULATED_ONLY）。

**不得混用或分解。** `V^{ENG_POOL}` 不與 VCP、VSC、DL、NEV 合併，也不做加法分解：它比較的是「同一集中規劃者、不同的工程組織方式」，與 06 的比較量處理的是不同的反事實。

---

## 17. 假設

| ID | 假設 | 類型 | 若不成立 |
|---|---|---|---|
| A-ENG-01 | 技能類別 `W^{ENG}` 為作者定義的操作性類別 | AUTHOR_DEFINED_OPERATIONAL_CATEGORY | 依企業職務紀錄重新登記 |
| A-ENG-02 | 技能之間不可替代 | AUTHOR_DEFINED_SKILL_NON_SUBSTITUTION_ASSUMPTION | 需要跨技能替代矩陣 |
| A-ENG-03 | 不允許減少既有人力（`n_w ≥ n^{cur}_w`） | STRUCTURAL（使用者決策） | 需要資遣、重新配置與擾動成本（多期） |
| A-ENG-04 | 兩個預算池：`B̄` 與 `B̄^{ENG}` | STRUCTURAL（backward compatibility） | UNIFIED_BUDGET_REGIME 作 sensitivity |
| A-ENG-05 | 容量型與交付型工作包互斥（ownership rule） | LEDGER | 重複計算 |
| A-ENG-06 | planning-time regime 分離：`IMPLEMENTATION_YEAR` 用完整 BUILD + RUN 實體工時作 canonical staffing；`STEADY_STATE_LEVELIZED` 才以 `AF` levelize BUILD 作敏感度；貨幣成本可獨立財務年化 | TIME_BASIS | 期內尖峰、招募延遲與跨期 sequencing 仍需多期模型 |
| A-ENG-07 | 線性容量與線性成本只是特例 | SPECIAL_CASE | 使用一般的 `K^{int}`、`C^{int}` |
| A-ENG-08 | 外部採購為線性價格加 retainer | LINEAR_EXTERNAL_COST | 分段價格 |
| A-ENG-09 | 外部市場容量以 `K̄^{ext}_w` 表示；其內品質與內部相同（每有效工時） | IDENTIFICATION | 品質差異須以 `a^{ENG,w}`（有效工時）或交付型處理，不得加分 |
| A-ENG-10 | C 中只有企業可聘人或簽約 | STRUCTURAL | C-ENG-LOCAL extension |
| A-ENG-11 | 部門分隔反事實的共享能力承載部門；現有人力與固定容量依部門分割；外部可得容量全企業共用 | AUTHOR_DEFINED_HOSTING_RULE | 只影響 `V^{ENG_POOL}` |
| A-ENG-12 | 三種制度（PLANE_OFF／SKILL_FIXED／ENDOGENOUS）分開報告；06 比較量名稱只用於 PLANE_OFF | REPORTING | 名稱誤用會把技能不可替代的效果誤記為 06 結果 |

既有假設（85／86 的 A-ORG-01 至 A-ORG-14、06 的完全資訊與 (AL) 條件、74 的 (C1)–(C3′)、(A-INV)）全部沿用。

---

## 18. 限制

- 所有參數目前為 `UNIDENTIFIED`；123／125 的數字全部是 `SIMULATED_ONLY`，不是企業結果、不是實證結果。
- `IMPLEMENTATION_YEAR` 以完整 BUILD + RUN 工時檢查導入年度的總實體容量，但單期模型仍無法表示招募延遲、到職訓練、合約期間、留任、學習與重用的動態，也不表示月／季內尖峰排程一定可行。
- `STEADY_STATE_LEVELIZED` 隱含穩態專案流，只是長期平均容量敏感度；它不得作為一次性導入年度的人力可行性證據。
- 完全資訊假設（06 P3）使 `F^B ≥ F^C`；分權的資訊優勢不在模型內，工程面不改變這一點。
- 技能不可替代、線性容量與線性成本是簡化。
- `η_w`（有效使用率）與 `K̄^{ext}_w`（外部可得容量）難以觀察，可能是主要的識別難點。
- 工程需求 `a^{ENG,w}` 通常只能引出區間；新的不確定因子（工程需求、有效容量、FTE 成本、顧問費率、外部可得性）**沒有**放入 51 的穩健性登錄表，工程面結果目前只報點值與敏感度，不得宣稱 ROBUST。之後另做 Engineering Robustness Extension。
- 影子價格 `μ^{ENG}_w`（工程容量限制的對偶值）只在連續放寬且對偶解釋適用時定義；混合整數解不得直接把 solver dual 當成完整的經濟影子價格，主要方法是有限差分（§13.3）。
- 文獻層級的關聯（G01–G16 的 O/E、q）不得變成企業權重（06 §1.3 第 6 條，不變）。

---

## 19. 多期擴充（future extension；不進 v1.1 canonical）

期間索引不得使用 `t`（每事件工時）、`T`（觀察期間）、`τ`（06 的門檻變體與 chargeback）或 `ν`（本檔的價格）。暫定 **`ψ ∈ \{1,…,Ψ\}`**（`ψ`、`Ψ` 在 06、74、75、89、118 中皆未使用），下一版正式採用前須再做一次符號稽核。需要的元素：

- 招募延遲與到職：期間 `ψ` 決定的聘用，在 `ψ + L_w` 才提供完整容量；到職訓練期的有效容量折減。
- 合約期間：外部 retainer 的最短期限與終止條件。
- 留任與流失：人力的期間動態。
- 學習與重用：未來的 `a^{ENG,w}` 隨已建能力下降（以能力來源狀態 `s` 的跨期演變表示，不加分）。
- 維運：已部署配置在後續期間的 `a^{ENG,w,run}`。
- 減編與重新配置：資遣成本、預告期、組織擾動（解除 A-ENG-03 的前提）。
- 折現：沿用 06 的 `r_d`。
- 與 06 §16 M5（`ξ_t` 狀態）整合。

---

## 附錄 A：方程變更分類

| 方程 | 狀態 |
|---|---|
| V1、X1、F1–F10、R1-BUD、R2、OBJ-U、AL1–AL4、Lemma E′、P1–P8、06 §11.1 比較量、T1–T5、§13 穩健性 | **UNCHANGED**（06） |
| X1′、V2′、74 §5 成本歸屬、noai_route、缺值語義 | **UNCHANGED**（74 候選語意） |
| `C^{impl} = C^{noneng} + C^{eng,direct}`；`F_c` 的同類拆分 | **ENG-REF**：只在工程面啟用時適用；停用時 06 原義 |
| R1-ENG-06 | **REPLACED WHEN ENABLED** by R1-ENG-W；停用時（PLANE_OFF）不變 |
| OBJ-E-ENG、R1-ENG-W、N-LB、X-CAP、R-BENG、MC、MV、`n^*`、`V^{EXT}`、`V^{ENG_POOL}`、P1-ENG、P2-ENG、P-EXT、P-POOL、Lemma E′ 在付費容量下的延伸 | **NEW** |
| 06 §11.1 比較量 | 只在 PLANE_OFF 使用 06 名稱；SKILL_FIXED 加 `^{W,fix}`；ENDOGENOUS 加 `^{ENG}`，A 為 NOT_COMPARABLE |

## 附錄 B：本檔的閘門判定

由 126 判定。
