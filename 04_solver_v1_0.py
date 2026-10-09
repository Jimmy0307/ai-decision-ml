
from itertools import product
from functools import lru_cache
import json, time

# ============================================================
# AI × Decision × Multi-Level Programming
# Mathematical Feasibility Prototype v1.0
#
# ALL NUMERIC VALUES ARE SIMULATED.
# NO PRIVILEGED INTERNAL JPC DATA ARE USED.
#
# Canonical objective implementation:
#   L3: U_im = Gain_im - 0.45*Burden_im - 0.75*ResidualRisk_im
#   L2: F2 = sum_i(0.90*Feas + 0.90*Rel + 0.45*Scalability
#                  -0.55*IntegrationCost -0.75*GovRisk
#                  +0.65*max(0,U_i*))
#   L1: F1 = 1.25*RealizedValue +0.20*AIAdoptions
#            -0.22*ResourceUse -0.75*ResidualRisk
#
# Exactness claim:
# exact only over the stated bounded finite Option-alpha prototype domain.
# ============================================================

TOY_RESOURCE_UNIT_COST = 1.0
INCORRECT_DECISION_FACTOR = 0.35

PROCESSES = [
    {"id":"P1","name":"Low-risk informational support","risk":1,
     "D0":1,"R0":1,"A0":0,"G0":1,"value":1.0,
     "selection":False,"execution":False,"tau":0.40,
     "score":None,"truth":None,
     "use_mode":"prediction","task_class":"prediction"},
    {"id":"P2","name":"Medium-risk recommendation/selection","risk":2,
     "D0":1,"R0":1,"A0":0,"G0":1,"value":1.2,
     "selection":True,"execution":False,"tau":0.60,
     "score":0.65,"truth":1,
     "use_mode":"recommendation","task_class":"selection"},
    {"id":"P3","name":"High-risk bounded execution","risk":3,
     "D0":2,"R0":2,"A0":0,"G0":1,"value":1.5,
     "selection":True,"execution":True,"tau":0.70,
     "score":0.72,"truth":1,
     "use_mode":"execution","task_class":"execution"},
]

GOVERNANCE = {
    "C":{"name":"C","K":5.5,"risk_mult":0.85,"cost_mult":1.10,"flex_mult":0.95},
    "F":{"name":"F","K":6.0,"risk_mult":1.00,"cost_mult":1.00,"flex_mult":1.00},
    "D":{"name":"D","K":6.5,"risk_mult":1.15,"cost_mult":0.90,"flex_mult":1.05},
}

CONFIG_ORDER = ["HumanOnly","AIAssist","HumanFirstAICheck","AIFirstReview","BoundedAutomation"]
CONFIG_RANK = {name:i for i,name in enumerate(CONFIG_ORDER)}

# G09: governance may alter the feasible configuration set.
# Baseline toy keeps all configurations allowed; permission sensitivity is tested separately.
ALLOW_CONFIG = {
    "C": {m: True for m in CONFIG_ORDER},
    "F": {m: True for m in CONFIG_ORDER},
    "D": {m: True for m in CONFIG_ORDER},
}

Q_DEFS = {
    "HumanOnly":{"A":0,"H":0,"WI":0,"EA":0,"gain":[0.0,0.0,0.0],"burden":0.0,"autonomy":0.0},
    "AIAssist":{"A":1,"H":0,"WI":1,"EA":1,"gain":[0.80,0.60,0.40],"burden":0.15,"autonomy":0.20},
    "AIFirstReview":{"A":2,"H":2,"WI":2,"EA":2,"gain":[0.65,0.90,0.70],"burden":0.25,"autonomy":0.50},
    "HumanFirstAICheck":{"A":2,"H":1,"WI":2,"EA":1,"gain":[0.75,1.00,0.80],"burden":0.30,"autonomy":0.40},
    "BoundedAutomation":{"A":3,"H":3,"WI":3,"EA":3,"gain":[0.40,0.70,1.20],"burden":0.10,"autonomy":1.00},
}

def D_req(A): return A
def R_req(A): return A

def H_req(A, risk, use_mode):
    # G02 and G08 share H but are distinguished by u=use_mode.
    if A == 0:
        return 0
    mode_adjust = {"prediction":0, "recommendation":0, "execution":0}[use_mode]
    return min(3, max(0, A + risk - 2 + mode_adjust))

def EA_req(A, risk, task_class):
    # G05 and G13 share EA but are distinguished by t=task_class.
    # The v1.0 toy does NOT instantiate an allocation process; G05's allocation slice
    # remains a formal/calibration role only.
    if A == 0:
        return 0
    task_adjust = {"prediction":0, "selection":0, "allocation":0, "execution":0}[task_class]
    return min(3, max(1, A + risk - 2 + task_adjust))

def WI_req(A, risk, execution):
    if A == 0:
        return 0
    if execution and A == 3:
        return 3
    return A

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))

def decision_consequence_factor(p):
    """G10 explicit score -> threshold -> decision -> outcome link.
    Returns (decision, factor).  All values are SIMULATED.
    """
    if not p["selection"]:
        # No selection decision exists for this process in the toy; define V ≡ 1.
        return None, 1.0
    d = int(p["score"] >= p["tau"])
    correct = (d == int(p["truth"]))
    # Explicit simulated downstream consequence of the realized choice.
    # Correct choice preserves full local benefit; incorrect choice realizes only 35%.
    return d, (1.0 if correct else INCORRECT_DECISION_FACTOR)

def psi_value(WI, EA, p):
    """G14 unified nonnegative value-realization multiplier.
    Signature is psi_i(WI_i, EA_i, tau_i; s_i, truth_i); s and truth enter through p. tau acts through the realized decision consequence.
    q affects realized value through configuration-specific base gain, not inside psi.
    """
    _, decision_factor = decision_consequence_factor(p)
    return max(0.0, (1.0 + 0.05*EA + 0.03*WI) * decision_factor)

def l3_best(proc_idx, A, H, WI, EA, gov):
    """Level-3 best response over allowed Human-AI configurations."""
    p = PROCESSES[proc_idx]
    best = None
    best_key = None

    for qn, qd in Q_DEFS.items():
        if not ALLOW_CONFIG[gov["name"]][qn]:
            continue
        if A < qd["A"] or H < qd["H"] or WI < qd["WI"] or EA < qd["EA"]:
            continue

        decision, _ = decision_consequence_factor(p)
        psi = psi_value(WI, EA, p)
        realized_gain = qd["gain"][proc_idx] * p["value"] * psi * gov["flex_mult"]

        residual_risk = (
            p["risk"] * qd["autonomy"] * gov["risk_mult"]
            / (1.0 + 0.45*H + 0.45*EA)
        )

        burden = qd["burden"] + 0.03*H + 0.02*EA + 0.02*WI
        utility = realized_gain - 0.45*burden - 0.75*residual_risk

        rec = {
            "q":qn,
            "decision":decision,
            "utility":utility,
            "gain":realized_gain,
            "psi":psi,
            "risk":residual_risk,
            "burden":burden,
        }
        key = (
            round(utility,12),
            -round(burden,12),
            -round(residual_risk,12),
            -CONFIG_RANK[qn],
        )
        if best is None or key > best_key:
            best, best_key = rec, key
    return best

def canonical_state_set(proc_idx, caps):
    """Mathematical Level-2 state set implied by the canonical v1.0 constraints.
    This is written independently of the generator loops and is used for conformance tests.
    """
    Dcap, Acap, Rcap, Gcap = caps
    p = PROCESSES[proc_idx]
    out = set()
    for A,H,WI,EA in product(range(4), repeat=4):
        if A > Acap or H > Gcap or EA > Gcap or WI > Dcap:
            continue
        if Dcap < D_req(A) or Rcap < R_req(A):
            continue
        if H < H_req(A,p["risk"],p["use_mode"]):
            continue
        if EA < EA_req(A,p["risk"],p["task_class"]):
            continue
        if WI < WI_req(A,p["risk"],p["execution"]):
            continue
        # Option alpha. On L={0,1,2,3}, these bind only at A=0.
        if H > 3*A or EA > 3*A or WI > 3*A:
            continue
        out.add((A,H,WI,EA))
    return out

def l2_options_for_proc(proc_idx, caps, gov, enforce_option_alpha=True, mutant_relax_A0_generator=False):
    """Solver generator for feasible L2 architectures.
    enforce_option_alpha=False is used only by the mutation regression test.
    """
    Dcap, Acap, Rcap, Gcap = caps
    p = PROCESSES[proc_idx]
    opts = []

    for A in range(0, Acap+1):
        if Dcap < D_req(A) or Rcap < R_req(A):
            continue

        if A == 0:
            if mutant_relax_A0_generator:
                Hvals = range(0,Gcap+1)
                Evals = range(0,Gcap+1)
                Wvals = range(0,Dcap+1)
            else:
                Hvals = Evals = Wvals = [0]
        else:
            hmin = H_req(A,p["risk"],p["use_mode"])
            emin = EA_req(A,p["risk"],p["task_class"])
            wmin = WI_req(A,p["risk"],p["execution"])
            if hmin > Gcap or emin > Gcap or wmin > Dcap:
                continue
            Hvals = range(hmin,Gcap+1)
            Evals = range(emin,Gcap+1)
            Wvals = range(wmin,Dcap+1)

        for H in Hvals:
            for EA in Evals:
                for WI in Wvals:
                    if enforce_option_alpha and (H > 3*A or EA > 3*A or WI > 3*A):
                        continue

                    hmin = H_req(A,p["risk"],p["use_mode"])
                    emin = EA_req(A,p["risk"],p["task_class"])

                    capuse = 0.42*A + 0.24*H + 0.24*EA + 0.20*WI
                    feasibility = clamp(
                        0.55
                        + 0.08*(Dcap-D_req(A))
                        + 0.08*(Rcap-R_req(A))
                        + 0.04*(Gcap-max(hmin,emin))
                    )
                    reliability = clamp(
                        0.45 + 0.10*EA + 0.06*H + 0.04*WI
                        - 0.030*A*p["risk"]
                    )
                    scalability = clamp(0.30 + 0.08*Dcap + 0.08*Rcap + 0.04*WI)
                    integration_cost = gov["cost_mult"]*(0.10*A + 0.06*WI + 0.05*H + 0.05*EA)
                    governance_risk = gov["risk_mult"]*(
                        0.0 if A==0 else 0.08*p["risk"]*A/(1.0+0.4*H+0.4*EA)
                    )

                    l3 = l3_best(proc_idx,A,H,WI,EA,gov)

                    f2 = (
                        0.90*feasibility
                        + 0.90*reliability
                        + 0.45*scalability
                        - 0.55*integration_cost
                        - 0.75*governance_risk
                        + 0.65*max(0.0,l3["utility"])
                    )

                    opts.append({
                        "A":A,"H":H,"WI":WI,"EA":EA,
                        "capuse":capuse,"feas":feasibility,"rel":reliability,
                        "scale":scalability,"icost":integration_cost,
                        "grisk":governance_risk,"l3":l3,"f2":f2,
                    })
    return opts

def generated_state_set(proc_idx, caps, gov_name="F", enforce_option_alpha=True, mutant_relax_A0_generator=False):
    return {
        (o["A"],o["H"],o["WI"],o["EA"])
        for o in l2_options_for_proc(
            proc_idx,caps,GOVERNANCE[gov_name],
            enforce_option_alpha=enforce_option_alpha,
            mutant_relax_A0_generator=mutant_relax_A0_generator
        )
    }

@lru_cache(None)
def best_l2_cached(gov_name, caps_tuple):
    gov = GOVERNANCE[gov_name]
    capsets = [caps_tuple[i*4:(i+1)*4] for i in range(3)]
    optlists = [l2_options_for_proc(i,capsets[i],gov) for i in range(3)]
    if any(not x for x in optlists):
        return None

    best = None
    best_key = None
    enumerated = 0
    for o1 in optlists[0]:
        for o2 in optlists[1]:
            for o3 in optlists[2]:
                enumerated += 1
                cap = o1["capuse"]+o2["capuse"]+o3["capuse"]
                if cap > gov["K"] + 1e-9:
                    continue
                opts=[o1,o2,o3]
                f2=sum(o["f2"] for o in opts)
                grisk=sum(o["grisk"] for o in opts)
                arch=tuple((o["A"],o["H"],o["WI"],o["EA"],CONFIG_RANK[o["l3"]["q"]]) for o in opts)
                key=(round(f2,12),-round(cap,12),-round(grisk,12),
                     tuple(-v for item in arch for v in item))
                rec={"opts":opts,"F2":f2,"capuse":cap,"enumerated":enumerated}
                if best is None or key > best_key:
                    best,best_key=rec,key
    return best

def generate_allocations(B):
    """All b_i^r in {0,1,2,3} with normalized resource cost <= B.
    Canonical v1.0 toy uses c_i^r = TOY_RESOURCE_UNIT_COST = 1 for all i,r.
    """
    assert TOY_RESOURCE_UNIT_COST == 1.0, "Enumeration assumes the canonical toy normalization c_i^r=1."
    out=[]
    max_units = int(B / TOY_RESOURCE_UNIT_COST)
    for total in range(max_units+1):
        def rec(n,rem,prefix):
            if n==1:
                if rem<=3:
                    yield prefix+(rem,)
                return
            for v in range(min(3,rem)+1):
                yield from rec(n-1,rem-v,prefix+(v,))
        out.extend(rec(12,total,()))
    return out

def caps_from_alloc(a):
    caps=[]
    for i,p in enumerate(PROCESSES):
        bD,bA,bR,bG=a[4*i:4*i+4]
        caps.extend([
            min(3,p["D0"]+bD),
            min(3,p["A0"]+bA),
            min(3,p["R0"]+bR),
            min(3,p["G0"]+bG),
        ])
    return tuple(caps)

def f1_for(alloc,l2):
    value=sum(max(0.0,o["l3"]["gain"]) for o in l2["opts"])
    risk=sum(o["l3"]["risk"] for o in l2["opts"])
    adoptions=sum(o["l3"]["q"]!="HumanOnly" for o in l2["opts"])
    resource_use = TOY_RESOURCE_UNIT_COST * sum(alloc)
    F1=1.25*value + 0.20*adoptions - 0.22*resource_use - 0.75*risk
    return F1,value,risk,adoptions

def solve(governance,B):
    best=None
    best_key=None
    allocations=generate_allocations(B)
    for alloc in allocations:
        caps=caps_from_alloc(alloc)
        l2=best_l2_cached(governance,caps)
        if l2 is None:
            continue
        F1,value,risk,adoptions=f1_for(alloc,l2)
        rec={"governance":governance,"budget":B,"F1":F1,"F2":l2["F2"],
             "alloc":alloc,"caps":caps,"value":value,"risk":risk,
             "adoptions":adoptions,"l2":l2,
             "l1_allocations_enumerated":len(allocations)}
        key=(round(F1,12),-sum(alloc),-round(risk,12),tuple(-v for v in alloc))
        if best is None or key > best_key:
            best,best_key=rec,key
    return best

def public_result(r):
    return {
        "governance":r["governance"],"budget":r["budget"],
        "F1_best":round(r["F1"],6),"F2_response":round(r["F2"],6),
        "L1_allocation_vector":list(r["alloc"]),"caps":list(r["caps"]),
        "realized_value":round(r["value"],6),"residual_risk":round(r["risk"],6),
        "AI_adoptions":r["adoptions"],
        "processes":[
            {
                "process":PROCESSES[i]["id"],
                "A":o["A"],"H":o["H"],"WI":o["WI"],"EA":o["EA"],
                "configuration":o["l3"]["q"],
                "AI_recommended_decision":o["l3"]["decision"],
                "adopted_decision":(None if o["l3"]["q"]=="HumanOnly" else o["l3"]["decision"]),
                "reported_psi":(None if o["l3"]["q"]=="HumanOnly" else round(o["l3"]["psi"],6)),
                "local_utility":round(o["l3"]["utility"],6)
            }
            for i,o in enumerate(r["l2"]["opts"])
        ],
        "status":"SIMULATED FEASIBILITY ONLY — NOT EMPIRICAL RESULT",
    }

def structural_proof_checks():
    c={}
    c["A0_thresholds_zero"]=all([
        D_req(0)==0,R_req(0)==0,
        H_req(0,1,"prediction")==0,
        H_req(0,2,"recommendation")==0,
        H_req(0,3,"execution")==0,
        EA_req(0,1,"prediction")==0,
        EA_req(0,2,"selection")==0,
        EA_req(0,3,"execution")==0,
        WI_req(0,1,False)==0,WI_req(0,3,True)==0,
    ])
    c["HumanOnly_requirements_zero"]=all(Q_DEFS["HumanOnly"][k]==0 for k in ["A","H","WI","EA"])
    c["HumanOnly_allowed_all_governance"]=all(ALLOW_CONFIG[g]["HumanOnly"] for g in GOVERNANCE)
    c["governance_capacity_nonnegative"]=all(g["K"]>=0 for g in GOVERNANCE.values())
    c["zero_allocation_exists"]=(0,)*12 in generate_allocations(0)
    for gn,gov in GOVERNANCE.items():
        ok=True
        for i,p in enumerate(PROCESSES):
            caps=(p["D0"],p["A0"],p["R0"],p["G0"])
            if (0,0,0,0) not in generated_state_set(i,caps,gn):
                ok=False
        c[f"null_architecture_exists_{gn}"]=ok
    c["all_sufficient_conditions_pass"]=all(c.values())
    return c

def generator_vs_canonical_domain_check():
    """H1 fix: this check calls the real solver generator and independently evaluates
    the written canonical constraints for every process x every 4^4 ceiling tuple.
    """
    mismatches=[]
    total_cases=0
    canonical_states=0
    for i in range(len(PROCESSES)):
        for caps in product(range(4),repeat=4):
            total_cases += 1
            canon=canonical_state_set(i,caps)
            gen=generated_state_set(i,caps,"F")
            canonical_states += len(canon)
            if canon != gen:
                mismatches.append({
                    "process":PROCESSES[i]["id"],"caps":list(caps),
                    "canonical_only":[list(x) for x in sorted(canon-gen)],
                    "generator_only":[list(x) for x in sorted(gen-canon)],
                })
    return {
        "cases":total_cases,
        "canonical_feasible_states_counted_with_repetition":canonical_states,
        "mismatch_cases":len(mismatches),
        "pass":len(mismatches)==0,
        "first_mismatches":mismatches[:5],
    }

def mutation_sensitivity_check():
    """Mutation regression test that exercises the REAL generator path.
    The mutant disables Option-alpha in l2_options_for_proc and compares it
    against the canonical state set across 3 processes x 256 ceiling tuples.
    """
    mismatch_cases = 0
    total_cases = 0
    for i in range(len(PROCESSES)):
        for caps in product(range(4), repeat=4):
            total_cases += 1
            canon = canonical_state_set(i, caps)
            mutant = generated_state_set(i, caps, "F", enforce_option_alpha=False, mutant_relax_A0_generator=True)
            if canon != mutant:
                mismatch_cases += 1
    return {
        "mutation":"disable_option_alpha_and_relax_A0_branch_in_real_generator",
        "cases":total_cases,
        "detected_mismatch_cases":mismatch_cases,
        "pass":mismatch_cases > 0,
    }

def g10_full_model_sensitivity():
    """Full-model sensitivity for G10: vary P2 tau while holding all other toy inputs fixed."""
    p=PROCESSES[1]
    original=p["tau"]
    rows=[]
    try:
        for tau in [0.50,0.60,0.70]:
            p["tau"]=tau
            best_l2_cached.cache_clear()
            r=solve("F",5)
            rows.append({
                "tau_P2":tau,
                "score_P2":p["score"],
                "truth_P2":p["truth"],
                "F1":round(r["F1"],6),
                "F2":round(r["F2"],6),
                "P2_configuration":r["l2"]["opts"][1]["l3"]["q"],
                "P2_AI_recommended_decision":r["l2"]["opts"][1]["l3"]["decision"],
                "P2_adopted_decision":(
                    None if r["l2"]["opts"][1]["l3"]["q"]=="HumanOnly"
                    else r["l2"]["opts"][1]["l3"]["decision"]
                ),
                "P2_reported_psi":(
                    None if r["l2"]["opts"][1]["l3"]["q"]=="HumanOnly"
                    else round(r["l2"]["opts"][1]["l3"]["psi"],6)
                ),
                "P2_local_utility":round(r["l2"]["opts"][1]["l3"]["utility"],6),
            })
    finally:
        p["tau"]=original
        best_l2_cached.cache_clear()
    return rows

def governance_permission_probe():
    """Full-solve permission probe.
    Baseline permissions remain all True; this temporarily forbids C/AIAssist,
    clears the Level-2 cache, solves B=5, then restores the matrix.
    """
    original = ALLOW_CONFIG["C"]["AIAssist"]
    try:
        baseline = solve("C",5)
        ALLOW_CONFIG["C"]["AIAssist"] = False
        best_l2_cached.cache_clear()
        restricted = solve("C",5)
        return {
            "scenario":"C,B=5",
            "baseline_F1":round(baseline["F1"],6),
            "restricted_F1":round(restricted["F1"],6),
            "baseline_configs":[o["l3"]["q"] for o in baseline["l2"]["opts"]],
            "restricted_configs":[o["l3"]["q"] for o in restricted["l2"]["opts"]],
            "permission_path_operates":round(baseline["F1"],12) != round(restricted["F1"],12)
                or [o["l3"]["q"] for o in baseline["l2"]["opts"]]
                != [o["l3"]["q"] for o in restricted["l2"]["opts"]],
        }
    finally:
        ALLOW_CONFIG["C"]["AIAssist"] = original
        best_l2_cached.cache_clear()

if __name__=="__main__":
    t0=time.time()
    # Canonical nine baseline scenarios.
    baseline=[]
    for B in [3,5,7]:
        for g in ["C","F","D"]:
            baseline.append(public_result(solve(g,B)))

    out={
        "model":"AI × Decision × MLP Mathematical Feasibility Prototype v1.0",
        "warning":"ALL NUMERIC VALUES ARE SIMULATED; NO PRIVILEGED INTERNAL JPC DATA USED.",
        "claim_scope":"v1.0 mathematical freeze: exact only over the bounded finite Option-alpha prototype domain under fixed tie-breaking selections; not a tractability claim for arbitrary continuous/nonconvex tri-level programs.",
        "robust_depletion_definition":"A robust depletion is a document-level AI-family x Decision-family cell whose observed edge count is significantly below the specified null expectation (BH q<=0.05) and directionally consistent in all four V5 analyses. It describes literature structure conditional on the observed marginal structure; it is not a field-wide absence claim and not an enterprise practical-problem claim.",
        "priority_gaps_freeze_note":"O_E_Ratio uses the analytic expectation E=k_a*k_d/M (M=2180), not Null_Mean. Null_Mean is the mean of 10,000 fixed-degree null replicates. The v1.0 validation pack includes all four manuscript q-value columns and direction indicators for G01-G16.",
        "tie_breaking_T3_order":["HumanOnly","AIAssist","HumanFirstAICheck","AIFirstReview","BoundedAutomation"],
        "conformance_common_mode_caveat":"The generator-vs-canonical test shares D_req/R_req/H_req/EA_req/WI_req implementations between oracle and generator. It detects generator-domain regressions but cannot by itself detect a common-mode defect in those threshold functions.",
        "option_alpha_note":"On ordinal L={0,1,2,3}, H<=3A, EA<=3A, WI<=3A bind only at A=0.",
        "toy_resource_unit_cost_c_ir":TOY_RESOURCE_UNIT_COST,
        "incorrect_decision_factor":INCORRECT_DECISION_FACTOR,
        "g10_modeling_disclosure":"Single fixed score/truth realization per selection process. s_i and truth_i are known to all three toy levels when they optimise. tau acts as a step at s_i. Oversight/assurance and review configurations reduce risk or change utility but do not correct a wrong AI recommendation. In the tau_P2=0.70 probe, Level 1 sets P2 b_A=0, so Abar_P2=0 and Level 2 must choose A=0. At a fixed Level-2 state (1,1,1,1), the Level-3 follower would still prefer AIAssist. This is a perfect-information sensitivity toy, not an ex-ante uncertainty/error-rate model.",
        "proof_checks":structural_proof_checks(),
        "generator_vs_canonical_domain_check":generator_vs_canonical_domain_check(),
        "mutation_sensitivity_check":mutation_sensitivity_check(),
        "governance_permission_probe":governance_permission_probe(),
        "g10_full_model_sensitivity":g10_full_model_sensitivity(),
        "activity_notes":{
            "G05":"Allocation task-class slice is not instantiated by the three-process v1.0 toy.",
            "G03":"The execution-specific A=3 WI floor is not reached in the nine baseline runs.",
            "G07":"Reliance/override is embedded in configuration utility and is not separately identified in v1.0.",
            "G16":"BASELINE_BRIDGE: bridge evidence for the bounded-automation compatibility row; not a duplicate hard constraint.",
            "G02_G08":"The u-indexed oversight slices are structurally distinct but numerically identical in v1.0 because all mode adjustments are 0.",
            "G05_G13":"The t-indexed assurance slices are structurally distinct but numerically identical in v1.0 because all task adjustments are 0.",
        },
        "depletion_roles":{
            "baseline":["G01","G02","G03","G05","G06","G07","G08","G09","G10","G13","G14","G15"],
            "baseline_bridge":["G16"],
            "static_baseline_role_count":13,
            "dynamic_extension":["G11","G12"],
            "temporal_monitor":["G04"],
        },
        "results":baseline,
        "runtime_seconds":round(time.time()-t0,4),
    }
    print(json.dumps(out,ensure_ascii=False,indent=2))
