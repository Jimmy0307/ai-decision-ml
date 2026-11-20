# Preregistration 10: co-occurrence vs flow in the scholarly literature (OpenAlex subfields)

**Status:** frozen 2026-11-20, before any OpenAlex co-occurrence or citation count for this plan was retrieved. The commit timestamp is the freeze record. A capability check returned three sampled works and two group counts for one year; these were used only to confirm the API fields. Changes after the freeze are dated amendments below the text.

**Known when written:**
- Plans 1–8 and Plan C, and the design of Plan 9, whose run is pending.
- In patents:
  - a co-occurrence gap marks a flow gap in 66.8% of field pairs (reversal 7.0%, MODERATE);
  - the taxonomy hypothesis (Plan 8) was not supported;
  - post hoc, neighbouring subclasses were least reliable.
- This plan is **data-informed**: it answers the objection that patents are not literature. The project's original inference was drawn from literature co-occurrence.

**Question:** in the scholarly literature, how often does sparse co-occurrence of two research areas (co-assignment of their topics to the same work) coincide with sparse citation flow between them? Does the neighbour pattern hold?

## 1. Units and data (OpenAlex, retrieved on the run date; the dates are logged)

**Fields:** the 252 OpenAlex subfields. A work belongs to every subfield of its assigned topics (up to three topics).

**Taxonomic level:**
- level 2: same field, different subfield (neighbours);
- level 3a: different field, same domain;
- level 3b: different domain.
- There is no level 1. Level 3 = 3a ∪ 3b.

**Co-occurrence (full population, via the `group_by` API):**
- Universe: works of type `article` published 2015–2024 with at least one topic.
- n_S: number of works in subfield S. n_ST: number of works in both S and T. N: universe size.
- OE_co = n_ST · N / (n_S n_T).
- Retrieved with one grouped query per subfield.

**Flow (random sample):**
- **Citing works:** a random sample of works of type `article` published 2015–2024 with at least one topic and at least one reference. The OpenAlex `sample` parameter is used with seeds 1, 2, … until 100,000 distinct citing works are reached or the request budget (§4) runs out. Each seed draws 10,000.
- **References:** each referenced work is looked up for its publication year and topics. A citation counts if both ends have at least one subfield.
- **Strata:** s = (citing year, cited year). M(s) = sampled citations in s.
- **Counts:** O_AB = citations from works in A \ B to works in B \ A.
- **Expected:** E_AB = Σ_s out_{A\B}(s) · in_{B\A}(s) / M(s). This is Plan 7's formula, computed with the sparse code verified in Plan 9.
- OE_flow = (O_AB + O_BA) / (E_AB + E_BA).

**Eligibility:** E_co ≥ 5 and E_flow ≥ 5.

## 2. Tests (Plan 7–9 rules, unchanged)

**L7 (literature replication of Plan 7):**
- C-gap / F-gap = lowest quartile among eligible pairs.
- Report PPV, reversal rate and Spearman ρ.
- Cluster bootstrap over subfields: 1,000 replicates, seed 20261119.
- Label:
  - RELIABLE if PPV ≥ 0.80 and reversal ≤ 0.05;
  - UNRELIABLE if PPV < 0.50 or reversal ≥ 0.20;
  - MODERATE otherwise.
- Secondary: S1 absolute cut-points (OE ≤ 0.5 on both measures); S3 eligibility at E ≥ 20.

**L9 (neighbour hypothesis, confirmatory):**
- **L9a:** PPV(level 2) − PPV(level 3) < 0 (95% CI entirely below 0).
- **L9b:** reversal(level 2) − reversal(level 3) > 0 (CI entirely above 0).
- **Overall:** SUPPORTED if both hold; PARTIAL if one; NOT_SUPPORTED if neither; REVERSED if either CI is entirely on the opposite side.

**L8 (descriptive):** mean divergence Δ (percentile rank of OE_flow minus that of OE_co) by level 2 / 3a / 3b, and the OLS of Δ on level indicators with Plan 8's controls.

**AI and decision in the literature (descriptive):**
- Report OE_co, OE_flow and gap membership for the pairs formed by the subfield "Artificial Intelligence" with:
  - "Management Science and Operations Research";
  - "Strategy and Management";
  - "Information Systems and Management";
  - "Management Information Systems".
- Use the exact display names; any of them missing in OpenAlex is reported as missing.
- This gives the literature analogue of the Study 1 premise.

## 3. Reading

- All labels are reported whatever they are.
- If L7 is RELIABLE, the manuscript must say that, in the literature, co-occurrence gaps track flow well, and must narrow its claims.
- If L9 is supported, the neighbour pattern is reported as replicated in literature data.

## 4. Retrieval rules (no authentication; no personal data sent)

- Anonymous requests only: no API key, and no e-mail sent to OpenAlex.
- At most 3 requests per second, and at most 60,000 requests per calendar day.
- Exponential back-off on HTTP 429 or 5xx.
- If the server keeps refusing requests (more than 20 consecutive failures), the run stops and is reported. Any change of retrieval method is recorded as an amendment.
- Every response is cached on disk, so the run resumes.
- Only aggregate tables and work identifiers are committed (OpenAlex data are CC0). No abstracts.

**Code:**
- `openalex_fetch.py`: retrieval and aggregation.
- `openalex_analyse.py`: L7, L8, L9 and the AI × decision location.

## Amendments (dated; the text above is unchanged)

**R10-A1, 2026-11-20, recorded before any co-occurrence row was completed and before any flow data were retrieved.**
- **What happened:** the first grouped co-occurrence query needed a second page. OpenAlex returned HTTP 401 for anonymous cursor paging, so the run stopped as designed.
- **Change in retrieval only** (the definitions of n_S, n_ST and N are unchanged):
  - For each subfield S, the first page of `group_by=topics.subfield.id` is retrieved without a cursor. These are the 200 largest co-assigned subfields, with exact counts.
  - For every subfield T not in that page and not already known from T's own row, n_ST is retrieved as the count of works matching `topics.subfield.id:S+T`.
- **Values seen while checking the syntax:**
  - n(Artificial Intelligence, 1702) = 1,120,805;
  - n(1803) = 875,053;
  - n(1702 and 1803) = 60,128.
  - No other co-occurrence count was seen.
