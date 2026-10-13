# 14 — G07 / G15 Boundary-Sensitivity Audit (Cleanup Debt E)

- Round: V1.8.1 Study 1 evidence freeze. Sub-agent G. Date: 2026-10-14.
- Mode: read-only. G01–G16 membership, the 32-core baseline and all values were left unchanged.
- **STOP status: NOT TRIGGERED.** There is no G07/G15 evidence conflict and no G01–G16 membership conflict.
- Script: `tools/G/recompute_seg.py`. Output: `tools/G/recompute_seg_out.json`, which holds per-G values for all 16 gaps plus input sha256s. Membership-rule check: `tools/G/verify_membership_rule.py`.

## 0. Verdicts

| G | Pair | Verdict |
|---|---|---|
| **G07** | HUMAN_AUGMENTATION × EVALUATION_SELECTION (人機增能 × 評估與選擇) | **WORDING_CONFIRMED** |
| **G15** | EXPLANATION_ASSURANCE × EVALUATION_SELECTION (解釋與保證 × 評估與選擇) | **WORDING_CONFIRMED** |
| Other G (G01–G06, G08–G14, G16) | — | All 14 are retained in **both** S1 and S2. Nothing to flag. |

## 1. Pair mapping

| Source | G07 | G15 |
|---|---|---|
| REPO `11_Priority_Gaps_Frozen_Export_G01_G16_v1_0_20261009.csv` | HUMAN_AUGMENTATION, EVALUATION_SELECTION; k_a 166, k_d 128, M 2,180 | EXPLANATION_ASSURANCE, EVALUATION_SELECTION; k_a 279, k_d 128, M 2,180 |
| W `r14_merge_v1_7/132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX.csv` | same pair (match = True); "Evidence-unit persistence" = 邊界敏感 | same pair (match = True); 邊界敏感 |
| v1.8 Table 4-10 (L1658 / L1666) | 人機增能 × 評估與選擇 | 解釋與保證 × 評估與選擇 |

The 132 persistence tag is 邊界敏感 for exactly G07 and G15 and 持續 for the other 14. All 16 pairs match between the two files.

## 2. Baseline (official V9 primary; frozen core)

Values come from the V9 `ROBUST_CORE_LOCAL_SENSITIVITY.csv` `official_*` columns. I cross-checked them against the V9.1 baseline-reproduction rows (byte-identical to the official freeze) and against the frozen G01–G16 export. All three agree.

| G | Core | Direction | O (recounted from 2,180 edge rows) | E = k_a·k_d/M | O/E | q main | q exact | q doc-preserving | q raw-record |
|---|---|---|---|---|---|---|---|---|---|
| G07 | YES | DEPLETED | **2** | 9.7468 | 0.2052 | .01969 | .01472 | .03039 | .02900 |
| G15 | YES | DEPLETED | **7** | 16.3817 | 0.4273 | .02057 | .02318 | .03870 | .01471 |

## 3. V9.1 re-segmentation status (membership recomputed from rows)

The membership rule is: all four q ≤ .05 **and** one common direction. Applied to `S1_120_CELL_RESULTS.csv` and `S2_120_CELL_RESULTS.csv`, it gives core sizes of 32 (baseline), 31 (S1) and 31 (S2). The packaged `full_sensitivity_robust` flag disagrees with this rule in 0 cells.

| G | Setting | O (edges) | raw O | q main | q exact | q doc | q raw | Directions | Core | Methods with q > .05 |
|---|---|---|---|---|---|---|---|---|---|---|
| G07 | S1 句層級 | 1 | 1 | .02526 | .02598 | .02228 | **.05271** | all DEPLETED | **NO (drops)** | raw-record only |
| G07 | S2 句與子句層級 | 1 | 1 | .02529 | .02434 | .02666 | .04841 | all DEPLETED | **YES** | — |
| G15 | S1 句層級 | 6 | 7 | **.12425** | **.11549** | **.12376** | **.08127** | all DEPLETED | **NO (drops)** | all four |
| G15 | S2 句與子句層級 | 6 | 7 | **.12212** | **.11567** | **.14018** | **.08133** | all DEPLETED | **NO (drops)** | all four |

Why each drops:
- **G07** drops in S1 only. Its document-level count falls from 2 to 1. The raw-record q is .0527, just above .05, while the other three methods stay below .05. In S2 it is retained with the same O = 1 (raw q .0484). Its direction stays DEPLETED in every method and setting, so there is no reversal. This is a marginal threshold crossing on a very small count.
- **G15** drops in both settings. Its count falls from 7 to 6 and all four q values rise to .08–.14. Its direction stays DEPLETED everywhere, so there is no reversal.

**Other G:** G01–G06, G08–G14 and G16 are in the core in both S1 and S2. Only G07 (S1) and G15 (S1, S2) drop, which matches the manuscript's 14 persistent + 2 boundary-sensitive. The third boundary-sensitive core cell, RECOMMENDATION_OPTIMIZATION × EVALUATION_SELECTION, is enriched and therefore outside G01–G16. **No unreported G drop.**

## 4. Local label sidecar (targeted human-label substitution; V9 `ROBUST_CORE_LOCAL_SENSITIVITY.csv`, `sidecar_*` columns)

| G | sidecar O | Core | Direction | q main / exact / doc / raw | Membership changed |
|---|---|---|---|---|---|
| G07 | 2 | YES | DEPLETED | .01527 / .01463 / .04049 / .02750 | NO |
| G15 | 7 | YES | DEPLETED | .02666 / .02372 / .01777 / .01452 | NO |

All 16 G are still in the core under label substitution. This confirms the claim at v1.8 L15/L31/L2238 that 「目標式人工標籤替換未移除其中任何一組」.

## 5. Every v1.8 sentence describing G07/G15 as boundary-sensitive

Manuscript: `REPO/claude/r14_merge_v1_8_source_closure/08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md` (sha256 1515b0f2…).

**Definition (L629):** 「\| L2∖L3 證據單元邊界敏感 \| 屬 L2，但至少一種重切分設定未保留 \| 3（1／2） \| 保留於主要統計結果；逐格解讀採保守語氣 \|」. Under this definition, a single non-retaining setting is enough. G07 (S1 only) and G15 (S1 and S2) both meet it.

| Line | Text (abridged where long) | Check |
|---|---|---|
| L15 | 「16 個穩健不足呈現（G01–G16；其中 G07、G15 屬證據單元邊界敏感；目標式人工標籤替換未移除其中任何一組〔…〕）只作為研究線索…」 | ✓ |
| L31 | "The sixteen robust depletions (G01–G16; G07 and G15 are evidence-unit boundary-sensitive; none was removed by the targeted human-label substitution)…" | ✓ |
| L413 | 「→ 16 組主要穩健不足呈現 G01–G16（14 持續＋2 邊界敏感）」 | ✓ |
| L642 | 「3. **邊界敏感標記隨之傳遞。** G07 與 G15 在企業層的轉譯照常進行，但其文獻證據強度在討論中與 14 組持續配對分開陳述。」 | ✓ |
| L685 | 「\| I3 人機配置與反應 \| M3 \| G01（持續；anchor）、G07（**邊界敏感**） \| …」 | ✓ |
| L686 | 「\| I4 評估與保證 \| M4 \| G06（持續；anchor）、G05（企業層，持續）、G13（持續；EA-X 條件）、G15（**邊界敏感**；EA-X 條件） \| …」 | ✓ |
| L705 | 「\| G07 \| 人機增能 × 評估與選擇 \| 2／9.75；0.21；邊界敏感 \| …（O = 2，小計數，幅度不作解讀）…」 | ✓ (O, E and O/E match) |
| L713 | 「\| G15 \| 解釋與保證 × 評估與選擇 \| 7／16.38；0.43；邊界敏感 \| …」 | ✓ |
| L729 / L735 | "G07 ─┘ (G07: evidence-unit boundary-sensitive)" / "G15 ─┘ (G15: evidence-unit boundary-sensitive)" | ✓ |
| L757 | 「…反之，證據單元邊界敏感的 G07 與 G15，在 AI pilot 中與研究者的對應一致。…」 | ✓ (boundary-sensitivity part) |
| L1490 / L1498 (Table 4-4) | 「\| 7 \| 人機增能 \| 評估與選擇 \| 2 \| 9.75 \| 0.21 \| \* \| 邊界敏感 \|」 / 「\| 15 \| 解釋與保證 \| 評估與選擇 \| 7 \| 16.38 \| 0.43 \| \* \| 邊界敏感 \|」 | ✓ (main q .0197 / .0206 → one star) |
| L1605 | 「『解釋與保證 × 評估與選擇』與『推薦與最佳化 × 評估與選擇』在兩種重切分設定下都退出穩健集合；…另有『人機增能 × 評估與選擇』只在句層級設定退出…」 | ✓ (G15 drops in both, G07 in S1 only; matches the rows exactly) |
| L1658 / L1666 (Table 4-10) | 「\| G07 \| 人機增能 \| 評估與選擇 \| 2 \| 9.75 \| 0.21 \| \* \| **邊界敏感** \| M3／static core \| 一致 \|」 / 「\| G15 \| … \| 7 \| 16.38 \| 0.43 \| \* \| **邊界敏感** \| M4／static conditional（EA-X） \| 一致 \|」 | ✓ |
| L1671 | 「第一，16 組中 14 組在三種證據單元設定中皆持續，G07 與 G15 屬邊界敏感；兩者的決策端都是「評估與選擇」；…退出替代設定穩健集合的 3 組，決策端都是加權度數僅 128 的「評估與選擇」。…」 | ✓ (k_d = 128) |
| L1720 | 「…其中 G07（M3）與 G15（M4，EA-X 條件分支）屬證據單元邊界敏感（表 4-10）。」 | ✓ |
| L2185 | 「…G07、G15 屬證據單元邊界敏感。…」 | ✓ |
| L2210 | 「主要分析共有 16 組穩健不足呈現，其中 14 組在主要設定與兩種較細粒度證據單元設定中皆持續存在；「人機增能 × 評估與選擇」與「解釋與保證 × 評估與選擇」則屬證據單元邊界敏感。…」 | ✓ |
| L2238 | 「…16 組主要穩健不足呈現（14 持續、2 邊界敏感）；目標式人工標籤替換未移除其中任何一組…」 | ✓ |
| L2244 | 「一組不足呈現可能在證據單元重切分後失去穩健集合資格（G07、G15 的情形）；…」 | ✓ |
| L2278 | 「…第二，證據強度隨之傳遞：G07 與 G15 的轉譯照常進行，但 M3 的錨點 G01 與 M4 的錨點 G06 都跨證據單元持續，G15 所屬的 EA-X 子面向也另有持續的 G13…」 | ✓ (G01, G06 and G13 are retained in S1 and S2) |

No v1.8 sentence overstates the G07/G15 status. None says G07 drops in both settings, none implies a direction reversal, and none says either gap is removed from G01–G16. **No weakening is required.**

Optional precision (not required): if a later version wants to say *why* G07 is boundary-sensitive, this sentence could be added next to L1605 in Traditional Chinese: 「人機增能 × 評估與選擇在句層級設定中觀察值由 2 降為 1，僅未去重原始記錄分析之 p_BH（.053）略高於 .05；其餘三套檢定仍達 .05 且方向不變。」 The numbers come from the rows in §3 of this report. Adding the sentence does not change any membership.

## 6. Status of the attribution of these values

The S1/S2 status in this report comes from the V9.1 sidecar (2026-10-03), measured against the frozen V9 primary baseline. R14 reports the same values. See `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md`; the recommended provenance tag applies to v1.8 L1605 and Table 4-9 in the same way.
