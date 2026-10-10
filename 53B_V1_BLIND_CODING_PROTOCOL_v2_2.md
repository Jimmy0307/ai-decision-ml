# 53B — V1 Blind Coding Protocol v2.2 (G→M construct coding)

**Status:** pre-registered protocol, frozen before any coder output exists (see §10 freeze record).
**Purpose:** obtain independent codes for 16 literature-network cases so that the researcher-adjudicated mapping in `41` can be tested, not confirmed by construction.

---

## 1. What coders receive — and what they must never see

Coders receive only:

1. this protocol (§1–§8; §9–§10 are for the study team and may be removed from the coder copy);
2. one packet (`54A_V1_BLIND_PACKET_A_v2_2.csv` or `54B_V1_BLIND_PACKET_B_v2_2.csv`) — same 16 cases, different row order;
3. an empty response sheet (§6 format).

Coders must not see, before their codes are frozen and hashed:

- `41_G01_G16_CONVERGENCE_AND_CONSTRUCT_FREEZE_v2_1.md`, `42`, `44` (or any manuscript text), `48`, `53A`;
- any Gap ID (G01–G16), the researcher's mechanism, interface, bridge/anchor, keep/merge/exclude, or static/dynamic decision;
- O/E ratios, observed counts or q-values (to avoid anchoring on effect strength);
- another coder's answers.

Because files 41 and 44 are in a public repository, a human coder must sign the attestation in §8 that they have not read them. Packets are delivered outside the repository.

## 2. The coding question

For each case you see one AI function family and one decision function family. The published literature directly linking the two is **underrepresented** relative to a statistical null structure. This is only a research lead: it does **not** mean the combination is impossible, ineffective, unimportant, or absent from practice.

Answer this question:

> If an enterprise deploys AI so that this kind of AI function feeds this kind of decision function, **which enterprise mechanism most directly determines how that connection is configured, controlled and made to work?** If no enterprise configuration decision is involved, say so.

Code the enterprise mechanism, not the technology and not the topic of the literature.

## 3. Codebook — primary and secondary codes

| Code | Name | Use it when the connection mainly raises a question of … | Do not use it when … |
|---|---|---|---|
| `M1` | Governance & Decision Rights / Authority-to-act | who may approve, reject, stop or change what the AI output is allowed to decide; formal versus effective control; accountability; enterprise policy boundaries | the main issue is how outputs are routed or technically validated |
| `M2` | Workflow & Integration / Routing & Recovery | how the AI output enters the next decision or action step; handoffs across systems or units; exception handling; rollback and recovery | the main issue is who holds authority |
| `M3` | Human–AI Work Configuration / Configuration & Response | the sequence and division of work between people and AI (who proposes, who decides, aggregation, delegation, override) and how users actually respond (use, verify, modify, escalate, reject, bypass) | the main issue is formal authority or validation evidence |
| `M4` | Evaluation & Assurance | pre-deployment validation, monitoring, revalidation, auditability, explanation usability, drift, evidence that the AI output is fit for the decision | the main issue is who decides or how work is sequenced |
| `M5` | Learning & Resource Feedback | how results observed over time change later resource allocation, policy or information acquisition (requires data across periods) | a single-period configuration choice is enough |
| `OPTIONAL_DATA_GATED` | Optional / data-gated | a configuration decision exists only if a specific kind of data is available (name it in the rationale); otherwise nothing can be configured | a mechanism applies without special data — then code the mechanism and set status `optional` |
| `EVIDENCE_ONLY` | Evidence only | the pairing describes a technology or research frontier but implies no distinct enterprise configuration decision beyond what M1–M5 already cover generally | a specific mechanism clearly applies |
| `OTHER` | Other mechanism | a distinct enterprise mechanism is needed that M1–M5 cannot express; set `new_construct_required = yes` and explain | M1–M5 can express it, even imperfectly |
| `INSUFFICIENT_INFORMATION` | Insufficient information | the definitions do not allow a defensible code | — |

- `primary_code`: exactly one code from the table.
- `secondary_code`: optional; at most one; use only when a second mechanism is clearly necessary (a "bridge"). Leave blank otherwise.
- You are **not** required to place every case in M1–M5.

## 4. Status codes

| Status | Meaning |
|---|---|
| `static` | can be represented as a single-period enterprise configuration choice |
| `dynamic` | can only be studied with outcomes observed across periods |
| `optional` | modelable only if specific data exist (name the data) |
| `evidence-only` | no distinct enterprise configuration decision |
| `insufficient` | cannot decide |

## 5. Other fields

- `confidence`: 0–100, your confidence in the primary code. Diagnostic only; it is never used to weight agreement.
- `rationale`: 1–3 sentences.
- `enterprise_decision_interface`: one short neutral phrase naming the enterprise decision (e.g., "who signs off before a model-based recommendation is executed").
- `new_construct_required`: `yes` or `no`. If `yes`, `new_construct_reason` must say why M1–M5 cannot express it.

## 6. Response format (CSV, UTF-8)

```
case_id,primary_code,secondary_code,status,confidence,rationale,enterprise_decision_interface,new_construct_required,new_construct_reason
```

One row per case, all 16 cases. Do not change case IDs.

## 7. Analysis plan (pre-registered)

**Unit of analysis:** case (n = 16).

**Primary reliability — primary_code (nominal):**
- two coders: raw agreement and Cohen's κ (Cohen, 1960);
- more than two coders: Krippendorff's α (nominal);
- for two coders, Krippendorff's α (nominal) is also reported so that the two-coder and multi-coder reports share one metric;
- 95% percentile bootstrap CI over cases (5,000 resamples, seed 20261011).

**Status reliability:** the same statistics computed separately on `status`. Never pooled with the primary code.

**Secondary codes:** reported as a disagreement table and as Jaccard agreement on the set {primary ∪ secondary}. Not used in the primary statistic.

**Confidence:** reported descriptively (median per coder; confidence on agreed vs disagreed cases). Not used for weighting.

**Agreement with the researcher key (53A):** computed only after all coder outputs are frozen, reported separately. The researcher key is a hypothesis, not ground truth.

## 8. Coder attestation (human coders)

> I have not read files 41, 42, 44, 48 or 53A of the repository, nor any manuscript text describing the mapping of these cases. I coded independently, without discussing cases with other coders before submitting. Name / date / signature.

## 9. Pass criteria — `V1_PASS_CRITERIA_PRE_REGISTERED`

Registered before any coder output exists. Thresholds are conventions adopted for this study, not universal truths.

| Criterion | Rule | Rationale / source |
|---|---|---|
| C1 Reliability of primary code | Krippendorff's α (nominal) on primary_code ≥ .800 → `RELIABLE`; .667 ≤ α < .800 → `TENTATIVE`; α < .667 → `NOT_ACCEPTABLE`. Cohen's κ is reported alongside but the decision uses α. | Content-analysis convention attributed to Krippendorff (2004, 2019) `[VERIFY: thresholds checked only in secondary sources; see 57]`. Landis & Koch (1977) labels are reported as descriptive benchmarks only. |
| C2 Precision | If the bootstrap 95% CI lower bound of α is < .667, the result is labelled `IMPRECISE` and at least one additional coder is required before any V1 claim. | n = 16 makes point estimates unstable. |
| C3 Status reliability | Same thresholds applied to `status`, reported separately. | Status decides whether a case enters the static model. |
| C4 Critical-case rule | Any case whose adjudicated primary code or status differs from the researcher key triggers the mapping-sensitivity procedure (§11). If the change is classified `model-structural`, V1 cannot pass until 42/44 are revised. | Disagreement matters only if it changes the model. |
| C5 Adjudication | Disagreements are resolved after both codes are frozen: (i) coders discuss without the researcher key; (ii) if unresolved, an adjudicator who did not author 41 decides, recording evidence and rationale in 55; (iii) the researcher key is revealed only after adjudicated codes are frozen. If the 41 author must adjudicate, this is flagged as a limitation. | Keeps the researcher's prior from deciding disagreements. |
| C6 V1 PASS (human) | Requires ≥ 2 independent human coders, C1 ≥ `TENTATIVE` and not `IMPRECISE`, C3 ≥ `TENTATIVE`, and no unresolved `model-structural` change under C4. | — |
| C7 AI pilot | The same statistics are computed on AI coders. Meeting C1–C3 yields only `AI_BLIND_CODING_PILOT_ACCEPTABLE`; it never yields V1 PASS. | AI coders are not independent human raters. |

## 10. Freeze record

The SHA-256 of this file, of both packets and of the sealed key are recorded in `v1_blind/FREEZE_MANIFEST.txt` before any coder output is produced. Coder outputs are hashed into the same manifest immediately after submission and before the key is revealed.

## 11. Mapping-sensitivity procedure

For every disagreement case, record: the alternative code; which 42 equation elements depend on the original code; whether those elements would remain in 42 for enterprise-architecture reasons (41 §7 rule 2); which 44 claims must be downgraded. Classify as `mapping-only`, `manuscript-only`, or `model-structural`.

## References used in this protocol

Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement, 20*(1), 37–46. https://doi.org/10.1177/001316446002000104

Krippendorff, K. (2004). Reliability in content analysis: Some common misconceptions and recommendations. *Human Communication Research, 30*(3), 411–433. https://doi.org/10.1111/j.1468-2958.2004.tb00738.x

Krippendorff, K. (2019). *Content analysis: An introduction to its methodology* (4th ed.). SAGE. `[VERIFY: SAGE lists May 2018 publication]`

Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. *Biometrics, 33*(1), 159–174. https://doi.org/10.2307/2529310

Family definitions in the packets are abridged English renderings of the operational definitions in the V5 conference manuscript (Table 2), which are this study's own taxonomy, not external sources.
