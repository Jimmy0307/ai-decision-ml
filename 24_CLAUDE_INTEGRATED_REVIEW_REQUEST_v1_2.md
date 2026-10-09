# 致 Claude｜JPC 研究架構與 Measurement Architecture v1.2 整合複審

請以 `calibration/v1.1-variable-model` 本輪新 commit 為審查基準，對照舊 `e9137d4`。**不要把 v1.0 求解器模擬 PASS 視為新架構已通過。** 新候選的正本為：`21_INTEGRATED_RESEARCH_ARCHITECTURE_CANDIDATE_v1_2.md`、`22_MEASUREMENT_AND_ELICITATION_CANDIDATE_v1_2.md`、`23_CORRECTION_VALIDATION_GATE_v1_2.md`；15–20 是先前 v1.1 審查歷史，若有衝突以 21–23 的候選修訂為準。

## 核心研究定位

文獻 G01–G16 → M1–M4 機制線索 → JPC use case 的 Boss → Manager → Junior 權力、設計和行為落差 → 情境界定的數學模型。全漢的關係企業與董事治理是須核實權限的外圍治理界面；兆豐創投是外部評估與反證，不是論文的主體、也不自動成為模型玩家。M5 為動態擴充，G04 為 evidence-only。

## 請以失敗優先的方式審

1. **F1**：逐一列出 21–22 中仍把序位 0–3 或 κ 當基數的方程／文字；查表或 `z_X` 方案有無明確單位、識別、作用點與保序重編碼規則？對 6/9 敏感性的修正是否仍只是承諾？
2. **F2**：Junior 的可行反應及效用、Manager 的反應依賴是否足以形成真正分散決策？請給反例，並列最低限度的權限／行為觀察及雙層、集中式對照。若仍不成立，請明確建議降級模型。
3. **F3**：共同卡與分配設計能否在 4–6 個實際 use case、約 14 個內部受訪者的負擔下辨認門檻？哪些主效應／交互作用根本無法識別？C6a/C6b 是否乾淨地分開可行和價值？
4. **文獻**：逐項核 Raisch、Elish、Bansal、Vaccaro、Shrestha、Jöhnk、Rudin、Miller；分 `SOURCE VERIFIED / ABSTRACT ONLY / UNVERIFIED`，避免把相關概念當特定方程的實證支持。請復核 M5、G04 的 V5 year 缺失及 gap 定義。
5. **整個論文**：研究問題、構念、案例、角色、門檻、方程、可識別性、外部效度是否形成同一條研究本體？全漢與兆豐的位置是否有權限誤設或把論文轉成投資報告？

請對每一問題回覆 `PASS / MAJOR CORRECTION / FAIL / UNVERIFIED`，引用檔名與具體段落或方程，給可落地的最小修正。請在最後給「可凍結項目」與「解除凍結所需證據」，明確分開文件修正、可執行實作、模擬驗證及實際觀察。若你有先前完整 A–J 報告與兩支診斷腳本，請將 R1–R12 的**原始編號和內容**逐一對上；若沒有，請勿推測編號。

這一輪的主張是 **修訂候選，仍未通過凍結**。不得因新文件把錯誤寫清楚就宣稱方程已被求解、門檻已識別、三層已實證存在。
