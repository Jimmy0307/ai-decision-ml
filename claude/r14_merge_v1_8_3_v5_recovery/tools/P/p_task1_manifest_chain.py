"""Sub-agent P, Task 1: V5 manifest-chain verification (read-only, stdlib only).

Usage: python -I p_task1_manifest_chain.py <V5_ROOT> <W_ROOT> <OUT_DIR>
Writes <OUT_DIR>/35_V5_MANIFEST_CHAIN.csv and <OUT_DIR>/35_v5_manifest_chain_raw.json
"""
import csv
import hashlib
import json
import os
import re
import sys

OLD_PREFIX = r"C:\NTUST_PAPER\outputs\20260911_AI_DECISION_V5_PRODUCTION"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
APP = r"C:\NTUST_PAPER\LocalCorpusWorkbench\v5_production_app"
_cache = {}


def sha(path):
    if path in _cache:
        return _cache[path]
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    _cache[path] = h.hexdigest()
    return _cache[path]


def remap(p, v5):
    if p and p.startswith(OLD_PREFIX):
        return v5 + p[len(OLD_PREFIX):]
    return p


def load(p):
    with open(p, encoding="utf-8-sig") as fh:
        return json.load(fh)


def claim(rows, stage, manifest, key, recorded, path, role, note=""):
    rows.append(dict(stage=stage, manifest=manifest, key=key, recorded_sha256=recorded,
                     resolved_path=path or "", role=role, note=note))


def walk_lineage(obj, prefix=""):
    """yield (key, sha, sibling_path) for every *_sha256 key in dict tree."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and HEX64.match(v) and k.endswith("sha256"):
                base = k[: -len("_sha256")] if k.endswith("_sha256") else ""
                p = None
                for cand in (base, base + "_path", base + "_canonical"):
                    if cand and isinstance(obj.get(cand), str) and ("\\" in obj[cand]):
                        p = obj[cand]
                        break
                if p is None and k == "sha256":
                    for cand in ("path", "source", "relative_path"):
                        if isinstance(obj.get(cand), str):
                            p = obj[cand]
                yield prefix + k, v, p
            elif isinstance(v, (dict, list)):
                yield from walk_lineage(v, prefix + k + ".")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_lineage(v, prefix + f"[{i}].")


def main():
    v5, w, out = sys.argv[1], sys.argv[2], sys.argv[3]
    rows = []
    S = {
        "08": os.path.join(v5, "08_FSC_STAGE3_RESIDUAL_CLOSURE", "closure_20260918T125655Z"),
        "09": os.path.join(v5, "09_ANALYTICAL_FREEZE", "analytical_freeze_v2_20260918T132206Z"),
        "10": os.path.join(v5, "10_DOCUMENT_DEDUP_MATRIX", "matrix_v1_20260918T132505Z"),
        "11": os.path.join(v5, "11_NULL_MODEL_NETWORK", "null_model_v1_20260918T132933Z"),
        "12": os.path.join(v5, "12_ROBUSTNESS_SENSITIVITY", "robustness_v1_20260918T133618Z"),
        "13": os.path.join(v5, "13_RESULTS_FREEZE", "results_freeze_v1_20260919T080120Z"),
        "13a": os.path.join(v5, "13_RESULTS_FREEZE", "results_freeze_v1_20260919T075633Z"),
        "14a": os.path.join(v5, "14_MANUSCRIPT_DATA_PACK", "data_pack_v1_20260919T081003Z"),
        "14b": os.path.join(v5, "14_MANUSCRIPT_DATA_PACK", "data_pack_v1_20260922T010012Z"),
    }
    canon = {
        "08": "STAGE3_RESIDUAL_CLOSURE_CANONICAL.json", "09": "ANALYTICAL_FREEZE_CANONICAL.json",
        "10": "DOCUMENT_DEDUP_MATRIX_CANONICAL.json", "11": "NULL_MODEL_NETWORK_CANONICAL.json",
        "12": "ROBUSTNESS_SENSITIVITY_CANONICAL.json", "13": "FINAL_RESULTS_FREEZE_CANONICAL.json",
        "13a": "FINAL_RESULTS_FREEZE_CANONICAL.json",
    }
    manifests = {
        "03": os.path.join(v5, "03_PROFILE", "V5_PRODUCTION_MANIFEST.json"),
        "06": os.path.join(v5, "06_STATUS", "V5_EVIDENCE_FREEZE_REPORT.json"),
        "08": os.path.join(S["08"], "STAGE3_RESIDUAL_CLOSURE_MANIFEST.json"),
        "09": os.path.join(S["09"], "ANALYTICAL_FREEZE_MANIFEST_V2.json"),
        "10": os.path.join(S["10"], "DOCUMENT_DEDUP_MATRIX_MANIFEST.json"),
        "11": os.path.join(S["11"], "NULL_MODEL_NETWORK_MANIFEST.json"),
        "12": os.path.join(S["12"], "ROBUSTNESS_SENSITIVITY_MANIFEST.json"),
        "13": os.path.join(S["13"], "FINAL_RESULTS_FREEZE_MANIFEST.json"),
    }
    # implied paths for hash keys without sibling path
    implied = {
        ("09", "canonical_sha256"): os.path.join(S["09"], canon["09"]),
        ("12", "lineage.robustness_sha256"): os.path.join(S["12"], canon["12"]),
        ("12", "lineage.matrix_sha256"): os.path.join(S["10"], canon["10"]),
        ("12", "lineage.null_sha256"): os.path.join(S["11"], canon["11"]),
        ("03", "fsc_definitions_sha256"): os.path.join(v5, "01_FSC", "FSC_V5_USER_RATIFIED_DEFINITIONS.json"),
        ("03", "fsc_taxonomy_sha256"): os.path.join(v5, "01_FSC", "fsc_taxonomy.json"),
        ("03", "semantic_schema_sha256"): os.path.join(APP, "profiles", "AI_DECISION_V5_PRODUCTION", "semantic_schema.json"),
        ("06", "database_sha256"): os.path.join(APP, "data", "workbench.sqlite"),
        ("09", "lineage.source_db_sha256"): os.path.join(APP, "data", "workbench.sqlite"),
        ("08", "lineage.source_db_sha256"): os.path.join(APP, "data", "workbench.sqlite"),
        ("08", "lineage.closure_canonical_sha256"): os.path.join(S["08"], canon["08"]),
        ("08", "lineage.reconstructed_scope_sha256"): os.path.join(
            v5, "07_FSC_STAGE2_STRICT_V102", "provenance_recovery", "scope_reconstruction_v2_20260918T120148Z",
            "ANALYTICAL_SCOPE_MEMBERSHIP_RECONSTRUCTED_CANONICAL.json"),
        ("03", "deterministic_input.input_database_sha256"): r"C:\NTUST_PAPER\LocalCorpusWorkbench\v5_run_app5\data\workbench.sqlite",
        ("03", "track_attribution.sha256"): r"C:\NTUST_PAPER\LocalCorpusWorkbench\recovery\v5_corpus_index.csv",
    }
    payload_keys = {"formal_scope_sha256", "profile_hash", "patterns_sha256", "model_digest", "digest",
                    "input_document_hash_set", "slot_set_sha256", "scope_manifest_sha256"}
    for st, mpath in manifests.items():
        m = load(mpath)
        mrel = os.path.relpath(mpath, v5)
        for key, val, p in walk_lineage(m):
            leaf = key.split(".")[-1]
            path = remap(p, v5) if p else implied.get((st, key))
            role = "input"
            note = ""
            if st == "03" and key.startswith("configuration_file_hashes."):
                name = key[len("configuration_file_hashes."):-len(".sha256")]
                path = os.path.join(APP, "profiles", "AI_DECISION_V5_PRODUCTION", *name.split("/"))
                role = "config"
            elif st == "03" and key.startswith("binary_hashes."):
                name = key[len("binary_hashes."):-len(".sha256")]
                path = os.path.join(APP, name)
                role = "binary"
            elif st == "03" and key.startswith("prompt_hashes."):
                role = "payload_dup"
                note = "prompt hash; same values as configuration_file_hashes prompts/*"
            if path is None and (leaf in payload_keys or key.startswith("model.")):
                role = "payload"
                note = note or "payload/identity hash, not a file hash"
            if path and os.path.normcase(path).startswith(os.path.normcase(v5)) and st in S and \
                    os.path.normcase(os.path.dirname(path)) == os.path.normcase(S[st]):
                role = "output"
            claim(rows, st, mrel, key, val, path, role, note)
        # canonical self + canonical source_* fields
    for st in ("08", "09", "10", "11", "12", "13", "13a"):
        cp = os.path.join(S[st], canon[st])
        c = load(cp)
        for k, v in c.items():
            if isinstance(v, str) and HEX64.match(v):
                claim(rows, st, os.path.relpath(cp, v5), "canonical." + k, v, None, "input",
                      "source hash embedded in canonical JSON (resolved below)")
    # data packs
    for st in ("14a", "14b"):
        mp = os.path.join(S[st], "MANUSCRIPT_DATA_PACK_MANIFEST.json")
        m = load(mp)
        for g in m["generated_files"]:
            claim(rows, st, os.path.relpath(mp, v5), "generated_files:" + g["relative_path"], g["sha256"],
                  os.path.join(S[st], g["relative_path"]), "output", "size_recorded=%s" % g["size_bytes"])
        with open(os.path.join(S[st], "02_PROVENANCE_HASHES.csv"), encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                claim(rows, st, os.path.relpath(os.path.join(S[st], "02_PROVENANCE_HASHES.csv"), v5),
                      "provenance:" + r["artifact"], r["sha256"], remap(r["path"], v5), "input",
                      "expected=%s matches_expected=%s" % (r["expected_sha256"], r["matches_expected"]))
    # resolve canonical source_* by hash lookup across stage canonicals
    by_hash = {}
    for st in ("08", "09", "10", "11", "12", "13", "13a"):
        p = os.path.join(S[st], canon[st])
        by_hash.setdefault(sha(p), p)
    for r in rows:
        if r["key"].startswith("canonical.") and not r["resolved_path"]:
            r["resolved_path"] = by_hash.get(r["recorded_sha256"], "")
            if not r["resolved_path"]:
                r["note"] += "; no stage canonical has this hash"
    # verify
    for r in rows:
        p = r["resolved_path"]
        if r["role"] in ("payload", "payload_dup"):
            r["actual_sha256"], r["status"] = "", "NOT_A_FILE_HASH"
            continue
        if not p:
            r["actual_sha256"], r["status"] = "", "UNRESOLVED_PATH"
            continue
        if not os.path.isfile(p):
            r["actual_sha256"], r["status"] = "", "MISSING"
            continue
        a = sha(p)
        r["actual_sha256"] = a
        r["status"] = "VERIFIED" if a == r["recorded_sha256"] else "MISMATCH"
        r["actual_size"] = os.path.getsize(p)
    # 13a/13b + 14a/14b byte comparisons
    comps = []
    for a_st, b_st in (("13a", "13"), ("14a", "14b")):
        names = set()
        for st in (a_st, b_st):
            for dp, _, fs in os.walk(S[st]):
                for f in fs:
                    names.add(os.path.relpath(os.path.join(dp, f), S[st]))
        for n in sorted(names):
            pa, pb = os.path.join(S[a_st], n), os.path.join(S[b_st], n)
            ha = sha(pa) if os.path.isfile(pa) else ""
            hb = sha(pb) if os.path.isfile(pb) else ""
            comps.append(dict(pair=f"{a_st}_vs_{b_st}", file=n, sha_a=ha, sha_b=hb,
                              size_a=os.path.getsize(pa) if ha else "", size_b=os.path.getsize(pb) if hb else "",
                              identical=(ha == hb and ha != "")))
    # zips
    zips = {}
    zd = os.path.join(v5, "14_MANUSCRIPT_DATA_PACK")
    for f in os.listdir(zd):
        if f.endswith(".zip"):
            zips[f] = dict(sha256=sha(os.path.join(zd, f)), size=os.path.getsize(os.path.join(zd, f)))
    # LATEST pointers
    latest = []
    for dp, _, fs in os.walk(v5):
        if os.sep + "work" in dp:
            continue
        for f in fs:
            if f.startswith("LATEST_") and f.endswith(".txt"):
                with open(os.path.join(dp, f), encoding="utf-8-sig") as fh:
                    tgt = fh.read().strip()
                rt = remap(tgt, v5)
                latest.append(dict(pointer=os.path.relpath(os.path.join(dp, f), v5), target_recorded=tgt,
                                   target_remapped=rt, exists_old_path=os.path.exists(tgt),
                                   exists_remapped=os.path.isdir(rt)))
    # V9.1 baseline reproduction comparison
    v91 = os.path.join(w, "02_V9_HUMAN_VALIDATION", "20260929_V9_HUMAN_VALIDATION",
                       "V9_1_SEGMENTATION_SENSITIVITY", "_baseline_reproduction")
    v5_index = {}
    for st in ("08", "09", "10", "11", "12", "13", "13a", "14a", "14b"):
        for dp, _, fs in os.walk(S[st]):
            for f in fs:
                p = os.path.join(dp, f)
                v5_index.setdefault(sha(p), []).append(os.path.relpath(p, v5))
    v91cmp = []
    if os.path.isdir(v91):
        for dp, _, fs in os.walk(v91):
            for f in fs:
                p = os.path.join(dp, f)
                h = sha(p)
                same_name = [os.path.relpath(os.path.join(d2, f2), v5) for st in S.values()
                             for d2, _, f2s in os.walk(st) for f2 in f2s if f2 == f]
                v91cmp.append(dict(file=os.path.relpath(p, v91), sha256=h, size=os.path.getsize(p),
                                   v5_hash_matches=";".join(v5_index.get(h, [])),
                                   v5_same_name=";".join(same_name)))
    os.makedirs(out, exist_ok=True)
    fields = ["stage", "manifest", "key", "role", "recorded_sha256", "actual_sha256", "status",
              "resolved_path", "actual_size", "note"]
    with open(os.path.join(out, "35_V5_MANIFEST_CHAIN.csv"), "w", encoding="utf-8", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        wr.writeheader()
        for r in rows:
            wr.writerow({k: r.get(k, "") for k in fields})
    with open(os.path.join(out, "35_v5_manifest_chain_raw.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(dict(comparisons=comps, zips=zips, latest=latest, v91=v91cmp), fh, indent=1)
    # console summary
    from collections import Counter
    c = Counter((r["stage"], r["status"]) for r in rows)
    for k in sorted(c):
        print(k, c[k])
    for r in rows:
        if r["status"] not in ("VERIFIED", "NOT_A_FILE_HASH"):
            print("!!", r["stage"], r["key"], r["status"], r["resolved_path"], r.get("note", ""))


if __name__ == "__main__":
    main()
