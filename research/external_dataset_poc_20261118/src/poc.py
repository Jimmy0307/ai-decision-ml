#!/usr/bin/env python3
"""Bounded external-data feasibility runner. All network/MLP claims are scoped."""
import argparse
import csv
import hashlib
import io
import itertools
import json
import os
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

SOURCES = {
 "CORDIS":"https://cordis.europa.eu/data/cordis-h2020projects-csv.zip",
 "OpenAlex":"https://api.openalex.org/works?search=artificial%20intelligence%20decision%20making&per-page=8",
 "OCDS_FICTIONAL":"https://raw.githubusercontent.com/open-contracting/sample-data/main/fictional-example/1.1/ocds-213czf-000-00001-04-award.json",
 "OCDS_REAL":"https://data.open-contracting.org/en/publication/128",
 "GLEIF":"https://api.gleif.org/api/v1/lei-records/5493001KJTIIGC8Y1R12",
 "SEC":"https://data.sec.gov/api/xbrl/companyconcept/CIK0000320193/us-gaap/Assets.json",
 "PyPSA_Transformers":"https://raw.githubusercontent.com/PyPSA/pypsa-eur/master/data/entsoegridkit/transformers.csv",
 "PyPSA_DC_Links":"https://raw.githubusercontent.com/PyPSA/pypsa-eur/master/data/entsoegridkit/links.csv",
 "PyPSA_AC_Lines":"https://raw.githubusercontent.com/PyPSA/pypsa-eur/master/data/entsoegridkit/lines.csv",
}
def bounded_get(url, max_bytes=8_000_000, ua="Academic research feasibility/0.1", accept=None):
    """Do not commit raw third-party response bodies; cap single file downloads."""
    if not url.startswith("https://"): raise ValueError("https_required")
    headers={"User-Agent":ua}
    if accept:headers["Accept"]=accept
    with urlopen(Request(url,headers=headers),timeout=30) as r:
        n=r.headers.get("Content-Length")
        if n and int(n)>max_bytes:raise ValueError("content_length_too_large")
        body=r.read(max_bytes+1)
    if len(body)>max_bytes:raise ValueError("stream_size_limit")
    return body,hashlib.sha256(body).hexdigest()

def grid_stats(transformers, links, lines=None):
    """UNOFFICIAL GridKit physical topology, NOT organization/social ties."""
    graph=defaultdict(set); edge_types={}; count={}
    for tag, raw in (("transformer",transformers),("dc_link",links),("ac_line",lines)):
        if raw is None:continue
        rd=csv.DictReader(io.StringIO(raw),quotechar="'")
        if not {"bus0","bus1"}.issubset(rd.fieldnames or []):raise ValueError("invalid_pypsa_schema")
        count[tag]=0
        for row in rd:
            count[tag]+=1
            a,b=(row.get("bus0") or "").strip(),(row.get("bus1") or "").strip()
            if not a or not b or a==b:continue
            e=tuple(sorted((a,b))); edge_types.setdefault(e,tag)
    for a,b in edge_types:
        graph[a].add(b);graph[b].add(a)
    seen=set();components=[]
    for n in graph:
        if n in seen:continue
        q=deque([n]);seen.add(n);k=0
        while q:
            x=q.popleft();k+=1
            for y in graph[x]:
                if y not in seen:seen.add(y);q.append(y)
        components.append(k)
    triangles=sum(len(graph[a]&graph[b]) for a,b in edge_types)//3
    return {"rows":count,"nodes":len(graph),"edges":len(edge_types),
            "components":len(components),"largest_component":max(components,default=0),
            "triangles":triangles,"ac_lines_included":lines is not None,
            "scope":"UNOFFICIAL_2022_GRIDKIT_MAP_PHYSICAL_NETWORK_ONLY"}

def ocds_stats(data):
    rs=data.get("releases",[])
    winners={s.get("id") for r in rs for a in r.get("awards",[]) for s in a.get("suppliers",[]) if s.get("id")}
    bidders={s.get("id") for r in rs for s in (r.get("tender") or {}).get("tenderers",[]) if s.get("id")}
    return {"releases":len(rs),"bidders":len(bidders),"winners":len(winners),
            "awards":sum(len(r.get("awards",[])) for r in rs),
            "scope":"SCHEMA_EXAMPLE_IS_FICTIONAL_NOT_EMPIRICAL"}

def openalex_stats(data):
    works=data.get("results",[])
    authors={a.get("author",{}).get("id") for w in works for a in w.get("authorships",[])}
    institutions={i.get("id") for w in works for a in w.get("authorships",[]) for i in a.get("institutions",[])}
    return {"works":len(works),"authors":len(authors-{None}),"institutions":len(institutions-{None}),
            "work_ids":[w.get("id") for w in works],
            "works_with_doi":sum(bool(w.get("doi")) for w in works),
            "any_truncated_authorships":any(w.get("is_authors_truncated",False) for w in works),
            "scope":"BOUNDED_LIVE_API_SAMPLE_NOT_A_RECONCILED_CORDIS_LINK"}

def gleif_stats(data):
    x=data.get("data",{})
    if isinstance(x,list):x=x[0] if x else {}
    rel=x.get("relationships") or {}
    return {"lei":x.get("id"),"returned_relationship_keys":sorted(rel.keys()),
            "parent_link_paths":{k:(rel.get(k,{}).get("links") or {}).get("related") for k in ("direct-parent","ultimate-parent")},
            "scope":"LEVEL_1_RESPONSE_PARENT_NOT_VERIFIED"}

def sec_stats(data):
    return {"cik":data.get("cik"),"tag":data.get("tag"),
            "financial_observations":sum(len(v) for v in data.get("units",{}).values() if isinstance(v,list)),
            "scope":"FINANCIAL_REPORTING_NOT_AI_INVESTMENT_OR_FOLLOWER_UTILITY"}

def toy_mlp(B=10):
    """Finite three-follower Stackelberg toy, independent follower reactions."""
    if B<0 or B>30:raise ValueError("B outside toy bounds")
    a=(8,7,9)
    def u(i,x):return a[i]*x-1.5*x*x
    leader_best=None
    for cap in itertools.product(range(B+1),repeat=3):
        if sum(cap)>B:continue
        x=tuple(max(range(cap[i]+1),key=lambda v:(u(i,v),-v)) for i in range(3))
        welfare=sum(u(i,x[i]) for i in range(3))
        leader=welfare-.65*sum(cap)-.2*(max(x)-min(x))
        if leader_best is None or leader>leader_best["objective"]:
            leader_best={"capacity":list(cap),"best_responses":list(x),"objective":leader,"welfare":welfare}
    central=max((sum(u(i,x[i]) for i in range(3)),x) for x in itertools.product(range(B+1),repeat=3) if sum(x)<=B)
    return {"evidence":"SYNTHETIC_TOY","budget":B,"leader":leader_best,
            "centralized_max_welfare":central[0],"centralized_allocation":list(central[1]),
            "warning":"Different objectives; not an empirical price of anarchy"}

def gne_shared_capacity(K=3):
    def u(x):return 4*x-.5*x*x
    eq=[]
    for x in range(K+1):
        for y in range(K+1-x):
            brx=max(range(K-y+1),key=u)
            bry=max(range(K-x+1),key=u)
            if x==brx and y==bry:eq.append([x,y])
    return {"evidence":"SYNTHETIC_GNE_TOY","capacity":K,"equilibria":eq,
            "warning":"Shared feasible set invalidates independent-follower decomposition"}

def run(mode="fixture", cordis=False, full_grid=False):
    result={"timestamp":datetime.now(timezone.utc).isoformat(),"mode":mode,
            "source_status":{},"source_urls":SOURCES,
            "toy_mlp":toy_mlp(),"toy_gne":gne_shared_capacity()}
    if mode=="fixture":
        result["fixture"]={
         "pypsa":grid_stats("transformer_id,bus0,bus1\nT1,1,2\nT2,2,3\nT3,1,3\n","link_id,bus0,bus1\nL1,3,4\n"),
         "ocds":ocds_stats({"releases":[{"buyer":{"id":"buyer-fixture"},
                                      "tender":{"tenderers":[{"id":"bidder1"}]},
                                      "awards":[{"suppliers":[{"id":"bidder1"}]}]}]})}
        for k in SOURCES:result["source_status"][k]={"status":"NOT_RETRIEVED_FIXTURE_MODE"}
        return result
    payloads={}
    enabled={"OpenAlex","OCDS_FICTIONAL","GLEIF","PyPSA_Transformers","PyPSA_DC_Links"}
    if full_grid:enabled.add("PyPSA_AC_Lines")
    if cordis:enabled.add("CORDIS")
    ua=os.environ.get("SEC_USER_AGENT","")
    if "@" in ua and len(ua)>15 and "example" not in ua.lower():enabled.add("SEC")
    for k,url in SOURCES.items():
        if k not in enabled:
            why={"CORDIS":"OPT_IN_BULK_DOWNLOAD","SEC":"VALID_CONTACT_USER_AGENT_REQUIRED",
                 "OCDS_REAL":"PUBLICATION_CHOICE_AND_COVERAGE_REQUIRED",
                 "PyPSA_AC_Lines":"OPT_IN_FULL_GRID"} .get(k,"SKIPPED")
            result["source_status"][k]={"status":"NOT_RUN","reason":why}
            continue
        try:
            raw,sha=bounded_get(url,
                  max_bytes=180_000_000 if k=="CORDIS" else 8_000_000,
                  ua=ua if k=="SEC" else "AI-Decision academic reproducibility feasibility/0.1",
                  accept="application/vnd.api+json" if k=="GLEIF" else None)
            result["source_status"][k]={"status":"FETCHED","size_bytes":len(raw),"sha256":sha}
            payloads[k]=raw
        except Exception as e:
            result["source_status"][k]={"status":"FETCH_FAILED","error":type(e).__name__,
                                       "message":str(e)[:170]}
    for key,fn in {"OpenAlex":openalex_stats,"OCDS_FICTIONAL":ocds_stats,
                   "GLEIF":gleif_stats,"SEC":sec_stats}.items():
        if key in payloads:
            try:result["source_status"][key]["parsed"]=fn(json.loads(payloads[key]))
            except Exception as e:result["source_status"][key]["parse_error"]=type(e).__name__
    # Small *empirical* public probes: do not confuse a successful HTTP response
    # with evidence that bidder coverage or consortia identification are adequate.
    from urllib.parse import quote
    cordis_query=("PREFIX eurio: <http://data.europa.eu/s66#> "
                  "SELECT ?project ?organisation ?role WHERE { "
                  "?project a eurio:Project . "
                  "?project eurio:hasInvolvedParty ?party . "
                  "?party eurio:isRoleOf ?organisation . "
                  "OPTIONAL { ?party eurio:roleLabel ?role . } } LIMIT 24")
    empirical_urls={
       "CORDIS_SPARQL":"https://cordis.europa.eu/datalab/sparql/query?query="+quote(cordis_query)+"&format=json",
       "OCDS_REAL_UK":"https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages?limit=1",
    }
    for k,url in empirical_urls.items():
        try:
            raw,sha=bounded_get(url,max_bytes=1_500_000,accept="application/sparql-results+json,application/json")
            obj=json.loads(raw)
            if k=="CORDIS_SPARQL":
                bindings=(obj.get("results") or {}).get("bindings",[])
                parsed={"row_count":len(bindings),
                        "fields":sorted({v for row in bindings for v in row}),
                        "unique_project_uris":len({r.get("project",{}).get("value") for r in bindings}),
                        "project_sample_uris":list(dict.fromkeys(r.get("project",{}).get("value") for r in bindings))[:24],
                        "scope":"TINY_CONSORTIUM_QUERY_NOT_H2020_POPULATION"}
            else:
                packages=obj.get("releases",obj.get("results",[]))
                parsed={"top_level_keys":sorted(obj.keys()),"releases_in_package":len(packages) if isinstance(packages,list) else None,
                        "ocids":[r.get("ocid") for r in packages[:3]] if isinstance(packages,list) else [],
                        "tags":[r.get("tag") for r in packages[:3]] if isinstance(packages,list) else [],
                        "tenderer_count_observed":sum(len((r.get("tender") or {}).get("tenderers",[])) for r in packages) if isinstance(packages,list) else 0,
                        "scope":"REAL_UK_NOTICE_PROBE_NOT_FAILED_BIDDER_COMPLETENESS"}
            result["source_status"][k]={"status":"FETCHED_PARSED","size_bytes":len(raw),"sha256":sha,
                                       "url":url,"parsed":parsed}
        except Exception as e:
            result["source_status"][k]={"status":"FETCH_OR_PARSE_FAILED","url":url,
                                       "error":type(e).__name__,"message":str(e)[:165]}
    if "PyPSA_Transformers" in payloads and "PyPSA_DC_Links" in payloads:
        try:
            result["grid_stats"]=grid_stats(payloads["PyPSA_Transformers"].decode("utf-8-sig"),
                payloads["PyPSA_DC_Links"].decode("utf-8-sig"),
                payloads["PyPSA_AC_Lines"].decode("utf-8-sig") if "PyPSA_AC_Lines" in payloads else None)
        except Exception as e:result["grid_error"]={"type":type(e).__name__,"message":str(e)[:160]}
    if "CORDIS" in payloads:
        import zipfile
        try:
            with zipfile.ZipFile(io.BytesIO(payloads["CORDIS"])) as z:
                result["cordis_inventory"]={"csv_members":[n for n in z.namelist() if n.endswith(".csv")],
                                            "status":"DOWNLOADED_NOT_FULL_JOIN_VALIDATED"}
        except Exception as e:result["cordis_inventory"]={"status":"ZIP_INVALID","type":type(e).__name__}
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--mode",choices=["fixture","live"],default="fixture")
    p.add_argument("--cordis-bulk",action="store_true")
    p.add_argument("--pypsa-full",action="store_true")
    p.add_argument("--output",default="research/external_dataset_poc_20261118/results/latest-run.json")
    a=p.parse_args()
    obj=run(a.mode,cordis=a.cordis_bulk,full_grid=a.pypsa_full)
    path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(path),"mode":a.mode,
                      "statuses":{k:v["status"] for k,v in obj["source_status"].items()},
                      "toy_leader":obj["toy_mlp"]["leader"]},ensure_ascii=False))
if __name__=="__main__":main()
