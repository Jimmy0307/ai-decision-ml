# S1C — 編碼手冊（S1b 編碼手冊 + 語意忠實度修補）

**僅供研究團隊。** 未在此列出的部分與 `claude/r14_merge_v1_8_2b_v1_s1b_zh_tw/S1B_CODEBOOK.md` 完全相同（並由差異關卡證明）。語意權威為 26（`claude/r14_merge_v1_8_2_v1_prefreeze/26_V1_FINAL_CODEBOOK_v1_8_2.md`）。標準代碼、下拉標籤、標籤對照不變。

## 1. 修補後的類別文字（編碼者看到的，逐字）

| 代碼 | 顯示標籤 | 定義 | 區分說明 |
|---|---|---|---|
| `M1` | M1｜權責與問責 | 此組合的主要議題是：誰可以核准、拒絕、停止，或改變 AI 輸出被允許作出的決策。包括正式控制與實際控制、問責，以及企業政策所設定的權限邊界。 | 若主要議題是 AI 輸出如何進入後續流程，選 M2。若主要議題是人與 AI 如何分工或回應，選 M3。若主要議題是如何確認 AI 輸出是否適合用於該項決策，選 M4。 |
| `M2` | M2｜流程路由與異常復原 | 此組合的主要議題是：AI 輸出如何進入下一個決策或行動步驟。包括跨系統或單位的交接、例外處理、回復與復原。 | 若主要議題是誰具有正式決策權限，選 M1。若主要議題是人與 AI 的工作分工與互動，選 M3。 |
| `M3` | M3｜人機配置與回應 | 此組合的主要議題是：人與 AI 的工作順序與分工，以及使用者如何回應 AI 輸出。例如：誰提出建議、誰做最後決定、如何委派或覆寫，以及使用者是否使用、驗證、修改、升級處理、拒絕或繞過 AI 輸出。 | 若主要議題是正式決策權限與問責，選 M1。若主要議題是流程如何轉交、升級或復原，選 M2。若主要議題是 AI 是否經過充分驗證、監控或保證，選 M4。 |
| `M4` | M4｜評估與保證 | 此組合的主要議題是：如何確認 AI 輸出適合被用於該項決策。包括：部署前驗證、持續監控、重新驗證、可稽核性、解釋是否足以供決策使用、漂移監測，以及其他能證明 AI 輸出適用於該決策的證據。 | 若主要議題是誰有權決定或誰負責，選 M1。若主要議題是人與 AI 如何分工與回應，選 M3。 |
| `EVIDENCE_ONLY` | 僅屬證據層 | 這個配對只呈現研究、技術、資訊或證據上的關係，但沒有形成這個配對所特有的企業決策介面。如果你能想到的問題，是幾乎任何 AI 功能進入這類決策功能時都會同樣遇到的一般性問題，也屬於此類。 | （S1b 原文，不變）Q1＝否時，Q2 請選此類別；Q1＝無法確定時也可選。Q1＝是時不可選。若有某一類別明顯適用，表示已形成決策介面，請改選該類別。 |

「判斷對象」規則（修補後）：「請判斷企業決策本身，而不是技術、文獻主題，或功能類型名稱與類別名稱之間碰巧相同的字詞。部分功能類型名稱與類別名稱有相同的字詞（例如：問責、流程、人機、配置、評估、保證）。功能類型名稱與機制類別有相同或相近字詞時，不得只因字詞相同就選擇該類別。」

作答聲明表頭（修補後）：「作答聲明：請逐條閱讀下列敘述，並從下拉選單選擇「符合」（這句敘述與你的實際情況相符）或「不符合」（這句敘述與你的實際情況不符）。請如實回答。若有任何一項選擇『不符合』，研究團隊會依預先設定的規則將該份作答標記並分開分析，不會在未標示的情況下與其他編碼者的主要信度分析合併。」

作答聲明第 1 條（修補後）：「在作答前與作答期間，我沒有另外查閱與本研究內容相關的外部資料；我的判斷只依據本問卷提供的內容。」第 2–7 條不變。

## 2. 忠實度檢查（S1c 中文 vs 26 §3 英文）

| 類別 | 26 英文要素 | S1c 對應 | 結果 |
|---|---|---|---|
| M1 | who may approve, reject, stop or change what the AI output is allowed to decide；formal vs effective control；accountability；enterprise policy boundaries；不用於 routed / technically validated | 核准、拒絕、停止或改變 AI 輸出被允許作出的決策；正式控制與實際控制；問責；企業政策所設定的權限邊界；區分：流程 → M2、確認適用 → M4（另加 → M3，與 26 M3「not formal authority」互為對稱） | PASS |
| M2 | how the AI output enters the next decision or action step；handoffs across systems or units；exception handling；rollback and recovery；不用於 who holds authority | 全部對應（回復與復原＝rollback and recovery）；區分：權限 → M1（另加 → M3） | PASS |
| M3 | sequence and division of work (who proposes, who decides, aggregation, delegation, override)；users respond (use, verify, modify, escalate, reject, bypass)；不用於 formal authority / validation evidence | 工作順序與分工；誰提出建議、誰做最後決定、委派、覆寫；使用、驗證、修改、升級處理、拒絕、繞過；區分：權限與問責 → M1、驗證 → M4（另加流程 → M2） | PASS_WITH_NOTE：「aggregation」（彙整）未出現在例子中；文字以「例如」列舉，構念不變 |
| M4 | pre-deployment validation, monitoring, revalidation, auditability, explanation usability, drift, evidence that the AI output is fit for the decision；不用於 who decides / how work is sequenced | 部署前驗證、持續監控、重新驗證、可稽核性、解釋是否足以供決策使用、漂移監測、適用證據；區分：誰決定或負責 → M1、分工與回應 → M3；不含「風險」 | PASS |
| EVIDENCE_ONLY | pairing describes a research or technology pattern but implies no distinct enterprise decision beyond what any AI function feeding this decision function would raise | 只呈現研究、技術、資訊或證據上的關係，沒有這個配對特有的企業決策介面；一般性問題也屬此類（＝非特定性準則） | PASS |

**與 S1b 語意變更紀錄的關係：** S1b 的 C-2（M1）、C-3（M2）、C-4（M3）、C-5（M4）、C-8（EVIDENCE_ONLY）在 S1c 中回到 26 的意義。S1b 的 C-6（跨時間學習與適應）、C-7（資料條件限制）、C-10（無法明確判定納入「證據不足」）依指示**不變**，仍是相對 26 的已核准語意變更（見 §4）。

## 3. 規則核對（未改，僅確認）

| 規則 | 26 §2 | S1b／S1c 編碼者文字 | 結果 |
|---|---|---|---|
| Q1＝否 | Q2 = EVIDENCE_ONLY | Q2 請選「僅屬證據層」 | 一致 |
| Q1＝是 | Q2 ∈ {M1–M4, LONGITUDINAL, DATA_GATED, NONE, AMBIGUOUS} | 不可選「僅屬證據層」 | 一致 |
| Q1＝無法確定 | 除 NONE 外任一 | 可選「無適用機制」以外任一（含僅屬證據層） | 一致 |
| NONE | Q1＝是＋Q5；不用於證據不足、兩類並列、無介面 | 同（S1b 文字） | 一致；coordinator 列出的「看不懂」未在文字中明列，屬省略而非衝突，未修改 |
| AMBIGUOUS | 兩類以上同樣合適或無法擇一 | 證據不足、兩類以上同樣合理、無法可靠指定單一主要機制 | S1b 已核准的 C-10 擴充，不變 |

**結論：** 沒有發現 coordinator 指定規則與凍結 S1 規則之間的衝突；邏輯未變。

## 4. 殘餘事項（記錄）

- 26 與 S1b／S1c 之間仍有三項已核准的語意差異：跨時間學習與適應、資料條件限制、無法明確判定（S1b C-6、C-7、C-10）。依 S1c 指示不在本次處理。
- 作答聲明第 1 條（外部資料、只依據本問卷）與第 2 條（論文或研究報告）、第 6 條（完全依靠自己的判斷）內容部分重疊但無矛盾；未修改其他條。
