# Empirical Feasibility & Identifiability Audit v1.1 — corrected status

**FAIL for Measurement Architecture freeze.** The original file at `e9137d4` concluded `PASS WITH EMPIRICAL CONDITIONS` and said no v1.0 structural equation must change. Claude's F1–F3 diagnostics invalidate both conclusions. This correction is a status record; the replacement research/measurement candidates are 21–23.

The finite v1.0 solver on `main@1f2e72f` remains a historical, all-simulated feasibility result. It proves neither empirical parameter identification nor three independent organizational levels. In particular, ordinal values and κ are used as numeric effects in F1/F2/U and related terms; L3 collapses under F2's dependence on `max(0,U*)`; the old C4–C6 do not independently identify threshold functions.

The only items eligible for an early freeze are (1) research positioning and claim boundary, (2) parameter registry field schema, (3) separate storage of observed and optimized states. Requirements, objective coefficients, decision rights, external governance constraints and empirical recommendation remain open.

| Gate | Required proof | Status |
|---|---|---|
| Ordinal / κ effects | Every numeric occurrence replaced by evidence-backed effect map or bounded scenario; recompute monotone recoding sensitivity | OPEN |
| Independent hierarchy | Different formal decision rights, feasible responses and objectives; Junior reaction changes Manager choice under at least one defensible scenario; compare centralized/bilevel | OPEN |
| Threshold identification | A-conditioned cards, independently varied consequence/task/execution, feasibility vs value questions, pilot coverage | OPEN |
| Literature claims | Primary-source claim-to-equation matrix and uncertainty labels | OPEN |
| Scope | M5 outside static baseline; G04 evidence-only; A_obs vs A* in gap; single-case external validity | DOCUMENT REVISED, EMPIRICAL CHECK OPEN |

The two Claude diagnostic scripts and full A–J report are not present in this repository. Their reported 6/9 and 9/9 results are cited as reviewer findings, not rerun evidence. The conditions and execution record are in 23. Until gates close, no `STRONG PASS` label applies to requirement thresholds.
