# 63 — Current Canonical State (2026-10-14)

```
CURRENT_MANUSCRIPT_VERSION=V1.8.5  (file 59a = v1.8.5a minimal boundary patch of 59)
CURRENT_MANUSCRIPT_MD=claude/r14_merge_v1_8_5_compute_closure/59a_MERGED_MASTER_THESIS_v1_8_5a_CANONICAL.md   sha256 bf4379a4d492d762ef2dbdd293b41c574e475b7368d210b6a129274cd61381bd
CURRENT_MANUSCRIPT_DOCX=claude/r14_merge_v1_8_5_compute_closure/59a_MERGED_MASTER_THESIS_v1_8_5a_CANONICAL.docx  (rendered from the .md; .md is the canonical text)
CURRENT_G_SET=G01–G16
COMPUTE_STATUS=CLOSED_WITH_BOUNDED_HUMAN_VALIDITY
STUDY1_PRIMARY_BASELINE=FROZEN (V5/R14; PRIMARY_BASELINE_REPLACED=NO)
CORPUS_WIDE_HUMAN_VALIDITY=NOT_ESTABLISHED
V1_STATUS=PRE-HUMAN / NOT_EXECUTED (S1 frozen; packet review: see 65)
ENTERPRISE_EMPIRICAL_STATUS=OPEN
ENTERPRISE_MODEL=UNCHANGED (v2.2; VCP/VSC/DL/NEV; solver v2.2; schema v2.3)
SUBMISSION_READY=NO
```

## Version consistency checks (orchestrator, 2026-10-14)

- The `.md` and `.docx` both exist, and the DOCX's status paragraph equals the `.md` status line.
- Number of hits in both the `.md` and the `.docx`:
  - old status strings `v1.8.3 V5 PROVENANCE CANDIDATE`, `v1.8.2 V1 PREFREEZE CANDIDATE`, `EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION`, `執行條件尚待滿足`: 0 each;
  - `CORPUS_WIDE_HUMAN_VALIDITY` / `NOT_ESTABLISHED`: present 5 times;
  - `PRIMARY_BASELINE_REPLACED = NO`: present 6 times.
- Forbidden claims have 0 hits in both: full human validation of the corpus, taxonomy fully validated, low κ solved, 50 records representing all 6,499, the sensitivity analysis replacing the primary baseline, G17. The phrase 「取代主要」 occurs only inside the negation 「不取代主要分析」.
- Primary and sensitivity numbers appear separately: primary figures in §4.1–4.5.4 and the primary tables, sensitivity figures in §4.5.5 and Table 4-9B.
- From 59 to 59a, math (25 display / 31 inline), the 182 headings and the 36 G01–G16 rows are identical. The DOCX conversion has 25 of 25 equations as native Word equations, 182 headings, 78 tables, 3 figures and 0 warnings.

## Superseded manuscript copies (kept, not deleted)

| Version | Repository path | Local history copy |
|---|---|---|
| v1.8.5 (unpatched) | `claude/r14_merge_v1_8_5_compute_closure/59_…` | — |
| v1.8.3 | `claude/r14_merge_v1_8_3_v5_recovery/41_…` | `outputs\80_HISTORY_2026\10_OCT\CURRENT_SUPERSEDED_20261014\01_MASTER_THESIS_v1_8_3\` |
| v1.8.2 | `claude/r14_merge_v1_8_2_v1_prefreeze/32_…` | `…\CURRENT_SUPERSEDED_20261014\01_MASTER_THESIS_v1_8_2\` |
