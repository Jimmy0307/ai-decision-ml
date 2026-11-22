# AI × Decision｜2026-11-22 研究兩軌與五層證據網站

本資料夾是新增的公開說明網站。原有 `docs/index.html`（V5–V11.1 2026-11-18 版本）完整保留，僅加入入口提示。所有網站頁面使用靜態 HTML/CSS，不使用外部 API、分析追蹤或第三方素材。

## 頁面
- `index.html`：兩條研究線、核心結論、Gate 狀態
- `original.html`：權威 V1.8.7、功能分析、MLP 與編碼效度
- `five-layers.html`：R/K/F/N/O、研究二 vs 專利 R2/R4、CPC、E9、M0–M3
- `advisor.html`：教授決策、Gate 0–4、B1/M1–M8、人工校準、停止條件
- `styles.css`：響應式版面和無 JS 互動

## 研究來源與資料層級
1. 權威原始稿：私人備份庫中 `V1_8_7_THEORY_GROUNDING_Q1_PROPAGATION_FINAL_20261021/01_V1_8_7_MANUSCRIPT.md`（研究者提供權威指定；需授權瀏覽）。
2. 公開論文分支：`Jimmy0307/ai-decision-ml` / `paper/ai-decision-manuscript-20261119` / `paper/zh/ch4_results.tex`（2026-11-20）。
3. 新研究凍結分析：私人備份庫 `research/cooccurrence-mechanisms-20261120`，commit `3113033d816cd7bf193dd584033df7bdaea47b90`；其中 `INTEGRATED_MANUSCRIPT_20261121`、`LAYER_MISMATCH_E9_20261121`、專利軌 `17`、`20`、`22`。
4. Gate 0–4 與 2026-11-22 決策準備：研究者在對話提供之本機代理執行摘要。實際檔案在 `C:\Users\user\ntust-worktrees\gates-20261121\GATES_AUDIT_20261121\`，**未上傳 GitHub，也尚未由本網頁開發流程獨立重算**。網站將其標示為「本機報告／待審議」。
5. 資料與結論不等價：研究二 3.05 為預先登錄的相對規則；專利 R2 0.35–0.38 為不同凍結絕對判準；全體參照 3.58–3.90 是事後；R4 2.81–2.92 全體參照雖在 R4 前凍結，參照選擇已知曉 R2 結果。

## 發布邊界
- 不包含原始專利、第三方摘要、文獻全文、人類審查包、私人關鍵字、個人或企業內部資料。
- 正式網站已由 Vercel Production 部署：https://ai-decision-research.vercel.app/；GitHub Pages 未啟用，兩者是不同服務。
- 2026-11-22 初版已經由 PR #8 合併至 `main`；本次圖解補強先在獨立 `docs/structural-hole-logic-20261122` 分支審查與發佈。
- 舊歷史頁的文字與數值未被覆寫，只有新的導覽通知。

## 2026-11-22 補充：從低整合到 Burt 結構洞的圖解
- 首頁新增「研究 A → 延伸問題 → 研究 B」可視化流程。
- 五層頁新增 `#structural-hole`：開放／閉合三元組 SVG、Burt constraint、文獻固定邊際配對期望、專利分層 O/E、構造性不可識別反例、R/K/F/N/O 推論流程及停止規則。
- 教授頁新增導覽連結；依使用者 11/22 最新回報修正第二輪決策審查狀態。
- 公式來源為公開論文分支 `paper/zh/ch2_literature.tex`、`paper/zh/ch4_results.tex`，不得將共現 O/E 視為 Burt network constraint。
- 概念圖與 W1/W2 皆為教育性例子，不是經驗發現；M0–M3 的確認性結果仍待真人標註。

## 2026-11-22 教授零基礎導覽
- `index.html` 重構為完整八步教學（點與線、Burt、文獻矩陣、16 格、研究延伸、專利 O/E、M0–M3、教授決策），`research-notes.html` 保存前版首頁。
- `original.html` 新增逐步研究來源、固定邊際期望公式、MLP 企業三層決策解釋。
- `five-layers.html` 新增五層的日常例子、雙世界可識別性反例、三套 O/E 的非技術說明。
- `advisor.html` 新增四步口頭解說與三條論文定位路線。
- 所有示意圖與假設例子不當成實際研究數據；正式結論與人工證據限制保留。

## 2026-11-22 依私人庫研究甲乙解說修訂
- 主要來源：`audit/gates-20261121` commit `01698f3`，`STUDY_EXPLAINERS_20261122/STUDY_A_*` 和 `STUDY_B_*`；確認權威 V1.8.7 中企業模型為企業—事業單位**雙層 MLP**。
- 新增 `study-map.html`：共用文獻根源 → 研究甲轉譯/雙層 MLP 與研究乙五層跨層檢核的雙軌 SVG、四項機制、通式公式、證據強度、教授會議說明。
- `index.html`、`original.html`、`five-layers.html`、`advisor.html` 增加視覺入口並矯正「原始研究三個研究階段」誤認為「原始 MLP 三層」的版本混淆。
- 研究二公司分隔 p=.001 正確來源是**計畫 4**（受資料啟發的預先登錄；度數未固定），計畫 6 是 `INVALID_NULL`；專利 R2 只能稱為**事先凍結絕對判準**，不可直接稱正式事前預註冊。
- 未直接修改私人庫的稽核勘誤提案、原始權威稿、原始凍結 protocol 或研究甲/乙的正式研究結果。

## 教授理解結構洞的核心教學新增（2026-11-22）
- 新增 `abc-to-patents.html`：B 被移除、開放三元組與閉合三元組的 SVG 對照；零值、偏低、缺邊與 Burt 結構洞的四概念區分；5/20 純教學 O/E；16 個零值格與 16 個非零不足格的差別；專利文件四種證據（可得的文字、CPC、引用、申請人）；七個步驟（0–6）的交叉檢核；研究二/R2/事後 O/E 和仲介結果；人工真值阻塞；教授兩分鐘講稿。
- 教學頁直接引用私人 audit 分支 Study A/B 解說與公開論文第二、四章。未把專利引用當成真實功能使用，不將事後參照視為新確認性結果。
- 首頁、研究演進圖、研究乙頁及教授決策頁加入新頁導覽；不變動 canonical、凍結研究稿或私人審查內容。

## 2026-11-22 來源先行與八張圖入門改版
- abc-to-patents.html 重新編成八張大圖：三人網絡、文獻擷取、零值/偏低、專利資料卡、CPC 分類、O/E 基準、專利/公司仲介、A 輸出是否被 B 使用。每張左圖／右公式／下方來源與可說/不能說；手機不隱藏公式。
- sources-for-professor.html 來源圖鑑：研究甲文獻、PatentsView、官方 CPC 修訂、E5、E4/E9、Crossref 以及目前沒有的雙人真值與企業資料。每份資料的來源與研究結果分開介紹。
- 公開數字依研究甲/乙私人解說及公開論文分支；5/20、6/2、6/12 都是明確標示的教學示例。
- 不更改正式研究、私人 audit 分支、人類盲審包或凍結預先登錄。
