# Calibration Execution Plan v1.1

Base: v1.0 mathematical skeleton remains frozen on `main@1f2e72f1894c8d4eb7929c39756d7b6af607545b`.

Goal: replace simulated inputs with a transparent mixture of public observations, consented observations, expert elicitation, interval/fuzzy values and scenario/sensitivity parameters without changing the mathematical skeleton unless a true contradiction is discovered.

**New governing audit gate:** before use cases are frozen, review `20_CLAUDE_REVIEW_PACKET_GAP_TO_CONSTRUCT_MODEL_v1_1.md`. The mechanism consolidation, construct definitions, 0–3 anchors, requirement-threshold logic, ordinal/cardinal separation, and multilevel hierarchy must survive conceptual audit first.

## Phase 0 — Gap-to-construct audit

Review and resolve:

- G01–G16 → M1–M5/T1 mechanism assignments;
- D/R/A/G/H/WI/EA construct distinctness;
- 0–3 anchor observability;
- requirement-threshold interpretation;
- ordinal/cardinal separation;
- multilevel hierarchy validity;
- identification status of every parameter family.

**Go/No-Go Gate 0A:** do not freeze empirical use cases or issue a questionnaire until the measurement architecture is judged defensible.

## Phase 0B — Freeze decision use cases

After Gate 0A, define 4–6 decision processes `i`.

Selection criteria:

1. strategically or operationally meaningful;
2. repeated or consequential enough to justify optimization;
3. clear owner and user;
4. clear inputs/outputs;
5. observable workflow and approval structure;
6. plausible AI involvement;
7. collectively cover different decision families.

Target coverage should include at least:

- prediction / diagnosis;
- recommendation / selection;
- allocation / planning;
- execution / coordination;
- a case with meaningful human-accountability or assurance requirements.

**Go/No-Go Gate 0B:** no questionnaire is finalized until the use-case list is frozen.

## Phase 1 — Public-data calibration table

Build a reproducible public-data table with two blocks.

### 1A. JPC public firm context

Preferred window: current multi-year period sufficient for normalization and scenario design.

Minimum fields:

- revenue;
- gross and operating margin;
- operating cash flow;
- cash / liquidity;
- R&D expense;
- CapEx;
- liabilities / leverage;
- relevant segment / product / public market exposure where disclosed.

These fields inform affordability and value context; they do **not** measure AI maturity.

### 1B. Industry context

Collect public evidence for:

- `ID_t` demand;
- `TP_t` technology transition;
- `CP_t` cost pressure;
- `SC_t` supply constraint;
- `SP_t` standards / policy / qualification pressure.

**Go/No-Go Gate 1:** every public-data variable must have provenance, date, unit and explicit model use. If its model use is unclear, keep it as context only.

## Phase 2 — Measurement anchors and pilot

Freeze the 0–3 anchor dictionaries for D/R/A/G/H/WI/EA and Low/Medium/High for `kappa`.

Pilot with:

- 1 IT/MIS respondent;
- 1 functional/process respondent;
- 1 frontline respondent.

Pilot objectives:

- identify ambiguous wording;
- verify respondents distinguish current state from desired state;
- verify thresholds can be answered as minimum requirements;
- estimate interview duration;
- detect parameters that respondents cannot reasonably judge.

**Go/No-Go Gate 2:** do not launch full elicitation until at least 80% of pilot questions can be answered without interviewer reinterpretation.

## Phase 3 — JPC internal calibration

### Target 14 respondents

Strategic:
- Chairman
- General Manager
- COO
- Finance leader

Technical / functional:
- IT/MIS leader
- IT/MIS engineer A
- IT/MIS engineer B
- RDPM
- Senior mechanical engineer
- Procurement / SCM
- QA leader or Plant Manager

Frontline:
- Accounting/finance operator
- Sales or sales-assistant user
- Production/planning/floor user

Optional:
- Spokesperson / IR-facing representative

### Expected interview burden

- Chairman / GM / COO: about 14 questions, 20–30 min.
- Finance: about 12 questions, 20 min.
- IT/MIS: about 16 questions, 25–35 min.
- Functional experts: about 14 questions, 20–30 min.
- Frontline: about 12 questions, 10–15 min.

No participant should be asked to answer parameters outside their role expertise merely to fill missing cells.

## Phase 4 — External challenge

### Fullon senior R&D / Marketing / Sales executive

Challenge:

- technology / market assumptions;
- risk classes;
- human oversight boundaries;
- workflow integration;
- assurance;
- Human–AI configuration value.

### Mega VC evaluator

Challenge:

- value-at-stake logic;
- affordability/resource-allocation logic;
- growth-risk trade-off;
- whether public-data-based `B^tot` and `v_i` scenarios are economically plausible.

External experts do not supply JPC-specific facts and are never asked for confidential company or investment records.

## Phase 5 — Parameter registry

Create one canonical parameter registry with fields:

`Parameter_ID`
`Symbol`
`Use_Case`
`Scenario`
`Value_or_Range`
`Scale`
`Provenance_Type`
`Primary_Source`
`Secondary_Source`
`Respondent_Role`
`Question_ID`
`Date`
`Uncertainty`
`Aggregation_Rule`
`Transform_Rule`
`Equation`
`Validation_Status`
`Notes`

Mandatory provenance values:

- PUBLIC_OBSERVED
- CONSENTED_OBSERVED
- EXPERT_ELICITED
- INFERRED_FROM_PUBLIC
- INTERVAL_OR_FUZZY
- SCENARIO_SENSITIVITY
- SIMULATED_ONLY

## Phase 6 — Calibration rules

### Rule 1 — never overwrite decision variables
Observed `A_obs/H_obs/WI_obs/EA_obs/q_obs` are baseline/validation evidence. The solver still chooses `A/H/WI/EA/q`.

### Rule 2 — preserve ordinality
A 0–3 state is not assumed to be equally spaced. Use separate monotone cardinalization only where the objective needs magnitude effects.

### Rule 3 — use role authority, not rank alone
Parameter aggregation uses relevance weights or scenario ranges. Chairman is not automatically authoritative for technical data quality; IT is not automatically authoritative for strategic value.

### Rule 4 — disagreement is information
If competent respondents disagree materially, retain Low/Base/High or fuzzy intervals instead of forcing an average.

### Rule 5 — public finance is context, not maturity
No financial statement line directly sets D/R/A/G/H/WI/EA.

### Rule 6 — external industry context is exogenous
Industry demand/technology/cost/supply/policy may shift calibrated parameters or scenarios, but does not directly set internal capability.

## Phase 7 — First non-simulated solve

Run at least three parameter regimes:

- Conservative / Low-capacity
- Base
- Expansion / High-opportunity

For each regime:

1. validate feasibility-preservation conditions;
2. solve Level 3 → Level 2 → Level 1 using frozen tie-breaking;
3. record optimal `b*`, `A*/H*/WI*/EA*`, `q*`;
4. compare against observed current state;
5. compute which constraints bind;
6. record why each recommendation changed across scenarios.

Do not interpret scenario differences as causal predictions.

## Phase 8 — Robustness analysis

At minimum stress-test:

- F1/F2/U weights;
- `B^tot`;
- `K_Gamma`;
- `phi_X`;
- requirement thresholds;
- `g_im`;
- `beta_m`;
- governance multipliers;
- industry scenarios.

Classify each recommended decision as:

- ROBUST — unchanged across plausible ranges;
- CONDITIONALLY ROBUST — changes only under identifiable parameter regimes;
- FRAGILE — small plausible perturbations change the recommendation.

The paper should emphasize robust/conditional findings and avoid strong claims from fragile optima.

## Phase 9 — Model feasibility review after data collection

The model remains acceptable if:

- every optimized use case has a feasible HumanOnly/null fallback;
- no threshold leaves the entire feasible set empty without explicit theoretical reason;
- all non-public numbers have consent/provenance;
- all C5 parameters are bounded/scenario-tested rather than falsely point-estimated;
- external validation challenges, rather than duplicates, internal calibration;
- solver results are reproducible from the parameter registry.

If these conditions hold, the study can advance from **Mathematical Feasibility** to **Empirically Calibrated Scenario Optimization**.

## Short request to the Chairman for respondent coordination

> This research does not require confidential company records or exact internal budgets. The mathematical model is already built; the next step is to calibrate a small set of decision, process, risk and resource parameters using role-specific expert judgment. I would like to invite approximately 14 internal participants covering senior management, IT/MIS, RD/PM, procurement, finance, manufacturing/quality and a few frontline workflow users. Each person receives only the questions relevant to their role, typically 10–16 questions and around 10–30 minutes. The purpose is to compare strategic requirements, technical feasibility and actual workflow, not to evaluate individual performance.
