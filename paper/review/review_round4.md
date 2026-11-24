THOUGHT:
<THOUGHT>
This is round 4. I read draft v7 in full: en/main.tex, abstract, front, studies, back and appendix. I also read:
- review_round3.md and REVISION_PLAN_round3.md;
- experimental_log.md, especially the new blocks E3.6 (Plan C), E3.7 (Plan 6), E5 (review) and E5.1 (R1);
- the raw files PLAN_C_RESULTS.json, PLAN6_RESULTS.json, review_results.json, coding_agreement.json, screening_flow.json, screening_agreement.json, search_log.json, included_studies_coded.csv, R1_D1D2.json and the four R1_D3_*.json;
- PROTOCOL.md, PREREGISTRATION_OPSAHL.md and R1_CLAIM_RECORD.md;
- from the research branch: PLAN_C_DESCRIPTIVE.md, PREREGISTRATION_FIRM_NULL_DEGREE.md and PLAN6_SMOKE_NOTE_20261119.md;
- the git history of the freezes (Plan C 15:01:48, results 15:03:43; Plan 6 frozen 15:21:56, smoke 15:25:32, results 15:49:45; review protocol 13:41:45, S1 14:00:10, results 14:25:45; R1 prereg 15:13:47, step 0 and R1-A1 15:19:05);
- figures fig_plan_c_locus.png and fig_research_design.png.

Checks run:
- audit_manuscript.py: AUDIT PASS (6 files, 93 labels, 82 refs, 8 figures).
- wordcount.py: abstract 198 (cap 200); main-text prose 11,999 words (cap 12,000). The count excludes tables, figures and captions, and the script still labels the total "Sections 1-9" although the conclusion is now Section 10.

Number verification. I checked every number in the new or changed text against the log and the JSON files:
- Plan C: 127,114 / 162,339; 2.9% -> 4.6%; 10.8% -> 14.4%; 22,796; 64.2% vs 48.2%; 18.6% vs 29.1%; 84.8% vs 74.1%; 13 firms, 42.8%; 1.331 / 0.695 / 0.701.
- Plan 6: rho 0.817 / 0.825; gate 0.90.
- Review:
  - 594 / 476 / 204 and 131 / 31 / 25 / 17; 135; 111; 10;
  - all Table tab:review shares and Wilson intervals; all kappas and raw agreements;
  - 119 / 0.361 / 0.681 / 38 / 243 / 254 / 26; 182;
  - final-code counts, period counts, unclear counts; 63 of 91; 165 of 204; 178 of 204; 0 of 73; 1 of 73; 70 / 72 / 63; 28 / 2.
- R1: 99.9%; 0.681 / 0.0077; all four D3 rows; p >= .653; 1,421 / 513 / 55; the 2002 S3 p = .005.
- Plan 5 (C-a to C-f), unchanged from round 3: correct.

I found **no numeric mismatch** between the manuscript and the log or JSON files. Two near-mismatches in wording:
- back L24 "about three in four structural-hole studies read Burt measures on projected networks as brokerage". The logged ratio for the 135 claims is F2 96/135 = 0.71 (F1 99/135 = 0.73); "three in four" fits only stream S (0.748 / 0.733).
- studies L419 "74.1% of patent ownership". The log defines this as the share of patent-owner pairs.

The log itself has stale lines:
- E5 (log L621) still says "Optional replication (protocol §8): not done in this round", although E5.1 reports it.
- The E3 header (log L162) still says "four preregistrations".

What changed and whether it holds.

(1) Significance, the binding issue of round 3. The authors did what round 3 asked for:
- a preregistered systematic review, classified by the failure modes;
- a re-analysis of one public dataset;
- a checklist.

This is a real change. The refuted inference is no longer documented only in the project's own pipeline. 46 of 66 gap claims read sparse co-occurrence as a gap with no baseline reported, and 96 of 135 hole or broker claims compute Burt measures or betweenness on a co-occurrence or affiliation network. R1 shows on open data that a betweenness and constraint reading of a projected affiliation network is reproduced by seat counts and board sizes alone. Significance moves from 2 to 3. Three limits remain.

- (a) The review's headline count is largely a different practice. The 135 hole or broker claims come almost entirely from stream S (131), and stream S is dominated by the query "structural hole" + patent (165 of 308 hits). 73 of the 135 claims are patent co-inventor, co-applicant or co-classification networks, and 63 of the 91 V = yes codes in S are patent-network studies relating an ego-level Burt score to later innovation outcomes. That is not the inference the project drew, which was a domain-level hole read from sparse label co-occurrence. Co-inventorship also records joint work, which most of that literature treats as a collaboration tie. The paper's critique (projection closure, constraint dominated by affiliation) bears on these studies as a measurement bias, not as an invalid inference. The text half-concedes this ("Two practices emerge", L465), but the abstract, the intro (L20), back L24 and the conclusion (L179) pool them as "the inference" or "the same inference".
- (b) Every screening, coding and adjudication decision was made by LLM agents of one model family (Claude, per log E5; the manuscript does not name it). The key gap indicator F3 has kappa 0.192, V 0.312 and screening 0.361. The paper's own Study 1 lesson, and its own Study 3 rule (appendix L456: "given Study 1, model-assisted coding will not substitute for [human coders]"), argue against resting a prevalence claim on LLM-only coding. A spot-check of included_studies_coded.csv also shows doubtful inclusions: a G3 study on humanism in clinical education with D2 "unclear"; a Zenodo item; preprints; 11 Academy of Management Proceedings abstracts. The abstract nevertheless calls the 204 "published studies".
- (c) R1 tests a reading that, by the authors' own step-0 record, the article does not make. The full text was not accessed, and the "broker" reading comes from uncited secondary literature. The case also lies outside the coded set. R1 is therefore a clean demonstration of the projection mechanism, not a correction of a published conclusion. The main text handles this better than it could have ("This concerns the brokerage reading later work gave the network, not the study's claims about prominence"). But it omits that the full text was not accessed, and it does not cite the "later work".

(2) Plan C (exploratory locus). The numbers are correct, and the section body mostly follows the frozen wording rules:
- co-classification is called co-occurrence;
- the within-firm share is explicitly "not evidence of a boundary inside firms".

But the claims have drifted where they are summarised:
- "The connection is growing" (studies L417; conclusion L175) rests on raw shares of in-scope citations. Yet the time-stratified OE of the same pair fell from 3.90 (2013) to 2.34 (2025), with a slope CI below 0. The BRIDGE share in the figure peaks at 5.1% in 2023 and falls to 4.1% in 2025. The Plan C preregistration itself (item C5) puts the yearly OE range and H2 slope next to C1/C2; the manuscript does not.
- "runs ... through firms that hold both kinds of patent" (front L20; studies L419; back L175) uses "through", which implies intermediation, the very brokerage question RQ2 leaves unresolved. The datum is that a MIXED firm is the citing party.
- The 64.2% vs 48.2% contrast has exactly the mechanical explanation the paper used to motivate Plan 4: MIXED firms own both kinds of patent and 74.1% of patent-owner pairs. Yet the "no portfolio baseline" caveat (L423) is attached only to the within-firm share.
- "a few firms" (front L20; back L175) has no baseline: no concentration figure is given for all citations. MIXED firms are 2,445 of 14,600 firms, not a few.
- Contribution 3 ("describes where the connection runs instead") turns an exploratory description into a contribution.

(3) Plan 6 is described correctly as INVALID_NULL and is not interpreted (studies L410; Table A1 row 6; back L41, L152). However, its own preregistration (§3) requires that, if the gate fails, "its T1/T2 p-values are reported as descriptive only". It also lists "also reported" quantities: the singleton-stratum share and the share of firms within ±20% of observed degree. None of these appears in the manuscript. This is a deviation from a preregistered reporting rule in a paper whose main asset is preregistration discipline. It also matters: under the (invalid) S-tech Plan 6 null, the T1 null median is 0.249, p = .236, and the null reproduces 98.7% of the gap. The values must be reported, labelled descriptive, without interpretation. The limitations should then say that T1, not only T2, is untested under a degree-holding null. Currently back L152 restricts the degree problem to T2, while the abstract and conclusion present the T1 separation as a result. The 2-replicate smoke test, which showed the gate failing before the full run (with T1/T2 sealed), should also be disclosed in one clause.

(4) Disclosure of LLM coding. It is disclosed in studies L438 and limitations L162 ("LLM agents did all screening and coding"). The model family is not named, and it should be. Abstract-level exposure is stated in the Table tab:review caption, L469 and L162. It is not stated in the abstract ("most gap claims lack a baseline"), intro L20, back L24, the checklist (rows 6, 8) or the conclusion L179. "Lack a baseline" should be "report no baseline in the abstract".

(5) Internal consistency after many edits. Several statements are now stale.
- "Five" plans or analyses: abstract L1; front L79 (Fig. 1 caption), L114, L142; studies L170; back L157; appendix L12 ("rests on five preregistration plans ... summarises the five plans"). Yet Table A1 has seven rows (Plans 1-5, C, 6), and the review protocol and the R1 preregistration are further frozen plans.
- front L146 lists amendments and Plan C but omits Plan 6, S1 and R1-A1.
- Checklist row 9 (back L46) lists "Plans 1-5, Plan C and amendments A1-C1", omitting Plan 6, the review protocol, S1, R1 and R1-A1.
- Checklist row 7 (back L44) reintroduces the round-3 conflation: "13 of 16 depleted cells keep their direction without same-term records", with no mention that the keyword matrix also changes the coding instrument.
- Figure 1 and the study overview table (front L89-129) do not show the systematic review or R1, although the review is now Contribution 1's main evidence and Section 6 of the paper.
- "Five contributions" (front L20) is internally consistent: five are listed.

(6) Layout. The new Plan C and Plan 6 rows make Table A1 (appendix L14-67, a single float in \footnotesize with five p-columns) very tall. My estimate from the cell lengths is about 75-80 text lines, about 900 pt, against a 9 in (about 650 pt) text height. It will almost certainly overflow the page, since floats cannot break. Table A2 (L69-94) is about 60 lines and borderline. Widths are fine: tab:construct about 15.7 cm; tab:checklist about 0.99\linewidth; Table A1 about 16.2 cm; Table A2 about 16.0 cm; tab:back_study3_rivals about 15.5 cm (text width 16.5 cm). Main-text prose is 1 word under the 12,000 cap, and it excludes the new checklist and review tables and the captions. Every required change below needs offsetting cuts.

(7) Round-3 items. Most are resolved:
- C-a to C-f renaming;
- strict /06 (C-e/C-f, OE 3.16) leading;
- one-sided granularity;
- non-independence;
- "round-2 review" removed (only "round-3 sample" for OCDS, appendix L249, remains);
- cost defined by return, with allocation requiring positive evidence;
- Level-3 constants printed;
- core-rule wording;
- Section 7 condensed.

The 11,200-word target of the round-3 plan is not met (11,999), because new material was added.

Overall judgement. The paper has moved from a careful self-audit to a self-audit plus a field-level prevalence scan, and that addresses the round-3 binding concern in part. What still limits the contribution:
- The field-level evidence is abstract-level, LLM-coded and low in reliability on the key gap indicator, and its headline count is dominated by a related but different practice (ego-level Burt scores on co-inventor networks).
- The only re-analysis does not touch any coded study's conclusion.
- The substantive AI-decision content is a negative domain result on two CPC classes plus an exploratory description.
- The one organisation-level question (RQ2) is still unresolved, and Plan 6 failed.
- The manuscript is now very broad: Study 1, an external screen, seven patent plans, a review, R1, an MLP agenda and a Study 3 plan, in 11,999 words with no headroom.

The new claim-discipline lapses (Plan C summary wording; Plan 6 reporting) are fixable but real.

Scores:
- Significance and Contribution rise from 2 to 3.
- Presentation drops to 2: stale counts, Figure 1 and the overview table missing the review, Table A1 overflow, zero word headroom.
- Soundness stays at 3.

I keep Overall at 5, with a clear path to 6-7 if Required Changes R1-R8 are made, in particular a human validation subsample for the review and the Plan 6 descriptive reporting.
</THOUGHT>

REVIEW JSON:
```json
{
  "Summary": "The paper (draft v7, 'Co-occurrence Is Not Flow') tests an inference the project itself drew: that sparse co-occurrence of AI and decision functions in an LLM-coded literature matrix indicates a Burt structural hole between AI and managerial decision-making. Study 1 finds that 16 depleted pairs keep their direction but lose significance under realistic misclassification. Study 2 (8,512,829 US patents) finds AI (G06N) and DEC (G06Q10/04+/06) over-connected: OE 3.05, and OE 3.16 with every /04-coded patent removed. The relative hole criteria fail in every sensitivity and construct check. At the firm level, specialist firms are separated beyond a portfolio-preserving null (p = .001), but brokerage by mixed firms is unresolved. A new degree-stratified null (Plan 6) failed its validity gate (INVALID_NULL). New since round 3: (i) an exploratory, preregistered description of where AI-DEC citations occur (Plan C); (ii) a preregistered, LLM-coded, abstract-level systematic review of 204 studies, in which 135 draw structural-hole or broker claims from co-occurrence or affiliation networks (mostly patent co-inventor networks) and 46 of 66 gap claims report no baseline; (iii) a preregistered re-analysis of the open Norwegian boards data (R1), in which projection triangles lie 99.9% within boards and betweenness and constraint readings are reproduced by an affiliation-preserving null; (iv) a nine-item checklist for hole, broker and gap claims. The MLP section is condensed and remains a simulated agenda, with Study 3 as a plan.",
  "Strengths": [
    "The round-3 binding request was taken seriously and executed under a frozen protocol. Search, eligibility, coding scheme, reading rule, an amendment (S1) recorded before coding, and reliability statistics are all reported, including unflattering ones (screening kappa 0.361; F3 0.192; V 0.312). Every review number in the manuscript matches review_results.json, coding_agreement.json and screening_flow.json.",
    "The review separates the two practices it finds (studies L465): Burt measures on projected networks used as predictors (stream S), and absence read as a gap without a baseline (the G streams). It notes that V in stream S mostly records prediction of outcomes, not flow. That is a careful and correct reading.",
    "R1 is cleanly preregistered. Step 0 recorded the article's claims before any download, and R1-A1 added the article's own snapshot before any download. The confirmatory label is reported (BROKERAGE_READING_EXPLAINED), and the main text limits the result to 'the brokerage reading later work gave the network, not the study's claims about prominence'. All D1-D3 numbers match the JSON files.",
    "Plan 6 is reported as INVALID_NULL in all three places it appears, and its tests are not interpreted (studies L410; Table A1 row 6; back L41, L152).",
    "The body of the Plan C section respects two of the frozen wording rules: co-classification is called co-occurrence, not flow (L417; figure title), and the within-firm share is 'not evidence of a boundary inside firms' (L423).",
    "Round-3 corrections are implemented: C-a to C-f naming; the strict /06 result (OE 3.16) leading; one-sided granularity and non-independence stated; references to the internal review process removed; cost defined by return, with allocation requiring positive evidence; Level-3 constants printed (Tables A-configs, A-processes); Section 7 condensed.",
    "No numeric mismatch was found between the manuscript and the log or JSON files in any new or changed passage."
  ],
  "Weaknesses_Major": [
    "M1. Plan 6 reporting deviates from its preregistration. PREREGISTRATION_FIRM_NULL_DEGREE.md §3: if the gate fails, 'its T1/T2 p-values are reported as descriptive only', and the singleton-stratum share and ±20% degree share are 'also reported'. The manuscript reports none of these (studies L410; appendix L60-64). The omitted values bear on a headline: under the S-tech Plan 6 null, the T1 null median is 0.249 [0.224-0.273], p = .236, with 98.7% of the gap reproduced (primary: 0.315, p = .001). Not interpreting them is correct; not reporting them is not. Relatedly, back L152 treats degree only as a problem for T2, but T1 has not been tested under a valid degree-holding null either.",
    "M2. The Plan C summary claims exceed the descriptions. (a) 'The connection is growing' (studies L417; conclusion back L175) rests on raw shares, while the time-stratified OE of the same pair declined from 3.90 to 2.34 (slope CI below 0), and the BRIDGE share fell from 5.1% (2023) to 4.1% (2025). The frozen Plan C item C5 pairs these, and the manuscript does not. (b) 'runs ... through firms that hold both kinds of patent' (front L20; studies L419; back L175): 'through' implies intermediation, the unresolved RQ2. The datum is only that a MIXED firm is the citing party. (c) The 64.2% vs 48.2% MIXED-citing contrast has the same portfolio-mechanical explanation that motivated Plan 4, but the 'no baseline' caveat (L423) covers only the within-firm share. (d) 'a few firms' (front L20; back L175) has no concentration baseline. (e) Contribution 3 presents an exploratory, test-free description as a contribution.",
    "M3. The review's headline prevalence pools a different practice with the inference under test. The project inferred a domain-level hole from sparse label co-occurrence. Of the 135 hole or broker claims, 131 are in stream S, which is dominated by the query 'structural hole' + patent (165 of 308 hits). 73 of the 135 are patent co-inventor, co-applicant or co-classification networks, which use ego-level Burt scores as predictors of innovation, on ties that record joint work. For these studies, the paper's mechanisms (projection closure; constraint driven by affiliation) are a measurement bias, not an invalid inference. The abstract (L1: 'finds the inference common'), intro L20, back L24 ('about three in four structural-hole studies...'; logged 96/135 = 0.71) and conclusion L179 ('the same inference in 135 of 204') overstate the match. The closest analogue to the project's inference is the gap practice (46 of 66 gap claims; F3).",
    "M4. The review rests solely on LLM coding, which contradicts the paper's own lesson. The coders, screeners and adjudicator were all LLM agents of one model family (Claude, log E5; not named in the manuscript). Reliability is low exactly where the paper's main claims sit: F3 kappa 0.192, V 0.312, screening 0.361, and 182 of 204 studies needed adjudication. Appendix L456 says of Study 3 that 'given Study 1, model-assisted coding will not substitute for' human coding. The included set contains doubtful items: a G3 clinical-education study with D2 unclear; a Zenodo item; preprints; 11 Academy of Management Proceedings abstracts. Without a human-validated subsample, the prevalence figures are model outputs at the abstract level, and 'published studies' overstates the set.",
    "M5. R1's handling of the original article is only partly in the main text. That the full text was not accessed, and that the article's measures are reconstructed from the abstract, a blog post and secondary summaries, appears only in appendix L517. The main text (studies L467) cites no source for 'the brokerage reading later work gave the network'. The main text also reports 'as in the 2008 and 2009 snapshots' but omits the 2002 snapshot, which is MIXED (women's lower constraint beyond affiliation, S3 p = .005). It does not say that 2009-08 is the article's own snapshot. And its list names only three of the four statistics behind 'all four p >= .653'. The limitations (back L162) do not mention the full-text limitation.",
    "M6. Remaining limit on significance (not fully fixable by editing). The substantive AI-decision evidence is a negative domain result on two CPC classes plus an exploratory description. RQ2, the only organisation-level question, remains unresolved after two firm nulls, one of them invalid. R1 does not touch the conclusion of any coded study. The manuscript now spans Study 1, an external screen, seven patent plans, a review, R1, an MLP agenda and a Study 3 plan, at 11,999 of 12,000 prose words. For a management or IS journal, the paper is a methodological correction with modest substantive content, and its breadth dilutes the message."
  ],
  "Weaknesses_Minor": [
    "m1. Plan counts are stale. The abstract (L1), front L79, L114, L142, studies L170, back L157 and appendix L12 say 'five' plans or analyses, while Table A1 lists seven (Plans 1-5, C, 6), and the review protocol and R1 preregistration are further frozen plans. front L146 omits Plan 6, S1 and R1-A1. Checklist row 9 (back L46) omits Plan 6, the review protocol, S1, R1 and R1-A1.",
    "m2. Checklist row 7 (back L44) reintroduces the round-3 conflation: '13 of 16 ... keep their direction without same-term records', with no mention that the keyword matrix also changes the coding instrument.",
    "m3. Figure 1 (fig_research_design.png) and the overview table (front L89-129) omit the systematic review and R1, although Section 6 is now central to Contribution 1.",
    "m4. Abstract-level exposure is not stated where the review's prevalence is headlined: abstract L1 ('most gap claims lack a baseline'), front L20, back L24, checklist rows 6 and 8 (back L43, L45), and conclusion back L179.",
    "m5. The Plan 6 smoke test (2 replicates showed the gate failing before the full run; T1/T2 were sealed unread) is not disclosed.",
    "m6. The appendix L249 phrase 'round-3 sample' (OCDS) is an internal round reference.",
    "m7. The log is stale. E5 (log L621) says the optional replication was 'not done in this round', contradicting E5.1. The E3 header (log L162) says 'four preregistrations', and the E3 commit list stops at Plan 4.",
    "m8. The word-count script labels the total 'Sections 1-9', but the conclusion is now Section 10. The prose count excludes the new checklist and review tables and all captions, so the main text, counted as most editors count it, is probably well above 12,000.",
    "m9. Search terms deviate slightly from the protocol ('research gap' was queried; the protocol says 'research gap(s)'). This should be noted in Appendix D.",
    "m10. studies L419 writes '74.1% of patent ownership' for what the log defines as the share of patent-owner pairs."
  ],
  "Originality": 2,
  "Quality": 3,
  "Clarity": 2,
  "Significance": 3,
  "Questions": [
    "Under the preregistered Plan 6 reporting rule, will you report the descriptive T1/T2 null medians and p-values, the singleton-stratum share and the ±20% degree share? Given the S-tech T1 value (p = .236), will you state that T1, not only T2, is untested under a degree-holding null?",
    "How many of the 135 hole or broker claims compute the measure on a network whose ties record joint work (co-inventorship, co-authorship, co-application), and how many on pure label or keyword co-occurrence? Does the abstract's 'the inference is common' survive restricting to the latter?",
    "Can a human coder, blind to the LLM codes, code a random subsample (for example 40-50 included studies plus 20 exclusions) on inclusion, D2, F1-F3 and V? What are the human-LLM agreement figures, especially for F3?",
    "What is the concentration of between-firm credit for all in-scope citations, so that the 42.8% held by 13 firms has a reference?",
    "Can you show cross citations' OE by period alongside the raw-share rise, as Plan C item C5 prescribes, so that 'growing' can be checked against the declining OE?",
    "Which secondary sources attribute the broker reading to the Norwegian board network, and can one be added to citation_map.json so that the main-text claim is sourced?",
    "Is there a coded study (not an outside case) with open two-mode data on which the diagnostic could be re-run, so that the re-analysis touches a conclusion in the coded set?"
  ],
  "Limitations": [
    "The review is abstract-level and LLM-coded, with low reliability on F3, V and screening; its prevalence figures record exposure, not error.",
    "The stream-S prevalence is dominated by ego-level Burt measures on co-inventor and collaboration networks, a practice related to but distinct from domain-level hole inference.",
    "R1 covers one case outside the coded set; the article's full text was not accessed, and the case tests a reading attributed to later work.",
    "Firm-level brokerage, and the robustness of T1 to firm degree, are untested: the degree-stratified null failed its gate.",
    "Plan C is descriptive with no portfolio baseline; raw shares and OE move in opposite directions over time.",
    "All carried-over limitations of round 3 still apply: CPC constructs; one-sided granularity; uncalibrated cell-level inference; self-timestamped plans; simulated MLP."
  ],
  "Ethical Concerns": false,
  "Soundness": 3,
  "Presentation": 2,
  "Contribution": 3,
  "Overall": 5,
  "Confidence": 4,
  "Decision": "Major revision (borderline). Significance has improved. The score is held at 5 by the Plan 6 reporting deviation, the Plan C summary overclaims, the LLM-only review with its pooled headline, and the presentation debt. With R1-R8 below done (above all, a human-validated review subsample and the Plan 6 descriptive reporting), a 6-7 is within reach.",
  "Number_Mismatches": "None found in the manuscript. Near-mismatches in wording: back L24 'about three in four' (log: 96/135 = 0.71 for F2; 99/135 = 0.73 for F1 among the 135 claims; 0.748/0.733 only in stream S); studies L419 'patent ownership' (log: patent-owner pairs). The log is internally stale at L162 ('four preregistrations') and L621 ('not done in this round').",
  "Required_Changes": [
    {"id": "R1", "file": "en/studies.tex; en/appendix.tex; en/back.tex", "line": "studies L410; appendix L60-64 (Table A1 row 6); back L152", "change": "As the Plan 6 preregistration (§3) requires, report the T1/T2 null medians, 95% bands and p-values for both schemes, the singleton-stratum share and the ±20% degree share, all labelled 'descriptive; INVALID_NULL; not interpreted' (an appendix row or note suffices). In back L152, add that T1, like T2, has not been tested under a valid degree-holding null, and mention the 2-replicate smoke test in one clause."},
    {"id": "R2", "file": "en/studies.tex; en/front.tex; en/back.tex", "line": "studies L417, L419, L423; front L20 (Contribution 3); back L175", "change": "Replace 'the connection is growing' with 'cross citations rose as a share of in-scope citations, while their intensity relative to expectation declined (OE 3.90 to 2.34) and the BRIDGE share fell after 2023'. Replace 'through firms that hold both kinds of patent' with 'with a mixed-portfolio firm as the citing party'. Extend the 'no portfolio baseline' caveat to the MIXED-citing share. Drop 'a few firms'. Recast Contribution 3 as the negative result, with Plan C as exploratory context."},
    {"id": "R3", "file": "en/abstract.tex; en/front.tex; en/back.tex; en/studies.tex", "line": "abstract L1; front L20; back L24, L179; studies L465, L469", "change": "Separate the two practices in every summary. Use '73 of the 135 hole or broker claims are patent co-inventor, co-applicant or co-classification networks, mostly used as predictors of outcomes; 46 of 66 gap claims report no baseline in the abstract'. Add the 73-of-135 cross-tabulation to log E5 first; all 73 D1 = patent studies are claims in included_studies_coded.csv. State that the project's own inference corresponds most closely to the gap practice. Replace 'about three in four' with '96 of 135'. Replace 'the same inference' (L179) with 'structural-hole or broker claims from co-occurrence or affiliation networks'."},
    {"id": "R4", "file": "en/studies.tex; en/appendix.tex; en/back.tex", "line": "studies L438; appendix L490-492; back L162", "change": "Name the LLM family and version used for screening, coding and adjudication. Add a human-coded random validation subsample (inclusion, D2, F1-F3, V) and report human-LLM agreement. If that is not possible, downgrade the F3-based statements to 'model-coded indication' and reconcile them explicitly with appendix L456 (Study 3 rejects model-assisted coding)."},
    {"id": "R5", "file": "en/abstract.tex; en/front.tex; en/back.tex", "line": "abstract L1; front L20; back L24, L43, L45, L179", "change": "Describe the review figures as abstract-level exposure wherever they are headlined, for example 'report no baseline in their abstracts' instead of 'lack a baseline'. Replace '204 published studies' with '204 studies indexed in OpenAlex (articles, proceedings and preprints)'."},
    {"id": "R6", "file": "en/studies.tex; en/back.tex", "line": "studies L467; back L162", "change": "In the main text, state that the article's full text was not accessed and that its measures were reconstructed from the abstract and secondary summaries. Cite or remove 'later work'. Report the 2002 snapshot (MIXED; S3 p = .005), note that 2009-08 is the article's snapshot, and name S3 in the list of statistics. Add the full-text limitation to back L162."},
    {"id": "R7", "file": "en/abstract.tex; en/front.tex; en/studies.tex; en/back.tex; en/appendix.tex; figures/fig_research_design.png", "line": "abstract L1; front L79, L89-129, L114, L142, L146; studies L170; back L44, L46, L157; appendix L12", "change": "Make the plan inventory consistent: seven frozen patent plans (Plans 1-5, one confirmatory; Plan C descriptive; Plan 6 INVALID_NULL), plus the review protocol (S1) and the R1 preregistration (R1-A1). Update front L146 and checklist row 9 accordingly. Restore the instrument-change qualifier in checklist row 7. Add the review and R1 to Figure 1 and to tab:front_overview."},
    {"id": "R8", "file": "en/appendix.tex", "line": "L14-67 (Table A1); L69-94 (Table A2)", "change": "Table A1 (about 75-80 lines at footnotesize) will exceed the 9 in text height. Split it into A1a (Plans 1-5) and A1b (Plans C, 6, review, R1), or set it with longtable/xltabular. Check Table A2 after compilation."},
    {"id": "R9", "file": "en/*.tex; scripts/wordcount.py", "line": "whole main text", "change": "Recover word headroom to absorb R1-R7 (target at most 11,500 prose words). For example, move the Study 1 network-lines table and paragraph (studies L129-161) and the P6-P10 detail to the appendix. Fix the 'Sections 1-9' label in the script, and report a count that includes tables and captions."},
    {"id": "R10", "file": "raw_materials/experimental_log.md; en/appendix.tex", "line": "log L162, L180, L621; appendix L249", "change": "Update the log: E3 header (seven plans; complete commit list) and E5 ('Optional replication: done, see E5.1'). Replace 'round-3 sample' (OCDS) with a neutral description."}
  ],
  "Integrity_Findings": [
    {
      "file": "en/studies.tex; en/appendix.tex",
      "location": "studies L410; Table A1 row 6 (appendix L60-64)",
      "issue": "A preregistered reporting rule is not followed (Plan 6).",
      "evidence": "PREREGISTRATION_FIRM_NULL_DEGREE.md §3: 'If the gate fails ... its T1/T2 p-values are reported as descriptive only'; it also lists the singleton-stratum share and the ±20% share as 'Also reported'. PLAN6_RESULTS.json and log E3.7 hold them (primary T1 0.315, p .001; S-tech T1 0.249, p .236; T2 p 1.000 in both; singleton shares 0.0052 and 0.062; ±20% shares 0.336 and 0.366). None appears in the manuscript.",
      "suggested_fix": "See R1."
    },
    {
      "file": "en/studies.tex; en/front.tex; en/back.tex",
      "location": "studies L417, L419; front L20; back L175",
      "issue": "Plan C summary wording exceeds the descriptions and omits the preregistered C5 pairing.",
      "evidence": "PLAN_C_DESCRIPTIVE.md item C5 pairs C1/C2 with the yearly OE and H2 slope. OE fell from 3.90 to 2.34; the BRIDGE share fell from 0.0514 (2023) to 0.0407 (2025) (PLAN_C_RESULTS.json). 'Through' firms implies intermediation; the datum is the citing owner's group. The MIXED-citing excess has a portfolio-mechanical explanation that the paper itself used to motivate Plan 4.",
      "suggested_fix": "See R2."
    },
    {
      "file": "en/abstract.tex; en/back.tex",
      "location": "abstract L1; back L24, L179",
      "issue": "The review prevalence is overstated as 'the (same) inference' and is not described as abstract-level exposure.",
      "evidence": "In included_studies_coded.csv, 73 of the 135 hole or broker claims have D1 = patent. search_log.json: the 'structural hole' + patent query gives 165 of 308 stream-S hits. Among the 135 claims, F2 = 96 (0.71). E = abstract for all 204.",
      "suggested_fix": "See R3 and R5."
    },
    {
      "file": "en/studies.tex; en/appendix.tex",
      "location": "studies L438; appendix L456, L490-492",
      "issue": "The paper relies on LLM-only coding, in tension with its own methodological rule, and the model is not named.",
      "evidence": "Log E5 disclosure: all screeners, coders and adjudicators were Claude subagents. coding_agreement.json: F3 0.192, V 0.312. screening_agreement.json: 0.361. Appendix L456 rejects model-assisted coding for Study 3 'given Study 1'.",
      "suggested_fix": "See R4."
    },
    {
      "file": "en/studies.tex",
      "location": "L467",
      "issue": "The R1 caveats are only in the appendix, and the secondary snapshot reporting is selective.",
      "evidence": "R1_CLAIM_RECORD.md: 'Full text not accessed'; the broker reading is '[secondary]'. R1_D3_2002-05-01.json: overall MIXED, S3 p = 0.005. The main text mentions only the 2008 and 2009 snapshots.",
      "suggested_fix": "See R6."
    },
    {
      "file": "en/appendix.tex",
      "location": "Table A1, L14-67",
      "issue": "Layout: the float is likely taller than the page.",
      "evidence": "From the cell lengths, about 75-80 lines at \\footnotesize (setspace keeps floats single-spaced), about 900 pt, against about 650 pt of text height (letter, 1 in margins). Widths fit (about 16.2 cm against 16.5 cm).",
      "suggested_fix": "See R8."
    }
  ],
  "Round3_Resolution": [
    {"weakness": "Significance and positioning (binding)", "status": "partially", "evidence": "The systematic review (Section 6, Table tab:review, Appendix D), R1 and the checklist (tab:checklist) were added under frozen protocols, and the numbers match. The limits are the abstract-level, LLM-only coding, a headline dominated by co-inventor-network Burt studies, and an R1 outside the coded set that tests a reading attributed to later work (M3-M5)."},
    {"weakness": "Construct checks mis-described (/06 only; one-sided granularity; non-independence)", "status": "resolved", "evidence": "studies L186, L210; Table tab:construct with C-e/C-f (OE 3.16); back L140; appendix L91 (C1). Numbers match E3.5."},
    {"weakness": "RQ2 untested (degree and portfolio null)", "status": "attempted; unresolved", "evidence": "Plan 6 was run and failed its validity gate (rho 0.817 / 0.825 < 0.90). The INVALID_NULL is reported correctly, but the preregistered descriptive values are omitted (M1)."},
    {"weakness": "Cell-level inference uncalibrated; M06-P as a contribution", "status": "partially", "evidence": "Contribution 5 now says 'proposes two null models, neither with a separate type-I calibration' (front L20). No calibration was run."},
    {"weakness": "Study 3 coding biased toward allocation", "status": "resolved", "evidence": "back L109, Table tab:back_study3_rivals, appendix L458: cost is defined by return, and allocation requires positive evidence."},
    {"weakness": "Section 7 not condensed; Level-3 constants withheld", "status": "resolved", "evidence": "Section 7 is now short; constants are in Tables tab:app_configs and tab:app_processes. Word headroom has not been recovered (11,999 / 12,000)."},
    {"weakness": "Self-pairing wording", "status": "partially", "evidence": "Fixed in studies L95, back L138 and appendix L96/L108. It has regressed in checklist row 7 (back L44)."},
    {"weakness": "Presentation: plan count, internal review references, label collision", "status": "partially", "evidence": "C-a to C-f naming done; 'round-2 review' removed. The plan count is now stale in a new way (five vs seven; m1); 'round-3 sample' remains (appendix L249)."}
  ]
}
```
