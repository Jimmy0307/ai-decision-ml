# 62 — G-Set Final Researcher Decision (2026-10-14)

Recorded by the orchestrator on the researcher's instruction in the V1.8.5 finalization round.

```
FORMAL_G_SET=G01–G16
ADD_SENSITIVITY_EMERGENT_CELL_TO_G_SET=NO
RENUMBER_G_SET=NO
HUMAN_AUGMENTATION × RISK_ASSESSMENT=SENSITIVITY_EMERGENT_DEPLETED_CELL
REPORT_IN_RESULTS=YES
REPORT_IN_DISCUSSION=YES
REPORT_AS_FUTURE_RESEARCH_CANDIDATE=YES
```

## Rationale

1. The primary frozen baseline (V5/R14) is not replaced by the sensitivity analysis (`PRIMARY_BASELINE_REPLACED=NO`).
2. The G set must not be expanded after the fact. G01–G16 were defined before the sensitivity analysis existed.
3. A member that appears only in the sensitivity analysis must be reported transparently, but it is not a G.
4. The full audited-label reanalysis confirmed G01–G16: 16 of 16 retained, 0 direction changes (55, 57, 60).

## Evidence for the classified cell

`HUMAN_AUGMENTATION × RISK_ASSESSMENT`:

| Analysis | Robust-core status | Document-preserving null q |
|---|---|---:|
| Primary (frozen) | Not robust; fails the document-preserving null | .0567 |
| Audited-label sensitivity | Robust, DEPLETED | .0325 |

Sources: `52_ALL_120_CELLS_BASELINE_VS_REVISED.csv`, `54_ROBUST_CORE_MEMBERSHIP_DIFF.csv`.

## Where it is reported in the manuscript (v1.8.5a, file 59a)

| Required placement | Section |
|---|---|
| Results | §4.5.5, including Table 4-9B |
| Discussion | §5.4.2 |
| Future-research candidate | §5.9, added by the minimal patch 59a; see `59a_PATCH_DIFF.md` |
| Not added to G01–G16 | §3.8.2; §5.9 says the same |

Its label in the text is 敏感度浮現格 (SENSITIVITY_EMERGENT_DEPLETED_CELL). It is never called G17.

## What this decision does not change

The following are unchanged:
- G numbering and the G→M assignments (Tables 3-4/3-4A);
- the V1 packet and the S1 freeze;
- Study 2 and the Enterprise model.
