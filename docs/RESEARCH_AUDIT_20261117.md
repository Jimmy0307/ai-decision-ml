# AI × Decision｜所有研究版本、資料、方法及結果：稽核總報告

**更新日期：2026-11-17｜會議用途：2026-11-18**  
**報告範圍：V5 既有功能語料，V6–V11.1 結構洞探索，以及 Gap Validity V1 / Limitation Scout V0.1。**

## 1. 決策摘要

本研究已建立 10×12 AI 功能與決策功能網路（120 種配對），既有凍結結果中 **32 組穩健關聯：16 組超額呈現與 16 組不足呈現**。但經引用網路、高階／三元關係與研究者合作網路等多軌探索，**截至 V11.1 沒有通過既定門檻的 AI×Decision Burt 仲介**。這不能推論「學界沒有知識缺口」，更不能把功能低整合改寫為 Burt 結構洞。

V9 人工審查揭露分類可靠性問題：在 20 筆雙人編碼中 AI、Decision family 均只有 4/20 完全一致（κ=0.048、0.140）；50 筆局部修正讓 24/120 格計數變動、核心 32 格成員一進一出。**必須完成全量再分析**。此外，作者合作網路的 V11.1 原始檔僅存於使用者 Windows 本機，本包保留其摘要數值但明確標示「尚未獨立核對」。

最後一輪先**補回舊有 PDF/TXT/HTML、DOI、作者 ID、citation edges 與 V11.1 外部查核 log**，按凍結規則重新檢查資料適配性；若仍無確認能力，停止用現有功能矩陣尋找 Burt，改採具有時序、群體與實際關係的資料。Limitation 研究是另一路線，目標是追查作者提出問題後的後續解決證據，不是 Burt 的替代指標。

## 2. 核心定量結果（來源級別請參閱 CSV）

| 範疇 | 量化成果 | 證據與解讀 |
|---|---:|---|
| V5 初始文獻 | 2,118 篇 | V9 稽核原文；歷史 1,729 篇可解析全文、388 skipped、1 failed |
| 證據處理 | 26,501 候選 → 6,499 嚴格納入 → 3,125 雙端分類 | 不是獨立文章數 |
| 功能矩陣 | 10 AI × 12 Decision；120 格，104 格有觀測邊 | 凍結研究鏈的二分功能網路 |
| 主零模型／穩健性 | 47 格 q≤.05 → 32 格四重檢驗維持，16 over/16 under | 四重檢驗相互關聯，不是四個獨立語料 |
| 模擬複核 | 主零模型 10,000；document-preserving null 5,000 | V9.1 基準重現；非論文篇數 |
| 人工審查 | 50 目標、20 第二編碼者、19 分歧協調 | 20 屬 50 子集，不能加總 |
| S1/S2 分段 | S1 保留 29/32；S2 保留 30/32；不足呈現分別保留 14/16、15/16 | 探索性敏感度，不取代全量人審 |
| 完整功能圖替代路徑 | 16/16 低整合配對移除直接邊仍可達、最短距離 3；7–9 條互不相交替代路徑 | 功能低整合不是網路斷裂 |
| 骨架跨分量數 | robust16: 10；main q≤.01:14；main q≤.05:0 | 數量受 backbone 定義影響 |
| V9 作者資料 | 7,880 篇查核，7,835 篇有作者，獨立網路 26,443 作者 | V11.1 使用者摘要，並非全文覆蓋率 |
| 合併作者網路 | 30,140 位作者，95 次匿名 OpenAlex 呼叫 | 需本機原始 CSV/log 獨立複核 |
| V11.1 候選 | 4 位；3 否決、1 資料不足；0 confirmed | Dwivedi 凍結文字與程式 verdict 存差異 |
| Limitation 初篩 | 25,112 段；1,104 文件 ID；100 有線索，142 個命中 | 尚未驗證後續研究解決狀態 |

## 3. V5–V11.1 方法完整歷程與正確解讀

本節區分 **研究版本** 與 **這週整理作業**。多個版本在 11 月 12–17 日以前就已執行；不能將所有歷史版本描述為「本週才跑完」。

| 版本 | 研究對象與方法 | 已做數量／結果 | 證據層級 |
|---|---|---|---|
| V5 | Functional corpus / 10×12 matrix；文獻擷取→LLM 語意編碼→四重統計穩健性 | 2,118 source; 1,729 parsed; 26,501 candidate records; 6,499 strict；32 robust (16 enriched, 16 depleted) | DIRECT_V9_FORENSIC |
| V6 | Citation SNA；引用缺邊、節點候選、red-team ground truth | 458 leads; 13 G2 candidates；0 confirmed | HISTORICAL_NOT_IN_UPLOAD |
| V7 | Author SNA early；作者標籤/共同作者/跨域初篩 | 446 works; 8 cross-domain authors; 2 focal candidates；0 confirmed | HISTORICAL_NOT_IN_UPLOAD |
| V8 | Citation enrichment；前後引用、外部引用關係 | 1,111 citing works; 5,592 references；Unconfirmed | HISTORICAL_NOT_IN_UPLOAD |
| V9 | Exploration / confirmation citation；3,983 discovery + 3,897 confirmation, null calibration | 7,880 works total；No confirmed Burt result | HISTORICAL_NOT_IN_UPLOAD |
| V9.1 | Sensitivity & calibration；10,000 main null; 5,000 document null; S1/S2 segmentation; citation calibration | 3,400 + 3,700 simulated trials (historical); 120 cells；32 frozen core; S1 retains 29, S2 30 | MIXED_DIRECT_AND_HISTORY |
| V9 Human | Human validation；50 first coder / 20 blind second coder / 19 reconciled | n=50 targeted; n=20 subset；FULL_REANALYSIS_REQUIRED | DIRECT_V9_FORENSIC |
| V10 | Higher-order network；超圖、三元共現/引用群體 | 14 exploratory candidates → 8 pairs / 7 brokers；Exploratory only | HISTORICAL_NOT_IN_UPLOAD |
| V10.1 | External independent review；跨群體替代連結、移除候選者反證 | 8 candidate pairs; 6 refuted, 2 unresolved；0 confirmed | HISTORICAL_NOT_IN_UPLOAD |
| V11 | Coauthor SNA；V9 independent and V5+V9 coauthor networks | 26,443 V9 authors; 30,140 merged authors；0 confirmed | USER_REPORTED_V11_1 |
| V11.1 | External identity & peer validation；95 anonymous OpenAlex requests; alias disambiguation; team isolation; peer robustness | 7,880 works examined; 7,835 with authors; 4 candidates；3 rejected, 1 insufficient, 0 confirmed | USER_REPORTED_V11_1 |
| Gap Validity V1 | Construct validity sidecar；Bipartite constraint decomposition, alt paths, threshold, projection, synthetic simulation | 120 cells; 104 observed; 16 depleted; 14 tests；16/16 alternate routes; cross-component 10/14/0 | DIRECT_SIDECAR |
| Limitation Scout V0.1 | Future-work tracing seed；Selected segments lexical screen and local fulltext scanner tool | 25,112 selected segments; 1,104 IDs；100 clue docs; 142 matches; no resolved-status verification | DIRECT_SIDECAR |

### 為什麼反覆檢查後仍沒有已確認 Burt 仲介？

1. **測量層級錯配**：功能二分邊反映 AI×Decision 被文獻直接連結的頻率，不是研究者之間具有獨占資訊通道。單純的稀少或低 O/E 不等於 Burt nonredundancy。
2. **替代路徑充足**：16 組低整合邊全數在完整功能網路中已有觀測值，拿掉自身直接邊後仍可以經由第三節點到達，且有 7–9 條互不相交替代路徑。
3. **骨架門檻不穩**：使用不同 enrichments 組成骨架，跨分量標記可由 14、10 變成 0；不能把標記數當穩定的結構洞個數。
4. **二分 Constraint 退化**：在本研究固定 simple bipartite 邊及 `p_ij` 正規化定義下，Burt 間接三元項為零，constraint 退化為直接權重集中度；投影後產生的三角形並非獨立觀測連結。
5. **外部合作反證**：V11.1 摘要報告 Herrera 存在 26 篇其不參與下的跨團隊合作；Dwivedi 也有 11 篇。不能只在截斷網路上把其判為獨占仲介。
6. **作者識別與同儕門檻**：Herrera 具有多個 OpenAlex author ID；Kwilinski 在 63 位同儕中另有 23 位同分；Kuzior 在 21 位同儕中並不突出。外部 alias 與 peer 比較是確認性條件。
7. **分類與資料完整性**：人審局部修正已改變核心成員；若未鎖定證據擷取與編碼，繼續調網路參數得不到可稽核的 Burt 結論。

## 4. V11.1 四位候選（僅來自本機完成摘要）

| 研究者 | 裁決 | 主要證據 | 資料界線 |
|---|---|---|---|
| Francisco Herrera | REJECTED | 26 cross-team papers without focal author, 2004–2023; two author-ID duplicates removed from earlier 28 | 需本機 V11.1 完整原檔 |
| Aleksy S. Kwilinski | REJECTED | 63 comparable peers; 23 tied at same score | 需本機 V11.1 完整原檔 |
| Aleksandra Kuzior | REJECTED | Not exceptional against 21 comparable peers | 需本機 V11.1 完整原檔 |
| Yogesh K. Dwivedi | INSUFFICIENT_DATA | 11 external papers connecting core teams without focal author; remaining low-frequency 1-paper tie; 2 peers only; frozen text/code verdict conflict | 需本機 V11.1 完整原檔 |

**注意：** Dwivedi 的凍結文字若逐字執行可能會得出「否決」，凍結程式記為「資料不足」。這項 taxonomy 衝突必須保留，不能改寫成已被一致否決。兩種判定都不構成確認成立。

## 5. V9 人工審查與可投稿性（直接對照原始稽核）

| 編碼欄位 | N | 完全一致 | Cohen κ |
|---|---:|---:|---:|
| C1 Evidence validity | 20 | 15/20 | 0.561 |
| C2 Relation type | 20 | 7/20 | 0.180 |
| C3 AI functional family | 20 | 4/20 | 0.048 |
| C4 Decision functional family | 20 | 4/20 | 0.140 |
| C5 Analytical inclusion | 20 | 12/20 | 0.316 |

上述是小型、針對性的 Robust-A 子樣本的一致性指標，不得當成全文編碼準確率。原始 V9 凍結核心仍未更動；局部 corrected sidecar 得到相同的 32 個核心格數，但新納入 `HUMAN_AUGMENTATION × RISK_ASSESSMENT`、移除 `COORDINATION_EXECUTION × GENERAL_DECISION_PROCESS`。需核准全面重分析後才能更新確認性結論。原報告另外把 legacy operational audit-log prefix 列為 `UNVERIFIED`，而非有竄改證據。

## 6. 我們到底有哪些 Social Network／結構洞工具？

| 類別 | 指標或方法 | 可以回答的問題 | 本次界線 |
|---|---|---|---|
| 二分功能網路 | Degree-controlled null / O:E / BH-FDR | 哪些 AI–Decision 接口相對不足？ | 是功能低整合，不是作者 Burt |
| Citation network | 引用連結與替代最短路徑 | 文獻是否跨群體傳遞引用？ | 未引用可能是截斷、時間差或其他形式的知識流動 |
| Coauthorship | Burt constraint、effective size、efficiency | 研究者的非冗餘社會連結程度 | 必須檢查作者 identity、群體與同儕 |
| Network brokerage | Betweenness、cut-vertex、node/edge disjoint path | 移除節點會否中斷關係？ | 高中介中心性或割點也不等於 Burt 必要充分條件 |
| Triads & higher order | Open triads / Hypergraphs | 成對關係是否失去共同群體資訊？ | 不可把共同出現直接當真實合作 |
| Multi-layer / temporal | Citation × coauthor × year | 仲介是否先於跨域知識流動？ | 原研究缺少完整時序與獨立結果測量 |
| Brokerage roles | Gould–Fernandez 五種群體角色 | coordinator/gatekeeper/representative/consultant/liaison | 需有群體定義與方向，非五種獨立 Burt 指標 |

## 7. Limitation：目前能與不能說的話

`Limitation Scout V0.1` 已對 V9 S1 選取段落做關鍵詞初篩，資料與測試可檢查。但此段落集原本為 AI × Decision 功能語意編碼而篩選，**並不是完整的 Limitation sections**。目前沒有追蹤 DOI 的後續文獻，也沒有針對「resolved / partially resolved / repeated / insufficient coverage」完成可靠分類。因此**沒有任何由本包新確認的長期未解研究缺口名單**。

正確順序：合法取得原始全文→擷取作者自己的 limitation 原文＋頁碼→同義問題聚類→依 DOI/引用＋語意搜尋後續文獻→逐項記錄解決或反證→抽樣人工複核。

## 8. 原始資料回收與停止條件

| Priority | 項目 | 狀態 | 下一步 |
|---|---|---|---|
| P0 | V11.1 raw external author checks | Not mounted | Need 00-03, final verdict CSV, API call log, author id aliases |
| P0 | V5 original paper fulltexts / SQLite | Not mounted | Need original PDF/TXT/HTML file inventory; DOI, SHA, permissions |
| P1 | V6–V10.1 canonical logs/manifests | Not mounted | Find exact per-version run IDs, candidate CSV, model seeds and gates |
| P1 | V9 full human reanalysis | In progress / not verified here | Fix mapping taxonomy and refresh main analyses after approval |
| P1 | Limitation fulltext extraction | Not executed here | Pass original limitation quotes, pages, DOI, versions |
| P1 | Later-publication resolution audit | Not executed | Forward/back citation + topic search and manual evidence grading |
| P2 | New Burt-suitable network if final gate fails | Conditional | Explicit edge semantics, time, groups, boundary and alternative paths |

**停止閘門**：在新一次 Burt 測試前固定樣本、連結定義、作者合併、時間窗、null 與 peer 條件；補回 V11.1 外部合作原始紀錄；如仍沒有實質非冗餘橋接，且資料不能支持知識流動推論，**停止此資料集上的 Burt 搜尋**並保留 0 confirmed；不得為求正面結果不斷更換門檻。若要追蹤作者 limitation，另立研究設計及全文搜尋覆蓋率品質閘門。

## 9. 檔案可取得性與再現品質

- `20260929_V9_HUMAN_VALIDATION.zip`：**920 個檔案成員**、全數可讀取／SHA256 已記錄；來源等級 V9 Human & V9.1。
- `AI_DECISION_GAP_VALIDITY_V1_COMPLETE.zip`：**25 個檔案成員**、全數可讀取／SHA256 已記錄；來源等級 Gap Validity Sidecar。
- `AI_DECISION_LIMITATION_SCOUT_V0_1_READY.zip`：**9 個檔案成員**、全數可讀取／SHA256 已記錄；來源等級 Limitation Scout。
- `AI_DECISION_WEEKLY_BRIEF_20261118.zip`：**7 個檔案成員**、全數可讀取／SHA256 已記錄；來源等級 Weekly Brief。
- `完整資料來源.zip`：**69 個檔案成員**、全數可讀取／SHA256 已記錄；來源等級 Earlier Archive Apr 2026。

**此輪重新執行的小範圍程式測試**：Gap Validity V1 `14/14 PASS`；Limitation Scout V0.1 `8/8 PASS`。**這不是**重跑 V11.1 OpenAlex、V9 全語料重掃或 V6–V10.1 歷史實驗。

`完整資料來源.zip` 為 2026-04-22 的舊分析封存，包含 PCA/FA、Tier、info-gap、主路徑與圖表。其 69 個實際檔案成員並不構成與 V9 功能母體同一版本的證據。本次保留路徑／SHA256、不混入 V9 統計母體。

## 10. 老師需要知道的最終狀態

- `V9_FUNCTIONAL_GAP_BASELINE`: **32 核心／16 低整合**，但全量人審後需再計算；不是已確認 Burt。
- `V11_1_BURT_CONFIRMED`: **0（使用者完成摘要）**，四名候選三否決、一未決；原始包待核對。
- `DATA_RECOVERY`: **PARTIAL**，5 個上傳 ZIP 檢視完成；Windows 本機原始包未接入。
- `LIMITATION_RESOLUTION`: **NOT_YET_VERIFIED**，不可稱已找到「沒人做」的研究缺口。
- `SUBMISSION_READY`: **NO**，需完成資料來源、編碼、人審與外部反證後再決定文章定位。

## 11. 來源與檔案檢索

每一數值皆在 `data/ALL_METRICS_WITH_PROVENANCE.csv` 保留原始來源路徑與證據層級，檔案 SHA-256 與類型在 `data/ALL_ARCHIVE_MEMBERS_SHA256.csv`。最重要的內部原始文檔節錄在 `docs/V9_SOURCE_VERIFICATION.md`、`docs/HUMAN_AUDIT_RAW.md`、`docs/SEGMENTATION_BASELINE_RAW.md`、`docs/GAP_VERDICT_RAW.md` 與 `docs/LIMITATION_SCOUT_RAW.md`。