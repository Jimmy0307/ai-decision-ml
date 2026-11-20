# Preregistration 3: Full patent replication of the AI × Decision research lines (V5–V11.1, Gap Validity)

**Version:** 1.0, frozen 2026-11-18.

**Already known when this was written:**
- the aggregate verdict (`HOLE_NOT_SUPPORTED`, OE = 3.05);
- the full-window 6×7 cell results ([RESULTS_V9_MATRIX_20261118.md](RESULTS_V9_MATRIX_20261118.md)).

**Not yet computed when this was written:** none of the modules below (time splits, adapted null, firm network, label audit) had been run. Their rules are fixed here.

**Goal:** re-run every research line of the original project on US patent data, so each version has a patent counterpart with a stated result. Lines that cannot be ported are marked `NOT_APPLICABLE`, with the reason.

**Common settings** (same as Preregistrations 1–2):
- grant years 2010–2025;
- AI = CPC G06N; DEC = G06Q10/04 and G06Q10/06;
- 6 AI-method rows × 7 decision-function columns;
- Part A = co-classification; Part B = applicant citations between AI-only and DEC-only patents;
- engine `src/ra_lib.py`, unchanged.

**"3-test" agreement:** used by P3 and P9. A cell passes when the main MC, exact and raw tests each give q ≤ .05, in the same direction.

## P1. V5/V9 functional matrix (M01–M07), with a patent-adapted M06

Patents violate the swap assumption of the original M06 (amendment B1). The adapted test **M06-P** uses the same idea in a form that patents allow:
- Within each stratum of (number of rows, number of columns) of a document, randomly permute the documents' **column sets**. Each document's row set stays fixed.
- Every document therefore remains a complete row × column block, and both margins are preserved exactly.
- Settings: 5,000 samples, seed 20260919, two-sided empirical p, and BH within the 42 cells.

**Adapted core:** main + exact + M06-P all q ≤ .05 in the same direction. **Adapted full core:** the adapted core plus raw.

Reported for A, for B, and for B with all citation categories. **Convergent core:** an adapted full-core depleted cell in both A and B.

## P2. V9.1 calibration (M10, M11)

- **Seed stability:** main MC with 20 seeds (20260918 + k, k = 0…19). For each cell, report how many seeds give q ≤ .05 and how many cells sit on the boundary (between 1 and 19 seeds).
- **False-positive rate:** 1,000 null matrices from stub permutation of the observed Part A and Part B margins. Count cells reaching q ≤ .05 after exact test + BH. Report the mean false cells per matrix and the share of matrices with any false cell.
- **Power:** take the observed matrix, remove 20% of the edges of one mid-sized cell, and redistribute them evenly across the other cells of the same row. Repeat for each cell with E ≥ 100. Report the share of cells detected (exact + BH, q ≤ .05, depleted).
- **Segmentation (M11):**
  - S1 = inventive CPC codes only;
  - S2 = documents with exactly one row and one column.

  Report the adapted full core for A and B under each, and its overlap with P1.

## P3. Citation-line exploration/confirmation (M08, M09)

- **Part A:** discovery = grants 2010–2017; confirmation = 2018–2025.
- **Part B:** discovery = citing years 2013–2018; confirmation = 2019–2025.
- **Replicated depleted cell:** passes the 3-test rule as depleted in **both** halves of the same part.
- The 3-test rule is used here because M06-P may lack power in half samples. M06-P results are reported too.

## P4. V9 human audit (M12) → label-validity audit

CPC labels are assigned by examiners, so the LLM-coder reliability study has no analogue. Replacement check: for each row and column label, compute the share of its patents whose **title** contains the label's keywords, and the lift over all other AI∪DEC patents.

| Label | Title keywords |
|---|---|
| G06N3 | neural, deep, network |
| G06N5 | knowledge, rule, inference, reasoning, ontology, expert |
| G06N7 | probabil, bayes, fuzzy, stochastic, markov |
| G06N10 | quantum, qubit |
| G06N20 | machine learning, learning, training, model |
| FORECAST_OPTIMISE | forecast, predict, optimi, route |
| RESOURCE_SCHEDULING | resource, schedul, allocat, plan |
| WORKFLOW | workflow, process |
| RISK | risk |
| STRATEGY | strateg, goal, decision |
| PERFORMANCE | performance, evaluat, assess, productiv |

A label passes if lift ≥ 1.5. This is face validity only; it is **not** inter-rater reliability.

## P5. V7/V11 author and co-author SNA (M13) → firm network

- **Nodes:** organisations (assignee types other than individuals, i.e. not 4, 5, 14 or 15) holding at least one AI or DEC patent granted 2010–2025.
- **Firm group:**
  - `AI_FIRM`: only AI-only patents;
  - `DEC_FIRM`: only DEC-only patents;
  - `MIXED`: both, or any bridge patent.
- **Edges:** undirected, weighted by the number of applicant citations between the firms' AI∪DEC patents. Self-citations within a firm are excluded.
- **Measures:** Burt constraint and effective size (networkx, weighted).
- **(a) Firm-level hole:** O/E of AI_FIRM ↔ DEC_FIRM tie weight under a degree-preserving (strength-proportional) expectation. A hole is indicated only if O/E < 1 and lower than the O/E of both AI_FIRM↔MIXED and DEC_FIRM↔MIXED.
- **(b) Broker test:** median constraint of MIXED firms vs a degree-matched null. Group labels are permuted among firms within strength deciles, 1,000 replicates, seed 20261118. `MIXED_LOWER_CONSTRAINT` if the one-sided p is below .05.
- **Candidate brokers:** the 10 MIXED firms with the lowest constraint among firms with degree ≥ 5.

## P6. V10.1 removal falsification / Gap M17 alternative paths

Remove the 10 candidate brokers, together and one at a time. Report:
- the share of AI_FIRM↔DEC_FIRM tie weight that remains;
- whether any path still connects AI_FIRM and DEC_FIRM firms;
- the size of the largest connected component containing both groups.

A candidate is refuted as an indispensable broker if, after its removal, AI_FIRM and DEC_FIRM firms remain connected. This mirrors V10.1.

## P7. V10 higher-order network (M14) → co-assignment hyperedges

Patents with at least 2 organisation assignees, within the AI∪DEC set. Report, descriptively:
- the number of hyperedges;
- the share that join an AI_FIRM with a DEC_FIRM or a MIXED firm;
- the size distribution.

## P8. V11.1 identity validation (M15)

For the top-10 broker candidates and the 50 firms with the largest strength, check whether any two `assignee_id`s share a normalised organisation name (case-folded, punctuation and corporate suffixes removed). Report the collision count. This counts possible aliases only; nothing is corrected.

## P9. Gap Validity (M16–M19) on the 6×7 network

- **M16:** constraint of each row and column node in the weighted bipartite cell network, split into its dyadic and indirect parts. The indirect part is 0 by construction in a strict bipartite graph, and this is reported as such.
- **M17:** for each P1 depleted cell (adapted full core, or 3-test agreement if the core is empty), count alternative length-3 routes r–c′–r′–c through non-zero cells.
- **M18:** depleted-cell counts at q ≤ .01 vs q ≤ .05.
- **M19:** covered by the P2 null and power simulations.

## P10. Limitation Scout (M20)

`NOT_APPLICABLE`. Patents have no limitations or future-work section, and full texts were not downloaded.

## Reporting and claims

- Every module is reported in a table: version → patent analogue → result → claim allowed.
- No module may relabel a depleted cell as a "Burt structural hole".
- The aggregate verdict from Preregistration 1 stands, whatever any module shows.
