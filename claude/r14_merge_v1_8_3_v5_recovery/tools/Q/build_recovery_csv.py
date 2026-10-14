"""Build OUT/37_PROTECTED_INPUT_RECOVERY.csv from protected_input_search.py output.

Read-only on all sources; writes one CSV. Usage:
python -I build_recovery_csv.py SEARCH_JSON LOG_PATH OUT_CSV
"""
import csv
import hashlib
import json
import sys
from collections import defaultdict

MATCH_CSV = (r"C:\NTUST_PAPER\outputs\00_CURRENT\02_STUDY1_FREEZE\02_STUDY1_FREEZE_V1_8_1\repo\claude"
             r"\r14_merge_v1_8_2a_workspace_reorg\v5_recovery\V5_PROTECTED_INPUT_MATCH.csv")
SIDECAR_SHA = "4e412a07af1f5c9e2f304408875fc1fc47018c9ff501a17dee437bea880e95a0"
APPEND_LOG_SHA = "c958f8072c38b2172d053d2c390cd2320ec7f41bdb57efa4b97dbbadd3c0eca1"
V18_NOT_RECOVERED = {
    "HUMAN_VALIDATION_400.csv", "SECOND_CODER_120.csv", "workbench.sqlite", "FSC_V5_STAGE1_ON_V4_RECORDS.csv",
    "FSC_V5_USER_RATIFIED_DEFINITIONS.json", "FSC_STAGE2_RESULTS_v1_0_2.sqlite", "LATEST_STAGE3_RESIDUAL_CLOSURE.txt",
    "FINAL_RESULTS_FREEZE_MANIFEST.json", "FREEZE_ROOT_SHA256.txt",
    "V9_CONFERENCE_CAMERA_READY_FULL_CHINESE_BODY_20260921.docx",
    "V9_CONFERENCE_CAMERA_READY_FULL_CHINESE_BODY_20260921.pdf", "SHA256SUMS.csv",
}
# Preferred "original-equivalent" location fragments, in priority order.
PREFERRED = [
    r"C:\NTUST_PAPER\FREEZE\AI_DECISION_V9_SUBMISSION_FREEZE_20260923\00_README_AND_MANIFEST",
    r"C:\NTUST_PAPER\FREEZE\AI_DECISION_V9_SUBMISSION_FREEZE_20260923\01_MANUSCRIPT",
    r"C:\NTUST_PAPER\FREEZE\AI_DECISION_V9_SUBMISSION_FREEZE_20260923\FREEZE_ROOT",
    r"C:\NTUST_PAPER\LocalCorpusWorkbench\v5_production_app\data",
    r"C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\04_V5_PRODUCTION_FREEZE\20260911_AI_DECISION_V5_PRODUCTION\0",
    r"C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\04_V5_PRODUCTION_FREEZE\20260911_AI_DECISION_V5_PRODUCTION\1",
    r"C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\02_V5_METHOD\20260920_V5_METHOD_HARDENING\04",
    r"C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\03_R14_STUDY1\01_SOURCE_CLOSURE_V1_8\02_V9_HUMAN_VALIDATION\20260929_V9_HUMAN_VALIDATION",
    r"C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\01_V9_HUMAN_VALIDATION",
]


def v18_status(path, name):
    if name in V18_NOT_RECOVERED:
        return "NOT_RECOVERED(V1.8 02 s5)"
    if path.startswith("outputs/20260929_V9_HUMAN_VALIDATION/"):
        return "IN_PACKAGE_MISMATCH" if name == "HUMAN_AUDIT_APPEND_ONLY_LOG.csv" else "IN_PACKAGE_MATCH"
    return "EXTERNAL_IDENTICAL_COPY_IN_PACKAGE"


def pick(locs, name, base_name):
    exact = [l for l in locs if "!" not in l and l.lower().endswith("\\" + base_name.lower())] or \
            [l for l in locs if "!" not in l] or locs
    for pref in PREFERRED:
        for loc in exact:
            if loc.startswith(pref):
                return loc
    return sorted(exact)[0] if exact else ""


def main(search_json, log_path, out_csv):
    with open(search_json, encoding="utf-8") as fh:
        res = json.load(fh)
    by_hash = defaultdict(list)
    for h in res["hits"]:
        by_hash[h["sha256"]].append(h["location"])
    with open(log_path, "rb") as fh:
        log = fh.read()
    prefix_ok = hashlib.sha256(log[:355]).hexdigest() == APPEND_LOG_SHA
    with open(MATCH_CSV, encoding="utf-8-sig", newline="") as fh:
        prior = {r["sha256"]: r["found_in"] for r in csv.DictReader(fh)}
    rows = []
    for i, b in enumerate(res["baseline"], 1):
        name = b["path"].rsplit("/", 1)[-1]
        locs = sorted(set(by_hash.get(b["sha256"], [])))
        status, mode, note = "NOT_RECOVERED", "", ""
        if locs:
            status, mode = "CONFIRMED", "FULL_SHA256_FILE"
            if any("!" in l for l in locs) and all("!" in l for l in locs):
                mode = "FULL_SHA256_ZIP_MEMBER"
        elif b["sha256"] == APPEND_LOG_SHA and prefix_ok:
            status, mode = "CONFIRMED", "FULL_SHA256_OF_355_BYTE_PREFIX"
            locs = [log_path + " [bytes 0..354]"]
            note = ("No standalone file at the protected hash exists anywhere searched. The first 355 bytes "
                    "(= protected size) of the current 625-byte log hash to the protected value, so the protected "
                    "state is a byte-exact prefix of the current append-only log.")
        if b["sha256"] == "8b1bc2ccf0315764e8ef908cf877b67068c0fa409f91ce1979008b6d341be762":
            note = "Same sha256 as the other SAMPLING_MANIFEST row (baseline has 37 rows / 36 distinct hashes)."
        rows.append({
            "row": i, "baseline_path": b["path"], "sha256": b["sha256"], "bytes": b["bytes"],
            "v1_8_status": v18_status(b["path"], name), "v1_8_2a_match": prior.get(b["sha256"], ""),
            "v1_8_3_status": status, "match_mode": mode,
            "primary_path": pick(locs, name, name) if mode.startswith("FULL_SHA256_F") or mode.endswith("ZIP_MEMBER") else (locs[0] if locs else ""),
            "identical_copies": len(locs) if mode != "FULL_SHA256_OF_355_BYTE_PREFIX" else 0,
            "all_locations": " | ".join(locs), "note": note,
        })
    side = sorted(set(by_hash.get(SIDECAR_SHA, [])))
    rows.append({
        "row": "S1", "baseline_path": "(not a baseline row) V9 sidecar core FINAL_ROBUST_CORE_32.csv",
        "sha256": SIDECAR_SHA, "bytes": "", "v1_8_status": "NOT_SHIPPED", "v1_8_2a_match": "NOT_FOUND",
        "v1_8_3_status": "CONFIRMED" if side else "NOT_RECOVERED", "match_mode": "FULL_SHA256_FILE" if side else "",
        "primary_path": side[0] if side else "", "identical_copies": len(side), "all_locations": " | ".join(side),
        "note": "Pinned in V9 FINAL_STATUS.json / ROBUST_CORE_LOCAL_SENSITIVITY_STATUS.json / REANALYSIS_PROPOSAL.md.",
    })
    with open(out_csv, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "rows;", sum(r["v1_8_3_status"] == "CONFIRMED" for r in rows), "CONFIRMED")


if __name__ == "__main__":
    main(*sys.argv[1:4])
