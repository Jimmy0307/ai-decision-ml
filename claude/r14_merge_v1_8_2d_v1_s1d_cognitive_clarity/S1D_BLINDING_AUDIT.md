# S1D — 洩漏、遮蔽、結構與差異稽核

全部於最終 S1d 檔案上重新執行。檢查項目同 S1b／S1c（`claude/r14_merge_v1_8_2b_v1_s1b_zh_tw/S1B_BLINDING_AUDIT.md` §2、`claude/r14_merge_v1_8_2c_v1_s1c_zh_tw/S1C_BLINDING_AUDIT.md`），另加 S1d 檢查。

| 稽核 | 腳本 / 結果檔 | 結果 |
|---|---|---|
| 洩漏＋遮蔽＋活頁簿結構＋中英禁止詞＋拉丁字白名單 | `tools/leakage_check_s1d.py` → `tools/leakage_check_result_s1d.json` | **PASS，0 項發現** |
| S1c 指定文字仍逐字存在；「風險」不作為 M4 關鍵詞 | 同上（沿用 S1c 檢查） | PASS |
| 認知清晰度 A–F（每種誤讀都有逐字阻擋文字與位址） | `tools/cognitive_clarity_check_s1d.py` → `S1D_COGNITIVE_CLARITY_AUDIT.md` | PASS |
| Q1/Q2 一致性（說明文字＝26 §2；未變動分析器 27 種組合＝26） | 同上 | PASS（含 UNCERTAIN＋AMBIGUOUS 合法） |
| 下拉驗證（選項與 S1c 位元組相同）＋標籤正規化＋對應 | `tools/test_s1d_label_map.py`；差異關卡（資料驗證無差異） | PASS（134 選項、173 變體） |
| 作答欄與聲明回答欄全空白 | 洩漏稽核＋相容性 (d) | PASS |
| 題目內容 S1 英文 ↔ S1b ↔ S1c ↔ S1d | `S1D_ITEM_CONTENT_CORRESPONDENCE.csv`（16/16 YES）；洩漏稽核逐列比對 | PASS（ITEM_CONTENT_CHANGED=NO） |
| 題目順序 | 建置時驗證＝S1c；稽核：三份兩兩不同、≠ 編號順序、≠ S1 順序 | PASS（ITEM_ORDER_CHANGED=NO） |
| S1c → S1d 逐格差異關卡 | `tools/s1c_to_s1d_diff_gate.py` → `S1D_PATCH_DIFF.md` | **PASS**：260 項差異，全部允許，0 項不允許 |

**拉丁字白名單：** AI、Q1–Q5、ITEM-Axx、M1–M4；ChatGPT／Claude／Gemini／Copilot 只在聲明第 6 條；**API 只在介面澄清句**。

**整句白名單新增：** 組合特有澄清句與 Q1「是」說明句含「連結」（此處意為「具體連結到」，不是網址連結；「連結」是 S1b 稽核自訂的禁止詞，非研究者禁止清單）。只在這兩整句中允許。

**題目特定內容：** 新增文字皆為一般性範圍說明，不含任何題目特定、正確答案、G 特定、研究者或 AI 試行的範例；稽核中類別標籤／代碼不出現在題目列（PASS）。

**共用字詞：** 新增說明使用「權限與責任」「流程如何轉交」「資料條件」「如何驗證與監控」等一般語詞描述企業決策範圍；它們出現在所有題目共用的說明中，不與任何單一題目連結。家族標籤與類別標籤的相同字詞不變（見結果 JSON `priming_report`）。

已知限制不變（公開儲存庫歷史；自我聲明無法驗證）。
