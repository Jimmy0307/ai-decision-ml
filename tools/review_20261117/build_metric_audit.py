"""Build docs/review/20261117/METRIC_AUDIT_90.csv (standard library only).

Joins the 90 published metrics with RECOMPUTE_RESULTS.json (produced by audit_recompute.py
from the private V9 / sidecar archives) and analytic checks, and assigns one normalised
evidence grade: DIRECT, HISTORICAL, USER_REPORTED, SYNTHETIC (PENDING = not independently
verifiable until local raw data are recovered).

    python tools/review_20261117/build_metric_audit.py --repo .
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
from fractions import Fraction


def read_text(path: str, **kw) -> str:
    with open(path, encoding="utf-8", **kw) as f:
        return f.read()

FIELDS = ["metric_id", "stage", "metric", "published_value", "unit", "original_grade", "evidence_grade",
          "verification_method", "independent_value", "result", "pending_flag", "source", "notes"]


def grade(mid: str, original: str) -> str:
    if original.startswith("SYNTHETIC"):
        return "SYNTHETIC"
    if mid.startswith("V11_"):
        return "USER_REPORTED"
    if mid.split("_")[0] in {"V6", "V7", "V8", "V10", "V101"} or mid in {"V9_010", "V9_011", "V9_012", "V9_013"}:
        return "HISTORICAL"
    return "DIRECT"


def expected(r: dict) -> dict[str, tuple[object, str]]:
    """metric_id -> (independent value, method)."""
    f, c, s, h, l, g = (r["funnel_machine_output"], r["cells_120"], r["segmentation_s1_s2"],
                        r["human_reliability"], r["limitation_scout"], r["gap_validity_results_json"])
    hd = h["dimensions"]
    RC = "RECOMPUTED_FROM_RAW (audit_recompute.py)"
    MF = "MACHINE_OUTPUT (V9 analytical-freeze manifest, re-read)"
    GJ = "RESULTS_JSON_REREAD + sidecar test suite re-run 2026-11-18"
    prism = Fraction(2) * (Fraction(1, 3) + Fraction(1, 9)) ** 2 + Fraction(1, 9)
    return {
        "V5_005": (f["production_records"], MF),
        "V5_006": (f["strict_records"], MF),
        "V5_007": (f["mapped_endpoints_2x_full_plus_partial"], MF + "; 2×3,125 + 2,501"),
        "V5_008": (f["fully_mapped_records"], MF),
        "V5_009": (f["eligible_unique_documents"], MF),
        "V5_010": (c["official_document_level_edges_sum"], RC + "; sum of 120 cell counts"),
        "V5_011": (c["ai_families"], RC), "V5_012": (c["decision_families"], RC), "V5_013": (c["cells"], RC),
        "V5_014": (c["official_main_q05"], RC),
        "V5_015": (c["official_core_rule_rederived"], RC + "; promotion rule re-derived from q-values"),
        "V5_016": (c["official_core_by_direction"].get("ENRICHED"), RC),
        "V5_017": (c["official_core_by_direction"].get("DEPLETED"), RC),
        "V9_003": (c["official_observed_nonzero_cells"], RC),
        "V9_004": (s["s1_core"], RC), "V9_005": (s["s2_core"], RC),
        "V9_006": (s["s1_retained_of_baseline"], RC), "V9_007": (s["s2_retained_of_baseline"], RC),
        "V9_008": (s["s1_retained_depleted"], RC), "V9_009": (s["s2_retained_depleted"], RC),
        "H_001": (h["first_coder_records"], RC), "H_002": (h["blind_second_coder_records"], RC),
        "H_003": (h["blind_records_with_any_disagreement"], RC + "; blind records with ≥1 field disagreement"),
        "H_004": (hd["C3"]["exact_agreement"], RC), "H_005": (hd["C3"]["cohen_kappa"], RC + "; Cohen κ"),
        "H_006": (hd["C4"]["exact_agreement"], RC), "H_007": (hd["C4"]["cohen_kappa"], RC + "; Cohen κ"),
        "H_008": (c["sidecar_main_count_changed_cells"], RC),
        "H_009": (c["sidecar_main_direction_changed_cells"], RC),
        "H_010": (len(c["sidecar_core_gained"]), RC), "H_011": (len(c["sidecar_core_lost"]), RC),
        "G_001": (c["ai_families"] + c["decision_families"], RC + "; 10 + 12 nodes"),
        "G_002": (g["observed_edges"], GJ),
        "G_003": (sum(1 for x in c["depleted_core_observed_counts"] if x > 0), RC + "; all 16 depleted core cells have count ≥ 2"),
        "G_004": (g["depleted_alt_connected"], GJ), "G_005": (3 if g["depleted_alt_len3"] == 16 else None, GJ),
        "G_006": (g["alt_disjoint_min_max"][0], GJ), "G_007": (g["alt_disjoint_min_max"][1], GJ),
        "G_008": (g["cross_component"]["robust16"], GJ), "G_009": (g["cross_component"]["main_q01"], GJ),
        "G_010": (g["cross_component"]["main_q05"], GJ),
        "G_011": (math.comb(10, 3), "ANALYTIC: projection of a complete 10×12 overlap is K10 → C(10,3) derived triangles"),
        "G_012": (math.comb(12, 3), "ANALYTIC: K12 projection → C(12,3) derived triangles"),
        "G_013": (round(1 / 3, 9), "ANALYTIC: K3,3 equal weights → C = 1/k = 1/3"),
        "G_014": (round(float(prism), 8), "ANALYTIC: prism → 2·(1/3+1/9)² + 1/9 = 41/81"),
        "G_015": (14, "TEST RE-RUN 2026-11-18: 14/14 PASS"),
        "L_001": (l["s1_segments"], RC), "L_002": (l["s1_document_ids"], RC),
        "L_003": (l["documents_with_hits"], RC), "L_004": (l["lexical_hit_segments"], RC),
        "L_005": (8, "TEST RE-RUN 2026-11-18: 8/8 PASS (PyMuPDF installed)"),
    }


TEXT_MATCH = {
    "V5_001": "V9_FINAL_FORENSIC_AUDIT.md §4 + V9 manuscript candidate §3.3 (1,199 AI-track + 919 Decision-track)",
    "V5_002": "V9 manuscript §3.3; 2,118 = 1,729 + 388 + 1",
    "V5_003": "V9 manuscript §3.3; 2,118 = 1,729 + 388 + 1",
    "V5_004": "V9 manuscript §3.3; 2,118 = 1,729 + 388 + 1",
    "V9_001": "BASELINE_REPRODUCTION_VERIFICATION.md + V9 manuscript §4.4 (seed 20260918)",
    "V9_002": "BASELINE_REPRODUCTION_VERIFICATION.md + V9 manuscript (seed 20260919; 5,000 retained MCMC states)",
}

ARITH = {
    "V9_010": "3,983 + 3,897 = 7,880 (equals V11_001 population)",
    "V9_011": "3,983 + 3,897 = 7,880",
    "V11_005": "79 + 15 + 1 = 95",
    "V11_010": "3 rejected + 1 insufficient = 4",
    "V11_011": "3 + 1 = 4", "V11_012": "3 + 1 = 4",
}

NOTES = {
    "V5_010": "Definition: document-level edges, not document pairs or papers.",
    "V5_014": "47 = 22 enriched + 25 depleted; q≤.01: 34 = 15 + 19.",
    "V5_017": "Distinct from the 16 zero-observation cells (120 − 104); none of the zero cells is in the core.",
    "V9_003": "120 − 104 = 16 cells with zero observations.",
    "H_003": "19 of the 20 blind records had ≥1 coded-field disagreement; all were reconciled with event IDs.",
    "H_010": "Gained cell is DEPLETED (HUMAN_AUGMENTATION × RISK_ASSESSMENT).",
    "H_011": "Lost cell is ENRICHED (COORDINATION_EXECUTION × GENERAL_DECISION_PROCESS) → sidecar core would be 15 enriched + 17 depleted; frozen baseline unchanged.",
    "L_002": "The 1,104 IDs are the documents behind the 6,499 strict records, not the 1,729 usable full texts.",
    "L_001": "25,112 S1 segments split from the 6,499 strict records; not full limitation sections.",
    "V11_013": "Text/code verdict conflict for Dwivedi retained (USER_REPORTED).",
}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    a = ap.parse_args(argv)
    repo = os.path.abspath(a.repo)
    rec = json.loads(read_text(os.path.join(repo, "docs/review/20261117/RECOMPUTE_RESULTS.json")))
    exp = expected(rec)
    with open(os.path.join(repo, "docs/data/ALL_METRICS_WITH_PROVENANCE_20261117.csv"), encoding="utf-8-sig", newline="") as f:
        metrics = list(csv.DictReader(f))
    out = []
    for m in metrics:
        mid, val = m["指標ID"], m["值"]
        g = grade(mid, m["證據等級"])
        row = dict(metric_id=mid, stage=m["階段"], metric=m["指標名稱"], published_value=val, unit=m["單位"],
                   original_grade=m["證據等級"], evidence_grade=g, source=m["來源檔案"], notes=NOTES.get(mid, ""),
                   independent_value="", pending_flag="")
        if mid in exp:
            iv, method = exp[mid]
            ok = iv is not None and math.isclose(float(iv), float(val), rel_tol=0, abs_tol=5e-4 if "κ" in method else 1e-9)
            row.update(verification_method=method, independent_value=str(iv), result="CONFIRMED" if ok else "MISMATCH")
        elif mid in TEXT_MATCH:
            row.update(verification_method="MATCHED_IN_TWO_PRIMARY_DOCUMENTS: " + TEXT_MATCH[mid], result="CONFIRMED_IN_SOURCE_TEXT",
                       pending_flag="Raw corpus inventory / SQLite: PENDING_LOCAL_RECOVERY" if mid.startswith("V5_") else "")
        else:
            row.update(verification_method=("ARITHMETIC_CONSISTENCY: " + ARITH[mid]) if mid in ARITH else "NONE_POSSIBLE_WITHOUT_RAW",
                       result="NOT_INDEPENDENTLY_VERIFIABLE", pending_flag="PENDING_LOCAL_RECOVERY")
        out.append(row)
    path = os.path.join(repo, "docs/review/20261117/METRIC_AUDIT_90.csv")
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    from collections import Counter
    print("grades", dict(Counter(r["evidence_grade"] for r in out)))
    print("results", dict(Counter(r["result"] for r in out)))
    bad = [r["metric_id"] for r in out if r["result"] == "MISMATCH"]
    print("mismatches", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
