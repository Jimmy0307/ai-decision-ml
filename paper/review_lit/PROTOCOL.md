# Protocol: How often do published studies infer structural holes or gaps from co-occurrence networks?

**Version:** 1.0, frozen 2026-11-19, before any search result was retrieved beyond the hit counts used to size the streams. The protocol is committed to the project repository; the commit timestamp is the freeze record.

**Purpose:** The manuscript shows, within one project, that inferring a Burt structural hole or a "gap" from co-occurrence or affiliation data is invalid, and it documents four failure modes. This review asks whether that inference is a published practice, and how often published studies show those failure modes. It is a **descriptive** systematic review. It tests no hypothesis.

## 1. Source and search

- **Database:** OpenAlex (`api.openalex.org`), searched in title and abstract (`title_and_abstract.search`). Filter: publication date ≥ 2000-01-01, any work type that has an abstract. Retrieved on the day the search runs; the date and the full query strings are recorded.
- **Stream S (structural-hole claims), all records:** "structural hole(s)" AND one of: "co-word", "keyword", "co-citation", "co-occurrence", bibliometric, patent.
- **Stream G (gap and broker claims from co-word or keyword networks):**
  - G1: "research gap(s)" AND "co-word". All records.
  - G2: "research gap(s)" AND "keyword co-occurrence". A simple random sample of 120 (seed 20261119).
  - G3: betweenness AND "co-word". A simple random sample of 80 (seed 20261119).
- Records are deduplicated by OpenAlex id, then by DOI. A record found in more than one stream is kept once and assigned to the first stream in the order S, G1, G2, G3.

## 2. Eligibility (title and abstract)

**Include** if both hold:
- **(a)** The study builds or analyses a network from co-occurrence or affiliation relations: keyword or co-word co-occurrence, co-citation, bibliographic coupling, co-authorship, patent co-classification or co-assignment, project co-membership, or similar.
- **(b)** From that network's structure it draws at least one substantive inference of these kinds:
  - a structural hole or Burt-type brokerage;
  - a broker or bridge node or topic (e.g. via betweenness);
  - a research gap, missing link, white space, or under-connected opportunity.

**Exclude:**
- networks of directed flows only (citations treated as directed links, communication or transaction networks);
- purely methodological papers that make no substantive claim;
- studies whose gap statements are not derived from network structure (e.g. "future research is needed" without a structural argument);
- no abstract available;
- not in English.

## 3. Coding scheme (for included studies; from title and abstract, and from open-access full text where a coder can access it)

| Variable | Values |
|---|---|
| D1 relation type | co-word/keyword; co-citation/coupling; co-authorship; patent co-classification/co-assignment; other co-occurrence; mixed |
| D2 claim type | structural hole (Burt); broker/bridge (betweenness or similar); research gap / missing link / opportunity; several |
| D3 measure named | Burt constraint / effective size; betweenness or brokerage roles; absence or weakness of links / sparse region; cluster or map position; none stated |
| **F1 projection read as flow or structure** | yes / no / unclear: co-occurrence or projected ties are interpreted as relations through which information or knowledge flows, or which create brokerage positions |
| **F2 constraint or betweenness on co-occurrence networks** | yes / no / unclear: a Burt measure or betweenness is computed on a (projected) co-occurrence network and read as brokerage or a hole |
| **F3 absence read as a gap without a baseline** | yes / no / unclear: low or absent co-occurrence is read as a gap or hole, with no null model, expected count or comparison set reported |
| **F4 label validity unreported** | yes / no / unclear: node labels come from automated or manual term extraction or classification, and no reliability or validation is reported |
| V validation | yes / no / unclear: the claimed hole or gap is checked against independent evidence (e.g. later outcomes, flow data, expert validation) |
| E evidence basis | abstract only; open-access full text |

F1–F4 operationalise the manuscript's failure modes:
- F1 corresponds to projection cliques;
- F2 to the bipartite or projection degeneration of constraint;
- F3 to the central absence-as-gap inference;
- F4 to model-inferred or unvalidated labels.

Same-term self-pairing (a fourth mode in the manuscript) cannot be judged from abstracts. It is not coded.

## 4. Procedure and reliability

1. **Screening:**
   - A primary screener (an LLM subagent) screens every record against section 2 and records its decision with a reason.
   - A second, independent screener screens a random 25% of records (seed 20261119), blind to the first decision.
   - Cohen's κ on include/exclude is reported.
   - Disagreements in the overlap set are resolved by a third reviewer.
2. **Coding:**
   - Two independent coders code **every** included study on D1–D3, F1–F4, V and E, blind to each other.
   - Cohen's κ is reported per variable.
   - Disagreements are resolved by a third reviewer. The resolved codes are the result.
3. **Disclosure:** all screeners and coders are LLM agents. Agreement between models is **not** human inter-rater reliability, and the manuscript will say so.

## 5. Outputs (pre-specified)

- The PRISMA-style flow: records found, deduplicated, screened and included, by stream.
- Among included studies, the share with each of F1–F4 and V, with Wilson 95% CIs. For stream S and G1 (complete) the share is over that stream. For G2 and G3 the shares are sample estimates; they are reported separately, and no inverse-probability weighting is applied.
- Breakdown by D1, D2 and year (2000–2014, 2015–2019, 2020–2026).
- κ for screening and per coding variable.
- A list of included studies: bibliographic metadata and codes only, without abstracts.

## 6. Reading rules

- "The inference is a published practice" is supported if at least 10 included studies draw a structural-hole or broker claim (D2) from a co-occurrence network.
- Shares of F1–F4 are descriptive prevalence estimates **at the abstract level**. "Unclear" counts are reported, not imputed. A study coded "no" on F3 may still fail in ways an abstract cannot show.
- No claim about any individual study's validity is made beyond its codes. Studies are reported as instances of a practice, not as errors to be named in the text.

## 7. Data handling

- Abstracts and any full texts are copyrighted. They stay in a local working folder and are **not** committed.
- The repository receives: query strings, the retrieval date, OpenAlex ids/DOIs/titles/years/venues, screening and coding decisions, κ, and the results.

## 8. Optional (exploratory, if feasible)

Re-run the manuscript's diagnostic on one published case whose network data are openly available: an observed-versus-expected comparison against a degree-preserving null, plus a check of projection closure. If no case has open data, this is reported as not done.

## Amendments (dated; the text above is unchanged)

**S1, 2026-11-19, recorded after screening and before adjudication or coding.**
- **What happened:** the blind 25% double-screen gave κ = 0.361 (raw agreement 0.681; 38 disagreements in 119 records). 243 of the 476 primary decisions were marked low-confidence (105 of the 216 primary inclusions).
- **Main source of disagreement:** studies that compute Burt structural-hole measures on co-patenting or co-authorship networks and use them as predictors. The primary screener included them; the second screener excluded them as "no structural inference". The original guide already lists co-patenting/co-assignment and co-authorship under (a) and Burt-type measures under (b), so such studies meet the criteria.
- **Change:**
  - The adjudicator re-screens **all 38 disagreements and all 243 low-confidence primary decisions**, not only the overlap disagreements.
  - The adjudicator applies the unchanged guide plus the clarifying note above.
  - High-confidence primary decisions outside the overlap stand.
- **Reporting:** κ = 0.361 is reported as observed. Screening reliability is a limitation of the review.
