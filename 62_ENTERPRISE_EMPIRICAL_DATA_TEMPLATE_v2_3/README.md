# 62 — Enterprise Empirical Data Template v2.3

Contract: `43_PARAMETER_IDENTIFICATION_AND_QUANTIFICATION_v2_1.md` (only). Model: `42` v2.2. Loader / validator / runner: `65_enterprise_data_loader_v2_3.py`.
The CSV headers, the `.xlsx` sheets and `DATA_DICTIONARY.md` are all generated from one schema (`65 TABLES`); regenerate with
`python 65_enterprise_data_loader_v2_3.py --make-template <dir>`.

| File / sheet | 43 block | Contents |
|---|---|---|
| `S_sources` | — | Source registry: `source_scope` internal/external, `source_kind`, `external_role` (board-related / partner-supplier / investor / other). External sources never become optimizers |
| `E_enterprise` | E | `A_bar_BUD`, `A_bar_ENG`, `rev_cap`(unit), `B0_BUD`/`B0_ENG`(unit), `lam`/`lam_u`/`lam_U`(role) |
| `E_capabilities` | E | Shared capabilities (`F`, `eng`, `y_cur`) and local-build alternatives (`scope=LOCAL`, `unit_id`) |
| `G_policy` | G | Per policy (`CURRENT`/`LEGAL_MINIMUM`/`ALTERNATIVE`): `gov_cost`, `allow`, `allow_loc`, `G`, `ebar`, `must`, `forbid` |
| `G_requirements` | G | `H_req`, `WI_req`, `EA_req`, `G_req` by (A level, kappa level); `R_req`, `D_req` by A level (policy `*`) |
| `X_initiatives` | X | Owner unit, `kappa`, `relevant_capabilities`, chargeback `tau` |
| `X_configurations` | X | Status-quo flag; `A`, `H`, `WI`, `EA`, `EAX`, `m`; prerequisites; `legal`, `eff_H`, `fallback`, `cons`; allowed responses; central funding `impl_x` |
| `X_config_costs` | X | `impl`, `eng` by capability-source state (`NONE`, `CAP:S`, `CAP:L`) |
| `X_capability_state` | X | `R_level`, `D_level` by capability-source state (F5e) |
| `R_roles`, `R_signal_outcome`, `R_responses` | R | `pi`, `P(z, ω)`, and `rho(r | z, role[, state])` by kind design / observed / counterfactual |
| `V_volume`, `V_outcomes` | V | `N`; per-event `v_u, v_x, l_u, l_x, c_u, c_x, t, t_rev, I_sev` (enterprise vs unit ledger split = the `_u` / `_x` pairs) |
| `U_registry` | U | Scenario groups and grouping rule, registered before results |

Every parameter row carries the value columns `value, unit, provenance_type, source_id, period, uncertainty, lower, upper, identification_status, assumption_note`. The validator (`65 --validate`) enforces the following rules.

- **Missing data.** A missing cell is `UNIDENTIFIED`, with value, lower and upper left blank. A typed 0 is never read as missing, and a blank is never read as 0.
- **Provenance:**
  - Expert values are intervals unless a point value is justified in `assumption_note`.
  - Public bounds and scenarios are never point values. Public effect-size bounds on `t` or `v` need a "task similarity" note.
  - External sources can only give `EXPERT_ELICITED_EXTERNAL` or `PUBLIC_OBSERVED_BOUND`.
- **Units, period and bounds.** Units must match the dictionary exactly. Every per-period and per-event cell needs a period, and all cells must use one period definition.
- **Ordinal and categorical values.** Ordinals are anchor levels 0–3, never cardinal scores. Ordinal, binary and list parameters take a point value or `UNIDENTIFIED`.
- **Wildcards.** A `*` in role, signal, outcome, response or capability state is an invariance claim and must be stated in `assumption_note`.

The minimum pilot skeleton (`63_MINIMUM_PILOT_SKELETON_v2_3/`) uses the same schema with every required row pre-listed as `UNIDENTIFIED`.
