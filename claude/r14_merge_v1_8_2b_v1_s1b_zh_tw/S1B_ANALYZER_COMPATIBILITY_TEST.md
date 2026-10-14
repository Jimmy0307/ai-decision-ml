# S1B — 分析器相容性測試

**分析器：** `tools/v1_construct_analyzer_s1b.py`，由 `claude/r14_merge_v1_8_2_v1_prefreeze/tools/v1_construct_analyzer_v182.py`（SHA-256 `9ce02b2a735e2baf7704ed3710ae2a740562a26d6e866d949d94cd8ccd862f9c`，未修改）衍生。
**完整差異：** `tools/analyzer_diff_v182_to_s1b.diff`（unified diff）。

**結論：ANALYZER_COMPATIBILITY=PASS。** 未建立任何已填答的活頁簿；所有含答案的測試資料都只存在記憶體中。

## 1. 差異範圍（只有輸入解析＋標示）

差異共 8 個 hunk，全部位於下列位置。v182 的 `is_empty()`、`validate()`（第 146–178 行）以及 `derived()` 到 `run()` 的計算與關卡邏輯（第 184–504 行：53B 對照、分類、κ／α 與 bootstrap、描述統計、裁決匯入、題目對照驗證、解封、C6、md 輸出、階段流程）**完全未動**。

| v182 位置 | 變更 | 類別 |
|---|---|---|
| 檔頭說明、Usage | 說明 S1b 只改解析；檔名範例 | 文件 |
| import 區 | 匯入同目錄的 `s1b_label_map` | 解析 |
| `VERSION` | `v1_construct_analyzer_v1_8_2` → `v1_construct_analyzer_s1b` | 標示 |
| 常數區 | 新增 S1b 解析常數（作答表前綴「作答_編碼者」、題目編號欄「題目編號」、聲明表「作答聲明」、姓名／日期／簽名、Q1–Q5 欄名前綴）；`OUT_REL` **保持指向 S1 的 V1_SEALED**（答案鍵與題目對照承諾不變） | 解析 |
| `read_sheet()` | 依中文工作表名與欄名找欄位；作答表名轉為標準名 `CODER_k`；Q1–Q4 經 `s1b_label_map` 由中文標籤轉成標準代碼（無法對應的非空白值保留原字串，交由原本的 `validate()` 判為無效）；聲明「符合／不符合」→ `COMPLIES／DOES_NOT_COMPLY`，非空白但無法對應者 → INPUT_INVALID | 解析 |
| `attestation_exposed()` | 判斷值由 `NO` 改為 `DOES_NOT_COMPLY`；略過姓名／日期／簽名 | 解析（聲明語意） |
| 結果輸出檔名 | `V1_RESULTS_v1_8_2.*` → `V1_RESULTS_S1B.*` | 標示 |

**不變：** 標準代碼集合 Q1–Q4、`validate()` 的全部一致性規則（含 OA-3）、`derived()`（53B 對照）、`reliability_v2_2.py` 雜湊檢查、α／κ／bootstrap（5,000 次、種子 20261011）、門檻 .800／.667 與 IMPRECISE、RESEARCH_CONVENTION、EXPOSED 處理（CLEAN／ALL 兩個範圍）、S2／S3 manifest 關卡、題目對照與答案鍵的雜湊驗證、C6 規則、NO_HUMAN_DATA 判定。

**偏離說明（請研究者知悉）：** 決定 11 要求「只改輸入解析」。除解析外，另有兩個純標示變更：`VERSION` 字串與結果檔名，以免 S1b 的結果檔被誤認為 S1 的結果。兩者不影響任何計算或關卡。

## 2. 測試結果

`tools/test_v1_construct_analyzer_s1b.py`（結果檔 `tools/test_v1_construct_analyzer_s1b_result.txt`）：

```
PASS (a)reliability_core=PASS kappa_vs_sklearn_max_abs_diff=2.498e-16 (n=300) alpha_vs_krippendorff_max_abs_diff=4.441e-16 (n=300) classification_rule=PASS oa3_none_validation=PASS s1b_parse_semantics=PASS | (b)label_map=PASS | (c)blank_run_NO_HUMAN_DATA=PASS | (d)structure=PASS
```

| 測試 | 內容 | 結果 |
|---|---|---|
| (a) 信度核心 | 未變的 `reliability_v2_2` 函式 vs `sklearn.metrics.cohen_kappa_score` 與 `krippendorff.alpha`，300 組記憶體內隨機向量；分類規則邊界；OA-3（NONE 需 Q1＝是與 Q5）；S1b 解析語意（記憶體內：中文標籤 → 代碼 → 原 `validate()`，例如「是」＋「僅屬證據層」被判為 Q1=YES with Q2=EVIDENCE_ONLY；英文代碼誤填「YES」於 Q2 被判無效；`DOES_NOT_COMPLY` → EXPOSED，`COMPLIES` → 不 EXPOSED） | PASS（與 S1 測試的最大誤差數值相同） |
| (b) 標籤對照 | `tools/test_s1b_label_map.py`（見 `S1B_BLINDING_AUDIT.md` §3） | PASS |
| (c) 空白檔執行 | 分析器讀三份空白 `CODER_k_ZH_TW.xlsx` → `NO_HUMAN_DATA`，不計算任何東西；輸出在 `tools/no_human_data_run_s1b/` | PASS |
| (d) 結構解析 | 每份檔：工作表名稱與順序；作答表 12 個欄名逐字；16 題、題序 1–16；Q1–Q4 清單驗證（範圍 H2:H17…K2:K17、選項與對照表一致、錯誤阻擋）與 Q5 字數驗證（≤ 600）；聲明 7 條＋姓名／日期／簽名、回答欄空白、單一下拉驗證涵蓋 C3–C9；分析器 `read_sheet()` 解析為 `CODER_k`、16 題、全空白、10 列聲明；`validate()` 在空白檔上只回報預期的 65 個「空白」錯誤 | PASS |

`tools/test_s1b_label_map_result.txt`：

```
PASS M1_M2_bijection_and_canonical_sets=PASS M3_workbook_dropdowns_map=PASS M4_variants_normalize_to_one_code=PASS M5_unknown_labels_unmapped=PASS dropdown_options_checked=134 variants_checked=173
```

## 3. 未驗證

與 S1 相同：尚未在已填答的工作表上端到端執行完整流程，因為人類編碼開始前不得建立任何已填答的活頁簿。
