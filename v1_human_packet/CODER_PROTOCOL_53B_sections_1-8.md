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

