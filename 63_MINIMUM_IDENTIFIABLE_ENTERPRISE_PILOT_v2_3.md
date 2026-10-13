# 63 — Minimum Identifiable Enterprise Pilot v2.3

**狀態：設計規格，2026-10-11。** 本檔回答：「最小但真的能解」的企業 pilot 需要哪些格、哪些格必須 OBSERVED、哪些可以用區間或界、缺哪一格會讓哪個研究問題變成 UNIDENTIFIED。參數契約只以 `43_PARAMETER_IDENTIFICATION_AND_QUANTIFICATION_v2_1.md` 為準；模型為 `42` v2.2；求解器為 `51`；資料進入方式為 `62` 樣板與 `65` loader。本檔**不含任何企業數值**，也不指定受訪者。

可直接使用的空白骨架：`63_MINIMUM_PILOT_SKELETON_v2_3/`。這是由 `python 65_enterprise_data_loader_v2_3.py --make-pilot` 產生的 CSV 與 .xlsx，每一格都已列出，狀態一律為 `UNIDENTIFIED`。對骨架執行 `--validate` 不會有錯誤，執行 `--run` 不會產生任何 point decision。

---

## 1. 最小結構與理由

| 元素 | 最小值 | 骨架中的代號 | 為什麼不能更少 |
|---|---|---|---|
| 事業單位／功能 | 2 | `BU1`、`BU2` | 雙層 Model C 的 envelope 分配與帳本對齊（DL）至少需要兩個 follower；只有一個單位時，C 與 B 的差只剩單一部門的帳本差異，無法檢驗跨單位資源競爭 |
| AI initiatives | 3（BU1 兩個、BU2 一個） | `INI1`、`INI2`（BU1）、`INI3`（BU2） | 同一單位內需有 initiatives 之間的取捨（部門計畫是組合），跨單位需有 envelope 競爭 |
| 共享能力 | 1，且至少一個單位有本地自建替代方案 | `CAP1`（SHARED）＋ `CAP1` LOCAL @ `BU2` | Q2 需要 `F_c^†`；shared vs local 比較需要 `F^loc`、`a^loc` 與 `C^impl(s=L)`，否則 VSC 只能比較「有共享 vs 完全沒有能力」 |
| 角色群 | 2 | `ROLE1`、`ROLE2` | `π`、角色別工時 `t` 與 `λ_ℓ` 才有意義；`ρ` 的角色差異是 M3 的核心 |
| 每個 initiative 的配置 | 2（status quo ＋ 一個 AI 配置） | `SQ`、`AI1` | 少於 2 就只能評估現況，沒有最適化 |
| 可見訊號 × 隱藏結果 | 2 × 2 | `Z_FLAG/Z_NOFLAG` × `W_OK/W_ERR` | `ρ` 必須以可見訊號為條件，且不得以 `ω` 為條件；錯誤結果是損失與 (F9) 的來源 |
| AI 配置的反應集合 | 3 | `Use`、`Verify`、`Reject` | 至少需要「接受」、「查核」、「拒用」才能表現反應如何改變價值（Q6）；可依實際權限增減 |
| Policy profiles | 2 | `POL_CUR`（CURRENT）、`POL_LEGALMIN`（LEGAL_MINIMUM） | Q3 的 VG 分解需要 `γ` 與法規最低方案 `γ^0`；只做 Q1、Q2 時可只填 `POL_CUR` |
| 模型 | B（集中）＋ C（雙層）；A、A+、C0 作比較 | — | 依使用者要求；A 需要 `B^0_u` |

骨架共有 620 列參數格：E 19、G 144、X 127、R 156、V 174。其中有不少是「擇一」或「只在某題需要」的格（§3），真正的最小核心少於此數。

**建議的最小粒度（已寫在骨架的 `assumption_note` 中，可以確認或拆細）：**

- `v_u, v_x, l_u, l_x, I_sev`：依 (initiative, config, ω, r) 填，並宣告對 role 與 z 不變（`*`）。
- `t`：依 (role, r) 填，並宣告對 z、ω 不變。
- `t_rev`：依 r 填。
- `c_u, c_x`：每個配置一格。

任何不變性宣告都是可檢驗的假設，不是補值。

## 2. 研究問題 × 最小識別集合

欄位說明：

- **最少參數**：該題計算必需的參數格。
- **必須 OBSERVED**：沒有文件或紀錄就無法辯護的格；以內部專家區間代替，會使該題的結論退成條件性。
- **EXP 區間**：可以 `EXPERT_ELICITED_INTERNAL`（或外部）區間進入。
- **PUB 界**：可以用 `PUBLIC_OBSERVED_BOUND` 給上下界。
- **SCN**：只能作預先登記的情境。
- **缺 → UNIDENTIFIED**：缺少該格時 51／65 的實際狀態與後果。

### Q1 企業協調 vs 各部門獨立（NEV = VCP + VSC − DL；VCP = VRA + DL0）

| 項目 | 內容 |
|---|---|
| 最少參數 | E：`Ā^BUD`、`Ā^ENG`、`rev_cap_u`、`B^0_u`（BUD、ENG）、`F_c`、`a^ENG_c`、`F^loc`、`a^loc`、`y^cur_c`。G（`POL_CUR`）：`Allow(j,k)`、`allow_loc`、`G_j`、實際用到的要求表格 `(A_k, κ_j)`、`ē_j`、`ΔC^gov`、`J^must/J^forbid`。X：`κ_j`、`Rel(j)`、配置屬性 `(A,H,WI,EA,m)`、`Pre`、`Legal`、`Eff_H`、`FB`、`Cons`、`R_k`、`C^impl(s)`、`a^ENG(s)`、`R_j(s)`／`D_j(s)`（只在要求高於尺度最小值時）。R：`π`、`P`、`ρ`（obs 或 cf）。V：`N`、`v、l、c、t、t_rev、I^sev`。λ：`λ_ℓ` 或至少 `λ^U_ℓ`。DL 另需帳本拆分（`v^u/v^x`、`l^u/l^x`、`c^u/c^x`、`C^{impl,x}`、`τ`、`λ^u`） |
| 必須 OBSERVED | `Ā`、`B^0_u`（預算文件）；`Allow`、`G_j`、要求表、`Legal`、`allow_loc`（政策與授權文件）；現況配置屬性、`κ_j`、`Pre`；`N_{j0}`（交易／案件紀錄）；帳本歸屬規則：哪些價值、損失、成本記在部門 P&L／KPI，`C^{impl,x}` 與 `τ` 的規則 |
| EXP 區間 | 未部署配置的 `C^impl`、`a^ENG`、`P`、`ρ^cf`（盲真值題卡）、`v、l、t、I^sev`；`F_c` 與 `F^loc`（若尚無報價）；`N_{jk}` |
| PUB 界 | `λ^U`（含負擔薪資上界）；`c`（推論／雲端公開價格）；`F_c`（公開授權價）；AI 配置 `t` 的端點（需附任務相似性說明） |
| SCN | `N_{jk} ≠ N_j` 的 throughput 情境 |
| 缺 → UNIDENTIFIED | `B^0` 缺 → Model A 不可解，VRA、VCP、NEV 為 UNIDENTIFIED（B、C、VSC、DL 照算）。帳本拆分缺 → C、C0、A 為 `FOLLOWER_LEDGER_UNIDENTIFIED`，DL、DL0、NEV 為 UNIDENTIFIED（VSC 照算）。`F^loc` 缺 → shared vs local 比較為 UNIDENTIFIED。`Ā` 缺 → 全部 `REJECT_INSUFFICIENT_IDENTIFIED_INPUTS`。`λ` 缺且無 `λ^U` → `PARTIAL_OBJECTIVE` 且掃描為 UNIDENTIFIED |

### Q2 共享能力何時值得集中投資（`F_c^†`、`δ^†`）

| 項目 | 內容 |
|---|---|
| 最少參數 | Q1 中 Model B 的全部格，**不含** `F_c` 本身（51 以 THRESHOLD_MODE 求 `F_c^†`）；`C^impl(s)` 在 `s=∅`、`s=S`（以及 `s=L`）三種狀態下的值（決定 `δ`） |
| 必須 OBSERVED | 同 Q1 的可行性與資源格 |
| EXP 區間 | `C^impl(s)` 各狀態（最好來自已完成專案的對照） |
| PUB 界 | `F_c` 公開價格 |
| SCN | `δ`（若無對照證據，以 `[0, δ^U]` 進 Θ） |
| 缺 → UNIDENTIFIED | `C^impl(s=S)` 或 `C^impl(s=∅)` 缺 → 該配置在該狀態被排除，`δ^†` 為 UNIDENTIFIED。在 C 中，帳本不對齊時建置區域可能是集合值（42 P4 反例），只報掃描結果 |

### Q3 治理何時提高價值而非只增加官僚（VG = EE + RE + CE）

| 項目 | 內容 |
|---|---|
| 最少參數 | 兩個完整 policy：`POL_CUR` 與 `POL_LEGALMIN`（`γ^0`），各自的 `Allow`、`G_j`、要求表、`ē`、`ΔC^gov`；以及 Q1 中 Model B 的全部格 |
| 必須 OBSERVED | 現行政策條文與授權矩陣；`γ^0` 的法規最低要求（以法規文本逐條界定） |
| EXP 區間 | `ΔC^gov`（委員會工時、稽核成本） |
| PUB 界 | `γ^0` 的法規下界（需逐條核對；EU AI Act 等只作結構參照） |
| SCN | 第三個替代 `γ`（若有實際被討論的方案） |
| 缺 → UNIDENTIFIED | 沒有 `γ^0` → VG 不可算（65：`governance = UNIDENTIFIED`）。`ΔC^gov` 缺 → 該 policy 被排除（`RESTRICTED_SOLVE`），整個 VG 不可算。註：51 的 `governance_decomposition` 需要兩個 policy 都有 `ΔC^gov` |

### Q4 部門最適何時偏離企業最適（DL 與 (AL) 來源）

| 項目 | 內容 |
|---|---|
| 最少參數 | Q1 中 C 與 B 的全部格，加上帳本拆分 `v^x, l^x, c^x, C^{impl,x}, τ, λ^u` |
| 必須 OBSERVED | 帳本拆分規則（部門 KPI／P&L 文件、內部計價、中央出資規則）；這些是 **DEF/OBS 規則**，不是估計值 |
| EXP 區間 | `v^x, l^x` 的大小（外部性：跨部門重工、客戶影響） |
| PUB 界 | 無 |
| SCN | 無 |
| 缺 → UNIDENTIFIED | 任一拆分缺 → `FOLLOWER_LEDGER_UNIDENTIFIED`，DL 與其來源分解為 UNIDENTIFIED。(AL3) 部門專屬限制不在 51 baseline，只有在有文件證據時才加入，否則不分解 |

### Q5 H／WI／EA 何時是必要限制（AT／ABOVE、`PR_X`、保護功能）

| 項目 | 內容 |
|---|---|
| 最少參數 | 要求表中被實際配置用到的格；配置屬性；`I^sev`、`ē`；Model B 的全部格 |
| 必須 OBSERVED | 要求表（政策條文；若無明文，由治理、IT、流程負責人引出並記錄理由）；配置的 `H, WI, EA` 等級（依 41 錨點的文件或系統檢查） |
| EXP 區間 | 未部署配置的 `I^sev` |
| PUB 界 | 無 |
| SCN | 無 |
| 缺 → UNIDENTIFIED | 要求表任一被用到的格缺 → 該配置被排除，`PR_X` 為 UNIDENTIFIED（65 不會用最高或最低值補）。要分辨「保護功能 vs 官僚候選」需要 Q7 的 registry 與 `I^sev` 區間 |

### Q6 使用者反應如何改變實際價值（VRG、design-response regret）

| 項目 | 內容 |
|---|---|
| 最少參數 | `ρ^design`（每個 AI 配置）；`ρ^obs`（已部署）或 `ρ^cf`（未部署）；Model B 的全部格 |
| 必須 OBSERVED | `ρ^design`（作業程序文件）；已部署配置的 `ρ^obs`（系統紀錄或抽樣觀察，需能對應到可見訊號 `z`） |
| EXP 區間 | `ρ^cf`（盲真值題卡：受訪者只看到 `z`，看不到 `ω`） |
| PUB 界 | 不得用演算法迴避／偏好文獻給數值，只能作方向參照 |
| SCN | 無 |
| 缺 → UNIDENTIFIED | `ρ^design` 缺 → VRG 不可算。實際 `ρ` 缺 → 該配置被排除。若設計 portfolio 在實際反應下違反 (F9)／(R2) → `DESIGN_INFEASIBLE_UNDER_RESPONSE`（這是正式結果，不是缺值） |

### Q7 哪些決策 ROBUST／CONDITIONAL／FRAGILE

| 項目 | 內容 |
|---|---|
| 最少參數 | Q1（B）的全部格，其中不確定的格以區間給出；**在看到任何結果前**完成 registry 登記與 commitment（`65 --make-registry`，並 commit 到 git） |
| 必須 OBSERVED | registry 本身是 DEF；區間來源需逐格標示 provenance |
| EXP 區間 | 所有 EXP 區間格 |
| PUB 界 | 所有 PUB 界格（只作界） |
| SCN | 情境組 `𝒢` |
| 缺 → UNIDENTIFIED | 沒有事前登記 → 不得報 ROBUST／CONDITIONAL／FRAGILE。頂點數超過 4096 → 需先在 `U_registry` 登記分組規則（研究者決策並揭露）。元素層級分類只報涵蓋率，不是證書（42 §13.2） |

### Q8 G01–G16 哪些真正成為企業決策問題（介面活化）

| 項目 | 內容 |
|---|---|
| 最少參數 | Q5 的 `PR_X`（I1：H、G；I2：WI；I4：EA）；最適配置與 status quo 的差異（I3）；以及 **V1 人類盲編結果**（介面 → gaps 的對應） |
| 必須 OBSERVED | 同 Q5 |
| EXP 區間 | 同 Q5 |
| PUB 界 | 無 |
| SCN | 無 |
| 缺 → UNIDENTIFIED | V1 人類盲編未完成 → 介面到 gaps 的回溯只能標「研究者裁決（待 V1）」。`PR_X` 缺 → 對應介面為 UNIDENTIFIED。ACTIVE-ROBUST 需要 Q7 |

## 3. 最小資料蒐集包（依格的性質分組，不依受訪者）

| 包 | 內容 | 性質 | 支援的研究問題 |
|---|---|---|---|
| D1 文件包 | 預算與人力配置（`Ā`、`B^0`、`rev_cap`）、政策／授權矩陣（`Allow`、`G_j`、要求表、`ē`、`J^must/forbid`、`allow_loc`）、法務／資安判定（`Legal`）、架構依賴（`Pre`、`Rel`）、作業程序（`ρ^design`、`Eff_H`、`FB`）、帳本規則（KPI／P&L 歸屬、`C^{impl,x}`、`τ`） | OBS / DEF | 全部；可行集合 |
| D2 系統紀錄包 | 事件量 `N_{j0}`；已部署配置的 `ρ^obs`、`P`（需有標記真值）；工時抽樣 `t`；事件紀錄 `I^sev`；推論帳單 `c` | OBS | Q1、Q6、Q5 |
| D3 成本包 | `F_c`、`F^loc`、`a^ENG`、`C^impl(s)`（報價、合約、專案估算） | OBS / EXP / PUB | Q1、Q2 |
| D4 盲真值題卡 | 未部署配置的 `ρ^cf`（受訪者只看到 `z`） | EXP 區間 | Q1、Q6 |
| D5 後果區間 | 未部署配置的 `v、l、t、I^sev` 區間，以及 `N_{jk}` | EXP 區間 / SCN | Q1、Q5 |
| D6 registry 登記 | `𝒢`、`ε_R`、分組規則 | DEF（事前） | Q7 |

## 4. 之後才附：來源建議（不指定姓名）

| 來源類型 | 可提供的格 | 進入方式 | 不得 |
|---|---|---|---|
| Focal enterprise 內部（財務、IT／資料、治理／法務、流程負責人、第一線角色） | D1–D5 的大多數 OBS 與 EXP 內部區間 | `OBSERVED`、`EXPERT_ELICITED_INTERNAL`、`DEFINITIONAL` | 以職稱替代文件；把名義權限當成 `Eff_H` |
| 董事／董事相關公司 | `v`、`J^must/forbid` 替代方案、`κ`、`ē` 的挑戰區間 | `EXPERT_ELICITED_EXTERNAL`（`source_scope=external`） | 成為 optimizer；把意見改標 OBSERVED |
| 合作商／策略供應商 | `F_c`、`F^loc`、`C^impl`、`c` 的報價或區間；`δ` 的對照案例 | 報價若是給本企業的正式報價 → OBS（`vendor_quote`，`source_scope=internal`，因為那是本企業的交易文件）；一般性的估計 → `EXPERT_ELICITED_EXTERNAL` | 以供應商宣稱的生產力效果作 OBSERVED |
| 投資端 | `v` 的策略價值區間、portfolio 優先序的 face-validity 挑戰（44 §4.9） | `EXPERT_ELICITED_EXTERNAL` | 覆寫模型結果；成為決策層級 |

外部來源一律只能擴大或收窄 `Θ_g`，或新增 `γ` 選項與情境組，並記錄理由；65 的 validator 會拒絕外部來源標成 `OBSERVED`。

## 5. 執行順序

```
python 65_enterprise_data_loader_v2_3.py --make-pilot  data_pilot/      # 或直接複製 63_MINIMUM_PILOT_SKELETON_v2_3/
# 依 §3 的 D1→D2→D3 填入（未取得者保持 UNIDENTIFIED）
python 65_enterprise_data_loader_v2_3.py --validate data_pilot/
python 65_enterprise_data_loader_v2_3.py --run      data_pilot/ --out enterprise_results/
# 有區間格時，先登記再求穩健性：
python 65_enterprise_data_loader_v2_3.py --make-registry data_pilot/ --out registry_v1/   # commit 後才進行下一步
python 65_enterprise_data_loader_v2_3.py --robust  data_pilot/ --registry registry_v1/ --out enterprise_results/
```
