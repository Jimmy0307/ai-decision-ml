"""Build v1.8.3 V5 PROVENANCE CANDIDATE from v1.8.2 by exact old->new replacements.
Each `old` must occur exactly once in v1.8.2 and exactly once at apply time.
Scope: provenance / status wording only (no math, no result numbers, no G rows, no headings,
no Table 3-4/3-4A, no V1 design text, no Enterprise model).
Usage: python -I patch_v183.py <v1.8.2 md> <v1.8.3 md out> <patches json out>"""
import sys, json, hashlib

SRC, DST, JOUT = sys.argv[1], sys.argv[2], sys.argv[3]
EXPECTED_SRC_SHA = "2d493edc2e1884f05e5b0617bc56f1f85cdab0fa33531ac566b61d343dd8f159"

raw = open(SRC, 'rb').read()
if hashlib.sha256(raw).hexdigest() != EXPECTED_SRC_SHA:
    sys.exit("STOP: v1.8.2 manuscript hash unexpectedly changed")

P = []


def add(pid, sec, cat, old, new, src):
    P.append(dict(id=pid, section=sec, category=cat, old=old, new=new, source=src))


EXEC_LONG = "其執行條件尚待滿足（須先事先登記標籤傳播規則並重現正式基準）"
EXEC_SHORT = "執行條件待滿足（須先登記傳播規則並重現基準）"
S35 = "OUT 35 §1–§2, §6"
S36 = "OUT 36 §A–§D"
S37 = "OUT 37 §1, §3, §6–§7"
S38 = "OUT 38 §1, §2e–g, §3–§4"
TRIP = "orchestrator triplet v1.8.3 (OUT 39 §3)"

# ---- 1. status line (L5) ---------------------------------------------------
add("R01", "稿件狀態", "version label",
    "合併碩士論文 v1.8.2 V1 PREFREEZE CANDIDATE（由 v1.8.1 修訂；v1.0–v1.8.1 保留、未覆寫；",
    "合併碩士論文 v1.8.3 V5 PROVENANCE CANDIDATE（由 v1.8.2 修訂；v1.0–v1.8.2 保留、未覆寫；",
    "this round (output 41); Appendix D row R24")
add("R02", "稿件狀態", "v1.8.3 provenance summary",
    "V1.8.1 的 19–21 封包顯示 G 編號，已被取代、不得發送。(1)",
    "V1.8.1 的 19–21 封包顯示 G 編號，已被取代、不得發送。"
    "v1.8.3 只更新來源與狀態描述，不改變任何數值、G 清單、V1 設計或企業模型："
    "V5 正式生產資料夾已尋回，並以完整 SHA-256 與各階段清單鏈核對（V1.8.3 檔案 35–38）；"
    "正式凍結核心檔（FINAL_ROBUST_CORE_32.csv）的來源由「只以重現檔佐證」改為已確認（CONFIRMED）；"
    "V5 Manuscript Data Pack 已尋回；V9 受保護基準的 37 項輸入全數以完整 SHA-256 確認；"
    "文獻層證據凍結的數值不變，只強化其來源（V1.8.3 檔案 39–40）。(1)",
    S35 + "; " + S36 + "; " + S37 + "; OUT 39 §1")
add("R03", "稿件狀態", "full-reanalysis execution status",
    "但以目前的來源集無法執行（37 項受保護輸入中 12 項未尋回；NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET）",
    "其執行條件尚待滿足（EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION："
    "37 項受保護輸入已全數以完整 SHA-256 確認，但須先由研究者事先登記並以雜湊承諾標籤傳播規則、"
    "在新的日期目錄中以僅修改路徑的程式複本重現 13 個雜湊釘定的正式輸出，並依 V9 經研究者核准）",
    TRIP + "; " + S38)

# ---- 2. abstract / Abstract ------------------------------------------------------
add("R04", "摘要", "full-reanalysis execution status",
    "完整重分析列為開放的驗證行動，但以目前的來源集無法執行，在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定。",
    "完整重分析列為開放的驗證行動，" + EXEC_LONG + "，在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定。",
    TRIP)
add("R05", "Abstract", "full-reanalysis execution status (English)",
    "it cannot be executed with the currently recovered source set (12 of 37 protected inputs are missing),",
    "its execution is pending researcher predeclaration and hash commitment of the label-propagation rule, "
    "byte-for-byte reproduction of the pinned official baseline in the current workspace, and researcher approval "
    "(all 37 protected inputs are now hash-confirmed),",
    TRIP + "; " + S37)

# ---- 3. chapter 1 ----------------------------------------------------------------
add("R06", "1.4", "full-reanalysis execution status",
    "但以目前的來源集無法執行，在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（第 4.5.5 節；附錄 E40）。研究問題三",
    EXEC_LONG + "，在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（第 4.5.5 節；附錄 E40）。研究問題三",
    TRIP)
add("R07", "1.4 表", "full-reanalysis execution status",
    "以目前來源集無法執行，V1 前不建議優先執行（附錄 E40） |",
    EXEC_SHORT + "，V1 前不建議優先執行（附錄 E40） |",
    TRIP)
add("R08", "1.5", "full-reanalysis execution status",
    "（開放驗證行動、以目前來源集無法執行、V1 前不建議優先執行）",
    "（開放驗證行動、執行條件待滿足、V1 前不建議優先執行）",
    TRIP)
add("R09", "1.6", "full-reanalysis execution status",
    "但以目前的來源集無法執行，在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（第 4.5.5 節；附錄 E40）；逐格解讀",
    EXEC_LONG + "，在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（第 4.5.5 節；附錄 E40）；逐格解讀",
    TRIP)

# ---- 4. chapter 3 ----------------------------------------------------------------
add("R10", "3.1.1", "full-reanalysis execution status",
    "但以目前的來源集無法執行，在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（第 3.7.4、4.5.5 節；附錄 E40）。第二層",
    EXEC_LONG + "，在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（第 3.7.4、4.5.5 節；附錄 E40）。第二層",
    TRIP)
add("R11", "3.1.1 流程", "full-reanalysis execution status",
    "完整重分析為開放驗證行動，目前無法執行）",
    "完整重分析為開放驗證行動，執行條件待滿足）",
    TRIP)
add("R12", "3.7.1", "HUMAN_AUDIT log hash wording",
    "V9 套件的完整性紀錄另顯示，早期稽核日誌 HUMAN_AUDIT_APPEND_ONLY_LOG.csv 的現行雜湊與受保護基準不符"
    "（套件記為 LEGACY_AUDIT_LOG_INTEGRITY = UNVERIFIED，未發現竄改證據）；"
    "凍結的第一位編碼者檔、盲式第二編碼檔與調和檔的雜湊均與套件雜湊清單相符。此為來源完整性的限制（附錄 E39）。",
    "V9 套件的完整性紀錄另顯示，早期稽核日誌 HUMAN_AUDIT_APPEND_ONLY_LOG.csv 的現行雜湊與受保護基準不符"
    "（套件當時記為 LEGACY_AUDIT_LOG_INTEGRITY = UNVERIFIED；此標記屬歷史紀錄，未發現竄改證據）；"
    "v1.8.3 的核對顯示，受保護狀態與現行附加式日誌的前 355 位元組逐位元組相同（完整 SHA-256 相符），"
    "其後的位元組皆為附加的事件，符合附加式日誌的預期，即受保護狀態已確認為附加式日誌的前綴（V1.8.3 檔案 37）；"
    "凍結的第一位編碼者檔、盲式第二編碼檔與調和檔的雜湊均與套件雜湊清單相符（附錄 E39）。",
    S37 + " (row 26, prefix match); orchestrator wording rule")
add("R13", "3.7.4", "sidecar generator / propagation rule provenance",
    "但產生敏感度表的程式未隨套件保存，人工標籤中的「不確定」「模糊」「無法對應」如何轉為配對資格，無法由套件重現 "
    "`[AUTHOR TO CONFIRM：標籤至配對資格的傳播規則與重算程式；附錄 E48]`。",
    "替換後的核心檔、側車產生程式與其標籤處理政策不在 V9 套件內，但已於 V9 側車資料夾尋回（V1.8.3 檔案 37–38）："
    "替換後的核心檔以完整 SHA-256 確認；側車產生程式的位置與其輸出一致，但其本身的雜湊未由 V9 釘定（PROBABLE）；"
    "產生敏感度表本身的程式仍未尋回。人工標籤中的「不確定」「模糊」「無法對應」如何轉為配對資格，"
    "已由側車政策尋回（RECOVERED_FROM_SIDECAR_POLICY），以獨立程式重算可重現側車的逐筆處理與配對資格變動；"
    "此規則屬事後尋回，不是事前登記，若執行完整重分析，仍須由研究者事先登記並以雜湊承諾 "
    "`[AUTHOR TO CONFIRM：是否採用尋回的傳播規則並事先登記；附錄 E48]`。",
    S37 + " §6; " + S38 + " §2e–f")
add("R14", "3.7.4", "full-reanalysis execution status",
    "以目前的來源集無法執行（37 項受保護輸入中 12 項未尋回）",
    "其執行條件尚待滿足（37 項受保護輸入已全數以完整 SHA-256 確認；須先事先登記標籤傳播規則並重現正式基準）",
    TRIP + "; " + S37)
add("R15", "3.8.3", "V5 Data Pack provenance",
    "（依專案紀錄的 V5 Manuscript Data Pack 模型資訊；Data Pack 原檔不在本稿工作環境中，投稿前須以原檔核對）",
    "（取自 V5 Manuscript Data Pack 的模型紀錄；v1.8.3 已尋回 Data Pack 原檔 data_pack_v1_20260922T010012Z，"
    "其清單所列 74 個檔案雜湊全數相符，模型摘要值與其中的 STAGE2_RUNTIME_SUMMARY 模型紀錄逐字相符；V1.8.3 檔案 35）",
    S35 + " §1 (stage 14, 74/74); data pack 04_STAGE2_RUNTIME_SUMMARY.json a4111914… (manifest-listed) unique_model_digests")

# ---- 5. chapter 4 / 5 ----------------------------------------------------------------
add("R16", "4.5.5", "full-reanalysis execution status",
    "以目前的來源集無法執行（37 項受保護輸入中 12 項未尋回；FULL_REANALYSIS_EXECUTION_STATUS = NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET）",
    "其執行條件尚待滿足（37 項受保護輸入已全數以完整 SHA-256 確認，但須先事先登記標籤傳播規則並重現正式基準，且經研究者核准；"
    "FULL_REANALYSIS_EXECUTION_STATUS = EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION）",
    TRIP)
add("R17", "4.11 表", "full-reanalysis execution status",
    "凍結的 32 組仍為推論基準；完整重分析為開放驗證行動，以目前來源集無法執行",
    "凍結的 32 組仍為推論基準；完整重分析為開放驗證行動，" + EXEC_SHORT,
    TRIP)
add("R18", "4.11", "full-reanalysis execution status",
    "完整重分析為開放驗證行動，以目前來源集無法執行，見附錄 E40）",
    "完整重分析為開放驗證行動，" + EXEC_SHORT + "，見附錄 E40）",
    TRIP)
add("R19", "5.3.2 表", "full-reanalysis execution status",
    "完整重分析為開放驗證行動，以目前來源集無法執行（附錄 E40） |",
    "完整重分析為開放驗證行動，" + EXEC_SHORT + "（附錄 E40） |",
    TRIP)
add("R20", "5.8.9", "full-reanalysis execution status",
    "FULL_REANALYSIS_EXECUTION_STATUS = NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET，FULL_REANALYSIS_PRIORITY_BEFORE_V1",
    "FULL_REANALYSIS_EXECUTION_STATUS = EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION，FULL_REANALYSIS_PRIORITY_BEFORE_V1",
    TRIP)
add("R21", "5.9", "full-reanalysis execution precondition",
    "執行前須先尋回缺件的受保護輸入，時程排在",
    "受保護輸入已全數尋回，執行前須先事先登記標籤傳播規則並在現行工作環境重現正式基準，時程排在",
    TRIP + "; " + S38 + " §3")
add("R22", "5.10", "full-reanalysis execution status",
    "但以目前的來源集無法執行（附錄 E40）。",
    EXEC_LONG + "（附錄 E40）。",
    TRIP)
add("R23", "3.8.1 表", "full-reanalysis execution status",
    "局部成員敏感度；不取代 L2；完整重分析為開放驗證行動，以目前來源集無法執行",
    "局部成員敏感度；不取代 L2；完整重分析為開放驗證行動，" + EXEC_SHORT,
    TRIP)

# ---- 6. Appendix D -----------------------------------------------------------------
add("R24", "附錄 D", "Appendix D rows 35–41",
    "| v1.8.2／32 | — | `32_MERGED_MASTER_THESIS_v1_8_2_V1_PREFREEZE_CANDIDATE.md` | 合併論文 v1.8.2（V1 凍結前版；只更新 V1 設計與狀態描述） | 本稿 |",
    "| v1.8.2／32 | — | `32_MERGED_MASTER_THESIS_v1_8_2_V1_PREFREEZE_CANDIDATE.md` | 合併論文 v1.8.2（V1 凍結前版；只更新 V1 設計與狀態描述） | v1.8.3 的修訂底稿（已保存；未覆寫） |\n"
    "| v1.8.3／35–36 | — | `35_V5_MANIFEST_CHAIN_VERIFICATION.md`、`36_V5_BASELINE_RECOMPUTATION.md`（另有 .csv／.json） | V5 正式生產資料夾的各階段清單鏈核對，以及由凍結原始列重算的文獻層基準（數值不變） | 稿件狀態；第 3.8.3 節；附錄 E12、E39 |\n"
    "| v1.8.3／37 | — | `37_PROTECTED_INPUT_RECOVERY.md`（另有 .csv） | V9 受保護基準 37 項輸入的尋回與完整雜湊確認；附加式日誌前綴核對；替換後核心檔的位置 | 第 3.7.1、3.7.4 節；附錄 E39 |\n"
    "| v1.8.3／38 | — | `38_FULL_REANALYSIS_FEASIBILITY.md` | 完整重分析的執行可行性；尋回的標籤傳播規則與側車產生程式 | 第 3.7.4、4.5.5、5.8.9 節；附錄 E40、E48 |\n"
    "| v1.8.3／39–40 | — | `39_STUDY1_FREEZE_PROVENANCE_ADDENDUM_v1_8_3.md`、`40_STUDY1_FREEZE_HASHES_v1_8_3.csv` | 文獻層（Study 1）證據凍結的來源補充與雜湊帳（凍結數值不變） | 稿件狀態；附錄 E39、E40 |\n"
    "| v1.8.3／41 | — | `41_MERGED_MASTER_THESIS_v1_8_3_V5_PROVENANCE_CANDIDATE.md` | 合併論文 v1.8.3（V5 來源版；只更新來源與狀態描述） | 本稿 |",
    "OUT file list 35–41; this round")

# ---- 7. Appendix E -----------------------------------------------------------------
add("R25", "附錄 E12", "V5 Data Pack provenance",
    "模型摘要值取自 V5 Data Pack 的模型紀錄；Ollama 版本未保存，維持為再現性限制",
    "模型摘要值取自 V5 Data Pack 的模型紀錄（v1.8.3 已尋回 Data Pack 原檔並核對一致，V1.8.3 檔案 35）；Ollama 版本未保存，維持為再現性限制",
    S35)
add("R26", "附錄 E39", "residual limit (a)",
    "（a）FINAL_STATUS.json 記錄一項受保護雜湊不符（HUMAN_AUDIT_APPEND_ONLY_LOG.csv；LEGACY_AUDIT_LOG_INTEGRITY = UNVERIFIED，未發現竄改證據），凍結的編碼檔與調和檔雜湊完好；",
    "（a）FINAL_STATUS.json 記錄一項受保護雜湊不符（HUMAN_AUDIT_APPEND_ONLY_LOG.csv；LEGACY_AUDIT_LOG_INTEGRITY = UNVERIFIED，屬歷史標記，未發現竄改證據）；"
    "v1.8.3 已確認受保護狀態為現行附加式日誌的前 355 位元組（完整 SHA-256 相符；V1.8.3 檔案 37），凍結的編碼檔與調和檔雜湊完好；",
    S37 + " row 26")
add("R27", "附錄 E39", "residual limit (b)",
    "（b）套件受保護基準所列 37 項輸入中有 12 項（含原始 400／120 抽樣檔、V9 原稿、凍結資料庫與凍結清單）不在套件中，正式凍結核心檔只以套件內位元組相同的重現檔佐證；",
    "（b）套件受保護基準所列 37 項輸入中有 12 項（含原始 400／120 抽樣檔、V9 原稿、凍結資料庫與凍結清單）不在套件中；"
    "v1.8.3 已在工作環境的其他位置尋回全部 37 項並以完整 SHA-256 確認（V1.8.3 檔案 37），"
    "正式凍結核心檔亦於 V5 正式生產資料夾尋回，並經 V5 各階段清單鏈核對確認（V1.8.3 檔案 35–36），不再只以重現檔佐證；",
    S35 + "; " + S36 + "; " + S37)
add("R28", "附錄 E39", "residual limit (c)",
    "（c）替換後的核心檔與產生敏感度表的程式未隨套件保存，替換後成員係由敏感度表逐列重現；",
    "（c）替換後的核心檔與側車產生程式不在套件中，已於 V9 側車資料夾尋回：替換後的核心檔以完整 SHA-256 確認，"
    "側車產生程式為 PROBABLE（其雜湊未由 V9 釘定）；產生敏感度表本身的程式仍未尋回，替換後成員係由敏感度表逐列重現，並與尋回的替換後核心檔一致；",
    S37 + " §6; " + S38 + " §2e")
add("R29", "附錄 E39", "residual-limit summary",
    "殘餘限制（a）–（d）保留，傳播規則見 E48，完整重分析見 E40 |",
    "殘餘限制（a）–（c）已依 v1.8.3 的來源核對更新（V1.8.3 檔案 35–39），（d）保留；傳播規則見 E48，完整重分析見 E40 |",
    "OUT 39")
add("R30", "附錄 E40", "full-reanalysis triplet",
    "FULL_REANALYSIS_EXECUTION_STATUS = NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET（套件受保護基準 37 項輸入中 12 項未尋回，E39（b））；"
    "FULL_REANALYSIS_PRIORITY_BEFORE_V1 = NOT_RECOMMENDED（V1.8 檔案 07 §8；V1.8.1 檔案 15、17）。",
    "FULL_REANALYSIS_EXECUTION_STATUS = EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION"
    "（v1.8.3：37 項受保護輸入已全數以完整 SHA-256 確認，E39（b）；尚待三項前置條件：研究者事先登記並以雜湊承諾標籤傳播規則、"
    "在新的日期目錄中以僅修改路徑的程式複本逐位元組重現 13 個雜湊釘定的正式輸出、依 V9 經研究者核准；V1.8.3 檔案 38）；"
    "FULL_REANALYSIS_PRIORITY_BEFORE_V1 = NOT_RECOMMENDED（V1.8 檔案 07 §8；V1.8.1 檔案 15、17；屬研究者決定。"
    "原理由 1「受保護輸入缺件」已不成立，理由 2–5 仍成立；已請研究者重新檢視此優先順序的理由：PRIORITY_RATIONALE_REVIEW_REQUESTED）。",
    TRIP + "; " + S38 + " §4")
add("R31", "附錄 E40", "full-reanalysis precondition",
    "重跑前須先補回缺件的受保護輸入（E39（b））並事先登記標籤傳播規則（E48）；",
    "重跑前須先事先登記並以雜湊承諾標籤傳播規則（E48），並在現行工作環境重現正式基準；",
    TRIP + "; " + S38 + " §3")
add("R32", "附錄 E44", "full-reanalysis execution status",
    "完整重分析為開放驗證行動且以目前來源集無法執行（E40）",
    "完整重分析為開放驗證行動且執行條件待滿足（E40）",
    TRIP)
add("R33", "附錄 E48", "propagation rule status",
    "人工標籤中「不確定」「模糊」「無法對應」轉為配對資格的規則，以及產生敏感度表的程式，未隨套件保存而無法重現；",
    "人工標籤中「不確定」「模糊」「無法對應」轉為配對資格的規則不在套件中，已由 V9 側車政策尋回（RECOVERED_FROM_SIDECAR_POLICY；V1.8.3 檔案 38），"
    "以獨立程式重算可重現側車的逐筆處理與配對資格變動，但屬事後尋回、非事前登記；側車產生程式已尋回（PROBABLE），產生敏感度表本身的程式仍未尋回；",
    S38 + " §2e–f")
add("R34", "附錄 E48", "propagation rule action",
    "由作者補述傳播規則並提供重算程式後，移除第 3.7.4 節的 `[AUTHOR TO CONFIRM]`；若執行完整重分析（E40），須事先登記此規則 |",
    "由研究者決定是否採用尋回的傳播規則（或另訂規則），事先登記並以雜湊承諾後，移除第 3.7.4 節的 `[AUTHOR TO CONFIRM]`；若執行完整重分析（E40），須以此登記的規則執行 |",
    TRIP + "; " + S38 + " §2f")

orig = raw.decode('utf-8')
assert '\r' not in orig
text = orig
for p in P:
    p['count_in_v182'] = orig.count(p['old'])
    assert p['count_in_v182'] == 1, f"{p['id']}: old matched {p['count_in_v182']} times in v1.8.2"
    p['v182_line'] = orig[:orig.find(p['old'])].count('\n') + 1
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
    print(p['id'], 'v1.8.2 line', p['v182_line'])
