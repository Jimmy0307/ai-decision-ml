# G 格到組織介面的追溯與構念錨點候選 v1.3

**狀態：研究者預先指派的候選 codebook，尚無第二位獨立編碼者、內容效度或 Q-sort。** G01–G16 的 O/E 與 q 值仍只作 V5 的文獻網絡線索，不能當 JPC 觀察或模型係數。20 號檔的 M5/T1 靜態映射已被撤回。

## 1. 指派規則與裁決

主機制按 pair 的可見決策界面而非文獻影響分數指派：M1 是誰有授權／否決與問責；M2 是輸出交接到流程與例外處置；M3 是人／AI 的決策順序、權限與依賴行為；M4 是系統驗證、性能監控與可用的解釋／復原證據。跨界 pair 可以標「橋接」而不強行單選；無對應組織機制的 pair 留在證據層。G04 保留 evidence-only；G11、G12 保留動態學習候選而不進靜態模型；G10 僅在有真實分數／標記資料時作 score-to-choice 附加模組，否則 evidence-only。

兩位以上編碼者須在未看到本表建議 M 值的情況下，依同一 codebook 獨立對 16 格作 `主 M／次 M／排除與理由`，再記逐格一致、分歧裁決與適當的一致性區間；沒有這一程序就不能稱為「文獻三角驗證」。以下對應只是供反駁的**待審提案**，不是已完成獨立指派。

| G 格及 pair 摘要 | 候選 M／狀態 | JPC 介面 | 題號 | 模型符號／用途 | 識別狀態 |
|---|---|---|---|---|---|
| G01 Human augmentation × prediction | M3 | Manager→Junior | C3,C7,C8 | `m,ρ,P` | 行為待觀察、結果情境 |
| G02 prediction risk × human review | M1 | 治理→JPC、Manager→Junior | C1,C2,C4,C8 | `Allow,H,κ,L` | 權限待核、損失區間 |
| G03 coordination execution × risk | M2 | Manager→Junior | C3,C6a,C8 | `WI,C_op,CapHours` | 流程可編碼、成本區間 |
| G04 generation × prediction | evidence-only | — | — | 無靜態係數；year 缺失 | 不識別時間趨勢 |
| G05 explanation assurance × allocation | M4（EA-X 候選） | Boss→Manager | C5,C7 | `EA-X,Allow` | 內容效度前未入式 |
| G06 evaluation assessment × prediction | M4 | Manager→Junior | C5,C7 | `EA-V,P` | 評估可描述、效果情境 |
| G07 human augmentation × selection | M3 | Manager→Junior | C3,C8 | `m,ρ` | 行為待觀察 |
| G08 recommendation × human review | M1／M3 橋接 | 治理→JPC、Manager→Junior | C1,C3,C4,C8 | `Allow,m,H,ρ` | 待雙人裁決 |
| G09 prediction risk × governance | M1 | 治理→JPC | C1,C2,C3 | `Γ,Allow,κ` | 正式權限待核 |
| G10 prediction risk × selection | score-to-choice 可選；靜態 evidence-only | Manager→Junior（若啟用） | C7,C8 | `P,ρ`；有 `s,τ,truth` 才增模組 | 無標記資料時不估 |
| G11 evaluation × allocation | 動態 M5 候選 | Boss→Manager（跨期） | — | 無靜態項 | 長期資料缺席 |
| G12 prediction risk × information | 動態 M5 候選 | Manager→Junior（跨期） | — | 無靜態項 | 長期資料缺席 |
| G13 explanation assurance × prediction | M4（EA-X 候選） | Manager→Junior | C5,C7,C8 | `EA-X,ρ` | 內容效度前未入式 |
| G14 prediction risk × general decision | M2／M3 待裁決 | Manager→Junior | C1,C3,C6a | `WI,m` | pair 過寬，待編碼 |
| G15 explanation assurance × selection | M4／M3 橋接 | Manager→Junior | C3,C5,C8 | `EA-X,m,ρ` | 待雙人裁決 |
| G16 coordination execution × human review | M1／M2 橋接 | 治理→JPC、Manager→Junior | C1,C4,C6a | `Allow,H,WI` | 待雙人裁決 |

表中「外部評估 ↔ 內部假設」是**個案校準的交叉質疑介面**，不從任一 G 格機械推導；C2、C7 與公開資料分別對 `B_TWD,κ,L,V` 提供情境挑戰。全漢正式權限與兆豐利益關係尚未查證，不能由此表宣稱外部治理成立。若雙人編碼否決任一 M 的可辯護性，刪除該 M 的理論主張而保留逐格證據；若 M 無題目或模型項，不能列為本研究實測機制。

## 2. 錨點：只對同一功能作序位比較

等級是**累積條件**：達第 k 級必滿足該級及所有較低級的單一核心條件，未滿足則停在較低級；資訊是否足夠、時間是否足夠等控制實效另設二元／區間指標，不能用較高 H 名義等級代替。以下錨點先送 6–8 位跨治理、IT、流程、前線的專家逐項評相關性、清晰度，再做盲 Q-sort；跨構念誤歸的文字須重寫，兩輪試測前不能定稿。

| 構念（唯一職責） | 0 | 1 | 2 | 3 | 分開記錄 |
|---|---|---|---|---|---|
| `D` 共用系統交換能力 | 無可重用的數位交換接口 | 一個共用系統可提供該資料 | 不同流程可穩定調用同一接口 | 共用接口有版本控制 | 範圍是跨 use case 的平台，不是本案 AI 交接 |
| `R` 資料可取得性 | 本案資料無法取得 | 可手工取得 | 可在需要時間內以固定格式取得 | 可依授權重現同一資料抽取 | 品質、合法性、缺漏另設觀測欄，不塞入同一級 |
| `G` 正式決策權 | 無指定決策權人 | 指定責任人 | 書面界定批准／否決權 | 另有明示的授權變更權限 | 誰持權、何時授權，非監控／測試／追蹤 |
| `A_aut` AI 對決定的權限 | 人獨立決定 | AI 僅提供資訊，人自行提出方案 | AI 提案，人保留最後批准 | AI 在已授權邊界內可作最後決定 | 不編碼流程接入；`A_aut_obs` 現況與 `A_cap0` 能力上限分開 |
| `H` 人對單次決定的介入權 | 無介入權 | 可在結果後提出異議 | 可在行動前否決 | 可在執行中止或回復 | 實際看得到資訊與有時間介入各另記 `H_effective` |
| `WI` 本案 AI 輸出路由 | 不進工作流程 | 由人手動轉入下一步 | 由系統送至下一個決策節點 | 由系統送至授權行動節點 | 例外路由／回復能力另記，不和平台 D 混同 |
| `EA-V` 系統驗證證據 | 無驗證記錄 | 上線前有測試記錄 | 運作中有定期性能測量 | 有按觸發條件重驗證記錄 | 測試品質與風險效果另有證據，不屬 G 或 H |
| `EA-X` 解釋可用性（可選） | 無可用理由 | 使用者可閱讀理由 | 使用者能以理由提出可檢驗的查核問題 | 使用者可在盲題中辨出理由何時不足 | Rudin／Miller 在此量測完成前不作 EA 的直接支持 |

`κ` 只按「可逆的局部影響／需跨部門修復／可能造成重大客戶、品質或法規後果」編低／中／高；具體 TWD 損失分表記，不將級別直接乘入風險。D、R、G、A_aut、H、WI、EA-V、EA-X 的錨點均為**待評估操作定義**，不是既有量表；若累積次序在特定任務不成立，分項記錄而不強制給單一等級。Jöhnk 的策略契合、資源、知識與文化另記為情境限制，不假稱已被這些量尺涵蓋。Khatri & Brown 的 governance／management 區分屬 data/IT 領域轉用到 AI 決策，需明示此推論邊界。

## 3. 結果登記

Q-sort 預先登記每張錨點卡及預期構念、各專家歸類、信心水準、誤歸原因；報逐項一致率與可行時的 Krippendorff α 區間，樣本少時保留原始分歧，不以單一 κ 或 80% 門檻冒充效度。之後至少兩輪小規模試測，檢查可回答性、單調性探針、重測一致、訪談負擔、`A_aut_obs/A_cap0` 區別及 H 的實際控制，必要時改錨點與門檻表。
