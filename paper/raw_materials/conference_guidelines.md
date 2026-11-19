# Venue guidelines (replacing PaperOrchestra's CVPR/ICLR guidelines)

**Target:** a management or information-systems journal (full research paper), for example a journal in information systems, strategy or technology management. The format is journal-style, not a conference paper.

## Length and format

- Main text: 9,000–12,000 words, excluding references and appendices.
- Abstract: at most 200 words, unstructured.
- Single column, 12 pt, author–year citations (natbib `\citet` / `\citep`), APA-like reference list.
- Tables use booktabs. Every number must come from `experimental_log.md`.
- Figures: all files listed in `figures/` must be used and referenced.

## Mandatory sections

1. Introduction (motivation, the structural-hole premise, what we do, findings, contributions).
2. Theoretical Background:
   - 2.1 Structural holes and their measurement;
   - 2.2 AI and decision-making as knowledge domains;
   - 2.3 Why co-occurrence is not flow.
3. Research Design and Preregistration (overview of the three studies, the preregistration log, claim boundaries).
4. Study 1: Literature Evidence (V5–V11.1).
5. Study 2: Patent Evidence (aggregate test; V9 battery on the CPC matrix; full replication suite; portfolio-preserving firm null).
5b. Systematic review of the co-occurrence → hole/gap inference (preregistered; descriptive).
6. Integrative Discussion (what the three data lines jointly show; measurement lessons).
7. A Multi-Level Programming Agenda (formal model; simulated illustration; Study 3 preregistered plan).
8. Limitations — **mandatory and explicit.** This overrides any instruction to avoid stating limitations.
9. Conclusion.
10. References.
11. Appendix:
    - A, preregistration and amendment log;
    - B, sensitivity tables;
    - C, MLP constraint details.

## Style

- Objective, precise, non-promotional. Report negative results plainly.
- State provenance grades (DIRECT / HISTORICAL / USER_REPORTED) where they matter.
- Never describe a depleted cell as a "gap" or a "structural hole".
- Use only the citation keys in `citation_map.json`.
