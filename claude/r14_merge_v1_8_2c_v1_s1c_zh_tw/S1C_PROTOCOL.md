# S1C — V1 編碼工具：小幅語意忠實度修補與最終發送前凍結（取代 S1b）

**僅供研究團隊。** 狀態：已建置、已稽核、已凍結，待研究者目視審閱（`S1C_RESEARCHER_VISUAL_REVIEW.md`）。**未發送；未蒐集任何人類資料；未產生模擬作答；未 commit／push。**

## 0. 版本關係

| 項目 | 值 |
|---|---|
| S1B_STATUS | SUPERSEDED_BEFORE_DISTRIBUTION |
| REASON | MINOR_SEMANTIC_FIDELITY_PATCH_BEFORE_ANY_HUMAN_CODING |
| NO_HUMAN_DATA_COLLECTED_UNDER_S1B | YES |
| S1b 資料夾 | `claude/r14_merge_v1_8_2b_v1_s1b_zh_tw/`，唯讀、未修改；其凍結清單 `FREEZE_MANIFEST_V1_S1B.txt`（SHA-256 `ba491cbd…815e`）於收尾時重新驗證 |
| S1 資料夾 | `claude/r14_merge_v1_8_2_v1_prefreeze/`，唯讀；21/21 於收尾時重新驗證 |
| 語意權威 | `claude/r14_merge_v1_8_2_v1_prefreeze/26_V1_FINAL_CODEBOOK_v1_8_2.md`。S1c 只翻譯與澄清，不改構念、分析邏輯、類別歸屬邏輯、Q1→Q2 一致性或信度計畫 |

## 1. S1c 改了什麼（且只改這些）

由 `tools/s1b_to_s1c_diff_gate.py` 逐格證明（`S1C_PATCH_DIFF.md`，DIFF GATE＝PASS，0 項不允許差異）：

1. M1–M4 的「定義」與「區分說明」儲存格：改為 coordinator 指定的中文（逐字），使其忠實於 26 §3 英文定義；M4 文字不含「風險」。
2. 「僅屬證據層」的定義儲存格（逐字）；三條 Q1 規則不變。
3. 作答聲明表頭：原句「選擇「不符合」會被記錄並另行分析，你的作答仍會被使用。」換成指定句（逐字）；前面的「請如實回答」由分號改為句號。
4. 作答聲明第 1 條（逐字）。
5. 「判斷對象」規則儲存格（**標記**）：S1b 沒有指定的提醒句原文，因此以指定句「功能類型名稱與機制類別有相同或相近字詞時，不得只因字詞相同就選擇該類別。」取代 S1b 的近義句「相同字詞不是選擇該類別的理由。」，並從例詞中移除「風險」（M4 修補後已沒有任何類別文字含「風險」，保留會誤導）。
6. 中繼資料：文件建立／修改時間戳記；總表檔名 `20_MASTER_PACKET_S1C_ZH_TW.xlsx`。編碼者檔案內**不放版本標籤**（版本字串屬禁止內容）。

**未改：** 16 題與 ITEM-A01…A16、每題的家族名稱與定義、文獻樣態句、每位編碼者的題目順序（沿用 S1b 種子，建置時驗證與 S1b 活頁簿逐一相同）、Q1–Q5 文字、Q1/Q2 一致性規則、判斷順序、跨時間學習與適應／資料條件限制／無適用機制／無法明確判定的文字、下拉標籤、工作表名稱、格式、資料驗證、標籤對照、分析器、分析計畫 29、所有密封承諾、題目編號 ↔ G 對照、研究者答案鍵。

## 2. 檔案

| 檔案 | 角色 |
|---|---|
| `coder_distribution/CODER_1_ZH_TW.xlsx`…`CODER_3_ZH_TW.xlsx` | 發給編碼者（各一份） |
| `20_MASTER_PACKET_S1C_ZH_TW.xlsx` | 研究團隊總表（無 G 編號） |
| `S1C_CODEBOOK.md` | 編碼手冊修補內容與忠實度檢查 |
| `S1C_PATCH_DIFF.md` | S1b → S1c 逐格差異 |
| `S1C_RESEARCHER_VISUAL_REVIEW.md` | 依編碼者看到的順序逐格列出（含位址、下拉選項、驗證訊息、文件屬性） |
| `S1C_CODER_FACING_PREVIEW.md` | 與 S1b 相同格式的可讀預覽 |
| `S1C_PACKET_MANIFEST.csv`、`S1C_ITEM_CONTENT_CORRESPONDENCE.csv` | 雜湊、種子、工作表；S1 英文 ↔ S1b ↔ S1c 逐題內容雜湊 |
| `S1C_BLINDING_AUDIT.md`、`S1C_ANALYZER_COMPATIBILITY_TEST.md`、`S1C_DISTRIBUTION_README.md`、`S1C_FINAL_STATUS.md` | 稽核、相容性、發送、最終狀態 |
| `tools/` | S1c 建置程式、差異關卡、洩漏稽核、測試、審閱稿產生器；**原樣沿用**的 `v1_construct_analyzer_s1b.py`、`s1b_label_map.json`／`.py`（與 S1b 位元組相同） |
| `V1_SEALED/FREEZE_MANIFEST_V1_S1C.txt` | 最後產生的凍結清單 |

順序紀錄：沿用 S1b 的承諾（`claude/r14_merge_v1_8_2b_v1_s1b_zh_tw/V1_SEALED/S1B_ITEM_ORDER_LOG.COMMITMENT.md`，明文 SHA-256 `a866e074…cbb0e`）；S1c 未產生新的順序紀錄，也未開啟任何順序紀錄或種子檔。

## 3. 分析、階段、資料治理

全部不變，見 `claude/r14_merge_v1_8_2b_v1_s1b_zh_tw/S1B_PROTOCOL.md` §6–§8 與分析計畫 29。S1c 凍結取代 S1b 凍結作為發送基準；S2／S3 清單建議命名 `FREEZE_MANIFEST_V1_S1C_S2.txt`／`_S3.txt`。分析器原樣沿用，因此結果檔名仍為 `V1_RESULTS_S1B.*`（標示用，不影響計算）。
