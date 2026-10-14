"""Match V9 PROTECTED_ARTIFACTS_BASELINE_20261003.csv entries (and known missing hashes) against the
V5 production folder by full SHA-256. Usage: python -I v5_protected_match.py <v5_dir> <baseline_csv> <out_csv>"""
import csv, hashlib, os, sys
v5, base, out = sys.argv[1:4]
KNOWN = {"a43b4b5897bb8b1dabfe251aa52b95da8f35b6951c98ada7c92663291770bd50": "Official final core (recorded NOT_RECOVERED/PROBABLE in V1.8/V1.8.1)",
         "4e412a07af1f5c9e2f304408875fc1fc47018c9ff501a17dee437bea880e95a0": "Sidecar core (recorded NOT_SHIPPED)"}
rows = list(csv.DictReader(open(base, encoding="utf-8-sig")))
hcol = next(c for c in rows[0] if "sha" in c.lower())
pcol = next((c for c in rows[0] if "path" in c.lower()), list(rows[0])[0])
prot = {r[hcol].lower(): r[pcol] for r in rows if r[hcol]}
found = {}
for dp, dn, fn in os.walk(v5):
    for f in fn:
        p = os.path.join(dp, f)
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for b in iter(lambda: fh.read(1 << 20), b""): h.update(b)
        d = h.hexdigest()
        if d in prot or d in KNOWN:
            found.setdefault(d, []).append(os.path.relpath(p, v5))
with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["sha256", "protected_baseline_entry", "known_missing_label", "status", "locations_in_v5_production"])
    for d, entry in sorted(prot.items(), key=lambda t: t[1]):
        w.writerow([d, entry, KNOWN.get(d, ""), "FOUND" if d in found else "NOT_FOUND_IN_V5_PRODUCTION", " | ".join(found.get(d, []))])
    for d, lab in KNOWN.items():
        if d not in prot:
            w.writerow([d, "", lab, "FOUND" if d in found else "NOT_FOUND_IN_V5_PRODUCTION", " | ".join(found.get(d, []))])
print("baseline entries", len(prot), "found", sum(d in found for d in prot), "| known:", {KNOWN[k][:20]: k in found for k in KNOWN})
