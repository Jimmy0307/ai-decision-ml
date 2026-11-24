THOUGHT:
<THOUGHT>
This is round 2. I read draft v3 in full: en/main.tex, abstract, front, studies, back and appendix, plus all seven figures. I also read the round-1 review, REVISION_PLAN_round1.md, the updated experimental_log.md, idea.md section 10, citation_map.json and references.bib. I spot-checked the raw result files in data/: V9_MATRIX_RESULTS.json and SUITE_P1_A/B_CELLS.csv.

Overall the revision is substantial and made in good faith.

What the revision fixed:
- The premise is now explicitly the project's own working premise, drawn from co-occurrence evidence, and it is no longer attributed to the IS literature.
- The preregistration chronology is honest and consistent across all four files:
  - only Plan 1 is confirmatory;
  - Plans 2-4 fixed rules, not questions;
  - the plans are self-timestamped commits, not OSF registrations;
  - M06-P was designed after M06 failed;
  - the firm null was motivated by P5.
- I verified the M06-P provenance claim. V9_MATRIX_RESULTS.json (Plan 2) contains only the degenerate M06 output: doc_q05 = 0, full_core = 0, 0 of 21,843,600 swaps accepted. The M06-P counts come from the SUITE_P1 files, and recounting them reproduces 8/7 (Part A) and 9/8 (Part B), and q <= .05 counts of 20/20/29/22 and 22/22/27/25.
- T1 is now reported as a significant residual. The degree confound of T2 is conceded everywhere.
- The Study 1 direction is downgraded to 'descriptive, unconfirmed', and a new claim boundary (viii) records this.
- The identity character of Gap Validity is stated.
- The persistence contrast between the two studies is withdrawn.
- The P5 / firm-null scope is reconciled, and the tau/permission-probe regimes are now logged.
- All six round-1 citation misuses are corrected.
- LaTeX: all floats are [tbp], and Table 1 now fits (0.91\linewidth + 32pt).

Numbers (check 1). The repo's audit script passes. I re-derived the following and found no arithmetic errors:
- 85/91% and 15/9%;
- 3.05/1.809 = 1.69;
- the 9/16 row/column count;
- the C < F < D ordering;
- the heat-map markers.

The remaining number-level problems are matters of scope or label, not arithmetic:
- studies L304 claims that 'the depleted O/E values lie between 0.70 and 0.95', but the Part B adapted core contains G06N_OTHER x PERFORMANCE at O/E 0.51 (O 17, E 33.0).
- The trend figure labels the DEC-side median (1.095) as 'the median of 179 comparable fields'.
- The H2 label PERSISTENT is attached to a significantly negative slope, and the H2 rule is never stated.

What the revision broke or left inconsistent:
(1) Figure 1 was regenerated, but it still encodes the round-1 logic. The Study 3 box says 'Calibrates the model'. The MLP box says 'parameters to be calibrated by Study 3'. The 'hole not supported' arrow leads straight into the MLP. This contradicts the new text: Study 3 first discriminates among five candidates and calibrates only if the organisational one survives.
(2) The firm-level conclusion has swung from understated to a different imbalance.
- 'Small' is scale-dependent. As a share of the distance to O = E, the residual is 15%/9%. As a ratio to the portfolio expectation, specialist ties are 33%/22% below it (0.240/0.356 and 0.240/0.307). That is larger than the patent cell depletions the paper calls 'modest' (0.70-0.95).
- The RQ2 conclusion ('does not support a firm-level structural hole') rests on T2, which the authors now concede cannot separate brokerage from degree. Meanwhile the only degree-controlled comparison (P5, p = .001) pointed the other way. RQ2 is really unresolved on brokerage.
(3) The abstract and back L33 say 'ruling out a knowledge-flow hole'. This is stronger than the paper's own 'not a proof that none exists'.
(4) The non-random-error argument for Study 1 is stated in the abstract (concentration of 9/16 cells in the inflated row/column). It is not connected to evidence the paper already holds: after removing 741 same-term records, 13/16 depleted cells keep their direction, and removing self-pairs drops only 2 depleted cells from the core.

What remains substantively open:
(a) Construct validity. The paper now concedes that Study 2 measures the technological proximity of patent classes. It still does not run the two cheap analyses that would tell readers how much of OE 3.05 is the forecasting/optimisation overlap: DEC = G06Q10/06 only, and a granularity-matched reference set. Sensitivity check s2 does not answer this, because it still contains /04.
(b) Edge-level tests and the 'core' remain uncalibrated under document clustering. M06-P remains uncalibrated. These are acknowledged, not fixed. M06-P is still offered as a contribution.
(c) Positioning. The new framing rests on 'gap research often reads sparse co-occurrence as structural separation' (abstract; back L186), and this sentence has no citation. The obvious anchors are co-word analysis and Swanson-style literature-based discovery, which literally infer gaps from non-co-occurrence. They are absent. Without them, the methodological lesson reads as known SNA results (Opsahl; Everett and Borgatti) applied to one project's own data.
(d) The MLP section is reframed well. It now includes a rival-explanation table, a unit of analysis, coding rules and stop rules. But:
   - it still occupies a full main-text section of a paper whose evidence does not bear on it;
   - the F2 weights are withheld, although the F1 weights are given;
   - the Study 3 thresholds are all deferred;
   - the 'cost' and 'organisational allocation' signatures overlap.

LaTeX (check 5). I found no undefined references, no duplicate labels, no unresolved citations and no unbalanced environments. All underscores outside math are escaped. Prose length is 10,957 words. pdflatex is not installed here, so I did not compile. The main.tex path dependence (inputs and ../figures resolve only when compiling from en/) is unchanged.

Citations (check 6). The new IS citations match their role notes: Shrestha, Raisch and Krakowski, Jarrahi, Berente. One small stretch remains: front L43 credits burt1992 with 'real ties', which is the role note of burt2004.

Assessment. This is a much more honest and internally consistent paper. Its claims now largely sit inside idea.md section 10, and in places more conservatively than idea.md. The remaining problems are:
- untested construct validity at the centre of the headline result;
- a firm-level conclusion that the conceded T2 confound cannot carry;
- uncalibrated inference for the cell analyses;
- thin positioning of the methodological contribution for an IS audience;
- an MLP agenda that is now correctly labelled but still out of proportion.

I raise the score by one point. A further round that runs the /06-only and granularity-matched analyses, plus a degree-and-portfolio-preserving null, and condenses Section 7, could make this publishable as a measurement/negative-result paper.
</THOUGHT>

REVIEW JSON:
```json
{
  "Summary": "The paper (draft v3, retitled 'Co-occurrence Is Not Flow') tests an inference the project itself had drawn: that sparse co-occurrence between AI functions and decision functions in a literature matrix indicates a Burt structural hole between AI and managerial decision-making. Study 1 re-examines the literature programme. Its 16 depleted cells in a 10x12 LLM-coded matrix keep their direction under seeds, tracks, periods and largely under keyword coding, but they lose significance under realistic misclassification. The direction is now explicitly treated as descriptive and possibly an artefact of non-random coding. HISTORICAL network lines found no broker. A screen of six public sources found none that is flow-valid. Study 2 applies four git-committed plans to US patents; only Plan 1 is treated as confirmatory. AI (G06N) and DEC (G06Q10/04 + /06) cite each other at OE 3.05 (95% CI 2.94-3.17), above 97.8%/92.2% of 179 reference main groups, so both relative hole criteria fail in all six sensitivity checks. Cell-level depletions in a 6x7 CPC matrix are modest and do not replicate across time halves; a patent-adapted null (M06-P) replaces the degenerate swap null. At the firm level, specialist AI and DEC firms are under-connected (O/E 0.24). A portfolio-preserving owner-permutation null reproduces 85-91% of this shortfall, leaving a significant residual (p = .001). Mixed firms are more constrained than under that null, but the null does not hold degree fixed, so a brokerage advantage cannot be established (verdict PARTIAL). The paper then lists five candidate explanations for weak AI-decision integration and formalises only the organisational one in a simulated tri-level programming model. It also sets out a planned enterprise study (Study 3) designed to discriminate among the candidates.",
  "Strengths": [
    "The revision is thorough and consistent across files. The premise is owned as the project's own inference. The preregistration chronology is stated identically in front (Section 3.3), studies, back (Section 8.3) and Appendix A, including the self-timestamped status of the plans and the data-informed character of Plans 2-4.",
    "The claim discipline is now stricter than the design notes require. Boundary (viii) on the Study 1 direction, the explicit 'one candidate among five' framing and the conditional calibration aims of Study 3 show this. The firm-level text now reports the significant T1 residual instead of hiding it.",
    "The M06-P provenance is now correct and verifiable. The Plan 2 result file (V9_MATRIX_RESULTS.json) records only the degenerate core (0 of 21,843,600 swaps accepted), and all M06-P counts come from the Plan 3 P1 output, as Amendment B1 states.",
    "Limitations Section 8.2 now lists the four calibration gaps explicitly: clustering, M06-P, the core's undefined FDR, and the simple synthetic generator. A reader can see exactly what the tests do and do not certify.",
    "The Study 3 plan now has a rival-explanation table with predicted signatures, a unit of analysis (the decision process / integration episode), a two-human-coder protocol that does not rely on model coding, and decision and stop rules. This is a real improvement in falsifiability.",
    "The P5 / firm-null scope, the quantum-row size, the tau/permission-probe regimes and the period-specific margins in Figure 2 are all reconciled with the log."
  ],
  "Weaknesses": [
    "The construct validity of Study 2 is conceded but not tested (studies L186, L204; back L156). The paper now says, correctly, that the test measures the technological proximity of patent classes and that G06Q10/04 overlaps methodologically with machine learning. It then declines the two analyses that would size the problem: OE with DEC = G06Q10/06 only, and a granularity-matched (subgroup-level) reference set for H1a. Sensitivity check s2 (all G06Q10, OE 2.59) is offered as partial reassurance, but s2 still contains /04, so it dilutes the overlap rather than removing it. The interpretation of the headline number therefore remains open: how much of OE 3.05 is definitional?",
    "The firm-level conclusion is stronger than T2 can bear, and 'small' is scale-dependent (studies L375-386; back L19, L168, L188; abstract). (a) T2 is now conceded to be unable to separate brokerage from degree. The only degree-controlled comparison, the P5 label null, found MIXED constraint lower than expected (p = .001). The defensible RQ2 answer is therefore 'separation beyond portfolio: yes, modest; brokerage net of both degree and portfolio: untested'. 'The evidence does not support a firm-level structural hole' implies a test that was not run. (b) The residual is 15%/9% of the distance to O = E. As a ratio, observed specialist ties are 0.240/0.356 = 0.67 and 0.240/0.307 = 0.78 of the portfolio expectation, a 33%/22% shortfall. That exceeds the patent cell depletions (O/E 0.70-0.95) that the paper calls 'modest'. Report both metrics, and either run a null that preserves both degree and portfolio (for example, a degree-constrained owner permutation, or degree-residualised constraint) or call RQ2 unresolved on brokerage.",
    "Inference for the cell-level analyses remains uncalibrated (studies L30, L263, L265, L334; back L161-166). The clustering, M06-P and core-FDR problems are now disclosed, which is welcome, but none is fixed. M06-P is still listed as a contribution (front L20) although it has no type-I calibration. A document-level permutation calibration of the exact/raw tests and of M06-P is a modest computation on the existing files. Without it, Table 5, the 16/16 Study 1 core and the P3 non-replication cannot be given an error rate.",
    "Positioning and significance for a management/IS readership (abstract; front L8; back L186). The reframing rests on a claim about field practice: 'gap research often reads sparse co-occurrence ... as structural separation'. This claim has no citation, and the closed library contains none for it. The natural anchors are co-word / science-mapping gap analysis and Swanson-style literature-based discovery, both of which infer gaps from non-co-occurrence, and they are missing. Without them, the general lesson ('co-occurrence is not flow'; projections create closure; constraint degenerates on bipartite graphs) restates known SNA results (Opsahl 2013; Everett & Borgatti 2020) and illustrates them on a single project's own pipeline. The empirical contribution is a negative result about class-level patent citation proximity that the authors themselves say is not a measure of organisational integration.",
    "The MLP agenda is reframed but still out of proportion, and partly unreproducible (back Section 7; appendix C; Figure 1). (a) A full main-text section and a long appendix formalise one of five candidates on which the evidence is silent. A two-page outlook would suffice. (b) The F2 weights are withheld 'because they carry no empirical content' (appendix L329), yet the equally uncalibrated F1 and U weights are printed. Table 7 cannot be reproduced from the paper, and the canonical file sits in an unnamed repository. (c) Every Study 3 threshold (minimum share, minimum informative sample, pilot agreement) is deferred. (d) The 'organisational allocation' and 'cost' signatures overlap (Table 8): both stop at budget or business-case review and map to budget parameters, and no observable separates them. (e) The regenerated Figure 1 still shows the round-1 logic: the negative result arrow points into the MLP, and Study 3 'calibrates the model'.",
    "Study 1's non-random-error argument is not connected to the evidence the paper already has (studies L53-54, L95; back L24; appendix L86, L128-129). The paper uses the concentration of 9/16 depleted cells in the PREDICTION_RISK_ESTIMATION row / PREDICTION_DIAGNOSIS column to argue that self-pairing can create depletion. It does not report the obvious test: do those 9 cells keep their direction after the 741 same-term records are removed? The aggregate results (13/16 same direction; only 2 depleted cells leave the core after removing self-pairs) suggest that the mechanism does not explain most of the pattern. Also, the identification of the inflated cell is inferred: the log names it only 'prediction x prediction'.",
    "Wording now overshoots in places, in both directions. 'Ruling out a knowledge-flow hole' (abstract; back L33) is stronger than the paper's own 'not a proof that no separation exists' (studies L247; caption Fig. 1). 'The AI-decision pairs co-occur less often than their margins imply' (studies L163) should name the 16 depleted pairs, since the closed matrix has 16 enriched pairs too. Elsewhere the caveats are so dense that the main message is hard to extract. The abstract, for example, spends four of nine sentences on qualifications.",
    "Presentation. Project-internal labels remain heavy in the main text: V5-V11.1, V9.1, P1-P10, M06/M06-P, S-tech, Gap Validity, Limitation Scout, sidecar. The suite Table 6 maps patent modules to project versions that readers cannot inspect. The main text is about 11,000 words with 8 tables and 7 figures; Section 5.3 (P2-P10) and the V6-V11.1 table could move to the appendix with little loss."
  ],
  "Originality": 2,
  "Quality": 3,
  "Clarity": 3,
  "Significance": 2,
  "Questions": [
    "What is OE(AI, G06Q10/06) with /04 excluded, and where does it rank among a reference set of CPC subgroups of comparable size? If it drops to the reference median, how would the RQ1 conclusion change?",
    "For RQ2, can you run an owner permutation that also preserves firm degree (or compare degree-residualised constraint)? Absent that, would you accept 'brokerage net of degree and portfolio is untested' as the RQ2 answer, given that the degree-controlled P5 comparison favoured lower MIXED constraint?",
    "Why is the T1 residual expressed as a share of (1 - T1) rather than as T1_obs / T1_null? Under the latter, specialist ties are 33% / 22% below the portfolio expectation. Why is that 'small'?",
    "What is the H2 decision rule that distinguishes CLOSING, PERSISTENT and NARROWING_BUT_OPEN? Why does a slope with 95% CI -0.130 to -0.065 receive PERSISTENT?",
    "How many of the 9 depleted cells in the PREDICTION_RISK_ESTIMATION row / PREDICTION_DIAGNOSIS column keep their direction in the rule-based keyword matrix that removes the 741 same-term records?",
    "What is the type-I error rate of the exact, raw and M06-P tests under a document-level permutation null, in Study 1 and in Part B?",
    "Which published gap-detection practice (co-word analysis, literature-based discovery, bibliometric 'research gap' studies in IS) makes the inference you refute? Can you cite two or three representative examples?",
    "In Study 3, what observable separates 'organisational allocation' (stop at budget allocation) from 'cost' (rejected in business-case review)? Both map to budget parameters in Table 8.",
    "Will the F2 weights and the canonical model file be released, for example as supplementary material, so that Table 7 can be reproduced?",
    "Which exact model versions were used for the qwen pipeline and the two Claude coders in Table 2?"
  ],
  "Limitations": [
    "Study 2 measures class-level technological proximity; the share of the over-connection that is definitional (/04 overlap; granularity) is not quantified.",
    "Neither firm null holds both degree and portfolio fixed, so firm-level brokerage is untested rather than refuted.",
    "Cell-level tests (Study 1 core; Part A/B cores; M06-P) lack calibration under document clustering, and the core has no defined FDR.",
    "The Study 1 direction may reflect non-random coding error; human reliability rests on n = 20.",
    "Plans 2-4 are data-informed and self-timestamped. Only Plan 1 is confirmatory.",
    "The MLP is simulated and uncalibrated, the F2 weights are not reported, and the Study 3 thresholds are deferred.",
    "The study covers US patents only, and the alias check covers 54 firms."
  ],
  "Ethical Concerns": false,
  "Soundness": 3,
  "Presentation": 3,
  "Contribution": 2,
  "Overall": 5,
  "Confidence": 4,
  "Decision": "Reject",
  "Integrity_Findings": [
    {
      "file": "figures/fig_research_design.png (Figure 1)",
      "location": "Study 3 box; MLP box; centre arrow; Study 1 box; Study 2 box line 1",
      "issue": "Check 2/4: the regenerated figure contradicts the revised framing.",
      "evidence": "Study 3 box: 'resources, decision rights, human-AI configuration ... Calibrates the model'. MLP box: 'parameters to be calibrated by Study 3'. The 'structural hole in knowledge flows not supported' arrow leads directly into the MLP box. The text (back L41, L100, L192; boundary v) says that Study 3 first discriminates five candidates and calibrates only if the organisational one survives, and that the MLP is 'a consequence, not a conclusion'. The Study 1 box says 'Direction robust', which conflicts with boundary (viii). The Study 2 line '8.5M US patents, 4 preregistered analyses' overruns the left border of its box.",
      "suggested_fix": "Study 3 box: 'Discriminates 5 candidate explanations; calibrates model only if the organisational one is supported'. MLP box: 'formalises the organisational candidate only; simulated'. Make the arrow dashed and label it 'removes one justification'. Study 1 box: 'Direction stable but unconfirmed'. Shrink the Study 2 text."
    },
    {
      "file": "en/studies.tex",
      "location": "L304",
      "issue": "Check 1: the range is stated without its scope.",
      "evidence": "Text: 'Apart from the small-sample quantum cell, the depleted O/E values lie between 0.70 and 0.95'. This holds for the five cells depleted in both parts (log L267-271). However, the Part B adapted full core also contains G06N_OTHER x PERFORMANCE with O/E 0.51 (O 17, E 33.0; data/SUITE_P1_B_CELLS.csv, shown as '0.51 ▼' in Figure 5).",
      "suggested_fix": "Write 'Apart from the quantum cell, the five cells depleted in both parts have O/E between 0.70 and 0.95'."
    },
    {
      "file": "en/studies.tex; figures/fig_patent_trend.png",
      "location": "L238, L243 (Figure 4 caption and in-figure label)",
      "issue": "Check 1: the reference median is ambiguous.",
      "evidence": "Text and figure: 'median of the 179 comparable fields (1.095)'. The log (L196) gives two medians: 1.240 on the AI side and 1.095 on the DEC side. The lower one is used without a label.",
      "suggested_fix": "Label it 'DEC-side reference median (1.095)'. Optionally also draw the AI-side median (1.240)."
    },
    {
      "file": "en/studies.tex; en/appendix.tex",
      "location": "studies L238; appendix L27 (Table A1, Plan 1 rule)",
      "issue": "Check 3/4: the H2 label is not verifiable from the paper.",
      "evidence": "Only the label names CLOSING / PERSISTENT / NARROWING_BUT_OPEN are given. The WLS slope is significantly negative (-0.097; CI -0.130 to -0.065), yet the label is PERSISTENT. The reader cannot check the rule.",
      "suggested_fix": "Quote the H2 decision rule from the frozen Plan 1 text in Table A1, and add a sentence on why a declining over-connection maps to PERSISTENT."
    },
    {
      "file": "en/studies.tex; en/back.tex; en/abstract.tex; en/front.tex",
      "location": "studies L375, L386; back L19, L168, L188; abstract; front L16",
      "issue": "Check 2/3: the RQ2 conclusion exceeds what T2 can show, and 'small' depends on the metric.",
      "evidence": "T2 is conceded to be unable to separate brokerage from degree (studies L353, L377). The degree-controlled P5 comparison gave MIXED 0.36 vs null 0.444, p = .001. Yet studies L386 says 'the evidence does not support a firm-level structural hole'. The residual is 15%/9% of (1 - T1). As a ratio, T1_obs/T1_null = 0.240/0.356 = 0.67 and 0.240/0.307 = 0.78, from logged values.",
      "suggested_fix": "Write 'RQ2: a significant separation beyond portfolio remains; whether mixed-portfolio firms broker it is untested, because neither null holds degree and portfolio fixed'. Report both residual metrics, adding the ratios to the log, or drop 'small'."
    },
    {
      "file": "en/abstract.tex; en/back.tex",
      "location": "abstract (penultimate sentence); back L33",
      "issue": "Check 2/4: the claim strength is inconsistent.",
      "evidence": "'Ruling out a knowledge-flow hole ...'. Elsewhere: 'not a proof that no separation exists' (studies L247); 'does not show that none exists' (front L80); 'Failing to support a hole is not proof that none exists' (back L161).",
      "suggested_fix": "Write 'Failing to find a knowledge-flow hole does not establish ...' in both places."
    },
    {
      "file": "en/front.tex",
      "location": "L147",
      "issue": "Check 4: the core definition is misstated.",
      "evidence": "Text: 'cells significant with the same direction in all four tests'. studies L28, Table A1 and log L28 require the same direction in main + exact + document-preserving tests, plus raw q <= .05; the direction of the raw test is not required.",
      "suggested_fix": "Write 'significant in all four tests, with the same direction in the main, exact and document-preserving tests'."
    },
    {
      "file": "en/studies.tex; en/back.tex; en/appendix.tex",
      "location": "studies L95; back L24; appendix L86 vs studies L53-54, appendix L128-129",
      "issue": "Check 3: the self-pairing mechanism is asserted without using the paper's own removal evidence.",
      "evidence": "The 9/16 concentration in the inflated row/column is presented as a threat. Removing self-pairs drops only 2 depleted cells from the core, and the rule-based matrix without 741 same-term records keeps 13/16 directions. The log (L71) names the inflated cell only as 'prediction x prediction'; mapping it to PREDICTION_RISK_ESTIMATION x PREDICTION_DIAGNOSIS is an inference.",
      "suggested_fix": "State the inferred cell identity explicitly. Report how many of the 9 row/column cells keep their direction after removal. Add one sentence stating what the removal evidence implies for the mechanism."
    },
    {
      "file": "en/studies.tex",
      "location": "L163",
      "issue": "Check 4: the descriptive claim is ambiguous.",
      "evidence": "'the AI-decision pairs co-occur less often than their margins imply'. In the closed matrix, 16 pairs are depleted and 16 are enriched (back L19).",
      "suggested_fix": "Write 'the 16 depleted AI-decision pairs co-occur less often ...'."
    },
    {
      "file": "en/studies.tex; en/back.tex",
      "location": "studies L186; back L156",
      "issue": "Check 3: s2 is presented as bearing on the /04 overlap, but it cannot isolate it.",
      "evidence": "s2 broadens DEC to all of G06Q10, which still includes G06Q10/04. A fall from 3.05 to 2.59 reflects dilution by other G06Q10 subgroups, not removal of the forecasting/optimisation overlap.",
      "suggested_fix": "Say that s2 does not isolate the /04 overlap. Ideally add a preregistration-labelled exploratory run with DEC = G06Q10/06 only."
    },
    {
      "file": "figures/fig_cpc_heatmap.png; en/studies.tex; en/front.tex",
      "location": "Figure 5 footnote; Table 5; boundary (ii) front L157",
      "issue": "Check 4: small-expected cells are both 'uninterpretable' and counted.",
      "evidence": "The figure footnote says that hatched cells (E < 10) have 'too few observations to interpret'. G06N10 x PERFORMANCE in Part B (E 8.9, hatched) is nevertheless counted among the 5 cells depleted in both parts and in the 9 depleted core cells. G06N_OTHER x MGMT_GENERAL in Part A (hatched) carries an enriched core marker and is counted among the 7.",
      "suggested_fix": "Either exclude E < 10 cells from the counts or soften the footnote to 'small-sample; interpret with caution', as in the Table 5 caption."
    },
    {
      "file": "en/back.tex",
      "location": "L95 (permission probe)",
      "issue": "Check 1/2: a model state is asserted that is not in the log.",
      "evidence": "Text: 'Capabilities and budget are unchanged, so the solution is bound by permission'. The Level-1 allocation, and hence the capability ceilings, is endogenous. Log E4 L399-401, L407 records only F1, the configurations and the disallowed configuration.",
      "suggested_fix": "Write 'initial capabilities and the budget are unchanged', or log the allocations of both solutions."
    },
    {
      "file": "en/appendix.tex; en/back.tex",
      "location": "appendix L263, L329; back L49, L178",
      "issue": "Check 4: reproducibility; the rationale for withholding weights is inconsistent.",
      "evidence": "The F2 weights omega_1-omega_6 are withheld 'because they carry no empirical content'. The equally uncalibrated F1 weights (1.25, 0.20, 0.22, 0.75) and U weights (0.45, 0.75) are printed (Eqs. C1, C3). Table 7 cannot be reproduced from the paper.",
      "suggested_fix": "Print the F2 and Level-3 constants in Appendix C (as SIMULATED) or in a supplementary file. Add them to the log first."
    },
    {
      "file": "en/back.tex",
      "location": "L113-117 (Table 8)",
      "issue": "Check 3: the rival signatures are not discriminant.",
      "evidence": "Organisational: episodes 'stop at internal approval, budget allocation or governance capacity'. Cost: episodes 'rejected in business-case review on cost or return grounds'. Both map to budget parameters (b_i^r vs B_tot, c_i^r), and no observable separates a budget refusal from a cost rejection.",
      "suggested_fix": "Define a distinguishing observable. For example, cost: a rejection that cites an absolute return threshold; allocation: a rejection that cites relative priority, or reversal after reallocation without a change in the business case."
    },
    {
      "file": "en/abstract.tex; en/back.tex",
      "location": "abstract S1; back L186",
      "issue": "Check 6: a claim about field practice has no source.",
      "evidence": "'Gap research often reads sparse co-occurrence between AI functions and decision functions as structural separation'. No entry in citation_map.json supports it. The abstract's 'is easily read as' is acceptable; 'often' is an empirical claim.",
      "suggested_fix": "Cite representative co-word / literature-based-discovery / bibliometric gap studies (add them to the library), or reword as 'can be read as'."
    },
    {
      "file": "en/front.tex",
      "location": "L43",
      "issue": "Check 6: a minor stretch of a role note.",
      "evidence": "'real ties of the kind Burt's construct presupposes [burt1992structural]'. 'Real ties and observed outcomes' is the role note of burt2004structural; the burt1992 note covers non-redundant contacts and constraint.",
      "suggested_fix": "Cite burt2004structural here, or rephrase as 'non-redundant contacts of the kind Burt's construct presupposes'."
    },
    {
      "file": "en/back.tex; en/appendix.tex",
      "location": "back L122; appendix L12; front L143",
      "issue": "Check 4: anonymity for blind review.",
      "evidence": "'(identified in the thesis, anonymised here)' reveals the thesis origin. 'PR #5 of the project repository' points to an unnamed, non-anonymised repository.",
      "suggested_fix": "Delete 'identified in the thesis'. Provide an anonymised repository link (for example via an anonymous-review mirror) for the plans and the canonical model file."
    },
    {
      "file": "en/main.tex; en/appendix.tex",
      "location": "main L17, L27, L37; appendix L336, L340",
      "issue": "Check 5: compilation depends on the working directory (unchanged from round 1); equation references are styled inconsistently.",
      "evidence": "\\input{abstract}, \\graphicspath{{../figures/}} and \\bibliography{../references} resolve only from en/. There is no Makefile or latexmkrc. The appendix uses 'Eq.~\\ref{eq:mlp_tau}' where the rest of the paper uses \\eqref. Otherwise clean by script: 0 undefined references, 0 duplicate labels, all citation keys resolve, environments balanced, all floats [tbp]. Not compiled (pdflatex unavailable).",
      "suggested_fix": "Add a latexmkrc or a README build line ('cd en && latexmk -pdf main'). Use \\eqref consistently."
    }
  ],
  "Round1_Resolution": [
    {
      "weakness": "1. Framing / straw man: the premise was the project's own and uncited",
      "status": "partially",
      "evidence": "Resolved in substance: front L6-8 states that no cited work makes the claim and that the premise is the project's own, drawn from V9 co-occurrence. The title and contributions are recast around the invalid inference. Still open: the new framing rests on an uncited generalisation about field practice ('Gap research often reads ...', back L186; abstract S1), with no co-word or literature-based-discovery anchor, so the surprise value for IS readers is still not established."
    },
    {
      "weakness": "2. Construct validity of Study 2 (G06Q10/04 overlap; H1a granularity)",
      "status": "partially",
      "evidence": "Caveats were added in front L48, studies L186 and L204, and back L156, and the test is relabelled as measuring the 'technological proximity of patent classes'. Neither requested analysis was run: '/04 and /06 are not reported separately'; 'We did not compute a subgroup-level reference set'. s2 still contains /04, so it does not isolate the overlap."
    },
    {
      "weakness": "3. The firm-level null is confounded by degree (T2 'reversal')",
      "status": "partially",
      "evidence": "The confound is conceded everywhere (studies L353, L377; Table 7 caption; Fig. 6 caption; back L26, L168), and 'mixed firms are not brokers' is gone. No null preserving both degree and portfolio was run. The RQ2 conclusion ('does not support a firm-level structural hole', studies L386; back L19) still leans on T2, while the degree-controlled P5 comparison pointed the other way."
    },
    {
      "weakness": "4. RQ2 understated the significant T1 result",
      "status": "resolved",
      "evidence": "T1 is now 'statistically significant but small' (p = .001, both stratifications; 15%/9% residual) in the abstract, front L16, studies L375-377, back L17, L168 and L188, and 'PARTIAL ... not that nothing remains'. A new caveat on the 'small' metric is raised in this round."
    },
    {
      "weakness": "5. Study 1 directional defence assumed non-differential error",
      "status": "resolved",
      "evidence": "Studies L93-97 limit the bound to non-differential error and explain the fixed-margin mechanism. L99 calls the 'as truth' runs stress tests; L127 qualifies 'DEFENSIBLE'; boundary (viii) is added; Table 3 notes n = 20. Residual: kappa CIs are not reported, and the removal evidence (13/16) is not connected to the 9/16 concentration argument."
    },
    {
      "weakness": "6. Preregistration rhetoric exceeded the design",
      "status": "resolved",
      "evidence": "front L143-147, studies L170 and L265, back L173 and Appendix A all state: self-timestamped commits, not OSF; only Plan 1 confirmatory; Plans 2-4 data-informed with rules fixed in advance; M06-P designed after M06 failed and the three-test results were known; Plan 4 motivated by P5. The old 'not the product of choosing a null after seeing the results' is removed, and Nosek is cited only for the purpose of preregistration. M06-P provenance was verified against V9_MATRIX_RESULTS.json."
    },
    {
      "weakness": "7. Statistical calibration gaps (clustering, M06-P, BH/core, synthetic generator)",
      "status": "partially",
      "evidence": "All four gaps are disclosed (studies L30, L199, L263, L265, L334; back L161-166). None is remedied: there is no document-level permutation calibration and no M06-P type-I rate. M06-P is still listed as a contribution (front L20)."
    },
    {
      "weakness": "8. The MLP agenda and Study 3 did not follow from the evidence",
      "status": "partially",
      "evidence": "Reframed as 'a consequence, not a conclusion' with five rival explanations (back L33-35), the V9 anchor withdrawn (L54), and the probes called 'by construction' (L95, L178). Study 3 gains a rival-signature table, unit and episode definition, human coding and decision/stop rules (back L100-145; appendix C.7). Still open: a full section remains in the main text; the F2 weights are withheld; all thresholds are deferred; the allocation and cost signatures overlap; Figure 1 still depicts 'hole not supported -> MLP' and 'Study 3 calibrates the model'."
    }
  ]
}
```
