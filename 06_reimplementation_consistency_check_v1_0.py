
import json, itertools, math
from pathlib import Path

# Re-implementation consistency check for canonical v1.0 Option-alpha domain.
# It intentionally re-implements the prototype equations instead of importing solver functions.

PROCESSES = [
    {"id":"P1","risk":1,"D0":1,"R0":1,"A0":0,"G0":1,"value":1.0,"selection":False,"execution":False,"tau":0.40,"score":None,"truth":None,"use_mode":"prediction","task_class":"prediction"},
    {"id":"P2","risk":2,"D0":1,"R0":1,"A0":0,"G0":1,"value":1.2,"selection":True,"execution":False,"tau":0.60,"score":0.65,"truth":1,"use_mode":"recommendation","task_class":"selection"},
    {"id":"P3","risk":3,"D0":2,"R0":2,"A0":0,"G0":1,"value":1.5,"selection":True,"execution":True,"tau":0.70,"score":0.72,"truth":1,"use_mode":"execution","task_class":"execution"},
]
GOV = {
    "C":{"K":5.5,"risk_mult":0.85,"cost_mult":1.10,"flex_mult":0.95},
    "F":{"K":6.0,"risk_mult":1.00,"cost_mult":1.00,"flex_mult":1.00},
    "D":{"K":6.5,"risk_mult":1.15,"cost_mult":0.90,"flex_mult":1.05},
}
ORDER = ["HumanOnly","AIAssist","HumanFirstAICheck","AIFirstReview","BoundedAutomation"]
RANK = {x:i for i,x in enumerate(ORDER)}
ALLOW={g:{m:True for m in ORDER} for g in ["C","F","D"]}
Q = {
    "HumanOnly":{"A":0,"H":0,"WI":0,"EA":0,"gain":[0.0,0.0,0.0],"burden":0.0,"autonomy":0.0},
    "AIAssist":{"A":1,"H":0,"WI":1,"EA":1,"gain":[0.80,0.60,0.40],"burden":0.15,"autonomy":0.20},
    "AIFirstReview":{"A":2,"H":2,"WI":2,"EA":2,"gain":[0.65,0.90,0.70],"burden":0.25,"autonomy":0.50},
    "HumanFirstAICheck":{"A":2,"H":1,"WI":2,"EA":1,"gain":[0.75,1.00,0.80],"burden":0.30,"autonomy":0.40},
    "BoundedAutomation":{"A":3,"H":3,"WI":3,"EA":3,"gain":[0.40,0.70,1.20],"burden":0.10,"autonomy":1.00},
}

def Dreq(A): return A
def Rreq(A): return A
def Hreq(A,k,use_mode):
    if A==0: return 0
    adj={"prediction":0,"recommendation":0,"execution":0}[use_mode]
    return min(3,max(0,A+k-2+adj))
def Ereq(A,k,task_class):
    if A==0: return 0
    adj={"prediction":0,"selection":0,"allocation":0,"execution":0}[task_class]
    return min(3,max(1,A+k-2+adj))
def Wreq(A,k,execution): return 0 if A==0 else (3 if execution and A==3 else A)
TOY_RESOURCE_UNIT_COST=1.0
INCORRECT_DECISION_FACTOR=0.35

def clamp(x): return max(0.0,min(1.0,x))

def decision_factor(p):
    if not p["selection"]:
        return None,1.0
    d=int(p["score"]>=p["tau"])
    return d,(1.0 if d==int(p["truth"]) else INCORRECT_DECISION_FACTOR)

def l3(proc_idx,A,H,W,E,gname):
    p=PROCESSES[proc_idx]
    g=GOV[gname]
    cand=[]
    for name,d in Q.items():
        if not ALLOW[gname][name]:
            continue
        if A<d["A"] or H<d["H"] or W<d["WI"] or E<d["EA"]:
            continue
        decision,factor=decision_factor(p)
        psi=max(0.0,(1+.05*E+.03*W)*factor)
        gain=d["gain"][proc_idx]*p["value"]*psi*g["flex_mult"]
        risk=p["risk"]*d["autonomy"]*g["risk_mult"]/(1+.45*H+.45*E)
        burden=d["burden"]+.03*H+.02*E+.02*W
        util=gain-.45*burden-.75*risk
        key=(round(util,12),-round(burden,12),-round(risk,12),-RANK[name])
        cand.append((key,{"q":name,"decision":decision,"psi":psi,"utility":util,"gain":gain,"risk":risk,"burden":burden}))
    assert cand
    return max(cand,key=lambda x:x[0])[1]

def process_options(idx,caps,gname):
    g=GOV[gname]
    Dcap,Acap,Rcap,Gcap=caps
    p=PROCESSES[idx]
    out=[]
    for A in range(Acap+1):
        if Dcap<Dreq(A) or Rcap<Rreq(A): continue
        if A==0:
            Hs=Es=Ws=[0]
        else:
            h0,e0,w0=Hreq(A,p["risk"],p["use_mode"]),Ereq(A,p["risk"],p["task_class"]),Wreq(A,p["risk"],p["execution"])
            if h0>Gcap or e0>Gcap or w0>Dcap: continue
            Hs=range(h0,Gcap+1); Es=range(e0,Gcap+1); Ws=range(w0,Dcap+1)
        for H in Hs:
            for E in Es:
                for W in Ws:
                    if H>3*A or E>3*A or W>3*A:
                        continue
                    cap=.42*A+.24*H+.24*E+.20*W
                    feas=clamp(.55+.08*(Dcap-Dreq(A))+.08*(Rcap-Rreq(A))+.04*(Gcap-max(Hreq(A,p["risk"],p["use_mode"]),Ereq(A,p["risk"],p["task_class"]))))
                    rel=clamp(.45+.10*E+.06*H+.04*W-.030*A*p["risk"])
                    scale=clamp(.30+.08*Dcap+.08*Rcap+.04*W)
                    icost=g["cost_mult"]*(.10*A+.06*W+.05*H+.05*E)
                    grisk=g["risk_mult"]*(0 if A==0 else .08*p["risk"]*A/(1+.4*H+.4*E))
                    br=l3(idx,A,H,W,E,gname)
                    f2=.90*feas+.90*rel+.45*scale-.55*icost-.75*grisk+.65*max(0,br["utility"])
                    out.append(dict(A=A,H=H,WI=W,EA=E,capuse=cap,feas=feas,rel=rel,scale=scale,icost=icost,grisk=grisk,l3=br,f2=f2))
    return out

CACHE={}
def best_l2(gname,caps12):
    key=(gname,tuple(caps12))
    if key in CACHE:return CACHE[key]
    g=GOV[gname]
    lists=[process_options(i,caps12[4*i:4*i+4],gname) for i in range(3)]
    best=None; bestk=None
    for combo in itertools.product(*lists):
        cap=sum(o["capuse"] for o in combo)
        if cap>g["K"]+1e-9: continue
        f2=sum(o["f2"] for o in combo)
        gr=sum(o["grisk"] for o in combo)
        arch=tuple((o["A"],o["H"],o["WI"],o["EA"],RANK[o["l3"]["q"]]) for o in combo)
        k=(round(f2,12),-round(cap,12),-round(gr,12),tuple(-v for item in arch for v in item))
        if best is None or k>bestk:
            bestk=k; best={"opts":combo,"F2":f2,"capuse":cap}
    assert best is not None
    CACHE[key]=best
    return best

def allocations(B):
    # Efficient bounded compositions: every vector in {0,1,2,3}^12 with sum <= B.
    def rec(pos, remaining, prefix):
        if pos == 12:
            yield tuple(prefix)
            return
        for v in range(min(3, remaining) + 1):
            prefix.append(v)
            yield from rec(pos + 1, remaining - v, prefix)
            prefix.pop()
    for total in range(B + 1):
        # exact-total generator to avoid duplicates
        def rec_exact(pos, rem, prefix):
            if pos == 12:
                if rem == 0:
                    yield tuple(prefix)
                return
            for v in range(min(3, rem) + 1):
                prefix.append(v)
                yield from rec_exact(pos + 1, rem - v, prefix)
                prefix.pop()
        yield from rec_exact(0, total, [])

def caps(alloc):
    out=[]
    for i,p in enumerate(PROCESSES):
        bD,bA,bR,bG=alloc[4*i:4*i+4]
        out += [min(3,p["D0"]+bD),min(3,p["A0"]+bA),min(3,p["R0"]+bR),min(3,p["G0"]+bG)]
    return tuple(out)

def leader_eval(alloc,l2):
    value=sum(max(0,o["l3"]["gain"]) for o in l2["opts"])
    risk=sum(o["l3"]["risk"] for o in l2["opts"])
    ad=sum(o["l3"]["q"]!="HumanOnly" for o in l2["opts"])
    f1=1.25*value+.20*ad-.22*(TOY_RESOURCE_UNIT_COST*sum(alloc))-.75*risk
    return f1,value,risk,ad

def solve(gname,B):
    best=None; bestk=None
    for a in allocations(B):
        c=caps(a)
        l2=best_l2(gname,c)
        f1,val,risk,ad=leader_eval(a,l2)
        k=(round(f1,12),-sum(a),-round(risk,12),tuple(-x for x in a))
        if best is None or k>bestk:
            bestk=k
            best={"governance":gname,"budget":B,"F1":f1,"F2":l2["F2"],"alloc":a,"caps":c,
                  "value":val,"risk":risk,"adoptions":ad,"opts":l2["opts"]}
    return best

def compare(a,b,tol=1e-6):
    return abs(a-b)<=tol

official=json.loads(Path(__file__).with_name("05_solver_results_v1_0.json").read_text(encoding="utf-8"))
off={(r["budget"],r["governance"]):r for r in official["results"]}

checks=[]
reproduced=[]
for B in [3,5,7]:
    for g in ["C","F","D"]:
        r=solve(g,B); o=off[(B,g)]
        per_process=[]
        for idx,x in enumerate(r["opts"]):
            op=o["processes"][idx]
            qn=x["l3"]["q"]
            adopted = None if qn=="HumanOnly" else x["l3"]["decision"]
            reported_psi = None if qn=="HumanOnly" else round(x["l3"]["psi"],6)
            pp={
                "process":PROCESSES[idx]["id"],
                "A_match":x["A"]==op["A"],
                "H_match":x["H"]==op["H"],
                "WI_match":x["WI"]==op["WI"],
                "EA_match":x["EA"]==op["EA"],
                "configuration_match":qn==op["configuration"],
                "AI_recommended_decision_match":x["l3"]["decision"]==op["AI_recommended_decision"],
                "adopted_decision_match":adopted==op["adopted_decision"],
                "reported_psi_match":reported_psi==op["reported_psi"],
                "local_utility_match":compare(x["l3"]["utility"],op["local_utility"]),
            }
            pp["pass"]=all(v for k,v in pp.items() if k.endswith("_match"))
            per_process.append(pp)
        row={
            "budget":B,"governance":g,
            "F1_reimpl":round(r["F1"],6),
            "F1_official":o["F1_best"],
            "F2_reimpl":round(r["F2"],6),
            "F2_official":o["F2_response"],
            "alloc_match":list(r["alloc"])==o["L1_allocation_vector"],
            "configs_reimpl":[x["l3"]["q"] for x in r["opts"]],
            "configs_official":[x["configuration"] for x in o["processes"]],
            "per_process_checks":per_process,
        }
        row["pass"]=(
            compare(r["F1"],o["F1_best"]) and compare(r["F2"],o["F2_response"]) and
            row["alloc_match"] and row["configs_reimpl"]==row["configs_official"] and
            all(pp["pass"] for pp in per_process)
        )
        checks.append(row)
        reproduced.append(r)

# Structural existence checks plus constraint validation of the 9 reproduced optima.
structural = {
    "A0_thresholds_zero": all([
        Dreq(0)==0, Rreq(0)==0,
        all(Hreq(0,k,"prediction")==0 for k in [1,2,3]),
        all(Ereq(0,k,"prediction")==0 for k in [1,2,3]),
        all(Wreq(0,k,False)==0 for k in [1,2,3]),
        all(Wreq(0,k,True)==0 for k in [1,2,3]),
    ]),
    "human_only_zero_requirements": Q["HumanOnly"]["A"]==Q["HumanOnly"]["H"]==Q["HumanOnly"]["WI"]==Q["HumanOnly"]["EA"]==0,
    "governance_capacity_nonnegative": all(v["K"]>=0 for v in GOV.values()),
    "human_only_allowed_all_governance": all(ALLOW[g]["HumanOnly"] for g in ALLOW),
    "toy_resource_cost_normalization": TOY_RESOURCE_UNIT_COST==1.0,
}

returned_constraints=[]
for r in reproduced:
    ok=True; reasons=[]
    B=r["budget"]; g=r["governance"]
    if sum(r["alloc"])>B: ok=False; reasons.append("budget")
    if sum(o["capuse"] for o in r["opts"])>GOV[g]["K"]+1e-9:
        ok=False; reasons.append("capacity")
    for idx,o in enumerate(r["opts"]):
        Dcap,Acap,Rcap,Gcap=r["caps"][4*idx:4*idx+4]
        p=PROCESSES[idx]
        if o["A"]>Acap or o["H"]>Gcap or o["EA"]>Gcap or o["WI"]>Dcap:
            ok=False; reasons.append("cap_bounds")
        if Dcap<Dreq(o["A"]) or Rcap<Rreq(o["A"]):
            ok=False; reasons.append("prereq")
        if o["H"]<Hreq(o["A"],p["risk"],p["use_mode"]) or o["EA"]<Ereq(o["A"],p["risk"],p["task_class"]) or o["WI"]<Wreq(o["A"],p["risk"],p["execution"]):
            ok=False; reasons.append("threshold")
        if o["H"]>3*o["A"] or o["EA"]>3*o["A"] or o["WI"]>3*o["A"]:
            ok=False; reasons.append("option_alpha")
        q=Q[o["l3"]["q"]]
        if not ALLOW[g][o["l3"]["q"]]:
            ok=False; reasons.append("permission")
        if o["A"]<q["A"] or o["H"]<q["H"] or o["EA"]<q["EA"] or o["WI"]<q["WI"]:
            ok=False; reasons.append("config")
    returned_constraints.append({"budget":B,"governance":g,"pass":ok,"reasons":sorted(set(reasons))})


# Generator-vs-canonical domain conformance.
def canonical_state_set(idx,caps):
    Dcap,Acap,Rcap,Gcap=caps
    p=PROCESSES[idx]
    out=set()
    for A,H,W,E in itertools.product(range(4),repeat=4):
        if A>Acap or H>Gcap or E>Gcap or W>Dcap: continue
        if Dcap<Dreq(A) or Rcap<Rreq(A): continue
        if H<Hreq(A,p["risk"],p["use_mode"]): continue
        if E<Ereq(A,p["risk"],p["task_class"]): continue
        if W<Wreq(A,p["risk"],p["execution"]): continue
        if H>3*A or E>3*A or W>3*A: continue
        out.add((A,H,W,E))
    return out

domain_mismatches=[]
canonical_count=0
cases=0
for idx in range(3):
    for caps4 in itertools.product(range(4),repeat=4):
        cases+=1
        canon=canonical_state_set(idx,caps4)
        gen={(o["A"],o["H"],o["WI"],o["EA"]) for o in process_options(idx,caps4,"F")}
        canonical_count += len(canon)
        if canon!=gen:
            domain_mismatches.append({"process":PROCESSES[idx]["id"],"caps":list(caps4),
                                      "canonical_only":[list(x) for x in sorted(canon-gen)],
                                      "generator_only":[list(x) for x in sorted(gen-canon)]})
domain_conformance=(len(domain_mismatches)==0)

output={
    "verifier":"reimplementation_consistency_check_v0_7",
    "generator_vs_canonical_domain_check":{"cases":cases,"canonical_feasible_states_counted_with_repetition":canonical_count,"pass":domain_conformance,"mismatch_cases":len(domain_mismatches)},
    "domain_mismatches": domain_mismatches,
    "official_9_scenario_reproduction":checks,
    "official_all_pass":all(x["pass"] for x in checks),
    "structural_sufficient_condition_checks":structural,
    "structural_all_pass":all(structural.values()),
    "returned_solution_constraint_checks":returned_constraints,
    "returned_solution_constraints_all_pass":all(x["pass"] for x in returned_constraints),
    "note":"Re-implementation consistency check; shares transcribed coefficients/equations with the canonical toy and is not external independent validation. v1.0 additionally compares per-process A/H/WI/EA, configuration, AI recommendation, adopted decision, reported psi, utility, and checks Option-alpha on returned optima."
}
print(json.dumps(output,ensure_ascii=False,indent=2))
