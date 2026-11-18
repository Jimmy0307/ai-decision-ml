# PROVENANCE_LIMITS｜證據等級、資料界線與待補證據（2026-11-18）

## 1. 證據等級（90 項指標正規化）

| 等級 | 定義 | 項數 | 本審查處理 |
|---|---|---:|---|
| DIRECT | 審查包內原始研究 ZIP 可直接讀到的機器輸出或原始文件 | 55 | 49 項由原始檔獨立重算一致；6 項（2,118／1,729／388／1／10,000／5,000）在兩份原始文件中互證 |
| HISTORICAL | V6–V10.1 歷史執行摘要；原始 run log／manifest 未取得 | 16 | 僅能做算術一致性檢查；`PENDING_LOCAL_RECOVERY` |
| USER_REPORTED | V11–V11.1 使用者提供之完成摘要；原始包只在地端 | 17 | 不可獨立重現；`PENDING_LOCAL_RECOVERY` |
| SYNTHETIC | 合成圖示範（K3,3、三角柱） | 2 | 解析式驗證；不得當成真實 SNA 實證 |
| PENDING | 尚未完成的研究工作（非數值） | — | V9 全量重分析、Limitation 全文追蹤 |

## 2. PENDING_LOCAL_RECOVERY 清單（需地端原始資料才能完成）

| 優先 | 資料 | 需要的檔案 | 影響 |
|---|---|---|---|
| P0 | V11.1 作者合作外部驗證原始包 | 00–03 報告、final verdict CSV、95 次 OpenAlex call log、author alias map、coauthor edges、scripts、seeds、run manifest、SHA-256 | V11_001–V11_017 只能維持 USER_REPORTED；Dwivedi 文字／程式裁決衝突無法裁定 |
| P0 | V5 原始全文與 `workbench.sqlite` | PDF／TXT／HTML 清單、DOI／UUID 對照、parser 狀態、SHA-256、授權 | 2,118／1,729／388／1 只能以文件互證，無法逐檔重建 |
| P1 | V9 全量重分析輸出 | 全語料重新映射、測試、delta 稽核、凍結版本身分 | 凍結 32 核心不得改寫；sidecar 15/17 不採用 |
| P1 | V6–V10.1 canonical run bundles | scripts、candidate CSV、raw networks、calibration、seeds、logs | 16 項 HISTORICAL 指標無法重算 |
| P1 | Limitation 全文重掃與後續解決稽核 | CORPUS_INVENTORY、LIMITATION_CLAIMS（原文＋頁碼＋DOI）、FOLLOWUP_EVIDENCE、FINAL_GAP_VERDICTS、run log | 只能稱 `Limitation candidate scan only` |
| P1 | Citation edges 與作者 ID canonical links | DOI↔OpenAlex IDs、refs／citations、alias、時間 | Burt 最後一輪 gate 無法執行 |

## 3. 本審查**沒有**做的事

- 沒有重跑 V11.1、沒有呼叫 OpenAlex、沒有重跑 V6–V10.1、沒有全量重掃 V9 或 Limitation。
- 沒有修改任何凍結研究結果（V9 32 核心、人審原始答案、v1.0 數學封版）。
- 沒有把原始全文、研究 ZIP、人工編碼的證據原文、作者資料、金鑰或本機路徑放進 public repo；只放聚合計數與 SHA-256。
- 沒有寫入 `Jimmy0307/LEM2`、`Jimmy0307/drsa-research`、獵頭研究 hub 或任何其他 repo；沒有操作 Google Drive；沒有變更任何 GitHub Pages 設定。
- 私有備份 repo 的指定 branch 只做唯讀核對（HEAD `a18927d` 與交接文件一致）；其中未找到 V6–V11.1 的原始 run 檔，未複製任何私有內容到本 repo。

## 4. 文獻原文取得界線

- 書目欄位（作者、年份、標題、期刊、DOI）以 Crossref API＋doi.org 解析核對。
- 全文讀取：Zádor et al. 2022（PLOS 全文）、Opsahl（作者預印本）、Jasny & Lubell（作者最終草稿）。
- 僅摘要：Johnson & Sasson 2026、Saglietto et al. 2020。
- 未取得（`UNVERIFIED_SOURCE_TEXT`，出版社頁面阻擋或付費牆）：Burt 1992、Burt 2004、Freeman 1977、Gould & Fernandez 1989、Everett & Borgatti 2020、Newman 2001、Granovetter 1973。相關公式以標準教科書形式與 igraph／networkx／R `sna` 文件核對，頁碼級記號待原書核對。

## 5. 部署狀態

2026-11-18 GitHub API：`Jimmy0307/ai-decision-ml` `has_pages=false`。網頁以 GitHub 檔案形式存在；未宣稱公開網站已部署。

## 6. 第二輪同步規則

11/19 之後若取得地端 raw，另開有版本的增量 PR：先比對 SHA-256 與本報告的 `RECOMPUTE_RESULTS.json`，再更新 HISTORICAL／USER_REPORTED 指標的等級；不得覆寫本次紀錄。
