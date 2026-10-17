# S1e Drive Hash Verification

Date: 2026-10-14

The three teacher-approved S1e coder workbooks were uploaded to Google Drive as raw XLSX files and then downloaded again from Drive. SHA-256 was recomputed on the downloaded bytes.

| File | Frozen SHA-256 | Drive-downloaded SHA-256 | Result |
|---|---|---|---|
| CODER_1_ZH_TW.xlsx | `cbbbaa0a9741426a051168439ae4f8ce2d212c2878ed1990e444a9b1e2655a29` | `cbbbaa0a9741426a051168439ae4f8ce2d212c2878ed1990e444a9b1e2655a29` | PASS |
| CODER_2_ZH_TW.xlsx | `5925ead55daa2c9db99a084c4cce48441bd6a3c2994371b1e170562bac0e3f38` | `5925ead55daa2c9db99a084c4cce48441bd6a3c2994371b1e170562bac0e3f38` | PASS |
| CODER_3_ZH_TW.xlsx | `50d8c818950a33ea4644fe038c8f89e9cde70990afd0d70dc194012c620084a9` | `50d8c818950a33ea4644fe038c8f89e9cde70990afd0d70dc194012c620084a9` | PASS |

`S1E_DRIVE_HASH_VERIFICATION=3/3_PASS`

The frozen files must not be opened/resaved in Google Sheets before distribution.

No human coding results existed at verification time.
