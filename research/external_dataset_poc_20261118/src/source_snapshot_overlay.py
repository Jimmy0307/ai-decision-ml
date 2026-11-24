#!/usr/bin/env python3
"""Overlay prior verified eight-work OpenAlex snapshot if live API rate-limits.

Does not rewrite original live run; returns separate analysis JSON, preserving
cached provenance and failing-live status. Never upgrades source to LIVE.
"""
import argparse
import json
from pathlib import Path

def overlay(data,snapshot):
    result=json.loads(json.dumps(data))
    src=result.setdefault("source_status",{}).setdefault("OpenAlex",{})
    if src.get("status")=="FETCHED" and (src.get("parsed") or {}).get("work_memberships"):
        src["analysis_provenance"]="CURRENT_LIVE_WORK_AUTHORS"
        return result
    works=snapshot.get("work_memberships") or []
    if len(works)!=8:
        raise ValueError("Pinned historical work count differs from eight")
    src["original_fetch_status"]={k:src.get(k) for k in ("status","error","message","size_bytes")}
    src["status"]="CACHED_HISTORICAL_WORK_SAMPLE"
    src["analysis_provenance"]="PRIOR_GITHUB_ACTIONS_ARTIFACT_NOT_NEW_FETCH"
    src["cached_source"]={"run":snapshot["source_run"],
         "raw_sha256":snapshot["raw_response_sha256"],
         "query":snapshot["raw_query"]}
    src["parsed"]={"works":len(works),"authors":len(set(a for w in works for a in w["authors"])),
         "institutions":len(set(i for w in works for i in w["institutions"])),
         "work_memberships":works,"works_with_doi":sum(bool(w["doi"]) for w in works),
         "scope":"HISTORICAL_PUBLIC_API_SAMPLE_ONLY_NOT_CURRENT_OR_CORDIS_LINKED"}
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--live-input",required=True)
    p.add_argument("--snapshot",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    data=json.loads(Path(a.live_input).read_text())
    snap=json.loads(Path(a.snapshot).read_text())
    obj=overlay(data,snap)
    dest=Path(a.output)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"openalex_analysis_provenance":obj["source_status"]["OpenAlex"]["analysis_provenance"],
      "original_status":data.get("source_status",{}).get("OpenAlex",{}).get("status")}))
if __name__=="__main__":main()
