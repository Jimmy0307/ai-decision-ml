# 08 — Information-Asymmetry Extension Note (future-extension research design)

```
INFORMATION_ASYMMETRY = SIDECAR_DESIGN_ONLY
```

**Agent:** T4. **Date:** 2026-10-14.

**What this note is not.** It does **not** modify 42 v2.2, 51 or any canonical file. It states **no canonical theorem**. It is **not complete**: several items in §7 are open. It is **not a primary result of the thesis**, and it must not appear in Chapter 4. The numerical example in §5 is SIMULATED_ONLY, and it is a constructive example, not evidence. No enterprise parameter, no ROI figure and no human data are used.

---

## 1. Why P3 is a limitation

42 v2.2 §15 P3 (l.630): "在本模型的完全資訊假設下 `F_E^B ≥ F_E^C` 恆成立；因此模型**不能**證明分權較佳." 42 §11.1 (l.437) adds: "模型假設企業層知道部門參數（完全資訊），因此 B 永遠弱優於 C。分權在真實組織中的資訊優勢（Alonso, Dessein, & Matouschek, 2008）**不在本模型內**." 59a §5.6 draws the consequence: if NEV is negative, "原因只能是授權損失大於集中規劃與共享能力價值之和，而不是資訊因素."

The ordering `B ≥ C` (P1) is therefore an **artifact of the information assumption**. It is not a finding about delegation. With `I_E = I_u = θ`, the central planner can replicate any delegated outcome: every Model C (leader, follower) pair is feasible in B. Three consequences follow.

1. **Built-in bias against delegation.** `DL = F_E^B − F_E^C ≥ 0` measures only the cost of ledger misalignment (P2). The main benefit that the organization literature attributes to decentralization is absent: local knowledge of local parameters (Alonso et al., 2008, TYPE B anchor).
2. **NEV has a one-sided interpretation.** `NEV = VCP + VSC − DL` can never be raised by local information, so the model can say when coordination pays but cannot say when autonomy pays.
3. **M1 (real authority) is only half-represented.** Aghion & Tirole (1997) tie real authority to information. v2.2 represents information only as the binary `Eff_H` feasibility flag ("行動前可見資訊、足夠時間、真實否決"). It does not represent the *value* of the information held by whoever has authority.

Ambiguity note. P3's sketch reads "企業以粗略估計 `θ̂` 規劃（Model B^info），部門以真實 `θ` 回應，於真實 `θ` 評估". This note fixes the following convention. `B^info` is the centralized decision computed under the enterprise's information and evaluated at the true `θ`, with no unit discretion. The phrase "部門以真實 θ 回應" is read as describing the delegated (C-side) comparator, which is `C^info` below. The other reading (a centralized plan under `θ̂`, after which units re-optimize with the true `θ`) is a hybrid. It would have to be defined separately and is not analyzed here.

---

## 2. Primitives

- **Parameter split.** `θ = (θ_0, (θ_u)_{u∈U})`. `θ_u` is the unit-local block: `π_j, P_j, ρ_j, v_j, l_j, c_j, t_j, N_jk` and, where unit-specific, `C^impl_jk(s)` for `j ∈ J_u`. `θ_0` holds enterprise-wide parameters (`F_c`, `Ā^h`, policy tables, `ΔC^gov`).
- **Information sets.** `I_E = (θ_0, (Θ_u^E, μ_u)_{u})`: the enterprise knows `θ_0` and only that `θ_u ∈ Θ_u^E`, possibly with a prior `μ_u`. `I_u = (θ_0, θ_u)`: unit `u` knows its own block. More generally `I_u = Θ_u^u ⊆ Θ_u^E` with `θ_u ∈ Θ_u^u` (refinement).
- **Assumptions (sidecar baseline).**
  - IA-A1 (refinement): `I_u` refines `I_E` on `θ_u`.
  - IA-A2 (no communication): no messages, no type-contingent menus.
  - IA-A3 (finite types): `Θ_u^E` is finite. This is needed for Proposition IA-2.
  - IA-A4 (pre-registered decision rule): the enterprise's rule under `I_E` is fixed before solving. Options are prior-mean plug-in, minimax regret over `Θ^E`, or a registered `θ̂`.
- **Status convention.** If a decision chosen under `I_E` is infeasible at the true `θ`, because (F9) or (R2) depend on `θ`, or because some unit has an empty feasible set, the outcome is reported as `INFEASIBLE_UNDER_TRUE_THETA`. This is the analogue of `DESIGN_INFEASIBLE_UNDER_RESPONSE` (42 §14 Q6). LIA, DL^info and NDV are then undefined for that `θ`; they are reported, not imputed.

---

## 3. Sidecar models

- **`B^full`**: the canonical v2.2 Model B, with value `F_E^B(θ)`.
- **`B^info`**: the enterprise chooses the whole decision `d^{B,info} = R_E(I_E)` (including `y`, `γ`, `q`, `y^loc`). Its value is `F_E^{B,info}(θ) := F_E(d^{B,info}; θ)`.
- **`C^info`**: the leader chooses `(y, γ, e)` by rule `R_E` while anticipating the type-contingent best responses `X_u^*(y,γ,e_u; θ_u)` for every `θ_u ∈ Θ_u^E`. The follower best-responds with its true `θ_u`. Ties are handled per type, with optimistic and pessimistic modes as in 42 §12.3. The value is `F_E^{C,info,mode}(θ)`, evaluated at the true `θ`.

### 3.1 Candidate quantities

| Name | Definition | Meaning |
|---|---|---|
| **LIA** (Local Information Advantage) | `LIA(θ) := F_E^B(θ) − F_E^{B,info}(θ)` | value lost by centralizing without local information |
| **DL^info** | `DL^info,mode(θ) := F_E^B(θ) − F_E^{C,info,mode}(θ)` | delegation loss when the leader also plans under `I_E` |
| **NDV** (Net Delegation Value) | `NDV^mode(θ) := F_E^{C,info,mode}(θ) − F_E^{B,info}(θ) = LIA(θ) − DL^info,mode(θ)` | net value of delegating to the informed unit, relative to informed-less central planning |
| candidate in the brief | `LIA − DL` (with v2.2 `DL = F_E^B − F_E^C`) | an **upper bound** on NDV (Proposition IA-1) |

The identity `NDV = LIA − DL^info` holds by definition whenever all three values are defined.

---

## 4. Results provable now (sidecar; not canonical)

**Proposition IA-1 (LIA − DL bounds NDV from above).** Assume IA-A1, IA-A2 and IA-A4, a fixed `mode ∈ {opt, pess}`, and that `F_E^{C,info,mode}(θ)` is defined. Then `F_E^{C,info,mode}(θ) ≤ F_E^{C,mode}(θ)`, hence `DL^info ≥ DL` and `NDV ≤ LIA − DL`. If in addition `d^{B,info}` is feasible at `θ`, then `LIA ≥ 0`.

*Proof.* The follower's information is the same in `C` and `C^info`: in both it knows the true `θ_u`. So for every leader decision `(y,γ,e)`, the follower's optimal set at the true `θ` is the same in both models, and so is the leader's true value under `mode`. `F_E^{C,mode}(θ)` is the maximum of this true value over all admissible leader decisions (42 §12.5 step 4). `F_E^{C,info,mode}(θ)` is that same true value at one particular admissible decision, the one chosen by `R_E`. A value at one point cannot exceed the maximum. For LIA: `d^{B,info}` is feasible in B at `θ` and `F_E^B(θ)` is the B optimum, so `F_E^B(θ) ≥ F_E(d^{B,info};θ)`. ∎

**Corollary (recovering P3).** If `I_E = I_u = θ` (full information), then `B^info = B` and `C^info = C`. Hence `LIA = 0` and `NDV = −DL ≤ 0`, which is exactly the P1/P3 ordering. The sidecar nests v2.2 and does not contradict it.

**Proposition IA-2 (envelope finitization under finite types — Lemma E″, proof sketch; needs independent audit before any use).** Assume IA-A2 and IA-A3. Assume also that the leader's objective aggregates per-type values through a map that is nondecreasing in each per-type value; expectation under `μ_u`, worst case and negative max-regret all qualify. Then the leader loses nothing by restricting `e_u` to

```
E″_u = { ∨_{θ_u∈Θ_u^E} a(x_{θ_u}; θ_u)  :  x_{θ_u} ∈ 𝒫_u(θ_u) }      (∨ = componentwise max)
```

*Sketch.* Fix any `e_u`. For each type, pick `x_θ` in the follower's optimal set `T_θ(e_u)`; under `opt`, pick the enterprise-best element. Let `e' = ∨_θ a(x_θ;θ) ≤ e_u`. For each type, the new affordable set `S_θ(e') ⊆ S_θ(e_u)` still contains `x_θ`. So the follower's maximum is unchanged, and `T_θ(e') = T_θ(e_u) ∩ S_θ(e') ⊆ T_θ(e_u)`. The optimistic per-type value is preserved, and the pessimistic per-type value weakly increases. By monotonicity of the aggregator, the leader's objective weakly increases. Because `e' ≤ e_u`, the leader's (R1′) constraint stays satisfied. Each coordinate of `e'` is a coordinate of some plan vector, so `|E″_u| ≤ (Σ_θ |𝒫_u(θ)|)^{|H^pool|}`, which is finite.

*Remarks.* (i) The canonical Lemma E′ set `E'_u = {a(x)}` does **not** suffice in general under type uncertainty: a single plan vector can be too small for another type's preferred plan. The closure under `∨` is the needed extension. (ii) For a continuum of types the finiteness argument fails, and the claim is NOT_PROVEN. (iii) Type-contingent envelope menus (screening contracts) are excluded by IA-A2.

**Proposition IA-3 (conditional sign; proof sketch).** Assume (AL1)–(AL4) of 42 §8.2. Assume the `C^info` leader uses the same `(y, γ)` as `d^{B,info}` and sets `e_u ≥ a(x_u^{B,info}; θ_u)` at the true `θ_u`. Then `NDV(θ) ≥ 0`, and optimistic and pessimistic values coincide.

*Sketch.* Under (AL), `φ^u = φ`. The unit at the true `θ_u` maximizes the enterprise contribution over its affordable set, and that set contains `x_u^{B,info}`. Under (AL), ties in `F_u` are ties in the enterprise contribution, so `opt = pess`. ∎

The second condition requires the leader to know an affordable upper bound at the true type. Choosing the envelope over `Θ^E` as in IA-2 guarantees this when the leader uses the componentwise max over types.

---

## 5. Constructive example (SIMULATED_ONLY; `Q\witness_parts\w_mech.py :: witness_ia_ndv_sign`, pass = True)

**Setup.** One unit, one initiative, `K = {k0, k1, k2}`, types `Θ_u^E = {a, b}` with prior `(½, ½)`. Enterprise contributions are `φ(k0,·) = 0`, `φ(k1,a) = 10`, `φ(k1,b) = 1`, `φ(k2,a) = 4`, `φ(k2,b) = 8`. Resource use satisfies `a(k1) = a(k2)`, so the envelope cannot separate the two configurations.

**B^info.** Both the prior-mean rule (5.5 vs 6.0) and minimax regret (7 vs 6) choose `k2`.

| Ledger | true θ | B^full | B^info | C^info | LIA | DL^info | NDV |
|---|---|---|---|---|---|---|---|
| aligned | a | 10 | 4 | 10 | 6 | 0 | **+6** |
| aligned | b | 8 | 8 | 8 | 0 | 0 | 0 |
| misaligned (`φ^u(k1,b) = 9`) | a | 10 | 4 | 10 | 6 | 0 | +6 |
| misaligned | b | 8 | 8 | 1 | 0 | 7 | **−7** |

**Reading.** Under asymmetric information, delegation can strictly beat centralized planning (`NDV > 0`), which reverses the P1/P3 ordering. Under misalignment it can strictly lose (`NDV < 0`). This trade-off between local information and alignment is the one Alonso et al. (2008) anchor conceptually (TYPE B). The example does not show how often either case occurs, and it says nothing about any enterprise.

---

## 6. Outline of a sidecar computational model (design only)

1. **Inputs.** The v2.2 instance plus the type registry `Θ_u^E` (finite), optionally a prior `μ_u`, the rule `R_E`, and evidence that `I_E ≠ I_u`. 42 P3 says the extension "需要「企業與部門知道不同參數」的證據，否則不執行". The proposed elicitation is to collect `Θ_u` intervals separately from central staff (`I_E`) and from unit staff (`I_u`) under the same template, and to treat a strictly narrower unit interval that contains the later observed value as the evidence. This must be pre-registered.
2. **Solver.** Enumerate `(y, γ)`. For each unit and type, enumerate follower plans; build `E″_u` (IA-2); compute per-type optimistic and pessimistic values; aggregate by `R_E`; run a multiple-choice knapsack over `E″_u` as in 42 §12.5. Evaluate the chosen decision at every true `θ` in the registry. Independent re-implementation is required (no import from 51), with brute-force cross-checks against unrestricted envelope grids, as was done for Lemma E′ (50 §6).
3. **Outputs.** `LIA`, `DL^info`, `NDV` per true type and per mode; the `INFEASIBLE_UNDER_TRUE_THETA` status; the sign pattern of NDV across the registry; a decomposition of NDV by turning off (AL1)–(AL4) one at a time, as for DL in 42 §14 Q4.
4. **Classification.** Lemma R does not apply because this is C-type and the value is not multilinear (42 §13.3 item 2). Results are reported "on evaluated points" with coverage, never as certificates.

---

## 7. What would have to be proven before any use beyond this note

| # | Item | Status |
|---|---|---|
| 1 | Well-posedness and status conventions under infeasibility at the true `θ` (§2) | defined here; needs audit |
| 2 | IA-1 (`NDV ≤ LIA − DL`; Corollary recovers P3) | proof complete (sidecar) |
| 3 | IA-2 (Lemma E″, finite types, monotone aggregator) | proof sketch; independent audit + brute-force check required |
| 4 | IA-3 (non-negative NDV under AL and envelope cover) | proof sketch; conditions restrictive |
| 5 | Necessary and sufficient conditions for `NDV > 0` (local-information value exceeds misalignment loss) | **NOT_PROVEN**; no iff is claimed |
| 6 | Interaction with P8 screening: can requirements substitute for missing information, or destroy LIA by removing the configurations that local information would select? | open (conjecture both directions possible) |
| 7 | Interaction with P4 (`F_c^†` monotone in C): does monotonicity survive leader uncertainty over `θ_u`? | open |
| 8 | Continuous type spaces; communication/messages; type-contingent menus (mechanism design) | out of scope; NOT_PROVEN |
| 9 | Identification protocol for `I_E` vs `I_u` (elicitation, pre-registration, provenance tags) | design only |
| 10 | Link to M1 (`Eff_H` as binary information flag vs graded value of information held by the right-holder) | conceptual (TYPE C candidate) |

---

## 8. Positioning and non-claims

- **TYPE B anchors (in the 59a reference list):** Alonso, Dessein & Matouschek (2008), information advantages of decentralization versus coordination; Aghion & Tirole (1997), real authority tied to information. Any further delegation or cheap-talk literature is **to verify** and is not cited here.
- **TYPE C (this note, sidecar):** the LIA, DL^info and NDV definitions, IA-1, the Corollary, and the IA-2 and IA-3 sketches.
- v2.2 is unchanged. P1–P8 and Lemma E′ hold as stated in their full-information setting. This note only adds a nested extension whose full-information special case reproduces P3.
- This is not a thesis primary result and not complete. The manuscript may mention it in §5.8.5 or §5.9 as a future-extension design, with the status line below.

```
INFORMATION_ASYMMETRY = SIDECAR_DESIGN_ONLY
```
