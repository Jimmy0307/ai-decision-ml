# S1B — V1 人類構念效度編碼：繁體中文版工具協定（S1b，取代 S1，發送前）

**僅供研究團隊。不寄給編碼者。**

**狀態：** 已建置、已稽核、待研究者目視審閱。**尚未發送；未蒐集任何人類資料；未產生任何模擬作答。** 本協定只更換編碼工具（語言、措辭、選項標籤、題目順序），分析計畫不變。

## 0. 與 S1 的關係

| 項目 | 值 |
|---|---|
| OLD_S1 | SUPERSEDED_BEFORE_DISTRIBUTION |
| NO_HUMAN_DATA_COLLECTED_UNDER_OLD_S1 | YES（沒有任何編碼者收到 S1 檔案，見 65 §A–C） |
| S1 檔案 | `claude/r14_merge_v1_8_2_v1_prefreeze/` 全部保持不變（唯讀）；S1 manifest 21/21 雜湊於建置前與收尾時各重新驗證一次 |
| 研究者決定 | 見 `S1B_RESEARCHER_DECISION_RECORD.md` |
| 取代範圍 | S1 的編碼者檔案、協定 25、編碼手冊 26 §1–4、發送說明 30，在 S1b 中分別由本目錄的對應檔案取代。S1 檔案保留作為歷史紀錄，**不得再發送**。 |

## 1. 目的與有限主張（不變）

與 25 §1 相同：V1 問的是三位獨立的人類編碼者，對 16 個文獻配對各自代表哪一種企業決策機制（若有）是否一致。主要問題是**編碼者間信度**，不是與研究者答案鍵的一致性。V1 只驗證 G → 企業機制的詮釋，不驗證核心格集合、分類架構或網絡統計。

## 2. 檔案

| 檔案 | 角色 | 誰會看到 |
|---|---|---|
| `coder_distribution/CODER_1_ZH_TW.xlsx`、`CODER_2_ZH_TW.xlsx`、`CODER_3_ZH_TW.xlsx` | 每位編碼者一份：填答說明、類別定義、題目資訊、自己的作答表、作答聲明 | **編碼者**（各自一份） |
| `20_MASTER_PACKET_S1B_ZH_TW.xlsx` | 研究團隊總表：三張作答表、題目資訊（依中性編號排序）、空白裁決表、`STUDY_TEAM_CODE_MAP`（中文標籤 → 標準代碼；中文家族名 → 標準家族代碼）。無 G 編號 | 研究團隊 |
| `S1B_CODEBOOK.md` | 編碼手冊、S1 英文 → S1b 中文對照、語意變更紀錄 | 研究團隊 |
| `S1B_RESEARCHER_DECISION_RECORD.md` | 研究者決定紀錄（S1b） | 研究團隊 |
| `S1B_DISTRIBUTION_README.md` | 發送與回收說明 | 研究協調人 |
| `S1B_PACKET_MANIFEST.csv` | 四個 xlsx 的 SHA-256、位元組、編碼者、順序種子、工作表清單 | 研究團隊 |
| `S1B_ITEM_CONTENT_CORRESPONDENCE.csv` | 每個題目編號：S1 英文內容雜湊 ↔ S1b 中文內容雜湊 | 研究團隊 |
| `S1B_BLINDING_AUDIT.md`、`S1B_ANALYZER_COMPATIBILITY_TEST.md`、`S1B_FINAL_STATUS.md` | 稽核、相容性測試、最終狀態 | 研究團隊 |
| `S1B_CODER_FACING_PREVIEW.md` | `CODER_1_ZH_TW.xlsx` 的逐格可讀版，供研究者目視審閱 | 研究團隊 |
| `V1_SEALED/S1B_ITEM_ORDER_LOG.COMMITMENT.md`、`V1_SEALED/FREEZE_MANIFEST_V1_S1B.txt` | 順序紀錄雜湊承諾；S1b 凍結清單（最後產生） | 研究團隊 |
| `tools/` | 建置、標籤對照、分析器、測試、洩漏稽核、預覽產生器與其結果 | 研究團隊 |
| 研究團隊私有資料夾 `outputs\20_SEALED_PRIVATE\V1_8_2B_S1B_STUDY_TEAM_ONLY\` | `S1B_ITEM_ORDER_LOG.json`（三份順序與種子；不在 git） | 研究團隊 |

**沿用、不變：**
- 分析計畫：`claude/r14_merge_v1_8_2_v1_prefreeze/29_V1_ANALYSIS_PLAN_FROZEN.md`，SHA-256 `4278bdfd…a05d`（全值見凍結清單）。
- 密封的題目編號 ↔ G 編號對照：承諾檔 `claude/r14_merge_v1_8_2_v1_prefreeze/V1_SEALED/ITEM_ID_TO_GID_MAP.COMMITMENT.md`，對照檔 SHA-256 `2a84d5de58ec3d13878281d684d82b959d8bc73be7068845bd4cd2f2448cbe81`。S1b 未開啟此對照檔。
- 研究者答案鍵承諾：`claude/r14_merge_v1_8_2_v1_prefreeze/V1_SEALED/RESEARCHER_ASSIGNMENT_COMMITMENT.md`（不變）。

## 3. 工具

- **題目：** 16 題，題目編號 ITEM-A01…ITEM-A16，**每個編號對應的題目內容與 S1 完全相同**（同一組 AI 功能類型 × 決策功能類型及其定義）。證明：`S1B_ITEM_CONTENT_CORRESPONDENCE.csv` 逐題列出 S1 英文內容的 SHA-256 與 S1b 中文內容的 SHA-256；建置程式從 S1 總表 `ITEM_INFO` 讀取每題英文內容，與三份 S1 編碼者檔逐題比對，再以逐字對應的翻譯表轉成中文（翻譯表以英文定義全文為鍵，定義不符即中止）；洩漏稽核再逐題比對四個 S1b 活頁簿與該 CSV 的中文雜湊。因此 S1 的密封對照在 S1b 下仍然有效、無需變更。
- **語言：** 編碼者看到的全部文字為繁體中文。允許的拉丁字元只有：M1–M4、Q1–Q5、AI、題目編號 ITEM-Axx，以及聲明第 6 條中的 AI 工具名稱（ChatGPT、Claude、Gemini、Copilot）。由稽核腳本強制檢查。
- **問題 Q1–Q5、類別、一致性規則、判斷順序、作答聲明：** 見 `S1B_CODEBOOK.md` §2–§5。
- **文獻樣態說明：** 每題相同、非技術性：「在本研究分析的文獻中，這兩類功能被一起討論的情形比依整體分布所預期的少。這只是研究線索，不代表這種組合不可能、無效、不重要，或在實務中不存在。」S1 `ITEM_INFO` 的「robust depletion」欄已整欄移除。
- **題目順序：** 每位編碼者一份新的、可重現的順序，種子公開記錄於 `S1B_PACKET_MANIFEST.csv`（`S1B_ZH_TW_20261014_CODER_k_ORDER`；規則 `random.Random(seed).shuffle(ITEM-A01..A16)`）。三份順序彼此不同、不等於編號順序、也不等於任何一份 S1 順序。順序本身只寫在研究團隊私有資料夾，OUT 只有雜湊承諾。種子不需保密：順序只涉及中性編號，且編碼者檔案本身就顯示順序。
- **預計作答時間：** 「約 60–120 分鐘，視閱讀速度而異。」

## 4. 角色與遮蔽（不變，措辭更新）

角色同 25 §4。遮蔽：中性題目編號、各自順序、直接寄送（不經任何雲端試算表或公開儲存空間）、7 項作答聲明（符合／不符合）。任何一項「不符合」→ `CODER_STATUS=EXPOSED`，分開報告，絕不默默合併。公開儲存庫的限制（28 §1）仍然成立：熟讀儲存庫的人仍可由功能類型配對反推題目；本工具不再在檔案中提到任何程式碼庫或線上資料位置，以免引導搜尋。

## 5. 洩漏、遮蔽與結構稽核

`tools/leakage_check_s1b.py`（延伸自 `leakage_check_v182.py`）必須回報 **0 項發現**。內容見 `S1B_BLINDING_AUDIT.md`；結果檔 `tools/leakage_check_result_s1b.json`。

## 6. 階段與凍結

與 25 §7 相同，僅名稱更新：

| 階段 | 動作 | 關卡 |
|---|---|---|
| **S1b** | 凍結工具、協定、編碼手冊、分析計畫引用、分析器、標籤對照、測試、洩漏腳本與結果、順序承諾 | `V1_SEALED/FREEZE_MANIFEST_V1_S1B.txt`（最後產生） |
| 發送 | 寄出三份 `CODER_k_ZH_TW.xlsx` | 寄出檔案的 SHA-256 必須等於 S1b 凍結值 |
| **S2** | 凍結三份回收檔 | `FREEZE_MANIFEST_V1_S1B_S2.txt`（分析器 `--s2-manifest`） |
| **R** | 只以中性編號計算信度 | 分析器 |
| **A / S3** | 裁決並凍結裁決檔 | `FREEZE_MANIFEST_V1_S1B_S3.txt`（`--s3-manifest`） |
| S / K / C | 敏感度、解封答案鍵、53B §11 分類 | 僅在 S3 之後；題目對照與答案鍵仍以 **S1 的承諾雜湊**驗證（分析器未改動此邏輯） |

## 7. 分析

不變：`29_V1_ANALYSIS_PLAN_FROZEN.md`。主要統計 = Q2 的 Krippendorff α（名目，16 題，3 位編碼者，bootstrap 5,000 次，種子 20261011）；次要 = 兩兩 Cohen κ；門檻 .800 / .667 標記為 RESEARCH_CONVENTION。實作：`tools/v1_construct_analyzer_s1b.py`，只更換輸入解析（`S1B_ANALYZER_COMPATIBILITY_TEST.md`）。29 中凡提到「S1-frozen `CODER_k.xlsx`」者，在 S1b 下讀作「S1b 凍結的 `CODER_k_ZH_TW.xlsx`」。

**已核准的語意變更對分析的影響：** 「無法明確判定」現在也涵蓋「證據不足」（`S1B_CODEBOOK.md` C-10）。標準代碼仍為 `AMBIGUOUS`；統計方法不變；AMBIGUOUS 比率照 29 §2 以描述統計報告，解讀時須註明 S1b 的定義已合併「證據不足」。

## 8. 資料治理（不變）

回收檔只存放在本機受控空間，**不得推送到公開儲存庫**，也不得上傳到任何雲端試算表。只公開去識別的彙總結果，且須經研究者審閱。任何編碼者一旦收到 S1b 檔案，任何內容變更都會使 S1b 失效。
