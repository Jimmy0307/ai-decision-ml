"""Build v1.8.1 CLEANUP CANDIDATE from v1.8 by exact old->new replacements.
Each `old` must occur exactly once in v1.8 and exactly once at apply time.
Usage: python -I patch_v181.py <v1.8 md> <v1.8.1 md out> <patches json out>"""
import sys, json, hashlib

SRC, DST, JOUT = sys.argv[1], sys.argv[2], sys.argv[3]
EXPECTED_SRC_SHA = "1515b0f241846b98a16bea7b13f07d1f82fa9199e1331c2228ffce1d04f7ad58"

raw = open(SRC, 'rb').read()
if hashlib.sha256(raw).hexdigest() != EXPECTED_SRC_SHA:
    sys.exit("STOP: V1.8 manuscript hash unexpectedly changed")

P = []


def add(pid, sec, cat, old, new, src):
    P.append(dict(id=pid, section=sec, category=cat, old=old, new=new, source=src))


# ---- shared wording -------------------------------------------------------
FR_SRC = ("V1.8 07_FULL_REANALYSIS_DECISION_MEMO.md §8; V1.8 02 §5 (12/37 protected inputs absent); "
          "V1.8.1 15_REANALYSIS_INPUT_GOVERNANCE.md §4; V1.8.1 17_STUDY1_EVIDENCE_FREEZE_v1.md §D; common_v181 terminology")
SEG_SRC = ("V1.8.1 13_SEGMENTATION_ATTRIBUTION_FORENSIC.md §0, §2 (recomputed from raw rows), §3, §4 proposed wording; "
           "V9/V9_1_SEGMENTATION_SENSITIVITY/SEGMENTATION_SENSITIVITY_FINAL_REPORT.md (2026-10-03T16:41:45Z)")
SHORT = "完整重分析列為開放的驗證行動，但以目前的來源集無法執行，在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定"
TBL = "完整重分析為開放驗證行動，以目前來源集無法執行，V1 前不建議優先執行（附錄 E40）"
SEG_TAG = ("〔來源：V9.1 證據單元重切分敏感度側車分析（V9 套件 `V9_1_SEGMENTATION_SENSITIVITY`，2026-10-03 產生；"
           "以凍結之主要分析為比較基準），R14 定稿第 4.6.2–4.6.3 節轉述；觀察值改變與方向改變格數已由兩種設定之文獻層級邊逐列重算核對〕")
FA = ("〔來源：V9 人工驗證套件（資料夾 20260929_V9_HUMAN_VALIDATION；V9 是檔案版本名，不是驗證閘門）之 FINAL_STATUS.json"
      "（驗證時間 2026-10-03）與 ROBUST_CORE_LOCAL_SENSITIVITY.csv；已逐列核對；附錄 E39")

# ---- 1. status line (L5) ---------------------------------------------------
add("J01", "稿件狀態", "status line (version label; Study 1 freeze; V1 packet READY_TO_RUN)",
    "合併碩士論文 v1.8 SOURCE-VERIFIED CANDIDATE（由 v1.7 修訂；v1.0–v1.7 保留、未覆寫；歷次版本說明移至附錄 F）。本版不新增任何分析，也不改變任何方程、模型元素、R14 數值或 G01–G16 凍結值；v1.7 已把既有證據的狀態收斂為一致的寫法，v1.8 再以 V9 人工驗證套件的原始檔案逐列核對其來源，只更新來源標示、日期與相應措辭。",
    "合併碩士論文 v1.8.1 CLEANUP CANDIDATE（由 v1.8 修訂；v1.0–v1.8 保留、未覆寫；v1.6 以前的版本說明見附錄 F，v1.7 以後的版本檔案見附錄 D）。本版不新增任何分析，也不改變任何方程、模型元素、R14 數值或 G01–G16 凍結值；v1.7 已把既有證據的狀態收斂為一致的寫法，v1.8 再以 V9 人工驗證套件的原始檔案逐列核對其來源；v1.8.1 只做清理：補上證據單元重切分數值的來源標示（V9.1 證據單元重切分敏感度側車分析，R14 轉述）、統一完整重分析的狀態寫法，並修正一處排版錯誤。同一輪另凍結文獻層（Study 1）的證據狀態（V1.8.1 檔案 17_STUDY1_EVIDENCE_FREEZE_v1.md），並備妥 V1 人類構念效度驗證封包（V1.8.1 檔案 19–21；狀態 READY_TO_RUN：已備妥、尚未執行，沒有任何人類編碼結果）。",
    "V1.8.1 17 §G; 19 L389 (V1_HUMAN_CONSTRUCT_VALIDATION_STATUS=READY_TO_RUN); this round")
add("J02", "稿件狀態", "FULL_REANALYSIS status wording",
    "V9 套件標記的完整重分析（FULL_REANALYSIS_REQUIRED）是否執行，仍為研究者待決事項（附錄 E40）；",
    "V9 套件標記的完整重分析（FULL_REANALYSIS_REQUIRED）在方法上列為開放的驗證行動（REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION），但以目前的來源集無法執行（37 項受保護輸入中 12 項未尋回；NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET），在 V1 人類構念效度驗證之前不建議優先執行（NOT_RECOMMENDED）；日後是否重跑仍由研究者決定（附錄 E40）；",
    FR_SRC)

# ---- 2. FULL_REANALYSIS wording elsewhere ----------------------------------
add("J03", "摘要", "FULL_REANALYSIS status wording",
    "凍結的 32 組仍為正式推論基準，完整重分析是否執行仍待研究者決定。",
    "凍結的 32 組仍為正式推論基準；" + SHORT + "。",
    FR_SRC)
add("J04", "Abstract", "FULL_REANALYSIS status wording",
    "and whether to run the full reanalysis flagged by the validation package remains an open researcher decision.",
    "and the full reanalysis flagged by the validation package remains an open validation action: it cannot be executed with the currently recovered source set (12 of 37 protected inputs are missing), it is not recommended as a priority before the V1 human construct validation, and whether to rerun it later remains a researcher decision.",
    FR_SRC)
add("J05", "1.4 研究問題", "FULL_REANALYSIS status wording",
    "局部敏感，完整重分析尚待執行（第 4.5.5 節）。",
    "局部敏感；" + SHORT + "（第 4.5.5 節；附錄 E40）。",
    FR_SRC)
add("J06", "表 1-1 研究問題二", "FULL_REANALYSIS status wording",
    "局部成員變動，完整重分析待執行 |",
    "局部成員變動；" + TBL + " |",
    FR_SRC)
add("J07", "1.5 研究設計概覽", "FULL_REANALYSIS status pointer (provenance bracket only; G-token line)",
    "完整重分析是否執行仍待研究者決定（第 4.5.5 節）" + FA + "〕",
    "完整重分析是否執行仍待研究者決定（第 4.5.5 節）" + FA + "；完整重分析的現行狀態（開放驗證行動、以目前來源集無法執行、V1 前不建議優先執行）見附錄 E40〕",
    FR_SRC)
add("J08", "1.6 推論邊界", "FULL_REANALYSIS status wording",
    "完整重分析尚待執行（第 4.5.5 節），逐格解讀因此依證據強度分層。",
    SHORT + "（第 4.5.5 節；附錄 E40）；逐格解讀因此依證據強度分層。",
    FR_SRC)
add("J09", "3.1 研究設計", "FULL_REANALYSIS status wording",
    "完整重分析尚待執行（第 3.7.4、4.5.5 節）。",
    SHORT + "（第 3.7.4、4.5.5 節；附錄 E40）。",
    FR_SRC)
add("J10", "3.1 研究流程圖（文字流程）", "FULL_REANALYSIS status wording",
    "凍結核心仍為推論基準；完整重分析待執行）",
    "凍結核心仍為推論基準；完整重分析為開放驗證行動，目前無法執行）",
    FR_SRC)
add("J11", "3.7.4", "FULL_REANALYSIS status wording",
    "依該檔，完整重分析須經研究者核准；是否在投稿前執行，仍為研究者待決事項（附錄 E40）。",
    "依該檔，完整重分析須經研究者核准；其現行狀態為：方法上列為 V9 的開放驗證行動，以目前的來源集無法執行（37 項受保護輸入中 12 項未尋回），在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（附錄 E40）。",
    FR_SRC)
add("J12", "3.8.1 表 3-3（L2′ 列）", "FULL_REANALYSIS status wording",
    "不取代 L2；完整重分析待研究者決定〔",
    "不取代 L2；" + TBL + "〔",
    FR_SRC)
add("J13", "4.5.5", "FULL_REANALYSIS status wording (status codes)",
    "最後一項是套件的狀態標記；依 FINAL_STATUS.json，完整重分析須經研究者核准，是否執行仍為研究者待決事項（附錄 E40）。",
    "最後一項是套件的狀態標記；依 FINAL_STATUS.json，完整重分析須經研究者核准。其現行狀態為：方法上列為 V9 的開放驗證行動（FULL_REANALYSIS_METHOD_STATUS = REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION）；以目前的來源集無法執行（37 項受保護輸入中 12 項未尋回；FULL_REANALYSIS_EXECUTION_STATUS = NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET）；在 V1 人類構念效度驗證之前不建議優先執行（FULL_REANALYSIS_PRIORITY_BEFORE_V1 = NOT_RECOMMENDED）；日後是否重跑仍由研究者決定（附錄 E40）。",
    FR_SRC)
add("J14", "4.11 表（研究問題二）", "FULL_REANALYSIS status wording",
    "凍結的 32 組仍為推論基準，完整重分析待研究者決定〔",
    "凍結的 32 組仍為推論基準；" + TBL + "〔",
    FR_SRC)
add("J15", "4.11 整合回答", "FULL_REANALYSIS status wording",
    "（人工標籤替換顯示局部成員敏感，完整重分析待執行）",
    "（人工標籤替換顯示局部成員敏感；完整重分析為開放驗證行動，以目前來源集無法執行，見附錄 E40）",
    FR_SRC)
add("J16", "5.3 表（功能低整合列）", "FULL_REANALYSIS status wording",
    "另新增一組不足呈現，待完整重分析 |",
    "另新增一組不足呈現；完整重分析為開放驗證行動，以目前來源集無法執行（附錄 E40） |",
    FR_SRC)
add("J17", "5.8.9", "FULL_REANALYSIS status wording (status codes)",
    "（V9 套件標記為 FULL_REANALYSIS_REQUIRED；是否及何時執行仍待研究者決定，附錄 E40）",
    "（V9 套件標記為 FULL_REANALYSIS_REQUIRED；現行狀態：FULL_REANALYSIS_METHOD_STATUS = REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION，FULL_REANALYSIS_EXECUTION_STATUS = NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET，FULL_REANALYSIS_PRIORITY_BEFORE_V1 = NOT_RECOMMENDED；日後是否及何時重跑仍由研究者決定，附錄 E40）",
    FR_SRC)
add("J18", "5.9 後續研究", "FULL_REANALYSIS status wording (priority/executability qualifier)",
    "以一致的標籤完成文獻層的完整重分析（第 5.8.9 節）",
    "以一致的標籤完成文獻層的完整重分析（第 5.8.9 節；執行前須先尋回缺件的受保護輸入，時程排在 V1 人類構念效度驗證之後，見附錄 E40）",
    FR_SRC)
add("J19", "5.10 結論", "FULL_REANALYSIS status wording",
    "，完整重分析尚待執行。",
    "；完整重分析列為開放的驗證行動，但以目前的來源集無法執行（附錄 E40）。",
    FR_SRC)
add("J20", "附錄 E E40", "FULL_REANALYSIS status wording (status codes) + input governance",
    "| V9 套件記為須經研究者核准；作者決定在投稿前或投稿後執行；",
    "| 現行狀態：FULL_REANALYSIS_METHOD_STATUS = REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；FULL_REANALYSIS_EXECUTION_STATUS = NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET（套件受保護基準 37 項輸入中 12 項未尋回，E39（b））；FULL_REANALYSIS_PRIORITY_BEFORE_V1 = NOT_RECOMMENDED（V1.8 檔案 07 §8；V1.8.1 檔案 15、17）。V9 套件記為須經研究者核准；日後是否及何時重跑仍由研究者決定；重跑時的標籤輸入只能取自 V1.8 檔案 04 表 T4（V1.8.1 檔案 15）；",
    FR_SRC + "; 15 §1-§2 (T4 only valid propagation source)")
add("J21", "附錄 E E44", "FULL_REANALYSIS status wording",
    "完整重分析待決（E40）",
    "完整重分析為開放驗證行動且以目前來源集無法執行（E40）",
    FR_SRC)

# ---- 1b. segmentation provenance (13 §4) -----------------------------------
add("J22", "4.5.2", "source attribution (re-segmentation figures)",
    "主要零模型的高於／低於期望方向分別有 12 與 11 格改變。",
    "主要零模型的高於／低於期望方向分別有 12 與 11 格改變" + SEG_TAG + "。",
    SEG_SRC)
add("J23", "4.5.3 表 4-8 表註", "source attribution (re-segmentation figures)",
    "三種設定共同保留的穩健配對沒有方向反轉。\n",
    "三種設定共同保留的穩健配對沒有方向反轉。句層級與句與子句層級兩列（含觀察值改變 84/120、85/120 與主測方向改變 12/120、11/120）取自 V9.1 證據單元重切分敏感度側車分析（V9 套件 `V9_1_SEGMENTATION_SENSITIVITY` 之 `S1_120_CELL_RESULTS.csv`、`S2_120_CELL_RESULTS.csv` 與 `SEGMENTATION_CELL_COUNT_DIFF.csv`；2026-10-03），以凍結之主要分析為比較基準；R14 定稿表 7 轉述。\n",
    SEG_SRC)
add("J24", "4.5.3", "source pointer (G07/G15 boundary wording; WORDING_CONFIRMED, not changed)",
    "五個變動位置列於表 4-9。",
    "五個變動位置列於表 4-9（成員判定的來源同表 4-8 表註）。",
    "V1.8.1 14_G07_G15_BOUNDARY_SENSITIVITY_AUDIT.md §0 (WORDING_CONFIRMED), §5 L1605, §6")
add("J25", "5.4.2", "source attribution (re-segmentation figures)",
    "84–85/120 格的觀察值發生變化，",
    "84–85/120 格的觀察值發生變化（V9.1 證據單元重切分敏感度側車分析；見第 4.5.2–4.5.3 節），",
    SEG_SRC)
add("J26", "5.8.3", "source attribution (re-segmentation figures)",
    "12 與 11 格的主要零模型方向改變，",
    "12 與 11 格的主要零模型方向改變（V9.1 側車分析，見第 4.5.2 節），",
    SEG_SRC)
add("J27", "附錄 D R14 列", "source attribution (re-segmentation figures) + stale R14 date provenance",
    "全部文獻層數值的權威來源 |",
    "全部文獻層數值的權威來源；其中第 3.7.3 節與第 4.5 節之證據單元重切分數值，原始分析出處為 V9.1 證據單元重切分敏感度側車分析（2026-10-03），R14 定稿（2026-10-04 起之修訂）其後納入並轉述。R14 docx 中繼資料之 2026-09-20 修改時間為範本沿用值，不代表成稿日期 |",
    SEG_SRC + " §1.4 (inherited docProps timestamp)")
add("J28", "附錄 D V9 列", "source attribution (V9.1 availability)",
    "第 3.7.4、4.5.5、5.4.2、5.8.9 節；已逐列核對（附錄 E39） |",
    "第 3.7.4、4.5.5、5.4.2、5.8.9 節；已逐列核對（附錄 E39）；套件內 `V9_1_SEGMENTATION_SENSITIVITY` 為證據單元重切分敏感度側車分析之機器可讀來源（第 3.7.3、4.5 節） |",
    SEG_SRC)

# ---- 7. Appendix D version rows ---------------------------------------------
add("J29", "附錄 D（版本與 V1.8.1 檔案列）", "version history rows (v1.8, v1.8.1)",
    "| 137 | — | `137_NEXT_ACTIONS.md` | 投稿前的關鍵路徑 | 附錄 E39–E48 |\n",
    "| 137 | — | `137_NEXT_ACTIONS.md` | 投稿前的關鍵路徑 | 附錄 E39–E48 |\n"
    "| v1.8／08 | — | `08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md` | 合併論文 v1.8（V9 來源核對版） | v1.8.1 的修訂底稿（已保存；未覆寫） |\n"
    "| v1.8.1／13 | — | `13_SEGMENTATION_ATTRIBUTION_FORENSIC.md` | 證據單元重切分數值的出處鑑識（由原始列重算） | 第 4.5.2–4.5.3、5.4.2、5.8.3 節的來源標示 |\n"
    "| v1.8.1／16 | — | `16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.md` | 合併論文 v1.8.1（清理版） | 本稿 |\n"
    "| v1.8.1／17 | — | `17_STUDY1_EVIDENCE_FREEZE_v1.md` | 文獻層（Study 1）證據凍結 | 稿件狀態；附錄 E40 |\n"
    "| v1.8.1／19–21 | — | `19_V1_HUMAN_CONSTRUCT_VALIDATION_PROTOCOL.md`、`20_V1_HUMAN_CONSTRUCT_VALIDATION_PACKET.xlsx`、`21_V1_HUMAN_CONSTRUCT_VALIDATION_CODEBOOK.md` | V1 人類構念效度驗證協定、封包與編碼手冊（READY_TO_RUN；尚未執行） | 稿件狀態；第 4.7.3 節 |\n",
    "V1.8.1 OUT file list; 17; 19 L389")

# ---- 6. typo -----------------------------------------------------------------
add("J30", "3.10.5 表（D07 列）", "typo (missing closing parenthesis)",
    "**決定工程資源的結構**（與 D06 合併判定 |",
    "**決定工程資源的結構**（與 D06 合併判定） |",
    "incidental typo scan (tools/J/typo_scan.py): unbalanced （ on v1.8 L869")

orig = raw.decode('utf-8')
assert '\r' not in orig
text = orig
for p in P:
    pos = orig.find(p['old'])
    p['count_in_v18'] = orig.count(p['old'])
    assert p['count_in_v18'] == 1, f"{p['id']}: old matched {p['count_in_v18']} times in v1.8"
    p['v18_line'] = orig[:pos].count('\n') + 1
    c = text.count(p['old'])
    assert c == 1, f"{p['id']}: old matched {c} times at apply time"
    text = text.replace(p['old'], p['new'], 1)
assert '\r' not in text
out = text.encode('utf-8')
open(DST, 'wb').write(out)
json.dump(P, open(JOUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('patches', len(P))
print('src sha', hashlib.sha256(raw).hexdigest())
print('dst sha', hashlib.sha256(out).hexdigest())
for p in P:
    print(p['id'], 'v1.8 line', p['v18_line'])
