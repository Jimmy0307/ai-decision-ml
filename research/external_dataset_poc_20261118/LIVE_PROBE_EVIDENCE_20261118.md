# 實際 GitHub Runner 外部資料測試｜2026-11-18

**Executor:** GitHub Actions (ubuntu-latest, Python 3.11)
**Run:** https://github.com/Jimmy0307/ai-decision-ml/actions/runs/44262625197
**Latest tested commit:** `15e8c711fbb4ae5ec3e97b6ca2bb5a5cc1f3fc19`
**Verdict:** 兩個 CI jobs 成功；18/18 deterministic unit tests PASS；5 個公開來源完成小樣本取得／6 個候選中的 SEC 因未提供合法 contact User-Agent 而跳過。**這不是六個資料庫的全量下載或實證完成。**

| 資料來源 | GitHub Actions 實際取得 | 量化結果 | 原始回應 SHA-256（完整性用，不等於版本固定） | 未通過的實證關卡 |
|---|---|---|---|---|
| **CORDIS（SPARQL）** | 是；1 次 LIMIT 24 查詢，7,819 bytes | 24 筆 project↔organisation 關係，21 個 project URI，未限定 H2020/AI | `31d4722d6130e38bd5a39c2945104d5341717e8c22292619ced61e60a3ab8324` | 每 project 至多片段、協作群體／時間窗／跨域標籤與真正的 group broker 尚未確認 |
| **OpenAlex** | 是；1 次 query，159,061 bytes | 8 works／25 authors／14 institutions；8/8 works 有 DOI，無作者清單截斷 | `4911e1a31e7e4540951d29d329f98acbd6b8205c05456570355953d54a76e5ab` | 未與 CORDIS DOI/ROR 匹配；檢索排序會變，**同一 query 不保證同一批作品** |
| **OCDS 真實採購** | 是；UK Find a Tender 1 個 OCDS release package；10,403 bytes | 1 筆 award＋contract 公告，`ocid=ocds-h6vhtk-06a9c4`；**已觀測 tenderers = 0** | `6dc4914f404b3420ebdaef1f9eb44f669e8f59a930996ec9465fa1a47c8e9945` | 無輸家投標資訊，不能做廠商 Nash／成本／均衡；須改用特定時間窗與投標者資料齊全的 publication |
| **OCDS 官方 fictional 範例** | 是；6,252 bytes | 1 buyer／2 tenderers／1 winner／1 award | `c6580073b045ecf2089fc4c932efa8046ebb01f13bf5356924a16720560a1342` | 完全虛構，只能驗證欄位映射 |
| **GLEIF** | 是；2,627 bytes | LEI `5493001KJTIIGC8Y1R12`；API 回傳 direct-parent 與 ultimate-parent **鍵名**，但兩者 `related` 為 null | `ddd0e68ce93df872993d5653b9b3e0eb39c6886867c7875635022d1f4aa65b3d` | 無法確認真實 Level-2 母子公司邊，需另外讀 relationship record / reporting exception |
| **PyPSA-Eur GridKit** | 是；1,039 transformer + 62 DC links，39,405 bytes | 1,096 undirected unique edges；2,061 incident bus IDs；997 components；32 triangles | transformers `cfac9ae6fac75c405232fc70ba6da477866ee791caec81d502c92f4fc33dcbf7`; DC `6cc90094d9e5ac4d67761f6b62c743ee741ec6e714288d550adf67fc8d520d28` | **未包含 AC lines.csv**；2022 非官方推導地圖，不能稱完整歐洲電網或社會／合作網路 |
| **SEC EDGAR** | **未執行** | N/A | N/A | 需先設定真實研究聯絡 `SEC_USER_AGENT`；不得以示範假地址或公司信箱替代 |

## 模型驗證（純合成）

- Leader budget = 10，三個 follower 接受 capacity allocation，分別最佳反應。最佳 leader caps = **[2,2,3]**，responses = **[2,2,3]**，leader objective = **26.75**，follower welfare = **31.5**。
- 中央規劃（**目標函數不同**）最高 welfare = **32.0**，allocation = **[3,2,3]**；兩者差不能直接稱為 price of anarchy。
- 共享 capacity K=3 的兩 follower toy generalized-Nash 有四組等效均衡：**(0,3)、(1,2)、(2,1)、(3,0)**。這說明 joint shared constraints 不能用獨立 follower argmax 取代；不是任何真實企業的均衡估計。

## 研究設計判定

1. 結構洞的第一候選外部母體仍是 **CORDIS consortium × OpenAlex 研究成果／DOI**。目前僅驗證兩個 API 可讀，**尚未建立同一實體的可追溯匹配**；不可直接把 24 筆樣本拿去跑 Burt 出論文結果。
2. 真實 OCDS API 可讀，但第一筆樣本沒有任何 tenderer 身分，反而是**資料缺漏風險的實測證據**。下一階段須計算足夠時間窗內的 bidder coverage；不適合因為 API 成功就直接設 Follower 效用。
3. GLEIF／SEC 是企業主從與財務補充，不是自動給你公司 AI 專案權限、工時、邊際效用的資料。
4. PyPSA 的真實物理拓樸適合**求解器與網路流壓力測試**；與 AI × Decision 的文獻機制是不同研究語境，不能混成「外部證明」。

## 可重現與異常處理

- GitHub Actions 產出 `external-dataset-live-probe` Artifact（14 日保留），內含每個來源的來源 URL、HTTP response SHA-256、資料筆數、失敗訊息、樣本 ID、求解結果；**不含原始來源大包／信箱金鑰／完整公司資料**。
- 每次 API 更新後先比對 response SHA-256，再比對固定的 ID 集合與指定時間窗。不把任意排名的搜尋前 8 篇當成固定研究母體。
- `docs/index.html` 原研究網站與舊版 RQ1–RQ3，**本研究 PR 沒有改動**。
