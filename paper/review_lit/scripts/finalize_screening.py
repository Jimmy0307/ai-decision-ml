"""Final screening decisions (adjudicated where re-screened, else primary) and coding batches for two blind coders."""
import csv
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = HERE / "screening_LOCAL"


def read(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        return {r["rid"].strip(): {k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)}


recs = {json.loads(l)["rid"]: json.loads(l) for l in open(HERE / "screening_set_LOCAL.jsonl", encoding="utf-8")}
meta = {r["rid"]: r for r in csv.DictReader(open(HERE / "screening_set_meta.csv", encoding="utf-8"))}
prim = {}
for k in range(1, 5):
    prim.update(read(S / f"primary_{k}.csv"))
adj = {}
for k in (1, 2):
    adj.update(read(S / f"adjudicated_{k}.csv"))
todo = {json.loads(l)["rid"] for k in (1, 2) for l in open(HERE / "batches_LOCAL" / f"adjudicate_{k}.jsonl", encoding="utf-8")}
missing = sorted(todo - set(adj))
final = {}
for r, p in prim.items():
    if r in adj:
        final[r] = {"decision": adj[r]["final_decision"].upper(), "source": "adjudicated",
                    "relation_type": adj[r]["relation_type"], "claim_type": adj[r]["claim_type"]}
    else:
        final[r] = {"decision": p["decision"].upper(), "source": "primary_high_conf",
                    "relation_type": p["relation_type"], "claim_type": p["claim_type"]}
inc = sorted(r for r, v in final.items() if v["decision"] == "INCLUDE")
reversed_ = sum(1 for r in adj if adj[r]["final_decision"].upper() != prim[r]["decision"].upper())
flow = {"screening_set": len(recs), "excluded_no_abstract": len(recs) - len(prim), "screened": len(prim),
        "re_screened_by_adjudicator": len(adj), "adjudicator_reversals": reversed_, "missing_adjudication": missing,
        "included": len(inc), "excluded": len(prim) - len(inc),
        "included_by_stream": dict(Counter(meta[r]["stream"] for r in inc)),
        "screened_by_stream": dict(Counter(meta[r]["stream"] for r in prim)),
        "included_claim_type": dict(Counter(final[r]["claim_type"] for r in inc)),
        "included_relation_type": dict(Counter(final[r]["relation_type"] for r in inc))}
json.dump(flow, open(HERE / "screening_flow.json", "w"), indent=1)
with open(HERE / "screening_final.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["rid", "stream", "decision", "source", "relation_type", "claim_type"])
    for r in sorted(final):
        w.writerow([r, meta[r]["stream"], final[r]["decision"], final[r]["source"], final[r]["relation_type"], final[r]["claim_type"]])
(HERE / "coding_LOCAL").mkdir(exist_ok=True)
rows = [{k: recs[r][k] for k in ("rid", "title", "year", "venue", "abstract")} for r in inc]
half = (len(rows) + 1) // 2
for coder in ("A", "B"):
    for k, chunk in enumerate((rows[:half], rows[half:]), 1):
        with open(HERE / "batches_LOCAL" / f"code_{coder}{k}.jsonl", "w", encoding="utf-8") as f:
            for d in chunk:
                f.write(json.dumps(d, ensure_ascii=False) + "\n")
print(json.dumps(flow, indent=1))
