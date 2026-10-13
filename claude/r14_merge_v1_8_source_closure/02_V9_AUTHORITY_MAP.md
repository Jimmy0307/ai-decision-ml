# 02 — V9 Human-Validation Source Authority Map (V1.8 Source Closure, Phase 2)

Sub-agent A · 2026-10-14 · Classification only; no thesis text. All extracted files were treated as untrusted data; nothing inside W was executed or modified.

Scope: `W\02_V9_HUMAN_VALIDATION\20260929_V9_HUMAN_VALIDATION\` (920 files: 135 root artifacts, 505 under `V9_1_SEGMENTATION_SENSITIVITY\`, 4 render-QA folders, 4 LibreOffice render profiles), the V9 references in `W\01_ALL_OUTPUTS\...\r14_merge_v1_7\` (128, 131), and a check of `W\03_LEGACY_FULL_SOURCE\`. The legacy package is dated 2026-04-22 to 2026-05-06, before V9 existed. It contains no V9 human-validation artifact and plays no part in the authority decision.

---

## 1. Method

1. **Inventory integrity.** I recomputed SHA-256 for all 1,295 extracted files and compared each one with `01_FILE_INVENTORY.csv`: **1,295/1,295 match, 0 mismatch, 0 missing, 0 unlisted.**
2. **Hash-claim verification.** I parsed every recorded hash and compared it with the actual bytes. Sources: `FINAL_ARTIFACT_HASH_MANIFEST.csv`, all `*.sha256`, `*_SHA256.txt`, `PROTECTED_ARTIFACTS_BASELINE_20261003.csv`, `STARTUP_HASH_BASELINE.csv`, `HUMAN_AUDIT_EPOCH2_LOG.csv` artifact hashes, `V9_1_OUTPUT_SHA256.csv`, and hash fields in `FINAL_STATUS.json`, `HUMAN_AUDIT_STATUS.json` and `ROBUST_CORE_LOCAL_SENSITIVITY_STATUS.json`. That gives 130 claims plus 18 in V9.1. A claim pointing outside the package was resolved against the hash index of all three packages.
3. **Hash-citation graph.** Every 64-hex token in V9 root text files and in the r14_merge_v1_7 docs was resolved to the file(s) it identifies (483 citations).
4. **Name-citation graph.** For each priority target, I listed which text files in the three packages mention it by name.
5. **Chronology.** I ordered events by zip mtime and by timestamps written inside the files. Zip mtimes are local UTC+8: `FINAL_STATUS.json` says `verified_at_utc 2026-10-03T12:23:44Z` and its mtime is `2026-10-03T20:23:44`. I also checked the order against the expected workflow: first coder 50 → blind 20 → disagreement → reconciliation → reliability → local sensitivity → forensic audit → readiness.
6. **Recomputation from raw rows (top of the source hierarchy).** I recomputed from `FIRST_CODER_50_FINAL_FROZEN.csv`, `BLIND_REPEAT_20_FINAL_FROZEN.csv`, `HUMAN_RECONCILED_20.csv`, `HUMAN_RECONCILIATION_EVENTS.jsonl`, `HUMAN_AUDIT_EPOCH2_LOG.csv` and `ROBUST_CORE_LOCAL_SENSITIVITY.csv`: counts, Cohen's kappa, model-vs-human agreement, event hash chains and sensitivity membership.

Helper scripts (kept for reproducibility; run with `python -I`):
- `C:\Users\user\AppData\Local\Temp\claude\C--NTUST-PAPER\b2185478-fbc8-4bee-8105-bb5557dd964b\scratchpad\v18\A\authority_scan.py` → `inventory_check.json`, `hash_claims.csv`, `hash_citations.csv`, `name_citations.json`
- `...\scratchpad\v18\A\reproduce_checks.py` → `reproduce_checks_output.txt`

---

## 2. Recomputation results (raw rows → reported values)

| Quantity | Reported in FINAL set | Recomputed from raw rows | State |
|---|---|---|---|
| First-coder frozen set | 50 COMPLETE, 50 unique, coder_id 1 | 50 / 50 unique / all COMPLETE / coder_id `1` ×50 / all stratum A | CONFIRMED |
| Blind second-coder set | 20/20, seed 20261003, subset of 50 | 20 / 20 unique / all COMPLETE / coder_id `2` ×20 / subset of 50 = True | CONFIRMED |
| Records with ≥1 C1–C5 disagreement | 19 | 19 | CONFIRMED |
| Pre-adjudication exact agreement C1..C5 | 15, 7, 4, 4, 12 /20 | 15, 7, 4, 4, 12 | CONFIRMED |
| Cohen's kappa C1..C5 | .561/.180/.048/.140/.316 | .5614/.1798/.0476/.1398/.3162 | CONFIRMED |
| Confidence exact match | 9/20 | 9 | CONFIRMED |
| Reconciled set | 20 rows; 19 HUMAN_ADJUDICATION + 1 UNANIMOUS | 20 unique; FINAL_C1–C5 populated 20/20; basis 19 / 1 | CONFIRMED |
| Original columns preserved in HUMAN_RECONCILED_20 | yes | 0 mismatches vs both frozen snapshots | CONFIRMED |
| Reconciliation events | 19, hash-chained | 19 COMPLETE events, researcher_id `3`; prev-links 19/19; `current_event_hash` = SHA-256(sorted compact JSON) reproduced **19/19**; 19/19 row→event hash links match | CONFIRMED |
| Epoch-2 audit log | PASS | genesis-file hash → prev-link chain OK; current_event_hash reproduced **5/5** | CONFIRMED |
| Model vs first-coder (50) | rel 14, AI 19, Dec 9, incl 33/42, 9 model-INCL/human-EXCL, 0 reverse | 14, 19, 9; (INCLUDE 33, EXCLUDE 9, UNCERTAIN 8), with model eligible = True for all 50 | CONFIRMED |
| Model vs reconciled (20) | rel 3, AI 7, Dec 7, incl 10/18, 8 model-INCL/final-EXCL | 3, 7, 7; FINAL_C5 INCLUDE 10 / EXCLUDE 8 / UNCERTAIN 2 | CONFIRMED |
| Local sensitivity | 120 cells; core 32→32; +HUMAN_AUGMENTATION×RISK_ASSESSMENT (DEPLETED); −COORDINATION_EXECUTION×GENERAL_DECISION_PROCESS (ENRICHED); 24 count changes; 3 direction changes; shared-direction changes 0; main q≤.05 47/47 | identical. Official core 16E/16D → sidecar **15E/17D** | CONFIRMED (from the manifest-pinned sidecar table) |
| Official core file hash `a43b4b58…` | official frozen | byte-identical file found only as the V9.1 baseline **reproduction** (`_baseline_reproduction/13_RESULTS_FREEZE/results_freeze_v1_20261003T133318Z/FINAL_ROBUST_CORE_32.csv`). The original freeze folder is not in the package | PROBABLE (reproduction matches the pinned hash; original file not present) |
| Sidecar core file hash `4e412a07…` | sidecar core | **not present in any package** | NOT_RECOVERED (membership is still CONFIRMED via the sensitivity CSV) |

---

## 3. Timeline

Times are given in UTC; local zip mtimes are UTC+8.

| # | UTC | Event | Evidence |
|---|---|---|---|
| 1 | 2026-09-18 13:22 → 09-19 08:01 | Official analytical freeze v2 and results freeze v1 (32-cell core) | folder names in PROTECTED/STARTUP baselines |
| 2 | 2026-09-21 / 09-23 | V9 camera-ready manuscript; submission freeze | `FREEZE/AI_DECISION_V9_SUBMISSION_FREEZE_20260923` paths (not in package) |
| 3 | 2026-09-29 15:50 → 09-29 17:55 | V9 validation workstation built (400/120 design); `STARTUP_HASH_BASELINE.csv` | mtimes 09-29 23:50 → 09-30 01:55 |
| 4 | 2026-09-30 02:03:09 | First COMPLETE submission (V5HV-0001, REC-A51A4D85E6A1A0AF), described as accidental | `RECORD_REOPEN_AUDIT_LOG.csv` |
| 5 | 2026-09-30 02:25:37 / 02:32:20 | Accidental-submission reopen; report written | `ACCIDENTAL_SUBMISSION_REOPEN_REPORT.md` |
| 6 | 2026-09-30 07:08–07:16 | Runtime codebook / alias gate | mtimes 15:08–15:16 |
| 7 | 2026-09-30 09:03:34 → 10-02 18:44:12 | First-coder coding of the 50 (REC-A51A… resubmitted 09:03:34) | `coder_timestamp` range in the frozen 50 |
| 8 | 2026-10-02 18:44:12 | `HUMAN_VALIDATION_FINAL_REPORT.md`: PARTIAL, 50/400, 0/120 | internal "Generated (UTC)" |
| 9 | 2026-10-02 19:49:38 | FIRST_CODER_50 frozen (`dd332dd8…`) | `FIRST_CODER_50_SHA256.txt` |
| 10 | 2026-10-02 20:18–20:54 | Protected baseline written; protocol revised 400/120 → 50/20, not preregistered | `PROTECTED_ARTIFACTS_BASELINE_20261003.csv`, `PROTOCOL_REVISION_50_20.md` |
| 11 | 2026-10-02 20:56:20 / 20:57:02 | Legacy log forensic snapshot; blind-20 sample reproduced (seed 20261003) | `LEGACY_AUDIT_LOG_INTEGRITY_NOTE.md`, `SECOND_CODER_BLIND_20_SHA256.txt` |
| 12 | 2026-10-02 21:07:47 → 21:16:45 | Epoch-2 log events E2-001..005; append verification PASS | `HUMAN_AUDIT_EPOCH2_*` |
| 13 | 2026-10-02 21:10 | `FINAL_STATUS.md` = second coder 0/20, ADJUDICATION WAITING | mtime 05:10 |
| 14 | 2026-10-02 21:22:29 → 10-03 06:38:24 | Blind second-coder coding; save bug diagnosed and fixed at 21:22–21:49 | blind `coder_timestamp`; `SECOND_CODER_BUG_PRESTATE*`, `SECOND_CODER_SAVE_FIX_VERIFICATION.md` |
| 15 | 2026-10-03 06:38:24 | `BLIND_REPEAT_20_FINAL_FROZEN.csv`; `HUMAN_AUDIT_STATUS.json` (20/20, adjudication WAITING) | mtime 14:38:24 |
| 16 | 2026-10-03 06:46:34 | `FINAL_CODING_INTEGRITY_CHECK.md` | internal "Verified 14:46:34+08:00" |
| 17 | 2026-10-03 06:50:54 | `HUMAN_RELIABILITY_20.*`; disagreement queue of 19 | mtime 14:50:54 |
| 18 | 2026-10-03 07:00:26 / 07:02:00 | `FINAL_HUMAN_AUDIT_DECISION.md` (C: reconciliation required, 0/19); `HUMAN_RECONCILIATION_GATE_STATUS.json` | mtime 15:00/15:02 |
| 19 | 2026-10-03 07:45:24 → 11:09:05 | 19 human reconciliation events (researcher_id 3) | `HUMAN_RECONCILIATION_EVENTS.jsonl` |
| 20 | 2026-10-03 11:14:12 | `HUMAN_RECONCILED_20.csv` (`4b7ceac2…`) + detached checksum | mtime 19:14:12 |
| 21 | 2026-10-03 11:15:54 → 11:16:48 | `HUMAN_RELIABILITY_FINAL.csv`, `MODEL_VS_RECONCILED_20*`, `MODEL_VS_HUMAN_FINAL_50.md` | mtimes |
| 22 | 2026-10-03 11:55 → 12:09:56 | Final error taxonomy; local sensitivity (CSV 11:58:50, DIFF 11:59:54, STATUS 12:09:56); `REANALYSIS_PROPOSAL.md` | mtimes |
| 23 | 2026-10-03 12:19:50 → 12:21:14 | Patched V9 candidate docx (`f5c9366a…`); render QA (22 pages) | mtimes |
| 24 | 2026-10-03 12:23:44 | `FINAL_STATUS.json`, `FINAL_HUMAN_AUDIT_DECISION_FINAL.md`, `V9_FINAL_FORENSIC_AUDIT.md`, `FINAL_HUMAN_AUDIT_REPORT.md`, `FINAL_SUBMISSION_READINESS_REPORT.md`, Codex / multi-agent summaries | `verified_at_utc` + mtime |
| 25 | 2026-10-03 12:24:32 | `FINAL_ARTIFACT_HASH_MANIFEST.csv` (last root write; pins 30 artifacts) | mtime 20:24:32 |
| 26 | 2026-10-03 13:31 → 16:41:46 | **V9.1 segmentation sensitivity** sidecar: baseline reproduction 13:31:57; nonconforming S2 archived 15:51:49; final 16:41:45 | `V9_1_SEGMENTATION_SENSITIVITY/FINAL_STATUS.json` |
| 27 | 2026-10-14 | v1.7 `128_CANONICAL_STATE.md` / `131_…REPORT.md` record the V9 package as **ABSENT** and label V9 values "user-reported (2026-09-29)" | 128 line 14; 131 §2, §8 |

The internal timestamps follow the expected workflow order with no inversions: first-coder freeze → blind → reliability-20 → gate → reconciliation → reliability-FINAL → sensitivity → forensic/readiness → manifest. After 12:24:32Z nothing in the V9 root was written. V9.1 is a later and separate experiment.

---

## 4. Authority table

Hashes are the first 12 hex characters. Timestamps are local zip mtimes, all on 2026-10-03 unless stated. "Hash-verified" means a recorded hash elsewhere matches the actual bytes. "Cited by" lists the downstream files that cite the target by name or hash.

| File | sha256 | mtime | Internal status | Cited by | Hash-verified? | Classification | Rationale |
|---|---|---|---|---|---|---|---|
| FIRST_CODER_50_FINAL_FROZEN.csv | dd332dd8cfec | 03:49:38 | 50 COMPLETE | Manifest, .sha256, FINAL_STATUS.json, EPOCH2 E2-001, RECONCILIATION_FINAL_AUDIT, FINAL_CODING_INTEGRITY_CHECK | YES (5 independent claims) | **FINAL_AUTHORITY (raw rows)** | Raw source; recomputation matches every derived number. Byte-identical to FIRST_CODER_50_FROZEN.csv |
| BLIND_REPEAT_20_FINAL_FROZEN.csv | 6afc8d7a2c2b | 14:38:24 | 20 COMPLETE | Manifest, .sha256, FINAL_STATUS.json, RECONCILIATION_FINAL_AUDIT | YES | **FINAL_AUTHORITY (raw rows)** | Byte-identical to the final SECOND_CODER_BLIND_20.csv |
| HUMAN_RECONCILED_20.csv + HUMAN_RECONCILIATION_EVENTS.jsonl | 4b7ceac2c8c8 / 9270accc7657 | 19:14:12 / 19:09:04 | 19 HUMAN_ADJUDICATION + 1 UNANIMOUS | Manifest, RECONCILIATION_FINAL.sha256, FINAL_STATUS.json, RECONCILIATION_FINAL_AUDIT | YES; event chain reproduced 19/19 | **FINAL_AUTHORITY (raw rows)** | Append-only, hash-chained human decisions |
| FINAL_STATUS.json | d9226d3148b9 | 20:23:44 | decision B: CONVERGED / LOCAL_SENSITIVITY_CHANGED / FULL_REANALYSIS_REQUIRED; submission_ready=false | Manifest | YES | **FINAL_AUTHORITY (machine-readable state)** | Latest status file; every numeric field reproduced from raw rows |
| FINAL_STATUS.md | 805d9d809fd3 | 05:10:04 | 0/20, ADJUDICATION WAITING | README, HUMAN_VALIDATION_FINAL_REPORT | no claim | SUPERSEDED_HISTORICAL_CHECKPOINT | Pre-blind checkpoint, about 15 h before the .json and never updated |
| HUMAN_AUDIT_STATUS.json | ce48b8271ef4 | 14:38:24 | 20/20 but ADJUDICATION WAITING, HUMAN_VALIDATION PARTIAL | README | no claim | SUPERSEDED_HISTORICAL_CHECKPOINT | Snapshot at blind freeze; predates reconciliation |
| FINAL_HUMAN_AUDIT_DECISION.md | 5faae2abb059 | 15:00:26 | "C. HUMAN_RECONCILIATION_REQUIRED", 0/19 | RECONCILIATION_INTERFACE_SHA256.txt | YES | SUPERSEDED_HISTORICAL_CHECKPOINT | Gate decision before reconciliation |
| FINAL_HUMAN_AUDIT_DECISION_FINAL.md | 6de949b2eef7 | 20:23:44 | CONVERGED / LOCAL_SENSITIVITY_CHANGED / FULL_REANALYSIS_REQUIRED | Manifest | YES | **FINAL_AUTHORITY (decision label)** | Latest decision; consistent with FINAL_STATUS.json and raw rows |
| HUMAN_RECONCILIATION_GATE_STATUS.json | 68559b6f34ae | 15:02:00 | REQUIRED, 0/19, server RUNNING | RECONCILIATION_INTERFACE_SHA256.txt | YES | SUPERSEDED_HISTORICAL_CHECKPOINT | Gate opened before reconciliation; later superseded (server stopped, 19/19) |
| HUMAN_RELIABILITY_20.csv/.md | 239aabf1f8bd / ec5d20cae2ba | 14:50:54 | pre-reconciliation, queue 19 | none | no claim | SUPERSEDED_HISTORICAL_CHECKPOINT | Same point estimates as FINAL; bootstrap CIs differ (seed scheme) |
| HUMAN_RELIABILITY_FINAL.csv/.md | ef7e55449686 / 44809c692c45 | 19:15:54 / 20:12:10 | PRE_ADJUDICATION_INTER_RATER | Manifest; values match v1.7/131 Table H-1 | YES | **FINAL_AUTHORITY (reliability)** | Kappa recomputed. These are the CIs v1.7 cites |
| ROBUST_CORE_LOCAL_SENSITIVITY.csv (+_DIFF.csv) | e3166ee183e1 / f6607aaee5c6 | 19:58:50 / 19:59:54 | 120 cells; 2 membership changes | Manifest | YES | **FINAL_AUTHORITY (sensitivity result)** | Membership and counts recomputed from the table. The sidecar core file is not shipped |
| ROBUST_CORE_LOCAL_SENSITIVITY_STATUS.json / .md | efc63b5b8841 / b25b9a84b42b | 20:09:56 | CHANGED | Manifest (.md); FINAL_STATUS.json mirrors it | .md YES; .json not pinned by the manifest | SUPPORTING | Summary of the CSV, consistent with it. The STATUS.json is not hash-pinned |
| V9_FINAL_FORENSIC_AUDIT.md | 36a117a0de99 | 20:23:44 | Fatal none; Major = sensitivity change; SUBMISSION_READY=NO | Manifest | YES | SUPPORTING (current audit report) | Numeric claims reproduced. Claims about the source docx, the original 400/120 and freeze artifacts cannot be checked here (files absent) |
| FINAL_HUMAN_AUDIT_REPORT.md | 63d651baa770 | 20:23:44 | 19/19 COMPLETE; decision as above | Manifest | YES | SUPPORTING (with defect) | Contains an unrendered template placeholder `{taxblock}` where the error-taxonomy table should be. Use FINAL_ERROR_TAXONOMY.csv/.md for those counts |
| FINAL_SUBMISSION_READINESS_REPORT.md | 55e83f696551 | 20:23:44 | SUBMISSION_READY=NO | Manifest | YES | **FINAL_AUTHORITY (readiness status)** | Latest readiness verdict; consistent with FINAL_STATUS.json |
| FINAL_ARTIFACT_HASH_MANIFEST.csv | 9387d8d2159b | 20:24:32 | pins 30 artifacts | nothing (no external anchor) | 30/30 MATCH | **FINAL_AUTHORITY (integrity anchor)** | Last write in the V9 root. Weakness: the manifest itself is not pinned by any detached checksum |
| HUMAN_AUDIT_EPOCH2_GENESIS.md / _LOG.csv / _APPEND_VERIFICATION.md | e5db33e886ef / 9ef14dc0aea6 / 904202656064 | 05:07–05:16 | AUDIT_EPOCH2_INTEGRITY=PASS | HUMAN_AUDIT_STATUS.json, .sha256 files, INTEGRITY_VERIFICATION, README | YES; chain reproduced 5/5 | SUPPORTING (provenance) | Covers events only up to 10-02 21:16Z (first-coder freeze, blind sample, blindness). Blind completion and reconciliation are covered by the separate reconciliation chain |
| ACCIDENTAL_SUBMISSION_REOPEN_REPORT.md | 10179e7667c5 | 09-30 10:32:20 | REOPEN=PASS | none | its "reopen event log SHA" `8FA19EA1…` = actual RECORD_REOPEN_AUDIT_LOG.csv (MATCH). Its annotation-audit "after append" hash `341971A2…` is not current (later appends) | SUPPORTING (historical provenance) | Pre-protocol-revision event. The record was later re-coded (09:03:34Z) and is in the frozen 50 |
| RECORD_REOPEN_AUDIT_LOG.csv | 8fa19ea138f2 | 09-30 10:25:36 | 1 event | PROTECTED baseline, INTEGRITY_VERIFICATION, reopen report | YES (2 claims) | SUPPORTING (historical provenance) | Unchanged since the event |
| PROTECTED_ARTIFACTS_BASELINE_20261003.csv | 0bf9042f8d22 | 04:18:42 | 37 protected paths | INTEGRITY_VERIFICATION | n/a | SUPPORTING | In-package rows: 10 MATCH, 1 MISMATCH (HUMAN_AUDIT_APPEND_ONLY_LOG.csv, `c958f807…` vs `151cf3d0…`; disclosed as the legacy log). 14 external rows are byte-identical to files in the package (13 from the V9.1 baseline reproduction + SAMPLING_MANIFEST). 12 external rows are absent (see §5) |
| STARTUP_HASH_BASELINE.csv | 8d6e50cffcee | 09-30 01:55:42 | 21 paths | WORKSTATION_RUNTIME_CHECK | n/a | SUPERSEDED_HISTORICAL_CHECKPOINT | Pre-coding baseline: 1 MATCH, 16 found as reproductions, 4 absent |
| *.sha256 / *_SHA256.txt (9 files) | — | various | — | — | 18 MATCH; 2 point-in-time MISMATCH for the mutable `SECOND_CODER_BLIND_20.csv` (queue state `0100e524…` at 04:57; bug prestate `c55ff2c8…` at 05:28) | SUPPORTING | Mismatches come from a working file that legitimately changed. The final state equals BLIND_REPEAT_20_FINAL_FROZEN |
| HUMAN_VALIDATION_FINAL_REPORT.md | acc1abc1c9fd | 04:27:30 | PARTIAL, 50/400, 0/120 (+ appended note: 0/20) | none | no | SUPERSEDED_HISTORICAL_CHECKPOINT | Named FINAL but is the **earliest** status report |
| README.md / HUMAN_AUDIT_50_20_PIPELINE.md | 2ec446e04682 / cced1718c937 | 05:13:52 | 0/20; points to HUMAN_AUDIT_STATUS.json/FINAL_STATUS.md as "current authoritative" | — | no | SUPERSEDED_HISTORICAL_CHECKPOINT | Stale pointers, never updated after convergence |
| V9_1_SEGMENTATION_SENSITIVITY/ (FINAL_STATUS.json, SEGMENTATION_SENSITIVITY_FINAL_REPORT.md, …) | FINAL_STATUS sha in inventory | 10-04 00:41:44–46 | SEGMENTATION_SENSITIVITY_COMPLETE; MODERATE_TURNOVER; S1/S2 core 31/31; counts changed 84/120 and 85/120 | its own V9_1_OUTPUT_SHA256.csv. It cites `FINAL_ERROR_TAXONOMY_CASES.csv` (`8949b671…`) as input | own manifest 18/18 MATCH | SUPPORTING (separate later sidecar) | See §6. Its own `FINAL_STATUS.json` is a different file from the root FINAL_STATUS.json and must not be confused with it |
| 01 r14_merge_v1_7/128_CANONICAL_STATE.md, 131_HUMAN_VALIDATION_INTEGRATION_REPORT.md | — | 10-14 | V9 "ABSENT / user-reported" | — | no V9 hash citations (only 1 hex token in 130, unresolved) | SUPERSEDED_HISTORICAL_CHECKPOINT (for the V9-availability claim) | Their numbers match the V9 FINAL artifacts, but their "artifact pending" status is now outdated |

UNRESOLVED: none of the priority targets. The residual unverifiable claims are listed in §5.

---

## 5. Contradictions and integrity notes

1. **FINAL_STATUS.md vs FINAL_STATUS.json.** Same stem, opposite states. The .md (2026-10-03 05:10 local) says `SECOND_CODER_COMPLETED=0/20`, `ADJUDICATION=WAITING`. The .json (20:23:44) says 20/20, 19/19 reconciled, converged. The .json is authoritative.
2. **HUMAN_AUDIT_STATUS.json is internally mixed.** It says `SECOND_CODER_COMPLETED=20/20` and `second_coder.status=COMPLETE`, but also `ADJUDICATION=WAITING`, `HUMAN_VALIDATION=PARTIAL` and next_action "At 20/20, prepare…". It is a frozen 14:38 checkpoint, superseded.
3. **FINAL_HUMAN_AUDIT_DECISION.md vs …_FINAL.md.** The first says reconciliation required, 0/19. The second says converged. Chronology settles it: 15:00 vs 20:23.
4. **HUMAN_RECONCILIATION_GATE_STATUS.json** says 0/19, `server_status=RUNNING_VERIFIED`, `local_sensitivity=NOT_RUN_HUMAN_GATE`. `HUMAN_RECONCILIATION_FINAL_AUDIT.md` later says 19/19 and the server stopped. The gate file is superseded.
5. **README.md and HUMAN_AUDIT_50_20_PIPELINE.md** still say 0/20 and name `HUMAN_AUDIT_STATUS.json` / `FINAL_STATUS.md` as the "current authoritative" state. They also describe planned outputs that were never produced under those names (`ADJUDICATION_QUEUE_20.csv`, `ADJUDICATION_LOG_20.csv`, `HUMAN_AUDIT_FINAL_STATUS.json`). The real outputs are `HUMAN_DISAGREEMENT_QUEUE_20.csv`, `HUMAN_RECONCILIATION_EVENTS.jsonl` and `FINAL_STATUS.json`. The pointers are stale.
6. **HUMAN_VALIDATION_FINAL_REPORT.md** is named FINAL but is the earliest report (10-02 18:44Z, PARTIAL, 0/120). Its appended revision notice still says 0/20.
7. **HUMAN_RELIABILITY_20 vs _FINAL.** Point estimates are identical. The kappa bootstrap CIs differ for C2–C5 by ≤0.006: for example C2 is (−0.079, 0.423) in _20 and (−0.081, 0.429) in FINAL, because the seed scheme changed from "derived from 20261003" to "20261003–20261007". v1.7/131 Table H-1 uses the FINAL CIs, which is correct.
8. **FINAL_HUMAN_AUDIT_REPORT.md has an unrendered `{taxblock}` placeholder.** The error-taxonomy table is missing from a manifest-pinned "FINAL" report. Counts must come from `FINAL_ERROR_TAXONOMY.csv/.md` or `FINAL_STATUS.json` (14 categories, 77 tags, 33 unique records).
9. **Protected-baseline mismatch.** `HUMAN_AUDIT_APPEND_ONLY_LOG.csv` is expected `c958f807…` but is actually `151cf3d0…`. This is disclosed as `LEGACY_AUDIT_LOG_INTEGRITY=UNVERIFIED` / `TAMPERING_EVIDENCE=NONE_FOUND`. The historical bytes are not in the package, so the state remains UNRESOLVED and is not evidence of tampering.
10. **Claims that cannot be checked from this package.** `FINAL_STATUS.json` asserts `original_400_sample_unchanged=PASS`, `original_120_sample_unchanged=PASS` and `frozen_results_unchanged=PASS`. The original `HUMAN_VALIDATION_400.csv` (`dc242f8d…`), `SECOND_CODER_120.csv` (`cc68a1ea…`), the V9 source manuscript docx (`62aff771…`) and PDF (`75db5775…`), `workbench.sqlite`, the FSC stage files, `FINAL_RESULTS_FREEZE_MANIFEST.json`, `FREEZE_ROOT_SHA256.txt` and `SHA256SUMS.csv` are **not in any extracted package**: 12 protected rows are NOT_RECOVERED. `RENDER_QA_SOURCE_20261003/V9_…20260921.pdf` (`cb805865…`) is a re-render, not the protected PDF. The official frozen outputs are supported only indirectly, through 13 byte-identical files from the V9.1 baseline reproduction.
11. **The sidecar core file (`4e412a07…`) is not shipped.** Membership is still CONFIRMED from the pinned `ROBUST_CORE_LOCAL_SENSITIVITY.csv`.
12. **v1.7 (128/131) vs package.** 128/131 say the V9 package was ABSENT and date the V9 state "2026-09-29". The package exists; 2026-09-29 is the workstation creation date, and the convergence decision is dated **2026-10-03T12:23:44Z**. 131's derived claims are now CONFIRMED by the sensitivity CSV: remaining 31 cells unchanged, sidecar 15 enriched / 17 depleted, shared-core direction changes 0. 131 E49 asks whether reconciled labels entered the re-segmentation analysis. V9.1 states explicitly that "no final/reconciled human label was propagated"; it used human-audit error tags only to force 11 records into candidate selection.
13. **Patch-scope wording is consistent.** "14 intended paragraphs + 2 edition details" in CODEX matches "16 edited paragraphs" in FORENSIC. Not a contradiction.
14. The Codex audit's claim "36/37 protected hashes match" cannot be fully re-verified here: 10 MATCH + 1 MISMATCH in-package, 14 identical copies, 12 absent.

---

## 6. What is V9_1_SEGMENTATION_SENSITIVITY?

It is a separate, later sidecar experiment ("V9.1", 2026-10-03 13:31–16:41Z), run after the human-audit convergence. It tests **conservative evidence re-unitization**: long or multi-clause strict records are split into segments and the affected segments are re-mapped with `qwen2.5:14b`. The run made 8 new calls; 199 outputs were valid and grounded, 28 grounding-invalid and 1 technical failure, and these were left unmapped.

- Scope: 3,112 of 6,499 strict records were candidates (47.88%). There are two segmentation rules, S1 and S2. The first S2 (comma-split) was found nonconforming and archived (`_S2_COMMA_SPLIT_NONCONFORMING_ARCHIVE_20261003T235149`, not used). The `_superseded_*` subfolders are earlier abandoned attempts.
- Results: S1 / S2 robust core 31 / 31; baseline 32 retained 29 / 30; observed counts changed in 84 / 85 of 120 cells; main directions changed in 12 / 11 cells. The verdict is `MODERATE_TURNOVER` (descriptive; it authorizes no promotion).
- Relation to the human audit: it **does not** propagate reconciled human labels. It is a different measurement operation from the local audited-label sensitivity (`ROBUST_CORE_LOCAL_SENSITIVITY*`). It is the source of the "84–85/120" re-segmentation figures that v1.7/131 attribute to R14.
- Integrity: its own `V9_1_OUTPUT_SHA256.csv` matches 18/18. Its `_baseline_reproduction` reproduces 13 protected official freeze artifacts byte-for-byte, including the official core `a43b4b58…`.
- Classification: SUPPORTING evidence for the segmentation-sensitivity claim only. It is not an authority for the human-validation decision.

---

## 7. Authoritative V9 human-validation source set (for downstream agents)

| Role | Authoritative file(s) |
|---|---|
| Raw human labels | `FIRST_CODER_50_FINAL_FROZEN.csv`, `BLIND_REPEAT_20_FINAL_FROZEN.csv`, `HUMAN_RECONCILED_20.csv`, `HUMAN_RECONCILIATION_EVENTS.jsonl` |
| Reliability | `HUMAN_RELIABILITY_FINAL.csv` |
| Model vs human | `MODEL_VS_RECONCILED_20.csv`, `MODEL_VS_HUMAN_FINAL_50.md`; values reproduced from the raw rows |
| Error taxonomy | `FINAL_ERROR_TAXONOMY.csv` / `.md` / `_CASES.csv` (not the `{taxblock}` section of FINAL_HUMAN_AUDIT_REPORT) |
| Local label sensitivity | `ROBUST_CORE_LOCAL_SENSITIVITY.csv` + `_DIFF.csv` |
| Decision / status | `FINAL_STATUS.json`, `FINAL_HUMAN_AUDIT_DECISION_FINAL.md`, `FINAL_SUBMISSION_READINESS_REPORT.md` → `HUMAN_AUDIT_CONVERGED / LOCAL_SENSITIVITY_CHANGED / FULL_REANALYSIS_REQUIRED`, `SUBMISSION_READY=NO` |
| Integrity anchor | `FINAL_ARTIFACT_HASH_MANIFEST.csv` (30/30 verified) |
| Segmentation sensitivity (separate) | `V9_1_SEGMENTATION_SENSITIVITY/SEGMENTATION_SENSITIVITY_FINAL_REPORT.md` + its `FINAL_STATUS.json` |

Do not cite as current: `FINAL_STATUS.md`, `HUMAN_AUDIT_STATUS.json`, `FINAL_HUMAN_AUDIT_DECISION.md`, `HUMAN_RECONCILIATION_GATE_STATUS.json`, `HUMAN_RELIABILITY_20.*`, `HUMAN_VALIDATION_FINAL_REPORT.md`, `README.md`, `HUMAN_AUDIT_50_20_PIPELINE.md`, `STARTUP_HASH_BASELINE.csv`.

---

## 8. Verdict

`V9_SOURCE_VERIFIED=PARTIAL`

Justification:
- **CONFIRMED.** The whole human-validation chain was reproduced from raw machine-readable rows, with hash anchors verified:
  - 50/20/19 counts and coder identities 1 / 2 / 3.
  - All five kappas and agreement counts.
  - Model-vs-human 14/19/9/33-of-42 and 3/7/7/10-of-18.
  - Both event hash chains (19/19 and 5/5).
  - The local-sensitivity membership change (+HUMAN_AUGMENTATION×RISK_ASSESSMENT depleted; −COORDINATION_EXECUTION×GENERAL_DECISION_PROCESS enriched; 32→32, 15E/17D, 24 count and 3 direction changes, 0 shared-direction changes).
  - The final decision. The manifest matches 30/30, and the inventory matches 1,295/1,295.
  - The authority ordering is unambiguous by chronology and content. There is no blocking contradiction among final-state artifacts; every contradiction is between a superseded checkpoint and the final set.
- **Not YES** because:
  - The 12 protected inputs that the FINAL claims rest on are NOT_RECOVERED in the package: the original 400/120 samples, the V9 source manuscript docx/pdf, the original freeze manifests and sqlite DBs.
  - The official frozen results are supported only via a reproduction (PROBABLE).
  - The sidecar core file is not shipped.
  - The legacy audit log remains UNVERIFIED (1 protected-hash mismatch).
  - The pinned `FINAL_HUMAN_AUDIT_REPORT.md` contains an unrendered `{taxblock}` defect.
  - `FINAL_ARTIFACT_HASH_MANIFEST.csv` itself has no external anchor.
- No STOP condition. The CONFIRMED set is enough to replace the "artifact pending / user-reported" status that v1.7 (128 CF-01, 131 §2/§8 E39) gave to the V9 values.
