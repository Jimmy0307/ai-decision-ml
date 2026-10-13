# 31 — V1.8.2 Final Status: V1 Human Construct Validation Pre-Human Freeze

**Date:** 2026-10-14.

**This round did not:**
- run any human coding;
- produce any human result, simulated coder answer, or expected/predicted α or κ;
- run a full reanalysis;
- change the Study 1 evidence freeze or the Enterprise model;
- modify `main`, V1.8 or V1.8.1, merge, or tag.

```
REPO=https://github.com/Jimmy0307/ai-decision-ml (PUBLIC at execution time)
BRANCH=research/v1.8.2-v1-human-prefreeze-20261014
BASE_COMMIT=66732a1c1ece404329d3f08eb870dc239398d698
COMMIT=(this commit; recorded in the push report)
MAIN_UNCHANGED=YES (1f2e72f1894c8d4eb7929c39756d7b6af607545b)

STUDY1_EVIDENCE_FREEZE=UNCHANGED
OA2=APPROVED_WITH_SCOPE_LIMIT
OA3=APPROVED
CODER_COUNT=3
GID_MASKING=ENABLED
BLINDING_STATUS=READY_WITH_PUBLIC_HISTORY_LIMITATION
S1_FREEZE=PASS
ANALYZER_STATUS=PASS
LEAKAGE_CHECK=PASS
V1_HUMAN_CONSTRUCT_VALIDATION=READY_TO_DISTRIBUTE
V1_HUMAN_RESULTS=NONE
FULL_REANALYSIS=DEFERRED
ENTERPRISE_MODEL_CHANGED=NO
SUBMISSION_READY=NO
```

## Pre-freeze audit (detail in 27)

```
CODER_FILES=3
ALL_RESPONSE_CELLS_EMPTY=YES
ALL_ATTESTATION_CELLS_EMPTY=YES
GID_VISIBLE_TO_CODERS=NO
RESEARCHER_MAPPING_VISIBLE_TO_CODERS=NO
AI_PILOT_VISIBLE_TO_CODERS=NO
SENSITIVITY_TARGET_MARKERS_VISIBLE=NO
LEAKAGE_FINDINGS=0
PRIMARY_RELIABILITY=KRIPPENDORFF_ALPHA_Q2_3_CODERS
PAIRWISE_KAPPA=SECONDARY
THRESHOLD_PROVENANCE=RESEARCH_CONVENTION
STUDY1_FREEZE_CHANGED=NO
ENTERPRISE_MODEL_CHANGED=NO
HUMAN_VALIDATION_EXECUTED=NO
```

## Orchestrator's independent verification (in addition to `tools/audit_v182.py`)

- **Identity gate:** base `66732a1c`, main `1f2e72f`, V1.8 `d2044161`, worktree clean. The branch was created from the base commit.
- **Coder files, XML level:** scanned every part of the three workbooks, including `docProps`.
  - No G-ID token. The only "G10"–"G16" strings are Excel cell references in column G.
  - No researcher, pilot, sealed or sensitivity terms, and no q, O/E or count values.
  - No defined names, comments, or hidden rows, columns or sheets.
  - All 16 item rows share one style signature, so no item is marked by formatting.
  - Each file has a different item order, and the neutral IDs ITEM-A01…A16 do not follow G order.
- **Sealed map:** a bijective 16-item permutation that does not follow G order. The plaintext map, order log and secret seed exist only in the study-team local store. Their SHA-256 values match the commitments, and none of them is visible to git.
- **S1 manifest:** 23 of 23 entries verified. That is 21 committed files plus the 2 sealed plaintexts by hash.
- **Analyzer:**
  - The correctness test re-run passes. κ matches sklearn within 2.5e-16 and α matches `krippendorff` within 4.4e-16, on in-memory random vectors only.
  - The OA-3 NONE validation passes.
  - On the blank packets the analyzer returns `NO_HUMAN_DATA`, exits 0 and computes nothing.
  - An `--unseal` attempt on blank data also stops at `NO_HUMAN_DATA`. The S3-gated unseal refusal cannot be exercised end to end before human data exist.
- **Manuscript v1.8.2 (32):** changes are confined to the V1 design and status wording (19 changes).
  - Byte-identical to v1.8.1: math spans, 182 headings, the 36 G01–G16 rows and §3.9.2 (Tables 3-4/3-4A).
  - The text contains no ITEM IDs and no result values. The OA-2 sentence is present.
  - DOCX built from it: 25/25 display equations converted to Word OMML, 182 headings, 77 tables, 3 figures, 0 warnings.

## Deviation from the requested layout (deliberate, for blinding)

The repository is **PUBLIC**. The plaintext `ITEM_ID_TO_GID_MAP.json` and the item-order log (seed, input G, neutral ID, coder order) are therefore **not committed**.

- `V1_SEALED/` holds `ITEM_ID_TO_GID_MAP.COMMITMENT.md` and `ITEM_ORDER_LOG.COMMITMENT.md`, which contain the hash and size only.
- The plaintext files are in study-team-only local storage at `C:\NTUST_PAPER\outputs\20261014_V1_8_2_PREFREEZE\SEALED_LOCAL_STUDY_TEAM_ONLY\`.

Committing them would let any repository reader map neutral IDs to G IDs, which would defeat the masking.

## Operational rules carried forward (see 28, 30)

- Coders receive their xlsx **directly from the researcher**, not through GitHub. The v1.8.1 packets (files 19–21 in the V1.8.1 folder) show G IDs and must **not** be distributed.
- Any content change after any coder receives a packet **invalidates S1** and requires a new version.
- Returned human coding sheets must **not** be pushed to the public repository. They stay in local, controlled storage. Only de-identified aggregates may be committed later, after researcher review.
- **Phases:** S1 → S2 (returned sheets frozen) → R (reliability on neutral IDs, key sealed) → A (adjudication) → S3 (adjudication frozen) → K (key unsealed) → C (mapping-sensitivity). The researcher key and the item map must not be used before S3.
- **Inter-rater reliability ≠ agreement with the researcher key.**
  - V1 validates only the G→enterprise-mechanism interpretation. It does not validate 32-cell membership, taxonomy accuracy or network statistics.
  - `V1_PASS_HUMAN_C6` is a continuity label under the earlier 53B protocol, not evidence that the amended Q1–Q5 instrument is identical to 53B.
- **Public-history limitation:** the repository was public before coding, so perfect blinding is not claimed. Making it private later does not remove the earlier exposure. In particular, the public 54A item text is indexed by G ID, so a repository reader could re-identify items. Mitigation: recruit coders with no prior project exposure, and have each sign the 7-item attestation. Exposed coders are flagged as `CODER_STATUS=EXPOSED` and never silently pooled.
