# 43 — Propagation Rule Pre-registration: BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1 (V1.8.5, sub-agent S, Phase 1)

Date: 2026-10-14. Status: **FROZEN before any revised run.** No revised analysis was executed in this round.

- **Rule status.** The researcher APPROVED `BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1` (orchestrator instruction).
- **This document's role.** It records how the rule is applied, field by field, with hashes. Companion files:
  - `44_PROPAGATION_RECORD_MANIFEST.csv`: 50 rows.
  - `45_PROPAGATION_RULE_HASHES.csv`: input, document, manifest and applier hashes.
- **Work-copy root.** All inputs were read from WORK copies, each verified equal to its source by SHA-256 (92 files, 0 mismatches): `WORK\inputs_S_20261014T040934Z\` (`INPUT_COPY_MANIFEST.csv`).

## 1. The approved rule (as given)

| Clause | Content |
|---|---|
| A | The 20 reconciled audit records take the **FINAL RECONCILED HUMAN LABEL**. Source: V9 `HUMAN_RECONCILED_20.csv`, verified against `HUMAN_RECONCILIATION_EVENTS.jsonl`. It takes precedence over both the first coder and the model. |
| B | The other 30 targeted audit records take the **FIRST-CODER HUMAN LABEL** (V9 `FIRST_CODER_50_FINAL_FROZEN.csv`), which takes precedence over the model. |
| C | Every other record **KEEPS ITS ORIGINAL MODEL LABEL**. |
| D | Forbidden: inferred correction of other records, error-rate extrapolation, corpus-wide or taxonomy-wide adjustment, probabilistic correction, imputation, and nearest-neighbour or rule-based relabelling. |

- **Precedence:** `RECONCILED_FINAL > FIRST_CODER > ORIGINAL_MODEL`.
- **Who may override:** only a record with an explicit human-audit match on `record_id` may override a model label.

## 2. Which label fields feed the pipeline

Determined by reading the stage code: V5 `work\stage2_strict_v102\*.py`, with hashes in 45.

**Stage 10 is the only stage that reads the analytical freeze.** Stages 11–13 read only stage-10, 11 and 12 outputs. Stage 10 uses the freeze files as follows:

| Freeze file | What stage 10 uses (`DOCUMENT_DEDUP_10X12_MATRIX_ACCEPTED.py`) | Label-bearing? |
|---|---|---|
| `ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv` | The eligible frame = **rows of this file**. Per row: `analytical_pair_eligible` (must be true), `mapping_completeness` (must be `FULLY_MAPPED`), `left_final_family` = **AI family**, `right_final_family` = **Decision family** (cell counts, edges, marginals), `document_id` (dedup unit), `record_id`; `relation_type` and `evidence_sha256` are concatenated **descriptively** into the `relation_types` / `evidence_sha256s` edge columns | YES |
| `ANALYTICAL_FREEZE_RECORD_LEVEL.csv` | Row count (strict records) and strict document ids | Count gate only |
| `ANALYTICAL_FREEZE_SIDE_LEVEL.csv` | Taxonomy = the set of mapped LEFT and RIGHT `final_family` values (10 × 12) | Not changed by the rule. The taxonomy stays frozen. |
| `ANALYTICAL_FREEZE_CANONICAL.json` | sha256 gate (`EXPECTED["freeze_sha256"]`) | Hash gate only |
| `ANALYTICAL_FREEZE_MANIFEST_V2.json` | `verdict == ANALYTICAL_FREEZE_ACCEPTED` | No |

**Pipeline fields written by the rule.** These are the record-level columns. The eligible file and the canonical JSON mirror them:
- `analytical_pair_eligible` (inclusion/eligibility);
- `left_final_family` (AI family);
- `right_final_family` (Decision family);
- `left_final_status`;
- `right_final_status`;
- `mapping_completeness`;
- `analytical_exclusion_reason`.

**Relation type (C2) is NOT propagated.**
- The 10 × 12 matrix and all four null/test methods have no relation dimension.
- The only place `relation_type` appears in a stage output is the descriptive `relation_types` column of the edge table.
- Under the recovered translation, it keeps the model value. In 44 this is recorded as `final_relation_type = <model value> (UNCHANGED; C2 descriptive only)`.

## 3. Translation of human codes into pipeline fields (documented, recovered; recorded verbatim)

**Authority.** The translation is taken from:
- the sidecar generator `prepare_and_run_corrected_sidecar.py` (sha256 `021e3d10c8a1085bdae57df9a964a9416a61b4cf68acb1e33360448fd6463ef3`), lines 344–394;
- its policy text `LOCAL_HUMAN_CORRECTION_POLICY.md` (sha256 `33d4d44c2d1940dc34498cbe1a13266ad20d9b668d3e420d1c4de1840200940a`).

Both come from the WORK copy of `SIDECAR\`.

V1.8.3 38 §2f / `tools\Q\rule_check.py` already re-derived the action set (50/50, −18). This round re-derived it again in `tools\S\s_phase1_propagation_manifest.py`: **0 mismatches** against the sidecar `HUMAN_AUDIT_LOCAL_CORRECTION_MAP.csv` (`d09db244…3313`) on action, eligibility, AI family and Decision family, for all 50 records.

### 3a. Policy text (verbatim, `LOCAL_HUMAN_CORRECTION_POLICY.md`)

> This sidecar applies confirmed human judgments only to the 50 audited record IDs. The 20-record overlap uses HUMAN_RECONCILED_20.csv; the other audited records use their original first-coder labels. Original first and blind coder files remain untouched.
>
> Human C5=EXCLUDE removes an audited record from the mapped-pair input. C5=INCLUDE is applied only when C1=VALID and both final family labels match the frozen 10-by-12 taxonomy. An included but unresolved family is omitted from the mapped-pair sidecar and logged distinctly. Uncertain or internally inconsistent labels are not applied and leave the official pair unchanged. Relation is retained for descriptive audit only because the frozen matrix has no relation dimension. All other records are unchanged apart from CSV reserialization in the sidecar.
>
> Official V9 results and source artifacts are unchanged. This analysis is local and does not represent corpus-wide correction.

### 3b. Code (verbatim, generator lines 354–363 and 373–394)

```python
    c1,c2,c3,c4,c5=[label[k].strip().upper() for k in ("C1","C2","C3","C4","C5")]
    if c5=="EXCLUDE":
        action="REMOVE_HUMAN_EXCLUDED_PAIR"; reason="FINAL_HUMAN_C5_EXCLUDE"
    elif c5=="INCLUDE" and c1=="VALID" and c3 in ai_families and c4 in decision_families:
        action="APPLY_HUMAN_FAMILY_PAIR"; reason="FINAL_HUMAN_INCLUDE_VALID_AND_BOTH_FAMILIES_IN_FROZEN_TAXONOMY"
    elif c5=="INCLUDE" and c1=="VALID":
        action="REMOVE_UNMAPPED_HUMAN_FAMILY_PAIR"; reason="HUMAN_INCLUDED_BUT_ONE_OR_BOTH_FAMILY_LABELS_UNRESOLVED_OR_OUTSIDE_FROZEN_TAXONOMY"
    else:
        action="LEAVE_OFFICIAL_PAIR_UNCHANGED"; reason="UNCERTAIN_OR_INCONSISTENT_HUMAN_LABELS; NO CONFIRMED OVERRIDE"
...
    if action=="REMOVE_HUMAN_EXCLUDED_PAIR":
        out["analytical_pair_eligible"]="False"
        out["analytical_exclusion_reason"]="HUMAN_AUDIT_LOCAL_SENSITIVITY_C5_EXCLUDE"
    elif action=="APPLY_HUMAN_FAMILY_PAIR":
        out["left_final_family"]=label["C3"].strip().upper()
        out["right_final_family"]=label["C4"].strip().upper()
        out["left_final_status"]="MAPPED"; out["right_final_status"]="MAPPED"
        out["mapping_completeness"]="FULLY_MAPPED"
        out["analytical_pair_eligible"]="True"; out["analytical_exclusion_reason"]=""
    elif action=="REMOVE_UNMAPPED_HUMAN_FAMILY_PAIR":
        c3=label["C3"].strip().upper(); c4=label["C4"].strip().upper()
        if c3 in ai_families:
            out["left_final_family"]=c3; out["left_final_status"]="MAPPED"
        else:
            out["left_final_family"]=""; out["left_final_status"]="UNRESOLVED_HUMAN_AUDIT"
        if c4 in decision_families:
            out["right_final_family"]=c4; out["right_final_status"]="MAPPED"
        else:
            out["right_final_family"]=""; out["right_final_status"]="UNRESOLVED_HUMAN_AUDIT"
        out["mapping_completeness"]="PARTIALLY_MAPPED" if (out["left_final_family"] or out["right_final_family"]) else "FULLY_UNRESOLVED"
        out["analytical_pair_eligible"]="False"
        out["analytical_exclusion_reason"]="HUMAN_AUDIT_LOCAL_SENSITIVITY_FAMILY_UNRESOLVED"
```

**Taxonomy.** `ai_families` and `decision_families` come from the official stage-10 canonical `DOCUMENT_DEDUP_MATRIX_CANONICAL.json` (`d816f34a…71b5`). That gives 10 AI and 12 Decision family codes. The taxonomy is frozen and not changed.

### 3c. Code-by-code translation table (complete; no ambiguous case)

Values are evaluated in this order, and the first matching row applies.

| # | Human code combination (C1 / C3 / C4 / C5) | Action | Pipeline effect | n (of 50) |
|---|---|---|---|---:|
| 1 | C5 = **EXCLUDE**, any C1/C3/C4. This includes C3/C4 = UNMAPPED, AMBIGUOUS or present families. **C5 overrides the family labels.** | `REMOVE_HUMAN_EXCLUDED_PAIR` | `analytical_pair_eligible=False`, `analytical_exclusion_reason=HUMAN_AUDIT_LOCAL_SENSITIVITY_C5_EXCLUDE`. Families and status are left as model values (not counted, because the record is ineligible) | 13 |
| 2 | C5 = INCLUDE **and** C1 = VALID **and** C3 ∈ 10 AI families **and** C4 ∈ 12 Decision families | `APPLY_HUMAN_FAMILY_PAIR` | Families set to the human C3/C4, status MAPPED/MAPPED, `FULLY_MAPPED`, eligible `True`, reason empty | 23 |
| 3 | C5 = INCLUDE **and** C1 = VALID, but C3 and/or C4 = **AMBIGUOUS** / **UNMAPPED** / outside the taxonomy | `REMOVE_UNMAPPED_HUMAN_FAMILY_PAIR` | A resolved side takes the human family (MAPPED). An unresolved side becomes `""` / `UNRESOLVED_HUMAN_AUDIT`. Then `PARTIALLY_MAPPED` (or `FULLY_UNRESOLVED`), eligible `False`, reason `HUMAN_AUDIT_LOCAL_SENSITIVITY_FAMILY_UNRESOLVED` | 5 |
| 4 | Otherwise: C5 = **UNCERTAIN** (any C1), or C5 = INCLUDE with C1 = **INVALID** or **UNCERTAIN** | `LEAVE_OFFICIAL_PAIR_UNCHANGED` | All 7 pipeline fields keep the model value. The human label is treated as "no confirmed override" | 9 |
| — | C2 relation (any value) | not applied | Descriptive only (§2) | — |

By precedence class:
- RECONCILED_FINAL: APPLY 9, EXCLUDE 8, UNMAPPED 1, LEAVE 2.
- FIRST_CODER: APPLY 14, EXCLUDE 5, UNMAPPED 4, LEAVE 7.

**Ambiguity check: none.**
- Every human code that occurs (C1 ∈ {VALID, INVALID, UNCERTAIN}; C3/C4 ∈ taxonomy ∪ {AMBIGUOUS, UNMAPPED}; C5 ∈ {INCLUDE, EXCLUDE, UNCERTAIN}) maps to exactly one action under the ordered rules above.
- The observed C5 × C1 combinations are:

  | C5 × C1 | n |
  |---|---:|
  | INCLUDE × VALID | 28 |
  | EXCLUDE × INVALID | 9 |
  | UNCERTAIN × UNCERTAIN | 6 |
  | EXCLUDE × VALID | 3 |
  | EXCLUDE × UNCERTAIN | 1 |
  | INCLUDE × INVALID | 1 |
  | INCLUDE × UNCERTAIN | 1 |
  | UNCERTAIN × VALID | 1 |

**Interaction with clauses A/B and D.** Rows 1–3 override the model label. Row 4 retains the model value. This is the documented translation of the human code "no confirmed override", so it is not an inferred correction. It changes no other record.

## 4. Join key and record verification

- **Join key:** `record_id` (format `REC-<16 hex>`).
  - V9: `FIRST_CODER_50_FINAL_FROZEN.csv.record_id` and `HUMAN_RECONCILED_20.csv.record_id`.
  - V5: `ANALYTICAL_FREEZE_RECORD_LEVEL.csv.record_id` (`fbb5f592…5a8f`; 6,499 rows, 6,499 unique).

| Check | Result |
|---|---|
| Unique audited records | **50** (FIRST_CODER_50: 50 rows, 50 unique) |
| RECONCILED_FINAL / FIRST_CODER | **20 / 30** (reconciled IDs ⊂ first-coder IDs; reconciled basis: 19 HUMAN_ADJUDICATION + 1 UNANIMOUS_PRE_ADJUDICATION) |
| Each audited record joins exactly one V5 row | **50/50**, 0 join problems. All 50 are in the 3,125 pair-eligible file |
| Reconciled FINAL labels vs event log | 19 events. 19/19 `current_event_hash` recomputed (SHA-256 of sort-keyed compact UTF-8 JSON). 18/18 prev-links, and event 1 links to the recomputed genesis (`D10F2CAC…`). 19/19 row → event FINAL_C1..C5 and event-hash equal. The unanimous row has FINAL = FIRST = BLIND |
| Conflicting final labels | **0**. Each record has exactly one label source under the precedence rule. The 18/20 first-coder ≠ FINAL differences (V1.8 04 T5) are resolved by precedence, not in conflict |
| V9 snapshot model labels vs V5 freeze row (AI family, Decision family, eligible) | 0 mismatches |
| Re-derived actions and pipeline values vs sidecar `HUMAN_AUDIT_LOCAL_CORRECTION_MAP.csv` | 0 mismatches (50/50) |
| Records whose pipeline fields change | 37 (the other 13 are APPLY-with-identical-labels or LEAVE) |
| Expected pair-eligible delta | **−18** (3,125 → 3,107) |

The `REANALYSIS_CANDIDATES_FROM_HUMAN_AUDIT.csv` (44 rows) is **not** used (V1.8.1 15 §1).

## 5. Application procedure (for the later revised run; not executed here)

- **Applier:** `tools\S\s_apply_propagation.py` (hash in 45).
- **Inputs:**
  - the hash-pinned 44 manifest;
  - a WORK copy of `V5\09_ANALYTICAL_FREEZE\analytical_freeze_v2_20260918T132206Z\`, with the 5 freeze hashes checked.
- **What it writes:** a new freeze directory. The applier:
  - checks every manifest row's `old_model_*` against the freeze row (STOP on mismatch);
  - writes only the 50 rows' `final_*` values and copies all 6,449 others unchanged;
  - regenerates the eligible CSV and updates canonical/manifest counts, as the reference implementation does.
- **Intended output directory:** `CC\revised_audited_label_analysis\<UTC timestamp>\`.

**Known issue for the revised-run phase (flagged, not resolved here):** the accepted stage scripts hard-code gate constants for the baseline.
- Stage 10: `EXPECTED["freeze_sha256"]`, `pair_eligible_records = 3125`, `pair_excluded_records = 3374`, `pair_eligible_unique_documents = 783`.
- Stage 11: `EXPECTED_MATRIX_SHA256`, `EXPECTED_M = 2180`.
- Stage 12: `EXPECTED` `matrix_sha256`, `null_sha256`, `dedup_M`, `raw_M`, `documents`.
- Stage 13: `EXPECTED_ROBUST_SHA256`, `EXPECTED_NULL_SHA256`, `EXPECTED_ROBUST_CORE = 32`.

Under substituted labels these gates fail by design. The V9 sidecar re-pinned them, which is not a path-only edit (generator lines 457–492). Whether gate-constant re-pinning is a permitted edit class must be decided before the revised run. It does not affect the Phase 3 baseline, which needs no such edit.

```
PROPAGATION_RULE=BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1 (FROZEN)
PROPAGATION_RECORDS=50 (RECONCILED_FINAL=20, FIRST_CODER=30)
JOIN_KEY=record_id; JOIN=50/50 unique, 0 duplicate, 0 unresolved
CONFLICTING_FINAL_LABELS=0
TRANSLATION=RECOVERED_SIDECAR_TRANSLATION (code 021e3d10…, policy 33d4d44c…); AMBIGUOUS_CODES=0
ACTIONS: APPLY=23, REMOVE_EXCLUDED=13, REMOVE_UNMAPPED=5, LEAVE=9; EXPECTED_ELIGIBLE_DELTA=-18
PHASE1_GATE=PASS; STOP=NONE
```
