# 42 — V1.8.3 Final Status: V5 Recovery Formal Verification

**Date:** 2026-10-14.

**This round did not:**
- run any reanalysis, null model, pipeline stage or sidecar code;
- start any human coding;
- change any number, G01–G16, the 32-core membership, the taxonomy, any network value, G→M, the Enterprise model or the V1 packet/S1;
- modify `main`, merge or tag.

```
REPO=https://github.com/Jimmy0307/ai-decision-ml
BRANCH=research/v1.8.3-v5-recovery-verification-20261014
BASE_COMMIT=5e170bc3f08132b3819c7b04fea98529747f103f
NEW_COMMIT=(this commit; recorded in the push report)

V5_BASELINE_REPRODUCED=YES
V5_MANIFEST_CHAIN=VERIFIED (201/203; 2 superseded-pack re-saves off the core path)
OFFICIAL_CORE_PROVENANCE=CONFIRMED
REAL_V5_DATA_PACK=RECOVERED
PROTECTED_INPUTS=37/37_CONFIRMED
SIDECAR_CORE=CONFIRMED
SIDECAR_GENERATOR=PROBABLE
PROPAGATION_RULE=RECOVERED_FROM_SIDECAR_POLICY_PENDING_PREDECLARATION
FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION
FULL_REANALYSIS_EXECUTION_STATUS=EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION
FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED
PRIORITY_RATIONALE_REVIEW_REQUESTED=YES
STUDY1_EVIDENCE_FREEZE=UNCHANGED (provenance strengthened)
V1_S1_FREEZE=UNCHANGED_VALID
V1_HUMAN_RESULTS=NONE
FULL_REANALYSIS_EXECUTED=NO
ENTERPRISE_MODEL_CHANGED=NO
SUBMISSION_READY=NO
```

## Outputs of this round

| File | sha256 | Summary |
|---|---|---|
| 35 `V5_MANIFEST_CHAIN_VERIFICATION.md` (+ .csv, raw .json) | `8e64c1dc…f25e` | 203 claims: 201 verified, 2 mismatched in the superseded 081003Z directory. 15/15 links verified. STOP: none |
| 36 `V5_BASELINE_RECOMPUTATION.md` (+ .json) | `4892eab9…0c5f` | 76/76 MATCH: 6,499 / 3,125 / 783 / 2,180 / 120 / 47 (34) / 32 = 16+16 / G01–G16 |
| 37 `PROTECTED_INPUT_RECOVERY.md` (+ .csv) | `3f4f9d10…1d0f` | 37/37 CONFIRMED (36 whole-file + 1 355-byte prefix); sidecar core CONFIRMED |
| 38 `FULL_REANALYSIS_FEASIBILITY.md` | `88969527…41e1` | Execution status EXECUTABLE_PENDING…; propagation rule recovered (50/50, −18) |
| 39 `STUDY1_FREEZE_PROVENANCE_ADDENDUM_v1_8_3.md` | `ced2ea705941741305a860d7df414dcda117ac94332804271a8b460dd97c354b` | Addendum to 17 (17 not modified): 11 items old → new, with the triplet and its rationale |
| 40 `STUDY1_FREEZE_HASHES_v1_8_3.csv` | `89de71e5a13a20773432964dfb7f5e72d5aa4ac0124f9c9d7873640afbc295a8` | 98 rows, same columns as 18; 0 mismatches. See breakdown below |
| 41 `MERGED_MASTER_THESIS_v1_8_3_V5_PROVENANCE_CANDIDATE.md` | `0da8cec1521dbeff900ffa1fa9a1de0a31b0cdfa34b82c03531eba2111d7f740` | From v1.8.2 (`2d493edc…f159`, asserted); 34 replacements on 27 v1.8.2 lines. All hard checks pass; see below |
| 41 `PATCH_LOG_v1_8_3.md` / 41b `V182_TO_V183_SEGMENT_DIFF.md` | `e260ea80…f844` / `25372e2d…49e8` | Old → new for every patch, numeric delta, segment diff |
| `tools/R/` | patch `90f1baa4…`, verify `7138d724…`, log `a425ee0c…`, hashes `20c9bf74…` | Stdlib, `python -I`; outputs `patches_v183.json`, `verify_out_v183.json`, `hashes_summary_v183.json` |

**40 breakdown (98 rows):**
- 43 rows carried from 18. All re-verified at their current paths, with the W and R14-docx paths moved per 33 §2.
- 4 of the 6 NOT_RECOVERED rows from 18 were replaced:
  - the official core, CONFIRMED;
  - the 12/37 protected-input row, which became 12 CONFIRMED rows plus 1 log-prefix row;
  - the sidecar core, CONFIRMED;
  - the sidecar generator, PROBABLE. The policy (PROBABLE) and the correction map (CONFIRMED) were also added.
- 2 rows stay NOT_RECOVERED and are outside this scope: `r14/04_G01_G16_FROZEN.csv` and the R14 canonical docx as a named file.
- 18 V5 chain anchors were added.
- 17 V1.8.3 evidence rows were added.
- Status counts: CONFIRMED 34, PROBABLE 2, NOT_RECOVERED 2, PRESENT 46, PRESENT_OUTSIDE_GIT 14.

**41 changes and checks:**
- **What changed:**
  - the status line L5;
  - every "12/37 missing" statement (×5 removed);
  - all 15 "以目前（的）來源集無法執行" phrases, plus the L412 diagram phrase;
  - 4 `NOT_EXECUTABLE…` → `EXECUTABLE_PENDING…`;
  - the HUMAN_AUDIT log wording;
  - the official core, Data Pack, sidecar and rule provenance;
  - E12, E39 (a)–(c), E40, E44 and E48;
  - the Appendix D rows for 35–41.
- **Hard checks, all PASS:**
  - math, headings (182), G rows (36), G tokens, §3.9.2, §3.9.3, §3.9.4, §3.9.5, §3.12, §4.4 and §4.7 are byte-identical;
  - no result-like tokens were added;
  - numeric delta: added numbers are only file IDs, SHA-256, 37/13/74/355 and section refs; removed numbers are only `12` ×5;
  - `NOT_REQUIRED` count is 0.

## Researcher decisions needed

1. **Propagation rule (E48):** either adopt the recovered V9 rule (`LOCAL_HUMAN_CORRECTION_POLICY.md` `33d4d44c…`, which re-derives 50/50 and −18) or declare another one. Then predeclare and hash-commit it before any rerun. The manuscript keeps `[AUTHOR TO CONFIRM]` in §3.7.4 until then.
2. **Priority rationale review (`PRIORITY_RATIONALE_REVIEW_REQUESTED`):** reason 1 for `NOT_RECOMMENDED` (missing inputs) has lapsed, and reasons 2–5 still hold. Confirm or revise the priority before V1. The status stays `NOT_RECOMMENDED` until you decide.
3. **If a rerun is chosen:** approve it as V9 requires. Then authorise a new dated directory for path-patched copies of the stage 10–13 scripts, and require byte-for-byte reproduction of the 13 pinned outputs first. V5 must never be written.
4. **Optional legacy wording:** you may adopt "protected state verified as prefix of append-only log" in place of V9's historical `LEGACY_AUDIT_LOG_INTEGRITY=UNVERIFIED`. The manuscript already marks V9's label as historical.
5. **Out of scope, still NOT_RECOVERED:** `r14/04_G01_G16_FROZEN.csv` (prefix `ace53a78…`) and the R14 canonical docx as a named file. Decide whether to search further or to record them as permanently unrecoverable.
