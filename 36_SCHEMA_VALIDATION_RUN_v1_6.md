# 多單位、多角色資料契約合成驗證 v1.6

**狀態：局部合成驗證；不包含任何企業實際參數、決策權、流程或問卷結果。** 本增量接續 `30` 的 V3/V4 前置檢查與 `34` 的未涵蓋清單。程式為 `35_schema_validator_synthetic_v1_6.py`，以 `python 35_schema_validator_synthetic_v1_6.py` 執行。v2.0 scope correction 後，本檔只保留為 enterprise portfolio schema 的歷史 synthetic evidence，不代表任何特定部門或流程。

## 本輪可執行界線

1. fixture 包含兩個**泛化 business-unit / initiative synthetic units**、每單位兩種角色、一個可見訊號與兩種隱藏結果。`ρ` 的索引只有 `option,role,z`，不含行動當下看不到的 `ω`。角色權重、`P(z,ω)` 與各角色的 `ρ` 必須各自非負且總和為 1；每個正規化反應與隱藏結果組合均需有結果查表。
2. 政策允許集先篩方案，再以 `(A,κ)` 查 H、WI、EA-V 三個**逐構念**最低門檻；若 A3 與「人保留最後決定權」同時出現即拒絕。序位鍵只比較同構念門檻，不進入收益算術。禁用的第一線反應不得有正機率。
3. 用 `TWDPerEvent`、`TWDPerPeriod`、`HoursPerPeriod` 包裝不同單位；事件數為每期間非負整數。結果以「事件數 × 每事件金額」轉為每期間金額，實施成本只能以每期間金額扣除，容量以每期間小時計。預算與容量過濾跨單位組合。

## 重現結果與限定範圍

既有執行 exit code 0，回傳 `SYNTHETIC_SCHEMA_PARTIAL_PASS`。合成事件數分別為 2 與 3；預算 8 TWD／期、容量 4 小時／期。四種可行組合的淨值按程式順序約為 62、58、54、50 TWD／期。容量收緊至 2 或預算收緊至 0 時，均只剩兩個 synthetic units 的 `human` option，淨值 50 TWD／期。

12 種反例被拒絕：角色權重與 P 不正規化、角色反應缺格、隱藏結果缺格、禁用反應有正機率、門檻不足或缺漏、A3 與人類最終權限矛盾、序位用數字、結果與預算單位錯置、非有限金額。浮點輸出可能顯示 61.99999999999999；斷言以容差比較。

## v2.0 解讀

此程式可以支持以下 enterprise-scope implementation claims：

- 多個 synthetic units 可共享同一 budget / capacity constraint。
- role weights、visible-signal response 與 hidden outcome 可以在 schema 層分離。
- ordinal requirements 與 monetary arithmetic 可以被型別／validation rule 分開。
- missing threshold、missing outcome、invalid probability 或 incompatible authority 可以被 fail closed。

但它**不能**支持：

- enterprise shared platform cost / governance cost 的真實估計
- business-unit preference conflict
- actual user response probability
- enterprise capability reuse / economies of scale
- cross-unit policy externality
- `Θ_adm` robustness classification
- empirical enterprise AI adoption effect

## 驗證邊界

此程式仍是 schema／policy／unit／有限組合檢查，不是 `39_ENTERPRISE_MULTILEVEL_MODEL_AND_DATA_CONTRACT_v2_0.md` 的完整 Enterprise–Business Unit portfolio solver。它沒有估計 `ρ`、`P`、`π`，沒有區間 `Θ_adm`、非貨幣限制、shared fixed cost、portfolio sequencing 或 empirical calibration。

`33_bilevel_validation_fixture_v1_5.py` 的 Manager–Boss tie 測試保持為另一組 synthetic regression，不得與本檔拼接成 v2.0 V5 全面通過。

## v2.0 後續驗收切片

下一版 solver 應以泛化 enterprise fixture 驗證：

1. 至少兩個 business units、三個以上 initiatives 與一個 shared capability。
2. shared platform fixed cost 只計一次。
3. enterprise budget、engineering capacity 與 policy constraints 同時存在。
4. local managers 的可行集合與 enterprise portfolio objective 可不同。
5. Manager ties 有 optimistic / pessimistic enterprise bounds。
6. centralized planner 與 bilevel portfolio 在同參數下可重現比較。
7. `UNIDENTIFIED` lookup cell 必須停止 point optimization。
8. `Θ_adm` 掃描後輸出 `ROBUST / CONDITIONAL / FRAGILE / UNIDENTIFIED`。

**因此，本檔在 v2.0 的地位是 reusable synthetic validation evidence，而不是舊 scope 的案例驗證紀錄。**