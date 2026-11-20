# Venue guidelines (replacing PaperOrchestra's CVPR/ICLR guidelines)

**Target:** a management or information-systems journal (full research paper), for example a journal in information systems, strategy or technology management. The format is journal-style, not a conference paper.

## Length and format

- Main text: 9,000–12,000 words, excluding references and appendices.
- Abstract: at most 200 words, unstructured.
- Single column, 12 pt, author–year citations (natbib `\citet` / `\citep`), APA-like reference list.
- Tables use booktabs. Every number must come from `experimental_log.md`.
- Figures: all files listed in `figures/` must be used and referenced, except the per-language skips in `scripts/audit_manuscript.py` (`FIG_SKIP`): the English version uses `fig_research_design_en.png` and not the MLP figure; the Chinese thesis uses `fig_research_design.png`.

## Mandatory sections

1. Introduction (motivation, the structural-hole premise, what we do, findings, contributions).
2. Theoretical Background:
   - 2.1 Structural holes and their measurement;
   - 2.2 AI and decision-making as knowledge domains;
   - 2.3 Why co-occurrence is not flow.
3. Research Design and Preregistration (overview of the studies, the preregistration log, claim boundaries).
4. Study 1: Literature Evidence (V5–V11.1).
5. Study 2: Patent Evidence (aggregate test; V9 battery on the CPC matrix; full replication suite; portfolio-preserving firm null; co-occurrence vs flow across field pairs, Plans 7–8).
5b. Systematic review of the co-occurrence → hole/gap inference (preregistered; descriptive).
6. Integrative Discussion (what the three data lines jointly show; measurement lessons; what the negative result does not settle; **Implications and future research**, at most 150 words).
7. *(Removed from the journal version; see the decision note below.)*
8. Limitations — **mandatory and explicit.** This overrides any instruction to avoid stating limitations.
9. Conclusion.
10. References.
11. Appendix:
    - A, preregistration and amendment log;
    - B, sensitivity tables;
    - C, systematic review protocol, flow and reliability.

**Decision note (2026-11-19).** The multi-level programming (MLP) model, its simulated illustration, the Study 3 plan and the MLP appendices move to a separate paper. The English journal version (`paper/en/`) replaces them with a short Implications and future research subsection in the discussion, and its research questions are RQ1 (domain-level hole), RQ2 (firm-level hole beyond portfolio) and RQ3 (how often, and when, gap inference from co-occurrence agrees with flow). The Chinese thesis (`paper/zh/`) keeps the MLP chapter, its appendices and the RQ3/RQ4 framing.

## Style

- Objective, precise, non-promotional. Report negative results plainly.
- State provenance grades (DIRECT / HISTORICAL / USER_REPORTED) where they matter.
- Never describe a depleted cell as a "gap" or a "structural hole".
- Use only the citation keys in `citation_map.json`.
