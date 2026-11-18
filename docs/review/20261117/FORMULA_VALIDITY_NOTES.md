# FORMULA_VALIDITY_NOTES｜8 組公式與 12 篇文獻描述的效度註記（2026-11-18）

> 範圍：`docs/THEORY_LITERATURE_COMPARISON_20261117.{md,html}` 與 `docs/data/LITERATURE_METHODS_20261117.csv`。下文引用的行號指 **更正前** 版本（commit `cba0f3c`）。
> 原則：只有實際讀到的來源才算核對；未取得原文者標 `SOURCE_TEXT_NOT_ACCESSED`／`UNVERIFIED_SOURCE_TEXT`，並改以標準教科書形式或開源實作文件（igraph、networkx、R `sna`）判斷，且明確標示。

## 本 PR 已套用的更正（摘要）

| ID | 公式／描述 | 判定 | 已套用的更正 | 原文取得狀態 |
|---|---|---|---|---|
| E1 | O/E + BH–FDR | MATCH（本研究自定統計量） | 無 | n/a |
| E2 | Burt constraint | CORRECTION_NEEDED（p 定義） | 補 `p_ij=(z_ij+z_ji)/Σ_k(z_ik+z_ki)`、`q≠i,j`、p_qj 以 q 自身總量正規化；O_j 標為未核對 | Burt 1992 未取得 |
| E3 | Effective size | MATCH | 標明 `k−2t/k` 為 Borgatti（1997）無向無權簡化，並附 Burt 一般式 | Borgatti 1997 未直接讀（依 networkx 文件） |
| E4 | Betweenness | CORRECTION_NEEDED | 無序配對 `s<t; s,t≠v`、標準化 `(n−1)(n−2)/2`、去除 `s→t` 有向暗示 | Freeman 1977 未取得（教科書形式） |
| E5 | Gould–Fernandez | CORRECTION_NEEDED | 加 `¬(s→t)` 開放二步路徑與相異條件；角色定義明列；原 GF 為**無權**計數 | GF 1989 未取得（sna 文件＋Zádor et al. 2022 全文） |
| E6 | 二分圖 constraint | MATCH（附但書） | 限定 `j∈N(i)`、「i 的各邊等權」 | n/a（代數） |
| E7 | 骨架敏感度 | MATCH（本研究計數） | 無；數值由 `results.json` 與測試重跑確認 | n/a |
| E8 | Limitation 框架 | MATCH（流程） | 無 | n/a |
| R05 | Newman 描述 | 歸屬修正 | 「coauthor 邊≠知識流動」改標為本研究解讀限制 | 未取得 |
| R09 | Everett & Borgatti 描述 | 無法核對 | 加註 UNVERIFIED_SOURCE_TEXT | 未取得 |
| R10 | Saglietto et al. | 類別修正 | 「系統性方法回顧」→「結構洞測量議題回顧」 | 僅摘要 |
| R12 | Johnson & Sasson | 措辭修正 | 依官方摘要改寫；定位為 constraint 測量研究，非否證理論 | 僅摘要 |

**未改動**：Opsahl（R07）、Jasny–Lubell（R08）、Zádor et al.（R11）的描述與作者草稿／全文一致；首頁新增表格中的 R07／R08／R11 定義依下列原文摘錄撰寫。

---

## 逐項核對紀錄（審稿代理原始紀錄，路徑已改為 repo 相對路徑）


Checked 2026-11-18 (UTC). Repo files checked (read only, not edited):

- `docs/THEORY_LITERATURE_COMPARISON_20261117.md` (MD, line numbers below)
- `docs/THEORY_LITERATURE_COMPARISON_20261117.html`: all body content sits on **line 3** of this minified file. Its formula text is identical to the MD.
- `docs/data/LITERATURE_METHODS_20261117.csv`: rows R01–R12 are on lines 2–13.

## What I actually read

| Source | Status |
|---|---|
| Zádor et al. 2022, PLOS ONE (R11) | **Full text read** (PLOS JATS XML) |
| Opsahl (R07) | **Author preprint read** (arXiv 1006.0887, "Draft date: May 6, 2011"). This is not the version of record. |
| Jasny & Lubell (R08) | **Author last draft read** (Univ. of Exeter figshare 29710082). This is not the version of record. |
| Johnson & Sasson 2026 (R12) | **Abstract only** (Crossref and OpenAlex). Full text not accessed: INFORMS returned 403. |
| Saglietto et al. 2020 (R10) | **Abstract only** (Crossref) |
| Burt 1992, Burt 2004, Freeman 1977, Gould & Fernandez 1989, Everett & Borgatti 2020, Newman 2001, Granovetter 1973 | **SOURCE_TEXT_NOT_ACCESSED**. JSTOR returned a bot challenge; Elsevier, Wiley and UChicago returned 403. |
| Authoritative open documentation | networkx `structuralholes.py` and `betweenness.py` docstrings (GitHub main); igraph R `constraint` doc; R `sna::brokerage` Rd (CRAN mirror) |

Where the original was not accessed, the judgment below compares the repo with the standard textbook or software-documentation form. Those judgments are labelled as such.

---

## E1. O/E depletion ratio (project's own statistic)

- **Repo text** (MD line 41, explanation line 44; HTML line 3): `R_ab = O_ab / E_null[O_ab]；並對 empirical p-values 施行 BH–FDR`
- **Standard definition:** this is an observed/expected ratio under a project-defined null model. BH–FDR is the Benjamini–Hochberg step-up procedure. No R01–R12 reference defines it, so no literature claim needs checking.
- **Verdict: MATCH** as a project-defined statistic; it is internally consistent.
- **Suggested addition** (precision, not an error): `E_null[O_ab] 為所指定零模型（須寫明保留之邊際／約束）下之期望值；p 值為單尾（depletion）經驗 p 值，BH–FDR 施於 120 個配對檢定族。`

## E2. Burt network constraint

- **Repo text** (MD line 51, explanation line 54; HTML line 3):
  `C_i = Σ_{j∈N(i)} (p_ij + Σ_{q∈N(i),q≠j} p_iq·p_qj)²`. Explanation: `p_ij 為 i 在 j 上的關係投入比例；直接依賴與鄰居間接冗餘均計入。亦有版本另乘 O_j，須固定版本。`
- **Standard definition** (igraph doc and networkx doc, both read):
  - C_i = Σ_{j∈V_i, j≠i} (p_ij + Σ_{q∈V_i, q≠i,j} p_iq p_qj)².
  - p_ij = (a_ij + a_ji) / Σ_{k∈N(i)} (a_ik + a_ki), the normalised mutual tie strength.
  - p_qj is normalised by **q's** own tie total, not by i's.
  - networkx defines local constraint ℓ(u,v) = (p_uv + Σ_w p_uw p_wv)² and sums it over neighbours.
- **Verdict: MATCH on structure** (the squared term is present and the index ranges are equivalent). **CORRECTION_NEEDED on the p definition.** "i 在 j 上的關係投入比例" leaves out two things: the mutual (in+out) weighting, and the fact that p_qj uses q's own denominator.
- **O_j factor:** SOURCE_TEXT_NOT_ACCESSED (Burt 1992 not read). Neither igraph nor networkx includes O_j. The repo's "亦有版本另乘 O_j" cannot be confirmed from what I read.
- **Proposed wording:**
  `p_ij = (z_ij + z_ji) / Σ_{k∈N(i)} (z_ik + z_ki)：i 對 j 的（雙向合計）關係投入占 i 全部關係投入的比例；p_qj 以 q 自身的關係總量正規化。j 取 i 的直接接觸者。（Burt 1992 原書另有含 O_j 的寫法——原文未核對，引用前須查原書頁碼；igraph／networkx 實作均不含 O_j。）`

## E3. Effective size and efficiency

- **Repo text** (MD line 61, explanation line 64; HTML line 3): `ES_i = k_i − 2t_i/k_i；Efficiency_i = ES_i/k_i`. Explanation: `適用於無向、無權簡單 ego 網路；k_i 是鄰居數，t_i 是鄰居彼此間的邊數；權重/方向網路不可直接套用。`
- **Standard definition** (networkx doc, read):
  - Burt's general form: e(u) = Σ_{v∈N(u)} (1 − Σ_w p_uw m_vw).
  - For unweighted, undirected graphs, Borgatti (1997) proposed the simplification e(u) = n − 2t/n, where t counts ties among alters (excluding ties to ego).
  - Efficiency = effective size / degree.
- **Verdict: MATCH.** The repo correctly restricts the formula to undirected, unweighted, simple ego networks. The one gap is attribution: k − 2t/k is Borgatti's (1997) simplification, not Burt's general formula.
- **Proposed wording:** `ES_i = k_i − 2t_i/k_i（Borgatti 1997 對無向、無權二元 ego 網路之簡化式；Burt 一般式為 ES_i = Σ_j [1 − Σ_{q≠i,j} p_iq m_jq]）；Efficiency_i = ES_i/k_i。` (Borgatti 1997 itself was not read; the attribution comes from the networkx documentation.)

## E4. Betweenness centrality (Freeman 1977)

- **Repo text** (MD line 71, explanation line 74; HTML line 3): `B(v) = Σ_{s≠v≠t} σ_st(v) / σ_st`. Explanation: `σ_st 為 s→t 最短路徑數，σ_st(v) 為經過 v 的數量`.
- **Source access:** SOURCE_TEXT_NOT_ACCESSED for Freeman 1977 (JSTOR blocked). Judged against the standard textbook form and networkx doc, labelled as such. In the standard form:
  - Freeman's measure is defined for undirected graphs as C_B(v) = Σ_{s<t; s,t≠v} σ_st(v)/σ_st, summed over **unordered** pairs.
  - The normalised version divides by the number of pairs, (n−1)(n−2)/2 for undirected graphs.
  - networkx documents an explicit normalisation factor P that depends on directedness.
- **Verdict: CORRECTION_NEEDED (minor; textbook-form judgment):**
  1. `s≠v≠t` does not exclude s = t. It should read s ≠ t, s ≠ v, t ≠ v.
  2. In an undirected graph, summing over ordered pairs doubles Freeman's score. State unordered pairs (s<t) for undirected graphs, or ordered pairs for directed graphs.
  3. No normalisation is stated, so scores are not comparable across networks of different size.
  4. "s→t" implies directed paths. Freeman's 1977 measure is for undirected graphs; directed use needs the directed variant.
- **Proposed wording:** `B(v) = Σ_{s<t; s,t≠v} σ_st(v)/σ_st（無向圖，無序配對；有向圖則對有序配對求和）；標準化：B'(v) = B(v) / [(n−1)(n−2)/2]（無向）。σ_st 為 s 與 t 之間最短路徑數。`

## E5. Gould–Fernandez brokerage roles

- **Repo text** (MD line 81, explanation line 84; HTML line 3): `GF_r(v) = Σ_{s,t} 1[(s→v)∧(v→t)] × I_r(g_s,g_v,g_t)`. Explanation: `依三人群體身分 r 區分 coordinator、gatekeeper、representative、consultant/itinerant、liaison；這是教學示意，非原論文加權精確式。`
- **Definition read** (sna::brokerage documentation; Zádor et al. 2022 section on GF; GF 1989 itself SOURCE_TEXT_NOT_ACCESSED):
  - "vertex v is a broker for distinct vertices a and b iff a→v→b and a ↛ b".
  - Roles, by group membership of the two-path A→B→C:
    - coordinator: A→A→A
    - itinerant: A→B→A
    - gatekeeper: A→B→B
    - representative: A→A→B
    - liaison: A→B→C
  - The score is the count of ordered pairs brokered.
  - Zádor et al. call the itinerant role "itinerant (or cosmopolitan)".
- **Verdict: CORRECTION_NEEDED:**
  1. **Missing open-triad condition** ¬(s→t). Without it the formula counts closed (transitive) two-paths, which GF do not count as brokerage.
  2. Missing distinctness s ≠ t, s,t ≠ v.
  3. "非原論文加權精確式" is misleading. The original GF measure is an **unweighted** count; the weighted version is Zádor et al. (2022).
  4. The label "consultant" did not appear in any source I read. sna uses "itinerant broker" and Zádor et al. use "itinerant (or cosmopolitan)".
- **Proposed wording:** `GF_r(v) = Σ_{s≠t; s,t≠v} 1[(s→v) ∧ (v→t) ∧ ¬(s→t)] × I_r(g_s,g_v,g_t)。coordinator: g_s=g_v=g_t；itinerant（cosmopolitan）: g_s=g_t≠g_v；gatekeeper: g_s≠g_v=g_t；representative: g_s=g_v≠g_t；liaison: g_s,g_v,g_t 互異。原 GF 為無權計數（另有隨機分組下的期望值與 z 檢定）；加權正規化版本見 Zádor et al. (2022)。`

## E6. Constraint in a strict bipartite graph (project algebra)

- **Repo text** (MD line 91, explanation line 94; HTML line 3): `若 q,j 同屬一側且不存在 q—j 邊：p_qj=0 ⇒ C_i=Σ_j p_ij²；若每邊等權 ⇒ C_i=1/k_i`
- **Check:** this holds under the standard form above. In a simple bipartite graph, every q ∈ N(i) lies on the same side as j ∈ N(i), so p_qj = 0 and C_i = Σ_j p_ij². With equal tie weights, p_ij = 1/k_i, so C_i = k_i·(1/k_i)² = 1/k_i.
- **Corroboration** (Opsahl preprint, read): "both the local clustering coefficient and constraint (structural holes) are inversely associated to nodes' two-mode degree."
- **Verdict: MATCH, with one caveat to state.** The result requires j to range over i's direct contacts only, as in the igraph and networkx definitions. If j were allowed to include i's two-step contacts, the indirect term Σ_q p_iq p_qj would be non-zero in a bipartite graph. In addition, "若每邊等權" should read "若 i 的各邊等權".
- **Proposed wording:** `二分圖中 i 的所有鄰居 q, j 同屬另一側、彼此不相連，故 p_qj=0 ⇒ C_i=Σ_{j∈N(i)} p_ij²；若 i 的各邊等權 ⇒ C_i=1/k_i（j 限 i 的直接接觸者，與 igraph／networkx 定義一致）。`

## E7 / E8 (project-internal counts and workflow)

- MD lines 101 and 111. These are not literature formulas, so there is nothing to check against a source. **Verdict: MATCH** (no external claim).

## R07. Opsahl two-mode clustering (no formula in repo, only a descriptive claim)

- **Repo text** (MD line 27; CSV line 8; HTML line 3): `單模投影會創造人造閉合；二模網路的 clustering 必須按原始模式重定義`
- **Original definition** (preprint, read; published version not accessed):
  - Global coefficient: C* = (number of closed 4-paths) / (number of 4-paths). A 4-path is closed when it is part of at least one 6-cycle, which Opsahl also describes as the first and last primary nodes sharing a secondary node not on the path.
  - Local coefficient: the same ratio, restricted to 4-paths centred on node i.
  - Opsahl notes that projection creates 2-paths that do not come from 4-paths, from multiple nodes sharing one secondary node.
- **Verdict: MATCH** for the descriptive claim. The repo gives no formula. If one is added, it must be based on 4-paths and closed 4-paths (6-cycles), **not** on triangles in the projection.
- **Proposed addition:** `C* = τ*_closed / τ*，τ* 為二模網路中的 4-path（三個主節點經兩個次節點相連）數，τ*_closed 為其中屬於至少一個 6-cycle 者；非以投影網路之三角形計算。`

## R08. Jasny & Lubell two-mode brokerage (descriptive)

- **Repo text** (MD line 28; CSV line 9): `使用含四條邊的二模 brokerage chains 與群體異質性，避免僅投影後計算 brokerage`
- **Original definition** (last draft, read): "A two-mode brokerage chain occurs whenever two institutions are separated by a shortest path containing three intervening nodes (two organizations and the brokering institution) and thus four ties." Chains in which the two end institutions are connected by a path of length 2 are excluded. The ties are undirected, so representative and gatekeeper are collapsed into one category. Chains are ordered by a heterogeneity (Simpson/Herfindahl-type) index across both modes.
- **Verdict: MATCH.**
- **Suggested precision:** `brokerage chain＝兩個機構之間最短路徑長度恰為 4（經兩個組織與一個中介機構）；無向，故 representative 與 gatekeeper 合併。`

## R11. Weighted and normalised GF, WNGF (descriptive)

- **Repo text** (MD line 31; CSV line 12): `保留邊權並正規化跨群體 brokerage，減少任意二值化造成的資訊損失`
- **Original definition** (full text, read):
  - Node r brokers q→s if 1/Z_qr + 1/Z_rs < 1/Z_qs, with Z_qs = 0 when there is no edge.
  - Normalisation: p_r^i = c_r^i / n_b^i, set to 0 when n_b^i = 0, where n_b^i is the role-specific upper bound.
  - Note: the published XML for Eq. (1) renders the right-hand side as Z_qs, while the prose says "inverse of the flow". If the formula is quoted, follow the prose and flag the inconsistency.
  - The authors also state that in a complete weighted graph, WNGF brokerage "is not linked to bridging structural holes".
- **Verdict: MATCH** for the descriptive claim.

## R12. Johnson & Sasson (2026): framing

- **Repo text:**
  - MD line 32 / CSV line 13: `經典 constraint 在實證上可能主要反映二元替代、集中度和度數，而非三元關係冗餘`, category `最新方法學批判`
  - MD line 127: `Everett–Borgatti／Johnson–Sasson | Constraint 分解、direct vs indirect contributions、程度控制 … 只證明測量界線`
  - MD line 134: `不可說：… 本研究已證明 constraint 失效`
- **Does the repo say the paper falsifies structural-hole theory?** **No.** The repo frames it as a methodological critique of the constraint measure, which is the right framing.
- **Original** (abstract only; full text SOURCE_TEXT_NOT_ACCESSED): "empirical research using constraint does not reliably support structural holes theory but does support simpler insights related to available alternatives, exchange partner diversity, and concentration … network constraint almost exclusively operationalizes dyadic constructs and not the broader structural network constructs with which constraint is associated."
- **Verdict: CORRECTION_NEEDED (wording):**
  - "度數" (degree) does not appear in the abstract and cannot be confirmed without the full text.
  - "exchange partner diversity" is missing from the repo summary.
  - "三元關係冗餘" is narrower than "broader structural network constructs".
  - The "direct vs indirect contributions" and degree-control decomposition in line 127 cannot be confirmed for either paper from what I read: J&S abstract only, and Everett & Borgatti not accessed.
- **Proposed wording:** `Johnson & Sasson (2026) 以形式、計算與實證方法指出：network constraint 幾乎只操作化二元（dyadic）構念，而非其常被賦予的更廣泛網路結構構念；因此以 constraint 為測量的既有實證結果並不能可靠支持結構洞理論，但支持關於可用替代對象、交換夥伴多樣性與集中度的較簡單論點。這是關於 constraint 測量內涵的研究，並非否證結構洞理論本身。`

## Other descriptive claims (not formulas)

- **R09 Everett & Borgatti** (MD line 29): "constraint 易受度數與 ego ties 影響，並非簡單的 0–1…". SOURCE_TEXT_NOT_ACCESSED (Elsevier 403; abstract not in Crossref or OpenAlex). Unverified.
- **R10 Saglietto et al.** (MD line 30): consistent with the abstract, which proposes "a guide to using existing measures of structural holes according to the type (simple or complex) of network". MATCH, based on the abstract.
- **R05 Newman** (MD line 25): "coauthor 邊並不等於知識流動的直接證據" is the project's own interpretive caveat, not something I could attribute to Newman 2001 (text not accessed). Phrase it as the project's caveat rather than Newman's claim.
