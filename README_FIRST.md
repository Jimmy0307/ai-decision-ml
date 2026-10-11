# READ FIRST — Enterprise AI Adoption v2.3 empirical-execution candidate

本分支目前唯一 canonical working line：

**企業人工智慧導入作為多層級決策系統：治理、能力配置、組織採用與價值實現。**

## v2.3 執行系統（先讀）

v2.3 不擴充模型，只把 v2.2 已收斂的模型接上真實資料。

| 檔案 | 用途 |
|---|---|
| `59_V1_HUMAN_VALIDATION_IMPORT_AND_ADJUDICATION_v2_3.md` ＋ `60_v1_human_validation_analyzer_v2_3.py` | 人類 G→M 盲編的匯入、信度、裁決、mapping sensitivity、G04／G10／G11 追蹤；目前 `V1_HUMAN_BLIND_CODING_PENDING` |
| `61_EAX_HUMAN_CVI_ANALYZER_v2_3.py` ＋ `eax_cvi_import/` | EA-X 人類 CVI；目前 `CONDITIONAL_CANDIDATE` |
| `62_ENTERPRISE_EMPIRICAL_DATA_TEMPLATE_v2_3/`（CSV＋.xlsx＋字典） | 以 43 為唯一契約的企業資料樣板 |
| `63_MINIMUM_IDENTIFIABLE_ENTERPRISE_PILOT_v2_3.md` ＋ `63_MINIMUM_PILOT_SKELETON_v2_3/` | 最小可解 pilot 與 Q1–Q8 識別表；全 UNIDENTIFIED 的骨架 |
| `64_EMPIRICAL_DATA_COLLECTION_PRIORITY_v2_3.md` | 依閘門、regret 抵銷與 VOI 排序的量測優先序 |
| `65_enterprise_data_loader_v2_3.py` | validate → coverage → 51 instance → B／C／A+／C0／A → 第四章表格；registry 登記與 robust／VOI |
| `44_MANUSCRIPT_ENTERPRISE_AI_DECISION_v2_3.md` | 第四章改為可回填骨架（無任何結果） |

第一批資料後的指令：`python 65_enterprise_data_loader_v2_3.py --validate DATA` → `--run DATA` →（有區間時）`--make-registry` → commit → `--robust`。

## 閱讀順序（v2.2 基礎）

1. `58_V2_2_FORENSIC_AUDIT_AND_FREEZE_STATUS.md` — v2.2 freeze 狀態、六項稽核、blockers（supersedes 48）。
2. `41_G01_G16_CONVERGENCE_AND_CONSTRUCT_FREEZE_v2_1.md` — G01–G16 收斂（研究者裁決；G04、G10、G11 經 AI pilot 標為爭議，見 54C）。
3. `42_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md` — canonical model（supersedes 42 v2.1；修訂見 §20）。
4. `43_PARAMETER_IDENTIFICATION_AND_QUANTIFICATION_v2_1.md` — 參數識別（未變）。
5. `44_MANUSCRIPT_ENTERPRISE_AI_DECISION_v2_2.md` — canonical 稿件 v2.2（已以 100,827-byte Drive v2.1 權威全文完成三方 reconciliation）。
6. `45_MODEL_VALIDATION_AND_SOLVER_PLAN_v2_2.md` — 測試清單與 V0–V7。
7. `50_SOLVER_COMPLETION_AND_V3_V6_VALIDATION_v2_2.md` — 20 項 synthetic 檢查證據、兩輪稽核、獨立手算 oracle。
8. `51_enterprise_portfolio_solver_v2_2.py`、`52_SOLVER_ORACLE_RUN_v2_2.txt` — `SIMULATED_ONLY` reference oracle（`V2_2_SYNTHETIC_ENGINEERING_VERDICT: PASS`）。
9. `53A`（sealed-key commitment）、`53B`（V1 盲編 protocol，預先登記判準）、`54A`／`54B`（盲化題包）、`54C`（AI-BLIND-CODING PILOT）、`55`（裁決模板）、`v1_blind/`、`v1_human_packet/`（人類編碼者用）。
10. `56_EAX_CONTENT_VALIDITY_PACKET_v2_2.md` — EA-X 內容效度（AI pilot＋人類評分用 v2.2.1 錨點）。
11. `57_REFERENCE_VERIFICATION_CLOSURE_v2_2.md` — 引文核對。
12. `49_V5_CORPUS_LINEAGE_RECONCILIATION_v2_1.md` — V5 corpus lineage（已調和）。

v2.1 的 42、44（locator）、45、46、47、48 保留作 provenance。

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
- `SYNTHETIC_ORACLE_PASS`／`V2_2_SYNTHETIC_ENGINEERING_VERDICT: PASS` 只代表模型／程式在合成實例的一致性。
- 兩個 LLM 編碼者的結果不得當作人類 V1 PASS；目前 `V1_AI_PILOT_COMPLETE`、`V1_HUMAN_BLIND_CODING_PENDING`。
- 人類編碼者只拿 `v1_human_packet/`，不得取得本 repository（54C 已揭露答案鍵）。