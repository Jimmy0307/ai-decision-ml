# S1D — 分析器相容性測試

**分析器與標籤對照原樣沿用（與 S1b、S1c 位元組相同）：**

| 檔案 | SHA-256（S1b ＝ S1c ＝ S1d） |
|---|---|
| `tools/v1_construct_analyzer_s1b.py` | `315c4f744e11cd736b330519f868ed7c6a98a40b9745793c00dfd40d1d4d5a8d` |
| `tools/s1b_label_map.json` | `86c5bb33c158a23ef8368c9ec95640256a4e119673e13685c9373d003eea3e8d` |
| `tools/s1b_label_map.py` | `77cb4812725735b4cedbe2c44583fb3346b4fd9b0e3d939d81aa7ee20fbc2720` |

S1d 只改 Q2 欄名文字；欄名仍以「Q2 」（半形空白）開頭，分析器依前綴辨識，解析不需調整。工作表名稱、題目編號欄、聲明表與所有下拉選項不變（差異關卡證明）。

`tools/test_v1_construct_analyzer_s1d.py` → `tools/test_v1_construct_analyzer_s1d_result.txt`：

```
PASS (a)reliability_core=PASS kappa_vs_sklearn_max_abs_diff=2.498e-16 (n=300) alpha_vs_krippendorff_max_abs_diff=4.441e-16 (n=300) classification_rule=PASS oa3_none_validation=PASS s1b_parse_semantics_on_s1d=PASS | (b)label_map=PASS | (c)blank_run_NO_HUMAN_DATA=PASS | (d)structure=PASS
```

- (a) 信度核心 vs sklearn／krippendorff（記憶體內）；分類規則；OA-3；解析語意。
- (b) `tools/test_s1d_label_map.py`：PASS。
- (c) 三份空白 S1d 檔 → `NO_HUMAN_DATA`（`tools/no_human_data_run_s1d/`，檔名沿用 `V1_RESULTS_S1B.*`）。
- (d) 結構解析（含新 Q2 欄名逐字比對）。
- Q1/Q2：27 種組合的接受／拒絕＝26 §2（`S1D_COGNITIVE_CLARITY_AUDIT.md`）。

未建立任何已填答的活頁簿。ANALYZER_COMPATIBILITY=PASS。
