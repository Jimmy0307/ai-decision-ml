"""Independently re-derive the sidecar label-propagation actions from the frozen human inputs.

Applies the rule stated in LOCAL_HUMAN_CORRECTION_POLICY.md to FIRST_CODER_50_FINAL_FROZEN.csv
and HUMAN_RECONCILED_20.csv, then compares with HUMAN_AUDIT_LOCAL_CORRECTION_MAP.csv.
Descriptive only: no pipeline stage is run. Usage: python -I rule_check.py
"""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE")
V9 = ROOT / r"03_R14_STUDY1\01_SOURCE_CLOSURE_V1_8\02_V9_HUMAN_VALIDATION\20260929_V9_HUMAN_VALIDATION"
SIDECAR = ROOT / r"01_V9_HUMAN_VALIDATION\20261003_V9_HUMAN_AUDIT_FINAL_CONVERGENCE_SIDECAR_20261003T192417"
MANIFEST = ROOT / (r"04_V5_PRODUCTION_FREEZE\20260911_AI_DECISION_V5_PRODUCTION\10_DOCUMENT_DEDUP_MATRIX"
                   r"\matrix_v1_20260918T132505Z\DOCUMENT_DEDUP_MATRIX_MANIFEST.json")


def rows(p):
    with open(p, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def action(lab, ai, dec):
    c1, c3, c4, c5 = (lab[k].strip().upper() for k in ("C1", "C3", "C4", "C5"))
    if c5 == "EXCLUDE":
        return "REMOVE_HUMAN_EXCLUDED_PAIR"
    if c5 == "INCLUDE" and c1 == "VALID" and c3 in ai and c4 in dec:
        return "APPLY_HUMAN_FAMILY_PAIR"
    if c5 == "INCLUDE" and c1 == "VALID":
        return "REMOVE_UNMAPPED_HUMAN_FAMILY_PAIR"
    return "LEAVE_OFFICIAL_PAIR_UNCHANGED"


def main():
    tax = json.loads(MANIFEST.read_text(encoding="utf-8"))["taxonomy"]
    ai, dec = set(tax["ai_families"]), set(tax["decision_families"])
    first_p, recon_p = V9 / "FIRST_CODER_50_FINAL_FROZEN.csv", V9 / "HUMAN_RECONCILED_20.csv"
    recon = {r["record_id"]: r for r in rows(recon_p)}
    derived = {}
    for r in rows(first_p):
        q = recon.get(r["record_id"])
        lab = ({k: q[f"FINAL_{k}"] for k in ("C1", "C3", "C4", "C5")} if q else
               {"C1": r["human_evidence_valid"], "C3": r["human_ai_family"],
                "C4": r["human_decision_family"], "C5": r["human_include"]})
        derived[r["record_id"]] = action(lab, ai, dec)
    mapped = {r["record_id"]: r["action"] for r in rows(SIDECAR / "HUMAN_AUDIT_LOCAL_CORRECTION_MAP.csv")}
    diff = sorted(k for k in set(derived) | set(mapped) if derived.get(k) != mapped.get(k))
    counts = Counter(derived.values())
    removed = counts["REMOVE_HUMAN_EXCLUDED_PAIR"] + counts["REMOVE_UNMAPPED_HUMAN_FAMILY_PAIR"]
    print(json.dumps({"first_coder_sha256": sha(first_p), "reconciled_sha256": sha(recon_p),
                      "policy_sha256": sha(SIDECAR / "LOCAL_HUMAN_CORRECTION_POLICY.md"),
                      "records": len(derived), "derived_actions": dict(counts),
                      "derived_eligible_delta": -removed, "action_mismatches_vs_map": diff}, indent=1))


if __name__ == "__main__":
    main()
