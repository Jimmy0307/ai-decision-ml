# S1C — 洩漏、遮蔽、結構與差異稽核

全部重新執行於最終 S1c 檔案上。檢查項目與 S1b 相同（見 `claude/r14_merge_v1_8_2b_v1_s1b_zh_tw/S1B_BLINDING_AUDIT.md` §2），另加 S1c 專屬檢查。

| 稽核 | 腳本 / 結果檔 | 結果 |
|---|---|---|
| 洩漏＋遮蔽＋活頁簿結構＋禁止詞（中英） | `tools/leakage_check_s1c.py` → `tools/leakage_check_result_s1c.json` | **PASS，0 項發現**（XML 部件：13／13／13／17，全部掃描） |
| S1c 指定文字逐字存在（時間句、提醒句、M1–M4 與僅屬證據層的定義／區分、聲明表頭、聲明第 1 條；舊表頭句已不存在） | 同上（`S1C_REQUIRED_TEXT_*`） | PASS（反向測試：對 S1b 檔案執行時，這些檢查正確回報 10 項發現） |
| 「風險」不得作為 M4 關鍵詞（M4 標籤、定義、區分說明、下拉標籤） | 同上（`M4_RISK_KEYWORD`） | PASS |
| 下拉驗證＋標籤正規化＋類別對應 | `tools/test_s1c_label_map.py` | PASS（134 個實際下拉選項；173 個變體） |
| 作答欄與聲明回答欄全部空白 | 洩漏稽核＋相容性測試 (d) | PASS |
| 題目內容逐題對應 S1 英文 ↔ S1b ↔ S1c | `S1C_ITEM_CONTENT_CORRESPONDENCE.csv`（16/16 `S1B_EQUALS_S1C=YES`、`S1_EN_EQUALS_S1B_RECORD=YES`）；洩漏稽核逐列比對四個活頁簿 | PASS |
| 題目順序 | 建置時驗證 S1c 順序＝S1b 活頁簿順序；稽核：三份兩兩不同、≠ 編號順序、≠ 任一 S1 順序 | PASS（ITEM_ORDER_CHANGED=NO） |
| S1b → S1c 逐格差異關卡 | `tools/s1b_to_s1c_diff_gate.py` → `S1C_PATCH_DIFF.md`、`tools/s1b_to_s1c_diff_gate_result.json` | **PASS**：70 項差異，全部屬允許類別，0 項不允許 |

**新增白名單（只在該整句中允許）：** 聲明表頭全句（含「預先設定」）、聲明第 1 條（含「外部」）。兩句皆為 coordinator 指定原文。

## 共用字詞觸發報告（只記錄）

標籤層相同字詞不變：人機、配置（M3）、問責（M1）、流程（M2）、評估、保證（M4）；全部列在「判斷對象」規則中。

定義層變化（修補的直接結果）：M4 定義不再含「風險」（S1b 的「風險」重疊消失）；新增「解釋」（M4 定義「解釋是否足以供決策使用」↔ 解釋與保證）、「問責」（M1 定義 ↔ 人工複核與問責）、「一般」（僅屬證據層定義「一般性問題」↔ 一般決策流程）。完整清單見結果 JSON 的 `priming_report`。

## 已知限制（不變）

同 S1b §5：公開儲存庫歷史中的配對資訊無法撤回；自我聲明無法驗證。
