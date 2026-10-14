# 57 — Independent Compute Verification of the revised run (V1.8.5, sub-agent S)

**Script.** `tools\S\s_independent_verify.py`, run as `python -I -B`, stdlib only. It imports no pipeline, applier or comparison code.

**Output.** `tools\S\independent_verify_out.json`.

**What it re-reads:**
- the revised freeze (`…\09_ANALYTICAL_FREEZE\analytical_freeze_v2_BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1`);
- the stage 10–13 output files of run `20261014T042729Z`;
- the baseline freeze copy;
- manifest 44;
- the G csv.

It recomputes everything below from scratch.

| Check | Independent result | Status |
|---|---|---|
| Strict records | 6,499 | PASS |
| Pair-eligible: record-level flag vs eligible file | 3,107 = 3,107 | PASS |
| Unique documents (eligible) | 781 | PASS |
| Document edges recomputed as distinct (document, AI, Decision) | 2,181. The set equals `DOCUMENT_PAIR_EDGES_DEDUP.csv` | PASS |
| Cells / AI / Decision families | 120 / 10 / 12 | PASS |
| Per-cell observed O vs main-null file | 0 mismatches | PASS |
| k_a, k_d degrees | 0 mismatches | PASS |
| E = k_a·k_d / M vs `independence_expected` | max rel diff 0.0 | PASS |
| Raw-record per-cell counts vs raw file | 0 mismatches | PASS |
| Exact hypergeometric p_upper / p_lower / p_two_sided, recomputed with `math.comb` and exact fractions (dedup, M = 2,181) | max rel diff 5.3e-12 | PASS |
| Raw-record exact p, recomputed (M = 3,107) | max rel diff 7.6e-12 | PASS |
| BH re-adjustment of p_two_sided: main / exact / document-null / raw | max abs diff 0.0 / 0.0 / 0.0 / 0.0 | PASS |
| Main q ≤ .05 / ≤ .01 | 47 / 32 | recorded |
| Robust predicate re-applied from `ROBUSTNESS_COMPARISON_120.csv` (all four q ≤ .05 and one common direction) | 32 = 15 ENRICHED + 17 DEPLETED | recorded |
| Predicate set and directions vs `FINAL_ROBUST_CORE_32.csv` | identical | PASS |
| Predicate vs `FINAL_ROBUST_STATUS_MATRIX_10X12.csv` | identical | PASS |
| G01–G16 in the revised core | 16/16, all DEPLETED; removed 0, direction changed 0 | recorded |
| 50 applications: targets / matched / final values applied | 50 / 50 / 50 | PASS |
| Field-changing records | 37 | as pre-registered |
| Non-target rows changed (parsed) | 0. The raw byte check in 51 gives 6,449 / 6,449 identical | PASS |

**Not independently recomputable here:** the Monte-Carlo p-values of the main fixed-degree null and the document-preserving null. Reproducing them would mean re-implementing the RNG-dependent samplers.

What covers them instead:
- **BH:** their BH adjustment is verified.
- **Same code as the baseline:** the baseline reproduction ran this identical, path-only-patched code and got 13/13 byte-identical outputs. In revised mode the sampler code is unchanged; only guard constants changed (REVISED_GUARD_SELF_AUDIT).
- **External cross-check:** their revised values equal the V9 sidecar's values exactly, with 0 diffs (58).

```
INDEPENDENT_VERIFICATION=PASS
```
