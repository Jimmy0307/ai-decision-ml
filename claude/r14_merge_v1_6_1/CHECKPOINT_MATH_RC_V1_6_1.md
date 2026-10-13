# R14 × Enterprise Math RC v1.6.1

Date: 2026-10-13

Canonical branch: `calibration/v1.1-variable-model`
Base branch head before publication: `e78d2f599d575c9b924e261bce9b93387970d870` (which already descends from `ce3e1b2bf8432d1d949e95b2cd8d392d2a21ed4b`).

## Scope

This checkpoint records the v1.6.1 mathematical-model RC. The change is deliberately narrow:

1. `IMPLEMENTATION_YEAR` is the canonical staffing/capacity regime: physical BUILD hours are charged in full in the implementation year, plus RUN hours.
2. `STEADY_STATE_LEVELIZED` remains sensitivity-only; AF-weighted BUILD hours must not be presented as implementation-year feasibility.
3. Original 06 comparison names (`VSC`, `VCP`, `DL`, `NEV`, etc.) are reserved for `PLANE_OFF`; `SKILL_FIXED` uses `^{W,fix}` labels and `ENDOGENOUS` uses `^{ENG}` labels.
4. A single-skill collapse regression requires `SKILL_FIXED` to equal `PLANE_OFF` when engineering demand/capacity are aggregated to one ENG resource and external capacity is disabled.

No change is made to R14 frozen numbers, 51/65, alpha/rho semantics, A/B/C/C0/A+/D baseline semantics, or `org_schema.py`.

## Verification

- TDD regression: `4 passed`.
- 124 acceptance tests: 17 total, with fresh tests 16 and 17 PASS.
- Test 12 (A/B/C backward reproduction) uses the previously certified v1.6 14-case / 386-comparison snapshot because 51 was not materialized in this execution environment. The current remote 51 blob at the branch base has SHA `7ec816284010bf4e743cdc356fa5d3a27f097134`, and the v1.6.1 `Adapter51`, `load51`, and `crosscheck51` code paths are byte-for-byte unchanged from v1.6.
- All numerical examples are `SIMULATED_ONLY`.
- `ORG_MAPPING_HUMAN_VALIDATION = PENDING`.
- `ENTERPRISE_EMPIRICAL_STATUS = PENDING`.

## Deliverable SHA-256

- `119_ENTERPRISE_AI_CANONICAL_MATHEMATICAL_MODEL_v1_1.md`: `1943f860d08b2877ace166ef17d484096db26fbfcfe3c5bf15a3c2691e130b5f`
- `120_MATHEMATICAL_SYMBOL_DICTIONARY_v1_1.xlsx`: `8b38369951729bc6b301731e0d4e1e0a583a8d79ea9b42ea440cc5bc452d31b6`
- `121_ENGINEERING_ECONOMIC_LEDGER_v1_1.xlsx`: `ddd2f8d8ad633d2aea3a1da9e5d70734dd7208cd236bf4f59fc3be5cc9040d32`
- `122_ENGINEERING_SOURCING_MODEL_SPEC_v1_1.md`: `9b7bf400a2c4298aaae579e452150e6e12f722efb8672d42ae68e750563a10a3`
- `123_ENGINEERING_SOURCING_SYNTHETIC_EXAMPLE_v1_1.xlsx`: `5cb3af68daaf13b4f229451dc25728f28b14cfc22a1e76582a118daa86a59128`
- `124_engineering_sourcing_model_reference.py`: `1a1aa58c1ad235b5fea6682401288be534f9fb98af6f6d282ccdab36e1cce995`
- `125_ENGINEERING_SOURCING_MODEL_RUN_v1_1.txt`: `9c6a5f0cd02274124953a55e52daa94aae9527aaeeb1e2d419e04fff7e97e12e`
- `126_MATHEMATICAL_MODEL_FORENSIC_AUDIT_v1_1.md`: `417c7294ff91c0a44c96c4539011c33820f350be86569ec4c8fd9f1e132483bd`
- `127_MERGED_MASTER_THESIS_R14_TO_ENTERPRISE_v1_6_1_MATH_RC_CANDIDATE.md`: `a511e1ec39e40e6088769380d960eecd76d42d9ffba85dcf8365db8641717ca2`
- `r14_merge_v1_6_1_deliverables.zip`: `3290c42a290b967e68f168531d33f7b6190c7476d83cb8ba2be7f956b472d6fc`

Status: `MATH_RC_V1_6_1_READY_FOR_REVIEW`; this is not an enterprise empirical freeze.