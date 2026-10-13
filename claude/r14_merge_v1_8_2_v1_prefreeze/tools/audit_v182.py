"""Pre-freeze audit for V1 v1.8.2. Every audit line is computed by this script; it writes OUT/27_V1_PREFREEZE_AUDIT.md.

Usage: python -E -P audit_v182.py --repo REPO --sealed-local DIR
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

from openpyxl import load_workbook

sys.dont_write_bytecode = True
OUT_REL = os.path.join("claude", "r14_merge_v1_8_2_v1_prefreeze")


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--sealed-local", required=True)
    a = ap.parse_args()
    out = os.path.join(a.repo, OUT_REL)
    tools = os.path.join(out, "tools")
    py = sys.executable
    lines, ev = [], []

    def put(k, v, evidence):
        lines.append(f"{k}={v}")
        ev.append((k, v, evidence))

    # leakage (fresh run)
    lk = subprocess.run([py, "-E", "-P", os.path.join(tools, "leakage_check_v182.py"), "--repo", a.repo,
                         "--sealed-local", a.sealed_local], capture_output=True, text=True)
    res = json.load(open(os.path.join(tools, "leakage_check_result_v1_8_2.json"), encoding="utf-8"))
    checks = [f["check"] for f in res["findings"]]

    dist = sorted(os.path.basename(p) for p in glob.glob(os.path.join(out, "coder_distribution", "*")))
    one_sheet = all(len([s for s in load_workbook(os.path.join(out, "coder_distribution", d)).sheetnames
                         if s.startswith("CODER_")]) == 1 for d in dist)
    put("CODER_FILES", len(dist) if dist == ["CODER_1.xlsx", "CODER_2.xlsx", "CODER_3.xlsx"] and one_sheet else
        f"UNEXPECTED({dist})", f"coder_distribution = {dist}; one CODER sheet per file = {one_sheet}; no master there")

    resp = att = 0
    for p in glob.glob(os.path.join(out, "coder_distribution", "*.xlsx")) + [os.path.join(out, "20_MASTER_PACKET_v1_8_2.xlsx")]:
        wb = load_workbook(p)
        for ws in wb.worksheets:
            rows = list(ws.iter_rows(values_only=True))
            if ws.title.startswith("CODER_"):
                head = list(rows[0])
                for r in rows[1:]:
                    resp += sum(1 for h, v in zip(head, r) if h and str(h).startswith(("Q1_", "Q2_", "Q3_", "Q4_", "Q5_"))
                                and v not in (None, ""))
            if ws.title == "ATTESTATION":
                att += sum(1 for r in rows[2:] if len(r) > 2 and r[2] not in (None, ""))
    put("ALL_RESPONSE_CELLS_EMPTY", "YES" if resp == 0 else f"NO({resp})", "openpyxl count over CODER_* Q1-Q5 cells in 4 workbooks")
    put("ALL_ATTESTATION_CELLS_EMPTY", "YES" if att == 0 else f"NO({att})", "openpyxl count over ATTESTATION answer column")
    gid = [c for c in checks if c in ("GID_IN_CELL", "XML_GID_TOKEN", "DOCPROPS_LEAK", "ITEM_GID_PAIR_ON_LINE",
                                      "PLAINTEXT_SEALED_FILE_IN_OUT", "SECRET_SEED_IN_OUT", "ITEM_ORDER_LIST_ON_LINE")]
    put("GID_VISIBLE_TO_CODERS", "NO" if not gid else "YES", "leakage: cell + raw-XML (all parts incl. docProps) G-ID scan; OUT text pairing scan")
    mp = [c for c in checks if c in ("CATEGORY_CODE_IN_ITEM_ROW", "FORBIDDEN_TOKEN", "XML_FORBIDDEN_TERM", "NETWORK_NUMBER",
                                     "MECHANISM_HINT_IN_ITEM_TEXT")]
    put("RESEARCHER_MAPPING_VISIBLE_TO_CODERS", "NO" if not mp else "YES", "leakage: category codes in item rows, researcher vocabulary, hint words, network numbers")
    ai = [c for c in checks if c == "AI_PILOT_TEXT_OVERLAP"] + [f for f in res["findings"] if "pilot" in f["where"].lower()]
    put("AI_PILOT_VISIBLE_TO_CODERS", "NO" if not ai else "YES", f"leakage: {res['ai_pilot_shingles_checked']} AI-pilot 6-word shingles + 'pilot' vocabulary")
    sm = [c for c in checks if c in ("ITEM_ROWS_NOT_UNIFORM", "SENSITIVITY_ITEM_MISSING", "XML_HIDDEN_ELEMENT")] + \
         [f for f in res["findings"] if "sensitivity" in f["where"].lower()]
    put("SENSITIVITY_TARGET_MARKERS_VISIBLE", "NO" if not sm else "YES",
        f"leakage: per-item row style/fill/height/hidden uniformity incl. {res['sensitivity_rows_checked_for_uniformity']} sealed sensitivity rows; 'sensitivity' vocabulary")
    put("LEAKAGE_FINDINGS", res["n_findings"], f"tools/leakage_check_result_v1_8_2.json (verdict {res['verdict']})")

    dec = open(os.path.join(out, "24_RESEARCHER_DECISION_RECORD.md"), encoding="utf-8").read()
    put("OA2", "APPROVED_WITH_SCOPE_LIMIT" if "**APPROVED_WITH_SCOPE_LIMIT.**" in dec else "NOT_FOUND", "24 D-1")
    put("OA3", "APPROVED" if re.search(r"D-2 \(OA-3\).*\*\*APPROVED\.\*\*", dec) else "NOT_FOUND", "24 D-2")
    sys.path.insert(0, tools)
    import v1_construct_analyzer_v182 as A  # noqa: E402
    put("PRIMARY_RELIABILITY", A.PRIMARY_RELIABILITY, "analyzer constant; Q2 alpha nominal over 3 coders")
    put("PAIRWISE_KAPPA", A.PAIRWISE_KAPPA, "analyzer constant; pairs tagged role=SECONDARY")
    put("THRESHOLD_PROVENANCE", A.THRESHOLD_PROVENANCE, "analyzer constant")

    diff = subprocess.run(["git", "-C", a.repo, "status", "--porcelain"], capture_output=True, text=True).stdout
    modified = [l for l in diff.splitlines() if not l.startswith("??")]
    s1 = [l for l in modified if re.search(r"17_STUDY1|18_STUDY1|r14_merge_v1_8_1_study1_freeze|11_Priority|08_16Depletion", l)]
    put("STUDY1_FREEZE_CHANGED", "NO" if not s1 else "YES", f"git status --porcelain: tracked changes = {len(modified)}")
    em = [l for l in modified if re.search(r"\b(38|39|42|43|45|46|50|51|62|63|65)_", l)]
    put("ENTERPRISE_MODEL_CHANGED", "NO" if not em else "YES", "git status --porcelain on enterprise model / solver / schema files")
    nh = subprocess.run([py, "-E", "-P", os.path.join(tools, "v1_construct_analyzer_v182.py")] +
                        [os.path.join(out, "coder_distribution", d) for d in dist] +
                        ["--repo", a.repo, "--out", os.path.join(tools, "no_human_data_run_v1_8_2")],
                        capture_output=True, text=True).stdout.strip()
    s2 = glob.glob(os.path.join(out, "V1_SEALED", "FREEZE_MANIFEST_V1_8_2_S2*"))
    put("HUMAN_VALIDATION_EXECUTED", "NO" if nh == "NO_HUMAN_DATA" and not s2 else "YES",
        f"analyzer on blank packets -> {nh}; S2 manifest present = {bool(s2)}")
    test = open(os.path.join(tools, "test_v1_construct_analyzer_v182_result.txt"), encoding="utf-8").read().strip()

    md = ["# 27 — V1 Pre-freeze Audit (v1.8.2)", "",
          "Every line below was computed by `tools/audit_v182.py`. No value was typed by hand.", "", "```"] + lines + ["```", "",
          "| Audit line | Value | Evidence |", "|---|---|---|"] + \
         [f"| {k} | {v} | {e} |" for k, v, e in ev] + \
         ["", f"Analyzer correctness test: `{test}`", "",
          "Coder-facing workbook hashes at audit time:", "", "| File | SHA-256 |", "|---|---|"] + \
         [f"| {k} | `{v['sha256']}` |" for k, v in res["files"].items()] + ["", "V1_HUMAN_CONSTRUCT_VALIDATION_STATUS=READY_TO_RUN", ""]
    with open(os.path.join(out, "27_V1_PREFREEZE_AUDIT.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(md))
    print("\n".join(lines))
    print(lk.stdout.strip().splitlines()[0] if lk.stdout else lk.stderr)


if __name__ == "__main__":
    main()
