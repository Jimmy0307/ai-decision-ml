# Preregistration 5: Construct-validity checks for the domain-level verdict

**Version:** 1.0, frozen 2026-11-19, before any of the analyses below were computed.

**Status: data-informed follow-up.** These checks were requested by the manuscript's round-2 review after the Plan 1 verdict (`HOLE_NOT_SUPPORTED`, OE = 3.05) was known. They test whether that verdict depends on two construct choices. Only the definitions, reference sets and decision rules are frozen here; the questions themselves were shaped by known results.

## Questions

- **CV1, class overlap.** DEC = G06Q10/04 (forecasting or optimisation) + G06Q10/06 (resources, workflow, management, decision analysis). Methodologically, /04 overlaps with AI. Does the verdict hold when DEC is restricted to **G06Q10/06** only?
- **CV2, reference granularity.** H1a compared DEC, a pair of subgroup families, with 179 CPC **main groups**. Does H1a still fail when the reference fields are built at the **same granularity** as DEC?

## Definitions (everything else as in Plan 1)

- **Data and scope:**
  - same data and citation scope: US utility patents, citing grant years 2010–2025, applicant citations;
  - same time-stratified configuration expectation and symmetric OE;
  - bridge patents excluded from cross counts;
  - Poisson cluster bootstrap over citing patents (2,000 replicates, seed 20261118);
  - AI = CPC G06N (unchanged).
- **DEC06:** any CPC code matching `^G06Q10/06`. **DEC04:** `^G06Q10/04`, reported descriptively only.
- **Subgroup-family reference set (`sub2`).**
  - Family key = CPC main group + "/" + the first two characters of the subgroup number (e.g. `G06F16/24…` → `G06F16/24`; `G06Q10/0631` → `G06Q10/06`). This is exactly how DEC's components are built.
  - Families in CPC classes G06, G16 and H04 with at least 2,000 patents granted 2010–2025 (Plan 1's threshold).
  - Excluded: families in G06N and every family starting `G06Q10`.
- **Main-group reference set (`all`):** as in Plan 1, i.e. main groups with at least 2,000 patents, excluding G06N and G06Q10.
- **BIZ (H1b comparator):** unchanged. G06Q excluding G06Q10.

## Specifications

| Id | DEC | Reference set | Role |
|---|---|---|---|
| P5a | DEC06 | main groups (`all`) | CV1 |
| P5b | DEC (04 + 06) | subgroup families (`sub2`) | CV2 |
| P5c | DEC06 | subgroup families (`sub2`) | CV1 + CV2 |
| P5d | DEC04 | main groups (`all`) | descriptive only |

## Decision rules

For each of P5a–P5c, apply Plan 1's rule unchanged:
- `HOLE_SUPPORTED` if H1a and H1b both hold;
- `PARTIAL_NOT_CLAIMED` if exactly one holds;
- `HOLE_NOT_SUPPORTED` if neither holds.

Here H1a = OE(AI,DEC) in the lowest quartile of {OE(AI,X)} and of {OE(DEC,X)}, and H1b = the upper bound of the 95% CI of OE(AI,DEC) / OE(AI,BIZ) is below 1.

**Construct-validity verdict:**
- **`ROBUST_TO_CONSTRUCT`** if P5a, P5b and P5c all give `HOLE_NOT_SUPPORTED`. The domain-level verdict then does not depend on the /04 overlap or on reference granularity.
- **`CONSTRUCT_SENSITIVE`** if any of P5a–P5c gives `PARTIAL_NOT_CLAIMED` or `HOLE_SUPPORTED`. The manuscript must then restrict the domain-level claim to the construct under which it holds and report the change.

Also reported, without bearing on the verdict:
- the percentile ranks of OE(AI,DEC) within each reference distribution;
- the reference medians;
- the number of reference fields;
- OE(AI,DEC04) from P5d.

## Implementation note

The code reuses `src/patent_hole.py` (`run_spec`, unchanged statistics). The only change is the reference-exclusion rule, which now drops every reference name beginning `G06Q10`, so that subgroup families of G06Q10 are excluded too. For main groups this is identical to Plan 1's rule.
