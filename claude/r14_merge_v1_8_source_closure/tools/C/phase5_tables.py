"""Emit markdown tables for 04_LOCAL_SENSITIVITY_REPRODUCTION.md from phase5 JSON outputs.
Usage: python -I phase5_tables.py <phase5_out.json> <phase5_part2_out.json> <W root>
"""
import json, sys, csv
from pathlib import Path
a = json.load(open(sys.argv[1], encoding="utf-8")); b = json.load(open(sys.argv[2], encoding="utf-8"))
W = Path(sys.argv[3])
full = {f'{r["ai_family"]} x {r["decision_family"]}': r for r in csv.DictReader(open(
    W / "02_V9_HUMAN_VALIDATION/20260929_V9_HUMAN_VALIDATION/ROBUST_CORE_LOCAL_SENSITIVITY.csv", encoding="utf-8-sig"))}
diff = list(csv.DictReader(open(W / "02_V9_HUMAN_VALIDATION/20260929_V9_HUMAN_VALIDATION/ROBUST_CORE_LOCAL_SENSITIVITY_DIFF.csv", encoding="utf-8-sig")))
P = print
P("### T1. Official (frozen) 32-cell core recomputed from CSV rows, with sidecar status\n")
P("| # | AI family x Decision family | Official dir | Sidecar member | Sidecar dir | G ID | main O off->sc | doc q off / sc |")
P("|---|---|---|---|---|---|---|---|")
gmap = {g["pair"]: g["G"] for g in a["G01_G16"]}
allc = sorted(set(a["official_core"]) | set(a["gained"]))
for i, k in enumerate(allc, 1):
    r = full[k]
    P(f'| {i} | {k} | {r["official_core_direction"] or "-(not member)"} | {r["sidecar_core_member"]} | {r["sidecar_core_direction"] or "-"} | {gmap.get(k, "")} | {r["official_observed"]}->{r["sidecar_observed"]} | {float(r["official_document_q"]):.4f} / {float(r["sidecar_document_q"]):.4f} |')
P("\n### T2. G01-G16 mapping (132 matrix) vs official/sidecar core\n")
P("| G | AI family x Decision family | O (132) | O main official (CSV) | official core | sidecar core | sidecar main O |")
P("|---|---|---|---|---|---|---|")
for g in a["G01_G16"]:
    P(f'| {g["G"]} | {g["pair"]} | {g["O_132"]} | {g["official_main_observed"]} | {g["official_core"]} | {g["sidecar_core"] or "REMOVED"} | {g["sidecar_main_observed"]} |')
P("\n### T3. All 33 rows of ROBUST_CORE_LOCAL_SENSITIVITY_DIFF.csv classified\n")
P("| Cell | main O delta | raw O delta | main dir off->sc | core off->sc | change class |")
P("|---|---|---|---|---|---|")
for r in diff:
    cls = []
    if r["core_membership_changed"] == "YES": cls.append("CORE_MEMBERSHIP")
    if r["main_direction_changed"] == "YES": cls.append("MAIN_DIRECTION(non-core)")
    if r["observed_count_delta"] != "0": cls.append("MAIN_COUNT")
    if r["raw_observed_count_delta"] != "0": cls.append("RAW_COUNT")
    if not cls: cls.append("Q_ONLY")
    P(f'| {r["ai_family"]} x {r["decision_family"]} | {r["observed_count_delta"]} | {r["raw_observed_count_delta"]} | {r["official_main_direction"]}->{r["sidecar_main_direction"]} | {r["official_core_member"]}->{r["sidecar_core_member"]} | {"+".join(cls)} |')
P("\n### T4. Audited-record label changes that a full reanalysis would need to propagate (model label -> human label used by sidecar)\n")
P("Source = RECONCILED_FINAL (HUMAN_RECONCILED_20.csv FINAL_C*) for the 20 blind-subset records, FIRST_CODER (FIRST_CODER_50_FINAL_FROZEN.csv human_*) for the other 30. Model side = current_ai_family / current_decision_family / model_analytical_pair_eligible in FIRST_CODER_50_FINAL_FROZEN.csv. Human C1 = evidence validity, C5 = analytical inclusion.\n")
P("| # | record_id | validation_id | source | C1 | inclusion: model -> human C5 | AI family: model -> human | Decision family: model -> human |")
P("|---|---|---|---|---|---|---|---|")
for i, x in enumerate(b["label_changes"], 1):
    incl = f'ELIGIBLE -> {x["human_C5"]}' if x["human_C5"] != "INCLUDE" else "unchanged (INCLUDE)"
    ai = f'{x["model_ai"]} -> {x["human_ai"]}' if x["model_ai"] != x["human_ai"] else f'unchanged ({x["model_ai"]})'
    de = f'{x["model_dec"]} -> {x["human_dec"]}' if x["model_dec"] != x["human_dec"] else f'unchanged ({x["model_dec"]})'
    P(f'| {i} | {x["record_id"]} | {x["validation_id"]} | {x["source"]} | {x["human_C1"]} | {incl} | {ai} | {de} |')
P("\n### T5. First-coder frozen label vs reconciled FINAL label for the 20 blind-subset records\n")
P("| record_id | resolution basis | reconciliation UTC | first-coder -> FINAL differences |")
P("|---|---|---|---|")
for x in b["reconciled_vs_first"]:
    dd = "; ".join(f"{k}: {o} -> {n}" for k, o, n in x["first_coder_frozen_vs_final"]) or "none"
    P(f'| {x["record_id"]} | {x["basis"]} | {x["ts"] or "-"} | {dd} |')
