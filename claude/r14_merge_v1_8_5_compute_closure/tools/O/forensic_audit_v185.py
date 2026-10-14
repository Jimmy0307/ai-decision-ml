"""Orchestrator forensic audit for V1.8.4/V1.8.5 compute closure (writes 60_COMPUTE_CLOSURE_FORENSIC_AUDIT.json).

Usage: python -I forensic_audit_v185.py <out_json>
Every check re-reads files from disk; nothing is imported from the pipeline or the sub-agent tools.
"""
import csv
import glob
import hashlib
import json
import os
import subprocess
import sys

REPO = r"C:\NTUST_PAPER\outputs\00_CURRENT\02_STUDY1_FREEZE\02_STUDY1_FREEZE_V1_8_1\repo"
RPT = os.path.join(REPO, r"claude\r14_merge_v1_8_5_compute_closure")
CC = r"C:\NTUST_PAPER\outputs\00_CURRENT\06_COMPUTE_CLOSURE_V1_8_5\compute_closure"
WORK = r"C:\NTUST_PAPER\outputs\00_CURRENT\06_COMPUTE_CLOSURE_V1_8_5\work"
V5 = r"C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\04_V5_PRODUCTION_FREEZE\20260911_AI_DECISION_V5_PRODUCTION"
BASE = os.path.join(CC, r"baseline_reproduction\20261014T041645Z")
REV = os.path.join(CC, r"revised_audited_label_analysis\20261014T042729Z")
G_FILE = os.path.join(REPO, "11_Priority_Gaps_Frozen_Export_G01_G16_v1_0_20261009.csv")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def rows(path):
    return list(csv.DictReader(open(path, encoding="utf-8-sig")))


def find(root, name):
    hits = glob.glob(os.path.join(root, "**", name), recursive=True)
    if len(hits) != 1:
        raise RuntimeError(f"expected exactly one {name} under {root}, found {len(hits)}")
    return hits[0]


def check_baseline_13():
    out = []
    for r in rows(os.path.join(RPT, "46_OFFICIAL_13_OUTPUT_MANIFEST.csv")):
        repro = find(BASE, r["filename"]) if r["filename"] != "FINAL_ROBUST_CORE_32.csv" else find(BASE, "FINAL_ROBUST_CORE_32.csv")
        out.append(dict(id=r["output_id"], file=r["filename"], historical=r["historical_sha256"], repro=sha(repro),
                        source_now=sha(r["current_source_path"])))
    ok = sum(o["historical"] == o["repro"] == o["source_now"] for o in out)
    return dict(n=len(out), byte_identical=ok, detail=out)


def check_propagation():
    man = rows(os.path.join(RPT, "44_PROPAGATION_RECORD_MANIFEST.csv"))
    ids = [r["record_id"] for r in man]
    classes = {c: sum(r["precedence_class"] == c for r in man) for c in set(r["precedence_class"] for r in man)}
    base_freeze = find(V5, "ANALYTICAL_FREEZE_RECORD_LEVEL.csv")
    rev_freeze = find(REV, "ANALYTICAL_FREEZE_RECORD_LEVEL.csv")
    b = {r["record_id"]: r for r in rows(base_freeze)}
    v = {r["record_id"]: r for r in rows(rev_freeze)}
    targets = set(ids)
    non_target_changed = [k for k in b if k not in targets and b[k] != v.get(k)]
    target_changed = [k for k in targets if b[k] != v[k]]
    return dict(manifest_rows=len(man), unique=len(set(ids)), classes=classes, base_rows=len(b), revised_rows=len(v),
                same_keyset=set(b) == set(v), non_target_rows_changed=len(non_target_changed),
                target_rows_changed=len(target_changed))


def check_cells_and_core():
    cells = rows(os.path.join(RPT, "52_ALL_120_CELLS_BASELINE_VS_REVISED.csv"))
    core_b = rows(find(BASE, "FINAL_ROBUST_CORE_32.csv"))
    core_r = rows(find(REV, "FINAL_ROBUST_CORE_32.csv"))
    kb = {(r["ai_family"], r["decision_family"]): r["direction"] for r in core_b}
    kr = {(r["ai_family"], r["decision_family"]): r["direction"] for r in core_r}
    g = [(r["AI_Family"], r["Decision_Family"]) for r in rows(G_FILE)]
    edges_r = len(rows(find(REV, "DOCUMENT_PAIR_EDGES_DEDUP.csv")))
    elig_r = rows(find(REV, "ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv"))
    return dict(cells_rows=len(cells), cells_unique=len({(r["AI_family"], r["Decision_family"]) for r in cells}),
                core_baseline=len(kb), core_revised=len(kr),
                enriched_baseline=sum(d == "ENRICHED" for d in kb.values()), depleted_baseline=sum(d == "DEPLETED" for d in kb.values()),
                enriched_revised=sum(d == "ENRICHED" for d in kr.values()), depleted_revised=sum(d == "DEPLETED" for d in kr.values()),
                gained=sorted(" x ".join(k) for k in set(kr) - set(kb)), lost=sorted(" x ".join(k) for k in set(kb) - set(kr)),
                shared_direction_changed=sum(kb[k] != kr[k] for k in set(kb) & set(kr)),
                g_removed=sum(k not in kr for k in g), g_direction_changed=sum(kr.get(k) not in (None, "DEPLETED") for k in g),
                g_baseline_all_depleted=all(kb.get(k) == "DEPLETED" for k in g),
                edges_revised=edges_r, eligible_revised=len(elig_r), docs_revised=len({r["document_id"] for r in elig_r}),
                core_revised_sha=sha(find(REV, "FINAL_ROBUST_CORE_32.csv")))


def check_reruns():
    def stage_files(root, stage):
        return {os.path.basename(p): sha(p) for p in glob.glob(os.path.join(root, stage, "**", "*.*"), recursive=True) if os.path.isfile(p)}
    res = {}
    for stage in ("10_DOCUMENT_DEDUP_MATRIX", "11_NULL_MODEL_NETWORK", "12_ROBUSTNESS_SENSITIVITY", "13_RESULTS_FREEZE"):
        b, r = stage_files(BASE, stage), stage_files(REV, stage)
        res[stage] = dict(baseline_files=len(b), revised_files=len(r), revised_differs_from_baseline=sum(b.get(k) != v for k, v in r.items()))
    return res


def check_protection():
    snap = open(os.path.join(WORK, "PROTECTION_SNAPSHOT_GIT_BLOBS.txt"), encoding="utf-8").read().splitlines()
    now = subprocess.run(["git", "-C", REPO, "ls-files", "-s", "claude/r14_merge_v1_8_2_v1_prefreeze", "42_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md",
                          "51_enterprise_portfolio_solver_v2_2.py", "62_ENTERPRISE_EMPIRICAL_DATA_TEMPLATE_v2_3", "65_enterprise_data_loader_v2_3.py"],
                         capture_output=True, text=True).stdout.splitlines()
    dirty = subprocess.run(["git", "-C", REPO, "status", "--porcelain", "--", "claude/r14_merge_v1_8_2_v1_prefreeze", "42_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md",
                            "51_enterprise_portfolio_solver_v2_2.py", "62_ENTERPRISE_EMPIRICAL_DATA_TEMPLATE_v2_3", "65_enterprise_data_loader_v2_3.py"],
                           capture_output=True, text=True).stdout.strip()
    v5_snap = {}
    for line in open(os.path.join(WORK, "V5_PRE_RUN_SNAPSHOT.sha256"), encoding="utf-8"):
        h, p = line.rstrip("\n").split(None, 1)
        v5_snap[p.lstrip("*").lstrip("./")] = h
    changed = [p for p, h in v5_snap.items() if not os.path.isfile(os.path.join(V5, p)) or sha(os.path.join(V5, p)) != h]
    count_now = sum(len(fn) for _, _, fn in os.walk(V5))
    return dict(v1_s1_and_enterprise_blobs_identical=snap == now, protected_worktree_dirty=bool(dirty),
                v5_files_snapshot=len(v5_snap), v5_files_now=count_now, v5_changed_or_missing=len(changed))


def main():
    out = dict(baseline_13=check_baseline_13(), propagation=check_propagation(), cells_core_g=check_cells_and_core(),
               reruns=check_reruns(), protection=check_protection())
    json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    s = dict(out)
    s["baseline_13"] = {k: v for k, v in out["baseline_13"].items() if k != "detail"}
    print(json.dumps(s, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
