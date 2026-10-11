# Calibration branch — Enterprise AI Adoption v2.0

## Governing status

2026-10-10 scope correction: the active research object is now **enterprise-wide AI adoption as a multilevel decision system**. Earlier development stages narrowed the empirical design to a small number of vertical process examples; that direction is superseded and no longer governs the branch.

The branch preserves historical evidence needed for auditability, but the current canonical research-design chain begins at files 38–40.

## Canonical reading order

1. `38_ENTERPRISE_AI_ADOPTION_RESEARCH_ARCHITECTURE_v2_0.md`
   - enterprise-wide research boundary
   - Enterprise > Business Unit / Function > AI Initiative / Shared Capability > Role-specific Users
   - G01–G16 → M1–M4 → enterprise adoption architecture
   - RQ1–RQ5

2. `39_ENTERPRISE_MULTILEVEL_MODEL_AND_DATA_CONTRACT_v2_0.md`
   - Enterprise–Business Unit bilevel / portfolio model
   - role-specific conditional user response `ρ`
   - shared platform/governance costs vs local implementation costs
   - cross-unit budget/capacity/policy coupling
   - enterprise V0–V7 gates

3. `40_MANUSCRIPT_CH1_3_ENTERPRISE_SCOPE_v2_0.md`
   - formal design-stage manuscript, Chapters 1–3
   - no firm-specific effect or ROI claim

4. `29_CLAIM_LEVEL_SOURCE_AUDIT_v1_5.md`
   - bounded literature claims that remain usable

5. `26_GAP_CONSTRUCT_TRACE_AND_ANCHORS_CANDIDATE_v1_3.md`
   - historical G01–G16 → M1–M4 candidate mapping and construct anchors
   - must be revalidated at enterprise interfaces before empirical freeze

6. `33_bilevel_validation_fixture_v1_5.py`, `34_VALIDATION_RUN_v1_5.md`, `35_schema_validator_synthetic_v1_6.py`, `36_SCHEMA_VALIDATION_RUN_v1_6.md`
   - synthetic implementation evidence only
   - not enterprise empirical calibration and not a complete v2.0 portfolio solver

## What remains valid from earlier work

- `main@1f2e72f` v1.0: historical simulated mathematical-feasibility regression only.
- G01–G16: literature-network research leads; not company gaps or weights.
- M1 Governance/Decision Rights, M2 Workflow/Integration, M3 Human–AI Configuration, M4 Evaluation/Assurance: static candidate mechanism layer.
- M5: longitudinal learning/resource-feedback extension only.
- ordinal/cardinal correction: 0–3 constructs are threshold/lookup keys, not direct utility arithmetic.
- provenance separation and `UNIDENTIFIED` missing-data rule.
- Boss–Manager critique: a third optimization layer is not assumed without independent discretion, different objectives/constraints, managerial anticipation, and counterfactual upstream impact.

## v2.0 model hierarchy

### Enterprise / Executive
Chooses strategy, policy, shared infrastructure/capabilities, risk appetite, budget, engineering capacity, and portfolio priorities.

### Business Unit / Functional Management
Chooses local configuration under enterprise constraints:

`x_j=(A_aut,j,H_j,WI_j,EA-V_j,m_j)`

where `j` is a business unit, function, initiative, or shared-capability deployment context rather than a fixed use case.

### Organizational users
Modeled by role-specific conditional response distributions:

`ρ_j(r|x_j,z,role,s)`

with responses such as use, verify, modify, escalate, reject, and bypass. A true third optimization layer is evidence-contingent.

## v2.0 economics

The enterprise model separates:

- `C_shared`: shared platform, infrastructure, security, governance, evaluation, and training costs
- `C_impl,j`: unit/initiative-specific implementation and maintenance
- `C_op,j`: operational/review/exception costs
- `V_j`, `L_j`: traceable value/loss lookups
- shared budget/capacity constraints and portfolio coupling

Shared costs are not replicated once per business unit.

## Validation status

No v2.0 enterprise empirical gate is currently claimed as passed.

- V0 enterprise authority/source evidence — OPEN
- V1 construct validity and blind G→M coding — OPEN
- V2 cross-functional pilot — OPEN
- V3 schema/units — PARTIAL synthetic evidence inherited from v1.5/v1.6
- V4 lookup completeness — PARTIAL synthetic rejection logic only
- V5 enterprise portfolio solver — OPEN / requires v2.0 implementation
- V6 sensitivity/invariance — PARTIAL historical synthetic evidence; enterprise Θ_adm scan OPEN
- V7 enterprise empirical calibration — OPEN

## Historical files and supersession rule

Earlier files remain only when they contribute provenance, review evidence, literature auditing, construct development, or reusable synthetic validation. Any statement that conflicts with files 38–40 is superseded.

The working branch must not reintroduce a single department/process as the central research object. Future empirical units are embedded evidence inside the enterprise architecture, not substitutes for the enterprise research boundary.