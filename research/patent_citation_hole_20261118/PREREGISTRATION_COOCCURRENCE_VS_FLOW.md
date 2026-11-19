# Preregistration 7: does sparse co-occurrence identify sparse knowledge flow? (all field pairs)

**Status:** frozen 2026-11-19, before any pair-level co-classification or citation quantity was computed. The commit timestamp is the freeze record. Changes after the freeze are dated amendments below the text.

**Known when written:**
- All results of Plans 1–6 and Plan C.
- For one pair of constructs (AI = G06N, DEC = G06Q10/04 + /06), literature co-occurrence was depleted while patent citation flow was over-connected (OE 3.05).
- No pair-level co-classification statistic for the field pairs below has been computed.
- The plan is **data-informed**: it was motivated by the question of whether that reversal is typical. Its definitions, rules and thresholds are fixed here.

**Question:** across many pairs of technology fields, how often does a co-occurrence gap (sparse co-classification) coincide with a flow gap (sparse citation)? How often does it coincide with the opposite, flow over-connection? This tests the inference "co-occurrence sparse ⇒ separated" within one database, on the same patents, at scale.

## 1. Units

- **Fields:** CPC main groups in classes G06, G16 and H04 with at least 2,000 patents granted 2010–2025.
  - Same membership source and threshold as the Plan 1 reference set, but G06N and G06Q10 main groups are included here.
  - Membership uses all CPC codes (current CPC, all types).
- **Units:** unordered pairs {A, B} of distinct fields.

## 2. Measures

**Co-occurrence (co-classification):**
- Universe: utility patents granted 2010–2025 with at least one membership in a selected field. N is their number.
- n_A is the number of patents in A, and n_AB the number in both A and B.
- OE_co(A,B) = n_AB · N / (n_A · n_B).
- Expected count E_co = n_A n_B / N.

**Flow (citations; Plan 1 method):**
- Applicant citations ("cited by applicant") whose citing patent was granted 2010–2025. In practice this is 2013–2025 (amendment A2 of Plan 1).
- Strata s = (citing grant year, cited grant year).
- M(s) is the number of such citations in stratum s, over all patents.
- O_AB is the number of citations from a patent in A \ B to a patent in B \ A.
- E_AB = Σ_s out_{A\B}(s) · in_{B\A}(s) / M(s).
- OE_flow(A,B) = (O_AB + O_BA) / (E_AB + E_BA), with E_flow = E_AB + E_BA.

**Eligible pairs:** E_co ≥ 5 and E_flow ≥ 5.

## 3. Primary definitions and estimands (eligible pairs)

**Definitions:**
- **C-gap:** OE_co is in the lowest quartile of OE_co across eligible pairs (≤ its 25th percentile).
- **F-gap:** OE_flow is in the lowest quartile of OE_flow across eligible pairs.
- **Flow over-connection:** OE_flow ≥ 1.

**Estimands:**
- **PPV** = P(F-gap | C-gap). The baseline under independence is about 0.25.
- **Reversal rate** RR = P(OE_flow ≥ 1 | C-gap).
- **Spearman ρ** between OE_co and OE_flow.
- **Absence:** among eligible pairs with n_AB = 0 (never co-classified), the share that is an F-gap and the share with OE_flow ≥ 1.

**Uncertainty:**
- Cluster bootstrap over fields: 1,000 replicates, seed 20261119.
- Each replicate resamples fields with replacement and recomputes PPV, RR and ρ over the pairs of distinct resampled fields, with multiplicity.
- Quartile thresholds stay fixed at their full-sample values.
- Report percentile 95% intervals.

## 4. Reading rule (decided now)

- `RELIABLE` if PPV ≥ 0.80 **and** RR ≤ 0.05.
- `UNRELIABLE` if PPV < 0.50 **or** RR ≥ 0.20.
- `MODERATE` otherwise.

The label is stated for the primary specification. The bootstrap intervals are reported beside it. If the 95% interval of PPV crosses a cut-point, this is said explicitly.

## 5. Secondary specifications (descriptive; no label changes)

| Spec | Change |
|---|---|
| S1 | strict cut-points: C-gap is OE_co ≤ 0.5; F-gap is OE_flow ≤ 0.5 |
| S2 | all citation categories (citing years 2010–2025) |
| S3 | eligibility E_co ≥ 20 and E_flow ≥ 20 |
| S4 | lowest decile instead of lowest quartile, for both |
| S5 | periods: co-classification among patents granted 2013–2018, citations with citing years 2013–2018; and the same for 2019–2025 |

**Also reported:** where the pairs of a G06N main group with G06Q10 fall. This includes their OE_co, OE_flow and quartile membership, as a link to Study 2.

## 6. Scope and reporting

- Co-classification is co-occurrence of labels in the same documents, the same kind of evidence as Study 1's matrix, but in patents. The result speaks to the inference from co-occurrence to separation in these technology fields. It does not speak to the literature directly.
- Every result is reported whatever it is. If the label is `RELIABLE`, the manuscript must say that the AI–decision reversal is atypical in these fields and must weaken any general claim accordingly.
- **Code:** `src/cooc_vs_flow.py`.
- **Data:** the local caches of Plans 1 and 5 (`cache_citations_LOCAL.npz`, `plan5_cpc_LOCAL.npz`) plus grant years from `g_patent`. No new download.
