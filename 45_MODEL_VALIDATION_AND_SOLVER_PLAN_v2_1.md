# Model Validation and Solver Plan v2.1

**狀態：v2.1 candidate，2026-10-10。** 本檔列出 `42_ENTERPRISE_PORTFOLIO_MODEL_v2_1.md` 的實作驗證計畫與目前執行狀態。`46_enterprise_portfolio_solver_v2_1.py` 是 synthetic reference oracle；其執行紀錄 `47_SOLVER_ORACLE_RUN_v2_1.txt` 只構成 V3／V5／V6 的**部分**證據，不構成企業實證校準。

---

## 1. 求解器架構

| 層 | 內容 | 42 對應 | 46 狀態 |
|---|---|---|---|
| Schema／單位層 | 型別包裝（ordinal guard、機率正規化、允許反應集合） | §1、§6 | 部分實作：`Ord` 禁止算術與跨構念比較；`ρ/P/π` 正規化；禁止反應拒絕。TWD／hours 型別包裝沿用 `35_schema_validator_synthetic_v1_6.py`，**尚未整合** |
| Precompute 層 | `Φ_jk`、`φ_jk`、`φ^u_jk`、資源使用 | §5、§7、§8 | 已實作（`jk_eval`） |
| Follower 層 | 部門計畫列舉、回應集合、ties | §12.3 | 已實作（`unit_plans`、`unit_response`） |
| Envelope 層 | Lemma E 有限化 | §12.4 | 已實作二維 `{BUD, ENG}`（`envelopes_lemmaE`＋Pareto 篩選） |
| Leader 層 | 多選擇背包（完整列舉） | §12.5 | 已實作（`solve_bilevel`）；DP 版本 **PENDING** |
| 型態比較層 | A、A+、B、C、指標 | §11 | 已實作（`architecture_metrics`）；Model D **PENDING（預設不執行）** |
| 治理與門檻層 | EE／RE／CE、`F_c^†` | §14 | 已實作（`governance_decomposition`、`capability_threshold`）；`δ^†` **PENDING** |
| 不確定性層 | `Θ_g`、頂點檢查、robust feasibility、分類、MaxRegret、VOI | §13 | 分類邏輯已實作（`robustness_class`）；**頂點列舉（Lemma R）、robust feasibility、MaxRegret、VOI 均 PENDING** |
| 輸出層 | `portfolio_result` v2.1 | §18 | **PENDING** |

---

## 2. 測試清單

狀態：`PASS-SYN` = 在 46 的 SIMULATED_ONLY 實例上通過；`PENDING` = 尚未實作；`N/A-EMP` = 需企業資料。

### 2.1 Schema 與單位（V3）

| ID | 測試 | 判準 | 狀態 |
|---|---|---|---|
| T-SCH-1 | `π`、`P`、每列 `ρ` 非負且和為 1 | 違反即 `INVALID_SCHEMA_OR_UNITS` | PASS-SYN（`ρ` 加 0.2 被拒） |
| T-SCH-2 | 禁止反應有正機率 | 拒算 | PASS-SYN |
| T-SCH-3 | ordinal 算術 | `TypeError` | PASS-SYN |
| T-SCH-4 | 跨構念 ordinal 比較 | `TypeError` | PASS-SYN |
| T-SCH-5 | TWD/event × events/period → TWD/period；TWD/period 不可與 TWD/event 相加 | 型別錯誤拒算 | PENDING（整合 35 的 typed units） |
| T-SCH-6 | `ω` 不得出現在 `ρ` 的鍵中 | schema 拒絕 | PASS-SYN（結構上 `ρ` 以 `(z, ℓ)` 為鍵）；需加入顯式斷言 → PENDING |
| T-SCH-7 | 非有限金額（NaN、inf） | 拒算 | PENDING（35 已有，需整合） |

### 2.2 查表完整性與缺值（V4）

| ID | 測試 | 判準 | 狀態 |
|---|---|---|---|
| T-MIS-1 | 非現況配置的結果格缺值 | 該配置被排除，回報 `RESTRICTED_SOLVE` | PASS-SYN（排除行為）；狀態碼輸出 PENDING |
| T-MIS-2 | 現況配置的結果格缺值 | `UNEVALUABLE_INITIATIVE`，不得求解 | PASS-SYN（拋出 `MissingInput`） |
| T-MIS-3 | `F_c` 缺 | `THRESHOLD_MODE`，報 `F_c^†` | PENDING（門檻計算已有，模式切換未接） |
| T-MIS-4 | `λ` 缺 | `PARTIAL_OBJECTIVE` 兩分量輸出 | PENDING |
| T-MIS-5 | 帳本拆分缺 | B 可解；Model C 不解，`FOLLOWER_LEDGER_UNIDENTIFIED` | PASS-SYN |
| T-MIS-8 | 缺 `Allow`、`Allow^loc`、chargeback、`G_j(γ)`、要求表格時不得以預設值補 | 視為缺值（配置排除或拒算） | PASS-SYN（缺 Allow 被記錄為排除） |
| T-MIS-6 | 任何缺值都不得以 0 進入目標 | 對每個缺值情境，比較「補 0」與實作行為，必須不同 | PENDING |
| T-MIS-7 | 現況違反 (F2)／(F9) | `STATUS_QUO_NONCOMPLIANT` | PASS-SYN（拋出） |

### 2.3 Synthetic oracle 與求解（V5）

| ID | 測試 | 判準 | 狀態 |
|---|---|---|---|
| T-ORC-1 | P1 排序 `A ≤ C0 ≤ A+ ≤ B`、`C0 ≤ C ≤ B`（opt 與 pess） | 6 seeds × aligned／misaligned | PASS-SYN |
| T-ORC-2 | P2 對齊 ⇒ `DL = DL0 = 0`（opt 與 pess） | 6 seeds | PASS-SYN；隨機不對齊實例 DL > 0 為 0／6，DL > 0 只在手算實例出現——**不對齊不必然造成 DL**（P2 只給必要條件） |
| T-ORC-3 | `NEV = VCP + VSC − DL`、`VCP = VRA + DL0` | 恆等式 | PASS-SYN |
| T-ORC-4 | Lemma E：有限 envelope 結果 = 整數網格 envelope 結果 | opt 與 pess 皆相同 | PASS-SYN |
| T-ORC-5 | 共享固定成本只計一次 | 以原始查表獨立重算 portfolio 價值等於求解值；`F_c` +1 時 `F_E` 恰 −1（4 個 initiatives 共用） | PASS-SYN（取代原先的套套邏輯測試） |
| T-ORC-6 | Ties：部門無差異但企業貢獻不同時，optimistic > pessimistic | 構造實例 | PASS-SYN |
| T-ORC-7 | (F9) 硬上限排除配置且不貨幣化 | 構造實例：4 個配置被排除 | PASS-SYN |
| T-ORC-8 | 手算 oracle：2 部門 × 1 initiative × 2 配置 × 1 能力，三個情境（對齊；不對齊但 envelope 可阻擋；不對齊且不可阻擋），手算表見 46 `test_hand_oracle` docstring | 逐項相等：B=C=30；B=C=15（DL=0）；B=15、C=10、DL=5、VSC=15、NEV=10 | PASS-SYN（手算表由研究者推導；仍建議第二人獨立重算） |
| T-ORC-9 | DP 背包版本 = 完整列舉 | 整數成本實例 | PENDING |
| T-ORC-10 | Shared vs no-shared：`VSC ≥ 0`；在 `F_c → ∞` 時 `VSC → 0` | 掃描 | VSC ≥ 0 PASS-SYN（P1）；極限掃描 PENDING |
| T-ORC-11 | Model A 可比性檢查：`Σ B^0_u + ΔC^gov > B̄` 時輸出 `NOT_COMPARABLE` | 構造實例 | PASS-SYN |
| T-ORC-12 | Model D 閘門：T1–T5 任一不成立時不執行 | 單元測試 | PENDING |
| T-ORC-13 | 重現性：同參數重跑結果逐位相同 | 兩次執行 | PASS-SYN（固定 seed；需加入顯式比對） |

### 2.3b 方程—實作一致性（Phase F 稽核發現）

| ID | 項目 | 狀態 |
|---|---|---|
| T-ALG-1 | (F5e) `R_j(ȳ) ≥ R^req(A)`、`D(ȳ) ≥ D^req(A)` 在 46 中尚未實作（合成實例未含 R／D 狀態表） | PENDING：加入能力狀態查表與對應測試 |
| T-ALG-2 | (F6)(F7)(F9)(F10)、chargeback 僅在使用共享版本時計入、`C^{impl,x}` 排除於部門帳本 | 已逐行對照 42，與實作一致 |
| T-ALG-3 | Model A 以 (OBJ-E) 評估並扣除 `ΔC^gov(γ)`；部門 envelope 不含治理成本 | 與 42 §11 一致 |
| T-ALG-4 | 部門自建能力在 Model C 受 `Allow^loc_γ` 限制 | 與 42 §4.2 一致 |

### 2.4 不變性與敏感度（V6）

| ID | 測試 | 判準 | 狀態 |
|---|---|---|---|
| T-INV-1 | 金額 ×1000 | `F` ×1000、決策不變 | PASS-SYN |
| T-INV-2 | 期間 ×2（`N`、期間成本、容量同乘） | `F` ×2、決策不變 | PASS-SYN |
| T-INV-3 | 所有 ordinal 構念嚴格遞增重標（含非等距、負值） | 解完全不變 | PASS-SYN |
| T-INV-4 | 角色、initiative、能力的標籤重排 | 解不變（同構） | PENDING |
| T-SEN-1 | P4 門檻：`F_c` 掃描只切換一次；預算寬鬆時 `F_c^† = G_1 − G_0` | 斷言 | PASS-SYN |
| T-SEN-2 | P7（B）：放寬要求 → `F^*` 不減；`VG = EE + RE + CE` 且 `RE ≤ 0`；`G_j(γ)` 歸賦能區塊 | 斷言 | PASS-SYN |
| T-SEN-2b | P8（C）：要求的篩選作用使 `F^C` 上升 | 手算實例 10 → 15 | PASS-SYN |
| T-SEN-3 | Lemma R：在乘積多面體 `Θ_g` 上，頂點檢查結果 = 密集抽樣結果 | 小實例 | PENDING |
| T-SEN-4 | Robust feasibility：只在部分 `θ` 可行的配置被標 `CONDITIONALLY_FEASIBLE` 且不參與 ROBUST 判定 | 構造實例 | PENDING |
| T-SEN-5 | 分類邏輯 ROBUST／CONDITIONAL／FRAGILE | 構造例 | PASS-SYN |
| T-SEN-6 | 預先登記：`𝒢` 在求解前凍結（hash 記錄） | 流程檢查 | PENDING |
| T-SEN-7 | VOI 診斷：固定一區塊後 MaxRegret 不增 | 斷言 | PENDING |
| T-SEN-8 | 以來源為索引的 `δ^†` 在 B 中唯一（允許本地自建） | 8 seeds 掃描，至多 0→1 一次，7 seeds 有切換 | PASS-SYN；C 中不對齊的非單調反例 PENDING |

---

## 3. V0–V7 Gate 狀態（企業研究層級）

| Gate | 內容 | 本輪後狀態 | 下一步需要的證據（依模型需求，不依受訪者） |
|---|---|---|---|
| V0 Source & Authority | 權限、共享資源、initiative 邊界有來源 | OPEN | Block G 與 Block X 的 OBS 文件 |
| V1 Construct Validity | G→M 雙人盲編、錨點內容效度 | OPEN（41 為研究者裁決的 candidate freeze） | 依 41 §1 的 S1–S4 流程盲編；EA-X 錨點內容效度 |
| V2 Cross-functional Pilot | 至少兩種功能脈絡試用量測 | OPEN | Block R 的題卡與 Block V 的結果查表試填 |
| V3 Schema & Units | 型別守恆 | PARTIAL（synthetic；T-SCH-5、7 待整合） | 整合 35 typed units |
| V4 Lookup Completeness | 缺格拒算 | PARTIAL（synthetic；狀態碼輸出待完成） | T-MIS-3 至 6 |
| V5 Enterprise Portfolio Solver | oracle、centralized vs bilevel、ties | PARTIAL（synthetic；T-ORC-8 獨立手算 oracle 未完成） | T-ORC-8、9、11、12 |
| V6 Invariance & Sensitivity | 不變性、`Θ_adm` 分類 | PARTIAL（synthetic；Lemma R、robust feasibility 未實作） | T-SEN-3、4、6、7、8 |
| V7 Enterprise Empirical Calibration | 企業資料交叉核對 | OPEN | 全部 43 的 OBS／EXP 參數 |

**沒有任何 gate 整體通過。** 46 的 `SYNTHETIC_ORACLE_PASS` 只表示 42 的命題在隨機合成實例上沒有被反駁，以及實作與方程一致；它不表示任何企業結論。

---

## 4. 下一個實作切片（依序）

1. 由第二人獨立重算 T-ORC-8 手算表。
2. 整合 35 的 typed units（T-SCH-5、7）與缺值狀態碼（T-MIS-3 至 6），實作 `portfolio_result` 輸出。
3. Lemma R 頂點檢查與 robust feasibility（T-SEN-3、4），再加 MaxRegret 與 VOI（T-SEN-7）。
4. DP 背包（T-ORC-9），使中等規模可解。
5. 任何新功能都要在同參數下與完整列舉比對，並更新 47 的執行紀錄。
