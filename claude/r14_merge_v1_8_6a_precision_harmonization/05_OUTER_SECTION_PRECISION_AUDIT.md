# 05 — V1.8.6a Outer-Section Precision Audit (RD-5) and Claim-Consistency Sweep

- **Audited / patched file:** `01_V1_8_6A_MANUSCRIPT.md` sha256 `12eee36a8c1a762a16603deb4f46d2962cc4019a62e443241c082629546d9517`; base V1.8.6 `94d41d56…`.
- **Authority for claim wording:** V1.8.6 `06_V1_8_6_THEORY_STATUS_MATRIX.md` (row cited per edit). Rule: only reduce overclaim, add scope conditions, separate necessary/sufficient, existence/universal, synthetic/empirical, AI-specific/general, human reliability/validity. No new claim; no citation added.
- Line numbers are V1.8.6 01 lines.

## 1. RD-5 items (from V1.8.6 12 RD-5 / 02 RD-5)

| # | Patch | Location | Old | New | Matrix row / justification |
|---|---|---|---|---|---|
| 1 | H35 | 表 1-1 研究問題四 (L150) (l.150) | ¦ 3.11、3.12 ¦ 4.10 ¦ 模型完成；合成驗證完成（僅合成）；實證待完成（V7） ¦ | ¦ 3.11、3.12 ¦ 4.10 ¦ 模型完成；模型內形式結果（第 3.12.4 節；附錄 C.10）：DL 為零的首佳相對刻畫（Lemma DL-1，為 Lemma E′ 之重述）、DL 為正的必要條件（AL3 且精確平手下，Cor DL-2o／2p）與充分條件（唯一首佳下，Cor DL-3），沒有不依賴首佳解的充要刻畫；合成驗證完成（僅合成）；實證待完成（V7） ¦ | V1.8.6 06 status matrix rows DL (characterization lemma / necessary / sufficient / primitive iff NOT_PROVEN); V1.8.6 12 RD-5 |
| 2 | H36 | 表 1-1 研究問題五 (L151) (l.151) | ¦ 3.10.4、3.11–3.13 ¦ 4.10 ¦ 模型完成；合成驗證完成（僅合成；v2.4 部分為候選）；實證待完成（V7） ¦ | ¦ 3.10.4、3.11–3.13 ¦ 4.10 ¦ 模型完成；模型內形式結果：治理篩選為條件性結果（恆等式 GS-I、充分條件 Prop GS-1、精確平手下的必要條件 Thm GS-N；不是一般性質），共享能力重用在 B 中單調（Thm D1，P4 之重述）、在 C 中以帳本對齊為充分條件（Thm D3，重述），否則存在建置區域不是區間的實例（Prop D6，存在性結果）；合成驗證完成（僅合成；v2.4 部分為候選）；實證待完成（V7） ¦ | V1.8.6 06 status matrix rows Screening (GS-I identity, GS-1 sufficient, GS-N necessary exact ties, never 'always'); Shared capability (D1/D3 restatement, D6 existence); V1.8.6 12 RD-5 |
| 3 | H37 | 表 1-1 研究問題六 (L152) (l.152) | ¦ 3.13、3.14 ¦ 4.8、4.10 ¦ 模型完成；合成驗證完成（僅合成）；實證待完成（V7） ¦ | ¦ 3.13、3.14 ¦ 4.8、4.10 ¦ 模型完成；頂點精確性只限 Model B（及 A+）的整個 portfolio（Thm R1，為 Lemma R 之重述）；VOI 的次序只對固定候選集合成立（Prop E.1、E.2），序列識別性質為 PARTIAL；合成驗證完成（僅合成）；實證待完成（V7） ¦ | V1.8.6 06 status matrix rows Robustness (vertex-exactness scope); VOI (sequential identification PARTIAL; fixed candidate set); V1.8.6 12 RD-5 |
| 4 | H38 | 2.13 對模型的意涵 (iv) (L332) (l.332) | (iv) 跨層衝突以帳本對齊條件 (AL1)–(AL4) 檢驗；對齊時授權損失為零（P2）。 | (iv) 跨層衝突以帳本對齊條件 (AL1)–(AL4) 檢驗；對齊時授權損失為零（P2）——對齊是授權損失為零的充分而非必要條件，不對齊也不足以使授權損失為正（第 3.12.4 節）。 | V1.8.6 06 status matrix rows DL necessary / sufficient (W2: misaligned but blockable, DL = 0); V1.8.6 12 RD-5 |
| 5 | H39 | 2.13 對模型的意涵 (vii) (L332) (l.332) | 輸出 ROBUST／CONDITIONAL／FRAGILE／UNIDENTIFIED。 ⏎  ⏎ ## 2.14 | 輸出 ROBUST／CONDITIONAL／FRAGILE／UNIDENTIFIED。(vii) 第 3.12.4 節與附錄 C.10 的授權損失、治理篩選與共享能力重用結果，是本研究在完全資訊、固定參數下的模型內結果（其中 Lemma DL-1 為 Lemma E′ 於首佳解之重述），不是上述文獻的主張。 ⏎  ⏎ ## 2.14 | V1.8.6 06 status matrix rows DL-1 RESTATEMENT, TYPE C labels; References row (0 new citations); theory pack 10 row 2.1 without the TO-VERIFY analogue clause |
| 6 | H40 | 表 3-10 Q2 (L1184) (l.1184) | ¦ 損益兩平固定成本 `F_c^†`、重用門檻 `δ^†` ¦ 五 ¦ | ¦ 損益兩平固定成本 `F_c^†`、重用門檻 `δ^†`（B 中唯一；C 中帳本對齊時唯一，否則報告集合值的建置區域與平手慣例） ¦ 五 ¦ | V1.8.6 06 status matrix rows Shared capability (D1 B monotone, D3 alignment, D6 existence); theory pack 10 §5 Q2 |
| 7 | H41 | 表 3-10 Q4 (L1186) (l.1186) | ¦ DL 及其來源分解 ¦ 四 ¦ | ¦ DL 及其來源分解（報告不成立的對齊條件，以及存在不可阻擋偏離的首佳計畫；成對檢查不足以判定 DL 的正負，W3c） ¦ 四 ¦ | V1.8.6 06 status matrix rows DL characterization (first-best-relative), primitive iff NOT_PROVEN (W3c); theory pack 10 §5 Q4 |
| 8 | H42 | 表 3-10 Q7 (L1189) (l.1189) | ¦ 元素層級穩健性分類、MaxRegret ¦ 六 ¦ | ¦ 元素層級穩健性分類（以涵蓋率報告）、MaxRegret（頂點精確只限 Model B 及 A+ 的整個 portfolio） ¦ 六 ¦ | V1.8.6 06 status matrix row Robustness (vertex-exactness scope); theory pack 10 §5 Q7 |
| 9 | H43 | 4.10.3 判讀規則 (L2114–2115) (l.2114) |   - 只有 Model B 的整體 portfolio 有精確證書（Lemma R）。元素層級與 Model C 只報涵蓋率，不稱「對所有 θ」。 ⏎   - VOI 同時報頂點版（可能高估）與網格版。 |   - 只有 Model B（及 A+）的整體 portfolio 在第 3.13 節所列前提 (R-a)–(R-e) 下有精確證書（Lemma R）。元素層級（除 Prop R4 的情形）與 Model C 只報涵蓋率，不稱「對所有 θ」。 ⏎   - VOI 同時報頂點版（可能高估）與網格版；兩者只在固定候選集合（第一批登記時的 ROBUSTLY_FEASIBLE 集合）下為真值的上界，重算候選集合只作次要診斷並標 `CANDIDATE_SET_EXPANDED`（第 3.14.3 節）。 | V1.8.6 06 status matrix rows Robustness, VOI; V1.8.6 12 RD-5 |
| 10 | H44 | 表 4-33 研究問題五 (L2268) (l.2268) | 共享重用效果在雙層且帳本不對齊時可使建置區域為集合值； | 共享重用效果在雙層且帳本不對齊時可使建置區域為集合值（存在性結果，Prop D6）； | V1.8.6 06 status matrix row Prop D6 (existence only; never 'generally non-monotone') |
| 11 | H45 | 表 4-33 研究問題五 (L2268) (l.2268) | P8 在雙層且帳本不對齊時要求可具篩選價值； | P8 在雙層且帳本不對齊時要求可具篩選價值（只在特定的錯位與可分離性條件下；篩選價值不超過較寬鬆要求下的授權損失，恆等式 GS-I）； | V1.8.6 06 status matrix rows Screening (GS-I identity; witnesses: 'may have positive screening value under specific…conditions'; never 'always') |
| 12 | H46 | 表 4-33 研究問題六 (L2269) (l.2269) | 研究設計：只有 Model B 的整體 portfolio 具精確穩健性證書（Lemma R）；元素層級與 Model C 只報涵蓋率；VOI 同時報頂點版與網格版。 | 研究設計：只有 Model B（及 A+）的整體 portfolio 具精確穩健性證書（Lemma R；前提見第 3.13 節）；元素層級（除 Prop R4 的情形）與 Model C 只報涵蓋率；VOI 同時報頂點版（可能高估）與網格版，兩者只在固定候選集合下為真值的上界（Prop E.1、E.2），依 VOI 排序之量測順序的最適性未證明。 | V1.8.6 06 status matrix rows Robustness, VOI (PARTIAL; VOI-greedy optimality open); V1.8.6 12 RD-5 |
| 13 | H47 | 5.8.4 (L2429) (l.2429) | 文獻分析的人工稽核（第 3.7 節）驗證的是語意證據與功能分類，不能替代 V1。 | 文獻分析的人工稽核（第 3.7 節）驗證的是語意證據與功能分類，不能替代 V1。V1 檢驗的是 G→M 對應在凍結類別定義下的編碼者間可詮釋性，不檢驗 M1–M4 的非冗餘性或充分性；NONE 是涵蓋缺口的訊號，AMBIGUOUS 用於證據不足或兩類並列的類別邊界情形，兩者的有無都不能建立或否定 M1–M4 的充分性（第 3.9.6 節）。 | V1.8.6 06 status matrix row M1–M4 (PARTIAL; minimal sufficiency NOT_PROVEN); theory pack 10 §10 'Also' §5.8.4; V1.8.6 12 RD-5 |
| 14 | H48 | 5.8.5 (L2433) (l.2433) | 只有取得「企業與部門知道不同參數」的證據，才執行資訊不對稱的敏感度分析。 | 只有取得「企業與部門知道不同參數」的證據，才執行資訊不對稱的敏感度分析；資訊不對稱的側車目前只是設計（SIDECAR_DESIGN_ONLY），不修改 v2.2，其完全資訊特例重現 P3（第 5.8.10 節）。 | V1.8.6 06 status matrix row Information asymmetry (SIDECAR_DESIGN_ONLY; limitations only); theory pack 10 §10 'Also' §5.8.5 |

**RD-5 list status:** Table 1-1 RQ4–RQ6 → RESOLVED (H35–H37). §2.13 implications → RESOLVED (H38 necessary/sufficient; H39 model-internal vs literature attribution, without the theory pack's TO-VERIFY analogue clause). Table 4-33 RQ6 VOI qualifier → RESOLVED (H46; plus RQ5 H44, H45). §4.10.3 → RESOLVED (H43). §3.12.5 Q2/Q4/Q7 rows → RESOLVED (H40–H42; Q1, Q3, Q5, Q8 rows need no change; Appendix C.5 is verbatim v2.2 and stays). §5.8.4 / §5.8.5 pointers → RESOLVED (H47, H48). Abstract / English Abstract: the screening clause was already bounded in V1.8.6 (T46/T47); the remaining 「以證明草稿說明」/"Proof sketches indicate" is accurate (C.6 contains proof sketches) → no change. MINOR items of V1.8.6 05/11 not yet applied: none (m1–m15 and n1 were resolved in V1.8.6 per the re-audits).

## 2. Claim-consistency sweep

Whole-document term scan (`work/PH/sweep.py`; hits in `work/PH/sweep_hits_v186a.tsv`, V1.8.6 baseline in `sweep_hits_v186.tsv`). Counts V1.8.6 → V1.8.6a:

| Term | V1.8.6 | V1.8.6a | Finding |
|---|---|---|---|
| 企業決策介面 | 17 | 5 | See 03: 14 changed / synced, 3 kept as historical or protected labels; 2 new mentions in notes. |
| 企業決策過程 | 1 | 9 | Only as the S1e coder-facing wording (§3.9.3, §3.9.6, Table 3-14, Table 4-13, E6, L5). |
| 企業決策機制 | 1 | 25 | Theoretical construct term throughout. |
| 組織決策安排 | 0 | 3 | Only as the alternative wording in the notes (L5, §3.9.1, §3.9.3 verbatim sentence). |
| 最小充分/minimal sufficient | 0 | 0 | 0 hits. M1–M4 are never called minimal sufficient. |
| 完整/complete | 129 | 129 | Technical (完整列舉, 完整重分析, 完整證明…) or negated (不宣稱…完備, 不窮盡). M1–M4 never called a complete taxonomy. |
| 非冗餘/non-redundant | 14 | 15 | M1–M4: "non-redundant under T1–T4 relative to the v2.2 attribute schema (definitional)", sufficiency PARTIAL; operational distinguishability "to be tested by V1, not yet run" (l.113, l.775 kept). Other hits are Burt non-redundant ties. |
| 必要/necessary | 43 | 48 | DL necessary conditions only under AL3 + exact ties, plus the AL3 channel; GS-N exact ties. One imprecise sentence fixed (H49). |
| 充分/sufficient | 48 | 55 | DL sufficient conditions (Cor DL-3 unique first best; DL-4 for DL = 0), GS-1, D4/D5 ("alignment sufficient, not necessary"), H38. Never written as iff. |
| 若且唯若/iff | 21 | 22 | Only first-best-relative (DL-1), unique-first-best (Cor DL-3), Lemma S, R1/R2, G4/G7, P^C = P^B ⇔ AL3; 充要 only negated / NOT_PROVEN. No DL iff theorem. |
| 定理/theorem | 30 | 34 | Thm GS-N, Thm E.7 (theorems); Thm D1/D3/R1 always tagged 重述. DL-1 is a lemma, GS-I an identity. |
| 驗證/validated | 6 | 6 | Only "合成驗證完成（僅合成）" and negations; no "validated" construct or model. |
| 構念效度/construct validity | 28 | 28 | Always pending (V1 HUMAN RESULT PENDING) or negated (AI pilot / researcher adjudication ≠ construct validity). |
| 實證/empirical | 80 | 82 | All pending or negated (EMPIRICAL RESULT PENDING; 不是企業實證證據). §5.7 AI-specific empirical parameterisation now tagged V7 尚未執行 (H52). |
| AI 特有/AI-specific | 13 | 13 | General formal property vs AI-specific instantiation split kept (l.182, l.2397); "AI 特定的推論（不是新結果）" in C.10.3. |
| 最適/optimal | 158 | 159 | Model-internal (首佳、最適解、最佳回應) or negated (不宣稱最適的企業人工智慧架構; VOI-greedy optimality NOT_PROVEN). |
| 可推廣/generalizable | 16 | 16 | Negated (不可外推, 外部效度未知) or "formal scope, not empirical generalizability". |

**Confirmed boundaries (after this pass):**
- M1–M4 = a mechanism decomposition defined by the decision-object criterion, non-redundant under T1–T4 relative to the v2.2 attribute schema (definitional); operational distinguishability is to be tested by V1 (not run); NOT minimal sufficient, NOT a complete taxonomy (06 rows M1–M4).
- DL = necessary conditions and sufficient conditions exist (and a first-best-relative characterization lemma); no primitive iff (06 rows DL).
- Governance screening = conditional formal result (identity GS-I, sufficient GS-1, necessary GS-N in exact ties; never "always") (06 rows Screening).
- Shared capability = existence of a non-interval build region (Prop D6), D1/D3 restatements; never "generally non-monotone" (06 rows Shared capability).
- VOI/robustness: vertex exactness only for Model B (and A+) whole portfolio; VOI order only for a fixed candidate set; sequential identification PARTIAL (06 rows VOI, Robustness).

**Inconsistencies found and fixed (minimal edits):**

| Patch | Location | Old | New | Matrix row |
|---|---|---|---|---|
| H49 | 5.6 企業協調的價值來源 (L2377) (l.2377) | DL 只在帳本不對齊且 envelope 無法分離不利配置時為正。 | DL 為正的必要條件是帳本不對齊：在 AL3 成立時，還須有 envelope 無法分離的不利配置（Cor DL-2o／2p），AL3 不成立時部門專屬限制本身即可使 DL 為正（第 3.12.4 節）；這些都只是必要條件，不是充分條件。 | V1.8.6 06 status matrix row DL necessary conditions (DL-2o/2p under AL3, plus the AL3 channel) |
| H52 | 5.7 一般形式貢獻與 AI 特定部分 (L2397) (l.2397) | 評估保證與 AI 治理的語意、AI 特定的實證參數化，以及後續的企業應用（第 1.7.2 節）。 | 評估保證與 AI 治理的語意、AI 特定的實證參數化（V7，尚未執行），以及後續的企業應用（第 1.7.2 節）。 | V1.8.6 11 m3 (applied only at l.182); V1.8.6 06 status matrix row AI-specificity |

No other contradiction with the 06 matrix was found. Not edited on purpose: the P4/P7 formal statements (「在 C 中只有帳本對齊時才保證」) — they are P1–P8 formal statements (protected) and are already bounded by Prop D4/D5 at §3.12.4 and C.10.4; Appendix C.5/C.6 (verbatim v2.2; superseding notes already in C.10.2/C.10.4).

```
RD5_ITEMS_RESOLVED=14 patches over 7 listed locations (all RESOLVED)
SWEEP_FIXES=2 (H49, H52)
NEW_CLAIMS=0
NEW_CITATIONS=0
OVERCLAIM_REMAINING=0 (per 06 matrix)
THEORY_STATUS=PARTIAL
SUBMISSION_READY=NO
```
