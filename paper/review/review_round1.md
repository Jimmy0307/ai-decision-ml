THOUGHT:
<THOUGHT>
The manuscript tests a premise: that AI and managerial decision-making are separated by a Burt structural hole. It uses three data lines: a literature co-occurrence programme (Study 1), a screen of six public relational sources, and four preregistered analyses of US patent citations (Study 2). It then moves to a simulated tri-level programming model and a planned enterprise study (Study 3). The patent work is the strongest part. The aggregate design is careful: time-stratified expectations, a relative rather than absolute criterion, a synthetic calibration, six sensitivity checks and an honest amendment log. The paper also keeps unusually disciplined claim boundaries. Depleted cells are never called gaps, model agreement is never called reliability, and the MLP outputs are labelled simulated throughout.

Numbers (check 1). I compared every number in the abstract, Sections 4-5 (studies.tex), the tables of Sections 6-7 (back.tex) and all appendix tables against experimental_log.md. I also ran a token-level script over all en/*.tex files. Every substantive number appears in the log. I recomputed the derived values and all are consistent:
- 30,843/10,112 = 3.05; 21,820/6,686 = 3.26; 9,023/3,426 = 2.63; 3.05/1.809 = 1.69; 886/3,700 = 0.24;
- (1-0.356)/(1-0.240) = 85%; (1-0.307)/0.760 = 91%; 18/27 = 67%; 23/29 = 79%;
- all ten O/E values in Table 5;
- the CPC heat-map markers: 8/7 in Part A, 9/8 in Part B;
- the nine MLP scenarios and the C < F < D ordering.

The remaining number-level problems are few:
- a row size misattributed to a cell (back.tex L18);
- a figure label that contradicts the DEC definition;
- an unstated regime/budget attribution for the threshold probe;
- a scope difference between P5 and the firm null that is never reconciled;
- a Study 1 figure whose period values both lie outside the pooled O/E of the most extreme cell;
- several items in Appendix A (commit ids, decision-rule thresholds) that are not in the ground-truth log.

Substance. A skeptical management/IS reviewer would attack first the framing and construct validity, not the arithmetic.
(1) The premise being refuted is the project's own. No cited source in the literature asserts that AI and decision-making are separated by a structural hole. The negative result therefore risks refuting a straw man.
(2) Study 2 measures citation flows between inventors in CPC G06N and in G06Q10/04+/06. G06Q10/04 (forecasting/optimisation) overlaps methodologically with machine learning, so an OE of about 3 is close to expected by construction. H1a also compares a narrow two-subgroup DEC set with 179 broad main groups, which favours high OE.
(3) The firm-level "reversal" rests on a portfolio null that does not preserve firm degree. Constraint is driven largely by degree, as the paper's own citation of Everett & Borgatti says. The null median constraint (0.104) and the degree-matched null median (0.444) differ by a factor of four, so T2 is a degree artefact and cannot show "no brokerage advantage". Meanwhile T1 rejects the portfolio null at p = .001 in both stratifications. Under Plan 4's own rule, that is half of an organisational-hole finding, and the conclusions understate it.
(4) Study 1's "direction is defensible" rests on non-differential misclassification. The paper's own analytic bound (accuracy product >= 0.71 required vs about 0.07 implied) shows that the random-error model cannot be reconciled with the audit. The paper also documents a differential mechanism: same-term self-pairing in the prediction x prediction cell. In a closed fixed-margin matrix, inflating that cell mechanically depletes its row and column, and 9 of the 16 depleted cells lie in the PREDICTION_RISK_ESTIMATION row or the PREDICTION_DIAGNOSIS column.
(5) The preregistration rhetoric is stronger than the design supports. Plans 2-4 were each written after earlier results were known. All were committed within about a day in the authors' own repository. M06-P was frozen after M06 failed and after the three-test cell results were known. Studies L375 nonetheless claims that the null reversal "is not the product of choosing a null after seeing the results".
(6) The MLP agenda does not follow from the evidence. Ruling out a knowledge-flow hole among patent inventors does not make an organisational bottleneck "more plausible" than the many other explanations: technical maturity, data, ROI, regulation, trust. The model's original empirical anchor (the 16 V9 cells) has been withdrawn. F2 is not specified, the simulated probes are tautological, and the Study 3 plan has no concrete decision rules, sample or identification strategy. The paper reads as two papers: a careful negative-result/methods paper and an unrelated modelling agenda.

Positioning the negative result. The paper would be much stronger if it were reframed as a measurement and methods paper. Its message would be: "Gap claims built on co-occurrence fail. Here is a calibrated, preregistered flow-based alternative, and here is what it shows for AI and decision technologies." Study 1 would be condensed to a cautionary case, and the MLP/Study 3 material would be removed or cut to a short outlook.

LaTeX (check 5). There are no undefined references, no duplicate labels, braces and environments are balanced, and every citation key resolves. pdflatex is not installed here, so I did not compile. The risks I found are:
- path-dependent compilation from en/;
- an overfull Table 1;
- 17 mostly [t]-only floats ahead of the clearpage.

Citations (check 6). Most uses match their role notes. The exceptions:
- Burt (1992) is credited with the directed, group-labelled requirement, which comes from Gould-Fernandez;
- Colson and Fortuny-Amat/McCarl are cited for a modelling restriction they do not support;
- Nosek is used to certify that the choice of null was not data-dependent;
- Burt is cited after an empirical finding of this paper;
- the "common explanation" premise has no source.

Overall: a disciplined, transparent piece of empirical work. It is framed around a straw-man premise, it has a confounded firm-level null and a weakly defended Study 1 directional claim, and it carries an MLP agenda that the evidence does not support. In its current form it is not ready for a management/IS journal. A refocused version could be.
</THOUGHT>

REVIEW JSON:
```json
{
  "Summary": "The paper tests the premise that AI and managerial decision-making are separated by a Burt structural hole. Study 1 re-examines a literature programme: an LLM-coded 10x12 AI-function by decision-function co-occurrence matrix (2,180 document edges, four null tests with BH-FDR), plus historical citation, co-author and higher-order network searches (V6-V11.1). It concludes that 16 depleted cells are directionally robust but lose significance under realistic misclassification (human kappa 0.05/0.14), and that no broker was confirmed. A screen of six public relational sources finds none that is flow-valid. Study 2 applies four preregistered analyses to US patents (AI = CPC G06N; DEC = G06Q10/04 + G06Q10/06). AI-DEC applicant citations run at OE 3.05 (95% CI 2.94-3.17), above 97.8%/92.2% of reference pairings, so both relative hole criteria fail (HOLE_NOT_SUPPORTED, 0/6 sensitivity checks disagree), with a declining but PERSISTENT trend. Cell-level depletions in a 6x7 CPC matrix are modest and do not replicate across time halves; the paper proposes a block-preserving null (M06-P) because the preregistered document-preserving swap is degenerate. At the firm level, specialist AI and DEC firms are under-connected (O/E 0.24), but a portfolio-preserving owner-permutation null reproduces 85-91% of this gap, and mixed-portfolio firms are more constrained than under that null (verdict PARTIAL). The paper then hypothesises that the integration bottleneck is organisational, formalises it in a tri-level programming model illustrated only with simulated parameters, and outlines a preregistered enterprise study (Study 3) to calibrate it.",
  "Strengths": [
    "Unusually transparent research practice: four preregistrations with commit ids, a dated amendment log that leaves the frozen texts unchanged (Appendix A), provenance grades (DIRECT / HISTORICAL / USER_REPORTED / SIMULATED), and explicit claim boundaries (Section 3.4) that are largely respected throughout.",
    "The aggregate patent test is well designed: time-stratified configuration expectations, a relative criterion (H1a/H1b) motivated by the field-locality of citing, a Poisson cluster bootstrap over citing patents, synthetic calibration before real data, and six preregistered sensitivity specifications that all agree (Table 4, Figure 3).",
    "Applicant-only citations are used as the primary flow measure, with examiner citations handled through a sensitivity check (Alcacer & Gittelman), and the PatentsView pre-2013 'cited by other' labelling is disclosed (Amendment A2).",
    "Honest treatment of a failed preregistered null: the 0-of-21.8M swap degeneracy of M06 is diagnosed structurally and reported as a deviation (Amendment B1) rather than hidden.",
    "The portfolio-preserving firm null is a sensible idea: firm-level separation between specialist firms is partly mechanical, and the paper shows this quantitatively (85-91%).",
    "Study 1 is reported with a self-critical data-validity re-analysis: an analytic attenuation bound, misclassification simulations, re-implementation, seeds, track-stratified and period checks, and keyword triangulation. The paper does not oversell its own earlier work.",
    "Model-to-model agreement is consistently distinguished from human reliability, and all MLP outputs are clearly labelled as simulated."
  ],
  "Weaknesses": [
    "Framing / straw man (front.tex L6-8, L18; back.tex L40-42). The premise being refuted is the project's own. No cited work in management/IS claims that AI and decision-making are separated by a structural hole; the 'common explanation' (front L6) carries only theory citations (Burt, Granovetter). A negative result needs a credible positive claim to refute. Without one, the headline contribution ('no hole; over-connected') has low surprise value for an IS readership. The title ('Unresolved in Organisations?') promises organisational evidence that the paper does not contain.",
    "Construct validity of Study 2 (studies.tex L169-195; front.tex L48). Citation flows between inventors in G06N and G06Q10/04+/06 measure technological proximity of patent classes, not integration between AI and managerial decision-making communities. G06Q10/04 (forecasting/optimisation) overlaps methodologically with machine learning, so over-connection is close to definitional. H1a compares a narrow, purpose-built two-subgroup DEC set with 179 broad CPC main groups; narrow, homogeneous groups typically yield higher OE, which biases the percentile upward. Report /04 and /06 separately and use a granularity-matched (subgroup-level) reference set.",
    "The firm-level null is confounded by degree (studies.tex L337-377; back.tex L20, L33). Permuting owner sets within strata preserves portfolio counts but not firm degree or tie concentration, and constraint is driven largely by degree (Everett & Borgatti, cited at front L39). The null median constraint (0.104) is a quarter of the degree-matched null median (0.444), so the 'reversal' (p = .001 vs p = 1.000) is what a degree-inflating null produces mechanically. It is not evidence that mixed firms lack brokerage advantage. Use a null that preserves both portfolio and degree, or compare degree-residualised constraint.",
    "RQ2 understates T1 (studies.tex L364, L377; back.tex L26, L186; appendix L44). T1 rejects the portfolio null at p = .001 in both stratifications. Under Plan 4's own rule this is one of the two organisational-hole criteria (hence PARTIAL). The residual 9-15% specialist separation is statistically significant group-level separation beyond portfolio. Concluding that 'no firm-level structural hole beyond portfolio composition is supported' conflates 'no evidence of brokers' with 'no separation'. Report the residual as a positive, if modest, finding.",
    "Study 1's directional claim is not defended (studies.tex L85-92; back.tex L31). The defence ('random error can only attenuate a depletion') assumes non-differential misclassification. The paper's own bound shows this model is irreconcilable with the audit (accuracy product >= 0.71 needed vs about 0.07 implied), which implies differential error. One differential mechanism is documented: same-term self-pairing inflates prediction x prediction. In a closed fixed-margin matrix (back L24), inflating one cell mechanically depletes its row and column, and 9/16 depleted cells lie in the PREDICTION_RISK_ESTIMATION row or PREDICTION_DIAGNOSIS column. The human-human kappa rests on n = 20 with 10-12 categories; using one of two disagreeing coders 'as truth' (Table 3) is incoherent. Study 1 is best presented as a cautionary measurement case, and condensed.",
    "The preregistration rhetoric exceeds the design (studies.tex L253, L375; appendix L30-44; back L171). Plans 2-4 were written sequentially after earlier results were known. All plans, amendments and the data download fall within about 1-2 days (2026-11-18/19), in self-controlled git commits whose timestamps are author-set. M06-P was frozen only after M06 failed and three-test cell results were known. Studies L375 still asserts that the null reversal 'is not the product of choosing a null after seeing the results', which contradicts back L171. Recommend third-party registration (OSF/AsPredicted), public repository links, and confirmatory/exploratory labels per analysis.",
    "Statistical calibration gaps (studies.tex L20-27, L253-255, L322; Table 6). In Study 1 and in Part B (66,056 edges from 30,843 citations), the exact and raw tests treat edges as independent although documents contribute several edges. P2's false-positive calibration uses stub-permutation null matrices that share that independence assumption, so it cannot detect clustering-induced anti-conservatism. M06-P, offered as a methodological contribution, has no reported type-I calibration and no formal statement of its null hypothesis. BH within a fixed-margin table (negative dependence) followed by intersection across four dependent tests gives a core whose error rate is undefined.",
    "The MLP agenda and Study 3 do not follow from the evidence (back.tex L37-155). (a) Ruling out a knowledge-flow hole among patent inventors does not make organisational constraints 'more plausible' than other explanations: technical maturity, data, ROI, regulation, user trust and skills. This is a non sequitur, even when labelled a hypothesis. (b) The model's original empirical anchor (the 16 V9 depleted cells, back L90) is withdrawn, leaving the parameters unmotivated. (c) F2 and the RealizedValue/ResidualRisk functions are not specified, so the model is not reproducible from the text. (d) The simulated probes are tautological: removing a permission makes the permission bind. (e) The Study 3 plan has no sample size, no operational definition of 'blocked by permission vs capability', no concrete stop rule and no identification strategy. The manuscript reads as two papers.",
    "The method contributions are modest or under-validated (front.tex L20, L61; back L31-35). Zero indirect constraint in a strict bipartite graph and closure created by projection are known results (Opsahl 2013; Newman 2001; Everett & Borgatti 2020). The 'Gap Validity' alternative-route checks are guaranteed in a 120-cell matrix with 104 observed cells (studies L153, L316). Presenting identities as empirical confirmations ('both confirm', front L61) inflates the contribution.",
    "Internal inconsistencies:\n- studies L36 says the strict filter did not create the depletion; back L164 says 'the filtering step itself may shape the pattern'.\n- studies L151 says the V6-V11.1 lines 'could not have carried Burt's construct even with perfect data', yet V6/V8/V9 are citation lines, and the paper argues that citations are directed flows (front L10, L67, L75).\n- Appendix B1 says three-test cells are exploratory, but Table 5 uses the three-test rule without that label.\n- studies L324 contrasts patent instability with literature stability, while back L24 concedes that the criteria differ (direction only vs three-test significance), and Part A's first half has only 543 documents.",
    "Presentation for a management/IS journal. The text is dense with project-internal jargon (V5-V11.1, V9.1, Route A, sidecar, Limitation Scout, G2 candidates, Gap Validity, S-tech) and reads like an audit trail. HISTORICAL/USER_REPORTED network results (Table 2) take main-text space but cannot be verified. Sixteen tables and seven figures crowd out the argument. Some figure text overstates the findings: 'no hole' (Fig. 1) and 'mixed firms are not brokers' (Fig. 6)."
  ],
  "Originality": 2,
  "Quality": 2,
  "Clarity": 2,
  "Significance": 2,
  "Questions": [
    "Which published work in management/IS asserts the AI-decision structural-hole premise? Can you cite it and state the claim you refute in its own terms?",
    "What are OE(AI, G06Q10/04) and OE(AI, G06Q10/06) separately? How does OE(AI,DEC) rank against a reference set of CPC subgroups of comparable size, rather than main groups?",
    "Under the portfolio-preserving null, how do firm degrees change relative to observed? Does T2 survive a null that preserves both portfolio and degree, or a degree-residualised constraint comparison?",
    "Do you accept that T1 (p = .001 in both stratifications) is significant evidence of specialist separation beyond portfolio composition? How should readers interpret the 9-15% residual?",
    "Given that the random-misclassification model cannot reconcile the observed magnitude with the audited accuracy, on what basis is the direction of the 16 depleted cells 'DEFENSIBLE'? How many of the 16 keep their direction after self-paired records are removed?",
    "What is the type-I error rate of M06-P and of the exact/raw tests under a document-level (clustered) permutation null, in both Study 1 and Part B?",
    "In Study 1, what share of documents contribute complete row x column blocks? Was the document-preserving test there partially degenerate as well?",
    "Were the M06-P results in V9_MATRIX_RESULTS.json (logged under Preregistration 2) computed before or after commit d641256?",
    "How do the firm-null scope (14,600 firms; 162,339 citations) and the P5 network (6,201 firms with ties; 109,508 citation weight) relate? What exactly does 'identity permutation reproduces P5 exactly' verify?",
    "How was the synthetic calibration network generated? What power does H1a/H1b have when the baseline OE is far above the reference lowest quartile, as in the real data?",
    "Why did Amendment A2 declare H3 (firm brokers) moot, while Plans 3-4 then tested firm brokerage?",
    "For Study 3: how many firms and processes will be sampled? How will 'feasible on capability grounds but blocked by permission' be observed rather than inferred from the model? What exactly are the stop rule and the falsifying pattern?"
  ],
  "Limitations": [
    "Patent citations among inventors are not evidence about how organisations integrate AI into managerial decisions. The organisational-bottleneck hypothesis is not informed by the firm-level citation network.",
    "The DEC operationalisation overlaps methodologically with AI, and the main-group reference set is coarser than the DEC set; both bias toward over-connection.",
    "The portfolio null does not preserve firm degree, so the constraint comparison is confounded.",
    "The Study 1 human reliability estimates rest on n = 20, and misclassification is plausibly differential, which undermines both significance and direction.",
    "Plans 2-4 were data-informed sequential designs within about a day, timestamped only by self-controlled commits.",
    "M06-P and the edge-level exact tests lack calibration under clustered nulls.",
    "The MLP objective F2 and the value/risk functions are not specified; all MLP parameters are simulated, and the original empirical anchor has been withdrawn.",
    "The study covers US patents only, and assignee disambiguation is checked for only 54 firms."
  ],
  "Ethical Concerns": false,
  "Soundness": 2,
  "Presentation": 2,
  "Contribution": 2,
  "Overall": 4,
  "Confidence": 4,
  "Decision": "Reject",
  "Integrity_Findings": [
    {
      "file": "en/back.tex",
      "location": "L18",
      "issue": "Check 1: a row size is attributed to a cell.",
      "evidence": "Text: 'Apart from the quantum-computing cell (74 edges in Part A)'. Log E3.2 L273: 'The quantum-computing row is tiny: 74 edges in A'. The G06N10 x PERFORMANCE cell itself has O = 1, E = 12.0 (log L271).",
      "suggested_fix": "Write 'Apart from the quantum-computing cell (1 observed vs 12.0 expected in Part A; the whole quantum row has 74 edges)'."
    },
    {
      "file": "figures/fig_research_design.png",
      "location": "Study 2 box, line 2",
      "issue": "Check 1/4: the figure's DEC definition contradicts the text and the log.",
      "evidence": "Figure: 'AI (G06N) x Decision (G06Q10)'. Log L170 and front.tex L80 caption: DEC = G06Q10/04 + G06Q10/06. 'All G06Q10' is sensitivity check s2 (log L209).",
      "suggested_fix": "Relabel as 'Decision (G06Q10/04 + /06)'."
    },
    {
      "file": "figures/fig_research_design.png",
      "location": "Study 2 box, line 3",
      "issue": "Check 2: absence of a hole is asserted. The caption qualifies only the arrow label, not the box text.",
      "evidence": "Box text: 'Technology level: OE 3.05, no hole'. front.tex L80 caption: 'it does not prove that none exists' (refers to the arrow only). idea.md sec. 10: the verdict is HOLE_NOT_SUPPORTED.",
      "suggested_fix": "Change to 'OE 3.05, hole not supported'."
    },
    {
      "file": "figures/fig_firm_null.png",
      "location": "Figure title",
      "issue": "Check 2: overclaim.",
      "evidence": "Title: 'mixed firms are not brokers'. The log (E3.4 L356) supports only 'the lower constraint of MIXED firms does not survive', i.e. no brokerage advantage relative to this null.",
      "suggested_fix": "Retitle: 'mixed-portfolio firms show no brokerage advantage under this null'."
    },
    {
      "file": "en/back.tex",
      "location": "L131",
      "issue": "Check 1: the regime and budget of the threshold probe are inferred, not logged.",
      "evidence": "Text: 'F1 2.244, the value of the regime-F, budget-5 baseline'. Log E4 L397-399 gives F1 2.244 and 1.450 but does not state the regime or budget of the selection-threshold probe.",
      "suggested_fix": "Confirm the regime and budget from MLP_SOLVER_RESULTS_v1_0.json and add them to the log, or drop the attribution."
    },
    {
      "file": "en/studies.tex",
      "location": "L328 vs L342",
      "issue": "Check 1/4: two scopes for the same firm network are not reconciled.",
      "evidence": "P5: 6,201 organisations with ties, 20,681 ties, weight 109,508 (log L315). Firm null: 127,114 patents, 14,600 firms, 162,339 citations (log L344). The text says 'The identity permutation reproduces P5 exactly' without explaining the difference.",
      "suggested_fix": "State what the 14,600 and 162,339 include (firms without ties? self-citations? DEC-only and AI-only patents?) and how P5 is derived from that scope."
    },
    {
      "file": "figures/fig_study1_direction.png",
      "location": "Row 'Prediction Risk Estimation x Human Review Accountability'",
      "issue": "Check 1: both period values lie outside the pooled value of the same cell. This needs explanation.",
      "evidence": "Pooled: O = 6, E = 44.9 (studies.tex L32; log L55), so log2(O/E) = -2.90. The figure shows about -2.45 (<= 2023) and about -2.70 (>= 2024): both periods are less depleted than the pooled cell. This is possible only if period-specific margins are used.",
      "suggested_fix": "State in the caption that E is recomputed from period-specific margins. Report the period O and E values in Appendix B."
    },
    {
      "file": "en/appendix.tex",
      "location": "L26, L38, L44, L60, L66",
      "issue": "Check 1/4: commit ids, decision-rule thresholds and verdict labels are not in the ground-truth log.",
      "evidence": "Not present in experimental_log.md:\n- commits a158e70 (A1) and 1eb7319 (Seeding);\n- '>= 4 of 6 sensitivity checks disagree -> FRAGILE';\n- the labels PARTIAL_NOT_CLAIMED, CLOSING, NARROWING_BUT_OPEN, ORGANISATIONAL_HOLE_BEYOND_PORTFOLIO, PORTFOLIO_ARTEFACT and TECH_MIX_SENSITIVE;\n- the P5 criterion 'below both MIXED O/Es';\n- 'three-test agreement for P3 and P9'.\nThe log header says that writers must not introduce numbers absent from the log.",
      "suggested_fix": "Add these items to the log with their provenance (the frozen preregistration texts), or cite the preregistration files directly as a separate graded source."
    },
    {
      "file": "en/abstract.tex",
      "location": "L1",
      "issue": "Check 1/4: preregistrations are miscounted as 'tests'.",
      "evidence": "Abstract: 'Study 2 applies four preregistered tests'. Log L162-180: four preregistrations, containing an aggregate test with six sensitivity checks, a 42-cell battery, ten suite modules and a two-statistic firm null.",
      "suggested_fix": "Write 'four preregistered analyses' (as in front.tex L14)."
    },
    {
      "file": "en/studies.tex",
      "location": "L322",
      "issue": "Check 1: stability is overstated.",
      "evidence": "Text: 'The significant set is stable across seeds'. Log L284: in Part A, 20 cells are always significant and 4 are boundary cells.",
      "suggested_fix": "Write 'stable in Part B (0 boundary cells); in Part A, 4 boundary cells'."
    },
    {
      "file": "en/abstract.tex; en/back.tex",
      "location": "abstract L1 ('no broker was confirmed'); back L186 ('no network line confirmed a broker')",
      "issue": "Check 2: HISTORICAL / USER_REPORTED results are stated without their grade (boundary vii).",
      "evidence": "The V6-V11.1 results are HISTORICAL / USER_REPORTED (log E1.6), and idea.md sec. 10 requires them to be labelled. front L16 and back L22 do label them; the abstract and the conclusion do not.",
      "suggested_fix": "Add '(historical, unverified project logs)' or similar in both places."
    },
    {
      "file": "en/back.tex",
      "location": "L190",
      "issue": "Check 2: the conclusion goes beyond the evidence and leans toward stating the organisational bottleneck as a finding.",
      "evidence": "Text: 'the explanation is therefore unlikely to lie in a missing bridge between knowledge communities'. The evidence concerns citation flows between patent classes and assignees, not organisational knowledge communities. idea.md sec. 10: the organisational bottleneck is a hypothesis.",
      "suggested_fix": "Write 'the patent evidence does not support a missing bridge between AI and decision technologies; whether the difficulty lies inside organisations is the hypothesis Study 3 will test'."
    },
    {
      "file": "en/studies.tex",
      "location": "L364",
      "issue": "Check 2: causal wording (boundary iii).",
      "evidence": "Text: 'Portfolio composition alone thus produces most of the separation'. The null reproduces the separation; causation is not shown.",
      "suggested_fix": "Write 'A null that holds portfolios fixed reproduces most of the separation'."
    },
    {
      "file": "en/studies.tex",
      "location": "L38, L155 (also figure 2 title)",
      "issue": "Check 2/3: 'under-integration ... persistent ... no sign of closing' implies volume and significance that the paper elsewhere disclaims.",
      "evidence": "back.tex L24: a depleted cell 'describes the composition of an existing connection, not its volume'. The re-analysis: significance is NOT DEFENSIBLE. p = .86 is a non-difference, not evidence of persistence.",
      "suggested_fix": "Write 'the compositional shortfall has the same direction in both periods; we find no evidence of change (p = .86)'. Avoid 'under-integration'."
    },
    {
      "file": "en/studies.tex",
      "location": "L312 (Table 6, P5 row)",
      "issue": "Check 2: the hole criterion is reported as met with no qualifier inside the table.",
      "evidence": "Table text: 'preregistered firm-level criterion met'. Only the prose (L328) adds that it is not a confirmed hole and was superseded by Plan 4.",
      "suggested_fix": "Add to the table cell: 'superseded by Plan 4 (PARTIAL); not a confirmed hole'."
    },
    {
      "file": "en/studies.tex",
      "location": "L375",
      "issue": "Check 2/4/6: the claim that the null choice was not data-dependent contradicts the chronology.",
      "evidence": "Text: 'Because the null was frozen before computation [Nosek], this reversal is not the product of choosing a null after seeing the results'. appendix L42: Plan 4 was 'written after P5'. back L171: 'the choice of which follow-up questions to ask was informed by data'.",
      "suggested_fix": "Write: 'The null was frozen before its replicates were computed, but it was designed after the P5 result was known; the reversal should be read with that in mind.'"
    },
    {
      "file": "en/studies.tex; en/back.tex",
      "location": "studies L85-92; back L31 ('direction can survive where significance does not')",
      "issue": "Check 3: the directional defence assumes non-differential error, but the paper's own numbers imply differential error.",
      "evidence": "Studies L90: an accuracy product >= 0.71 is required vs about 0.07 implied, so the two 'cannot be reconciled' under random error. Same-term self-pairing (L50) is differential and inflates prediction x prediction. Under fixed margins this depletes the PREDICTION_RISK_ESTIMATION row (5 depleted cells) and the PREDICTION_DIAGNOSIS column (4 depleted cells) mechanically.",
      "suggested_fix": "State that the attenuation argument does not apply under differential error. Re-run the direction check for all 16 cells after removing self-paired records. Downgrade 'direction DEFENSIBLE' accordingly."
    },
    {
      "file": "en/studies.tex",
      "location": "L92, Table 3 (L103-104)",
      "issue": "Check 3: the scenarios that treat one human coder as truth are ill-defined.",
      "evidence": "Human-human kappa is 0.05/0.14 on n = 20 (Table 2), yet 'First human coder as truth' is called a 'realistic' scenario. No confidence intervals are given for kappa.",
      "suggested_fix": "Report kappa with CIs. Frame the result as a failure of measurement validity rather than a calibrated error model."
    },
    {
      "file": "en/studies.tex",
      "location": "L20-27; L255; L322 (P2)",
      "issue": "Check 3: BH and edge-level tests are used without accounting for clustering; the calibration is circular.",
      "evidence": "Exact and raw tests treat document edges as independent: Study 1 has 2,180 edges from 1,729 documents, and Part B has 66,056 edges from 30,843 citations. P2 calibrates on stub-permutation null matrices that make the same independence assumption. BH under fixed-margin negative dependence, followed by intersection across four dependent tests, gives a core with no defined FDR. M06-P has no type-I calibration.",
      "suggested_fix": "Calibrate the exact, raw and M06-P tests under a document-level permutation null. Report Benjamini-Yekutieli as a robustness check, or calibrate the core rule as a whole."
    },
    {
      "file": "en/studies.tex",
      "location": "L337-377; back.tex L33",
      "issue": "Check 3: the portfolio-preserving null does not preserve firm degree, so the T2 'reversal' is degree-confounded.",
      "evidence": "Under the portfolio null, the MIXED median constraint is 0.104/0.116; under the degree-matched null (P5) it is 0.444. Constraint is driven by degree (front L39, citing Everett & Borgatti). back L33 claims the portfolio null 'must preserve the structure that generates the data', but it does not preserve degree.",
      "suggested_fix": "Add a null that preserves both portfolio and degree, or compare degree-residualised constraint. Temper 'only the portfolio-preserving null holds fixed the structure that generates the data'."
    },
    {
      "file": "en/studies.tex; en/back.tex",
      "location": "studies L377; back L26, L186",
      "issue": "Check 3: the RQ2 conclusion understates a significant result.",
      "evidence": "T1 is 0.240 vs null 0.356/0.307, p = .001 in both stratifications. Plan 4's rule (appendix L44) counts this as one of the two hole criteria, which is why the verdict is PARTIAL. The text concludes that no firm-level hole beyond portfolio is supported.",
      "suggested_fix": "Write 'a modest but significant specialist separation beyond portfolio composition remains; there is no evidence that mixed firms broker it'."
    },
    {
      "file": "en/studies.tex",
      "location": "L189; front.tex L117",
      "issue": "Check 3: the scope of the calibration is overstated.",
      "evidence": "The synthetic no-hole baseline OE (0.388) sits next to Q1 (0.356). The real AI-DEC OE (3.05) is about 4x the AI-side Q1 (0.787). Detecting 30% suppression in synthetic data says little about power at the real baseline. The synthetic generator is not described.",
      "suggested_fix": "Describe the generator. Report the suppression needed to reach H1a/H1b at the real baseline. Qualify 'calibrated'."
    },
    {
      "file": "en/studies.tex",
      "location": "L191 (H1a)",
      "issue": "Check 3: the reference set is not granularity-matched.",
      "evidence": "DEC is two CPC subgroups (G06Q10/04, /06), while the 179 reference X are main groups with >= 2,000 patents. G06Q10/04 (forecasting/optimisation) is methodologically adjacent to G06N.",
      "suggested_fix": "Add a subgroup-level reference set of comparable size. Report /04 and /06 separately."
    },
    {
      "file": "en/studies.tex; en/back.tex",
      "location": "studies L324 vs back L24",
      "issue": "Check 3/4: the Study 1 vs Study 2 persistence contrast uses different criteria and an underpowered half.",
      "evidence": "studies L324: patent depletions are 'unstable over time, unlike the literature depletions'. back L24: Study 1 uses direction only, while patents require three-test significance in both halves. Part A's first half has 543 documents (appendix L178).",
      "suggested_fix": "Apply the same direction-only criterion to the patent halves, or delete the contrast at L324."
    },
    {
      "file": "en/studies.tex",
      "location": "L151; front.tex L75",
      "issue": "Check 3/4: the claim that the citation lines could not carry Burt's construct conflicts with the paper's own premise that citations are flows.",
      "evidence": "L151: 'These lines could not have carried Burt's construct even with perfect data'. V6, V8 and V9 are citation lines (Table 2). front L10/L67 argue that citations are directed flows, and front L75 says that only line (iii) proved flow-valid.",
      "suggested_fix": "Restrict L151 to the co-author/projection lines (V7, V11). Explain separately why the paper-citation lines failed (labels, sampling, scale)."
    },
    {
      "file": "en/front.tex; en/studies.tex",
      "location": "front L61 ('both confirm'); studies L153, L316",
      "issue": "Check 3: mathematical identities and guaranteed properties are presented as empirical checks.",
      "evidence": "The zero indirect term in a strict bipartite graph is derived at front L61. Alternative routes are guaranteed when 104/120 cells are observed.",
      "suggested_fix": "Present Gap Validity as a derivation, not as evidence."
    },
    {
      "file": "en/studies.tex; en/back.tex",
      "location": "studies L36 vs back L164",
      "issue": "Check 4: the role of the strict filter is described in contradictory ways.",
      "evidence": "L36: 'The depletion is therefore not created by the filter'. L164: 'so the filtering step itself may shape the pattern'.",
      "suggested_fix": "Pick one reading. Since depleted cells pass the filter more often (38% vs 28%), filtering, if anything, attenuates depletion; say so in both places."
    },
    {
      "file": "en/appendix.tex; en/studies.tex",
      "location": "appendix L64 (B1) vs studies L255-283 (Table 5)",
      "issue": "Check 4: exploratory status is inconsistent.",
      "evidence": "B1: 'Three-test cells reported as exploratory'. Table 5 uses the three-test rule for the enriched rows and as corroboration for the depleted rows, with no 'exploratory' label.",
      "suggested_fix": "Label the three-test results as exploratory in Table 5 and its caption."
    },
    {
      "file": "en/studies.tex",
      "location": "L253",
      "issue": "Check 4: the provenance and chronology of the M06-P results are unclear.",
      "evidence": "Text: M06-P 'was itself frozen in Preregistration 3 (module P1) before it was computed'. Log E3.2 (L242, L257) lists the M06-P results under Preregistration 2, in V9_MATRIX_RESULTS.json and SUITE_P1_*_CELLS.csv.",
      "suggested_fix": "State which commit and file produced the M06-P counts. Confirm that they post-date d641256."
    },
    {
      "file": "en/appendix.tex",
      "location": "L62 (A2)",
      "issue": "Check 4: the rationale is inconsistent with the later analyses.",
      "evidence": "A2: 'H3 was not run: with H1 unsupported there is no hole to broker'. Plans 3-4 (P5, P6 and the firm null) and RQ2 then test firm brokerage anyway.",
      "suggested_fix": "Explain why firm-level brokerage remained a meaningful question after H1 failed (RQ2 is conceptually independent), and amend the A2 wording."
    },
    {
      "file": "en/studies.tex",
      "location": "L27",
      "issue": "Check 4: an imprecise cross-reference.",
      "evidence": "'we do not call depleted cells gaps (Section ref sec:design)' points to the whole of Section 3; the boundary is in Section 3.4 (sec:design_boundaries).",
      "suggested_fix": "Reference sec:design_boundaries. Also note that tab:app_v9cells, tab:app_s1robust and tab:app_sources are never referenced by number."
    },
    {
      "file": "en/main.tex",
      "location": "L15, L25-39, L35",
      "issue": "Check 5: compilation depends on the working directory.",
      "evidence": "input{abstract}, graphicspath{../figures/} and bibliography{../references} resolve only when compiling from en/. Compiling from paper/ fails to find the inputs.",
      "suggested_fix": "Document the build directory (or add a Makefile/latexmkrc), or use paths relative to paper/ with a top-level main."
    },
    {
      "file": "en/front.tex",
      "location": "L89 (Table 1)",
      "issue": "Check 5: overfull table.",
      "evidence": "The p-columns sum to 15.0 cm. Five inter-column gaps of 12 pt add about 2.1 cm, for about 17.1 cm against a 16.5 cm text width (letter, 1in margins). 'USER_REPORTED' cannot break inside the 1.9 cm Grade column.",
      "suggested_fix": "Reduce column widths or tabcolsep, use tabularx, or abbreviate the grade (HIST./USER, as in Table 2)."
    },
    {
      "file": "en/studies.tex; en/front.tex",
      "location": "all float environments",
      "issue": "Check 5: float-queue risk.",
      "evidence": "17 floats precede the clearpage. Most are [t]-only and full-width, including 8 in Section 5. This risks floats drifting to the end or 'Too many unprocessed floats'. Not compiled: pdflatex is unavailable in the review environment. No undefined references, no duplicate labels, balanced braces/environments, and all citation keys resolve (checked by script).",
      "suggested_fix": "Use [tbp] and add placeins/FloatBarrier at section ends."
    },
    {
      "file": "en/back.tex",
      "location": "L14",
      "issue": "Check 6: Burt (1992) is credited with a requirement that comes from Gould & Fernandez.",
      "evidence": "Text: 'directed dyadic flows between actors with externally assigned group labels, which is what Burt's construct requires [burt1992structural]'. Role note: non-redundant contacts; defines constraint. Direction plus group membership is the gould1989structures role note.",
      "suggested_fix": "Cite gould1989structures for direction and group labels; cite burt1992structural only for real ties and non-redundancy."
    },
    {
      "file": "en/appendix.tex",
      "location": "L262",
      "issue": "Check 6: the citations do not support the modelling restriction they are attached to.",
      "evidence": "colson2007overview and fortunyamat1981representation are cited for the bound H, EA, WI <= 3A ruling out oversight of an absent AI component. Role notes: a bilevel overview, and a KKT/complementarity reformulation.",
      "suggested_fix": "Remove the citations. The restriction is a design assumption of the prototype."
    },
    {
      "file": "en/studies.tex",
      "location": "L375",
      "issue": "Check 6: Nosek et al. is used beyond its role.",
      "evidence": "Role note: preregistration fixes the plan 'before observing outcomes'. Plan 4 was fixed after the P5 outcome was observed (appendix L42).",
      "suggested_fix": "Cite Nosek only for the confirmatory/exploratory distinction, and label the Plan 4 rationale as data-informed."
    },
    {
      "file": "en/studies.tex",
      "location": "L366",
      "issue": "Check 6: Burt is cited as support for this paper's empirical finding.",
      "evidence": "'mixed-portfolio firms show no brokerage advantage [burt1992structural, burt2004structural]'. The role notes cover the concept of brokerage benefits only.",
      "suggested_fix": "Move the citation to the definition of brokerage advantage (e.g. 'the brokerage advantage that Burt (1992, 2004) describes')."
    },
    {
      "file": "en/front.tex",
      "location": "L6",
      "issue": "Check 6: one citation is stretched, and the premise has no source.",
      "evidence": "burt2004structural is cited for 'information and control benefits'; its role note is 'better ideas; real ties and observed outcomes', while info/control benefits are in the burt1992structural role note. The claim 'a common explanation ... is structural' has no source in citation_map.json.",
      "suggested_fix": "Cite burt1992structural for information/control benefits. Add sources that assert the AI-decision separation premise, or reword it as the project's own working premise."
    }
  ]
}
```
