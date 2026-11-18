# AI × Decision｜六源 Burt、隨機對照、多層網路與 GLEIF 全量結果（第三輪，2026-11-18）

> **來源：** GitHub Actions [run #44275890175](https://github.com/Jimmy0307/ai-decision-ml/actions/runs/44275890175)（head `e6d2b27`）。`bounded-public-probe` 與 `gleif-rr-bulk` 兩個 job 成功；`deterministic-qa` 因 1 個程式錯誤失敗，已在 `5599a76` 修正（見 §6）。
>
> 本文件把 CI artifact（`external-dataset-live-probe`、`gleif-rr-cdf-bulk-profile`）裡的結果寫進 repo。原 artifact 的保存期限只有 14 天。數字彙整於 [results/ROUND3_KEY_NUMBERS_20261118.json](results/ROUND3_KEY_NUMBERS_20261118.json)。
>
> **總裁決：** `NO_SOURCE_PASSES_INDEPENDENT_RELATIONAL_AND_VALIDATION_GATES`。六個來源都沒有找到經確認的 Burt 中介者。這個結果的意思是：這些資料的「關係」不是資訊流，所以無法用來檢驗結構洞。它**不是**在說「真實世界沒有結構洞」。

## 1. CORDIS H2020：唯一具真實關係結構的來源

**資料：** 195 個關鍵詞候選計畫（未經人工驗證）× 1,105 個機構，共 1,436 條計畫–機構邊。

| 檢查 | 結果 | 意義 |
|---|---:|---|
| 原始二模網路的 Burt 間接項 | **全部 = 0** | 純二分圖上 C = 1/k，只反映度數，Burt 在二模層級無法識別 |
| 一模投影（共同參與計畫） | 1,049 節點、12,181 邊；constraint 中位數 0.180，最低 0.024 | 只是描述性指標 |
| 投影時從計畫內部「自動生出」的三角形 | **102,660 個** | 一個 60 機構的計畫會直接生成完全圖，constraint 因此被結構性壓低 |
| 至少共同參與 2 個計畫的重複邊 | **156 / 12,181** | 只保留這些重複邊時：87 節點，constraint 中位數 0.926（幾乎沒有中介位置） |
| 兩個時期的邊重疊（2014–17 vs 2018–20） | 2 條（Jaccard 0.0002） | 跨期幾乎沒有持續的關係 |

### 1.1 保度數的二分圖交換隨機對照（49 次）

先挑出 constraint 最低的 12 個機構，再和隨機網路裡「投影度數相近」的節點比較：

- **5 個**有至少 20 個同度數隨機樣本可比：單尾 p = 0.41、0.42、0.48、0.79、0.86；BH q = 0.80–0.86。
- **7 個**同度數樣本不足（3–19 個），算不出 p 值。
- **q < .05：0 個。**

也就是說，看起來最像「中介者」的機構，和隨機網路裡同樣連結數的節點沒有差別。低 constraint 主要來自度數與計畫規模。另外有三點限制：這是事後挑選、只做了 49 次、檢定力弱，所以只能當探索性結果。

### 1.2 候選中介者的穩定性

| 敏感度設定 | 與基準前 12 名的重疊 |
|---|---:|
| 只保留共同參與 ≥2 個計畫的邊 | 7 / 12 |
| 排除超過 20 個成員的計畫 | 5 / 12 |
| 篩選時加入 topics/keywords（233 個計畫） | 7 / 12 |
| 只看 2014–2017 | 3 / 12 |
| 只看 2018–2020 | 11 / 12 |

候選名單隨設定而變，主要被 2018–2020 的大型計畫主導。

**CORDIS 裁決：** `NO_CONFIRMED_BURT_BROKER_ONLY_PROJECTION_DIAGNOSTICS`

## 2. GLEIF Level 2 全量關係檔（RR-CDF，快照 2026-08-10）

官方 ZIP 大小為 37.2 MB（解壓後的 XML 約 1.10 GB），完整解析：

- **663,449** 筆關係紀錄，其中 ACTIVE 481,247 筆、INACTIVE 125,124 筆、狀態空白 57,078 筆。
- 有效的直接合併關係 125,538 筆、最終合併關係 131,784 筆，兩者重疊 88,686 筆。
- 把直接與最終關係合併後的無向圖：182,135 個節點、168,635 條邊、41,734 個連通分量，最大分量 1,044 個節點。
- 抽 1,500 個 ego（隨機種子 20261118，只取度數 2–100 的節點）：constraint 中位數 0.539，effective size 中位數 1.0。

**GLEIF 裁決：** `LEGAL_CONSOLIDATION_GRAPH_VALID_SOCIAL_BURT_NOT_IDENTIFIED`。這是法律上的合併報表關係，不是資訊或知識的流動。檔案也不含 reporting exceptions，以及沒有 LEI 的母公司。

## 3. 其他來源

| 來源 | 本輪結果 | 裁決 |
|---|---|---|
| OpenAlex | 8 篇論文 → 24 位作者、37 條共同作者邊；作者圖 effective size 全部 = 1.0（每篇論文都是一個小團體） | `UNCONFIRMED_IDENTITY_AND_OUTCOME` |
| OCDS（英國） | 本輪固定月份樣本取得 **0 條**可驗證的買方–供應商邊。artifact 裡的公告數與得標數欄位都是空值，所以分不清是抓取沒有回傳資料，還是全部被 party-ID 檢查排除，需要重跑確認 | `OBSERVED_AWARDS_NOT_INDEPENDENT_BROKERAGE` |
| SEC | 未執行（需要真實聯絡用的 User-Agent） | `NOT_APPLICABLE` |
| PyPSA GridKit | 8,786 個母線；10,594 條交流線、1,039 個變壓器、57 條直流連結；effective size 中位數 2.0 | `DIAGNOSTICS_ONLY_NOT_SOCIAL_BURT` |
| 跨來源多層網路 | 未建構：各來源的實體 ID 沒有通過解析 | `NOT_CONSTRUCTED` |

## 4. 方法可攜性

V9 的 10×12 家族配對檢定（M01–M07）、Limitation 語意分類（M20）、Gould–Fernandez 角色，以及因果中介或 leader–follower 均衡，**都不能直接套用到這六個來源**。原因有三：抽樣框架不同、關係語意不同、也沒有共同的實體。

## 5. 對 RQ3／RQ4（Multi-Level Programming）的意義

1. **這輪結果和 V9 遇到的是同一個問題：** 資料中的「關係」要嘛是共同出現（文獻功能、計畫共同參與），要嘛是所有權（GLEIF）或物理連接（電網）。這些都不是 Burt 構念需要的「行動者之間的資訊或資源流」。換資料源，沒有解決關係語意的問題。
2. **MLP 的成立不依賴 Burt 結構洞。** 多層規劃的前提是有不同目標與決策權的層級（leader／follower）和共享限制。CORDIS 可以提供真實的計畫→機構經費配置 \(y_{pu}\)，做為 `SEMI_EMPIRICAL_CALIBRATION` 的分配基準。
3. **如果要實證檢驗「AI 與決策之間有結構洞」，下一個資料源必須具備有方向的、二元的流動關係。** 例如：
   - 跨領域引用：AI 社群與決策科學社群的論文或專利互相引用；
   - 組織內部的實際溝通、審批或工單紀錄。

   檢定也要先預先登錄，再用保度數的隨機對照。不要再用共同出現的投影圖。

## 6. 程式修正（`5599a76`）

`multinetwork_six_sources.gridkit()` 把資產→母線的歸屬傳給 `project_affiliations`，方向放反了。結果輸出的是「母線投影圖」，卻被標成「資產 line graph」。artifact 中該項的數值是 8,786 個節點、11,690 條邊，正好等於母線數與資產數，可以佐證這一點。

修正後改用原本就已建好、方向正確的 `bus_asset_aff`。離線測試 **90/90 PASS**。這一項只是電網對照組的統計，不影響上面任何裁決；正確數值需要重跑 workflow 才會產生。
