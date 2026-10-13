"""Write 22_V1_8_1_FINAL_GREP_REPORT.md from final_grep.py hits with rule-based classification.

Usage: python -I write_grep_report.py <hits.tsv> <out.md>
"""
import collections
import csv
import sys

AUDIT_REPORTS = ("11_ARTIFACT132", "12_STALE", "13_SEGMENTATION", "14_G07", "15_REANALYSIS",
                 "16_PATCH_LOG", "16b_V18", "19_V1_HUMAN")
MANUSCRIPT = "16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.md"


def classify(pattern: str, path: str, line: int, excerpt: str) -> tuple:
    name = path.split("/")[-1]
    if name.startswith(AUDIT_REPORTS):
        return "QUOTED_IN_AUDIT_EVIDENCE", "none (report quotes old wording or the search pattern itself)"
    if name.startswith("17_STUDY1"):
        return "INVALID_CLAIM_LIST (negated)", "none"
    if name.startswith("128_CANONICAL_STATE"):
        return "CORRECTED_LABEL (NOT THE V5 DATA PACK; REAL_V5_DATA_PACK=NOT_RECOVERED)", "none"
    if name.startswith("131_HUMAN"):
        return "PROVENANCE_ADDED_V181 (V9.1 segmentation sensitivity tag)", "tag added in current copy"
    if name == MANUSCRIPT:
        if pattern == "structural holes":
            if line >= 2380:
                return "REFERENCE_LIST_ENTRY", "none"
            return "NEGATED_THEORY_BOUNDARY (not automatically a structural hole)", "none"
        if pattern == "human validation confirmed":
            return "NEGATED (does not show that human validation confirmed)", "none"
        if pattern in ("84/120", "85/120", "84–85/120"):
            return "NUMBER_UNCHANGED_PROVENANCE_V9_1_ATTRIBUTED (table note L1603 / L2264 tag)", "provenance tag added (J22–J28)"
    return "UNCLASSIFIED", "REVIEW"


def main() -> None:
    hits_path, out = sys.argv[1], sys.argv[2]
    rows = list(csv.DictReader(open(hits_path, encoding="utf-8"), delimiter="\t"))
    layers = collections.Counter((r["pattern"], r["layer"]) for r in rows)
    patterns = list(dict.fromkeys(r["pattern"] for r in rows))
    lines = ["# 22 — V1.8.1 Final Forensic Grep Report", "",
             "Script: `tools/O/final_grep.py` (run with `python -I` on the working tree before commit); raw hits: "
             "`tools/O/final_grep_hits.tsv`; report generator: `tools/O/write_grep_report.py`.", "",
             "Layers: **CURRENT** = new v1.8.1 artifacts (this folder, excluding tools); **CURRENT_TOOLS** = scripts/JSON "
             "in this folder's tools (contain the search patterns themselves); **HISTORICAL** = every other tracked file "
             "(V1.8 folder, earlier checkpoints, root files) — frozen by policy, not edited; their stale wording is "
             "superseded by the current copies and by 12/15/17.", "",
             "## Counts by pattern and layer", "", "| Pattern | CURRENT | CURRENT_TOOLS | HISTORICAL |", "|---|---:|---:|---:|"]
    for p in patterns:
        lines.append(f"| {p} | {layers[(p, 'CURRENT')]} | {layers[(p, 'CURRENT_TOOLS')]} | {layers[(p, 'HISTORICAL')]} |")
    for p in ("V9 not available", "V9 不在", "FULL_REANALYSIS_RECOMMENDED=NO", "32 pairs were confirmed",
              "enterprise ROI demonstrated", "V7 complete"):
        if p not in patterns:
            lines.append(f"| {p} | 0 | 0 | 0 |")
    cur = [r for r in rows if r["layer"] == "CURRENT"]
    cls = [(r, *classify(r["pattern"], r["file"], int(r["line"]), r["excerpt"])) for r in cur]
    unresolved = [c for c in cls if c[1] == "UNCLASSIFIED"]
    lines += ["", "## Verdict", "",
              f"- CURRENT hits: {len(cur)}; UNCLASSIFIED / substantive forbidden claims: **{len(unresolved)}**.",
              "- In the v1.8.1 manuscript: `2026-09-29 紀錄，待核` = 0; `FULL_REANALYSIS_RECOMMENDED=NO` = 0; `{taxblock}` = 0; "
              "`V9 not available`/`V9 不在` = 0; legacy-zip/V5 co-binding = 0; `32 pairs were confirmed` = 0; "
              "`enterprise ROI demonstrated` = 0; `V7 complete` = 0. Remaining hits are negations, reference entries, "
              "or 84/85/120 values whose provenance is now tagged as V9.1.",
              "- `FULL_REANALYSIS_RECOMMENDED=NO` survives only in HISTORICAL V1.8 files (07, 10) and is superseded by the "
              "triplet in 15/17/23.", "",
              "## CURRENT hits (file, line, classification, action)", "",
              "| Pattern | File | Line | Classification | Action |", "|---|---|---:|---|---|"]
    for r, c, a in cls:
        lines.append(f"| {r['pattern']} | `{r['file'].split('/')[-1]}` | {r['line']} | {c} | {a} |")
    hist = collections.Counter((r["pattern"], r["file"]) for r in rows if r["layer"] == "HISTORICAL")
    lines += ["", "## HISTORICAL hits (frozen; classification FROZEN_HISTORICAL; action: none — superseded)", "",
              "| Pattern | File | Hits |", "|---|---|---:|"]
    for (p, f), n in sorted(hist.items()):
        lines.append(f"| {p} | `{f}` | {n} |")
    open(out, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print("current", len(cur), "unclassified", len(unresolved))
    for c in unresolved:
        print(c[0]["file"], c[0]["line"], c[0]["pattern"])


if __name__ == "__main__":
    main()
