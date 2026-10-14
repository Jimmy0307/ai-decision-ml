# AI × Decision V5 Final Results Freeze

**Verdict:** `FINAL_RESULTS_FREEZE_ACCEPTED`

## Final robust result set

- Robust core: **32 / 120 cells**
- Robust enrichment: **15**
- Robust depletion: **17**

## Promotion rule

A cell is promoted to the final robust core only when it is significant at q ≤ .05 and has the same direction under the main fixed-degree Monte Carlo test, exact hypergeometric test, document-preserving null, and raw-record sensitivity analysis.

## Top robust enrichments

- #1 `RETRIEVAL_SYNTHESIS` × `INFORMATION_SYNTHESIS`: O=7, E=0.95, O/E=7.375, document q=0.016612
- #2 `HUMAN_AUGMENTATION` × `HUMAN_REVIEW_ACCOUNTABILITY`: O=57, E=16.06, O/E=3.549, document q=0.002181
- #3 `PREDICTION_RISK_ESTIMATION` × `PREDICTION_DIAGNOSIS`: O=220, E=70.75, O/E=3.109, document q=0.002181
- #4 `RETRIEVAL_SYNTHESIS` × `INFORMATION_ACQUISITION`: O=21, E=6.77, O/E=3.102, document q=0.002181
- #5 `EXPLANATION_ASSURANCE` × `HUMAN_REVIEW_ACCOUNTABILITY`: O=74, E=26.80, O/E=2.761, document q=0.002181
- #6 `EVALUATION_ASSESSMENT` × `EVALUATION_SELECTION`: O=44, E=17.27, O/E=2.548, document q=0.002181
- #7 `RECOMMENDATION_OPTIMIZATION` × `GENERAL_DECISION_PROCESS`: O=40, E=17.10, O/E=2.339, document q=0.002181
- #8 `PREDICTION_RISK_ESTIMATION` × `RISK_ASSESSMENT`: O=82, E=35.38, O/E=2.318, document q=0.002181
- #9 `COORDINATION_EXECUTION` × `ALLOCATION_PLANNING`: O=67, E=30.09, O/E=2.226, document q=0.002181
- #10 `EXPLANATION_ASSURANCE` × `GOVERNANCE_OVERSIGHT`: O=100, E=52.83, O/E=1.893, document q=0.002181

## Top robust depletions

- #1 `HUMAN_AUGMENTATION` × `RISK_ASSESSMENT`: O=1, E=12.71, O/E=0.079, document q=0.032510
- #2 `HUMAN_AUGMENTATION` × `PREDICTION_DIAGNOSIS`: O=3, E=25.42, O/E=0.118, document q=0.002181
- #3 `PREDICTION_RISK_ESTIMATION` × `HUMAN_REVIEW_ACCOUNTABILITY`: O=7, E=44.70, O/E=0.157, document q=0.002181
- #4 `COORDINATION_EXECUTION` × `RISK_ASSESSMENT`: O=3, E=16.92, O/E=0.177, document q=0.002181
- #5 `EXPLANATION_ASSURANCE` × `ALLOCATION_PLANNING`: O=7, E=37.72, O/E=0.186, document q=0.002181
- #6 `GENERATION_SYNTHESIS` × `PREDICTION_DIAGNOSIS`: O=7, E=37.52, O/E=0.187, document q=0.002181
- #7 `HUMAN_AUGMENTATION` × `EVALUATION_SELECTION`: O=2, E=9.82, O/E=0.204, document q=0.040492
- #8 `RECOMMENDATION_OPTIMIZATION` × `HUMAN_REVIEW_ACCOUNTABILITY`: O=8, E=36.09, O/E=0.222, document q=0.002181
- #9 `EVALUATION_ASSESSMENT` × `PREDICTION_DIAGNOSIS`: O=10, E=44.72, O/E=0.224, document q=0.002181
- #10 `PREDICTION_RISK_ESTIMATION` × `GOVERNANCE_OVERSIGHT`: O=25, E=88.12, O/E=0.284, document q=0.002181

## Canonical artifact

`eafa9c7efbde222f057bffa10e1f676081bf9fdef64e2d3a4cc0723211654dc4`

## Hard checks

- `robustness_manifest_accepted`: **PASS**
- `null_manifest_accepted`: **PASS**
- `robustness_sha_exact`: **PASS**
- `null_sha_exact`: **PASS**
- `main_null_cell_count_exact`: **PASS**
- `comparison_cell_count_exact`: **PASS**
- `robust_input_count_exact`: **PASS**
- `final_core_count_exact`: **PASS**
- `robust_keys_unique`: **PASS**
- `robust_keys_unique_structural`: **PASS**
- `final_core_matches_robust_input_structural`: **PASS**
- `partition_complete_structural`: **PASS**
- `full_sensitivity_set_matches_structural_set`: **PASS**
- `all_structurally_robust`: **PASS**
- `all_full_sensitivity_robust`: **PASS**
- `all_main_q05`: **PASS**
- `all_exact_q05`: **PASS**
- `all_document_q05`: **PASS**
- `all_raw_q05`: **PASS**
- `unexpected_direction_zero`: **PASS**
- `partition_exact`: **PASS**
- `duplicate_null_keys_zero`: **PASS**
- `duplicate_robust_keys_zero`: **PASS**
- `input_errors_zero`: **PASS**
- `join_errors_zero`: **PASS**
- `taxonomy_shape_exact`: **PASS**
