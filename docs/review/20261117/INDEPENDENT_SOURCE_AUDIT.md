# AI × Decision｜獨立來源稽核報告（V5–V11.1、90 項指標、20 項方法、12 篇文獻、8 組公式）

**審查日期：2026-11-18（台北）｜審查者：Claude Code（獨立方法學審稿＋研究文件工程）**
**基礎版本：`Jimmy0307/ai-decision-ml` `main` @ `cba0f3cf26148f990a9694bc71baabd1bd112268`（審查開始時以 `git ls-remote` 與 GitHub API 確認未前進）**

> 本報告只陳述可由來源支持的內容。原始研究 ZIP、全文與私有資料**未**上傳本 public repo；本報告引用的是 ZIP 名稱、成員路徑與 SHA-256。缺少的地端資料一律標 `PENDING_LOCAL_RECOVERY`，未等待、也未推測 11/19 之後的地端重掃結果。

## 0. 結論摘要

1. **90 項已發布數值沒有任何一項數值錯誤。** 55 項 DIRECT 中 49 項由原始檔獨立重算一致、6 項在兩份原始文件中互證；2 項 SYNTHETIC 以解析式驗證；33 項（16 HISTORICAL＋17 USER_REPORTED）無原始資料可重算，標 `PENDING_LOCAL_RECOVERY`。見 [`METRIC_AUDIT_90.csv`](METRIC_AUDIT_90.csv)。
2. **發現並更正的是定義、單位、版本標籤、證據等級、文獻與公式問題**（56 項已套用，見 [`CORRECTION_LOG.csv`](CORRECTION_LOG.csv)）。最重要的五項：
   - 2,180 是「文獻層級功能配對邊」（120 格計數總和），不是「document pairs」或篇數。
   - 人審 sidecar 的「32 核心一進一出」：進入者為 depleted、退出者為 enriched，故 sidecar 組成為 **15 enriched / 17 depleted**；凍結基準 16/16 未改動。
   - 120 格中另有 **16 個零觀測格**，與 16 個 depleted 核心格（觀測 2–26 次）**無交集**，不可混用兩個「16」。
   - Limitation Scout 的 25,112 段來自 6,499 筆嚴格紀錄、1,104 篇**嚴格分析文獻**，不是 1,729 篇全文、也不是完整 limitation 章節。
   - Gould–Fernandez 公式（E5）漏列開放二步路徑條件 `¬(s→t)`；Burt constraint（E2）未定義 `p_ij` 的雙向權重與 `p_qj` 分母；betweenness（E4）未指明無序配對與標準化。
3. **未決（不改寫）**：V11.1（user-reported, raw local-only）、V9 全量重分析（pending）、V6–V10.1 原始 run log、Limitation 全文追蹤。Dwivedi 的凍結文字／程式裁決衝突保留。

## 1. 來源盤點與完整性

| 檢查 | 結果 |
|---|---|
| 審查包 `checks/LIGHT_MANIFEST.json` 40 個檔案 SHA-256 | 40/40 一致 |
| 審查包 `checks/verify_bundle.py` | PASS（7 必要檔、12 文獻、20 方法、13 版本、repo 身分） |
| 6 個來源 ZIP 的整檔 SHA-256 | 6/6 與 `SOURCE_ARCHIVE_MANIFEST.csv` 一致（見首頁 #provenance 表） |
| ZIP 成員（以 Python 分批解壓，不進模型 context） | V9 920、Gap 25、Scout 9、Weekly 7、2026-04 封存 69 → **1,030 檔**；另 master audit ZIP 自身 32 檔 |
| 與 11/17 稽核索引 `ALL_ARCHIVE_MEMBERS_SHA256.csv` 比對 | 1,030/1,030 SHA-256 一致；索引外的 32 檔即 master audit ZIP 自身成員（索引不可能包含自己） |
| 「1,309」「75」 | 是 ZIP entries（含目錄 389／6 個），不是檔案數；首頁 KPI 已改標「來源 ZIP 檔案成員（非論文數）」 |
| ZIP 成員時間戳 | V9 Human／V9.1 ≤ 2026-10-04（歷史）；Gap Validity、Limitation Scout 2026-11-16；master audit、週報 2026-11-17（本週） |

## 2. 統計稽核：研究漏斗與 V9 凍結基準

工具：[`tools/review_20261117/audit_recompute.py`](../../../tools/review_20261117/audit_recompute.py)（標準函式庫；原始 ZIP 路徑以參數傳入）→ [`RECOMPUTE_RESULTS.json`](RECOMPUTE_RESULTS.json)。

| 數值 | 定義（正確單位） | 獨立驗證來源 | 結果 |
|---|---:|---|---|
| 2,118 | 來源**文件**（1,199 AI 來源群組＋919 Decision 來源群組） | V9 稿候選 `.docx` §3.3＋`V9_FINAL_FORENSIC_AUDIT.md` | 兩文件一致；原始檔清單 PENDING |
| 1,729／388／1 | 可用全文／未進入分析／解析失敗 | 同上；2,118 = 1,729＋388＋1 | 一致 |
| 26,501 | 候選語意**紀錄**（非論文數） | `ANALYTICAL_FREEZE_MANIFEST_V2.json` `production_records` | 重算一致 |
| 6,499 | 嚴格紀錄，來自 **1,104** 篇文獻 | 同上 `strict_records`, `strict_unique_documents` | 一致；6,499 = 3,125＋2,501＋873 |
| 8,751 | 已映射端點 = 2×3,125＋2,501 | 同上 | 一致 |
| 3,125 | 兩端皆映射的紀錄 | 同上 | 一致 |
| 783 | 可配對文獻 | `DOCUMENT_DEDUP_MATRIX_MANIFEST.json` | 一致 |
| 2,180 | **文獻層級功能配對邊**（同篇同配對合併） | 120 格 `official_observed` 總和 | 一致；名稱已更正 |
| 10×12＝120；104 | 可能配對格；有觀測格（另 16 格零觀測） | `ROBUST_CORE_LOCAL_SENSITIVITY.csv` | 一致 |
| 47 | 主零模型 q≤.05：22 enriched＋25 depleted（q≤.01：34＝15＋19） | 同上 | 一致 |
| 46／32／54 | 精確檢定／文獻內結構保持／未去重 q≤.05 | 同上 | 一致 |
| 32＝16＋16 | 四重穩健核心；以 q 值與方向**重新推導**升級規則 | 同上 | 一致；規則與旗標 120/120 相符 |
| 10,000／5,000 | 主零模型重抽（seed 20260918）／文獻內 MCMC 保留狀態（seed 20260919） | `BASELINE_REPRODUCTION_VERIFICATION.md`＋V9 稿 | 一致（模擬數，非論文數） |

**不得把 26,501 當論文數**：它是候選片段紀錄；論文層級分母依階段為 2,118 → 1,729 → 1,104 → 783。

## 3. V9 人工驗證（50 targeted／20 blind）

| 欄位 | n | 一致 | Cohen κ（重算） | 已發布 |
|---|---:|---:|---:|---:|
| C1 Evidence validity | 20 | 15 | 0.5614 | 0.561 |
| C2 Relation type | 20 | 7 | 0.1798 | 0.180 |
| C3 AI family | 20 | 4 | **0.0476** | 0.048 |
| C4 Decision family | 20 | 4 | **0.1398** | 0.140 |
| C5 Inclusion | 20 | 12 | 0.3162 | 0.316 |

- 20 筆 blind 全部屬於 50 筆 first-coder 子集（不可相加）；第一編碼者 1 人、盲審者另 1 人。20 筆中 **19 筆**至少一欄不一致，皆有 reconciliation event ID。
- 局部 sidecar（20 筆用調和後標籤、30 筆用第一編碼者標籤，其餘不動）：主矩陣 **24/120** 格計數改變、**3/120** 方向改變；嚴格可配對紀錄 3,125→3,107、文獻 783→781、邊 2,180→2,181。
- 核心 32→32，但 **gained `HUMAN_AUGMENTATION × RISK_ASSESSMENT`（depleted）／lost `COORDINATION_EXECUTION × GENERAL_DECISION_PROCESS`（enriched）** → sidecar 組成 15/17。
- **凍結基準未改寫為 corrected full reanalysis**：原始稽核裁決 `FULL_REANALYSIS_REQUIRES_RESEARCHER_APPROVAL`，本審查維持 `V9 full reanalysis pending`。

## 4. 13 個版本的證據等級與裁決

| 版本 | 證據等級 | 本審查可核到的範圍 | 裁決 |
|---|---|---|---|
| V5（功能語料；V9 凍結分析） | DIRECT | 漏斗、120 格、32 核心全部重算 | 數值確認；定義已更正 |
| V6 citation | HISTORICAL | 僅週報摘要 | PENDING_LOCAL_RECOVERY |
| V7 author early | HISTORICAL | 僅週報摘要 | PENDING_LOCAL_RECOVERY |
| V8 citation enrichment | HISTORICAL | 僅週報摘要 | PENDING_LOCAL_RECOVERY |
| V9 citation line | HISTORICAL | 3,983＋3,897＝7,880（算術） | 與 V9 功能線同名，已加註 |
| V9.1 | DIRECT（功能線）＋HISTORICAL（引用校準） | S1/S2 核心 31/31、保留 29/30、depleted 保留 14/15 重算一致 | 列內兩條研究線已分開標示 |
| V9 Human | DIRECT | κ、24/120、一進一出重算一致 | FULL_REANALYSIS_REQUIRED |
| V10 | HISTORICAL | 僅摘要 | PENDING_LOCAL_RECOVERY |
| V10.1 | HISTORICAL | 僅摘要（6 否決／2 未決） | PENDING_LOCAL_RECOVERY；指標表 `V101` 已改 `V10.1` |
| V11 | USER_REPORTED | 僅完成摘要 | raw local-only |
| V11.1 | USER_REPORTED | 79＋15＋1＝95、3＋1＝4（算術） | 0 confirmed / 3 rejected / 1 insufficient 無法獨立重現；Dwivedi 文字／程式衝突保留 |
| Gap Validity V1 | DIRECT（sidecar）＋SYNTHETIC | 14/14 測試重跑 PASS；results.json 欄位語意一致 | 方法診斷，非新樣本確認 |
| Limitation Scout V0.1 | DIRECT（初篩） | 25,112／1,104／100／142 重算；8/8 測試重跑 PASS | Limitation candidate scan only |

**V11.1 ≠ Limitation 全量重跑**：V11.1 是作者／合作網路的 OpenAlex 外部身分與同儕驗證；Limitation 全文重掃是獨立路線，尚未完成。

## 5. 20 項方法

| ID | 方法 | 本審查驗證 |
|---|---|---|
| M01 | Corpus extraction | 2,118／1,729／388／1 兩份原始文件一致；原始全文清單 PENDING |
| M02 | LLM 語意編碼與嚴格納入 | 26,501→6,499→3,125 機器輸出一致；人審 κ 低 → 重分析 |
| M03 | 文獻層級去重 | 2,180＝120 格總和；名稱更正 |
| M04 | 固定度數二分零模型 | 47（22/25）重算一致 |
| M05 | 精確超幾何 | 46 重算一致（已補入 CSV） |
| M06 | 文獻內結構保持零模型 | 32 重算一致；5,000 為 MCMC 保留狀態 |
| M07 | 未去重原始紀錄敏感度 | 54 重算一致（已補入 CSV）；核心規則重推導一致 |
| M08–M10 | Citation SNA／探索確認／FPR-Power | HISTORICAL；版本名稱加註 citation line |
| M11 | S1/S2 分段 | 重算一致 |
| M12 | 雙人編碼 | κ 重算一致 |
| M13、M15 | 作者同儕／OpenAlex | USER_REPORTED；95 次呼叫算術一致 |
| M14 | 高階網路 | HISTORICAL |
| M16–M18 | constraint 分解／替代路徑／骨架 | 測試重跑 PASS；E6 代數成立 |
| M19 | 合成反例 | SYNTHETIC；K3,3＝1/3、三角柱＝41/81 解析驗證 |
| M20 | Limitation 初篩 | 重算一致 |

## 6. 文獻與公式

- 12 篇以 Crossref API 與 doi.org 解析逐筆核對（2026-11-18）：8 VERIFIED、4 VERIFIED_WITH_CORRECTION、0 UNVERIFIED_SOURCE（書目層級）。見 [`BIBLIOGRAPHY_VERIFICATION.csv`](BIBLIOGRAPHY_VERIFICATION.csv)。
  - R04 Burt 1992：Harvard University Press，DOI `10.4159/9780674029095`（JSTOR 為平台）。
  - R07 Opsahl：2013 刊期（35(2):159–167），2011 線上優先，故 DOI 含 2011，非錯誤。
  - R10：作者為 Laurence Saglietto、Cécile Cézanne、Delphine David（審查包佇列 CSV 誤為 Caroline／Danièle；repo 原只用姓氏）。
  - R11：四位作者 Zádor、Zhu、Smith、Gorgoni。
  - R12 Johnson & Sasson：Strategy Science 線上優先 2026-03-10，卷期未定；**是對 constraint 測量內涵的研究，不是否證結構洞理論**。
- 四種構念不得混淆：功能低整合（V9 16 depleted）／Freeman 路徑仲介／Gould–Fernandez 角色／Burt ego 非冗餘。「移除節點後圖仍連通」或「有替代路徑」單獨不能判定沒有 Burt 結構洞。
- 原文全文未取得者（Burt 1992/2004、Freeman 1977、Gould & Fernandez 1989、Everett & Borgatti 2020、Newman 2001、Granovetter 1973）之公式，以標準教科書／igraph／networkx／R `sna` 文件核對並標示。見 [`FORMULA_VALIDITY_NOTES.md`](FORMULA_VALIDITY_NOTES.md)。

## 7. Limitation 線

- `selected spans 25,112`／`document IDs 1,104`／`flagged docs 100`／`lexical hits 142` 重算一致；142 列狀態全部為 `LEXICAL_HIT_IN_SELECTED_SPAN_NOT_FULLTEXT`。
- **不是 142 個 verified limitations**，也沒有任何 confirmed research gap：缺作者原文全文＋頁碼＋後續解決論文證據。
- 未虛構 11/19 以後才可能完成的重掃結果。

## 8. 網站更新（增量）

- 以 clone 得到的 `docs/index.html`、`THEORY_LITERATURE_COMPARISON_20261117.{html,md}` 為基礎修改；**未**以審查包 `03_SITE_REVIEW_BASELINE` 的舊 HTML 覆寫。原有 11 個區塊、搜尋功能、90／20／13／32 列表格全部保留。
- 新增：證據狀態標示、11/18 更正表、12 篇理論＋8 公式表、本週／歷史時間界線、三條網路研究線表、假說→反證→停止門檻、來源與證據等級導航（含 ZIP SHA-256）。
- GitHub Pages：API 顯示 `has_pages=false`；網頁以 repo 檔案形式提供，未宣稱已部署。

## 9. 重現指令

```text
python -I tools/review_20261117/audit_recompute.py --v9-dir <extract>/20260929_V9_HUMAN_VALIDATION \
    --gap-dir <extract>/AI_DECISION_GAP_VALIDITY_V1 --scout-dir <extract>/AI_DECISION_LIMITATION_SCOUT_V0_1 \
    --out docs/review/20261117/RECOMPUTE_RESULTS.json
python -I tools/review_20261117/build_metric_audit.py --repo .
python -I tools/review_20261117/qa_site.py --repo . --base origin/main
python -I -m unittest discover -s tools/review_20261117 -p "test_*.py"
```

命令輸出見 [`QA_AND_TEST_LOG.md`](QA_AND_TEST_LOG.md)；資料界線見 [`PROVENANCE_LIMITS.md`](PROVENANCE_LIMITS.md)。
