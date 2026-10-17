# 10 — Q1 Manuscript Integration Plan (planning only; the manuscript is NOT edited)

**Pack:** Q1_THEORY_UPGRADE_V1_20261014. **Integrator:** T5. **Date:** 2026-10-15.
**Target manuscript (read-only):** `REPO\claude\r14_merge_v1_8_5_compute_closure\59a_MERGED_MASTER_THESIS_v1_8_5a_CANONICAL.md`. It has 3,135 lines, and every line number below refers to that file. Short quotes are cut at about 120 characters; "…" marks a cut.
**Inputs:** Q/01–08 (theory), Q/09 together with `q1_theory_witnesses.py` (witnesses, `Q1_WITNESS_VERDICT: PASS`), and 42 v2.2 (canonical; its equations are unchanged).

## Rules applied

* **No v2.2 equation, set, proposition statement (P1–P8), Lemma E′ or Lemma R is rewritten.**
  * New material is added as *new, separately labelled* statements: DL-1, GS-I, D1, D3, D6, E.1, R1, G1–G8, IRR, COV, and so on.
  * Appendix C says it "逐字收錄企業模型規格 v2.2" (l.2793). So the new proofs go into a **new** sub-appendix, "C.10 Q1 理論補充（新增，非 v2.2 原文）", and not into C.1–C.9.
* **Status vocabulary for every new item:**
  * theorem / proposition / lemma / corollary: proven in Q/0x;
  * conjecture: NOT_PROVEN;
  * constructive example (witness): SIMULATED_ONLY;
  * empirical hypothesis: untested, needs V7 data.
* **Claim types:**
  * all new formal results are **TYPE C**;
  * literature anchors are **TYPE A or B** and come only from the 59a reference list (l.2419–2688);
  * anything else is marked **TO VERIFY**;
  * no TYPE C result is written as "according to X".
* **Evidence label for each change:**
  * **SAFE**: a formal or wording change that needs no new evidence;
  * **NEEDS-HUMAN**: depends on V1 or other human coding, none of which exists;
  * **NEEDS-ENTERPRISE**: depends on V0/V2/V7 enterprise data, none of which exists;
  * **NEEDS-CITATION-CHECK**: the anchor must be verified first.
* Nothing below claims V7, empirical or enterprise validity. All witnesses are SIMULATED_ONLY constructive examples.

---

## 0. Two manuscript defects already found (fix first; both SAFE)

### D-a. §3.14.3, l.1327, priority level (4): the status-quo rationale is false in general

* **Current text (quote):** "(4) **邊際價值低**：現況結果格的精確度——它在所有候選 portfolio 中以相同方式出現，在 regret 與 VOI 的差分中抵銷；但現況格必須存在。"
* **Why it is wrong:** Q/07 Remark G7 and witness **W8b(iii)**. For one initiative, `φ_j1 − φ_j0 = (g_1 − x) − C^impl`. The status-quo cell `x` decides between k=0 and k=1: in W8b(iii), k=1 is optimal iff `x < 4`. The cell cancels only between portfolios that agree on keeping `j` at the status quo. 42 §13.4 is already consistent with this, since it marks a missing status-quo cell `UNEVALUABLE_INITIATIVE`. Only the 59a priority rationale contradicts it.
* **Proposed replacement (Chinese draft):** "(4) **邊際價值低**：僅限現況基線項 `N_j0 g_j0(ȳ^cur)` 中對所有候選 portfolio 共同、且不影響『維持現況或切換』比較的部分；凡進入 `k = 0` 與 `k ≥ 1` 比較的現況結果格，其精確度可改變決策（附錄 C.10 Remark G7；構造例 W8b），應依第一批資料的 VOI 排入第 (2) 或 (3) 級。"
* **Also check:** whether Appendix C.4 (l.2852–2869) or 4.10.3 repeats the "抵銷" rationale. A grep found it only at l.1327.
* **Status:** SAFE. The change narrows a claim; no evidence is needed.

### D-b. §3.13, l.1277: "both versions are upper bounds" needs "for a fixed candidate set"

* **Current text (quote):** "`sup` 只取區塊頂點時可能高估（解析例：頂點版為 1、真值為 0.5），故同時報告只取頂點與加入內點網格的兩個版本；兩者皆為真值的上界，網格版不大於頂點版。"
* **Why it is incomplete:** Q/05 Props E.1 and E.2 prove the ordering `0 ≤ VOI^true ≤ VOI^grid ≤ VOI^vertex ≤ MMR`, but **only for a fixed candidate set** (which is how 51 `voi_table` behaves). If the robust candidate set is recomputed on the narrowed Θ (adaptive convention), the ordering fails. Witness **W6b**: MMR goes 0 → 1 and VOI_q = −1. A second gap: for probability blocks with ≥ 3 vertices, 51's "interior points" are edge points only, so the grid does not converge to the true value (W6c: ≥ 1/2 against a true 1/3).
* **Proposed insertion after "網格版不大於頂點版":** "（以上次序僅對**固定候選集合**成立〔附錄 C.10 Prop E.1、E.2〕；若縮小 `Θ` 後重新計算 robust 候選集合，MMR 可能上升、VOI 可能為負〔構造例 W6b〕。網格版以等距網格與二頂點混合點構成；機率區塊有三個以上頂點時，只取邊上點的網格不保證收斂到真值〔W6c〕。）"
* **Same qualifier elsewhere:**
  * l.1269 ("對固定候選集合" is already present for MaxRegret; keep it);
  * table 4-20, l.1917;
  * Table 4-11 RQ6 row, l.2217 ("VOI 同時報頂點版與網格版");
  * C.5.
* **Status:** SAFE.

### Additional defects found during this integration (all SAFE)

* **D-c. §5.6, l.2317.** Current text: "P8 同時提出一個可檢驗的實務命題：當預算 envelope 無法阻擋部門的不利選擇時，規則型治理可以替代預算型協調。"
  * Problem: the condition is **necessary, not sufficient** (Q/03 Thm GS-N vs Prop GS-1).
  * Counterexamples: W4c (GSV < 0 although a non-separable reversal is screened), W4d (pairwise screening is insufficient) and W4b (a rule where the envelope already separates).
  * Replace with the Q/03 §9 short form: "當預算 envelope 無法阻擋部門偏好但對企業不利的配置時，篩除該配置的治理要求**可以**回收授權損失——但不超過該損失，且須扣除該要求在集中最適下的代價（GSV = DL_loose − DL_strict − PR_B ≤ DL_loose）。"
* **D-d. §3.14.3, l.1329 stopping rule.** Current text: "停止規則事前登記：MMR ≤ `ε_R`、整體 portfolio 的 Lemma R 證書成立，或所有剩餘區塊的網格 VOI ≤ `ε_R`，三者任一成立即停止". Three problems:
  * (i) The candidate-set convention must be declared. Under re-registration with recomputed candidates, MMR can rise after narrowing (W6b), and a rule-A stop can be withdrawn.
  * (ii) "All remaining grid VOI ≤ ε_R" is a **myopic** rule. In W6e every single-block VOI is 0 while joint identification removes all regret (MMR 1 → 0).
  * (iii) Termination needs finite (discretised) evidence states (Thm E.7); W6f shows non-termination without them.
  * Fix: add "（固定候選集合〔F〕為主、重算候選集合〔Ad〕只作次要診斷並標 `CANDIDATE_SET_EXPANDED`；第三項為短視停止規則，不保證殘餘 regret；需以預先登記的有限證據狀態或步數上限保證終止）".
* **D-e. §3.12.4 P2 remark, l.1138, and §5.6, l.2323.** Current text: "若不利企業的配置需要池化資源，企業可以 envelope 阻止". This is imprecise. A configuration that uses pooled resources, but **no more of each pooled resource** than the enterprise-preferred plan, cannot be blocked (Lemma S: separable ⇔ `a(x^H) ≰ a(x^G)`).
  * Replace with "若不利企業的配置在至少一項池化資源上需要**多於**企業偏好配置的用量".
  * The v2.2 verbatim remark in C.6 (l.2899) is already correct ("在企業必須給予的 envelope 內仍負擔得起"). Leave it unchanged.

---

## 1. Chapter 1 — contribution and RQ wording

| # | Location | Change | Status of new item | Current wording to change | Claim made stronger | Remaining limitation | Evidence |
|---|---|---|---|---|---|---|---|
| 1.1 | §1.3 objective 3, **l.113** | Downgrade "minimal sufficient" | IRR = proposition (proven under typing axioms T1–T4); COV = lemma (proven; circular); global sufficiency = conjecture (NOT_PROVEN) | "將穩健不足呈現收斂為**最小充分**的企業機制與構念架構" → "收斂為一組在型別公設 T1–T4 下對 v2.2 屬性結構非冗餘、且在 v2.2 靜態模型內共同充分（內部封閉、具循環性）的企業機制工作集合（M1–M4；對一般企業 AI 決策問題僅為概念分解，不宣稱完備）" *(T7: "不可化約" replaced per Q/11 A9)* | Non-redundancy of each of M1–M4 under T1–T4 is a proven (definitional) proposition rather than an adjudication; it shows only that the v2.2 schema has no dead attribute class | Sufficiency holds only relative to `𝒰_v22`, which was built from M1–M4 (circularity caveat). Information asymmetry is a known residual | SAFE |
| 1.2 | Table 1-1, RQ4 row, **l.150**, status column | Add "模型內：DL 為零之首佳相對可實施性刻畫（Lemma DL-1，即 Lemma E′ 於首佳之重述）、唯一首佳下的原始條件充要（Cor DL-3）、治理篩選會計恆等式（GS-I）與必要條件（GS-N）" *(T7 relabel per Q/11 A1–A2, A4)* | characterization lemma / corollary / identity / theorem | Append only; RQ4 text (l.134) unchanged | RQ4's "在何種帳本與限制條件下…偏離" gets an exact in-model answer (DL-1, DL-3, DL-6) | The characterization (Lemma DL-1) quantifies over all first-best solutions [T8-fix], so checking it is as hard as solving B; there is no primitive iff | SAFE (empirical part stays NEEDS-ENTERPRISE) |
| 1.3 | Table 1-1, RQ5 row, **l.151** | Add "δ 單調性：B 證明（Thm D1）；C 對齊時證明（Thm D3），否則存在非區間建置區域（Prop D6）" (Thm D1 = explicit form of P4, B part; Thm D3 = restatement of P2 pointwise) [T8-fix] | restatement / proposition (existence) | Append | P4's C caveat becomes sufficient conditions plus an existence result | Conj M2 is open | SAFE |
| 1.4 | Table 1-1, RQ6 row, **l.152** | Add "Lemma R 適用範圍（Thm R1）；VOI 次序僅對固定候選集合（Prop E.1–E.2）" (Thm R1 = restatement of 42 Lemma R) [T8-fix] | restatement / proposition | Append | VOI and robustness claims carry an exact scope | VOI-greedy optimality is NOT_PROVEN | SAFE |
| 1.5 | §1.7.2 theory contribution, **l.178** | Add a fifth point: "本研究在模型內（完全資訊、固定 θ）給出唯一首佳下授權損失的原始條件充要（Cor DL-3）、envelope 只能設上限的結果（DL-6）、治理篩選的必要條件（GS-N）與三種失效型態，並界定共享能力重用、頂點精確性與 VOI 的成立範圍（TYPE C；附錄 C.10）。這些組合層級結果是企業–部門架構的性質，對任何共用平台的 IT 組合皆成立；AI 特定內容在 M1–M4 結構、依自主等級設定的要求表與人員回應層 ρ。" *(T7 per Q/11 A1, A11)* | lemmas / corollaries / theorems | Insert after "…說明為何活躍使用者比例或使用量本身不能被讀成價值。" | New TYPE C formal contribution | Scope is the complete-information, static model at fixed θ; no empirical claim | SAFE |
| 1.6 | §1.7.2 method contribution, **l.180** | Qualify "以集合式不確定性與 regret 進行決策元素層級的穩健性分類" | Thm R1 (restatement of 42 Lemma R) / Prop R3 [T8-fix] | Add "（整個 portfolio 於 Model B 有頂點精確證書；元素層級與 Model C 以列舉／抽樣報告涵蓋率）" | — | Element-level and Model C results are coverage-only | SAFE |
| 1.7 | §1.7.2 practical contribution, **l.182** | No change needed. Optionally add "以及治理要求何時具篩選價值（上界為授權損失）" | — | — | — | Needs V7 | NEEDS-ENTERPRISE for any application |

**Not recommended:** rewording RQ1–RQ6 themselves (l.124–138). The RQs are frozen design text, and the new results answer them inside the model without changing the questions.

---

## 2. Chapter 2 — theory anchors (TYPE A/B only from the reference list)

| # | Location | Anchor to add or keep | Type | Constraint |
|---|---|---|---|---|
| 2.1 | §2.13 bilevel, **l.322–328** | Colson et al. (2007); Dempe (2002); Moore & Bard (1990); Kleinert et al. (2021); Wiesemann et al. (2013) for the leader–follower form, optimistic vs pessimistic selection, and the integer lower level | **TYPE A** | Already in the list. Add one sentence to "對模型的意涵": "DL-1 為 Lemma E′ 於首佳之重述（首佳相對可實施性刻畫引理）；Cor DL-3、envelope 為上限（DL-6）等為本研究的模型內結果（TYPE C），其機制在授權／委任與資本預算文獻中有已知類比（待查證），不屬上述文獻。" *(T7 per Q/11 A1, A10)* |
| 2.2 | §2.9 governance / decision rights, **l.282–288** | Aghion & Tirole (1997): formal vs real authority | **TYPE B** (conceptual only) | Do **not** write "依 Aghion & Tirole，DL…". Their mechanism is informational, while v2.2 is complete-information (P3). Sambamurthy & Zmud (1999), A. E. Brown & Grant (2005), C. V. Brown & Magill (1994) and Tiwana & Konsynski (2010) are TYPE A for the definition of governance as the allocation of decision rights, and TYPE B for the mapping to `(y,γ,e)`. Elish (2019) and Green (2022) are TYPE B for M1 `Eff`/`Acc` |
| 2.3 | §2.9, l.282 | Weill & Ross (2004) | **TO VERIFY** | It is cited only through A. E. Brown & Grant (2005) and is not in the reference list. Keep it as a secondary citation; it must not anchor M1 |
| 2.4 | §2.13 Alonso et al. (2008), l.322, 328 | Information advantage of decentralisation, outside the model | **TYPE B** (boundary) | Also anchor the information-asymmetry sidecar (Q/08) here as future work only |
| 2.5 | §2.13 "(v) regret", l.324 | Savage (1951) for minimax regret | **TYPE B, PARTIAL** (N34 / E3: attribution only via secondary sources) | Ben-Tal et al. (2009) (N32) and Lempert et al. (2003) (N33) are TYPE B for set-based robustness. Lemma 0, E.1–E.10 and the trilemma are TYPE C |
| 2.6 | §2.12, l.318 | Benaroch & Kauffman (1999) | **TYPE B** | Only for the dynamic / option-value layer (SIP is a static-sequential reading, not an option model) |
| 2.7 | §2.8 / §2.10 / §2.11 | Parasuraman et al. (2000), Shrestha et al. (2019), Raisch & Krakowski (2021) → M3; Breck et al. (2017), Raji et al. (2020), Mökander et al. (2021) → M4; Amershi et al. (2019), Sculley et al. (2015) → M2; Vaccaro et al. (2024), Bansal et al. (2021), Dietvorst et al. (2015), Logg et al. (2019), Lebovitz et al. (2022), Kellogg et al. (2020) → `ρ` | **TYPE B** (A only for each work's own finding) | All in the list. They anchor the M1–M4 object definitions (Q/01 §9) |
| 2.8 | New sentence in §2.15 or §2.13 | Principal–agent and optimal-delegation framing: Jensen & Meckling (1976); Holmström (1984); Alonso & Matouschek (2008); Laffont & Martimort (2002); **delegated project choice (Armstrong & Vickers)**; **capital-budget ceilings (Harris & Raviv-type models)** — the last two added per Q/11 A4/A10, details not checked | **TO VERIFY — not in list; do not cite until verified and added** | If added, position them as a contrast: here the loss comes from instrument incompleteness under complete information, not from hidden information or hidden action |
| 2.9 | §2.13 / §3.13 | Monotone comparative statics (Topkis; Milgrom & Shannon); expected VOI (Howard, 1966; Raiffa & Schlaifer, 1961); interval minmax-regret combinatorial optimisation (Kouvelis & Yu, 1997; Averbakh); partial identification (Manski); **menu-dependence of minimax regret (Chernoff; Stoye)**; **complementarity / non-submodularity of information value**; **"more options can hurt" / Braess-type paradoxes**; pessimistic bilevel (Loridan & Morgan) — added per Q/11 A10, details not checked | **TO VERIFY — not in list** | None is needed for any proof (D1, E.x and G.x are proved directly). If cited, they serve as a contrast only (for example, v2.2's VOI is a worst-case MMR reduction, not an expected VOI) |
| 2.10 | §3.14 / Appendix C.10, missingness | Angrist et al. (1996) | **TYPE B, loose** | Only for "identification is assumption-dependent". It does **not** support G1–G8 |

**Status:** SAFE for the wording. Rows 2.8 and 2.9 are NEEDS-CITATION-CHECK before any use. Also add one row to Appendix E for the TO-VERIFY list.

---

## 3. §3.9 — M1–M4 definition (incl. downgraded sufficiency label)

| # | Insertion point | New item | Status | Current wording affected | Stronger claim | Remaining limitation | Evidence |
|---|---|---|---|---|---|---|---|
| 3.1 | §3.9.1, after the I1–I5 table (**after l.673**) | Compact Defs 2.2–2.5 (M1 `𝔇=(Agt,Rt,Auth,Eff,Acc,Pol)`, M2 `𝔑=(G_k,route_k,X_k,fb_k)`, M3 `ℭ=(m_k,A_k,σ_k,agg_k,ρ)`, M4 `𝔄=(Ev,ev_k,Accpt_γ,Prov)`); mechanism-neutral layers (F5 architecture, economic primitives, organizational form); the **object test** "以決策對象界定機制邊界" plus the 6-pair boundary table (Q/01 §3) | definitions (TYPE C) | The "機制" column of the l.665–673 table stays. Add one sentence: keywords never decide the class | Mechanisms are defined by decision object, not by topic words | Typing axioms T1–T4 are a modelling commitment | SAFE |
| 3.2 | New **§3.9.6** "機制的非冗餘性與充分性狀態" (after l.767, before §3.10 l.769) | **Prop IRR** (each Mi is necessary for some v2.2 instance = non-redundancy under T1–T4 relative to the v2.2 schema; definitional, holds for any partition into four non-empty classes; T7 relabel per Q/11 A9); **Lemma COV** (every v2.2 static element is assigned; proven by enumeration) with the **circularity caveat**; **global sufficiency = NOT_PROVEN**, with the named residual list (information asymmetry; pure accountability allocation; vendor/procurement; AI-to-AI chains); constructive example W_MECH_ABL | proposition / lemma / conjecture; witness SIMULATED_ONLY | — | IRR is proven | Label must read "在型別公設 T1–T4 下對 v2.2 屬性結構非冗餘、且在 v2.2 靜態模型內共同充分（內部、循環）的工作集合；一般而言為概念分解（mechanism taxonomy），不宣稱完備". **Never** "irreducible" / "minimal sufficient" without these qualifiers | SAFE |
| 3.3 | §3.9.3 V1 design, **l.751**, end of item (1) | Add "V1 檢驗的是 G→M 對應的編碼者間可詮釋性，不檢驗 M1–M4 的不可化約性（為形式命題）或充分性（16 項不是問題母體的樣本）。" | clarification | — | Prevents V1 from being read as a sufficiency test | — | SAFE (V1 results themselves: NEEDS-HUMAN) |
| 3.4 | §3.9.4 / §5.8.4 | NONE = coverage-anomaly signal, AMBIGUOUS = boundary signal, EVIDENCE_ONLY = out-of-domain marker, DATA_GATED = identification condition (Q/01 §7) | conceptual (TYPE C) | none (codebook unchanged) | — | No human coding exists; nothing may be anticipated | SAFE |
| 3.5 | §3.9.1, I5 row (l.673) and §5.8.6 (l.2379) | "M5 = 靜態 M1–M4 × F5 之上的時間 × 資訊狀態維度（D1/D2 轉移），保留標籤但非第五個平行機制" | conceptual | I5 row: "M5（僅動態）" → add "（正交的時間維度）" | — | — | SAFE |

---

## 4. §3.12.4 — P1–P8 refinements (new labelled results next to the unchanged P-statements)

**Insertion point:** after the P8 bullet (**after l.1143**), add a block "**Q1 補充結果（TYPE C；證明見附錄 C.10）**". The P1–P8 bullets at l.1137–1143 keep their v2.2 content, with only the D-e wording fix in P2's remark sentence (l.1138).

| # | New item | Status | Relation to P | Current wording (quote) and change | Stronger claim | Remaining limitation | Witness |
|---|---|---|---|---|---|---|---|
| 4.1 | **Lemma S** (envelope separability ⇔ `a(x^H) ≰ a(x^G)`); **Lemma DL-1o/DL-1p** (first-best-relative implementability characterization lemma = Lemma E′ at a first best; T7 relabel): DL^m = 0 ⇔ some first-best solution is m-self-enforcing; **Cor DL-2o/2p** (strict reversal necessary for DL_opt; weak reversal for DL_pess); **Cor DL-3** (pairwise iff under a unique first best; Part (ii) AL3 clause, restated T7); **Prop DL-4** (sufficient conditions for DL = 0; proof repaired T7); **DL-5** (computable upper bound); **DL-6** (an envelope is a ceiling: under AL3 under-adoption and cheap harmful adoption; plus the AL3 unit-only-exclusion channel) | characterization lemma (restatement-level) / corollaries / propositions | Formalises the P2 remark (C.6 l.2899) | l.1138 "不對齊是 DL > 0 的必要而非充分條件：若不利企業的配置需要池化資源，企業可以 envelope 阻止。" → D-e fix, plus "（精確刻畫見 Lemma DL-1；「不對齊」須含 AL3 部門專屬限制，見構造例 W_DL_AL3）" | P2's remark is restated exactly with the correct quantifier (every first best); the new content is Cor DL-2o, Cor DL-3, W3c, DL-6 | No iff in first-best-independent primitives (impossible as a Boolean combination of (A)–(F), W3c). DL-1 / Lemma E′ now PROVEN also for 51's relative `ε_tie` (F_u-maximal selection; Q/02 §2.2; exact affordability); Cor DL-2–DL-5 exact ties only. STRICT_REVERSAL / NON_SEPARABILITY necessary only under AL3. Restricted envelope institutions are not analysed | W1–W3, W3m, W3b, W3c, W_DL_AL3 |
| 4.2 | **GS-0** (= P7 restated with the cost channel); **Identity GS-I** (accounting decomposition) `GSV^m = DL^m(loose) − DL^m(strict) − PR_B`; `GSV ≤ DL_loose` as a corollary of P1 + P7 (T7 relabel per Q/11 A4); **Prop GS-1** (full screening ⇒ GSV = DL_loose); **Prop GS-2** (pairwise screening is insufficient); **Thm GS-N** (necessary: an excluded, envelope-non-separable, enterprise-worse best response); **Cor GS-4** (full envelope separability ⇒ GSV ≤ 0) | theorems / propositions | Refines P7 (GS-0 = P7 + cost) and P8 (GS-1 / GS-N bracket it) | l.1142 P7 and l.1143 P8 unchanged. Add after P8: "P8 的篩選價值滿足 GSV ≤ DL_loose（恆等式 GS-I 與 P1、P7 之推論）；正篩選價值的必要條件為 GS-N，充分條件為 GS-1；兩者之間沒有原始條件的充要刻畫。" | P8 becomes a bounded, exactly accounted channel. The pessimistic case can come from follower indifference (W4e) | A primitive iff for GSV > 0 is **NOT_PROVEN**. Joint γ → γ′ moves give only NGE = GSV + DGC. Assurance value under Θ_g is outside these fixed-θ results | W4, W4b–W4e |
| 4.3 | **Thm D1** (B monotone in δ under A1 source indexing, A2, A3 fixed candidate set, A4 no follower, A5); **Thm D3** (restatement: P2 applied pointwise in (y,γ); AL ⇒ C = B at every (y,γ), so C is monotone in both modes); **Lemma I** (implementability; renamed from "Lemma S" to avoid the clash with Q/02's Lemma S); **Props D4, D5** (weaker sufficient conditions); **Prop D6** (existence: under misalignment the C build region is not an interval; strict [0,3) ∪ (4,∞), tie-build [0,3) ∪ [4,∞)); **Lemma M** (a single 2-option follower cannot produce 1→0→1) | restatement (D1: explicit form of P4, B part; D3: restatement of P2 pointwise) / propositions / lemma [T8-fix]; **Conj M2 NOT_PROVEN** | Sharpens P4 | l.1140 "在 C 中只有帳本對齊時才保證。" → keep it and add "（對齊為充分而非必要條件；較弱的充分條件見 Prop D4、D5；Prop D6 為存在性結果，給出連續建置區域與 tie 慣例）". Also state the leader-tie convention (51: strict) | P4's δ claim becomes proven in B and in aligned C, plus an explicit continuous region | Joint cost+quality δ scans are not covered. Source indexing (A1) is load-bearing (W5b). **Every-resource footprint caveat** (Q/04 §6): non-monotonicity needs reuse to bring the misaligned unit's AI configuration to a pooled footprint ≤ the enterprise-preferred plan's in every pooled resource incl. ENG; W5's margins are thin (1 TWD; 162/400 survive ±5 %), so cite W5 as existence only and W5_WIDE (367/400 at ±5 %) as the robustness illustration | W5 (incl. W5-min), W5b, W5_WIDE |
| 4.4 | Governance-function map (Q/03 §7): compliance / assurance / screening / enablement / operating cost; **caveat**: screening by `J^forbid` or `Allow = 0` is booked in EE, not RE | conceptual (TYPE C) | Q3 decomposition (l.1147–1151) | l.1151 "以及僅在雙層且帳本不對齊時出現的**篩選**（P8：以規則替代無法以預算達成的協調）" → add "（篩選價值不超過授權損失，恆等式 GS-I；由禁止或不允許達成的篩選記入 EE 而非 RE）" | Avoids undercounting screening done by prohibitions | — | — |

**D1/D3/D6 vs P4, P7, P8 (consistency statement to place in C.10).**
* D1 is P4's B part with all assumptions explicit.
* D3 is P2 applied at each fixed `(y,γ)`.
* D6 is P4's C caveat, now an existence proposition.
* GS-0 is P7 plus the cost channel.
* GS-I, GS-1 and GS-N bracket P8.
* W5 is a P8-type situation: a rule that excludes U2's k=1 would restore F^C = F^B.
* **No P-statement is contradicted.**
* **Status:** SAFE.

---

## 5. §3.12.5 — Q1–Q8 implications (Table 3-10, l.1159–1168; C.5, l.2874–2881)

| Q | Change | Current wording | Status / limitation | Evidence |
|---|---|---|---|---|
| Q1 (l.1161) | Report DL^opt and DL^pess. NEV's sign remains model-undetermined (P1) | none | — | SAFE |
| Q2 (l.1162) | "重用門檻 `δ^†`" → "B：唯一 `δ^†`（Thm D1）；C：對齊時唯一（Thm D3），否則報告集合值建置區域與 tie 慣例（Prop D6）" | "損益兩平固定成本 `F_c^†`、重用門檻 `δ^†`" | `F_c^†` stays monotone in C (P4 unchanged) | SAFE |
| Q3 (l.1163) | VG = EE + RE + CE; in C, RE = GSV ≤ DL_loose (GS-I) | none | No primitive iff | SAFE |
| Q4 (l.1164; C.5 l.2877) | DL source decomposition: "逐一關閉 (AL1)–(AL4)" **plus** the DL-1 separability diagnosis: report (i) which AL fails and (ii) which first-best plan has an unblockable deviation (`a(x^H) ≤ a(x*)`) | C.5 l.2877 "DL > 0 必有某個 (AL) 不成立（P2）；分解指出是哪一個" | Pairwise checks are insufficient (W3c). The iff needs all first-best solutions | SAFE |
| Q5 (l.1165; C.5 l.2878) | "screening" verdict `PR^C_X < 0` ⇔ the DL reduction exceeds `PR^B_X` (GS-I restated in Q5 terms) | none | — | SAFE |
| Q7 (l.1167; C.5 l.2880) | Add the scope sentence of Q/06 §5 (vertex-exact only for B/A+ whole portfolio, MaxRegret and the λ box; element level only in the Prop R4 case) | none | Element level and C are coverage-only | SAFE |
| Q8 (l.1170) | No change. Interface activation remains an **empirical** result | — | — | NEEDS-HUMAN (V1) and NEEDS-ENTERPRISE (V7) |

**Empirical hypotheses (status: empirical hypothesis, untested)** may be listed only in §5.9 or as Q4/Q5 follow-ups:
* H-DL1: footprint signature;
* H-DL2: ledger signature, conditional on H-DL1;
* H-DL3: budget tightening is ineffective for low-footprint configurations;
* H-DL4: platform coupling;
* H-DL5: indifference / defaults.

**Status:** NEEDS-ENTERPRISE. They must not appear in Chapter 4.

---

## 6. §3.13 — robustness and VOI (incl. the "for a fixed candidate set" qualification)

| # | Insertion point | New item | Status | Current wording (quote) and change | Stronger claim | Limitation | Witness |
|---|---|---|---|---|---|---|---|
| 6.1 | l.1271, Lemma R paragraph | **Thm R1** (restatement of 42 Lemma R [T8-fix]; Lemma R with explicit hypotheses (R-a)–(R-e): whole portfolio in B/A+; block-affine single-factor-class blocks; Cartesian product of polytopes; fixed robustly feasible candidate set; weak optimality); **Cor R1a** (MaxRegret); **Cor R1b** (λ box) | restatement / corollaries [T8-fix] | "**Lemma R（精確檢查，僅限 Model B 的整個 portfolio）**" → keep it, and add "（精確前提 (R-a)–(R-e) 見附錄 C.10 Thm R1；A+ 亦適用）" | Exact hypothesis list | Dependent Θ and conditionally feasible members are excluded | W7 (positive control) |
| 6.2 | l.1271, element-level sentence ("元素層級因此以「存在單一 robust portfolio 含該值」為充分條件") | **Prop R2** (exact covering characterisation); **Prop R3** (vertex test not exact; the T-SEN-3 instance is minimal, with 3 portfolios × 1 block); **Prop R4** (exact when exactly one candidate carries the element value) | propositions | Add "（當恰一個候選 portfolio 含該值時，頂點檢查亦為必要條件：Prop R4）" | — | Covering needs the switching-surface arrangement | W7(a) |
| 6.3 | l.1271, Model C sentence | **Prop R5**: Model C is not vertex-exact even for a fixed leader decision. Aligned → convex; misaligned → **discontinuous** pessimistic value | proposition | "Model C 的 leader 價值經由隨 `θ` 改變的部門最佳回應決定，亦一律以列舉或抽樣判定" → add "（帳本不對齊時悲觀值可在部門切換面上不連續，故網格結論只對評估點成立）" | — | Grid coverage only | W7(b), (c) |
| 6.4 | l.1277 | **D-b** (see §0). Add **Prop E.1** (fixed C ⇒ MMR monotone under narrowing), **E.2** (ordering), **E.3 / E.5** (overstatement; sufficient condition for exactness), **E.4** (exact VOI by finite enumeration; implemented for scale blocks only), **E.6** (nested grids monotone; non-nested and edge-only grids are not) | propositions | see D-b | VOI ordering is proven under its true premise | Adaptive convention: monotonicity fails (W6b); sharp benchmark: vertex exactness fails (W6d). The trilemma is not a general impossibility theorem (NOT_PROVEN) | W6, W6b, W6c, W6d |
| 6.5 | l.1277, end ("…不進目標（G12 的靜態影子）") | Static-sequential identification procedure (SIP) as a **protocol**: **Thm E.7** (termination with finite evidence states); **Prop E.10** (rule B ⇔ MMR = 0 ⇔ Lemma R certificate); rule C carries no guarantee (W6f); rule D is myopic (W6e) | theorem / proposition; protocol = EXTENSION | Add one paragraph; SIP needs **versioned registries** (an extension of l.1256's single-commit registry) | — | VOI-greedy optimality is NOT_PROVEN; no enterprise run | W6e, W6f |
| 6.6 | §3.14 missingness (l.1299–1317) or C.4 (l.2852) | **Def G** (DC / DIER / NULL, plus the orthogonal FC channel); **Props G1–G6, G8**; **Remark G7**. Explain why each 42 §13.4 status is the correct epistemic report. Position as a **methodological / model-identification** contribution | definition / propositions / remark | Add a paragraph and table (Q/07 §4) | v2.2's status machine is justified formally | Model C DIER status for continuous cells holds only at evaluated points. There is no bracketing for multi-option cells | W8a, W8b, W8c |

**Status:** SAFE for all rows.

---

## 7. §4.9 — synthetic engineering validation (witness list, SIMULATED_ONLY)

* **Insertion point:** after table 4-20C and its note (**after l.1984**, before §4.10 at l.1986). Add "**表 4-20D：Q1 理論構造例（SIMULATED_ONLY；構造例，非證明）**".
* **Content:** the 27 witnesses of Q/09 (26 from T5 plus W5_WIDE added by T7 on 2026-10-15; id; what it demonstrates; supported or refuted statement; source test; PASS; SHA-256 prefix), plus `Q1_WITNESS_VERDICT: PASS`, the `witness_set_sha256` (`f5814c96…36a0`), and the determinism statement. Next to W5, add the W5 fragility note: margins of 1 TWD, two exact zeros, and W5_WIDE as the wide-margin illustration (Q/09).
* **Mandatory lead sentence:** "下表各列為構造例（computational witnesses），只顯示存在性或反駁全稱主張，不是一般定理的證明；證明見附錄 C.10。所有數值為代數構造，`SIMULATED_ONLY`，不構成企業結論、實證效度或 V7 證據。"
* **Cross-reference existing rows:**
  * l.1905 (P8 10 → 15) = W4;
  * l.1907 (hand oracle 30/15/10) = W1–W3;
  * l.1917 (VOI 1 vs 0.5) = W6 (add "對固定候選集合");
  * l.1918 (δ sequence 1,1,1,1,0,0,0,1) = W5;
  * l.1916 (element / C ScopeError) = W7.
* **Mandatory exclusion:** **W_IA_NDV must NOT be listed in Chapter 4.** Q/08 forbids it there. Mention it only in §5.8.5 or §5.9.
* **Status:** SAFE. No enterprise evidence is involved.

---

## 8. §5.6 — conditional implications

| # | Location | Change | Status | Evidence |
|---|---|---|---|---|
| 8.1 | l.2317 | D-c fix (screening is bounded by DL; the condition is necessary, not sufficient) | GS-I, GS-1, GS-N | SAFE |
| 8.2 | l.2323 | D-e fix. Add "envelope 只能設上限、不能強制採用：低於或等於企業偏好配置資源用量的不利配置（含維持現況的採用不足）無法以預算阻擋（Prop DL-6）；只有 `γ`（禁止、強制或要求）或 `y` 能作用。" | proposition | SAFE |
| 8.3 | l.2325 | Keep. Add "DL 為正的刻畫（模型內；Lemma E′ 於首佳之重述）：每一個集中最適解都至少有一個部門存在不可阻擋的偏離（Lemma DL-1）；在唯一首佳下可寫成原始條件（Cor DL-3）" | characterization lemma / corollary | SAFE |
| 8.4 | l.2327 | "在雙層中只有在帳本對齊時才保證單調，否則建置區域可為集合值" → "對齊為充分條件（Thm D3〔P2 逐點之重述〕；較弱條件 D4、D5）；不對齊時存在非區間的建置區域（Prop D6）：共享能力的重用可能破壞 envelope 的分離能力——重用使部門偏好的不利配置變得不需更多池化資源。治理篩選與重用非單調是同一種分離失效。" (Thm D3 = restatement of P2 pointwise) [T8-fix] | restatement / proposition | SAFE |
| 8.5 | after l.2329 | One paragraph on robustness and VOI: exactness only for the B whole portfolio; VOI is an upper bound only for a fixed candidate set; myopic VOI | Thm R1 (restatement of 42 Lemma R), Prop E.2 [T8-fix] | SAFE |
| 8.6 | — | Every implication stays tagged "模型內性質" plus `[EMPIRICAL RESULT PENDING]` | — | Application: NEEDS-ENTERPRISE |

---

## 9. §5.7 — theoretical contribution (TYPE C claims only, scoped)

* **Insertion point:** after l.2339 ("…本研究的模型候選把這些斷點分別寫成可量測的變數。").
* **New paragraph "形式理論貢獻（模型內；TYPE C）":**
  1. Delegation loss: a primitive pairwise iff under a unique first best (Cor DL-3), the impossibility of an iff in the predicates (A)–(F) (W3c), the strict-reversal selection result (Cor DL-2o) and the "envelope is a ceiling" result (DL-6); DL-1 itself is presented as a characterization lemma (Lemma E′ at a first best), not as a headline theorem. The loss comes from **instrument incompleteness** under complete information, not from hidden information. `DL ≥ 0` is built in by construction (P1); the contribution is the characterization of when `DL = 0` (Q/11 A3).
  2. Governance screening: a non-definitional necessary condition (GS-N), a sufficient condition (GS-1), and three failure modes (W4c/W4d/W4e); GS-I is an accounting identity and `GSV ≤ DL_loose` a corollary of P1 + P7.
  3. Shared-capability reuse: monotone in B and in aligned C; non-interval regions otherwise (D4–D6, Lemma M; D1/D3 restate P4/P2) [T8-fix].
  4. The scope of vertex exactness (R2, R4, R5(ii); R1 restates 42 Lemma R) [T8-fix] and of VOI (E.1–E.7).
  5. Missingness classes as model identification (G1–G8).
  6. M1–M4 non-redundancy under typing axioms T1–T4 relative to the v2.2 schema (IRR; definitional), with sufficiency PARTIAL.
* **Mandatory scope sentence:** "以上皆為完全資訊、單期靜態、固定 θ（R/E 系列另以登記的 Θ_g）的模型內結果；文獻僅作概念錨點（TYPE B），不宣稱任何企業中成立。"
* **Mandatory AI-specificity sentence (T7 per Q/11 A11):** "第 1–5 項的組合層級結果（授權損失、治理篩選、重用非單調、穩健性範圍、VOI、缺值）是企業–部門架構的性質，對任何共用平台的 IT 組合皆成立；本研究的 AI 特定內容在於配置結構（M1–M4）、依自主等級設定的要求表，以及人員對自動化建議的回應層（ρ）。"
* **Mandatory novelty qualifier (T7 per Q/11 A10):** each item is "TYPE C 模型內結果；機制在 X 文獻中已知（待查證）", with X = optimal delegation / delegated project choice (1, 2), capital budgeting with spending ceilings (1), Braess-type "more options can hurt" (3), robust optimization / interval minmax regret (4), minimax-regret menu dependence and VOI complementarity (4), partial identification (5).
* **Must not:** write "according to Aghion & Tirole / Alonso et al." for any TYPE C result.
* **Status:** SAFE.

---

## 10. §5.8 — limitations (NOT_PROVEN list)

**Insertion point:** a new **§5.8.10 "理論結果的未證明部分"**, after l.2391 and before §5.9 at l.2393. Alternatively, split it into §5.8.4–5.8.6. Content: NOT_PROVEN items, each labelled with its source.

| Item | Source |
|---|---|
| Global sufficiency of M1–M4 (no closed universe; the information-asymmetry residual) | Q/01 §6.3 |
| An iff for DL in first-best-independent primitives (W3c shows it is impossible as a Boolean combination of (A)–(F)); Cor DL-2–DL-5 and GS-N under a tolerant tie rule; 51's absolute affordability slack (DL-1 under the relative `ε_tie` itself is now PROVEN, Q/02 §2.2) | Q/02 §9 |
| Comparative statics of DL; robust DL; Model D; restricted envelope institutions | Q/02 §9 |
| A primitive iff for GSV > 0; joint γ moves; requirement-menu design; assurance value on Θ_g | Q/03 §11 |
| Conjecture M2; joint δ–quality scans | Q/04 §9 |
| VOI-greedy optimality; an adaptive + monotone + vertex-exact convention; an exact sharp benchmark; the converse of E.5; E.4(b) implementation; any guarantee for rule C; expected-value VOI (not definable without a prior) | Q/05 §9 |
| Model C vertex exactness (false); dependent Θ | Q/06 |
| Model C DIER for continuous cells; multi-option cells | Q/07 §9 |
| Information asymmetry: `SIDECAR_DESIGN_ONLY`; IA-2 and IA-3 are proof sketches; there is no iff for NDV > 0 | Q/08 §7 |

**Also:**
* If §5.8.10 is added, l.2343 ("研究限制依證據鏈分為九類") must become "十類".
* §5.8.5, l.2375 ("模型是完全資訊模型…才執行資訊不對稱的敏感度分析"): add a pointer to the sidecar design (Q/08), status `SIDECAR_DESIGN_ONLY`. Its full-information special case reproduces P3.
* §5.8.4, l.2371: add the NONE / AMBIGUOUS distinction (coverage vs boundary). V1 does not test sufficiency.

**Status:** SAFE.

---

## 11. Appendix C — formal proofs

* **Insertion point:** a new **"C.10 Q1 理論補充（新增；非 v2.2 原文）"**, after C.9 (which ends at l.2961) and before Appendix D (l.2962).
* **Why a new section:** this keeps the l.2793 statement ("本附錄逐字收錄企業模型規格 v2.2") true for C.1–C.9.
* **Sub-sections, each containing the statement, an explicit assumption list, tie conventions (opt and pess), a complete proof and the witness reference:**

| Sub-section | Content | Source |
|---|---|---|
| C.10.1 | M1–M4 definitions, object test, Prop IRR, Lemma COV with the circularity caveat | Q/01 |
| C.10.2 | Lemma S, Lemma DL-1o/p (characterization lemma) incl. the tolerant-tie version (§2.2), Cor DL-2o/p, Cor DL-3 (Parts (i)/(ii)), Props DL-4 (repaired proof), DL-5, DL-6 | Q/02 |
| C.10.3 | GS-0 (P7 restated + cost), Identity GS-I and Cor GS-I′; Prop GS-1, GS-2; Thm GS-N; Cor GS-4; the P8 decomposition; v2.2 embedding notes for the single-BU cores | Q/03 |
| C.10.4 | Thm D1 (explicit form of P4, B part) [T8-fix], Lemma I (implementability; formerly "Lemma S"), Thm D3 (restatement of P2 pointwise), Props D4–D6, Lemma M, the every-resource footprint caveat, W5/W5_WIDE; Conj M2 marked NOT_PROVEN | Q/04 |
| C.10.5 | Lemma 0; Props E.1, E.2, E.4, E.5, E.6, E.10; Thm E.7; the counterexamples | Q/05 |
| C.10.6 | Thm R1 (restatement of 42 Lemma R) [T8-fix], Cor R1a/b, Props R2–R5 | Q/06 |
| C.10.7 | Def G; Props G1 (premise corrected), G2–G3, G4 (quantifier corrected: every zero-fill optimum; NULL separated), G5–G6, G8; Remark G7 | Q/07 |
| C.10.8 | Witness index: the Q/09 table, `q1_theory_witnesses.py`, `witness_set_sha256` | Q/09 |

* **In C.6:**
  * after the P2 remark (l.2899), add the pointer "精確化見 C.10.2"; after P4 (l.2903), "見 C.10.4"; after P8 (l.2911), "見 C.10.3";
  * **do not edit** the v2.2 verbatim text.
* **In C.3:** after scope item 1 (l.2835), add the pointer "Prop R2–R4 見 C.10.6".
* **Not to include:** Q/08 (IA sidecar) goes, if anywhere, into a separately labelled "未來擴充設計" note. It is not a proof section.
* **Status:** SAFE.

---

## 12. Summary: safe vs evidence-dependent

| Category | Changes |
|---|---|
| **SAFE (no new evidence; wording and formal additions)** | D-a, D-b, D-c, D-d, D-e; §1 rows 1.1–1.6; §2 wording (TYPE A/B from the list); §3.1–3.5; §4.1–4.4; §5 Q1–Q7 table edits; §6.1–6.6; §7 (table 4-20D); §8.1–8.5; §9; §10; §11 |
| **NEEDS-CITATION-CHECK** | Weill & Ross (2004) — secondary only; Jensen & Meckling (1976); Holmström (1984); Alonso & Matouschek (2008); Laffont & Martimort (2002); Topkis / Milgrom–Shannon; Howard (1966); Raiffa & Schlaifer (1961); Kouvelis & Yu (1997); Averbakh; Manski. None of them is required by any proof |
| **NEEDS-HUMAN (V1 / EA-X; no human data exist)** | Any statement that a G→M mapping is validated; whether NONE or AMBIGUOUS rates signal coverage or boundary problems; Q8 tracing to gaps |
| **NEEDS-ENTERPRISE (V0 / V2 / V7; 620 cells UNIDENTIFIED)** | H-DL1–H-DL5; any enterprise DL, GSV, `δ` region, VOI ranking or robustness class; the information-asymmetry elicitation (Q/08 §6); any practical recommendation drawn from §5.6 |
| **Never** | Claiming V7 or empirical validity; promoting G01–G16, Study 1, the frozen robust 32, or v2.4 α/ATT to canonical; writing a witness as a proof; writing a TYPE C result as "according to X"; listing W_IA_NDV in Chapter 4; changing any v2.2 equation |

---

## 13. Researcher decision items added after the red-team review (T7, 2026-10-15)

| # | Decision | Background | Options | Evidence |
|---|---|---|---|---|
| R-1 | **42 erratum candidate**: Lemma E′'s pessimistic proof sentence (42 §12.4 l.476, "取任一 `x ∈ T`") is false under 42's own tie tolerance. The statement survives if the `F_u`-maximal element of the tie set is chosen. 51's computed numbers are unaffected. | `13_Q1_CANONICAL_42_ERRATUM_CANDIDATE.md`; Q/11 A5 and §2.7; Q/02 §2.2 | (a) Accept and correct 42 (and the 51 `envelopes_lemmaE` docstring wording) at the next canonical version bump. (b) Accept, and in the meantime add a one-line note in Appendix C.10.2: "v2.2 Lemma E′ 之悲觀證明句在 `ε_tie > 0` 時需改取 `T` 中部門目標最大者；敘述與 51 數值不受影響（見 C.10.2）". C.1–C.9 verbatim text stays unchanged. (c) Reject, with a reason. | SAFE (proof text only) |
| R-2 | **Framing of DL-1 / GS-I** in the abstract, §1.7.2 and §5.7 | Q/11 A1–A4 | Present DL-1 as a characterization lemma (restatement of Lemma E′) and GS-I as an accounting identity. Lead with Cor DL-2o, Cor DL-3, W3c, DL-6, GS-N and W4c–W4e. State "DL ≥ 0 by construction (P1, complete information); the contribution is the characterization of when DL = 0". | SAFE |
| R-3 | **AI-specificity statement** (§1.7.2, §5.7) | Q/11 A11 | Adopt the mandatory sentence in §9 above, so that a referee cannot read the portfolio results as AI-specific. | SAFE |
| R-4 | **Known-analogue citations** | Q/11 A10; rows 2.8 and 2.9 | Verify, then add to the reference list or drop: Armstrong & Vickers; Alonso & Matouschek; Holmström; Harris & Raviv-type capital budgeting; Chernoff / Stoye; Manski; Topkis / Milgrom–Shannon; Kouvelis & Yu / Averbakh; Loridan & Morgan. No bibliographic details are asserted in this pack. | NEEDS-CITATION-CHECK |
| R-5 | **Use of W5** in §5.6 (H-DL4, "platform coupling") | Q/11 A6; Q/04 §6 | Cite W5 only as an existence witness. Add the every-resource footprint condition and the W5_WIDE robustness illustration. Do not present reuse non-monotonicity as practically prevalent. | SAFE |
