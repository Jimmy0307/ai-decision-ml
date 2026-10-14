# 50 — Baseline Code Diff (V1.8.5, sub-agent S, Phase 3)

Date: 2026-10-14. Run `20261014T041645Z`.

| Item | Location |
|---|---|
| Original scripts | WORK copies of `V5\work\stage2_strict_v102\` |
| Byte copies of the originals | `WORK\code_baseline_20261014T041645Z\original\` |
| Patched copies (these ran) | `WORK\code_baseline_20261014T041645Z\patched\` |
| Raw diff files | `WORK\code_baseline_20261014T041645Z\diffs\*.diff` |

**How the patch was made.** Patching was mechanical, done by `tools\S\s_phase3_run_baseline.py`: an exact byte replacement of one literal per script, plus one block in stage 10. Before replacing, the script asserted that each target occurs exactly once.

**Preserved and untouched:**
- the scripts' CRLF line endings;
- every hash/count gate constant;
- seeds, replicate counts, MCMC controls, BH and the promotion rule.

These are unlike the V9 sidecar runner, which also rewrote the gate hashes onto one line.

| Script | Stage | Original sha256 (= FREEZE SHA256SUMS = sidecar run record) | Patched sha256 | Hunks | Lines changed |
|---|---|---|---|---:|---:|
| `DOCUMENT_DEDUP_10X12_MATRIX_ACCEPTED.py` | 10 | `a3892528ecac135839681429916d8d6607f1ef4685456d9663373b49a1175cd7` | `7452c31ae1d6783719c9a778da37250b0f450c8dce483573c69768821d5526db` | 1 | 2 |
| `NULL_MODEL_NETWORK_ANALYSIS_ACCEPTED.py` | 11 | `cd96c48d685fe05d23d526638bf3d0ab7201a115f3c9cab0d908277c1d0b12e3` | `a85b8dde93a6f8b2c35722418f843710ee7f0d014d3b4ac15f6fee3908b52017` | 1 | 1 |
| `ROBUSTNESS_SENSITIVITY_ACCEPTED.py` | 12 | `7700d98c934db95ff28dc7aba19be1ce6558fff2957bc79bff54f63a63087c19` | `ba248d82a64a562607390a308c7a88401bcc7bf7f2ad93e30b9baeaebfbb23b6` | 1 | 1 |
| `FINAL_RESULTS_FREEZE_ACCEPTED.py` | 13 | `9af8c4393fec761d0104562d6de0086a4d577e395cdcb965e3f5a2d4495fc303` | `6b2364ece2f029af87ad6e3137ad9b84f0924d419776caabd8d47442a8a62617` | 1 | 1 |

## Full unified diffs

The CR characters of the CRLF endings are omitted below for display. The `.diff` files keep them.

### Stage 10 — `DOCUMENT_DEDUP_10X12_MATRIX_ACCEPTED.py`

```diff
--- V5/work/stage2_strict_v102/DOCUMENT_DEDUP_10X12_MATRIX_ACCEPTED.py
+++ WORK/code_baseline_20261014T041645Z/patched/DOCUMENT_DEDUP_10X12_MATRIX_ACCEPTED.py
@@ -13,11 +13,11 @@
 # ============================================================
 
 BASE = Path(
-    r"C:\NTUST_PAPER\outputs\20260911_AI_DECISION_V5_PRODUCTION"
+    r"C:\NTUST_PAPER\outputs\00_CURRENT\06_COMPUTE_CLOSURE_V1_8_5\compute_closure\baseline_reproduction\20261014T041645Z"
 )
 
 FREEZE_ROOT = (
-    BASE / "09_ANALYTICAL_FREEZE"
+    Path(r"C:\NTUST_PAPER\outputs\00_CURRENT\06_COMPUTE_CLOSURE_V1_8_5\work\run_inputs_baseline_20261014T041645Z\09_ANALYTICAL_FREEZE")
 )
 
 OUTPUT_ROOT = (
```

### Stage 11 — `NULL_MODEL_NETWORK_ANALYSIS_ACCEPTED.py`

```diff
--- V5/work/stage2_strict_v102/NULL_MODEL_NETWORK_ANALYSIS_ACCEPTED.py
+++ WORK/code_baseline_20261014T041645Z/patched/NULL_MODEL_NETWORK_ANALYSIS_ACCEPTED.py
@@ -15,7 +15,7 @@
 # ============================================================
 
 BASE = Path(
-    r"C:\NTUST_PAPER\outputs\20260911_AI_DECISION_V5_PRODUCTION"
+    r"C:\NTUST_PAPER\outputs\00_CURRENT\06_COMPUTE_CLOSURE_V1_8_5\compute_closure\baseline_reproduction\20261014T041645Z"
 )
 
 MATRIX_ROOT = (
```

### Stage 12 — `ROBUSTNESS_SENSITIVITY_ACCEPTED.py`

```diff
--- V5/work/stage2_strict_v102/ROBUSTNESS_SENSITIVITY_ACCEPTED.py
+++ WORK/code_baseline_20261014T041645Z/patched/ROBUSTNESS_SENSITIVITY_ACCEPTED.py
@@ -15,7 +15,7 @@
 # ============================================================
 
 BASE = Path(
-    r"C:\NTUST_PAPER\outputs\20260911_AI_DECISION_V5_PRODUCTION"
+    r"C:\NTUST_PAPER\outputs\00_CURRENT\06_COMPUTE_CLOSURE_V1_8_5\compute_closure\baseline_reproduction\20261014T041645Z"
 )
 
 MATRIX_ROOT = (
```

### Stage 13 — `FINAL_RESULTS_FREEZE_ACCEPTED.py`

```diff
--- V5/work/stage2_strict_v102/FINAL_RESULTS_FREEZE_ACCEPTED.py
+++ WORK/code_baseline_20261014T041645Z/patched/FINAL_RESULTS_FREEZE_ACCEPTED.py
@@ -13,7 +13,7 @@
 # ============================================================
 
 BASE = Path(
-    r"C:\NTUST_PAPER\outputs\20260911_AI_DECISION_V5_PRODUCTION"
+    r"C:\NTUST_PAPER\outputs\00_CURRENT\06_COMPUTE_CLOSURE_V1_8_5\compute_closure\baseline_reproduction\20261014T041645Z"
 )
 
 ROBUST_ROOT = (
```

## Hunk classification

| Script | Hunk | Change | Class |
|---|---|---|---|
| Stage 10 | @@ -13,11 +13,11 @@ (line 1) | `BASE` root: the obsolete V5 root (it no longer exists) → the new dated CC run dir. Every output root (`OUTPUT_ROOT`) derives from it | **PATH (output path)** |
| Stage 10 | @@ -13,11 +13,11 @@ (line 2) | `FREEZE_ROOT`: `BASE / "09_ANALYTICAL_FREEZE"` → an absolute WORK path holding the hash-verified copy of `analytical_freeze_v2_20260918T132206Z` (7 files, all 7 hashes checked before and after the run). The script still selects the freeze through its own `LATEST_ANALYTICAL_FREEZE_V2.txt` pointer logic. The pointer file was written in WORK to point at the copy | **PATH (input path)** |
| Stage 11 | @@ -15,7 +15,7 @@ | `BASE` root → the CC run dir. Inputs are read from `BASE/10_…` (this run's stage-10 output) and outputs go to `BASE/11_…` | **PATH (input/output path)** |
| Stage 12 | @@ -15,7 +15,7 @@ | `BASE` root → the CC run dir (reads `BASE/10_…`, `BASE/11_…`; writes `BASE/12_…`) | **PATH (input/output path)** |
| Stage 13 | @@ -13,7 +13,7 @@ | `BASE` root → the CC run dir (reads `BASE/11_…`, `BASE/12_…`; writes `BASE/13_…`) | **PATH (input/output path)** |

**Classification totals:**
- 5 changed lines in 4 hunks, all **PATH**.
- 0 ENV, 0 ENCODING.
- 0 changes to statistics, filters, predicates, taxonomy, dedup, null-model/RNG semantics, seeds, reps, thresholds, BH, the robust-core predicate, direction logic or gate constants.

**Environment differences.** These were applied at invocation, not in code:
- `python -I -B -X utf8`, with `cwd` = the run dir.
- `-X utf8` matches the V9 sidecar's `PYTHONUTF8=1`. Every file write in the scripts already passes an explicit encoding.

Gate constants left at their original values (verified by regex in 49):

| Stage | Constants |
|---|---|
| 11 | `SEED = 20260918`, `N_NULL = 10000`, `EXPECTED_M = 2180`, `EXPECTED_CELLS = 120`; `EXPECTED_MATRIX_SHA256` = `d816f34a…` (two-line literal, unchanged) |
| 12 | `DOCUMENT_NULL_SEED = 20260919`, `DOCUMENT_NULL_REPLICATES = 5000`, `BURN_IN_ATTEMPTS_PER_EDGE = 20`, `BETWEEN_SAMPLE_ATTEMPTS_PER_EDGE = 2`; `EXPECTED` dict unchanged |
| 13 | `EXPECTED_ROBUST_CORE = 32`, `EXPECTED_CELLS = 120`; `EXPECTED_ROBUST_SHA256` / `EXPECTED_NULL_SHA256` unchanged |
| 10 | `EXPECTED` dict (`freeze_sha256` `9a4e8fc2…`, 6499 / 3125 / 3374 / 1104 / 783 / 10 / 12) unchanged |

All gates passed with the original constants.

```
CODE_DIFF_HUNKS=4; CHANGED_LINES=5; CLASS=PATH_ONLY (5/5); NON_PATH_EDITS=0
```
