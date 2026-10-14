# 41b — v1.8.2 → v1.8.3 segment diff

Input sha256 `2d493edc2e1884f05e5b0617bc56f1f85cdab0fa33531ac566b61d343dd8f159`. Output sha256 `0da8cec1521dbeff900ffa1fa9a1de0a31b0cdfa34b82c03531eba2111d7f740`.

- Changed lines in v1.8.2: [5, 13, 29, 122, 147, 158, 168, 405, 412, 591, 605, 609, 630, 651, 1629, 2185, 2192, 2240, 2364, 2368, 2380, 3033, 3050, 3077, 3078, 3082, 3086].
- Changed lines in v1.8.3: [5, 13, 29, 122, 147, 158, 168, 405, 412, 591, 605, 609, 630, 651, 1629, 2185, 2192, 2240, 2364, 2368, 2380, 3033, 3034, 3035, 3036, 3037, 3038, 3055, 3082, 3083, 3087, 3091].

## Invariants (script-verified; all must be `true`)

- changed_lines_subset_of_patched_lines: True
- math_identical_ordered: True
- fenced_blocks_identical_except_listed_status_patches: True
- equation_tags_identical: True
- no_math_markers_in_patch_text: True
- headings_identical: True
- table_figure_captions_identical: True
- G_rows_identical_ordered: True
- G_token_count_unchanged: True
- GM_arrow_tokens_identical: True
- section_3_9_2_tables_3_4_3_4A_identical: True
- section_3_9_3_V1_design_identical: True
- section_3_9_4_identical: True
- section_3_9_5_identical: True
- section_3_12_enterprise_math_identical: True
- section_4_4_results_identical: True
- section_4_7_V1_results_identical: True
- count_unchanged_VCP: True
- count_unchanged_VSC: True
- count_unchanged_DL: True
- count_unchanged_NEV: True
- count_unchanged_Enterprise: True
- count_unchanged_SIMULATED_ONLY: True
- count_unchanged_EMPIRICAL RESULT PENDING: True
- count_unchanged_SUBMISSION_READY: True
- count_unchanged_UNIDENTIFIED: True
- count_unchanged_M1: True
- count_unchanged_M2: True
- count_unchanged_M3: True
- count_unchanged_M4: True
- count_unchanged_M5: True
- count_unchanged_REAL EVIDENCE: True
- count_unchanged_HUMAN_RESULT_PENDING: True
- no_stale_not_executable: True
- no_NOT_REQUIRED: True
- method_status_unchanged: True
- priority_status_unchanged_or_added: True
- numeric_patch_sum_matches_doc: True
- numeric_added_all_allowlisted: True
- numeric_removed_only_12: True
- no_result_like_tokens_added: True

## Numeric tokens added / removed (whole document)

- Added: `{"1": 2, "13": 2, "2": 1, "256": 11, "3.7.1": 1, "3.7.4": 2, "3.8.3": 1, "35": 7, "355": 2, "36": 3, "37": 9, "38": 6, "39": 4, "4.5.5": 1, "40": 3, "41": 2, "5": 1, "5.8.9": 1, "74": 1}`
- Removed: `{"12": 5}`
- The per-patch deltas sum to the document delta: True.
- Added tokens outside the provenance allowlist: {}.

| Patch | Added | Removed | Justification |
|---|---|---|---|
| R02 | `{"256": 2, "35": 1, "38": 1, "37": 1, "39": 1, "40": 1}` | `{}` | "35", "38", "37", "39", "40" = V1.8.3 file IDs 35–38 and 39–40; "37" (also) = count of V9 protected inputs (provenance count, unchanged baseline size); "256" = SHA-256. |
| R03 | `{"256": 1, "13": 1}` | `{"12": 1}` | Removed "12" = superseded "12 of 37 missing" provenance count. Added "256" = SHA-256; "13" = number of hash-pinned official outputs to reproduce (OUT 38 §2g). "37" retained. |
| R05 | `{}` | `{"12": 1}` | Removed "12" = superseded "12 of 37 protected inputs are missing" (English abstract). "37" retained. |
| R12 | `{"355": 1, "256": 1, "37": 1}` | `{}` | "355" = byte length of the protected prefix of the append-only log (OUT 37 row 26); "256" = SHA-256; "37" = file ID 37. |
| R13 | `{"37": 1, "38": 1, "256": 1}` | `{}` | "37", "38" = V1.8.3 file IDs; "256" = SHA-256. |
| R14 | `{"256": 1}` | `{"12": 1}` | Removed "12" = superseded missing count. Added "256" = SHA-256. "37" retained. |
| R15 | `{"74": 1, "35": 1}` | `{}` | "74" = number of file-hash claims verified in the data-pack manifest (OUT 35 §1); "35" = file ID. The run id 20260922T010012Z is inside a single token (not split). "04_STAGE2_RUNTIME_SUMMARY" avoided as a token. |
| R16 | `{"256": 1}` | `{"12": 1}` | Removed "12" = superseded missing count. Added "256" = SHA-256. |
| R24 | `{"35": 2, "36": 2, "3.8.3": 1, "37": 3, "3.7.1": 1, "3.7.4": 2, "38": 2, "4.5.5": 1, "5.8.9": 1, "39": 2, "40": 2, "1": 1, "41": 2}` | `{}` | Appendix D: file IDs 35, 36, 37, 38, 39, 40, 41 (and "1" from `_v1_8_3` file-name tail); section cross-references 3.8.3, 3.7.1, 3.7.4, 4.5.5, 5.8.9. |
| R25 | `{"35": 1}` | `{}` | "35" = file ID. |
| R26 | `{"355": 1, "256": 1, "37": 1}` | `{}` | "355" = protected prefix length; "256" = SHA-256; "37" = file ID. |
| R27 | `{"37": 2, "256": 1, "35": 1, "36": 1}` | `{}` | "37" (x2) = protected-input count and file ID 37; "35", "36" = file IDs; "256" = SHA-256. Old "37" and "12" (historical V1.8 package statement) retained verbatim. |
| R28 | `{"256": 1}` | `{}` | "256" = SHA-256. |
| R29 | `{"35": 1, "39": 1}` | `{}` | "35", "39" = file IDs 35–39. |
| R30 | `{"256": 1, "13": 1, "38": 1, "1": 1, "2": 1, "5": 1}` | `{"12": 1}` | Removed "12" = superseded missing count. Added "256" = SHA-256; "13" = pinned official outputs; "38" = file ID; "1", "2", "5" = V1.8.1 reason numbers (reason 1 lapsed; reasons 2–5 hold). |
| R33 | `{"38": 1}` | `{}` | "38" = file ID. |

Every added number is one of the following:
- a file ID (35–41) or version label (1.8.2, 1.8.3);
- "256" from "SHA-256";
- a provenance count: 37 protected inputs, 13 pinned outputs, 74 data-pack hash claims, or the 355-byte prefix;
- a V1.8.1 reason number (1, 2–5);
- a section cross-reference.

The only number removed is the superseded "12" (×5), from "12 of 37 missing". The historical V1.8 package statement in E39 (b) keeps its "12".

No network, statistical, human-audit, synthetic or enterprise value was added or removed.

## Segment diff (changed lines only)

### v1.8.2 L5–5 → v1.8.3 L5–5 (replace)

- OLD: `2`
  NEW: `3`
- OLD: `1`
  NEW: `5`
- OLD: `∅`
  NEW: `OV`
- OLD: `FREEZ`
  NEW: `NANC`
- OLD: `1`
  NEW: `2`
- OLD: `1`
  NEW: `2`
- OLD: `∅`
  NEW: `v1.8.3 只更新來源與狀態描述，不改變任何數值、G 清單、V1 設計或企業模型：V5 正式生產資料夾已尋回，並以完整 SHA-256 與各階段清單鏈核對（V1.8.3 檔案 35–38）；正式凍結核心檔（FINAL_ROBUST_CORE_32.csv）的來源由「只以重現檔佐證」改為已確認（CONFIRMED）；V5 Manuscript Data Pack 已尋回；V9 受保護基準的 37 項輸入全數以完整 SHA-256 確認；文獻層證據凍結的數值不變，只強化其來源（V1.8.3 檔案 39–40）。`
- OLD: `但以目前的來源集無法`
  NEW: `其`
- OLD: `∅`
  NEW: `條件尚待滿足`
- OLD: `37 項受保護輸入中 12 項未尋回；NOT_`
  NEW: `∅`
- OLD: `W`
  NEW: `PEND`
- OLD: `∅`
  NEW: `NG_PROPAGA`
- OLD: `H`
  NEW: `ION`
- OLD: `C`
  NEW: `R`
- OLD: `R`
  NEW: `LE_AND_BASELINE_`
- OLD: `∅`
  NEW: `PRODUCTIO`
- OLD: `T_`
  NEW: `：37 項受保護輸入已全數以完整 `
- OLD: `OURCE_SET`
  NEW: `HA-256 確認，但須先由研究者事先登記並以雜湊承諾標籤傳播規則、在新的日期目錄中以僅修改路徑的程式複本重現 13 個雜湊釘定的正式輸出，並依 V9 經研究者核准`

### v1.8.2 L13–13 → v1.8.3 L13–13 (replace)

- OLD: `但以目前的來源集無法`
  NEW: `其`
- OLD: `∅`
  NEW: `條件尚待滿足（須先事先登記標籤傳播規則並重現正式基準）`

### v1.8.2 L29–29 → v1.8.3 L29–29 (replace)

- OLD: ` cannot be`
  NEW: `s`
- OLD: `∅`
  NEW: `ion is pending researcher predeclaration and hash commitment of the label-propagation rule, byte-for-byte reproduction of the pinn`
- OLD: `w`
  NEW: `off`
- OLD: `th`
  NEW: `cial baseline in`
- OLD: `ly`
  NEW: ` workspace, and`
- OLD: `∅`
  NEW: `sear`
- OLD: `∅`
  NEW: `her appr`
- OLD: `ered source set`
  NEW: `al`
- OLD: `12 of`
  NEW: `all`
- OLD: `∅`
  NEW: `now hash-confir`
- OLD: `issing`
  NEW: `ed`

### v1.8.2 L122–122 → v1.8.3 L122–122 (replace)

- OLD: `但以目前的來源集無法`
  NEW: `其`
- OLD: `∅`
  NEW: `條件尚待滿足（須先事先登記標籤傳播規則並重現正式基準）`

### v1.8.2 L147–147 → v1.8.3 L147–147 (replace)

- OLD: `以目前來源集無法`
  NEW: `∅`
- OLD: `∅`
  NEW: `條件待滿足（須先登記傳播規則並重現基準）`

### v1.8.2 L158–158 → v1.8.3 L158–158 (replace)

- OLD: `以目前來源集無法`
  NEW: `∅`
- OLD: `∅`
  NEW: `條件待滿足`

### v1.8.2 L168–168 → v1.8.3 L168–168 (replace)

- OLD: `但以目前的來源集無法`
  NEW: `其`
- OLD: `∅`
  NEW: `條件尚待滿足（須先事先登記標籤傳播規則並重現正式基準）`

### v1.8.2 L405–405 → v1.8.3 L405–405 (replace)

- OLD: `但以目前的來源集無法`
  NEW: `其`
- OLD: `∅`
  NEW: `條件尚待滿足（須先事先登記標籤傳播規則並重現正式基準）`

### v1.8.2 L412–412 → v1.8.3 L412–412 (replace)

- OLD: `目前無法`
  NEW: `∅`
- OLD: `∅`
  NEW: `條件待滿足`

### v1.8.2 L591–591 → v1.8.3 L591–591 (replace)

- OLD: `∅`
  NEW: `當時`
- OLD: `∅`
  NEW: `；此標記屬歷史紀錄`
- OLD: `∅`
  NEW: `）；v1.8.3 的核對顯示，受保護狀態與現行附加式日誌的前 355 位元組逐位元組相同（完整 SHA-256 相符），其後的位元組皆為附加的事件，符合附加式日誌的預期，即受保護狀態已確認為附加式日誌的前綴（V1.8.3 檔案 37`
- OLD: `。此為來源完整性的限制`
  NEW: `∅`

### v1.8.2 L605–605 → v1.8.3 L605–605 (replace)

- OLD: `∅`
  NEW: `替換後的核心檔、側車產生程式與其標籤處理政策不在 V9 套件內，`
- OLD: `∅`
  NEW: `已於 V9 側車資料夾尋回（V1.8.3 檔案 37–38）：替換後的核心檔以完整 SHA-256 確認；側車產生程式的位置與其輸出一致，但其本身的雜湊未由 V9 釘定（PROBABLE）；`
- OLD: `∅`
  NEW: `本身`
- OLD: `∅`
  NEW: `仍`
- OLD: `隨套件保存，`
  NEW: `尋回。`
- OLD: `無法`
  NEW: `已`
- OLD: `套件`
  NEW: `側車政策尋回（RECOVERED_FROM_SIDECAR_POLICY），以獨立程式重算可`
- OLD: `∅`
  NEW: `側車的逐筆處理與配對資格變動；此規則屬事後尋回，不是事前登記，若執行完整重分析，仍須由研究者事先登記並以雜湊承諾`
- OLD: `標籤至配對資格`
  NEW: `是否採用尋回`
- OLD: `與重算程式`
  NEW: `並事先登記`

### v1.8.2 L609–609 → v1.8.3 L609–609 (replace)

- OLD: `以目前的來源集無法`
  NEW: `其`
- OLD: `∅`
  NEW: `條件尚待滿足`
- OLD: `中`
  NEW: `已全數以完整`
- OLD: `1`
  NEW: `SHA-`
- OLD: `∅`
  NEW: `56`
- OLD: `項未尋回`
  NEW: `確認；須先事先登記標籤傳播規則並重現正式基準`

### v1.8.2 L630–630 → v1.8.3 L630–630 (replace)

- OLD: `以目前來源集無法`
  NEW: `∅`
- OLD: `∅`
  NEW: `條件待滿足（須先登記傳播規則並重現基準）`

### v1.8.2 L651–651 → v1.8.3 L651–651 (replace)

- OLD: `依專案紀錄的`
  NEW: `取自`
- OLD: `∅`
  NEW: `的`
- OLD: `資訊`
  NEW: `紀錄`
- OLD: `∅`
  NEW: `v1.8.3 已尋回 `
- OLD: `不在本稿工作環境`
  NEW: ` data_pack_v1_20260922T010012Z，其清單所列 74 個檔案雜湊全數相符，模型摘要值與其`
- OLD: `，投稿前須以原`
  NEW: `的 STAGE2_RUNTIME_SUMMARY 模型紀錄逐字相符；V1.8.3 `
- OLD: `核對`
  NEW: `案 35`

### v1.8.2 L1629–1629 → v1.8.3 L1629–1629 (replace)

- OLD: `以目前的來源集無法`
  NEW: `其`
- OLD: `∅`
  NEW: `條件尚待滿足`
- OLD: `中`
  NEW: `已全數以完整`
- OLD: `1`
  NEW: `SHA-`
- OLD: `∅`
  NEW: `56`
- OLD: `項未尋回`
  NEW: `確認，但須先事先登記標籤傳播規則並重現正式基準，且經研究者核准`
- OLD: `NOT_`
  NEW: `∅`
- OLD: `W`
  NEW: `PEND`
- OLD: `∅`
  NEW: `NG_PROPAGA`
- OLD: `H`
  NEW: `ION`
- OLD: `C`
  NEW: `R`
- OLD: `R`
  NEW: `LE_AND_BASELINE_`
- OLD: `∅`
  NEW: `PRODUCTIO`
- OLD: `T_SOURCE_SET`
  NEW: `∅`

### v1.8.2 L2185–2185 → v1.8.3 L2185–2185 (replace)

- OLD: `以目前來源集無法`
  NEW: `∅`
- OLD: `∅`
  NEW: `條件待滿足（須先登記傳播規則並重現基準）`

### v1.8.2 L2192–2192 → v1.8.3 L2192–2192 (replace)

- OLD: `以目前來源集無法`
  NEW: `∅`
- OLD: `∅`
  NEW: `條件待滿足（須先登記傳播規則並重現基準）`

### v1.8.2 L2240–2240 → v1.8.3 L2240–2240 (replace)

- OLD: `以目前來源集無法`
  NEW: `∅`
- OLD: `∅`
  NEW: `條件待滿足（須先登記傳播規則並重現基準）`

### v1.8.2 L2364–2364 → v1.8.3 L2364–2364 (replace)

- OLD: `NOT_`
  NEW: `∅`
- OLD: `W`
  NEW: `PEND`
- OLD: `∅`
  NEW: `NG_PROPAGA`
- OLD: `H`
  NEW: `ION`
- OLD: `C`
  NEW: `R`
- OLD: `R`
  NEW: `LE_AND_BASELINE_`
- OLD: `∅`
  NEW: `PRODUCTIO`
- OLD: `T_SOURCE_SET`
  NEW: `∅`

### v1.8.2 L2368–2368 → v1.8.3 L2368–2368 (replace)

- OLD: `∅`
  NEW: `受保護輸入已全數尋回，`
- OLD: `尋回缺件的受保護輸入`
  NEW: `事先登記標籤傳播規則並在現行工作環境重現正式基準`

### v1.8.2 L2380–2380 → v1.8.3 L2380–2380 (replace)

- OLD: `但以目前的來源集無法`
  NEW: `其`
- OLD: `∅`
  NEW: `條件尚待滿足（須先事先登記標籤傳播規則並重現正式基準）`

### v1.8.2 L3033–3033 → v1.8.3 L3033–3038 (replace)

- OLD: `本`
  NEW: `v1.8.3 的修訂底`
- OLD: `∅`
  NEW: `（已保存；未覆寫）`
- INSERTED: `\| v1.8.3／35–36 \| — \| `35_V5_MANIFEST_CHAIN_VERIFICATION.md`、`36_V5_BASELINE_RECOMPUTATION.md`（另有 .csv／.json） \| V5 正式生產資料夾的各階段清單鏈核對，以及由凍結原始列重算的文獻層基準（數值不變） \| 稿件狀態；第 3.8.3 節；附錄 E12、E39 \|`
- INSERTED: `\| v1.8.3／37 \| — \| `37_PROTECTED_INPUT_RECOVERY.md`（另有 .csv） \| V9 受保護基準 37 項輸入的尋回與完整雜湊確認；附加式日誌前綴核對；替換後核心檔的位置 \| 第 3.7.1、3.7.4 節；附錄 E39 \|`
- INSERTED: `\| v1.8.3／38 \| — \| `38_FULL_REANALYSIS_FEASIBILITY.md` \| 完整重分析的執行可行性；尋回的標籤傳播規則與側車產生程式 \| 第 3.7.4、4.5.5、5.8.9 節；附錄 E40、E48 \|`
- INSERTED: `\| v1.8.3／39–40 \| — \| `39_STUDY1_FREEZE_PROVENANCE_ADDENDUM_v1_8_3.md`、`40_STUDY1_FREEZE_HASHES_v1_8_3.csv` \| 文獻層（Study 1）證據凍結的來源補充與雜湊帳（凍結數值不變） \| 稿件狀態；附錄 E39、E40 \|`
- INSERTED: `\| v1.8.3／41 \| — \| `41_MERGED_MASTER_THESIS_v1_8_3_V5_PROVENANCE_CANDIDATE.md` \| 合併論文 v1.8.3（V5 來源版；只更新來源與狀態描述） \| 本稿 \|`

### v1.8.2 L3050–3050 → v1.8.3 L3055–3055 (replace)

- OLD: `∅`
  NEW: `（v1.8.3 已尋回 Data Pack 原檔並核對一致，V1.8.3 檔案 35）`

### v1.8.2 L3077–3078 → v1.8.3 L3082–3083 (replace)

- OLD: `∅`
  NEW: `屬歷史標記，`
- OLD: `∅`
  NEW: `）；v1.8.3 已確認受保護狀態為現行附加式日誌的前 355 位元組（完整 SHA-256 相符；V1.8.3 檔案 37`
- OLD: `∅`
  NEW: `；v1.8.3 已在工作環境的其他位置尋回全部 37 項並以完整 SHA-256 確認（V1.8.3 檔案 37）`
- OLD: `∅`
  NEW: `亦於 V5 正式生產資料夾尋回，並經 V5 各階段清單鏈核對確認（V1.8.3 檔案 35–36），不再`
- OLD: `套件內位元組相同的`
  NEW: `∅`
- OLD: `∅`
  NEW: `側車產生程式不在套件中，已於 V9 側車資料夾尋回：替換後的核心檔以完整 SHA-256 確認，側車產生程式為 PROBABLE（其雜湊未由 V9 釘定）；`
- OLD: `∅`
  NEW: `本身`
- OLD: `∅`
  NEW: `仍`
- OLD: `隨套件保存`
  NEW: `尋回`
- OLD: `∅`
  NEW: `，並與尋回的替換後核心檔一致`
- OLD: `∅`
  NEW: `c）已依 v1.8.3 的來源核對更新（V1.8.3 檔案 35–39），（`
- OLD: `，`
  NEW: `；`
- OLD: `NOT_`
  NEW: `∅`
- OLD: `W`
  NEW: `PEND`
- OLD: `∅`
  NEW: `NG_PROPAGA`
- OLD: `H`
  NEW: `ION`
- OLD: `C`
  NEW: `R`
- OLD: `R`
  NEW: `LE_AND_BASELINE_`
- OLD: `∅`
  NEW: `PRODUCTIO`
- OLD: `T_SOURCE_SET`
  NEW: `∅`
- OLD: `套件受保護基準 `
  NEW: `v1.8.3：`
- OLD: `∅`
  NEW: `受保護`
- OLD: `中`
  NEW: `已全數以完整`
- OLD: `1`
  NEW: `SHA-`
- OLD: `∅`
  NEW: `56`
- OLD: `項未尋回`
  NEW: `確認`
- OLD: `∅`
  NEW: `；尚待三項前置條件：研究者事先登記並以雜湊承諾標籤傳播規則、在新的日期目錄中以僅修改路徑的程式複本逐位元組重現 13 個雜湊釘定的正式輸出、依 V9 經研究者核准；V1.8.3 檔案 38`
- OLD: `∅`
  NEW: `；屬研究者決定。原理由 1「受保護輸入缺件」已不成立，理由 2–5 仍成立；已請研究者重新檢視此優先順序的理由：PRIORITY_RATIONALE_REVIEW_REQUESTED`
- OLD: `補回缺件的受保護輸入（E39（b））並`
  NEW: `∅`
- OLD: `∅`
  NEW: `並以雜湊承諾`
- OLD: `∅`
  NEW: `，並在現行工作環境重現正式基準`

### v1.8.2 L3082–3082 → v1.8.3 L3087–3087 (replace)

- OLD: `以目前來源集無法`
  NEW: `∅`
- OLD: `∅`
  NEW: `條件待滿足`

### v1.8.2 L3086–3086 → v1.8.3 L3091–3091 (replace)

- OLD: `∅`
  NEW: `不在套件中，已由 V9 側車政策尋回（RECOVERED_FROM_SIDECAR_POLICY；V1.8.3 檔案 38）`
- OLD: `及`
  NEW: `獨立程式重算可重現側車的逐筆處理與配對資格變動，但屬事後尋回、非事前登記；側車產生程式已尋回（PROBABLE），`
- OLD: `∅`
  NEW: `本身`
- OLD: `，`
  NEW: `仍`
- OLD: `隨套件保存而無法重現`
  NEW: `尋回`
- OLD: `作`
  NEW: `研究`
- OLD: `補述`
  NEW: `決定是否採用尋回的`
- OLD: `∅`
  NEW: `（或另訂規則），事先登記`
- OLD: `提供重算程式`
  NEW: `以雜湊承諾`
- OLD: `事先`
  NEW: `以此`
- OLD: `此`
  NEW: `的`
- OLD: `∅`
  NEW: `執行`

