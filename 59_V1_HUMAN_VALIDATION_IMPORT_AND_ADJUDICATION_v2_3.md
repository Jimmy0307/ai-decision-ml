# 59 — V1 Human Validation: Import, Reliability and Adjudication Shell v2.3

**Status: `V1_HUMAN_BLIND_CODING_PENDING`.** No human response sheet has been received, so every result cell below reads `[HUMAN RESULT PENDING]`. The AI pilot (54C) is never imported here and never fills any cell. The analyzer `60_v1_human_validation_analyzer_v2_3.py` refuses AI coders and refuses any sheet identical to an AI-pilot output.

The pre-registered rules stay those of 53B §7, §9 and §11 (frozen; SHA-256 in `v1_blind/FREEZE_MANIFEST.txt` stage 1). This file adds no new criterion. It only fixes how human data enter, in which order, and where each number appears.

---

## 1. Workflow and freeze stages

| Step | Action | Evidence written | Command |
|---|---|---|---|
| 1 | Coordinator sends each human coder only `v1_human_packet/` (protocol §1–§8, clarifications v2.2.1, packet A or B, empty response sheet). Coders never get repository access: 54C already reveals the key. | delivery log (outside git) | — |
| 2 | Coder returns the sheet and signs the 53B §8 attestation | signed attestation (outside git; name kept by coordinator) | — |
| 3 | **Freeze stage 3.** Append the SHA-256 of every human sheet to `v1_blind/FREEZE_MANIFEST.txt`, and commit, before any analysis | manifest lines `<sha256>  human_<coder_id>.csv` | `sha256sum v1_human_import/human_*.csv >> v1_blind/FREEZE_MANIFEST.txt` |
| 4 | Fill `v1_human_import/coders.csv` (schema §2.2) | registry | — |
| 5 | **Stage R.** Reliability only; the key stays sealed | `v1_human_results/V1_HUMAN_RESULTS.json`, `TABLES_4_1.md` | `python 60_v1_human_validation_analyzer_v2_3.py --coders v1_human_import/coders.csv` |
| 6 | Disagreements go to coder discussion **without the key**, then to an adjudicator who did not author 41 (53B C5). Fill `v1_human_import/adjudication.csv` (schema §6) | adjudication file | — |
| 7 | **Freeze stage 4.** Append the SHA-256 of the adjudication file to the manifest, and commit | manifest line | `sha256sum v1_human_import/adjudication.csv >> v1_blind/FREEZE_MANIFEST.txt` |
| 8 | **Stage K.** Open the key (the hash must equal the 53A commitment `d1702188…6734`). The analyzer writes `# KEY_OPENED adjudication=<sha>` into the manifest. From then on, only that adjudication file is accepted, so final codes cannot change after the key is seen | results JSON / tables (provisional classes) | `python 60_… --coders … --adjudication v1_human_import/adjudication.csv --key <path>/sealed_key.json` |
| 9 | **Stage C.** For every changed case, write the 53B §11 class in a separate file `v1_human_import/classes.csv` (`case_id,model_change_class,rationale,manuscript_change`). Freeze it (stage 5), then rerun with `--classes`. The adjudication file itself is never edited after the key opening | classes file + manifest line | `python 60_… --adjudication … --key … --classes v1_human_import/classes.csv` |
| 10 | Transfer the tables into 44 §4.1; if C4 finds a `model-structural` change, revise 42/44 before claiming V1 | 44 v2.x | — |

The analyzer enforces steps 3, 5, 7, 8 and 9 mechanically.

**Independence and anti-copy checks.** The analyzer rejects:

- two coders with the same sheet (by hash or identical content);
- a sheet that copies at least 4 AI-pilot rationales verbatim.

The analyzer also enforces:

- it refuses sheets or adjudication files that are not hash-frozen;
- it refuses the key before the adjudication is frozen;
- it refuses a key whose hash differs from the commitment.

## 2. Import schemas

### 2.1 Coder A / Coder B response sheet (unchanged from 53B §6)

`case_id,primary_code,secondary_code,status,confidence,rationale,enterprise_decision_interface,new_construct_required,new_construct_reason`

| Field | Rule (validated by 60) |
|---|---|
| `case_id` | exactly C01–C16, once each |
| `primary_code` | one of `M1 M2 M3 M4 M5 OPTIONAL_DATA_GATED EVIDENCE_ONLY OTHER INSUFFICIENT_INFORMATION` |
| `secondary_code` | blank or one code from the same list, different from the primary |
| `status` | `static dynamic optional evidence-only insufficient` |
| `confidence` | integer 0–100 (descriptive only; never a weight) |
| `rationale` | required, 1–3 sentences |
| `new_construct_required` | `yes`/`no`; `yes` needs `new_construct_reason` |

Packets A and B contain the same 16 case IDs in different row orders. Coder A uses `RESPONSE_SHEET_A.csv` and Coder B uses `RESPONSE_SHEET_B.csv`; further coders alternate.

### 2.2 Coder registry `v1_human_import/coders.csv`

`coder_id,coder_type,packet,response_sheet,sheet_sha256,attestation_signed,attestation_date`

- `coder_type` must be `HUMAN`.
- `packet` is `A` or `B`.
- `response_sheet` is a path relative to the registry.
- `sheet_sha256` must equal both the file hash and a manifest line.
- `attestation_signed` must be `yes`.

At least two rows are required. Names are kept by the coordinator, not in git.

## 3. Primary-mechanism and status agreement

**Table 59.1 — Inter-coder reliability (human).** The decision uses α (53B C1/C3). κ and its bootstrap interval are reported alongside.

| Field | Coder pair | Agreement (n/16) | Cohen's κ | κ 95% bootstrap CI | Krippendorff's α (nominal) | α 95% bootstrap CI | 53B class (C1/C2/C3) |
|---|---|---|---|---|---|---|---|
| primary_code | A vs B | [HUMAN RESULT PENDING] | [HUMAN RESULT PENDING] | [HUMAN RESULT PENDING] | [HUMAN RESULT PENDING] | [HUMAN RESULT PENDING] | [HUMAN RESULT PENDING] |
| status | A vs B | [HUMAN RESULT PENDING] | [HUMAN RESULT PENDING] | [HUMAN RESULT PENDING] | [HUMAN RESULT PENDING] | [HUMAN RESULT PENDING] | [HUMAN RESULT PENDING] |

**Computation:**

- Raw agreement and Cohen's κ (Cohen, 1960) per coder pair.
- Krippendorff's α (nominal) across all coders.
- 95% percentile bootstrap over cases (5,000 resamples, seed 20261011), for both α and κ. Resamples with undefined κ (no variance) are dropped and their number is reported.
- The functions are the same `v1_blind/reliability_v2_2.py` functions used for the AI pilot, imported unchanged.
- Landis & Koch labels are **not** reported: the label boundaries could not be verified at the primary source (57 §R11, v2.3), and they were never a decision rule.

## 4. Secondary codes

**Table 59.2 — Secondary-code agreement.** Mean Jaccard of {primary ∪ secondary} over cases and coder pairs: [HUMAN RESULT PENDING]. Secondary codes are never used in the primary statistic (53B §7).

## 5. Disagreement matrix

**Table 59.3a — Primary code, Coder A (rows) × Coder B (columns).** Rows and columns: `M1 … M5, OPTIONAL_DATA_GATED, EVIDENCE_ONLY, OTHER, INSUFFICIENT_INFORMATION` (only codes actually used are printed). Cells: [HUMAN RESULT PENDING]

**Table 59.3b — Status, Coder A × Coder B.** Cells: [HUMAN RESULT PENDING]

**Table 59.3c — Case-level disagreements** (any of primary, secondary or status). Disagreement types follow 55: `PRIMARY`, `STATUS`, `SECONDARY`, `NEW_CONSTRUCT`. `KEY` is assigned only at stage K.

| Case | Coder A (p/s/status) | Coder B (p/s/status) | Type |
|---|---|---|---|
| [HUMAN RESULT PENDING] | | | |

Confidence is reported descriptively: the median per coder, and the median on agreed vs disagreed cases. [HUMAN RESULT PENDING]

## 6. Adjudication import (55 Block H)

`v1_human_import/adjudication.csv`:

`case_id,final_primary,final_secondary,final_status,resolution_route,adjudicator_role,evidence_used,rationale,model_change_class,manuscript_change`

**Rules:**

- **Coverage:** one row for every case with a primary or status disagreement. Agreed cases take the coders' common codes automatically.
- **`resolution_route`:** `CODER_CONSENSUS`, `INDEPENDENT_ADJUDICATOR` or `AUTHOR_ADJUDICATED`. Author-adjudicated cases are reported as a limitation (53B C5).
- **`model_change_class`:** must be **blank** in this file; the analyzer rejects it otherwise. Classes are written after stage K, in the separate `classes.csv` (stage C).
- **Freeze:** the file is frozen (stage 4) before the key is opened, and it is bound at the first opening.
- **Validation:** duplicate or unknown case IDs, and a final secondary code equal to the primary, are rejected.

**Table 59.4 — Adjudicated codes.**

| Case | Final (p/s/status) | Route | Adjudicator role | Rationale |
|---|---|---|---|---|
| [HUMAN RESULT PENDING] | | | | |

## 7. Researcher key comparison and mapping sensitivity (stage K)

**Table 59.5 — Final codes vs researcher key (53A).** The key is a hypothesis, not ground truth.

| Case | Gap | Final | Key | Primary = key | Status = key | Provisional class (60) | Confirmed class (adjudication) |
|---|---|---|---|---|---|---|---|
| C01–C16 | [HUMAN RESULT PENDING] | | | | | | |

**Provisional classification by 60 (53B §11), which a human must confirm:**

- `NO_CHANGE`: the final primary code and status equal the key.
- `REVIEW_POTENTIALLY_MODEL_STRUCTURAL`: the final code is `OTHER` (with a new-construct reason) or `INSUFFICIENT_INFORMATION`, or the final status is `insufficient`.
- `mapping-only (provisional)`: any other change. The basis is the 54C §5 finding that gaps select 42 elements but never parameterize them.

**Mechanism support check:** any of M1–M5 left with no supporting primary code after adjudication is flagged under 41 §7 rule 2. Its equation elements may stay for enterprise-architecture reasons, but the 44 claims that the gaps support that mechanism must be downgraded.

## 8. Special tracking — G04, G10, G11

These three cases are where the AI pilot (54C §4) diverged from the researcher key. They are tracked whatever the human result.

| Gap | Case | Researcher key | Why tracked | Human A | Human B | Final | Consequence if final ≠ key |
|---|---|---|---|---|---|---|---|
| G04 | C03 | EVIDENCE_ONLY / — / evidence-only | AI pilot: M4/static; no codebook test for "distinct" decision (clarification v2.2.1 adds one) | [HUMAN RESULT PENDING] | [HUMAN RESULT PENDING] | [HUMAN RESULT PENDING] | 41/44 counts change (static 13, evidence-only 0); mapping-only |
| G10 | C11 | M3 / M4 / optional | AI pilot: static; `optional` status not operationalised | [HUMAN RESULT PENDING] | [HUMAN RESULT PENDING] | [HUMAN RESULT PENDING] | "optional" restated as an identification condition (43 Block R); mapping-only |
| G11 | C01 | M5 / M4 / dynamic | AI pilot: M4/static with M5 secondary | [HUMAN RESULT PENDING] | [HUMAN RESULT PENDING] | [HUMAN RESULT PENDING] | M5 rests on G12 alone; the 41 §3 Q4 merge is flagged; mapping-only + manuscript-only |

The AI-pilot codes are printed by 60 in a separate "context only" column. They are never pooled with, substituted for, or used to adjudicate human codes.

## 9. Decision (53B §9, C1–C7)

| Condition | Output label |
|---|---|
| no human sheets | `V1_HUMAN_BLIND_CODING_PENDING` |
| reliability computed, adjudication/key not done | `V1_HUMAN_RELIABILITY_COMPUTED__ADJUDICATION_AND_KEY_PENDING` |
| C2: lower CI bound of α (primary) < .667 | `V1_ADDITIONAL_CODER_REQUIRED` |
| C1 or C3 `NOT_ACCEPTABLE` / undefined | `V1_NOT_PASSED` |
| any changed case without a confirmed class | `V1_PENDING_MAPPING_SENSITIVITY_CONFIRMATION` |
| any confirmed `model-structural` change | `V1_BLOCKED_MODEL_STRUCTURAL` (revise 42/44 first) |
| ≥ 2 human coders, C1 ≥ TENTATIVE and not IMPRECISE, C3 ≥ TENTATIVE, adjudication and key done, no structural change | `V1_PASS_HUMAN_C6` |

**Current decision: `V1_HUMAN_BLIND_CODING_PENDING`.**

The .800 / .667 thresholds are pre-registered study conventions. Their attribution to Krippendorff is still `[VERIFY]` at a primary source (57, v2.3 section).

## 10. Analyzer verification

`python 60_v1_human_validation_analyzer_v2_3.py --self-test` runs only on temporary fixtures labelled TEST and writes nothing to `v1_human_results/`. It checks:

- the κ oracle (0.5 on a known table);
- the C6 decision table;
- `PENDING` without input;
- rejection of unfrozen sheets, of `AI` coder types, of a renamed copy of an AI-pilot sheet, and of the same sheet registered as two coders;
- refusal of an adjudication file changed after the first key opening;
- refusal of the key before adjudication.

With `V1_SEALED_KEY` set, it also runs stages A and K on the TEST fixture and confirms that no PASS is produced.
