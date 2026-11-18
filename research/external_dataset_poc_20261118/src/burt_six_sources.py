#!/usr/bin/env python3
"""Six-source structural-hole falsification, explicit measurement boundaries.

DO NOT interpret projected consortium/coauthor or electrical links as observed
bilateral information flows. This computes topology diagnostics and abstains
from confirmatory Burt/MLP verdicts when construct validity is not established.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict, deque
from itertools import combinations
import json
import math
import random
from pathlib import Path
from statistics import median

def build_graph(edges):
    g=defaultdict(set)
    for e in edges:
        a,b=e[:2]
        a,b=str(a),str(b)
        if a and b and a!=b:
            g[a].add(b)
            g[b].add(a)
    return dict(g)

def project_affiliations(rows, min_shared=1, max_project_size=250, allow=None):
    """Clique projection of public project membership; explicitly not dyadic ties."""
    members=defaultdict(set)
    for item in rows:
        pid=str(item["project_id"])
        if allow is not None and pid not in allow:continue
        members[pid].add(str(item["organisation_id"]))
    counter=Counter()
    excluded=0
    for ns in members.values():
        if len(ns)>max_project_size:
            excluded+=1
            continue
        counter.update(combinations(sorted(ns),2))
    edges=[(a,b) for (a,b),n in counter.items() if n>=min_shared]
    return build_graph(edges),counter,{"projects":len(members),"excluded_oversize_projects":excluded,
         "nodes_in_edges":len({x for a,b in edges for x in (a,b)}),
         "edges":len(edges),"recurring_edges":sum(n>=2 for n in counter.values())}

def score_graph(graph):
    """Unweighted, undirected Burt constraint using p_qj=1/degree(q).
    C_i=sum_j(p_ij+sum_{q!=j}p_iq*p_qj)^2; ES=k-2t/k for simple graphs.
    No claim that this graph encodes independent social ties.
    """
    out={}
    for i,ns in graph.items():
        k=len(ns)
        if k==0:continue
        inv=1/k
        indirect=defaultdict(float)
        t_twice=0
        for q in ns:
            qns=graph[q]
            shared=ns.intersection(qns)
            t_twice+=len(shared)
            factor=inv/len(qns)
            for j in shared:
                indirect[j]+=factor
        direct=inv
        c=sum((direct+indirect[j])**2 for j in ns)
        indirect_extra=c-direct
        out[i]={"degree":k,"constraint":c,"dyadic_hhi":direct,
                "indirect_excess":indirect_extra,
                "effective_size":k-t_twice/k,
                "efficiency":1-t_twice/(k*k),
                "triangles_local":t_twice//2}
    return out

def fdr_bh(pvalues):
    n=len(pvalues)
    ordering=sorted(range(n),key=lambda i:pvalues[i])
    q=[1.0]*n
    best=1.0
    for rank0 in range(n-1,-1,-1):
        idx=ordering[rank0]
        best=min(best,pvalues[idx]*n/(rank0+1))
        q[idx]=best
    return q

def describe(values):
    values=[v for v in values if v is not None and math.isfinite(v)]
    if not values:return {"n":0}
    return {"n":len(values),"min":min(values),"median":median(values),
            "max":max(values),"mean":sum(values)/len(values)}

def betweenness_landmarks(g, n_sources=24, seed=1118):
    """Unweighted sampled Brandes; exploratory ranks only, NOT exact centrality."""
    rng=random.Random(seed)
    nodes=sorted(g)
    starts=rng.sample(nodes,min(len(nodes),n_sources))
    bt=defaultdict(float)
    for s in starts:
        stack=[]
        preds=defaultdict(list)
        sig=defaultdict(float); sig[s]=1.
        dist={s:0}
        q=deque([s])
        while q:
            v=q.popleft()
            stack.append(v)
            for w in g[v]:
                if w not in dist:
                    dist[w]=dist[v]+1
                    q.append(w)
                if dist[w]==dist[v]+1:
                    sig[w]+=sig[v]
                    preds[w].append(v)
        delta=defaultdict(float)
        while stack:
            w=stack.pop()
            if sig[w]:
                for v in preds[w]:
                    delta[v]+=sig[v]/sig[w]*(1+delta[w])
            if w!=s:bt[w]+=delta[w]
    return {"sampled_sources":len(starts),"scores":bt,
            "scope":"UNNORMALIZED_SAMPLED_BRANDES_NOT_EXACT_BETWEENNESS"}

def retained_alter_reachability(g, ego):
    """Check alter reachability after removing ego; NOT a sufficient Burt test."""
    ns=g.get(ego,set())
    if len(ns)<2:return {"alter_pairs":0,"reachable_fraction":None}
    assigned={}
    for u in ns:
        if u in assigned:continue
        queue=deque([u])
        assigned[u]=u
        while queue:
            a=queue.popleft()
            for b in g.get(a,set()):
                if b!=ego and b not in assigned:
                    assigned[b]=u; queue.append(b)
    groups=Counter(assigned[u] for u in ns)
    n=len(ns)
    pairs=n*(n-1)//2
    connected=sum(k*(k-1)//2 for k in groups.values())
    return {"alter_pairs":pairs,"reachable_fraction":connected/pairs,
            "scope":"REACHABILITY_AFTER_EGO_REMOVAL_NOT_BURT_EQUIVALENT"}

def top_candidates(scores, membership_counts=None, limit=12):
    membership_counts=membership_counts or {}
    elig=[(n,x) for n,x in scores.items() if x["degree"]>=3 and
          membership_counts.get(n,2)>=2]
    return sorted(elig,key=lambda nx:(nx[1]["constraint"],-nx[1]["degree"],nx[0]))[:limit]

def shuffled_affiliation(rows, rng, swaps=3500):
    """Exact project size and org participation degree are preserved via edge swaps."""
    edges=list({(str(r["project_id"]),str(r["organisation_id"])) for r in rows})
    occupied=set(edges)
    if len(edges)<2:return [{"project_id":p,"organisation_id":o} for p,o in edges],0
    accepted=0
    for _ in range(swaps):
        i,j=rng.sample(range(len(edges)),2)
        p,o=edges[i]
        q,t=edges[j]
        if p==q or o==t or (p,t) in occupied or (q,o) in occupied:continue
        occupied.remove((p,o));occupied.remove((q,t))
        edges[i]=(p,t);edges[j]=(q,o)
        occupied.add((p,t));occupied.add((q,o))
        accepted+=1
    return [{"project_id":p,"organisation_id":o} for p,o in edges],accepted

def null_degree_preserving(rows, target_nodes, observed, reps=49, seed=20261118):
    """Bipartite edge-swap null; descriptive, no temporal/identity conditioning.
    Compare constraint for each target while checking projected degree drift.
    """
    rng=random.Random(seed)
    keep={n:{"obs":observed[n]["constraint"],"obs_degree":observed[n]["degree"],
             "values":[],"degrees":[]} for n in target_nodes}
    accept=[]
    for k in range(reps):
        shuffled,accepted=shuffled_affiliation(rows,rng,swaps=max(3500,3*len(rows)))
        accept.append(accepted)
        graph,_,_=project_affiliations(shuffled)
        null_scores=score_graph(graph)
        for n,record in keep.items():
            v=null_scores.get(n)
            if v:
                record["values"].append(v["constraint"])
                record["degrees"].append(v["degree"])
    entries=[]
    for n,record in keep.items():
        vals=record["values"]
        degs=record["degrees"]
        valid=[x for x,d in zip(vals,degs) if abs(d-record["obs_degree"])<=max(1,round(.2*record["obs_degree"]))]
        # With fewer than 20 comparable replications we abstain from q claims.
        p=(1+sum(x<=record["obs"] for x in valid))/(1+len(valid)) if valid else None
        entries.append({"node":n,"observed_constraint":record["obs"],
                        "observed_projected_degree":record["obs_degree"],
                        "valid_degree_matched_nulls":len(valid),
                        "null_total":len(vals),"null_degree_median":median(degs) if degs else None,
                        "null_constraint_median_degree_matched":median(valid) if valid else None,
                        "empirical_lower_tail_p":p if len(valid)>=20 else None})
    selected=[x for x in entries if x["empirical_lower_tail_p"] is not None]
    q=fdr_bh([x["empirical_lower_tail_p"] for x in selected])
    for x,v in zip(selected,q):x["bh_q"]=v
    for x in entries:
        if "bh_q" not in x:x["bh_q"]=None
    return {"reps":reps,"swap_accepted":describe(accept),
            "tested":entries,"bh_q_below_point05":sum(x["bh_q"] is not None and x["bh_q"]<.05 for x in entries),
            "caveat":"Post-selected top candidates; p-values exploratory only; degree-tolerance conditioning and 49 permutations have weak power, no confirmatory inference."}

def digest_graph(label,graph, membership=None, sample_betweenness=True):
    scores=score_graph(graph)
    top=top_candidates(scores,membership)
    b=betweenness_landmarks(graph) if sample_betweenness else {"sampled_sources":0,"scores":{}}
    return {"label":label,"nodes":len(graph),"edges":sum(len(x) for x in graph.values())//2,
            "degree":describe([x["degree"] for x in scores.values()]),
            "constraint":describe([x["constraint"] for x in scores.values()]),
            "dyadic_hhi":describe([x["dyadic_hhi"] for x in scores.values()]),
            "indirect_excess":describe([x["indirect_excess"] for x in scores.values()]),
            "effective_size":describe([x["effective_size"] for x in scores.values()]),
            "triangles_local_sum_over_three":sum(x["triangles_local"] for x in scores.values())//3,
            "n_with_indirect_excess":sum(x["indirect_excess"]>1e-10 for x in scores.values()),
            "betweenness_approx_sources":b["sampled_sources"],
            "top_low_constraint_candidates":[{"node":n,**x,
              "project_count":membership.get(n) if membership else None,
              "sampled_betweenness":b["scores"].get(n,0),
              "ego_removed":retained_alter_reachability(graph,n)} for n,x in top]}

def cordis_round(live,reps=49):
    p=live.get("cordis_bulk_profile") or {}
    e=(p.get("exploratory_ai_decision") or {})
    rows=e.get("derived_affiliations") or []
    alt=e.get("alternate_affiliations") or []
    membership=Counter(r["organisation_id"] for r in rows)
    g,pairs,meta=project_affiliations(rows)
    obs=score_graph(g)
    top=top_candidates(obs,membership)
    ids=[n for n,_ in top]
    other_g,other_pairs,other_meta=project_affiliations(rows,min_shared=2)
    altg,_,altmeta=project_affiliations(alt)
    smallg,_,smallmeta=project_affiliations(rows,max_project_size=20)
    projects=e.get("selected_project_metadata") or {}
    early={pid for pid,info in projects.items() if str(info.get("startDate") or "")[:4]<="2017"}
    late={pid for pid,info in projects.items() if str(info.get("startDate") or "")[:4]>="2018"}
    earlyg,_,_=project_affiliations(rows,allow=early)
    lateg,_,_=project_affiliations(rows,allow=late)
    base_top=set(ids)
    variants={}
    for label,gx,mx in (("two_or_more_common_projects",other_g,other_meta),
                         ("max_project_size_20",smallg,smallmeta),
                         ("with_topics_keywords",altg,altmeta),
                         ("early_2014_2017",earlyg,{}),
                         ("late_2018_2020",lateg,{})):
        vsc=score_graph(gx)
        ranked={n for n,x in top_candidates(vsc,membership)}
        variants[label]={"nodes":len(gx),"edges":sum(len(v) for v in gx.values())//2,
                          "candidate_overlap_with_baseline_top12":len(base_top & ranked),
                          "candidate_count":len(ranked)}
    null=null_degree_preserving(rows,ids,obs,reps=reps) if ids and reps else {"reps":0,"tested":[]}
    two_mode_degrees=Counter()
    for r in rows:two_mode_degrees[str(r["organisation_id"])]+=1
    return {"source":"CORDIS_H2020","status":"EXPLORATORY_REAL_AFFILIATION_ONLY",
        "selection":"195 projects from unvalidated title+objective keyword selection; alternative 233 projects including topics/keywords",
        "two_mode":{"project_org_edges":len(rows),"unique_orgs":len(two_mode_degrees),
          "organisation_degree":describe(list(two_mode_degrees.values())),
          "triangles_in_bipartite":0,
          "uniform_strict_bipartite_constraint":"1/k (indirect terms 0), cannot establish Burt brokerage"},
        "one_mode_projection":digest_graph("consortium_co_membership_projection",g,membership),
        "projection_metadata":meta,
        "degree_preserving_null":null,
        "sensitivity":variants,
        "publication_linkage":"NO_CONFIRMED_INDEPENDENT_OUTCOME_OR_EXTERNAL_BILATERAL_TIES",
        "verdict":"NO_CONFIRMED_BURT_BROKER_ONLY_PROJECTION_DIAGNOSTICS"}

def paper_memberships(works,key):
    return [{"project_id":w.get("work_id"),"organisation_id":id_}
            for w in works if w.get("work_id") for id_ in w.get(key,[]) if id_]

def other_sources_round(live):
    src=live.get("source_status") or {}
    alex=(src.get("OpenAlex",{}).get("parsed") or {})
    works=alex.get("work_memberships") or []
    result={"OpenAlex":{"source_count_works":len(works),
                         "status":"LOW_POWER_PUBLIC_API_SAMPLE",
                         "author_graph":None,"institution_graph":None,
                         "verdict":"UNCONFIRMED_IDENTITY_AND_OUTCOME"}}
    if works:
        for field,which in (("authors","author_graph"),("institutions","institution_graph")):
            rows=paper_memberships(works,field)
            graph,_,_=project_affiliations(rows)
            result["OpenAlex"][which]=digest_graph("shared_paper_"+field,graph,sample_betweenness=False)
    uk=src.get("OCDS_REAL_UK",{}).get("parsed") or {}
    # An unconnected single buyer does not establish a brokerage network.
    edge_pairs=uk.get("real_buyer_supplier_edges") or []
    result["OCDS"]={"real_notices":uk.get("releases_in_package"),"buyer_supplier_edges":len(edge_pairs),
                    "schema_fictional_excluded":True,
                    "status":"ONLY_BOUNDED_UK_REAL_NOTICE","verdict":"NO_IDENTIFIABLE_BROKERAGE_NETWORK",
                    "note":"Repeated buyer-supplier contracting and actual bids would be required; 1 notice is not population."}
    gleif=src.get("GLEIF",{}).get("parsed") or {}
    result["GLEIF"]={"sample_records":1 if gleif.get("lei") else 0,
                     "verified_parent_edges":0,"status":"LEI_PARENT_RELATION_NOT_VERIFIED",
                     "verdict":"NOT_IDENTIFIABLE"}
    result["SEC"]={"status":"NOT_FETCHED_VALID_CONTACT_REQUIRED",
                   "relational_edges":0,"verdict":"NOT_APPLICABLE_FINANCIAL_FACTS_NOT_SOCIAL_NETWORK"}
    grid=live.get("grid_stats") or {}
    edge_rows=grid.get("derived_edges") or []
    pgraph=build_graph([(x["u"],x["v"]) for x in edge_rows])
    result["PyPSA_Eur"]={"status":"REAL_UNOFFICIAL_PHYSICAL_TOPOLOGY",
            "data_rows":grid.get("rows"),
            "network":digest_graph("physical_gridkit",pgraph) if edge_rows else None,
            "verdict":"DIAGNOSTICS_ONLY_NOT_SOCIAL_BURT",
            "warning":"GridKit March 2022 physical AC/DC/transformer map is NOT evidence of scholarly/organizational ties."}
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--input",required=True)
    parser.add_argument("--output",required=True)
    parser.add_argument("--null-reps",type=int,default=49)
    args=parser.parse_args()
    if not 0<=args.null_reps<=199:parser.error("null-reps must be between 0 and 199")
    live=json.loads(Path(args.input).read_text(encoding="utf8"))
    out={"schema":"ai-decision-six-source-burt/1.0",
         "evidence":"SOURCE_DERIVED_EXPLORATORY_NOT_HYPOTHESIS_CONFIRMATION",
         "sources":other_sources_round(live),
         "CORDIS":cordis_round(live,reps=args.null_reps),
         "frozen_V9_and_V11_1_not_modified":True,
         "confirmed_brokers_across_six_sources":None,
         "conclusion":"NO_SOURCE_PASSES_INDEPENDENT_RELATIONAL_AND_VALIDATION_GATES",
         "method_crosswalk":{"M13":"author/organisation candidate graph",
           "M15":"no independent peer verification",
           "M16":"dyadic vs indirect decomposition",
           "M17":"ego removal alternative reachability (NOT a Burt sufficiency test)",
           "M18":"backbone/project size/temporal selection sensitivity",
           "M19":"bipartite degree-preserving swap null"},
         "not_transferable":{"M01-M07":"semantic-coded 10x12 function matrix; no common 120-cell hypothesis family",
            "M20":"limitation keyword evidence not included in organizational network",
            "confirmed_significance":"no preregistered empirical ties, outcome or independent peer checks"}}
    outpath=Path(args.output)
    outpath.parent.mkdir(exist_ok=True,parents=True)
    outpath.write_text(json.dumps(out,ensure_ascii=False,indent=2,default=list)+"\n",encoding="utf8")
    print(json.dumps({"output":str(outpath),"CORDIS_candidates":len(out["CORDIS"]["one_mode_projection"]["top_low_constraint_candidates"]),
     "source_verdicts":{k:v["verdict"] for k,v in out["sources"].items()},
     "result":out["conclusion"]},ensure_ascii=False))
if __name__=="__main__":main()
