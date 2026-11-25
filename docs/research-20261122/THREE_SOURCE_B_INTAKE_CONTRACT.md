# B｜CPC 共分類網絡結案資料接入規格（2026-11-25）

此檔案是公開研究網站的 **sidecar 接口**，供使用者完成 B 後插入，不是新的預先登錄，也不會自行更改 B 的真實研究協定。

## 1. 保留 A、C 固定證據
- A：私人 GitHub RQ1 folder 34（`97022752` 讀取），Level 1 analytical closure；配對洞 0/16、Graph K 低限制度 0/22。
- C：Google Drive `r2_brokerage_summary.json` 與 `r4_firm_brokerage_summary.json`；專利與公司各有 200 次零模型。紀錄為 read-only summary，並未重新建網。
- B：目前 `PENDING_USER_GITHUB_PUSH`；不能用歷史 8/42 類別敏感度代替新計算。

## 2. B 完成後必須提供
1. **確切 GitHub repo／branch／commit SHA／檔案路徑**。不要只給「main 最新」或相似 repository。
2. 執行日期、原始輸入 hash、來源專利母體、年份範圍、CPC as-of/current 版本和取樣限制。
3. 節點／邊／權重定義；如何處理一件專利多碼、分類層級、同族、年份及不可連結記錄。
4. 樣本數、節點／邊／連通分量、觀察／期望關係；Burt Constraint、Effective Size、橋接或路徑測量。
5. 零模型與重抽方法，seed、reps、統計尾部、p 值和 q 值、多重比較、信賴區間或靈敏度。
6. 如果對照 as-of/current，固定相同母體還是重新篩選？兩種做法估計對象不同。
7. 最終判定範圍、負結果／不可估、失敗項目、重現命令和獨立重驗證據。

## 3. 合併驗收門檻
- B 引用的每個數字能以其 commit SHA 來源回查。
- A 的 H1–H3、Graph K 指標與 C 的 liaison O/E 不被混成單一「相同結構洞檢定」。
- 新增 B 資料後才更新三軌結論，保留 A/C frozen snapshot 和 B 本身的版本。
- 任何 B 中止、未通過或未完成零模型，都明示為 `INCOMPLETE` 或 `INCONCLUSIVE`，絕不代替成 `0` 或 `NO_HOLE`。
- GitHub push 不會自動修改此頁；使用者告知實際 B SHA 後，再做來源核對、網頁更新與部署。

## 4. 相關公開位置
- `three-source-network.html` 教授版三軌比較頁。
- `data/three-source-evidence-20261125.json` 來源鎖定的 A/C 快照與 B 空欄位。
- 原研究正本不受此教學網站更動。
