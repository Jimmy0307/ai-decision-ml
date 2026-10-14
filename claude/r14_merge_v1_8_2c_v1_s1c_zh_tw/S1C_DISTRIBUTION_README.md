# S1C — 發送與回收說明（研究協調人用；取代 S1b 與 30）

**目前狀態：READY_TO_DISTRIBUTE=NO。** 須先完成研究者目視審閱（`S1C_RESEARCHER_VISUAL_REVIEW.md`）並由研究者明確核准發送。

1. **每位編碼者收到什麼。** 每人只收到一個檔案，由研究者以電子郵件或受控檔案傳輸**直接寄送**：
   - 編碼者 1 → `coder_distribution/CODER_1_ZH_TW.xlsx`
   - 編碼者 2 → `coder_distribution/CODER_2_ZH_TW.xlsx`
   - 編碼者 3 → `coder_distribution/CODER_3_ZH_TW.xlsx`

   **絕不經由雲端試算表（包括 Google 試算表）傳送、開啟或預覽。** 在 Google 試算表中開啟會破壞資料驗證並改變檔案位元組（65 B-1：S1 的 `CODER_1.xlsx` 本機副本即因此失效）。也不要用 Excel／WPS 開啟後「另存」寄送用副本。不提供任何儲存庫連結。

2. **寄出前驗證 SHA-256。** 寄出的每個檔案都必須等於 `V1_SEALED/FREEZE_MANIFEST_V1_S1C.txt`（與 `S1C_PACKET_MANIFEST.csv`）中的值。例如：
   ```
   certutil -hashfile CODER_1_ZH_TW.xlsx SHA256
   ```
   不一致就停止，重新從儲存庫取得位元組完全相同的副本。寄送日期與雜湊記錄在 git 之外。

3. **絕不寄給編碼者的檔案。** 本目錄其他所有檔案，特別是：`20_MASTER_PACKET_S1C_ZH_TW.xlsx`（含三張作答表與代碼對照）、所有 `S1C_*.md`／`.csv`、`V1_SEALED/`、`tools/`、研究團隊私有資料夾，以及所有 S1 與 S1b 檔案（`claude/r14_merge_v1_8_2_v1_prefreeze/`、`claude/r14_merge_v1_8_2b_v1_s1b_zh_tw/`，皆已 SUPERSEDED_BEFORE_DISTRIBUTION；S1b 的編碼者檔與 S1c 同名，切勿混用，以雜湊為準）。

4. **任何變更都會使 S1c 失效。** 一旦有編碼者收到檔案，工具、編碼手冊、協定或分析器的任何內容變更都使 S1c 失效；必須另立版本、重新凍結並揭露。

5. **回收檔處理。**
   - 回收檔只存在本機受控空間。**不得推送到公開儲存庫，不得放進本目錄，也不得上傳到任何雲端試算表。**
   - 只做格式檢查（`S1C_CODEBOOK.md` §3 與 S1b 編碼手冊 §2 的規則），只要求修正格式錯誤；絕不提供內容回饋。
   - 分析前先計算每個回收檔的 SHA-256，寫入 `FREEZE_MANIFEST_V1_S1C_S2.txt`（S2）。

6. **分析（S2 之後）。**
   ```
   python -E -P tools/v1_construct_analyzer_s1b.py <C1.xlsx> <C2.xlsx> <C3.xlsx> --s2-manifest <S2 manifest> --out <本機資料夾>
   ```
   其後依 `S1C_PROTOCOL.md` §3（及 S1b 協定 §6） 與分析計畫 29 進行。分析器與 S1b 位元組相同（原樣沿用）。

7. **可公開的內容。** 只有去識別的彙總結果，且須經研究者審閱。不公開編碼者姓名、原始作答檔或個別理由。

8. **題目對照與答案鍵。** 留在受控空間，只在 S3 之後使用（29 §6）；以 S1 的承諾雜湊驗證。
