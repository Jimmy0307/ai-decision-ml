"""Sub-agent A: independent recomputation from raw V9 rows (read-only).
Usage: python -I reproduce_checks.py <V9_dir>
"""
import csv, hashlib, json, os, sys
from collections import Counter

V9 = sys.argv[1]
out = {}


def rows(name):
    with open(os.path.join(V9, name), encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def sha_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb.get(k, 0) for k in ca) / (n * n)
    return (po - pe) / (1 - pe) if pe != 1 else None


first = rows("FIRST_CODER_50_FINAL_FROZEN.csv")
blind = rows("BLIND_REPEAT_20_FINAL_FROZEN.csv")
rec = rows("HUMAN_RECONCILED_20.csv")
out["first_n"] = len(first)
out["first_unique"] = len({r["record_id"] for r in first})
out["first_status"] = dict(Counter(r["review_status"] for r in first))
out["first_coder_ids"] = dict(Counter(r["coder_id"] for r in first))
out["first_ts_range"] = [min(r["coder_timestamp"] for r in first), max(r["coder_timestamp"] for r in first)]
out["blind_n"] = len(blind)
out["blind_unique"] = len({r["record_id"] for r in blind})
out["blind_status"] = dict(Counter(r["review_status"] for r in blind))
out["blind_coder_ids"] = dict(Counter(r["coder_id"] for r in blind))
out["blind_ts_range"] = [min(r["coder_timestamp"] for r in blind), max(r["coder_timestamp"] for r in blind)]
fid = {r["record_id"]: r for r in first}
out["blind_subset_of_first"] = all(r["record_id"] in fid for r in blind)

F = ["human_evidence_valid", "human_relation_type", "human_ai_family", "human_decision_family", "human_include"]
rel = {}
dis_records = 0
for r in blind:
    f = fid[r["record_id"]]
    if any(f[k] != r[k] for k in F):
        dis_records += 1
for k in F:
    a = [fid[r["record_id"]][k] for r in blind]
    b = [r[k] for r in blind]
    rel[k] = {"exact": sum(x == y for x, y in zip(a, b)), "n": len(a), "kappa": round(kappa(a, b), 4)}
out["pre_adjudication_reliability_recomputed"] = rel
out["records_with_any_disagreement"] = dis_records
conf = sum(fid[r["record_id"]]["coder_confidence"] == r["coder_confidence"] for r in blind)
out["confidence_exact"] = conf

# reconciled
out["reconciled_n"] = len(rec)
out["reconciled_unique"] = len({r["record_id"] for r in rec})
out["reconciled_final_populated"] = sum(all(r[f"FINAL_C{i}"] for i in range(1, 6)) for r in rec)
out["reconciled_with_event"] = sum(bool(r["RECONCILIATION_EVENT_ID"]) for r in rec)
out["reconciled_basis"] = dict(Counter(r["RESOLUTION_BASIS"] for r in rec))
# do FIRST_/BLIND_ columns equal frozen snapshots?
mism = 0
bid = {r["record_id"]: r for r in blind}
for r in rec:
    for i, k in enumerate(F, 1):
        if r[f"FIRST_C{i}"] != fid[r["record_id"]][k] or r[f"BLIND_C{i}"] != bid[r["record_id"]][k]:
            mism += 1
out["reconciled_original_columns_mismatch_vs_frozen"] = mism
ev = [json.loads(l) for l in open(os.path.join(V9, "HUMAN_RECONCILIATION_EVENTS.jsonl"), encoding="utf-8") if l.strip()]
out["events_n"] = len(ev)
out["events_types"] = dict(Counter(e["event_type"] for e in ev))
out["events_researcher_ids"] = dict(Counter(e.get("researcher_id") for e in ev))
out["events_ts_range"] = [min(e["timestamp_utc"] for e in ev), max(e["timestamp_utc"] for e in ev)]
link_ok = all(ev[i]["previous_event_hash"] == ev[i - 1]["current_event_hash"] for i in range(1, len(ev)))
out["events_prev_link_ok"] = link_ok
# try to reproduce current_event_hash
def tryhash(e):
    body = {k: v for k, v in e.items() if k != "current_event_hash"}
    cands = {
        "sorted_compact": json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False),
        "sorted_compact_ascii": json.dumps(body, sort_keys=True, separators=(",", ":")),
        "sorted_default": json.dumps(body, sort_keys=True, ensure_ascii=False),
    }
    return {k: hashlib.sha256(v.encode("utf-8")).hexdigest().upper() == e["current_event_hash"].upper() for k, v in cands.items()}
out["event_hash_formula_reproduced"] = Counter(k for e in ev for k, ok in tryhash(e).items() if ok)
evmap = {e["event_id"]: e for e in ev}
out["reconciled_event_hash_match"] = sum(
    1 for r in rec if r["RECONCILIATION_EVENT_ID"] and evmap.get(r["RECONCILIATION_EVENT_ID"], {}).get("current_event_hash", "").upper() == r["RECONCILIATION_EVENT_HASH"].upper())

# epoch2 chain
e2 = rows("HUMAN_AUDIT_EPOCH2_LOG.csv")
gen = sha_file(os.path.join(V9, "HUMAN_AUDIT_EPOCH2_GENESIS.md")).upper()
prev = gen
ok = True
for r in e2:
    ok &= r["previous_event_hash"].upper() == prev
    prev = r["current_event_hash"].upper()
out["epoch2_prev_link_ok_from_genesis_file_hash"] = ok

# sensitivity
s = rows("ROBUST_CORE_LOCAL_SENSITIVITY.csv")
T = lambda v: str(v).strip().lower() in ("true", "1", "yes")
out["sens_cells"] = len(s)
out["sens_official_core"] = sum(T(r["official_core_member"]) for r in s)
out["sens_sidecar_core"] = sum(T(r["sidecar_core_member"]) for r in s)
out["sens_official_core_dirs"] = dict(Counter(r["official_core_direction"] for r in s if T(r["official_core_member"])))
out["sens_sidecar_core_dirs"] = dict(Counter(r["sidecar_core_direction"] for r in s if T(r["sidecar_core_member"])))
out["sens_membership_changed"] = [(r["ai_family"], r["decision_family"], r["official_core_member"], r["sidecar_core_member"], r["official_core_direction"], r["sidecar_core_direction"]) for r in s if T(r["core_membership_changed"])]
out["sens_obs_changed"] = sum(r["official_observed"] != r["sidecar_observed"] for r in s)
out["sens_main_dir_changed"] = sum(T(r["main_direction_changed"]) for r in s)
out["sens_main_q05"] = [sum(T(r["official_main_q05"]) for r in s), sum(T(r["sidecar_main_q05"]) for r in s)]

# V9_1 output manifest
v91 = os.path.join(V9, "V9_1_SEGMENTATION_SENSITIVITY")
res = Counter()
bad = []
with open(os.path.join(v91, "V9_1_OUTPUT_SHA256.csv"), encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        p = os.path.join(v91, r["relative_path"])
        if not os.path.exists(p):
            res["MISSING"] += 1; bad.append(r["relative_path"]); continue
        if sha_file(p) == r["sha256"].lower():
            res["MATCH"] += 1
        else:
            res["MISMATCH"] += 1; bad.append(r["relative_path"])
out["v9_1_output_manifest"] = dict(res)
out["v9_1_output_manifest_bad"] = bad
print(json.dumps(out, indent=1, ensure_ascii=False, default=str))

# appended: epoch2 current_event_hash formula check (sha256 of sorted compact JSON of all other fields)
_e2 = rows("HUMAN_AUDIT_EPOCH2_LOG.csv")
print("epoch2_current_hash_reproduced", sum(
    hashlib.sha256(json.dumps({k: v for k, v in r.items() if k != "current_event_hash"}, sort_keys=True,
                              separators=(",", ":"), ensure_ascii=False).encode()).hexdigest().upper()
    == r["current_event_hash"].upper() for r in _e2), "/", len(_e2))
print("sens_core_direction_changed", sum(r["core_direction_changed"].upper() == "YES" for r in s))

# appended: model-vs-human reproduction (model columns from frozen first-coder file)
print("model_vs_first50", {
    "relation": sum(r["model_relation_type"] == r["human_relation_type"] for r in first),
    "ai_family": sum(r["current_ai_family"] == r["human_ai_family"] for r in first),
    "decision_family": sum(r["current_decision_family"] == r["human_decision_family"] for r in first),
    "inclusion_pairs": dict(Counter((r["model_analytical_pair_eligible"], r["human_include"]) for r in first)),
    "strata": dict(Counter(r["stratum"] for r in first))})
print("model_vs_reconciled20", {
    "relation": sum(fid[r["record_id"]]["model_relation_type"] == r["FINAL_C2"] for r in rec),
    "ai_family": sum(fid[r["record_id"]]["current_ai_family"] == r["FINAL_C3"] for r in rec),
    "decision_family": sum(fid[r["record_id"]]["current_decision_family"] == r["FINAL_C4"] for r in rec),
    "final_c5": dict(Counter(r["FINAL_C5"] for r in rec))})
