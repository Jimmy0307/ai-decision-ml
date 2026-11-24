"""R1: re-analysis of the Norwegian boards data (PREREGISTRATION_OPSAHL.md, amendment R1-A1).

Usage:
    python r1_opsahl.py d1d2 --raw <dir> --out <dir>
    python r1_opsahl.py d3   --raw <dir> --out <dir> --snapshot 2011-08-01 --reps 1000 --workers 6

<dir> holds data_people.txt and net2m_<date>.txt from http://www.opsahl.co.uk/boardsandgender/data.php
(CC BY-NC 3.0; not redistributed). Gender code 2 = women, 1 = men (checked against first names).
D3 needs python-igraph (fast betweenness and Burt constraint); D1/D2 need networkx only.
"""
import argparse
import itertools
import json
import time
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path

import numpy as np

SNAPSHOTS = ["2011-08-01", "2002-05-01", "2008-02-01", "2009-08-01"]   # index = seed component; 0 is primary
SEED = 20261119


def load(raw: Path, snap: str):
    pairs = set()
    for line in (raw / f"net2m_{snap}.txt").read_text(encoding="latin-1").split("\n"):
        p = line.split()
        if len(p) >= 2:
            pairs.add((int(p[0]), int(p[1])))                 # (company, person); duplicates removed
    gender = {}
    for line in (raw / "data_people.txt").read_text(encoding="latin-1").split("\n")[1:]:
        p = line.split()
        if len(p) >= 2 and p[0].isdigit():
            gender[int(p[0])] = int(p[-1])
    boards = defaultdict(set)                                  # person -> companies
    members = defaultdict(set)                                 # company -> persons
    for c, d in pairs:
        boards[d].add(c)
        members[c].add(d)
    return pairs, boards, members, gender


# ------------------------------------------------------------------ D1 projection closure
def projection_edges(members):
    w = defaultdict(int)
    for ms in members.values():
        for a, b in itertools.combinations(sorted(ms), 2):
            w[(a, b)] += 1
    return w


def d1(boards, members):
    import networkx as nx
    w = projection_edges(members)
    G = nx.Graph()
    G.add_nodes_from(boards)
    G.add_edges_from(w)
    trans = nx.transitivity(G)
    tri = clique = 0
    adj = {n: set(G[n]) for n in G}
    for a in G:
        for b in adj[a]:
            if b <= a:
                continue
            for c in adj[a] & adj[b]:
                if c <= b:
                    continue
                tri += 1
                if boards[a] & boards[b] & boards[c]:
                    clique += 1
    # Opsahl (2013) two-mode transitivity: 4-paths i-b1-j-b2-k (i, j, k distinct directors; b1 != b2)
    # closed if some third board b3 (not b1, b2) links i and k
    paths = closed = 0
    for j, bj in boards.items():
        for b1, b2 in itertools.permutations(bj, 2):
            for i in members[b1] - {j}:
                for k in members[b2] - {j, i}:
                    paths += 1
                    if (boards[i] & boards[k]) - {b1, b2}:
                        closed += 1
    return {"directors": len(boards), "boards": len(members), "two_mode_edges": sum(len(v) for v in boards.values()),
            "projection_edges": len(w), "projection_transitivity": trans, "projection_triangles": tri,
            "triangles_within_one_board": clique, "share_triangles_within_one_board": clique / tri if tri else None,
            "dominated_by_board_cliques": (clique / tri >= 0.90) if tri else None,
            "two_mode_4paths": paths, "two_mode_closed_4paths": closed,
            "opsahl_two_mode_transitivity": closed / paths if paths else None}


# ------------------------------------------------------------------ D2 constraint identity on the two-mode graph
def d2(boards, members):
    import networkx as nx
    G = nx.Graph()
    G.add_edges_from((("p", d), ("c", c)) for d, cs in boards.items() for c in cs)
    con = nx.constraint(G, nodes=[("p", d) for d in boards])
    diff = np.array([abs(con[("p", d)] - 1 / len(boards[d])) for d in boards])
    return {"directors": len(boards), "max_abs_diff": float(diff.max()), "share_within_1e-9": float((diff < 1e-9).mean())}


# ------------------------------------------------------------------ D3 affiliation-preserving null
def curveball(boards_list, rng, trades):
    """boards_list: list of sets (one per director). Keeps each director's degree and each board's size."""
    B = [set(s) for s in boards_list]
    n = len(B)
    for _ in range(trades):
        a, b = rng.choice(n, 2, replace=False)
        A, Bb = B[a], B[b]
        oa, ob = A - Bb, Bb - A
        if not oa or not ob:
            continue
        pool = list(oa | ob)
        rng.shuffle(pool)
        k = len(oa)
        B[a] = (A & Bb) | set(pool[:k])
        B[b] = (A & Bb) | set(pool[k:])
    return B


def stats(dirs, boards_list, women, men, multi):
    import igraph as ig
    idx = {d: i for i, d in enumerate(dirs)}
    mem = defaultdict(list)
    for i, bs in enumerate(boards_list):
        for c in bs:
            mem[c].append(i)
    w = defaultdict(int)
    for ms in mem.values():
        for a, b in itertools.combinations(sorted(ms), 2):
            w[(a, b)] += 1
    g = ig.Graph(n=len(dirs), edges=list(w), directed=False)
    g.es["weight"] = list(w.values())
    n = len(dirs)
    btw = np.array(g.betweenness(directed=False)) / ((n - 1) * (n - 2) / 2)
    con = np.array(g.constraint(weights="weight"), dtype=float)
    wi, mi, si = (np.array([idx[d] for d in s]) for s in (women, men, multi))
    med = lambda x: float(np.nanmedian(x)) if np.isfinite(x).any() else float("nan")
    return {"S1": float(btw[wi].mean() - btw[mi].mean()), "S2": float(np.median(btw[si])),
            "S3": med(con[wi]) - med(con[mi]), "S4": med(con[si])}


def _rep(args):
    dirs, blist, women, men, multi, sidx, r, trades = args
    rng = np.random.default_rng([SEED, sidx, r])
    return stats(dirs, curveball(blist, rng, trades), women, men, multi)


def d3(raw, out, snap, reps, workers):
    pairs, boards, members, gender = load(raw, snap)
    dirs = sorted(boards)
    blist = [boards[d] for d in dirs]
    women = [d for d in dirs if gender.get(d) == 2]
    men = [d for d in dirs if gender.get(d) == 1]
    multi = [d for d in dirs if len(boards[d]) >= 3]
    trades = 5 * len(pairs)
    obs = stats(dirs, blist, women, men, multi)
    sidx = SNAPSHOTS.index(snap)
    part = out / f"R1_D3_{snap}_PARTIAL.json"
    null = json.loads(part.read_text()) if part.exists() else []
    t0 = time.time()
    with Pool(workers) as pool:
        todo = [(dirs, blist, women, men, multi, sidx, r, trades) for r in range(len(null), reps)]
        for k, res in enumerate(pool.imap(_rep, todo, chunksize=4)):
            null.append(res)
            if (k + 1) % 50 == 0:
                part.write_text(json.dumps(null))
                print(snap, len(null), "replicates", round(time.time() - t0), "s", flush=True)
    part.write_text(json.dumps(null))
    res = {"snapshot": snap, "primary": sidx == 0, "reps": reps, "trades_per_replicate": trades,
           "n_directors": len(dirs), "n_women": len(women), "n_men": len(men), "n_multi_seat": len(multi),
           "observed": obs, "tests": {}}
    for s, tail in (("S1", "upper"), ("S2", "upper"), ("S3", "lower"), ("S4", "lower")):
        v = np.array([x[s] for x in null], dtype=float)
        v = v[np.isfinite(v)]
        o = obs[s]
        p = (1 + ((v >= o) if tail == "upper" else (v <= o)).sum()) / (1 + len(v))
        res["tests"][s] = {"tail": tail, "observed": o, "null_median": float(np.median(v)),
                           "null_2.5": float(np.percentile(v, 2.5)), "null_97.5": float(np.percentile(v, 97.5)),
                           "ratio_obs_to_null_median": o / float(np.median(v)) if np.median(v) else None,
                           "p": float(p), "label": "BEYOND_AFFILIATION" if p < .05 else "EXPLAINED_BY_AFFILIATION",
                           "valid_null_values": int(len(v))}
    b = [res["tests"][s]["label"] == "BEYOND_AFFILIATION" for s in ("S1", "S2", "S3", "S4")]
    res["overall"] = ("BROKERAGE_READING_SURVIVES" if (b[0] or b[1]) and (b[2] or b[3])
                      else "BROKERAGE_READING_EXPLAINED" if not any(b) else "MIXED")
    (out / f"R1_D3_{snap}.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["d1d2", "d3"])
    ap.add_argument("--raw", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--snapshot", default=SNAPSHOTS[0])
    ap.add_argument("--reps", type=int, default=1000)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    if a.mode == "d1d2":
        res = {}
        for s in SNAPSHOTS:
            pairs, boards, members, gender = load(a.raw, s)
            res[s] = {"D1": d1(boards, members),
                      "women": sum(gender.get(d) == 2 for d in boards), "men": sum(gender.get(d) == 1 for d in boards),
                      "gender_missing": sum(d not in gender for d in boards)}
            if s == SNAPSHOTS[0]:
                res[s]["D2"] = d2(boards, members)
            print(s, json.dumps(res[s]), flush=True)
        (a.out / "R1_D1D2.json").write_text(json.dumps(res, indent=1))
    else:
        d3(a.raw, a.out, a.snapshot, a.reps, a.workers)


if __name__ == "__main__":
    main()
