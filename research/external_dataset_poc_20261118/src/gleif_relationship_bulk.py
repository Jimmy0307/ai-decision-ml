#!/usr/bin/env python3
"""Official dated GLEIF RR-CDF 2.1 full XML relationship file; exploratory.

The dataset records legal consolidation/fund relations, NOT information
brokerage. Strong distinction between Level 2 parent and social ties.
"""
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET
import zipfile

OFFICIAL_PINNED_URL="https://leidata.gleif.org/api/v1/concatenated-files/rr/get/41888/zip"
SOURCE_DATE="2026-08-10"  # fixed historical snapshot, not 2026-11-18 latest
MAX_BYTES=72_000_000

def local(tag):
    return tag.rsplit("}",1)[-1]

def legal_graph_profile(active_by_type, sample_limit=1500, max_ego_degree=100, seed=20261118):
    """Full active direct/ultimate legal graph; Burt only on bounded-degree ego sample.

    The graph is composed of legal consolidating relations, not knowledge flows.
    Large-degree egos are excluded from sampling; summary cannot represent all.
    """
    from collections import defaultdict, deque
    import random
    from statistics import median
    direct=active_by_type.get("IS_DIRECTLY_CONSOLIDATED_BY",set())
    ultimate=active_by_type.get("IS_ULTIMATELY_CONSOLIDATED_BY",set())
    adjacency=defaultdict(set)
    for a,b in direct|ultimate:
        if a!=b:
            adjacency[a].add(b); adjacency[b].add(a)
    seen=set();cc_sizes=[]
    for root in adjacency:
        if root in seen:continue
        seen.add(root);q=deque([root]);size=0
        while q:
            x=q.popleft();size+=1
            for y in adjacency[x]:
                if y not in seen:seen.add(y);q.append(y)
        cc_sizes.append(size)
    eligible=sorted(u for u,n in adjacency.items() if 2<=len(n)<=max_ego_degree)
    rng=random.Random(seed)
    picked=rng.sample(eligible,min(sample_limit,len(eligible)))
    samples=[]
    for u in picked:
        ns=adjacency[u];k=len(ns);inv=1/k
        common_twice=0; c=0.0
        for j in ns:
            shared=ns & adjacency[j]
            common_twice+=len(shared)
            indirect=sum(inv/len(adjacency[q]) for q in shared)
            c+=(inv+indirect)**2
        samples.append({"degree":k,"constraint":c,"effective_size":k-common_twice/k,
                        "indirect_excess":c-inv})
    def summarize(vals):
        if not vals:return {"n":0}
        return {"n":len(vals),"min":min(vals),"median":median(vals),"max":max(vals)}
    return {"direct_active_edges":len(direct),"ultimate_active_edges":len(ultimate),
            "direct_ultimate_active_edge_overlap":len(direct&ultimate),
            "direct_ultimate_active_union_edges":len(direct|ultimate),
            "directed_edge_source_and_target_same_legal_entity_type":True,
            "role_coded_two_mode":{"child_legal_entities":len({a for a,b in direct}),
              "consolidating_parent_entities":len({b for a,b in direct}),
              "affiliation_edges":len(direct),
              "strict_role_bipartite_constraint":"1/k; no same-side indirect term by construction",
              "role_graph_is_artificial":"Same entity may appear as child and parent; duplication of roles is not independent social membership."},
            "undirected_parent_union":{"nodes_with_edge":len(adjacency),
              "edges":len({tuple(sorted((a,b))) for a,b in direct|ultimate}),
              "connected_components":len(cc_sizes),
              "largest_component_nodes":max(cc_sizes,default=0),
              "nodes_degree_2_to_100":len(eligible),
              "nodes_degree_over_100":sum(len(v)>max_ego_degree for v in adjacency.values())},
            "bounded_ego_constraint_sample":{"sample_size":len(samples),
              "seed":seed,"max_ego_degree":max_ego_degree,
              "constraint":summarize([x["constraint"] for x in samples]),
              "effective_size":summarize([x["effective_size"] for x in samples]),
              "indirect_excess":summarize([x["indirect_excess"] for x in samples]),
              "number_positive_indirect":sum(x["indirect_excess"]>1e-10 for x in samples),
              "not_a_population_estimate":"Excludes ego degrees 0,1 and >100; directed legal relation converted to undirected; not confirmatory social brokerage."}}

def parse_xml_stream(fileobj,retain_sample=80):
    context=ET.iterparse(fileobj,events=("start","end"))
    _,root=next(context)
    kinds=Counter(); statuses=Counter();types=Counter()
    direct=set();ultimate=set(); nodes=set(); invalid=0;count=0;examples=[]
    active_by_type=__import__('collections').defaultdict(set)
    active_rows=Counter()
    for event,elem in context:
        if event!="end" or local(elem.tag)!="RelationshipRecord":
            continue
        count+=1
        relationship=next((x for x in elem.iter() if local(x.tag)=="Relationship"),None)
        fields={}
        if relationship is not None:
            for sub in relationship:
                name=local(sub.tag)
                if name in ("StartNode","EndNode"):
                    fields[name]=next((x.text for x in sub.iter() if local(x.tag)=="NodeID"),None)
                elif name in ("RelationshipType","RelationshipStatus"):
                    fields[name]=sub.text
        a,b=fields.get("StartNode"),fields.get("EndNode")
        ty=fields.get("RelationshipType") or "UNSPECIFIED"
        status=fields.get("RelationshipStatus") or "UNSPECIFIED"
        types[ty]+=1;statuses[status]+=1
        if a and b and a!=b:
            nodes.update((a,b))
            edge=(a,b)
            if status=="ACTIVE":
                active_by_type[ty].add(edge)
                active_rows[ty]+=1
            if ty=="IS_DIRECTLY_CONSOLIDATED_BY":direct.add(edge)
            if ty=="IS_ULTIMATELY_CONSOLIDATED_BY":ultimate.add(edge)
            if len(examples)<retain_sample:
                examples.append({"child":a,"parent":b,"relation_type":ty,
                                  "relationship_status":status})
        else:invalid+=1
        elem.clear()
        root.clear()
    return {"record_rows":count,"relationship_types":dict(types),"status_values":dict(statuses),
            "unique_nodes_with_relationship":len(nodes),"direct_unique_edges":len(direct),
            "ultimate_unique_edges":len(ultimate),
            "different_direct_and_ultimate_edges":len(direct.symmetric_difference(ultimate)),
            "invalid_start_end_or_self_loop":invalid,
            "active_relationship_type_rows":dict(active_rows),
            "active_relationship_distinct_edges":{k:len(v) for k,v in active_by_type.items()},
            "active_multilayer_legal_graph":legal_graph_profile(active_by_type),
            "examples_first_records":examples,
            "global_direct_parent_child_degree":degree_digest(direct),
            "global_ultimate_parent_child_degree":degree_digest(ultimate),
            "all_recorded_relation_types_included_in_parent_graph":False,
            "source_scope":"GLOBAL_LEGAL_ENTITY_RELATIONSHIPS_NOT_KNOWLEDGE_BROKERAGE"}

def degree_digest(edges):
    from statistics import median
    parent=Counter(b for a,b in edges);child=Counter(a for a,b in edges)
    return {"unique_parents":len(parent),"unique_children":len(child),
            "parent_max_children":max(parent.values(),default=0),
            "median_parent_children":median(parent.values()) if parent else None,
            "parents_with_2plus_children":sum(x>=2 for x in parent.values()),
            "children_with_2plus_parents":sum(x>=2 for x in child.values()),
            "top_parent_lei_anonymized":[{"rank":i+1,"child_count":v}
                  for i,(_,v) in enumerate(parent.most_common(12))]}

def parse_zip(blob):
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        xmls=[x for x in z.namelist() if x.lower().endswith(".xml")]
        if not xmls:raise ValueError("No XML member")
        with z.open(xmls[0]) as stream:
            out=parse_xml_stream(stream)
        out["zip_members"]=[{"name":n,"uncompressed_bytes":z.getinfo(n).file_size}
                            for n in z.namelist()]
        return out

def fetch_and_profile(max_bytes=MAX_BYTES):
    with urlopen(Request(OFFICIAL_PINNED_URL,
                          headers={"User-Agent":"AI Decision reproducible public-data methods study/1.0"}),
                 timeout=120) as r:
        blob=r.read(max_bytes+1)
    if len(blob)>max_bytes:raise ValueError("GLEIF ZIP exceeds size gate")
    data=parse_zip(blob)
    return {"status":"DOWNLOADED_AND_PARSED",
            "official_url":OFFICIAL_PINNED_URL,"snapshot_date":SOURCE_DATE,
            "bytes_downloaded":len(blob),"sha256":hashlib.sha256(blob).hexdigest(),
            "relationship_profile":data,
            "verdict":"LEGAL_CONSOLIDATION_GRAPH_VALID_SOCIAL_BURT_NOT_IDENTIFIED",
            "warning":"Source snapshot includes relationship records, not reporting exceptions, private non-LEI parents, social ties or firm decision utility."}

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--output",required=True)
    p=a.parse_args()
    try:out=fetch_and_profile()
    except Exception as e:
        out={"status":"FETCH_OR_PARSE_BLOCKED","reason":type(e).__name__,"detail":str(e)[:220],
             "official_url":OFFICIAL_PINNED_URL,"snapshot_date":SOURCE_DATE}
    dest=Path(p.output);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"status":out["status"],"output":str(dest),
                      "record_rows":out.get("relationship_profile",{}).get("record_rows"),
                      "error":out.get("detail")},ensure_ascii=False))
if __name__=="__main__":main()
