# Claude 審查證據包（calibration/v1.1-variable-model）

本資料夾保存 Claude 對 Measurement Architecture v1.1／v1.2 候選所做審查的原始報告、診斷腳本與重跑輸出，供 `23_CORRECTION_VALIDATION_GATE_v1_2.md` 的驗證門檻引用。

**狀態界線**：所有數值都是對 `main@1f2e72f` 的 v1.0 **SIMULATED** toy 所做的診斷，不是 JPC 實證結果，也不是 v1.2 候選版的驗證。v1.2 需要新的求解器才能檢驗。

## 內容

| 路徑 | 說明 |
|---|---|
| `reports/Claude_v1_1_Measurement_Architecture_Review.docx` | 對 `e9137d4` 的完整 A–J 審查報告（判定 FAIL；原始修正清單 R1–R14） |
| `reports/Claude_v1_2_Candidate_Rereview.docx` | 對 `4587c52` 的複審（24 號檔五題判定、R1–R14 逐項對照、可凍結項目與解除凍結證據） |
| `scripts/ordinal_invariance.py` | 只在連續目標式內對 κ 與 0–3 等級做保序重編碼，計算九個情境中最適解改變的數目 |
| `scripts/hierarchy_diagnostic.py` | 比較三層解、單層聯合規劃解、兩層（L2 直接選 q）解 |
| `rerun_4587c52/` | 在 HEAD `4587c52` 上的重跑輸出與環境資訊 |
| `SHA256SUMS.txt` | 本資料夾所有檔案的雜湊值 |

## 重跑結果摘要（HEAD 4587c52）

- `run_all.py`（v1.0 歷史回歸）：FINAL LOCAL VERDICT: PASS。只證明 v1.0 模擬輸出未被破壞。
- 保序重編碼：κ {1,2,4} → 6/9 最適解改變；κ {1,2.5,3} → 0/9；H/EA/WI {0,1,1.5,1.8} → 6/9；{0,1,2.5,4.5} → 3/9。
- 階層：兩層與三層在 9/9 情境相同；B=7 的 C/F/D 情境，單層聯合規劃的 F1 比三層解高 0.387600 / 0.422471 / 0.172750。

## 重跑方式

在 repository 根目錄執行：

```
python3 claude_review_evidence/scripts/ordinal_invariance.py .
python3 claude_review_evidence/scripts/hierarchy_diagnostic.py .
```

兩支腳本只讀 `04_solver_v1_0.py` 與 `05_solver_results_v1_0.json`，不寫回 repository（ordinal_invariance.py 會在 /tmp 產生暫存變體檔）。hierarchy_diagnostic.py 需數分鐘。

## 與 23 號檔的對應

23 號檔中「Claude 提述的 6/9、9/9、.17–.42 是轉述，不是本輪獨立重跑」以及「腳本未在倉庫中，標 NOT AVAILABLE」兩處，現在可以改為引用本資料夾的腳本與 `rerun_4587c52/` 輸出。是否修改 23 號檔由研究者決定，本證據包不改動任何既有檔案。
