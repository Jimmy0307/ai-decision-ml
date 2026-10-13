# 28 — V1 Blinding and Recruitment Plan (v1.8.2)

## 1. Public-repository limitation (stated honestly)

The repository (`Jimmy0307/ai-decision-ml`) was **public before coding**, and it remains public. The researcher's G→M mapping is readable there in several places:
- 41;
- 54C, which reproduces the sealed key;
- the v1.8 manuscript (Tables 3-4, 3-4A, 4-11);
- the v1.8.1 cleanup candidate manuscript;
- the 132 matrix copies;
- the v1.8.1 packet files (which show G IDs).

The 54A packet text, which these coder files reuse, is also public and is indexed by case ID. The family pairs are listed with G IDs in 11 and 41. A person who has read the repository could therefore **re-identify every item from its AI family × decision family pair**, even though G IDs are masked.

**Perfect blinding is therefore not claimed.** Masking G IDs and randomizing item order prevent casual identification. They do not stop deliberate lookup.

Making the repository private later would not undo any exposure that has already happened. The history stays public until then, and copies may exist elsewhere.

## 2. Mitigation: recruit people with no prior exposure

| Criterion | Rule |
|---|---|
| Independence | The coder is not a member of the study team, not the author of 41, and not a translator of the materials. |
| No prior exposure | The coder has never opened the project repository, the thesis or manuscript drafts, 54C, or any AI-pilot output, and has not discussed the item mappings with the researcher. |
| Profile (preferred, not mandatory) | (1) enterprise IT / AI-governance practitioner; (2) IS / management researcher; (3) AI / decision-science practitioner. One coder per profile is preferred. |
| Language | Able to read the English definitions. The Chinese family labels are copied from the manuscript and are not a new translation. |
| AI tools | The coder agrees not to use ChatGPT, Claude, Gemini, Copilot or any other AI tool. |

## 3. Attestation and exposure

- **Attestation.** Each coder answers the 7 attestation statements in the `ATTESTATION` sheet (YES/NO) and adds name, date and signature.
- **Exposure.** Any NO answer, or any later discovery of exposure, sets `CODER_STATUS=EXPOSED`.
  - The analyzer reports `CLEAN_CODERS_ONLY` as the primary result and `ALL_CODERS_INCLUDES_EXPOSED` alongside it. It never pools them silently.
  - An exposed coder is replaced by a new coder, who receives a fresh copy of the same S1-frozen file (29 §4).
- **Verification.** Self-attestation cannot be verified. This remains a limitation of V1.

## 4. What the coordinator must not do

- Send packets through GitHub, or link to the repository.
- Discuss items, categories or the researcher's view with a coder before that coder's sheet is frozen (S2).
- Tell a coder anything about another coder's answers.
- Use any AI tool to "pre-check" a coder's answers.

## 5. Further disclosures for the report

- The codebook's order-of-tests and its clarifications were written after the AI pilot had been compared with the key (54C §6).
- The v1.8.1/v1.8.2 codebook edits were made by agents that had read the key in order to screen for leakage.
- The family names share some words with category labels (Evaluation, Accountability, Assurance).
