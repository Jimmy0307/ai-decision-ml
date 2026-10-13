# 62 data dictionary (generated from 65 TABLES; single source of truth)

Common value columns for every parameter row: `value`, `unit`, `provenance_type`, `source_id`, `period`, `uncertainty`, `lower`, `upper`, `identification_status`, `assumption_note`

- provenance_type: OBSERVED, EXPERT_ELICITED_INTERNAL, EXPERT_ELICITED_EXTERNAL, PUBLIC_OBSERVED_BOUND, SCENARIO_SENSITIVITY, DEFINITIONAL, UNIDENTIFIED
- uncertainty: POINT, INTERVAL, NONE
- identification_status: IDENTIFIED_POINT, IDENTIFIED_INTERVAL, BOUND_ONLY, SCENARIO_ONLY, UNIDENTIFIED
- UNIDENTIFIED rows keep value/lower/upper blank. A blank is never read as zero.

## S_sources (Block S)

Every source_id used anywhere must be registered here. source_scope=external sources can only support EXPERT_ELICITED_EXTERNAL or PUBLIC_OBSERVED_BOUND cells; external roles are never optimizers.

Columns: source_id, source_scope, source_kind, external_role, description, date, custodian_role, access_restriction

## E_enterprise (Block E)

Pooled budget and engineering capacity; unit review capacity rev_cap and status-quo envelopes B0 (unit_id); time values lam (enterprise), lam_u (unit ledger), lam_U (upper bound) by role.

Index columns: parameter, unit_id, role

| parameter | unit | kind |
|---|---|---|
| A_bar_BUD | TWD/period | num |
| A_bar_ENG | hours/period | num |
| rev_cap | hours/period | num |
| B0_BUD | TWD/period | num |
| B0_ENG | hours/period | num |
| lam | TWD/hour | num |
| lam_u | TWD/hour | num |
| lam_U | TWD/hour | num |

## E_capabilities (Block E)

scope=SHARED (enterprise, unit_id blank) or LOCAL (unit-built alternative, unit_id required). y_cur only for SHARED: 1 if already in operation.

Index columns: capability_id, scope, unit_id, parameter

| parameter | unit | kind |
|---|---|---|
| F | TWD/period | num |
| eng | hours/period | num |
| y_cur | binary | bin |

## G_policy (Block G)

policy_role in CURRENT / LEGAL_MINIMUM / ALTERNATIVE. allow per (initiative, config); allow_loc per (unit, capability); G, ebar, must, forbid per initiative.

Index columns: policy_id, policy_role, parameter, initiative_id, config_id, unit_id, capability_id

| parameter | unit | kind |
|---|---|---|
| gov_cost | TWD/period | num |
| allow | binary | bin |
| allow_loc | binary | bin |
| G | ordinal_level | ord |
| ebar | incidents/period | num |
| must | binary | bin |
| forbid | binary | bin |

## G_requirements (Block G)

Requirement tables keyed by (A level, kappa level), levels 0-3. R_req/D_req are enterprise-wide: policy_id='*', kappa_level blank.

Index columns: policy_id, parameter, A_level, kappa_level

| parameter | unit | kind |
|---|---|---|
| H_req | ordinal_level | ord |
| WI_req | ordinal_level | ord |
| EA_req | ordinal_level | ord |
| G_req | ordinal_level | ord |
| R_req | ordinal_level | ord |
| D_req | ordinal_level | ord |

## X_initiatives (Block X)

Owner unit, consequence class kappa, the capabilities whose state indexes the initiative's lookups (semicolon list; NONE = empty list), chargeback tau per capability (DEFINITIONAL 0 only if the rule says none).

Index columns: initiative_id, unit_id, parameter, capability_id

| parameter | unit | kind |
|---|---|---|
| kappa | ordinal_level | ord |
| relevant_capabilities | list | list |
| tau | TWD/period | num |

## X_configurations (Block X)

One status-quo configuration per initiative (is_status_quo=1). EAX is recorded as a rho grouping key only (conditional candidate; never a requirement).

Index columns: initiative_id, config_id, parameter

| parameter | unit | kind |
|---|---|---|
| is_status_quo | binary | bin |
| A | ordinal_level | ord |
| H | ordinal_level | ord |
| WI | ordinal_level | ord |
| EA | ordinal_level | ord |
| EAX | ordinal_level | ord |
| m | nominal | nominal |
| prerequisites | list | list |
| legal | binary | bin |
| eff_H | binary | bin |
| fallback | binary | bin |
| cons | binary | bin |
| allowed_responses | list | list |
| impl_x | TWD/period | num |

## X_config_costs (Block X)

Implementation cost and engineering hours by capability-source state, e.g. 'CAP1:S' (shared), 'CAP1:L' (local), 'NONE'; '*' = invariant across states (assumption_note required).

Index columns: initiative_id, config_id, capability_state, parameter

| parameter | unit | kind |
|---|---|---|
| impl | TWD/period | num |
| eng | hours/period | num |

## X_capability_state (Block X)

Data availability R_j(s) and interface level D_j(s) per capability-source state (F5e).

Index columns: initiative_id, capability_state, parameter

| parameter | unit | kind |
|---|---|---|
| R_level | ordinal_level | ord |
| D_level | ordinal_level | ord |

## R_roles (Block R)

Exposure weight of each role group; rows of one (initiative, config) sum to 1.

Index columns: initiative_id, config_id, role, parameter

| parameter | unit | kind |
|---|---|---|
| pi | probability | prob |

## R_signal_outcome (Block R)

Joint probability of visible signal z and hidden outcome omega; rows sum to 1; z and omega labels disjoint.

Index columns: initiative_id, config_id, signal, outcome, parameter

| parameter | unit | kind |
|---|---|---|
| P | probability | prob |

## R_responses (Block R)

rho(r | k, z, role[, capability state]); rho_kind in design / observed / counterfactual. Never conditioned on the hidden outcome. capability_state blank = all states.

Index columns: initiative_id, config_id, signal, role, capability_state, rho_kind, response, parameter

| parameter | unit | kind |
|---|---|---|
| rho | probability | prob |

## V_volume (Block V)

Events per period by configuration.

Index columns: initiative_id, config_id, parameter

| parameter | unit | kind |
|---|---|---|
| N | events/period | num |

## V_outcomes (Block V)

Per-event path values: v_u/v_x value (unit ledger / outside it), l_u/l_x loss, c_u/c_x operating cost, t role time, t_rev review time, I_sev severe-incident probability. '*' = invariant (note required).

Index columns: initiative_id, config_id, role, signal, outcome, response, parameter

| parameter | unit | kind |
|---|---|---|
| v_u | TWD/event | num |
| v_x | TWD/event | num |
| l_u | TWD/event | num |
| l_x | TWD/event | num |
| c_u | TWD/event | num |
| c_x | TWD/event | num |
| t | hours/event | num |
| t_rev | hours/event | num |
| I_sev | probability | prob |

## U_registry (Block U)

Scenario groups registered BEFORE any result is seen. grouping_rule documents how interval cells are grouped into blocks (default: one block per elicited interval row).

Columns: group_id, meaning, eps_R, tie_tol, registered_before_results, registration_date, grouping_rule, notes
