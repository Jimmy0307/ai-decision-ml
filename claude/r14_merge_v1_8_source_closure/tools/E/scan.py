import sys, re, os, json, csv
D = sys.argv[1]
OUT = sys.argv[2]
pats = ["pending verification","待核","待確認","待驗證","待查","source unavailable","artifact missing","2026-09-29","20260929","not available in this package","not shipped","unverified","TODO","TBD",r"\[VERIFY","pending","未驗證","未提供","尚未"]
rx = re.compile("|".join(pats), re.I)
files = sorted(f for f in os.listdir(D) if re.match(r"1(2[89]|3[0-7])_.*\.(md|csv)$", f))
rows=[]
for f in files:
    head="(none)"
    with open(os.path.join(D,f), encoding="utf-8-sig", errors="replace") as fh:
        for i,line in enumerate(fh,1):
            if f.endswith(".md") and re.match(r"^#{1,6}\s", line): head=line.strip()[:120]
            for m in rx.finditer(line):
                s=max(0,m.start()-160); e=min(len(line),m.end()+160)
                rows.append(dict(file=f,line=i,section=head,match=m.group(0),ctx=line[s:e].strip()))
with open(OUT,"w",encoding="utf-8",newline="") as o:
    w=csv.DictWriter(o,fieldnames=["file","line","section","match","ctx"]); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows)); print(Counter((r["file"],r["match"].lower()) for r in rows))
