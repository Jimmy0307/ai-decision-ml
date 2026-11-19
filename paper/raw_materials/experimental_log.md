# Experimental log — AI × Decision structural-hole programme (ground truth for all numbers)

Every number below is copied from a result file in `paper/data/` or from a file in the
`Jimmy0307/ai-decision-ml` repository, as named in each block. Provenance grades:

- **DIRECT**: recomputed or parsed from frozen files in 2026-11.
- **HISTORICAL**: reported in earlier project logs; the raw files were not available for re-verification.
- **USER_REPORTED**: reported by the researcher; raw files local only.

Writers must not introduce any number that is not in this log.

---

## E1. Study 1 — Literature functional matrix (V5 corpus, V9 frozen analysis)

### E1.1 Corpus and matrix (DIRECT)

- 2,118 source documents; 1,729 parsed; 26,501 candidate evidence records; 6,499 strict records.
- Bipartite AI-family × Decision-family matrix: 10 AI families × 12 decision families = 120 cells.
- 2,180 document-level edges, deduplicated within each document.
- 104 cells observed; 16 zero cells. The zero cells are disjoint from the 16 depleted cells.
- Four tests:
  - main fixed-degree stub Monte Carlo (R = 10,000, seed 20260918);
  - exact hypergeometric test;
  - document-preserving within-document swap MCMC (5,000 samples, burn-in 43,600, thinning 4,360, seed 20260919);
  - raw-record exact test (non-deduplicated records, n = 3,125).
- Benjamini–Hochberg FDR within the 120 cells.
- Frozen core: q ≤ .05 in main + exact + document-preserving tests with the same direction, plus raw. Result: **32 cells (16 enriched, 16 depleted)**.
- Expected count: E = k_a k_d / M, with M = 2,180.
- 86.5% of edges come from AI-track documents.

### E1.2 The 16 depleted cells (V9 frozen; observed counts; `paper/data/V9_ROBUSTNESS_MASTER_TABLE.csv`)

Names are AI family × decision family; O is the observed count.

| AI family | Decision family | O |
|---|---|---:|
| COORDINATION_EXECUTION | HUMAN_REVIEW_ACCOUNTABILITY | 10 |
| COORDINATION_EXECUTION | RISK_ASSESSMENT | 3 |
| EVALUATION_ASSESSMENT | ALLOCATION_PLANNING | 12 |
| EVALUATION_ASSESSMENT | PREDICTION_DIAGNOSIS | 9 |
| EXPLANATION_ASSURANCE | ALLOCATION_PLANNING | 7 |
| EXPLANATION_ASSURANCE | EVALUATION_SELECTION | 7 |
| EXPLANATION_ASSURANCE | PREDICTION_DIAGNOSIS | 15 |
| GENERATION_SYNTHESIS | PREDICTION_DIAGNOSIS | 7 |
| HUMAN_AUGMENTATION | EVALUATION_SELECTION | 2 |
| HUMAN_AUGMENTATION | PREDICTION_DIAGNOSIS | 3 |
| PREDICTION_RISK_ESTIMATION | EVALUATION_SELECTION | 8 |
| PREDICTION_RISK_ESTIMATION | GENERAL_DECISION_PROCESS | 8 |
| PREDICTION_RISK_ESTIMATION | GOVERNANCE_OVERSIGHT | 26 |
| PREDICTION_RISK_ESTIMATION | HUMAN_REVIEW_ACCOUNTABILITY | 6 |
| PREDICTION_RISK_ESTIMATION | INFORMATION_ACQUISITION | 21 |
| RECOMMENDATION_OPTIMIZATION | HUMAN_REVIEW_ACCOUNTABILITY | 8 |

The most extreme cell is PREDICTION_RISK_ESTIMATION × HUMAN_REVIEW_ACCOUNTABILITY: O = 6, E = 44.9.

### E1.3 Robustness of the pattern (DIRECT; data-validity re-analysis 2026-11-18)

- **Re-implementation:**
  - the exact and raw tests reproduce the official q values (|Δq| ≤ 6×10⁻¹²);
  - the Jaccard overlap of the 32-cell core is .94.
- **20 Monte Carlo seeds:**
  - 31 cells are in the core under every seed, including all 16 depleted cells;
  - 2 cells are boundary cells. They are exactly the one-in / one-out pair of the human-corrected sidecar.
- **Exclusion bias:** depleted core cells pass the strict filter more often than other cells (38% vs 28%).
- **Track-stratified null** (fixed composition of AI-track vs decision-track documents): 16/16 depleted and 16/16 enriched cells remain significant, with unchanged direction.
- **Two periods (≤2023 vs ≥2024):**
  - 16/16 cells are depleted in both periods;
  - the change does not differ from a permutation null (p = .86). The under-integration is persistent, with no sign of closing.
- **Keyword (stage-1) triangulation:** 13/16 depleted cells have the same direction under keyword coding.
- **Same-term self-pairing:** in the strongest enriched cell (prediction × prediction), 33% of records pair the same term (e.g. "forecasting") on both sides. Removing them, 2 prediction-related depleted cells drop out of the core.
- **Rule-based keyword matrix:**
  - 741 same-term records are removed, leaving 1,431 document edges;
  - 13/16 depleted cells keep the same direction, 6 are significant and 0 are significantly reversed;
  - only 7 cells reach the four-test core.

### E1.4 Measurement reliability (DIRECT)

| Comparison | AI κ | Decision κ |
|---|---:|---:|
| Human vs human (n = 20) | 0.05 | 0.14 |
| Pipeline LLM (qwen) vs first human coder (n = 50) | 0.27 | 0.12 |
| Pipeline LLM test–retest (143 sides) | 0.64 | 0.63 |
| Theory-merged taxonomy (7×6), human vs human | 0.08 | 0.16 |
| Two Claude models, blind, codebook v2 (250 records): Sonnet vs Haiku | 0.72 (0.87 among sides both coded) | 0.56 (0.82) |
| Claude (codebook v2) vs reconciled human answers (n = 20) | 0.45 | 0.70–0.76 |
| Pipeline qwen vs reconciled human answers | 0.11 | 0.29 |

- Under codebook v2, 42–64% of evidence sentences state no explicit decision function. The pipeline's rate was 18%.
- Only about 9% of matrix records are reproduced in the same cell by both new coders.
- Agreement between models shows that the tool is reproducible. It is **not** human inter-rater reliability.

### E1.5 Misclassification sensitivity (DIRECT)

**Analytic bound.** Under non-differential (random) misclassification:

O_obs/E − 1 = (1 − e_AI)(1 − e_Dec)(T/E − 1)

- Random error can only attenuate a depletion; it cannot create one.
- For the most extreme cell, even the 95% upper bound requires the product of the two accuracies to be ≥ 0.71. The human audit implies a product of about 0.07.

**Simulation.** 300 runs per scenario; in each run the matrix is rebuilt and the BH exact test redone. Figures are the median (5th–95th percentile) number of the 16 depleted cells.

| Scenario | Still significant | Still depleted |
|---|---|---|
| First human coder as truth | 0 (0–1) | 11 (8–13) |
| Reconciled human as truth | 0 (0–1) | 12 (10–14) |
| 20% random error + 20% deletion | 7 (5–10) | 16 (15–16) |
| 40% random error + 20% deletion | 0 (0–1) | 14 (12–16) |
| 60% random error + 20% deletion | 0 (0–0) | 10 (7–13) |
| Claude consensus (codebook v2) as truth | 4 (3–6) | 14 (12–15) |

No scenario produced a spurious depleted cell.

**Verdict (2026-11-18):**
- directional under-integration: DEFENSIBLE;
- "16 statistically robust depleted pairs": NOT DEFENSIBLE as measured;
- Burt structural hole: STOP;
- research gap: NOT SUPPORTED.

### E1.6 Network lines V6–V11.1 (HISTORICAL / USER_REPORTED unless noted)

| Version | Line | Scale | Result |
|---|---|---|---|
| V6 | citation SNA | 458 leads; 13 G2 candidates | 0 confirmed |
| V7 | author SNA | 446 works; 8 cross-domain authors; 2 focal candidates | 0 confirmed |
| V8 | citation enrichment | 1,111 citing works; 5,592 references | unconfirmed |
| V9 | citation line | 3,983 discovery + 3,897 confirmation works (7,880 total) | no confirmed Burt result |
| V10 | higher-order network | 14 exploratory candidates → 8 pairs / 7 brokers | exploratory only |
| V10.1 | external review | 8 candidate pairs | 6 refuted, 2 unresolved, 0 confirmed |
| V11 | co-author SNA | 26,443 V9 authors; 30,140 merged authors | 0 confirmed |
| V11.1 | external identity / peer validation | 95 OpenAlex requests; 7,880 works examined; 4 candidates | 3 rejected, 1 insufficient, 0 confirmed |

**Gap Validity V1 (DIRECT sidecar):**
- in the bipartite family network, all 16 depleted cells have alternative routes (16/16);
- the indirect term of Burt constraint is identically zero in a strict bipartite graph.

---

## E2. External-data feasibility (six public sources; DIRECT; `paper/data/EXTERNAL_ROUND3_KEY_NUMBERS.json`)

**CORDIS H2020:**
- 35,389 projects; 179,063 organisation participations.
- Keyword candidates: 195 projects × 1,105 organisations = 1,436 edges.
- Co-membership projection: 1,049 nodes, 12,181 edges. Projection creates 102,660 within-project triads, and only 156 edges recur across ≥ 2 projects.
- Degree-preserving bipartite swap null (49 reps):
  - 5 testable low-constraint candidates, with p = .41–.86 and BH q ≥ .80;
  - 0 significant.

**GLEIF Level-2:** 663,449 relationship records (481,247 active). This is legal consolidation, not information flow.

**Other sources:**
- OpenAlex: 8 works.
- OCDS: 0 verifiable buyer–supplier edges in the round-3 sample.
- SEC: not fetched (requires a genuine contact User-Agent).
- PyPSA: 8,786 buses (a physical grid).

**Verdict:** no source passes the independent-relation and validation gates. Co-membership, ownership and physical topology are not information flows.

---

## E3. Study 2 — US patents (DIRECT; four preregistrations frozen before analysis)

**Data:** USPTO PatentsView `pvgpatdis`, downloaded 2026-11-18.
- 8,512,829 utility patents granted 1976–2025.
- 152,631,929 citation rows. In scope (citing year 2010–2025): 87,414,291; of these, 63,083,371 applicant citations.
- Before 2013, PatentsView labels non-examiner citations "cited by other", so the applicant-only specification effectively covers citing years 2013–2025.
- Grant years 2010–2025:
  - AI (CPC G06N): 94,929 patents;
  - DEC (CPC G06Q10/04 forecasting/optimisation + G06Q10/06 resources, workflow, management, decision analysis): 37,501;
  - BRIDGE (both): 5,316;
  - other business-method patents (G06Q excluding G06Q10): 150,170.

**Preregistration commits:**
- aggregate test `a8f3289`;
- V9 battery `a6266f7`;
- full suite `d641256`;
- firm null `b59fc71`.

All commits are in PR #5 of `Jimmy0307/ai-decision-ml`.

### E3.1 Aggregate test (preregistration 1; `paper/data/PATENT_HOLE_RESULTS.json`)

**Statistic:** symmetric intensity OE(A,B) = [O(A→B) + O(B→A)] / [E(A→B) + E(B→A)], where

E(A→B) = Σ_s out_A(s) · in_B(s) / M(s)

over strata s = (citing grant year, cited grant year).

**Primary result (applicant citations):**
- O = 30,843 and E = 10,112, so **OE(AI,DEC) = 3.05** (95% CI 2.94–3.17; Poisson cluster bootstrap over citing patents, 2,000 reps).
- AI→DEC: O = 21,820, E = 6,686 (O/E 3.26). DEC→AI: O = 9,023, E = 3,426 (O/E 2.63).

**H1a — comparison with 179 reference CPC main groups (G06/G16/H04, ≥ 2,000 patents):**
- OE(AI,DEC) exceeds 97.8% of {OE(AI,X)} and 92.2% of {OE(DEC,X)};
- reference lowest-quartile values: AI side 0.787, DEC side 0.502; medians 1.240 and 1.095;
- criterion (OE in the lowest quartile on both sides): FAIL.

**H1b — comparison with other business-method patents:**
- OE(AI,DEC) / OE(AI,BIZ-OTHER) = 1.69 (95% CI 1.60–1.77), where OE(AI,BIZ-OTHER) = 1.809;
- criterion (upper CI bound < 1): FAIL.

**Verdict: HOLE_NOT_SUPPORTED.** All 6 preregistered sensitivity checks agree (0/6 disagree; not fragile):

| Specification | OE(AI,DEC) | Ratio vs BIZ (95% CI) | Percentile AI / DEC | Verdict |
|---|---:|---|---|---|
| primary | 3.05 | 1.69 (1.60–1.77) | 97.8% / 92.2% | NOT_SUPPORTED |
| s1 all citation categories | 3.00 | 1.65 (1.55–1.75) | 98.9% / 92.7% | NOT_SUPPORTED |
| s2 DEC = all G06Q10 | 2.59 | 1.43 (1.38–1.49) | 95.5% / 89.9% | NOT_SUPPORTED |
| s3 AI broadened (+G06F18, G06V10/70) | 2.69 | 1.56 (1.50–1.63) | 94.4% / 86.6% | NOT_SUPPORTED |
| s4 inventive codes only | 3.00 | 1.62 (1.54–1.70) | 97.7% / 94.5% | NOT_SUPPORTED |
| s5 citing 2015+ | 3.04 | 1.69 (1.61–1.78) | 98.2% / 92.9% | NOT_SUPPORTED |
| s6 bridge patents counted on both sides | 4.25 | 2.35 (2.23–2.47) | 100% / 99.4% | NOT_SUPPORTED |

**H2 — trend over citing years** (primary; OE by year with 95% CI):

| Year | OE | 95% CI |
|---|---:|---|
| 2013 | 3.90 | 3.16–4.85 |
| 2014 | 2.84 | 2.42–3.41 |
| 2015 | 3.79 | 3.14–4.55 |
| 2016 | 4.05 | 3.42–4.75 |
| 2017 | 3.29 | 2.78–3.86 |
| 2018 | 3.20 | 2.81–3.64 |
| 2019 | 3.99 | 3.48–4.54 |
| 2020 | 3.55 | 3.18–3.94 |
| 2021 | 3.34 | 3.03–3.69 |
| 2022 | 2.95 | 2.62–3.30 |
| 2023 | 3.05 | 2.78–3.34 |
| 2024 | 2.69 | 2.40–2.98 |
| 2025 | 2.34 | 2.08–2.64 |

- WLS slope −0.097 per year (95% CI −0.130 to −0.065).
- Last-3-year OE 2.69, against a reference median of 1.095.
- Preregistered label: PERSISTENT. The over-connection declines but remains more than twice the reference median.
- **H2 rule (Plan 1):**
  - `CLOSING` if the slope is > 0 with a 95% CI above 0 **and** last-3-year OE ≥ the reference median;
  - `PERSISTENT` if the slope CI includes 0 or lies below it;
  - otherwise `NARROWING_BUT_OPEN`.
  - The rule was written for the hole case.

**Synthetic calibration** (before real data):
- no hole: OE 0.388 vs reference lowest quartile 0.356; ratio 0.99 (0.79–1.21) → HOLE_NOT_SUPPORTED;
- 30% suppression: 0.275, ratio 0.66 (0.52–0.83) → detected;
- 50% suppression: 0.223, ratio 0.47 → detected.

### E3.2 V9 test battery on a patent CPC matrix (preregistration 2; `paper/data/V9_MATRIX_RESULTS.json`, `SUITE_P1_*_CELLS.csv`)

**Matrix:**
- Rows: 6 AI-method rows (G06N3 neural, G06N5 knowledge-based, G06N7 probabilistic/fuzzy, G06N10 quantum, G06N20 machine learning, G06N_OTHER).
- Columns: 7 decision-function columns (FORECAST_OPTIMISE G06Q10/04; RESOURCE_SCHEDULING /0631; WORKFLOW /0633; RISK /0635; STRATEGY /0637; PERFORMANCE /0639; MGMT_GENERAL other /06).
- 42 cells in total.
- Engine: byte-identical copy of the Route A V9 engine (SHA-256 09c3d60c…bc33).

**Parts:**
- Part A, co-classification: 5,316 patents, 14,573 edges.
- Part B, applicant citations between AI-only and DEC-only patents: 30,843 citations, 66,056 edges.
- Part B, all citation categories: 38,252 citations, 80,849 edges.

**Original M06 (document-preserving swap): 0 of 21,843,600 swaps accepted.** Each document contributes the complete row × column product, so every swap targets an existing edge. The preregistered core is 0 by construction, which is uninformative (amendment B1).

**Patent-adapted M06-P** (permute column sets among documents within (|rows|, |cols|) strata; both margins and the block structure preserved; 5,000 samples):
- Part A: adapted full core 8 depleted / 7 enriched;
- Part B: 9 depleted / 8 enriched;
- Part B, all categories: 8 / 8.
- Number of q ≤ .05 cells by test (main / exact / raw / M06-P): A 20 / 20 / 29 / 22; B 22 / 22 / 27 / 25.

**Cells depleted in both A and B** (adapted full core and 3-test agreement give the same set). Note: G06N10 × PERFORMANCE has expected count < 10 in Part B, so read it as small-sample. Values are O/E, with observed / expected in brackets:

| AI method | Decision function | Part A | Part B |
|---|---|---|---|
| G06N3 | RISK | 0.78 (171 / 219.5) | 0.70 (1,050 / 1,510.6) |
| G06N5 | RISK | 0.87 (255 / 291.9) | 0.85 (2,008 / 2,366.6) |
| G06N3 | MGMT_GENERAL | 0.87 (497 / 572.7) | 0.95 (4,189 / 4,414.8) |
| G06N20 | FORECAST_OPTIMISE | 0.89 (994 / 1,120.9) | 0.93 (2,255 / 2,425.9) |
| G06N10 | PERFORMANCE | 0.08 (1 / 12.0) | 0 (0 / 8.9) |

The quantum-computing row is tiny: 74 edges in A.

**Cells enriched in both A and B under the 3-test rule** (main + exact + raw; G06N7 × PERFORMANCE is adapted full core only in B: Part A M06-P q = .93):
- G06N20 × RISK (1.18 / 1.33);
- G06N3 × FORECAST_OPTIMISE (1.09 / 1.17);
- G06N5 × MGMT_GENERAL (1.16 / 1.06);
- G06N7 × PERFORMANCE (1.15 / 1.16).

### E3.3 Full replication suite (preregistration 3; `paper/data/FULL_SUITE_RESULTS.json`)

**P2, V9.1 calibration:**
- Seeds (20 × 10,000): in A, 20 cells are always q ≤ .05 and 4 are boundary cells; in B, 22 always and 0 boundary.
- 1,000 stub-permutation null matrices (exact + BH):
  - mean false cells per matrix: 0.045 (A), 0.049 (B);
  - share of matrices with any false cell: 3.6% (A), 4.4% (B).
- Power to detect a 20% depletion in cells with E ≥ 100: 18/27 = 67% (A), 23/29 = 79% (B).
- Segmentation (adapted full core depleted, with overlap with P1):
  - S1, inventive codes only: A 8 (overlap 6), B 11 (overlap 8);
  - S2, single-code documents: A 8 (overlap 5), B 8 (overlap 4).

**P3, exploration/confirmation by time (V6/V8/V9 citation line):**
- Part A, 2010–2017: 543 documents, 0 depleted. 2018–2025: 4,773 documents, 8 depleted.
- Part B, 2013–2018: 4,772 documents, 3 depleted. 2019–2025: 26,071 documents, 11 depleted.
- **0 depleted cells replicate in both halves, in A or in B.**

**P4, label face validity** (title keyword hit rate vs other AI∪DEC patents; pass if lift ≥ 1.5). All 11 labels pass:

| Label | Lift |
|---|---:|
| G06N3 | 4.69 |
| G06N5 | 7.81 |
| G06N7 | 14.28 |
| G06N10 | 1,650 |
| G06N20 | 2.18 |
| FORECAST_OPTIMISE | 3.31 |
| RESOURCE_SCHEDULING | 4.51 |
| WORKFLOW | 4.88 |
| RISK | 55.39 |
| STRATEGY (hit rate 4.5%) | 4.40 |
| PERFORMANCE | 6.32 |

**P5, firm network (V7/V11 analogue):**
- 6,201 organisations with ties and 20,681 ties (total weight 109,508 applicant citations; self-citations excluded).
- Groups: 2,926 AI_FIRM (only AI-only patents), 1,570 DEC_FIRM, 1,705 MIXED.
- Group O/E: AI_FIRM~DEC_FIRM 0.24 (O 886, E 3,700); AI_FIRM~MIXED 0.81; DEC_FIRM~MIXED 0.97. The preregistered firm-level hole criterion is met.
- Median Burt constraint: AI_FIRM 0.62, DEC_FIRM 0.76, MIXED 0.36.
- MIXED versus a degree-matched label-permutation null: null median 0.444, one-sided p = .001.
- Lowest-constraint MIXED firms with degree ≥ 5: International Business Machines, General Electric, Tesla, ioCurrents, Google, Accenture, Amazon Technologies, T-Mobile USA, Optum Services, Strong Force VCN Portfolio 2019.

**P6, removal falsification (V10.1 analogue):**
- After removing all 10 candidates, AI_FIRM and DEC_FIRM firms remain connected; the largest component containing both groups falls from 5,954 to 5,563 firms.
- 10/10 candidates are refuted as indispensable brokers.
- The cross-weight-retained metric is identically 1 by construction, so it is uninformative.

**P7, co-assignment hyperedges:** 2,546; 32% join an AI_FIRM with a DEC_FIRM or MIXED firm.

**P8, alias check:** 54 firms checked; 0 possible alias collisions.

**P9, Gap Validity:**
- the indirect constraint term is 0 (bipartite);
- every depleted cell has 20–30 alternative length-3 routes;
- depleted cells at q ≤ .01 vs q ≤ .05: A 7 vs 9, B 9 vs 10.

**P10, Limitation Scout:** NOT_APPLICABLE (patents have no limitation section).

### E3.4 Portfolio-preserving firm null (preregistration 4; `paper/data/FIRM_NULL_RESULTS.json`, `FIRM_NULL_REPLICATES.csv`)

**Null:** within strata, permute patents' owner sets. This keeps every firm's portfolio and group and the whole patent-level citation network fixed.
- Primary strata: patent type × grant year (48 strata).
- S-tech strata: type × year × AI rows × DEC columns (1,795 strata).
- 1,000 replicates each; replicate r uses seed sequence [20261119, s, r].
- Scope: 127,114 patents, 14,600 firms, 162,339 citations.
- The identity permutation reproduces P5 exactly.

| Statistic | Observed | Primary null median [95%] | p | S-tech null median [95%] | p |
|---|---:|---|---:|---|---:|
| T1 OE(AI_FIRM~DEC_FIRM) | 0.240 | 0.356 [0.317–0.398] | .001 | 0.307 [0.277–0.345] | .001 |
| T2 MIXED median constraint | 0.358 | 0.104 [0.098–0.111] | 1.000 | 0.116 [0.110–0.122] | 1.000 |
| OE AI_FIRM~MIXED | 0.809 | 1.000 | .001 | 0.985 | .001 |
| OE DEC_FIRM~MIXED | 0.970 | 1.009 | .001 | 1.025 | .001 |

**Share of the T1 gap reproduced by the portfolio null:** 85% (primary), 91% (S-tech).

**Derived residual:** the share of the observed specialist separation (1 − T1_obs) that the portfolio null does **not** reproduce is 15% (primary) and 9% (S-tech), i.e. 1 − 0.847 and 1 − 0.911. T1 is significant at the smallest attainable p with 1,000 replicates, p = 1/1,001 ≈ .001.

**Scope difference with P5:** the firm null starts from all 127,114 in-scope patents and 14,600 firms that own any in-scope patent, with 162,339 applicant citations among in-scope patents. P5 reports only the 6,201 firms that have at least one inter-firm tie after self-citations are removed, with 20,681 ties and total weight 109,508. The identity permutation reproduces the P5 values exactly.

**Ratio form of T1 (derived):** observed T1 divided by the null median is 0.240/0.356 = 0.67 (primary) and 0.240/0.307 = 0.78 (S-tech). Specialist ties are therefore 33% and 22% below what the portfolio null implies. On the gap-from-1 scale the null reproduces 85% / 91%; on the ratio scale the shortfall is 33% / 22%. Both readings are valid, and they answer different questions.

**Known limitation of the null:** the null preserves each firm's portfolio counts by type and year, not its degree or strength. Constraint is degree-dependent, so T2 cannot separate brokerage from degree. The degree-matched label null in P5 (null median 0.444) and the portfolio null (null median 0.104) answer different questions.

**Verdict: PARTIAL in both stratifications** (not tech-mix sensitive). Specialist separation is mostly a portfolio effect. The lower constraint of MIXED firms does not survive: real firms are more clustered than the null.

### E3.5 Construct-validity checks (Preregistration 5; `paper/data/PLAN5_CONSTRUCT_RESULTS.json`)

Frozen in commit `100f06a` (2026-11-19 10:44:56) before computation. This is a data-informed follow-up requested by the round-2 review. Plan 1's decision rule is unchanged.
- **DEC06** = any G06Q10/06 code: 33,926 patents (2010+). **DEC04** = any G06Q10/04 code: 5,893.
- Of these, 2,318 carry both /04 and /06 codes, 3,575 carry /04 only, and **31,608 carry /06 with no /04 code (DEC06S, strict)**. DEC06 therefore drops only the 3,575 /04-only patents; it is not a removal of /04.
- **Subgroup-family reference set** = main group + first two characters of the subgroup (built like DEC): 3,763 families in G06/G16/H04, of which 826 have at least 2,000 patents (excluding G06N and G06Q10).

| Spec | DEC | Reference | OE(AI,DEC) (95% CI) | Ratio vs BIZ (95% CI) | Percentile AI / DEC | Ref lowest quartile AI / DEC | Ref median AI / DEC | Verdict |
|---|---|---|---|---|---|---|---|---|
| P5a | any /06 code | 179 main groups | 3.04 (2.92–3.16) | 1.68 (1.60–1.76) | 97.8% / 90.5% | 0.787 / 0.511 | 1.240 / 1.077 | HOLE_NOT_SUPPORTED |
| P5b | /04 + /06 | 826 subgroup families | 3.05 (2.94–3.17) | 1.69 (1.60–1.77) | 89.8% / 84.1% | 0.875 / 0.605 | 1.419 / 1.316 | HOLE_NOT_SUPPORTED |
| P5c | any /06 code | 826 subgroup families | 3.04 (2.92–3.16) | 1.68 (1.60–1.76) | 89.6% / 83.5% | 0.875 / 0.612 | 1.419 / 1.330 | HOLE_NOT_SUPPORTED |
| P5d (descriptive) | any /04 code | 179 main groups | 3.83 (3.59–4.06) | 2.12 (1.96–2.29) | 99.4% / 93.9% | 0.787 / 0.486 | 1.240 / 1.129 | — |
| P5e (amendment C1) | strict /06, no /04 code | 179 main groups | 3.16 (3.05–3.27) | 1.75 (1.66–1.83) | 98.9% / 91.6% | 0.787 / 0.462 | 1.240 / 1.082 | HOLE_NOT_SUPPORTED |
| P5f (amendment C1) | strict /06, no /04 code | 826 subgroup families | 3.16 (3.05–3.27) | 1.75 (1.66–1.83) | 90.7% / 83.3% | 0.875 / 0.606 | 1.419 / 1.340 | HOLE_NOT_SUPPORTED |

**Counts:** P5a O = 28,877, E = 9,507. P5e O = 29,464, E = 9,328.

**Amendment C1** (commit `e6dce5c`, frozen 2026-11-19 12:30:21, before P5e/P5f were computed) adds the strict specifications after the round-3 review found the DEC06 overlap.

**Plan 5 decision rule:**
- Each specification uses Plan 1's rule.
- Construct verdict: `ROBUST_TO_CONSTRUCT` only if all verdict specifications are HOLE_NOT_SUPPORTED, otherwise `CONSTRUCT_SENSITIVE`.
- After C1 the verdict specifications are P5a, P5b, P5c, P5e and P5f.

**Known limits of Plan 5:**
- Granularity is matched on the reference side only; AI stays the whole G06N subclass.
- P5b has the same DEC as Plan 1, so its H1b is identical to Plan 1's and is not an independent check.
- Because OE(AI,DEC) is far above every reference quartile, the construct rule was expected to pass unless a respecification changed OE drastically.

**Construct verdict (five specifications): ROBUST_TO_CONSTRUCT.**
- Removing every /04-coded patent (P5e) raises OE slightly, from 3.05 to 3.16, so the over-connection is not produced by /04.
- /04 is more tightly linked to AI (OE 3.83).
- With granularity-matched references, the percentile falls to about 84–90% but stays far above the lowest quartile.

---

### E3.6 Plan C: locus of AI–decision integration (exploratory, descriptive; `PLAN_C_DESCRIPTIVE.md` frozen 969e60b; `paper/data/PLAN_C_RESULTS.json`)

**Scope and wording rules:**
- No p-values.
- Co-classification is not flow.
- Within-firm shares describe where citations occur, not organisational mechanisms.

**Data:**
- 127,114 in-scope patents: AI only 89,613; DEC only 32,185; BRIDGE 5,316.
- 14,600 firms.
- 162,339 applicant citations among the in-scope patents.

**C1 BRIDGE share (co-classification in G06N and G06Q10/04 or /06):**
- Overall: 5,316 / 127,114 = 0.0418 (4.2%).
- By year: 2010 1.3% (0.0126); peak 2023 5.1% (0.0514); 2024 0.0449; 2025 4.1% (0.0407).
- By period:
  - 2013–2018: 547 / 19,185 = 0.0285 (2.9%);
  - 2019–2025: 4,669 / 101,641 = 0.0459 (4.6%).

**C2 Cross citations (AI-only ↔ DEC-only, applicant):**
- Overall: 22,796 / 162,339 = 0.1404 (14.0%).
- By direction: AI cites DEC 15,999; DEC cites AI 6,797 (raw counts).
- By period:
  - 2013–2018: 1,785 / 16,524 = 0.108 (10.8%);
  - 2019–2025: 21,011 / 145,815 = 0.1441 (14.4%).
- Bridge citations (a BRIDGE patent at either end): 16,194 (0.0998).

**C2 Locus**, as shares of citations:

| | Cross citations | All in-scope citations |
|---|---|---|
| Within firm | 4,249, 18.6% (0.1864) | 47,320, 29.1% (0.2915) |
| Between firms, a MIXED firm citing | 14,636, 64.2% (0.6420) | 78,306, 48.2% (0.4824) |
| Between firms, specialists citing | 2,624, 11.5% (0.1151) | 28,155, 17.3% (0.1734) |
| Unowned end | 1,287, 5.7% (0.0565) | 8,558, 5.3% (0.0527) |

By period, cross citations:
- 2013–2018: within firm 17.0% (0.1697); between, MIXED citing 58.5% (0.5849); between, specialists citing 18.5% (0.1854).
- 2019–2025: within firm 18.8% (0.1878); between, MIXED citing 64.7% (0.6469); between, specialists citing 10.9% (0.1091).

**C3 Between-firm cross-citation credit** (one unit per citing owner):
- 17,372 units held by 1,247 firms.
- Concentration: top 10 firms 39.2% (0.3924); top 1% of credited firms (13 firms) 42.8% (0.4284).
- Credit share by owner group: MIXED 84.8% (0.8483), AI_FIRM 10.6% (0.1057), DEC_FIRM 4.6% (0.0460).
- Reference, share of patent–owner pairs: MIXED 74.1% (0.7412), AI_FIRM 19.2% (0.1920), DEC_FIRM 6.7% (0.0669).
- Firms by group: AI_FIRM 7,942, DEC_FIRM 4,213, MIXED 2,445.
- Patents without a non-individual owner: 4,086 (0.0321).

**C4 Within the 6×7 AI × DEC applicant-citation matrix** (O/E relative to the matrix margins; 29 cells with expected ≥ 100):
- Highest: G06N20 × RISK 1.331; G06N7 × STRATEGY 1.287; G06N3 × FORECAST_OPTIMISE 1.170.
- Lowest: G06N3 × RISK 0.695; G06N7 × RISK 0.701; G06N5 × RISK 0.848.

**Reading (post hoc):** the lower within-firm share of cross citations (18.6% vs 29.1%) has no baseline that holds portfolios fixed. It is a question for Study 3, not a finding about organisational boundaries.

## E4. Multi-level programming prototype (v1.0; SIMULATED; `paper/data/MLP_SOLVER_RESULTS_v1_0.json`)

**Model and exactness checks:**
- Exact backward induction over a bounded finite tri-level prototype: 3 processes, governance regimes C/F/D, budgets 3/5/7.
- All coefficients are simulated; no internal company data.
- Generator vs canonical domain check: 768 cases, 3,121 canonical-feasible state occurrences, 0 mismatches.
- Mutation sensitivity: 720/768 detected.
- Runtime 13.9 s.

**Level-2 objective (canonical model `01_CANONICAL_MODEL_v1_0.md`; weights are uncalibrated design values):**

F2 = Σ_i [0.90 Feas + 0.90 Rel + 0.45 Scalability − 0.55 IntegrationCost − 0.75 GovRisk + 0.65 max(0, U_i*)]

- Feas = clip[0,1](0.55 + 0.08(D̄ − D_req) + 0.08(R̄ − R_req) + 0.04(Ḡ − max(H_req, EA_req)))
- Rel = clip[0,1](0.45 + 0.10 EA + 0.06 H + 0.04 WI − 0.030 A·κ)
- Scalability = clip[0,1](0.30 + 0.08 D̄ + 0.08 R̄ + 0.04 WI)
- IntegrationCost = cost_Γ(0.10 A + 0.06 WI + 0.05 H + 0.05 EA)
- GovRisk = 0 if A = 0, else risk_Γ · 0.08 · κ · A / (1 + 0.4 H + 0.4 EA)

Level 3: Gain = g_im v_i ψ_i flex_Γ; Burden = β_m + 0.03 H + 0.02 EA + 0.02 WI; ResidualRisk = κ · autonomy_m · risk_Γ / (1 + 0.45 H + 0.45 EA).

In the permission probe, Level 1 re-optimises its allocation; capabilities are endogenous and are **not** held fixed.

**Level-3 constants (`04_solver_v1_0.py`; simulated design values).**

Configurations (A, H, WI, EA requirements; base gain g for processes P1/P2/P3; burden β; autonomy):

| Configuration | Requirements (A, H, WI, EA) | Gain g (P1 / P2 / P3) | Burden β | Autonomy |
|---|---|---|---:|---:|
| HumanOnly | (0, 0, 0, 0) | 0 / 0 / 0 | 0 | 0 |
| AIAssist | (1, 0, 1, 1) | 0.80 / 0.60 / 0.40 | 0.15 | 0.20 |
| AIFirstReview | (2, 2, 2, 2) | 0.65 / 0.90 / 0.70 | 0.25 | 0.50 |
| HumanFirstAICheck | (2, 1, 2, 1) | 0.75 / 1.00 / 0.80 | 0.30 | 0.40 |
| BoundedAutomation | (3, 3, 3, 3) | 0.40 / 0.70 / 1.20 | 0.10 | 1.00 |

Processes:

| Process | Description | κ | Value v | (D0, R0, A0, G0) | Selection / execution | τ | Score / truth |
|---|---|---:|---:|---|---|---:|---|
| P1 | low-risk informational support | 1 | 1.0 | (1, 1, 0, 1) | no / no | 0.40 | — |
| P2 | medium-risk recommendation/selection | 2 | 1.2 | (1, 1, 0, 1) | yes / no | 0.60 | 0.65 / 1 |
| P3 | high-risk bounded execution | 3 | 1.5 | (2, 2, 0, 1) | yes / yes | 0.70 | 0.72 / 1 |

ψ = max(0, (1 + 0.05 EA + 0.03 WI) × V), with V = 1 for a correct decision and 0.35 for an incorrect one.

Level-1 unit resource cost: c_i^r = 1 for every process and resource (canonical model "toy c_i^r=1"; solver output `toy_resource_unit_cost_c_ir` = 1.0). Toy capability map: φ_X(X⁰, b) = min(3, X⁰ + b).

**Governance regimes** (`04_solver_v1_0.py`). The source defines the letters C, F and D only as parameter sets and **does not name them**, so do not expand them (e.g. not "centralised"):

| Regime | Capacity K_Γ | Risk multiplier | Cost multiplier | Flexibility multiplier |
|---|---:|---:|---:|---:|
| C | 5.5 | 0.85 | 1.10 | 0.95 |
| F | 6.0 | 1.00 | 1.00 | 1.00 |
| D | 6.5 | 1.15 | 0.90 | 1.05 |

In the baseline all five configurations are permitted under every regime.

**Nine baseline scenarios:**

| Governance | Budget | F1 | Realised value | Residual risk | AI adoptions | Configurations (3 processes) |
|---|---:|---:|---:|---:|---:|---|
| C | 3 | 1.708 | 1.560 | 0.268 | 2 | AIAssist ×2, HumanOnly ×1 |
| F | 3 | 1.775 | 1.642 | 0.316 | 2 | AIAssist ×2, HumanOnly ×1 |
| D | 3 | 1.842 | 1.724 | 0.363 | 2 | AIAssist ×2, HumanOnly ×1 |
| C | 5 | 2.158 | 2.221 | 0.451 | 3 | AIAssist ×3 |
| F | 5 | 2.244 | 2.338 | 0.530 | 3 | AIAssist ×3 |
| D | 5 | 2.331 | 2.454 | 0.610 | 3 | AIAssist ×3 |
| C | 7 | 2.158 | 2.221 | 0.451 | 3 | AIAssist ×3 (same as budget 5) |
| F | 7 | 2.244 | 2.338 | 0.530 | 3 | AIAssist ×3 (same as budget 5) |
| D | 7 | 2.616 | 3.286 | 0.736 | 3 | AIAssist ×2, HumanFirstAICheck ×1 |

**Governance permission probe** (C, B = 5):
- restricting configuration permissions lowers F1 from 2.158 to 0.837;
- configurations change from AIAssist ×3 to HumanOnly ×2 + HumanFirstAICheck ×1.

**Selection-threshold sensitivity** (process P2; score 0.65; truth 1):
- at τ ≤ 0.6, P2 uses AIAssist (F1 2.244);
- at τ = 0.7, Level 1 allocates nothing to P2's AI capability and P2 reverts to HumanOnly (F1 1.450).
- The τ probe holds the governance regime and budget fixed at regime F, budget 5. Its F1 at τ ≤ 0.6 (2.244) equals the F/5 baseline.
- In the permission probe (regime C, B = 5), AIAssist is disallowed.

---

## E5. Systematic review of the co-occurrence → hole/gap inference (DIRECT; protocol `paper/review_lit/PROTOCOL.md` v1.0, amendment S1; data `paper/review_lit/data/`)

**Search (OpenAlex, title and abstract, publication date ≥ 2000-01-01; retrieved 2026-11-19; `search_log.json`):**
- Stream S ("structural hole" + co-word / keyword / co-citation / co-occurrence / bibliometric / patent): hits 7, 63, 11, 19, 43, 165 (sum 308); 261 unique records, all kept.
- G1 ("research gap" + "co-word"): 133 records, all kept.
- G2 ("research gap" + "keyword co-occurrence"): 971 hits, 964 after cross-stream deduplication; simple random sample of 120 (seed 20261119).
- G3 (betweenness + "co-word"): 1,146 hits, 1,087 after deduplication; simple random sample of 80 (seed 20261119).
- Screening set 594; 118 without an abstract excluded; 476 screened (S 183, G1 117, G2 110, G3 66).

**Screening (`screening_agreement.json`, `screening_flow.json`):**
- Blind second screen of 119 records (25%): κ 0.361, raw agreement 0.681, 38 disagreements.
- 243 of 476 primary decisions low-confidence. Amendment S1: the adjudicator re-screened 254 records (all disagreements and all low-confidence decisions); 26 reversals.
- Included 204 (S 131, G1 31, G2 25, G3 17); excluded 272.

**Coding reliability (two blind coders on all 204; `coding_agreement.json`):**

| Variable | κ | raw agreement |
|---|---|---|
| D1 relation | 0.739 | 0.809 |
| D2 claim | 0.428 | 0.593 |
| D3 measure | 0.558 | 0.706 |
| F1 | 0.612 | 0.784 |
| F2 | 0.626 | 0.789 |
| F3 | 0.192 | 0.657 |
| F4 | 0.534 | 0.882 |
| V | 0.312 | 0.657 |

182 records had at least one disagreement on D2 or F1–V and were adjudicated. E = abstract for all 204.

**Final codes (`review_results.json`, `included_studies_coded.csv`):**
- D2 claim: hole 99, several 33, broker 3, gap 66, unclear 3. Hole, broker or several: 135 (preregistered "published practice" threshold: ≥ 10).
- D3 measure: constraint 111, position 39, absence 35, none 12, betweenness 7.
- D1 relation: patent 73, mixed 66, coword 42, other 11, coauthorship 6, comembership 2, unclear 4.
- Period: 2000–2014 n = 11; 2015–2019 n = 28; 2020–2026 n = 165.

Prevalence, yes / n with Wilson 95% CI (abstract level; "unclear" counted as not yes):

| | n | F1 projection as flow | F2 Burt/betweenness on co-occurrence | F3 absence as gap, no baseline | F4 label validity unreported | V validation |
|---|---|---|---|---|---|---|
| All | 204 | 100 (0.490; 0.422–0.558) | 96 (0.471; 0.403–0.539) | 60 (0.294; 0.236–0.360) | 178 (0.873; 0.820–0.912) | 92 (0.451; 0.384–0.520) |
| S | 131 | 98 (0.748; 0.667–0.815) | 96 (0.733; 0.651–0.801) | 13 (0.099; 0.059–0.162) | 110 (0.840; 0.767–0.893) | 91 (0.695; 0.611–0.767) |
| G1 | 31 | 0 (0.000; 0.000–0.110) | 0 (0.000; 0.000–0.110) | 19 (0.613; 0.438–0.763) | 30 (0.968; 0.838–0.994) | 1 (0.032; 0.006–0.162) |
| G2 (sample) | 25 | 1 (0.040; 0.007–0.195) | 0 (0.000; 0.000–0.133) | 18 (0.720; 0.524–0.857) | 23 (0.920; 0.750–0.978) | 0 (0.000; 0.000–0.133) |
| G3 (sample) | 17 | 1 (0.059; 0.010–0.270) | 0 (0.000; 0.000–0.184) | 10 (0.588; 0.360–0.784) | 15 (0.882; 0.657–0.967) | 0 (0.000; 0.000–0.184) |

Unclear counts (all 204): F1 9, F2 6, F3 4, F4 20, V 4.

Gap streams G1–G3 combined: n = 73; F2 yes 0; V yes 1. Among the 135 hole, broker or several claims: F1 yes 99, F2 yes 96; among the other 69 studies: F3 yes 46. Hole, broker or several claims by stream: S 131; G1 1; G2 2; G3 1 (G3 also has 3 unclear claims).

By relation (yes counts): patent n = 73: F1 70, F2 72, F3 0, V 63. Coword n = 42: F1 3, F2 5, F3 28, F4 40, V 2.
By claim (yes counts): hole n = 99: F1 77, F2 81, V 81. Gap n = 66: F3 46, F4 62, V 1.

**Coding observation (interpretation, not a code):** of the 91 stream-S studies coded V = yes, 63 are patent-network studies (D1 = patent), and 71 of the 91 titles name an innovation, performance or other outcome effect (title keyword count: innovat / performance / impact / effect / influence / breakthrough / outcome). In these studies V = yes reflects a test of whether a Burt score computed on a co-inventor, co-applicant or co-classification network predicts later outcomes. That checks the score's predictive association; it does not check that the network carries flow.

**Optional replication (protocol §8):** not done in this round.

**Disclosure:** all screeners, coders and adjudicators were LLM subagents (Claude); agreement is between models, not human inter-rater reliability.
