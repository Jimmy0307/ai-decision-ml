"""Generate docs/CODEBOOK_v2_DRAFT.md: verbatim ratified definitions + proposed decision rules."""
import os, json
import ra_lib as L

src = json.load(open(os.path.join(L.INP, "FAMILY_DEFINITIONS_22.json"), encoding="utf-8"))
fam = src["families"]
conf = json.load(open(os.path.join(L.OUT, "01_taxonomy", "TAXONOMY_EVIDENCE_REPORT.json"), encoding="utf-8"))

RULES = """## Part B — Proposed decision rules (NEW; require researcher/advisor ratification BEFORE coder training)

These rules do not change any family definition. Each one targets a failure mode observed in the frozen
audit materials (`outputs/01_taxonomy/PAIRWISE_CONFUSION_ALL_SOURCES.csv`). Once ratified they are frozen:
they must not be edited after any reliability item has been coded.

**R0 — Coding unit and evidence quote (all families).**
Code only a function that the evidence span itself states. For every AI-family and Decision-family code, copy
the exact words that express that function into `C3_ai_quote` / `C4_decision_quote`. If no words can be quoted,
the code is `NONE`. Do not use the document title, the surrounding paper or background knowledge.

**R1 — NONE vs AMBIGUOUS (largest single source of disagreement).**
`NONE`: the span names AI (or a decision context) as a topic but states no function (for example a reference
fragment, a heading, a list of technologies, or "AI is transforming management").
`AMBIGUOUS`: a function is stated, but after applying R2–R6 two families still fit equally well. List both in `notes`.

**R2 — No lexical self-pairing.**
The same word or phrase must not be the only evidence for both sides. "forecasting" alone cannot be both
PREDICTION_RISK_ESTIMATION (AI) and PREDICTION_DIAGNOSIS (Decision). The decision side needs its own decision
object: what is being diagnosed, forecast or decided, and by or for whom. Otherwise the decision side is `NONE`.
(184 pair-eligible records, 33% of the largest enriched cell, were paired this way; see step 4.)

**R3 — AI side: the most specific operational function wins.**
Code what the AI system does: estimate, recommend, generate, retrieve, perceive, explain, evaluate, coordinate.
HUMAN_AUGMENTATION and COORDINATION_EXECUTION apply only when augmentation or coordination/execution is itself
the stated function. If the span says "AI supports managers by predicting demand", code PREDICTION_RISK_ESTIMATION.
(Targets the observed COORDINATION_EXECUTION↔PREDICTION_RISK_ESTIMATION, HUMAN_AUGMENTATION↔PREDICTION_RISK_ESTIMATION
and EVALUATION_ASSESSMENT↔PREDICTION_RISK_ESTIMATION confusions.)

**R4 — Decision side: residual family last.**
GENERAL_DECISION_PROCESS is allowed only when the span concerns decision making as a whole and none of the other
11 families applies (this follows the ratified exclusion note). "Data-driven decision making" plus a forecast of
a state is PREDICTION_DIAGNOSIS, not GENERAL_DECISION_PROCESS. (Targets GENERAL_DECISION_PROCESS↔PREDICTION_DIAGNOSIS.)

**R5 — PREDICTION_DIAGNOSIS vs RISK_ASSESSMENT.**
If the decision object is a risk, hazard, vulnerability or safety exposure that is assessed or prioritised,
code RISK_ASSESSMENT. If it is the likely state or outcome itself (diagnosis, demand, failure time), code
PREDICTION_DIAGNOSIS. A prediction of risk produced by the AI is coded on the AI side (ratified exclusion note).

**R6 — GOVERNANCE_OVERSIGHT needs a mechanism.**
GOVERNANCE_OVERSIGHT requires an explicit policy, authority, control, compliance or review mechanism. A span that
only mentions "ethics", "responsible AI" or "trust" with no mechanism is `NONE` on the decision side.
(Targets the AMBIGUOUS↔GOVERNANCE_OVERSIGHT confusion, the most frequent decision-side disagreement.)

**R7 — No external assistance.**
Coders must not consult any AI system, search engine or the other coder while coding. In the V9 audit the first
coder consulted external AI on boundary cases; that is not permitted here.
"""


def main():
    lines = ["# CODEBOOK v2 DRAFT — AI × Decision functional families",
             "",
             "> **Status: DRAFT for ratification.** Part A reproduces the ratified V5 definitions verbatim; Part B proposes",
             "> new decision rules. Nothing here has been used to code data. The source of Part A is",
             f"> `{src['source_file']}` (SHA-256 `{src['source_sha256']}`).",
             "",
             "## Part A — Ratified family definitions (verbatim, unchanged)",
             ""]
    for side, fams in (("AI side (10)", L.AI_FAMS), ("Decision side (12)", L.DEC_FAMS)):
        lines += [f"### {side}", "", "| ID | Name | Ratified definition | Ratified exclusion / boundary notes |", "|---|---|---|---|"]
        for f in fams:
            o = fam[f]
            ex = "; ".join(o.get("exclusions") or []) or "—"
            gen = "; ".join(o.get("generic_not_sufficient") or [])
            if gen:
                ex += f" (generic terms not sufficient: {gen})"
            res = " **[residual family]**" if o.get("residual") else ""
            lines.append(f"| `{f}` | {o.get('name_en', '')}{res} | {o['functional_definition']} | {ex} |")
        lines.append("")
    lines += ["Allowed non-family values: `NONE` (no function stated) and `AMBIGUOUS` (function stated, two families tie after the rules).", ""]
    lines += [RULES, "", "## Part C — Observed confusions motivating Part B (frozen audit materials, all sources pooled)", "",
              "| Side | Pair | Disagreements |", "|---|---|---:|"]
    for side, rows in conf["top_confusions"].items():
        for a, b, n in rows:
            lines.append(f"| {side} | {a} ↔ {b} | {n} |")
    lines += ["", "Sources: first vs blind second coder (n=20), model vs first coder (n=50), model pass 1 vs pass 2 (n=143 sides).",
              "These samples are small and targeted (Robust-A); they motivate rules but cannot validate them."]
    out = os.path.join(os.path.dirname(L.OUT), "docs", "CODEBOOK_v2_DRAFT.md")
    open(out, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print("written", out)


if __name__ == "__main__":
    main()
