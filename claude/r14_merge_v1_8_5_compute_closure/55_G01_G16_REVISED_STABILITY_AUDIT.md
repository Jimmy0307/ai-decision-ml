# 55 — G01–G16 Revised Stability Audit (V1.8.5, sub-agent S)

**Inputs:**
- G list: `11_Priority_Gaps_Frozen_Export_G01_G16_v1_0_20261009.csv` (sha256 `76a2a00c…209d`, WORK copy).
- Baseline: the reproduced official core `a43b4b58…`.
- Revised: core `4e412a07…`.

The robust predicate (q ≤ .05 and the same direction in main, exact, document-null and raw) was also re-applied independently from the q and direction columns (57). It agrees.

| G | AI × Decision | Baseline robust | Revised robust | Baseline dir | Revised dir | O base → rev | doc-null q base → rev | Revised main / exact / raw q |
|---|---|---|---|---|---|---|---|---|
| G01 | HUMAN_AUGMENTATION × PREDICTION_DIAGNOSIS | YES | YES | DEPLETED | DEPLETED | 3 → 3 | .0024 → .0022 | .0009 / <.0001 / <.0001 |
| G02 | PREDICTION_RISK_ESTIMATION × HUMAN_REVIEW_ACCOUNTABILITY | YES | YES | DEPLETED | DEPLETED | 6 → 7 | .0024 → .0022 | .0009 / <.0001 / <.0001 |
| G03 | COORDINATION_EXECUTION × RISK_ASSESSMENT | YES | YES | DEPLETED | DEPLETED | 3 → 3 | .0024 → .0022 | .0009 / .0001 / <.0001 |
| G04 | GENERATION_SYNTHESIS × PREDICTION_DIAGNOSIS | YES | YES | DEPLETED | DEPLETED | 7 → 7 | .0042 → .0022 | .0009 / <.0001 / <.0001 |
| G05 | EXPLANATION_ASSURANCE × ALLOCATION_PLANNING | YES | YES | DEPLETED | DEPLETED | 7 → 7 | .0024 → .0022 | .0009 / <.0001 / <.0001 |
| G06 | EVALUATION_ASSESSMENT × PREDICTION_DIAGNOSIS | YES | YES | DEPLETED | DEPLETED | 9 → 10 | .0024 → .0022 | .0009 / <.0001 / <.0001 |
| G07 | HUMAN_AUGMENTATION × EVALUATION_SELECTION | YES | YES | DEPLETED | DEPLETED | 2 → 2 | .0304 → .0405 | .0153 / .0146 / .0275 |
| G08 | RECOMMENDATION_OPTIMIZATION × HUMAN_REVIEW_ACCOUNTABILITY | YES | YES | DEPLETED | DEPLETED | 8 → 8 | .0024 → .0022 | .0009 / <.0001 / <.0001 |
| G09 | PREDICTION_RISK_ESTIMATION × GOVERNANCE_OVERSIGHT | YES | YES | DEPLETED | DEPLETED | 26 → 25 | .0024 → .0022 | .0009 / <.0001 / <.0001 |
| G10 | PREDICTION_RISK_ESTIMATION × EVALUATION_SELECTION | YES | YES | DEPLETED | DEPLETED | 8 → 9 | .0058 → .0042 | .0009 / <.0001 / <.0001 |
| G11 | EVALUATION_ASSESSMENT × ALLOCATION_PLANNING | YES | YES | DEPLETED | DEPLETED | 12 → 12 | .0024 → .0022 | .0009 / <.0001 / <.0001 |
| G12 | PREDICTION_RISK_ESTIMATION × INFORMATION_ACQUISITION | YES | YES | DEPLETED | DEPLETED | 21 → 21 | .0024 → .0022 | .0009 / <.0001 / <.0001 |
| G13 | EXPLANATION_ASSURANCE × PREDICTION_DIAGNOSIS | YES | YES | DEPLETED | DEPLETED | 15 → 14 | .0024 → .0022 | .0009 / <.0001 / <.0001 |
| G14 | PREDICTION_RISK_ESTIMATION × GENERAL_DECISION_PROCESS | YES | YES | DEPLETED | DEPLETED | 8 → 10 | .0089 → .0298 | .0177 / .0149 / <.0001 |
| G15 | EXPLANATION_ASSURANCE × EVALUATION_SELECTION | YES | YES | DEPLETED | DEPLETED | 7 → 7 | .0387 → .0178 | .0267 / .0237 / .0145 |
| G16 | COORDINATION_EXECUTION × HUMAN_REVIEW_ACCOUNTABILITY | YES | YES | DEPLETED | DEPLETED | 10 → 10 | .0137 → .0223 | .0216 / .0159 / .0086 |

**Boundary cells.** These are the cells closest to the q = .05 line in the revised document-preserving null:
- G07 (.0405);
- G14 (.0298);
- G16 (.0223).

**Gained cell vs the G list.** The gained depleted cell `HUMAN_AUGMENTATION × RISK_ASSESSMENT` is **not** a G cell. G-list membership was not changed: there is no G17. Whether to add it is a separate governance decision, outside this audit.

Because no G cell was removed and no G direction changed, no researcher decision memo (56) is required and none was written.

```
G01_G16_BASELINE_ROBUST=16/16 DEPLETED
G01_G16_REVISED_ROBUST=16/16 DEPLETED
G_BACKBONE_CONFLICT=NONE
G01_G16_REMOVED=0
G01_G16_DIRECTION_CHANGED=0
```
