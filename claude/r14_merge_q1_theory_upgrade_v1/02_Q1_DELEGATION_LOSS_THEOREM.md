# 02 — Q1 Delegation Loss Theorem (Task B, theory agent T1)

**Status:** Q1 theory-upgrade candidate, 2026-10-14. Additive to canonical v2.2. 42 and 51 were not modified.
**Evidence class:** the lemmas, corollaries and propositions below come with complete proofs (TYPE C = in-model formal results of this thesis; several are restatements of v2.2 facts, see "Restatement vs new" below, and the mechanism has known analogues in the delegation literature, §7). The witnesses (`witness_parts/w_dl_gov.py`) are *constructive examples* and *synthetic regressions*. They show that something exists or refute a universal claim. They are never used to prove a universal claim. All numbers are SIMULATED_ONLY algebra: no enterprise parameters, no V7, no coder data.

**Verdict lines**

```
DL_IFF_THEOREM                      = PROVEN only as Lemma DL-1o / DL-1p, a FIRST-BEST-RELATIVE IMPLEMENTABILITY CHARACTERIZATION LEMMA
                                      (= 42 Lemma E' applied to a first best + the definition DL = F^B - F^C; restatement-level).
                                      Primitive iff: NOT_PROVEN in general (impossible as a Boolean combination of (A)-(F), W3c);
                                      primitive pairwise iff under a unique first best: Cor DL-3 (genuinely new)
DL_IFF_IN_PAIRWISE_PRIMITIVES_A_F   = IMPOSSIBLE for Boolean combinations of the existential predicates (A)-(F) as defined in §1
                                      (W3c: all of (A)-(F) take identical truth values in I1 and I2, yet DL=2 vs DL=0); not claimed for "pairwise primitives" in general
DL_1_UNDER_TIE_TOLERANCE            = QUALIFIED [T8-fix]: PROVEN for every tie rule {F_u >= g(m)} with g non-decreasing, g(m) <= m (covers 51's l.673 rule)
                                      ONLY under exact affordability a(x) <= e (§2.2); 51's +1e-9 affordability slack (l.667) NOT covered (T8 2-plan
                                      counterexample, Q/15 §1.2); Cor DL-2...DL-5, Lemma S, Lemma I (04), GS-N (03) remain exact-tie results
MISALIGNMENT_NECESSARY              = YES for ledger-or-feasibility misalignment (AL1-AL4 incl. AL3); ledger misalignment alone NOT necessary (W_DL_AL3)
MISALIGNMENT_SUFFICIENT             = NO (W2)
STRICT_REVERSAL_NECESSARY           = YES for DL_opt UNDER AL3 (no unit-only constraints; Cor DL-2o, relative to the follower best-response set);
                                      without AL3, DL may arise from the AL3 channel alone, with no reversal (W_DL_AL3); NO for DL_pess (W3b), where weak reversal (tie) is necessary
REVERSAL_SUFFICIENT                 = NO (W2)
ENVELOPE_NON_SEPARABILITY_NECESSARY = YES UNDER AL3 (no unit-only constraints; Lemma DL-1: every deviation that matters satisfies a(x^H) <= a(x*_u));
                                      without AL3, DL may arise from the AL3 channel alone (W_DL_AL3)
NON_SEPARABILITY_SUFFICIENT         = NO (pairwise); YES jointly over all first-best solutions (Lemma DL-1)
REVERSAL+NON_SEPARABILITY_SUFFICIENT= NO pairwise (W3c, W4 under g_req); YES against a unique first best (Cor DL-3)
DL_OPT=0<DL_PESS                    = YES, minimal witness W3b (1 BU, 2 plans, tie)
T-ORC-8 reproduction                = PASS (W1 30/30, W2 15/15, W3 15/10/DL 5; A=C0=A+=0; opt=pess)
```

**Restatement of v2.2 vs genuinely new (TYPE C), consistent with the red-team report Q/11 §1 A1–A2, §3** (added 2026-10-15, T7):

| Restatement / specialization of v2.2 (label honestly; no new content) | Genuinely new in-model content (TYPE C) |
|---|---|
| **Lemma DL-1o/p**: 42 Lemma E′ (§12.4) applied to a first-best plan, plus the definition `DL = F^B − F^C`; it formalizes the P2 remark (42 l.628) with the correct quantifier ("every first best"). Near-tautological. | **Cor DL-2o** (the `ΣF_u`-maximal first-best selection forces a strict reversal against the best-response set; under AL3) |
| `DL ≥ 0` and `DL^opt ≤ DL^pess` (P1, P3: built in by construction under complete information) | **Cor DL-3** (primitive pairwise iff under a unique first best, with the separate AL3 clause) |
| **Lemma S** (envelope separability ⇔ `a(x^H) ≰ a(x^G)`): a two-line fact | **W3c** (no Boolean combination of the predicates (A)–(F) decides the sign of DL) |
| Opt/pess gap W3b as a phenomenon (standard optimistic/pessimistic bilevel gap; Wiesemann et al., 2013, in list) — only the minimal witness is new | **Prop DL-6** (envelopes are ceilings: under AL3, cheaper-or-equal plans cannot be blocked; plus the AL3 channel), **DL-4** (sufficient conditions, repaired proof), **DL-5** (computable bound) |
| | **§2.2** tie-tolerance version of DL-1 (repaired pessimistic shrink; covers 51's relative `ε_tie`) and the 42 l.476 erratum candidate (Q/13) |

---

## 0. Exact v2.2 sources relied on (quoted from 42, read-only)

| Item | 42 location | Content used |
|---|---|---|
| Leader instruments | §4.1, l.147–151 | `b = (y, γ, e)`, `y ∈ {0,1}^{|C|}`, `γ ∈ Γ`, `e = (e_u^h)_{u∈U,h∈H^pool}` |
| Follower variables | §4.2, l.157–161 | `x_u = (q_u, y^loc_u)`; `y^loc_uc = 1` only if `Allow^loc_γ(u,c)=1` |
| Pooled resource, bilevel | §5.1 (R1′), l.222–230 | leader: `Σ_c a^h_c y_c + Σ_u e^h_u + 1[h=BUD]ΔC^gov(γ) ≤ Ā^h`; unit: `Σ_c a^{h,loc}_{uc} y^loc_uc + Σ_{j∈J_u}Σ_k q_jk a^h_jk ≤ e^h_u` |
| Enterprise objective | §7.4 (OBJ-E), l.297 | `F_E = Σ q φ_jk(ȳ,s) − Σ_c F_c(y_c−y^cur_c) − Σ_u Σ_c F^loc_uc y^loc_uc − ΔC^gov(γ)` |
| Unit objective | §8.1 (OBJ-U), l.318–324 | `F_u(x_u | y,γ) = Σ q φ^u_jk(ȳ) − Σ_c F^loc_uc y^loc_uc` |
| Unit feasible set | §8.1, l.333–335 | `X_u(y,γ,e_u;θ) = {x_u : (F1)–(F10), (R1′) unit part, (R2), unit-only constraints, y^loc ≤ Allow^loc}` |
| Alignment | §8.2 (AL1)–(AL4), l.339–346 | AL3: "no unit-only constraints, or they are also in the enterprise problem" |
| DL | §11.1, l.431 | `DL = F_E^B − F_E^C` (optimistic and pessimistic bounds), `≥ 0` (P1) |
| Follower response | §12.3, l.455–464 | `X*_u(y,γ,e_u) = argmax F_u` (tolerance `ε_tie`); `φ^opt_u = max_{X*_u}[Σ q φ − Σ F^loc y^loc]`, `φ^pess_u = min` |
| Lemma E′ | §12.4, l.466–478 | `E′_u = {a(x_u) : x_u ∈ 𝒫_u}` suffices for both opt and pess |
| Leader C | §12.5, l.480–494 | knapsack over `e_u`; max over `(y,γ)`; opt and pess each maximized separately |
| Model B | §12.6, l.498 | enumerate `(y,γ)`, replace (OBJ-U) by the enterprise contribution, same knapsack |
| P1, P2 (+remark), P3 | §15, l.614–630 | ordering; alignment ⇒ zero DL; "misalignment necessary, not sufficient … envelope cannot separate it"; complete information |

**Tie convention.** 42 §12.3 uses a relative tolerance `ε_tie` (default `1e-9`). All results below use exact ties (`ε_tie = 0`) unless stated otherwise. The witnesses use integer data, so their ties are exact. §2.2 extends Lemma DL-1 (only DL-1) to tolerant tie rules, including 51's relative rule.

---

## 1. Formal setup (mapped to v2.2)

Fix `θ`. For each leader pair `(y,γ) ∈ {0,1}^{|C|} × Γ` and unit `u ∈ U`:

* **Plan sets.** `P^C_u(y,γ)` is the set of `x_u` that satisfy every constraint of `X_u` (42 l.334) **except** the envelope constraint. `P^B_u(y,γ)` is the same set with the unit-only constraints removed. So `P^C_u ⊆ P^B_u`, with equality iff AL3 holds. (51 implements no unit-only constraints, so `P^C = P^B` in every 51 test.) *Convention note (Q/11 §2.4):* dropping unit-only constraints from `P^B` is a convention; 42 AL3 (l.343) also allows them to be "in the enterprise problem". If a unit-only constraint is an operational fact (e.g. a service floor `s^min`), a planner that ignores it inflates `F^B` and hence DL. Every statement below that uses the AL3 channel (W_DL_AL3, the `P^C` clause of Cor DL-3, the third source in DL-6) holds under this convention; under the alternative convention (unit-only constraints also in B) that channel disappears.
* **Resource vector.** `a_u(x) ∈ ℝ^{H^pool}` is the left side of the unit part of (R1′) (42 l.229). It can have negative components (42 l.212).
* **Follower objective.** `F_u(x | y,γ)` (OBJ-U). **Enterprise contribution.** `φ^E_u(x | y) := Σ_{j∈J_u}Σ_k q_jk φ_jk(ȳ,s) − Σ_c F^loc_uc y^loc_uc`, the bracket of 42 l.462.
* **Leader cost and budget.** `K(y,γ) := Σ_c F_c(y_c − y^cur_c) + ΔC^gov(γ)` and `b̄(y,γ) := Ā − Σ_c a_c y_c − 1_BUD ΔC^gov(γ)`.
* **Model B (first best).** `F^B = max { Σ_u φ^E_u(x_u) − K(y,γ) : x_u ∈ P^B_u(y,γ), Σ_u a_u(x_u) ≤ b̄(y,γ) }`. A maximizer `(y*,γ*,x*)` is a **first-best solution**, and `𝓑*` is the (finite) set of all of them.
* **Model C.** The follower best-response set is `BR_u(e | y,γ) := argmax { F_u(x) : x ∈ P^C_u(y,γ), a_u(x) ≤ e }`, which is X*_u of 42 l.458. A leader triple `(y,γ,e)` is admissible if `Σ_u e_u ≤ b̄(y,γ)` and every `BR_u ≠ ∅`. Its value is `V^opt(y,γ,e) = Σ_u max_{BR_u} φ^E_u − K` and `V^pess = Σ_u min_{BR_u} φ^E_u − K`. Then `F^{C,m} = max V^m` for `m ∈ {opt, pess}` (42 §12.5 step 4).
* **Delegation loss.** `DL^m = F^B − F^{C,m}`. By P1, `0 ≤ DL^opt ≤ DL^pess`. The second inequality holds because `V^pess ≤ V^opt` pointwise.

**What the C leader controls:**
* `y`: shared capabilities, common to all units. It changes `P_u` through (F4) and (F5e), and changes `F_u` and `φ^E_u` through `ȳ`, `s`, and `τ`.
* `γ`: chosen only from the finite menu `Γ`. It sets Allow, Allow^loc, `G_j(γ)`, `J^must`, `J^forbid`, the requirement tables, `ē`, and `ΔC^gov`. One `γ` applies to all units.
* `e`: pooled-resource envelopes only (`H^pool`, e.g. BUD and ENG).

The leader does **not** control `q_u`, `y^loc_u` (beyond Allow^loc), the unit's own REV capacity (R2), or unit-only constraints. The envelope is a **ceiling**: it can remove plans but never compel one. Only `γ` can compel (F10, `J^must`).

**Separability notions.** Fix `(y,γ)`, a unit `u`, and two plans `x^H, x^G ∈ P^C_u(y,γ)`.
* *Envelope-separable:* some envelope `e` admits `x^G` and excludes `x^H`.
  **Lemma S.** `(x^H, x^G)` is envelope-separable ⇔ `a_u(x^H) ≰ a_u(x^G)`, i.e. `x^H` uses strictly more of at least one pooled resource. *Proof.* (⇐) Take `e = a_u(x^G)`. (⇒) If `a(x^H) ≤ a(x^G) ≤ e`, then every `e` that admits `x^G` also admits `x^H`. ∎
* *Policy-separable:* some `γ′ ∈ Γ` has `x^G ∈ P^C_u(y,γ′)` and `x^H ∉ P^C_u(y,γ′)`. *Capability-separable:* defined the same way with `y′`.
* *Joint (instrument-set) separability* cannot be defined pairwise, because `y` and `γ` are common to all units and also carry cost `K`. A policy or capability that separates `x^H` from `x^G` for unit `u` can destroy another unit's first-best plan (W3, W4b–W4c) or cost `ΔC^gov`. The right joint object is the first-best solution:
  **Definition (self-enforcing first best).** `(y*,γ*,x*) ∈ 𝓑*` is *opt-self-enforcing* if, for every `u`, `x*_u ∈ P^C_u(y*,γ*)` and `x*_u ∈ BR_u(a_u(x*_u) | y*,γ*)`. It is *pess-self-enforcing* if, in addition, `min_{x∈BR_u(a_u(x*_u))} φ^E_u(x) ≥ φ^E_u(x*_u)` for every `u`.
  The **joint non-separability condition (C\*)** says: *no* first-best solution is self-enforcing. Policy and capability alternatives are covered automatically: if some `(y′,γ′)` screens the bad plan and still attains `F^B`, it is itself an element of `𝓑*`.

**Candidate conditions (precise).** All are evaluated on `P^C_u(y,γ)`.
* (A) *Ledger sign disagreement:* there exist `x, x′` with `sign(F_u(x)−F_u(x′)) ≠ sign(φ^E_u(x)−φ^E_u(x′))` (ties count as sign 0).
* (B) *Strict preference reversal:* `F_u(x^H) > F_u(x^G)` and `φ^E_u(x^H) < φ^E_u(x^G)`.
* (B_w) *Weak reversal:* `F_u(x^H) ≥ F_u(x^G)` and `φ^E_u(x^H) < φ^E_u(x^G)`. This includes the tie case (D).
* (C) *Envelope non-separability* of the pair: `a_u(x^H) ≤ a_u(x^G)`.
* (D) *Follower tie:* `F_u(x^H) = F_u(x^G)` and `φ^E_u(x^H) ≠ φ^E_u(x^G)`.
* (E) *Coupling across BUs:* (E1) the pooled budget `b̄`; (E2) the shared capability `y`; (E3) the common policy `γ`.
* (F) *Policy/feasibility interaction:* `P^C ⊊ P^B` (AL3 fails), or `γ` changes `P_u`.

---

## 2. Main characterization lemma (restatement-level; TYPE C in-model)

*Label (T7, per Q/11 A1–A2):* DL-1 is a **first-best-relative implementability characterization lemma**: 42 Lemma E′ applied to a first best, plus the definition of DL. It is not a primitive iff and is not presented as a headline theorem. The genuinely new DL content is Cor DL-2o, Cor DL-3, W3c and DL-6 (table above).

**Lemma DL-1o (optimistic characterization) [multi-BU].** `DL^opt = 0` ⇔ some first-best solution is opt-self-enforcing. Equivalently, `DL^opt > 0` ⇔ for **every** `(y*,γ*,x*) ∈ 𝓑*` there is a unit `u` such that either `x*_u ∉ P^C_u(y*,γ*)`, or there is `x^H ∈ P^C_u(y*,γ*)` with `a_u(x^H) ≤ a_u(x*_u)` and `F_u(x^H) > F_u(x*_u)`.

**Lemma DL-1p (pessimistic characterization) [multi-BU].** `DL^pess = 0` ⇔ some first-best solution is pess-self-enforcing. Equivalently, `DL^pess > 0` ⇔ for every `(y*,γ*,x*) ∈ 𝓑*` there is a unit `u` such that either `x*_u ∉ P^C_u`, or some `x^H ∈ BR_u(a_u(x*_u))` has `φ^E_u(x^H) < φ^E_u(x*_u)`. Such an `x^H` automatically satisfies `a(x^H) ≤ a(x*_u)` and `F_u(x^H) ≥ F_u(x*_u)`.

*Proof (both modes).* Two steps.

**(⇐)** Let `(y*,γ*,x*)` be self-enforcing and set `e_u := a_u(x*_u)`.
* The triple is admissible: `Σ_u e_u = Σ_u a_u(x*_u) ≤ b̄(y*,γ*)` because `x*` is B-feasible, and `x*_u ∈ BR_u(e_u)`, so `BR_u ≠ ∅`.
* Opt: `max_{BR_u} φ^E_u ≥ φ^E_u(x*_u)` because `x*_u ∈ BR_u`.
* Pess: `min_{BR_u} φ^E_u ≥ φ^E_u(x*_u)` by definition.
* So `F^{C,m} ≥ V^m(y*,γ*,e) ≥ Σ_u φ^E_u(x*_u) − K = F^B`. With P1 this gives `DL^m = 0`.

**(⇒)** Let `DL^m = 0`, and let `(y,γ,e)` attain `F^{C,m} = F^B`.
* **Opt.** For each `u`, choose `x̂_u ∈ BR_u(e_u)` attaining the `max` of `φ^E_u` over `BR_u(e_u)`. Then `x̂_u ∈ P^C_u ⊆ P^B_u` and `Σ a_u(x̂_u) ≤ Σ e_u ≤ b̄`, so `(y,γ,x̂)` is B-feasible with value `F^{C,opt} = F^B` and belongs to `𝓑*`. Shrink step: `x̂_u` is `F_u`-maximal on `{a ≤ e_u}` (exact ties), and `{a ≤ a(x̂_u)}` is a subset that still contains `x̂_u`, so `x̂_u ∈ BR_u(a(x̂_u))`: opt-self-enforcement.
* **Pess (repaired, T7 per Q/11 A5/§2.7).** Let `μ_u := min_{BR_u(e_u)} φ^E_u`, so `Σ_u μ_u − K = F^B`. For each `u`, choose `x̃_u ∈ BR_u(e_u)` with `F_u(x̃_u) = max_{a≤e_u} F_u` (an `F_u`-maximal element of the tie set; under exact ties every element of `BR_u(e_u)` qualifies). Shrink step: `{a ≤ a(x̃_u)} ⊆ {a ≤ e_u}` still contains the maximizer `x̃_u`, so the maximum is unchanged and `BR_u(a(x̃_u)) = BR_u(e_u) ∩ {a ≤ a(x̃_u)} ⊆ BR_u(e_u)`. Hence `min_{BR_u(a(x̃_u))} φ^E_u ≥ μ_u`. *Per-unit sum argument:* `φ^E_u(x̃_u) ≥ μ_u` for every `u` (since `x̃_u ∈ BR_u(e_u)`), and the profile `x̃` is B-feasible (`P^C ⊆ P^B`, `Σ a(x̃_u) ≤ Σ e_u ≤ b̄`), so `Σ_u φ^E_u(x̃_u) − K ≤ F^B = Σ_u μ_u − K`. Therefore `φ^E_u(x̃_u) = μ_u` for every `u`, `(y,γ,x̃) ∈ 𝓑*`, and `min_{BR_u(a(x̃_u))} φ^E_u ≥ μ_u = φ^E_u(x̃_u)`: pess-self-enforcement.
* (The earlier text chose `x̂_u` as the `φ`-minimizer of `BR_u(e_u)`. Under exact ties that is also valid, because every tie-set element is `F_u`-maximal; under a tolerant tie rule it is not, see §2.2.)

The "equivalently" forms are the negations. For pess, take `x^H ∈ BR_u(a(x*_u))`. Then `a(x^H) ≤ a(x*_u)` by affordability, and `F_u(x^H) ≥ F_u(x*_u)` because `x*_u` is affordable at that envelope. ∎

**Relation to v2.2.** The proof is Lemma E′ applied to a first-best plan; DL-1 is therefore a characterization lemma (restatement-level), not a new theorem. DL-1 is the formal version of the P2 remark (42 l.628): "misalignment is necessary but not sufficient … DL>0 only when the enterprise-unfavourable configuration remains affordable within the envelope the enterprise must give". DL-1 states that remark exactly, with the correct quantifier: *every* first best.

### 2.1 Corollaries

**Cor DL-2o (strict reversal relative to the best-response set is necessary for DL^opt > 0) [multi-BU, AL3].** Suppose `DL^opt > 0` and `P^C = P^B`. Take any `(y*,γ*)` that supports a first best, and among the first-best profiles at `(y*,γ*)` pick `x°` maximizing `Σ_u F_u(x°_u)`. Then some unit `u` has a nonempty `BR_u(a(x°_u))`, and **every** `x^H` in it satisfies (B) and (C) against `x^G := x°_u`:
`F_u(x^H) > F_u(x°_u)`, `φ^E_u(x^H) < φ^E_u(x°_u)`, and `a(x^H) ≤ a(x°_u)`.

*Proof.* By DL-1o, `x°` is not opt-self-enforcing, so some `u` has `x°_u ∉ BR_u(a(x°_u))`. Each `x^H ∈ BR_u(a(x°_u))` has `a ≤ a(x°_u)` and `F_u(x^H) > F_u(x°_u)`. Suppose `φ^E_u(x^H) ≥ φ^E_u(x°_u)`. Replacing `x°_u` by `x^H` keeps the profile B-feasible (resources do not increase) and gives value `≥ F^B`. That is a first best at `(y*,γ*)` with larger `Σ F_u`, a contradiction. ∎

**Cor DL-2p (weak reversal is necessary for DL^pess > 0) [multi-BU, AL3].** If `DL^pess > 0`, then every first best `(y*,γ*,x*)` has a unit `u` and an `x^H ∈ BR_u(a(x*_u))` satisfying (B_w) and (C). *Proof:* DL-1p. ∎ Strict reversal is **not** necessary: W3b has DL^pess = 1 with only a tie.

**Cor DL-3 (iff in primitive pairwise form under a unique first best) [multi-BU; exact ties].** *Standing hypothesis (H0):* `𝓑* = {(y*,γ*,x*)}` (unique first best). *(Repaired T7 per Q/11 §2.3: the earlier draft assumed `x*_u ∈ P^C_u` for all `u` and then treated `x*_u ∉ P^C_u` in the same statement; the two cases are now separate parts with their own hypotheses.)*

**Part (i) — first best available in C.** Assume (H0) and, in addition, `x*_u ∈ P^C_u(y*,γ*)` for all `u`. Then:
* `DL^opt > 0` ⇔ some `u` and `x^H ∈ P^C_u(y*,γ*)` have `a_u(x^H) ≤ a_u(x*_u)` and `F_u(x^H) > F_u(x*_u)`.
* `DL^pess > 0` ⇔ some `u` and `x^H ≠ x*_u` in `P^C_u(y*,γ*)` have `a_u(x^H) ≤ a_u(x*_u)` and `F_u(x^H) ≥ F_u(x*_u)`.
* In both cases `φ^E_u(x^H) < φ^E_u(x*_u)` holds automatically. So under (H0) and Part (i)'s hypothesis, **DL>0 ⇔ (B) [opt] or (B_w) [pess] + (C) against the first-best plan.**

**Part (ii) — AL3 fails on the first best.** Assume (H0) and that some `x*_u ∉ P^C_u(y*,γ*)`. Then `DL^opt > 0` and `DL^pess > 0`.

*Proof of (i).*
* Automatic `φ` drop: swapping `x*_u → x^H ≠ x*_u` with `a(x^H) ≤ a(x*_u)` gives a different B-feasible solution (`x^H ∈ P^C_u ⊆ P^B_u`, resources do not increase). By uniqueness it is not optimal, so `φ^E_u(x^H) < φ^E_u(x*_u)`.
* Opt: DL-1o with `𝓑*` a singleton and `x*_u ∈ P^C_u`. `x*_u ∉ BR_u(a(x*_u))` ⇔ some affordable plan has strictly larger `F_u`.
* Pess (⇐): if such an `x^H` exists, either `x*_u ∉ BR_u` (then BR elements have `φ < φ(x*_u)` by the automatic drop), or `x*_u ∈ BR_u` and `F_u(x^H) = F_u(x*_u)` (then `x^H ∈ BR_u` with `φ < φ(x*_u)`). Either way the min falls below `φ(x*_u)`, and DL-1p gives `DL^pess > 0`.
* Pess (⇒): if no such `x^H` exists for any `u`, then `BR_u(a(x*_u)) = {x*_u}` for all `u`, so `x*` is pess-self-enforcing and DL-1p gives `DL^pess = 0`.

*Proof of (ii).* Suppose `F^{C,m} = F^B` for some `m`, attained at `(y,γ,e)`. Selecting any `x̂_u ∈ BR_u(e_u)` gives a B-feasible profile (`P^C ⊆ P^B`, `Σ a(x̂_u) ≤ b̄`) with value `≥ V^pess(y,γ,e)`; for `m = opt` take the `φ`-maximizers, for `m = pess` the per-unit sum argument of DL-1p (⇒). Either way `(y,γ,x̂)` attains `F^B`, so by (H0) it equals `(y*,γ*,x*)`. But `x̂_u ∈ P^C_u` for all `u`, while some `x*_u ∉ P^C_u`: contradiction. Hence `F^{C,m} < F^B` for both modes. ∎

*Re-verification against the witnesses (T7).* W3: unique first best (`y_c=1`, U1:k1, U2:k0), Part (i) applies; U2's `x^H = k1` has `a = (0,0) ≤ (0,0)` and `F_u = 20 > 0` ⇒ `DL^opt, DL^pess > 0` (computed DL = 5/5) ✓. W3b: unique first best `xG` (φ 1 > 0); no `x^H` with `F_u > 0` ⇒ `DL^opt = 0`; `xH ≠ xG` with `a = 0 ≤ 0`, `F_u = 0 ≥ 0` ⇒ `DL^pess > 0` (computed 0/1) ✓. W3c-I1 (= W3m): unique first best `xG`; `xH` has `a = 0 ≤ 1`, `F_u = 1 > 0` ⇒ DL > 0 (computed 2/2) ✓. W3c-I2: `xG` and `xM` are both first best (φ = 2), so (H0) fails and Cor DL-3 is silent; DL-1 applies (`xM` is self-enforcing; computed 0/0) ✓. W_DL_AL3: unique first best `xG` with `xG ∉ P^C` ⇒ Part (ii): `DL > 0` (computed 1/1) ✓. The falsification search below covered both parts.

*Falsification search (not a proof).* `work/B/fuzz_dl_gov.py` checked DL-1o/p on 1,358 random instances and Cor DL-3 on 2,221 unique-first-best cases (1–2 BUs, 0–1 capabilities, 2-dimensional pooled resources with negative components allowed). 0 violations. An early version of the check omitted the AL3 clause of Cor DL-3 and was "violated" exactly on instances where the unique first-best plan breaks a unit-only constraint. That clause is now part of the statement.

**Prop DL-4 (sufficient conditions for DL = 0) [multi-BU; AL3; exact ties].** All three parts assume AL3 (`P^C = P^B`); without it (b) and (c) fail (W_DL_AL3). [T8-fix]
* (a) **No weak reversal on non-separable pairs.** Suppose AL3 holds and, for every `(y,γ)`, `u`, and `x^H, x^G ∈ P^C_u` with `a(x^H) ≤ a(x^G)`, `F_u(x^H) ≥ F_u(x^G) ⇒ φ^E_u(x^H) ≥ φ^E_u(x^G)`. Then `DL^opt = DL^pess = 0`.
* (b) **No strict reversal on non-separable pairs.** If only `F_u(x^H) > F_u(x^G) ⇒ φ^E_u(x^H) ≥ φ^E_u(x^G)` holds on those pairs, then `DL^opt = 0`. `DL^pess` may be positive (W3b).
* (c) **Ordinal alignment.** If `F_u` and `φ^E_u` induce the same weak order on every `P^C_u` (weaker than AL1, AL2, AL4: e.g. `F_u = αφ^E_u + β`, `α > 0`), then (a) holds. P2 is the special case `F_u ≡ φ^E_u`.

*Proof (repaired T7 per Q/11 §2.1: direct bound `V^m(a(x*)) ≥ F^B`; the earlier text concluded that `x*` itself is self-enforcing, which fails when some affordable plan has strictly larger `F_u`).* AL3 holds, so `x*_u ∈ P^C_u`. Take any first best `(y*,γ*,x*)` and set `e_u = a(x*_u)`. The triple is admissible (`Σ e_u ≤ b̄`; `x*_u` is affordable, so `BR_u(e_u) ≠ ∅`). Every `x ∈ BR_u(e_u)` has `a(x) ≤ a(x*_u)` and `F_u(x) ≥ F_u(x*_u)` (exact ties; `x*_u` is affordable).
* Under (a): every `x ∈ BR_u(e_u)` has `φ(x) ≥ φ(x*_u)`. So `V^pess(y*,γ*,e) ≥ Σ_u φ(x*_u) − K = F^B`, and `V^opt ≥ V^pess`. With P1, `DL^opt = DL^pess = 0`.
* Under (b): if `max_{a≤e_u} F_u > F_u(x*_u)`, every `x ∈ BR_u(e_u)` has `F_u(x) > F_u(x*_u)`, hence `φ(x) ≥ φ(x*_u)`; otherwise `x*_u ∈ BR_u(e_u)`. Either way `max_{BR_u(e_u)} φ ≥ φ(x*_u)`, so `V^opt(y*,γ*,e) ≥ F^B` and `DL^opt = 0`.
(Equivalently, via DL-1: under (a), any `F_u`-maximal `x̃_u ∈ BR_u(e_u)` gives a self-enforcing first best; under (b), take `x̃_u = x*_u` when `max F_u = F_u(x*_u)`, and any element of `BR_u(e_u)` otherwise.) [T8-fix] ∎

**Prop DL-5 (computable upper bound) [multi-BU, AL3].** `DL^m ≤ min_{(y*,γ*,x*)∈𝓑*} Σ_u [φ^E_u(x*_u) − v^m_u(a(x*_u))]`, where `v^opt_u(e) = max_{BR_u(e)} φ^E_u` and `v^pess_u(e) = min_{BR_u(e)} φ^E_u`. Each summand is `≥ 0`.

*Proof.* The bound is the value of the admissible leader choice `e = a(x*)`. A summand cannot be negative: a BR element with `φ > φ(x*_u)` and `a ≤ a(x*_u)` would improve on `F^B`. ∎ The bound is attained in W3: U2's gap is `0 − (−5) = 5 = DL`.

**Prop DL-6 (the envelope is a ceiling) [multi-BU].** For any `e` admitting `x^G`, the admitted set contains `{x : a(x) ≤ a(x^G)}`. So an envelope can never remove a plan that is no more resource-intensive than the target. **Under AL3**, DL therefore comes from exactly two sources:
* **under-adoption**: the unit prefers a cheaper plan, e.g. the status quo, to an enterprise-preferred AI configuration (W3m);
* **cheap harmful adoption**: the unit prefers a plan that is no more expensive but enterprise-worse (W3, U2:k1 with `a = 0`).

**Without AL3** there is a third channel (added T7 per Q/11 §2.2): **unit-only exclusion** — a unit-only constraint removes the first-best plan from `P^C_u` even with `F_u ≡ φ^E_u` (W_DL_AL3; Cor DL-3 Part (ii); under the convention of §1 that B omits unit-only constraints).

None of these can be fixed by any `e`. Only `γ` (Allow/`J^forbid` to exclude, `J^must` to compel, requirements to screen) or `y` (removing a prerequisite) can act on the first two; the third is outside the leader's instruments as modelled. *Proof:* Lemma S for the first two; the third by definition of `P^C`. ∎

### 2.2 Tolerant tie rules: Lemma DL-1 and Lemma E′ under 51's relative `ε_tie` (added T7 per Q/11 A5, §2.7)

**Setting.** Exact affordability `S_u(e) = {x ∈ P^C_u : a_u(x) ≤ e}`, `m_u(e) = max_{S_u(e)} F_u`, and a tie rule `BR^g_u(e) = {x ∈ S_u(e) : F_u(x) ≥ g(m_u(e))}` with `g : ℝ → ℝ` **non-decreasing** and `g(m) ≤ m`. This covers exact ties (`g(m) = m`), any absolute tolerance (`g(m) = m − t`), and 51's relative rule (51 l.673: `g(m) = m − 10^{-9}·max(1,|m|)`, which has slope `1`, `1 − 10^{-9}` or `1 + 10^{-9}` on its three pieces, hence is increasing). `V^m`, self-enforcement and `F^{C,m}` are defined as in §1 with `BR^g` in place of `BR`.

**Shrink facts.** (S-weak) For any `x ∈ BR^g_u(e)`: `S_u(a(x)) ⊆ S_u(e)`, so `m_u(a(x)) ≤ m_u(e)` and `F_u(x) ≥ g(m_u(e)) ≥ g(m_u(a(x)))`, i.e. `x ∈ BR^g_u(a(x))`. But `BR^g_u(a(x))` may contain plans **not** in `BR^g_u(e)` (new near-ties below the old threshold). (S-max) If moreover `F_u(x̃) = m_u(e)`, then `m_u(a(x̃)) = m_u(e)` and `BR^g_u(a(x̃)) = BR^g_u(e) ∩ S_u(a(x̃)) ⊆ BR^g_u(e)`.

**Lemma E′ under `g` (statement of 42 §12.4 holds).** Opt: take `x` `φ`-maximal in `BR^g(e)`; by (S-weak) `x ∈ BR^g(a(x))`, so the opt value at `a(x)` is `≥ φ(x)` = the opt value at `e`. Pess: take `x̃` `F_u`-maximal in `BR^g(e)`; by (S-max) the pess value at `a(x̃)` is `≥` the pess value at `e`. Resource use does not increase in either case. ∎ The proof sentence of 42 l.476 ("取任一 `x ∈ T`") fails for the pessimistic case under any tie rule with `g` strictly increasing near `m` (every absolute tolerance and 51's relative rule) [T8-fix; for a locally constant step rule `g` no new near-ties appear]: shrinking to a non-maximal tie element can admit new near-ties (counterexample `x_top, x_hat, x_low`, pess value 10 → −100; Q/13). The statement survives with the `F_u`-maximal choice. 42 is **not** modified; see `13_Q1_CANONICAL_42_ERRATUM_CANDIDATE.md`.

**Lemma DL-1o/p under `g`.** Both statements hold verbatim with `BR^g`. *Proof.* (⇐) uses only the definitions (unchanged). (⇒) opt: as in §2 with (S-weak) in place of exact `F_u`-maximality. (⇒) pess: exactly the repaired argument of §2 — it uses only `x̃_u ∈ BR^g_u(e_u)`, (S-max), and the per-unit sum argument. ∎ *The "equivalently" primitive forms change:* `x*_u ∉ BR^g_u(a(x*_u))` ⇔ some `x^H ∈ S_u(a(x*_u))` has `g(F_u(x^H)) > F_u(x*_u)` (unit-preferred beyond tolerance); and an `x^H ∈ BR^g_u(a(x*_u))` satisfies `F_u(x^H) ≥ g(F_u(x*_u))`, not necessarily `F_u(x^H) ≥ F_u(x*_u)`.

**Scope of the upgrade.** (1) Exact affordability is assumed. 51's `unit_response` additionally admits `a ≤ e + 10^{-9}` (51 l.667, absolute slack on resources); that slack is not covered by this proof [T8-fix] (under 51's slack the unit at envelope `e` sees `{a ≤ e + 10^{-9}}`, so 51 evaluates the exact-affordability model at `e + 10^{-9}`; this coincides with offering `e` itself whenever no two distinct values of any pooled-resource coordinate across a unit's plans differ by a positive amount `≤ 10^{-9}`. Then 51 equals the exact model with budget `b̄ + 10^{-9}` in both B and C. Otherwise E′ can be inexact under 51's own semantics (T8 example, Q/15 §1: plan `x` with `a = 1 + 0.5·10^{-9}`, `F = 10`, `φ = 5`, and plan `bad` with `a = 1 + 1.2·10^{-9}`, `F = 20`, `φ = −100`; envelope `e = 1` gives 5, the best E′ envelope gives −100)). (2) Only Lemma E′ and DL-1o/p are upgraded. Cor DL-2o/2p, DL-3, DL-4, DL-5, Lemma S and the 04 implementability lemma (Lemma I) use strict/weak `F_u` comparisons and remain **exact-tie** results; GS-N (03) genuinely needs exact ties (`BR_s = BR_l ∩ P_s`). (3) 51's computed numbers are unaffected: `envelopes_lemmaE` enumerates every `a(x)`, including `a(x̃)`. *Falsification search (not a proof; T7 scratch `t7/tol_fuzz.py`, seed 7):* 20,000 random 1-resource instances with near-tie `F_u` values (gaps 0.4–2·10⁻⁹) under 51's relative rule: 0 violations of the Lemma E′ statement on an envelope grid, and 0 violations of DL-1o/p in 40,000 two-unit checks. The original exact-tie search `work/B/fuzz_dl_gov.py` was re-run after the Cor DL-3 restatement: 1,358 instances, 2,221 unique-first-best checks (both parts), 430 `GSV > 0` cases, 0 violations.

---

## 3. Answers to items 1–10

| # | Question | Answer | Status | Where |
|---|---|---|---|---|
| 1 | Is misalignment necessary for DL>0? | **Yes, if "misalignment" includes AL3.** DL>0 needs a weak reversal against a first-best plan (B_w)+(C) (Cor DL-2), or a first-best plan excluded by a unit-only constraint. Ledger misalignment (AL1, AL2, AL4) alone is **not** necessary: W_DL_AL3 (T1 part id "W5") has `F_u ≡ φ^E_u` and DL=1 (under the §1 convention that B omits unit-only constraints). Consistent with P2's corollary, which lists AL3. | Lemma + witness | DL-1, DL-2, DL-4c, W_DL_AL3 |
| 2 | Is misalignment sufficient? | **No.** W2: U2's ledger is reversed (`F_u(k1)=15 > 0`, `φ^E(k1)=−10 < 0`), but `a(k1)=(5,0) ≰ (0,0)`. The envelope `e_U2=(0,0)` blocks it and DL=0. Smallest form: 1 BU, `x^H=(a=1,F_u=1,F_E=−1)`, `x^G=(a=0,0,0)`. | Counterexample | W2 |
| 3 | Is preference reversal necessary? | **Opt: yes, strict reversal relative to the best-response set** at a `Σ F_u`-maximal first best (Cor DL-2o). A pairwise reversal anywhere in `P_u` is not the right object. **Pess: only weak reversal** (a tie suffices, W3b). | Theorem + counterexample | DL-2o/p, W3b |
| 4 | Is reversal sufficient? | **No** (W2). Even reversal plus envelope non-separability of a pair is not sufficient (W3c). | Counterexample | W2, W3c |
| 5 | Is non-separability necessary? | **Yes, under AL3.** Every deviation that creates DL satisfies `a(x^H) ≤ a(x*_u)` (DL-1). Without AL3, DL can arise from a unit-only constraint alone (W_DL_AL3). With full envelope separability of all reversing pairs, DL=0 (DL-4a). | Lemma (DL-1) + corollary [T8-fix] | DL-1, DL-4 |
| 6 | Is non-separability sufficient? | **No as a pairwise property** (no reversal; or a third plan `x^M` is the best response, W3c; or a screening policy exists in `Γ`, W4 under `g_req`). **Yes jointly**, as (C\*): no first best is self-enforcing ⇔ DL>0. | Counterexample / Lemma [T8-fix] | W3c, W4, DL-1 |
| 7 | Are reversal + non-separability sufficient? | **Pairwise: no** (W3c: the pair (xH,xG) is identical in I1 and I2; DL=2 vs DL=0). **Against a unique first best: yes, iff** (Cor DL-3). **In general: iff against every first best** (DL-1). | Lemma (DL-1) + corollary + counterexample [T8-fix] | DL-1, DL-3, W3c |
| 8 | What else is needed? | Five further conditions, each part of DL-1's "for every first best" quantifier. (i) **No screening instrument in the menu `Γ`:** if a `γ′` excludes `x^H`, keeps `x*`, and costs no more, then `(y*,γ′,x*) ∈ 𝓑*` is self-enforcing (W4 at `g_req`). (ii) **Resource availability:** `x^G` must be first-best given `b̄`; a reversal against a plan the budget would not fund anyway is irrelevant. (iii) **No equivalent alternative first best** that is self-enforcing (W3c-I2: `x^M`). (iv) **Tie-breaking:** opt needs a strict reversal, pess only a weak one (W3b). (v) **Portfolio coupling (E2/E3):** `y` and `γ` are common, so an instrument that separates for one unit may destroy another unit's first-best plan. In W3, `y_c=0` would block U2:k1 but costs U1's 25; in W4b and W4c a requirement that screens U2 prices out U1:k1. (E1), the pooled budget, does **not** by itself create DL: the first-best split `e_u=a(x*_u)` is always admissible. | Lemma (DL-1) + corollary + witnesses [T8-fix] | §1, §2 |
| 9 | Optimistic vs pessimistic results [T8-fix] | DL-1o/DL-1p, DL-2o/DL-2p, DL-3 (both modes). Always `DL^opt ≤ DL^pess`. Opt needs a strict reversal; pess needs a weak one. | Lemma + corollaries [T8-fix] | §2 |
| 10 | Can DL_opt=0 but DL_pess>0? | **Yes.** Minimal witness W3b: 1 BU, 1 resource, plans `xG=(a=0,F_u=0,F_E=1)` and `xH=(a=0,F_u=0,F_E=0)`. `B=1`, `C_opt=1`, `C_pess=0`. Minimal because a tie needs ≥2 plans and every other dimension is at its floor. v2.2 reading: both configurations have equal unit-ledger value, and `xG` carries enterprise-only value (`v^x>0` or avoided `l^x`). AL1 fails only through the tie. | Constructive example | W3b |

**Scope labels.** DL-1, DL-2, DL-3, DL-4, DL-5, and DL-6 are proven for any finite `U`, so [MULTI-BU]. W3m, W3b, W3c, and W_DL_AL3 are [SINGLE-BU] witnesses. A single-BU witness can only refute a universal claim; it cannot represent cross-BU coupling, which W3, W4b, and W4c show.

**v2.2 embedding of the single-BU minimal cores (T7 per Q/11 §2.13 item 3).** These cores are abstract finite bilevel instances, not literal v2.2 instances. W3m reads `xH = (a=0, F_u=1, φ=0)` as the status quo, which contradicts `φ^u_{j0} = φ_{j0} = 0` (42 V2/OBJ-U); the per-unit constant shift `F_u(xG) = −1, F_u(xH) = 0` gives a literal instance with the same best responses and the same B, C and DL values (a constant added to `F_u` changes no `argmax`). W3b and W3c-I2 read the same way (W3b: `xH = (0,0,0)` is literally the status quo). W_DL_AL3: `x0 = (0,0,0)` is literally the status quo.

---

## 4. Witnesses (`witness_parts/w_dl_gov.py`; all PASS)

All witnesses are computed by an engine written independently from the definitions (no import of 51). Each witness also checks two things:
* the Lemma E′ envelope set gives the same C values as the v2.1 product envelope set;
* DL-1's predicate (whether a self-enforcing first best exists) matches the computed sign of DL.

| ID | Inputs (algebraic) | B | C_opt | C_pess | DL (opt/pess) | Source-test mapping | Minimality |
|---|---|---|---|---|---|---|---|
| W1 aligned | U1:k1 `v_u=3,l_x=0,impl=5`; U2:k1 `v_u=2,l_x=0,impl=5`; N=10, F_c=10 | 30 | 30 | 30 | 0/0 | 51 T-ORC-8 "aligned" `hand_instance(5,0)` | not minimal; T-ORC-8 dimensions kept |
| W2 blockable | U2:k1 `l_x=2.5, impl=5` | 15 | 15 | 15 | 0/0 | T-ORC-8 "blockable" `(5,2.5)` | core: 1 BU, 2 plans |
| W3 unblockable | U2:k1 `l_x=2.5, impl=0` | 15 | 10 | 10 | 5/5 | T-ORC-8 "unblockable" `(0,2.5)` | core is W3m; 2 BUs + `c` add the capability-coupling reading |
| W3m | `xG=(a=1,F_u=0,F_E=2)`, `xH=(a=0,1,0)`, Ā=1 | 2 | 0 | 0 | 2/2 | new | minimal |
| W3b | `xG=(0,0,1)`, `xH=(0,0,0)` | 1 | 1 | 0 | 0/1 | new; related T-ORC-9 `tie_instance` | minimal |
| W3c | I1 = W3m; I2 = W3m + `xM=(1,2,2)` | 2 / 2 | 0 / 2 | 0 / 2 | 2 / 0 | new | one-plan extension |
| W_DL_AL3 (part id W5) | `F_u≡F_E`; `xG` violates a unit-only constraint | 1 | 0 | 0 | 1/1 | spec-level (42 §8.1–8.2; not in 51) | minimal |

All of W1–W3 also reproduce `A=C0=A+=0`, `VRA=DL0=VCP=0`, `VSC=B`, `NEV=C`, and opt=pess. That is every number asserted by `t_orc8_independent_hand`.

### 4.1 Mapping to T-ORC-8's three states

The fixture: `φ^E(U1:k1) = 10·3 − 5 = 25`, `φ^E(U2:k1) = 10(2 − l_x) − impl`, and `F_U2(k1) = 20 − impl`. Both AI configurations need `c` (`F_c=10`). The status quo has value 0 and `a = 0`.

| State | Unique first best | Reversal (B)? | `a(x^H) ≤ a(x^G)` (C)? | Cor DL-3 | Result |
|---|---|---|---|---|---|
| aligned (5, 0) | `y_c=1`, U1:k1, U2:k1 (25+15−10=30) | none (`F_u ≡ φ^E`) | — | no deviation | DL = 0 |
| blockable (5, 2.5) | `y_c=1`, U1:k1, U2:k0 (25−10=15) | U2: `F_u(k1)=15>0`, `φ^E(k1)=−10<0` | **No**: `(5,0) ≰ (0,0)`, so `e_U2=(0,0)` blocks | no unblockable deviation | DL = 0 |
| unblockable (0, 2.5) | `y_c=1`, U1:k1, U2:k0 (15) | U2: `F_u(k1)=20>0`, `φ^E(k1)=−5<0` | **Yes**: `(0,0) ≤ (0,0)` | strict unblockable deviation | DL = 5 (C = max{25−5−10, 0} = 10) |

In the unblockable state the leader holds two blunt instruments. `y_c = 0` blocks U2:k1 but forfeits U1's 25. `Γ = {g}` contains no screening policy. So DL = 5 is the shadow price of instrument coupling (E2) when `Γ` cannot screen. Adding `g_req` to `Γ` (W4) removes it.

---

## 5. Managerial interpretation (TYPE C content, plain language)

1. **Budgets block over-spending, not misdirection.** An envelope can stop a unit from adopting a configuration that costs more pooled resource than the enterprise-preferred one. It cannot stop a configuration that is *cheaper or equal* in every pooled resource (Prop DL-6). Delegation loss lives exactly in that region.
2. **Two loss patterns.** (a) *Under-adoption*: the unit does not book the enterprise-wide value (`v^x`, avoided `l^x`), so it keeps the status quo. A budget cannot compel adoption; only a mandate (`J^must`) or a ledger fix can. (b) *Cheap harmful adoption*: low-cost AI use whose losses fall outside the unit's ledger (`l^x`). A budget cannot see it; a requirement (screening) or a prohibition can.
3. **Misalignment is a precondition, not a diagnosis.** A misaligned ledger produces no loss when the envelope can separate the conflicting configurations (W2). Diagnosing DL needs both (i) which AL condition fails and (ii) why no first-best plan survives at its own budget. This sharpens the P2 remark into an exact test (DL-1/DL-3).
4. **Shared platforms couple units.** A capability that enables one unit's valuable configuration can also enable another unit's harmful, unblockable one (W3). The enterprise then faces a portfolio trade-off, not a unit-level fix. This is consistent with the δ-nonmonotonicity counterexample (42 P4, T-SEN-8).
5. **Indifference is a risk under pessimism.** When units are indifferent between configurations the enterprise ranks differently, the pessimistic bound already shows a loss (W3b). Tie-breaking norms (defaults, procurement templates) matter.

---

## 6. Empirical observable implications (HYPOTHESES only — not tested, no data)

Every hypothesis below is a **conditional prediction of the model**. None has been observed. Testing them requires V0/V7-type enterprise data, which do not exist (42 §13.4; manuscript E43).

* **H-DL1 (footprint signature).** Where DL>0 operates, the unit-chosen configuration has a pooled-resource footprint (BUD/ENG incl. incremental opex, D9) no larger than the enterprise-preferred alternative. Observable: budget records plus the configuration register.
* **H-DL2 (ledger signature).** Units with documented external ledger items (`v^x`, `l^x`, chargeback `τ`, `C^impl,x`) show more divergence between unit-chosen and centrally evaluated configurations than units without them, *conditional on* H-DL1's footprint condition. Without that condition, no difference is predicted (W2).
* **H-DL3 (budget-tightening ineffectiveness).** Cutting a unit's envelope does not change its configuration choice when the disputed configuration is low-footprint. Requirements, prohibitions, or mandates do.
* **H-DL4 (platform coupling).** Introducing a shared capability can be followed by adoption of low-footprint, externally costly configurations in units the platform was not built for (W3, T-SEN-8).
* **H-DL5 (indifference).** Where units are indifferent across configurations, observed choices follow defaults and templates, and dispersion in enterprise value across otherwise similar units is larger (W3b).

---

## 7. Positioning (TYPE A / B / C)

Only works in the manuscript reference list (59a, "參考文獻") are cited. Anything else is marked **to verify** and must not be cited until it is added and verified.

| Claim | Type | Anchor |
|---|---|---|
| Bilevel (leader–follower) formulation; optimistic vs pessimistic follower selection; integer lower levels; KKT reformulation invalid for integer lower levels | **TYPE A** | Colson, Marcotte, & Savard (2007); Dempe (2002); Moore & Bard (1990); Kleinert et al. (2021); Wiesemann et al. (2013) — all in the list |
| IT governance is the allocation of decision rights over IT; centralized / decentralized / federal arrangements | **TYPE A** (definitional) / **TYPE B** for the mapping to `(y,γ,e)` | Sambamurthy & Zmud (1999); A. E. Brown & Grant (2005); C. V. Brown & Magill (1994); Tiwana & Konsynski (2010) |
| Formal authority (the leader's instruments: `G_j(γ)`, Allow, requirements, envelopes) vs real authority (the follower's actual choice inside them); DL as the value consequence of real authority sitting with the unit | **TYPE B** (conceptual anchor only). Aghion & Tirole's mechanism is informational; v2.2 is complete-information (P3). The thesis must not write "according to Aghion & Tirole, DL…" | Aghion & Tirole (1997) — in the list |
| Coordination vs adaptation; decentralization's informational benefit is outside this model | **TYPE B** (boundary statement; P3) | Alonso, Dessein, & Matouschek (2008) — in the list |
| Principal–agent misalignment of objectives; delegation as choosing the agent's permitted set | **TYPE B, to verify** — no principal–agent or delegation-set classic is in the reference list. Candidates to verify before citing: Jensen & Meckling (1976); Holmström (1984) on delegation; Alonso & Matouschek (2008, optimal delegation); Laffont & Martimort (2002). Bibliographic details not checked here. | — |
| **Known analogues — TO VERIFY** (named by Q/11 A10; none in the 59a list; no bibliographic details asserted): optimal delegation / permitted-set design (Holmström-type delegation; Alonso & Matouschek); **delegated project choice (Armstrong & Vickers)**; **capital-budget ceilings / spending limits (Harris & Raviv-type capital-budgeting models)**; optimistic vs pessimistic bilevel selection (Loridan & Morgan) | **TYPE B, to verify** — the DL mechanism (the principal restricts the set, the agent picks its favourite; budgets as ceilings) is known there. Do not cite until verified and added | — |
| DL-1 | **Restatement-level** (42 Lemma E′ at a first best; first-best-relative characterization lemma) | 42 §12.4; this document |
| DL-2o/DL-3/DL-4/DL-5/DL-6, §2.2, W1–W3c, W_DL_AL3 | **TYPE C (in-model; known analogues — TO VERIFY):** the mechanism "the principal restricts the agent's permitted set and the agent picks its favourite" is known from optimal delegation / delegated project choice; envelopes as ceilings are known qualitatively from capital budgeting with spending limits. New here: the envelope-as-ceiling instrument incompleteness with a finite policy menu, the opt/pess exactness, the unique-first-best primitive iff and W3c | this document |

**Difference from the principal–agent and optimal-delegation framing (to be confirmed against the to-verify works).** Here the follower's objective is *observable* (a booked ledger, 42 §8.1), information is complete, and the leader's instruments are institutionally fixed: pooled-resource ceilings, a finite policy menu, and shared capabilities. The loss therefore comes from **instrument incompleteness**, not from hidden information or hidden action. DL-1 characterizes when that incompleteness binds.

**AI-specificity (T7 per Q/11 A11).** Nothing in this document uses AI-specific structure: the objects are finite plan sets, pooled resource vectors, two ledgers, a finite policy menu with binary feasibility flags, and shared capabilities. DL-1 to DL-6 and every witness here hold verbatim for any shared-platform IT portfolio (ERP, cloud migration) under budget envelopes. The results are properties of the enterprise–BU architecture. The AI-specific content of the thesis lies elsewhere: the M1–M4 configuration schema (01), the autonomy-keyed requirement tables `X^req(A,κ)`, and the human-response layer `ρ` (VRG, design-response regret). One AI-specific reading is available but is a corollary, not a new result: screening via `EA^req(A,κ)` (03) acts only on configurations whose autonomy level `A` makes the requirement bind.

---

## 8. Relation to v2.2 (no contradiction)

* P1 and P2 are untouched. P2 is the special case DL-4c (`F_u ≡ φ^E_u`). The P2 corollary ("DL>0 ⇒ some AL fails") is consistent with DL-1 because AL3 is part of AL (W_DL_AL3).
* The P2 remark (42 l.628) is formalized by DL-1, DL-3, and DL-6.
* Lemma E′ is the shrink step of DL-1. No change to E′'s statement. Its pessimistic proof sentence (42 l.476, "取任一 `x ∈ T`") fails under a tolerant tie rule; the statement survives with the `F_u`-maximal choice (§2.2). Recorded as an erratum candidate for researcher review in `13_Q1_CANONICAL_42_ERRATUM_CANDIDATE.md`; 42 is not modified.
* P8 and P7 are treated in `03_Q1_GOVERNANCE_SCREENING_THEOREM.md`.

---

## 9. NOT PROVEN / open

1. **An iff in first-best-independent primitives (A)–(F): not provable as posed.** W3c shows the pairwise pattern does not determine the sign of DL. The proven characterization (Lemma DL-1) needs the set `𝓑*`, so checking it is as hard as solving B. Cor DL-3 gives a primitive form only under a unique first best.
2. **Tolerance version — UPGRADED, QUALIFIED [T8-fix] (T7, 2026-10-15): PROVEN for DL-1o/p and Lemma E′ ONLY under exact affordability** under every tie rule `{F_u ≥ g(m)}` with `g` non-decreasing and `g(m) ≤ m`, which includes 51's relative `ε_tie` (51 l.673), under exact affordability (§2.2). *Previous text (superseded):* "DL-1 is proven for `ε_tie = 0` (and any absolute tolerance), not for the relative one. Status: NOT_PROVEN for relative `ε_tie`". The earlier draft's (⇒) proof was also not valid for an absolute tolerance, because it chose the `φ`-minimizer of the tie set (Q/11 §2.7); the repaired `F_u`-maximal selection fixes both. *Still open:* 51's absolute affordability slack (`a ≤ e + 10^{-9}`, 51 l.667) is not covered; Cor DL-2o/2p, DL-3, DL-4, DL-5 remain exact-tie results.
3. **Comparative statics of DL** (monotonicity in `l^x`, `impl`, `F_c`, `δ`, `Ā`): not proven, and false in general for `δ` (42 P4 / T-SEN-8).
4. **Robust versions** (DL over `Θ_g`, element-level classification), **Model D** (tri-level), and **information asymmetry** (P3, Model B^info): not covered.
5. **Restricted envelope institutions** (envelopes only on BUD, discretized envelopes, `e ≥ 0` while `a` can be negative, a common pool under D3-B/GNEP): DL-1 assumes unrestricted real envelopes over all of `H^pool`, as in 42 §4.1/§12.4. Under restrictions, Lemma S and DL-1 change. Not analysed.
6. **Lower bound on DL** in primitives: none established beyond DL-1 and DL-5.

**Files:** `witness_parts/w_dl_gov.py` (W1, W2, W3, W3m, W3b, W3c, W5 [= W_DL_AL3 in the assembled `q1_theory_witnesses.py`]; Task C witnesses in the same file); `work/B/fuzz_dl_gov.py` (falsification search, scratch).
