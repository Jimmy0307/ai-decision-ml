# 外部資料 × AI × Decision × Multi-Level Programming｜可重現可行性實驗

> **Research-only / 2026-11-18.** 分支 `research/external-data-mlp-feasibility-20261118`。目前測試為 **dataset feasibility / schema validation / synthetic model**，不是 V9 重分析，也不是證實結構洞／企業 AI 最適解。既有 `main`、V9/V11.1、LEM2、DRSA 一律不覆蓋。

## 先看結論

1. **PyPSA-Eur 實資料已獨立讀取。** 實際自 `PyPSA/pypsa-eur` 下載型 GitHub 內容接口取得 `transformers.csv`（1,039 列）及 `links.csv`（62 列），轉成不含自迴圈的無向去重網路 1,096 邊、2,061 節點、997 個連通分量（最大 10）、32 個局部三角形。這是**缺少 AC `lines.csv` 的局部物理拓樸**，絕不可拿它計算「全歐洲社會／合作結構洞」。原始資料來自 GridKit 對 2022 年 3 月非官方 ENTSO-E 地圖的推導；`transformers` 為推導所得，非官方核准資料。來源原始 GitHub blob SHA 及量化結果在 [real_source_poc_20261118.json](results/real_source_poc_20261118.json)。
2. **OCDS 僅驗證 schema**：讀取官方 open-contracting `sample-data` 的 **fictional** 範例，正確取出一買方、兩投標者、一得標者、一獎項及 GBP 幣別；**不可作政府採購經驗證據**。
3. **本機 14/14 測試 PASS**：可重現下載／解析 guard、各來源 schema 範例、簡化 GNE 和 leader→multi-follower 最佳反應。GitHub 分支上的簡化 CI 另提供 18 項 deterministic QA（**CI 結果需實際查 Actions**）。
4. **OpenAlex、CORDIS、GLEIF、SEC、OCDS 真實採購：官方路徑已核對、編寫受控取得程式，但尚未取得足夠原始資料來證明研究適配性**。不可把「有 API」等同於實際取得、可串聯或通過資料品質驗證。

## 六大資料來源與適配定位

| 源 | 唯一來源／官方規格 | 主要欄位與驗證目標 | 目前裁決 |
|---|---|---|---|
| CORDIS H2020 | [EU CORDIS](https://cordis.europa.eu/projects/en) [官方 ZIP](https://cordis.europa.eu/data/cordis-h2020projects-csv.zip) | `project.id ↔ organization.projectID`、participant、coordinator、funding、start/end | 官網確認；**大包未執行，待下載與 schema/joins QA** |
| OpenAlex | [OpenAlex API](https://help.openalex.org/api/) | works、authorships、institutions/ROR、topics、citations，與 CORDIS project DOI 對接 | 小批查詢 adapter 已編寫；CI live 選用，尚無獨立外部匹配 |
| OCDS | [OCP Data Registry](https://data.open-contracting.org/en/) [UK 真實出版者](https://data.open-contracting.org/en/publication/128) | buyer、tenderers、awards、suppliers、amount、date | 官方**fictional schema 已測**；UK 真實發布資料未定母體 |
| GLEIF | [GLEIF API](https://www.gleif.org/en/lei-data/gleif-api) [Level 2](https://www.gleif.org/en/lei-data/access-and-use-lei-data/level-2-data-who-owns-whom) | LEI、direct / ultimate accounting consolidating parent | adapter 已編寫，未聲稱驗證 parent edge；reporting exception 必須處理 |
| SEC EDGAR | [SEC XBRL API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) | CIK、`us-gaap/Assets` 等財務時序；**不是 AI 導入參數** | 需具真實研究聯絡方式之 `SEC_USER_AGENT` 才允許擷取，未設就跳過 |
| PyPSA-Eur | [PyPSA-Eur](https://github.com/PyPSA/pypsa-eur) [GridKit](https://github.com/PyPSA/pypsa-eur/tree/master/data/entsoegridkit) | buses、AC/DC lines、topology、physical network；再建 multi-follower power planning | 兩份真實來源局部圖已量化；全網 `lines.csv`、需求／成本、solver 尚未執行 |

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
