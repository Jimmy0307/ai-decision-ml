# 32 — Patch Log v1.8.1 → v1.8.2 (V1 PREFREEZE CANDIDATE)

- Input: `claude/r14_merge_v1_8_1_study1_freeze/16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.md` sha256 `cddeb89b07439ff2bba9af1ba119824cb1cf815c4fc8a78e084900cd24e06bda` (asserted).
- Output: `32_MERGED_MASTER_THESIS_v1_8_2_V1_PREFREEZE_CANDIDATE.md` sha256 `2d493edc2e1884f05e5b0617bc56f1f85cdab0fa33531ac566b61d343dd8f159`.
- Method: `tools/K/patch_v182.py` — 19 exact old→new replacements, each asserted to match exactly once in v1.8.1 and once at apply time. Verification: `tools/K/verify_v182.py` → `tools/K/verify_out.json`. This log: `tools/K/build_log_v182.py`.
- Scope: V1 design/status wording only. No equation, network value, G01–G16 row, G→M researcher assignment, VCP/VSC/DL/NEV, enterprise model, Study 1 freeze statement, heading, or result was changed. No human result, simulated value or expected α/κ was inserted. No DOCX built.

## Changes

| ID | v1.8.1 line | v1.8.2 line | Section | Category | Source |
|---|---|---|---|---|---|
| K01 | 5 | 5 | 稿件狀態 | version label | this round (output 32); Appendix D row K16 |
| K02 | 5 | 5 | 稿件狀態 | V1 status wording | OUT 24 (D-1..D-15); OUT 25 §10 (supersession); OUT 27 HUMAN_VALIDATION_EXECUTED=NO |
| K03 | 5 | 5 | 稿件狀態 | V1 gate status wording | OUT 25 Status; OUT 27 |
| K04 | 15 | 15 | 摘要 | V1 design wording (coder count) | OUT 24 (D-1..D-15) D-3; OUT 25 Status |
| K05 | 749 | 749 | 3.9.3 V1 獨立盲編設計 | V1 design rewrite (v1.8.2) | OUT 24 (D-1..D-15); OUT 25 §1, §3–§8; OUT 26 §1–§4; OUT 28 §1–§3; OUT 29 §0–§6 |
| K06 | 757 | 757 | 3.9.4 AI 盲編 pilot 與爭議格 | added sentence (sensitivity targets not marked) | OUT 29 §6.1; OUT 24 D-9 (sensitivity marker excluded); OUT 27 SENSITIVITY_TARGET_MARKERS_VISIBLE=NO |
| K07 | 1336 | 1336 | 3.14.4 表 3-14（V1 列） | V1 design/status wording | OUT 24 (D-1..D-15) D-3, D-5..D-8; OUT 29 §0–§6 |
| K08 | 1336 | 1336 | 3.14.4 表 3-14（V1 列） | V1 status wording | OUT 25 Status; OUT 27 |
| K09 | 1344 | 1344 | 3.14.4 表 3-14 表註 | V1 status wording | OUT 25 Status |
| K10 | 1693 | 1693 | 4.7 狀態 | V1 status wording | OUT 25 Status; OUT 27 HUMAN_VALIDATION_EXECUTED=NO |
| K11 | 1699 | 1699 | 4.7 回填規則 | V1 analyzer reference | OUT 25 §10; OUT 30 §5; tools/no_human_data_run_v1_8_2/ (output filename) |
| K12 | 1738 | 1738 | 4.7.3 表 4-13 | placeholder table restructured to 3-coder design (all cells pending) | OUT 29 §0–§6 §1–§4; OUT 30 §4–§5; OUT 28 §3 |
| K13 | 1752 | 1754 | 4.7.3 表 4-14 | placeholder table restructured to 3-coder design (all cells pending) | OUT 29 §0–§6 §2 (per item, confusion matrices), §5 |
| K14 | 1772 | 1774 | 4.7.3 表 4-15 說明 | V1 analyzer/phase wording | OUT 29 §0–§6 §6; OUT 25 §7 |
| K15 | 1775 | 1777 | 4.7.3 表 4-15 說明 | V1 continuity-label wording (OA-2) and status | OUT 24 (D-1..D-15) D-1; OUT 29 §0–§6 §2.B, §6.3 |
| K16 | 1778 | 1780 | 4.7.3 表 4-15 說明 | V1 status wording | OUT 25 Status; OUT 27 |
| K17 | 3022 | 3024 | 附錄 D（v1.8.1／16 列） | artifact table (this file no longer 本稿) | this round |
| K18 | 3024 | 3026 | 附錄 D（v1.8.1／19–21 列 + v1.8.2 列） | artifact table (supersession + new v1.8.2 rows) | OUT file list (24–30, coder_distribution, tools); this round |
| K19 | 3035 | 3044 | 附錄 E6 | V1 design/status wording | OUT 24 (D-1..D-15) D-3, D-8, D-10, D-15; OUT 30 §1 |

## Old → new text

### K01 — 稿件狀態 (v1.8.1 L5 → v1.8.2 L5)

Source: this round (output 32); Appendix D row K16

OLD:

```text
合併碩士論文 v1.8.1 CLEANUP CANDIDATE（由 v1.8 修訂；v1.0–v1.8 保留、未覆寫；
```

NEW:

```text
合併碩士論文 v1.8.2 V1 PREFREEZE CANDIDATE（由 v1.8.1 修訂；v1.0–v1.8.1 保留、未覆寫；
```

### K02 — 稿件狀態 (v1.8.1 L5 → v1.8.2 L5)

Source: OUT 24 (D-1..D-15); OUT 25 §10 (supersession); OUT 27 HUMAN_VALIDATION_EXECUTED=NO

OLD:

```text
並備妥 V1 人類構念效度驗證封包（V1.8.1 檔案 19–21；狀態 READY_TO_RUN：已備妥、尚未執行，沒有任何人類編碼結果）。
```

NEW:

```text
並備妥 V1 人類構念效度驗證封包（V1.8.1 檔案 19–21）。v1.8.2 只更新 V1 人類構念效度驗證的設計與狀態描述：依研究者決策紀錄（V1.8.2 檔案 24），V1 改為三位獨立人類編碼者、不使用 AI 編碼者、編碼者材料遮蔽 G 編號的設計；協定、編碼手冊、分析計畫與封包已於 S1 凍結（人類編碼前；V1.8.2 檔案 25–30），封包已備妥待發送；人類編碼尚未執行，沒有任何人類編碼結果；V1.8.1 的 19–21 封包顯示 G 編號，已被取代、不得發送。
```

### K03 — 稿件狀態 (v1.8.1 L5 → v1.8.2 L5)

Source: OUT 25 Status; OUT 27

OLD:

```text
V1 為 AI PILOT COMPLETE；HUMAN BLIND CODING PENDING；V3–V6
```

NEW:

```text
V1 為 AI PILOT COMPLETE；HUMAN BLIND CODING PENDING（協定已於 S1 凍結、人類編碼尚未執行）；V3–V6
```

### K04 — 摘要 (v1.8.1 L15 → v1.8.2 L15)

Source: OUT 24 (D-1..D-15) D-3; OUT 25 Status

OLD:

```text
AI 盲編 pilot 對 G04、G10、G11 提出與研究者不同的編碼，人類雙人盲編尚待完成。
```

NEW:

```text
AI 盲編 pilot 對 G04、G10、G11 提出與研究者不同的編碼；三位獨立人類編碼者的盲編協定已凍結，人類編碼尚未執行。
```

### K05 — 3.9.3 V1 獨立盲編設計 (v1.8.1 L749 → v1.8.2 L749)

Source: OUT 24 (D-1..D-15); OUT 25 §1, §3–§8; OUT 26 §1–§4; OUT 28 §1–§3; OUT 29 §0–§6

OLD:

```text
研究者裁決必須由獨立編碼者檢驗，本研究稱為 V1（構念效度）。V1 的協定在任何編碼輸出產生之前凍結並記錄雜湊值，內容如下。(1) **編碼材料。** 編碼者只收到協定、一份盲編封包（16 個個案，每個個案只列一個人工智慧功能家族與一個決策功能家族的定義；兩份封包的列序不同）與空白回答表。編碼者在其編碼凍結前不得看到缺口編號、研究者的機制與狀態裁決、任何論文文字，也不得看到 O/E、觀察計數或 p 值，以免以效果強度定錨；人類編碼者須簽署未閱讀相關文件的聲明。(2) **編碼內容。** 每個個案編一個主碼（M1–M5、資料條件型、僅證據層、其他機制或資訊不足）、至多一個次碼、狀態（static、dynamic、optional、evidence-only、insufficient）與信心值；編碼者不必把每個個案放進 M1–M5。(3) **信度。** 主碼與狀態分開計算：兩位編碼者時報告一致數與 J. Cohen（1960）的 κ，並同時報告 Krippendorff 的 α（名目；Krippendorff, 2004），以 5,000 次個案自助法求 95% 區間；判定以 α 為準：α ≥ .800 為 RELIABLE，.667 ≤ α < .800 為 TENTATIVE，α < .667 為 NOT_ACCEPTABLE；α 的區間下界低於 .667 時另標為 IMPRECISE，須增加編碼者（.800／.667 兩個門檻依 Krippendorff, 2004，為預先登記的研究慣例；NOT_ACCEPTABLE 與 IMPRECISE 兩類為本研究的操作化）。次碼只以 {主碼 ∪ 次碼} 的 Jaccard 一致度描述，信心值不作加權。(4) **裁決。** 分歧先由編碼者在不看答案鍵的情況下討論，再交由非轉譯作者的裁決者裁決；研究者答案鍵視為假設而非真值，只在裁決結果凍結後才開啟；若由轉譯作者裁決，列為研究限制。凡最終碼與研究者答案不同的個案，都要分類為「只影響對應（mapping-only）」「只影響論文敘述」或「影響模型結構（model-structural）」。(5) **通過條件。** 只有在至少兩位人類編碼者、主碼信度至少 TENTATIVE 且非 IMPRECISE、狀態信度至少 TENTATIVE，且沒有未解的模型結構性變更時，才判定 V1 通過（`V1_PASS_HUMAN_C6`）。AI 編碼者即使達到相同門檻，也只能得到「AI 盲編 pilot 可接受」，永遠不構成 V1 通過。
```

NEW:

```text
研究者裁決必須由獨立編碼者檢驗，本研究稱為 V1（構念效度）。V1 的協定、編碼手冊、分析計畫與分析程式在任何人類編碼產生之前凍結（階段 S1），並以 SHA-256 記錄雜湊值；v1.8.2 的設計如下（V1.8.2 檔案 24–29）。(1) **範圍與研究問題。** V1 只檢驗「缺口 → 企業機制」的轉譯解讀，不檢驗 32 格的成員資格、分類體系的正確性或文獻網路的統計量。主要問題是編碼者間信度，即三位獨立的人類編碼者是否把同一配對歸入同一企業決策類別；與研究者答案鍵的一致是另一個問題，只在答案鍵開啟之後才比較。(2) **編碼者與材料。** 編碼者為三位獨立的人類，不使用 AI 編碼者。每個項目只以中性的項目編號呈現，缺口編號（G 編號）不出現在任何編碼者材料中；項目編號由以秘密種子產生的隨機排列指派，項目編號與 G 編號的對照表由研究團隊密封保管，每位編碼者的項目順序也各自以種子隨機排列。每個項目只列一個人工智慧功能家族與一個決策功能家族的定義、一句標準的不足呈現陳述與中性的證據描述；編碼者在其編碼凍結前不得看到研究者的機制與狀態裁決、AI pilot 的編碼、任何論文文字，也不得看到 O/E、觀察計數或 q 值，以免以效果強度定錨。(3) **盲性聲明。** 每位編碼者填寫七項聲明：未讀過公開的研究儲存庫、未讀過論文或稿件、未看過研究者的 G→M 對應、未看過 AI pilot 的輸出、未與其他編碼者商量、未使用任何 AI 工具作答，以及獨立完成編碼。任一項曝露即標為 EXPOSED；曝露的編碼者不會被默默併入分析：主要範圍只含未曝露的編碼者，含與不含曝露者的結果分開並列報告。(4) **編碼工具（Q1–Q5）。** Q1 判斷該配對是否對應可辨識的企業決策介面（YES、NO、UNCERTAIN）；Q2 從一組平面類別中選一個：M1、M2、M3、M4、LONGITUDINAL（跨期）、DATA_GATED（資料條件）、EVIDENCE_ONLY（僅證據層）、NONE 或 AMBIGUOUS；Q3 為對 Q2 的信心（HIGH、MEDIUM、LOW）；Q4 為選填的次要類別；Q5 為一至三句的理由。NONE 的定義是：存在可辨識的企業決策介面，但 M1–M4、LONGITUDINAL 與 DATA_GATED 都不足以表達；它要求 Q1 = YES，且 Q5 須寫出未被涵蓋的企業決策。證據不足或兩類並列時不使用 NONE（改用 AMBIGUOUS 或 Q1 = UNCERTAIN），沒有獨立的介面時也不使用 NONE（改用 EVIDENCE_ONLY）。(5) **信度。** 主要指標是 Q2 的 Krippendorff α（名目；Krippendorff, 2004），以全部 16 個項目、三位編碼者計算，並報告以項目為單位、5,000 次自助法的 95% 區間、原始一致率與各類別次數。次要指標是兩兩編碼者配對的 J. Cohen（1960）κ，各附自助法區間。Q1 報告 α 與兩兩 κ，不作通過或不通過的判定；Q3 只作描述，永不作為權重；Q4 只以 {Q2 ∪ Q4} 的集合 Jaccard 一致度描述。判讀以 Q2 的 α 點估計為準：α ≥ .800 為 RELIABLE，.667 ≤ α < .800 為 TENTATIVE，α < .667 為 UNRESOLVED/NOT_ACCEPTABLE；α 的區間下界低於 .667 時另標為 IMPRECISE。這些門檻是本研究預先登記的研究慣例，不是普遍適用的標準（出處的核對見附錄 E4）。(6) **與 53B 協定的延續性。** 由 Q2 推導的 53B 主碼與狀態，以及 `V1_PASS_HUMAN_C6` 標籤，只作為次要的延續性指標，與主要結果分節報告（CURRENT_INSTRUMENT_RELIABILITY 與 53B_CONTINUITY_RELIABILITY），兩者不合併；如協定所載："V1_PASS_HUMAN_C6 is a continuity label under the earlier 53B protocol, not evidence that the amended Q1–Q5 instrument is identical to 53B."(7) **階段與裁決。** 執行依序為 S1（封包凍結）→ S2（三份回收編碼表凍結）→ R（信度計算，只用中性項目編號，答案鍵與項目對照表保持密封）→ A（裁決）→ S3（裁決結果凍結）→ K（開啟研究者答案鍵）→ C（mapping-sensitivity 分類）。分歧先由編碼者在不看答案鍵的情況下討論，再交由非轉譯作者的裁決者裁決；研究者答案鍵視為假設而非真值，在 S3 之後才開啟，其雜湊須等於預先承諾值；若由轉譯作者裁決，列為研究限制。凡最終碼與研究者答案不同的個案，都要分類為「只影響對應（mapping-only）」「只影響論文敘述」或「影響模型結構（model-structural）」。AI 編碼者不參與 V1；先前的 AI 盲編 pilot（第 3.9.4 節）只是診斷，即使達到相同門檻也永遠不構成 V1 通過。(8) **盲性的限制。** 研究儲存庫在編碼開始之前即已公開，研究者的對應可在其中讀到，讀過儲存庫的人可能由功能家族配對辨認出項目；因此本研究不主張完美的盲性。緩解方式是只招募未曾接觸儲存庫、論文稿件與 AI pilot 輸出的編碼者，並以七項聲明記錄；自我聲明無法查證，列為研究限制。目前狀態：協定已於 S1 凍結（人類編碼前），封包已備妥待發送，人類編碼尚未執行，結果待完成。
```

### K06 — 3.9.4 AI 盲編 pilot 與爭議格 (v1.8.1 L757 → v1.8.2 L757)

Source: OUT 29 §6.1; OUT 24 D-9 (sensitivity marker excluded); OUT 27 SENSITIVITY_TARGET_MARKERS_VISIBLE=NO

OLD:

```text
「三格皆只影響對應」的判定也只是目前設計下的性質，須在人類盲編完成後重新檢查。
```

NEW:

```text
「三格皆只影響對應」的判定也只是目前設計下的性質，須在人類盲編完成後重新檢查。G04、G10、G11 已預先登記為 V1 的敏感度分析對象（S3 之後以 16 項對 13 項重算，16 項的結果仍為判定基準），但編碼者材料中不標示這三格。
```

### K07 — 3.14.4 表 3-14（V1 列） (v1.8.1 L1336 → v1.8.2 L1336)

Source: OUT 24 (D-1..D-15) D-3, D-5..D-8; OUT 29 §0–§6

OLD:

```text
| V1 Construct Validity | G→M 雙人盲編；錨點內容效度 | 預先登記判準（第 3.9.3 節）：Krippendorff's α（名目；Krippendorff, 2004）與 Cohen's κ（J. Cohen, 1960）、5,000 次 bootstrap 區間；α ≥ .800 為 RELIABLE、.667 ≤ α < .800 為 TENTATIVE（預先登記的研究慣例門檻，依 Krippendorff, 2004）；至少兩位人類編碼者；
```

NEW:

```text
| V1 Construct Validity | G→M 三位獨立人類盲編（遮蔽 G 編號）；錨點內容效度 | S1 凍結的判準（第 3.9.3 節）：Q2 的 Krippendorff's α（名目；Krippendorff, 2004；三位編碼者、16 項）為主要信度，兩兩 Cohen's κ（J. Cohen, 1960）為次要，5,000 次 bootstrap 95% 區間；α ≥ .800 為 RELIABLE、.667 ≤ α < .800 為 TENTATIVE、α < .667 為 UNRESOLVED/NOT_ACCEPTABLE（預先登記的研究慣例，非普遍標準）；三位獨立人類編碼者、不使用 AI 編碼者；
```

### K08 — 3.14.4 表 3-14（V1 列） (v1.8.1 L1336 → v1.8.2 L1336)

Source: OUT 25 Status; OUT 27

OLD:

```text
AI PILOT COMPLETE；HUMAN BLIND CODING PENDING（`V1_AI_PILOT_COMPLETE`；`V1_HUMAN_BLIND_CODING_PENDING`） |
```

NEW:

```text
AI PILOT COMPLETE；HUMAN BLIND CODING PENDING（`V1_AI_PILOT_COMPLETE`；`V1_HUMAN_BLIND_CODING_PENDING`；協定與封包已於 S1 凍結，人類編碼尚未執行） |
```

### K09 — 3.14.4 表 3-14 表註 (v1.8.1 L1344 → v1.8.2 L1344)

Source: OUT 25 Status

OLD:

```text
V0 與 V2 為 OPEN；V1 目前只有 AI 盲編 pilot。
```

NEW:

```text
V0 與 V2 為 OPEN；V1 目前只有 AI 盲編 pilot，人類盲編的協定與封包已於 S1 凍結、尚未執行。
```

### K10 — 4.7 狀態 (v1.8.1 L1693 → v1.8.2 L1693)

Source: OUT 25 Status; OUT 27 HUMAN_VALIDATION_EXECUTED=NO

OLD:

```text
第 4.7.3–4.7.4 節的人類結果全部為 `[HUMAN RESULT PENDING]`。
```

NEW:

```text
第 4.7.3–4.7.4 節的人類結果全部為 `[HUMAN RESULT PENDING]`。V1 人類盲編（v1.8.2 設計：三位獨立人類編碼者）的協定已於 S1 凍結（人類編碼前），封包已備妥待發送，人類編碼尚未執行，結果待完成。
```

### K11 — 4.7 回填規則 (v1.8.1 L1699 → v1.8.2 L1699)

Source: OUT 25 §10; OUT 30 §5; tools/no_human_data_run_v1_8_2/ (output filename)

OLD:

```text
   - V1 分析器 `60_v1_human_validation_analyzer_v2_3.py` → `v1_human_results/`
```

NEW:

```text
   - V1 分析器 `v1_construct_analyzer_v182.py`（v1.8.2，取代 `60_v1_human_validation_analyzer_v2_3.py`）→ `V1_RESULTS_v1_8_2.json`（存於受控的本機儲存，尚未產生）
```

### K12 — 4.7.3 表 4-13 (v1.8.1 L1738 → v1.8.2 L1738)

Source: OUT 29 §0–§6 §1–§4; OUT 30 §4–§5; OUT 28 §3

OLD:

```text
| 欄位 | 編碼者配對 | 一致數（/16） | Cohen's κ [95% CI] | Krippendorff's α [95% CI] | 協定分類（C1–C3） |
|---|---|---|---|---|---|
| 主機制 | A vs B | `[HUMAN RESULT PENDING]` | `[HUMAN RESULT PENDING]` | `[HUMAN RESULT PENDING]` | `[HUMAN RESULT PENDING]` |
| 狀態 | A vs B | `[HUMAN RESULT PENDING]` | `[HUMAN RESULT PENDING]` | `[HUMAN RESULT PENDING]` | `[HUMAN RESULT PENDING]` |
| 次機制 Jaccard（平均） | — | `[HUMAN RESULT PENDING]` | | | |

- 來源資料：`v1_human_import/coders.csv`，以及凍結於 manifest stage 3 的人類 response sheets。
- 計算程式：`python 60_v1_human_validation_analyzer_v2_3.py --coders v1_human_import/coders.csv`。
- 輸出變數：`reliability.fields.{primary_code,status}.{alpha, alpha_ci95, c1_c3_class, pairs[].{agreements, kappa, kappa_ci95}}`、`secondary_jaccard_mean`。
- 判讀規則（第 3.9.3 節；協定 C1–C3）：決策依 α——α ≥ .800 為 RELIABLE，.667 ≤ α < .800 為 TENTATIVE；α < .667 為 NOT_ACCEPTABLE；α 的 CI 下界 < .667 為 IMPRECISE，須加編碼者。κ 與其區間並列報告；不另報告文字強度標籤。
- 待決條件：至少兩位人類編碼者的已凍結 sheets。
```

NEW:

```text
| 欄位 | 編碼者 | 一致數（/16） | Cohen's κ [95% CI] | Krippendorff's α [95% CI] | 分類（研究慣例） |
|---|---|---|---|---|---|
| Q2 類別（主要；A. CURRENT_INSTRUMENT_RELIABILITY） | 三位編碼者 | `[HUMAN RESULT PENDING]` | — | `[HUMAN RESULT PENDING]` | `[HUMAN RESULT PENDING]` |
| Q2 類別（次要） | 兩兩配對（1–2、1–3、2–3） | `[HUMAN RESULT PENDING]` | `[HUMAN RESULT PENDING]` | — | — |
| Q1 企業決策介面 | 三位編碼者與兩兩配對 | `[HUMAN RESULT PENDING]` | `[HUMAN RESULT PENDING]` | `[HUMAN RESULT PENDING]` | 不作通過判定 |
| {Q2 ∪ Q4} Jaccard（平均） | — | `[HUMAN RESULT PENDING]` | | | |
| 53B 延續性（B. 53B_CONTINUITY_RELIABILITY；次要，另節報告） | 三位編碼者 | `[HUMAN RESULT PENDING]` | | `[HUMAN RESULT PENDING]` | `[HUMAN RESULT PENDING]` |

- 來源資料：三份回收的人類編碼表（每位編碼者一份），其雜湊須先寫入 `FREEZE_MANIFEST_V1_8_2_S2.txt`（階段 S2）；回收的編碼表只存於受控的本機儲存，不推送至公開儲存庫。
- 計算程式：`python v1_construct_analyzer_v182.py <三份編碼表> --s2-manifest <S2 manifest> --out <本機目錄>`（階段 R；只用中性項目編號，研究者答案鍵與項目對照表保持密封）。
- 輸出變數：`V1_RESULTS_v1_8_2.json` 中的 `reliability`（主要範圍為未曝露的編碼者；若有 EXPOSED 編碼者，含與不含曝露者兩種範圍分開並列）、`classification`；Q3 只作描述，不作權重。
- 判讀規則（第 3.9.3 節）：判讀以 Q2 的 α 為準——α ≥ .800 為 RELIABLE，.667 ≤ α < .800 為 TENTATIVE；α < .667 為 UNRESOLVED/NOT_ACCEPTABLE；α 的 CI 下界 < .667 時另標 IMPRECISE。門檻為研究慣例，不是普遍標準；κ 與其區間並列報告；不另報告文字強度標籤。
- 待決條件：三位人類編碼者的編碼表已回收並凍結於 S2。目前狀態：協定已於 S1 凍結（人類編碼前），封包已備妥待發送，人類編碼尚未執行，結果待完成。
```

### K13 — 4.7.3 表 4-14 (v1.8.1 L1752 → v1.8.2 L1754)

Source: OUT 29 §0–§6 §2 (per item, confusion matrices), §5

OLD:

```text
| 個案 | 編碼者 A | 編碼者 B | 分歧類型 | 最終碼 | 裁決路徑 |
|---|---|---|---|---|---|
| `[HUMAN RESULT PENDING]` | | | | | |

- 來源資料：同上，另加 `v1_human_import/adjudication.csv`（凍結於 manifest stage 4）。
- 計算程式：`60 … --adjudication …`。
- 輸出變數：`reliability.disagreements`、`reliability.fields.*.pairs[].disagreement_matrix`、`final_codes`。
```

NEW:

```text
| 項目（中性編號） | 編碼者 1 | 編碼者 2 | 編碼者 3 | 分歧類型 | 最終碼 | 裁決路徑 |
|---|---|---|---|---|---|---|
| `[HUMAN RESULT PENDING]` | | | | | | |

- 來源資料：同上，另加以中性項目編號為鍵的裁決檔（CSV），其雜湊寫入 `FREEZE_MANIFEST_V1_8_2_S3.txt`（階段 S3）。
- 計算程式：`v1_construct_analyzer_v182.py … --adjudication … --s3-manifest …`（階段 A／S3）。
- 輸出變數：逐項的 AGREED／TO_ADJUDICATION 狀態、各編碼者配對的 Q2 與 Q1 混淆矩陣、裁決後的最終碼。
```

### K14 — 4.7.3 表 4-15 說明 (v1.8.1 L1772 → v1.8.2 L1774)

Source: OUT 29 §0–§6 §6; OUT 25 §7

OLD:

```text
- 計算程式：`60 … --adjudication … --key <sealed_key.json>`；改變的個案另以凍結的 `classes.csv` 提供 mapping-sensitivity 分類（`--classes`）。
```

NEW:

```text
- 計算程式：`v1_construct_analyzer_v182.py … --adjudication … --s3-manifest … --item-map … --unseal --key <sealed_key.json>`（階段 K，只在 S3 之後；項目對照表的雜湊須等於承諾值）；改變的個案另以凍結的 classes 檔提供 mapping-sensitivity 分類（`--classes`，階段 C）。
```

### K15 — 4.7.3 表 4-15 說明 (v1.8.1 L1775 → v1.8.2 L1777)

Source: OUT 24 (D-1..D-15) D-1; OUT 29 §0–§6 §2.B, §6.3

OLD:

```text
  - V1 判定依協定 C6：至少兩位人類編碼者、C1 ≥ TENTATIVE 且非 IMPRECISE、C3 ≥ TENTATIVE、沒有未解的 model-structural 變更，才得到 `V1_PASS_HUMAN_C6`。
```

NEW:

```text
  - `V1_PASS_HUMAN_C6` 只在 B. 53B_CONTINUITY_RELIABILITY 中報告，屬次要的延續性標籤：至少兩位未曝露的人類編碼者、C1 ≥ TENTATIVE 且非 IMPRECISE、C3 ≥ TENTATIVE、沒有未解的 model-structural 變更，才得到此標籤；主要的構念效度判讀依表 4-13 的 Q2 α。"V1_PASS_HUMAN_C6 is a continuity label under the earlier 53B protocol, not evidence that the amended Q1–Q5 instrument is identical to 53B."
```

### K16 — 4.7.3 表 4-15 說明 (v1.8.1 L1778 → v1.8.2 L1780)

Source: OUT 25 Status; OUT 27

OLD:

```text
- 待決條件：裁決已凍結。**目前狀態：`V1_HUMAN_BLIND_CODING_PENDING`。**
```

NEW:

```text
- 待決條件：裁決已凍結（S3）。**目前狀態：`V1_HUMAN_BLIND_CODING_PENDING`（協定已於 S1 凍結（人類編碼前），封包已備妥待發送，人類編碼尚未執行，結果待完成）。**
```

### K17 — 附錄 D（v1.8.1／16 列） (v1.8.1 L3022 → v1.8.2 L3024)

Source: this round

OLD:

```text
| 合併論文 v1.8.1（清理版） | 本稿 |
```

NEW:

```text
| 合併論文 v1.8.1（清理版） | v1.8.2 的修訂底稿（已保存；未覆寫） |
```

### K18 — 附錄 D（v1.8.1／19–21 列 + v1.8.2 列） (v1.8.1 L3024 → v1.8.2 L3026)

Source: OUT file list (24–30, coder_distribution, tools); this round

OLD:

```text
| V1 人類構念效度驗證協定、封包與編碼手冊（READY_TO_RUN；尚未執行） | 稿件狀態；第 4.7.3 節 |
```

NEW:

```text
| V1 人類構念效度驗證協定、封包與編碼手冊（v1.8.1 版；已由 v1.8.2 檔案 24–30 取代；其封包顯示 G 編號，不得發送） | 稿件狀態；第 4.7.3 節 |
| v1.8.2／24 | — | `24_RESEARCHER_DECISION_RECORD.md` | V1 研究者決策紀錄（三位人類編碼者、遮蔽 G 編號、OA-2／OA-3 的決定） | 稿件狀態；第 3.9.3 節 |
| v1.8.2／25–26 | — | `25_V1_FINAL_PROTOCOL_v1_8_2.md`、`26_V1_FINAL_CODEBOOK_v1_8_2.md` | V1 最終協定與編碼手冊（S1 凍結；人類編碼前） | 第 3.9.3、4.7.3 節 |
| v1.8.2／27 | — | `27_V1_PREFREEZE_AUDIT.md` | V1 凍結前稽核（由程式計算；人類編碼尚未執行） | 第 3.9.3 節 |
| v1.8.2／28 | — | `28_V1_BLINDING_AND_RECRUITMENT_PLAN.md` | 盲性與招募計畫（含公開儲存庫的限制） | 第 3.9.3 節 |
| v1.8.2／29 | — | `29_V1_ANALYSIS_PLAN_FROZEN.md`、`tools/v1_construct_analyzer_v182.py` | 凍結的 V1 分析計畫與分析程式（Q2 α 為主要信度） | 第 3.9.3、4.7.3 節 |
| v1.8.2／30 | — | `30_V1_DISTRIBUTION_README.md`、`coder_distribution/`、`20_MASTER_PACKET_v1_8_2.xlsx` | 封包發送說明與三份編碼者封包（已備妥待發送；研究團隊主檔不給編碼者） | 第 4.7.3 節 |
| v1.8.2／32 | — | `32_MERGED_MASTER_THESIS_v1_8_2_V1_PREFREEZE_CANDIDATE.md` | 合併論文 v1.8.2（V1 凍結前版；只更新 V1 設計與狀態描述） | 本稿 |
```

### K19 — 附錄 E6 (v1.8.1 L3035 → v1.8.2 L3044)

Source: OUT 24 (D-1..D-15) D-3, D-8, D-10, D-15; OUT 30 §1

OLD:

```text
| E6 | V1 人類雙人盲編與 EA-X 人類內容效度（AI pilot 已完成） | 表 3-4 的對應仍只是研究者裁決；G04、G10、G11 具爭議 | 依預先登記協定執行；至少兩位人類編碼者；編碼者只收到盲編封包 |
```

NEW:

```text
| E6 | V1 人類盲編（三位獨立人類編碼者；v1.8.2 協定已於 S1 凍結，人類編碼尚未執行）與 EA-X 人類內容效度（AI pilot 已完成） | 表 3-4 的對應仍只是研究者裁決；G04、G10、G11 具爭議 | 依 v1.8.2 凍結協定（V1.8.2 檔案 25、26、29）執行：三位獨立人類編碼者、不使用 AI 編碼者；編碼者只收到遮蔽 G 編號的盲編封包並填寫七項聲明；封包直接寄送，不經公開儲存庫 |
```

## Verification summary (from verify_out.json)

- `line_count`: `[3086, 3095]`
- `math_identical_ordered`: `{"$$": true, "$inline": true, "\\[\\]": true, "begin_env": true}`
- `fenced_blocks_identical`: `true`
- `equation_tags_identical`: `true`
- `changed_lines_with_math_markers`: `[]`
- `headings`: `{"v181": 182, "v182": 182, "identical": true}`
- `table_figure_captions_identical`: `true`
- `G_table_rows`: `{"v181": 36, "v182": 36, "identical_ordered": true}`
- `section_3_9_2_tables_3_4_and_3_4A_identical`: `true`
- `section_4_7_1_table_4_11_identical`: `true`
- `section_4_7_2_table_4_12_identical`: `true`
- `section_4_7_4_EAX_identical`: `true`
- `section_3_9_5_identical`: `true`
- `EAX_paragraph_3_9_3_unchanged`: `true`
- `G_token_counts`: `[288, 291]`
- `G_tokens_per_patch`: `{"K04": [3, 3], "K06": [0, 3], "K19": [3, 3]}`
- `GM_arrow_tokens_identical`: `true`
- `count_VCP`: `[28, 28]`
- `count_VSC`: `[26, 26]`
- `count_DL`: `[59, 59]`
- `count_NEV`: `[28, 28]`
- `count_Enterprise`: `[10, 10]`
- `count_Study 1`: `[2, 2]`
- `count_M5`: `[43, 41]`
- `count_HUMAN_RESULT_PENDING`: `[41, 44]`
- `result_like_tokens_added`: `{}`
- `oa2_sentence_count_v182`: `2`
- `leak_item_ids_v182`: `0`
- `leak_seed_like_v182`: `false`
- `numeric_patch_sum_matches_doc`: `true`
- `numeric_added_not_in_allowlist`: `{}`

Notes: `G_token_counts` rises by 3 only because K06 adds the sentence naming G04、G10、G11 as predeclared sensitivity targets (allowed edit 3); no G row or G→M assignment changed. `count_M5` falls by 2 because the old §3.9.3 instrument text "M1–M5" (twice) was replaced by the v1.8.2 flat Q2 categories (M1–M4, LONGITUDINAL, …); M5 elsewhere is unchanged. `count_HUMAN_RESULT_PENDING` rises by 3 because Table 4-13/4-14 placeholders were restructured to the 3-coder design (all cells pending).
