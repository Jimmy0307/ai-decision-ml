# G01–G16 收斂與構念凍結 v2.1（Frozen Gap-to-Mechanism Map v2.1 candidate）

**狀態：v2.1 candidate freeze，2026-10-10。** 本檔取代 `26_GAP_CONSTRUCT_TRACE_AND_ANCHORS_CANDIDATE_v1_3.md` 的 G→M 對應表，以及 handoff bundle `03_GAP_TO_MECHANISM_CANDIDATE.md` 的候選對應。輸入來源依優先序為：handoff bundle `CLAUDE_ENTERPRISE_AI_V2_1_HANDOFF`（01–07）＞ repo 38–40 ＞ 26/29/30。

**本檔凍結的是「研究者裁決的理論對應與模型位置」，不是已完成的獨立編碼效度。** V1（至少兩位盲編者、逐格一致與裁決）仍為 OPEN；若盲編否決某一對應，依 §7 的回退規則處理，不改寫網絡統計。

---

## 0. 讀法與鐵律

1. G01–G16 是 V5 文獻網絡（10 AI families × 12 Decision families = 120 cells；document-level edges M = 2,180）中，經 global fixed-degree null、exact hypergeometric、document-preserving null 與 raw-record sensitivity 四重檢定皆 q ≤ .05 且方向一致的 **16 個 robust depletion cells**（32 個 robust core 中的 16 個 depletion；另 16 個為 enrichment，不在本檔處理範圍）。
2. Depletion 的唯一語義是：**在指定 null 結構與觀察邊際下，該 AI-family × Decision-family pairing 在文獻中相對低度出現。** 它不表示企業中存在該問題、該功能無效、兩者不相容，或該介面不重要。
3. O/E、q 值、observed count 只用於 `Network_Evidence` 欄，**不進入任何目標函數、權重、門檻或先驗**。
4. 收斂的判準不是「每個 gap 都要有變數」，而是：**一個 gap 是否指向一個企業必須做出的配置決策（enterprise decision interface）**。若指向同一介面，就合併；若無介面，就留在 evidence layer。
5. Corpus-parity 限制（AI 側證據大量來自 abstract-level，Decision 側主要為 full text）使 depletion 的「幅度」解讀必須保守；本檔只使用其「方向」作為研究線索。

---

## 1. 收斂方法

每一 gap 依序回答四個問題：

| 步驟 | 問題 | 輸出 |
|---|---|---|
| S1 理論問題 | 文獻低連結代表哪一個「AI 輸出 → 組織行動」之間缺乏研究的連接？ | `Theoretical_Problem` |
| S2 企業介面 | 在企業中，誰在哪一層、對什麼做出決定時會碰到這個連接？ | `Enterprise_Interface`（I1–I5） |
| S3 可觀察狀態 | 企業內可被文件、記錄或角色資料觀察的是什麼？ | `Observable_State` |
| S4 模型位置 | 它成為決策變數、可行性限制、期望結果查表、成本項，或不進模型？ | `Decision_Variable`、`Constraint_or_Objective` |

S2 的企業介面以 Decision-family 所代表的「組織決策節點」為主，AI-family 為輔。理由：本研究的對象是企業如何把 AI 輸出接到組織決策上；同一決策節點上的不同 AI 能力，在企業層面面對的是同一組配置選擇。

收斂後的五個企業介面：

| 介面 | 企業必須決定的問題 | 機制 |
|---|---|---|
| **I1 Authority-to-act** | 誰可以讓 AI 的風險估計、建議或執行結果成為行動；誰能否決、停止、變更授權；誰承擔責任 | M1 |
| **I2 Routing & recovery** | AI 輸出如何被送進下一個決策／行動節點；例外與失敗如何被接住、回復 | M2 |
| **I3 Human–AI configuration & response** | 人與 AI 的順序、最終權與聚合方式；使用者實際如何反應 | M3 |
| **I4 Assurance** | 什麼驗證、監控、重驗證與可用解釋證據，是某一授權深度的前提；企業層的配置決策本身如何被保證 | M4 |
| **I5 Learning & reallocation** | 跨期結果如何改變下一期的配置與資訊取得 | M5（dynamic only） |

---

## 2. 16-gap Convergence Matrix

欄位定義：`Network_Evidence` = Observed / analytic E（= k_a·k_d/M）/ O/E；四個 q 依序為 primary BH、exact、document-preserving、raw-record。全部 16 格四檢定皆 DEPLETED 且 q ≤ .05（來源：`02_G01_G16_FROZEN.csv`，Export 2026-10-09）。

| Gap | AI_Family | Decision_Family | Network_Evidence | Theoretical_Problem | Primary_Mechanism | Secondary_Mechanism | Enterprise_Interface | Observable_State | Decision_Variable | Constraint_or_Objective | Static/Dynamic/Evidence-only | Keep/Merge/Exclude | Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G01 | HUMAN_AUGMENTATION | PREDICTION_DIAGNOSIS | O=3; E=25.89; O/E=.116; q=.0009/<.0001/.0024/<.0001 | 增強人判斷的 AI 很少被研究用於預測／診斷決策；人機在預測任務上的分工與相對表現缺乏連接 | M3 | M4 | I3 | 每個 initiative 的決策順序、最終權、是否聚合；角色別使用／查核／修改／拒用的實際頻率 | `m_k`（配置型態）；`A_k` | 進入期望結果 `E_jk[·]`（透過 `ρ,P,π`）；`Cons(A,m)` 可行性 | Static core | **Keep（I3 anchor）** | 是 M3 最直接的文獻表現；人機組合不必然優於較佳單方（S3），故結果必須查表而非假設 |
| G02 | PREDICTION_RISK_ESTIMATION | HUMAN_REVIEW_ACCOUNTABILITY | O=6; E=44.93; O/E=.134; q=.0009/<.0001/.0024/<.0001 | AI 風險估計與人工審查／問責之間缺乏連接：誰審、何時審、誰負責 | M1 | M3 | I1（Level 2 表現） | 部門層對特定 initiative 的審查責任人、可否在行動前否決、有效控制（資訊／時間） | `H_k`；`Eff_H(j,k)` | `H_k ≥ H_req^γ(A_k,κ_j)`；`Eff_H=1` 若 `H_req≥2` | Static core | **Merge → I1** | 與 G09 為同一授權介面的部門層表現（G09 為企業層）；不另立構念 |
| G03 | COORDINATION_EXECUTION | RISK_ASSESSMENT | O=3; E=16.78; O/E=.179; q=.0009/.0002/.0024/<.0001 | AI 協調／執行能力與風險評估之間缺乏連接：被執行的流程如何承接風險、例外與回復 | M2 | M1 | I2 | AI 輸出路由深度；例外路由；rollback 是否存在；整合工時 | `WI_k`；`FB_jk` | `WI_k ≥ WI_req^γ(A_k,κ_j)`；`FB_jk=1` 若 `A_k≥2`；成本 `C^impl`、容量 `K^ENG` | Static core | **Keep（I2 anchor）** | 是 M2 最直接的文獻表現；執行深度上升時的回復與例外處理是企業必須設計的限制 |
| G04 | GENERATION_SYNTHESIS | PREDICTION_DIAGNOSIS | O=7; E=38.21; O/E=.183; q=.0009/<.0001/.0042/<.0001 | 生成式 AI 用於預測／診斷的研究相對稀少 | — | — | 無獨立介面 | 無（企業中若有 GenAI 診斷 initiative，其配置問題已由 I1–I4 處理） | 無 | 無 | **Evidence-only** | **Exclude（from model）** | 此 pair 描述的是技術應用前沿，不是組織配置決策；若建模只會重複 I1–I4 的變數。保留為文獻監測與 Discussion 素材 |
| G05 | EXPLANATION_ASSURANCE | ALLOCATION_PLANNING | O=7; E=37.63; O/E=.186; q=.0009/<.0001/.0024/<.0001 | 解釋／保證能力很少被連到資源配置與規劃決策 | M4 | M1 | I4（**Level 1 表現**） | 企業是否有共用評估基礎設施；配置決策是否附 provenance 與穩健性等級 | `y_EVAL`（共享評估能力）；企業輸出要求 | `y_EVAL ∈ Pre(j,k)` 若 `EA_k ≥ EA^cap`（即 (F4) 前提）；求解輸出必須附 provenance 與 robustness class | Static bridge | **Merge → I4** | 在企業層，「配置決策」就是 portfolio allocation；其保證要求以 (i) 共享評估能力前提、(ii) 模型輸出的可稽核性呈現，不另設 EA-X 權重 |
| G06 | EVALUATION_ASSESSMENT | PREDICTION_DIAGNOSIS | O=9; E=45.85; O/E=.196; q=.0009/<.0001/.0024/<.0001 | 對預測系統的評估／驗證研究與預測決策之間缺乏連接 | M4 | — | I4 | 上線前測試、運作中性能量測、觸發式重驗證記錄 | `EA_k`（EA-V） | `EA_k ≥ EA_req^γ(A_k,κ_j)`；EA 成本進 `C^impl`；`P(z,ω|k)` 可依 EA 不同而不同（僅有證據時） | Static core | **Keep（I4 anchor）** | 是 M4 最直接的文獻表現 |
| G07 | HUMAN_AUGMENTATION | EVALUATION_SELECTION | O=2; E=9.75; O/E=.205; q=.0197/.0147/.0304/.0290 | 增強人判斷的 AI 與評選／挑選決策之間缺乏連接 | M3 | — | I3 | 同 G01，但決策型態為多選項評選 | `m_k`；`A_k` | 同 G01 | Static core | **Merge → I3** | 與 G01 同一人機配置介面，差異只在任務型態（以 `task_family` 標籤記錄，不另設構念）；observed=2 屬小計數，幅度不作解讀 |
| G08 | RECOMMENDATION_OPTIMIZATION | HUMAN_REVIEW_ACCOUNTABILITY | O=8; E=36.27; O/E=.221; q=.0009/<.0001/.0024/<.0001 | AI 建議／最佳化結果與人工審查問責之間缺乏連接 | M1 | M3 | I1（Level 2）＋ I3 bridge | 建議被採用前誰簽核；建議是否可被修改；採用與修改的實際頻率 | `H_k`；`m_k` | 同 G02 的 H 門檻；`ρ(Modify)`、`ρ(Use)` 進期望結果 | Static bridge | **Merge → I1** | 授權與問責是主問題（建議能否直接成為行動）；人機配置作為次要連結 |
| G09 | PREDICTION_RISK_ESTIMATION | GOVERNANCE_OVERSIGHT | O=26; E=89.01; O/E=.292; q=.0009/<.0001/.0024/<.0001 | AI 風險估計與治理／監督結構之間缺乏連接 | M1 | — | I1（**Level 1 表現**） | 企業 AI policy、禁止條件、授權變更權、名義與正式決策權等級 | `γ ∈ Γ`（policy profile）；`Allow_γ`；`G_j(γ)` | `q_jk ≤ Allow_γ(j,k)`；`G_j(γ) ≥ G_req(A_k,κ_j)`；`C^gov(γ)` 進目標 | Static core | **Keep（I1 anchor）** | 企業層唯一直接決定授權邊界的介面；也是 policy 是否「增加價值或只增加官僚」的分析點 |
| G10 | PREDICTION_RISK_ESTIMATION | EVALUATION_SELECTION | O=8; E=27.13; O/E=.295; q=.0009/<.0001/.0058/<.0001 | 風險分數如何轉成選擇（門檻設定）缺乏研究 | M3 | M4 | I3（optional） | 分數分布、真實標記、門檻規則 | 門檻 `τ`（以離散配置變體 `k_τ` 進 `M_j`） | `P(z,ω|k_τ)` 需由分數與標記資料識別 | **Optional module** | **Keep as optional；否則 evidence-only** | 只有存在真實 score／label／truth 時，門檻才是可識別的決策變數；否則任何門檻值都會是虛構 |
| G11 | EVALUATION_ASSESSMENT | ALLOCATION_PLANNING | O=12; E=39.65; O/E=.303; q=.0009/<.0001/.0024/<.0001 | 評估結果回饋到下一期配置與規劃的連接 | M5 | M4 | I5 | 跨期 initiative 結果與下一期預算／配置變更紀錄 | `b_{t+1}` 對 `O_t` 的反應 | 跨期轉移式（§6.3）；不進靜態目標 | **Dynamic** | **Keep as M5** | 本質是時間序列的回饋；靜態模型若放入會把未觀察的學習效果當成係數 |
| G12 | PREDICTION_RISK_ESTIMATION | INFORMATION_ACQUISITION | O=21; E=68.24; O/E=.308; q=.0009/<.0001/.0024/<.0001 | 風險估計如何指引資訊取得（先試點、再擴大） | M5 | M4 | I5 | 試點決策、試點後參數區間縮小的紀錄 | 試點／資訊取得決策 | 跨期；靜態對應只作 **value-of-identification 診斷**（42 §13.5），不作目標項 | **Dynamic** | **Keep as M5** | 資訊取得的價值來自跨期；靜態版只能回答「哪些參數最值得先量」 |
| G13 | EXPLANATION_ASSURANCE | PREDICTION_DIAGNOSIS | O=15; E=43.51; O/E=.345; q=.0009/<.0001/.0024/<.0001 | 解釋能力與預測決策的使用之間缺乏連接 | M4 | M3 | I4（EA-X 子面向） | 使用者能否用理由形成可檢驗的查核問題；解釋出現時的接受／查核行為 | `EA-X_k`（候選） | **只作 `ρ` 的查表鍵**：`ρ(r|k,z,ℓ)` 可依 EA-X 不同；不作風險降低項、不作門檻（內容效度前） | Static conditional | **Merge → I4** | S4 指出解釋可能增加錯誤建議的接受；故 EA-X 不能被寫成單調降低風險 |
| G14 | PREDICTION_RISK_ESTIMATION | GENERAL_DECISION_PROCESS | O=8; E=20.56; O/E=.389; q=.0045/.0032/.0089/<.0001 | 風險估計如何嵌入一般決策流程 | M2 | M3 | I2 | 風險輸出是否被系統送入決策節點；在哪一節點被使用 | `WI_k` | 同 G03 的 WI 門檻 | Static bridge | **Merge → I2** | Decision family 為「一般決策流程」，企業層問題是路由；pair 過寬，故不單獨立構念 |
| G15 | EXPLANATION_ASSURANCE | EVALUATION_SELECTION | O=7; E=16.38; O/E=.427; q=.0206/.0232/.0387/.0147 | 解釋能力與評選決策的連接 | M4 | M3 | I4（EA-X）＋ I3 bridge | 同 G13，任務型態為評選 | `EA-X_k`（候選） | 同 G13 | Static conditional | **Merge → I4** | 與 G13 為同一 EA-X 介面的不同任務型態 |
| G16 | COORDINATION_EXECUTION | HUMAN_REVIEW_ACCOUNTABILITY | O=10; E=21.30; O/E=.470; q=.0169/.0168/.0137/.0086 | AI 執行與人工審查／問責之間缺乏連接：AI 已執行的行動誰能停止、誰負責 | M1 | M2 | I1 ＋ I2 bridge | 執行中止權、回復路徑、事後問責 | `H_k`（H=3 停止／回復）；`FB_jk` | `A_k=3 ⇒ H_k ≥ H_req(3,κ)` 且 `FB_jk=1`；回復成本進 `C^impl` | Static bridge | **Merge → I1** | 主問題是授權與停止權（M1），流程回復為其必要條件（M2） |

---

## 3. 對四個問題的回答

### Q1 16 gaps 能否收斂成 M1–M4？

**可以，但不是 16 個都收進 M1–M4。** 最終命運：

| 命運 | Gaps | 數量 |
|---|---|---|
| Static core / bridge → **M1 (I1)** | G09（L1 anchor）、G02、G08、G16 | 4 |
| Static core / bridge → **M2 (I2)** | G03（anchor）、G14 | 2 |
| Static core → **M3 (I3)** | G01（anchor）、G07 | 2 |
| Static core / bridge / conditional → **M4 (I4)** | G06（anchor）、G05（L1）、G13、G15（後兩者 EA-X conditional） | 4 |
| **Optional module**（M3/M4 內） | G10 | 1 |
| **Dynamic extension M5 (I5)** | G11、G12 | 2 |
| **Evidence-only** | G04 | 1 |
| **Excluded（無任何角色）** | — | 0 |

12 個 gap 進入靜態模型（透過 4 個介面），1 個為條件模組，2 個為動態擴充，1 個留在證據層。沒有「保留但不知道作什麼」的 gap。

### Q2 是否需要新增 Strategic Alignment `S` 或 Change / Absorptive Capability `C`？

**不新增。** 兩者都能由既有企業層變數表達，新增只會造成與既有變數重疊的構念：

| 候選 | 若新增會量什麼 | 既有架構如何表達 | 判定 |
|---|---|---|---|
| `S` Strategic Alignment | initiative 與企業策略的契合 | (i) 可貨幣化的策略價值進 `v_j`（需證據）；(ii) 不可貨幣化的策略要求進 policy profile `γ` 的強制集合 `J^must_γ`／禁止集合 `J^forbid_γ`；(iii) 外部評估者（董事端、合作商、投資端）挑戰 `v_j` 區間與強制集合 | **不新增**；S 若作為 0–3 分數，將被迫以權重進目標，違反尺度規則 |
| `C` Change / Absorptive Capability | 組織吸收與使用新能力的程度 | (i) 靜態：共享能力 `y_CHG`（訓練、支援、變革管理）作為部分配置的前提，且 `ρ` 可依 `y_CHG` 不同（僅有證據時）；(ii) 動態：吸收能力的累積屬 M5 | **不新增**；Cohen & Levinthal（1990）指出吸收能力依賴先前相關知識，本質是跨期累積，不宜成為靜態分數 |

### Q3 哪些 G 不應進靜態數學模型？

| Gap | 處理 | 何時可升級 |
|---|---|---|
| **G04** | Evidence-only，不建模 | 只有在企業中發現生成式診斷有**不同於 I1–I4 的配置問題**時（目前沒有理論依據）才重審 |
| **G10** | Optional score-to-choice | 存在真實分數分布、標記真值、可回溯門檻規則時，以離散門檻變體 `k_τ ∈ M_j` 加入；`P(z,ω|k_τ)` 必須由資料識別 |
| **G11** | Dynamic M5 | 至少兩期的 initiative 結果與配置變更紀錄 |
| **G12** | Dynamic M5；靜態只作 value-of-identification 診斷 | 至少一次試點前後的參數區間紀錄 |

另外，**G13、G15（EA-X）是 static conditional**：在 EA-X 錨點通過內容效度（V1）前，只能作為 `ρ` 的分組鍵，不得作為門檻或風險降低項。

### Q4 哪些 gaps 是同一企業介面的不同文獻表現？

| 合併群 | 共同企業決策 | 合併理由 |
|---|---|---|
| **G09 + G02** | 授權邊界：企業層定政策（G09），部門層定審查責任（G02） | 同一授權介面在兩個層級的表現；以 `γ → (Allow, G_j, H_req)` 一組變數表達 |
| **G02 + G08 + G16** | AI 輸出成為行動前／中／後，誰審、誰停、誰負責 | 三者 Decision family 皆為 HUMAN_REVIEW_ACCOUNTABILITY；AI family 不同（風險估計／建議／執行）只改變 `A_k` 與 `H_req` 查表格，不需新構念 |
| **G03 + G14** | AI 輸出路由與回復 | 皆為「輸出如何進入流程」的問題；以 `WI`、`FB` 表達 |
| **G01 + G07** | 人機配置 | AI family 同為 HUMAN_AUGMENTATION；差異只是任務型態標籤 |
| **G13 + G15** | 解釋可用性對反應的影響 | AI family 同為 EXPLANATION_ASSURANCE；差異只是任務型態 |
| **G06 + G05** | 評估保證：部門層驗證（G06）與企業層共享評估能力／配置決策保證（G05） | 同一 assurance 介面的兩個層級 |
| **G11 + G12** | 跨期學習與再配置 | 皆需 longitudinal evidence |

一個值得在 Discussion 中保守處理的結構觀察：16 個 depletion 中有 5 個（G02、G09、G10、G12、G14）以 PREDICTION_RISK_ESTIMATION 為 AI family，且分別連到審查、治理、評選、資訊取得與一般流程。這只表示「風險估計類 AI 與這些組織決策節點的連結在文獻中相對少見」，**不表示企業中風險估計 AI 沒有被治理或沒有被使用**。

---

## 4. Frozen Gap-to-Mechanism Map v2.1

```
G09 ─┐                                  ┌─ Γ / γ, Allow_γ, G_j(γ), C^gov(γ)        [Level 1]
G02 ─┼─ I1 Authority-to-act ── M1 ──────┼─ H_k, Eff_H(j,k), H_req^γ(A,κ)          [Level 2]
G08 ─┤                                  └─ ē_j^γ（severe-incident tolerance）     [hard constraint]
G16 ─┘ (bridge → I2)

G03 ─┬─ I2 Routing & recovery ── M2 ──── WI_k, WI_req^γ(A,κ), FB_jk, C^impl, K^ENG
G14 ─┘

G01 ─┬─ I3 Configuration & response ── M3 ── m_k, A_k, Cons(A,m), ρ, P, π
G07 ─┘
G10 ─── (optional threshold variants k_τ; data-gated)

G06 ─┐                                  ┌─ EA_k, EA_req^γ(A,κ)                     [Level 2]
G05 ─┼─ I4 Assurance ── M4 ─────────────┼─ y_EVAL prerequisite; output provenance   [Level 1]
G13 ─┤                                  └─ EA-X_k as ρ-key only (conditional)
G15 ─┘

G11 ─┬─ I5 Learning & reallocation ── M5 (dynamic only)
G12 ─┘   static shadow: value-of-identification diagnostic

G04 ─── evidence layer only
```

---

## 5. Construct Freeze（Phase B）

### 5.1 最小充分構念架構

目標是**不重疊、可觀察、與方程相關、理論可辯護、在企業層有意義**。結果為 **4 個機制構念族 + 1 個企業架構族**，另有 1 個動態擴充：

| 族 | 來源 | 凍結元素 | 型別 | 在模型中的唯一職責 |
|---|---|---|---|---|
| **F1 Governance & Decision Rights（M1）** | I1 | `γ ∈ Γ`（policy profile） | nominal（有限選單） | 企業層決策變數 |
| | | `Allow_γ(j,k)`、`Legal_jk` | binary | 可行性 |
| | | `G_j(γ)` | ordinal 0–3 | 同構念門檻 `G_j(γ) ≥ G_req(A_k,κ_j)` |
| | | `H_k` | ordinal 0–3 | 同構念門檻 `H_k ≥ H_req^γ(A_k,κ_j)`；查表鍵 |
| | | `Eff_H(j,k)` | binary | 有效控制（資訊、時間、真實否決）；`H_req ≥ 2` 時必須為 1 |
| | | `κ_j` | ordinal class（低／中／高） | 只作查表鍵 |
| | | `ē_j^γ` | count／period | 不可貨幣化的硬性風險上限 |
| | | `C^gov(γ)` | TWD／period | 治理營運成本 |
| **F2 Workflow & Integration（M2）** | I2 | `WI_k` | ordinal 0–3 | 同構念門檻；查表鍵 |
| | | `FB_jk` | binary | fallback／rollback 存在 |
| | | 例外與整合成本、工時 | TWD、hours | 進 `C^impl`、`c^op`、`K^h` |
| **F3 Human–AI Configuration & Response（M3）** | I3 | `m_k ∈ {HumanOnly, AI→Human, Human→AI, Aggregation, Delegated, BoundedExecution}` | nominal | 配置型態 |
| | | `A_k` | ordinal 0–3 | 同構念門檻鍵；`Cons(A,m)` |
| | | `ρ_j(r|k,z,ℓ,y)`、`P_j(z,ω|k)`、`π_j(ℓ)` | probability | 期望結果 |
| **F4 Evaluation & Assurance（M4）** | I4 | `EA_k`（EA-V） | ordinal 0–3 | 同構念門檻；查表鍵 |
| | | `EA-X_k` | ordinal 0–3（**conditional**） | 僅作 `ρ` 的分組鍵，內容效度前不作門檻 |
| | | `y_EVAL` | binary | 共享評估能力前提 |
| **F5 Shared Capability & Resource Architecture（企業架構，非 gap 推導）** | 38/39 §10 | `y_c` | binary | 企業層決策變數 |
| | | `F_c`、`K^h_c` | TWD／period、hours／period | 共享固定成本與容量，只計一次 |
| | | `Pre(j,k)` | binary relation | 前提限制 |
| | | `R_j(y)`、`D(y)` | ordinal 0–3（由 `y` 查表決定） | 同構念門檻 `R_j(y) ≥ R_req(A_k)` |
| | | `B̄`、`K̄^h`、envelopes `e_u` | TWD／period、hours／period | 資源限制與企業分配 |
| | | `C^impl_jk(y)` | TWD／period | 共用能力可改變局部成本（reuse），僅有證據時 |
| **（Dynamic）M5 Learning & Resource Feedback** | I5 | `O_t → b_{t+1}`；試點資訊 | 跨期 | 不進靜態 baseline |

### 5.2 與 v2.0 構念清單的差異

| v2.0 構念 | v2.1 處理 | 理由 |
|---|---|---|
| `D` shared interoperability | 改為 `D(y)`：由共享能力狀態決定的 ordinal 門檻鍵，歸 F5 | D 是企業平台能力，不是部門配置選擇；由 `y_INT` 決定 |
| `R` data readiness | 改為 `R_j(y)`：由 `y_DATA` 與單位現況決定的 ordinal 門檻鍵，歸 F5 | 同上 |
| `G` formal decision rights | 改為 `G_j(γ)`：由企業 policy 決定，歸 F1 | 正式權限是 policy 的產物，不是部門自選 |
| `A_aut`、`H`、`WI`、`EA-V` | 保留為 ordinal 門檻鍵與查表鍵 | 不變 |
| `EA-X` | 保留為 conditional `ρ` 分組鍵 | S4 |
| `κ` | 保留為後果類別鍵 | 不變 |
| 新增 `Eff_H` | binary | Elish（2019）與 Aghion & Tirole（1997）支持名義權與實質控制分離 |
| 新增 `ē_j^γ` | count／period 硬性上限 | 不可貨幣化風險不換算 TWD |
| `S`、`C` | 不新增 | §3 Q2 |

### 5.3 尺度鐵律（重申）

- Ordinal 值（`A,H,WI,EA,EA-X,G,R,D,κ`）只出現在：(a) 同構念 `≥` 比較；(b) 查表索引；(c) 可行性旗標。
- 任何 ordinal 值**不得**出現在 `+ − × ÷`、加權總分、分母、乘數中。
- 對任何保序重新標號（strictly increasing relabeling），可行集合與最適解必須不變（42 §15、45 T-INV-3）。

---

## 6. Gap → Mechanism → Observable → Variable → Equation（追溯表）

方程編號對應 `42_ENTERPRISE_PORTFOLIO_MODEL_v2_1.md`。

| Gap | Mechanism | Observable | Variable | Equation / Constraint | 模型命運 |
|---|---|---|---|---|---|
| G09 | M1 | AI policy 文件、禁止條件、授權變更權 | `γ`, `Allow_γ`, `G_j(γ)`, `C^gov(γ)` | (F3) `q_jk ≤ Allow_γ(j,k)`；(F5c) `G_j(γ) ≥ G_req(A_k,κ_j)`；(OBJ-E) `−C^gov(γ)` | Core static |
| G02 | M1 | 審查責任人、行動前否決權、可見資訊與時間 | `H_k`, `Eff_H` | (F5a) `H_k ≥ H_req^γ(A_k,κ_j)`；(F6) `Eff_H=1` 若 `H_req≥2` | Core static（merged） |
| G08 | M1／M3 | 建議採用前簽核、修改紀錄 | `H_k`, `m_k`, `ρ` | (F5a)；(X1) 期望值中的 `ρ(Modify)`、`ρ(Use)` | Bridge |
| G16 | M1／M2 | 執行中止與回復紀錄 | `H_k`, `FB_jk` | (F5a) with `A_k=3`；(F7) `FB_jk=1` | Bridge |
| G03 | M2 | 路由深度、例外路由、整合工時 | `WI_k`, `FB_jk`, `C^impl`, `K^ENG` | (F5b)；(F7)；(R1)(R2) | Core static |
| G14 | M2／M3 | 風險輸出進入決策節點的位置 | `WI_k` | (F5b) | Bridge（merged） |
| G01 | M3 | 決策順序、最終權、角色反應 | `m_k`, `A_k`, `ρ`, `P`, `π` | (F8) `Cons(A_k,m_k)=1`；(X1)；(OBJ-E) | Core static |
| G07 | M3 | 同上（評選任務） | 同上 | 同上 | Core static（merged） |
| G10 | M3／M4 | 分數、標記、門檻 | `k_τ ∈ M_j` | (X1) 中 `P(z,ω|k_τ)` 由資料識別 | Optional |
| G06 | M4 | 測試、監控、重驗證紀錄 | `EA_k` | (F5d) `EA_k ≥ EA_req^γ(A_k,κ_j)`；EA 成本進 `C^impl` | Core static |
| G05 | M4（L1） | 共享評估平台、配置決策的稽核輸出 | `y_EVAL` | (F4) `q_jk ≤ y_EVAL` 若 `EA_k ≥ EA^cap`；42 §18 輸出契約中的 provenance／robustness 欄位 | Bridge（L1） |
| G13 | M4（EA-X） | 理由可用性、解釋下的接受行為 | `EA-X_k` | (X1) `ρ(r|k,z,ℓ)` 以 EA-X 分組；不作門檻 | Conditional |
| G15 | M4／M3 | 同上（評選） | 同上 | 同上 | Conditional（merged） |
| G11 | M5 | 跨期結果與再配置 | `b_{t+1}(O_t)` | (D1)（42 §16） | Dynamic |
| G12 | M5 | 試點前後參數區間 | 試點決策 | (D2)；靜態 VOI 診斷（42 §13.5） | Dynamic |
| G04 | — | — | — | — | Evidence-only |

---

## 7. 回退與驗證規則（V1 前的保護）

1. **盲編否決單一 gap 的主機制**：該 gap 改掛盲編裁決的機制；若新機制已在 F1–F4 內，只改追溯表，不改模型。
2. **盲編否決一整個機制**（例如 M3 的 G01、G07 都被判定不屬人機配置）：該機制在 Discussion 中降為「研究者提出、未獲獨立支持的介面」，但其方程元素（如 `m_k`、`ρ`）仍可因 38/39 的企業架構理由保留——**模型元素的存在理由與 gap 的支持必須分開陳述**。
3. **盲編主張 G04 有獨立介面**：需提出 I1–I4 無法表達的配置決策，才重審。
4. **EA-X 內容效度未過**：G13、G15 留在 evidence layer，`ρ` 不以 EA-X 分組。
5. 盲編結果、分歧、裁決與一致性區間全部寫入 Chapter 4.1／4.2，不以研究者對應表代替。

---

## 8. 本輪新增文獻在收斂中的角色

（完整 claim-level 審核見 `44_MANUSCRIPT_ENTERPRISE_AI_DECISION_v2_1.md` 附錄 A。）

| 文獻 | 支持的收斂判斷 | 不支持 |
|---|---|---|
| Aghion & Tirole（1997） | F1 中名義（formal）與實質（real）權威分離 → `G_j(γ)` 與 `Eff_H` 分開 | 不支持任何 AI 特定的權限門檻值 |
| Sambamurthy & Zmud（1999）；Weill & Ross（2004） | IT 治理是決策權的配置模式，且依多重情境而異 → `Γ` 為有限 policy 選單，而非單一最佳 | 不支持特定 policy 對 AI 價值的效果 |
| Dietvorst et al.（2015）；Logg et al.（2019）；Lebovitz et al.（2022） | 使用者可能迴避、偏好或依情境選擇是否採用演算法 → `ρ` 方向不可預設 | 不支持任何企業的實際反應機率 |
| Breck et al.（2017）；Raji et al.（2020） | 生產環境 ML 需要測試、監控與內部稽核 → EA-V 錨點與成本是實質項目 | 不支持 EA 必然降低損失 |
| Cohen & Levinthal（1990） | 吸收能力依先前相關知識累積 → C 歸 M5，不作靜態分數 | 不支持吸收能力的量化尺度 |

**本檔凍結 v2.1 的 gap 收斂結果與構念架構。後續模型（42）、參數識別（43）、正文（44）與驗證（45）均以本檔為上位對應。**
