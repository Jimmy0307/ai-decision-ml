# 50 — Solver Completion and V3–V6 Validation v2.2

**Label: `SIMULATED_ONLY`.** Every number in this file comes from synthetic instances generated in `51_enterprise_portfolio_solver_v2_2.py`. Nothing here is an enterprise observation, an empirical result, or Chapter 4 evidence.

**Verdicts**

- `V2_2_SYNTHETIC_ENGINEERING_VERDICT: PASS`. All 20 required items pass, as do the extra groups STATE, REG and AUDIT. See `52_SOLVER_ORACLE_RUN_v2_2.txt` (exit code 0).
- `INDEPENDENT_COMPUTATIONAL_REDERIVATION_PASS` (T-ORC-8; §8).
- Scope: this verdict covers synthetic engineering only. **V3 Schema & Units, V4 Lookup Completeness, V5 Portfolio Solver and V6 Invariance & Sensitivity are now complete *at the synthetic level*.** None of them is an enterprise gate pass. V0, V2 and V7 stay OPEN, and V1 is `V1_HUMAN_BLIND_CODING_PENDING` (54C).

**Artifacts**

| Role | File | Notes |
|---|---|---|
| Model spec | `42_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md` | supersedes 42 v2.1 |
| Solver | `51_enterprise_portfolio_solver_v2_2.py` | supersedes 46 as the reference implementation; 46 kept |
| Run log | `52_SOLVER_ORACLE_RUN_v2_2.txt` | SHA-256 of 51 at run time and the reproducibility hash are recorded in its header |
| Test plan | `45_MODEL_VALIDATION_AND_SOLVER_PLAN_v2_2.md` | supersedes 45 v2.1 |

---

## 1. What was built (relative to 46)

| Area | Implementation in 51 | 42 v2.2 |
|---|---|---|
| Typed units | `Q` (dimensions over TWD, hour, event, period, incident; `+`/`−`/`≤` require identical dimensions; `×`/`÷` compose); every numeric input is validated through `Q.of` | §1.1 |
| ω guard | `ρ` keys must be `(z, role)` or `(z, role, capability-state)`; any key containing a hidden outcome ω is rejected, as are signal/outcome label collisions | §6 |
| Finiteness | `Q` rejects NaN, ±inf and non-numeric values; probabilities are checked to lie in [0, 1] and rows to sum to 1 | §1.1 |
| F5e | `R_j(s)`, `D_j(s)` are looked up at the chosen capability-source state for every k (including k = 0). A requirement at the scale minimum needs no lookup. A missing cell is `MissingStateLookup`, which excludes only that `(j, k, s)` | §5 |
| Output contract / state machine | `solve()` never raises for data problems. It returns one of 13 statuses plus the full ordered flag list. Malformed objects, unknown models and invalid DP quanta are reported as `INVALID_SCHEMA_OR_UNITS` | §13.4, §18 |
| Missing `F_c` | `THRESHOLD_MODE`, B and C only (C reports both opt and pess); A, A+ and C0 record F_c as unused unless `c ∈ y^cur` | §13.4 |
| Missing λ | `PARTIAL_OBJECTIVE`. Exact 2^m box-vertex certificate for B/A+; grid only (no point decision) for C/C0; `NO_LEADER_DECISION` for A. `F_E^{−time}` removes all λ terms; `ΔHours` is reported by role; `λ^u` is never overridden | §7.4 |
| DP | Ceil DP (feasible lower bound) and floor DP (relaxation upper bound) give `dp_exact` and `dp_bound`. Falls back to enumeration when ceil is infeasible and floor is not | §12.5 |
| Lemma E′ | Envelopes are each unit's own plan resource vectors; exact for both opt and pess | §12.4 |
| Model D gate | T1–T4 come from documentary evidence and T5 is computed. Any failure gives `MODEL_D_NOT_IDENTIFIED` with zero tri-level calls | §9.2 |
| Robust module | `validate_registry` (single factor kind per block, no overlapping blocks); exact-float `registry_commitment` including nominal values; θ-independent candidate superset; four feasibility classes with witness; Lemma R (scope-guarded: Model B, whole portfolio); MaxRegret / minimax regret; vertex and grid VOI; element-level classification with coverage | §13 |

## 2. Required items — evidence (from 52)

| # | Item | Verdict key | Evidence (synthetic) |
|---|---|---|---|
| 1 | T-SCH-5 | typed units PASS | Unit algebra checks; 4 dimension mismatches rejected; typed φ_E equals float φ_E on 4 (j, k); per-event − per-period is rejected |
| 2 | T-SCH-6 | explicit omega leakage guard PASS | Capability-state ρ key accepted; 4 ω-bearing keys and 1 label collision rejected as `INVALID_SCHEMA_OR_UNITS` |
| 3 | T-SCH-7 | NaN/inf rejection PASS | 57 mutations (NaN, +inf, −inf × 19 numeric classes) plus 1 out-of-range probability, all rejected |
| 4 | T-ALG-1 | F5e PASS | R/D pass and fail cases; a missing or absent R(s) excludes only (j, 1). Status quo at the chosen state: a minimum requirement needs no lookup; otherwise only k = 0 in that state is excluded; the same k = 0 is feasible in one state and not in another. Capability-state ρ rows are used only in their state. Invariant under strictly increasing relabelling |
| 5 | STATE | state-machine/output-contract PASS | All 13 statuses reached and returned as results; garbage objects and an unknown model give INVALID; Model A infeasibility gives INFEASIBLE |
| 6 | T-MIS-3 | missing F_c threshold mode PASS | B: `F_c^† = 82.497`, consistent with 8 explicit solves and no point decision. C: opt/pess thresholds consistent with explicit solves. A+/C0: F_c recorded as unused |
| 7 | T-MIS-4 | missing lambda partial objective PASS | Wide box → FRAGILE with no point decision. Narrow box → ROBUST: certified, checked on a grid, and `F_E^{−time}` equals the λ = 0 objective. Absent key detected; λ^u untouched; no λ^U → UNIDENTIFIED |
| 8 | T-MIS-6 | no silent zero fill PASS | 40 mutations (20 classes × B, C) compared with zero-fill: 12 give no point decision, 16 a different decision or objective, 12 the same decision with the missing input disclosed (the zero-fill run discloses nothing) |
| 9 | T-ORC-9 | DP == exhaustive PASS | 20 integer seeds with budget × 0.3 (binding in 20): B, C-opt, C-pess and forced capability on/off match exactly. 400 random integer MCK instances (mixed-sign weights) match. 400 non-integer instances: OPT ∈ [DP, DP + bound], 0 silent infeasibilities. Fallback path exercised |
| 10 | T-ORC-10 | high-F_c shared limit PASS | Budget non-binding: VSC ≥ 0 on 8 seeds; shared capability chosen at normal F_c in 8/8. At F_c × 10⁴ the all-shared portfolio is affordable but worse, so it is rejected on value and VSC = 0 |
| 11 | T-ORC-12 | Model D gate PASS | Every single T1–T4 failure, and a T5 failure, gives `MODEL_D_NOT_IDENTIFIED` with 0 tri-level calls. With all five true, the tri-level solve executes (pess 1.0 vs bilevel 0.0) |
| 12 | T-ORC-13 | reproducibility PASS | Identical results and SHA-256 across 2 in-process and 2 fresh-process runs (`e072fe1a…`) |
| 13 | T-INV-4 | label permutation invariance PASS | 3 seeds; units, initiatives, roles and capabilities renamed; the full optimal set (B) is equal after inverse mapping; C values equal |
| 14 | T-SEN-3 | Lemma R scope test PASS | 3 certified portfolios: 60 interior samples per seed found no violation, and element classification agrees. 30 uncertified: vertex gap ≤ sampled gap. ScopeError for C and element scope. Element counterexample: vertices only gives ROBUST, adding the interior gives FRAGILE |
| 15 | T-SEN-4 | robust feasibility PASS | Classes 239 robust / 118 conditional (each with a joint witness) / 0 / 0. The risk-sensitive config is never robust. INFEASIBLE when violated at every vertex. The jointly-infeasible example gives UNDETERMINED |
| 16 | T-SEN-6 | scenario registry hashing PASS | Commitment computed before the solve; tampering is detected for range, eps_R, range + 1e-12, and nominal × (1 + 1e-12) |
| 17 | T-SEN-7 | MaxRegret PASS | Seed 10: MMR 15.874 over 4 vertices and 356 robust candidates; vertex MaxRegret never exceeded on a 49-point interior grid |
| 18 | T-SEN-7 | VOI monotonic information test PASS | Analytic oracle: vertex VOI 1 (overstated), grid VOI 0.5 (true). Portfolio: 0 ≤ grid VOI ≤ vertex VOI |
| 19 | T-SEN-8 | Model C delta nonmonotonic counterexample PASS | B: at most one 0 → 1 switch (7/8 seeds switch). C: `y_c*` = 1, 1, 1, 1, 0, 0, 0, 1 over δ = 0, 1, 2, 2.9, 3, 3.5, 4, 5, so the build region is set-valued |
| 20 | T-ORC-8 | independent hand-oracle rederivation PASS | §8 |

Extra groups: **REG** (v2.1 regression: P1 with C0, P2, identities, P8 screening 10 → 15, P7 in B, P6 money scaling) and **AUDIT** (regressions for the review findings, §7).

## 3. Propositions after v2.2 testing

| Proposition | Status after v2.2 | Change |
|---|---|---|
| P1–P3, P5, P6 | Not refuted on synthetic instances | none |
| P4 (F_c threshold) | Holds in B and C; bisection is valid | none |
| P4 (δ threshold) | Unique in B; **set-valued in C** (T-SEN-8 counterexample) | 42 §15 P4 states the counterexample |
| P7 | Holds in B only | none (v2.1 already restricted it) |
| P8 | Screening example reproduced (10 → 15) | none |
| Lemma E | Superseded by **Lemma E′** (smaller, exact for opt and pess) | 42 §12.4 |
| Lemma R | Exact only for Model B whole portfolios with registry blocks of a single factor kind; ScopeError otherwise | `validate_registry` now enforces the multilinear precondition |

**Counterexamples kept, propositions revised, tests not altered to fit:**

- The C-δ non-monotonicity was kept, and P4 was revised.
- The element-level Lemma R counterexample was kept, and the scope was restricted.
- The vertex-VOI overstatement was kept, and VOI is now reported in two versions.
- The v2.1 feasibility dichotomy was replaced by four classes after a joint-infeasibility counterexample.

## 4. Performance notes

The full suite takes several minutes (roughly 5–10) in a single process on the session machine. The robust tests use `n_init = 1` instances (≈ 360 candidate portfolios). Lemma E′ reduced the per-unit envelope set from at most |𝒫|² to |𝒫|.

## 5. Limitations

- All instances are synthetic. Passing says the implementation agrees with 42 v2.2 and that its propositions were not refuted on these instances. It says nothing about any enterprise.
- Element-level robustness, the Model C λ scan and VOI are classified only on evaluated points (vertices, grid, samples), with coverage reported. They are never certificates.
- The registry factor-kind rule is conservative: it may reject blocks that are in fact affine.
- The run uses one model family for both implementation and review (§7). Human code review remains advisable before any enterprise use.

## 6. Lemma E′ confirmation

The first adversarial reviewer brute-forced Lemma E′ against the v2.1 product envelope set on 800 random follower instances: optimistic and pessimistic leader values were identical in every case. The second reviewer re-derived the proof (42 §12.4) and found it correct.

## 7. Adversarial reviews and fixes

**Round 1 (13 findings).** Status after fixes, as confirmed by round 2:

| # | Finding | Fix | Round-2 verdict |
|---|---|---|---|
| 1 | `solve_robust` built candidates from nominal-feasible portfolios, which drops robust ones | θ-independent superset → `robust_feasibility`; AUDIT regression (209 portfolios recovered) | FIXED |
| 2 | Missing λ effectively zero-filled; override leaked into λ^u | role detection, box scan, F_E^{−time} over all roles, override on enterprise λ only | PARTIAL → fixed in round 2 (see below) |
| 3 | T-MIS-6 vacuous | three-way criterion (no point / different payload / disclosed) | FIXED |
| 4 | DP bound could be silently wrong | ceil/floor DPs, enumeration fallback, bilevel bound reported | FIXED |
| 5 | T-ORC-9 never binding | budget × 0.3 (binding asserted ≥ 5; observed 20) + random fuzz | FIXED |
| 6 | λ scan only on the diagonal | box vertices | FIXED |
| 7 | Exceptions escaped `solve`; Model A infeasible labelled INVALID | guarded wrapper; `ModelAInfeasible` → INFEASIBLE | PARTIAL → fixed in round 2 |
| 8 | Missing inputs handled at the wrong scope | only requested policies checked; Allow(j,0) and state lookups config-local; THRESHOLD_MODE B/C only; C opt+pess; absent λ key | PARTIAL → fixed in round 2 |
| 9 | VOI vertex-only; tautological asserts | vertex + grid VOI; analytic oracle | FIXED |
| 10 | CONDITIONALLY_FEASIBLE could be wrong | joint witness required; otherwise UNDETERMINED | FIXED |
| 11 | k = 0 F5e state; capability-state ρ ignored | chosen-state F5e for all k; `(z, ℓ, s)` rows | FIXED |
| 12 | Registry hash omitted nominal values and rounded floats | `_exact` (float.hex) + nominal values | FIXED (solve_robust); round 2 extended to `solve(registry=…)` |
| 13 | Header cited a nonexistent 42 v2.2; T-ORC-8 independence undocumented; T-ORC-10 passed by unaffordability; element classification missing | 42 v2.2 written; §8; affordable large-F_c test; `classify_element` + tests | FIXED |

**Round 2 (7 new issues).** All were fixed and are covered by the AUDIT test:

1. Missing λ on an infeasible instance returned INVALID (KeyError). It now returns `INFEASIBLE` with `PARTIAL_OBJECTIVE`.
2. C/C0/A were "certified" from a grid. Now C/C0 give `ROBUST_ON_GRID` with no point decision, and A gives `NO_LEADER_DECISION`.
3. An inexact DP was used inside the λ certificate. Solves inside the scan are now always exhaustive.
4. A status-quo gap in one capability state rejected the whole solve. Any lookup gap is now local to (j, k, s).
5. `beta = 0` or a tiny β escaped as ZeroDivision/Overflow. β is now validated, and ArithmeticError is mapped to INVALID.
6. `solve(registry=…)` emitted no commitment. It now does, and `verify_registry(r, reg, inst)` passes.
7. Overlapping blocks overwrote each other, and a block could span several factor kinds (breaking multilinearity). `validate_registry` now rejects both.

Round 2 also flagged a latent T-SEN-3 logic gap: "certified ⇒ element ROBUST" holds only when no portfolio is merely conditionally feasible. The assertion is now guarded by that condition.

Both reviewers ran on the same model family as the implementer. This is weaker than independent human review and is recorded as a limitation.

## 8. Independent hand-oracle rederivation (T-ORC-8)

**Procedure.**

- A separate agent context was told not to read any file and not to run code.
- It received only a verbal specification of the fixture: two units, one initiative each, two configurations, one shared capability with F_c = 10, N = 10, degenerate probabilities, U1 v_u = 3 with C_impl = 5, and U2 v_u = 2.
- It also received the definitions of the forms A, C0, A+, B and C (optimistic and pessimistic), the metric definitions, and three scenarios for U2: aligned (C_impl 5, l_x 0); misaligned and blockable (C_impl 5, l_x 2.5); misaligned and unblockable (C_impl 0, l_x 2.5).
- It derived every value by hand with the arithmetic shown.
- Its table was recorded first and then compared with the solver. Expected values in `t_orc8_independent_hand` are the agent's values.

**Result (both opt and pess unless stated):**

| Scenario | A | C0 | A+ | B | C | VRA | DL0 | VCP | VSC | DL | NEV |
|---|---|---|---|---|---|---|---|---|---|---|---|
| aligned | 0 | 0 | 0 | 30 | 30 | 0 | 0 | 0 | 30 | 0 | 30 |
| blockable | 0 | 0 | 0 | 15 | 15 | 0 | 0 | 0 | 15 | 0 | 15 |
| unblockable | 0 | 0 | 0 | 15 | 10 | 0 | 0 | 0 | 15 | 5 | 10 |

**Why the scenarios differ:**

- **Blockable:** the leader can give U2 an envelope below 5, so U2 cannot afford its harmful AI configuration and DL = 0.
- **Unblockable:** U2's AI costs 0, so no envelope excludes it once c is built, and DL = 5.
- **A = C0 = A+ = 0** because without the shared capability no AI configuration is feasible.

The solver matched all 66 values (3 scenarios × 11 metrics, opt and pess). **`INDEPENDENT_COMPUTATIONAL_REDERIVATION_PASS`.**

**Independence limits:**

- The specification was written by the study team, so a shared misreading of 42 would not be caught.
- The checker is the same model family as the implementer.
- A human second rederivation remains advisable before any of these fixtures is cited as a teaching example.
