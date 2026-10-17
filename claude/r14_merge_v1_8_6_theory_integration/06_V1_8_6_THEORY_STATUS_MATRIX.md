# 06 — V1.8.6 Theory Status Matrix

**Columns:**
- "Pack status": the final label from theory pack 12, after the red team (11), the repairs (14) and the independent verification (15).
- "Integrated as": how the result appears in `01_V1_8_6_THEORY_INTEGRATED_MANUSCRIPT.md`.
- "Location": where in `01` it is integrated.

**Type labels:**
- `TYPE C`: an in-model result of this thesis.
- `RESTATEMENT`: a specialisation of an existing v2.2 result.
- `WITNESS`: a SIMULATED_ONLY constructive example.

| Area | Result | Pack status | Integrated as | Location in 01 |
|---|---|---|---|---|
| M1–M4 | Non-redundant under T1–T4 within the v2.2 static model | PARTIAL (minimal sufficiency NOT_PROVEN) | Operationally distinguishable, non-redundant mechanism decomposition. Completeness, universal sufficiency and uniqueness NOT established. Not exhaustive. | Ch1, §3.9.6, §5.7, §5.8.10 |
| M1–M4 | "Minimal sufficient" claim | Removed | Removed (Ch1 l.113) | Ch1 |
| DL | Zero-loss characterization (Lemma DL-1, first-best-relative) | RESTATEMENT of Lemma E′ | Characterization lemma, not a theorem | §3.12.4, C.10 |
| DL | Necessary conditions for DL > 0 (DL-2o/2p under AL3, plus the AL3 channel) | ESTABLISHED | Necessary conditions, TYPE C | §3.12.4, C.10 |
| DL | Sufficient conditions (Cor DL-3 under a unique first best; DL-4 for DL = 0, AL3 and exact ties) | ESTABLISHED | Sufficient conditions, TYPE C | §3.12.4, C.10 |
| DL | Primitive iff | NOT_PROVEN (impossible as a pairwise Boolean condition; W3c) | Counterexample showing the simple pairwise iff fails; no iff claim | §3.12.4, §5.8.10 |
| DL | Tie-tolerance robustness | QUALIFIED (exact affordability only) | Stated with scope; 51's slack open | §3.12.6, C.10.9, §5.8.10 |
| DL | Optimistic vs pessimistic (W3b: DL_opt = 0 < DL_pess) | TYPE C | Reported separately | §3.12.4 |
| Screening | Model B: pruning cannot raise the priced optimum (GS-0) | RESTATEMENT of P7 plus cost channel | Restatement | §3.12.4 |
| Screening | Identity GSV = DL_loose − DL_strict − PR_B (GS-I) | Accounting identity | Identity; GSV ≤ DL_loose as a corollary | §3.12.4, §5.6 |
| Screening | Sufficient condition (GS-1) | PASS | Sufficient condition, TYPE C | §3.12.4 |
| Screening | Necessary condition (GS-N) | PASS, exact ties only | Necessary condition in its exact-tie form | §3.12.4, §5.6 (l.2317 fix) |
| Screening | Witnesses W4 10→15, W4b 15→10, W4c, W4d | WITNESS PASS | "May have positive screening value under specific bilevel misalignment and separability conditions"; never "always" | §3.12.4, §4.9.1 |
| Shared capability | Prop D6: the build region need not be an interval | PASS (existence) | Existence result only; never "generally non-monotone" | §3.12.4, §4.9.1 |
| Shared capability | D1 (Model B monotone), D3 (alignment) | RESTATEMENT | Restatement | C.10 |
| Shared capability | W5 1→0→1 (primary, 162/400); W5_WIDE (367/400) | WITNESS PASS | Primary vs sensitivity kept separate (see 10) | §4.9.1, C.10.4 |
| VOI | Vertex overstatement, VOI_vertex = 1 vs VOI_true = 0.5 | PASS | SYNTHETIC ANALYTIC COUNTEREXAMPLE | §3.13, §4.9.1 |
| VOI | Sequential identification properties | PARTIAL (fixed candidate set; adaptive refuted; greedy optimality open) | PARTIAL; VOI is not this thesis's invention; not enterprise measurement efficiency | §3.13 (l.1277, l.1329 fixes) |
| Robustness | Vertex-exactness scope | YES (R1 restates Lemma R; R2/R4/R5 new) | Only Model B whole-portfolio under multilinearity and a product uncertainty set; not element-level; not Model C; T-SEN-3 as a scope counterexample | §3.13 |
| Missingness | Three classes, linked to the status machine | YES (methodological) | Feasibility-changing / objective-ranking-changing / decision-invariant but epistemically relevant; Missing ≠ 0; partial-identification methodology, not AI organization theory | §3.13 (l.1327 fix) |
| Information asymmetry | NDV, LIA design | SIDECAR_DESIGN_ONLY | Not in the main results; limitations / future work only | §5.8.10 |
| AI-specificity | General formal contribution vs AI-specific instantiation | Red-team finding | Split stated explicitly | Ch1, §5.7 |
| Erratum | 42 Lemma E′ pessimistic proof wording | ACCEPT (R-1) | Wording erratum only | §3.12.6, C.10.9 (see 09) |
| References | TO VERIFY items | R-3 | 0 new citations in the main text | (see 07/08) |
