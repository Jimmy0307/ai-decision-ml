# 15 — Independent verification of the T7 repairs (verifier T8)

**Date:** 2026-10-15. **Scope:** only the T7-tagged changes in Q/01–07 (diffed line by line against the pre-edit originals in `scratchpad/t7/orig/`). Q/10 was checked for leftover overclaims only. Canonical sources were read only: 42 §12.3–12.4 (l.458, l.466–478) and 51 `unit_response` (l.666–674), with `TOL = 1e-9` (51 l.37). Nothing in REPO or in Q/01–07 was edited.

**T8 scratch:** `work/T8/t8_tie_fuzz.py` and `work/T8/t8_power.py`. Both are pure stdlib and deterministic. They are a falsification search, **not a proof**.

---

## 1. 02 §2.2 / §9.2: tolerance upgrade NOT_PROVEN → PROVEN

**Verdict: CONFIRMED_WITH_QUALIFICATION**

### 1.1 Is 51's tie rule of the form `{F_u ≥ g(m)}`, with `g` non-decreasing and `g(m) ≤ m`?

Yes. 51 l.672–673 reads:

```
m = max(p["fU"] for p in aff)
tied = [p for p in aff if p["fU"] >= m - TOL * max(1.0, abs(m))]
```

- `m` is the maximum of the **unit ledger** `F_u` over the affordable set, so the tolerance is relative to the follower's own optimum. That is the quantity the proof uses.
- So `g(m) = m − t·max(1,|m|)` with `t = 1e-9`. Piecewise:
  - `(1−t)m` for `m ≥ 1`;
  - `m − t` for `|m| < 1`;
  - `(1+t)m` for `m ≤ −1`.
- It is continuous at `±1`, the slopes are `1−t`, `1` and `1+t`, all positive, and `g(m) ≤ m` everywhere.
- Negative values cause no sign problem: for `m ≤ −1` the threshold `(1+t)m` lies below `m`. The `abs` keeps the band on the correct side.

### 1.2 The proof

Every step of the pessimistic (⇒) direction checks out:

- **Choice of `x̃_u`.** An `F_u`-maximal element `x̃_u` exists in `BR^g_u(e_u)` because `g(m) ≤ m`.
- **(S-max).** `x̃_u ∈ S_u(a(x̃_u)) ⊆ S_u(e_u)`. Hence `m_u(a(x̃_u)) = m_u(e_u)`, and so `BR^g(a(x̃_u)) = BR^g(e_u) ∩ S(a(x̃_u))`.
- **(S-weak).** This step needs only monotonicity of `g`.
- **Attainment of `F^{C,m}`.** This is valid because `BR^g_u(e)` depends on `e` only through the finite family of affordable sets.

**Multiple BUs and coupled envelopes.** The per-unit sum argument holds:

- The only cross-unit coupling at fixed `(y,γ)` is `Σ_u e_u ≤ b̄(y,γ)`. It is preserved because `a(x̃_u) ≤ e_u` (exact affordability).
- `K(y,γ)` is common to both models.
- `Σ_u φ(x̃_u) − K ≤ F^B = Σ_u μ_u − K` together with `φ(x̃_u) ≥ μ_u` forces termwise equality.
- Coupling through `y` and `γ` is held fixed, so it does not interfere.

**The 1e-9 affordability slack is correctly excluded, and it matters.** 51 l.667 admits `a ≤ e + 1e-9`. Under that slack the affordable set after shrinking, `{a ≤ a(x̃)+t}`, is not a subset of `{a ≤ e+t}`. T8 built an explicit gap (`t8_tie_fuzz.py`, last line of output):

- plan `x`: `a = 1 + 0.5e-9`, `F = 10`, `φ = 5`;
- plan `bad`: `a = 1 + 1.2e-9`, `F = 20`, `φ = −100`.

With 51's slack semantics, the non-E′ envelope `e = 1` gives value 5, but the best E′ envelope gives −100. So under 51's own semantics E′ is not exact on adversarial data. The scope note in 02 §2.2(1) is therefore necessary, not cosmetic. Its wording is slightly imprecise; the fix is in Required text change 1 below.

### 1.3 Counterexample search

Setting:

- 6,000 instances under 51's exact rule `g`;
- 1–3 BUs, 2 pooled resources with negative components allowed, a coupled budget;
- `F_u` scales `±1`, `±1e3`, `±1e6`, `0.3`, `−0.7`, with near-ties spaced `0.45e-9·max(1,|scale|)`;
- envelopes on the exact product grid of plan coordinates, which reaches every distinct affordable set.

Results:

- Lemma E′ (product grid = E′, for both opt and pess): **0 violations**.
- DL-1o/p (`DL^m = 0` ⇔ some first best is m-self-enforcing, with `BR^g`) over 11,424 checks, of which 1,369 opt and 3,015 pess had `DL > 0`: **0 violations**.
- P1 held throughout.

**Power check (`t8_power.py`).**

- On 48,685 multi-element tolerant tie sets, the **old** step failed 139 times. The old step chose the `φ`-minimizer of the tie set and then shrank.
- The **repaired** step (`F_u`-maximal choice) failed 0 times.
- So the search can detect exactly the defect that T7 repaired.
- The Q/13 counterexample (`x_top`, `x_hat`, `x_low`; pess 10 → −100) was recomputed by hand and is correct.

### Qualifications

- **(Q1a)** The result is exact-affordability only, as T7 states. 51's slack produces a real gap on adversarial data (example above).
- **(Q1b)** In §2.2, "the proof sentence of 42 l.476 is **false** … under **any** `g(m) < m`" is too strong. If `g` is locally constant (a non-decreasing step rule), then `g(F(x̂)) = g(m)` and no new near-ties appear. The sentence fails whenever `g` is strictly increasing near `m`. That covers absolute tolerances and 51's relative rule.
- **(Q1c)** Only DL-1o/p and Lemma E′ are upgraded. Cor DL-2/3, DL-4/5, Lemma S, Lemma I and GS-N remain exact-tie results. T7 states this correctly.

### Required text changes (02 only)

1. In §2.2 "Scope of the upgrade" (1), replace "(it is immaterial whenever … differ by more than `10^{-9}`)" with:

   > "(under 51's slack the unit at envelope `e` sees `{a ≤ e + 10^{-9}}`, so 51 evaluates the exact-affordability model at `e + 10^{-9}`; this coincides with offering `e` itself whenever no two distinct values of any pooled-resource coordinate across a unit's plans differ by a positive amount `≤ 10^{-9}`. Then 51 equals the exact model with budget `b̄ + 10^{-9}` in both B and C. Otherwise E′ can be inexact under 51's own semantics (T8 example, Q/15 §1))".

2. In §2.2 "Lemma E′ under `g`", replace "is **false** for the pessimistic case under any `g(m) < m`" with:

   > "fails for the pessimistic case under any tie rule with `g` strictly increasing near `m` (every absolute tolerance and 51's relative rule)".

---

## 2. Cor DL-3 repair (unique first best; Parts (i) and (ii))

**Verdict: CONFIRMED**

**Hypotheses are now consistent.**

- (H0) is the standing hypothesis.
- Part (i) adds `x*_u ∈ P^C_u` for all `u`.
- Part (ii) assumes it fails for some `u`.
- The earlier contradiction (assuming membership and then treating non-membership) is gone. "[exact ties]" is now in the header.

**Proof of (i) is valid.**

- *Automatic `φ` drop:* the swapped profile is B-feasible (`P^C ⊆ P^B`, resource use does not increase) and differs from `x*`, so uniqueness forces `φ(x^H) < φ(x*_u)`.
- *Opt:* this is DL-1o with a singleton `𝓑*`.
- *Pess (⇐):* both cases (`x* ∉ BR`; and `x* ∈ BR` with a tie) are handled correctly.
- *Pess (⇒):* if no such `x^H` exists, `x*_u` is the unique maximizer on `S(a(x*_u))`, so `BR = {x*_u}`.

**Proof of (ii) is valid.**

- For pess, *any* selection from `BR(e)` already has value between `V^pess = F^B` and `F^B`, so the per-unit argument is not even needed.
- For opt, the `φ`-maximizers give value `F^B`.
- Either way the selected profile lies in `P^C`. By (H0) it would have to equal `x*`, but some `x*_u ∉ P^C_u`. Contradiction.

**Witness re-verification.** Checked against `witness_parts/w_dl_gov.py` and the witness output:

| Witness | First best | Part applied | Predicted | Computed |
|---|---|---|---|---|
| W3 | unique | (i) | DL > 0 (U2 `k1`: `a = 0`, `F_u` 20 > 0) | 5/5 |
| W3b | unique `xG` | (i) | opt: no strict deviation ⇒ 0; pess: weak deviation `xH` ⇒ > 0 | 0/1 |
| W3c-I1 | unique `xG` | (i) | `xH`: `a` 0 ≤ 1, `F_u` 1 > 0 ⇒ DL > 0 | 2/2 |
| W3c-I2 | `xG` and `xM` (both `φ` = 2); (H0) fails | Cor DL-3 silent | DL-1 applies; `xM` is self-enforcing at `e = 1` | 0/0 |
| W_DL_AL3 | unique `xG`, `unit_ok = False` | (ii) | DL > 0 | 1/1 |

---

## 3. DL-4 repair (direct bound `V^m(a(x*)) ≥ F^B`)

**Verdict: CONFIRMED_WITH_QUALIFICATION**

**What is valid.**

- The main proof is correct. At `e = a(x*)`, every BR element has `a ≤ a(x*_u)` and `F_u ≥ F_u(x*_u)`.
- (a) gives `φ ≥ φ(x*_u)` for all BR elements, hence `V^pess ≥ F^B`.
- (b) splits into "`max F > F(x*)` ⇒ every BR element strictly beats `x*` in `F_u`" and "otherwise `x*_u ∈ BR`". That gives `V^opt ≥ F^B`.
- The repair also fixes the old error: concluding that `x*` itself is self-enforcing.

**Two defects remain.**

- **(Q3a) The closing parenthetical is false for (b).** It says that any `F_u`-maximal `x̃_u ∈ BR(e)` gives a self-enforcing first best. In the tie case of (b) it does not. W3b satisfies (b), since it has no strict reversal: there `x̃ = xH` is `F_u`-maximal with `φ = 0 < 1 = φ(xG)`, so `x̃` is not a first best.
- **(Q3b) AL3 is not stated in (b) or (c).** It appears only in the proof ("AL3 holds"). Without AL3, both (b) and (c) are false: W_DL_AL3 has `F_u ≡ φ^E_u` (so (b) and (c) hold) yet `DL^opt = 1`.

**Required text changes (02 §2.1, Prop DL-4).**

1. Header: replace "**[multi-BU].**" with "**[multi-BU; AL3; exact ties].** All three parts assume AL3 (`P^C = P^B`); without it (b) and (c) fail (W_DL_AL3)."
2. Parenthetical: replace "(Equivalently, via DL-1: by the shrink step any `x̃_u ∈ BR_u(e_u)` with maximal `F_u` gives a self-enforcing first best `x̃`, …)" with:

   > "(Equivalently, via DL-1: under (a), any `F_u`-maximal `x̃_u ∈ BR_u(e_u)` gives a self-enforcing first best; under (b), take `x̃_u = x*_u` when `max F_u = F_u(x*_u)`, and any element of `BR_u(e_u)` otherwise.)"

---

## 4. 07 G4 and G1; 06 R5(i); 04 W5 / W5_WIDE caveats

### 4.1 07 G4 (corrected quantifier, NULL separated)

**Verdict: CONFIRMED**

- The old wording conflicted with Definition G ("some" decision versus "every" zero-fill optimum). The counterexample `d1`/`d2` is correct: `D*(0) = {d1, d2}`, `D*(4) = {d1}`, so the case is DC.
- New DC test: "some element of `D*_0` fails a vertex". This is correct by Thm R1: a fixed portfolio is optimal on the box iff it is optimal at the vertices, because `F*` is convex.
- New NULL test: `ΔHours(d°) = 0` (so `F*` is constant) and no `d ∉ D*_0` is optimal at any vertex. The second condition is correct: `F(d°) − F(d)` is affine and `≥ 0` on the box, so if it reaches 0 anywhere, it reaches 0 at a vertex.
- DIER is the remainder. `ID_F` is the vertex interval because `F*` is affine there.

### 4.2 07 G1 (premise)

**Verdict: CONFIRMED**

- The "same sign of effect" premise matches the list. `C^impl` lowers value and shrinks feasibility, and so do `N E[I^sev]` and the requirement thresholds.
- With `0 = min V_p`, the inclusions and value inequalities follow.

### 4.3 06 R5(i) qualifier

**Verdict: CONFIRMED**

- With `θ`-independent `a_u`, the affordable set is fixed. `V` is then a maximum of finitely many block-multilinear functions, hence block-convex.
- The qualifier correctly sends the `θ`-dependent affordability case (`a^BUD ∋ N·E[c]`) to (iii).
- W7b is unaffected because its costs are zero.

### 4.4 04 every-resource footprint caveat and W5 / W5_WIDE fragility

**Verdict: CONFIRMED_WITH_QUALIFICATION**

- All numbers match `q1_theory_witnesses_output.txt`:
  - W5 survivors: 398/400 at ±1 %, 162/400 at ±5 %.
  - W5_WIDE survivors: 367/400 at ±5 %, 256/400 at ±10 %.
  - Knife-edge components: `cost_floor_0_01 = 1`, `eng_footprint_1e_6 = 1`, `floor_0_5_plus_negative_opex_minus_1 = 2`.
  - Margins 3 versus 1.
  - `D = 3+δ` / `δ−7` / `3` gives the region `[0,4) ∪ (7,∞)`.
- The renaming Lemma S → Lemma I is consistent throughout 04.
- The Lemma M qualifier matches Lemma M's hypotheses.

**Defect: internal inconsistency in the caveat.** The caveat says: "With any strictly positive ENG footprint or any strictly positive floor on the reused cost, the envelope always separates and the region is an interval." Its own parenthetical reports that a floor of 0.5 with opex −1 **restores** the non-interval region (2 components). The binding quantity is the **net** pooled footprint (reused cost plus incremental opex) relative to the status quo. The cost floor is not the binding quantity. Likewise, "the same two exact zeros" (header line `W5_FRAGILITY` and §6) should read: net BUD footprint ≤ status quo, and ENG footprint = 0. Also, "always … interval" is shown only for the W5 / W5_WIDE family, through D5-type invariance of the order.

**Required text changes (04).**

1. §6 caveat: replace "With any strictly positive ENG footprint or any strictly positive floor on the reused cost, the envelope always separates and the region is an interval" with:

   > "In the W5/W5_WIDE family, any strictly positive ENG footprint, or any strictly positive floor on the AI configuration's **net** BUD footprint (reused cost plus incremental opex) relative to the status quo, makes the envelope separate for every `δ`, and the region is an interval".

2. Header `W5_FRAGILITY` and §6 ("same two exact zeros"): replace "(zero reused-cost floor, zero ENG footprint)" with:

   > "(net BUD footprint reaching ≤ the status quo's — a zero reused-cost floor in W5/W5_WIDE, or a positive floor offset by negative incremental opex — and zero ENG footprint)".

---

## 5. Relabels: remaining overclaims in 01–07 and 10

**Verdict: CONFIRMED_WITH_QUALIFICATION**

Most relabels are in place and correct:

- 01: IRR is labelled as non-redundancy; "irreducible" is removed from the status lines, from the §6 combined claim and from the §8 manuscript label; the Legal factor is moved into `Φ^{M1}`.
- 02: DL-1 is labelled a characterization lemma; the restatement table is present; the `DL_IFF_THEOREM` line is honest.
- 03: GS-0 is a restatement, GS-I an identity, GS-I′ a corollary; the embeddings are stated.
- 04: D1 and D3 are labelled restatement-level.
- 05: Lemma 0, E.2, E.3 and E.10 are labelled restatements; SIP is a protocol.
- 06: Thm R1 is labelled a restatement.
- 07: TYPE C (known framework); the restatement list is present.

Residual overclaims, with the minimal changes:

| # | Location | Problem | Minimal change |
|---|---|---|---|
| R-a | 02 §3 table, Status column, rows 5–9 | "Theorem" cites DL-1, which is now a lemma (restatement-level); row 9 is titled "Optimistic vs pessimistic theorems" | Rows 5, 7, 8: "Theorem" → "Lemma (DL-1) + corollary". Row 6: "Counterexample / Theorem" → "Counterexample / Lemma". Row 9: title "theorems" → "results"; status "Theorem" → "Lemma + corollaries" |
| R-b | 01 l.1 title, §5 heading (l.169), §6.1 heading and first sentence (l.201, l.203), l.277 | Bare "irreducibility", contrary to 01's own terminology note at l.158 | "irreducibility" → "non-redundancy (IRR, under T1–T4)" at each place. l.266 "genuinely irreducible to the static model" is unrelated usage and can stay |
| R-c | 10 rows 1.3, 1.4, 1.6, 4.3, 6.1, 8.4, 8.5, C.10.6 | "Thm R1", "Thm D1" and "Thm D3" are given the status "theorem" without the restatement tag that 04/06 now carry | Add "(restatement of 42 Lemma R)" after Thm R1 and "(restatement of P2 pointwise)" / "(explicit form of P4, B part)" after Thm D3 / D1; status column "theorem" → "restatement / proposition" |
| R-d | 10 §… "形式理論貢獻（模型內；TYPE C）", items 3 and 4 | D1, D3 and R1 are listed under the TYPE C heading | Item 3: "(D1, D3, D6)" → "(D4–D6, Lemma M; D1/D3 restate P4/P2)". Item 4: "(R1–R5)" → "(R2, R4, R5(ii); R1 restates 42 Lemma R)" |
| R-e | 10 row 1.2, column "risk" | "The iff quantifies over all first-best solutions" | "The characterization (Lemma DL-1) quantifies over all first-best solutions" |
| R-f | 02 §2.2 (wording, see §1) and 03 l.268 | 03 says that GS-1 (BR-form) "carries over" to `g`, "noted, not separately re-proved" | Acceptable as worded (it is not claimed as proven); no change required |

**Outside 01–07/10, informational only.** `witness_parts/w_dl_gov.py` (l.167, 195, 204, 366, 392) and the assembled `q1_theory_witnesses.py` still say "Theorem DL-1" / "Thm DL-1p". Relabel them to "Lemma DL-1" at the next witness regeneration; the hash changes accordingly. The `envelopes_lemmaE` docstring in 51 (l.683–686) repeats the "every `x` in `T`" claim. Q/13 could mention this; 51 must not be edited.

---

## 6. Summary of verdicts

| Item | Verdict |
|---|---|
| 1. Tolerance upgrade (02 §2.2 / §9.2) | CONFIRMED_WITH_QUALIFICATION (exact affordability; 51 slack gap is real; "any `g(m) < m`" wording) |
| 2. Cor DL-3 repair | CONFIRMED |
| 3. DL-4 repair | CONFIRMED_WITH_QUALIFICATION (AL3 missing from the (b)/(c) statement; parenthetical false for (b)) |
| 4a. 07 G4 | CONFIRMED |
| 4b. 07 G1 | CONFIRMED |
| 4c. 06 R5(i) | CONFIRMED |
| 4d. 04 W5 / W5_WIDE caveats | CONFIRMED_WITH_QUALIFICATION (net-footprint wording) |
| 5. Relabels | CONFIRMED_WITH_QUALIFICATION (R-a to R-e) |

No item is REJECTED. No revert is recommended.

```
RECOMMENDED_STATUS
DL_NECESSARY_CONDITIONS                  = PROVEN       Lemma DL-1 (every first best; also under tolerant g with exact affordability); Cor DL-2o/2p under AL3 + exact ties; AL3 channel otherwise
DL_SUFFICIENT_CONDITIONS                 = QUALIFIED    DL-4 valid only with AL3 stated for (b)/(c) and the (b) parenthetical corrected; Cor DL-3 (unique first best) PROVEN; becomes PROVEN after the two DL-4 text changes
DL_IFF_THEOREM                           = NOT_PROVEN   as a primitive iff (W3c); what is PROVEN is a first-best-relative characterization lemma (restatement of Lemma E') and Cor DL-3 under a unique first best
DL_TIE_TOLERANCE_ROBUSTNESS              = QUALIFIED    PROVEN for Lemma E' and DL-1o/p under every {F_u >= g(m)}, g non-decreasing, g(m) <= m (incl. 51 l.673), EXACT affordability only; 51's +1e-9 affordability slack not covered (T8 gap example); all corollaries exact-tie only
GOVERNANCE_SCREENING_NECESSARY_CONDITION = PROVEN       GS-N (exact ties; T7 changed labels only; proof re-read, steps valid)
MISSINGNESS_CLASSIFICATION_FORMALIZED    = PROVEN       Def G + G1-G8 with corrected G1 premise and G4 quantifier / NULL split (methodological)
Q1_THEORY_UPGRADE_VERDICT                = PARTIAL      no CRITICAL error and no revert needed; apply the minimal text changes in §1, §3, §4.4, §5 (R-a to R-e); citations still TO VERIFY; 42 erratum is a researcher decision
```
