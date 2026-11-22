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
- GitHub `has_pages=false`（2026-11-22 檢查時）；GitHub 來源檔更新不等於 Pages 已公開部署。
- 本次修改透過獨立 `docs/research-portfolio-20261122` 分支及 PR 提交，未合併 main。
- 舊歷史頁的文字與數值未被覆寫，只有新的導覽通知。
