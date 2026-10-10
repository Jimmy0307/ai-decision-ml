# READ FIRST — Enterprise AI Adoption v2.1 candidate

本分支目前唯一 canonical working line：

**企業人工智慧導入作為多層級決策系統：治理、能力配置、組織採用與價值實現。**

## 閱讀順序

1. `48_FORENSIC_AUDIT_AND_V2_1_FREEZE_STATUS.md` — freeze 狀態、已修缺陷、剩餘 open gates。
2. `41_G01_G16_CONVERGENCE_AND_CONSTRUCT_FREEZE_v2_1.md` — G01–G16 收斂至 M1–M4／M5／optional／evidence-only。
3. `42_ENTERPRISE_PORTFOLIO_MODEL_v2_1.md` — canonical Enterprise–Business Unit bilevel portfolio model。
4. `43_PARAMETER_IDENTIFICATION_AND_QUANTIFICATION_v2_1.md` — 每個參數的識別需求與缺值後果。
5. `44_MANUSCRIPT_ENTERPRISE_AI_DECISION_v2_1.md` — Ch1–3 完整、Ch4–6 skeleton、reference audit。
6. `45_MODEL_VALIDATION_AND_SOLVER_PLAN_v2_1.md` — V0–V7、solver 與 sensitivity 尚待項。
7. `46_enterprise_portfolio_solver_v2_1.py`、`47_SOLVER_ORACLE_RUN_v2_1.txt` — `SIMULATED_ONLY` reference oracle。
8. `49_V5_CORPUS_LINEAGE_RECONCILIATION_v2_1.md` — V5 corpus lineage 已調和。

38–40 為 v2.0 上游 provenance；26、29、30、33–36 為早期 theory／audit／synthetic evidence，不再高於 41–49。

## V5 corpus provenance

G01–G16 的正式 network lineage 採 V5 analytical freeze：

`6,499 strict → 3,125 fully mapped/pair-eligible records → 783 pair-eligible documents → M=2,180 document-level edges`

Stage 2 unresolved mapping 使用 `qwen2.5:14b` constrained double-pass。較早的 404 publications／2,425 strict records／GPT-5.6 lineage 是 predecessor corpus 歷史，不是本版 G01–G16 denominator。

## 不可違反

- 不把單一部門、流程或 application 當研究本體。
- 不把 G01–G16 當企業問題、效用權重或係數。
- 不把 ordinal 0–3 當 cardinal utility。
- 不把 missing 補 0。
- shared cost 不可跨 unit 重複扣除。
- 外部 productivity effect 不可當企業自身 effect。
- user layer 預設為 conditional response，不為了 multilevel 名稱硬造第三層 optimizer。
- `SYNTHETIC_ORACLE_PASS` 只代表模型／程式在合成實例的一致性。