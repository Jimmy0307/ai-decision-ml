# 06 — Source flag inventory and closure (Phase 7, sub-agent E)

Scope: v1.7 manuscript `r14_merge_v1_7/130_…_v1_7_EVIDENCE_CONVERGED_CANDIDATE.md` plus artifacts 128–137 (.md/.csv) in the same folder. Every flag was checked against the V9 package `W/02_V9_HUMAN_VALIDATION/20260929_V9_HUMAN_VALIDATION/`. The full record is `W/06_SOURCE_FLAG_CLOSURE.csv` (275 rows).

## 1. Method

1. **Flag extraction.** `extract.py` scanned every line of 128–137 (.md/.csv). It searched for the requested patterns, case-insensitive: pending verification / 待核 / 待確認 / 待驗證 / source unavailable / artifact missing / 2026-09-29 / 20260929 / not available in this package / not shipped / unverified / TODO / TBD / [VERIFY / pending. It also searched for every variant of the v1.7 V9 provenance flag: `〔來源：2026-09-29 …附錄 E39〕`, `〔2026-09-29 紀錄，待核〕`, `〔變動依 2026-09-29 紀錄，待核〕`, the English "as reported in the 2026-09-29 validation record, pending verification", `[SOURCE: V9 …]` (128 L44 only), `[AUTHOR TO CONFIRM…]`, 依作者回報, 不在本稿工作環境中, 缺件, ABSENT, USER-REPORTED and 使用者陳述.
   - Each output row is one (file, line, flag phrase).
   - The section is the nearest preceding markdown heading, or the CSV G-row ID for 132.
   - Six extra rows were added by hand for claims that carry no literal flag. These are L5 (50/20/19), L1629, L2268 and L2376 (wording), L3064 (E40), and the second half of 137 P0-1 (Drive).
2. **Hash checks.** `verify.py` computed the sha256 of every V9 file used and compared it with `W/01_FILE_INVENTORY.csv`, `FINAL_ARTIFACT_HASH_MANIFEST.csv`, the package `*.sha256`/`*SHA256.txt` files and the snapshot hashes inside `FINAL_STATUS.json`. All cited files match the inventory.
   - The core files also match the manifest, the `.sha256` side files and `FINAL_STATUS.json`: FIRST_CODER_50_FINAL_FROZEN dd332dd8…, BLIND_REPEAT_20_FINAL_FROZEN 6afc8d7a…, HUMAN_RECONCILED_20 4b7ceac2…, HUMAN_RELIABILITY_FINAL ef7e5544…, ROBUST_CORE_LOCAL_SENSITIVITY.csv e3166ee1…, _DIFF.csv f6607aae…, .md b25b9a84…, FINAL_STATUS.json d9226d31…, FINAL_ERROR_TAXONOMY(.csv/_CASES) 68e97c01…/8949b671….
   - The V9 zip itself is recorded in `W/00_INPUT_MANIFEST.csv` with sha 8f63e88e….
3. **Row-level value checks.** The checks used scripts only, not summary prose. Results are in `verify_out.json`.
   - **Coder counts:** 50 first-coder rows, 50 unique, 50 complete. The blind file has 20/20 complete, and its records are a subset of the 50. The reconciled file has 20 rows; 19 have at least one field in disagreement and 1 agrees fully; 19 have reconciliation event IDs.
   - **Kappa:** Cohen's κ was recomputed from the raw FIRST_C*/BLIND_C* columns: .5614 / .1798 / .0476 / .1398 / .3162, with agreement 15/7/4/4/12. This equals HUMAN_RELIABILITY_FINAL.csv.
   - **Robust core:** the 120-row sensitivity table gives official core 32 (16 enriched / 16 depleted) and sidecar core 32 (15 / 17). The 31 shared pairs have 0 direction changes. Only 2 of 120 rows have core_membership_changed=YES.
     - Gained: HUMAN_AUGMENTATION × RISK_ASSESSMENT (depleted).
     - Lost: COORDINATION_EXECUTION × GENERAL_DECISION_PROCESS (enriched).
   - **Core rule:** recomputing "q ≤ .05 and same direction in main + exact + document-preserving (+ raw)" from the q-values reproduces both core sets exactly.
   - **G01–G16:** the 16 cells equal the official depleted core. All 16 are in the sidecar core and still depleted. The O values in 132 equal V9 official_observed.
   - **Model vs first coder (n=50):** relation 14, AI family 19, decision family 9; inclusion 33 of 42, with 9 cases where the model included and the human excluded, and 0 reverse cases.
   - **E49:** in the V9.1 segmentation sidecar (S1 and S2), all 22 UNCHANGED_FROZEN rows of the audited records keep the model families: 22/22 equal the model family and 0/22 equal the human family.
4. **Duplicate formats** (`dupcheck.py` plus an openpyxl read):
   - The 130 `.docx` carries exactly the same flag counts as the `.md` (for example 14 `〔2026-09-29 紀錄，待核〕`, 4 long V9 flags, 2 AUTHOR TO CONFIRM, 69 / 46 EMPIRICAL / HUMAN RESULT PENDING). It duplicates the md and must be regenerated from the v1.8 md.
   - Sheet `G_to_M_matrix` of the 132 `.xlsx` is a 17×27 duplicate of the CSV, with only float-precision differences in the E column. It contains the same 16 V9 flags.
5. **Closure rule.** CLOSED_SOURCE_VERIFIED required three things: the file exists, its hash matches the inventory/manifest, and the specific value matches at row level. Values that exist only in summary md/json (replacement scope, seeds) were left OPEN_NEEDS_PHASE4.

**Scripts** (reproducible; run with `python -I`), in `C:\Users\user\AppData\Local\Temp\claude\C--NTUST-PAPER\b2185478-fbc8-4bee-8105-bb5557dd964b\scratchpad\v18\E\`:
- `extract.py`
- `verify.py` → `verify_out.json`
- `build.py` (holds the explicit status rules)
- `dupcheck.py`
- `v9claims.py`

## 2. Counts by status (275 rows)

| new_status | all files | 130 only | V9-related rows (excluding 129 history) |
|---|---:|---:|---:|
| CLOSED_SOURCE_VERIFIED | 81 | 34 | 81 |
| OPEN_VALUE_MISMATCH | 11 | 9 | 10 + 1 (L2376) |
| OPEN_NEEDS_PHASE4 | 6 | 4 | 6 |
| OPEN_SOURCE_NOT_FOUND | 12 | 7 | 3 (Data Pack digest, Drive) |
| KEEP_AS_LIMITATION | 124 | 112 | 3 (full reanalysis E40, E44 remainder) |
| NOT_A_FLAG | 41 | 5 | 1 |

- **KEEP_AS_LIMITATION** rows are almost all `[EMPIRICAL RESULT PENDING]` (enterprise data V0/V2/V7 not collected) and `[HUMAN RESULT PENDING]` / V1 / EA-X / ORG-V human coding. These are genuinely unavailable and outside V9 scope.
- **NOT_A_FLAG** rows are all of 129, because it is a historical delta log whose live flags sit in 130. They also include marker legends (130 L168, L1372, L2668, L3080; 133 L48/L51; 136 L62), the 135 parser note and 134 rule text.
- **Non-V9 open items:**
  - EUR-Lex 2026/1744 `[VERIFY]` at L2594.
  - Reference UNVERIFIED entries N6, N35, N66 at L2683, L2712, L2743; E36 at L3045 and L3060.
  - Submission-format templates (128 L16, 137 L22).
  - Legacy 完整資料來源 at 128 L15. It now exists in W/03 but was not examined by E.

## 3. Lines in the v1.7 .md to edit in v1.8 (provenance or flag wording only)

These edits change no number, equation, G01–G16, taxonomy or result. Standard replacements:
- **(A) Long flag**
  - Old: `〔來源：2026-09-29 人工驗證狀態紀錄（檔名 20260929_V9_HUMAN_VALIDATION；V9 是檔案版本名，不是驗證閘門）；原始檔案未在本稿工作環境中，投稿前須逐項核對；附錄 E39〕`
  - New: `〔來源：V9 人工驗證套件（資料夾 20260929_V9_HUMAN_VALIDATION；V9 是檔案版本名，不是驗證閘門）之 FINAL_STATUS.json（驗證時間 2026-10-03）與 ROBUST_CORE_LOCAL_SENSITIVITY.csv；已逐列核對；附錄 E39〕`
- **(B) Short flag**
  - Old: `〔2026-09-29 紀錄，待核〕` and `〔變動依 2026-09-29 紀錄，待核〕`
  - New: `〔V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv，已逐列核對〕`

| v1.7 line | Section | Change |
|---|---|---|
| 5 | 稿件狀態 | (A) |
| 13 | 摘要 | (B) |
| 15 | 摘要 | (B) |
| 29 | Abstract | "as reported in the 2026-09-29 validation record, pending verification" → "verified row by row against the V9 validation package" |
| 158 | 1.5 | (A) |
| 591 | 3.7.1 | 「狀態紀錄日期 2026-09-29」→「V9 套件 FINAL_STATUS.json，驗證時間 2026-10-03」. 「依該紀錄的整理，分歧可能來自四類來源…〔2026-09-29 紀錄，待核〕」→「依 V9 錯誤型態表（FINAL_ERROR_TAXONOMY.csv）對模型標籤與人工標籤差異所作的詮釋性整理（非裁決），分歧可能來自四類主要來源…」 Keep 「19 筆分歧尚未逐筆依這四類來源歸類」(true). |
| 605 | 3.7.4 | 「依作者回報」→「依 V9 套件紀錄（ROBUST_CORE_LOCAL_SENSITIVITY.md、FINAL_STATUS.json）」. `[AUTHOR TO CONFIRM：2026-09-29 人工驗證紀錄；附錄 E48]` → `[程序細節見 V9 ROBUST_CORE_LOCAL_SENSITIVITY.md；逐列重現待完成；附錄 E48]`. Replace fully only after Phase 4 row-reproduces scope and seeds. |
| 607 | 3.7.4 | 「兩者的處理範圍可能部分重疊——…須以補充資料 S10 與 2026-09-29 紀錄核對（附錄 E49）」→「兩者的標籤處理範圍不重疊：重切分設定沒有把任何人工標籤傳播至受稽核或未稽核記錄，人工稽核的錯誤標記只用於強制納入重切分候選（V9.1 重切分記錄層級檔與最終報告；附錄 E49）」. Keep 「不是事前登記」. |
| 609 | 3.7.4 | 「來自 2026-09-29 的人工驗證狀態紀錄」→「來自 V9 人工驗證套件的 FINAL_STATUS.json」, plus (A) |
| 619 | 3.8.1 | 「L2′ 依作者回報推得，待核」→「L2′ 取自 V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv（已逐列核對）」 |
| 630 | 表 3-3 | 「（依作者回報；判準待核）」→「（判準同 L2）」; 「32（若無其他未回報的變動，推得 15／17：…）」→「32（15／17：+1 不足、−1 過度）」; (B) |
| 645 | 3.8.2 規則 6 | (B) |
| 716 | 3.9.2 表註 | (B) |
| 1559 | 4.5.1 | Same four-source rewording as L591 |
| 1629 | 4.5.5 | 「以人工調和後的標籤替換」→「以人工標籤（研究者審閱或調和後的標籤）替換」 (V9 used 20 reconciled + 30 first-coder labels), plus (A) |
| 1638 | 表 4-9A 註 | 「表中只列作者回報發生變動的配對；若無其他未回報的變動，替換後集合推得為…」→「表中列出 120 格逐列比對下全部發生成員變動的配對；替換後集合為 15 組過度呈現與 17 組不足呈現，凍結核心其餘 31 組成員與方向皆不變」, plus (B) |
| 1640 | 4.5.5 | 「依作者回報的變動（若無其他未回報的變動），」→「依 V9 套件的逐列結果，」 |
| 2183 | 4.11 表 | (B) |
| 2206 | 5.1 | (B) |
| 2262 | 5.4.2 | Same four-source rewording; drop 〔…待核〕 |
| 2268 | 5.4.2 | 「以人工調和標籤替換」→「以人工標籤（研究者審閱或調和後）替換」; 〔變動依 2026-09-29 紀錄，待核〕→ (B) |
| 2362 | 5.8.9 | (B); 「兩者的處理範圍是否部分重疊，待核（附錄 E49）」→「兩者的標籤處理範圍不重疊（附錄 E49 已核）」 |
| 2376 | 5.10 | 「人工稽核再指出，編碼分歧同時來自…」→「人工稽核提示，編碼分歧可能同時來自…」 (not flagged in v1.7; stronger than V9's "interpretive hypothesis") |
| 2378 | 5.10 | (B) |
| 2664 | 附錄 A S8 | 「（V9，2026-09-29；待以原始檔案核對，附錄 E39）」→「（V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv／_DIFF.csv／.md；已核，附錄 E39）」. S8 must actually ship these files. |
| 3008 | 附錄 D | 「（不在本稿工作環境中）」→「（已納入工作環境；SHA-256 8f63e88e…）」; 「待核對（附錄 E39）」→「已核對（附錄 E39）」 |
| 3063 | E39 | Rewrite as resolved: originals obtained and checked row by row. All items match: 2 changed pairs, 32 = 15/17, 31 unchanged, no other change, status flags, 50/20/19, κ. Record the residual: FINAL_STATUS `protected_hash_mismatches` on HUMAN_AUDIT_APPEND_ONLY_LOG.csv and LEGACY_AUDIT_LOG_INTEGRITY=UNVERIFIED. The frozen 50/20/19 files' hashes are intact. |
| 3068 | E44 | Delete the component 「2026-09-29 人工驗證原始檔案待核（E39）、」. Keep the rest (SUBMISSION_READY=NO, which agrees with FINAL_STATUS submission_ready=false). |
| 3072 | E48 | 「依 2026-09-29 原始紀錄逐項填入 `[AUTHOR TO CONFIRM]`」→「程序細節已見 V9 ROBUST_CORE_LOCAL_SENSITIVITY.md（20 筆調和標籤＋其餘第一位編碼者標籤；未稽核記錄不變；種子與重複次數見該檔）；逐列重現待 Phase 4」 |
| 3073 | E49 | Mark resolved, with the wording from L607 |
| 651 (non-V9) | 3.8.3 | Optional: 「（同一摘要值、Q4_K_M、temperature 0、seed 20260909、num_ctx 8192 亦見於 V9.1 重切分 Stage-2 模型驗證紀錄；主分析 Data Pack 原檔仍待核）」 |

**Artifacts:**
- 132 .csv and .xlsx: replace 16× `目標式人工標籤替換：未移除〔2026-09-29 紀錄，待核〕` with `…：未移除〔V9 套件，已逐列核對〕`.
- 128 L14/L29/L44/L53/L64/L73, 131 L40–53/L97/L104/L145, 133 L34 and 137 P0-1/L35 are superseded. Mark the V9 package as present and verified.
- 131 L53 still needs the four-source scope correction.

**Not a flag, but an author choice:** L1640 says R14 did not report document-preserving p_BH for the two changed pairs. V9 rows contain them: official document q = .0567 for HUMAN_AUGMENTATION × RISK_ASSESSMENT and .0435 for COORDINATION_EXECUTION × GENERAL_DECISION_PROCESS. Adding them would be new numbers, so this is left to the author and Phase 4.

## 4. Every v1.7 statement about V9 human-validation status, checked against raw V9 rows

**Consistent:**

| Line(s) | Content | Basis in raw V9 rows |
|---|---|---|
| 5 | 50/50, 20/20, 19/19; 32 retained, local change; full reanalysis pending; 16/16 | rows + FINAL_STATUS |
| 13 | κ .561 and .048–.180; 19 disagreements all reconciled; +1 depletion −1 enrichment, 32 retained | rows |
| 15, 31, 356, 645, 716, 2238 | G01–G16 none removed; extra depletion outside G | row-level |
| 29 | 50/20/19; κ .561, .048–.180; membership change; 16+16 | rows |
| 105, 112, 122, 147, 405, 412, 1625, 2190 | Generic "local membership sensitivity; full reanalysis pending" | FINAL_STATUS: LOCAL_SENSITIVITY_CHANGED / FULL_REANALYSIS_REQUIRED |
| 158, 2183, 2206, 2378 | +HUMAN_AUGMENTATION × RISK_ASSESSMENT depleted / −COORDINATION_EXECUTION × GENERAL_DECISION_PROCESS enriched; 16/16 | row-level |
| 591 | 400/120 → 50/20, not preregistered; 19 of 20 disagree; rates 75/35/20/20/60% | HUMAN_AUDIT_STATUS original targets 400/120 and preregistered_stopping_rule=false; rows |
| 601 | R14 statement that reconciled labels are not propagated in re-segmentation | V9.1 report and rows |
| 605 | "研究者審閱或調和後的標籤" | Consistent with V9 scope (20 reconciled + 30 first-coder), which is json/md only → PHASE4 |
| 609, 1629 (status flags) | Status flags | FINAL_STATUS decision_text |
| 619, 630, 1638, 1640 | 32 = 15/17; 31 unchanged; no other change | row-level |
| 632 | L2′ does not replace L2 | (interpretation, consistent) |
| 1557 | 14/50, 19/50, 9/50; 33/42; 9 model-include / human-exclude; 0 reverse | first-coder rows |
| 1567–1571 (表 4-6) | Agreement and κ | Recomputed from rows |
| 1567–1571 (表 4-6) | Bootstrap CIs [.242,.841], [−.081,.429], [−.081,.176], [−.027,.314], [.015,.623] | Equal HUMAN_RELIABILITY_FINAL.csv; bootstrap not re-run → PENDING_PHASE4 |
| 1573 | 20,000 bootstrap replicates | kappa_valid_bootstrap_replicates = 20000 |
| 1635–1636 | HUMAN_AUGMENTATION × RISK_ASSESSMENT main q < .001 and not in the official document-preserving set; COORDINATION_EXECUTION × GENERAL_DECISION_PROCESS O = 19, * tier | official main q = .00092 / doc q = .0567; observed 19, main q = .0167 |
| 2262, 2324, 2326 | κ .561/.180/.048/.140/.316; 20% family agreement; 400/120 → 50/20; 19 reconciled | rows |
| 2268 | "19 筆文獻層級邊" | official_document_observed = 19 |
| 2362 | 50 records concentrated in the robust-core-related stratum | all 50 rows stratum = A; FINAL_STATUS "TARGETED_ROBUST_A_AUDIT" |

**Inconsistent or partial** (all wording or provenance, no number wrong):
- **L591, L1559, L2262, L2376, 131 L53 — scope of the four-source attribution.** V9 attributes the four likely sources to model-vs-human label differences. They are an interpretive hypothesis, not adjudication, and V9 adds a fifth class, TRUE_CONCEPTUAL_AMBIGUITY. V9 does not attribute them to the 19 coder-vs-coder disagreements. L2376 states the attribution as fact.
- **L591 — status date.** The manuscript says 2026-09-29. The raw dates are freeze 2026-10-02T19:49Z, reconciliation 2026-10-03T07:45–11:09Z and FINAL_STATUS 2026-10-03T12:23Z.
- **L1629, L2268 — "以人工調和後的標籤".** V9 used reconciled labels for 20 records and first-coder labels for 30.
- **L3063 (E39) — "只來自作者 2026-10-13 的陳述".** Now superseded by the raw files.

## 5. Residual observations (no STOP condition)

- None of the 50/20/19 counts, κ values, 32 / 16-16 / 15-17, the two changed pairs or G01–G16 conflict with raw rows. **No STOP condition.**
- **Stale intermediate files must not be cited as authoritative.** `HUMAN_AUDIT_STATUS.json` says ADJUDICATION WAITING and `HUMAN_RECONCILIATION_GATE_STATUS.json` says completed 0/19. Both are earlier snapshots superseded by `FINAL_STATUS.json` and HUMAN_RECONCILED_20.csv.
- **Stale hash note.** `SECOND_CODER_BLIND_20_SHA256.txt` lists C55FF2C8… (the save-bug pre-state), while the current SECOND_CODER_BLIND_20.csv = BLIND_REPEAT_20_FINAL_FROZEN.csv = 6afc8d7a…. The frozen file's hash agrees with the manifest and FINAL_STATUS.
- **Integrity limitation.** FINAL_STATUS reports one protected-hash mismatch: HUMAN_AUDIT_APPEND_ONLY_LOG.csv, expected c958f807…, current 151cf3d0…. The legacy audit-log integrity is UNVERIFIED with no tampering found. Disclose this as a limitation in E39 or 3.7.1.
- **Kappa cross-check.** E's recomputed κ is unweighted Cohen's κ on exact label strings. Phase 4's independent recomputation should be compared. The CSV marks these rows "YES_BY_E; PHASE4_CROSSCHECK_PENDING" in notes.
