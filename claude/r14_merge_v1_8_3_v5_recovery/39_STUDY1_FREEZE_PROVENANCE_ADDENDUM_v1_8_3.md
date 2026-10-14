# 39 — Study 1 Evidence Freeze: Provenance Addendum (V1.8.3)

Date: 2026-10-14. Branch: `research/v1.8.3-v5-recovery-verification-20261014`, base `5e170bc3f08132b3819c7b04fea98529747f103f`.

This is an **addendum** to `claude/r14_merge_v1_8_1_study1_freeze/17_STUDY1_EVIDENCE_FREEZE_v1.md` (sha256 `5c415af43e6c20b52c7356531d3d568f67abb436a748f5775c2a556136c98cff`). File 17 is not modified. Its successor hash ledger is `40_STUDY1_FREEZE_HASHES_v1_8_3.csv`, which replaces `18_STUDY1_FREEZE_HASHES.csv` (`0b63b362…8d99f`) for current use. File 18 itself stays unchanged.

**What this addendum changes:** provenance and status only. No number in 17 changes.

**What it does not change:**
- G01–G16;
- the 32-core membership (16 + 16);
- the taxonomy;
- any network value;
- the G→M assignment;
- the Enterprise v2.2 model;
- the V1 packet or S1 freeze.

No reanalysis, null model or pipeline stage was run.

```
STUDY1_EVIDENCE_FREEZE=READY (UNCHANGED; provenance strengthened)
SUBMISSION_READY=NO
```

## 0. Evidence files (this round, sha256)

| File | sha256 | Content |
|---|---|---|
| `35_V5_MANIFEST_CHAIN_VERIFICATION.md` | `8e64c1dc1913ed44ba5acf1e051b94d941322b6535e534a65f59533f37aaf25e` | V5 manifest chain: 201/203 claims verified, 15/15 links verified; the 2 mismatches are spreadsheet re-saves in the superseded 081003Z pack directory, off the core path |
| `35_V5_MANIFEST_CHAIN.csv` | `4a7b7df233919b1419aa12a8b1cb34dee13ca05e2491a4ccb494606439546bcf` | Machine-readable chain |
| `36_V5_BASELINE_RECOMPUTATION.md` | `4892eab9c6885b679331f8d760bb421a602403b966368435e23ef3f6c09e5c0f` | 76/76 MATCH, 0 CONFLICT |
| `36_V5_BASELINE_RECOMPUTATION.json` | `af7c7b0dfc202d7d17ae4f207dd704808094d2c00339e0664d20ae06d8682cbd` | Machine-readable |
| `37_PROTECTED_INPUT_RECOVERY.md` | `3f4f9d10c0cc2644cfe1e91a04ddea5edeed36f394bc5b5af65d45cc38da1d0f` | 37/37 protected inputs CONFIRMED; sidecar core CONFIRMED |
| `37_PROTECTED_INPUT_RECOVERY.csv` | `7b9723f7776fc1c31f43b9c91730b80b11fb0865a48a7af72912ad04ca4dc653` | One row per protected input |
| `38_FULL_REANALYSIS_FEASIBILITY.md` | `889695273ad7e0c37a400ce3a7dd9e93a250013ae1539021eb9b9f89b11241e1` | Execution feasibility; recovered propagation rule |
| `tools/Q/rule_check_result.json` | `f2c8ac16c43fc58767e061919407afcde8d0f60dceebac4a966a2c5bd5da485d` | Rule re-derivation: 50/50 actions, −18 |

V5 root: `C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\04_V5_PRODUCTION_FREEZE\20260911_AI_DECISION_V5_PRODUCTION`.

Sidecar root: `C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\01_V9_HUMAN_VALIDATION\20261003_V9_HUMAN_AUDIT_FINAL_CONVERGENCE_SIDECAR_20261003T192417`.

The `W:` prefix now means `C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\03_R14_STUDY1\01_SOURCE_CLOSURE_V1_8` (path map, 33 §2).

## 1. Provenance items: old status → new status

| # | Item | V1.8.1 status (17/18) | V1.8.3 status | Evidence (file + hash) |
|---|---|---|---|---|
| 1 | Official final core `FINAL_ROBUST_CORE_32.csv` | PROBABLE (reproduction only; 18 row `NOT_RECOVERED`) | **CONFIRMED** | See §1.1 |
| 2 | Real V5 Manuscript Data Pack | NOT_RECOVERED (`REAL_V5_DATA_PACK=NOT_RECOVERED`, 23 Debt C) | **RECOVERED** | See §1.2 |
| 3 | Protected inputs (V9 `PROTECTED_ARTIFACTS_BASELINE_20261003.csv`) | 12/37 NOT_RECOVERED (V1.8 02 §5; 17 §A, §D reason 1) | **37/37 CONFIRMED by full SHA-256** | See §1.3 |
| 4 | `HUMAN_AUDIT_APPEND_ONLY_LOG.csv`, protected state | Current hash ≠ protected hash. V9 `LEGACY_AUDIT_LOG_INTEGRITY=UNVERIFIED`; V1.8 wording "UNRESOLVED, not evidence of tampering" | **CONFIRMED: protected state verified as prefix of append-only log** | See §1.4 |
| 5 | Sidecar core `4e412a07…` | NOT_SHIPPED / NOT_RECOVERED (membership known only from the sensitivity CSV) | **CONFIRMED** | See §1.5 |
| 6 | Sidecar generator `prepare_and_run_corrected_sidecar.py` | NOT_RECOVERED | **PROBABLE** | See §1.6 |
| 7 | Label-propagation rule (E48) | `UNRESOLVED_MUST_BE_PREDECLARED` (15 §3) | **RECOVERED_FROM_SIDECAR_POLICY_PENDING_PREDECLARATION** | See §1.7 |
| 8 | Strict analytical records **6,499** | Taken from the manuscript; the upstream DB was NOT_RECOVERED, so not recomputed (17 §A) | **RECOMPUTED from V5 rows** | See §1.8 |
| 9 | Unique documents **783** | Taken from the V9 status file and manuscript; not recomputable from cell-level rows (17 §A) | **RECOMPUTED from V5 rows** | See §1.9 |
| 10 | 3,125 / 2,180 / 120 / 47 (34) / 32 = 16+16 / G01–G16 | Recomputed from V9 `official_*` columns | **Also recomputed from raw V5 rows; equal** | See §1.10 |
| 11 | `r14/04_G01_G16_FROZEN.csv` (prefix `ace53a780434c309`) and the R14 canonical docx as a named file | NOT_RECOVERED | **Unchanged: NOT_RECOVERED.** Outside this round's scope. A name search found no file. The R14 docx keeps its PROBABLE identity via `V9_FINAL_SUBMISSION_CANDIDATE_20261004.docx` (13; ledger row in 40) | — |

### 1.1 Official final core

- **Location:** `V5\13_RESULTS_FREEZE\results_freeze_v1_20260919T080120Z\FINAL_ROBUST_CORE_32.csv`.
- **Hash:** sha256 `a43b4b5897bb8b1dabfe251aa52b95da8f35b6951c98ada7c92663291770bd50`, the full recorded value. 7,705 bytes. It is listed in `FINAL_RESULTS_FREEZE_MANIFEST.json` (`f156f775…`).
- **Chain:** 13 → 14 is verified (35 §1–§2).
- **Copies:** 16 identical copies (37 §5).
- **Earlier run:** run 075633Z holds the same 32 cells and directions (35 §3).

### 1.2 Real V5 Manuscript Data Pack

- **Location:** `V5\14_MANUSCRIPT_DATA_PACK\data_pack_v1_20260922T010012Z`.
- **Manifest:** `MANUSCRIPT_DATA_PACK_MANIFEST.json` sha256 `28c5b631761d6522353cda2b3faa10ba1458f71e1a42b21c8a3e8249da7db4bf`. All 74/74 hash claims verify, and the sizes match.
- **Zip:** `AI_DECISION_V5_MANUSCRIPT_DATA_PACK_20260922T010012Z.zip` `fdf7cd89…`, with all members equal to the directory files (35 §1, §3).
- **Model digest:** the manuscript cites qwen2.5:14b with digest `7cdf5a01…22f6`. This digest equals `unique_model_digests` in the pack's `04_STAGE2_RUNTIME_SUMMARY.json` (`a4111914…`, manifest-listed).
- **Superseded pack (note):** `data_pack_v1_20260919T081003Z` is superseded. In its directory copy, 2 files were re-saved by a spreadsheet tool after packing: `26_OBSERVED_EXPECTED_RATIO_MATRIX_10X12.csv` (value-identical) and `33_EXACT_HYPERGEOMETRIC_RESULTS_120.csv` (max relative diff 5.0e-8). The 081003Z zip still holds the original bytes. Only 010012Z is cited, and nothing was modified.

### 1.3 Protected inputs

- **Count:** 36 rows match as whole files and 1 matches as a 355-byte prefix (37 §1–§5).
- **The 12 previously missing rows (now CONFIRMED):** 400 / 120 samples, `workbench.sqlite` (`367e588c…`), FSC stage-1 CSV, definitions, stage-2 sqlite (`cc425630…`), `LATEST_STAGE3_RESIDUAL_CLOSURE.txt`, `FINAL_RESULTS_FREEZE_MANIFEST.json`, `FREEZE_ROOT_SHA256.txt`, V9 camera-ready docx and PDF, and `SHA256SUMS.csv`. Their paths and hashes are in 40, layer `V9_PROTECTED_INPUT`.
- **FREEZE root:** recomputed, with 51/51 targeted files matching (37 §4).

### 1.4 HUMAN_AUDIT_APPEND_ONLY_LOG, protected state

- **Prefix match:** bytes 0–354 of the current 625-byte log (`151cf3d0…`) hash to the protected value `c958f8072c38…eca1`. They are the header plus event 1, `FIRST_CODER_50_FROZEN`. All 6 copies of the log carry this prefix (37 §3).
- **Status of V9's label:** V9's own `UNVERIFIED` label is historical. It is kept as V9 wrote it and is not rewritten.

### 1.5 Sidecar core

- **Location:** `SIDECAR\V5_CORRECTED\13_RESULTS_FREEZE\results_freeze_v1_20261003T115651Z\FINAL_ROBUST_CORE_32.csv`.
- **Hash:** sha256 `4e412a07af1f5c9e2f304408875fc1fc47018c9ff501a17dee437bea880e95a0`, equal to V9 `FINAL_STATUS.json` `sidecar_core_sha256`.
- **Contents:** 32 cells = 15 + 17, the same set as `sidecar_core_member=YES` (37 §6).

### 1.6 Sidecar generator

- **Location:** `SIDECAR\prepare_and_run_corrected_sidecar.py`, sha256 `021e3d10c8a1085bdae57df9a964a9416a61b4cf68acb1e33360448fd6463ef3`.
- **Why PROBABLE and not CONFIRMED:** its location and self-consistent outputs fit, but no V9 artifact pins the script's own hash (38 §2e). It was not executed.
- **Still not recovered:** the script that wrote `ROBUST_CORE_LOCAL_SENSITIVITY.csv`.

### 1.7 Label-propagation rule (E48)

- **Source:** `SIDECAR\LOCAL_HUMAN_CORRECTION_POLICY.md` (`33d4d44c…`, PROBABLE as a file). The generator's code lines 345–363 contain the same rule.
- **Re-derivation:** an independent stdlib re-derivation reproduces the sidecar's action for 50/50 records and the pair-eligible delta of −18 (38 §2f).
- **Still required:** researcher predeclaration and hash commitment before any rerun. Recovered is not the same as predeclared.

### 1.8 Strict analytical records 6,499

- **Source:** `ANALYTICAL_FREEZE_RECORD_LEVEL.csv` (`fbb5f592…`), with 6,499 unique `record_id`.
- **Cross-checks:** this set equals the canonical JSON (`9a4e8fc2…`, manifest-verified) and the production DB `passed_strict_filter=1` set (DB `367e588c…`). See 36 §A.

### 1.9 Unique documents 783

- **Result:** 783 distinct `document_id` among the 3,125 pair-eligible records in the same file (36 §A).

### 1.10 Other baseline numbers

- **Edges and cells:** M = 2,180, and the edge set equals the `DOCUMENT_PAIR_EDGES_DEDUP.csv` set (`3ba370c1…`). Per-cell O, E and O/E equal the frozen values.
- **Significance:** the BH re-adjustment of the frozen p values has max diff 0.
- **Core:** the core rule re-applied gives 32 = 16 + 16, and G01–G16 equals the V5 depleted set.
- **Totals:** 76/76 MATCH (36).
- **W columns:** the W `official_*` columns equal V5 exactly (36 §C).

## 2. Section-by-section effect on 17

| 17 section | Effect |
|---|---|
| §A table, "Verification" column | 6,499 and 783 change from manuscript/status-file sourced to **recomputed from V5 rows**. All other rows are additionally recomputed from raw V5 rows. **Values unchanged.** |
| §B human audit | Unchanged |
| §C local label sensitivity | The sentence "sidecar generator script is NOT_RECOVERED" is superseded. The generator is PROBABLE and the sidecar core is CONFIRMED. The 32 → 32 result, the 16/16 → 15/17 split and the +1/−1 changes are unchanged. G01–G16 removals: 0. There is no G17. |
| §D interpretation labels | Unchanged: LOCALLY_SENSITIVE / LOCALLY_STABLE / NOT_ESTABLISHED / TARGETED / DEFERRED |
| §D triplet and rationale | Execution status updated, and the rationale annotated (§3 below) |
| §E invalid claims, §F Study 2 boundary, §G | Unchanged. `STUDY1_EVIDENCE_FREEZE=READY` |

## 3. Full-reanalysis triplet (current)

```
FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION                         (unchanged)
FULL_REANALYSIS_EXECUTION_STATUS=EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION  (changed; was NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET)
FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED                                               (unchanged; researcher decision)
PRIORITY_RATIONALE_REVIEW_REQUESTED=YES
```

**Execution blockers (all three must clear before any rerun):**

1. **Propagation rule.** The researcher predeclares and hash-commits the propagation rule: either the recovered V9 rule (policy `33d4d44c…`) or another rule. The label input must be T4-exact, with its sha recorded (V1.8 07 §7.3; 15 §2).
2. **Baseline reproduction.** Path-patched copies of the stage 10–13 scripts go into a **new dated directory**, with the diff limited to `ROOT`; V5 is never written. These copies must reproduce the 13 pinned official outputs byte-for-byte (38 §2g):
   - `d816f34a`, `3ba370c1`, `ebac2b66`, `e5883e51`;
   - `682a58f7`, `e7019dfe`;
   - `8c0441ce`, `8538fc82`, `6b7c6e29`, `12e8b7e3`, `1e30bf06`;
   - `b1d8b5ee`, `a43b4b58`.
   The V9 2026-10-03 PASS predates the workspace move and was produced by a PROBABLE runner. It must be re-shown, not inherited.
3. **Researcher approval.** Required per V9 (`full_reanalysis_requires_researcher_approval=true`).

**Rationale for `NOT_RECOMMENDED`.** The five reasons are those of 17 §D / 15 §4.

| # | Reason | V1.8.3 |
|---|---|---|
| 1 | 12/37 protected inputs not recovered | **No longer holds.** All 37/37 are CONFIRMED. |
| 2 | The local sidecar shows G01–G16 unaffected | Holds, and is stronger: the sidecar core file is CONFIRMED (15/17; G01–G16 all remain core DEPLETED), and the rule re-derives −18 |
| 3 | A rerun adds reproducibility, not corpus-wide label validity | Holds |
| 4 | The real limitation is the small targeted sample with low agreement | Holds |
| 5 | A rerun remains a researcher decision | Holds |

The priority stays `NOT_RECOMMENDED`, because that is a researcher decision and was not changed by this round. Because reason 1 has lapsed, the researcher is asked to review the priority rationale (`PRIORITY_RATIONALE_REVIEW_REQUESTED`). This addendum does not write, and must never be read as, a "not required" status for the full reanalysis.

## 4. Manuscript

`41_MERGED_MASTER_THESIS_v1_8_3_V5_PROVENANCE_CANDIDATE.md` carries the same provenance and status changes. It makes 34 asserted-once replacements in provenance and status wording only. Math, headings, G rows, §3.9.2, §3.9.3, results and the Enterprise model are verified identical. See `41_PATCH_LOG_v1_8_3.md` and `41b_V182_TO_V183_SEGMENT_DIFF.md`.

## 5. Unchanged

```
G01_G16=UNCHANGED (set = V5 FINAL_ROBUST_DEPLETED; 16/16)
CORE_32=UNCHANGED (16 enriched + 16 depleted)
EXACT_32_CORE_STATUS=LOCALLY_SENSITIVE
G01_G16_STATUS=LOCALLY_STABLE
CORPUS_WIDE_HUMAN_VALIDITY=NOT_ESTABLISHED
TAXONOMY/NETWORK_VALUES/G_TO_M=UNCHANGED
ENTERPRISE_MODEL_CHANGED=NO
V1_S1_FREEZE=UNCHANGED_VALID
FULL_REANALYSIS_EXECUTED=NO
```
