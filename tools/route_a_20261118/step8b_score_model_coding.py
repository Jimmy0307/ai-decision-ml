"""Step 8b: score independent LLM coders (codebook v2) against each other, the original qwen labels and the
existing human audit labels; test whether 'NONE' judgements are differential by cell type; feed a
model-consensus error model into the step-7 misclassification simulation (scenario E4)."""
import os, glob, json
from collections import Counter, defaultdict
import numpy as np
import ra_lib as L
from step_common import kappa, alpha_nominal
import step7_misclassification as S7

OUTD = os.path.join(L.OUT, "08_model_coding")
VALID_AI = set(L.AI_FAMS) | {"NONE", "AMBIGUOUS"}
VALID_DE = set(L.DEC_FAMS) | {"NONE", "AMBIGUOUS"}
HUM = {"UNMAPPED": "NONE", "": "NONE"}


def norm(v, valid):
    v = (v or "").strip().upper()
    v = HUM.get(v, v)
    return v if v in valid else "INVALID:" + v


def load_coder(prefix):
    out = {}
    for f in sorted(glob.glob(os.path.join(OUTD, "coded", f"{prefix}_BATCH_*.csv"))):
        for r in L.read_csv(f):
            out[r["mm_id"]] = {"ai": norm(r["ai_family"], VALID_AI), "de": norm(r["decision_family"], VALID_DE),
                               "conf": r.get("confidence", "")}
    return out


def agree(pairs):
    if not pairs:
        return {}
    a = [x for x, _ in pairs]; b = [y for _, y in pairs]
    sub = [(x, y) for x, y in pairs if x not in ("NONE", "AMBIGUOUS") and y not in ("NONE", "AMBIGUOUS")]
    return {"n": len(pairs), "exact": sum(x == y for x, y in pairs), "kappa": round(kappa(a, b), 3),
            "alpha": round(alpha_nominal(pairs), 3), "n_both_substantive": len(sub),
            "kappa_both_substantive": round(kappa([x for x, _ in sub], [y for _, y in sub]), 3) if len(sub) > 1 else None}


def main():
    key = {r["mm_id"]: r for r in L.read_csv(os.path.join(OUTD, "MM_MASTER_KEY_HIDDEN.csv"))}
    coders = {"SONNET": load_coder("SONNET"), "HAIKU": load_coder("HAIKU")}
    qwen = {m: {"ai": k["qwen_ai_family"] if k["qwen_ai_family"] in L.AI_FAMS else "NONE",
                "de": k["qwen_decision_family"] if k["qwen_decision_family"] in L.DEC_FAMS else "NONE"} for m, k in key.items()}
    coders["QWEN_v1"] = qwen
    first = {r["record_id"]: r for r in L.read_csv(os.path.join(L.INP, "FIRST_CODER_50_FINAL_FROZEN.csv"))}
    blind = {r["record_id"]: r for r in L.read_csv(os.path.join(L.INP, "BLIND_REPEAT_20_FINAL_FROZEN.csv"))}
    recon = {r["record_id"]: r for r in L.read_csv(os.path.join(L.INP, "HUMAN_RECONCILED_20.csv"))}
    rep = {"coverage": {c: len(v) for c, v in coders.items()},
           "invalid_labels": {c: sum(1 for x in v.values() for s in ("ai", "de") if x[s].startswith("INVALID")) for c, v in coders.items()}}
    ids = sorted(set(key) & set(coders["SONNET"]) & set(coders["HAIKU"]))
    rep["items_scored"] = len(ids)
    rep["none_rates"] = {c: {s: round(sum(coders[c][m][s] == "NONE" for m in ids) / len(ids), 3) for s in ("ai", "de")} for c in coders}
    pairs = [("SONNET", "HAIKU"), ("SONNET", "QWEN_v1"), ("HAIKU", "QWEN_v1")]
    rep["model_model"] = {f"{a}_vs_{b}": {s: agree([(coders[a][m][s], coders[b][m][s]) for m in ids]) for s in ("ai", "de")} for a, b in pairs}
    gold = [m for m in ids if key[m]["source"] == "GOLD"]
    hum1 = {m: {"ai": HUM.get(first[key[m]["record_id"]]["human_ai_family"], first[key[m]["record_id"]]["human_ai_family"]),
                "de": HUM.get(first[key[m]["record_id"]]["human_decision_family"], first[key[m]["record_id"]]["human_decision_family"])} for m in gold}
    rec_ids = [m for m in gold if key[m]["record_id"] in recon]
    humR = {m: {"ai": HUM.get(recon[key[m]["record_id"]]["FINAL_C3"], recon[key[m]["record_id"]]["FINAL_C3"]),
                "de": HUM.get(recon[key[m]["record_id"]]["FINAL_C4"], recon[key[m]["record_id"]]["FINAL_C4"])} for m in rec_ids}
    humB = {m: {"ai": HUM.get(blind[key[m]["record_id"]]["human_ai_family"], blind[key[m]["record_id"]]["human_ai_family"]),
                "de": HUM.get(blind[key[m]["record_id"]]["human_decision_family"], blind[key[m]["record_id"]]["human_decision_family"])}
            for m in gold if key[m]["record_id"] in blind}
    rep["model_vs_human"] = {}
    for c in coders:
        rep["model_vs_human"][c] = {
            "vs_first_coder_50": {s: agree([(coders[c][m][s], hum1[m][s]) for m in gold]) for s in ("ai", "de")},
            "vs_reconciled_20": {s: agree([(coders[c][m][s], humR[m][s]) for m in rec_ids]) for s in ("ai", "de")},
            "vs_blind_coder_20": {s: agree([(coders[c][m][s], humB[m][s]) for m in humB]) for s in ("ai", "de")}}
    rep["human_first_vs_blind_20_reference"] = {s: agree([(hum1[m][s], humB[m][s]) for m in humB]) for s in ("ai", "de")}

    # Differential NONE: among fully mapped qwen items, is the Claude-consensus decision NONE rate different by qwen cell type?
    rc = L.read_csv(os.path.join(L.INP, "ROBUSTNESS_COMPARISON_120.csv"))
    ctype = {(r["ai_family"], r["decision_family"]): ("DEPLETED_CORE" if r["main_mc_direction"] == "DEPLETED" else "ENRICHED_CORE")
             for r in rc if r["full_sensitivity_robust"] == "True"}
    diff = defaultdict(lambda: Counter())
    for m in ids:
        q = qwen[m]
        if q["ai"] == "NONE" or q["de"] == "NONE":
            continue
        t = ctype.get((q["ai"], q["de"]), "OTHER")
        cons_none = coders["SONNET"][m]["de"] == "NONE" and coders["HAIKU"][m]["de"] == "NONE"
        cons_none_ai = coders["SONNET"][m]["ai"] == "NONE" and coders["HAIKU"][m]["ai"] == "NONE"
        diff[t]["n"] += 1; diff[t]["decision_none_both"] += cons_none; diff[t]["ai_none_both"] += cons_none_ai
        cons_same = coders["SONNET"][m]["ai"] == coders["HAIKU"][m]["ai"] == q["ai"] and coders["SONNET"][m]["de"] == coders["HAIKU"][m]["de"] == q["de"]
        diff[t]["cell_confirmed_by_both"] += cons_same
    rep["differential_by_qwen_cell_type"] = {t: dict(v) for t, v in diff.items()}

    # E4: error model qwen -> Claude consensus (only items where Sonnet and Haiku agree), qwen fully mapped items
    e4_ai, e4_de = [], []
    for m in ids:
        q = qwen[m]
        if q["ai"] == "NONE" or q["de"] == "NONE":
            continue
        if coders["SONNET"][m]["ai"] == coders["HAIKU"][m]["ai"]:
            e4_ai.append((q["ai"], coders["SONNET"][m]["ai"]))
        if coders["SONNET"][m]["de"] == coders["HAIKU"][m]["de"]:
            e4_de.append((q["de"], coders["SONNET"][m]["de"]))
    em_ai, da = S7.error_model(e4_ai, L.AI_FAMS)
    em_de, dd = S7.error_model(e4_de, L.DEC_FAMS)
    rep["E4_error_model"] = {"ai": da, "decision": dd, "accuracy_product": round(da["pooled_keep"] * dd["pooled_keep"], 3)}
    base_dep = {k for k, v in ctype.items() if v == "DEPLETED_CORE"}; base_enr = {k for k, v in ctype.items() if v == "ENRICHED_CORE"}
    rng = np.random.default_rng(20261211)
    rep["E4_simulation_claude_consensus_as_truth"] = S7.simulate(L.load_official_raw_pairs(), em_ai, em_de, 0.0, 200, rng, base_dep, base_enr)
    L.write_json(os.path.join(OUTD, "MODEL_CODING_REPORT.json"), rep)
    show = {k: rep[k] for k in ("coverage", "invalid_labels", "items_scored", "none_rates", "model_model", "human_first_vs_blind_20_reference",
                                "differential_by_qwen_cell_type", "E4_error_model")}
    show["model_vs_human"] = {c: {g: {s: (v[s].get("n"), v[s].get("exact"), v[s].get("kappa"), v[s].get("kappa_both_substantive")) for s in v}
                                  for g, v in d.items()} for c, d in rep["model_vs_human"].items()}
    show["E4_sim"] = {k: v for k, v in rep["E4_simulation_claude_consensus_as_truth"].items() if not k.startswith("per_cell")}
    print(json.dumps(show, indent=1, default=str))


if __name__ == "__main__":
    main()
