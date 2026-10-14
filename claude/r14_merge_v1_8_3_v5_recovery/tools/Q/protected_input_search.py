"""V1.8.3 sub-agent Q: search for the 37 V9 protected inputs across the workspace.

Read-only. Candidate selection by case-insensitive basename or exact byte size
(from PROTECTED_ARTIFACTS_BASELINE_20261003.csv); only candidates are hashed.
Zip archives are listed and candidate members hashed in memory (no extraction).

Usage: python -I protected_input_search.py BASELINE_CSV OUT_JSON ROOT [ROOT ...] [--names-only ROOT ...]
"""
import csv
import hashlib
import json
import os
import sys
import zipfile

SIDECAR_SHA = "4e412a07af1f5c9e2f304408875fc1fc47018c9ff501a17dee437bea880e95a0"
SIDECAR_HINTS = ("sidecar", "robust_core")
CHUNK = 1 << 20


def load_baseline(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    return [{"path": r["path"], "sha256": r["sha256"].lower(), "bytes": int(r["bytes"])} for r in rows]


def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def sha_member(zf, info):
    h = hashlib.sha256()
    with zf.open(info) as fh:
        for block in iter(lambda: fh.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def walk(root):
    stack = [root]
    while stack:
        d = stack.pop()
        try:
            with os.scandir(d) as it:
                for e in it:
                    try:
                        if e.is_symlink():
                            continue
                        if e.is_dir(follow_symlinks=False):
                            stack.append(e.path)
                        elif e.is_file(follow_symlinks=False):
                            yield e.path, e.name, e.stat(follow_symlinks=False).st_size
                    except OSError as exc:
                        yield None, str(exc), -1
        except OSError as exc:
            yield None, f"{d}: {exc}", -1


def is_candidate(name, size, names, sizes, names_only):
    low = name.lower()
    if low in names:
        return "name"
    if not names_only and size in sizes:
        return "size"
    if any(h in low for h in SIDECAR_HINTS) and low.endswith(".csv"):
        return "sidecar_hint"
    return None


def scan(roots, names_only_roots, baseline):
    names = {os.path.basename(r["path"]).lower() for r in baseline}
    sizes = {r["bytes"] for r in baseline}
    targets = {r["sha256"] for r in baseline} | {SIDECAR_SHA}
    hits, cands, errors, stats = [], [], [], {"files": 0, "zips": 0, "zip_members": 0, "hashed": 0}

    def record(loc, name, size, why, digest):
        cands.append({"location": loc, "name": name, "bytes": size, "why": why, "sha256": digest,
                      "target_hit": digest in targets})
        if digest in targets:
            hits.append({"location": loc, "sha256": digest, "bytes": size})

    for root, names_only in [(r, False) for r in roots] + [(r, True) for r in names_only_roots]:
        for path, name, size in walk(root):
            if path is None:
                errors.append(name)
                continue
            stats["files"] += 1
            why = is_candidate(name, size, names, sizes, names_only)
            if why:
                try:
                    record(path, name, size, why, sha_file(path))
                    stats["hashed"] += 1
                except OSError as exc:
                    errors.append(f"{path}: {exc}")
            if name.lower().endswith(".zip"):
                stats["zips"] += 1
                try:
                    with zipfile.ZipFile(path) as zf:
                        for info in zf.infolist():
                            if info.is_dir():
                                continue
                            stats["zip_members"] += 1
                            mname = info.filename.rsplit("/", 1)[-1]
                            mwhy = is_candidate(mname, info.file_size, names, sizes, names_only)
                            if mwhy:
                                try:
                                    record(f"{path}!{info.filename}", mname, info.file_size, mwhy,
                                           sha_member(zf, info))
                                    stats["hashed"] += 1
                                except Exception as exc:  # noqa: BLE001 - record any member read failure
                                    errors.append(f"{path}!{info.filename}: {exc}")
                except Exception as exc:  # noqa: BLE001 - corrupt/encrypted zips are recorded
                    errors.append(f"{path}: zip {exc}")
    return {"stats": stats, "hits": hits, "candidates": cands, "errors": errors}


def main(argv):
    baseline_csv, out_json = argv[1], argv[2]
    rest = argv[3:]
    if "--names-only" in rest:
        i = rest.index("--names-only")
        roots, names_only = rest[:i], rest[i + 1:]
    else:
        roots, names_only = rest, []
    baseline = load_baseline(baseline_csv)
    result = scan(roots, names_only, baseline)
    result["baseline"] = baseline
    result["roots"] = roots
    result["names_only_roots"] = names_only
    with open(out_json, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1)
    print(json.dumps(result["stats"]), len(result["hits"]), "hits", len(result["errors"]), "errors")


if __name__ == "__main__":
    main(sys.argv)
