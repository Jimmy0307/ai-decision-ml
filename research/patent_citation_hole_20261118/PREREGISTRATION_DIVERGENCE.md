# Preregistration 8: when does co-occurrence misjudge flow? (explaining Plan 7's disagreements)

**Status:** frozen 2026-11-19, before any breakdown of the Plan 7 pair data by the variables below was computed. The commit timestamp is the freeze record. Changes after the freeze are dated amendments below the text.

**Known when written:**
- Plan 7's aggregate results:
  - primary PPV 0.668;
  - reversal 0.070;
  - ρ 0.80;
  - MODERATE;
  - the hexbin plot of OE_co against OE_flow;
  - the AI × DEC pair values.
- The field list: 185 CPC main groups, 19 subclasses, classes G06/G16/H04.
- No statistic by taxonomic distance, size or volume has been computed or plotted.
- The plan is **data-informed**: it was motivated by Plan 7's disagreement rate. Its hypotheses, variables, models and rules are fixed here.

**Theory:**
- Co-occurrence records joint categorisation: two labels assigned to the same document. Patent co-classification is assigned by examiners within a hierarchical scheme.
- Citation flow records knowledge dependence.
- If co-occurrence mostly reflects categorisation, it should understate flow most where the categorisation scheme puts fields far apart. Knowledge can cross that distance, while a single document rarely carries labels from distant branches.
- The hypothesis is therefore that **the gap between flow and co-occurrence grows with taxonomic distance**.

## 1. Data

- `paper/data/PLAN7_PAIRS_primary.csv` (Plan 7 primary specification).
- The 16,703 eligible pairs (E_co ≥ 5 and E_flow ≥ 5).
- Plan 7's quartile thresholds for C-gap and F-gap (OE_co ≤ 0.0269; OE_flow ≤ 0.3291).

## 2. Variables

**Taxonomic distance** (from the CPC symbols of the two main groups):
- level 1: same subclass, e.g. G06F16 and G06F17;
- level 2: same class, different subclass, e.g. G06F and G06N;
- level 3: different class, e.g. G06 and H04, or G06 and G16.

**Divergence Δ:**
- Δ = percentile rank of OE_flow minus percentile rank of OE_co, both ranks taken among eligible pairs (ties get average ranks; range −1 to 1).
- Δ > 0: flow is higher, relative to other pairs, than co-occurrence suggests (co-occurrence understates flow).

**Controls:**
- log(n_a · n_b), pair size;
- |log n_a − log n_b|, size asymmetry;
- log E_flow, citation volume.

## 3. Hypotheses and tests

**H8a (main):** Δ increases with taxonomic distance.
- **Model:** OLS of Δ on indicators for level 2 and level 3 (reference: level 1), plus the three controls.
- **Supported** if both hold:
  - the level-3 coefficient is > 0 with a 95% CI excluding 0;
  - the unadjusted mean Δ is ordered level 1 < level 2 < level 3.
- **Reversed** if the level-3 coefficient is < 0 with a 95% CI excluding 0.
- **Not supported** otherwise.

**H8b (consequence for gap inference):** among C-gaps, the false-gap rate (not an F-gap) and the reversal rate (OE_flow ≥ 1) are higher for level-3 pairs than for level-1 and level-2 pairs combined.
- **Supported** if the level-3 minus levels-1/2 difference in the false-gap rate is > 0 with a 95% CI excluding 0.
- The reversal difference is reported beside it.

**Uncertainty:**
- Cluster bootstrap over fields, 1,000 replicates, seed 20261119.
- Each replicate resamples fields with replacement and keeps pairs of distinct resampled fields, with multiplicity as weights.
- Coefficients and rate differences are recomputed with those weights.
- Report percentile 95% CIs.
- Ranks and thresholds are fixed at full-sample values.

## 4. Secondary (descriptive)

- **S1:** H8a with Δ' = log OE_flow − log OE_co, for pairs with n_ab > 0.
- **S2:** H8a without controls.
- **S3:**
  - mean Δ for pairs that include a G16 field;
  - mean Δ for pairs within the AI × DEC construct (G06N main groups × G06Q10) as a reference point;
  - the share of all C-gap reversals that are level-3 pairs.
- **Not done:** no "method vs application" coding. It would need subjective labels; it is noted as future work.

## 5. Reporting

- Results are reported whatever they are.
- If H8a is not supported or is reversed, the manuscript must not claim that taxonomy explains the disagreement.
- Code: `src/divergence.py`.
- Output: `results/PLAN8_RESULTS.json`.
