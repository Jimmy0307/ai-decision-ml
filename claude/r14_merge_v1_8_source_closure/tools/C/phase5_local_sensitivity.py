"""Phase 5 (sub-agent C): reproduce local robust-core sensitivity from raw CSV rows.
Usage: python -I phase5_local_sensitivity.py <W root>
Read-only; prints JSON to stdout.
"""
import csv, json, sys, hashlib
from pathlib import Path

W = Path(sys.argv[1])
V9 = W / "02_V9_HUMAN_VALIDATION" / "20260929_V9_HUMAN_VALIDATION"
R17 = W / "01_ALL_OUTPUTS" / "AI_DECISION_THESIS_ALL_OUTPUTS" / "r14_merge_v1_7"


def rows(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


out = {}
full = rows(V9 / "ROBUST_CORE_LOCAL_SENSITIVITY.csv")
diff = rows(V9 / "ROBUST_CORE_LOCAL_SENSITIVITY_DIFF.csv")
out["sha256"] = {n: sha(V9 / n) for n in [
    "ROBUST_CORE_LOCAL_SENSITIVITY.csv", "ROBUST_CORE_LOCAL_SENSITIVITY_DIFF.csv",
    "ROBUST_CORE_LOCAL_SENSITIVITY_STATUS.json", "ROBUST_CORE_LOCAL_SENSITIVITY.md",
    "ROBUST_CORE_IMPACT_SCREEN_50.csv", "REANALYSIS_CANDIDATES_FROM_HUMAN_AUDIT.csv",
    "HUMAN_RECONCILED_20.csv", "FIRST_CODER_50_FINAL_FROZEN.csv"]}
out["n_rows_full"] = len(full)
out["n_unique_cells"] = len({(r["ai_family"], r["decision_family"]) for r in full})
out["n_rows_diff"] = len(diff)

key = lambda r: f'{r["ai_family"]} x {r["decision_family"]}'
off = {key(r): r["official_core_direction"] for r in full if r["official_core_member"] == "YES"}
sc = {key(r): r["sidecar_core_direction"] for r in full if r["sidecar_core_member"] == "YES"}
out["official_core_n"] = len(off)
out["sidecar_core_n"] = len(sc)
cnt = lambda d, v: sum(1 for x in d.values() if x == v)
out["official_enriched_depleted"] = [cnt(off, "ENRICHED"), cnt(off, "DEPLETED")]
out["sidecar_enriched_depleted"] = [cnt(sc, "ENRICHED"), cnt(sc, "DEPLETED")]
out["gained"] = {k: sc[k] for k in sorted(set(sc) - set(off))}
out["lost"] = {k: off[k] for k in sorted(set(off) - set(sc))}
common = set(off) & set(sc)
out["common_n"] = len(common)
out["common_direction_changes"] = [k for k in common if off[k] != sc[k]]
out["official_core"] = dict(sorted(off.items()))

# recompute structural-core rule from q-values to check member flags
def member(r, side):
    meths = ["main", "exact", "document"]
    qs = [float(r[f"{side}_{m}_q"]) for m in meths]
    dirs = {r[f"{side}_{m}_direction"] for m in meths}
    raw_ok = float(r[f"{side}_raw_q"]) <= .05 and r[f"{side}_raw_direction"] in dirs and len(dirs) == 1
    return all(q <= .05 for q in qs) and len(dirs) == 1, raw_ok

mism = []
for r in full:
    for side in ("official", "sidecar"):
        s3, raw = member(r, side)
        flag = r[f"{side}_core_member"] == "YES"
        if flag != (s3 and raw):
            mism.append((key(r), side, s3, raw, flag))
out["member_flag_vs_recomputed_rule_mismatches"] = mism

# diff classification
cls = {"core_membership_changed": 0, "main_direction_changed": 0, "observed_count_changed": 0,
       "core_direction_changed": 0}
for r in diff:
    cls["core_membership_changed"] += r["core_membership_changed"] == "YES"
    cls["main_direction_changed"] += r["main_direction_changed"] == "YES"
    cls["observed_count_changed"] += r["observed_count_delta"] != "0"
    cls["core_direction_changed"] += r["core_direction_changed"] == "YES"
out["diff_classes"] = cls
out["diff_rows_main_direction_changed"] = [key(r) for r in diff if r["main_direction_changed"] == "YES"]
# diff rows also present in full with identical values?
fullmap = {key(r): r for r in full}
out["diff_rows_identical_to_full"] = all(fullmap[key(r)] == r for r in diff)
# full-file counts
out["full_counts"] = {
    "observed_count_changed": sum(r["observed_count_delta"] != "0" for r in full),
    "main_direction_changed": sum(r["main_direction_changed"] == "YES" for r in full),
    "core_membership_changed": sum(r["core_membership_changed"] == "YES" for r in full),
    "sum_observed_official": sum(int(r["official_observed"]) for r in full),
    "sum_observed_sidecar": sum(int(r["sidecar_observed"]) for r in full),
    "sum_document_official": sum(int(r["official_document_observed"]) for r in full),
    "sum_document_sidecar": sum(int(r["sidecar_document_observed"]) for r in full),
    "sum_raw_official": sum(int(r["official_raw_observed"]) for r in full),
    "sum_raw_sidecar": sum(int(r["sidecar_raw_observed"]) for r in full),
    "official_main_q05": sum(r["official_main_q05"] == "True" for r in full),
    "sidecar_main_q05": sum(r["sidecar_main_q05"] == "True" for r in full),
    "official_main_q01": sum(r["official_main_q01"] == "True" for r in full),
    "sidecar_main_q01": sum(r["sidecar_main_q01"] == "True" for r in full),
}
# sha of core lists (try several canonical serialisations against status json)
status = json.loads((V9 / "ROBUST_CORE_LOCAL_SENSITIVITY_STATUS.json").read_text(encoding="utf-8"))
out["status_hashes"] = [status["official_core_sha256"], status["sidecar_core_sha256"]]

# G01-G16 from 132
g = rows(R17 / "132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX.csv")
gl = []
for r in g:
    pair = f'{r["AI family"]} x {r["Decision family"]}'
    gl.append({"G": r["G ID"], "pair": pair, "O_132": r["O (doc-level edges)"],
               "official_core": off.get(pair), "sidecar_core": sc.get(pair),
               "official_document_observed": fullmap.get(pair, {}).get("official_document_observed"),
               "sidecar_document_observed": fullmap.get(pair, {}).get("sidecar_document_observed"),
               "official_main_observed": fullmap.get(pair, {}).get("official_observed"),
               "sidecar_main_observed": fullmap.get(pair, {}).get("sidecar_observed")})
out["G01_G16"] = gl
gpairs = {x["pair"] for x in gl}
offdep = {k for k, v in off.items() if v == "DEPLETED"}
out["G_set_equals_official_depleted"] = gpairs == offdep
out["G_minus_official_depleted"] = sorted(gpairs - offdep)
out["official_depleted_minus_G"] = sorted(offdep - gpairs)
out["G_removed_in_sidecar"] = sorted(p for p in gpairs if p not in sc)

# label changes: 20 reconciled -> FINAL_*, 30 others -> first-coder
fc = rows(V9 / "FIRST_CODER_50_FINAL_FROZEN.csv")
rec = {r["record_id"]: r for r in rows(V9 / "HUMAN_RECONCILED_20.csv")}
changes = []
for r in fc:
    rid = r["record_id"]
    model = {"evidence/inclusion": r["model_analytical_pair_eligible"],
             "ai_family": r["current_ai_family"], "decision_family": r["current_decision_family"]}
    if rid in rec:
        h = rec[rid]
        src = "RECONCILED_FINAL"
        hum = {"inclusion(C5)": h["FINAL_C5"], "ai_family": h["FINAL_C3"], "decision_family": h["FINAL_C4"],
               "validity(C1)": h["FINAL_C1"]}
    else:
        src = "FIRST_CODER"
        hum = {"inclusion(C5)": r["human_include"], "ai_family": r["human_ai_family"],
               "decision_family": r["human_decision_family"], "validity(C1)": r["human_evidence_valid"]}
    changes.append({"record_id": rid, "validation_id": r["validation_id"], "source": src,
                    "model_eligible": model["evidence/inclusion"],
                    "model_ai": model["ai_family"], "model_dec": model["decision_family"],
                    "human_C1": hum["validity(C1)"], "human_C5": hum["inclusion(C5)"],
                    "human_ai": hum["ai_family"], "human_dec": hum["decision_family"]})
out["n_first_coder_rows"] = len(fc)
out["n_reconciled"] = len(rec)
out["reconciled_ids_in_first50"] = sum(1 for r in fc if r["record_id"] in rec)
out["label_rows"] = changes
print(json.dumps(out, ensure_ascii=False, indent=1))
