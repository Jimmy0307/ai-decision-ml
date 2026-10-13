"""Assign closure status to every extracted flag row and write W/06_SOURCE_FLAG_CLOSURE.csv.
Usage: python -I build.py <flags.csv> <out_csv>
Rules are explicit (per file/line/type) and documented in 06_SOURCE_FLAG_CLOSURE_NOTES.md.
Evidence values come from verify_out.json (verify.py) - see notes."""
import sys, csv

FLAGS, OUT = sys.argv[1], sys.argv[2]
V = "V9=W/02_V9_HUMAN_VALIDATION/20260929_V9_HUMAN_VALIDATION/"
S_CNT = (V + "FIRST_CODER_50_FINAL_FROZEN.csv(sha dd332dd8..);BLIND_REPEAT_20_FINAL_FROZEN.csv(6afc8d7a..);"
         "HUMAN_RECONCILED_20.csv(4b7ceac2..) [sha = 01_FILE_INVENTORY = FINAL_ARTIFACT_HASH_MANIFEST = *.sha256 = FINAL_STATUS.json]")
S_KAP = S_CNT + ";HUMAN_RELIABILITY_FINAL.csv(ef7e5544..)"
S_SEN = (V + "ROBUST_CORE_LOCAL_SENSITIVITY.csv(e3166ee1..);ROBUST_CORE_LOCAL_SENSITIVITY_DIFF.csv(f6607aae..);"
         "FINAL_STATUS.json(d9226d31..) [sha = inventory = FINAL_ARTIFACT_HASH_MANIFEST]")
S_G = S_SEN + ";r14_merge_v1_7/132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX.csv (16 G rows)"
S_ST = V + "FINAL_STATUS.json(d9226d31..; decision_text=HUMAN_AUDIT_CONVERGED/LOCAL_SENSITIVITY_CHANGED/FULL_REANALYSIS_REQUIRED; submission_ready=false)"
S_TAX = V + "FINAL_ERROR_TAXONOMY.csv(68e97c01..);FINAL_ERROR_TAXONOMY_CASES.csv(8949b671..);HUMAN_RECONCILED_20.csv"
S_SEG = (V + "V9_1_SEGMENTATION_SENSITIVITY/S1_ANALYTICAL_FREEZE_RECORD_LEVEL.csv(ad5e8958..);S2_..(b42e3086..);"
         "SEGMENTATION_SENSITIVITY_FINAL_REPORT.md(15d48ecb..) line 7")
S_E48 = V + "ROBUST_CORE_LOCAL_SENSITIVITY.md(b25b9a84..);FINAL_STATUS.json sensitivity.audited_record_scope;ROBUST_CORE_LOCAL_SENSITIVITY.csv"
S_ZIP = "W/00_INPUT_MANIFEST.csv: 20260929_V9_HUMAN_VALIDATION.zip sha 8f63e88e..; extracted under W/02_V9_HUMAN_VALIDATION"

CL, MM, NF, P4, KL, NA = ("CLOSED_SOURCE_VERIFIED", "OPEN_VALUE_MISMATCH", "OPEN_SOURCE_NOT_FOUND",
                          "OPEN_NEEDS_PHASE4", "KEEP_AS_LIMITATION", "NOT_A_FLAG")

# reusable verdicts: (status, source_found, verified, source_artifact, needed_evidence, notes)
MEMB = (CL, "YES", "YES", S_SEN, "V9 sensitivity rows for the 2 changed pairs and core size",
        "Row-level: official core 32 (16E/16D) -> sidecar core 32 (15E/17D); gained HUMAN_AUGMENTATION x RISK_ASSESSMENT (DEPLETED); lost COORDINATION_EXECUTION x GENERAL_DECISION_PROCESS (ENRICHED); 31 common, 0 direction changes; core_membership_changed=YES in exactly 2/120 rows. Flag wording must cite V9 files, not 'artifact not in workspace'.")
GKEEP = (CL, "YES", "YES", S_G, "sidecar core membership of the 16 G cells",
         "Row-level: all 16 G01-G16 cells (= official DEPLETED core, exact set match) are sidecar core members, all DEPLETED; 132 O values = V9 official_observed for all 16.")
COUNT = (CL, "YES", "YES", S_KAP, "row counts 50/20/19 and pre-adjudication kappas",
         "Row-level: first coder 50 rows/50 unique/50 complete; blind 20/20 complete, subset of the 50; reconciled file 20 rows, 19 with >=1 field disagreement (1 full agreement), 19 event IDs, FINAL complete 20/20. Kappa recomputed by E from raw FIRST_C*/BLIND_C* columns = .5614/.1798/.0476/.1398/.3162 (= HUMAN_RELIABILITY_FINAL.csv); independent Phase-4 recomputation still pending (verified_kappa=YES_BY_E;PHASE4_CROSSCHECK_PENDING).")
STAT = (CL, "YES", "YES", S_ST + ";" + S_SEN, "machine-readable status flags + sensitivity rows",
        "FINAL_STATUS.json decision_text = HUMAN_AUDIT_CONVERGED, LOCAL_SENSITIVITY_CHANGED, FULL_REANALYSIS_REQUIRED; counts in it match raw rows; sensitivity values match ROBUST_CORE_LOCAL_SENSITIVITY.csv. Status date: FINAL_STATUS verified_at 2026-10-03T12:23:44Z (folder name says 20260929).")
D1517 = (CL, "YES", "YES", S_SEN, "sidecar core direction counts and unchanged 31",
         "Row-level: sidecar core ENRICHED 15 / DEPLETED 17; 31 official core pairs retained with identical direction; no other membership or direction change in any of 120 rows (the 'if no other unreported change' condition is satisfied). 'Inferred' wording can become 'observed'.")
CRIT = (CL, "YES", "YES", S_SEN + ";" + S_E48, "core-promotion rule",
        "Row-level: recomputing core = q<=.05 & same direction in main+exact+document-preserving (+raw) from the 120-row q-values reproduces both official_core_member (32) and sidecar_core_member (32) exactly; matches L2 criterion of Table 3-3.")
E49 = (CL, "YES", "YES", S_SEG, "whether segmentation sidecar used human labels for audited records",
       "Row-level: in S1 and S2 record-level freezes, all 22 UNCHANGED_FROZEN rows of the 50 audited records keep model families (22/22 = current model family, 0/22 = first-coder human family although human differs from model on all 22); FINAL_REPORT line 7: 'no final/reconciled human label was propagated'. Human audit error tags were used only to force candidate selection. Label scopes therefore do NOT overlap; only candidate selection depended on audit tags.")
E48 = (P4, "YES", "PARTIAL", S_E48, "replacement scope, matrix rebuild, untouched records, test set, seeds",
       "Found (summary md/json, not row-reproduced): labels = 20 reconciled FINAL labels + first-coder labels for the other 30 audited records; unaudited records unchanged; main fixed-degree null 10,000 reps seed 20260918; document-preserving null 5,000 reps seed 20260919; exact + raw with accepted scripts; BH within each 120-cell method; 13 official outputs reproduced byte-for-byte. Promotion rule verified row-level (see CRIT). Scope/seeds need sidecar rerun (Phase 4) to be row-verified.")
FOUR = (MM, "YES", "PARTIAL", S_TAX, "classification of disagreements into 4 sources",
        "V9 has the four sources (MODEL_MAPPING / TAXONOMY_BOUNDARY / EVIDENCE_SEGMENTATION / PDF_EXTRACTION) plus TRUE_CONCEPTUAL_AMBIGUITY (MULTI_STAGE_DECISION_CHAIN, 2 records) as likely_source of a 14-type error taxonomy; status INTERPRETIVE_HYPOTHESIS_FROM_ACTUAL_EVIDENCE; NOT_ADJUDICATION. It classifies MODEL-vs-HUMAN label differences over the 50 audited records (77 tags on 33 records; 17 of the 19 coder-disagreement records carry >=1 tag), not the 19 coder-vs-coder disagreements. Manuscript attributes the 4-way grouping to the human disagreements and omits the 5th class: provenance/scope wording mismatch (no number change).")
DATE = (MM, "YES", "YES", S_CNT + ";" + S_ST, "date of the status record",
        "Manuscript: 2026-09-29. Raw: first-coder freeze 2026-10-02T19:49:38Z; reconciliation events 2026-10-03T07:45-11:09Z; FINAL_STATUS verified_at 2026-10-03T12:23:44Z. 20260929 is only the package/folder name.")
LABSCOPE = (MM, "YES", "PARTIAL", S_E48, "which human labels replaced model labels",
            "Manuscript says reconciled (人工調和後) labels replaced audited-record labels; V9 FINAL_STATUS/ROBUST_CORE_LOCAL_SENSITIVITY.md: 20 reconciled labels + first-coder (researcher-reviewed) labels for the other 30. Wording should say 'researcher-reviewed or reconciled' (as L605 already does).")
ZIP = (CL, "YES", "YES", S_ZIP + ";" + S_SEN, "V9 package presence",
       "V9 package is now in the workspace (zip hash recorded); all V9 values cited by v1.7 were re-checked row-level (see other rows). 'Not in workspace' wording is obsolete.")
EMP = (KL, "NO", "N/A", "", "enterprise data (V0/V2/V7) not collected",
       "Genuinely unavailable enterprise empirical data; outside V9 scope; keep marker.")
HUM = (KL, "NO", "N/A", "", "human V1 / EA-X / ORG-V coding not yet run",
       "V9 covers only the literature-layer audit; enterprise construct-validity human coding has not been conducted; keep marker.")
HIST = (NA, "N/A", "N/A", "", "", "Historical change-log / rule text describing a flag that lives in 130; no claim to close here (live flag tracked on its 130 line).")
LEG = (NA, "N/A", "N/A", "", "", "Legend / definition of a status marker, not an open claim.")
REFS = (NF, "NO", "NO", "", "reference full text / official publication record",
        "Reference-verification flag outside V9 scope; V9 package contains no bibliographic sources.")

R = {}
def put(f, ln, t, v, flag=None):
    R[(f, ln, t)] = v

# ---- 128
put("128", 14, "V9_DATE", ZIP); put("128", 14, "SRC_MISSING", ZIP)
put("128", 15, "SRC_MISSING", (NF, "PARTIAL", "NO", "W/03_LEGACY_FULL_SOURCE/完整資料來源 (zip sha 138dbeac..)", "V5 Manuscript Data Pack",
                               "Legacy package is now extracted in W/03 but its content is outside Phase 7 (V9) scope; not checked by E."))
put("128", 16, "SRC_MISSING", (NF, "NO", "NO", "", "投稿格式.pdf / 投稿範例.pdf / 全文投稿樣板 docx", "Submission-format templates not in V9 or W/03 filename search."))
put("128", 29, "V9_DATE", STAT); put("128", 29, "SRC_MISSING", STAT); put("128", 29, "PENDING", STAT); put("128", 29, "HUM_PENDING", HUM)
put("128", 34, "PENDING", EMP)
put("128", 44, "V9_DATE", MEMB); put("128", 44, "SRC_MISSING", MEMB)
put("128", 46, "ZH_PENDING", (NF, "PARTIAL", "PARTIAL", V + "V9_1_SEGMENTATION_SENSITIVITY/SEGMENT_STAGE2_MODEL_VERIFICATION.json(feb1ae6a..)", "V5 Data Pack model record",
                              "Same digest 7cdf5a01.., Q4_K_M, temperature 0, seed 20260909, num_ctx 8192 found in the V9.1 frozen Stage-2 contract verification (2026-10-03), which corroborates but is not the original main-run Data Pack."))
put("128", 53, "V9_DATE", E49); put("128", 53, "ZH_PENDING", E49)
put("128", 64, "SRC_MISSING", ZIP); put("128", 73, "SRC_MISSING", ZIP)
# ---- 130
put("130", 5, "V9_SRC_LONG", STAT)
put("130", 13, "V9_SHORT", MEMB); put("130", 15, "V9_SHORT", GKEEP)
put("130", 29, "V9_EN", MEMB)
put("130", 29, "PENDING", (KL, "YES", "YES", S_ST, "full reanalysis not run", "FINAL_STATUS: FULL_REANALYSIS_REQUIRED; full_reanalysis_requires_researcher_approval=true. Genuine open step, keep."))
put("130", 31, "PENDING", HUM)
put("130", 158, "V9_SRC_LONG", MEMB)
put("130", 168, "HUM_PENDING", LEG)
put("130", 591, "V9_SHORT", FOUR); put("130", 591, "V9_DATE", DATE)
put("130", 605, "AUTHOR_CONFIRM", E48)
put("130", 605, "SRC_MISSING", (P4, "YES", "PARTIAL", S_E48, "replacement label source",
                                "'研究者審閱或調和後的標籤' is consistent with V9 scope (20 reconciled + 30 first-coder labels) per FINAL_STATUS/md; row-level reproduction needs sidecar rerun."))
put("130", 607, "V9_DATE", E49)
put("130", 609, "V9_SRC_LONG", STAT); put("130", 609, "V9_DATE", STAT)
put("130", 619, "ZH_PENDING", D1517); put("130", 619, "SRC_MISSING", D1517)
put("130", 630, "V9_SHORT", D1517); put("130", 630, "ZH_PENDING", CRIT); put("130", 630, "SRC_MISSING", D1517)
put("130", 645, "V9_SHORT", GKEEP)
put("130", 651, "SRC_MISSING", R[("128", 46, "ZH_PENDING")])
put("130", 716, "V9_SHORT", GKEEP)
put("130", 1372, "HUM_PENDING", LEG)
put("130", 1559, "V9_SHORT", FOUR); put("130", 1559, "V9_DATE", FOUR)
put("130", 1629, "V9_SRC_LONG", STAT)
put("130", 1638, "V9_SHORT", D1517)
put("130", 1640, "SRC_MISSING", D1517)
put("130", 2183, "V9_SHORT", MEMB); put("130", 2206, "V9_SHORT", MEMB)
put("130", 2262, "V9_SHORT", FOUR); put("130", 2262, "V9_DATE", FOUR)
put("130", 2268, "V9_SHORT", (CL, "YES", "YES", S_SEN, "membership change + 19 document-level edges + position in main analysis",
                              "Row-level: gained HUMAN_AUGMENTATION x RISK_ASSESSMENT official main q=.00092 (<.001), official document-preserving q=.0567 (>.05, so not in official core); lost COORDINATION_EXECUTION x GENERAL_DECISION_PROCESS official_observed=19, official_document_observed=19, official main q=.0167 (* tier). All match."))
put("130", 2308, "ZH_PENDING", (NA, "N/A", "N/A", "", "", "'待驗證的中介機制' describes testable propositions, not a source flag."))
put("130", 2362, "V9_SHORT", MEMB); put("130", 2362, "ZH_PENDING", E49)
put("130", 2378, "V9_SHORT", MEMB)
put("130", 2594, "VERIFY", (NF, "NO", "NO", "", "EUR-Lex Official Journal record (full title + OJ publication date) of Regulation (EU) 2026/1744", "Reference flag outside V9 scope."))
put("130", 2664, "V9_DATE", (CL, "YES", "YES", S_SEN + ";" + S_E48, "replacement list, post-replacement matrix, core comparison for S8",
                             "Sources located and hash-verified; S8 must now actually ship ROBUST_CORE_LOCAL_SENSITIVITY.csv/_DIFF.csv/.md (and the 50/20/19 files) - packaging action, not a provenance gap."))
put("130", 2668, "UNVERIFIED", LEG)
for ln in (2683, 2712, 2743, 3060):
    put("130", ln, "UNVERIFIED", REFS)
put("130", 3008, "V9_DATE", ZIP); put("130", 3008, "ZH_PENDING", ZIP); put("130", 3008, "SRC_MISSING", ZIP)
put("130", 3045, "ZH_PENDING", REFS)
put("130", 3062, "PENDING", EMP)
put("130", 3063, "V9_DATE", ZIP)
put("130", 3063, "SRC_MISSING", (CL, "YES", "YES", S_KAP + ";" + S_SEN + ";" + S_ST, "all E39 check items",
                                 "Every E39 check item verified row-level: replacement result (2 changed pairs), post-replacement core 32 (15/17), 31 unchanged, no other unreported change, status flags, 50/20/19 and kappas. Residual (not E39): FINAL_STATUS lists 1 protected_hash_mismatch (HUMAN_AUDIT_APPEND_ONLY_LOG.csv) and LEGACY_AUDIT_LOG_INTEGRITY=UNVERIFIED - report as limitation."))
put("130", 3068, "V9_DATE", ZIP)
put("130", 3068, "ZH_PENDING", (KL, "YES", "YES", S_ST, "E40/E6/E50/E43/E46 items",
                                "Only the E39 component of E44 closes; FINAL_STATUS submission_ready=false agrees with SUBMISSION_READY=NO. Remaining components are genuine open work."))
put("130", 3072, "AUTHOR_CONFIRM", E48); put("130", 3072, "V9_DATE", E48)
put("130", 3073, "V9_DATE", E49)
put("130", 3080, "HUM_PENDING", HIST)
# ---- 131
put("131", 40, "SRC_MISSING", COUNT); put("131", 44, "SRC_MISSING", COUNT)
put("131", 51, "V9_DATE", STAT); put("131", 51, "SRC_MISSING", STAT)
put("131", 52, "SRC_MISSING", MEMB)
put("131", 53, "V9_DATE", FOUR); put("131", 53, "SRC_MISSING", FOUR)
put("131", 97, "ZH_PENDING", D1517); put("131", 104, "ZH_PENDING", E49)
put("131", 129, "AUTHOR_CONFIRM", E48)
put("131", 145, "ZH_PENDING", D1517); put("131", 145, "SRC_MISSING", ZIP)
# ---- 133
put("133", 34, "V9_DATE", ZIP); put("133", 34, "SRC_MISSING", MEMB)
# ---- 135 / 136 / 137
put("135", 15, "VERIFY", HIST); put("135", 44, "V9_DATE", (NA, "N/A", "N/A", "", "", "Parser note: 'V9, 2026-09-29' is a data-version tag, not a citation."))
put("136", 53, "AUTHOR_CONFIRM", (P4, "YES", "PARTIAL", S_E48, "removal of internal flags before submission",
                                  "E39 can be closed now; E48 still needs Phase-4 row-level reproduction of replacement scope/seeds before the last [AUTHOR TO CONFIRM] can be removed."))
put("136", 62, "EMP_PENDING", LEG)
for t in ("HUM_PENDING",):
    put("133", 48, t, LEG); put("133", 51, t, LEG)
put("137", 10, "V9_DATE", ZIP)
put("137", 22, "SRC_MISSING", R[("128", 16, "SRC_MISSING")])
put("137", 35, "V9_DATE", ZIP)

TYPE_DEFAULT = {"EMP_PENDING": EMP, "HUM_PENDING": HUM}

rows = []
for r in csv.DictReader(open(FLAGS, encoding="utf-8")):
    f3 = r["file"][:3]
    key = (f3, int(r["line"]), r["type"])
    if key in R:
        v = R[key]
    elif f3 == "129":
        v = HIST
    elif f3 == "132" and r["type"] == "V9_SHORT":
        v = GKEEP
    elif key == ("134", 138, "UNVERIFIED"):
        v = (NA, "N/A", "N/A", "", "", "Rule text defining when to use UNVERIFIED for stakeholder disclosures; not an open claim.")
    elif r["type"] in TYPE_DEFAULT:
        v = TYPE_DEFAULT[r["type"]]
    elif r["type"] == "PENDING":
        v = HUM if ("ORG" in r["flag"] or "人類" in r["flag"] or "human" in r["flag"].lower()) else EMP
    else:
        v = ("UNASSIGNED", "", "", "", "", "")
    rows.append({"file": r["file"], "section": r["section"], "old_flag": r["flag"], "source_found": v[1], "verified": v[2],
                 "source_artifact": v[3], "new_status": v[0], "line": r["line"], "needed_evidence": v[4], "notes": v[5]})

# extra rows: claims/flags not caught by the literal-pattern scan
F130 = "130_MERGED_MASTER_THESIS_R14_TO_ENTERPRISE_v1_7_EVIDENCE_CONVERGED_CANDIDATE.md"
def extra(f, ln, sec, flag, v):
    rows.append({"file": f, "section": sec, "old_flag": flag, "source_found": v[1], "verified": v[2], "source_artifact": v[3],
                 "new_status": v[0], "line": ln, "needed_evidence": v[4], "notes": v[5]})
extra(F130, 5, "> 稿件狀態", "(claim under V9 flag) 第一位編碼者 50/50、盲式第二編碼 20/20、分歧調和 19/19", COUNT)
extra(F130, 1629, "### 4.5.5 目標式人工標籤替換的局部敏感度", "(unflagged wording) 以人工調和後的標籤替換受稽核記錄的模型標籤", LABSCOPE)
extra(F130, 2268, "### 5.4.2 分類與證據單元的測量界線", "(unflagged wording) 以人工調和標籤替換受稽核記錄後", LABSCOPE)
extra(F130, 2376, "## 5.10 結論", "(unflagged claim) 人工稽核再指出，編碼分歧同時來自模型映射、分類邊界、證據切分與全文擷取品質",
      (MM, "YES", "PARTIAL", S_TAX, "status of the four-source attribution",
       "Stated as an established finding; V9 marks the four sources as INTERPRETIVE_HYPOTHESIS ... NOT_ADJUDICATION for model-vs-human differences, and v1.7 elsewhere (L13, L591, L1559, L2262) says '可能來自'. Wording should be hedged to match (no number change)."))
extra(F130, 3064, "## 附錄 E　作者待決事項與未解決的引文需求", "E40 完整重分析（FULL_REANALYSIS_REQUIRED）的時點與範圍",
      (KL, "YES", "YES", S_ST, "researcher decision + full reanalysis run",
       "FINAL_STATUS: full_reanalysis_requires_researcher_approval=true; ROBUST_CORE_LOCAL_SENSITIVITY_STATUS reanalysis_requires_researcher_approval=true. Genuine open step."))
extra("137_NEXT_ACTIONS.md", 10, "# 137 — NEXT_ACTIONS（投稿關鍵路徑；v1.7）", "P0-1 (second half) 確認 Drive 上沒有比 R14／V9 更新的版本",
      (NF, "NO", "NO", "", "author confirmation / Drive listing", "Cannot be verified from local packages; only the author can confirm."))
rows.sort(key=lambda x: (x["file"], int(x["line"])))
with open(OUT, "w", encoding="utf-8-sig", newline="") as o:
    w = csv.DictWriter(o, fieldnames=["file", "section", "old_flag", "source_found", "verified", "source_artifact", "new_status",
                                      "line", "needed_evidence", "notes"])
    w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), Counter(x["new_status"] for x in rows))
print([ (x["file"][:3], x["line"], x["old_flag"][:60]) for x in rows if x["new_status"] == "UNASSIGNED"])
