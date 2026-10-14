# 58 — V9 local sidecar vs V1.8.5 full audited-label reanalysis (sub-agent S)

**Purpose and inputs.** The sidecar numbers were used **only as a cross-check**. They were never an input to the revised run.
- **The revised run's inputs** were the baseline freeze copy, manifest 44 and the pinned applier.
- **The comparison script** was `tools\S\s_revised_compare.py`, output `tools\S\revised_compare_summary.json`.
- **The sidecar sources** (WORK copies; the copies' hashes were verified):
  - V9 `ROBUST_CORE_LOCAL_SENSITIVITY.csv` (`e3166ee1…5b59`);
  - SIDECAR `V5_CORRECTED` final run directories: 48 files copied to `WORK\inputs_S_sidecar_corrected_20261014\`, 0 hash mismatches.

## 1. Headline numbers (V1.8 04 / 17 §C vs this run)

| Quantity | V1.8 local sidecar | V1.8.5 full reanalysis | Match |
|---|---|---|---|
| Pair-eligible | 3,125 → 3,107 | 3,125 → 3,107 | = |
| Unique documents | 783 → 781 | 783 → 781 | = |
| Document edges | 2,180 → 2,181 | 2,180 → 2,181 | = |
| Robust core | 32 → 32 | 32 → 32 | = |
| Enriched / depleted | 16/16 → 15/17 | 16/16 → 15/17 | = |
| Gained | `HUMAN_AUGMENTATION × RISK_ASSESSMENT` DEPLETED | same | = |
| Lost | `COORDINATION_EXECUTION × GENERAL_DECISION_PROCESS` ENRICHED | same | = |
| Main observed changed / main direction changed | 24 / 3 cells | 24 / 3 cells | = |
| Main q ≤ .05 / ≤ .01 | 47 / 32 | 47 / 32 | = |
| G01–G16 removed | 0 | 0 | = |

## 2. All 120 rows of `ROBUST_CORE_LOCAL_SENSITIVITY.csv`: sidecar columns vs revised outputs

| Sidecar column | Revised source column | Mismatching rows | Max abs diff |
|---|---|---:|---:|
| `sidecar_observed` | main `observed` | 0 | 0 |
| `sidecar_main_direction` | main `direction` | 0 | — |
| `sidecar_main_q` | main `q_bh_two_sided` | 0 | 0.0 |
| `sidecar_exact_observed` / `_direction` / `_q` | comparison `dedup_observed`, `exact_direction`, `exact_q` | 0 / 0 / 0 | 0.0 |
| `sidecar_document_observed` / `_direction` / `_q` | comparison `dedup_observed`, `document_null_direction`, `document_null_q` | 0 / 0 / 0 | 0.0 |
| `sidecar_raw_observed` / `_direction` / `_q` | comparison `raw_observed`, `raw_direction`, `raw_q` | 0 / 0 / 0 | 0.0 |
| `sidecar_core_member` / `sidecar_core_direction` | `FINAL_ROBUST_CORE_32.csv` | 0 / 0 | — |
| (control) `official_core_member` | baseline reproduced core | 0 | — |

All q values agree to full float precision, with max abs diff 0.0 in every q column.

## 3. Artifact-level comparison with SIDECAR `V5_CORRECTED`

- **Byte-identical: 33 of 47 same-named files.** These include:
  - the corrected `ANALYTICAL_FREEZE_RECORD_LEVEL.csv` (`89422095…16cc`) and `ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv` (`ba72b3ed…73af`), which equal the sidecar `LOCAL_HUMAN_CORRECTION_MANIFEST.json` pins;
  - every stage 10–13 data CSV (edges, matrices, 120-cell results for all 4 methods, comparison, robust cells);
  - **`FINAL_ROBUST_CORE_32.csv` = `4e412a07af1f5c9e2f304408875fc1fc47018c9ff501a17dee437bea880e95a0`**. This equals V9 `FINAL_STATUS.json` `sidecar_core_sha256`.
- **Not byte-identical: 14 files.** They are the 5 canonical JSONs, 5 manifests and 4 summaries. Flattened field comparison of the canonicals gives:
  - **09 canonical:** only `local_sensitivity_derivative.scope` (`BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1` vs `LOCAL_HUMAN_AUDIT_SENSITIVITY_ONLY`) and the added `propagation_manifest_sha256`. This is provenance metadata written by the pre-registered applier.
  - **10 / 11 / 12 / 13 canonicals:** only the lineage hash fields that inherit from it (`source_analytical_freeze_sha256`, `source_document_matrix_sha256`, `source_matrix_sha256` + `source_null_sha256`, `source_robustness_sha256` + `source_null_model_sha256`).
  - **Manifests and summaries:** they contain those hashes plus `generated_utc` and paths.
  - **No numeric or categorical field differs.**

## 4. Verdict

**`EXACT_MATCH`** at the result level:
- all 120 cells × all 4 methods (observed, direction, q);
- core membership and directions;
- every data CSV byte-identical, including the core file `4e412a07…`.

At the artifact level, the canonical/manifest JSONs are a SEMANTIC_MATCH_WITH_SERIALIZATION_DIFF, with lineage and provenance metadata only. That difference is explained in §3.

**Interpretation.** The pre-registered BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1, applied with the pinned applier and the accepted stage scripts:
- independently regenerates the V9 local sidecar result exactly;
- moves the 2026-10-03 sidecar's status from "reported by the sidecar run" to "independently re-executed and hash-matched".

The result is still a 50-record targeted substitution. It is not a corpus-wide correction, and no error rate is extrapolated.

```
SIDECAR_VS_FULL_REANALYSIS=EXACT_MATCH (results; core 4e412a07 byte-identical; 120x4 q max diff 0)
ARTIFACT_LEVEL=33/47 byte-identical; 14 differ only in lineage/provenance hash, time and path fields
```
