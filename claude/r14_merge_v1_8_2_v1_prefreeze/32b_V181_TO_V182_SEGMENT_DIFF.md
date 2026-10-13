# 32b — v1.8.1 → v1.8.2 segment diff

Input sha256 `cddeb89b07439ff2bba9af1ba119824cb1cf815c4fc8a78e084900cd24e06bda`; output sha256 `2d493edc2e1884f05e5b0617bc56f1f85cdab0fa33531ac566b61d343dd8f159`. Changed lines v1.8.1: [5, 15, 749, 757, 1336, 1344, 1693, 1699, 1738, 1740, 1741, 1742, 1744, 1745, 1746, 1747, 1748, 1752, 1753, 1754, 1756, 1757, 1758, 1772, 1775, 1778, 3022, 3024, 3035]; v1.8.2: [5, 15, 749, 757, 1336, 1344, 1693, 1699, 1738, 1740, 1741, 1742, 1743, 1744, 1746, 1747, 1748, 1749, 1750, 1754, 1755, 1756, 1758, 1759, 1760, 1774, 1777, 1780, 3024, 3026, 3027, 3028, 3029, 3030, 3031, 3032, 3033, 3044].

## Invariants (script-verified)

- Math spans byte-identical (ordered, $$ / inline $ / \[\] / begin-env): {'$$': True, '$inline': True, '\\[\\]': True, 'begin_env': True}; equation \tag set identical: True; changed lines with math markers: [].
- Heading list identical: {'v181': 182, 'v182': 182, 'identical': True}.
- G-table rows (`| G01`…`| G16`) identical in order: {'v181': 36, 'v182': 36, 'identical_ordered': True}.
- §3.9.2 (Tables 3-4 and 3-4A) byte-identical: True; Table 4-11 section identical: True; G→M arrow tokens identical: True.
- §3.9.5, §4.7.2 (AI pilot table), §4.7.4 (EA-X) and the §3.9.3 EA-X paragraph unchanged: True, True, True, True.
- VCP/VSC/DL/NEV/Enterprise/Study 1 counts unchanged: VCP [28, 28], VSC [26, 26], DL [59, 59], NEV [28, 28], Enterprise [10, 10], Study 1 [2, 2].
- No human result inserted: result-like tokens added = {}; all new V1 result cells are `[HUMAN RESULT PENDING]`.
- Public-repo sealing: ITEM-ID tokens in manuscript = 0; no item↔G pairing, order list or seed.
- OA-2 verbatim sentence occurrences: 2 (§3.9.3 item 6; §4.7.3 Table 4-15 rule).

## Numeric tokens added / removed (whole document)

- Added: `{"1": 3, "13": 1, "16": 3, "19": 1, "2": 4, "20": 1, "21": 1, "24": 5, "25": 4, "256": 1, "26": 3, "27": 2, "28": 2, "29": 4, "3": 3, "3.9.3": 5, "3.9.4": 1, "30": 4, "32": 3, "4-13": 1, "4.7.3": 3, "53": 10, "6": 1, "7": 1, "8": 1, "95": 1}`
- Removed: `{".800": 1, "2004": 2, "4": 1, "60": 3}`
- Sum of per-patch deltas equals document delta: True. Tokens outside the design-parameter allowlist: {}.

| Patch | Added | Removed | Justification |
|---|---|---|---|
| K02 | `{"19": 1, "21": 1, "24": 1, "25": 1, "30": 1}` | `{}` | "19", "21" = v1.8.1 file IDs 19–21; "24", "25", "30" = v1.8.2 file IDs 24 and 25–30 (design parameters / artifact IDs). |
| K05 | `{"256": 1, "24": 1, "29": 1, "32": 1, "6": 1, "53": 5, "7": 1, "3.9.4": 1, "8": 1}` | `{"2004": 1, ".800": 1, ".667": 1}` | "24", "29" = file IDs 24–29; "256" = SHA-256; "32" = 32-cell scope statement (D-14); "53" (x5) = protocol name 53B (OA-2 wording, continuity metric names); "6", "7", "8" = new enumerated design items (6)–(8); "3.9.4" = cross-reference. Removed: one ".800" and one ".667" (old "(.800／.667 兩個門檻依 Krippendorff, 2004 ...)" provenance clause, replaced by research-convention statement; thresholds still stated once each), one "2004" (same clause; Krippendorff 2004 citation retained for α). Retained from old: 16, 5,000, 95, .800, .667, 1960, 2004. |
| K06 | `{"16": 2, "13": 1}` | `{}` | "16" (x2), "13" = 16-item vs 13-item sensitivity design (29 §6.1). |
| K07 | `{"16": 1, "95": 1, ".667": 1}` | `{"2004": 1}` | "16" = 16 items; "95" = 95% bootstrap CI; ".667" = α < .667 UNRESOLVED/NOT_ACCEPTABLE threshold (D-7). Removed "2004" = threshold attribution "依 Krippendorff, 2004" replaced by research-convention label (29 §3); α citation Krippendorff 2004 retained. |
| K12 | `{"1": 2, "2": 2, "3": 1, "53": 2}` | `{"60": 1}` | "1", "2", "3" = coder labels in pairwise pairs 1–2, 1–3, 2–3; "53" (x2) = 53B continuity section name. Removed "60" = superseded analyzer filename prefix. |
| K13 | `{"1": 1, "2": 1, "3": 1}` | `{"4": 1, "60": 1}` | "1", "2", "3" = coder column labels. Removed "4" = old "manifest stage 4"; "60" = superseded analyzer. |
| K14 | `{}` | `{"60": 1}` | Removed "60" = superseded analyzer filename prefix. |
| K15 | `{"53": 3, "4-13": 1}` | `{}` | "53" (x3) = 53B (section name + OA-2 verbatim sentence); "4-13" = cross-reference to Table 4-13. |
| K18 | `{"24": 3, "30": 3, "4.7.3": 3, "2": 1, "3": 1, "3.9.3": 5, "25": 2, "26": 2, "27": 2, "28": 2, "29": 2, "20": 1, "32": 2}` | `{}` | file IDs 24–30, 32, 20 (20_MASTER_PACKET_v1_8_2.xlsx); "2", "3" = decision labels OA-2／OA-3; section refs 3.9.3, 4.7.3. |
| K19 | `{"25": 1, "26": 1, "29": 1}` | `{}` | "25", "26", "29" = v1.8.2 file IDs. |

All added numbers are design parameters (3 coders, 16 items, 13-item sensitivity, .800/.667, 95%, 5,000), file/artifact IDs (19–32), protocol names (53B), SHA-256, coder labels 1–3, or cross-references. No empirical, synthetic or network value was added or removed.

## Remaining "兩位編碼者" / two-coder mentions (all intentional; none is a V1 design statement)

| Pattern | v1.8.2 line | Context | Why kept |
|---|---|---|---|
| 兩位編碼者 | 591 | NAL_ERROR_TAXONOMY.csv，已核對〕；因此本研究不把分歧單獨歸因於語言模型不準確。這項整理針對模型與人工標籤的差異，不是對兩位編碼者 19 筆分歧的分類；19 筆分歧尚未逐筆依這四類來源歸類。V9 套件的完整性紀錄另顯示，早期稽核日誌 HUMAN_AUDIT_A | Study 1 literature human audit (V9), not V1 |
| 兩位編碼者 | 946 | 果不得用來支持參考答案。順序固定為「證據 → D 編碼 → 裁決 → 映射」：裁決者在完成裁決前不看 archetype 或正式模型的結果，兩位編碼者的原值保留，不一致依九類理由記錄（定義模糊、值重疊、缺證據、證據衝突、編碼者錯誤、編碼手冊缺口、附屬碼規則錯誤、映射規則模糊、其他 | ORG-V study (organization coding), not V1 |
| 兩位編碼者 | 948 | **ORG-V4 與 ORG-V5。** 以兩位編碼者各自與裁決後的編碼，分別執行既有的 archetype 判定與正式模型映射規則（`org_schema.py`，不修改）。ORG- | ORG-V study, not V1 |
| 兩位編碼者 | 1559 | 均由研究者逐筆調和；首輪部分困難邊界案例曾使用外部 AI 討論編碼規則，因此這組一致度屬目標式診斷，不是完全 AI 盲的外部驗證。也就是說，兩位編碼者較常能同意『這段是否真正支持一個人工智慧 × 決策功能關係』，但把同一段文字壓成單一關係類型與單一家族時，一致度明顯下降。這個型態 | Study 1 audit agreement |
| 兩位編碼者 | 2264 | 人工稽核補上了另一個測量面向：證據是否有效與『應被壓成哪一個單一功能家族』並不是同一問題。兩位編碼者在調和前對證據有效性的一致度（κ = .561）明顯高於對關係類型（.180）、人工智慧家族（.048）與決策家族（.140）的一 | Study 1 audit discussion |
| 兩位編碼者 | 2326 | 訂為 50 筆研究者目標稽核與 20 筆盲式第二編碼，且 50 筆集中於穩健核心相關分層，因此只能作為目標式診斷，不能推廣成全語料效能估計。兩位編碼者在 20 筆上的人工智慧家族與決策家族一致率均為 20%（κ = .048 與 .140），19 筆分歧經研究者人工調和；首輪部分 | Study 1 audit limitation |
| 至少兩位 | 1777 |   - `V1_PASS_HUMAN_C6` 只在 B. 53B_CONTINUITY_RELIABILITY 中報告，屬次要的延續性標籤：至少兩位未曝露的人類編碼者、C1 ≥ TENTATIVE 且非 IMPRECISE、C3 ≥ TENTATIVE、沒有未解的 model-s | C6 continuity-label rule (≥ 2 clean coders, plan 29 §6.3), not a coder-count design statement |
| 編碼者 A | 2995 | _CODER_A_TEMPLATE_v1_0.xlsx`、`113_ORG_V_CODER_B_TEMPLATE_v1_0.xlsx` \| 編碼者 A／B 的空白編碼表 \| 第 3.10.7 節 \| | ORG-V coder A/B templates (Appendix D), not V1 |

## Segment diff (changed lines only)

### v1.8.1 L5–5 → v1.8.2 L5–5 (replace)

- OLD: `∅`
  NEW: `2 V`
- OLD: `CL`
  NEW: `PR`
- OLD: `ANUP`
  NEW: `FREEZE`
- OLD: `∅`
  NEW: `.1`
- OLD: `∅`
  NEW: `.1`
- OLD: `；`
  NEW: `）。v1.8.2 只更新 V1 人類構念效度驗證的設計與`
- OLD: `∅`
  NEW: `描述：依研究者決策紀錄（V1.8.2`
- OLD: `RE`
  NEW: `檔案 24），V1 改為三位獨立人類編碼者、不使用 `
- OLD: `DY_TO_RUN：`
  NEW: `I 編碼者、編碼者材料遮蔽 G 編號的設計；協定、編碼手冊、分析計畫與封包已於 S1 凍結（人類編碼前；V1.8.2 檔案 25–30），封包`
- OLD: `、`
  NEW: `待發送；人類編碼`
- OLD: `）`
  NEW: `；V1.8.1 的 19–21 封包顯示 G 編號，已被取代、不得發送`
- OLD: `∅`
  NEW: `（協定已於 S1 凍結、人類編碼尚未執行）`

### v1.8.1 L15–15 → v1.8.2 L15–15 (replace)

- OLD: `∅`
  NEW: `；三位獨立人類編碼者的盲編協定已凍結`
- OLD: `雙人盲`
  NEW: `∅`
- OLD: `∅`
  NEW: `碼`
- OLD: `待完成`
  NEW: `未執行`

### v1.8.1 L749–749 → v1.8.2 L749–749 (replace)

- OLD: `∅`
  NEW: `、編碼手冊、分析計畫與分析程式`
- OLD: `∅`
  NEW: `人類`
- OLD: `輸出`
  NEW: `∅`
- OLD: `∅`
  NEW: `（階段 S1），`
- OLD: `∅`
  NEW: `以 SHA-256 `
- OLD: `，內容`
  NEW: `；v1.8.2 的設計`
- OLD: `∅`
  NEW: `（V1.8.2 檔案 24–29）`
- OLD: `∅`
  NEW: `範圍與研究問題。** V1 只檢驗「缺口 → 企業機制」的轉譯解讀，不檢驗 32 格的成員資格、分類體系的正確性或文獻網路的統計量。主要問題是`
- OLD: `∅`
  NEW: `者間信度，即三位獨立的人類編碼者是否把同一配對歸入同一企業決策類別；與研究者答案鍵的一致是另一個問題，只在答案鍵開啟之後才比較。(2) **編碼者與`
- OLD: `∅`
  NEW: `為三位獨立的人類，不使用 AI 編碼者。每個項目`
- OLD: `收到協定、一份盲`
  NEW: `以中性的項目`
- OLD: `∅`
  NEW: `號呈現，缺口編號（G 編號）不出現在任何編碼者材料中；項目編號由以秘密種子產生的隨機排列指派，項目編號與 G 編號的對照表由研究團隊密`
- OLD: `包（16 個個案`
  NEW: `保管`
- OLD: `∅`
  NEW: `位編碼者的項目順序也各自以種子隨機排列。每`
- OLD: `個案`
  NEW: `項目`
- OLD: `∅`
  NEW: `、一句標準的不足呈現陳述與中性的證據描述`
- OLD: `兩份封包的列序不同）與空白回答表。`
  NEW: `∅`
- OLD: `缺口編號、`
  NEW: `∅`
- OLD: `∅`
  NEW: `、AI pilot 的編碼`
- OLD: `p`
  NEW: `q`
- OLD: `；人類`
  NEW: `。(3) **盲性聲明。** 每位`
- OLD: `須簽署未閱讀相關文件的`
  NEW: `填寫七項`
- OLD: `∅`
  NEW: `：未讀過公開的研究儲存庫、未讀過論文或稿件、未看過研究者的 G→M 對應、未看過 AI pilot 的輸出、未與其他編碼者商量、未使用任何 AI 工具作答，以及獨立完成編碼。任一項曝露即標為 EXPOSED；曝露的編碼者不會被默默併入分析：主要範圍只含未曝露的編碼者，含與不含曝露者的結果分開並列報告`
- OLD: `2`
  NEW: `4`
- OLD: `內容`
  NEW: `工具（Q1–Q5）`
- OLD: `每個個案編`
  NEW: `Q1 判斷該配對是否對應可辨識的企業決策介面（YES、NO、UNCERTAIN）；Q2 從一組平面類別中選`
- OLD: `主碼（`
  NEW: `：`
- OLD: `–`
  NEW: `、`
- OLD: `5`
  NEW: `2`
- OLD: `∅`
  NEW: `M3、M4、LONGITUDINAL（跨期）、DATA_GATED（`
- OLD: `型`
  NEW: `）`
- OLD: `∅`
  NEW: `EVIDENCE_ONLY（`
- OLD: `、其他機制或資訊不足`
  NEW: `∅`
- OLD: `至多一個次碼、狀態（static、dynamic、optional、evidence-only、insufficient）與`
  NEW: `NONE 或 AMBIGUOUS；Q3 為對 Q2 的`
- OLD: `值`
  NEW: `（HIGH、MEDIUM、LOW）`
- OLD: `編碼者不必把每個個案放進`
  NEW: `Q4 為選填的次要類別；Q5 為一至三句的理由。NONE 的定義是：存在可辨識的企業決策介面，但`
- OLD: `∅`
  NEW: `4、LONGITUDINAL 與 DATA_GATED 都不足以表達；它要求 Q1 = YES，且 Q`
- OLD: `∅`
  NEW: ` 須寫出未被涵蓋的企業決策。證據不足或兩類並列時不使用 NONE（改用 AMBIGUOUS 或 Q1 = UNCERTAIN），沒有獨立的介面時也不使用 NONE（改用 EVIDENCE_ONLY）`
- OLD: `3`
  NEW: `5`
- OLD: `碼與狀態分開計算：兩位編碼者時報告一致數與`
  NEW: `要指標是`
- OLD: `J.`
  NEW: `Q2`
- OLD: `Cohen（1960）`
  NEW: `∅`
- OLD: ` κ，並同時報告`
  NEW: `∅`
- OLD: ` 的`
  NEW: `∅`
- OLD: `∅`
  NEW: `全部`
- OLD: `∅`
  NEW: `16 個項目、三位編碼者計算，並報告以項目為單位、`
- OLD: `個案`
  NEW: `∅`
- OLD: `求`
  NEW: `的`
- OLD: `；判定以`
  NEW: `、原始一致率與各類別次數。次要指標是兩兩編碼者配對的 J. Cohen（1960）κ，各附自助法區間。Q1 報告`
- OLD: `∅`
  NEW: `與兩兩 κ，不作通過或不通過的判定；Q3 只作描述，永不作為權重；Q4 只以 {Q2 ∪ Q4} 的集合 Jaccard 一致度描述。判讀以 Q2 的 α 點估計`
- OLD: `∅`
  NEW: `UNRESOLVED/`
- OLD: `，須增加編碼者（.800／.667 兩個`
  NEW: `。這些`
- OLD: `依 Krippendorff, 2004，為`
  NEW: `是本研究`
- OLD: `；NOT_ACC`
  NEW: `，不是普遍適用的標準（出處的核對見附錄 `
- OLD: `PTABLE 與 IMPRECISE 兩類為本研究的操作化`
  NEW: `4`
- OLD: `次碼只以 {主碼 ∪ 次碼} 的 Jaccard 一致度描述，信心值不作加權。`
  NEW: `∅`
- OLD: `4`
  NEW: `6`
- OLD: `∅`
  NEW: `與 53B 協定的延續性。** 由 Q2 推導的 53B 主碼與狀態，以及 `V1_PASS_HUMAN_C6` 標籤，只作為次要的延續性指標，與主要結果分節報告（CURRENT_INSTRUMENT_RELIABILITY 與 53B_CONTINUITY_RELIABILITY），兩者不合併；如協定所載："V1_PASS_HUMAN_C6 is a continuity label under the earlier 53B protocol, not evidence that the amended Q1–Q5 instrument is identical to 53B."(7) **階段與`
- OLD: `∅`
  NEW: `執行依序為 S1（封包凍結）→ S2（三份回收編碼表凍結）→ R（信度計算，只用中性項目編號，答案鍵與項目對照表保持密封）→ A（裁決）→ S3（裁決結果凍結）→ K（開啟研究者答案鍵）→ C（mapping-sensitivity 分類）。`
- OLD: `只`
  NEW: `∅`
- OLD: `裁決結果凍結`
  NEW: ` S3 之`
- OLD: `∅`
  NEW: `，其雜湊須等於預先承諾值`
- OLD: `(5) **通過條件。** 只有在至少兩位人類編碼者、主碼信度至少 TENTATIVE 且非 IMPRECISE、狀態信度至少 TENTATIVE，且沒有未解的模型結構性變更時，才判定 V1 通過（`V1_PASS_HUMAN_C6`）。`
  NEW: `∅`
- OLD: `即使達到相同門檻，也只能得到「`
  NEW: `不參與 V1；先前的 `
- OLD: `∅`
  NEW: `（第`
- OLD: `可接受」`
  NEW: `3.9.4 節）只是診斷`
- OLD: `∅`
  NEW: `即使達到相同門檻也`
- OLD: `∅`
  NEW: `(8) **盲性的限制。** 研究儲存庫在編碼開始之前即已公開，研究者的對應可在其中讀到，讀過儲存庫的人可能由功能家族配對辨認出項目；因此本研究不主張完美的盲性。緩解方式是只招募未曾接觸儲存庫、論文稿件與 AI pilot 輸出的編碼者，並以七項聲明記錄；自我聲明無法查證，列為研究限制。目前狀態：協定已於 S1 凍結（人類編碼前），封包已備妥待發送，人類編碼尚未執行，結果待完成。`

### v1.8.1 L757–757 → v1.8.2 L757–757 (replace)

- OLD: `∅`
  NEW: `G04、G10、G11 已預先登記為 V1 的敏感度分析對象（S3 之後以 16 項對 13 項重算，16 項的結果仍為判定基準），但編碼者材料中不標示這三格。`

### v1.8.1 L1336–1336 → v1.8.2 L1336–1336 (replace)

- OLD: `雙`
  NEW: `三位獨立`
- OLD: `∅`
  NEW: `類`
- OLD: `∅`
  NEW: `（遮蔽 G 編號）`
- OLD: `預先登記`
  NEW: `S1 凍結的`
- OLD: `∅`
  NEW: `Q2 的 `
- OLD: `∅`
  NEW: `；三位編碼者、16 項`
- OLD: `與`
  NEW: `為主要信度，兩兩`
- OLD: `、`
  NEW: `為次要，`
- OLD: `∅`
  NEW: ` 95%`
- OLD: `∅`
  NEW: `、α < .667 為 UNRESOLVED/NOT_ACCEPTABLE`
- OLD: `門檻`
  NEW: `∅`
- OLD: `依 Krippendorff, 2004`
  NEW: `非普遍標準`
- OLD: `至少兩`
  NEW: `三`
- OLD: `∅`
  NEW: `獨立`
- OLD: `∅`
  NEW: `編碼者、不使用 AI `
- OLD: `∅`
  NEW: `；協定與封包已於 S1 凍結，人類編碼尚未執行`

### v1.8.1 L1344–1344 → v1.8.2 L1344–1344 (replace)

- OLD: `∅`
  NEW: `，人類盲編的協定與封包已於 S1 凍結、尚未執行`

### v1.8.1 L1693–1693 → v1.8.2 L1693–1693 (replace)

- OLD: `∅`
  NEW: `V1 人類盲編（v1.8.2 設計：三位獨立人類編碼者）的協定已於 S1 凍結（人類編碼前），封包已備妥待發送，人類編碼尚未執行，結果待完成。`

### v1.8.1 L1699–1699 → v1.8.2 L1699–1699 (replace)

- OLD: `∅`
  NEW: ` `v1_construct_analyzer_v182.py`（v1.8.2，取代`
- OLD: ` `
  NEW: `）`
- OLD: `∅`
  NEW: `V1_RESULTS_`
- OLD: `huma`
  NEW: `8_2.jso`
- OLD: `_results/`
  NEW: `∅`
- OLD: `∅`
  NEW: `（存於受控的本機儲存，尚未產生）`

### v1.8.1 L1738–1738 → v1.8.2 L1738–1738 (replace)

- OLD: `配對`
  NEW: `∅`
- OLD: `協定`
  NEW: `∅`
- OLD: `C1–C3`
  NEW: `研究慣例`

### v1.8.1 L1740–1742 → v1.8.2 L1740–1744 (replace)

- OLD: `∅`
  NEW: `Q2 類別（`
- OLD: `機制`
  NEW: `要；A. CURRENT_INSTRUMENT_RELIABILITY）`
- OLD: `∅`
  NEW: `三位編碼者 \| `[HUM`
- OLD: `∅`
  NEW: `N`
- OLD: `vs`
  NEW: `RESULT`
- OLD: `B`
  NEW: `PENDING]` \| —`
- OLD: ` `[HUMAN RESULT PENDING]` \| `[HUMAN RESULT PENDING]` \|`
  NEW: `∅`
- OLD: `狀態`
  NEW: `Q2 類別（次要）`
- OLD: `A vs B`
  NEW: `兩兩配對（1–2、1–3、2–3）`
- OLD: ``[HUMAN RESULT PENDING]``
  NEW: `—`
- OLD: ``[HUMAN RESULT PENDING]``
  NEW: `—`
- OLD: `次機制`
  NEW: `Q1`
- OLD: `Jaccard（平均）`
  NEW: `企業決策介面`
- OLD: `—`
  NEW: `三位編碼者與兩兩配對`
- OLD: `\|`
  NEW: ``[HUMAN RESULT PENDING]``
- OLD: `∅`
  NEW: ``[HUMAN RESULT PENDING]` `
- OLD: `∅`
  NEW: ` 不作通過判定 \|`
- OLD: `∅`
  NEW: `\| {Q2 ∪ Q4} Jaccard（平均） \| — \| `[HUMAN RESULT PENDING]` \| \| \| \|`
- OLD: `∅`
  NEW: `\| 53B 延續性（B. 53B_CONTINUITY_RELIABILITY；次要，另節報告） \| 三位編碼者 \| `[HUMAN RESULT PENDING]` \| \| `[HUMAN RESULT PENDING]` \| `[HUMAN RESULT PENDING]` \|`

### v1.8.1 L1744–1748 → v1.8.2 L1746–1750 (replace)

- OLD: ``v1_human_import/coders.csv`，以及凍結於 manifest stage 3 `
  NEW: `三份回收`
- OLD: `∅`
  NEW: `編碼表（每位編碼者一份），其雜湊須先寫入`
- OLD: `response`
  NEW: ``FREEZE_MANIFEST_V1_8_2_S2.txt`（階段`
- OLD: `sheets`
  NEW: `S2）；回收的編碼表只存於受控的本機儲存，不推送至公開儲存庫`
- OLD: `60_`
  NEW: `∅`
- OLD: `human_validati`
  NEW: `c`
- OLD: `∅`
  NEW: `struct`
- OLD: `∅`
  NEW: `18`
- OLD: `_3`
  NEW: `∅`
- OLD: `∅`
  NEW: `<三份編碼表> `
- OLD: `coder`
  NEW: `∅`
- OLD: ` v1_hu`
  NEW: `2-`
- OLD: `_`
  NEW: `∅`
- OLD: `∅`
  NEW: `fest <S2 `
- OLD: `p`
  NEW: `anifest> --`
- OLD: `r`
  NEW: `u`
- OLD: `/coders.csv`
  NEW: ` <本機目錄>`
- OLD: `∅`
  NEW: `（階段 R；只用中性項目編號，研究者答案鍵與項目對照表保持密封）`
- OLD: `∅`
  NEW: ``V1_RESULTS_v1_8_2.json` 中的 `
- OLD: `.fields.{primary_code,status}.{alpha,`
  NEW: ``（主要範圍為未曝露的編碼者；若有`
- OLD: `alpha_ci95,`
  NEW: `EXPOSED`
- OLD: `c1_c3_`
  NEW: `編碼者，含與不含曝露者兩種範圍分開並列）、``
- OLD: `, p`
  NEW: `ific`
- OLD: `∅`
  NEW: `t`
- OLD: `rs[].{agreements, kappa, kappa_ci95}}`、`sec`
  NEW: `∅`
- OLD: `dary_jaccard_mean`
  NEW: `∅`
- OLD: `∅`
  NEW: `；Q3 只作描述，不作權重`
- OLD: `；協定 C1–C3`
  NEW: `∅`
- OLD: `決策依`
  NEW: `判讀以 Q2 的`
- OLD: `∅`
  NEW: ` 為準`
- OLD: `∅`
  NEW: `UNRESOLVED/`
- OLD: `為`
  NEW: `時另標`
- OLD: `∅`
  NEW: `。門檻為研究慣例`
- OLD: `須加編碼者。`
  NEW: `不是普遍標準；`
- OLD: `至少兩`
  NEW: `三`
- OLD: `∅`
  NEW: `編碼表`
- OLD: `∅`
  NEW: `回收並`
- OLD: `∅`
  NEW: `於`
- OLD: `sheets`
  NEW: `S2`
- OLD: `∅`
  NEW: `目前狀態：協定已於 S1 凍結（人類編碼前），封包已備妥待發送，人類編碼尚未執行，結果待完成。`

### v1.8.1 L1752–1754 → v1.8.2 L1754–1756 (replace)

- OLD: `個案`
  NEW: `項目（中性編號）`
- OLD: `A`
  NEW: `1`
- OLD: `B`
  NEW: `2 \| 編碼者 3`
- OLD: `∅`
  NEW: `---\|`
- OLD: `∅`
  NEW: ` \|`

### v1.8.1 L1756–1758 → v1.8.2 L1758–1760 (replace)

- OLD: `∅`
  NEW: `以中性項目編號為鍵的裁決檔（CSV），其雜湊寫入`
- OLD: `v`
  NEW: `FREEZE_MANIFEST_V`
- OLD: `human`
  NEW: `8`
- OLD: `impor`
  NEW: `2_S3.`
- OLD: `/adjudica`
  NEW: `x`
- OLD: `ion.csv`
  NEW: `∅`
- OLD: `凍結於`
  NEW: `階段`
- OLD: `manifest stage 4`
  NEW: `S3`
- OLD: `60`
  NEW: `v1_construct_analyzer_v182.py`
- OLD: `∅`
  NEW: ` --s3-manifest …`
- OLD: `∅`
  NEW: `（階段 A／S3）`
- OLD: ``reliability.disagreements``
  NEW: `逐項的 AGREED／TO_ADJUDICATION 狀態`
- OLD: ``reliability.fields.*.pairs[].disagreement_matrix``
  NEW: `各編碼者配對的 Q2 與 Q1 混淆矩陣`
- OLD: ``final_codes``
  NEW: `裁決後的最終碼`

### v1.8.1 L1772–1772 → v1.8.2 L1774–1774 (replace)

- OLD: `60`
  NEW: `v1_construct_analyzer_v182.py`
- OLD: `∅`
  NEW: ` --s3-manifest … --item-map … --unseal`
- OLD: `∅`
  NEW: `（階段 K，只在 S3 之後；項目對照表的雜湊須等於承諾值）`
- OLD: ```
  NEW: `∅`
- OLD: `.csv``
  NEW: `∅`
- OLD: `∅`
  NEW: `檔`
- OLD: `∅`
  NEW: `，階段 C`

### v1.8.1 L1775–1775 → v1.8.2 L1777–1777 (replace)

- OLD: `∅`
  NEW: ```
- OLD: ` 判定依協定 `
  NEW: `_PASS_HUMAN_`
- OLD: `∅`
  NEW: `` 只在 B. 53B_CONTINUITY_RELIABILITY 中報告，屬次要的延續性標籤`
- OLD: `∅`
  NEW: `未曝露的`
- OLD: `∅`
  NEW: `此標籤；主要的構念效度判讀依表`
- OLD: ```
  NEW: `4-13 的 Q2 α。"`
- OLD: ``。`
  NEW: ` is a continuity label under the earlier 53B protocol, not evidence that the amended Q1–Q5 instrument is identical to 53B."`

### v1.8.1 L1778–1778 → v1.8.2 L1780–1780 (replace)

- OLD: `∅`
  NEW: `（S3）`
- OLD: `∅`
  NEW: `（協定已於 S1 凍結（人類編碼前），封包已備妥待發送，人類編碼尚未執行，結果待完成）`

### v1.8.1 L3022–3022 → v1.8.2 L3024–3024 (replace)

- OLD: `本`
  NEW: `v1.8.2 的修訂底`
- OLD: `∅`
  NEW: `（已保存；未覆寫）`

### v1.8.1 L3024–3024 → v1.8.2 L3026–3033 (replace)

- OLD: `READY_TO_RUN`
  NEW: `v1.8.1 版`
- OLD: `尚未執行`
  NEW: `已由 v1.8.2 檔案 24–30 取代；其封包顯示 G 編號，不得發送`
- OLD: `∅`
  NEW: `\| v1.8.2／24 \| — \| `24_RESEARCHER_DECISION_RECORD.md` \| V1 研究者決策紀錄（三位人類編碼者、遮蔽 G 編號、OA-2／OA-3 的決定） \| 稿件狀態；第 3.9.3 節 \|`
- OLD: `∅`
  NEW: `\| v1.8.2／25–26 \| — \| `25_V1_FINAL_PROTOCOL_v1_8_2.md`、`26_V1_FINAL_CODEBOOK_v1_8_2.md` \| V1 最終協定與編碼手冊（S1 凍結；人類編碼前） \| 第 3.9.3、4.7.3 節 \|`
- OLD: `∅`
  NEW: `\| v1.8.2／27 \| — \| `27_V1_PREFREEZE_AUDIT.md` \| V1 凍結前稽核（由程式計算；人類編碼尚未執行） \| 第 3.9.3 節 \|`
- OLD: `∅`
  NEW: `\| v1.8.2／28 \| — \| `28_V1_BLINDING_AND_RECRUITMENT_PLAN.md` \| 盲性與招募計畫（含公開儲存庫的限制） \| 第 3.9.3 節 \|`
- OLD: `∅`
  NEW: `\| v1.8.2／29 \| — \| `29_V1_ANALYSIS_PLAN_FROZEN.md`、`tools/v1_construct_analyzer_v182.py` \| 凍結的 V1 分析計畫與分析程式（Q2 α 為主要信度） \| 第 3.9.3、4.7.3 節 \|`
- OLD: `∅`
  NEW: `\| v1.8.2／30 \| — \| `30_V1_DISTRIBUTION_README.md`、`coder_distribution/`、`20_MASTER_PACKET_v1_8_2.xlsx` \| 封包發送說明與三份編碼者封包（已備妥待發送；研究團隊主檔不給編碼者） \| 第 4.7.3 節 \|`
- OLD: `∅`
  NEW: `\| v1.8.2／32 \| — \| `32_MERGED_MASTER_THESIS_v1_8_2_V1_PREFREEZE_CANDIDATE.md` \| 合併論文 v1.8.2（V1 凍結前版；只更新 V1 設計與狀態描述） \| 本稿 \|`

### v1.8.1 L3035–3035 → v1.8.2 L3044–3044 (replace)

- OLD: `雙人`
  NEW: `∅`
- OLD: `∅`
  NEW: `（三位獨立人類編碼者；v1.8.2 協定已於 S1 凍結，人類編碼尚未執行）`
- OLD: `預先登記`
  NEW: ` v1.8.2 凍結`
- OLD: `∅`
  NEW: `（V1.8.2 檔案 25、26、29）`
- OLD: `；至少兩`
  NEW: `：三`
- OLD: `∅`
  NEW: `獨立`
- OLD: `∅`
  NEW: `編碼者、不使用 AI `
- OLD: `∅`
  NEW: `遮蔽 G 編號的`
- OLD: `∅`
  NEW: `並填寫七項聲明；封包直接寄送，不經公開儲存庫`

