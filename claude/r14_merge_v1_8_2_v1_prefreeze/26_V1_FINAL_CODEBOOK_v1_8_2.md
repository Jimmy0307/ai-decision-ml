# 26 — V1 Final Codebook v1.8.2 (supersedes 21)

**Audience.** Sections 1–4 are the coder-facing codebook. They are reproduced word for word in the `README_INSTRUCTIONS`, `CATEGORY_DEFINITIONS` and `ATTESTATION` sheets of `coder_distribution/CODER_k.xlsx`. Sections 5–7 are for the study team only. Coders receive only their own xlsx, never this file.

**Status.** Frozen at S1. Prepared, not run. This file contains no item-to-category, item-to-G, or G-to-category assignment.

**Definition sources.**
- M1–M4: 53B §3, verbatim. The lead phrase is reworded to "Use when the main issue of the connection is …".
- LONGITUDINAL and DATA_GATED: 53B §3–§4 and clarifications v2.2.1 A–D.
- NONE: decision D-2 (24).
- M1 label: decision D-12.

## 1. Unit and stimulus

The unit is 16 items. Each item is identified only by a neutral item ID in the range ITEM-A01…ITEM-A16. The IDs come from a secret seeded random permutation, so they carry no information about the study's internal numbering or ordering.

Every item shows the same fields:
- the AI function family, with its English and Chinese label and its definition;
- the decision function family, with its English and Chinese label and its definition;
- one standard depletion statement: "DEPLETED: observed below the expectation of a statistical null model under all four pre-specified methods; a research lead only";
- the neutral evidence description from 54A, with no counts, O/E or q values.

Each coder sees the items in a different seeded order.

## 2. Questions (identical wording for every item)

| Q | Question | Allowed values | Required |
|---|---|---|---|
| Q1 | Does this pairing correspond to an identifiable enterprise decision interface? | `YES` / `NO` / `UNCERTAIN` | yes |
| Q2 | Best category | `M1` `M2` `M3` `M4` `LONGITUDINAL` `DATA_GATED` `EVIDENCE_ONLY` `NONE` `AMBIGUOUS` | yes, every item |
| Q3 | Confidence in Q2 | `HIGH` / `MEDIUM` / `LOW` | yes |
| Q4 | Optional secondary category | blank, or `M1` `M2` `M3` `M4` `LONGITUDINAL` `DATA_GATED` (must differ from Q2) | no |
| Q5 | Rationale, 1–3 sentences, ≤ 600 characters | free text | yes, every item |

**Enterprise decision interface.** A decision an enterprise must make about how this kind of AI function feeds this kind of decision function, where that decision is specific to this pairing.

**Consistency rules.** The analyzer enforces these as validation errors:
- Q1 = YES → Q2 ∈ {M1, M2, M3, M4, LONGITUDINAL, DATA_GATED, NONE, AMBIGUOUS}.
- Q1 = NO → Q2 = EVIDENCE_ONLY.
- Q1 = UNCERTAIN → any Q2 except NONE.
- Q4 ≠ Q2.
- NONE requires Q1 = YES and a non-empty Q5 that states the enterprise decision no listed category captures.

## 3. Categories

| Code | Label | Use when | Do not use when / note |
|---|---|---|---|
| `M1` | Authority & Accountability (授權與問責; = Governance & Decision Rights / authority-to-act) | The main issue of the connection is who may approve, reject, stop or change what the AI output is allowed to decide. This includes formal versus effective control, accountability and enterprise policy boundaries. | The main issue is how outputs are routed or technically validated. |
| `M2` | Workflow Routing & Recovery | The main issue of the connection is how the AI output enters the next decision or action step. This includes handoffs across systems or units, exception handling, and rollback and recovery. | The main issue is who holds authority. |
| `M3` | Human–AI Configuration & Response | The main issue of the connection is the sequence and division of work between people and AI (who proposes, who decides, aggregation, delegation, override) and how users actually respond (use, verify, modify, escalate, reject, bypass). | The main issue is formal authority or validation evidence. |
| `M4` | Evaluation & Assurance | The main issue of the connection is pre-deployment validation, monitoring, revalidation, auditability, explanation usability, drift, or evidence that the AI output is fit for the decision. | The main issue is who decides or how work is sequenced. |
| `LONGITUDINAL` | Longitudinal extension | The enterprise decision can only be studied with outcomes observed over more than one period: results of one cycle change later resource allocation, policy or information acquisition. | A single-period configuration choice is enough. The M1–M4 category involved may go in Q4. |
| `DATA_GATED` | Data-gated module | An enterprise decision exists only if a specific kind of data is available. Name the data in Q5. | A category applies without special data. The M1–M4 category involved may go in Q4. |
| `EVIDENCE_ONLY` | Evidence-layer only | The pairing describes a research or technology pattern but implies no distinct enterprise decision beyond what any AI function feeding this decision function would raise. | Use with Q1 = NO (or UNCERTAIN). |
| `NONE` | None of the listed categories | An identifiable enterprise decision interface exists, but none of M1, M2, M3, M4, LONGITUDINAL or DATA_GATED adequately expresses it. Requires Q1 = YES; Q5 must state the decision that is not captured. | Not for insufficient evidence or a two-category tie (use AMBIGUOUS, or Q1 = UNCERTAIN). Not for "no distinct interface" (use EVIDENCE_ONLY). |
| `AMBIGUOUS` | Ambiguous | Two or more categories fit equally well, or the definitions do not allow a defensible single choice. Name the competing categories in Q5. | Not a default. |

## 4. Procedure rules (coder-facing)

1. **Order of tests for Q2.** Ask in this order and stop at the first that applies:
   - (a) The decision can only be represented with outcomes over more than one period → LONGITUDINAL.
   - (b) The decision exists only if a named dataset is available → DATA_GATED.
   - (c) There is a distinct single-period decision → the M1–M4 category that fits the main issue, or NONE if none of them expresses it.
   - (d) Otherwise → EVIDENCE_ONLY, with Q1 = NO.

   Use AMBIGUOUS only if you cannot choose.
2. **Residual family.** "General Decision Process" is a residual family. Code it like any other family if a category fits; otherwise use EVIDENCE_ONLY or AMBIGUOUS.
3. **Code the enterprise decision.** Do not code the technology, the topic, or a word that a family name happens to share with a category name. The shared words are "Evaluation", "Accountability" and "Assurance".
4. **Q3 and Q4.** Q3 refers to Q2 only and is never a weight. Leave Q4 blank unless a second category is clearly needed.
5. **Attestation.** Answer 7 statements YES or NO, then fill in name, date and signature. An honest NO is recorded, and that coder is analysed separately (EXPOSED), never silently pooled.

---

## 5. Crosswalk to 53B (study team only; OA-2 = APPROVED_WITH_SCOPE_LIMIT, so these are secondary continuity metrics only)

| v1.8.2 Q2 | `primary_53B` | `status_53B` | 41 / manuscript interface |
|---|---|---|---|
| `M1`–`M4` | same code | `static` | I1–I4 |
| `LONGITUDINAL` | `M5` | `dynamic` | I5 (M5, dynamic only) |
| `DATA_GATED` | Q4 if Q4 ∈ M1–M4, otherwise `OPTIONAL_DATA_GATED` | `optional` | conditional module |
| `EVIDENCE_ONLY` | `EVIDENCE_ONLY` | `evidence-only` | evidence layer only |
| `NONE` | `OTHER` (new_construct_required = YES) | `static` | — |
| `AMBIGUOUS` | `INSUFFICIENT_INFORMATION` | `insufficient` | — |

"V1_PASS_HUMAN_C6 is a continuity label under the earlier 53B protocol, not evidence that the amended Q1–Q5 instrument is identical to 53B."

## 6. Flattening the sealed key (phase K only, after S3)

The key's (primary, secondary, status) entries are mapped to one Q2-style category by these rules, applied in order:
1. status `dynamic` → LONGITUDINAL
2. status `optional` → DATA_GATED
3. status `evidence-only` → EVIDENCE_ONLY
4. otherwise → the primary code M1–M4

A mechanism-level comparison on `primary_53B` / `status_53B` is also reported. No flattened key is written before unsealing.

## 7. Changes from v1.8.1 (21)

| Change | Reason |
|---|---|
| G ID replaced by a neutral item ID; secret permutation; per-coder seeded order | D-8 and D-11 (masking) |
| NONE defined with the Q1 = YES and Q5 requirements; NONE not allowed with Q1 = UNCERTAIN | D-2 (OA-3) |
| M1 label aligned | D-12 |
| Attestation expanded to 7 YES/NO statements | D-10 |
| Coders return sheets "directly to the study coordinator (not via any shared repository)" | D-15 (public repository) |
| Examples "(e.g., labelled outcomes, score distributions)" remain removed | potential hint for one data-gated pairing |
