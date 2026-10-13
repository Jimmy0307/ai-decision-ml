"""61 — EA-X human content-validity (CVI) analyzer v2.3. Implements the pre-registered plan of 56 section 6 for the
revised anchors v2.2.1 (56 section 8.2). Deterministic; standard library only.

Without human ratings EA-X stays CONDITIONAL_CANDIDATE. AI ratings (56 section 8, AI_CONTENT_VALIDITY_PILOT) are never
accepted: every reviewer must be typed HUMAN, attested, and every input file must be hash-frozen before analysis.

Inputs (folder, default eax_cvi_import/):
  reviewers.csv    reviewer_id,reviewer_type,role_group,anchor_version,attestation_signed,attestation_date
  ratings.csv      reviewer_id,item,relevance,clarity,ambiguity,next_level_more_demanding,suggested_rewording
                   item in {DEF,L0,L1,L2,L3}; relevance/clarity 1-4; ambiguity in {none,EA-V,H,response,other};
                   next_level_more_demanding in {yes,no,unsure} (blank for DEF and L3)
  set_ratings.csv  reviewer_id,representativeness,missing_aspects        (representativeness 1-4, rated once)
  sort.csv         reviewer_id,statement_id,assigned                       (statement 1-8; assigned in {EA-X,EA-V,H,response})
  FREEZE_MANIFEST.txt  SHA-256 lines of the four files above, written by the coordinator before analysis

Usage:
  python 61_EAX_HUMAN_CVI_ANALYZER_v2_3.py                       -> EA-X CONDITIONAL_CANDIDATE (no human ratings)
  python 61_EAX_HUMAN_CVI_ANALYZER_v2_3.py --in eax_cvi_import    -> I-CVI, modified kappa, S-CVI/Ave, S-CVI/UA, ...
  python 61_EAX_HUMAN_CVI_ANALYZER_v2_3.py --self-test
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = "61_EAX_HUMAN_CVI_ANALYZER_v2_3"
ITEMS = ["DEF", "L0", "L1", "L2", "L3"]
AMBIG = {"none", "EA-V", "H", "response", "other"}
SORT_KEY = {1: "EA-X", 2: "EA-V", 3: "H", 4: "response", 5: "EA-X", 6: "EA-V", 7: "H", 8: "response"}   # 56 section 5 / 8.1
ANCHOR_VERSION = "v2.2.1"
ICVI_MIN, MIN_REVIEWERS, PLANNED_PANEL = 0.78, 3, (6, 8)     # 56 section 6 (Polit, Beck, & Owen, 2007); 56 section 3
PENDING = "[HUMAN RESULT PENDING]"


class CVIImportError(ValueError):
    pass


def sha256(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def _read(path, header):
    with open(path, encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        if rd.fieldnames is None or [x.strip() for x in rd.fieldnames] != header:
            raise CVIImportError(f"{os.path.basename(path)}: header must be exactly {','.join(header)}")
        return [{k: (v or "").strip() for k, v in r.items()} for r in rd]


def _int(v, lo, hi, where):
    try:
        x = int(v)
    except ValueError:
        raise CVIImportError(f"{where}: integer {lo}-{hi} required")
    if not lo <= x <= hi:
        raise CVIImportError(f"{where}: out of range {lo}-{hi}")
    return x


def load(folder):
    files = dict(reviewers=["reviewer_id", "reviewer_type", "role_group", "anchor_version", "attestation_signed", "attestation_date"],
                 ratings=["reviewer_id", "item", "relevance", "clarity", "ambiguity", "next_level_more_demanding", "suggested_rewording"],
                 set_ratings=["reviewer_id", "representativeness", "missing_aspects"],
                 sort=["reviewer_id", "statement_id", "assigned"])
    man = os.path.join(folder, "FREEZE_MANIFEST.txt")
    frozen = {l.split()[0] for l in open(man, encoding="utf-8") if l.strip() and not l.startswith("#")} if os.path.exists(man) else set()
    data, hashes = {}, {}
    for name, hdr in files.items():
        p = os.path.join(folder, f"{name}.csv")
        if not os.path.exists(p):
            raise CVIImportError(f"missing {name}.csv")
        h = sha256(p)
        if h not in frozen:
            raise CVIImportError(f"{name}.csv not hash-frozen in {man} -- freeze before analysis")
        hashes[name] = h
        data[name] = _read(p, hdr)
    revs = {}
    for r in data["reviewers"]:
        if r["reviewer_type"] != "HUMAN":
            raise CVIImportError(f"reviewer {r['reviewer_id']}: reviewer_type must be HUMAN (AI ratings are AI_CONTENT_VALIDITY_PILOT, "
                                 "never CVI evidence)")
        if r["anchor_version"] != ANCHOR_VERSION:
            raise CVIImportError(f"reviewer {r['reviewer_id']}: anchors must be {ANCHOR_VERSION} (56 section 8.2)")
        if r["attestation_signed"] != "yes" or not r["attestation_date"]:
            raise CVIImportError(f"reviewer {r['reviewer_id']}: signed independence statement (56 section 3) required")
        if r["reviewer_id"] in revs:
            raise CVIImportError(f"duplicate reviewer {r['reviewer_id']}")
        revs[r["reviewer_id"]] = r
    ratings = {}
    for r in data["ratings"]:
        rid, it = r["reviewer_id"], r["item"]
        if rid not in revs or it not in ITEMS:
            raise CVIImportError(f"ratings: unknown reviewer or item {rid}/{it}")
        if (rid, it) in ratings:
            raise CVIImportError(f"ratings: duplicate {rid}/{it}")
        if r["ambiguity"] not in AMBIG:
            raise CVIImportError(f"ratings {rid}/{it}: ambiguity must be one of {sorted(AMBIG)}")
        nl = r["next_level_more_demanding"]
        if it in ("DEF", "L3"):
            if nl:
                raise CVIImportError(f"ratings {rid}/{it}: next_level_more_demanding must be blank")
        elif nl not in ("yes", "no", "unsure"):
            raise CVIImportError(f"ratings {rid}/{it}: next_level_more_demanding must be yes/no/unsure")
        ratings[(rid, it)] = dict(relevance=_int(r["relevance"], 1, 4, f"{rid}/{it} relevance"),
                                  clarity=_int(r["clarity"], 1, 4, f"{rid}/{it} clarity"), ambiguity=r["ambiguity"],
                                  next=nl, rewording=r["suggested_rewording"])
    for rid in revs:
        miss = [it for it in ITEMS if (rid, it) not in ratings]
        if miss:
            raise CVIImportError(f"reviewer {rid}: missing ratings for {miss} (missing ratings are never imputed)")
    if not revs:
        raise CVIImportError("no reviewers")
    sets = {}
    for r in data["set_ratings"]:
        if r["reviewer_id"] not in revs:
            raise CVIImportError("set_ratings: unknown reviewer")
        if r["reviewer_id"] in sets:
            raise CVIImportError(f"set_ratings: duplicate reviewer {r['reviewer_id']}")
        sets[r["reviewer_id"]] = dict(rep=_int(r["representativeness"], 1, 4, "representativeness"), missing=r["missing_aspects"])
    sort = {}
    for r in data["sort"]:
        if r["reviewer_id"] not in revs or r["assigned"] not in ("EA-X", "EA-V", "H", "response"):
            raise CVIImportError(f"sort: invalid row {r}")
        key = (r["reviewer_id"], _int(r["statement_id"], 1, 8, "statement_id"))
        if key in sort:
            raise CVIImportError(f"sort: duplicate {key}")
        sort[key] = r["assigned"]
    for rid in revs:                                     # missing ratings are never imputed or silently dropped
        if rid not in sets:
            raise CVIImportError(f"reviewer {rid}: representativeness rating missing")
        miss = [s_ for s_ in SORT_KEY if (rid, s_) not in sort]
        if miss:
            raise CVIImportError(f"reviewer {rid}: confusion-sort answers missing for statements {miss}")
    return revs, ratings, sets, sort, hashes


def wilson(k, n, z=1.959963984540054):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def modified_kappa(icvi, n, a):
    pc = math.comb(n, a) * 0.5 ** n                    # Polit, Beck, & Owen (2007)
    return (icvi - pc) / (1 - pc), pc


def analyze(revs, ratings, sets, sort):
    n = len(revs)
    items, retained = {}, []
    for it in ITEMS:
        rel = [ratings[(r, it)]["relevance"] for r in revs]
        a = sum(x >= 3 for x in rel)
        icvi = a / n
        ks, pc = modified_kappa(icvi, n, a)
        flags = [ratings[(r, it)]["ambiguity"] for r in revs if ratings[(r, it)]["ambiguity"] != "none"]
        clar = [ratings[(r, it)]["clarity"] for r in revs]
        nxt = [ratings[(r, it)]["next"] for r in revs if ratings[(r, it)]["next"]]
        if n < MIN_REVIEWERS:
            dec = "INSUFFICIENT_REVIEWERS"
        elif round(icvi, 2) >= ICVI_MIN and len(flags) <= 1:      # I-CVI compared at two decimals (e.g. 7/9 = .78)
            dec = "RETAIN"
        else:
            dec = "REWORD_AND_RERATE"
        reasons = []
        if round(icvi, 2) < ICVI_MIN:
            reasons.append(f"I-CVI {icvi:.2f} < {ICVI_MIN}")
        if len(flags) > 1:
            reasons.append(f"{len(flags)} reviewers place it in another construct: {sorted(set(flags))}")
        if nxt and sum(x == "yes" for x in nxt) / len(nxt) < ICVI_MIN:
            reasons.append("cumulativity to the next level not supported (yes-share < .78): check in V2 before using the order")
        if sum(x >= 3 for x in clar) / n < ICVI_MIN:
            reasons.append("clarity: fewer than 78% rate 3-4 (descriptive; reword recommended)")
        items[it] = dict(n=n, agree_3_4=a, I_CVI=icvi, I_CVI_wilson95=wilson(a, n), modified_kappa=ks, p_chance=pc,
                         clarity_mean=sum(clar) / n, clarity_share_3_4=sum(x >= 3 for x in clar) / n,
                         ambiguity_flags={k: flags.count(k) for k in sorted(set(flags))},
                         next_level_more_demanding={k: nxt.count(k) for k in ("yes", "no", "unsure")} if nxt else None,
                         decision=dec, recommendations=reasons,
                         suggested_rewordings=[ratings[(r, it)]["rewording"] for r in revs if ratings[(r, it)]["rewording"]])
        if dec == "RETAIN":
            retained.append(it)
    s_ave = sum(items[i]["I_CVI"] for i in ITEMS) / len(ITEMS)
    s_ua = sum(items[i]["I_CVI"] == 1.0 for i in ITEMS) / len(ITEMS)
    reps = [sets[r]["rep"] for r in revs if r in sets]
    sort_acc = {}
    for s_id, truth in SORT_KEY.items():
        got = [sort[(r, s_id)] for r in revs if (r, s_id) in sort]
        sort_acc[s_id] = dict(key=truth, n=len(got), accuracy=(sum(g == truth for g in got) / len(got)) if got else None,
                              misassigned={g: got.count(g) for g in set(got) if g != truth})
    all_ok = retained == ITEMS
    status = ("CONDITIONAL_CANDIDATE — content validity supported for definition and all four levels; leaves conditional status "
              "only after the V2 two-round pilot confirms the levels are distinguishable (56 section 6)") if all_ok else \
             (f"CONDITIONAL_CANDIDATE — revise and re-rate {[i for i in ITEMS if i not in retained]}")
    return dict(n_reviewers=n, below_planned_panel=n < PLANNED_PANEL[0],
                role_groups=sorted({revs[r]["role_group"] for r in revs}), items=items,
                S_CVI_Ave=s_ave, S_CVI_UA=s_ua, scale_index_used_for_report="S-CVI/Ave (S-CVI/UA also reported)",
                representativeness=dict(n=len(reps), mean=(sum(reps) / len(reps)) if reps else None,
                                        share_3_4=(sum(x >= 3 for x in reps) / len(reps)) if reps else None,
                                        missing_aspects=[sets[r]["missing"] for r in revs if r in sets and sets[r]["missing"]]),
                confusion_sort=sort_acc, eax_status=status)


def render(res):
    if "items" not in res:
        return f"# EA-X human CVI ({VERSION})\n\nEA-X status: **{res['eax_status']}**\n\nAll result cells: {PENDING}\n"
    L = [f"# EA-X human CVI ({VERSION})", "", f"Reviewers: {res['n_reviewers']} (role groups: {', '.join(res['role_groups'])})"
         + (" — below the planned panel of 6–8" if res["below_planned_panel"] else ""), "",
         "| Item | I-CVI [Wilson 95%] | k* | Clarity 3–4 share | Ambiguity flags | Next level more demanding | Decision |",
         "|---|---|---|---|---|---|---|"]
    for it, r in res["items"].items():
        L.append(f"| {it} | {r['I_CVI']:.2f} [{r['I_CVI_wilson95'][0]:.2f}, {r['I_CVI_wilson95'][1]:.2f}] | {r['modified_kappa']:.2f} | "
                 f"{r['clarity_share_3_4']:.2f} | {r['ambiguity_flags'] or 'none'} | {r['next_level_more_demanding'] or '—'} | {r['decision']} |")
    L += ["", f"S-CVI/Ave = {res['S_CVI_Ave']:.2f}; S-CVI/UA = {res['S_CVI_UA']:.2f}", "",
          f"Representativeness: mean {res['representativeness']['mean']}", "", "| Statement | Key | Accuracy | Misassigned |", "|---|---|---|---|"]
    for s, r in res["confusion_sort"].items():
        L.append(f"| {s} | {r['key']} | {r['accuracy']} | {r['misassigned']} |")
    L += ["", f"EA-X status: **{res['eax_status']}**"]
    return "\n".join(L) + "\n"


def run(argv):
    folder, out = None, os.path.join(HERE, "eax_cvi_results")
    i = 0
    while i < len(argv):
        if argv[i] == "--in":
            folder = argv[i + 1]; i += 2
        elif argv[i] == "--out":
            out = argv[i + 1]; i += 2
        else:
            raise SystemExit(f"unknown argument {argv[i]}")
    if folder is None:
        res = dict(analyzer=VERSION, eax_status="CONDITIONAL_CANDIDATE", reason="no human ratings supplied; the AI content-validity "
                   "pilot (56 section 8) is never used as CVI evidence")
    else:
        revs, ratings, sets, sort, hashes = load(folder)
        res = dict(analyzer=VERSION, input_sha256=hashes, **analyze(revs, ratings, sets, sort))
    os.makedirs(out, exist_ok=True)
    json.dump(res, open(os.path.join(out, "EAX_CVI_RESULTS.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(out, "TABLE_4_2.md"), "w", encoding="utf-8").write(render(res))
    return res


def self_test():
    ks, pc = modified_kappa(5 / 6, 6, 5)
    assert abs(pc - 6 / 64) < 1e-12 and abs(ks - (5 / 6 - 6 / 64) / (1 - 6 / 64)) < 1e-12
    lo, hi = wilson(5, 6)
    assert 0 < lo < 5 / 6 < hi <= 1
    tmp = tempfile.mkdtemp(prefix="eax_selftest_")
    try:
        assert run(["--out", os.path.join(tmp, "o")])["eax_status"] == "CONDITIONAL_CANDIDATE"
        d = os.path.join(tmp, "in"); os.makedirs(d)
        R = [f"T{i}" for i in range(6)]

        def w(name, header, rows):
            with open(os.path.join(d, name), "w", newline="", encoding="utf-8") as f:
                ww = csv.writer(f); ww.writerow(header); ww.writerows(rows)
        w("reviewers.csv", ["reviewer_id", "reviewer_type", "role_group", "anchor_version", "attestation_signed", "attestation_date"],
          [[r, "HUMAN", "TEST", ANCHOR_VERSION, "yes", "2026-01-01"] for r in R])
        rows = []
        for i, r in enumerate(R):
            for it in ITEMS:
                rel = 2 if (it == "L3" and i < 3) else 4                    # L3: 3/6 relevant -> I-CVI .50 -> reword
                amb = "EA-V" if (it == "L1" and i < 2) else "none"          # L1: 2 ambiguity flags -> reword
                rows.append([r, it, rel, 3, amb, "" if it in ("DEF", "L3") else "yes", ""])
        w("ratings.csv", ["reviewer_id", "item", "relevance", "clarity", "ambiguity", "next_level_more_demanding", "suggested_rewording"], rows)
        w("set_ratings.csv", ["reviewer_id", "representativeness", "missing_aspects"], [[r, 3, ""] for r in R])
        w("sort.csv", ["reviewer_id", "statement_id", "assigned"], [[r, s, SORT_KEY[s]] for r in R for s in SORT_KEY])
        try:
            run(["--in", d, "--out", os.path.join(tmp, "o")]); raise AssertionError("unfrozen accepted")
        except CVIImportError:
            pass
        with open(os.path.join(d, "FREEZE_MANIFEST.txt"), "w") as f:
            for n in ("reviewers", "ratings", "set_ratings", "sort"):
                f.write(f"{sha256(os.path.join(d, n + '.csv'))}  {n}.csv\n")
        res = run(["--in", d, "--out", os.path.join(tmp, "o")])
        assert res["items"]["DEF"]["decision"] == "RETAIN" and abs(res["items"]["DEF"]["I_CVI"] - 1) < 1e-12
        assert res["items"]["L3"]["decision"] == "REWORD_AND_RERATE" and abs(res["items"]["L3"]["I_CVI"] - 0.5) < 1e-12
        assert res["items"]["L1"]["decision"] == "REWORD_AND_RERATE"
        assert abs(res["S_CVI_Ave"] - (4 + 0.5) / 5) < 1e-12 and abs(res["S_CVI_UA"] - 4 / 5) < 1e-12
        assert res["eax_status"].startswith("CONDITIONAL_CANDIDATE")
        rv = os.path.join(d, "reviewers.csv")
        txt = open(rv).read().replace("T0,HUMAN", "T0,AI")
        open(rv, "w").write(txt)
        with open(os.path.join(d, "FREEZE_MANIFEST.txt"), "a") as f:
            f.write(f"{sha256(rv)}  reviewers.csv\n")
        try:
            run(["--in", d, "--out", os.path.join(tmp, "o")]); raise AssertionError("AI reviewer accepted")
        except CVIImportError:
            pass
    finally:
        shutil.rmtree(tmp)
    print("SELF-TEST PASS: modified-kappa oracle (N=6, A=5); CONDITIONAL_CANDIDATE without input; unfrozen inputs and AI reviewers "
          "rejected; I-CVI, S-CVI/Ave, S-CVI/UA and retain/reword rules on labelled TEST fixtures (not results)")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test(); sys.exit(0)
    try:
        r = run(sys.argv[1:])
    except CVIImportError as e:
        print(json.dumps(dict(analyzer=VERSION, eax_status="CONDITIONAL_CANDIDATE", import_error=str(e)), indent=1)); sys.exit(2)
    print(json.dumps(dict(analyzer=VERSION, eax_status=r["eax_status"]), indent=1, ensure_ascii=False))
