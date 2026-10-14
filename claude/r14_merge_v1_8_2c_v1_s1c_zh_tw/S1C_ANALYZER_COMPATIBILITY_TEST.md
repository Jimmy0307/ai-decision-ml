# S1C — 分析器相容性測試

**分析器：原樣沿用 S1b。** S1c 未改任何下拉標籤、工作表名稱、欄名或聲明選項，因此不需要調整解析。`tools/` 中的下列檔案與 S1b 位元組完全相同：

| 檔案 | SHA-256（S1b ＝ S1c） |
|---|---|
| `v1_construct_analyzer_s1b.py` | `315c4f744e11cd736b330519f868ed7c6a98a40b9745793c00dfd40d1d4d5a8d` |
| `s1b_label_map.json` | `86c5bb33c158a23ef8368c9ec95640256a4e119673e13685c9373d003eea3e8d` |
| `s1b_label_map.py` | `77cb4812725735b4cedbe2c44583fb3346b4fd9b0e3d939d81aa7ee20fbc2720` |

語意未變的證明：分析器與標籤對照位元組相同；差異關卡證明下拉驗證、工作表名稱、欄名與聲明選項沒有任何差異。與 v182 的差異仍是 `claude/r14_merge_v1_8_2b_v1_s1b_zh_tw/tools/analyzer_diff_v182_to_s1b.diff`（只有解析與標示）。結果檔名因此仍為 `V1_RESULTS_S1B.*`。

## 測試結果（在 S1c 檔案上重跑）

`tools/test_v1_construct_analyzer_s1c.py` → `tools/test_v1_construct_analyzer_s1c_result.txt`：

```
PASS (a)reliability_core=PASS kappa_vs_sklearn_max_abs_diff=2.498e-16 (n=300) alpha_vs_krippendorff_max_abs_diff=4.441e-16 (n=300) classification_rule=PASS oa3_none_validation=PASS s1b_parse_semantics_on_s1c=PASS | (b)label_map=PASS | (c)blank_run_NO_HUMAN_DATA=PASS | (d)structure=PASS
```

- (a) 信度核心 vs sklearn／krippendorff（記憶體內隨機向量）、分類規則、OA-3、解析語意（含 DOES_NOT_COMPLY → EXPOSED）。
- (b) `tools/test_s1c_label_map.py`：PASS（134 個選項、173 個變體）。
- (c) 三份空白 S1c 編碼者檔 → `NO_HUMAN_DATA`（`tools/no_human_data_run_s1c/`）。
- (d) 結構解析：工作表名稱與順序、欄名、16 題、驗證範圍與選項、聲明 7＋3 列（第 1 條為 S1c 新文字）、全空白。

未建立任何已填答的活頁簿。EXPOSED 規則不變：任何「不符合」→ `CODER_STATUS=EXPOSED` → 分開報告，絕不默默合併。
