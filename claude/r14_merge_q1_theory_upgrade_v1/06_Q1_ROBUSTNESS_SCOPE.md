# 06 — Scope of vertex exactness: Lemma R, element-level classification, and Model C (Task F, theory agent T2)

**Status:** Q1 theory-upgrade candidate, 2026-10-14. Additive to canonical v2.2. 42 and 51 were read only.
**Evidence class:** Theorem R1 restates Lemma R with explicit hypotheses and a complete proof. Propositions R2–R5 and Corollaries R1a–R1b also have complete proofs (TYPE C). The counterexamples are constructive examples with hand algebra, re-checked by `witness_parts/w_mono_rob_miss.py::witness_W7`. All numbers are SIMULATED_ONLY.

**Verdict lines**

```
LEMMA_R_WHOLE_PORTFOLIO_B          = RESTATEMENT: Thm R1 = 42 Lemma R with explicit hypotheses (R-a)..(R-e) (proof complete); also MaxRegret (Cor R1a = 42 §13.2) and the lambda-box certificate (Cor R1b = 42 §7.4 (iii))
ELEMENT_LEVEL_VERTEX_EXACT         = NO in general (Prop R3; minimal counterexample = T-SEN-3 instance, 3 portfolios x 1 block, minimality proved)
ELEMENT_LEVEL_EXACT_SPECIAL_CASE   = YES when exactly one robustly feasible candidate contains the element value (Prop R4)
ELEMENT_LEVEL_EXACT_CHARACTERIZATION= covering condition (Prop R2): robust iff the optimality regions of portfolios containing d0 cover Theta_g
MODEL_C_VERTEX_EXACT               = NO, even for a fixed leader decision (Prop R5; W7b aligned = continuous convex, W7c misaligned = discontinuous)
SCOPE_SENTENCE                     = §5 (valid for B/A+ whole portfolios, MaxRegret, lambda box; not for elements, C/C0/A, dependent Theta, theta-varying candidate sets)
T-SEN-3 reconciliation             = EXACT (vertex-only ROBUST, interior FRAGILE on (0.4,0.6); ScopeError semantics match Prop R3/R5)
```

---

## 0. Exact v2.2 sources relied on

| Item | 42 location | Content |
|---|---|---|
| Block-multilinearity | §6, l.253 | "(X1) 對 `π`、`P`、每一列 `ρ`、以及 `f` 各自為線性；整體為 **block-multilinear**。§13 的穩健性精確檢查依賴此性質。" |
| `Θ_g` form | §13.1, l.514–520 | product of intervals for monetary/quantity parameters; each probability row = "單純形 ∩ 區間盒" polytope; "預先登記的相依限制" allowed |
| Registry validation | §13.1 (i), l.522 | each block within one factor class; two blocks of a group may not touch the same cell; "所有頂點論證 … 所需的 block-multilinear 前提的**可檢查**版本" |
| Classes | §13.2, l.528–535 | ROBUST/CONDITIONAL/FRAGILE/UNIDENTIFIED for a decision element `d` (`y_c`, `q_j`, `e_u`, `γ`, or the whole portfolio); MaxRegret vertex-exact in B for a fixed candidate set |
| Lemma R | §13.3, l.541 | "對兩個固定的 portfolio `d, d'`，`Δ(θ) = F_E(d;θ) − F_E(d';θ)` … block-multilinear … 若 `Θ_g` 是各區塊多面體的乘積，則 `min Δ` 在乘積的某個頂點達成" |
| Scope limits | §13.3 items 1–3, l.545–547 | element level not exact (counterexample `θ`, `1−θ`, `0.6`); "Model C 不適用"; dependent constraints → sampling |
| Candidate set | §13.3, l.549–560 | only ROBUSTLY_FEASIBLE portfolios enter; four feasibility classes |
| λ certificate | §7.4 (iii), l.304 | B/A+: affine in `λ`, feasibility `λ`-free ⇒ "在 2^m 個頂點皆最適 ⇒ 在整個盒上最適"; C/C0: pessimistic value concave in `λ`, grid only, `ROBUST_ON_GRID`, no point decision |
| 51 guard | `lemma_r_check` | raises `ScopeError` unless `model == "B"` and `scope == "whole_portfolio"` |

---

## 1. Whole-portfolio exactness: precise domain of Lemma R

**Notation.** A *whole portfolio* `d = (y, y^loc, γ, q)` fixes every leader and follower variable. `F(d;θ)` is (OBJ-E) evaluated at `θ`. A group `Θ_g` has blocks `b = 1..B`. `θ_b ∈ P_b`, where `P_b` is a polytope with finite vertex set `vert(P_b)`.

**Hypotheses.**
* **(R-a) Model / decision object.** The decision being certified is a whole portfolio, and its value is a fixed formula in `θ`. No optimization inside the evaluation depends on `θ`. This covers Model B and A+ (42 §12.6). It excludes C, C0 and A, where the follower's plan is `argmax F_u(·;θ)` (42 §12.3, 12.7).
* **(R-b) Objective structure.** For each `d`, `θ ↦ F(d;θ)` is affine in `θ_b` when the other blocks are held fixed, for every `b`. By (X1) and (V1)–(V2) this holds when (i) each block contains cells of one factor class (`N`, path cells `v/l/c/t`, `P`, `π`, one `ρ` row family, `λ`, `C^impl`, `F_c`, `ΔC^gov`, …), and (ii) no two blocks share a cell. This is 42 §13.1 (i) and 51 `validate_registry`. A block holding two factors that multiply in (X1)/(V2) (e.g. `N_jk` and `P_jk`, or `λ_ℓ` and `t`) would make `F` quadratic in that block and break (R-b).
* **(R-c) Uncertainty set.** `Θ_g = ∏_b P_b` is a Cartesian product of polytopes, with no cross-block dependence constraints. A two-distribution mixture `θ_b ∈ [0,1]` is the segment polytope whose vertices are the two distributions. Any vertex enumeration must return *all* vertices of each `P_b`.
* **(R-d) Fixed candidate set.** The competitor set `𝒟_g` consists of portfolios that are feasible for every `θ ∈ Θ_g` (ROBUSTLY_FEASIBLE, 42 §13.3). Constraints that depend on `θ` — (F9), (R2), and (R1) through `a^BUD ∋ N E[c]` — must not remove a competitor at some `θ`.
* **(R-e) Optimality notion.** "`d` optimal at `θ`" means `F(d;θ) ≥ F(d';θ)` for all `d' ∈ 𝒟_g` (weak; ties allowed). A tolerance `ε` shifts the test to `≥ −ε` and does not affect the argument.

**Theorem R1 (Lemma R, precise form) — restatement of 42 Lemma R with explicit hypotheses (label T7 per Q/11 A1).** Under (R-a)–(R-e), and for `d ∈ 𝒟_g`:
`d` is optimal for every `θ ∈ Θ_g` ⇔ `F(d;θ) − F(d';θ) ≥ 0` for every `d' ∈ 𝒟_g` and every `θ ∈ ∏_b vert(P_b)`.

*Proof.* (⇒) is trivial. (⇐) Fix `d'` and write `Δ(θ) = F(d;θ) − F(d';θ)`. By (R-b), `Δ` is affine in each block, so it is continuous, and `Θ_g` is compact, so a minimizer `θ*` exists. Replace `θ*_1` by a vertex of `P_1`: an affine function on a polytope attains its minimum at a vertex, so the value does not rise. Do the same for blocks `2..B` in turn, holding the already-replaced blocks fixed. The result `θ^v ∈ ∏ vert(P_b)` has `Δ(θ^v) ≤ Δ(θ*) = min Δ`. So `min Δ` is attained at a vertex profile, and non-negativity at all vertex profiles gives non-negativity everywhere. (R-d) guarantees that the competitor set over which `d` must be optimal is the same at every `θ`. ∎

**Corollary R1a (MaxRegret).** Under (R-a)–(R-d), `MaxRegret(d) = max_θ max_{d'} [F(d';θ) − F(d;θ)]` is attained at a vertex profile. *Proof.* Each `F(d') − F(d)` is affine per block. The maximum of affine functions is convex per block, and a function convex in each block separately attains its maximum over `∏ P_b` at a vertex profile (same block-by-block replacement, now with maxima). ∎ This is 42 §13.2, made explicit.

**Corollary R1b (λ box).** With `Θ = ∏_ℓ [0, λ^U_ℓ]`, (OBJ-E) is affine in `λ` and feasibility does not depend on `λ` (42 §7.4 (iii)). So "optimal at all `2^m` vertices ⇒ optimal on the box" for B and A+. This is Theorem R1 with interval blocks.

---

## 2. Element level: why vertex checks fail

**Definition.** Let `d°` be a value of a decision element (e.g. `y_c = 1`). Let `𝒟^1 = {d ∈ 𝒟_g : d ∋ d°}` and `𝒟^0 = 𝒟_g ∖ 𝒟^1`. Define

`h(θ) = max_{d∈𝒟^1} F(d;θ) − max_{d∈𝒟_g} F(d;θ) = min{0, M_1(θ) − M_0(θ)}`, with `M_i = max_{𝒟^i} F`.

`d°` is optimal at `θ` iff `h(θ) = 0` iff `M_1(θ) ≥ M_0(θ)`.

**Why `h` is not multilinear.** `M_1` and `M_0` are pointwise maxima of block-affine functions, so each is block-convex and piecewise affine. Their kinks lie on the switching surfaces `{F(d) = F(d')}`, which are generally not at vertices. `M_1 − M_0` is a *difference* of block-convex functions. It has neither the minimum-at-vertex property (that needs block-concavity) nor the maximum-at-vertex property. The element indicator `1[M_1 ≥ M_0]` is a max/min composition of multilinear functions, not a multilinear function. That is the precise reason the 42 §13.3 item 1 formula "`min_θ [max_{d∋d°} F − max_d F] ≥ 0`" escapes Theorem R1.

**Proposition R2 (exact characterization: covering).** Let `Θ(d) = {θ ∈ Θ_g : d optimal at θ}`. Each `Θ(d)` is closed. `d°` is optimal on all of `Θ_g` iff `∪_{d∈𝒟^1} Θ(d) = Θ_g`. *Proof:* immediate from the definition of `h`. Checking this cover requires the arrangement of switching surfaces, not only vertices. ∎

**Proposition R3 (vertex test is not exact at element level; minimal counterexample).** There is an instance satisfying (R-a)–(R-e) in which `d°` is optimal at every vertex of `Θ_g` but not on all of `Θ_g`. The smallest such instance has 3 portfolios and 1 one-dimensional block.

*Proof (existence).* This is the T-SEN-3 / 42 §13.3 instance; see Appendix A.
*Proof (minimality).* If `|𝒟^1| = 1`, Prop R4 below makes the vertex test exact. If `|𝒟^0| = 0`, `d°` is trivially robust. So a counterexample needs `|𝒟^1| ≥ 2` and `|𝒟^0| ≥ 1`, i.e. at least 3 portfolios. One one-dimensional block suffices, so the instance is minimal in both counts. ∎

**Proposition R4 (an exact special case).** If `𝒟^1 = {d_1}`, then `d°` is optimal on `Θ_g` iff `F(d_1;θ) − F(d;θ) ≥ 0` for all `d ∈ 𝒟^0` and all vertex profiles `θ`. *Proof.* `M_1 − M_0 = min_{d∈𝒟^0} [F(d_1) − F(d)]` is a minimum of block-affine functions. Exchanging the two minima, `min_θ min_d = min_d min_θ`, and each inner minimum is attained at a vertex profile (Theorem R1). ∎
42 §13.3 (a) is the corresponding *sufficient* condition: some single `d ∈ 𝒟^1` is Lemma-R certified. R4 adds that, when `𝒟^1` is a singleton, the same test is also necessary.

---

## 3. Model C: why vertex exactness fails even for a fixed leader decision

In Model C a leader decision `b = (y, γ, e)` does not fix the portfolio. Its value is

`V^m(b;θ) = Σ_u sel^m_{x ∈ X*_u(b;θ)} Ψ_u(x;θ) − K(b;θ)`, with `sel^opt = max` and `sel^pess = min`,

where `X*_u(b;θ) = argmax_{a_u(x;θ) ≤ e_u, x ∈ X_u(θ)} F_u(x;θ)`. Even when every `F_u(x;·)` and `Ψ_u(x;·)` is block-affine (R-b holds plan by plan), `V^m(b;·)` is a *selection* of the `Ψ_u(x;·)` driven by the follower's argmax regions.

**Proposition R5.** Assume (R-b)–(R-e) for all plan-level quantities.
(i) Under (AL) **and θ-independent resource vectors** (`a_u(x;θ) ≡ a_u(x)`, so the affordable set does not switch with `θ`), `V(b;θ) = Σ_u max_{x affordable} Ψ_u(x;θ) − K`. This is block-convex in `θ` and continuous. *(Qualifier added T7 per Q/11 §2.12: affordability `a_u(x;θ) ≤ e_u` depends on `θ` in general, because `a^BUD ∋ N·E[c]` (42 §5.1); then the affordable set switches with `θ` and the maximum need not be block-convex — that case falls under (iii). The counterexample W7b is unaffected: its costs are zero.)* A leader decision is then structurally an *element* (Section 2), and the vertex test is not exact.
(ii) Without (AL), `V^m(b;·)` is in general piecewise block-affine and **discontinuous** on the follower's switching surfaces. Where the follower is indifferent, `V^pess` takes the lower and `V^opt` the upper limit. Neither the minimum nor the maximum of `V(b) − V(b')` need be at a vertex.
(iii) `θ`-dependent follower feasibility (F9, R2 inside `X_u(θ)`) adds further switching surfaces.
In each case there are instances where some `b` is optimal at every vertex profile but not on `Θ_g`.

*Proof.* (i) is the alignment argument of 04 Thm D3 applied pointwise in `θ`. The block-convexity of a maximum of block-affine functions is standard. Counterexample (aligned, W7b): one block `θ ∈ [0,1]`. Leader options: build (`F_c = 0.6`) or not (value 0). With `c`, the aligned follower chooses between `a` (`Ψ = F_u = θ`) and `b` (`1 − θ`). `V(build) = max(θ, 1 − θ) − 0.6 = 0.4` at both vertices, but `−0.1` at `θ = 0.5`. Build fails exactly on `(0.4, 0.6)`.
(ii) Counterexample (misaligned, W7c). Options `a`, `m`, `b` all need `c` and cost 0, so no envelope separates them. Follower ledger: `u_a = 1 − θ`, `u_m = 0.6`, `u_b = θ`. Enterprise: `Ψ_a = Ψ_b = 1`, `Ψ_m = 0`. `F_c = 0.5`. The follower picks `a` on `[0, 0.4)`, `m` on `(0.4, 0.6)`, and `b` on `(0.6, 1]`. So `V(build) = 0.5, −0.5, 0.5` on these pieces. It jumps at `0.4` and `0.6`. At the ties, `V^opt = 0.5` and `V^pess = −0.5`. Build is optimal at both vertices (`0.5 > 0`) and not on `(0.4, 0.6)` (closed at the tie points for pess).
(iii) Follows from (ii) with feasibility switching in place of preference switching. ∎

This matches 42 §13.3 item 2 ("Leader 的價值經由部門最佳回應決定，而最佳回應隨 `θ` 改變，價值函數不是 multilinear") and 42 §7.4 (iii), which says C/C0 can only be graded `ROBUST_ON_GRID`. R5(ii) adds that the pessimistic value is not merely non-multilinear but can be discontinuous. So grid coverage statements in C are statements about the evaluated points only.

---

## 4. Consequences for the v2.2 outputs

| Output | Exact by vertices? | Basis |
|---|---|---|
| B/A+ whole-portfolio `whole_portfolio_robust` (`lemma_r_check`) | **Yes** under (R-a)–(R-e) | Thm R1 |
| B/A+ MaxRegret, minimax-regret decision | **Yes** (same hypotheses) | Cor R1a |
| B/A+ λ-box certificate (`PARTIAL_OBJECTIVE`, `certified`) | **Yes** | Cor R1b |
| B element classification (`classify_element`) | **No**, except in the R4 case or under the 42 §13.3 (a) sufficient certificate | Props R2–R4 |
| C/C0/A anything (leader decision, `F_E^{C,m}`, DL, NEV) | **No** | Prop R5 |
| Any model with dependent constraints across blocks | **No** | (R-c) fails |
| Candidate sets with CONDITIONALLY_FEASIBLE members | **No** for those members | (R-d) fails |
| VOI vertex version | Upper bound only (42 §13.5, T-SEN-7) | not a vertex property in the sup over `v` |

## 5. Scope sentence (for the manuscript)

> **Vertex exactness is valid for** whole-portfolio optimality, MaxRegret and the λ-box certificate in Model B (and A+). This requires a fixed set of robustly feasible candidate portfolios, a registered group `Θ_g` that is a Cartesian product of block polytopes without cross-block dependence constraints, and an objective that is affine in each registered block (single-factor-class blocks). **It is not valid for** decision-element classifications (`y_c`, `q_j`, `e_u`, `γ`) in any model, except when a single candidate portfolio carries the element value. It is also not valid for any Model C, C0 or A quantity whose value passes through a follower best response (leader decisions, `F_E^{C,opt/pess}`, DL, NEV), for groups with dependence constraints, or for portfolios that are only conditionally feasible.

## 6. Relation to v2.2 and literature

* No contradiction with 42 §13.3: Theorem R1 restates Lemma R with explicit (R-a)–(R-e). Props R2, R4 and R5(ii) are additions: an exact covering characterization, an exact special case, and discontinuity in C.
* **Restatement of v2.2 vs genuinely new (T7, consistent with Q/11 §3 item 4).** *Restatement:* Thm R1 (Lemma R), Cor R1a (42 §13.2), Cor R1b (42 §7.4 (iii)), and the R3 instance (42 §13.3 / T-SEN-3; only the minimality proof is new). *Genuinely new in-model:* Prop R2 (exact covering characterization), Prop R4 (exact special case: the vertex test is also necessary when one candidate carries the element value), Prop R5(ii) (discontinuity of `V^pess` in Model C), and the scope sentence (§5).
* **Known analogues — TO VERIFY (Q/11 A10):** interval minmax-regret combinatorial optimization (Kouvelis & Yu; Averbakh) — not in the 59a list; the vertex property itself is standard robust-optimization knowledge (Ben-Tal et al., 2009, in list, TYPE B). Optimistic vs pessimistic bilevel discontinuity: Dempe (2002), Wiesemann et al. (2013) (in list); Loridan & Morgan (to verify).
* **AI-specificity (Q/11 A11):** nothing here is AI-specific; R1–R5 hold for any block-multilinear portfolio model.
* Relation to P1–P8: none of P1–P8 is used. Lemma E′ is not used: the follower's envelope plays no role in R5 except through `X*_u`.
* **TYPE B anchors (reference list of 59a only):** Ben-Tal et al. (2009) for set-based uncertainty / robust optimization; Savage (1951) for the minimax-regret criterion (manuscript marks it PARTIAL, N34); Wiesemann et al. (2013) for pessimistic bilevel selection. The vertex property of block-affine functions on product polytopes is standard. It is proved here in full rather than cited, because no reference in the list states it. Theorem R1's hypothesis list and Props R2–R5 are **TYPE C**.

## Appendix A — T-SEN-3 minimal counterexample (element level, Model B)

**Instance.** One block `θ ∈ [0,1]`: a two-distribution mixture of one probability row, so `F` is affine in `θ` and (R-b), (R-c) hold. Three robustly feasible whole portfolios (R-d): `y1_a` with `F = θ`, `y1_b` with `F = 1 − θ` (both contain `y_c = 1`), and `y0` with `F = 0.6` (`y_c = 0`). Element `d°: y_c = 1`.

**Optimality regions.** `y1_b` on `[0, 0.4]`, `y0` on `[0.4, 0.6]`, `y1_a` on `[0.6, 1]`. At `0.4` and `0.6` there are ties.

**Vertex check.** `θ = 0`: `max(0, 1) = 1 ≥ 0.6`. `θ = 1`: `max(1, 0) = 1 ≥ 0.6`. So the element test gives **ROBUST** at the vertices.

**Truth.** At `θ = 0.5`, `max(0.5, 0.5) = 0.5 < 0.6`, so `y_c = 1` is not optimal. It fails exactly on `(0.4, 0.6)`, and the correct class is **FRAGILE** (single group). The 42 §13.3 (a) sufficient condition is silent here, as it should be. `y1_a` is not optimal at `θ = 0` (`0 < 1`), and `y1_b` is not optimal at `θ = 1`, so no single portfolio containing `d°` is Lemma-R certified.

**Whole-portfolio control.** For every pair of portfolios, the minimum of the affine gap over a 101-point grid equals the minimum over `{0, 1}`, and every portfolio's MaxRegret over the grid equals its vertex value. Theorem R1 and Cor R1a hold on the same instance (W7, `B_lemma_r_whole_portfolio_exact = B_maxregret_vertex_exact = True`).

**Reconciliation with 51 T-SEN-3.** 51 asserts `robustness_class` gives ROBUST from `{0, 1}` and FRAGILE from `{0, ¼, ½, ¾, 1}`, and that `lemma_r_check` raises `ScopeError` for `model = "C"` and for `scope = "element"`. Baseline stdout l.14 reports PASS. These are exactly Prop R3 (element) and Prop R5 (Model C). 51's 4-seed whole-portfolio checks (vertex gap ≤ sampled gap; no sampled violation for certified portfolios) are synthetic regressions consistent with Theorem R1. They are not a proof of it.
