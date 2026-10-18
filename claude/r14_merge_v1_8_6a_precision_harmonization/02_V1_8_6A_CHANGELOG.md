# 02 — V1.8.6a PRECISION HARMONIZATION + ERRATUM LINEAGE CLOSURE: change log

- **Base:** V1.8.6 `01_V1_8_6_THEORY_INTEGRATED_MANUSCRIPT.md` sha256 `94d41d5682818953912784d0e870d58d1e4c418e7261b619d5c73485dfee82f4` (asserted before patching; file unchanged on disk).
- **Output:** `01_V1_8_6A_MANUSCRIPT.md` sha256 `12eee36a8c1a762a16603deb4f46d2962cc4019a62e443241c082629546d9517`.
- **Method:** `work/PH/patch_v186a.py` — 52 exact old→new replacements, each asserted to match exactly once in V1.8.6 and once at apply time (no layered patches); `work/PH/verify_v186a.py` → `work/PH/verify_out_v186a.json` (ALL_HARD_CHECKS_PASS = True, 52/52).
- **Version character:** wording / precision / lineage closure. Not a new theory version, not an empirical version, not a model revision. Theory status stays PARTIAL; `SUBMISSION_READY = NO`. No git commit/push.
- **Changed V1.8.6 lines:** 45 (5, 11, 15, 27, 31, 89, 93, 95, 105, 130, 150, 151, 152, 160, 180, 190, 222, 332, 399, 407, 667, 755, 779, 1159, 1184, 1186, 1189, 1366, 1797, 2114, 2115, 2268, 2269, 2277, 2322, 2351, 2377, 2397, 2429, 2433, 2461, 2475, 3125, 3241, 3252).

## Hard checks (verify_v186a.py)

| Check | Result |
|---|---|
| source_sha_expected | PASS |
| reverse_replay_reproduces_v186 | PASS |
| changed_lines_subset_of_patched_lines | PASS |
| each_old_once_in_v186 | PASS |
| math_spans_identical_ordered | PASS |
| equation_tags_identical | PASS |
| no_dollar_or_latex_in_new_text | PASS |
| fenced_code_blocks_identical | PASS |
| headings_same_count | PASS |
| headings_only_expected_changes | PASS |
| G_rows_identical_ordered | PASS |
| GM_arrow_tokens_identical | PASS |
| no_new_G_code | PASS |
| table_rows_and_note_identical_ 3-4：G0 | PASS |
| table_v186_heuristic_window_identical_ 3-4：G0 | PASS |
| table_identical_to_59a_ 3-4：G0 | PASS |
| table_rows_and_note_identical_ 3-4A：G | PASS |
| table_v186_heuristic_window_identical_ 3-4A：G | PASS |
| table_identical_to_59a_ 3-4A：G | PASS |
| appendix_C1_C9_identical_to_v186 | PASS |
| appendix_C1_C9_identical_to_59a | PASS |
| P1_P8_bullets_identical_to_v186 | PASS |
| P2_formal_statement_identical_to_59a_and_v186 | PASS |
| P1_P3_P8_identical_to_59a | PASS |
| P2_remark_kept_from_v186 | PASS |
| no_strong_P1_P8_provenance_phrase | PASS |
| standard_phrase_present_ge_4 | PASS |
| study1_primary_phrases_unchanged | PASS |
| study1_tokens_unchanged | PASS |
| no_numeric_token_removed | PASS |
| no_new_citation_keys | PASS |
| no_year_tokens_added_except_2026 | PASS |
| reference_list_identical | PASS |
| no_unverified_anchor_names_added | PASS |
| no_forbidden_phrases | PASS |
| W5_WIDE_367_only_as_sensitivity | PASS |
| W5_162_reported_as_primary | PASS |
| M1_M4_bounded_phrasing_kept | PASS |
| verbatim_S1e_sentence_once | PASS |
| verbatim_sentence_in_3_9_3_item4 | PASS |
| 3_9_3_no_enterprise_decision_interface | PASS |
| first_body_S1e_mention_is_verbatim_sentence | PASS |
| enterprise_decision_interface_kept_5 | PASS |
| technical_model_interface_terms_not_reduced | PASS |
| table_3_4A_header_kept | PASS |
| status_line_V186a | PASS |
| SUBMISSION_READY_NO_count_kept | PASS |
| appendix_D_row_V186a | PASS |
| C10_9_lineage_record | PASS |
| canonical_42_51_unchanged | PASS |
| S1e_packets_unchanged_full_sha | PASS |
| v186_source_file_unchanged_on_disk | PASS |

Numeric tokens added (section numbers, file names, the S1e freeze date 2026-10-14, '16 個項目'): 01×2, 02×1, 03×2, 04×2, 05×2, 1×4, 1-1×1, 16×1, 2×4, 2.13×1, 2026-10-14×1, 256×1, 3×1, 3-10×1, 3-14×1, 3-4×5, 3.10.3×1, 3.12.4×4, 3.12.5×1, 3.13×2, 3.14.3×1, 3.9.3×1, 3.9.6×1, 4-13×1, 4-33×1, 4.10.3×1, 42×3, 5.6×1, 5.7×1, 5.8.10×1, 5.8.4×1, 5.8.5×1, 51×2. Numeric tokens removed: none. Study 1 tokens and primary phrases: identical counts.

## Researcher-decision items closed in this pass

- **RD-1 (terminology)** — CLOSED. Construct = 企業決策機制 (組織決策安排 where organisational configuration is emphasised); S1e coder-facing = 企業決策過程; verbatim S1e sentence at §3.9.3 (4); §3.9.3, Table 3-14, Table 4-13, E6 and §3.9.6 synced; model terms (I1–I5, 介面活化, 資料／介面門檻) and technical interfaces kept. Full inventory in 03.
- **RD-2 (P2 remark)** — KEPT as in V1.8.6 (T07). Checks: P1–P5/P7/P8 bullets identical to V1.8.6 and P1, P3–P8 identical to 59a; P2 formal statement (text up to 「即 DL = 0。」) identical to 59a and V1.8.6; P2 remark identical to V1.8.6. Domain check: the remark is not part of P2's hypothesis or conclusion; it restates the converse-direction remark (misalignment necessary, not sufficient, for DL > 0) with the exact blockability condition of Lemma S (strictly more of at least one pooled resource than the enterprise-preferred plan), which narrows an informal sentence and changes no theorem's domain, hypothesis or conclusion; C.6 keeps the verbatim v2.2 remark and C.10.2 records the supersession. → no STOP.
  Strong provenance phrases replaced in the manuscript by 「P1–P8 的形式陳述與數學語意不變；說明性備註可能含非實質的精確化修訂。」: L5 「命題 P1–P8 的陳述」 (H02), L1159 「上列 P1–P8 的陳述不變」 (H33), L3125 「…P1–P8 與 51 的所有計算數值皆不變」 (H34); the V1.8.6a status line states it once more (H01). Remaining strong phrases: 0.
  Occurrences in the V1.8.6 reports (listed only; reports not edited): 02 l.67 ("P2 formal statement unchanged"; "'P1–P8 text unchanged'"), 02 l.119 (quotes L5 「命題 P1–P8 的陳述」), 02 l.264 (quotes 「上列 P1–P8 的陳述不變」), 02 l.746 (quotes 「…P1–P8 與 51 的所有計算數值皆不變」), 03 l.190 and l.237 (same quotes), 05 l.65 ("P1–P8 statements are identical"), 08 l.99 ("P1–P8 and solver are unaffected"), 09 l.37 ("the P1–P8 scientific results are all unchanged"), 11 l.24 ("The P1–P8 statements are identical"), 12 l.62 ("Revert it if 'P1–P8 unchanged' is meant to include the remarks"). Read with this pass, each means: P1–P8 formal statements and mathematical semantics remain unchanged; explanatory remarks may contain non-substantive precision edits.
- **RD-3 (42 erratum lineage)** — lineage record added: C.10.9 bullet (H50) and Appendix D row (H51) name `42a_CANONICAL_42_ERRATUM_V1_8_6.md` / `04_42A_ERRATUM.md`. 42 and 51 unchanged (0249e7b9… / 37f26a52…). Carrying it into a future canonical 42 stays a researcher decision.
- **RD-5 (outer precision)** — CLOSED; see 05.
- **Citations** — none added (reference list identical; citation-pattern counts identical).

## Summary table

| id | V1.8.6 line | section | category | source |
|---|---|---|---|---|
| H01 | 5 | 稿件狀態 (L5) | VERSION label + RD-2 provenance phrase | common_v186a.txt / orchestrator brief PH item 5; V1.8.6 06 status matrix (theory PARTIAL) |
| H02 | 5 | 稿件狀態 (L5) v1.8.6 sentence | RD-2 provenance phrase | common_v186a.txt / orchestrator brief PH item 2 (RD-2) |
| H03 | 11 | 摘要 (L11) | RD-1 construct term | common_v186a.txt / orchestrator brief PH item 1 |
| H04 | 15 | 摘要 (L15) | RD-1 construct term | common_v186a.txt / orchestrator brief PH item 1 |
| H05 | 27 | Abstract (L27) | RD-1 construct term (EN) | common_v186a.txt / orchestrator brief PH item 1 |
| H06 | 31 | Abstract (L31) | RD-1 construct term (EN) | common_v186a.txt / orchestrator brief PH item 1 |
| H07 | 89 | 1.2.2 (L89) | RD-1 construct term | common_v186a.txt / orchestrator brief PH item 1 |
| H08 | 93 | 1.2.3 (L93) | RD-1 construct term | common_v186a.txt / orchestrator brief PH item 1 |
| H09 | 95 | 1.2.3 (L95) | RD-1 construct term | common_v186a.txt / orchestrator brief PH item 1 |
| H10 | 105 | 1.2.3 證據鏈 (L105) | RD-1 construct term | common_v186a.txt / orchestrator brief PH item 1 |
| H11 | 130 | 1.4 研究問題三 (L130) | RD-1 construct term | common_v186a.txt / orchestrator brief PH item 1 |
| H12 | 160 | 1.5 (L160) | RD-1 construct term | common_v186a.txt / orchestrator brief PH item 1 |
| H13 | 180 | 1.7.2 (L180) | RD-1 construct term | common_v186a.txt / orchestrator brief PH item 1 |
| H14 | 190 | 1.7.3 (L190) | RD-1 construct term | common_v186a.txt / orchestrator brief PH item 1 |
| H15 | 222 | 2.2 (L222) | RD-1 construct term | common_v186a.txt / orchestrator brief PH item 1 |
| H16 | 399 | 2.15 圖 2-1 說明 (L399) | RD-1 construct term (I-label kept in parentheses) | common_v186a.txt / orchestrator brief PH item 1 |
| H17 | 407 | 3.1.1 (L407) | RD-1 construct term | common_v186a.txt / orchestrator brief PH item 1 |
| H18 | 667 | 3.9.1 轉譯程序 (L667) | RD-1 construct definition + terminology note | common_v186a.txt / orchestrator brief PH item 1; Table 3-3 (I1–I5 ↔ M1–M5, unchanged) |
| H19 | 755 | 3.9.3 (4) 編碼工具 (L755) | RD-1 verbatim S1e sentence + coder-facing wording sync | common_v186a.txt / orchestrator brief PH item 1 (verbatim sentence); S1e records (V1_S1E_CURRENT_STATUS.md; S1E_PROCESS_WORDING_CHANGELOG.md; FREEZE_MANIFEST_V1_S1E_PROCESS_WORDING.txt); S1e CODER_1 Q1 wording 「Q1 這段內容是否呈現一個可辨識的企業決策過程？」 (read-only) |
| H20 | 755 | 3.9.3 (4) NONE 定義 (L755) | RD-1 coder-facing wording sync (S1e) | S1e records (V1_S1E_CURRENT_STATUS.md; S1E_PROCESS_WORDING_CHANGELOG.md; FREEZE_MANIFEST_V1_S1E_PROCESS_WORDING.txt); S1e 類別定義 「只有在存在企業決策過程，但其他所有機制…都不適用時才能選」 |
| H21 | 755 | 3.9.3 (4) EVIDENCE_ONLY (L755) | RD-1 coder-facing wording sync (S1e) | S1e records (V1_S1E_CURRENT_STATUS.md; S1E_PROCESS_WORDING_CHANGELOG.md; FREEZE_MANIFEST_V1_S1E_PROCESS_WORDING.txt); S1e 「沒有可辨識的決策過程時，請選「僅屬證據層」」 |
| H22 | 755 | 3.9.3 目前狀態 (L755) | RD-1 V1-design status sync (S1e packet version) | S1e records (V1_S1E_CURRENT_STATUS.md; S1E_PROCESS_WORDING_CHANGELOG.md; FREEZE_MANIFEST_V1_S1E_PROCESS_WORDING.txt) |
| H23 | 779 | 3.9.6 輔助類別 (L779) | RD-1 description sync (§3.9.3 now synced) | S1e records (V1_S1E_CURRENT_STATUS.md; S1E_PROCESS_WORDING_CHANGELOG.md; FREEZE_MANIFEST_V1_S1E_PROCESS_WORDING.txt); V1.8.6 05 O-2 / 12 RD-1 |
| H24 | 1366 | 表 3-14 V1 列 (L1366) | RD-1 V1-design status sync (S1e) | S1e records (V1_S1E_CURRENT_STATUS.md; S1E_PROCESS_WORDING_CHANGELOG.md; FREEZE_MANIFEST_V1_S1E_PROCESS_WORDING.txt) |
| H25 | 1797 | 表 4-13 Q1 列 (L1797) | RD-1 coder-facing wording sync (S1e) | S1e records (V1_S1E_CURRENT_STATUS.md; S1E_PROCESS_WORDING_CHANGELOG.md; FREEZE_MANIFEST_V1_S1E_PROCESS_WORDING.txt) |
| H26 | 2277 | 第五章導言 (L2277) | RD-1 construct term | common_v186a.txt / orchestrator brief PH item 1 |
| H27 | 2322 | 表 5-1 (L2322) | RD-1 construct term | common_v186a.txt / orchestrator brief PH item 1 |
| H28 | 2351 | 5.5 標題 (L2351) | RD-1 construct term (heading) | common_v186a.txt / orchestrator brief PH item 1 |
| H29 | 2461 | 5.9 (L2461) | RD-1 construct term | common_v186a.txt / orchestrator brief PH item 1 |
| H30 | 2475 | 5.10 (L2475) | RD-1 construct term | common_v186a.txt / orchestrator brief PH item 1 |
| H31 | 2475 | 5.10 (L2475) | RD-1 construct term | common_v186a.txt / orchestrator brief PH item 1 |
| H32 | 3252 | 附錄 E6 (L3252) | RD-1 V1-design status sync (S1e) | S1e records (V1_S1E_CURRENT_STATUS.md; S1E_PROCESS_WORDING_CHANGELOG.md; FREEZE_MANIFEST_V1_S1E_PROCESS_WORDING.txt) |
| H33 | 1159 | 3.12.4 分類段 (L1159) | RD-2 provenance phrase | common_v186a.txt / orchestrator brief PH item 2 |
| H34 | 3125 | C.10.9 影響 (L3125) | RD-2 provenance phrase | common_v186a.txt / orchestrator brief PH item 2 |
| H35 | 150 | 表 1-1 研究問題四 (L150) | RD-5 scope condition (DL) | V1.8.6 06 status matrix rows DL (characterization lemma / necessary / sufficient / primitive iff NOT_PROVEN); V1.8.6 12 RD-5 |
| H36 | 151 | 表 1-1 研究問題五 (L151) | RD-5 scope condition (screening; shared capability) | V1.8.6 06 status matrix rows Screening (GS-I identity, GS-1 sufficient, GS-N necessary exact ties, never 'always'); Shared capability (D1/D3 restatement, D6 existence); V1.8.6 12 RD-5 |
| H37 | 152 | 表 1-1 研究問題六 (L152) | RD-5 scope condition (robustness; VOI) | V1.8.6 06 status matrix rows Robustness (vertex-exactness scope); VOI (sequential identification PARTIAL; fixed candidate set); V1.8.6 12 RD-5 |
| H38 | 332 | 2.13 對模型的意涵 (iv) (L332) | RD-5 separate necessary/sufficient | V1.8.6 06 status matrix rows DL necessary / sufficient (W2: misaligned but blockable, DL = 0); V1.8.6 12 RD-5 |
| H39 | 332 | 2.13 對模型的意涵 (vii) (L332) | RD-5 attribution boundary (model-internal vs literature) | V1.8.6 06 status matrix rows DL-1 RESTATEMENT, TYPE C labels; References row (0 new citations); theory pack 10 row 2.1 without the TO-VERIFY analogue clause |
| H40 | 1184 | 表 3-10 Q2 (L1184) | RD-5 scope condition (δ threshold) | V1.8.6 06 status matrix rows Shared capability (D1 B monotone, D3 alignment, D6 existence); theory pack 10 §5 Q2 |
| H41 | 1186 | 表 3-10 Q4 (L1186) | RD-5 separate necessary/sufficient (DL diagnosis) | V1.8.6 06 status matrix rows DL characterization (first-best-relative), primitive iff NOT_PROVEN (W3c); theory pack 10 §5 Q4 |
| H42 | 1189 | 表 3-10 Q7 (L1189) | RD-5 scope condition (vertex exactness) | V1.8.6 06 status matrix row Robustness (vertex-exactness scope); theory pack 10 §5 Q7 |
| H43 | 2114 | 4.10.3 判讀規則 (L2114–2115) | RD-5 scope condition (Lemma R; VOI fixed candidate set) | V1.8.6 06 status matrix rows Robustness, VOI; V1.8.6 12 RD-5 |
| H44 | 2268 | 表 4-33 研究問題五 (L2268) | RD-5 existence vs universal | V1.8.6 06 status matrix row Prop D6 (existence only; never 'generally non-monotone') |
| H45 | 2268 | 表 4-33 研究問題五 (L2268) | RD-5 scope condition (screening) | V1.8.6 06 status matrix rows Screening (GS-I identity; witnesses: 'may have positive screening value under specific…conditions'; never 'always') |
| H46 | 2269 | 表 4-33 研究問題六 (L2269) | RD-5 VOI qualifier | V1.8.6 06 status matrix rows Robustness, VOI (PARTIAL; VOI-greedy optimality open); V1.8.6 12 RD-5 |
| H47 | 2429 | 5.8.4 (L2429) | RD-5 pointer (V1 does not test sufficiency; NONE/AMBIGUOUS) | V1.8.6 06 status matrix row M1–M4 (PARTIAL; minimal sufficiency NOT_PROVEN); theory pack 10 §10 'Also' §5.8.4; V1.8.6 12 RD-5 |
| H48 | 2433 | 5.8.5 (L2433) | RD-5 pointer (information-asymmetry sidecar) | V1.8.6 06 status matrix row Information asymmetry (SIDECAR_DESIGN_ONLY; limitations only); theory pack 10 §10 'Also' §5.8.5 |
| H49 | 2377 | 5.6 企業協調的價值來源 (L2377) | SWEEP necessary-condition precision (AL3 channel) | V1.8.6 06 status matrix row DL necessary conditions (DL-2o/2p under AL3, plus the AL3 channel) |
| H52 | 2397 | 5.7 一般形式貢獻與 AI 特定部分 (L2397) | SWEEP empirical-status qualifier (V7 not run) | V1.8.6 11 m3 (applied only at l.182); V1.8.6 06 status matrix row AI-specificity |
| H50 | 3125 | C.10.9 沿革紀錄（新增 bullet） | VERSION erratum lineage record | common_v186a.txt / orchestrator brief PH item 5; V1.8.6 12 RD-3; theory pack 13 |
| H51 | 3241 | 附錄 D v1.8.6 列 + v1.8.6a 列 | VERSION Appendix D row | common_v186a.txt / orchestrator brief PH item 5 |

## Patches (old → new)

### H01 — 稿件狀態 (L5) (VERSION label + RD-2 provenance phrase)

- source: common_v186a.txt / orchestrator brief PH item 5; V1.8.6 06 status matrix (theory PARTIAL)
- V1.8.6 line: 5

**old**

```text
> **稿件狀態（供人工審閱，2026-10-18）：** 合併碩士論文 v1.8.6 THEORY INTEGRATION CANDIDATE（由 v1.8.5a 修訂；`SUBMISSION_READY = NO`）。v1.8.6 只整合
```

**new**

```text
> **稿件狀態（供人工審閱，2026-10-18）：** 合併碩士論文 V1.8.6a PRECISION HARMONIZATION + ERRATUM LINEAGE CLOSURE（由 v1.8.6 修訂；`SUBMISSION_READY = NO`；THEORY PARTIAL）。v1.8.6a 是用語、精確度與勘誤沿革的收斂，不是新的理論版本、不是實證版本，也不是模型修訂；理論補充包的整體判定維持 PARTIAL。v1.8.6a 只做三件事：(i) 理論構念統一稱為企業決策機制（強調組織配置時稱組織決策安排），先前的「企業決策介面」是較早的理論用語，S1e 問卷的編碼者用語「企業決策過程」對應同一構念；第 3.9.3 節、表 3-14、表 4-13 與附錄 E6 的 V1 設計描述依 S1e 編碼者用語同步，不改變編碼者封包、類別定義或 V1 協定；v2.2 模型的「介面 I1–I5」「介面活化檢驗」「資料／介面門檻」等模型標籤與技術介面用語不變（逐處分類見交付檔 03_TERMINOLOGY_HARMONIZATION_REPORT.md）；(ii) 表 1-1、表 3-10、表 4-33，以及第 2.13、4.10.3、5.6、5.7、5.8.4、5.8.5 節的精確化：只縮小過度主張、補上範圍條件，不新增主張；(iii) Lemma E′ 證明用語勘誤的沿革紀錄（附錄 C.10.9；附錄 D）。v1.8.6a 不改變任何方程、G01–G16、表 3-4／3-4A、Study 1 數值、企業模型 v2.2、求解器 51 或 S1e 編碼者封包，也不新增任何引文；P1–P8 的形式陳述與數學語意不變；說明性備註可能含非實質的精確化修訂。前一版為合併碩士論文 v1.8.6 THEORY INTEGRATION CANDIDATE（由 v1.8.5a 修訂）：v1.8.6 只整合
```

### H02 — 稿件狀態 (L5) v1.8.6 sentence (RD-2 provenance phrase)

- source: common_v186a.txt / orchestrator brief PH item 2 (RD-2)
- V1.8.6 line: 5

**old**

```text
不改變任何方程、命題 P1–P8 的陳述、G01–G16、表 3-4／3-4A、第 3.9.2–3.9.5 節的 V1 設計、Study 1 數值、企業模型 v2.2 或求解器 51，也不新增任何引文；
```

**new**

```text
不改變任何方程、G01–G16、表 3-4／3-4A、第 3.9.2–3.9.5 節的 V1 設計、Study 1 數值、企業模型 v2.2 或求解器 51，也不新增任何引文（P1–P8 的形式陳述與數學語意不變；說明性備註可能含非實質的精確化修訂）；
```

### H03 — 摘要 (L11) (RD-1 construct term)

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 11

**old**

```text
再把低整合接口轉譯為企業必須做出的決策介面，
```

**new**

```text
再把低整合接口轉譯為企業必須做出配置決策的企業決策機制，
```

### H04 — 摘要 (L15) (RD-1 construct term)

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 15

**old**

```text
12 個對應到四個企業決策介面——
```

**new**

```text
12 個對應到四個企業決策機制——
```

### H05 — Abstract (L27) (RD-1 construct term (EN))

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 27

**old**

```text
into decision interfaces that an enterprise must configure,
```

**new**

```text
into enterprise decision mechanisms that an enterprise must configure,
```

### H06 — Abstract (L31) (RD-1 construct term (EN))

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 31

**old**

```text
map onto four enterprise decision interfaces—
```

**new**

```text
map onto four enterprise decision mechanisms—
```

### H07 — 1.2.2 (L89) (RD-1 construct term)

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 89

**old**

```text
而轉譯成立之後，該介面是否真的在某一企業中改變決策
```

**new**

```text
而轉譯成立之後，該企業決策機制是否真的在某一企業中改變決策
```

### H08 — 1.2.3 (L93) (RD-1 construct term)

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 93

**old**

```text
**第一，文獻低整合配對可收斂為少數企業決策介面。**
```

**new**

```text
**第一，文獻低整合配對可收斂為少數企業決策機制。**
```

### H09 — 1.2.3 (L95) (RD-1 construct term)

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 95

**old**

```text
**第二，這四個介面在企業中不是彼此獨立的部門問題
```

**new**

```text
**第二，這四個機制在企業中不是彼此獨立的部門問題
```

### H10 — 1.2.3 證據鏈 (L105) (RD-1 construct term)

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 105

**old**

```text
→ 企業決策介面 M1–M4（M5 為跨期擴充）
```

**new**

```text
→ 企業決策機制 M1–M4（M5 為跨期擴充）
```

### H11 — 1.4 研究問題三 (L130) (RD-1 construct term)

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 130

**old**

```text
分別指向哪些企業必須做出的決策介面與模型元素？此一轉譯在獨立編碼下是否成立？在企業證據下，哪些介面真正形成企業決策問題？
```

**new**

```text
分別指向哪些企業必須做出配置決策的企業決策機制與模型元素？此一轉譯在獨立編碼下是否成立？在企業證據下，哪些轉譯後的機制真正形成企業決策問題？
```

### H12 — 1.5 (L160) (RD-1 construct term)

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 160

**old**

```text
先經研究者逐格轉譯為企業決策介面與模型元素
```

**new**

```text
先經研究者逐格轉譯為企業決策機制與模型元素
```

### H13 — 1.7.2 (L180) (RD-1 construct term)

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 180

**old**

```text
本研究建立文獻網絡低連結與企業決策介面之間的中介層
```

**new**

```text
本研究建立文獻網絡低連結與企業決策機制之間的中介層
```

### H14 — 1.7.3 (L190) (RD-1 construct term)

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 190

**old**

```text
也被轉譯為企業決策介面，它仍只有
```

**new**

```text
也被轉譯為企業決策機制，它仍只有
```

### H15 — 2.2 (L222) (RD-1 construct term)

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 222

**old**

```text
第 3.9 節把文獻低整合轉譯為企業介面時
```

**new**

```text
第 3.9 節把文獻低整合轉譯為企業決策機制時
```

### H16 — 2.15 圖 2-1 說明 (L399) (RD-1 construct term (I-label kept in parentheses))

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 399

**old**

```text
第一，G01–G16 透過四個介面進入模型
```

**new**

```text
第一，G01–G16 透過四個企業決策機制（M1–M4；模型標籤為介面 I1–I4）進入模型
```

### H17 — 3.1.1 (L407) (RD-1 construct term)

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 407

**old**

```text
把穩健的功能低整合轉譯為企業必須做出的決策介面，建立
```

**new**

```text
把穩健的功能低整合轉譯為企業必須做出配置決策的企業決策機制，建立
```

### H18 — 3.9.1 轉譯程序 (L667) (RD-1 construct definition + terminology note)

- source: common_v186a.txt / orchestrator brief PH item 1; Table 3-3 (I1–I5 ↔ M1–M5, unchanged)
- V1.8.6 line: 667

**old**

```text
**一個缺口是否指向一個企業必須做出的配置決策（企業決策介面）**。若多個缺口指向同一介面，就合併；若沒有介面，就留在證據層。
```

**new**

```text
**一個缺口是否指向一個企業必須做出的配置決策（企業決策機制）**。若多個缺口指向同一介面，就合併；若沒有介面，就留在證據層。本稿的理論構念統一稱為企業決策機制（強調組織配置時稱組織決策安排）；先前版本與表 3-4A 欄名所用的「企業決策介面」是較早的理論用語，與企業決策機制指同一構念，不是第三個構念。下表、表 3-4 與表 3-4A 的「介面 I1–I5」，以及第 3.12.5 節的「介面活化檢驗」，沿用構念凍結文件與 v2.2 模型的標籤：介面 I1–I5 依序對應機制 M1–M5，標示各機制在模型中的位置，也不是另一個構念；它們與第 3.10.3 節資料門檻中的「共用介面」，以及使用者介面、API 或系統串接介面等技術介面無關。
```

### H19 — 3.9.3 (4) 編碼工具 (L755) (RD-1 verbatim S1e sentence + coder-facing wording sync)

- source: common_v186a.txt / orchestrator brief PH item 1 (verbatim sentence); S1e records (V1_S1E_CURRENT_STATUS.md; S1E_PROCESS_WORDING_CHANGELOG.md; FREEZE_MANIFEST_V1_S1E_PROCESS_WORDING.txt); S1e CODER_1 Q1 wording 「Q1 這段內容是否呈現一個可辨識的企業決策過程？」 (read-only)
- V1.8.6 line: 755

**old**

```text
(4) **編碼工具（Q1–Q5）。** Q1 判斷該配對是否對應可辨識的企業決策介面（YES、NO、UNCERTAIN）；
```

**new**

```text
(4) **編碼工具（Q1–Q5）。** 為降低獨立編碼者的理解負擔，S1e 問卷採用『企業決策過程』作為 coder-facing wording；其所對應的理論構念仍為本文所稱之企業決策機制／組織決策安排，並不構成另一個不同構念。Q1 判斷該配對是否呈現可辨識的企業決策過程（YES、NO、UNCERTAIN）；
```

### H20 — 3.9.3 (4) NONE 定義 (L755) (RD-1 coder-facing wording sync (S1e))

- source: S1e records (V1_S1E_CURRENT_STATUS.md; S1E_PROCESS_WORDING_CHANGELOG.md; FREEZE_MANIFEST_V1_S1E_PROCESS_WORDING.txt); S1e 類別定義 「只有在存在企業決策過程，但其他所有機制…都不適用時才能選」
- V1.8.6 line: 755

**old**

```text
NONE 的定義是：存在可辨識的企業決策介面，但 M1–M4
```

**new**

```text
NONE 的定義是：存在可辨識的企業決策過程，但 M1–M4
```

### H21 — 3.9.3 (4) EVIDENCE_ONLY (L755) (RD-1 coder-facing wording sync (S1e))

- source: S1e records (V1_S1E_CURRENT_STATUS.md; S1E_PROCESS_WORDING_CHANGELOG.md; FREEZE_MANIFEST_V1_S1E_PROCESS_WORDING.txt); S1e 「沒有可辨識的決策過程時，請選「僅屬證據層」」
- V1.8.6 line: 755

**old**

```text
沒有獨立的介面時也不使用 NONE（改用 EVIDENCE_ONLY）
```

**new**

```text
沒有可辨識的企業決策過程時也不使用 NONE（改用 EVIDENCE_ONLY）
```

### H22 — 3.9.3 目前狀態 (L755) (RD-1 V1-design status sync (S1e packet version))

- source: S1e records (V1_S1E_CURRENT_STATUS.md; S1E_PROCESS_WORDING_CHANGELOG.md; FREEZE_MANIFEST_V1_S1E_PROCESS_WORDING.txt)
- V1.8.6 line: 755

**old**

```text
目前狀態：協定已於 S1 凍結（人類編碼前），封包已備妥待發送，人類編碼尚未執行，結果待完成。

EA-X（解釋可用性）
```

**new**

```text
目前狀態：協定已於 S1 凍結（人類編碼前）；編碼者封包其後改為 S1e 版（2026-10-14 以 SHA-256 凍結，經審閱核可、可發送；只改編碼者用語與答案表版面，16 個項目、各編碼者的隨機順序、類別定義、Q1／Q2 一致性規則與 Q3–Q5 的語意不變，Q1 的判斷內容不變；S1d 保留為歷史版本，不覆寫），人類編碼尚未執行，結果待完成。

EA-X（解釋可用性）
```

### H23 — 3.9.6 輔助類別 (L779) (RD-1 description sync (§3.9.3 now synced))

- source: S1e records (V1_S1E_CURRENT_STATUS.md; S1E_PROCESS_WORDING_CHANGELOG.md; FREEZE_MANIFEST_V1_S1E_PROCESS_WORDING.txt); V1.8.6 05 O-2 / 12 RD-1
- V1.8.6 line: 779

**old**

```text
存在可辨識的企業決策過程（S1e 編碼者材料的用語；第 3.9.3 節沿用 S1d 的「企業決策介面」，兩者指同一判斷，S1e 只改編碼者用語與答案表版面，不改類別定義）
```

**new**

```text
存在可辨識的企業決策過程（S1e 編碼者材料的用語，第 3.9.3 節已同步；S1d 與本稿先前版本使用「企業決策介面」，兩者指同一判斷，對應的理論構念都是企業決策機制；S1e 只改編碼者用語與答案表版面，不改類別定義）
```

### H24 — 表 3-14 V1 列 (L1366) (RD-1 V1-design status sync (S1e))

- source: S1e records (V1_S1E_CURRENT_STATUS.md; S1E_PROCESS_WORDING_CHANGELOG.md; FREEZE_MANIFEST_V1_S1E_PROCESS_WORDING.txt)
- V1.8.6 line: 1366

**old**

```text
協定與封包已於 S1 凍結，人類編碼尚未執行）
```

**new**

```text
協定與封包已於 S1 凍結；現行編碼者封包為 S1e 版〔編碼者用語「企業決策過程」，只改用語與答案表版面，類別定義不變〕，人類編碼尚未執行）
```

### H25 — 表 4-13 Q1 列 (L1797) (RD-1 coder-facing wording sync (S1e))

- source: S1e records (V1_S1E_CURRENT_STATUS.md; S1E_PROCESS_WORDING_CHANGELOG.md; FREEZE_MANIFEST_V1_S1E_PROCESS_WORDING.txt)
- V1.8.6 line: 1797

**old**

```text
| Q1 企業決策介面 |
```

**new**

```text
| Q1 企業決策過程（S1e 編碼者用語；理論構念為企業決策機制） |
```

### H26 — 第五章導言 (L2277) (RD-1 construct term)

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 2277

**old**

```text
再討論從文獻低整合到企業決策介面的轉譯（第 5.5 節）
```

**new**

```text
再討論從文獻低整合到企業決策機制的轉譯（第 5.5 節）
```

### H27 — 表 5-1 (L2322) (RD-1 construct term)

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 2322

**old**

```text
| 企業決策介面 | 研究者轉譯經獨立的人類編碼驗證 |
```

**new**

```text
| 企業決策機制 | 研究者轉譯經獨立的人類編碼驗證 |
```

### H28 — 5.5 標題 (L2351) (RD-1 construct term (heading))

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 2351

**old**

```text
## 5.5 從低整合接口到企業決策介面
```

**new**

```text
## 5.5 從低整合接口到企業決策機制
```

### H29 — 5.9 (L2461) (RD-1 construct term)

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 2461

**old**

```text
後者在企業中檢驗轉譯後的介面是否改變決策。
```

**new**

```text
後者在企業中檢驗轉譯後的機制是否改變決策。
```

### H30 — 5.10 (L2475) (RD-1 construct term)

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 2475

**old**

```text
本論文把 16 組主要穩健不足呈現轉譯為企業決策介面，
```

**new**

```text
本論文把 16 組主要穩健不足呈現轉譯為企業決策機制，
```

### H31 — 5.10 (L2475) (RD-1 construct term)

- source: common_v186a.txt / orchestrator brief PH item 1
- V1.8.6 line: 2475

**old**

```text
評估與保證四個介面，2 組歸入
```

**new**

```text
評估與保證四個機制，2 組歸入
```

### H32 — 附錄 E6 (L3252) (RD-1 V1-design status sync (S1e))

- source: S1e records (V1_S1E_CURRENT_STATUS.md; S1E_PROCESS_WORDING_CHANGELOG.md; FREEZE_MANIFEST_V1_S1E_PROCESS_WORDING.txt)
- V1.8.6 line: 3252

**old**

```text
編碼者只收到遮蔽 G 編號的盲編封包並填寫七項聲明；封包直接寄送，不經公開儲存庫 |
```

**new**

```text
編碼者只收到遮蔽 G 編號的盲編封包（現行為 S1e 版；編碼者用語「企業決策過程」，對應理論構念企業決策機制；S1d 保留為歷史版本）並填寫七項聲明；封包直接寄送，不經公開儲存庫 |
```

### H33 — 3.12.4 分類段 (L1159) (RD-2 provenance phrase)

- source: common_v186a.txt / orchestrator brief PH item 2
- V1.8.6 line: 1159

**old**

```text
上列 P1–P8 的陳述不變。
```

**new**

```text
上列 P1–P8 的形式陳述與數學語意不變；說明性備註可能含非實質的精確化修訂。
```

### H34 — C.10.9 影響 (L3125) (RD-2 provenance phrase)

- source: common_v186a.txt / orchestrator brief PH item 2
- V1.8.6 line: 3125

**old**

```text
Lemma E′ 的陳述、所有方程、目標、可行集合、P1–P8 與 51 的所有計算數值皆不變：
```

**new**

```text
Lemma E′ 的陳述、所有方程、目標、可行集合與 51 的所有計算數值皆不變（P1–P8 的形式陳述與數學語意不變；說明性備註可能含非實質的精確化修訂）：
```

### H35 — 表 1-1 研究問題四 (L150) (RD-5 scope condition (DL))

- source: V1.8.6 06 status matrix rows DL (characterization lemma / necessary / sufficient / primitive iff NOT_PROVEN); V1.8.6 12 RD-5
- V1.8.6 line: 150

**old**

```text
| 3.11、3.12 | 4.10 | 模型完成；合成驗證完成（僅合成）；實證待完成（V7） |
```

**new**

```text
| 3.11、3.12 | 4.10 | 模型完成；模型內形式結果（第 3.12.4 節；附錄 C.10）：DL 為零的首佳相對刻畫（Lemma DL-1，為 Lemma E′ 之重述）、DL 為正的必要條件（AL3 且精確平手下，Cor DL-2o／2p）與充分條件（唯一首佳下，Cor DL-3），沒有不依賴首佳解的充要刻畫；合成驗證完成（僅合成）；實證待完成（V7） |
```

### H36 — 表 1-1 研究問題五 (L151) (RD-5 scope condition (screening; shared capability))

- source: V1.8.6 06 status matrix rows Screening (GS-I identity, GS-1 sufficient, GS-N necessary exact ties, never 'always'); Shared capability (D1/D3 restatement, D6 existence); V1.8.6 12 RD-5
- V1.8.6 line: 151

**old**

```text
| 3.10.4、3.11–3.13 | 4.10 | 模型完成；合成驗證完成（僅合成；v2.4 部分為候選）；實證待完成（V7） |
```

**new**

```text
| 3.10.4、3.11–3.13 | 4.10 | 模型完成；模型內形式結果：治理篩選為條件性結果（恆等式 GS-I、充分條件 Prop GS-1、精確平手下的必要條件 Thm GS-N；不是一般性質），共享能力重用在 B 中單調（Thm D1，P4 之重述）、在 C 中以帳本對齊為充分條件（Thm D3，重述），否則存在建置區域不是區間的實例（Prop D6，存在性結果）；合成驗證完成（僅合成；v2.4 部分為候選）；實證待完成（V7） |
```

### H37 — 表 1-1 研究問題六 (L152) (RD-5 scope condition (robustness; VOI))

- source: V1.8.6 06 status matrix rows Robustness (vertex-exactness scope); VOI (sequential identification PARTIAL; fixed candidate set); V1.8.6 12 RD-5
- V1.8.6 line: 152

**old**

```text
| 3.13、3.14 | 4.8、4.10 | 模型完成；合成驗證完成（僅合成）；實證待完成（V7） |
```

**new**

```text
| 3.13、3.14 | 4.8、4.10 | 模型完成；頂點精確性只限 Model B（及 A+）的整個 portfolio（Thm R1，為 Lemma R 之重述）；VOI 的次序只對固定候選集合成立（Prop E.1、E.2），序列識別性質為 PARTIAL；合成驗證完成（僅合成）；實證待完成（V7） |
```

### H38 — 2.13 對模型的意涵 (iv) (L332) (RD-5 separate necessary/sufficient)

- source: V1.8.6 06 status matrix rows DL necessary / sufficient (W2: misaligned but blockable, DL = 0); V1.8.6 12 RD-5
- V1.8.6 line: 332

**old**

```text
(iv) 跨層衝突以帳本對齊條件 (AL1)–(AL4) 檢驗；對齊時授權損失為零（P2）。
```

**new**

```text
(iv) 跨層衝突以帳本對齊條件 (AL1)–(AL4) 檢驗；對齊時授權損失為零（P2）——對齊是授權損失為零的充分而非必要條件，不對齊也不足以使授權損失為正（第 3.12.4 節）。
```

### H39 — 2.13 對模型的意涵 (vii) (L332) (RD-5 attribution boundary (model-internal vs literature))

- source: V1.8.6 06 status matrix rows DL-1 RESTATEMENT, TYPE C labels; References row (0 new citations); theory pack 10 row 2.1 without the TO-VERIFY analogue clause
- V1.8.6 line: 332

**old**

```text
輸出 ROBUST／CONDITIONAL／FRAGILE／UNIDENTIFIED。

## 2.14
```

**new**

```text
輸出 ROBUST／CONDITIONAL／FRAGILE／UNIDENTIFIED。(vii) 第 3.12.4 節與附錄 C.10 的授權損失、治理篩選與共享能力重用結果，是本研究在完全資訊、固定參數下的模型內結果（其中 Lemma DL-1 為 Lemma E′ 於首佳解之重述），不是上述文獻的主張。

## 2.14
```

### H40 — 表 3-10 Q2 (L1184) (RD-5 scope condition (δ threshold))

- source: V1.8.6 06 status matrix rows Shared capability (D1 B monotone, D3 alignment, D6 existence); theory pack 10 §5 Q2
- V1.8.6 line: 1184

**old**

```text
| 損益兩平固定成本 `F_c^†`、重用門檻 `δ^†` | 五 |
```

**new**

```text
| 損益兩平固定成本 `F_c^†`、重用門檻 `δ^†`（B 中唯一；C 中帳本對齊時唯一，否則報告集合值的建置區域與平手慣例） | 五 |
```

### H41 — 表 3-10 Q4 (L1186) (RD-5 separate necessary/sufficient (DL diagnosis))

- source: V1.8.6 06 status matrix rows DL characterization (first-best-relative), primitive iff NOT_PROVEN (W3c); theory pack 10 §5 Q4
- V1.8.6 line: 1186

**old**

```text
| DL 及其來源分解 | 四 |
```

**new**

```text
| DL 及其來源分解（報告不成立的對齊條件，以及存在不可阻擋偏離的首佳計畫；成對檢查不足以判定 DL 的正負，W3c） | 四 |
```

### H42 — 表 3-10 Q7 (L1189) (RD-5 scope condition (vertex exactness))

- source: V1.8.6 06 status matrix row Robustness (vertex-exactness scope); theory pack 10 §5 Q7
- V1.8.6 line: 1189

**old**

```text
| 元素層級穩健性分類、MaxRegret | 六 |
```

**new**

```text
| 元素層級穩健性分類（以涵蓋率報告）、MaxRegret（頂點精確只限 Model B 及 A+ 的整個 portfolio） | 六 |
```

### H43 — 4.10.3 判讀規則 (L2114–2115) (RD-5 scope condition (Lemma R; VOI fixed candidate set))

- source: V1.8.6 06 status matrix rows Robustness, VOI; V1.8.6 12 RD-5
- V1.8.6 line: 2114

**old**

```text
  - 只有 Model B 的整體 portfolio 有精確證書（Lemma R）。元素層級與 Model C 只報涵蓋率，不稱「對所有 θ」。
  - VOI 同時報頂點版（可能高估）與網格版。
```

**new**

```text
  - 只有 Model B（及 A+）的整體 portfolio 在第 3.13 節所列前提 (R-a)–(R-e) 下有精確證書（Lemma R）。元素層級（除 Prop R4 的情形）與 Model C 只報涵蓋率，不稱「對所有 θ」。
  - VOI 同時報頂點版（可能高估）與網格版；兩者只在固定候選集合（第一批登記時的 ROBUSTLY_FEASIBLE 集合）下為真值的上界，重算候選集合只作次要診斷並標 `CANDIDATE_SET_EXPANDED`（第 3.14.3 節）。
```

### H44 — 表 4-33 研究問題五 (L2268) (RD-5 existence vs universal)

- source: V1.8.6 06 status matrix row Prop D6 (existence only; never 'generally non-monotone')
- V1.8.6 line: 2268

**old**

```text
共享重用效果在雙層且帳本不對齊時可使建置區域為集合值；
```

**new**

```text
共享重用效果在雙層且帳本不對齊時可使建置區域為集合值（存在性結果，Prop D6）；
```

### H45 — 表 4-33 研究問題五 (L2268) (RD-5 scope condition (screening))

- source: V1.8.6 06 status matrix rows Screening (GS-I identity; witnesses: 'may have positive screening value under specific…conditions'; never 'always')
- V1.8.6 line: 2268

**old**

```text
P8 在雙層且帳本不對齊時要求可具篩選價值；
```

**new**

```text
P8 在雙層且帳本不對齊時要求可具篩選價值（只在特定的錯位與可分離性條件下；篩選價值不超過較寬鬆要求下的授權損失，恆等式 GS-I）；
```

### H46 — 表 4-33 研究問題六 (L2269) (RD-5 VOI qualifier)

- source: V1.8.6 06 status matrix rows Robustness, VOI (PARTIAL; VOI-greedy optimality open); V1.8.6 12 RD-5
- V1.8.6 line: 2269

**old**

```text
研究設計：只有 Model B 的整體 portfolio 具精確穩健性證書（Lemma R）；元素層級與 Model C 只報涵蓋率；VOI 同時報頂點版與網格版。
```

**new**

```text
研究設計：只有 Model B（及 A+）的整體 portfolio 具精確穩健性證書（Lemma R；前提見第 3.13 節）；元素層級（除 Prop R4 的情形）與 Model C 只報涵蓋率；VOI 同時報頂點版（可能高估）與網格版，兩者只在固定候選集合下為真值的上界（Prop E.1、E.2），依 VOI 排序之量測順序的最適性未證明。
```

### H47 — 5.8.4 (L2429) (RD-5 pointer (V1 does not test sufficiency; NONE/AMBIGUOUS))

- source: V1.8.6 06 status matrix row M1–M4 (PARTIAL; minimal sufficiency NOT_PROVEN); theory pack 10 §10 'Also' §5.8.4; V1.8.6 12 RD-5
- V1.8.6 line: 2429

**old**

```text
文獻分析的人工稽核（第 3.7 節）驗證的是語意證據與功能分類，不能替代 V1。
```

**new**

```text
文獻分析的人工稽核（第 3.7 節）驗證的是語意證據與功能分類，不能替代 V1。V1 檢驗的是 G→M 對應在凍結類別定義下的編碼者間可詮釋性，不檢驗 M1–M4 的非冗餘性或充分性；NONE 是涵蓋缺口的訊號，AMBIGUOUS 用於證據不足或兩類並列的類別邊界情形，兩者的有無都不能建立或否定 M1–M4 的充分性（第 3.9.6 節）。
```

### H48 — 5.8.5 (L2433) (RD-5 pointer (information-asymmetry sidecar))

- source: V1.8.6 06 status matrix row Information asymmetry (SIDECAR_DESIGN_ONLY; limitations only); theory pack 10 §10 'Also' §5.8.5
- V1.8.6 line: 2433

**old**

```text
只有取得「企業與部門知道不同參數」的證據，才執行資訊不對稱的敏感度分析。
```

**new**

```text
只有取得「企業與部門知道不同參數」的證據，才執行資訊不對稱的敏感度分析；資訊不對稱的側車目前只是設計（SIDECAR_DESIGN_ONLY），不修改 v2.2，其完全資訊特例重現 P3（第 5.8.10 節）。
```

### H49 — 5.6 企業協調的價值來源 (L2377) (SWEEP necessary-condition precision (AL3 channel))

- source: V1.8.6 06 status matrix row DL necessary conditions (DL-2o/2p under AL3, plus the AL3 channel)
- V1.8.6 line: 2377

**old**

```text
DL 只在帳本不對齊且 envelope 無法分離不利配置時為正。
```

**new**

```text
DL 為正的必要條件是帳本不對齊：在 AL3 成立時，還須有 envelope 無法分離的不利配置（Cor DL-2o／2p），AL3 不成立時部門專屬限制本身即可使 DL 為正（第 3.12.4 節）；這些都只是必要條件，不是充分條件。
```

### H52 — 5.7 一般形式貢獻與 AI 特定部分 (L2397) (SWEEP empirical-status qualifier (V7 not run))

- source: V1.8.6 11 m3 (applied only at l.182); V1.8.6 06 status matrix row AI-specificity
- V1.8.6 line: 2397

**old**

```text
評估保證與 AI 治理的語意、AI 特定的實證參數化，以及後續的企業應用（第 1.7.2 節）。
```

**new**

```text
評估保證與 AI 治理的語意、AI 特定的實證參數化（V7，尚未執行），以及後續的企業應用（第 1.7.2 節）。
```

### H50 — C.10.9 沿革紀錄（新增 bullet） (VERSION erratum lineage record)

- source: common_v186a.txt / orchestrator brief PH item 5; V1.8.6 12 RD-3; theory pack 13
- V1.8.6 line: 3125

**old**

```text
不依賴證明中 `x` 的特定選法。

```

**new**

```text
不依賴證明中 `x` 的特定選法。
- **沿革紀錄（v1.8.6a）。** 本勘誤的沿革紀錄為勘誤檔 `42a_CANONICAL_42_ERRATUM_V1_8_6.md`（v1.8.6a 交付檔 `04_42A_ERRATUM.md`）：它只記錄上述悲觀情形的證明用語修正，不修改企業模型規格 v2.2（42）與求解器 51 本身，也不改變任何數值；是否在下一個正式版本納入此修正，仍由研究者決定（附錄 D）。

```

### H51 — 附錄 D v1.8.6 列 + v1.8.6a 列 (VERSION Appendix D row)

- source: common_v186a.txt / orchestrator brief PH item 5
- V1.8.6 line: 3241

**old**

```text
| 合併論文 v1.8.6（理論整合版；v1.8.5a 為修訂底稿） | 本稿 |
```

**new**

```text
| 合併論文 v1.8.6（理論整合版；v1.8.5a 為修訂底稿） | v1.8.6a 的修訂底稿（已保存；未覆寫） |
| v1.8.6a／01–05 | — | `01_V1_8_6A_MANUSCRIPT.md`（另有 `02_V1_8_6A_CHANGELOG.md`、`03_TERMINOLOGY_HARMONIZATION_REPORT.md`、`04_42A_ERRATUM.md`、`05_OUTER_SECTION_PRECISION_AUDIT.md`）；勘誤沿革紀錄 `42a_CANONICAL_42_ERRATUM_V1_8_6.md` | 合併論文 v1.8.6a（PRECISION HARMONIZATION + ERRATUM LINEAGE CLOSURE：用語、精確度與勘誤沿革的收斂；不是新的理論版本、實證版本或模型修訂；v1.8.6 為修訂底稿） | 本稿；附錄 C.10.9 |
```

