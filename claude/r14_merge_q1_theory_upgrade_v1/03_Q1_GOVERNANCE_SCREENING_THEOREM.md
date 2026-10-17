# 03 — Q1 Governance Screening Theorem (Task C, theory agent T1)

**Status:** Q1 theory-upgrade candidate, 2026-10-14. Additive to canonical v2.2. 42 and 51 were not modified.
**Evidence class:** the results below have complete proofs. GS-0 is P7 restated with the cost channel and GS-I is an accounting identity (restatement-level); GS-N, GS-1/GS-2, Cor GS-4 and W4b–W4e are the in-model TYPE C content, whose mechanism (restricting the agent's permitted set) has known analogues in the delegation literature (§10). W4–W4e are constructive examples and synthetic regressions, and they are never used to prove a universal statement. All values are SIMULATED_ONLY algebra.
**Notation:** as in `02_Q1_DELEGATION_LOSS_THEOREM.md` §1 (`P^C_u`, `P^B_u`, `a_u`, `F_u`, `φ^E_u`, `BR_u`, `K`, `b̄`, `𝓑*`, DL-1).

**Verdict lines**

```
B_MONOTONICITY (stricter requirement => F_B* weakly lower)      = RESTATEMENT: GS-0 = 42 P7 restated with the cost channel (needs DeltaC_gov(strict) >= DeltaC_gov(loose) for the net version)
EXACT_IDENTITY GSV = DL_loose - DL_strict - PR_B                = IDENTITY GS-I (accounting decomposition; substitution of F^C = F^B - DL), opt and pess separately;
                                                                  GSV <= DL_loose is a COROLLARY of P1 + P7
SUFFICIENT_CONDITION_FOR_GSV>0                                  = PROVEN (Prop GS-1; full screening => GSV = DL_loose)
NECESSARY_CONDITION_FOR_GSV>0                                   = PROVEN (Thm GS-N: excluded, envelope-non-separable strict [opt] / weak [pess] reversal)
GSV_IFF                                                         = NOT_PROVEN in primitive terms (GS-I gives an exact accounting identity, not a primitive iff)
ALIGNED => GSV<=0                                               = PROVEN for "no weak reversal"; for "no strict reversal" only GSV_opt<=0 (W4e: GSV_pess=1)
FULL_ENVELOPE_SEPARABILITY => GSV<=0                            = PROVEN (Cor GS-4)
P8 10->15 algebraic witness                                     = PASS (W4); opposite 15->10 = PASS (W4b)
```

**Restatement of v2.2 vs genuinely new (TYPE C), consistent with Q/11 A1, A4, §3** (added 2026-10-15, T7):

| Restatement / identity (no new content) | Genuinely new in-model content (TYPE C) |
|---|---|
| **GS-0** = 42 P7 with the cost channel `ΔC^gov` made explicit | **Thm GS-N** (necessary condition: a requirement adds value only by excluding a loose best response that is envelope-non-separable from, and enterprise-worse than, a surviving plan; non-definitional; exact ties) |
| **GS-I** = accounting identity (substitute `F^C = F^B − DL`); **`GSV ≤ DL_loose`** = corollary of P1 + P7 | **W4c, W4d, W4e** (the three ways a "screening" rule fails or succeeds unexpectedly: price of requirement, pairwise screening, pessimistic-only screening from a tie) |
| `B_MONOTONICITY` (= P7); "B has no screening effect" (B has no follower) | **Prop GS-1** (full screening ⇒ `GSV = DL_loose`; near-definitional via DL-1, but with an explicit primitive form under a unique first best), **GS-2**, **Cor GS-4** |
| P8 10 → 15 itself (42 P8, 51 REG); W4 reproduces it | The governance-function map (§7) with the `EE`-vs-`RE` booking caveat for screening by prohibitions |

---

## 0. v2.2 sources (quoted, read-only)

| Item | 42 location |
|---|---|
| Requirement tables `H^req_γ, WI^req_γ, EA^req_γ, G^req, R^req/D^req`; `ē^γ_j`; Allow; `G_j(γ)` is a permission level (enablement) | §3.1 l.90–97; §5 (F3)–(F9) l.177–191 |
| `ΔC^gov(γ)` enters both (OBJ-E) and (R1)/(R1′) BUD | §7.4 l.297; §5.1 l.217, l.223 |
| Q3 decomposition `VG = EE + RE + CE` (enablement / requirement / cost blocks) | §14 Q3, l.603 |
| Q5 Price of Requirement `PR_X = F*(Req_X relaxed one level) − F*`; "screening" when `PR_X < 0` in C | §14 Q5, l.605 |
| P7: relaxing a requirement only enlarges B's feasible set (fixed θ and costs); in C only under AL | §15 P7, l.638 |
| P8: in C with AL failing, tightening can strictly raise leader value; 46 hand instance 10→15 | §15 P8, l.640 |
| Three channels of positive policy value: enablement, robust feasibility, (C only) screening | §15, l.642 |
| REG regression: `hand_instance(0.0, 2.5, ea_levels=(2,1), ea_req=2)`: `C(g)=10`, `C(g_req)=15` | 51 `t_regression_v21` |

---

## 1. Definitions

Write `Req` for the requirement block of a policy: `(H^req, WI^req, EA^req, G^req, R^req, D^req, ē)`.
* **Strict vs loose.** `Req_s ⪰ Req_l` ("stricter") means every requirement table is pointwise `≥` and `ē_s ≤ ē_l`. The enablement block (Allow, Allow^loc, `G_j(γ)`, `J^must`, `J^forbid`) is held fixed. Costs `C_s := ΔC^gov(Req_s)` and `C_l` may differ.
* **Value functions.** `F^B(Req, C)` and `F^{C,m}(Req, C)` are the B and C values with `γ` fixed to that requirement–cost pair. For a menu, take the max over its elements.
* **Price of requirement in B.** `PR_B := F^B(Req_l, C_l) − F^B(Req_s, C_l)`, measured at equal cost. This is 42 Q5's `PR_X` in B.
* **Gross screening effect** (task's GSV; equals 42's requirement effect RE in C):
  `GSV^m := F^{C,m}(Req_s, C_l) − F^{C,m}(Req_l, C_l)`.
* **Direct governance cost effect:** `DGC^m := F^{C,m}(Req_s, C_s) − F^{C,m}(Req_s, C_l)`.
* **Net governance effect:** `NGE^m := F^{C,m}(Req_s, C_s) − F^{C,m}(Req_l, C_l) = GSV^m + DGC^m`.

---

## 2. Model B monotonicity

**GS-0 (B) — 42 P7 restated with the cost channel [multi-BU; restatement].**
* (a) At equal cost, `F^B(Req_s, C) ≤ F^B(Req_l, C)`, i.e. `PR_B ≥ 0`.
* (b) If `C_s ≥ C_l`, then `DGC^B ≤ −(C_s − C_l) ≤ 0`, so `F^B(Req_s, C_s) ≤ F^B(Req_l, C_l) − (C_s − C_l)`.
* (c) If `C_s < C_l`, the net B effect can be positive. Any such gain comes from **cost**, never from the requirement.

*Proof.*

(a) Every requirement flag is antitone in its requirement:
* (F5a)–(F5e) are `𝟙[level ≥ req]`.
* (F6) is `1` if `H^req < 2`, else `Eff_H ≤ 1`. Raising `H^req` can only move the flag from `1` to `Eff_H`.
* (F9) is `𝟙[N E[I^sev] ≤ ē]`, which is monotone in `ē`.

So `Φ_jk(Req_s) ≤ Φ_jk(Req_l)` pointwise, and `P^B_u(y, Req_s) ⊆ P^B_u(y, Req_l)` for every `(y, u)`. Neither (OBJ-E) nor `a_u` depends on `Req`. B maximizes the same objective over a smaller set.

(b) `ΔC^gov` enters the objective as `−C` and the BUD budget as `b̄ − C`. For fixed `Req`, raising `C` subtracts `C_s − C_l` from every feasible portfolio's value and shrinks the feasible set.

(c) Reverse the inequality in (b). ∎

This is P7, together with an explicit statement of the cost channel that P7 holds fixed.

**Why B has no screening effect.** B has no follower: `DL ≡ 0` in B, so `GSV^B = −PR_B ≤ 0` (GS-I with both DL terms equal to 0). A requirement only removes options from a planner who would choose the best one anyway.

---

## 3. Exact accounting identity

**Identity GS-I (accounting decomposition) [multi-BU, both modes].** At equal cost,

`GSV^m = DL^m(Req_l) − DL^m(Req_s) − PR_B`, where `DL^m(Req) := F^B(Req) − F^{C,m}(Req)`.

*Proof.* Substitute `F^{C,m} = F^B − DL^m` in both regimes. ∎ (An identity, not a theorem.)

**Corollary GS-I′ (of P1 + P7).** `GSV^m ≤ DL^m(Req_l)`. *Proof:* `DL^m(Req_s) ≥ 0` (P1) and `PR_B ≥ 0` (P7 = GS-0(a)) in GS-I. ∎

**Reading.** A requirement adds value in C exactly when it reduces delegation loss by more than its first-best price. Since `DL^m(Req_s) ≥ 0` (P1) and `PR_B ≥ 0` (GS-0), it follows that **`GSV^m ≤ DL^m(Req_l)`**: screening can at most remove the existing delegation loss. In 42 Q5 terms, with `Req_s` = current and `Req_l` = relaxed one level: `PR^C_X = −GSV = PR^B_X − [DL(relaxed) − DL(current)]`. The Q5 "screening" verdict (`PR^C_X < 0`) means the DL reduction exceeds `PR^B_X`.

All six governance witnesses check GS-I numerically. The falsification search (`work/B/fuzz_dl_gov.py`) also found 0 violations in 1,358 random instances. That search is not a proof; GS-I is an algebraic identity.

---

## 4. Sufficient condition

**Prop GS-1 (full screening) [multi-BU, both modes].** Assume equal cost and AL3, and suppose `DL^m(Req_l) > 0`. Suppose there is a first-best solution `(y*, γ_l, x*)` of the loose regime such that:
1. (keeps the first best) `x*_u ∈ P^C_u(y*, Req_s)` for all `u`; and
2. (removes all unblockable deviations) the opt condition is `x*_u ∈ BR_u(a(x*_u) | y*, Req_s)` for all `u`, and the pess condition additionally requires `min_{BR_u(a(x*_u) | Req_s)} φ^E_u ≥ φ^E_u(x*_u)`.

Then `F^{C,m}(Req_s) = F^B(Req_s) = F^B(Req_l)` and `GSV^m = DL^m(Req_l) > 0`.

*Proof.*
* By condition 1, `x*` is B-feasible under `Req_s`, so `F^B(Req_s) ≥ F^B(Req_l)`. GS-0 gives the reverse inequality, so the two are equal and `PR_B = 0`.
* By conditions 1–2, `(y*, γ_s, x*)` is a self-enforcing first best of the strict regime. DL-1 then gives `DL^m(Req_s) = 0`.
* Apply GS-I. ∎

**Primitive version (task's candidate list), under a unique loose first best [multi-BU].** Let `𝓑*(Req_l) = {(y*, x*)}` and let `U^dev` be the units with an unblockable deviation, i.e. `x^H ≠ x*_u` with `a(x^H) ≤ a(x*_u)` and `F_u(x^H) > F_u(x*_u)` (opt) or `≥` (pess). By Cor DL-3 each such `x^H` is a reversal (`φ^E(x^H) < φ^E(x*_u)`) and envelope-non-separable from `x^G := x*_u`. Then `GSV^m = DL^m(Req_l) > 0` if:
* the strict requirement gives `R_s(x^G) = 1` for every first-best plan (it does not exclude a needed configuration), and
* it gives `R_s(x^H) = 0` for **every** unblockable deviation `x^H` of **every** unit in `U^dev`, not just one reversing pair.

This follows from GS-1 because, after exclusion, `BR_u(a(x*_u) | Req_s) = {x*_u}` holds in both modes.

**Why "every" is needed.**
* **Prop GS-2 (pairwise screening is insufficient):** W4d. U2 has two unblockable deviations, `xH = k1` (`F_u = 20`, `φ^E = −5`, EA=1) and `xM = k2` (`F_u = 19`, `φ^E = −6`, EA=2). The strict EA≥2 rule removes `xH` only, so U2 switches to `xM`. Result: `C: 10 → 9`, `GSV = −1`, `DL: 5 → 6`. GS-I check: `−1 = 5 − 6 − 0`.
* "Every envelope admitting `x^G` admits `x^H`" (the task's candidate) is exactly Lemma S's `a(x^H) ≤ a(x^G)`. It is required for the deviation to matter (GS-N), but without the other conditions it is not sufficient (W4b, W4c, W4d).

---

## 5. Necessary condition

**Thm GS-N [multi-BU].** Assume equal cost and equal enablement block. If `GSV^m > 0`, then all of the following hold.

(i) `DL^m(Req_l) ≥ GSV^m > 0`. So every DL-necessary condition holds in the loose regime (02, DL-1/DL-2).

(ii) There are a capability vector `y` (the strict regime's C-optimal one), a unit `u`, and plans `x^G ∈ P^C_u(y, Req_s)` and `x^H ∈ P^C_u(y, Req_l) \ P^C_u(y, Req_s)` such that:
* `a_u(x^H) ≤ a_u(x^G)` (envelope non-separability);
* `φ^E_u(x^H) < φ^E_u(x^G)`;
* `F_u(x^H) > F_u(x^G)` if `m = opt`, or `F_u(x^H) ≥ F_u(x^G)` if `m = pess`.

Moreover, `x^H` is a loose-regime follower best response at the envelope `a(x^G)`. In words: **a requirement adds value only by excluding a follower best response that is enterprise-worse than a surviving plan needing no more pooled resource.**

*Proof.*

(i) `F^{C,m}(s) ≤ F^B(s) ≤ F^B(l)` (P1, GS-0), so `F^{C,m}(l) < F^{C,m}(s) ≤ F^B(l)`.

(ii) Let `(y, e)` be C-optimal under `Req_s`. For each `u`, pick `x^G_u ∈ BR_u(e_u | s)`. For opt, take the `φ^E`-maximal element; for pess, any element. Replace `e_u` by `a(x^G_u)` (Lemma E′: opt value unchanged, pess weakly higher, hence equal by optimality). This envelope profile is also admissible under `Req_l`: same budget, and `x^G_u ∈ P_l` is affordable. Its loose value is `≤ F^{C,m}(l) < F^{C,m}(s)`. Since the values are sums over units, some `u` has a loose contribution strictly below its strict contribution at `e_u = a(x^G_u)`.

Use `P_s ⊆ P_l`. If `BR_u(e | l) ∩ P_s ≠ ∅`, then `BR_u(e | s) = BR_u(e | l) ∩ P_s ⊆ BR_u(e | l)`.

* **Opt.** Inclusion would give `max_l ≥ max_s`, so the intersection must be empty. Then every `x^H ∈ BR_u(e | l)` lies in `P_l \ P_s` and has `F_u(x^H) > F_u(x^G_u)`, because `x^G_u` is affordable but not a loose BR. Also `max_{BR_l} φ^E < φ^E(x^G_u)`.
* **Pess, intersection nonempty.** `min_l < min_s` forces an `x^H ∈ BR_u(e | l) \ P_s` with `φ^E(x^H) < min_s ≤ φ^E(x^G_u)` and `F_u(x^H) = F_u(x^G_u)`, since both lie in `BR_u(e | l)`.
* **Pess, intersection empty.** As in the opt case, with `F_u(x^H) > F_u(x^G_u)`.

In every case `a(x^H) ≤ e_u = a(x^G_u)`. ∎

**Status of an iff.** Together, GS-1 (sufficient) and GS-N (necessary) bracket `GSV > 0`, and GS-I is an exact accounting identity. A **primitive** iff is NOT_PROVEN. The gap is that the excluded best responses must outweigh `PR_B`, which is a portfolio-level comparison (W4c: an excluded unblockable reversal exists, yet `GSV < 0`).

---

## 6. Answers to items 1–9

| # | Question | Answer | Status |
|---|---|---|---|
| 1 | Sufficient condition | GS-1: a strict requirement that keeps some loose first best and removes **all** of its unblockable deviations (both modes; pess also removes tied enterprise-worse plans), at equal cost, gives `GSV = DL_loose > 0`. Primitive form under a unique first best: §4. | Proposition |
| 2 | Necessary condition | GS-N: `DL_loose ≥ GSV > 0`, plus an **excluded** plan `x^H` that is a loose best response at `a(x^G)`, envelope-non-separable from a surviving `x^G`, enterprise-worse, and weakly (pess) or strictly (opt) unit-preferred. | Theorem |
| 3 | Why B has no screening effect | No follower, so DL ≡ 0 and `GSV^B = −PR_B ≤ 0` (GS-0, GS-I). | Theorem |
| 4 | Aligned ledger ⇒ GSV ≤ 0? | **Precise version.** (a) If no non-separable pair has a **weak** reversal (in particular under AL1–AL4, or ordinal alignment), then `GSV^opt, GSV^pess ≤ 0` (and, if AL3 also holds, `GSV = −PR_B`). (b) If there is no **strict** reversal but there are ties, only `GSV^opt ≤ 0` is guaranteed. W4e: `F_u(xG) = F_u(xH) = 0`, `φ^E = 1` vs `0`; the strict rule removes `xH`; `GSV^pess = 1`, `GSV^opt = 0`. So "positive screening cannot arise from preference conflict alone" is the wrong statement. The correct one: **positive optimistic screening requires a strict conflict; positive pessimistic screening requires a strict conflict or follower indifference with enterprise disagreement.** Proof: GS-N(ii) is violated under (a), and under (b) for opt, so `GSV ≤ 0`. GS-N does not use AL3, so the sign result does not need it. With AL3, DL-4 gives DL = 0 in both regimes, and GS-I gives `GSV = −PR_B`. | Theorem + counterexample |
| 5 | Full envelope separability ⇒ positive effect vanishes? | **Yes.** Assume every reversing pair in `P^C_u(y, Req_l)` is envelope-separable, for all `y` and `u`: `a(x^H) ≤ a(x^G)` ⇒ no strict reversal (opt) / no weak reversal (pess). Then GS-N(ii) fails and `GSV^m ≤ 0`. The property is inherited by `Req_s` because `P_s ⊆ P_l`. With AL3, `DL = 0` in both regimes and `GSV = −PR_B`. (Cor GS-4) | Corollary |
| 6 | Negative governance example (strict rule excludes `x^H` and the better `x^G`) | **W4b:** U1 has `k1` (EA=1, `φ = F_u = 25`) and `k2` (EA=2, `φ = F_u = 20`). U2:k1 is a blockable reversal (impl 5). Strict EA≥2 removes U1:k1 and U2:k1. `B: 15 → 10`, `C: 15 → 10`, `GSV = −5 = 0 − 0 − 5`. **W4c** (the trade-off case): U2:k1 is *unblockable*, and U1:k2 has `φ = 17`. The strict rule removes `DL = 5` but costs `PR_B = 8`: `C: 10 → 7`, `GSV = −3 = 5 − 0 − 8`. Screening and price of requirement appear together, through the policy-coupling channel (one `γ` for all units). | Constructive examples |
| 7 | Governance taxonomy mapped to v2.2 | See §7. | Definitional |
| 8 | Minimal algebraic decomposition of P8 10→15 | See §8. | Witness + proof |
| 9 | Opposite 15→10 counterexample | W4b (above; §8). | Constructive example |

*v2.2 embedding of W4e (T7 per Q/11 §2.13 item 3).* W4e is an abstract single-BU core. With a literal status quo `k0 = (0,0,0)` present, `xH = (a=0, F_u=0, φ=0)` coincides with `k0`; `GSV_pess = 1` then requires the strict requirement to exclude the status quo itself, which 42 l.200 allows ((F2)–(F9) apply to every `k`, incl. `k = 0`). If `xH` is a separate AI configuration and `k0` survives the strict rule, `k0` ties with `xG` and `GSV_pess = 0`.

---

## 7. Governance functions mapped to v2.2 terms

| Function | v2.2 instrument / term | Where its value appears | Sign possibilities |
|---|---|---|---|
| **Compliance** (hard floor) | (F2) `Legal`; (F9) at `γ^0` legal minimum; `STATUS_QUO_NONCOMPLIANT` | Not valued. A constraint common to every model (42 §1.3 rule: no monetization; D5) | Neither a gain nor a cost in the comparisons; defines `γ^0` |
| **Assurance** (robust feasibility) | Requirement tables beyond `γ^0` that keep a portfolio feasible on all of `Θ_g` | §13.3 feasibility classes; Q5 "robustness-protective" | Positive only under uncertainty (`Θ_g`), not at fixed `θ`. Not covered by GS-0–GS-N, which are fixed-`θ` results |
| **Screening** | The same requirement tables, in C | `RE` in C = `GSV`; Q5 `PR^C_X < 0`; P8 | `GSV ≤ DL_loose`. Positive only under GS-N's conditions |
| **Enablement** | Allow, Allow^loc, `G_j(γ)` (permission level), `J^must`, `J^forbid` | `EE` in Q3 | Either sign. **Caveat:** `J^forbid` and `Allow = 0` can *screen* (exclude `x^H`) and `J^must` can *compel* (cure under-adoption, which envelopes cannot; 02 Prop DL-6). Under 42's Q3 block assignment, such screening is booked in `EE`, not `RE`. A thesis claim that "screening = requirement effect" undercounts screening done by prohibitions |
| **Operating governance cost** | `ΔC^gov(γ)` in (OBJ-E) and the BUD budget | `CE` in Q3; `DGC` here | `≤ −(C_s − C_l)` when stricter is costlier (GS-0b). Only cost changes can make the B-side net effect positive |

Summary: **NGE = GSV (screening, C only) + DGC (operating cost)**, where `GSV = −PR_B + [DL_l − DL_s]`. Assurance is evaluated separately on `Θ_g`. Enablement is a different block.

---

## 8. P8 decomposition and opposite case (W4, W4b)

**W4: P8 10 → 15** (= 51 REG `hand_instance(0.0, 2.5, ea_levels=(2,1), ea_req=2)`).

Inputs (N=10, `F_c=10`, `Ā = (100,100)`, `ΔC^gov = 0` in both regimes):
* U1:k1 has `v_u=3`, `l_x=0`, impl 5, EA=2, so `φ^E = F_u = 25` and `a = (5,0)`.
* U2:k1 has `v_u=2`, `l_x=2.5`, impl 0, EA=1, so `F_u = 20`, `φ^E = −5`, and `a = (0,0)`.
* Loose: EA_req = 0. Strict: EA_req = 2 for A ≥ 1.

| Term | Value | Derivation |
|---|---|---|
| `F^B(loose)` = `F^B(strict)` | 15 | unique first best `y_c=1`, U1:k1, U2:k0: `25 − 10`. The strict rule keeps U1:k1 (EA=2) |
| `PR_B` | 0 | |
| `F^{C}(loose)` | 10 | U2:k1 is an unblockable strict reversal (Cor DL-3). Best leader choice: `25 − 5 − 10 = 10` vs `y_c=0`: 0 |
| `DL(loose)` | 5 | |
| `F^{C}(strict)` | 15 | U2:k1 is excluded (EA 1 < 2), so `BR_U2 = {k0}`. GS-1 holds: full screening |
| `DL(strict)` | 0 | |
| `GSV` | **+5** | `= DL_l − DL_s − PR_B = 5 − 0 − 0`. Opt = pess. `DGC = 0`, `NGE = 5` |
| C with menu `{loose, strict}` | 15 | the leader picks strict |

**Minimal algebraic core [SINGLE-BU]:** plans `xG = (a=0, F_u=0, φ=1, EA=2)` and `xH = (a=0, F_u=1, φ=0, EA=1)`. Loose `C = 0`, strict `C = 1 = B`, `GSV = 1 = DL_loose`. The second BU and the capability in W4 reproduce P8's exact numbers. They also show why the capability instrument (`y_c = 0`) is too blunt there: it would also remove U1's 25. *v2.2 embedding (T7 per Q/11 §2.13 item 3):* this core is an abstract finite bilevel instance. In a literal v2.2 instance the status quo `k0 = (a=0, F_u=0, φ=0)` is always present; if it survives the strict rule it ties with `xG` (`F_u = 0`), giving `GSV_opt = 1` but `GSV_pess = 0`. A literal embedding with the same result in both modes raises the unit ledger of both AI plans by 1: `xG = (0, F_u=1, φ=1, EA=2)`, `xH = (0, F_u=2, φ=0, EA=1)` (then `BR_strict = {xG}`, `GSV = 1` in both modes). W4 itself (two BUs) is a literal instance and needs no adjustment.

**W4b: opposite 15 → 10.** U1 has `k1` (EA=1, 25) and `k2` (EA=2, `v_u = 2.5`, so 20). U2:k1 is blockable (impl 5, `l_x = 2.5`, `φ^E = −10`).

| Term | Value |
|---|---|
| `F^B(l)`, `F^C(l)` | 15, 15 (DL_l = 0: the envelope `e_U2 = (0,0)` already blocks U2:k1) |
| `F^B(s)`, `F^C(s)` | 10, 10 (U1 is forced to k2: `20 − 10`) |
| `PR_B`, `GSV` | 5, **−5** `= 0 − 0 − 5` |

The strict rule screens a reversal that was already blocked, and it excludes the better first-best configuration. Core [SINGLE-BU]: `xG (F=2, EA 1)`, `xG′ (F=1, EA 2)`, `x0`; strict gives `2 → 1`.

---

## 9. Assessing the sentence

> "Governance can substitute for incomplete incentive alignment when resource allocation cannot separate enterprise-preferred from unit-preferred configurations."

**Problems.**
1. **"can substitute" vs "when".** The sentence implies the condition is sufficient. It is only necessary (GS-N). Counterexamples:
   * W4c: non-separable reversal present, `GSV < 0`, because the rule also prices out a first-best configuration;
   * W4d: pairwise screening lets a worse unblockable plan take over;
   * W4b: the rule is applied where the envelope already separates.
2. **"cannot separate" is ambiguous.** The binding object is the follower's best response relative to the *first-best* plan. A pair is non-separable iff `a(x^H) ≤ a(x^G)` (Lemma S). Separation by `y` or `γ` counts too (02 §1).
3. **"incentive alignment"** should be **ledger alignment** (AL1–AL4, observable accounting). The model has complete information and no incentive contracts.
4. **Ties.** Under pessimistic tie-breaking, governance can also substitute where units are indifferent (W4e), not only where preferences conflict.
5. **Scope.** The claim holds only in Model C (the bilevel model with complete information) and at fixed `θ`. It says nothing about assurance under `Θ_g`, and P3's information boundary applies.

**Strongest true version (TYPE C; proven by GS-0, GS-I, GS-1, GS-N; 02 DL-1):**

> In the complete-information enterprise–BU bilevel model, a stricter AI-governance requirement raises enterprise value only if some unit's booked ledger diverges from the enterprise ledger (or the unit is indifferent where the enterprise is not) in a way that pooled-resource envelopes cannot block. That means the requirement must exclude a unit's best-response configuration that uses no more pooled resource than a surviving configuration, yet is worth less to the enterprise. The value it adds equals the reduction in delegation loss minus the requirement's first-best price, so it never exceeds the delegation loss under the looser rule. It fully substitutes for ledger alignment, recovering the centralized value, exactly when it removes every such unblockable deviation from some centralized-optimal portfolio while keeping that portfolio feasible at no extra governance cost. Under ledger alignment, or when envelopes separate every conflicting configuration pair, a stricter requirement cannot raise enterprise value.

Short form for the abstract/discussion:

> "When budget envelopes cannot block a unit's preferred but enterprise-inferior AI configuration, a governance requirement that screens out that configuration can recover the delegation loss — but never more than that loss, and only net of the requirement's own cost to the centralized optimum."

---

## 10. Positioning (TYPE A / B / C)

| Claim | Type | Anchor (manuscript reference list only) |
|---|---|---|
| Requirements as feasibility restrictions in a leader–follower program; opt/pess selection | TYPE A | Colson et al. (2007); Dempe (2002); Wiesemann et al. (2013) |
| Governance = allocation of decision rights; centralized / federal designs | TYPE A (definitional) / TYPE B (mapping to Req, Allow, envelope) | Sambamurthy & Zmud (1999); A. E. Brown & Grant (2005); C. V. Brown & Magill (1994); Tiwana & Konsynski (2010) |
| Rules vs discretion: formal authority constraining real authority | TYPE B (conceptual only; A&T's mechanism is informational, ours is not) | Aghion & Tirole (1997) |
| Restricting the agent's choice set as an optimal-delegation instrument | TYPE B, **to verify** (not in list): Holmström (1984); Alonso & Matouschek (2008, REStud); **Armstrong & Vickers (delegated project choice; added per Q/11 A4, details not checked)**. Do not cite until verified and added | — |
| GS-0 (P7 + cost channel), GS-I (identity), GS-I′ (corollary of P1 + P7) | **Restatement-level** | 42 P1, P7 (in-model) |
| GS-1, GS-2, GS-N, GS-4, W4–W4e | **TYPE C (in-model; known analogues — TO VERIFY):** "pruning the follower's option set can raise the leader's value" is the standard delegation-set insight (Holmström-type delegation; Alonso & Matouschek, optimal delegation; **Armstrong & Vickers, delegated project choice**). New here: the necessary condition GS-N (non-definitional), the three failure modes W4c/W4d/W4e, the finite policy menu, and opt/pess exactness | this document; 42 P8 (in-model) |

**AI-specificity (T7 per Q/11 A11).** GS-0 to GS-N use only finite plan sets, pooled resources, two ledgers and binary requirement flags; they hold verbatim for any shared-platform IT portfolio with rule-based governance. The AI-specific element is only the *content* of the requirement tables: `H^req, WI^req, EA^req, G^req` are keyed by the autonomy level `A_k` and consequence class `κ_j` (01 S1). Hence a corollary, not a new result: screening via `EA^req(A,κ)` acts only on configurations whose autonomy level makes the requirement bind (in W4, the strict rule `EA ≥ 2 for A ≥ 1` cannot touch the status quo `A = 0`). The thesis should present GS as a property of the enterprise–BU architecture, not as an AI-specific finding.

---

## 11. NOT PROVEN / open

1. **A primitive iff for `GSV > 0`.** Not proven. Only GS-1 (sufficient), GS-N (necessary), and the exact identity GS-I are available. The missing piece is a primitive condition for "DL reduction > PR_B" at the portfolio level.
2. **Joint changes of requirements, enablement, and cost** (a full `γ → γ′` move). Only the additive decomposition `NGE = GSV + DGC` and 42 Q3's order-dependent `EE/RE/CE` are available. No sign theorem beyond GS-0(b).
3. **Assurance value** (robust feasibility on `Θ_g`): outside the fixed-`θ` results.
4. **Relative `ε_tie`:** GS-N and the unique-first-best primitive version of GS-1 need exact ties (GS-N's step `BR_s = BR_l ∩ P_s` uses the exact `argmax`). GS-0, GS-I and GS-1 (in its `BR`-form) carry over to tie rules `{F_u ≥ g(m)}` through 02 §2.2 (Lemma DL-1 under `g`); this is noted, not separately re-proved here.
5. **Existence/optimality of a screening requirement within a finite menu `Γ`** (requirement design): not addressed. GS-1 shows only when a given requirement fully screens.

**Files:** `witness_parts/w_dl_gov.py` (W4, W4b, W4c, W4d, W4e, plus Task B witnesses); `work/B/fuzz_dl_gov.py` (falsification search for GS-I and GS-N, 430 `GSV > 0` cases, 0 violations).
