# AI × Decision × MLP — Variable & Measurement Master v1.1

Base mathematical freeze: `main@1f2e72f1894c8d4eb7929c39756d7b6af607545b`.

This file does **not** modify the v1.0 mathematical skeleton. It defines the empirical calibration layer needed to move from simulated feasibility inputs to public-data / consented-elicitation parameters.

## 1. Governing separation

The empirical design must keep five object types separate:

1. **Endogenous decision variables** — chosen by the optimizer; never directly replaced by survey scores.
2. **Observed states / context** — measured from public data or consented respondents before optimization.
3. **Calibrated parameters** — estimated, elicited, bounded or scenario-defined before optimization.
4. **Derived quantities** — deterministically computed once decisions and parameters are supplied.
5. **Evidence descriptors** — literature-network evidence such as O/E and BH q-values; they motivate representation but are never optimization coefficients.

Observed values must use an `obs` suffix when stored, e.g. `H_obs`, while optimized values remain `H*` or `H` in the solver.

## 2. Unit of analysis

The index `i` must refer to a clearly defined **decision process / use case**, not a department, employee or entire company. A valid use case must have:

- identifiable decision owner;
- recurring or meaningful decision event;
- defined inputs and outputs;
- observable workflow handoffs;
- defined failure consequence;
- plausible Human–AI configurations.

Before empirical collection, freeze a small set of approximately 4–6 use cases that jointly cover prediction, recommendation/selection, allocation/planning and execution-oriented decisions.

## 3. Core 0–3 construct anchors

The optimizer may retain 0–3 discrete states, but empirical measurement must treat them as **ordinal** unless a separate monotone cardinalization map is justified.

| Construct | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| `D` Digital / Process Infrastructure Readiness | mainly manual / fragmented | digital tools exist but siloed | integrated workflows and stable structured exchange | interoperable end-to-end digital workflow with reliable automation hooks |
| `R` Data Readiness | unavailable / unreliable | partial, inconsistent or weakly governed | sufficient structured data with ownership and basic quality control | validated, governed, timely, traceable and sustainable for AI use |
| `A` AI Decision Integration Depth | no AI decision support | AI information / assistance | AI recommendation or checking integrated into decision flow | bounded AI execution / automation |
| `G` Governance Capability | no formal governance | basic rules / named responsibility | formal policy, ownership and monitoring | audit, escalation, control and lifecycle governance |
| `H` Human Oversight | no systematic oversight | optional / light review | mandatory review / override / accountable owner | continuous oversight, escalation and traceability |
| `WI` Workflow Integration | AI outside workflow | manual transfer of outputs | system triggers / handoffs / exception routing integrated | bounded end-to-end action with fallback / exception handling |
| `EA` Evaluation & Assurance | no formal evaluation | ad hoc testing | predefined metrics, validation and monitoring | continuous assurance, audit, drift / rollback / traceability |

If cardinal effects are required, use a monotone transform `z_X(l)` for `l ∈ {0,1,2,3}` rather than silently assuming equal spacing. The default empirical rule is: **state level is ordinal; effect size is separately calibrated**.

## 4. Variable and parameter master

| Symbol / object | Type | Operational meaning | Scale | Directly computable now? | Primary source | Calibration / measurement | Model role |
|---|---|---|---|---|---|---|---|
| `D_i^0` | observed baseline | digital/process infrastructure readiness before new investment | ordinal 0–3 | no | IT/MIS + public evidence | anchored expert coding, preferably ≥2 raters | L1 capability baseline |
| `R_i^0` | observed baseline | data readiness for use case `i` | ordinal 0–3 | no | IT/MIS | anchored expert coding | L1 capability baseline |
| `A_i^0` | observed baseline | current AI decision-integration depth | ordinal 0–3 | partial | IT/MIS + process owner | coding of current state, not optimized target | L1 capability baseline |
| `G_i^0` | observed baseline | current governance capability | ordinal 0–3 | no | IT/MIS + QA/governance/plant manager | anchored coding | L1 capability baseline |
| `b_i^D,b_i^A,b_i^R,b_i^G` | **L1 decision** | resource allocation to capability categories | discrete 0–3 | chosen by solver | none | never elicited as final values | L1 decision |
| `c_i^r` | calibrated parameter | normalized or monetary cost of one resource step | ratio / normalized / interval | no | public cost evidence + finance + IT | point only if supported; otherwise interval / fuzzy / scenario | L1 budget constraint |
| `B^tot` | calibrated constraint | total affordable transformation resource envelope | ratio / normalized / scenario | no exact point | public financials + finance + executive | Low/Base/High envelope preferred to confidential exact budget | L1 budget constraint |
| `phi_i^X` | calibrated transition function | how investment changes capability ceiling | monotone function | no | IT/MIS / transformation expert | monotone transition table or bounded scenario; do not claim causal estimation from cross-section | L1→L2 bridge |
| `Dbar,Abar,Rbar,Gbar` | derived | post-investment capability ceilings | 0–3 | yes after `phi,b` | formula | deterministic | L2 feasibility bounds |
| `A_i` | **L2 decision** | target AI decision integration depth | discrete 0–3 | chosen by solver | none | distinguish from `A_obs` | L2 decision |
| `H_i` | **L2 decision** | target human oversight intensity | discrete 0–3 | chosen by solver | none | distinguish from `H_obs` | L2 decision |
| `WI_i` | **L2 decision** | target workflow integration intensity | discrete 0–3 | chosen by solver | none | distinguish from `WI_obs` | L2 decision |
| `EA_i` | **L2 decision** | target evaluation/assurance intensity | discrete 0–3 | chosen by solver | none | distinguish from `EA_obs` | L2 decision |
| `u_i` | observed context | use type such as prediction / recommendation / execution-oriented use | nominal | yes after coding | process owner / RDPM / procurement / operations | structured case coding | threshold context |
| `t_i` | observed context | decision task type such as prediction / selection / allocation / execution | nominal | yes after coding | process owner | structured case coding | threshold context |
| `exec_i` | observed context | whether use case includes execution/action authority | binary | yes after coding | process owner + IT | case coding | `WI_req` context |
| `kappa_i` | calibrated / observed context | consequence class if the decision is wrong | ordinal low/medium/high | not from financials alone | process owner + QA/plant manager + executives | anchored risk-class coding; cardinal effect handled separately | requirements and risk |
| `D_req(A)` | calibrated threshold | minimum digital capability for AI depth `A` | ordinal threshold | no | IT/MIS | threshold elicitation by AI depth | L2 feasibility |
| `R_req(A)` | calibrated threshold | minimum data readiness for AI depth `A` | ordinal threshold | no | IT/MIS | threshold elicitation by AI depth | L2 feasibility |
| `H_req(A,kappa,u)` | calibrated threshold | minimum human oversight | ordinal threshold | no | QA/plant manager + process expert + executives | scenario-based threshold elicitation | L2 feasibility |
| `EA_req(A,kappa,t)` | calibrated threshold | minimum evaluation/assurance | ordinal threshold | no | QA/plant manager + process expert + IT | scenario-based threshold elicitation | L2 feasibility |
| `WI_req(A,kappa,exec)` | calibrated threshold | minimum workflow integration | ordinal threshold | no | COO + IT + process owner | scenario-based threshold elicitation | L2 feasibility |
| `K_Gamma` | calibrated constraint | simultaneous organizational transformation / governance absorption capacity | relative / normalized / scenario | no | COO + IT + executives | scenario envelope rather than pretending exact physical units | shared L2 capacity |
| `CapUse_i` | derived | use-case consumption of transformation capacity | normalized index | yes after weights | formula | current coefficients are simulated until calibrated | shared L2 capacity |
| `Feas_i` | derived | model-defined feasibility score | 0–1 | yes after calibration | formula | coefficients require empirical or sensitivity treatment | F2 component |
| `Rel_i` | derived | model-defined reliability score | 0–1 | yes after calibration | formula | coefficients require calibration / robustness | F2 component |
| `Scalability_i` | derived | model-defined scalability score | 0–1 | yes after calibration | formula | coefficients require calibration / robustness | F2 component |
| `IntegrationCost_i` | derived | integration burden/cost index | normalized | yes after calibration | formula | depends on `cost_Gamma` and component weights | F2 component |
| `GovRisk_i` | derived | governance risk index | normalized | yes after calibration | formula | depends on `risk_Gamma`, `kappa`, H/EA | F2 component |
| `Gamma` | scenario / policy state | governance architecture/environment | categorical | codable | executives + IT/governance | explicitly defined scenario classes | L2/L3 context |
| `Allow_mGamma` | calibrated policy constraint | whether configuration `m` is permitted under governance scenario | binary | partial | governance/QA/IT + executives | policy matrix; disagreement retained for sensitivity | L3 feasibility |
| `q_im` | **L3 decision** | selected Human–AI configuration | binary one-hot | chosen by solver | none | observed configuration kept separately as `q_obs` | L3 decision |
| `y_i` | derived | whether AI is adopted | binary | yes | formula | `1-q_HumanOnly` | L1 objective component |
| `g_im` | calibrated parameter | relative benefit multiplier of configuration `m` for use case `i` | relative / interval | no | process experts + external domain expert | pairwise / anchored relative judgment; avoid false precision | L3 gain |
| `v_i` | calibrated parameter | value-at-stake of use case `i` | normalized / interval | partial | public firm/industry data + executives + spokesperson + external validator | combine public exposure with elicited strategic importance | L3 gain / L1 realized value |
| `beta_m` | calibrated parameter | baseline burden of Human–AI configuration | normalized / interval | no | frontline users + process experts | workflow-time / burden anchors or fuzzy interval | L3 burden |
| `autonomy_m` | calibrated parameter | relative autonomy/risk potential of configuration | ordered / 0–1 | partial | AI/IT + governance expert | anchored configuration coding | residual risk |
| `flex_Gamma` | calibrated scenario factor | governance scenario effect on flexibility/value realization | interval / scenario | no | executives + IT | scenario/sensitivity | gain |
| `cost_Gamma` | calibrated scenario factor | governance scenario effect on integration cost | interval / scenario | no | finance + IT/COO | scenario/sensitivity | integration cost |
| `risk_Gamma` | calibrated scenario factor | governance scenario effect on residual risk | interval / scenario | no | QA/governance + executives | scenario/sensitivity | risk |
| `s_i` | optional observed input | AI model score | 0–1 | only if a real benchmark/model exists | benchmark/model output | otherwise keep as sensitivity toy | G10 sensitivity |
| `tau_i` | policy parameter | decision threshold applied to score | 0–1 | not inherently | policy / expert / sensitivity | policy choice or threshold analysis | G10 sensitivity |
| `truth_i` | optional observed outcome | labeled true outcome | binary / task-specific | only if labeled data exists | benchmark / public dataset / consented outcome | otherwise do not make empirical accuracy claims | G10 sensitivity |
| `psi_i` | derived | realized value multiplier | nonnegative | yes after inputs | formula | deterministic | L3 gain |
| `Gain_im` | derived | realized benefit component | continuous | yes after calibration | formula | deterministic | L3 utility |
| `Burden_im` | derived | workload / operating burden component | continuous | yes after calibration | formula | deterministic | L3 utility |
| `ResidualRisk_im` | derived | residual risk component | continuous | yes after calibration | formula | deterministic | L3 utility |
| `U_im` | derived objective | L3 utility | continuous | yes after calibration | formula | objective weights require elicitation / robustness | L3 objective |
| `F2` | derived objective | architecture-level objective | continuous | yes after calibration | formula | weights calibrated via structured elicitation | L2 objective |
| `F1` | derived objective | enterprise resource-allocation objective | continuous | yes after calibration | formula | weights calibrated via executive/financial elicitation | L1 objective |
| `O/E`, `q_BH`, four-analysis depletion flags | evidence only | literature-network structural evidence | ratio / probability-adjusted evidence | yes | frozen literature evidence | never converted into optimization weights | evidence justification only |

## 5. External context calibration layer

Industry and financial variables are **exogenous calibration inputs**, not maturity scores and not optimizer decisions.

Define an industry-context vector:

`Z_t = (ID_t, TP_t, CP_t, SC_t, SP_t)`

where:

- `ID_t` = industry demand;
- `TP_t` = technology-transition pressure;
- `CP_t` = cost pressure;
- `SC_t` = supply constraint;
- `SP_t` = standards / policy / qualification pressure.

Define a public firm-financial vector:

`F_t = (Revenue, Margin, OCF, Cash, R&D, CapEx, Leverage, SegmentExposure, ...)`.

The empirical calibration function is conceptually:

`theta_t = Theta(Z_t, F_t, E_internal, E_external)`

where `theta_t` supplies calibrated / bounded parameters to the frozen MLP. Do not add an unnecessary Level 0 unless later theory requires endogenous industry behavior.

## 6. Measurement rules that cannot be violated

1. `D/R/A/G/H/WI/EA` 0–3 levels are ordinal unless separately cardinalized.
2. Survey observations are `*_obs`; optimized decisions are `*` or `*` with a star. Never overwrite one with the other.
3. Public financial data may calibrate affordability, value exposure and scenarios, but cannot directly identify AI maturity.
4. Industry growth cannot be used as evidence that firm AI capability is high.
5. O/E and depletion q-values remain literature evidence and never become utility / objective weights.
6. `B^tot` is not equal to cash, R&D expense or any single line item.
7. `phi_X`, `g_im`, `beta_m`, governance multipliers and objective coefficients must remain interval/fuzzy/scenario values until identified by evidence.
8. Lack of identification is handled by robustness analysis, not invented precision.

## 7. Empirical status coding

Every parameter record must carry one provenance type:

- `PUBLIC_OBSERVED`
- `CONSENTED_OBSERVED`
- `EXPERT_ELICITED`
- `INFERRED_FROM_PUBLIC`
- `INTERVAL_OR_FUZZY`
- `SCENARIO_SENSITIVITY`
- `SIMULATED_ONLY`

Every value must also record source, date, uncertainty/range and the exact model equation it enters.
