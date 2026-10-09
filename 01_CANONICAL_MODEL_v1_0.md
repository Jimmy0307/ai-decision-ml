# AI × Decision × Multi-Level Programming — Canonical v1.0 Mathematical Freeze

Status: mathematical-feasibility skeleton frozen after Claude v0.9 re-validation.

## Evidence boundary

All executable coefficients, thresholds, scores, truth states, rankings and numerical outputs are SIMULATED. No privileged internal JPC data are used.

A robust depletion is a document-level AI-family × Decision-family cell whose observed edge count is significantly below the specified null expectation (BH q <= .05) and whose depletion direction is consistent in all four V5 analyses. It describes literature-network structure conditional on observed marginals. It is NOT a field-wide absence claim and NOT an enterprise practical-problem claim. O/E and q values are evidence descriptors only and never optimization weights.

## Governing G01–G16 source

The governing canonical source for v1.0 is the Priority_Gaps tab of:
AI × Decision Making｜Gap & Literature Matrix
https://docs.google.com/spreadsheets/d/19OBPkXP6v9DQJCW-ygCqHKCnsgkkAr3-_IP3Q1s-Wr4/edit

The pack contains 11_Priority_Gaps_Frozen_Export_G01_G16_v1_0_20261009.csv with Gap_ID, family codes, k_a, k_d, M, E_analytic, Observed, Null_Mean, O/E, all four manuscript q values, all four direction indicators and robustness flags.

A separate file-level derivation from an independent V5 Data Pack export is not established here. Priority_Gaps governs v1.0. Any future conflict must be explicitly reconciled before publication.

## O/E semantics

M = 2,180.
E_analytic = k_a*k_d/M.
O_E_Ratio = Observed/E_analytic.

Null_Mean is the mean of the 10,000 fixed-degree null replicates and is NOT the denominator of O_E_Ratio.

## Canonical thresholds

D_req(A)=A
R_req(A)=A

H_req(A,kappa,u)=0 if A=0; else min(3,max(0,A+kappa-2+adj_u))
EA_req(A,kappa,t)=0 if A=0; else min(3,max(1,A+kappa-2+adj_t))
WI_req(A,kappa,exec)=0 if A=0; =3 if exec=true and A=3; else A

All adj_u and adj_t equal 0 in v1.0.

## Level 1

b_i^r ∈ {0,1,2,3}, r ∈ {D,A,R,G}
Σ_i,r c_i^r b_i^r ≤ Btot
toy c_i^r=1.

Dbar=phi_D(D0,bD), Abar=phi_A(A0,bA), Rbar=phi_R(R0,bR), Gbar=phi_G(G0,bG)
toy phi_X=min(3,X0+b)

RealizedValue=Σ_i max(0,Gain_i*)
ResourceUse=Σ_i,r c_i^r b_i^r
ResidualRisk=Σ_i ResidualRisk_i*

F1=1.25 RealizedValue +0.20 AIAdoptions -0.22 ResourceUse -0.75 ResidualRisk

## Level 2

A,H,WI,EA ∈ {0,1,2,3}

0≤A≤Abar
0≤H,EA≤Gbar
0≤WI≤Dbar

Dbar≥D_req(A)
Rbar≥R_req(A)
H≥H_req(A,kappa,u)
EA≥EA_req(A,kappa,t)
WI≥WI_req(A,kappa,exec)

Option alpha:
H≤3A
EA≤3A
WI≤3A

CapUse=.42A+.24H+.24EA+.20WI
Σ CapUse≤K_Gamma

Feas=clip[0,1](.55+.08(Dbar-D_req)+.08(Rbar-R_req)+.04(Gbar-max(H_req,EA_req)))
Rel=clip[0,1](.45+.10EA+.06H+.04WI-.030A*kappa)
Scalability=clip[0,1](.30+.08Dbar+.08Rbar+.04WI)
IntegrationCost=cost_Gamma(.10A+.06WI+.05H+.05EA)
GovRisk=0 if A=0 else risk_Gamma*.08*kappa*A/(1+.4H+.4EA)

F2=Σ_i[.90Feas+.90Rel+.45Scalability-.55IntegrationCost-.75GovRisk+.65max(0,U_i*)]

## Level 3

q_im∈{0,1}; Σ_m q_im=1
y_i=1-q_i,HumanOnly

A≥Σ_m A_req^m q_im
H≥Σ_m H_req^m q_im
WI≥Σ_m WI_req^m q_im
EA≥Σ_m EA_req^m q_im
q_im≤Allow_mGamma

HumanOnly=(0,0,0,0)
AIAssist=(1,0,1,1)
AIFirstReview=(2,2,2,2)
HumanFirstAICheck=(2,1,2,1)
BoundedAutomation=(3,3,3,3)

Gain=g_im*v_i*psi_i*flex_Gamma
Burden=beta_m+.03H+.02EA+.02WI
ResidualRisk=kappa*autonomy_m*risk_Gamma/(1+.45H+.45EA)
U_im=Gain-.45Burden-.75ResidualRisk

G15 belongs to configuration compatibility.
G16 is BASELINE_BRIDGE evidence for the BoundedAutomation row and is not an extra hard constraint.

## G10 / G14

Selection:
d_i=1[s_i>=tau_i]
V(d,truth)=1 if correct else .35.

Non-selection:
d_i undefined; V=1.

s_i and truth_i are known to all three toy levels. This is a perfect-information single-realization sensitivity toy, not an ex-ante uncertainty/error-rate model.

At tau_P2=.70, Level 1 sets P2 b_A=0, so Abar_P2=0 and Level 2 must choose A=0.
At fixed Level-2 state (1,1,1,1), Level 3 still prefers AIAssist.

HumanOnly => adopted decision=N/A and reported psi=N/A.

psi=(1+.05EA+.03WI)*V(d,truth)>=0.

## Roles

BASELINE: G01,G02,G03,G05,G06,G07,G08,G09,G10,G13,G14,G15
BASELINE_BRIDGE: G16
DYNAMIC: G11,G12
TEMPORAL_MONITOR: G04
Static role count=13.

## Tie breaking

T3:
max U -> min Burden -> min ResidualRisk ->
HumanOnly, AIAssist, HumanFirstAICheck, AIFirstReview, BoundedAutomation.

T2:
max ΣF2 -> min ΣCapUse -> min ΣGovRisk ->
lexicographically smallest (A,H,WI,EA,configuration-rank), using T3 rank.

T1:
max F1 -> min Σb -> min ResidualRisk ->
lexicographically smallest allocation vector.

These rules select a deterministic representative. They do not imply singleton argmax sets and do not establish optimistic/pessimistic equivalence.

## Exactness

Generator-vs-canonical: 768 cases, 3,121 canonical-feasible state occurrences, 0 mismatch.
Real generator mutation: 720/768 detected.
Nine baseline scenarios reproduce.

The conformance test shares D_req/R_req/H_req/EA_req/WI_req implementations between oracle and generator. It detects generator-domain regressions but cannot by itself detect a common-mode defect in those shared functions.

Exact enumeration of this bounded finite prototype is NOT a tractability claim for arbitrary continuous or nonconvex tri-level programs.
