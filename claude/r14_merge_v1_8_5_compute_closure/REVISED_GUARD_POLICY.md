# REVISED_GUARD_POLICY — dual-mode guards for the V1.8.5 audited-label reanalysis (sub-agent S)

Date: 2026-10-14. Revised run timestamp: `20261014T042729Z`. Approved by the researcher, as relayed by the coordinator: Phase B under the DUAL-MODE GUARD policy.

## Mode A — baseline reproduction (closed, untouched)

- **Code:** `WORK\code_baseline_20261014T041645Z\patched\`. It carries path-only edits (50) and all original hard-coded guards.
- **Result:** 13/13 outputs byte-identical (47/48). This is canonical evidence and is not modified or re-run.

## Mode B — revised audited-label reanalysis

- **Code:** `WORK\code_revised_20261014T042729Z\`, derived **from the baseline patched copy**. It contains:
  - `from_baseline\`: byte copies of the 4 baseline-patched scripts;
  - `revised\`: the scripts that run;
  - `diffs\`: revised vs baseline-patched.
- **Output:** `CC\revised_audited_label_analysis\20261014T042729Z\`.

### Guard classes

| Class | Rule in revised mode |
|---|---|
| **STRUCTURAL_INVARIANT** | Hard-fail and unchanged. Covers: 10 AI families, 12 Decision families, 120 cells, schema, unique keys, no duplicate joins, propagation targets = 50, matched = 50, unauthorized replacement = 0, statistical-method identity (no edit to any computation), historical seeds and replicates (20260918 / 10,000; 20260919 / 5,000; burn-in 20/edge; thinning 2/edge), V1 S1 blobs unchanged, Enterprise model blobs unchanged, and strict-record population unchanged (6,499 records / 1,104 documents; the rule touches no strict-filter field). |
| **LINEAGE_REPINNED** | Lineage and stage-handoff guards only: upstream input SHA-256, previous-stage output SHA-256, pair-eligible count, pair-excluded count, unique-document count, document-edge count (M), raw-record M. A new value is pinned only if three conditions hold: (1) it is taken from the previous stage's actual revised output (file sha or that stage's manifest), (2) it is recounted by `tools\S\s_independent_recount.py`, which is stdlib-only and imports no pipeline code, and (3) both agree. Otherwise STOP. |
| **OBSERVED_RESULT** | A scientific, to-be-observed result is never an abort constant. Stage 13's `robust_input_count_exact`, `final_core_count_exact`, `robust_keys_unique` and `partition_exact` all compare against `EXPECTED_ROBUST_CORE = 32`. They stay computed and recorded in the stage-13 manifest `checks`, but they are excluded from the verdict through `OBSERVED_RESULT_CHECKS`. Results are compared after computation in 52–55. No 47 / 16 / 16 / G-list / membership / direction constant exists in stages 10–12, as verified by grep. |

**Structural replacements in stage 13.** Three non-blocking OBSERVED_RESULT checks also enforced a structural property implicitly: key uniqueness, partition completeness and the join being complete. In their place, the same structural property is asserted **without a preset count**:
- `robust_keys_unique_structural`: `len(robust_core_keys) == len(robust_rows)`;
- `partition_complete_structural`: `len(enriched) + len(depleted) == len(final_rows)`;
- `final_core_matches_robust_input_structural`: `len(final_rows) == len(robust_rows)`.

These are hard-fail.

### Stage-by-stage re-pinning sequence

Each step runs only after the previous one has passed.

1. Apply the 50 substitutions with the pinned `tools\S\s_apply_propagation.py` (sha `02d141ac…bfee`, manifest 44 `fbc043e8…531a`) to a copy of the baseline freeze. The result goes to `CC\…\20261014T042729Z\09_ANALYTICAL_FREEZE\analytical_freeze_v2_BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1\`. Then run the independent application audit (51).
2. Independently recount the revised freeze: canonical sha, eligible rows, excluded rows and eligible unique documents. Compare with the applier report. If they agree, **pin the stage-10 guards** and run stage 10.
3. Independently recount stage 10: canonical sha vs the manifest `dedup_canonical_sha256`; M from the edges file, from a recount from freeze rows, and from the manifest. If they agree, **pin the stage-11 guards** and run stage 11.
4. Independently recount stage 11: null canonical sha vs the manifest `null_model_sha256`, plus 120 rows. With step 3's M, raw M and documents, **pin the stage-12 guards** and run stage 12.
5. Independently recount stage 12: robustness canonical sha vs the manifest `robustness_sha256`. **Pin the stage-13 guards**, apply the OBSERVED_RESULT conversion and run stage 13.

### Permitted hunk types in the revised code diff

- PATH: run root, freeze root.
- LINEAGE_REPIN: hash literal, handoff count literal.
- OBSERVED_RESULT_PLUMBING: the `OBSERVED_RESULT_CHECKS` constant, the verdict filter and the 3 structural replacement checks.

Any hunk that touches a computation, filter, taxonomy, seed, replicate count, threshold, BH, null model, robust predicate or direction logic is a STOP. Self-audit result: `REVISED_GUARD_SELF_AUDIT.md`. Values: `REVISED_GUARD_DIFF.csv`.
