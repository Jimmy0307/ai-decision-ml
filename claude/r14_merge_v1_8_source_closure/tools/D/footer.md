---

## 3. Overlap / contamination check against v1.7 (130, 3,080 lines) and 128

### 3.1 Zero-hit terms and numbers (no trace of legacy results)

In 130 **and** 128: `main path`, `主路徑`, `SPLC`, `SPNP`, `SPC`, `PCA`, `主成分`, `factor analysis`, `因素分析`, `varimax`, `Kaiser`,
`citation network`, `引用網路`, `citation edge`, `Monte Carlo`, `gap_priority`, `Tier-A`, `Tier-B`, `info_gap`, `2,003`, `1,981`, `98.90`,
`714` (as a token), `29.90`, `57.30`, `-0.1413`, `0.9734`, `0.6468`, `bridging`, `betweenness` — all **0 hits**.
Of 1,403 distinctive numeric tokens extracted from legacy text files, only the generic/coincidental ones in §3.3 appear in 130; **0** appear in 128.
None of the 27 legacy concept labels appears as an analysis object in 130 (only common English words inside reference titles, §3.3).

### 3.2 Term hits in 130 and their classification

| Term | 130 lines | What the hit is | Verdict |
|---|---|---|---|
| 結構洞 (29) / structural hole (4) / Burt (31) | 21, 37, 57, 83, 174, 186, 190, 196, 234, 236, 238, 240, 244, 270, 354, 579, 583, 641, 716, 1677, 1679, 1685, 2184, 2218, 2228, 2232, 2234, 2240, 2304, 2338, 2358, 2380, 2386; refs 2396, 2436, 2438, 2440, 2442, 2630, 2719, 2720; errata 3041, 3049, 3058 | v1.7's own theoretical framing (Burt 1992/2004; Ahuja 2000; Fleming et al. 2007): "functional under-integration ≠ Burt-type structural hole ≠ enterprise problem". Line 583 states Burt constraint was **not** applied to the function-family network; line 2240 (Table 5-1) marks Burt-type structural hole as "未檢驗"; line 2338 says no Burt algorithm was pre-specified. Some Burt hits are author-name substrings (Burton-Jones, 270/2358/2630/2719/2720/3041/3049). | LEGITIMATE — theory/boundary statements; no legacy number, corpus, concept or tier is imported. Not an improper merge. |
| 骨幹 / backbone (v1.7 lines 579, 1677, 1685, 2184, 2380) | — | v1.7's exploratory "operational integration skeleton" built from its 16 robust over-representations (10 cross-component / 6 within-component; 0–14 under alternative skeletons). Legacy "backbone" is a top-30 %-weight concept co-occurrence graph of 27 governance concepts. | Same word, different construct and data — LEGITIMATE, not a merge. |
| 制約 (583) / constraint (31, 381, 722) | 583: Burt constraint explicitly *not* used; 31: English abstract; 381, 722: enterprise-model "hard constraint" (incident tolerance ē). | Unrelated to legacy Burt-constraint correlation (rho = -0.1890). LEGITIMATE. |
| 約束 (51, 254, 284, 474, 484, 2204, 2912) | Relation label "constrain" in the R14 semantic coding scheme and governance prose. | Unrelated. LEGITIMATE. |
| OpenAlex (2668, 2684, 2750, 3054, 3056, 3059) | OpenAlex used only to reconstruct reference abstracts for quotation verification (Appendix B, errata E30/E32/E35). | Not the legacy OpenAlex external-validation result. LEGITIMATE. |
| Jaccard (640, 749, 1439, 1447, 1589, 1593, 1742, 1746) | Jaccard of robust-cell sets across null models / evidence-unit re-segmentation (e.g. .853 at 1593) and V1 secondary-mechanism Jaccard (pending). | Legacy Jaccard (tier stability 0.7452 etc.) absent. LEGITIMATE. |
| AI 治理 (282, 332, 940, 2682, 2684, 2734) | IT/AI governance literature review and expert-panel qualifications. | Topic overlap only; no legacy result. LEGITIMATE. |

### 3.3 Numeric-token hits in 130 (all coincidental)

| Token | 130 lines | Context in v1.7 | Legacy source | Verdict |
|---|---|---|---|---|
| `5,000` | 573, 749, 1336, 1443 | Number of retained null-model states / V1 bootstrap draws | Legacy `FINAL_CLOSEOUT_SUMMARY` (5,000 bootstrap of concept-network correlations) | Coincidental round number; different analysis. Not a merge. |
| `20,000` | 1561, 1573 | κ bootstrap resamples (R14 human audit) | Legacy formal thesis | Coincidental. |
| `1.000` | 1728 | κ = α = 1.000 (AI A vs AI B agreement, 16/16) | Legacy theses / info-gap | Coincidental. |
| `0.000` / `0.0000` | 1908, 2746 | MaxRegret vertex 0.0000; "P < 0.00001" in a Kawamoto quote | Legacy formal thesis | Coincidental. |
| `0.1186`, `10.6028`, `10.1016`, `0.125`, `10.125` | 2398–2652 | Fragments of DOIs in the reference list | Legacy formal thesis references | Coincidental (DOI substrings). |
| Accountability / Fairness / Ethics / Governance | 63, 2560, 2590, 2734, 2752 | Words inside reference titles / prose | Legacy concept list | Coincidental. |

### 3.4 Hits in 128_CANONICAL_STATE.md

| 128 line | Content | Verdict |
|---|---|---|
| 15 | `完整資料來源.zip` listed as **ABSENT** and described as "V5 Manuscript Data Pack 本體". | **CONFLICT (labeling, non-blocking):** the zip now present (`C:\NTUST_PAPER\read\generated_v2\完整資料來源.zip`, sha256 138dbeac…) is *not* a V5 data pack; it is the April–May 2026 legacy structural-hole / citation / PCA-FA package. 128 §3's V5 cross-check was done against R14 + `04_G01_G16_FROZEN.csv`, not this zip, so no canonical number depends on it. The 128 description of this zip should be corrected in the v1.8 canonical state; any "V5 Data Pack" provenance must be sought elsewhere (status of a true V5 data pack: NOT_RECOVERED from this zip). |
| 80 | "V4 稿件 … 與 V4 結構洞層（不得恢復）" listed as historical provenance only. | Consistent with this boundary (same structural-hole line; exact identity with V4 layer UNRESOLVED). |

### 3.5 Result

- Improper merges of legacy results into v1.7: **0**.
- Legitimate theory/boundary mentions of structural holes / Burt in v1.7: present (§3.2) and already framed as *not tested* by the thesis.
- Coincidental numeric collisions: 10 tokens, all explained (§3.3).
- v1.7 never names `完整資料來源`; 128 names it once (line 15) with a wrong description (§3.4).

---

## 4. Classification and boundary

Classification: **LEGACY_HISTORICAL_PROVENANCE** — an earlier, methodologically distinct study (2,003-paper AI-governance corpus; gap_priority structural-hole tiers; citation main path SPLC/SPNP; PCA/FA; OpenAlex external validation) that precedes the R14 corpus and the G01–G16 robust-depletion analysis. It may be cited only as project history (e.g. "an earlier structural-hole prototype was abandoned"), never as evidence.

Rules binding on v1.8 and later:

DO_NOT_OVERRIDE_R14
DO_NOT_OVERRIDE_V5
DO_NOT_OVERRIDE_G01_G16
DO_NOT_MERGE_STRUCTURAL_HOLE_RESULTS

Operational meaning:
- No number, table, figure, tier, concept ranking, main path, PCA/FA loading or validation statistic from this package may enter the manuscript, appendices, canonical state, or enterprise model.
- The legacy `FINAL_THESIS_*` drafts are not authoritative despite the "FINAL" name (audit protocol: name confers no authority).
- The legacy Burt-constraint / betweenness correlations must not be used to upgrade v1.7's "Burt-type structural hole = 未檢驗" status.
- Any future reference to this zip must cite sha256 `138dbeac661fb39a0ab7f3fe84f312e332a9d8b64b5b47c399034bffd4c0d283` and this boundary file.
- Required follow-up (outside this phase): correct 128 line 15's description of `完整資料來源.zip`.

LEGACY_ZIP_CLASSIFICATION=LEGACY_HISTORICAL_PROVENANCE
