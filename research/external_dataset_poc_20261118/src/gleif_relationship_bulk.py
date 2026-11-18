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

def parse_xml_stream(fileobj,retain_sample=80):
    context=ET.iterparse(fileobj,events=("start","end"))
    _,root=next(context)
    kinds=Counter(); statuses=Counter();types=Counter()
    direct=set();ultimate=set(); nodes=set(); invalid=0;count=0;examples=[]
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
