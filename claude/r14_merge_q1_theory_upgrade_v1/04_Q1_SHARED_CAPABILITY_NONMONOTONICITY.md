# 04 — Shared-capability reuse: monotone in Model B, possibly non-monotone in Model C (Task D, theory agent T2)

**Status:** Q1 theory-upgrade candidate, 2026-10-14. Additive to canonical v2.2. 42 and 51 were read only; nothing in REPO was modified.
**Evidence class:** Theorems D1 and D3, Propositions D4, D5, D6, Lemma I and Lemma M have complete proofs. D3 is a restatement (42 P2 applied pointwise in `(y,γ)`); D1 makes 42 P4's B part explicit; D4, D5, D6, Lemma M are TYPE C in-model results (known type of phenomenon, §8). Proposition D6 is an **existence** result. Its proof is an explicit hand-algebra construction, re-checked by the witness `witness_parts/w_mono_rob_miss.py::witness_W5_delta`. Conjecture M2 has only a proof outline and bounded-search support, so it is **not proven**. All numbers are SIMULATED_ONLY algebra: no enterprise parameters, no V7, no coder data.

**Verdict lines**

```
B_MONOTONE_IN_DELTA                 = PROVEN (Thm D1; uses A1 source indexing, A2 delta only on S-cells of C^impl/a^BUD,
                                      A3 delta-free feasibility, A4 no follower, A5 delta-free F_c, F^loc, DeltaC^gov, Abar)
BUDGET_BINDING_NEEDED_FOR_D1        = NO (W5b boundary instance has a binding budget and is still monotone under A1)
SOURCE_INDEXING_NEEDED_FOR_D1       = YES as an assumption: dropping it gives a B counterexample 1->0->1 (W5b, availability indexing)
C_CAN_BE_NONMONOTONE                = YES (Prop D6, existence; W5 = T-SEN-8 analog; W5-min single follower; W5_WIDE wide-margin supplement)
W5_FRAGILITY                        = W5 margins are 1 TWD on quantities of order 24-30 (survives ~1% joint perturbation, not 5%) and W5 depends on
                                      two exact zeros (net BUD footprint reaching ≤ the status quo's — a zero reused-cost floor in W5/W5_WIDE, or a positive floor offset by negative incremental opex — and zero ENG footprint) [T8-fix]; W5_WIDE widens the numeric margins to 3
                                      (367/400 survive +-5%) but has the SAME two structural zeros (§6, Q/09)
ALIGNMENT_RESTORES_MONOTONICITY     = YES (Thm D3: (AL1)-(AL4) => V_1^{C,opt} = V_1^{C,pess} = V_1^B for every delta; both modes, any ties,
                                      any cross-BU coupling, binding or not)
ALIGNMENT_NECESSARY                 = NO (Prop D4 partial alignment; Prop D5 delta-invariant separability)
BUILD_REGION_NOT_AN_INTERVAL        = PROVEN as existence (Prop D6); NOT claimed for all C instances
T-SEN-8 reconciliation              = EXACT (grid sequence 1,1,1,1,0,0,0,1 reproduced; continuous region [0,3) U (4,inf) strict / [0,3) U [4,inf) tie-build)
MINIMALITY                          = 2-option single follower impossible (Lemma M, proved); 3-option single follower with uniform reuse:
                                      NOT_PROVEN (Conjecture M2; 0 of 6,912 bounded-search instances)
```

---

## 0. Exact v2.2 sources relied on (42, read-only)

| Item | 42 location | Content used (quoted or paraphrased exactly) |
|---|---|---|
| Source state, `δ` | §10 item 5, l.396–402 | `s_jc = L` if `y^loc_{u(j)c}=1`; `S` if `y_c=1, y^loc=0`; `∅` otherwise; `C^impl_jk(s) = C^impl_jk(s_{j,Rel(j)})`; "共享重用效果定義為 `δ_jkc = C^impl_jk(s_c=∅) − C^impl_jk(s_c=S)`"; source indexing chosen because availability indexing "會使 `y_c=0` 分支的最適值隨 `δ` 改變而破壞 P4 的單調性" |
| Budget use | §5.1, l.208–212 | `a^BUD_jk(s) = C^impl_jk(s) + (N_jk E_jk[c] − N_j0 E_j0[c])` |
| Prerequisite | (F4), l.184 | `Φ^(F4)_jk = Π_{c∈Pre(j,k)} ȳ_jc` |
| (F5e) | l.187, 202 | evaluated at the **chosen source state** `s_j`, not at `δ` |
| Enterprise objective | (OBJ-E), l.297 | `F_E = Σ q φ_jk(ȳ,s) − Σ_c F_c(y_c − y^cur_c) − Σ F^loc y^loc − ΔC^gov(γ)` |
| Unit objective | (OBJ-U), l.319–323 | `φ^u_jk = N g^u_jk − N g^u_j0 − (C^impl_jk − C^impl,x_jk) − Σ_{c∈Pre} τ_jc y_c(1−y^loc)` |
| Alignment | §8.2, l.339–346 | (AL1) no external ledger items; (AL2) `τ = 0`; (AL3) no unit-only constraints, or they are also in the enterprise problem; (AL4) `λ^u = λ` |
| Follower response | §12.3, l.455–464 | `X*_u = argmax F_u` (tolerance `ε_tie`); `φ^opt_u = max_{X*_u}[…]`, `φ^pess_u = min_{X*_u}[…]` |
| Lemma E′ | §12.4, l.470–476 | it suffices to offer `E′_u = {a(x_u) : x_u ∈ 𝒫_u}`; exact for opt and pess |
| Leader | §12.5, l.486–494 | knapsack over `e_u`; maximize over `(y,γ)`; opt and pess separately |
| P2 | §15, l.622–624 | (AL) ⇒ `F_E^{C,opt} = F_E^{C,pess} = F_E^B` |
| P4 | §15, l.632 | "`G_0` 不依賴 `δ`，而 `G_1` 對 `δ` 非遞減，在 B 中 break-even `δ^†` 唯一；**在 C 中只有 (AL) 成立時才保證單調**"; T-SEN-8: sequence `1,1,1,1,0,0,0,1`; "C 中的建置區域是集合值" |

**Undefined in v2.2, fixed here (conventions).**
(i) *The `δ` path.* v2.2 defines `δ_jkc` cell by cell but does not define a one-parameter scan. Definition 1 does.
(ii) *Leader ties at a switch point.* v2.2 does not fix them. 51 enumerates `y = ∅` first and replaces it only if another value is strictly better (`val > best + TOL`, 51 `solve_bilevel`). That is the **strict** convention: build only if `V_1 − V_0 > 0`. We also report **tie-build**: build if `V_1 − V_0 ≥ 0`.
(iii) *Follower ties.* We use exact ties (`ε_tie = 0`). Optimistic and pessimistic selection are each reported.
(iv) *Affordability* is the weak inequality `a(x) ≤ e_u` of (R1′). 51 implements it the same way: `p["bud"] <= e_bud + TOL`.

---

## 1. Setup

**Definition 1 (reuse path).** Fix a capability `c` and an ordered parameter set `Δ ⊆ ℝ_{≥0}`. A *reuse path* is a family of instances `θ(δ)`, `δ ∈ Δ`, such that:
* (A2) for every `(j,k,s)` with `s_c = S`, the cells `C^impl_jk(s;δ)` are non-increasing in `δ`. Hence so is `a^BUD_jk(s;δ)`, by §5.1. `a^ENG_jk(s)` is non-increasing in `δ` (constant in all witnesses). Every cell with `s_c ≠ S` (`∅` or `L`) does not depend on `δ`.
* (A3) `δ` enters no other parameter. In particular it does not enter `π`, `P`, `ρ`, the path cells, `N`, `Legal`, `Allow`, `Allow^loc`, the requirement tables, `R_j(s)`, `D_j(s)`, `ē`, `I^sev`, `ΔK̄^REV`. So the sets of configurations and plans that satisfy (F2)–(F10) and (R2) do not depend on `δ`. This is the "fixed candidate set".
* (A5) `F_c`, `F^loc`, `ΔC^gov(γ)`, `Ā`, `τ` do not depend on `δ`. For Model C, `C^impl,x` does not depend on `δ` either. The follower's net cost `C^impl − C^impl,x` then moves one-for-one with `C^impl`.

T-SEN-8 uses the special case `C^impl_jk(S;δ) = max(0, base_jk − δ)` with weight 1 on every S-cell ("uniform reuse"). W5-min uses option-specific weights `w_jk ∈ {0,1}`: `C^impl(S;δ) = max(0, base − w δ)`. Both are reuse paths.

**Definition 2 (branch values, build region).** For model `M ∈ {B, C}` and, in C, mode `m ∈ {opt, pess}`, let `V^{M,m}_1(δ)` (resp. `V^{M,m}_0(δ)`) be the maximal (OBJ-E) value over all leader decisions with `y_c = 1` (resp. `y_c = 0`), including the `F_c(y_c − y^cur_c)` term. Let `D^{M,m}(δ) = V_1 − V_0`. The **build region** is

`B_c^{M,m,conv} = {δ ∈ Δ : y_c*(δ) = 1}`, with `y_c* = 1` iff `D > 0` (conv = strict) or `D ≥ 0` (conv = tie-build).

P4's `G_1 − F_c` vs `G_0` is the case `y^cur_c = 0`. With `y^cur_c = 1` the `F_c` term moves into `V_0` as a saving, and the arguments below are unchanged.

A set `S ⊆ Δ` is an **up-set** if `δ ∈ S, δ' ∈ Δ, δ' ≥ δ ⇒ δ' ∈ S`. An up-set of an interval `Δ` is an interval (`[δ^†, sup Δ]` or `(δ^†, sup Δ]`).

---

## 2. Model B is monotone in δ

**Theorem D1 (B monotone).** Under A1 (source-indexed reuse cells, 42 §10 / D8), A2, A3, A4 (centralized planner, 42 §12.6: no follower), and A5:
(a) `V^B_0(δ)` is constant on `Δ`;
(b) `V^B_1(δ)` is non-decreasing on `Δ`;
(c) hence `D^B` is non-decreasing, and `B_c^{B,strict}` and `B_c^{B,tie}` are up-sets of `Δ`.
For an interval `Δ` they are intervals, and `δ^† = inf{δ : D^B(δ) ≥ 0}` is unique, as P4 states. This holds for any number of capabilities, any `Γ`, any budget slack, and any `y^cur`.

*Proof.* (a) Take any leader–follower combination `ω = (y, y^loc, γ, q)` with `y_c = 0`. For every `j`, `s_jc ∈ {∅, L}` by §10. By A1 and A2, no cell that `ω` uses depends on `δ`. Its objective value (OBJ-E) and its resource vector do not depend on `δ` (A5 for `F_c`, `F^loc`, `ΔC^gov`). Its feasibility does not depend on `δ` either (A3 for (F2)–(F10) and (R2); (R1) uses only `δ`-free resource terms). So the set of feasible `ω` with `y_c = 0` and their values are `δ`-free, and `V^B_0` is constant.
(b) Let `δ < δ'` and let `ω` with `y_c = 1` be feasible at `δ`. Every `δ`-dependent cell that `ω` uses is an S-cell. By A2, `C^impl(·;δ') ≤ C^impl(·;δ)` and `a^h(·;δ') ≤ a^h(·;δ)` componentwise. So the left side of every (R1) row weakly falls, and `ω` is feasible at `δ'` (A3 for the rest). Its (OBJ-E) value changes only through `−Σ q C^impl`, which weakly rises. So `V^B_1(δ') ≥ F_E(ω;δ') ≥ F_E(ω;δ)`. Taking `ω` optimal at `δ` gives the claim. `k = 0` has `C^impl_j0 ≡ 0` (V2), so it is unaffected.
(c) is immediate. A non-decreasing `D` has up-set level sets `{D > 0}` and `{D ≥ 0}`. ∎

**Which assumptions the proof uses, each tested at its boundary.**

| Assumption | Used in | Boundary test / counterexample | Result |
|---|---|---|---|
| A1 source-indexed cells (D8) | (a) | **W5b boundary instance.** 2 BUs. `F_c = 5`. U1 may build a local `c` (`F^loc = 1`); U2 may not. Pooled BUD = 6 (binding). j1 (U1): `V = 10`, cost base 6. j2 (U2): `V = 6.5`, cost base 1. Under *availability indexing* `δ` also lowers j1's local-version cost, so `V_0` rises. `D(δ) = 0.5, −2.5, −4.5, 2.5, 2.5` at `δ = 0, 1, 3, 5, 6`, so B goes 1→0→0→1→1. Under *source indexing* (L-cell fixed at 6), `D = 0.5, 1.5, 1.5, 10.5, 11.5`, monotone. | **Load-bearing.** This instance is a concrete form of the Phase-F audit #3 (42 §19). |
| A2 monotone reuse path | (b) | If an S-cell *rose* with `δ` (not a reuse effect), `V_1` could fall. The claim is about reuse, so A2 is definitional. | Definitional |
| A3 fixed candidate set | (a), (b) | If the scan also moved a version-specific `P`/`ρ`/`I^sev` (42 §10 allows the shared version to differ in quality, tabulated separately), (F9) could remove `y_c = 1` plans as `δ` grows, and `V_1` could fall. v2.2 defines `δ` on `C^impl` only. Joint scans of cost and quality are **not covered** by D1. | Load-bearing; satisfied by v2.2's definition |
| A4 no follower | (b) | **W5 (Model C)**: same data, non-monotone. | Load-bearing |
| A5 `δ`-free `F_c`, `F^loc`, `ΔC^gov`, `Ā` | (a), (b) | Trivial: if `F_c` grew with `δ`, the one-for-one P4 argument would apply against monotonicity. | Definitional |
| Budget binding vs slack | — | Not used. The W5b boundary instance is budget-binding and still monotone under A1. W5 is budget-slack. | Not needed |
| Ties | (c) only | A tie at `D = 0` moves only the endpoint (open vs closed). | Convention only |
| Integer follower / Lemma E′ | — | Not used (no follower). | — |

---

## 3. Why Model C can be non-monotone: the causal chain

Fix `y` with `y_c = 1` and `γ`. Write `𝒫_u` for BU `u`'s plans that are feasible apart from the envelope. For `x ∈ 𝒫_u`, `F_u(x;δ)` is the (OBJ-U) value, `Ψ_u(x;δ)` the enterprise contribution (bracket of 42 l.462), and `a_u(x;δ)` the pooled resource vector.

**Lemma I (implementability via Lemma E′; renamed from "Lemma S" by T7 to avoid the clash with 02's Lemma S = envelope separability).** Let `≻_δ` be the follower's strict preference (`F_u` larger) and `∼_δ` indifference. Define:
* `x` is **opt-implementable at δ** iff no `p ∈ 𝒫_u` has `p ≻_δ x` and `a_u(p;δ) ≤ a_u(x;δ)`.
* `x` is **pess-implementable at δ** iff, in addition, every `p ∼_δ x` with `a_u(p;δ) ≤ a_u(x;δ)` has `Ψ_u(p;δ) ≥ Ψ_u(x;δ)`.

Then, for `m ∈ {opt, pess}`:

`V^{C,m}_1(δ) = max { Σ_u Ψ_u(x_u;δ) : x_u m-implementable at δ, Σ_u a_u(x_u;δ) ≤ b̄(y,γ) } − K(y,γ)`,

where `b̄` and `K` are as in 42 §12.5 (they do not depend on `δ`, by A5).

*Proof.* By Lemma E′ (42 §12.4) the leader loses nothing by offering `e_u = a_u(x;δ)` for some plan `x`. With `e_u = a_u(x)`, the affordable set is `{p : a_u(p) ≤ a_u(x)}`. Its optimal set contains `x` iff no affordable `p ≻ x`. The optimistic leader then obtains `max` of `Ψ` over the tie set, which is at least `Ψ(x)` and is attained by a tied affordable plan whose own envelope is no larger. The pessimistic leader obtains `Ψ(x)` exactly iff every affordable tied plan has `Ψ ≥ Ψ(x)`. In both cases, the value the leader can secure with `e_u = a_u(x)` equals `Ψ` of some m-implementable plan with resource vector `≤ a_u(x)`. Conversely, every m-implementable `x` is secured by `e_u = a_u(x)`. The knapsack (42 §12.5) then maximizes over profiles. ∎

**The chain δ → build decision.** Every arrow below is forced by the definitions. The witness rows are W5 (T-SEN-8 analog, §5).

1. **δ → local cost of shared-source configurations.** By A2, `C^impl_jk(S;δ)` falls. Through (OBJ-U) this raises `F_u` of every plan that uses those configurations, one-for-one when `C^impl,x` is `δ`-free. Through §5.1 it lowers `a^BUD`. *W5:* `C_2(δ) = max(0, 3 − δ)` for U2's k=1.
2. **Shared-capability economics.** `F_c` is sunk in the comparison of plans with `y_c = 1`. It enters `D` one-for-one but does not move with `δ` (A5). That is why `F_c^†` stays monotone in C (P4, last sentence). The `δ` effect acts only through the follower stage.
3. **→ Follower ranking and affordability order.** Two things change with `δ`. (i) The *preference order* `≻_δ`: plans with larger reuse gains rise. (ii) The *resource order* among plans: `a(p;δ) ≤ a(x;δ)` can switch from false to true when `p`'s cost falls faster than `x`'s. By Lemma I, implementability depends only on these two orders and on `Ψ` within tie classes. *W5:* U2's k=1 is strictly preferred for every `δ`. Its resource order relative to k=0 switches at `δ = 3`: `a(1) = 3 − δ > 0 = a(0)` for `δ < 3`, and `a(1) = 0 ≤ a(0)` for `δ ≥ 3`.
4. **→ Follower configuration choice.** When (3) makes a follower-preferred, enterprise-inferior plan `p` affordable inside every envelope that admits the leader's target plan `x`, `x` stops being implementable (Lemma I). The follower now picks `p` under every envelope the leader can afford to offer for `x`. *W5:* for `δ ≥ 3`, U2's k=0 is no longer implementable. Even `e_U2 = 0` admits k=1.
5. **→ Enterprise value.** `V^{C,m}_1(δ)` is a maximum over the *implementable* profiles. That set can lose its best element as `δ` grows, so `V_1` can fall even though every individual `Ψ` rises. *W5:* `V_1 − V_0 = 1 + δ` on `[0,3)`, jumps to `−1` at `δ = 3`, and then rises as `δ − 4` on `[3,5]` (U1's cost keeps falling).
6. **→ Build decision.** `y_c* = 1[D > 0]` (strict) follows `D`: `1` on `[0,3)`, `0` on `[3,4]`, and `1` again on `(4,∞)`, because U1's reuse gain eventually covers U2's unavoidable loss.

The non-monotonicity therefore needs **(i) a BU whose ledger ranks a plan above an enterprise-better plan** (misalignment), and **(ii) a δ-induced loss of envelope separability (or a preference flip)** for that BU. That is the D-chain step 3. Theorem D3 and Propositions D4–D5 make "needs" precise.

---

## 4. Does ledger alignment restore monotonicity?

**Theorem D3 (alignment ⇒ monotone build region in C) — restatement: 42 P2 applied pointwise in `(y,γ)` (label T7 per Q/11 A1).** Assume A1–A3, A5 and (AL1)–(AL4) for every BU. Then for every `δ ∈ Δ` and every `(y,γ)`, the C value at `(y,γ)` equals the B value at `(y,γ)`, in both modes:

`V^{C,opt}(y,γ;δ) = V^{C,pess}(y,γ;δ) = V^B(y,γ;δ)`.

Hence `D^{C,opt} = D^{C,pess} = D^B` is non-decreasing (Theorem D1), and `B_c^{C,m,conv} = B_c^{B,conv}` is an up-set. This holds for both modes, for any follower ties, for any cross-BU coupling through the pooled budget, and whether or not the budget binds.

*Proof.* Under (AL1), (AL2) and (AL4), `φ^u_jk = φ_jk + κ_j` for a constant `κ_j` that does not depend on `k`. The two baselines `N g^u_j0` and `N g_j0(ȳ^cur)` may differ only by a `j`-constant.¹ Since (F1) picks exactly one `k` per `j`, `F_u(x) = Ψ_u(x) + Σ_{j∈J_u} κ_j` on `𝒫_u`. Under (AL3), the unit's plan set equals B's plan set for unit `u`. So for any envelope `e_u` every follower optimum maximizes `Ψ_u` over `{x : a_u(x) ≤ e_u}`, and all of them have the same `Ψ_u`. Optimistic and pessimistic values coincide, and `φ_u(e_u) = max{Ψ_u(x) : a_u(x) ≤ e_u}`. The leader's problem at `(y,γ)` becomes `max_{Σ e_u ≤ b̄} Σ_u max_{a_u(x_u) ≤ e_u} Ψ_u(x_u) − K`. This is `max{Σ Ψ_u(x_u) : Σ a_u(x_u) ≤ b̄} − K` (take `e_u = a_u(x_u)` in one direction; use `a_u(x_u) ≤ e_u` in the other). That is B's value at `(y,γ)`, 42 §12.6. This is P2's argument applied at each fixed `(y,γ)` instead of only at B's optimum. Maximizing over `y_c ∈ {0,1}` separately gives `V^C_i = V^B_i`, and Theorem D1 applies. ∎

**What else is needed — nothing, under full alignment.**
* *Ties.* Irrelevant: all follower optima have equal `Ψ`.
* *Coupling across BUs.* Irrelevant: the knapsack's feasible envelope space `{e : Σ e_u ≤ b̄}` is `δ`-free. Note that the *candidate* set `E′_u(δ)` moves with `δ`, so monotonicity must be argued on the full envelope space, as done here, not on `E′_u`.
* *Budget.* Irrelevant.

¹ *Footnote (T7 per Q/11 §2.6).* This step relies on 42's own P2 assertion `φ^u = φ` under (AL). 42 leaves the argument of `g^u_j0` unstated; we fix it at `ȳ^cur` (the status-quo capability state), so the baseline is plan-constant. If `g^u_j0` were evaluated at `ȳ`, which includes the follower's own `y^loc`, the baseline would not be plan-constant and D3 would need an additional hypothesis. This inherits 42's ambiguity rather than creating a new error.

**Alignment is sufficient, not necessary.** Two weaker sufficient conditions:

**Proposition D4 (partial alignment).** Assume A1–A3, A5. Suppose every BU `u` that has some `δ`-dependent cell (i.e. some `j ∈ J_u`, `k`, with `c ∈ Rel(j)` and `C^impl_jk(S;·)` non-constant) satisfies (AL1)–(AL4) for its own initiatives. Misaligned BUs may exist, but their cells are `δ`-free. Then `V^{C,m}_1` is non-decreasing for both `m`, and `V^{C,m}_0` is constant. So the build region is an up-set.

*Proof.* Take the leader's problem at `(y,γ)` over the full envelope space. For a `δ`-free BU, `φ^m_u(e;δ)` does not depend on `δ` for any `e`. For an aligned BU, `φ_u(e;δ) = max{Ψ_u(x;δ) : a_u(x;δ) ≤ e}`, which is non-decreasing in `δ` for every fixed `e`: by A2 the affordable set grows and each `Ψ` rises. The objective `Σ_u φ_u(e_u;δ)` is pointwise non-decreasing over a `δ`-free feasible set, so its maximum is non-decreasing. `V_0` is constant by (a) of D1, which needs no follower argument because no S-cell exists when `y_c = 0`. ∎

**Proposition D5 (δ-invariant separability).** Assume A1–A3, A5. Suppose that for every BU `u` and all `δ ∈ Δ`: (i) the preference relation `≻_δ` and the indifference relation `∼_δ` on `𝒫_u` do not depend on `δ`; (ii) the componentwise resource order `{(p,x) : a_u(p;δ) ≤ a_u(x;δ)}` does not depend on `δ`; (iii) for `m = pess` only, the `Ψ`-order inside each indifference class does not depend on `δ`. (iii) holds trivially when there are no follower ties. Then `V^{C,m}_1` is non-decreasing.

*Proof.* By Lemma I, implementability depends only on `≻`, `∼`, the resource order and (for pess) the `Ψ`-order inside tie classes. All of these are `δ`-invariant, so the m-implementable set of each BU is `δ`-invariant. Each `Ψ_u(x;δ)` is non-decreasing (A2). Each resource vector is non-increasing, so a profile that is budget-feasible at `δ` stays feasible at `δ' > δ`. The maximum over a fixed set of non-decreasing functions under a weakly relaxing constraint is non-decreasing. ∎

W5 violates D5(ii) at `δ = 3` (`a(1) ≤ a(0)` becomes true). W5-min violates D5(ii) at `δ = 4` (`C_b ≤ C_a` becomes true). Both violate D4 because the misaligned BU's own cell moves with `δ`. If W5 is modified so that U2's reuse weight is 0, D4 applies and the region becomes the up-set `[0,∞)`. Within the scope of D4/D5, therefore, misalignment needs a reuse effect *on the misaligned BU* to produce non-monotonicity.

---

## 5. Minimal counterexamples: build → no build → build

### 5.1 W5 — T-SEN-8 analog (2 BUs × 1 initiative × 2 options, uniform reuse)

Data (SIMULATED_ONLY; same numbers as 51 `hand_instance(None, 2.5, delta, u1_base=5, u2_base=3)` with `F_c = 24`):
* One capability `c`; `y^cur = ∅`; `F_c = 24`; pooled BUD `= 100`; ENG use 0 everywhere; no local versions (`Allow^loc = 0`); `Pre(j,1) = {c}`.
* U1 (aligned): `N = 10`, `v_u = 3`, `l_x = 0`. So `Ψ_U1(1) = F_U1(1) = 30 − C_1(δ)`, with `C_1(δ) = max(0, 5 − δ)` (S-cell).
* U2 (misaligned, (AL1) fails): `N = 10`, `v_u = 2`, `l_x = 2.5`. So `F_U2(1) = 20 − C_2(δ)` and `Ψ_U2(1) = −5 − C_2(δ)`, with `C_2(δ) = max(0, 3 − δ)`.
* k=0: all values and costs 0. `V_0 ≡ 0`: with `y_c = 0` every k=1 violates (F4).

Computation (by hand, re-checked by the witness):
* Both followers strictly prefer k=1 at every `δ` (`30 − C_1 > 0`, `20 − C_2 > 0`). **No follower ties anywhere, so opt = pess.**
* `E′_U2 = {0, C_2(δ)}`. With `e_U2 = 0`, U2 can afford k=1 iff `C_2(δ) ≤ 0` iff `δ ≥ 3`.
* `δ < 3`: the leader blocks U2 (`e_U2 = 0`) and admits U1. `D(δ) = 30 − (5 − δ) − 24 = 1 + δ > 0`.
* `3 ≤ δ ≤ 5`: U2 is unblockable, and its loss `−5` is unavoidable once `c` is built. Admitting U1 is still best. `D(δ) = 30 − (5 − δ) − 5 − 24 = δ − 4`. This is negative on `[3,4)`, zero at `4`, and positive on `(4,5]`.
* `δ ≥ 5`: `D = 1`.

| δ | 0 | 1 | 2 | 2.9 | 3 | 3.5 | 4 | 5 |
|---|---|---|---|---|---|---|---|---|
| `D^{C,pess} = D^{C,opt}` | 1 | 2 | 3 | 3.9 | −1 | −0.5 | 0 | 1 |
| `y_c*` strict (51 convention) | 1 | 1 | 1 | 1 | 0 | 0 | **0** | 1 |
| `y_c*` tie-build | 1 | 1 | 1 | 1 | 0 | 0 | **1** | 1 |
| `D^B` (W5b) | 1 | 2 | 3 | 3.9 | 4 | 4.5 | 5 | 6 |

**Continuous build regions:** `B_c^{C,m,strict} = [0,3) ∪ (4,∞)` and `B_c^{C,m,tie} = [0,3) ∪ [4,∞)` for `m ∈ {opt, pess}`. `B_c^B = [0,∞)`.

### 5.2 W5-min — single follower (1 BU × 1 initiative × 3 options, option-specific reuse)

Options `{0, a, b}`, all with `Pre = {c}`. `a`: `W = V = 10`, `C_a = 2` (no reuse effect). `b`: `W = 20`, `V = 6`, `C_b(δ) = max(0, 6 − δ)`. `F_c = 5`, BUD = 100.
* `δ < 4`: `C_b > C_a`, so `e = 2` admits `{0, a}` only. The follower picks `a` (`8 > 0`). `D = 10 − 2 − 5 = 3`.
* `δ ≥ 4`: `C_b ≤ 2`, so every envelope that admits `a` also admits `b`, and the follower prefers `b` (`20 − C_b ≥ 18 > 8`). The leader can implement only `b` (`Ψ_b = 6 − C_b(δ)`) or k=0 (`e = 0`, `Ψ = 0`). So `D = max(6 − C_b(δ), 0) − 5`. That is `δ − 5` on `[4,6]` and `1` for `δ ≥ 6`.
* Region (strict): `[0,4) ∪ (5,∞)`. Witness sequence on `{0, 2, 3.9, 4, 5, 5.5, 6, 7}`: `1,1,1,0,0,1,1,1` (tie at 5).

### 5.3 Minimality

**Lemma M (one follower with two options cannot produce 1→0→1).** Take Model C, either mode and either convention. Suppose there is a single BU with a single initiative, `K = {0, a}`, `c ∈ Pre(a)`, no local version, `y^cur_c = 0`, `F_c > 0`, a reuse path satisfying A1–A3, A5, and `a_u(a;δ) ≥ 0` componentwise. Suppose also that the capability has **no status-quo effect**: `ρ(·|0,z,ℓ,ȳ)` does not depend on `ȳ`, so `φ_j0 ≡ 0` (42 §7.3). Then `B_c^{C,m,conv}` is an up-set.

*Proof.* `V_0 = 0`, because only k=0 is feasible when `y_c = 0` and `φ_j0 = 0`. With `y_c = 1`, Lemma I gives the following. k=0 is implementable iff `a_u(a;δ) ≰ 0` or `a ⊁_δ 0`. Both are down-sets in `δ`: `a_u(a;·)` is non-increasing, and `F_u(a;·)` is non-decreasing. `a` is implementable iff `a ⪰_δ 0` (with the pessimistic tie qualifier); this is an up-set. Implementing k=0 gives `V_1 = −F_c < 0 = V_0`. So `y_c* = 1` iff `a` is implementable and `Ψ(a;δ) − F_c > 0` (resp. `≥ 0`). Implementability of `a` is an up-set, and `Ψ(a;δ)` is non-decreasing (A2). The intersection of two up-sets is an up-set. ∎

*The no-status-quo-effect hypothesis is needed.* If `c` raises the status quo's own value (`κ_0 := φ_j0(ȳ with c) − F_c > 0`, e.g. a change capability that improves current checking behaviour, 42 §6), then the build region contains the down-set where k=0 is implementable. It can therefore be the union of a down-set and an up-set, which is not an interval in general. This variant was not constructed in a witness.

So, **under Lemma M's hypotheses** (`a_u(a;δ) ≥ 0` componentwise and no status-quo effect of `c`), a 1→0→1 pattern needs **either** ≥ 3 options in one follower (W5-min, which uses option-specific reuse) **or** ≥ 2 follower decision units: 2 BUs as in W5, or 2 initiatives in one BU. The bounded search in the witness agrees: 0 of 288 two-option instances.

**Conjecture M2 (NOT_PROVEN).** With *uniform* reuse (`C^impl(S;δ) = max(0, base − δ)` on every S-cell) and one follower with one initiative, a 1→0→1 pattern needs ≥ 2 follower decision units (any `|K|`). *Outline for `|K| = 3`:* with uniform clipped costs, `C_b − C_a` is monotone in `δ`. So the resource order between `a` and `b` switches at most once, and the switch happens only when the cheaper base reaches 0. After that, all costs are 0 and nothing changes. A complete case analysis for general `|K|`, ties and multi-resource envelopes has not been written. *Support (not proof):* 0 of 6,912 bounded-search instances for `|K| = 3` (`W, V, base` on small integer grids, `δ ∈ {0, 0.5, …, 8}`). With option-specific weights `w ∈ {0,1}`, the same search finds 24 instances.

---

## 6. Build region: the non-interval proposition

**Proposition D6 (existence; under ledger misalignment the build region need not be an interval).** There exist finite instances of v2.2 Model C that satisfy all of: A1–A3, A5; a single capability; a single binding-free pooled resource; identified follower ledgers; no follower ties at any `δ`; and exactly one assumption of Theorem D3 violated, namely (AL1) for one BU. For these instances, `B_c^{C,m,conv}` is **not an interval** for both modes `m ∈ {opt, pess}` and both conventions `conv ∈ {strict, tie-build}`. On the same instance, `B_c^B` is an interval (Theorem D1).

*Proof.* The W5 instance (§5.1): `B_c^{C,m,strict} = [0,3) ∪ (4,∞)` and `B_c^{C,m,tie} = [0,3) ∪ [4,∞)`. `3.5` lies between `2.9` and `5`, both in the region, but `3.5` is not in it. Opt = pess because every follower optimum is unique. ∎

**What the proposition does not say.** It does not say that misaligned C instances are generically non-monotone. Theorem D3 and Propositions D4–D5 identify broad classes where the region is an interval. Misalignment with envelope separability preserved (42 P2 remark; D5) gives monotone regions. The proposition is an existence claim only.

**Modelling caveat: every-resource footprint condition (T7 per Q/11 A6).** In W5 (and W5_WIDE) the non-monotonicity requires that reuse drives the misaligned unit's AI configuration to a pooled-resource footprint `≤` that of an enterprise-preferred plan (here the status quo) **in every pooled resource, including ENG**. In the W5/W5_WIDE family, any strictly positive ENG footprint, or any strictly positive floor on the AI configuration's **net** BUD footprint (reused cost plus incremental opex) relative to the status quo, makes the envelope separate for every `δ`, and the region is an interval [T8-fix] (W5_WIDE `knife_edge_components`: ENG footprint `1e−6` → 1 component; cost floor `0.01` → 1 component; floor `0.5` with incremental opex `−1`, allowed by 42 §5.1/D9, restores the non-interval region). This condition is implicit in Lemma I but was not stated as a hypothesis before.

**Fragile margins of W5 and the wide-margin supplement W5_WIDE.** Prop D6 claims existence only and stays correct. But the canonical W5 (kept unchanged, because it must reproduce T-SEN-8's grid exactly) has margins of 1 TWD (`D(0) = 1`, `D(3) = −1`, `D(≥5) = 1`) against `F_c = 24` and `N_1 v_1 = 30`. In the deterministic check of W5_WIDE (400 joint multiplicative perturbations of all 8 scalars per radius, private seed 20261015, region scanned on `δ ∈ {0, 0.05, …, 12}`), W5 keeps a non-interval region in **398/400** draws at ±1 % but only **162/400** at ±5 %. The supplementary witness **W5_WIDE** (`N1=10, v1=3, b1=10, N2=10, v2=2, l_x=3, b2=4, F_c=17`; red-team instance) gives `D = 3 + δ` on `[0,4)`, `δ − 7` on `[4,10]`, `3` after, so the region is **`[0,4) ∪ (7,∞)`** (strict; `[0,4) ∪ [7,∞)` tie-build) in both modes, with margins of 3; it keeps a non-interval region in **367/400** draws at ±5 % and **256/400** at ±10 %. These counts are a synthetic regression on a fixed seed, not a proof of robustness. W5_WIDE widens the numeric margins only: it depends on the **same two exact zeros** as W5 (net BUD footprint reaching ≤ the status quo's — a zero reused-cost floor in W5/W5_WIDE, or a positive floor offset by negative incremental opex — and zero ENG footprint) [T8-fix]. If W5 is used in the manuscript to support H-DL4 or "platform coupling" as a practically relevant phenomenon, the every-resource footprint condition must be stated with it.

**Tie handling at switch points (W5).**
* `δ = 3` is a *resource-order* switch. With the weak affordability inequality of (R1′), `δ = 3` is already unblockable, so the left piece is `[0,3)`, right-open. Under a strict-affordability convention (not v2.2's), it would be `[0,3]`. Either way, the region is not an interval.
* `δ = 4` is a *leader* tie (`D = 0`). The strict convention (51) excludes `4`; tie-build includes it.
* There are no follower ties. If a follower tie occurred at a switch point, `D^{C,opt} ≥ D^{C,pess}` pointwise on the `y_c = 1` side. In W5, `V_0` has no follower choice, so `B^{pess} ⊆ B^{opt}`. In general there is no inclusion, because `V_0^{pess}` may also be below `V_0^{opt}`.

**Reconciliation with 51 T-SEN-8 (read-only).** 51 scans `δ ∈ {0, 1, 2, 2.9, 3, 3.5, 4, 5}` with `hand_instance(None, 2.5, δ, u1_base=5, u2_base=3)`, `F_c = 24`, and reports the C-pess sequence `1,1,1,1,0,0,0,1` and the "set-valued build region `[0.0, 1.0, 2.0, 2.9, 5.0]`" (baseline stdout l.18). The witness reproduces this exactly. In 51's fixture, the `∅`-state cell carries the same reduced cost as the S-cell. This is harmless because k=1 requires `c` and no local version exists, so the `∅`-cell is never used. 42 P4 states the region as "`{0,1,2,2.9} ∪ {5}`", which is the grid trace. The continuous region and the explicit conventions are added here. `F^C_pess` falls between consecutive grid points (`3.9 → 0` at `δ: 2.9 → 3`), which matches T-SEN-8's assertion that the leader value falls as reuse improves. Here "value" means `max(V_0, V_1)`.

---

## 7. Relation to P1–P8, Lemma E′, and consistency with v2.2

* **P1:** `F^C ≤ F^B` at every `δ`. In W5, `DL(δ) = F^B − F^{C,pess}` takes the values `0, 0, 0, 0, 4, 4.5, 5, 5` on the grid. DL is non-monotone in reuse and jumps from 0 to 4 at the separability switch. This is consistent with 42 P2's remark that misalignment yields `DL > 0` only when "envelope 無法分離它".
* **P2:** Theorem D3 is P2 applied at each fixed `(y,γ)`.
* **P4:** confirmed and sharpened. `F_c^†` stays a monotone threshold in C, because `F_c` enters neither the follower ledger nor the resource order among plans. `δ^†` is unique in B (Thm D1) and in C under (AL) (Thm D3), D4 or D5. It is set-valued otherwise (D6).
* **P7/P8:** W5 is a P8-type situation. A policy that forbids U2's k=1, or a requirement that U2's k=1 fails while U1's passes, would screen out the unblockable plan and restore `F^C = F^B`. Governance screening and reuse non-monotonicity are the same envelope-separability failure (cf. 03 and 02 of this pack).
* **Lemma E′:** used in Lemma I. Monotonicity arguments must be made on the full envelope space, because `E′_u(δ)` moves with `δ`.
* **No contradiction with v2.2:** every statement above either reproduces a v2.2 claim (P4 in B; P4's C caveat; T-SEN-8) or makes one precise (unspecified conventions; sufficient conditions in place of "only (AL) guarantees").

## 8. Literature positioning

| Claim | Type | Anchor (reference list of 59a only) |
|---|---|---|
| Sequential leader–follower decisions can be represented as a bilevel problem; optimistic vs pessimistic bounds must be distinguished | TYPE B | Colson et al. (2007); Dempe (2002); Wiesemann et al. (2013) |
| Theorem D1 (B monotone; makes 42 P4's B part explicit), Theorem D3 (restatement: P2 pointwise in `(y,γ)`) | **Restatement-level** | 42 P2, P4 |
| Lemma I, Props D4–D6, Lemma M, W5_WIDE | **TYPE C (in-model; known type of phenomenon — TO VERIFY):** "more options can hurt the principal" / Braess-type paradoxes in Stackelberg games; monotone comparative statics (Topkis; Milgrom & Shannon). New here: the specific reuse → loss-of-envelope-separability chain, D4/D5 (monotonicity without full alignment, correcting 42 P4's "只有 (AL)"), Lemma M | — (elementary monotonicity arguments) |
| General monotone comparative statics (Topkis; Milgrom & Shannon) | — | **[NOT IN REFERENCE LIST — TO VERIFY; do not cite until added]**. Not needed: D1 is proved directly. |
| Centralization need not dominate in reality (information) | TYPE B boundary | Alonso et al. (2008). The non-monotonicity here arises **within** the complete-information model (P3) and does not rely on information effects. |

**AI-specificity (T7 per Q/11 A11).** D1–D6 and Lemma M use only shared capabilities with source-indexed costs, pooled resources, two ledgers and finite plan sets. They hold verbatim for any shared-platform IT portfolio (e.g. a shared data platform or ERP module reused by several units). Reuse non-monotonicity is a property of the enterprise–BU architecture, not an AI-specific result; the AI-specific content of the thesis is the M1–M4 schema, the autonomy-keyed requirement tables and the response layer `ρ`.

**Restatement of v2.2 vs genuinely new (TYPE C), consistent with Q/11 §3 item 3** (T7):
* *Restatement / explicit form of v2.2:* D1 (42 P4, B part, with assumptions made explicit), D3 (42 P2 pointwise in `(y,γ)`), Lemma I (Lemma E′ read as an implementability condition).
* *Genuinely new in-model:* D4 and D5 (monotonicity without full alignment; corrects 42 P4's "只有 (AL)"), the D6 existence result with explicit continuous regions and conventions, the wide-margin witness W5_WIDE together with the every-resource footprint caveat, Lemma M, and the W5b demonstration that source indexing (A1) is load-bearing.

## 9. NOT PROVEN / open

* Conjecture M2 (uniform reuse requires ≥ 2 follower decision units): proof outline and bounded search only.
* Joint scans in which the shared version's quality (`P`, `ρ`, `I^sev`) moves together with `δ`: outside D1, no result.
* Non-zero `ε_tie` (relative tolerance): all statements use exact ties. With a tolerance, endpoints can shift by `O(ε_tie)`, and the region's non-interval property in W5 is unaffected (gap width 1). Lemma I's proof uses Lemma E′; under a tolerant tie rule its pessimistic step needs the same `F_u`-maximal selection as 02 §2.2 (Q/13). Lemma I under tolerance is not re-proved here (exact ties only).

## 10. Integration note (manuscript 59a)

* Section 3.12/P4 paragraph: replace "只有 (AL) 成立時才保證單調" with Theorem D3 plus Props D4/D5 (sufficient conditions). State Prop D6 as an existence result with the explicit continuous region and conventions.
* Section 5.6: interpret the chain in §3 as "reuse can destroy envelope separability". That is the managerial reading. Pair it with P8 screening.
* Appendix C: proofs of D1, Lemma I, D3, D6 and Lemma M. W5/W5b/W5_WIDE as constructive examples (SIMULATED_ONLY), with the every-resource footprint caveat and W5's fragile margins (§6).
