# Preregistration 6: firm null preserving portfolio and degree (design A2)

**Status:** frozen 2026-11-19, before any replicate of this null was computed. The commit timestamp is the freeze record. Changes after the freeze are dated amendments below the text.

**Known when written:**
- Plans 1–5 and Plan C are complete.
- Under the degree-matched label null (Plan 3, P5), MIXED firms had low constraint (p = .001).
- Under the portfolio-preserving null (Plan 4), they had high constraint (T2 p = 1.000), and T1 was significant (p = .001).
- Plan 6 is therefore **data-informed**: its question was motivated by that contradiction. Only its definitions, rules and thresholds are fixed in advance.

**Question (RQ2):** do specialist AI and decision firms remain separated (T1), and do MIXED firms have lower constraint than expected (T2), under a null that holds fixed both each firm's patent portfolio and, as closely as possible, its degree?

## 1. Data and statistics (unchanged from Plan 4)

**Data:** the slim firm model `outputs/firm_model_LOCAL.pkl` from `src/firm_null.py`:
- 127,114 in-scope patents;
- 14,600 firms;
- 162,339 applicant citations;
- owner groups AI_FIRM, DEC_FIRM and MIXED.

**Firm network:**
- The firm × firm tie weights are those of `FirmModel.weights` (owner pairs of each citation; self-pairs removed).
- **T1:** O/E of AI_FIRM–DEC_FIRM tie weight.
- **T2:** median Burt constraint of active MIXED firms.
- Both are computed by `FirmModel.stats`.
- The observed values must reproduce Plan 3 P5 and Plan 4 exactly: T1 0.240, T2 0.358, 20,681 ties. Otherwise the run stops.

## 2. Null (A2)

**Strata:** owner sets are permuted among patents in the same stratum.
- **Primary stratum:** patent type × grant year × out-degree class × in-degree class.
  - The out-degree is the number of in-scope applicant citations the patent makes.
  - The in-degree is the number it receives.
  - Each class is the exact count for 0–9; 10 and above form one class.
- **Secondary stratum (S-tech):** the Plan 4 S-tech key (type × year × AI rows × DEC columns) × the same degree classes.
- Strata with one patent are fixed.

**What it preserves:**
- **Exactly:**
  - each firm's portfolio by type and year (S-tech: also by technology mix);
  - the patent citation network;
  - each firm's number of citation incidences, for every patent whose degrees are below 10 on both sides.
- **Approximately:** each firm's number of distinct partners (binary degree) and tie strength.

**Replicates:**
- R = 1,000 per scheme.
- Replicate r of scheme s uses `default_rng([20261119, 6, s, r])`.
- Checkpoint every 50 replicates.

## 3. Validity gate (decided before any test result is read)

For each replicate, compute the Spearman rank correlation, across the firms with at least one tie in the observed network, between:
- observed and null binary degree (number of distinct partners);
- observed and null strength.

**The null is valid for a scheme only if both hold:**
- median degree ρ ≥ 0.90;
- median strength ρ ≥ 0.95.

**Also reported:**
- the share of patents in singleton strata;
- the share of firms whose null median degree is within ±20% of the observed degree.

**If the gate fails for a scheme:**
- that scheme's verdict is `INVALID_NULL`;
- its T1/T2 p-values are reported as descriptive only;
- no claim about brokerage is made from it.

## 4. Tests and verdicts (Plan 4 rules)

**p-values:** one-sided lower-tail Monte Carlo p-values, p = (1 + #{null ≤ observed}) / (1 + R), for T1 and T2.

**Verdict per scheme (gate passed):**
- `HOLE_BEYOND_PORTFOLIO_AND_DEGREE`: T1 p < .05 and T2 p < .05;
- `PARTIAL`: exactly one of them;
- `PORTFOLIO_DEGREE_ARTEFACT`: neither.

**Reading rules:**
- If the primary and S-tech verdicts differ (both valid), the result is labelled `TECH_MIX_SENSITIVE`.
- A T2 p < .05 means that MIXED firms have lower constraint than firms with the same portfolio and nearly the same degree would have. It is the strongest firm-level brokerage evidence this programme can produce. It is still evidence of a structural position in a citation network, not of an organisational mechanism.
- A T2 p ≥ .05 means the low constraint seen under P5 is accounted for by portfolio and degree.

**Also reported:**
- for T1 and T2: the null median and 95% band;
- for T1: the share of the gap from 1 reproduced by the null.

## 5. Stop rules and computing

- The run may take place on any machine. Because of the seeding rule, results do not depend on where it runs.
- If R = 1,000 is infeasible, R = 500 may be used. This is recorded as an amendment before any null statistic is read.
- A failed exact-reproduction check (§1) stops the run.
- Code: `src/firm_null_degree.py`. It reuses `FirmModel` and adds only the degree-class strata and the gate.
