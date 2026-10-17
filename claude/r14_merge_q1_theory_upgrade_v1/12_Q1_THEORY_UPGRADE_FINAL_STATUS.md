# 12 — Q1 Theory Upgrade Pack: Final Status

**Date:** 2026-10-15
**Folder:** `outputs\00_CURRENT\Q1_THEORY_UPGRADE_V1_20261014\`
**Branch:** none; this pack is not committed to git.

**Inputs (read-only):**
- canonical v2.2 model `42_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md` (sha256 `0249e7b9…`);
- solver `51_enterprise_portfolio_solver_v2_2.py` (`37f26a52…`);
- manuscript 59a (V1.8.5a), used for planning only.

```
BASELINE_V2_2_REPRODUCTION = PASS            (V2_2_SYNTHETIC_ENGINEERING_VERDICT: PASS; baseline\BASELINE_V2_2_RUN_STDOUT.txt)
CANONICAL_V2_2_CHANGED = NO                  (42 0249e7b9…, 51 37f26a52… unchanged; repo worktree clean)
CODER_INSTRUMENT_CHANGED = NO                (S1d CODER_1/2/3 387c9bed… / 796f0666… / 2f24b78e… unchanged, repo + local distribution copies)
STUDY1_BASELINE_CHANGED = NO
G01_G16_CHANGED = NO                         (11_Priority_Gaps… 76a2a00c… unchanged; no G17; sensitivity cell not added)
HUMAN_RESULTS_CREATED = NO
ENTERPRISE_RESULTS_CREATED = NO

M1_M4_MINIMAL_SUFFICIENCY = PARTIAL
DL_NECESSARY_CONDITIONS = ESTABLISHED
DL_SUFFICIENT_CONDITIONS = ESTABLISHED
DL_IFF_THEOREM = NOT_PROVEN
GOVERNANCE_SCREENING_SUFFICIENT_CONDITION = PASS
GOVERNANCE_SCREENING_NECESSARY_CONDITION = PASS        (exact-tie scope)
GOVERNANCE_SCREENING_WITNESS = PASS
SHARED_CAPABILITY_NONMONOTONICITY_PROPOSITION = PASS    (existence result)
MODEL_C_BUILD_REGION_NONINTERVAL_WITNESS = PASS          (canonical W5 margins fragile; W5_WIDE added)
VOI_VERTEX_OVERSTATEMENT_COUNTEREXAMPLE = PASS
SEQUENTIAL_IDENTIFICATION_PROPERTIES = PARTIAL
ROBUSTNESS_SCOPE_FORMALIZED = YES
MISSINGNESS_CLASSIFICATION_FORMALIZED = YES
INFORMATION_ASYMMETRY = SIDECAR_DESIGN_ONLY

Q1_THEORY_DEPTH_IMPROVED = YES
Q1_THEORY_UPGRADE_VERDICT = PARTIAL
```

## Basis for each status

| Key | Status | Basis (file) |
|---|---|---|
| M1–M4 | PARTIAL | Formal definitions are given, with boundaries defined by the object of the decision. Non-redundancy holds under typing axioms T1–T4, but those axioms make it definitional. Coverage is internal to v2.2 and circular (COV). Global sufficiency is NOT_PROVEN, with named residuals: information asymmetry, pure accountability allocation, procurement/data rights, AI-to-AI chains, and time. Adopted label: "non-redundant, jointly sufficient working set for the v2.2 static model; otherwise a conceptual decomposition". (01) |
| DL necessary | ESTABLISHED | Lemma DL-1 (first-best-relative characterization, i.e. Lemma E′ applied to a first best) holds over all first-best solutions. Strict reversal plus envelope non-separability (DL-2o/2p) is necessary under AL3; without AL3 the unit-only-constraint channel applies (W_DL_AL3). (02) |
| DL sufficient | ESTABLISHED | DL = 0: Prop DL-4, with the proof repaired and the AL3 / exact-tie scope stated. DL > 0: Cor DL-3 under a unique first best; the hypotheses are repaired and checked by an independent verifier. (02, 15) |
| DL iff | NOT_PROVEN | Only a first-best-relative characterization is proven, and it restates Lemma E′. A primitive iff is impossible in Boolean combinations of (A)–(F) (W3c). Cor DL-3 gives an iff only under a unique first best. Tie tolerance is QUALIFIED: it covers 51's relative ε_tie only under exact affordability, not 51's +1e-9 affordability slack. (02, 13, 15) |
| Screening sufficient | PASS | GS-1. GS-I is an accounting identity; GSV ≤ DL_loose follows from P1 + P7. (03) |
| Screening necessary | PASS (exact ties) | GS-N, non-definitional. With ties, GSV_pess can be > 0 even under alignment (W4e). (03) |
| Screening witnesses | PASS | W4 reproduces P8 10 → 15. Opposite and negative cases: W4b 15 → 10, W4c 10 → 7, W4d 10 → 9. (03, 09) |
| Shared-capability non-monotonicity | PASS (existence) | Prop D6: the build region need not be an interval. D1 is P7-type Model B monotonicity and D3 is P2 at fixed (y,γ); both are restatements. D4, D5 and Lemma M are new. Conjecture M2 is open. (04) |
| Build-region witness | PASS | W5 reproduces T-SEN-8's 1,1,1,1,0,0,0,1 exactly, but with fragile margins (162/400 survive ±5%). W5_WIDE survives 367/400 at ±5%. Both rely on a zero net BUD footprint. (04, 09) |
| VOI vertex overstatement | PASS | W6: vertex VOI 1 vs true 1/2, derived analytically. The phenomenon already appears in v2.2 T-SEN-7. (05) |
| Sequential identification | PARTIAL | MMR monotonicity, VOI ≥ 0, nested-grid monotonicity and finite-state termination are proven for a fixed candidate set. Adaptive candidate-set versions are refuted (W6b). VOI-greedy optimality is NOT_PROVEN. Continuous-evidence termination is not guaranteed (W6f). (05) |
| Robustness scope | YES | R1 is Lemma R with explicit hypotheses (a restatement). R2, R4 and R5 are new. Scope sentence: vertex exactness holds for the whole portfolio in Models B/A+ under R-a…R-e; it does not hold at the element level or for Model C. (06) |
| Missingness | YES | DC / DIER / NULL classes plus the FC channel tag; G1–G8, with the G4 and G1 repairs verified. This is a methodological / model-identification contribution, not enterprise theory. (07) |
| Information asymmetry | SIDECAR_DESIGN_ONLY | IA-1 is proven (NDV ≤ LIA − DL). IA-2 and IA-3 are sketches only. v2.2 is not modified. (08) |

## Why the overall verdict is PARTIAL, not PASS

1. **There is no CRITICAL error and no contradiction with v2.2.** The red team (11) checked every main proof, and the repairs (14) were independently verified (15).
2. **Novelty is narrower than the original headlines.**
   - Several results are restatements of v2.2: DL-1, GS-0, GS-I, D1, D3, R1 and Lemma 0.
   - Genuinely new (TYPE C):
     - DL: Cor DL-2/DL-3, DL-6, the impossibility of a pairwise iff (W3c), and the gap between optimistic and pessimistic follower selection.
     - Screening: GS-N with W4c/W4d/W4e.
     - Shared capability: D4/D5, the D6 existence result, and Lemma M.
     - Robustness: R2, R4 and R5.
     - VOI: E.6(e) (51's edge-only grid does not converge on blocks with 3+ vertices), E.7 and E.8.
     - Missingness: G2(iii) and G7. G7 shows that manuscript 59a l.1327 is false in general.
3. **Nothing in 02–07 is AI-specific.** These results hold for any shared-platform IT portfolio. The AI-specific content is limited to the M1–M4 schema, the autonomy-keyed requirement tables and the human-response layer ρ.
4. **Literature positioning is not finished.** The known-analogue literatures are all marked TO VERIFY: optimal delegation / delegated project choice, capital-budget ceilings, menu dependence of minimax regret, complementarity of information, and partial identification. No bibliographic details were invented.

## Researcher decisions (not taken in this pack)

- **R-1, canonical 42 erratum candidate (13).** 42 l.476's proof sentence for the pessimistic case of Lemma E′ ("取任一 x ∈ T") fails under 51's relative ε_tie. The repair is to choose the F_u-maximal tied element. 51's computed numbers are unaffected. 42 was not modified.
- **R-2, manuscript defects found (10).**
  - l.1327: status-quo cells do not cancel in general.
  - l.1277: "upper bounds" needs "for a fixed candidate set".
  - l.2317: the screening "substitute" sentence states a condition that is only necessary.
  - l.1329: the stopping rule needs a declared candidate convention.
  - l.1138 / 2323: the "blockable" wording is imprecise.
  - Ch1 l.113: drop "minimal sufficient".
  - The manuscript was not edited. 10 gives the exact insertion points.
- **R-3: verify the TO VERIFY citations** before any TYPE A/B claim enters the manuscript.
- **R-4:** whether to keep canonical W5 or switch the manuscript to W5_WIDE as the illustrative instance.

## Artifacts

All files are in this folder. Their SHA-256 values are in `FREEZE_MANIFEST_Q1_THEORY_UPGRADE_V1.txt`.

- **Pack documents:** 01–15 (01–12 as required; 13 erratum candidate, 14 red-team response log, 15 repair verification).
- **Witness script:** `q1_theory_witnesses.py`, standalone and stdlib only. It is deterministic: 27/27 PASS, `witness_set_sha256 a68664ce…f8f1`, and the full output was byte-identical across fresh processes.
- **Witness output:** `q1_theory_witnesses_output.txt`.
- **Witness parts:** `witness_parts\`, the per-agent sources of the witnesses.
- **Baseline run:** `baseline\`.
- **Working scripts and sidecars:** `work\`. These include `work\T2\s51_copy.py`, a sidecar copy of 51 used only for the T-MIS-6 per-site reconciliation.

Every number is SIMULATED_ONLY. The witnesses are constructive examples, not proofs of general theorems, and are not enterprise evidence.
