# 09 — V1.8.6 Erratum Report (R-1)

```
R1_42_ERRATUM = ACCEPT (researcher decision)
PROOF_WORDING_ERRATUM = YES
MODEL_EQUATIONS_CHANGED = NO
SOLVER_RESULTS_CHANGED = NO
SCIENTIFIC_RESULT_CHANGED = NO
```

## What the erratum is

**Source.** Theory pack `13_Q1_CANONICAL_42_ERRATUM_CANDIDATE.md`. The candidate was corrected in pack 14 (T8-fix) and verified independently in pack 15.

**The problem.** In the canonical v2.2 proof of Lemma E′ (42, around l.476), the pessimistic-leader sentence reads 「取任一 x ∈ T」 ("take any x in T"). That sentence does not hold under 51's relative equality tolerance, `F_u ≥ m − 1e-9·max(1,|m|)` (51 l.673).

- **Counterexample:** with plans x_top, x_hat, x_low, shrinking the envelope to a(x_hat) drops the pessimistic value from 10 to −100.
- **Scope of the failure:** it occurs when the tie rule g is strictly increasing near m. This covers 51's rule.

**The correction.** Take the F_u-maximal element of the tie set, which matches the solver's selection, and use the per-unit sum argument. With this choice the Lemma E′ statement holds for tie rules of the form {F_u ≥ g(m)} with g non-decreasing and g(m) ≤ m. The repair is valid only under exact affordability; 51's `+1e-9` affordability slack (l.667) is not covered and remains open.

## Where it was applied

| Location | Change |
|---|---|
| Manuscript §3.12.6 | Wording note on Lemma E′'s pessimistic case: tie-element selection and exact-affordability scope |
| Manuscript Appendix C.10.9 (new) | Formal erratum: the original sentence, the counterexample, the corrected wording, its scope and the open slack case |
| Manuscript Appendix C.2 | Unchanged. It reproduces v2.2 verbatim, and C.10.9 points to the sentence it corrects. |
| `42_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md` | **Not edited.** The file is the frozen canonical source, and its hash `0249e7b9…` is referenced by the Study 1 ledgers (18, 40). The erratum is recorded here and in the manuscript. Carrying it into a future canonical revision of 42 is researcher decision RD-3. |
| `51_enterprise_portfolio_solver_v2_2.py` | **Not edited** (`37f26a52…`) |

## Evidence that no result changed

- **Solver output identical.** Solver 51 was rerun at preflight: `V2_2_SYNTHETIC_ENGINEERING_VERDICT: PASS`. Its full stdout is byte-identical to the Q1-pack baseline run (`diff`: no differences).
- **Witnesses identical.** The Q1 witnesses rerun at 27/27 PASS with an unchanged `witness_set_sha256 a68664ce…f8f1`.
- **Only the status date changed.** Theory pack 15 independently checked that the repaired argument produces the same 51 numbers. In the manuscript patch, the only numeric token removed is the status-line date, as verified in 03.
- **Statuses unchanged.** Equations, objective, feasible set, the 13 statuses and the P1–P8 scientific results are all unchanged.
