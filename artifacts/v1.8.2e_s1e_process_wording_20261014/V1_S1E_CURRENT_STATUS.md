# V1 S1e Current Status

Date: 2026-10-14

## Status

- `S1E_VERSION=S1E`
- `TEACHER_REVIEW=APPROVED_TO_RUN`
- `READY_TO_DISTRIBUTE=YES`
- `HUMAN_RESULTS=NONE`
- `OLD_S1D_PRESERVED=YES`
- `CODER_INSTRUMENT_CHANGED_AFTER_S1D=YES`
- `CHANGE_SCOPE=CODER_FACING_WORDING_AND_ANSWER_SHEET_LAYOUT`
- `G01_G16_CHANGED=NO`
- `STUDY1_BASELINE_CHANGED=NO`
- `ENTERPRISE_MODEL_CHANGED=NO`
- `SUBMISSION_READY=NO`

## Instrument change

The coder-facing term `企業決策介面` was revised to `企業決策過程` for interpretability. The intended judgment remains whether an AI-function × decision-function pairing implies a distinct enterprise organizational choice, setting, or judgment.

Technical uses of `介面` remain technical terms, including `使用者介面`, `API`, and `系統串接介面`.

The answer sheet layout places Q1–Q5 in columns G–K and `文獻樣態說明` in column L.

## Frozen packet hashes

- CODER_1_ZH_TW.xlsx  
  `cbbbaa0a9741426a051168439ae4f8ce2d212c2878ed1990e444a9b1e2655a29`
- CODER_2_ZH_TW.xlsx  
  `5925ead55daa2c9db99a084c4cce48441bd6a3c2994371b1e170562bac0e3f38`
- CODER_3_ZH_TW.xlsx  
  `50d8c818950a33ea4644fe038c8f89e9cde70990afd0d70dc194012c620084a9`

## Distribution rule

Send the three raw XLSX files directly to the three eligible independent coders. Do not provide the public GitHub repository link. Do not open/resave the frozen XLSX files in Google Sheets before distribution. Verify SHA-256 immediately before sending.

On return, freeze the received originals by hash before any analysis or normalization.

## GitHub lineage

- Historical S1d branch: `research/v1.8.2d-v1-s1d-cognitive-clarity-20261014`
- Historical S1d head before S1e: `ca56f75461c1f995f8f742c09ceb292d40ecbbc2`
- S1e branch: `research/v1.8.2e-v1-s1e-process-wording-20261014`

S1d remains historical evidence and is not overwritten.
