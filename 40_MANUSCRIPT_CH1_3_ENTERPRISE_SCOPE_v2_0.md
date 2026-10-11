# 論文候選稿 v2.0｜企業級 AI 導入之緒論、文獻回顧與研究方法

**中文題名：企業人工智慧導入作為多層級決策系統：治理、能力配置、組織採用與價值實現**

**English title: Enterprise AI Adoption as a Multilevel Decision System: Governance, Capability Allocation, Organizational Adoption, and Value Realization**

**稿件狀態：研究設計階段。** 本稿不報告企業實證效果、ROI、樣本結果或已驗證的最適配置。既有大規模 AI × Decision 文獻語料與 G01–G16 網絡結果作為前階段 evidence foundation；本稿只把經過來源稽核的理論主張與 v2.0 enterprise architecture 接起來。任何未識別的企業參數均保留為 `UNIDENTIFIED` 或明示情境。

## 中文摘要（設計階段）

企業導入人工智慧已由單一工具採用逐漸轉向跨部門的能力配置、治理與資源協調問題。然而，模型能力提升或局部生產力改善並不能直接回答企業應如何分配共用 AI 能力、設定決策權與風險邊界，以及部門配置如何轉化為員工實際採用與組織價值。本研究將企業 AI 導入建構為多層級決策系統：企業層決定戰略、政策、共用基礎設施與資源配置；事業／功能單位在其約束下選擇 AI 權限、人工介入、工作流程整合與評估保證配置；不同角色的使用者再依可見訊號形成使用、查核、修改、升級、拒用或繞過等條件反應。研究以前階段 AI × Decision 大規模文獻網絡中的 G01–G16 結構性低連結議題為問題線索，將其轉譯為治理與決策權、流程與交接、人機工作安排、評估與保證四項候選組織機制。方法採嵌入式企業個案設計，結合文件、跨層級角色資料、可追溯的成本與結果查表，以及 Enterprise–Business Unit 雙層 portfolio model；第一線行為預設以角色別條件分布內嵌，只有在證據支持獨立裁量與不同目標時才擴充第三層。所有有序構念僅作同構念門檻或查表鍵，未識別輸入不得以零值或任意係數補齊。本研究預計檢驗企業治理、共享能力、部門異質需求與實際使用反應如何共同形成可行的 AI portfolio，並以 ROBUST、CONDITIONAL、FRAGILE 與 UNIDENTIFIED 報告配置對參數不確定性的敏感度。

**關鍵詞：** 企業人工智慧導入；多層級決策；AI 治理；能力配置；組織採用；人機協作；價值實現

## Abstract (design stage)

Enterprise artificial intelligence adoption is increasingly a cross-functional problem of capability allocation, governance, and resource coordination rather than the adoption of a single tool. Improvements in model capability or local productivity do not by themselves determine how an enterprise should allocate shared AI capabilities, define decision rights and risk boundaries, or convert local deployments into sustained organizational value. This study conceptualizes enterprise AI adoption as a multilevel decision system. At the enterprise level, executives determine strategy, policy, shared infrastructure, and resource allocation. Business units or functions select configurations of AI authority, human intervention, workflow integration, and evaluation and assurance under those constraints. Role-specific users then respond to visible signals through use, verification, modification, escalation, rejection, or bypass. The study uses G01–G16 structural low-connectivity findings from a prior large-scale AI × Decision literature network as research leads and translates them into four candidate organizational mechanisms: governance and decision rights, workflow and handoffs, human–AI work arrangements, and evaluation and assurance. The proposed method is an embedded enterprise case design combining documentary evidence, cross-level role data, traceable cost and outcome lookups, and an Enterprise–Business Unit bilevel portfolio model. Frontline behavior is represented by conditional role-specific response distributions unless evidence supports an independent third optimization level. Ordinal constructs are used only as within-construct thresholds or lookup keys, and unidentified inputs are not replaced with zeroes or arbitrary coefficients. The study is designed to evaluate how enterprise governance, shared capabilities, heterogeneous unit requirements, and actual user responses jointly shape feasible AI portfolios and to classify decisions as ROBUST, CONDITIONAL, FRAGILE, or UNIDENTIFIED under admissible parameter uncertainty.

**Keywords:** enterprise AI adoption; multilevel decision making; AI governance; capability allocation; organizational adoption; human–AI collaboration; value realization

# 壹、緒論

## 1.1 研究背景

人工智慧在企業中的角色已不再局限於單一模型或單一工作自動化。當生成式 AI、預測模型、搜尋與推薦能力逐漸進入不同功能單位，企業面對的核心問題轉變為：哪些能力應集中建置、哪些決策權應保留在企業或部門層、何種工作可以授權 AI、哪些情境必須保留人工控制，以及有限的工程、資料、運算與治理資源應如何在多個 AI initiative 之間配置。

這類問題不能只用「是否採用 AI」或模型準確率回答。同一套 AI capability 可能被多個部門共用，但各部門的資料條件、錯誤後果、工作流程、人工查核能力與價值來源不同；企業統一平台可能降低重複成本與治理複雜度，也可能與部門追求快速、彈性的局部配置產生張力。更重要的是，管理層設計的配置並不等於組織實際使用。員工可能採用、查核、修改、升級、拒用或繞過 AI，而這些行為會反過來改變實際成本、風險與績效。

因此，本研究把企業 AI 導入視為跨層級決策問題，而不是單一應用導入問題。企業層負責戰略、政策、共享資源與 portfolio；事業／功能單位在企業限制下形成局部 AI configuration；使用者行為則是配置能否轉化為實際結果的重要中介機制。此一層級化結構使企業 AI adoption 同時具有治理、資源配置、人機協作與價值實現的特徵。

## 1.2 前階段文獻研究與問題來源

本研究的 evidence foundation 來自前階段 AI × Decision 大規模文獻語料與網絡分析。G01–G16 表示 AI family 與 decision family 之間的結構性低連結 pair；它們是文獻結構所提出的 research leads，而不是企業中已被觀察到的十六項缺口，更不能直接用作模型權重或效用係數。

為避免由 bibliometric gap 直接跳到企業因果主張，本研究將這些 research leads 轉譯為四個可被組織資料反駁的機制：M1 治理與決策權、M2 工作流程與交接、M3 人機工作配置、M4 評估與保證。G04 保留在 evidence monitoring 層；涉及跨期學習與重新配置的議題只有在取得 longitudinal evidence 時才進入 M5。由此建立「文獻證據 → 組織機制 → 多層配置 → 行為反應 → 組織結果」的研究鏈。

## 1.3 研究缺口

既有研究已分別提供幾項重要觀點。Shrestha、Ben-Menahem 與 von Krogh（2019）指出，人與 AI 的組織決策可採不同的委託、順序或聚合結構，顯示 AI 導入的關鍵不只是模型能力，而是決策權與配置方式。Raisch 與 Krakowski（2021）指出 automation 與 augmentation 在管理實務中存在相互依賴，不能被簡化為永久互斥的兩種策略。Vaccaro、Almaatouq 與 Malone（2024）的 meta-analysis 顯示，人機組合並不保證優於人或 AI 單獨工作的較佳者，而且效果受到任務型態、相對能力與分工方式影響。Bansal 等人（2021）顯示解釋可能增加使用者接受 AI 建議的機率，包括錯誤建議，意味「提供 explanation」不能直接等同風險降低。Elish（2019）指出複雜自動化可能使控制能力有限者承擔不相稱責任。Jöhnk、Weißert 與 Wyrtki（2021）則將 organizational AI readiness 分為多類因素，顯示資料與技術能力不足以涵蓋完整企業準備度。

上述研究支持配置、治理、相對能力、使用行為與組織準備度的重要性，但它們並未共同提供一個可直接用於 enterprise-wide portfolio decision 的完整架構。特別是，仍需處理三個連接問題：第一，企業共享能力與政策如何約束多個 business units；第二，部門配置如何透過角色別行為轉化為實際結果；第三，共享成本、局部成本、風險與價值如何在同一可稽核架構中被比較而不重複計算或把 ordinal scales 當基數效用。

本研究因此不以特定部門或流程代表企業，而將企業、business unit / function、AI initiative / shared capability 與 role-specific users 建構為嵌套分析層級。

## 1.4 研究目的

本研究目的為：

1. 建立 enterprise-wide AI adoption 的多層決策架構，明確區分企業層治理／資源配置、部門層 AI configuration 與使用者層條件反應。
2. 將 G01–G16 文獻網絡線索轉譯為 M1–M4 組織機制，建立可追溯的 literature-to-mechanism evidence chain。
3. 建立可同時處理 shared capabilities、shared costs、local implementation、risk constraints 與 heterogeneous unit requirements 的 enterprise AI portfolio model。
4. 建立 observed、elicited、public、scenario、simulated 與 optimized data 的 provenance separation，避免由資料缺口產生虛構參數。
5. 檢驗企業層與部門層的目標／限制是否真的形成 multilevel conflict，而不是先由模型形式假定衝突存在。
6. 評估不同 configuration 在 admissible uncertainty 下的穩健性，形成 ROBUST、CONDITIONAL、FRAGILE、UNIDENTIFIED 的決策支援輸出。

## 1.5 研究問題

**RQ1：** 企業層級的 AI 戰略、治理、共享能力與資源配置如何影響不同事業／功能單位的 AI 導入選擇？

**RQ2：** 企業層設定的目標、政策與能力邊界，與各部門實際需求、配置及工作流程之間，在何種條件下形成一致、落差或衝突？

**RQ3：** 部門層級的 AI 權限、人工控制、工作流程整合與 assurance 配置，如何對應到不同角色的實際使用、查核、修改、升級、拒用與繞過行為？

**RQ4：** 在有限預算、共享 AI 能力、治理要求與異質部門需求下，企業應如何形成可行的 AI initiative portfolio 與資源配置？

**RQ5：** 哪些 enterprise AI configurations 在成本、績效、風險、可擴展性與組織採用之間形成較穩健的價值實現？

## 1.6 預期貢獻

本研究的第一項貢獻是把 enterprise AI adoption 從單一 adoption score 轉為多層 decision architecture。第二項貢獻是建立 literature-network gap 與 organizational mechanism 之間可稽核的中介層，避免 bibliometric depletion 被誤寫成企業事實。第三項貢獻是把 shared platform economics 與 local unit implementation 放進同一 portfolio model，避免企業級共享成本在部門模型中重複計算。第四項貢獻是將 role-specific user response 納入配置結果，而不先假設員工一定遵循管理設計。第五項貢獻是建立 missing-as-UNIDENTIFIED 與 sensitivity classification，使資料不足本身成為可報告的研究結果，而不是被任意係數掩蓋。

# 貳、文獻回顧與理論架構

## 2.1 AI 與組織決策配置

Shrestha 等人（2019）討論 AI 與人類在組織決策中的不同安排，包括人對 AI 的委託、兩種順序式決策以及聚合等結構。對本研究而言，其核心價值不是提供 A0–A3 等級，而是提醒配置必須記錄誰先形成判斷、誰有最終權限、是否聚合，以及 AI 是否被授權執行。本研究的 `A_aut` 是研究者為企業資料操作化所提出的 decision-right anchor，不等同原文分類。

在 enterprise scope 下，相同 AI capability 可能在不同 unit 被配置為不同 `m_j`。因此企業採用不是單一 binary adoption，而是多個 unit configurations 在共同 governance 与 resource constraints 下的 portfolio。

## 2.2 Automation–augmentation 與跨層導入

Raisch 與 Krakowski（2021）指出 automation 與 augmentation 並不能被整齊地永久分離。對企業而言，某一能力可能在一個步驟自動化，在另一個步驟增加人工判斷、協調或監督負擔。因此本研究不以「automation 比例」直接當成價值，而將 `A_aut`、`H`、`WI`、`EA` 與工作配置分開記錄。

此觀點也支持跨期擴充：一項 AI initiative 的實際結果可能改變下一期企業投資與 governance，但此 feedback 必須有 longitudinal data 才能進 M5，不能由靜態模型預設。

## 2.3 Human–AI performance 與角色反應

Vaccaro 等人（2024）對 106 項實驗與 370 個效果量的綜合分析指出，人機組合平均不必然優於人或 AI 單獨工作的較佳者，且 task type、relative performance 與 division of labor 具有異質性。此結果支持本研究不設定固定「AI adoption reward」，也不以外部平均效果量直接替代企業自身 outcome data。

Bansal 等人（2021）的研究顯示 explanations 可能提高使用者對 AI 建議的接受，包括錯誤建議。故本研究將 `EA-V`（validation / monitoring / revalidation）與 `EA-X`（explanation usability）分開；是否提供 explanation 與是否降低風險是兩個不同的 empirical questions。

使用者反應因此以 `ρ_j(r|x,z,role,s)` 表示，而不是假設管理者選定 configuration 後員工必然採用。真實 outcome `ω` 不在行動前提供給受訪者，以避免 perfect-information bias。

## 2.4 Governance、control 與 accountability

Elish（2019）的 moral crumple zone 分析指出，自動化環境中可能出現責任與實際控制能力不對稱。因此，本研究將 formal decision right `G`、nominal intervention right `H` 與 `H_effective` 分開。是否能在行動前取得足夠資訊、是否有時間、是否能真正否決或回復，都不能由「有人簽核」推定。

Enterprise scope 進一步要求把 enterprise policy 與 local control 分開。企業可能設定風險與禁止規則，但部門是否有能力執行該規則仍需觀察 workflow、data access 與 actual rights。

## 2.5 Organizational AI readiness 與 shared capability

Jöhnk 等人（2021）提出五類、十八項 organizational AI readiness factors，涵蓋策略、資源、知識、文化、資料等面向。本研究既有 `D/R/G/A/H/WI/EA` 是較窄的 decision-architecture constructs，不能宣稱完整覆蓋 organizational readiness。

因此 enterprise v2.0 將 strategy、change capability、knowledge/culture 等先作 context 或候選 construct，除非後續文獻與內容效度支持，不直接加入 objective function。其目的是保持模型可識別，而不是把所有 readiness 因素壓成一個 maturity score。

## 2.6 從 G01–G16 到 M1–M4

前階段文獻網絡的 G01–G16 只表示某些 AI-family × Decision-family 介面在文獻中相對低連結。本研究採以下 codebook：

- `M1 Governance & Decision Rights`：授權、否決、問責、政策邊界
- `M2 Workflow & Integration`：handoff、routing、exception、rollback
- `M3 Human–AI Work Configuration`：順序、delegation、augmentation、aggregation、override
- `M4 Evaluation & Assurance`：validation、monitoring、revalidation、auditability、explanation usability

G→M mapping 必須由至少兩位獨立編碼者在看不到研究者建議答案的情況下盲編，保留分歧與裁決。沒有 organizational mechanism 對應的 gap 留在 evidence layer，不強迫進模型。

## 2.7 Enterprise AI adoption 的整合架構

綜合上述文獻，本研究提出：

`Enterprise Governance & Shared Capability → Business-unit Configuration → Role-specific Response → Operational/Economic Outcomes → (future longitudinal feedback)`

其中企業與部門之間可能存在 resource allocation、policy fit 與 local optimization 的衝突；但該衝突是 empirical proposition，不由 bilevel mathematics 自動成立。

# 參、研究方法

## 3.1 研究設計

本研究採 embedded enterprise case design。企業為 primary case；business units / functions、AI initiatives / shared capabilities 為 embedded units；role-specific users 提供實際行為與控制證據。

研究不要求某一特定功能單位成為核心案例。選擇 embedded units 的目的在於取得異質的 governance、workflow、AI authority、risk consequence 與 value structures，以檢查 enterprise architecture 是否能跨單位成立。

## 3.2 資料來源

資料來源分為：

1. **Enterprise documents**：AI policy、information/data governance、decision rights、shared platform/infrastructure、budget/capacity boundaries 等可授權資料。
2. **Business-unit evidence**：initiative inventory、local workflow、local resource requirements、exception/rollback、implementation effort。
3. **Role-specific evidence**：實際可見訊號、使用／查核／修改／升級／拒用／繞過行為，以及名目權限與有效控制差異。
4. **Outcome/cost evidence**：工作量、時間、implementation/operation cost、quality/service proxies、risk events；必須明確期間與單位。
5. **Public/external evidence**：只作 context、benchmark 或 sensitivity bounds，不回填為 firm-specific effect。

所有資料均附 provenance 與 authorization scope。敏感原始資料、可識別個人資料及未授權公司資料不進公開 repository。

## 3.3 變數與操作化

核心 constructs：

- `D`：shared interoperability
- `R`：data/resource accessibility
- `G`：formal governance / decision rights
- `A_aut`：AI authority / autonomy
- `H`：human intervention right
- `WI`：workflow integration
- `EA-V`：evaluation / assurance
- `EA-X`：explanation usability candidate
- `κ`：consequence class

上述 ordinal levels 只在同一 construct 內做 requirement comparison 或 lookup key。企業共享能力與 unit-specific states 分表保存。

`Gap_X(j,s)=1[X_obs(j)<Req_X(A_target,j,s)]`

只表示方向性不一致；未識別值不計 gap，ordinal difference 不解讀為損失大小。

## 3.4 多層配置與使用者反應

企業層決策：

`b=(B,Γ,Infrastructure,SharedCapability,Priority)`

Business unit / initiative `j` 的配置：

`x_j=(A_aut,j,H_j,WI_j,EA-V_j,m_j)`

使用者層：

`ρ_j(r|x_j,z,role,s)`

其中 `r∈{Use,Verify,Modify,Escalate,Reject,Bypass}`。

預設只有 Enterprise–Business Unit 兩層 optimization。若後續證據顯示使用者有至少兩個具後果的可行動作、能自主偏離設計、具有不同 objective/constraints、管理者預期其反應，且反事實上會改變上游選擇，才加入第三層作模型比較。

## 3.5 Enterprise portfolio economics

對每個 initiative `j` 定義工作量 `N_j(T)`、value `V_j`、enterprise loss `L_j`、local controllable loss `L_oper,j`、operational cost `C_op,j`、local implementation cost `C_impl,j` 與 capacity `CapHours_j`。

企業共用成本 `C_shared(b,s)` 包含可被多個 initiatives 共用的 platform、infrastructure、security、governance、evaluation 或 training 成本。該成本在 enterprise level 計算一次，禁止逐部門重複扣除。

候選 enterprise objective：

`F_E(b,x;s)=Σ_j N_j(T)[E_j(V_j)-E_j(L_j)-E_j(C_op,j)]-C_shared(b,s)-Σ_j C_impl,j(x_j,b,s)`

Business-unit candidate objective：

`F_M,j(x_j|b,s)=-N_j(T)[E_j(L_oper,j)+E_j(C_op,j)]-C_impl,j(x_j,b,s)`

若 non-monetary rights、privacy、legal、security 或 quality boundaries 無法合理換算為 TWD，則以 constraints 表示。

## 3.6 Shared capability 與 portfolio coupling

多個 initiatives 可能共用：

- model/runtime/inference service
- data interface / retrieval layer
- access-control / audit layer
- evaluation infrastructure
- engineering / review capacity
- organizational training and support

因此可行集合不是每個部門獨立求解後簡單相加。Portfolio solver 必須同時處理 shared fixed cost、capacity competition、enterprise policy、reuse 與 sequence effects。跨期 sequence 與 learning 只在 M5 longitudinal extension 中建模。

## 3.7 Identification 與 missing-data rule

所有數值依來源分為 `OBSERVED`、`EXPERT_ELICITED`、`PUBLIC_OBSERVED`、`SCENARIO_SENSITIVITY`、`SIMULATED_ONLY` 或 `UNIDENTIFIED`。

禁止：

- 用舊 synthetic coefficient 填企業資料缺口
- 用 0 代替 missing
- 用 ordinal level 直接做 monetary arithmetic
- 用外部 productivity average 當本企業 effect
- 用單一部門 observation 推論 enterprise-wide effect
- 用模型形式存在推論真實 preference conflict

## 3.8 驗證流程 V0–V7

**V0 Source & Authority**：建立 enterprise policy、business-unit decision rights、shared capability、initiative boundary 與 authorization evidence。

**V1 Construct Validity**：跨治理、IT、management、functional users 做 content validity；G01–G16→M1–M4 至少雙人 blind coding。

**V2 Cross-functional Pilot**：在至少兩種不同功能脈絡測試題項理解、missingness、non-monotonicity、role disagreement 與 burden，而非固定兩個預選 use cases。

**V3 Schema & Units**：驗證 probability normalization、ordinal keys、one-hot、TWD/event、TWD/period、hours/period。

**V4 Lookup Completeness**：每個實際求解 cell 具有來源或 bounded interval；缺格停止 point optimization。

**V5 Portfolio Solver**：以 synthetic exhaustive oracle 驗證 multi-unit shared budget/capacity、ties、centralized vs bilevel 與 forbidden paths。

**V6 Sensitivity**：以 `Θ_adm` 掃描 admissible ranges，報 coverage 與 `ROBUST / CONDITIONAL / FRAGILE / UNIDENTIFIED`。

**V7 Enterprise Empirical Calibration**：企業層政策、部門配置、role-specific response 與 outcome/cost proxies 可以跨來源交叉核對。

## 3.9 分析程序

1. 重建 enterprise AI inventory 與 shared capability map。
2. 建立 governance / decision-right matrix。
3. 建立 business-unit / initiative configuration records。
4. 執行 G→M blind coding 與 construct content validation。
5. 進行 cross-functional pilot，修正 measurement contract。
6. 建立 traceable outcome/cost lookup 與 `Θ_adm`。
7. 執行 centralized planner 與 Enterprise–Business Unit bilevel portfolio 對照。
8. 報告 user-response sensitivity、shared resource bottlenecks 與 gap interfaces。
9. 對每個 portfolio recommendation 分類 robustness，而非只報單一 optimum。

## 3.10 研究界線

在 V7 完成前，本研究只能宣稱 enterprise research architecture、measurement specification 與 synthetic implementation validity；不能宣稱企業已達成特定 ROI、AI 已改善績效、某部門為最佳導入點、或本研究結果可直接外推至其他企業。

# 參考文獻（本稿目前實際使用）

Bansal, G., Wu, T., Zhou, J., Fok, R., Nushi, B., Kamar, E., Ribeiro, M. T., & Weld, D. S. (2021). Does the whole exceed its parts? The effect of AI explanations on complementary team performance. *Proceedings of CHI 2021*. https://doi.org/10.1145/3411764.3445717

Elish, M. C. (2019). Moral crumple zones: Cautionary tales in human-robot interaction. *Engaging Science, Technology, and Society, 5*, 40–60. https://doi.org/10.17351/ests2019.260

Jöhnk, J., Weißert, M., & Wyrtki, K. (2021). Ready or not, AI comes—An interview study of organizational AI readiness factors. *Business & Information Systems Engineering, 63*, 5–20. https://doi.org/10.1007/s12599-020-00676-7

Raisch, S., & Krakowski, S. (2021). Artificial intelligence and management: The automation–augmentation paradox. *Academy of Management Review, 46*(1), 192–210. https://doi.org/10.5465/amr.2018.0072

Shrestha, Y. R., Ben-Menahem, S. M., & von Krogh, G. (2019). Organizational decision-making structures in the age of artificial intelligence. *California Management Review*. https://doi.org/10.1177/0008125619862257

Vaccaro, M., Almaatouq, A., & Malone, T. (2024). When combinations of humans and AI are useful: A systematic review and meta-analysis. *Nature Human Behaviour, 8*, 2293–2303. https://doi.org/10.1038/s41562-024-02024-1

---

**Canonical note:** 本稿自 v2.0 起不以任何特定功能流程作為理論或實證研究的中心；後續新增案例只能作為 embedded unit evidence，不能重新縮窄 enterprise-wide research boundary。