# S1D — 54A Stimulus Clarification

**Date:** 2026-10-14
**Type:** documentation-only clarification, recorded on the S1d branch.

This file changes no instrument content. The S1d coder workbooks, their hashes, the freeze manifest, the category semantics, item order, Q1–Q5, the analyzer, the analysis plan and the recruitment rules are all unchanged. S1e was not created.

```
S1D_STATUS=FINAL
CODER_INSTRUMENT=APPROVED
54A_RECOVERY=CONFIRMED
54A_ITEM_SPECIFIC_EMPIRICAL_EVIDENCE=NO
54A_TEMPLATE_OMISSION_SUBSTANTIVE_EFFECT=NONE
PAIR_LEVEL_CONCEPTUAL_VALIDATION=YES
LITERATURE_EVIDENCE_REVALIDATION=NO
V1_HUMAN_RESULTS=NONE
READY_TO_DISTRIBUTE=YES
SUBMISSION_READY=NO
```

## 1. Why this clarification was needed

Before distribution, the researcher raised a concern. Codebook 26 §1 lists, for every item, "the neutral evidence description from 54A". The S1d coder workbooks show no separate field with that name. If 54A held item-specific empirical evidence, S1d would be missing a substantive stimulus layer.

This file records the verification of that concern.

## 2. Canonical 54A — identification

| Property | Value |
|---|---|
| Canonical path | `54A_V1_BLIND_PACKET_A_v2_2.csv` (repository root) |
| SHA-256 | `517675e7491212c4630d190c5b082ff3f7a6904a1f5d84047be79d8b84d07f4d` |
| Git blob | `5ce4bf74df65db76ab55c9f5bdb13698de0af7cd` |
| Introduced in | commit `c409a8c` "V1: pre-registered blind-coding protocol, blinded packets A/B, sealed-key commitment (pre-coding freeze)" |
| Fields | `case_id`, `ai_family`, `ai_family_definition`, `decision_family`, `decision_family_definition`, `neutral_pair_description`, `network_evidence` |
| Rows | 16 (`case_id` C01–C16) |

**How it was uniquely identified:**
- **Same file everywhere.** Every remote branch that contains `54A_V1_BLIND_PACKET_A_v2_2.csv` (11 branches) carries the same blob `5ce4bf74…`. The file is not present on `main`.
- **No other candidate locally.** A search of `C:\NTUST_PAPER\outputs` and `C:\NTUST_PAPER\FREEZE` for files with a `neutral_pair_description` column found only four files: this 54A file, its counterpart 54B (packet B, same content in a different order), and the two `v1_human_packet/PACKET_*.csv` copies.
- **Explicit references.** Codebook 26 §1 ("the neutral evidence description from 54A") and protocol 25 §3 ("The item content comes from frozen 54A only … the neutral pair description") refer to this file.

**Item mapping without any answer key:** each ITEM-Axx is linked to its 54A row by its unique AI-family × decision-family pair. No sealed key, researcher assignment or AI-pilot output was opened or consulted.

## 3. What 54A's "neutral evidence description" contains

`neutral_pair_description` is one generic template, repeated across all 16 items, with only the two family names substituted:

> "Published research that directly links AI functions of the type '‹AI family›' to decision functions of the type '‹Decision family›'."

- There are 16 distinct raw strings, but once the family names are masked they collapse to **1 template**.
- The field contains no excerpt, case, finding, count or other item-specific empirical content.
- `network_evidence` is identical for all 16 rows ("Robust depletion: underrepresented relative to the null structure under all four pre-specified tests …"). It carries the depletion label and test language that the blinding rules exclude. The coder-facing literature-pattern statement already replaces it with neutral wording.

## 4. What happened to it in S1b–S1d

- **S1 (English):** the `ITEM_INFO` sheet had an `Evidence_description` column holding the 54A template sentence, followed by the `network_evidence` text. The coding sheet itself did not show this column.
- **S1b:** while removing the "robust depletion" wording, the whole `Evidence_description` column was dropped. That removed the template sentence together with the leaky text. S1c and S1d inherited this.

## 5. Assessment

1. **Nothing substantive was removed.** The omission removed redundant wording, not item-specific empirical evidence, because 54A contains no such evidence.
2. **Restoring the template would add nothing.** It restates the AI and decision family names already shown in S1d, which also shows both family definitions and the neutral literature-pattern statement.
3. **S1d already gives coders the intended stimulus.** It presents the pair-level conceptual stimulus that the frozen S1 design intended: the AI family, the decision family, their definitions and the common neutral pattern statement. The coders are working from the material the design called for.

## 6. Claim boundary

**What V1 is.** V1 is a **pair-level conceptual construct-interpretation reliability study**. It is not a human re-review of underlying literature excerpts.

**What coders do:**
- Coders judge whether each AI-function × decision-function pairing implies an identifiable enterprise decision interface, under the general-enterprise framing given in the instructions.
- If it does, they judge which enterprise decision mechanism it best fits.

**What coders do not do.** Coders are not validating individual source papers, the literature evidence behind any cell, or empirical enterprise cases.

**Manuscript wording:**

- **APPROVED:** "V1 evaluated whether independent coders could consistently translate the 16 AI-function × decision-function pairings into enterprise decision mechanisms."
- **NOT APPROVED:**
  - "Experts validated the literature evidence for the 16 gaps."
  - "Human coders confirmed that each depleted cell represents an enterprise problem."
  - "Coders independently reviewed the underlying literature supporting each G."

## 7. Unchanged artifacts (verified at time of writing)

| File | SHA-256 |
|---|---|
| `coder_distribution/CODER_1_ZH_TW.xlsx` | `387c9bed46fe54f22a9cc86cf855be398da6b04aac68ab363ccf6ff73619061f` |
| `coder_distribution/CODER_2_ZH_TW.xlsx` | `796f0666dded56340ba8410ee834dfd244c3a91b84c8cd8f0a7e0a2cb3621c8c` |
| `coder_distribution/CODER_3_ZH_TW.xlsx` | `2f24b78e4db08695bc27bb157feffb883ef3497875a3f12f2a67c11ce0feb58b` |
| `V1_SEALED/FREEZE_MANIFEST_V1_S1D.txt` | `eb12518ed030df7e7f4b6b6ccb227a4e11942bddf606118bc6b7d4139dc05588` |
