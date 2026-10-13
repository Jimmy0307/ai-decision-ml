# AI × Decision × MLP v1.1 — Claude Review Packet: Gap → Mechanism → Measurement → MLP

> **SUPERSEDED / HISTORICAL v1.1 PROPOSAL — Measurement freeze FAIL.** Read 21–23 for the governing v1.2 candidate and 24 for the Claude re-review. The no-structural-change, three-independent-level, threshold-identification and static-M5 claims below are withdrawn where they conflict. v1.0 solver remains a simulated historical baseline.

Base mathematical freeze: `main@1f2e72f1894c8d4eb7929c39756d7b6af607545b`.

Purpose: provide an audit-ready consolidation of the research positioning, G01–G16 evidence, literature triangulation, construct definitions, measurement logic, and the precise boundary between source-supported claims and researcher-designed operationalization.

**Critical boundary:** this document does not modify the frozen v1.0 solver/equations. It proposes the empirical/theoretical calibration layer for review before any model update.

---

## 1. Research claim being made — and claims NOT being made

### 1.1 What the frozen corpus establishes

The canonical Priority_Gaps export identifies 16 **robust AI × Decision depletions**. A robust depletion is a document-level AI-family × Decision-family cell whose observed count is below the fixed-degree/null expectation with BH-adjusted significance and consistent depletion direction in all four audited V5 analyses.

These are literature-network structural properties. They are **not** automatically:

- field-wide research gaps;
- causal deficiencies;
- enterprise practical problems;
- optimization weights;
- evidence that JPC itself lacks a capability.

The correct chain is:

`Robust depletion → literature mechanism hypothesis → enterprise measurement → requirement/capability gap → MLP representation → robustness analysis`.

### 1.2 Core research positioning

The study is not primarily asking whether AI improves firm performance or whether firms adopt AI. It asks:

> **How should firms allocate AI-related capabilities and configure Human–AI decision architectures under resource, workflow, governance, assurance, and risk constraints?**

The optimization target is therefore an organizational decision architecture, not an AI classifier.

---

## 2. Canonical G01–G16 and proposed mechanism consolidation

| Gap | Canonical AI family × Decision family | Proposed mechanism role |
|---|---|---|
| G01 | HUMAN_AUGMENTATION × PREDICTION_DIAGNOSIS | M3 Human–AI Decision Configuration |
| G02 | PREDICTION_RISK_ESTIMATION × HUMAN_REVIEW_ACCOUNTABILITY | M1 Decision Authority, Governance & Accountability |
| G03 | COORDINATION_EXECUTION × RISK_ASSESSMENT | M2 AI-to-Workflow / Decision-Process Integration |
| G04 | GENERATION_SYNTHESIS × PREDICTION_DIAGNOSIS | T1 Temporal / Emerging Technology Monitor |
| G05 | EXPLANATION_ASSURANCE × ALLOCATION_PLANNING | M4 Evaluation & Assurance |
| G06 | EVALUATION_ASSESSMENT × PREDICTION_DIAGNOSIS | M4 Evaluation & Assurance |
| G07 | HUMAN_AUGMENTATION × EVALUATION_SELECTION | M3 Human–AI Decision Configuration |
| G08 | RECOMMENDATION_OPTIMIZATION × HUMAN_REVIEW_ACCOUNTABILITY | M1 Decision Authority, Governance & Accountability |
| G09 | PREDICTION_RISK_ESTIMATION × GOVERNANCE_OVERSIGHT | M1 Decision Authority, Governance & Accountability |
| G10 | PREDICTION_RISK_ESTIMATION × EVALUATION_SELECTION | M3 Human–AI Decision Configuration / score-to-choice boundary |
| G11 | EVALUATION_ASSESSMENT × ALLOCATION_PLANNING | M5 Adaptive Information, Learning & Resource Feedback |
| G12 | PREDICTION_RISK_ESTIMATION × INFORMATION_ACQUISITION | M5 Adaptive Information, Learning & Resource Feedback |
| G13 | EXPLANATION_ASSURANCE × PREDICTION_DIAGNOSIS | M4 Evaluation & Assurance |
| G14 | PREDICTION_RISK_ESTIMATION × GENERAL_DECISION_PROCESS | M2 AI-to-Workflow / Decision-Process Integration |
| G15 | EXPLANATION_ASSURANCE × EVALUATION_SELECTION | M3 primary / M4 secondary |
| G16 | COORDINATION_EXECUTION × HUMAN_REVIEW_ACCOUNTABILITY | M1 + M2 bridge; baseline bridge in v1.0 |

### 2.1 Why consolidate rather than create 16 variables

The 16 cells are evidence descriptors, not 16 independent latent constructs. Treating each as a variable would confound corpus structure with enterprise measurement. The proposed empirical model therefore consolidates them into five mechanisms plus one temporal monitor:

- **M1 — Decision Authority, Governance & Accountability**
- **M2 — AI-to-Workflow / Decision-Process Integration**
- **M3 — Human–AI Decision Configuration**
- **M4 — Evaluation & Assurance**
- **M5 — Adaptive Information, Learning & Resource Feedback**
- **T1 — Temporal / Emerging Technology Monitor**

**Audit status:** this clustering is a researcher synthesis. It is triangulated by literature below; no cited source independently proves that the 16 corpus depletions must cluster exactly this way.

---

## 3. Literature triangulation with exact source language

The quotations below are deliberately short. They are included so an auditor can check whether our interpretation is warranted.

### 3.1 Human–AI complementarity is contingent, not automatically beneficial

**Jarrahi (2018), Business Horizons, DOI 10.1016/j.bushor.2018.03.007, abstract**

Exact source language:

> “AI systems should be designed with the intention of augmenting, not replacing, human contributions.”

Supports: treating Human–AI architecture as a design problem rather than assuming full automation is optimal.

Does **not** establish: our five configurations, our 0–3 scale, or our utility coefficients.

**Raisch & Krakowski (2021), Academy of Management Review, DOI 10.5465/amr.2018.0072, abstract**

Exact source language:

> “automation implies that machines take over a human task, augmentation means that humans collaborate closely with machines to perform a task.”

Supports: separating automation depth from augmentation/human collaboration.

Does **not** establish: the numerical boundary between A=1/2/3.

**Vaccaro, Almaatouq & Malone (2024), Nature Human Behaviour, DOI 10.1038/s41562-024-02024-1, abstract**

Exact source language:

> “human–AI combinations performed significantly worse than the best of humans or AI alone.”

Supports: rejecting the assumption that more Human–AI combination is always better; motivates configuration-specific optimization and task/context moderation.

Does **not** establish: which configuration is optimal for JPC.

**Bansal et al. (2021), CHI, DOI 10.1145/3411764.3445717, abstract**

Exact source language:

> “explanations increased the chance that humans will accept the AI’s recommendation, regardless of its correctness.”

Supports: explanation/assurance cannot be equated mechanically with better team performance; trust and reliance need separate treatment.

Does **not** establish: that explanation is harmful in all settings.

### 3.2 Organizational decision structure and delegation matter

**Shrestha, Ben-Menahem & von Krogh (2019), California Management Review, DOI 10.1177/0008125619862257, p. 8 in accessible PDF**

Exact source language:

> “humans and AI-based algorithms sequentially make decisions such that the output of one decision maker provides the input to the other.”

Supports: modeling Human–AI decision arrangements as structural configurations and treating handoffs/workflow as part of the decision architecture.

The same paper distinguishes full delegation, two sequential hybrid structures, and aggregated Human–AI decision making; it also emphasizes search-space specificity, interpretability, alternative-set size, speed, and replicability when choosing structures.

Does **not** establish: our exact five-state L3 menu or its ordering.

### 3.3 Governance and accountability must be modeled separately from technical capability

**Elish (2019), Engaging Science, Technology, and Society, DOI 10.17351/ests2019.260, abstract**

Exact source language:

> “accurately locate who is responsible when agency is distributed in a system.”

Supports: explicitly representing decision authority, oversight, accountability, and the danger of assigning nominal human responsibility without effective control.

Does **not** establish: a specific H threshold or residual-risk formula.

**Khatri & Brown (2010), Communications of the ACM, DOI 10.1145/1629175.1629210, p. 149 / governance framework**

Exact source language:

> “who holds the decision rights and is held accountable for an organization’s decision-making about its data assets.”

Supports: separating governance/decision rights/accountability from operational management and technical infrastructure.

Does **not** establish: our G=0–3 anchor by itself.

**Berente et al. (2021), MIS Quarterly, DOI 10.25300/MISQ/2021/16274, abstract**

Exact source language:

> “making decisions about three related, interdependent facets of AI—autonomy, learning, and inscrutability”

Supports: treating AI management as more than technical deployment and recognizing autonomy/governance as an organizational design issue.

Does **not** establish: the autonomy_m values currently used in the toy model.

### 3.4 Evaluation, correction, assurance, and interpretability are distinct requirements

**Amershi et al. (2019), CHI, DOI 10.1145/3290605.3300233, Guideline 9**

Exact source language:

> “Make it easy to edit, refine, or recover when the AI system is wrong.”

Supports: operational controls for correction/recovery and the idea that Human–AI systems require mechanisms for error handling, not only predictive accuracy.

The guideline set also includes communicating capability limits, scoping services under uncertainty, explanations, feedback, cautious updating, and global controls.

Does **not** establish: a single universal EA score.

**Rudin (2019), Nature Machine Intelligence, DOI 10.1038/s42256-019-0048-x, abstract**

Exact source language:

> “The way forward is to design models that are inherently interpretable.”

Supports: stronger assurance/interpretability requirements in high-stakes decisions and the inadequacy of treating post-hoc explanation as automatically sufficient.

Does **not** establish: that every enterprise use case requires an interpretable model.

**Miller (2019), Artificial Intelligence, DOI 10.1016/j.artint.2018.07.007, abstract**

Exact source language:

> “looking at how humans explain to each other can serve as a useful starting point for explanation in artificial intelligence.”

Supports: explanation is a human-facing socio-technical construct, not merely a model-internal property.

Does **not** establish: our EA thresholds.

### 3.5 Readiness must be purpose- and context-specific

**Jöhnk, Weißert & Wyrtki (2021), Business & Information Systems Engineering, DOI 10.1007/s12599-020-00676-7, abstract**

Exact source language:

> “companies need to assess whether their assets, capabilities, and commitment are ready for the individual AI adoption purpose.”

Supports: measuring readiness at the use-case/adoption-purpose level rather than assigning one undifferentiated firm-wide maturity score.

The paper further argues that AI readiness is context- and purpose-specific and should be continuously assessed.

Does **not** validate our exact D/R/A/G decomposition.

**Vial (2019), Journal of Strategic Information Systems, DOI 10.1016/j.jsis.2019.01.003, abstract**

Exact source language:

> “digital technologies create disruptions triggering strategic responses from organizations”

Supports: separating external digital/technology context from internal organizational response/capability.

Does **not** establish our five-element industry vector `Z_t`.

### 3.6 Learning/feedback is dynamic and should not be overclaimed in the static baseline

**Argote & Miron-Spektor (2011), Organization Science, DOI 10.1287/orsc.1100.0621, abstract**

Exact source language:

> “organizational experience interacts with the context to create knowledge.”

Supports: treating learning/resource feedback as a dynamic mechanism rather than a one-time static score.

Does **not** establish: a specific t→t+1 transition equation for this study.

### 3.7 Mathematical hierarchy is compatible with multilevel programming, but AI literature does not prove our exact MLP

**Colson, Marcotte & Savard (2007), Annals of Operations Research, DOI 10.1007/s10479-007-0176-2, abstract**

Exact source language:

> “bilevel optimization, a branch of mathematical programming of both practical and theoretical interest.”

Supports: hierarchical optimization as a recognized mathematical-programming form.

**Fortuny-Amat & McCarl (1981), Journal of the Operational Research Society, DOI 10.1057/jors.1981.156, abstract**

Exact source language:

> “hierarchial problems that show a two-stage decision making process”

Supports: the general idea of hierarchical/multilevel decision making.

Does **not** prove: our tri-level formulation, our discrete finite solver, or empirical validity. Those are properties of the proposed model and must be independently demonstrated.

---

## 4. Proposed construct system

The 16 depletions are not converted into 16 enterprise variables. The proposed empirical core uses seven constructs:

### 4.1 Capability / prerequisite constructs

- `D` — Digital / Process Infrastructure Readiness
- `R` — Data Readiness
- `G` — Governance Capability

These describe what the organization/use case is capable of supporting.

### 4.2 AI decision-architecture constructs

- `A` — AI Decision Integration Depth
- `H` — Human Oversight
- `WI` — Workflow Integration
- `EA` — Evaluation & Assurance

These describe how the Human–AI decision architecture is configured.

### 4.3 Important measurement claim

These seven constructs are **not claimed to be an existing validated seven-factor scale**. They are a theory-informed operational construct system synthesized from the depletion evidence and literature. Therefore content validity, discriminant clarity, and inter-rater reliability must be empirically checked before publication.

---

## 5. Operational definitions and 0–3 anchors

The state scale is ordinal. Level differences are not assumed equal.

| Construct | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| D Digital/Process Readiness | manual/fragmented | digital but siloed | integrated workflow + stable structured exchange | interoperable end-to-end workflow with reliable automation hooks |
| R Data Readiness | unavailable/unreliable | partial/inconsistent | sufficient structured data + owner/basic quality | validated, governed, timely, traceable, sustainable AI-ready data |
| A AI Decision Integration Depth | no AI | information/assist | recommendation/check embedded in decision flow | bounded execution/automation |
| G Governance Capability | no formal governance | basic rule/responsibility | formal policy/ownership/monitoring | audit/escalation/control/lifecycle governance |
| H Human Oversight | no systematic oversight | optional/light review | mandatory review/override/accountable owner | continuous oversight/escalation/traceability |
| WI Workflow Integration | outside workflow | manual transfer | integrated trigger/handoff/exception routing | bounded end-to-end action with fallback/escalation |
| EA Evaluation & Assurance | none | ad hoc testing | predefined metrics/validation/monitoring | continuous assurance/audit/drift/rollback/traceability |

### 5.1 Why G, H and EA must remain separate

- `G`: organizational decision rights, policy, ownership, accountability framework.
- `H`: human involvement in a specific decision process/instance.
- `EA`: evidence and controls used to validate/monitor the AI system and recover from failures.

The literature supports these as distinct functions, but the exact three-way operational separation is our synthesis and must be checked for discriminant validity.

### 5.2 Why WI is separate from D

- `D` = infrastructure/process capability available.
- `WI` = degree to which AI output/action is actually embedded in the use-case workflow.

A digitally mature process may still keep AI outside the workflow; conversely, a narrow workflow may have a specific integration even when broader enterprise digital maturity is modest.

---

## 6. Measurement architecture

### 6.1 Never substitute observed state for optimizer decision

Observed/current state:

`D_obs, R_obs, A_obs, G_obs, H_obs, WI_obs, EA_obs, q_obs`

Optimized decision state:

`A, H, WI, EA, q_im` plus L1 resource decisions `b_i^r`.

Observed values calibrate or validate the model; they are not entered as the solver’s chosen final decision values.

### 6.2 Baseline/current-state measurement

Use anchored coding by at least two knowledgeable raters where possible:

- D/R/A: IT/MIS + process owner.
- G: IT/MIS + QA/governance/plant manager.
- H/WI/EA observed: process owner + frontline user + relevant technical/quality role.

Recommended reliability checks: weighted Cohen’s kappa for two raters, or Krippendorff’s alpha / ICC where design permits. Disagreements are adjudicated and preserved in an audit trail.

### 6.3 Requirement thresholds are the key empirical bridge

The most important empirical objects are not generic attitudes but minimum requirements:

`D_req(A)`

`R_req(A)`

`H_req(A, kappa, u)`

`EA_req(A, kappa, t)`

`WI_req(A, kappa, exec)`

Recommended method: **scenario/vignette-based threshold elicitation**, not abstract Likert agreement.

Example:

> For a high-consequence decision in which AI makes a recommendation but a human retains final authority, what is the minimum Human Oversight level required: H0/H1/H2/H3?

Then vary AI depth, consequence class, task type, and execution authority in a controlled design.

### 6.4 Enterprise requirement gaps

Only after both observed and required values exist do we define enterprise gaps:

`Gap_D_i = max(0, D_req_i - D_obs_i)`

`Gap_R_i = max(0, R_req_i - R_obs_i)`

`Gap_H_i = max(0, H_req_i - H_obs_i)`

`Gap_WI_i = max(0, WI_req_i - WI_obs_i)`

`Gap_EA_i = max(0, EA_req_i - EA_obs_i)`

**Audit status:** these formulas are researcher-defined operationalizations. They are not direct formulas taken from the cited literature. Their validity depends on the validity of the anchors and threshold elicitation.

### 6.5 Ordinal scale and cardinalization

The 0–3 levels are ordinal. Do not automatically treat 0→1, 1→2, and 2→3 as equal effect increments.

If a continuous objective needs cardinal effects, define a monotone map:

`z_X(0) < z_X(1) < z_X(2) < z_X(3)`

and estimate/bound it separately. Until identified, use interval/fuzzy/scenario mappings and sensitivity analysis.

The same rule applies to `kappa ∈ {Low, Medium, High}`: risk classes are ordinal; High is not assumed to be three times Low.

---

## 7. Mechanism → measurable construct → MLP mapping

| Mechanism | Main empirical measurements | MLP representation |
|---|---|---|
| M1 Authority/Governance/Accountability | G_obs, H_obs, H_req, kappa, Allow_mGamma | governance ceiling, oversight constraint, policy permission, residual risk |
| M2 Workflow/Decision-Process Integration | D_obs, WI_obs, WI_req, handoffs, execution authority | WI decision/constraint, D ceiling, K_Gamma capacity |
| M3 Human–AI Decision Configuration | A_obs, A target, q_obs, configuration preference/acceptability | A decision, q_im configuration choice, configuration compatibility |
| M4 Evaluation & Assurance | R_obs, EA_obs, EA_req, validation/recovery controls | EA decision/constraint, reliability/governance-risk components |
| M5 Learning/Resource Feedback | information availability, feedback/review cycle, resource capacity | R/K_Gamma in static baseline; dynamic t→t+1 only in later extension |
| T1 Temporal/Emerging | external technology transition indicators | exogenous TP_t scenario; not a baseline endogenous variable |

---

## 8. What should remain OUTSIDE the core construct model

### 8.1 Literature depletion statistics

`O/E`, BH q-values, and four-analysis consistency remain evidence descriptors. They justify why mechanisms deserve investigation. They never become utility/objective weights.

### 8.2 Industry context

`Z_t = (ID_t, TP_t, CP_t, SC_t, SP_t)`

These are exogenous scenario/calibration inputs:

- Industry demand
- Technology-transition pressure
- Cost pressure
- Supply constraints
- Standards/policy/qualification pressure

The exact five-component vector is researcher-designed. Vial and Jöhnk support context sensitivity, not this exact decomposition.

### 8.3 Public financial context

`F_t = (Revenue, Margin, OCF, Cash, R&D, CapEx, Leverage, SegmentExposure, ...)`

Public financials may bound affordability/value-at-stake scenarios such as `Btot` and `v_i`, but must not be used to infer D/R/A/G/H/WI/EA.

`Btot ≠ Cash` and `Btot ≠ R&D expense`.

### 8.4 G10 score-to-choice toy

`s_i`, `tau_i`, and `truth_i` should remain a sensitivity/benchmark module unless a real AI model and labeled outcomes exist. The enterprise study should not drift into classifier-threshold optimization without empirical data.

---

## 9. Proposed Multi-Level Programming interpretation after convergence

### Level 1 — Enterprise resource allocation

Question: **Where should scarce transformation resources be allocated?**

Decision variables: `b_i^D, b_i^A, b_i^R, b_i^G`.

Primary constraints/parameters: `Btot`, `c_i^r`, capability transition `phi_X`.

### Level 2 — AI decision architecture

Question: **For each use case, what target levels of AI integration, human oversight, workflow integration, and assurance are feasible and preferred?**

Decision variables: `A_i, H_i, WI_i, EA_i`.

Constraints: capability ceilings plus `D_req, R_req, H_req, WI_req, EA_req`, and shared organizational capacity `K_Gamma`.

### Level 3 — Human–AI configuration

Question: **Which work/decision arrangement should be selected?**

Current v1.0 menu:

- HumanOnly
- AIAssist
- HumanFirstAICheck
- AIFirstReview
- BoundedAutomation

Decision: `q_im`.

**Audit status:** literature supports delegation, sequential hybrid, aggregation, augmentation and automation as meaningful distinctions. The exact five-state menu is our operational design and must be validated for content coverage and mutual distinguishability.

---

## 10. Proposed research questions

**RQ1 — Structural evidence**  
Which AI-family × decision-family interfaces are robustly depleted relative to the fixed-degree/null expectation in the frozen corpus?

**RQ2 — Mechanism translation**  
Can these robust depletions be coherently translated into measurable organizational mechanisms involving governance/accountability, workflow integration, Human–AI configuration, assurance, and information/resource feedback?

**RQ3 — Requirement/capability fit**  
For specific enterprise decision use cases, what minimum D/R/H/WI/EA requirements are associated with different AI-integration depths, consequence classes, task types, and execution authority?

**RQ4 — Multilevel optimization**  
Given resource, capability, risk, governance and organizational-capacity constraints, which multilevel Human–AI decision architectures are selected by the model?

**RQ5 — Robustness**  
How stable are selected architectures across plausible parameter uncertainty and external industry/financial scenarios?

---

## 11. Candidate title / positioning

Preferred working title:

**From Structural Depletion to Decision Architecture: A Multi-Level Programming Framework for Human–AI Decision Configuration under Organizational Constraints**

Alternative enterprise-emphasis title:

**Optimizing Human–AI Decision Architectures under Capability, Governance, and Resource Constraints: Evidence from AI × Decision Structural Depletions**

Avoid in title/claims unless separately established:

- “16 research gaps”
- “16 organizational problems”
- “causal effect of structural holes”
- “empirically estimated optimal AI budget”

---

## 12. Identification status by parameter family

### Directly observable/codable after cases are frozen

- use-case type `u_i`, task type `t_i`, `exec_i`;
- current-state workflow facts;
- public financial/industry observations.

### Anchored expert-measurable

- `D_obs, R_obs, A_obs, G_obs, H_obs, WI_obs, EA_obs`;
- consequence class `kappa_i`;
- threshold functions `D_req/R_req/H_req/WI_req/EA_req`.

### Elicited preference/policy

- `Allow_mGamma`;
- objective priorities/weights;
- `Btot` Low/Base/High envelope;
- `K_Gamma` scenario capacity.

### Not point-identifiable from the planned cross-sectional evidence

- `phi_X` causal investment→capability transitions;
- exact `g_im` outcome multipliers;
- exact `beta_m` burden coefficients unless measured with repeated workflow/time data;
- exact continuous coefficients in Feas/Rel/Scalability/GovRisk/F1/F2/U.

These must remain bounded/fuzzy/scenario parameters and undergo sensitivity/robustness analysis unless stronger outcome data are obtained.

---

## 13. Falsification / audit checks for Claude

Please challenge the following explicitly:

1. **Evidence-to-mechanism validity:** Do G01–G16 logically justify M1–M5/T1, or are any assignments arbitrary or overlapping beyond defensibility?
2. **Construct distinctness:** Are D, R, A, G, H, WI and EA conceptually separable, especially G vs H vs EA and D vs WI?
3. **Measurement validity:** Are the 0–3 anchors observable and mutually distinguishable? Are there missing anchors or double-barreled definitions?
4. **Ordinal misuse:** Does any proposed equation still treat ordinal 0–3 levels as cardinal without explicit `z_X` mapping?
5. **Requirement elicitation:** Can experts reliably answer minimum-threshold vignettes, and what factorial design is needed to avoid impossible respondent burden?
6. **Common-source bias:** Are requirement and observed-state ratings being obtained from the same respondent too often?
7. **Endogeneity:** Does `v_i` or `Btot` accidentally absorb current firm performance in a way that makes the optimization tautological?
8. **Hierarchy validity:** Do L1, L2 and L3 represent genuinely sequential decision rights/response behavior, or merely an artificial decomposition of one optimization problem?
9. **Objective identifiability:** Which F1/F2/U coefficients can be defensibly elicited, and which must remain scenario weights?
10. **M5 scope:** Should G11/G12 remain future dynamic extension rather than be forced into the static baseline?
11. **T1/G04:** Is treating G04 as a temporal/exogenous monitor justified, or should it remain evidence-only until longitudinal corpus analysis is available?
12. **Five L3 configurations:** Are HumanFirstAICheck and AIFirstReview sufficiently distinct from Shrestha-style sequential structures, and is BoundedAutomation operationally clear?
13. **External validity:** Does a JPC calibration plus Fullon executive and Mega VC external validation support only a case-calibrated model, or can any broader claims be made?
14. **No privileged data:** Verify that every planned empirical input can be obtained from public data or consented expert/frontline elicitation without using privileged company records.
15. **Mathematical feasibility vs empirical validity:** Verify that v1.0 solver PASS is not being misrepresented as proof of empirical correctness.

---

## 14. Decision gate after review

Do **not** merge this calibration design into `main` or change the frozen v1.0 numerical model until the audit resolves:

- mechanism assignments;
- construct definitions;
- measurement anchors;
- threshold-vignette design;
- parameter identification class;
- multilevel hierarchy validity.

If these pass, the next freeze should be **Measurement Architecture v1.1**, followed by freezing 4–6 decision use cases and piloting the elicitation instrument.
