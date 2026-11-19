# Systematic review: the co-occurrence → structural-hole / gap inference

Preregistered, descriptive review (protocol `PROTOCOL.md` v1.0, frozen 2026-11-19; amendment S1). It asks how often published studies infer a structural hole, a broker or a gap from co-occurrence or affiliation networks, and how often they show the manuscript's failure modes. Reported in the manuscript as Section "How Common Is the Inference? A Systematic Review" (`paper/en/studies.tex`, label `sec:review`; ZH `zh:sec:review`) and Appendix `app:review`.

## Headline results (all from `data/review_results.json`)

| | n | F1 projection read as flow | F2 Burt/betweenness on co-occurrence | F3 absence as gap, no baseline | F4 label validity unreported | V validated |
|---|---|---|---|---|---|---|
| All | 204 | 0.490 | 0.471 | 0.294 | 0.873 | 0.451 |
| S (complete) | 131 | 0.748 | 0.733 | 0.099 | 0.840 | 0.695 |
| G1 (complete) | 31 | 0.000 | 0.000 | 0.613 | 0.968 | 0.032 |
| G2 (sample) | 25 | 0.040 | 0.000 | 0.720 | 0.920 | 0.000 |
| G3 (sample) | 17 | 0.059 | 0.000 | 0.588 | 0.882 | 0.000 |

Wilson 95% CIs are in the JSON and in the manuscript table.

- **Published-practice criterion met:** 135 of the 204 included studies draw a structural-hole or broker claim (threshold ≥ 10). 111 name Burt constraint or effective size.
- **Two practices:**
  - Stream S computes Burt measures on projected (mostly patent co-inventor or co-applicant) networks, reads them as brokerage, and relates them to later outcomes. V there means predictive association, not evidence of flow.
  - The gap streams read sparse co-occurrence as a gap without a baseline and almost never validate it (1 of 73).
- **Reliability:**
  - Screening κ = 0.361.
  - Coding κ ranges from 0.192 (F3) to 0.739 (D1).
  - All screeners, coders and adjudicators were LLM subagents; this is not human inter-rater reliability.
- **Not done:** the optional replication on an open-data published case (protocol §8).

## Files

- `PROTOCOL.md`: frozen protocol plus amendment S1.
- `SCREENING_GUIDE.md`, `CODING_GUIDE.md`: the instructions given to screeners and coders.
- `data/search_log.json`: query strings, hit counts, deduplication and sampling, retrieval date.
- `data/screening_set_meta.csv`: the 594 screened-set records (OpenAlex id, DOI, year, venue, title; **no abstracts**).
- `data/screening_agreement.json`, `data/screening_flow.json`, `data/screening_final.csv`: screening κ, the flow, and the final include/exclude decisions.
- `data/coding_agreement.json`: per-variable κ and raw agreement.
- `data/review_results.json`, `data/included_studies_coded.csv`: final codes and prevalence tables (metadata and codes only).
- `scripts/`: search, batching, merging and result scripts.
  - They were run in a local working folder that also held the abstracts (`*_LOCAL*`), the cached OpenAlex responses and the per-coder CSVs.
  - Those are not committed, because abstracts are copyrighted and coder notes paraphrase them.
  - The scripts expect that layout.
