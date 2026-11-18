# 外部資料 × AI × Decision × Multi-Level Programming｜可重現可行性實驗

> **Research-only / 2026-11-18.** 分支 `research/external-data-mlp-feasibility-20261118`。目前測試為 **dataset feasibility / schema validation / synthetic model**，不是 V9 重分析，也不是證實結構洞／企業 AI 最適解。既有 `main`、V9/V11.1、LEM2、DRSA 一律不覆蓋。

## 第三輪結果（最新、正式閱讀入口）

**[ROUND3_BURT_MULTINETWORK_RESULTS_20261118.md](ROUND3_BURT_MULTINETWORK_RESULTS_20261118.md)**：來自 GitHub Actions [#44275890175](https://github.com/Jimmy0307/ai-decision-ml/actions/runs/44275890175)，關鍵數字在 [results/ROUND3_KEY_NUMBERS_20261118.json](results/ROUND3_KEY_NUMBERS_20261118.json)。
- **六個來源都沒有找到經確認的 Burt 中介者**（`NO_SOURCE_PASSES_INDEPENDENT_RELATIONAL_AND_VALIDATION_GATES`）。
- CORDIS 保度數隨機對照做了 49 次：可算 p 值的 5 個候選 p = 0.41–0.86，q ≥ 0.80，沒有任何一個 q < .05；另外 7 個同度數對照樣本不足。
- CORDIS 投影圖由計畫內部自動生成了 102,660 個三角形。在重複邊骨幹圖上，constraint 中位數是 0.926。
- GLEIF 全量 RR-CDF：663,449 筆關係紀錄，其中 481,247 筆為 ACTIVE；這是法律合併關係，不是資訊流。
- 跨來源多層網路沒有建成，因為實體 ID 對不起來。
- 離線測試 **90/90 PASS**（`5599a76` 修正了 PyPSA line graph 的投影方向）。

## 第二輪結論（歷史紀錄）

**[ROUND2_RESEARCH_CONCLUSIONS_20261118.md](ROUND2_RESEARCH_CONCLUSIONS_20261118.md)** — GitHub Actions #44269235163 已對 H2020 全量 project/participation 進行第二輪對帳及六來源可識別性評估。**33/33 deterministic tests PASS**。195 title/objective 候選的經費與角色資料可形成 **semi-empirical allocation benchmark**；加入 topics/keywords 則有 233 個字詞候選（未人工驗證）。187/187 可對帳 EC projects 在 1% 差距內；OpenAlex 跨資料庫獨立獎補助／成果連結尚未解決，SEC 未執行，沒有 confirmed Burt holes 或 empirical MLP equilibrium。

**注意：**H2020 project ZIP 裡**沒有** publication.csv；CORDIS 出版品資料另有來源，且官方資料集註有欄位錯置風險。先前授款編號查詢 500 筆不等於 500 筆有效 CORDIS grants（不同 funder 會重複編號）。

## 第一輪已執行結果（歷史紀錄）

**正式成果入口**：[GitHub Actions 全部六源實測報告](EXTERNAL_DATA_FINAL_POC_REPORT_20261118.md) · [公開來源與證據等級 JSON](results/FROZEN_SIX_SOURCE_SNAPSHOT_20261118.json) · [實際 GitHub Actions](https://github.com/Jimmy0307/ai-decision-ml/actions/runs/44264544878)

- **CORDIS H2020 完整 ZIP：已在 GitHub Runner 真實下載並解析** 35,389 projects、179,063 organization participations、41,995 organisation IDs；探索性 title+objective AI∩Decision 詞彙交集 195 projects、1,436 個 project-org edges、1,105 機構。**不是 195 件經人審的研究。**
- **PyPSA 非官方 GridKit AC/DC/Transformer：已在 GitHub Runner 取回三份 CSV**，11,690 distinct edges、8,786 incident buses；不是 CORDIS 的合作網路。
- OpenAlex／GLEIF／英國真實 OCDS 均已在 GitHub 取得小樣本，但實證識別不足；**SEC 因需提供真實聯絡 User-Agent 而未跑**。
- GitHub CI offline tests **19/19 PASS**（新 CORDIS 合成 ZIP join 測試加入）；這不是各外部母體已完成確認性假說檢驗。
- **原始大型 ZIP 不推入公開 repository**；取得指令、source SHA-256、run IDs、資料來源上限及 QA 已記錄；衍生小母體的 public project/organisation IDs 由 GitHub Actions artifact 保留。

## 先看結論（已更新至第三輪）

1. **CORDIS H2020 是唯一有真實關係結構的來源。** 完整官方 ZIP 已解析：35,389 個計畫、179,063 筆參與紀錄。用關鍵詞選出 195 個候選計畫（未經人工驗證）。經費對帳 187/187 都在 1% 以內，可以做 **semi-empirical allocation benchmark**。但「共同參與計畫」不等於資訊流，Burt 中介者在第三輪隨機對照中 0 個顯著。
2. **GLEIF（全量關係檔）、PyPSA（完整的交流、直流與變壓器拓樸）是有效的網路**，但分別是法律所有權與物理電網，不是社會或知識網路，只能當對照組。
3. **OpenAlex（8 篇）、OCDS（第三輪 0 條可驗證邊）、SEC（未執行）** 的樣本或識別不足。
4. **MLP 數值仍全部是 SYNTHETIC。** 沒有觀測到 follower 的效用、反應函數或決策順序，所以不能宣稱實證均衡。
5. 早期描述（PyPSA 只有 1,096 邊、CORDIS 大包未執行、14/14 或 19/19 測試）已被後續輪次取代，只保留在歷史報告中。


## 六大資料來源與適配定位

| 源 | 唯一來源／官方規格 | 主要欄位與驗證目標 | 目前裁決 |
|---|---|---|---|
| CORDIS H2020 | [EU CORDIS](https://cordis.europa.eu/projects/en) [官方 ZIP](https://cordis.europa.eu/data/cordis-h2020projects-csv.zip) | `project.id ↔ organization.projectID`、participant、coordinator、funding、start/end | **完整 ZIP 已解析**；195 個候選計畫的經費基準可用；Burt 0 個顯著（第三輪） |
| OpenAlex | [OpenAlex API](https://help.openalex.org/api/) | works、authorships、institutions/ROR、topics、citations，與 CORDIS project DOI 對接 | 8 篇小樣本；尚未與 CORDIS 確認性連結 |
| OCDS | [OCP Data Registry](https://data.open-contracting.org/en/) [UK 真實出版者](https://data.open-contracting.org/en/publication/128) | buyer、tenderers、awards、suppliers、amount、date | fictional schema 已測；英國真實樣本第三輪 0 條可驗證邊 |
| GLEIF | [GLEIF API](https://www.gleif.org/en/lei-data/gleif-api) [Level 2](https://www.gleif.org/en/lei-data/access-and-use-lei-data/level-2-data-who-owns-whom) | LEI、direct / ultimate accounting consolidating parent | **全量 RR-CDF 已解析**（663,449 筆）；法律合併關係，不是社會網路；不含 reporting exceptions |
| SEC EDGAR | [SEC XBRL API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) | CIK、`us-gaap/Assets` 等財務時序；**不是 AI 導入參數** | 需具真實研究聯絡方式之 `SEC_USER_AGENT` 才允許擷取，未設就跳過 |
| PyPSA-Eur | [PyPSA-Eur](https://github.com/PyPSA/pypsa-eur) [GridKit](https://github.com/PyPSA/pypsa-eur/tree/master/data/entsoegridkit) | buses、AC/DC lines、topology、physical network；再建 multi-follower power planning | 交流、直流與變壓器三份 CSV 已完整解析（8,786 個母線）；需求／成本與 solver 尚未執行 |

> 權限與限制：OpenAlex 的 2026 API 用量依 API key 與方案變動；設定 `OPENALEX_API_KEY` 前先確認當前價格／rate-limit，不得直接對全資料庫暴力爬取。SEC 公開指南要求 **真實 User-Agent（機構和聯絡資訊）**，請從本機環境變數提供，切勿提交公司／私人信箱於 GitHub。CORDIS 原始 ZIP 不在 public git 儲存；PyPSA 原始資料、不同第三方模型授權可能不一樣。

## 執行

```bash
# 無 API、無額外 Python 套件、可重現合成示例
python -m unittest discover -s research/external_dataset_poc_20261118/tests -p 'test_*.py' -v
python research/external_dataset_poc_20261118/src/poc.py --mode fixture \
  --output /tmp/ai_decision_fixture.json

# 官方可公開來源：小批／限速／8MB 上限；SEC 預設跳過，CORDIS ZIP 不下載
python research/external_dataset_poc_20261118/src/poc.py --mode live \
  --output /tmp/ai_decision_public_live.json

# 明確選擇才取 2022 GridKit AC lines，並重建較完整但仍不等同 PyPSA-Eur solved network
python research/external_dataset_poc_20261118/src/poc.py --mode live --pypsa-full \
  --output /tmp/ai_decision_grid_extra.json

# 只有經同意之地端／大型儲存環境才允許 CORDIS H2020 bulk（上限 180 MB）
python research/external_dataset_poc_20261118/src/poc.py --mode live --cordis-bulk \
  --output /tmp/ai_decision_cordis_probe.json

# SEC: 使用真實研究身分，不能使用示範信箱或公開密鑰
export SEC_USER_AGENT='Research institute ResearcherName researcher@real-domain.edu'
python research/external_dataset_poc_20261118/src/poc.py --mode live
```

**資料處理上限**：預設最多 8MB/檔，HTTPS only、30 秒 HTTP timeout；CORDIS bulk 明確 opt-in。原始第三方 raw bytes 不寫入 GitHub，僅留下查詢來源、SHA256、資料筆數／品質統計。GitHub Actions 上的 `bounded-public-probe` 只能以 `workflow_dispatch` 且 `live_probe=true` 呼叫；PR 自動只跑 deterministic QA。

## 對 Multi-Level Programming 的可驗證意義

- **Leader** 先分配共享 AI capacity / budget / policy，**Followers** 在各自 cap 下各自最佳反應。含 cap 的下層若獨立，能枚舉求解，不需要假裝是 GNE。
- **Follower 共同爭奪尚未分割的總資源**時，會形成耦合可行集合，必須明確建立 Generalized Nash Equilibrium 或 equilibrium constraints，不可用原本獨立 `argmax` 代替。
- `src/poc.py` 的兩個求解例都是 **synthetic-only**，沒有估計企業參數，不代表這六個資料源具備人員工時、AI 效用／部門反應或企業導入 ROI。
- 結構洞外部驗證首選 **CORDIS 具真實明確關係的 consortium** + OpenAlex 獨立後續論文；行政合作與共同發表是**兩種關係**，不能視作獨立樣本抽樣。OCDS 採購可以是獨立的 multi-follower case，但會改變論文應用域。

## 下一個證據關卡

1. 選定資料源的時間窗、空間／機構母體及授權，把取得版與 checksum 凍結；
2. CORDIS consortium participant 關係圖與 OpenAlex 外部成果**先做 join 匹配率／ID 正規化**，不急著計算 Burt；
3. OCDS 真實資料需驗證有多少筆具 **投標者與失敗投標者、時序、金額、標案與買方**，不是只列中標供應商；
4. GLEIF/SEC 只能作企業層級與金融條件**輔助變數**；母公司擁有權 ≠ AI resource authority；
5. 每條線必須設立「是否可觀測 Leader、Follower 決策與 shared constraints」判斷。無真實效用函數便僅標 simulation／estimated parameters。

**Branch-only; PR for review, not merged into `main`.** CI 可通過是程式可執行，不等於取得足以發表的實證資料。
