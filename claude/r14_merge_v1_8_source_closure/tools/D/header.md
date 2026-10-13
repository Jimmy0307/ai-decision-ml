# 05 — LEGACY SOURCE BOUNDARY (`完整資料來源.zip`)

Run: V1.8 SOURCE-VERIFIED EVIDENCE CLOSURE — Phase 6 (legacy zip quarantine), sub-agent D. Date: 2026-10-14.
Scope: read-only audit of `W\03_LEGACY_FULL_SOURCE\完整資料來源\` (69 files) against the v1.7 candidate manuscript
`r14_merge_v1_7\130_MERGED_MASTER_THESIS_R14_TO_ENTERPRISE_v1_7_EVIDENCE_CONVERGED_CANDIDATE.md` (3,080 lines) and
`r14_merge_v1_7\128_CANONICAL_STATE.md`. No extracted file was modified; no code from inside W was executed.

Reproducibility (helper scripts, run with `python -I`):
- `C:\Users\user\AppData\Local\Temp\claude\C--NTUST-PAPER\b2185478-fbc8-4bee-8105-bb5557dd964b\scratchpad\v18\D\legacy_audit.py` — hashes every file, joins `01_FILE_INVENTORY.csv` (zip entry mtimes), classifies analysis family, extracts 1,403 distinctive numeric tokens from legacy text (decimals with >= 3 places, comma-grouped integers, percentages) plus the 27 legacy concept names, and greps v1.7 / 128 for them and for 37 method terms. Raw output: `...\v18\D\legacy_audit_result.json`.
- `...\v18\D\assemble.py` — builds this file from the JSON.

Source zip: `C:\NTUST_PAPER\read\generated_v2\完整資料來源.zip`, sha256 `138dbeac661fb39a0ab7f3fe84f312e332a9d8b64b5b47c399034bffd4c0d283`, 13,143,635 B, mtime 2026-05-06T15:11:55 (`00_INPUT_MANIFEST.csv`). All 69 extracted files re-hashed: 69/69 match `01_FILE_INVENTORY.csv`.

---

## 1. Summary

**The package is an earlier, separate body of work — CONFIRMED.** It is the April–May 2026 project
"AI 治理結構洞的自動化識別與優先序排列 — 一個基於大規模文獻計量的機器驅動方法" (automated identification and prioritisation of
structural holes in AI governance literature), built on a **2,003-paper** corpus with the pre-R14 `read/generated_v2` pipeline.
Its README is dated 2026-04-22 17:00:40; zip entry mtimes: 55 files 2026-04-22, 9 files 2026-05-05, 5 files 2026-05-06.

Analysis families present (all confirmed by file content, not only filenames):

1. **Structural-hole "gap_priority" ranking** of 27 AI-governance concepts (info-gap matrix, four-dimension maturity score, Tier-A/B/C = rank 1–10/11–20/21–27) with a 50,000-run Monte Carlo tier-stability test (seed 20260422; Tier-A mean retention 84.92 %, Jaccard mean 0.7452).
2. **Classical network metrics vs gap_priority** on a 27-node / 72-edge concept k-NN graph — betweenness, **Burt constraint**, bridging centrality; all Spearman rho in [-0.2552, -0.0202], none significant; 5,000-resample bootstrap CIs all include 0.
3. **Citation network + main path analysis (SPLC / SPNP)**: 2,003 papers, 1,981 resolved via Crossref/DOI (98.90 %), 714 in-corpus citation edges, 8-node main path (SPLC = SPNP); multi-path robustness 15,000 runs.
4. **PCA + factor analysis (FA)** on 34 yearly observations x 7 features: PC1 29.90 %, PC2 27.40 %, cumulative 57.30 %; FA varimax, 3 factors (Kaiser > 1).
5. **External validation** (independent OpenAlex: 27 shared concepts, rho = -0.1413, p = 0.4821) and **ablation** of gap_priority signals.
6. **Concept co-occurrence backbone** (top-30 % weight edges; hub "Decision-making Algorithms" degree 36) — 2026-05-06.
7. **Old thesis drafts** (`FINAL_THESIS_FORMAL_VERSION_2026-04-12.md` 2,507 lines; `..._Q1_CLEAN_VERSION.md`; `..._WITH_DELETION_MARKS.md`) and Q1 revision plans/progress reports (TASK1/TASK2, 2026-05-05).

Legacy internal-quality defects observed (reasons, beyond lineage, why nothing here may be merged):
- The SPLC/SPNP main path consists of computer-vision papers (AlexNet NIPS-2012 → ResNet 1512.03385 → … → Swin Transformer → 2304.08069), not AI-governance literature — the citation layer does not describe the stated corpus topic.
- `q1_upgrade_citation_multisource_mapping_2026-04-22.csv`: 209 of 2,003 rows have year > 2026 (max 2200), min year 0.
- `q1_upgrade_citation_edges_in_corpus_2026-04-22.csv`: 9 of 714 edges are self-loops (e.g. `1412_3555v1 → 1412_3555v1`).
- Inconsistent external-validation numbers inside the package: closeout summary rho = -0.1413, top-10 overlap 0.20; `visualization_dashboard_metrics_2026-04-22.csv` rho = -0.218, top-10 overlap 0.1.
- Inconsistent tier assignment: `structural_hole_marked_list_2026-04-22.md` uses 10/10/7 (MCDM and Risk_assessment = Tier-A); `Enhanced_Concept_Statistics_2026-05-06.csv` uses 6/13/8 (both = Tier-B).
- The package's own closeout states the effect evidence is weak (all bootstrap CIs include 0; independent external consistency weak).

Relationship to other lineages: the legacy thesis is not the R14 corpus (R14/v1.7 report 47,402 pages, 9,984 section spans, 26,501 candidates, 6,499 retained records, 22 function families, G01–G16); no R14 / V5 / G01–G16 figures appear in any legacy text file (incidental string hits only inside PNG bytes and bibliographic titles in the 11 MB mapping CSVs). Whether this package is the "V4 structural-hole layer" named in 128 §4 is **UNRESOLVED** (the V4 manuscript was not examined in this phase); it is at least the same structural-hole research line.

### Analysis-family file counts

{{FAMILY_TABLE}}

---

## 2. File-by-file table (69 files)

Dates: "Filename date" is the date embedded in the file name; "Zip entry mtime" is from `01_FILE_INVENTORY.csv` (local-time zip entry timestamp). Filename dates can be older than content (README notes `info_gap_matrix_2026-04-11.csv` was recomputed 2026-04-22).

{{FILE_TABLE}}

