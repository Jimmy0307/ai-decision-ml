"""Build OUT/07_V1_8_6_REFERENCE_VERIFICATION.csv from the RV verification records."""
import csv
from collections import Counter
from pathlib import Path

OUT = Path(r"C:\NTUST_PAPER\outputs\00_CURRENT\V1_8_6_THEORY_INTEGRATION_20261018")
COLS = ["citation_key", "claim_supported", "source_type", "fulltext_available",
        "verification_status", "exact_support_location", "allowed_in_main_text", "notes",
        "bibliographic_identity", "in_59a_reference_list", "theory_pack_location"]

FT, AB, SE, UN = "FULLTEXT_VERIFIED", "ABSTRACT_VERIFIED", "SECONDARY_ONLY", "UNVERIFIED"

R = []
def row(key, claim, stype, fta, status, loc, allowed, notes, ident, in59a, tp):
    R.append(dict(zip(COLS, [key, claim, stype, fta, status, loc, allowed, notes, ident, in59a, tp])))

# ---------------- In 59a reference list: theory anchors ----------------
row("Aghion_Tirole_1997",
    "Formal authority (the right to decide) and real authority (effective control over decisions) are distinct and can diverge; real authority depends on information (conceptual anchor only for Auth vs Eff / G_j(gamma) vs Eff_H; NOT for the DL mechanism)",
    "journal article (JPE 105(1):1-29)", "YES (UCL Discovery copy of published JPE article, discovery.ucl.ac.uk/17678)",
    FT, "Abstract, p. 1: 'This paper develops a theory of the allocation of formal authority (the right to decide) and real authority (the effective control over decisions) within organizations' ... 'Real authority is determined by the structure of information, which in turn depends on the allocation of formal authority. An increase in an agent's real authority promotes initiative but results in a loss of control for the principal.'",
    "YES",
    "Main text only as TYPE B conceptual separation. Their mechanism is informational; v2.2 is complete-information (P3): never write 'according to Aghion & Tirole, DL...'. Consistent with 59a App. B N8.",
    "59a ref list DOI 10.1086/262063 (matches published header)", "YES",
    "01 §9 table ('formal authority and real authority can diverge -> separate Auth from Eff'); 02 §7 ('Formal authority ... vs real authority ... TYPE B (conceptual anchor only)'); 03 §10; 08 §7; 10 row 2.2")
row("Alonso_Dessein_Matouschek_2008",
    "Decentralization can dominate centralization because dispersed local information is used better (an information advantage excluded by the complete-information model; boundary statement P3 / Q08 sidecar)",
    "journal article (AER 98(1):145-179)", "YES (LSE Research Online author accepted version, eprint 58664)",
    FT, "Abstract (accepted ms p. 1): 'As a result, decentralization can dominate centralization even when coordination is extremely important relative to adaptation.'; Section 2 (related literature): 'Decentralization may nevertheless be strictly preferred because it allows for a better use of dispersed information.'",
    "YES",
    "Accepted-manuscript pagination; published p. 145 per 59a N31. Use only as boundary (outside the model). Consistent with 59a App. B N31.",
    "Crossref: 10.1257/aer.98.1.145, AER 98(1) 145-179 (matches 59a)", "YES",
    "02 §7 ('Coordination vs adaptation; decentralization's informational benefit is outside this model ... TYPE B (boundary statement; P3)'); 04 §8; 08 §1/§7; 10 row 2.4")
row("Kleinert_Labbe_Ljubic_Schmidt_2021",
    "(a) Optimistic vs pessimistic bilevel versions differ when the lower-level solution set is not a singleton; (b) single-level KKT / strong-duality reformulation requires a convex lower level with a constraint qualification, and integer lower-level variables make the lower level nonconvex (hence KKT reformulation is not available for integer lower levels); (c) Moore & Bard (1990) initiated bilevel problems with discrete variables",
    "survey article (EURO J. Comput. Optim. 9, Art. 100007)", "YES (TRR154 preprint 'bilevel-survey-preprint.pdf', opus4.kobv.de; publisher PDF blocked 403)",
    FT, "Preprint §1 after eq. (1): 'Most of the time, we will consider the optimistic version ... the leader also optimizes over the lower-level outcome y in S(x) if ... S(x) is not a singleton. On the contrary, the pessimistic version is given by ...' (refers to Wiesemann et al. (2013) for the general pessimistic setting); §1: 'the solution techniques are very much different depending on whether the lower-level problem is continuous and convex or whether it is nonconvex, e.g., due to the presence of integer variables'; §3.2 Single-Level Reformulations: 'If the lower-level problem ... is convex and satisfies a suitable constraint qualification ... then one can reformulate the bilevel problem into a single-level optimization problem ... uses the KKT conditions ... or a strong duality theorem'; §5: 'Moore and Bard (1990) initiated the studies of bilevel optimization problems involving discrete variables.'",
    "YES",
    "Preprint text; published article-number pagination not checked. The 'KKT invalid for integer lower level' wording should be phrased as 'KKT/duality reformulation presupposes a convex lower level; integer lower levels are nonconvex' (exact text located). Can carry the TYPE A claims of plan row 2.1 that Colson/Dempe/Moore&Bard/Wiesemann could only support at abstract level.",
    "59a ref list DOI 10.1016/j.ejco.2021.100007; OpenAlex confirms gold OA", "YES",
    "02 §7 ('Bilevel (leader-follower) formulation; optimistic vs pessimistic follower selection; integer lower levels; KKT reformulation invalid for integer lower levels | TYPE A'); 10 row 2.1")
row("Colson_Marcotte_Savard_2007",
    "Bilevel (leader-follower) formulation; optimistic vs pessimistic selection (TYPE A per pack)",
    "survey article (Ann. Oper. Res. 153(1):235-256)", "NO (author copy iro.umontreal.ca blocked by bot protection; Springer paywall)",
    AB, "Abstract only (IAOR/59a N26: 'This paper is devoted to bilevel optimization, a branch of mathematical programming'); opt/pess passage not located",
    "NO",
    "Keep existing 59a citation for general bilevel background; do not attach the opt/pess or integer-lower-level TYPE A claim to it in new text. Use Kleinert et al. (2021) for those claims.",
    "Crossref: 10.1007/s10479-007-0176-2, 153(1) 235-256 (matches 59a)", "YES",
    "02 §7 TYPE A row; 03 §10; 04 §8; 06 §6; 10 row 2.1")
row("Dempe_2002",
    "Foundations of bilevel programming; distinction of unique vs non-unique lower-level solution (optimistic/pessimistic bounds); opt/pess discontinuity",
    "monograph (Kluwer, NOIA Vol. 61)", "NO",
    AB, "Publisher description only (OpenAlex/59a N27: 'Bilevel programming problems are hierarchical optimization problems where the constraints of one problem ... are defined in part by a second parametric optimization problem')",
    "NO",
    "Existing 59a use stands on its own App. B record; no new claim may rest on it.",
    "Crossref/OpenAlex: 10.1007/b101970 (matches 59a)", "YES",
    "02 §7; 03 §10; 04 §8; 06 §6 ('Optimistic vs pessimistic bilevel discontinuity: Dempe (2002), Wiesemann et al. (2013) (in list)'); 10 row 2.1")
row("Moore_Bard_1990",
    "Mixed-integer linear bilevel problems; integer lower levels need specialised methods (KKT not used)",
    "journal article (Oper. Res. 38(5):911-921)", "NO (closed)",
    AB, "Abstract (OpenAlex index): 'A two-person, noncooperative game in which the players move in sequence can be modeled as a bilevel optimization problem ... decision variables are variously partitioned into continuous and discrete sets ... extremely difficult to solve, even by complete enumeration ... two of the three standard fathoming rules common to branch and bound cannot be applied fully.' No KKT statement in the abstract.",
    "NO",
    "Abstract supports 'sequential game = bilevel; discrete variables make it hard' only. Secondary: Kleinert §5 says Moore & Bard initiated discrete bilevel studies.",
    "Crossref: 10.1287/opre.38.5.911 (matches 59a)", "YES",
    "02 §7 TYPE A row; 10 row 2.1")
row("Wiesemann_Tsoukalas_Kleniati_Rustem_2013",
    "Pessimistic bilevel selection (constraints must hold for every lower-level optimal solution)",
    "journal article (SIAM J. Optim. 23(1):353-380)", "NO (MIT DSpace HTTP 429; Imperial Spiral bot-protected)",
    AB, "Abstract (OpenAlex index): 'We study a variant of the pessimistic bilevel optimization problem, which comprises constraints that must be satisfied for any optimal solution of a subordinate (lower-level) optimization problem.'",
    "NO",
    "Full text exists as green OA (MIT DSpace 1721.1/79608) but could not be read in this run; retry later. Kleinert et al. (2021) §1 (full text) defines the pessimistic version and refers to Wiesemann et al. (2013).",
    "Crossref/OpenAlex: 10.1137/120864015 (matches 59a)", "YES",
    "02 §7; 03 §10; 04 §8; 06 §6 ('Wiesemann et al. (2013) for pessimistic bilevel selection'); 10 row 2.1")
row("Sambamurthy_Zmud_1999",
    "IT governance arrangements = patterns of authority (decision rights) for key IT activities; centralized/decentralized/federal modes; contingent (TYPE A definitional / TYPE B mapping to (y,gamma,e))",
    "journal article (MISQ 23(2):261-289)", "NO (closed)",
    AB, "Abstract (OpenAlex index): 'IT governance arrangements refers to the patterns of authority for key IT activities in business firms ... three primary modes of IT governance have become prevalent: centralized, decentralized, and the federal mode.'",
    "NO",
    "Abstract wording directly matches the definitional claim, but status is abstract-only (59a N5 also ABSTRACT_ONLY). Existing 59a sentence may stay; do not add new detailed claims.",
    "Crossref/OpenAlex: 10.2307/249754 (matches 59a)", "YES",
    "01 §9; 02 §7; 03 §10; 10 row 2.2")
row("Brown_AE_Grant_2005",
    "IT governance as the framework for decision rights and accountabilities; centralized/decentralized/federal forms (review)",
    "review article (CAIS 15:696-712)", "NO in this run (AISeL PDF behind Cloudflare challenge; landing page read)",
    AB, "AISeL landing page abstract (paraphrased by fetch tool): prior work on IT decision rights and IT loci of control; two research streams. 59a App. B N57/N75 record FULL_TEXT p. 698 and p. 701 quotes, not re-read by RV.",
    "NO",
    "59a's existing use is backed by 59a's own full-text record (N57, N75); RV could not re-locate it, so no NEW claim may rest on it until the PDF is re-read. Weill & Ross (2004) only via this review (secondary).",
    "Crossref/OpenAlex: 10.17705/1CAIS.01538 (matches 59a)", "YES",
    "01 §9; 02 §7; 03 §10; 10 rows 2.2-2.3")
row("Brown_CV_Magill_1994",
    "Decentralized, centralized or hybrid locus of IS responsibility",
    "journal article (MISQ 18(4):371-403)", "NO (closed)",
    AB, "Abstract (OpenAlex index): '... a firm's IS organization design decision for a decentralized, centralized, or \"hybrid\" locus of responsibility ...'",
    "NO", "Abstract-only (= 59a N58).",
    "Crossref/OpenAlex: 10.2307/249521 (matches 59a)", "YES", "02 §7; 03 §10; 10 row 2.2")
row("Tiwana_Konsynski_2010",
    "Decentralization of IT governance complements IT architecture modularity (governance as allocation of decision rights, background)",
    "journal article (ISR 21(2):288-304)", "NO (closed)",
    AB, "Abstract (OpenAlex index): '... IT architecture modularity helps sustain IT alignment by increasing IT agility, and that decentralization of IT governance strengthens this relationship.'",
    "NO", "Abstract-only (= 59a N59). OpenAlex lists publication_year 2009 (online-first); issue 21(2) 2010.",
    "Crossref/OpenAlex: 10.1287/isre.1080.0206 (matches 59a)", "YES", "02 §7; 03 §10; 10 row 2.2")
row("Elish_2019",
    "Responsibility may be misattributed to a human actor with limited control over an automated system (moral crumple zone) -> M1 Eff/Acc distinction, Pi_notM1 (TYPE B)",
    "journal article (ESTS 5:40-60)", "YES (ESTS open-access PDF)",
    FT, "Abstract, p. 40: 'I introduce the concept of a moral crumple zone to describe how responsibility for an action may be misattributed to a human actor who had limited control over the behavior of an automated or autonomous system.'",
    "YES", "TYPE B only; = 59a S5.", "DOI 10.17351/ests2019.260 printed on PDF header (matches 59a)", "YES",
    "01 §3 Pi_notM1 ('Elish's (2019) misallocation of responsibility under limited control (TYPE B anchors)'); 01 §9; 10 row 2.2")
row("Green_2022",
    "Policies requiring human oversight need not yield effective oversight (people often unable to perform the oversight functions) - public-sector algorithms",
    "journal article (CLSR 45, Art. 105681)", "YES (published version PDF, CC BY, arXiv 2109.05067)",
    FT, "Abstract, p. 1: 'First, evidence suggests that people are unable to perform the desired oversight functions. Second, as a result of the first flaw, human oversight policies legitimize government uses of faulty and controversial algorithms ...'",
    "YES", "TYPE B; scope = government algorithms (do not generalise to the enterprise as a finding). = 59a N56.",
    "Header 'computer law & security review 45 (2022) 105681' (matches 59a)", "YES", "01 §9; 10 row 2.2")
row("Savage_1951",
    "Minimax-regret criterion as a decision rule (attribution)",
    "journal article (JASA 46(253):55-67)", "NO (closed; no OA copy)",
    SE, "No primary text. Secondary: Stoye (2011, author WP p. 2): 'The minimax regret decision criterion was suggested in Savage's [50] reading of Wald [65]' (ref [50] = Savage, JASA 46 (1951) 55-67).",
    "NO",
    "Keep 59a's existing PARTIAL attribution (E3/N34) unchanged; no new claim. If the manuscript wants a full-text-backed attribution sentence, Stoye (2011) is FULLTEXT_VERIFIED for that sentence but is not in the list (researcher decision to add).",
    "Crossref: 10.1080/01621459.1951.10500768 (matches 59a)", "YES",
    "05 §7 ('Savage (1951) - in list, PARTIAL attribution'); 06 §6; 10 row 2.5")
row("Ben-Tal_ElGhaoui_Nemirovski_2009",
    "Set-based (uncertainty-set) robustness: an uncertain problem is a family over an uncertainty set U; robust feasibility is unchanged when U_i is replaced by its convex hull and U can be taken as the direct product of constraint-wise sets (TYPE B for Theta_g / product polytopes)",
    "monograph (Princeton UP)", "YES (author-hosted pre-publication manuscript 'ROBook May 2009', www2.isye.gatech.edu/~nemirovs/FullBookDec11.pdf)",
    FT, "Preface p. xii: 'an uncertain LP problem is defined as a collection ... of LP programs of a common structure with the data (c, A, b) varying in a given uncertainty set U'; Ch. 1 §1.2, p. 12: 'If x is a robust feasible solution of (Ci), then x remains robust feasible when we extend the uncertainty set Ui to its convex hull Conv(Ui)'; p. 13: '... U is the direct product of these sets.'",
    "YES",
    "Pre-publication manuscript; print pagination not cross-checked. Supports set-based robustness and constraint-wise convex-hull invariance only. It does NOT state the block-affine/multilinear vertex property of the objective used in Thm R1 - that remains proved in-house (TYPE C), as 06 §6 already says.",
    "59a ref DOI 10.1515/9781400831050; manuscript title page 'Princeton University Press ... Copyright 2009'", "YES",
    "05 §7 ('Set-based (uncertainty-set) robustness; product polytopes as uncertainty sets | TYPE B'); 06 §6; 07 §8; 10 row 2.5")
row("Lempert_Popper_Bankes_2003",
    "Evaluate strategies across a wide range of plausible futures (robust rather than optimal for one forecast)",
    "RAND report MR-1626-RPC", "YES (RAND PDF)",
    FT, "Preface p. iii: 'systematic consideration of a multiplicity of plausible futures in a way that will enhance our ability to make good decisions today in the face of deep uncertainty'; Summary p. xiv: 'rather than seeking strategies that are optimal for some set of expectations about the long-term future, this approach seeks near-term strategies that are robust--i.e., that perform reasonably well compared to the alternatives across a wide range of plausible futures'",
    "YES", "TYPE B. = 59a N33. Lempert also uses (relative) regret across scenarios citing Kouvelis & Yu (1997) (Ch. 3, eq. 3.2).",
    "59a ref DOI 10.7249/MR1626", "YES", "05 §7; 10 row 2.5")
row("Benaroch_Kauffman_1999",
    "Option value of staged IT investment (dynamic layer only)",
    "journal article (ISR 10(1):70-86)", "NO (closed)",
    AB, "Abstract (OpenAlex index): '(1) it provides a formal theoretical grounding for the validity of the Black-Scholes option pricing model in the context of the spectrum of capital budgeting methods that might be employed to assess IT investments'",
    "NO", "Abstract-only (= 59a N23). Existing 59a use for 'option value excluded from the static objective' unchanged.",
    "Crossref/OpenAlex: 10.1287/isre.10.1.70 (matches 59a)", "YES", "05 §7; 10 row 2.6")
row("Angrist_Imbens_Rubin_1996",
    "Identification is assumption-dependent (loose; does NOT support G1-G8)",
    "journal article (JASA 91(434):444-455)", "NO (closed)",
    AB, "Abstract (OpenAlex index): framework for causal inference with imperfect compliance using instrumental variables",
    "NO", "Plan row 2.10 itself says it does not support G1-G8. = 59a N73 (ABSTRACT_ONLY).",
    "Crossref/OpenAlex: 10.1080/01621459.1996.10476902 (matches 59a)", "YES", "07 §8; 10 row 2.10")

# ---------------- In 59a list: M1-M4 object anchors (plan row 2.7) ----------------
row("Parasuraman_Sheridan_Wickens_2000", "Types and levels of automation -> A_k, m_k (TYPE B)",
    "journal article (IEEE SMC-A 30(3):286-297)", "NO (closed; no OA copy reached)", AB,
    "Abstract (OpenAlex index): 'We outline a model for types and levels of automation that provides a framework and an objective basis for making such choices.'",
    "NO", "Abstract supports the anchor; abstract-only status.", "Crossref/OpenAlex 10.1109/3468.844354", "YES", "01 §9; 10 row 2.7")
row("Shrestha_BenMenahem_vonKrogh_2019", "Full delegation, sequential and aggregated human-AI decision structures -> m_k",
    "journal article (CMR 61(4):66-83)", "NO (closed)", AB,
    "Abstract (OpenAlex index) identifies human vs AI decision idiosyncrasies along five contingency factors; 59a S1 quote 'full human to AI delegation' (Abstract)",
    "NO", "= 59a S1 ABSTRACT_ONLY.", "Crossref/OpenAlex 10.1177/0008125619862257", "YES", "01 §9; 10 row 2.7")
row("Raisch_Krakowski_2021", "Automation and augmentation not cleanly separable -> m_k x A_k",
    "journal article (AMR 46(1):192-210)", "NO in this run (AOM full text not reached)", AB,
    "Abstract (OpenAlex index): automation vs augmentation concepts; 59a S2 FULL_TEXT quote 'augmentation cannot be neatly separated from automation' (Abstract, p. 192) not re-read by RV",
    "NO", "Existing 59a use backed by 59a S2 record.", "Crossref/OpenAlex 10.5465/amr.2018.0072", "YES", "01 §9; 10 row 2.7")
row("Vaccaro_Almaatouq_Malone_2024", "Human-AI combinations are not on average better than the better of human or AI alone; losses in decision tasks",
    "journal article (Nat. Hum. Behav. 8(12):2293-2303)", "YES (arXiv 2405.06087v2, 29 Oct 2024)", FT,
    "Abstract (arXiv v2 p. 1): 'we found that, on average, human-AI combinations performed significantly worse than the best of humans or AI alone (Hedges' g = -0.23 ...). Second, we found performance losses in tasks that involved making decisions ...'",
    "YES", "arXiv version; published pagination not checked. = 59a S3.", "OpenAlex 10.1038/s41562-024-02024-1", "YES", "01 §9; 10 row 2.7")
row("Dietvorst_Simmons_Massey_2015", "Algorithm aversion after seeing algorithms err -> rho direction not fixed",
    "journal article (JEP:G 144(1):114-126)", "YES (Wharton-hosted advance-online version, header 'JEP:G 2014, Vol. 143, No. 6, 000')", FT,
    "Abstract p. 1: 'people more quickly lose confidence in algorithmic than human forecasters after seeing them make the same mistake'",
    "YES", "Advance-online version header shows 2014 vol./issue; final print is 2015 144(1) per 59a/Crossref - cite the print record.", "DOI 10.1037/xge0000033 on PDF", "YES", "01 §9; 10 row 2.7")
row("Logg_Minson_Moore_2019", "Algorithm appreciation -> rho direction not fixed",
    "journal article (OBHDP 151:90-103)", "YES (HBS Working Paper 17-086)", FT,
    "Abstract (WP p. 4): 'results from six experiments show that lay people adhere more to advice when they think it comes from an algorithm than from a person'",
    "YES", "Working-paper version; published p. 90 per 59a N16 not re-checked.", "59a ref DOI 10.1016/j.obhdp.2018.12.005", "YES", "01 §9; 10 row 2.7")
row("Lebovitz_LifshitzAssaf_Levina_2022", "Engagement with AI under opacity varies; AI results diverging from initial judgment raise uncertainty -> rho",
    "journal article (Org. Sci. 33(1):126-148)", "YES (Warwick WRAP author accepted manuscript)", FT,
    "Abstract (AAM p. 2): 'this opacity resulted in professionals experiencing increased uncertainty because AI tool results often diverged from their initial judgment without providing underlying reasoning'",
    "YES", "AAM pagination. = 59a N17.", "59a ref DOI 10.1287/orsc.2021.1549", "YES", "01 §9; 10 row 2.7")
row("Kellogg_Valentine_Christin_2020", "Algorithmic control and worker resistance -> rho Reject/Bypass",
    "review article (AMA 14(1):366-410)", "NO in this run (NSF PAR link failed)", AB,
    "Abstract (OpenAlex index): 'We use Edwards' (1979) perspective of \"contested terrain\" ... to synthesize the interdisciplinary research on algorithms at work.'",
    "NO", "Existing 59a use backed by 59a N14 record.", "Crossref/OpenAlex 10.5465/annals.2018.0174", "YES", "01 §9; 10 row 2.7")
row("Bansal_et_al_2021", "Explanations raise acceptance of AI recommendations regardless of correctness -> EAX as rho-key",
    "conference paper (CHI '21)", "YES (arXiv 2006.14779v3)", FT,
    "Abstract p. 1: 'explanations increased the chance that humans will accept the AI's recommendation, regardless of its correctness'",
    "YES", "arXiv author version. = 59a S4.", "59a ref (CHI 2021)", "YES", "01 §9; 10 row 2.7")
row("Amershi_et_al_2019", "Integrating ML into software workflows raises AI-specific engineering challenges -> M2 costs in C^impl (existence, not magnitude)",
    "conference paper (ICSE-SEIP 2019)", "YES (Microsoft Research-hosted PDF)", FT,
    "Abstract p. 1: 'we have identified three aspects of the AI domain that make it fundamentally different from prior software application domains: 1) discovering, managing, and versioning the data ... 2) model customization and model reuse require very different skills ... 3) AI components are more difficult to handle as distinct modules'",
    "YES", "Supports 'substantive', not cost magnitude.", "59a ref", "YES", "01 §9; 10 row 2.7")
row("Sculley_et_al_2015", "ML systems incur ongoing maintenance costs -> M2 costs",
    "conference paper (NeurIPS 28)", "YES (NeurIPS proceedings PDF)", FT,
    "Abstract p. 1: 'we find it is common to incur massive ongoing maintenance costs in real-world ML systems'", "YES", "= 59a N13.", "59a ref", "YES", "01 §9; 10 row 2.7")
row("Breck_et_al_2017", "Testing and monitoring as recordable, gradable activities -> ev_k, EA_k",
    "conference paper (IEEE Big Data 2017)", "YES (Google Research-hosted PDF)", FT,
    "Abstract p. 1: 'we present 28 specific tests and monitoring needs, drawn from experience with a wide range of production ML systems'", "YES", "= 59a N18.", "59a ref DOI 10.1109/BigData.2017.8258038", "YES", "01 §9; 10 row 2.7")
row("Raji_et_al_2020", "Internal algorithmic audit framework across the lifecycle -> EA_k",
    "conference paper (FAT* 2020)", "YES (arXiv 2001.00973v1)", FT,
    "Abstract p. 1: 'we introduce a framework for algorithmic auditing that supports artificial intelligence system development end-to-end, to be applied throughout the internal organization development lifecycle'", "YES", "= 59a N19.", "59a ref", "YES", "01 §9; 10 row 2.7")
row("Mokander_et_al_2021", "Ethics-based auditing as a structured, assessable governance mechanism -> EA_k",
    "journal article (Sci. Eng. Ethics 27(4), Art. 44)", "YES (arXiv 2110.10980 accepted pre-print)", FT,
    "Abstract p. 1: 'we define EBA as a structured process whereby an entity's present or past behaviour is assessed for consistency with relevant principles or norms'", "YES", "Pre-print pagination.", "59a ref DOI 10.1007/s11948-021-00319-4", "YES", "01 §9; 10 row 2.7")
row("Papagiannidis_Mikalef_Conboy_2025", "Structural/procedural/relational responsible-AI governance practices (structural reference only)",
    "review article (JSIS 34(2), Art. 101885)", "NO (not reached)", AB,
    "OpenAlex index shows highlights only; 59a N7 abstract quote via OpenAlex reconstruction", "NO", "Abstract-only.", "Crossref/OpenAlex 10.1016/j.jsis.2024.101885", "YES", "01 §9")
row("NIST_2023_AI_RMF", "Voluntary AI risk-management structure (structural reference only, never a parameter source)",
    "government framework (NIST AI 100-1)", "YES (nvlpubs.nist.gov PDF)", FT,
    "p. 2 (PDF p. 7): 'to help manage the many risks of AI and promote trustworthy and responsible development and use of AI systems. The Framework is intended to be voluntary ...'", "YES", "= 59a N9.", "DOI 10.6028/NIST.AI.100-1", "YES", "01 §9")
row("ISO_IEC_42001_2023", "AI management system requirements (structural reference only)",
    "standard", "NO (paywalled standard)", UN,
    "Not checked by RV (59a N10 ABSTRACT_ONLY: official abstract)", "NO", "No new claim may rest on it.", "59a ref (iso.org/standard/42001)", "YES", "01 §9")

# ---------------- NOT in 59a list ----------------
row("Weill_Ross_2004", "IT governance archetypes / decision rights (book)",
    "book (HBS Press)", "NO", UN, "No primary text; no Crossref record found by bibliographic query; only via A. E. Brown & Grant (2005) p. 707 per 59a N6/N75",
    "NO", "Secondary citation only, never an anchor for M1 (plan row 2.3).", "NOT CONFIRMED (no Crossref match)", "NO",
    "01 §9 ('only as secondary citation via Brown & Grant (2005) - to verify; do not cite directly'); 10 row 2.3")
row("Jensen_Meckling_1976", "Principal-agent misalignment / agency costs (framing, contrast)",
    "journal article", "NO", UN, "Crossref metadata only; no abstract/full text read",
    "NO", "Identity only. Contrast-only use per plan row 2.8 would still need full text.",
    "Crossref: 10.1016/0304-405x(76)90026-x, J. Financial Economics 3(4) 305-360, 1976-10", "NO", "02 §7 ('Candidates to verify before citing: Jensen & Meckling (1976) ...'); 10 rows 2.8, §12")
row("Holmstrom_1984", "Optimal delegation: principal restricts the agent's permitted set (delegation problem)",
    "book chapter", "NO", SE,
    "No Crossref record. Secondary: Alonso & Matouschek (2008, AAM) reference list: 'Holmstrom, B. ... (1984): \"On the Theory of Delegation,\" in Bayesian Models in Economic Theory, ed. by M. Boyer, and R. Kihlstrom. North-Holland, New York.' (no pages given); Armstrong & Vickers (2008 WP) describe the 'Holmstrom (1984) setting' of the delegation problem.",
    "NO", "Bibliographic details only as printed in citing works; no pages asserted.", "NOT IN CROSSREF; secondary bibliographic record only", "NO",
    "02 §7; 03 §10 ('Holmstrom (1984); Alonso & Matouschek (2008, REStud) ... to verify'); 11 A4; 10 rows 2.8, R-4")
row("Alonso_Matouschek_2008", "Delegation as the principal committing to a set of decisions from which the agent picks his preferred one (optimal delegation set) - known analogue of DL/GS mechanism",
    "journal article (REStud 75(1):259-293)", "YES (LSE Research Online author accepted version, eprint 58665)", FT,
    "Abstract (AAM p. 1): 'The contracting problem reduces to a delegation problem in which the principal commits to a set of decisions from which the agent chooses his preferred one. We characterize the optimal delegation set ...'",
    "YES (conditional)",
    "Allowed only after it is ADDED to the reference list, and only as analogue/contrast: their agent is informed and biased (hidden information); here the loss comes from instrument incompleteness under complete information. Must not be used to claim DL-x/GS-x results.",
    "Crossref: 10.1111/j.1467-937x.2007.00471.x, REStud 75(1) 259-293, 2008-01", "NO",
    "02 §7 ('optimal delegation / permitted-set design ... TO VERIFY'); 03 §10; 11 A4; 10 rows 2.8, R-4")
row("Laffont_Martimort_2002", "Principal-agent theory (framing, contrast)", "monograph (Princeton UP)", "NO", UN,
    "Crossref metadata only", "NO", "Identity only.", "Crossref: 10.1515/9781400829453 'The Theory of Incentives' (Princeton UP, issued 2002-12-31)", "NO", "02 §7; 10 row 2.8")
row("Armstrong_Vickers_2010", "Delegated project choice: principal determines the set of projects from which the agent may choose; agent selects the permitted project that best serves her interests",
    "journal article (Econometrica 78(1):213-244)", "YES (June 2008 working-paper version, UCL Discovery eprint 14431; published abstract via OpenAlex)", FT,
    "WP Abstract p. 1: 'We present a model in which a principal delegates the choice of project to an agent with different preferences. The principal determines the set of projects from which the agent may choose.'; §1 p. 1: 'The agent ... will select from her available projects the permitted project that best serves her interests.' Published abstract (OpenAlex) has the same first two sentences.",
    "YES (conditional)",
    "Working-paper text (published version paywalled). Allowed only after adding to the reference list and only as analogue/contrast (principal does not know which projects are available = asymmetric information; v2.2 is complete-information).",
    "Crossref: 10.3982/ecta7965, Econometrica 78(1) 213-244, 2010 (Crossref author field empty; authors from WP title page)", "NO",
    "02 §7 ('delegated project choice (Armstrong & Vickers)'); 03 §10; 11 A4; 10 rows 2.8, R-4")
row("Harris_Raviv_1996", "Capital-budget ceilings / spending limits as a known analogue of envelope-as-ceiling",
    "journal article (J. Finance 51(4):1139-1174)", "NO (closed)", AB,
    "Abstract (OpenAlex index): 'Observed budgeting processes are explained as a response to decentralized information and incentive problems. It is shown that these imperfections can result in underinvestment ... and overinvestment ...' - no explicit 'ceiling/spending limit' wording in the abstract",
    "NO", "Abstract does not establish the ceiling claim.", "Crossref: 10.1111/j.1540-6261.1996.tb04065.x, 51(4) 1139-1174, 1996-09 (also JSTOR 10.2307/2329390)", "NO",
    "02 §7 ('capital-budget ceilings / spending limits (Harris & Raviv-type capital-budgeting models)'); 10 rows 2.8, R-4")
row("Harris_Raviv_1998", "Capital budgeting and delegation (spending limits)", "journal article", "NO", UN,
    "Crossref metadata only", "NO", "Identity only.", "Crossref: 10.1016/s0304-405x(98)00038-5, J. Financial Economics 50(3) 259-289, 1998-12", "NO", "02 §7; 10 R-4")
row("Topkis_1978", "Monotone comparative statics (isotone optimal solutions)", "journal article (Oper. Res. 26(2):305-321)", "NO", AB,
    "Abstract (OpenAlex index): 'general conditions under which a collection of optimization problems ... has optimal solutions that are an isotone function of the parameter'", "NO",
    "Not needed for any proof (04 §8: D1 proved directly).", "Crossref: 10.1287/opre.26.2.305", "NO", "04 §8 ('[NOT IN REFERENCE LIST - TO VERIFY]'); 10 rows 2.9, §12")
row("Topkis_1998_book", "Supermodularity and complementarity (monotone comparative statics)", "monograph (Princeton UP)", "NO", AB,
    "Publisher abstract (OpenAlex): 'monotone comparative statics ... manifestations of complementarity ... super-modular function on a lattice'", "NO",
    "Crossref issued date 2011-12-31 (digital edition); original 1998 year NOT confirmed by Crossref - do not assert.", "Crossref: 10.1515/9781400822539", "NO", "04 §8; 10 row 2.9")
row("Milgrom_Shannon_1994", "Monotone comparative statics", "journal article (Econometrica 62(1), first page 157)", "NO", AB,
    "Abstract (OpenAlex index): 'a necessary and sufficient condition for the solution set of an optimization problem to be monotonic in the parameters'", "NO",
    "Crossref gives first page 157 only; last page not shown by Crossref - do not assert.", "Crossref: 10.2307/2951479, Econometrica 62(1) 157, 1994-01", "NO", "04 §8; 10 row 2.9")
row("Howard_1966", "Expected value of information (contrast: v2.2 VOI is worst-case MMR reduction); joint value of resolving several uncertainties is non-additive (analogue of E.9 complementarity)",
    "journal article (IEEE TSSC 2(1):22-26)", "NO (closed)", AB,
    "Abstract (OpenAlex index): '... numerical values can be assigned to the elimination or reduction of any uncertainty. Furthermore, it is seen that the joint elimination of the uncertainty about a number of even independent factors in a problem can have a value that differs from the sum of the values of eliminating the uncertainty in each factor separately.'",
    "NO", "Abstract-only; would be an expected-value (prior-based) contrast, not support for E.x.", "Crossref: 10.1109/tssc.1966.300074, 2(1) 22-26", "NO", "05 §7 ('Howard (1966) ... TYPE B, to verify'); 10 rows 2.9, §12")
row("Raiffa_Schlaifer_1961", "Classical (expected) value of information (contrast)", "book", "NO", SE,
    "No book record in Crossref; existence shown only by 1961 book reviews indexed in Crossref (Technometrics 3(3) 439, 10.2307/1266736; Biometrika 48(3/4) 478, 10.2307/2332787)", "NO",
    "Publisher/edition details not asserted.", "NOT IN CROSSREF as a book; reviews only", "NO", "05 §7; 10 rows 2.9, §12")
row("Kouvelis_Yu_1997", "Minimax-regret robust discrete optimization (interval data)", "monograph (Springer/Kluwer, NOIA)", "NO", SE,
    "Crossref book record; content seen only through citing works: Ben-Tal et al. (2009) Preface ('revived circa 1997 ... in the frameworks of both Integer Programming (Kouvelis and Yu [70])'); Lempert et al. (2003) Ch. 3 eq. (3.2) relative regret attributed to Kouvelis and Yu", "NO",
    "Lempert/Ben-Tal list it as Kluwer 1997; Crossref lists Springer US (Nonconvex Optimization and Its Applications).", "Crossref: 10.1007/978-1-4757-2620-6", "NO", "05 §7; 06 §6; 10 rows 2.9, §12")
row("Averbakh_2001", "Interval minmax-regret combinatorial optimization", "journal article (Math. Program. 90(2):263-272)", "NO", UN,
    "Crossref metadata only", "NO", "Identity only.", "Crossref: 10.1007/pl00011424, 2001-04", "NO", "05 §7; 06 §6; 10 row 2.9")
row("Averbakh_Lebedev_2004", "Interval-data minmax-regret network optimization", "journal article (DAM 138(3):289-301)", "NO", UN,
    "Crossref metadata only", "NO", "Crossref issued 2004-04; OpenAlex year 2003 (online). Identity only.", "Crossref: 10.1016/s0166-218x(03)00462-1", "NO", "05 §7; 06 §6")
row("Manski_2003", "Partial identification: report identified sets rather than impute (anchor for Definition G)", "monograph (Springer Series in Statistics)", "NO", UN,
    "Crossref metadata only (author field empty in Crossref)", "NO", "Identity only; Definition G stays TYPE C, Methods/Appendix.", "Crossref: 10.1007/b97478 'Partial Identification of Probability Distributions' (2003)", "NO", "07 §8 ('Partial-identification literature (e.g. Manski): [NOT IN 59a REFERENCE LIST - TO VERIFY]'); 11 A8; 10 row 2.9")
row("Chernoff_1954", "Menu-dependence / IIA failure of minimax regret (known since Chernoff)", "journal article (Econometrica 22(4):422-)", "NO (closed)", SE,
    "Secondary only: Stoye (2011 WP) p. 7 fn 6 (IIA property 'goes back at least to Chernoff [11]') and p. 11 ('anticipated ... (Chernoff [11, theorem 2])'); Stoye ref [11] = 'Rational selection of decision functions, Econometrica 22 (1954) 422-443'", "NO",
    "The pack's specific attribution (Chernoff showed minimax regret violates IIA) is not located in any text read.", "Crossref: 10.2307/1907435, 22(4) first page 422, 1954-10", "NO", "05 §0, §7; 11 A7; 14 A7; 10 row 2.9")
row("Stoye_2011", "Minimax regret is menu-dependent / violates independence of irrelevant alternatives (known analogue of E.1/E.2-adaptive, W6b)",
    "journal article (JET 146(6):2226-2251)", "YES (author working version dated July 14, 2011, stoye.economics.cornell.edu)", FT,
    "WP p. 2: 'this ordering is menu dependent, i.e. the ranking of acts can depend on the feasible set within which they are compared'; p. 7: 'a crucial, and controversial, feature of minimax regret, namely that it violates independence of irrelevant alternatives (IIA)'",
    "YES (conditional)",
    "Working version (final JET text not read). Allowed only after adding to the reference list and only to position E.1/E.2-adaptive as an in-model instance of a known property (TYPE C stays TYPE C).",
    "Crossref: 10.1016/j.jet.2011.10.004, JET 146(6) 2226-2251, 2011-11", "NO", "05 §0, §7 ('Stoye (minimax-regret axiomatization) ... verify'); 11 A7; 10 row 2.9")
row("Loridan_Morgan_1996", "Optimistic vs pessimistic (weak vs strong Stackelberg) bilevel", "journal article (J. Global Optim. 8(3):263-287)", "NO", UN,
    "Crossref metadata only", "NO", "Identity only; Kleinert (2021) already covers opt/pess at full-text level.", "Crossref: 10.1007/bf00121269, 1996-04", "NO", "06 §6; 11 §5 table; 10 row 2.9")
row("LIT_Braess_type_more_options_hurt", "'More options can hurt the principal' / Braess-type paradoxes in Stackelberg games (analogue of Lemma I, D4-D6, W5_WIDE)", "literature stream (no specific work named)", "NO", UN,
    "No specific work identified in the pack; nothing verified", "NO", "Do not mention in main text.", "N/A", "NO", "04 §8; 10 row 2.9")
row("LIT_VOI_complementarity", "Complementarity / non-submodularity of information value (analogue of E.9, W6e)", "literature stream", "NO", UN,
    "No specific work named; closest located: Howard (1966) abstract (non-additive joint value) - ABSTRACT only", "NO", "Do not mention in main text.", "N/A", "NO", "05 §0, §7; 11 A7; 12 §4; 10 row 2.9")
row("LIT_capital_budget_ceiling", "Envelopes as ceilings known qualitatively from capital budgeting with spending limits (analogue of DL-6)", "literature stream", "NO", UN,
    "Only Harris & Raviv 1996 abstract read (no ceiling wording); 1998 identity only", "NO", "Do not mention in main text.", "N/A", "NO", "02 §7; 12 §4; 10 rows 2.8, R-4")

assert len({r['citation_key'] for r in R}) == len(R)
with open(OUT / "07_V1_8_6_REFERENCE_VERIFICATION.csv", "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.DictWriter(fh, fieldnames=COLS, quoting=csv.QUOTE_ALL)
    w.writeheader()
    w.writerows(R)
c = Counter(r["verification_status"] for r in R)
yes = [r["citation_key"] for r in R if r["allowed_in_main_text"].startswith("YES")]
bad = [r["citation_key"] for r in R if r["allowed_in_main_text"].startswith("YES") and r["verification_status"] != FT]
print(len(R), dict(c))
print("YES", len(yes), yes)
print("YES_but_not_FT", bad)
print("in59a", Counter(r["in_59a_reference_list"] for r in R))
print("YES in59a", sum(1 for r in R if r["allowed_in_main_text"]=="YES" and r["in_59a_reference_list"]=="YES"))
