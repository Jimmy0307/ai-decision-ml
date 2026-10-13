> **CURRENT COPY (V1.8.1, 2026-10-14) — current copy; history preserved.**
> Historical source: `W\01_ALL_OUTPUTS\AI_DECISION_THESIS_ALL_OUTPUTS\r14_merge_v1_7\133_V0_V7_VALIDATION_LEDGER.md` (sha256 `5440c66e91f522577bece150262d82ef1ec05d2de36432911de397f6f9fbf018`), left unchanged.
> Changed: only stale V9-availability / 2026-09-29 / 依作者回報 / full-reanalysis status spans (3 edits; line-by-line log in `claude/r14_merge_v1_8_1_study1_freeze/12_STALE_STATUS_CLEANUP_REPORT.md`, line numbers = historical file).
> Sentences describing the execution environment at that time are kept verbatim with the marker `〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：…〕`; current-status sentences are updated with citations.
> File names 02–10 refer to `claude/r14_merge_v1_8_source_closure/`; 11/12/15 refer to `claude/r14_merge_v1_8_1_study1_freeze/`.
> No number, G01–G16 content, taxonomy, G→M assignment, model, solver, schema or empirical result was changed. `SUBMISSION_READY = NO`.

# 133 — V0_V7_VALIDATION_LEDGER（v1.7）

日期：2026-10-14　｜　對應稿件：130 表 3-14（第 3.14.4 節）、第 4.7–4.10 節
規則：狀態字串全文統一；「COMPLETE — SYNTHETIC ONLY」只表示工程檢查在合成實例上完成，不是企業層級的通過。

---

## 1. 企業模型的驗證閘門

| Gate | 名稱 | 狀態（全文統一字串） | 已有證據（artifact） | 這個證據**支持**什麼 | 這個證據**不支持**什麼 | 通過條件（exit criteria） | 阻擋什麼 |
|---|---|---|---|---|---|---|---|
| V0 | Source & Authority | **OPEN** | 無企業文件；研究端的來源裁定見 128；倫理與資料治理為前提（130 §3.14.7，DRAFT） | — | 任何「企業現況」的陳述 | 企業的權限、共享資源、initiative 邊界與授權範圍經文件與角色交叉核對；每個 `source_id` 登記於 `S_sources`，並記錄 custodian 與存取限制 | V7；任何企業結果 |
| V1 | Construct Validity | **AI PILOT COMPLETE；HUMAN BLIND CODING PENDING** | 53B 協定（雜湊預先承諾）、54A/B 盲編封包、54C AI pilot（主機制 14/16、狀態 13/16；分歧 G04、G10、G11，皆 mapping-only）、60 分析器輸出 `V1_HUMAN_BLIND_CODING_PENDING`；EA-X：56 封包、61 分析器（`CONDITIONAL_CANDIDATE`） | 編碼簿可被一個模型家族一致使用；最具爭議的格是 G04、G10、G11；目前設計下分歧不改變方程 | 人類構念效度；研究者裁決的正確性；EA-X 的內容效度 | ≥ 2 位人類編碼者；主碼的 Krippendorff's α 至少 TENTATIVE（≥ .667，依 Krippendorff, 2004）且非 IMPRECISE（區間下界不低於 .667）；狀態的 α 至少 TENTATIVE；無未解的 model-structural 變更 → `V1_PASS_HUMAN_C6`（130 §3.9.3）；EA-X：≥ 3 位（規劃 6–8 位）人類評分者，I-CVI ≥ .78（Polit et al., 2007） | 「構念效度完成」的任何表述；G→M 對應的確定敘述；EA-X 作為門檻 |
| V2 | Cross-functional Pilot | **OPEN** | 無 | — | 錨點在不同功能脈絡下可理解、可區分 | 至少兩種功能脈絡試用：題卡理解、缺格、非單調、角色差異、填答負擔；EA-X 等級在兩輪 pilot 中可區分 | V7 的引出工具；EA-X 序位假設 |
| V3 | Schema & Units | **COMPLETE — SYNTHETIC ONLY** | 51 v2.2：T-SCH-5、T-SCH-6、T-SCH-7（型別、ω 防漏、NaN／inf 拒絕）；65 載入器 validate：58/58 參數鍵、0 錯誤 0 警告（空白骨架） | 型別與單位守恆在受測實例上成立；資料契約可執行 | 企業資料的單位正確（尚無資料） | 已達（合成） | — |
| V4 | Lookup Completeness | **COMPLETE — SYNTHETIC ONLY** | 51：T-ALG-1、T-MIS-6（40 個缺值變異：無靜默補零）、STATE（13 個狀態可達） | 缺格時拒算或回傳狀態碼，不靜默補零 | 企業查表的完整性（620 格全為 UNIDENTIFIED） | 已達（合成） | — |
| V5 | Portfolio Solver | **COMPLETE — SYNTHETIC ONLY** | 51／52：20 項必要檢查全部 PASS（含獨立手算 oracle 重推、DP == 窮舉、T-ORC-8 恆等式 NEV = VCP + VSC − DL） | 在受測合成實例上實作與方程一致；P1–P8 未被受測實例反駁 | 企業價值；最適企業架構；實證效度 | 已達（合成）；範圍只限 v2.2 求解器 | — |
| V6 | Invariance & Sensitivity | **COMPLETE — SYNTHETIC ONLY**（元素層級與 Model C 的分類只以涵蓋率報告） | 51：T-INV-4（標籤重排不變）、T-SEN-3／4／6／7／8（Lemma R 範圍、穩健可行、registry 雜湊、VOI、δ 非單調反例） | 不變性與敏感度程序在受測實例上正確 | 企業決策的穩健性（需事前登記的企業參數集合） | 已達（合成） | — |
| V7 | Enterprise Empirical Calibration | **OPEN** | 65 run：`NO_EVALUABLE_INITIATIVE_OR_POLICY`；求解次數 0；點決策 0；620 格全 `UNIDENTIFIED`（E 19、G 144、X 127、R 156、V 174） | 工程與資料契約已就緒（DATA NOT YET IDENTIFIED） | 任何企業的 VCP、VSC、DL、NEV、最適 portfolio、ROI、因果效果、外部效度 | 見 134 §8：閘門格識別 → 寬區間 → 事前登記並承諾雜湊 → 求解 → 實測 VOI → 第二批 → 停止規則 → 跨來源一致 | 第 4.10 節全部；第 5.6 節的企業結論 |

**V7 完成前不得宣稱**：企業 ROI、最適企業人工智慧架構、最佳導入部門、因果的績效改善、企業層級外部效度、可推廣至其他企業（130 §1.6、§3.14.4、§5.10）。

**模型失敗 vs 資料尚未識別**：V7 的現況是後者。模型失敗指方程、實作或資料契約有錯（V3–V6 任一檢查失敗、求解器與方程不一致、validate 出錯）；目前 V3–V6 在合成實例上全部通過、validate 0 錯誤，求解器拒絕產生點決策是缺值規則的預期行為。

---

## 2. 不在 V0–V7 內、但影響投稿的其他驗證線

| 驗證線 | 狀態 | 證據 | 範圍 |
|---|---|---|---|
| 文獻層統計穩健性（L1→L2） | 完成（凍結） | R14 表 4、7、9–11；r14/04 | 47 → 32（16／16） |
| 文獻層證據單元敏感度（L3） | 完成 | R14 表 6–8 | 29 持續、3 邊界敏感 |
| 文獻層人工稽核 | HUMAN_AUDIT_CONVERGED | R14 表 5；V9 | 50／20／19 |
| 文獻層人工標籤替換（L2′） | LOCAL_SENSITIVITY_CHANGED；V9 標籤 FULL_REANALYSIS_REQUIRED → 現行 FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET；FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED | V9 人工驗證套件（資料夾 20260929_V9_HUMAN_VALIDATION；V9 是檔案版本名，不是驗證閘門）之 `FINAL_STATUS.json`（2026-10-03）與 `ROBUST_CORE_LOCAL_SENSITIVITY.csv`（`e3166ee1…`）；V9 source package recovered and partially verified in V1.8（`02`、`04`） | 格數 32（15／17）；±1 成員（V1.8 逐列核對，`04` T1）；G01–G16 未移除 |
| 研究倫理與資料治理（企業層） | DRAFT（未取得授權、同意與機構判定） | 研究庫 27 草案；130 §3.14.7 | V0、V2、V7 資料蒐集的前提 |
| v2.4 使用率擴充（候選） | 合成檢查 16/16 PASS（SIMULATED_ONLY） | 74A／74B | 不在 V3–V6 範圍內 |
| 組織映射規則（候選） | 規則檢查 PASS（SIMULATED_ONLY）；ORG-V1–V5 PENDING | 85A／85B；107–117 | 不在 V3–V6 範圍內 |
| 工程／外部採購面（候選） | 15/15 驗收測試 PASS（SIMULATED_ONLY）；14 個 51 實例回溯一致 | 124／125／126 | 不在 V3–V6 範圍內 |
| 參考文獻鑑識 | 雙向對應無實質不符；2 項 PARTIAL | 135 | — |

---

## 3. 狀態字串一致性檢查（v1.7 全文）

| 字串 | 出現位置（130） |
|---|---|
| `OPEN`（V0、V2、V7） | 表 3-14；稿件狀態說明 |
| `AI PILOT COMPLETE；HUMAN BLIND CODING PENDING` | 表 3-14 V1 列（另保留程式狀態碼 `V1_AI_PILOT_COMPLETE`、`V1_HUMAN_BLIND_CODING_PENDING`） |
| `COMPLETE — SYNTHETIC ONLY`（V3–V6） | 表 3-14；表後說明；稿件狀態說明 |
| 「COMPLETE（僅合成）」舊寫法 | 0 處（已全部替換） |
| `THEORETICAL CONVERGENCE COMPLETE`／`HUMAN CONSTRUCT VALIDATION PENDING` | 3.9.2；4.6.1 欄位分組；4.7；摘要（中文：理論收斂完成；人類構念效度驗證待完成） |
