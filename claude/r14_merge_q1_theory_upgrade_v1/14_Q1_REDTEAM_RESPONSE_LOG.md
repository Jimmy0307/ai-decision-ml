# 14 — Q1 Theory Upgrade: response log to the Reviewer #2 red-team report (agent T7)

**Date:** 2026-10-15. **Input:** `11_Q1_THEORY_UPGRADE_REVIEWER_2_REDTEAM.md` (T6). It was read in full and not modified.

**Files changed (minimal edits; each edit is tagged "T7" in the text):** Q\01–07, Q\09, Q\10, `q1_theory_witnesses.py` and `q1_theory_witnesses_output.txt`.

**New files:**
* `13_Q1_CANONICAL_42_ERRATUM_CANDIDATE.md`
* `witness_parts\w_w5_wide.py`
* this log

**Not modified:** REPO (42, 51, 59a and everything else), `11_*`, `baseline\`, 08 (the red team found nothing to fix there), and the code of every existing witness.

**Pre-edit copies:** Q\01–11, the script and the output are kept in the session scratchpad `t7/orig/` for diffing.

**Action vocabulary:**
* **FIXED**: the text or code was corrected.
* **RELABELED**: a status or name label was changed to match what is actually proven.
* **DOWNGRADED**: the scope or status of a claim was weakened.
* **RECORDED_ONLY**: the finding is accepted, but no pack change is needed or possible (for example, it targets 42 or the manuscript).
* **NOT_ACCEPTED**: rejected, with a reason.

## 1. Per-finding log

| Finding (11 §) | Severity (T6) | Action | What was done | File / section changed |
|---|---|---|---|---|
| A1 Headline results are restatements (DL-1, GS-0, GS-I, D3, R1, Lemma 0, E.2, G5) | MAJOR | **RELABELED** | Each item now carries its restatement label: DL-1 = characterization lemma; GS-0 = P7 plus the cost channel; GS-I = identity; D3 = P2 applied pointwise; R1 = Lemma R; Lemma 0 / E.2 / E.3 / E.10 = restatements; G4 = R1 applied to the λ box; G5 = P4. A "Restatement vs genuinely new (TYPE C)" list was added to each document. | 02 verdict + table + §2 + §7; 03 header/verdict + table + §2–3 + §10; 04 header + D3 + §8; 05 §0 + §7; 06 verdict + R1 + §6; 07 §8 + new list; 10 rows 1.2, 2.1, 4.1–4.3, 8.3, §9, §11 |
| A2 DL "iff" is near-tautological | MAJOR | **RELABELED** | `DL_IFF_THEOREM` now reads "PROVEN only as Lemma DL-1o/p, a first-best-relative implementability characterization lemma (Lemma E′ at a first best)". The primitive iff is NOT_PROVEN in general. Cor DL-2o, Cor DL-3, W3c and DL-6 are now presented as the DL contribution. | 02 verdict, §2 label, §7; 10 rows 1.2, 1.5, 4.1, 8.3, §9 item 1 |
| A3 `DL ≥ 0` is built in by construction (P1/P3) | NOT_VALID vs pack (MAJOR for the manuscript) | **RECORDED_ONLY** | The pack already frames this correctly. A manuscript guard was added: "`DL ≥ 0` by construction (P1); the contribution is the characterization of when `DL = 0`". | 02 restatement table row; 10 §9 item 1, §13 R-2 |
| A4 Screening is feasible-set pruning; GS-I is an identity; delegation-set literature | MAJOR | **RELABELED** | GS-I is now "Identity GS-I (accounting decomposition)". New Cor GS-I′ (`GSV ≤ DL_loose`, a corollary of P1 + P7). GS-0 is labelled "P7 restated". GS-N and W4c–W4e are presented as the contribution. Armstrong & Vickers (delegated project choice) was added to the to-verify list. | 03 header, verdict, §2, §3, §10; 10 rows 2.8, 4.2, §9 item 2 |
| A5 Hidden tie-break | NOT_VALID | **RECORDED_ONLY** | Exact ties are stated throughout; no change needed. | — |
| A5′ / §2.7 42 Lemma E′ pessimistic proof and the DL-1p (⇒) proof fail under 51's `ε_tie` | MINOR (upgrade possible) | **FIXED** (and upgrade applied, with one qualifier) | DL-1p (⇒) now chooses the `F_u`-maximal tie element and uses the per-unit sum argument. New 02 §2.2 proves Lemma E′ and DL-1o/p for every tie rule `{F_u ≥ g(m)}` with `g` non-decreasing and `g(m) ≤ m`, which includes 51's relative rule, **under exact affordability**. 02 §9.2 was upgraded from NOT_PROVEN to PROVEN. Qualifier: 51's absolute affordability slack (`a ≤ e + 1e-9`, 51 l.667) is not covered. The red team did not mention it, so it is stated as open. The erratum candidate for 42 l.476 is recorded with the counterexample, the repair, and "51 numbers unaffected". 42 itself is not modified. Falsification search: `t7/tol_fuzz.py`, 0 violations. | 02 §0 tie convention, §2 proof, §2.2 (new), §8, §9.2; 03 §11.4; 04 §9; 09 NOT_PROVEN list; 10 rows 4.1, §10, §13 R-1; **13 (new)** |
| A6 W5 has thin margins and two knife-edge zeros | MINOR (MAJOR if used as practically relevant) | **FIXED** | Canonical W5 is unchanged and still reproduces T-SEN-8 exactly. New supplementary witness **W5_WIDE** uses the red-team instance and gives region `[0,4) ∪ (7,∞)`. It includes a deterministic perturbation check: private seed 20261015, 400 draws per radius. Results: W5_WIDE 367/400 at ±5 % and 256/400 at ±10 %; W5 398/400 at ±1 % and 162/400 at ±5 %. A knife-edge check is also included: ENG footprint `1e-6` or a cost floor of `0.01` turns the region into an interval, for both W5 and W5_WIDE. The every-resource footprint caveat and a W5 fragility note were added to 04 and 09. | `q1_theory_witnesses.py` (part T7 + registry row + randomness docstring); `witness_parts\w_w5_wide.py`; output file; 04 verdict + §6 + §8 + §10; 09 verdict, notes, row; 10 row 4.3, §7, §13 R-5 |
| A7 VOI results are standard minimax-regret / VOI facts | MAJOR (positioning) | **RELABELED** | Label changed to "TYPE C in-model; known analogues (minimax-regret menu dependence — Chernoff, Stoye; VOI complementarity) — TO VERIFY". E.6(e) and E.7/E.8 are now the contribution. SIP is labelled a protocol, not a theorem. The sentence that VOI policies did not beat RANDOM is kept. | 05 §0 (new block), §7 rows, §8; 10 row 2.9, §9 |
| A8 Missingness is methodology | MINOR | **RELABELED** | The pack already positions it as methodology. Added: "known framework applied" (partial identification, to verify), the restatement vs new list, and a recommendation to place it in Methods or the Appendix. | 07 §8 row + new paragraph |
| A9 IRR is an artefact of typing axioms T1–T4 | MAJOR (framing) | **RELABELED** | "Irreducible" is replaced by "non-redundant under typing axioms T1–T4 relative to the v2.2 attribute schema (definitional; holds for any partition; does not validate the taxonomy)". Added an `Eff_H` retyping example, a terminology note, and new manuscript labels. `M1_M4_MINIMAL_SUFFICIENCY` stays PARTIAL. | 01 verdict, §4 note, §5.1 title, §5.2 item 0, §6.2, §6.3 label, §9, §10; 09 W_MECH_ABL row; 10 rows 1.1, 3.2, §9 item 6 |
| A10 Prior literature (delegation, capital budgeting, bilevel, minimax regret, partial identification) | MAJOR | **FIXED** (positioning added; citations remain TO VERIFY) | Each document gets a "known analogues — TO VERIFY" pointer: optimal delegation and delegated project choice (02, 03); capital-budget ceilings (02); Braess-type and Topkis (04); minimax-regret menu dependence and VOI complementarity (05); interval minmax regret and pessimistic bilevel (06); partial identification (07); IT-governance anchors (01). No bibliographic details were invented. Where a year appeared only in 11, it is marked unverified. | 01 §9; 02 §7; 03 §10; 04 §8; 05 §7; 06 §6; 07 §8; 10 rows 2.8, 2.9, §9, §13 R-4 |
| A11 No result in 02–07 is AI-specific | MAJOR (framing) | **FIXED** | An "AI-specificity" paragraph was added to every document. Results 02–07 hold for any shared-platform IT portfolio. The AI-specific content is the M1–M4 schema, the autonomy-keyed requirement tables and the response layer ρ. One AI-specific corollary (EA^req screening binds only where the autonomy level makes it bind) is stated as a corollary, not as a new result. A mandatory sentence was added to 10. | 01 §9; 02 §7; 03 §10; 04 §8; 05 §8; 06 §6; 07 §8; 10 §9, §13 R-3 |
| §2.1 DL-4 proof uses `x*` instead of a BR element | MINOR | **FIXED** | The proof now gives the direct bound `V^m(a(x*)) ≥ F^B` for (a) and (b), plus the equivalent DL-1 route via `F_u`-maximal `x̃`. | 02 Prop DL-4 proof |
| §2.2 Verdict lines lack the AL3 qualifier; DL-6 "exactly two sources" | MINOR (must fix) | **DOWNGRADED** (scope restricted) | STRICT_REVERSAL_NECESSARY and ENVELOPE_NON_SEPARABILITY_NECESSARY now hold "UNDER AL3", with the W_DL_AL3 exception. DL-6 reads "under AL3, exactly two sources", plus a third channel without AL3 (unit-only exclusion). Q-table row 5 is qualified. | 02 verdict, DL-6, §3 rows 1 and 5 |
| §2.3 Cor DL-3 has contradictory hypotheses | MINOR | **FIXED** | Restated as a standing hypothesis (H0, unique first best) plus Part (i) (first best available in C) and Part (ii) (AL3 fails on the first best), each with its own proof. Re-verified by hand against W3 (5/5), W3b (0/1), W3c-I1 (2/2), W3c-I2 (H0 fails; DL-1 gives 0/0) and W_DL_AL3 (Part (ii), 1/1). `work/B/fuzz_dl_gov.py` was re-run: 2,221 unique-first-best checks covering both parts, 0 violations. No downgrade was needed. | 02 Cor DL-3 |
| §2.4 W5 (DL) depends on the convention that B omits unit-only constraints | MINOR | **FIXED** | Convention note added. Under the alternative convention, the AL3 channel disappears. | 02 §1 |
| §2.5 "IMPOSSIBLE" scope | MINOR | **DOWNGRADED** (scope restricted) | Now restricted to Boolean combinations of the existential predicates (A)–(F) of §1. It is not claimed for "pairwise primitives" in general. | 02 verdict, §9; 09 W3c row; 10 row 4.1, §10 |
| §2.6 Lemma M "needs" sentence drops its hypotheses; D3 baseline ambiguity; 04 Lemma S tolerance | MINOR | **FIXED** (Lemma M, D3) / **RECORDED_ONLY** (Lemma I tolerance) | Lemma M sentence now reads "under Lemma M's hypotheses". D3 gets a footnote fixing `g^u_j0` at `ȳ^cur` (this inherits 42's ambiguity). Lemma I under tolerance needs the same `F_u`-max fix; it is noted as exact-tie only and not re-proved. | 04 §5.3, §4 footnote ¹, §9 |
| §2.7 = A5′ | MINOR | see A5′ | — | — |
| §2.8 03 `B_MONOTONICITY` is P7 | MINOR | **RELABELED** | Labelled "RESTATEMENT: GS-0 = 42 P7 restated with the cost channel". | 03 verdict, §2 |
| §2.9 05 E.6(c) constant; keep the SIP-vs-RANDOM sentence | MINOR (cosmetic) | **FIXED** | Bound tightened to `Lip·(U−L)/(2n)` (the old bound was also valid). The sidecar sentence is reinforced in the novelty block. | 05 §6(4)(c), §0 block |
| §2.10 07 G4 quantifier slip; NULL not separated | MINOR (must fix) | **FIXED** | G4 now requires **every** zero-fill optimum to be optimal at all `2^m` vertices. DC, NULL and DIER are separated by exact vertex checks. The red-team counterexample (`d1`, `d2`) is included. W8b/W8c classes were re-checked: still DC/DIER. | 07 Prop G4, verdict line; 10 §11 C.10.7 |
| §2.11 07 G1 premise vs list | MINOR | **FIXED** | Premise is now "constraints and/or the objective with the same sign of effect"; the proof wording was adjusted to match. | 07 Prop G1 |
| §2.12 06 R5(i) ignores θ-dependent affordability | MINOR | **FIXED** | Added "for θ-independent resource vectors; otherwise (iii)". W7b is unaffected. | 06 Prop R5(i) |
| §2.13.1 Witness id `W5` collision | MINOR | **FIXED** | The T5 integrator had already renamed it to W_DL_AL3 in the script. T7 renamed the remaining 02 references (`W5` → `W_DL_AL3`). | 02 verdict, §3, §4, §8, files line |
| §2.13.2 "Lemma S" name collision | MINOR | **FIXED** | 04's lemma is renamed **Lemma I** (9 occurrences). 02's Lemma S is unchanged. | 04 throughout; 10 rows 4.3, C.10.4 |
| §2.13.3 Single-BU cores are not literal v2.2 instances | MINOR | **FIXED** | Embedding notes added: W3m (constant shift `F_u(xG) = −1`, `F_u(xH) = 0`); W4 core (status-quo tie; literal variant with `F_u` raised by 1 gives GSV = 1 in both modes); W4e (requires the strict rule to exclude `k = 0`, which 42 l.200 allows; otherwise GSV_pess = 0). | 02 §3 scope labels; 03 §8 (W4 core), §6 (W4e); 09 rows W3m, W4e |
| §2.13.4 Witness engines use absolute ties, 51 uses relative ties | MINOR | **FIXED** | Stated in the script docstring and in 09. | `q1_theory_witnesses.py` header; 09 |
| §2.14 08 information-asymmetry note | NOT_VALID | **RECORDED_ONLY** | No change; 08 untouched. | — |
| §2.15 Contradictions with v2.2 | NOT_VALID (none found) | **RECORDED_ONLY** | The three sharpenings are presented openly: D4/D5 versus 42 P4's "只有 (AL)" (04 §7, already present); 59a l.1327 is false (07 G7 / 10 D-a, already present); 42 l.476 → Q/13 (new). | 13; 10 §13 R-1 |
| 01-inc `Φ^{Leg}` separate in §2.7 vs (F2) ∈ M1 in COV | MINOR | **FIXED** | `Legal_jk` (F2) moved into `Φ^{M1}`; the separate `Φ^{Leg}` factor was removed. This is consistent with Def 2.2 and COV. | 01 §2.7 |

## 2. Action counts

There are 30 rows. A5′ and §2.7 share one row, and §2.6 counts once under FIXED.

| Action | Count | Findings |
|---|---|---|
| FIXED | 17 | A5′/§2.7, A6, A10, A11, §2.1, §2.3, §2.4, §2.6, §2.9, §2.10, §2.11, §2.12, §2.13.1, §2.13.2, §2.13.3, §2.13.4, 01-inc |
| RELABELED | 7 | A1, A2, A4, A7, A8, A9, §2.8 |
| DOWNGRADED | 2 | §2.2, §2.5 (scope restricted) |
| RECORDED_ONLY | 4 (+1 partial) | A3, A5, §2.14, §2.15 (+ §2.6 Lemma I tolerance part) |
| NOT_ACCEPTED | 0 | — |

**Partial acceptance (not a rejection).** On A5′, T6 said 02 §9.2 "can be upgraded to PROVEN for 51's rule". It is upgraded for 51's **tie** rule under exact affordability. 51 also applies an absolute affordability slack (`a ≤ e + 1e-9`, 51 l.667), which neither the red-team argument nor this repair covers. That slack is stated as open and is immaterial whenever no plan's resource coordinate lies in `(e_h, e_h + 1e-9]`.

## 3. Witness verification

```
Q1_WITNESS_VERDICT        : PASS (27/27 witnesses; 7/7 canonical cross-checks; baseline anchors MATCH)
witness_set_sha256        : f5814c969e5b73479b05c29fbfdf809f44947d88dc0ff407b6b60a5bea5636a0
W5_WIDE witness_sha256    : f05b23d58f7498ce65ffead74b80611211e65fb6e1338dbb1ab614bfd25f0143
script sha256             : ab5bcb3811fe302c5d8e80159c05c36d871ab60fa23be5297f5d0ef27b93fcd4
output file sha256        : b4375bed036385828da5e48c021f5e3a6402660d20acdf826aaba8dcf64bdc0c
determinism               : run A (fresh, PYTHONHASHSEED=0) and run B (fresh, -I, PYTHONHASHSEED=random) byte-identical;
                            run C (fresh, PYTHONHASHSEED=777, --hashes) per-witness hashes identical; in-process 2-run check PASS;
                            the 26 pre-existing per-witness hashes are unchanged from T5's run of 2026-10-14
```

## 4. Status changes

* **02 §9.2: NOT_PROVEN → PROVEN** for Lemma DL-1o/p and Lemma E′ under 51's relative `ε_tie` (any `{F ≥ g(m)}` with `g` non-decreasing, `g(m) ≤ m`), under exact affordability.
  * Cor DL-2/3/4/5, Lemma S, Lemma I and GS-N remain exact-tie results.
  * 51's absolute affordability slack is open.
* `DL_IFF_THEOREM`: relabeled. It is a characterization lemma (restatement-level); a primitive iff is NOT_PROVEN, except Cor DL-3 under a unique first best.
* STRICT_REVERSAL / ENVELOPE_NON_SEPARABILITY necessity: restricted to AL3.
* IMPOSSIBLE: restricted to Boolean combinations of (A)–(F).
* `M1_M4_IRREDUCIBILITY`: relabeled to "non-redundant under T1–T4 relative to the v2.2 schema" (definitional).

## 5. Recommended final status (T7)

```
M1_M4_MINIMAL_SUFFICIENCY                     = PARTIAL   non-redundancy under T1-T4 is definitional; sufficiency only internal/circular (COV); global NOT_PROVEN
DL_NECESSARY_CONDITIONS                       = ESTABLISHED  Lemma DL-1 (every first best; now tolerance-robust); Cor DL-2o/2p (reversal + non-separability) UNDER AL3; AL3 channel otherwise
DL_SUFFICIENT_CONDITIONS                      = ESTABLISHED  DL=0: DL-4 (proof repaired); DL>0: Cor DL-3 (unique first best, Parts i/ii) and DL-1 jointly; no primitive sufficient condition without uniqueness
DL_IFF_THEOREM                                = NOT_PROVEN   only a first-best-relative characterization lemma (restatement of Lemma E'); primitive iff impossible in Boolean combos of (A)-(F); Cor DL-3 under uniqueness only
GOVERNANCE_SCREENING_SUFFICIENT_CONDITION     = PASS      GS-1 (near-definitional via DL-1; primitive form under a unique first best)
GOVERNANCE_SCREENING_NECESSARY_CONDITION      = PASS      GS-N proven, non-definitional (exact ties only)
GOVERNANCE_SCREENING_WITNESS                  = PASS      W4 reproduces P8 10->15; W4b-W4e PASS; single-BU core embeddings now stated
SHARED_CAPABILITY_NONMONOTONICITY_PROPOSITION = PASS      Prop D6 (existence) + D1, D3 (restatement), D4, D5, Lemma M proven; Conj M2 NOT_PROVEN; every-resource footprint caveat stated
MODEL_C_BUILD_REGION_NONINTERVAL_WITNESS      = PASS      W5 reproduces T-SEN-8 exactly but margins are fragile (162/400 at +-5%); W5_WIDE 367/400 at +-5%; both rest on two exact zeros
VOI_VERTEX_OVERSTATEMENT_COUNTEREXAMPLE       = PASS      W6 exact (vertex 1 vs true 1/2); phenomenon pre-exists in v2.2 T-SEN-7, minimal 2x2 witness new
SEQUENTIAL_IDENTIFICATION_PROPERTIES          = PARTIAL   E.1/E.2/E.4/E.7/E.10 proven for a FIXED candidate set; adaptive versions refuted (W6b); VOI-greedy optimality open; known analogues; SIP is a protocol
ROBUSTNESS_SCOPE_FORMALIZED                   = YES       R1 (= Lemma R with hypotheses), R2, R4, R5 (R5(i) qualifier added), scope sentence
MISSINGNESS_CLASSIFICATION_FORMALIZED         = YES       Def G + G1-G8 after the G4 quantifier fix and G1 premise fix; methodological, not theory
Q1_THEORY_UPGRADE_VERDICT                     = PARTIAL   all must-fix items repaired and relabels applied, no CRITICAL error; but the novelty is narrower than the original
                                                          headlines, the known-analogue citations are still TO VERIFY, and the T7 edits have not been re-reviewed. PASS is
                                                          reachable once the researcher verifies citations (10 §13 R-4) and accepts the 42 erratum decision (R-1)
```

## 6. T8-fix pass (independent verifier T8, `15_Q1_T7_REPAIR_VERIFICATION.md`; applied by T7, 2026-10-15)

Only the text changes that T8 specified were applied. Each one is tagged "T8-fix" in the file.

| T8 item | Change | File / section |
|---|---|---|
| §1 Q1a / text change 1 | The tie-tolerance upgrade is now stated as **QUALIFIED**. It holds for every `{F_u ≥ g(m)}` with `g` non-decreasing and `g(m) ≤ m`, which covers 51's l.673 rule, **only under exact affordability**. 51's `+1e-9` affordability slack (l.667) is not covered; T8's 2-plan counterexample is cited, together with the condition under which 51 coincides with the exact model. Cor DL-2…DL-5, Lemma S, Lemma I and GS-N remain exact-tie results. | 02 verdict line `DL_1_UNDER_TIE_TOLERANCE`, §2.2 Scope (1), §9.2 |
| §1 Q1b / text change 2 | "false … under any `g(m) < m`" changed to "fails … under any tie rule with `g` strictly increasing near `m` (every absolute tolerance and 51's relative rule)". The same weakening is applied in 13, and the slack counterexample is added there. | 02 §2.2; 13 §2, §4 |
| §3 Q3a, Q3b | Prop DL-4 header now reads "[multi-BU; AL3; exact ties]", with the W_DL_AL3 failure note. The false "Equivalently…" parenthetical is replaced by T8's wording. | 02 Prop DL-4 |
| §4.4 | The W5/W5_WIDE caveat is reworded in terms of the **net** BUD footprint relative to the status quo, restricted to the W5/W5_WIDE family. The "two exact zeros" wording is reworded the same way. | 04 `W5_FRAGILITY` verdict line, §6 caveat, §6 fragility paragraph |
| §5 R-a | 02 §3 table: the Status column of rows 5–9 now reads "Lemma (DL-1) + corollary" or "Counterexample / Lemma", and row 9 is titled "results". | 02 §3 |
| §5 R-b | Bare "irreducibility" replaced by "non-redundancy (IRR, under T1–T4)" in the title, the §5 heading, the §6.1 heading and first sentence, and l.277 (two occurrences). l.266 ("genuinely irreducible to the static model") is unrelated usage and is kept, as T8 allows. | 01 |
| §5 R-c, R-d, R-e | Thm R1, D1 and D3 are tagged as restatements in rows 1.3, 1.4, 1.6, 4.3, 6.1, 8.4, 8.5, C.10.4 and C.10.6. §9 items 3 and 4 now list D4–D6 / Lemma M and R2 / R4 / R5(ii), with D1, D3 and R1 marked as restatements. Row 1.2 now reads "The characterization (Lemma DL-1) quantifies…". | 10 |
| §5 R-f | No change required, as T8 states. | — |
| §5 informational | Witness text "Theorem DL-1" / "Thm DL-1(p)" changed to "Lemma DL-1 (first-best-relative characterization)". This touches 2 hashed minimality strings (W3b, W3c) and 3 comments/docstrings. The witness logic is unchanged. The 51 docstring is not edited (no REPO edits). | `q1_theory_witnesses.py`; `witness_parts\w_dl_gov.py` |
| rerun | Three runs, all PASS (27/27), byte-identical, with determinism PASS: fresh process with PYTHONHASHSEED=0; fresh process with `-I` and PYTHONHASHSEED=random; and `--hashes` with PYTHONHASHSEED=777. New **witness_set_sha256 = a68664cefa61f4d23e00982309c09afe77b74b5db3ba9e70b4607043fa29f8f1**. The script sha256 is `ff9d26eb…3e46` and the output sha256 is `2834bd4f…71ea8`. Only the W3b and W3c hashes changed. | output file; 09 verdict block and W3b/W3c rows |

**Pre-T8 copies:** the session scratchpad `t7/pre_t8/`.

**Status changes from the T8 pass:**
* `DL_1_UNDER_TIE_TOLERANCE` is now QUALIFIED.
* DL-4 (`DL_SUFFICIENT_CONDITIONS`) is now valid as stated, because AL3 appears in the statement.

**Section 5 statuses after the T8 pass.**
* `MODEL_C_BUILD_REGION_NONINTERVAL_WITNESS`: its justification now refers to net-BUD-footprint and ENG zeros rather than "two exact zeros".
* All other statuses are unchanged.
