# V1.8.6 Reference Verification — Impact Report (agent RV)

Scope: every literature item that the Q1 theory pack (`REPO\claude\r14_merge_q1_theory_upgrade_v1\01–15`) marks TO VERIFY or uses as a TYPE A/B anchor. That is 58 rows: 35 are in the 59a reference list (l.2419–2688), 23 are not, and 3 of those 23 are literature streams with no named work. Per-item evidence is in `07_V1_8_6_REFERENCE_VERIFICATION.csv`. Scratch material is in `work\RV\`: Crossref JSON (`cr_*.json`), OpenAlex abstracts (`openalex_abstracts.txt`) and the generator `build_07.py`.

Method:
- Crossref `query.bibliographic` was used for identity only.
- OpenAlex abstract indexes were used for abstracts. Their word order is reconstructed, as 59a E32 notes.
- Open-access full texts were read with `pdftotext` and searched for the exact claim: publisher, author, repository and arXiv copies.
- Several sources could not be read in this run because of blocking: AISeL (Cloudflare), MIT DSpace (HTTP 429), Imperial Spiral and Montréal (bot walls), ScienceDirect (403).
- No DOI, page or volume was written from memory. Where Crossref shows only a first page, or a digital-edition date, the CSV says so.

## 1. Counts

| verification_status | all | in 59a list | not in list |
|---|---|---|---|
| FULLTEXT_VERIFIED | 21 | 18 | 3 |
| ABSTRACT_VERIFIED | 20 | 15 | 5 |
| SECONDARY_ONLY | 5 | 1 (Savage 1951) | 4 |
| UNVERIFIED | 12 | 1 (ISO/IEC 42001) | 11 |
| **total** | **58** | **35** | **23** |

`allowed_in_main_text`:
- **YES: 21** (18 in the list; 3 not in the list, conditional on being added).
- **NO: 37.**
- Every YES row is FULLTEXT_VERIFIED for the exact claim stated, so there are no YES rows that are not FULLTEXT_VERIFIED.

## 2. Items that may enter the main text, and for which exact claim

**A. In the 59a list: theory anchors that the integration plan cites in main text (rows 2.1–2.6)**

| key | permitted claim (only this) | support located |
|---|---|---|
| Aghion & Tirole (1997) | Formal authority (the right to decide) and real authority (effective control) are distinct and can diverge. TYPE B only; never "according to A&T, DL…" | Abstract, p. 1 (UCL copy of the JPE article) |
| Alonso, Dessein & Matouschek (2008) | Decentralization can dominate centralization through better use of dispersed information. This is a boundary statement: it lies outside the complete-information model (P3/Q08) | Abstract and §2 (LSE accepted ms) |
| Kleinert et al. (2021) | (a) Optimistic and pessimistic versions differ when the lower-level solution set is not a singleton. (b) The KKT/strong-duality single-level reformulation presupposes a convex lower level with a CQ; integer lower-level variables make it nonconvex. (c) Moore & Bard (1990) initiated discrete bilevel studies | §1 (after eq. 1), §3.2, §5 (TRR154 preprint) |
| Ben-Tal, El Ghaoui & Nemirovski (2009) | Set-based robustness over an uncertainty set U. Robust feasibility is unchanged when U_i is replaced by its convex hull, and U can be taken as a product of constraint-wise sets. **Not** the block-affine vertex property of the objective, which stays proved in-house (TYPE C) | Preface p. xii; Ch. 1 §1.2 pp. 12–13 (author-hosted manuscript, May 2009) |
| Lempert, Popper & Bankes (2003) | Choose strategies that are robust across a wide range of plausible futures rather than optimal for one set of expectations | Preface p. iii; Summary p. xiv (RAND PDF) |

**B. In the 59a list: M1–M4 object anchors (row 2.7; each work's own finding, TYPE B for the modelling consequence)**

| key | permitted claim | where the support was found |
|---|---|---|
| Elish (2019) | Responsibility can be misattributed to a human with limited control | Abstract p. 40 |
| Green (2022) | Oversight policies: people are often unable to perform oversight (government algorithms) | Abstract p. 1 |
| Vaccaro et al. (2024) | On average, human–AI combinations performed worse than the best of humans or AI alone; there were losses in decision tasks | Abstract (arXiv v2) |
| Dietvorst et al. (2015) | People lose confidence in algorithms faster after seeing them err | Abstract (advance-online version) |
| Logg et al. (2019) | People adhere more to advice they believe comes from an algorithm | Abstract (HBS WP 17-086) |
| Lebovitz et al. (2022) | Opacity, plus AI results that diverge from initial judgment, raises uncertainty | Abstract (WRAP accepted ms) |
| Bansal et al. (2021) | Explanations raise acceptance regardless of correctness | Abstract (arXiv v3) |
| Amershi et al. (2019) | Integrating ML into software workflows has AI-specific engineering challenges. This supports existence, not cost magnitude | Abstract |
| Sculley et al. (2015) | Massive ongoing maintenance costs in ML systems | Abstract |
| Breck et al. (2017) | 28 specific tests and monitoring needs | Abstract |
| Raji et al. (2020) | An end-to-end internal algorithmic audit framework | Abstract (arXiv) |
| Mökander et al. (2021) | Ethics-based auditing (EBA) is a structured assessment of behaviour against principles | Abstract (arXiv accepted pre-print) |
| NIST (2023) | A voluntary AI risk-management framework. Structural reference only | p. 2 |

**C. Not in the 59a list: may enter only after the researcher adds them to the reference list, and only as analogue/contrast (all are FULLTEXT_VERIFIED, from working or accepted versions)**

| key | permitted claim | support located | mandatory framing |
|---|---|---|---|
| Alonso & Matouschek (2008, REStud) | The delegation problem: the principal commits to a set of decisions, and the agent picks his preferred one | Abstract (LSE accepted ms) | Their agent is informed and biased. In v2.2 the loss is instrument incompleteness under complete information |
| Armstrong & Vickers (2010, Econometrica) | The principal determines the set of projects the agent may choose from; the agent picks the permitted project that best serves her | Abstract and §1 p. 1 (June 2008 WP) | Their principal does not know the available projects (asymmetric information) |
| Stoye (2011, JET) | Minimax regret is menu-dependent and violates IIA | pp. 2 and 7 (author version, 14 July 2011) | E.1/E.2-adaptive and W6b stay TYPE C in-model instances of a known property |

## 3. Items that stay in research notes (NO)

- **In the list, abstract-only in this run:** Colson et al. (2007), Dempe (2002), Moore & Bard (1990), Wiesemann et al. (2013), Sambamurthy & Zmud (1999), A. E. Brown & Grant (2005), C. V. Brown & Magill (1994), Tiwana & Konsynski (2010), Benaroch & Kauffman (1999), Angrist et al. (1996), Parasuraman et al. (2000), Shrestha et al. (2019), Raisch & Krakowski (2021), Kellogg et al. (2020), Papagiannidis et al. (2025).
  - Their **existing** 59a sentences keep resting on 59a's own App. B records. Some of those records are FULL_TEXT: Brown & Grant N57/N75, Raisch S2, Kellogg N14.
  - **No new or more detailed claim** in V1.8.6 may be attached to them.
  - In particular, the plan row 2.1 TYPE A claims (opt/pess selection; integer lower level / KKT) should be carried by **Kleinert et al. (2021)**. Colson, Dempe, Moore & Bard and Wiesemann can stay only as the existing general bilevel background.
  - Wiesemann's green-OA full text exists (MIT DSpace) but was rate-limited. Retry before giving it a specific claim.
- **In the list, SECONDARY_ONLY:** Savage (1951). Keep 59a's PARTIAL wording (E3/N34) unchanged. Stoye's working paper (p. 2) is full-text secondary support for the attribution.
- **In the list, UNVERIFIED by RV:** ISO/IEC 42001.
- **Not in the list:**
  - ABSTRACT only: Harris & Raviv (1996) (the abstract has no "ceiling" wording), Topkis (1978), Topkis book, Milgrom & Shannon (1994), Howard (1966). Howard's abstract notes that the joint value of removing several uncertainties differs from the sum of the separate values, which is the closest analogue to E.9.
  - SECONDARY_ONLY: Holmström (1984) (bibliographic record only via Alonso & Matouschek's reference list; no Crossref record, no pages), Raiffa & Schlaifer (1961) (only 1961 book reviews in Crossref), Kouvelis & Yu (1997) (via Ben-Tal and Lempert), Chernoff (1954) (via Stoye; the pack's specific attribution to Chernoff is not located).
  - UNVERIFIED, Crossref identity only: Jensen & Meckling (1976), Laffont & Martimort (2002), Harris & Raviv (1998), Averbakh (2001), Averbakh & Lebedev (2004), Manski (2003), Loridan & Morgan (1996).
  - UNVERIFIED, no Crossref match: Weill & Ross (2004).
  - UNVERIFIED, literature streams with no named work: Braess-type "more options can hurt", VOI complementarity/non-submodularity, and the capital-budget-ceiling literature.

## 4. Impact on manuscript integration

1. **TYPE C results are stated without analogue citations.** DL-2o to DL-6, GS-1/GS-2/GS-N/GS-4, Lemma I, D4–D6, Lemma M, E.1–E.10, R1–R5 and G1–G8 go into the main text as in-model results of this thesis, with the mandatory scope sentence. None of them is written as "according to X".
2. **The plan row 2.1 sentence** ("…其機制在授權／委任與資本預算文獻中有已知類比（待查證）…") must not appear in the main text while the analogues remain unadded. Use one of these instead:
   - (i) drop the analogue clause from the main text and keep it in research notes or Appendix E (TO-VERIFY list); or
   - (ii) if the researcher adds Alonso & Matouschek (2008) and/or Armstrong & Vickers (2010) to the reference list, write the analogue clause citing only them, with the contrast framing in §2C.
   - Capital-budget ceilings (Harris & Raviv) stay out in both cases.
3. **The plan row 2.5/2.9 VOI and minimax-regret positioning:**
   - The menu-dependence analogue may cite only Stoye (2011), and only if it is added.
   - Chernoff, Howard, Raiffa & Schlaifer, Kouvelis & Yu, Averbakh, Manski, Topkis, Milgrom & Shannon and Loridan & Morgan stay in notes.
   - Where the manuscript needs to name these analogues at all, they appear only as "related literature not yet verified", in research notes or Appendix E, **never in the main text**.
4. **Bilevel TYPE A anchors (plan row 2.1):** replace or extend with Kleinert et al. (2021) for the opt/pess definition and the convexity requirement of KKT reformulation. The wording must follow the located text ("presupposes a convex lower level; integer lower levels are nonconvex"), not "KKT is invalid".
5. **Robustness (06 §6):** Ben-Tal et al. may anchor set-based robustness and convex-hull invariance. The vertex property of block-affine objectives remains proved in-house (TYPE C), as 06 §6 already states.
6. **Governance anchors (plan row 2.2):**
   - The existing 59a sentences on Sambamurthy & Zmud and Brown & Grant can stay.
   - No new detailed claim may be added to them in V1.8.6.
   - Aghion & Tirole stays TYPE B conceptual only.
   - Weill & Ross stays secondary-only.
7. **The 42 erratum, numbers, P1–P8 and solver are unaffected.** This is a citation-only report.

Researcher decision items raised (not decided here):
- (a) whether to add Alonso & Matouschek (2008), Armstrong & Vickers (2010) and Stoye (2011) to the reference list. If they are added, the final published versions should be checked for pagination;
- (b) a retry of the Wiesemann (MIT DSpace) and Brown & Grant (AISeL) full texts.

R3_UNVERIFIED_REFERENCES_ALLOWED_IN_MAIN=0
