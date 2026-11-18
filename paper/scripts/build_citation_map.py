"""Build citation_map.json (PaperOrchestra's citation library) from the verified references.bib.

Each entry adds a short role note describing what the source is cited for in this paper. Role notes are
paraphrased from the verified bibliography records; they are not quotations or abstracts.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]

ROLES = {
    "granovetter1973strength": "Weak ties can carry information across groups; strong ties are associated with overlap within communities. Theoretical background only.",
    "freeman1977set": "Betweenness centrality: the share of shortest paths between other node pairs that pass through a node. Not a sufficient test of Burt brokerage.",
    "gould1989structures": "Five brokerage roles defined on directed open two-paths (s->v->t with no direct s->t tie), combined with group membership.",
    "burt1992structural": "Structural holes: non-redundant contacts in an ego network give information and control benefits. Defines network constraint.",
    "newman2001scientific": "Co-authorship collaboration networks built from article-author two-mode data and projected to one mode. In this paper, co-authorship is not treated as direct evidence of knowledge flow.",
    "burt2004structural": "Managers who span structural holes have better ideas; brokerage needs real ties and observed outcomes.",
    "opsahl2013triadic": "One-mode projection of two-mode networks creates artificial closure; clustering must be redefined for two-mode data.",
    "jasny2015two": "Two-mode brokerage chains with group heterogeneity, as an alternative to computing brokerage after projection.",
    "everett2020unpacking": "Burt's constraint is driven by degree and dyadic ties; it is not a simple 0-1 index of exclusive brokerage.",
    "saglietto2020research": "Review of measurement issues in structural-hole research: different measures suit different data types and cannot be substituted arbitrarily.",
    "zador2022weighted": "Weighted and normalised Gould-Fernandez brokerage measure that avoids information loss from dichotomisation.",
    "johnson2026reassessing": "Network constraint operationalises mainly dyadic constructs (alternatives, partner diversity, concentration) rather than broader network structure. A reinterpretation framework for structural-hole findings, not a refutation of the theory.",
    "dempe2002foundations": "Foundations of bilevel programming: hierarchy, non-unique follower responses, optimistic and pessimistic formulations.",
    "colson2007overview": "Overview of bilevel optimisation formulations and solution approaches, including MPEC.",
    "fortunyamat1981representation": "KKT/complementarity reformulation of two-level programming problems.",
    "jeroslow1985polynomial": "Complexity of multilevel (competitive) programming: existence does not imply tractability.",
    "lee2001fuzzy": "Interactive fuzzy approaches to multi-level decision making.",
    "cheng2019fuzzy": "Updated soft-computing methods for fuzzy and multi-level decision making.",
    "nash1951noncooperative": "Existence of mixed-strategy equilibrium in finite non-cooperative games; a boundary reference only, not a coupled generalised equilibrium.",
    "jaffe1993geographic": "Patent citations as evidence of knowledge spillovers (flows), with a matched-control design.",
    "alcacer2006patent": "Examiner-added citations make up a large share of patent citations and affect their use as measures of knowledge flow; inventor or applicant citations should be distinguished.",
    "benjamini1995controlling": "False discovery rate control (BH procedure) for multiple testing.",
    "cohen1960coefficient": "Cohen's kappa: chance-corrected agreement for nominal scales.",
    "nosek2018preregistration": "Preregistration separates confirmatory from exploratory research by fixing the analysis plan before observing outcomes.",
    "granovetter1985economic": "Economic action is embedded in concrete ongoing social relations. Background for locating integration problems inside organisations.",
    "shrestha2019organizational": "Organisational decision-making structures that combine humans and AI (full delegation to AI, sequential human-AI or AI-human decision-making, aggregated decision-making), and the decision-task conditions under which each fits.",
    "raisch2021artificial": "Automation versus augmentation of managerial tasks with AI as a paradox; argues the two are interdependent across time and space and should be managed together.",
    "jarrahi2018artificial": "Human-AI symbiosis in organisational decision making: AI is suited to complexity, while humans contribute where decisions involve uncertainty and equivocality.",
    "berente2021managing": "Managing AI as the frontier of computing; the facets of autonomy, learning and inscrutability raise distinctive management challenges for information-systems research.",
    "uspto2026patentsview": "USPTO PatentsView granted-patent tables (pvgpatdis): patents, current CPC classifications, US patent citations and disambiguated assignees.",
}


def braced(text, start):
    """Return (content, end) for the brace group whose '{' is at text[start-1]."""
    depth, j = 1, start
    while depth:
        depth += {"{": 1, "}": -1}.get(text[j], 0)
        j += 1
    return text[start:j - 1], j


def parse_bib(text):
    entries, i = {}, 0
    head = re.compile(r"@(\w+)\{([^,]+),")
    while (m := head.search(text, i)):
        body, i = braced(text, m.end())
        fields, k = {}, 0
        for fm in re.finditer(r"(\w+)\s*=\s*\{", body):
            if fm.start() < k:
                continue
            fields[fm.group(1).lower()], k = braced(body, fm.end())
        entries[m.group(2).strip()] = (m.group(1).lower(), fields)
    return entries


def main():
    entries = parse_bib((HERE / "references.bib").read_text(encoding="utf-8"))
    assert set(entries) == set(ROLES), (set(entries) ^ set(ROLES))
    out = {}
    for key, (typ, f) in entries.items():
        out[key] = {"type": typ, "title": f.get("title"), "authors": f.get("author"), "year": f.get("year"),
                    "venue": f.get("journal") or f.get("publisher") or f.get("howpublished"),
                    "doi": f.get("doi"), "abstract_or_role": ROLES[key]}
    (HERE / "citation_map.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(out), "entries;", sum(bool(v["doi"]) for v in out.values()), "with DOI")


if __name__ == "__main__":
    main()
