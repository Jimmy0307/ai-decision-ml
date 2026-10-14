# 53 — Global Pipeline Diff: baseline vs revised audited-label reanalysis (V1.8.5, sub-agent S)

| Run | Location |
|---|---|
| Baseline (reproduced; 13/13 byte-identical to official) | `CC\baseline_reproduction\20261014T041645Z\` |
| Revised | `CC\revised_audited_label_analysis\20261014T042729Z\` |

**Rule:** BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1 (43/44).
- 50 targets, 50 matched, 50 applied, 37 records with changed fields.
- 0 unauthorized replacements (51).

**Seeds and replicates:**
- Main null: seed 20260918, 10,000 replicates.
- Document-preserving null: seed 20260919, 5,000 replicates, burn-in 20/edge, thinning 2/edge.

**Computed by:** `tools\S\s_revised_compare.py`, output `tools\S\revised_compare_summary.json`. The independent recomputation (57) agrees.

**Label-dependent stages re-run: 10, 11, 12, 13.**
- Stage-09-level pair eligibility (mapped-record and pair eligibility) is **not recomputed inside stage 10**.
  - Stage 10 takes the eligible frame as the rows of `ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv`.
  - It only *validates* `analytical_pair_eligible`, `mapping_completeness = FULLY_MAPPED` and the family membership of each row.
  - The eligibility re-derivation for the 50 records is done by the pre-registered applier, using the recovered translation. The applier regenerates the eligible file from the record-level `analytical_pair_eligible` flag.
- No other label-dependent stage exists between 09 and 13. Stages 11–13 read only the outputs of stages 10–12.
- Stage 14 (the manuscript data pack) is a packaging step and was not run.

| Quantity | Baseline | Revised | Δ |
|---|---:|---:|---:|
| Strict records | 6,499 | 6,499 | 0 |
| Pair-eligible records (raw M) | 3,125 | 3,107 | −18 |
| Pair-excluded records | 3,374 | 3,392 | +18 |
| Unique documents (pair-eligible) | 783 | 781 | −2 |
| Document-level edges (M) | 2,180 | 2,181 | +1 |
| Cells | 120 (10 × 12) | 120 (10 × 12) | 0 |
| Primary significant, main null BH q ≤ .05 | 47 | 47 | 0 |
| Main null q ≤ .01 | 34 | 32 | −2 |
| Exact hypergeometric q ≤ .05 | 46 | 47 | +1 |
| Document-preserving q ≤ .05 | 32 | 32 | 0 |
| Raw-record q ≤ .05 | 54 | 55 | +1 |
| Robust core | 32 | 32 | 0 |
| Enriched | 16 | 15 | −1 |
| Depleted | 16 | 17 | +1 |
| Cells with a changed main (dedup) observed count | — | 24 / 120 | |
| Cells with a changed raw-record count | — | 28 / 120 | |
| Main-null direction flips | — | 3 / 120 (all non-core) | |
| Core membership | — | 31 unchanged, +1 gained, −1 lost | |
| Core direction changes among shared members | — | 0 | |

**Gained and lost core cells (54):**
- **GAINED:** `HUMAN_AUGMENTATION × RISK_ASSESSMENT` (DEPLETED). Document-null q goes from .0567 to .0325, and its own O = 1 is unchanged.
- **LOST:** `COORDINATION_EXECUTION × GENERAL_DECISION_PROCESS` (ENRICHED). Document-null q goes from .0434 to .0610, and its own O = 19 is unchanged.

**Main-null direction flips.** All three are non-core: `EVALUATION_ASSESSMENT × INFORMATION_SYNTHESIS`, `GENERATION_SYNTHESIS × ALLOCATION_PLANNING` and `RECOMMENDATION_OPTIMIZATION × EXECUTION_COORDINATION`.

**Hashes:**

| Artifact | Baseline | Revised |
|---|---|---|
| Final core | `a43b4b58…bd50` | `4e412a07af1f5c9e2f304408875fc1fc47018c9ff501a17dee437bea880e95a0` |
| Results canonical | — | `eafa9c7e…54dc4` |
| Matrix canonical | — | `692f8702…0b28` |
| Null canonical | — | `2f1cafe2…57ba` |
| Robustness canonical | — | `32b15da0…2e52` |
| Revised freeze canonical | — | `c1afa617…fdb0` |
| Record-level | `fbb5f592…` | `89422095…16cc` |
| Eligible | `9ee5fd53…` | `ba72b3ed…73af` |

The revised OBSERVED_RESULT checks were recorded, not enforced: core = 32, so `robust_input_count_exact`, `final_core_count_exact`, `robust_keys_unique` and `partition_exact` all record `true`.

```
STRICT=6499→6499; ELIGIBLE=3125→3107; DOCS=783→781; EDGES=2180→2181
PRIMARY_Q05=47→47; CORE=32→32; ENRICHED=16→15; DEPLETED=16→17
```
