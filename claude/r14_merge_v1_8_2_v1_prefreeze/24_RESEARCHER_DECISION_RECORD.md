# 24 — Researcher Decision Record (V1 human construct validation, v1.8.2 pre-human freeze)

**Date:** 2026-10-14.

**Source of decisions:** the user (researcher / PI), relayed by the orchestrator. These decisions are authoritative and newer than 53B (2026-10-10) and v1.8.1 (files 19–21). They supersede the v1.8.1 open items OA-2 and OA-3, and the v1.8.1 choice to show G IDs.

**Scope:** these decisions change no Study 1 freeze, 32-core, 47-cell, G01–G16 or G→M researcher assignment, and no taxonomy, enterprise model, solver or schema.

| ID | Decision | Value |
|---|---|---|
| D-1 (OA-2) | Derived `primary_53B` / `status_53B` and `V1_PASS_HUMAN_C6` | **APPROVED_WITH_SCOPE_LIMIT.** They may be computed as SECONDARY CONTINUITY METRICS only. The primary construct-validity analysis is Q2 (flat category) with Krippendorff's α (nominal) across 3 coders. Results are reported in two separate sections: **A. CURRENT_INSTRUMENT_RELIABILITY** and **B. 53B_CONTINUITY_RELIABILITY**. The two are never collapsed. |
| D-1 wording | Required manuscript wording (verbatim) | "V1_PASS_HUMAN_C6 is a continuity label under the earlier 53B protocol, not evidence that the amended Q1–Q5 instrument is identical to 53B." |
| D-2 (OA-3) | Meaning of `NONE` | **APPROVED.** NONE means an identifiable enterprise decision interface exists, but none of M1, M2, M3, M4, LONGITUDINAL or DATA_GATED adequately expresses it. It requires Q1 = YES, and Q5 must state the enterprise decision that is not captured. Derived values: `primary_53B = OTHER`, `status_53B = static`, `new_construct_required = YES`. NONE is not used for insufficient evidence or a tie between two categories (use AMBIGUOUS, or Q1 = UNCERTAIN), nor when there is no distinct interface (use EVIDENCE_ONLY). The analyzer treats NONE with Q1 ≠ YES, or NONE with an empty Q5, as a validation error. |
| D-3 | Number of coders | `N_HUMAN_CODERS=3`: CODER_1, CODER_2 and CODER_3, all independent humans. No AI coder. |
| D-4 | Recruitment preference (not mandatory) | (1) enterprise IT / AI-governance practitioner; (2) IS / management researcher; (3) AI / decision-science practitioner. All must meet the blinding criteria (28). |
| D-5 | Primary reliability | Krippendorff's α (nominal) on Q2, all 16 items, 3 coders. Reported with: α, 95% bootstrap CI, raw agreement and category frequencies. |
| D-6 | Secondary reliability | Pairwise Cohen's κ (1v2, 1v3, 2v3), each with a bootstrap CI. Q1: α plus pairwise κ, with no pass/fail. Q3: descriptive only, never a weight. Q4: set-based Jaccard only. |
| D-7 | Classification | α ≥ .800 → RELIABLE; .667 ≤ α < .800 → TENTATIVE; α < .667 → UNRESOLVED/NOT_ACCEPTABLE; CI lower bound < .667 → IMPRECISE. Labelled `RESEARCH_CONVENTION`. No Landis & Koch labels. No claim that these thresholds are universal. |
| D-8 | G IDs | **MASKED** in all coder-facing packets. Coders see neutral IDs ITEM-A01…ITEM-A16, assigned by a frozen, seeded random permutation; the seed is secret and held in SEALED_LOCAL. The ITEM-ID → G-ID map and the order log are kept only in SEALED_LOCAL; OUT holds hash commitments only. This replaces the v1.8.1 decision to show G IDs. |
| D-9 | Coder-facing content | Allowed: neutral item ID; AI family and its definition; decision family and its definition; neutral depletion statement; neutral evidence description; category definitions; Q1–Q5; attestation. Excluded: researcher mapping, AI-pilot mapping, q-values or observed/expected counts, G ID, sensitivity marker, Study 1 interpretation, the 132 interpretation, previous coder results. |
| D-10 | Attestation (7 items, blank) | Each coder states: (1) not read the public repository; (2) not read the thesis or manuscript; (3) not seen the researcher's G→M assignments; (4) not seen AI-pilot output; (5) did not consult another coder; (6) did not use ChatGPT, Claude, Gemini, Copilot or any other AI to answer; (7) coded independently. Any exposure → `CODER_STATUS=EXPOSED`. Exposed coders are never silently pooled: the analyzer flags them, excludes them from the primary scope, and reports both scopes. |
| D-11 | Item order | Each coder file uses a different deterministic seeded order. The original order is not exposed. |
| D-12 | M1 label | "Authority & Accountability (授權與問責; = Governance & Decision Rights / authority-to-act)". The operational definition is unchanged (53B §3 M1). |
| D-13 | Phases | **S1** packet freeze → **S2** three returned sheets frozen → **R** reliability (key sealed) → **A** adjudication → **S3** adjudication frozen → **K** researcher key unsealed → **C** mapping-sensitivity classification. The primary question is inter-rater agreement, not agreement with the researcher key. |
| D-13a | Item map at phase R (orchestrator-delegated decision, recorded here) | **Not used at R.** Primary α and every R statistic are computed on neutral IDs, following "Do not unseal merely to compute reliability". The item map is accepted only after S3, and only if its hash verifies. It is used only for the G04/G10/G11 sensitivity analysis and for indexing the key at K. |
| D-14 | Bounded claim | V1 validates only the G → enterprise-mechanism interpretation. It does not validate 32-cell membership, the taxonomy or the network statistics. |
| D-15 | Repository status | The repository (`Jimmy0307/ai-decision-ml`) is PUBLIC. Sealed plaintext is kept in SEALED_LOCAL only. Coder packets are sent directly, not via GitHub. Returned sheets are never pushed (30). |

Status: these decisions are implemented in 25, 26, 29 and 30, in `tools/`, and in `V1_SEALED/`. They are verified in 27.
