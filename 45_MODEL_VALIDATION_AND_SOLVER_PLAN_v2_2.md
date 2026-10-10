# Model Validation and Solver Plan v2.2

**狀態：v2.2 engineering candidate，2026-10-11。Supersedes `45_MODEL_VALIDATION_AND_SOLVER_PLAN_v2_1.md`（保留作 provenance）。** 本檔列出 `42_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md` 的驗證計畫與執行狀態。`51_enterprise_portfolio_solver_v2_2.py` 是 synthetic reference oracle（46 保留）；執行紀錄 `52_SOLVER_ORACLE_RUN_v2_2.txt`，測試證據與稽核紀錄 `50_SOLVER_COMPLETION_AND_V3_V6_VALIDATION_v2_2.md`。所有結果為 `SIMULATED_ONLY`，不構成企業實證校準。

**Synthetic verdict：`V2_2_SYNTHETIC_ENGINEERING_VERDICT: PASS`（20/20 必要項，另 STATE、REG、AUDIT 群組通過）。**

---

## 1. 求解器架構（51）

| 層 | 內容 | 42 v2.2 | 51 狀態 |
|---|---|---|---|
| Schema／單位層 | `Q` typed units、`Ord` guard、`ω` guard、NaN/inf、機率列、路徑格欄位集合、要求表鍵型別 | §1、§6 | 已實作並測試（T-SCH-1–7） |
| Precompute 層 | `Φ_jk`（含 F5e 於所選狀態）、`φ_jk`、`φ^{−time}_jk`、依角色的 `ΔHours`、`φ^u_jk`、資源使用 | §5、§7、§8 | 已實作（`jk_eval`） |
| Follower 層 | 計畫列舉、缺值局部排除、ties | §12.3 | 已實作（`unit_plans`、`unit_response`） |
| Envelope 層 | Lemma E′ | §12.4 | 已實作（`envelopes_lemmaE`）；v2.1 乘積集合保留作交叉檢查 |
| Leader 層 | 多選擇背包：列舉與 DP（下界／上界／退回列舉） | §12.5 | 已實作（`mck_enum`、`mck_dp`） |
| 型態比較層 | A、C0、A+、B、C、指標；Model D 閘門 | §9.2、§11 | 已實作（`architecture_metrics`、`solve_model_D`） |
| 治理與門檻層 | EE／RE／CE、`F_c^†`（B；C opt/pess）、`δ` 掃描 | §14、§15 | 已實作 |
| 缺值狀態機 | 13 個狀態、無例外路徑、無靜默補零 | §13.4、§18 | 已實作（`solve`） |
| 不確定性層 | registry 驗證與承諾、可行性四類、Lemma R（範圍守衛）、MaxRegret、vertex／grid VOI、元素層級分類 | §13 | 已實作（`solve_robust` 等） |
| 輸出層 | `portfolio_result` v2.2 | §18 | 已實作 |

## 2. 測試清單

狀態：`PASS-SYN` = 在 51 的 SIMULATED_ONLY 實例上通過；`N/A-EMP` = 需企業資料。

### 2.1 Schema 與單位（V3）

| ID | 判準 | 狀態 |
|---|---|---|
| T-SCH-1 | `π`、`P`、`ρ` 非負且和為 1 | PASS-SYN（v2.1；51 沿用） |
| T-SCH-2 | 禁止反應有正機率 → 拒算 | PASS-SYN（51 在 schema 層拒絕） |
| T-SCH-3／4 | ordinal 算術、跨構念比較 → `TypeError` | PASS-SYN |
| T-SCH-5 | typed units：維度代數、4 種不相容運算拒絕、typed φ = float φ | **PASS-SYN（v2.2）** |
| T-SCH-6 | `ω` 出現在 `ρ` 鍵 → 拒算；能力狀態鍵合法 | **PASS-SYN（v2.2）** |
| T-SCH-7 | NaN／±inf／越界機率 → 拒算（57＋1 個突變） | **PASS-SYN（v2.2）** |

### 2.2 查表完整性與缺值（V4）

| ID | 判準 | 狀態 |
|---|---|---|
| T-MIS-1 | 非現況配置缺格 → 該配置排除、`RESTRICTED_SOLVE` | PASS-SYN（狀態碼已輸出） |
| T-MIS-2 | 現況配置在目前狀態的非局部缺格 → `UNEVALUABLE_INITIATIVE` | PASS-SYN（結果，非例外） |
| T-MIS-3 | `F_c` 缺 → `THRESHOLD_MODE`（B；C opt/pess）；A+/C0 記為未使用 | **PASS-SYN（v2.2）** |
| T-MIS-4 | `λ` 缺 → `PARTIAL_OBJECTIVE`；盒頂點證書；只在證書通過時給 point decision | **PASS-SYN（v2.2）** |
| T-MIS-5 | 帳本拆分缺 → B 可解；C `FOLLOWER_LEDGER_UNIDENTIFIED` | PASS-SYN |
| T-MIS-6 | 20 類缺值 × B、C：不得與補零無法區分 | **PASS-SYN（v2.2；三分判準）** |
| T-MIS-7 | 現況違反 (F2)／(F9) → `STATUS_QUO_NONCOMPLIANT`（結果） | PASS-SYN |
| T-MIS-8 | `Allow`、`Allow^loc`、`G_j`、要求表、chargeback 不得以預設補 | PASS-SYN（`Allow(j,0)` 缺只排除 `k=0`） |
| STATE | 13 個狀態皆可達且以結果回傳 | **PASS-SYN（v2.2）** |

### 2.3 Oracle 與求解（V5）

| ID | 判準 | 狀態 |
|---|---|---|
| T-ORC-1–7、11 | v2.1 項目 | PASS-SYN（REG 群組回歸） |
| T-ORC-8 | 獨立手算 oracle | **PASS-SYN（v2.2；`INDEPENDENT_COMPUTATIONAL_REDERIVATION_PASS`，見 50 §8）** |
| T-ORC-9 | DP = 列舉（20 seeds、預算綁住、800 隨機 MCK、退回列舉） | **PASS-SYN（v2.2）** |
| T-ORC-10 | 大 `F_c`（仍負擔得起）→ 不選、VSC = 0 | **PASS-SYN（v2.2）** |
| T-ORC-12 | Model D 閘門 | **PASS-SYN（v2.2）** |
| T-ORC-13 | 重現性（同程序與新程序，SHA-256） | **PASS-SYN（v2.2）** |
| T-ALG-1 | (F5e) | **PASS-SYN（v2.2）** |
| T-ALG-2–4 | 方程—實作對照 | 與 42 v2.2 一致（v2.1 結論沿用；F5e、λ、DP 部分已重新對照） |

### 2.4 不變性與敏感度（V6）

| ID | 判準 | 狀態 |
|---|---|---|
| T-INV-1–3 | 金額、期間、ordinal 重標 | PASS-SYN |
| T-INV-4 | 標籤重排，完整最適集合同構 | **PASS-SYN（v2.2）** |
| T-SEN-1、2、2b、5 | v2.1 項目 | PASS-SYN |
| T-SEN-3 | Lemma R 範圍：B 整體 portfolio 精確；C 與元素層級 ScopeError；元素層級反例 | **PASS-SYN（v2.2）** |
| T-SEN-4 | 可行性四類（含 witness、UNDETERMINED） | **PASS-SYN（v2.2）** |
| T-SEN-6 | registry 雜湊與承諾（含名目值、精確浮點） | **PASS-SYN（v2.2）** |
| T-SEN-7 | MaxRegret（頂點 = 密集網格最大）；VOI 解析 oracle（vertex 1 vs grid 0.5） | **PASS-SYN（v2.2）** |
| T-SEN-8 | B 中 `δ^†` 唯一；C 中集合值反例 | **PASS-SYN（v2.2）** |
| AUDIT | 兩輪對抗式稽核的回歸測試 | **PASS-SYN（v2.2）** |

## 3. V0–V7 Gate 狀態

| Gate | 本輪後狀態 | 下一步 |
|---|---|---|
| V0 Source & Authority | OPEN | Block G／X 的 OBS 文件 |
| V1 Construct Validity | `V1_AI_PILOT_COMPLETE`；`V1_HUMAN_BLIND_CODING_PENDING`（53B、54A/B、54C、55） | 至少兩位人類編碼者依 53B 完成盲編；EA-X 人類 CVI（56） |
| V2 Cross-functional Pilot | OPEN | Block R 題卡、Block V 查表試填；EA-X 等級累積性檢查 |
| V3 Schema & Units | **COMPLETE（synthetic）** | 企業資料進來時重跑 |
| V4 Lookup Completeness | **COMPLETE（synthetic）** | 同上 |
| V5 Portfolio Solver | **COMPLETE（synthetic）**；建議人工 code review | 同上 |
| V6 Invariance & Sensitivity | **COMPLETE（synthetic）**；元素層級與 C 的分類只以涵蓋率報告 | 預先登記 `𝒢`（真實 registry） |
| V7 Enterprise Empirical Calibration | OPEN | 43 的 OBS／EXP 參數 |

**沒有任何 enterprise gate 通過。** `PASS-SYN` 只表示 51 與 42 v2.2 一致，且命題在 synthetic 實例上未被反駁。

## 4. 下一個切片

1. 人類 V1 盲編（53B）與 EA-X CVI（56 v2.2.1 錨點）；之後依 54C §5 重做 mapping sensitivity。
2. 人工 code review 51（兩輪稽核皆為同一模型家族）。
3. 預先登記真實 scenario registry（`registry_commitment` 於看到結果前寫入）。
4. 大規模時以 MIBLP（Kleinert et al., 2021）取代列舉，並與 51 在小規模上逐位比對。
