# Route A analysis scripts (2026-11-18)

These are the scripts behind [`docs/review/20261118_data_validity/DATA_VALIDITY_VERDICT.md`](../../docs/review/20261118_data_validity/DATA_VALIDITY_VERDICT.md). They need Python 3.11 with `numpy` and `scipy`.

**The inputs are not in this public repository.** The scripts expect a local workspace laid out like this:

```text
<workspace>/scripts/        <- these files
<workspace>/inputs_LOCAL_ONLY/
<workspace>/outputs/
```

`inputs_LOCAL_ONLY/` holds files from the V9 research archive (analytical freeze, document edges, official test results, human audit files) and three metadata files (`docs.csv`, `records_all.csv`, `records_strict.csv`) from the researcher's private snapshot. Those files contain evidence text from copyrighted papers, so they are kept out of public storage.

| Script | Purpose |
|---|---|
| `ra_lib.py` | Engine: stub Monte Carlo, exact hypergeometric, document-preserving swap null, raw-record test, BH, core rule |
| `step0_lineage.py` | Checks that the metadata matches the official freeze |
| `step1_taxonomy.py`, `step_common.py` | Confusion evidence; κ and Krippendorff α under T0/T1/T2 |
| `step2_reliability_design.py`, `score_reliability.py` | Human reliability study design and gate scorer (prepared, not run) |
| `step3_pipeline_validation.py`, `step3b_seed_stability.py` | Re-implementation vs official results; 20-seed stability |
| `step4_exclusion_bias.py`, `step4e_sensitivity.py` | Filter/mapping selectivity, keyword triangulation, same-term removal |
| `step5_track_sensitivity.py`, `step6_temporal_validity.py` | Track-stratified null; persistence test |
| `step7_misclassification.py` | Analytic error bound and misclassification simulation |
| `step8_prepare_model_coding.py`, `step8b_score_model_coding.py` | Blind multi-LLM coding batches and scoring |
| `step9_rule_based_primary.py` | Keyword-only matrix through the full test pipeline |
| `build_master_table.py`, `build_codebook.py`, `run_all.py`, `test_route_a.py` | Summary table, codebook generator, runner, unit tests |
