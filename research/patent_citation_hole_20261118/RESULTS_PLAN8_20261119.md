# Results: Plan 8, when co-occurrence misjudges flow (taxonomic distance)

- **Plan:** `PREREGISTRATION_DIVERGENCE.md`, frozen in 6a35b21.
- **Code:** `src/divergence.py`.
- **Output:** `results/PLAN8_RESULTS.json`.
- **Data:** the 16,703 eligible Plan 7 pairs.
  - Level 1 (same subclass): 1,337 pairs, 13 C-gaps.
  - Level 2 (same class, different subclass): 6,547 pairs, 1,252 C-gaps.
  - Level 3 (different class): 8,819 pairs, 2,911 C-gaps.
- **Bootstrap:** 1,000 field-cluster replicates.

## Preregistered tests

**H8a: divergence Δ (flow rank minus co-occurrence rank) increases with distance. NOT SUPPORTED.**
- OLS with controls:
  - level-2 coefficient 0.050 [0.029, 0.070];
  - level-3 coefficient 0.023 [0.003, 0.046].
- The unadjusted means are not ordered:
  - level 1: −0.023 [−0.037, −0.008];
  - level 2: 0.022 [0.000, 0.042];
  - level 3: −0.013 [−0.036, 0.010].
- The rule requires both a positive level-3 coefficient and the ordering L1 < L2 < L3, so the verdict is not supported.
- Δ is highest for level 2, not level 3.

**H8b: among C-gaps, the false-gap rate is higher for level 3 than for levels 1–2. NOT SUPPORTED; the difference runs the other way.**
- False-gap rate: level 3 0.304 [0.247, 0.367]; levels 1–2 0.398 [0.311, 0.499].
- Difference −0.094 [−0.199, −0.002]: lower at level 3, with the CI excluding 0.
- Reversal rate: level 3 0.056 [0.033, 0.086]; levels 1–2 0.103 [0.060, 0.156].
- Difference −0.046 [−0.100, 0.001].

## Secondary (descriptive)

- **S1:** log OE_flow − log OE_co, for 13,716 pairs with n_ab > 0. Level-2 coefficient 1.015 [0.825, 1.215]; level-3 coefficient 1.273 [1.085, 1.473]. Among co-classified pairs, the log divergence does grow with distance. This is a different subset and scale from the preregistered Δ.
- **S2:** no controls. Level-2 coefficient 0.045 [0.025, 0.063]; level-3 coefficient 0.010 [−0.014, 0.035].
- **S3:**
  - pairs with a G16 field: mean Δ −0.114 (2,055 pairs);
  - AI × DEC pairs: mean Δ −0.137 (5 pairs);
  - 294 C-gap reversals, 0.558 of them at level 3.

## Post hoc (not preregistered; descriptive)

PPV and reversal of C-gaps, by level:

| Level | C-gaps | PPV | Reversal |
|---|---|---|---|
| 1 | 13 | 0.385 | 0.231 |
| 2 | 1,252 | 0.605 | 0.101 |
| 3 | 2,911 | 0.696 | 0.056 |

Co-occurrence gaps are least reliable between fields that the classification places close together but in separate subclasses. AI (G06N) and decision (G06Q) are such a pair: same class G06, different subclass. This reading is post hoc. Level 1 has only 13 C-gaps.

## Reading

- The preregistered taxonomy hypothesis is not supported, so the manuscript must not claim that taxonomic distance explains the disagreement.
- What can be said:
  - co-occurrence gaps are *more* trustworthy across classes than within a class;
  - false gaps and reversals concentrate in neighbouring subclasses (post hoc);
  - among pairs that are co-classified at all, the log gap between flow and co-occurrence grows with distance (S1).
