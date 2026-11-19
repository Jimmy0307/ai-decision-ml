THOUGHT:
<THOUGHT>
This is round 3. I read draft v5 in full: en/main.tex, abstract, front, studies, back and appendix. I also read:
- review_round2.md and REVISION_PLAN_round2.md;
- experimental_log.md, including the new block E3.5;
- the raw result file data/PLAN5_CONSTRUCT_RESULTS.json;
- the role notes in citation_map.json;
- figures 1, 4 and 5.

I ran scripts/audit_manuscript.py (AUDIT PASS: 6 files, 80 labels, 71 refs, 7 figures) and scripts/wordcount.py (main-text prose 11,498 words, against a cap of 11,500). I did not compile the paper, but the README now documents the build ('from paper/en, latexmk -pdf main.tex'). The widths of the new table tab:construct and of Tables A1 and A2 fit a 6.5in text width.

What changed, and whether it holds.

(1) Construct validity, the main technical weakness of round 2, has been addressed with the two requested analyses.
- Every number in Table tab:construct matches E3.5 and the JSON: P5a-P5d OE values and CIs, ratios, percentiles, Q1 values, medians, the 826/3,763 family counts, and 33,926 / 5,893 / 37,501 patents.
- The interpretation is scoped correctly. The text says 'a statement about these CPC constructs, not about decision-making as a whole' (studies L210; back L135, L165).
- The authors also report the substantive shifts, not only the verdict label: OE 3.05 -> 3.04; DEC-side percentile 92% -> 84%; reference median 1.095 -> 1.316/1.330.

Three problems remain.
(a) 'DEC06 = /06 only' is not 'DEC without /04'. By inclusion-exclusion on the logged counts, 33,926 + 5,893 - 37,501 = 2,318 patents carry both /04 and /06 codes. They remain in DEC06 (6.8% of it, and 39% of DEC04). The JSON confirms the definitions: BRIDGE is 4,585 under DEC06, against 5,316 under DEC. So P5a removes only the 3,575 /04-exclusive patents (9.5% of DEC), not 'the 5,893 /04 patents'. Several sentences overstate this: 'removes /04', 'without G06Q10/04' and 'a small share (5,893 of 37,501), so removing it barely changes OE'. P5d's OE 3.83 also includes the 2,318 dual-coded patents. A back-of-envelope from logged O and E values gives the /04-exclusive increment as about (30,843 - 28,877)/(10,112 - 9,507), roughly 3.2. This is approximate, because the AI-only set shifts with BRIDGE. The verdict will almost certainly survive, but the description is inaccurate.
(b) Granularity is matched on one side only. The references are now DEC-like subgroup families, but AI is still the whole G06N subclass (94,929 patents). On the DEC side the comparison is therefore OE(DEC, subclass) against OE(DEC, subgroup family). Under the paper's own argument that narrow groups show higher OE, this mismatch runs against over-connection, so the bias is conservative. It should still be said.
(c) The Plan 5 decision rule set a very low bar. ROBUST_TO_CONSTRUCT required only that all three specifications stay HOLE_NOT_SUPPORTED, while OE sits roughly 3.5-5 times above the lowest-quartile thresholds. The verdict was therefore close to certain before computation, and the information lies in the magnitudes, which the text does report. Also, P5b uses the primary DEC, so its H1b is identical to the primary run. 'All 6 sensitivity and 3 construct checks' therefore overstates the number of independent H1b checks.

(2) Plan 5 chronology. It is described honestly and consistently as data-informed:
- front L143-145: 'Plans 2-5 were each written after earlier results were known';
- studies L210: 'requested by review, is data-informed, but its rules were frozen before computation';
- Table A1: 'Known: the Plan 1-4 results';
- limitations L152.

The commit time (10:44:56) and the runtime in the JSON (892 s) are consistent with 'frozen before computation'.

Two presentation problems remain:
- The manuscript cites an unexplained 'round-2 review' (appendix L12, L49) and says 'requested by review' (front L143; studies L210). A journal reader will take this to mean the journal's own review.
- The abstract now advertises 'five preregistered analyses' without saying that only one is confirmatory. The fifth is a robustness check frozen minutes before it was run, so counting it as a preregistered analysis inflates the preregistration rhetoric that the body carefully deflates.
In addition, Figure 1 still says '4 preregistered analyses', and the caption patches this.

(3) RQ2 is now stated as unresolved everywhere: abstract, intro L16, studies L401 and L410, back L17-19, L147 and L167, and the Figure 1 box. Both residual metrics are reported (85/91% of the gap from parity; 0.67/0.78, a 33%/22% shortfall), and both match the log. This meets the round-2 request ('either run a null... or call RQ2 unresolved'). Substantively, though, the only organisation-level question in the paper remains open, although a degree-and-portfolio-preserving null is feasible on the existing data.

(4) Study 1. The self-pairing argument is now tied to the removal evidence, and the inflated cell is named only as 'prediction x prediction'. Good. One conflation remains. The '13/16 keep their direction without the 741 same-term records' comes from the rule-based keyword matrix, which also changes the coding instrument. Stage-1 keyword coding alone also gives 13/16. So the evidence does not isolate removal within the LLM-coded matrix. 'Self-pairing does not explain' the direction (conclusion L167) is stronger than the evidence.

(5) The Study 3 rival table now has discriminating signatures, as requested. But the new coding rule introduces a bias. Section 6.3 defines cost as 'expected value does not cover its cost' (an ROI rejection). Table 8 and Appendix C.7 instead define cost as 'integration cost exceeds the budget even after reallocation' (an affordability rejection), and code an episode as allocation whenever 'budget exists in aggregate but the leader has allocated it elsewhere'. A standard ROI-based rejection in a firm with aggregate budget would therefore be coded as organisational allocation. That is the candidate the model formalises.

(6) Unchanged from round 2, all acknowledged rather than fixed:
- the cell-level inference is uncalibrated (clustering, M06-P, the FDR of the core), and M06-P is still listed as a contribution;
- Section 7 is not shortened (about 1,500 words with two tables and a figure), and the main text is 2 words under its cap;
- the Level-3 constants are still only in the withheld canonical file.

(7) Positioning. Callon et al. (1983) and Swanson (1986) are now cited, within their role notes, and the unsourced 'gap research often...' claim is gone. The SNA results are explicitly conceded as known. This is honest, but it exposes the central problem for an IS journal.
- The cited practices map themes (co-word analysis) or generate hypotheses from non-co-occurrence (literature-based discovery). Neither infers a Burt structural hole.
- The inference the paper refutes is still documented only in this project.
- The empirical headline is that two CPC classes for data-processing methods cite each other more than expected. The authors themselves say this is not a measure of organisational integration.
- The firm-level result, the one finding with organisational content, is unresolved.

The paper is now technically careful, internally consistent and honest about its limits. What keeps it below the bar is the size of the contribution for a management/IS audience.

Scores. Soundness stays at 3: the central domain test is now well defended, but the cell-level inference is uncalibrated and RQ2 is untested. Significance and Contribution stay at 2. I do not raise the Overall score. The construct-validity work removes a soundness objection, but it does not change the size of the contribution, and that is what binds the decision.

The single most valuable change would turn the paper from a self-audit into a field-level contribution: show that the co-occurrence -> structural-hole/gap inference is an actual published practice. For example:
- assemble a small systematic set of IS/scientometric studies that compute structural holes, constraint or betweenness 'gaps' on co-word, co-citation or co-mention networks;
- classify them by the paper's four failure modes;
- re-run the diagnostic on one or two of their public datasets, or on the closest replicable analogue.

The degree-and-portfolio null for RQ2 and condensing Section 7 into a one-page outlook should come next.
</THOUGHT>

REVIEW JSON:
```json
{
  "Summary": "The paper (draft v5, 'Co-occurrence Is Not Flow') tests an inference the project itself had drawn: that sparse co-occurrence between AI functions and decision functions in an LLM-coded literature matrix indicates a Burt structural hole between AI and managerial decision-making. Study 1 shows that 16 depleted function pairs keep their direction across seeds, tracks and periods, and in a rule-based keyword matrix without same-term records, but lose significance under realistic misclassification; the direction is treated as descriptive and unconfirmed. A screen of six public relational sources finds none that is flow-valid. Study 2 uses US patents under five self-timestamped plans, of which only Plan 1 is confirmatory. AI (G06N) and DEC (G06Q10/04 + /06) cite each other at OE 3.05 (95% CI 2.94-3.17), so both relative hole criteria fail in all six sensitivity checks. A new, data-informed Plan 5 shows that the verdict also holds for DEC restricted to G06Q10/06 (OE 3.04) and against 826 granularity-matched subgroup-family references (percentiles about 84-90%). Cell-level depletions are modest and do not replicate across time halves. At the firm level, specialist AI and DEC firms are tied significantly less than a portfolio-preserving null implies (p = .001). Portfolios reproduce 85-91% of the gap from parity, but on the ratio scale ties are 0.67/0.78 of the null expectation. Whether mixed-portfolio firms broker the separation is explicitly left unresolved (verdict PARTIAL). The paper then lists five candidate explanations for weak AI-decision integration, formalises only the organisational one in a simulated tri-level programming model, and sets out a planned enterprise study (Study 3) to discriminate among them.",
  "Strengths": [
    "The construct-validity analyses requested in round 2 were run and are reported transparently (Table tab:construct; Section 5.1). Every number matches E3.5 and PLAN5_CONSTRUCT_RESULTS.json. The authors report the informative magnitudes (OE 3.05 -> 3.04; DEC-side percentile 92% -> 84%; reference median 1.095 -> 1.316/1.330) and scope the claim to 'these CPC constructs, not decision-making as a whole'.",
    "The chronology of the preregistrations is honest and identical across front Section 3.3, studies Section 5.1, Limitations Section 8.3 and Table A1. Plan 5 is labelled data-informed, written after Plans 1-4 were known, with rules frozen before computation, and Plan 1's rule unchanged. The commit time and the logged runtime are consistent with this.",
    "The answer to RQ2 is now calibrated. It is stated as unresolved in every section, reports both the gap-from-parity metric and the ratio metric (both in the log), and explains why neither available null can decide brokerage. PARTIAL is explicitly read as 'not confirmed, not ruled out'.",
    "The self-pairing threat in Study 1 is now weighed against the paper's own removal evidence. The inflated cell is named only as the log names it, and boundary (viii) is kept.",
    "Many small round-2 problems are fixed: the H2 rule is quoted and its reading for an over-connection explained; the O/E range is scoped; the heat-map note is reconciled with the counts; the 'capabilities unchanged' claim is removed; the F2 formula is printed; burt2004 is cited for real ties; the anonymity leaks are removed; \\eqref is used consistently; and Figure 1 shows the correct Study 2 -> Study 3 -> conditional-MLP logic.",
    "The positioning now cites co-word analysis and literature-based discovery within their role notes, and concedes that the SNA mechanisms (projection closure, two-mode brokerage, degree-driven constraint) are known. The contribution claimed is their consequence for gap inference, demonstrated end to end."
  ],
  "Weaknesses": [
    "The significance and positioning for a management/IS readership remain the binding problem (abstract S1-S2; front L8, L20; back L165-169). The cited practices map themes (Callon et al.) or generate link hypotheses from non-co-occurrence (Swanson). Neither infers a Burt structural hole or 'organisational separation' from co-occurrence. The inference the paper refutes is still documented only in this project's own pipeline, so the paper reads as a careful self-audit rather than a correction of field practice. The domain-level empirical result is that two CPC classes for data-processing methods cite each other about three times more than expected, and the authors rightly say this is not a measure of organisational integration. The firm-level result, the one finding with organisational content, is unresolved. The paper does not yet show what an IS reader learns about AI and organisational decision-making beyond 'do not infer holes from co-occurrence'.",
    "The construct checks are correct in their numbers but partly mis-described (studies L186, L210; back L17, L135, L165; front L16). (a) DEC06 is 'patents with a G06Q10/06 code'. By inclusion-exclusion on the logged counts (33,926 + 5,893 - 37,501), 2,318 of them also carry /04, and BRIDGE shrinks from 5,316 to 4,585. P5a therefore removes only the 3,575 /04-exclusive patents (9.5% of DEC). It does not test DEC 'without G06Q10/04', and the 5,893-of-37,501 argument uses the wrong subset. P5d's OE 3.83 includes the 2,318 dual-coded patents. (b) Granularity is matched only on the reference side. AI remains the whole G06N subclass (94,929 patents), so on the DEC side OE(DEC, subclass) is ranked against OE(DEC, subgroup family). By the paper's own logic this is conservative, but it should be stated. (c) The ROBUST_TO_CONSTRUCT rule (all three specifications not supported) was nearly certain to pass, given that OE is 3.5-5 times the Q1 thresholds. P5b's H1b is identical to the primary run, so 'all 6 sensitivity and 3 construct checks' (abstract) overstates the number of independent H1b checks.",
    "RQ2 is honestly unresolved but still untested (studies L377, L401, L410; back L147). This is the only organisation-level question in the paper, and a null that preserves both degree and portfolio is computationally modest on the existing files. Possible designs: owner permutation within degree-by-portfolio strata; a degree-preserving rewiring constrained to portfolio classes; or a comparison of degree-residualised constraint. Leaving it open makes the firm-level section mainly a demonstration that 'the choice of null determines the reading', which is the known Everett-Borgatti point.",
    "Inference for the cell-level analyses remains uncalibrated: clustering, M06-P and the FDR of the core (studies L30, L289; back L141-143). This is unchanged since round 1 and disclosed only. M06-P is still offered as Contribution 4 (front L20), with 'no separate type-I calibration' attached. A document-level permutation calibration of the exact, raw and M06-P tests on the existing files would let Table tab:cells_both and the P3 non-replication carry an error rate. Otherwise M06-P should be presented as a diagnostic, not a contribution.",
    "The Study 3 discriminant rule now biases coding toward the organisational candidate (back L33 vs L102, Table tab:back_study3_rivals; appendix L411). Section 6.3 defines cost as 'expected value does not cover its cost', a return-based rejection. Table 8 and Appendix C.7 define cost only as 'integration cost exceeds the budget even after reallocation', and code allocation whenever 'budget exists in aggregate but the leader has allocated it elsewhere'. An ordinary ROI rejection in a firm with aggregate budget is therefore coded as organisational allocation, the candidate the model formalises. The reversal observable in the table row ('proceeds after reallocation with no change in its business case') is the right discriminant, but the appendix coding rule does not require it.",
    "The MLP agenda was not condensed (back Section 7, about 1,500 words with Table 7, Figure 7 and Table 8; Plan item 17). The main text is 11,498 words against an 11,500 cap, so any new analysis will force cuts. The Level-3 constants (g_im, beta_m, autonomy_m, psi_i) are still only in a canonical file withheld for review, so Table 7 cannot be reproduced from the submission.",
    "The wording around Study 1's removal evidence is slightly stronger than the evidence (abstract; studies L95; back L24, L133, L167; appendix L94). '13/16 keep their direction without the 741 same-term records' comes from the rule-based keyword matrix, which also changes the coding instrument, and stage-1 keyword coding alone gives the same 13/16. The paper does not report what happens within the LLM-coded matrix when only the same-term records are removed. 'Self-pairing does not explain' the direction (conclusion L167) should read 'does not appear to be the main driver'.",
    "Presentation. The abstract now advertises 'five preregistered analyses' without saying that only one is confirmatory, while Figure 1 still says '4 preregistered analyses'. The Plan 5 specifications P5a-P5d collide with module P5 of Plan 3 (the caption has to disambiguate), and Table A1 adds a third scheme (CV1/CV2). The manuscript refers to an unexplained 'round-2 review'. Project-internal labels (V5-V11.1, P1-P10, M06/M06-P, S-tech, Gap Validity, Limitation Scout) still burden the main text."
  ],
  "Originality": 2,
  "Quality": 3,
  "Clarity": 3,
  "Significance": 2,
  "Questions": [
    "What is OE(AI, DEC) when DEC is restricted to patents with a /06 code and no /04 code (by the logged counts, 31,608 patents)? Can P5a's label be changed to '/06-coded' unless this is run?",
    "Can you cite published IS, management or scientometric studies that compute structural holes, constraint or betweenness 'gaps' on co-word, co-citation or co-mention networks and interpret them as separations between fields or communities? How many are there, and would your four failure modes change their conclusions?",
    "Is a degree-and-portfolio-preserving firm null feasible within the existing FIRM_NULL pipeline, for example by permuting owners within (type x year x firm-degree-bin) strata? If it is, what does T2 look like under it?",
    "On the DEC side of the granularity-matched H1a, AI is a subclass and the references are subgroup families. Would ranking OE(DEC, G06N main groups) against the same families change the DEC-side percentile?",
    "In Study 3, how will a return-based rejection in a firm with aggregate budget be coded: as cost or as allocation? Will allocation require the observed reversal without any change to the business case?",
    "Within the LLM-coded V9 matrix, how many of the 16 depleted cells keep their direction when only the same-term records are removed and the coding instrument is held fixed?",
    "Will the Level-3 constants and the canonical model file be supplied as anonymised supplementary material, so that Table 7 can be reproduced?"
  ],
  "Limitations": [
    "Study 2 measures class-level technological proximity. The /06-only check retains 2,318 /04-co-coded patents, and granularity is matched only on the reference side.",
    "Firm-level brokerage is untested, because no null holds both degree and portfolio fixed. The specialist residual is significant but unexplained.",
    "Cell-level tests (the Study 1 core; the Part A/B cores; M06-P) lack calibration under document clustering, and the core has no defined FDR.",
    "The Study 1 direction may reflect model-inferred labels, a non-random error source that is untested. Human reliability rests on n = 20.",
    "Only Plan 1 is confirmatory. Plans 2-5 are data-informed and self-timestamped, and Plan 5 was added after all other results were known.",
    "The MLP is simulated and uncalibrated, some of its constants are not in the text, and the Study 3 thresholds are deferred.",
    "The study covers US patents only, firm identities depend on assignee disambiguation, and the alias check covers 54 firms."
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
      "file": "en/studies.tex; en/back.tex; en/front.tex",
      "location": "studies L186 ('Plan 5 therefore removes /04'), L210 ('small share of DEC (5,893 of 37,501 patents), so removing it barely changes OE'); back L17, L135, L165 ('without G06Q10/04'); front L16",
      "issue": "Checks 2 and 3: the construct check is described as removing /04, but it retains the patents co-coded /04 and /06.",
      "evidence": "From log E3.1 and E3.5: DEC = 37,501, DEC06 = 33,926 and DEC04 = 5,893, so 2,318 patents carry both codes. PLAN5_CONSTRUCT_RESULTS.json: BRIDGE is 4,585 under DEC06 and 5,316 under DEC. P5a therefore drops only the 3,575 /04-exclusive patents (9.5% of DEC). The retained 2,318 are 6.8% of DEC06 and 39% of DEC04, and P5d's OE 3.83 includes them. A back-of-envelope estimate from logged O and E (P5b minus P5a) puts the OE of the dropped increment at about 3.2. It is approximate, because the AI-only set changes with BRIDGE.",
      "suggested_fix": "Describe P5a as 'DEC restricted to /06-coded patents (2,318 also carry /04)'. Replace 'removes /04' and 'without G06Q10/04' with 'restricted to G06Q10/06'. Replace the 5,893-of-37,501 argument with the correct subset, or add the overlap count to the log. Ideally, add a descriptive run with /06 excluding any /04 code."
    },
    {
      "file": "en/studies.tex",
      "location": "L204, L210; Table tab:construct caption",
      "issue": "Check 3: granularity is matched on one side only.",
      "evidence": "The references are now subgroup families 'built like DEC', but AI remains the G06N subclass (94,929 patents). The DEC-side percentile ranks OE(DEC, AI-subclass) against OE(DEC, family). By the paper's own argument (narrow groups show higher OE), this mismatch runs against over-connection, so it is conservative, but this is not stated.",
      "suggested_fix": "Add one sentence that AI is not granularity-matched and that the mismatch is conservative for the DEC-side percentile. Optionally report the DEC-side rank of the G06N main groups."
    },
    {
      "file": "en/abstract.tex; en/studies.tex",
      "location": "abstract S5 ('all 6 sensitivity and 3 construct checks'); studies L210; Table A1 Plan 5 rule",
      "issue": "Check 3: independence of checks and informativeness of the decision rule.",
      "evidence": "P5b uses the primary DEC, so its H1b ratio is identical to the primary run: 1.69 (1.60-1.77). Only P5a and P5c vary H1b, and they are identical to each other (1.68). ROBUST_TO_CONSTRUCT required only that all three stay HOLE_NOT_SUPPORTED, while OE 3.04-3.05 is about 3.5-5 times the Q1 thresholds (0.511-0.875), so the label was almost certain in advance.",
      "suggested_fix": "Write 'H1a fails in three construct checks; H1b in the two that change DEC'. Say in one clause that the label was near-certain and that the informative result is the size of the shifts (percentiles 92% -> 84%; median 1.095 -> 1.33)."
    },
    {
      "file": "en/abstract.tex; figures/fig_research_design.png; en/front.tex",
      "location": "abstract S5 ('five preregistered analyses'); Figure 1 Study 2 box ('4 preregistered analyses'); Figure 1 caption",
      "issue": "Check 4: the count of plans is inconsistent, and the abstract inflates the preregistration rhetoric.",
      "evidence": "The figure still says 4 while the text says 5, and the caption patches this ('four preregistered analyses plus preregistered construct checks'). The abstract does not say that only Plan 1 is confirmatory. Plan 5 is a post-review robustness check frozen minutes before it was run (commit 10:44:56; runtime 892 s).",
      "suggested_fix": "Regenerate Figure 1 with '1 confirmatory + 4 data-informed plans'. In the abstract, write 'one confirmatory and four data-informed preregistered analyses'."
    },
    {
      "file": "en/appendix.tex; en/front.tex; en/studies.tex",
      "location": "appendix L12, L49 ('requested by the round-2 review'); front L143; studies L210 ('requested by review')",
      "issue": "Check 4: reference to an unexplained review process.",
      "evidence": "A journal reader will take 'requested by review' to mean this journal's review. The 'round-2 review' is internal and undocumented in the submission.",
      "suggested_fix": "Write 'added after a pre-submission review raised the construct-validity question'. Keep the 'data-informed' label."
    },
    {
      "file": "en/abstract.tex; en/studies.tex; en/back.tex; en/appendix.tex",
      "location": "abstract S4 ('13 keep it without same-term records'); studies L95; back L24, L133, L167 ('which self-pairing does not explain'); appendix L94 (Table tab:app_v9cells caption)",
      "issue": "Checks 2 and 3: the evidence for removing same-term records is confounded with a change of coding instrument.",
      "evidence": "Log E1.3: the 13/16 figure comes from the rule-based keyword matrix (741 same-term records removed, 1,431 edges), which also replaces LLM coding with keyword coding. Stage-1 keyword coding alone also gives 13/16. Within the LLM matrix the log reports only that removal 'drops 2 prediction-related depleted cells from the core', which concerns significance, not direction.",
      "suggested_fix": "Write 'in a rule-based keyword matrix that also excludes the 741 same-term records, 13/16 keep their direction'. In the conclusion, change 'does not explain' to 'does not appear to be the main driver of'."
    },
    {
      "file": "en/back.tex; en/appendix.tex",
      "location": "back L33 (candidate 3, Cost), L102, Table tab:back_study3_rivals; appendix L411",
      "issue": "Check 3: the definition of cost is inconsistent, and the coding rule favours the organisational candidate.",
      "evidence": "Section 6.3: cost means 'expected value does not cover its cost', a return-based rejection. Table 8 and App. C.7: cost means 'integration cost exceeds the budget even after reallocation', and allocation is coded whenever 'budget exists in aggregate but the leader has allocated it elsewhere'. A return-based rejection in a firm with aggregate budget is therefore coded as allocation.",
      "suggested_fix": "Code cost whenever the rejection cites a return or hurdle threshold, whatever the aggregate budget. Code allocation only when the episode is reversed by reallocation or a rule change with no change to its business case, or when the rejection cites priority or decision rights. Align Section 6.3 with this."
    },
    {
      "file": "en/back.tex",
      "location": "Section 7 (L38-124); scripts/wordcount.py",
      "issue": "Plan item 17 is not implemented, and there is no headroom left for revisions.",
      "evidence": "Section 7 is still a full main-text section of about 1,500 words with two tables and a figure. Main-text prose is 11,498 words against the 11,500 cap.",
      "suggested_fix": "Move the simulated illustration (Table 7, Figure 7, the probes) to Appendix C. Keep a one-page outlook with the rival table."
    },
    {
      "file": "en/appendix.tex",
      "location": "L353 (Level-3 constants)",
      "issue": "Check 4: the paper cannot be reproduced from the submission.",
      "evidence": "g_im, beta_m, autonomy_m and psi_i 'are given in the canonical model file', which is withheld for review. Table 7 cannot be reproduced from the text and appendix alone.",
      "suggested_fix": "Print these constants in a small table in Appendix C (SIMULATED), or supply the canonical file as anonymised supplementary material."
    },
    {
      "file": "en/front.tex; en/studies.tex; en/appendix.tex; raw_materials/experimental_log.md",
      "location": "front L147 and studies L28 ('plus raw q <= .05 in the same direction'); Table A1 Plan 2 rule ('plus raw'); log E1.1 ('plus raw')",
      "issue": "Check 4: the core rule is worded differently in different places (minor).",
      "evidence": "The main text requires the raw test to agree in direction, while the frozen-rule quotation in Table A1 and the log do not mention direction.",
      "suggested_fix": "Confirm the rule against the V9 engine and use the same wording in all three places, adding it to the log."
    },
    {
      "file": "raw_materials/experimental_log.md; en/appendix.tex",
      "location": "Table A1 (H2 rule; Plan 5 ROBUST/CONSTRUCT_SENSITIVE rule)",
      "issue": "Check 1: decision rules quoted in the paper are absent from the ground-truth log (minor).",
      "evidence": "E3.1 records only the label PERSISTENT, not the rule 'CI includes 0 or lies below 0'. E3.5 records the construct verdict but not its rule. The appendix says it quotes these from the frozen texts.",
      "suggested_fix": "Add both rules verbatim to E3.1 and E3.5, so that every claim in the paper is traceable to the log."
    },
    {
      "file": "en/front.tex; en/back.tex",
      "location": "front L20 (Contribution 4); back L26",
      "issue": "Check 3, carried over: a null model without calibration is offered as a contribution.",
      "evidence": "M06-P 'has no separate type-I calibration' (front L20; back L142), and the portfolio null does not hold degree fixed. Both are listed as contributions.",
      "suggested_fix": "Either calibrate M06-P on document-level permutations, or present both nulls as diagnostics with stated limits rather than as contributions."
    },
    {
      "file": "en/studies.tex; en/appendix.tex",
      "location": "Table tab:construct (P5a-P5d); Table A1 (CV1/CV2); module P5 throughout",
      "issue": "Presentation: labels collide.",
      "evidence": "'P5' denotes both the firm-network module of Plan 3 and the Plan 5 specifications. Table A1 adds a third scheme (CV1/CV2), and the caption has to disambiguate.",
      "suggested_fix": "Rename the Plan 5 specifications (for example C1-C4) and use the same names in Table A1."
    },
    {
      "file": "en/main.tex; en/*.tex",
      "location": "whole manuscript (check 5)",
      "issue": "LaTeX: no breaking problems found.",
      "evidence": "audit_manuscript.py: AUDIT PASS (80 labels, 71 references, 7 figures, all citation keys resolve). The new tables fit a 6.5in text width: tab:construct about 15.2 cm; Table A1 about 16.2 cm. The README documents the build from en/. Not compiled here.",
      "suggested_fix": "None required. Optionally add a top-level latexmkrc so the build does not depend on the working directory."
    }
  ],
  "Round2_Resolution": [
    {
      "weakness": "1. Construct validity of Study 2 conceded but not tested (/06-only; granularity-matched H1a)",
      "status": "resolved",
      "evidence": "Plan 5 (Table tab:construct; studies L210; back L135) runs both analyses. Numbers match E3.5 and the JSON (P5a 3.04; P5b/P5c percentiles 89.8/84.1 and 89.6/83.5; medians 1.419/1.316 and 1.419/1.330), and the claim is scoped to the CPC constructs. New, minor issues: '/06 only' retains 2,318 /04-co-coded patents, so 'without /04' is inaccurate; granularity is matched on the reference side only; the H1b check count is overstated (Integrity Findings 1-3)."
    },
    {
      "weakness": "2. Firm-level conclusion stronger than T2 can bear; 'small' depends on the scale",
      "status": "resolved",
      "evidence": "RQ2 is 'unresolved' in the abstract, front L16, studies L401/L410, back L17-19/L147/L167 and the Figure 1 box. Both metrics are reported (85/91% of the gap; 0.67/0.78, a 33/22% shortfall), matching log E3.4, and PARTIAL is read as 'not confirmed, not ruled out'. This meets the review's 'or call RQ2 unresolved' option. A null preserving both degree and portfolio was not run, which remains a substantive limitation."
    },
    {
      "weakness": "3. Cell-level inference uncalibrated (clustering, M06-P, FDR of the core)",
      "status": "unresolved",
      "evidence": "Disclosed again (studies L30, L289; back L141-143), but there is no document-level permutation calibration and no type-I rate for M06-P. M06-P is still Contribution 4 (front L20), now qualified with 'no separate type-I calibration'."
    },
    {
      "weakness": "4. Positioning and significance for an IS readership; uncited 'gap research often...'",
      "status": "partially",
      "evidence": "The unsourced claim is removed. Callon et al. (1983) and Swanson (1986) anchor co-occurrence-based structure reading within their role notes (front L8; back L165), and the SNA results are conceded as known (front L20; back L24). Still, no published study is shown to infer structural holes or separation from co-occurrence, so the refuted inference remains the project's own, and the significance for IS is unchanged."
    },
    {
      "weakness": "5. MLP agenda out of proportion and partly unreproducible (F2 withheld; thresholds deferred; cost/allocation overlap; Figure 1 logic)",
      "status": "partially",
      "evidence": "Fixed: Figure 1 now shows Study 2 -> 'which constraint binds?' -> Study 3 -> MLP (dashed, 'only if supported'); F2 and its components are printed (Eq. app_f2); the signatures in Table 8 are discriminant. Not fixed: Section 7 is not shortened (about 1,500 words); the Level-3 constants are still withheld; the thresholds are deferred to Study 3's own preregistration. New: the coding rule codes ROI rejections as allocation."
    },
    {
      "weakness": "6. Study 1 non-random-error argument not connected to the removal evidence",
      "status": "resolved",
      "evidence": "Studies L95, back L24/L133 and appendix L82/L94 now state that 13/16 keep direction and only 2 drop from the core, so self-pairing is not the main driver, while model-inferred labels remain untested. The inflated cell is named only as 'prediction x prediction'. Residual: the 13/16 comes from a matrix that also changes the coding instrument (Integrity Finding 6)."
    }
  ],
  "Plan2_Items": [
    {"item": "1. RQ2 / firm level becomes UNRESOLVED everywhere", "status": "resolved", "evidence": "Abstract; front L16; studies L401, L410; back L17-19, L147; conclusion L167; Figure 1 'Firm: unresolved (PARTIAL)'. Both scales are reported, and the degree-matched P5 result and the absence of a joint null are stated."},
    {"item": "2. Positioning: ground in co-word / LBD; remove 'gap research often'; concede known SNA results", "status": "resolved", "evidence": "front L8, L20; back L24, L165. Citations are used within their role notes. The underlying significance concern remains (Weakness 1)."},
    {"item": "3. State plainly that construct validity is untested; list /06-only and matched references as future work", "status": "resolved", "evidence": "Superseded: both analyses were run (Plan 5, Table tab:construct), and s2 is described as 'dilutes the overlap rather than isolating it' (studies L186). The '/06 only' wording needs correcting (Integrity Finding 1)."},
    {"item": "4. 'Ruling out' -> 'not supporting'", "status": "resolved", "evidence": "No 'ruling out' remains. The abstract reads 'Failing to find a knowledge-flow hole does not establish...', and 'not a proof that no separation exists' is kept (studies L271)."},
    {"item": "5. Study 1 self-pairing connected to the removal evidence", "status": "resolved", "evidence": "studies L95; back L24, L133; appendix L82, L94. The inflated cell is named only as 'prediction x prediction'. Minor conflation of instrument and removal (Integrity Finding 6)."},
    {"item": "6. O/E 0.70-0.95 scoped to the five both-part cells; the 0.51 cell described qualitatively", "status": "resolved", "evidence": "studies L328: 'one further Part-B core cell lies below it'. No number outside the log is used."},
    {"item": "7. State the H2 rule", "status": "resolved", "evidence": "studies L262; Figure 4 caption; Table A1 Plan 1. The rule is quoted from the frozen text, but it is not in the log (Integrity Finding 11)."},
    {"item": "8. Wording of the core rule", "status": "resolved", "evidence": "front L147 and studies L28 now give main + exact + document-preserving (M06-P in the adapted core) plus raw. Minor mismatch with the Table A1/log wording of the raw direction (Integrity Finding 10)."},
    {"item": "9. 'The AI-decision pairs' -> 'the 16 depleted pairs'", "status": "resolved", "evidence": "studies L163."},
    {"item": "10. Heat-map note on small-sample cells", "status": "resolved", "evidence": "Figure 5 footnote and caption: 'shown, marked and counted, but not interpreted'. The marker counts match (A 8/7; B 9/8)."},
    {"item": "11. Remove 'capabilities unchanged'; Level 1 re-optimises", "status": "resolved", "evidence": "back L95 and L157."},
    {"item": "12. Print F2 and its components", "status": "resolved", "evidence": "appendix Eq. app_f2 and its components match log E4. The Level-3 constants are still only in the canonical file (Integrity Finding 9)."},
    {"item": "13. Discriminant signatures for cost vs allocation", "status": "partially", "evidence": "Table 8, back L102 and appendix L411 now separate them by aggregate budget and a reversal observable. However, cost is defined differently in Section 6.3 (return-based) and Table 8 (budget-exceeding), and the coding rule assigns return-based rejections to allocation (Integrity Finding 7)."},
    {"item": "14. Cite burt2004 for real ties", "status": "resolved", "evidence": "front L30, L43."},
    {"item": "15. Anonymity (thesis mention; PR #5; repository naming)", "status": "resolved", "evidence": "There are no hits for 'thesis' or 'PR #', and identifiers are 'withheld for review'. A new minor issue is the reference to the 'round-2 review' (Integrity Finding 5)."},
    {"item": "16. Use \\eqref consistently", "status": "resolved", "evidence": "There are no remaining 'Eq.~\\ref' uses, and appendix L353 and L357 use \\eqref."},
    {"item": "17. Shorten Section 7", "status": "unresolved", "evidence": "Section 7 still has the full model summary, Table 7, Figure 7, the probes and Table 8 (about 1,500 words). Main text 11,498 / 11,500 words."}
  ]
}
```
