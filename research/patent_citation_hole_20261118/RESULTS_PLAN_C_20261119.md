# Results: Plan C, the locus of AI–decision integration (exploratory, descriptive)

- **Plan:** `PLAN_C_DESCRIPTIVE.md`, frozen in 969e60b before computing.
- **Script:** `src/plan_c_descriptive.py`.
- **Output:** `results/PLAN_C_RESULTS.json`.
- **Scope:** 127,114 in-scope patents (AI only 89,613; DEC only 32,185; BRIDGE 5,316), 14,600 owning firms and 162,339 applicant citations among the patents. No p-values. The Wilson intervals in the JSON ignore clustering.

## C1 Artefact-level integration (co-classification; not flow)

- BRIDGE patents (classified in both G06N and G06Q10/04 or /06) are 5,316 of 127,114, a share of 0.0418.
- The share rose from 0.0126 (2010) to a peak of 0.0514 (2023). It was 0.0449 in 2024 and 0.0407 in 2025.
- By period:
  - 2013–2018: 547 of 19,185 (0.0285);
  - 2019–2025: 4,669 of 101,641 (0.0459).

## C2 Locus of cross-domain flow

**Cross citations:**
- Cross citations (AI-only ↔ DEC-only, applicant) are 22,796 of 162,339 in-scope citations (0.1404).
- By direction: AI cites DEC 15,999; DEC cites AI 6,797. These are raw counts, not normalised for the different numbers of AI and DEC patents.
- By period:
  - 2013–2018: 1,785 of 16,524 (0.108);
  - 2019–2025: 21,011 of 145,815 (0.1441).
- No in-scope applicant citation has a citing grant year before 2013.

**Bridge citations:** citations with a BRIDGE patent at either end are 16,194 (0.0998).

Locus (mutually exclusive, in order):

| | Cross citations (n = 22,796) | All in-scope citations (n = 162,339) | Bridge citations (n = 16,194) |
|---|---|---|---|
| Within firm (shared owner) | 4,249 (0.1864) | 47,320 (0.2915) | 3,305 (0.2041) |
| Between firms, a MIXED firm citing | 14,636 (0.6420) | 78,306 (0.4824) | 11,305 (0.6981) |
| Between firms, specialists citing | 2,624 (0.1151) | 28,155 (0.1734) | 652 (0.0403) |
| An end without a non-individual owner | 1,287 (0.0565) | 8,558 (0.0527) | 932 (0.0576) |

Cross-citation locus by period:

| | Within firm | Between, MIXED citing | Between, specialists citing | Unowned end |
|---|---|---|---|---|
| 2013–2018 | 303 (0.1697) | 1,044 (0.5849) | 331 (0.1854) | 107 (0.0599) |
| 2019–2025 | 3,946 (0.1878) | 13,592 (0.6469) | 2,293 (0.1091) | 1,180 (0.0562) |

## C3 Who carries between-firm cross citations

- Credit (one unit to each owner of the citing patent): 17,372 units, held by 1,247 firms.
- **Concentration:**
  - the top 10 firms hold 0.3924;
  - the top 1% of credited firms (13) hold 0.4284.
- **Credit share by owner group:** MIXED 0.8483, AI_FIRM 0.1057, DEC_FIRM 0.0460.
- **Reference, share of patent–owner pairs:** MIXED 0.7412, AI_FIRM 0.1920, DEC_FIRM 0.0669.
- **Firms by group:** AI_FIRM 7,942, DEC_FIRM 4,213, MIXED 2,445.
- 4,086 patents (0.0321) have no non-individual owner.

## C4 Technology locus (summary of Plan 3 cells; O/E relative to the margins of the AI × DEC matrix, not to all fields)

29 cells have an expected count of at least 100.

| | AI family | DEC family | O/E | Three-test agreement |
|---|---|---|---|---|
| Highest | G06N20 | RISK | 1.331 | ENRICHED |
| | G06N7 | STRATEGY | 1.287 | ENRICHED |
| | G06N3 | FORECAST_OPTIMISE | 1.170 | ENRICHED |
| Lowest | G06N3 | RISK | 0.695 | DEPLETED |
| | G06N7 | RISK | 0.701 | DEPLETED |
| | G06N5 | RISK | 0.848 | DEPLETED |

## Reading (descriptive; the plan's wording rules apply)

- **Growth:** the AI–decision connection in US patents is growing at the artefact level (co-classification) and in citation share.
- **Locus:**
  - Cross-domain citations occur between firms more often than citations generally do.
  - The citing firm usually holds both kinds of patent.
  - Credit is concentrated: 13 firms hold 0.4284.
  - Cross-domain citations are less often within-firm than in-scope citations overall (0.1864 vs 0.2915).
  - That last gap is a post hoc observation with no baseline that holds firm portfolios fixed. It is not evidence of an organisational boundary inside firms. It is a candidate question for Study 3.
- **Risk column is heterogeneous:** within the AI × DEC matrix it is the most enriched cell with G06N20 (machine learning) and the most depleted cells with G06N3 and G06N7.
