# Preregistration: Is there a structural hole between AI and decision technologies? A US patent-citation test

**Version:** 1.0, frozen 2026-11-18, **before any patent data was downloaded or inspected**. Changes after this date go in a dated amendment section. They must not overwrite this text, and any analysis they add is labelled exploratory.

**Context:** This test belongs to the AI × Decision project (RQ1 motivation for the RQ3/RQ4 multi-level programming model). Earlier corpora measured co-occurrence (literature functions, project co-membership) rather than flows between actors, so they could not test Burt's construct ([data-validity verdict, PR #4](https://github.com/Jimmy0307/ai-decision-ml/pull/4); [round 3 of PR #3](https://github.com/Jimmy0307/ai-decision-ml/blob/research/external-data-mlp-feasibility-20261118/research/external_dataset_poc_20261118/ROUND3_BURT_MULTINETWORK_RESULTS_20261118.md)). Patent citations are directed, dyadic records of prior art that the citing invention builds on. They are the closest public proxy for knowledge flow between technology communities.

## 1. Question and claim boundary

**Question:** Do AI technologies and decision/management technologies cite each other less than comparable technology fields do, after holding grant-year structure and each field's overall citation volume fixed?

**What a positive result would support:** at the level of technology communities, the two are weakly connected relative to their connections elsewhere. That is a *structural hole between technology domains*, used as empirical motivation for RQ3/RQ4.

**What it would not support:**
- a structural hole inside any firm;
- causal claims;
- the 16 V9 depleted cells;
- any parameter value of the multi-level programming model.

## 2. Data

- **Source:** PatentsView granted-patent tables, the current release on the USPTO Open Data Portal (dataset `pvgpatdis`).
- **Files:** `g_patent.tsv.zip`, `g_cpc_current.tsv.zip`, `g_us_patent_citation.tsv.zip`. Optional: `g_assignee_disambiguated.tsv.zip` (H3 only).
- **Provenance:** the SHA-256, size and release date of every file are recorded before analysis.
- **Storage:** raw files stay local and are never pushed. Only aggregate counts are published.

## 3. Population and windows

- **Units:** US utility patents (`patent_type == "utility"`, numeric `patent_id`). Withdrawn patents are excluded.
- **Citing window:** grant years 2010 to the last complete calendar year in the release (Y_end).
- **Cited patents:** any US utility patent in the release.
- **Citation type:** `citation_category`.
  - **Primary:** applicant citations (`cited by applicant`).
  - **Sensitivity:** all categories, including examiner citations. Examiner citations reflect art-unit search practice, not inventor knowledge flow.

## 4. Group definitions

Membership uses every CPC code in `g_cpc_current` (inventive and additional), unless a sensitivity check says otherwise.

| Group | CPC definition | Role |
|---|---|---|
| **AI** | subclass `G06N` | Focal group 1 |
| **DEC** | main groups `G06Q10/04` (forecasting or optimisation) and `G06Q10/06` (resources, workflows, human or project management, enterprise planning, decision analysis), including all their subgroups | Focal group 2 |
| BRIDGE | patents in both AI and DEC | Counted and reported. **Excluded** from the AI–DEC cross counts |
| BIZ-OTHER | `G06Q` main groups other than `G06Q10` (G06Q20, 30, 40, 50, 90, 99) | Control for business-method separation |
| Reference fields R | every CPC main group (e.g. `G06F16`, `H04L67`) in classes G06, G16, H04 with at least 2,000 citing-window patents, excluding anything in `G06N` and `G06Q10` | Comparison distribution |

For any pair of groups (A, B), the cross counts use patents in A but not B, and patents in B but not A.

## 5. Statistic

For a citation c = (i → j), the stratum is s = (grant year of i, grant year of j). Per stratum:
- M(s) is the total number of citations;
- out_A(s) is the number of citations made by patents in A;
- in_B(s) is the number of citations received by patents in B.

The configuration expectation, which holds citing volume, cited volume and grant-year structure fixed, is:

E(A→B) = Σ_s out_A(s) · in_B(s) / M(s)

The **symmetric intensity** is:

OE(A,B) = [O(A→B) + O(B→A)] / [E(A→B) + E(B→A)]

Uncertainty comes from a **Poisson cluster bootstrap over citing patents**: 2,000 replicates, seed 20261118. E is held fixed because the stratum margins come from the whole network.

## 6. Hypotheses and decision rules

**H1 (primary): structural hole between AI and DEC.** It is supported only if **both** of these hold under the primary specification.

- **H1a (relative to comparable fields):** OE(AI, DEC) lies in the lowest quartile of {OE(AI, X) : X ∈ R} **and** in the lowest quartile of {OE(DEC, X) : X ∈ R}.
- **H1b (not explained by business-method separation):** OE(AI, DEC) / OE(AI, BIZ-OTHER) < 1, with the upper bound of the 95% bootstrap CI below 1.

**Verdict labels:**
- Both hold: `HOLE_SUPPORTED`.
- Exactly one holds: `PARTIAL_NOT_CLAIMED`.
- Neither holds: `HOLE_NOT_SUPPORTED`. The structural-hole line ends in this project; structural holes may then be used only as conceptual motivation, not as an empirical claim.

**H2 (secondary): is the hole closing?** Compute OE(AI, DEC) by citing year, with bootstrap CIs, and fit a weighted least-squares slope on citing year.
- `CLOSING` if the slope is > 0 with a 95% CI above 0 **and** OE in the last 3 citing years is at or above the median of R.
- `PERSISTENT` if the slope CI includes 0 or lies below it.
- Otherwise `NARROWING_BUT_OPEN`.

**H3 (exploratory, only if the assignee file is available):** firms holding both AI and DEC patents are candidate brokers. The test is Burt constraint in the assignee-level applicant-citation network, compared with degree-matched firms. This is exploratory; no claim will be made from it.

## 7. Sensitivity analyses

These are reported, but they do not change the H1 verdict.

1. All citation categories (applicant + examiner + other).
2. DEC = all of `G06Q10`.
3. AI broadened: `G06N` + `G06F18` (pattern recognition) + `G06V10/70` (image recognition using ML).
4. Inventive CPC codes only (`cpc_type == "inventive"`).
5. Citing window 2015 to Y_end.
6. BRIDGE patents assigned to both groups instead of being excluded.

The report will state whether each sensitivity agrees with the primary verdict. If at least 4 of the 6 disagree, the primary verdict is labelled `FRAGILE`.

## 8. What will not be done

- No changes to group definitions, windows, reference set or thresholds after data inspection, except as dated, exploratory amendments.
- No search over CPC definitions to find a significant pair.
- No reporting of only the favourable specification.

## 9. Pipeline calibration (synthetic, before real data)

`tests/test_patent_hole.py` builds field-local synthetic citation networks. Every cross-field O/E is below 1 in these networks, so "O/E < 1" alone is not evidence of a hole.

| Planted AI–DEC suppression | OE(AI,DEC) | Lowest quartile of reference fields | OE ratio vs BIZ (95% CI) | Verdict |
|---|---:|---:|---|---|
| none | 0.388 | 0.356 | 0.99 (0.79–1.21) | HOLE_NOT_SUPPORTED |
| 30% | 0.275 | 0.376 | 0.66 (0.52–0.83) | HOLE_SUPPORTED |
| 50% | 0.223 | 0.387 | 0.47 (0.36–0.58) | HOLE_SUPPORTED |

The decision rule does not flag a network with no hole, and it detects a 30% suppression.

