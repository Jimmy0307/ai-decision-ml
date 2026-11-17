# AI × Decision｜現有資料交接與地端待回收清單（2026-11-17）

> 這份文件同步的是**版本邊界與回收條件**，不是本機研究重跑的完成證明。既有 GitHub 網頁與 V9 frozen artifacts 不重寫；不影響 LEM2／DRSA。

## 版本身分（不能合併）

| 線別 | 實際工作 | 完成／可驗證程度 |
|---|---|---|
| V11.1 | OpenAlex author/co-author external cross-team validation, author alias checks, peers and alternate ties; **0 confirmed Burt broker** | 完成摘要已提供；**原始本機 CSV/log 尚未接入**；非 Limitation 全量重掃 |
| V9 Full Reanalysis | 對 V5/V9 語料、人工編碼、10×12 功能矩陣做全量品質修正 | `FULL_REANALYSIS_REQUIRED`，目前不等於完成 |
| Gap Validity V1 | 二分 Burt constraint 分解、alternative-path / backbone sensitivity / synthetic demonstrations | 14/14 程式測試 PASS；不是作者網路經驗驗證 |
| Limitation Scout V0.1 | 原始全文擷取工具＋25,112 選取證據段落的初步詞彙掃描 | 100 個文件 ID／142 次命中，8/8 工具測試 PASS；不是「已找到 100 個研究缺口」 |
| Limitation Followup V1 | 擷取論文限制、追查後續研究是否解決、反證審核 | 待本機全量執行與取得原始輸出，**尚無 resolved/partial/gap verdict** |

## 已在雲端／已整理的材料

- [研究網頁](index.html)、[本週完整稽核](RESEARCH_AUDIT_20261117.md)、[老師摘要](SUPERVISOR_BRIEF_20261118.md)、[90 項指標來源表](data/ALL_METRICS_WITH_PROVENANCE_20261117.csv) 已提交公開 `Jimmy0307/ai-decision-ml`。
- 近期結構洞研究私有 repo `Jimmy0307/ai-decision-ml-private-backup-20261018` 分支 `research/structural-hole-discovery-v2-20261113` 有網站快照與摘要資料。
- 11/17 本次現存的主資料包：`20260929_V9_HUMAN_VALIDATION.zip`、`完整資料來源.zip`、`AI_DECISION_GAP_VALIDITY_V1_COMPLETE.zip`、`AI_DECISION_LIMITATION_SCOUT_V0_1_READY.zip`、`AI_DECISION_MASTER_AUDIT_20261117_COMPLETE.zip`、`AI_DECISION_WEEKLY_BRIEF_20261118.zip`。
- 上述 ZIP 已於本次交接驗證可讀；合併封包與 SHA256 清單保存在 ChatGPT 此次交付附件，**尚未上傳到 GitHub 或 Drive**。
- Google Drive 有歷史 V8/V9 與結構洞文件，但 11/17 最新總包在前次搜尋未找到；不得宣稱與 GitHub 全同步。

## 地端回收清單（請唯讀掃描，保留原路徑、執行日誌及雜湊）

1. **P0 V11.1 raw**：final verdict、95 次 OpenAlex 原始查核紀錄、author ID alias、coauthor graph edges、peer baseline、執行程式與 run manifest。
2. **P0 V5 original fulltexts**：`C:\NTUST_PAPER\LocalCorpusWorkbench\v5_production_app\data\workbench.sqlite`（唯讀）及原始 PDF/TXT/HTML、DOI 映射、parser 狀態、SHA256。
3. **P0 V9 full reanalysis**：修正後的逐筆 family coding、人工審查/裁決、120-cell 凍結前後差異、統計 rerun 及完整 manifests。
4. **P1 V6–V10.1 raw runs**：citation / higher-order / broker candidate CSV、零模型配置、時間窗、種子、外部否證與執行 log。
5. **P1 Limitation Followup V1**（若已運行）：`CORPUS_INVENTORY.csv`、`LIMITATION_CLAIMS.csv`、`LIMITATION_CLUSTERS.csv`、`FOLLOWUP_EVIDENCE.csv`、`FINAL_GAP_VERDICTS.csv`、`RUN_MANIFEST.json`；未執行則記 `NOT_EXECUTED`。
6. **P1 citation/author linkage**：DOI↔OpenAlex ID、引用 edges、作者身份及時間欄位；保留來源標籤，勿用 metadata 覆蓋全文標籤。

## 驗收不變條件

- V9 frozen 16 depleted 指**功能低整合**，不可寫成 16 個 Burt holes。
- V11.1 3 rejected + 1 insufficient、0 confirmed 為**已回報、尚待原包查核**；Dwivedi 裁決文字與程式不一致需保留。
- Limitation 關鍵字初篩未建立任何已證實「後人沒有處理」的研究缺口。
- LEM2/DRSA、現行論文封版、原始 ZIP/DB、Git history 一律不覆蓋；資料補回採 additive immutable sidecar。
