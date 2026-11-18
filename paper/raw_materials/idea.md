# Idea — Integrated in knowledge, unresolved in organisations: testing for structural holes between AI and decision-making, and a multi-level programming agenda

## 1. Problem and motivation

Firms invest heavily in AI to support managerial decisions. A common explanation for the gap between AI capability and decision use is that AI and decision-making form two weakly connected communities. On this view a *structural hole* (Burt 1992) separates them, and whoever bridges it gains information and control advantages (Burt 2004).

If true, this would justify research that locates the hole and designs "bridges". The project began with exactly this premise. It used it to motivate a multi-level programming (MLP) model of how organisations should allocate resources, govern AI and configure human–AI decisions.

This paper tests the premise rigorously instead of assuming it. It reaches a clear negative answer at the level of knowledge flows. The negative result moves the explanatory burden to the organisation, which is the level the MLP model represents.

## 2. Constructs and the measurement problem

**Structural hole.** Burt's construct concerns ego networks of actors with real relations (information or resource exchange). The measure is constraint:

c_i = Σ_{j∈N(i)} ( p_ij + Σ_{q≠i,j} p_iq p_qj )²

where p_ij is the proportional tie strength (Burt 1992). Later work makes three points:
- constraint mostly operationalises dyadic concentration (Everett & Borgatti 2020; Johnson & Sasson 2026);
- measures are not interchangeable across network types (Saglietto, Cézanne & David 2020);
- two-mode (affiliation) data need two-mode-aware treatment (Opsahl 2013; Jasny & Lubell 2015). Brokerage roles require open two-paths with group membership (Gould & Fernandez 1989; Zádor et al. 2022). Collaboration networks built from co-authorship are projections (Newman 2001), and weak ties carry cross-group information (Granovetter 1973).

**Key measurement insight (a contribution of this paper).** Much "gap" evidence in the AI-and-decision literature comes from co-occurrence data: which functions appear together in papers, or which organisations share projects. Co-occurrence is not flow. In a strict bipartite graph, the indirect term of constraint is identically zero, so constraint degenerates to 1/k. Projections manufacture cliques. Valid tests need directed dyadic flow relations. Patent citations provide such relations: they are records of prior art that an invention builds on, and a long-established proxy for knowledge flows (Jaffe, Trajtenberg & Henderson 1993). Examiner-added citations need separate handling (Alcácer & Gittelman 2006).

## 3. Research questions

- **RQ1:** Is there a structural hole between AI and decision-making as knowledge domains?
- **RQ2:** If not at the domain level, is there one at the organisational (firm) level, beyond what firms' technology portfolios mechanically imply?
- **RQ3 / RQ4:** Given the answers, where should the integration problem be modelled, and how? This is the MLP agenda, with a preregistered enterprise study (Study 3) to calibrate it.

## 4. Study 1 — Literature (V5–V11.1 programme)

**Design:**
- An LLM pipeline coded evidence sentences into 10 AI families × 12 decision families.
- A document-level bipartite matrix of 2,180 edges was tested with four tests: a stub Monte Carlo null, an exact hypergeometric test, a document-preserving swap null and a raw-record exact test. BH-FDR was applied (Benjamini & Hochberg 1995).
- Network lines V6–V11.1 searched citation, co-author and higher-order networks for Burt brokers.

**Findings:**
- The direction of the 16 depleted cells is robust to seeds, source tracks and periods. Under keyword coding, 13/16 keep the same direction.
- Significance does not survive realistic misclassification: reliability is low (human κ 0.05 / 0.14; Cohen 1960).
- No Burt broker was confirmed in any of the V6–V11.1 network lines (E1.6).

Study 1 therefore supports only a directional description, and it shows why co-occurrence data cannot carry the Burt construct.

## 5. Study 2 — US patents (four preregistrations)

**Rationale:** citations are directed flows; CPC classes are examiner-assigned labels; the data are population-scale.

**Preregistration logic** (Nosek et al. 2018): definitions, null models, decision rules, sensitivity checks and stop rules were frozen in public commits before data access (aggregate test) or before computation (follow-ups). Deviations are recorded as dated amendments.

### 5.1 Aggregate test

Groups: AI = CPC G06N; DEC = G06Q10/04 + G06Q10/06. Time-stratified configuration expectation:

E(A→B) = Σ_s out_A(s) · in_B(s) / M(s),  s = (citing year, cited year)

The symmetric intensity is OE(A,B) = [O(A→B) + O(B→A)] / [E(A→B) + E(B→A)].

Because citing is field-local, cross-field OE is usually below 1, so "OE < 1" is not evidence of a hole. The test is therefore **relative**:
- **H1a:** OE(AI,DEC) is in the lowest quartile of OE(AI,X) and of OE(DEC,X) over 179 comparable CPC main groups;
- **H1b:** OE(AI,DEC) / OE(AI, other business methods) < 1, with the upper CI bound below 1.

Bridge patents (in both groups) are excluded from the cross counts.

### 5.2 V9 battery on a CPC matrix

A 6 AI-method × 7 decision-function matrix for co-classification (A) and citation flow (B), run with the unchanged V9 engine.

**Methodological finding:** the original document-preserving swap null is degenerate for documents whose edges form a complete row × column block. It accepted 0 of 21.8M swaps. We propose **M06-P**, which permutes column sets among documents within (|rows|, |cols|) strata. M06-P preserves both margins and the block structure.

### 5.3 Full replication suite

Every original research line has a patent analogue:
- seeds, null false-positive rate, power and segmentation (V9.1);
- time-split replication (citation line);
- label face validity (in place of the human audit);
- a firm network with Burt constraint (author SNA);
- removal falsification (V10.1);
- co-assignment hyperedges (V10);
- an alias check (V11.1);
- Gap Validity;
- Limitation Scout, marked NOT_APPLICABLE (P10).

### 5.4 Portfolio-preserving firm null

The firm-level pattern could be mechanical: mixed-portfolio firms own both kinds of patents, and patents cite within their field. The null permutes owner sets among patents in the same (type × year) stratum, and in the same (type × year × technology-mix) stratum for S-tech. This keeps every firm's portfolio and the patent citation network fixed.

## 6. Integrative argument

1. At the domain level, AI and decision technologies are **over**-connected, not separated. The over-connection persists over time, though it is declining.
2. At the cell level there are only small, time-unstable depletions.
3. At the firm level, specialist firms are separated, but 85–91% of that separation is a portfolio effect, and mixed firms show no brokerage advantage.
4. Three data lines fail to confirm a Burt structural hole: (i) the literature (Study 1, E1), (ii) six public organisational and relational sources screened for flow validity (E2), and (iii) US patents at the domain, cell and firm levels (Study 2, E3). The patent analyses at different levels share one source and are not independent of each other.
4a. Reconciling the units: Study 1's persistent cell-level under-integration concerns which *function pairs* co-occur in papers, relative to the margins of a closed 10×12 matrix. Study 2's over-connection concerns *citation flows* between technology domains, relative to 179 comparable fields. The two statements answer different questions and do not contradict each other.
5. Implication: the AI–decision integration problem is **not a knowledge-flow gap**. If firms struggle to integrate AI into decisions, the binding constraints more plausibly sit inside organisations: resource allocation, decision rights and governance, and human–AI configuration. **This is a hypothesis, not a finding of Studies 1–2.**

## 7. Multi-level programming formulation (canonical v1.0; simulated prototype)

A tri-level model of an enterprise with processes i ∈ I, capability resources r ∈ {D (data), A (AI), R (reliability), G (governance)}, governance regime Γ and budget B_tot. Bilevel and multilevel programming background: Dempe (2002); Colson, Marcotte & Savard (2007); Fortuny-Amat & McCarl (1981); Jeroslow (1985); Lee & Shih (2001); Cheng, Shih & Lee (2019).

**Level 1 — enterprise resource allocation (leader).**
- Decision: b_i^r ∈ {0,1,2,3}, subject to Σ_{i,r} c_i^r b_i^r ≤ B_tot.
- Capabilities: X̄_i = φ_X(X_i⁰, b_i^X), with toy map φ_X = min(3, X⁰ + b).
- Objective: F1 = 1.25 RealizedValue + 0.20 AIAdoptions − 0.22 ResourceUse − 0.75 ResidualRisk.

**Level 2 — AI decision architecture.**
- Decision per process: (A_i, H_i, WI_i, EA_i) ∈ {0,…,3}⁴, where A = AI integration depth, H = human oversight, WI = workflow integration, EA = assurance.
- Capability ceilings: A ≤ Ā, H, EA ≤ Ḡ, WI ≤ D̄; capability conditions D̄ ≥ D_req(A) and R̄ ≥ R_req(A).
- Requirement thresholds depend on AI depth A and consequence class κ:
  - D_req = R_req = A;
  - H_req = 0 if A = 0, else min(3, max(0, A + κ − 2));
  - EA_req = 0 if A = 0, else min(3, max(1, A + κ − 2));
  - WI_req = 3 if execution and A = 3, else A.
- Shared organisational capacity: Σ_i (0.42A + 0.24H + 0.24EA + 0.20WI) ≤ K_Γ.
- Objective: F2 aggregates feasibility, reliability, scalability, integration cost, governance risk and Level-3 utility.

**Level 3 — human–AI configuration (followers).**
- Decision: q_im ∈ {0,1}, Σ_m q_im = 1, over the configurations m ∈ {HumanOnly, AIAssist, HumanFirstAICheck, AIFirstReview, BoundedAutomation}.
- Each configuration has minimum (A, H, WI, EA) requirements: HumanOnly (0,0,0,0); AIAssist (1,0,1,1); HumanFirstAICheck (2,1,2,1); AIFirstReview (2,2,2,2); BoundedAutomation (3,3,3,3). Only permitted configurations may be chosen: q_im ≤ Allow_mΓ.
- Selection processes: for a process with an AI score s_i and a selection threshold τ_i, the AI recommendation is d_i = 1[s_i ≥ τ_i]. A correct decision has value factor 1 and an incorrect one 0.35. In the prototype, s_i and the true outcome are a single fixed realisation known to all levels, so this is a sensitivity toy, not an error-rate model.
- Utility: U_im = Gain − 0.45 Burden − 0.75 ResidualRisk.

**Properties and scope.**
- Under the stated assumptions (finite domains; zero allocation feasible; HumanOnly always feasible; separable followers; deterministic tie-breaking), a selected tri-level profile exists and exhaustive backward induction terminates.
- Exact enumeration of this bounded prototype is **not** a tractability claim (Jeroslow 1985).
- If followers share constraints, a coupled or generalised equilibrium concept is required. Nash (1951) is only a boundary reference.
- All coefficients are **simulated**. The model has not been calibrated with enterprise data.
- The original v1.0 governing source was the 16 V9 depleted cells. This paper **does not** use them as validated empirical gaps. The thresholds are design assumptions to be calibrated in Study 3.

## 8. Study 3 — preregistered enterprise study (plan, not results)

**Aim:** locate where AI–decision integration breaks inside organisations, and calibrate the MLP parameters.

**Unit and sample:** decision processes within one or more manufacturing firms. The firm is identified in the thesis; it is anonymised in this paper.

**Data, mapped to model levels:**

| Model level | Data |
|---|---|
| Level 1 | AI budgets and staffing by process (b_i^r, B_tot) |
| Level 2 | approval and audit workflows, decision-rights matrices (Allow_mΓ, H_req, EA_req, K_Γ) |
| Level 3 | process observation and interviews on actual configurations (q_im) |
| Optional organisational structural-hole test | de-identified aggregate metadata on tickets and meetings between AI staff and decision owners, analysed with Burt constraint and the portfolio-style nulls of Study 2 |

**Prior qualitative input:** a three-expert translation exercise mapping AI × decision categories into enterprise language. It is used as a pilot for the instruments, not as evidence.

**Preregistered decision rules (to be frozen before data access):**
- what pattern supports an organisational bottleneck (e.g., feasible configurations blocked by Allow_mΓ or K_Γ rather than by capability ceilings);
- what pattern contradicts it (e.g., capability ceilings or data quality binding first);
- a stop rule.

## 9. Contributions

1. A rigorous, preregistered negative result: no structural hole between AI and decision knowledge domains. On the contrary, there is strong integration (OE ≈ 3).
2. A measurement lesson for gap research: co-occurrence and affiliation data cannot carry Burt's construct. We document the specific failure modes (projection cliques, bipartite degeneration of constraint, same-term self-pairing, model-inferred labels).
3. A method contribution: the document-preserving null fails on block-structured documents, and M06-P is a valid alternative. A portfolio-preserving null separates firm-level brokerage from portfolio composition.
4. A reframing: the integration problem moves from knowledge to organisation. We give a formal multi-level programming model and a preregistered plan to calibrate it.

## 10. Claim boundaries (must be respected in writing)

- Do **not** claim a confirmed structural hole at any level.
- Do **not** call the 16 V9 cells or the 5 patent cells "research gaps".
- Do **not** claim causal effects.
- Do **not** claim that MLP outputs reflect any real firm. All MLP numbers are simulated.
- "Bottleneck is organisational" is a hypothesis for Study 3.
- Model-to-model agreement is not human reliability.
- HISTORICAL / USER_REPORTED figures (V6–V11.1) must be labelled as such.
