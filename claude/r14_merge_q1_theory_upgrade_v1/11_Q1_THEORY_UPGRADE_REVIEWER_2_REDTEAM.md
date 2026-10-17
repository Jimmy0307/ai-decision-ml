# 11 — Q1 Theory Upgrade: Reviewer #2 Red-Team Report (agent T6)

**Date:** 2026-10-15. **Role:** hostile Q1-journal Reviewer #2, adversarial but fair. An attack is marked NOT_VALID when the pack already handles it.
**Read-only inputs:** Q\01–08, Q\witness_parts\w_*.py, REPO\42_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md (42), and REPO\51_enterprise_portfolio_solver_v2_2.py (51; only l.37 and l.666–674 were inspected, for the tie rule). No REPO file and no other Q file was modified.
**Scratch computations** (pure stdlib, SIMULATED_ONLY, no 51 import) are in the session scratchpad `t6/`: `w5_robust.py`, `w5_wide.py`, `tie_shrink.py`. They are re-runnable checks. They are not part of the pack and prove nothing universal.
**Witness run:** all 26 `witness_*` functions in the four parts return `pass=True` (run with `python -I`, imported one by one).

Severity scale: **CRITICAL** = a false main theorem or a contradiction with v2.2 that invalidates a headline. **MAJOR** = must change before submission (overclaim of a headline, a novelty or positioning gap a referee will reject on, a result whose content is definitional). **MINOR** = a local proof gap, quantifier slip, labeling or integration defect, each fixable in a few lines. **NOT_VALID** = the attack fails, or the pack already handles it.

---

## 0. Executive summary

* **No CRITICAL defect was found.** Every main proof I checked line by line holds under its stated hypotheses (exact ties). That includes DL-1o/p, Cor DL-2o, Cor DL-3, GS-I, GS-N, GS-1, D1, D3, D4, D5, Lemma S (04), Lemma M, R1, R4, R5, E.1, E.2, E.4, E.7, E.10, and G1–G3.
* **The weakness is substance, not correctness.** Several headline results are restatements or definitional identities:
  * DL-1 is Lemma E′ applied to a first best; the pack says so itself at 02 l.107.
  * GS-I is an accounting identity.
  * GS-0 is P7.
  * D3 is P2 applied at each fixed `(y,γ)`.
  * R1 is Lemma R; Lemma 0 is 42 l.535.
  * IRR holds by construction once typing axioms T1–T4 assign each attribute that v2.2 reads to exactly one mechanism.

  The genuinely new content is narrower than the verdict lines suggest (§3 lists it).
* **Positioning.** The mechanisms are known in other literatures:
  * restricting the agent's permitted set (optimal delegation; delegated project choice);
  * budgets as spending ceilings (capital budgeting);
  * menu-dependence of minimax regret;
  * complementarity of information;
  * partial identification.

  None of 02–07 uses AI-specific structure. Unless the manuscript says this explicitly, a Q1 referee will reject the "AI theory" framing.
* **New technical findings from this review:**
  1. **Tie-tolerance gap.** The pessimistic part of 42's Lemma E′ proof ("取任一 x ∈ T", 42 l.476) is false under 51's tie rule (51 l.673). Concrete counterexample in §2.7. The same gap affects the DL-1p proof as written. The *statements* survive with a corrected choice: take the `F_u`-maximal element of the tie set. That also lets 02 §9.2 ("NOT_PROVEN for relative ε_tie") be upgraded.
  2. **Thin W5 margins.** The W5 build-region witness lies in an open set but has margins of 1 TWD on quantities of order 24–30. It survives ±1 % joint parameter perturbation (398/400) but only 44 % of ±5 % draws. It is knife-edge in two structural zeros: an exactly zero floor on the reused cost, and an exactly zero ENG footprint. Any ε > 0 destroys it. A wide-margin replacement is given (§2.6).
  3. **G4 quantifier slip** (07): "some decision optimal at all vertices" does not match Definition G's "`D*(θ^0) ⊆ RD`". Counterexample in §2.10.
  4. **Verdict-line overclaims in 02.** STRICT_REVERSAL_NECESSARY and ENVELOPE_NON_SEPARABILITY_NECESSARY need the AL3 qualifier. The pack's own W5 (DL with `F_u ≡ F_E`) refutes them as written.
  5. **DL-4 proof gap**, repairable (§2.1).
  6. **Integration hazards:** two different witnesses have id `W5` (w_dl_gov and w_mono_rob_miss), and two different results are named "Lemma S" (02 and 04).
* **Recommended overall verdict: `Q1_THEORY_UPGRADE_VERDICT=PARTIAL`** (§6).

---

## 1. Requested attacks

### A1. "Is this merely relabeling?"

**Attack.** Many "theorems" re-express v2.2 facts in new notation.

**Verification.**

| New label | What it actually is | Pack's own admission |
|---|---|---|
| DL-1o/p (02 l.86–105) | 42 Lemma E′ (l.476) applied to a first-best plan, plus the definition `DL = F^B − F^C` | 02 l.107: "The proof is Lemma E′ applied to a first-best plan" |
| GS-0 (03 l.52–70) | P7 plus the cost channel | 03 l.70: "This is P7" |
| GS-I (03 l.78–82) | substitution of `F^C = F^B − DL` | 03 l.86: "GS-I is an algebraic identity" |
| D3 (04 l.127–133) | P2's proof applied at each fixed `(y,γ)` | 04 l.133 |
| Thm R1 (06 l.47–50), Lemma 0 (05 l.62–66) | 42 Lemma R and 42 l.535 with hypotheses listed | 05 l.66: "No new content" |
| E.2 (05 l.191) | the ordering 42 §13.5 already asserts | 05 l.202 |
| G5 (07 l.95) | P4 | 07 l.159 |

**Genuinely new (not relabeling):**
* Cor DL-2o: the `ΣF_u`-maximal first-best selection forces a strict reversal against the best-response set.
* Cor DL-3: a primitive iff under a unique first best.
* W3c: pairwise patterns cannot decide the sign of DL.
* DL-6: envelopes are ceilings, so cheaper or equal plans cannot be blocked.
* GS-N with W4c, W4d, W4e.
* D4 and D5: monotonicity without full alignment, which corrects 42 P4's "只有 (AL)".
* Lemma M.
* E.1-adaptive and E.2-adaptive refutations; E.4 exact VOI; E.6(e) non-convergence of 51's edge-only grid; E.7 and E.8.
* R2, R4, R5(ii): discontinuity of `V^pess` in C.
* G1–G4, and G7, which finds a false sentence in 59a l.1327.

**Severity: MAJOR** for the headline framing. The proofs themselves are fine (§2).

**Minimal correction.**
* Relabel DL-1 as "Lemma DL-1 (implementability characterization)".
* Relabel GS-I as "Identity GS-I (accounting decomposition)".
* Relabel GS-0 as "P7 restated with cost channel".
* Mark D3, R1 and Lemma 0 as "restatements with explicit hypotheses".
* Lead with the genuinely new results listed above.

### A2. "Is the DL theorem tautological?"

**Attack.** "DL = 0 iff some first best is self-enforcing at its own resource vector" restates "DL = 0 iff the first best is implementable in C". Lemma E′ already reduces C to envelopes in `{a(x)}`.

**Verification.** Correct, the result is near-tautological:
* `F^{C,m} = F^B` holds iff some C outcome attains `F^B`.
* A C outcome is B-feasible, because `P^C ⊆ P^B` and envelopes sum to at most `b̄`. So that outcome is a first best.
* The only nontrivial step is that the leader can shrink to `e = a(x̂)` without loss. That is literally Lemma E′'s argument.

The proof is correct line by line for exact ties:
* (⇐): l.92–96 is correct.
* (⇒): the shrink `BR_u(a(x̂)) ⊆ BR_u(e)` holds because `x̂` is `F_u`-maximal on the larger set.

Under 51's tolerance the proof as written fails (§2.7).

**Non-trivial content that remains:**
1. **Cor DL-2o** (02 l.111–114). The selection argument (maximize `ΣF_u` among first bests at `(y*,γ*)`) is a real step. I checked the contradiction: replacing `x°_u` by `x^H` keeps B-feasibility because only the pooled budget couples units and `a(x^H) ≤ a(x°_u)`.
2. **Cor DL-3**, the primitive iff under a unique first best. Verified.
3. **W3c**, impossibility of an iff in the predicates (A)–(F). Verified: in I1 and I2, every existential predicate (A)–(F) has the same truth value, yet DL is 2 versus 0. So no Boolean function of (A)–(F) is an iff.
4. **DL-6**, "budgets block over-spending, not misdirection". This is managerially useful, but mathematically it is Lemma S (02 l.67), a two-line fact.
5. **The opt/pess gap W3b** is the standard optimistic/pessimistic bilevel gap (Wiesemann et al., 2013, already in the reference list). It is not new as a phenomenon, only as a minimal witness.

**Severity: MAJOR** (labeling and claimed novelty). The theorem is true.

**Minimal correction.**
* Change `DL_IFF_THEOREM = PROVEN` to "PROVEN as a first-best-relative implementability characterization (Lemma); no primitive iff".
* Make Cor DL-2o, Cor DL-3 and W3c the reported DL contribution.

### A3. "Is delegation loss mechanically built into the model?"

**Attack.** DL ≥ 0 holds by construction (P1: C's feasible set is inside B's, under complete information). DL > 0 requires researcher-specified ledger splits (`v^x`, `l^x`, `τ`, `C^{impl,x}`) or unit-only constraints. So DL > 0 is an input, not a finding.

**Verification.** The *sign* is built in: 42 P1 (l.614–620) and P3 (l.630). The *magnitude* depends on unidentified ledger splits: 42 §13.4 `FOLLOWER_LEDGER_UNIDENTIFIED`. The pack handles this:
* 02 §7 (l.238) frames DL as "instrument incompleteness";
* 08 §1 states that `B ≥ C` is "an artifact of the information assumption";
* every DL witness is SIMULATED_ONLY.

What the theorems add is *when* the built-in loss is zero or positive. They do not show that it exists.

**Severity: NOT_VALID** against the pack. It becomes **MAJOR** for the manuscript if any sentence presents "DL > 0" as an empirical or theoretical finding about enterprises.

**Minimal correction.** In 59a §3.11, §5.6 and the abstract, say: "DL ≥ 0 by construction (P1, complete information); the contribution is the characterization of when DL = 0."

### A4. "Is governance screening just feasible-set pruning? Is GS-I an accounting identity?"

**Verification.**
* In v2.2 a requirement acts only through the binary flags (F5a–e), (F6) and (F9), so it only prunes `P_u`. The pack agrees (03 §2, proof of GS-0(a)).
* "Pruning the follower's option set can raise the leader's value" is the standard delegation-set insight. The principal restricts the agent's permitted set (Holmström-type delegation; Alonso & Matouschek, optimal delegation; Armstrong & Vickers, delegated project choice). These are listed as **to verify**: none is in the 59a reference list and I give no bibliographic details. 03 §10 flags Holmström and Alonso & Matouschek as to-verify; Armstrong & Vickers is missing.
* GS-I is an identity (A1).

**What survives:**
* **GS-N** (03 l.117–140), verified line by line. The case split on `BR_l ∩ P_s` is correct. `BR_s = BR_l ∩ P_s` whenever the intersection is nonempty, because the loose maximum is then attained inside `P_s`. GS-N is a clean, non-definitional *necessary* condition: a requirement helps only by excluding a loose best response that is envelope-non-separable from a surviving plan.
* **W4c, W4d and W4e** (verified numerically; e.g. W4c: `PR_B = 15 − 7 = 8`, `GSV = 7 − 10 = −3`) refute the naive "screening helps when budgets cannot separate".

**Severity: MAJOR** (positioning and labeling). No proof error.

**Minimal correction.**
* Call GS-I an identity and GSV ≤ DL_loose a corollary of P1 + P7.
* Present GS-N plus W4c/W4d/W4e as the contribution.
* Add Armstrong & Vickers (delegated project choice) to the to-verify list.

### A5. "Does any theorem depend on a hidden tie-break rule?"

**Verification.** The pack states exact ties throughout (02 l.42; 03 §11.4; 04 l.45; 05 l.141; 06 (R-e)) and covers leader ties in 04 (strict vs tie-build, l.44). Opt and pess are reported separately everywhere. There is no *hidden* rule.

What the pack did not see: 51's rule (l.673) is `tied = {F ≥ m − TOL·max(1,|m|)}`, a threshold that depends only on the affordable-set maximum `m`. Under any such rule:
* Shrinking to `a(x)` for an `x` that is *not* `F_u`-maximal can admit new near-ties.
* So 42's Lemma E′ pessimistic step ("取任一 x ∈ T") is false. Counterexample in §2.7.
* The DL-1p (⇒) proof, which picks the φ-minimizer, fails the same way.
* 02 §9.2's claim "proven for … any absolute tolerance" is not supported by the given proof.

Choosing `x̃` = the `F_u`-maximal element of the tie set keeps the maximum, so `BR(a(x̃)) = BR(e) ∩ {a ≤ a(x̃)}`. With that choice:
* Lemma E′, DL-1o and DL-1p all hold under 51's relative rule. In the per-unit sum argument, each `φ(x̃_u)` equals `min_{BR} φ` because the profile is B-feasible and its sum is at least `F^B`.
* 51's numbers are unaffected, because `envelopes_lemmaE` enumerates every `a(x)`, including `a(x̃)`.

**Severity: MINOR**. This is a proof-text gap in 42 and 02; no statement and no computed number is wrong. Upgrade opportunity: 02 §9.2 can move from NOT_PROVEN to PROVEN for 51's rule. GS-N's step `BR_s = BR_l ∩ P_s` genuinely needs exact ties, so GS-N stays exact-tie only.

**Minimal correction.**
* In 02 (and in an erratum note for 42 §12.4 at the next version bump; do not edit 42 now), replace "choose `x̂` attaining the min/max of φ" with "choose `x̃_u` = an `F_u`-maximal element of `BR_u(e_u)`" in the pessimistic shrink.
* Restate DL-1 as valid for any tie set of the form `{F ≥ g(m)}` with `g` non-decreasing and `g(m) ≤ m`.

### A6. "Does the build-region counterexample depend on pathological parameters?"

**Verification** (`t6/w5_robust.py`, an independent engine with Lemma E′ envelopes, opt and pess, on a δ-grid of step 0.01 over [0,10]).
* The W5 algebra (04 l.156–178) is reproduced: `D = 1+δ` on [0,3), `δ−4` on [3,5], 1 after.
* The phenomenon is **non-degenerate**: it holds on an open set of parameters. Random joint multiplicative perturbations of all 8 scalars (`N1, v1, b1, N2, v2, lx, b2, F_c`) keep a non-interval region in:

| perturbation | non-interval kept |
|---|---|
| ±0.5 % | 400/400 |
| ±1 % | 398/400 |
| ±2 % | 333/400 |
| ±3 % | 259/400 |
| ±5 % | 218/500 |
| ±20 % | 54/500 |

  The cause: all three margins (D(0) = 1, D(3) = −1, D(≥5) = 1) are 1 TWD against `F_c` = 24 and `N1·v1` = 30.
* It is **structurally knife-edge** in two places:

| variant | result |
|---|---|
| U2's reused cost floored at `f` = 0.01 instead of 0 | region becomes an interval |
| U2:k1 ENG footprint 1e-6 (instead of 0) | region becomes an interval; the ENG envelope always separates |
| floor 0.5 plus incremental opex −1 (negative opex is allowed by 42 §5.1/D9) | non-interval restored |

  So the mechanism needs reuse to make the misaligned unit's AI configuration weakly cheaper than its status quo in **every** pooled resource. That condition is implicit in Lemma S (04) but never stated as a hypothesis or modelling caveat.
* **Wide-margin replacement** (`t6/w5_wide.py`):
  * Inputs: `N1=10, v1=3, b1=10, N2=10, v2=2, lx=3, b2=4, F_c=17`, single resource, uniform clipped reuse.
  * D(δ): 3 on δ=0, 6.9 at 3.9, −3 at 4, −1 at 6, +3 for δ ≥ 10.
  * Region: [0,4) ∪ (7,∞) in both modes, with margins of 3.
  * Robustness: 360/400 kept at ±5 %, 237/400 at ±10 %.

**Severity: MINOR** for Prop D6, which claims existence only and is correct. It would be **MAJOR** if the manuscript uses W5 to support H-DL4 or "platform coupling" as a practically relevant phenomenon without the every-resource footprint condition.

**Minimal correction.**
* Add to 04 §6: "Non-monotonicity requires that reuse drives the misaligned unit's AI configuration to a pooled-resource footprint ≤ that of an enterprise-preferred plan in every pooled resource (incl. ENG); with any strictly positive ENG footprint or cost floor the region is an interval."
* Add the wide-margin witness, and report the perturbation radius.

### A7. "Does VOI add anything beyond standard value-of-information / minimax-regret logic?"

**Verification.**
* E.1 (fixed C) is trivial.
* E.1-adaptive and E.2-adaptive (W6b) are the classic menu-dependence (IIA failure) of minimax regret: enlarging the menu raises the regret benchmark. Known since Chernoff (1954); characterized axiomatically by Stoye. Both are to verify and neither is in the list.
* W6e (myopic VOI = 0 while joint identification removes all regret) is the standard complementarity of information.
* W6 (vertex overstatement) is already in v2.2 (42 l.590, 51 T-SEN-7); 05 adds only the minimal 2×2 witness.
* E.4 (exact sup via line arrangement) is a standard parametric piecewise-linear argument.
* **Genuinely useful:**
  * E.6(e): 51's edge-only probability grid can stay ≥ 1/2 against a true value of 1/3. This is an implementation-relevant finding, and still consistent with 42, since grid VOI remains an upper bound.
  * E.7/E.8 (termination needs finite evidence states).
  * The (F)/(Ad)/(♯) trilemma table, correctly marked "not a general impossibility".

I re-derived W6 (`F_X = v, F_Y = q`: MMR(v) = min(v, 1−v); vertex VOI 1, true 1/2), W6b, and E.6(e) (`MMR(w) = 1 − max_i w_i`). All correct.

**Severity: MAJOR** (positioning only). 05 l.309 calls these "new formal results of this thesis". They are TYPE C in-model statements with well-known analogues.

**Minimal correction.**
* Relabel as "TYPE C (in-model formalization; known analogues: minimax-regret menu dependence, VOI complementarity — to verify)".
* Keep E.6(e) and E.7/E.8 as the contribution.
* In the manuscript, present SIP as a protocol, not a theorem.

### A8. "Is the missingness framework just software engineering?"

**Verification.**
* Definition G (DC/DIER/NULL plus the FC tag) is a decision-theoretic restatement of partial identification: identified set versus robust decision set (Manski; to verify, not in the list, as 07 §8 correctly flags).
* G1–G3 are elementary monotone comparative statics. 07 itself positions this as "methodological / model-identification, not a new theory of the enterprise" (l.4).
* Substantive bits:
  * G2(iii): the C counterexample to RESTRICTED_SOLVE being a lower bound.
  * G7: 59a l.1327's "status-quo cells cancel in regret/VOI" is false. I verified it: `φ_j0 ≡ 0` while the baseline `N_j0 g_j0(ȳ^cur)` sits inside every `φ_jk` with `k ≠ 0`, so it does not cancel between `k = 0` and `k ≠ 0`.

**Severity: MINOR.** The attack is largely valid, but the pack already positions the material correctly.

**Minimal correction.** Keep this in Methods or Appendix, not among the theory contributions. Fix G4 (§2.10) and the G1 premise (§2.11).

### A9. "Are M1–M4 really irreducible, or is irreducibility an artefact of typing axioms that encode the conclusion?"

**Verification.**
* Definition 4.3 (01 l.154) plus T1–T4 (l.156–163) make IRR equivalent to: "each of the four attribute groups contains at least one attribute that some v2.2 feasibility or value map reads non-trivially". The construction (l.173–180) just varies that attribute, holding the rest fixed.
* This is a non-redundancy (no dead variable) property of the v2.2 schema under a chosen partition. It holds for *any* partition of the read attributes into four non-empty classes.
* The typing carries the conclusion:
  * Π_¬M1 uses `Eff_H`, defined in 42 §3.2 as "行動前可見資訊、足夠時間、真實否決". "Pre-action information" is as naturally an M2 (does the route deliver the output before action?) or M4 (evidence) object.
  * Retyping `Eff_H` to M2 would leave M1's irreducibility resting only on `H_k`. That is again a typing choice: `H_k = 3` is a "stop/rollback right", which 01 itself treats as an M1/M2 bridge (G16).
* 01 is honest: "without them the claim is false" (l.156); COV is "circular" (l.211); MINIMAL_SUFFICIENCY = PARTIAL.
* The word "irreducible" in "irreducible and jointly sufficient" (l.209) and in the manuscript-ready label (l.226) still oversells.

**Additional inconsistency (MINOR).** §2.7 (l.115) factors `Φ^{Leg}` as separate from `Φ^{M1}`, but COV (l.207) and Definition 2.2 (`Pol ∋ Legal_jk`, l.67) assign (F2) to M1. Pick one.

**Severity: MAJOR** (framing). No logical error.

**Minimal correction.**
* Replace "irreducible" with "non-redundant under typing axioms T1–T4 relative to the v2.2 attribute schema".
* State explicitly that IRR does not support the M1–M4 taxonomy as a theory of enterprise AI decisions: it only shows that the v2.2 schema has no dead attribute class.
* Keep `M1_M4_MINIMAL_SUFFICIENCY = PARTIAL`.

### A10. "Which contributions already exist in the literature?"

All entries are **to verify**: none is in the 59a reference list unless marked. No bibliographic details are asserted here.

| Pack result | Closest existing literature | Assessment |
|---|---|---|
| DL-1, DL-6, GS-N, P8 screening | Optimal delegation / permitted-set design (Holmström-type delegation; Alonso & Matouschek); delegated project choice (Armstrong & Vickers); principal–agent misalignment (Jensen & Meckling) | Same mechanism (the principal restricts the set; the agent picks its favourite). New here: envelope-as-ceiling instrument incompleteness, finite policy menu, and opt/pess exactness |
| Envelope = ceiling (DL-6, Lemma S) | Capital budgeting with spending limits / budget ceilings (Harris & Raviv-type models) | Known qualitatively; the formal Lemma S is trivial |
| Opt/pess bilevel, W3b, R5 discontinuity | Dempe (2002); Colson et al. (2007); Wiesemann et al. (2013), **in list**; Loridan & Morgan (to verify) on pessimistic bilevel | Known phenomenon; new only as minimal witnesses |
| D1, D3–D5 monotone comparative statics | Topkis; Milgrom & Shannon (04 l.233 already flags them as to-verify) | Elementary; D4/D5 are new in-model sufficient conditions |
| D6 non-monotone build region | "More options can hurt the principal", Braess-type paradoxes in Stackelberg games | Known type of phenomenon; the specific reuse → separability-loss chain is new in-model |
| VOI E.1-adaptive, W6e | Chernoff (minimax regret violates IIA); Stoye (minimax-regret axioms); non-submodularity of information value | Known analogues |
| Lemma R / R1, MaxRegret at vertices | Robust optimization (Ben-Tal et al., 2009, **in list**); interval minmax regret (Kouvelis & Yu; Averbakh) | Standard |
| Missingness DC/DIER | Partial identification (Manski) | Known framework, applied |
| M1–M4 | IT governance decision rights (Sambamurthy & Zmud; Brown & Grant, **in list**); levels of automation (Parasuraman et al., **in list**) | Taxonomy; TYPE B anchors are adequate |

**Severity: MAJOR.** A Q1 referee will name these.

**Minimal correction.** Add a "Relation to existing results" paragraph per document with the to-verify anchors, and change "TYPE C new formal result" to "TYPE C in-model result; mechanism known in X".

### A11. "Which results are AI-specific versus true for any generic IT portfolio?"

**Verification.** 02, 03, 04, 05, 06 and 07 use only these objects: finite plan sets, pooled resource vectors, two ledgers, a finite policy menu with binary feasibility flags, shared capabilities with source-indexed costs, and block-multilinear uncertainty. None uses `A`, `H`, `WI`, `EA`, `EAX`, `m`, `ρ`, or the AOA process.
* Every DL, GS, D, VOI, R and G result holds verbatim for an ERP, cloud-migration, or any shared-platform IT portfolio under budget envelopes.
* AI specificity enters only through:
  * the configuration attribute schema and requirement tables keyed by autonomy `A` (01 S1);
  * the response layer `ρ` (VRG, design-response regret; 42 Q6);
  * EAX as a ρ-key (M4 → M3).
* Even `ρ` (human response to automated advice) is automation-generic.

**Severity: MAJOR** (framing for an "AI" Q1 venue).

**Minimal correction.**
* State explicitly: "The portfolio-level results (DL, GS, reuse non-monotonicity, robustness scope, VOI, missingness) are properties of the enterprise–BU architecture and hold for any shared-platform IT portfolio; the AI-specific content lies in the configuration schema (M1–M4), the autonomy-keyed requirement tables, and the human-response layer."
* Optionally, give one AI-specific corollary: e.g., screening via the `EA^req(A,κ)` table acts only on configurations whose autonomy level makes the requirement bind.

---

## 2. Line-by-line proof checks and additional findings

### 2.1 02 Prop DL-4(a)/(b) — proof gap (MINOR)

* The proof (l.138) takes a first best `x*` and `e = a(x*)`, then concludes "pess-self-enforcing".
* But pess-self-enforcing (l.70) includes opt-self-enforcing, i.e. `x*_u ∈ BR_u(a(x*_u))`. That fails if some affordable `x` has `F_u(x) > F_u(x*_u)`. Hypothesis (a) then only gives `φ(x) ≥ φ(x*_u)`.
* The conclusion DL = 0 still holds:
  * Every BR element has `φ ≥ φ(x*_u)`. Strict `>` would beat `F^B` (under AL3), so all BR elements have `φ = φ(x*_u)`.
  * Take `x̃_u` = any BR element. By the shrink, `BR(a(x̃_u)) ⊆ BR(e)`, so `x̃` is a pess-self-enforcing first best.
  * Or skip DL-1: `V^pess(e) ≥ Σφ(x*) − K = F^B`.
* (b) has the same gap: "then `x*_u ∈ BR_u`" is false when another BR element is strictly preferred.

**Correction:** use the direct bound `V^m(a(x*)) ≥ F^B`, or self-enforce `x̃`, not `x*`.

### 2.2 02 verdict lines — missing AL3 qualifier (MINOR, must fix)

* l.13 `STRICT_REVERSAL_NECESSARY = YES for DL_opt` and l.15 `ENVELOPE_NON_SEPARABILITY_NECESSARY = YES` are false as stated.
* The pack's own W5 (w_dl_gov `witness_W5`) has `F_u ≡ F_E`, no reversal and no deviation, yet DL_opt = DL_pess = 1, because a unit-only constraint excludes the first-best plan.
* Cor DL-2o (l.111) does carry "[AL3]".

**Correction:** append "under AL3 (`P^C = P^B`); otherwise DL may arise from AL3 alone (W5)" to both lines. Likewise, DL-6's "exactly two sources" (l.144) must add the AL3 channel.

### 2.3 02 Cor DL-3 — drafting contradiction (MINOR)

Cor DL-3 assumes "`x*_u ∈ P^C_u` for all `u`" (l.118). Its last bullet (l.122) then treats "if some `x*_u ∉ P^C_u`".

**Correction:** move the `P^C` clause into a separate bullet with its own hypotheses.

### 2.4 02 — convention dependence of W5 (DL) (MINOR)

`P^B` drops unit-only constraints (l.50). This is a convention: 42 AL3 (l.343) allows them to be "also in the enterprise problem". If a unit-only constraint is an operational fact (service floor `s^min`), a planner that ignores it inflates `F^B`, and therefore DL.

**Correction:** state that W5's "ledger misalignment not necessary" holds under the convention that B omits unit-only constraints. Under the alternative convention, the AL3 channel disappears.

### 2.5 02 — "IMPOSSIBLE" scope (MINOR)

l.10 should read: "no Boolean combination of the existential predicates (A)–(F) as defined in §1 is an iff". I verified that all of (A)–(F) take identical truth values in W3c I1 and I2. The word "impossible" should not be extended to "pairwise primitives" in general.

### 2.6 04 — W5 robustness and Lemma M scope (MINOR)

* For W5, see A6.
* Lemma M (l.189–195) carries the hypotheses `a_u(a;δ) ≥ 0` and "no status-quo effect". The sentence "So a 1→0→1 pattern needs either ≥ 3 options … or ≥ 2 follower decision units" (l.195) drops them. It should read "under Lemma M's hypotheses".
* Lemma S (04 l.100–110) is correct for exact ties: I checked both directions and both modes. It needs the same `F_u`-maximal fix as A5 for tolerance.
* D1 (l.77–79) and D3 (l.133) are correct.
* D3's claim that the baseline difference is a `j`-constant relies on 42's own P2 assertion `φ^u = φ` under AL. 42 leaves the argument of `g^u_j0` unstated, and if it were evaluated at `ȳ`, which includes the follower's `y^loc`, it would not be plan-constant. This inherits 42's ambiguity rather than creating a new error. Add a footnote fixing `g^u_j0` at `ȳ^cur`.

### 2.7 42 Lemma E′ (pess) and 02 DL-1p under 51's tie rule (MINOR; also an upgrade)

Counterexample (`t6/tie_shrink.py`, 51's rule `F ≥ m − 1e-9·max(1,|m|)` re-implemented). One resource, plans:

| plan | a | F_u | φ |
|---|---|---|---|
| x_top | 2 | 1 | 10 |
| x_hat | 1 | 1 − 0.9e-9 | 10 |
| x_low | 0 | 1 − 1.5e-9 | −100 |

* At `e = 2`: `T = {x_top, x_hat}`, pess = 10.
* Shrinking to `a(x_hat) = 1` (x_hat ∈ T, as 42's "取任一 x ∈ T" allows): `T′ = {x_hat, x_low}`, pess = **−100**.
* Shrinking to `a(x_top)`: pess = 10.

So 42 l.476's pess sentence is false under ε_tie > 0. Lemma E′'s *statement* is true, via the `F_u`-maximal choice, and 51's values are unaffected. The same applies to the (⇒) step of DL-1p (02 l.98–102).

**Correction:** see A5. Do **not** edit 42 now; record it for the next version and in Appendix C.

### 2.8 03 — verified. One labeling issue (MINOR)

* GS-N (both modes, all three cases) and GS-1 are verified.
* The unique-first-best primitive version (l.103–107) is verified: after exclusion, every remaining affordable plan at `a(x*)` has `F_u < F_u(x*)`.
* §6 item 4's claim that the sign result needs no AL3 is correct: GS-N(ii) needs a reversal, which is impossible when `F_u = φ + const`.
* Labeling: `B_MONOTONICITY` (l.10) is P7. Mark it "restatement".

### 2.9 05 — verified. One positioning issue (A7)

* E.2 needs `V_p ⊇ vert(Θ_p)` for the middle inequality, which is stated.
* E.6(c)'s bound can be halved (`Lip·(U−L)/(2n)`). Cosmetic.
* The SIP sidecar table honestly reports that VOI policies did **not** beat RANDOM on residual regret (l.292). Keep that sentence in any manuscript use.

### 2.10 07 Prop G4 — quantifier slip (MINOR, must fix)

* Definition G (l.58): DIER requires `D*(θ^0) ⊆ RD`, i.e. **every** zero-fill optimum is robust.
* G4 (l.89): "DIER (certified) iff **some** decision is optimal at all 2^m vertices".
* Counterexample: `d1: F^{−time} = 10, ΔHours = 0`; `d2: F^{−time} = 10, ΔHours = 1`; `λ ∈ [0,4]`.
  * At `λ = 0`, `D* = {d1, d2}`.
  * `RD = {d1}`, and `d1` is optimal at both vertices.
  * G4 says DIER; Definition G says DC, because `d2 ∉ RD`.
* G4 also does not separate DIER from NULL (when `ΔHours = 0` for every optimum, `R` is constant).

**Correction:** "DIER iff every element of `D*(λ=0)` is optimal at all `2^m` vertices and `F*` is not constant on the box; NULL if additionally `F*` is constant."

### 2.11 07 Prop G1 — premise and list mismatch (MINOR)

* Premise: "p enters only constraints" (l.68).
* The list includes "`C^impl` in `a^BUD`", but `C^impl` also enters (OBJ-E) as `−C^impl`.
* The conclusion still holds, because both effects push the same way.

**Correction:** "p enters constraints and/or the objective with the same sign of effect".

### 2.12 06 R5(i) — affordability depends on θ (MINOR)

* R5(i) (l.89) asserts that `V(b;θ) = Σ max_{affordable} Ψ_u − K` is block-convex.
* Affordability `a_u(x;θ) ≤ e_u` depends on θ, because `a^BUD ∋ N·E[c]` (42 §5.1). The affordable set then switches with θ, and the max need not be block-convex.
* The counterexample W7b is unaffected (zero costs).

**Correction:** add "for θ-independent resource vectors"; otherwise defer to (iii).

### 2.13 Witness contract and literal-instance issues (MINOR)

1. **ID collision.** `id = "W5"` is used by both `w_dl_gov.witness_W5` (AL3 channel, DL) and `w_mono_rob_miss.witness_W5_delta` (reuse non-monotonicity). 07 l.99 ("W5 instance") refers to the latter. The integrator must rename them (e.g. `W5_DL_AL3`, `W5_DELTA`). Function names do not collide (checked).
2. **Name collision.** "Lemma S" means envelope separability in 02 l.67 and implementability in 04 l.100. Rename 04's to "Lemma I".
3. **Not literal v2.2 instances.** Several "minimal cores" are abstract finite bilevel instances, not literal v2.2 instances:
   * W3m: `xH` with `F_u = 1, φ = 0` read as the status quo contradicts `φ^u_{j0} = φ_{j0} = 0` (42 V2/OBJ-U). A per-unit constant shift (`F_u(xG) = −1, F_u(xH) = 0`) fixes it without changing any result.
   * W4's single-BU core and W4e: if a status quo `k0 = (a=0, F_u=0, φ=0)` is present and survives the strict rule, it ties with `xG` and gives `GSV_pess = 0`. For W4e this works only if the strict requirement also excludes the status quo, which 42 l.200 allows.

   **Correction:** add one sentence per core giving the v2.2 embedding (constant shift; status-quo treatment).
4. **Mapping to 51.** The witness engines use absolute `1e-9` ties, while 51 uses relative ties. This does not matter on integer data. State it in the assembled file header.

### 2.14 08 — verified; no overclaim

IA-1 and its corollary are correct. IA-2/IA-3 are correctly labeled as sketches. The example arithmetic checks out (minimax regret: k1 7, k2 6, so k2). Status SIDECAR_DESIGN_ONLY is appropriate. **NOT_VALID** as a target.

### 2.15 Contradictions with v2.2

None found. Three items are *corrections or sharpenings* of v2.2 or manuscript text, and should be presented as such, not hidden:
* 42 P4's "在 C 中只有 (AL) 成立時才保證單調" is shown non-necessary by D4/D5 (04 l.244 handles this);
* 59a l.1327 is false (07 G7);
* 42 l.476's pess proof text is false under ε_tie (§2.7, this review).

---

## 3. What genuinely survives (for the integrator)

1. Cor DL-2o, Cor DL-3, W3c, W5 (AL3 channel, convention-qualified), DL-6 (instrument incompleteness: envelopes are ceilings).
2. GS-N plus W4c, W4d and W4e (necessity, and the three ways a "screening" rule fails). GS-1 as a sufficient condition.
3. D4/D5 (monotonicity without full alignment), the D6 existence result with the wide-margin witness and the every-resource footprint caveat, and Lemma M.
4. R2, R4, R5(ii) (discontinuity of `V^pess` in C), and the scope sentence (06 §5).
5. E.6(e) (non-convergence of 51's edge grid), E.7/E.8, the adaptive-candidate-set warning (E.1/E.2-adaptive) as an operational caveat, and E.4.
6. G2(iii), G3(c), G7 (a manuscript error), and the corrected G4.
7. The upgraded tie result: DL-1 and Lemma E′ hold under 51's relative ε_tie once the `F_u`-maximal selection is used.

---

## 4. Severity summary

| # | Attack / finding | Location | Severity |
|---|---|---|---|
| A1 | Headline results are relabelings / restatements (DL-1, GS-0, GS-I, D3, R1, Lemma 0, E.2, G5) | 02 l.86–107; 03 l.52–86; 04 l.127–133; 05 l.62–66; 06 l.47–50 | **MAJOR** |
| A2 | DL "iff" near-tautological (Lemma E′ + definition) | 02 l.9, l.86–107 | **MAJOR** (label) |
| A3 | DL ≥ 0 built in by P1/P3 | 42 l.614–630; 02 §7; 08 §1 | NOT_VALID vs pack (MAJOR if the manuscript calls DL > 0 a finding) |
| A4 | Screening = feasible-set pruning; GS-I = identity; delegation-set literature | 03 l.78–86, §10 | **MAJOR** (positioning / label) |
| A5 | Hidden tie-break | all | NOT_VALID (exact ties stated) |
| A5′ | 42 Lemma E′ pess proof and DL-1p (⇒) proof fail under 51's ε_tie; statements survive | 42 l.476; 02 l.98–102, l.254; 51 l.673 | MINOR (proof text; upgrade possible) |
| A6 | W5 build-region witness: thin margins; knife-edge zero floor / zero ENG footprint | 04 l.156–178, l.203–205 | MINOR (existence valid; MAJOR if used as practically relevant) |
| A7 | VOI results are standard minimax-regret / VOI facts | 05 l.17–30, l.309 | **MAJOR** (positioning) |
| A8 | Missingness = methodology | 07 | MINOR |
| A9 | IRR an artefact of typing T1–T4 (non-redundancy only) | 01 l.154–180, l.209, l.226 | **MAJOR** (framing) |
| A10 | Prior literature (delegation, capital budgeting, bilevel, minimax regret, partial ID) | all | **MAJOR** |
| A11 | No result in 02–07 is AI-specific | 02–07 | **MAJOR** (framing) |
| 2.1 | DL-4 proof uses `x*` instead of a BR element | 02 l.138 | MINOR |
| 2.2 | Verdict lines lack the AL3 qualifier; refuted by the pack's own W5; DL-6 "exactly two sources" | 02 l.13, l.15, l.144 | MINOR (must fix) |
| 2.3 | Cor DL-3 contradictory hypotheses | 02 l.118–122 | MINOR |
| 2.4 | W5 (DL) depends on the B-omits-unit-only-constraints convention | 02 l.50 | MINOR |
| 2.5 | "IMPOSSIBLE" scope | 02 l.10 | MINOR |
| 2.6 | Lemma M "needs" drops hypotheses; D3 baseline argument inherits 42 ambiguity | 04 l.195, l.133 | MINOR |
| 2.9 | E.6(c) constant | 05 l.232 | MINOR (cosmetic) |
| 2.10 | G4 quantifier slip (some vs every); NULL not separated | 07 l.89 | MINOR (must fix) |
| 2.11 | G1 premise vs list | 07 l.68–69 | MINOR |
| 2.12 | R5(i) ignores θ-dependent affordability | 06 l.89 | MINOR |
| 2.13 | Witness id `W5` collision; "Lemma S" name collision; abstract cores not literal v2.2 instances | witness_parts; 02/04; 02 W3m, 03 W4 core, W4e | MINOR |
| 01-inc | `Φ^{Leg}` separate in §2.7 vs (F2) ∈ M1 in COV | 01 l.115 vs l.207 | MINOR |
| 2.14 | 08 information-asymmetry note | 08 | NOT_VALID |
| 2.15 | Contradiction with v2.2 | all | NOT_VALID (none found) |
| — | Any false main theorem | all | **none (no CRITICAL)** |

---

## 5. Claims that MUST be downgraded or relabeled

| Claim (as written) | Recommended label |
|---|---|
| `DL_IFF_THEOREM = PROVEN (Thm DL-1o/DL-1p)` | **PROVEN — Lemma DL-1 (first-best-relative implementability characterization; restatement of Lemma E′ at a first best). No primitive iff.** Cor DL-3 is the primitive iff under a unique first best. |
| `STRICT_REVERSAL_NECESSARY = YES for DL_opt` | **YES under AL3 only** (W5-DL refutes the unqualified line) |
| `ENVELOPE_NON_SEPARABILITY_NECESSARY = YES` | **YES under AL3 only** |
| `DL_IFF_IN_PAIRWISE_PRIMITIVES_A_F = IMPOSSIBLE` | **IMPOSSIBLE for Boolean combinations of the existential predicates (A)–(F) of 02 §1** |
| DL-6 "exactly two sources" | "two sources under AL3, plus the unit-only-constraint channel" |
| `EXACT_IDENTITY GSV = … = PROVEN (Thm GS-I)` | **Identity GS-I (accounting decomposition)**; GSV ≤ DL_loose as a corollary of P1 + P7 |
| `B_MONOTONICITY … PROVEN (Thm GS-0)` | **P7 restated with the cost channel** |
| Thm D3 | **P2 applied pointwise in `(y,γ)` (restatement)** |
| Thm R1, Lemma 0 | **Lemma R / 42 l.535 with explicit hypotheses (restatement)** |
| 05 "TYPE C new formal results" (E.1, E.2, W6b, W6e) | **TYPE C in-model; known analogues (minimax-regret menu dependence; VOI complementarity) — to verify** |
| `M1_M4_IRREDUCIBILITY = PROPOSITION (proof complete)` and "irreducible and jointly sufficient" (01 l.209, l.226) | **"non-redundant under typing axioms T1–T4 relative to the v2.2 attribute schema" (definitional); sufficiency internal and circular (COV); global NOT_PROVEN** |
| 07 G4 | corrected quantifier (every zero-fill optimum) |
| 42 l.476 pess proof text (no edit now) | erratum for the next 42 version: choose the `F_u`-maximal element |
| 02 §9.2 "NOT_PROVEN for relative ε_tie" | can be **upgraded to PROVEN** for tie rules `{F ≥ g(m)}` with the corrected selection (A5) |
| Any manuscript sentence presenting DL > 0, reuse non-monotonicity, or screening as AI-specific or as empirically established | "property of the enterprise–BU architecture; holds for any shared-platform IT portfolio; SIMULATED_ONLY witnesses" |

---

## 6. Recommended overall verdict

```
Q1_THEORY_UPGRADE_VERDICT=PARTIAL
```

**Justification.**
* **Why not PASS.**
  * Several headline results are restatements or identities (A1, A2, A4).
  * The irreducibility claim is definitional under the typing axioms (A9).
  * Novelty is unpositioned against delegation, capital-budgeting, minimax-regret and partial-identification literatures (A10).
  * None of the portfolio theorems is AI-specific (A11).
  * Four statements need wording fixes before they are true as written: §2.2, §2.3, §2.10, §2.11.
* **Why not FAIL.** Correctness is high: no CRITICAL error, no contradiction with v2.2, and all checked proofs valid under the stated exact-tie convention. The pack is unusually explicit about NOT_PROVEN items, circularity (COV) and scope. It contains real in-model contributions (§3), and it exposes three genuine errors in the canonical or manuscript text (59a l.1327; 42 P4's "只有 (AL)"; 42 l.476's pess proof text).
* **What would move it to PASS.**
  * Apply the relabels in §5.
  * Add a literature-relation paragraph and an AI-specificity scope statement.
  * Fix the MINOR must-fix items (§2.1–2.3, 2.10, 2.13).
  * Replace or augment W5 with a wide-margin witness, plus the every-resource footprint caveat.

---

## 7. RECOMMENDED_STATUS per final-status key

```
M1_M4_MINIMAL_SUFFICIENCY                  = PARTIAL  (non-redundant under T1-T4 relative to v2.2 schema [definitional];
                                                       internal closure COV, circular; global sufficiency NOT_PROVEN;
                                                       do not use "irreducible" or "minimal sufficient" unqualified)
DL_NECESSARY_CONDITIONS                    = PROVEN   (DL-1 quantifier over all first bests; Cor DL-2o strict reversal [opt]
                                                       and DL-2p weak reversal [pess] + envelope non-separability
                                                       UNDER AL3; AL3 failure alone suffices otherwise (W5-DL))
DL_SUFFICIENT_CONDITIONS                   = PROVEN   (for DL=0: DL-4 after the proof repair in section 2.1;
                                                       for DL>0: Cor DL-3 under a unique first best only)
DL_IFF_THEOREM                             = PROVEN_AS_CHARACTERIZATION_LEMMA (first-best-relative; restatement of
                                                       Lemma E' implementability; primitive iff NOT_PROVEN and impossible
                                                       in Boolean combinations of (A)-(F) per W3c)
GOVERNANCE_SCREENING_SUFFICIENT_CONDITION  = PROVEN   (GS-1; near-definitional via DL-1; primitive form under unique first best)
GOVERNANCE_SCREENING_NECESSARY_CONDITION   = PROVEN   (GS-N; exact ties only; genuinely non-definitional)
GOVERNANCE_SCREENING_WITNESS               = CONSTRUCTIVE_EXAMPLE_PASS (W4 = P8 10->15 reproduced; W4b-W4e PASS; state the
                                                       v2.2 embedding of single-BU cores re status quo)
SHARED_CAPABILITY_NONMONOTONICITY_PROPOSITION = PROVEN (existence, Prop D6; D1, D3 [restatement of P2 pointwise], D4, D5,
                                                       Lemma M proven; Conjecture M2 NOT_PROVEN)
MODEL_C_BUILD_REGION_NONINTERVAL_WITNESS   = CONSTRUCTIVE_EXAMPLE_PASS_FRAGILE_MARGINS (open-set but ~1% robustness radius;
                                                       requires zero floor / zero ENG footprint; add wide-margin witness
                                                       [N1=10,v1=3,b1=10,N2=10,v2=2,lx=3,b2=4,F_c=17: region [0,4)U(7,inf)]
                                                       and the every-resource footprint caveat)
VOI_VERTEX_OVERSTATEMENT_COUNTEREXAMPLE    = CONSTRUCTIVE_EXAMPLE_PASS (pre-existing in v2.2 T-SEN-7; minimal 2x2 witness W6 new)
SEQUENTIAL_IDENTIFICATION_PROPERTIES       = PROVEN_FOR_FIXED_CANDIDATE_SET (E.1, E.2, E.4, E.7, E.10; adaptive versions
                                                       REFUTED by W6b; SIP = protocol EXTENSION; known minimax-regret/VOI
                                                       analogues - relabel novelty)
ROBUSTNESS_SCOPE_FORMALIZED                = PROVEN   (R1 = Lemma R restated with hypotheses; R2, R4, R5 new; fix R5(i)
                                                       affordability caveat)
MISSINGNESS_CLASSIFICATION_FORMALIZED      = PROVEN_METHODOLOGICAL (after the G4 quantifier fix and G1 premise fix; position
                                                       as methods, not theory; G7 manuscript flag stands)
```
