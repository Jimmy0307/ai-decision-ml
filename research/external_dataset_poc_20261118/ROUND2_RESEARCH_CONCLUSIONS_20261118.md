# AI × Decision｜六源資料第二輪實證可行性與 MLP 裁決（2026-11-18）

> **基準：** 此報告完全由 GitHub Actions [run #44269235163](https://github.com/Jimmy0307/ai-decision-ml/actions/runs/44269235163) 實際執行之 `ci-live.json` 與 `ci-research-conclusions.json` 彙整。33/33 個 offline deterministic tests PASS；完整 H2020 官方 project/organisation 來源 ZIP 讀入並分析。**沒有將統計假說結果寫回 main，也沒有宣稱 OpenAlex/SEC 全庫已下載。**
>
> **研究裁決：** `CORDIS_RESOURCE_ALLOCATION_SEMI_EMPIRICAL_READY`；`BURT_BROKERAGE_NOT_IDENTIFIED`；`MULTI_FOLLOWER_EQUILIBRIUM_NOT_IDENTIFIED`。

## 1. 資料庫全體巡檢（實際下載 vs 限制）

| 來源 | 本輪實際運作 | 量化結果 | 實證可識別性 |
|---|---|---|---|
| **CORDIS H2020** | 官方 55,260,681 bytes project/organization ZIP **全數讀取** | 35,389 projects、179,063 participation rows、41,995 organization IDs；project key join **100%** | 可以建立計畫－機構雙模網路、角色與資源分配；無 Follower 偏好/最佳反應 |
| **OpenAlex** | 官方 8-works API 小樣本；**非全庫** | 8 works（8 DOI）、25 author IDs、14 institution IDs；尚無與 CORDIS 的確認性 linkage | 無完整 external-outcome validation；之前 award number-only matching 有碰撞，**不能當 matched grants** |
| **OCDS** | 官方虛構 schema 解析 + UK Find a Tender **1 筆真正公告** | 虛構 2 bidders，真實公告 `tenderers=0` | 沒有可用的反事實投標者集合與成本 |
| **GLEIF Level 2** | 官方真實 LEI API 1 筆 | parent-link keys 存在，parent entity link 仍為 null | 無已驗證母子公司控制邊 |
| **SEC EDGAR** | **未執行** | 需符合官方要求之真實聯絡 User-Agent；沒有用假身分繞過限制 | 財報即使取得也不是內部 AI 資源配置 |
| **PyPSA-Eur** | 非官方 March 2022 GridKit AC/DC/Transformer 三份來源 CSV 已完整讀取 | 11,151 AC + 62 DC + 1,039 transformers → **8,786 節點、11,690 條無向去重物理邊** | 物理拓樸可做 network/solver benchmark，不等於企業組織/社會網絡 |

**完整性與快照：** [FROZEN_SIX_SOURCE_SNAPSHOT_20261118.json](results/FROZEN_SIX_SOURCE_SNAPSHOT_20261118.json) 保留原始回應 SHA-256。GitHub [latest Actions artifact](https://github.com/Jimmy0307/ai-decision-ml/actions/runs/44269235163) 有此輪輸入 JSON、每個來源狀態及完整匯總。OpenAlex 在上一個 run 一度遇 HTTP 429（Too Many Requests），本輪 8-work API 正常；再次抓取應以受控 API 額度處理。**API 成功不等於有研究模型可用。**

## 2. CORDIS 真實資源分配：可以開始做哪一種 MLP？

### 2.1 來源母體與分類敏感度

- 從 **35,389** 個 H2020 計畫，原來只檢查 title/ objective 的探索式 AI/Decision 字串，得到 **195** 個候選。
- 納入 `topics` / `keywords` 欄位後，候選增加到 **233**（比原範疇多 **38**）；這是分類規則敏感度，**不能把 195 或 233 當成已驗證的 AI × Decision 項目**。
- 195 個候選有 **1,436 個不同 project×organisation 配對**，但原始 project/participant-role 記錄是 **1,439 列**（跨角色/重複配對不應被當作獨立單位）。
- 1,105 個 organisation IDs，188 個至少參與兩個候選計畫；195 個計畫均有一列 coordinator 角色，但 coordinator 不等於 Stackelberg leader。
- 195 個候選的 project `totalCost` 加總 **595,155,509.43**，`ecMaxContribution` 合計 **513,799,012.70**；是 CORDIS 公開 project financial fields，**不是企業 AI 額度**。

### 2.2 資金與資料治理驗收

| 確認項目 | 數值 | 解釋 |
|---|---:|---|
| 全 H2020 project/organisation key join | **179,063/179,063** | 不等於所有企業法定身分均已解歧 |
| 全 H2020 organisation `ecContribution` 空值 | **7,800/179,063（4.36%）** | 不應用零代填 |
| 候選 `ecContribution` 空值 | **26/1,439（1.81%）** | 零與 null 不混合 |
| 候選可完整 EC 對帳之 project | **187/195** | 另 8 項不可對帳；不代表失敗 |
| EC 對帳相對差距 ≤1% | **187/187** | 官方 project `ecMaxContribution` ≈ participant `ecContribution` 加總，觀測一致 |
| 候選可完整 `totalCost` 對帳 | **192/195** | 與 EC 欄位不同母體 |
| `totalCost` 對帳差距 ≤1% | **177/192** | 另有 **7/192 差距 >5%**，應查角色與數據口徑 |
| EC allocation HHI（195 項） | median **1.000** | 其中大量 single-beneficiary projects。**必須以至少兩名實際 funding beneficiaries 重新分層**，否則不能推論集中治理 |

**可用於 MLP 的部分**：真實 (y_{pu})（計畫到機構的 EC 配置額）、計畫總資金及協調者／參與者角色；可構建觀測資源分配現況、資源集中度與預算可行性基準。**不等於**我們觀測到各機構選擇 (x_u^*(y)) 反應曲線、效用 (F_u)、底層 shared constraints、行為順序或 Nash equilibrium。因此能做 **semi-empirical constrained resource allocation benchmark**，不能宣稱 `EMPIRICAL_STACKELBERG_VALIDATED`。

## 3. 真實網路測試與 Burt 結構洞的負面界線

- 從 195 個候選項目形成的**投影**網路是 1,049 incident organisations / 12,181 co-membership edges。
- **只有 156/12,181** 個投影邊來自至少兩項共同計畫。其餘單次共同參與形成的連結不能解釋為不存在其他實際合作。
- 863/1,049 個有投影邊的機構僅在一個候選計畫出現；186/1,049 至少兩個。
- 投影圖 Burt Constraint median **0.179911**；「只在一個候選計畫出現」的 median **0.191717**，多計畫機構 median **0.080753**。多計畫者往往度數也較高；**沒有 degree-matched null/independent bilateral ties 時，這不是顯著 broker 結果**。
- Constraint 的最低值約 **0.024007**，但 `Low Constraint = broker` 在由共同計畫生成 clique 的網路上高度容易誤判，**目前 0 validated brokers**（並非檢定出「真實社會網絡沒有 broker」）。

## 4. 跨資料源／原始出版品匹配的 QA 阻塞

- **OpenAlex 授款編號重名：**之前 [run #44268462073](https://github.com/Jimmy0307/ai-decision-ml/actions/runs/44268462073) 用 195 個 CORDIS 數字 project IDs 查 `awards.funder_award_id`，不同 funder/award 會共用數字；查詢分頁也截斷，因此出現 500 筆 `awards` raw results。**不能把這 500 筆或 194 個有編號回應，視為 CORDIS 的確認性授款 matches。** 需同時檢查 DOI `10.3030/{project_id}`、CORDIS provenance、funder 身分，以及分頁 completeness。
- **OpenAlex works：**同輪 `works` 回應超過 2MB 單次保護上限，無可用的逐篇確證；非「未發表任何論文」。
- **CORDIS H2020 project ZIP 確認不包含 `publication.csv`**，裡面只有 project、organisation、topics、euroSciVoc 等七份 CSV；公開資料提供者另有 H2020 publication 分發檔 <https://data.europa.eu/data/datasets/cordish2020projects>。該出版品資料尚未併入本次分析，且官方資料集頁公開標記 2026 年出版品 CSV 欄位錯置問題。**不得以 grant DOI 取代論文 DOI，也不得靜默使用疑似欄位錯位的出版品 CSV。**
- **OCDS：**一張真實 notice 的 0 tenderer 只能說本次公告不能識別 bids，不能推論英國全部政府採購都缺投標者。
- **GLEIF：**一筆 entity record 未提供可驗證的 parent target，不能推論整體 Level 2 coverage。
- **SEC：**不以假的 User-Agent 冒用合法存取。

## 5. 與原本 RQ1–RQ3 的研究決策

| 路線 | 本次裁決 | 統計／識別界線 |
|---|---|---|
| 原 Route A V9：16 組不足呈現顯著 | **不能以本實驗恢復確認性主張** | 新樣本不是原 V9 corpus；Route A 的本機新結果須另收原包審查 |
| RQ1：CORDIS 跨計畫組織網路 | **可做描述與網路建模** | 要先解決同計畫 clique 投影、驗證獨立關係才有 Burt 實證 |
| RQ2：企業機制訪談與治理 | **資料庫不能直接取代** | CORDIS 合作協調關係 ≠ 企業 AI 主管／部門 |
| RQ3：MLP 與共享資源 | **半實證資源分配基準可行** | project funding split 可以驗證分配可行性，仍缺效用、反應、決策先後 |
| Limitation 未解研究問題 | **本輪無證據** | 新資料來源不包含經後續審稿核對的 limitation verdict |

**建議研究選擇**：不要再以「找到低 Constraint 節點」作為成功判準。用 CORDIS 建立具來源的 (y_{pu})、資源上限與 role-based assignment 的 **observed feasible allocation baseline**；把 follower payoff 及 shared constraint 設成**明示的假設、敏感度範圍與合成消融**。接著才利用有獨立且可信的 outcome／偏好證據校準真正 MLP，不可把 33/33 CI PASS 當成模型已經實證確認。

## 6. 後續停止規則

1. 若外部來源只能提供計畫參與而無直接知識／合作流動，Burt 構念維持**描述性投影指標**；不要偷換為真實資訊橋接。
2. 若只有 (y) 而無真實 (x_u^*(y))、(F_u)、時序與共享約束，MLP 標記 `SEMI_EMPIRICAL_CALIBRATION`；不得聲稱正向經驗均衡。
3. 先剔除 single-beneficiary projects；在可比對且多受益者的子集重做 funding shares、role concentration、偏差來源，才可比較中央 vs 分權。
4. 下一輪跨庫連結應先做**授款 DOI + funder + CORDIS provenance** 強制精確匹配，對缺 DOI 或相同數字的不同 funded grants 一律 `UNRESOLVED`。

**實驗封存：**所有數據、公式、命令及 33 項 offline QA 在 [PR #3](https://github.com/Jimmy0307/ai-decision-ml/pull/3) 及其 GitHub Actions artifact；branch-only，維持 draft，`main` 未改。若 OpenAlex API 429、SEC User-Agent、實際企業 follower response 未取得，屬於**來源／識別阻塞**，不是使用者電腦跑不動。
