# Plan C: Where does AI–decision integration occur? (exploratory, descriptive)

**Status:** frozen 2026-11-19 before any of the quantities below were computed. The commit timestamp is the freeze record. The plan is **exploratory and descriptive**. It tests no hypothesis and cannot change any verdict of Plans 1–5.

**Motivation:** Plans 1–5 show what the AI–decision relation is *not*: no knowledge-flow hole at the domain level. Plan C describes what it *is*: in which technologies, inside or between which organisations, and how over time the AI–decision connection is carried.

## Data (all already built; no new download)

- **`outputs/firm_model_LOCAL.pkl`** (built by `src/firm_null.py` from the Plan 3 cache). It holds:
  - the 127,114 in-scope patents (AI = CPC G06N; DEC = G06Q10/04 or G06Q10/06; grant year ≥ 2010);
  - their type (AI only, DEC only, BRIDGE = both);
  - grant year;
  - non-individual owners (disambiguated assignees);
  - owner group (AI_FIRM, DEC_FIRM, MIXED as in Plan 3 P5);
  - the 162,339 applicant citations among them.
- Existing result files, used only for summaries (no recomputation):
  - `SUITE_P1_B_CELLS.csv` (Plan 3, CPC 6×7 applicant-citation cells);
  - `PATENT_HOLE_RESULTS.json` (Plan 1, yearly OE and H2 trend);
  - `PLAN5_CONSTRUCT_RESULTS.json` (Plan 5, /04 vs /06).

## Quantities (pre-specified)

**C1. Artefact-level integration (co-classification; descriptive only, not flow).**
- For each grant year 2010–2025: the number of BRIDGE patents, and their share of all in-scope patents.
- The whole-period total and share.

**C2. Locus of cross-domain flow.**
- A *cross citation* is an applicant citation between an AI-only and a DEC-only patent (either direction).
- A *bridge citation* is one with a BRIDGE patent at either end.
- Among cross citations, report the share in each of these, mutually exclusive in this order:
  - **(i) within-firm:** citing and cited share at least one owner;
  - **(ii) between-firm, MIXED citing:** both ends owned, no shared owner, and at least one citing owner is MIXED;
  - **(iii) between-firm, specialist citing:** as (ii), but no citing owner is MIXED;
  - **(iv) unowned end:** at least one end has no non-individual owner.
- The same shares for all citations within the in-scope set serve as a reference.
- Also report the share of all in-scope citations that are cross citations and that are bridge citations.

**C3. Who carries the cross-domain flow.**
- Credit each between-firm cross citation once to each owner of the citing patent.
- Report the share of that credit held by:
  - the top 10 firms;
  - the top 1% of firms (by credit);
  - each owner group.
- For comparison, report the share of in-scope patents owned by each owner group.
- Firm names are not reported.

**C4. Technology locus (summary of Plan 3 cells; no new computation).**
- From the 6×7 applicant-citation matrix: the three cells with the highest and the three with the lowest O/E among cells with expected count ≥ 100.
- The /04 vs strict-/06 OE from Plan 5.

**C5. Time (summary of Plan 1; no new computation).**
- Yearly OE range, H2 slope and label.
- For C1 and C2, also the shares for 2013–2018 vs 2019–2025.

## Reporting rules

- **Exploratory.**
  - No p-values.
  - Shares are reported with counts.
  - Wilson 95% intervals are given only as a description of binomial uncertainty. They ignore clustering by patent and firm.
- **Wording.**
  - Co-classification (C1) is never described as flow.
  - Within-firm citation share (C2) is a description of where citations occur. It is not evidence about organisational mechanisms.
  - Statements such as "integration is organisational" are not supported by these data and will not be made.
- **Use in the manuscript.**
  - Results enter the manuscript as an exploratory subsection, labelled as such.
  - Any quantity not listed above is reported, if at all, as post hoc.
