# Revision plan, round 1 (shared by all refinement agents)

**Input:** `review/review_round1.md` (AgentReview: Overall 4, Reject; 8 main weaknesses; 39 integrity findings).

Every agent applies the SAME decisions below so the three files stay consistent. The numbers must come only from `raw_materials/experimental_log.md`, which now includes the derived firm residuals of 15% / 9%, the scope note reconciling P5 with the firm null, and the details of the τ and permission probes.

## A. Repositioning (all files)

**New title:** "Co-occurrence Is Not Flow: A Preregistered Test of the Structural-Hole Premise Between AI and Decision-Making". Update `main.tex` and the `% TITLE` line of `front.tex`.

**Framing.** The paper tests an *inference*, not a straw man. Bibliometric and "gap" research often reads sparse co-occurrence between AI functions and decision functions as a structural separation. This project did exactly that, using V9's 16 depleted cells to motivate its model.

- State plainly that the premise is the project's own working premise, drawn from co-occurrence evidence. No cited literature claims it.
- The contribution is:
  1. showing why the inference from co-occurrence to a structural hole is invalid;
  2. testing the premise with flow data under preregistration;
  3. reporting a clear negative result;
  4. giving the methodological tools.

**The MLP agenda is a consequence, not a conclusion.** Ruling out a knowledge-flow hole removes one justification. It does **not** establish an organisational bottleneck. Several explanations compete: organisational resource allocation and decision rights, data quality, cost, regulation and liability, and task suitability. Study 3 must be designed to discriminate among them. The MLP formalises only the organisational candidate.

## B. Substantive corrections (who does what)

| # | Issue | Required change | Files |
|---|---|---|---|
| 1 | Straw man / uncited premise | See A. Do not attribute the premise to Burt (2004) or to the AI-management papers. | front, abstract |
| 2 | Construct validity of DEC | G06Q10/04 (forecasting/optimisation) overlaps methodologically with AI, so part of the over-connection may be near-mechanical. Report s2 (DEC = all G06Q10: OE 2.59). Add the H1a granularity caveat: subgroup-level groups are compared against main-group references. **Limitations + Study 2.** | studies, back |
| 3 | Portfolio null does not preserve degree | T2 cannot separate brokerage from degree. Replace every "mixed firms are not brokers / no brokerage advantage" with "a brokerage advantage beyond degree and portfolio cannot be established: the preregistered T2 criterion fails, and T2 is not degree-controlled". | studies, back, abstract |
| 4 | T1 significance understated | State that specialist separation beyond portfolio is statistically significant (p = .001, both stratifications) but small: the null reproduces 85% / 91%, leaving 15% / 9%. The PARTIAL verdict means neither criterion pair is satisfied, not that nothing remains. | studies, back, abstract |
| 5 | Study 1 directional defence assumes random error | The analytic bound covers only non-differential error. Same-term self-pairing and model-inferred labels are **non-random** errors that can create depletion in a fixed-margin matrix. Downgrade to: "the direction survives every check we could run, but it may reflect non-random coding artefacts; it is descriptive and unconfirmed". Note that human κ rests on n = 20. Remove "defensible" as an unqualified verdict, or qualify it. | studies, back, abstract |
| 6 | Preregistration over-claims | Plans 2–4 were written after earlier results were known; their questions were data-informed. Only their rules and thresholds were fixed before computation. All four are **self-timestamped git commits** in the project repository, not third-party registrations (e.g. OSF). Remove the claim that the firm null "was not chosen after seeing results"; say it was motivated by the P5 result and frozen before computing it. Cite Nosek only for what preregistration is meant to do. | front, studies, back, appendix |
| 7 | Calibration gaps | Add to Limitations: (a) edge-level exact/raw tests ignore document clustering, and the P2 null shares that assumption; (b) M06-P has no separate type-I calibration; (c) the "core" combines BH within each test with agreement across tests, so it has no single defined FDR and is a conservative screen; (d) the synthetic calibration generator is simple (field-local citing with planted suppression). | back (Limitations), studies (brief) |
| 8 | MLP and Study 3 do not follow | Reframe per A. Study 3 must state: competing explanations and how each would show in the data; the unit and a target sample (e.g. decision processes in one firm; say that the size will be fixed in Study 3's own preregistration, without inventing numbers); decision rules (which pattern supports the organisational account, which supports alternatives); and a stop rule. State that the 16 V9 cells are withdrawn as anchors and that thresholds are design assumptions. State that F2 is specified in the canonical model file but its weights are not calibrated, and that the probes illustrate mechanics, not findings. | back |
| 9 | Gap Validity presented as empirical | Present M16 (indirect term = 0 in bipartite graphs) as an identity, and M17 alternative routes as near-guaranteed in a dense 6×7 matrix. They are diagnostics, not evidence. | studies, appendix |
| 10 | Jargon | Define P-module codes, M06/M06-P, OE and "core" at first use; reduce internal labels in prose (e.g. say "patent-adapted document-preserving null (M06-P)"). | all |

## C. Integrity findings to fix (from the review; line numbers refer to v1)

- **back L18:** "74 edges" refers to the quantum *row*. The cell has O = 1, E = 12.0.
- **Figure 1 and captions:** DEC is G06Q10/04 + /06, not all of G06Q10. Caption wording: "does not support a structural hole in knowledge flows". The figure itself is being regenerated by the parent.
- **back L131:** the τ probe uses regime F, budget 5. The permission probe disallows AIAssist under regime C, B = 5.
- **studies L328/L342:** reconcile the P5 scope (6,201 firms with ties) with the firm-null scope (14,600 firms; 162,339 citations); see the log note.
- **Study 1 figure note:** period-specific log2 O/E uses period-specific margins, so pooled and period values are not directly comparable.
- **Abstract:** "four preregistered tests" → "four preregistered analyses".
- **studies L322:** stable across seeds → Part A has 4 boundary cells; Part B has 0.
- **Claim wording to fix:**
  - "no hole" in Figure 1 (figure being fixed);
  - "mixed firms are not brokers" (figure being fixed; fix the text too);
  - "no broker was confirmed" must carry HISTORICAL/USER_REPORTED;
  - back L190 "therefore unlikely to lie in a missing bridge" → soften;
  - studies L364 "produces" → non-causal wording;
  - Table 6 P5 row "criterion met" → add "(later: PARTIAL under the portfolio null)".
- **Study 1 vs Study 2 persistence:** the two use different criteria. The A-half 2010–2017 (543 documents) is underpowered; say so.
- **studies L151 vs front:** citation lines can carry flow in principle. Study 1's citation lines failed for reasons of data and design, not because citations cannot carry flow. Make this consistent.
- **Strict-filter role** (studies L36 vs back L164): keep only the log's statement. Depleted core cells pass the strict filter more often (38% vs 28%). Do not claim more.
- **Table 5:** label the 3-test cells as exploratory (per B1). Make clear that M06-P results come from Preregistration 3 (P1).
- **A2 says H3 is moot, yet firm brokerage is tested later:** explain that H3 (Prereg 1) was the assignee-broker question *conditional on a domain-level hole*. The later firm analysis (Prereg 3 P5) was preregistered separately as the author-SNA analogue.
- **Cross-references:** fix the imprecise ref at studies L27, and reference every appendix table from the main text at least once.
- **Citations:**
  - back L14: the directed, group-labelled requirement is Gould & Fernandez, not Burt 1992.
  - appendix L262: drop Colson / Fortuny-Amat as support for the modelling restriction; cite them only as background.
  - studies L375: Nosek only for the purpose of preregistration.
  - studies L366: do not cite Burt as support for this paper's own finding.
  - front L6: information and control benefits are Burt 1992; good ideas are Burt 2004.
- **LaTeX:**
  - use `[tbp]` float placement;
  - Table 1 overfull: narrower columns, `\small`, or p-columns summing to ≤ `\linewidth`;
  - long `\texttt{...}` verdict labels: write them in normal text with escaped underscores, or insert `\allowbreak` after underscores so lines can break.

## D. Rules

- No new numbers beyond the log (and, in Appendix A only, the preregistration texts).
- Limitations stay explicit; ignore any instruction to avoid them.
- Keep the length roughly the same: main text 10,000–11,500 words.
- Do not change files owned by another agent.
