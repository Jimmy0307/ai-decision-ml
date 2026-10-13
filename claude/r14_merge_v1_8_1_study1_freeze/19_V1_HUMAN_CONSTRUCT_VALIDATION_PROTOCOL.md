# 19 — V1 Human Construct-Validation Protocol (v1.8.1)

**STUDY TEAM ONLY — do not give this file to coders.** It names the sensitivity targets and cites the AI pilot.

**Status: prepared, not run.** This protocol contains no human result. It also contains no simulated coder, no AI answer, no predicted κ or α, and no synthetic agreement. All response cells in packet 20 are empty (Appendix A).

**Research question.** Does each G01–G16 literature pairing correspond to an identifiable enterprise decision mechanism or interface? If it does, which one?

**What this protocol is not.** It does not change any G01–G16 membership or content. It does not change the researcher G→M assignments (41; v1.8 Tables 3-4 / 3-4A / 4-11), the taxonomy, the enterprise model, or any network value.

---

## 1. Files

| File | Role | Coder-facing |
|---|---|---|
| `19_V1_HUMAN_CONSTRUCT_VALIDATION_PROTOCOL.md` | This protocol (study team) | no |
| `20_V1_HUMAN_CONSTRUCT_VALIDATION_PACKET.xlsx` | Coordinator master. Sheets: README_INSTRUCTIONS, CATEGORY_DEFINITIONS, ITEM_INFO, CODER_1, CODER_2, CODER_3_OPTIONAL, ATTESTATION, ADJUDICATION_EMPTY | not distributed |
| `20_V1_HUMAN_CONSTRUCT_VALIDATION_PACKET_CODER_1.xlsx` / `_CODER_2.xlsx` / `_CODER_3_OPTIONAL.xlsx` | One file per coder. Each holds only that coder's sheet, plus instructions, item info (in that coder's order), category definitions and attestation | yes (one file per coder) |
| `21_V1_HUMAN_CONSTRUCT_VALIDATION_CODEBOOK.md` | Codebook. §1–4 mirror the xlsx; §5–7 hold the crosswalk, derived variables and conflicts | no (coders get the xlsx only) |
| `V1_SEALED/RESEARCHER_ASSIGNMENT_COMMITMENT.md` | SHA-256 commitment of the sealed key and of every researcher-mapping file | no |
| `tools/I/build_v1_construct_packet.py` | Builds packet 20 from 54A and the 11-CSV | — |
| `tools/I/leakage_check_v1_packet.py`, `tools/I/leakage_check_result.json` | Leakage check (Appendix A) | — |
| `tools/I/v1_construct_analyzer.py` | **Frozen analysis script** (OA-1). SHA-256 `b5628633a997190a5bf54e25a93c40647ef94494b4ca6f9fe6071454872e278a`, also recorded in V1_SEALED §D | — |
| `tools/I/test_v1_construct_analyzer.py`, `tools/I/test_v1_construct_analyzer_result.txt` | κ/α correctness test (Appendix C) | — |
| `tools/I/no_human_data_run/V1_CONSTRUCT_RESULTS.{json,md}` | Analyzer run on the blank coder files: `NO_HUMAN_DATA` | — |
| `tools/I/item_order_log.json` | Seeds and per-coder item orders | no |

## 2. Inputs read

These are REPO tracked files, base `d2044161`. Hashes are in Appendix B.

- v1.8 manuscript `claude/r14_merge_v1_8_source_closure/08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md` (SHA-256 `1515b0f2…`): §3.9.1–3.9.5 (lines 657–766) and §4.7–4.7.4 (lines 1691–1804);
- `41_G01_G16_CONVERGENCE_AND_CONSTRUCT_FREEZE_v2_1.md`;
- `53A` (a hash stub; the plaintext key is outside git, under `W\…\v2_2\sealed_key_DO_NOT_GIVE_TO_CODERS\`);
- `53B_V1_BLIND_CODING_PROTOCOL_v2_2.md`;
- `54A` and `54B`;
- `54C_AI_BLIND_CODING_PILOT_RESULTS_v2_2.md`;
- `55`;
- `59_V1_HUMAN_VALIDATION_IMPORT_AND_ADJUDICATION_v2_3.md`;
- `60_v1_human_validation_analyzer_v2_3.py`;
- `v1_blind/*` and `v1_human_packet/*`;
- `11_Priority_Gaps_Frozen_Export_G01_G16_v1_0_20261009.csv`;
- `W\…\r14_merge_v1_7\132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX.csv`.

## 3. Relationship to the frozen 53B round (amendment, not replacement)

53B, 54A/54B, 59 and 60 stay frozen and unedited. This instrument is a **v1.8.1 amendment**. It follows the user's specification:

- Q1 is a new question (interface yes/no);
- Q2 uses one flat category set that merges 53B `primary_code` and `status`;
- Q3 confidence is ordinal (53B used 0–100);
- the G ID is shown (53B §1 forbade it).

Consequences:

1. **The 60 analyzer cannot ingest Q1–Q5 sheets. OA-1 is CLOSED.** The dedicated analyzer `tools/I/v1_construct_analyzer.py` (SHA-256 `b5628633…278a`) implements §9–§11. It imports `cohen_kappa`, `kripp_alpha_nominal`, `bootstrap_alpha` and `classify` unchanged from `v1_blind/reliability_v2_2.py`, and checks that file's SHA-256 (`866e9005…48e7`) at runtime. It refuses sheets that are not hash-frozen, fewer than 2 coders, and duplicate or identical sheets. AI coders are excluded procedurally (§4); xlsx sheets carry no coder type.
2. **53B C1/C3/C6 can be computed only on derived variables** (codebook 21 §5.2). Using them for `V1_PASS_HUMAN_C6` is an amendment. The study team must accept it in writing in the freeze record (OA-2).
3. **Two rounds must not be pooled.** If a 53B-format human round is also run, its sheets and the Q1–Q5 sheets are never combined in one reliability statistic.

## 4. Roles

| Role | Who | Constraints |
|---|---|---|
| Coordinator | study team member | Distributes files, receives sheets, hashes them, and runs scripts. Never discusses item content with coders. Never tells a coder anything about another coder's codes. |
| Coders, k ≥ 2 (CODER_1, CODER_2; CODER_3_OPTIONAL recommended) | independent human raters | Work alone and blind (§5). They receive only their own per-coder xlsx. AI coders are never admitted (59 §1; 53B C7). |
| Adjudicator | one person who is **not** a coder, **not** the author of 41, and **not** the translator of any coder-facing material | Acts only after coder sheets are frozen. Sees coder codes and rationales, never the key before adjudication is frozen. If the 41 author must adjudicate, the case is marked `AUTHOR_ADJUDICATED` and reported as a limitation (53B C5). |
| Translator (only if instructions are translated) | a person who is not the adjudicator | The translation is frozen and hashed with the packet before coding. The Chinese family labels in packet 20 are copied from v1.8 Table 3-4A; they are not a new translation. |

## 5. Blinding and its known limits

**What coders must not see before their sheet is frozen:**

- the researcher target category of any item (41, 53A plaintext, sealed_key.json, 54C, 55 Block P, 59 §8, 132, v1.8 manuscript §3.9 / §4.7, `current_artifacts/132_*`);
- AI-pilot answers (`v1_blind/ai_coder_*`, 54C);
- any "correct answer";
- other coders' sheets;
- O/E, counts or q-values.

**Blinding risk (recorded as a limitation, not resolved).**

- 53A itself holds only hashes. However, the same mapping is readable in PUBLIC repository files: 41, 54C (which reproduces the key), and the v1.8 manuscript (Tables 3-4, 3-4A, 4-11). 59 §1 already notes that "54C already reveals the key".
- **The G ID is shown (decided).** The user's explicit, newer instruction overrides 53B §1, and this is recorded as a deviation from 53B §1. Rationale: even without the G ID, the AI × decision family pair alone identifies every item in 41 and in Table 3-4A, so masking would add little blinding. Blinding therefore rests on recruitment and attestation.

**Mitigations:**

- **Recruit coders who have not seen the repository or the manuscript.** Prefer people outside the project team, for example enterprise IT / AI-governance practitioners or IS researchers with no access to the project.
- Coders sign the attestation in sheet ATTESTATION. Its wording is adapted from 53B §8 so that it no longer names file numbers.
- Instructions tell coders not to consult the repository, any manuscript, other coders or an AI assistant.
- A coder who has seen project documents must declare it. That coder is then excluded, or reported separately as `EXPOSED`; never pooled silently.
- The attestation is self-report and cannot be verified. This stays a limitation of V1.

**Further disclosures required in the report:**

- the 53B v2.2.1 clarifications, on which the codebook's order-of-tests is based, were written after the AI pilot was compared with the key (54C §6);
- the v1.8.1 codebook edits (codebook 21 §6.3) were made by a sub-agent that had read the key in order to screen for leakage.

## 6. Materials and item order

- **Items.** There are 16 (G01–G16). Every item uses identical wording; codebook 21 §1 gives the content. Item text comes only from frozen packet 54A. The 132 "文獻解讀" column was screened and rejected: 10/16 texts leak mechanism hints (Appendix A.3).
- **G04, G10, G11.** These items carry no special marking in any coder-facing file. The leakage check verifies that their rows have the same style and the same number of filled cells as every other row.
- **Randomization.** Each coder gets a different item order.
  - Rule: `random.Random(20261014 + k).shuffle(["G01", …, "G16"])` for coder k (Python stdlib). The base seed is **20261014**.
  - CODER_1: G03 G10 G06 G02 G13 G05 G09 G16 G15 G11 G12 G01 G14 G08 G04 G07
  - CODER_2: G08 G10 G03 G06 G01 G02 G04 G16 G13 G07 G15 G11 G14 G09 G12 G05
  - CODER_3_OPTIONAL: G10 G15 G13 G07 G04 G12 G05 G06 G16 G14 G02 G11 G03 G08 G01 G09
  - A further coder k ≥ 4 uses seed 20261014 + k (`--k` option of the build script).
- **Response cells.** All are empty. Q1–Q4 use drop-down data validation; Q5 has a 600-character limit.

## 7. Procedure

| Step | Action | Evidence |
|---|---|---|
| P0 | OA-1 is closed. OA-2 and OA-3 are open researcher approvals that do **not** block distribution (§13). Rebuild the packet only if needed, then rerun the leakage check: it must PASS. | `leakage_check_result.json` |
| P1 | **Freeze V181-S1.** Create `V1_SEALED/FREEZE_MANIFEST_V1_8_1.txt` with the SHA-256 of 19, 20 (master and per-coder files), 21, the commitment file, the analysis script (OA-1) and `item_order_log.json`. Commit before distribution. | manifest |
| P2 | Send each coder only their own `20_…_CODER_k.xlsx`, outside the repository. Log the date and file hash. | delivery log (outside git) |
| P3 | Receive the sheet and the signed attestation. **Format check only:** every Q1–Q3 and Q5 filled, values legal, Q1/Q2 consistency (codebook 21 §2). If a check fails, return only that item number and the rule broken. Never give content feedback. Log every correction request. | correction log |
| P4 | **Freeze V181-S2.** Append the SHA-256 of every returned sheet to the manifest and commit, before any statistic is computed. | manifest |
| P5 | **Stage R (key sealed).** Compute the statistics in §9. | results JSON / tables |
| P6 | **Adjudication.** Disagreements are first discussed by the coders without the key, then go to the adjudicator (§4). Use sheet ADJUDICATION_EMPTY of the master file, or the 59 §6 schema adapted to Q1/Q2/Q4. | adjudication file |
| P7 | **Freeze V181-S3.** Append the adjudication-file hash and commit. | manifest |
| P8 | **Stage K (unsealing).** See §11. | key-comparison tables |
| P9 | **Stage C.** Run the 53B §11 mapping-sensitivity classification for every item whose final code differs from the flattened key. Freeze the classes before they are used. | classes file |

## 8. Coding questions

Codebook 21 gives the questions, definitions, consistency rules and order of tests.

- Q1: interface? YES/NO/UNCERTAIN.
- Q2: best category (M1, M2, M3, M4, LONGITUDINAL, DATA_GATED, EVIDENCE_ONLY, NONE, AMBIGUOUS), answered for every item.
- Q3: confidence HIGH/MEDIUM/LOW.
- Q4: optional secondary category.
- Q5: rationale.

## 9. Analysis plan (predeclared)

**Unit:** item (n = 16).

**Common settings (53B §7, line 86):**

- missing values are not allowed;
- all bootstrap intervals are "95% percentile bootstrap CI over cases (5,000 resamples, seed 20261011)";
- resamples with undefined κ or α (no variance) are dropped and their number is reported (59 §3).

### 9.1 Validation before analysis

The analysis script rejects:

- illegal values;
- Q1/Q2 inconsistency;
- Q4 equal to Q2;
- duplicate or missing G IDs;
- a sheet that is not hash-frozen;
- two coders with identical sheets;
- any coder of type AI (59 §1).

### 9.2 Primary and secondary reliability

| Variable | Scale | Two coders | More than two coders |
|---|---|---|---|
| **Q2 (primary)** | nominal, 9 categories | raw agreement; **Cohen's κ** with bootstrap CI; Krippendorff's α (nominal) with bootstrap CI, so that two- and multi-coder reports share one metric (53B §7) | **Krippendorff's α (nominal)** with bootstrap CI; pairwise raw agreement and κ |
| Q1 (secondary) | nominal, 3 categories | raw agreement; κ with CI; α with CI | α with CI; pairwise κ |
| Q4 | set-valued | mean Jaccard of {Q2 ∪ Q4} over items and coder pairs (53B §7); never in the primary statistic | same |
| Q3 confidence | **ordinal** | descriptive only: distribution and median per coder; median on agreed vs disagreed items | same |

Q3 is never mixed into κ or α of Q1 or Q2, and never used as a weight.

### 9.3 Continuity statistics for 53B

The derived `primary_53B` and `status_53B` (codebook 21 §5.2) get α with CI and κ with CI. They are used only for the `V1_PASS_HUMAN_C6` label, and only if OA-2 is accepted.

### 9.4 Descriptives

- **Per-item agreement.** For each G: number of coders, each coder's Q1/Q2, the modal Q2, the share of agreeing coder pairs, and an all-agree flag. The same is done for Q1.
- **Confusion matrices.** Q2 and Q1, for every coder pair; only the categories actually used are printed.
- **Category frequency.** Q2 per coder and pooled; Q4 per coder.
- **Ambiguity and uncertainty rate.** Per coder and pooled: the share of Q1 = UNCERTAIN, the share of Q2 = AMBIGUOUS, and the share of Q2 = NONE (with its Q5 descriptions listed).

### 9.5 Predeclared sensitivity targets: G04, G10, G11

**Why these three.** In the AI blind pilot both AI coders departed from the researcher assignment on exactly these items (54C §3, lines 36, 38, 46; 54C §4; manuscript §3.9.4, line 755):

- G04 primary and status;
- G11 primary and status;
- G10 status only.

They are the predeclared points of definitional pressure. Coders are not told this.

**Analyses (all reported; none changes the decision rule, which uses all 16 items):**

- (a) per-item coder codes and agreement for each of the three;
- (b) Q2 κ/α with CI recomputed on the 13 items excluding G04, G10 and G11, to show whether overall reliability depends on the contested items;
- (c) after unsealing only: final code vs flattened key, and vs the mechanism-level key (codebook 21 §5.3), for each of the three. AI-pilot codes are shown in a separate "context only" column and are never pooled, substituted or used in adjudication (59 §8).

The evidence-unit boundary-sensitive items G07 and G15 (manuscript §3.9.4) are **not** additional sensitivity targets in this protocol.

### 9.6 What is never computed

- No predicted or simulated κ or α.
- No AI-coder statistic in any human table.
- No Landis & Koch strength labels: 59 §3, line 82, says "Landis & Koch labels are **not** reported".

## 10. Decision rule: RELIABLE / TENTATIVE / UNRESOLVED

### 10.1 Thresholds actually adopted by the sources (quoted exactly)

- **53B §9, line 106 (C1):** "Krippendorff's α (nominal) on primary_code ≥ .800 → `RELIABLE`; .667 ≤ α < .800 → `TENTATIVE`; α < .667 → `NOT_ACCEPTABLE`. Cohen's κ is reported alongside but the decision uses α."
- **53B §9, line 107 (C2):** "If the bootstrap 95% CI lower bound of α is < .667, the result is labelled `IMPRECISE` and at least one additional coder is required before any V1 claim."
- **53B §9, line 111 (C6):** "Requires ≥ 2 independent human coders, C1 ≥ `TENTATIVE` and not `IMPRECISE`, C3 ≥ `TENTATIVE`, and no unresolved `model-structural` change under C4."
- **v1.8 manuscript line 749 (§3.9.3 (3)):** "判定以 α 為準：α ≥ .800 為 RELIABLE，.667 ≤ α < .800 為 TENTATIVE，α < .667 為 NOT_ACCEPTABLE；α 的區間下界低於 .667 時另標為 IMPRECISE，須增加編碼者（.800／.667 兩個門檻依 Krippendorff, 2004，為預先登記的研究慣例；NOT_ACCEPTABLE 與 IMPRECISE 兩類為本研究的操作化）"
- **v1.8 manuscript line 1775 (§4.7.3):** "V1 判定依協定 C6：至少兩位人類編碼者、C1 ≥ TENTATIVE 且非 IMPRECISE、C3 ≥ TENTATIVE、沒有未解的 model-structural 變更，才得到 `V1_PASS_HUMAN_C6`。"
- **Code, `v1_blind/reliability_v2_2.py` lines 67–68:** `c = "RELIABLE" if alpha >= 0.800 else "TENTATIVE" if alpha >= 0.667 else "NOT_ACCEPTABLE"`; `if lo != lo or lo < 0.667: c += "+IMPRECISE"`. The 60 analyzer imports these unchanged (59 §3).

### 10.2 Provenance label: RESEARCH_CONVENTION

The .800 and .667 values are labelled **`RESEARCH_CONVENTION`**, not a universal standard. Their provenance is disputed across the sources:

- the v1.8 manuscript (line 3028, E4) records the Krippendorff (2004) attribution as resolved by an author-postprint check;
- 59 (line 164) still records it as `[VERIFY]` at a primary source;
- 53B C1 carries `[VERIFY]`;
- all three call the values a pre-registered study convention;
- the v1.8 manuscript (line 2713, N36) quotes the source as saying "there are no magical numbers".

### 10.3 Mapping the user's three labels onto the adopted rule (no new threshold)

| Label | Rule (Q2, α nominal, all 16 items, all coders) | Source |
|---|---|---|
| `RELIABLE` | α ≥ .800 **and** CI lower bound ≥ .667 | C1 RELIABLE and not C2 IMPRECISE |
| `TENTATIVE` | .667 ≤ α < .800 **and** CI lower bound ≥ .667 | C1 TENTATIVE and not C2 IMPRECISE |
| `UNRESOLVED` | α < .667 (`NOT_ACCEPTABLE`); or CI lower bound < .667 (`IMPRECISE` → add a coder, C2); or α undefined | union of the C1/C2 failure classes. The sub-label is always printed. |

- **Two coders.** As the user specified, **Cohen's κ (with bootstrap CI) is the primary reported coefficient** for Q2, and secondary for Q1. Krippendorff's α (nominal, with CI) is **reported alongside**. **The RELIABLE / TENTATIVE / UNRESOLVED classification is made on α**, because that is the 53B convention (53B C1: "the decision uses α"). No source adopts a κ threshold, and Landis & Koch labels were dropped (59 §3). This is a recorded divergence from the user's wording, not a STOP (§14 F-2).
- **More than two coders.** α only.
- `V1_PASS_HUMAN_C6` additionally requires:
  - C1 on `primary_53B`;
  - C3 on `status_53B`;
  - adjudication and Stage K completed;
  - no confirmed `model-structural` change.

  This label applies only if OA-2 is accepted.

### 10.4 Rules for which no threshold exists (stated qualitatively; no threshold invented)

| Rule | Statement | Flag |
|---|---|---|
| Q1 reliability | α and κ for Q1 are reported with CI and **not classified**. 53B adopts thresholds only for `primary_code` (C1) and `status` (C3), and Q1 has no 53B counterpart. | `NO_SOURCE_THRESHOLD` |
| Per-item agreement | An item is `AGREED` when all coders give the same Q2. Otherwise it goes to adjudication. No per-item agreement-proportion cut-off is used. | `NO_SOURCE_THRESHOLD` |
| Ambiguity / uncertainty rate | Reported descriptively. A high rate is discussed as a codebook-clarity problem; no cut-off is applied. | `NO_SOURCE_THRESHOLD` |
| Sensitivity (13-item) result | Reported next to the 16-item result. It does not override the decision. | `NO_SOURCE_THRESHOLD` |

## 11. Unsealing procedure (hash commitment)

1. **Precondition.** Freezes V181-S2 (coder sheets) and V181-S3 (adjudication) are committed.
2. The coordinator obtains `sealed_key.json` and the 53A plaintext from outside the repository (`W\…\v2_2\sealed_key_DO_NOT_GIVE_TO_CODERS\`).
3. **Hash check.** SHA-256(`sealed_key.json`) must equal `d1702188359e2efa872ae3d5a3ebdae8b75bb220b49931af4f2f59e524936734`. SHA-256(53A plaintext) must equal `9d9de02bfb68566d94cd7023fbff14b79f29fb5db8cf8d364fb941cb6b2e0d3d`. Both values are committed in 53A, in `v1_blind/FREEZE_MANIFEST.txt` stage 1, and in `V1_SEALED/RESEARCHER_ASSIGNMENT_COMMITMENT.md`; sub-agent I re-verified both on 2026-10-14. **On any mismatch: STOP.** No comparison is made, and the event is reported.
4. **Record the opening.** Append `# KEY_OPENED adjudication=<sha256>` to the manifest. From then on the adjudication file is bound: final codes cannot change.
5. **Compare.**
   - The script flattens the key with the predeclared rule (codebook 21 §5.3) and computes the agreement of the final codes with it.
   - It also computes the mechanism-level comparison on `primary_53B` / `status_53B`.
   - The key is a hypothesis, not ground truth (53B §7).
6. **Mapping sensitivity.**
   - Every changed item gets a 53B §11 class: `mapping-only`, `manuscript-only` or `model-structural`.
   - 41 §7 and manuscript §3.9.5 fallback rules apply.
   - No manuscript assignment is changed by this protocol.

## 12. Limitations (to be reported with any result)

- The mapping is public (§5). Coder blinding rests on recruitment and self-attestation.
- n = 16 items gives wide intervals. A C2 `IMPRECISE` result is plausible with two coders, so recruiting CODER_3 from the start is recommended. This is a recommendation, not a threshold.
- The codebook merges mechanism and status into one category set (codebook 21 §7 C-2).
- The order-of-tests and the definitional edits were informed by the AI pilot and written by people or agents who knew the key (§5).
- Family names share words with category labels (Evaluation, Accountability, Assurance; Appendix A.4). Coders are instructed not to code on shared words.

## 13. Open actions before distribution

| ID | Action | Owner |
|---|---|---|
| OA-1 | **CLOSED 2026-10-14.** Analyzer `tools/I/v1_construct_analyzer.py` (SHA-256 `b5628633a997190a5bf54e25a93c40647ef94494b4ca6f9fe6071454872e278a`). Correctness test PASS (Appendix C). The run on the blank packet returns `NO_HUMAN_DATA`. | done |
| OA-2 | Researcher approval, **open, not blocking distribution**: accept or reject the derived-variable route for C1/C3/`V1_PASS_HUMAN_C6` (§3 item 2). Until accepted, the derived statistics are reported as continuity only, and no `V1_PASS_HUMAN_C6` label is issued. | user / PI |
| OA-3 | Researcher approval, **open, not blocking distribution**: confirm the meaning of `NONE` (codebook 21 §7 C-3). The codebook definition is used unless changed **before** freeze V181-S1. | user / PI |
| OA-4 | Recruit k ≥ 2 coders (3 recommended) and one adjudicator who meet §4–§5. | study team |

## 14. Conflicts and flags found while preparing

- **F-1. Category labels vs manuscript (M1 label RESOLVED).** The coder-facing M1 label is now "Authority & Accountability (授權與問責; = 53B Governance & Decision Rights / authority-to-act)". This aligns the user's label, the manuscript's Table 4-11 wording and the 53B/41 name. The operational definitions are unchanged. The other crosswalk entries: M5 → LONGITUDINAL; `OPTIONAL_DATA_GATED` / status `optional` → DATA_GATED; `OTHER` → NONE (OA-3); `INSUFFICIENT_INFORMATION` → AMBIGUOUS. No assignment conflict was found: 41 §2, `sealed_key.json` and v1.8 Table 3-4/3-4A agree item by item.
- **F-2. κ vs α as the decision coefficient.** The user names κ as primary for two coders. 53B C1 and manuscript line 749 decide on α. κ is reported as primary; the classification uses α. This is a design divergence, not a numeric κ conflict, so it is not a STOP condition.
- **F-3. G ID shown vs 53B §1 (DECIDED: shown, per the user's instruction).** This is a recorded deviation from 53B §1 (§5; codebook 21 §7 C-4).
- **F-4. Flat category set vs 53B two-dimension coding.** See §3 and codebook 21 §7 C-2.
- **F-5. 132 literature-interpretation text leaks mechanism hints** in 10/16 items. It was not used (Appendix A.3).

No STOP condition was met: no 84–85/120 conflict, no G07/G15 evidence conflict, no G01–G16 membership conflict, no numeric κ conflict, and no enterprise-model change.

---

## Appendix A — Leakage check result

- **Script:** `tools/I/leakage_check_v1_packet.py`, SHA-256 `6d6a3ddc4f9b8a7fdcf3a5c1acf227197b771262d6d14e6b1b75a00c1eb38473`. It was run with `python -E -P` instead of `-I`, because openpyxl is installed only in the user site-packages, which `-I` disables.
- **Result file:** `tools/I/leakage_check_result.json`.
- **Verdict: PASS. 0 findings across 4 coder-facing workbooks.** The check was re-run on 2026-10-14 after the M1 relabel and rebuild.

### A.1 Checks performed on every coder-facing workbook

The four workbooks are the master and the three per-coder files.

| Check | Result |
|---|---|
| Response cells (Q1–Q5) and attestation answer cells empty | PASS. 0 non-empty cells in every file. |
| Each per-coder file contains exactly one CODER sheet | PASS. CODER_1, CODER_2 and CODER_3_OPTIONAL files each have one. |
| No cell contains a G ID together with a category code | PASS |
| No category code appears in any item row (CODER_*, ITEM_INFO, ADJUDICATION_EMPTY) | PASS |
| No researcher / AI-pilot vocabulary (I1–I5, anchor, Merge, Keep, bridge, static core, researcher, sealed, key, 41_, 53A, 54C, 132, convergence, pilot, AI coder, contested, sensitivity, 爭議, 研究者, 裁決, 答案, static, dynamic, evidence-only, O/E, q=, p_BH) | PASS |
| No mechanism-hint terms in item text (Literature_pattern, Evidence_description) | PASS. The scan covers 38 English and 21 Chinese hint terms; family names are masked during the scan (see A.4). |
| No overlap with AI-pilot output text | PASS. The check compares 6-word shingles with 1,161 AI-pilot shingles from `ai_coder_A_output.csv` and `ai_coder_B_output.csv` (rationale and interface phrase). 1 shingle that already occurs in the pre-coding 53B / v2.2.1 codebook text was excluded. An earlier build failed this check on the codebook lead phrase, which was then reworded (codebook 21 §6.3). |
| No network numbers (Observed, E, O/E, q) | PASS. 85 numeric strings from the 11-CSV were checked. |
| G04, G10, G11 rows carry no special marking (same fill, font and number of filled cells as all other rows) | PASS |
| The packet's G ID ↔ family-pair mapping equals the sealed case map | PASS. Only equality is checked; no assignment is printed. |
| Codebook 21: no line pairs a G ID with a category | PASS |

**Negative control.** A scratch copy of the CODER_1 file was deliberately contaminated with:

- a filled Q1 cell;
- "researcher: M5 dynamic anchor" in an item cell;
- "G04 EVIDENCE_ONLY";
- a bold item row.

The checker reported all of them:

- `NON_EMPTY_RESPONSE_CELL`;
- `CATEGORY_CODE_IN_ITEM_ROW`;
- `FORBIDDEN_TOKEN` (×3);
- `G_ID_AND_CATEGORY_IN_SAME_CELL`;
- `SPECIAL_MARKING_OF_SENSITIVITY_ITEM`.

The scratch copy lives in the session scratchpad only. It was not written to OUT.

### A.2 Coder-facing files checked

| File | SHA-256 | Non-empty response cells |
|---|---|---|
| `20_V1_HUMAN_CONSTRUCT_VALIDATION_PACKET.xlsx` | `4a79b66be262f7b553e9ecf04507857ae494f036bdb73afeb0746b6d4f921f2c` | 0 |
| `20_V1_HUMAN_CONSTRUCT_VALIDATION_PACKET_CODER_1.xlsx` | `99eb27aff52054fa0f9e81a1d98630e631d20a340b997617fb528630e01b96c3` | 0 |
| `20_V1_HUMAN_CONSTRUCT_VALIDATION_PACKET_CODER_2.xlsx` | `7529b83e9dd1df8df865056b3259eba308b41b85262177fa36daf2c3b93dbad0` | 0 |
| `20_V1_HUMAN_CONSTRUCT_VALIDATION_PACKET_CODER_3_OPTIONAL.xlsx` | `2fa5b15d8f72e53e35a93b41099f9197face5145ec84393ff238f76f375302c2` | 0 |

The xlsx files are content-reproducible but not byte-reproducible, because openpyxl writes timestamps. Re-freeze the hashes at V181-S1 after any rebuild.

### A.3 Screen of the 132 "文獻解讀" column (alternative item-text source; not used)

| Result | Items |
|---|---|
| Mechanism hint present (`LEAKS_MECHANISM_HINT`) | G01 (分工), G02 (誰, 負責, 問責, 審), G03 (回復, 例外, 流程), G04 (配置決策, 組織配置, 技術應用前沿), G08 (誰, 問責, 簽核), G10 (門檻), G11 (回饋, 下一期, 審), G12 (試點), G14 (流程, 嵌入), G16 (誰, 負責, 問責, 停止) — 10/16 |
| Family-name overlap only | G06 (審) — 1/16 |
| No hint term found | G05, G07, G09, G13, G15 — 5/16. G07's text also discloses a count ("O = 2"). |

**Decision.** No 132 text is used. Item text comes from frozen 54A for all 16 items.

### A.4 Lexical overlap (inherent in the stimulus; reported, not removable)

Family names that share a word with a category label:

- "Evaluation and Audit" (evaluation);
- "Evaluation and Selection" (evaluation);
- "Human Review and Accountability" (accountability);
- "Explanation and Assurance" (assurance).

The family names are the stimulus and cannot be changed (taxonomy freeze). The codebook instructs coders not to code on shared words (rule 3).

## Appendix B — Input hashes (SHA-256)

| File | SHA-256 |
|---|---|
| 08 v1.8 manuscript | `1515b0f241846b98a16bea7b13f07d1f82fa9199e1331c2228ffce1d04f7ad58` |
| 41 | `b660fd93875c44cf1fb8ffce3a977295d78d4f225937f10c7e115fa508364e02` |
| 53A (stub) | `2f864f58a800f17bfd38bf16541f7eff7126c6e1164093159a0d03d72fcc5561` |
| 53B | `994ac34b5bcd84697ed9bc9ee383dbe659192c45c25bd3671e91acc240e57223` |
| 54A | `517675e7491212c4630d190c5b082ff3f7a6904a1f5d84047be79d8b84d07f4d` |
| 54B | `62107a9ae8aeeb7fa31ec7504f97bd67a7fb4586ee63892bfca80dfeee83df7a` |
| 54C | `b05c72b3071547810b1fa2a2e6cce8d98b30ceb5fb5e8d2e1bd1e52307abdb63` |
| 55 | `cdb4ac86860af5a13fb0de9c5671560d00aeb2ed817d4bce32264886085a4e18` |
| 59 | `9941c21ece3fba23c18fa6818ee16b6a96015320f893943fe3bcc7b4ab4b66b8` |
| 60 | `39b360230045f512de3226cc1e82e7e1c916f4f7b6c3151cce5609f0d12ca9d8` |
| v1_blind/reliability_v2_2.py | `866e9005da8a20e996c93b5c8f6bee916992f24d60c6a96e8f1dcda4556848e7` |
| v1_blind/FREEZE_MANIFEST.txt | `3b56d5ccc070bd808d383e24402b1222518fdfd073ebd4b40608ebf45ddaf305` |
| 11 G01–G16 frozen export | `76a2a00c078ee10168e1f6aece6c26b7507cede0019045528f1fd8695d29209d` |
| W 132 csv (r14_merge_v1_7) | `7f7d06c4c7d91777dfc2baf7c959a7538780a6a88ffbeec0e891c0d0e7b5aef3` |
| tools/I/build_v1_construct_packet.py | `26d2f7da851d63da8fa7581e8c26b7dba5c92d90e919dd32349223f8e5ddc621` |

## Appendix C — Analyzer verification (OA-1)

- **Analyzer.** `tools/I/v1_construct_analyzer.py`, SHA-256 `b5628633a997190a5bf54e25a93c40647ef94494b4ca6f9fe6071454872e278a`.
  - It computes exactly the metrics of §9: Q2/Q1 raw agreement, κ with bootstrap CI and α with bootstrap CI (5,000 resamples, seed 20261011); the Q2 RELIABLE/TENTATIVE/UNRESOLVED class (§10.3); derived 53B continuity statistics; Jaccard; per-item agreement; confusion matrices; category frequency; UNCERTAIN/AMBIGUOUS/NONE rates; Q3 descriptives (never in κ/α); and 16-item vs 13-item results (G04/G10/G11 excluded).
  - Output is JSON plus markdown.
  - `--unseal` first checks SHA-256(`sealed_key.json`) against V1_SEALED table A and requires a hash-frozen adjudication file. On mismatch it stops.
- **Run on the blank packet.** `python -E -P v1_construct_analyzer.py <CODER_1.xlsx> <CODER_2.xlsx> <CODER_3_OPTIONAL.xlsx> --out tools/I/no_human_data_run` returned **`NO_HUMAN_DATA`** with exit 0. Nothing was computed. The output (`V1_CONSTRUCT_RESULTS.json` / `.md`) lists only the input hashes.
- **Correctness test.** `tools/I/test_v1_construct_analyzer.py` (SHA-256 `7fa7b3231a25d17bec4e632df4891ad7707caaf4e4873b5ebca574419f8ad002`) compared the analyzer with independent reference implementations on 300 random label vectors generated in memory (seed 987654321; never written to disk):
  - the analyzer's κ against `sklearn.metrics.cohen_kappa_score` (scikit-learn 1.9.1);
  - the analyzer's α against `krippendorff.alpha(level_of_measurement="nominal")` (krippendorff 0.9.0);
  - the §10.3 boundary rule.

  The test was run in `.venv_docx`. Result: **`PASS kappa_max_abs_diff=2.220e-16 (n=300) alpha_max_abs_diff=4.441e-16 (n=300) classification_rule=PASS`** (`tools/I/test_v1_construct_analyzer_result.txt`).
- **Limit.** The full stage-R pipeline on filled sheets was not exercised end to end, because the instructions forbid creating answer-filled workbooks. Only the statistical core and the `NO_HUMAN_DATA` path are verified.

FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION
FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET
FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED

V1_HUMAN_CONSTRUCT_VALIDATION_STATUS=READY_TO_RUN
