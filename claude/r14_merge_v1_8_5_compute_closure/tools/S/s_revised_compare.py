"""Baseline (reproduced) vs revised comparison -> 52, 54 and a summary JSON for 53/55/58 (stdlib; no pipeline imports).
Usage: python -I -B s_revised_compare.py
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(r"C:\NTUST_PAPER\outputs\00_CURRENT\06_COMPUTE_CLOSURE_V1_8_5")
RPT = Path(r"C:\NTUST_PAPER\outputs\00_CURRENT\02_STUDY1_FREEZE\02_STUDY1_FREEZE_V1_8_1\repo\claude\r14_merge_v1_8_5_compute_closure")
BASE = ROOT / r"compute_closure\baseline_reproduction\20261014T041645Z"
REV = ROOT / r"compute_closure\revised_audited_label_analysis\20261014T042729Z"
SC = ROOT / r"work\inputs_S_sidecar_corrected_20261014"
V9S = ROOT / r"work\inputs_S_20261014T040934Z\V9\ROBUST_CORE_LOCAL_SENSITIVITY.csv"
GCSV = SC / "11_Priority_Gaps_Frozen_Export_G01_G16_v1_0_20261009.csv"


def rows(p):
    with Path(p).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def latest(run, sd):
    return Path(next((run / sd).glob("LATEST_*.txt")).read_text(encoding="utf-8").strip())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(run, fz):
    d10, d11, d12, d13 = (latest(run, s) for s in ("10_DOCUMENT_DEDUP_MATRIX", "11_NULL_MODEL_NETWORK", "12_ROBUSTNESS_SENSITIVITY", "13_RESULTS_FREEZE"))
    key = lambda r: (r["ai_family"], r["decision_family"])
    main = {key(r): r for r in rows(d11 / "CELL_NULL_MODEL_RESULTS_120.csv")}
    cmp_ = {key(r): r for r in rows(d12 / "ROBUSTNESS_COMPARISON_120.csv")}
    core = {key(r): r["direction"] for r in rows(d13 / "FINAL_ROBUST_CORE_32.csv")}
    rec = rows(fz / "ANALYTICAL_FREEZE_RECORD_LEVEL.csv")
    eli = rows(fz / "ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv")
    edges = rows(d10 / "DOCUMENT_PAIR_EDGES_DEDUP.csv")
    g = {"strict_records": len(rec), "pair_eligible": len(eli), "unique_documents": len({r["document_id"] for r in eli}),
         "document_edges": len(edges), "primary_q05": sum(float(r["q_bh_two_sided"]) <= 0.05 for r in main.values()),
         "primary_q01": sum(float(r["q_bh_two_sided"]) <= 0.01 for r in main.values()),
         "exact_q05": sum(float(r["exact_q"]) <= 0.05 for r in cmp_.values()),
         "document_null_q05": sum(float(r["document_null_q"]) <= 0.05 for r in cmp_.values()),
         "raw_q05": sum(float(r["raw_q"]) <= 0.05 for r in cmp_.values()),
         "robust_core": len(core), "enriched": sum(v == "ENRICHED" for v in core.values()), "depleted": sum(v == "DEPLETED" for v in core.values())}
    hashes = {"core": sha(d13 / "FINAL_ROBUST_CORE_32.csv"), "results_canonical": sha(d13 / "FINAL_RESULTS_FREEZE_CANONICAL.json"),
              "matrix_canonical": sha(d10 / "DOCUMENT_DEDUP_MATRIX_CANONICAL.json"), "null_canonical": sha(d11 / "NULL_MODEL_NETWORK_CANONICAL.json"),
              "robust_canonical": sha(d12 / "ROBUSTNESS_SENSITIVITY_CANONICAL.json"), "dirs": [str(d) for d in (d10, d11, d12, d13)]}
    return main, cmp_, core, g, hashes, (d10, d11, d12, d13)


def main():
    bfz = ROOT / r"work\run_inputs_baseline_20261014T041645Z\09_ANALYTICAL_FREEZE\analytical_freeze_v2_20260918T132206Z"
    rfz = REV / r"09_ANALYTICAL_FREEZE\analytical_freeze_v2_BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1"
    bm, bc, bcore, bg, bh, bdirs = load(BASE, bfz)
    rm, rc, rcore, rg, rh, rdirs = load(REV, rfz)
    out, mem = [], []
    for k in sorted(bm):
        b, r, b2, r2 = bm[k], rm[k], bc[k], rc[k]
        brob, rrob = k in bcore, k in rcore
        bdir, rdir = bcore.get(k, ""), rcore.get(k, "")
        out.append({"AI_family": k[0], "Decision_family": k[1],
                    "baseline_observed": b["observed"], "revised_observed": r["observed"], "observed_delta": int(r["observed"]) - int(b["observed"]),
                    "baseline_raw_observed": b2["raw_observed"], "revised_raw_observed": r2["raw_observed"],
                    "baseline_expected": b["independence_expected"], "revised_expected": r["independence_expected"],
                    "baseline_primary_p": b["p_two_sided"], "revised_primary_p": r["p_two_sided"],
                    "baseline_primary_q": b["q_bh_two_sided"], "revised_primary_q": r["q_bh_two_sided"],
                    "baseline_hypergeom_q": b2["exact_q"], "revised_hypergeom_q": r2["exact_q"],
                    "baseline_doc_null_q": b2["document_null_q"], "revised_doc_null_q": r2["document_null_q"],
                    "baseline_raw_sensitivity_q": b2["raw_q"], "revised_raw_sensitivity_q": r2["raw_q"],
                    "baseline_main_direction": b["direction"], "revised_main_direction": r["direction"],
                    "baseline_robust": brob, "revised_robust": rrob, "baseline_core_direction": bdir, "revised_core_direction": rdir,
                    "membership_changed": brob != rrob, "direction_changed": b["direction"] != r["direction"],
                    "core_direction_changed": brob and rrob and bdir != rdir})
        status = "UNCHANGED_MEMBER" if brob and rrob else "GAINED" if rrob else "LOST" if brob else "UNCHANGED_NONMEMBER"
        mem.append({"AI_family": k[0], "Decision_family": k[1], "status": status, "baseline_direction": bdir, "revised_direction": rdir,
                    "core_direction_changed": brob and rrob and bdir != rdir, "main_direction_changed": b["direction"] != r["direction"],
                    "baseline_doc_null_q": b2["document_null_q"], "revised_doc_null_q": r2["document_null_q"]})
    for name, data in (("52_ALL_120_CELLS_BASELINE_VS_REVISED.csv", out), ("54_ROBUST_CORE_MEMBERSHIP_DIFF.csv", mem)):
        with (RPT / name).open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(data[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(data)
    # G01-G16
    G = []
    for r in rows(GCSV):
        k = (r["AI_Family"], r["Decision_Family"])
        G.append({"G": r["Gap_ID"], "cell": f"{k[0]} x {k[1]}", "baseline_robust": k in bcore, "revised_robust": k in rcore,
                  "baseline_direction": bcore.get(k, ""), "revised_direction": rcore.get(k, ""),
                  "baseline_O": bm[k]["observed"], "revised_O": rm[k]["observed"], "baseline_doc_q": bc[k]["document_null_q"], "revised_doc_q": rc[k]["document_null_q"],
                  "revised_main_q": rm[k]["q_bh_two_sided"], "revised_exact_q": rc[k]["exact_q"], "revised_raw_q": rc[k]["raw_q"]})
    # sidecar cross-check (V9 ROBUST_CORE_LOCAL_SENSITIVITY.csv) - cross-check only
    sc_rows = {(r["ai_family"], r["decision_family"]): r for r in rows(V9S)}
    cols = [("sidecar_observed", rm, "observed"), ("sidecar_main_direction", rm, "direction"), ("sidecar_main_q", rm, "q_bh_two_sided"),
            ("sidecar_exact_q", rc, "exact_q"), ("sidecar_exact_direction", rc, "exact_direction"), ("sidecar_document_q", rc, "document_null_q"),
            ("sidecar_document_direction", rc, "document_null_direction"), ("sidecar_raw_q", rc, "raw_q"), ("sidecar_raw_direction", rc, "raw_direction"),
            ("sidecar_raw_observed", rc, "raw_observed"), ("sidecar_document_observed", rc, "dedup_observed"), ("sidecar_exact_observed", rc, "dedup_observed")]
    sc_cmp = {}
    for col, src, sk in cols:
        mism, maxd = 0, 0.0
        for k, s in sc_rows.items():
            a, b = s[col], src[k][sk]
            try:
                d = abs(float(a) - float(b))
                maxd = max(maxd, d)
                mism += d != 0
            except ValueError:
                mism += a != b
        sc_cmp[col] = {"mismatches": mism, "max_abs_diff": maxd}
    core_m = sum(1 for k, s in sc_rows.items() if (s["sidecar_core_member"] == "YES") != (k in rcore))
    core_d = sum(1 for k, s in sc_rows.items() if k in rcore and s["sidecar_core_direction"] != rcore[k])
    off_m = sum(1 for k, s in sc_rows.items() if (s["official_core_member"] == "YES") != (k in bcore))
    # byte comparison with sidecar V5_CORRECTED outputs
    scd = {"09": SC / "09_ANALYTICAL_FREEZE", "10": SC / r"10_DOCUMENT_DEDUP_MATRIX\matrix_v1_20261003T115608Z", "11": SC / r"11_NULL_MODEL_NETWORK\null_model_v1_20261003T115609Z",
           "12": SC / r"12_ROBUSTNESS_SENSITIVITY\robustness_v1_20261003T115615Z", "13": SC / r"13_RESULTS_FREEZE\results_freeze_v1_20261003T115651Z"}
    mine = {"09": rfz, "10": rdirs[0], "11": rdirs[1], "12": rdirs[2], "13": rdirs[3]}
    byte = {}
    for st, d in scd.items():
        for p in sorted(d.iterdir()):
            if p.is_file() and (mine[st] / p.name).exists():
                byte[f"{st}/{p.name}"] = sha(p) == sha(mine[st] / p.name)
    summary = {"baseline": bg, "revised": rg, "baseline_hashes": bh, "revised_hashes": rh,
               "membership": {s: sum(1 for m in mem if m["status"] == s) for s in ("UNCHANGED_MEMBER", "GAINED", "LOST", "UNCHANGED_NONMEMBER")},
               "gained": [f"{m['AI_family']} x {m['Decision_family']} ({m['revised_direction']})" for m in mem if m["status"] == "GAINED"],
               "lost": [f"{m['AI_family']} x {m['Decision_family']} ({m['baseline_direction']})" for m in mem if m["status"] == "LOST"],
               "core_direction_changes": sum(m["core_direction_changed"] for m in mem),
               "main_direction_changes": sum(m["main_direction_changed"] for m in mem),
               "observed_changed_cells": sum(o["observed_delta"] != 0 for o in out),
               "raw_changed_cells": sum(o["baseline_raw_observed"] != o["revised_raw_observed"] for o in out),
               "G": G, "G01_G16_REMOVED": sum(1 for x in G if x["baseline_robust"] and not x["revised_robust"]),
               "G01_G16_DIRECTION_CHANGED": sum(1 for x in G if x["baseline_robust"] and x["revised_robust"] and x["baseline_direction"] != x["revised_direction"]),
               "sidecar_columns_vs_revised": sc_cmp, "sidecar_core_member_mismatch": core_m, "sidecar_core_direction_mismatch": core_d,
               "official_core_member_vs_baseline_mismatch": off_m, "sidecar_V5_CORRECTED_byte_equal": byte,
               "sidecar_csv_sha256": sha(V9S)}
    (RPT / "tools" / "S" / "revised_compare_summary.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k not in ("G", "sidecar_V5_CORRECTED_byte_equal")}, indent=1))
    print("byte-equal with sidecar V5_CORRECTED:", sum(byte.values()), "/", len(byte), [k for k, v in byte.items() if not v])


if __name__ == "__main__":
    main()
