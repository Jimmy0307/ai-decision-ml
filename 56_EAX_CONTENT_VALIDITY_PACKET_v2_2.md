# 56 — EA-X (Explanation Usability) Content-Validity Packet v2.2

**Status:** human reviewer packet ready; human content validity **not started**. Any AI ratings are labelled `AI_CONTENT_VALIDITY_PILOT` and are not CVI evidence.

**Consequence until human CVI is complete:** EA-X stays a *conditional candidate*. It may only act as a grouping key for the response distribution `ρ` (42 §6). G13 and G15 may not be upgraded to hard constraints, and EA-X may not appear in any requirement table `EA^req`.

This packet is separate from the G→M blind coding (53B/54). Reviewers of this packet may be the same people as G→M coders only if they complete the G→M coding first.

---

## 1. Construct under review

**EA-X — explanation usability:** the degree to which the people who act on an AI output can *use* the rationale attached to it to check that output. It is distinct from:

- **EA-V (evaluation & assurance evidence):** whether the system has been validated, monitored and revalidated — evidence about the system, not about a user's ability to check one output;
- **H (human intervention right):** whether the user is *allowed* to intervene;
- **user response (ρ):** what the user actually does (use, verify, modify, escalate, reject, bypass).

Background for reviewers: research reports that explanations can increase acceptance of AI advice whether or not the advice is correct (Bansal et al., 2021). EA-X is therefore not assumed to reduce risk; it is a condition under which user responses may differ.

## 2. Candidate anchors (ordinal, cumulative)

| Level | Anchor statement |
|---|---|
| 0 | No usable rationale is available to the person acting on the output. |
| 1 | A rationale is shown and can be read by the person acting on the output. |
| 2 | The person can use the rationale to form at least one concrete, checkable verification question about the output. |
| 3 | In a blinded check, the person can tell when the rationale is insufficient to support the output. |

Levels are intended to be cumulative (level k presumes levels below it).

## 3. Reviewer panel

- 6–8 reviewers spanning governance/risk, IT/data, process owners and frontline users of AI outputs. Panel size is a study convention; the earlier attribution to Lynn (1986) is withdrawn because it could not be verified at a primary source (57, v2.3 section). Analysis: `61_EAX_HUMAN_CVI_ANALYZER_v2_3.py`.
- Each reviewer works independently and signs: "I rated these items independently and have not seen other reviewers' ratings."

## 4. Rating form (one row per anchor; repeat for the construct definition)

| Item | Relevance to EA-X (1 not relevant – 4 highly relevant) | Clarity (1–4) | Representativeness: does the set of levels cover the construct? (1–4, rate once for the whole set) | Ambiguity: could this statement belong to EA-V, H or user response instead? (none / EA-V / H / response / other) | Is the level above this one strictly more demanding? (yes / no / unsure) | Suggested rewording |
|---|---|---|---|---|---|---|
| Definition | | | | | — | |
| Level 0 | | | | | | |
| Level 1 | | | | | | |
| Level 2 | | | | | | |
| Level 3 | | | | | — | |

## 5. Construct-confusion sort (blind)

Present the eight statements below in random order; ask reviewers to assign each to EA-X, EA-V, H, or user response. Two of each are correct by design; misassignments show where wording is confusing.

1. The person can tell when the shown reasons do not justify the output. *(EA-X)*
2. The model was tested before deployment on held-out cases. *(EA-V)*
3. The person may stop the action before it is executed. *(H)*
4. The person accepted the output without checking it. *(response)*
5. The reasons shown let the person ask a checkable question. *(EA-X)*
6. Performance is measured periodically in operation. *(EA-V)*
7. The person may object after the result is known. *(H)*
8. The person escalated the case to a supervisor. *(response)*

(The italic key is removed from the reviewer copy.)

## 6. Analysis plan (pre-registered)

- **I-CVI** per item = proportion of reviewers rating relevance 3 or 4.
- **Modified kappa** per item: k* = (I-CVI − p_c) / (1 − p_c), p_c = [N! / (A!(N−A)!)] · 0.5^N, where N = reviewers and A = reviewers rating 3–4 (Polit, Beck, & Owen, 2007).
- **S-CVI/Ave** = mean I-CVI over the five items; **S-CVI/UA** = proportion of items with universal agreement (Polit & Beck, 2006). Report which one is used.
- Clarity and ambiguity reported descriptively; confusion-sort accuracy per statement.
- **Decision rule:** an anchor is retained if I-CVI ≥ .78 (with ≥ 3 reviewers; Polit et al., 2007) and no more than one reviewer flags it as belonging to another construct; otherwise reword and re-rate. EA-X may leave "conditional candidate" status only if all four levels and the definition are retained **and** a two-round pilot (V2) confirms that levels are distinguishable in practice. Thresholds are study conventions, not universal truths.

## 7. AI content-validity pilot

See §8. AI ratings can only identify wording problems before the human round. They are never pooled with human ratings and never reported as CVI.

## 8. AI_CONTENT_VALIDITY_PILOT results

**Label: `AI_CONTENT_VALIDITY_PILOT` — two AI reviewers (separate contexts, same model family). Not CVI evidence; never pooled with human ratings.**

| Item | R1 relevance / clarity | R2 relevance / clarity | AI "I-CVI" (n = 2, diagnostic only) | Ambiguity flags | Main wording problem raised by both |
|---|---|---|---|---|---|
| Definition | 4 / 3 | 4 / 3 | 1.00 | R1: response (minor) | "check" is vague; separate capability ("is able to") from behaviour (ρ) and from permission (H) |
| Level 0 | 4 / 3 | 4 / 3 | 1.00 | both: circular ("usable") and overlapping Level 1 | define by absence or unreadability, not by "usable" |
| Level 1 | 3 / 3 | 3 / 3 | 1.00 | both: reads as system transparency/display | require that the person can restate what the rationale claims |
| Level 2 | 4 / 3 | 4 / 3 | 1.00 | both: could be confused with the `Verify` response | define "checkable" against information available to the person |
| Level 3 | 4 / 2 | 4 / 2 | 1.00 | R1: EA-V; R2: response + EA-V | the anchor embeds a measurement procedure ("blinded check"); threshold undefined; **not clearly cumulative over Level 2** (both rated "unsure") |
| Representativeness (set) | 3 | 3 | — | — | missing: timeliness of the rationale, access to information needed to answer the verification question, calibration against over-acceptance |

Confusion sort: both AI reviewers sorted all eight statements correctly, but both noted that statements 1 and 5 paraphrase Levels 3 and 2 so closely that the sort tests word-matching, not discrimination.

### 8.1 Consequences for the human round

1. Human reviewers rate **revised anchors v2.2.1** (below); the original anchors are kept in §2 for the record. The revision responds only to wording problems raised in the AI pilot.
2. Cumulativity of Level 3 over Level 2 is an open empirical question for the V2 pilot; the ordinal assumption must not be used until it is checked.
3. Confusion-sort statements 1 and 5 are paraphrased away from the anchor wording.
4. Unchanged: EA-X remains a conditional candidate and a `ρ` grouping key only.

### 8.2 Revised anchors v2.2.1 (for human rating)

| Level | Anchor statement |
|---|---|
| 0 | No rationale specific to this output is shown to the person acting on it, or what is shown cannot be read at the point of action. |
| 1 | A rationale specific to this output is shown at the point of action, and the person can correctly restate what it claims. |
| 2 | Using the rationale and information available in their work setting, the person can state at least one concrete question whose answer would confirm or disconfirm the output. |
| 3 | When shown rationales that do and do not support their outputs (support status hidden), the person identifies the unsupported ones at a rate above a pre-specified threshold. (Scoring procedure and threshold are defined in the V2 pilot protocol, not in the anchor.) |

Revised definition: *The degree to which the person who acts on a specific AI output is able to use the rationale attached to that output to judge whether the output is supported — independent of whether they are permitted to intervene (H) and of what they actually do (ρ).*

Revised confusion-sort statements: (1) "Given several justifications, the person notices which ones do not hold up." (5) "The justification points the person to something they can look up to confirm the result."

## References

Bansal, G., Wu, T., Zhou, J., Fok, R., Nushi, B., Kamar, E., Ribeiro, M. T., & Weld, D. S. (2021). Does the whole exceed its parts? The effect of AI explanations on complementary team performance. In *Proceedings of the 2021 CHI Conference on Human Factors in Computing Systems*. https://doi.org/10.1145/3411764.3445717

Polit, D. F., & Beck, C. T. (2006). The content validity index: Are you sure you know what's being reported? Critique and recommendations. *Research in Nursing & Health, 29*(5), 489–497. https://doi.org/10.1002/nur.20147

Polit, D. F., Beck, C. T., & Owen, S. V. (2007). Is the CVI an acceptable indicator of content validity? Appraisal and recommendations. *Research in Nursing & Health, 30*(4), 459–467. https://doi.org/10.1002/nur.20199
