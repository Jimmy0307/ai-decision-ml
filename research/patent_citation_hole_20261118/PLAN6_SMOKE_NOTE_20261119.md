# Plan 6 smoke test (2 replicates): validity gate is likely to fail

**Recorded:** 2026-11-19, after a 2-replicate smoke test of `src/firm_null_degree.py` and before any full run.

## What ran

- `export` wrote `firm_model_A2_LOCAL.npz` (arrays only; not committed).
- `run --reps 2 --workers 1` reproduced the Plan 3/4 observed values exactly (T1, T2, ties), so the assertion passed.

## Gate statistics printed by the smoke run (2 replicates)

| Scheme | median ρ degree | median ρ strength | firms whose null degree is within ±20% |
|---|---|---|---|
| primary | 0.817 | 0.952 | 0.317 |
| S-tech | 0.826 | 0.956 | 0.342 |

The preregistered gate requires ρ degree ≥ 0.90 and ρ strength ≥ 0.95. On these two replicates the degree criterion fails in both schemes, by a wide margin compared with the replicate-to-replicate variation. If the full run behaves the same way, Plan 6 ends `INVALID_NULL`.

## What was not looked at

- The smoke run also wrote T1/T2 statistics for its 2 replicates.
- Those files were moved, unread, to a local `SEALED_NOT_READ` folder.
- No T1/T2 value from this null has been inspected.

## Status

- Plan 6 is unchanged.
- How to proceed is the researcher's decision. The options are:
  - run the preregistered design in full and report `INVALID_NULL`;
  - or record an amendment that changes the null **before** any T1/T2 value is read. Any such amendment would be data-informed by this gate result and is labelled as such.
- The gate threshold is not changed.
