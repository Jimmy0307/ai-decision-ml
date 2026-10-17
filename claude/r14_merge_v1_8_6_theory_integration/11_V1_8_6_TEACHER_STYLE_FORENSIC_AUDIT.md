# 11 — V1.8.6 Teacher-Style Forensic Audit (auditor TA: thesis advisor / hostile Q1 reviewer)

- **Audited file:** `OUT\01_V1_8_6_THEORY_INTEGRATED_MANUSCRIPT.md`
- **Audited sha256:** `4d480a3e326bdb8f6850378148313e5736985a8324eec8a502fb16d661b64f36`. This is the rebuilt version: T23 removed the §5.7 "前所未見" sentence, and T28 added row E51 at l.3296. Both were re-read.
- **Line numbers:** refer to 01.
- **Companion file:** 05 (term-level claim-boundary table).
- **Scratch:** `work\TA\` (`diff.txt`, `scan.py`, `hits.tsv`).

## A. The 12 questions

| # | Question | Answer | Evidence |
|---|---|---|---|
| 1 | PARTIAL written as PASS? | **NO** | M1–M4 「充分性狀態 PARTIAL」 (l.777, 3035, 2395). Sequential identification 「PARTIAL」 (l.1303, 3090). Tie tolerance 「有條件成立（只限精確可負擔）」 = QUALIFIED (l.3050, 2453(3)). The "27/27 PASS" at l.2022 / 3116 refers to witnesses, which is correct. Minor gap: the pack-level `Q1_THEORY_UPGRADE_VERDICT = PARTIAL` (12 l.37) is not disclosed anywhere (m7) |
| 2 | Downgraded results re-promoted? | **NO** | DL-1 is 「Lemma DL-1，為 Lemma E′ 之重述，不作為主要定理」 (l.2395; also l.180, 1161, 3042). GS-I is 「恆等式」/「會計恆等式」 (l.1163, 2395, 3057). D1/D3 are 「重述」 (l.1165, 2379, 2395, 3068, 3070). R1 is 「為 Lemma R 之重述」 (l.1295, 2395, 3094). No "Theorem DL-1" or "GS-I theorem" anywhere. Minor: l.2034 (W7 row) says 「Thm R1（正向對照）」 without the 重述 tag. l.2395(4) groups 「Prop E.1–E.7」, although E.2 and E.3 are restatements and E.7 is a Thm (m9) |
| 3 | Synthetic as empirical? | **NO** | 「構造例只顯示存在性或反駁全稱主張」 (l.170). 「這些合成案例只建立計算一致性、形式存在性或反例，不是企業實證證據」 (l.2036). 「不支持重用非單調在實務上常見」 (l.2036). C.10.8 (l.3116) |
| 4 | V1 human results implied? | **NO results implied, but one pre-judging phrase** | l.781 is correct: 「人類編碼尚未執行，本節不使用也不預期任何結果」, and α high/low is correctly decoupled from sufficiency. **However**, l.113 and l.775 describe M1–M4 as 「操作上可區辨」. That label is not in the pack (10 rows 1.1/3.2; 01 l.14), and operational distinguishability is what V1 tests → **MAJOR-1** |
| 5 | V7 implied? | **NO** | No V7 result. l.182 lists 「AI 特定的實證參數化（V7）」 as part of the AI-specific contribution without noting that V7 is OPEN (m3). The parallel §5.7 text (l.2397) correctly omits V7 |
| 6 | M1–M4 as complete taxonomy? | **NO** | 「本研究不宣稱這組分解完備、普遍充分或唯一」 (l.113). 「M1–M4 的完備性、普遍充分性與唯一性都未建立…也不窮盡」 (l.777). Global sufficiency NOT_PROVEN (l.3035, 2453(8)). Minor: the residual lists at l.777 and l.3035 omit **time**, which pack 12 lists as a residual. l.779 covers it only implicitly via LONGITUDINAL (m6) |
| 7 | DL as iff? | **NO** | The positive iff is only first-best-relative (Lemma DL-1: l.1161, 2383, 3042) or under a unique first best (Cor DL-3, l.3045). 「這些結果不包含授權損失為正的原始條件充要刻畫」 (l.180). 「(A)–(F) 的任何布林組合，都不能構成…充要判準」 (l.1161). 5.8.10(1) (l.2453). Minor: l.2383 「DL 為零若且唯若…」 drops the opt/pess index (m4) |
| 8 | Governance screening as necessarily value-adding? | **NO** | 「本稿不宣稱治理要求一般會提高企業價值」 (l.1163). 「envelope 無法阻擋只是正篩選價值的必要條件…不是充分條件（W4c、W4d）」 (l.2369). 「但這不是一般性質」 (l.2383). Counter-witnesses W4b/W4c/W4d appear at l.1163 and 3063. The unchanged Abstract (l.15/l.31) still reads 「可藉由篩除…提高企業價值」 / "can raise enterprise value by screening". That is modal, so not a violation, but it is less bounded than the body (m11) |
| 9 | 367/400 swapped in as primary? | **NO** | 「W5…保留非區間建置區域 162/400 次，這是主要報告值」 and 「W5_WIDE 只作…敏感度分析…不作為主要結果，也不取代 W5」 (l.2036, l.3075, l.3116). This is consistent with R-4 |
| 10 | TO VERIFY citations used? | **NO** | No new citation key or author/year token in changed or new text. None of the 08 §3 "NO" items (Holmström, Alonso & Matouschek 2008 REStud, Armstrong & Vickers, Stoye, Chernoff, Topkis, Manski, Harris & Raviv, …) appears in 01. The analogue clause was removed (T23). E51 (l.3296) is name-free. The only reference-like token in changed text is the pre-existing 59a negation 「不宣稱特定治理框架（例如 NIST AI RMF 或 ISO/IEC 42001）…效果」 (l.2369). ISO/IEC 42001 is UNVERIFIED in 07, but no claim is attached to it |
| 11 | Coder instrument affected? | **NO instrument change. YES, a description inconsistency** | S1e packet sha256 values are unchanged: `cbbbaa0a…`, `5925ead5…`, `50d8c818…` (re-hashed by TA). l.779 explicitly says the readings do not change S1e categories or §3.9.3 semantics. **Mismatch:** §3.9.3 (l.755, protected, byte-identical to 59a) and the new §3.9.6 (l.779) use 「企業決策介面」 for Q1/NONE. The S1e packets use 「企業決策過程」 (S1e status: `CODER_INSTRUMENT_CHANGED_AFTER_S1D=YES`, wording + layout only). l.779 is also the first and only mention of "S1e" in 01, which is never introduced. **Classification: a manuscript-description inconsistency (pre-existing in 59a §3.9.3 and propagated into the new §3.9.6), not an instrument change** → **MAJOR-2** (changelog RD-1 already flags it, but does not fix the new sentence) |
| 12 | v2.2 equation semantics changed? | **NO** | Math spans and tags are identical (03 hard checks; TA diff). The P1–P8 statements are identical. The only edit inside a proposition bullet is the P2 **remark** (l.1152): 「需要池化資源」 → 「在至少一項池化資源上需要多於企業偏好配置的用量」. This is the Lemma S refinement, and it agrees with 42's semantics. The Lemma E′ erratum (l.1200, C.10.9) is proof wording only, and 51's numbers are unaffected (13, 15). C.2 and C.6 are verbatim. Minor: the status line (l.5) says 「不改變…命題 P1–P8 的陳述」. That is true, but it should also disclose 「P2 備註用語精確化」 (m13) |

## B. Readability and advisor-style pass

**Coherence in Traditional Chinese.**
- The new text is grammatical, uses the thesis's established terms (首佳、envelope、帳本、樂觀／悲觀), and labels its results consistently (重述／恆等式／引理／命題／推論／構造例／未證明).
- Main weakness: density. The DL paragraph at l.1161 is a single paragraph of about 1,000 characters with four labelled sub-parts (A)–(D) plus DL-6 and W3b. An advisor will ask for it to be split.
- The status line (l.5) has grown to about 3,500 characters.

**Placement of the new subsections.** These are logical:
- §3.9.6 comes after the V1 design, before §3.10.
- The 3.12.4 classification block comes after P8, before the decomposition.
- The §3.13 scope paragraphs sit next to the Lemma R and VOI text.
- §4.9.1 comes after Table 4-20C, before §4.10.
- §5.8.10 is the last limitation.
- C.10 comes after C.9.
- One ordering issue: the 3.12.4 governance paragraph (l.1163) ends with 「在下述分解中記入賦能區塊 EE」, but the decomposition paragraph (l.1173) comes only after the shared-capability paragraph (l.1165) (m12).

**3.12.4 block versus the existing P2/P8 remarks. No contradiction.**
- The P2 remark (l.1152) and block (B) at l.1161 agree. The block adds that "不對齊" includes AL3, which is consistent because (AL1)–(AL4) include AL3.
- The P8 parenthetical (l.1173) still says 「以規則替代無法以預算達成的協調」, but it is now immediately bounded by GS-I / GS-N. That is acceptable.
- C.6's verbatim P2 remark (l.2961) still has the imprecise 「需要池化資源」. C.10.2 should flag that it is superseded, as C.10.4 does for P4 and C.10.7 does for §3.14.3 (m10).

**Ch1 versus Ch5 consistency.**
- Ch1 §1.7.2 (l.180–184) and §5.7 (l.2395–2397) list the same contributions with the same labels (DL-1 restatement, Cor DL-2o, Cor DL-3, W3c, DL-6; GS-I identity, GS-1, GS-N; D6 existence; R/E scope; missingness; AI-specificity split).
- Ch1 l.170 matches the boundaries in §5.8.10.
- Differences:
  - Ch1 l.182 mentions V1/V7-dependent "AI 特定的實證參數化（V7）"; §5.7 does not (m3).
  - The Abstract and English Abstract (l.15, l.31) and the Ch6 conclusion were not updated. They are consistent but still read "proof sketches", and they omit the new formal contributions and their PARTIAL status (m11; RD-5).

### Major issues (exact minimal fix text; 01 not edited)

**MAJOR-1: 「操作上可區辨」 (l.113, l.775).** The phrase is not a pack label, and it pre-judges V1.
- l.113: replace 「一組在本研究既定企業 AI 決策問題範圍內、操作上可區辨且在型別定義 T1–T4 下非冗餘的企業機制分解」 with 「一組在本研究既定企業 AI 決策問題範圍內、以決策對象判準界定（其操作上的可區辨性待 V1 人類編碼檢驗）、且在型別定義 T1–T4 下對 v2.2 屬性結構非冗餘的企業機制分解」.
- l.775: replace 「操作上可區辨且在 T1–T4 型別定義下非冗餘的 mechanism decomposition」 with 「以決策對象判準界定、且在 T1–T4 型別定義下對 v2.2 屬性結構非冗餘的 mechanism decomposition（操作上的可區辨性由 V1 檢驗，尚未執行）」.

**MAJOR-2: 介面 versus 過程, and the undefined "S1e" (l.779).** This is a description inconsistency, not an instrument change. In l.779, replace 「NONE 是涵蓋缺口的訊號：存在可辨識的企業決策介面，但不在 M1–M4 工作集合內」 with 「NONE 是涵蓋缺口的訊號：存在可辨識的企業決策過程（S1e 編碼者材料的用語；第 3.9.3 節沿用 S1d 的「企業決策介面」，兩者指同一判斷，S1e 只改編碼者用語與答案表版面，不改類別定義），但不在 M1–M4 工作集合內」. §3.9.3 / Table 3-14 / E6 wording sync stays a researcher decision (RD-1).

### Minor issues (fix text)

- **m1 (= 05 O-3), l.1295:** replace 「只有在恰一個候選 portfolio 含該元素值時，頂點檢查才同時是必要條件（Prop R4）」 with 「若恰一個候選 portfolio 含該元素值，頂點檢查同時也是必要條件（Prop R4；此為充分條件下的特例，不表示其他情形必不精確）」.
- **m2, l.182 and l.2397:** after 「對任何共用平台的資訊科技 portfolio 都成立」 (l.182; the analogous clause at l.2397), add 「（指具相同模型結構者的形式適用範圍，不是經驗上的可推廣性）」.
- **m3, l.182:** replace 「AI 特定的實證參數化（V7）」 with 「AI 特定的實證參數化（V7，尚未執行）」.
- **m4, l.2383:** replace 「DL 為零若且唯若至少一個集中最適解可在雙層中自我實施」 with 「樂觀（悲觀）DL 為零，若且唯若至少一個集中最適解在雙層中可樂觀（悲觀）自我實施」.
- **m5, l.1161:** replace 「與求解 B 同樣困難」 with 「因此至少需先求解 B 並取得全部首佳解」. The pack says "as hard as" only informally; no complexity result is proven.
- **m6, l.777 and l.3035:** append 「，以及時間（跨期）維度（由 LONGITUDINAL／M5 處理，不屬靜態 M1–M4）」 to the residual list (pack 12, M1–M4 row).
- **m7, l.5 status line, after 「附錄 C.10.9 另記一項…勘誤…」:** add 「理論補充包的整體判定為 PARTIAL（Q1_THEORY_UPGRADE_VERDICT = PARTIAL；附錄 D）」.
- **m8, l.5 and l.1159:** at l.5, replace 「新增的形式結果皆為本研究的模型內結果（TYPE C）」 with 「新增的形式結果（含以明確前提重寫的 v2.2 重述）皆為本研究的模型內結果」. At l.1159, replace the header tag 「TYPE C」 with 「重述與 TYPE C」.
- **m9:**
  - l.2034: replace 「Thm R1（正向對照）」 with 「Thm R1（重述；正向對照）」.
  - l.2395(4): replace 「Prop E.1–E.7」 with 「Prop E.1、E.4–E.6 與 Thm E.7（E.2、E.3 為重述）」.
- **m10, C.10.2 (after l.3050):** add a bullet 「**與 v2.2 的關係。** C.6 的 P2 備註（「需要池化資源」）依逐字原則保留；其精確條件為 Lemma S，第 3.12.4、5.6 節已改用此精確用語。」
- **m11, Abstract (l.15) and English Abstract (l.31):** in a separate pass (RD-5), change 「可藉由篩除部門的不利選擇而提高企業價值」 to 「在特定的錯位與可分離性條件下，可藉由篩除部門的不利選擇而提高企業價值（不是一般性質）」, and make the matching EN edit.
- **m12, §3.12.4 ordering:** move the shared-capability paragraph (l.1165) after the decomposition paragraph (l.1173), or change 「在下述分解中」 to 「在本節稍後的治理價值分解中」.
- **m13, l.5:** add 「P2 的備註用語依 Lemma S 精確化（P2 陳述不變）」.
- **m14, l.3044:** change 「Cor DL-2p（推論；AL3）」 to 「Cor DL-2p（推論；AL3；精確平手）」, consistent with 12/14 and 5.8.10(3).
- **m15, l.3059 (Prop GS-1):** append 「（經由 Lemma DL-1，近乎定義性；唯一首佳下為原始條件形式）」, per 14 §5.

### Verdict rationale

- There are no CRITICAL defects:
  - no number, equation, G-row, Study 1 token, solver or packet changed;
  - no human, enterprise or V7 result;
  - no TO VERIFY citation;
  - no theorem inflation;
  - primary W5 162/400 is preserved.
- The six R-2 fixes and the R-1 erratum are correctly applied.
- Two MAJOR wording or description issues remain, both fixable by single-sentence edits:
  - MAJOR-1 adds an unsupported qualifier that pre-judges V1;
  - MAJOR-2 is the coder-term inconsistency, plus an undefined "S1e".
- Until those two are applied, the candidate is PARTIAL.

```
AUDITED_SHA256=4d480a3e326bdb8f6850378148313e5736985a8324eec8a502fb16d661b64f36
MAJOR_ISSUES=2
MINOR_ISSUES=15
RECOMMENDED_VERDICT=PARTIAL
```

---

## Re-audit (sha256 bb0fa9e3…)

The earlier sections above are kept unchanged.

- **Audited file sha256:** `bb0fa9e3a52e8abd2d154994afb0f9cbe241efb95aa5616813b77ddb44957c43`. The fixes were applied as T29–T50.
- **Method:**
  - Fresh line diff of 59a against 01 (`work\TA\diff2.txt`) and the delta from the previous audit (`work\TA\delta.txt`, 90 lines).
  - Term scan re-run over all changed and new lines (`work\TA\hits.tsv`; the previous run is in `hits_v1.tsv`).
  - Character-level diff of Abstract l.15 and English Abstract l.31.
- **Hunk structure:** the same as before, plus l.15 and l.31 now changed, plus one more line in C.10 (the C.10.2 relation bullet).

### 1. Resolution of earlier items

| Item | Status | Evidence (01 line) |
|---|---|---|
| MAJOR-1 「操作上可區辨」 | **RESOLVED** | l.113: 「以決策對象判準界定（其操作上的可區辨性待 V1 人類編碼檢驗）、且…對 v2.2 屬性結構非冗餘」. l.775: 「（操作上的可區辨性由 V1 檢驗，尚未執行）」 |
| MAJOR-2 介面／過程 and undefined S1e | **RESOLVED** (within scope) | l.779 now uses 「企業決策過程（S1e 編碼者材料的用語；第 3.9.3 節沿用 S1d 的「企業決策介面」…不改類別定義）」. §3.9.3 is untouched (protected). The wider §3.9.3 / Table 3-14 / E6 sync stays researcher decision RD-1, and is now disclosed in the text |
| m1 R4 converse (l.1295) | RESOLVED | 「若恰一個…頂點檢查同時也是必要條件（Prop R4；此為充分條件下的特例…）」 |
| m2 generality qualifier | RESOLVED | l.182 and l.2397: 「（指具相同模型結構者的形式適用範圍，不是經驗上的可推廣性）」 |
| m3 V7 status | RESOLVED | l.182: 「（V7，尚未執行）」 |
| m4 opt/pess index | RESOLVED | l.2383 (and l.1161): 「樂觀（悲觀）DL 為零…可樂觀（悲觀）自我實施」 |
| m5 "as hard as B" | RESOLVED | l.1161: 「因此至少需先求解 B 並取得全部首佳解」 |
| m6 time residual | RESOLVED (cosmetic residue) | l.777 and l.3035 now add the time (跨期) dimension. At l.777 the sentence reads 「…以及 AI 對 AI 的輸出鏈，以及時間（跨期）維度…」 with 以及 doubled; see new n1 |
| m7 pack verdict PARTIAL | RESOLVED | l.5: 「理論補充包的整體判定為 PARTIAL（Q1_THEORY_UPGRADE_VERDICT = PARTIAL；附錄 D）」 |
| m8 TYPE C vs restatement | RESOLVED | l.5: 「（含以明確前提重寫的 v2.2 重述）」. l.1159: 「重述與 TYPE C」 |
| m9 R1 / E labels | RESOLVED | l.2034: 「Thm R1（重述；正向對照）」. l.2395: 「Prop E.1、E.4–E.6 與 Thm E.7（E.2、E.3 為重述）」 |
| m10 C.6 P2 remark supersession | RESOLVED | New bullet at l.3051 |
| m11 Abstract / English Abstract | RESOLVED | l.15 inserts only 「在特定的錯位與可分離性條件下，」 and 「（不是一般性質）」. l.31 inserts only ", under specific misalignment and separability conditions (not as a general property),". The character-level diff shows no other change. T47 mirrors the Chinese fix into English, which is acceptable |
| m12 forward reference | RESOLVED | l.1163: 「在本節稍後的治理價值分解中」 (the alternative wording) |
| m13 P2 remark disclosure | RESOLVED | l.5: 「P2 的備註用語依 Lemma S 精確化（P2 陳述不變）」 |
| m14 Cor DL-2p exact ties | RESOLVED | l.3044: 「（推論；AL3；精確平手）」 |
| m15 GS-1 near-definitional | RESOLVED | l.3060: 「（經由 Lemma DL-1，近乎定義性；唯一首佳下為原始條件形式）」 |

### 2. The 12 questions, re-run on the current 01

All 12 answers are **NO**, with no new evidence against them.

- (1) PARTIAL as PASS: NO. The pack verdict PARTIAL is now disclosed (l.5).
- (2) Downgraded results re-promoted: NO.
- (3) Synthetic as empirical: NO.
- (4) V1 results implied: NO. The pre-judging phrase was removed.
- (5) V7 implied: NO. l.182 now says 尚未執行.
- (6) M1–M4 as a complete taxonomy: NO.
- (7) DL as iff: NO.
- (8) Governance necessarily value-adding: NO. The Abstract is now bounded too.
- (9) 367/400 as primary: NO.
- (10) TO VERIFY citations used: NO. No new author/year tokens, and E51 remains name-free.
- (11) Coder instrument affected: NO. The packets are unchanged, and the description inconsistency is fixed in the new text and disclosed for §3.9.3.
- (12) v2.2 equation semantics changed: NO.

The claim scan of the fixes found no new overclaim:
- The new hits all come from the whole Abstract lines 15/31 now counting as "changed" (their old text is unchanged) and from line shifts.
- Every inserted phrase is a qualifier or negation.

### 3. Protected regions and S1e (re-verified by TA)

| Region / file | Result |
|---|---|
| §3.9.1–§3.9.5 | Byte-identical to 59a |
| Chapter 2 | Byte-identical to 59a |
| Appendix C.1–C.9 | Byte-identical to 59a |
| Reference list | Byte-identical to 59a |
| Math spans | Identical and in the same order (49 = 49) |
| G-rows | 35 = 35 |
| P1 and P3–P8 bullets | Identical |
| P2 bullet | Only the remark differs, as documented |
| S1e CODER_1/2/3 | `cbbbaa0a…` / `5925ead5…` / `50d8c818…`, unchanged |
| 42 / 51 | `0249e7b9…` / `37f26a52…`, unchanged |

### 4. New items

- **n1 (MINOR, cosmetic), l.777:** 「以及 AI 對 AI 的輸出鏈，以及時間（跨期）維度」 doubles 以及. Fix: 「、AI 對 AI 的輸出鏈，以及時間（跨期）維度」, which matches the l.3035 phrasing.
- **Noted, not counted:** the §3.9.3 / Table 3-14 / E6 terminology sync to S1e remains researcher decision RD-1. It is now disclosed in l.779.

```
AUDITED_SHA256=bb0fa9e3a52e8abd2d154994afb0f9cbe241efb95aa5616813b77ddb44957c43
MAJOR_ISSUES=0
MINOR_ISSUES=1
RECOMMENDED_VERDICT=PASS
```
(PASS is for the v1.8.6 theory-integration candidate only. SUBMISSION_READY stays NO.)
