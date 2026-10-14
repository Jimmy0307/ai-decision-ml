# 47 — Baseline Reproduction Report (V1.8.5, sub-agent S, Phase 3)

Date: 2026-10-14. Run timestamp: `20261014T041645Z`.

- **Mode:** a re-run of V5 stages 10–13 with the **ORIGINAL MODEL LABELS**.
  - No label substitution.
  - No model calls.
  - The revised analysis was **not** run.
- **Outputs:** `C:\NTUST_PAPER\outputs\00_CURRENT\06_COMPUTE_CLOSURE_V1_8_5\compute_closure\baseline_reproduction\20261014T041645Z\`. This is a new directory, outside git.

**Related files:**

| File | Content |
|---|---|
| 46 | Official 13 manifest |
| 48 | Per-output diff |
| 49 | Environment lock |
| 50 | Code diff |
| `tools\S\phase3_compare_summary.json` | Comparison summary |
| `tools\S\v5_untouched_check.json` | V5 untouched check |

## 1. Entry stage and why

**Entry stage = 10** (`DOCUMENT_DEDUP_10X12_MATRIX_ACCEPTED.py`). Stage 10 consumes the hash-verified stage-09 analytical freeze `analytical_freeze_v2_20260918T132206Z` as a fixed input.

**Why stage 09 (the analytical freeze built from the strict DB copy) is not re-run:**

1. **None of the 13 official outputs is a stage-09 output.** All 13 are produced by stages 10–13 (46). Stage 09's outputs reach them only as inputs, and those inputs are hash-pinned:
   - V5 09 manifest `69c7a7df…`, canonical `9a4e8fc2…`;
   - 10-manifest `source_analytical_freeze_sha256`;
   - 35 §2, 15/15 chain links.
2. **Stage 10 is the earliest stage at which labels enter the computation.** It is the only stage that reads the analytical freeze (§2 of 43). The approved rule substitutes labels on the stage-09 record rows by `record_id`, as in the reference implementation. So the label-dependent part of the pipeline that the rule changes runs from stage 10 onward.
3. **Stage 09 has never been demonstrated reproducible.** Re-running it is not needed by the approved propagation rule (38 §2g, last paragraph). Making it the entry stage would add a separate reproduction claim beyond the 13.

**The freeze input itself:**
- 7 files, copied from the WORK input copy.
- Hashes verified before the run and again after it (`post_run_freeze_input_hashes_ok = true`): `fbb5f592`, `9ee5fd53`, `9a4e8fc2`, `69c7a7df`, `7704e743`, `d53c5e95`, `e4d0a638`.
- Location: `WORK\run_inputs_baseline_20261014T041645Z\09_ANALYTICAL_FREEZE\`.

## 2. Run

| Stage | Script (patched copy; original sha) | Exit | Elapsed | Gates |
|---|---|---:|---:|---|
| 10 | `DOCUMENT_DEDUP_10X12_MATRIX_ACCEPTED.py` (`a3892528…`) | 0 | 0.4 s | DOCUMENT_DEDUP_10X12_MATRIX_ACCEPTED |
| 11 | `NULL_MODEL_NETWORK_ANALYSIS_ACCEPTED.py` (`cd96c48d…`): seed 20260918, 10,000 reps | 0 | 10.6 s | NULL_MODEL_NETWORK_ANALYSIS_ACCEPTED |
| 12 | `ROBUSTNESS_SENSITIVITY_ACCEPTED.py` (`7700d98c…`): document-null seed 20260919, 5,000 reps, burn-in 20/edge, thinning 2/edge | 0 | 60.3 s | ROBUSTNESS_SENSITIVITY_ACCEPTED |
| 13 | `FINAL_RESULTS_FREEZE_ACCEPTED.py` (`9af8c439…`) | 0 | 0.1 s | FINAL_RESULTS_FREEZE_ACCEPTED (23/23 checks PASS) |

**Environment.**
- Python 3.14.2 (CPython, `C:\Program Files\Python314\python.exe`) on Windows-11-10.0.26200, invoked as `python -I -B -X utf8`.
- Stdlib only.

**Code changes.** These are path-only: 5 lines in 4 hunks (50). All hash, count, seed and replicate gate constants are original, and every gate passed with them.

**Logs.** `WORK\logs\baseline_20261014T041645Z_stage{10,11,12,13}.log`. The run record is `WORK\baseline_20261014T041645Z_RUN_RECORD.json`.

## 3. Comparison of the 13 official outputs (48)

| ID | Output | Official sha256 (pin) | Reproduced sha256 | Byte | Rows | Schema | Sort | Keys | Numeric diffs | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | matrix canonical | d816f34a…71b5 | d816f34a…71b5 | = | 15,650 paths | = | = | = | 0 | BYTE_IDENTICAL |
| 02 | dedup edges | 3ba370c1…15a2 | 3ba370c1…15a2 | = | 2,180 | = | = | = | 0 | BYTE_IDENTICAL |
| 03 | document count matrix | ebac2b66…ec46 | ebac2b66…ec46 | = | 11 | = | = | = | 0 | BYTE_IDENTICAL |
| 04 | raw count matrix | e5883e51…a938 | e5883e51…a938 | = | 11 | = | = | = | 0 | BYTE_IDENTICAL |
| 05 | null canonical | 682a58f7…9b66 | 682a58f7…9b66 | = | 2,769 paths | = | = | = | 0 | BYTE_IDENTICAL |
| 06 | main null 120 | e7019dfe…4d1f | e7019dfe…4d1f | = | 120 | = | = | = | 0 | BYTE_IDENTICAL |
| 07 | robustness canonical | 8c0441ce…9993 | 8c0441ce…9993 | = | 129 paths | = | = | = | 0 | BYTE_IDENTICAL |
| 08 | exact 120 | 8538fc82…2516 | 8538fc82…2516 | = | 120 | = | = | = | 0 | BYTE_IDENTICAL |
| 09 | document null 120 | 6b7c6e29…0f0b | 6b7c6e29…0f0b | = | 120 | = | = | = | 0 | BYTE_IDENTICAL |
| 10 | raw-record exact 120 | 12e8b7e3…5051 | 12e8b7e3…5051 | = | 120 | = | = | = | 0 | BYTE_IDENTICAL |
| 11 | comparison 120 | 1e30bf06…cbf5 | 1e30bf06…cbf5 | = | 120 | = | = | = | 0 | BYTE_IDENTICAL |
| 12 | results canonical | b1d8b5ee…74d0 | b1d8b5ee…74d0 | = | 425 paths | = | = | = | 0 | BYTE_IDENTICAL |
| 13 | official final core | a43b4b58…bd50 | a43b4b58…bd50 | = | 32 | = | = | = | 0 | BYTE_IDENTICAL |

Full 64-hex values are in 48 and 46.

**Non-identical outputs:** none. No classification (PATH_ONLY_METADATA / NON_SEMANTIC_SERIALIZATION / SORT_ORDER_ONLY / NUMERIC_DIFFERENCE / LOGIC_DIFFERENCE) applies, and no exception was needed or approved.

**Non-pinned side files (informational, not among the 13).**
- 27 other files sit in the same 4 stage directories.
- 23 are byte-identical to V5.
- The 4 stage manifests (`DOCUMENT_DEDUP_MATRIX_MANIFEST.json`, `NULL_MODEL_NETWORK_MANIFEST.json`, `ROBUSTNESS_SENSITIVITY_MANIFEST.json`, `FINAL_RESULTS_FREEZE_MANIFEST.json`) differ.
  - Flattened field comparison shows the differences are only `generated_utc` and `lineage.*` absolute path fields: 4, 4, 3 and 6 differing keys respectively, and 0 non-path, non-time differences.
  - This class would be PATH_ONLY_METADATA, but these files are not among the 13.

**Implied 120-cell results.** These are bytes-identical to the official files:

| Method | q ≤ .05 | q ≤ .01 |
|---|---:|---:|
| Main | 47 | 34 |
| Exact | 46 | 34 |
| Document-preserving | 32 | 27 |
| Raw-record | 54 | 48 |

Core = 32 = 16 enriched + 16 depleted.

## 4. V5 untouched check

- **Method.** All files under V5 were recomputed after the run and compared with `WORK\V5_PRE_RUN_SNAPSHOT.sha256` (sha256 `ac40ed93…9677`, 1,217 entries).
- **Result.** 1,217 files: 0 changed, 0 missing, 0 added. **`V5_UNTOUCHED=YES`**.
- **No writes elsewhere.** Nothing was written into V9, SIDECAR or FREEZE. Every input was read from the WORK copies (`inputs_S_20261014T040934Z`; 92/92 copy hashes equal the source hashes).

## 5. Status

```
ENTRY_STAGE=10 (stage-09 analytical freeze used as hash-pinned input; justification §1)
CODE_EDITS=PATH_ONLY (5 lines, 4 hunks)
SEEDS_REPS=20260918/10000 (main), 20260919/5000 (document null) — unchanged
V5_UNTOUCHED=YES (1217/1217, 0 changed/missing/added)
REVISED_ANALYSIS_RUN=NO
STOP=NONE
BASELINE_REPRODUCTION=PASS
OFFICIAL_13=13/13
BYTE_IDENTICAL=13/13
```
