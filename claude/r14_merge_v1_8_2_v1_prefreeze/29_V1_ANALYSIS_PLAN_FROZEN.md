# 29 — V1 Analysis Plan (FROZEN at S1, v1.8.2)

This plan is implemented by `tools/v1_construct_analyzer_v182.py`. Its SHA-256 is in `V1_SEALED/RESEARCHER_ASSIGNMENT_COMMITMENT.md` §C and in `V1_SEALED/FREEZE_MANIFEST_V1_8_2_S1.txt`.

No result, simulated value, expected α/κ or synthetic agreement appears in this plan.

## 0. Question and bounded claim

- **Primary question:** do three independent human coders agree on which enterprise decision category each of the 16 depleted literature pairings represents? This is a question of inter-rater reliability.
- **Not the primary question:** agreement with the researcher's key. The key is a hypothesis, not ground truth.
- **Bounded claim:** V1 validates only the G → enterprise-mechanism interpretation. It does not validate the 32-cell membership, the taxonomy or the network statistics.

## 1. Data and units

- **Unit:** item (n = 16), identified by neutral ID ITEM-A01…ITEM-A16.
- **Coders:** CODER_1, CODER_2, CODER_3, all human (`N_HUMAN_CODERS=3`).
- **Missing data:** none allowed. Every validation rule in codebook 26 §2 is enforced.
- **Rejected sheets:** the analyzer rejects sheets that are not hash-frozen at S2, sheets with identical content, and sheets with a count other than 3.

## 2. Phase R — reliability (researcher key and item map stay sealed; neutral IDs only)

### A. CURRENT_INSTRUMENT_RELIABILITY (primary)

| Metric | Specification |
|---|---|
| **PRIMARY** | Krippendorff's α (nominal) on Q2, all 16 items, 3 coders (`PRIMARY_RELIABILITY=KRIPPENDORFF_ALPHA_Q2_3_CODERS`). |
| CI | 95% percentile bootstrap over items, 5,000 resamples, seed 20261011. Resamples with undefined α or κ are dropped and their number is reported. |
| Raw agreement | Number of items where all 3 coders agree, pairwise raw agreement, and mean pairwise raw agreement. |
| Category frequencies | Q2 per coder and pooled. |
| Secondary | Pairwise Cohen's κ for 1v2, 1v3 and 2v3, each with a bootstrap CI (`PAIRWISE_KAPPA=SECONDARY`). |
| Q1 | α (nominal) plus pairwise κ with CIs. **No pass/fail** (no source threshold). |
| Q3 | Descriptive only: distribution and lower median per coder, and medians on agreed versus disagreed items. Never used as a weight, and never entered into κ or α. |
| Q4 | Set-based Jaccard of {Q2 ∪ Q4}, mean over items and coder pairs. Nothing else is computed for Q4. |
| Per item | Each coder's Q2 and Q1, modal Q2, pair-agreement share, and AGREED / TO_ADJUDICATION status. |
| Confusion matrices | Q2 and Q1 for each coder pair. |
| Rates | Q1 = UNCERTAIN, Q2 = AMBIGUOUS and Q2 = NONE, per coder and pooled. Every NONE row is listed with its Q5 text. |

### B. 53B_CONTINUITY_RELIABILITY (secondary; never collapsed with A)

- The derived `primary_53B` (C1) and `status_53B` (C3) (codebook 26 §5) are analysed with α and the 53B C1/C3 classes. They are reported in their own section.
- "V1_PASS_HUMAN_C6 is a continuity label under the earlier 53B protocol, not evidence that the amended Q1–Q5 instrument is identical to 53B."

## 3. Classification (`THRESHOLD_PROVENANCE=RESEARCH_CONVENTION`)

The classification applies to α on Q2, computed over the primary scope.

| Rule | Label |
|---|---|
| α ≥ .800 | RELIABLE |
| .667 ≤ α < .800 | TENTATIVE |
| α < .667 | UNRESOLVED/NOT_ACCEPTABLE |
| CI lower bound < .667 | IMPRECISE (appended to the label) |
| α undefined | UNRESOLVED |

**Sources.** The rules come from 53B §9 C1/C2 (lines 106–107), v1.8 manuscript line 749 and `v1_blind/reliability_v2_2.py` lines 67–68.

**Provenance.** The attribution of these thresholds to Krippendorff (2004) is disputed across the source documents: 59 still marks it `[VERIFY]`, while the v1.8 manuscript (E4) records it as resolved. The thresholds are therefore labelled a research convention:
- they are not universal;
- Landis & Koch labels are not used;
- κ has no adopted threshold.

**No threshold is invented** for Q1, for per-item agreement, or for the ambiguity rate. These are reported descriptively.

## 4. Exposure handling

- **When a coder is EXPOSED.** A coder is `EXPOSED` if they answer NO to any attestation statement, or if the coordinator flags them (`--exposed CODER_k`).
- **Reporting.** If anyone is exposed, the analyzer reports both `ALL_CODERS_INCLUDES_EXPOSED` and `CLEAN_CODERS_ONLY`, labelled; they are never silently pooled.
- **Primary scope:** the clean coders.
- **Fewer than 3 clean coders.** Recruit a replacement coder, who receives a fresh copy of the same S1-frozen `CODER_k.xlsx`, so the file hash is unchanged.
- **Fewer than 2 clean coders.** Primary reliability is `NOT_COMPUTABLE`.

## 5. Phase A / S3 — adjudication

- **Discussion.** Coders discuss their disagreements without the key.
- **Adjudicator.** Remaining disagreements go to an adjudicator who is not a coder, not the author of 41, and not a translator. If the author adjudicates, the decision is recorded as `AUTHOR_ADJUDICATED` and treated as a limitation.
- **Adjudication file.** It is a CSV with columns `Item_ID,Final_Q1,Final_Q2,Final_Q4,Route,Adjudicator_role,Evidence_used,Rationale`, keyed by neutral ID.
- **S3 freeze.** S3 is complete when the SHA-256 of that CSV is written into `V1_SEALED/FREEZE_MANIFEST_V1_8_2_S3.txt`. Nothing below unlocks without it.

## 6. After S3 only

1. **Sensitivity (G04, G10, G11).**
   - `--item-map` (from SEALED_LOCAL) is accepted only if its SHA-256 equals `ITEM_ID_TO_GID_MAP.COMMITMENT.md`.
   - Section A and section B are recomputed on 13 items, excluding the three study-team-only sensitivity targets.
   - The 16-item result stays the decision basis.
   - Why these three: in the AI pilot, both AI coders departed from the researcher assignment on these items (54C §3–§4). AI-pilot codes are context only and are never pooled.
2. **Phase K — unsealing.**
   - `--unseal` is refused unless all of the following hold: the S3 manifest verifies the adjudication file; the item map verifies; and SHA-256(`sealed_key.json`) equals `d1702188359e2efa872ae3d5a3ebdae8b75bb220b49931af4f2f59e524936734` (from `RESEARCHER_ASSIGNMENT_COMMITMENT.md` §A).
   - The opening is logged in the S3 manifest.
   - The final codes are compared with the flattened key (codebook 26 §6) and at mechanism level.
3. **Phase C.**
   - Every changed item gets a 53B §11 class (`mapping-only`, `manuscript-only` or `model-structural`), recorded in a classes CSV frozen in its own manifest.
   - The analyzer then reports the `V1_PASS_HUMAN_C6` continuity label (section B only). It requires: ≥ 2 clean coders; C1 ≥ TENTATIVE and not IMPRECISE; C3 ≥ TENTATIVE; and no `model-structural` change.
   - A `model-structural` change is handled through the 41 §7 and manuscript §3.9.5 fallback rules. This plan changes no assignment.

## 7. Verification of the analyzer (pre-freeze)

- **Correctness test.** `tools/test_v1_construct_analyzer_v182.py` uses only random label vectors generated in memory; nothing is written to disk. Result (`tools/test_v1_construct_analyzer_v182_result.txt`): `PASS kappa_vs_sklearn_max_abs_diff=2.498e-16 (n=300) alpha_vs_krippendorff_max_abs_diff=4.441e-16 (n=300) classification_rule=PASS oa3_none_validation=PASS`.
- **Blank-packet run.** The run on the three blank coder files returns `NO_HUMAN_DATA` and computes nothing (`tools/no_human_data_run_v1_8_2/`).
- **Not verified.** The full pipeline has not been run end to end on filled sheets, because no answer-filled workbook may be created before human coding.
