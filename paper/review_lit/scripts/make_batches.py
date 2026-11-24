"""Split the screening set into primary-screener batches and a blind 25% second-screener sample (seed 20261119)."""
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
recs = [json.loads(l) for l in open(HERE / "screening_set_LOCAL.jsonl", encoding="utf-8")]
screen = [r for r in recs if r["abstract"].strip()]
noabs = [r["rid"] for r in recs if not r["abstract"].strip()]
(HERE / "batches_LOCAL").mkdir(exist_ok=True)


def dump(name, rows):
    with open(HERE / "batches_LOCAL" / name, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps({k: r[k] for k in ("rid", "title", "year", "venue", "abstract")}, ensure_ascii=False) + "\n")


n = 4
for k in range(n):
    dump(f"primary_{k + 1}.jsonl", screen[k::n])
second = random.Random(20261119).sample(sorted(screen, key=lambda r: r["rid"]), round(0.25 * len(screen)))
dump("second.jsonl", sorted(second, key=lambda r: r["rid"]))
json.dump({"screenable": len(screen), "no_abstract_excluded": noabs, "second_sample": [r["rid"] for r in second]},
          open(HERE / "batches_LOCAL" / "manifest.json", "w"), indent=1)
print("screenable", len(screen), "no abstract", len(noabs), "second", len(second), [len(screen[k::n]) for k in range(n)])
