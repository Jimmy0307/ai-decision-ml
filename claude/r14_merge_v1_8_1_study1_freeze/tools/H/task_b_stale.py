"""Task B/C (V1.8.1, agent H): current copies of 128/131/133/137 with stale V9 / 2026-09-29 /
full-reanalysis status cleaned up line by line. Historical files are read-only.

Usage: python -I task_b_stale.py <HIST_DIR> <OUT_DIR>
Writes OUT/current_artifacts/{128,131,133,137}_..._v1_8_1.md and task_b_out.json (edit log).
Every edit is (file, historical line no, old substring, new substring, classification); each old
substring must occur exactly once on that line, so nothing outside the listed spans can change.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import hashlib, json, os

HIST, OUT = sys.argv[1], sys.argv[2]
CA = os.path.join(OUT, 'current_artifacts')

M = '〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：V9 source package recovered and partially verified in V1.8〕'
T = ('FULL_REANALYSIS_METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；'
     'FULL_REANALYSIS_EXECUTION_STATUS=NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET；'
     'FULL_REANALYSIS_PRIORITY_BEFORE_V1=NOT_RECOMMENDED')
H, C = 'HISTORICAL_ENV', 'CURRENT_STATUS'

FILES = {
    '128': ('128_CANONICAL_STATE.md', '128_CANONICAL_STATE_v1_8_1.md'),
    '131': ('131_HUMAN_VALIDATION_INTEGRATION_REPORT.md', '131_HUMAN_VALIDATION_INTEGRATION_REPORT_v1_8_1.md'),
    '133': ('133_V0_V7_VALIDATION_LEDGER.md', '133_V0_V7_VALIDATION_LEDGER_v1_8_1.md'),
    '137': ('137_NEXT_ACTIONS.md', '137_NEXT_ACTIONS_v1_8_1.md'),
}


def hist(s):
    return (s, s + M, H)


EDITS = {
    '128': [
        (10, *hist('使用者列出的優先來源中，以下 **不在本工作環境中**（uploads 目錄為空，全檔系統搜尋無結果）：')),
        (14, '| `20260929_V9_HUMAN_VALIDATION.zip` | **ABSENT** |',
         '| `20260929_V9_HUMAN_VALIDATION.zip` | **RECOVERED；V9_SOURCE_VERIFIED=PARTIAL（V1.8）**（v1.7 時記為 ABSENT） |', C),
        (14, *hist('人工標籤替換的局部敏感度結果（+人機增能 × 風險評估；−協調與執行 × 一般決策流程）與 `HUMAN_AUDIT_CONVERGED / LOCAL_SENSITIVITY_CHANGED / FULL_REANALYSIS_REQUIRED` 狀態，在本環境中**唯一來源是使用者 2026-10-13 的指示文字**。')),
        (14, 'κ 值、50/20/19 筆數可由 R14 定稿獨立核對（相符）。',
         'κ 值、50/20/19 筆數可由 R14 定稿獨立核對（相符）。現況：V9 source package recovered and partially verified in V1.8——'
         'zip sha256 `8f63e88e…`；替換結果與狀態旗標已由 `ROBUST_CORE_LOCAL_SENSITIVITY.csv`（`e3166ee1…`）與 `FINAL_STATUS.json`'
         '（`d9226d31…`，verified_at 2026-10-03T12:23:44Z）逐列核對（`02_V9_AUTHORITY_MAP.md`、`04_LOCAL_SENSITIVITY_REPRODUCTION.md`）；'
         '12/37 受保護輸入仍未尋回。完整重分析現行狀態：' + T + '（`07_FULL_REANALYSIS_DECISION_MEMO.md` §8）。', C),
        (15, '| `完整資料來源.zip` | **ABSENT** |',
         '| `完整資料來源.zip` | **PRESENT IN V1.8 INPUTS（sha256 `138dbeac…`）— LEGACY_HISTORICAL_PROVENANCE**（v1.7 時記為 ABSENT） |', C),
        (15, 'V5 Manuscript Data Pack 本體未在環境中；',
         '`LEGACY_HISTORICAL_PROVENANCE — STRUCTURAL-HOLE / CITATION-NETWORK STUDY PACKAGE (NOT THE V5 DATA PACK); REAL_V5_DATA_PACK=NOT_RECOVERED`'
         '（`05_LEGACY_SOURCE_BOUNDARY.md` §1、§3.4，sha256 `03205f44…`；v1.7 誤稱為「V5 Manuscript Data Pack 本體」）；', C),
        (16, '| `投稿格式.pdf`、`投稿範例.pdf`、`全文投稿樣板 windows (2).docx` | **ABSENT** |',
         '| `投稿格式.pdf`、`投稿範例.pdf`、`全文投稿樣板 windows (2).docx` | **ABSENT**（V1.8 仍為 OPEN_SOURCE_NOT_FOUND：`06_SOURCE_FLAG_CLOSURE.csv` 128 L16） |', C),
        (17, '| Google Drive 版本 | **無法存取**（本工作階段無 Drive 連接器） |',
         '| Google Drive 版本 | **無法存取**（本工作階段無 Drive 連接器；V1.8 仍未核對：`06_SOURCE_FLAG_CLOSURE.csv` 137 L10 OPEN_SOURCE_NOT_FOUND） |', C),
        (29, '(b) 人工標籤替換局部敏感度與稽核狀態：V9 套件（2026-09-29）——**artifact 不在環境中，僅使用者陳述**。',
         '(b) 人工標籤替換局部敏感度與稽核狀態：V9 套件（資料夾 `20260929_V9_HUMAN_VALIDATION`；`FINAL_STATUS.json` 驗證時間 2026-10-03T12:23:44Z）——'
         '**V9 source package recovered and partially verified in V1.8**（`02_V9_AUTHORITY_MAP.md` §7 權威檔案集；`04_LOCAL_SENSITIVITY_REPRODUCTION.md`）。', C),
        (29, '(b) **USER-REPORTED, ARTIFACT PENDING**',
         '(b) **V9_SOURCE_VERIFIED=PARTIAL（V1.8；50/20/19、κ、局部敏感度成員由原始列重現）**', C),
        (29, 'R14 02:218, 361, 365–375；使用者指示 §4–5 |',
         'R14 02:218, 361, 365–375；使用者指示 §4–5；V1.8 `02`／`03`／`04` |', C),
        (44, *hist('目標式人工標籤替換後核心仍為 32 格，但 +人機增能 × 風險評估（不足）、−協調與執行 × 一般決策流程（過度）；`FULL_REANALYSIS_REQUIRED`')),
        (44, 'B 較新（09-29 > R14 docx 09-20）',
         'B 較新（V9 `FINAL_STATUS.json` 2026-10-03 > R14 docx 09-20；v1.7 原記 09-29）', C),
        (44, *hist('但 B 的原始 artifact 不在環境中')),
        (44, *hist('所有 B 的數字加 `[SOURCE: V9 human-validation state, 2026-09-29 — artifact not in workspace; verify before submission]`。')),
        (44, '**作者須提供 V9 套件以核對**（137 P0-1）。',
         '**V9 套件已取得並於 V1.8 逐列核對**：32 = 15／17、+1／−1、其餘 31 組不變、G01–G16 未移除（`04_LOCAL_SENSITIVITY_REPRODUCTION.md` T1–T3）；'
         'v1.8 稿件已將 V9 出處旗標改為來源引用（`06_SOURCE_FLAG_CLOSURE_NOTES.md` §3；`08_PATCH_LOG.md`）；137 P0-1 = PARTIALLY DONE。', C),
        (46, '並註明 Data Pack 原檔待核。',
         '並註明 Data Pack 原檔待核（V1.8：REAL_V5_DATA_PACK=NOT_RECOVERED；`完整資料來源.zip` 不是 Data Pack，見 `05_LEGACY_SOURCE_BOUNDARY.md` §3.4；'
         '同一模型摘要值另見 V9.1 `SEGMENT_STAGE2_MODEL_VERIFICATION.json`，`06_SOURCE_FLAG_CLOSURE.csv` 128 L46）。', C),
        (53, *hist('不適用（缺 2026-09-29 原始紀錄）')),
        (53, 'v1.7 改寫為「不同的測量操作；範圍可能部分重疊，待核」（E49）',
         'v1.7 改寫為「不同的測量操作；範圍可能部分重疊，待核」（E49）；V1.8 已核（`04_LOCAL_SENSITIVITY_REPRODUCTION.md` §3b）：'
         '標籤處理不重疊（V9.1 重切分未傳播任何人工標籤），記錄樣本部分重疊（50 筆受稽核記錄中 28 筆亦被重切分；其中 11 筆因人工錯誤標記被強制納入候選）', C),
        (64, '**未觸發，但 artifact 缺件**',
         '**未觸發**（v1.7 時 artifact 缺件；V1.8 已取得並核對）', C),
        (64, *hist('替換結果只見於使用者指示（CF-01）。')),
        (64, '替換結果只見於使用者指示（CF-01）。' + M,
         '替換結果只見於使用者指示（CF-01）。' + M + ' V1.8：50/20/19 與 κ 由原始列重現（`03_HUMAN_AUDIT_REPRODUCTION.md`；無 HUMAN_RELIABILITY_CONFLICT），'
         '替換結果由 `ROBUST_CORE_LOCAL_SENSITIVITY.csv` 逐列重現（`04`）。', C),
        (73, *hist('觸發的兩項（CF-01 缺件、CF-02 證據不足）已以「不猜、加出處旗標、改寫為可支持表述」處理，並列入 OPEN BLOCKERS。')),
    ],
    '131': [
        (14, '| 後續要求 | `FULL_REANALYSIS_REQUIRED` |',
         '| 後續要求 | V9 套件狀態標籤 `FULL_REANALYSIS_REQUIRED`（`FINAL_STATUS.json`；需研究者核准）；現行：' + T + '（`07_FULL_REANALYSIS_DECISION_MEMO.md` §8） |', C),
        (28, '| R14 定稿 §3.7.1、§4.6.1、表 5；V9 狀態紀錄 | 收斂；局部敏感；須完整重分析 |',
         '| R14 定稿 §3.7.1、§4.6.1、表 5；V9 人工驗證套件（V1.8 已取得並部分核對：`02_V9_AUTHORITY_MAP.md`） | 收斂；局部敏感；完整重分析：' + T + ' |', C),
        (40, '| R14 02:218、357 | ✔ 與使用者陳述一致 |',
         '| R14 02:218、357；V9 `FIRST_CODER_50_FINAL_FROZEN.csv`（`dd332dd8…`） | ✔ 與 V9 原始列一致（V1.8 `03_HUMAN_AUDIT_REPRODUCTION.md`） |', C),
        (42, '✔（使用者稱 19/19 reconciliation）',
         '✔（V9 `HUMAN_RECONCILED_20.csv`（`4b7ceac2…`）＋調和事件雜湊鏈 19/19；V1.8 `02` §2、`03` 重現）', C),
        (44, '| R14 表 5、02:361 | ✔ 與使用者陳述一致 |',
         '| R14 表 5、02:361；V9 `HUMAN_RELIABILITY_FINAL.csv`（`ef7e5544…`） | ✔ 與 V9 原始列重算一致（V1.8 `03`：.5614／.1798／.0476／.1398／.3162） |', C),
        (51, '| 使用者陳述（V9，2026-09-29） | ✖ 原始檔案不在環境中 |',
         '| V9 `FINAL_STATUS.json`（`d9226d31…`；verified_at 2026-10-03T12:23:44Z）；完整重分析現行三元組：' + T +
         ' | ✔ V1.8 已核（`02_V9_AUTHORITY_MAP.md` §4、§7）；V9_SOURCE_VERIFIED=PARTIAL |', C),
        (52, '| 使用者陳述（V9） | ✖ 原始檔案不在環境中；兩個配對在 R14 中的位置已核（下節） |',
         '| V9 `ROBUST_CORE_LOCAL_SENSITIVITY.csv`（`e3166ee1…`）／`_DIFF.csv`（`f6607aae…`） | ✔ V1.8 逐列核對（`04_LOCAL_SENSITIVITY_REPRODUCTION.md` T1、T3）；兩個配對在 R14 中的位置已核（下節） |', C),
        (53, '| 使用者陳述；R14 02:361',
         '| V9 `FINAL_ERROR_TAXONOMY.csv`（`68e97c01…`）／`.md`（`33044106…`）；R14 02:361', C),
        (53, '作為四分類的整理來自 2026-09-29 紀錄；',
         '作為四分類的整理來自 V9 錯誤型態表（V1.8 部分核對，`06_SOURCE_FLAG_CLOSURE_NOTES.md` §4）：V9 將其列為模型標籤與人工標籤差異的詮釋性假說（非裁決），'
         '並另列第五類 `TRUE_CONCEPTUAL_AMBIGUITY`，不是對 19 筆編碼者間分歧的歸類；', C),
        (90, '**表 H-2：成員變動（V9；待以原始檔案核對）**',
         '**表 H-2：成員變動（V9 `ROBUST_CORE_LOCAL_SENSITIVITY.csv`；V1.8 已逐列核對，`04` T1）**', C),
        (97, '推得（不是新的觀察）：若無其他未回報的變動，凍結核心其餘 31 組不變，替換後集合為 15 過度／17 不足；G01–G16 全部保留；新增的不足呈現不屬 G01–G16。稿件以「依回報的變動推得」標示，並列入附錄 E39 待核。',
         'V1.8 逐列核對（`04_LOCAL_SENSITIVITY_REPRODUCTION.md` Q1–Q3、T1–T3）：核心成員沒有其他變動，凍結核心其餘 31 組成員與方向不變，替換後集合為 15 過度／17 不足；'
         'G01–G16 全部保留；新增的不足呈現不屬 G01–G16。核心以外，120 格中共 33 格有計數或非核心方向差異（不影響核心成員）。'
         'v1.7 原以「依回報的變動推得」標示並列入附錄 E39 待核；v1.8 已改以 V9 逐列結果表述（E39 已核）。', C),
        (103, '3. 成員有變 → 須完整重分析；不以替換後集合取代凍結結果。',
         '3. 成員有變 → 完整重分析列為 V9 的開放驗證行動（' + T + '；`07` §8）；不以替換後集合取代凍結結果。', C),
        (104, 'R14 註明重切分設定中「人工調和標籤不傳播至未稽核記錄」，受稽核記錄在重切分中是否已使用人工標籤待核（E49），因此兩者的處理範圍可能部分重疊。',
         'R14 註明重切分設定中「人工調和標籤不傳播至未稽核記錄」；V1.8 已核（`04` §3b，E49）：重切分未傳播任何人工標籤（受稽核但未被重切分的 22 筆在 S1／S2 中 22/22 保留模型家族），'
         '因此標籤處理不重疊；但記錄樣本部分重疊（50 筆中 28 筆亦被重切分，其中 11 筆因人工錯誤標記被強制納入候選）。', C),
        (145, '1. **V9 原始檔案缺件**：替換清單、替換後矩陣、變動配對、是否有其他未回報的變動、「凍結核心其餘 31 組不變」皆待核（E39）。',
         '1. **V9 原始檔案：已取得並於 V1.8 部分核對**：替換清單（`04` T4）、變動配對、無其他核心成員變動、「凍結核心其餘 31 組不變」皆已逐列核對（E39）。'
         '殘留：替換後 q 值的產生腳本與 sidecar 核心檔 NOT_RECOVERED（只重現成員與判準，未重跑零模型）；12/37 受保護輸入未尋回；'
         '`HUMAN_AUDIT_APPEND_ONLY_LOG.csv` 受保護雜湊不符（UNVERIFIED，無竄改證據）（`02` §5）。', C),
        (146, '2. **完整重分析的時點與範圍**，',
         '2. **完整重分析的時點與範圍**（現行：' + T + '；`07` §8；是否重跑仍屬研究者決定），', C),
        (147, '矩陣重建方式、檢定組合、隨機種子。',
         '矩陣重建方式、檢定組合、隨機種子。V1.8 部分解答：50 筆皆替換（20 筆用調和 FINAL 標籤、30 筆用第一位編碼者標籤；未稽核記錄不變，`04` Q4）；'
         '依 V9 `ROBUST_CORE_LOCAL_SENSITIVITY.md` 摘要（未逐列重現）：主零模型 10,000 次、seed 20260918；文獻內部結構保持零模型 5,000 次、seed 20260919；'
         '產生腳本 NOT_RECOVERED，標籤→納入資格的傳播規則 UNRESOLVED。', C),
        (148, '4. **兩種敏感度的處理範圍是否重疊**（E49）。',
         '4. **兩種敏感度的處理範圍是否重疊**（E49）。V1.8 已核：標籤處理不重疊；記錄樣本 28/50 重疊（`04` §3b）。', C),
    ],
    '133': [
        (34, '| LOCAL_SENSITIVITY_CHANGED；FULL_REANALYSIS_REQUIRED |',
         '| LOCAL_SENSITIVITY_CHANGED；V9 標籤 FULL_REANALYSIS_REQUIRED → 現行 ' + T + ' |', C),
        (34, '| 2026-09-29 人工驗證紀錄（檔名含 V9；不是驗證閘門；原始檔案缺件） |',
         '| V9 人工驗證套件（資料夾 20260929_V9_HUMAN_VALIDATION；V9 是檔案版本名，不是驗證閘門）之 `FINAL_STATUS.json`（2026-10-03）與 '
         '`ROBUST_CORE_LOCAL_SENSITIVITY.csv`（`e3166ee1…`）；V9 source package recovered and partially verified in V1.8（`02`、`04`） |', C),
        (34, '| 格數 32；±1 成員（依作者回報） |',
         '| 格數 32（15／17）；±1 成員（V1.8 逐列核對，`04` T1）；G01–G16 未移除 |', C),
    ],
    '137': [
        (10, '| P0-1 | P0 | **canonical source conflict：取得 V9 人工驗證原始檔案**（`20260929_V9_HUMAN_VALIDATION.zip`），並確認 Drive 上沒有比 R14／V9 更新的版本 |',
         '| P0-1 | P0 | **[PARTIALLY DONE — V1.8]** **canonical source conflict：取得 V9 人工驗證原始檔案**（`20260929_V9_HUMAN_VALIDATION.zip`）＝**DONE**'
         '（已取得，zip sha256 `8f63e88e…`；於 V1.8 部分核對：`02_V9_AUTHORITY_MAP.md` V9_SOURCE_VERIFIED=PARTIAL），'
         '並確認 Drive 上沒有比 R14／V9 更新的版本＝**OPEN**（作者確認；`06_SOURCE_FLAG_CLOSURE.csv` 137 L10） |', C),
        (10, *hist('稽核狀態旗標與標籤替換結果在本環境只有作者陳述；')),
        (10, '以原始檔案核對：替換清單、替換後矩陣、兩個變動配對、凍結核心其餘 31 組不變、是否有其他未回報的變動、15／17；不一致時以原始檔案重寫各處；移除 V9 旗標',
         '以原始檔案核對——V1.8 結果：✔ 替換清單（50 筆，`04` T4）；✔ 兩個變動配對；✔ 凍結核心其餘 31 組不變；✔ 無其他核心成員變動（另有 33/120 格計數或非核心方向差異）；'
         '✔ 15／17；✔ 無數值不一致，無須重寫數值；✔ v1.8 稿件移除 V9 旗標（`08_PATCH_LOG.md`）；✔ 132 於 V1.8.1 重新產生（`11_ARTIFACT132_SOURCE_CLOSURE_REPORT.md`）。'
         '殘留：替換後矩陣的產生腳本與 sidecar 核心檔 NOT_RECOVERED（q 值未重算）；12/37 受保護輸入 NOT_RECOVERED', C),
        (12, '**文獻層完整重分析的決策**（FULL_REANALYSIS_REQUIRED；含 E49：兩種敏感度的處理範圍是否重疊）',
         '**文獻層完整重分析的決策**（V9 標籤 FULL_REANALYSIS_REQUIRED；現行：' + T + '；E49 已於 V1.8 核定：標籤處理不重疊、記錄樣本 28/50 重疊）', C),
        (12, '作者決定「投稿前重分析」或「投稿稿明載凍結基準＋局部敏感度」；',
         '作者決定「投稿前重分析」或「投稿稿明載凍結基準＋局部敏感度」；V1.8 建議為後者（`07_FULL_REANALYSIS_DECISION_MEMO.md` §8），但仍屬研究者決定；'
         '若選擇重跑，須先通過 `07` §4 閘門（受保護輸入回復並雜湊比對），標籤輸入只能用 `04` T4，傳播規則須事前宣告（`15_REANALYSIS_INPUT_GOVERNANCE.md`）；', C),
        (12, '| 作者；重分析需 V5 pipeline | P0-1 |',
         '| 作者；重分析需 V5 pipeline | P0-1（V9 部分已完成） |', C),
        (22, '格式檔案不在環境中；',
         '格式檔案不在環境中（V1.8 仍為 OPEN_SOURCE_NOT_FOUND，`06_SOURCE_FLAG_CLOSURE.csv` 137 L22）；', C),
        (35, *hist('P0-1 只需要作者把 `20260929_V9_HUMAN_VALIDATION.zip`（以及若有更新的 R14／Drive 版本）放進這個工作階段；核對與重寫可在同一輪完成。')),
        (35, '核對與重寫可在同一輪完成。' + M,
         '核對與重寫可在同一輪完成。' + M + ' 現況：V9 部分已於 V1.8 完成；P0-1 只剩 Drive 對帳（作者確認）。不需要外部資料的下一步：'
         '依 `15_REANALYSIS_INPUT_GOVERNANCE.md` 事前宣告 UNCERTAIN／AMBIGUOUS／UNMAPPED 的傳播規則（P0-3 的前置條件；不執行重分析）。', C),
    ],
}

HEADER = """> **CURRENT COPY (V1.8.1, 2026-10-14) — current copy; history preserved.**
> Historical source: `W\\01_ALL_OUTPUTS\\AI_DECISION_THESIS_ALL_OUTPUTS\\r14_merge_v1_7\\{src}` (sha256 `{sha}`), left unchanged.
> Changed: only stale V9-availability / 2026-09-29 / 依作者回報 / full-reanalysis status spans ({n} edits; line-by-line log in `claude/r14_merge_v1_8_1_study1_freeze/12_STALE_STATUS_CLEANUP_REPORT.md`, line numbers = historical file).
> Sentences describing the execution environment at that time are kept verbatim with the marker `〔SUPERSEDED_BY_V1_8_SOURCE_CLOSURE：…〕`; current-status sentences are updated with citations.
> File names 02–10 refer to `claude/r14_merge_v1_8_source_closure/`; 11/12/15 refer to `claude/r14_merge_v1_8_1_study1_freeze/`.
> No number, G01–G16 content, taxonomy, G→M assignment, model, solver, schema or empirical result was changed. `SUBMISSION_READY = NO`.

"""


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    os.makedirs(CA, exist_ok=True)
    log = []
    for key, (src, dst) in FILES.items():
        raw = open(os.path.join(HIST, src), 'rb').read()
        lines = raw.decode('utf-8').split('\n')
        for ln, old, new, cls in EDITS[key]:
            cur = lines[ln - 1]
            assert cur.count(old) == 1, (key, ln, old[:40], cur.count(old))
            lines[ln - 1] = cur.replace(old, new)
            log.append(dict(file=src, current_copy=dst, line=ln, old=old, new=new, classification=cls))
        body = '\n'.join(lines)
        out = HEADER.format(src=src, sha=sha(raw), n=len(EDITS[key])) + body
        with open(os.path.join(CA, dst), 'wb') as f:
            f.write(out.encode('utf-8'))
    json.dump(log, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'task_b_out.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    from collections import Counter
    print(Counter((e['file'][:3], e['classification']) for e in log), len(log))


if __name__ == '__main__':
    main()
