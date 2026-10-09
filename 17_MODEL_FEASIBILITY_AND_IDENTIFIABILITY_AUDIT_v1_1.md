# AI × Decision × MLP — Empirical Feasibility & Identifiability Audit v1.1

Base mathematical freeze: `main@1f2e72f1894c8d4eb7929c39756d7b6af607545b`.

## Executive verdict

**PASS WITH EMPIRICAL CONDITIONS**

The v1.0 finite tri-level mathematical skeleton remains computationally and logically feasible. The empirical extension is also feasible **if the study is positioned as a calibrated decision-support / scenario-optimization model rather than a causal estimator of true firm behavior**.

No structural equation in v1.0 must be changed to begin empirical calibration. The main work is to replace simulated constants with public-data-supported, consented, elicited, interval/fuzzy or sensitivity values while preserving provenance.

The model is **not yet point-identified** for every coefficient. That is acceptable if non-identifiable quantities are treated honestly as intervals, fuzzy values or scenarios and are stress-tested.

## 1. Why the mathematical model remains feasible

The current skeleton has:

- finite discrete Level-1 allocations;
- finite discrete Level-2 architecture states;
- finite Level-3 Human–AI configurations;
- explicit feasibility constraints;
- deterministic tie-breaking;
- previously verified finite enumeration and returned-solution constraints.

The empirical calibration layer changes parameter values and evidence provenance. It does not require changing the existence proof, provided calibrated thresholds and policy matrices retain at least one feasible null architecture, e.g. HumanOnly / zero-AI adoption when necessary.

### Empirical safety condition E0

Every calibrated scenario must satisfy a feasibility-preservation check before optimization:

1. `B^tot >= 0`;
2. `K_Gamma >= 0`;
3. HumanOnly is allowed in at least one governance state used for a scenario;
4. zero-AI architecture remains feasible unless the study explicitly models mandatory adoption;
5. calibrated requirement thresholds remain within the state domain `{0,1,2,3}`;
6. any cardinalized maps are finite and monotone where required.

If E0 fails, the issue is with the empirical parameterization, not with the frozen mathematical skeleton.

## 2. Identifiability classes

### C1 — directly computable / observed
Can be obtained with little modeling ambiguity.

Examples:

- literature O/E and q-values;
- public financial line items;
- public industry series;
- nominal use-case type after coding;
- `exec_i` after process definition;
- derived quantities once inputs are fixed.

### C2 — directly codable with an anchored rubric
Requires human coding, but construct definition can be explicit.

Examples:

- `D_i^0`, `R_i^0`, `A_i^0`, `G_i^0`;
- observed `H_obs`, `WI_obs`, `EA_obs`;
- `kappa_i` as an ordinal consequence class.

Use multiple raters where possible and report agreement/disagreement.

### C3 — threshold-elicitable
Cannot be read directly from public data but can be elicited using structured scenarios.

Examples:

- `D_req(A)`;
- `R_req(A)`;
- `H_req(A,kappa,u)`;
- `EA_req(A,kappa,t)`;
- `WI_req(A,kappa,exec)`;
- `Allow_mGamma`.

These are among the strongest candidates for expert elicitation because the question is naturally expressed as a minimum acceptable requirement.

### C4 — preference / resource parameters
Require decision-maker preference or financial interpretation.

Examples:

- `B^tot` scenarios;
- `K_Gamma` scenarios;
- F1/F2/U criterion weights;
- `cost_Gamma`, `risk_Gamma`, `flex_Gamma`;
- policy threshold `tau_i` if not externally fixed.

Use BWM/fuzzy-BWM, scenario ranges or explicit policy choices rather than arbitrary coefficients.

### C5 — not point-identifiable from the planned cross-sectional evidence
These must not be falsely presented as statistically estimated constants.

Examples:

- exact causal capability transition function `phi_X`;
- exact `g_im` productivity multipliers;
- exact `beta_m` burden constants;
- exact marginal effect of each 0–3 maturity step;
- true causal effect of industry pressure on firm outcome;
- true error-rate/payoff function for G10 without a labeled benchmark.

Use monotone transition tables, intervals, triangular fuzzy numbers, scenario grids, observed proxies and robustness analysis.

## 3. Parameter-block feasibility

| Block | Main parameters | Identifiability | Feasibility judgment | Required treatment |
|---|---|---|---|---|
| Literature evidence | O/E, four q-values | C1 | PASS | frozen evidence only |
| Industry context | `ID,TP,CP,SC,SP` | C1/C2 | PASS | public-data indices / scenario coding |
| Firm financial context | revenue, margin, OCF, cash, R&D, CapEx, leverage | C1 | PASS | public filings only |
| Baseline capability | `D0,R0,A0,G0` | C2 | PASS | anchored IT/process coding |
| L1 budget | `B^tot` | C4 | PASS as scenario | Low/Base/High affordability envelope; do not equate to cash/R&D |
| Capability cost | `c_i^r` | C4/C5 | PASS with ranges | public cost evidence + expert interval |
| Capability transition | `phi_X` | C5 | PASS with structural restraint | monotone transition table / scenario, not causal point estimate |
| Context coding | `u,t,exec,kappa` | C2 | PASS | process-owner coding + risk anchors |
| Requirement thresholds | `D_req,R_req,H_req,EA_req,WI_req` | C3 | STRONG PASS | structured expert threshold elicitation |
| Shared capacity | `K_Gamma` | C4 | PASS as scenario | COO/IT/executive envelope |
| Governance permissions | `Allow_mGamma` | C3/C4 | PASS | role-authoritative policy matrix |
| Use-case value | `v_i` | C1/C4 | PASS | public value exposure + executive/market elicitation |
| Configuration gain | `g_im` | C5 | PASS with relative scale | relative/pairwise/fuzzy judgments; external validation |
| Configuration burden | `beta_m` | C2/C5 | PASS with observational proxy | frontline workflow burden + interval |
| Autonomy | `autonomy_m` | C2/C4 | PASS | anchored configuration coding |
| Governance multipliers | `flex/cost/risk_Gamma` | C4/C5 | PASS as scenarios | scenario/sensitivity |
| F1 weights | enterprise priorities | C4 | PASS | chairman/GM/finance BWM/fuzzy-BWM |
| F2 weights | architecture priorities | C4 | PASS | COO/IT/QA/process-expert BWM/fuzzy-BWM |
| L3 utility weights | gain/burden/risk trade-off | C4 | PASS | process-owner / frontline / external challenge |
| G10 score/truth | `s,tau,truth` | C1 only with benchmark | CONDITIONAL | empirical only if real labeled data exists; otherwise sensitivity layer |

## 4. Main model risks and how to prevent them

### Risk R1 — treating ordinal levels as cardinal
The values 0,1,2,3 do not prove equal spacing.

**Control:** retain discrete states for feasibility, but estimate any effect through a monotone map `z_X(level)` or scenario table. Do not interpret a move 0→1 as economically equal to 2→3 without evidence.

### Risk R2 — using observed states as optimizer decisions
A survey score of current oversight is not the model's chosen `H`.

**Control:** store `H_obs/WI_obs/EA_obs/A_obs` separately from optimized `H*/WI*/EA*/A*`.

### Risk R3 — executive-only bias
Only senior leaders would describe policy/intention, not actual workflow burden.

**Control:** include IT engineers and frontline accounting, sales/assistant, and production/planning/floor users.

### Risk R4 — frontline-only bias
Frontline users can observe workflow but cannot determine enterprise risk appetite or investment envelope.

**Control:** keep strategic, functional and frontline modules distinct.

### Risk R5 — financial-data overreach
Public financial statements do not identify AI maturity or exact AI budget.

**Control:** use them to calibrate affordability/value context only.

### Risk R6 — industry-data overreach
Industry growth does not prove internal capability.

**Control:** industry variables remain exogenous context/scenario inputs.

### Risk R7 — expert averaging destroys meaning
Averaging a QA assurance judgment with a finance judgment for the same parameter may be meaningless.

**Control:** parameter-specific epistemic authority weights and range preservation.

### Risk R8 — common-source circularity
The same respondent could define a requirement and validate the resulting optimum.

**Control:** separate calibration and challenge roles; use Fullon and Mega VC as external validators for different parameter families.

### Risk R9 — false precision in `phi_X`, `g_im`, `beta_m`
Cross-sectional expert judgment cannot identify true causal coefficients.

**Control:** intervals/fuzzy values + sensitivity/robustness; report as calibrated assumptions, not estimated causal effects.

## 5. Minimum empirical package before the first non-simulated solve

The first empirical/scenario solve should not start until all items below are complete.

### M1 — freeze use cases
Freeze 4–6 decision processes with clear owners, inputs, outputs, workflow and failure consequences.

### M2 — freeze measurement dictionary
Freeze the 0–3 anchors for D/R/A/G/H/WI/EA and the Low/Medium/High risk anchors for `kappa`.

### M3 — build public context table
At minimum:

- JPC public financials: revenue, gross/operating margin, OCF, cash, R&D, CapEx, leverage and relevant segment/public exposure;
- industry: demand, technology transition, cost pressure, supply pressure and standards/qualification context;
- full provenance and date.

### M4 — collect internal calibration
Core panel target: 14 JPC respondents using role-specific modules.

### M5 — external challenge
Fullon senior cross-functional executive + Mega VC evaluator.

### M6 — create parameter registry
Every parameter record must include:

`Parameter_ID | Symbol | Value/Range | Provenance_Type | Source | Respondent_Role | Date | Uncertainty | Transform_Rule | Equation | Notes`

### M7 — feasibility gate
For each Low/Base/High or fuzzy parameter scenario, automatically test E0 before optimization.

### M8 — robustness gate
The result is not considered stable unless key decisions remain interpretable across plausible intervals/scenarios, especially for:

- objective weights;
- `B^tot`;
- `K_Gamma`;
- `phi_X`;
- `g_im`;
- `beta_m`;
- governance multipliers;
- industry scenarios.

## 6. Claim boundary for the eventual paper

### Defensible claim after calibration

> Given a transparent set of public-data-supported, consented-elicited and scenario-bounded parameters, the multi-level model identifies resource, architecture and Human–AI configuration choices that are internally feasible and robust under specified assumptions.

### Not defensible without stronger longitudinal/experimental data

- the model estimates the true causal effect of AI investment;
- the coefficients are statistically identified population parameters;
- an optimized policy will definitely improve future firm performance;
- JPC represents the entire connector / AI-infrastructure industry;
- industry growth causes a specific internal AI maturity level.

## 7. Feasibility verdict

### Mathematical skeleton
`PASS — frozen v1.0 remains feasible.`

### Measurement architecture
`PASS — all major constructs have a definable measurement or elicitation route.`

### Parameter identification
`PASS WITH CONDITIONS — several parameters are interval/scenario identifiable rather than point-identifiable.`

### Public-data-only boundary
`PASS — no privileged internal record is required for the proposed calibration design; consented expert judgments and workflow descriptions are sufficient for the non-public parts.`

### Overall

**The research is feasible as a calibrated, role-structured, public-data-supported MLP decision model. The next blocker is no longer mathematical existence; it is the disciplined execution of use-case selection, measurement anchoring and parameter provenance.**
