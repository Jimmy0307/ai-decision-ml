#!/usr/bin/env python3
"""Real-data feasibility analysis of bounded Github Actions source acquisition.

Only observed CORDIS consortium affiliations/funding and upstream source profiles
are empirical. Burt metrics on consortium one-mode projections are diagnostics,
NOT evidence of social brokerage. MLP models in poc.py remain synthetic.
"""
import argparse
import collections
import csv
import itertools
import json
import math
import statistics
from pathlib import Path

def money(x):
    if x is None or str(x).strip()=="":
        return None
    s=str(x).replace(" ","").replace("\u00a0","")
    if "." in s and "," in s:
        s=s.replace(".","").replace(",",".") if s.rfind(",")>s.rfind(".") else s.replace(",","")
    elif "," in s:
        s=s.replace(",",".")
    try:
        v=float(s)
        return v if math.isfinite(v) else None
    except ValueError:
        return None

def summary(xs):
    vals=sorted(float(x) for x in xs if x is not None and math.isfinite(float(x)))
    if not vals:
        return {"n":0}
    n=len(vals)
    return {"n":n,"min":vals[0],"median":statistics.median(vals),
            "mean":statistics.mean(vals),"max":vals[-1],"sum":sum(vals)}

def eligible_grade(data):
    sources=data.get("source_status",{})
    p=data.get("cordis_bulk_profile") or {}
    out={}
    checks={
     "CORDIS_H2020":{"acquired":sources.get("CORDIS",{}).get("status")=="FETCHED",
       "join":p.get("status")=="BOUNDED_BULK_READ_SUCCESS" and
          p.get("organisation_rows")==p.get("organisation_rows_with_matched_project_id"),
       "follower_allocations":bool((p.get("exploratory_ai_decision") or {}).get("derived_allocations")),
       "follower_utilities":False},
     "OpenAlex":{"acquired":sources.get("OpenAlex",{}).get("status")=="FETCHED",
       "cordis_identity_linkage":False,"following_outcomes_traced":False},
     "OCDS_REAL_UK":{"acquired":sources.get("OCDS_REAL_UK",{}).get("status")=="FETCHED_PARSED",
       "observed_bidders":(sources.get("OCDS_REAL_UK",{}).get("parsed") or {}).get("tenderer_count_observed",0)>0,
       "private_costs":False},
     "GLEIF":{"acquired":sources.get("GLEIF",{}).get("status")=="FETCHED",
       "parent_relation_verified":False,"ai_budget_authority_observed":False},
     "SEC_EDGAR":{"acquired":sources.get("SEC",{}).get("status")=="FETCHED",
       "genuine_contact_configured":False,"enterprise_ai_allocation_observed":False},
     "PyPSA_EUR_GRIDKIT":{"acquired":all(sources.get(x,{}).get("status")=="FETCHED"
                        for x in ("PyPSA_AC_Lines","PyPSA_DC_Links","PyPSA_Transformers")),
       "physical_topology_parsed":bool(data.get("grid_stats",{}).get("ac_lines_included")),
       "power_load_or_dispatch_observed":False,
       "enterprise_ai_decisions_observed":False},
    }
    for key,flags in checks.items():
        out[key]={"checks":flags,"all_required_mlp_observed":False,
                  "verdict":"FEASIBILITY_OR_PARTIAL_SCHEMA_ONLY"}
    return out

def profile_cordis(p):
    expl=p.get("exploratory_ai_decision") or {}
    edges=expl.get("derived_affiliations") or []
    allocation=expl.get("derived_allocations") or []
    metadata=expl.get("selected_project_metadata") or {}
    projects=collections.defaultdict(set)
    org_projects=collections.defaultdict(set)
    for r in edges:
        pid,oid=str(r["project_id"]),str(r["organisation_id"])
        projects[pid].add(oid);org_projects[oid].add(pid)
    pair_count=collections.Counter()
    for nodes in projects.values():
        if len(nodes)>250:
            continue
        pair_count.update(itertools.combinations(sorted(nodes),2))
    neighbors=collections.defaultdict(set)
    for (a,b) in pair_count:
        neighbors[a].add(b);neighbors[b].add(a)
    broker=[]
    for org,ns in neighbors.items():
        k=len(ns)
        if not k:continue
        triangles=sum(len(ns&neighbors[j]) for j in ns)/2
        constraint=0
        for j in ns:
            indirect=sum(1/(k*len(neighbors[q])) for q in ns&neighbors[j])
            constraint+=(1/k+indirect)**2
        broker.append({"org_id":org,"degree":k,"project_count":len(org_projects[org]),
                       "constraint":constraint,"effective_size":k-2*triangles/k,
                       "alter_alter_edges":int(triangles)})
    broker.sort(key=lambda r:r["constraint"])
    single=[x for x in broker if x["project_count"]==1]
    multi=[x for x in broker if x["project_count"]>=2]
    role_counts=collections.Counter(str(r.get("role") or "").lower() for r in allocation)
    funding_cols=("ecContribution","netEcContribution","totalCost")
    funding_missing={k:sum(money(r.get(k)) is None for r in allocation) for k in funding_cols}
    by_project=collections.defaultdict(list)
    for r in allocation:
        by_project[str(r["project_id"])].append(r)
    funding_reconciliation=[]
    for pid,rows in by_project.items():
        meta=metadata.get(pid,{})
        project_ec=money(meta.get("ecMaxContribution"))
        project_cost=money(meta.get("totalCost"))
        ec=[money(r.get("ecContribution")) for r in rows]
        costs=[money(r.get("totalCost")) for r in rows]
        net=[money(r.get("netEcContribution")) for r in rows]
        coords=[r for r in rows if "coordinator" in str(r.get("role") or "").lower()]
        if project_ec is not None and all(x is not None for x in ec):
            ec_gap=sum(ec)-project_ec
            ec_ratio=ec_gap/project_ec if project_ec else None
        else:
            ec_gap=ec_ratio=None
        if project_cost is not None and all(x is not None for x in costs):
            cost_gap=sum(costs)-project_cost
            cost_ratio=cost_gap/project_cost if project_cost else None
        else:
            cost_gap=cost_ratio=None
        ec_positive=[x for x in ec if x is not None and x>0]
        ec_total=sum(x for x in ec if x is not None)
        hhi=sum((x/ec_total)**2 for x in ec if x is not None) if ec_total>0 else None
        funding_reconciliation.append({
            "project_id":pid,"organizations":len({r["organisation_id"] for r in rows}),
            "coordinator_rows":len(coords),"ec_max":project_ec,
            "project_total_cost":project_cost,"participant_ec_total":sum(ec) if all(x is not None for x in ec) else None,
            "participant_cost_total":sum(costs) if all(x is not None for x in costs) else None,
            "participant_net_ec_total":sum(net) if all(x is not None for x in net) else None,
            "ec_relative_gap":ec_ratio,"ec_absolute_gap":ec_gap,
            "cost_relative_gap":cost_ratio,"cost_absolute_gap":cost_gap,
            "participant_ec_hhi":hhi,
            "participants_missing_ec":sum(x is None for x in ec),
            "participants_missing_cost":sum(x is None for x in costs)})
    ec_comparable=[r for r in funding_reconciliation if r["ec_relative_gap"] is not None]
    cost_comparable=[r for r in funding_reconciliation if r["cost_relative_gap"] is not None]
    project_yrs=collections.Counter((r.get("startDate") or "MISSING")[:4] for r in metadata.values())
    return {
      "scope":"OBSERVED_CONSORTIUM_FUNDING_AND_PROJECTED_NETWORK_ONLY",
      "cordis_same_source_publication_links":p.get("publication_profile"),
      "full_h2020":{"project_rows":p.get("project_rows"),
                    "organisation_rows":p.get("organisation_rows"),
                    "unique_organisations":p.get("unique_participant_organisation_ids"),
                    "project_id_join_fraction":
                    p.get("organisation_rows_with_matched_project_id",0)/max(1,p.get("organisation_rows",0)),
                    "full_org_funding_missing":p.get("full_organisation_funding_missing")},
      "selected_keyword":{"projects":len(metadata),"participation_edges":len(edges),"allocation_rows":len(allocation),
          "alternate_with_topics_and_keywords":expl.get("joint_ai_decision_projects_including_topics_keywords"),
          "additional_candidates_from_topics_and_keywords":expl.get("selection_added_only_by_topics_keywords"),
          "projects_with_participants":len(projects),"unique_organisations":len(org_projects),
          "project_start_year_counts":dict(sorted(project_yrs.items())),
          "affiliation_project_size":summary(map(len,projects.values())),
          "project_count_per_organisation":summary(map(len,org_projects.values())),
          "project_ec_max":summary(money(x.get("ecMaxContribution")) for x in metadata.values()),
          "project_total_cost":summary(money(x.get("totalCost")) for x in metadata.values()),
          "funding_missing_rows":funding_missing,
          "funding_missing_share":{k:v/max(1,len(allocation)) for k,v in funding_missing.items()},
          "coordinator_role_counts":dict(role_counts),
          "coordinator_rows_by_project":dict(collections.Counter(str(r["project_id"]) for r in allocation
                                                    if "coordinator" in str(r.get("role") or "").lower()))},
      "reconciliation":{"projects":len(funding_reconciliation),"ec_comparable_projects":len(ec_comparable),
          "cost_comparable_projects":len(cost_comparable),
          "ec_abs_relative_gap":summary(abs(r["ec_relative_gap"]) for r in ec_comparable),
          "cost_abs_relative_gap":summary(abs(r["cost_relative_gap"]) for r in cost_comparable),
          "ec_gap_le_1percent":sum(abs(r["ec_relative_gap"])<=.01 for r in ec_comparable),
          "ec_gap_gt_5percent":sum(abs(r["ec_relative_gap"])>.05 for r in ec_comparable),
          "cost_gap_le_1percent":sum(abs(r["cost_relative_gap"])<=.01 for r in cost_comparable),
          "cost_gap_gt_5percent":sum(abs(r["cost_relative_gap"])>.05 for r in cost_comparable),
          "allocation_ec_hhi":summary(r["participant_ec_hhi"] for r in funding_reconciliation),
          "warning":"EC contribution and cost are recorded funding allocations, NOT measured followers' utilities or leader objectives"},
      "projected_graph":{"nodes_with_incident_links":len(neighbors),"all_organisations":len(org_projects),
          "one_mode_edges":len(pair_count),
          "edges_shared_by_two_or_more_projects":sum(k>=2 for k in pair_count.values()),
          "degree":summary(x["degree"] for x in broker),
          "constraint":summary(x["constraint"] for x in broker),
          "single_project_orgs":len(single),"multi_project_orgs":len(multi),
          "constraint_single_project":summary(x["constraint"] for x in single),
          "constraint_multi_project":summary(x["constraint"] for x in multi),
          "top_ten_low_constraint":broker[:10],
          "warning":"Burt scores are calculated on automatically clique-projected co-membership edges, not confirmed bilateral information ties; degree/size confounding and selection bias remain."
      },
      "readiness":{"leader_coordinator_role":True,"observed_follower_funding_allocations":bool(allocation),
                   "observed_follower_actions":False,"observed_follower_preferences_or_utilities":False,
                   "identifiable_stackelberg_equilibrium":False,
                   "can_calibrate_resource_shares":len(ec_comparable)>0}
    }

def openalex_award_linkage(project_ids, batch_size=40, max_batches=6):
    """Explicit award-ID match against OpenAlex: bounded API, no fuzzy names.

    Work grants list under \`awards\` in current OpenAlex schema. Any unmatched
    ID is UNKNOWN (possible missing index), NOT evidence of no publications.
    """
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode
    import hashlib
    ids=sorted({str(x).strip() for x in project_ids if str(x).strip()})
    if len(ids)>240:
        raise ValueError("Too many grant ids for bounded crosslink")
    summary={"status":"ATTEMPTED","input_project_ids":len(ids),
             "award_record_matches":0,"works_matched_records":0,
             "matched_grant_ids":[],"grant_work_links":[],
             "queries":[],"errors":[],
             "warning":"Award match is a metadata linkage, not a verified independent collaboration or publication causal effect."}
    if not ids:
        summary["status"]="NO_PROJECT_IDS"
        return summary
    def pull(url):
        with urlopen(Request(url,headers={"User-Agent":"Academic research methods reproduction/1.0"}),timeout=40) as resp:
            blob=resp.read(2_000_001)
        if len(blob)>2_000_000:
            raise ValueError("bounded_openalex_response_limit")
        return json.loads(blob),hashlib.sha256(blob).hexdigest(),len(blob)
    for start in range(0,len(ids),batch_size):
        if start//batch_size>=max_batches:
            summary["errors"].append("BATCH_LIMIT")
            break
        block=ids[start:start+batch_size]
        for typ in ("awards","works"):
            if typ=="awards":
                filt="funder_award_id:"+"|".join(block)
            else:
                filt="awards.funder_award_id:"+"|".join(block)
            url="https://api.openalex.org/"+typ+"?"+urlencode({"filter":filt,"per_page":"100"})
            try:
                obj,sha,size=pull(url)
                found=obj.get("results") or []
                metadata={"entity":typ,"input_ids":len(block),"count_returned":len(found),
                          "api_reported_total":(obj.get("meta") or {}).get("count"),
                          "response_sha256":sha,"response_bytes":size,"query_url":url,
                          "response_truncated":((obj.get("meta") or {}).get("count") or 0)>len(found)}
                summary["queries"].append(metadata)
                if typ=="awards":
                    summary["award_record_matches"]+=len(found)
                    for a in found:
                        gid=str(a.get("funder_award_id") or "")
                        if gid in block:
                            summary["matched_grant_ids"].append(gid)
                            summary["grant_work_links"].append(
                                {"grant_id":gid,"openalex_award_id":a.get("id"),
                                 "reported_funded_outputs_count":a.get("funded_outputs_count"),
                                 "works_api_url":a.get("works_api_url")})
                else:
                    summary["works_matched_records"]+=len(found)
                    for w in found:
                        awards=w.get("awards") or []
                        for a in awards:
                            gid=str(a.get("funder_award_id") or "")
                            if gid in block:
                                summary["grant_work_links"].append(
                                   {"grant_id":gid,"openalex_work_id":w.get("id"),"doi":w.get("doi"),
                                    "publication_year":w.get("publication_year")})
            except Exception as e:
                summary["errors"].append({"entity":typ,"input_ids":len(block),
                                          "error":type(e).__name__,"message":str(e)[:150]})
    summary["matched_grant_ids"]=sorted(set(summary["matched_grant_ids"]))
    summary["status"]="COMPLETE_BOUNDED" if not summary["errors"] else "PARTIAL_BOUNDED"
    return summary

def assess(data):
    p=data.get("cordis_bulk_profile") or {}
    result={"schema":"ai-decision-external-dataset-round2/1.0",
      "source_run_timestamp":data.get("timestamp"),
      "source_mode":data.get("mode"),
      "source_status":{k:{"status":v.get("status"),"sha256":v.get("sha256"),
                            "size_bytes":v.get("size_bytes"),"parsed":v.get("parsed")}
                         for k,v in (data.get("source_status") or {}).items()},
      "readiness":eligible_grade(data),
      "grid_stats":data.get("grid_stats"),
      "toy_mlp":data.get("toy_mlp"),
      "toy_gne":data.get("toy_gne"),
      "decision":"RESEARCH_FEASIBILITY_ONLY_NO_CONFIRMED_BURT_OR_EMPIRICAL_MLP"}
    if p.get("status")=="BOUNDED_BULK_READ_SUCCESS":
        result["cordis"]=profile_cordis(p)
    return result

def main():
    arg=argparse.ArgumentParser()
    arg.add_argument("--input",required=True)
    arg.add_argument("--output",required=True)
    arg.add_argument("--openalex-awards",action="store_true")
    x=arg.parse_args()
    data=json.loads(Path(x.input).read_text(encoding="utf-8"))
    out=assess(data)
    if x.openalex_awards and out.get("cordis"):
        out["openalex_grant_linkage"]=openalex_award_linkage(
            (data.get("cordis_bulk_profile",{}).get("exploratory_ai_decision",{})
               .get("selected_project_metadata") or {}).keys())
    p=Path(x.output);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(p),"decision":out["decision"],
      "source_status":{k:v["status"] for k,v in out["source_status"].items()},
      "cordis_projects":out.get("cordis",{}).get("selected_keyword",{}).get("projects"),
      "ec_comparable":out.get("cordis",{}).get("reconciliation",{}).get("ec_comparable_projects")},ensure_ascii=False))
if __name__=="__main__":main()
