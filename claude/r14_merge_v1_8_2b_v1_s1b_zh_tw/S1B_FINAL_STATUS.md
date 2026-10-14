# S1B — 最終狀態（2026-10-14）

**範圍：** V1 編碼工具繁體中文版（S1b），研究者已核准設計。**未發送、未分享、未寄出任何檔案；未蒐集任何人類資料；未產生任何模擬作答；未 commit／push。**

## 1. 產出

| 檔案 | SHA-256 | 位元組 |
|---|---|---|
| `coder_distribution/CODER_1_ZH_TW.xlsx` | `f700e7a50d4cb33171cb154ae0e364cbb77f82bf36c1570a0515410c3ef518eb` | 19,467 |
| `coder_distribution/CODER_2_ZH_TW.xlsx` | `90c02624ffadd4f752b978970740e8e92143f84886790ee092e4cf0588705227` | 19,496 |
| `coder_distribution/CODER_3_ZH_TW.xlsx` | `d83c05e725f20345d16a07f73d2e2be1e788aff123eb75577f396668794fd321` | 19,494 |
| `20_MASTER_PACKET_S1B_ZH_TW.xlsx`（研究團隊） | `d80f5a2d7e46822acf248ad721288aa2ba99c06bc90c7216bf4c97c9e58d5f1b` | 31,672 |
| `tools/s1b_label_map.json` | `86c5bb33c158a23ef8368c9ec95640256a4e119673e13685c9373d003eea3e8d` | |
| `tools/v1_construct_analyzer_s1b.py` | `315c4f744e11cd736b330519f868ed7c6a98a40b9745793c00dfd40d1d4d5a8d` | |
| 研究團隊私有：`S1B_ITEM_ORDER_LOG.json` | `a866e074429bc896c7175e5eab53e34457857943033e1adeb84b4aa6366cbb0e` | 1,366 |

其餘檔案的雜湊見 `V1_SEALED/FREEZE_MANIFEST_V1_S1B.txt`（最後產生）。

## 2. 檢查結果

| 檢查 | 結果 |
|---|---|
| 題目內容逐題對應 S1（同編號＝同題） | PASS（`S1B_ITEM_CONTENT_CORRESPONDENCE.csv`；建置與稽核兩次比對） |
| 密封的題目編號 ↔ G 對照 | 不變、未開啟；承諾 `2a84d5de58ec3d13878281d684d82b959d8bc73be7068845bd4cd2f2448cbe81` |
| 三份新順序 | 彼此不同、不同於編號順序、不同於任何 S1 順序 |
| 洩漏＋遮蔽＋結構稽核 | PASS，0 項發現（`S1B_BLINDING_AUDIT.md`） |
| 標籤對照測試 | PASS（134 個下拉選項、173 個變體） |
| 分析器相容性 (a)(b)(c)(d) | PASS（`S1B_ANALYZER_COMPATIBILITY_TEST.md`）；空白檔 → NO_HUMAN_DATA |
| S1 檔案未修改 | S1 manifest 21/21 雜湊相符（建置前、文件完成後各驗證一次；凍結後再驗） |
| S1b 凍結清單 | 寫入後立即逐行重新計算驗證（見清單） |

## 3. 偏離與待確認

- **分析器標示變更：** 除輸入解析外，`VERSION` 字串與結果檔名改為 S1b（不影響計算或關卡）。
- **待研究者目視確認的措辭問題：** 見 `S1B_RESEARCHER_DECISION_RECORD.md` §C（拉丁字元白名單、聲明第 2 條「論文」與第 3 條「研究者」、「區分說明」欄的操作化文字、文獻樣態句保留免責句、家族與類別的字面重疊、題目資訊表重複、無法明確判定在 Q1＝否時不可選）。
- **發送：** 尚未核准；須先完成目視審閱。發送規則見 `S1B_DISTRIBUTION_README.md`（直接寄送、寄前驗證 SHA-256、不經雲端試算表）。

## 4. 狀態

OLD_S1=SUPERSEDED_BEFORE_DISTRIBUTION
NO_HUMAN_DATA_COLLECTED_UNDER_OLD_S1=YES
OLD_S1_FILES_UNMODIFIED=YES (21/21)

OLD_S1_STATUS=SUPERSEDED_BEFORE_DISTRIBUTION
NEW_S1_VERSION=S1B
LANGUAGE=ZH_TW
CODER_FILES=3
BLINDING_AUDIT=PASS
ANALYZER_COMPATIBILITY=PASS
S1B_FREEZE=PASS
V1_HUMAN_RESULTS=NONE
READY_FOR_RESEARCHER_VISUAL_REVIEW=YES
READY_TO_DISTRIBUTE=NO
