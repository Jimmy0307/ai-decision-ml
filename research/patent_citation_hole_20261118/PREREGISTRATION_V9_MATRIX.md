# Preregistration 2: the V9 test battery on a patent AI-method × decision-function matrix

**Version:** 1.0, frozen 2026-11-18. It was written **after** the aggregate test in [PREREGISTRATION.md](PREREGISTRATION.md) returned `HOLE_NOT_SUPPORTED` (OE = 3.05), and **before** any cell-level count of the matrix below was computed. This is a separate, follow-up analysis. It does not change or replace the aggregate verdict.

**Purpose:** To apply the same calculation as the V9 literature analysis to patents, so the two can be compared method for method. The question is whether, inside an overall strongly connected AI–decision relationship, particular AI-method × decision-function combinations are under-represented.

## 1. Engine

The engine is `src/ra_lib.py`, a byte-identical copy (SHA-256 `09c3d60c…bc33`) of the Route A engine published in PR #4 (`tools/route_a_20261118/ra_lib.py`). That engine reproduces the official V9 exact and raw tests (|Δq| ≤ 6e-12). It is used unchanged, with the V9 settings:

| V9 method | Setting |
|---|---|
| M04 main fixed-degree stub Monte Carlo | R = 10,000, seed 20260918 |
| M05 exact hypergeometric | analytic |
| M06 document-preserving within-document swap | 5,000 samples, burn-in 43,600, thin 4,360, seed 20260919 |
| M07 raw-record exact test | non-deduplicated code-level records |
| BH-FDR | within each matrix (42 cells) for each test |
| **Structural core** | q ≤ .05 in main + exact + document-preserving, all in the same direction |
| **Full core** | structural core plus raw q ≤ .05 in the same direction |

## 2. Cells (fixed in advance from the CPC scheme, not from data)

**Rows (AI method, CPC G06N main groups):**
- `G06N3`: biological models, including neural networks;
- `G06N5`: knowledge-based models;
- `G06N7`: specific mathematical models, e.g. probabilistic or fuzzy;
- `G06N10`: quantum computing;
- `G06N20`: machine learning;
- `G06N_OTHER`: any other G06N code.

**Columns (decision function, G06Q10).** Each code is assigned to the first matching rule:

| Column | Codes |
|---|---|
| `FORECAST_OPTIMISE` | `G06Q10/04*` |
| `RESOURCE_SCHEDULING` | `G06Q10/0631*` |
| `WORKFLOW` | `G06Q10/0633*` |
| `RISK` | `G06Q10/0635*` |
| `STRATEGY` | `G06Q10/0637*` |
| `PERFORMANCE` | `G06Q10/0639*` |
| `MGMT_GENERAL` | any other `G06Q10/06*` (e.g. /06, /063, /067) |

That gives 6 × 7 = **42 cells**. Codes in G06Q10/08, /10, /20 and /30 are not part of the DEC definition and are ignored.

## 3. Two matrices

**Part A: co-classification, the direct V9 analogue.**
- **Document:** a US utility patent granted 2010–2025 that carries at least one row code and at least one column code (an AI × decision patent).
- **Edge:** a unique (patent, row, column) combination, as in V9's document-level deduplication (M03).
- **Raw record:** each (AI code, DEC code) symbol pair on the patent.

**Part B: citation flow, the knowledge-flow analogue.**
- **Document:** a citation between an AI-only patent and a DEC-only patent, in either direction. AI-only means G06N but not G06Q10/04 or /06; DEC-only means G06Q10/04 or /06 but not G06N.
- **Citation scope:** as in the aggregate test, citing years 2010–2025 and **applicant citations** (which in practice covers 2013–2025; see amendment A2).
- **Edge:** a unique (citation, row of the AI-side patent, column of the DEC-side patent) combination.
- **Raw record:** each code-pair combination.

**Sensitivity (reported, does not change the verdict):** Part B using all citation categories (2010–2025).

## 4. What is reported and how it is read

1. **Every** cell, depleted and enriched alike, with O, E, O/E and the q value and direction for every test.
2. **Convergent depletion:** a cell that is a full-core *depleted* cell in **both** Part A and Part B.
3. **Allowed reading of a depleted core cell:** "this AI-method × decision-function combination is under-represented relative to its margins in patents". This is directional under-integration at the cell level, the same claim level V9 can support. It is **not** called a Burt structural hole, and it does not override the aggregate result (AI and DEC overall are strongly connected, OE = 3.05).
4. There is no mapping between V9's LLM-coded families and CPC groups, so V9 and patent cells are **not** matched one to one. Only the overall pattern is compared: how many cells are depleted or enriched, and how they are distributed.
5. No other granularity, row or column definition, window or citation type will be substituted after results are seen. Any extra analysis will be labelled exploratory.
