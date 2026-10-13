> **CURRENT COPY (V1.8.1, 2026-10-14) — current copy; history preserved.**
> Historical source: `W\01_ALL_OUTPUTS\AI_DECISION_THESIS_ALL_OUTPUTS\r14_merge_v1_7\128_CANONICAL_STATE.md` (sha256 `4d807997232858c6930c78f8cc8b1c2738bc0f7a16ebd89528e497aa99d7a698`), left unchanged.
> Changed: only stale V9-availability / 2026-09-29 / 依作者回報 / full-reanalysis status spans (23 edits; line-by-line log in `claude/r14_merge_v1_8_1_study1_freeze/12_STALE_STATUS_CLEANUP_REPORT.md`, line numbers = historical file).
> Sentences describing the execution environment at that time are kept verbatim with the marker `〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：…〕`; current-status sentences are updated with citations.
> File names 02–10 refer to `claude/r14_merge_v1_8_source_closure/`; 11/12/15 refer to `claude/r14_merge_v1_8_1_study1_freeze/`.
> No number, G01–G16 content, taxonomy, G→M assignment, model, solver, schema or empirical result was changed. `SUBMISSION_READY = NO`.

# 128 — CANONICAL_STATE（v1.7 收斂輪）

建立日期：2026-10-14　｜　範圍：千篇論文研究／AI × Decision Making／Enterprise AI Multilevel Decision System
本文件只盤點與裁定「哪一份是權威」，不修改任何既有 artifact。所有雜湊值為 SHA-256 前 16 碼，於本輪重新計算。

---

## 0. 本輪可取得與不可取得的來源

使用者列出的優先來源中，以下 **不在本工作環境中**（uploads 目錄為空，全檔系統搜尋無結果）：〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕

| 來源 | 狀態 | 影響 |
|---|---|---|
| `20260929_V9_HUMAN_VALIDATION.zip` | **RECOVERED；V9_SOURCE_VERIFIED=PARTIAL（V1.8）**（v1.7 時記為 ABSENT） | 人工標籤替換的局部敏感度結果（+人機增能 × 風險評估；−協調與執行 × 一般決策流程）與 `HUMAN_AUDIT_CONVERGED / LOCAL_SENSITIVITY_CHANGED / FULL_REANALYSIS_REQUIRED` 狀態，在本環境中**唯一來源是使用者 2026-10-13 的指示文字**。〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕κ 值、50/20/19 筆數可由 R14 定稿獨立核對（相符）。現況：V9 source package recovered and partially verified in V1.8——zip sha256 `8f63e88e…`；替換結果與狀態旗標已由 `ROBUST_CORE_LOCAL_SENSITIVITY.csv`（`e3166ee1…`）與 `FINAL_STATUS.json`（`d9226d31…`，verified_at 2026-10-03T12:23:44Z）逐列核對（`02_V9_AUTHORITY_MAP.md`、`04_LOCAL_SENSITIVITY_REPRODUCTION.md`）；12/37 受保護輸入仍未尋回。完整重分析現行狀態：FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET；FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED（`07_FULL_REANALYSIS_DECISION_MEMO.md` §8）。 |
| `完整資料來源.zip` | **PRESENT IN V1.8 INPUTS（sha256 `138dbeac…`）— LEGACY_HISTORICAL_PROVENANCE**（v1.7 時記為 ABSENT） | `LEGACY_HISTORICAL_PROVENANCE — STRUCTURAL-HOLE / CITATION-NETWORK STUDY PACKAGE (NOT THE V5 DATA PACK); REAL_V5_DATA_PACK=NOT_RECOVERED`（`05_LEGACY_SOURCE_BOUNDARY.md` §1、§3.4，sha256 `03205f44…`；v1.7 誤稱為「V5 Manuscript Data Pack 本體」）；本輪以 R14 定稿 + `04_G01_G16_FROZEN.csv` + 專案指示所列 V5 數字交叉核對（全部一致，見 §3）。 |
| `投稿格式.pdf`、`投稿範例.pdf`、`全文投稿樣板 windows (2).docx` | **ABSENT**（V1.8 仍為 OPEN_SOURCE_NOT_FOUND：`06_SOURCE_FLAG_CLOSURE.csv` 128 L16） | 格式差距只能以既有投稿稿（R14 定稿、V5 camera-ready）推論，見 136。 |
| Google Drive 版本 | **無法存取**（本工作階段無 Drive 連接器；V1.8 仍未核對：`06_SOURCE_FLAG_CLOSURE.csv` 137 L10 OPEN_SOURCE_NOT_FOUND） | 無法判定 Drive 與本地是否有未解決差異；最後一次已知的 Drive 對帳是 repo commit `e3c373e`（v2.2 稿件）。 |

可取得且已核對的來源：`/home/claude/r14/`（R14 合併套件，含 MANIFEST）、`/home/claude/ai-decision-ml/`（branch `calibration/v1.1-variable-model`，HEAD `ce3e1b2`，工作樹乾淨）、`/home/claude/v24/out*`（66–127 合併稿與支援文件）、專案文件 `V5_CONFERENCE_FINAL_CAMERA_READY_DECISION_ORCHESTRATION_20260921.docx`。

---

## 1. 權威來源一覽

| # | 項目 | 權威來源（版本／雜湊） | 狀態 | 依據 |
|---|---|---|---|---|
| 1 | **Authoritative manuscript** | 文獻層正文：`r14/01_R14_AI_DECISION_FINAL_SUBMISSION_CANONICAL.docx`（f4252f765c4294fe…；抽取版 02 = 52b13fce39ef88e0…）。整合論文：`127_…v1_6_MATH_CANONICAL_CANDIDATE.md`（96f7e725d619b078…）為上一輪最新候選；本輪產出 **`130_…v1_7_EVIDENCE_CONVERGED_CANDIDATE.md`** 取代其為現行候選。 | CANDIDATE（非定稿） | r14/00 權威順序第 1 位；66→73→82→100→105→118→127 為逐輪修訂鏈，皆未覆寫 |
| 2 | **Authoritative corpus/network result** | R14 定稿 §3–§4（表 1–11）＋ `r14/04_G01_G16_FROZEN.csv`（ace53a780434c309…）。數字與專案指示所列 V5 Data Pack 數字逐項一致。 | FROZEN | r14/00 第 1–2 位；專案指示 SOURCE PRIORITY |
| 3 | **Authoritative human-validation result** | (a) 文獻語意證據的人工稽核：R14 §3.7.1、§4.6.1、表 5（50 筆研究者目標稽核、20 筆盲式第二編碼、19 筆分歧調和；調和前 κ = .561／.180／.048／.140／.316）。(b) 人工標籤替換局部敏感度與稽核狀態：V9 套件（資料夾 `20260929_V9_HUMAN_VALIDATION`；`FINAL_STATUS.json` 驗證時間 2026-10-03T12:23:44Z）——**V9 source package recovered and partially verified in V1.8**（`02_V9_AUTHORITY_MAP.md` §7 權威檔案集；`04_LOCAL_SENSITIVITY_REPRODUCTION.md`）。(c) 企業 G→M 構念的人類 V1：`v1_human_results/TABLES_4_1.md` = `V1_HUMAN_BLIND_CODING_PENDING`。 | (a) VERIFIED vs R14；(b) **V9_SOURCE_VERIFIED=PARTIAL（V1.8；50/20/19、κ、局部敏感度成員由原始列重現）**；(c) PENDING | R14 02:218, 361, 365–375；使用者指示 §4–5；V1.8 `02`／`03`／`04` |
| 4 | **Authoritative mathematical model** | `r14/06_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md`（0249e7b980f060e9…；與 repo `42_…v2_2.md` 同雜湊）。候選擴充：`74` v2.4（使用率 α）、`89` v2.5 變數字典、`119` canonical 數學 v1.0（四層面＋工程／外部採購層，6aa95b8a13f020c1…）——**皆為 CANDIDATE，未取代 06**。 | v2.2 FROZEN；其餘 CANDIDATE | r14/00 第 5 位 |
| 5 | **Authoritative solver** | `ai-decision-ml/51_enterprise_portfolio_solver_v2_2.py`（37f26a529ff2f42a…，與 52 記錄的執行時雜湊一致）；執行紀錄 `52_SOLVER_ORACLE_RUN_v2_2.txt`：20 個必要檢查全部 PASS（含獨立手算 oracle 重推），verdict = PASS（SIMULATED_ONLY）。工程層參考實作 `124`（63e53ececc8da062…）＋ `125` 執行紀錄：15/15 驗收測試 PASS（SIMULATED_ONLY；CANDIDATE）。 | v2.2 COMPLETE—SYNTHETIC ONLY | 52:6, 30；51:2743–2748 |
| 6 | **Authoritative empirical schema** | `62_ENTERPRISE_EMPIRICAL_DATA_TEMPLATE_v2_3`（xlsx ad6d74c02fc43ca1…，與 r14/09 同雜湊）＋ 載入器 `65_enterprise_data_loader_v2_3.py`（601650413dcf0d7f…）。本輪於隔離副本重跑：58/58 樣板參數鍵；validate 0 errors、0 warnings；620 格全為 `UNIDENTIFIED`（E 19、G 144、X 127、R 156、V 174）；run = `NO_EVALUABLE_INITIATIVE_OR_POLICY`；runs = 0（求解次數 0、點決策 0）。v2.4（80）、v2.5（90）樣板為 CANDIDATE，載入器不讀取。 | ENGINEERING READY；DATA NOT YET IDENTIFIED | 本輪重跑（隔離副本；repo 未改動） |
| 7 | **Unresolved references** | 見 135。Savage（1951）歸屬 PARTIAL；McFarlan（1981）卷期頁 PARTIAL；Krippendorff 門檻出處已以 2004 HCR 原文（作者 postprint）核對；Landis & Koch（1977）、Lynn（1986）正文未使用。引文 ↔ 參考文獻雙向對應：實質不符 0。 | PARTIAL（2 項） | 135 |
| 8 | **Unresolved empirical fields** | v2.3 全部 620 格；v2.4 使用層 19 格（候選）；組織導入層欄位（候選）；工程層全部參數（候選）；人類 V1、EA-X 內容效度、ORG-V1–V5 結果。 | ALL UNIDENTIFIED／PENDING | 134 |
| 9 | **Historical provenance only** | 見 §4。 | — | — |
| 10 | **Must NOT override newer canonical evidence** | 見 §5。 | — | — |

---

## 2. 衝突清單（不得靜默調和）

| ID | CONFLICT | SOURCE A | SOURCE B | WHICH ONE APPEARS NEWER | WHY | ACTION REQUIRED |
|---|---|---|---|---|---|---|
| CF-01 | 人工稽核後的穩健核心成員 | R14 定稿：32 格（16 過度／16 不足）為主要統計結果；人工調和標籤「不傳播至未稽核記錄」，未報告標籤替換重算 | 使用者指示（V9，2026-09-29）：目標式人工標籤替換後核心仍為 32 格，但 +人機增能 × 風險評估（不足）、−協調與執行 × 一般決策流程（過度）；`FULL_REANALYSIS_REQUIRED`〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕 | B 較新（V9 `FINAL_STATUS.json` 2026-10-03 > R14 docx 09-20；v1.7 原記 09-29） | B 是新增的敏感度層，不推翻 A 的凍結推論基準；但 B 的原始 artifact 不在環境中〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕 | v1.7 以「凍結核心＝官方推論基準；替換結果＝局部敏感度」並列報告，所有 B 的數字加 `[SOURCE: V9 human-validation state, 2026-09-29 — artifact not in workspace; verify before submission]`。〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕**V9 套件已取得並於 V1.8 逐列核對**：32 = 15／17、+1／−1、其餘 31 組不變、G01–G16 未移除（`04_LOCAL_SENSITIVITY_REPRODUCTION.md` T1–T3）；v1.8 稿件已將 V9 出處旗標改為來源引用（`06_SOURCE_FLAG_CLOSURE_NOTES.md` §3；`08_PATCH_LOG.md`）；137 P0-1 = PARTIALLY DONE。 |
| CF-02 | 「摘要／全文覆蓋不對稱」限制 | 使用者指示 §3、§18：AI 側與 Decision 側證據的全文／摘要覆蓋不同，須寫入限制 | 127 附錄 E1（v1.1 已退役）：R14 定稿明載候選證據由 1,729 份可解析全文建立，無證據支持「AI 側多為摘要層級」；可支持的是來源群組保留率差異（AI 5,620/20,621 = 27.3%；Decision 879/5,880 = 14.9%） | A 較新（指示），B 有 R14 證據 | **evidence 不足以支持 claim**（停止條件）。A 的主張在本環境找不到可追溯計數 | **不寫入「摘要／全文不對稱」**。改以 R14 可支持的「來源群組選擇性流失不對稱」表述同一個推論邊界（方向可作研究線索，幅度不可作效果量）。若作者持有可追溯的摘要／全文計數，須以新主張重新提出（137 P0-2）。 |
| CF-03 | 文獻層定稿版本 | 專案文件 `V5_CONFERENCE_FINAL_CAMERA_READY_…_20260921.docx` | `r14/01_R14_…CANONICAL.docx`（docx 中繼資料修改時間 2026-09-20） | **B（內容較新）**，雖然檔案時間戳較早 | V5 camera-ready 寫「400 筆／120 筆人工驗證尚未完成」；R14 已含 50／20／19 稽核與證據單元重切分。時間戳不可靠，以內容判定 | V5 camera-ready 降為歷史出處；不得用其覆寫 R14。其中未被 R14 取代或改變的正式執行設定紀錄（第 3.13 節：Q4_K_M、num_ctx 8192、temperature 0、seed 20260909 等）可作為 130 §3.8.3 的出處，並註明 Data Pack 原檔待核（V1.8：REAL_V5_DATA_PACK=NOT_RECOVERED；`完整資料來源.zip` 不是 Data Pack，見 `05_LEGACY_SOURCE_BOUNDARY.md` §3.4；同一模型摘要值另見 V9.1 `SEGMENT_STAGE2_MODEL_VERIFICATION.json`，`06_SOURCE_FLAG_CLOSURE.csv` 128 L46）。 |
| CF-04 | 論文題目 | 127：「從文獻功能低整合到企業人工智慧多層級決策：……」 | 使用者指示 §8 研究主題：「企業人工智慧導入作為多層級決策系統：治理、能力配置、組織採用與價值實現」 | B 較新 | B 被表述為「完整研究主題」，未明說取代題目；且 B 未涵蓋文獻層（Study 1） | v1.7 保留 127 題目，於 §1.3 寫入 B 為整體研究主題；**題目更換屬作者決定**（137 P1）。 |
| CF-05 | Study 2 核心研究問題措辭 | 127 第 59–61 行（v2.3 措辭：企業選哪些 initiatives） | 使用者指示 §8：企業層如何配置能力、政策與資源 envelope，以在共享資源、治理限制、組織反應、不確定性與事業單位自主下極大化可實現價值 | B 較新 | B 與 06 v2.2 的 leader 決策變數（y、γ、e）一致，A 較窄；不是改研究問題，而是精確化 | v1.7 改用 B 措辭（與 06 一致，屬安全修改）。 |
| CF-06 | 數學模型版本 | 06 v2.2（權威） | 119 v1.0 canonical（候選）、74 v2.4（候選）；127 §3.12.7 未標 CANDIDATE | 119 較新 | 119 未經人工審查凍結；r14/00 規定 06 為數學權威 | v1.7 於 §3.12.7 標示 CANDIDATE，並註明 V5 gate 的 COMPLETE 只涵蓋 51 v2.2。 |
| CF-07 | 實證樣板版本 | v2.3（62/09；載入器 65 讀取） | v2.4（80）、v2.5（90）候選樣板 | 候選較新 | 載入器只讀 v2.3；候選樣板未被採用 | 維持 v2.3 為權威；候選區塊（Y、O）只列為候選。 |
| CF-08 | Drive 與本地 | 本地 r14 套件與 repo | Google Drive（不可存取） | 未知 | 無連接器 | 記為 `DRIVE_STATE_UNKNOWN`；作者確認 Drive 上無比 R14／V9 更新的版本（137 P0-1 併辦）。 |
| CF-09 | r14/03 vs repo 44 v2.3 | r14/03（8671eefa…） | repo 44 v2.3（99137414…） | — | 只差一行指向（v2_2 vs v2_1）與檔尾換行；r14 版正確 | 無須行動；兩者皆已被 66–130 合併稿取代。 |
| CF-11 | 兩種文獻層敏感度的處理範圍 | 使用者指示：標籤替換與證據單元重切分是不同的局部敏感度 | R14 02:258：重切分設定中「人工調和標籤不傳播至未稽核記錄」→ 受稽核記錄可能已用人工標籤 | 不適用（缺 2026-09-29 原始紀錄）〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕 | 若受稽核記錄在重切分中已用人工標籤，兩種敏感度的處理範圍部分重疊，「互相獨立」的說法不成立 | v1.7 改寫為「不同的測量操作；範圍可能部分重疊，待核」（E49）；V1.8 已核（`04_LOCAL_SENSITIVITY_REPRODUCTION.md` §3b）：標籤處理不重疊（V9.1 重切分未傳播任何人工標籤），記錄樣本部分重疊（50 筆受稽核記錄中 28 筆亦被重切分；其中 11 筆因人工錯誤標記被強制納入候選） |
| CF-10 | 127 §3.14.3 用詞 | 「交付方式 6 格」 | v1.2 已以 `hosting_boundary × workflow_delivery` 取代 `delivery_mode` | B | 舊術語殘留 | v1.7 改術語；6 格是否仍成立列作者確認。 |

---

## 3. 停止條件逐項檢查

| 停止條件 | 結果 | 證據 |
|---|---|---|
| network counts 不一致 | **未觸發** | 127 中的 lineage 與推論關鍵數字（26,501／6,499／12,998／4,079／8,919／4,672／3,862／164／221／3,125／2,501／873／3,374／51.9157%／1,104／783／2,180／945／47／34／46／32／54）數值與 R14 及專案指示的 V5 數字一致；第 4 章 32 格 O、E、O/E 與 G01–G16 的 q 值逐格核對一致（delta_C）；r14/04 與 repo 11 的 G 表 0 值差異。 |
| official robust core 不一致 | **未觸發** | R14 表 9–10 與 r14/04、repo 11 一致；16 不足呈現依序即 G01–G16。 |
| human audit artifact 不一致 | **未觸發**（v1.7 時 artifact 缺件；V1.8 已取得並核對） | κ、50／20／19 與 R14 一致；替換結果只見於使用者指示（CF-01）。〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕 V1.8：50/20/19 與 κ 由原始列重現（`03_HUMAN_AUDIT_REPRODUCTION.md`；無 HUMAN_RELIABILITY_CONFLICT），替換結果由 `ROBUST_CORE_LOCAL_SENSITIVITY.csv` 逐列重現（`04`）。 |
| model equation 與 solver implementation 不一致 | **未觸發** | 06 §11.1、51:768–773、119 §、124:991–1002 的 VRA／DL0／VCP／VSC／DL／NEV 定義相同；51 T-ORC-8 驗證恆等式。 |
| VCP／VSC／DL／NEV 定義衝突 | **未觸發** | VCP = F^{A+} − F^A；VSC = F^B − F^{A+}；DL = F^B − F^C；NEV = F^C − F^A = VCP + VSC − DL；VCP = VRA + DL0。工程層 ENDOGENOUS 制度下 VCP^{ENG}、NEV^{ENG} 為 NOT_COMPARABLE（不是衝突，是有意的不定義）。 |
| current manuscript authority 不明 | **未觸發** | 見 §1-1。 |
| empirical schema authority 不明 | **未觸發** | 見 §1-6。 |
| Drive vs local unresolved diff | **無法判定** | CF-08。 |
| reference primary source 無法驗證 | **部分觸發（2 項）** | Savage（1951）歸屬、McFarlan（1981）卷期頁 → 依規則標 PARTIAL，不刪除也不補造。 |
| evidence 不足以支持 claim | **觸發（1 項）** | CF-02「摘要／全文不對稱」→ 不寫入，改用可支持的表述。 |

結論：沒有觸發必須整輪停止的核心衝突（計數、核心、方程、比較量定義皆一致）。觸發的兩項（CF-01 缺件、CF-02 證據不足）已以「不猜、加出處旗標、改寫為可支持表述」處理，並列入 OPEN BLOCKERS。〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕

---

## 4. 只作歷史出處（historical provenance only）

- 404 篇論文／2,425 筆嚴格記錄／GPT-5.6 Sol 語意編碼的早期 lineage（不得作 G01–G16 分母；127 與 v1.7 全文 0 次出現）。
- V4 稿件（`MANUSCRIPT_SUBMISSION_V4(2).docx`）與 V4 結構洞層（不得恢復）。
- `V5_CONFERENCE_FINAL_CAMERA_READY_DECISION_ORCHESTRATION_20260921.docx`（CF-03）。
- 400 筆 `HUMAN_VALIDATION_400` 與 AI 預編碼（AI_PRECODE_CLAUDE）——不得當人類標註。
- `handoff/`（v2.0／v2.1 交接包）、`44_…v2_1/v2_2/v2_3` 企業稿、`42_…v2_1`、`46/47` v2.1 求解器。
- 合併稿 66、73、82、100、105、118、127（逐輪 checkpoint；127 為上一輪候選）。
- main branch v1.0（合成迴歸出處，非現行模型）。
- r14/13 V5 lineage reconciliation（只在需要解釋 lineage 時引用）。

## 5. 不得覆寫較新 canonical 證據的檔案

| 檔案 | 不得覆寫的對象 |
|---|---|
| 任何 V4／V5 camera-ready 稿 | R14 定稿的稽核、敏感度與結果分層 |
| 41／r14/05 的 G→M 研究者裁決 | 不得被寫成人類構念效度；不得被 AI pilot 覆寫 |
| 54C AI 盲編 pilot | 不得當人類 V1 |
| 52／125 合成執行紀錄 | 不得當企業實證結果 |
| 74、80、89、90、119、124 候選 | 不得取代 06 v2.2、51、62 v2.3 的權威地位 |
| 使用者指示中無 artifact 支撐的主張（CF-02） | 不得覆寫 127 E1 的退役判定 |
| 任何 R14 O／E／q 值 | 不得成為企業模型權重、係數、先驗或門檻 |

## 6. 本輪 repo 狀態

`/home/claude/ai-decision-ml`：branch `calibration/v1.1-variable-model`，HEAD `ce3e1b2`，ahead of origin by 1（前一輪既有），工作樹乾淨；本輪未修改、未 commit、未 push。所有驗證重跑皆在 scratchpad 隔離副本中進行。
