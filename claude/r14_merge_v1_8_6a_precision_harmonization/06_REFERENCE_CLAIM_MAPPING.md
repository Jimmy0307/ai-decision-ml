# 06 — Reference Claim Mapping (V1.8.6a; agent RM)

Scope: the three verified candidates that are not in the reference list: Alonso & Matouschek (2008), Armstrong & Vickers (2010) and Stoye (2011). For each one, this file decides whether an **existing** V1.8.6 sentence needs it.

Rules applied:
- No new claim is written.
- No citation padding.
- Bibliographic data comes only from Crossref, as recorded in `work\RV\cr_*.json`.

Inputs (all READ-ONLY), in `REPO\claude\r14_merge_v1_8_6_theory_integration\`:
- `01_V1_8_6_THEORY_INTEGRATED_MANUSCRIPT.md` (sha256 94d41d56…). Line numbers below refer to this file.
- `07_V1_8_6_REFERENCE_VERIFICATION.csv`
- `08_V1_8_6_REFERENCE_IMPACT_REPORT.md`
- `work\RV\cr_alonso_matouschek.json`, `cr_armstrong_vickers.json`, `cr_stoye.json`

Also used: theory pack `REPO\claude\r14_merge_q1_theory_upgrade_v1\` 02 §7 (l.278–284), 03 §10 (l.255–257) and 05 (l.32, l.317–318).

Supporting passages are those RV located in full text (07 CSV `exact_support_location`). They were not re-fetched, because no candidate is ADDed and no passage is used in the manuscript.

## Governing manuscript constraints (existing text)

- **l.3297 (App. E, E51):** 「Q1 理論補充（第 3.12.4、3.13、5.7 節；附錄 C.10）的相關文獻定位尚未查證｜這些形式結果在正文只以本研究的模型內結果（TYPE C）陳述｜相關文獻經查證並加入參考文獻之前，正文不引用、不比較，也不據以主張新穎性」
- **l.170:** 「…都是本研究在完全資訊、單期靜態、固定參數 `θ`…的企業—事業單位雙層模型內的結果（TYPE C）…它們不是企業中已發生的現象…」
- **l.182:** 「…是企業—事業單位架構的一般形式性質，並非 AI 所獨有…」
- **l.1303:** 「資訊價值的概念並非本研究所創。本研究的貢獻限於：…」

The manuscript therefore makes no novelty claim against the delegation or minimax-regret literatures. A citation can be needed only if an existing sentence would otherwise misstate a prior-literature boundary.

---

## CLAIM_MAPPING 1 — Alonso & Matouschek (2008), *Optimal Delegation*, REStud

- **Candidate attachment point (the closest existing sentences):**
  - **l.2395** (§5, 形式理論貢獻 (1)): 「…確定 DL 何時為零…；損失來自完全資訊下的工具不完備，而不是隱藏資訊。」
  - **l.1163** (§3.12.4 治理篩選): 「…在 Model C 中，要求改變的是部門的最佳回應對應，因此可能具有篩選作用。」 and 「…本稿不宣稱治理要求一般會提高企業價值。」
  - **l.2973** (App. C, P8; v2.2 text verbatim, cannot be edited): 「要求縮小部門的可選集合，可以排除部門偏好但對企業不利、且無法以 envelope 阻擋的配置。」
- **Supporting passage** (RV, LSE Research Online AAM eprint 58665, Abstract p. 1): "The contracting problem reduces to a delegation problem in which the principal commits to a set of decisions from which the agent chooses his preferred one. We characterize the optimal delegation set …"
- **Role:** EXISTING_THEORY. It would be a known analogue or contrast: the agent is informed and biased (hidden information), whereas in v2.2 the agent's ledger is observable and information is complete.
- **genuinely_needed = NO.**
  - None of these sentences claims that restricting a choice set is new.
  - l.2395 already places the loss in "完全資訊下的工具不完備，而不是隱藏資訊", which is an in-model description, not a comparison.
  - The prior-literature boundary for hidden-information or decentralization benefits is already stated and cited at **l.2377**: 「…理論上分權可能具有的資訊優勢（Alonso et al., 2008）不在模型內。」
  - E51 explicitly defers positioning.
  - Attaching the citation would need a new comparison clause, i.e., a new claim, which E51 and this round's rules forbid.
- **redundant_with_existing_citation = YES (partial).**
  - The hidden-information boundary is carried by Alonso, Dessein & Matouschek (2008, AER; l.2377, l.326, l.336), with Aghion & Tirole (1997; l.336) on formal vs real authority.
  - A&M (2008) would add only the permitted-set analogue, and no existing sentence asserts that analogue.
- **DECISION: KEEP_IN_VERIFIED_RESEARCH_NOTES.**
  - It is FULLTEXT_VERIFIED and remains the first-choice citation if a future version adds a related-literature positioning sentence for DL/GS.
  - It would be framed as a contrast only: hidden information vs instrument incompleteness. It must never support DL-x or GS-x results.
  - Adding it now would be padding.
- Reference entry: not produced (not ADDed). Crossref identity, for the record: 10.1111/j.1467-937x.2007.00471.x; *Review of Economic Studies* 75(1), 259–293; 2008-01; authors Ricardo Alonso, Niko Matouschek.

## CLAIM_MAPPING 2 — Armstrong & Vickers (2010), *A Model of Delegated Project Choice*, Econometrica

- **Candidate attachment point:** the same sentences as above (l.2395; l.1163; l.2973 P8, which is verbatim and cannot be edited).
- **Supporting passage** (RV, UCL Discovery WP June 2008, eprint 14431):
  - Abstract p. 1: "We present a model in which a principal delegates the choice of project to an agent with different preferences. The principal determines the set of projects from which the agent may choose."
  - §1 p. 1: "The agent … will select from her available projects the permitted project that best serves her interests."
  - OpenAlex has the same first two sentences for the published abstract. The published full text was not read.
- **Role:** EXISTING_THEORY, as a known analogue or contrast. In their model the principal does not know which projects are available (asymmetric information); v2.2 is a complete-information model.
- **genuinely_needed = NO.**
  - There is no existing sentence that compares the work with the delegated-project-choice literature, or that claims the "permitted set + agent's favourite" mechanism as new.
  - The relevant boundary is already handled by l.2377 (ADM 2008) and by E51.
- **redundant_with_existing_citation = YES.**
  - It overlaps with A&M (2008) in the role that matters here: the permitted-set analogue.
  - The information boundary is already cited (ADM 2008; Aghion & Tirole 1997).
  - If a positioning sentence is ever added, one delegation-set citation (A&M 2008) is enough. A&V is optional.
- **DECISION: KEEP_IN_VERIFIED_RESEARCH_NOTES.** It is verified from the working-paper version only. Check the published pagination and text before any future use.
- Reference entry: not produced. Crossref identity: 10.3982/ecta7965; *Econometrica* 78(1), 213–244; 2010. The Crossref author field is empty; the authors (Mark Armstrong, John Vickers) appear only on the WP title page. Any future entry must take author names from the publisher page.

## CLAIM_MAPPING 3 — Stoye (2011), *Axioms for minimax regret choice correspondences*, JET

- **Candidate attachment points:**
  - **l.1301** (§3.13 VOI 診斷): 「若縮小 `Θ` 後重新計算 robust 候選集合（調適慣例），此次序不再成立：MMR 可能上升、VOI 可能為負（構造例 W6b）。」
  - **l.1303:** 「…候選集合隨 `Θ` 調適時的對應性質已被反駁（W6b）…」
  - **l.326** (§2.13): 「…minimax-regret 準則一般溯源至 Savage（1951）`[PARTIAL：書目已以 Crossref 核對；歸屬僅見二手文獻，原文未取得；附錄 B N34]`。」
- **Supporting passage** (RV, author working version dated July 14, 2011):
  - p. 2: "this ordering is menu dependent, i.e. the ranking of acts can depend on the feasible set within which they are compared"
  - p. 7: "a crucial, and controversial, feature of minimax regret, namely that it violates independence of irrelevant alternatives (IIA)"
  - p. 2, for the attribution: "The minimax regret decision criterion was suggested in Savage's [50] reading of Wald [65]"
  - The final JET text was not read.
- **Role:**
  - At l.1301/1303: EXISTING_THEORY. W6b would be an in-model instance of the known menu dependence of minimax regret.
  - At l.326: CONCEPTUAL_ANCHOR, as secondary attribution support only.
- **genuinely_needed = NO.**
  - l.1301/1303 present W6b only as a counterexample that limits the manuscript's own Prop E.1/E.2 to a fixed candidate set. They do not claim that menu dependence is a new finding.
  - l.1303 limits the contribution explicitly, and l.2395 (4) lists only Prop E.1, E.4–E.6 and Thm E.7 (fixed candidate set), not W6b, as formal results.
  - The novelty is therefore not misrepresented.
  - At l.326, the Savage attribution is already honestly marked PARTIAL, with secondary sources recorded (App. B N34; E3).
  - Adding Stoye would strengthen that sourcing, but it is not required for the sentence to be accurate.
- **redundant_with_existing_citation:**
  - At l.1301/1303: **NO**. No existing citation covers menu dependence.
  - At l.326: **YES (partial)**. The attribution is already carried by Savage (1951) together with the N34 PARTIAL flag.
- **DECISION: KEEP_IN_VERIFIED_RESEARCH_NOTES.**
  - It is the first-choice citation if a future version (a) adds a sentence placing W6b as an instance of the known menu dependence of minimax regret (TYPE C stays TYPE C), or (b) closes E3 by citing a full-text secondary source for the Savage attribution.
  - Either option is a researcher decision. Neither is a precision fix within this round's scope.
  - Before use, check the pagination of the final JET version.
- Reference entry: not produced. Crossref identity: 10.1016/j.jet.2011.10.004; *Journal of Economic Theory* 146(6), 2226–2251; 2011-11; author Jörg Stoye.

---

## Summary

| candidate | attach line(s) | role | genuinely_needed | redundant | decision |
|---|---|---|---|---|---|
| Alonso & Matouschek (2008) | l.2395, l.1163 (l.2973, verbatim) | EXISTING_THEORY (contrast) | NO | YES (partial: ADM 2008 l.2377; Aghion & Tirole 1997) | KEEP_IN_VERIFIED_RESEARCH_NOTES |
| Armstrong & Vickers (2010) | l.2395, l.1163 (l.2973, verbatim) | EXISTING_THEORY (contrast) | NO | YES (overlaps A&M; ADM 2008) | KEEP_IN_VERIFIED_RESEARCH_NOTES |
| Stoye (2011) | l.1301, l.1303; l.326 | EXISTING_THEORY; CONCEPTUAL_ANCHOR at l.326 | NO | NO at l.1301; YES (partial) at l.326 | KEEP_IN_VERIFIED_RESEARCH_NOTES |

- No reference-list change.
- E51 (l.3297) stays accurate as written.
- No DOI or page was written from memory.

NEW_REFERENCES_RECOMMENDED=0
LIST=(none)
