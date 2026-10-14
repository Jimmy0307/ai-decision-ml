# 65 — V1 Coder Packet: Pre-Distribution Review (independent, read-only)

**Reviewer:** sub-agent V. This was a read-only review. No packet, workbook, protocol or manifest was modified. The sealed folder `outputs\20_SEALED_PRIVATE\` was not opened. The two `SEALED_LOCAL:` plaintext lines in the S1 manifest were skipped. Files 53A, 41, 54C, Tables 3-4/3-4A and manuscript §3.9.2/§3.9.4 were not read. No coder was simulated, no answer was filled in, no α or κ was estimated, nothing was sent or committed.

**Reviewed:**
- `r14_merge_v1_8_2_v1_prefreeze/coder_distribution/CODER_{1,2,3}.xlsx`, which are the S1-frozen copies;
- the local distribution copies in `outputs\00_CURRENT\03_V1_HUMAN_VALIDATION\01_CODER_PACKETS_READY_TO_SEND\PACKETS\`;
- files 24, 25, 26, 27, 28, 29 and 30;
- `V1_SEALED/FREEZE_MANIFEST_V1_8_2_S1.txt`.

**Scripts:** `outputs\00_CURRENT\07_V1_PACKET_REVIEW_WORK\`:
- `check_packets.py` re-hashes the manifest and scans cells plus raw XML;
- `diff_local_copy.py` compares the local copy with the repo copy;
- `dump_packet.py` dumps the packet contents.

**Machine-readable results:** `65_V1_CODER_PACKET_CHECKS.json`, next to this memo.

---

## A. CURRENT_PACKET_STATUS

**REVISION_RECOMMENDED.**

- **The S1 repository packets pass every Task-1 check** (see the table below).
- **One BLOCKING distribution issue (B-1).** The local "ready to send" copy of `CODER_1.xlsx` is **not** the S1 file. It has been round-tripped through Google Sheets, and its SHA-256 no longer matches S1. It must not be sent.
  - Fixing this needs a byte-exact re-copy from the repo. It does **not** need a packet revision or an S1 re-freeze.
- **Content issues.** There are several non-blocking content issues: attestation double negatives, a "GitHub" cue, a technical depletion statement, an under-estimated time, and wording inconsistencies in the order of tests. I would fix them before sending, because no coder has received a packet yet.
  - **Adopting any of them changes the packet hashes and needs a new S1 freeze** (S1b, versioned and disclosed).
  - If the researcher keeps the packet as is, it can be sent once B-1 is fixed.

### Task-1 (S1 verification) results, computed by script

| Check | Result |
|---|---|
| S1 manifest: 21 committed entries re-hash equal (2 SEALED_LOCAL lines skipped) | **PASS** (21/21) |
| `S1_HASH_CHANGED` | **NO** |
| `CODER_COUNT` | 3 |
| `ITEMS` per coder | 16 / 16 / 16. Same item set in all three files; item content identical across files; the three orders differ |
| Item IDs neutral (`ITEM-A01…A16`, unique) | PASS |
| `G_ID_VISIBLE` (G01–G16 tokens outside cell refs, all XML parts incl. docProps and data validations) | **NO** |
| `RESEARCHER_MAPPING_VISIBLE` | **NO** |
| `AI_PILOT_VISIBLE` | **NO** (the only match was "Co*pilot*", a false positive) |
| `SENSITIVITY_TARGET_VISIBLE` (word scan; row style, fill, font, height and hidden flags) | **NO**. One distinct row signature in each of the CODER_k and ITEM_INFO sheets; no conditional formatting |
| `REVISED_ANALYSIS_GAIN_LOSS_VISIBLE` (gain/loss, 32/47/132, core, significance/q/p/O-E, enriched, enum family tokens) | **NO** |
| GitHub URL, repo name, manuscript link | **NO**. The word "GitHub" appears once, inside attestation statement 1 (see N-2) |
| Other coders' answers or IDs | **NO** |
| Hidden sheets, defined names, comments, customXml, external links, VBA, formulas | none |
| docProps | creator / lastModifiedBy = "study coordinator"; app = "Microsoft Excel Compatible / Openpyxl 3.1.5" |
| `RESPONSE_CELLS` (H2:L17) | **EMPTY** |
| `ATTESTATION_CELLS` (C3:C12) | **EMPTY** |
| Local distribution copies byte-identical to the repo | **CODER_2: yes. CODER_3: yes. CODER_1: NO → STOP for that file** (B-1) |

`TASK1_S1_REPO_PACKETS_VERDICT=PASS`; `TASK1_LOCAL_DISTRIBUTION_COPIES_VERDICT=STOP_DO_NOT_SEND_MISMATCHED_LOCAL_COPY`.

---

## B. BLOCKING_ISSUES

### B-1. The local CODER_1 distribution copy is not the S1 file and was round-tripped through Google Sheets

**Hashes:**
- File: `…\01_CODER_PACKETS_READY_TO_SEND\PACKETS\CODER_1.xlsx`, 31,212 bytes, modified 2026-10-14 11:00.
- Local SHA-256: `a59107292dc39496f90215b28455036e3a22170149e4d911d01c07f1b344c1a6`.
- S1 SHA-256: `840addf9978ee30b725d4e190b940adfa13f0c1683c7ab2b3bde60a0ff4ce301`.

**Evidence of the Google Sheets round trip:**
- `xl/workbook.xml` contains the `GoogleSheetsCustomDataVersion2` extension;
- an `xl/metadata` protobuf with locale `zh_TW` and timezone `America/Los_Angeles`;
- 5 empty drawing parts;
- `docProps/app.xml` is missing.

**What changed:**
- `Item_order` integers became floats (1 → 1.0).
- The Q5 600-character `textLength` rule became `custom LTE(LEN(L2),600)`.
- Every response cell now has an input prompt reading "Invalid value – Choose a value from the drop-down list." This message appears as soon as a coder clicks any response cell, which is confusing.
- No coder-visible text was added or removed. The response and attestation cells are still empty.

**Why this blocks:**
- Distribution gate 25 §7 and 30 §1 require the SHA-256 of each file sent to equal its S1 hash.
- The upload also placed a coder packet in a cloud account. This is not a G-ID leak, because the packet contains none, but the coordinator should confirm the file was not shared with anyone.

**Action:**
- Replace the local file with a byte-exact copy of the repo `coder_distribution/CODER_1.xlsx` and re-verify its hash.
- Do not open distribution copies in Google Sheets, Excel or WPS and save them.
- **No S1 re-freeze is needed.**

No other blocking issue was found. In particular, there is no blinding leak in the S1 files.

---

## C. NON_BLOCKING_ISSUES

Severity uses the code-review scale. Nothing here is CRITICAL.

| ID | Sev. | Issue |
|---|---|---|
| N-1 | HIGH | **Attestation double negative.** Every statement is phrased negatively ("I have **not** read…") and is answered YES/NO. A coder who *has* read the repository must answer "NO" to "I have not read". This is error-prone in both directions: it can produce false EXPOSED flags or hide real exposure. The column header "Answer (YES/NO)" does not say that YES means "this statement is true for me". The attestation drop-down also has `showErrorMessage=False`, so free text is accepted. |
| N-2 | MEDIUM | **Blinding cue.** README A4 mentions "the project's code repository". Attestation statement 1 says "the **public** code repository (e.g. on **GitHub**)". Together they tell coders that a public GitHub repository exists, which invites a search. The family names plus "this study's literature network" are searchable. |
| N-3 | MEDIUM | **Technical depletion statement.** See D-0. It contains "statistical null model", "all four pre-specified analysis methods" and the upper-case label "DEPLETED". ITEM_INFO column J adds "Robust depletion: underrepresented relative to the null structure under all four pre-specified tests". This is unnecessary technical background and implies passed significance tests. It discloses no values and is identical for all 16 items, so it does not differentiate items. It is more technical than the approved neutral form ("appears less often than expected"). |
| N-4 | MEDIUM | **Time is under-estimated.** "Expected time: 45–60 minutes" is low. My estimate is about 80–120 minutes (section G). An under-estimate pushes coders to rush the later items, and the order is coder-specific, so the rushed items differ by coder. |
| N-5 | MEDIUM | **Order-of-tests inconsistencies:** <br>• Test (d) says "→ EVIDENCE_ONLY **with Q1 = NO**", but the consistency rule and the EVIDENCE_ONLY row allow Q1 = UNCERTAIN.<br>• Test (b) says "a **named dataset**", but the DATA_GATED definition says "a specific **kind** of data". "Named dataset" can be read as a specific branded dataset. |
| N-6 | MEDIUM | **Lexical overlap between category text and family labels is broader than the shared-word rule covers.** Rule C17 ("not shared words between a family name and a category name") lists no words. Overlaps visible to coders:<br>• M1's label "Governance" and "Accountability" match the decision families "Governance and Oversight" (1 item) and "Human Review and Accountability" (3 items).<br>• M4 "Evaluation & Assurance" matches the AI families "Evaluation and Audit" (2) and "Explanation and Assurance" (3), and the decision family "Evaluation and Selection" (3).<br>• The LONGITUDINAL definition says "resource **allocation**… **information acquisition**", which matches the decision families "Allocation and Planning" (2) and "Information Acquisition" (1).<br>Study-team file 28 §5 discloses only Evaluation, Accountability and Assurance. I did not and cannot judge whether any overlap agrees with the key; this is recorded as a priming risk only. |
| N-7 | LOW | **Inconsistent use of "category".** C16 calls "General Decision Process" a "residual **category**" (the same wording appears in its family definition), but "category" is the term for the Q2 codes. Codebook 26 §4 says "residual family". |
| N-8 | LOW | **ITEM_INFO duplicates the CODER sheet.** It is about 2,600 words. Its only additions are separate ZH columns, which are already shown in parentheses on the CODER sheet, and column J "Evidence_description". Column J only restates the pair plus a more technical depletion sentence (N-3). That doubles the reading and adds a second, different depletion wording. |
| N-9 | LOW | **No in-sheet check for inconsistent answers.** Drop-downs exist for Q1–Q4, but no rule flags invalid combinations: Q1 = NO with Q2 ≠ EVIDENCE_ONLY; NONE with Q1 ≠ YES; Q4 = Q2. Such errors are caught only by the analyzer, which forces a format-correction round trip. That round trip is allowed (30 §4), but it is another contact with the coder. |
| N-10 | LOW | **Q1 is double-barrelled** (see D-1). |
| N-11 | LOW | **The AMBIGUOUS definition overlaps NONE.** Its clause "or the definitions do not allow a defensible single choice" can be read as "nothing fits", which is NONE territory (see E). |
| N-12 | LOW | **The Q3 note discloses an analysis detail.** "It is descriptive and never weights agreement" is harmless but unnecessary. |
| N-13 | LOW | **Attestation preamble wording.** "An honest NO is recorded and does not invalidate your work silently" is awkward and could be read as a threat. |
| N-14 | INFO | **Chinese labels only on M1.** Only M1 has a Chinese gloss among M1–M4. The ZH strings themselves are valid UTF-8 Traditional Chinese (verified by code point). |

---

## D. QUESTION-BY-QUESTION REVIEW

### D-0. Stimulus: the literature-pattern statement, identical for every item

Coder-facing text (CODER sheet column G and ITEM_INFO column I):

> "Literature pattern: DEPLETED. In this study's literature network, the number of published documents that directly link AI functions of type 'X' to decision functions of type 'Y' is below the number expected under a statistical null model, and this holds under all four pre-specified analysis methods. This is a research lead only. It does not mean that the combination is impossible, ineffective, unimportant, or absent from practice."

- **Neutrality.** The statement is directionally neutral. It makes no claim about importance and includes an explicit disclaimer, and it is identical for all 16 items, so it cannot single out any item, including any sensitivity target.
- **Not an enrichment disclosure.** Every item is depleted, so it reveals no item-specific statistic.
- **Priming risk.** It frames every pairing as an *under-studied combination*. That can prompt a "why is this missing?" line of reasoning, which favours reading a governance or assurance gap into the pairing and may shift base rates for Q1 = YES and the M1/M4 categories. Because the shift is uniform, it affects category frequencies more than inter-rater agreement.
- **Unnecessary technical detail.** "statistical null model", "four pre-specified analysis methods", and in ITEM_INFO J "robust depletion… null structure… tests" add nothing to the coding task. **REWRITE_RECOMMENDED** (N-3).
- **Stimulus is thin.** The only item-specific content is two family labels and their definitions, about 35 unique words per item. The rest of the roughly 113 words in each item row is the shared depletion text. This is a design property (D-9), not a defect, but it makes Q1's "specific to this pairing" judgement hard (see D-1).

### D-1. Q1: identifiable enterprise decision interface (YES / NO / UNCERTAIN)

> README: "Does this pairing correspond to an identifiable enterprise decision interface? … An enterprise decision interface is a decision that an enterprise must make about how this kind of AI function feeds this kind of decision function, and that is specific to this pairing."
> Definitions: YES = "You can name a decision … specific to this pairing." NO = "The only decisions you can name would apply equally to almost any AI function feeding this decision function, or no enterprise decision is involved." UNCERTAIN = "You cannot decide between YES and NO."

- **Comprehensibility.** The question is moderate to hard. "Interface" is jargon, but it is defined, and the YES row turns it into an action ("you can name a decision"), which helps.
- **Double-barrelled.** Q1 asks (i) whether an enterprise decision exists and (ii) whether it is specific to this pairing. The NO row merges two different reasons: non-specific, or no decision at all.
- **Asymmetric specificity test.** NO compares only against "any AI function feeding *this decision function*". It does not compare against this AI function feeding any decision function. Coders may apply specificity unevenly.
- **Leading language:** none. **Significance leakage:** none.
- **Consistency with Q2.** Q1 = NO forces Q2 = EVIDENCE_ONLY. Q1 = UNCERTAIN allows any Q2 except NONE, including M1–M4 and EVIDENCE_ONLY. Q1 = YES allows everything except EVIDENCE_ONLY. A coder answering Q1 = NO must still fill Q2, with a forced value. This is redundant but harmless, and it is a mis-entry risk (N-9).
- **Verdict: CLARIFY.**

### D-2. Q2: best category (required)

- The drop-down offers exactly the 9 codes. The "Use when" / "Do not use when" table, the consistency rule and the order of tests are all on one sheet.
- **Order of tests:** LONGITUDINAL, then DATA_GATED, then M1–M4/NONE, then EVIDENCE_ONLY, with AMBIGUOUS as the last resort. It is clear, but it has two inconsistencies (N-5).
- Test (a)'s wording, "represented only with outcomes over more than one period", is abstract for a practitioner.
- No G numbering, sensitivity marker or researcher hint is present. The lexical overlap risk is covered in N-6.
- **Verdict: KEEP the structure; CLARIFY tests (a), (b) and (d).**

### D-3. Q3: confidence (HIGH / MEDIUM / LOW)

- Clear, with a drop-down. It refers to Q2 only.
- The sentence "never weights agreement" is unnecessary (N-12).
- **Verdict: KEEP; optionally REMOVE the second sentence.**

### D-4. Q4: optional secondary category

- The drop-down is restricted to M1–M4, LONGITUDINAL and DATA_GATED, so EVIDENCE_ONLY, NONE and AMBIGUOUS cannot be chosen. Good.
- "Leave blank unless a second category is clearly necessary." The LONGITUDINAL and DATA_GATED rows invite putting the M-category involved in Q4. That is coherent with the order of tests.
- **Can Q4 contaminate Q2?** Low risk. Q2 is required and analysed alone; Q4 enters only a Jaccard statistic. The plausible effect is the reverse: a hedging coder may pick a Q2 and park the alternative in Q4 rather than choose AMBIGUOUS, which lowers the AMBIGUOUS rate. That is acceptable.
- **Gaps:**
  - The sheet does not enforce "Q4 must differ from Q2".
  - It does not say what Q4 means when Q2 is EVIDENCE_ONLY, NONE or AMBIGUOUS. With AMBIGUOUS, a coder may put one competing category in Q4 and the other only in Q5.
- **Verdict: CLARIFY.** Proposed wording is in H-8.

### D-5. Q5: rationale (1–3 sentences, ≤ 600 characters, required)

> "Short rationale (1-3 sentences). Required for every item. If Q2 is NONE, state the enterprise decision that no listed category captures. If Q2 is DATA_GATED, name the data. If Q2 is AMBIGUOUS, name the competing categories."

- It asks only for reasons plus the three required specifics. It does not lead, and the 600-character limit is enforced by a `textLength ≤ 600` rule with an error message.
- **Verdict: KEEP.**

---

## E. CATEGORY-DEFINITION REVIEW

Each entry quotes the coder-facing text from the CATEGORY_DEFINITIONS sheet and compares it with the approved definition. Conflicts are recorded only.

**M1: Authority & Accountability (授權與問責; = Governance & Decision Rights / authority-to-act)**
> Use when: "the main issue of the connection is who may approve, reject, stop or change what the AI output is allowed to decide; formal versus effective control; accountability; enterprise policy boundaries." Do not use when: "the main issue is how outputs are routed or technically validated."

- It is distinguishable from M2 and M4.
- **Boundary with M3 is the weakest in the set.** M3's own text includes "who decides" and "override", and M4's exclusion line says "who decides". That points coders to M1 *or* M3. The intended line, formal authority (M1) versus operational division of work (M3), is only implicit through M3's exclusion "formal authority".
- The label's gloss "Governance" adds lexical overlap (N-6).
- No conflict with the approved definition (D-12 label).

**M2: Workflow Routing & Recovery**
> Use when: "the main issue of the connection is how the AI output enters the next decision or action step; handoffs across systems or units; exception handling; rollback and recovery." Do not use when: "the main issue is who holds authority."

- It is clear.
- Mild overlap with M3: "handoffs" sits near "sequence and division of work", and M3's "escalate" sits near M2's "exception handling".
- Its exclusion line names only M1. It does not say "not when the issue is the human–AI split (M3)".

**M3: Human–AI Configuration & Response**
> Use when: "the main issue of the connection is the sequence and division of work between people and AI (who proposes, who decides, aggregation, delegation, override) and how users actually respond (use, verify, modify, escalate, reject, bypass)." Do not use when: "the main issue is formal authority or validation evidence."

- **It is two constructs in one:** configuration *and* behavioural response. That is broad, so it may attract residual choices.
- "verify" overlaps M4's "validation".

**M4: Evaluation & Assurance**
> Use when: "the main issue of the connection is pre-deployment validation, monitoring, revalidation, auditability, explanation usability, drift, or evidence that the AI output is fit for the decision." Do not use when: "the main issue is who decides or how work is sequenced."

- It is clear.
- "auditability" sits near M1's "accountability".
- The label shares words with three family labels (N-6).

**LONGITUDINAL: Longitudinal extension**
> Use when: "the enterprise decision can only be studied with outcomes observed over more than one period: results of one cycle change later resource allocation, policy or information acquisition. A single-period choice is not enough to represent it." Do not use when: "a single-period configuration choice is enough. If you use it, you may put the M1-M4 category involved in Q4."

- **Recorded conflict with the approved definition.** The approved definition is "core is learning / adaptation / feedback / capability evolution over time". The packet operationalises it as multi-period outcomes feeding later allocation, policy or information acquisition. It never uses the words learning, adaptation, feedback or capability.
- A coder who sees a feedback or learning loop in an item may not recognise it as LONGITUDINAL.
- "resource allocation" and "information acquisition" echo decision-family labels (N-6).
- Its wording is close to 53B; the conflict is recorded only.

**DATA_GATED: Data-gated module**
> Use when: "an enterprise decision exists only if a specific kind of data is available. Name the data in Q5." Do not use when: "a category applies without special data. If you use it, you may put the M1-M4 category involved in Q4."

- **Recorded difference from the approved definition.** The approved definition is "applicability of the enterprise decision mechanism explicitly depends on data availability **or readiness**". The packet's "exists only if … available" is a stronger existence condition and omits *readiness* (quality, labelling, access).
- Test (b) says "named dataset" (N-5).
- It is easy to confuse with EVIDENCE_ONLY when a coder reasons that the pairing only matters if the data exist.

**EVIDENCE_ONLY: Evidence-layer only**
> Use when: "the pairing describes a research or technology pattern but implies no distinct enterprise decision beyond what any AI function feeding this decision function would raise." Do not use when / rule: "Use together with Q1 = NO (or UNCERTAIN). Do not use when a specific category clearly applies."

- **Recorded difference from the approved definition.** The approved definition is "the role stays at the evidence/information layer rather than an identifiable enterprise decision interface". The packet uses a *non-specificity* criterion ("beyond what any AI function … would raise"). It is consistent with the packet's own Q1 = NO definition, but it is a different operationalisation; "evidence/information layer" is never stated.
- It is consistent with Q1: NO → EVIDENCE_ONLY is forced, and UNCERTAIN is allowed. Test (d) contradicts the UNCERTAIN allowance (N-5).

**NONE: None of the listed categories**
> Use when: "an identifiable enterprise decision interface exists but none of M1, M2, M3, M4, LONGITUDINAL or DATA_GATED adequately expresses it. Requires Q1 = YES, and Q5 must state the enterprise decision that is not captured." Do not use when: "for insufficient evidence or when two categories tie (use AMBIGUOUS, or Q1 = UNCERTAIN), or when there is no distinct interface (use EVIDENCE_ONLY)."

- **Matches the approved definition (D-2) in full:** Q1 = YES, Q5 names the decision, and the exclusions for insufficient evidence, unsure, tie and no interface. Good.

**AMBIGUOUS**
> Use when: "two or more categories fit equally well and you cannot choose one, or the definitions do not allow a defensible single choice. Name the competing categories in Q5." Do not use when: "as a default; choose a category whenever one fits better."

- It is broadly consistent with the approved definition ("several plausible mechanisms cannot be reliably separated for the primary category").
- **Its second clause invites "nothing fits" cases, which belong to NONE** (N-11).
- **NONE versus AMBIGUOUS is otherwise clear:** several fit means AMBIGUOUS, none fits means NONE.

**Cross-checks**
- **Q1 against EVIDENCE_ONLY and NONE.** The rules are internally consistent and enforced by the analyzer.
  - A coder answering Q1 = NO must fill Q2 (= EVIDENCE_ONLY). This is stated twice, in D3 and C14.
  - Q1 = UNCERTAIN with NONE is barred.
  - Q1 = YES with EVIDENCE_ONLY is barred implicitly: it is not in the YES list.
- **Confusability of DATA_GATED, EVIDENCE_ONLY and LONGITUDINAL.** The order of tests separates them procedurally. Conceptually, the main confusions are "data-dependent" versus "not an enterprise decision", and multi-period versus feedback. The second one is made worse by the LONGITUDINAL wording.

---

## F. BLINDING REVIEW

Each item was confirmed **absent** from all three S1 files, in cells and in raw XML:

| Item | Status |
|---|---|
| GitHub URL or repo name | Absent. The word "GitHub" appears only in attestation statement 1 (N-2) |
| Manuscript or thesis content or link | Absent. The word appears only in the prohibitions |
| G01–G16 tokens | Absent |
| Researcher mapping or key vocabulary (sealed, 53B, 54A/B/C, 41, Table 3-4) | Absent |
| AI-pilot output or vocabulary | Absent |
| 32-core / 47 / 132 | Absent |
| Significance, q, p, O/E | Absent |
| Sensitivity, gain/loss, revised analysis | Absent |
| G04/G10/G11 markers | Absent. Row formatting is uniform; no conditional formatting; no hidden rows, columns or sheets; no comments; no defined names |
| Other coders' answers or IDs | Absent |

**Attestation: all 7 items present.**

| # | Required | Coder-facing statement |
|---|---|---|
| 1 | not read the public repository | "I have not read the public code repository (e.g. on GitHub) for this project." |
| 2 | not read the thesis or manuscript | "I have not read the thesis or any manuscript or report of this project." |
| 3 | not seen researcher G→M | "I have not seen the researcher's assignments of these items to categories." |
| 4 | not seen AI-pilot output | "I have not seen any AI-generated coding output for these items." |
| 5 | not discussed with other coders | "I did not consult another coder." Narrower than "discussed with". **CLARIFY** |
| 6 | no ChatGPT/Claude/Gemini/Copilot/other AI | "I did not use ChatGPT, Claude, Gemini, Copilot or any other AI tool to answer." |
| 7 | completed independently | "I coded every item independently." |

Name, Date and Signature rows are present and empty.

**Known limitation (context only, not a new finding).** The public repository history contains the 54A text indexed by G ID, and the family pairs are listed with G IDs (28 §1). A motivated coder could re-identify items from AI-family × decision-family pairs. Masking and per-coder order prevent only casual identification. N-2 is relevant because the packet itself tells coders that a public GitHub repository exists.

---

## G. ESTIMATED CODER BURDEN

**Word counts** (English words, by script):

| Part | Words |
|---|---|
| README | 269 |
| CATEGORY_DEFINITIONS | 765 |
| ATTESTATION | 124 |
| CODER sheet | 1,876, i.e. 105–121 per item (mean about 114) |
| ITEM_INFO (duplicate) | 2,610 |

About 80 of each item's ~114 words are the identical depletion boilerplate.

**Time estimate for a careful human coder:**

| Step | Time |
|---|---|
| Read and absorb README, 9 category definitions, 5 rules and the order of tests | 15–20 min |
| Per item: read about 35 unique words; Q1; walk tests (a)–(d); Q2; Q3; optional Q4; write 1–3 sentences | 4–6 min (× 16 = 64–96 min) |
| Attestation | 2 min |
| **Total** | **about 80–120 min**, against the stated 45–60 min (N-4) |

**Usability notes:**
- **Flipping back.** Frequent flipping is likely between the CODER sheet and CATEGORY_DEFINITIONS, because 9 categories, M1–M4 boundary lines and 4 rules are hard to hold in memory.
- **Jargon:** "enterprise decision interface", "null model", "pre-specified analysis methods", "period/cycle", "evidence layer", "data-gated module".
- **Entry risk:**
  - Q1–Q4 have drop-downs with error stops. Q5 is free text with a length limit.
  - Attestation uses a YES/NO drop-down, but free text is not blocked, and the double negative is the biggest risk (N-1).
  - Cross-field consistency is not checked in the sheet (N-9).
- **Examples.** Do not add examples. Any example touching these family pairs or category names would lead answers. None were added.

**Element verdicts:**

| Element | Verdict |
|---|---|
| README time estimate | CLARIFY |
| README A4 / attestation 1 GitHub wording | REWRITE_RECOMMENDED |
| Q1 | CLARIFY |
| Q2 + drop-down | KEEP |
| Order of tests | CLARIFY |
| Q3 | KEEP (trim the note) |
| Q4 | CLARIFY |
| Q5 | KEEP |
| Literature-pattern statement | REWRITE_RECOMMENDED |
| ITEM_INFO sheet | REMOVE, or remove column J |
| Residual-family rule | CLARIFY |
| Shared-word rule | CLARIFY |
| Attestation | REWRITE_RECOMMENDED (answer semantics) |
| Category definitions M1–M4, NONE | KEEP (record-only notes in E) |
| AMBIGUOUS | CLARIFY |
| LONGITUDINAL / DATA_GATED / EVIDENCE_ONLY | KEEP as frozen; conflicts with the approved definitions recorded for the researcher |

---

## H. RECOMMENDED CHANGES

Except for H-1, every change below alters the coder xlsx, and most also alter codebook 26 §1–4. **Each therefore requires a new S1 freeze** (S1b: rebuild, leakage check, audit, new manifest; versioned and disclosed per 30 §3). That is permissible because no coder has received a packet. None of them is required.

| # | Tag | Change | Proposed wording | S1 re-freeze? |
|---|---|---|---|---|
| H-1 | **REQUIRED (blocking, B-1)** | Replace the local `PACKETS\CODER_1.xlsx` with a byte copy of the repo `coder_distribution/CODER_1.xlsx`. Re-verify that all three hashes equal S1 before sending. Never open or save distribution copies in Google Sheets, Excel or WPS. Confirm the Google copy was not shared. | — | **NO** |
| H-2 | REWRITE_RECOMMENDED | Attestation answer semantics (N-1). Either make the statements positive, or state the semantics explicitly. | Header C2: "Is this statement true for you? (YES = true, NO = not true)". Preamble A1: "Answer each statement YES (true for me) or NO (not true for me). If a statement is not true, answer NO; this is recorded and reported, and your sheet is still used." Turn on the error stop for C3:C9. | YES |
| H-3 | REWRITE_RECOMMENDED | Remove the GitHub and "public" cue (N-2). | Attestation 1: "I have not looked at any code, data files or online materials of this project." README A4: "Do not consult any code, data, thesis, manuscript or report of this project, any other coder, or any AI assistant (ChatGPT, Claude, Gemini, Copilot or other) while coding." | YES |
| H-4 | REWRITE_RECOMMENDED | Plain-language depletion statement (N-3), with the same text on every item. | "Literature pattern: in this study's collection of published research, papers that directly link AI functions of type 'X' to decision functions of type 'Y' appear less often than expected. This is a research lead only. It does not mean the combination is impossible, ineffective, unimportant, or absent from practice." | YES |
| H-5 | REMOVE | Drop the ITEM_INFO sheet, or at least column J "Evidence_description" (N-8, N-3). The CODER sheet already has every item field. | — | YES |
| H-6 | CLARIFY | Time estimate (N-4). | "Expected time: about 90–120 minutes. You may take a break, but do not discuss the items with anyone until you have submitted." | YES |
| H-7 | CLARIFY | Order of tests (N-5). | "(b) Does the decision exist only if a specific kind of data is available? → DATA_GATED (name the data in Q5). … (d) Otherwise → EVIDENCE_ONLY (with Q1 = NO, or Q1 = UNCERTAIN)." For (a): "(a) Is the decision about how results from one cycle change later choices (learning or adjustment over several periods)? → LONGITUDINAL." This last part needs researcher approval, because it moves toward the approved definition and away from 53B wording. | YES |
| H-8 | CLARIFY | Q4 scope (D-4). | README A12: "Q4 Optional secondary category. Leave blank unless a second category is clearly necessary. It must differ from Q2. If Q2 is EVIDENCE_ONLY or NONE, leave Q4 blank. If Q2 is AMBIGUOUS, name all competing categories in Q5." | YES |
| H-9 | CLARIFY | Shared-word rule (N-6). | C17: "Code the enterprise decision, not the technology or the topic. Some family names share words with category names (for example Evaluation, Assurance, Accountability, Governance, Allocation, Information). A shared word is not a reason to choose a category." | YES |
| H-10 | CLARIFY | Residual family wording (N-7). | C16: "'General Decision Process' is a residual decision family (not a category). Code it like any other family …". The family definition text "(residual category)" would become "(residual family)". | YES |
| H-11 | CLARIFY | AMBIGUOUS versus NONE (N-11). | "Use when two or more categories fit about equally well and you cannot defensibly choose one. Name the competing categories in Q5. If no category fits, use NONE (with Q1 = YES) instead." Requires researcher approval as a definition edit. | YES |
| H-12 | CLARIFY | Q1 double-barrel (D-1). | Add to the NO row: "Answer NO if no enterprise decision is involved, or if every decision you can name would arise equally for almost any AI function feeding this decision function." Optional: split the reason into Q5. | YES |
| H-13 | CLARIFY | Attestation 5 (F). | "I did not discuss these items with, or consult, any other coder." | YES |
| H-14 | CLARIFY (optional) | Add conditional formatting that highlights in red: Q1 = NO with Q2 ≠ EVIDENCE_ONLY; Q2 = NONE with Q1 ≠ YES; Q4 = Q2. It must be uniform on all rows so it cannot mark items. Re-run the leakage and uniformity checks afterwards. | — | YES |
| H-15 | REMOVE (optional) | Q3 note "It is descriptive and never weights agreement." (N-12) | — | YES |
| H-16 | RECORD ONLY | LONGITUDINAL omits learning, adaptation, feedback and capability evolution. DATA_GATED omits readiness and is stated as an existence condition. EVIDENCE_ONLY uses non-specificity rather than "evidence/information layer". M1/M3 "who decides" overlap. These are differences from the approved definitions given to this reviewer. Researcher decision required; the reviewer does not change definitions. | — | YES, if adopted |

**Bottom line:**
- If the researcher accepts the packet as is: do H-1 only, then distribute. There is no re-freeze.
- If any of H-2 to H-16 is adopted, the packet must be versioned and re-frozen as S1b before any coder receives a file.
- The reviewer's recommendation is to adopt at least H-2, H-3, H-4 and H-6, which are low risk, before sending.

V1_PACKET_REVIEW=REVISION_RECOMMENDED
V1_PACKET_REVISION_REQUIRED=NO
S1_REFREEZE_REQUIRED=NO
V1_S1_HASH_CHANGED=NO
