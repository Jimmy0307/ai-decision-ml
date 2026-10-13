"""Phase 7 sub-agent E: row-level verification of V9 values cited by v1.7 flags.
Usage: python -I verify.py <W> <out_json>"""
import sys, os, csv, json, hashlib
from collections import Counter

W = sys.argv[1]
OUT = sys.argv[2]
V9 = os.path.join(W, "02_V9_HUMAN_VALIDATION", "20260929_V9_HUMAN_VALIDATION")
V17 = os.path.join(W, "01_ALL_OUTPUTS", "AI_DECISION_THESIS_ALL_OUTPUTS", "r14_merge_v1_7")
R = {}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def rd(name, base=V9):
    with open(os.path.join(base, name), encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


# ---------------- hash checks
inv = {}
with open(os.path.join(W, "01_FILE_INVENTORY.csv"), encoding="utf-8-sig", newline="") as f:
    for r in csv.DictReader(f):
        inv[(r["source_package"], r["relative_path"])] = r["sha256"].lower()
man = {r["relative_path"]: r["sha256"].lower() for r in rd("FINAL_ARTIFACT_HASH_MANIFEST.csv")}
side = {}
for fn in os.listdir(V9):
    if fn.endswith(".sha256") or fn.endswith("SHA256.txt"):
        for line in open(os.path.join(V9, fn), encoding="utf-8-sig", errors="replace"):
            parts = line.strip().split()
            if len(parts) == 2 and len(parts[0]) == 64:
                side.setdefault(parts[1], set()).add(parts[0].lower())
            if "SHA-256:" in line:
                a, b = line.split("SHA-256:")
                side.setdefault(a.strip(), set()).add(b.strip().lower())
keys = ["FIRST_CODER_50_FINAL_FROZEN.csv", "FIRST_CODER_50_FROZEN.csv", "BLIND_REPEAT_20_FINAL_FROZEN.csv",
        "SECOND_CODER_BLIND_20.csv", "HUMAN_RECONCILED_20.csv", "HUMAN_RELIABILITY_FINAL.csv",
        "HUMAN_DISAGREEMENT_QUEUE_20.csv", "ROBUST_CORE_LOCAL_SENSITIVITY.csv",
        "ROBUST_CORE_LOCAL_SENSITIVITY_DIFF.csv", "ROBUST_CORE_LOCAL_SENSITIVITY_STATUS.json",
        "ROBUST_CORE_LOCAL_SENSITIVITY.md", "FINAL_STATUS.json", "FINAL_ERROR_TAXONOMY.csv",
        "FINAL_ERROR_TAXONOMY_CASES.csv", "HUMAN_DISAGREEMENT_SUMMARY_20.md",
        "V9_1_SEGMENTATION_SENSITIVITY/SEGMENTATION_SENSITIVITY_FINAL_REPORT.md",
        "V9_1_SEGMENTATION_SENSITIVITY/S1_ANALYTICAL_FREEZE_RECORD_LEVEL.csv",
        "V9_1_SEGMENTATION_SENSITIVITY/S2_ANALYTICAL_FREEZE_RECORD_LEVEL.csv"]
hashes = {}
for k in keys:
    p = os.path.join(V9, k)
    if not os.path.exists(p):
        hashes[k] = {"exists": False}
        continue
    s = sha(p)
    iv = inv.get(("02_V9_HUMAN_VALIDATION", "20260929_V9_HUMAN_VALIDATION/" + k))
    hashes[k] = {"exists": True, "sha256": s,
                 "inventory_match": (iv == s) if iv else "NOT_IN_INVENTORY",
                 "final_manifest_match": (man.get(k) == s) if k in man else "NOT_IN_MANIFEST",
                 "sidecar_sha_file_match": (s in side[k]) if k in side else "NO_SIDECAR"}
R["hashes"] = hashes

fs = json.load(open(os.path.join(V9, "FINAL_STATUS.json"), encoding="utf-8"))
R["final_status"] = {
    "first_coder_hash_ok": fs["first_coder"]["snapshot_sha256"] == hashes["FIRST_CODER_50_FINAL_FROZEN.csv"]["sha256"],
    "blind_hash_ok": fs["blind_round"]["snapshot_sha256"] == hashes["BLIND_REPEAT_20_FINAL_FROZEN.csv"]["sha256"],
    "reconciled_hash_ok": fs["reconciliation"]["sha256"] == hashes["HUMAN_RECONCILED_20.csv"]["sha256"],
    "verified_at_utc": fs["verified_at_utc"], "decision_text": fs["decision_text"],
    "submission_ready": fs["submission_ready"], "sensitivity_scope": fs["sensitivity"]["audited_record_scope"],
    "protected_hash_mismatches": fs.get("protected_hash_mismatches")}

# ---------------- counts
HUM = ["human_evidence_valid", "human_relation_type", "human_ai_family", "human_decision_family", "human_include"]
fc = rd("FIRST_CODER_50_FINAL_FROZEN.csv")
br = rd("BLIND_REPEAT_20_FINAL_FROZEN.csv")
rc = rd("HUMAN_RECONCILED_20.csv")
fcd = {r["record_id"]: r for r in fc}
brd = {r["record_id"]: r for r in br}
R["first_coder"] = {"rows": len(fc), "unique_ids": len(fcd),
                    "complete_rows": sum(all(r[c].strip() for c in HUM) for r in fc),
                    "review_status": dict(Counter(r["review_status"] for r in fc))}
R["blind20"] = {"rows": len(br), "unique": len(brd), "complete": sum(all(r[c].strip() for c in HUM) for r in br),
                "subset_of_first50": set(brd) <= set(fcd),
                "review_status": dict(Counter(r["review_status"] for r in br))}


def F(r, p):
    return tuple(r[f"{p}_C{i}"].strip() for i in range(1, 6))


dis = [r for r in rc if F(r, "FIRST") != F(r, "BLIND")]
dis_ids = sorted(r["record_id"] for r in dis)
ts = [r["RECONCILIATION_TIMESTAMP_UTC"] for r in rc if r["RECONCILIATION_TIMESTAMP_UTC"].strip()]
R["reconciled20"] = {
    "rows": len(rc), "unique": len({r["record_id"] for r in rc}),
    "rows_with_any_disagreement": len(dis), "rows_full_agreement": len(rc) - len(dis),
    "final_complete": sum(all(F(r, "FINAL")) for r in rc),
    "rows_with_event_id": sum(bool(r["RECONCILIATION_EVENT_ID"].strip()) for r in rc),
    "timestamp_range": [min(ts), max(ts)] if ts else None,
    "same_ids_as_blind": {r["record_id"] for r in rc} == set(brd),
    "FIRST_matches_frozen_first": all(F(r, "FIRST") == tuple(fcd[r["record_id"]][c].strip() for c in HUM) for r in rc),
    "BLIND_matches_frozen_blind": all(F(r, "BLIND") == tuple(brd[r["record_id"]][c].strip() for c in HUM) for r in rc),
}


def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n / n
    return None if pe >= 1 else (po - pe) / (1 - pe)


kp = {}
for i, c in enumerate(HUM, 1):
    a = [r[f"FIRST_C{i}"].strip() for r in rc]
    b = [r[f"BLIND_C{i}"].strip() for r in rc]
    k = kappa(a, b)
    kp[c] = {"agree": sum(x == y for x, y in zip(a, b)), "n": len(a), "kappa": None if k is None else round(k, 4)}
R["kappa_recomputed_simple_unweighted"] = kp
R["reliability_final_csv"] = {r["field"]: {"agree": r["exact_agreement_count"], "kappa": r["cohens_kappa"]}
                              for r in rd("HUMAN_RELIABILITY_FINAL.csv")}

# ---------------- robust core local sensitivity
sens = rd("ROBUST_CORE_LOCAL_SENSITIVITY.csv")
cell = lambda r: (r["ai_family"], r["decision_family"])
off = {cell(r): r["official_core_direction"] for r in sens if r["official_core_member"] == "YES"}
sid = {cell(r): r["sidecar_core_direction"] for r in sens if r["sidecar_core_member"] == "YES"}
S = {"cells": len(sens), "official_n": len(off), "sidecar_n": len(sid),
     "official_dir": dict(Counter(off.values())), "sidecar_dir": dict(Counter(sid.values())),
     "gained": [f"{k[0]} x {k[1]} ({v})" for k, v in sid.items() if k not in off],
     "lost": [f"{k[0]} x {k[1]} ({v})" for k, v in off.items() if k not in sid],
     "common_n": len(set(off) & set(sid)),
     "common_direction_changes": [k for k in set(off) & set(sid) if off[k] != sid[k]],
     "rows_core_membership_changed_YES": sum(r["core_membership_changed"] == "YES" for r in sens),
     "rows_core_direction_changed_YES": sum(r["core_direction_changed"] == "YES" for r in sens),
     "rows_main_direction_changed_YES": sum(r["main_direction_changed"] == "YES" for r in sens),
     "rows_observed_count_changed": sum(r["observed_count_delta"] not in ("0", "") for r in sens)}
diff = rd("ROBUST_CORE_LOCAL_SENSITIVITY_DIFF.csv")
S["diff_rows"] = len(diff)
S["diff_core_changes"] = [cell(r) for r in diff if "YES" in (r["core_membership_changed"], r["core_direction_changed"])]
for c in [("HUMAN_AUGMENTATION", "RISK_ASSESSMENT"), ("COORDINATION_EXECUTION", "GENERAL_DECISION_PROCESS")]:
    r = next(x for x in sens if cell(x) == c)
    S["cell " + " x ".join(c)] = {k: r[k] for k in [
        "official_observed", "sidecar_observed", "official_main_direction", "official_main_q", "sidecar_main_q",
        "official_exact_q", "sidecar_exact_q", "official_document_observed", "official_document_q",
        "sidecar_document_q", "official_raw_q", "sidecar_raw_q", "official_core_member", "sidecar_core_member"]}
oq = sorted(((float(r["official_main_q"]), " x ".join(cell(r))) for r in sens if r["official_core_member"] == "YES"),
            reverse=True)
S["official_core_largest_main_q_top3"] = oq[:3]
R["sensitivity"] = S

g = rd("132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX.csv", V17)
gset = {(r["AI family"], r["Decision family"]) for r in g}
dep_off = {k for k, v in off.items() if v == "DEPLETED"}
sens_by = {cell(r): r for r in sens}
R["G01_G16"] = {
    "n_rows_132": len(g), "equals_official_depleted_core": gset == dep_off,
    "all_in_sidecar_core": all(k in sid for k in gset),
    "all_depleted_in_sidecar": all(sid.get(k) == "DEPLETED" for k in gset),
    "O_mismatch_vs_V9_official_observed": [(r["G ID"], r["O (doc-level edges)"],
                                           sens_by[(r["AI family"], r["Decision family"])]["official_observed"])
                                          for r in g if r["O (doc-level edges)"] !=
                                          sens_by[(r["AI family"], r["Decision family"])]["official_observed"]]}

# ---------------- error taxonomy vs the 19 human disagreements
tax = rd("FINAL_ERROR_TAXONOMY.csv")
cases = rd("FINAL_ERROR_TAXONOMY_CASES.csv")
case_ids = {r["record_id"] for r in cases}
R["error_taxonomy"] = {
    "categories": len(tax),
    "likely_source_by_type": {r["error_type"]: r["likely_source_interpretation"] for r in tax},
    "likely_source_status": dict(Counter(r["likely_source_status"] for r in tax)),
    "case_unique_records": len(case_ids), "audit_source_values": dict(Counter(r["audit_source"] for r in cases)),
    "disagreement19_ids_with_any_tag": sum(i in case_ids for i in dis_ids), "disagreement19_n": len(dis_ids)}

# ---------------- E49: did the segmentation sidecar use human labels for audited records?
seg = os.path.join(V9, "V9_1_SEGMENTATION_SENSITIVITY")
e49 = {}
for s in ["S1", "S2"]:
    rows = rd(f"{s}_ANALYTICAL_FREEZE_RECORD_LEVEL.csv", seg)
    oid = lambda r: (r.get("original_record_id") or r["record_id"]).strip()
    sub = [r for r in rows if oid(r) in fcd]
    m_eq = h_eq = h_diff_m = 0
    for r in sub:
        f = fcd[oid(r)]
        fam = (r["left_final_family"], r["right_final_family"])
        m_eq += fam == (f["current_ai_family"], f["current_decision_family"])
        h_eq += fam == (f["human_ai_family"], f["human_decision_family"])
        h_diff_m += (f["human_ai_family"], f["human_decision_family"]) != (f["current_ai_family"], f["current_decision_family"])
    e49[s] = {"rows_for_audited_records": len(sub), "audited_records_covered": len({oid(r) for r in sub}),
              "mapping_provenance": dict(Counter(r["mapping_provenance"] for r in sub)),
              "unitization_status": dict(Counter(r["unitization_status"] for r in sub)),
              "families_equal_model_current": m_eq, "families_equal_first_coder_human": h_eq,
              "rows_where_human_differs_from_model": h_diff_m,
              "any_provenance_mentions_human": any("HUMAN" in (r["mapping_provenance"] + r["source_mapping_basis"]).upper()
                                                   for r in rows)}
R["E49_segmentation_label_scope"] = e49

json.dump(R, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
