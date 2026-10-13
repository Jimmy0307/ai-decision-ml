"""Independent recomputation of V9 human audit 50/20/19 counts and C1-C5 Cohen's kappa.

Usage: python -I recompute_human_audit.py <package_dir> <out_json>
Reads raw CSV/JSONL rows only; does not import or execute package code.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

DIMS = [
    ("C1", "Evidence validity", "human_evidence_valid"),
    ("C2", "Relation type", "human_relation_type"),
    ("C3", "AI functional family", "human_ai_family"),
    ("C4", "Decision functional family", "human_decision_family"),
    ("C5", "Analytical inclusion", "human_include"),
]
RELATIONS = {"SUPPORTS", "GOVERNS", "TRANSFORMS", "CONSTRAINS", "INFORMS", "ENABLES",
             "ASSOCIATED_WITH", "AMBIGUOUS", "NOT_APPLICABLE"}
REQUIRED = ["human_evidence_valid", "human_relation_type", "human_ai_family",
            "human_decision_family", "human_include", "coder_confidence", "coder_id"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest().upper()


def rcsv(p: Path) -> list[dict[str, str]]:
    with p.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_crosswalk(pkg: Path) -> tuple[dict, dict, set, set]:
    rows = rcsv(pkg / "MODEL_FAMILY_CODEBOOK_CROSSWALK.csv")
    alias = {"AI": {}, "DECISION": {}}
    canon = {"AI": set(), "DECISION": set()}
    for r in rows:
        side = r["SIDE"]
        if r["CANONICAL_FAMILY_ID"]:
            canon[side].add(r["CANONICAL_FAMILY_ID"])
            alias[side][r["HUMAN_REVIEW_DISPLAY_LABEL"]] = r["CANONICAL_FAMILY_ID"]
            alias[side][r["MODEL_SOURCE_LABEL"]] = r["CANONICAL_FAMILY_ID"]
    ai_ok = canon["AI"] | {"UNMAPPED", "AMBIGUOUS"}
    dec_ok = canon["DECISION"] | {"UNMAPPED", "AMBIGUOUS"}
    return alias["AI"], alias["DECISION"], ai_ok, dec_ok


def enums(ai_ok: set, dec_ok: set) -> dict[str, set]:
    return {
        "human_evidence_valid": {"VALID", "INVALID", "UNCERTAIN"},
        "human_relation_type": RELATIONS,
        "human_ai_family": ai_ok,
        "human_decision_family": dec_ok,
        "human_include": {"INCLUDE", "EXCLUDE", "UNCERTAIN"},
        "coder_confidence": {"HIGH", "MEDIUM", "LOW"},
    }


def complete(row: dict[str, str], en: dict[str, set]) -> tuple[bool, list[str]]:
    probs = []
    if row.get("review_status") != "COMPLETE":
        probs.append(f"review_status={row.get('review_status')!r}")
    for f in REQUIRED:
        if not (row.get(f) or "").strip():
            probs.append(f"blank:{f}")
    for f, allowed in en.items():
        if (row.get(f) or "") not in allowed:
            probs.append(f"invalid:{f}={row.get(f)!r}")
    return (not probs), probs


def kappa(a: list[str], b: list[str]) -> dict:
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    labels = sorted(set(a) | set(b))
    pe = sum(ca[l] * cb[l] for l in labels) / (n * n)
    k = None if abs(1 - pe) < 1e-12 else (po - pe) / (1 - pe)
    return {"n": n, "agree": sum(x == y for x, y in zip(a, b)), "Po": po, "Pe": pe,
            "kappa": k, "labels": labels, "marg_A": dict(ca), "marg_B": dict(cb)}


def canon_val(field: str, v: str, ai_alias: dict, dec_alias: dict) -> str:
    if field == "human_ai_family":
        return ai_alias.get(v, v)
    if field == "human_decision_family":
        return dec_alias.get(v, v)
    return v


def main() -> None:
    pkg, out = Path(sys.argv[1]), Path(sys.argv[2])
    res: dict = {}
    ai_alias, dec_alias, ai_ok, dec_ok = load_crosswalk(pkg)
    en = enums(ai_ok, dec_ok)
    res["crosswalk_sha256"] = sha(pkg / "MODEL_FAMILY_CODEBOOK_CROSSWALK.csv")

    # hashes of all inputs
    names = ["FIRST_CODER_50_FINAL_FROZEN.csv", "FIRST_CODER_50_FROZEN.csv", "HUMAN_VALIDATION_400_WORKING.csv",
             "HUMAN_AUDIT_APPEND_ONLY_LOG.csv", "HUMAN_AUDIT_EPOCH2_LOG.csv", "HUMAN_AUDIT_EPOCH2_GENESIS.md",
             "SECOND_CODER_BLIND_20.csv", "BLIND_REPEAT_20_FINAL_FROZEN.csv", "SECOND_CODER_BLIND_20_AUDIT_LOG.csv",
             "SECOND_CODER_120_WORKING.csv", "SECOND_CODER_BLIND_20_ALLOCATION.csv", "SECOND_CODER_BLIND_20_MANIFEST.csv",
             "SECOND_CODER_BUG_PRESTATE.csv", "HUMAN_DISAGREEMENT_QUEUE_20.csv", "DISAGREEMENT_QUEUE.csv",
             "HUMAN_RECONCILED_20.csv", "HUMAN_RECONCILIATION_EVENTS.jsonl", "ADJUDICATION_LOG.csv",
             "FIRST_CODER_50_MANIFEST.csv", "LEGACY_AUDIT_LOG_FORENSIC_SNAPSHOT.csv",
             "HUMAN_RELIABILITY_FINAL.csv", "HUMAN_RELIABILITY_20.csv", "MODEL_FAMILY_CODEBOOK_CROSSWALK.csv"]
    res["hashes"] = {n: sha(pkg / n) for n in names if (pkg / n).is_file()}

    # sidecar verification
    side = []
    for p in sorted(pkg.glob("*.sha256")):
        txt = p.read_text(encoding="utf-8-sig")
        for line in txt.splitlines():
            parts = line.split()
            if len(parts) == 2 and len(parts[0]) == 64:
                tgt = pkg / parts[1]
                actual = sha(tgt) if tgt.is_file() else "MISSING"
                side.append({"sidecar": p.name, "target": parts[1], "recorded": parts[0].upper(),
                             "actual": actual, "match": actual == parts[0].upper()})
            elif "=" in line:
                k, v = line.split("=", 1)
                side.append({"sidecar": p.name, "kv": k, "value": v})
    for p in ["FIRST_CODER_50_SHA256.txt", "SECOND_CODER_BLIND_20_SHA256.txt", "HUMAN_RECONCILIATION_INTERFACE_SHA256.txt"]:
        for line in (pkg / p).read_text(encoding="utf-8-sig").splitlines():
            parts = line.split()
            if len(parts) == 2 and len(parts[0]) == 64:
                tgt = pkg / parts[1]
                actual = sha(tgt) if tgt.is_file() else "MISSING"
                side.append({"sidecar": p, "target": parts[1], "recorded": parts[0].upper(), "actual": actual,
                             "match": actual == parts[0].upper()})
            elif "SHA-256:" in line:
                fn, h = line.split(" SHA-256: ")
                tgt = pkg / fn.strip()
                actual = sha(tgt) if tgt.is_file() else "MISSING"
                side.append({"sidecar": p, "target": fn.strip(), "recorded": h.strip().upper(), "actual": actual,
                             "match": actual == h.strip().upper()})
            elif "=" in line:
                k, v = line.split("=", 1)
                entry = {"sidecar": p, "kv": k, "value": v}
                if k.endswith("SHA256") and k not in ("SOURCE_CURRENT_SHA256",):
                    # try to map to a file
                    keymap = {"SNAPSHOT_SHA256": "FIRST_CODER_50_FROZEN.csv",
                              "FROZEN_FIRST_CODER_SNAPSHOT_SHA256": "FIRST_CODER_50_FROZEN.csv",
                              "QUEUE_SHA256": "SECOND_CODER_BLIND_20.csv",
                              "MANIFEST_SHA256": "SECOND_CODER_BLIND_20_MANIFEST.csv",
                              "ALLOCATION_SHA256": "SECOND_CODER_BLIND_20_ALLOCATION.csv",
                              "SOURCE_FIRST_CODER_400_WORKING_SHA256": "HUMAN_VALIDATION_400_WORKING.csv"}
                    if k in keymap:
                        tgt = pkg / keymap[k]
                        entry["target"] = keymap[k]
                        entry["actual"] = sha(tgt)
                        entry["match"] = entry["actual"] == v.strip().upper()
                side.append(entry)
    res["sidecars"] = side

    # FIRST CODER
    f_final = rcsv(pkg / "FIRST_CODER_50_FINAL_FROZEN.csv")
    f_frozen = rcsv(pkg / "FIRST_CODER_50_FROZEN.csv")
    res["first_final_vs_frozen_bytes_identical"] = sha(pkg / "FIRST_CODER_50_FINAL_FROZEN.csv") == sha(pkg / "FIRST_CODER_50_FROZEN.csv")
    first = f_final
    fc = [complete(r, en) for r in first]
    res["FIRST_CODER_TOTAL"] = len(first)
    res["FIRST_CODER_UNIQUE_IDS"] = len({r["record_id"] for r in first})
    res["FIRST_CODER_COMPLETE"] = sum(ok for ok, _ in fc)
    res["first_incomplete_problems"] = {r["record_id"]: p for r, (ok, p) in zip(first, fc) if not ok}
    res["first_coder_ids"] = dict(Counter(r["coder_id"] for r in first))
    res["first_strata"] = dict(Counter(r.get("sampling_stratum_detail", "") for r in first))
    res["first_alias_labels_present"] = {
        f: sorted({r[f] for r in first if r[f] in (ai_alias if f == "human_ai_family" else dec_alias) and
                   (ai_alias if f == "human_ai_family" else dec_alias)[r[f]] != r[f]})
        for f in ("human_ai_family", "human_decision_family")}

    # 400 working: cross-check the 50
    w400 = rcsv(pkg / "HUMAN_VALIDATION_400_WORKING.csv")
    res["w400_rows"] = len(w400)
    res["w400_status"] = dict(Counter(r.get("review_status", "") for r in w400))
    w400c = [r for r in w400 if complete(r, en)[0]]
    res["w400_complete_valid"] = len(w400c)
    w_by = {}
    for r in w400:
        w_by.setdefault(r["record_id"], []).append(r)
    mism = []
    for r in first:
        cands = [w for w in w_by.get(r["record_id"], []) if w.get("validation_id") == r.get("validation_id")]
        if len(cands) != 1:
            mism.append((r["record_id"], "no_unique_match_in_400"))
            continue
        w = cands[0]
        diffs = [k for k in r if r.get(k, "") != w.get(k, "")]
        if diffs:
            mism.append((r["record_id"], diffs))
    res["first_vs_400_mismatches"] = mism
    res["w400_complete_ids_eq_first50"] = {r["validation_id"] for r in w400c} == {r["validation_id"] for r in first}

    # manifest
    man = rcsv(pkg / "FIRST_CODER_50_MANIFEST.csv")
    res["first_manifest_rows"] = len(man)
    res["first_manifest_ids_eq"] = {m["record_id"] for m in man} == {r["record_id"] for r in first}

    # SECOND CODER
    s_live = rcsv(pkg / "SECOND_CODER_BLIND_20.csv")
    s_frozen = rcsv(pkg / "BLIND_REPEAT_20_FINAL_FROZEN.csv")
    res["second_live_vs_frozen_bytes_identical"] = sha(pkg / "SECOND_CODER_BLIND_20.csv") == sha(pkg / "BLIND_REPEAT_20_FINAL_FROZEN.csv")
    second = s_frozen
    sc = [complete(r, en) for r in second]
    res["SECOND_CODER_TOTAL"] = len(second)
    res["SECOND_CODER_UNIQUE_IDS"] = len({r["record_id"] for r in second})
    res["SECOND_CODER_COMPLETE"] = sum(ok for ok, _ in sc)
    res["second_incomplete_problems"] = {r["record_id"]: p for r, (ok, p) in zip(second, sc) if not ok}
    res["second_coder_ids"] = dict(Counter(r["coder_id"] for r in second))
    res["second_columns"] = list(second[0].keys())
    f_by = {r["record_id"]: r for r in first}
    sid = {r["record_id"] for r in second}
    res["second_subset_of_first"] = sid <= set(f_by)
    res["second_evidence_text_matches_first"] = all(f_by[r["record_id"]]["evidence_text"] == r["evidence_text"] for r in second)
    res["coder_id_overlap"] = sorted(set(res["first_coder_ids"]) & set(res["second_coder_ids"]))
    # blindness: columns exposing coder A or model values
    leak_cols = [c for c in res["second_columns"] if c.startswith(("model_", "current_", "left_", "right_", "source_model", "first_", "coder1"))]
    res["second_file_leak_columns"] = leak_cols
    # alias labels in second
    res["second_alias_labels_present"] = {
        f: sorted({r[f] for r in second if (ai_alias if f == "human_ai_family" else dec_alias).get(r[f], r[f]) != r[f]})
        for f in ("human_ai_family", "human_decision_family")}

    # manifest / allocation
    sman = rcsv(pkg / "SECOND_CODER_BLIND_20_MANIFEST.csv")
    res["second_manifest_rows"] = len(sman)
    res["second_manifest_ids_eq_second"] = {m["record_id"] for m in sman} == sid
    # reproduce selection
    grouped = {}
    for r in first:
        grouped.setdefault(r["sampling_stratum_detail"], []).append(r["record_id"])
    alloc = rcsv(pkg / "SECOND_CODER_BLIND_20_ALLOCATION.csv")
    repro = set()
    for a in alloc:
        ids = grouped.get(a["sampling_stratum"], [])
        ranked = sorted((hashlib.sha256(f"{a['seed']}|{a['sampling_stratum']}|{i}".encode()).hexdigest().upper(), i) for i in ids)
        repro |= {i for _, i in ranked[: int(a["selected_n"])]}
    res["selection_reproduced_from_seed"] = repro == sid
    res["allocation"] = alloc

    # audit log of second coder
    alog = rcsv(pkg / "SECOND_CODER_BLIND_20_AUDIT_LOG.csv")
    res["second_audit_log_rows"] = len(alog)
    res["second_audit_log_status"] = dict(Counter(r["role"] + "|" + r["review_status"] for r in alog))
    last_complete = {}
    for r in alog:
        if r["review_status"] == "COMPLETE":
            last_complete[r["record_id"]] = json.loads(r["answer_json"])
    res["second_audit_log_complete_ids"] = len(last_complete)
    lm = []
    for r in second:
        lc = last_complete.get(r["record_id"])
        if lc is None:
            lm.append((r["record_id"], "no COMPLETE event"))
            continue
        d = [f for _, _, f in DIMS if lc.get(f) != r[f]]
        if d:
            lm.append((r["record_id"], d))
    res["second_vs_auditlog_last_complete_mismatch"] = lm
    s120 = rcsv(pkg / "SECOND_CODER_120_WORKING.csv")
    res["second120_rows"] = len(s120)
    res["second120_status"] = dict(Counter(r.get("review_status", "") for r in s120))
    res["second120_nonblank_answers"] = sum(1 for r in s120 if any((r.get(f) or "").strip() for f in REQUIRED))

    # DISAGREEMENTS
    pairs = [(f_by[r["record_id"]], r) for r in sorted(second, key=lambda x: x["record_id"])]

    def dis_set(canonical: bool, dims=DIMS) -> dict[str, list[str]]:
        out_ = {}
        for a, b in pairs:
            d = []
            for c, _, f in dims:
                va, vb = a[f], b[f]
                if canonical:
                    va, vb = canon_val(f, va, ai_alias, dec_alias), canon_val(f, vb, ai_alias, dec_alias)
                if va != vb:
                    d.append(c)
            if d:
                out_[a["record_id"]] = d
        return out_

    raw_dis = dis_set(False)
    can_dis = dis_set(True)
    res["disagree_any5_raw"] = raw_dis
    res["disagree_any5_canonical"] = can_dis
    res["disagree_rule_counts"] = {
        "any_of_5_raw": len(raw_dis), "any_of_5_canonical": len(can_dis),
        "any_of_C1_C2_C5_only": len(dis_set(True, [DIMS[0], DIMS[1], DIMS[4]])),
        "any_of_C3_C4_only": len(dis_set(True, [DIMS[2], DIMS[3]])),
        "all_5_disagree": sum(1 for v in can_dis.values() if len(v) == 5),
        "C1_only_rule": len(dis_set(True, [DIMS[0]])),
    }
    res["field_level_disagreements"] = sum(len(v) for v in can_dis.values())
    full_agree = sorted(set(sid) - set(can_dis))
    res["full_agreement_ids"] = full_agree

    q = rcsv(pkg / "HUMAN_DISAGREEMENT_QUEUE_20.csv")
    res["queue20_rows"] = len(q)
    qids = {r["record_id"] for r in q}
    res["queue20_eq_derived"] = qids == set(can_dis)
    qmis = []
    fieldmap = {c: f for c, _, f in DIMS}
    for r in q:
        a, b = f_by[r["record_id"]], next(x for x in second if x["record_id"] == r["record_id"])
        for c, f in fieldmap.items():
            if r[f"first_{c}"] != a[f] or r[f"blind_round_{c}"] != b[f]:
                qmis.append((r["record_id"], c))
        exp = ";".join(fieldmap[c] for c in can_dis.get(r["record_id"], []))
        if r["disagreement_fields"] != exp:
            qmis.append((r["record_id"], "disagreement_fields", r["disagreement_fields"], exp))
    res["queue20_value_mismatches"] = qmis
    res["legacy_DISAGREEMENT_QUEUE_rows"] = len(rcsv(pkg / "DISAGREEMENT_QUEUE.csv"))
    res["legacy_ADJUDICATION_LOG_rows"] = len(rcsv(pkg / "ADJUDICATION_LOG.csv"))

    # RECONCILIATION
    rec = rcsv(pkg / "HUMAN_RECONCILED_20.csv")
    events = [json.loads(l) for l in (pkg / "HUMAN_RECONCILIATION_EVENTS.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    res["reconciled_rows"] = len(rec)
    res["reconciled_unique"] = len({r["record_id"] for r in rec})
    res["events_n"] = len(events)
    res["events_types"] = dict(Counter(e.get("event_type") for e in events))
    res["events_unique_records"] = len({e["record_id"] for e in events})
    res["events_researchers"] = dict(Counter(e.get("researcher_id") for e in events))
    # chain check
    chain_ok = True
    prev = None
    chain_notes = []
    for e in sorted(events, key=lambda x: x["sequence_number"]):
        if prev is not None and e["previous_event_hash"] != prev:
            chain_ok = False
            chain_notes.append(("prev_link_break", e["sequence_number"]))
        body = {k: v for k, v in e.items() if k != "current_event_hash"}
        h1 = hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest().upper()
        if h1 != e["current_event_hash"]:
            chain_notes.append(("self_hash_unverified_with_assumed_canonicalization", e["sequence_number"]))
        prev = e["current_event_hash"]
    res["events_link_chain_ok"] = chain_ok
    res["events_selfhash_notes"] = chain_notes[:5]
    res["events_selfhash_unverified_n"] = sum(1 for n in chain_notes if n[0].startswith("self"))
    ev_by = {e["record_id"]: e for e in events if e.get("event_type") == "COMPLETE"}
    valid_final = {"FINAL_C1": en["human_evidence_valid"], "FINAL_C2": en["human_relation_type"],
                   "FINAL_C3": en["human_ai_family"], "FINAL_C4": en["human_decision_family"],
                   "FINAL_C5": en["human_include"]}
    rc_complete = 0
    rprob = {}
    for r in rec:
        p = []
        for k, allowed in valid_final.items():
            if r[k] not in allowed:
                p.append(f"{k}={r[k]!r}")
        if not r.get("RESOLUTION_REASON", "").strip():
            p.append("blank RESOLUTION_REASON")
        e = ev_by.get(r["record_id"])
        if e is None:
            p.append("no COMPLETE event")
        else:
            for k in valid_final:
                if e[k] != r[k]:
                    p.append(f"event_mismatch {k}")
            if e["current_event_hash"] != r.get("RECONCILIATION_EVENT_HASH"):
                p.append("event hash mismatch")
        a, b = f_by[r["record_id"]], next(x for x in second if x["record_id"] == r["record_id"])
        for c, f in fieldmap.items():
            if r[f"FIRST_{c}"] != a[f] or r[f"BLIND_{c}"] != b[f]:
                p.append(f"orig_mismatch {c}")
        if p:
            rprob[r["record_id"]] = p
        else:
            rc_complete += 1
    res["RECONCILIATION_COMPLETE"] = rc_complete
    res["reconciliation_problems"] = rprob
    res["reconciled_ids_eq_queue"] = {r["record_id"] for r in rec} == qids
    res["reconciled_ids_in_full_agree"] = sorted({r["record_id"] for r in rec} & set(full_agree))
    res["resolution_basis_counts"] = dict(Counter(r.get("RESOLUTION_BASIS", "") for r in rec))
    res["first_coder_ids_in_reconciled"] = dict(Counter(r["FIRST_CODER_ID"] for r in rec))
    res["blind_coder_ids_in_reconciled"] = dict(Counter(r["BLIND_CODER_ID"] for r in rec))
    res["DISAGREEMENT_TOTAL"] = len(can_dis)

    # KAPPA
    kap = {}
    for c, name, f in DIMS:
        a = [x[f] for x, _ in pairs]
        b = [y[f] for _, y in pairs]
        kr = kappa(a, b)
        ac = [canon_val(f, v, ai_alias, dec_alias) for v in a]
        bc = [canon_val(f, v, ai_alias, dec_alias) for v in b]
        kc = kappa(ac, bc)
        kap[c] = {"name": name, "field": f, "raw": kr, "canonical": kc}
    res["kappa"] = kap
    # also pairs with second live file
    res["kappa_note_live_vs_frozen_second_identical"] = res["second_live_vs_frozen_bytes_identical"]

    # summary files
    res["HUMAN_RELIABILITY_FINAL_csv"] = rcsv(pkg / "HUMAN_RELIABILITY_FINAL.csv")
    res["HUMAN_RELIABILITY_20_csv"] = rcsv(pkg / "HUMAN_RELIABILITY_20.csv")
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print("written", out)


if __name__ == "__main__":
    main()
