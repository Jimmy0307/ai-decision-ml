# Manuscript: "Co-occurrence Is Not Flow: A Preregistered Test of the Structural-Hole Premise Between AI and Decision-Making"

This folder holds the English journal manuscript (`en/`) and the Traditional Chinese thesis version (`zh/`). They were produced with the workflow of Google Research's **PaperOrchestra** (Apache-2.0), adapted as described below.

The PDFs are built by GitHub Actions (`.github/workflows/compile-paper.yml`) and downloadable as the `manuscript-pdfs` artifact of each run.

## Build

- **Automatic:** GitHub Actions compiles both versions on every push to `paper/**`.
  - English: pdflatex + bibtex.
  - Chinese: xelatex + Noto CJK TC fonts.
- **Local:** from `paper/en`, run `latexmk -pdf main.tex`. From `paper/zh`, run `latexmk -xelatex thesis_zh.tex`.
- **Checks:**
  - `python scripts/audit_manuscript.py` (or `--zh`) checks that every number is in `raw_materials/experimental_log.md`, that every citation key is in the verified `references.bib`, that every `\ref` resolves, that every figure is used, and that claim-boundary phrases hold.
  - `python scripts/wordcount.py` counts prose words.
- **Figures:** `python scripts/make_figures.py` redraws all 7 figures from the aggregate files in `data/`.

## How PaperOrchestra was used and adapted

| PaperOrchestra stage | Here | Adaptation |
|---|---|---|
| Raw materials (`idea.md`, `experimental_log.md`) | `raw_materials/` | Every number comes from result files in `data/`, with provenance grades. The log is the only number source writers may use. |
| Outline agent | Claude subagent using PaperOrchestra's outline prompt → `outline.json` | Management/IS journal instead of an ML conference (`raw_materials/conference_guidelines.md`). |
| Literature agent (Semantic Scholar search) | **Not run** | A closed library of **32 references, each checked on Crossref** (`references.bib`, `citation_map.json`). Four DOIs recalled from memory failed verification and were excluded. |
| Section-writing agent | 3 parallel Claude subagents using PaperOrchestra's section prompt | Shared label conventions; numbers only from the log. |
| Plotting agent | `scripts/make_figures.py` (matplotlib) | Plots drawn from real data; palette checked with a colour validator. |
| Reviewer (AgentReview) + content-refinement agent | 2 review rounds + 2 refinement rounds | The stock refinement prompt says "never explicitly state a limitation". **This was overridden: limitations are mandatory.** Codex was the planned reviewer, but the host stopped it under memory pressure, so a Claude subagent ran the same AgentReview prompt. |
| LaTeX compile | GitHub Actions | No local LaTeX install. |

## Review history

Files in `review/`:

| Round | Overall (1–10) | Decision | Main issues |
|---|---|---|---|
| 1 (draft v1) | 4 | Reject | Straw-man premise; DEC construct validity; firm null not degree-controlled; T1 understated; Study 1 direction assumed random error; preregistration over-claims; calibration gaps; MLP did not follow |
| 2 (draft v3) | 5 | Reject, encouraged to resubmit | 3 of 8 resolved and 5 partially. Remaining: construct validity untested; RQ2 stronger than T2 could bear; positioning; MLP proportion |
| 3 (draft v5) | 5 | Reject (resubmit as a shorter measurement / negative-result paper) | 15 of 17 plan items resolved. Found that '/06 only' kept 2,318 /04+/06 patents. Binding issue: significance; the co-occurrence-to-hole inference is shown only in this project |

Draft v4 applies the 17 items of `review/REVISION_PLAN_round2.md`. Its main changes:
- the firm level is reported as **unresolved**;
- the premise is grounded in co-word analysis and literature-based discovery;
- construct validity is stated as untested.

v4 has not been re-reviewed.

v5 (2026-11-19) adds **Preregistration 5, the construct-validity checks** the round-2 review asked for:
- G06Q10/06 only: OE 3.04;
- granularity-matched H1a against 826 subgroup families: percentiles of 84–90%;
- both changes together.

All three give HOLE_NOT_SUPPORTED, so the construct verdict is `ROBUST_TO_CONSTRUCT` (Study 2, Table `tab:construct`).

v6 (2026-11-19) applies the 13 items of `review/REVISION_PLAN_round3.md`:
- corrects the '/06 only' description;
- adds amendment C1, a strict /06 check with no /04 code (OE 3.16, still ROBUST over five specifications);
- states that granularity is matched on one side only;
- describes the preregistrations as one confirmatory and four data-informed;
- removes references to the review process;
- uses one cost definition in Study 3, with a coding rule that no longer favours the organisational candidate;
- publishes all Level-3 constants and c = 1;
- relabels the Plan 5 specifications C-a to C-f;
- condenses Section 7 by about 500 words (main text 11,169 words).

## Known open items (stated in the manuscript's Limitations)

- The construct checks are done (Preregistration 5, ROBUST_TO_CONSTRUCT). The domain verdict still applies only to these CPC constructs.
- No null holds firm degree and portfolio fixed together.
- Cell-level tests ignore document clustering. M06-P has no type-I calibration.
- The MLP prototype is simulated. Study 3 is a plan, not a result.

## Folder map

| Path | Contents |
|---|---|
| `raw_materials/` | PaperOrchestra inputs |
| `data/` | Aggregate result files |
| `figures/` | Generated PNGs |
| `en/` | English manuscript (`main.tex` inputs `abstract`, `front`, `studies`, `back`, `appendix`) |
| `zh/` | Chinese thesis version (`thesis_zh.tex` inputs `ch1`–`ch6`, `appendix_zh`), with a translation glossary |
| `review/` | Reviews and revision plans |
| `scripts/` | Figure, audit, word-count and citation-map tools |
