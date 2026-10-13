# 17 — Study 1 Evidence Freeze v1 (V1.8.1)

Freeze date: 2026-10-14
Branch: `research/v1.8.1-study1-freeze-20261014`, based on `d2044161` (V1.8 source closure).

**What this freezes:** the current, defensible evidence state of Study 1, the literature layer.

**What this does not do:**
- It is not a reanalysis. No record was rerun, and no network value, taxonomy, core membership, G01–G16 or G→M assignment changed.
- It is not a FINAL tag and not a submission-readiness claim (`SUBMISSION_READY=NO`).

Hashes of every artifact this freeze depends on are in `18_STUDY1_FREEZE_HASHES.csv`.

Recomputation script: `tools/O/baseline_check.py`, run with `python -I`; output in `tools/O/baseline_check.json`. It recomputes the section A cell counts directly from the `official_*` columns of the V9 `ROBUST_CORE_LOCAL_SENSITIVITY.csv` (sha256 `e3166ee1…`).

---

## A. Primary inferential baseline (R14 frozen result; official inferential reference)

| Quantity | Value | Verification in this freeze |
|---|---|---|
| Strict analytical records | **6,499** | Manuscript v1.8 L13/L29/L443. The upstream frozen DB is NOT_RECOVERED (02 §5), so this was not recomputed. |
| Pair-eligible semantic records (both ends mapped) | **3,125** | Recomputed: the sum of `official_raw_observed` over 120 cells = 3,125 |
| Unique documents | **783** | V9 `ROBUST_CORE_LOCAL_SENSITIVITY_STATUS.json` (`official: 783`) and manuscript. Not recomputable from cell-level rows. |
| Document-level edges | **2,180** | Recomputed: the sum of `official_observed` = 2,180 |
| Cells | **10 AI families × 12 Decision families = 120** | Recomputed: 10 and 12 distinct family codes, 120 rows |
| Primary-significant cells (main null, BH q ≤ .05) | **47** (34 at q ≤ .01) | Recomputed from `official_main_q05` / `_q01` |
| Robust core (q ≤ .05 in all four methods, same direction) | **32 = 16 enriched + 16 depleted** | Recomputed from `official_core_member` / `_direction`. The promotion rule re-applied to the per-method q values gives 0 mismatches (V1.8 04 §1). |
| G01–G16 | **= the 16 official depleted core cells** (official depleted backbone) | Recomputed: exact set equality between `11_Priority_Gaps_Frozen_Export_G01_G16_v1_0_20261009.csv` and the 16 official DEPLETED core cells, with no naming differences (also matches 132, per V1.8 04 T2) |

G01–G16 (unchanged, listed for traceability):

| G | AI family × Decision family |
|---|---|
| G01 | HUMAN_AUGMENTATION × PREDICTION_DIAGNOSIS |
| G02 | PREDICTION_RISK_ESTIMATION × HUMAN_REVIEW_ACCOUNTABILITY |
| G03 | COORDINATION_EXECUTION × RISK_ASSESSMENT |
| G04 | GENERATION_SYNTHESIS × PREDICTION_DIAGNOSIS |
| G05 | EXPLANATION_ASSURANCE × ALLOCATION_PLANNING |
| G06 | EVALUATION_ASSESSMENT × PREDICTION_DIAGNOSIS |
| G07 | HUMAN_AUGMENTATION × EVALUATION_SELECTION |
| G08 | RECOMMENDATION_OPTIMIZATION × HUMAN_REVIEW_ACCOUNTABILITY |
| G09 | PREDICTION_RISK_ESTIMATION × GOVERNANCE_OVERSIGHT |
| G10 | PREDICTION_RISK_ESTIMATION × EVALUATION_SELECTION |
| G11 | EVALUATION_ASSESSMENT × ALLOCATION_PLANNING |
| G12 | PREDICTION_RISK_ESTIMATION × INFORMATION_ACQUISITION |
| G13 | EXPLANATION_ASSURANCE × PREDICTION_DIAGNOSIS |
| G14 | PREDICTION_RISK_ESTIMATION × GENERAL_DECISION_PROCESS |
| G15 | EXPLANATION_ASSURANCE × EVALUATION_SELECTION |
| G16 | COORDINATION_EXECUTION × HUMAN_REVIEW_ACCOUNTABILITY |

## B. Human audit (V9, reproduced from raw rows in V1.8)

- **First coder 50/50, blind second coder 20/20, reconciliation 19/19.** Recomputed from `FIRST_CODER_50_FINAL_FROZEN.csv`, `BLIND_REPEAT_20_FINAL_FROZEN.csv`, `HUMAN_RECONCILED_20.csv` and `HUMAN_RECONCILIATION_EVENTS.jsonl` (V1.8 03).
- **Pre-reconciliation Cohen's κ (n = 20):**

  | Dimension | κ |
  |---|---|
  | C1 evidence validity | **.5614** |
  | C2 relation | **.1798** |
  | C3 AI family | **.0476** |
  | C4 Decision family | **.1398** |
  | C5 analytical inclusion | **.3162** |

  All five reproduce `HUMAN_RELIABILITY_FINAL.csv` within 0.00004. The bootstrap CIs come from that file and were not re-run.
- **Design:** a targeted sample of 50 Robust-A records. It is not a probability sample of the 6,499 records.

## C. Local label sensitivity (V9 sidecar, re-verified in V1.8)

- **Label scope:** 50 audited records relabelled (20 with reconciled FINAL labels, 30 with first-coder labels); all other records keep model labels.
- **Core:** 32 → **32**, split **16/16 → 15/17**.
  - **+ `HUMAN_AUGMENTATION × RISK_ASSESSMENT`** (DEPLETED; document-null q .0567 → .0325)
  - **− `COORDINATION_EXECUTION × GENERAL_DECISION_PROCESS`** (ENRICHED; document-null q .0435 → .0611)
- **Other 31 core pairs:** unchanged in membership and direction.
- **G01–G16 removals: 0.** The gained depleted cell is **not** added to the G list. There is no G17; any change to the G list is a governance decision outside this freeze.
- **Not a full-corpus rerun:** `model_calls: 0`, and the sidecar generator script is NOT_RECOVERED.

## D. Interpretation (frozen status labels)

| Object | Status | Basis |
|---|---|---|
| Exact 32-core membership | **LOCALLY_SENSITIVE** | One-in/one-out at the q = .05 boundary of the document-preserving null under 50-record relabelling |
| G01–G16 depletion backbone | **LOCALLY_STABLE** | 0/16 removed under the label sidecar. Boundary caveats for G07 and G15 under the separate V9.1 segmentation sensitivity are in 14. |
| Corpus-wide human validity of labels | **NOT_ESTABLISHED** | Targeted n = 50, low agreement on C2–C4. No corpus-wide error estimate is supported. |
| Human audit | **TARGETED** | Robust-A stratum only |
| Full reanalysis | **DEFERRED** | See below |

Full-reanalysis status, using the current terminology (see `15_REANALYSIS_INPUT_GOVERNANCE.md`):

```
FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION
FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET
FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED
```

Rationale:
1. 12 of the 37 protected inputs are not recovered.
2. The local sidecar shows G01–G16 unaffected.
3. A full rerun would only add reproducibility; it cannot establish corpus-wide human-label validity.
4. The real limitation is the small targeted human sample and low model–human agreement.
5. Whether to run it later remains a researcher decision.

This is **not** `FULL_REANALYSIS_NOT_REQUIRED`.

## E. Invalid claims (must not appear in any current artifact)

- "Human validation confirmed all 32 pairs" (or the robust core).
- "Human validation confirmed the taxonomy."
- "G01–G16 are empirically proven enterprise problems."
- "Depletion = structural hole." Burt-type structural holes were not tested; the nodes here are function families, not actors.
- "Network magnitude (O, E, O/E, q) = enterprise effect size." Under 128 §5, no R14 value enters the enterprise model as a weight, coefficient, prior or threshold.

## F. Boundary to Study 2 (unchanged by this freeze)

Study 1 provides only three things to Study 2: research motivation, mechanism candidates and construct traceability.

This freeze does not modify the Enterprise v2.2 model (`42_…v2_2.md`), the VCP/VSC/DL/NEV definitions, the solver (`51_…v2_2.py`), the v2.3 schema (`62_…v2_3`) or the 620-cell empirical workbook.

The G→M assignment is unchanged. Its human construct validation (V1) is prepared, not executed, in 19–21.

## G. Freeze status

`STUDY1_EVIDENCE_FREEZE=READY` (subject to the cleanup audits 11–14 recorded in `23_V1_8_1_FINAL_STATUS.md`).
