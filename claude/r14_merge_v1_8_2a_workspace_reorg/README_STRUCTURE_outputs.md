# outputs 資料夾架構（2026-10-14 整理）

| 資料夾 | 內容 | 規則 |
|---|---|---|
| `00_CURRENT\` | 現行版本 | 新的工作版本放這裡 |
| `00_CURRENT\01_MASTER_THESIS\` | 最新合併稿件（v1.8.2）.md／.docx | .md 是正文的權威來源；.docx 由 .md 產生 |
| `00_CURRENT\02_STUDY1_FREEZE\` | V1.8.1 Study 1 證據凍結；`repo\` 是 GitHub `Jimmy0307/ai-decision-ml` 的本機工作副本 | 不要手動搬動 `repo\` 裡的檔案，否則 git 會把它們視為已刪除 |
| `00_CURRENT\03_V1_HUMAN_VALIDATION\` | V1 人類構念效度：寄給編碼者的封包與 V1.8.2 正式文件 | S1 已凍結：封包寄出後不可修改內容 |
| `00_CURRENT\04_CURRENT_STATUS\` | 目前狀態檔、Drive 索引，以及 `_reorg_20261014\`（本次整理的搬移紀錄與還原腳本） | — |
| `10_CANONICAL_EVIDENCE\` | 權威證據：V1.8 輸入包、V9 人工驗證、V5 方法、R14／Study 1 source closure、V5 正式產出凍結（`04_V5_PRODUCTION_FREEZE\`） | 唯讀，不修改 |
| `20_SEALED_PRIVATE\` | 研究團隊專用的封存檔（V1.8.2 題號對照表、順序紀錄、亂數種子） | 不給編碼者，不上傳 GitHub，S3 之前不開啟；請另做私人備份 |
| `80_HISTORY_2026\` | 依月份歸檔的歷次 run（`08_AUG`、`09_SEP`、`10_OCT`），以及原本散在根目錄的舊稿 docx | 歷史紀錄，只新增不修改 |
| `99_LEGACY\` | 早期的結構洞研究（2,003 篇；含 5 月的 TASK2B／TASK3 檔案） | 不得併入現行結果 |

根目錄 `C:\NTUST_PAPER\` 只保留 pipeline 執行需要的檔案：主程式、13 個 `run*.bat`、它們呼叫的腳本與 `.sql`、`AGENTS.md`。舊的工具腳本移到 `ARCHIVE\`，pipeline 說明文件移到 `docs\pipeline_2026-04\`。

本次整理只做搬移，沒有刪除任何檔案。

- 搬移紀錄：`00_CURRENT\04_CURRENT_STATUS\_reorg_20261014\MOVE_MANIFEST_20261014.csv`，共 71 項，全數驗證通過。
- 全部還原：執行 `python -I ROLLBACK_20261014.py`（同一資料夾）。
