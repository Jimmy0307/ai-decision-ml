# GitHub Pages 發布設定｜AI × Decision 研究總覽

## 目前狀態（2026-11-17）

資料與 HTML **已提交到公開 repository `Jimmy0307/ai-decision-ml` 的 `main` 分支**，入口為 `docs/index.html`，所有相對連結均指向 `docs/` 下的稽核報告、老師會議摘要、JSON 狀態與 CSV。

**本紀錄沒有宣稱 Pages 已部署成功。** GitHub 內容已存在，但 Pages 設定／實際部署 URL 尚無可核驗的成功回傳。

## 一次性操作

1. 開啟 https://github.com/Jimmy0307/ai-decision-ml/settings/pages
2. 在 **Build and deployment → Source** 選 **Deploy from a branch**。
3. **Branch** 設為 `main`，**Folder** 設為 `/docs`，按 **Save**。
4. 到 Actions 查看 `pages build and deployment` 是否成功，並於 GitHub Pages 設定頁按 **Visit site**。
5. 典型 Pages 位址為 `https://jimmy0307.github.io/ai-decision-ml/`，但**僅以 GitHub 設定頁實際顯示的公開連結與成功部署狀態為準**。

## 驗收要求

- 首頁包含「本週研究進展｜2026/11/12–11/17」及「為何重新掃描」。
- 版本表 13 條、方法表 20 條、來源數字 90 條。
- V11.1 = 0 confirmed；3 rejected + 1 insufficient；95 API calls **標註 USER_REPORTED**。
- V9 = 32 robust、16 depleted，但必須同時顯示 `FULL_REANALYSIS_REQUIRED`。
- Limitation = 25,112 選取片段初篩，**不得**標成已證明無人解決的研究缺口。
- HTML 頁面內點擊三份 CSV、完整稽核報告、老師會議摘要、狀態 JSON，皆應可以閱讀。

官方說明：https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
