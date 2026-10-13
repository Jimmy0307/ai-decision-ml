# 126 MATHEMATICAL MODEL FORENSIC AUDIT v1.1

> 日期：2026-10-13｜對象：119–127 v1.6.1 RC｜狀態：ENGINEERING / SOURCING MATH RC
> 本檔只報告可檢驗的工程與數學稽核事實。所有數值例子皆為 `SIMULATED_ONLY`；`ORG_MAPPING_HUMAN_VALIDATION = PENDING`、`ENTERPRISE_EMPIRICAL_STATUS = PENDING`。

## 1. Final gate

```text
MATHEMATICAL_COLLISION_FOUND = NO
CANONICAL_SYMBOLS = PASS
VALUE_LEDGER = PASS
USAGE_MIXTURE = PASS
PORTFOLIO_FORMULATION = PASS
ENGINEERING_DEMAND_MODEL = PASS
INTERNAL_STAFFING_MODEL = PASS
EXTERNAL_SOURCING_MODEL = PASS
MARGINAL_COST_DEFINITION = PASS
MARGINAL_VALUE_DEFINITION = PASS
TEAM_SIZE_OPTIMIZATION = PASS
BUILD_BUY_HYBRID_LOGIC = PASS
A_B_C_BACKWARD_COMPATIBILITY = PASS_WITH_INHERITED_CERTIFIED_CROSSCHECK
NO_DOUBLE_COUNTING = PASS
SYNTHETIC_REPRODUCTION = PASS
ORG_MAPPING_HUMAN_VALIDATION = PENDING
ENTERPRISE_EMPIRICAL_STATUS = PENDING
```

`PASS_WITH_INHERITED_CERTIFIED_CROSSCHECK` 的意思不是本輪重新執行 51。v1.6 已對 51 的 14 個實例完成 386 個比較並通過；本輪執行環境沒有把 51 物化到本機，因此不冒充 fresh rerun。本輪已確認 v1.6 → v1.6.1 的 `Adapter51`、`load51`、`crosscheck51` 三段程式碼逐字不變，且 GitHub 目前 `calibration/v1.1-variable-model` 基準歷史中的 `51_enterprise_portfolio_solver_v2_2.py` blob SHA 為 `7ec816284010bf4e743cdc356fa5d3a27f097134`。新的 time-regime 與 single-skill collapse 測試則是本輪 fresh execution。

## 2. v1.6.1 修正範圍

本輪只修四件事：

1. **physical capacity 與 financial annualization 分離**：`IMPLEMENTATION_YEAR` 成為 canonical staffing regime；BUILD 工時完整進入導入年度容量限制，RUN 工時照當期計入。
2. **保留 levelized sensitivity**：`STEADY_STATE_LEVELIZED` 仍可用 `AF(r_d,H)` levelize BUILD，但只表示長期穩態平均容量，不得冒充建置年尖峰可行性。
3. **比較量名稱鎖定**：原 06 的 `VSC/VCP/DL/NEV` 只屬 `PLANE_OFF`；技能固定制用 `^{W,fix}`；內生工程制用 `^{ENG}`。
4. **single-skill collapse regression**：當 `|W^{ENG}|=1` 且需求與容量逐項對齊 06、外部容量關閉時，`SKILL_FIXED` 必須退化為 `PLANE_OFF`。

沒有改動 R14 凍結數字、α／ρ 語意、A/B/C/C0/A+/D baseline semantics、51、65 或 `org_schema.py`。

## 3. Fresh tests

本輪先以 TDD 建立三個失敗測試，再實作：

- `TIME_REGIMES` / canonical time-regime contract；
- BUILD=100、RUN=20 時，`IMPLEMENTATION_YEAR = 120`，`STEADY_STATE_LEVELIZED = AF×100+20`；
- single-skill collapse 下 B、A+、C(opt/pess)、C0(opt/pess)、A(opt/pess) 逐一相等。

`pytest -q test_v161_time_regime.py`：**4 passed**（fresh，2026-10-13）。

另以 124 本體 fresh 執行兩個核心機制檢查：test 16 得 `implementation=120.0`、`levelized=56.720856...`；test 17 對 B、A+、C/C0 opt/pess、A opt/pess 的 8 個差值全部為 0。

目前 124 的接受測試共有 17 項。除 test 12 的 crosscheck 證據沿用 v1.6 certified snapshot 外，其餘改動範圍在本輪重新求解。新增：

- `16_physical_build_hours_not_financially_annualized = PASS`
- `17_single_skill_collapse_to_06 = PASS`（8 個比較量差均為 0）

完整執行記錄見 125；結構化結果見 `124_REFERENCE_RESULT_v1_1.json`（工作證據，不是企業資料）。

## 4. Planning-time regime result（SIMULATED_ONLY）

同一個合成實例：

| regime | 性質 | F_E | AI_LLM FTE | DATA FTE | INTEG FTE | AI_LLM 外部時數 |
|---|---|---:|---:|---:|---:|---:|
| IMPLEMENTATION_YEAR | canonical | 11,367.21404 | 2 | 1 | 2 | 200 |
| STEADY_STATE_LEVELIZED | sensitivity only | 19,861.089075 | 1 | 1 | 1 | 0 |

這個差異本身就是為何不能拿 financial/levelized hours 當作 physical staffing feasibility：levelized regime 會把一次性 BUILD 需求攤薄，導致較低的建置期人力與較高的可行 portfolio。它不是企業估計，也不能被解讀為 levelized 制度「比較好」。

## 5. Regime naming / VSC boundary

v1.6 曾出現 `VSC = 3,727 → 0` 的表面衝突。根因不是 VSC 方程失效，而是可行集合不同：

- `PLANE_OFF`：06 單一池化 ENG 資源；使用原始比較量名稱。
- `SKILL_FIXED`：逐技能、不可替代、現有人力固定；使用 `VSC^{W,fix}` 等。
- `ENDOGENOUS`：逐技能 + 內生 staffing/sourcing；使用 `VSC^{ENG}` 等。

跨 regime 的差不得直接敘述為同一制度下的 improvement / deterioration。

## 6. Single-skill collapse

若把所有工程需求、既有人力容量與固定容量聚合成唯一技能 `ENG`，且外部容量停用，則：

\[
\mathcal F^{W,fix}=\mathcal F^{OFF}.
\]

124 test 17 對 B、A+、C(opt)、C0(opt)、C(pess)、C0(pess)、A(opt)、A(pess) 共 8 個最適值逐一檢查，差值均為 0。這證明技能模型在單技能極限下是 06 的 refinement，而不是 unrelated model。

## 7. Ledger audit

維持規則：**one economic consequence → one monetary ledger location**。

- 內部增量 FTE 費用：`ΔC^int_w`；
- 容量型顧問：`C^ext_w`；
- 固定總價交付：`C^impl` 或 `F_c`；
- API / inference：事件成本 `c`；
- business-process human time：`λ_ℓ t`；
- AI engineering labour 不進 `λ_ℓ t`。

貨幣成本可做財務年化；**physical BUILD hours 在 canonical implementation-year capacity 中不得做 financial annualization**。

## 8. Remaining limitations

- `IMPLEMENTATION_YEAR` 檢查全年總實體工時，不是月／季內排程；短期尖峰、招募 lag、合約 lead time 仍需多期／期內模型。
- 技能不可替代仍是作者定義假設；cross-skill productivity matrix 未建模。
- Model A 的內生 staffing 版本（A-ENG）仍未定義，因此 `ENDOGENOUS` 下 A 與含 staffing 的 B/C 不直接比較。
- 新增工程參數仍未有企業資料；所有 staffing/headcount 結果仍是 `SIMULATED_ONLY`。
- ORG-V 人類驗證與企業實證皆維持 PENDING。

## 9. SHA-256

1808f2644b68e5d2e5a4fb748261e7d879faf3e032318cf81c4f22b0aa434116  119_ENTERPRISE_AI_CANONICAL_MATHEMATICAL_MODEL_v1_1.md
8b38369951729bc6b301731e0d4e1e0a583a8d79ea9b42ea440cc5bc452d31b6  120_MATHEMATICAL_SYMBOL_DICTIONARY_v1_1.xlsx
ddd2f8d8ad633d2aea3a1da9e5d70734dd7208cd236bf4f59fc3be5cc9040d32  121_ENGINEERING_ECONOMIC_LEDGER_v1_1.xlsx
d6b503f3cdd017a1c532a2cb1e34c44fc46050ffe8575328220b7b02a4002aea  122_ENGINEERING_SOURCING_MODEL_SPEC_v1_1.md
5cb3af68daaf13b4f229451dc25728f28b14cfc22a1e76582a118daa86a59128  123_ENGINEERING_SOURCING_SYNTHETIC_EXAMPLE_v1_1.xlsx
1a1aa58c1ad235b5fea6682401288be534f9fb98af6f6d282ccdab36e1cce995  124_engineering_sourcing_model_reference.py
865b8507303296cfd6bc336f8aae6bf914c686dc291825d2862139477c8d235d  125_ENGINEERING_SOURCING_MODEL_RUN_v1_1.txt
147834c115bf8cf338697d16af31e150d8bc3d5a5d196f43ae5db15dadbe6d38  127_MERGED_MASTER_THESIS_R14_TO_ENTERPRISE_v1_6_1_MATH_RC_CANDIDATE.md
