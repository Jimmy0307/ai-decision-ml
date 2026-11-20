# Revision plan, round 2

**Input:** `review/review_round2.md` (Overall 5, Reject with encouragement).

Updated ground truth in `raw_materials/experimental_log.md`:
- T1 ratio form 0.67 / 0.78 (shortfall 33% / 22%);
- F2 and the Level-2/3 component formulas;
- capabilities in the permission probe are endogenous.

Two new verified references (`citation_map.json`):
- `swanson1986fish` (literature-based discovery);
- `callon1983translations` (co-word analysis).

`fig_research_design.png` is regenerated with the new logic: Study 2 → "which constraint binds?" → Study 3 discriminates; the MLP is calibrated only if the organisational account is supported; the firm level is "unresolved (PARTIAL)". `fig_patent_trend.png` now labels the median line as the DEC-side median (1.095), with AI side 1.240.

## Decisions

1. **RQ2 / firm level becomes UNRESOLVED.** It must not read "not supported". Everywhere (abstract, intro, 5.4, 6.1, 8, 9), state:
   - specialist separation beyond portfolio is significant (p = .001 in both stratifications);
   - its size depends on the scale: on the gap-from-1 scale the null reproduces 85% / 91%; on the ratio scale specialist ties are 0.67 / 0.78 of the null expectation (a 33% / 22% shortfall);
   - the degree-matched P5 null favoured lower constraint for mixed firms (p = .001), but the portfolio null does not hold degree fixed (T2);
   - no available null holds degree and portfolio fixed together, so whether mixed firms broker is **unresolved**;
   - the preregistered verdict PARTIAL means the firm-level hole is not confirmed. Say so, and do not claim it is ruled out.
2. **Positioning / straw man.**
   - Ground "inferring gaps or separations from non-co-occurrence" in co-word analysis (`callon1983translations`) and literature-based discovery (`swanson1986fish`), at the level of their role notes. Remove any unsourced "gap research often…" claim, or attach these citations to it.
   - Say that this project applied the same inference to AI × decision, and that this paper tests whether flow data support it.
   - Concede that the SNA lessons (projection cliques, bipartite constraint) are known in the literature cited (Opsahl, Jasny & Lubell, Everett & Borgatti). The contribution is their consequence for gap inference, demonstrated end to end, not their discovery.
3. **Construct validity remains untested** (state plainly in 5.1 and Limitations):
   - s2 still contains /04, so it cannot isolate the overlap;
   - a /06-only analysis and a granularity-matched H1a reference set were not run;
   - list both as the first robustness checks for future work;
   - the domain-level verdict should be read as applying to G06N vs G06Q10/04+/06 as defined.
4. **"Ruling out" → "not supporting"** a knowledge-flow hole (abstract, back L33, everywhere). Keep "not a proof that none exists".
5. **Study 1 self-pairing.** Connect it to the paper's own evidence:
   - after removing the same-term records, 13/16 depleted cells keep their direction, and removal drops 2 depleted cells from the core;
   - so self-pairing is not the main driver;
   - model-inferred labels remain an untested non-random source;
   - do not name the inflated cell beyond the log's "prediction × prediction".
6. **Cell O/E range:** "O/E 0.70–0.95" applies to the five cells depleted in both parts. Say so; the Part B core also includes cells outside that range.
   - Only use G06N_OTHER × PERFORMANCE = 0.51 if it is in the log. It is NOT, so describe it qualitatively ("one further Part-B core cell lies below this range") or omit it.
7. **H2 label:** state the preregistered rule. PERSISTENT = the slope CI includes 0 or lies below 0. It was written for the hole case, so with an over-connection the label only means "not closing toward the reference"; the over-connection is declining.
8. **Core rule wording** (front L147): same direction in main, exact and document-preserving (or M06-P), plus raw q ≤ .05 in the same direction for the full core.
9. **studies L163:** "the AI–decision pairs" → "the 16 depleted pairs".
10. **Heatmap note:** small-sample (E < 10) cells are shown but are not interpreted; say whether they are inside the counts (they are, and they are marked).
11. **back L95:** remove "capabilities unchanged". In the permission probe, Level 1 re-optimises.
12. **F2:** print the F2 formula and its components in Appendix C from the log (uncalibrated design weights), so the prototype is reproducible from the text and the canonical file.
13. **Study 3 table:** make the cost signature and the allocation/decision-rights signature discriminant.
    - Cost binds when feasible configurations are rejected because their integration cost exceeds budget even after reallocation.
    - Allocation binds when budget exists in aggregate but is allocated elsewhere by the leader, or decision rights block adoption.
    - Keep the signatures observational.
14. **Real ties:** cite `burt2004structural` (its role note), not burt1992.
15. **Anonymity:**
    - remove "identified in the thesis";
    - replace "PR #5" and any repository or commit naming in the main text with "the project repository (identifiers withheld for review; listed in Appendix A)";
    - Appendix A may keep commit ids.
16. **Equation references:** use `\eqref` consistently.
17. **MLP proportion:** shorten Section 7 slightly if possible (it is the consequence, not the core). Keep 7.1 summary, 7.2 table and figure, and 7.3 rivals table.

## Rules

- No numbers outside the log.
- Keep all existing caveats.
- The main text must stay ≤ 11,500 prose words (`python scripts/wordcount.py`).
- Finish with `python scripts/audit_manuscript.py` → AUDIT PASS.
