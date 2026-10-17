# 01 — Q1 Theory Upgrade: M1–M4 Mechanism Theory (formal definitions, boundaries, non-redundancy (IRR, under T1–T4) [T8-fix], sufficiency status)

**Agent:** T4. **Date:** 2026-10-14. **Status:** theory sidecar. It does not modify 42 v2.2, 51, 41 or the manuscript. No human coding results exist and none are used or imagined. No sealed folder was opened. All numbers in §5.4 are SIMULATED_ONLY illustrations.

```
M1_M4_FORMAL_DEFINITIONS      = COMPLETE (TYPE C; relations/functions on the AI-output-to-organizational-action process)
M1_M4_BOUNDARIES              = DEFINED_BY_DECISION_OBJECT (6 pairs, incl. M1/M2)
M1_M4_IRREDUCIBILITY          = RELABELED (T7 per Q/11 A9): NON-REDUNDANT UNDER TYPING AXIOMS T1–T4 RELATIVE TO THE v2.2 ATTRIBUTE SCHEMA
                                (Prop IRR, proof complete; definitional: no dead attribute class; holds for ANY partition of the
                                 v2.2-read attributes into four non-empty classes; does NOT support M1–M4 as a theory of enterprise AI decisions)
M1_M4_MINIMAL_SUFFICIENCY     = PARTIAL
  - relative to U_v22 (v2.2 static, single-period, full-information universe): non-redundant under T1–T4 + jointly sufficient (Lemma COV; internal, circular; caveat §6.2)
  - relative to "enterprise AI decision problems" in general: NOT_PROVEN (no closed universe) -> label downgraded to
    "jointly sufficient working set for U_v22 / conceptual decomposition (mechanism taxonomy) otherwise"
NONE                          = COVERAGE-ANOMALY SIGNAL (not a classification failure; not a sufficiency test)
EVIDENCE_ONLY                 = OUT-OF-DOMAIN MARKER of the partial map G -> M (never forced into M1–M4)
DATA_GATED                    = IDENTIFICATION CONDITION (gate on the domain of a mechanism), not a mechanism
LONGITUDINAL / M5             = ORTHOGONAL TIME x INFORMATION-STATE DIMENSION ("M5" kept only as a label)
V1                            = tests inter-rater interpretability of the G->M mapping; does NOT test minimal sufficiency
V1_HUMAN_RESULTS              = NONE EXIST (not used, not simulated)
v2.2 / 51 MODIFIED            = NO
WITNESS                       = Q\witness_parts\w_mech.py :: witness_mech_ablation (pass=True), witness_ia_ndv_sign (pass=True; used by Q\08)
```

---

## 1. Sources relied on (exact locations)

| Source | Location | What is used |
|---|---|---|
| 42 v2.2 | §2 l.69–75 | configuration attribute tuple `k ≡ (A_k, H_k, WI_k, EA_k, EAX_k, m_k[, τ_k])` |
| 42 v2.2 | §5 table l.177–191 | each feasibility factor and its "來源機制" column: (F3) M1; (F4) F5/M4(G05); (F5a) M1; (F5b) M2; (F5c) M1; (F5d) M4; (F5e) F5; (F6) M1; (F7) M2; (F8) M3; (F9) M1; (F10) S via policy |
| 42 v2.2 | §5 l.202 | (F5e) evaluated at the selected capability-source state `s_j` for every `k` incl. `k=0`; missing cell excludes only `(j,k,s)` |
| 42 v2.2 | §6 (X1) l.247–253 | `E_jk[f|ȳ] = Σ_ℓ π Σ_{z,ω} P Σ_r ρ(r|k,z,ℓ,ȳ) f`; `ω` not in `ρ`'s conditioning set; `ρ` rows keyed `(z,ℓ)` or `(z,ℓ,s_j)`; "`EAX_k` 只透過 `ρ(·|k,…)` 影響結果；不另有方程項" |
| 42 v2.2 | §9.1–9.2 | `ρ^obs, ρ^cf, ρ^design`; Model D gate T1–T5 |
| 42 v2.2 | §11, §15 P1–P8, §12.4 Lemma E′, §13.4–13.5, §16 (D1)(D2) | organizational forms; propositions; missing-value rules; VOI; M5 |
| 41 v2.1 | §1 l.34–40 | interfaces I1–I5 and their "企業必須決定的問題" |
| 41 v2.1 | §5.1 l.156–183 | construct families F1–F4 (M1–M4), F5 (architecture, "非 gap 推導"), M5 dynamic |
| 41 v2.1 | §3 Q4, §6, §7 | merge groups; G→M→variable→equation trace; fallback rules |
| 59a | §3.9.1–3.9.5 | translation procedure S1–S4, Table 3-4/3-4A, V1 design (Q1–Q5, Krippendorff α thresholds), AI pilot (G04/G10/G11 contested, mapping-only), fallback rules |
| 59a | §3.11–3.12, §5.6–5.8 | model statement, P1–P8 as stated in the manuscript, limitations (5.8.4 V1 pending; 5.8.5 full information; 5.8.6 M5) |
| 26 V1 codebook v1.8.2 | §2–§5 | category definitions, consistency rules, order of tests (a) LONGITUDINAL → (b) DATA_GATED → (c) M1–M4/NONE → (d) EVIDENCE_ONLY; crosswalk NONE→OTHER (new_construct_required=YES) |
| S1D codebook | §1–§3 | clarifications only; "語意變更：無" |

---

## 2. The AI-output-to-organizational-action (AOA) process

Fix an initiative `j` with consequence class `κ_j` and a configuration `k ∈ K_j`. The AOA process describes how one AI output becomes (or fails to become) an organizational action.

**Definition 2.1 (AOA process).** An AOA process for `(j,k)` is a tuple

```
𝒫_{jk} = ( O_j, Act_j, Λ_j, Z_j, Ω_j ;  𝔇_{jk}, 𝔑_{jk}, ℭ_{jk}, 𝔄_{jk} )
```

- `O_j`: the set of AI outputs (risk estimate, recommendation, generated artefact, executed action); `Act_j`: organizational actions, containing the null action `a_∅` (status quo / no AI-induced action).
- `Λ_j`: roles; `Z_j`: signals visible at action time; `Ω_j`: hidden outcome classes (42 §2).
- `𝔇, 𝔑, ℭ, 𝔄`: the four mechanism objects defined below. Everything else (costs, volumes, resource use, capability state, ledgers) is **mechanism-neutral** (Definition 2.6).

The process is evaluated per event: an output `o` is produced, a signal `z` is visible, the hidden outcome `ω` is drawn from `P_j(z,ω|k)`, a role `ℓ` is exposed with `π_j(ℓ|k)`, a response `r ∈ R ∪ {NA}` occurs, and the path value `f_j(k,ℓ,z,ω,r)` is realized ((X1), (V1)).

**Definition 2.2 (M1: decision-right structure).** `𝔇_{jk} = (Agt, Rt, Auth, Eff, Acc, Pol)` with

- `Rt = {authorize, approve, override, stop, change-authorization}`;
- `Auth ⊆ Agt × Rt × Scope`: the **formal** (deontic) relation "agent `α` holds right `ρt` over the transition `o ↦ a` in scope `σ`";
- `Eff : Auth → {0,1}`: whether a formal right is **effective** — the holder has pre-action information, time, and a real veto (42 §3.2 `Eff_H`, after Aghion & Tirole, 1997; Elish, 2019);
- `Acc : (Act ∪ Fail) → Agt`: the accountable agent for actions and failure events;
- `Pol`: the enterprise policy boundary that generates admissible right structures (`γ ∈ Γ`, `Allow_γ`, `J^must_γ`, `J^forbid_γ`, `G_j(γ)`, `ē_j^γ`, `Legal_jk`).

**Object of M1:** *who may make the transition `o ↦ a` happen, prevent it, stop it, or change who may — and who answers for it.* Its values are permissions and obligations, not behaviours.

v2.2 representation (42 §3.1, §5): `γ`, `Allow_γ(j,k)` (F3), `G_j(γ) ≥ G^req(A_k,κ_j)` (F5c), `H_k ≥ H^req_γ(A_k,κ_j)` (F5a), `Eff_H(j,k)` (F6), `ē_j^γ` (F9), `Legal_jk` (F2), `J^must_γ` (F10), `ΔC^gov(γ)` in (OBJ-E). The ordinal `H_k` encodes "which rights a human holds at which point" (41 §5.1: `H_k = 3` = stop/rollback right, G16).

**Definition 2.3 (M2: routing structure).** `𝔑_{jk} = (G_k, route_k, X_k, fb_k)` with

- `G_k = (V, E)`: a directed graph of decision/action nodes (systems, units, roles) with a source node `v_AI` and terminal action nodes; edges are handoffs;
- `route_k : O_j × Z_j → Paths(G_k)`: the nominal path an output takes to an action node (routing depth = 42 `WI_k`);
- `X_k ⊆ O_j × Z_j`: the exception predicate (off-nominal outputs/signals) and the exception path assigned to it;
- `fb_k : Fail → Paths(G_k) ∪ {⊥}`: fallback / rollback / recovery paths for failure states (`⊥` = no recovery path; 42 `FB_jk = 1[fb_k ≠ ⊥]`).

**Object of M2:** *where the output goes, across which handoffs, and how the process is caught and restored when it leaves the nominal path.* Its values are paths and recovery maps.

v2.2: `WI_k ≥ WI^req_γ(A_k,κ_j)` (F5b), `FB_jk` (F7: required when `A_k ≥ 2`), integration/rollback cost in `C^impl_jk(s)`, engineering hours `a^ENG_jk(s)` in (R1)/(R1′).

**Definition 2.4 (M3: human–AI role and response policy).** `ℭ_{jk} = (m_k, A_k, σ_k, agg_k, ρ_{jk})` with

- `m_k ∈ {HumanOnly, AI→Human, Human→AI, Aggregation, Delegated, BoundedExecution}` (configuration type) and `A_k` the ordinal autonomy depth;
- `σ_k`: the sequence in which human and AI contributions occur at a node (who proposes, who decides); `agg_k`: the combination rule (including score-to-choice thresholds `τ_k`, G10);
- `ρ_{jk}(r | z, ℓ, s_j)`: the response kernel — how role `ℓ` **actually** responds given visible `z` (`r ∈ {Use, Verify, Modify, Escalate, Reject, Bypass}`), with `ω` excluded from the conditioning set (42 §6); `π_j(ℓ|k)` the exposure law.

**Object of M3:** *what each actor contributes at a node, in which order, how contributions are combined, and how people actually behave given what they can see.* Its values are divisions of cognitive labour and behavioural kernels.

v2.2: `Cons(A_k,m_k)` (F8), `ρ, π` (and, through `A_k`, the keys of every requirement table) in (X1); `ρ^design/ρ^obs/ρ^cf` and VRG / design-response regret (42 §14 Q6); Model D only if T1–T5 hold.

**Definition 2.5 (M4: assurance predicate).** `𝔄_{jk} = (Ev, ev_k, Accpt_γ, Prov)` with

- `Ev`: a set of evidence states (pre-deployment validation, operational monitoring, triggered revalidation, auditability, explanation usability);
- `ev_k ∈ Ev`: the evidence state configuration `k` provides (42 `EA_k` for EA-V; `EAX_k` for explanation usability);
- `Accpt_γ : Ev × A × κ → {0,1}`: the acceptability predicate — whether use at depth `A` in class `κ` is acceptable given the evidence (42 `1[EA_k ≥ EA^req_γ(A_k,κ_j)]`, F5d);
- `Prov`: the enterprise-level assurance of the configuration decision itself (shared evaluation capability `y_EVAL ∈ Pre(j,k)` via (F4); provenance and robustness class in the output contract, 42 §18; G05).

**Object of M4:** *what must be known, and documented, about the output's fitness for this decision before (and while) its use is acceptable.* Its values are epistemic states and acceptance predicates — not outcomes. In v2.2 the outcome law `P(z,ω|k)` may differ by EA level "only with evidence" (41 G06) and `EAX` enters only through `ρ` (42 §6); neither is a monotone risk-reduction term.

**Definition 2.6 (mechanism-neutral layers).** The following are not mechanisms in the G→M sense:
(a) **F5 architecture** (41 §5.1 "企業架構，非 gap 推導"): `y`, `y^loc`, `Pre(j,k)`, `R_j(s)`, `D_j(s)`, `F_c`, `δ`, capability source state `s_j`;
(b) **economic primitives**: `N_jk`, `v, l, c, t, t^REV, λ`, `I^sev`, `C^impl` amounts, `Ā^h`, `ΔK̄^REV_u`;
(c) **organizational form** (42 §11): who chooses the configuration (`A, C0, A+, B, C, D`), envelopes `e_u`, ledger splits `v^u/v^x`, chargeback `τ`, `C^{impl,x}`.

Note the two distinct levels of "decision rights": M1 governs rights over the **output-to-action transition** (operational level, inside `𝒫_{jk}`); organizational form governs rights over the **choice of `k` itself** (design level, outside `𝒫_{jk}`). Both are decision-rights questions in the sense of Aghion & Tirole (1997) and Sambamurthy & Zmud (1999), but the object differs; v2.2 keeps them in different places (§5 vs §11), and this theory follows it.

### 2.7 How the four objects enter v2.2 (composition)

For fixed `(y, y^loc, γ; θ)`:

```
Φ_jk = Φ^{M1}_jk · Φ^{M2}_jk · Φ^{M3}_jk · Φ^{M4}_jk · Φ^{F5}_jk            (factorization of 42 §5; (F2) Legal_jk is placed in Φ^{M1}, consistent with Def 2.2 `Pol ∋ Legal_jk` and Lemma COV — T7 fix per Q/11 A9; the earlier separate Φ^{Leg} factor is removed)
  Φ^{M1} = Legal_jk (F2) · Allow_γ(j,k)·1[j∉J^forbid ∨ k=0] · 1[H_k ≥ H^req_γ(A_k,κ_j)] · 1[G_j(γ) ≥ G^req(A_k,κ_j)] · Φ^(F6) · Φ^(F9)
  Φ^{M2} = 1[WI_k ≥ WI^req_γ(A_k,κ_j)] · Φ^(F7)
  Φ^{M3} = Cons(A_k, m_k)
  Φ^{M4} = 1[EA_k ≥ EA^req_γ(A_k,κ_j)]   (· the y_EVAL factor of (F4) when EA_k ≥ EA^cap: Level-1 M4 expressed through F5)
  Φ^{F5} = Π_{c∈Pre(j,k)\{EVAL}} ȳ_jc · 1[R_j(s_j) ≥ R^req(A_k)] · 1[D_j(s_j) ≥ D^req(A_k)]
value:  g_jk = E_jk[f]  with the kernel ρ (M3), exposure π (M3), outcome law P (neutral; may be EA-keyed with evidence), EAX as ρ-key (M4→M3 channel)
```

Two structural facts follow directly from 42 §5 and §6:

- **(S1) Cross-mechanism keying.** Every same-construct requirement is a relation between an M3 coordinate (`A_k`) and another mechanism's coordinate (`H_k`, `WI_k`, `EA_k`, `G_j(γ)`), indexed by `κ_j`. The requirement tables are therefore the formal locus of the boundaries in §3: they say "at autonomy depth `A`, the M1/M2/M4 object must be at least …".
- **(S2) Value asymmetry.** In the static full-information model, M3 is the only mechanism that enters the **value** term `g_jk` structurally (through `ρ, π`); M1, M2 and M4 enter feasibility, costs (`C^impl`, `ΔC^gov`), and value only through evidence-conditional lookups (`P` by EA; `ρ` by EAX or `y_CHG`). This is consistent with P7: in Model B the requirement block cannot add priced value (`RE ≤ 0`); their in-model positive value comes only from enablement, robust feasibility, or (Model C only) screening (P8).

---

## 3. Boundaries defined by the object of the decision

**Object test.** For a decision question `Q` about an AOA process, let `obj(Q)` be the component of `(𝔇, 𝔑, ℭ, 𝔄)` that must change to answer `Q` differently, **holding the other three fixed**. `Q` is classified to the mechanism whose component is `obj(Q)`. If two components must change jointly, `Q` is a **bridge** (primary = the component whose change is the reason for the question; secondary = the enabling one), as in 41 (G08 M1/M3, G16 M1/M2). Keywords ("evaluation", "accountability", "assurance" — 26 §4 rule 3) never decide the class.

| Pair | M_a object | M_b object | Discriminating counterfactual | v2.2 elements | Bridge cases (41) |
|---|---|---|---|---|---|
| **M1/M3** | deontic relation `Auth`, `Eff`, `Acc`: who *may* approve/override/stop and who answers | sequencing `σ`, aggregation `agg`, kernel `ρ`: who *does* what, and how people *actually* respond | Change who holds the veto while keeping sequence and observed behaviour fixed → M1. Change who proposes/decides first, or how often reviewers modify, while keeping rights fixed → M3. "Formal right without effective control" is M1 (`Eff`); "reviewers rubber-stamp" is M3 (`ρ(Use|z)` high) — the same observed outcome can arise from either, but the enterprise decision variable differs (`Eff_H` vs `m_k`/`ρ`). | M1: `H_k, Eff_H, G_j(γ)`; M3: `m_k, A_k, ρ`; link: `Cons(A,m)` and all `X^req(A,κ)` tables | G08 (M1 primary: may a recommendation become an action without sign-off; M3 secondary: modify/use frequencies) |
| **M1/M4** | who may authorize | what evidence must exist before anyone may authorize | Same signer, more/less validation required → M4. Same evidence, different signer or veto → M1. Both are `(A,κ)`-keyed thresholds of identical form (`H^req` vs `EA^req`) — the object, not the form, separates them. | M1: (F5a)(F5c)(F6); M4: (F5d), `y_EVAL` | G05 (M4 primary at Level 1, M1 secondary: assurance of the allocation decision itself) |
| **M2/M3** | **inter-node** topology: where `o` goes, handoffs, exception and recovery paths | **intra-node** composition and behaviour | Does the change alter the path graph `G_k`/`route_k`/`fb_k` (M2) or what happens at a node given the same path (M3)? `Escalate` as a *response* is M3 (`ρ(Escalate|z)`); *where* escalation routes to, and whether it is caught, is M2 (`X_k`). | M2: `WI_k, FB_jk`; M3: `m_k, ρ` | G14 (M2 primary: does the risk output reach a decision node at all; M3 secondary) |
| **M2/M4** | what happens to the flow after a failure (recovery) | what is known about fitness before/while used (validation, monitoring) | Monitoring that *detects* drift is M4 (`ev_k`); the path that *restores* operation once detected is M2 (`fb_k`). Removing monitoring but keeping rollback changes only M4; removing rollback but keeping monitoring changes only M2 (§5 Π_¬M2, Π_¬M4). | M2: (F7), (F5b); M4: (F5d) | G03 (M2 primary, M1 secondary — exception handling of executed actions); G06 (M4 only) |
| **M3/M4** | how humans respond / combine with AI | properties of the evidence/artefact offered to them | Explanation **usability** (`EAX_k`) is an M4 property of the artefact; its **effect** is realized only through M3's kernel (`ρ` keyed by EAX; 42 §6). A threshold `τ` mapping scores to choices is M3 (`agg_k`); the calibration evidence that makes `P(z,ω|k_τ)` identifiable is M4/data (G10, see §7.3). | M3: `ρ, agg_k`; M4: `EAX_k` (ρ-key only), `EA_k` | G13, G15 (M4 primary, M3 secondary); G01 (M3 primary, M4 secondary) |
| **M1/M2** (added for completeness) | who may stop/reverse | whether stop/reverse is executable and how operation is restored | A stop right with no recovery path (`H_k = 3`, `FB_jk = 0`) is the canonical bridge: M1 is satisfied formally, M2 fails. | (F5a) with `A=3`; (F7) | G16 (M1 primary, M2 secondary) |

**Boundary to the mechanism-neutral layers.** (i) M1 vs organizational form: rights over `o ↦ a` (M1) vs rights over the choice of `k` (form; Models A–D). (ii) M4 vs F5: per-configuration evidence `EA_k` (M4) vs enterprise capability `y_EVAL` (F5 carrier of Level-1 M4). (iii) M2 vs F5: routing/recovery design (M2) vs data/interface readiness levels `R_j(s_j), D_j(s_j)` determined by capability state (F5; 41 §5.2: "D 是企業平台能力，不是部門配置選擇").

---

## 4. What "represent" means

**Definition 4.1 (enterprise AI decision problem, static).** A problem is `Π = (K, Φ^Π, V^Π)` with a finite alternative set `K` (configurations of one or more initiatives), a feasibility map `Φ^Π : K → {0,1}` and a value map `V^Π : K → ℝ`. Its solution correspondence is `S^Π = argmax{V^Π(k) : Φ^Π(k) = 1}` (full tie set; no tie-breaking is needed because representation is required for the whole correspondence, and for Φ and V separately).

**Definition 4.2 (mechanism schema and projection).** Each alternative `k` carries coordinates `(d_k, n_k, c_k, a_k, ν_k)` for `𝔇, 𝔑, ℭ, 𝔄` and the mechanism-neutral layer. For `S ⊆ {M1,M2,M3,M4}` let `π_S(k)` be the tuple of the `S`-coordinates together with `ν_k`.

**Definition 4.3 (S-representability).** `S` represents `Π` iff there exist functions `φ_S, v_S` such that `Φ^Π(k) = φ_S(π_S(k))` and `V^Π(k) = v_S(π_S(k))` for all `k ∈ K` — i.e., `Φ^Π` and `V^Π` are measurable with respect to the partition of `K` induced by `π_S`. (Equivalently: no two alternatives with the same `π_S` image are treated differently by `Π`.)

**Typing axioms (needed — without them the claim is false).** If coordinates could be recoded freely, any finite distinction could be stuffed into one label (e.g., enlarge the domain of `m_k` to also record veto rights), and every mechanism would be "reducible". Irreducibility is therefore a statement about **object-typed** coordinates. *(Terminology, T7 per Q/11 A9: in this document "irreducibility" / IRR is only the name of the property "non-redundant under typing axioms T1–T4 relative to the v2.2 attribute schema"; it must not be paraphrased as "irreducible" without that qualifier.)*

- **T1 (M1 typing).** `d_k` ranges only over right structures `(Auth, Eff, Acc, Pol)`; it is invariant under changes of paths, behaviour and evidence.
- **T2 (M2 typing).** `n_k` ranges only over `(G_k, route_k, X_k, fb_k)`.
- **T3 (M3 typing).** `c_k` ranges only over `(m_k, A_k, σ_k, agg_k, ρ_jk, π_j)`.
- **T4 (M4 typing).** `a_k` ranges only over `(ev_k, Accpt_γ, Prov)`.

These axioms are exactly the object definitions of §2 and the "唯一職責" column of 41 §5.1; they are a modelling commitment, not an empirical finding.

---

## 5. Ablation and non-redundancy (IRR, under T1–T4) [T8-fix]

### 5.1 Proposition IRR — non-redundancy under typing axioms T1–T4 (TYPE C, definitional; proof complete under T1–T4)

*For each `i ∈ {1,2,3,4}` there exists a problem `Π_{¬Mi}` that is an instance of the v2.2 static model (one initiative, Model B, `θ` fixed and fully identified, all ordinal comparisons by `≥` only) such that `{M1,…,M4} \ {Mi}` does not represent `Π_{¬Mi}` while `{M1,…,M4}` does.*

*Proof.* By Definition 4.3, it suffices to exhibit two alternatives `k¹, k²` with `π_{S_i}(k¹) = π_{S_i}(k²)` for `S_i = {M1..M4} \ {Mi}` and `Φ^Π(k¹) ≠ Φ^Π(k²)` or `V^Π(k¹) ≠ V^Π(k²)`; then no `φ_{S_i}, v_{S_i}` can exist. Representability by the full set holds because in each construction `k¹ ≠ k²` differ in an `Mi` coordinate and `Φ, V` are, by construction, functions of the full coordinate tuple (they are the v2.2 maps). The four constructions below share: `κ_j = high`; requirement tables `H^req(A,high) = WI^req(A,high) = EA^req(A,high) = 2` for `A ≥ 2` and `0` otherwise; `Cons = {(0,HumanOnly), (2,AI→Human), (2,Aggregation), (3,BoundedExecution), (3,Delegated)}`; mechanism-neutral coordinates identical across each pair (same `N`, `C^impl`, `a^h`, `Pre`, `R/D` levels, `Legal = 1`, `Allow = 1`); `P(correct) = 0.9, P(wrong) = 0.1`; path values `f(Verify,·) = (7, −3)`, `f(Use,·) = (10, −50)`.

- **Π_¬M1 (rights).** `k¹ = (H=3, Eff_H=1; WI=3, FB=1; m=AI→Human, A=2, ρ=Verify; EA=3)`, `k²` identical except `Eff_H = 0` (nominal post-hoc sign-off without pre-action information, time or real veto). `π_{M2,M3,M4}(k¹) = π_{M2,M3,M4}(k²)`; values equal (`6.0 = 6.0`, because behaviour `ρ` is the same); `Φ(k¹) = 1`, `Φ(k²) = 0` by (F6) since `H^req = 2`. The distinction is about a right, not about behaviour, routing or evidence — Aghion & Tirole's formal-vs-real authority separation and Elish's (2019) misallocation of responsibility under limited control (TYPE B anchors).
- **Π_¬M2 (routing/recovery).** `k²` = `k¹` with `FB = 0`. Same rights (including the stop right `H = 3`), same roles/behaviour, same evidence; `Φ(k²) = 0` by (F7) since `A = 2`. A stop right without a recovery path (G16 bridge) cannot be expressed by M1, M3 or M4 coordinates.
- **Π_¬M3 (configuration/response), two variants.** (a) feasibility: `k¹ = (…; m=BoundedExecution, A=3, ρ=Use; …)`, `k² = (…; m=AI→Human, A=3, ρ=Use; …)`; `Φ(k²) = 0` by (F8). (b) value: `k¹ = (…; m=AI→Human, A=2, ρ=Verify; …)`, `k² = (…; m=Aggregation, A=2, ρ=Use; …)`, both feasible; `V(k¹) = 0.9·7 + 0.1·(−3) = 6.0`, `V(k²) = 0.9·10 + 0.1·(−50) = 4.0`; `S^Π = {k¹}`. Without M3 the expectation operator (X1) has no `ρ` to vary, so the value distinction — and with it VRG and design-response regret (42 §14 Q6) — is not expressible.
- **Π_¬M4 (assurance).** `k²` = `k¹` with `EA = 1`. Same rights, routing, roles and the **same outcome law `P`** (the evidence state is changed, not the true fitness); `V` equal; `Φ(k²) = 0` by (F5d). Hence M4 cannot be absorbed into the outcome law: the acceptability predicate binds on *documented knowledge* even when the modeller's `P` is unchanged.

In each case the two alternatives coincide on all remaining-mechanism coordinates and on the neutral layer, and `Π` distinguishes them. ∎

**Witness.** `Q\witness_parts\w_mech.py :: witness_mech_ablation()` re-implements (F5a)(F5b)(F5d)(F6)(F7)(F8) and (X1) from the definitions (no import from 51) and checks, for all five pairs, projection equality on the remaining mechanisms and `Π`-distinction: `pass = True` (failed flags for `k²`: F6, F7, F8, F5d; M3_value 6.0 vs 4.0). This is a computational witness of the constructions, not the proof.

### 5.2 Scope of Proposition IRR (what it does and does not say)

0. **What IRR is (T7 per Q/11 A9).** Under Definition 4.3 and T1–T4, IRR is equivalent to: "each of the four attribute groups contains at least one attribute that some v2.2 feasibility or value map reads non-trivially"; the constructions vary that attribute and hold the rest fixed. This is a **non-redundancy (no dead variable) property of the v2.2 schema under a chosen partition**, and it holds for *any* partition of the read attributes into four non-empty classes. The typing carries the conclusion: e.g. `Eff_H` ("pre-action information, enough time, real veto", 42 §3.2) could as naturally be typed M2 (does the route deliver the output before action?) or M4 (evidence); retyping it to M2 would leave M1's non-redundancy resting on `H_k` alone, which is itself an M1/M2 bridge (G16). IRR therefore does **not** support M1–M4 as a theory of enterprise AI decisions; it only shows that the v2.2 schema has no dead attribute class under T1–T4.

1. It is **relative to the v2.2 attribute schema and T1–T4**. It says the four object types are not mutually substitutable as carriers of v2.2 decision distinctions. It does not say that the world "contains" four mechanisms.
2. Each `Π_{¬Mi}` is an admissible v2.2 instance: costs being equal across `k¹,k²` is a parameter choice, permitted because all parameters are free in `Θ` (every cell is UNIDENTIFIED in the canonical model). If, in a particular enterprise, rollback preparation always has a distinct cost, the M2 distinction is *additionally* visible in the neutral layer; that does not reduce M2 — the feasibility distinction remains.
3. It is invariant under strictly increasing ordinal relabelling (P5): every construction uses only `≥` comparisons and lookups.
4. It is **not** contradicted by P7: P7 says relaxing a requirement weakly increases `F^{B*}`; IRR concerns which coordinates the requirement must be stated on.
5. It does not use Model C, envelopes or Lemma E′; with one aligned unit and a non-binding envelope, C reproduces B (P2), so the constructions transfer to C unchanged.
6. Constructive example vs theorem: the proposition is proven; the numerical values are illustrative only (SIMULATED_ONLY).

---

## 6. Sufficiency

### 6.1 Why non-redundancy (IRR, under T1–T4) ≠ sufficiency [T8-fix]

Non-redundancy (IRR, under T1–T4) [T8-fix] says each mechanism is **necessary** for some problem. Sufficiency says the four **jointly cover every** problem in a universe `𝒰`: for all `Π ∈ 𝒰`, `Π` is representable by `{M1..M4}` plus the neutral layer. Sufficiency is a universal statement and can only be proven over a **closed, formally specified** universe.

### 6.2 Lemma COV (TYPE C; proof by exhaustive enumeration of 42 v2.2 static)

Let `𝒰_v22` be the class of static, single-period, full-information problems expressible in 42 v2.2 §2–§12 (configurations `k ∈ K_j` with attributes `(A,H,WI,EA,EAX,m[,τ])`, feasibility (F1)–(F10), resources (R1)/(R1′)/(R2), value (X1)/(V1)/(V2)/(OBJ-E)/(OBJ-U), organizational forms A–C).

*Lemma COV.* Every configuration attribute and every feasibility factor of `𝒰_v22` is a function of M1–M4 coordinates, the F5 architecture, the economic primitives, or the organizational form.

*Proof.* Attributes: `H` (M1), `WI` (M2), `A, m, τ` (M3), `EA, EAX` (M4) — 41 §5.1. Feasibility factors: (F2) `Legal` and (F3) `Allow_γ`, (F5a), (F5c), (F6), (F9) are M1 (42 §5 column; 41 §5.1 places `Legal_jk`, `ē`, `γ` in F1); (F10) is labelled "S（以 policy 表達）" in 42 §5 and is carried by the policy profile `γ` (`J^must_γ`; 41 §3 Q2), hence by the M1 policy block; (F5b), (F7) M2; (F8) M3; (F5d) M4; (F4) and (F5e) F5 (with the `y_EVAL` prerequisite as F5 carrier of Level-1 M4); (F1) is structural one-hotness. Value: `π, ρ` M3; `P` neutral (EA-keyed only with evidence); `v,l,c,t,λ,N` economic; `C^impl(s), a^ENG(s)` neutral with M2/M4 cost components. Resources and ledgers: neutral / organizational form. No element is left unassigned. ∎

Combined with Proposition IRR (whose instances lie in `𝒰_v22`): **relative to `𝒰_v22` and T1–T4, {M1,M2,M3,M4} is a set of mechanism types that is non-redundant under typing axioms T1–T4 relative to the v2.2 attribute schema, and jointly sufficient for `𝒰_v22` (internal closure, circular — see caveat), with F5, economic primitives and organizational form as non-mechanism layers.** *(Relabeled T7 per Q/11 A9: "irreducible" replaced.)*

**Circularity caveat (must be stated whenever COV is cited).** `𝒰_v22` was built *from* M1–M4 (41 → 42). COV therefore certifies internal closure (no orphan model element, no missing mechanism inside the model the thesis actually uses), not that M1–M4 capture enterprise AI decision problems at large. It is a consistency result, not an external completeness result.

### 6.3 Global sufficiency: NOT_PROVEN, with named candidate residuals

There is no closed universe of "enterprise AI decision problems". The following candidate problem types are **not** representable in `𝒰_v22` with M1–M4 and are either deliberately excluded or open:

| Candidate residual | Why not in M1–M4 × `𝒰_v22` | Status |
|---|---|---|
| Information asymmetry between enterprise and BU (value of local information) | full-information model; P3 | excluded by design → sidecar `Q\08` |
| Pure accountability allocation (who is blamed) with no change in control, ledger or behaviour | v2.2 represents accountability only through `H_k`/`Eff_H` (a named reviewer with effective control), `ē`, and ledger incidence `l^u/l^x` (organizational form); `Acc` has no free variable of its own | open: representable only if it changes `ρ` (M3) or ledgers; otherwise a gap of the model, not of the taxonomy |
| Learning, sequencing, information acquisition, absorptive capacity | single-period | orthogonal time dimension (§7.4) |
| Vendor/procurement contracts, data rights acquisition | outside 42 §2 sets (59a §3.12.7 treats procurement as candidate engineering facet) | open |
| AI-to-AI chains (agentic outputs consumed by other AI) | expressible as M2 paths with AI nodes, but not tested | open; conjecturally M2 |
| Strategic alignment, change capability | absorbed into `γ` (`J^must`, `J^forbid`), `v`, `y_CHG`, M5 (41 §3 Q2) | covered by non-mechanism layers |

**Decision: `M1_M4_MINIMAL_SUFFICIENCY = PARTIAL`.** Justification: necessity (IRR) is proven under explicit typing axioms; sufficiency is proven only over `𝒰_v22`, which is circular with respect to the derivation of M1–M4; global sufficiency is NOT_PROVEN and at least one residual (information asymmetry) is known to lie outside. **Downgraded label for the manuscript (relabeled T7 per Q/11 A9):** "M1–M4 form a *working set of mechanism types that is non-redundant under typing axioms T1–T4 relative to the v2.2 attribute schema, and jointly sufficient for the static enterprise model (v2.2; internal closure, circular)*; with respect to enterprise AI decision problems in general they are a *conceptual decomposition / mechanism taxonomy* whose completeness is not claimed." Neither "irreducible" nor "minimal sufficient" should be used without these qualifiers.

---

## 7. NONE, EVIDENCE_ONLY, DATA_GATED, LONGITUDINAL

### 7.1 Is NONE a classification-failure signal?

No. 26 §3 defines NONE as: an identifiable enterprise decision interface exists (Q1 = YES), but none of M1–M4, LONGITUDINAL, DATA_GATED expresses it, and Q5 must state the uncaptured decision; it is explicitly not for ties (AMBIGUOUS) or for "no interface" (EVIDENCE_ONLY); the crosswalk maps it to `OTHER (new_construct_required = YES)` (26 §5). Formally:

- **AMBIGUOUS** signals a **boundary** problem (the object test of §3 does not separate two mechanisms for that item) — this *is* the classification-interpretability signal.
- **NONE** signals a **coverage** anomaly: a candidate problem outside the working set. It is the item-level analogue of a counterexample to sufficiency.
- But NONE is **not a sufficiency test**: (i) the 16 items are robust depletion cells selected by network statistics, not a sample from any universe of enterprise decision problems, so the absence of NONE cannot establish sufficiency; (ii) a NONE answer is a coder judgment that must still be checked against `𝒰_v22`: if the Q5 decision is expressible through F5, organizational form or economic primitives, it is a mapping-only issue; if not, it is a candidate residual for §6.3 (analogous to 41 §7 rule 3 for G04).

### 7.2 Why EVIDENCE_ONLY is not forced into M1–M4

The G→M map is a **partial** function `μ : 𝒢 ⇀ {M1..M4}` whose domain is the set of pairings that point to a pairing-specific enterprise decision (41 §0 rule 4; 26 §2 "specific to this pairing"; S1D "組合特有"). The mechanism objects of §2 act on an AOA process; a pairing with no pairing-specific decision has no object for them to act on. Forcing it into M1–M4 would (i) violate the object test (the classification would be driven by topical words — 26 §4 rule 3), (ii) duplicate variables already present for every AI function feeding that decision family (41 G04 reason), and (iii) make the G→M map total by fiat, which would let network depletion statistics masquerade as enterprise problems (41 §0 rule 2). EVIDENCE_ONLY is therefore the out-of-domain marker of `μ`; sufficiency is about covering interfaces, not pairings.

### 7.3 DATA_GATED: mechanism or identification condition?

**Identification condition.** Formally, for a data predicate `δ_D ∈ {0,1}` (e.g., score distribution + true labels + retraceable threshold rule, G10):

```
M_j^eff = M_j ∪ { k_τ : τ ∈ T_j }   if δ_D = 1      (k_τ carries an M3 aggregation rule agg = threshold τ)
M_j^eff = M_j                         if δ_D = 0      (k_τ not imputed; 42 §1.3 rule 5)
```

The gate changes the **domain** of the mechanism functions, not their type: the gated variable `k_τ` is an M3 object (score-to-choice rule) whose outcome law `P(z,ω|k_τ)` must be identified from data (an M4/data question). This matches the codebook: test (b) precedes (c), and the crosswalk maps DATA_GATED to the Q4 mechanism when one is given (26 §5). It also matches v2.2's missing-value semantics: a configuration whose lookup cannot be identified is excluded (`RESTRICTED_SOLVE`) and affected decision elements become `UNIDENTIFIED` (42 §13.4).

Distinguish two "data" notions that v2.2 keeps apart:
- **Operational data readiness** `R_j(s_j) ≥ R^req(A_k)`, `D_j(s_j) ≥ D^req(A_k)` (F5e): an F5 feasibility threshold, **state-dependent** on the capability source state `s_j ∈ {∅, S, L}` and evaluated for every `k` incl. `k = 0` (42 §5 l.202). It asks whether the *enterprise* can run the configuration.
- **Identification data** (DATA_GATED): whether the *researcher* can identify the parameters that make the configuration a well-defined decision variable.
The first is part of the model; the second is a precondition for including part of the model. Neither is a mechanism.

### 7.4 LONGITUDINAL: M5 mechanism or orthogonal time dimension?

**Orthogonal time × information-state dimension.** v2.2 §16 defines the state `ξ_t = (y_t, Θ_t, Ξ_t)` and the transition `b_{t+1} = Π(b_t, O_t)` (D1), with `b = (y, γ, e)`, and information acquisition `Θ_{t+1} ⊂ Θ_t` (D2). The transition acts on the **whole** leader decision, which already contains M1 elements (`γ`), F5 elements (`y`) and envelopes. Every mechanism has a temporal counterpart (rights revised after incidents — M1; routing re-engineered — M2; `ρ` drifting with experience — M3; revalidation — M4). Therefore "M5" is not a fifth coordinate of the configuration tuple; it is the time indexing and the transition/information operator over the static state space. What is genuinely irreducible to the static model is the dependence of value on `Θ_{t+1}` (information acquisition) and on sequencing — the static VOI diagnostic (42 §13.5) is only its shadow, and option value is excluded from the static ledger (42 §7.2).

Consequences: (i) keep "M5" as a label (41, 59a use it) but describe it as "dynamic extension of M1–M4 × F5", not as a fifth parallel mechanism; (ii) the codebook already treats it orthogonally (test (a) first; the M1–M4 category may go in Q4), so no instrument change is implied; (iii) Proposition IRR and Lemma COV are statements about the static section `t` fixed and are unaffected by M5. If the AI-pilot disagreement on G11 (M4/static vs M5/dynamic) were confirmed by humans, it would be consistent with this reading: G11's object (evaluation results feeding allocation) is an M4-type object observed over time.

---

## 8. What V1 tests (and what it does not)

V1 (59a §3.9.3; 26) measures **inter-rater agreement** of three independent human coders on Q2 (Krippendorff α, nominal; pairwise κ), and only after unsealing compares the adjudicated codes with the researcher key. Therefore:

- V1 tests the **inter-rater interpretability of the G→M mapping** under the frozen category definitions (whether the boundaries of §3 are usable by independent people on these 16 items).
- V1 does **not** test non-redundancy (IRR, under T1–T4) [T8-fix] (a logical property proven in §5 under T1–T4), and does **not** test sufficiency (the 16 items are not a sample of a universe; agreement on categories is silent on what is missing). A high α would not establish minimal sufficiency; a low α would not refute non-redundancy (IRR, under T1–T4) [T8-fix] — it would indicate that the object test is not reliably applied to these stimuli.
- The only V1 outputs bearing on this document are: AMBIGUOUS rates (boundary interpretability, §3), NONE answers with Q5 text (coverage anomalies, §7.1), and LONGITUDINAL/DATA_GATED vs Q4 patterns (orthogonality, §7.3–7.4). None of these exist yet: **no human coding has occurred**, and this document neither uses nor anticipates any result.
- Fallback rules (41 §7; 59a §3.9.5) remain in force: model elements' reasons for existence (enterprise architecture, Lemma COV) are stated separately from gap support.

---

## 9. Literature positioning (TYPE A / B / C)

Only works in the 59a reference list are cited. "TYPE A" = the literature directly establishes the stated claim; "TYPE B" = conceptual anchor; "TYPE C" = new formal result of this thesis (never written as "according to X").

| Stream | Work (in 59a list) | Claim it supports here | Type |
|---|---|---|---|
| Decision rights; formal vs real authority | Aghion & Tirole (1997) | formal authority and real authority can diverge → separate `Auth` from `Eff` (`G_j(γ)`, `H_k` vs `Eff_H`) | A for the general separation; B for its use in AI configurations |
| | Elish (2019) | responsibility can be attributed to humans with limited control ("moral crumple zones") → `Eff`, `Acc` distinction; Π_¬M1 | B |
| | Green (2022) | policies requiring human oversight need not yield effective oversight | B |
| IT governance | Sambamurthy & Zmud (1999); A. E. Brown & Grant (2005) | governance as allocation of decision rights (and accountabilities), contingent on context → `Γ` as a finite policy menu; M1 vs organizational form | B |
| | Weill & Ross (2004) | only as secondary citation via Brown & Grant (2005) — METADATA_ONLY in Appendix B N6 | **to verify; do not cite directly** |
| | Papagiannidis et al. (2025); NIST (2023); ISO/IEC 42001 (2023) | structural/procedural/relational governance practices; structural references only | B (never a parameter source) |
| Human–AI collaboration | Parasuraman, Sheridan & Wickens (2000) | types and levels of automation → `A_k`, `m_k` | B |
| | Shrestha et al. (2019) | full delegation, sequential (both directions), aggregation structures → `m_k` | B |
| | Raisch & Krakowski (2021) | automation and augmentation are not cleanly separable → `m_k × A_k` not binary | B |
| | Vaccaro et al. (2024) | human–AI combinations not on average better than the better of the two → `P, ρ` looked up, not assumed | A (for the meta-analytic average); B for the modelling consequence |
| | Dietvorst et al. (2015); Logg et al. (2019); Lebovitz et al. (2022); Kellogg et al. (2020) | response direction is not fixed (aversion, appreciation, engagement under opacity, resistance) → `ρ` with Reject/Bypass | A (for the respective findings); B for `ρ` |
| | Bansal et al. (2021) | explanations raise acceptance regardless of correctness → EAX only as `ρ`-key (M4→M3 channel) | A for the finding; B for the boundary M3/M4 |
| Workflow / routing | Amershi et al. (2019); Sculley et al. (2015) | integration and maintenance are substantive and costly → M2 costs in `C^impl` | B |
| AI assurance | Breck et al. (2017); Raji et al. (2020); Mökander et al. (2021) | testing, monitoring, internal audit as recordable, gradable activities → `ev_k`, `EA_k` | B |
| Information and delegation | Alonso, Dessein & Matouschek (2008) | decentralization can have information advantages excluded by the full-information model → §6.3 residual, `Q\08` | B |
| This thesis | — | AOA formalization (§2), object test (§3), representability (§4), Proposition IRR (§5), Lemma COV + circularity caveat (§6), NONE/EVIDENCE_ONLY/DATA_GATED/LONGITUDINAL status (§7) | **C** |

No literature directly establishes that M1–M4 are non-redundant or sufficient; both are TYPE C (IRR definitional under T1–T4; COV internal and circular).

**Restatement vs genuinely new (T7, consistent with Q/11 A9, §3).** *Restatement / regrouping of v2.2:* the factorization §2.7 (42 §5 "來源機制" column), Lemma COV (enumeration of 42's own element list; circular), S1/S2 (read off 42 §5–6). *Definitional:* Prop IRR (non-redundancy under T1–T4). *Genuinely new (conceptual, TYPE C):* the AOA formalization (§2), the object test and the six-pair boundary table (§3), the representability notion (§4), and the NONE / EVIDENCE_ONLY / DATA_GATED / LONGITUDINAL status analysis (§7). Known anchors for the taxonomy are TYPE B and adequate: IT-governance decision rights (Sambamurthy & Zmud; Brown & Grant, in list) and levels of automation (Parasuraman et al., in list).

**AI-specificity (T7 per Q/11 A11).** This document is where the thesis's AI-specific content lives: the M1–M4 configuration schema, the autonomy-keyed requirement tables `X^req(A,κ)` (S1), and the human-response layer `ρ` (M3; VRG, design-response regret; EAX as a ρ-key, M4 → M3). The portfolio-level results in 02–07 (DL, governance screening, reuse non-monotonicity, robustness scope, VOI, missingness) do not use this structure and hold for any shared-platform IT portfolio. Even `ρ` is automation-generic rather than AI-specific.

---

## 10. Claims register

| ID | Claim | Kind | Status |
|---|---|---|---|
| D-AOA, D-M1…D-M4 | Definitions 2.1–2.6 | definitions | COMPLETE |
| S1, S2 | cross-mechanism keying; value asymmetry (only M3 structural in `g_jk`) | observations derived from 42 §5–6 | follow by inspection |
| IRR | each of M1–M4 necessary for some v2.2 instance (non-redundancy, "no dead attribute class") | proposition (definitional) | PROVEN under T1–T4, relative to v2.2 schema; holds for any partition of the v2.2-read attributes into four non-empty classes, so it does not validate the taxonomy |
| COV | every v2.2 static element assigned | lemma | PROVEN by enumeration; circular w.r.t. derivation |
| SUFF-GLOBAL | M1–M4 sufficient for all enterprise AI decision problems | conjecture | NOT_PROVEN (no closed universe; known residual: information asymmetry) |
| W-MECH | numerical pairs reproduce IRR fibres | computational witness | pass = True (SIMULATED_ONLY) |
| NONE / EO / DG / LONG | §7 interpretations | conceptual (TYPE C) | consistent with 26 crosswalk and order of tests; no instrument change implied |

---

## 11. Relation to P1–P8, Lemma E′ and v2.2 — no contradiction

- No equation, set or proposition of v2.2 is changed. The factorization in §2.7 is a regrouping of 42 §5 by its own "來源機制" column.
- P1, P2, P4, P6, P8, Lemma E′ concern organizational form and leader–follower structure — the neutral layer of Definition 2.6(c); IRR/COV do not interact with them.
- P5 is used (constructions are relabelling-invariant). P7/P8 explain observation S2 (requirement blocks carry no priced value in B; screening value only in C).
- P3 is the boundary that makes information asymmetry a residual (§6.3); its treatment is in `Q\08`, which also does not modify v2.2.

## 12. Integration notes (planning only; REPO not modified)

- 59a §3.9.1: after the interface table, add Definitions 2.2–2.5 in compact form and the object test (§3) as "判準：以決策對象界定機制邊界".
- 59a §3.9.5 or a new §3.9.6: Proposition IRR (statement + one-line fibre argument; full proof to Appendix C), Lemma COV with the circularity caveat, and the PARTIAL sufficiency status with the downgraded label.
- 59a §3.9.3: one sentence: "V1 檢驗的是 G→M 對應的編碼者間可詮釋性，不檢驗 M1–M4 的最小充分性。"
- 59a §5.8.4: add the NONE/AMBIGUOUS distinction (coverage vs boundary signals); §5.8.6: describe M5 as an orthogonal time × information dimension.
