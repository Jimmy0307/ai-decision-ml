# 13 — Forensic Audit of the "84–85/120" Re-segmentation Figures (Cleanup Debt D)

- Round: V1.8.1 Study 1 evidence freeze. Sub-agent G. Date: 2026-10-14.
- Scope: every occurrence of the 84/120 and 85/120 figures and their variants; the source chain; R14 vs V9.1 attribution; corrected provenance wording.
- Mode: read-only on REPO tracked files, W, the V9 package and the docx files under `C:\NTUST_PAPER\`. Nothing was rewritten. This file and the tools in `tools/G/` are the only outputs.
- **STOP status: NOT TRIGGERED.** Every number was recomputed from raw rows and matches the manuscript. Only the attribution needs correcting.

---

## 0. Verdict (short)

| Question | Answer | Evidence grade |
|---|---|---|
| Are 84/120 (S1) and 85/120 (S2) correct? | **Yes.** I recomputed them from raw document-edge rows: 84 and 85 cells changed their observed count against the frozen baseline. | CONFIRMED (raw rows > code output) |
| Are the companion figures correct? | **Yes.** Direction changes are 12 and 11. Both cores have 31 cells (15 enriched / 16 depleted). Baseline cells retained: 29/32 and 30/32. Enriched retained: 15/16 and 15/16. Depleted retained: 14/16 and 15/16. Persistent in all three settings: 29. Jaccard: .853, .909 and .938. Candidates: 3,112/6,499. Units: 25,112 and 25,503. Pair-eligible units: 2,412 and 2,394. Documents: 652 and 650. Edges: 1,678 and 1,663. q≤.05 counts (main/exact/doc/raw): 40/40/32/48 and 42/41/31/51. | CONFIRMED |
| Origin of the figures | **(c) A V9.1 sidecar sensitivity analysis, computed against the frozen V9 primary baseline.** That baseline is the primary 32-core analysis (analytical freeze `20260918T132206Z`), which was reproduced byte-identically on 2026-10-03. It is the same primary analysis that R14 reports. R14 later copied the V9.1 results into its own text (R14 §3.11.1, §4.6.2–4.6.3 with Tables 6–7, §5.5, and supplement S10). | CONFIRMED for the origin. PROBABLE for R14's file identity (see §3). |
| Did R14 have its own pre-2026-10-03 re-segmentation analysis? | **No evidence of one exists.** The premise "R14 = 2026-09-20" comes from inherited docx metadata. The R14 docx is a **post-V9.1** revision, and its lineage runs from 2026-10-04 to 2026-10-07. The real 2026-09-20/21 submission (`V9_CONFERENCE_CAMERA_READY_FULL_CHINESE_BODY_20260921.docx`) contains **zero** re-segmentation content. | CONFIRMED for the absence in the 09-21 docx and for the inherited-metadata explanation. PROBABLE for R14 = the 2026-10-07 file. |
| Is attributing the figures to "R14" wrong? | **Incomplete, not false.** R14 is a correct *text* source because the figures appear verbatim in R14. It is wrong as an *analytic* source: R14 did not compute them. The open flags in v1.8 (02 §6, 08_PATCH_LOG, 10_FINAL_STATUS #2) treat R14 and V9.1 as competing sources. They are one chain: V9.1 computed the figures (2026-10-03) and R14 reported them (≥ 2026-10-04). | — |

---

## 1. Occurrence inventory

Search tool: `tools/G/find_84_85.py`. It scanned all text files (md, txt, csv, json, jsonl, py, html, tex, tsv, yaml, xml, js; files ≤ 5 MB) and applied NFKC normalization, so fullwidth digits and slashes were folded in. Patterns covered:
- `84/120` and `85/120`, also written with `／`, `of`, `格`, `個` or `之`;
- `84–85`, plus the `-` and `~` variants;
- `84 and/與/和/、 85`;
- "84" followed within 40 characters by "120".

Roots scanned: REPO (whole working tree), `W\01_ALL_OUTPUTS` (r14_merge, v1_1–v1_7, v2_1–v2_3) and `W\02_V9_HUMAN_VALIDATION` (including V9_1_SEGMENTATION_SENSITIVITY). Docx files were scanned separately with `tools/G/docx_scan.py` and `docx_text.py`. Raw hit list: `tools/G/hits.tsv` (410 lines).

### 1.1 Manuscripts (v1.8 is current; the others are historical checkpoints and must not be rewritten)

Every merged manuscript from v1.0 to v1.8 carries the **same five lines**. They were copied verbatim from R14, except the 5.8.3 limitation, which was newly written in the v1.0 fragment `r14_merge/tools/frag/f50_ch5.md:87`. All five lines present the figures as the study's own sensitivity analysis (「本研究在完成主要分析後加入兩種保守的證據單元重切分設定」, v1.8 L599). No line names a source inline. The only attribution is implicit, through the source-code appendix: v1.8 L2939 makes R14 「第 2.1–2.7、3.1–3.8、4.1–4.6、5.1–5.4、5.7–5.10 節的文獻層內容與全部文獻層數值的權威來源」. Neither the body nor the appendix names V9.1. V9_1_SEGMENTATION_SENSITIVITY appears only in Appendix E49 (L3073), and only for the label-propagation question.

| Manuscript | §4.5.2 first-order effects ("84 與 85 格") | Table 4-8 rows ("84/120；12/120", "85/120；11/120") | §5.4.2 ("84–85/120 格") | §5.8.3 ("84 與 85 個矩陣格") | Attributed to |
|---|---|---|---|---|---|
| **v1.8** `REPO/claude/r14_merge_v1_8_source_closure/08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md` (sha256 1515b0f2…) | L1577 | L1600, L1601 | L2264 | L2334 | Implicit R14 (L2939). V9.1 not named. |
| v1.7 `W/.../r14_merge_v1_7/130_…EVIDENCE_CONVERGED_CANDIDATE.md` (+ .docx with the same strings) | L1577 | L1600, L1601 | L2264 | L2334 | Implicit R14 |
| v1.6 `r14_merge_v1_6/127_…` | L1522 | L1545, L1546 | L2166 | L2228 | Implicit R14 |
| v1.5 `r14_merge_v1_5/118_…` | L1474 | L1497, L1498 | L2118 | L2180 | Implicit R14 |
| v1.4 `r14_merge_v1_4/105_…` | L1446 | L1469, L1470 | L2077 | L2139 | Implicit R14 |
| v1.3 `r14_merge_v1_3/100_…` | L1451 | L1474, L1475 | L2082 | L2144 | Implicit R14 |
| v1.2 `r14_merge_v1_2/82_…` | L1446 | L1469, L1470 | L2077 | L2139 | Implicit R14 |
| v1.1 `r14_merge_v1_1/73_…` | L1334 | L1357, L1358 | L1912 | L1972 | Implicit R14 |
| v1.0 `r14_merge/66_…` | L1243 | L1266, L1267 | L1775 | L1833 | Implicit R14 |
| v2_1, v2_2, v2_3 | — | — | — | — | no hits |

Exact v1.8 text of each hit:
- **L1577:** 「…相較原始記錄的家族配對集合，兩種設定分別有 742 與 765 筆候選記錄發生改變；120 個矩陣位置中，觀察值分別有 84 與 85 格改變，主要零模型的高於／低於期望方向分別有 12 與 11 格改變。…」
- **L1600:** 「\| 句層級重切分 \| 40 / 40 / 32 / 48 \| 31 (15/16) \| 29/32 \| 過度 15/16；不足 14/16 \| 84/120；12/120 \| 中度 \|」
- **L1601:** 「\| 句與子句層級重切分 \| 42 / 41 / 31 / 51 \| 31 (15/16) \| 30/32 \| 過度 15/16；不足 15/16 \| 85/120；11/120 \| 中度 \|」
- **L2264:** 「兩種較細粒度的重切分設定顯示，證據單元界定確實會影響矩陣，但影響具有層次。84–85/120 格的觀察值發生變化，…主要穩健集合中的 29/32 與 30/32 格仍被保留，且三種設定共同保留的 29 格沒有方向反轉。…」
- **L2334:** 「證據單元界定會改變局部計數：兩種重切分設定分別使 84 與 85 個矩陣格的觀察值改變、12 與 11 格的主要零模型方向改變，並使 3 組主要穩健配對（…）的穩健集合資格改變。…」

### 1.2 Memos and reports

| File:line | Exact text (abridged) | Attributes figures to |
|---|---|---|
| REPO `…v1_8_source_closure/02_V9_AUTHORITY_MAP.md:115` | "…SEGMENTATION_SENSITIVITY_COMPLETE; MODERATE_TURNOVER; S1/S2 core 31/31; counts changed 84/120 and 85/120…" | V9.1 |
| same, `:146` | "observed counts changed in 84 / 85 of 120 cells; main directions changed in 12 / 11 cells" | V9.1 |
| same, `:147` | "It is the source of the "84–85/120" re-segmentation figures that v1.7/131 attribute to R14." | V9.1, with v1.7/131 → R14 framed as a conflict |
| REPO `…/08_PATCH_LOG.md:445` | "02 §6 notes that the 84–85/120 re-segmentation figures come from the V9.1 sidecar. v1.7 attributes the segmentation analysis to R14. That attribution was not changed … **Flag for the next round.**" | V9.1 vs R14 (open flag) |
| REPO `…/10_FINAL_STATUS.md:94` | "v1.7/v1.8 attribute the "84–85/120" re-segmentation figures to R14, but the source is V9.1 `SEGMENTATION_SENSITIVITY` (2026-10-03). This attribution has not been audited…" | V9.1 vs R14 (open flag) |
| REPO `…/tools/E/v9claims.txt:49`, `…/tools/E/v9lines.txt:57` | copies of v1.8 L2264 | (working files, no attribution) |
| REPO `…/tools/F/build_log.py:127` | generator string for the 08_PATCH_LOG line above | (generator) |
| W `r14_merge/68_R14_ENTERPRISE_RECONCILIATION_v1_0.md:48–49` | "句層級 \| …觀察值改變 84/120；方向改變 12/120；中度" / "句與子句層級 \| …85/120；11/120；中度"; column header "R14（01/02）值" | R14 (text source) |
| W `r14_merge/69_MERGED_THESIS_FORENSIC_AUDIT_v1_0.md:61` | "92 項 R14 數值與措辭(含 … 84/120、85/120 等)逐一搜尋 \| 0 項缺漏" | R14 (text source) |
| W `r14_merge/tools/audit69.py:77` | required-token list `'84/120', '85/120', '12/120', '11/120'…` | R14 (text source) |
| W `r14_merge/tools/frag/f50_ch5.md:87` | source fragment of the §5.8.3 sentence | (new text written in the merge; numbers from R14) |
| W `r14_merge_v1_7/131_HUMAN_VALIDATION_INTEGRATION_REPORT.md:83` | "\| 3. 證據片段切分歧義 \| 多功能、過寬的片段；重切分使 84–85/120 格觀察值改變 \| …" | none inline. Context: the 131 §2 sources are R14 line refs |
| W `r14_merge_v1_7/133_V0_V7_VALIDATION_LEDGER.md:32` (related; no 84/85) | "文獻層證據單元敏感度（L3）\| 完成 \| R14 表 6–8 \| 29 持續、3 邊界敏感" | R14 Tables 6–8 (text source) |
| W `r14_merge_v1_7/128_CANONICAL_STATE.md:46` (related; CF-03) | "`r14/01_R14_…CANONICAL.docx`（docx 中繼資料修改時間 2026-09-20）… R14 已含 50／20／19 稽核與證據單元重切分。時間戳不可靠，以內容判定" | Origin of the "R14 = 2026-09-20" premise |

### 1.3 V9 package (V9_1_SEGMENTATION_SENSITIVITY)

| File:line | Text | Status |
|---|---|---|
| `SEGMENTATION_FIRST_ORDER_EFFECTS.md:16` | "Observed counts changed in 84/120 cells; all-cell main-test direction changed in 12/120; … unchanged in 76 and changed in 8." | **Operative** (sha 08d52cf4…, listed in V9_1_OUTPUT_SHA256.csv) |
| `SEGMENTATION_FIRST_ORDER_EFFECTS.md:19` | "Observed counts changed in 85/120 cells; all-cell main-test direction changed in 11/120; … unchanged in 77 and changed in 8." | **Operative** |
| `SEGMENTATION_SENSITIVITY_FINAL_REPORT.md:17` | "5. Observed counts changed in **S1 84/120; S2 85/120** cells." Generated UTC 2026-10-03T16:41:45Z | **Operative** (sha 15d48ecb…) |
| `_S2_COMMA_SPLIT_NONCONFORMING_ARCHIVE_20261003T235149/SEGMENTATION_SENSITIVITY_FINAL_REPORT.md:17` | "Observed counts changed in **S1 84/120; S2 87/120** cells." | **Superseded** nonconforming S2 (comma split). Not used; the final report states it is excluded. |
| `_S2_COMMA_SPLIT_NONCONFORMING_ARCHIVE_…/SEGMENTATION_FIRST_ORDER_EFFECTS.md:14` | "Observed counts changed in 84/120 cells; main-test direction changed in 0/120…" | **Superseded** |

No other V9 text file contains the figures.

### 1.4 Docx files under `C:\NTUST_PAPER\` (outside W; read-only)

| File | sha256 | Re-segmentation content |
|---|---|---|
| `V9_CONFERENCE_CAMERA_READY_FULL_CHINESE_BODY_20260921.docx` (the actual 2026-09-20/21 submission) | 62aff771bcad1e1f… | **0** hits for 重切分, 84/120, 85/120, 3,112, 29/32 or 30/32. It still describes the 400/120 human validation. |
| `outputs/20260929_V9_HUMAN_VALIDATION/V9_HUMAN_AUDIT_PATCHED_CANDIDATE.docx` (same sha as the W copy) | f5c9366a7581ee49… | **0** hits |
| `V9_FINAL_SUBMISSION_CANDIDATE_20261004.docx` (file mtime 2026-10-07 03:11 +08) | **f4252f765c4294fe**7c9cda219af6685fa00372613235c228aae29978cddc3ff6 | 84/120 ×1; 85/120 ×2; 「84 與 85」 ×1; 「84–85」 ×1; 3,112 ×2; 重切分 ×36. In §3.11.1, §4.6.2, Table 7 (§4.6.3) and §5.5. |
| `V9_FINAL_SUBMISSION_CANDIDATE_20261005_R7/_R9_VERIFIED.docx` | fe6ae39e…, 88e1b506… | same figures present |
| W `r14_merge_v1_7/130_…v1_7…docx` | d053b4b8… | same figures (mirror of the 130 md) |

All of these docx files carry the **same** `docProps/core.xml` modified timestamp, `2026-09-20T13:37:37Z`, including the camera-ready that has no re-segmentation and the candidates from 10-04 to 10-07. The timestamp is template metadata inherited from one source document. **It does not date any of them.**

### 1.5 False positives (excluded)

- `r14_merge_v1_2/93_ORG_IMPLEMENTATION_CHANGELOG_v1_0.md:42`, `org_schema.py:2` (v1_2–v1_5 copies), `tools/audit92.py:74` and `tools/gen92_93.py:177`: these refer to file numbers 83/84/85.
- REPO `…/tools/A/hash_citations.csv:100`: a SHA-256 string.
- 339 hits in machine-data files (.csv/.json/.jsonl in the V9/V9.1 package): record IDs, hashes and counts. None contains an "84/120"-type figure string. **No figure attribution occurs in machine data.** The figures exist there only as derivable counts (§2).

---

## 2. Source chain and recomputation from raw rows

Script: `tools/G/recompute_seg.py`. Output: `tools/G/recompute_seg_out.json`, which records sha256 for every input. Membership-rule check: `tools/G/verify_membership_rule.py`. Unit counts: `tools/G/count_units.py`.

**Chain** (raw rows → code output → summary → manuscript):

1. **Baseline:** `V9_1_SEGMENTATION_SENSITIVITY/_baseline_reproduction/10_DOCUMENT_DEDUP_MATRIX/matrix_v1_20261003T133157Z/DOCUMENT_PAIR_EDGES_DEDUP.csv` (2,180 rows) and `…/12_ROBUSTNESS_SENSITIVITY/robustness_v1_20261003T133222Z/ROBUSTNESS_COMPARISON_120.csv`. `BASELINE_REPRODUCTION_VERIFICATION.md` reports a byte-identical match to the official V9 freeze `analytical_freeze_v2_20260918T132206Z` (27/27 PASS). My recomputed baseline core equals `FINAL_ROBUST_CORE_32.csv` (`True`).
2. **Variants:** `S1_DOCUMENT_EDGES.csv` (1,678 rows; 652 documents) and `S2_DOCUMENT_EDGES.csv` (1,663 rows; 650 documents) → `S1_120_CELL_RESULTS.csv` (sha 6b50e837…) and `S2_120_CELL_RESULTS.csv` (sha f1f23c06…). The per-cell edge counts match `dedup_observed` with 0/120 mismatches in each of baseline, S1 and S2.
3. **Comparison:** `SEGMENTATION_CELL_COUNT_DIFF.csv`, which is byte-identical to `ROBUST_CORE_COMPARISON.csv` (sha 10b0f65b… for both) → `SEGMENTATION_FIRST_ORDER_EFFECTS.md` / `SEGMENTATION_SENSITIVITY_FINAL_REPORT.md`. All hashes match `V9_1_OUTPUT_SHA256.csv`.

**Recomputed figures:**

| Figure (manuscript) | Recomputed from raw rows | Packaged diff/report | Match |
|---|---|---|---|
| Observed count changed, S1 / S2 (cells whose edge count ≠ baseline) | **84 / 85** | 84 / 85 (`*_count_delta ≠ 0`) | ✓ |
| Main-null direction changed, all 120 cells | **12 / 11** | 12 / 11 | ✓ |
| Core size (all four q ≤ .05 and one common direction) | **31 / 31**; 15 enriched / 16 depleted in each | 31 / 31 | ✓ (rule check: 0 flag mismatches) |
| Baseline 32 retained | **29 / 30** | 29 / 30 | ✓ |
| Baseline enriched / depleted retained | **15/16, 14/16** (S1); **15/16, 15/16** (S2) | same | ✓ |
| Direction reversals among retained cells | **0 / 0** | 0 / 0 | ✓ |
| Persistent in all 3 settings, same direction | **29** | 29 | ✓ |
| Jaccard baseline–S1 / baseline–S2 / S1–S2 | **.853 / .909 / .938** | same | ✓ |
| q≤.05 counts, main / exact / doc / raw | baseline 47/46/32/54; S1 **40/40/32/48**; S2 **42/41/31/51** | Table 4-8 | ✓ |
| Candidates | **3,112 / 6,499** (`SEGMENTATION_CANDIDATE_MANIFEST.csv`, `candidate=True`) | 3,112; 47.88% | ✓ |
| Analysis units / pair-eligible units / documents / edges | S1 **25,112 / 2,412 / 652 / 1,678**; S2 **25,503 / 2,394 / 650 / 1,663** | same | ✓ |
| Candidate sub-units | 25,112 − 3,387 = **21,725**; 25,503 − 3,387 = **22,116** (arithmetic) | same | ✓ |
| Changed candidate parents, 742 / 765 | NOT_RECOMPUTED (summary level: FINAL_REPORT item 4) | 742 / 765 | not checked |
| Entries/exits | S1: +COORDINATION_EXECUTION×PREDICTION_DIAGNOSIS, +RECOMMENDATION_OPTIMIZATION×GOVERNANCE_OVERSIGHT; −EXPLANATION_ASSURANCE×EVALUATION_SELECTION, −HUMAN_AUGMENTATION×EVALUATION_SELECTION, −RECOMMENDATION_OPTIMIZATION×EVALUATION_SELECTION. S2: +COORDINATION_EXECUTION×PREDICTION_DIAGNOSIS; −EXPLANATION_ASSURANCE×EVALUATION_SELECTION, −RECOMMENDATION_OPTIMIZATION×EVALUATION_SELECTION | same | ✓ |

**No number-vs-source conflict was found, so no STOP.**

Note on S2: the superseded comma-split S2 run gave 87/120. The manuscript's 85/120 is the corrected, conservative S2, which is the operative result.

---

## 3. R14 vs V9.1: what the evidence shows

**What "R14" is.** In 128 §1 row 1, R14 is `r14/01_R14_AI_DECISION_FINAL_SUBMISSION_CANONICAL.docx` with sha256 prefix **f4252f765c4294fe…**. The R14 package itself is not in W or REPO, and its full hash is **NOT_RECOVERED**. One file on disk matches that 16-hex prefix exactly: `C:\NTUST_PAPER\V9_FINAL_SUBMISSION_CANDIDATE_20261004.docx`, sha256 f4252f765c4294fe7c9cda219af6685fa00372613235c228aae29978cddc3ff6, mtime 2026-10-07 03:11 +08. Its §4.6.2 paragraph is verbatim identical to v1.8 L1577. Its §3.11.1 contains 「人工調和標籤也不傳播至未稽核記錄」, which 128 CF-11 and 131 cite as "R14 02:258". Identity R14 = this file is **PROBABLE**: a 64-bit prefix match plus verbatim content.

**Timeline** (file mtimes and in-file timestamps; filesystem times are +08):

| When | Artifact | Re-segmentation content |
|---|---|---|
| 2026-09-18 (UTC run id) | V9 analytical freeze `analytical_freeze_v2_20260918T132206Z` — the primary 32-core baseline | n/a (baseline) |
| 2026-09-20T13:37Z (docProps) / file 2026-09-22 | V9 camera-ready `…FULL_CHINESE_BODY_20260921.docx` — the "2026-09-20" submission | **none** |
| 2026-10-03 (run ids 20261003T13–16Z) | V9.1 sidecar runs; `SEGMENTATION_SENSITIVITY_FINAL_REPORT.md` generated 2026-10-03T16:41:45Z | **computed here** |
| 2026-10-03 20:19 | `V9_HUMAN_AUDIT_PATCHED_CANDIDATE.docx` | none |
| 2026-10-04 02:30 | `V9_FINAL_PATCH_REPORT_20261004.md`: "Replaced … wording with the completed **V9.1 segmentation sensitivity** result … Added Method §3.11.1 … Result §4.10 with the V9.1 counts" (candidate sha at that time 0001a6ea…) | first manuscript import of V9.1 |
| 2026-10-04 02:49 | `V9_RESULTS_SENSITIVITY_R2_CHANGELOG_20261004.md`: "first-order V9.1 re-unitization effects … 84/120 and 85/120 observed-count changes; 12/120 and 11/120" | V9.1 → manuscript (R2) |
| 2026-10-04 03:28 → 2026-10-05 02:33 | R3 changelog; R7/R8/R9 `_VERIFIED.docx` | V9.1 figures carried forward |
| 2026-10-07 03:11 | `V9_FINAL_SUBMISSION_CANDIDATE_20261004.docx`, sha f4252f76… = R14 prefix | V9.1 figures (R14 §3.11.1, §4.6.2–4.6.3, Tables 6–7, §5.5, S10) |
| 2026-10-11 | r14_merge v1.0 (66–72): R14 imported as "權威 1" | inherited |
| 2026-10-13/14 | v1.7 (130/131), v1.8 (08) | inherited |

**Conclusions**

1. R14 is a **revision of the V9 final-submission-candidate lineage dated 2026-10-04 to 10-07**. It is **not** the 2026-09-20 literature-layer submission. The "2026-09-20" label comes only from inherited `docProps/core.xml` metadata, which every docx in the lineage shares. 128 CF-03 had already noted 「時間戳不可靠，以內容判定」.
2. No document in W, REPO or the scanned `C:\NTUST_PAPER\` docx set reports re-segmentation results dated before 2026-10-03. The only pre-10-03 manuscript, the 09-21 camera-ready, has none. So **R14 did not contain an independent re-segmentation analysis**. Its re-segmentation text is the V9.1 sidecar result, imported through the 10-04 patch chain.
3. **Classification: (c).** The figures come from the V9.1 sidecar sensitivity analysis, computed against the frozen V9 primary baseline. That baseline is the 32-core primary analysis that R14 also reports, so "against the R14 baseline" holds in substance. R14 reported the results afterwards. Listing R14 as the *text* locator for these numbers (as 67/68/69/133 do) is accurate. Calling R14 the *analytic* origin, or implying an R14-date provenance, is not.
4. The v1.8 open flag (10_FINAL_STATUS #2, 08_PATCH_LOG L445, 02 L147) can close as **RESOLVED — attribution chain V9.1 → R14 → merge**. There is no conflict.

---

## 4. Corrected provenance wording (attribution only; all numbers unchanged)

These are proposals for the next manuscript revision (v1.8.x/v1.9). Historical files (v1.0–v1.8, 02, 08_PATCH_LOG, 10, 128–137) are **not** edited. Inside the Chinese manuscript text, do not use the bare labels "S1/S2" for the two settings, because the manuscript already uses 補充資料 S1/S2 for supplements. Use 句層級／句與子句層級.

Standard tag (Traditional Chinese), modelled on the existing v1.8 tag at L609:

> 〔來源：V9.1 證據單元重切分敏感度側車分析（V9 套件 `V9_1_SEGMENTATION_SENSITIVITY`，2026-10-03 產生；以凍結之主要分析為比較基準），R14 定稿第 4.6.2–4.6.3 節轉述；觀察值改變與方向改變格數已由兩種設定之文獻層級邊逐列重算核對〕

| Hit | Current attribution | Proposed wording |
|---|---|---|
| v1.8 L1577 (§4.5.2) | implicit R14 | Append the standard tag after 「…分別有 12 與 11 格改變。」. Leave the sentence text unchanged. |
| v1.8 L1600–1601 (Table 4-8 rows) and the table note at L1603 | implicit R14 | Append to the L1603 table note: 「句層級與句與子句層級兩列（含觀察值改變 84/120、85/120 與主測方向改變 12/120、11/120）取自 V9.1 證據單元重切分敏感度側車分析（V9 套件 `V9_1_SEGMENTATION_SENSITIVITY` 之 `S1_120_CELL_RESULTS.csv`、`S2_120_CELL_RESULTS.csv` 與 `SEGMENTATION_CELL_COUNT_DIFF.csv`；2026-10-03），以凍結之主要分析為比較基準；R14 定稿表 7 轉述。」 |
| v1.8 L2264 (§5.4.2) | implicit R14 | After 「84–85/120 格的觀察值發生變化」, insert 「（V9.1 證據單元重切分敏感度側車分析；見第 4.5.2–4.5.3 節）」. |
| v1.8 L2334 (§5.8.3) | implicit R14 | After 「12 與 11 格的主要零模型方向改變」, insert 「（V9.1 側車分析，見第 4.5.2 節）」. |
| v1.8 L2939 (appendix code table, R14 row, column 「在本論文中的角色」) | R14 as the authority for all literature-layer numbers | Append: 「；其中第 3.7.3 節與第 4.5 節之證據單元重切分數值，原始分析出處為 V9.1 證據單元重切分敏感度側車分析（2026-10-03），R14 定稿（2026-10-04 起之修訂）其後納入並轉述。R14 docx 中繼資料之 2026-09-20 修改時間為範本沿用值，不代表成稿日期。」 |
| v1.8 L3008 (appendix, V9 row) | V9 package, human validation | Append: 「；套件內 `V9_1_SEGMENTATION_SENSITIVITY` 為證據單元重切分敏感度側車分析之機器可讀來源（第 3.7.3、4.5 節）」. |
| v1.7 131 L83 | none inline | (historical; no edit) If a current copy is made: 「重切分（V9.1 側車分析，R14 轉述）使 84–85/120 格觀察值改變」. |
| v1.7 133 L32 | "R14 表 6–8" | (historical) Current form: 「R14 表 6–8（轉述 V9.1 側車分析，2026-10-03）」. |
| r14_merge 68 L48–49, 69 L61, audit69.py L77 | "R14（01/02）值" | (historical; correct as a text source) No change. Note for readers: R14 values in these rows originate from V9.1. |
| REPO 02 L147 | "…figures that v1.7/131 attribute to R14" | Current memo wording: "V9.1 is the analytic origin of the 84–85/120 figures. R14 (a post-V9.1 revision, file lineage 2026-10-04…10-07; full hash NOT_RECOVERED, prefix f4252f76…) reports them verbatim. The v1.7/131 → R14 attribution is a correct text locator, not an analytic origin." |
| REPO 08_PATCH_LOG L445; 10_FINAL_STATUS L94 | "open; v1.7/v1.8 attribute to R14 but source is V9.1" | Current memo wording: "RESOLVED in V1.8.1 (13_SEGMENTATION_ATTRIBUTION_FORENSIC): chain V9.1 (computed 2026-10-03) → R14 (reported) → merge. Numbers verified from raw rows. No conflict." |
| W 128 CF-03 | "docx 中繼資料修改時間 2026-09-20" | Current memo wording: "The 2026-09-20 docProps timestamp is inherited template metadata shared by the 09-21 camera-ready and the 10-04…10-07 candidates. R14 content postdates V9.1 (2026-10-03)." |

---

## 5. Residual items

- The full R14 sha256 and its package location (`r14/…`, `r14_merge_bundle_v1_0.zip`, Drive folder `r14_merge_v1_0_20261011`) are **NOT_RECOVERED** in this environment. The identity in §3 stays PROBABLE until the bundle hash is checked against f4252f765c4294fe7c9cda219af6685fa00372613235c228aae29978cddc3ff6.
- The 742/765 changed-parent counts were not recomputed. They depend on parent-level pair-set comparison in `SEGMENT_PROVENANCE_S*.csv` and are summary-level only.
- The docx files under `C:\NTUST_PAPER\` root are outside W and REPO. They were used read-only as provenance evidence and should be added to an input manifest if this evidence is to be committed.

Tools (copies in `claude/r14_merge_v1_8_1_study1_freeze/tools/G/`): `find_84_85.py`, `docx_scan.py`, `docx_text.py`, `recompute_seg.py`, `verify_membership_rule.py`, `count_units.py`; output `recompute_seg_out.json`, `hits.tsv`.
