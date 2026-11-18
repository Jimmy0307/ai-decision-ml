#!/usr/bin/env python3
"""Six-source two-mode, one-mode, typed/multilayer Burt diagnostics.

All analyses respect source edge semantics. No source is claimed to evidence
actual information brokerage merely because topological constraint is small.
The 10x12 V9 null models cannot be silently transferred to different units.
"""
import argparse
from collections import Counter, defaultdict, deque
from itertools import combinations
import json
import math
from pathlib import Path
from statistics import median
from burt_six_sources import build_graph, score_graph, describe, project_affiliations

def sgraph_stats(g,top=6):
    s=score_graph(g)
    return {"nodes":len(g),"edges":sum(map(len,g.values()))//2,
            "degree":describe([v["degree"] for v in s.values()]),
            "constraint":describe([v["constraint"] for v in s.values()]),
            "effective_size":describe([v["effective_size"] for v in s.values()]),
            "indirect_term_nonzero":sum(v["indirect_excess"]>1e-10 for v in s.values()),
            "low_constraint_examples":[{"node":u,"degree":x["degree"],
                "constraint":round(x["constraint"],6),"effective_size":round(x["effective_size"],5)}
                for u,x in sorted(s.items(),key=lambda item:(item[1]["constraint"],item[0]))[:top]],
            "status":"TOPOLOGICAL_DIAGNOSTIC_NOT_CONFIRMATORY"}

def two_mode(rows,left,right,left_prefix="P:",right_prefix="O:"):
    links={(str(item[left]),str(item[right])) for item in rows
            if item.get(left) and item.get(right)}
    g=build_graph([(left_prefix+a,right_prefix+b) for a,b in links])
    scores=score_graph(g)
    side_a=[x for x in scores if x.startswith(left_prefix)]
    side_b=[x for x in scores if x.startswith(right_prefix)]
    return {"original_rows":len(rows),"unique_affiliation_edges":len(links),
       "left_nodes":len(side_a),"right_nodes":len(side_b),
       "strict_bipartite_indirect_term_nonzero":sum(x["indirect_excess"]>1e-10 for x in scores.values()),
       "constraint_left":describe([scores[x]["constraint"] for x in side_a]),
       "constraint_right":describe([scores[x]["constraint"] for x in side_b]),
       "interpretation":"For simple strict bipartite graph, indirect term zero and C_i=1/k_i. This cannot identify nonredundant same-side ego contacts."}

def weighted_constraint(counter):
    """Burt's normalized network constraint on weighted undirected ties.

    Tie weight = count of distinct shared consortium projects (not observed
    communication). Uses degree-normalized edge strengths, not Euclidean norm.
    """
    weighted=defaultdict(dict)
    for (a,b),weight in counter.items():
        if weight>0 and a!=b:
            weighted[a][b]=float(weight)
            weighted[b][a]=float(weight)
    totals={a:sum(ns.values()) for a,ns in weighted.items()}
    out={}
    for a,ns in weighted.items():
        t=totals[a]
        val=0.0
        for b,wab in ns.items():
            p=wab/t
            indirect=sum(wq/t * weighted[q].get(b,0.)/totals[q]
                         for q,wq in ns.items() if q!=b and totals[q]>0)
            val+=(p+indirect)**2
        out[a]=val
    return out

def undirected_layers(layers, top=6):
    """Within-source typed layers; do not merge nodes across unrelated sources."""
    edges_by_type={}
    for name,edges in layers.items():
        edge_set={tuple(sorted((str(a),str(b)))) for a,b in edges if str(a)!=str(b)}
        edges_by_type[name]=edge_set
    active={k:v for k,v in edges_by_type.items() if v}
    union=set().union(*active.values()) if active else set()
    both={}
    names=sorted(active)
    for i,a in enumerate(names):
        for b in names[i+1:]:
            common=len(active[a]&active[b])
            total=len(active[a]|active[b])
            both[a+"__"+b]={"overlapping_edges":common,
                            "jaccard":common/total if total else None}
    counts=Counter(e for es in active.values() for e in es)
    return {"layers":{k:{"distinct_edges":len(v),
                   "stats":sgraph_stats(build_graph(v),top=top)} for k,v in edges_by_type.items()},
            "union":sgraph_stats(build_graph(union),top=top),
            "edge_overlap":both,
            "shared_edges_across_layers":sum(v>1 for v in counts.values()),
            "disclaimer":"Layers must share node identity AND edge semantic for cross-layer brokerage. Intersection alone is not evidence of mediation."}

def right_projection_from_affiliations(rows):
    """Project/project projection through common organizations (reverse one-mode)."""
    entities=defaultdict(set)
    for row in rows:
        a=row.get("project_id")
        b=row.get("organisation_id")
        if a and b:
            entities[str(b)].add(str(a))
    shared=Counter()
    for pids in entities.values():
        shared.update(combinations(sorted(pids),2))
    return build_graph(shared.keys()),shared

def higher_order_affiliation(rows):
    """Summarize native project hyperedges without equating co-membership to ties."""
    members=defaultdict(set)
    for row in rows:
        pid=row.get("project_id");oid=row.get("organisation_id")
        if pid and oid:members[str(pid)].add(str(oid))
    sizes=[len(v) for v in members.values()]
    triangles_created_by_clique_projection=sum(math.comb(k,3) for k in sizes if k>=3)
    return {"projects":len(members),
            "project_size":describe(sizes),
            "projects_2plus_members":sum(k>=2 for k in sizes),
            "projects_3plus_members":sum(k>=3 for k in sizes),
            "projects_4plus_members":sum(k>=4 for k in sizes),
            "within_project_triads_created_in_projection_counting_repeat_triples":triangles_created_by_clique_projection,
            "scope":"HYPEREDGE_MEMBERSHIP_COUNTS_NOT_OBSERVED_TRIADIC_INFORMATION_FLOWS"}

def cordis(live):
    p=(live.get("cordis_bulk_profile") or {}).get("exploratory_ai_decision") or {}
    aff=p.get("derived_affiliations") or []
    alt=p.get("alternate_affiliations") or []
    meta=p.get("selected_project_metadata") or {}
    type_rows=defaultdict(list)
    for item in p.get("derived_allocations") or []:
        role=(item.get("role") or "").lower()
        type_rows["coordinator" if "coordinator" in role else "non_coordinator"].append(item)
    g,edges,profile=project_affiliations(aff)
    project_graph,project_shared=right_projection_from_affiliations(aff)
    repeat_graph,repeat_edges,rep_meta=project_affiliations(aff,min_shared=2)
    wa=weighted_constraint(edges)
    unweighted=score_graph(g)
    diff={n:abs(wa[n]-unweighted[n]["constraint"]) for n in wa if n in unweighted}
    by_year=defaultdict(list)
    for row in aff:
        yr=str((meta.get(str(row["project_id"])) or {}).get("startDate") or "")[:4]
        if yr.isdigit():
            if int(yr)<=2017:layer="2014-2017"
            elif int(yr)<=2020:layer="2018-2020"
            else:layer="other"
        else:layer="unknown"
        by_year[layer].append(row)
    temporal={}
    for k,rows in by_year.items():
        one,_,_=project_affiliations(rows)
        temporal[k]={"two_mode":two_mode(rows,"project_id","organisation_id"),
                     "projected":sgraph_stats(one)}
    joint=undirected_layers({yr:list(project_affiliations(r)[1].keys())
                             for yr,r in by_year.items()})
    # Entity is organisation. Time segments are the ONLY directly comparable layers here.
    return {"status":"OBSERVED_PROJECT_AFFILIATION_TOPOLOGY_ONLY",
      "selection":"195 keyword-selected projects, NOT manually labelled; 233 inclusive variant",
      "two_mode":two_mode(aff,"project_id","organisation_id"),
      "by_role_two_mode":{
          name:two_mode(rows,"project_id","organisation_id")
          for name,rows in type_rows.items()},
      "one_mode_unweighted":sgraph_stats(g),
      "reverse_one_mode_shared_participant_project_graph":sgraph_stats(project_graph),
      "project_pairs_sharing_2plus_organizations":sum(x>=2 for x in project_shared.values()),
      "native_higher_order_consortium_hyperedges":higher_order_affiliation(aff),
      "one_mode_shared_project_count_weighted_constraint":describe(list(wa.values())),
      "difference_absolute_weighted_vs_binary_constraint":describe(list(diff.values())),
      "at_least_two_projects_backbone":sgraph_stats(repeat_graph),
      "repeated_edge_count":rep_meta["edges"],
      "inclusive_topics_keywords":{"two_mode":two_mode(alt,"project_id","organisation_id"),
           "projected":sgraph_stats(project_affiliations(alt)[0])},
      "time_layers":temporal,
      "time_multilayer":joint,
      "measured_heterogeneous_network":"project--organization affiliations with coordinator or participant role, funding amount attribute; role/funding are NOT observed information flows",
      "cross_dataset_linkage":"NONE_VERIFIED",
      "significance":"NOT_IDENTIFIED_AS_REAL_SOCIAL_BURT",
      "note":"The projected cliques inflate same-side edges. Low C can largely track k, project consortium size, or repeated memberships. Preserve 2-mode source."}

def openalex(live):
    x=(live.get("source_status",{}).get("OpenAlex",{}).get("parsed") or {})
    works=x.get("work_memberships") or []
    out={"status":"SMALL_PUBLIC_API_WORK_SAMPLE","works":len(works),"layers":{}}
    for key,prefix in (("authors","A:"),("institutions","I:")):
        rows=[{"work":w["work_id"],"entity":ent} for w in works
              for ent in w.get(key,[]) if w.get("work_id")]
        graph,proj,_=project_affiliations([{"project_id":x["work"],"organisation_id":x["entity"]} for x in rows])
        work_graph,work_overlap=right_projection_from_affiliations([{"project_id":x["work"],"organisation_id":x["entity"]} for x in rows])
        out["layers"][key]={"two_mode":two_mode(rows,"work","entity","W:",prefix),
                            "reverse_one_mode_shared_entity_work_graph":sgraph_stats(work_graph),
                            "work_pairs_sharing_two_plus_entities":sum(v>=2 for v in work_overlap.values()),
                            "one_mode":sgraph_stats(graph),
                            "repeated_cooccurrence_edges":sum(v>1 for v in proj.values())}
    authors_in_year=defaultdict(list)
    for w in works:
        yr=w.get("year")
        if yr is not None:
            for a in w.get("authors",[]):
                authors_in_year[str(yr)].append({"project_id":w.get("work_id"),"organisation_id":a})
    by_period=defaultdict(list)
    for yr,rows in authors_in_year.items():
        period="pre_2021" if yr.isdigit() and int(yr)<2021 else "2021_plus"
        by_period[period].extend(rows)
    period_edges={k:list(project_affiliations(v)[1].keys()) for k,v in by_period.items()}
    out["author_time_multilayer"]=undirected_layers(period_edges)
    out["cross_source_entity_linkage"]="NOT_VERIFIED_CORDIS_ROR_DOI"
    out["verdict"]="LOW_N_INSUFFICIENT_CONFIRMATORY_BURT"
    return out

def ocds(live):
    item=(live.get("source_status",{}).get("OCDS_REAL_UK",{}).get("parsed") or {})
    pairs=item.get("verified_scheme_id_buyer_supplier_edges") or []
    rows=[{"buyer":str(a),"supplier":str(b)} for a,b in pairs]
    buyer_supplier=two_mode(rows,"buyer","supplier","BUYER:","SUPPLIER:")
    purchase_aff=[{"project_id":x["buyer"],"organisation_id":x["supplier"]} for x in rows]
    p=project_affiliations(purchase_aff)
    buyer_proj, buyer_overlap=right_projection_from_affiliations(purchase_aff)
    return {"status":"FIXED_WINDOW_BOUNDED_UK_AWARD_SAMPLE",
            "real_notice_count":item.get("releases_in_package"),
            "award_count":item.get("award_count"),
            "two_mode_buyer_supplier":buyer_supplier,
            "supplier_one_mode_common_buyer":sgraph_stats(p[0]),
            "buyer_one_mode_common_supplier":sgraph_stats(buyer_proj),
            "note":"Common buyer ≠ supplier cooperation; award ≠ bid; party-ID missingness can remove most edges.",
            "verdict":"NO_VALIDATED_INFO_BROKERAGE"}

def gridkit(live):
    grid=live.get("grid_stats") or {}
    edges=grid.get("derived_edges") or []
    by_type=defaultdict(list)
    for x in edges:by_type[str(x.get("kind") or "unknown")].append((x["u"],x["v"]))
    # bus--asset incidence is two-mode by construction; a mathematical representation,
    # not the original electrical network (which has bus--bus physical edges).
    asset_edges=[]
    for idx,x in enumerate(edges):
        asset="asset:"+str(idx)
        asset_edges.append({"bus":"bus:"+str(x["u"]),"asset":asset})
        asset_edges.append({"bus":"bus:"+str(x["v"]),"asset":asset})
    layer_result=undirected_layers(by_type)
    bus_asset_aff=[{"project_id":x["bus"],"organisation_id":x["asset"]} for x in asset_edges]
    # Line graph: assets are linked when they share a bus, so buses play the "project" role.
    asset_proj,asset_overlap,_=project_affiliations(bus_asset_aff)
    return {"status":"UNOFFICIAL_2022_PHYSICAL_GRID_TOPOLOGY",
            "typed_edge_count_in_upstream":{k:len(v) for k,v in by_type.items()},
            "bus_asset_incidence_two_mode":two_mode(asset_edges,"bus","asset","BUS:","ASSET:"),
            "asset_one_mode_shared_bus_line_graph":sgraph_stats(asset_proj),
            "physical_bus_network":layer_result,
            "note":"Bus--asset incidence has C_i=1/k_i by construction, but electrical paths are not information or social brokerage.",
            "verdict":"TOPOLOGICAL_CONTROL_NOT_SOCIAL_BURT"}

def gleif(live):
    # GLEIF full RR-CDF bulk lives in a separate bounded Action job.
    x=(live.get("source_status",{}).get("GLEIF",{}).get("parsed") or {})
    return {"status":"LEVEL1_SINGLE_ENTITY_ONLY_FULL_RR_SEPARATE_JOB",
            "reported_keys":x.get("returned_relationship_keys"),
            "directed_parent_graph":"SEPARATE_RR_CDF_JOB",
            "two_mode":"NOT_APPLICABLE_LEGAL_ENTITY_PARENT_CHILD_SAME_NODE_TYPE",
            "social_burt":"NOT_IDENTIFIED_AS_KNOWLEDGE_FLOW",
            "verdict":"PARENT_RELATIONSHIP_MAY_BE_TOPOLOGICALLY_VALID_NOT_BURT_EVIDENCE"}

def sec(live):
    return {"status":"NO_SEC_FACTS_FETCHED_WITH_GENUINE_USER_AGENT",
            "two_mode":"NO_MULTIPLE_ENTITIES_OR_ENTITY_TO_ENTITY_RELATION_OBSERVED",
            "one_mode":"NOT_CONSTRUCTIBLE",
            "multilayer":"NOT_CONSTRUCTIBLE_FROM_FINANCIAL_ACCOUNTING_FACTS",
            "verdict":"ABSTAIN"}

def run(live):
    return {"schema":"ai-decision-six-source-multinetwork/1.0",
            "evidence":"OBSERVED_SOURCE_TOPOLOGY_OR_SCHEMA_ONLY",
            "CORDIS":cordis(live),"OpenAlex":openalex(live),"OCDS":ocds(live),
            "GLEIF":gleif(live),"SEC":sec(live),"PyPSA":gridkit(live),
            "cross_source_multiplex":"NOT_CONSTRUCTED_BECAUSE_COMMON_ENTITY_IDS_DO_NOT_PASS_RESOLUTION",
            "methods_not_portable":["V9 10x12 family pair null/hypergeometric/q; no identical sample frame",
                  "limitation claims and source-text semantic classes; not measured by organizational edge tables",
                  "Gould-Fernandez groups not established uniformly across all six sources",
                  "causal brokerage / innovation outcome or leader-follower equilibria not identifiable"],
            "overall":"NO_CONFIRMATORY_BURT_OR_SHARED_SEMANTIC_MULTIPLEX_YET"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    obj=run(json.loads(Path(a.input).read_text(encoding="utf-8")))
    dest=Path(a.output)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(dest),
      "CORDIS_projected_edges":obj["CORDIS"]["one_mode_unweighted"]["edges"],
      "CORDIS_temporal_layers":list(obj["CORDIS"]["time_layers"]),
      "verdict":obj["overall"]},ensure_ascii=False))

if __name__=="__main__":main()
