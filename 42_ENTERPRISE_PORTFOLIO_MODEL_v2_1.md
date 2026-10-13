# Enterprise AI Portfolio Multilevel Optimization Model v2.1

**狀態：v2.1 canonical candidate model，2026-10-10。** 本檔把 `04_ENTERPRISE_MODEL_SPEC_v2_0.md`／`39_ENTERPRISE_MULTILEVEL_MODEL_AND_DATA_CONTRACT_v2_0.md` 的候選規格形式化為可直接實作的有限離散模型，並以 `41_G01_G16_CONVERGENCE_AND_CONSTRUCT_FREEZE_v2_1.md` 的構念架構為上位對應。所有數值參數目前均為 `UNIDENTIFIED`；本檔不含任何企業估計值。參考實作見 `46_enterprise_portfolio_solver_v2_1.py`（synthetic only），其執行紀錄見 `47_SOLVER_ORACLE_RUN_v2_1.txt`：P1、P2、P4（`F_c` 與 `δ`）、P5、P6、P7（B）、P8（C 中的篩選反例）、Lemma E、帳本恆等式、ties、缺值拒算與 (F9) 均在 SIMULATED_ONLY 實例上未被反駁。本檔在 Phase F 對抗式稽核後修訂（見 §19）。

閱讀順序：§1 慣例 → §2 集合 → §3 參數 → §4 決策變數 → §5 可行性 → §6 期望算子 → §7 帳本與企業目標 → §8 部門目標 → §9 使用者反應層 → §10 共享能力耦合 → §11 組織型態比較 → §12 求解程序 → §13 不確定性與穩健性 → §14 研究問題的計算量 → §15 命題 → §16 M5 動態擴充 → §17 A/B 模型選擇紀錄 → §18 輸出契約。

---

## 1. 慣例

### 1.1 單位

| 型別 | 符號 | 允許運算 |
|---|---|---|
| `TWD/event` | 小寫 `v, l, c` | 乘以 `events/period` 後成 `TWD/period` |
| `TWD/period` | 大寫 `F, C, B` | 加減 |
| `hours/event` | `t` | 乘以 `events/period` 成 `hours/period`；乘以 `TWD/hour` 成 `TWD/event` |
| `hours/period` | `K` | 加減、與容量比較 |
| `TWD/hour` | `λ` | 時間換算 |
| `events/period` | `N` | 乘法 |
| `incidents/period` | `ē` | 與期望事件數比較 |
| probability | `π, P, ρ, I` | 非負、正規化；作期望權重 |
| ordinal key | `A, H, WI, EA, EAX, G, R, D, κ` | **只允許** `≥` 比較與查表索引 |
| nominal | `m, γ, ℓ, z, ω, r` | 只作索引 |
| binary | `y, q, Legal, Allow, Eff_H, FB, Cons` | 0/1 |

觀察期間 `T` 固定；所有 `/period` 量使用同一 `T`。一次性成本以年金因子攤提（§3.4）。

### 1.2 Provenance

每個參數格附 `provenance ∈ {OBSERVED, EXPERT_ELICITED, PUBLIC_OBSERVED, SCENARIO_SENSITIVITY, SIMULATED_ONLY, UNIDENTIFIED}`。`EXPERT_ELICITED` 另附 `source_scope ∈ {internal, external}`；external 指董事端、合作商或投資端的評估者，**他們是參數界定與挑戰來源，不是模型中的決策者**。

### 1.3 不允許的運算（實作必須拒絕）

1. 任何 ordinal 值進入算術式。
2. `κ` 作為乘數。
3. `H`、`EA`、`EAX` 作為損失的分母或單調降低項。
4. 固定的 AI adoption bonus。
5. 缺值補 0、補平均、補 synthetic 值。
6. G01–G16 的 O/E、q、observed count 進入任何參數。
7. 外部研究效果量作為本企業 `OBSERVED` 值（只可作 `PUBLIC_OBSERVED` 的 sensitivity bound）。
8. 共享成本 `F_c` 在任何部門帳本中重複扣除。

---

## 2. 集合與索引

| 集合 | 元素 | 說明 |
|---|---|---|
| `U` | `u` | business units / functions |
| `J` | `j` | AI initiatives；`u(j)` 為擁有者；`J_u = {j : u(j)=u}` |
| `C` | `c` | 共享能力（model service、data layer、integration interface、access control/audit、evaluation infrastructure、change/training program 等） |
| `K_j = {0} ∪ M_j` | `k` | initiative `j` 的候選配置；`k=0` 為 status quo（不新增 AI 部署）；`M_j` 為有限列舉的 AI 配置 |
| `Γ` | `γ` | 企業 policy profiles 的有限選單；`γ^0` = legal-minimum profile；`γ^cur` = 現行 policy |
| `R ∪ {NA}` | `r` | `R = {Use, Verify, Modify, Escalate, Reject, Bypass}`；`NA` 為 HumanOnly／status quo 下「無 AI 輸出」 |
| `Λ_j` | `ℓ` | 與 initiative `j` 相關的角色群 |
| `Z_j` | `z` | 行動當下可見的訊號（例：AI 信心旗標、與自身判斷是否分歧、例外旗標） |
| `Ω_j` | `ω` | 行動當下不可見的真實結果類別（例：AI 輸出正確／錯誤 × 嚴重度） |
| `H^pool` | `h` | 企業池化資源類別；最小形式 `{BUD, ENG}` |
| `H^own_u` | `h` | 部門自有資源類別；最小形式 `{REV}`（人工審查工時） |
| `𝒢` | `g` | 預先登記的 scenario groups；`Θ_g` 為其可接受參數集合；`Θ_adm = ∪_g Θ_g` |

每個 `k ∈ M_j` 是屬性組：

$$
k \equiv (A_k, H_k, WI_k, EA_k, EAX_k, m_k[, \tau_k])
$$

其中 `m_k ∈ {HumanOnly, AI→Human, Human→AI, Aggregation, Delegated, BoundedExecution}`；`τ_k` 只在 G10 optional module 啟用時出現（離散門檻變體）。`k=0` 的屬性為現況配置（通常 `m=HumanOnly`，但若現況已有 AI 部署，則照實記錄）。

---

## 3. 參數

### 3.1 企業層

| 參數 | 意義 | 單位 |
|---|---|---|
| `Ā^h`, `h∈H^pool` | 池化資源總量（`Ā^BUD = B̄` 預算；`Ā^ENG` 工程工時） | TWD/period；hours/period |
| `F_c` | 共享能力 `c` 啟用時的期間成本（資源限制用絕對值；目標函數以相對現況 `y^cur` 的增量計，見 §7.4） | TWD/period |
| `y^cur_c` | 現況已啟用的共享能力 | binary（OBSERVED） |
| `a^h_c` | 能力 `c` 消耗的池化資源（`a^BUD_c = F_c`） | 同 `h` |
| `F^loc_{uc}`, `a^{h,loc}_{uc}` | 部門 `u` 自建本地版本 `c` 的成本與資源（僅 Model A/A+ 與允許本地自建的 policy） | TWD/period；hours/period |
| `ΔC^gov(γ)` | policy `γ` 相對於現行治理的營運成本差 | TWD/period |
| `Allow_γ(j,k)` | policy 是否允許 `j` 採用 `k` | binary |
| `Allow^loc_γ(u,c)` | policy 是否允許 `u` 自建本地 `c` | binary |
| `G_j(γ)` | policy 下 `j` 的正式決策權等級（**permission level**：數值越高越寬鬆，屬賦能而非要求） | ordinal 0–3 |
| `H^req_γ(A,κ)`, `WI^req_γ(A,κ)`, `EA^req_γ(A,κ)`, `G^req(A,κ)` | 同構念最低要求表 | ordinal 0–3 |
| `ē_j^γ` | `j` 的嚴重事件容忍上限 | incidents/period |
| `J^must_γ`, `J^forbid_γ` | 策略強制與禁止 initiative 集合（S 的表達方式） | set |
| `Legal_{jk}` | 法規、隱私、權利、安全硬限制 | binary |
| `B^0_u`, `K^{ENG,0}_u` | 現況部門預算與工程容量（Model A 用） | TWD/period；hours/period |

### 3.2 Initiative 層

| 參數 | 意義 | 單位 |
|---|---|---|
| `κ_j` | 後果類別 | ordinal class |
| `N_{jk}` | 配置 `k` 下的事件量；預設 `N_{jk}=N_j`，僅在有 throughput 證據時隨 `k` 變 | events/period |
| `Pre(j,k) ⊆ C` | `k` 所需的能力前提（例：評估等級達 `EA^cap` 以上時 `y_EVAL ∈ Pre(j,k)`，G05） | set |
| `R_j(y)`, `D(y)` | 能力狀態決定的資料可得性與介面等級 | ordinal 0–3 |
| `R^req(A)`, `D^req(A)` | 同構念要求 | ordinal 0–3 |
| `Eff_H(j,k)` | 名義介入權是否具有效控制（行動前可見資訊、足夠時間、真實否決） | binary |
| `FB_{jk}` | fallback／rollback 路徑存在 | binary |
| `Cons(A,m)` | 權限與配置型態一致（例：`A=3` 與 `m=AI→Human` 矛盾） | binary（定義性） |
| `O_{jk}`, `Rec_{jk}(s)` | 一次性導入成本、每期持續成本（整合、在地訓練、監控、維護、rollback 準備）；`s` 為能力來源狀態（§10） | TWD；TWD/period |
| `a^{ENG}_{jk}(s)` | 工程工時 | hours/period |
| `C^{impl,x}_{jk}` | 導入成本中不入部門帳本的部分（中央出資） | TWD/period |
| `τ_{jc}` | 內部 chargeback（若存在） | TWD/period |

### 3.3 反應與結果查表

| 參數 | 意義 | 單位 |
|---|---|---|
| `π_j(ℓ|k)` | 角色暴露權重，`Σ_ℓ π = 1` | probability |
| `P_j(z,ω|k)` | 可見訊號與隱藏結果的聯合分布，`Σ_{z,ω} P = 1` | probability |
| `ρ_j(r|k,z,ℓ,y)` | 角色在可見訊號下的反應分布，`Σ_r ρ = 1`；`ρ(r)=0` 若 `r ∉ R_k^γ` | probability |
| `v_j(k,ℓ,z,ω,r)` | 可貨幣化價值（營收、機會價值），拆為 `v^u + v^x` | TWD/event |
| `l_j(k,ℓ,z,ω,r)` | 損失（錯誤決策、營運失敗、重工、延誤、客戶影響），拆為 `l^u + l^x` | TWD/event |
| `c_j(k,ℓ,z,r)` | 非人工營運成本（推論、外部服務、例外處理之非人工部分），拆為 `c^u + c^x` | TWD/event |
| `t_j(k,ℓ,z,ω,r)` | 角色工時（含查核、修改、升級、重工中的人工） | hours/event |
| `t^{REV}_j(k,ℓ,z,ω,r)` | 其中屬審查容量的工時 | hours/event |
| `λ_ℓ`, `λ^u_ℓ` | 角色時間的可實現機會價值（企業／部門帳本） | TWD/hour |
| `I^{sev}_j(k,ℓ,z,ω,r)` | 該路徑產生嚴重事件的機率 | probability |
| `s_j(·)`, `s^min_j` | 部門服務／品質指標與其下限（若有） | 指標單位 |

### 3.4 攤提

$$
AF(r_d, H) = \frac{r_d}{1-(1+r_d)^{-H}}, \qquad C^{impl}_{jk}(s) = O_{jk}\,AF(r_d,H_j) + Rec_{jk}(s)
$$

`r_d`（期間折現率）與 `H_j`（攤提期數）為有 provenance 的參數；`F_c` 同理。若 `r_d` 未識別，以 `[r_L, r_U]` 進 `Θ_adm`。

---

## 4. 決策變數

### 4.1 企業層（Leader）

$$
b = (y, \gamma, e), \qquad y \in \{0,1\}^{|C|},\ \gamma \in \Gamma,\ e = (e_u^h)_{u\in U, h\in H^{pool}}
$$

`e_u^h` 為分配給部門 `u` 的池化資源 envelope（預算與工程工時）。

### 4.2 部門層（Follower）

對 `u`：

$$
x_u = \big(q_u, y^{loc}_u\big), \qquad q_{jk}\in\{0,1\}\ \forall j\in J_u, k\in K_j, \qquad y^{loc}_{uc}\in\{0,1\}
$$

`y^loc_{uc}` 只在 `Allow^loc_γ(u,c)=1` 時可為 1。

### 4.3 使用者層

預設**不是決策變數**；以 `ρ` 內嵌（§9）。

---

## 5. 可行性

令能力可用狀態 `ȳ_{jc} = max(y_c, y^loc_{u(j)c})`。對每個 `(j,k)`，定義可行旗標

$$
\Phi_{jk}(y,y^{loc},\gamma;\theta) = \prod_{i=2}^{9} \Phi^{(Fi)}_{jk}
$$

| 編號 | 限制 | 形式 | 來源機制 |
|---|---|---|---|
| (F1) | one-hot | $\sum_{k\in K_j} q_{jk} = 1\ \ \forall j$ | — |
| (F2) | 法規／權利硬限制 | $\Phi^{(F2)}_{jk} = Legal_{jk}$ | F1 |
| (F3) | policy 允許 | $\Phi^{(F3)}_{jk} = Allow_\gamma(j,k)\cdot \mathbb 1[j\notin J^{forbid}_\gamma \lor k=0]$ | M1 (G09) |
| (F4) | 能力前提 | $\Phi^{(F4)}_{jk} = \prod_{c\in Pre(j,k)} \bar y_{jc}$ | F5；M4 (G05) |
| (F5a) | 人工介入 | $\mathbb 1[H_k \ge H^{req}_\gamma(A_k,\kappa_j)]$ | M1 (G02, G08, G16) |
| (F5b) | 流程整合 | $\mathbb 1[WI_k \ge WI^{req}_\gamma(A_k,\kappa_j)]$ | M2 (G03, G14) |
| (F5c) | 正式決策權 | $\mathbb 1[G_j(\gamma) \ge G^{req}(A_k,\kappa_j)]$ | M1 (G09) |
| (F5d) | 評估保證 | $\mathbb 1[EA_k \ge EA^{req}_\gamma(A_k,\kappa_j)]$ | M4 (G06) |
| (F5e) | 資料／介面 | $\mathbb 1[R_j(\bar y) \ge R^{req}(A_k)]\cdot\mathbb 1[D(\bar y) \ge D^{req}(A_k)]$ | F5 |
| (F6) | 有效控制 | $\Phi^{(F6)}_{jk} = 1$ 若 $H^{req}_\gamma(A_k,\kappa_j) < 2$，否則 $Eff_H(j,k)$ | M1 (Elish; Aghion & Tirole) |
| (F7) | fallback／rollback | $\Phi^{(F7)}_{jk} = 1$ 若 $A_k \le 1$，否則 $FB_{jk}$ | M2 (G03, G16) |
| (F8) | 權限—配置一致 | $\Phi^{(F8)}_{jk} = Cons(A_k,m_k)$ | M3 (G01) |
| (F9) | 嚴重事件硬上限 | $\Phi^{(F9)}_{jk} = \mathbb 1\big[N_{jk}\,\mathbb E_{jk}[I^{sev}] \le \bar e_j^\gamma\big]$ | M1；不可貨幣化風險 |
| (F10) | 策略強制 | $\sum_{k\ne 0} q_{jk} = 1\ \ \forall j \in J^{must}_\gamma$ | S（以 policy 表達） |

連結：

$$
q_{jk} \le \Phi_{jk}(y,y^{loc},\gamma;\theta)\quad \forall j,k
$$

**實作規則：** (F5a–e) 是查表後的布林旗標；ordinal 值只在 `≥` 中出現。**(F2)–(F9) 對所有 `k`（含 `k=0`）一律適用**：新 policy 可能使現況配置不可行，此時該 initiative 必須改選其他可行配置。為此每個 `K_j` 應包含至少一個不依賴新能力的 fallback 配置。若在某 `(y,γ)` 下某 `j` 沒有任何可行配置，該 `(y,γ)` 不可行並列入報告；若 `k=0` 違反 (F2) 或 (F9)，另輸出 `STATUS_QUO_NONCOMPLIANT`（作為結果，不是中止求解）。

### 5.1 資源限制

每個 `(j,k)` 的資源使用：

$$
a^{BUD}_{jk}(s) = C^{impl}_{jk}(s) + \big(N_{jk}\,\mathbb E_{jk}[c] - N_{j0}\,\mathbb E_{j0}[c]\big),\qquad a^{ENG}_{jk}(s),\qquad a^{REV}_{jk} = N_{jk}\,\mathbb E_{jk}[t^{REV}] - N_{j0}\,\mathbb E_{j0}[t^{REV}]
$$

預算使用包含**增量每事件營運支出**（推論、外部服務），可為負（AI 降低支出時釋出預算）。人工時間不是現金支出，只進容量 (R2) 與目標中的 `λt`。

**(R1) 池化資源（centralized 形式）：**

$$
\sum_c a^h_c y_c + \sum_u\sum_c a^{h,loc}_{uc} y^{loc}_{uc} + \sum_j\sum_k q_{jk}\,a^h_{jk} + \mathbb 1[h=BUD]\,\Delta C^{gov}(\gamma) \le \bar A^h\quad \forall h\in H^{pool}
$$

**(R1′) 池化資源（bilevel 形式）：** 企業層

$$
\sum_c a^h_c y_c + \sum_u e^h_u + \mathbb 1[h=BUD]\,\Delta C^{gov}(\gamma) \le \bar A^h
$$

部門層

$$
\sum_c a^{h,loc}_{uc} y^{loc}_{uc} + \sum_{j\in J_u}\sum_k q_{jk}\,a^h_{jk} \le e^h_u
$$

**(R2) 部門自有資源：**

$$
\sum_{j\in J_u}\sum_k q_{jk}\,a^{REV}_{jk} \le \Delta\bar K^{REV}_u
$$

`ΔK̄^REV_u` 為部門可另外投入審查的工時（相對於現況）。`a^REV` 可為負（AI 降低審查量）。容量限制以期望值表示；穩健版在 §13 以 `Θ_g` 上界檢查。

---

## 6. 期望算子

對任何路徑函數 `f`：

$$
\mathbb E_{jk}[f\mid \bar y] = \sum_{\ell\in\Lambda_j}\pi_j(\ell\mid k)\sum_{z\in Z_j}\sum_{\omega\in\Omega_j}P_j(z,\omega\mid k)\sum_{r\in R_k}\rho_j(r\mid k,z,\ell,\bar y)\,f_j(k,\ell,z,\omega,r) \tag{X1}
$$

- `ω` 不在 `ρ` 的條件集合中（使用者在行動當下看不到真實結果）。
- `ρ` 對 `ȳ` 的依賴只在有證據時存在（例如訓練／變革能力 `y_CHG` 改變查核行為）；否則 `ρ` 不隨 `ȳ` 變。
- `EAX_k` 只透過 `ρ(·|k,…)` 影響結果；不另有方程項（G13、G15）。
- (X1) 對 `π`、`P`、每一列 `ρ`、以及 `f` 各自為線性；整體為 **block-multilinear**。§13 的穩健性精確檢查依賴此性質。

---

## 7. 帳本與企業目標

### 7.1 路徑淨貢獻（TWD/event）

$$
f_j(k,\ell,z,\omega,r) = v_j - l_j - c_j - \lambda_\ell\,t_j \tag{V1}
$$

### 7.2 Benefit／Cost／Loss 帳本（防重複計算）

每一經濟後果**只能**落在一個項目：

| 後果 | 唯一歸屬 | 不得同時出現在 |
|---|---|---|
| 人工時間節省或增加 | `−λ_ℓ t`（V1）＋容量 (R2) | `v`（不得再以「人力節省」計入價值） |
| Throughput（多處理的事件） | `N_{jk}` 變動 × 每事件淨貢獻 | 若釋出的時間已以 `λ` 計價，則 throughput 不得再計同一批時間 |
| 決策品質／錯誤減少 | `l`（損失下降） | `v` |
| 營收／機會價值 | `v` | `l` |
| 推論、外部服務 | `c` | `C^impl` |
| 整合、在地訓練、監控、維護、rollback 準備 | `C^impl`（期間化） | `c` |
| 共享平台、共享模型服務固定成本、資料層、資安、評估平台、共用訓練計畫 | `F_c`（只在企業層一次） | 任何 `C^impl` 或部門帳本 |
| 治理營運（委員會、稽核、文件） | `ΔC^gov(γ)` | `F_c`（除非治理平台本身被定義為能力 `c`） |
| 重工、延誤、客戶影響 | `l` | `c` |
| 合規、隱私、權利、資安底線 | (F2)(F9) 硬限制 | 不換算為 TWD |
| 能力重用、跨部門重用 | `C^impl_{jk}(s)` 隨能力來源狀態的差異（§10） | `v`（不得另列「重用效益」） |
| Option value | **不進靜態目標**；M5 或 real-option sensitivity | `v` |
| Chargeback `τ` | 只在部門帳本 | 企業目標（內部移轉，企業層相互抵銷） |

### 7.3 每事件期望淨貢獻與 initiative 貢獻

$$
g_{jk}(\bar y) = \mathbb E_{jk}[f\mid\bar y],\qquad
\varphi_{jk}(\bar y, s) = N_{jk}\,g_{jk}(\bar y) - N_{j0}\,g_{j0}(\bar y^{cur}) - C^{impl}_{jk}(s),\qquad C^{impl}_{j0}\equiv 0 \tag{V2}
$$

`φ_{jk}` 是**相對於「現況配置 `k=0` 在現況能力狀態 `ȳ^cur` 下」的增量**貢獻（TWD/period）。因此 `φ_{j0}(ȳ) = N_{j0}[g_{j0}(ȳ) − g_{j0}(ȳ^cur)]`，只在現況配置的反應或結果確實隨能力狀態改變時（例如變革能力 `y_CHG` 改變現有 AI 的查核行為）不為 0。識別只需要差額；若直接以增量引出，provenance 須標註。

### 7.4 企業目標（OBJ-E）

$$
F_E(y,y^{loc},\gamma,q;\theta) = \sum_{j}\sum_{k} q_{jk}\,\varphi_{jk}(\bar y, s) - \sum_c F_c\,(y_c - y^{cur}_c) - \sum_u\sum_c F^{loc}_{uc}\,y^{loc}_{uc} - \Delta C^{gov}(\gamma) \tag{OBJ-E}
$$

單位 TWD/period，意義為「相對於現況 portfolio 的企業增量價值」：保留既有能力的增量成本為 0，停用既有能力節省 `F_c`，新建能力花費 `F_c`。資源限制 (R1) 仍以絕對值 `Σ_c a^h_c y_c` 計，因為 `B̄` 是包含既有能力營運的總預算。

**若 `λ_ℓ` 未識別：** 不以 0 代入。求解改報兩分量 `(F_E^{−time}, ΔHours)`，其中 `F_E^{−time}` 去除 `λt` 項，`ΔHours = Σ_{j,k} q_{jk}(N_{jk}E_{jk}[t] − N_{j0}E_{j0}[t])`（hours/period），並以 `λ_ℓ ∈ [0, λ^U_ℓ]`（`λ^U` 可由公開薪資資料界定）做 §13 分類；若決策隨 `λ` 改變，該決策標為 `CONDITIONAL` 或 `FRAGILE`，不得宣稱 ROBUST。

---

## 8. 部門目標與對齊

### 8.1 部門帳本（OBJ-U）

部門的目標**由其被考核的帳本界定**（預算、P&L、KPI 文件可觀察），不由研究者設定偏好權重：

$$
f^u_j = v^u_j - l^u_j - c^u_j - \lambda^u_\ell t_j,\qquad g^u_{jk} = \mathbb E_{jk}[f^u]
$$

$$
\varphi^u_{jk} = N_{jk}g^u_{jk} - N_{j0}g^u_{j0} - \big(C^{impl}_{jk} - C^{impl,x}_{jk}\big) - \sum_{c\in Pre(j,k)} \tau_{jc}\,y_c\,(1-y^{loc}_{u(j)c})
$$

$$
F_u(x_u\mid y,\gamma) = \sum_{j\in J_u}\sum_k q_{jk}\,\varphi^u_{jk}(\bar y) - \sum_c F^{loc}_{uc}\,y^{loc}_{uc} \tag{OBJ-U}
$$

部門另有自身限制（僅在有文件或行為證據時加入）：

- 服務／品質下限：`E_{jk}[s_j] ≥ s^min_j`
- 部門問責上限：`N_{jk}E_{jk}[I^{sev}] ≤ ē^u_j`（可比企業 `ē_j^γ` 更嚴）

部門可行集合：

$$
X_u(y,\gamma,e_u;\theta) = \{x_u : \text{(F1)–(F10) for } j\in J_u,\ \text{(R1′) unit part},\ \text{(R2)},\ \text{unit-only constraints},\ y^{loc}_{uc}\le Allow^{loc}_\gamma(u,c)\}
$$

### 8.2 對齊條件（Alignment, AL）

部門與企業**完全對齊**，若同時成立：

- (AL1) 無外部帳本項：`v^x = l^x = c^x = 0`，`C^{impl,x}=0`；
- (AL2) 無 chargeback：`τ = 0`（或其等值於企業真實邊際成本且已在 `c` 中，不另計）；
- (AL3) 無部門專屬限制，或其也在企業問題中；
- (AL4) `λ^u_ℓ = λ_ℓ`。

在 (AL) 下，`φ^u_{jk} = φ_{jk}`，部門最佳化即企業對該部門 initiative 的最佳化（§15 P2）。

### 8.3 為什麼不用 39 版的部門目標

39 版 `F_M = −N[E(L_oper)+E(C_op)] − C_impl` 讓部門完全不計價值；這等同假設 `v^u = 0`。在 v2.1 中它是 (OBJ-U) 的**特例**，只在帳本證據顯示部門不被以價值考核時才成立。以它作預設會在模型中製造部門必然偏向 status quo 的假衝突（§17 D2）。

---

## 9. 使用者反應層

### 9.1 三種 `ρ`

| 版本 | 意義 | 識別來源 |
|---|---|---|
| `ρ^obs` | 已部署配置下的實際反應 | 系統紀錄、抽樣觀察（OBSERVED） |
| `ρ^cf` | 尚未部署配置下的反應 | 盲真值題卡（vignette）引出區間（EXPERT_ELICITED）或 scenario |
| `ρ^design` | 配置程序文件所設計的反應（退化分布） | 作業程序文件（OBSERVED） |

預設 `ρ^design`：`HumanOnly→NA`；`AI→Human→Verify`；`Human→AI→Use`；`Aggregation→Use`；`Delegated→Use`（若 `z` 為例外旗標則 `Escalate`）；`BoundedExecution→Use`（越界訊號則 `Escalate`）。實際設計以企業文件為準。

### 9.2 第三層 optimizer 的觸發測試（T1–T5）

只有五項**全部**成立，才建立 Model D：

| 測試 | 條件 | 證據 |
|---|---|---|
| T1 | 使用者可在無事前核准下選擇 `r` | 權限文件、觀察 |
| T2 | 至少兩個具後果的可行反應 | `ρ^obs` 有兩個以上非零且後果不同 |
| T3 | 使用者有不同於部門的目標或限制 | 工作量、問責、績效制度證據 |
| T4 | 部門在選配置時預期使用者反應 | 決策紀錄、訪談 |
| T5 | 以結構化反應取代 `ρ` 會改變上游最適配置 | 計算：`d*(ρ) ≠ d*(ρ^{BR})` 於 `Θ_adm` 中的某合理區域 |

Model D（若觸發）：

$$
\rho^{BR}_j(r\mid k,z,\ell) = \text{uniform over } \arg\max_{r\in R_k} U_\ell(r\mid k,z)
$$

`U_ℓ` 為角色效用查表（需獨立識別）；ties 以 optimistic／pessimistic 界報告。**未觸發時不執行 Model D。**

---

## 10. 共享能力耦合

五種耦合，全部已進入上式：

1. **共享固定成本**：`F_c y_c` 只在 (OBJ-E) 與 (R1) 出現一次。
2. **前提**：(F4) `q_{jk} ≤ ȳ_{jc}`, `c ∈ Pre(j,k)`。
3. **容量耦合**：(R1)/(R1′) 中多個 initiative 共用 `Ā^ENG`。
4. **Policy 耦合**：同一 `γ` 對所有部門設定 `Allow`、要求表、`ē`。
5. **重用效果**：`C^{impl}_{jk}(s)`、`a^{ENG}_{jk}(s)` 為**以能力來源為索引的查表**。對 `c ∈ Rel(j)` 定義來源狀態

$$
s_{jc} = \begin{cases} \text{L} & y^{loc}_{u(j)c}=1 \\ \text{S} & y_c = 1,\ y^{loc}_{u(j)c}=0 \\ \varnothing & \text{otherwise}\end{cases},\qquad C^{impl}_{jk}(s) = C^{impl}_{jk}\big(s_{j,Rel(j)}\big)
$$

共享重用效果定義為 `δ_{jkc} = C^{impl}_{jk}(s_c=∅) − C^{impl}_{jk}(s_c=S)`；本地版的效果另以 `s_c=L` 的格表示。以來源而非可用與否為索引的理由：本地版與共享版的成本、品質與重用性可能不同；若以 `ȳ` 為索引，`δ` 也會作用在本地版，使 `y_c=0` 分支的最適值隨 `δ` 改變而破壞 P4 的單調性（Phase F 稽核發現）。**沒有證據時不假設 `δ>0`**：`δ` 以 `[0, δ^U]` 進 `Θ_adm`；若 `δ^U` 也未識別，改報 break-even `δ^†`（§14 Q2）。不假設「共用一定更便宜」，也不假設本地版與共享版的品質相同——若 `P` 或 `ρ` 隨能力版本不同，需分別查表。

Sequencing（啟動順序）屬 M5，不進靜態版。

---

## 11. 組織型態與比較量

所有比較在**同一 `θ`、同一 policy regime** 下進行。Policy regime 有兩種報法：(i) 固定 `γ`（條件比較）；(ii) 各型態自選 `γ`。

| Model | 誰決定什麼 | 目標 | 能力 | 預算 |
|---|---|---|---|---|
| **A Independent local** | 各部門決定 `(q_u, y^loc_u)` | (OBJ-U) | 只可本地自建 | 固定 `B^0_u`, `K^{ENG,0}_u` |
| **C0 Bilevel, no sharing** | 企業決定 `(γ, e)`；部門決定 `(q_u,y^loc_u)` | Leader (OBJ-E)；Follower (OBJ-U) | 只可本地版（`y_c ≡ 0`） | envelope |
| **A+ Central, no sharing** | 企業決定全部 | (OBJ-E) | 只可本地版（`y_c ≡ 0`） | 池化 `Ā` |
| **B Centralized planner** | 企業決定全部 | (OBJ-E) | 共享與本地皆可 | 池化 `Ā` |
| **C Enterprise–BU bilevel** | 企業決定 `(y,γ,e)`；部門決定 `(q_u,y^loc_u)` | Leader (OBJ-E)；Follower (OBJ-U) | 共享（企業）＋本地（若 `Allow^loc`） | envelope |
| **D Tri-level**（條件） | C ＋ 使用者以 `U_ℓ` 選 `r` | 同 C；使用者 `U_ℓ` | 同 C | 同 C |

Model A 的企業價值以 (OBJ-E) 評估其解；A 的 ties 以 enterprise optimistic／pessimistic 界報告。比較需要 `Σ_u B^0_u + ΔC^{gov}(γ) ≤ B̄`、`Σ_u K^{ENG,0}_u ≤ Ā^ENG`，且 A 所用的 `γ` 在其他型態中可選；若不成立，A 與其他型態的資源基礎不同，比較標為 `NOT_COMPARABLE`。

### 11.1 比較量（凍結名稱與語義）

| 名稱 | 定義 | 符號性質 | 語義 |
|---|---|---|---|
| **VRA** Value of Reallocation | $F_E^{C0} - F_E^{A}$ | ≥ 0（P1） | 不共享能力、部門仍自主時，企業重新分配 envelope 的價值 |
| **DL0** Delegation Loss without sharing | $F_E^{A+} - F_E^{C0}$ | ≥ 0（P1） | 不共享能力時，部門帳本不對齊造成的損失 |
| **VCP** Value of Central Planning | $F_E^{A+} - F_E^{A} = VRA + DL0$ | ≥ 0（P1） | 不共享能力時，集中規劃的總價值＝資源重分配＋帳本對齊兩部分（**不是**純重分配價值） |
| **VSC** Value of Shared Capability | $F_E^{B} - F_E^{A+}$ | ≥ 0（P1） | 在集中規劃下，允許共享能力的價值 |
| **DL** Delegation Loss | $F_E^{B} - F_E^{C}$（optimistic／pessimistic 兩界） | ≥ 0（P1） | 把配置選擇交給部門所造成的企業價值損失；**只由帳本不對齊產生**（P2） |
| **NEV** Net Enterprise-architecture Value | $F_E^{C} - F_E^{A} = VCP + VSC - DL$ | **可正可負** | 「企業協調架構＋部門自主」相對於「各部門自行做 AI」的淨價值 |
| **VG(γ)** Value of Governance | $F_E^{*}(\gamma) - F_E^{*}(\gamma^0)$ | 可正可負 | policy 相對於 legal-minimum 的價值；分解見 §14 Q3 |

bundle 草稿中的 `VoC = F^Centralized − F^Bilevel` 即本檔的 **DL**。改名理由：在完全資訊模型中，此差額必然 ≥ 0，它衡量的是「授權損失」而非「協調創造的價值」；協調創造的價值由 VCP 與 VSC 衡量。`ReuseValue` 改為 **VSC**，因為共享能力的價值包含重用以外的前提賦能效果。

**DL 的重要限制：** 模型假設企業層知道部門參數（完全資訊），因此 B 永遠弱優於 C。分權在真實組織中的資訊優勢（Alonso, Dessein, & Matouschek, 2008）**不在本模型內**。§15 P3 與附錄 sensitivity 說明。

---

## 12. 求解程序

### 12.1 為什麼用有限列舉，而不是 KKT／MPEC

下層（部門）問題是**整數**選擇（one-hot 配置、二元本地能力）。KKT 條件只對凸、連續的下層問題是最適性的必要充分條件；對整數下層問題，KKT 單層重構**不成立**。若規模需要，可用 value-function 或 branch-and-bound 類的 mixed-integer bilevel 方法（Moore & Bard, 1990；Kleinert et al., 2021）。在已識別的規模下，有限列舉是**精確**的，並可直接作為 synthetic oracle。

### 12.2 前處理

1. Schema 與單位檢查（45 T-SCH）；失敗輸出 `INVALID_SCHEMA_OR_UNITS`。
2. 對每個 `j`、每個 `k`、每個能力來源模式，檢查所需查表格是否有值或區間（§13.4 缺值規則）。
3. 對每個 `(γ, ȳ_{Rel(j)}, s_{j,Rel(j)})` 預先計算 `Φ_{jk}`、`g_{jk}`、`φ_{jk}`、`φ^u_{jk}`、`a_{jk}`。

### 12.3 部門回應（Follower）

對給定 `(y, γ, e_u)`：

1. 列舉部門計畫 `x_u = (q_u, y^loc_u)`：`∏_{j∈J_u}|K_j| × 2^{|C^loc_u|}` 個，篩去不可行者。
2. `X*_u(y,γ,e_u) = argmax F_u`（容差 `ε_tie`，預先登記；預設 `1e-9` 相對）。
3. Leader 對 `u` 的貢獻界：

$$
\phi^{opt}_u = \max_{x_u\in X^*_u}\Big[\sum_{j\in J_u}\sum_k q_{jk}\varphi_{jk} - \sum_c F^{loc}_{uc}y^{loc}_{uc}\Big],\quad
\phi^{pess}_u = \min_{x_u\in X^*_u}[\cdots]
$$

### 12.4 Envelope 的精確有限化（Lemma E）

對部門 `u`，令 `𝒫_u` 為其可行計畫集合、`a(x_u) ∈ ℝ^{|H^pool|}` 為計畫的池化資源使用。對任何 envelope `e_u`，以

$$
e'_u = \bigvee\{a(x_u): x_u\in\mathcal P_u,\ a(x_u)\le e_u\}\quad(\text{componentwise max})
$$

取代 `e_u`，部門可行集合不變、回應集合不變、且 `e'_u ≤ e_u`。因此 leader 只需考慮有限集合

$$
E_u = \Big\{\bigvee S : S\subseteq \{a(x_u)\}\Big\}
$$

當 `H^pool = {BUD, ENG}`（二維）時，`E_u ⊆ {(a^{BUD}(x), a^{ENG}(x')) : x,x' ∈ 𝒫_u}`，此乘積集合大小至多 `|𝒫_u|²`；列舉整個乘積集合仍是精確的，因為其中任何 envelope 的回應都等於其約化後的 join 的回應。一維時即為計畫成本集合。

### 12.5 Leader（Model C）

對每個 `(y, γ)`：

1. 對每個 `u`、每個 `e_u ∈ E_u` 計算 `φ^{opt}_u(e_u)`、`φ^{pess}_u(e_u)`。
2. 解多選擇背包（multiple-choice knapsack）：

$$
\max_{(e_u)_u}\ \sum_u \phi^{\{opt,pess\}}_u(e_u)\quad\text{s.t.}\quad \sum_u e^h_u \le \bar A^h - \sum_c a^h_c y_c - \mathbb 1[h=BUD]\Delta C^{gov}(\gamma)
$$

小規模用完整列舉；中規模以預算量子 `β` 做 DP（若所有成本為 `β` 的整數倍則精確，否則誤差上界 `|U|·β·(邊際價值上界)`，須報告）。

3. $F_E^{C,\{opt,pess\}}(y,\gamma) = \text{(2) 的最適值} - \sum_c F_c y_c - \Delta C^{gov}(\gamma)$。
4. 對 `(y,γ)` 取最大。Optimistic 與 pessimistic 分別取最大（pessimistic bilevel 的 leader 解是「對最不利 follower 反應最好的 leader 決策」；有限情形下必可達，見 Wiesemann et al., 2013 的一般性討論）。

### 12.6 Centralized（Model B）與 A+

直接列舉 `(y, γ)`，對每個部門以 (OBJ-E) 的部門貢獻取代 (OBJ-U) 求部門最佳，配合 12.5 的背包。A+ 同 B 但 `y ≡ 0`。C0 同 12.5（Model C）但 `y ≡ 0`。

### 12.7 Model A

各部門以固定 `(B^0_u, K^{ENG,0}_u)` 為 envelope、`γ = γ^cur`（或指定）、`y ≡ 0`，解 (OBJ-U)；以 (OBJ-E) 評估其解，報 ties 界。

### 12.8 複雜度

`|Γ| · 2^{|C|} · Σ_u |𝒫_u|·|E_u|` 次部門評估加背包。參考規模（`|C|≤8`, `|Γ|≤4`, `|U|≤8`, 每部門 ≤4 initiatives × ≤6 configs）可精確求解；超過時記錄所用近似與誤差界。

---

## 13. 不確定性、穩健性與缺值

### 13.1 Θ_adm

`Θ_adm = ∪_{g∈𝒢} Θ_g`。每個 `Θ_g` 為：

- 貨幣與數量參數的區間積（`[L,U]`）；
- 每一機率列（`π(·|k)`、`P(·,·|k)`、`ρ(·|k,z,ℓ)`）為「單純形 ∩ 區間盒」的多面體；
- 預先登記的相依限制（例：`v` 與 `N` 同向）。

`𝒢` 在看到求解結果前登記（例：`g1` 現況延續、`g2` 高採用、`g3` 高錯誤後果）。

### 13.2 分類（決策元素層級）

令 `d` 為一個決策元素（某 `y_c`、某 `q_j`、某 `e_u`、`γ`、或整個 portfolio），`d*(θ)` 為 `θ` 下最適集合中該元素的值（ties 以完整集合處理）。

| 類別 | 定義 |
|---|---|
| **UNIDENTIFIED** | 至少一個影響 `d` 的必要參數沒有可接受界（不屬任何 `Θ_g`），或該參數的缺值使某個可能最適的候選配置被排除 |
| **ROBUST** | 存在單一值 `d°` 使 `d° ∈ d*(θ)` 對所有 `θ ∈ Θ_adm` 成立（最適集合以 §13.3 的 robust-feasible 候選集合計算） |
| **CONDITIONAL** | 非 ROBUST；但對每個 `g`，存在 `d°_g` 使 `d°_g ∈ d*(θ)` 對所有 `θ ∈ Θ_g` 成立 |
| **FRAGILE** | 存在某個 `g`，`Θ_g` 內沒有單一值對整組最適 |

同時報告**最大 regret**：`MaxRegret(d) = max_θ [F^*(θ) − F(d,θ)]`，以及預先登記容差 `ε_R`（TWD/period）下的 ε-ROBUST。

### 13.3 精確檢查（Lemma R）與其適用範圍

**Lemma R（整個 portfolio、Model B）。** 對兩個固定的 portfolio `d, d'`，`Δ(θ) = F_E(d;θ) − F_E(d';θ)` 在 (X1) 的各參數區塊上 block-multilinear（且對貨幣參數線性）。若 `Θ_g` 是各區塊多面體的乘積，則 `min_{θ∈Θ_g} Δ(θ)` 在乘積的某個頂點達成。因此在 Model B 中，「整個 portfolio `d` 在 `Θ_g` 內恆為最適」可由對每個競爭者 `d'` 做頂點檢查精確判定。貨幣區塊的最小值可直接以「係數符號選端點」求得（區間算術）。

**適用範圍的限制（Phase F 稽核修正）：**

1. **決策元素層級不精確。** 「元素值 `d°` 恆屬最適」等價於 `min_θ [max_{d∋d°} F(d,θ) − max_d F(d,θ)] ≥ 0`；含 `d°` 的最佳 portfolio 會隨 `θ` 改變，最大值的最小值不保證在頂點達成。反例：單一機率參數 `θ∈[0,1]`，兩個含 `y_c=1` 的 portfolio 價值為 `θ` 與 `1−θ`，`y_c=0` 的 portfolio 價值為 0.6；兩個頂點上 `y_c=1` 皆最適，但 `θ=0.5` 時不是。因此元素層級分類採：(a) **充分條件**——若存在單一含 `d°` 的 portfolio 依 Lemma R 在 `Θ_g` 內恆最適，則 `d°` 在 `Θ_g` 內恆最適；(b) 否則以密集列舉或抽樣判定，並報告涵蓋率。
2. **Model C 不適用。** Leader 的價值經由部門最佳回應決定，而最佳回應隨 `θ` 改變，價值函數不是 multilinear；C 的分類一律以列舉或抽樣判定並報告涵蓋率。
3. 存在相依限制或頂點過多時，改用抽樣並報告涵蓋率；不得宣稱「對所有 θ」。

可行性 (F9) 與容量 (R2) 依賴 `θ`，會使競爭者集合隨 `θ` 改變而破壞 Lemma R 的前提。Canonical 處理：在每個 `Θ_g` 中，**只把 robust-feasible 的配置與計畫**（`Φ^{(F9)}=1` 且 (R2) 對整個 `Θ_g` 成立；以各區塊頂點檢查，因兩者對機率區塊為 multilinear）納入分類用的候選集合；只在部分 `θ` 可行的配置另列為 `CONDITIONALLY_FEASIBLE`，不參與 ROBUST 判定。如此 Lemma R 在固定候選集合上精確。

### 13.4 缺值規則

| 缺值位置 | 處理 | 輸出狀態 |
|---|---|---|
| schema／單位錯 | 拒算 | `INVALID_SCHEMA_OR_UNITS` |
| `j` 的 status quo 查表 | `j` 無法評估，自 portfolio 移除並列出 | `UNEVALUABLE_INITIATIVE` |
| 某 `k ∈ M_j` 的查表格 | `k` 移除；所有可能受影響的決策元素降為 UNIDENTIFIED | `RESTRICTED_SOLVE` |
| `F_c`（或 `a_c`） | 不強制 `y_c=0`；改報 break-even `F_c^†`（§14 Q2） | `THRESHOLD_MODE` |
| `λ_ℓ` | 報兩分量目標（§7.4） | `PARTIAL_OBJECTIVE` |
| 帳本拆分（`v^x` 等）未識別 | Model C 不求解；B、A+ 照常；DL 標 UNIDENTIFIED | `FOLLOWER_LEDGER_UNIDENTIFIED` |
| `B̄`、`Ā^ENG` | 拒算 point；可報資源—價值前緣 | `REJECT_INSUFFICIENT_IDENTIFIED_INPUTS` |
| 只有區間 | 區間求解並分類 | `OK_INTERVAL` |

### 13.5 Value-of-identification 診斷（G12 的靜態影子）

對參數區塊 `p`，以「固定 `p` 在其 `Θ_g` 範圍內的任一值後的最大 regret」與「不固定時的最大 regret」差額，排序哪些參數最值得先量測。此診斷**只作資料蒐集優先序**，不進目標。

---

## 14. 研究問題的計算量

| 研究問題 | 計算量 | 判讀 |
|---|---|---|
| **Q1** 各部門自行做 AI vs enterprise-coordinated | `NEV = VCP + VSC − DL`，其中 `VCP = VRA + DL0`；含 ties 界與穩健性分類 | NEV 在 `Θ_adm` 上恆正 → 企業協調架構 ROBUST 優於；跨組變號 → CONDITIONAL |
| **Q2** 共享能力何時值得集中投資 | 預算不綁時 `F_c^† = G_1 − G_0`，其中 `G_1`／`G_0` 為強制 `y_c=1`／`0` 且目標排除 `F_c` 的最適值；預算綁住時 `F_c^† = sup{F : G_1(F) − F ≥ G_0}`（P4）；同理 `δ^†`（break-even 共享重用，以來源為索引） | `F_c ≤ F_c^†` 於整個 `Θ_adm` → 集中投資 ROBUST |
| **Q3** governance 何時提高價值而非只增加官僚 | `VG(γ) = EE + RE + CE`：enablement `EE = F^*(Allow_γ,Req_{γ^0},C_{γ^0}) − F^*(γ^0)`；requirement `RE = F^*(Allow_γ,Req_γ,C_{γ^0}) − F^*(Allow_γ,Req_{γ^0},C_{γ^0})`；cost `CE = F^*(γ) − F^*(Allow_γ,Req_γ,C_{γ^0})`；另報反向順序 | 賦能區塊包含 `Allow_γ`、`Allow^loc_γ`、`G_j(γ)`、`J^must_γ`、`J^forbid_γ`；要求區塊包含 `H^req, WI^req, EA^req, G^req, ē`。因 `γ^0` 為 legal-minimum（要求表逐項最弱），在 B 中依 P7 得 `RE ≤ 0`；在 C 中 `RE` 可為正（P8，篩選）。policy 的模型內正價值只能來自 **賦能**、**穩健可行**或（僅 C）**篩選** |
| **Q4** 部門最適何時偏離企業最適 | `DL` 及其來源分解：逐一關閉 (AL1)–(AL4) 的不對齊來源重算 DL | DL > 0 必有某個 (AL) 不成立（P2）；分解指出是哪一個 |
| **Q5** H、WI、EA 何時是必要限制而非越多越好 | 對每個 initiative 報：`AT_REQUIREMENT`／`ABOVE_REQUIREMENT`；**Price of Requirement** `PR_X = F^*(Req_X relaxed one level) − F^*`；並檢查放寬後的解是否在 `Θ_g` 中違反 (F9) | `ABOVE_REQUIREMENT` 只在查表顯示淨效益時出現。在 B：`PR_X > 0` 且放寬後仍 robustly feasible → 模型內無保護功能的要求（候選官僚成本，非定論）；放寬後失去 robust feasibility → **robustness-protective**。在 C：`PR_X` 可為負（放寬反而降低 leader 價值）→ **screening**（要求承擔了帳本不對齊下的協調功能） |
| **Q6** 使用者反應如何改變實際價值 | 令 `d^D = d^*(ρ^{design})`、`ρ^R ∈ {ρ^{obs}, ρ^{cf}}`。**VRG**（Value Realization Gap）`= F_E(d^D;ρ^{design}) − F_E(d^D;ρ^R)`；**Design-response regret** `= F_E(d^*(ρ^R);ρ^R) − F_E(d^D;ρ^R) ≥ 0`；以及 `d^*` 是否隨 `ρ` 改變 | VRG 是「以設計反應估計的價值」與「實際反應下同一 portfolio 的價值」之差（可正可負）；regret 是以設計假設做決策的代價。因 (F9) 與 (R2) 依賴 `ρ`，`d^D` 在 `ρ^R` 下可能不可行；此時兩者皆不定義，輸出 `DESIGN_INFEASIBLE_UNDER_RESPONSE`——這本身是重要結果（設計的 portfolio 在實際反應下違反硬限制或容量） |
| **Q7** 哪些決策 ROBUST／FRAGILE | §13.2 元素層級分類＋MaxRegret | 只報預先登記的 `𝒢`；不挑選有利 scenario |
| **Q8** G01–G16 哪些真正形成企業決策問題 | **Interface activation test**：介面 I1–I4 的模型元素在 `d^*` 中是否綁住（`PR > 0`）或其變數不同於 status quo；分類 `ACTIVE-ROBUST`／`ACTIVE-CONDITIONAL`／`INACTIVE`／`UNIDENTIFIED`，再經 41 §6 追溯回 gaps | gap 是否「成為企業決策問題」是**實證結果**，不是由網絡統計推定 |

---

## 15. 命題（模型內，皆有證明草稿；由 46 的 synthetic oracle 檢查）

**P1（排序）** 在 `Σ_u B^0_u + ΔC^{gov}(γ) ≤ B̄`、`Σ_u K^{ENG,0}_u ≤ Ā^{ENG}`、且 Model A 所用 `γ` 在其他型態中可選時，對 `mode ∈ {opt, pess}`：

$$
F_E^{A,mode} \le F_E^{C0,mode} \le F_E^{A+} \le F_E^{B},\qquad F_E^{C0,mode} \le F_E^{C,mode} \le F_E^{B}
$$

*證明：* C0 的 leader 可選擇 `e_u = (B^0_u, K^{ENG,0}_u)`（由 Lemma E 等價於某候選 envelope），得到與 A 相同的回應集合；C0 的任何 (leader, follower) 組合在 A+ 中可行；A+ 的可行集合是 B 的子集合；C 的 leader 可選 `y = 0` 而得到 C0；C 的任何組合在 B 中可行。∎ 因此 VRA、DL0、VCP、VSC、DL ≥ 0，而 NEV 的符號不由模型決定。

**P2（對齊 ⇒ 零授權損失）** 若 (AL1)–(AL4) 成立且池化資源以 envelope 分配，則 `F_E^{C,opt} = F_E^{C,pess} = F_E^{B}`；同理 `F_E^{C0,opt} = F_E^{C0,pess} = F_E^{A+}`（DL0 = 0）。

*證明：* 取 B 的最適解 `(y^*,γ^*,x^*)`，設 `e_u = a(x^*_u)`。`x^*_u ∈ X_u`。若部門最適 `x'_u` 有 `F_u(x'_u) > F_u(x^*_u)`，由 (AL) 其企業貢獻也較大，且 `a(x'_u) ≤ e_u`，以 `x'_u` 取代 `x^*_u` 在 B 中可行且嚴格較佳，矛盾。故所有部門最適的企業貢獻等於 `x^*_u` 的貢獻，pessimistic 亦同。∎

*推論：* `DL > 0` 必有下列至少一項：外部帳本項（AL1）、chargeback（AL2）、部門專屬限制（AL3）、時間評價差異（AL4）。四者皆可由會計、預算、KPI 文件觀察。正值 chargeback 在 envelope 制度下**不是**對齊所需，反而可能使部門少用共享能力或自建重複能力。

*備註（由 46 的手算 oracle 呈現）：* 不對齊是 `DL > 0` 的必要條件但不是充分條件。若不對齊部門偏好的配置需要池化資源，企業可以用較小的 envelope 阻止它，`DL` 仍為 0；只有當不利企業的配置在企業必須給予的 envelope 內仍負擔得起（例如幾乎不需池化資源，或與部門的其他有利配置綁在一起）時，`DL > 0`。因此 DL 的實證判讀需同時報告 (i) 哪一個 (AL) 不成立，(ii) envelope 為何無法分離它。

**P3（完全資訊的界線）** 在本模型的完全資訊假設下 `F_E^B ≥ F_E^C` 恆成立；因此模型**不能**證明分權較佳。若需檢驗資訊優勢，使用附錄 sensitivity：企業以粗略估計 `θ̂`（例：`Θ_g` 中點或最差情形）規劃（Model B^info），部門以真實 `θ` 回應，於真實 `θ` 評估。此擴充需要「企業與部門知道不同參數」的證據，否則不執行。

**P4（門檻結構）** 對能力 `c`，令 `G_1(F_c)` 為強制 `y_c=1` 時排除 `F_c` 項的最適值（`F_c` 仍佔預算），`G_0` 為強制 `y_c=0` 的最適值。`G_1(F_c) − F_c` 對 `F_c` 嚴格遞減、`G_0` 不依賴 `F_c`，定義 `F_c^† = sup{F : G_1(F) − F ≥ G_0}`（`G_1` 為階梯函數，方程式可能無根，故以 sup 定義），則 `y_c^* = 1 ⇔ F_c ≤ F_c^†`（等號處為 tie）。此性質在 B 成立；在 C（optimistic、pessimistic 分別）也成立，因為 `F_c` 只進 leader 目標與池化預算，不進部門帳本（前提：chargeback `τ` 不是 `F_c` 的函數）。對重用 `δ`（以來源為索引，§10）：`δ` 只作用於 `s_c = S` 的格，故 `G_0` 不依賴 `δ`，而 `G_1` 對 `δ` 非遞減，在 B 中 break-even `δ^†` 唯一；**在 C 中只有 (AL) 成立時才保證單調**——成本下降可能改變不對齊部門的回應而使 leader 價值下降，此時 `δ^†` 以掃描報告，不宣稱唯一。∎

**P5（序位重標不變）** 對任何 ordinal 構念施加嚴格遞增重標，並同時套用到等級與要求表，`Φ`、可行集合與最適解不變。*證明：* ordinal 值只出現在 `≥` 與查表索引。∎

**P6（單位與期間尺度不變）** 所有 TWD 量乘以 `α>0`，`F` 乘以 `α`，argmax 不變；所有 `/period` 參數（`N`、期間成本、容量、`ē`）同乘 `s>0`，`F` 乘以 `s`，argmax 不變。∎ 注意：這**不等於**改變期間長度 `T`——年金因子 `AF(r_d,H)` 對期間長度不是線性的，改變 `T` 時必須以新的 `r_d`、`H` 重新期間化，結果不保證不變。

**P7（要求放寬單調，Model B）** 在固定 `θ` 與成本下，放寬任一要求表（`H^req`、`WI^req`、`EA^req`、`G^req`、`R^req`、`ē`）只會擴大 B 的可行集合，故 `F^{B*}` 不減，`RE^B ≤ 0`、`PR^B_X ≥ 0`。在 Model C 中，此結論只在 (AL) 成立時保證成立。∎（`G_j(γ)` 是 permission level，不在要求表之列，歸入賦能。）

**P8（要求的篩選作用，Model C）** 若 (AL) 不成立，收緊要求可能**嚴格提高** leader 價值：要求縮小部門的可選集合，可以排除部門偏好但對企業不利、且無法以 envelope 阻擋的配置。46 的手算實例中，對 `EA` 加上門檻使 `F^C` 由 10 升至 15（等於 `F^B`），而 `F^B` 不變。∎

**P7 與 P8 合起來是 Q3、Q5 的判讀基礎：** 治理要求在模型內的正價值只能來自三個管道——(i) **賦能**（Allow 與 `G_j(γ)` 使原本不可行的較高授權配置成為可行）；(ii) **穩健可行**（使 portfolio 在整個 `Θ_g` 上仍滿足硬限制）；(iii) **篩選**（只在雙層且帳本不對齊時，以規則替代無法以預算達成的協調）。在集中規劃或帳本對齊時，要求本身不會增加已定價的價值。

---

## 16. M5 動態擴充（不進 baseline）

期間 `t = 1,…,T`，狀態 `ξ_t = (y_t, Θ_t, Ξ_t)`：已建能力、目前可接受參數集合、累積使用經驗（吸收能力的可觀察代理，若有）。

**(D1) 評估回饋配置（G11）：** `b_{t+1} = Π(b_t, O_t)`，`O_t` 為第 `t` 期觀察結果；研究問題是 `Π` 的經驗形式，而不是假設其最適。

**(D2) 資訊取得（G12）：** 試點 `k^pilot` 為小量 `N` 的配置，其成本進 `t` 期目標，其觀察使 `Θ_{t+1} ⊂ Θ_t`。動態目標：

$$
\max\ \mathbb E\Big[\sum_t \beta^t F_E(b_t, x_t;\theta)\Big]
$$

需要跨期資料才可識別；在此之前只報 §13.5 的靜態診斷。Option value 與 real-option 評價（Benaroch & Kauffman, 1999）屬此層。

---

## 17. A/B 模型選擇紀錄

| # | 方案 A | 方案 B | 識別需求 | 理論一致性 | 資料需求 | 計算 | **Canonical** | 另一版 |
|---|---|---|---|---|---|---|---|---|
| D1 | 增量目標（相對 status quo） | 絕對目標 | A 只需差額 | 同 | A 較低 | 同 | **A** | B 僅作檢查 |
| D2 | 部門帳本拆分（OBJ-U） | 39 版成本最小化 | A：帳本文件可觀察；B：隱含 `v^u=0` | A 不製造假衝突 | A 需拆帳 | 同 | **A**（B 為特例） | B 作 sensitivity |
| D3 | Envelope 分配（部門問題可分離） | 共用池先到先得（多 follower 共享限制，需 GNEP） | A：預算制度可觀察；B：需優先規則 | A 對應一般預算分配 | 同 | A 精確有限；B 需均衡概念 | **A** | B 於附錄，僅在證據顯示無 envelope 時 |
| D4 | 時間線性計價 `λ_ℓ` | 非對稱（增加以全薪、節省以實現比例 `φ`） | A：`λ` 可公開界定；B：需 `φ` | A 保持 multilinear，可精確穩健檢查 | A 較低 | A 精確 | **A** | B 作 sensitivity |
| D5 | 嚴重事件次數硬上限 (F9) | 合規損失貨幣化 | A：policy 可觀察 | A 遵守不可貨幣化規則 | A 較低 | 同 | **A** | B 不採用 |
| D6 | 有限列舉＋Lemma E | MILP／KKT | A 精確 | KKT 對整數下層不成立 | 同 | A 在參考規模可行 | **A** | 大規模用 MIBLP（Kleinert et al., 2021） |
| D7 | 集合式穩健（`Θ_g`＋regret） | Bayesian 期望 | B 需先驗，未識別 | A 不偽造分布 | A 較低 | A 在 B 的整體 portfolio 層級可精確（Lemma R），其餘以列舉／抽樣 | **A** | B 僅在有可辯護先驗時 |
| D8 | 重用查表以能力**來源**（無／共享／本地）為索引 | 以能力是否可用為索引 | A 需分別估本地與共享版成本 | A 允許兩者品質與成本不同；B 會使 `δ` 作用於本地版而破壞 P4 | A 略高 | 同 | **A** | — |
| D9 | 預算包含增量每事件營運支出 | 預算只含導入成本 | A 需 `c` 的帳務歸屬 | A 使 envelope 能約束高營運支出的配置 | 同 | 同 | **A** | B 只在 `B̄` 依制度明確只涵蓋導入時 |

---

## 18. 輸出契約（`portfolio_result` v2.1）

```
scenario_group, theta_id, model ∈ {A, C0_opt, C0_pess, A+, B, C_opt, C_pess, D_opt, D_pess},
status ∈ {OK_POINT, OK_INTERVAL, RESTRICTED_SOLVE, THRESHOLD_MODE, PARTIAL_OBJECTIVE,
          FOLLOWER_LEDGER_UNIDENTIFIED, UNEVALUABLE_INITIATIVE, STATUS_QUO_NONCOMPLIANT,
          DESIGN_INFEASIBLE_UNDER_RESPONSE,
          REJECT_INSUFFICIENT_IDENTIFIED_INPUTS, INVALID_SCHEMA_OR_UNITS, INFEASIBLE, NOT_COMPARABLE},
y, y_loc, gamma, envelopes, configs{j: k}, F_E, F_u{u}, F_E_minus_time, delta_hours,
binding{constraint: PR}, requirement_status{j: AT|ABOVE},
VRA[opt,pess], DL0[opt,pess], VCP, VSC, DL[opt,pess], NEV[lo,hi], VG, EE, RE, CE, F_c_threshold{c}, delta_threshold{c},
VRG, design_response_regret,
robustness{element: ROBUST|CONDITIONAL|FRAGILE|UNIDENTIFIED}, max_regret,
interface_activation{I1..I4}, missing_inputs[], excluded_configs[], provenance_summary
```

所有輸出附產生它的參數 provenance 摘要；`SIMULATED_ONLY` 的結果不得出現在 Chapter 4 實證段落。

**本檔為 v2.1 canonical candidate；任何實作與正文方程以本檔為準。若正文與本檔不一致，以本檔修正正文。**

---

## 19. Phase F 對抗式稽核後的修訂紀錄

| # | 稽核發現 | 嚴重度 | 修訂 |
|---|---|---|---|
| 1 | P7（`RE ≤ 0`）在 Model C 不成立：要求可篩除不對齊部門的不利選擇 | HIGH | P7 限於 B（或 C 在 AL 下）；新增 P8（篩選）；Q3、Q5 判讀加入 C 的篩選管道 |
| 2 | Lemma R 對決策元素層級與 Model C 不精確 | HIGH | §13.3 限定 Lemma R 只用於 B 的整體 portfolio；元素層級用充分條件＋列舉／抽樣 |
| 3 | 重用表以可用與否為索引時，`δ` 作用於本地版，`δ^†` 在 B 中可能多次切換 | HIGH | 改以能力來源為索引（§10、D8）；46 中 `δ` 掃描於允許本地自建時仍單調 |
| 4 | P1 漏掉治理成本條件，VCP 可為負 | MEDIUM | P1 與 `NOT_COMPARABLE` 條件加入 `ΔC^gov` 與 `γ` 可選性；46 加斷言 |
| 5 | 現況基準隨能力狀態移動；既有能力 `F_c` 使現況分數為負 | MEDIUM | (V2) 以 `g_{j0}(ȳ^cur)` 為基準；(OBJ-E) 以 `y_c − y^cur_c` 計；F2–F9 對 `k=0` 一律適用 |
| 6 | `G_j(γ)` 被當成要求，致 B 中 `RE > 0` | MEDIUM | `G_j(γ)` 明定為 permission level，歸入賦能區塊 |
| 7 | 設計 portfolio 在實際反應下可能不可行，VRG 與 regret 不定義 | MEDIUM | 新增 `DESIGN_INFEASIBLE_UNDER_RESPONSE` |
| 8 | 每事件營運支出不在預算內，使 envelope 無法約束 | MEDIUM | `a^{BUD}` 加入增量營運支出（D9） |
| 9 | VCP 混合了重分配與帳本對齊 | MEDIUM | 新增 Model C0；`VCP = VRA + DL0` |
| 10 | 參考實作以預設值補缺（Allow、chargeback、中央出資比例） | MEDIUM | 46 改為嚴格查表；缺帳本拆分時 B 可解、C 拒算 |
| 12 | 實作與規格對 `k=0` 的處理不一致 | LOW | 規格與實作統一：限制對所有 `k` 適用，不中止求解 |
| 13 | P6 的「期間長度」敘述錯誤（年金因子非線性） | LOW | P6 改為「所有 /period 參數同乘」 |
| 14 | `F_c^†` 「唯一根」不精確；Lemma E 集合「等於」應為「包含於」 | LOW | 以 sup 定義；改為 ⊆ |

（第 11、15 項為正文用語與文獻強度問題，於 44 修訂。）
