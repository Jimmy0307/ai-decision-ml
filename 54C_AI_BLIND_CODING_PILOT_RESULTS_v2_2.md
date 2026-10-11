# 54C — AI-BLIND-CODING PILOT Results v2.2

**Label: `AI-BLIND-CODING PILOT`. This is not human blind coding, not V1 PASS, and not independent human construct validation.**

Verdicts: `AI_BLIND_CODING_PILOT_ACCEPTABLE` (by the 53B §9 statistics) · `V1_AI_PILOT_COMPLETE` · `V1_HUMAN_BLIND_CODING_PENDING`

---

## 1. Procedure actually followed

| Step | Evidence |
|---|---|
| Protocol, packets and sealed key hashed before any coding | `v1_blind/FREEZE_MANIFEST.txt` stage 1; commit `c409a8c` |
| Two AI coders (separate sub-agent contexts, same underlying model family) each instructed to read exactly one prompt file containing 53B §1–§8 and its own packet (A or B row order); no access to 41, 44, 53A or each other | prompts `coder_prompt_A.txt` / `coder_prompt_B.txt`; each agent reported 1 tool use |
| Outputs saved and hashed before the key was opened | `v1_blind/ai_coder_A_output.csv`, `…B_output.csv`; manifest stage 2; commit `2ecf33d` |
| Key opened; statistics computed with the pre-registered script | `v1_blind/reliability_v2_2.py` → `v1_blind/ai_pilot_reliability_v2_2.json` |

Residual blinding risk: both coders ran on the same machine as the repository; they were instructed not to read other files and each made a single read call. This is weaker than human blinding and is recorded as a limitation.

## 2. Inter-coder reliability (AI A vs AI B)

| Field | Raw agreement | Cohen's κ | Krippendorff's α (nominal) | 95% bootstrap CI | 53B class |
|---|---|---|---|---|---|
| primary_code | 16/16 | 1.000 | 1.000 | [1.000, 1.000] | RELIABLE |
| status | 16/16 | 1.000 | 1.000 | [1.000, 1.000] (3,183 of 5,000 resamples had variance) | RELIABLE |
| primary ∪ secondary (Jaccard, mean) | — | — | — | — | 0.844 |

Median confidence: 65 (both coders).

**Interpretation.** Perfect agreement between two instances of the same model family is expected and is **not informative about human reliability**: the raters share training, priors and the same reading of the codebook. Its only use is diagnostic — it shows the codebook can be applied consistently, and it exposes where *both* AI coders depart from the researcher key in the same direction, which marks definitional pressure points for the human round.

## 3. Comparison with the researcher key (revealed after freezing)

| Case | Gap | AI A (primary/secondary/status, conf.) | AI B | Researcher key (41) | Primary = key | Status = key |
|---|---|---|---|---|---|---|
| C01 | G11 | M4/M5/static (55) | M4/M5/static (60) | M5/M4/dynamic | ✗ | ✗ |
| C02 | G01 | M3/—/static (80) | M3/—/static (70) | M3/—/static | ✓ | ✓ |
| C03 | G04 | M4/M3/static (60) | M4/—/static (50) | EVIDENCE_ONLY/—/evidence-only | ✗ | ✗ |
| C04 | G02 | M1/M3/static (70) | M1/M3/static (70) | M1/M3/static | ✓ | ✓ |
| C05 | G12 | M5/—/dynamic (65) | M5/—/dynamic (50) | M5/M4/dynamic | ✓ | ✓ |
| C06 | G15 | M4/M3/static (65) | M4/M3/static (65) | M4/M3/static | ✓ | ✓ |
| C07 | G05 | M4/M1/static (55) | M4/M3/static (60) | M4/M1/static | ✓ | ✓ |
| C08 | G14 | M2/—/static (60) | M2/—/static (45) | M2/M3/static | ✓ | ✓ |
| C09 | G06 | M4/—/static (80) | M4/—/static (75) | M4/—/static | ✓ | ✓ |
| C10 | G07 | M3/—/static (80) | M3/—/static (70) | M3/—/static | ✓ | ✓ |
| C11 | G10 | M3/M1/static (50) | M3/M4/static (45) | M3/M4/optional | ✓ | ✗ |
| C12 | G03 | M2/M1/static (55) | M2/M4/static (50) | M2/M1/static | ✓ | ✓ |
| C13 | G09 | M1/—/static (65) | M1/—/static (60) | M1/—/static | ✓ | ✓ |
| C14 | G08 | M1/M3/static (75) | M1/M3/static (70) | M1/M3/static | ✓ | ✓ |
| C15 | G13 | M4/—/static (75) | M4/—/static (65) | M4/M3/static | ✓ | ✓ |
| C16 | G16 | M1/M2/static (70) | M1/M2/static (70) | M1/M2/static | ✓ | ✓ |

Primary-code agreement with key: 14/16 per coder. Status agreement with key: 13/16 per coder. All 12 researcher "static" cases were coded static with the same primary mechanism by both AI coders.

## 4. Disagreement map

| Case / Gap | Type | What the AI coders did | Pressure point |
|---|---|---|---|
| C03 / G04 Generation × Prediction | primary + status | M4 static (lowest confidence 50–60); B's rationale names "technology frontier" as plausible alternative | `EVIDENCE_ONLY` competes with a generic M4 "validate the output" reading that fits almost any AI × prediction pairing. The codebook gives no test for "distinct" configuration decision. |
| C01 / G11 Evaluation × Allocation | primary + status | M4 static with M5 as secondary | Both coders see a static assurance gate on allocation (validated inputs before a plan is committed) and the feedback loop only as secondary. The researcher reads the pairing as cross-period feedback. |
| C11 / G10 Risk estimation × Selection | status | M3 static (lowest confidence 45–50) | The data condition (score distribution + labelled truth) that makes the researcher call it `optional` is not salient to coders; the status table's `optional` definition is not operationalised. |
| C08 / G14 Risk estimation × General process | none vs key, but low confidence (45) | B flags `EVIDENCE_ONLY` as plausible because the decision family is a residual category | Residual decision families need a coding rule. |
| C07, C11, C12 | secondary only | different secondary codes (M1 vs M3; M1 vs M4; M1 vs M4) | Secondary codes are noisy; consistent with 53B not using them in the primary statistic. |

## 5. Mapping-sensitivity analysis (53B §11)

| Case / Gap | Alternative (AI) | 42 elements tied to the key code | Would the element stay in 42 anyway? | Classification |
|---|---|---|---|---|
| G04 → M4 static | G04 joins I4 | none (G04 had no model element) | n/a — I4 already contains `EA ≥ EA^req`; a generative-AI diagnostic initiative is just another initiative `j` | **mapping-only**; manuscript counts change (static 13, evidence-only 0); 44 §3.4/4.1 tables and the sentence "G04 留在證據層" must be marked as researcher adjudication pending V1 |
| G11 → M4 static (M5 secondary) | G11 joins I4 at enterprise level, beside G05 | M5 dynamic block (D1) | Yes — M5 remains for G12 and for 38/39 architectural reasons; the static I4 gate (`y_EVAL ∈ Pre`, auditable allocation output) already exists through G05 | **mapping-only** (+ manuscript-only: M5 rests on G12 alone; 41 §3 Q4 merge "G11+G12" must be flagged as disputed) |
| G10 → static (M3) | G10 becomes core rather than optional | threshold variants `k_τ ∈ M_j` | Yes — any `k ∈ M_j` already requires `P(z,ω|k)` to be identified; the data gate is enforced by identification rules (43 Block R), not by the mapping | **mapping-only**; manuscript states that G10's "optional" status is an identification condition, not a mechanism difference |

**Result:** none of the three AI-pilot disagreements is `model-structural`. The equations of 42 do not depend on whether G04, G10 or G11 carry the researcher code or the AI-pilot code; only the counts in 41/44 and the wording of the convergence claims change. This is a property of the current design (gaps select model elements but never parameterize them) and should be re-checked after the human round.

## 6. Changes carried into the human round (logged, not applied to 53B)

The 53B protocol remains frozen. Clarifications for human coders are added in `v1_human_packet/CODER_CLARIFICATIONS_v2_2_1.md`; they address only ambiguities named in the AI coders' own rationales and are worded symmetrically (they do not indicate which answer is expected):

1. a three-question status decision procedure (cross-period outcomes needed? → `dynamic`; configuration exists only if a named dataset exists? → `optional`; else a distinct configuration choice? → `static`, otherwise `evidence-only`);
2. a "distinctness" test for `EVIDENCE_ONLY` versus a generic mechanism;
3. a rule for residual decision families;
4. a reminder that secondary codes are optional and should be left blank unless clearly necessary.

Because the study team saw the key comparison before writing these clarifications, the human-round report must disclose this sequence.

## 7. What this pilot does and does not establish

- Establishes: the packets are usable; the codebook can be applied consistently by one model family; three cases (G04, G10, G11) are where the researcher's convergence is most contestable; no pilot disagreement changes the model structure.
- Does not establish: human inter-rater reliability; construct validity of M1–M5; any V1 gate. **V1 remains `V1_HUMAN_BLIND_CODING_PENDING`.**
