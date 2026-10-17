# 05 — Sequential identification and value of identification (VOI): formalization, proofs, counterexamples

**Pack:** Q1_THEORY_UPGRADE_V1_20261014 · **Task:** E (theory agent T3) · **Date:** 2026-10-14
**Authority:** this file adds to v2.2 and does not change it. It does not modify `42_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md` (henceforth **42**) or `51_enterprise_portfolio_solver_v2_2.py` (henceforth **51**). Every numerical object below is either an algebraic oracle or a `SIMULATED_ONLY` synthetic instance. There are no enterprise parameters, no ROI claims, and no V7 or enterprise-validity claim. Human coder results do not exist and none are used.
**Scope:** Model B (centralized, whole portfolio) only, as in 42 §13.3. Model C and element-level classification are excluded (see §8).
**Witness code:** `Q\witness_parts\w_voi.py` (pure stdlib, exact `Fraction` arithmetic). It has six witnesses, W6, W6b, W6c, W6d, W6e and W6f, and all of them PASS.
**Sidecar (SIMULATED_ONLY):** `Q\work\E\voi_sidecar_sim.py` writes `Q\work\E\VOI_SIDECAR_SIMULATED_ONLY.json`.

Status vocabulary: **THEOREM / PROPOSITION** means proved here. **COUNTEREXAMPLE** means a constructive example with exact witness arithmetic and a hand derivation. **EXTENSION** means a definition that v2.2 does not contain. **NOT_PROVEN** means an open item. **SYNTHETIC REGRESSION** means the sidecar run. No result here is proved by simulation.

---

## 0. Verdict lines

| # | Claim | Status |
|---|---|---|
| E.1 | `Θ' ⊆ Θ ⇒ MMR_C(Θ') ≤ MMR_C(Θ)` for a **fixed** candidate set `C` | PROPOSITION (proved) |
| E.1-adaptive | The same claim when the candidate set is recomputed as `C(Θ)` = ROBUSTLY_FEASIBLE on `Θ`. This is what calling `solve_robust` at every step does. | **REFUTED**: W6b gives MMR 0 → 1, and 0 → 3/5 in the one-block variant |
| E.1-sharp | With a Θ-independent pointwise-feasible benchmark, MMR is non-increasing, but vertex exactness is lost | PROPOSITION (monotonicity) + COUNTEREXAMPLE W6d (vertex value 0, true value 1/2) |
| E.2 | `0 ≤ VOI_p^true ≤ VOI_p^grid ≤ VOI_p^vertex ≤ MMR(Θ)` for a fixed `C`. This is the v2.2 definition as implemented in 51 `voi_table`. | PROPOSITION (proved) |
| E.2-adaptive | VOI ≥ 0 when the candidate set is recomputed on the conditioned set | **REFUTED**: W6b gives `VOI_q = −1`. True for one block only. |
| E.3 | Vertex-only VOI overstates; T-SEN-7 oracle: `VOI_v^vertex = 1`, `VOI_v^true = 1/2` | PROPOSITION (analytic derivation) + W6. The minimal witness is 2 candidates × 2 blocks. |
| E.4 | Exact VOI is computable from a finite set of points: the breakpoints of a line arrangement for a scale block, and the vertices of a hyperplane arrangement for a probability block | PROPOSITION (proved; implemented for scale blocks only) |
| E.5 | A common minimax-regret minimizer for all `v ∈ Θ_p` implies that vertex VOI is exact | PROPOSITION (sufficient condition only; the converse is NOT_PROVEN) |
| E.6 | Nested grids give monotonically non-increasing (improving) upper bounds. Non-nested grids do not (W6c: grid 4 → grid 5 moves 1/2 → 3/5). 51's edge-only probability-block grid does not converge when a block has ≥ 3 vertices (W6c: ≥ 1/2 against a true value of 1/3). | PROPOSITION + COUNTEREXAMPLES |
| E.7 | Termination is guaranteed when evidence states are finite (≤ Σ_p h_p measurement steps) | THEOREM (proved) |
| E.8 | Without discretized evidence, termination under rule A is not guaranteed | COUNTEREXAMPLE W6f (strictly nested boxes, MMR > 1/4 for all t) |
| E.9 | Myopic VOI can be 0 for every block while joint identification removes all regret, so rule D can stop with MMR = 1 | COUNTEREXAMPLE W6e |
| E.10 | Rule B ⇔ `MMR_C(Θ^(t)) = 0` ⇔ a Lemma R whole-portfolio certificate holds for some `d ∈ C` | PROPOSITION (proved, for a fixed `C`) |
| — | Optimality of VOI-greedy ordering; a convention that is adaptive, monotone and vertex-exact at once; an exact algorithm for the sharp benchmark; any guarantee for rule C | **NOT_PROVEN** (see §9) |

**Novelty label (T7 per Q/11 A7, A10): TYPE C in-model; known analogues — TO VERIFY.** The results above are in-model formalizations of facts with well-known analogues: E.1-adaptive / E.2-adaptive (W6b) are the menu-dependence (IIA failure) of minimax regret (Chernoff; Stoye's minimax-regret axioms); E.9 (W6e) is the standard complementarity / non-submodularity of information value; E.4 is a standard parametric piecewise-linear argument; W6 (vertex overstatement) is already in v2.2 (42 l.590, 51 T-SEN-7). None of these works is in the 59a list; no bibliographic details are asserted.

**Restatement of v2.2 vs genuinely new (consistent with Q/11 §3 item 5):**
* *Restatement / specialization:* Lemma 0 (42 l.535 with its proof made explicit), E.2 (the ordering 42 §13.5 already asserts; new is only the explicit fixed-candidate-set premise), E.3 (= T-SEN-7 / 42 l.590; only the minimal 2×2 witness W6 is new), E.10 (Lemma R restated as a stopping rule).
* *Genuinely new in-model:* E.6(e) (51's edge-only probability grid does not converge: ≥ 1/2 against a true 1/3 — implementation-relevant), E.7 / E.8 (termination needs finite evidence states), the adaptive-candidate-set warning E.1/E.2-adaptive as an operational caveat (W6b), E.4 (exact VOI by finite enumeration), and the (F)/(Ad)/(♯) table (not a general impossibility).
* *Protocol, not theorem:* SIP (§3) is an EXTENSION protocol; in the manuscript it must be presented as a protocol, and the sidecar's finding that VOI policies did **not** beat RANDOM on residual regret (§6(6)) must be kept with any use.

---

## 1. Canonical definitions used (quoted from v2.2)

**D1 — Admissible set** (42 §13.1, L512–520). "`Θ_adm = ∪_{g∈𝒢} Θ_g`. Each `Θ_g` is: the interval product of monetary and quantity parameters (`[L,U]`); for each probability row, the polytope 'simplex ∩ interval box'; and pre-registered dependence restrictions." 42 §13.1(i) (L522) requires block-multilinearity: each block acts on a single factor class, and no two blocks act on the same cell. It describes this as "the checkable version of the block-multilinear premise needed by all vertex arguments (Lemma R, MaxRegret, feasibility certificates)."
*Assumption used throughout (A-PROD):* `Θ_g = ×_{p∈P} Θ_p` is a product of block polytopes with no dependence restrictions. This is the precondition of 42 §13.3, and item 3 there excludes the dependent case. In 51 a block is either `scale` (an interval `[L,U]` multiplying target cells) or `prob` (the convex hull of listed vertex rows) (51 `block_vertices`, L1278–1283; `apply_theta`, L1294–1306).

**D2 — Candidate set** (42 §13.3, L549, and the feasibility classes, L551–558). "In each `Θ_g`, **only robust-feasible configurations and plans** are admitted to the classification candidate set … Lemma R is exact on the fixed candidate set." Candidates are first enumerated from θ-independent conditions (F2)–(F8). A portfolio is `ROBUSTLY_FEASIBLE` when "every slack ≥ 0 at every vertex", which is a certificate because slacks are affine per block. In 51 `solve_robust` (L1435–1465), `cands` = the ROBUSTLY_FEASIBLE portfolios **for the group's blocks**. We write `C(Θ)` for this set.

**D3 — Regret** (42 §13.2, L535). "`MaxRegret(d) = max_θ [F^*(θ) − F(d,θ)]` … In B, for a fixed candidate set, `F^*(θ) − F(d,θ)` is the max of multilinear functions minus a multilinear function, convex in each block separately, so MaxRegret is attained at a vertex of the product polytope (exact)." The benchmark is `F^*_C(θ) = max_{d'∈C} F(d',θ)`, the best **candidate** (51 `max_regret`, L1497–1499). We write `R_d^C(θ) = F^*_C(θ) − F(d,θ)` and `MR_C(d;Θ) = max_{θ∈Θ} R_d^C(θ)`.
*Convention for ε-ROBUST* (42 L535 names it but does not define it): `d` is ε-ROBUST on `Θ` iff `MR_C(d;Θ) ≤ ε_R`.

**D4 — MMR** (42 §13.5, L588: "`MMR` is the minimax regret over the candidate set"; 51 `minimax_regret`, L1502–1503). `MMR_C(Θ) = min_{d∈C} MR_C(d;Θ)`. Ties: `solve_robust` selects `d* = argmin (MR, canonical JSON of d)` (L1462). We write `M_C(Θ)` for the full argmin set.

**D5 — VOI** (42 §13.5, L583–593; 51 `voi_generic`, L1506–1534):

$$VOI_p = MMR(\Theta_g) - \sup_{v\in V_p} MMR(\Theta_g \mid \theta_p = v).$$

"`MMR(Θ_g)` and every `MMR(Θ_g | θ_p = v)` are exact on the vertices of the other blocks. … **vertex VOI**: `V_p` = the vertices of block `p`; this can **overstate** … **grid VOI**: `V_p` adds interior points (an equally spaced grid; a probability block includes two-vertex mixtures). It is still an upper bound on the true value and no larger than the vertex VOI." The diagnostic "only sets data-collection priority and does not enter the objective."

Three points of interpretation fix the semantics:

- **(i) Grid vs vertex.** v2.2 defines VOI with a sup over a value set `V_p` and reports two computational versions, vertex and grid. We define `VOI_p^true` as the case `V_p = Θ_p`. 42 calls this "the true value" (真值) without a symbol.
- **(ii) Worst-case, full identification.** `VOI_p` is a **worst-case (over the revealed value) guaranteed MMR reduction from fully identifying block `p` to a point**. It is not an expectation, because v2.2 has no prior (42 §17 D7).
- **(iii) Fixed candidate set.** 51 `voi_table(inst, gamma, candidates, blocks)` uses the caller's candidate set for the unconditioned set and for every conditioned set. The candidate set is **fixed** at `C(Θ_g)`. All of 42 §13.5's ordering claims hold under this reading (Proposition E.2).

**D6 — Lemma R** (42 §13.3, L541). "For two fixed portfolios `d, d'`, `Δ(θ) = F_E(d;θ) − F_E(d';θ)` is block-multilinear … `min_{θ∈Θ_g} Δ(θ)` is attained at a vertex of the product. Hence in Model B, 'the whole portfolio `d` is optimal throughout `Θ_g`' can be decided exactly by vertex checks against every competitor `d'`."

**D7 — Dynamic shadow** (42 §16 (D2), L652). "Its observation makes `Θ_{t+1} ⊂ Θ_t` … until then report only the static diagnostic of §13.5." The procedure below is a **static-sequential** reading of (D2). It has no prior and no discounting, and it is not the dynamic expected-value program.

### Lemma 0 (vertex exactness; a restatement of 42 L535 with its proof made explicit)

*Assumptions:* (A-PROD), (A-ML): `F(d,·)` is multilinear across blocks, meaning affine in each block's point when the other blocks are fixed. `C` is finite and fixed. *Claim:* for every `d ∈ C`, `MR_C(d;Θ) = max_{θ∈vert(Θ)} R_d^C(θ)`, where `vert(Θ) = ×_p vert(Θ_p)`. Consequently `MMR_C(Θ)` is computed exactly on `vert(Θ)`.

*Proof.* Fix all blocks except `p`. Each `F(d',·) − F(d,·)` is affine in `θ_p`, so `R_d^C` (a max of finitely many affine functions) is convex in `θ_p`. A convex function on a polytope attains its maximum at a vertex. Start from a maximizer `θ⁰` of the continuous function `R_d^C` on the compact set `Θ` (the max exists). Replace `θ⁰_1` by a vertex of `Θ_1` without decreasing `R`, then do the same for `θ_2`, and so on. After `|P|` steps all coordinates are vertices and the value is ≥ `R_d^C(θ⁰)`, so it equals the max. ∎ (TYPE C restatement of a v2.2 claim. No new content.)

**What Lemma 0 does *not* give:** the outer `sup_v MMR_C(Θ | θ_p = v)`. As a function of `v`, `MMR_C(v) := MMR_C(Θ|θ_p=v) = min_{d∈C} r_d(v)` with `r_d(v) = max_{τ∈vert(Θ_{−p})} R_d^C(v,τ)`. Each `r_d` is convex in `v`, but a **min of convex functions is not convex**, so the sup can lie in the interior of `Θ_p`. That is the entire mechanism behind the vertex-VOI overstatement (§6.3(3)).

---

## 2. Lemma R vs parameter-identification VOI (must not be conflated)

| | Lemma R (42 §13.3) | VOI_p (42 §13.5) |
|---|---|---|
| Object | One fixed whole portfolio `d` against fixed competitors | A parameter block `p` of `Θ` |
| Question | Is `d` optimal for **all** `θ ∈ Θ_g`? Equivalently, `min_θ Δ ≥ 0` | By how much is minimax regret **guaranteed** to fall if `θ_p` is learned exactly? |
| Optimization structure | `min_θ` of a multilinear function: exact at a vertex | `max_v min_d max_τ`: the inner max is exact at vertices (Lemma 0), the outer `max_v` of a min is **not** |
| Exactness | Exact certificate (Model B, fixed `C`) | Vertex version: upper bound, possibly loose (W6). Grid: tighter upper bound. True value: finite arrangement (E.4). |
| Relation | Lemma R holds for some `d` ⇔ `MMR_C(Θ) = 0` (Prop. E.10) ⇒ `VOI_p = 0` for every `p` | VOI quantifies how far the current state is from a Lemma R certificate, per block |

Lemma R is **portfolio-level and exact**. VOI is **parameter-level and only upper-bounded** unless E.4 is used. In the manuscript, the "exact" claim of §3.13 must stay attached to MaxRegret and Lemma R and must never be attached to VOI.

---

## 3. §6.1 Sequential identification procedure (SIP)

**Setting.** Registered group `g`, initial set `Θ^(0) = Θ_g = ×_p Θ_p^(0)`, and tolerance `ε_R ≥ 0` (pre-registered, 42 L522). An **evidence state** for block `p` is a nonempty sub-polytope `Θ_p^(t) ⊆ Θ_p^(0)`. Block `p` is **identified** at step `t` iff `Θ_p^(t)` is a singleton. `U_t` is the set of unidentified blocks.

**Narrowing (formal meaning of "collect evidence").** A measurement of block `p` at step `t` returns an evidence state `o ∈ 𝓔_p(Θ_p^(t))`. Here `𝓔_p(S)` is the pre-registered family of possible outcomes when the current state is `S`. Each `o` satisfies `o ⊆ S` (consistency), and the outcomes cover `S` (`∪ 𝓔_p(S) = S`, so the true `θ_p` is always consistent with some outcome). Then

$$\Theta^{(t+1)} = \Theta_1^{(t)}\times\cdots\times o \times\cdots\times\Theta_{|P|}^{(t)},\qquad \Theta^{(t+1)}\subseteq\Theta^{(t)}\ \text{(block-wise shrinkage, product structure preserved)}.$$

- *v2.2-consistent special case:* `𝓔_p(S) = {{v}: v ∈ S}` (full identification). This is exactly the conditioning in `VOI_p`.
- *EXTENSION — partial evidence:* `𝓔_p(S)` = a finite family of sub-intervals (for example the halves of `S`) or sub-polytopes. The matching index is `VOI_p^{𝓔} = MMR(Θ^(t)) − max_{o∈𝓔_p} MMR(Θ^(t) with Θ_p := o)`. It reduces to D5 when `𝓔_p` is the set of singletons.
- *Registry discipline (EXTENSION).* v2.2 commits one registry per solve (42 L522(ii)). Changing an interval afterwards fails verification by design (T-SEN-6). SIP therefore needs **versioned registries**: each `Θ^(t)` is committed as registry version `t` with a parent hash and the evidence record that justified the narrowing. v2.2 has no such lineage object. An observation outside `Θ_p^(t)` is a registry contradiction and must be reported (suggested status `REGISTRY_INCONSISTENT_EVIDENCE`, an extension). It must not be silently absorbed.

**Candidate-set convention (must be declared; it changes the theory, see §5).**

- **(F) fixed:** `C^(t) ≡ C^(0) = C(Θ^(0))`. This is consistent with 51 `voi_table`.
- **(Ad) adaptive:** `C^(t) = C(Θ^(t))`. This is what calling `solve_robust` with the narrowed group at each step does. Here `C(Θ^(t)) ⊇ C(Θ^(t−1))` (Lemma 5.1).

**Algorithm SIP.**

```
input: Θ^(0) (registered, committed), ε_R, convention ∈ {F, Ad}, VOI mode ∈ {vertex, grid(n), exact}, rule set ⊆ {A,B,C,D}
t ← 0
loop:
  C^(t) ← C^(0) (F) or C(Θ^(t)) (Ad)                 # 51 robust_feasibility at vertices
  if C^(t) = ∅: stop with status INFEASIBLE (as solve_robust)
  MMR_t ← min_{d∈C^(t)} max_{θ∈vert Θ^(t)} R_d^{C^(t)}(θ)       # exact, Lemma 0
  d*_t ← argmin (MR, canonical d)  ;  M_t ← full argmin set
  if any active stopping rule fires (§4): stop, report (d*_t, MMR_t, M_t, Θ^(t), registry lineage)
  for p ∈ U_t (eligible = not exhausted):
     VOI_p^(t) ← MMR_t − sup_{v∈V_p(mode)} MMR_{C^(t)}(Θ^(t) | θ_p = v)     # D5 at state Θ^(t)
  if no eligible block: stop with status EXHAUSTED (report MMR_t > ε_R if so)
  p_t ← argmax_p VOI_p^(t)  (ties: registry block order)
  collect evidence on p_t → Θ^(t+1) (narrowing above); commit registry version t+1
  t ← t+1
```

**Mode reporting** (inherits 42 L588: "the way the sup is taken must be reported"). A vertex mode carries the flag `VOI_UPPER_BOUND_LOOSE_POSSIBLE` (§6.3(3)). A grid mode must report `n` and whether the grids used across steps are nested (§6.3(4)).

**Guarantee interpretation (Corollary of E.1/E.2, fixed C, exact sup).** If `p_t` is fully identified at any `v_obs ∈ Θ_{p_t}^(t)`, then `MMR_{t+1} ≤ MMR_t − VOI_{p_t}^{(t),true}`. *Proof:* `MMR_{t+1} = MMR_C(Θ^(t)|θ_p=v_obs) ≤ sup_v MMR_C(Θ^(t)|θ_p=v) = MMR_t − VOI^true`. ∎ This guarantee **fails for vertex VOI**. In W6 the vertex VOI promises `MMR_{t+1} ≤ 0`, yet observing `v = 1/2` leaves `MMR = 1/2`. For a grid VOI the guarantee holds only if the grid contains the maximizer of `MMR(v)`.

---

## 4. §6.2 Stopping rules

**Rule A (ε-regret).** Stop when `MMR_t ≤ ε_R`. The reported `d*_t` is then ε-ROBUST on `Θ^(t)` (D3 convention). This is exact by Lemma 0. Under (F), `MMR_t` is non-increasing (E.1), so once rule A fires it stays satisfied under further narrowing. Under (Ad) this is **false**: W6b gives `MMR_0 = 0 ≤ ε_R` and then `MMR_1 = 1` after narrowing. A certificate issued under (Ad) at step `t` is relative to `C(Θ^(t))` and may be withdrawn at `t+1`.

**Rule B (certified optimal portfolio).** Stop when some `d ∈ C^(t)` is optimal for every `θ ∈ Θ^(t)`.

*Proposition E.10.* Under (A-PROD), (A-ML) and fixed finite `C^(t)` the following are equivalent:
- (a) there exists `d ∈ C^(t)` with `F(d,θ) ≥ F(d',θ)` for all `d' ∈ C^(t)` and all `θ ∈ Θ^(t)`;
- (b) `MMR_{C^(t)}(Θ^(t)) = 0`;
- (c) for some `d`, the Lemma R vertex check `min_{θ∈vert} [F(d,θ) − F(d',θ)] ≥ 0` holds for every `d'`.

*Proof.* (a)⇒(b): `R_d ≡ 0`, so `MR(d) = 0`, and `MMR ≥ 0` because `d ∈ C` gives `R_d ≥ 0`. (b)⇒(a): the min over finite `C` is attained, so `MR(d) = 0` for some `d`, i.e. `F^*_C(θ) = F(d,θ)` for all `θ`. (a)⇔(c) is Lemma R (D6). ∎

*Ties:* 51 uses a tolerance of `1e-7` in `lemma_r_check`. With tolerance τ, (b) becomes `MMR ≤ τ`, and rule B coincides with rule A at `ε_R = τ`. Rule B is the `ε_R = 0` case of rule A. Optimistic vs pessimistic follower selection does not arise because this is Model B. With non-unique `M_t` the certificate holds for **every** member of `M_t` that has `MR = 0`, and `solve_robust`'s canonical tie-break selects one. The certificate is relative to `C^(t)`; a CONDITIONALLY_FEASIBLE portfolio can be better at some θ and still sits outside the comparison (42 L549).

**Rule C (stability; heuristic, not a certificate).** Fix a window `W ≥ 1`, an element map `e(·)` (for example `y`, or `γ`, or the full portfolio), and a tolerance `ε_R`. Define

- *strong stability at t:* `M_t = M_{t−1} = … = M_{t−W}` and `|M_t| = 1`;
- *weak stability at t:* `∩_{s=t−W}^{t} M_s ≠ ∅` (some decision has been minimax-regret optimal throughout the window; this is robust to tie-breaking);
- *element stability at t:* `e(d)` is constant over `∪_{s=t−W}^{t} M_s` (key elements are stable even if the portfolio changes).

Rule C stops on the declared stability type. The two tie conventions correspond to weak stability (any common minimizer counts) and strong stability (requires uniqueness). Rule C carries **no regret guarantee**. In W6f, `M_t = {D, E}` for every `t`, so weak stability, element stability, and the canonical `d*_t = D` all hold, while `MMR_t = 1/4 + 2^{−(t+2)} > 1/4`. (Strong stability fails only because of the `D`/`E` tie: both equal 1/2 once `q = 1/2` is identified.) The output must therefore always report `MMR_t` alongside a rule-C stop. Rule C must not be described as robustness.

**Rule D (marginal VOI below measurement cost) — EXTENSION.** v2.2 contains **no measurement cost**. 42 §16 (D2) puts the pilot cost into the dynamic objective, which is not in the baseline. Introduce pre-registered costs `κ_p ≥ 0` in TWD/period, the same unit as MMR (42 L535, `ε_R` in TWD/period). Stop when `max_{p∈U_t} (VOI_p^(t) − κ_p) ≤ 0`.

- *Stop-safety (proved).* If rule D is evaluated with any upper bound `\overline{VOI}_p ≥ VOI_p^true` (vertex or grid, E.2), then stopping implies `VOI_p^true ≤ κ_p` for all `p`. Rule D therefore never stops "too early" relative to the true single-block index. The **selection** of `p_t` can still be wrong under a loose bound: W6 ranks `v` at 1 and `q` at 1 under vertex VOI, while both are 1/2 in truth.
- *Myopia (COUNTEREXAMPLE W6e).* With `F_X = (2v−1)(2q−1)` and `F_Y = 0`, `VOI_v^true = VOI_q^true = 0` and `MMR = 1`, but identifying both blocks gives `MMR = 0`. Rule D with any `κ > 0` stops at `MMR = 1`. Single-block VOI is not super-modular in general, and rule D is a myopic index, not an optimal stopping rule.
- Comparing a worst-case MMR reduction with a cost is a **decision-rule choice**, not a theorem. It should be stated as such and pre-registered.

---

## 5. §6.3(1) Does shrinking Θ make MMR non-increasing?

**Lemma 5.1 (hereditary robust feasibility).** If `Θ' ⊆ Θ`, then `C(Θ') ⊇ C(Θ)`. *Proof:* `d ∈ C(Θ)` ⇔ every slack is ≥ 0 at every vertex of `Θ` ⇔ (slacks multilinear, Lemma 0 argument applied to `−slack`) every slack is ≥ 0 on all of `Θ` ⇒ ≥ 0 on `Θ'` ⇔ `d ∈ C(Θ')`. ∎

**Proposition E.1 (fixed C).** For finite fixed `C ≠ ∅` and `Θ' ⊆ Θ`: `MMR_C(Θ') ≤ MMR_C(Θ)`. *Proof:* for each `d`, `MR_C(d;Θ') = max_{Θ'} R_d^C ≤ max_Θ R_d^C`, because `R_d^C` does not depend on `Θ`. Take the min over the same `C`. ∎ Neither multilinearity nor product structure is used. (TYPE C, elementary.)

**Proposition E.1-adaptive is FALSE (COUNTEREXAMPLE W6b).** Blocks `v, q ∈ [0,1]`. Portfolio `A`: `F = v`, always feasible. Portfolio `B`: `F = 1 − v`, slack `1/2 − q` (affine, so allowed by 42 L522).
- `Θ^(0) = [0,1]²`: `B` is infeasible at `q = 1`, so `C = {A}` and `MMR_0 = 0`. Rule A is satisfied for any `ε_R ≥ 0`, and Lemma R certifies `A` vacuously.
- Evidence narrows `q` to `[0, 1/2]`, giving `Θ^(1) = [0,1]×[0,1/2]`. Now `C = {A,B}`. `MR(A) = max_v (1−v) − v = 1` (at `v = 0`) and `MR(B) = 1` (at `v = 1`), so `MMR_1 = 1`.
- With `C` frozen at `{A}`: `MMR_1 = 0`, consistent with E.1.
- *One-block variant:* `v ∈ [0,1]`, `B` with slack `4/5 − v`, `Θ^(1) = [0, 4/5]`. Then `MR(A) = max_v (1 − 2v)^+ = 1` and `MR(B) = max_v (2v − 1)^+ = 3/5` (at `v = 4/5`), so MMR goes from 0 to `3/5`.

*Mechanism.* Narrowing enlarges `C` (Lemma 5.1), which enlarges both the minimization set (pushing MMR down) and the **regret benchmark** `F^*_C` (pushing MMR up). The second effect can dominate. The "increase" is not a loss of achievable value: `A` still guarantees exactly what it guaranteed before. What changed is that a better-in-places alternative entered the comparison. This links to 42 P7/P8 channel (ii), "robust feasibility": narrowing `Θ` can create robust feasibility, and with it new regret.

**Proposition E.1-sharp (Θ-independent benchmark).** Define `F^♯(θ) = max{F(d,θ): d statically feasible and all slacks ≥ 0 at θ}`, the best portfolio feasible **at** `θ`, independent of `Θ`. Let `MMR^♯(Θ) = min_{d∈C(Θ)} max_{θ∈Θ} [F^♯(θ) − F(d,θ)]`. Then `Θ' ⊆ Θ ⇒ MMR^♯(Θ') ≤ MMR^♯(Θ)`. *Proof:* each max is over a smaller set with an unchanged integrand, and the min is over a larger set (Lemma 5.1). ∎ **But** `F^♯` is not multilinear, because the feasible set jumps with `θ`. Lemma 0 then fails. **W6d:** `A`: `F = 0`; `B`: `F = q`, slack `1/2 − q`. The vertex MaxRegret♯ of `A` is 0, while the true value at `q = 1/2` is 1/2.

**Summary (trilemma among the three conventions examined; not a general impossibility theorem):**

| Convention | MMR monotone under narrowing | Vertex-exact (Lemma 0) | Uses newly robust-feasible portfolios |
|---|---|---|---|
| (F) fixed `C^(0)` | yes (E.1) | yes | no |
| (Ad) adaptive `C(Θ^(t))`, benchmark over `C` | **no** (W6b) | yes | yes |
| (♯) adaptive `C`, pointwise-feasible benchmark | yes (E.1-sharp) | **no** (W6d) | yes |

Whether some other convention achieves all three is **NOT_PROVEN**. *Recommendation:* run SIP under (F) for the monotone guarantee and the stopping-rule semantics. Report (Ad) as a secondary diagnostic, with a flag `CANDIDATE_SET_EXPANDED` whenever `C(Θ^(t)) ⊋ C^(0)`.

---

## 6. §6.3(2)–(6)

### (2) Is VOI ≥ 0?

**Proposition E.2 (fixed C; v2.2 as implemented).** Under (A-PROD), (A-ML), finite fixed `C`, and any `V_p ⊆ Θ_p` containing the vertices of `Θ_p`:
`0 ≤ VOI_p^true ≤ VOI_p^{V} ≤ VOI_p^{vertex} ≤ MMR_C(Θ)`.
Moreover, `VOI_p^{G'} ≤ VOI_p^{G}` whenever `vert(Θ_p) ⊆ G ⊆ G'`.

*Proof.*
- `{θ: θ_p = v} ⊆ Θ`, so `MMR_C(Θ|v) ≤ MMR_C(Θ)` for every `v` (E.1). Hence `sup_{Θ_p} ≤ MMR(Θ)` and `VOI^true ≥ 0`.
- `sup_{v∈V} ≤ sup_{v∈Θ_p}` for `V ⊆ Θ_p` gives `VOI^V ≥ VOI^true`.
- `G ⊆ G'` gives `sup_G ≤ sup_{G'}` and therefore `VOI^{G'} ≤ VOI^G`. With `G = vert(Θ_p)` this yields `VOI^V ≤ VOI^vertex`.
- `MMR(Θ|v) ≥ 0` gives `VOI ≤ MMR(Θ)`.
- *Existence of the sup:* `v ↦ MMR_C(Θ|v) = min_d max_{τ∈vert(Θ_{−p})} R_d^C(v,τ)` is a finite min of finite maxima of continuous (affine) functions, hence continuous on the compact set `Θ_p`. The sup is attained. ∎

This is exactly the ordering that 42 §13.5 asserts and that 51 T-SEN-7 checks (`0 ≤ grid ≤ vertex`). The proof shows it needs **only** the fixed candidate set, and not multilinearity, except for the exactness of each `MMR` evaluation.

**E.2-adaptive is FALSE (W6b).** With the candidate set recomputed on each conditioned set, `MMR(Θ^(0)) = 0`, `MMR(Θ^(0)|q=0) = 1` (because `C = {A,B}`), and `MMR(Θ^(0)|q=1) = 0`. Hence `VOI_q^{vertex, adaptive} = 0 − 1 = −1`. The true adaptive value is also ≤ −1, since `q = 0 ∈ Θ_q`. *Minimality:* with a single block, every conditioned set is a point, and the adaptive `MMR(point) = 0` (choose the best feasible candidate). So adaptive `VOI ≥ 0` for one block, and negativity needs ≥ 2 blocks.

### (3) The vertex-only VOI overstates the true value: analytic derivation (T-SEN-7 oracle)

Candidates `F_A = 1−v`, `F_B = v`, `F_D = q`, `F_E = 1−q`, with `Θ = [0,1]²` and a fixed `C = {A,B,D,E}`.

- *MMR(Θ).* `F^*(v,q) = max(1−v, v, q, 1−q)`, which equals 1 at every vertex. At the vertex `(v,q) = (1,·)` the regret of `A` is `1 − 0 = 1`. Likewise `B` at `v=0`, `D` at `q=0` and `E` at `q=1` each have regret 1. So `MMR(Θ) = 1`.
- *MMR(Θ | v).* The other block `q` ranges over its vertices `{0,1}`, so `F^* = 1` there (Lemma 0 makes the vertices sufficient). Regrets: `MR(A) = 1 − (1−v) = v`, `MR(B) = 1 − v`, and `MR(D) = MR(E) = 1` (at `q = 0` and `q = 1` respectively). So `MMR(v) = min(v, 1−v)`.
- *Vertex VOI.* `V_v = {0,1}`, with `MMR(0) = MMR(1) = 0`, so `VOI_v^vertex = 1 − 0 = 1`.
- *True VOI.* `sup_{v∈[0,1]} min(v,1−v) = 1/2` at `v = 1/2`, so `VOI_v^true = 1 − 1/2 = 1/2`. The grid with `n = 4` contains `1/2`, so `VOI_v^{grid4} = 1/2`. By symmetry `VOI_q^true = 1/2`.

The overstatement factor is 2 (W6 PASS; the exact breakpoint sup E.4 finds `v = 1/2` among 5 candidate points). The **operational meaning** is that vertex VOI = 1 implies "after measuring `v`, MMR will be 0". If the measured value is `v = 1/2`, MMR stays at 1/2.

**Formal statement.** `VOI_p^vertex − VOI_p^true = sup_{Θ_p} MMR(·) − max_{vert Θ_p} MMR(·) ≥ 0`. Equality holds iff the sup of `MMR(v) = min_d r_d(v)` is attained at a vertex. Since each `r_d` is convex (Lemma 0 argument) and the min of convex functions is not convex, equality is not guaranteed.

**Proposition E.5 (sufficient condition for exact vertex VOI).** If some `d° ∈ C` belongs to `M_C(Θ|θ_p=v)` for every `v ∈ Θ_p`, then `MMR(v) = r_{d°}(v)` is convex and its sup is attained at a vertex, so `VOI^vertex = VOI^true`. ∎ (The converse is NOT_PROVEN and probably false.) In T-SEN-7 the minimizer switches from `A` (`v < 1/2`) to `B` (`v > 1/2`), and that switch is exactly the failure of E.5.

**Minimality (W6).** The minimal witness is 2 candidates × 2 scale blocks: `F_X = v`, `F_Y = q`. Here `MMR(Θ) = 1` and `MMR(v) = min(v, 1−v)`, so the vertex VOI is 1 and the true VOI is 1/2. With one candidate, regret is identically 0. With one block, conditioning yields a point with `MMR = 0` for every `v`, and vertex and true VOI coincide. 51's T-SEN-7 oracle (4 candidates) is therefore not minimal, but it is algebraically equivalent in mechanism.

**Proposition E.4 (exact VOI by finite enumeration).**
- *(a) Scale block `p` with `Θ_p = [L,U]`.* For `τ ∈ vert(Θ_{−p})` and `d, d' ∈ C`, the functions `ℓ_{d,d',τ}(v) = F(d',v,τ) − F(d,v,τ)` are affine (A-ML). `MMR(v) = min_d max_{d',τ} ℓ_{d,d',τ}(v)` is continuous and piecewise linear, with kinks only where two of these lines intersect. On each interval between consecutive points of `B = {L,U} ∪ {intersections in [L,U]}`, the order of all lines is constant, so `MMR` is affine there and attains its max at an endpoint. Hence `sup_{[L,U]} MMR = max_{v∈B} MMR(v)`, with `|B| ≤ 2 + (|C|²·|vert Θ_{−p}|)²/2`.
- *(b) Probability block with vertex set `{w^1..w^m}`.* In barycentric weights `λ ∈ Δ^{m−1}` (51 `apply_theta`: `θ_p = Σ λ_i w^i`), each `ℓ` is affine in `λ`. Take the arrangement of all hyperplanes `{ℓ_a = ℓ_b}`, intersected with `Δ^{m−1}`. On each closed cell the total order of the `ℓ`'s is fixed, so `MMR` is affine on the cell. The max over the polytope cell is at one of its vertices, and the cells have finitely many vertices in total. So `sup MMR` = max over the finite set of arrangement vertices. ∎ (TYPE C. (a) is implemented in `w_voi._w6_exact_sup_1d` and in the sidecar `VOI_EXACT`. (b) is proved but not implemented. Its complexity is exponential in `m` and in the arrangement size, and no complexity bound is claimed.)

### (4) Does grid refinement monotonically improve the upper bound?

**Proposition E.6.**
- (a) *Nested grids.* If `vert(Θ_p) ⊆ G_1 ⊆ G_2 ⊆ …`, then `VOI^{G_k}` is non-increasing in `k` and bounded below by `VOI^true` (E.2).
- (b) *51's uniform grids.* For a scale block, `G_n = {L + (U−L)t/n}`. `G_n ⊆ G_m` iff `n | m`: if `n | m`, then `t/n = (tm/n)/m`; conversely, `1/n ∈ G_m` requires `m/n ∈ ℤ`. The same holds for 51's two-vertex mixtures `t/grid` on each edge of a probability block (51 `block_values`, L1363–1377). So refining along the chain `n → kn` is monotone.
- (c) *Convergence.* For a scale block, or a probability block with exactly 2 vertices (a segment), `MMR(v)` is Lipschitz (piecewise linear with finitely many pieces). Hence `|VOI^{G_n} − VOI^true| ≤ Lip·(U−L)/(2n) → 0` (every point lies within half a grid step of a grid point; the earlier constant `Lip·(U−L)/n` is also valid but loose — tightened per Q/11 §2.9), along any sequence of grids, nested or not.
- (d) *Non-nested grids: COUNTEREXAMPLE (W6c).* On the T-SEN-7 oracle, `VOI^{G_4} = 1/2`, `VOI^{G_5} = 3/5` and `VOI^{G_9} = 5/9`. Moving from 5 points to 6 points makes the upper bound **worse**. 51's own T-SEN-7 check `vg9` (grid 9) only asserts the bound, which is consistent with this.
- (e) *Edge-only probability grids do not converge: COUNTEREXAMPLE (W6c).* A probability block with 3 vertices `e_1, e_2, e_3`, plus a scale block `q`. Candidates `W_i = w_i` and `D = q`, `E = 1−q`. Then `MMR(Θ) = 1` and `MMR(w) = 1 − max_i w_i`. On the 1-skeleton (51's grid), `max_i w_i ≥ 1/2`, so `VOI^{grid} ≥ 1/2` for every `n`. The true sup is attained at the barycentre (`max_i w_i ≥ 1/3`, with equality only there), so `VOI^true = 1 − 2/3 = 1/3`.

The statement "grid VOI ≤ vertex VOI" in 42 §13.5 is correct. But "adding interior points" in 51 means **edge points**, which leaves the interior of probability blocks with ≥ 3 vertices unexplored. *Recommendation:* add interior simplex lattice points, or use E.4(b), for such blocks.

### (5) Termination

**Theorem E.7 (finite evidence states ⇒ termination).** Suppose that:
- for every block `p`, the set of reachable evidence states `𝓢_p` (all sub-polytopes that any sequence of outcomes can produce) is **finite**;
- each measurement step on `p` replaces `Θ_p^(t)` by a **strictly smaller** element of `𝓢_p`, and a block with no strictly smaller reachable state is marked exhausted and becomes ineligible;
- `P` is finite.

Then SIP performs at most `H = Σ_p h_p` measurement steps, where `h_p` is the length of the longest strictly decreasing chain in `(𝓢_p, ⊊)`, and stops by a rule (A–D) or by EXHAUSTED. The number of MMR evaluations is at most `(H+1)(1 + Σ_p |V_p|)` for the vertex and grid modes. If the minimal states are singletons, then at exhaustion `Θ^(T)` is a point and `MMR_T = 0` under (F) and under (Ad) (choose the best candidate; `C(point) ⊇ C^(0) ≠ ∅` by Lemma 5.1), so rule A holds for any `ε_R ≥ 0`.

*Proof.* The potential `Φ_t = Σ_p ht_p(Θ_p^(t))` (the height of the current state in the finite poset) is a non-negative integer and strictly decreases with each measurement. The loop either stops or measures, so it runs at most `Φ_0 ≤ H` iterations. The evaluation count follows by counting per iteration. At a point, every `R_d` is evaluated at one θ, the minimizer is the best candidate, and `MMR = 0`. ∎

*Special case:* full identification with v2.2 conditioning has `h_p = 1` and gives at most `|P|` steps.

**Remark E.8 (non-termination without discretization: COUNTEREXAMPLE W6f).** Take the T-SEN-7 oracle with `q` identified at 1/2, and evidence boxes `Θ_v^(t) = [1/4 − 2^{−(t+2)}, 3/4 + 2^{−(t+2)}]`, which are strictly nested and infinitely many. Then `MMR_t = 1/4 + 2^{−(t+2)} > 1/4` for all `t` (computed exactly: 3/8, 5/16, 9/32, …). Rule A with `ε_R < 1/4` never fires. Rule C (weak or element stability) fires spuriously, since `M_t = {D,E}` is constant. Termination therefore requires either (i) finite evidence states (E.7), or (ii) a pre-registered budget/step cap, which yields a status such as `BUDGET_EXHAUSTED_UNRESOLVED` (an extension).

### (6) Synthetic benchmark protocol (and SIMULATED_ONLY sidecar)

**Protocol (pre-registrable).**

1. *Instance generator (synthetic only):* `K` scale blocks on `[0,1]` and `N` candidates with integer multilinear coefficients, plus optionally slacks for (Ad) studies. The ground truth `θ*` is drawn on a finite lattice, which gives finite evidence states (E.7).
2. *Evidence model:* measuring `p` reveals `θ*_p` (full identification, v2.2 conditioning). Variant: dyadic halving (`𝓔_p` = halves; EXTENSION).
3. *Policies:*
   - **FULL**: measure all blocks in registry order, then decide.
   - **VOI-vertex**, **VOI-grid(n)** (nested `n` across runs) and **VOI-exact** (E.4(a)): argmax VOI, ties broken by registry order.
   - **RANDOM**: seeded order.
4. *Stopping:* rule A with `ε_R ∈ {0 (= rule B), 0.1·MMR_0}`. Optionally rule D with registered `κ_p` (extension).
5. *Metrics:*
   - number of blocks measured;
   - MMR evaluations (solve count);
   - final `d*` and final `MMR_T`;
   - **realised regret** `F^*_C(θ*) − F(d*_T, θ*)`. A sanity invariant must hold: realised regret ≤ `MMR_T`, since `θ* ∈ Θ^(T)`;
   - share of runs whose realised value equals FULL's;
   - (Ad) only: count of `CANDIDATE_SET_EXPANDED` events and MMR increases.
6. *Reporting:* means and maxima over seeds, the generator and seeds, a SIMULATED_ONLY label, and no enterprise interpretation.

**Sidecar run (SIMULATED_ONLY; fixed C; K = 4, N = 6; 50 seeded instances).** The full output is in `Q\work\E\VOI_SIDECAR_SIMULATED_ONLY.json`. The run asserts at every step that MMR is non-increasing (E.1) and that realised regret ≤ final MMR; both assertions held.

| ε_R | Policy | mean blocks measured | mean MMR evaluations (solve count) | mean final MMR | mean / max realised regret | realised value = FULL |
|---|---|---|---|---|---|---|
| 0 (rule B) | FULL | 4.00 | 5.0 | 0 | 0 / 0 | 100% |
| 0 | VOI-vertex | 2.92 | 20.7 | 0 | 0 / 0 | 100% |
| 0 | VOI-grid8 | 2.92 | 79.5 | 0 | 0 / 0 | 100% |
| 0 | VOI-exact | 2.92 | 2001.7 | 0 | 0 / 0 | 100% |
| 0 | RANDOM | 3.26 | 4.3 | 0 | 0 / 0 | 100% |
| 0.1·MMR_0 | FULL | 4.00 | 5.0 | 0 | 0 / 0 | 100% |
| 0.1·MMR_0 | VOI-vertex | 2.58 | 19.4 | 0.155 | 0.018 / 0.5 | 94% |
| 0.1·MMR_0 | VOI-grid8 | 2.56 | 74.3 | 0.183 | 0.018 / 0.5 | 94% |
| 0.1·MMR_0 | VOI-exact | 2.56 | 1947.9 | 0.183 | 0.018 / 0.5 | 94% |
| 0.1·MMR_0 | RANDOM | 3.00 | 4.0 | 0.127 | 0.001 / 0.047 | 98% |

All rows are SIMULATED_ONLY: 50 instances, generator seeds 1000+s, RANDOM-order seeds 5000+s.

- **Blocks measured.** On these instances, VOI-guided ordering measured fewer blocks than RANDOM and FULL: 2.92 against 3.26 and 4 at ε_R = 0.
- **Solve count.** The price was many more MMR evaluations. VOI-exact was about 400× FULL, because the line-arrangement enumeration is large.
- **Stopping at ε_R > 0.** Rule A stops with positive MMR. Realised regret then stays within MMR, and the invariant held. In this sample, the VOI policies ended with a *larger* final MMR and realised regret than RANDOM. Stopping earlier means accepting more residual regret, so measurement count and residual regret trade off.
- **Vertex vs exact ranking.** Vertex VOI and exact VOI chose the same blocks in almost all runs here. W6 shows they can differ.

*Reading (synthetic regression, not evidence of anything enterprise-related):* the sidecar only illustrates the protocol mechanics and the E.1/E.2 invariants on random multilinear instances. It does not establish that VOI-guided ordering is better than random in general. That would need a theorem, and VOI-greedy optimality is NOT_PROVEN (W6e is a myopic failure).

---

## 7. Citation positioning (TYPE A / B / C)

| Claim | Type | Source (only references already in the manuscript list, or flagged) |
|---|---|---|
| Minimax-regret criterion as a decision rule | TYPE B (conceptual anchor) | Savage (1951) — in list, PARTIAL attribution (59a App. B N34; secondary sources only) |
| Set-based (uncertainty-set) robustness; product polytopes as uncertainty sets | TYPE B | Ben-Tal, El Ghaoui & Nemirovski (2009) — in list (N32) |
| Evaluating decisions across many plausible futures instead of one forecast | TYPE B | Lempert et al. (2003) — in list (N33) |
| Option value of information acquisition / staged investment (dynamic layer only) | TYPE B | Benaroch & Kauffman (1999) — in list; already cited in 42 §16 (D2) |
| Classical (expected) value of information; value of perfect information | TYPE B, **to verify** | e.g. Howard (1966) "Information value theory", Raiffa & Schlaifer (1961). **Not in the manuscript list; bibliographic details must be verified before use.** v2.2's VOI is *not* the expected-value VOI (there is no prior, 42 §17 D7). It is a worst-case MMR reduction, so these works can only be cited as a contrast. |
| Minimax-regret robust combinatorial optimization (interval data) | TYPE B, **to verify** | e.g. Kouvelis & Yu (1997); Averbakh's work on interval minmax regret. **Not in the list; verify.** |
| Lemma 0, E.2, E.3, E.10 | **Restatement-level** (42 l.535, §13.5, l.590; Lemma R) | 42 v2.2 |
| E.1, E.4, E.5, E.6, E.7; counterexamples W6–W6f; the (F)/(Ad)/(♯) trilemma | **TYPE C (in-model formalization; known analogues: minimax-regret menu dependence — Chernoff, Stoye; VOI complementarity / non-submodularity of information value — TO VERIFY)** | In-model results of this thesis. They must not be written as "according to X". Contribution to stress: E.6(e), E.7/E.8 |
| Minimax-regret violates IIA / menu dependence; axioms of minimax regret | TYPE B, **to verify** | Chernoff (year as named in Q/11; unverified); Stoye (minimax-regret axiomatization). **Not in the list; verify before citing; no details asserted.** |

No TYPE A claim is made: no cited work in the list directly establishes any of E.1–E.10 for this model.

---

## 8. Relation to P1–P8, Lemma E′, and scope

- **P1–P8 and Lemma E′** are untouched. VOI and SIP operate on Model B's whole-portfolio regret over a registered group. They do not change feasibility sets, envelopes (Lemma E′), or orderings (P1). P4 thresholds (`F_c^†`) are scalar break-evens, and a VOI over an `F_c` block is consistent with them. When the `F_c` interval straddles `F_c^†`, its VOI is positive, matching 59a §3.14's priority level (3). That is a qualitative remark, not a proved equivalence (NOT_PROVEN as a general statement).
- **P7 (ii) robust feasibility channel:** Lemma 5.1 and W6b show that this channel interacts with the regret benchmark. Narrowing `Θ` (evidence) can convert CONDITIONALLY_FEASIBLE portfolios into ROBUSTLY_FEASIBLE ones. This is value-creating in the model, but it raises MMR under (Ad).
- **Model C:** excluded. 42 §13.3 item 2 states that the leader value is not multilinear, so Lemma 0 fails and all MMR values are enumeration-based, with coverage only. E.1 and E.2 (fixed `C`) do not use multilinearity for their inequalities and so would hold for *exact* MMR values in C. But the exact values are not computable by vertices, and the computed ones are sample-based. **No claim about C is made.**
- **Element level:** excluded (42 §13.3 item 1). SIP stops on whole-portfolio quantities. Element stability in rule C is a heuristic only.
- **AI-specificity (T7 per Q/11 A11):** nothing here uses AI-specific structure. SIP, VOI and the E-results hold for any block-multilinear portfolio model with a registered uncertainty set; they are not AI-specific findings.
- **No contradiction with v2.2:** every v2.2 VOI statement (42 §13.5; 59a §3.13: "both are upper bounds on the true value, the grid version is no larger than the vertex version") is proved here **under the fixed candidate set that 51 uses**. The new findings concern conventions v2.2 does not state: the adaptive candidate set, the meaning of grid refinement, and probability blocks with ≥ 3 vertices.

**Suggested manuscript integration (59a §3.13, VOI paragraph; text for the integrator, not applied):** append "(for a fixed candidate set; if the candidate set is recomputed after narrowing, MMR may increase and VOI may be negative — counterexample in Appendix C)". In §4.9/§5.7, add the SIP as a *protocol* (no enterprise run), with Theorem E.7's finite-evidence premise stated explicitly.

---

## 9. NOT_PROVEN / open items (explicit)

1. **VOI-greedy optimality.** It is not proved that argmax-VOI minimizes the number of measurements or the final regret. W6e shows myopic failure, and no approximation guarantee is claimed.
2. **A convention that is adaptive, monotone and vertex-exact at once.** Its existence or impossibility is not shown. The table in §5 covers only three conventions.
3. **The exact sharp benchmark `MMR^♯`.** Vertices are insufficient (W6d). Cell enumeration over feasibility breakpoints is plausible but not proved here. The witness uses a grid, which is a lower bound.
4. **The converse of E.5.** Not proved.
5. **E.4(b) complexity and implementation.** Proved in principle; not implemented and no bound given.
6. **Rule C.** No guarantee of any kind (W6f).
7. **The expected-value VOI.** Not definable in v2.2 (no prior; 42 §17 D7) and not pursued.

---

## 10. Witness ↔ source-test mapping (Q\witness_parts\w_voi.py)

| Witness | Claim | Source test / v2.2 locus | Result | Minimality |
|---|---|---|---|---|
| W6 | Vertex VOI overstates (1 vs 1/2); guarantee failure at `v = 1/2` | 51 `t_sen7_regret_voi` (1), L2544–2555; 42 §13.5 L590 | PASS | 2 candidates × 2 blocks (`X=v`, `Y=q`); one block or one candidate cannot overstate |
| W6b | (Ad): MMR 0 → 1 under narrowing; `VOI_q = −1`; (F): 0 and 0 | 51 `solve_robust` L1435–1465, T-SEN-4; 42 §13.3 L549–558 | PASS | 2 portfolios; 1 block suffices for the MMR increase (0 → 3/5); 2 blocks are needed for negative VOI |
| W6c | Nested monotone; grid 4 → 5 moves 1/2 → 3/5; edge-only grid ≥ 1/2 vs true 1/3 | 51 `block_values` L1363–1377, T-SEN-7 `vg9`; 42 §13.5 L591 | PASS | grids 4 and 5; a probability block needs ≥ 3 vertices |
| W6d | Sharp benchmark: monotone, vertex value 0 vs true 1/2 | 42 L535 ("for a fixed candidate set"); 51 `regret_table` ScopeError | PASS | 1 block, 2 portfolios |
| W6e | `VOI_v = VOI_q = 0`, joint identification → MMR 0 | 42 §13.5 (single-block VOI); new | PASS | 2 candidates × 2 blocks |
| W6f | Strictly nested boxes, MMR > 1/4 for all t | 42 §16 (D2) `Θ_{t+1} ⊂ Θ_t`; new | PASS | 1 open block |
