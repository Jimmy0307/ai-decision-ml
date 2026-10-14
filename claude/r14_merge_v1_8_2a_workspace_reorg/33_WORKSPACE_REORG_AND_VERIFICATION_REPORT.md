# 33 — Workspace Reorganization and Full Verification (V1.8.2a, 2026-10-14)

**Scope:** the local workspace `C:\NTUST_PAPER` was reorganized, and every frozen record was then re-verified.

**This round did not:**
- change any research content, manuscript, packet, freeze, G01–G16, the Enterprise model or the V1 protocol;
- start human coding;
- invalidate S1, because no packet content changed.

**Base:** `research/v1.8.2-v1-human-prefreeze-20261014` @ `e2781b66542a0f7b3a2ca51227d6ee781cb758f4`.

## 1. What moved

The reorganization had two parts.

**(a) Moves made by the researcher, 2026-10-14 10:02–10:26.** Observed, not logged by script:
- created `outputs\00_CURRENT`, `10_CANONICAL_EVIDENCE`, `20_SEALED_PRIVATE`, `80_HISTORY_2026` and `99_LEGACY`;
- moved the dated runs and this session's working folders into them.

**(b) Scripted, move-only completion: 71 moves.**
- 69 root files went to `ARCHIVE\`, `docs\pipeline_2026-04\`, `outputs\80_HISTORY_2026\…`, `outputs\99_LEGACY\…` and `outputs\10_CANONICAL_EVIDENCE\00_INPUT_BUNDLES\`.
- 2 output folders were moved: `20260911_AI_DECISION_V5_PRODUCTION` → `10_CANONICAL_EVIDENCE\04_V5_PRODUCTION_FREEZE\`, and `20260907_submission_package_v4` → `80_HISTORY_2026\09_SEP\`.
- Nothing was deleted or overwritten.
- Log: `MOVE_MANIFEST_20261014.csv`. Reverse script: `ROLLBACK_20261014.py`.
- 69 rows are `DONE_EARLIER_RUN`. Their first run stopped at a locked folder before the log was written, so they carry post-move SHA-256 only. A same-volume rename does not change content.
- 2 rows are `OK`, with file count and bytes identical before and after.

**What stayed in the root:** 28 files, all required by the pipeline. A reference scan (`root_dependency_scan.json`) confirmed that every file kept at the root is called by `run_local_pipeline.py`, `run_workspace_refresh.py`, a `run*.bat` launcher or `scripts\`. No root directory was moved.

**Local git working copy:** the researcher's move had taken 35 committed v1.8.2 files out of the tracked tree. They were restored with `git checkout`, so the working copy is clean. The moved copies in `00_CURRENT\03_V1_HUMAN_VALIDATION\03A_V1_8_2_FORMAL_OUTPUTS` were kept.

## 2. Path map for paths cited in earlier committed documents

| Old path cited in V1.8 / V1.8.1 / V1.8.2 documents | Current location |
|---|---|
| `outputs\20261014_AI_DECISION_V1_8_SOURCE_CLOSURE\` (V1.8 workspace W) | `outputs\10_CANONICAL_EVIDENCE\03_R14_STUDY1\01_SOURCE_CLOSURE_V1_8\` |
| `outputs\20261014_V1_8_1_STUDY1_FREEZE\` (git working copy, tools, .venv_docx) | `outputs\00_CURRENT\02_STUDY1_FREEZE\02_STUDY1_FREEZE_V1_8_1\` |
| `outputs\20261014_V1_8_2_PREFREEZE\SEALED_LOCAL_STUDY_TEAM_ONLY\` | `outputs\20_SEALED_PRIVATE\V1_8_2_STUDY_TEAM_ONLY\` |
| `outputs\20261014_V1_8_2_PREFREEZE\tools\` | `outputs\00_CURRENT\03_V1_HUMAN_VALIDATION\03_V1_HUMAN_VALIDATION_PREFREEZE_V1_8_2\tools\` |
| `outputs\20260929_V9_HUMAN_VALIDATION.zip` | `outputs\10_CANONICAL_EVIDENCE\01_V9_HUMAN_VALIDATION\20260929_V9_HUMAN_VALIDATION.zip` |
| `C:\NTUST_PAPER\V9_FINAL_SUBMISSION_CANDIDATE_20261004.docx` (R14 identity evidence in 13/18) | `outputs\80_HISTORY_2026\10_OCT\ROOT_V9_FINAL_SUBMISSION_CANDIDATES_20261004\` |
| `outputs\20260911_AI_DECISION_V5_PRODUCTION\` | `outputs\10_CANONICAL_EVIDENCE\04_V5_PRODUCTION_FREEZE\20260911_AI_DECISION_V5_PRODUCTION\` |

The committed documents are not edited: their paths are historical. Use this map instead.

## 3. Full verification after the move (`tools/verify_all_20261014.py`, result `verify_all_20261014_result.json`)

| Check | Rows | Result |
|---|---:|---|
| A. Local copies in `00_CURRENT` vs committed repo blobs | 108 | **92 identical.** 3 differ: older scratch outputs in local `tools\G\` (`hits.tsv`, `recompute_seg_out.json`; 02:55/03:00) and `tools\J\verify_stdout.txt`, versus newer committed versions (03:05). The committed versions are authoritative, and no frozen record is affected. 13 are scratch or cache files with no repo counterpart (`__pycache__`, trial DOCX/PDF, context notes); informational only. |
| B. V1.8.2 S1 freeze manifest | 23 | **23/23 OK.** This covers 21 committed files plus 2 sealed plaintexts at the new sealed location. |
| C. V1.8.1 Study 1 freeze ledger (18) | 49 | **43/43 hashed rows OK** across repo files, raw sources at the new W location and the external R14 docx. The 6 NOT_RECOVERED rows were skipped; see 34 for the recovery. |
| D. V1.8 extracted-file inventory | 1,295 | **1,295/1,295 OK** at the new W location |
| E. V1.8 raw input zips | 3 | **3/3 OK** (SHA-256 unchanged) |
| F. Reorganization move manifest | 71 | **71/71 OK.** Every new path exists, every old path is gone, and file hashes are unchanged. |
| Sealed files | 3 | Item map `2a84d5de…`, order log `79cd727f…` and seed `79caee63…` are unchanged |
| Git | — | Working copy clean at `e2781b6`. Remote v1.8.2 = `e2781b6`, main = `1f2e72f`. |

**Verdict: `WORKSPACE_REORG_VERIFIED=PASS`.** No frozen research record changed. The S1 packet freeze remains valid.
