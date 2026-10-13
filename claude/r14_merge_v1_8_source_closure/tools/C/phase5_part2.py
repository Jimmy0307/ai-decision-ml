"""Phase 5 part 2: core-hash reproduction attempts, label-change list, segmentation-scope overlap.
Usage: python -I phase5_part2.py <W root> <phase5_out.json>
"""
import csv, json, sys, hashlib, itertools
from pathlib import Path

W = Path(sys.argv[1]); d = json.load(open(sys.argv[2], encoding="utf-8"))
V9 = W / "02_V9_HUMAN_VALIDATION" / "20260929_V9_HUMAN_VALIDATION"
SEG = V9 / "V9_1_SEGMENTATION_SENSITIVITY"


def rows(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

res = {}
# --- hash attempts
full = rows(V9 / "ROBUST_CORE_LOCAL_SENSITIVITY.csv")
targets = set(d["status_hashes"])
def cores(side):
    return sorted((r["ai_family"], r["decision_family"], r[f"{side}_core_direction"]) for r in full if r[f"{side}_core_member"] == "YES")
found = {}
for side in ("official", "sidecar"):
    c = cores(side)
    cands = {}
    for sep in (" x ", " × ", "|", ",", "\t", "::"):
        for withdir in (True, False):
            items = [(f"{a}{sep}{b}" + (f"{sep}{dd}" if withdir else "")) for a, b, dd in c]
            for joiner in ("\n", ",", "|", ""):
                for trail in ("", "\n"):
                    cands[f"sep={sep!r},dir={withdir},join={joiner!r},trail={trail!r}"] = joiner.join(items) + trail
    cands["json_list_pairs"] = json.dumps([[a, b] for a, b, _ in c])
    cands["json_list_triples"] = json.dumps([[a, b, dd] for a, b, dd in c])
    cands["json_list_triples_compact"] = json.dumps([[a, b, dd] for a, b, dd in c], separators=(",", ":"))
    cands["json_dicts"] = json.dumps([{"ai_family": a, "decision_family": b, "direction": dd} for a, b, dd in c], sort_keys=True)
    cands["json_dicts_compact"] = json.dumps([{"ai_family": a, "decision_family": b, "direction": dd} for a, b, dd in c], sort_keys=True, separators=(",", ":"))
    for k, s in cands.items():
        h = hashlib.sha256(s.encode("utf-8")).hexdigest()
        if h in targets:
            found[side] = k
res["core_hash_reproduced"] = found or "NOT_REPRODUCED_WITH_TRIED_SERIALISATIONS"

# --- label changes
lab = []
for r in d["label_rows"]:
    ch = []
    elig = r["model_eligible"].strip().upper() in ("TRUE", "YES", "1")
    hum_incl = r["human_C5"].upper() == "INCLUDE"
    if elig != hum_incl:
        ch.append(("inclusion", "ELIGIBLE" if elig else "NOT_ELIGIBLE", r["human_C5"]))
    if r["model_ai"] != r["human_ai"]:
        ch.append(("ai_family", r["model_ai"], r["human_ai"]))
    if r["model_dec"] != r["human_dec"]:
        ch.append(("decision_family", r["model_dec"], r["human_dec"]))
    lab.append({**r, "changes": ch})
res["label_change_summary"] = {
    "records": len(lab),
    "records_with_any_change": sum(1 for x in lab if x["changes"]),
    "by_source": {s: sum(1 for x in lab if x["source"] == s and x["changes"]) for s in ("RECONCILED_FINAL", "FIRST_CODER")},
    "field_changes": sum(len(x["changes"]) for x in lab),
}
res["label_changes"] = lab

# compare with impact screen (first-coder based) for the 20 reconciled
scr = {r["record_id"]: r for r in rows(V9 / "ROBUST_CORE_IMPACT_SCREEN_50.csv")}
res["impact_screen_categories"] = {}
for r in scr.values():
    res["impact_screen_categories"][r["impact_screen_category"]] = res["impact_screen_categories"].get(r["impact_screen_category"], 0) + 1
cand = rows(V9 / "REANALYSIS_CANDIDATES_FROM_HUMAN_AUDIT.csv")
res["reanalysis_candidates_n"] = len(cand)
res["reanalysis_candidates_unique"] = len({r["record_id"] for r in cand})
# first-coder vs reconciled differences on the 20
fc = {r["record_id"]: r for r in rows(V9 / "FIRST_CODER_50_FINAL_FROZEN.csv")}
rec = rows(V9 / "HUMAN_RECONCILED_20.csv")
diffs = []
for h in rec:
    f = fc[h["record_id"]]
    pairs = [("C1", f["human_evidence_valid"], h["FINAL_C1"]), ("C3_ai", f["human_ai_family"], h["FINAL_C3"]),
             ("C4_dec", f["human_decision_family"], h["FINAL_C4"]), ("C5_incl", f["human_include"], h["FINAL_C5"])]
    fd = [(k, a, b) for k, a, b in pairs if a != b]
    fd_first_vs_reconciled_first = [(k, a, b) for k, a, b in [("C3", f["human_ai_family"], h["FIRST_C3"]), ("C4", f["human_decision_family"], h["FIRST_C4"]), ("C5", f["human_include"], h["FIRST_C5"])] if a != b]
    diffs.append({"record_id": h["record_id"], "basis": h["RESOLUTION_BASIS"], "ts": h["RECONCILIATION_TIMESTAMP_UTC"],
                  "first_coder_frozen_vs_final": fd, "frozen_first_vs_reconciled_FIRST_cols": fd_first_vs_reconciled_first})
res["reconciled_vs_first"] = diffs
res["reconciliation_ts_range"] = [min(x["ts"] for x in diffs if x["ts"]), max(x["ts"] for x in diffs if x["ts"])]

# --- segmentation overlap
audited = {r["record_id"] for r in d["label_rows"]}
man = rows(SEG / "SEGMENTATION_CANDIDATE_MANIFEST.csv")
mc = {r["record_id"]: r for r in man}
res["seg_manifest_rows"] = len(man)
res["seg_candidates_total"] = sum(r["candidate"] == "True" for r in man)
res["audited_in_manifest"] = sum(1 for a in audited if a in mc)
res["audited_selected_as_candidates"] = sorted(a for a in audited if a in mc and mc[a]["candidate"] == "True")
res["audited_selected_via_human_tag"] = sorted(a for a in audited if a in mc and "HUMAN_AUDIT_ERROR_TAG" in mc[a]["candidate_reasons"])
# do S1/S2 record-level outputs for audited, non-candidate records carry model or human families?
humfam = {r["record_id"]: (r["human_ai"], r["human_dec"]) for r in d["label_rows"]}
modfam = {r["record_id"]: (r["model_ai"], r["model_dec"]) for r in d["label_rows"]}
for v in ("S1", "S2"):
    rl = rows(SEG / f"{v}_ANALYTICAL_FREEZE_RECORD_LEVEL.csv")
    agree_h = agree_m = n = 0
    seen = {}
    for r in rl:
        rid = r.get("original_record_id") or r.get("parent_record_id") or r["record_id"]
        if rid not in audited:
            continue
        if mc.get(rid, {}).get("candidate") == "True":
            continue  # re-segmented records: families re-mapped by model
        n += 1
        fam = (r["left_final_family"], r["right_final_family"])
        famset = set(fam)
        agree_m += set(modfam[rid]) <= famset
        agree_h += set(humfam[rid]) <= famset and modfam[rid] != humfam[rid]
    res[f"{v}_noncandidate_audited_rows"] = n
    res[f"{v}_noncandidate_audited_match_model_families"] = agree_m
    res[f"{v}_noncandidate_audited_match_human_only"] = agree_h
print(json.dumps(res, ensure_ascii=False, indent=1))
