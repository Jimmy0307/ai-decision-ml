"""Merge screening decisions, compute agreement on the double-screened sample, list disagreements."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = HERE / "screening_LOCAL"


def read(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        return {r["rid"].strip(): {k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)}


def kappa(a, b):
    labs = sorted(set(a) | set(b))
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(l) / n) * (b.count(l) / n) for l in labs)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def main():
    man = json.load(open(HERE / "batches_LOCAL" / "manifest.json"))
    prim = {}
    for k in range(1, 5):
        prim.update(read(S / f"primary_{k}.csv"))
    sec = read(S / "second.csv")
    expected = {json.loads(l)["rid"] for k in range(1, 5) for l in open(HERE / "batches_LOCAL" / f"primary_{k}.jsonl", encoding="utf-8")}
    missing = sorted(expected - set(prim))
    both = sorted(set(sec) & set(prim))
    a = [prim[r]["decision"].upper() for r in both]
    b = [sec[r]["decision"].upper() for r in both]
    dis = [r for r in both if prim[r]["decision"].upper() != sec[r]["decision"].upper()]
    out = {"screenable": man["screenable"], "primary_coded": len(prim), "missing_primary": missing,
           "second_coded": len(sec), "overlap": len(both),
           "kappa_include_exclude": round(kappa(a, b), 3), "raw_agreement": round(sum(x == y for x, y in zip(a, b)) / len(a), 3),
           "disagreements": dis,
           "primary_includes": sum(v["decision"].upper() == "INCLUDE" for v in prim.values())}
    json.dump(out, open(HERE / "screening_agreement.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "disagreements"}, indent=1), "\ndisagreements", len(dis))


if __name__ == "__main__":
    main()
