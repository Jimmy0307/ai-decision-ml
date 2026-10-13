# 25 — V1 Final Protocol v1.8.2 (pre-human freeze; supersedes 19)

**STUDY TEAM ONLY — not for coders.**

**Status:** prepared and frozen at S1. **No human coding has been executed.** No result, simulated coder, expected α or κ, or synthetic agreement exists. The research decisions behind this protocol are recorded in 24.

## 1. Purpose and bounded claim

V1 asks whether independent human coders agree on which enterprise decision mechanism or interface, if any, each of the 16 robust-depletion literature pairings represents. The primary question is **inter-rater reliability**, not agreement with the researcher's key.

**V1 validates only the G → enterprise-mechanism interpretation. It does not validate the 32-cell membership, the taxonomy, or the network statistics.** Nothing in V1 changes:
- the Study 1 freeze, the 32 core cells, the 47 cells, or G01–G16;
- the researcher's G→M assignments;
- VCP / VSC / DL / NEV;
- the Enterprise v2.2 model, the solver, or the schema.

## 2. Files

| File | Role | Who sees it |
|---|---|---|
| 24 | Researcher decision record | study team |
| 25 | This protocol | study team |
| 26 | Codebook (§1–4 mirror the coder xlsx) | study team; coders see only the xlsx |
| 27 | Pre-freeze audit (script-verified) | study team |
| 28 | Blinding and recruitment plan | study team |
| 29 | Frozen analysis plan | study team |
| 30 | Distribution README | coordinator |
| `coder_distribution/CODER_1.xlsx`, `CODER_2.xlsx`, `CODER_3.xlsx` | One packet per coder: neutral IDs, own seeded order, blank responses and attestation | **coders** |
| `20_MASTER_PACKET_v1_8_2.xlsx` | Study-team master: all 3 coder sheets, items in neutral-ID order, empty adjudication sheet; no G IDs | study team only |
| `V1_SEALED/RESEARCHER_ASSIGNMENT_COMMITMENT.md`, `ITEM_ID_TO_GID_MAP.COMMITMENT.md`, `ITEM_ORDER_LOG.COMMITMENT.md`, `FREEZE_MANIFEST_V1_8_2_S1.txt` | Hash commitments and the S1 freeze | study team |
| `tools/` | `build_v1_packet_v182.py`, `v1_construct_analyzer_v182.py`, `test_v1_construct_analyzer_v182.py` (+ result), `leakage_check_v182.py` (+ result), `audit_v182.py`, `no_human_data_run_v1_8_2/` | study team |
| SEALED_LOCAL (`20261014_V1_8_2_PREFREEZE\SEALED_LOCAL_STUDY_TEAM_ONLY\`, not in git) | `ITEM_ID_TO_GID_MAP.json`, `ITEM_ORDER_LOG.json`, `SECRET_SEED_v1_8_2.txt` | study team only |

## 3. Instrument

The instrument has 16 items, identified by neutral IDs ITEM-A01…ITEM-A16. The IDs are assigned by a permutation from a secret seed, so they carry no relation to the study's internal numbering. Each coder file has its own seeded item order.

The item content comes from frozen 54A only:
- the families and their definitions;
- the neutral pair description;
- a standard depletion statement.

The items carry no counts, q-values, G IDs or sensitivity markers. Questions Q1–Q5, the categories, the consistency rules and the 7-item attestation are defined in codebook 26.

**Approved decisions (24):**
- **OA-2: APPROVED_WITH_SCOPE_LIMIT.** The derived 53B variables are secondary continuity metrics only.
- **OA-3: APPROVED.** NONE requires Q1 = YES and a Q5 that states the decision not captured.

## 4. Roles

| Role | Requirements |
|---|---|
| Coordinator | Study team. Distributes and receives files, computes hashes, runs scripts. Never gives content feedback. |
| Coders | Three independent humans (`N_HUMAN_CODERS=3`): CODER_1, CODER_2, CODER_3. No AI coder. Blinding and recruitment criteria are in 28. |
| Adjudicator | Not a coder, not the author of 41, not a translator. If the author must adjudicate, the case is marked `AUTHOR_ADJUDICATED` and treated as a limitation. |

## 5. Blinding

- Masked G IDs and per-coder seeded orders.
- Coders receive packets directly, never through GitHub.
- 7-item attestation. Exposed coders are flagged and never silently pooled.

**Limitation (28 §1):** the repository was public before coding, and a repository reader could re-identify the items from their family pairs. Perfect blinding is not claimed.

## 6. Leakage control

`tools/leakage_check_v182.py` scans two layers and must report **0 findings**:
- **Cell level:** every coder-facing workbook.
- **Raw XML:** every part of each xlsx, including:
  - `docProps/core.xml` and `docProps/app.xml`;
  - data validations;
  - any custom XML;
  - any comments;
  - defined names;
  - hidden elements;
  - formulas.

In addition, every text file in OUT is checked for:
- ITEM-ID ↔ G-ID pairs;
- per-coder order lists;
- the secret seed;
- plaintext sealed files.

The current result is in `tools/leakage_check_result_v1_8_2.json`, and the audit lines are in 27.

## 7. Phases and freezes

| Phase | Action | Gate (enforced by the analyzer where marked *) |
|---|---|---|
| **S1** | Freeze the packet, protocol, codebook, analysis plan, analyzer, leakage script and result, commitments, and the plaintext map/log (by hash). | `V1_SEALED/FREEZE_MANIFEST_V1_8_2_S1.txt`, generated last |
| Distribution | Send the per-coder files (30). | The SHA-256 of each file sent must equal its S1 hash. |
| **S2** | Freeze the three returned sheets. | `FREEZE_MANIFEST_V1_8_2_S2.txt` (*: phase R refuses sheets not listed in it) |
| **R** | Reliability on neutral IDs only. The researcher key and item map stay sealed; nothing is unsealed just to compute reliability. Output: A. CURRENT_INSTRUMENT_RELIABILITY (primary) and B. 53B_CONTINUITY_RELIABILITY (secondary), never collapsed. | * |
| **A** | Adjudication: coders discuss without the key, then the adjudicator decides. | — |
| **S3** | Freeze the adjudication file. | `FREEZE_MANIFEST_V1_8_2_S3.txt` (*: the item map, `--unseal` and classes all require it) |
| S | G04/G10/G11 sensitivity (16 vs 13 items), using the hash-verified item map. | * after S3 only |
| **K** | Unseal the researcher key. The SHA-256 of `sealed_key.json` must equal the committed `d1702188…6734`. Compare with the flattened key. | * never before S3; on a hash mismatch, STOP |
| **C** | 53B §11 mapping-sensitivity classes (frozen); then the `V1_PASS_HUMAN_C6` continuity label. | * classes file must be hash-frozen |

## 8. Analysis and decision rule

The analysis is specified in 29.

- **Primary statistic:** Krippendorff's α (nominal) on Q2, all 16 items, 3 coders, with a 95% bootstrap CI (5,000 resamples, seed 20261011).
- **Secondary statistic:** pairwise Cohen's κ.
- **Classification:**

  | α (point estimate) | Label |
  |---|---|
  | ≥ .800 | RELIABLE |
  | .667 to < .800 | TENTATIVE |
  | < .667 | UNRESOLVED/NOT_ACCEPTABLE |

  If the lower CI bound is below .667, the label also carries IMPRECISE.
- **Threshold provenance:** RESEARCH_CONVENTION, not a universal standard. Landis & Koch labels are not used.

**Required manuscript wording:** "V1_PASS_HUMAN_C6 is a continuity label under the earlier 53B protocol, not evidence that the amended Q1–Q5 instrument is identical to 53B."

## 9. Data governance

- Returned sheets are kept in local, controlled storage and are never pushed to the public repository.
- Only de-identified aggregate results are published, and only after the researcher has reviewed them (30).
- Once any coder has received a packet, any content change invalidates S1.

## 10. Supersession

v1.8.1 files 19, 20* and 21 are superseded. In particular, the v1.8.1 packets show G IDs and **must not be distributed**. The v1.8.1 analyzer is superseded by `v1_construct_analyzer_v182.py`.

FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION
FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET
FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED

V1_HUMAN_CONSTRUCT_VALIDATION_STATUS=READY_TO_RUN
