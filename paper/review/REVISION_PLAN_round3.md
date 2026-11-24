# Revision plan, round 3 (option A: correct errors and fix integrity findings)

**Input:** `review/review_round3.md` (Overall 5, Reject). Updated ground truth: `raw_materials/experimental_log.md`.
- E3.5 now has the corrected DEC06 description and the strict P5e/P5f results (OE 3.16), the Plan 5 decision rule, amendment C1 and Plan 5's known limits.
- The H2 rule is now in E3.1.
- The Level-3 constants are now in E4.

Apply every item to **both** `en/` and `zh/`, keeping them parallel.

## Corrections (must do)

1. **DEC06 is not "without /04".** Replace every "/06 only", "without G06Q10/04", "removing /04" and "5,893 of 37,501" argument with the corrected facts:
   - DEC06 (any /06 code) keeps 2,318 dual-coded patents and drops only the 3,575 /04-only patents;
   - the **strict** check P5e/P5f removes every /04-coded patent (31,608 patents left) and gives OE 3.16 (3.05–3.27), slightly *higher* than 3.05, with percentiles 98.9/91.6 (main groups) and 90.7/83.3 (subgroup families);
   - lead with the strict result.
   - Update `tab:construct` with rows P5e and P5f, and relabel P5a/P5c as "any /06 code".
2. **One-sided granularity:** state that matching is on the reference side only; AI remains the whole G06N subclass.
3. **Not independent checks:** do not count "6 sensitivity and 3 construct checks" as independent. P5b's H1b equals Plan 1's. The construct rule was expected to pass unless OE changed drastically. State this once, briefly.
4. **Preregistration count:** "five preregistered analyses, one confirmatory (Plan 1); Plans 2–5 data-informed". Figure 1 is already regenerated with this wording.
5. **Remove references to the internal review process** ("requested by review", "round-2 review") from the manuscript text. Use "a follow-up specified after the Plan 1 verdict was known (data-informed)". Appendix A may say "added after the main verdict".
6. **Self-pairing:** the rule-based matrix also changes the coding instrument, so 13/16 is not a clean removal test. Say "self-pairing does not appear to be the main driver" (abstract, Section 4, 6.2, 8.1, Appendix).
7. **Study 3 cost vs allocation:**
   - Define cost in one way only, by return: the expected value of a feasible, permitted configuration does not cover its integration cost, even after reallocation.
   - The coding rule must not default to "allocation" whenever aggregate budget exists. "Allocation / decision rights" requires positive evidence that a proposal with a positive expected return (by the firm's own business case) was blocked by where the leader allocated budget, or by a decision right. Otherwise code it as cost or as unclear.
   - Fix Section 6.3, Table 8 and Appendix C.7.
8. **Level-3 constants:** print the configuration and process constants from E4 in Appendix C, so Table 7 is reproducible from the text.
9. **Core-rule wording:** make the raw-direction wording identical everywhere: "plus raw q ≤ .05 in the same direction", matching Table A1 and the frozen Plan 2.
10. **H2 and Plan 5 rules:** quote them consistently with the log (E3.1, E3.5).
11. **Contributions:** describe M06-P and the portfolio-preserving null as *proposed* nulls without separate type-I calibration (one clause).
12. **Label collision:** in the manuscript, rename the Plan 5 specifications P5a–P5f to **C-a, C-b, C-c, C-d, C-e, C-f**, so "P5" refers only to the Plan 3 firm-network module. The data file keeps its internal names; mention the mapping once in the table caption.
13. **Shorten Section 7** by at least 400 prose words. Move detail to Appendix C, keeping 7.1 (short), the Table 7 scenarios, Figure 7 and the rivals table. The English main text must end ≤ 11,200 prose words, giving headroom.

## Rules

- No numbers outside the log.
- Citations only from `citation_map.json`.
- Keep all limitations.
- `python scripts/audit_manuscript.py` and `--zh` must both PASS.
- Report word counts from `python scripts/wordcount.py`.
