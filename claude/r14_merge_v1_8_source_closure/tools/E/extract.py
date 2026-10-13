"""Extract flag occurrences (one row per file/line/flag phrase) from v1.7 artifacts 128-137.
Usage: python -I extract.py <r14_merge_v1_7 dir> <out_csv>"""
import sys, os, re, csv

D, OUT = sys.argv[1], sys.argv[2]
# ordered: specific phrases first; spans already consumed are skipped
PATS = [
    ("V9_SRC_LONG", r"〔來源：2026-09-29[^〕]*〕"),
    ("V9_SHORT", r"〔[^〕]{0,20}2026-09-29[^〕]{0,20}待核〕"),
    ("V9_EN", r"as reported in the 2026-09-29 validation record, pending verification"),
    ("AUTHOR_CONFIRM", r"\[AUTHOR TO CONFIRM[^\]]*\]"),
    ("VERIFY", r"\[VERIFY[^\]]*\]|`\[VERIFY\]`"),
    ("EMP_PENDING", r"\[?EMPIRICAL RESULT PENDING\]?"),
    ("HUM_PENDING", r"\[?HUMAN RESULT PENDING\]?|HUMAN CONSTRUCT VALIDATION PENDING|HUMAN BLIND CODING PENDING|V1_HUMAN_BLIND_CODING_PENDING|ORG_MAPPING_HUMAN_VALIDATION = PENDING"),
    ("V9_DATE", r"2026-09-29|20260929"),
    ("UNVERIFIED", r"UNVERIFIED|unverified"),
    ("PENDING_VERIF", r"pending verification"),
    ("ZH_PENDING", r"待核對|待核|待確認|待驗證"),
    ("SRC_MISSING", r"source unavailable|artifact missing|not available in this package|not shipped|ABSENT|不在本稿工作環境中|不在環境中|原始檔案缺件|缺件|依作者回報|USER-REPORTED|使用者陳述|作者 2026-10-13 的陳述"),
    ("TODO", r"\bTODO\b|\bTBD\b"),
    ("PENDING", r"(?i)pending"),
]
rx = [(n, re.compile(p)) for n, p in PATS]
files = sorted(f for f in os.listdir(D) if re.match(r"1(2[89]|3[0-7])_.*\.(md|csv)$", f))
rows = []
for f in files:
    head = "(none; CSV row)" if f.endswith(".csv") else "(none)"
    for i, line in enumerate(open(os.path.join(D, f), encoding="utf-8-sig", errors="replace"), 1):
        line = line.rstrip("\n")
        if f.endswith(".md") and re.match(r"^#{1,6}\s", line):
            head = line.strip()
        if f.endswith(".csv") and i > 1:
            head = "CSV row " + line.split(",", 1)[0]
        used = []
        seen = set()
        for n, r in rx:
            for m in r.finditer(line):
                if any(m.start() < e and m.end() > s for s, e in used):
                    continue
                used.append((m.start(), m.end()))
                phrase = m.group(0)
                if n in ("V9_DATE", "ZH_PENDING", "SRC_MISSING", "PENDING", "UNVERIFIED", "PENDING_VERIF", "TODO"):
                    s0 = max(0, m.start() - 45); e0 = min(len(line), m.end() + 30)
                    phrase = line[s0:e0]
                k = (n, m.group(0)) if n in ("EMP_PENDING", "HUM_PENDING") else (n, phrase)
                if k in seen:
                    continue
                seen.add(k)
                rows.append({"file": f, "line": i, "section": head[:150], "type": n, "flag": phrase.strip()})
with open(OUT, "w", encoding="utf-8", newline="") as o:
    w = csv.DictWriter(o, fieldnames=["file", "line", "section", "type", "flag"])
    w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), Counter(r["type"] for r in rows))
