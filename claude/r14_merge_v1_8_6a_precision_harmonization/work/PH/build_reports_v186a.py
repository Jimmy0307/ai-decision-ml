"""Build OUT 02 (changelog), 03 (terminology report), 05 (outer-section precision audit) for V1.8.6a.
Usage: python -I build_reports_v186a.py <V1.8.6 01 md> <V1.8.6a 01 md> <patches json> <verify json> <OUT dir>"""
import sys, re, json, hashlib, os

sys.stdout.reconfigure(encoding="utf-8")
A = open(sys.argv[1], encoding='utf-8').read()
B = open(sys.argv[2], encoding='utf-8').read()
P = json.load(open(sys.argv[3], encoding='utf-8'))
V = json.load(open(sys.argv[4], encoding='utf-8'))
OUT = sys.argv[5]
la = A.split('\n')
SHA_A, SHA_B = hashlib.sha256(A.encode()).hexdigest(), hashlib.sha256(B.encode()).hexdigest()
PID = {p['id']: p for p in P}
esc = lambda s: s.replace('|', '¦').replace('\n', ' ⏎ ')

# ------------------------------------------------------------------ 03 classification
# key: global ordinal n over regex 企業決策介面|介面|[Ii]nterfaces? in V1.8.6 01
CLS = {
 1: ('a', 'H03', 'construct term (enterprise decision the enterprise must make)'),
 2: ('a', 'H04', 'construct term (four M1–M4 decision mechanisms)'),
 3: ('d', None, 'EN "functional interface in the literature" = literature-level AI × decision functional interface (接口), not the V1 construct'),
 4: ('d', None, 'EN "under-integrated interfaces" = literature-level functional interfaces (接口)'),
 5: ('a', 'H05', 'EN construct term'),
 6: ('a', 'H06', 'EN construct term (four enterprise decision mechanisms M1–M4)'),
 7: ('d', None, 'EN "A literature interface" = literature-level functional interface'),
 8: ('a', 'H07', 'construct term (the translated decision element)'),
 9: ('a', 'H08', 'construct term'),
 10: ('a', 'H09', 'construct term (the four M1–M4)'),
 11: ('a', 'H10', 'construct term in the evidence chain'),
 12: ('c', None, 'v2.2 model term: Q8 interface activation test (介面活化檢驗)'),
 13: ('a', 'H11', 'construct term in RQ3'),
 14: ('a', 'H11', 'construct term in RQ3 (→ 轉譯後的機制, matching the Abstract/§1.4 integrated claim)'),
 15: ('c', None, 'v2.2 model term: Q8 介面活化檢驗 (Table 1-1)'),
 16: ('a', 'H12', 'construct term'),
 17: ('a', 'H13', 'construct term'),
 18: ('a', 'H14', 'construct term'),
 19: ('c', None, 'technical readiness term: data availability / interface → model threshold keys R_j(s), D_j(s)'),
 20: ('a', 'H15', 'construct term (企業介面 = translated enterprise decision element)'),
 21: ('c', None, 'v2.2 model term: Q8 介面活化檢驗'),
 22: ('c', None, 'technical interface: AI features embedded in platform interfaces (Edwards & Murthy, 2026)'),
 23: ('a', 'H16', 'construct term; the model label I1–I4 is retained in parentheses'),
 24: ('a', 'H17', 'construct term'),
 25: ('a', 'H18', 'construct DEFINITION; terminology note added here (企業決策介面 = earlier wording, same construct; I1–I5 = model labels)'),
 26: ('c', None, 'model label: the I1–I5 structure of the following table (同一介面 = same I_k); covered by the §3.9.1 note'),
 27: ('c', None, 'model label: no I_k → evidence layer'),
 28: ('c', None, 'model label: 企業介面 = I1–I5 structure (S2)'),
 29: ('c', None, 'model label: 收斂後的企業介面有五個 (I1–I5)'),
 30: ('c', None, 'model label: header of the I1–I5 table (Table in §3.9.1)'),
 31: ('c', None, 'model label: Table 3-4 header 企業介面 (protected table; byte-identical)'),
 32: ('c', None, 'model label: Table 3-4 is organised by I_k'),
 33: ('a-kept', None, 'construct term kept as historical label: names the Table 3-4A column 「企業決策介面」 (Table 3-4A is protected); the §3.9.1 note states it is the earlier wording of 企業決策機制, not a third construct'),
 34: ('c', None, 'model label: lists the Table 3-4A columns (介面 = the I_k column)'),
 35: ('a-kept', None, 'Table 3-4A column header (protected, byte-identical); historical wording covered by the §3.9.1 note'),
 36: ('c', None, 'Table 3-4A cell (protected): 無獨立介面 = no separate I_k'),
 37: ('b-sync', 'H19', 'coder-facing description of Q1: synced to the S1e wording 企業決策過程 (S1e Q1: 「這段內容是否呈現一個可辨識的企業決策過程？」); verbatim S1e sentence inserted before it'),
 38: ('b-sync', 'H20', 'coder-facing NONE definition: synced to S1e (「只有在存在企業決策過程…」)'),
 39: ('b-sync', 'H21', 'coder-facing EVIDENCE_ONLY rule: synced to S1e (「沒有可辨識的決策過程時，請選『僅屬證據層』」)'),
 40: ('d', None, 'quoted rollback-rule label 「研究者提出、未獲獨立支持的介面」 from the frozen construct-freeze document 41 (§3.9.5); refers to the I_k of a rejected mechanism; kept verbatim'),
 41: ('d', None, 'same quoted rollback-rule label (§3.9.5 rule (2))'),
 42: ('c', None, 'model label: rollback rule (3) 「G04 有獨立介面」 = an I_k outside I1–I4'),
 43: ('b-kept', 'H23', 'historical quotation of the S1d coder-facing wording; the sentence is updated because §3.9.3 is now synced (it no longer says §3.9.3 uses 企業決策介面)'),
 44: ('c', None, 'v2.2 model term: F5 R_j(s), D_j(s) 資料可得性、共用介面 (data/interface threshold keys)'),
 45: ('c', None, 'v2.2 model term: 介面活化檢驗 (Table 3-10 Q8)'),
 46: ('c', None, 'v2.2 model term: interface activation test (EN gloss)'),
 47: ('c', None, 'v2.2 model term: 介面 I1–I4 (Q8)'),
 48: ('c', None, 'v2.2 model term: interface classified ACTIVE/INACTIVE (Q8)'),
 49: ('c', None, 'v2.2 model term: Q8 interface vs Q1–Q6 quantities'),
 50: ('c', None, 'v2.2 model term: (F5e) 資料／介面門檻'),
 51: ('d', None, 'section title 3.14.5 外部評估介面 = organisational interface with external evaluators; not the construct'),
 52: ('b-sync', 'H25', 'coder-facing Q1 row of Table 4-13: synced to S1e (企業決策過程) with the construct named'),
 53: ('c', None, 'v2.2 model term: (F5e) 資料／介面門檻 (Table 4-20, SIMULATED_ONLY)'),
 54: ('c', None, 'v2.2 model term: 介面活化 (Table 4-28)'),
 55: ('c', None, 'code key derived.interface_activation'),
 56: ('c', None, 'v2.2 model term: Table 4-32 title 介面活化（Q8）'),
 57: ('c', None, 'model label: Table 4-32 header (I1–I4)'),
 58: ('c', None, 'v2.2 model term: Q8 介面活化 (Table 4-33)'),
 59: ('a', 'H26', 'construct term'),
 60: ('d', None, 'literature-level functional interface (技術—治理介面 between two AI × decision family regions)'),
 61: ('d', None, 'literature-level functional interface (直接轉譯介面)'),
 62: ('a', 'H27', 'construct term (Table 5-1 claim row)'),
 63: ('c', None, 'v2.2 model term: Q8 介面活化檢驗 (Table 5-1)'),
 64: ('c', None, 'model term: the I_k classified INACTIVE by Q8'),
 65: ('c', None, 'model term: the I_k classified INACTIVE by Q8'),
 66: ('c', None, 'model label: I1–I4 介面'),
 67: ('a', 'H28', 'construct term (heading §5.5)'),
 68: ('c', None, 'model label: 企業介面 I1 (M1 named in the same sentence)'),
 69: ('d', None, 'quoted rollback-rule label from §3.9.5 / document 41 (kept verbatim)'),
 70: ('c', None, 'v2.2 model term: Q8 介面活化檢驗'),
 71: ('c', None, 'model term: object of the Q8 test (轉譯而來的介面)'),
 72: ('a', 'H29', 'construct term outside the Q8 sentence (→ 轉譯後的機制)'),
 73: ('a', 'H30', 'construct term'),
 74: ('a', 'H31', 'construct term (four M1–M4)'),
 75: ('c', None, 'technical interface: verbatim source quote "platform interfaces" (Appendix B N82)'),
 76: ('c', None, 'technical interface: 嵌入平台介面 (Appendix B N82)'),
 77: ('c', None, 'v2.2 model term: Interface activation test (Appendix C.5, verbatim v2.2)'),
 78: ('c', None, 'v2.2 model term: 介面 I1–I4 (Appendix C.5, verbatim v2.2)'),
}
occ = []
n = 0
for i, l in enumerate(la, 1):
    for m in re.finditer(r'企業決策介面|介面|[Ii]nterfaces?', l):
        n += 1
        occ.append((n, i, m.group(0), l[max(0, m.start() - 22):m.end() + 14]))
assert n == len(CLS) == 78, n


def after_text(cls, pid, ctx):
    if pid is None:
        return 'unchanged'
    p = PID[pid]
    return p['new'] if len(p['new']) < 260 else p['new'][:240] + '…'


rows = []
tally = {}
for (k, line, term, ctx) in occ:
    cls, pid, why = CLS[k]
    key = ('企業決策介面' if term == '企業決策介面' else ('EN interface' if term.lower().startswith('interface') else '介面 (bare)'), cls)
    tally[key] = tally.get(key, 0) + 1
    action = ('CHANGED (' + pid + ')') if (pid and cls in ('a', 'b-sync')) else ('KEPT; sentence edited (' + pid + ')' if pid else 'KEPT')
    rows.append(f"| {k} | {line} | {term} | …{esc(ctx)}… | {action}: {esc(after_text(cls, pid, ctx)) if pid else 'unchanged'} | {cls} | {esc(why)} |")

CLASS_DEF = """- **a** = construct term → changed to 企業決策機制 (EN: enterprise decision mechanism).
- **a-kept** = construct term kept as a quoted historical / protected-table label; the §3.9.1 note (H18) states that 「企業決策介面」 was the earlier theoretical wording of 企業決策機制, not a third construct.
- **b-sync** = coder-facing description of the S1d/S1e instrument → synced to the S1e wording 「企業決策過程」 (packets untouched).
- **b-kept** = coder-facing quotation kept (historical S1d wording), sentence updated.
- **c** = technical interface or v2.2 model term/label (I1–I5, 介面活化檢驗, 資料／介面門檻, (F5e), R_j/D_j 共用介面, 使用者介面, platform interfaces, code keys) → kept; changing it would alter model-term semantics.
- **d** = other (literature-level functional interface 接口 in EN/zh prose, quoted rollback-rule label from document 41, organisational 外部評估介面) → kept."""

t03 = []
t03.append("# 03 — V1.8.6a Terminology Harmonization Report (RD-1)\n")
t03.append(f"- **Base:** V1.8.6 `01_V1_8_6_THEORY_INTEGRATED_MANUSCRIPT.md`, sha256 `{SHA_A}` (asserted before patching).")
t03.append(f"- **Output:** `01_V1_8_6A_MANUSCRIPT.md`, sha256 `{SHA_B}`.")
t03.append("- **Method:** `work/PH/patch_v186a.py` (exact, asserted-once replacements; no global replace) and `work/PH/verify_v186a.py` (52/52 hard checks PASS). Line numbers below are V1.8.6 01 lines.")
t03.append("- **Decision applied:** theoretical term = 「企業決策機制」 (「組織決策安排」 where organisational configuration is emphasised). S1e coder-facing wording stays 「企業決策過程」; the S1e packets were not touched (sha256 cbbbaa0a… / 5925ead5… / 50d8c818…, re-hashed after the build).\n")
t03.append("## 1. Verbatim S1e sentence (first mention of the V1 instrument)\n")
t03.append("Inserted once, at §3.9.3 item (4) 「編碼工具（Q1–Q5）」, the first place in the body where the V1 instrument (questionnaire) is described (patch H19):\n")
t03.append("> 為降低獨立編碼者的理解負擔，S1e 問卷採用『企業決策過程』作為 coder-facing wording；其所對應的理論構念仍為本文所稱之企業決策機制／組織決策安排，並不構成另一個不同構念。\n")
t03.append("Verification: the sentence occurs exactly once; it lies inside §3.9.3 item (4); it is the first body mention of 「S1e」 (the only earlier mention is the L5 version/status meta-line, which describes this V1.8.6a pass). §3.9.3 now contains 0 × 「企業決策介面」 and 4 × 「企業決策過程」.\n")
t03.append("## 2. V1-design locations synchronised\n")
t03.append("| Location | Patch | Change |\n|---|---|---|")
for pid, loc in [('H19', '§3.9.3 (4) Q1'), ('H20', '§3.9.3 (4) NONE'), ('H21', '§3.9.3 (4) EVIDENCE_ONLY rule'), ('H22', '§3.9.3 目前狀態 (S1e packet version)'),
                 ('H23', '§3.9.6 輔助類別 (sentence about §3.9.3)'), ('H24', 'Table 3-14 V1 row status'), ('H25', 'Table 4-13 Q1 row'), ('H32', 'Appendix E6'), ('H18', '§3.9.1 terminology note')]:
    t03.append(f"| {loc} | {pid} | {esc(PID[pid]['new'][:300])}{'…' if len(PID[pid]['new']) > 300 else ''} |")
t03.append("\nS1e facts used (all from the S1e records, `V1_S1E_CURRENT_STATUS.md`, `S1E_PROCESS_WORDING_CHANGELOG.md`, `FREEZE_MANIFEST_V1_S1E_PROCESS_WORDING.txt`, and the CODER_1 packet text read read-only): coder-facing term 企業決策介面 → 企業決策過程; scope = wording + answer-sheet layout; 16 items, per-coder random order, category semantics, Q1/Q2 consistency rules and Q3–Q5 semantics preserved; S1d preserved; teacher review APPROVED_TO_RUN; READY_TO_DISTRIBUTE = YES; HUMAN_RESULTS = NONE. Not changed: protocol, codebook semantics, categories, analysis plan, any number.\n")
t03.append("## 3. Classes\n")
t03.append(CLASS_DEF + "\n")
t03.append("## 4. Counts\n")
t03.append("| Term | Class | Count (V1.8.6) |\n|---|---|---|")
for (term, cls), c in sorted(tally.items()):
    t03.append(f"| {term} | {cls} | {c} |")
tc = V['term_counts']
t03.append(f"\nWhole-document string counts V1.8.6 → V1.8.6a: 企業決策介面 {tc['企業決策介面'][0]} → {tc['企業決策介面'][1]}; 企業決策過程 {tc['企業決策過程'][0]} → {tc['企業決策過程'][1]}; 企業決策機制 {tc['企業決策機制'][0]} → {tc['企業決策機制'][1]}; 組織決策安排 {tc['組織決策安排'][0]} → {tc['組織決策安排'][1]}; 介面 (all, incl. inside 企業決策介面) {tc['介面'][0]} → {tc['介面'][1]}.")
t03.append("\nThe 5 remaining 「企業決策介面」 in V1.8.6a: L5 (version note naming it as the earlier wording), L667 (the §3.9.1 terminology note), L699 and L703 (Table 3-4 lead-in naming the Table 3-4A column, and the protected Table 3-4A header; class a-kept), L779 (historical S1d quotation, class b-kept).")
t03.append("\nTechnical / model-term counts (V1.8.6 → V1.8.6a; none decreased): " + "; ".join(f"{k} {v[0]}→{v[1]}" for k, v in V['technical_or_model_interface_counts'].items()) + ".\n")
t03.append("## 5. Full inventory (every 「企業決策介面」, bare 「介面」 and EN interface occurrence in V1.8.6 01)\n")
t03.append("| # | Line | Term | Before (context) | After | Class | Reason |\n|---|---|---|---|---|---|---|")
t03.extend(rows)
t03.append("\n## 6. Kept on purpose (math / model semantics)\n")
t03.append("- No math span, equation tag, G row, Table 3-4/3-4A row or note, or Appendix C.1–C.9 text was edited (hard checks). The v2.2 model terms 「介面 I1–I5」, 「介面活化檢驗」/interface activation test, `derived.interface_activation`, 「資料／介面門檻」(F5e) and 「共用介面」 (R_j, D_j) are model terms, not the V1 construct, and are kept. Renaming them would alter model-term semantics, so they are reported here and left unchanged.")
t03.append("- Literature-level 「接口」/EN \"interface\" (functional AI × decision pairing) and 「技術—治理介面」「直接轉譯介面」 in §5.3.1 are literature-structure terms and are kept.")
t03.append("- The rollback-rule label 「研究者提出、未獲獨立支持的介面」 (§3.9.5 ×2, §5.8.4) is quoted from the frozen construct-freeze document 41 and refers to the I_k of a rejected mechanism; kept verbatim (class d).")
t03.append("\n```\nENTERPRISE_DECISION_INTERFACE_BEFORE=17\nENTERPRISE_DECISION_INTERFACE_AFTER=5\nCHANGED_TO_MECHANISM=11 (zh) + 2 EN\nSYNCED_TO_S1E_PROCESS=3 (+ 1 bare 介面 in the EVIDENCE_ONLY rule)\nKEPT_HISTORICAL_OR_PROTECTED=3\nBARE_介面_CHANGED=" +
           str(sum(1 for (k, line, term, ctx) in occ if term == '介面' and CLS[k][0] in ('a', 'b-sync'))) +
           "\nBARE_介面_KEPT=" + str(sum(1 for (k, line, term, ctx) in occ if term == '介面' and CLS[k][0] not in ('a', 'b-sync'))) +
           "\nGLOBAL_REPLACE=NO\nS1E_PACKETS_CHANGED=NO\nVERBATIM_S1E_SENTENCE_INSERTED=YES (§3.9.3 (4), once)\n```")
open(os.path.join(OUT, '03_TERMINOLOGY_HARMONIZATION_REPORT.md'), 'w', encoding='utf-8').write('\n'.join(t03) + '\n')

# ------------------------------------------------------------------ 05 outer-section precision audit
RD5 = ['H35', 'H36', 'H37', 'H38', 'H39', 'H40', 'H41', 'H42', 'H43', 'H44', 'H45', 'H46', 'H47', 'H48']
SW = ['H49', 'H52']
t05 = ["# 05 — V1.8.6a Outer-Section Precision Audit (RD-5) and Claim-Consistency Sweep\n",
       f"- **Audited / patched file:** `01_V1_8_6A_MANUSCRIPT.md` sha256 `{SHA_B}`; base V1.8.6 `{SHA_A[:8]}…`.",
       "- **Authority for claim wording:** V1.8.6 `06_V1_8_6_THEORY_STATUS_MATRIX.md` (row cited per edit). Rule: only reduce overclaim, add scope conditions, separate necessary/sufficient, existence/universal, synthetic/empirical, AI-specific/general, human reliability/validity. No new claim; no citation added.",
       "- Line numbers are V1.8.6 01 lines.\n",
       "## 1. RD-5 items (from V1.8.6 12 RD-5 / 02 RD-5)\n",
       "| # | Patch | Location | Old | New | Matrix row / justification |", "|---|---|---|---|---|---|"]
for i, pid in enumerate(RD5, 1):
    p = PID[pid]
    t05.append(f"| {i} | {pid} | {p['section']} (l.{p['line_src']}) | {esc(p['old'])} | {esc(p['new'])} | {esc(p['source'])} |")
t05.append("\n**RD-5 list status:** Table 1-1 RQ4–RQ6 → RESOLVED (H35–H37). §2.13 implications → RESOLVED (H38 necessary/sufficient; H39 model-internal vs literature attribution, without the theory pack's TO-VERIFY analogue clause). Table 4-33 RQ6 VOI qualifier → RESOLVED (H46; plus RQ5 H44, H45). §4.10.3 → RESOLVED (H43). §3.12.5 Q2/Q4/Q7 rows → RESOLVED (H40–H42; Q1, Q3, Q5, Q8 rows need no change; Appendix C.5 is verbatim v2.2 and stays). §5.8.4 / §5.8.5 pointers → RESOLVED (H47, H48). Abstract / English Abstract: the screening clause was already bounded in V1.8.6 (T46/T47); the remaining 「以證明草稿說明」/\"Proof sketches indicate\" is accurate (C.6 contains proof sketches) → no change. MINOR items of V1.8.6 05/11 not yet applied: none (m1–m15 and n1 were resolved in V1.8.6 per the re-audits).\n")
t05.append("## 2. Claim-consistency sweep\n")
t05.append("Whole-document term scan (`work/PH/sweep.py`; hits in `work/PH/sweep_hits_v186a.tsv`, V1.8.6 baseline in `sweep_hits_v186.tsv`). Counts V1.8.6 → V1.8.6a:\n")
ca = json.load(open(os.path.join(OUT, 'work', 'PH', 'sweep_counts_v186.json'), encoding='utf-8'))
cb = json.load(open(os.path.join(OUT, 'work', 'PH', 'sweep_counts_v186a.json'), encoding='utf-8'))
t05.append("| Term | V1.8.6 | V1.8.6a | Finding |\n|---|---|---|---|")
FIND = {
 '企業決策介面': 'See 03: 14 changed / synced, 3 kept as historical or protected labels; 2 new mentions in notes.',
 '企業決策過程': 'Only as the S1e coder-facing wording (§3.9.3, §3.9.6, Table 3-14, Table 4-13, E6, L5).',
 '企業決策機制': 'Theoretical construct term throughout.',
 '組織決策安排': 'Only as the alternative wording in the notes (L5, §3.9.1, §3.9.3 verbatim sentence).',
 '最小充分/minimal sufficient': '0 hits. M1–M4 are never called minimal sufficient.',
 '完整/complete': 'Technical (完整列舉, 完整重分析, 完整證明…) or negated (不宣稱…完備, 不窮盡). M1–M4 never called a complete taxonomy.',
 '非冗餘/non-redundant': 'M1–M4: "non-redundant under T1–T4 relative to the v2.2 attribute schema (definitional)", sufficiency PARTIAL; operational distinguishability "to be tested by V1, not yet run" (l.113, l.775 kept). Other hits are Burt non-redundant ties.',
 '必要/necessary': 'DL necessary conditions only under AL3 + exact ties, plus the AL3 channel; GS-N exact ties. One imprecise sentence fixed (H49).',
 '充分/sufficient': 'DL sufficient conditions (Cor DL-3 unique first best; DL-4 for DL = 0), GS-1, D4/D5 ("alignment sufficient, not necessary"), H38. Never written as iff.',
 '若且唯若/iff': 'Only first-best-relative (DL-1), unique-first-best (Cor DL-3), Lemma S, R1/R2, G4/G7, P^C = P^B ⇔ AL3; 充要 only negated / NOT_PROVEN. No DL iff theorem.',
 '定理/theorem': 'Thm GS-N, Thm E.7 (theorems); Thm D1/D3/R1 always tagged 重述. DL-1 is a lemma, GS-I an identity.',
 '驗證/validated': 'Only "合成驗證完成（僅合成）" and negations; no "validated" construct or model.',
 '構念效度/construct validity': 'Always pending (V1 HUMAN RESULT PENDING) or negated (AI pilot / researcher adjudication ≠ construct validity).',
 '實證/empirical': 'All pending or negated (EMPIRICAL RESULT PENDING; 不是企業實證證據). §5.7 AI-specific empirical parameterisation now tagged V7 尚未執行 (H52).',
 'AI 特有/AI-specific': 'General formal property vs AI-specific instantiation split kept (l.182, l.2397); "AI 特定的推論（不是新結果）" in C.10.3.',
 '最適/optimal': 'Model-internal (首佳、最適解、最佳回應) or negated (不宣稱最適的企業人工智慧架構; VOI-greedy optimality NOT_PROVEN).',
 '可推廣/generalizable': 'Negated (不可外推, 外部效度未知) or "formal scope, not empirical generalizability".',
}
for k in ca:
    t05.append(f"| {k} | {ca[k]} | {cb[k]} | {FIND.get(k, '')} |")
t05.append("\n**Confirmed boundaries (after this pass):**")
t05.append("- M1–M4 = a mechanism decomposition defined by the decision-object criterion, non-redundant under T1–T4 relative to the v2.2 attribute schema (definitional); operational distinguishability is to be tested by V1 (not run); NOT minimal sufficient, NOT a complete taxonomy (06 rows M1–M4).")
t05.append("- DL = necessary conditions and sufficient conditions exist (and a first-best-relative characterization lemma); no primitive iff (06 rows DL).")
t05.append("- Governance screening = conditional formal result (identity GS-I, sufficient GS-1, necessary GS-N in exact ties; never \"always\") (06 rows Screening).")
t05.append("- Shared capability = existence of a non-interval build region (Prop D6), D1/D3 restatements; never \"generally non-monotone\" (06 rows Shared capability).")
t05.append("- VOI/robustness: vertex exactness only for Model B (and A+) whole portfolio; VOI order only for a fixed candidate set; sequential identification PARTIAL (06 rows VOI, Robustness).")
t05.append("\n**Inconsistencies found and fixed (minimal edits):**\n")
t05.append("| Patch | Location | Old | New | Matrix row |\n|---|---|---|---|---|")
for pid in SW:
    p = PID[pid]
    t05.append(f"| {pid} | {p['section']} (l.{p['line_src']}) | {esc(p['old'])} | {esc(p['new'])} | {esc(p['source'])} |")
t05.append("\nNo other contradiction with the 06 matrix was found. Not edited on purpose: the P4/P7 formal statements (「在 C 中只有帳本對齊時才保證」) — they are P1–P8 formal statements (protected) and are already bounded by Prop D4/D5 at §3.12.4 and C.10.4; Appendix C.5/C.6 (verbatim v2.2; superseding notes already in C.10.2/C.10.4).\n")
t05.append("```\nRD5_ITEMS_RESOLVED=14 patches over 7 listed locations (all RESOLVED)\nSWEEP_FIXES=2 (H49, H52)\nNEW_CLAIMS=0\nNEW_CITATIONS=0\nOVERCLAIM_REMAINING=0 (per 06 matrix)\nTHEORY_STATUS=PARTIAL\nSUBMISSION_READY=NO\n```")
open(os.path.join(OUT, '05_OUTER_SECTION_PRECISION_AUDIT.md'), 'w', encoding='utf-8').write('\n'.join(t05) + '\n')

# ------------------------------------------------------------------ 02 changelog
hc = V['hard_checks']
t02 = ["# 02 — V1.8.6a PRECISION HARMONIZATION + ERRATUM LINEAGE CLOSURE: change log\n",
       f"- **Base:** V1.8.6 `01_V1_8_6_THEORY_INTEGRATED_MANUSCRIPT.md` sha256 `{SHA_A}` (asserted before patching; file unchanged on disk).",
       f"- **Output:** `01_V1_8_6A_MANUSCRIPT.md` sha256 `{SHA_B}`.",
       f"- **Method:** `work/PH/patch_v186a.py` — {len(P)} exact old→new replacements, each asserted to match exactly once in V1.8.6 and once at apply time (no layered patches); `work/PH/verify_v186a.py` → `work/PH/verify_out_v186a.json` (ALL_HARD_CHECKS_PASS = {V['ALL_HARD_CHECKS_PASS']}, {sum(1 for v in hc.values() if v is True)}/{len(hc)}).",
       "- **Version character:** wording / precision / lineage closure. Not a new theory version, not an empirical version, not a model revision. Theory status stays PARTIAL; `SUBMISSION_READY = NO`. No git commit/push.",
       f"- **Changed V1.8.6 lines:** {len(V['changed_lines_v186'])} ({', '.join(map(str, V['changed_lines_v186']))}).\n",
       "## Hard checks (verify_v186a.py)\n", "| Check | Result |", "|---|---|"]
for k, v in hc.items():
    t02.append(f"| {k} | {'PASS' if v is True else 'FAIL'} |")
t02.append("\nNumeric tokens added (section numbers, file names, the S1e freeze date 2026-10-14, '16 個項目'): " + ", ".join(f"{k}×{v}" for k, v in V['numeric_added_doc'].items()) + ". Numeric tokens removed: none. Study 1 tokens and primary phrases: identical counts.\n")
t02.append("## Researcher-decision items closed in this pass\n")
t02.append("- **RD-1 (terminology)** — CLOSED. Construct = 企業決策機制 (組織決策安排 where organisational configuration is emphasised); S1e coder-facing = 企業決策過程; verbatim S1e sentence at §3.9.3 (4); §3.9.3, Table 3-14, Table 4-13, E6 and §3.9.6 synced; model terms (I1–I5, 介面活化, 資料／介面門檻) and technical interfaces kept. Full inventory in 03.")
t02.append("- **RD-2 (P2 remark)** — KEPT as in V1.8.6 (T07). Checks: P1–P5/P7/P8 bullets identical to V1.8.6 and P1, P3–P8 identical to 59a; P2 formal statement (text up to 「即 DL = 0。」) identical to 59a and V1.8.6; P2 remark identical to V1.8.6. Domain check: the remark is not part of P2's hypothesis or conclusion; it restates the converse-direction remark (misalignment necessary, not sufficient, for DL > 0) with the exact blockability condition of Lemma S (strictly more of at least one pooled resource than the enterprise-preferred plan), which narrows an informal sentence and changes no theorem's domain, hypothesis or conclusion; C.6 keeps the verbatim v2.2 remark and C.10.2 records the supersession. → no STOP.")
t02.append("  Strong provenance phrases replaced in the manuscript by 「P1–P8 的形式陳述與數學語意不變；說明性備註可能含非實質的精確化修訂。」: L5 「命題 P1–P8 的陳述」 (H02), L1159 「上列 P1–P8 的陳述不變」 (H33), L3125 「…P1–P8 與 51 的所有計算數值皆不變」 (H34); the V1.8.6a status line states it once more (H01). Remaining strong phrases: 0.")
t02.append("  Occurrences in the V1.8.6 reports (listed only; reports not edited): 02 l.67 (\"P2 formal statement unchanged\"; \"'P1–P8 text unchanged'\"), 02 l.119 (quotes L5 「命題 P1–P8 的陳述」), 02 l.264 (quotes 「上列 P1–P8 的陳述不變」), 02 l.746 (quotes 「…P1–P8 與 51 的所有計算數值皆不變」), 03 l.190 and l.237 (same quotes), 05 l.65 (\"P1–P8 statements are identical\"), 08 l.99 (\"P1–P8 and solver are unaffected\"), 09 l.37 (\"the P1–P8 scientific results are all unchanged\"), 11 l.24 (\"The P1–P8 statements are identical\"), 12 l.62 (\"Revert it if 'P1–P8 unchanged' is meant to include the remarks\"). Read with this pass, each means: P1–P8 formal statements and mathematical semantics remain unchanged; explanatory remarks may contain non-substantive precision edits.")
t02.append("- **RD-3 (42 erratum lineage)** — lineage record added: C.10.9 bullet (H50) and Appendix D row (H51) name `42a_CANONICAL_42_ERRATUM_V1_8_6.md` / `04_42A_ERRATUM.md`. 42 and 51 unchanged (0249e7b9… / 37f26a52…). Carrying it into a future canonical 42 stays a researcher decision.")
t02.append("- **RD-5 (outer precision)** — CLOSED; see 05.")
t02.append("- **Citations** — none added (reference list identical; citation-pattern counts identical).\n")
t02.append("## Summary table\n")
t02.append("| id | V1.8.6 line | section | category | source |\n|---|---|---|---|---|")
for p in P:
    t02.append(f"| {p['id']} | {p['line_src']} | {esc(p['section'])} | {esc(p['category'])} | {esc(p['source'])} |")
t02.append("\n## Patches (old → new)\n")
for p in P:
    t02.append(f"### {p['id']} — {p['section']} ({p['category']})\n")
    t02.append(f"- source: {p['source']}\n- V1.8.6 line: {p['line_src']}\n")
    t02.append("**old**\n\n```text\n" + p['old'] + "\n```\n\n**new**\n\n```text\n" + p['new'] + "\n```\n")
open(os.path.join(OUT, '02_V1_8_6A_CHANGELOG.md'), 'w', encoding='utf-8').write('\n'.join(t02) + '\n')
print('03 rows', len(rows), 'tally', tally)
print('written 02, 03, 05')
