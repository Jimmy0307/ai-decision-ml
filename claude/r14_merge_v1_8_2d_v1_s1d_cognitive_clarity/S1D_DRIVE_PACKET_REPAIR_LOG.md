# S1D — Drive Packet Repair Log

**Date:** 2026-10-14

## Scope

This record documents an operational repair of the Google Drive distribution copy of `CODER_1_ZH_TW.xlsx`. It does not modify the S1d instrument, GitHub canonical workbook bytes, freeze manifest, category semantics, Q1–Q5, analyzer, analysis plan, recruitment rules, or Study 1 results.

## Incident

The Drive/local distribution copy of `CODER_1_ZH_TW.xlsx` was opened and re-saved through Google Sheets. The re-saved workbook retained the same visible cell text but its OOXML package and validation structure changed and its SHA-256 no longer matched the approved frozen S1d packet. That re-saved copy was therefore not approved for distribution.

The affected Google-Sheets-resaved forensic copy is preserved outside the active distribution set and is explicitly marked `DO_NOT_SEND`.

## Repair

The active `CODER_1_ZH_TW.xlsx` distribution copy was replaced byte-for-byte with the approved S1d canonical workbook from:

`claude/r14_merge_v1_8_2d_v1_s1d_cognitive_clarity/coder_distribution/CODER_1_ZH_TW.xlsx`

The replacement was not opened or re-saved before verification.

## Post-repair verification

The three current Drive distribution workbooks were independently downloaded and SHA-256 checked after the repair:

- `CODER_1_ZH_TW.xlsx` — `387c9bed46fe54f22a9cc86cf855be398da6b04aac68ab363ccf6ff73619061f` — 21,645 bytes — MATCH
- `CODER_2_ZH_TW.xlsx` — `796f0666dded56340ba8410ee834dfd244c3a91b84c8cd8f0a7e0a2cb3621c8c` — 21,672 bytes — MATCH
- `CODER_3_ZH_TW.xlsx` — `2f24b78e4db08695bc27bb157feffb883ef3497875a3f12f2a67c11ce0feb58b` — 21,664 bytes — MATCH

`FREEZE_MANIFEST_MATCH=3/3`

No formal human coding data were collected from the mutated copy.

## Current status

`S1D_VERSION=S1D`

`GITHUB_CANONICAL_UNCHANGED=YES`

`CODER_1_DRIVE_REPAIR=PASS`

`CODER_1_HASH=PASS`

`CODER_2_HASH=PASS`

`CODER_3_HASH=PASS`

`FREEZE_MANIFEST_MATCH=3/3`

`GOOGLE_SHEETS_MUTATED_COPY_REMOVED_FROM_DISTRIBUTION=YES`

`V1_HUMAN_RESULTS=NONE`

`READY_TO_DISTRIBUTE=YES`

`SUBMISSION_READY=NO`

## Distribution control

Before sending any packet, verify its SHA-256 against `FREEZE_MANIFEST_V1_S1D.txt`. Do not open or convert the frozen XLSX packets in Google Sheets before distribution. Use the researcher visual-review artifacts for content inspection whenever possible.
