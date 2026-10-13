# 23 — V1.8.1 Final Status

**Round:** V1.8.1 repository cleanup, Study 1 evidence freeze, and V1 construct-validation readiness. Date: 2026-10-14.

**This round did not:**
- run a full reanalysis or rerun any record;
- change the taxonomy, the official 32-cell core, G01–G16, the G→M assignments, VCP/VSC/DL/NEV, the Enterprise v2.2 model, the solver or the v2.3 schema;
- add any enterprise result or human V1 result;
- modify `main`, merge, or tag.

```
REPO=https://github.com/Jimmy0307/ai-decision-ml
BRANCH=research/v1.8.1-study1-freeze-20261014
BASE_COMMIT=d2044161a30266267ac237177021ac86ac58b77c
NEW_COMMIT=(this commit; see `git log` — recorded in the push report)

V1_8_SOURCE_CLOSURE=PARTIAL
50_20_19_REPRODUCED=YES
KAPPA_REPRODUCED=YES
LOCAL_SENSITIVITY_REPRODUCED=YES
EXACT_32_CORE_STATUS=LOCALLY_SENSITIVE
G01_G16_STATUS=LOCALLY_STABLE
G01_G16_REMOVED=0
CORPUS_WIDE_HUMAN_VALIDITY=NOT_ESTABLISHED
FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION
FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET
FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED
STUDY1_EVIDENCE_FREEZE=READY
V1_HUMAN_CONSTRUCT_VALIDATION_PACKET=READY
V1_HUMAN_CONSTRUCT_VALIDATION_STATUS=READY_TO_RUN
V1_HUMAN_CONSTRUCT_VALIDATION_EXECUTED=NO
ENTERPRISE_MODEL_CHANGED=NO
DOCX_STATUS=BUILT_STRUCTURE_VERIFIED
SUBMISSION_READY=NO
```

## Audit results

| Step | Result | Artifact |
|---|---|---|
| 0 Identity gate | PASS. Remote `Jimmy0307/ai-decision-ml`; V1.8 head `d2044161…`; main `1f2e72f…`; V1.8 parent `ee750b1`; worktree clean. | — |
| 4 Full-reanalysis terminology | Triplet applied in all current artifacts (15, 17, 23, current 128/137 copies, v1.8.1 manuscript). The `NOT_REQUIRED` wording appears nowhere. V1.8's `FULL_REANALYSIS_RECOMMENDED=NO` is kept only in historical V1.8 files. | 15, 16, 17 |
| 5 Debt A: artifact 132 | 33 flag cells: 33 VERIFIED_SOURCE, 0 pending. XLSX sheet names, dimensions and all 22 formulas unchanged. | 11, `current_artifacts/132_*` |
| 6 Debt B: 128/131/133/137 | 52 line edits: 10 HISTORICAL_ENV (marked SUPERSEDED), 42 CURRENT_STATUS. One more V9.1 provenance tag was added to the 131 copy during the final grep. | 12, `current_artifacts/*` |
| 7 Debt C: legacy mislabel | 128 L15 fixed: `LEGACY_HISTORICAL_PROVENANCE — STRUCTURAL-HOLE / CITATION-NETWORK STUDY PACKAGE (NOT THE V5 DATA PACK); REAL_V5_DATA_PACK=NOT_RECOVERED`. One more historical mis-binding was found in `work_v17/adversarial_review_v17.md` L85 and recorded only. The manuscript has 0 hits. | 12 |
| 8 Debt D: 84–85/120 | No conflict. All figures were recomputed from raw rows and match. Provenance: the V9.1 segmentation sensitivity (2026-10-03), computed against the frozen primary baseline and reported in R14. R14 is the text source, not the analytic origin. Provenance tags were added to the manuscript; no number changed. | 13 |
| 9 Debt E: G07/G15 | **G07: WORDING_CONFIRMED.** It drops only in S1, only on the raw-record q (.0527). **G15: WORDING_CONFIRMED.** It drops in S1 and S2, with all four q between .08 and .14. No other G drops. Membership unchanged. | 14 |
| 10 `{taxblock}` | `FINAL_HUMAN_AUDIT_REPORT.md` = HISTORICAL_FINAL_REPORT_WITH_TEMPLATE_DEFECT (placeholder at L49). Taxonomy authority = `FINAL_ERROR_TAXONOMY.csv` / `.md`. Current citations of the placeholder: 0. | 15 |
| 11 Reanalysis input | `REANALYSIS_CANDIDATES_FROM_HUMAN_AUDIT.csv` = DO_NOT_USE_FOR_PROPAGATION. The only valid source is V1.8 04 T4 (20 reconciled + 30 first-coder labels). The propagation rule must be predeclared. | 15 |
| 12 DOCX | Built from the canonical v1.8.1 Markdown with pandoc 2.19.2. Equations, tables, headings and figures all carry over: 25/25 display equations become native Word equations (56 equations in total), 182/182 headings, 77/77 tables, 3/3 figures, 0 pandoc warnings. Word opens the file (256 pages, 56 equations) and a visual spot check of the VCP/NEV equation passed. One render-only change: a display block with a bare `\\` line break was wrapped in `aligned`; the canonical Markdown is unchanged. Styling is pandoc default, not the conference template, which is a separate packaging step. | 16 .docx, `tools/O/docx_build_report.json` |
| 13 Study 1 freeze | Baseline recomputed from the raw V9 `official_*` columns: 120 = 10×12 cells; 47 at q ≤ .05; core 32 = 16 + 16; 2,180 edges; 3,125 records; G01–G16 equal the official depleted set. The figures 6,499 and 783 are taken from the manuscript and the V9 status file; the frozen DB is NOT_RECOVERED. | 17 |
| 14 Freeze hashes | 49 ledger rows. 6 upstream canonical sources are NOT_RECOVERED, recorded with their known values and no invented hash. Enterprise v2.2 (`0249e7b9…`) and solver (`37f26a52…`) match the hashes recorded before this round. | 18 |
| 15–22 V1 packet | Protocol, codebook, master packet plus 3 per-coder workbooks; all response cells empty (80 per coder file); leakage check PASS with 0 findings; sealed commitment holds hashes only; frozen analyzer `b5628633…` returns NO_HUMAN_DATA on the blank packet, and its κ/α core matches sklearn/krippendorff (max diff 4.4e-16) on in-memory random vectors only; G04/G10/G11 are predeclared sensitivity targets and unmarked for coders. | 19, 20, 21, `V1_SEALED/`, `tools/I/` |
| 25 Final grep | 121 hits in current files, 0 substantive or unclassified. | 22 |

## Open researcher decisions (do not block packet distribution)

- **OA-2:** the derived `V1_PASS_HUMAN_C6` mapping from the new flat category set is an amendment to frozen 53B and needs researcher approval.
- **OA-3:** the meaning of `NONE`, which is mapped from 53B `OTHER`, needs confirming.
- **κ vs α:** κ is primary for two coders, as instructed. The RELIABLE/TENTATIVE/UNRESOLVED classification uses α ≥ .800 / .667. These thresholds are labelled `RESEARCH_CONVENTION` because their attribution is disputed between manuscript L3028 and 59 L164.
- **Deviation from 53B §1:** the G ID is shown to coders, as instructed. A `--mask-gid` build option exists.
- **Blinding limitation:** researcher assignments are readable in the public repository (41, 53A, 54C, the manuscript). Recruit coders who have not seen the repo.
- **Full reanalysis:** remains a researcher decision; see the triplet above and 15.
- **Remaining 137 P0 items:** V1 execution, V0 enterprise sources, ethics, parameter identification, V7, author metadata and format files.
