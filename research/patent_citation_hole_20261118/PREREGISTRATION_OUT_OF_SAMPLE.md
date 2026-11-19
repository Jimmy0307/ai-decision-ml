# Preregistration 9: out-of-sample replication of Plans 7 and 8 in all other technology fields

**Status:** frozen 2026-11-19, before any CPC membership outside G06/G16/H04 was extracted. The commit timestamp is the freeze record. Changes after the freeze are dated amendments below the text.

**Known when written:**
- All results of Plans 1–8 and Plan C.
- In G06/G16/H04, Plan 7 gave PPV 0.668 and reversal 0.070 (MODERATE). Plan 8's H8a and H8b were not supported.
- The post hoc pattern from Plan 8: C-gap PPV was lower between neighbouring subclasses of one class (level 2: 0.605; reversal 0.101) than across classes (level 3: 0.696; reversal 0.056).

**Purpose:** two parts.
- **(i) Replicate the whole Plan 7 and Plan 8 battery** with identical definitions, rules and code paths on data not used so far.
- **(ii) Test the post hoc neighbour pattern as a confirmatory hypothesis.**

## 1. Held-out universe

- **Fields:** CPC main groups in every section A–H **except** classes G06, G16 and H04 (used in Plans 7–8) and section Y (cross-sectional tagging codes).
- **Threshold:** at least 2,000 utility patents granted 2010–2025.
- Membership uses all current CPC codes of each patent.
- **Units:** unordered pairs of distinct held-out fields. Pairs involving G06/G16/H04 fields are excluded.

## 2. Measures (identical to Plan 7)

- **Co-occurrence:** OE_co = n_AB · N / (n_A n_B) among patents granted 2010–2025 with at least one held-out membership.
- **Flow:** symmetric citation OE using the Plan 1 method (strata = citing grant year × cited grant year; M(s) over all citations of the specification). O_AB counts citations from A \ B to B \ A.
- **Eligibility:** E_co ≥ 5 and E_flow ≥ 5.
- **Gaps:** C-gap / F-gap = lowest quartile of OE_co / OE_flow among eligible pairs.
- **Reversal:** a C-gap with OE_flow ≥ 1.
- **Taxonomic level (Plan 8):**
  - 1 = same subclass;
  - 2 = same class, different subclass;
  - 3 = different class.
  - Level 3 is also split, descriptively, into 3a (same section) and 3b (different section).

The computation of the expected flow may be reorganised for memory, for example sparse corrections for patents in both fields. It must give results identical to Plan 7's formula. This is checked by recomputing the G06/G16/H04 primary specification with the new code: PPV, reversal and ρ must match Plan 7 to 1e-9.

## 3. Hypotheses and rules

**R7 (replication of Plan 7).** The Plan 7 label rule is applied to the held-out primary specification:
- RELIABLE if PPV ≥ 0.80 and reversal ≤ 0.05;
- UNRELIABLE if PPV < 0.50 or reversal ≥ 0.20;
- MODERATE otherwise.
- **Replicates** if the held-out label equals Plan 7's (MODERATE).
- Plan 7's secondary specifications S1–S5 are also recomputed and labelled with the same rules (descriptive).

**R8 (replication of Plan 8).** H8a and H8b are re-tested with Plan 8's exact variables, models and decision rules. The labels are reported as replications.

**H9 (confirmatory, new): co-occurrence gaps are least reliable between neighbouring subclasses.**
- **H9a:** among C-gaps, PPV(level 2) − PPV(level 3) < 0. Supported if the 95% CI is entirely below 0.
- **H9b:** among C-gaps, reversal(level 2) − reversal(level 3) > 0. Supported if the 95% CI is entirely above 0.
- **Overall:**
  - **H9 SUPPORTED** if both H9a and H9b are supported;
  - **PARTIAL** if one is;
  - **NOT_SUPPORTED** if neither is;
  - **REVERSED** if either difference has a CI entirely on the opposite side.

**Uncertainty:**
- Cluster bootstrap over fields, 1,000 replicates, seed 20261119.
- Each replicate takes pairs of distinct resampled fields, with multiplicity weights.
- Thresholds and ranks are fixed at full-sample values.

## 4. Reporting

- All labels are reported whatever they are.
- **Manuscript statements depend on the outcome:**
  - If H9 is supported, the manuscript may state the neighbour pattern as a replicated finding across the held-out technology fields, with its effect sizes.
  - If H9 is partial or not supported, it stays a pattern seen in G06/G16/H04 only.
- **Code:** `src/oos_replication.py`.
- **Output:**
  - `results/PLAN9_RESULTS.json`;
  - `results/PLAN9_PAIRS_primary.csv` (CPC symbols and counts only).
- **Scope:** US patents only. Co-classification is co-occurrence of labels in the same documents; the replication does not cover literature co-word data.
