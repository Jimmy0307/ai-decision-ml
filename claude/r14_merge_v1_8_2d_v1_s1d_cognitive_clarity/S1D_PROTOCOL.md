# S1D — V1 編碼工具：最終認知清晰度修補與發送前凍結（取代 S1c）

**僅供研究團隊。** 狀態：已建置、已稽核、已凍結，待研究者目視審閱（`S1D_RESEARCHER_VISUAL_REVIEW.md`）。**未發送；未蒐集人類資料；未產生模擬作答；未 commit／push。**

## 0. 版本關係

| 項目 | 值 |
|---|---|
| S1（`claude/r14_merge_v1_8_2_v1_prefreeze/`） | SUPERSEDED_BEFORE_DISTRIBUTION；21/21 收尾重新驗證 |
| S1b（`claude/r14_merge_v1_8_2b_v1_s1b_zh_tw/`） | SUPERSEDED_BEFORE_DISTRIBUTION；凍結清單收尾重新驗證 |
| S1c（`claude/r14_merge_v1_8_2c_v1_s1c_zh_tw/`） | SUPERSEDED_BEFORE_DISTRIBUTION；REASON=COGNITIVE_CLARITY_PATCH_BEFORE_ANY_HUMAN_CODING；NO_HUMAN_DATA_COLLECTED_UNDER_S1C=YES；凍結清單收尾重新驗證 |
| 構念權威 | `claude/r14_merge_v1_8_2_v1_prefreeze/26_V1_FINAL_CODEBOOK_v1_8_2.md` |
| 中文語意權威 | `claude/r14_merge_v1_8_2c_v1_s1c_zh_tw/S1C_CODEBOOK.md` |
| 修補動機 | `S1D_COGNITIVE_READABILITY_DECISION.md`（研究者非正式可讀性檢查；不是正式前測） |

## 1. 研究主張的邊界

V1 的主張是：**評估三位獨立人類編碼者，是否能一致地將 16 個功能配對轉譯為企業決策機制。**

V1 **不**主張：專家驗證了文獻缺口；證明了 G 集合；確認了企業實務中確實存在這些問題；驗證了 Study 1 的統計結果；或建立了整個語料的效度。論文中稱編碼者為「具相關領域背景之獨立人工編碼者」（`S1D_RECRUITMENT_ELIGIBILITY.md`），不稱「三位專家」。

## 2. S1d 改了什麼（且只改這些）

由 `tools/s1c_to_s1d_diff_gate.py` 證明（`S1D_PATCH_DIFF.md`：PASS，260 項差異全部屬允許類別，0 項不允許）。所有文字為研究者核准原文，外層引號省略：

| # | 位置（CODER_1） | 內容 | 類別 |
|---|---|---|---|
| 4 | 填答說明 A9（正式定義 A10 之前） | 【作答視角】… | VIEWPOINT |
| 5 | 填答說明 A11 | 企業決策介面不是軟體畫面、使用者介面、API… | INTERFACE_CLARIFICATION |
| 6 | 填答說明 A12 | 企業決策不只指高階主管的策略決策… | DECISION_SCOPE_CLARIFICATION |
| 7 | 填答說明 A13 | 「這個組合特有」不表示只能出現在此組合… | PAIRING_SPECIFIC_CLARIFICATION |
| 8 | 填答說明 A16–A18 | Q1 三個選項說明（Q1 題目與下拉標籤不變） | Q1_OPTION_EXPLANATIONS |
| 9 | 填答說明 A19（Q1 說明正下方） | 請勿因為「我的公司不需要這個」…而選「否」 | NON_APPLICABILITY_WARNING |
| 10 | 填答說明 A20；每張作答頁 I1 | Q2 新措辭（每題必填）；已無任何「如果有」 | Q2_WORDING |
| 11 | 填答說明 A25 | Q1「無法確定」與 Q2「無法明確判定」是不同層次 | Q1_UNCERTAIN_VS_Q2_AMBIGUOUS |
| 12 | 填答說明 A26 | 快速區分（僅重述） | QUICK_DISTINCTION |
| 13 | 題目資訊與作答頁 G 欄（每題） | 文獻樣態說明原兩句不變，追加一句；16 題完全相同 | DEPLETION_FINAL_SENTENCE |
| 14 | 作答聲明 A1 | 原句不變，追加「選擇『不符合』不是答錯…」 | ATTESTATION_SOCIAL_DESIRABILITY |
| — | docProps、zip 部件 | 建立／修改時間戳記；承載上列變更的工作表 XML | METADATA |

**未改：** 標準代碼；M1–M4、跨時間學習與適應、資料條件限制、僅屬證據層、無適用機制、無法明確判定的意義與文字；Q1/Q2 一致性規則；判斷順序；Q3/Q4/Q5；16 題、題目編號、家族名稱與定義；每位編碼者題目順序（建置時驗證＝S1c）；下拉選項（與 S1c 位元組相同）；分析器與標籤對照（與 S1c 位元組相同）；分析計畫、指標、bootstrap、S2/S3 邏輯；所有密封承諾。

**兩個排版說明：**
- 填答說明中的 Q2 列使用研究者原文（「Q2」後為全形空白）。作答頁 I1 欄名在「Q2」後保留半形空白（與 Q1、Q3–Q5 欄名一致），因為未變動的分析器以「Q2 」前綴辨識該欄；文字其餘部分逐字相同。
- 第 (16) 項：沿用 S1c 提醒句「功能類型名稱與機制類別有相同或相近字詞時，不得只因字詞相同就選擇該類別。」（已含要求的意義，未改）。

## 3. 檔案

| 檔案 | 角色 |
|---|---|
| `coder_distribution/CODER_1_ZH_TW.xlsx`…`CODER_3_ZH_TW.xlsx` | 發給編碼者 |
| `20_MASTER_PACKET_S1D_ZH_TW.xlsx` | 研究團隊總表（無 G 編號） |
| `S1D_CODEBOOK.md`、`S1D_PATCH_DIFF.md`、`S1D_COGNITIVE_CLARITY_AUDIT.md`、`S1D_COGNITIVE_READABILITY_DECISION.md` | 編碼手冊增補、差異、清晰度稽核、修補決定 |
| `S1D_RESEARCHER_VISUAL_REVIEW.md`、`S1D_CODER_FACING_PREVIEW.md` | 目視審閱稿（含位址）、預覽 |
| `S1D_PACKET_MANIFEST.csv`、`S1D_ITEM_CONTENT_CORRESPONDENCE.csv` | 雜湊／種子；S1 英文 ↔ S1b ↔ S1c ↔ S1d 逐題 |
| `S1D_BLINDING_AUDIT.md`、`S1D_ANALYZER_COMPATIBILITY_TEST.md`、`S1D_RECRUITMENT_ELIGIBILITY.md`、`S1D_DISTRIBUTION_README.md`、`S1D_FINAL_STATUS.md` | 稽核、相容性、招募資格、發送、狀態 |
| `tools/` | S1d 建置、差異關卡、清晰度檢查、洩漏稽核、測試、審閱稿產生器；原樣沿用的分析器與標籤對照 |
| `V1_SEALED/FREEZE_MANIFEST_V1_S1D.txt` | 最後產生的凍結清單 |

## 4. 分析、階段、資料治理

不變（分析計畫 29；S1b 協定 §6–§8）。S1d 凍結取代 S1c 作為發送基準；S2／S3 清單建議命名 `FREEZE_MANIFEST_V1_S1D_S2.txt`／`_S3.txt`。分析器原樣沿用，結果檔名仍為 `V1_RESULTS_S1B.*`。
