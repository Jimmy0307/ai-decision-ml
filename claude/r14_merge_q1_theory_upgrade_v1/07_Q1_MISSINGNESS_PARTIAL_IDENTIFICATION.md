# 07 — Missingness as a model-identification problem: three classes and the v2.2 status machine (Task G, theory agent T2)

**Status:** Q1 theory-upgrade candidate, 2026-10-14. Additive to canonical v2.2. 42 and 51 were read only. The per-site T-MIS-6 table in §6 comes from a sidecar (`work/T2/mis6_per_site.py`, `work/T2/bracket_check.py`) that imports a **copy** of 51 placed in `work/T2/`. It is a synthetic regression on 51's seed-5 instance, not a proof.
**Positioning.** This is a **methodological / model-identification** contribution: how a decision model should report its output when an input is unidentified. It is **not** a new theory of the enterprise. Propositions G1–G7 are TYPE C. The partial-identification literature would be the natural TYPE B anchor, but it is **not in the 59a reference list** (see §8).

**Verdict lines**

```
CLASSES (formal)                    = DC (decision-changing), DIER (decision-invariant but epistemically relevant), NULL; channel FC (feasibility-changing) orthogonal
ZERO_FILL_BIAS_DIRECTION (B)        = PROVEN by constraint role (Prop G1); undetermined in C (P8 mechanism)
RESTRICTED_SOLVE_LOWER_BOUND        = PROVEN in B (Prop G2); FALSE in C (W8a part 2)
SINGLE-OPTION MONOTONE CELL         = threshold-identified decision map in B (Prop G3); zero-fill = best-case endpoint, restricted = worst case
LAMBDA DC vs DIER vs NULL           = exactly decidable at box vertices in B/A+ (Prop G4, corrected: EVERY zero-fill optimum must be vertex-optimal; NULL separated); grid only in C
F_c                                 = THRESHOLD_MODE is the sharp identified decision map (Prop G5, from P4)
LEDGER SPLIT                        = NULL for B's own output, DC-possible for C (Prop G6; W8b part ii)
INADMISSIBLE ZERO                   = zero-fill outside Theta_adm for 14/40 T-MIS-6 runs (10 INVALID, 4 INFEASIBLE)
STATUS-QUO CELL                     = decision-relevant (Remark G7) -> contradicts 59a l.1327 priority-(4) rationale (flag for integrator)
T-MIS-6 reconciliation              = 12/16/12 bins reproduced per site; bins are solver-output classes, not the formal classes (mapping §6)
```

---

## 0. Exact v2.2 sources relied on

| Item | 42 location | Content |
|---|---|---|
| No zero imputation | §1.3 item 5, l.45 | "缺值補 0、補平均、補 synthetic 值" is forbidden |
| UNIDENTIFIED (element) | §13.2, l.530 | "至少一個影響 `d` 的必要參數沒有可接受界 … 或該參數的缺值使某個可能最適的候選配置被排除" |
| Missing-value rules | §13.4, l.564–576 | per-site rules → `RESTRICTED_SOLVE`, `THRESHOLD_MODE` (B, C), `PARTIAL_OBJECTIVE`, `FOLLOWER_LEDGER_UNIDENTIFIED`, `UNEVALUABLE_INITIATIVE`, `REJECT_INSUFFICIENT_IDENTIFIED_INPUTS`, `OK_INTERVAL` |
| No-silent-zero test semantics | §13.4, l.578 | each missingness must, relative to the zero-filled instance, (a) emit no point decision, or (b) emit a different decision/objective, or (c) emit the same decision but disclose the missing input, which the zero-fill does not (T-MIS-6) |
| λ rule | §7.4 (i)–(iv), l.302–304 | two-component objective `(F_E^{−time}, ΔHours)`; point decision only if invariant on `∏[0,λ^U]`; exact at vertices for B/A+; grid only for C/C0 |
| P4 | §15, l.632 | `y_c* = 1 ⇔ F_c ≤ F_c^†` in B and in C (per mode) |
| P8 | §15, l.640 | in C, narrowing the follower's option set can **raise** leader value |
| F5e/Allow missing | §5, l.202 | missing `R_j(s)`, `D_j(s)`, `Allow_γ(j,k)` exclude only that `(j,k,s)` (`RESTRICTED_SOLVE`) |

---

## 1. Setup

Let `θ = (θ_{−p}, θ_p)`, where `p` is a parameter cell (or block) that is **missing**. Let `V_p` be its admissible set. This is the registered bound if one exists (42 §13.1). Otherwise it is the logical domain `Dom_p`: e.g. `[0,∞)` for a cost, resource use or loss; `{0,1}` for `Allow`; the simplex for a `ρ` row; the ordinal code set for a requirement. For a model `M`, write:
* `X(θ)`: the feasible set of whole decisions;
* `D*(θ) ⊆ X(θ)`: the optimal set (ties included; for C, the leader's optimal set per mode);
* `F*(θ)`: the optimal value;
* `R(θ) = (D*(θ), F*(θ), X(θ))`: the **result object** that an `OK_POINT` output claims to have identified.

**Zero-fill** sets `θ^0 = (θ_{−p}, 0)`. Note that `0` need not lie in `V_p`.

**Identified sets** (in the sense of "all results consistent with the identified inputs"):
* `ID_D = ∪_{v∈V_p} D*(θ_{−p},v)` — decisions that are optimal for some admissible value;
* `RD = ∩_{v∈V_p} D*(θ_{−p},v)` — decisions that are optimal for every admissible value;
* `ID_F = {F*(θ_{−p},v) : v ∈ V_p}`;
* `ID_X = {X(θ_{−p},v) : v ∈ V_p}`.

## 2. The three classes

**Definition G (classes of missingness for model `M`).**
* **DC — decision-changing.** `∃ v ∈ V_p : D*(θ^0) ⊄ D*(θ_{−p}, v)`. Some decision that zero-fill may output is not optimal, or not feasible, at an admissible value.
* **DIER — decision-invariant but epistemically relevant.** `D*(θ^0) ⊆ RD` (zero-fill's decisions are optimal for every admissible value), **and** `R(θ_{−p}, ·)` is not constant on `V_p`: the value or the feasible set is not point-identified. An `OK_POINT` output that reports `F*(θ^0)` or `X(θ^0)` as identified overstates what the data identify.
* **NULL.** `D*(θ^0) ⊆ RD` and `R` is constant on `V_p`. Zero-fill does no harm to *this model's* result object.
* **Channel tag FC — feasibility-changing.** `∃ v ∈ V_p : X(θ^0) ≠ X(θ_{−p}, v)`. FC is orthogonal to the outcome classes: FC∩DC, FC∩DIER and FC∩NULL can all occur. **Objective-ranking-changing** missingness is DC ∧ ¬FC: the feasible set is fixed and the ranking of feasible decisions moves.

DC, DIER and NULL partition all cases. *Proof:* either `D*(θ^0) ⊄ RD`, which is DC by definition, or `D*(θ^0) ⊆ RD`, which splits on whether `R` is constant. ∎ The 42 §13.2 UNIDENTIFIED label is the element-level form of "`ID_D` contains decisions differing in that element", i.e. the element is not robust over `V_p`.

---

## 3. Propositions

**Proposition G1 (direction of zero-fill bias by constraint role; Model B).** Let `p` enter the constraints and/or the objective monotonically, **with the same sign of effect** (raising `p` weakly shrinks the feasible set and weakly lowers every feasible value, or weakly enlarges it and weakly raises every value). *(Premise corrected T7 per Q/11 §2.11: the earlier "only constraints" did not match the list, since `C^impl` also enters (OBJ-E) as `−C^impl`; both effects push the same way, so the conclusion is unchanged.)*
(i) If `p` is a **use** term — a non-negative left-hand side of `≤`: `a^h_jk`, `C^impl` in `a^BUD`, `t^REV` in (R2), `N E[I^sev]` in (F9) — or a **requirement threshold** — `H^req`, `WI^req`, `EA^req`, `G^req`, `R^req`, `D^req` at the scale minimum — then `X(θ^0) ⊇ X(θ_{−p},v)` for all `v ∈ V_p`, and `F*(θ^0) ≥ F*(v)`. Zero-fill fabricates feasibility (optimistic bias).
(ii) If `p` is a **capacity or permission** term — `Ā^h`, `ΔK̄^REV_u`, `ē_j`, `Allow`, `Allow^loc`, `Legal`, `G_j(γ)` (permission level) — then `X(θ^0) ⊆ X(v)` and `F*(θ^0) ≤ F*(v)`, possibly with `X(θ^0) = ∅` (pessimistic bias, or fabricated infeasibility).
In Model C neither inequality on `F*` holds in general, because shrinking or growing the follower's option set can move leader value either way (P8).

*Proof.* Monotonicity of each constraint in `p`, plus `0 = min V_p` for the listed non-negative cells, gives the set inclusions. Maximizing over nested sets an objective that moves in the same direction gives the value inequalities. For C, P8 and W8a part 2 give counterexamples. ∎

**Proposition G2 (`RESTRICTED_SOLVE` is a lower bound and a safety test in B, not in C).** Let `p` affect only one option `o = (j,k,s)`, and let the restricted problem exclude `o` (42 §13.4). Write `F^R` and `D^R` for its optimal value and set.
(i) Model B: `F^R ≤ F*(θ_{−p}, v)` for every `v ∈ V_p`, because the restricted feasible set is a subset of every admissible feasible set with the same values on it.
(ii) Model B: `D^R ⊆ RD` iff, for every `v`, no portfolio using `o` strictly beats `F^R`. If so, the exclusion is decision-safe and the restricted output is correct, with `X` disclosed as unidentified (DIER via the FC channel).
(iii) Model C: (i) is **false**. In W8a part 2, the follower has options `a` (`u = 5`, `Ψ = 5`) and `b` (`u = v` missing, `Ψ = −3`), all at cost 0. Excluding `b` gives `F^R = 5`. The true pessimistic value is `5` for `v < 5` and `−3` for `v ≥ 5`, so `F^R > F*(v)` on `[5, 10]`.
*Proof of (i)–(ii):* inclusion and identical values on the subset. (iii) by the example. ∎

**Proposition G3 (single-option monotone cells have a threshold decision map; Model B).** Let `p` affect only option `o`. Suppose that as `v` grows, `o`'s objective contribution is non-increasing, its resource use is non-decreasing componentwise, and its feasibility flags are non-increasing (e.g. `C^impl`, `l`, `c`, `a^ENG`, `t^REV` of `o`). Let `V_p = [0, U]` with `U ≤ ∞`. Then:
(a) `W_o(v) := max{F(d;v) : d uses o, d feasible}` is non-increasing, and `W_{¬o} = F^R` is constant;
(b) `o` is used at the optimum iff `v ∈ {v : W_o(v) ≥ F^R}`, which is a down-set `[0, v^†]` or `[0, v^†)`. The decision map is threshold-identified, exactly as P4 is for `F_c`;
(c) **endpoint bracketing:** `F^R ≤ F*(v) ≤ F*(0)`. If `F*(0) = F^R` (zero-fill does not strictly gain from `o`), then every `d ∈ D^R` lies in `RD`. The missingness is then DIER (when `o` is FC-relevant) or NULL, and zero-fill's decision coincides with the honest one. If `F*(0) > F^R`, it is DC whenever `v^† < U`.
*Proof.* (a) Each portfolio using `o` loses value and feasibility as `v` grows, and the others are unaffected. (b) is the level set of a non-increasing function. (c) uses `F*(v) = max(W_o(v), F^R)`. If `W_o(0) ≤ F^R`, then `W_o(v) ≤ F^R` for all `v`, so `F*(v) = F^R` and `D^R ⊆ D*(v)`. ∎
*Reading.* Zero-filling such a cell evaluates the **best case** for `o`. The honest restricted solve evaluates the **worst case**: `v → U`, or `o` removed. The two solves together bracket the identified set. Zero-fill's error is not the number it computes but presenting that endpoint as the point.

**Proposition G4 (λ: exact DC/DIER separation in B/A+; grid only in C).** With `V = ∏_ℓ [0, λ^U_ℓ]` and fixed portfolios, `F_E(d;λ) = F_E^{−time}(d) − Σ_ℓ λ_ℓ ΔHours_ℓ(d)` is affine and feasibility does not depend on `λ` (42 §7.4). So, by Theorem R1 / Cor R1b (doc 06):
*(Corrected T7 per Q/11 §2.10. The earlier wording, "DIER iff **some** decision is optimal at all `2^m` vertices", did not match Definition G, which requires `D*(θ^0) ⊆ RD`, i.e. **every** zero-fill optimum robust, and it did not separate DIER from NULL. Counterexample to the old wording: `d1` with `F^{−time} = 10, ΔHours = 0` and `d2` with `F^{−time} = 10, ΔHours = 1`, `λ ∈ [0,4]`: `D*(λ=0) = {d1, d2}`, `d1` is optimal at both vertices, but `d2` is not optimal at `λ = 4`, so the case is DC by Definition G.)* Write `D*_0 := D*(λ = 0)` for the zero-fill optima. By Thm R1, a fixed portfolio is optimal on the whole box iff it is optimal at all `2^m` vertices. Hence:
* **DC** iff some element of `D*_0` is not optimal at some vertex. v2.2 emits no point decision.
* Otherwise every element of `D*_0` is optimal on the box (`D*_0 ⊆ RD`); all of them then have the same `F` everywhere, and `F*(λ) = F_E(d°;λ)` for any `d° ∈ D*_0`. **NULL** iff, in addition, `R` is constant on the box: `ΔHours_ℓ(d°) = 0` for all `ℓ` (so `F*` is constant) **and** no `d ∉ D*_0` is optimal at any vertex (so `D*` is constant; for such `d`, `F_E(d°) − F_E(d)` is affine and `≥ 0` on the box, so it vanishes somewhere iff it vanishes at a vertex). `X` does not depend on `λ`. All three checks are vertex checks.
* **DIER (certified)** in the remaining case: every zero-fill optimum is optimal on the box, but `F*` or `D*` varies. Then `ID_F = [min_vertex F*, max_vertex F*]`, and v2.2 reports `(F_E^{−time}, ΔHours)` with `decision_valid_for_all_lambda_in_box`.
* Zero-fill (`λ = 0`) is one vertex. It is the **upper** end of the value interval for portfolios with `ΔHours ≥ 0` and the lower end when `ΔHours ≤ 0`.
* In C/C0 the leader's value passes through the follower's argmax (doc 06 Prop R5), so only `ROBUST_ON_GRID` is available, and v2.2 correctly refuses a point decision.
λ is a pure objective channel (¬FC), so its DC case is objective-ranking-changing.

**Proposition G5 (F_c: `THRESHOLD_MODE` is the sharp identified decision map).** With `V_{F_c} = [F^L, F^U]`, P4 gives, in B and in C per mode, `ID_D(y_c) = {1}` if `F^U ≤ F_c^†`, `{0}` if `F^L > F_c^†`, and `{0,1}` otherwise (DC). When `F^L = 0` (the logical domain), zero-fill selects the most build-favourable endpoint. `F_c` also enters (R1) as `a^BUD_c = F_c`, so it is FC as well; P4's `sup` definition already accounts for this. Reporting `F_c^†` (both modes in C) instead of a point therefore reports the identified set exactly.

**Proposition G6 (follower-ledger split).** Let `p` be a ledger-split cell that does not change enterprise totals: `C^impl,x`, `τ`, or the split `v^u/v^x` or `l^u/l^x` with the total fixed.
(i) Model B, A+: `p` does not enter (OBJ-E), the constraints, or any B output, so it is **NULL** for B. This is what 51 discloses as `unidentified_inputs_not_used_by_this_model`. At the level of the *architecture contract* it is relevant: `DL = F^B − F^C` and `NEV` are not identified.
(ii) Model C: `p` enters (OBJ-U) and can therefore be **DC**. W8b part (ii) uses the W5 instance at `δ = 3.5`. U2's enterprise loss is fixed at `2.5/event`, and the split `s = l_x ∈ [0, 2.5]` is missing. U2's follower gross is `10(s − 0.5)`. For `s ≤ 0.5`, U2 chooses k=0 and C builds `c`. For `s > 0.5`, U2's k=1 is unblockable and C does not build. B builds for every `s`.
So `FOLLOWER_LEDGER_UNIDENTIFIED` (refuse C, solve B, mark DL UNIDENTIFIED) is the conservative output. A sharper alternative, not implemented, would be to report the C decision as a function of the split, analogous to `THRESHOLD_MODE`.

**Remark G7 (status-quo outcome cells are decision-relevant).** For one initiative with `N_j0 = N_j1 = 1`, write `x` for the status-quo per-event value. Then `φ_j0 = 0` and `φ_j1 = g_1 − x − C^impl`. So `k = 1` is optimal iff `x < g_1 − C^impl`; in W8b part (iii), `x < 4`. The status-quo cell enters the comparison between keeping `k = 0` and switching. It cancels only between portfolios that agree on whether `j` stays at the status quo. 42 §13.4 is consistent with this: it marks the initiative `UNEVALUABLE_INITIATIVE`. But 59a §3.14 (l.1327, priority level (4)) says the precision of status-quo outcome cells has low marginal value because they "在所有候選 portfolio 中以相同方式出現，在 regret 與 VOI 的差分中抵銷". **That rationale is false in general.** **Flag for the integrator:** restrict the statement to the baseline term `N_j0 g_j0(ȳ^cur)`, or move status-quo cells up a priority level.

**Proposition G8 (inadmissible zero).** If `0 ∉ V_p` (ordinal codes without a 0 level, normalized probability rows, a strictly positive `ē` policy, `N > 0`), then `θ^0 ∉ Θ_adm`. The zero-fill result is not in any identified set, so it is neither DC, DIER nor NULL relative to `V_p`; it is out of model. In T-MIS-6, 14 of 40 zero-filled runs were out of model: 10 `INVALID_SCHEMA_OR_UNITS` (`G_j`, requirement cell, `R_state`, `D_state`, `ρ` probability, × B, C) and 4 `INFEASIBLE` (`ē`, `Ā`, × B, C).

---

## 4. Mapping to the v2.2 status machine

| Status (42 §13.4) | Missing site | Class (generic) | Why v2.2's output is the right epistemic report | Proposition |
|---|---|---|---|---|
| `RESTRICTED_SOLVE` | `Allow(j,k)`, `R_j(s)`/`D_j(s)`, config-level lookups, state-specific cells | FC (and DC or DIER) | B: `F^R` is a lower bound and `D^R` is safe iff no excluded option can win. Excluding plus disclosing reports the worst-case endpoint honestly, and affected elements are marked UNIDENTIFIED. C: no bound (P8). | G1, G2, G3 |
| `THRESHOLD_MODE` | `F_c` (B, C) | DC (+FC via R1) | Reports the full decision map `F_c ↦ y_c*` (per mode in C) | G5 |
| `PARTIAL_OBJECTIVE` | `λ_ℓ` | DC or DIER (objective channel) | B/A+: an exact vertex certificate separates DIER (decision, two-component value) from DC (no point). C: grid only, never a point. | G4 |
| `UNIDENTIFIED` (element label) | any `p` with `|ID_D|` > 1 in that element | DC at element level | Literal definition, 42 §13.2 | Def G |
| `FOLLOWER_LEDGER_UNIDENTIFIED` | `C^impl,x`, `τ`, ledger split | NULL for B, DC-possible for C | C refused, B solved, DL UNIDENTIFIED | G6 |
| `UNEVALUABLE_INITIATIVE` | status-quo cells | DC-possible | The comparator of every switch decision is missing | G7 |
| `REJECT_INSUFFICIENT_IDENTIFIED_INPUTS` | `Ā`, `ΔK̄^REV`, all policies' `ΔC^gov` | FC (capacity) | Without capacity, `X` is not identified at all | G1(ii) |

## 5. Witnesses (W8a–c; `witness_parts/w_mono_rob_miss.py`)

| Witness | Class | Instance (algebraic) | Zero-fill | Honest v2.2 output | Identified set |
|---|---|---|---|---|---|
| **W8a** | FC ∩ DC | `φ_j1 = 5`; `a^ENG_j1 = v` missing, `V = [0,30]`; `Ā^ENG = 10` | `k = 1`, `F = 5`, OK_POINT, nothing disclosed. Infeasible for `v ∈ (10,30]`. | `RESTRICTED_SOLVE`: `k = 0`, `F^R = 0` (lower bound), excluded `(j,1)`, `q_j` UNIDENTIFIED | `ID_D = {0,1}` with threshold `v^† = 10` (G3) |
| W8a part 2 | C counterexample to G2(i) | follower options `a` (5/5), `b` (`u = v` missing / `Ψ = −3`), cost 0 | — | Restricted `F^R = 5` | true pess value `−3` for `v ≥ 5`, so `F^R` is not a lower bound |
| **W8b** | DC ∧ ¬FC | `F^{−time}_1 = 10`, `ΔHours_1 = 5`, `λ ∈ [0,4]` | `k = 1`, `F = 10` | `PARTIAL_OBJECTIVE`, FRAGILE, no point | `k = 1` iff `λ ≤ 2` (tie at 2) |
| W8b (ii) | DC (C only) | ledger split `s ∈ [0,2.5]`, W5 instance at `δ = 3.5` | `s = 0` ⇒ build | `FOLLOWER_LEDGER_UNIDENTIFIED` | C: build iff `s ≤ 0.5`; B: build ∀`s` |
| W8b (iii) | DC | status-quo value `x` missing | — | `UNEVALUABLE_INITIATIVE` | `k = 1` iff `x < 4` |
| **W8c** | DIER | `F^{−time}_1 = 10`, `ΔHours_1 = 1`, `λ ∈ [0,4]` | `k = 1`, `F_E = 10` reported as identified | `PARTIAL_OBJECTIVE`, certified decision, `(10, 1)` | decision `{1}`; value `[6, 10]` |
| W8c (Allow) | FC ∩ DIER | `Allow(j,2)` missing; `φ_2 ∈ [0,3] < φ_1 = 5` | `k = 1` (Allow treated as 0) | `RESTRICTED_SOLVE` (disclosed) | decision `{1}`; `X` not identified |

*Minimality:* each core witness has 1 initiative, 2 options and 1 missing scalar. A single-option instance has no decision, so it cannot be smaller. W8a part 2 needs a follower with ≥ 2 non-status-quo options.

## 6. Reconciliation with 51 T-MIS-6 (40 mutations: 12 / 16 / 12)

T-MIS-6 compares, on 51's seed-5 instance, the honest solve with a missing cell against the zero-filled solve. It sorts each run into (a) no point decision, (b) a different payload, or (c) the same payload with disclosure. These **bins are classes of solver behaviour on one instance**, not the formal classes of Definition G: the formal classes need `V_p`, which T-MIS-6 does not specify. The sidecar reproduces the counts per site (B | C):

| Site (T-MIS-6) | Honest status | Zero-fill status | Bin (B, C) | Formal reading |
|---|---|---|---|---|
| `F_c` | THRESHOLD_MODE | OK_POINT | (a), (a) | DC-possible (G5) |
| `λ` | PARTIAL_OBJECTIVE | OK_POINT | (a), (a) | Seed 5: not certified, so DC on the box (B); C grid-only (G4) |
| `Ā` | REJECT | INFEASIBLE | (a), (a) | FC; zero out of model (G8) |
| `ΔC^gov` | REJECT (+RESTRICTED) | OK_POINT | (a), (a) | Only policy unusable |
| `rev_cap` | REJECT | OK_POINT | (a), (a) | FC capacity (G1 ii) |
| `impl_x`, `τ` (ledger) | B: OK_POINT, disclosed; C: FOLLOWER_LEDGER_UNIDENTIFIED | OK_POINT | B (c), C (a) | B NULL (contract-level DIER); C DC-possible (G6) |
| impl cell (S) | RESTRICTED_SOLVE | OK_POINT | (c), (c) | **B: DIER proved by G3(c)**. Zero-fill = best case equals restricted = worst case. Sidecar: same decision at `v ∈ {0,1,10,100,10^6}`. C: evaluated points only. |
| eng cell (S) | RESTRICTED_SOLVE | OK_POINT | (c), (c) | Same as impl cell (FC channel) |
| outcome cell `l_u` (k>0) | RESTRICTED_SOLVE | OK_POINT | (c), (c) | Same as impl cell (objective channel) |
| `Allow`, `Allow^loc` | RESTRICTED_SOLVE | OK_POINT | (c), (c) | Binary domain `{0,1}`. Sidecar evaluated both values, so FC ∩ DIER on this instance, exactly for B and C. |
| outcome cell (status quo) | UNEVALUABLE_INITIATIVE | OK_POINT | (b), (b) | DC-possible (G7) |
| `N` | RESTRICTED_SOLVE | OK_POINT | (b), (b) | Non-monotone cell (`N` multiplies `g`, `I^sev`, `t^REV`); no bracket |
| `G_j`, requirement cell, `R_state`, `D_state`, `ρ` prob | RESTRICTED / UNEVALUABLE | **INVALID_SCHEMA** | (b), (b) | Zero out of model (G8) |
| `ē` | UNEVALUABLE_INITIATIVE | **INFEASIBLE** | (b), (b) | Zero out of model / fabricated infeasibility (G1 ii, G8) |

Totals: (a) 12 = 5 sites × 2 + ledger in C × 2; (b) 16; (c) 12 = 5 sites × 2 + ledger in B × 2. This matches baseline stdout l.8. In every (c) run the zero-filled run discloses nothing (zero-fill status OK_POINT), which is the "falsely raised certainty" of DIER. Of the 16 (b) runs, only 4 (status-quo cell and `N`, × 2) are genuinely different point decisions. The other 12 are zero-fills that leave the model (10 INVALID, 2 INFEASIBLE). So T-MIS-6 bin (b) mixes DC-type and out-of-model cases, and bin (c) is *necessary but not sufficient* for DIER. Sufficiency needs G3(c) (monotone single-option cells in B) or exhaustive evaluation of a finite domain (`Allow`).

## 7. Relation to P1–P8, Lemma E′ and v2.2

* G1 and G2(i) rely on B being a plain maximization over nested sets. G2(iii) and G6(ii) are instances of P8 (C value is not monotone in the follower's option set). G5 is P4. G4 is Lemma R (doc 06 Theorem R1). Lemma E′ is untouched.
* No contradiction with 42. The propositions explain *why* each 42 §13.4 rule is the correct epistemic output, and when an `OK_POINT`-equivalent decision would be safe (G2(ii), G3(c), G4 certified). One manuscript inconsistency is flagged (Remark G7; 59a l.1327).

## 8. Literature positioning

| Claim | Type | Anchor |
|---|---|---|
| Report the set of results consistent with the identified inputs rather than impute (identified sets, bounds) | TYPE B | Partial-identification literature (e.g. Manski): **[NOT IN 59a REFERENCE LIST — TO VERIFY; add and verify before citing; do not invent details]** |
| Set-based treatment of unidentified parameters instead of a prior | TYPE B | Ben-Tal et al. (2009) (in list) |
| Identification requires stated assumptions (causal effect identification) | TYPE B, loose | Angrist et al. (1996) (in list); used only for the general point that identification is assumption-dependent. It does **not** support the propositions here. |
| Definition G, Props G1–G8, Remark G7 | TYPE C (in-model; known framework applied — TO VERIFY) | Definition G is a decision-theoretic restatement of partial identification (identified set vs robust decision set; Manski, to verify). G1–G3 are elementary monotone comparative statics; G4 is Thm R1 (Lemma R) applied to the λ box; G5 is P4. Substantive in-model content: G2(iii) (C counterexample to RESTRICTED_SOLVE as a lower bound), G3(c), the corrected G4, and Remark G7 (59a l.1327 is false). Methodological, not enterprise theory; place in Methods/Appendix, not among the theory contributions |

**AI-specificity (T7 per Q/11 A11).** Definition G and G1–G8 apply to any decision model with a status machine for unidentified inputs; nothing here is AI-specific.

**Restatement vs genuinely new (consistent with Q/11 A8, §3 item 6).** *Restatement / specialization:* G4 (Thm R1 on the λ box), G5 (P4), G1–G3(a)(b) (elementary monotone comparative statics), Definition G (partial-identification logic in decision form). *Genuinely new in-model:* G2(iii), G3(c), the corrected G4 quantifier with the NULL/DIER split, G6(ii), G8, and Remark G7 (a manuscript error).

## 9. NOT PROVEN / open

* For Model C, the DIER status of the T-MIS-6 continuous cells (impl, eng, `l_u`) is established only at the evaluated points `{0, 1, 10, 100, 10^6}`, since G3 does not hold in C.
* Multi-option cells (one missing value shared by several options, e.g. `N`, `ρ` rows, `ΔC^gov`) have no general bracketing result. Their class must be decided by scanning `V_p` with coverage reported.
