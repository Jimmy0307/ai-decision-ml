# 15 — Reanalysis Input Governance and Authority Notes (V1.8.1, sub-agent H, Task D)

Date: 2026-10-14. Status: **governance rule only**. No reanalysis was executed, no label was propagated, and no empirical result changed. `SUBMISSION_READY = NO`.

Path conventions:
- `V9/` = `W\02_V9_HUMAN_VALIDATION\20260929_V9_HUMAN_VALIDATION\` (read-only, not in git).
- `V1.8/` = `claude/r14_merge_v1_8_source_closure/`.

All sha256 values below were recomputed this run, or copied from the named V1.8 report where that report verified them.

---

## 1. Rule: `REANALYSIS_CANDIDATES_FROM_HUMAN_AUDIT.csv` = DO_NOT_USE_FOR_PROPAGATION

| Item | Value |
|---|---|
| File | `V9/REANALYSIS_CANDIDATES_FROM_HUMAN_AUDIT.csv` |
| sha256 | `489a1af42eacf3b495c99643026cbb5b691d8664cb0a821e48121caae976c1ba` |
| Rows | 44 rows, 44 unique records (out of the 50 audited) |
| Rule | **`DO_NOT_USE_FOR_PROPAGATION`** |

Why:

1. **It uses first-coder labels throughout.** Its `human_ai_family` / `human_decision_family` equal `FIRST_CODER_50_FINAL_FROZEN.csv` for **44/44** rows (checked by `tools/H/task_d_check.py`). It never uses the reconciled FINAL labels.
2. **18 of the 20 reconciled records carry different FINAL labels.** For 18/20 blind-subset records, the reconciled FINAL label in `HUMAN_RECONCILED_20.csv` differs from the first-coder frozen label on at least one of C1/C3/C4/C5. The diffs are in V1.8/`04_LOCAL_SENSITIVITY_REPRODUCTION.md` T5 and were recomputed this run as 18/20. 15 of those 20 records appear in the candidate file with their superseded first-coder labels.
3. **It is an impact screen, not a label table.** Its 44 rows are POTENTIAL_FAMILY_REASSIGNMENT 19, UNDETERMINED 14 and POTENTIAL_EXCLUSION 11. The 6 audited records screened NO_IMPACT in `ROBUST_CORE_IMPACT_SCREEN_50.csv` (`04` §4) are omitted, so the file is neither the sidecar's input nor a complete propagation list.

## 2. The only valid future propagation source

**`V1.8/04_LOCAL_SENSITIVITY_REPRODUCTION.md` Table T4**

- 04 sha256: `d9ab7bbf8b4756e5fe0b8d69db282e4de70083e56588f239f46b3d80f812a5cc`.
- It lists 50 audited records, each with its model label → human label for C5 inclusion, C3 AI family and C4 Decision family.
- 46 of the 50 records change at least one field, for 91 field changes in total.

| Records | Label source used in T4 | Source file | sha256 |
|---|---|---|---|
| 20 blind-subset records | Reconciled **FINAL** (`FINAL_C*`) | `V9/HUMAN_RECONCILED_20.csv` | `4b7ceac2c8c8bf2912ea542d88a1b887a42ed450aa248dce371525c25bb5bda0` |
| Other 30 records | **First-coder** (`human_*`) | `V9/FIRST_CODER_50_FINAL_FROZEN.csv` | `dd332dd8cfecf7dde9a29d32bca654b7c04c49f499c3e6213cd4d9a2ed157400` |
| Model side (all 50) | `current_ai_family` / `current_decision_family` / `model_analytical_pair_eligible` | same `FIRST_CODER_50_FINAL_FROZEN.csv` | (as above) |

Supporting hashes:
- Reconciliation event chain `V9/HUMAN_RECONCILIATION_EVENTS.jsonl` (`9270accc7657…`): 19/19 events reproduced (V1.8/`02` §2).
- `V9/ROBUST_CORE_LOCAL_SENSITIVITY.csv`: `e3166ee183e18f340c539b983108e2c972d18b916672a62510a25638db8b5b59`.

Any future rerun must record the sha256 of the exact T4-derived label input it consumes (`07` §7 criterion 3).

## 3. Unresolved propagation rule — must be predeclared

The V9 sidecar's rule for how human labels map to pair eligibility cannot be recovered from the package (`04` Q4):
- The generator script is NOT_RECOVERED.
- None of five plausible rules reproduces the sidecar's −18 pair-eligible delta. They give −13, −17, −21, −24, −25 and −27.

Before any rerun, the researcher must predeclare and hash-commit the handling of each case below (`07` §7 criterion 2):

| Human value | Field(s) | Decision required |
|---|---|---|
| `UNCERTAIN` | C5 inclusion (7 records), C1 | exclude / keep model label / keep as pair-eligible |
| `AMBIGUOUS` | C3 / C4 family | drop pair / keep model family / multi-assign |
| `UNMAPPED` | C3 / C4 family | drop pair / keep model family |
| `EXCLUDE` with family labels present | C5 vs C3/C4 | C5 overrides family (yes/no) |
| C2 relation type | C2 | used for eligibility or not |

Until this is predeclared: `PROPAGATION_RULE_STATUS=UNRESOLVED_MUST_BE_PREDECLARED`.

## 4. Full-reanalysis status (current terminology)

```
FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION
FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET
FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED
```

Reasons, from V1.8/`07_FULL_REANALYSIS_DECISION_MEMO.md` §8 (sha256 `6c628632187390388d2222cc525453c60c8b82c34e6a47a2e3f800879d1e6558`) and V1.8/`02` §5:

1. **12 of 37 protected inputs are not recovered.** These are the frozen strict-record DB, the freeze manifests and the original 400/120 samples. The `07` §4 pre-run gate (restore and hash-match) cannot pass, so the execution status is NOT_EXECUTABLE.
2. **The sidecar shows G01–G16 unaffected.** It gives 32 → 32 cells, 15/17, +1 depleted / −1 enriched, and no G cell removed (`04` T1/T2). A rerun with the same 50 labels is expected to reproduce this.
3. **A rerun adds reproducibility, not corpus-wide label validity.** Propagating 50 labels into a 3,125-record model-labelled frame gives a mixed-source corpus. It does not correct labels across the corpus and does not support a corpus-wide error estimate.
4. **The true limitation is a small, targeted sample with low model–human agreement.** The 50 records are Robust-A only. Agreement was relation 14/50, AI family 19/50, Decision family 9/50 and inclusion 33/42. A properly scoped, larger human audit is the remedy, not a rerun.
5. **A future rerun remains a researcher decision.** V9's own `FULL_REANALYSIS_REQUIRED` carries `full_reanalysis_requires_researcher_approval = true`. This note is advisory and does not resolve it. If a rerun is chosen, it must use §2 (T4) as input and §3 as its predeclared rule, and it must pass `07` §4–§7.

No "not required" status may be written for the full reanalysis.

---

## 5. Authority note: human-audit report and taxonomy

| File | sha256 | Classification |
|---|---|---|
| `V9/FINAL_HUMAN_AUDIT_REPORT.md` (82 lines; manifest-pinned) | `63d651baa7709a240c3ef09ddc52e8c271723f1ab43243d36bb4d68689b18a7e` | **`HISTORICAL_FINAL_REPORT_WITH_TEMPLATE_DEFECT`** |
| `V9/FINAL_ERROR_TAXONOMY.csv` | `68e97c01465fad51ad9020956dea0e463617ea290ca0e5debd6c6ab14b554244` | **Taxonomy authority (machine-readable)** |
| `V9/FINAL_ERROR_TAXONOMY.md` | `3304410602aaca6079c6e75cdef51b6f782dda6f7effbc88352786bc77a59e00` | **Taxonomy authority (text)** |
| `V9/FINAL_ERROR_TAXONOMY_CASES.csv` | `8949b671ae3619869c1cd3e15ce89955c3cb64114a21d9367dc2cd6800139306` | Supporting case list |

### The defect

- **Where it is.** `FINAL_HUMAN_AUDIT_REPORT.md` **line 49** is the literal unrendered placeholder `{taxblock}`. It sits in section `## Error taxonomy`, directly under the table header `| Error pattern | n | % of 50 |` (lines 47–48).
- **What is missing.** The error-taxonomy rows were never rendered.
- **What is still usable.** The surrounding prose is rendered and is consistent with `FINAL_ERROR_TAXONOMY.*`: "77 category-tag assignments on 33 unique records" (line 45) and the sidecar-scope sentence (line 61). The prose may be quoted, but the taxonomy table must not be taken from this file.
- **Rules.** Taxonomy counts, categories and per-record tags come only from `FINAL_ERROR_TAXONOMY.csv` / `.md`. Taxonomy content is unchanged by this note.

### Search: does anything quote `{taxblock}` content or cite FINAL_HUMAN_AUDIT_REPORT for taxonomy?

Scope: all files in V1.8/ (including `tools/`) and the v1.8 manuscript `V1.8/08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md` (sha256 `1515b0f2…7ad58`). Search terms: `taxblock`, `FINAL_HUMAN_AUDIT_REPORT`, `ERROR_TAXONOMY`, `錯誤型態表`.

| Location | Reference | Cites the FINAL report for taxonomy, or quotes `{taxblock}`? |
|---|---|---|
| V1.8/`02_V9_AUTHORITY_MAP.md` L104, L131, L160, L188 | Flags the `{taxblock}` defect; directs taxonomy to `FINAL_ERROR_TAXONOMY.*` | No. It is the defect notice. |
| V1.8/`02` L75 | Timeline entry listing the file | No |
| V1.8/`04_LOCAL_SENSITIVITY_REPRODUCTION.md` L70 (+ `tools/C/head.md` L70) | Cites `FINAL_HUMAN_AUDIT_REPORT.md` **l.61** for the sidecar label scope (20 reconciled + 30 first-coder) | No. It is a non-taxonomy line outside the placeholder. |
| V1.8/`10_FINAL_STATUS.md` L96 | "contains an unfilled `{taxblock}` placeholder. Use `FINAL_ERROR_TAXONOMY.*`" | No. It is the defect notice. |
| V1.8/`01_FILE_INVENTORY.csv` L343; `tools/A/hash_claims.csv` L29, `hash_citations.csv` L66, `name_citations.json`, `authority_scan.py` L178 | Inventory and hash rows | No |
| v1.8 manuscript L591, L1559 (×2 each), L2262 | Cites `〔V9 套件 FINAL_ERROR_TAXONOMY.csv，已核對〕` / 「V9 錯誤型態表（FINAL_ERROR_TAXONOMY.csv）」 | No. It cites the correct authority. |
| v1.8 manuscript (all 3,080 lines) | `FINAL_HUMAN_AUDIT_REPORT` / `taxblock` | **0 occurrences** |

Result: **0 references quote `{taxblock}` content, and 0 cite FINAL_HUMAN_AUDIT_REPORT for taxonomy.** The v1.8 manuscript already uses `FINAL_ERROR_TAXONOMY.csv`.

---

## Machine-readable summary

```
REANALYSIS_CANDIDATES_FROM_HUMAN_AUDIT.csv=DO_NOT_USE_FOR_PROPAGATION
VALID_PROPAGATION_SOURCE=V1.8/04_LOCAL_SENSITIVITY_REPRODUCTION.md#T4 (20 RECONCILED_FINAL + 30 FIRST_CODER)
PROPAGATION_RULE_STATUS=UNRESOLVED_MUST_BE_PREDECLARED
FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION
FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET
FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED
FINAL_HUMAN_AUDIT_REPORT.md=HISTORICAL_FINAL_REPORT_WITH_TEMPLATE_DEFECT (line 49 {taxblock})
TAXONOMY_AUTHORITY=FINAL_ERROR_TAXONOMY.csv + FINAL_ERROR_TAXONOMY.md
TAXBLOCK_QUOTATIONS_FOUND=0
```
