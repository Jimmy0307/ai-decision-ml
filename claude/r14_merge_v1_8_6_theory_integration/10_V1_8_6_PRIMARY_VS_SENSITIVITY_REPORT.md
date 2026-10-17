# 10 — V1.8.6 Primary vs Sensitivity Report (R-4)

```
PRIMARY = W5 (canonical witness) — ±5% perturbation survival 162/400
W5_WIDE = SENSITIVITY / EXPANDED WITNESS ONLY — ±5% perturbation survival 367/400
PRIMARY_BASELINE_REPLACED = NO
R4_PRIMARY_162_OF_400_PRESERVED = YES
R4_W5_WIDE_367_OF_400 = SENSITIVITY_ONLY
```

## What the two numbers are

| | W5 (primary) | W5_WIDE (sensitivity) |
|---|---|---|
| Role | Canonical constructive witness for Prop D6 (the Model C build region need not be an interval) | Expanded sidecar instance with wider margins |
| Reproduces canonical v2.2 test | Yes: T-SEN-8 build sequence 1,1,1,1,0,0,0,1 exactly | No (a different instance, from red team 11) |
| Build region | [0,3) ∪ (4,∞) under 51's convention | [0,4) ∪ (7,∞) |
| ±5% joint perturbation, fixed seed, 400 draws: non-interval region survives | **162/400** | 367/400 |
| ±1% | 398/400 | — |
| Structural dependence | Both depend on a zero net BUD footprint (exact zeros) | Same |

**Source:** theory pack 04, 09, 14 §6 and 15. The witness script is deterministic (`witness_set_sha256 a68664ce…`).

## Why 162/400 stays primary

- W5 is the instance that reproduces the canonical v2.2 regression (T-SEN-8). Any primary claim about the existence result rests on that instance.
- W5_WIDE is a different instance, a different parameter vector chosen for margin. It is not the same population, the same preregistered scope or the same parameter range. Using it would not correct a defect in W5; no implementation bug was found in W5 or in the perturbation procedure.
- **The proposition itself is an existence result.** Perturbation survival measures how fragile the witness is, not whether the result holds. Neither number is an enterprise frequency or a probability that non-monotonicity occurs in practice.

## How the manuscript reports it (`01`)

- §4.9.1 (Table 4-20D) and Appendix C.10.4 report **W5 (primary): 162/400 at ±5%** and, labelled separately, **W5_WIDE (expanded sidecar sensitivity): 367/400 at ±5%**.
- The manuscript patch checks verified that 367/400 never appears without the sensitivity label and is never presented as the primary result (03, check R4).
- The unified footnote applies to both: they establish computational consistency, formal existence or counterexamples only, and are not enterprise empirical evidence.
