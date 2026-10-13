# 03 — Human Audit Reproduction (Phase 3: 50/20/19 counts, Phase 4: C1–C5 Cohen's kappa)

Run: V1.8 SOURCE-VERIFIED EVIDENCE CLOSURE — sub-agent B. Date 2026-10-14.
Package: `W\02_V9_HUMAN_VALIDATION\20260929_V9_HUMAN_VALIDATION\` (treated as untrusted data; no package code executed).

## Method

- Independent code, written fresh. Package scripts (`analyze_human_validation.py`, `finalize_blind_audit_20.py`, `codebook.py`, `converge_human_audit_50.py`, `human_reconciliation_server.py`, `build_codebook_gate.py`) were read as text only, to learn field names, the enum/codebook, alias canonicalization and the kappa variant used.
- Helper scripts (run with `python -I`):
  - `C:\Users\user\AppData\Local\Temp\claude\C--NTUST-PAPER\b2185478-fbc8-4bee-8105-bb5557dd964b\scratchpad\v18\B\recompute_human_audit.py` produces `...\v18\B\result.json`
  - `C:\Users\user\AppData\Local\Temp\claude\C--NTUST-PAPER\b2185478-fbc8-4bee-8105-bb5557dd964b\scratchpad\v18\B\extra_checks.py` checks timestamps, the unanimous row, the blank-queue hash reconstruction, confidence matches and Wilson CIs.
- I computed my own numbers first. Only after that did I read the summary files (`HUMAN_RELIABILITY_FINAL.*`, `HUMAN_RELIABILITY_20.*`) and compare against them.

### Definition of "complete"

This matches the package's `completed()` / `row_is_complete()` rules, which I re-implemented. A row is complete only if all of these hold:
1. `review_status == "COMPLETE"`.
2. These fields are non-empty: `human_evidence_valid`, `human_relation_type`, `human_ai_family`, `human_decision_family`, `human_include`, `coder_confidence` and `coder_id`. `coder_notes` is optional.
3. Each value is inside the frozen codebook enum:
   - C1 is one of {VALID, INVALID, UNCERTAIN}.
   - C2 is one of {SUPPORTS, GOVERNS, TRANSFORMS, CONSTRAINS, INFORMS, ENABLES, ASSOCIATED_WITH, AMBIGUOUS, NOT_APPLICABLE}.
   - C3 is one of the 10 canonical V5 AI IDs, UNMAPPED or AMBIGUOUS.
   - C4 is one of the 12 canonical V5 Decision IDs, UNMAPPED or AMBIGUOUS.
   - C5 is one of {INCLUDE, EXCLUDE, UNCERTAIN}.
   - Confidence is one of {HIGH, MEDIUM, LOW}.

   The canonical ID lists come from `MODEL_FAMILY_CODEBOOK_CROSSWALK.csv`, SHA-256 `E589864E…FB31D`. This equals the hash pinned in `codebook.py`.

For a reconciled row to count as complete:
- FINAL_C1..C5 must all be in the enums above.
- `RESOLUTION_REASON` must be non-empty.
- There must be a matching `COMPLETE` event in `HUMAN_RECONCILIATION_EVENTS.jsonl` with identical FINAL values and an identical event hash.
- FIRST_/BLIND_ values must equal the frozen coder rows.

### Alias canonicalization

The package maps four UI display labels to canonical V5 IDs:
- EVALUATION_AUDIT → EVALUATION_ASSESSMENT
- RETRIEVAL_INTEGRATION → RETRIEVAL_SYNTHESIS
- INFORMATION_INTEGRATION → INFORMATION_SYNTHESIS
- RESOURCE_ALLOCATION_PLANNING → ALLOCATION_PLANNING

I applied the same mapping. Neither coder file contains any alias label, because both already store canonical IDs. So the raw-label and canonical-label results are identical for every dimension.

## Source hashes (SHA-256, computed now)

| File | SHA-256 |
|---|---|
| FIRST_CODER_50_FINAL_FROZEN.csv | DD332DD8CFECF7DDE9A29D32BCA654B7C04C49F499C3E6213CD4D9A2ED157400 |
| FIRST_CODER_50_FROZEN.csv | DD332DD8CFECF7DDE9A29D32BCA654B7C04C49F499C3E6213CD4D9A2ED157400 (byte-identical to FINAL_FROZEN) |
| HUMAN_VALIDATION_400_WORKING.csv | C4C7F4FE0B2102D9B18548F84721AA5E6BCAE83D6A54908C56F0B816D7235315 |
| FIRST_CODER_50_MANIFEST.csv | DE1C1D5CD1E83473E71BFAF75745BF6D3A3E35E363B6DF7D6A25509B2748522E |
| HUMAN_AUDIT_APPEND_ONLY_LOG.csv | 151CF3D0CB6FBA4930FBEFBDE290396872E90FED4CBAE9C6999FD29C5127A817 (= LEGACY_AUDIT_LOG_FORENSIC_SNAPSHOT.csv) |
| HUMAN_AUDIT_EPOCH2_LOG.csv | 9EF14DC0AEA628CD207CD590BD89AFA5D6614D5AC81E1381EFD9C8923B617AF5 |
| HUMAN_AUDIT_EPOCH2_GENESIS.md | E5DB33E886EF784FB112FAFB6D38EB1C2BC5FC3BAFD533786232E9DD5B43919D |
| SECOND_CODER_BLIND_20.csv | 6AFC8D7A2C2BB5F1E507F50B2F6664FE4D80216CF7F2FCB36C4E94B813BFF797 |
| BLIND_REPEAT_20_FINAL_FROZEN.csv | 6AFC8D7A2C2BB5F1E507F50B2F6664FE4D80216CF7F2FCB36C4E94B813BFF797 (byte-identical to SECOND_CODER_BLIND_20) |
| SECOND_CODER_BLIND_20_AUDIT_LOG.csv | 1FB0905A9E02BA5D0843046FC922E9343F9157DCCAF378DD4AC99F4009454E72 |
| SECOND_CODER_BLIND_20_MANIFEST.csv | CE9D4C4EEDD422FC25953A4280C2DA9CA7DF94006DE9CEC1FD67388366D8E5E0 |
| SECOND_CODER_BLIND_20_ALLOCATION.csv | ED0218CC589F8BFA293796E2C9CFAA6AA041539C4CB846876E9C749A61223E80 |
| SECOND_CODER_120_WORKING.csv | A0860BA7C9C445174829174FD3D37F636E10447BCE03B3D77FFDFBA4CEBDEC40 |
| SECOND_CODER_BUG_PRESTATE.csv | C55FF2C8DB43E998B5EB803BE7E9B44D469F5DB4C864C0ED1A78C26D9D06ECAC |
| HUMAN_DISAGREEMENT_QUEUE_20.csv | 58D02370AAB70BAFC2DE7F644DAD904AAB0BFD862BF47DBB9B11F6E645DD682F |
| DISAGREEMENT_QUEUE.csv (legacy 120 design) | DE973C10D5A7251D5C517EB66415937E54D2C3D8A2F0B65C86E9C59FDB89732D |
| HUMAN_RECONCILED_20.csv | 4B7CEAC2C8C8BF2912EA542D88A1B887A42ED450AA248DCE371525C25BB5BDA0 |
| HUMAN_RECONCILIATION_EVENTS.jsonl | 9270ACCC7657006C32D3965A01FF3DAE95B0EC25AB5BF5F52D2B1DCB6AF2CC2D |
| ADJUDICATION_LOG.csv (legacy 120 design) | 2A7449EA564F504516BF638CFFDDF03FB83D8BB4A3ED51C0108E52AC0DFB541B |
| MODEL_FAMILY_CODEBOOK_CROSSWALK.csv | E589864E8ABA9DECF5DC8ABFDF45F6310E5CB4F22A443B4F285449DF892FB31D |
| HUMAN_RELIABILITY_FINAL.csv | EF7E554496866DED471498DEAFDBF3B6D24E617CF884D24DBDEDC4749533D2DE |
| HUMAN_RELIABILITY_20.csv | 239AABF1F8BD9CBEDC842015061C5A32FBE2178052E0C2C2BBD603E413525A02 |

### Sidecar verification

| Sidecar | Target | Result |
|---|---|---|
| FIRST_CODER_50_FINAL_FROZEN.sha256 | FIRST_CODER_50_FINAL_FROZEN.csv | MATCH |
| BLIND_REPEAT_20_FINAL_FROZEN.sha256 | BLIND_REPEAT_20_FINAL_FROZEN.csv | MATCH |
| HUMAN_AUDIT_EPOCH2_GENESIS.sha256 | HUMAN_AUDIT_EPOCH2_GENESIS.md | MATCH |
| HUMAN_AUDIT_EPOCH2_LOG.sha256 | HUMAN_AUDIT_EPOCH2_LOG.csv | MATCH |
| HUMAN_RECONCILIATION_FINAL.sha256 | HUMAN_RECONCILED_20.csv | MATCH |
| LEGACY_AUDIT_LOG_FORENSIC_SNAPSHOT.sha256 | snapshot = current HUMAN_AUDIT_APPEND_ONLY_LOG.csv (151CF3D0…) | MATCH |
| FIRST_CODER_50_SHA256.txt | SNAPSHOT_SHA256 → FIRST_CODER_50_FROZEN.csv; SOURCE_400_WORKING → HUMAN_VALIDATION_400_WORKING.csv | MATCH / MATCH. ORIGINAL_SAMPLING_400 (DC242F8D…) was not checked because the file is not in the package. |
| SECOND_CODER_BLIND_20_SHA256.txt | MANIFEST_SHA256, ALLOCATION_SHA256, FROZEN_FIRST_CODER_SNAPSHOT_SHA256 | MATCH |
| SECOND_CODER_BLIND_20_SHA256.txt | QUEUE_SHA256 = 0100E524… vs current SECOND_CODER_BLIND_20.csv = 6AFC8D7A… | EXPECTED MISMATCH, explained (see below) |
| HUMAN_RECONCILIATION_INTERFACE_SHA256.txt | 7 files (server/html/js/test/check/gate/decision) | 7/7 MATCH |

**Why QUEUE_SHA256 differs.** QUEUE_SHA256 is the hash of the queue as prepared on 2026-10-02T20:21–20:57Z, before any second-coder answers were entered. To test this I rebuilt that blank state from the current file:
- Kept `record_id` and `evidence_text`.
- Blanked all other fields and set `review_status=NOT_STARTED`.
- Wrote UTF-8 with BOM and CRLF line endings, in the same row order.

The rebuilt file hashes to exactly `0100E52409608F26DE0DB772AC08D8FD03CCD81DC307A56EF79A0D9C3792101B`. **CONFIRMED:** record IDs, evidence text and row order did not change between blank preparation and coder-B completion. Only the answer, coder and status fields were filled in.

## PHASE 3 — 50/20/19 from raw rows

| Metric | Value | Source rows |
|---|---:|---|
| FIRST_CODER_TOTAL | **50** | FIRST_CODER_50_FINAL_FROZEN.csv (50 rows, 50 unique record_id) |
| FIRST_CODER_COMPLETE | **50** | 50/50 pass the completeness rule; 0 problems |
| SECOND_CODER_TOTAL | **20** | BLIND_REPEAT_20_FINAL_FROZEN.csv (= SECOND_CODER_BLIND_20.csv; 20 rows, 20 unique) |
| SECOND_CODER_COMPLETE | **20** | 20/20 pass the completeness rule; 0 problems |
| DISAGREEMENT_TOTAL | **19** | Derived by me: A vs B on the 20 paired records, any of C1–C5 differs |
| RECONCILIATION_COMPLETE | **19** | HUMAN_RECONCILED_20.csv: 19 HUMAN_ADJUDICATION rows that are valid and event-backed, plus 1 UNANIMOUS_PRE_ADJUDICATION row |

### First coder (A) cross-checks

- FIRST_CODER_50_FINAL_FROZEN.csv and FIRST_CODER_50_FROZEN.csv are byte-identical.
- In HUMAN_VALIDATION_400_WORKING.csv (400 rows), the status counts are COMPLETE=50, DRAFT=5 and NOT_STARTED=345.
- The 50 COMPLETE rows there are exactly the 50 frozen rows, matched by `validation_id`. Every field is identical (0 mismatches).
- FIRST_CODER_50_MANIFEST.csv has 50 rows, and its IDs equal the frozen IDs.
- All 50 rows have `coder_id="1"` and stratum `Robust A`.
- First-coder timestamps run from 2026-09-30T09:03:34Z to 2026-10-02T18:44:12Z. All are before the freeze at 2026-10-02T19:49:38Z.
- HUMAN_AUDIT_APPEND_ONLY_LOG.csv has 2 events:
  - FIRST_CODER_50_FROZEN with 50/50 records and snapshot DD332DD8….
  - SECOND_CODER_BLIND_20_PREPARED with 20/20 records.
- HUMAN_AUDIT_EPOCH2_LOG.csv has 5 hash-chained events (E2-…-001 to 005) that record the 50 verification and blindness checks.

### Blind second coder (B) cross-checks

- All 20 rows have `coder_id="2"`. There is no coder-ID overlap with A.
- All 20 IDs are a subset of A's 50, and `evidence_text` is identical to A's for all 20 records.
- I reproduced the selection independently. Within the stratum, records are ranked by SHA-256(`20261003|Robust A|record_id`) and the top 20 are taken. The result equals both the 20 IDs in the file and the manifest IDs. The allocation is Robust A 20 of 50, seed 20261003.
- SECOND_CODER_BLIND_20_AUDIT_LOG.csv has 21 events: 1 DRAFT and 20 COMPLETE. The last COMPLETE answer for each record equals the frozen B values for C1–C5 on all 20 records. The one DRAFT row has a blank `coder_id`, which is a minor gap in the log.
- Coder-B timestamps run from 2026-10-02T21:22:29Z to 2026-10-03T06:38:24Z. All are after A's freeze and after the blind subset was prepared.
- SECOND_CODER_120_WORKING.csv (legacy 120 design) has 120 rows, all NOT_STARTED, with 0 non-blank answers. It was not used.
- **Blindness:**
  - **CONFIRMED (file level):** B's file has only these columns: `record_id, evidence_text, human_* (C1–C5), coder_confidence, coder_notes, coder_id, coder_timestamp, review_status`. It contains no coder-A values, model labels or source-family columns.
  - **PROBABLE (process level):** The claim that B could not reach A's answers through the UI/API (`/api/first`=423) comes from EPOCH2 log events 004 and 005 and was not re-tested here. Coder IDs "1"/"2" are pseudonymous. That they are different people is a package claim and cannot be verified from the rows.

### Disagreement set — rules tested

| Rule | Records |
|---|---:|
| Any of the 5 dimensions differs (raw labels) | **19** |
| Any of the 5 dimensions differs (canonical labels) | **19** |
| Any of C1, C2, C5 only | 14 |
| Any of C3, C4 only | 18 |
| All 5 differ | 4 |
| C1 only | 5 |

The package rule is "any of 5". It is the rule used by `make_queue()` and by `verify_disagreement_queue()` in `human_reconciliation_server.py`. It yields 19.

The only fully agreeing record is `REC-0D720884574345B4`. Field-level disagreements total 58: C1=5, C2=13, C3=16, C4=16, C5=8.

Comparison with the queue file HUMAN_DISAGREEMENT_QUEUE_20.csv:
- It has 19 rows, and its ID set equals my derived set.
- All `first_Cx` and `blind_round_Cx` values equal the frozen A and B values.
- The `disagreement_fields` strings match exactly. There are 0 mismatches.

The legacy-design files DISAGREEMENT_QUEUE.csv and ADJUDICATION_LOG.csv are header-only (0 rows). They belong to the superseded 120-row design and do not conflict.

### Reconciliation

- HUMAN_RECONCILED_20.csv has 20 rows: 19 `HUMAN_ADJUDICATION` and 1 `UNANIMOUS_PRE_ADJUDICATION` (`REC-0D720884574345B4`). FINAL equals the shared A=B values for the unanimous row. It has no event and no reason, by design.
- HUMAN_RECONCILIATION_EVENTS.jsonl has 19 events, all `COMPLETE`, on 19 unique records, all by `researcher_id="3"`. Events are timed from 2026-10-03T07:45Z to 11:09Z, after B finished.
- The `previous_event_hash` chain is intact.
- I recomputed all 19 `current_event_hash` values as SHA-256 of the sort-keyed, compact, UTF-8 JSON of the event without that field. All 19 verify.
- For the 19 adjudicated rows:
  - FINAL values are within the codebook.
  - They equal the event values, and the event hashes equal `RECONCILIATION_EVENT_HASH`.
  - `RESOLUTION_REASON` is non-empty.
  - FIRST_/BLIND_ values equal the frozen coder rows.

  Result: RECONCILIATION_COMPLETE = 19/19.
- The 19 reconciled IDs equal the 19 queue IDs.

## PHASE 4 — Cohen's kappa (A vs blind B, pre-reconciliation, n=20)

- **Sources:**
  - Coder A: `FIRST_CODER_50_FINAL_FROZEN.csv`, filtered to the 20 B record IDs.
  - Coder B: `BLIND_REPEAT_20_FINAL_FROZEN.csv`.
  - Pairs were matched by `record_id`.
- **Kappa variant:** unweighted nominal Cohen's kappa. The label set is the union of labels observed for either coder. Pe = Σ (nA_c · nB_c) / n². This is the same as `cohen_kappa()` in both package scripts.

| Dim | Source column | n | Agree | Po | Pe | kappa (canonical = raw) |
|---|---|---:|---:|---:|---:|---:|
| C1 Evidence validity | human_evidence_valid | 20 | 15 | 0.7500 | 0.4300 | **0.561404** |
| C2 Relation type | human_relation_type | 20 | 7 | 0.3500 | 0.2075 | **0.179811** |
| C3 AI functional family | human_ai_family | 20 | 4 | 0.2000 | 0.1600 | **0.047619** |
| C4 Decision functional family | human_decision_family | 20 | 4 | 0.2000 | 0.0700 | **0.139785** |
| C5 Analytical inclusion | human_include | 20 | 12 | 0.6000 | 0.4150 | **0.316239** |

### Label sets and marginals (A | B)

- **C1** {INVALID, UNCERTAIN, VALID}
  - A: VALID 14, INVALID 4, UNCERTAIN 2
  - B: VALID 10, INVALID 6, UNCERTAIN 4
- **C2** {AMBIGUOUS, ASSOCIATED_WITH, CONSTRAINS, ENABLES, GOVERNS, INFORMS, NOT_APPLICABLE, SUPPORTS, TRANSFORMS}
  - A: SUPPORTS 6, NOT_APPLICABLE 4, ENABLES 3, INFORMS 2, GOVERNS 2, TRANSFORMS 2, CONSTRAINS 1
  - B: SUPPORTS 9, NOT_APPLICABLE 6, AMBIGUOUS 2, ENABLES 1, INFORMS 1, ASSOCIATED_WITH 1
- **C3** 11 labels
  - A: PREDICTION_RISK_ESTIMATION 6, AMBIGUOUS 5, COORDINATION_EXECUTION 3, EVALUATION_ASSESSMENT 2, UNMAPPED 1, RECOMMENDATION_OPTIMIZATION 1, EXPLANATION_ASSURANCE 1, HUMAN_AUGMENTATION 1
  - B: PREDICTION_RISK_ESTIMATION 9, GENERAL_REASONING_SYSTEMS 2, GENERATION_SYNTHESIS 2, HUMAN_AUGMENTATION 2, EXPLANATION_ASSURANCE 2, AMBIGUOUS 1, RECOMMENDATION_OPTIMIZATION 1, PERCEPTION_EXTRACTION 1
- **C4** 12 labels
  - A: AMBIGUOUS 6, PREDICTION_DIAGNOSIS 3, GENERAL_DECISION_PROCESS 3, RISK_ASSESSMENT 2, EXECUTION_COORDINATION 2, INFORMATION_SYNTHESIS 1, GOVERNANCE_OVERSIGHT 1, ALLOCATION_PLANNING 1, INFORMATION_ACQUISITION 1
  - B: GENERAL_DECISION_PROCESS 5, ALLOCATION_PLANNING 4, RISK_ASSESSMENT 3, UNMAPPED 3, GOVERNANCE_OVERSIGHT 3, OPTION_GENERATION 1, EVALUATION_SELECTION 1
- **C5** {EXCLUDE, INCLUDE, UNCERTAIN}
  - A: INCLUDE 13, EXCLUDE 4, UNCERTAIN 3
  - B: INCLUDE 10, EXCLUDE 6, UNCERTAIN 4

### Comparison with the package summaries (read only after computing)

| Dim | Mine | HUMAN_RELIABILITY_FINAL.csv | HUMAN_RELIABILITY_20.csv | MD (both) | Expected | Abs diff vs csv (all ≤ 0.0005) |
|---|---:|---:|---:|---:|---:|---:|
| C1 | 0.561404 | 0.5614 | 0.5614 | 0.561 | 0.561 | 0.000004 |
| C2 | 0.179811 | 0.1798 | 0.1798 | 0.180 | 0.180 | 0.000011 |
| C3 | 0.047619 | 0.0476 | 0.0476 | 0.048 | 0.048 | 0.000019 |
| C4 | 0.139785 | 0.1398 | 0.1398 | 0.140 | 0.140 | 0.000015 |
| C5 | 0.316239 | 0.3162 | 0.3162 | 0.316 | 0.316 | 0.000039 |

Other values reproduced:
- Agreement counts 15/7/4/4/12 and disagreement counts 5/13/16/16/8.
- Wilson 95% CIs for raw agreement: 53.13–88.81, 18.12–56.71, 8.07–41.60, 8.07–41.60 and 38.66–78.12.
- Confidence exact match 9/20.
- `HUMAN_RECONCILIATION_REQUIRED=19`.

All of these equal the summary files.

**Observation (not a point-estimate conflict; not reproduced):** the paired-bootstrap kappa 95% CIs differ between `HUMAN_RELIABILITY_FINAL.csv` and `HUMAN_RELIABILITY_20.csv` for C2–C5. C1 is identical in both.

| Dim | FINAL CI | _20 CI |
|---|---|---|
| C2 | −0.0811 to 0.4286 | −0.0791 to 0.4231 |
| C3 | −0.0811 to 0.1758 | −0.0778 to 0.1753 |
| C4 | −0.027 to 0.3143 | −0.0298 to 0.3162 |
| C5 | 0.0148 to 0.6227 | 0.0141 to 0.6172 |

Both files state 20,000 resamples. Their seed descriptions differ: the FINAL file says "field seeds 20261003…20261007", while the _20 file says "field-specific seeds derived from 20261003". This bootstrap CI is UNRESOLVED as to which version is canonical. Any manuscript citing kappa CIs should name the file it uses. The point estimates are unaffected.

`SECOND_CODER_RELIABILITY.csv` (legacy 120 design) is header-only and plays no role here.

### Caveats (carried, not introduced)

- n=20 from a single stratum (Robust A). All kappas are exploratory.
- The package itself describes the first-coder 50 as a "researcher-reviewed human audit with coding-rule consultation, not fully AI-blind independent validation" (`finalize_blind_audit_20.py`).

## Verdict

- The 50/20/19 counts are reproduced from raw rows: 50/50 first coder, 20/20 blind second coder, 19 disagreements (any-of-5 rule, equal to the queue file) and 19/19 reconciled with a valid hash chain.
- Cohen's kappa for C1–C5 is reproduced within 0.0005 of both summary CSVs, using both raw and alias-canonical labels.
- The raw data do not conflict with the summary point estimates. The only inconsistency is the bootstrap CIs in FINAL vs _20, which lie outside the kappa point-estimate scope.

50_20_19_REPRODUCED=YES
KAPPA_REPRODUCED=YES
