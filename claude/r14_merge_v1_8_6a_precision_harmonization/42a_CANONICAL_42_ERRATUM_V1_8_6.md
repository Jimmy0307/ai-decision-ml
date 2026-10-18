# 42a — Canonical 42 Erratum (V1.8.6 / V1.8.6a lineage record)

**File identity:** this file is `42a_CANONICAL_42_ERRATUM_V1_8_6.md`, also delivered as `04_42A_ERRATUM.md` in the V1.8.6a output folder. It is an **additive erratum record**. It is **not** a replacement for 42 and does not pretend to be 42. The original canonical 42 stays frozen and byte-identical.

```
ERRATUM_TYPE = PROOF_WORDING / CHARACTERIZATION PRECISION
RESEARCHER_DECISION = ACCEPT (R-1, V1.8.6)
EQUATIONS_CHANGED = NO
FEASIBLE_SET_CHANGED = NO
OBJECTIVE_CHANGED = NO
NUMERICAL_OUTPUT_CHANGED = NO
SCIENTIFIC_CONCLUSION_CHANGED = NO
SOLVER_CHANGED = NO
ORIGINAL_42_MUTATED = NO
```

## 1. Original canonical file

| Field | Value |
|---|---|
| Filename | `42_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md` (repository root, `Jimmy0307/ai-decision-ml`) |
| SHA-256 | `0249e7b980f060e979afcaa77d6f7161dd890ae5b2353f95a7607d7f7adb9af9` |
| Location | §12.4, proof of Lemma E′, l.476 |
| Status | Frozen canonical v2.2 mathematical authority; **not modified** |

## 2. Original wording (verbatim, 42 l.476, pessimistic step)

> Pessimistic leader：取任一 `x ∈ T`；`T' ⊆ T`，故 `T'` 上的最小企業貢獻不小於 `T` 上的最小值（pessimistic 值弱增）。

The surrounding proof first defines `S = {x : a(x) ≤ e_u}`, `T ⊆ S` (the unit's optimal set), `e' = a(x)` and `S' = {p : a(p) ≤ a(x)}`. It then states 「`T' = T ∩ S'`（最大值不變）⊆ `T`」.

## 3. Corrected wording (accepted)

> Pessimistic leader：取 `x` 為 `T` 中部門目標最大者（`F_u(x) = max_S F_u`）；此時 `S'` 仍含最大值點，最大值不變，`T' = T ∩ S' ⊆ T`，故 `T'` 上的最小企業貢獻不小於 `T` 上的最小值。（若取 `T` 中非最大者，在 `ε_tie > 0` 下 `T'` 可能納入原本不在 `T` 中的計畫，悲觀值可下降。）Optimistic leader 在容差下取 `T` 中企業貢獻最大者仍成立（該點仍在 `T'`，optimistic 值弱增）。

**Characterization precision.** For the optimistic case, the original 「optimistic 值等於原值」 is accurate under exact ties. Under a tolerant tie rule the precise wording is "weakly higher".

## 4. Why the original wording is too strong

- **42 itself defines a tolerance.** 42 §12.3 (l.458) defines the follower optimal set with a pre-registered tolerance `ε_tie`, with a default of `1e-9` relative.
- **Under exact ties the original is fine.** Every element of `T` is then `F_u`-maximal on `S`, so 「最大值不變」 and `T' ⊆ T` hold for any `x ∈ T`.
- **Under a tolerant rule it fails.** If `x ∈ T` is only within tolerance of the maximum, shrinking the envelope to `a(x)` can lower the maximum on `S'`. Whenever the tie threshold `g` is strictly increasing near `m`, which covers every absolute tolerance and 51's relative rule, the threshold then drops too. `T'` can then admit plans outside `T`, and the pessimistic value can fall. 「取任一 `x ∈ T`」 is therefore too strong.
- **Counterexample.** It reimplements 51's rule `F ≥ m − 1e-9·max(1,|m|)` with one pooled resource:
  - Plans: `x_top` (a = 2, F_u = 1, φ = 10), `x_hat` (a = 1, F_u = 1 − 0.9e-9, φ = 10), `x_low` (a = 0, F_u = 1 − 1.5e-9, φ = −100).
  - At `e = 2`, T = {x_top, x_hat} and pess = 10.
  - Shrinking to `a(x_hat) = 1` gives T′ = {x_hat, x_low} ⊄ T and pess = −100.
  - Shrinking to `a(x_top) = 2`, the F_u-maximal element, keeps pess = 10.
  - Source: theory pack `13_Q1_CANONICAL_42_ERRATUM_CANDIDATE.md` §3, independently re-verified in `15_Q1_T7_REPAIR_VERIFICATION.md`.
- **Scope of the corrected proof.**
  - It holds for every tie rule `T = {x ∈ S : F_u(x) ≥ g(max_S F_u)}` with `g` non-decreasing and `g(m) ≤ m`. This covers exact ties, absolute tolerances and 51's relative rule.
  - It assumes exact affordability `a(x) ≤ e`. 51's `+1e-9` affordability slack (l.667) is **not** covered and remains an open, documented qualification (theory pack 13 §4, 15 §1.2).

## 5. Relationship to solver 51

| Field | Value |
|---|---|
| Solver | `51_enterprise_portfolio_solver_v2_2.py`, SHA-256 `37f26a529ff2f42a3b951155ca41fa1423e8028435214dd2024719f348eff516`, **not modified** |
| Tie rule implemented | `unit_response`, l.672–673: `m = max(fU)`; `tied = [p : fU ≥ m − TOL·max(1,|m|)]` |
| Envelope enumeration | `envelopes_lemmaE` (l.682) enumerates every resource vector `a(x)`, including `a(x̃)` for the F_u-maximal `x̃`, and the leader maximizes over all of them |

51 therefore relies only on the **statement** of Lemma E′, never on the proof's particular choice of `x`. The statement is true under 51's rule (with exact affordability). 51's `envelopes_lemmaE` docstring repeats the same "every x in T" wording. That is documentation only and falls under this same erratum; the code is unchanged.

**Evidence that no output changed:**
- In V1.8.6 preflight, 51 gave `V2_2_SYNTHETIC_ENGINEERING_VERDICT: PASS`, with full stdout byte-identical to the Q1 theory-pack baseline.
- The Q1 witnesses ran 27/27 PASS with unchanged `witness_set_sha256 a68664ce…`.
- All reported 51 numbers (T-ORC-8, T-ORC-9/13, T-SEN-3/7/8, T-MIS-6, REG including P8 10 → 15) are unaffected.

## 6. Where the corrected wording is applied (lineage)

| Artifact | Treatment |
|---|---|
| 42 (canonical) | Unchanged; superseded only in wording by this erratum record |
| Manuscript V1.8.6 §3.12.6 and Appendix C.10.9 | Corrected wording applied (V1.8.6 patch set; `09_V1_8_6_ERRATUM_REPORT.md`) |
| Manuscript V1.8.6a | C.10.9 references this 42a record as the lineage record |
| Manuscript Appendix C.2 | Keeps the v2.2 proof verbatim, with C.10.9 pointing to the corrected sentence |
| Next canonical version of 42 | May incorporate this wording at the next version bump; still a researcher decision (RD-3), and it does not change any equation |

## 7. Lineage chain

```
42 v2.2 (0249e7b9…) ─ frozen
   └─ erratum candidate: theory pack 13 (2026-10-15), verified 15
        └─ accepted R-1 and applied as manuscript wording: V1.8.6 (ff151d8)
             └─ formal erratum record 42a (this file): V1.8.6a
```
