# 10 — V1.8 Source-Verified Evidence Closure: Final Status

Run date: 2026-10-14
Workspace: `C:\NTUST_PAPER\outputs\20261014_AI_DECISION_V1_8_SOURCE_CLOSURE`

- The original zips are unchanged; their hashes were re-verified after extraction (`00_INPUT_HASHES.txt`).
- Nothing was committed, pushed or merged.

Execution: multi-agent.

| Agent | Phase |
|---|---|
| A | Authority map |
| B | Raw 50/20/19 and κ |
| C | Local sensitivity |
| D | Legacy quarantine |
| E | Flag closure |
| F | Manuscript patch |

The orchestrator wrote 00/01/07/09/10 and independently checked the v1.7→v1.8 diff (`08b`).

## Outputs

| File | Phase |
|---|---|
| `00_INPUT_MANIFEST.csv`, `00_INPUT_HASHES.txt` | 0 |
| `01_FILE_INVENTORY.csv` (1,295 files) | 1 |
| `02_V9_AUTHORITY_MAP.md` | 2 |
| `03_HUMAN_AUDIT_REPRODUCTION.md` | 3–4 |
| `04_LOCAL_SENSITIVITY_REPRODUCTION.md` | 5 |
| `05_LEGACY_SOURCE_BOUNDARY.md` | 6 |
| `06_SOURCE_FLAG_CLOSURE.csv` (275 rows), `06_SOURCE_FLAG_CLOSURE_NOTES.md` | 7 |
| `07_FULL_REANALYSIS_DECISION_MEMO.md` | 8 |
| `08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md`, `08_PATCH_LOG.md`, `08b_V17_TO_V18_SEGMENT_DIFF.md` | 9 |
| `09_FINAL_GREP_REPORT.md` | 10 |

Helper scripts are in the session scratchpad under `v18\A`–`F` and `v18\p01.py` / `p10.py`. All were run with `python -I`, and no package code was executed.

## Final output

```
V9_SOURCE_VERIFIED=PARTIAL
50_20_19_REPRODUCED=YES
KAPPA_REPRODUCED=YES
LOCAL_SENSITIVITY_REPRODUCED=YES
G01_G16_REMOVAL_IN_LOCAL_SIDECAR=NONE
FULL_REANALYSIS_EXECUTED=NO
FULL_REANALYSIS_RECOMMENDED=NO
LEGACY_ZIP_CLASSIFICATION=LEGACY_HISTORICAL_PROVENANCE
SOURCE_CLOSURE_STATUS=PARTIAL
MANUSCRIPT_V1_8_CREATED=YES
SUBMISSION_READY=NO
```

### Basis for each value

- **V9_SOURCE_VERIFIED=PARTIAL.**
  - The human-validation chain is CONFIRMED from the raw rows: the 30/30 hash manifest and both event hash chains verify.
  - 12 of 37 protected inputs are absent from all packages. These include the frozen DB, the freeze manifests and the original 400/120 samples.
  - The official core file is PROBABLE only, because it exists as a byte-identical reproduction inside V9.1.
  - The sidecar generator script is NOT_RECOVERED.
  - The protected hash of `HUMAN_AUDIT_APPEND_ONLY_LOG.csv` does not match. The package itself discloses this as UNVERIFIED, with no evidence of tampering.
- **50/20/19 and κ.**
  - Recomputed by independent code from the raw CSVs and the events JSONL: 50/50, 20/20, 19/19.
  - κ values are .5614 / .1798 / .0476 / .1398 / .3162, all within 0.00004 of `HUMAN_RELIABILITY_FINAL.csv`, so there is no `HUMAN_RELIABILITY_CONFLICT`.
  - The bootstrap CIs differ between the FINAL and `_20` files. v1.8 cites FINAL, and the CIs were not re-run.
- **Local sensitivity.**
  - Core stays at 32 cells; the split goes from 16/16 to 15/17.
  - Gained: `HUMAN_AUGMENTATION×RISK_ASSESSMENT`, DEPLETED. Lost: `COORDINATION_EXECUTION×GENERAL_DECISION_PROCESS`, ENRICHED.
  - The other 31 pairs are unchanged, and none of G01–G16 is removed.
  - Answers to the four questions: (1) exact membership does change, one in and one out; (2) no G cell is removed; (3) yes, the only core changes are one added depleted pair and one lost enriched pair, although 33/120 cells differ in counts or non-core direction; (4) the full corpus was **not** rerun. This was a local sidecar using 20 reconciled labels plus 30 first-coder labels.
  - Membership and the promotion rule were reproduced. The null-model draws themselves were not re-executed, because the generator is missing.
- **FULL_REANALYSIS_RECOMMENDED=NO (before v1).** The reasons are in 07 §8:
  - The run is not executable without the missing protected inputs.
  - The expected result equals the sidecar, which leaves G01–G16 intact.
  - A rerun cannot fix the real limitation, which is a small targeted sample with low model–human agreement.
  - The V9 package's own `FULL_REANALYSIS_REQUIRED` remains an open **researcher decision**, and v1.8 states it as such.
- **SOURCE_CLOSURE_STATUS=PARTIAL.**
  - Closed: all V9 provenance flags in v1.7. That is 81 CLOSED rows in 06, and in 130 all 29 `2026-09-29` dates were re-dated or re-sourced.
  - Still open: 12 non-V9 sources not found (references, EUR-Lex, format templates, the V5 Data Pack, Drive) and 124 KEEP_AS_LIMITATION rows (enterprise data, V1 human coding and similar).
  - Not regenerated this round: artifact 132 (.csv/.xlsx) still carries 16 old `〔2026-09-29 紀錄，待核〕` flags; the 128/131/133/137 memos still describe V9 as ABSENT; the 130 .docx has not been rebuilt from v1.8.
- **MANUSCRIPT_V1_8_CREATED=YES.**
  - sha256 `1515b0f2…7ad58`, 3,080 lines, same as v1.7.
  - 34 lines changed through 41 asserted replacements.
  - Math blocks, headings (182), G01–G16 rows, G→M and VCP/VSC/DL/NEV are byte-identical to v1.7. No R14 empirical value changed.
  - Phase 10 found 0 substantive forbidden-claim hits.
- **SUBMISSION_READY=NO.**
  - V9 `FINAL_STATUS.json` itself says NO.
  - Open P0 items from 137 remain: V1 human construct validation, V0 enterprise sources, ethics approvals, parameter identification, V7 calibration, the reanalysis decision, author metadata, and format files.

## New findings to carry forward (not fixed this round)

1. 128 L15 mislabels `完整資料來源.zip` as the "V5 Data Pack". It is actually the legacy structural-hole study (05). The real V5 Data Pack is NOT_RECOVERED.
2. v1.7/v1.8 attribute the "84–85/120" re-segmentation figures to R14, but the source is V9.1 `SEGMENTATION_SENSITIVITY` (2026-10-03). This attribution has not been audited and was left unchanged.
3. The V9.1 segmentation sensitivity drops G15 (S1, S2) and G07 (S1). v1.8 already describes G07 and G15 as "邊界敏感"; that wording is consistent but should be cross-checked.
4. `FINAL_HUMAN_AUDIT_REPORT.md` contains an unfilled `{taxblock}` placeholder. Use `FINAL_ERROR_TAXONOMY.*` instead.
5. `REANALYSIS_CANDIDATES_FROM_HUMAN_AUDIT.csv` must not be used as a propagation list. Use 04 T4.
