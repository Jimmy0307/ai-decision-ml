# 05 — V1.8.6 Claim-Boundary Audit (auditor TA, independent)

- **Audited file:** `OUT\01_V1_8_6_THEORY_INTEGRATED_MANUSCRIPT.md`
- **Audited sha256:** `4d480a3e326bdb8f6850378148313e5736985a8324eec8a502fb16d661b64f36`. This is the rebuilt version that includes T23 (the §5.7 "前所未見" sentence is removed) and T28 (neutral row E51). Re-checked: "前所未見" is absent; E51 is at l.3296 and names no authors.
- **Base:** 59a, sha256 `bf4379a4…81bd` (verified).
- **Diff:** `work\TA\diff.txt`, a line diff of 59a against 01. It gives 27 hunks and 183 changed or new 01 lines, which matches 03 (14 lines changed in place, 2 replaced, 169 inserted).
- **Theory labels used:** pack 12 (final status), 14 §5–§6 (the T7/T8 final labels), 15, 13, 11, and the 01–06 statement texts where a label needed checking.
- **Hit list:** `work\TA\hits.tsv`, from the term scan `work\TA\scan.py` run over the changed and new lines only.
- **Other checks:** 07/08 for citations, and the S1e packets by hash (read-only).
- **Line numbers:** all refer to 01.

## 0. Hard facts checked independently

| Check | Result |
|---|---|
| S1e packets CODER_1/2/3 sha256 | `cbbbaa0a…` / `5925ead5…` / `50d8c818…`: unchanged |
| New author/year tokens in changed or new text | None. The only reference-like tokens are the pre-existing "NIST AI RMF / ISO/IEC 42001" non-claim sentence at l.2369 (in 59a; negated: 「不宣稱…效果」). No 08 §3 "NO" item (Holmström, Alonso & Matouschek, Armstrong & Vickers, Stoye, Chernoff, Topkis, Manski, …) appears anywhere in 01 |
| Equations (math spans, tags) | Unchanged per 03 hard checks. The diff shows only one `$…$` span touched, at l.1152 (P2), and its formula text is identical |
| W5 162/400 as primary, W5_WIDE 367/400 as sensitivity only | Yes (l.2036, l.3075) |
| `DL_IFF_THEOREM` | Never written as a theorem. Every "若且唯若" is one of: first-best-relative (DL-1, l.1161 / 2383 / 3042), unique-first-best (Cor DL-3, l.3045), Lemma S separability (l.3041), restatement (R1 l.3094, E.10), R2/R4 element-level characterizations, or G4/G7 |

## 1. Term-by-term classification (changed or new text)

Hit counts are over the changed and new lines only (`hits.tsv`). Classes:
- **S** = SUPPORTED: the text matches the pack id or witness.
- **B** = NEGATED-OR-BOUNDED: fine as written.
- **O** = OVERCLAIM: needs a fix (given in §3).

| Term (zh / en) | Hits | Lines | Class | Basis / note |
|---|---|---|---|---|
| minimal sufficient / 最小充分 | 0 | — | — | Removed from l.113, as R-2 requires. No other occurrence in 01 |
| complete / 完整 / 完備 / 窮盡 | 15 | 113, 777, 3035 (negated: 「不宣稱…完備」「不窮盡」「完備性…未建立」); 5, 1305, 2018, 3026 (「完整列舉」「完整證明」「完整決策對應」, technical) | B | Pack 01 §6.3 and 12: M1–M4 = PARTIAL |
| all enterprise / 所有企業 | 0 | — | — | — |
| construct validity / 構念效度 | 4 | 5 (retained 59a status text; V1 pending) | B | No new construct-validity claim. **However**, see O-1: 「操作上可區辨」 implies an untested operational validity |
| validated / 已驗證 / 驗證完成 | 0 | — | — | — |
| proved / 證明 | 44 | 170, 2020, 2022, 3026 (「不能用來證明」「未被反駁不等於被證明」「不是一般定理的證明」); 1303, 1357, 2453 (scoped "只對固定候選集合證明", NOT_PROVEN list); 3033–3124 (proof sketches) | S/B | 02–07 proofs; 15 verified repairs |
| theorem / 定理 / Thm | 29 | Thm GS-N (1163, 3061); Thm E.7 (1303, 1357, 3087); Thm D1/D3 (1165, 3068, 3070, 2379, 2395); Thm R1 (1295, 2034, 2395, 3094) | S | GS-N = "Theorem" (03 l.129, l.163). E.7 = "THEOREM (proved)" (05 l.26). D1/D3/R1 are tagged **重述** at every main-text occurrence except l.2034 (minor m9). DL-1 is always "Lemma … 重述", never a theorem. GS-I is always "恆等式" |
| optimal / 最適 / 最佳 | 49 | Model-internal "首佳／最適解／最佳回應" throughout; 1303, 1357, 2453 「VOI-greedy…未證明」「不表示…為最適」 | S/B | No claim of an optimal enterprise architecture |
| causal / 因果 | 0 | — | — | — |
| generalizable / 可推廣 / 一般形式 | 6 | 182, 2397 「…是企業—事業單位架構的一般形式性質…對任何共用平台的資訊科技 portfolio 都成立」 | S, but needs a qualifier (m2) | Pack 03 §10 / 12 §3: "hold for any shared-platform IT portfolio" (a formal, structural statement). It must not be readable as empirical generalizability |
| enterprise evidence / 企業證據 / 實證 | 8 | 5, 180, 182, 1916, 2036, 2383, 2397, 3116 | B | All negations: 「不是企業實證證據」「EMPIRICAL RESULT PENDING」. l.182 lists "AI 特定的實證參數化（V7）" as part of the AI-specific contribution without saying that V7 is OPEN (m3) |
| AI-specific / AI 特有 / AI 特定 | 10 | 182, 2397, 3064 | S | Pack 12 §3, 14 A11. 3064 is the AI-specific *corollary*, correctly labelled 「不是新結果」 |
| robust / 穩健 | 23 | 184, 1295, 2383, 3092–3099 | S | Scope matches 06: whole-portfolio B/A+ only. **1295, the R4 clause, is O-3** |
| necessary / 必要 | 22 | 1152, 1161, 1163, 1173, 2369, 2375, 2379, 2395, 2453, 3044, 3061 | S | DL-2o/2p are under AL3 + exact ties. GS-N is exact ties. "Misalignment is necessary, not sufficient" matches Lemma S / DL-6. **1295 is O-3** |
| sufficient / 充分 | 32 | 113, 777, 779, 781 (negated); 1161, 1163, 1165, 2379, 3046, 3059, 3071 | S | DL-4 (AL3, exact ties), GS-1, D4/D5 ("(AL) is sufficient, not necessary": 04 D4/D5, 14 §2.15). GS-1 is "near-definitional via DL-1" in 14 §5; the manuscript does not say so (m15) |
| iff / 若且唯若 / 充要 | 23 | See §0 | S/B | Every positive iff is scoped. 「充要」 occurs only negated (180, 1161, 1163, 2453). 2383 drops the opt/pess index (m4) |

## 2. Targeted pattern checks

| Pattern | Finding | Class |
|---|---|---|
| Necessary written as sufficient | l.2369 (P8 "substitute" sentence) is fixed: 「其條件只是必要條件」, with W4c/W4d. l.2375 and l.1152 are fixed via Lemma S. **But l.1295 has the converse error: R4's sufficient condition is written as 「只有…才」 (only-if)** | O-3 |
| Sufficient written as iff | None. "DL>0 iff" appears only under a unique first best (3045), or negated | B |
| Existence written as universal | D6 at 1165 is 「D6 只是存在性結果，不表示…多半如此」. The W5 note at 2036 says 「不支持重用非單調在實務上常見」 | B |
| Synthetic written as empirical | None. Every witness is SIMULATED_ONLY (2022, 2024, 2036, 3116) | B |
| Non-redundant written as complete | 777 and 3033 are 「定義性…不驗證此分類」, PARTIAL. But l.113 and l.775 add 「操作上可區辨」, which is not in the pack label (10 row 1.1 / 3.2; 01 l.14) | **O-1** |
| Mathematical verification written as enterprise validation | None. 2020 states 「未被反駁不等於被證明」, and the 4.9 intro (1916) is retained | B |
| PARTIAL written as PASS | M1–M4 PARTIAL (777, 3035, 2395). Sequential identification PARTIAL (1303, 3090). Tie tolerance is 「有條件成立」 = QUALIFIED (3050). The pack's overall `Q1_THEORY_UPGRADE_VERDICT = PARTIAL` is not stated anywhere in 01 (m7) | B (m7) |
| Downgraded results re-promoted (DL-1 as theorem, GS-I as theorem, D1/D3/R1 as new) | Not found. DL-1 is "Lemma…重述，不作為主要定理" (2395). GS-I is 「會計恆等式」. D1/D3/R1 are 「重述」. The block header at l.1159 tags the whole block 「TYPE C」, and the status line at l.5 says 「新增的形式結果皆為…TYPE C」 although the block contains restatements (m8) | B (m8) |
| V1 human results implied | 781 「人類編碼尚未執行，本節不使用也不預期任何結果」 is correct. O-1 (「操作上可區辨」) is the only implicit pre-judgement of V1 | O-1 |
| V7 implied | No V7 result. l.182 names V7 as a contribution component without an OPEN tag (m3) | B (m3) |
| Governance always adds value | No. 1163, 2369, 2383 say 「不宣稱治理要求一般會提高企業價值」. The unchanged Abstract (l.15, l.31: 「可藉由篩除…而提高企業價值」 / "can raise enterprise value by screening") is consistent but less precise (m11) | B |
| 367/400 as primary | No. 2036 and 3075 give 162/400 as primary | B |
| TO VERIFY citations in main text | None. No new key. No 08 §3 NO-item in 01. E51 is neutral | B |
| v2.2 equation semantics change | None. Math spans are identical. P1–P8 statements are identical. The P2 *remark* (l.1152) is refined, and its meaning is consistent with 42 (Lemma S). The status-line wording 「不改變…P1–P8 的陳述」 is true, but the remark edit should be disclosed there (m13) | B |
| Coder instrument impact | Packets are unchanged (hash). 779 states that it does not change the S1e categories or the §3.9.3 semantics. **However**, 779 defines NONE using 「企業決策介面」, while S1e uses 「企業決策過程」 | **O-2** (description inconsistency; not an instrument change) |
| Lemma E′ erratum (R-1) | Wording only (1200, 3118–3124). No number changed. The "QUALIFIED: exact affordability only; 51's +1e-9 slack open" caveat is present (3042, 3123, 2453) | S (13, 15) |
| R-2 six fixes + l.113 | l.1327 → 1355 (G7). l.1277 → 1301 (fixed candidate set). l.2317 → 2369. l.1329 → 1357. l.1138 / 2323 → 1152 / 2375. l.113 is done but over-qualified (O-1) | S |

## 3. Spot-check of unchanged text against the new theory results

| Location | Text | Status |
|---|---|---|
| l.2961, C.6 P2 remark (verbatim v2.2) | 「若不對齊部門偏好的配置需要池化資源，企業可以用較小的 envelope 阻止它」 | Imprecise relative to Lemma S (the fix that R-2 applied at 1152 / 2375). C.6 is verbatim and must stay. C.10.2 should add a one-line supersession note, as C.10.4 does for P4 and C.10.7 does for §3.14.3 (m10) |
| l.1173, the P8 parenthetical | 「以規則替代無法以預算達成的協調」 | Now bounded by the added GS-I / GS-N clause. Acceptable |
| l.15 / l.31, Abstract | 「以證明草稿說明…可藉由篩除…提高企業價值」 / "Proof sketches indicate…" | Not contradicted, but less precise and not updated (RD-5; m11) |
| l.2156, l.2167 (4.10.5) | 「C 中 `PR_X < 0` → 篩選」 | Consistent |
| l.1057 | "Model B 整體 portfolio 的 Lemma R…頂點精確性在 (A-INV) 下成立" | Consistent with the R1 scope |
| l.1945 / 4-20 rows | VOI "網格 = 真值" | Qualified at 1945 |
| l.755, §3.9.3 (protected) | Q1 / NONE use 「企業決策介面」 | Pre-existing mismatch with S1e (see O-2; changelog RD-1) |

## 4. Overclaims and exact minimal fixes (01 was not edited)

**O-1 (MAJOR): 「操作上可區辨」 at l.113 and l.775 is not a theory-pack label, and it pre-judges V1.**
- Problem:
  - Pack 10 rows 1.1 / 3.2 and pack 01 l.14 label M1–M4 only as non-redundant under T1–T4 *relative to the v2.2 attribute schema*: definitional, PARTIAL, otherwise a conceptual decomposition.
  - Operational distinguishability is exactly what V1 (human, pending) tests.
- Fix at l.113: replace 「一組在本研究既定企業 AI 決策問題範圍內、操作上可區辨且在型別定義 T1–T4 下非冗餘的企業機制分解」 with 「一組在本研究既定企業 AI 決策問題範圍內、以決策對象判準界定（其操作上的可區辨性待 V1 人類編碼檢驗）、且在型別定義 T1–T4 下對 v2.2 屬性結構非冗餘的企業機制分解」.
- Fix at l.775: replace 「操作上可區辨且在 T1–T4 型別定義下非冗餘的 mechanism decomposition」 with 「以決策對象判準界定、且在 T1–T4 型別定義下對 v2.2 屬性結構非冗餘的 mechanism decomposition（操作上的可區辨性由 V1 檢驗，尚未執行）」.

**O-2 (MAJOR; pre-existing description inconsistency, now propagated into new text): the term 「企業決策介面」 versus S1e 「企業決策過程」.**
- Problem:
  - New l.779 defines NONE as 「存在可辨識的企業決策介面」 and calls the instrument "S1e 編碼者材料".
  - Yet 01 never introduces S1e: §3.9.3 and the status line still describe the S1 / v1.8.2 (S1d) wording.
  - The teacher-approved S1e packets (hash-unchanged) use 「企業決策過程」. Per `V1_S1E_CURRENT_STATUS.md`, `CODER_INSTRUMENT_CHANGED_AFTER_S1D=YES`, scope = wording + layout.
- Classification: a **manuscript-description inconsistency**. It is **not an instrument change** by v1.8.6, because the packets are byte-identical.
- Fix (minimal; §3.9.3 stays protected): in l.779, replace 「NONE 是涵蓋缺口的訊號：存在可辨識的企業決策介面，但不在 M1–M4 工作集合內」 with 「NONE 是涵蓋缺口的訊號：存在可辨識的企業決策過程（S1e 編碼者材料的用語；第 3.9.3 節沿用 S1d 的「企業決策介面」，兩者指同一判斷，S1e 只改編碼者用語與答案表版面，不改類別定義），但不在 M1–M4 工作集合內」.
- Follow-up: the researcher should sync the §3.9.3 / Table 3-14 / E6 wording in a separate V1-text pass (RD-1).

**O-3 (MINOR): the R4 converse at l.1295.**
- Problem: 「只有在恰一個候選 portfolio 含該元素值時，頂點檢查才同時是必要條件（Prop R4）」 turns R4's sufficient condition (06 l.75–76) into an only-if.
- Fix: replace it with 「若恰一個候選 portfolio 含該元素值，頂點檢查同時也是必要條件（Prop R4；此為充分條件下的特例，不表示其他情形必不精確）」.

Further MINOR items (m2–m15, with fix text) are in 11 §B.

```
AUDITED_SHA256=4d480a3e326bdb8f6850378148313e5736985a8324eec8a502fb16d661b64f36
OVERCLAIM_MAJOR=2 (O-1, O-2)
OVERCLAIM_MINOR=1 (O-3) + 13 minor precision items (see 11)
TO_VERIFY_CITATIONS_IN_MAIN_TEXT=0
V2_2_EQUATION_SEMANTICS_CHANGED=NO
CODER_INSTRUMENT_CHANGED_BY_V1_8_6=NO (description inconsistency only)
```

---

## Re-audit (sha256 bb0fa9e3…)

The earlier sections above are kept unchanged.

- **Audited file sha256:** `bb0fa9e3a52e8abd2d154994afb0f9cbe241efb95aa5616813b77ddb44957c43`. The fixes were applied as T29–T50. Details are in 11, "Re-audit".

**Earlier overclaims:**
- **O-1 (操作上可區辨):** RESOLVED (l.113, l.775).
- **O-2 (介面／過程):** RESOLVED in new text (l.779). It is still a manuscript-description issue only: the S1e packets are hash-unchanged, and the §3.9.3 sync remains researcher decision RD-1.
- **O-3 (R4 only-if):** RESOLVED (l.1295).
- **The 13 precision items (m2–m15):** all RESOLVED.

**Term scan re-run** on all changed and new lines (`work\TA\hits.tsv`):
- No new OVERCLAIM.
- Abstract l.15 and l.31 now appear as changed lines. Their only insertions are the qualifiers 「在特定的錯位與可分離性條件下，」, 「（不是一般性質）」 and ", under specific misalignment and separability conditions (not as a general property),".
- The other new insertions are all bounding or negating phrases:
  - 「待 V1 人類編碼檢驗」「尚未執行」
  - 「形式適用範圍，不是經驗上的可推廣性」
  - 「近乎定義性」
  - 「精確平手」
  - 「（含…重述）」
  - 「整體判定為 PARTIAL」
- No citation key was added. No TO VERIFY item appears in main text.
- Math spans, the reference list, §3.9.1–3.9.5, C.1–C.9, the G-rows, 42/51 and the S1e packets are all unchanged.

**One new cosmetic item:** n1, the doubled 以及 at l.777 (see 11).

```
AUDITED_SHA256=bb0fa9e3a52e8abd2d154994afb0f9cbe241efb95aa5616813b77ddb44957c43
OVERCLAIM_MAJOR=0
OVERCLAIM_MINOR=0 (+1 cosmetic, n1)
TO_VERIFY_CITATIONS_IN_MAIN_TEXT=0
V2_2_EQUATION_SEMANTICS_CHANGED=NO
CODER_INSTRUMENT_CHANGED_BY_V1_8_6=NO
MAJOR_ISSUES=0
MINOR_ISSUES=1
RECOMMENDED_VERDICT=PASS
```
