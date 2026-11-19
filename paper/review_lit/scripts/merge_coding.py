"""Merge two blind coders, compute kappa per variable, build adjudication batch; after adjudication, compute results.

Usage:
    python merge_coding.py agree      # kappa + adjudication batch
    python merge_coding.py results    # final codes (A=B, else adjudicated) + prevalence tables
"""
import csv
import json
import math
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
C = HERE / "coding_LOCAL"
VARS = ["D1", "D2", "D3", "F1", "F2", "F3", "F4", "V", "E"]
FLAGS = ["F1", "F2", "F3", "F4", "V"]


def read(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        return {r["rid"].strip(): {k.strip(): (v or "").strip().lower() for k, v in r.items()} for r in csv.DictReader(f)}


def kappa(a, b):
    n = len(a)
    labs = sorted(set(a) | set(b))
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(l) / n) * (b.count(l) / n) for l in labs)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def wilson(k, n, z=1.96):
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [max(0.0, round((c - h) / d, 3)), min(1.0, round((c + h) / d, 3))]


def load_pair():
    A, B = {}, {}
    for k in (1, 2):
        A.update(read(C / f"A{k}.csv"))
        B.update(read(C / f"B{k}.csv"))
    return A, B


def agree():
    A, B = load_pair()
    both = sorted(set(A) & set(B))
    out = {"coded_A": len(A), "coded_B": len(B), "both": len(both), "kappa": {}, "raw_agreement": {}}
    dis = {}
    for v in VARS:
        a = [A[r].get(v, "") for r in both]
        b = [B[r].get(v, "") for r in both]
        out["kappa"][v] = round(kappa(a, b), 3)
        out["raw_agreement"][v] = round(sum(x == y for x, y in zip(a, b)) / len(both), 3)
        for r in both:
            if A[r].get(v, "") != B[r].get(v, "") and v in FLAGS + ["D2"]:
                dis.setdefault(r, []).append(v)
    out["records_with_flag_or_claim_disagreement"] = len(dis)
    json.dump(out, open(HERE / "coding_agreement.json", "w"), indent=1)
    recs = {json.loads(l)["rid"]: json.loads(l) for l in open(HERE / "screening_set_LOCAL.jsonl", encoding="utf-8")}
    items = []
    for r, vs in sorted(dis.items()):
        d = {k: recs[r][k] for k in ("rid", "title", "year", "venue", "abstract")}
        d["disputed"] = {v: {"A": A[r].get(v), "B": B[r].get(v)} for v in vs}
        d["A_note"], d["B_note"] = A[r].get("note", ""), B[r].get("note", "")
        items.append(d)
    with open(HERE / "batches_LOCAL" / "code_adjudicate.jsonl", "w", encoding="utf-8") as f:
        for d in items:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=1))


def results():
    A, B = load_pair()
    adj = read(C / "adjudicated.csv") if (C / "adjudicated.csv").exists() else {}
    meta = {r["rid"]: r for r in csv.DictReader(open(HERE / "screening_set_meta.csv", encoding="utf-8"))}
    final = {}
    for r in sorted(set(A) & set(B)):
        row = {}
        for v in VARS:
            if A[r].get(v) == B[r].get(v):
                row[v] = A[r].get(v)
            elif r in adj and adj[r].get(v):
                row[v] = adj[r][v]
            else:
                row[v] = A[r].get(v) if v in ("D1", "D3", "E") else "unclear"
        final[r] = row
    year = lambda r: int(meta[r]["year"]) if meta[r]["year"] else 0
    period = lambda y: "2000-2014" if y <= 2014 else ("2015-2019" if y <= 2019 else "2020-2026")

    def prevalence(rs):
        n = len(rs)
        res = {"n": n}
        for v in FLAGS:
            c = Counter(final[r][v] for r in rs)
            res[v] = {"yes": c["yes"], "no": c["no"], "unclear": c["unclear"],
                      "share_yes": round(c["yes"] / n, 3) if n else None, "wilson95": wilson(c["yes"], n)}
        return res
    allr = sorted(final)
    out = {"overall": prevalence(allr),
           "by_stream": {s: prevalence([r for r in allr if meta[r]["stream"] == s]) for s in ("S", "G1", "G2", "G3")},
           "by_relation": {k: prevalence([r for r in allr if final[r]["D1"] == k]) for k in sorted({final[r]["D1"] for r in allr})},
           "by_claim": {k: prevalence([r for r in allr if final[r]["D2"] == k]) for k in sorted({final[r]["D2"] for r in allr})},
           "by_period": {p: prevalence([r for r in allr if period(year(r)) == p]) for p in ("2000-2014", "2015-2019", "2020-2026")},
           "D3_measure": dict(Counter(final[r]["D3"] for r in allr)),
           "E_evidence": dict(Counter(final[r]["E"] for r in allr)),
           "hole_or_broker_claims": sum(final[r]["D2"] in ("hole", "broker", "several") for r in allr),
           "adjudicated_records": len(adj)}
    json.dump(out, open(HERE / "review_results.json", "w"), indent=1)
    with open(HERE / "included_studies_coded.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rid", "stream", "openalex_id", "doi", "year", "venue", "title"] + VARS)
        for r in allr:
            m = meta[r]
            w.writerow([r, m["stream"], m["openalex_id"], m["doi"], m["year"], m["venue"], m["title"]] + [final[r][v] for v in VARS])
    print(json.dumps(out["overall"], indent=1))
    print("hole/broker claims", out["hole_or_broker_claims"], "D3", out["D3_measure"])


if __name__ == "__main__":
    {"agree": agree, "results": results}[sys.argv[1]]()
