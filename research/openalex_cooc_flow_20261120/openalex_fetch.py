"""Plan 10 retrieval (PREREGISTRATION_OPENALEX.md): OpenAlex subfield co-occurrence (full population, group_by)
and a random sample of citing works with their references' years and subfields, aggregated for the Plan 7 formula.

Anonymous requests only (no API key, no e-mail), <= 3 requests/s, <= 60,000 requests/day, exponential back-off,
stop after 20 consecutive failures. Every response is cached, so the script resumes.

Usage:
    python openalex_fetch.py --work <local dir> [--target 100000]
Writes into <work>: cache_LOCAL/ (raw responses), subfields.json, cooccurrence.npz, flow_aggregates.npz,
sample_ids.txt.gz, fetch_log.json.
"""
import argparse
import gzip
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

import numpy as np

API = "https://api.openalex.org"
BASE_FILTER = "type:article,publication_year:2015-2024,topics.domain.id:1|2|3|4"
UA = "openalex-research-script/1.0"
MIN_GAP, DAY_CAP, MAX_FAIL = 0.34, 60_000, 20


class Client:
    def __init__(self, cache: Path, state: Path):
        self.cache, self.state_path = cache, state
        cache.mkdir(parents=True, exist_ok=True)
        self.state = json.loads(state.read_text()) if state.exists() else {"days": {}, "fail_streak": 0}
        self.last = 0.0

    def get(self, path, params):
        q = urllib.parse.urlencode(params, safe=":|,*>!")
        url = f"{API}/{path}?{q}"
        key = hashlib.sha1(url.encode()).hexdigest()
        f = self.cache / key[:2] / f"{key}.json.gz"
        if f.exists():
            return json.loads(gzip.decompress(f.read_bytes()))
        day = time.strftime("%Y-%m-%d")
        if self.state["days"].get(day, 0) >= DAY_CAP:
            raise SystemExit(f"daily request cap {DAY_CAP} reached; resume tomorrow")
        delay = 1.0
        while True:
            wait = MIN_GAP - (time.time() - self.last)
            if wait > 0:
                time.sleep(wait)
            self.last = time.time()
            self.state["days"][day] = self.state["days"].get(day, 0) + 1
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=60) as r:
                    data = json.loads(r.read())
                self.state["fail_streak"] = 0
                f.parent.mkdir(exist_ok=True)
                f.write_bytes(gzip.compress(json.dumps(data).encode()))
                if self.state["days"][day] % 200 == 0:
                    self.save()
                return data
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
                code = getattr(e, "code", None)
                self.state["fail_streak"] += 1
                self.save()
                if self.state["fail_streak"] > MAX_FAIL:
                    raise SystemExit(f"stopping: {self.state['fail_streak']} consecutive failures (last {code or e}); "
                                     "server refusing requests - report and do not retry blindly")
                if code is not None and code < 500 and code != 429:
                    raise SystemExit(f"HTTP {code} for {url}")
                time.sleep(min(delay, 120))
                delay *= 2

    def save(self):
        self.state_path.write_text(json.dumps(self.state))


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def subfields(c):
    rows = []
    for page in (1, 2):
        d = c.get("subfields", {"per_page": 200, "page": page})
        rows += d["results"]
    out = [{"id": r["id"].rsplit("/", 1)[-1], "name": r["display_name"],
            "field": r["field"]["id"].rsplit("/", 1)[-1], "field_name": r["field"]["display_name"],
            "domain": r["domain"]["id"].rsplit("/", 1)[-1], "domain_name": r["domain"]["display_name"]} for r in rows]
    return sorted(out, key=lambda x: int(x["id"]))


def grouped(c, flt):
    """All groups of topics.subfield.id for a filter (group_by paging with cursor)."""
    res, cursor = {}, "*"
    while cursor:
        d = c.get("works", {"filter": flt, "group_by": "topics.subfield.id", "per_page": 200, "cursor": cursor})
        for g in d["group_by"]:
            k = str(g["key"]).rsplit("/", 1)[-1]
            if k.isdigit():
                res[k] = g["count"]
        cursor = d.get("meta", {}).get("next_cursor")
        if not d["group_by"]:
            break
    return res


def cooccurrence(c, sf):
    ids = [s["id"] for s in sf]
    ix = {k: i for i, k in enumerate(ids)}
    G = len(ids)
    N = c.get("works", {"filter": BASE_FILTER, "per_page": 1})["meta"]["count"]
    C = -np.ones((G, G), np.int64)                 # -1 = unknown
    for i, s in enumerate(ids):                     # amendment R10-A1: first group_by page only (no cursor)
        d = c.get("works", {"filter": f"{BASE_FILTER},topics.subfield.id:{s}", "group_by": "topics.subfield.id",
                            "per_page": 200})
        for g in d["group_by"]:
            k = str(g["key"]).rsplit("/", 1)[-1]
            if k in ix:
                C[i, ix[k]] = g["count"]
        if i % 25 == 0:
            log("co-occurrence rows", i + 1, "of", G)
    C = np.where(C >= 0, C, C.T)                    # known from the other row
    pairs = 0
    for i in range(G):
        for j in range(i + 1, G):
            if C[i, j] < 0:
                d = c.get("works", {"filter": f"{BASE_FILTER},topics.subfield.id:{ids[i]}+{ids[j]}", "per_page": 1,
                                    "select": "id"})
                C[i, j] = C[j, i] = d["meta"]["count"]
                pairs += 1
                if pairs % 1000 == 0:
                    log("pairwise co-occurrence queries", pairs)
    assert (C >= 0).all()
    log("pairwise co-occurrence queries total", pairs)
    return C, N


def sample_works(c, target):
    works, seed = {}, 1
    flt = f"{BASE_FILTER},referenced_works_count:>0"
    while len(works) < target:
        for page in range(1, 51):
            d = c.get("works", {"filter": flt, "sample": 10000, "seed": seed, "per_page": 200, "page": page,
                                "select": "id,publication_year,topics,referenced_works"})
            for w in d["results"]:
                wid = w["id"].rsplit("/", 1)[-1]
                sfs = sorted({t["subfield"]["id"].rsplit("/", 1)[-1] for t in (w.get("topics") or []) if t.get("subfield")})
                if sfs and w.get("referenced_works"):
                    works[wid] = (w["publication_year"], sfs, [r.rsplit("/", 1)[-1] for r in w["referenced_works"]])
            if not d["results"]:
                break
        log("sample seed", seed, "distinct citing works", len(works))
        seed += 1
    return works


def lookup(c, ids):
    info, ids = {}, sorted(ids)
    for b in range(0, len(ids), 100):
        chunk = ids[b:b + 100]
        d = c.get("works", {"filter": "openalex:" + "|".join(chunk), "per_page": 100,
                            "select": "id,publication_year,topics"})
        for w in d["results"]:
            wid = w["id"].rsplit("/", 1)[-1]
            sfs = sorted({t["subfield"]["id"].rsplit("/", 1)[-1] for t in (w.get("topics") or []) if t.get("subfield")})
            info[wid] = (w.get("publication_year"), sfs)
        if (b // 100) % 500 == 0:
            log("lookups", b + len(chunk), "of", len(ids))
    return info


def aggregate(works, info, sf, y0=1900):
    ids = [s["id"] for s in sf]
    ix = {k: i for i, k in enumerate(ids)}
    G = len(ids)
    ys = [w[0] for w in works.values()]
    cy0, cy1 = min(ys), max(ys)
    ny = cy1 - y0 + 1
    S = (cy1 - cy0 + 1) * ny
    M = np.zeros(S, np.int64)
    outF = np.zeros((S, G), np.int64)
    inF = np.zeros((S, G), np.int64)
    from array import array
    okeys, ikeys, O = array("q"), array("q"), np.zeros((G, G), np.int64)
    GG = G * G
    n_cit = 0
    for wid, (yi, si, refs) in works.items():
        a_set = [ix[x] for x in si if x in ix]
        for r in refs:
            if r not in info:
                continue
            yj, sj = info[r]
            b_set = [ix[x] for x in sj if x in ix]
            if not a_set or not b_set or yj is None or yj < y0 or yj > cy1:
                continue
            s = (yi - cy0) * ny + (yj - y0)
            M[s] += 1
            n_cit += 1
            for a in a_set:
                outF[s, a] += 1
                for a2 in a_set:
                    if a2 != a:
                        okeys.append(s * GG + a * G + a2)
            for b in b_set:
                inF[s, b] += 1
                for b2 in b_set:
                    if b2 != b:
                        ikeys.append(s * GG + b * G + b2)
            A, B = set(a_set), set(b_set)
            for a in A - B:
                for b in B - A:
                    O[a, b] += 1

    def pack(keys):
        u, cnt = np.unique(np.frombuffer(keys, dtype=np.int64), return_counts=True)
        return np.c_[u // GG, (u % GG) // G, u % G].astype(np.int64), cnt.astype(np.int64)
    ok_k, ok_v = pack(okeys)
    ik_k, ik_v = pack(ikeys)
    return dict(M=M, outF=outF, inF=inF, O=O, outFF_keys=ok_k, outFF_vals=ok_v, inFF_keys=ik_k, inFF_vals=ik_v,
                citing_year0=cy0, cited_year0=y0, n_cited_years=ny), n_cit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--target", type=int, default=100_000)
    a = ap.parse_args()
    w = a.work
    w.mkdir(parents=True, exist_ok=True)
    c = Client(w / "cache_LOCAL", w / "client_state.json")
    started = time.strftime("%Y-%m-%d %H:%M:%S")
    sf = subfields(c)
    (w / "subfields.json").write_text(json.dumps(sf, indent=1), encoding="utf-8")
    log("subfields", len(sf))
    C, N = cooccurrence(c, sf)
    np.savez_compressed(w / "cooccurrence.npz", C=C, N=N, subfield_ids=np.array([s["id"] for s in sf]))
    log("co-occurrence done; universe", N)
    works = sample_works(c, a.target)
    with gzip.open(w / "sample_ids.txt.gz", "wt") as f:
        f.write("\n".join(sorted(works)))
    refs = {r for v in works.values() for r in v[2]}
    log("distinct referenced works", len(refs))
    info = lookup(c, refs)
    agg, n_cit = aggregate(works, info, sf)
    np.savez_compressed(w / "flow_aggregates.npz", subfield_ids=np.array([s["id"] for s in sf]), **agg)
    c.save()
    json.dump({"preregistration": "PREREGISTRATION_OPENALEX.md", "started": started,
               "finished": time.strftime("%Y-%m-%d %H:%M:%S"), "filter": BASE_FILTER,
               "subfields": len(sf), "cooccurrence_universe": int(N), "citing_works": len(works),
               "distinct_referenced_works": len(refs), "referenced_works_found": len(info),
               "citations_aggregated": int(n_cit), "requests_by_day": c.state["days"]},
              open(w / "fetch_log.json", "w"), indent=1)
    log("done; citations aggregated", n_cit)


if __name__ == "__main__":
    main()
