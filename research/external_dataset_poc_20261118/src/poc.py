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
 "OpenAlex":"https://api.openalex.org/works?search=artificial%20intelligence%20decision%20making&per-page=50",
 "OCDS_FICTIONAL":"https://raw.githubusercontent.com/open-contracting/sample-data/main/fictional-example/1.1/ocds-213czf-000-00001-04-award.json",
 "OCDS_REAL":"https://data.open-contracting.org/en/publication/128",
 "GLEIF":"https://api.gleif.org/api/v1/lei-records/5493001KJTIIGC8Y1R12",
 "SEC":"https://data.sec.gov/api/xbrl/companyconcept/CIK0000320193/us-gaap/Assets.json",
 "PyPSA_Transformers":"https://raw.githubusercontent.com/PyPSA/pypsa-eur/master/data/entsoegridkit/transformers.csv",
 "PyPSA_DC_Links":"https://raw.githubusercontent.com/PyPSA/pypsa-eur/master/data/entsoegridkit/links.csv",
 "PyPSA_AC_Lines":"https://raw.githubusercontent.com/PyPSA/pypsa-eur/master/data/entsoegridkit/lines.csv",
}
def bounded_get(url, max_bytes=8_000_000, ua="Academic research feasibility/0.1", accept=None, timeout=30):
    """Do not commit raw third-party response bodies; cap single file downloads."""
    if not url.startswith("https://"): raise ValueError("https_required")
    headers={"User-Agent":ua}
    if accept:headers["Accept"]=accept
    with urlopen(Request(url,headers=headers),timeout=timeout) as r:
        n=r.headers.get("Content-Length")
        if n and int(n)>max_bytes:raise ValueError("content_length_too_large")
        body=r.read(max_bytes+1)
    if len(body)>max_bytes:raise ValueError("stream_size_limit")
    return body,hashlib.sha256(body).hexdigest()

def grid_stats(transformers, links, lines=None, export_edges=False):
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
            "derived_edges":[{"u":a,"v":b,"kind":t} for (a,b),t in sorted(edge_types.items())] if export_edges else None,
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
    work_authorship=[{"work_id":w.get("id"),"doi":w.get("doi"),
        "year":w.get("publication_year"),
        "authors":sorted({a.get("author",{}).get("id") for a in w.get("authorships",[]) if a.get("author",{}).get("id")}),
        "institutions":sorted({i.get("id") for a in w.get("authorships",[]) for i in a.get("institutions",[]) if i.get("id")})} for w in works]
    authors={a.get("author",{}).get("id") for w in works for a in w.get("authorships",[])}
    institutions={i.get("id") for w in works for a in w.get("authorships",[]) for i in a.get("institutions",[])}
    return {"works":len(works),"authors":len(authors-{None}),"institutions":len(institutions-{None}),
            "work_ids":[w.get("id") for w in works],
            "work_memberships":work_authorship,
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

def cordis_bulk_stats(blob):
    """Stream official H2020 project/organisation CSVs. Aggregate participation counts only."""
    import zipfile
    from pathlib import PurePosixPath
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        members={PurePosixPath(p).name.lower():p for p in archive.namelist()}
        if any(x not in members for x in ("project.csv","organization.csv")):
            return {"status":"MISSING_REQUIRED_MEMBERS","csv_members":[x for x in members if x.endswith(".csv")]}
        def reader(name):
            handle=archive.open(members[name])
            wrapper=io.TextIOWrapper(handle,encoding="utf-8-sig",errors="replace",newline="")
            first=wrapper.readline()
            delim=";" if first.count(";")>first.count(",") else ","
            from itertools import chain
            return csv.DictReader(chain([first],wrapper),delimiter=delim)
        # Exploratory text keywords, not validated AI/Decision concept annotations.
        ai_terms=("artificial intelligence","machine learning","deep learning","neural network","predictive analytics")
        decision_terms=("decision making","decision-making","decision support","decision process","decision maker","decision-maker")
        pids=set(); project_rows=0
        ai_projects=set(); decision_projects=set(); joint_projects=set()
        topic_sensitivity_joint=set()
        joint_metadata={}
        project_fields=reader("project.csv").fieldnames
        org_fields=reader("organization.csv").fieldnames
        for row in reader("project.csv"):
            project_rows+=1
            pid=(row.get("id") or row.get("projectID") or "").strip()
            if pid:
                pids.add(pid)
                combined=" ".join(str(row.get(k) or "") for k in ("title","objective","topic")).lower()
                hit_ai=any(term in combined for term in ai_terms)
                hit_de=any(term in combined for term in decision_terms)
                if hit_ai:ai_projects.add(pid)
                if hit_de:decision_projects.add(pid)
                alltext=combined+" "+str(row.get("topics") or "").lower()+" "+str(row.get("keywords") or "").lower()
                if any(term in alltext for term in ai_terms) and any(term in alltext for term in decision_terms):
                    topic_sensitivity_joint.add(pid)
                if hit_ai and hit_de:
                    joint_projects.add(pid)
                    joint_metadata[pid]={
                      "startDate":row.get("startDate"),"endDate":row.get("endDate"),
                      "totalCost":row.get("totalCost"),"ecMaxContribution":row.get("ecMaxContribution"),
                      "grantDoi":row.get("grantDoi"),"frameworkProgramme":row.get("frameworkProgramme")}
        organisation_rows=0; orgids=set(); source_projectids=set()
        selected_participants=defaultdict(set)
        alternate_participants=defaultdict(set)
        selected_roles=defaultdict(set)
        selected_allocation_rows=[]
        full_organisation_funding_missing={"ecContribution":0,"netEcContribution":0,"totalCost":0}
        def to_money(value):
            if value is None or not str(value).strip():return None
            v=str(value).replace(" ","").replace("\u00a0","")
            if "," in v and "." in v:
                v=v.replace(".","").replace(",",".") if v.rfind(",")>v.rfind(".") else v.replace(",","")
            elif "," in v:
                v=v.replace(",",".")
            try:return float(v)
            except ValueError:return None
        project_members=defaultdict(int); matched_projects=0; valid_orgids=0; coordinator_roles=0
        for row in reader("organization.csv"):
            organisation_rows+=1
            pid=(row.get("projectID") or row.get("projectId") or "").strip()
            oid=(row.get("organisationID") or row.get("organizationID") or "").strip()
            role=(row.get("role") or "").strip().lower()
            if pid:
                source_projectids.add(pid); project_members[pid]+=1
                if pid in pids: matched_projects+=1
            if oid:
                orgids.add(oid); valid_orgids+=1
                if pid in topic_sensitivity_joint: alternate_participants[pid].add(oid)
                if pid in joint_projects:
                    selected_participants[pid].add(oid)
                    selected_roles[oid].add(role)
                    selected_allocation_rows.append({
                       "project_id":pid,"organisation_id":oid,"role":role,
                       "ecContribution":to_money(row.get("ecContribution")),
                       "netEcContribution":to_money(row.get("netEcContribution")),
                       "totalCost":to_money(row.get("totalCost")),
                       "country":row.get("country"),"activityType":row.get("activityType")})
            for funding_col in full_organisation_funding_missing:
                if to_money(row.get(funding_col)) is None: full_organisation_funding_missing[funding_col]+=1
            if "coordinator" in role:coordinator_roles+=1
        # Induced shared-consortium *affiliation projection*: NOT observed bilateral
        # research communication or an independently validated Burt network.
        publication_profile={"status":"NO_PUBLICATION_CSV",
                             "csv_members":sorted(n for n in members if n.endswith(".csv"))}
        pub_name=next((n for n in ("publication.csv","publications.csv") if n in members),None)
        if pub_name:
            pubs=reader(pub_name)
            pub_fields=pubs.fieldnames
            pub_rows=0; joined_pub=0;selected_pub=0;selected_doi=0;selected_doi_ids=set()
            selected_publication_links=[]
            for row in pubs:
                pub_rows+=1
                pid=(row.get("projectID") or row.get("projectId") or "").strip()
                if pid in pids:joined_pub+=1
                if pid in joint_projects:
                    selected_pub+=1
                    doi=(row.get("doi") or row.get("DOI") or "").strip()
                    if doi: selected_doi+=1; selected_doi_ids.add(doi.lower())
                    if len(selected_publication_links)<300:
                        selected_publication_links.append({"project_id":pid,"doi":doi,
                                               "publication_year":row.get("year") or row.get("publishedYear")})
            publication_profile={"status":"PARSED",
                  "file":pub_name,"fields":pub_fields,"all_rows":pub_rows,
                  "rows_joining_h2020_projects":joined_pub,
                  "selected_195_project_publication_rows":selected_pub,
                  "selected_publication_rows_with_doi":selected_doi,
                  "unique_selected_publication_dois":len(selected_doi_ids),
                  "up_to_300_selected_publication_id_links":selected_publication_links,
                  "warning":"CORDIS outcome catalog and project record are the SAME source; not an independent validation sample."}
        projected_edges=set()
        for names in selected_participants.values():
            if len(names)>250:continue  # prevent unusual huge consortium expansion
            for aa,bb in itertools.combinations(sorted(names),2):
                projected_edges.add((aa,bb))
        projected_adj=defaultdict(set)
        for aa,bb in projected_edges:
            projected_adj[aa].add(bb);projected_adj[bb].add(aa)
        proj_visited=set();sizes=[]
        for start in projected_adj:
            if start in proj_visited:continue
            dq=deque([start]);proj_visited.add(start);size=0
            while dq:
                x=dq.popleft();size+=1
                for y in projected_adj[x]:
                    if y not in proj_visited:
                        proj_visited.add(y);dq.append(y)
            sizes.append(size)
        membership_count=defaultdict(int)
        for members in selected_participants.values():
            for org in members:membership_count[org]+=1
        derived_affiliations=[{"project_id":pid,"organisation_id":oid}
                              for pid in sorted(selected_participants)
                              for oid in sorted(selected_participants[pid])]
        # The selected public identifiers form a reproducible derived bi-modal dataset.
        # Institution/author names, full source text and original CORDIS ZIP are not emitted.
        exploratory={"definition":"UNVALIDATED_STRING_MATCHING_IN_TITLE_OBJECTIVE_TOPIC",
                     "ai_terms":list(ai_terms),"decision_terms":list(decision_terms),
                     "ai_projects":len(ai_projects),"decision_projects":len(decision_projects),
                     "joint_ai_decision_projects":len(joint_projects),
                     "joint_ai_decision_projects_including_topics_keywords":len(topic_sensitivity_joint),
                     "selection_added_only_by_topics_keywords":len(topic_sensitivity_joint-joint_projects),
                     "joint_projects_with_participant":len(selected_participants),
                     "joint_projects_with_2plus_organizations":sum(len(v)>1 for v in selected_participants.values()),
                     "unique_joint_project_organizations":len(membership_count),
                     "organizations_in_two_or_more_joint_projects":sum(x>=2 for x in membership_count.values()),
                     "selected_project_participation_edges":len(derived_affiliations),
                     "project_records_with_cost":sum(bool(m.get("totalCost")) for m in joint_metadata.values()),
                     "project_records_with_grant_doi":sum(bool(m.get("grantDoi")) for m in joint_metadata.values()),
                     "derived_affiliations":derived_affiliations,
                     "alternate_affiliations":[{"project_id":pid,"organisation_id":oid} for pid in sorted(alternate_participants) for oid in sorted(alternate_participants[pid])],
                     "derived_allocations":selected_allocation_rows,
                     "selected_project_metadata":joint_metadata,
                     "consortium_projected_unique_edges":len(projected_edges),
                     "projected_nonisolated_organizations":len(projected_adj),
                     "projected_connected_components":len(sizes),
                     "projected_largest_component":max(sizes,default=0),
                     "scope":"DRAFT_AFFILIATION_PROJECTION_NOT_CONFIRMED_BURT_BROKERAGE"}
        return {"status":"BOUNDED_BULK_READ_SUCCESS",
                "project_csv_columns":project_fields,"organization_csv_columns":org_fields,
                "publication_profile":publication_profile,
                "exploratory_ai_decision":exploratory,
                "project_rows":project_rows,"unique_project_ids":len(pids),
                "organisation_rows":organisation_rows,"unique_participant_organisation_ids":len(orgids),
                "organisation_rows_with_matched_project_id":matched_projects,
                "organisation_rows_with_identifier":valid_orgids,
                "full_organisation_funding_missing":full_organisation_funding_missing,
                "project_ids_in_organisation_rows":len(source_projectids),
                "projects_with_two_or_more_participations":sum(x>=2 for x in project_members.values()),
                "max_participation_rows_in_one_project":max(project_members.values(),default=0),
                "coordinator_role_mentions":coordinator_roles,
                "scope":"CONSORTIUM_MEMBERSHIP_NOT_DIRECT_INDIVIDUAL_BROKERAGE"}

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
                  accept="application/vnd.api+json" if k=="GLEIF" else None,
                  timeout=105 if k=="CORDIS" else 30)
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
       "OCDS_REAL_UK":"https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages?limit=100&stages=award&updatedFrom=2026-08-01T00:00:00&updatedTo=2026-08-31T23:59:59",
    }
    for k,url in empirical_urls.items():
        try:
            raw,sha=bounded_get(url,max_bytes=8_000_000,accept="application/sparql-results+json,application/json")
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
                def stable_key(item,parties):
                    pid=str((item or {}).get("id") or "")
                    party=next((x for x in parties if str(x.get("id") or "")==pid),{})
                    ident=party.get("identifier") or {}
                    if not ident.get("id"):ident=(item or {}).get("identifier") or {}
                    scheme,ident_id=str(ident.get("scheme") or ""),str(ident.get("id") or "")
                    return scheme+":"+ident_id if scheme and ident_id else None
                stable_edges=set(); awards_count=0; with_stable_buyer=0
                if isinstance(packages,list):
                    for record in packages:
                        parties=record.get("parties") or []
                        buyer=stable_key(record.get("buyer"),parties)
                        if buyer:with_stable_buyer+=1
                        for award in record.get("awards") or []:
                            awards_count+=1
                            for supplier in award.get("suppliers") or []:
                                sup=stable_key(supplier,parties)
                                if buyer and sup and buyer!=sup:stable_edges.add((buyer,sup))
                parsed={"top_level_keys":sorted(obj.keys()),"releases_in_package":len(packages) if isinstance(packages,list) else None,
                        "window":"updatedFrom=2026-08-01 through updatedTo=2026-08-31; stages=award; max 100 releases",
                        "award_count":awards_count,"notices_with_global_buyer_id":with_stable_buyer,
                        "verified_scheme_id_buyer_supplier_edges":sorted(stable_edges),
                        "ocids":[r.get("ocid") for r in packages[:3]] if isinstance(packages,list) else [],
                        "tags":[r.get("tag") for r in packages[:3]] if isinstance(packages,list) else [],
                        "tenderer_count_observed":sum(len((r.get("tender") or {}).get("tenderers",[])) for r in packages) if isinstance(packages,list) else 0,
                        "real_buyer_supplier_edges":sorted({(str((r.get("buyer") or {}).get("id")),str(s.get("id"))) for r in packages for a in r.get("awards",[]) for s in a.get("suppliers",[]) if (r.get("buyer") or {}).get("id") and s.get("id")}) if isinstance(packages,list) else [],
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
                payloads["PyPSA_AC_Lines"].decode("utf-8-sig") if "PyPSA_AC_Lines" in payloads else None,export_edges=True)
        except Exception as e:result["grid_error"]={"type":type(e).__name__,"message":str(e)[:160]}
    if "CORDIS" in payloads:
        try:result["cordis_bulk_profile"]=cordis_bulk_stats(payloads["CORDIS"])
        except Exception as e:result["cordis_bulk_profile"]={"status":"PARSE_FAILED","type":type(e).__name__,"message":str(e)[:170]}
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
