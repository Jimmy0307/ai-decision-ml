"""Sub-agent P, Task 2: recompute the frozen Study 1 baseline from raw V5 rows.

Descriptive recomputation only (counts, set equality, dedup, BH re-adjustment of frozen
p-values for consistency). No null model / reanalysis is run. Read-only; stdlib only.

Usage: python -I p_task2_baseline_recompute.py <V5_ROOT> <W_V9_DIR> <REPO> <OUT_JSON>
"""
import csv
import hashlib
import json
import os
import sqlite3
import sys
from collections import Counter

csv.field_size_limit(1 << 30)
_c = {}


def sha(p):
    if p not in _c:
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for b in iter(lambda: fh.read(1 << 20), b""):
                h.update(b)
        _c[p] = h.hexdigest()
    return _c[p]


def rows(p):
    with open(p, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def fnum(x):
    x = (x or "").strip()
    if x.startswith("<"):
        return None
    try:
        return float(x)
    except ValueError:
        return None


def tf(x):
    return str(x).strip().lower() in ("true", "1", "yes")


RESULTS = []


def rec(item, value, expected, source, method):
    if expected is None:
        status = "INFO"
    else:
        status = "MATCH" if value == expected else "CONFLICT"
    srcs = source if isinstance(source, list) else [source]
    RESULTS.append(dict(item=item, value=value, expected=expected, status=status, method=method,
                        sources=[dict(path=s, sha256=sha(s)) for s in srcs]))
    return status


def bh(ps):
    n = len(ps)
    order = sorted(range(n), key=lambda i: ps[i])
    q = [0.0] * n
    prev = 1.0
    for rank in range(n, 0, -1):
        i = order[rank - 1]
        prev = min(prev, ps[i] * n / rank)
        q[i] = prev
    return q


def main():
    v5, wv9, repo, out_json = sys.argv[1:5]
    d09 = os.path.join(v5, "09_ANALYTICAL_FREEZE", "analytical_freeze_v2_20260918T132206Z")
    d10 = os.path.join(v5, "10_DOCUMENT_DEDUP_MATRIX", "matrix_v1_20260918T132505Z")
    d11 = os.path.join(v5, "11_NULL_MODEL_NETWORK", "null_model_v1_20260918T132933Z")
    d12 = os.path.join(v5, "12_ROBUSTNESS_SENSITIVITY", "robustness_v1_20260918T133618Z")
    d13 = os.path.join(v5, "13_RESULTS_FREEZE", "results_freeze_v1_20260919T080120Z")
    d13a = os.path.join(v5, "13_RESULTS_FREEZE", "results_freeze_v1_20260919T075633Z")
    d14 = os.path.join(v5, "14_MANUSCRIPT_DATA_PACK", "data_pack_v1_20260922T010012Z")
    d14a = os.path.join(v5, "14_MANUSCRIPT_DATA_PACK", "data_pack_v1_20260919T081003Z")
    extra = {}

    # ---------- A. strict records ----------
    p_rec = os.path.join(d09, "ANALYTICAL_FREEZE_RECORD_LEVEL.csv")
    R = rows(p_rec)
    ids = [r["record_id"] for r in R]
    rec("strict_records (rows in RECORD_LEVEL.csv)", len(R), 6499, p_rec, "row count")
    rec("strict_records unique record_id", len(set(ids)), 6499, p_rec, "distinct record_id")
    rec("strict unique documents", len({r["document_id"] for r in R}), 1104, p_rec, "distinct document_id")
    mc = Counter(r["mapping_completeness"] for r in R)
    rec("FULLY_MAPPED records", mc["FULLY_MAPPED"], 3125, p_rec, "count mapping_completeness")
    rec("PARTIALLY_MAPPED records", mc["PARTIALLY_MAPPED"], 2501, p_rec, "count mapping_completeness")
    rec("FULLY_UNRESOLVED records", mc["FULLY_UNRESOLVED"], 873, p_rec, "count mapping_completeness")
    elig = [r for r in R if tf(r["analytical_pair_eligible"])]
    rec("pair_eligible_records (analytical_pair_eligible=True)", len(elig), 3125, p_rec, "count flag")
    rec("pair_excluded_records", len(R) - len(elig), 3374, p_rec, "6499 - eligible")
    rec("pair-excluded share of strict (manuscript 51.9%)", round((len(R) - len(elig)) / len(R) * 100, 1), 51.9,
        p_rec, "3374/6499*100 rounded 1dp")
    elig_both_mapped = all(r["left_final_status"] == "MAPPED" and r["right_final_status"] == "MAPPED"
                           and r["left_final_family"] and r["right_final_family"] for r in elig)
    rec("every eligible record has both sides MAPPED", elig_both_mapped, True, p_rec, "row check")
    rec("eligible == FULLY_MAPPED set", {r["record_id"] for r in elig} ==
        {r["record_id"] for r in R if r["mapping_completeness"] == "FULLY_MAPPED"}, True, p_rec, "set equality")
    rec("unique documents among pair-eligible", len({r["document_id"] for r in elig}), 783, p_rec,
        "distinct document_id over eligible rows")
    p_el = os.path.join(d09, "ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv")
    p_ex = os.path.join(d09, "ANALYTICAL_PAIR_EXCLUDED_RECORDS.csv")
    E1, X1 = rows(p_el), rows(p_ex)
    rec("ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv rows / set == flagged eligible",
        (len(E1), {r["record_id"] for r in E1} == {r["record_id"] for r in elig}), (3125, True), p_el, "rows + set eq")
    rec("ANALYTICAL_PAIR_EXCLUDED_RECORDS.csv rows / disjoint & union == strict",
        (len(X1), {r["record_id"] for r in X1}.isdisjoint({r["record_id"] for r in E1}),
         {r["record_id"] for r in X1} | {r["record_id"] for r in E1} == set(ids)),
        (3374, True, True), p_ex, "rows + partition")
    p_can = os.path.join(d09, "ANALYTICAL_FREEZE_CANONICAL.json")
    with open(p_can, encoding="utf-8") as fh:
        can = json.load(fh)
    can_ids = {r.get("record_id") for r in can["records"]}
    rec("canonical JSON records == CSV record set", (len(can["records"]), can_ids == set(ids)), (6499, True),
        p_can, "set equality canonical vs CSV")
    can_elig = {r.get("record_id") for r in can["records"] if str(r.get("pair_eligible")) == "True"}
    rec("canonical JSON pair-eligible set == CSV eligible set", can_elig == {r["record_id"] for r in elig}, True,
        p_can, "set equality (canonical key pair_eligible)")
    csv_by_id = {r["record_id"]: r for r in R}
    fam_ok = all(c["left_family"] == csv_by_id[c["record_id"]]["left_final_family"] and
                 c["right_family"] == csv_by_id[c["record_id"]]["right_final_family"] and
                 c["left_status"] == csv_by_id[c["record_id"]]["left_final_status"] and
                 c["right_status"] == csv_by_id[c["record_id"]]["right_final_status"] and
                 c["document_id"] == csv_by_id[c["record_id"]]["document_id"] for c in can["records"])
    rec("canonical JSON per-record doc/families/statuses == CSV", fam_ok, True, [p_can, p_rec], "per-record compare")
    rt = Counter(r["relation_type"] for r in R)
    extra["strict_relation_type_share_pct"] = {k: round(v / len(R) * 100, 2) for k, v in rt.most_common()}
    exp_rt = {"ENABLES": 37.70, "SUPPORTS": 34.33, "CONSTRAINS": 11.29, "INFORMS": 7.82, "GOVERNS": 6.60,
              "TRANSFORMS": 2.18, "ASSOCIATED_WITH": 0.08}
    rec("strict relation-type shares (manuscript 3.3.2)", extra["strict_relation_type_share_pct"] == exp_rt, True,
        p_rec, "count/6499*100 rounded 2dp")

    # sides
    p_side = os.path.join(d09, "ANALYTICAL_FREEZE_SIDE_LEVEL.csv")
    S = rows(p_side)
    rec("strict functional sides", len(S), 12998, p_side, "row count")
    rs = Counter(r["resolution_stage"] for r in S)
    fs = Counter(r["final_status"] for r in S)
    rec("stage1 resolved sides", rs["STAGE1_DETERMINISTIC_ANCHOR"], 4079, p_side, "count resolution_stage")
    rec("stage2-eligible sides (12998-4079)", len(S) - rs["STAGE1_DETERMINISTIC_ANCHOR"], 8919, p_side, "difference")
    rec("stage2 accepted sides", rs["STAGE2_CONSTRAINED_DOUBLE_PASS"], 4672, p_side, "count resolution_stage")
    rec("mapped sides", fs["MAPPED"], 8751, p_side, "count final_status")
    rec("unmapped sides", len(S) - fs["MAPPED"], 4247, p_side, "12998-8751")
    rec("mapped share % (manuscript 67.3)", round(fs["MAPPED"] / len(S) * 100, 1), 67.3, p_side, "rounded 1dp")
    rec("semantic review sides", fs["UNRESOLVED_SEMANTIC_REVIEW"], 3862, p_side, "count final_status")
    rec("technical review sides", fs["UNRESOLVED_TECHNICAL_REVIEW"], 164, p_side, "count final_status")
    rec("insufficient-evidence sides", fs["UNMAPPED_INSUFFICIENT_EVIDENCE"], 221, p_side, "count final_status")

    # ---------- B. document dedup edges ----------
    ai_fam = {r["ai_family"] for r in rows(os.path.join(d10, "AI_FAMILY_MARGINALS.csv"))}
    dec_fam = {r["decision_family"] for r in rows(os.path.join(d10, "DECISION_FAMILY_MARGINALS.csv"))}
    left_in_ai = all(r["left_final_family"] in ai_fam and r["right_final_family"] in dec_fam for r in elig)
    rec("eligible: left side in AI families, right side in Decision families", left_in_ai, True,
        [p_rec, os.path.join(d10, "AI_FAMILY_MARGINALS.csv")], "membership check")
    rec("AI families x Decision families", (len(ai_fam), len(dec_fam), len(ai_fam) * len(dec_fam)), (10, 12, 120),
        [os.path.join(d10, "AI_FAMILY_MARGINALS.csv"), os.path.join(d10, "DECISION_FAMILY_MARGINALS.csv")], "count")
    edges = {(r["document_id"], r["left_final_family"], r["right_final_family"]) for r in elig}
    rec("document-level dedup edges M (recomputed)", len(edges), 2180, p_rec, "distinct (doc, AI fam, Dec fam)")
    rec("collapsed duplicate records", len(elig) - len(edges), 945, p_rec, "3125 - 2180")
    p_ed = os.path.join(d10, "DOCUMENT_PAIR_EDGES_DEDUP.csv")
    ED = rows(p_ed)
    fe = {(r["document_id"], r["ai_family"], r["decision_family"]) for r in ED}
    rec("frozen DOCUMENT_PAIR_EDGES_DEDUP.csv == recomputed edge set", (len(ED), fe == edges), (2180, True), p_ed,
        "set equality")
    rec("frozen edge source_record_count sums to 3125", sum(int(r["source_record_count"]) for r in ED), 3125, p_ed, "sum")
    obs = Counter((a, d) for _, a, d in edges)
    ka = Counter(a for _, a, _ in edges)
    kd = Counter(d for _, _, d in edges)
    M = len(edges)

    # ---------- C. cells ----------
    p_cell = os.path.join(d14, "11_CELL_RESULTS_ALL_120.csv")
    C = rows(p_cell)
    rec("11_CELL_RESULTS_ALL_120 rows", len(C), 120, p_cell, "row count")
    obs_ok = all(int(float(r["observed"])) == obs[(r["ai_family"], r["decision_family"])] for r in C)
    deg_ok = all(int(float(r["ai_degree"])) == ka[r["ai_family"]] and
                 int(float(r["decision_degree"])) == kd[r["decision_family"]] and int(float(r["M"])) == M for r in C)
    e_diff = max(abs(float(r["independence_expected"]) - ka[r["ai_family"]] * kd[r["decision_family"]] / M) for r in C)
    oe_diff = max(abs(float(r["observed_expected_ratio"]) -
                      obs[(r["ai_family"], r["decision_family"])] / (ka[r["ai_family"]] * kd[r["decision_family"]] / M))
                  for r in C)
    rec("120 cell observed == recomputed from edges", obs_ok, True, [p_cell, p_rec], "per-cell compare")
    rec("120 cell k_a, k_d, M == recomputed", deg_ok, True, p_cell, "per-cell compare")
    rec("max |E_frozen - k_a*k_d/M|", e_diff < 1e-9, True, p_cell, f"max abs diff = {e_diff:.3e}")
    rec("max |O/E_frozen - O/E_recomputed|", oe_diff < 1e-9, True, p_cell, f"max abs diff = {oe_diff:.3e}")
    for fn in ("OBSERVED_MATRIX_10X12.csv",):
        pm = os.path.join(d11, fn)
        mat = rows(pm)
        key0 = list(mat[0].keys())[0]
        ok = all(int(float(row[d])) == obs[(row[key0], d)] for row in mat for d in dec_fam)
        rec("11 OBSERVED_MATRIX_10X12 == recomputed", ok, True, pm, "per-cell compare")
    q = [float(r["q_bh_two_sided"]) for r in C]
    rec("primary q<=.05 cells", sum(x <= 0.05 for x in q), 47, p_cell, "count q_bh_two_sided<=0.05")
    rec("primary q<=.01 cells", sum(x <= 0.01 for x in q), 34, p_cell, "count q_bh_two_sided<=0.01")
    q_re = bh([float(r["p_two_sided"]) for r in C])
    qd = max(abs(a - b) for a, b in zip(q_re, q))
    rec("BH(p_two_sided) re-adjustment == frozen q", qd < 1e-12, True, p_cell, f"max abs diff = {qd:.3e}")
    # robust core recomputation from ROBUSTNESS_COMPARISON_120
    p_cmp = os.path.join(d12, "ROBUSTNESS_COMPARISON_120.csv")
    CMP = rows(p_cmp)
    robust = {}
    for r in CMP:
        qs = [float(r[k]) for k in ("main_mc_q", "exact_q", "document_null_q", "raw_q")]
        dirs = {r[k] for k in ("main_mc_direction", "exact_direction", "document_null_direction", "raw_direction")}
        if all(x <= 0.05 for x in qs) and len(dirs) == 1:
            robust[(r["ai_family"], r["decision_family"])] = dirs.pop()
    nen = sum(v == "ENRICHED" for v in robust.values())
    rec("robust core recomputed (4 q<=.05 + same direction)", (len(robust), nen, len(robust) - nen), (32, 16, 16),
        p_cmp, "rule applied to frozen per-method q/direction")
    cmp_dedup_ok = all(int(float(r["dedup_observed"])) == obs[(r["ai_family"], r["decision_family"])] for r in CMP)
    rec("ROBUSTNESS_COMPARISON dedup_observed == recomputed", cmp_dedup_ok, True, p_cmp, "per-cell")
    raw_obs = Counter((r["left_final_family"], r["right_final_family"]) for r in elig)
    raw_ok = all(int(float(r["raw_observed"])) == raw_obs[(r["ai_family"], r["decision_family"])] for r in CMP)
    rec("ROBUSTNESS_COMPARISON raw_observed == recomputed record counts", raw_ok, True, [p_cmp, p_rec], "per-cell")
    p_core = os.path.join(d13, "FINAL_ROBUST_CORE_32.csv")
    core = {(r["ai_family"], r["decision_family"]): r["direction"] for r in rows(p_core)}
    rec("FINAL_ROBUST_CORE_32 == recomputed robust set (with direction)", core == robust, True, p_core, "dict equality")
    p_dep = os.path.join(d13, "FINAL_ROBUST_DEPLETED.csv")
    p_enr = os.path.join(d13, "FINAL_ROBUST_ENRICHED.csv")
    dep = {(r["ai_family"], r["decision_family"]) for r in rows(p_dep)}
    enr = {(r["ai_family"], r["decision_family"]) for r in rows(p_enr)}
    rec("FINAL_ROBUST_DEPLETED/ENRICHED partition", (len(dep), len(enr), dep | enr == set(core), dep & enr == set()),
        (16, 16, True, True), [p_dep, p_enr], "set ops")
    p_sm = os.path.join(d13, "FINAL_ROBUST_STATUS_MATRIX_10X12.csv")
    sm = rows(p_sm)
    smd = {(row["AI_FAMILY"], d): row[d] for row in sm for d in dec_fam}
    rec("FINAL_ROBUST_STATUS_MATRIX == recomputed", all(
        (smd[k] == robust[k]) if k in robust else smd[k] == "NOT_ROBUST" for k in smd) and len(smd) == 120, True,
        p_sm, "per-cell")
    cell_class = all((r["final_result_class"] == "ROBUST_" + ("ENRICHMENT" if robust[(r["ai_family"], r["decision_family"])] == "ENRICHED" else "DEPLETION"))
                     if (r["ai_family"], r["decision_family"]) in robust else not r["final_result_class"].startswith("ROBUST")
                     for r in C)
    rec("11_CELL_RESULTS final_result_class == recomputed", cell_class, True, p_cell, "per-cell")
    # 13a vs 13
    p_core_a = os.path.join(d13a, "FINAL_ROBUST_CORE_32.csv")
    ca = rows(p_core_a)
    cb = {(r["ai_family"], r["decision_family"]): r for r in rows(p_core)}
    shared_ok = all(all(r[k] == cb[(r["ai_family"], r["decision_family"])][k] for k in r) for r in ca)
    rec("13 run 075633Z core rows == 080120Z on all shared columns", (len(ca), shared_ok), (32, True),
        [p_core_a, p_core], "row/column compare; 080120Z adds observed_minus_expected")

    # ---------- D. G01-G16 ----------
    p_g = os.path.join(repo, "11_Priority_Gaps_Frozen_Export_G01_G16_v1_0_20261009.csv")
    G = rows(p_g)
    gset = {(r["AI_Family"], r["Decision_Family"]) for r in G}
    rec("G01-G16 set == V5 16 robust depleted", (len(G), gset == dep), (16, True), [p_g, p_dep], "set equality")
    cmap = {(r["ai_family"], r["decision_family"]): r for r in C}
    gdet = []
    for r in G:
        k = (r["AI_Family"], r["Decision_Family"])
        c = cmap[k]
        o = obs[k]
        e = ka[k[0]] * kd[k[1]] / M
        row = dict(G=r["Gap_ID"], ai=k[0], dec=k[1], O_v5=o, O_G=fnum(r["Observed"]), ka_v5=ka[k[0]],
                   ka_G=fnum(r["k_a"]), kd_v5=kd[k[1]], kd_G=fnum(r["k_d"]), E_v5=e, E_G=fnum(r["E_analytic"]),
                   OE_v5=round(o / e, 4), OE_G=fnum(r["O_E_Ratio"]), null_mean_v5=float(c["null_mean"]),
                   null_mean_G=fnum(r["Null_Mean"]), q_main_v5=float(c["q_bh_two_sided"]),
                   q_main_G=r["q_primary_BH"], q_exact_v5=float(c["exact_q"]), q_exact_G=r["q_exact"],
                   q_doc_v5=float(c["document_null_q"]), q_doc_G=r["q_document_preserving"],
                   q_raw_v5=float(c["raw_q"]), q_raw_G=r["q_raw_record"])
        ok = (row["O_v5"] == row["O_G"] and row["ka_v5"] == row["ka_G"] and row["kd_v5"] == row["kd_G"] and
              abs(row["E_v5"] - row["E_G"]) < 1e-9 and row["OE_v5"] == row["OE_G"] and
              abs(row["null_mean_v5"] - row["null_mean_G"]) < 1e-9)
        for a, b in (("q_main_v5", "q_main_G"), ("q_exact_v5", "q_exact_G"), ("q_doc_v5", "q_doc_G"),
                     ("q_raw_v5", "q_raw_G")):
            gv = row[b].strip()
            if gv.startswith("<"):
                ok = ok and row[a] < float(gv[1:])
            else:
                ok = ok and abs(round(row[a], 4) - float(gv)) < 1e-12
        row["match"] = ok
        gdet.append(row)
    extra["G_detail"] = gdet
    rec("G01-G16 per-G O, k_a, k_d, E, O/E(4dp), null mean, 4 q (4dp / '<.0001') == V5", all(r["match"] for r in gdet),
        True, [p_g, p_cell], "per-row compare")
    p132 = os.path.join(repo, "claude", "r14_merge_v1_8_1_study1_freeze", "current_artifacts",
                        "132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX_v1_8_1.csv")
    T = rows(p132)
    t_ok, t_det = True, []
    for r in T:
        gid = r["G ID"]
        k = (r["AI family"], r["Decision family"])
        o132 = fnum(r["O (doc-level edges)"])
        oe132 = fnum(r["O/E"])
        e = ka[k[0]] * kd[k[1]] / M
        ok = k in dep and o132 == obs[k] and oe132 == round(obs[k] / e, 4) and abs(fnum(r["E analytic = k_a·k_d/M"]) - e) < 1e-9
        t_ok = t_ok and ok
        t_det.append(dict(G=gid, O_132=o132, O_v5=obs[k], OE_132=oe132, OE_v5=round(obs[k] / e, 4), match=ok))
    extra["T132_detail"] = t_det
    rec("132 CSV G rows: O, E, O/E == V5 recomputed (and cell in V5 depleted set)", (len(T), t_ok), (16, True),
        [p132, p_rec], "per-row compare")

    # ---------- E. W ROBUST_CORE_LOCAL_SENSITIVITY official columns ----------
    p_w = os.path.join(wv9, "ROBUST_CORE_LOCAL_SENSITIVITY.csv")
    WR = rows(p_w)
    cm = {(r["ai_family"], r["decision_family"]): r for r in CMP}
    mism = Counter()
    maxd = Counter()
    for r in WR:
        k = (r["ai_family"], r["decision_family"])
        c, x = cmap[k], cm[k]
        checks = {
            "official_observed": (fnum(r["official_observed"]), obs[k]),
            "official_exact_observed": (fnum(r["official_exact_observed"]), obs[k]),
            "official_document_observed": (fnum(r["official_document_observed"]), obs[k]),
            "official_raw_observed": (fnum(r["official_raw_observed"]), raw_obs[k]),
            "official_main_direction": (r["official_main_direction"], x["main_mc_direction"]),
            "official_exact_direction": (r["official_exact_direction"], x["exact_direction"]),
            "official_document_direction": (r["official_document_direction"], x["document_null_direction"]),
            "official_raw_direction": (r["official_raw_direction"], x["raw_direction"]),
            "official_main_q05": (tf(r["official_main_q05"]), float(c["q_bh_two_sided"]) <= 0.05),
            "official_main_q01": (tf(r["official_main_q01"]), float(c["q_bh_two_sided"]) <= 0.01),
            "official_core_member": (r["official_core_member"] == "YES", k in robust),
            "official_core_direction": (r["official_core_direction"] or "", robust.get(k, "")),
        }
        for name, (a, b) in checks.items():
            if a != b:
                mism[name] += 1
        for name, col in (("official_main_q", "main_mc_q"), ("official_exact_q", "exact_q"),
                          ("official_document_q", "document_null_q"), ("official_raw_q", "raw_q")):
            d = abs(float(r[name]) - float(x[col]))
            maxd[name] = max(maxd[name], d)
    extra["W_official_mismatch_counts"] = dict(mism)
    extra["W_official_q_max_abs_diff"] = dict(maxd)
    rec("W ROBUST_CORE_LOCAL_SENSITIVITY official_* (120 rows): categorical/count mismatches",
        (len(WR), sum(mism.values())), (120, 0), [p_w, p_cmp, p_cell], "per-cell compare of 12 columns")
    rec("W official q columns max abs diff vs V5", max(maxd.values()) == 0.0, True, [p_w, p_cmp],
        "max abs diff: " + json.dumps({k: float(v) for k, v in maxd.items()}))
    rec("W official_core_member YES count", sum(r["official_core_member"] == "YES" for r in WR), 32, p_w, "count")

    # ---------- F. lineage numbers from hash-verified source DB ----------
    dbp = r"C:\NTUST_PAPER\LocalCorpusWorkbench\v5_production_app\data\workbench.sqlite"
    con = sqlite3.connect("file:" + dbp.replace("\\", "/") + "?mode=ro&immutable=1", uri=True)
    one = lambda s: con.execute(s).fetchone()[0]  # noqa: E731
    rec("source documents", one("select count(*) from documents"), 2118, dbp, "count documents")
    rec("source_group AI / DECISION", tuple(one(f"select count(*) from documents where source_group='{g}'")
                                           for g in ("AI", "DECISION")), (1199, 919), dbp, "count")
    rec("documents status Done/Skipped/Failed",
        tuple(one(f"select count(*) from documents where status='{s}'") for s in ("Done", "Skipped", "Failed")),
        (1729, 388, 1), dbp, "count")
    rec("pages", one("select count(*) from pages"), 47402, dbp, "count")
    rec("section spans", one("select count(*) from sections"), 9984, dbp, "count")
    rec("candidates", one("select count(*) from candidates"), 26501, dbp, "count")
    rec("semantic records", one("select count(*) from semantic_records"), 26501, dbp, "count")
    rec("documents with semantic records", one("select count(distinct document_id) from semantic_records"), 1729,
        dbp, "distinct document_id")
    rec("strict retained (passed_strict_filter=1)", one("select count(*) from semantic_records where passed_strict_filter=1"),
        6499, dbp, "count")
    rec("strict excluded", one("select count(*) from semantic_records where passed_strict_filter=0"), 20002, dbp, "count")
    rec("excluded: REQUIRES_HUMAN_REVIEW / RELATION_TYPE_AMBIGUOUS",
        (one("select count(*) from semantic_records where strict_exclusion_reason='REQUIRES_HUMAN_REVIEW'"),
         one("select count(*) from semantic_records where strict_exclusion_reason='EXCLUDED_RELATION_TYPE_AMBIGUOUS'")),
        (19942, 60), dbp, "count")
    db_strict = {x[0] for x in con.execute("select record_id from semantic_records where passed_strict_filter=1")}
    rec("source-DB strict record_id set == V5 analytical freeze record set", db_strict == set(ids), True, [dbp, p_rec],
        "set equality")
    rec("reader (agent) outputs", one("select count(*) from agent_outputs"), 5858, dbp, "count")
    rec("integrator (controller) outputs", one("select count(*) from controller_outputs"), 2117, dbp, "count")
    by_g = con.execute("select d.source_group, count(*), sum(s.passed_strict_filter=1) from semantic_records s "
                       "join documents d on d.document_id=s.document_id group by 1").fetchall()
    bg = {g: (n, k) for g, n, k in by_g}
    rec("strict by source group AI k/n, DECISION k/n", (bg["AI"][1], bg["AI"][0], bg["DECISION"][1], bg["DECISION"][0]),
        (5620, 20621, 879, 5880), dbp, "join documents.source_group")
    con.close()
    # data-pack-only numbers (file hash-verified in Task 1, not recomputed from Stage2 sidecar)
    p_gr = os.path.join(d14, "03_STAGE2_GROUNDING_DISTRIBUTION.csv")
    gr = {r["grounding_status"]: int(r["count"]) for r in rows(p_gr)}
    rec("Stage2 grounding EXACT/NORM/UNGROUNDED/NOT_REQUIRED/SCHEMA_INVALID (data pack only)",
        tuple(gr[k] for k in ("EXACT", "NORMALIZED_WHITESPACE_OCR", "UNGROUNDED", "NOT_REQUIRED", "SCHEMA_INVALID")),
        (6916, 6818, 2811, 1087, 349), p_gr, "read from hash-verified data pack; NOT recomputed from sidecar")
    p_att = os.path.join(d14, "01_ATTRITION_AND_GATES.csv")
    att = {r["stage"]: int(r["n"]) for r in rows(p_att)}
    rec("01_ATTRITION_AND_GATES core n values",
        tuple(att[k] for k in ("Production semantic records", "Strict analytical records", "Strict functional sides",
                               "Stage1 resolved sides", "Stage2 eligible sides", "Stage2 accepted sides",
                               "Fully mapped records", "Strict unique documents", "Pair-eligible unique documents",
                               "Document-level dedup edges", "Possible 10x12 cells", "Global fixed-degree q<=.05",
                               "Global fixed-degree q<=.01", "Structurally robust cells")),
        (26501, 6499, 12998, 4079, 8919, 4672, 3125, 1104, 783, 2180, 120, 47, 34, 32), p_att, "read")
    # 14a value-equivalence of the two re-saved files
    for fn, key in (("26_OBSERVED_EXPECTED_RATIO_MATRIX_10X12.csv", None), ("33_EXACT_HYPERGEOMETRIC_RESULTS_120.csv", None)):
        a, b = rows(os.path.join(d14a, fn)), rows(os.path.join(d14, fn))
        md, cat_ok = 0.0, len(a) == len(b)
        for ra, rb in zip(a, b):
            for k in rb:
                va, vb = ra.get(k, ""), rb[k]
                fa, fb = fnum(va), fnum(vb)
                if fa is not None and fb is not None:
                    md = max(md, abs(fa - fb) / max(1.0, abs(fb)))
                elif va.strip().lower() != vb.strip().lower():
                    cat_ok = False
        rec(f"14a {fn} value-equivalent to 14b/stage copy (<=1e-6 rel; spreadsheet re-save precision)", cat_ok and md < 1e-6, True,
            [os.path.join(d14a, fn), os.path.join(d14, fn)], f"max rel diff = {md:.3e}; categorical equal = {cat_ok}")

    out = dict(results=RESULTS, extra=extra,
               conflicts=[r["item"] for r in RESULTS if r["status"] == "CONFLICT"])
    with open(out_json, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=1, default=str)
    for r in RESULTS:
        print(r["status"], "|", r["item"], "|", r["value"], "|", r["method"])
    print("CONFLICTS:", out["conflicts"])
    print(json.dumps(extra["W_official_mismatch_counts"]), json.dumps({k: float(v) for k, v in extra["W_official_q_max_abs_diff"].items()}))


if __name__ == "__main__":
    main()
