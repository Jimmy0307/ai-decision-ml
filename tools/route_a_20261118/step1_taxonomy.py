"""Step 1: taxonomy revision evidence and candidate coarser taxonomies.

Confusion sources (all frozen V9 materials):
  H-H  first coder vs blind second coder (n=20)          — human inter-rater
  M-H  model label vs first coder (n=50, Robust-A only)  — model validity
  M-M  stage-2 pass 1 vs pass 2 on the same task (n<=166) — model test-retest (V9.1 segmentation run)
Outputs: per-side pairwise confusion table, per-family agreement, and agreement/kappa recomputed
under candidate taxonomies T0 (original 10x12), T1 (a-priori theory-grouped), T2 (confusion-driven).
T1 is defined from the ratified definitions BEFORE inspecting the new reliability study; T2 is derived
from the confusion evidence below and therefore must be validated on NEW data (it is data-dependent).
"""
import os, json, itertools
from collections import Counter, defaultdict
import ra_lib as L
from step_common import kappa, alpha_nominal

OUTD = os.path.join(L.OUT, "01_taxonomy")

T1_AI = {"PERCEPTION_EXTRACTION": "A1_SENSE_RETRIEVE", "RETRIEVAL_SYNTHESIS": "A1_SENSE_RETRIEVE",
         "PREDICTION_RISK_ESTIMATION": "A2_PREDICT", "RECOMMENDATION_OPTIMIZATION": "A3_PRESCRIBE_OPTIMIZE",
         "GENERATION_SYNTHESIS": "A4_GENERATE", "EXPLANATION_ASSURANCE": "A5_ASSURE_EVALUATE",
         "EVALUATION_ASSESSMENT": "A5_ASSURE_EVALUATE", "COORDINATION_EXECUTION": "A6_ACT_AUGMENT",
         "HUMAN_AUGMENTATION": "A6_ACT_AUGMENT", "GENERAL_REASONING_SYSTEMS": "A7_GENERAL_REASONING"}
T1_DE = {"PROBLEM_FRAMING": "D1_INTELLIGENCE", "INFORMATION_ACQUISITION": "D1_INTELLIGENCE",
         "INFORMATION_SYNTHESIS": "D1_INTELLIGENCE", "PREDICTION_DIAGNOSIS": "D1_INTELLIGENCE",
         "RISK_ASSESSMENT": "D1_INTELLIGENCE", "OPTION_GENERATION": "D2_DESIGN",
         "EVALUATION_SELECTION": "D3_CHOICE", "ALLOCATION_PLANNING": "D3_CHOICE",
         "EXECUTION_COORDINATION": "D4_IMPLEMENTATION", "GOVERNANCE_OVERSIGHT": "D5_REVIEW_CONTROL",
         "HUMAN_REVIEW_ACCOUNTABILITY": "D5_REVIEW_CONTROL", "GENERAL_DECISION_PROCESS": "D6_GENERAL"}
SPECIAL = {"UNMAPPED", "AMBIGUOUS", "", "INSUFFICIENT_EVIDENCE"}


def pairs_hh():
    f = {r["record_id"]: r for r in L.read_csv(os.path.join(L.INP, "FIRST_CODER_50_FINAL_FROZEN.csv"))}
    b = {r["record_id"]: r for r in L.read_csv(os.path.join(L.INP, "BLIND_REPEAT_20_FINAL_FROZEN.csv"))}
    return {"AI": [(f[i]["human_ai_family"], b[i]["human_ai_family"]) for i in b],
            "DECISION": [(f[i]["human_decision_family"], b[i]["human_decision_family"]) for i in b]}


def pairs_mh():
    out = {"AI": [], "DECISION": []}
    for r in L.read_csv(os.path.join(L.INP, "FIRST_CODER_50_FINAL_FROZEN.csv")):
        out["AI"].append((r["source_model_family_canonical_AI"] or "UNMAPPED", r["human_ai_family"]))
        out["DECISION"].append((r["source_model_family_canonical_DECISION"] or "UNMAPPED", r["human_decision_family"]))
    return out


def pairs_mm():
    by = defaultdict(dict)
    for r in L.read_csv(os.path.join(L.INP, "SEGMENT_STAGE2_RESULTS.csv")):
        if r["task_status"] != "VALID":
            continue
        ref = json.loads(r["references_json"])[0]
        by[(ref["record_id"], r["side"])][r["pass_no"]] = r["decision"]
    out = {"AI": [], "DECISION": []}
    for (_, side), v in by.items():
        if "1" in v and "2" in v:
            out["AI" if side == "LEFT" else "DECISION"].append((v["1"], v["2"]))
    return out


def recode(pairs, mp):
    return [(mp.get(a, a), mp.get(b, b)) for a, b in pairs]


def summarize(pairs):
    a = [x for x, _ in pairs]; b = [y for _, y in pairs]
    sub = [(x, y) for x, y in pairs if x not in SPECIAL and y not in SPECIAL]
    return {"n": len(pairs), "exact": sum(x == y for x, y in pairs), "kappa": round(kappa(a, b), 4) if pairs else None,
            "alpha": round(alpha_nominal(pairs), 4) if pairs else None,
            "n_both_substantive": len(sub), "kappa_both_substantive": round(kappa([x for x, _ in sub], [y for _, y in sub]), 4) if len(sub) > 1 else None}


def main():
    src = {"HH_first_vs_blind_20": pairs_hh(), "MH_model_vs_first_50": pairs_mh(), "MM_stage2_pass1_vs_pass2": pairs_mm()}
    conf_rows, rep = [], {"sources": {}, "taxonomies": {}}
    pair_mass = {"AI": Counter(), "DECISION": Counter()}
    for name, sides in src.items():
        rep["sources"][name] = {s: len(p) for s, p in sides.items()}
        for side, pairs in sides.items():
            for x, y in pairs:
                if x != y:
                    key = tuple(sorted((x, y)))
                    pair_mass[side][key] += 1
                    conf_rows.append({"source": name, "side": side, "label_a": x, "label_b": y})
    pair_rows = [{"side": s, "family_1": k[0], "family_2": k[1], "disagreements_all_sources": v,
                  "involves_unmapped_or_ambiguous": bool(set(k) & SPECIAL)}
                 for s in pair_mass for k, v in pair_mass[s].most_common()]
    L.write_csv(os.path.join(OUTD, "PAIRWISE_CONFUSION_ALL_SOURCES.csv"), pair_rows)
    L.write_csv(os.path.join(OUTD, "DISAGREEMENT_EVENTS.csv"), conf_rows)

    # T2: merge substantive family pairs confused >= 2 times across sources (single-linkage, same side)
    t2 = {}
    for side in ("AI", "DECISION"):
        fams = L.AI_FAMS if side == "AI" else L.DEC_FAMS
        parent = {f: f for f in fams}
        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x
        for (x, y), v in pair_mass[side].items():
            if v >= 2 and x in parent and y in parent:
                parent[find(x)] = find(y)
        groups = defaultdict(list)
        for f in fams:
            groups[find(f)].append(f)
        mp = {}
        for g in groups.values():
            label = "+".join(sorted(g)) if len(g) > 1 else g[0]
            for f in g:
                mp[f] = label
        t2[side] = mp
    taxa = {"T0_original": ({}, {}), "T1_theory": (T1_AI, T1_DE), "T2_confusion": (t2["AI"], t2["DECISION"])}
    for tname, (mai, mde) in taxa.items():
        rep["taxonomies"][tname] = {"ai_categories": len(set(mai.get(f, f) for f in L.AI_FAMS)),
                                    "decision_categories": len(set(mde.get(f, f) for f in L.DEC_FAMS)),
                                    "mapping_ai": mai, "mapping_decision": mde, "agreement": {}}
        for sname, sides in src.items():
            rep["taxonomies"][tname]["agreement"][sname] = {
                "AI": summarize(recode(sides["AI"], mai)), "DECISION": summarize(recode(sides["DECISION"], mde))}
    rep["top_confusions"] = {s: [(k[0], k[1], v) for k, v in pair_mass[s].most_common(10)] for s in pair_mass}
    rep["guard"] = ("Agreement under T2 is optimistic by construction (merges chosen from the same disagreements). "
                    "Only a NEW independent reliability sample can validate any taxonomy.")
    L.write_json(os.path.join(OUTD, "TAXONOMY_EVIDENCE_REPORT.json"), rep)
    short = {t: {s: {side: (v[side]["n"], v[side]["exact"], v[side]["kappa"], v[side]["alpha"]) for side in v}
                 for s, v in d["agreement"].items()} for t, d in rep["taxonomies"].items()}
    print(json.dumps({"sources": rep["sources"], "categories": {t: (d["ai_categories"], d["decision_categories"]) for t, d in rep["taxonomies"].items()},
                      "n_exact_kappa_alpha": short, "top_confusions": rep["top_confusions"], "T2": t2}, indent=1))


if __name__ == "__main__":
    main()
