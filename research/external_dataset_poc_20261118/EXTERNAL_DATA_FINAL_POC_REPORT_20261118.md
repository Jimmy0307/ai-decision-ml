# AI × Decision × MLP｜外部資料 PoC 最終第一輪報告（2026-11-18）

**唯一研究 repo**：`Jimmy0307/ai-decision-ml`；**實驗 branch**：`research/external-data-mlp-feasibility-20261118`；**PR**：[#3](https://github.com/Jimmy0307/ai-decision-ml/pull/3)（DRAFT / **DO NOT MERGE**）。本實驗不改寫 `main`、V9/V11.1 凍結數據或 LEM2/DRSA。

## 可重現的 GitHub 實測證據

| Run | 執行內容 | 結果 |
|---|---|---|
| [44262023630](https://github.com/Jimmy0307/ai-decision-ml/actions/runs/44262023630) | 18 deterministic tests + OpenAlex / GLEIF / OCDS fictional / PyPSA DC limited live | PASS |
| [44262625197](https://github.com/Jimmy0307/ai-decision-ml/actions/runs/44262625197) | 加入 CORDIS SPARQL 24 筆及英國真實 OCDS 公告 1 筆 | PASS |
| [44263485647](https://github.com/Jimmy0307/ai-decision-ml/actions/runs/44263485647) | H2020 官方完整 ZIP（約 55.3 MB）與 AC+DC+transformer GridKit 公開 CSV | PASS |
| [44263879106](https://github.com/Jimmy0307/ai-decision-ml/actions/runs/44263879106) | 全量 CORDIS 依固定英文詞篩出 AI×Decision 資料子圖 | PASS |
| [44264544878](https://github.com/Jimmy0307/ai-decision-ml/actions/runs/44264544878) | 保留 195 project metadata 與 1,436 個 project↔org ID edges；19/19 deterministic tests | PASS |

上述 Actions 的 **live raw bytes** 只在 Runner 暫存記憶體；GitHub Artifacts 保留有統計、ID 與來源 SHA，不含完整原始 CORDIS 研究 ZIP。**自動測試 PASS 不等於研究假說確認**。

## 六個資料來源逐一裁決

| Dataset | 實際執行 | 結果與限制 |
|---|---|---|
| **CORDIS H2020** | **完整官方 ZIP 已取回且整包解析** | 35,389 projects、179,063 project–organisation rows、41,995 unique organisation IDs，179,063/179,063 rows 的 project ID 可對接；14,755 個 project 有至少兩個組織參與紀錄 |
| **OpenAlex** | **真實 API 8 篇小樣本** | 8 work DOI、25 authors、14 institution IDs；未完成與 CORDIS 的 DOI／ROR entity resolution |
| **OCDS** | **官方 fictional + 英國 1 筆真實公告** | Fictional 為 1 buyer／2 tenderers／1 winner；UK real sample 的 tenderers=0，不能用來估計多供應商反應函數 |
| **GLEIF Level 2** | **一筆真實 LEI API 紀錄** | 有 direct/ultimate parent 關聯 key，但相關 parent record URL 均未顯示；不能斷言母子企業關係已證實 |
| **SEC EDGAR** | **因 User-Agent 身分未提供而停止** | 已編寫讀取公司 Assets 的 adapter；不得偽造研究者聯絡資料，亦不以一般財報推論 AI 部門成本 |
| **PyPSA-Eur / GridKit** | **三種物理網路 CSV 成功下載** | 1,039 transformer rows + 62 DC links + 11,151 AC lines = 8,786 incident bus IDs、11,690 unique undirected links、117 components，最大分量 8,422 nodes；為**非官方 2022 物理電網拓樸，非社會網路** |

## CORDIS AI × Decision 候選母體

**來源與演算法身分：**官方 H2020 `project.csv` 與 `organization.csv`，先以固定 AI 5 字詞、Decision 6 字詞進行不區分大小寫的 *substring* 比對；本次實際納入的是 `title` + `objective`（程式寫了 singular `topic`，但官方欄位是 `topics`，因此並未納入 topics/keywords）。此為**概念的高召回／語義準確率尚未測量的探索性篩選**，不是人審後的 AI×Decision corpus。

| 計數 | 結果 |
|---|---:|
| 有 AI 詞彙 | 1,902 projects |
| 有 Decision 詞彙 | 1,522 projects |
| 兩種詞均命中的候選 | **195 projects** |
| 195 project 的組織參與原始二模邊 | **1,436 edges** |
| 不同機構 | **1,105 org IDs** |
| 參與兩項以上被選計畫的組織 | **188 org IDs** |
| 至少 2 個組織參與的被選計畫 | **104 projects** |
| 共同參與計畫衍生的去重機構合作投影邊 | **12,181** |
| 投影網路的非孤立機構／最大連通分量 | **1,049／1,029** |

195 個 project 的 `totalCost` 與 `ecMaxContribution` 原文字串都可解析；`totalCost` 總和 **595,155,509.43**（CORDIS 專案成本數值；須以官方單位核定）、中位數 **1,709,875**。經費不代表 AI 導入預算或 leader 已實際分配給各 follower 的額度。該候選母體包含 195 個 `grantDoi`，其為**授款計畫 DOI，不等於研究論文 DOI**。

**實驗觀察：**候選關係圖已具有比文獻功能共現更合理的 *project affiliation* 構念，但由同一計畫推導的聯繫會自動形成 clique，不等於雙邊資訊流。**不能用 12,181 條投影邊當作 12,181 條已觀測合作交流；也尚未測得可信 Burt brokers。**

## MLP 實作

- 真正的 `leader → 3 independent followers` 有限整數小模型已於 GitHub Runner 獨立運行：budget 10；最適 leader cap = [2,2,3]，follower best response = [2,2,3]，leader objective 26.75，follower welfare 31.5。
- 共享 capacity 的兩個 follower generalized-Nash toy 用以測試耦合可行集合；與 independent-follower case 邊界清楚。
- 所有這些值是 **SYNTHETIC**，未經 CORDIS、OCDS 或企業數據校準；不能當成企業效益或實際社會均衡。

## 決策與停止條件

**最值得深入的雙軌**：（1）CORDIS 的 project×organisation 雙模關係，先做 project/organisation ID、主題分類、時間窗與投影效度；以 OpenAlex DOI/ROR 建立真正外部成果追蹤；（2）獨立的 multi-follower/shared-capacity MLP 實證，需可觀測 budget、allocation、utility、constraint。若資料只有 outcomes 沒有 follower decisions，至少明確識別不可推論的參數。

**不建議直接充當企業 AI 決策資料**：PyPSA 是電網演算法壓測；OCDS 目前拿到的真實範例沒有失敗投標者；GLEIF 是企業所有權，不是資源決策；SEC 是財報指標。

**地端執行需求**：目前 GitHub 已成功處理 CORDIS 55 MB 和完整 GridKit source CSV，**尚不需要使用者的 Windows 電腦重跑**。未完成的是 full OpenAlex institutional linkages、OCDS 有效 bidder population、GLEIF parent record、SEC 合法 User-Agent，以及正式 Burt null tests。這些是資料識別與取得範圍的限制，非 GitHub 記憶體不足。

**附錄/入口**：
- [Coded adapters](src/poc.py)
- [19 offline deterministic tests](tests/test_poc.py)
- [來源狀態與實際檔案 SHA](results/FROZEN_SIX_SOURCE_SNAPSHOT_20261118.json)
- [第一次小樣本審查](LIVE_PROBE_EVIDENCE_20261118.md)
- [數據源母體登錄](DATA_CATALOG.csv)

**PR 為 DRAFT、不得合併**，直到外部效度及資料保留方式確定。
