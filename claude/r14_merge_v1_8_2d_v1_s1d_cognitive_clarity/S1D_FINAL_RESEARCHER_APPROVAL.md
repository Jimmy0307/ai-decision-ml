# S1D — Final Researcher Approval and Provenance Addendum

**Date:** 2026-10-14  
**Base frozen instrument commit:** `a1ff54e8a4c557c642b5f33c4d8902125f9aa886`  
**Instrument version:** S1D  
**Purpose of this file:** post-freeze researcher approval and provenance correction only. This file does **not** alter the frozen coder workbooks, category semantics, analysis plan, sealed mappings, or any Study 1 computation.

## 1. Final researcher decision

The researcher completed the final visual review of `S1D_RESEARCHER_VISUAL_REVIEW.md` and accepts S1D as the final pre-distribution coder instrument.

- `FINAL_RESEARCHER_VISUAL_REVIEW=PASS`
- `CODER_INSTRUMENT=APPROVED`
- `COGNITIVE_CLARITY=PASS`
- `CATEGORY_SEMANTICS_CHANGED=NO`
- `Q1_CONSTRUCT_CHANGED=NO`
- `Q2_CONSTRUCT_CHANGED=NO`
- `ANALYSIS_PLAN_CHANGED=NO`
- `V1_HUMAN_RESULTS=NONE`
- `READY_TO_DISTRIBUTE=YES`

No S1d coder packet had been distributed and no formal human coding data had been collected before this approval.

## 2. Provenance correction for the cognitive-readability note

`S1D_COGNITIVE_READABILITY_DECISION.md` recorded the wording risk as a researcher readability check. The more precise provenance is:

Before formal distribution, the researcher conducted an informal readability check and also received feedback from one **informal reader** who identified a possible interpretation of Q1 as asking whether the reader's own company needs or would adopt the AI configuration. That person was **not a formal coder**, the feedback was **not collected as study data**, was **not included in any statistical analysis**, and did **not** constitute a formal pilot or pretest.

The feedback was used only to identify a comprehension risk before any formal coding began. The resulting S1d patch clarified wording without changing item pairings, category assignments, researcher keys, G mappings, category semantics, Q1/Q2 logic, or the frozen reliability analysis plan.

Because the informal reader has already seen and discussed the instrument, that person must **not** be recruited as one of the three formal V1 coders.

## 3. Frozen workbook identity remains unchanged

This approval addendum does not modify the S1d coder workbooks. Their approved SHA-256 values remain:

- `CODER_1_ZH_TW.xlsx` = `387c9bed46fe54f22a9cc86cf855be398da6b04aac68ab363ccf6ff73619061f`
- `CODER_2_ZH_TW.xlsx` = `796f0666dded56340ba8410ee834dfd244c3a91b84c8cd8f0a7e0a2cb3621c8c`
- `CODER_3_ZH_TW.xlsx` = `2f24b78e4db08695bc27bb157feffb883ef3497875a3f12f2a67c11ce0feb58b`

`FREEZE_MANIFEST_V1_S1D.txt` remains the freeze authority for the instrument artifacts. This post-freeze approval record is intentionally additive and does not require rewriting the frozen workbook hashes.

## 4. Distribution rule

Each of the three eligible independent coders receives exactly one corresponding frozen XLSX file as a direct attachment or controlled file transfer.

Do not provide:

- a GitHub/repository link;
- the master workbook;
- researcher mappings;
- item-to-G mappings;
- AI pilot outputs;
- any answer guidance beyond the frozen S1d workbook.

Do not open or convert the XLSX files in Google Sheets before distribution.

Coder eligibility remains governed by `S1D_RECRUITMENT_ELIGIBILITY.md`. The manuscript should refer to them as **具相關領域背景之獨立人工編碼者** unless a stricter expert criterion is separately defined and frozen.

## 5. Return and analysis gate

After all three completed XLSX files are returned:

1. Preserve the returned originals.
2. Compute SHA-256 for each returned workbook before analysis.
3. Create the S2 freeze manifest.
4. Run the frozen analyzer and the pre-specified reliability analysis.
5. Report pre-adjudication reliability before any reconciliation/adjudication.

## 6. Current authoritative status

`S1_STATUS=SUPERSEDED_BEFORE_DISTRIBUTION`  
`S1B_STATUS=SUPERSEDED_BEFORE_DISTRIBUTION`  
`S1C_STATUS=SUPERSEDED_BEFORE_DISTRIBUTION`  
`S1D_VERSION=S1D`  
`S1D_FREEZE=PASS`  
`FINAL_RESEARCHER_VISUAL_REVIEW=PASS`  
`V1_HUMAN_RESULTS=NONE`  
`READY_TO_DISTRIBUTE=YES`  
`SUBMISSION_READY=NO`

This file supersedes only the **distribution-gate status** and the **readability-check provenance wording** in earlier S1d status notes. It does not supersede the frozen instrument, freeze manifest, protocol, codebook, recruitment eligibility rules, or analysis plan.
