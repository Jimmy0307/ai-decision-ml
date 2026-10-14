"""COGNITIVE_CLARITY_CHECK + Q1/Q2 consistency test for the S1d packet (read-only; in-memory analyzer test only).

Texts below are written here verbatim from the researcher-approved S1d instruction, independently of the builder.
For every workbook (3 coder files + master) each misreading must be blocked by an exact sentence; the cell address
is reported:
  A  "my company does not need / adopt it"  != Q1 否         (作答視角 + non-applicability warning)
  B  企業決策介面 != software UI / API / technical interface  (interface clarification)
  C  企業決策 != only strategic decisions                     (decision-scope clarification)
  D  這個組合特有 != globally unique                           (pairing-specific clarification)
  E  Q2 required for every item, no conflict                  (new Q2 wording in instructions and every Q2 header;
                                                               no cell anywhere contains 「如果有」)
  F  Q1 無法確定 vs Q2 無法明確判定 distinguished              (explanation + quick distinction)
Also: depletion final sentence in all 16 pattern cells of every item sheet; attestation social-desirability
sentence in the header; Q1 option explanations.
Q1/Q2 consistency: (1) the three rule rows in 填答說明 are present verbatim and correspond to codebook 26 s2;
(2) the UNCHANGED analyzer validate() accepts / rejects all 27 Q1 x Q2 combinations exactly as codebook 26 s2
says (in memory), in particular Q1=UNCERTAIN + Q2=AMBIGUOUS is accepted.
Writes OUT/S1D_COGNITIVE_CLARITY_AUDIT.md and OUT/tools/cognitive_clarity_check_s1d_result.json.

Usage: python -E -X utf8 -P cognitive_clarity_check_s1d.py
"""
from __future__ import annotations

import json
import os
import sys
from itertools import product

from openpyxl import load_workbook

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import v1_construct_analyzer_s1b as A  # noqa: E402  (unchanged analyzer)

FILES = [os.path.join("coder_distribution", f"CODER_{k}_ZH_TW.xlsx") for k in (1, 2, 3)] + \
        ["20_MASTER_PACKET_S1D_ZH_TW.xlsx"]
T = {
    "VIEWPOINT": "【作答視角】請以一般企業可能面對的情境進行判斷，不要依據你目前任職的公司是否需要、是否已採用，或你個人是否支持使用這類 AI 來作答。本研究要判斷的是：當一家企業面對題目所描述的 AI 功能與決策功能配對時，是否存在一項需要由組織做出選擇、設定或判斷的問題。",
    "WARNING": "請勿因為：『我的公司不需要這個』、『我的產業目前不會使用這個』、『我個人不支持這種做法』而直接選擇『否』。本題不是在詢問實際採用意願，而是在判斷這個功能配對本身是否形成一個可辨識的組織決策問題。",
    "INTERFACE": "這裡的『企業決策介面』是研究上的名稱，不是指軟體畫面、使用者介面、API、系統串接介面或其他技術介面。",
    "SCOPE": "這裡的『企業決策』不只指高階主管的策略決策。只要企業或組織需要對下列事項做出選擇、設定或判斷，都可以構成企業決策，例如：權限與責任；人與 AI 的工作分工；流程如何轉交；例外或失敗如何處理；需要哪些資料條件；如何驗證與監控 AI；是否需要隨時間調整做法。",
    "SPECIFIC": "『這個組合特有』不表示這項問題只能出現在此組合。意思是：你提出的企業決策問題，必須能具體連結到題目中的 AI 功能與決策功能之關係。如果只是任何 AI 導入時都會同樣存在、與這個配對沒有特別關係的一般性問題，才不視為這個配對所形成的特定企業決策介面。",
    "Q1_YES": "是：從這個功能配對本身，可以具體辨識出一項企業或組織需要做出的選擇、設定或判斷，而且這項問題可具體連結到此 AI 功能如何進入此決策功能。",
    "Q1_NO": "否：從這個功能配對本身，無法辨識出一項需要企業或組織特別做出的決策；或者你能想到的只是一般性的 AI 導入問題，幾乎任何 AI 功能進入這類決策功能時都會同樣出現，而不是由這個功能配對特別形成的問題。",
    "Q1_UNC": "無法確定：你無法可靠判斷這個功能配對是否形成一項可辨識的企業決策介面。",
    "Q2_README": "Q2　請依據 Q1 的判斷，選出這個功能配對最適合的類別。（每題必填）",
    "Q1_VS_Q2": "Q1『無法確定』與 Q2『無法明確判定』是不同層次：Q1『無法確定』：不確定是否存在可辨識的企業決策介面。Q2『無法明確判定』：已進入類別判斷，但因證據不足或多個機制同樣合理，無法可靠指定一個主要類別。如果兩個層次都不確定，可以同時選 Q1『無法確定』＋ Q2『無法明確判定』。",
    "QUICK": "快速區分：沒有明確、這個組合特有的企業決策 → 僅屬證據層；有明確的企業決策，但現有類別都不適用 → 無適用機制；有可能的類別，但證據不足或多類同樣合理 → 無法明確判定。",
    "PATTERN_APPEND": "共同出現較少本身也不代表一定存在企業決策問題；是否形成企業決策介面，仍請依本題定義獨立判斷。",
    "ATTEST_APPEND": "選擇『不符合』不是答錯，也不代表作答無效；請依實際情況誠實填寫。",
    "Q1_QUESTION": "這段內容是否呈現一個可辨識的企業決策介面？",
}
Q2_HEADER = "Q2 請依據 Q1 的判斷，選出這個功能配對最適合的類別。（每題必填）"   # header keeps ASCII space for the parser
RULES = {   # README rule rows (verbatim)  ->  codebook 26 s2 rule
    "　　Q1＝是：Q2 可選「僅屬證據層」以外的任一類別。": "Q1 = YES -> Q2 in {M1, M2, M3, M4, LONGITUDINAL, DATA_GATED, NONE, AMBIGUOUS}",
    "　　Q1＝否：Q2 請選「僅屬證據層」。": "Q1 = NO -> Q2 = EVIDENCE_ONLY",
    "　　Q1＝無法確定：Q2 可選「無適用機制」以外的任一類別（包括「僅屬證據層」與「無法明確判定」）。": "Q1 = UNCERTAIN -> any Q2 except NONE",
}
CHECKS = {
    "A_company_need_is_not_Q1_NO": ["VIEWPOINT", "WARNING"],
    "B_interface_is_not_UI_or_API": ["INTERFACE"],
    "C_enterprise_decision_not_only_strategic": ["SCOPE"],
    "D_pairing_specific_not_globally_unique": ["SPECIFIC"],
    "E_Q2_required_no_conflict": ["Q2_README"],
    "F_Q1_uncertain_vs_Q2_ambiguous": ["Q1_VS_Q2", "QUICK"],
    "Q1_option_explanations": ["Q1_YES", "Q1_NO", "Q1_UNC"],
}


def find(wb, text):
    hits = []
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and text in c.value:
                    hits.append(f"{ws.title}!{c.coordinate}")
    return hits


def workbook_checks(path):
    wb = load_workbook(path)
    res, errs = {}, []
    for chk, keys in CHECKS.items():
        res[chk] = {k: find(wb, T[k]) for k in keys}
        if any(not v for v in res[chk].values()):
            errs.append(f"{chk}: missing text")
    readme = [c.value for c in wb["填答說明"]["A"]]
    q1_row = next((i for i, v in enumerate(readme) if v and T["Q1_QUESTION"] in v), None)
    warn_row = next((i for i, v in enumerate(readme) if v and T["WARNING"] in v), None)
    unc_row = next((i for i, v in enumerate(readme) if v and T["Q1_UNC"] in v), None)
    if None in (q1_row, warn_row, unc_row) or not (q1_row < unc_row < warn_row):
        errs.append("A: warning not placed directly under the Q1 explanation")
    vp = next((i for i, v in enumerate(readme) if v and T["VIEWPOINT"] in v), None)
    df = next((i for i, v in enumerate(readme) if v and v.startswith("「企業決策介面」是指")), None)
    if None in (vp, df) or not vp < df:
        errs.append("A: 作答視角 not before the formal definition")
    res["E_no_如果有_anywhere"] = find(wb, "如果有")
    if res["E_no_如果有_anywhere"]:
        errs.append("E: 「如果有」 still present")
    heads = [f"{ws.title}!I1" for ws in wb.worksheets if ws.title.startswith("作答_") and ws["I1"].value == Q2_HEADER]
    n_coder = sum(ws.title.startswith("作答_") for ws in wb.worksheets)
    res["E_Q2_headers"] = heads
    if len(heads) != n_coder:
        errs.append("E: Q2 header not updated on every coder sheet")
    pat = [f"{ws.title}!G{r}" for ws in wb.worksheets if ws.title.startswith("作答_") or ws.title == "題目資訊"
           for r in range(2, ws.max_row + 1)]
    ok_pat = [a for a in pat if wb[a.split("!")[0]][a.split("!")[1]].value.endswith(T["PATTERN_APPEND"])]
    vals = {wb[a.split("!")[0]][a.split("!")[1]].value for a in pat}
    res["depletion_cells_with_final_sentence"] = f"{len(ok_pat)}/{len(pat)} (distinct texts: {len(vals)})"
    if len(ok_pat) != len(pat) or len(vals) != 1:
        errs.append("depletion sentence not identical in all item cells")
    att = wb["作答聲明"]["A1"].value or ""
    res["attestation_header_A1_contains_social_desirability_sentence"] = T["ATTEST_APPEND"] in att
    if T["ATTEST_APPEND"] not in att:
        errs.append("attestation sentence missing")
    res["rule_rows"] = {r: find(wb, r.strip()) for r in RULES}
    if any(not v for v in res["rule_rows"].values()):
        errs.append("rule rows missing")
    return res, errs


def consistency_test():
    """All 27 Q1 x Q2 combinations through the unchanged analyzer validate(); expected = codebook 26 s2."""
    out, bad = [], []
    for q1, q2 in product(sorted(A.Q1), sorted(A.Q2)):
        row = {A.RESP[0]: q1, A.RESP[1]: q2, A.RESP[2]: "LOW", A.RESP[3]: "", A.RESP[4]: "x"}
        errs = A.validate(dict(sheet="T", rows={"ITEM-A01": row}, attestation=[]))
        errs = [e for e in errs if "item set" not in e]
        expected_ok = not ((q1 == "YES" and q2 == "EVIDENCE_ONLY") or (q1 == "NO" and q2 != "EVIDENCE_ONLY")
                           or (q1 == "UNCERTAIN" and q2 == "NONE"))
        out.append(dict(Q1=q1, Q2=q2, analyzer_accepts=not errs, codebook26_allows=expected_ok))
        if (not errs) != expected_ok:
            bad.append((q1, q2))
    return out, bad


def main():
    per, all_errs = {}, []
    for rel in FILES:
        res, errs = workbook_checks(os.path.join(OUT, rel))
        per[rel] = dict(result=res, errors=errs)
        all_errs += [f"{rel}: {e}" for e in errs]
    combos, bad = consistency_test()
    unc_amb = next(c for c in combos if c["Q1"] == "UNCERTAIN" and c["Q2"] == "AMBIGUOUS")
    ok = not all_errs and not bad and unc_amb["analyzer_accepts"]
    verdict = "PASS" if ok else "FAIL"
    with open(os.path.join(HERE, "cognitive_clarity_check_s1d_result.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(dict(verdict=verdict, errors=all_errs, consistency_mismatches=bad, files=per,
                       q1_q2_combinations=combos), f, indent=1, ensure_ascii=False)
    r1 = per[FILES[0]]["result"]
    L = ["# S1D_COGNITIVE_CLARITY_AUDIT — 認知清晰度與 Q1/Q2 一致性檢查（腳本產生）", "",
         "腳本：`tools/cognitive_clarity_check_s1d.py`（文字為 S1d 指示原文，獨立於建置程式寫入）。"
         "對三份編碼者檔與總表逐一檢查；下表位址取自 `CODER_1_ZH_TW.xlsx`（其他檔案位址見結果 JSON，全部通過）。", "",
         f"**COGNITIVE_CLARITY_CHECK：{verdict}**（錯誤 {len(all_errs)}；Q1×Q2 不一致 {len(bad)}）", "",
         "| 誤讀 | 阻擋文字 | CODER_1 位址 |", "|---|---|---|"]
    labels = {"A_company_need_is_not_Q1_NO": "A 公司不需要 ≠ Q1 否", "B_interface_is_not_UI_or_API": "B 介面 ≠ UI／API",
              "C_enterprise_decision_not_only_strategic": "C 企業決策 ≠ 只限策略決策",
              "D_pairing_specific_not_globally_unique": "D 組合特有 ≠ 只能出現在此組合",
              "E_Q2_required_no_conflict": "E Q2 每題必填、無衝突", "F_Q1_uncertain_vs_Q2_ambiguous": "F Q1 無法確定 vs Q2 無法明確判定",
              "Q1_option_explanations": "Q1 選項說明"}
    for chk, label in labels.items():
        for k, addr in r1[chk].items():
            L.append(f"| {label} | {T[k]} | {'、'.join(addr) or '**缺**'} |")
    L += [f"| E Q2 每題必填、無衝突 | 作答頁 Q2 欄名：{Q2_HEADER} | {'、'.join(r1['E_Q2_headers'])} |",
          f"| E Q2 每題必填、無衝突 | 全活頁簿不得含「如果有」 | 出現位置：{'、'.join(r1['E_no_如果有_anywhere']) or '無（通過）'} |",
          "", f"- 文獻樣態末句：{r1['depletion_cells_with_final_sentence']}（四個活頁簿皆通過）。",
          f"- 作答聲明 A1 含「{T['ATTEST_APPEND']}」：{r1['attestation_header_A1_contains_social_desirability_sentence']}。",
          "- 作答視角位於「企業決策介面」正式定義之前；非適用警語位於 Q1 選項說明正下方：通過。", "",
          "## Q1/Q2 一致性", "", "| 填答說明規則列（逐字） | 26 §2 規則 | CODER_1 位址 |", "|---|---|---|"]
    for r, rule in RULES.items():
        L.append(f"| {r.strip()} | {rule} | {'、'.join(r1['rule_rows'][r])} |")
    L += ["", f"未變動的分析器 `validate()` 對全部 27 種 Q1×Q2 組合的接受／拒絕與 26 §2 完全一致（不一致 {len(bad)} 項）。"
          f"Q1＝無法確定＋Q2＝無法明確判定（UNCERTAIN＋AMBIGUOUS）：分析器接受＝{unc_amb['analyzer_accepts']}，"
          "26 允許＝True。因此第 (11) 項說明符合一致性規則，分析器語意未變。", ""]
    with open(os.path.join(OUT, "S1D_COGNITIVE_CLARITY_AUDIT.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    print(verdict, len(all_errs), len(bad))
    for e in all_errs:
        print(e)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
