"""List every v1.7 line that states V9 human-validation status. Usage: python -I v9claims.py <130.md> <out.txt>"""
import sys, re

KW = {"50/20/19": r"50/50|20/20|19/19|50／20／19|50 筆|20 筆|19 筆|n = 20|\b400\b 筆|120 筆",
      "kappa/agreement": r"κ = \.|\.561|\.048|\.180|\.140|\.316|75%、35%",
      "reconciliation": r"調和|reconcil",
      "label-substitution sensitivity": r"人工標籤替換|label substitution|L2′|15／17|31 組|表 4-9A|HUMAN_AUDIT_CONVERGED|LOCAL_SENSITIVITY|FULL_REANALYSIS",
      "V9 provenance": r"2026-09-29|20260929|V9"}
L = open(sys.argv[1], encoding="utf-8").read().split("\n")
head = ""
with open(sys.argv[2], "w", encoding="utf-8") as o:
    for i, line in enumerate(L, 1):
        if re.match(r"^#{1,6}\s", line):
            head = line.strip()[:60]
        hits = [k for k, p in KW.items() if re.search(p, line)]
        if hits:
            o.write(f"L{i} [{head}] {';'.join(hits)} :: {line[:200]}\n")
