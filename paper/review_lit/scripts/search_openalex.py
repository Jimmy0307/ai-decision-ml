"""Systematic review search (PROTOCOL.md v1.0): OpenAlex title/abstract queries, dedup, seeded sampling.

Writes (local only, contains abstracts): records_all_LOCAL.jsonl, screening_set_LOCAL.jsonl
Writes (public-safe): search_log.json (queries, date, counts), screening_set_meta.csv (ids/titles/years/venues/doi/stream)
"""
import csv
import json
import random
import re
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = {"User-Agent": "research-review-script/1.0"}
TERMS_S = ['"co-word"', '"keyword"', '"co-citation"', '"co-occurrence"', 'bibliometric', 'patent']
STREAMS = [("S", [f'"structural hole" {t}' for t in TERMS_S], None),
           ("G1", ['"research gap" "co-word"'], None),
           ("G2", ['"research gap" "keyword co-occurrence"'], 120),
           ("G3", ['betweenness "co-word"'], 80)]
SEED = 20261119


def abstract(inv):
    if not inv:
        return ""
    pos = {}
    for w, idx in inv.items():
        for i in idx:
            pos[i] = w
    return " ".join(pos[i] for i in sorted(pos))


def fetch(q):
    cache = HERE / "cache_LOCAL" / (re.sub(r"[^A-Za-z0-9]+", "_", q).strip("_") + ".json")
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    out = _fetch(q)
    cache.parent.mkdir(exist_ok=True)
    cache.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    return out


def _fetch(q):
    out, cursor = [], "*"
    page = 1
    while cursor:
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode({
            "filter": f"title_and_abstract.search:{q},from_publication_date:2000-01-01",
            "per-page": 200, "page": page,   # page-based paging (anonymous cursor paging is rate-limited)
            "select": "id,doi,title,publication_year,type,language,primary_location,abstract_inverted_index,authorships"})
        for k in range(6):
            try:
                d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
                break
            except Exception as e:
                err = e
                print("retry", k, q[:40], e, flush=True)
                time.sleep(20 * (k + 1))
        else:
            raise SystemExit(f"failed {q}: {err}")
        for w in d["results"]:
            src = ((w.get("primary_location") or {}).get("source") or {})
            out.append({"id": w["id"].split("/")[-1], "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
                        "title": w.get("title") or "", "year": w.get("publication_year"), "type": w.get("type"),
                        "language": w.get("language"), "venue": src.get("display_name") or "",
                        "n_authors": len(w.get("authorships") or []),
                        "abstract": abstract(w.get("abstract_inverted_index"))})
        page += 1
        cursor = len(d["results"]) == 200 and len(out) < d["meta"]["count"]
        time.sleep(1.0)
    return out


def main():
    log = {"protocol": "PROTOCOL.md v1.0", "retrieved": str(date.today()), "queries": [], "streams": {}}
    seen_id, seen_doi, final = set(), set(), []
    allrec = []
    for stream, qs, sample in STREAMS:
        pool = []
        for q in qs:
            recs = fetch(q)
            log["queries"].append({"stream": stream, "query": q, "hits": len(recs)})
            for r in recs:
                r["stream"] = stream
            pool += recs
            allrec += recs
        uniq, ids = [], set()
        for r in pool:
            if r["id"] in ids:
                continue
            ids.add(r["id"])
            uniq.append(r)
        fresh = [r for r in uniq if r["id"] not in seen_id and (not r["doi"] or r["doi"].lower() not in seen_doi)]
        if sample:
            fresh_sorted = sorted(fresh, key=lambda r: r["id"])
            chosen = random.Random(SEED).sample(fresh_sorted, min(sample, len(fresh_sorted)))
        else:
            chosen = fresh
        for r in chosen:
            seen_id.add(r["id"])
            if r["doi"]:
                seen_doi.add(r["doi"].lower())
        final += chosen
        log["streams"][stream] = {"retrieved_unique": len(uniq), "after_cross_stream_dedup": len(fresh),
                                  "screening_set": len(chosen), "sampled": bool(sample)}
        print(stream, log["streams"][stream])
    with open(HERE / "records_all_LOCAL.jsonl", "w", encoding="utf-8") as f:
        for r in allrec:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(HERE / "screening_set_LOCAL.jsonl", "w", encoding="utf-8") as f:
        for k, r in enumerate(final):
            r["rid"] = f"R{k + 1:04d}"
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(HERE / "screening_set_meta.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rid", "stream", "openalex_id", "doi", "year", "type", "language", "venue", "title", "has_abstract"])
        for r in final:
            w.writerow([r["rid"], r["stream"], r["id"], r["doi"], r["year"], r["type"], r["language"], r["venue"], r["title"], bool(r["abstract"])])
    log["screening_set_total"] = len(final)
    log["no_abstract"] = sum(1 for r in final if not r["abstract"])
    (HERE / "search_log.json").write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")
    print("total", len(final), "no abstract", log["no_abstract"])


if __name__ == "__main__":
    main()
