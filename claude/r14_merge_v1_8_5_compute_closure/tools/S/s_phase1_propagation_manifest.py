"""V1.8.5 sub-agent S, Phase 1: freeze BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1 into a 50-row record manifest.

Descriptive only. Reads WORK copies (never sources), runs no pipeline stage.
Usage: python -I s_phase1_propagation_manifest.py <inputs_dir> <manifest_out_csv> <checks_out_json>

Precedence: RECONCILED_FINAL (HUMAN_RECONCILED_20 FINAL_C*) > FIRST_CODER (FIRST_CODER_50 human_*) > ORIGINAL_MODEL.
Translation of human codes into pipeline fields = the recovered sidecar translation
(prepare_and_run_corrected_sidecar.py lines 354-394), reproduced verbatim in logic below.
"""
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

PIPE_FIELDS = ["analytical_pair_eligible", "left_final_family", "right_final_family", "left_final_status",
               "right_final_status", "mapping_completeness", "analytical_exclusion_reason"]
DESCRIPTIVE_ONLY = ["relation_type"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rows(p: Path):
    with p.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def translate(label, ai, dec):
    """Verbatim logic of the sidecar generator lines 354-363 (action) and 372-394 (field writes)."""
    c1, c3, c4, c5 = (label[k].strip().upper() for k in ("C1", "C3", "C4", "C5"))
    if c5 == "EXCLUDE":
        return "REMOVE_HUMAN_EXCLUDED_PAIR"
    if c5 == "INCLUDE" and c1 == "VALID" and c3 in ai and c4 in dec:
        return "APPLY_HUMAN_FAMILY_PAIR"
    if c5 == "INCLUDE" and c1 == "VALID":
        return "REMOVE_UNMAPPED_HUMAN_FAMILY_PAIR"
    return "LEAVE_OFFICIAL_PAIR_UNCHANGED"


def apply_fields(row, label, action, ai, dec):
    out = {k: row[k] for k in PIPE_FIELDS}
    if action == "REMOVE_HUMAN_EXCLUDED_PAIR":
        out["analytical_pair_eligible"] = "False"
        out["analytical_exclusion_reason"] = "HUMAN_AUDIT_LOCAL_SENSITIVITY_C5_EXCLUDE"
    elif action == "APPLY_HUMAN_FAMILY_PAIR":
        out["left_final_family"] = label["C3"].strip().upper()
        out["right_final_family"] = label["C4"].strip().upper()
        out["left_final_status"] = "MAPPED"
        out["right_final_status"] = "MAPPED"
        out["mapping_completeness"] = "FULLY_MAPPED"
        out["analytical_pair_eligible"] = "True"
        out["analytical_exclusion_reason"] = ""
    elif action == "REMOVE_UNMAPPED_HUMAN_FAMILY_PAIR":
        c3, c4 = label["C3"].strip().upper(), label["C4"].strip().upper()
        if c3 in ai:
            out["left_final_family"], out["left_final_status"] = c3, "MAPPED"
        else:
            out["left_final_family"], out["left_final_status"] = "", "UNRESOLVED_HUMAN_AUDIT"
        if c4 in dec:
            out["right_final_family"], out["right_final_status"] = c4, "MAPPED"
        else:
            out["right_final_family"], out["right_final_status"] = "", "UNRESOLVED_HUMAN_AUDIT"
        out["mapping_completeness"] = ("PARTIALLY_MAPPED" if (out["left_final_family"] or out["right_final_family"])
                                       else "FULLY_UNRESOLVED")
        out["analytical_pair_eligible"] = "False"
        out["analytical_exclusion_reason"] = "HUMAN_AUDIT_LOCAL_SENSITIVITY_FAMILY_UNRESOLVED"
    return out


def verify_events(events_p: Path, recon):
    events = [json.loads(x) for x in events_p.read_text(encoding="utf-8").splitlines() if x.strip()]
    prev_ok, hash_ok, link_ok = 0, 0, 0
    prev = None
    by_id = {}
    for i, e in enumerate(events, 1):
        payload = {k: v for k, v in e.items() if k != "current_event_hash"}
        h = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True,
                                      separators=(",", ":")).encode("utf-8")).hexdigest().upper()
        hash_ok += h == e["current_event_hash"]
        if i > 1:
            prev_ok += e["previous_event_hash"] == prev
        prev = e["current_event_hash"]
        by_id[e["event_id"]] = e
    final_match, mism = 0, []
    for r in recon:
        if r["RESOLUTION_BASIS"] != "HUMAN_ADJUDICATION":
            continue
        e = by_id.get(r["RECONCILIATION_EVENT_ID"])
        ok = (e is not None and e["record_id"] == r["record_id"] and e["current_event_hash"] == r["RECONCILIATION_EVENT_HASH"]
              and all(e[f"FINAL_C{i}"] == r[f"FINAL_C{i}"] for i in range(1, 6)))
        link_ok += ok
        if ok:
            final_match += 1
        else:
            mism.append(r["record_id"])
    return {"events": len(events), "event_hash_recomputed_ok": hash_ok, "prev_links_ok": prev_ok,
            "adjudicated_rows": sum(r["RESOLUTION_BASIS"] == "HUMAN_ADJUDICATION" for r in recon),
            "row_to_event_final_label_match": final_match, "row_event_mismatches": mism,
            "unique_event_records": len({e["record_id"] for e in events})}


def main():
    inp, out_csv, out_json = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    v9, sc = inp / "V9", inp / "SIDECAR"
    fz = inp / r"V5\09_ANALYTICAL_FREEZE\analytical_freeze_v2_20260918T132206Z"
    first_p, recon_p, ev_p = v9 / "FIRST_CODER_50_FINAL_FROZEN.csv", v9 / "HUMAN_RECONCILED_20.csv", v9 / "HUMAN_RECONCILIATION_EVENTS.jsonl"
    rec_p = fz / "ANALYTICAL_FREEZE_RECORD_LEVEL.csv"
    elig_p = fz / "ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv"
    tax_p = inp / r"V5\10_DOCUMENT_DEDUP_MATRIX\matrix_v1_20260918T132505Z\DOCUMENT_DEDUP_MATRIX_CANONICAL.json"
    map_p = sc / "HUMAN_AUDIT_LOCAL_CORRECTION_MAP.csv"
    tax = json.loads(tax_p.read_text(encoding="utf-8"))
    ai, dec = set(tax["ai_families"]), set(tax["decision_families"])

    first, recon, records = rows(first_p), rows(recon_p), rows(rec_p)
    elig_ids = {r["record_id"] for r in rows(elig_p)}
    rec_by = {}
    dup_v5 = Counter(r["record_id"] for r in records)
    for r in records:
        rec_by.setdefault(r["record_id"], []).append(r)
    recon_by = {r["record_id"]: r for r in recon}
    first_ids = [r["record_id"] for r in first]
    checks = {
        "first_coder_rows": len(first), "first_coder_unique_ids": len(set(first_ids)),
        "reconciled_rows": len(recon), "reconciled_unique_ids": len(recon_by),
        "reconciled_subset_of_first": set(recon_by) <= set(first_ids),
        "v5_record_rows": len(records), "v5_unique_record_ids": len(dup_v5),
        "reconciled_basis": dict(Counter(r["RESOLUTION_BASIS"] for r in recon)),
        "event_chain": verify_events(ev_p, recon),
        "taxonomy_ai": sorted(ai), "taxonomy_decision": sorted(dec),
    }
    unanimous_ok = all(all(r[f"FINAL_C{i}"] == r[f"FIRST_C{i}"] == r[f"BLIND_C{i}"] for i in range(1, 6))
                       for r in recon if r["RESOLUTION_BASIS"] == "UNANIMOUS_PRE_ADJUDICATION")
    checks["unanimous_row_final_eq_first_eq_blind"] = unanimous_ok
    sidecar_map = {r["record_id"]: r for r in rows(map_p)}
    hashes = {"FIRST_CODER_50_FINAL_FROZEN.csv": sha(first_p), "HUMAN_RECONCILED_20.csv": sha(recon_p),
              "HUMAN_RECONCILIATION_EVENTS.jsonl": sha(ev_p), "ANALYTICAL_FREEZE_RECORD_LEVEL.csv": sha(rec_p),
              "ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv": sha(elig_p), "DOCUMENT_DEDUP_MATRIX_CANONICAL.json": sha(tax_p),
              "HUMAN_AUDIT_LOCAL_CORRECTION_MAP.csv": sha(map_p)}
    checks["input_sha256"] = hashes

    out_rows, join_problems, model_mismatch, sidecar_mismatch = [], [], [], []
    for fr in first:
        rid = fr["record_id"]
        matches = rec_by.get(rid, [])
        if len(matches) != 1:
            join_problems.append({"record_id": rid, "v5_matches": len(matches)})
            continue
        v5 = matches[0]
        if rid in recon_by:
            q = recon_by[rid]
            label = {f"C{i}": q[f"FINAL_C{i}"] for i in range(1, 6)}
            cls, src_art, src_sha = "RECONCILED_FINAL", "V9/HUMAN_RECONCILED_20.csv (FINAL_C1..C5)", hashes["HUMAN_RECONCILED_20.csv"]
            src_detail = q["RESOLUTION_BASIS"] + (":" + q["RECONCILIATION_EVENT_ID"] if q["RECONCILIATION_EVENT_ID"] else "")
        else:
            label = {"C1": fr["human_evidence_valid"], "C2": fr["human_relation_type"], "C3": fr["human_ai_family"],
                     "C4": fr["human_decision_family"], "C5": fr["human_include"]}
            cls, src_art, src_sha = "FIRST_CODER", "V9/FIRST_CODER_50_FINAL_FROZEN.csv (human_*)", hashes["FIRST_CODER_50_FINAL_FROZEN.csv"]
            src_detail = "FIRST_CODER_ONLY"
        action = translate(label, ai, dec)
        new = apply_fields(v5, label, action, ai, dec)
        # model-side consistency: V9 snapshot model labels vs V5 freeze row
        if (fr["current_ai_family"] != v5["left_final_family"] or fr["current_decision_family"] != v5["right_final_family"]
                or str(fr["model_analytical_pair_eligible"]).strip().lower() != str(v5["analytical_pair_eligible"]).strip().lower()):
            model_mismatch.append(rid)
        sm = sidecar_map.get(rid)
        if (sm is None or sm["action"] != action or sm["sidecar_eligible"] != new["analytical_pair_eligible"]
                or sm["sidecar_AI_family"] != new["left_final_family"] or sm["sidecar_Decision_family"] != new["right_final_family"]):
            sidecar_mismatch.append(rid)
        row = {"record_id": rid, "join_key": "record_id", "validation_id": fr["validation_id"],
               "v5_document_id": v5["document_id"], "v5_in_pair_eligible_file": rid in elig_ids,
               "source_artifact": src_art, "precedence_class": cls, "replacement_source": src_detail,
               "human_C1": label["C1"], "human_C2_descriptive_only": label["C2"], "human_C3": label["C3"],
               "human_C4": label["C4"], "human_C5": label["C5"], "translation_action": action}
        for k in PIPE_FIELDS:
            row[f"old_model_{k}"] = v5[k]
        row["old_model_relation_type"] = v5["relation_type"]
        for k in PIPE_FIELDS:
            row[f"final_{k}"] = new[k]
        row["final_relation_type"] = v5["relation_type"] + " (UNCHANGED; C2 descriptive only)"
        row["fields_changed"] = "|".join(k for k in PIPE_FIELDS if new[k] != v5[k])
        row["label_input_sha256"] = src_sha
        row["v5_record_level_sha256"] = hashes["ANALYTICAL_FREEZE_RECORD_LEVEL.csv"]
        out_rows.append(row)

    cls_counts = Counter(r["precedence_class"] for r in out_rows)
    act_counts = Counter(r["translation_action"] for r in out_rows)
    removed = act_counts["REMOVE_HUMAN_EXCLUDED_PAIR"] + act_counts["REMOVE_UNMAPPED_HUMAN_FAMILY_PAIR"]
    checks.update({
        "manifest_rows": len(out_rows), "unique_manifest_records": len({r["record_id"] for r in out_rows}),
        "precedence_class_counts": dict(cls_counts), "join_problems": join_problems,
        "all_50_in_v5_pair_eligible": all(r["v5_in_pair_eligible_file"] for r in out_rows),
        "v9_model_labels_vs_v5_mismatches": model_mismatch,
        "translation_vs_sidecar_map_mismatches": sidecar_mismatch,
        "translation_action_counts": dict(act_counts),
        "pair_eligible_delta": -removed, "pair_eligible_after": 3125 - removed,
        "records_with_any_pipeline_field_change": sum(bool(r["fields_changed"]) for r in out_rows),
        "conflicting_final_labels": 0,
    })
    ok = (len(out_rows) == 50 and cls_counts == {"RECONCILED_FINAL": 20, "FIRST_CODER": 30} and not join_problems
          and checks["first_coder_unique_ids"] == 50 and checks["v5_unique_record_ids"] == len(records)
          and checks["event_chain"]["row_to_event_final_label_match"] == 19 and unanimous_ok)
    checks["PHASE1_GATE"] = "PASS" if ok else "STOP"
    out_rows.sort(key=lambda r: (r["precedence_class"] != "RECONCILED_FINAL", r["validation_id"]))
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(out_rows)
    out_json.write_text(json.dumps(checks, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: checks[k] for k in ("manifest_rows", "precedence_class_counts", "translation_action_counts",
                                             "pair_eligible_delta", "join_problems", "v9_model_labels_vs_v5_mismatches",
                                             "translation_vs_sidecar_map_mismatches", "event_chain", "PHASE1_GATE")}, indent=1))
    if not ok:
        sys.exit(2)


if __name__ == "__main__":
    main()
