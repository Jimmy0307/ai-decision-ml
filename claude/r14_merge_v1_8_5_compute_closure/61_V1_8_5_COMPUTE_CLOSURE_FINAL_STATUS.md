# 61 — V1.8.5 Compute Closure Final Status

**Round:** COMPUTATIONAL CLOSURE RUN — V1.8.4 baseline reproduction → V1.8.5 full audited-label reanalysis. Date: 2026-10-14.

```
REPO=https://github.com/Jimmy0307/ai-decision-ml
BRANCH=research/v1.8.4-v1.8.5-compute-closure-20261014
BASE_COMMIT=1d511eb4119b5a28c4f6f5e55b3accb0dd6bff30
FINAL_COMMIT=(this commit; recorded in the push report)

V5_PROTECTED_INPUTS=37/37
PROPAGATION_RULE=BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1
PROPAGATION_RULE_APPROVED=YES
PROPAGATION_TARGETS=50
PROPAGATION_MATCHED=50

BASELINE_REPRODUCTION=PASS
OFFICIAL_OUTPUTS_REPRODUCED=13/13
BYTE_IDENTICAL=13/13

FULL_REANALYSIS_EXECUTED=YES   (AUDITED_LABEL_SENSITIVITY_ANALYSIS)

STRICT_RECORDS_BASELINE=6499
STRICT_RECORDS_REVISED=6499
PAIR_ELIGIBLE_BASELINE=3125
PAIR_ELIGIBLE_REVISED=3107
UNIQUE_DOCS_BASELINE=783
UNIQUE_DOCS_REVISED=781
DOCUMENT_EDGES_BASELINE=2180
DOCUMENT_EDGES_REVISED=2181
PRIMARY_SIGNIFICANT_BASELINE=47
PRIMARY_SIGNIFICANT_REVISED=47
ROBUST_CORE_BASELINE=32
ROBUST_CORE_REVISED=32
ENRICHED_BASELINE=16
ENRICHED_REVISED=15
DEPLETED_BASELINE=16
DEPLETED_REVISED=17
ROBUST_CORE_GAINED=HUMAN_AUGMENTATION x RISK_ASSESSMENT (DEPLETED)
ROBUST_CORE_LOST=COORDINATION_EXECUTION x GENERAL_DECISION_PROCESS (ENRICHED)

G01_G16_REMOVED=0
G01_G16_DIRECTION_CHANGED=0
G01_G16_REVISED_STATUS=STABLE_UNDER_FULL_AUDITED_LABEL_REANALYSIS
LOCAL_SIDECAR_COMPARISON=EXACT_MATCH

CORPUS_WIDE_HUMAN_VALIDITY=NOT_ESTABLISHED
PRIMARY_BASELINE_REPLACED=NO
V1_S1_HASH_CHANGED=NO
ENTERPRISE_MODEL_CHANGED=NO

COMPUTATIONAL_VALIDATION_STATUS=CLOSED_WITH_BOUNDED_HUMAN_VALIDITY
V1_HUMAN_CONSTRUCT_VALIDATION=READY_TO_DISTRIBUTE
V1_HUMAN_RESULTS=NONE
SUBMISSION_READY=NO
```

## Gates passed, in order

1. **Identity gate:** base `1d511eb`, main `1f2e72f`, V1.8.2 `e2781b6`, 0 tags, worktree clean.
2. **Propagation freeze, before any run.** Recorded in 43–45:
   - exactly 50 records, 20 RECONCILED_FINAL and 30 FIRST_CODER;
   - unique join on `record_id`;
   - 0 conflicting labels;
   - the human-code translation taken from the recovered sidecar policy, with no ambiguous codes;
   - the applier script hash pinned before it was run.
3. **Baseline reproduction, original guards and model labels** (46–50): 13 of 13 outputs byte-identical. Patches were path-only: 5 lines in 4 hunks.
4. **Researcher-approved dual-mode guard policy.** In REVISED_GUARD_POLICY, REVISED_GUARD_DIFF and REVISED_GUARD_SELF_AUDIT:
   - 13 lineage guards were re-pinned, each confirmed by an independent recount;
   - 4 checks based on scientific results became OBSERVED_RESULT checks, recorded rather than used to abort;
   - structural invariants still hard-fail;
   - the self-audit found 0 statistical hunks.
5. **Revised run** (51–55):
   - the 50 substitutions were applied, 37 of them changing fields, and 0 non-target rows changed;
   - stages 10–13 were rerun with the historical seeds;
   - G01–G16 are stable (Case A), so no memo 56 was needed.
6. **Independent verification** (57): PASS. The orchestrator's forensic audit (60), with its own script, also passes on every item.
7. **Comparison with the V1.8 local sidecar** (58): EXACT_MATCH. All 120 rows have zero difference, and the revised core equals the sidecar core `4e412a07…`.

## Positioning (unchanged authority)

The primary analysis remains the pre-frozen V5/R14 baseline. The revised run is an audited-label sensitivity analysis: it applies a bounded substitution of 50 targeted human-audit labels and fully reruns every label-dependent analysis. It does not replace the primary baseline, and it does not establish corpus-wide human validity.

The manuscript v1.8.5 (59 .md/.docx) keeps the two sets of numbers apart. Primary-analysis and sensitivity-analysis numbers are never mixed; the sensitivity result appears in Table 4-9B.

## Where the outputs are

- **Compute outputs (local, not in git):** `C:\NTUST_PAPER\outputs\00_CURRENT\06_COMPUTE_CLOSURE_V1_8_5\compute_closure\`. Every file is hashed in `62_COMPUTE_OUTPUT_HASH_INDEX.csv`.
- **Revised stage-13 results freeze:** copied into `revised_results_freeze/` in this folder, 11 files.
- **Patched code copies and run records:** `…\06_COMPUTE_CLOSURE_V1_8_5\work\`.

## Researcher decisions still open

- Whether to ever replace the primary baseline with the revised analysis. This round set `PRIMARY_BASELINE_REPLACED=NO`.
- Whether `HUMAN_AUGMENTATION × RISK_ASSESSMENT`, which entered the core in the sensitivity analysis, should be discussed as a candidate. It is not added to the G list.
- Remaining items from 137:
  - V1 human coding (packets ready);
  - enterprise sources, ethics, parameter identification and V7;
  - author metadata and submission formatting.
