# 03 — v1.8.5a (59a) → v1.8.6 (01): segment diff summary

## Summary counts

| item | value |
|---|---|
| patches | 50 |
| line count 59a → 01 | 3136 → 3304 |
| 59a lines changed in place | 16 |
| new lines inserted | 170 |
| 59a lines replaced by multi-line segments (no content deleted; see segments) | 2 |
| characters 59a → 01 | 306992 → 334440 |
| headings added | 13 (existing 182 preserved in order) |
| captions added | **表 4-20D：理論補充的構造例（SIMULATED_ONLY；構造例，非證明）** |
| math spans ($$ / inline $) | [18, 18] / [31, 31] (identical: True) |
| G01–G16 table rows | [36, 36] (identical: True) |
| citation-pattern counts main text (before/after) | [[205, 205], [119, 119], [109, 109], [21, 21], [0, 0]] |
| ALL_HARD_CHECKS_PASS | True |

## Hard checks

- source_sha_expected: True
- changed_lines_subset_of_patched_lines: True
- reverse_replay_reproduces_59a: True
- math_spans_identical_ordered: True
- equation_tags_identical: True
- no_dollar_or_latex_in_patch_new_text: True
- fenced_code_blocks_identical: True
- existing_headings_preserved_in_order: True
- headings_added_exactly_expected: True
- no_heading_removed: True
- captions_only_4_20D_added: True
- G_rows_identical_ordered: True
- GM_arrow_tokens_identical: True
- no_G17_or_new_G_code: True
- section_3_9_1_identical: True
- section_3_9_2_tables_3_4_3_4A_identical: True
- section_3_9_3_V1_design_identical: True
- section_3_9_4_identical: True
- section_3_9_5_identical: True
- section_3_11_x_identical: True
- section_3_11_2_identical: True
- section_3_11_3_identical: True
- section_3_11_4_identical: True
- section_3_12_1_identical: True
- section_3_12_2_identical: True
- section_3_12_3_identical: True
- section_3_12_5_identical: True
- section_3_12_7_identical: True
- section_4_1_to_4_8_identical: True
- section_4_10_identical: True
- section_4_11_identical: True
- section_chapter2_identical: True
- section_3_1_to_3_8_identical: True
- section_5_1_to_5_5_identical: True
- section_5_8_1_to_5_8_9_identical: True
- section_references_identical: True
- section_appendix_A_B_identical: True
- section_appendix_E_F_except_E51_identical: True
- table_identical_ 3-4：G0: True
- table_identical_ 3-4A：G: True
- appendix_C1_C9_verbatim: True
- P1_P3_to_P8_bullets_identical: True
- P2_formal_statement_identical: True
- P2_only_remark_changed_by_T07: True
- study1_primary_phrases_unchanged: True
- study1_tokens_unchanged: True
- numeric_patch_sum_matches_doc: True
- numeric_added_all_traceable: True
- numeric_removed_only_status_date: True
- no_new_citation_keys_main_text: True
- no_new_citation_keys_whole_document: True
- no_year_tokens_added_except_status_date: True
- reference_list_identical: True
- no_unverified_anchor_names_added: True
- no_forbidden_phrases_in_01: True
- W5_WIDE_367_only_as_sensitivity: True
- W5_162_reported_as_primary: True
- every_充要_in_new_text_scoped_or_negated: True
- every_positive_iff_scoped_to_unique_first_best: True
- 4_9_1_footnote_present: True
- 4_9_1_ABC_present: True
- 4_9_1_W1_W7_rows: True
- governance_sentence_present: True
- M1_M4_scope_sentence_TA_MAJOR1: True
- synthetic_analytic_counterexample_label: True
- W_IA_NDV_not_in_chapter4: True
- status_line_L5_v186: True
- SUBMISSION_READY_NO_kept: True
- erratum_present_and_C2_verbatim: True
- canonical_42_51_unchanged: True
- S1e_packets_unchanged: True

## Protected-region verification

- Math spans identical (ordered): True; equation tags identical: True; fenced blocks identical: True.
- Existing headings preserved in order: True; added headings: 13.
- §3.9.1–§3.9.5 byte-identical (incl. Tables 3-4/3-4A and V1 design §3.9.3): True; all M1–M4 scope sentences were placed in new §3.9.6 (no sentence added inside §3.9.2–§3.9.5).
- P1, P3–P8 bullets identical: True; P2 formal statement identical: True; P2 remark changed only by T07: True.
  - P2 remark old: `不對齊是 DL > 0 的必要而非充分條件：若不利企業的配置需要池化資源，企業可以 envelope 阻止。`
  - P2 remark new: `不對齊是 DL > 0 的必要而非充分條件：若不利企業的配置在至少一項池化資源上需要多於企業偏好配置的用量，企業可以 envelope 阻止（envelope 可分離性的精確條件見 Lemma S，附錄 C.10.2）。`
- Appendix C.1–C.9 verbatim: True; Chapter 2, §3.1–3.8, §3.11, §3.12.1–3.12.3/3.12.5/3.12.7, §4.1–4.8, §4.10, §4.11, §5.1–5.5, §5.8.1–5.8.9, references, Appendices A/B/E/F identical: True.
- Study 1 phrases/tokens unchanged: True / True. Canonical 42/51 unchanged: True (42 0249e7b9…, 51 37f26a52…). S1e packets unchanged: True.
- No new citation keys (main text and whole document, 5 reference-like patterns; reference list identical; no unverified anchor names): True / True / True / True.
- Forbidden-phrase grep on 01 (minimal sufficient, DL>0 iff, governance always, generally non-monotone, enterprise-evidence-for-synthetic, FULLY_VALIDATED): {'minimal sufficient (claim)': {}, 'DL>0 iff': {}, 'governance always': {}, 'generally non-monotone': {}, 'enterprise evidence for synthetic': {}, 'FULLY_VALIDATED': {}}; 59a had: {'minimal sufficient (claim)': {'最小充分': 1}, 'DL>0 iff': {}, 'governance always': {}, 'generally non-monotone': {}, 'enterprise evidence for synthetic': {}, 'FULLY_VALIDATED': {}}.
- Every '充要' sentence in new text is scoped/negated: True; every 'X 為正若且唯若' sentence is scoped to a unique first best: True.
- 367/400 only as sensitivity: True; 162/400 as primary: True.

## Numeric tokens

### Added (token: count — source)

- `0`: +74 — witness values (W1–W7, W3b DL^opt = 0, W2/W1 DL = 0, W6e MMR 1→0, interval endpoints) and model notation (k = 0, ε_tie = 0, a(x)=0 cases) — theory pack r14_merge_q1_theory_upgrade_v1 02–07, 09
- `0,3`: +5 — W5 region [0,3) — theory pack r14_merge_q1_theory_upgrade_v1 04 §5.1, §6
- `0,4`: +1 — W5_WIDE region [0,4) — theory pack r14_merge_q1_theory_upgrade_v1 04 §6
- `0.4`: +3 — T-SEN-3 / W7 FRAGILE interval (0.4, 0.6) (already in 59a l.1271) — theory pack r14_merge_q1_theory_upgrade_v1 06 App A
- `0.5`: +2 — W6 analytic oracle true VOI 0.5 (already in 59a l.1277, 1917) — theory pack r14_merge_q1_theory_upgrade_v1 05 §6(3)
- `0.6`: +4 — T-SEN-3 / W7 interval endpoint and y0 value 0.6 — theory pack r14_merge_q1_theory_upgrade_v1 06 App A
- `01`: +6 — theory pack file numbers 01–09 / OUT file ids 01–03 (Appendix D rows; C.10 headings)
- `02`: +2 — theory pack file numbers 01–09 / OUT file ids 01–03 (Appendix D rows; C.10 headings)
- `03`: +3 — theory pack file numbers 01–09 / OUT file ids 01–03 (Appendix D rows; C.10 headings)
- `04`: +1 — theory pack file numbers 01–09 / OUT file ids 01–03 (Appendix D rows; C.10 headings)
- `05`: +1 — theory pack file numbers 01–09 / OUT file ids 01–03 (Appendix D rows; C.10 headings)
- `06`: +1 — theory pack file numbers 01–09 / OUT file ids 01–03 (Appendix D rows; C.10 headings)
- `07`: +1 — theory pack file numbers 01–09 / OUT file ids 01–03 (Appendix D rows; C.10 headings)
- `08`: +1 — theory pack file numbers 01–09 / OUT file ids 01–03 (Appendix D rows; C.10 headings)
- `09`: +2 — theory pack file numbers 01–09 / OUT file ids 01–03 (Appendix D rows; C.10 headings)
- `1`: +53 — witness values (W3b DL^pess = 1, W_DL_AL3 DL = 1, W4e GSV_pess = 1, W6 vertex VOI = 1, W5 sequence 1→0→1, W5 D(δ)=1+δ), N_j0 = N_j1 = 1 (G7), margins 1 TWD — theory pack r14_merge_q1_theory_upgrade_v1 02–07, 09
- `1,1,1,1,0,0,0,1`: +3 — W5 / 51 T-SEN-8 build sequence (already in 59a l.1140, 1918, 2903)
- `1.7.2`: +2 — section / table / appendix reference (no data value)
- `1/2`: +4 — W6 true VOI 1/2; W6c grid ≥ 1/2 — theory pack r14_merge_q1_theory_upgrade_v1 05 §6
- `1/3`: +2 — W6c edge-only grid true value 1/3 — theory pack r14_merge_q1_theory_upgrade_v1 05 §6(4e)
- `10`: +13 — W4 / W4c / W4d loose C = 10; W4b 15 → 10; erratum pess value 10 (13 §3); C.10 heading — theory pack r14_merge_q1_theory_upgrade_v1 03, 13
- `100`: +1 — erratum counterexample pess value −100 — theory pack r14_merge_q1_theory_upgrade_v1 13 §3
- `13`: +2 — theory pack file 13 (erratum); existing '13 種輸出狀態' (4-20) — theory pack r14_merge_q1_theory_upgrade_v1 13
- `13.2`: +1 — section / table / appendix reference (no data value) (v2.2 §13.2/§13.4 cited by theory pack r14_merge_q1_theory_upgrade_v1 05/07)
- `13.4`: +1 — section / table / appendix reference (no data value) (v2.2 §13.2/§13.4 cited by theory pack r14_merge_q1_theory_upgrade_v1 05/07)
- `15`: +12 — W2/W3 B = 15; W4 15; W4b 15 → 10; theory pack 01–15 — theory pack r14_merge_q1_theory_upgrade_v1 02 §4, 03 §8
- `16`: +2 — G01–G16 / 16 V1 items (existing manuscript facts, 3.9.3)
- `162/400`: +2 — R-4 PRIMARY: canonical W5 ±5% survival — theory pack r14_merge_q1_theory_upgrade_v1 04 §6, 09, 14 A6, 15 §4.4
- `2`: +18 — W3c DL = 2; W3m B = 2; 'two sources' counts — theory pack r14_merge_q1_theory_upgrade_v1 02 §2.1, 09
- `2026-10-18`: +1 — status-line review date (orchestrator brief; replaces 2026-10-14)
- `27`: +2 — 27 witnesses — theory pack r14_merge_q1_theory_upgrade_v1 09, 12, 14 §3
- `27/27`: +1 — witness verdict 27/27 PASS — theory pack r14_merge_q1_theory_upgrade_v1 09, 12
- `3`: +18 — W5 region endpoint 3 ([0,3)); W5_WIDE margin 3; 3 portfolios × 1 block (R3); ≥3 vertices (E.6e) — theory pack r14_merge_q1_theory_upgrade_v1 04 §5–§6, 05 §6, 06 App A
- `3,5`: +1 — W5 D(δ) piece on [3,5] — theory pack r14_merge_q1_theory_upgrade_v1 04 §5.1
- `3-4`: +2 — section / table / appendix reference (no data value)
- `3.11.2`: +1 — section / table / appendix reference (no data value)
- `3.12.4`: +7 — section / table / appendix reference (no data value)
- `3.12.6`: +2 — section / table / appendix reference (no data value)
- `3.13`: +7 — section / table / appendix reference (no data value)
- `3.14.3`: +6 — section / table / appendix reference (no data value)
- `3.9.2`: +1 — section / table / appendix reference (no data value)
- `3.9.3`: +2 — section / table / appendix reference (no data value)
- `3.9.5`: +1 — section / table / appendix reference (no data value)
- `3.9.6`: +4 — section / table / appendix reference (no data value)
- `3/5`: +1 — W6c non-nested grid 4 → 5 value 3/5 — theory pack r14_merge_q1_theory_upgrade_v1 05 §6(4d)
- `30`: +2 — W1 B = C = 30 — theory pack r14_merge_q1_theory_upgrade_v1 02 §4 / 51 T-ORC-8 (already in 59a table 4-20)
- `367/400`: +2 — R-4 SENSITIVITY ONLY: W5_WIDE ±5% survival — theory pack r14_merge_q1_theory_upgrade_v1 04 §6, 09, 14 A6, 15 §4.4
- `4`: +16 — W5 region endpoint 4 ((4,∞)); W5_WIDE [0,4); Remark G7 x < 4 (W8b iii); 4-20 table ids — theory pack r14_merge_q1_theory_upgrade_v1 04, 07
- `4-20`: +17 — section / table / appendix reference (no data value)
- `4.9.1`: +5 — section / table / appendix reference (no data value)
- `400`: +1 — 400 deterministic perturbation draws per radius — theory pack r14_merge_q1_theory_upgrade_v1 04 §6, 09, 14 A6
- `42`: +1 — canonical model file id 42 (v2.2), not modified
- `5`: +19 — W3 DL = 5; W4 GSV = DL_loose = 5; W4c DL = 5; D(δ) piece [3,5] — theory pack r14_merge_q1_theory_upgrade_v1 02 §4, 03 §8, 04 §5.1
- `5.6`: +3 — section / table / appendix reference (no data value)
- `5.7`: +1 — section / table / appendix reference (no data value)
- `5.8`: +2 — section / table / appendix reference (no data value)
- `5.8.10`: +2 — section / table / appendix reference (no data value)
- `5.8.5`: +1 — section / table / appendix reference (no data value)
- `51`: +20 — canonical solver file id 51 (v2.2), not modified
- `6`: +8 — theory pack file 06 (C.10.6 heading) and W-series counts — theory pack r14_merge_q1_theory_upgrade_v1 06
- `6,912`: +1 — Conjecture M2 bounded search 0 of 6,912 — theory pack r14_merge_q1_theory_upgrade_v1 04 §5.3, 09
- `7`: +7 — W4c C 10 → 7; W5_WIDE region (7,∞); 7/7 canonical cross-checks; file 07 — theory pack r14_merge_q1_theory_upgrade_v1 03 §6, 04 §6, 09
- `8`: +8 — W4c PR_B = 8; eight scalars perturbed (W5/W5_WIDE); file 08 — theory pack r14_merge_q1_theory_upgrade_v1 03 §6, 04 §6
- `9`: +6 — W4d C 10 → 9; v2.2 C.8 D1–D9 reference; file 09 — theory pack r14_merge_q1_theory_upgrade_v1 03 §4, 09

### Removed (token: count)

- `2026-10-14`: −1 (status-line date replaced by 2026-10-18)

No Study 1 number, model number or witness number from 59a was removed or changed; the R-1 erratum changes wording only.

## Segment diff per changed line

### changed — 59a l.5 → 01 l.5

- ⊖ `4`
- ⊕ `8`
- ⊕ `合併碩士論文 v1.8.6 THEORY INTEGRATION CANDIDATE（由 v1.8.5a 修訂；ˋSUBMISSION_READY = NOˋ）。v1.8.6 只整合 Q1 理論補充包（附錄 D）的最終標籤：第一章的貢獻與推論邊界、第 3.9.6 節的 M1–M4 範圍、第 3.12.4 節的命題分類、第 3.13 節的穩健性、VOI 與缺值範圍、第 3.14.3 節的量測優先序與停止規則、第 4.9.1 節的合成驗證分類與構造例、第 5.6–5.8 節的條件性意涵、理論貢獻與未證明清單，以及附錄 C.10（新增；C.1–C.9 逐字不變）；不改變任何方程、命題 P1–P8 的陳述、G01–G16、表 3-4／3-4A、第 3.9.2–3.9.5 節的 V1 設計、Study 1 數值、企業模型 v2.2 或求解器 51，也不新增任何引文；附錄 C.10.9 另記一項 Lemma E′ 證明用語的勘誤（只改證明用語，不改任何數值）。P2 的備註用語依 Lemma S 精確化（P2 陳述不變）。理論補充包的整體判定為 PARTIAL（Q1_THEORY_UPGRADE_VERDICT = PARTIAL；附錄 D）。新增的形式結果（含以明確前提重寫的 v2.2 重述）皆為本研究的模型內結果，構造例皆為 ˋSIMULATED_ONLYˋ，不是企業實證證據。前一版為`

### changed — 59a l.15 → 01 l.15

- ⊕ `，在特定的錯位與可分離性條件下，`
- ⊕ `（不是一般性質）`

### changed — 59a l.31 → 01 l.31

- ⊕ `, under specific misalignment and separability conditions (not as a general property),`

### changed — 59a l.113 → 01 l.113

- ⊖ `最小充分`
- ⊕ `一組在本研究既定企業 AI 決策問題範圍內、以決策對象判準界定（其操作上的可區辨性待 V1 人類編碼檢驗）、且在型別定義 T1–T4 下對 v2.2 屬性結構非冗餘`
- ⊕ `分解（mechanism decomposition；M1–M4，第 3.9.6 節）`
- ⊕ `；本研究不宣稱這組分解完備、普遍充分或唯一`

### inserted — 59a l.169 → 01 l.170

- ⊕ `理論結果的推論邊界同樣分層陳述。第 3.12.4、3.13、3.14.3 節與附錄 C.10 的形式結果，都是本研究在完全資訊、單期靜態、固定參數 ˋθˋ（穩健性與 VOI 另以預先登記的參數集合）的企業—事業單位雙層模型內的結果（TYPE C）：它們說明在模型的哪些條件下授權損失為零或為正、治理要求何時可能具有篩選價值、共享能力重用何時可能使建置決策不是單一門檻、頂點檢查與 VOI 在什麼範圍內精確，以及缺值如何改變可報告的結論；它們不是企業中已發生的現象，合成構造例也不能用來證明它們。構造例只顯示存在性或反駁全稱主張；凡標為未證明（NOT_PROVEN）者，本稿不以其作為結論（第 5.8.10 節）。 ⏎ `

### changed — 59a l.178 → 01 l.180

- ⊕ `第五，本研究在模型內給出一組形式結果（TYPE C；第 3.12.4、3.13 節；附錄 C.10），並明列其範圍：授權損失由構造即非負（P1），本研究的貢獻在於刻畫它何時為零、何時為正——首佳相對的可實施性刻畫（Lemma DL-1，為 Lemma E′ 於首佳解之重述）、在無部門專屬限制（AL3）且精確平手下的必要條件、唯一首佳下的原始條件刻畫（Cor DL-3）、envelope 只能設上限（Prop DL-6），以及成對條件無法判定其正負的構造例（W3c）；治理篩選價值的會計恆等式、充分條件與精確平手下的必要條件；共享能力重用在雙層中可能使建置區域不是區間的存在性結果；以及頂點精確性、VOI 與缺值分類的成立範圍。這些結果不包含授權損失為正的原始條件充要刻畫，也不宣稱任何治理要求必然提高企業價值。`

### replaced (old line; new text in following insertion) — 59a l.180

- ⊖ `**方法貢獻。** 第一，本研究提供一套同時處理共享固定成本、能力前提、資源 envelope 與政策耦合的有限離散雙層模型，並證明 envelope 的有限化（Lemma E′：只需以部門自身可行計畫的資源向量作為候選 envelope；附錄 C.2），使模型可精確求解。第二，本研究嚴格區分序位與基數、名義權限與有效控制、設計反應與實際反應，並給出缺值的拒算與部分輸出規則。第三，本研究以集合式不確定性與 regret 進行決策元素層級的穩健性分類，避免以單一最有利情境作為結論。第四，本研究提出使用率的混合算子候選：ˋα ≡ 1ˋ 時還原原模型，並以恆等式說明簡化式「事件量 × 使用率 × 效果 − 導入成本」成立的條件與選擇偏誤的方向。`

### inserted — 59a l.179 → 01 l.182

- ⊕ `**一般形式貢獻與 AI 特定實例化。** 上述第五點的組合層級性質——授權損失、治理篩選、共享能力重用的非單調性、識別價值（VOI）、穩健性範圍與缺值分類——只使用有限計畫集合、池化資源、兩套帳本、有限政策選單與區塊多線性的不確定集合，因此是企業—事業單位架構的一般形式性質，並非 AI 所獨有，對任何共用平台的資訊科技 portfolio 都成立（指具相同模型結構者的形式適用範圍，不是經驗上的可推廣性）。本研究的 AI 特定部分在於：AI × 決策文獻的功能結構與 G01–G16、M1–M4 對企業 AI 機制的詮釋、人機配置（ˋm_kˋ、ˋA_kˋ）與依授權深度設定的要求表、人員對 AI 輸出的反應函數 ˋρˋ、評估保證與 AI 治理的語意（ˋEAˋ、ˋEAXˋ），以及 AI 特定的實證參數化（V7，尚未執行）與後續的企業應用。兩者分開陳述，避免把一般形式性質讀成 AI 特有的發現。 ⏎  ⏎ **方法貢獻。** 第一，本研究提供一套同時處理共享固定成本、能力前提、資源 envelope 與政策耦合的有限離散雙層模型，並證明 envelope 的有限化（Lemma E′：只需以部門自身可行計畫的資源向量作為候選 envelope；附錄 C.2），使模型可精確求解。第二，本研究嚴格區分序位與基數、名義權限與有效控制、設計反應與實際反應，並給出缺值的拒算與部分輸出規則。第三，本研究以集合式不確定性與 regret 進行決策元素層級的穩健性分類，避免以單一最有利情境作為結論；其中只有 Model B（及 A+）的整個 portfolio 在區塊多線性與乘積型不確定集合下具頂點精確證書，元素層級與 Model C 只以列舉或抽樣報告涵蓋率（第 3.13 節）。第四，本研究提出使用率的混合算子候選：ˋα ≡ 1ˋ 時還原原模型，並以恆等式說明簡化式「事件量 × 使用率 × 效果 − 導入成本」成立的條件與選擇偏誤的方向。`

### inserted — 59a l.768 → 01 l.773

- ⊕ `### 3.9.6 M1–M4 的範圍、非冗餘性與充分性狀態（v1.8.6 新增） ⏎  ⏎ **定位。** 本研究把 M1–M4 界定為「在本研究既定企業 AI 決策問題範圍內，以決策對象判準界定、且在 T1–T4 型別定義下對 v2.2 屬性結構非冗餘的 mechanism decomposition（操作上的可區辨性由 V1 檢驗，尚未執行）」。T1–T4 是機制物件的型別公設：M1 的座標只取決策權結構（授權、有效控制、問責與政策邊界），M2 只取路由、例外與回復路徑，M3 只取人機角色、順序、彙整規則與實際反應，M4 只取評估保證證據與可接受性判準（附錄 C.10.1）；它們與第 3.11.2 節 Model D 的 T1–T5 觸發條件無關。機制的邊界以決策對象界定：一個企業決策問題歸入哪一個機制，取決於在其他三個機制物件固定時必須改變的是哪一個物件，而不是由關鍵詞決定；兩個物件必須同時改變時為橋接。 ⏎  ⏎ **已建立與未建立的性質。** (1) 非冗餘性（Prop IRR）：在 T1–T4 下，對每一個 Mi 都存在一個 v2.2 實例，使去掉 Mi 的其餘三者無法表示該實例的可行性或價值。這是在 T1–T4 與 v2.2 屬性結構下的定義性結果，對任何把 v2.2 讀取的屬性分成四個非空類別的分割都成立，因此它只表示 v2.2 的屬性結構沒有閒置的機制類別，不構成 M1–M4 作為企業 AI 決策理論的驗證。(2) 內部涵蓋（Lemma COV）：v2.2 靜態模型的每一個配置屬性與可行性因子都歸屬於 M1–M4、共享能力架構（F5）、經濟原始量或組織型態之一；由於 v2.2 本身由 M1–M4 推導而來，這是具循環性的內部封閉，不是外部完備性。(3) 未建立：M1–M4 的完備性、普遍充分性與唯一性都未建立（充分性狀態 PARTIAL；附錄 C.10.1），M1–M4 也不窮盡企業 AI 的所有組織機制；已知的候選殘差包括企業與部門之間的資訊不對稱、不改變控制與帳本的純問責歸屬、採購與資料權利，以及 AI 對 AI 的輸出鏈，以及時間（跨期）維度（由 LONGITUDINAL／M5 處理，不屬靜態 M1–M4）。 ⏎  ⏎ **輔助類別的理論讀法。** 下列讀法依理論補充包的最終定義，只說明各類別在理論上的角色，不改變 S1e 編碼者材料的類別定義，也不改變第 3.9.3 節 V1 設計的語意。DATA_GATED 是識別條件：它決定某一機制函數的定義域是否納入需由資料識別的變數（例如 G10 的門檻變體），不是另一種機制。LONGITUDINAL 是與靜態 M1–M4 正交的時間（與資訊狀態）維度；M5 只保留為標籤，不是第五個平行機制。NONE 是涵蓋缺口的訊號：存在可辨識的企業決策過程（S1e 編碼者材料的用語；第 3.9.3 節沿用 S1d 的「企業決策介面」，兩者指同一判斷，S1e 只改編碼者用語與答案表版面，不改類別定義），但不在 M1–M4 工作集合內；它在單一項目上對應充分性的反例，但 16 個項目不是企業決策問題母體的樣本，因此 NONE 的有無都不能建立或否定充分性。EVIDENCE_ONLY 表示該配對落在部分對應 G→M 的定義域之外（沒有配對特有的企業決策），不被強迫歸入 M1–M4。 ⏎  ⏎ **V1 檢驗什麼。** V1 檢驗的是 G→M 對應在凍結類別定義下的編碼者間可詮釋性，不檢驗 M1–M4 的非冗餘性（形式命題），也不檢驗其充分性或是否為最小的機制集合（16 個項目不是問題母體的樣本）；Q2 的 α 高，不表示 M1–M4 充分，α 低也不否定非冗餘性，只表示對這些項目而言決策對象判準未被穩定套用。人類編碼尚未執行，本節不使用也不預期任何結果。 ⏎ `

### changed — 59a l.1138 → 01 l.1152

- ⊖ `需要`
- ⊕ `在至少一項`
- ⊕ `上需要多於企業偏好配置的用量`
- ⊕ `（envelope 可分離性的精確條件見 Lemma S，附錄 C.10.2）`

### inserted — 59a l.1143 → 01 l.1158

- ⊕ ` ⏎ **命題的分類與 Q1 理論補充（v1.8.6；重述與 TYPE C；證明與構造例見附錄 C.10）。** 上列 P1–P8 的陳述不變。以下把相關的新增結果依性質分類：*重述*（v2.2 既有內容以明確前提重寫）、*恆等式*、*引理／命題／推論*（在所列前提下證明）、*構造例*（ˋSIMULATED_ONLYˋ，只顯示存在性或反駁全稱主張）與*未證明*（NOT_PROVEN）。所有結果皆為完全資訊、固定 ˋθˋ 的模型內結果；除另有說明，均採精確平手（ˋε_tie = 0ˋ），樂觀與悲觀分別陳述。編號沿用理論補充包（Lemma S、DL-、GS-、Thm D1／D3、Prop D4–D6、Lemma M 等），與附錄 C.8 的模型選擇 D1–D9、M5 的 (D1)(D2)、組織維度 D01–D12 及資源限制 (R1) 皆無關。 ⏎  ⏎ *授權損失（DL）。* 由 P1，DL ≥ 0 是由構造而來；理論問題是 DL 何時為零、何時為正。(A) **零損失刻畫**：Lemma DL-1o／DL-1p——樂觀（悲觀）DL 為零，若且唯若至少一個集中最適解（首佳解）在 Model C 中可自我實施；這是首佳相對的刻畫，即 Lemma E′ 於首佳解之重述，判定它需要知道全部首佳解，因此至少需先求解 B 並取得全部首佳解。(B) **DL 為正的必要條件**：在沒有部門專屬限制（AL3 成立）時，樂觀 DL 為正需要部門最佳回應相對於某一首佳計畫的嚴格偏好逆轉，且該偏離無法由 envelope 分離（Cor DL-2o）；悲觀 DL 為正只需弱逆轉（平手即足夠，Cor DL-2p）；AL3 不成立時，部門專屬限制本身即可使 DL 為正而不需任何帳本逆轉（AL3 管道；構造例 W_DL_AL3）。因此 P2 備註所說的「不對齊」包含 AL3。(C) **充分條件**：在唯一首佳的前提下，Cor DL-3 以原始條件刻畫 DL 何時為正（Part (i)：首佳計畫在 C 中可行時，為嚴格〔樂觀〕或弱〔悲觀〕逆轉加上 envelope 不可分離；Part (ii)：首佳計畫違反部門專屬限制時，兩種界的 DL 皆為正）；Prop DL-4 給出 DL = 0 的充分條件（多部門、AL3、精確平手；AL3 不成立時其 (b)(c) 不成立）。(D) **反例**：構造例 W3c 顯示，同一對逆轉且不可分離的計畫，可在一個實例中造成 DL = 2、在另一實例中 DL = 0，因此理論補充包所列成對存在性條件 (A)–(F) 的任何布林組合，都不能構成 DL 正負號的充要判準。由此保留的結論是：帳本不對齊本身不足以造成授權損失；不對齊但可由 envelope 阻擋時 DL = 0（W2）；不對齊且不可阻擋時 DL > 0（W3）。Prop DL-6 說明 envelope 只能設上限、不能強制採用：在 AL3 下，DL 只來自採用不足（部門偏好較便宜的計畫，例如維持現況）與資源用量不高於目標計畫的不利採用兩個來源，AL3 不成立時另有部門專屬排除的管道；這些都無法以任何 envelope 修正，只有 ˋγˋ（禁止、強制或要求）或 ˋyˋ 能作用於前兩者。樂觀與悲觀分開報告：構造例 W3b 為 DL^opt = 0 < DL^pess = 1（只由部門平手造成）。本稿不宣稱任何不依賴首佳解的 DL 原始充要條件。 ⏎  ⏎ *治理篩選。* 在 Model B 中，較嚴格的要求只會縮小集中規劃的可行集合，因此不會因篩除選項而得到價值（GS-0：P7 加上治理營運成本管道之重述）；在 Model C 中，要求改變的是部門的最佳回應對應，因此可能具有篩選作用。以較寬鬆要求 ˋReq_lˋ 與較嚴格要求 ˋReq_sˋ 比較，定義總篩選效果（Gross Screening Effect）ˋGSV^m = F^{C,m}(Req_s, C_l) − F^{C,m}(Req_l, C_l)ˋ（相同治理成本下）、直接治理成本效果（Direct Governance Cost）ˋDGC^m = F^{C,m}(Req_s, C_s) − F^{C,m}(Req_s, C_l)ˋ，以及淨治理效果（Net Governance Effect）ˋNGE^m = GSV^m + DGC^mˋ。恆等式 GS-I 為 ˋGSV^m = DL^m(Req_l) − DL^m(Req_s) − PR_Bˋ（ˋPR_Bˋ 為 B 中的要求代價），由 P1 與 P7 推得 ˋGSV^m ≤ DL^m(Req_l)ˋ：篩選價值不超過較寬鬆要求下的授權損失。Prop GS-1 為充分條件：嚴格要求保留某一寬鬆首佳解、且移除其全部不可阻擋的偏離（悲觀時另移除平手的不利計畫）時，ˋGSV = DL_looseˋ。Thm GS-N 為必要條件，只在精確平手下以其精確形式成立：ˋGSV^m > 0ˋ 時，必有一個被排除的寬鬆最佳回應，它在 envelope 上與一個保留的計畫不可分離、對企業較差，且部門對它嚴格（樂觀）或弱（悲觀）偏好。兩者之間沒有原始條件的充要刻畫（未證明）。構造例：W4 重現 P8 的 ˋF^Cˋ 由 10 升至 15（ˋGSV = DL_loose = 5ˋ、ˋPR_B = 0ˋ）；反向的 W4b 由 15 降至 10（嚴格要求篩除原本已可阻擋的計畫，並排除較佳的首佳配置）；W4c 由 10 降至 7（篩除 DL = 5，但要求代價為 8）；W4d 由 10 降至 9（只篩除一個不可阻擋的偏離，另一個更差的不可阻擋計畫取而代之）。因此，在特定的雙層錯位與可分離性條件下，治理可能具有正的篩選價值；本稿不宣稱治理要求一般會提高企業價值。由禁止（ˋJ^forbidˋ）或不允許（ˋAllow = 0ˋ）達成的篩選，在本節稍後的治理價值分解中記入賦能區塊 EE，而不是要求區塊 RE。 ⏎  ⏎ *共享能力重用。* Thm D1 為 P4 中 B 部分的明確形式（以能力來源為索引等前提下，B 的建置區域為上集），Thm D3 為 P2 逐點於 ˋ(y, γ)ˋ 的重述（帳本對齊時 C 的建置區域與 B 相同）；Prop D4、D5 給出比完全對齊更弱的單調性充分條件，因此 P4 所說「只有帳本對齊時才保證」的帳本對齊是充分而非必要條件。Prop D6 是存在性結果：存在帳本不對齊的 C 實例，其建置區域不是區間，亦即投資決策不必對重用效益單調；構造例 W5 重現 51 T-SEN-8 的建置序列 1,1,1,1,0,0,0,1（建置 → 不建置 → 建置），其連續的建置區域為 ˋ[0,3) ∪ (4,∞)ˋ（51 的嚴格慣例）。Lemma M 說明在其前提下單一部門、兩個選項無法產生此型態；三選項、均一重用下的對應命題（Conjecture M2）未證明。D6 只是存在性結果，不表示帳本不對齊的 Model C 實例多半如此；合成構造例不等於企業現象。`

### changed — 59a l.1151 → 01 l.1173

- ⊕ `；篩選價值不超過較寬鬆要求下的授權損失〔恆等式 GS-I〕，正篩選價值的必要條件見 Thm GS-N；由禁止或不允許達成的篩選記入 EE 而非 RE`

### changed — 59a l.1178 → 01 l.1200

- ⊖ `故`
- ⊕ `資源使用不增。樂觀情形取`
- ⊕ `為最適集合中企業貢獻最大者：ˋxˋ 在新集合上`
- ⊖ `最適集合只會縮小——`
- ⊕ `減（精確平手下不`
- ⊖ `（`
- ⊕ `）。悲觀情形須`
- ⊖ `樂觀`
- ⊖ `佳`
- ⊕ `適集合中部門目標 ˋF_uˋ 最大`
- ⊖ `）`
- ⊕ `：新集合仍含部門目標的最大值點`
- ⊕ `最大值不變，新的最適集合是原最適集合的子集合，故`
- ⊕ `。在預先登記的平手容差 ˋε_tie > 0ˋ 下`
- ⊖ `而資源使`
- ⊕ `若改取最適集合中非最大者，新的最適集合可能納入原本不在其中的計畫，悲觀值可能下降；因此悲觀情形的證明`
- ⊖ `不增`
- ⊕ `語須取 ˋF_uˋ 最大者`
- ⊕ `；勘誤見附錄 C.10.9）。此修正只改證明用語，Lemma E′ 的陳述與求解器 51 的計算數值不變（51 列舉所有計畫的資源向量，含 ˋF_uˋ 最大者`

### inserted — 59a l.1272 → 01 l.1295

- ⊕ `**頂點精確性的適用範圍（v1.8.6；附錄 C.10.6）。** 頂點精確性只適用於 Model B（及 A+）的整個 portfolio 最適性、MaxRegret 與 ˋλˋ 盒證書，且須同時滿足：(R-a) 被檢查的是整個 portfolio，其價值是 ˋθˋ 的固定函式；(R-b) 價值對每一登記區塊為仿射（區塊多線性；每區塊只含單一類乘數因子）；(R-c) ˋΘ_gˋ 為各區塊多面體的笛卡兒乘積，無跨區塊相依限制；(R-d) 候選集合固定且只含 ROBUSTLY_FEASIBLE 的 portfolio；(R-e) 以弱最適判定（Thm R1，為 Lemma R 之重述；Cor R1a、R1b 為 MaxRegret 與 ˋλˋ 盒的重述）。它不適用於決策元素層級：頂點檢查不精確（Prop R3），最小反例即上段的 T-SEN-3 實例——頂點上判為 ROBUST、在 ˋ(0.4, 0.6)ˋ 內為 FRAGILE；若恰一個候選 portfolio 含該元素值，頂點檢查同時也是必要條件（Prop R4；此為充分條件下的特例，不表示其他情形必不精確），元素層級的精確判準是含該值之 portfolio 的最適區域能否覆蓋 ˋΘ_gˋ（Prop R2）。它也不適用於 Model C：即使固定 leader 決策，帳本不對齊時悲觀值可能在部門的切換面上不連續（Prop R5），因此 C 的網格結論只對被評估的點成立；含相依限制的參數集合或只是條件可行的候選，也不在範圍內。（編號 R1–R5 屬理論補充包，與資源限制 (R1)(R2) 無關。） ⏎ `

### replaced (old line; new text in following insertion) — 59a l.1277

- ⊖ `**Value-of-identification 診斷。** $VOI_p = MMR(\Theta_g) - \sup_v MMR(\Theta_g \mid \theta_p = v)$，用以排序最值得優先量測的參數。ˋsupˋ 只取區塊頂點時可能高估（解析例：頂點版為 1、真值為 0.5），故同時報告只取頂點與加入內點網格的兩個版本；兩者皆為真值的上界，網格版不大於頂點版。此診斷只決定資料蒐集優先序，不進目標（G12 的靜態影子）。v2.4 candidate 中，ˋαˋ 可作為一個參數區塊計算 ˋVOI_αˋ，即識別使用率對決策的價值。`

### inserted — 59a l.1276 → 01 l.1301

- ⊕ `**Value-of-identification 診斷。** $VOI_p = MMR(\Theta_g) - \sup_v MMR(\Theta_g \mid \theta_p = v)$，用以排序最值得優先量測的參數。ˋsupˋ 只取區塊頂點時可能高估（解析例：頂點版為 1、真值為 0.5），故同時報告只取頂點與加入內點網格的兩個版本；在固定候選集合（51 之 ˋvoi_tableˋ 的慣例）下，兩者皆為真值的上界（固定候選集合上界），網格版不大於頂點版（Prop E.1、E.2，附錄 C.10.5）。若縮小 ˋΘˋ 後重新計算 robust 候選集合（調適慣例），此次序不再成立：MMR 可能上升、VOI 可能為負（構造例 W6b）。網格版以等距網格與二頂點混合點構成；機率區塊有三個以上頂點時，只取邊上點的網格不保證收斂到真值（構造例 W6c：網格值不低於 1/2，真值為 1/3）。此診斷只決定資料蒐集優先序，不進目標（G12 的靜態影子）。v2.4 candidate 中，ˋαˋ 可作為一個參數區塊計算 ˋVOI_αˋ，即識別使用率對決策的價值。 ⏎  ⏎ **VOI 在本研究中的定位（v1.8.6）。** 資訊價值的概念並非本研究所創。本研究的貢獻限於：在部分識別的企業 AI 雙層 portfolio 中，以 VOI 排定參數識別的優先序；區分只取頂點的值與納入內點的值（頂點版可能高估：第 4.9.1 節表 4-20D 的解析 oracle 中頂點版為 1、真值為 0.5，標為合成解析反例，SYNTHETIC ANALYTIC COUNTEREXAMPLE）；並提出序列識別程序（第 3.14.3 節）作為程序而非定理。已證明的性質只對固定候選集合成立：縮小 ˋΘˋ 時 MMR 不增、VOI 非負且有上述次序、巢狀網格單調，以及在預先登記有限證據狀態時程序必然終止（Prop E.1、E.2、E.6，Thm E.7）；候選集合隨 ˋΘˋ 調適時的對應性質已被反駁（W6b），依 VOI 由大到小逐一量測的最適性（VOI-greedy）未證明，只以單一區塊 VOI 判斷的停止規則是短視的（W6e：每一區塊的 VOI 皆為 0，聯合識別卻使 MMR 由 1 降為 0）。因此序列識別性質的狀態為 PARTIAL。這些結果不表示企業的量測效率，也不構成任何企業的量測結果。（E 系列編號屬理論補充包，與附錄 E 的待決事項編號無關。） ⏎  ⏎ **缺值的三類（v1.8.6；附錄 C.10.7）。** 未識別的參數格依其對結果的作用分為三類，並對應理論補充包的定義（Def G）：(1) **改變可行性**（feasibility-changing）——缺值使可行集合不被點識別，對應通道標記 FC；(2) **改變目標或排序**（objective/ranking-changing）——可行集合不變，但可行決策的排序隨缺值改變，對應 DC 且非 FC；(3) **不改變決策但具認識上的重要性**（decision-invariant but epistemically relevant）——以 0 填補時的每一個最適決策，在所有可接受值下仍為最適，但價值或可行集合未被點識別，對應 DIER；結果物件在可接受值上完全不變者為 NULL。FC 與 DC／DIER／NULL 正交，可與三者分別同時出現。缺值不等於 0：以 0 填補可能落在可接受集合之外（Prop G8），也可能虛構可行性或不可行性（Prop G1）。這是部分識別的方法論，屬模型識別的處理規則，不是 AI 組織理論。第 3.12.6 節的狀態對應如下：ˋRESTRICTED_SOLVEˋ（FC，可能為 DC 或 DIER；在 B 中受限求解的值是下界，在 C 中不是，Prop G2）、ˋTHRESHOLD_MODEˋ（ˋF_cˋ 的完整決策對應即精確的識別集合，Prop G5）、ˋPARTIAL_OBJECTIVEˋ（ˋλˋ 盒在 B／A+ 可由頂點精確區分 DC、DIER 與 NULL，C 只能以網格，Prop G4）、ˋUNIDENTIFIEDˋ（元素層級的 DC）、ˋFOLLOWER_LEDGER_UNIDENTIFIEDˋ（對 B 為 NULL，對 C 可能為 DC，Prop G6）。（命題編號 G1–G8 屬理論補充包，與缺口 G01–G16 無關。）`

### changed — 59a l.1327 → 01 l.1355

- ⊕ `僅限`
- ⊖ `結果格的精確度——它在`
- ⊕ `基線項 ˋN_j0 g_j0(ȳ^cur)ˋ 中對`
- ⊖ `中以`
- ⊕ `共同、且不影響「維持現況或切換」比較的部分——只有在所比較的 portfolio 對 ˋjˋ 是否維持現況的選擇`
- ⊖ `方式出`
- ⊕ `時，`
- ⊖ `，`
- ⊕ `況結果格才`
- ⊖ `但`
- ⊕ `凡進入 ˋk = 0ˋ 與 ˋk ≥ 1ˋ 比較的現況結果格，其精確度可改變決策（附錄 C.10.7 Remark G7；構造例 W8b），應依第一批資料的 VOI 排入第 (2) 或 (3) 級；`

### changed — 59a l.1329 → 01 l.1357

- ⊕ `這三項規則須搭配預先宣告的候選集合慣例：以固定候選集合（第一批登記時的 ROBUSTLY_FEASIBLE 集合）為主，重算候選集合只作次要診斷並標 ˋCANDIDATE_SET_EXPANDEDˋ（重算時 MMR 可能上升，已觸發的第一項規則可能被撤回，構造例 W6b）；第三項以單一區塊的網格 VOI 判斷，是短視的停止規則，不保證殘餘 regret（W6e）；程序的終止須以預先登記的有限證據狀態或步數上限保證（Thm E.7；沒有離散化時可能不終止，W6f）。以上性質都只對固定候選集合證明，也不表示依 VOI 排序的量測順序為最適。`

### changed — 59a l.1888 → 01 l.1916

- ⊕ `依證據性質，本節的合成驗證分為 A 實作驗證、B 形式性質回歸與 C 構造例／反例三類，其對照與構造例表見第 4.9.1 節。`

### changed — 59a l.1917 → 01 l.1945

- ⊕ `；對固定候選集合；合成解析反例，見表 4-20D 的 W6`

### inserted — 59a l.1984 → 01 l.2013

- ⊕ ` ⏎ ### 4.9.1 合成驗證的三類區分與構造例（v1.8.6 新增；SIMULATED_ONLY） ⏎  ⏎ 本節不新增任何求解器檢查，也不改變表 4-20 至 4-20C 的任何數值；它只依證據性質把上述結果分為三類，並列出理論補充包的構造例。 ⏎  ⏎ **A. 實作驗證（implementation verification）。** 檢查實作是否忠實執行規格：型別與單位、ˋωˋ 洩漏防護與 NaN／inf 拒絕；(F5e) 在所選能力狀態下求值；13 種輸出狀態與缺值處理（含不以 0 補值、ˋF_cˋ 門檻模式與 ˋλˋ 部分目標）；精確性（動態規劃 = 完整列舉、Lemma R 的範圍錯誤、可行性四類與 registry 承諾）；以及重現性與標籤重排（表 4-20 的 v2.2 各列、表 4-20A 的還原與編碼一致性各列、表 4-20B 與表 4-20C）。 ⏎  ⏎ **B. 形式性質回歸（formal-property regression）。** 檢查命題在受測合成實例上未被反駁：P1 排序、P2 對齊時 DL = 0、P4 能力門檻、P5 序位重標不變、P6 尺度不變、P7 在 B 中放寬要求單調、P8 的篩選作用、恆等式 NEV = VCP + VSC − DL 與 VCP = VRA + DL0、Lemma E／E′、樂觀與悲觀界、(F9) 硬上限，以及 MaxRegret 與 VOI 的次序（表 4-20 的對應各列；表 4-20A 的 P10–P12 各列）。未被反駁不等於被證明；命題的證明見附錄 C.6 與 C.10。 ⏎  ⏎ **C. 構造例與反例（constructive witnesses／counterexamples）。** 下表的構造例以手算代數實例顯示存在性或反駁全稱主張，不是一般定理的證明；證明見附錄 C.10。構造例由獨立的標準函式庫程式重算（ˋq1_theory_witnesses.pyˋ；27 個構造例全部 PASS，構造例集合雜湊前綴 ˋa68664ceˋ，重複執行的輸出逐位元組相同；附錄 D），其中 W1–W7 對應 51 號實作既有的合成檢查。 ⏎  ⏎ **表 4-20D：理論補充的構造例（SIMULATED_ONLY；構造例，非證明）** ⏎  ⏎ | 構造例 | 顯示什麼 | 支持或反駁的陳述 | 與既有檢查的對應 | ⏎ |---|---|---|---| ⏎ | W1 | 帳本對齊：B = C = 30，DL = 0（樂觀 = 悲觀） | 支持 P2 與 Prop DL-4(c) | 表 4-20 手算 oracle 的對齊情境 | ⏎ | W2 | 帳本不對齊但可由 envelope 阻擋：B = C = 15，DL = 0 | 反駁「不對齊即造成 DL > 0」；支持 Lemma S | 手算 oracle 的可阻擋情境 | ⏎ | W3 | 帳本不對齊且不可阻擋：B = 15 > C = 10，DL = 5 | 支持 Lemma DL-1 與 Cor DL-3 Part (i)；Prop DL-5 的上界在此達成 | 手算 oracle 的不可阻擋情境 | ⏎ | W4 | P8 篩選：ˋF^Cˋ 由 10 升至 15，ˋGSV = DL_loose = 5ˋ，ˋPR_B = 0ˋ | 支持 P8、Prop GS-1 與恆等式 GS-I | 表 4-20 的 P8 列 | ⏎ | W5 | Model C 中建置決策對重用 ˋδˋ 非單調：序列 1,1,1,1,0,0,0,1（1 → 0 → 1）；嚴格慣例下的建置區域為 ˋ[0,3) ∪ (4,∞)ˋ | 支持 Prop D6（存在性）；反駁「C 的建置區域必為區間」 | 表 4-20 的 C 中 ˋδˋ 非單調列（T-SEN-8） | ⏎ | W6 | 解析 oracle 中頂點 VOI = 1、真值 VOI = 0.5（固定候選集合；合成解析反例，SYNTHETIC ANALYTIC COUNTEREXAMPLE） | 支持 Prop E.2、E.3（頂點版可能高估） | 表 4-20 的 MaxRegret 與 VOI 列（T-SEN-7） | ⏎ | W7 | 元素層級：頂點判為 ROBUST、內點 ˋ(0.4, 0.6)ˋ 為 FRAGILE；整個 portfolio 的 Lemma R 與 MaxRegret 仍頂點精確 | 支持 Prop R3、R5 與 Thm R1（重述；正向對照） | 表 4-20 的 Lemma R 範圍列（T-SEN-3） | ⏎  ⏎ 表註：W5 是主要（canonical）構造例，逐點重現 T-SEN-8；在全部八個純量同時 ±5% 的確定性擾動下（固定種子，400 次抽樣），W5 保留非區間建置區域 162/400 次，這是主要報告值（其邊際只有 1 TWD）。擴大邊際的側車構造例 W5_WIDE 只作擴大構造例的敏感度分析（SENSITIVITY）：在相同 ±5% 擾動下保留 367/400 次，不作為主要結果，也不取代 W5。兩者都依賴同樣的兩個結構零點：不對齊部門之 AI 配置的淨 BUD 用量不高於現況，且其 ENG 用量為 0；在此家族中，任一池化資源出現正的淨用量，建置區域即成為區間。因此 W5 只作存在性構造例，不支持重用非單調在實務上常見。補充構造例（W3b、W3c、W_DL_AL3、W4b–W4e、W5b、W5_WIDE、W6b–W6f、W8a–W8c、W_MECH_ABL）的內容見附錄 C.10.8；資訊不對稱側車的構造例不列入本章。這些合成案例只建立計算一致性、形式存在性或反例，不是企業實證證據。`

### changed — 59a l.2317 → 01 l.2369

- ⊕ `，但其條件只是必要條件`
- ⊖ `的`
- ⊕ `偏好但對企業`
- ⊖ `選擇`
- ⊕ `的配置`
- ⊖ `規則型`
- ⊕ `篩除該配置的`
- ⊕ `要求`
- ⊖ `替`
- ⊕ `回收授權損失——但不超過該損失，且須扣除該要求在集中最適下的`
- ⊖ `預算型協調`
- ⊕ `價（恆等式 GS-I：ˋGSV = DL_loose − DL_strict − PR_B ≤ DL_looseˋ）；envelope 無法阻擋只是正篩選價值的必要條件（Thm GS-N，精確平手），不是充分條件（構造例 W4c、W4d；附錄 C.10.3）`

### changed — 59a l.2323 → 01 l.2375

- ⊕ `若不利配置在至少一項池化資源上需要多於企業偏好配置的用量，`
- ⊖ `需要池化`
- ⊕ `它（Lemma S）；反之，`
- ⊕ `用量不高於企業偏好配置`
- ⊕ `（含維持現況的採用不足）無法以預算阻擋，只有 ˋγˋ（禁止、強制或要求）或 ˋyˋ 能作用（Prop DL-6）`

### changed — 59a l.2327 → 01 l.2379

- ⊖ `，`
- ⊕ `；`
- ⊖ `只有在`
- ⊕ `，`
- ⊖ `時才保證`
- ⊕ `是`
- ⊕ `的充分條件而非必要條件（Thm D3 為 P2 逐點之重述；較弱的充分條件見 Prop D4、D5）`
- ⊖ `否`
- ⊕ `不對齊時`
- ⊕ `存在`
- ⊖ `可為集合值`
- ⊕ `不是區間的實例`
- ⊕ `Prop D6 的存在性結果；`
- ⊕ `：重用可能使部門偏好的不利配置不再需要更多池化資源，從而破壞 envelope 的分離能力——治理篩選與重用非單調是同一種分離失效`

### inserted — 59a l.2329 → 01 l.2382

- ⊕ ` ⏎ **理論補充的條件性意涵（v1.8.6；模型內性質）。** 第一，授權損失的判定不能只看單一部門的成對比較：在模型內，樂觀（悲觀）DL 為零，若且唯若至少一個集中最適解在雙層中可樂觀（悲觀）自我實施（Lemma DL-1，為 Lemma E′ 之重述），只有在唯一首佳的前提下才能寫成原始條件（Cor DL-3）；因此企業資料的 DL 診斷須同時報告哪一個對齊條件不成立，以及哪一個首佳計畫存在不可阻擋的偏離。第二，envelope 只能設上限：它阻擋超用，不能阻擋方向錯誤但不更耗資源的選擇（Prop DL-6）。第三，治理要求的篩選價值以較寬鬆要求下的授權損失為上界，且須扣除其要求代價；在特定的雙層錯位與可分離性條件下，治理可能具有正的篩選價值，但這不是一般性質。第四，穩健性的精確證書只限 B 的整個 portfolio；VOI 只在固定候選集合下是真值的上界，只依單一區塊 VOI 的停止判斷是短視的。第五，缺值分類決定可報告的結論形式，而不是以 0 補值。以上皆為完全資訊、靜態、固定 ˋθˋ 的模型內性質，不是企業實證發現：ˋ[EMPIRICAL RESULT PENDING]ˋ。`

### inserted — 59a l.2340 → 01 l.2395

- ⊕ `**形式理論貢獻（模型內；TYPE C）。** 企業層另有一組形式結果，其範圍明列如下（附錄 C.10）：(1) 授權損失：DL ≥ 0 由構造而來（P1），貢獻在於刻畫 DL 何時為零——首佳相對的可實施性刻畫（Lemma DL-1，為 Lemma E′ 之重述，不作為主要定理）、AL3 下的嚴格逆轉選擇結果（Cor DL-2o）、唯一首佳下的原始條件刻畫（Cor DL-3）、成對條件無法判定 DL 正負的構造例（W3c）與 envelope 只能設上限（Prop DL-6）；損失來自完全資訊下的工具不完備，而不是隱藏資訊。(2) 治理篩選：非定義性的必要條件（Thm GS-N）、充分條件（Prop GS-1）與三種失效型態（W4c、W4d、W4e）；GS-I 是會計恆等式，ˋGSV ≤ DL_looseˋ 是 P1 與 P7 的推論。(3) 共享能力重用：在 B 與帳本對齊的 C 中單調，否則存在建置區域不是區間的實例（Prop D4–D6、Lemma M；Thm D1、D3 為 P4、P2 的重述）。(4) 頂點精確性與 VOI 的成立範圍（Prop R2、R4、R5(ii)；Thm R1 為 Lemma R 之重述；Prop E.1、E.4–E.6 與 Thm E.7（E.2、E.3 為重述），序列識別性質為 PARTIAL）。(5) 缺值分類作為模型識別的方法論（Def G、Prop G1–G8）。(6) M1–M4 在型別定義 T1–T4 下對 v2.2 屬性結構非冗餘（定義性），充分性為 PARTIAL。以上皆為完全資訊、單期靜態、固定 ˋθˋ（R、E 系列另以登記的 ˋΘ_gˋ）的模型內結果，不宣稱任何企業中成立。 ⏎  ⏎ **一般形式貢獻與 AI 特定部分的區分。** 第 (1)–(5) 項的組合層級結果是企業—事業單位架構的性質，不是 AI 所獨有，對任何共用平台的資訊科技 portfolio 皆成立（指具相同模型結構者的形式適用範圍，不是經驗上的可推廣性）。本研究的 AI 特定部分在於 AI × 決策文獻結構與 G01–G16、M1–M4 對企業 AI 機制的詮釋、人機配置與依授權深度設定的要求表、人員對 AI 輸出的反應函數 ˋρˋ、評估保證與 AI 治理的語意、AI 特定的實證參數化，以及後續的企業應用（第 1.7.2 節）。 ⏎ `

### changed — 59a l.2343 → 01 l.2401

- ⊖ `九`
- ⊕ `十`

### inserted — 59a l.2391 → 01 l.2450

- ⊕ ` ⏎ ### 5.8.10 理論結果的未證明部分（v1.8.6 新增） ⏎  ⏎ 第 3.12.4、3.13 節與附錄 C.10 的形式結果有明確的邊界；下列項目未證明（NOT_PROVEN），本稿不以其作為結論：(1) 授權損失為正的原始條件充要刻畫（不依賴首佳解；構造例 W3c 顯示它無法寫成成對存在性條件 (A)–(F) 的布林組合，Cor DL-3 只在唯一首佳下成立）。(2) 治理篩選價值為正的原始條件充要刻畫（只有 Prop GS-1 的充分條件與 Thm GS-N 的精確平手必要條件）。(3) 平手容差：Lemma DL-1 與 Lemma E′ 在求解器 51 的相對平手容差下，只在精確可負擔（ˋa(x) ≤ eˋ）時成立；51 另允許的 1e-9 資源容差不在證明範圍內，Cor DL-2–DL-5、Lemma S、Lemma I 與 Thm GS-N 仍只是精確平手的結果。(4) Conjecture M2（均一重用下，只有一個部門、一個 initiative 時不論選項多少都無法產生 1 → 0 → 1 型態，此型態需要兩個以上的部門決策單位）。(5) 依 VOI 由大到小量測（VOI-greedy）的最適性。(6) 同時具備候選集合調適、MMR 單調與頂點精確的慣例是否存在。(7) Prop E.5 的逆命題。(8) M1–M4 對一般企業 AI 決策問題的全域充分性。(9) 資訊不對稱側車的 IA-2 與 IA-3（只有證明草稿；側車狀態為 SIDECAR_DESIGN_ONLY，不修改 v2.2；其完全資訊特例重現 P3）。此外，Model C 不具頂點精確性（Prop R5 證明其不成立），多選項缺值格沒有一般的區間界定結果，Model C 中連續缺值格的 DIER 狀態只在被評估的點上成立。這些邊界與第 5.8.5 節的完全資訊假設一致：資訊不對稱只在側車設計中處理。`

### inserted — 59a l.2961 → 01 l.3024

- ⊕ `### C.10 Q1 理論補充（v1.8.6 新增；非 v2.2 原文） ⏎  ⏎ 本節不是企業模型規格 v2.2 的原文；C.1–C.9 逐字不變。本節依 Q1 理論補充包（附錄 D）的最終狀態，列出新增的形式結果、其性質標籤、前提、證明要點與構造例；完整證明見理論補充包 01–08，構造例見 09 與 ˋq1_theory_witnesses.pyˋ。性質標籤：**重述**（restatement；v2.2 既有內容以明確前提重寫）、**恆等式**、**引理**、**命題**、**推論**、**定理**、**構造例**（constructive example；ˋSIMULATED_ONLYˋ，只顯示存在性或反駁全稱主張）、**猜想**（NOT_PROVEN）。除另有說明，均採精確平手、完全資訊、固定 ˋθˋ，樂觀與悲觀分別陳述。所有新結果皆為本研究的模型內結果（TYPE C），不以「依某文獻」的方式陳述。編號沿用理論補充包，與本論文其他編號系統無關：G1–G8 不是缺口 G01–G16；D1–D6 不是附錄 C.8 的 D1–D9、M5 的 (D1)(D2) 或組織維度 D01–D12；R1–R5 不是資源限制 (R1)(R2)；E.1–E.10 不是附錄 E 的待決事項；型別公設 T1–T4 不是 Model D 的觸發條件 T1–T5。 ⏎  ⏎ #### C.10.1 M1–M4 的形式定義與狀態（理論補充包 01） ⏎  ⏎ - **定義（M1–M4 物件）。** M1 為決策權結構 ˋ𝔇 = (Agt, Rt, Auth, Eff, Acc, Pol)ˋ：誰可以讓 AI 輸出成為行動、阻止、停止或變更授權，以及誰承擔責任（ˋEffˋ 區分名義權限與有效控制）；M2 為路由結構 ˋ𝔑 = (G_k, route_k, X_k, fb_k)ˋ：輸出經過哪些交接、例外如何處理、失敗如何回復；M3 為人機角色與反應 ˋℭ = (m_k, A_k, σ_k, agg_k, ρ)ˋ：各節點的分工、順序、彙整規則與人員實際如何反應；M4 為保證判準 ˋ𝔄 = (Ev, ev_k, Accpt_γ, Prov)ˋ：使用前與使用中須具備並記錄何種證據，才可接受某一授權深度的使用。共享能力架構（F5）、經濟原始量與組織型態是機制中立的層，不屬 M1–M4。 ⏎ - **對象判準（定義）。** 決策問題歸入在其他三個物件固定時必須改變的那一個物件；兩個物件須同時改變者為橋接（例如 G08 的 M1／M3、G16 的 M1／M2）。關鍵詞不決定類別。 ⏎ - **型別公設 T1–T4（建模承諾）。** 各機制座標只取其物件型別的值（T1：ˋd_kˋ 只取權責結構；T2：ˋn_kˋ 只取路徑與回復；T3：ˋc_kˋ 只取 ˋm, A, σ, agg, ρ, πˋ；T4：ˋa_kˋ 只取證據狀態與可接受性）。 ⏎ - **Prop IRR（命題；定義性）。** 在 T1–T4 下，對每一個 Mi 都存在一個 v2.2 實例（單一 initiative、Model B、ˋθˋ 固定），使 {M1,…,M4} 去掉 Mi 後無法表示其可行性或價值，而四者全體可以。*證明要點：* 對每個 Mi 構造兩個只在 Mi 座標不同的替代方案，分別由 (F6)、(F7)、(F8)／(X1)、(F5d) 區分。此性質對任何把 v2.2 讀取的屬性分為四個非空類別的分割都成立，因此只表示 v2.2 屬性結構沒有閒置類別，不驗證此分類。構造例 W_MECH_ABL（PASS；SIMULATED_ONLY）。 ⏎ - **Lemma COV（引理；以列舉證明；具循環性）。** v2.2 靜態模型的每一個配置屬性與可行性因子，都是 M1–M4 座標、F5 架構、經濟原始量或組織型態的函數。v2.2 由 M1–M4 推導而來，故此為內部封閉，不是外部完備性。 ⏎ - **全域充分性（猜想；NOT_PROVEN）。** 沒有封閉的「企業 AI 決策問題」全集；已知殘差包括資訊不對稱（排除於設計外，見側車）、純問責歸屬、採購與資料權利、AI 對 AI 的輸出鏈，以及時間（跨期）維度（由 LONGITUDINAL／M5 處理，不屬靜態 M1–M4）。M1–M4 的充分性狀態為 PARTIAL；完備性、普遍充分性與唯一性皆未建立。 ⏎  ⏎ #### C.10.2 授權損失（理論補充包 02） ⏎  ⏎ 設定：固定 ˋθˋ；ˋP^C_u ⊆ P^B_uˋ（兩者相等若且唯若 AL3 成立；本節採 B 不含部門專屬限制的慣例）；首佳解集合 ˋ𝓑*ˋ；部門最佳回應 ˋBR_u(e)ˋ。首佳解 ˋ(y*, γ*, x*)ˋ 為 opt 自我實施，若每一部門的 ˋx*_u ∈ P^C_uˋ 且 ˋx*_u ∈ BR_u(a(x*_u))ˋ；為 pess 自我實施，若另有 ˋBR_u(a(x*_u))ˋ 上的最小企業貢獻不低於 ˋx*_uˋ 的企業貢獻。 ⏎  ⏎ - **Lemma S（引理）。** 計畫對 ˋ(x^H, x^G)ˋ 可由 envelope 分離（某一 envelope 容許 ˋx^Gˋ 而排除 ˋx^Hˋ），若且唯若 ˋa_u(x^H) ≰ a_u(x^G)ˋ，即 ˋx^Hˋ 至少在一項池化資源上用量嚴格較多。*證明：* (⇐) 取 ˋe = a_u(x^G)ˋ；(⇒) 若 ˋa(x^H) ≤ a(x^G) ≤ eˋ，凡容許 ˋx^Gˋ 的 envelope 都容許 ˋx^Hˋ。∎ ⏎ - **Lemma DL-1o／DL-1p（引理；首佳相對的可實施性刻畫；Lemma E′ 於首佳解之重述）。** ˋDL^opt = 0ˋ 若且唯若存在 opt 自我實施的首佳解；ˋDL^pess = 0ˋ 若且唯若存在 pess 自我實施的首佳解。*證明要點：* (⇐) 取 ˋe_u = a(x*_u)ˋ，此 leader 決策可行且價值不低於 ˋF^Bˋ，再由 P1。(⇒) 取達成 ˋF^{C,m} = F^Bˋ 的 leader 決策；樂觀取各部門最佳回應中企業貢獻最大者，悲觀取 ˋF_uˋ 最大者並以逐部門加總論證（所選剖面在 B 中可行，其加總不超過 ˋF^Bˋ，故每一部門的企業貢獻恰等於其最佳回應集合上的最小值），再把 envelope 縮為該計畫的資源向量。此證明對任一形如 ˋ{F_u ≥ g(max F_u)}ˋ（ˋgˋ 非遞減、ˋg(m) ≤ mˋ）的平手規則成立，涵蓋求解器 51 的相對容差，但只限精確可負擔；51 另允許的 1e-9 資源容差不在範圍內（理論補充包 15 的兩計畫例）。判定需要全部首佳解。 ⏎ - **Cor DL-2o（推論；多部門、AL3、精確平手）。** 若 ˋDL^opt > 0ˋ，則在任一支持首佳解的 ˋ(y*, γ*)ˋ 上、取 ˋΣF_uˋ 最大的首佳剖面 ˋx°ˋ，某一部門的最佳回應集合 ˋBR_u(a(x°_u))ˋ 中每一個計畫都對 ˋx°_uˋ 構成嚴格逆轉（ˋF_uˋ 較高、企業貢獻較低）且 envelope 不可分離。 ⏎ - **Cor DL-2p（推論；AL3；精確平手）。** 若 ˋDL^pess > 0ˋ，每一首佳解都有某一部門存在弱逆轉（ˋF_uˋ 不低、企業貢獻較低）且不可分離的偏離；嚴格逆轉不是必要（W3b）。 ⏎ - **Cor DL-3（推論；唯一首佳 H0；精確平手）。** Part (i)：在唯一首佳下，若首佳計畫在 C 中皆可行，則 ˋDL^optˋ 為正若且唯若某一部門存在 ˋa(x^H) ≤ a(x*_u)ˋ 且 ˋF_u(x^H) > F_u(x*_u)ˋ 的計畫，ˋDL^pessˋ 為正若且唯若存在 ˋx^H ≠ x*_uˋ、ˋa(x^H) ≤ a(x*_u)ˋ 且 ˋF_u(x^H) ≥ F_u(x*_u)ˋ 的計畫（企業貢獻較低自動成立）。Part (ii)：若某一首佳計畫違反部門專屬限制，兩種界的 DL 皆為正。此原始條件刻畫只在唯一首佳下成立。 ⏎ - **Prop DL-4（命題；多部門、AL3、精確平手）。** (a) 若所有不可分離的計畫對上都沒有弱逆轉，則 ˋDL^opt = DL^pess = 0ˋ；(b) 若只排除嚴格逆轉，則 ˋDL^opt = 0ˋ（ˋDL^pessˋ 可為正，W3b）；(c) 序數對齊蘊含 (a)，P2 為其特例。*證明（修正後）：* 對任一首佳解取 ˋe_u = a(x*_u)ˋ，直接證明 ˋV^m(a(x*)) ≥ F^Bˋ。AL3 不成立時 (b)(c) 不成立（W_DL_AL3）。 ⏎ - **Prop DL-5（命題；AL3）。** ˋDL^m ≤ min over 𝓑* of Σ_u [φ^E_u(x*_u) − v^m_u(a(x*_u))]ˋ，各項非負；W3 達成此上界。 ⏎ - **Prop DL-6（命題；envelope 是上限）。** 容許 ˋx^Gˋ 的任一 envelope 都容許所有 ˋa(x) ≤ a(x^G)ˋ 的計畫。在 AL3 下，DL 恰來自兩個來源：採用不足（部門偏好較便宜的計畫，例如維持現況；W3m）與資源用量不高於目標的不利採用（W3）；AL3 不成立時另有部門專屬排除的管道（W_DL_AL3）。三者都無法以 envelope 修正；前兩者只有 ˋγˋ 或 ˋyˋ 能作用。 ⏎ - **反例與構造例。** W1（對齊：B = C = 30，DL = 0）；W2（不對齊但可阻擋：B = C = 15，DL = 0；不對齊不充分）；W3（不對齊且不可阻擋：B = 15、C = 10、DL = 5）；W3m（最小的採用不足：B = 2、C = 0）；W3b（DL^opt = 0 < DL^pess = 1，只由平手造成）；W3c（同一逆轉且不可分離的計畫對，加入第三個計畫後 DL 由 2 變為 0；成對存在性條件 (A)–(F) 的任何布林組合都不是 DL 正負號的充要判準）；W_DL_AL3（ˋF_u ≡ φ^Eˋ，只因部門專屬限制而 DL = 1）。 ⏎ - **狀態。** DL 必要條件：已建立（Lemma DL-1；Cor DL-2o／2p 在 AL3 與精確平手下）；DL 充分條件：已建立（DL = 0：Prop DL-4；DL > 0：唯一首佳下的 Cor DL-3）；不依賴首佳解的原始充要刻畫：NOT_PROVEN；平手容差：有條件成立（只限精確可負擔）。 ⏎ - **與 v2.2 的關係。** C.6 的 P2 備註（「需要池化資源」）依逐字原則保留；其精確條件為 Lemma S，第 3.12.4、5.6 節已改用此精確用語。 ⏎  ⏎ #### C.10.3 治理篩選（理論補充包 03） ⏎  ⏎ 定義（較寬鬆要求 ˋReq_lˋ、較嚴格要求 ˋReq_sˋ；賦能區塊固定；治理成本 ˋC_lˋ、ˋC_sˋ）：ˋPR_B = F^B(Req_l, C_l) − F^B(Req_s, C_l)ˋ；總篩選效果 ˋGSV^m = F^{C,m}(Req_s, C_l) − F^{C,m}(Req_l, C_l)ˋ；直接治理成本效果 ˋDGC^m = F^{C,m}(Req_s, C_s) − F^{C,m}(Req_s, C_l)ˋ；淨治理效果 ˋNGE^m = GSV^m + DGC^mˋ。 ⏎  ⏎ - **GS-0（重述：P7 加上治理成本管道）。** 在 B 中，相同成本下較嚴格要求只縮小可行集合（ˋPR_B ≥ 0ˋ）；較嚴格且較貴時淨效果更低；B 的任何淨增益只可能來自成本，不來自要求。B 沒有 follower，故 ˋGSV^B = −PR_B ≤ 0ˋ。 ⏎ - **Identity GS-I（恆等式）。** ˋGSV^m = DL^m(Req_l) − DL^m(Req_s) − PR_Bˋ（以 ˋF^C = F^B − DLˋ 代入）。 ⏎ - **Cor GS-I′（P1 與 P7 的推論）。** ˋGSV^m ≤ DL^m(Req_l)ˋ。 ⏎ - **Prop GS-1（命題；充分條件；AL3）。** 若嚴格要求保留某一寬鬆首佳解，且使其在自身資源向量下自我實施（悲觀時另排除平手的不利計畫），則 ˋGSV^m = DL^m(Req_l)ˋ（經由 Lemma DL-1，近乎定義性；唯一首佳下為原始條件形式）。 ⏎ - **Prop GS-2（命題）。** 只篩除一對逆轉不足以回收授權損失（W4d）。 ⏎ - **Thm GS-N（定理；必要條件；只在精確平手下以此精確形式成立）。** 相同成本與賦能下若 ˋGSV^m > 0ˋ，則 (i) ˋDL^m(Req_l) ≥ GSV^m > 0ˋ；(ii) 在嚴格要求的 C 最適 ˋyˋ 下，存在部門 ˋuˋ 與計畫 ˋx^G ∈ P_sˋ、ˋx^H ∈ P_l \ P_sˋ，使 ˋa(x^H) ≤ a(x^G)ˋ、ˋx^Hˋ 的企業貢獻較低、ˋF_u(x^H) > F_u(x^G)ˋ（樂觀）或 ˋ≥ˋ（悲觀），且 ˋx^Hˋ 是寬鬆要求下 envelope ˋa(x^G)ˋ 的部門最佳回應。*證明要點：* 取嚴格要求下的 C 最適決策並以 Lemma E′ 縮 envelope；此剖面在寬鬆要求下仍可行，逐部門比較並以 ˋBR_s = BR_l ∩ P_sˋ（此步需要精確平手）分情形。∎ ⏎ - **Cor GS-4（推論）。** 若所有逆轉對都可由 envelope 分離，則 ˋGSV^m ≤ 0ˋ。帳本對齊（無弱逆轉）時 ˋGSV ≤ 0ˋ；只無嚴格逆轉而有平手時，只保證 ˋGSV^opt ≤ 0ˋ（W4e：ˋGSV^pess = 1 > GSV^opt = 0ˋ）。 ⏎ - **構造例。** W4（P8 的 10 → 15；ˋGSV = DL_loose = 5ˋ、ˋPR_B = 0ˋ）；W4b（反向的 15 → 10，ˋGSV = −5 = −PR_Bˋ）；W4c（10 → 7：移除 DL = 5，但 ˋPR_B = 8ˋ）；W4d（10 → 9：成對篩除不足）；W4e（只在悲觀界為正的篩選）。 ⏎ - **狀態。** 不存在已證明的原始條件充要刻畫（NOT_PROVEN）。AI 特定的推論（不是新結果）：以 ˋEA^req(A, κ)ˋ 表達的篩選，只作用於授權深度使該要求綁住的配置。 ⏎  ⏎ #### C.10.4 共享能力重用（理論補充包 04） ⏎  ⏎ - **Thm D1（重述：P4 之 B 部分的明確形式）。** 在 (A1) 以能力來源為索引、(A2) ˋδˋ 只降低共享狀態格的成本、(A3) 候選集合不隨 ˋδˋ 改變、(A4) 沒有 follower、(A5) ˋF_cˋ 等不隨 ˋδˋ 改變的前提下，B 的建置區域為上集。構造例 W5b 顯示 (A1) 是必要的前提（以可用與否為索引時 B 也可出現 1 → 0 → 1）。 ⏎ - **Lemma I（引理；Lemma E′ 讀為可實施性條件；原稱 Lemma S，為避免與 C.10.2 混淆而改名）。** C 在 ˋy_c = 1ˋ 分支的值，等於各部門只取可實施計畫時的背包最適值。精確平手。 ⏎ - **Thm D3（重述：P2 逐點於 ˋ(y, γ)ˋ）。** (AL1)–(AL4) 下，C 在每一 ˋ(y, γ)ˋ 的值等於 B，故 C 的建置區域與 B 相同（兩種界、任何平手、任何跨部門耦合）。 ⏎ - **Prop D4、D5（命題）。** 只有 ˋδˋ-相依格所屬的部門對齊即足夠（D4）；偏好、資源順序與平手類內的企業貢獻順序不隨 ˋδˋ 改變亦足夠（D5）。因此 v2.2 P4 的「只有 (AL) 成立時才保證」中，(AL) 是充分而非必要條件。 ⏎ - **Prop D6（命題；存在性）。** 存在滿足 (A1)–(A3)、(A5)，只違反一部門 (AL1) 的 C 實例，其建置區域在兩種界與兩種平手慣例下都不是區間；同一實例的 B 建置區域是區間。構造例 W5：ˋD(δ) = 1 + δˋ（ˋ[0,3)ˋ）、ˋδ − 4ˋ（ˋ[3,5]ˋ）、ˋ1ˋ（ˋδ ≥ 5ˋ），嚴格慣例的區域為 ˋ[0,3) ∪ (4,∞)ˋ，平手即建置慣例為 ˋ[0,3) ∪ [4,∞)ˋ；格點序列 1,1,1,1,0,0,0,1 與 51 T-SEN-8 一致。投資決策不必對重用效益單調。 ⏎ - **Lemma M（引理）。** 單一部門、單一 initiative、兩個選項，且資源用量非負、能力對現況沒有效果時，建置區域為上集。 ⏎ - **Conjecture M2（猜想；NOT_PROVEN）。** 均一重用下，只有一個部門、一個 initiative 時不論選項多少都無法產生 1 → 0 → 1 型態，此型態需要兩個以上的部門決策單位；只有有界搜尋的支持（三選項 6,912 個實例中找到 0 個），不是證明。 ⏎ - **用量前提與構造例的穩健性（R-4）。** 非單調需要重用使不對齊部門的 AI 配置在每一項池化資源（含 ENG）上的淨用量都不高於企業偏好的計畫（此處為現況）。主要（canonical）構造例為 W5：逐點重現 T-SEN-8，在全部八個純量同時 ±5% 的確定性擾動下保留非區間區域 162/400 次（主要報告值；邊際 1 TWD）。擴大邊際的側車構造例 W5_WIDE（區域 ˋ[0,4) ∪ (7,∞)ˋ，邊際 3）在相同擾動下保留 367/400 次，只是敏感度分析（擴大構造例），不作為主要結果，也不取代 W5；兩者依賴同樣的兩個結構零點（淨 BUD 用量不高於現況、ENG 用量為 0）。 ⏎ - **與 v2.2 的關係。** C.6 的 P4 原文逐字保留；D4、D5 是對其「只有 (AL)」措辭的精確化，而非矛盾。W5 是 P8 型的情境：排除 U2 之 AI 配置的規則可使 ˋF^Cˋ 回到 ˋF^Bˋ；治理篩選與重用非單調是同一種 envelope 分離失效。 ⏎  ⏎ #### C.10.5 VOI 與序列識別（理論補充包 05） ⏎  ⏎ - **Lemma 0（重述：v2.2 §13.2 的頂點精確性）。** 在乘積型參數集合、價值區塊多線性與固定有限候選集合下，各候選的 MaxRegret 與 MMR 在頂點上精確。 ⏎ - **Prop E.1（命題）。** 固定候選集合下，ˋΘ' ⊆ Θˋ 蘊含 ˋMMR(Θ') ≤ MMR(Θ)ˋ。候選集合隨 ˋΘˋ 重算時不成立（W6b：MMR 由 0 升為 1）。 ⏎ - **Prop E.2（重述並明示前提）。** 固定候選集合下 ˋ0 ≤ VOI^true ≤ VOI^grid ≤ VOI^vertex ≤ MMRˋ；候選集合重算時 VOI 可為負（W6b：ˋVOI_q = −1ˋ）。 ⏎ - **Prop E.3（重述：T-SEN-7）。** 頂點版 VOI 可能高估：解析 oracle 中頂點版為 1、真值為 1/2（合成解析反例，SYNTHETIC ANALYTIC COUNTEREXAMPLE；最小構造例 W6 為兩個候選 × 兩個區塊）。 ⏎ - **Prop E.4（命題）。** 真值 VOI 可由有限點列舉精確計算（尺度區塊的直線排列斷點；機率區塊的超平面排列頂點；後者已證明但未實作）。 ⏎ - **Prop E.5（命題；只為充分條件）。** 若某一候選在區塊的每一個值下都屬 minimax-regret 最適集合，則頂點版 VOI 精確；逆命題 NOT_PROVEN。 ⏎ - **Prop E.6（命題與反例）。** 巢狀網格使上界單調不增；非巢狀網格不必（W6c：網格 4 → 5 由 1/2 變為 3/5）；51 只取邊上點的機率區塊網格在三個以上頂點時不收斂（W6c：網格值不低於 1/2，真值為 1/3）。 ⏎ - **Thm E.7（定理）。** 若每一區塊可達的證據狀態有限、每次量測嚴格縮小狀態，則序列識別程序在有限步內終止。**Remark E.8（反例 W6f）。** 沒有離散化時可能不終止，且穩定性規則可能誤觸發。 ⏎ - **短視性（反例 W6e）。** 每一區塊的單一 VOI 皆為 0，聯合識別卻使 MMR 由 1 降為 0；只依單一區塊 VOI 的停止規則不是最適停止規則。 ⏎ - **Prop E.10（重述）。** 規則 B（認證的最適 portfolio）⇔ ˋMMR = 0ˋ ⇔ 某一候選的 Lemma R 整體證書成立（固定候選集合）。 ⏎ - **序列識別程序（程序，不是定理）。** 以固定候選集合為主、重算候選集合只作次要診斷（ˋCANDIDATE_SET_EXPANDEDˋ）；需要版本化的 registry。合成側車中，依 VOI 排序的量測並未在殘餘 regret 上優於隨機順序（SIMULATED_ONLY）。依 VOI 由大到小量測的最適性 NOT_PROVEN。序列識別性質的狀態為 PARTIAL。 ⏎  ⏎ #### C.10.6 穩健性範圍（理論補充包 06） ⏎  ⏎ - **Thm R1（重述：Lemma R 的明確前提 (R-a)–(R-e)）。** 整個 portfolio、價值為 ˋθˋ 的固定函式（B、A+）；價值對每一單一因子類區塊為仿射；ˋΘ_gˋ 為區塊多面體的乘積；候選集合固定且皆 ROBUSTLY_FEASIBLE；弱最適。在此之下，整個 portfolio 在 ˋΘ_gˋ 內恆最適若且唯若在所有頂點剖面上不劣於每一競爭者。**Cor R1a、R1b（重述）**：MaxRegret 與 ˋλˋ 盒證書。 ⏎ - **Prop R2（命題；精確刻畫）。** 元素值 ˋd°ˋ 在 ˋΘ_gˋ 內恆最適，若且唯若含 ˋd°ˋ 之 portfolio 的最適區域覆蓋 ˋΘ_gˋ；檢查覆蓋需要切換面的排列，不只頂點。 ⏎ - **Prop R3（命題；最小反例）。** 元素層級的頂點檢查不精確；最小實例為三個 portfolio × 一個區塊（T-SEN-3：ˋθˋ、ˋ1 − θˋ 與 0.6；頂點判為 ROBUST，在 ˋ(0.4, 0.6)ˋ 內為 FRAGILE；構造例 W7）。 ⏎ - **Prop R4（命題）。** 若恰一個候選 portfolio 含該元素值，頂點檢查同時是充分與必要條件。 ⏎ - **Prop R5（命題）。** Model C 即使固定 leader 決策也不具頂點精確性：(i) 對齊且資源向量不隨 ˋθˋ 改變時，價值為區塊凸，但仍屬元素型問題；(ii) 不對齊時悲觀值可在部門切換面上不連續；(iii) 隨 ˋθˋ 改變的部門可行性另增切換面（W7 的 (b)(c)）。 ⏎ - **範圍句。** 頂點精確性只適用於 B（及 A+）的整個 portfolio、MaxRegret 與 ˋλˋ 盒；不適用於元素層級（除 R4 的情形）、任何經部門最佳回應決定的 C、C0、A 量（leader 決策、ˋF_E^{C}ˋ、DL、NEV）、含相依限制的參數集合，或只是條件可行的候選。 ⏎  ⏎ #### C.10.7 缺值分類（理論補充包 07） ⏎  ⏎ - **Def G（定義）。** 對缺值參數 ˋpˋ 及其可接受集合 ˋV_pˋ，以 0 填補得 ˋθ^0ˋ：DC（改變決策：某一可接受值使以 0 填補的最適決策不再最適或不可行）；DIER（以 0 填補的每一最適決策在所有可接受值下仍為最適，但價值或可行集合未被點識別）；NULL（結果物件不變）；FC（可行集合隨可接受值改變）為正交的通道標記。改變目標或排序者為 DC 且非 FC；改變可行性者帶 FC；不改變決策但具認識上重要性者為 DIER。 ⏎ - **Prop G1（命題；前提已修正）。** 在 B 中，若 ˋpˋ 以同一方向影響限制與目標：使用量或要求門檻的 0 填補虛構可行性（樂觀偏誤），容量或許可的 0 填補虛構不可行性（悲觀偏誤）；在 C 中不成立（P8 機制）。 ⏎ - **Prop G2（命題）。** B 中 ˋRESTRICTED_SOLVEˋ 的值是所有可接受值下最適值的下界；C 中不是（W8a 第二部分）。 ⏎ - **Prop G3（命題）。** B 中只影響單一選項的單調缺值格具門檻型決策對應；0 填補為該選項的最佳端點、受限求解為最差端點。 ⏎ - **Prop G4（命題；量詞已修正）。** ˋλˋ 盒在 B／A+ 中：DC 若且唯若某一以 0 填補的最適決策在某一頂點不最適；否則依價值與最適集合是否在盒上不變區分 NULL 與 DIER；三者皆可由頂點檢查判定；C 只能以網格判定。 ⏎ - **Prop G5（命題；即 P4）。** ˋF_cˋ 的 ˋTHRESHOLD_MODEˋ 是精確的識別決策對應。 ⏎ - **Prop G6（命題）。** 帳本拆分缺值對 B 為 NULL、對 C 可能為 DC（W8b 第二部分）。 ⏎ - **Remark G7（說明；修正第 3.14.3 節原措辭）。** 單一 initiative、ˋN_j0 = N_j1 = 1ˋ 時，ˋφ_j0 = 0ˋ、ˋφ_j1 = g_1 − x − C^implˋ（ˋxˋ 為現況每事件價值），故 ˋk = 1ˋ 最適若且唯若 ˋx < g_1 − C^implˋ（W8b 第三部分：ˋx < 4ˋ）。現況結果格進入「維持現況或切換」的比較，只在所比較的 portfolio 對 ˋjˋ 是否維持現況的選擇相同時才抵銷。v2.2 §13.4 將缺現況格標為 ˋUNEVALUABLE_INITIATIVEˋ，與此一致；v1.8.5a 第 3.14.3 節優先序 (4) 的「抵銷」理由不成立，v1.8.6 已改為條件性陳述。 ⏎ - **Prop G8（命題）。** 若 ˋ0 ∉ V_pˋ，以 0 填補落在可接受集合之外，其結果不屬任何識別集合。 ⏎ - **定位與狀態。** 方法論／模型識別的貢獻，不是 AI 組織理論；C 中連續缺值格的 DIER 只在被評估的點上成立，多選項缺值格沒有一般的區間界定結果。 ⏎  ⏎ #### C.10.8 構造例索引（理論補充包 09） ⏎  ⏎ 全部構造例由單一標準函式庫程式 ˋq1_theory_witnesses.pyˋ 計算，27/27 PASS，與 51 基準的 7 項交叉檢查全部 PASS，構造例集合雜湊前綴 ˋa68664ceˋ，重複執行逐位元組相同；全部為 ˋSIMULATED_ONLYˋ 的代數構造，不是一般定理的證明，也不是企業實證證據。主要構造例 W1–W7 見表 4-20D。補充構造例：W3m、W3b、W3c、W_DL_AL3（C.10.2）；W4b、W4c、W4d、W4e（C.10.3）；W5b、W5_WIDE（C.10.4；W5_WIDE 只作敏感度分析）；W6b、W6c、W6d、W6e、W6f（C.10.5）；W8a、W8b、W8c（C.10.7）；W_MECH_ABL（C.10.1）。資訊不對稱側車的構造例只屬側車設計（SIDECAR_DESIGN_ONLY），不是 v2.2 或本論文的結果，不列入第四章。 ⏎  ⏎ #### C.10.9 勘誤：Lemma E′ 悲觀情形的證明用語（只改用語） ⏎  ⏎ - **位置。** C.2 逐字收錄的 v2.2 證明中，悲觀情形一句為「Pessimistic leader：取任一 ˋx ∈ Tˋ」。C.2 依本附錄的逐字原則保留不改；本勘誤記錄其用語的修正，並已套用於第 3.12.6 節的說明文字。企業模型規格 v2.2 與求解器 51 本身不修改（凍結的正式版本），是否在下一個正式版本修正由研究者決定。 ⏎ - **問題。** 在精確平手下，ˋTˋ 的每一個元素都是 ˋF_uˋ 最大者，原句成立。在預先登記的平手容差 ˋε_tie > 0ˋ（v2.2 預設為相對容差）下，若取 ˋTˋ 中只是落在容差內、但非最大的元素並把 envelope 縮為其資源向量，新集合上的最大值可能下降，平手門檻隨之下降，ˋT'ˋ 可能納入原本不在 ˋTˋ 中的計畫，悲觀值可能下降。理論補充包 13 的三計畫反例中，悲觀值由 10 降為 −100；改取 ˋF_uˋ 最大者則維持 10。 ⏎ - **修正後的用語。** Pessimistic leader：取 ˋxˋ 為 ˋTˋ 中部門目標最大者（ˋF_u(x) = max_S F_uˋ）；此時 ˋS'ˋ 仍含最大值點，最大值不變，ˋT' = T ∩ S' ⊆ Tˋ，故 ˋT'ˋ 上的最小企業貢獻不小於 ˋTˋ 上的最小值。Optimistic leader 在容差下取 ˋTˋ 中企業貢獻最大者仍成立（該點仍在 ˋT'ˋ，optimistic 值弱增；精確平手下不變）。 ⏎ - **範圍。** 修正後的證明對任一形如 ˋ{F_u ≥ g(max_S F_u)}ˋ、ˋgˋ 非遞減且 ˋg(m) ≤ mˋ 的平手規則成立，涵蓋精確平手、任何絕對容差與 51 的相對容差；但只在精確可負擔（ˋa(x) ≤ eˋ）下成立，51 另允許的 1e-9 資源容差不在範圍內。 ⏎ - **影響。** Lemma E′ 的陳述、所有方程、目標、可行集合、P1–P8 與 51 的所有計算數值皆不變：51 列舉每一個計畫的資源向量（含 ˋF_uˋ 最大者），只依賴 Lemma E′ 的陳述，不依賴證明中 ˋxˋ 的特定選法。 ⏎ `

### inserted — 59a l.3074 → 01 l.3240

- ⊕ `| v1.8.6／Q1 理論補充包 01–15 | — | ˋ01_Q1_M1_M4_MECHANISM_THEORY.mdˋ 至 ˋ15_Q1_T7_REPAIR_VERIFICATION.mdˋ（研究庫 ˋclaude/r14_merge_q1_theory_upgrade_v1/ˋ）、ˋq1_theory_witnesses.pyˋ、ˋq1_theory_witnesses_output.txtˋ | Q1 理論補充：形式結果、紅隊審查、回應紀錄、修正驗證與 27 個構造例（SIMULATED_ONLY）；不修改企業模型規格 v2.2（42）與求解器（51） | 第 1.7.2、3.9.6、3.12.4、3.13、3.14.3、4.9.1、5.6–5.8 節；附錄 C.10 | ⏎ | v1.8.6／01–03 | — | ˋ01_V1_8_6_THEORY_INTEGRATED_MANUSCRIPT.mdˋ（另有 ˋ02_V1_8_6_CHANGELOG.mdˋ、ˋ03_V1_8_6_DIFF_SUMMARY.mdˋ） | 合併論文 v1.8.6（理論整合版；v1.8.5a 為修訂底稿） | 本稿 |`

### inserted — 59a l.3129 → 01 l.3297

- ⊕ `| E51 | Q1 理論補充（第 3.12.4、3.13、5.7 節；附錄 C.10）的相關文獻定位尚未查證 | 這些形式結果在正文只以本研究的模型內結果（TYPE C）陳述 | 相關文獻經查證並加入參考文獻之前，正文不引用、不比較，也不據以主張新穎性 |`



## Addendum: T51 (orchestrator, re-audit item n1)

After the TA re-audit (01 sha256 bb0fa9e3…; MAJOR=0, MINOR=1), the single cosmetic item n1 was fixed: §3.9.6 「…以及 AI 對 AI 的輸出鏈，以及時間（跨期）維度」 → 「…、AI 對 AI 的輸出鏈，以及時間（跨期）維度」. It is folded into patch T38 (work/MI/ta_patches.py). Rebuilding 01 from 59a reproduces the edited file byte for byte. Final 01 sha256 = 94d41d5682818953912784d0e870d58d1e4c418e7261b619d5c73485dfee82f4. verify_v186.py: 71/71 hard checks PASS (work/MI/verify_out.json).
