"""Extra checks: timestamps ordering, unanimous row, blank-queue hash reconstruction, confidence match, Wilson CI.
Usage: python -I extra_checks.py <package_dir>"""
import csv, hashlib, io, json, math, sys
from pathlib import Path
pkg = Path(sys.argv[1])
def r(n):
    with (pkg/n).open(encoding="utf-8-sig", newline="") as f: return list(csv.DictReader(f))
first = {x["record_id"]: x for x in r("FIRST_CODER_50_FINAL_FROZEN.csv")}
sec = r("BLIND_REPEAT_20_FINAL_FROZEN.csv")
rec = {x["record_id"]: x for x in r("HUMAN_RECONCILED_20.csv")}
ft = sorted(x["coder_timestamp"] for x in first.values())
st = sorted(x["coder_timestamp"] for x in sec)
print("first coder_timestamp range", ft[0], ft[-1])
print("second coder_timestamp range", st[0], st[-1])
ev = [json.loads(l) for l in (pkg/"HUMAN_RECONCILIATION_EVENTS.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
et = sorted(e["timestamp_utc"] for e in ev)
print("reconciliation events range", et[0], et[-1])
u = rec["REC-0D720884574345B4"]
print("unanimous row:", {k: u[k] for k in u if k.startswith(("FIRST_C","BLIND_C","FINAL_C","RESOLUTION"))})
print("conf match", sum(first[x["record_id"]]["coder_confidence"] == x["coder_confidence"] for x in sec))
# blank queue reconstruction
raw = (pkg/"BLIND_REPEAT_20_FINAL_FROZEN.csv").read_bytes()
bom = raw.startswith(b"\xef\xbb\xbf")
txt = raw.decode("utf-8-sig")
nl = "\r\n" if "\r\n" in txt else "\n"
rows = list(csv.DictReader(io.StringIO(txt)))
fields = list(rows[0].keys())
target = "0100E52409608F26DE0DB772AC08D8FD03CCD81DC307A56EF79A0D9C3792101B"
order_variants = {"file_order": rows}
hit = None
for status in ("NOT_STARTED", ""):
    for oname, rr in order_variants.items():
        for b in (True, False):
            for le in ("\r\n", "\n"):
                out = io.StringIO()
                w = csv.DictWriter(out, fieldnames=fields, lineterminator=le)
                w.writeheader()
                for x in rr:
                    y = dict(x)
                    for k in fields:
                        if k not in ("record_id", "evidence_text"): y[k] = ""
                    y["review_status"] = status
                    w.writerow(y)
                data = (b"\xef\xbb\xbf" if b else b"") + out.getvalue().encode("utf-8")
                if hashlib.sha256(data).hexdigest().upper() == target: hit = (status, oname, b, repr(le))
print("blank-queue hash reconstruction hit:", hit)
def wilson(k, n, z=1.959963984540054):
    p = k/n; d = 1+z*z/n; c = (p + z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return round(100*(c-h),2), round(100*(c+h),2)
for k in (15,7,4,4,12): print("wilson", k, wilson(k,20))
