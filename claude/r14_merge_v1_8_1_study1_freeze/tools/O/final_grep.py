"""V1.8.1 final forensic search over tracked + new text files in the repo.

Usage: python -I final_grep.py <repo_root> <out_tsv>
Writes one row per hit: pattern, file, line, layer (CURRENT / HISTORICAL), excerpt.
Layer: files under claude/r14_merge_v1_8_1_study1_freeze/ (excluding tools/) are CURRENT; everything
else (V1.8 folder, earlier checkpoints, root files) is HISTORICAL and frozen.
"""
import csv
import os
import re
import sys

PATTERNS = [
    ("V9 not available", r"V9 not available"),
    ("V9 不在", r"V9\s*不在"),
    ("2026-09-29 紀錄，待核", r"2026-09-29 紀錄，待核"),
    ("完整資料來源.zip + V5 Data Pack (same line)", r"完整資料來源.*V5.*Data Pack|V5.*Data Pack.*完整資料來源"),
    ("FULL_REANALYSIS_RECOMMENDED=NO", r"FULL_REANALYSIS_RECOMMENDED\s*=\s*NO"),
    ("84–85/120", r"84\s*[–-]\s*85\s*[/／]\s*120"),
    ("84/120", r"(?<![\d–-])84\s*[/／]\s*120"),
    ("85/120", r"(?<![\d–-])85\s*[/／]\s*120"),
    ("{taxblock}", r"\{taxblock\}"),
    ("human validation confirmed", r"human validation confirmed"),
    ("32 pairs were confirmed", r"32 pairs were confirmed"),
    ("structural holes", r"structural holes?"),
    ("enterprise ROI demonstrated", r"enterprise ROI demonstrated"),
    ("V7 complete", r"V7 complete"),
]
TEXT_EXT = {".md", ".csv", ".txt", ".json", ".py", ".tsv"}
CURRENT_PREFIX = "claude/r14_merge_v1_8_1_study1_freeze/"


def main() -> None:
    root, out = sys.argv[1], sys.argv[2]
    rows = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d != ".git"]
        for f in fn:
            if os.path.splitext(f)[1].lower() not in TEXT_EXT:
                continue
            path = os.path.join(dp, f)
            rel = os.path.relpath(path, root).replace("\\", "/")
            layer = "CURRENT" if rel.startswith(CURRENT_PREFIX) and "/tools/" not in rel else (
                "CURRENT_TOOLS" if rel.startswith(CURRENT_PREFIX) else "HISTORICAL")
            try:
                lines = open(path, encoding="utf-8").read().splitlines()
            except UnicodeDecodeError:
                continue
            for name, rx in PATTERNS:
                for i, line in enumerate(lines, 1):
                    m = re.search(rx, line, flags=re.I)
                    if m:
                        k = m.start()
                        rows.append([name, rel, i, layer, line[max(0, k - 90):k + 110].replace("\t", " ")])
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["pattern", "file", "line", "layer", "excerpt"])
        w.writerows(rows)
    from collections import Counter
    for (p, l), n in sorted(Counter((r[0], r[3]) for r in rows).items()):
        print(f"{p}\t{l}\t{n}")


if __name__ == "__main__":
    main()
