import sys, os, hashlib, csv, zipfile, datetime, pathlib
W = pathlib.Path(sys.argv[1])
INPUTS = [("01_ALL_OUTPUTS", r"C:\Users\user\Downloads\AI_DECISION_THESIS_ALL_OUTPUTS_20261014.zip"),
          ("02_V9_HUMAN_VALIDATION", r"C:\NTUST_PAPER\outputs\20260929_V9_HUMAN_VALIDATION.zip"),
          ("03_LEGACY_FULL_SOURCE", r"C:\NTUST_PAPER\read\generated_v2\完整資料來源.zip")]
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
W.mkdir(parents=True, exist_ok=True)
rows = []
for pkg, p in INPUTS:
    st = os.stat(p)
    rows.append(dict(source_package=pkg, absolute_path=p, file_size=st.st_size, sha256=sha(p),
        modified_time=datetime.datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds")))
with open(W/"00_INPUT_MANIFEST.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
with open(W/"00_INPUT_HASHES.txt", "w", encoding="utf-8") as f:
    for r in rows: f.write(f"{r['sha256']}  {r['absolute_path']}\n")
inv = []
for pkg, p in INPUTS:
    dest = W/pkg; dest.mkdir(exist_ok=True)
    with zipfile.ZipFile(p) as z:
        for info in z.infolist():
            name = info.filename
            if not (info.flag_bits & 0x800):
                try: name = name.encode("cp437").decode("cp950")
                except Exception: pass
            rel = pathlib.PurePosixPath(name)
            if rel.is_absolute() or ".." in rel.parts: print("SKIP unsafe", name); continue
            out = dest.joinpath(*rel.parts)
            if info.is_dir(): out.mkdir(parents=True, exist_ok=True); continue
            out.parent.mkdir(parents=True, exist_ok=True)
            with z.open(info) as src, open(out, "wb") as dst:
                while b := src.read(1 << 20): dst.write(b)
            mt = datetime.datetime(*info.date_time).isoformat()
            inv.append(dict(source_package=pkg, relative_path=str(rel), extension=out.suffix.lower(),
                size=info.file_size, modified_time=mt, sha256=sha(out)))
with open(W/"01_FILE_INVENTORY.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(inv[0])); w.writeheader(); w.writerows(inv)
# verify zips unchanged
for r in rows: assert sha(r["absolute_path"]) == r["sha256"], r
from collections import Counter
print(Counter(r["source_package"] for r in inv))
