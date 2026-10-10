# 論文候選稿 v1.5｜緒論、文獻回顧與研究方法

**中文題名：從 AI 建議到組織決策：權限、流程與第一線反應的個案研究及雙層情境模型**

**English title: From AI Recommendations to Organizational Decisions: Decision Rights, Workflow, Frontline Responses, and a Bilevel Scenario Model**

**稿件狀態：研究設計與前三章可投稿編修稿，尚無 JPC 個案結果或模型估計。** 依隨附中文投稿格式作單欄內容編修；定稿排版須 A4、摘要起雙欄、20 頁內及該模板的字型／尺寸規範。本稿不填造作者、摘要結果、樣本數、訪談引語或績效數字。29 是引文主張稽核，30 是變數與驗證協定，31 是試測問卷，25–28 是方程、構念、倫理與兩案候選規格。

## 中文摘要（設計階段）

企業導入 AI 後，預測或建議是否改善決策，取決於誰設定目標與限制、誰設計人機交接，以及執行者在可見資訊和實際權限下如何查核與採納。本研究以 AI × Decision 為主軸，將既有文獻網絡中的低連結議題作為問題線索，提出權責治理、流程交接、人機安排、評估保證四項候選機制，並以單一企業的具名決策事件檢驗其適用性。方法結合文件與角色別訪談、同一案例內控制因素的情境題卡，以及 Boss–Manager 雙層、內嵌第一線條件反應的有限查表模型。變數採有序錨點與來源可追溯的成本、結果區間；對未識別資料拒絕生成點值最適解。研究預計比較集中規劃與分層決策下的可行配置，並報告來源分歧和敏感度。本文目前僅提出可反駁的設計與驗證門檻，不聲稱企業已部署、改善績效或取得因果效果。

**關鍵詞：** 人機決策、決策權、組織流程、AI 治理、雙層模型、情境分析

## Abstract (design-stage)

Whether an AI recommendation improves an organizational decision depends on who sets objectives and constraints, who designs the workflow, and how frontline workers respond to information they can actually see. This study connects AI and decision making by translating prior literature-network gaps into four candidate organizational mechanisms: governance and decision rights, workflow handoffs, human–AI arrangements, and evaluation and assurance. It proposes an embedded case design using role-specific interviews, controlled within-case vignettes, and a finite Boss–Manager bilevel scenario model with conditional frontline responses. Ordinal anchors serve as feasibility keys; outcome and cost lookups require traceable evidence or explicitly bounded scenarios. Missing inputs prevent a point recommendation. The present manuscript specifies the research design and validation gates. It does not report company deployment, estimated effects, or empirical model results.

**Keywords:** human–AI decision making; decision rights; workflow; AI governance; bilevel model; scenario analysis

# 壹、緒論

## 1.1 研究背景與問題

AI 能產生搜尋結果、預測與建議，然而輸出本身不等於組織決策。一項品質問題的相似案例可供工程或品質人員審查；一份職務條件匹配結果也可能只供招募人員查閱。兩種輸出走到正式行動之前，均經過政策授權、流程轉送、人工查核、例外升級及結果驗證。若只量「是否使用 AI」或模型準確率，便難分辨失敗來自技術、決策權、流程接點，還是前線無法有效推翻錯誤建議。

組織決策研究已區分人完全交給 AI、AI 與人依序接力，以及兩者意見聚合等結構（Shrestha et al., 2019）。此分類描述配置，並未替一間企業辨認誰真有批准或中止權。人機績效的系統性回顧亦顯示，組合績效依任務、單獨表現與分工而異，平均值不能直接外推到某個品質或招募流程（Vaccaro et al., 2024）。解釋可能提高對錯誤建議的接受（Bansal et al., 2021）；責任甚至可能落在控制能力有限的操作員身上（Elish, 2019）。這些研究共同指出需要把 AI 輸出與**決策事件**、決策權及實際反應連接起來。上述「共同指出」是本研究的綜合推論，並非文獻已證實本個案存在這些問題。

本研究的前階段 V5 文獻網絡提出 G01–G16 十六個低連結 pair，作為研究問題的候選線索。這些是文獻關係的描述，不能解讀為十六項已發生的公司缺口或效用係數。本稿預先將其置於 M1 權責治理、M2 流程交接、M3 人機決策安排及 M4 評估保證四個可觀察介面，允許雙重映射或排除，並由獨立編碼者盲審。G04 僅監測證據；G11/G12 所指向的跨期學習列為未來 M5，因現有 year 欄位缺失且無縱向組織資料，不從文獻網絡推時間趨勢。

## 1.2 研究目的與問題

本研究目的在具名 use case 中追溯「政策與資源 → 管理設計 → 可見訊號下的第一線反應 → 可定義結果」的鏈條，找出不同角色所說的要求與可觀察流程的差異，並檢驗這些差異如何在明示假設的模型中改變可行選擇。研究問題如下：

1. **RQ1 權限與流程：** 對同一決策事件，正式授權、管理設計與第一線可行的查核、否決、升級行為在哪些介面一致或不一致？
2. **RQ2 條件性反應：** 在固定任務與執行權後，AI 權限、錯誤後果及當下可見訊號的變化，如何對應到各角色的最低安全要求、可行配置及行為反應？本研究描述題卡範圍內的方向和分歧，不估計跨案例人口效果。
3. **RQ3 模型意義：** 在同一來源可追溯的參數區間下，集中規劃與 Boss–Manager 雙層配置何時相同、何時不同？結論對哪些未識別輸入最敏感？

本研究的貢獻預期是可稽核的「文獻線索 → 組織介面 → 題項／證據 → 可行性與結果表」追溯，以及在資料不足時仍可明確拒絕單一最適推薦的決策支援規格。是否真的觀察到分層目標衝突或績效差異，是研究要檢查的命題，不能預寫成發現。

# 貳、文獻回顧與分析架構

## 2.1 從 AI 能力到決策安排

Shrestha 等人（2019）比較人與 AI 在決策搜尋空間、可解釋性、選項數、速度及可複製性上的條件，進而提出完全委託、兩種順序的人機結構與聚合結構。本研究據此要求每一方案記錄誰先判斷、誰能最後批准、AI 是否直接執行、由誰中止或聚合；A_aut 的 A0–A3 是本研究的候選**決策權錨點**，不是原文分類的轉寫。AI 權限相同的兩個方案仍可能因順序、執行與救濟不同而有不同風險與工作量。

Raisch 與 Krakowski（2021）的自動化與增能悖論提醒，兩種用途在管理實務中相互依賴。本文以它作為不強迫流程落入互斥類別的理論理由；其跨期回饋不放入此一靜態模型。Jöhnk 等人（2021）把組織 AI readiness 分成五類、十八項因素，顯示單靠資料和系統能力不足以概括策略契合、知識、文化及管理資源。本研究 D、R、G 專門測量交換、取得與授權；其他 readiness 條件另列脈絡和進案限制，避免用窄量尺宣稱完整成熟度。

## 2.2 人機互補、可見訊號與責任

Vaccaro 等人（2024）對符合人單獨、AI 單獨與組合比較條件的實驗作綜合分析，發現平均組合未勝過較佳單方，且決策任務與內容生成任務的結果不同。其樣本與設計異質性限制了公司層級推論，但足以支持本文在每個案例分列任務類別、基準表現與分工，而不把「加入 AI」當固定收益。Bansal 等人（2021）在三組資料的實驗發現，解釋會提高建議被接受的機會，連錯誤建議亦然。因此 EA-V 的驗證監控與 EA-X 的解釋可用性不能合成一個保證降風險的分數；更需問第一線看到甚麼、能否獨立查核及如何選擇。

Elish（2019）提出自動化下有限控制者可能承擔錯置責任的分析。本研究把正式權責 G 與逐次決策介入 H 分開；H 的名目等級又與可見資訊、反應時間、真實否決或回復能力分開。這提供可查的疑問，而非斷定公司有責任錯置。對 HR 初篩還要把隱私、公平與不得自動淘汰等政策寫成限制，不以假定金額交換基本權利。

## 2.3 文獻網絡線索到可反駁機制

M1 問正式授權、風險政策與覆核權是否匹配；M2 問 AI 輸出到下一個工作節點、例外與回復如何接續；M3 問順序、最終決定權與對建議的接受／查核；M4 問上線前測試、運行監控、重驗證及理由是否真可用。它們是研究者提出的機制代碼，須經雙人獨立指派、內容效度與個案反例才能保留。G01–G16 的逐格候選映射在 26 號表。AI × Decision 在本研究具體指「AI 所供訊號如何進入人的選擇以及誰承擔可控制的後果」，同時要求相對績效與結果資料，避免把資訊產生、採納與正式決策混為一談。

# 參、研究方法

## 3.1 研究設計、範圍與案例進案

採嵌入式單一個案設計，分析單位是一段有可界定輸入、輸出、角色、授權、結果期間與錯誤後果的決策 episode，而非企業整體 AI 成熟度。優先試探兩個尚待核實的垂直切片：8D 品質問題中 AI 輔助證據檢索與方案草稿，以及 HR 履歷條件定位與初篩人工複核。兩者只是候選題卡，並不表示 JPC 已部署。若公司授權、倫理程序、至少兩類角色的權限互證、非敏感流程證據和結果代理均無法達成，該案退為純 vignette，不進實證校準。4–6 個深描案例是工作量規劃，非統計估計的有效樣本數。

資料來源依權限分層：正式且可分享的空白政策／流程記錄、各角色獨立訪談、同一卡內變因控制的反事實回答，以及另行核准的去識別結果代理。外部公開財務和適格專家的意見只挑戰成本／價值情境，不代替內部能力觀察；關係企業的正式權利須逐文件查核，不按身分預設控制。招募與同意、唯一職位可反識別、存取期限和外部分享按 27 號倫理草案補足後才實施；原始訪談不進公開儲存處。

## 3.2 構念、觀察與題卡

D（跨案交換）、R（本案資料取得）、G（正式權限）、A_aut（AI 決定權）、H（人的介入權）、WI（本案路由）、EA-V（驗證證據）分別採 0–3 的候選累積錨點；EA-X 是可選的解釋可用性。κ 僅為低／中／高後果類別。每個錨點只在本構念內比較等級，不作等距加減。現況 A_aut_obs、部署上限 A_cap0、題卡 A_target、模型 A* 分表記，H_obs 與實際控制 H_effective 也分開。最低安全 WI_req 與足以抵銷成本的 value_onset 由不同問題取得。

兩個模板各固定任務、用途及執行權，在同一模板內改 A 和 κ；受訪者按自己的專業角色回答 C1–C9。卡面讓前線只看到行動前訊號 z，例如證據定位、介面提示及可用時間；當時不可見的真實結果 ω 只供事後標記。A3 與「人最後核准」若互斥，登記禁止配置而非要求虛構門檻。重複卡、單調性反例及 C6a/C6b 題序交錯檢查理解與疲勞。任務和執行權與模板仍可能混淆，不能估其獨立主效應。6–8 位跨角色專家先審錨點清晰度和相關性，再盲 Q-sort；兩輪試測報逐格原答、分歧與缺漏，不以小樣本平均為真值。完整試測工具及欄位見 31。

對固定 A_target 定義 Gap_X(i,s)=1[X_obs(i)<Req_X(A_target,s)]，僅在同一錨點且兩端均有證據時使用；同時保存是否現況 A_obs 的落差或推薦 A* 的條件性反事實。Gap 是方向與觸發限制，不是 0–3 數值差或企業損失。沒有觀察值的格維持未識別。

## 3.3 Boss–Manager 雙層與前線反應

Boss 的 b 選資源、政策和授權；Manager 在允許集合 X(b,s) 中選每案 x_i=(A_aut,H,WI,EA-V,m)，m 明列順序、最後權限、執行與回復。前線依角色 role、配置 x、當下可見訊號 z 及情境 s，形成條件行為分布 ρ_i(r|x,z,role,s)，r 可接受、查核、改寫／覆核、升級、拒用。對每個角色的政策禁止反應令機率為零；ρ 和訊號／真值聯合表 P_i(z,ω|x,s) 均需正規化。ω 不作前線回答的條件。沒有可授權行為觀察時，ρ 只作明示區間或情境，不能假裝精確估得。

在共同期間 T，事件數 N_i(T) 乘以每事件的條件期望價值 V_i、企業損失 L_i 及運作成本 C_op,i，扣資本成本 C_cap，構成 Boss 的 TWD／T 情境目標 F_B。Manager 的 F_M 由其可控營運損失 L_oper,i、C_op,i 與實施成本 C_impl 構成，另有品質／服務底線。若經訪談未發現職權或取捨不同，這兩個形式目標不可當作真實偏好衝突。正式式子、期望算子、多解的有利／不利界及限制見 25；本稿不另創未估得的係數。

各構念等級與 κ 只能作門檻或查表鍵。V、L、成本的來源、單位、事件定義、期間和區間逐格登記；不足時先報可行集、分項／Pareto 或 **INSUFFICIENT_IDENTIFIED_INPUTS** 的缺格，不輸出最適金額。非貨幣權利及合規要求保留政策限制，不以任意權重交換。

## 3.4 驗證與分析界線

先做來源／權限、內容效度與兩輪試測，再測資料型別、機率和 one-hot 正規化、跨單位加總及查表缺格。小型合成 fixture 以窮舉核對 Manager 反應、Boss 上層選擇與多解界，再在同一參數下比較集中規劃和雙層結果。預先登記參數區間 Θ_adm 的端點和內部情境，逐決策報 ROBUST、CONDITIONAL、FRAGILE 或 UNIDENTIFIED，並報掃描涵蓋率。這些是**待執行的驗證程序**；v1.0 舊模擬 PASS 並不驗證新方程。若日後要加 Junior argmax 第三層，須同時有獨立可行裁量、不同目標／限制、經理預期反應及同參數反事實改變配置的證據。

完成後本研究最多支持這些案例與界定情境下的配置、門檻分歧和敏感度。小樣本、角色權力關係、代理結果的選擇偏差與缺乏實際人機基準會限制識別；不主張因果、母體參數、產業外推或已實現的最適績效。目前結果章、討論中的實證解釋與結論須等資料與 V0–V7 關卡，不在本稿虛構。

# 參考文獻（本稿實際使用）

Bansal, G., Wu, T., Zhou, J., Fok, R., Nushi, B., Kamar, E., Ribeiro, M. T., & Weld, D. S. (2021). Does the whole exceed its parts? The effect of AI explanations on complementary team performance. *Proceedings of CHI 2021*. https://doi.org/10.1145/3411764.3445717

Elish, M. C. (2019). Moral crumple zones: Cautionary tales in human-robot interaction. *Engaging Science, Technology, and Society, 5*, 40–60. https://doi.org/10.17351/ests2019.260

Jöhnk, J., Weißert, M., & Wyrtki, K. (2021). Ready or not, AI comes—An interview study of organizational AI readiness factors. *Business & Information Systems Engineering, 63*, 5–20. https://doi.org/10.1007/s12599-020-00676-7

Raisch, S., & Krakowski, S. (2021). Artificial intelligence and management: The automation–augmentation paradox. *Academy of Management Review, 46*(1), 192–210. https://doi.org/10.5465/amr.2018.0072

Shrestha, Y. R., Ben-Menahem, S. M., & von Krogh, G. (2019). Organizational decision-making structures in the age of artificial intelligence. *California Management Review*. https://doi.org/10.1177/0008125619862257

Vaccaro, M., Almaatouq, A., & Malone, T. (2024). When combinations of humans and AI are useful: A systematic review and meta-analysis. *Nature Human Behaviour, 8*, 2293–2303. https://doi.org/10.1038/s41562-024-02024-1
