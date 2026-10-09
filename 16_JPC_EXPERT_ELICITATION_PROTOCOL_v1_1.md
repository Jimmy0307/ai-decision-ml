# JPC Expert Elicitation Protocol v1.1

Purpose: collect only the judgments and workflow evidence needed to calibrate the frozen v1.0 MLP. This protocol does **not** request confidential internal records, exact undisclosed budgets, ERP transaction dumps, private customer data, or privileged system logs.

## 1. Target panel

### Core JPC internal panel: 14 respondents

#### Strategic layer — 4
1. Chairman
2. General Manager
3. COO
4. Finance leader / senior accounting-finance manager

#### Technical / functional layer — 7
5. IT/MIS leader
6. IT/MIS engineer A
7. IT/MIS engineer B
8. RDPM
9. Senior mechanical engineer
10. Procurement / SCM representative
11. QA/quality leader **or**, if unavailable, Plant Manager

#### Frontline / actual-workflow layer — 3
12. Accounting/finance operator
13. Sales or sales-assistant user
14. Production / planning / factory-floor user

### Optional JPC respondent
15. Spokesperson / IR-facing representative — market/company-public-strategy triangulation only; not a substitute for IT or process experts.

### External validation — 2
16. Fullon senior executive spanning R&D / Marketing / Sales
17. Mega Venture Capital investment evaluator

External validators are **not pooled** with JPC internal respondents. Their role is challenge / triangulation, not firm-specific parameter averaging.

## 2. Why 14 internal respondents

The goal is not a large-sample SEM survey. The goal is **role-structured parameter elicitation**. Each parameter family is answered primarily by respondents with relevant epistemic authority.

Do not average every respondent equally. For parameter `j`, aggregation may use role-specific weights `omega_ej`:

`theta_hat_j = sum_e(omega_ej * x_ej) / sum_e(omega_ej)`

The weights represent **relevance to the parameter**, not organizational rank.

Examples:

- `EA_req`: QA/plant-manager and IT/process-expert weight high.
- `B^tot`: finance and senior management weight high.
- `K_Gamma`: COO and IT weight high.
- `D0/R0`: IT/MIS weight high.
- `v_i`: executives + process owner + external market validator weight high.

Where disagreement is substantively meaningful, preserve it as an interval / scenario instead of forcing a mean.

## 3. Common Core — 6 questions for all internal respondents

Use the same frozen set of 4–6 decision use cases for every respondent.

### C1 — AI value priority
Which 2–3 decision processes would create the greatest value if improved with AI assistance or automation? Rank them.

**Supports:** `v_i` relative ordering.

### C2 — consequence class
If the decision is wrong, how serious is the consequence?

- Low: easily corrected, limited operational impact.
- Medium: material cost, delay, customer or coordination impact.
- High: major quality, customer, financial, compliance or strategic impact.

**Supports:** `kappa_i`.

### C3 — maximum acceptable Human–AI configuration
For this decision, what is the highest configuration that should be allowed under normal governance?

1. HumanOnly
2. AIAssist
3. HumanFirstAICheck
4. AIFirstReview
5. BoundedAutomation

**Supports:** `Allow_mGamma`, configuration compatibility evidence.

### C4 — minimum human oversight
What is the minimum human-oversight level required if AI participates?

Use the frozen `H` 0–3 anchors.

**Supports:** `H_req`.

### C5 — minimum evaluation / assurance
What is the minimum evaluation/assurance level required before and during use?

Use frozen `EA` 0–3 anchors.

**Supports:** `EA_req`.

### C6 — minimum workflow integration
How deeply must AI be connected to actual workflow before it creates material value?

Use frozen `WI` 0–3 anchors.

**Supports:** `WI_req`.

## 4. Chairman / General Manager module — 8 additional questions

Total target: **14 questions**, approximately 20–30 minutes.

### E1 — most important enterprise criterion
Among enterprise value, reliability, scalability, integration cost, governance risk and downstream user utility, which criterion is most important for AI/digital-transformation decisions?

### E2 — least important enterprise criterion
Which criterion is least important?

E1/E2 are the starting anchors for BWM/fuzzy-BWM elicitation of objective priorities; respondents are not asked to invent exact optimizer coefficients.

### E3 — capability-investment priority
When resources are limited, which capability category would normally receive priority: digital/process infrastructure, data readiness, AI integration, or governance?

### E4 — non-automation boundary
What types of decisions should remain human-controlled even if AI performance is high?

### E5 — strategic transformation load
How many major transformation initiatives can the organization realistically absorb at the same time before execution quality deteriorates?

Use broad categories / scenarios rather than a pseudo-precise number.

**Supports:** `K_Gamma`.

### E6 — stop / defer conditions
What conditions would cause management to pause, defer or reduce a digital/AI investment?

### E7 — short-term ROI vs long-term capability
When short-term financial return conflicts with long-term strategic capability, how is the trade-off normally resolved?

### E8 — downturn response
If industry conditions deteriorate materially, which categories of investment would be reduced first and which would be protected?

**Supports:** `F1` preference structure, `B^tot` scenarios, governance constraints.

## 5. COO module — 8 additional questions

Total target: **14 questions**.

1. At what point does running multiple transformation projects simultaneously create organizational overload?
2. Which bottlenecks appear first: people, systems, data, approvals, coordination, supplier/customer interfaces, or governance?
3. Which workflow handoffs most often block implementation?
4. Does an AI recommendation have real value if it remains outside ERP/MES/operational workflow? Under what conditions?
5. Which operational decisions always require escalation or human override?
6. What is the biggest barrier to moving from AI assistance to bounded execution?
7. What creates the greatest implementation burden: integration, training, validation, exception handling, change management, or maintenance?
8. What makes a solution scalable across departments / plants / processes?

**Supports:** `K_Gamma`, `WI_req`, burden assumptions, scalability construct validity.

## 6. Finance module — 6 additional questions

Total target: **12 questions**.

Do not request undisclosed exact budgets.

1. What financial conditions matter most when judging whether a transformation investment is affordable?
2. Which downside financial risk is least acceptable?
3. Which cost type is most likely to constrain adoption: CapEx, recurring Opex, maintenance, integration, training, or uncertain payback?
4. Which public-style indicators best represent investment capacity: OCF, cash, leverage, margin, R&D intensity, CapEx intensity, payback, or another metric?
5. Define Low / Base / High transformation-capacity scenarios without revealing confidential budget figures.
6. If growth opportunity is high but uncertainty also rises, how should investment capacity or hurdle rates change?

**Supports:** `B_L/B_M/B_H`, `c_i^r` interpretation, L1 financial preference.

## 7. IT/MIS module — 10 additional questions

Total target: **16 questions**.

### T1–T4 — baseline capability coding
Using the frozen anchors, score current use-case-specific:

- `D_i^0`
- `R_i^0`
- `A_i^0`
- `G_i^0`

For each score, require one observable justification sentence.

### T5 — anchor check
What concrete system/data/governance condition distinguishes each adjacent level (0→1, 1→2, 2→3)?

### T6 — digital prerequisite
For AI integration depth `A=1,2,3`, what is the minimum `D` level required?

**Supports:** `D_req(A)`.

### T7 — data prerequisite
For `A=1,2,3`, what is the minimum `R` level required?

**Supports:** `R_req(A)`.

### T8 — workflow prerequisite
For `A=1,2,3`, what is the minimum `WI` level required?

**Supports:** `WI_req(A)`.

### T9 — capability transition
What must actually change for a capability to move from level `x` to `x+1`? Do not answer in terms of money only; identify systems, interfaces, data quality, permissions, governance, testing and staffing requirements.

**Supports:** monotone `phi_X` transition design.

### T10 — dominant technical bottleneck
Rank data, integration, permission/security, reliability, infrastructure and change-management bottlenecks.

## 8. Functional / process module — RDPM, senior mechanical engineer, procurement, QA or plant manager

Common Core + 8 questions = **14 questions**.

1. Identify the 2–3 most important recurring decisions in your work.
2. Classify each decision as prediction, recommendation, selection, allocation/planning, execution, or mixed.
3. What happens if the decision is wrong? Provide Low/Medium/High consequence and a short reason.
4. If AI participates, what is the minimum human review / override arrangement?
5. What validation, evidence, traceability or quality checks are required before accepting the output?
6. How deeply must the output connect into workflow or systems before it becomes useful?
7. Among the five Human–AI configurations, which is most likely to improve performance for this decision and why?
8. Which configuration would create the highest operational/cognitive burden and why?

**Supports:** `u_i`, `t_i`, `exec_i`, `kappa_i`, `H_req`, `EA_req`, `WI_req`, `g_im`, `beta_m`.

### QA fallback rule
If QA/quality leadership is not available, use the **Plant Manager** as the operational-assurance respondent. If both are available, retain both and treat QA as assurance-focused and Plant Manager as execution-focused.

## 9. Frontline module — accounting, sales/sales assistant, production/planning/floor

Target: **12 questions**, approximately 10–15 minutes.

The frontline module measures actual workflow, not strategy.

1. What decisions do you personally make or prepare most often?
2. What information/data do you need before deciding?
3. How many handoffs or approvals normally occur?
4. Who has final approval or override authority?
5. Where does rework most often occur?
6. Which step consumes the most time or attention?
7. If AI gives a recommendation, would you independently re-check it? Why?
8. If AI is wrong, is the error easy to detect before impact occurs?
9. If AI output cannot enter the existing system/workflow directly, how useful is it?
10. Which step is suitable for AI assistance today?
11. Which step should not be automated today?
12. Would adding AI likely reduce, preserve or increase total workload? What new work would be created?

**Supports observed-state measures:** `H_obs`, `WI_obs`, `EA_obs`, `Burden_obs`, approval/handoff evidence.

## 10. Spokesperson / public-strategy triangulation module — optional

Target: Common Core + 4 questions = **10 questions**.

1. Which product/market themes are publicly presented as major growth drivers?
2. Which public risks are most material to the company's strategic outlook?
3. Which publicly observable financial/operational indicators best reflect strategic capacity?
4. Which statements can be supported using annual reports, quarterly reports, investor materials or public announcements?

**Supports:** `v_i` external/business validity and `Z_t/F_t` provenance. Does not score IT maturity.

## 11. External Fullon module

Target: approximately **12 questions**.

Role: cross-functional technology–market challenge of JPC-specific assumptions.

Focus on:

- technology and market pressure;
- risk class of R&D / product / marketing / sales decisions;
- Human–AI oversight boundaries;
- workflow integration requirements;
- evaluation/assurance requirements;
- relative value of Human–AI configurations;
- whether JPC-derived thresholds appear firm-specific or industry-plausible.

Do not request confidential Fullon data.

## 12. External Mega VC module

Target: approximately **10 questions**.

Role: capital/value/risk challenge.

Focus on:

- how growth, margin, cash generation, R&D, CapEx, customer/market concentration and downside risk enter investment judgment;
- what makes technology investment financially credible;
- how strategic value differs from short-term ROI;
- how uncertainty changes acceptable investment capacity;
- whether public-data-based `v_i` and `B^tot` scenarios are economically plausible.

Do not request confidential investment-committee scores, due-diligence records or non-public IPO materials.

## 13. Data handling rule

Every response used in calibration must store:

- respondent role category, not unnecessary personal identifiers;
- parameter(s) informed;
- question ID;
- raw ordinal/category response;
- short rationale;
- provenance (`EXPERT_ELICITED` or `CONSENTED_OBSERVED`);
- uncertainty / disagreement;
- transformation rule used to enter the model.

## 14. Minimum success condition

The panel is sufficient to begin empirical calibration when:

- every major parameter family has at least one role-authoritative source;
- every threshold family has at least two perspectives when possible;
- frontline workflow evidence exists for at least one use case in each major process class;
- disagreements are preserved as ranges/scenarios;
- no confidential internal record is required to run the model.
