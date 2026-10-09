# Formal Proof and Scope — v1.0

A1. I, M and all prototype state domains are finite.
A2. b_i^r∈{0,1,2,3}; Btot≥0; zero Level-1 allocation is admissible.
A3. At A=0, D_req=R_req=H_req=EA_req=WI_req=0 for every context.
A4. HumanOnly has zero A/H/WI/EA requirements and Allow_HumanOnly,Gamma=1.
A5. CapUse(0,0,0,0)=0 and K_Gamma≥0.
A6. F1, F2 and U_im are finite on feasible discrete profiles.
A7. Level-3 followers are separable conditional on upstream decisions.
A8. Deterministic T1/T2/T3 select among multiple optima.
A9. Capability maps return states in L={0,1,2,3}.
A10. Static depletion-derived constraints admit the null HumanOnly architecture; A10 is retained as an explicit audit-summary condition.

Lemma L3:
HumanOnly makes each Level-3 feasible set nonempty. Finiteness and A6 imply an argmax. T3 selects a representative.

Lemma L2:
For any feasible x1, A9 gives finite nonnegative capability ceilings. Choose A=H=WI=EA=0. Capability bounds, A3 thresholds, Option alpha, A5 capacity and A10 are satisfied. Thus X2(x1) is finite and nonempty. F2 attains a maximum and T2 selects a representative.

Lemma L1:
The zero resource vector is feasible under A2 and X1 is finite.

Theorem 1':
Under A1–A10, fixed Gamma, initial state, parameter snapshot and T1–T3, at least one selected tri-level profile exists and exhaustive backward induction terminates finitely.

Selected-representative uniqueness is not argmax-set uniqueness.
Optimistic and pessimistic formulations are not generally equivalent.

T3 solver order:
HumanOnly, AIAssist, HumanFirstAICheck, AIFirstReview, BoundedAutomation.

If A7 fails:
- shared constraints require a coupled/generalized solution concept;
- payoff interaction may eliminate pure-equilibrium existence;
- cooperative joint objectives can be reformulated as one joint lower follower and re-proved.

Nash (1951) is a boundary reference only for mixed equilibrium in finite non-cooperative games.

Conformance caveat:
The canonical-state and generator tests share threshold-function implementations and cannot alone detect common-mode threshold defects.

Computational boundary:
Exact finite enumeration and existence here do not imply tractability for arbitrary continuous or nonconvex tri-level programs.

Claim scope:
PROVED FOR FINITE OPTION-ALPHA PROTOTYPE: nonempty feasibility, selected-response existence, finite termination.
COMPUTATIONALLY VERIFIED FOR TOY INSTANCES: nine scenarios; 768/3121/0 domain conformance; 720/768 mutation detection; G10 and permission probes.
EMPIRICALLY UNVERIFIED: all toy coefficients, thresholds, scores, truth states, permission matrices, governance orderings, and every JPC-specific conclusion.
