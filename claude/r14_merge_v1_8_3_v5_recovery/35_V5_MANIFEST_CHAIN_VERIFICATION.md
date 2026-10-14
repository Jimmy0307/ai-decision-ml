# 35 — V5 production manifest-chain verification (sub-agent P, Task 1)

Date: 2026-10-14 · Mode: read-only verification; I ran no pipeline stage, null model or reanalysis.
V5 = `C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\04_V5_PRODUCTION_FREEZE\20260911_AI_DECISION_V5_PRODUCTION`
Machine-readable: `35_V5_MANIFEST_CHAIN.csv` (one row per recorded hash claim), `35_v5_manifest_chain_raw.json` (13/14 run comparisons, zips, LATEST pointers, V9.1 comparison).
Tools: `tools/P/p_task1_manifest_chain.py` (stdlib only; `python -I`).

## 0. Path relocation

Every manifest and every `LATEST_*.txt` records the original root `C:\NTUST_PAPER\outputs\20260911_AI_DECISION_V5_PRODUCTION\…`. That path no longer exists. I remapped that prefix to the current V5 root, and all 9 LATEST pointer targets exist after remapping (0/9 exist at the recorded path). This is a relocation only. No content depends on it, because every check below is by SHA-256.

| LATEST pointer | Target (remapped) | Exists |
|---|---|---|
| 07 LATEST_COMPLETION_AUDIT.txt | completion_audits\audit_20260918T115016Z | yes |
| 07 LATEST_COMPLETION_AUDIT_V2.txt | completion_audits\audit_v2_20260918T115545Z | yes |
| 08 | closure_20260918T125655Z | yes |
| 09 | analytical_freeze_v2_20260918T132206Z | yes |
| 10 | matrix_v1_20260918T132505Z | yes |
| 11 | null_model_v1_20260918T132933Z | yes |
| 12 | robustness_v1_20260918T133618Z | yes |
| 13 | results_freeze_v1_20260919T080120Z (not 075633Z) | yes |
| 14 | data_pack_v1_20260922T010012Z (not 081003Z) | yes |

## 1. Per-stage hash verification

The "Listed" column counts the file-hash claims in that stage's manifest, plus the `source_*_sha256` fields embedded in its canonical JSON. Payload or identity hashes are counted separately.

| Stage / manifest | Listed | Verified | Mismatched | Missing | Payload-only | Notes |
|---|---|---|---|---|---|---|
| 03 `V5_PRODUCTION_MANIFEST.json` | 22 | 22 | 0 | 0 | 1 (`sectioning.patterns_sha256`, not checked) | FSC definitions and taxonomy (01_FSC), 8 profile config files, 9 app binaries (`LocalCorpusWorkbench\v5_production_app`), input DB `v5_run_app5\data\workbench.sqlite` (3645aa24…), track index `v5_corpus_index.csv` (83404ea0…). The `profile_hash`, `prompt_hashes` and model digest are identity values. The prompt hashes equal the verified prompt-file hashes. |
| 06 `V5_EVIDENCE_FREEZE_REPORT.json` | 1 | 1 | 0 | 0 | – | production DB `v5_production_app\data\workbench.sqlite` = 367e588c… |
| 07 `ANALYTICAL_SCOPE_MANIFEST.json` (summary) | 3 | 3 | 0 | 0 | 2, both recomputed and matching | See §1a |
| 08 `STAGE3_RESIDUAL_CLOSURE_MANIFEST.json` | 7 | 7 | 0 | 0 | 1 (`formal_scope_sha256`; recomputed in §1a) | Stage-2 final audit V3 (91c518f7…), sidecar sqlite (cc425630…), split manifest and CSV, source DB, reconstructed scope (968e6d22…), closure canonical (cd20aab5…) |
| 09 `ANALYTICAL_FREEZE_MANIFEST_V2.json` | 5 | 5 | 0 | 0 | 1 (formal scope) | canonical 9a4e8fc2…; lineage: source DB, sidecar, reconstructed scope, stage-3 closure |
| 10 `DOCUMENT_DEDUP_MATRIX_MANIFEST.json` | 3 | 3 | 0 | 0 | – | input 9a4e8fc2… → output d816f34a… |
| 11 `NULL_MODEL_NETWORK_MANIFEST.json` | 3 | 3 | 0 | 0 | – | input d816f34a… → output 682a58f7… |
| 12 `ROBUSTNESS_SENSITIVITY_MANIFEST.json` | 5 | 5 | 0 | 0 | – | inputs d816f34a…, 682a58f7… → output 8c0441ce… |
| 13 `FINAL_RESULTS_FREEZE_MANIFEST.json` (080120Z) | 5 | 5 | 0 | 0 | – | inputs 8c0441ce…, 682a58f7… → output b1d8b5ee… |
| 13 run 075633Z (no manifest) | 1 | 1 | 0 | 0 | – | canonical's `source_robustness_sha256` = 8c0441ce… (verified) |
| 14 `MANUSCRIPT_DATA_PACK_MANIFEST.json` 20260922T010012Z (LATEST) | 74 (61 generated_files + 13 rows of 02_PROVENANCE_HASHES.csv) | **74** | 0 | 0 | – | all sizes also match |
| 14 `MANUSCRIPT_DATA_PACK_MANIFEST.json` 20260919T081003Z (superseded) | 74 | 72 | **2** | 0 | – | `26_OBSERVED_EXPECTED_RATIO_MATRIX_10X12.csv`, `33_EXACT_HYPERGEOMETRIC_RESULTS_120.csv`; see §3 |

Totals: 203 file-hash claims checked. 201 VERIFIED, 2 MISMATCH (both in the superseded 081003Z directory copy), 0 MISSING, 0 unresolved.

The two mismatches are not on a file the official core depends on. The core's lineage runs 09→10→11→12→13(080120Z)→14(010012Z), and every file in it verifies. The STOP condition is therefore not triggered.

### 1a. Stage-2 analytical scope manifest (07, 385,263 bytes; file sha256 80a953ff…)

- Contents: 6,499 strict retained / 20,002 strict excluded records; 5,774 eligible records; 8,919 slot ids (8,919 unique), 4,137 LEFT / 4,782 RIGHT; sentinels UNRESOLVED_NO_ANCHOR 8,243 / COLLISION_UNRESOLVED 676; tracks AI 7,732 / DECISION 1,187.
- Hashes it records that I verified against files: `source_db_sha256` 367e588c… (production DB), `freeze_report_sha256` faecdf67… (06 report), `definitions_sha256` 08f256af… (01_FSC).
- `scope_manifest_sha256` = f763039d… is a **payload** hash. I recomputed it as `sha256(json.dumps(manifest minus {generated_utc, scope_manifest_sha256, deterministic_hash_note}, sort_keys=True, separators=(',',':')))`, and it **matches**. Stages 08 and 09 cite this value as `formal_scope_sha256`, so that link is closed too.
- `slot_set_sha256` = 34360e58… = sha256 of the newline-joined slot ids. **Matches.**
- The manifest's file hash (80a953ff…) is the value recorded as `scope_manifest_sha256` in the Stage-2 supervisor and worker lifecycle records under `work\stage2_strict_v102\lifecycle_runs\`.

## 2. Chain links (recorded input hash = previous stage's output hash = actual file hash)

| Link | Hash | Recorded in | Status |
|---|---|---|---|
| production DB → 06 / 07 / 08 / 09 / 14 | 367e588c… | 06 report, 07, 08, 09 lineage, 14 provenance CSV | VERIFIED (file hashed: 521,801,728 B) |
| 07 formal scope → 08, 09 | f763039d… (payload) | 08, 09 | VERIFIED (payload recomputed) |
| Stage-2 sidecar → 08, 09, 14 | cc425630… | 08, 09, 14 | VERIFIED |
| Stage-2 final audit V3 → 08, 14 | 91c518f7… | 08, 14 | VERIFIED |
| reconstructed scope → 08, 09, 14 | 968e6d22… | 08, 09, 14 | VERIFIED |
| 08 output → 09 input | cd20aab5… | 08 `closure_canonical_sha256`; 09 `stage3_closure_sha256` | VERIFIED |
| 09 output → 10 input | 9a4e8fc2… | 09 `canonical_sha256`; 10 manifest + 10 canonical `source_analytical_freeze_sha256` | VERIFIED |
| 10 output → 11 input | d816f34a… | 10 `dedup_canonical_sha256`; 11 manifest + canonical | VERIFIED |
| 10 output → 12 input | d816f34a… | 12 manifest + canonical `source_matrix_sha256` | VERIFIED |
| 11 output → 12 input | 682a58f7… | 11 `null_model_sha256`; 12 manifest + canonical `source_null_sha256` | VERIFIED |
| 11 output → 13 input | 682a58f7… | 13 manifest + canonical `source_null_model_sha256` | VERIFIED |
| 12 output → 13 input | 8c0441ce… | 12 `robustness_sha256`; 13 manifest + canonical (both runs) | VERIFIED |
| 13 output → 14 input | b1d8b5ee… | 13 `results_freeze_sha256`; 14 raw_source_artifacts + 02_PROVENANCE_HASHES | VERIFIED |
| definitions → 03, 07, 14 | 08f256af… | 03, 07, 14 | VERIFIED |
| 06 report → 07, 14 | faecdf67… | 07, 14 | VERIFIED |

**15/15 chain links verified. 0 broken.**

Coverage gap: the stage manifests hash only each stage's canonical JSON, not its CSV side outputs. The analytical-freeze record, side, eligible and excluded CSVs, and `DOCUMENT_PAIR_EDGES_DEDUP.csv`, are therefore not manifest-hashed. They are corroborated three other ways:

- Record and edge sets equal the hash-verified canonical JSONs. The 6,499 records match on document, families and statuses, and the 2,180 edges match exactly (Task 2 / 36).
- The strict record set equals the hash-verified production DB.
- They are byte-identical to the independent V9.1 copies (§4).

The 14 (010012Z) data-pack CSVs are all manifest-hashed.

## 3. The two 13 runs and the two 14 data packs

**13: 075633Z vs 080120Z (LATEST).** Neither run has a written note explaining the rerun. The canonical and the LATEST pointer show:

- Both runs use the same input, `source_robustness_sha256` = 8c0441ce….
- Both contain the same 32 cells with the same directions (16+16). Every column shared by the two `FINAL_ROBUST_CORE_32.csv` files is identical in all 32 rows.
- 075633Z is an incomplete earlier emission. It has no MANIFEST, no SUMMARY and no `FINAL_ROBUST_STATUS_MATRIX_10X12.csv`. Its canonical uses the keys `enriched_count`/`depleted_count`, carries per-cell `structurally_robust`/`full_sensitivity_robust` flags, and has no null-model source hash.
- 080120Z adds `promotion_rule` (q ≤ .05 and the same direction under the main Monte Carlo test, the exact hypergeometric test, the document-preserving null and the raw-record test), `source_null_model_sha256`, an `observed_minus_expected` column, the manifest, the summary and the status matrix.
- All 10 files differ in bytes between the runs (formatting and schema), not in results. 080120Z is the run that 14 consumes.

**14: 081003Z (superseded) vs 010012Z (LATEST).** 57 of 62 files are byte-identical. The other 5:

- `00_MASTER_SUMMARY.json` and `README_DATA_DICTIONARY.md` differ only in their generated-UTC lines.
- `MANUSCRIPT_DATA_PACK_MANIFEST.json` differs in `generated_utc`, `output_dir` and the hashes of those two files. Both manifests record the **same** hashes for `26_*` and `33_*`: 74e48c12… and 8538fc82…, which are the stage-11 and stage-12 originals.
- `26_OBSERVED_EXPECTED_RATIO_MATRIX_10X12.csv` and `33_EXACT_HYPERGEOMETRIC_RESULTS_120.csv`: the copies in the 081003Z **directory** were rewritten on 2026-09-20 17:53 and 18:23 local time, after the pack was built. The pattern looks like a spreadsheet re-save: `0.0`→`0`, `True`→`TRUE`, about 10 significant digits, and in 26 the size went from 1,609 to 1,577 B.
  - 26 is value-identical to the original (max diff 0).
  - 33 is value-equivalent: categorical values equal, max relative diff 5.0e-8 from precision truncation.
  - The 081003Z **zip** still holds the original bytes for both files (74e48c12… / 8538fc82…, matching the manifest).
- The 010012Z pack was regenerated on 2026-09-22. Its directory, its zip, the stage files and its manifest all agree, with 74/74 verified.

| Zip | sha256 | Bytes |
|---|---|---|
| `AI_DECISION_V5_MANUSCRIPT_DATA_PACK_20260919T081003Z.zip` | fac00723…5bbc | 1,519,909 |
| `AI_DECISION_V5_MANUSCRIPT_DATA_PACK_20260922T010012Z.zip` | fdf7cd89…9575 | 1,519,908 (all members equal to the directory files) |

## 4. V5 vs V9.1 `_baseline_reproduction`

`W\02_V9_HUMAN_VALIDATION\20260929_V9_HUMAN_VALIDATION\V9_1_SEGMENTATION_SENSITIVITY\_baseline_reproduction` contains 56 files:

- **43 of 43 data and canonical outputs are byte-identical** to V5 by SHA-256: 09 ×7, 10 ×9, 11 ×10, 12 ×8, 13 ×9. This includes the 9 stage-13 outputs, which match the 080120Z files.
- The 4 manifests (10, 11, 12, 13) differ in bytes only in `generated_utc` and absolute paths. I flattened them and compared every other field: there are 0 non-path, non-time differences.
- The 5 LATEST pointers point to V9.1 paths.
- The 4 scripts under `work\stage2_strict_v102\*_ACCEPTED.py` differ from the V5 `work\` versions. They are patched copies, which I did not execute.

So the 2026-10-03 V9.1 rerun of stages 10–13 reproduced the V5 outputs bit for bit.

## 5. Declared status (V5's own files)

- `06_STATUS\V5_EVIDENCE_FREEZE_REPORT.json` (2026-09-14) declares verdict `V5_EVIDENCE_CORPUS_FROZEN`: 2,118 documents, 26,501 candidates, 26,501 coded, 0 pending, strict 6,499 + excluded 20,002, 11/11 checks PASS, DB 367e588c….
- The stage verdicts after it: `STAGE3_RESIDUAL_CLOSURE_ACCEPTED` → `ANALYTICAL_FREEZE_ACCEPTED` → `DOCUMENT_DEDUP_10X12_MATRIX_ACCEPTED` → `NULL_MODEL_NETWORK_ANALYSIS_ACCEPTED` → `ROBUSTNESS_SENSITIVITY_ACCEPTED` → `FINAL_RESULTS_FREEZE_ACCEPTED` → `MANUSCRIPT_DATA_PACK_ACCEPTED`. Every manifest `checks` block is all-true, and every error list is empty.
- `FINAL_STATUS.md` (mtime 2026-09-11 05:27) is **stale**. It still reads `V5_QWEN_PRODUCTION_CONFIRMED_RUNNING`, with G8 `V5_EVIDENCE_CORPUS_FROZEN` "blocked only by run duration". Later artifacts supersede it, and it was never updated. It should not be cited as the current status.

## 6. Verdict

- Manifest chain 03/06/07→08→09→10→11→12→13(080120Z)→14(010012Z): **VERIFIED**. All file hashes match, all 15 links hold, and the formal-scope payload hashes recompute.
- The only anomaly is that two directory files in the superseded pack 081003Z were re-saved by a spreadsheet tool after packing. They are value-equivalent, the zip of that pack is intact, and the pack is not on the LATEST path. Recommended handling: record it as a superseded-pack anomaly, cite only 010012Z, and leave the files untouched.
- Recommended provenance status for the V5 baseline chain: **CONFIRMED** (full SHA-256 and manifest chain verified).
