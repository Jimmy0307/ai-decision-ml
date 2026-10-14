# 41 — Patch Log v1.8.2 → v1.8.3 (V5 PROVENANCE CANDIDATE)

- Input: `claude/r14_merge_v1_8_2_v1_prefreeze/32_MERGED_MASTER_THESIS_v1_8_2_V1_PREFREEZE_CANDIDATE.md` sha256 `2d493edc2e1884f05e5b0617bc56f1f85cdab0fa33531ac566b61d343dd8f159` (asserted by the patch script).
- Output: `41_MERGED_MASTER_THESIS_v1_8_3_V5_PROVENANCE_CANDIDATE.md` sha256 `0da8cec1521dbeff900ffa1fa9a1de0a31b0cdfa34b82c03531eba2111d7f740`.
- Method: `tools/R/patch_v183.py`, which applies 34 exact old→new replacements. Each `old` is asserted to match exactly once in v1.8.2 and once at apply time.
- Verification: `tools/R/verify_v183.py` → `tools/R/verify_out_v183.json`. This log is built by `tools/R/build_log_v183.py`, which refuses to run unless every hard check passes.
- Scope: provenance and status wording only.
  - Changed: the status line; every "12/37 protected inputs missing" statement; the official-core provenance; the V5 Data Pack provenance; the sidecar core and generator; the propagation rule; the HUMAN_AUDIT log hash wording; the full-reanalysis execution status; the E39/E40/E44/E48/E12 residual-limit text; and the Appendix D rows for 35–41.
  - Unchanged: math, result numbers, G rows, Table 3-4/3-4A, headings, V1 design text (§3.9.3) and the Enterprise model.
  - No DOCX was built.

## Changes

| ID | v1.8.2 line | v1.8.3 line | Section | Category | Source |
|---|---|---|---|---|---|
| R01 | 5 | 5 | 稿件狀態 | version label | this round (output 41); Appendix D row R24 |
| R02 | 5 | 5 | 稿件狀態 | v1.8.3 provenance summary | OUT 35 §1–§2, §6; OUT 36 §A–§D; OUT 37 §1, §3, §6–§7; OUT 39 §1 |
| R03 | 5 | 5 | 稿件狀態 | full-reanalysis execution status | orchestrator triplet v1.8.3 (OUT 39 §3); OUT 38 §1, §2e–g, §3–§4 |
| R04 | 13 | 13 | 摘要 | full-reanalysis execution status | orchestrator triplet v1.8.3 (OUT 39 §3) |
| R05 | 29 | 29 | Abstract | full-reanalysis execution status (English) | orchestrator triplet v1.8.3 (OUT 39 §3); OUT 37 §1, §3, §6–§7 |
| R06 | 122 | 122 | 1.4 | full-reanalysis execution status | orchestrator triplet v1.8.3 (OUT 39 §3) |
| R07 | 147 | 147 | 1.4 表 | full-reanalysis execution status | orchestrator triplet v1.8.3 (OUT 39 §3) |
| R08 | 158 | 158 | 1.5 | full-reanalysis execution status | orchestrator triplet v1.8.3 (OUT 39 §3) |
| R09 | 168 | 168 | 1.6 | full-reanalysis execution status | orchestrator triplet v1.8.3 (OUT 39 §3) |
| R10 | 405 | 405 | 3.1.1 | full-reanalysis execution status | orchestrator triplet v1.8.3 (OUT 39 §3) |
| R11 | 412 | 412 | 3.1.1 流程 | full-reanalysis execution status | orchestrator triplet v1.8.3 (OUT 39 §3) |
| R12 | 591 | 591 | 3.7.1 | HUMAN_AUDIT log hash wording | OUT 37 §1, §3, §6–§7 (row 26, prefix match); orchestrator wording rule |
| R13 | 605 | 605 | 3.7.4 | sidecar generator / propagation rule provenance | OUT 37 §1, §3, §6–§7 §6; OUT 38 §1, §2e–g, §3–§4 §2e–f |
| R14 | 609 | 609 | 3.7.4 | full-reanalysis execution status | orchestrator triplet v1.8.3 (OUT 39 §3); OUT 37 §1, §3, §6–§7 |
| R15 | 651 | 651 | 3.8.3 | V5 Data Pack provenance | OUT 35 §1–§2, §6 §1 (stage 14, 74/74); data pack 04_STAGE2_RUNTIME_SUMMARY.json a4111914… (manifest-listed) unique_model_digests |
| R16 | 1629 | 1629 | 4.5.5 | full-reanalysis execution status | orchestrator triplet v1.8.3 (OUT 39 §3) |
| R17 | 2185 | 2185 | 4.11 表 | full-reanalysis execution status | orchestrator triplet v1.8.3 (OUT 39 §3) |
| R18 | 2192 | 2192 | 4.11 | full-reanalysis execution status | orchestrator triplet v1.8.3 (OUT 39 §3) |
| R19 | 2240 | 2240 | 5.3.2 表 | full-reanalysis execution status | orchestrator triplet v1.8.3 (OUT 39 §3) |
| R20 | 2364 | 2364 | 5.8.9 | full-reanalysis execution status | orchestrator triplet v1.8.3 (OUT 39 §3) |
| R21 | 2368 | 2368 | 5.9 | full-reanalysis execution precondition | orchestrator triplet v1.8.3 (OUT 39 §3); OUT 38 §1, §2e–g, §3–§4 §3 |
| R22 | 2380 | 2380 | 5.10 | full-reanalysis execution status | orchestrator triplet v1.8.3 (OUT 39 §3) |
| R23 | 630 | 630 | 3.8.1 表 | full-reanalysis execution status | orchestrator triplet v1.8.3 (OUT 39 §3) |
| R24 | 3033 | 3033 | 附錄 D | Appendix D rows 35–41 | OUT file list 35–41; this round |
| R25 | 3050 | 3055 | 附錄 E12 | V5 Data Pack provenance | OUT 35 §1–§2, §6 |
| R26 | 3077 | 3082 | 附錄 E39 | residual limit (a) | OUT 37 §1, §3, §6–§7 row 26 |
| R27 | 3077 | 3082 | 附錄 E39 | residual limit (b) | OUT 35 §1–§2, §6; OUT 36 §A–§D; OUT 37 §1, §3, §6–§7 |
| R28 | 3077 | 3082 | 附錄 E39 | residual limit (c) | OUT 37 §1, §3, §6–§7 §6; OUT 38 §1, §2e–g, §3–§4 §2e |
| R29 | 3077 | 3082 | 附錄 E39 | residual-limit summary | OUT 39 |
| R30 | 3078 | 3083 | 附錄 E40 | full-reanalysis triplet | orchestrator triplet v1.8.3 (OUT 39 §3); OUT 38 §1, §2e–g, §3–§4 §4 |
| R31 | 3078 | 3083 | 附錄 E40 | full-reanalysis precondition | orchestrator triplet v1.8.3 (OUT 39 §3); OUT 38 §1, §2e–g, §3–§4 §3 |
| R32 | 3082 | 3087 | 附錄 E44 | full-reanalysis execution status | orchestrator triplet v1.8.3 (OUT 39 §3) |
| R33 | 3086 | 3091 | 附錄 E48 | propagation rule status | OUT 38 §1, §2e–g, §3–§4 §2e–f |
| R34 | 3086 | 3091 | 附錄 E48 | propagation rule action | orchestrator triplet v1.8.3 (OUT 39 §3); OUT 38 §1, §2e–g, §3–§4 §2f |

## Old → new text

### R01 — 稿件狀態 (v1.8.2 L5 → v1.8.3 L5)

Source: this round (output 41); Appendix D row R24

OLD:

```text
合併碩士論文 v1.8.2 V1 PREFREEZE CANDIDATE（由 v1.8.1 修訂；v1.0–v1.8.1 保留、未覆寫；
```

NEW:

```text
合併碩士論文 v1.8.3 V5 PROVENANCE CANDIDATE（由 v1.8.2 修訂；v1.0–v1.8.2 保留、未覆寫；
```

### R02 — 稿件狀態 (v1.8.2 L5 → v1.8.3 L5)

Source: OUT 35 §1–§2, §6; OUT 36 §A–§D; OUT 37 §1, §3, §6–§7; OUT 39 §1

OLD:

```text
V1.8.1 的 19–21 封包顯示 G 編號，已被取代、不得發送。(1)
```

NEW:

```text
V1.8.1 的 19–21 封包顯示 G 編號，已被取代、不得發送。v1.8.3 只更新來源與狀態描述，不改變任何數值、G 清單、V1 設計或企業模型：V5 正式生產資料夾已尋回，並以完整 SHA-256 與各階段清單鏈核對（V1.8.3 檔案 35–38）；正式凍結核心檔（FINAL_ROBUST_CORE_32.csv）的來源由「只以重現檔佐證」改為已確認（CONFIRMED）；V5 Manuscript Data Pack 已尋回；V9 受保護基準的 37 項輸入全數以完整 SHA-256 確認；文獻層證據凍結的數值不變，只強化其來源（V1.8.3 檔案 39–40）。(1)
```

### R03 — 稿件狀態 (v1.8.2 L5 → v1.8.3 L5)

Source: orchestrator triplet v1.8.3 (OUT 39 §3); OUT 38 §1, §2e–g, §3–§4

OLD:

```text
但以目前的來源集無法執行（37 項受保護輸入中 12 項未尋回；NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET）
```

NEW:

```text
其執行條件尚待滿足（EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION：37 項受保護輸入已全數以完整 SHA-256 確認，但須先由研究者事先登記並以雜湊承諾標籤傳播規則、在新的日期目錄中以僅修改路徑的程式複本重現 13 個雜湊釘定的正式輸出，並依 V9 經研究者核准）
```

### R04 — 摘要 (v1.8.2 L13 → v1.8.3 L13)

Source: orchestrator triplet v1.8.3 (OUT 39 §3)

OLD:

```text
完整重分析列為開放的驗證行動，但以目前的來源集無法執行，在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定。
```

NEW:

```text
完整重分析列為開放的驗證行動，其執行條件尚待滿足（須先事先登記標籤傳播規則並重現正式基準），在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定。
```

### R05 — Abstract (v1.8.2 L29 → v1.8.3 L29)

Source: orchestrator triplet v1.8.3 (OUT 39 §3); OUT 37 §1, §3, §6–§7

OLD:

```text
it cannot be executed with the currently recovered source set (12 of 37 protected inputs are missing),
```

NEW:

```text
its execution is pending researcher predeclaration and hash commitment of the label-propagation rule, byte-for-byte reproduction of the pinned official baseline in the current workspace, and researcher approval (all 37 protected inputs are now hash-confirmed),
```

### R06 — 1.4 (v1.8.2 L122 → v1.8.3 L122)

Source: orchestrator triplet v1.8.3 (OUT 39 §3)

OLD:

```text
但以目前的來源集無法執行，在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（第 4.5.5 節；附錄 E40）。研究問題三
```

NEW:

```text
其執行條件尚待滿足（須先事先登記標籤傳播規則並重現正式基準），在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（第 4.5.5 節；附錄 E40）。研究問題三
```

### R07 — 1.4 表 (v1.8.2 L147 → v1.8.3 L147)

Source: orchestrator triplet v1.8.3 (OUT 39 §3)

OLD:

```text
以目前來源集無法執行，V1 前不建議優先執行（附錄 E40） |
```

NEW:

```text
執行條件待滿足（須先登記傳播規則並重現基準），V1 前不建議優先執行（附錄 E40） |
```

### R08 — 1.5 (v1.8.2 L158 → v1.8.3 L158)

Source: orchestrator triplet v1.8.3 (OUT 39 §3)

OLD:

```text
（開放驗證行動、以目前來源集無法執行、V1 前不建議優先執行）
```

NEW:

```text
（開放驗證行動、執行條件待滿足、V1 前不建議優先執行）
```

### R09 — 1.6 (v1.8.2 L168 → v1.8.3 L168)

Source: orchestrator triplet v1.8.3 (OUT 39 §3)

OLD:

```text
但以目前的來源集無法執行，在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（第 4.5.5 節；附錄 E40）；逐格解讀
```

NEW:

```text
其執行條件尚待滿足（須先事先登記標籤傳播規則並重現正式基準），在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（第 4.5.5 節；附錄 E40）；逐格解讀
```

### R10 — 3.1.1 (v1.8.2 L405 → v1.8.3 L405)

Source: orchestrator triplet v1.8.3 (OUT 39 §3)

OLD:

```text
但以目前的來源集無法執行，在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（第 3.7.4、4.5.5 節；附錄 E40）。第二層
```

NEW:

```text
其執行條件尚待滿足（須先事先登記標籤傳播規則並重現正式基準），在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（第 3.7.4、4.5.5 節；附錄 E40）。第二層
```

### R11 — 3.1.1 流程 (v1.8.2 L412 → v1.8.3 L412)

Source: orchestrator triplet v1.8.3 (OUT 39 §3)

OLD:

```text
完整重分析為開放驗證行動，目前無法執行）
```

NEW:

```text
完整重分析為開放驗證行動，執行條件待滿足）
```

### R12 — 3.7.1 (v1.8.2 L591 → v1.8.3 L591)

Source: OUT 37 §1, §3, §6–§7 (row 26, prefix match); orchestrator wording rule

OLD:

```text
V9 套件的完整性紀錄另顯示，早期稽核日誌 HUMAN_AUDIT_APPEND_ONLY_LOG.csv 的現行雜湊與受保護基準不符（套件記為 LEGACY_AUDIT_LOG_INTEGRITY = UNVERIFIED，未發現竄改證據）；凍結的第一位編碼者檔、盲式第二編碼檔與調和檔的雜湊均與套件雜湊清單相符。此為來源完整性的限制（附錄 E39）。
```

NEW:

```text
V9 套件的完整性紀錄另顯示，早期稽核日誌 HUMAN_AUDIT_APPEND_ONLY_LOG.csv 的現行雜湊與受保護基準不符（套件當時記為 LEGACY_AUDIT_LOG_INTEGRITY = UNVERIFIED；此標記屬歷史紀錄，未發現竄改證據）；v1.8.3 的核對顯示，受保護狀態與現行附加式日誌的前 355 位元組逐位元組相同（完整 SHA-256 相符），其後的位元組皆為附加的事件，符合附加式日誌的預期，即受保護狀態已確認為附加式日誌的前綴（V1.8.3 檔案 37）；凍結的第一位編碼者檔、盲式第二編碼檔與調和檔的雜湊均與套件雜湊清單相符（附錄 E39）。
```

### R13 — 3.7.4 (v1.8.2 L605 → v1.8.3 L605)

Source: OUT 37 §1, §3, §6–§7 §6; OUT 38 §1, §2e–g, §3–§4 §2e–f

OLD:

```text
但產生敏感度表的程式未隨套件保存，人工標籤中的「不確定」「模糊」「無法對應」如何轉為配對資格，無法由套件重現 `[AUTHOR TO CONFIRM：標籤至配對資格的傳播規則與重算程式；附錄 E48]`。
```

NEW:

```text
替換後的核心檔、側車產生程式與其標籤處理政策不在 V9 套件內，但已於 V9 側車資料夾尋回（V1.8.3 檔案 37–38）：替換後的核心檔以完整 SHA-256 確認；側車產生程式的位置與其輸出一致，但其本身的雜湊未由 V9 釘定（PROBABLE）；產生敏感度表本身的程式仍未尋回。人工標籤中的「不確定」「模糊」「無法對應」如何轉為配對資格，已由側車政策尋回（RECOVERED_FROM_SIDECAR_POLICY），以獨立程式重算可重現側車的逐筆處理與配對資格變動；此規則屬事後尋回，不是事前登記，若執行完整重分析，仍須由研究者事先登記並以雜湊承諾 `[AUTHOR TO CONFIRM：是否採用尋回的傳播規則並事先登記；附錄 E48]`。
```

### R14 — 3.7.4 (v1.8.2 L609 → v1.8.3 L609)

Source: orchestrator triplet v1.8.3 (OUT 39 §3); OUT 37 §1, §3, §6–§7

OLD:

```text
以目前的來源集無法執行（37 項受保護輸入中 12 項未尋回）
```

NEW:

```text
其執行條件尚待滿足（37 項受保護輸入已全數以完整 SHA-256 確認；須先事先登記標籤傳播規則並重現正式基準）
```

### R15 — 3.8.3 (v1.8.2 L651 → v1.8.3 L651)

Source: OUT 35 §1–§2, §6 §1 (stage 14, 74/74); data pack 04_STAGE2_RUNTIME_SUMMARY.json a4111914… (manifest-listed) unique_model_digests

OLD:

```text
（依專案紀錄的 V5 Manuscript Data Pack 模型資訊；Data Pack 原檔不在本稿工作環境中，投稿前須以原檔核對）
```

NEW:

```text
（取自 V5 Manuscript Data Pack 的模型紀錄；v1.8.3 已尋回 Data Pack 原檔 data_pack_v1_20260922T010012Z，其清單所列 74 個檔案雜湊全數相符，模型摘要值與其中的 STAGE2_RUNTIME_SUMMARY 模型紀錄逐字相符；V1.8.3 檔案 35）
```

### R16 — 4.5.5 (v1.8.2 L1629 → v1.8.3 L1629)

Source: orchestrator triplet v1.8.3 (OUT 39 §3)

OLD:

```text
以目前的來源集無法執行（37 項受保護輸入中 12 項未尋回；FULL_REANALYSIS_EXECUTION_STATUS = NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET）
```

NEW:

```text
其執行條件尚待滿足（37 項受保護輸入已全數以完整 SHA-256 確認，但須先事先登記標籤傳播規則並重現正式基準，且經研究者核准；FULL_REANALYSIS_EXECUTION_STATUS = EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION）
```

### R17 — 4.11 表 (v1.8.2 L2185 → v1.8.3 L2185)

Source: orchestrator triplet v1.8.3 (OUT 39 §3)

OLD:

```text
凍結的 32 組仍為推論基準；完整重分析為開放驗證行動，以目前來源集無法執行
```

NEW:

```text
凍結的 32 組仍為推論基準；完整重分析為開放驗證行動，執行條件待滿足（須先登記傳播規則並重現基準）
```

### R18 — 4.11 (v1.8.2 L2192 → v1.8.3 L2192)

Source: orchestrator triplet v1.8.3 (OUT 39 §3)

OLD:

```text
完整重分析為開放驗證行動，以目前來源集無法執行，見附錄 E40）
```

NEW:

```text
完整重分析為開放驗證行動，執行條件待滿足（須先登記傳播規則並重現基準），見附錄 E40）
```

### R19 — 5.3.2 表 (v1.8.2 L2240 → v1.8.3 L2240)

Source: orchestrator triplet v1.8.3 (OUT 39 §3)

OLD:

```text
完整重分析為開放驗證行動，以目前來源集無法執行（附錄 E40） |
```

NEW:

```text
完整重分析為開放驗證行動，執行條件待滿足（須先登記傳播規則並重現基準）（附錄 E40） |
```

### R20 — 5.8.9 (v1.8.2 L2364 → v1.8.3 L2364)

Source: orchestrator triplet v1.8.3 (OUT 39 §3)

OLD:

```text
FULL_REANALYSIS_EXECUTION_STATUS = NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET，FULL_REANALYSIS_PRIORITY_BEFORE_V1
```

NEW:

```text
FULL_REANALYSIS_EXECUTION_STATUS = EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION，FULL_REANALYSIS_PRIORITY_BEFORE_V1
```

### R21 — 5.9 (v1.8.2 L2368 → v1.8.3 L2368)

Source: orchestrator triplet v1.8.3 (OUT 39 §3); OUT 38 §1, §2e–g, §3–§4 §3

OLD:

```text
執行前須先尋回缺件的受保護輸入，時程排在
```

NEW:

```text
受保護輸入已全數尋回，執行前須先事先登記標籤傳播規則並在現行工作環境重現正式基準，時程排在
```

### R22 — 5.10 (v1.8.2 L2380 → v1.8.3 L2380)

Source: orchestrator triplet v1.8.3 (OUT 39 §3)

OLD:

```text
但以目前的來源集無法執行（附錄 E40）。
```

NEW:

```text
其執行條件尚待滿足（須先事先登記標籤傳播規則並重現正式基準）（附錄 E40）。
```

### R23 — 3.8.1 表 (v1.8.2 L630 → v1.8.3 L630)

Source: orchestrator triplet v1.8.3 (OUT 39 §3)

OLD:

```text
局部成員敏感度；不取代 L2；完整重分析為開放驗證行動，以目前來源集無法執行
```

NEW:

```text
局部成員敏感度；不取代 L2；完整重分析為開放驗證行動，執行條件待滿足（須先登記傳播規則並重現基準）
```

### R24 — 附錄 D (v1.8.2 L3033 → v1.8.3 L3033)

Source: OUT file list 35–41; this round

OLD:

```text
| v1.8.2／32 | — | `32_MERGED_MASTER_THESIS_v1_8_2_V1_PREFREEZE_CANDIDATE.md` | 合併論文 v1.8.2（V1 凍結前版；只更新 V1 設計與狀態描述） | 本稿 |
```

NEW:

```text
| v1.8.2／32 | — | `32_MERGED_MASTER_THESIS_v1_8_2_V1_PREFREEZE_CANDIDATE.md` | 合併論文 v1.8.2（V1 凍結前版；只更新 V1 設計與狀態描述） | v1.8.3 的修訂底稿（已保存；未覆寫） |
| v1.8.3／35–36 | — | `35_V5_MANIFEST_CHAIN_VERIFICATION.md`、`36_V5_BASELINE_RECOMPUTATION.md`（另有 .csv／.json） | V5 正式生產資料夾的各階段清單鏈核對，以及由凍結原始列重算的文獻層基準（數值不變） | 稿件狀態；第 3.8.3 節；附錄 E12、E39 |
| v1.8.3／37 | — | `37_PROTECTED_INPUT_RECOVERY.md`（另有 .csv） | V9 受保護基準 37 項輸入的尋回與完整雜湊確認；附加式日誌前綴核對；替換後核心檔的位置 | 第 3.7.1、3.7.4 節；附錄 E39 |
| v1.8.3／38 | — | `38_FULL_REANALYSIS_FEASIBILITY.md` | 完整重分析的執行可行性；尋回的標籤傳播規則與側車產生程式 | 第 3.7.4、4.5.5、5.8.9 節；附錄 E40、E48 |
| v1.8.3／39–40 | — | `39_STUDY1_FREEZE_PROVENANCE_ADDENDUM_v1_8_3.md`、`40_STUDY1_FREEZE_HASHES_v1_8_3.csv` | 文獻層（Study 1）證據凍結的來源補充與雜湊帳（凍結數值不變） | 稿件狀態；附錄 E39、E40 |
| v1.8.3／41 | — | `41_MERGED_MASTER_THESIS_v1_8_3_V5_PROVENANCE_CANDIDATE.md` | 合併論文 v1.8.3（V5 來源版；只更新來源與狀態描述） | 本稿 |
```

### R25 — 附錄 E12 (v1.8.2 L3050 → v1.8.3 L3055)

Source: OUT 35 §1–§2, §6

OLD:

```text
模型摘要值取自 V5 Data Pack 的模型紀錄；Ollama 版本未保存，維持為再現性限制
```

NEW:

```text
模型摘要值取自 V5 Data Pack 的模型紀錄（v1.8.3 已尋回 Data Pack 原檔並核對一致，V1.8.3 檔案 35）；Ollama 版本未保存，維持為再現性限制
```

### R26 — 附錄 E39 (v1.8.2 L3077 → v1.8.3 L3082)

Source: OUT 37 §1, §3, §6–§7 row 26

OLD:

```text
（a）FINAL_STATUS.json 記錄一項受保護雜湊不符（HUMAN_AUDIT_APPEND_ONLY_LOG.csv；LEGACY_AUDIT_LOG_INTEGRITY = UNVERIFIED，未發現竄改證據），凍結的編碼檔與調和檔雜湊完好；
```

NEW:

```text
（a）FINAL_STATUS.json 記錄一項受保護雜湊不符（HUMAN_AUDIT_APPEND_ONLY_LOG.csv；LEGACY_AUDIT_LOG_INTEGRITY = UNVERIFIED，屬歷史標記，未發現竄改證據）；v1.8.3 已確認受保護狀態為現行附加式日誌的前 355 位元組（完整 SHA-256 相符；V1.8.3 檔案 37），凍結的編碼檔與調和檔雜湊完好；
```

### R27 — 附錄 E39 (v1.8.2 L3077 → v1.8.3 L3082)

Source: OUT 35 §1–§2, §6; OUT 36 §A–§D; OUT 37 §1, §3, §6–§7

OLD:

```text
（b）套件受保護基準所列 37 項輸入中有 12 項（含原始 400／120 抽樣檔、V9 原稿、凍結資料庫與凍結清單）不在套件中，正式凍結核心檔只以套件內位元組相同的重現檔佐證；
```

NEW:

```text
（b）套件受保護基準所列 37 項輸入中有 12 項（含原始 400／120 抽樣檔、V9 原稿、凍結資料庫與凍結清單）不在套件中；v1.8.3 已在工作環境的其他位置尋回全部 37 項並以完整 SHA-256 確認（V1.8.3 檔案 37），正式凍結核心檔亦於 V5 正式生產資料夾尋回，並經 V5 各階段清單鏈核對確認（V1.8.3 檔案 35–36），不再只以重現檔佐證；
```

### R28 — 附錄 E39 (v1.8.2 L3077 → v1.8.3 L3082)

Source: OUT 37 §1, §3, §6–§7 §6; OUT 38 §1, §2e–g, §3–§4 §2e

OLD:

```text
（c）替換後的核心檔與產生敏感度表的程式未隨套件保存，替換後成員係由敏感度表逐列重現；
```

NEW:

```text
（c）替換後的核心檔與側車產生程式不在套件中，已於 V9 側車資料夾尋回：替換後的核心檔以完整 SHA-256 確認，側車產生程式為 PROBABLE（其雜湊未由 V9 釘定）；產生敏感度表本身的程式仍未尋回，替換後成員係由敏感度表逐列重現，並與尋回的替換後核心檔一致；
```

### R29 — 附錄 E39 (v1.8.2 L3077 → v1.8.3 L3082)

Source: OUT 39

OLD:

```text
殘餘限制（a）–（d）保留，傳播規則見 E48，完整重分析見 E40 |
```

NEW:

```text
殘餘限制（a）–（c）已依 v1.8.3 的來源核對更新（V1.8.3 檔案 35–39），（d）保留；傳播規則見 E48，完整重分析見 E40 |
```

### R30 — 附錄 E40 (v1.8.2 L3078 → v1.8.3 L3083)

Source: orchestrator triplet v1.8.3 (OUT 39 §3); OUT 38 §1, §2e–g, §3–§4 §4

OLD:

```text
FULL_REANALYSIS_EXECUTION_STATUS = NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET（套件受保護基準 37 項輸入中 12 項未尋回，E39（b））；FULL_REANALYSIS_PRIORITY_BEFORE_V1 = NOT_RECOMMENDED（V1.8 檔案 07 §8；V1.8.1 檔案 15、17）。
```

NEW:

```text
FULL_REANALYSIS_EXECUTION_STATUS = EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION（v1.8.3：37 項受保護輸入已全數以完整 SHA-256 確認，E39（b）；尚待三項前置條件：研究者事先登記並以雜湊承諾標籤傳播規則、在新的日期目錄中以僅修改路徑的程式複本逐位元組重現 13 個雜湊釘定的正式輸出、依 V9 經研究者核准；V1.8.3 檔案 38）；FULL_REANALYSIS_PRIORITY_BEFORE_V1 = NOT_RECOMMENDED（V1.8 檔案 07 §8；V1.8.1 檔案 15、17；屬研究者決定。原理由 1「受保護輸入缺件」已不成立，理由 2–5 仍成立；已請研究者重新檢視此優先順序的理由：PRIORITY_RATIONALE_REVIEW_REQUESTED）。
```

### R31 — 附錄 E40 (v1.8.2 L3078 → v1.8.3 L3083)

Source: orchestrator triplet v1.8.3 (OUT 39 §3); OUT 38 §1, §2e–g, §3–§4 §3

OLD:

```text
重跑前須先補回缺件的受保護輸入（E39（b））並事先登記標籤傳播規則（E48）；
```

NEW:

```text
重跑前須先事先登記並以雜湊承諾標籤傳播規則（E48），並在現行工作環境重現正式基準；
```

### R32 — 附錄 E44 (v1.8.2 L3082 → v1.8.3 L3087)

Source: orchestrator triplet v1.8.3 (OUT 39 §3)

OLD:

```text
完整重分析為開放驗證行動且以目前來源集無法執行（E40）
```

NEW:

```text
完整重分析為開放驗證行動且執行條件待滿足（E40）
```

### R33 — 附錄 E48 (v1.8.2 L3086 → v1.8.3 L3091)

Source: OUT 38 §1, §2e–g, §3–§4 §2e–f

OLD:

```text
人工標籤中「不確定」「模糊」「無法對應」轉為配對資格的規則，以及產生敏感度表的程式，未隨套件保存而無法重現；
```

NEW:

```text
人工標籤中「不確定」「模糊」「無法對應」轉為配對資格的規則不在套件中，已由 V9 側車政策尋回（RECOVERED_FROM_SIDECAR_POLICY；V1.8.3 檔案 38），以獨立程式重算可重現側車的逐筆處理與配對資格變動，但屬事後尋回、非事前登記；側車產生程式已尋回（PROBABLE），產生敏感度表本身的程式仍未尋回；
```

### R34 — 附錄 E48 (v1.8.2 L3086 → v1.8.3 L3091)

Source: orchestrator triplet v1.8.3 (OUT 39 §3); OUT 38 §1, §2e–g, §3–§4 §2f

OLD:

```text
由作者補述傳播規則並提供重算程式後，移除第 3.7.4 節的 `[AUTHOR TO CONFIRM]`；若執行完整重分析（E40），須事先登記此規則 |
```

NEW:

```text
由研究者決定是否採用尋回的傳播規則（或另訂規則），事先登記並以雜湊承諾後，移除第 3.7.4 節的 `[AUTHOR TO CONFIRM]`；若執行完整重分析（E40），須以此登記的規則執行 |
```

## Verification summary (from verify_out_v183.json)

- `changed_lines_subset_of_patched_lines`: `True`
- `math_identical_ordered`: `True`
- `fenced_blocks_identical_except_listed_status_patches`: `True`
- `equation_tags_identical`: `True`
- `no_math_markers_in_patch_text`: `True`
- `headings_identical`: `True`
- `table_figure_captions_identical`: `True`
- `G_rows_identical_ordered`: `True`
- `G_token_count_unchanged`: `True`
- `GM_arrow_tokens_identical`: `True`
- `section_3_9_2_tables_3_4_3_4A_identical`: `True`
- `section_3_9_3_V1_design_identical`: `True`
- `section_3_9_4_identical`: `True`
- `section_3_9_5_identical`: `True`
- `section_3_12_enterprise_math_identical`: `True`
- `section_4_4_results_identical`: `True`
- `section_4_7_V1_results_identical`: `True`
- `count_unchanged_VCP`: `True`
- `count_unchanged_VSC`: `True`
- `count_unchanged_DL`: `True`
- `count_unchanged_NEV`: `True`
- `count_unchanged_Enterprise`: `True`
- `count_unchanged_SIMULATED_ONLY`: `True`
- `count_unchanged_EMPIRICAL RESULT PENDING`: `True`
- `count_unchanged_SUBMISSION_READY`: `True`
- `count_unchanged_UNIDENTIFIED`: `True`
- `count_unchanged_M1`: `True`
- `count_unchanged_M2`: `True`
- `count_unchanged_M3`: `True`
- `count_unchanged_M4`: `True`
- `count_unchanged_M5`: `True`
- `count_unchanged_REAL EVIDENCE`: `True`
- `count_unchanged_HUMAN_RESULT_PENDING`: `True`
- `no_stale_not_executable`: `True`
- `no_NOT_REQUIRED`: `True`
- `method_status_unchanged`: `True`
- `priority_status_unchanged_or_added`: `True`
- `numeric_patch_sum_matches_doc`: `True`
- `numeric_added_all_allowlisted`: `True`
- `numeric_removed_only_12`: `True`
- `no_result_like_tokens_added`: `True`
- `line_count`: `[3095, 3100]`
- `math_counts`: `{"$$": [18, 18], "$inline": [31, 31], "\\[\\]": [7, 7], "begin_env": [0, 0]}`
- `headings`: `[182, 182]`
- `G_table_rows`: `[36, 36]`
- `G_token_counts`: `[291, 291]`
- `fenced_patches`: `["R11"]`
- `fenced_blocks_changed`: `[1]`
- `term_NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET`: `[4, 0]`
- `term_EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION`: `[0, 4]`
- `term_REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION`: `[4, 4]`
- `term_NOT_RECOMMENDED`: `[4, 4]`
- `term_PRIORITY_RATIONALE_REVIEW_REQUESTED`: `[0, 1]`
- `term_RECOVERED_FROM_SIDECAR_POLICY`: `[0, 2]`
- `term_12 項未尋回`: `[4, 0]`
- `term_NOT_REQUIRED`: `[0, 0]`
- `term_AUTHOR TO CONFIRM`: `[2, 2]`

Notes:
- The only fenced block that changed is the §3.1.1 flow diagram (R11). It changes one status phrase: "目前無法執行" → "執行條件待滿足". With R11 reversed, every fenced block is byte-identical.
- The `[AUTHOR TO CONFIRM]` count is unchanged at 2. The §3.7.4 marker now asks whether the researcher adopts and predeclares the recovered rule, because predeclaration is still a researcher decision.
- No result number, G token or M token changed in count.
