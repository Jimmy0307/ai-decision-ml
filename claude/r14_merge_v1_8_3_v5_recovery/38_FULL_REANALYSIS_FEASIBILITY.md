# 38 — Full-Reanalysis Execution Feasibility (V1.8.3, sub-agent Q, Task 2)

Date: 2026-10-14. Mode: read-only assessment.
- **Nothing was executed.** No pipeline, null-model or sidecar code was run. All code below was read and hashed only.
- **Two checks were recomputed.** The descriptive checks were recomputed from frozen rows. The propagation rule was re-derived from the frozen human-label files with a stdlib comparison script (`tools\Q\rule_check.py`), which does not run any pipeline stage.
- **Gates assessed.** V1.8 `07_FULL_REANALYSIS_DECISION_MEMO.md` §4–§7 and V1.8.1 `15_REANALYSIS_INPUT_GOVERNANCE.md`.
- **Evidence files.** `tools\Q\feasibility_evidence.py` → `feasibility_evidence.json`, and `tools\Q\rule_check.py` → `rule_check_result.json`.

**Recommended status: `FULL_REANALYSIS_EXECUTION_STATUS=EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION`** (was `NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET`).

Unchanged:
- `FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION`.
- The priority before V1 (`NOT_RECOMMENDED`) remains a researcher decision.

STOP: none.
- The V5 frozen rows equal the baseline: 6,499 strict / 3,125 pair-eligible / 783 documents / M = 2,180 / 120 cells / 47 main q ≤ .05 / core 32 = 16 + 16.
- G01–G16 ⊂ core DEPLETED: 16/16.
- 0 manifest hash mismatches.

---

## 1. Element-by-element status

| # | Required element | Status | Evidence |
|---|---|---|---|
| a | Protected inputs (07 §4 gate, 07 §7.1) | **PRESENT + VERIFIED, 37/37** | `37_PROTECTED_INPUT_RECOVERY.md`: 36 full-file SHA-256 matches + 1 byte-prefix match; FREEZE_ROOT chain recomputed |
| b | Frozen strict-record DB and analytical freeze | **PRESENT + VERIFIED** | See §2b |
| c | Code for stages 09–13 | **PRESENT + VERIFIED** (code hash pinned by FREEZE SHA256SUMS and by the sidecar run record; **not** by the V5 stage manifests) | See §2c |
| d | Seeds and replicates | **PRESENT + VERIFIED** | See §2d |
| e | V9 sidecar generator | **PRESENT. Generator file: PROBABLE. Its outputs: CONFIRMED** | See §2e |
| f | Label-propagation rule (E48) | **RECOVERED (the V9 rule), independently re-derived. Still needs researcher predeclaration and hash-commit** | See §2f |
| g | Reproduce the 13 hash-pinned official outputs | **ALL 13 PRESENT AND MATCH THEIR PINS. Byte-for-byte reproduction was demonstrated by V9 on 2026-10-03, but has not been re-shown since the workspace move. The code pins an obsolete ROOT path.** | See §2g |

## 2. Detail

### (b) Strict-record DB and analytical freeze

- **Inputs, all at matching hashes.**
  - `07_FSC_STAGE2_STRICT_V102\FSC_STAGE2_RESULTS_v1_0_2.sqlite` (`cc425630…`).
  - Source DB `LocalCorpusWorkbench\v5_production_app\data\workbench.sqlite` (`367e588c…`), at its original lineage path.
  - Definitions `08f256af…`.
  - Reconstructed scope `968e6d22…`.
  - Stage-3 closure canonical `cd20aab5…`.
- **Analytical freeze v2.** `09_ANALYTICAL_FREEZE\analytical_freeze_v2_20260918T132206Z\`, with canonical `9a4e8fc2…`, RECORD_LEVEL `fbb5f592…`, PAIR_ELIGIBLE `9ee5fd53…` and MANIFEST_V2 `69c7a7df…`.
  - MANIFEST_V2's lineage block pins the workbench, stage-2 and definitions hashes listed above. All 28 of its checks are `true`.
- **Manifest chain across stages.** The pins chain from stage to stage and every link matches:
  - analytical freeze `9a4e8fc2` → matrix manifest;
  - matrix `d816f34a` → null manifest;
  - null `682a58f7` → robustness manifest;
  - robustness `8c0441ce` and null `682a58f7` → results-freeze manifest.

### (c) Code for stages 09–13

All paths are under `V5\work\stage2_strict_v102\`.

| Stage | Script | sha256 | Bytes |
|---|---|---|---:|
| 08 | `STAGE3_RESIDUAL_CLOSURE_ACCEPTED.py` | `ff39df6d24015bfa74cd2f858ebf25611ebf4e978598cbaa49cb5d207b1512f7` | 29,518 |
| 09 | `build_analytical_freeze_v2.py` | `f4e55227c3c9a60d6b7859a9d6da1acae01aa62ded52596be4d3ae28fad78187` | 55,116 |
| 09 helper | `analytical_downstream_contract.py` | `af3dad4c691b7992dba0dc086c7ea30ea5f4ffcfadadc58b2ffddc53a80d35f9` | 1,326 |
| 09 helper | `stage2_common.py` | `4422e4e144eccbe699a260ae0f63710f04d9a4c7a037e6453fe3a4cce953e385` | 19,698 |
| 10 | `DOCUMENT_DEDUP_10X12_MATRIX_ACCEPTED.py` | `a3892528ecac135839681429916d8d6607f1ef4685456d9663373b49a1175cd7` | 35,640 |
| 11 | `NULL_MODEL_NETWORK_ANALYSIS_ACCEPTED.py` | `cd96c48d685fe05d23d526638bf3d0ab7201a115f3c9cab0d908277c1d0b12e3` | 32,700 |
| 12 | `ROBUSTNESS_SENSITIVITY_ACCEPTED.py` | `7700d98c934db95ff28dc7aba19be1ce6558fff2957bc79bff54f63a63087c19` | 51,468 |
| 13 | `FINAL_RESULTS_FREEZE_ACCEPTED.py` | `9af8c4393fec761d0104562d6de0086a4d577e395cdcb965e3f5a2d4495fc303` | 43,506 |

**Where the code hashes are pinned:**

- **V5 stage manifests (09–13): no code hash.** The manifests record input/output hashes, verdicts and checks, but not the hash of the script that produced them.
- **FREEZE `SHA256SUMS.csv`: yes, all match.** Every script above is listed under `02_SOURCE_CORPUS_LINEAGE/V5_PRODUCTION/work/stage2_strict_v102/` with an identical sha256, and the FREEZE copies re-hash to match.
  - The FREEZE is dated 2026-09-24, after the stage runs of 09-18/09-19. It therefore proves the code has been unchanged since 09-24. It does not, by itself, prove which code ran on 09-18.
- **V9 sidecar run record: yes, for stages 10–13.** `CORRECTED_SIDECAR_OUTPUTS.json` (`a6dc30c9…`) records `analysis_script_sha256` for the 4 stage 10–13 scripts. All 4 equal the hashes above.
  - The baseline run, using these scripts with only the path changed, reproduced the 13 pinned 09-18/09-19 outputs byte-for-byte (§2g). That is strong evidence that this is the code that produced them.
- **Stage 09 has no output-reproduction evidence.** Its code is pinned only by the FREEZE. No sidecar or V9 reproduction re-ran stage 09: the sidecar starts from the frozen RECORD_LEVEL CSV.

Other locations searched:
- `C:\NTUST_PAPER\scripts\`, `tools\`, the repo and root-level `*.py` contain no stage 09–13 implementation.
- The FREEZE `CODE_INVENTORY.csv` (5,898 code files) indexes them.
- **Runtime.** All scripts import only the standard library (`csv`, `hashlib`, `json`, `math`, `random`, `sqlite3`, `collections`, `datetime`, `pathlib`). The FREEZE `ENVIRONMENT_SNAPSHOT.md` records Python 3.14.2, and the installed Python is 3.14.2.

### (d) Seeds and replicates

| Null | Code constant | Manifest / parameter file |
|---|---|---|
| Main fixed-degree MC | `SEED = 20260918`, `N_NULL = 10000` (lines 39, 42) | Null manifest `null_model.seed=20260918`, `replicates=10000` |
| Document-preserving | `DOCUMENT_NULL_SEED = 20260919`, `DOCUMENT_NULL_REPLICATES = 5000` (lines 54, 52); burn-in 20/edge, between-sample 2/edge | Robustness manifest `replicates=5000`; FREEZE `08_STATISTICAL_ANALYSIS\DOCUMENT_NULL_CHAIN_PARAMETERS.json` (`94d7364a…`, SHA256SUMS MATCH): `seed=20260919`, 43,600 burn-in, 4,360 between-sample, 5,000 samples, single chain |

The python-random seed and stream are deterministic under CPython's `random`, and the same interpreter version is installed.

### (e) The V9 sidecar generator

**Folder.** `C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\01_V9_HUMAN_VALIDATION\20261003_V9_HUMAN_AUDIT_FINAL_CONVERGENCE_SIDECAR_20261003T192417\`. It contains 208 files. Neither V1.8 nor V1.8.2a searched it.

| File | sha256 |
|---|---|
| `prepare_and_run_corrected_sidecar.py` (the generator: builds the correction map, the corrected freeze and the V5_CORRECTED stage runs) | `021e3d10c8a1085bdae57df9a964a9416a61b4cf68acb1e33360448fd6463ef3` |
| `run_baseline_reproduction.py` / `continue_baseline_reproduction.py` / `verify_baseline_reproduction.py` | `cbe6aa94…` / `96e48bab…` / `6a4f2739…` |
| `LOCAL_HUMAN_CORRECTION_POLICY.md` | `33d4d44c2d1940dc34498cbe1a13266ad20d9b668d3e420d1c4de1840200940a` |
| `HUMAN_AUDIT_LOCAL_CORRECTION_MAP.csv` (50 rows) | `d09db24472c060e723f52acf6ef7ea26918368d9189f288efb6b8ce94d493313` (= `corrections_map_sha256` in `CORRECTED_SIDECAR_OUTPUTS.json`) |
| `LOCAL_HUMAN_CORRECTION_MANIFEST.json` | `6a4ca321…` |
| `V5_CORRECTED\…\FINAL_ROBUST_CORE_32.csv` | `4e412a07…` = V9 `FINAL_STATUS.json` `sidecar_core_sha256` |

**ROBUST_CORE_LOCAL_SENSITIVITY / sidecar_core_member.**
- **The script that wrote this CSV was not found.** A search of all `*.py` under `C:\NTUST_PAPER` for `sidecar_core_member` finds only scripts that read the CSV, all in the repo's V1.8 / V1.8.1 / V1.8.3 tools. None writes it. The generator produces the V5_CORRECTED stage outputs and the core.
- **The CSV's content still matches the generator's outputs.** Its `sidecar_core_member=YES` set equals the core file `4e412a07`: 32 cells = 15 + 17.

**Grading.**
- The **outputs** are CONFIRMED: core `4e412a07` and the map hash chain.
- The **generator script** is PROBABLE. Its location and self-consistent outputs fit, but no V9 artifact pins its own sha256.
- The script hard-codes the obsolete root paths `C:\NTUST_PAPER\outputs\20261003_…SIDECAR…` and `C:\NTUST_PAPER\outputs\20260929_V9_HUMAN_VALIDATION`.

### (f) Label-propagation rule (E48)

**Source.** The rule comes from the generator's code (lines 345–363) and is stated verbatim in `LOCAL_HUMAN_CORRECTION_POLICY.md`.

**Labels used:**
- **20 records** use `HUMAN_RECONCILED_20.csv` FINAL_C*: 19 `HUMAN_RECONCILIATION` + 1 `UNANIMOUS_PRE_ADJUDICATION`.
- **30 records** use `FIRST_CODER_50_FINAL_FROZEN.csv`.
- This equals 07 §2 / T4.

**Rule:**

| Human label | Action | n |
|---|---|---:|
| C5 = EXCLUDE (any C1) | REMOVE pair (not eligible) | 13 |
| C5 = INCLUDE, C1 = VALID, C3 ∈ 10 AI families and C4 ∈ 12 Decision families | APPLY human family pair | 23 |
| C5 = INCLUDE, C1 = VALID, C3 or C4 AMBIGUOUS/UNMAPPED/outside taxonomy | REMOVE pair (family unresolved) | 5 |
| Otherwise: C5 = UNCERTAIN (7), or C5 = INCLUDE with C1 = INVALID/UNCERTAIN (2) | LEAVE official model pair unchanged | 9 |
| C2 relation | Descriptive only; not used (no relation dimension in the matrix) | — |

**Independent check (`rule_check.py`).**
- **Inputs.** The rule was re-applied to the frozen inputs `dd332dd8…` and `4b7ceac2…` and the frozen 10 × 12 taxonomy.
- **Agreement.** It gives the same action for **50/50 records (0 mismatches)** and a **−18** pair-eligible delta. That is 3,125 → 3,107, exactly the sidecar's pinned delta.
- **Why V1.8 missed it.** None of V1.8's five candidate rules (−13 … −27) was this rule. Its distinguishing features are:
  - UNCERTAIN keeps the model label;
  - INCLUDE together with C1 ≠ VALID keeps the model label;
  - INCLUDE with an unresolved family drops the pair.

**Status recommendation.**
- `PROPAGATION_RULE_STATUS=RECOVERED_V9_RULE_REQUIRES_RESEARCHER_PREDECLARATION`.
- The 07 §7 criterion 2 still requires the researcher to predeclare and hash-commit the rule before execution. The researcher can adopt this recovered rule (policy sha `33d4d44c…`) or another one.
- If adopted unchanged, a rerun is expected to reproduce the sidecar (`4e412a07`).

### (g) Reproducing the 13 hash-pinned official outputs

**Pins.** All 13 pins come from the sidecar's `BASELINE_REPRODUCTION_VERIFICATION.md`, and all 13 V5 files match them:

| Stage | Pinned outputs (sha256 prefix) |
|---|---|
| 10 | matrix canonical `d816f34a`, dedup edges `3ba370c1`, doc-count matrix `ebac2b66`, raw-count matrix `e5883e51` |
| 11 | null canonical `682a58f7`, main null 120 `e7019dfe` |
| 12 | robustness canonical `8c0441ce`, exact 120 `8538fc82`, document-null 120 `6b7c6e29`, raw-record 120 `12e8b7e3`, comparison 120 `1e30bf06` |
| 13 | results canonical `b1d8b5ee`, final core `a43b4b58` |

**Previous reproduction.**
- **V9 run, 2026-10-03.** `BASELINE_REPRODUCTION_VERIFICATION.json` reports PASS 13/13. The run used copies of the official stage 10–13 scripts with input analytical-freeze files `fbb5f592` / `9ee5fd53` / `9a4e8fc2` / `69c7a7df` / `7704e743`.
- **How the copies differ.** A diff shows the sidecar `V5_PRODUCTION` copies differ from the official scripts only in:
  - (i) the `ROOT` path line;
  - (ii) the line-split of an embedded hash string, which leaves the value unchanged.

**What a future reproduction needs:**
- the 4 stage 10–13 scripts above;
- the 09 analytical-freeze files (present);
- the same seeds;
- Python 3.14 standard library (present);
- a relocated ROOT.

**The ROOT problem.**
- The official scripts pin `ROOT = C:\NTUST_PAPER\outputs\20260911_AI_DECISION_V5_PRODUCTION`. That path no longer exists, because the V1.8.2a reorganisation moved it to `10_CANONICAL_EVIDENCE\04_V5_PRODUCTION_FREEZE\`.
- A rerun therefore needs path-patched copies in a new dated directory, with the diff recorded, as the sidecar did.
- Writing into V5 must never be used to get around this.

**Stage 09.** Reproducing stage 09 from `workbench.sqlite` is possible in principle, since all inputs and code are present. It has never been demonstrated, and label propagation does not need it.

## 3. Conclusion

**`FULL_REANALYSIS_EXECUTION_STATUS=EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION`**

**Why not NOT_EXECUTABLE.** That status rested on "12/37 protected inputs NOT in any package". Now:
- All 37 are hash-confirmed, the strict DB and freeze chain verify, and the stage code and seeds are present and pinned.
- The sidecar core and the generator are located.
- The propagation rule is recovered and independently re-derived.

**Why not EXECUTABLE.** 07 §7 criteria 1 (second half) and 2 are not yet met in the current environment:

**Minimal remaining blockers:**
1. **Propagation rule.** The researcher must predeclare and hash-commit the rule. The recovered V9 rule (policy `33d4d44c…`, re-derived 50/50, −18) is the obvious candidate, but adopting it is a researcher decision. The label input must be T4-exact, with its sha recorded (07 §7.3).
2. **Baseline reproduction in the current layout.** Path-patched copies of the 4 stage 10–13 scripts (and the stage 09 script, if 09 is rerun) must be created in a new dated directory, with the diff limited to ROOT. The 13 pinned outputs must then reproduce byte-for-byte (07 §5, §7.1) before any corrected run. The 2026-10-03 PASS predates the move and was produced by a PROBABLE-graded runner, so it should be re-shown, not inherited.
3. **Researcher approval.** This is required by V9 (`full_reanalysis_requires_researcher_approval=true`). It is a governance gate, not a technical one.

Non-blocking caveats:
- The V5 stage manifests carry no code hash. Code identity rests on the FREEZE SHA256SUMS (dated 09-24) plus the 13/13 output reproduction.
- The FREEZE `MISSING_OR_UNKNOWN_ARTIFACTS.csv` lists "101 V5 run differences partially explained" as required for **exact upstream** reproduction. This affects only regenerating stages ≤ 07 (LLM coding), not 09–13.
- The generator is PROBABLE. A rerun should use a fresh, hash-committed runner and treat `prepare_and_run_corrected_sidecar.py` as the reference implementation.

## 4. Do the 5 V1.8.1 reasons for `NOT_RECOMMENDED` still hold? (advisory; the priority is a researcher decision)

| # | Reason (15 §4) | Still holds? |
|---|---|---|
| 1 | 12/37 protected inputs unrecovered → not executable | **No longer holds.** 37/37 are confirmed. Execution is now gated only by the rule predeclaration, the baseline re-reproduction and approval |
| 2 | The sidecar shows G01–G16 unaffected; a rerun is expected to reproduce it | **Holds, and is stronger.** The sidecar core file `4e412a07` is now located: 32 = 15/17, +1/−1, G01–G16 all remain core DEPLETED. The generator and rule are recovered, and the rule re-derives −18 exactly |
| 3 | A rerun adds reproducibility, not corpus-wide label validity | Holds |
| 4 | The real limitation is a small targeted sample with low agreement | Holds |
| 5 | A rerun is a researcher decision | Holds |

So 1 of the 5 reasons lapses. The other 4 are unchanged, so the advisory basis for `FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED` is still substantively intact. The researcher may now choose a rerun as a low-cost reproducibility exercise, since all inputs are local. Reason 1 should be reworded in any successor note.

```
FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION          (unchanged)
FULL_REANALYSIS_EXECUTION_STATUS=EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION  (recommended; was NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET)
FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED                              (unchanged; researcher decision; reason 1 lapsed, 2–5 hold)
PROPAGATION_RULE_STATUS=RECOVERED_V9_RULE_REQUIRES_RESEARCHER_PREDECLARATION    (recommended; was UNRESOLVED_MUST_BE_PREDECLARED)
SIDECAR_GENERATOR=PRESENT (script PROBABLE; outputs CONFIRMED)                  (was NOT_RECOVERED)
STAGE_CODE_09_13=PRESENT_VERIFIED (FREEZE SHA256SUMS + sidecar run record; no code hash in V5 manifests)
OFFICIAL_13_PINNED_OUTPUTS=13/13 PRESENT_MATCH; byte reproduction PASS on 2026-10-03, re-show required after relocation
STOP=NONE
```
