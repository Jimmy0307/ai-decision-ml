# 13 — Erratum CANDIDATE for canonical 42 v2.2: Lemma E′ pessimistic proof sentence (§12.4, l.476)

**Status:** ERRATUM CANDIDATE for researcher review. Recorded 2026-10-15 by agent T7 from finding A5 / §2.7 of the red-team report `11_Q1_THEORY_UPGRADE_REVIEWER_2_REDTEAM.md`. **42 is NOT modified, and neither is 51.** Whether, when and how to correct 42 (for example at the next version bump) is a researcher decision. It is listed as a decision item in `10_Q1_MANUSCRIPT_INTEGRATION_PLAN.md` §13.

**Severity:** MINOR. The defect is in one *proof sentence*. The statement of Lemma E′ is true, and no number computed by 51 is affected.

## 1. The sentence in question

42 `42_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md`, §12.4, l.476 (proof of Lemma E′), quoted verbatim:

> 任取 envelope `e_u`，其可負擔集合為 `S = {x : a(x) ≤ e_u}`，部門最適集合為 `T ⊆ S`。取 `x ∈ T` 並令 `e' = a(x)`。新可負擔集合 `S' = {p : a(p) ≤ a(x)} ⊆ S`，且 `x ∈ S'`，因此 `x` 在 `S'` 上仍為部門最適，`T' = T ∩ S'`（最大值不變）⊆ `T`。… Pessimistic leader：**取任一 `x ∈ T`**；`T' ⊆ T`，故 `T'` 上的最小企業貢獻不小於 `T` 上的最小值（pessimistic 值弱增）。…

42 §12.3, l.458 defines the follower's optimal set with a tolerance: "`X*_u(y,γ,e_u) = argmax F_u`（容差 `ε_tie`，預先登記；預設 `1e-9` 相對）". 51 implements it at l.672–673 (`unit_response`):

```
m = max(p["fU"] for p in aff)
tied = [p for p in aff if p["fU"] >= m - TOL * max(1.0, abs(m))]
```

## 2. The issue

The claims "`T' = T ∩ S'`（最大值不變）" and "`T' ⊆ T`" hold under **exact** ties for every `x ∈ T`, because every element of `T` is then `F_u`-maximal on `S`. Under a tolerant tie rule (`ε_tie > 0`, absolute or relative) they hold **only** when `x` is an `F_u`-maximal element of `T`. If `x ∈ T` lies strictly below the maximum (it is only within tolerance of it), the maximum on `S'` can drop. The tie threshold then drops with it whenever `g` is strictly increasing near `m` (every absolute tolerance and 51's relative rule; for a locally constant step rule no new near-ties appear) [T8-fix], and `T'` can admit plans that were outside `T`. The pessimistic value can fall. "取任一 `x ∈ T`" therefore fails for the pessimistic case under 42's own (relative) tolerance.

## 3. Counterexample

Red-team scratch check `t6/tie_shrink.py`, which re-implements 51's rule `F ≥ m − 1e-9·max(1,|m|)`. Re-run by T7 on 2026-10-15 with identical output. There is one pooled resource:

| plan | `a` | `F_u` | `φ` (enterprise contribution) |
|---|---|---|---|
| `x_top` | 2 | 1 | 10 |
| `x_hat` | 1 | 1 − 0.9·10⁻⁹ | 10 |
| `x_low` | 0 | 1 − 1.5·10⁻⁹ | −100 |

* At `e = 2`: `m = 1`, so the threshold is `1 − 10⁻⁹`, and `T = {x_top, x_hat}`. Opt = pess = **10**.
* Shrink to `a(x_hat) = 1`. This is allowed by "取任一 `x ∈ T`", since `x_hat ∈ T`. Now `m′ = 1 − 0.9·10⁻⁹` and the threshold is about `1 − 1.9·10⁻⁹`, so `T′ = {x_hat, x_low}` ⊄ `T`. The pessimistic value is **−100**: it fell from 10 to −100 instead of weakly increasing.
* Shrink to `a(x_top) = 2`, the `F_u`-maximal element of `T`. Then `T′ = T` and pess = 10.

Run output:

```
e=2 -> {'opt': 10.0, 'pess': 10.0, 'T': ['x_top', 'x_hat']}
 shrink to a(x_top)=2.0 -> {'opt': 10.0, 'pess': 10.0, 'T': ['x_top', 'x_hat']}
 shrink to a(x_hat)=1.0 -> {'opt': 10.0, 'pess': -100.0, 'T': ['x_hat', 'x_low']}
```

## 4. Repair (proposed wording; statement unchanged)

**Repaired pessimistic step.** Pessimistic leader: take `x̃` to be an `F_u`-**maximal** element of `T`, i.e. `F_u(x̃) = max_S F_u`. Then `S' = {p : a(p) ≤ a(x̃)} ⊆ S` contains the maximizer, so the maximum is unchanged. Hence `T' = T ∩ S' ⊆ T`, and the minimum enterprise contribution on `T'` is not smaller than on `T`.

The optimistic step is valid as written under tolerance. Let `x` be the `φ`-maximal element of `T`. The maximum on `S'` can only fall, so `x` still clears the (weakly lower) threshold and `x ∈ T'`. The optimistic value at `e'` is therefore `≥` the original. It is "weakly higher", not necessarily "unchanged".

**Proposed replacement for the Chinese text (for the researcher, not applied):** "Pessimistic leader：取 `x` 為 `T` 中部門目標最大者（`F_u(x) = max_S F_u`）；此時 `S'` 仍含最大值點，最大值不變，`T' = T ∩ S' ⊆ T`，故 `T'` 上的最小企業貢獻不小於 `T` 上的最小值。（若取 `T` 中非最大者，在 `ε_tie > 0` 下 `T'` 可能納入原本不在 `T` 中的計畫，悲觀值可下降。）Optimistic leader 在容差下取 `T` 中企業貢獻最大者仍成立（該點仍在 `T'`，optimistic 值弱增）。"

**Scope of the repaired lemma** (proved in `02_Q1_DELEGATION_LOSS_THEOREM.md` §2.2). The repair holds for every tie rule `T = {x ∈ S : F_u(x) ≥ g(max_S F_u)}` with `g` non-decreasing and `g(m) ≤ m`. That covers exact ties, any absolute tolerance, and 51's relative rule, whose `g(m) = m − 10⁻⁹·max(1,|m|)` is increasing. The proof assumes exact affordability `a(x) ≤ e`. 51 also admits `a ≤ e + 10⁻⁹` (51 l.667); that absolute slack on resources is not covered by this repair. [T8-fix] Under that slack Lemma E′ can be inexact on adversarial data (T8 2-plan counterexample, Q/15 §1.2: `x` with `a = 1 + 0.5·10⁻⁹`, `F = 10`, `φ = 5`; `bad` with `a = 1 + 1.2·10⁻⁹`, `F = 20`, `φ = −100`; envelope `e = 1` gives 5, the best E′ envelope −100); it coincides with the exact model whenever no two distinct values of a pooled-resource coordinate across a unit's plans differ by a positive amount `≤ 10⁻⁹`.

## 5. Effect on 51 and on computed numbers

**None.** 51's `envelopes_lemmaE` (51 l.682) enumerates every resource vector `a(x)`, including `a(x̃)` for the `F_u`-maximal `x̃`. The leader's knapsack maximizes over all of them. So 51 relies only on the *statement* of Lemma E′ (some element of `E′_u` is at least as good as any envelope), never on the proof's particular choice of `x`. The statement is true under 51's rule (§4). Every reported 51 number (T-ORC-8, T-ORC-9/13, T-SEN-3/7/8, T-MIS-6, REG including P8 10 → 15; baseline `Q\baseline\BASELINE_V2_2_RUN_STDOUT.txt`, VERDICT PASS) is unaffected. 51's docstring for `envelopes_lemmaE` repeats the same "every x in T" wording. That is documentation only, and the same erratum candidate applies to it.

## 6. Related in-pack consequences

* `02` Lemma DL-1p, (⇒) step. The earlier draft chose the `φ`-minimizer of the tie set, which has the same gap. It is now repaired with the `F_u`-maximal selection plus a per-unit sum argument (02 §2). As a result, 02 §9.2 is upgraded from NOT_PROVEN to PROVEN for 51's relative `ε_tie`, under exact affordability.
* `04` Lemma I (formerly "Lemma S", implementability via Lemma E′) and `03` GS-N remain exact-tie results.

## 7. Researcher decision requested

1. Accept or reject this erratum candidate for 42 §12.4 l.476 (and for the 51 docstring wording) at the next canonical version bump.
2. Decide whether Appendix C of the manuscript should carry a short note now. The proposed wording is in 10 §13; v2.2's verbatim text in C.1–C.9 stays unchanged.
