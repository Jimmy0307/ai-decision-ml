> **CURRENT COPY (V1.8.1, 2026-10-14) — current copy; history preserved.**
> Historical source: `W\01_ALL_OUTPUTS\AI_DECISION_THESIS_ALL_OUTPUTS\r14_merge_v1_7\137_NEXT_ACTIONS.md` (sha256 `94f15cb4da23b4fbf6556cc82c06eb94948eac72333697b82d6dc38b95b07f54`), left unchanged.
> Changed: only stale V9-availability / 2026-09-29 / 依作者回報 / full-reanalysis status spans (9 edits; line-by-line log in `claude/r14_merge_v1_8_1_study1_freeze/12_STALE_STATUS_CLEANUP_REPORT.md`, line numbers = historical file).
> Sentences describing the execution environment at that time are kept verbatim with the marker `〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：…〕`; current-status sentences are updated with citations.
> File names 02–10 refer to `claude/r14_merge_v1_8_source_closure/`; 11/12/15 refer to `claude/r14_merge_v1_8_1_study1_freeze/`.
> No number, G01–G16 content, taxonomy, G→M assignment, model, solver, schema or empirical result was changed. `SUBMISSION_READY = NO`.

# 137 — NEXT_ACTIONS（投稿關鍵路徑；v1.7）

日期：2026-10-14　｜　只列會阻擋投稿的事項；依優先序排列，格式排在實證之後。
目前：`SUBMISSION_READY = NO`。

---

| 序 | 優先 | 事項 | 為什麼阻擋 | 完成的定義（DoD） | 需要誰 | 依賴 | 稿件位置 |
|---|---|---|---|---|---|---|---|
| P0-1 | P0 | **[PARTIALLY DONE — V1.8]** **canonical source conflict：取得 V9 人工驗證原始檔案**（`20260929_V9_HUMAN_VALIDATION.zip`）＝**DONE**（已取得，zip sha256 `8f63e88e…`；於 V1.8 部分核對：`02_V9_AUTHORITY_MAP.md` V9_SOURCE_VERIFIED=PARTIAL），並確認 Drive 上沒有比 R14／V9 更新的版本＝**OPEN**（作者確認；`06_SOURCE_FLAG_CLOSURE.csv` 137 L10） | 稽核狀態旗標與標籤替換結果在本環境只有作者陳述；〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕摘要、3.7.4、4.5.5 等附錄 E39 所列各處依賴它 | 以原始檔案核對——V1.8 結果：✔ 替換清單（50 筆，`04` T4）；✔ 兩個變動配對；✔ 凍結核心其餘 31 組不變；✔ 無其他核心成員變動（另有 33/120 格計數或非核心方向差異）；✔ 15／17；✔ 無數值不一致，無須重寫數值；✔ v1.8 稿件移除 V9 旗標（`08_PATCH_LOG.md`）；✔ 132 於 V1.8.1 重新產生（`11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md`）。殘留：替換後矩陣的產生腳本與 sidecar 核心檔 NOT_RECOVERED（q 值未重算）；12/37 受保護輸入 NOT_RECOVERED | 作者（上傳檔案）；Claude（核對） | — | E39；128 CF-01、CF-08 |
| P0-2 | P0 | **canonical source conflict：「摘要／全文覆蓋不對稱」主張** | 作者要求寫入限制，但可取得證據（R14：全部候選證據來自 1,729 份全文）不支持；本輪依停止條件未寫入 | 作者提供可追溯的摘要／全文計數 → 以新主張寫入；或確認接受本輪以來源群組保留率（27.3% vs 14.9%）表述 | 作者 | — | E41；128 CF-02；130 §5.8.2 |
| P0-3 | P0 | **文獻層完整重分析的決策**（V9 標籤 FULL_REANALYSIS_REQUIRED；現行：FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET；FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED；E49 已於 V1.8 核定：標籤處理不重疊、記錄樣本 28/50 重疊） | 局部成員變動表示逐格結論對標籤敏感；投稿稿若宣稱 32 組，需先決定是否以一致標籤重跑 | 作者決定「投稿前重分析」或「投稿稿明載凍結基準＋局部敏感度」；V1.8 建議為後者（`07_FULL_REANALYSIS_DECISION_MEMO.md` §8），但仍屬研究者決定；若選擇重跑，須先通過 `07` §4 閘門（受保護輸入回復並雜湊比對），標籤輸入只能用 `04` T4，傳播規則須事前宣告（`15_REANALYSIS_INPUT_GOVERNANCE.md`）；若重分析改變 L2：依凍結程序重新產生 G 清單、重做 3.9 轉譯與 V1 封包 | 作者；重分析需 V5 pipeline | P0-1（V9 部分已完成） | E40；130 §3.7.4、§4.5.5、§5.8.9 |
| P0-4 | P0 | **human construct validation（V1）**：至少兩位人類盲編 G01–G16 → M1–M5／狀態；EA-X 人類 CVI | 構念效度目前只有研究者裁決與 AI pilot；不得宣稱完成 | `60` 輸出 `V1_PASS_HUMAN_C6` 或明確的未通過與回退（3.9.5）；`61` 輸出 EA-X 判定；結果回填 4.7.3–4.7.4 | 2 位以上人類編碼者、1 位非轉譯作者的裁決者 | P0-3（若 G 清單改變須先完成） | E6；133 V1；134 §7 |
| P0-5 | P0 | **enterprise source authority（V0）** | 沒有企業文件就沒有可行集合；任何企業陳述都只能是情境 | `S_sources` 登記完成；權限、共享資源、initiative 邊界、授權範圍經文件與角色交叉核對 | 焦點企業的財務、IT、法務／治理、流程負責人 | — | E43；134 §2 |
| P0-5a | P0 | **研究倫理、知情同意與資料治理** | 未取得公司授權、個別同意與機構審查／豁免判定前，不能啟動任何企業訪談或資料蒐集；投稿時也需要倫理聲明 | 公司授權書、資訊說明與同意表、資料保管計畫、去識別與小格數規則、利益關係揭露、機構審查或豁免判定皆完成（研究庫 27 草案 → 定稿） | 作者；所屬機構；焦點企業 | — | E50；130 §3.14.7；134 §10 |
| P0-6 | P0 | **enterprise parameter identification** | 620 格全為 `UNIDENTIFIED`；求解次數 0 | 第一批：閘門格（D1、現況存在性）＋高價值格寬區間；`65 --validate` 0 錯誤；`--run` 不再是 `NO_EVALUABLE_INITIATIVE_OR_POLICY` | 焦點企業各角色；研究者 | P0-5、P0-5a | E43；134 §1、§8 步驟 2–4 |
| P0-7 | P0 | **V7 empirical calibration** | 第 4.10 節全部待填；不得宣稱任何企業結果 | 事前登記並承諾雜湊 → `--run`／`--robust` → 實測 VOI → 第二批 → 停止規則 → 跨來源一致 → 回填 4.10 | 研究者；焦點企業 | P0-6；P0-4（Q8 需要 V1） | 134 §8；133 V7 |
| P1-1 | P1 | **targeted references** | Savage（1951）歸屬與 McFarlan（1981）卷期頁仍為 PARTIAL | 取得 JASA 原文與 HBR 館藏紀錄後更新或維持 PARTIAL；不得補造 | 作者（館藏存取） | — | E3、E45；135 |
| P1-2 | P1 | **cross-functional pilot（V2）** | 引出工具與 EA-X 等級的可區分性未檢驗 | 至少兩種功能脈絡試用並記錄題卡理解、缺格、非單調、角色差異、負擔 | 焦點企業兩個功能單位 | P0-5 | 133 V2 |
| P1-3 | P1 | **ORG-V1–V5**（若組織導入層保留在投稿範圍內） | 組織編碼與映射未經人類驗證 | 依 107 協定完成並回填表 4-32F | 人類編碼者 | — | E20 |
| P1-4 | P1 | **final manuscript convergence** | 3.7.4 程序細節、3.14.3 格數、題目、表 4-32F 位置等作者決定 | E42、E47、E48 結案；P0 各項結果回填後重跑本輪的禁止主張搜尋與數值稽核 | 作者；Claude | P0-1–P0-7 | 129 §2 |
| P2-1 | P2 | **submission formatting** | 格式檔案不在環境中（V1.8 仍為 OPEN_SOURCE_NOT_FOUND，`06_SOURCE_FLAG_CLOSURE.csv` 137 L22）；投稿稿範圍未決 | 作者決定投稿範圍（136 §1）；取得三份格式檔案；依 136 §4 核對；由 canonical 稿產生投稿稿 | 作者；Claude | P1-4 | E11、E46；136 |

---

## 不在關鍵路徑上（不阻擋投稿，可平行或之後）

- 工程／外部採購面（候選）的企業資料與 A-ENG、C-ENG-LOCAL 的定義（E38）。
- v2.4 使用率擴充與 v2.5 組織層樣板是否採用（E15、E24）。
- M5 縱向擴充（G11、G12）。
- 配對機制稽核（穩健不足 vs 穩健過度的決策編排描述差異；5.9）。

## 立即可做、不需要外部資料的一步

P0-1 只需要作者把 `20260929_V9_HUMAN_VALIDATION.zip`（以及若有更新的 R14／Drive 版本）放進這個工作階段；核對與重寫可在同一輪完成。〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕 現況：V9 部分已於 V1.8 完成；P0-1 只剩 Drive 對帳（作者確認）。不需要外部資料的下一步：依 `15_REANALYSIS_INPUT_GOVERNANCE.md` 事前宣告 UNCERTAIN／AMBIGUOUS／UNMAPPED 的傳播規則（P0-3 的前置條件；不執行重分析）。
