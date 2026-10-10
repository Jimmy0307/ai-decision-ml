# AI 輔助決策如何產生可衡量價值？製造業 8D 與 HR 初篩之多層治理與情境成本效益模型

## How Can AI-Assisted Decisions Create Measurable Value? A Multilevel Governance and Scenario Cost–Benefit Model for Manufacturing 8D and HR Screening

廖睿豪

國立臺灣科技大學科技管理研究所

## 摘要

企業導入人工智慧（AI）時，常以「自動化程度」或模型準確度代替投資價值，卻忽略一項更根本的問題：AI 建議經由哪些角色、權限與覆核機制，才轉化為可觀察的流程結果？本文以單一企業個案之研究設計為主軸，選取製造業 8D 問題處理與人力資源（HR）履歷初篩兩個垂直流程，提出 Boss–Manager 雙層配置、Junior 行為反應分布，以及不依賴虛構收益的情境成本效益模型。當企業尚無 AI 上線後的收益、成本與品質結果時，本文先以基準工時、完整人力成本、採用率、覆核與例外處理成本估算可實現的人力節省；第三方研究只提供節省率範圍，不視為企業本身的實證效果。外部現場研究顯示生成式 AI 對客服人員的平均生產力增幅約 15%，受控寫作任務的時間降幅約 37%，但任務、技能與品質風險具有顯著異質性。以採用率 70%、完整時薪 NT$350 的示例計算，每 1,000 小時基準工時在 10%、15% 與 37% 節省率下，年度人力價值分別為 NT$24,500、36,750 與 90,650；若年度化總成本為 NT$120,000，15% 情境的損益兩平基準工時為 3,265 小時。上述數字皆為情境分析，不是 JPC 的已實現效益。本文的主要貢獻是建立可稽核的估值順序：先界定決策事件與角色權限，再量測工時與行為，最後才計算財務結果；品質、客訴、公平與法遵效益在未取得授權資料前一律不貨幣化。

**關鍵字：** 人工智慧；決策支援；多層治理；成本效益；8D；人力資源

## Abstract

Organizations often evaluate artificial intelligence (AI) adoption through automation levels or model accuracy while overlooking the organizational pathway through which AI recommendations become observable outcomes. This study develops a formal research design for a single-firm case and focuses on two vertical use cases: manufacturing 8D problem solving and human-resource résumé screening. The proposed framework combines a Boss–Manager bilevel configuration model, role-specific Junior response distributions, and a scenario-based cost–benefit model that does not require fabricated revenue or quality benefits. When post-adoption outcome data are unavailable, realized labor value is estimated from baseline task hours, fully loaded labor costs, adoption rates, review effort, and exception-handling effort. External studies supply only plausible productivity ranges and are not treated as evidence of firm-specific impact. A field study of 5,172 customer-support agents reports an average productivity increase of approximately 15%, whereas a controlled experiment on professional writing tasks reports a time reduction of approximately 37%; both studies also indicate substantial task and worker heterogeneity. Under an illustrative 70% adoption rate and a fully loaded hourly cost of NT$350, every 1,000 baseline hours generate labor values of NT$24,500, NT$36,750, and NT$90,650 at savings rates of 10%, 15%, and 37%, respectively. If annualized total cost is NT$120,000, the break-even baseline workload under the 15% scenario is 3,265 hours. These are sensitivity results, not realized JPC outcomes. The contribution is an auditable valuation sequence: define decision episodes and rights, measure labor and behavior, and only then estimate financial effects. Quality, customer, fairness, and compliance benefits remain non-monetized until authorized outcome data are available.

**Keywords:** artificial intelligence; decision support; multilevel governance; cost–benefit analysis; 8D; human resources

# 壹、緒論

生成式 AI 使企業能以較低邊際成本產生摘要、分類、建議與草稿，但「工具能產生輸出」不等於「組織已獲得價值」。價值必須通過具名的決策事件：誰看見 AI 訊號、誰能修改或否決、誰承擔最終決定、錯誤如何被發現，以及節省的時間是否真正被移轉至其他工作。若只以模型能力或一次性模擬結果推論投資報酬，容易同時高估收益、低估覆核與治理成本，也無法解釋管理層與第一線使用行為的落差。

本研究聚焦 JPC 單一個案的校準與決策支援，不把研究寫成外部創投報告，也不主張企業已導入或驗證本文所述 AI。研究選擇兩個可被具體觀察的垂直流程。第一個是 8D 問題處理，AI 可協助檢索相似案件、定位證據、整理根因候選與改善方案草稿；第二個是 HR 履歷初篩，AI 可協助職缺條件比對、原文定位與待人工複核名單形成。兩案皆保留人工決策責任：8D 不讓 AI 自動核准或執行矯正措施，HR 不讓 AI 自動淘汰或決定錄用。

目前最重要的資料限制，是尚未取得足以估算兩套流程實際收益、成本與品質效果的授權資料。因此本文不再用單次校準或合成求解結果填補空缺，而改採「可換入企業資料」的正式情境模型。研究問題如下：

1. Boss、Manager 與 Junior 之間的權限、可見訊號與行為反應，如何影響 AI 建議能否轉化為可衡量流程價值？
2. 在缺乏企業實際收益資料時，如何以人力節省、導入與維運成本、以及第三方實證範圍建立不誤導的投資判斷？
3. 8D 與 HR 兩個流程應蒐集哪些最小資料，才能由情境分析升級為可驗證的企業內效果估計？

本文先回顧 AI 決策配置、人機協作與組織準備度研究，再提出角色治理與情境成本效益模型；其後以現有文獻語料與人工稽核說明證據限制，最後提出兩案的量測方案、決策門檻與可檢驗命題。

# 貳、文獻回顧與研究缺口

## 2.1 AI 決策配置不等同自動化程度

Shrestha、Ben-Menahem 與 von Krogh [1] 指出，組織可採完全委託、AI 與人依序決策或意見聚合等不同結構。此分類的重點不是介面是否使用 AI，而是搜尋空間、速度、可解釋性、選項規模與最終權限如何分配。對企業流程而言，兩個看似相同的「AI 輔助」方案，可能因核准者、否決權與例外路由不同而產生完全不同的風險與工作量。

Raisch 與 Krakowski [2] 進一步說明自動化與增能並非可永久切割的互斥選項；同一系統可能在某一步驟取代人工，又在另一階段增加判斷、協調或監督負擔。因此，本研究不把 AI 權限等級直接換算成效益，而要求逐案記錄工作流、執行權與實際人工工時。

## 2.2 人機組合不保證優於人或 AI 單獨工作

Vaccaro、Almaatouq 與 Malone [3] 對 106 項實驗、370 個效果量進行綜合分析，結果顯示人機組合平均未必超過人或 AI 單獨工作中較佳的一方，且決策任務、內容生成任務、相對基準能力與分工方式會改變結果。這表示第三方研究可協助設定敏感度範圍，卻不能直接當成 JPC 的收益率。

Bansal 等人 [4] 的實驗亦顯示，解釋可能提高使用者接受 AI 建議的機率，包括接受錯誤建議。因而「有解釋」與「有驗證」不能合併成單一品質分數。8D 與 HR 使用者必須能看見來源、回到原始證據、修改輸出，並在資訊不足時回到既有流程。

## 2.3 權責、有效控制與組織準備度

Elish [5] 以 moral crumple zone 說明，在複雜自動化系統中，控制能力有限的操作員可能承擔不相稱責任。本文因此區分名目上的人工介入權與「有效控制」：使用者是否在行動前取得足夠資訊、是否有時間查核，以及是否真正具備否決、停止或復原權。

Jöhnk、Weißert 與 Wyrtki [6] 將組織 AI 準備度整理為五類、十八項因素，涵蓋策略、資源、知識、文化與資料等條件。本文只針對決策權、工作流、資料可得性與驗證機制建立窄模型，不宣稱涵蓋完整 AI 成熟度。

## 2.4 外部生產力研究的可用範圍

Brynjolfsson、Li 與 Raymond [7] 研究 5,172 名客服人員在生成式 AI 助理導入前後的表現，平均每小時解決案件數提高約 15%，但效益主要集中於較缺乏經驗或技能的人員；高技能者的品質可能沒有改善。Noy 與 Zhang [8] 在 444 名大專以上專業工作者的寫作任務實驗中，處理時間由控制組平均 27 分鐘降至 17 分鐘，約減少 37%，且品質提高；然而其任務是短期、界線明確的寫作活動，缺少企業脈絡與長期例外成本。

上述兩項研究提供三個可用資訊。第一，AI 的時間效益可以存在；第二，效果依工作者與任務而異；第三，外部效果不能取代企業自身的基準工時與品質資料。因此本文採 10% 作保守壓力測試、15% 作外部現場參考、37% 作寫作型任務上限敏感度；三者都不是 JPC 的估計係數。

## 2.5 研究缺口

既有研究分別討論決策配置、人機績效、組織準備度與工具生產力，但企業投資決策仍缺少一個可將四者連接的可稽核方法：先定義一次決策事件與權限，再測量實際工時、覆核、例外與採用行為，最後才計算財務價值。本文以 Boss–Manager–Junior 的角色結構與兩個垂直案例補足此一缺口。

# 參、研究設計與方法

## 3.1 研究邊界與證據層級

本研究採單一個案、雙流程垂直切片。JPC 為主要校準場域；全漢的關係企業／董事角色與兆豐創投的外部評估觀點，僅在後續取得授權訪談時作治理或外部觀點，不被當作 JPC 內部營運資料。

證據分為三層。第一層為外部已發表研究，用於界定理論與節省率範圍；第二層為現有研究語料與人工稽核，用於判斷結構洞與分類結果的可靠程度；第三層為 JPC 授權資料，包括流程文件、角色權限、基準工時、實際使用紀錄與結果。只有第三層能支持 JPC 的企業內估值，前兩層不能取代它。

## 3.2 分析單位：決策事件

每筆分析以一個可重建的 decision episode 為單位，至少包含：案件開始與結束、任務類型、AI 輸出、當時可見訊號、參與角色、最後執行權、人工行為、工時、例外與結果。真實結果若只有事後才知道，不得出現在第一線使用者的情境題卡中。

8D 案例從證據彙整與根因候選形成開始，至改善措施核准與有效性確認為止。HR 案例從職缺條件形成與履歷檢索開始，至人工決定是否進入下一階段為止。兩案皆以「AI 提供資訊或方案、人保留最後決定」作主要試點範圍。

## 3.3 角色與權限模型

Boss 設定資源、政策與不可違反的授權邊界；Manager 選擇流程配置，包括 AI 權限、人工覆核、工作流接入與驗證機制；Junior 代表實際操作的角色群，其反應不是預設的效用最大化結果，而是依可見訊號與角色形成條件分布。

令方案為 x=(A,H,WI,EA,m)：A 表示 AI 在決策中的權限；H 表示人工介入與否決；WI 表示工作流接入與例外路由；EA 表示測試、監控與重驗證；m 表示人與 AI 的順序或聚合方式。A、H、WI、EA 皆先作有文字錨點的序位類別，只能用於同一構念的門檻比較，不得直接相加或乘上金額。

Junior 在方案 x、可見訊號 z、角色 g 與案例 s 下的反應分布寫為：

ρ(r | x,z,g,s)，r∈{採用、查核、修改、升級、拒用／回原流程}。　(1)

若沒有足夠觀察，ρ 只以原始次數或區間呈現，不強行估計精確機率。只有當 Junior 有獨立裁量、不同目標或限制、且其反應會反事實地改變 Manager 的選擇時，才把模型擴充為三層。

## 3.4 人力節省與成本模型

對流程 i，令 N_i 為年度事件數，t0_i 為每件事件的基準人工時數，tAI_i 為使用 AI 後的操作時間，tv_i 為人工覆核時間，p_i 為例外機率，te_i 為每次例外的額外處理時間。可實現節省工時為：

Hsave_i=N_i×max{0,t0_i−tAI_i−tv_i−p_i×te_i}。　(2)

若尚無導入後觀察值，只能以外部節省率 s 與實際採用率 u 作情境估計：

Hsave_i^scenario=H0_i×s×u，其中 H0_i=N_i×t0_i。　(3)

角色 r 的完整時薪 c_r 應由年度固定薪資、雇主負擔的保險與退休金、可歸屬福利及有效工時估算；2026 年臺灣最低時薪 NT$196 [9] 僅作法律下限檢查，不代表品質、工程或 HR 專業人員的完整成本。

年度人力價值為：

Blabor=Σ_iΣ_r Hsave_ir×c_r。　(4)

一次性導入成本 C0 包括需求定義、資料整理、系統整合、測試、教育訓練與治理審查；年度維運成本 C1 包括授權或 API、運算、監控、模型或提示維護、安全與再訓練。若導入成本以 L 年攤提，年度淨效益與 ROI 為：

NB=Blabor+Bquality,verified−C1−C0/L。　(5)

ROI=NB/(C1+C0/L)。　(6)

Bquality,verified 只包含已有事件定義、比較基準與授權資料的品質價值。在目前階段，8D 的重複發生、停線、重工、客訴，以及 HR 的漏選、誤選、招募週期、公平與隱私效益全部設為「未識別」，不是設為零。為避免把未知品質效益包進投資建議，本文情境試算令 Bquality,verified=0。

在純人力價值下，年度化總成本 Cannual=C1+C0/L 的損益兩平基準工時為：

H0,BE=Cannual/(s×u×c)。　(7)

## 3.5 兩個 use case 的最小量測表

| 流程 | 基準工時 H0 的量測 | 導入後新增時間 | 不先貨幣化的品質結果 | 決策與資料限制 |
|---|---|---|---|---|
| 8D | 每案證據蒐集、相似案例檢索、根因草擬、會議與報告整理工時；依案件嚴重度分層 | 來源查核、人工修改、升級、錯誤建議回復、監控與重驗證 | 重複發生、圍堵時間、重工、客訴、措施有效性 | AI 不自動核准／執行；客戶、產品與製程敏感資料不得進公開資料庫 |
| HR | 每職缺條件整理、每份履歷檢視、初篩名單形成、人工複核與溝通工時 | 原文查核、條件修正、例外人工複核、稽核與公平檢查 | 漏選／誤選代理、招募週期、候選人體驗、公平、隱私 | AI 不自動淘汰或錄用；個資與個人決策紀錄不進公開 repo |

## 3.6 外部基準與使用規則

| 基準 | 原始研究 | 可用數字 | 本文用途 | 不可外推事項 |
|---|---|---:|---|---|
| 保守壓力測試 | 本文設定 | 10% 時間節省 | 檢查較低效益下是否仍能損益兩平 | 不是研究估計，也不是 JPC 預測 |
| 企業現場參考 | Brynjolfsson et al. [7] | 平均生產力 +15%；n=5,172 | 中央情境節省率 | 客服案件不等於 8D 或 HR；熟練者效果較小 |
| 界線明確寫作任務 | Noy & Zhang [8] | 27→17 分鐘，約 -37%；n=444 | 高情境敏感度 | 短期寫作任務不含企業資料、法遵與長期維運 |
| 人力成本下限 | 中華民國勞動部 [9] | 2026 年 NT$196／小時 | 合法下限與 sanity check | 不代表專業職務完整成本 |

## 3.7 研究程序與識別策略

正式試點分四階段。第一階段以核准文件與兩個不同角色交叉確認 episode、權限與資料邊界；第二階段對每案抽取至少 20–30 個基準事件進行工時研究，案件量足夠時再擴大；第三階段採相同任務的人工作業與 AI 輔助作業比較，至少記錄工時、覆核、例外與品質代理；第四階段才估計式 (2)–(7)，並依角色、案件難度與期間報告不確定性。

若不能隨機分派，至少採同一人員交叉、相近案件配對或分階段導入，並記錄案件難度與學習曲線。問卷用於解釋採用、信任、查核與升級行為，不能取代系統工時紀錄或成為 ROI 的唯一資料。

# 肆、前期證據與情境分析結果

## 4.1 文獻語料與人工稽核對主張強度的限制

既有研究資料庫包含 2,003 篇文獻與 27 個核心概念，可用於描述 AI 與決策研究的主題結構。然而，後續人工稽核顯示分類結果仍需保守使用：第一位編碼者完成 50 筆，第二位編碼者對其中 20 筆進行盲編，19 筆分歧完成裁決。裁決前 20 筆的精確一致率分別為證據有效性 75%、關係類型 35%、AI 功能家族 20%、決策功能家族 20%、分析納入 60%；Cohen's κ 分別為 0.561、0.180、0.048、0.140 與 0.316。這些指標僅為 n=20 的探索性結果。

相較人工標記，模型在 50 筆目標稽核中的關係、AI 家族與決策家族精確一致率為 28%、38% 與 18%；在 20 筆裁決子樣本中為 15%、35% 與 35%。局部 sidecar 修正改變 120 個主表格中的 24 個計數與 3 個方向；核心集合數仍為 32，但有一格加入、一格移出。因此，現有文獻網路可作研究問題與量測設計的來源，不能把「完全自動化分類已驗證」或特定 32 格核心已經人工確認寫成最終實證結論。

## 4.2 每 1,000 基準工時的人力價值

為使不同流程可在尚無案件量時比較，本文先以每 1,000 小時基準工時為單位，假設實際採用率 u=70%。NT$196 為法定下限；NT$350 與 NT$500 是用於敏感度的完整時薪情境，必須由 JPC 實際薪資與雇主負擔替換。

| 節省率 s | 可實現節省工時（u=70%） | c=NT$196 | c=NT$350 | c=NT$500 |
|---:|---:|---:|---:|---:|
| 10% | 70 小時 | NT$13,720 | NT$24,500 | NT$35,000 |
| 15% | 105 小時 | NT$20,580 | NT$36,750 | NT$52,500 |
| 37% | 259 小時 | NT$50,764 | NT$90,650 | NT$129,500 |

此表揭示一項容易被忽略的結論：對低案件量流程，即使 AI 能節省 15% 時間，僅靠人力節省也未必足以支付整合、授權與治理成本。企業必須先知道 8D 與 HR 的年度基準工時，不能從「AI 看起來更快」直接跳到正 ROI。

## 4.3 損益兩平分析

以下以年度化總成本 Cannual=NT$120,000、完整時薪 c=NT$350、採用率 u=70% 作純情境示例。

| 節省率 s | 損益兩平基準工時 H0,BE | 意義 |
|---:|---:|---|
| 10% | 4,898 小時／年 | 保守情境需很高工作量才回本 |
| 15% | 3,265 小時／年 | 現場研究參考下的中央門檻 |
| 37% | 1,324 小時／年 | 僅適合作高效、界線明確任務之上限測試 |

在 15% 節省率下，不同年度基準工時的結果如下：

| 8D+HR 合計基準工時 | 年度人力價值 | 扣除 NT$120,000 後淨效益 | ROI |
|---:|---:|---:|---:|
| 1,500 小時 | NT$55,125 | -NT$64,875 | -54.1% |
| 4,000 小時 | NT$147,000 | NT$27,000 | 22.5% |
| 6,000 小時 | NT$220,500 | NT$100,500 | 83.8% |

這不是 JPC 的投資試算，而是決策門檻示範。JPC 只需替換四個值——基準工時、完整時薪、實際採用率與年度化成本——即可得到第一版可辯護的財務範圍。若結果接近損益兩平，再投入品質效益量測；若在保守與中央情境下均明顯為負，應先縮小整合範圍或降低固定成本，而非用未經驗證的品質金額美化結果。

## 4.4 8D 與 HR 的價值形成路徑

8D 最可能先產生價值的活動，是跨文件證據定位、相似案例檢索與報告草稿，而不是根因或措施的自動核准。其基準工時必須依案件嚴重度分層，因一般內部問題與客戶／安全相關事件的覆核強度不同。若 AI 讓第一線更快產生草稿，卻增加 Manager 查證與重開案件的時間，式 (2) 會直接扣除新增工作。

HR 最可能先產生價值的活動，是在人工可回看原履歷的前提下進行條件比對與證據定位。價值不以「自動淘汰多少人」衡量，而以每份履歷或每個職缺的淨節省時間、人工推翻率、需補資料比例及例外工時衡量。任何涉及敏感屬性、公平或個資的風險先作不可違反限制，不以低人力成本交換。

# 伍、討論

## 5.1 對 JPC 投資決策的直接含義

第一，現在不能回答「8D 或 HR 系統各自會賺多少」，因為缺少年度事件數、基準工時、導入後工時與完整成本；但已能回答「在何種工作量與成本下可能回本」。這比以合成參數報單一 ROI 更誠實，也更有決策價值。

第二，兩案應先採 A1–A2 的輔助模式：AI 定位資訊或提出草案，人員保留最後批准。只有在高頻、低後果、例外率低且監控充分的子任務，才討論更高自動化。這不是因為人工一定較準確，而是目前沒有足夠證據把錯誤成本與修復能力量化。

第三，Junior 的行為是收益能否實現的中介。若第一線因信任不足而完全不用系統，採用率 u 下降；若因解釋介面而過度接受錯誤建議，覆核或品質成本上升。Boss 與 Manager 的決策模型不能把 u、覆核時間與例外率當作固定常數，應由試點資料分角色估計。

## 5.2 管理機制與 gap 的追溯

若流程文件無法指出誰有最後決定權，對應的管理機制是權責釐清；若 AI 輸出無法回到原始證據，對應的是資料／工作流交接；若人工只能名義上覆核而沒有時間或否決權，對應的是有效介入；若使用後沒有錯誤監控與重驗證觸發，對應的是評估保證。這些 gap 必須連到具體工作流控制，而不是累加成一個抽象成熟度分數。

## 5.3 研究貢獻

理論上，本文將人機決策配置與多層組織權限連接，並把第一線反應分布納入 Manager 的流程選擇。方法上，本文把外部生產力研究降格為敏感度輸入，而將企業基準工時與實際採用行為置於估值核心。實務上，本文提供可直接填數的損益兩平式，讓管理層在品質效益尚未可得時，仍能以純人力價值判斷是否值得啟動小型試點。

## 5.4 限制

本文尚未取得 JPC 的授權工時、導入成本與品質結果，因此所有金額皆為情境而非實證。外部研究的客服與寫作任務不等同 8D 或 HR，37% 不應作為預算承諾。既有文獻分類人工稽核樣本有限，且局部修正曾改變核心成員，故結構洞結果仍需完整重分析。最後，單一個案即使完成量測，也只能支持 JPC 內部決策，不應直接外推至其他公司或產業。

# 陸、結論與下一步

本文提出一個可在資料不完整時仍保持誠實的 AI 投資評估方法。正式順序是：界定決策事件與角色權限、量測基準工時、記錄 AI 後工時與例外、估計實際採用率、計入完整導入與維運成本，最後才計算 ROI。以每 1,000 基準工時的情境結果可知，若節省率為 15%、採用率為 70%、完整時薪為 NT$350，人力價值僅 NT$36,750；因此案件量、整合成本與覆核負擔是決定是否回本的核心，而不是 AI 模型能力本身。

下一階段應直接執行兩個小型 time study。8D 依案件嚴重度選取去識別事件，HR 使用去識別或合成履歷；各案先取得 20–30 筆基準與 AI 輔助流程資料，紀錄角色工時、採用、修改、升級、例外及品質代理。正式訪談與試點前需完成倫理、同意、資料治理與權限核准。只有當 V0 來源／權限、V1 內容效度、V2 試測、V3 型別與單位、V4 查表完整性、V5 求解器、V6 敏感度與 V7 實務校準逐項有證據時，才可將情境參數改寫為 JPC 的實證估計。

# 參考文獻

[1] Shrestha, Y. R., Ben-Menahem, S. M., & von Krogh, G. (2019). Organizational decision-making structures in the age of artificial intelligence. *California Management Review*. https://doi.org/10.1177/0008125619862257

[2] Raisch, S., & Krakowski, S. (2021). Artificial intelligence and management: The automation–augmentation paradox. *Academy of Management Review, 46*(1), 192–210. https://doi.org/10.5465/amr.2018.0072

[3] Vaccaro, M., Almaatouq, A., & Malone, T. W. (2024). When combinations of humans and AI are useful: A systematic review and meta-analysis. *Nature Human Behaviour, 8*, 2293–2303. https://doi.org/10.1038/s41562-024-02024-1

[4] Bansal, G., Wu, T., Zhou, J., Fok, R., Nushi, B., Kamar, E., Ribeiro, M. T., & Weld, D. S. (2021). Does the whole exceed its parts? The effect of AI explanations on complementary team performance. *Proceedings of the 2021 CHI Conference on Human Factors in Computing Systems*. https://doi.org/10.1145/3411764.3445717

[5] Elish, M. C. (2019). Moral crumple zones: Cautionary tales in human–robot interaction. *Engaging Science, Technology, and Society, 5*, 40–60. https://doi.org/10.17351/ests2019.260

[6] Jöhnk, J., Weißert, M., & Wyrtki, K. (2021). Ready or not, AI comes—An interview study of organizational AI readiness factors. *Business & Information Systems Engineering, 63*, 5–20. https://doi.org/10.1007/s12599-020-00676-7

[7] Brynjolfsson, E., Li, D., & Raymond, L. R. (2025). Generative AI at work. *The Quarterly Journal of Economics, 140*(2), 889–942. https://doi.org/10.1093/qje/qjae044

[8] Noy, S., & Zhang, W. (2023). Experimental evidence on the productivity effects of generative artificial intelligence. *Science, 381*(6654), 187–192. https://doi.org/10.1126/science.adh2586

[9] Ministry of Labor, Republic of China (Taiwan). (2025). Starting on January 1, 2026, monthly minimum wage to be increased to NT$29,500; hourly minimum wage to be increased to NT$196. https://english.mol.gov.tw/21139/40790/87087/

# 附錄 A：JPC 可直接填入的第一版估值欄位

| 欄位 | 8D | HR | 資料來源 | 狀態 |
|---|---:|---:|---|---|
| 年度事件數 N | 待填 | 待填 | 系統彙總／核准報表 | 未識別 |
| 每件基準工時 t0 | 待填 | 待填 | 20–30 件 time study | 未識別 |
| AI 操作時間 tAI | 待填 | 待填 | 試點系統紀錄 | 未識別 |
| 人工覆核時間 tv | 待填 | 待填 | 試點系統紀錄 | 未識別 |
| 例外率 p／例外工時 te | 待填 | 待填 | 例外隊列與工時 | 未識別 |
| 角色完整時薪 c | 待填 | 待填 | 財會／HR 核准計算 | 未識別 |
| 實際採用率 u | 待填 | 待填 | 使用紀錄；分角色 | 未識別 |
| 一次性導入成本 C0 | 待填 | 待填 | 專案工時、採購、整合 | 未識別 |
| 年度維運成本 C1 | 待填 | 待填 | 授權、API、維護、監控 | 未識別 |
| 品質效益 | 不貨幣化 | 不貨幣化 | 待授權結果資料 | 未識別 |

**版本狀態：** 正式文章候選 v1.7。本文已將「外部基準」「情境假設」與「JPC 實證」分層；在附錄 A 欄位完成前，不得將情境試算寫成 JPC 已實現收益或模型已驗證。
