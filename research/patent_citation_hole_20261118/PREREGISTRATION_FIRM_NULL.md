# Preregistration 4: Is the firm-level hole more than a portfolio artefact?

**Version:** 1.0, frozen 2026-11-18. This was written **after** the P5 result of the full suite, and **before** any portfolio-preserving null replicate was computed.

**Known:**
- Specialist AI-firm ↔ DEC-firm tie O/E = 0.24, compared with 0.81 for AI-firm ↔ MIXED and 0.97 for DEC-firm ↔ MIXED.
- MIXED median constraint = 0.358, against 0.444 under the degree-matched label null (p = .001).

## Why a new null

The P5 null permuted group labels among firms of similar strength. That null does not hold fixed what a firm owns. MIXED firms own both AI and DEC patents, and patents cite within their own field. So part of P5 could be mechanical: a firm holding both kinds of patents collects ties to both specialist groups even if nothing about the firm itself matters.

The new null keeps every firm's **portfolio** and the **whole patent-level citation network** fixed. It breaks only the link between a particular patent and a particular firm.

## Null model

1. Patents in scope:
   - every US utility patent granted 2010–2025 that is AI-only, DEC-only or BRIDGE;
   - including patents with no organisation assignee, whose owner set is empty.
2. Strata:
   - **primary:** patent type (AI-only, DEC-only, BRIDGE) × grant year;
   - **sensitivity S-tech:** type × grant year × the patent's set of AI rows × its set of DEC columns, using the 6×7 matrix definitions.
3. Within each stratum, the patents' **owner sets** are permuted. This keeps each firm's number of patents of each type and year exactly, and keeps its group (AI_FIRM, DEC_FIRM or MIXED). The patents, and their applicant citations, are unchanged.
4. Firm ties are rebuilt exactly as in P5:
   - undirected;
   - weighted by applicant citations between the firms' in-scope patents;
   - citing year 2010 or later;
   - self-ties excluded.
5. 1,000 replicates, seed 20261119.

## Statistics and decision rule

| Statistic | One-sided p |
|---|---|
| T1 = OE(AI_FIRM ~ DEC_FIRM), using the P5 strength-based expectation | lower tail: (1 + #{null ≤ obs}) / (R + 1) |
| T2 = median Burt constraint of MIXED firms with at least one tie | lower tail |

Also reported, without bearing on the verdict:
- OE(AI_FIRM ~ MIXED) and OE(DEC_FIRM ~ MIXED);
- the medians of the null distributions;
- the share of the observed T1 gap from 1 that the null reproduces: (1 − null median) / (1 − obs).

**Verdict for the primary stratification:**
- `ORGANISATIONAL_HOLE_BEYOND_PORTFOLIO` if T1 p < .05 **and** T2 p < .05;
- `PARTIAL` if exactly one of the two holds;
- `PORTFOLIO_ARTEFACT` if neither holds.

**S-tech:** reported with its own verdict. If it disagrees with the primary verdict, the result is labelled `TECH_MIX_SENSITIVE`.

## What follows from each outcome

- `ORGANISATIONAL_HOLE_BEYOND_PORTFOLIO`: the firm result may be written as an organisational-level structural-hole pattern. The caveats from the full-suite report still apply: no single broker is indispensable, and the bridging is diffuse.
- `PORTFOLIO_ARTEFACT`: the firm result is explained by what firms own. It must not be presented as a structural hole.
- `PARTIAL`: report both statistics and claim neither.
