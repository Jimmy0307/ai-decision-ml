"""Sub-agent A: V9 source-authority scan (read-only over W).
Usage: python -I authority_scan.py <W_root> <out_dir>
Outputs: inventory_check.json, hash_claims.csv, hash_citations.csv, name_citations.json
"""
import csv, hashlib, json, os, re, sys
from collections import defaultdict

W = sys.argv[1]
OUT = sys.argv[2]
V9 = os.path.join(W, "02_V9_HUMAN_VALIDATION", "20260929_V9_HUMAN_VALIDATION")
PKGS = ["01_ALL_OUTPUTS", "02_V9_HUMAN_VALIDATION", "03_LEGACY_FULL_SOURCE"]
TEXT_EXT = {".md", ".txt", ".json", ".csv", ".jsonl", ".sha256", ".html", ".js", ".py"}
HEX = re.compile(r"\b[0-9A-Fa-f]{64}\b")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def read_text(p):
    with open(p, "rb") as f:
        raw = f.read()
    for enc in ("utf-8-sig", "cp950", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return ""


# 1. actual hashes for every extracted file
actual = {}  # (pkg, rel) -> sha
by_hash = defaultdict(list)
for pkg in PKGS:
    base = os.path.join(W, pkg)
    for dp, _, fns in os.walk(base):
        for fn in fns:
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, base).replace("\\", "/")
            h = sha(p)
            actual[(pkg, rel)] = h
            by_hash[h].append(f"{pkg}/{rel}")

# 2. inventory check
inv = {}
with open(os.path.join(W, "01_FILE_INVENTORY.csv"), encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        inv[(r["source_package"], r["relative_path"])] = r
match = mismatch = missing_on_disk = 0
mism = []
for k, r in inv.items():
    if k not in actual:
        missing_on_disk += 1
        mism.append({"key": "/".join(k), "issue": "IN_INVENTORY_NOT_ON_DISK"})
    elif actual[k].lower() == r["sha256"].lower():
        match += 1
    else:
        mismatch += 1
        mism.append({"key": "/".join(k), "issue": "SHA_MISMATCH"})
not_in_inv = [("/".join(k)) for k in actual if k not in inv]
json.dump({"inventory_rows": len(inv), "files_on_disk": len(actual), "match": match,
           "mismatch": mismatch, "missing_on_disk": missing_on_disk,
           "on_disk_not_in_inventory": not_in_inv, "problems": mism},
          open(os.path.join(OUT, "inventory_check.json"), "w", encoding="utf-8"), indent=1)

V9KEY = "20260929_V9_HUMAN_VALIDATION/"


def v9_actual(name):
    return actual.get(("02_V9_HUMAN_VALIDATION", V9KEY + name))


claims = []  # source, target, claimed, actual, status


def add(src, target, claimed, act_override=None, note=""):
    a = act_override if act_override is not None else v9_actual(target)
    if a is None:
        alt = by_hash.get(claimed.lower(), [])
        status = "TARGET_NOT_IN_PACKAGE" + ("; HASH_FOUND_AT:" + "|".join(alt[:3]) if alt else "; HASH_NOT_FOUND_ANYWHERE")
    else:
        status = "MATCH" if a.lower() == claimed.lower() else "MISMATCH"
    claims.append([src, target, claimed.lower(), (a or ""), status, note])


# a. FINAL_ARTIFACT_HASH_MANIFEST
with open(os.path.join(V9, "FINAL_ARTIFACT_HASH_MANIFEST.csv"), encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        add("FINAL_ARTIFACT_HASH_MANIFEST.csv", r["relative_path"], r["sha256"])
# b. detached .sha256 "HASH  name" files and KEY=HASH files
for fn in sorted(os.listdir(V9)):
    p = os.path.join(V9, fn)
    if not os.path.isfile(p):
        continue
    if fn.endswith(".sha256") or fn.endswith("_SHA256.txt"):
        txt = read_text(p)
        kv = {}
        for line in txt.splitlines():
            m = re.match(r"^([0-9A-Fa-f]{64})\s+\*?(\S.*)$", line.strip())
            if m:
                add(fn, m.group(2).strip(), m.group(1))
                continue
            m = re.match(r"^(\S[^:=]*?)\s*(?:=|SHA-256:)\s*(.+)$", line.strip())
            if m:
                kv[m.group(1).strip()] = m.group(2).strip()
        # KEY=VALUE conventions: X=<file>, X_SHA256=<hash>
        for k, v in kv.items():
            if HEX.fullmatch(v):
                stem = k[:-7] if k.endswith("_SHA256") else k
                target = kv.get(stem)
                if target and not HEX.fullmatch(target):
                    add(fn, target, v)
                elif k.endswith(".csv") or k.endswith(".md"):
                    add(fn, k.split()[0], v)
                else:
                    add(fn, "(key)" + k, v, act_override="", note="no direct target; resolved by hash")
# c. protected / startup baselines
for fn, pcol in (("PROTECTED_ARTIFACTS_BASELINE_20261003.csv", "path"), ("STARTUP_HASH_BASELINE.csv", "path")):
    with open(os.path.join(V9, fn), encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            path = r[pcol].replace("\\", "/")
            if "outputs/20260929_V9_HUMAN_VALIDATION/" in path:
                add(fn, path.split("outputs/20260929_V9_HUMAN_VALIDATION/")[1], r["sha256"])
            else:
                add(fn, "(external)" + path, r["sha256"], act_override="", note="external path")
# d. epoch2 log artifact hashes
with open(os.path.join(V9, "HUMAN_AUDIT_EPOCH2_LOG.csv"), encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        add("HUMAN_AUDIT_EPOCH2_LOG.csv:" + r["event_id"], r["artifact_path"], r["artifact_sha256"])
# e. json status fields
for fn in ("FINAL_STATUS.json", "HUMAN_AUDIT_STATUS.json", "ROBUST_CORE_LOCAL_SENSITIVITY_STATUS.json"):
    d = json.load(open(os.path.join(V9, fn), encoding="utf-8-sig"))

    def walk(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, path + "." + k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{path}[{i}]")
        elif isinstance(o, str) and HEX.fullmatch(o):
            add(fn + path, "(field)", o, act_override="", note="resolved by hash")
    walk(d)

# resolve "(...)" claims purely by hash lookup
for c in claims:
    if c[1].startswith("("):
        hits = by_hash.get(c[2], [])
        c[4] = ("HASH_FOUND_AT:" + "|".join(hits[:4])) if hits else "HASH_NOT_FOUND_IN_EXTRACTED_PACKAGES"
with open(os.path.join(OUT, "hash_claims.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["claim_source", "target", "claimed_sha256", "actual_sha256", "status", "note"])
    w.writerows(claims)

# 3. hash citation graph: every 64-hex token in V9 root text files + 01 r14_merge_v1_7 128/131 docs
cit_rows = []
scan_files = [os.path.join(V9, fn) for fn in os.listdir(V9)
              if os.path.isfile(os.path.join(V9, fn)) and os.path.splitext(fn)[1].lower() in TEXT_EXT]
v17 = os.path.join(W, "01_ALL_OUTPUTS", "AI_DECISION_THESIS_ALL_OUTPUTS", "r14_merge_v1_7")
if os.path.isdir(v17):
    scan_files += [os.path.join(v17, fn) for fn in os.listdir(v17)
                   if os.path.splitext(fn)[1].lower() in {".md", ".json", ".csv", ".txt"}]
for p in scan_files:
    txt = read_text(p)
    for h in sorted(set(x.lower() for x in HEX.findall(txt))):
        hits = by_hash.get(h, [])
        cit_rows.append([os.path.relpath(p, W).replace("\\", "/"), h, "|".join(hits) if hits else "NOT_FOUND"])
with open(os.path.join(OUT, "hash_citations.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["citing_file", "sha256", "resolves_to"])
    w.writerows(cit_rows)

# 4. name citations for priority targets across all three packages (text files only)
targets = ["FINAL_HUMAN_AUDIT_DECISION_FINAL", "FINAL_HUMAN_AUDIT_DECISION.md", "FINAL_HUMAN_AUDIT_REPORT",
           "FINAL_SUBMISSION_READINESS_REPORT", "FINAL_STATUS.json", "FINAL_STATUS.md", "HUMAN_AUDIT_STATUS",
           "V9_FINAL_FORENSIC_AUDIT", "HUMAN_RELIABILITY_FINAL", "HUMAN_RELIABILITY_20",
           "ROBUST_CORE_LOCAL_SENSITIVITY", "HUMAN_RECONCILIATION_GATE_STATUS", "HUMAN_AUDIT_EPOCH2",
           "ACCIDENTAL_SUBMISSION_REOPEN_REPORT", "RECORD_REOPEN_AUDIT_LOG", "FINAL_ARTIFACT_HASH_MANIFEST",
           "PROTECTED_ARTIFACTS_BASELINE_20261003", "STARTUP_HASH_BASELINE", "V9_1_SEGMENTATION_SENSITIVITY",
           "HUMAN_RECONCILED_20", "MODEL_VS_RECONCILED_20", "FIRST_CODER_50_FINAL_FROZEN",
           "BLIND_REPEAT_20_FINAL_FROZEN", "SEGMENTATION_SENSITIVITY_FINAL_REPORT", "V9_HUMAN_AUDIT_PATCHED_CANDIDATE"]
name_cit = {t: [] for t in targets}
for (pkg, rel) in actual:
    if os.path.splitext(rel)[1].lower() not in {".md", ".txt", ".json", ".csv", ".jsonl"}:
        continue
    p = os.path.join(W, pkg, rel)
    if os.path.getsize(p) > 3_000_000:
        txt = read_text(p)
    else:
        txt = read_text(p)
    for t in targets:
        if t in txt and not rel.endswith("/" + t) and os.path.basename(rel) != t:
            name_cit[t].append(f"{pkg}/{rel}")
json.dump(name_cit, open(os.path.join(OUT, "name_citations.json"), "w", encoding="utf-8"), indent=1)
print("done", len(actual), "files;", match, "inventory matches;", mismatch, "mismatches;",
      len(claims), "hash claims")
