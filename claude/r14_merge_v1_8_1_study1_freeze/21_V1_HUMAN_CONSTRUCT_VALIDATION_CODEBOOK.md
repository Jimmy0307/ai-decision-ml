# 21 — V1 Human Construct-Validation Codebook (v1.8.1)

**Audience.** Sections 1–4 are the coder-facing codebook. They are reproduced word for word in sheet `CATEGORY_DEFINITIONS` and sheet `README_INSTRUCTIONS` of packet 20. Sections 5–7 are for the study team only. They contain the category crosswalk and derived variables. The analysis script is `tools/I/v1_construct_analyzer.py` (protocol 19 §13). Give coders only the xlsx files, not this markdown file.

**Status.** Prepared, not run. This file contains no item-to-category assignment.

**Sources of the definitions.** The M1–M4 operational definitions ("use when" and "do not use when") are taken from the frozen 53B §3 codebook (`53B_V1_BLIND_CODING_PROTOCOL_v2_2.md`, SHA-256 `994ac34b…7223`). The only edit is the lead phrase, which is reworded as "Use when the main issue of the connection is …". The LONGITUDINAL and DATA_GATED tests are adapted from 53B §3–§4 (M5, `OPTIONAL_DATA_GATED`, status `dynamic`/`optional`) and from `v1_human_packet/CODER_CLARIFICATIONS_v2_2_1.md` A–D. Section 6.3 lists every change.

---

## 1. Unit and stimulus

There are 16 items, one per literature pairing (G01–G16). Every item shows the same five things:

- the G ID;
- the AI function family, with its English and Chinese label and its definition;
- the decision function family, with its English and Chinese label and its definition;
- the same standard literature-pattern text: "DEPLETED: observed below the expectation of a statistical null model under all four pre-specified methods; a research lead only";
- the neutral evidence description from packet 54A (no counts, O/E or q-values).

The family definitions are the 54A English renderings of the study's own taxonomy (V5 Table 2).

## 2. Questions (identical wording for every item)

| Q | Question | Allowed values | Required |
|---|---|---|---|
| Q1 | Does this pairing correspond to an identifiable enterprise decision interface? | `YES` / `NO` / `UNCERTAIN` | yes |
| Q2 | Best category | `M1` `M2` `M3` `M4` `LONGITUDINAL` `DATA_GATED` `EVIDENCE_ONLY` `NONE` `AMBIGUOUS` | yes, for every item |
| Q3 | Confidence in Q2 | `HIGH` / `MEDIUM` / `LOW` | yes |
| Q4 | Optional secondary category | blank, or `M1` `M2` `M3` `M4` `LONGITUDINAL` `DATA_GATED` (must differ from Q2) | no |
| Q5 | Short rationale (1–3 sentences, ≤ 600 characters) | free text | yes |

**Enterprise decision interface.** This is a decision that an enterprise must make about how this kind of AI function feeds this kind of decision function, and that is specific to this pairing.

- `YES`: such a decision can be named.
- `NO`: the only decisions that can be named would apply equally to almost any AI function feeding this decision function, or no enterprise decision is involved.
- `UNCERTAIN`: you cannot decide between YES and NO.

**Consistency rules.** The xlsx cannot enforce these rules. The analysis script checks them (protocol 19 §9.1).

- If Q1 = `YES`, Q2 must be one of `M1`–`M4`, `LONGITUDINAL`, `DATA_GATED`, `NONE` or `AMBIGUOUS`.
- If Q1 = `NO`, Q2 must be `EVIDENCE_ONLY`.
- If Q1 = `UNCERTAIN`, Q2 may be any value.
- Q4 must differ from Q2.

## 3. Category definitions (Q2 / Q4)

| Code | Label | Use when | Do not use when / note |
|---|---|---|---|
| `M1` | Authority & Accountability (授權與問責; = 53B Governance & Decision Rights / authority-to-act) | The main issue of the connection is who may approve, reject, stop or change what the AI output is allowed to decide. This covers formal versus effective control, accountability and enterprise policy boundaries. | The main issue is how outputs are routed or technically validated. |
| `M2` | Workflow Routing & Recovery | The main issue of the connection is how the AI output enters the next decision or action step. This covers handoffs across systems or units, exception handling, and rollback and recovery. | The main issue is who holds authority. |
| `M3` | Human–AI Configuration & Response | The main issue of the connection is the sequence and division of work between people and AI (who proposes, who decides, aggregation, delegation, override) and how users actually respond (use, verify, modify, escalate, reject, bypass). | The main issue is formal authority or validation evidence. |
| `M4` | Evaluation & Assurance | The main issue of the connection is pre-deployment validation, monitoring, revalidation, auditability, explanation usability, drift, or evidence that the AI output is fit for the decision. | The main issue is who decides or how work is sequenced. |
| `LONGITUDINAL` | Longitudinal extension | The enterprise decision can be studied only with outcomes observed over more than one period: results of one cycle change later resource allocation, policy or information acquisition. A single-period choice is not enough to represent it. | A single-period configuration choice is enough. The M1–M4 category involved may be put in Q4. |
| `DATA_GATED` | Data-gated module | An enterprise decision exists only if a specific kind of data is available. Name the data in Q5. | A category applies without special data. The M1–M4 category involved may be put in Q4. |
| `EVIDENCE_ONLY` | Evidence-layer only | The pairing describes a research or technology pattern but implies no distinct enterprise decision beyond what any AI function feeding this decision function would raise. | Use only with Q1 = `NO` (or `UNCERTAIN`). Do not use when a specific category clearly applies. |
| `NONE` | None of the listed categories | A distinct enterprise decision interface exists (Q1 = `YES`), but none of M1–M4, LONGITUDINAL or DATA_GATED can express it. Describe the decision in Q5. | A listed category can express it, even imperfectly. |
| `AMBIGUOUS` | Ambiguous | Two or more categories fit equally well and you cannot choose, or the definitions do not allow a defensible single choice. Name the competing categories in Q5. | Do not use it as a default. |

## 4. Decision procedure and coding rules (coder-facing)

1. **Order of tests for Q2.**
   - (a) Can the decision be represented only with outcomes over more than one period? If so, code `LONGITUDINAL`.
   - (b) Does the decision exist only if a named dataset is available? If so, code `DATA_GATED`.
   - (c) Is there a distinct single-period decision? If so, code the M1–M4 category whose "use when" text fits the main issue, or `NONE`.
   - (d) Otherwise, code `EVIDENCE_ONLY` with Q1 = `NO`.
   - Use `AMBIGUOUS` only if you cannot choose.
2. **Residual family.** "General Decision Process" is a residual category. Code it like any other family if a category fits. Otherwise use `EVIDENCE_ONLY` or `AMBIGUOUS`.
3. **Code the enterprise decision.** Do not code the technology, the topic of the literature, or words that a family name shares with a category name. Several family names share a word with a category label: "Evaluation and Audit" and "Evaluation and Selection" (Evaluation), "Human Review and Accountability" (Accountability), and "Explanation and Assurance" (Assurance). A shared word is not evidence for that category.
4. **Q3** describes your confidence in Q2 only. It is never used to weight agreement.
5. **Q4** is left blank unless a second category is clearly necessary.

---

## 5. Category crosswalk (study team only)

### 5.1 User category set ↔ frozen 53B codes ↔ manuscript interfaces

| v1.8.1 code (this instrument) | User label | 53B §3 primary code | 53B §4 status | 41 / v1.8 §3.9.1 interface | Operational definition source | Mapping quality |
|---|---|---|---|---|---|---|
| `M1` | Authority & Accountability (授權與問責; = 53B Governance & Decision Rights / authority-to-act) | `M1` "Governance & Decision Rights / Authority-to-act" | static | I1 授權行動 (Authority-to-act) | 53B §3 M1 row (verbatim) | Same definition, different label: 53B and 41 F1 name it "Governance & Decision Rights"; the v1.8 manuscript (Table 4-11) names it "I1 授權與問責". See §7 C-1. |
| `M2` | Workflow Routing & Recovery | `M2` "Workflow & Integration / Routing & Recovery" | static | I2 路由與回復 | 53B §3 M2 row (verbatim) | Exact. |
| `M3` | Human–AI Configuration & Response | `M3` "Human–AI Work Configuration / Configuration & Response" | static | I3 人機配置與反應 | 53B §3 M3 row (verbatim) | Exact. |
| `M4` | Evaluation & Assurance | `M4` "Evaluation & Assurance" | static | I4 評估與保證 | 53B §3 M4 row (verbatim) | Exact. |
| `LONGITUDINAL` | longitudinal extension | `M5` "Learning & Resource Feedback" | dynamic | I5 學習與再配置 (M5, dynamic only) | 53B §3 M5 row and §4 `dynamic`; clarification A1 | The mechanism code and the status are merged into one category. See §7 C-2. |
| `DATA_GATED` | data-gated module | `OPTIONAL_DATA_GATED`, or any M plus status `optional` | optional | "條件模組" (conditional module, M3/M4) | 53B §3 `OPTIONAL_DATA_GATED`, §4 `optional`; clarification A2 | 53B allowed two encodings; one category here. See §7 C-2. |
| `EVIDENCE_ONLY` | evidence-layer-only | `EVIDENCE_ONLY` | evidence-only | "僅證據層" (evidence layer only) | 53B §3 `EVIDENCE_ONLY`; clarification B | Exact. Here it is tied to Q1 = NO. |
| `NONE` | none | `OTHER` (with `new_construct_required = yes`) | (static) | — | 53B §3 `OTHER` | **Interpretation.** NONE is read as "an interface exists but no listed category fits", which keeps 53B's `OTHER` outcome. See §7 C-3. |
| `AMBIGUOUS` | ambiguous | `INSUFFICIENT_INFORMATION` | insufficient | — | 53B §3 `INSUFFICIENT_INFORMATION`, §4 `insufficient` | Near match. AMBIGUOUS also covers "two categories tie". |
| Q1 `YES`/`NO`/`UNCERTAIN` | — | no 53B field (closest is the `enterprise_decision_interface` phrase plus `evidence-only` status) | — | 41 §0 rule 4 (the convergence criterion: "does a gap point to an enterprise configuration decision") | New question | New. Q1 has no adopted threshold (protocol 19 §10.4). |

### 5.2 Derived 53B-compatible variables (predeclared; computed by script, never by hand)

These are used only to report the 53B C1/C3/C6 quantities for continuity (protocol 19 §9.3).

| Q2 value | `primary_53B` | `status_53B` |
|---|---|---|
| `M1`–`M4` | same code | `static` |
| `LONGITUDINAL` | `M5` | `dynamic` |
| `DATA_GATED` | Q4 if Q4 ∈ {M1..M4}; otherwise `OPTIONAL_DATA_GATED` | `optional` |
| `EVIDENCE_ONLY` | `EVIDENCE_ONLY` | `evidence-only` |
| `NONE` | `OTHER` | `static` |
| `AMBIGUOUS` | `INSUFFICIENT_INFORMATION` | `insufficient` |

### 5.3 Flattening the sealed researcher key into this category set (applied only at unsealing)

The sealed key stores `(primary, secondary, status)` in 53B vocabulary. It is flattened by the following rule, in this order:

1. status `dynamic` → `LONGITUDINAL`
2. status `optional` → `DATA_GATED`
3. status `evidence-only` → `EVIDENCE_ONLY`
4. otherwise → the primary code (`M1`–`M4`)

The researcher's Q1 is defined as `NO` for `EVIDENCE_ONLY` and as `YES` otherwise. This rule follows the row structure of v1.8 Table 3-4, which lists "I5 學習與再配置 / 條件模組 / 僅證據層" as separate rows from I1–I4. The rule is applied by script to `sealed_key.json` after the coding freeze. No flattened key is written before unsealing.

A secondary, mechanism-level comparison is also reported. It compares `primary_53B` with the key's primary code, and `status_53B` with the key's status. This keeps comparability with 53B §7 and 54C.

## 6. Leakage controls on the stimulus

### 6.1 Item text source

All item text comes from 54A, a frozen pre-coding packet whose SHA-256 is in `v1_blind/FREEZE_MANIFEST.txt` stage 1. The fields used are the family labels, the definitions, `neutral_pair_description` and `network_evidence`. The literature-pattern sentence is one template, identical for all items.

### 6.2 The 132 "文獻解讀" (Literature interpretation) column was screened and NOT used

The script `tools/I/leakage_check_v1_packet.py` searched the 132 column for mechanism-hint terms such as 誰／負責／問責／簽核／停止／回復／例外／流程／門檻／回饋／下一期／試點／分工／配置決策／技術應用前沿／嵌入. Results:

- 10/16 texts contain at least one mechanism hint.
- 1/16 contains only a family-name overlap.
- 5/16 contain no hint term.

The per-item result is in `tools/I/leakage_check_result.json` → `screen_132_literature_interpretation`. Using the clean subset would break the "same wording for all items" requirement, and the 5 clean texts would differ systematically from the others. For this reason no 132 text is used.

### 6.3 Changes relative to the 53B and v2.2.1 coder wording

| Change | Reason |
|---|---|
| The lead phrase "Use it when the connection mainly raises a question of …" is reworded to "Use when the main issue of the connection is …". | The literal 6-word sequence also appears in an AI-pilot rationale. The leakage check flags any AI-pilot text overlap, so the definitions were reworded. The meaning is unchanged. |
| The examples "(e.g., labelled outcomes, score distributions)" in clarification A2 are dropped. Coders now only "name the data". | These examples mirror the researcher's observable-state text for one data-gated pairing in 41/Table 3-4A. They are a potential hint. |
| No example of an "enterprise_decision_interface" phrase is given (53B §5 had one). | The 53B example ("who signs off before a model-based recommendation is executed") describes one specific family pairing. |
| Status and primary code are merged into one Q2 category set; Q1 is new. | This follows the user's specification. The consequences are in §7. |

## 7. Conflicts and flags (reported, not resolved here)

- **C-1. Label of M1 (RESOLVED 2026-10-14, orchestrator instruction).** The coder-facing label is now "Authority & Accountability (授權與問責; = 53B Governance & Decision Rights / authority-to-act)". It aligns the user's label, the manuscript's Table 4-11 wording (授權與問責) and the 53B/41 F1 name. The operational definition is unchanged (53B §3 M1, verbatim). No manuscript assignment is changed.
- **C-2. Two dimensions merged into one.** 53B codes the mechanism (`primary_code`) and the model status (`status`) separately, and 53B C6 requires reliability on both. The user's set merges them: LONGITUDINAL = M5 + dynamic, and DATA_GATED = optional status with any mechanism. Three consequences follow:
  - Q2 reliability is not numerically comparable with 53B C1 or C3.
  - Researcher assignments that combine a mechanism with `optional` status lose their mechanism in the flat comparison. They keep it in the secondary comparison (§5.3).
  - `V1_PASS_HUMAN_C6` can be computed only on the derived variables (§5.2), which is an amendment to frozen 53B (protocol 19 §3).
- **C-3. NONE.** The user listed NONE without a definition. It is defined here as "an interface exists, but no listed category fits", so that 53B's `OTHER` / new-construct outcome is preserved. If the user meant NONE as "no interface", it would duplicate `EVIDENCE_ONLY` + Q1 = `NO`. Please confirm before the freeze. **Open researcher approval (OA-3). It does not block distribution.**
- **C-4. G ID shown to coders (DECIDED: shown).** 53B §1 forbids showing any Gap ID to coders. The user's explicit, newer instruction requires the G ID, so it is shown, and this is recorded as a deviation from 53B §1. Rationale: the AI × decision family pair alone already identifies every item in the public 41 and manuscript tables, so the G ID adds little lookup risk. Blinding rests on recruitment and attestation (protocol 19 §5). `build_v1_construct_packet.py --mask-gid` remains available but is not used.
