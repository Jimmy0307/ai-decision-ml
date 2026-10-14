# 60 — Compute Closure Forensic Audit (V1.8.4 → V1.8.5)

**Auditor:** orchestrator. This audit is independent of the sub-agent's own checks (`57`).

**Script:** `tools/O/forensic_audit_v185.py`, run with `python -I`. It re-reads every file from disk and imports nothing from the pipeline or the sub-agent tools.

**Raw result:** `60_COMPUTE_CLOSURE_FORENSIC_AUDIT.json`.

| # | Check | Evidence (recomputed here) | Result |
|---|---|---|---|
| 1 | Baseline reproduction 13/13 | For all 13 outputs in `46`, the reproduced file's SHA-256 equals the historical pin and also equals the current V5 original. | **PASS 13/13 byte-identical** |
| 2 | Hashes / lineage | Baseline mode kept every original guard and needed path-only patches (`50`). Revised mode re-pinned 13 lineage guards, each confirmed by an independent recount (`REVISED_GUARD_DIFF.csv`, `REVISED_GUARD_SELF_AUDIT.md`). | **PASS** |
| 3 | Propagation exactly 50 | `44` has 50 rows and 50 unique record IDs: RECONCILED_FINAL 20, FIRST_CODER 30. | **PASS** |
| 4 | No unauthorized replacement | The baseline and revised record-level freezes have the same 6,499 keys. 0 non-target rows changed; 37 target rows changed, matching the preregistered field-changing count. | **PASS** |
| 5 | All 120 cells rerun | `52` has 120 rows with 120 unique cells. | **PASS** |
| 6 | Null models rerun | Stage 11: 12 of 12 output files regenerated, and they differ from the baseline because the revised inputs differ. Stage 12 (exact, document-preserving and raw-record): 10 of 10 regenerated. The historical seeds are kept (`49b`). | **PASS** |
| 7 | BH rerun | Recomputed independently in `57`, with a maximum difference of 0 across the four methods. | **PASS** |
| 8 | Robust predicate rerun | Stage 13: 11 of 11 regenerated. Revised core = 32 (15 enriched / 17 depleted); SHA-256 `4e412a07…`. | **PASS** |
| 9 | G01–G16 audit | All 16 G cells are DEPLETED in the baseline. In the revised run, 0 were removed and 0 changed direction. | **PASS (Case A)** |
| 10 | Core diff | Gained: `HUMAN_AUGMENTATION × RISK_ASSESSMENT` (depleted). Lost: `COORDINATION_EXECUTION × GENERAL_DECISION_PROCESS` (enriched). Shared cells with a direction change: 0. | recorded |
| 11 | Revised globals | 3,107 pair-eligible records, 781 documents, 2,181 edges | recorded |
| 12 | V1 S1 unchanged | The git blobs of the V1.8.2 folder and the enterprise files match the pre-run snapshot exactly, and the working tree is clean for those paths. | **PASS (V1_S1_HASH_CHANGED=NO)** |
| 13 | Enterprise unchanged | Same blob comparison: `42_…v2_2.md`, `51_…v2_2.py`, `62_…v2_3`, `65_…v2_3.py`. | **PASS (ENTERPRISE_MODEL_CHANGED=NO)** |
| 14 | Frozen outputs untouched | V5 has 1,217 files now versus 1,217 in the pre-run snapshot, with 0 changed or missing. Inputs were read only from verified copies in WORK. | **PASS** |

**Limits, stated rather than hidden:**
- **Monte Carlo p-values cannot be recomputed independently** without rerunning the sampler. Their validity rests on three things: the 13/13 byte-identical baseline (same sampler code, same seeds), the unchanged statistical code in revised mode (self-audit: 0 statistical hunks), and the exact match with the 2026-10-03 V9 sidecar (`58`).
- **Human validity is bounded:** only 50 targeted records carry human labels, so CORPUS_WIDE_HUMAN_VALIDITY remains NOT_ESTABLISHED.

**Verdict:** `COMPUTATIONAL_VALIDATION_STATUS=CLOSED_WITH_BOUNDED_HUMAN_VALIDITY`
