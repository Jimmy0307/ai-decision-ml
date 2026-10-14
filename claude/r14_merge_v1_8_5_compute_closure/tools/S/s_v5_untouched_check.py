"""Recompute SHA-256 of every file under V5 (read-only) and compare with WORK\\V5_PRE_RUN_SNAPSHOT.sha256.
Usage: python -I -B s_v5_untouched_check.py <snapshot_file> <out_json>
Snapshot line format: '<sha256> *./<relative/path>'.
"""
import hashlib
import json
import sys
from pathlib import Path

V5 = Path(r"C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\04_V5_PRODUCTION_FREEZE\20260911_AI_DECISION_V5_PRODUCTION")


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    snap, out = Path(sys.argv[1]), Path(sys.argv[2])
    expected = {}
    for line in snap.read_text(encoding="utf-8").splitlines():
        if line.strip():
            h, rel = line.split(" ", 1)
            expected[rel.lstrip("*").removeprefix("./")] = h.lower()
    current = {p.relative_to(V5).as_posix(): sha(p) for p in V5.rglob("*") if p.is_file()}
    changed = sorted(k for k in expected if k in current and current[k] != expected[k])
    missing = sorted(k for k in expected if k not in current)
    added = sorted(k for k in current if k not in expected)
    res = {"snapshot": str(snap), "snapshot_sha256": sha(snap), "snapshot_entries": len(expected),
           "current_files": len(current), "changed": changed, "missing": missing, "added": added,
           "V5_UNTOUCHED": "YES" if not (changed or missing or added) else "NO"}
    out.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in res.items()}))


if __name__ == "__main__":
    main()
