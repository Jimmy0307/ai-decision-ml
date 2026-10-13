# 07 — Full Reanalysis Decision Memo (V1.8 Source Closure, Phase 8)

Date: 2026-10-14 | Status: **DECISION MEMO ONLY — full reanalysis NOT executed in this round** (`FULL_REANALYSIS_EXECUTED=NO`).
Inputs: `02_V9_AUTHORITY_MAP.md`, `03_HUMAN_AUDIT_REPRODUCTION.md`, `04_LOCAL_SENSITIVITY_REPRODUCTION.md` (all this run).

---

## 1. Trigger

The V9 package's authoritative status (`FINAL_STATUS.json`, verified 2026-10-03T12:23:44Z) is
`HUMAN_AUDIT_CONVERGED / LOCAL_SENSITIVITY_CHANGED / FULL_REANALYSIS_REQUIRED`, with
`full_reanalysis_requires_researcher_approval = true` and `SUBMISSION_READY = NO`.

The trigger is the local audited-record sidecar (`ROBUST_CORE_LOCAL_SENSITIVITY.csv`, sha256 `e3166ee1…`). This run re-verified it from the CSV rows:

- **Core size:** 32 → 32. Membership changed by one in and one out (Jaccard 31/33).
  - **Gained:** `HUMAN_AUGMENTATION × RISK_ASSESSMENT`, DEPLETED (document-null q .0567 → .0325).
  - **Lost:** `COORDINATION_EXECUTION × GENERAL_DECISION_PROCESS`, ENRICHED (document-null q .0435 → .0611).
- **Enriched/depleted split:** 16/16 → 15/17. The other 31 pairs are unchanged in membership and direction.
- **G01–G16:** none removed. All 16 remain DEPLETED core members.
- **Corpus deltas:** pair-eligible records 3,125 → 3,107; document edges 2,180 → 2,181; main observed counts changed in 24/120 cells; main direction flipped in 3/120 non-core cells (q = 1.0).

Both changes are boundary effects at the q = .05 promotion line in the document-preserving null. Neither cell's own observed count changed.

## 2. Exact labels to propagate

Source: `04_LOCAL_SENSITIVITY_REPRODUCTION.md` §4 and table **T4**. These are the 50 audited records, each with its model label → human label.

- **Which human label is used:**
  - The 20 blind-subset records use the reconciled FINAL labels (`HUMAN_RECONCILED_20.csv`, sha256 `4b7ceac2…`).
  - The other 30 records use first-coder labels (`FIRST_CODER_50_FINAL_FROZEN.csv`, sha256 `dd332dd8…`).
- **Fields:** C5 analytical inclusion, C3 AI functional family and C4 Decision functional family. C2 relation type is propagated only if the pipeline's eligibility rule uses it.
- **Volume:** 46/50 records have at least one changed field, for 91 field changes in total. Human C5 gives INCLUDE 30, EXCLUDE 13 and UNCERTAIN 7.
- **Do NOT use `REANALYSIS_CANDIDATES_FROM_HUMAN_AUDIT.csv` (44 rows) as the propagation list.** It uses first-coder labels throughout, and 18 of the 20 reconciled records carry different FINAL labels (T5).
- **Must be predeclared before any rerun, because it is UNRESOLVED from the package:** how UNCERTAIN, AMBIGUOUS and UNMAPPED human labels map to pair eligibility. None of five plausible rules reproduces the sidecar's −18 pair-eligible delta.

## 3. Affected pipeline stages

1. Strict-record label table: replace labels for the 50 records only. The remaining 6,449 strict records stay model-labelled.
2. Pair-eligibility / fully-mapped record frame (3,125).
3. Document-level edge aggregation (2,180).
4. 120-cell AI-family × Decision-family O/E with four null methods: main (10,000 reps, seed 20260918), exact, document-preserving (5,000 reps, seed 20260919) and raw-record. Then BH within each method.
5. Robust-core promotion (q ≤ .05 in all four methods, same direction) → 32-cell core and G list.
6. Downstream only if the G list changes: the §3.9 G→M translation, the V1 human blind-coding packets, and Chapter 4 tables 9–10 and the G01–G16 table.
7. Not affected: the enterprise model (06 v2.2), solver 51, the VCP/VSC/DL/NEV definitions, the empirical schema v2.3, and Study 2 equations. Per 128 §5, no R14 O/E/q value enters the enterprise model.

## 4. Required frozen hashes (pre-run gate)

| Item | SHA-256 | Status this run |
|---|---|---|
| Official final core (R14) | `a43b4b5897bb8b1dabfe251aa52b95da8f35b6951c98ada7c92663291770bd50` | PROBABLE. Present only as a byte-identical reproduction inside `V9_1_SEGMENTATION_SENSITIVITY/_baseline_reproduction`; the original freeze file is not in the package. |
| Sidecar core | `4e412a07af1f5c9e2f304408875fc1fc47018c9ff501a17dee437bea880e95a0` | NOT SHIPPED. Membership confirmed from the CSV. |
| `FIRST_CODER_50_FINAL_FROZEN.csv` | `dd332dd8cfecf7dde9a29d32bca654b7c04c49f499c3e6213cd4d9a2ed157400` | VERIFIED |
| `HUMAN_RECONCILED_20.csv` | `4b7ceac2c8c8bf2912ea542d88a1b887a42ed450aa248dce371525c25bb5bda0` | VERIFIED |
| `ROBUST_CORE_LOCAL_SENSITIVITY.csv` | `e3166ee183e18f340c539b983108e2c972d18b916672a62510a25638db8b5b59` | VERIFIED (manifest) |
| G01–G16 frozen list (`r14/04_G01_G16_FROZEN.csv`) | `ace53a780434c309…` (16-char prefix from 128) | Not in this run's packages. Pair names match 132 exactly. |
| Frozen strict-record DB / freeze manifests | listed in `PROTECTED_ARTIFACTS_BASELINE_20261003.csv` | **12/37 protected inputs NOT in any package** (02 §5) |

**Gate:** a rerun may start only after the missing protected inputs are restored and hash-matched. That includes the strict-record sqlite, the freeze manifests and the original core file.

## 5. Rollback plan

- Run into a new dated directory, e.g. `outputs\YYYYMMDD_R14_HUMAN_LABEL_REANALYSIS_v1\`. Never write into R14, V5, V9 or this V1.8 directory.
- First reproduce the 13 hash-pinned official outputs byte-for-byte with the uncorrected labels, as the V9 sidecar claims it did. If that fails, abort.
- The official frozen core stays the manuscript's inferential baseline until the researcher explicitly adopts the new result. Rollback means not adopting it: no file is overwritten, so nothing needs to be restored.

## 6. Expected downstream impact

- **G01–G16:** expected unchanged. The sidecar uses the same 50 labels and removes no G, but three cells sit near the boundary: G07 (q .0405), G14 (.0298) and G16 (.0223).
- **Core membership:** expected to reproduce the sidecar (+1 depleted, −1 enriched, 15/17). A different result would indicate that the sidecar's undocumented eligibility rule differs.
- **Study 2:** no impact while G01–G16 stand. Adding `HUMAN_AUGMENTATION × RISK_ASSESSMENT` would create a 17th depleted pair. Whether it enters the G list is a G-list governance decision, not an automatic consequence.
- **What a rerun cannot fix:** the human sample is 50 targeted Robust-A records. Model–human agreement there is low (relation 14/50, AI family 19/50, Decision family 9/50, inclusion 33/42). Propagating 50 labels into a 3,125-record model-labelled frame yields a mixed-source corpus. It does not correct label error corpus-wide, and it does not support a corpus-wide error estimate (`REANALYSIS_PROPOSAL.md`, Safeguards).

## 7. Acceptance criteria (for a future rerun)

1. The protected inputs are restored and hash-matched, and the uncorrected baseline reproduces all 13 pinned outputs byte-for-byte.
2. The propagation rule (UNCERTAIN, AMBIGUOUS, UNMAPPED, C2 usage) is predeclared and hash-committed before execution.
3. The label input is exactly T4 (reconciled for 20 records, first coder for 30), with its sha256 recorded.
4. Same seeds, reps, null methods, BH scope and promotion rule as R14, so there is no method drift.
5. The generating script ships with its outputs. The current sidecar generator is NOT_RECOVERED, which is a reproducibility gap in itself.
6. The output reports a full diff against the official core and G01–G16. Any G change triggers the §3.9 / V1 downstream redo, which stays out of scope until approved.

## 8. Recommendation

**RECOMMEND_FULL_REANALYSIS_BEFORE_V1=NO**

Rationale:

- **A rerun is not executable now.** 12 of the 37 protected inputs, including the frozen strict-record DB, are missing from every package (acceptance criterion 1 fails).
- **The expected result is already known at the level that matters.** A rerun with the same 50 labels is expected to reproduce the sidecar. The sidecar already shows G01–G16 intact and Study 2 unaffected, so it would add reproducibility but not new information.
- **A rerun does not address the real validity limitation.** That limitation is low model–human agreement on a 50-record targeted sample. A properly scoped, larger human audit is the remedy, and that belongs in v2, not v1.
- **The honest v1 position is fully supported by verified sources.** The manuscript can report the frozen 32-cell core as the inferential baseline, the label-replacement sidecar as a local sensitivity (15/17, +1/−1, G01–G16 intact), and the exact-membership label sensitivity as a stated limitation.

Conditions attached to NO:

- **(a) No overclaiming.** The manuscript must not state or imply that human validation confirmed the 32-cell membership.
- **(b) Package status reported faithfully.** The V9 package's own `FULL_REANALYSIS_REQUIRED` status must be stated as an open researcher decision, not as resolved.
- **(c) Researcher choice.** If the researcher prefers to rerun before submission, §4–§7 define the gate. This memo is advisory: the package records the decision as requiring researcher approval.
