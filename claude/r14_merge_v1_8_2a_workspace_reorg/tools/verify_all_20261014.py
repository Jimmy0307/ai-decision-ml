"""Post-reorganization verification of every frozen record (2026-10-14).

Usage: python -I verify_all_20261014.py <out_json>
Checks:
  A  local copies in outputs\\00_CURRENT equal the committed blobs in the git working copy
  B  V1.8.2 S1 freeze manifest (committed files + sealed plaintext at its new location)
  C  V1.8.1 Study 1 freeze ledger (18): repo rows, raw-source rows (V1.8 workspace, new location), external R14 docx
  D  V1.8 file inventory (1,295 extracted files) at the new V1.8 workspace location
  E  V1.8 input zips (00_INPUT_MANIFEST.csv) at their current locations
  F  reorganization move manifest (71 rows)
"""
import csv
import hashlib
import json
import os
import sys

O = r"C:\NTUST_PAPER\outputs"
REPO = os.path.join(O, r"00_CURRENT\02_STUDY1_FREEZE\02_STUDY1_FREEZE_V1_8_1\repo")
V182 = os.path.join(REPO, r"claude\r14_merge_v1_8_2_v1_prefreeze")
V181 = os.path.join(REPO, r"claude\r14_merge_v1_8_1_study1_freeze")
V18 = os.path.join(REPO, r"claude\r14_merge_v1_8_source_closure")
W = os.path.join(O, r"10_CANONICAL_EVIDENCE\03_R14_STUDY1\01_SOURCE_CLOSURE_V1_8")
SEALED = os.path.join(O, r"20_SEALED_PRIVATE\V1_8_2_STUDY_TEAM_ONLY")
REORG = os.path.join(O, r"00_CURRENT\04_CURRENT_STATUS\_reorg_20261014")
_cache = {}


def sha(path):
    if path not in _cache:
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for block in iter(lambda: fh.read(1 << 20), b""):
                h.update(block)
        _cache[path] = h.hexdigest()
    return _cache[path]


def tally(results):
    return {"ok": sum(r[-1] == "OK" for r in results), "fail": [r for r in results if r[-1] != "OK"]}


def check_copies():
    res = []
    pairs = []
    for d, dn, fn in os.walk(os.path.join(O, "00_CURRENT")):
        if "repo" in dn and d.endswith("02_STUDY1_FREEZE_V1_8_1"):
            dn.remove("repo")
        dn[:] = [x for x in dn if x not in ("_reorg_20261014", ".venv_docx")]
        for f in fn:
            pairs.append(os.path.join(d, f))
    index = {}
    for d, dn, fn in os.walk(os.path.join(REPO, "claude")):
        for f in fn:
            index.setdefault(f, []).append(os.path.join(d, f))
    for p in pairs:
        f = os.path.basename(p)
        cands = index.get(f, [])
        if not cands:
            res.append([p, "NO_REPO_COUNTERPART", "INFO"])
            continue
        res.append([p, cands[0], "OK" if any(sha(p) == sha(c) for c in cands) else "DIFFERS_FROM_REPO"])
    return res


def check_s1():
    res = []
    for line in open(os.path.join(V182, r"V1_SEALED\FREEZE_MANIFEST_V1_8_2_S1.txt"), encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        h, path = line.split()[0], line.split()[-1]
        p = os.path.join(SEALED, path.split(":", 1)[1]) if path.startswith("SEALED_LOCAL:") else os.path.join(V182, path)
        res.append([path, "OK" if os.path.isfile(p) and sha(p) == h else "FAIL"])
    return res


def check_ledger18():
    res = []
    for r in csv.DictReader(open(os.path.join(V181, "18_STUDY1_FREEZE_HASHES.csv"), encoding="utf-8")):
        if not r["sha256"]:
            res.append([r["artifact"], r["status"], "SKIP_NOT_RECOVERED"])
            continue
        p = r["path"]
        if p.startswith("repo:"):
            loc = os.path.join(REPO, p[5:])
        elif p.startswith("W:"):
            loc = os.path.join(W, p[2:])
        else:
            loc = os.path.join(O, r"80_HISTORY_2026\10_OCT\ROOT_V9_FINAL_SUBMISSION_CANDIDATES_20261004", os.path.basename(p))
        res.append([r["artifact"], loc, "OK" if os.path.isfile(loc) and sha(loc) == r["sha256"] else "FAIL"])
    return res


def check_inventory():
    res = []
    for r in csv.DictReader(open(os.path.join(W, "01_FILE_INVENTORY.csv"), encoding="utf-8-sig")):
        p = os.path.join(W, r["source_package"], r["relative_path"])
        res.append([p, "OK" if os.path.isfile(p) and sha(p) == r["sha256"] else "FAIL"])
    return res


def check_zips():
    where = {
        "01_ALL_OUTPUTS": r"C:\Users\user\Downloads\AI_DECISION_THESIS_ALL_OUTPUTS_20261014.zip",
        "02_V9_HUMAN_VALIDATION": os.path.join(O, r"10_CANONICAL_EVIDENCE\01_V9_HUMAN_VALIDATION\20260929_V9_HUMAN_VALIDATION.zip"),
        "03_LEGACY_FULL_SOURCE": r"C:\NTUST_PAPER\read\generated_v2\完整資料來源.zip",
    }
    res = []
    for r in csv.DictReader(open(os.path.join(W, "00_INPUT_MANIFEST.csv"), encoding="utf-8")):
        p = where[r["source_package"]]
        res.append([r["source_package"], p, "OK" if os.path.isfile(p) and sha(p) == r["sha256"] else "FAIL"])
    return res


def check_moves():
    res = []
    for r in csv.DictReader(open(os.path.join(REORG, "MOVE_MANIFEST_20261014.csv"), encoding="utf-8")):
        new = os.path.join(r"C:\NTUST_PAPER", r["new_path"])
        old = os.path.join(r"C:\NTUST_PAPER", r["old_path"])
        ok = os.path.exists(new) and not os.path.exists(old)
        if ok and r["kind"] == "file":
            ok = sha(new) == r["fingerprint_after"]
        res.append([r["new_path"], "OK" if ok else "FAIL"])
    return res


def main():
    out = {}
    for name, fn in [("A_copies_vs_repo", check_copies), ("B_s1_manifest", check_s1), ("C_ledger18", check_ledger18),
                     ("D_v18_inventory", check_inventory), ("E_input_zips", check_zips), ("F_move_manifest", check_moves)]:
        rows = fn()
        out[name] = {"rows": len(rows), "ok": sum(r[-1] == "OK" for r in rows),
                     "other": [r for r in rows if r[-1] != "OK"]}
        print(f"{name}: rows={len(rows)} ok={out[name]['ok']} other={len(out[name]['other'])}")
        for r in out[name]["other"][:8]:
            print("   ", r)
    json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
