"""Check whether 130 .docx / 132 .xlsx carry the same flags as the .md / .csv.
Usage: python -I dupcheck.py <r14_merge_v1_7 dir>"""
import sys, os, re, zipfile, csv, json

D = sys.argv[1]
FL = ["2026-09-29 紀錄，待核", "原始檔案未在本稿工作環境中", "AUTHOR TO CONFIRM", "EMPIRICAL RESULT PENDING",
      "HUMAN RESULT PENDING", "判準待核", "依作者回報", "VERIFY", "不在本稿工作環境中", "待核"]


def text_of(zpath, members):
    z = zipfile.ZipFile(zpath)
    out = []
    for m in z.namelist():
        if any(re.fullmatch(p, m) for p in members):
            x = z.read(m).decode("utf-8", "replace")
            out.append(re.sub(r"<[^>]+>", "", x))
    return "".join(out)


md = open(os.path.join(D, "130_MERGED_MASTER_THESIS_R14_TO_ENTERPRISE_v1_7_EVIDENCE_CONVERGED_CANDIDATE.md"), encoding="utf-8").read()
dx = text_of(os.path.join(D, "130_MERGED_MASTER_THESIS_R14_TO_ENTERPRISE_v1_7_EVIDENCE_CONVERGED_CANDIDATE.docx"),
             [r"word/document\.xml", r"word/footnotes\.xml"])
csvt = open(os.path.join(D, "132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX.csv"), encoding="utf-8-sig").read()
xl = text_of(os.path.join(D, "132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX.xlsx"),
             [r"xl/sharedStrings\.xml", r"xl/worksheets/sheet\d+\.xml"])
res = {"130": {f: [md.count(f), dx.count(f)] for f in FL}, "132": {f: [csvt.count(f), xl.count(f)] for f in FL}}
print(json.dumps(res, ensure_ascii=False, indent=1))
