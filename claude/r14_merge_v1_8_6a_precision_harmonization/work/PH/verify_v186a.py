"""Verify V1.8.6a (OUT 01) against V1.8.6 (01) and V1.8.5a (59a).
Usage: python -I verify_v186a.py <V1.8.6 01 md> <V1.8.6a 01 md> <patches json> <59a md> <repo root> <out json>
Exit code 1 if any hard invariant fails."""
import sys, re, json, difflib, hashlib, os
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
A = open(sys.argv[1], encoding='utf-8').read()
B = open(sys.argv[2], encoding='utf-8').read()
PATCHES = json.load(open(sys.argv[3], encoding='utf-8'))
C59 = open(sys.argv[4], encoding='utf-8').read()
REPO, OUT = sys.argv[5], sys.argv[6]
la, lb, l59 = A.split('\n'), B.split('\n'), C59.split('\n')
sha = lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()
res = {'sha256_v186': sha(A), 'sha256_v186a': sha(B), 'line_count': [len(la), len(lb)], 'patch_count': len(PATCHES)}
hard = {}
hard['source_sha_expected'] = res['sha256_v186'] == "94d41d5682818953912784d0e870d58d1e4c418e7261b619d5c73485dfee82f4"
NEWTXT = '\n'.join(p['new'] for p in PATCHES)
OLDTXT = '\n'.join(p['old'] for p in PATCHES)

# ---- 1. reverse replay + diff confinement ----
Brev = B
for p in reversed(PATCHES):
    assert Brev.count(p['new']) == 1, p['id']
    Brev = Brev.replace(p['new'], p['old'], 1)
hard['reverse_replay_reproduces_v186'] = Brev == A
sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
changed = set()
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal':
        changed |= set(range(i1 + 1, i2 + 1))
patched = set()
for p in PATCHES:
    s = p['line_src']
    patched |= set(range(s, s + p['old'].count('\n') + 1))
res['changed_lines_v186'] = sorted(changed)
hard['changed_lines_subset_of_patched_lines'] = changed <= patched
hard['each_old_once_in_v186'] = all(A.count(p['old']) == 1 for p in PATCHES)


# ---- 2. math ----
def math_spans(t):
    blocks = re.findall(r'\$\$.*?\$\$', t, flags=re.S)
    t2 = re.sub(r'\$\$.*?\$\$', '', t, flags=re.S)
    return {'$$': blocks, '$inline': re.findall(r'(?<!\\)\$[^$\n]+?\$', t2),
            '\\[\\]': re.findall(r'\\\[.*?\\\]', t, flags=re.S),
            'begin_env': re.findall(r'\\begin\{.*?\\end\{[^}]*\}', t, flags=re.S)}


ma, mb = math_spans(A), math_spans(B)
res['math_counts'] = {k: [len(ma[k]), len(mb[k])] for k in ma}
hard['math_spans_identical_ordered'] = all(ma[k] == mb[k] for k in ma)
TAG = re.compile(r'\\tag\{[^}]*\}')
hard['equation_tags_identical'] = TAG.findall(A) == TAG.findall(B)
hard['no_dollar_or_latex_in_new_text'] = not any(re.search(r'\$|\\frac|\\sum|\\tag|\\begin', p['new']) for p in PATCHES)
hard['fenced_code_blocks_identical'] = re.findall(r'```.*?```', A, flags=re.S) == re.findall(r'```.*?```', B, flags=re.S)

# ---- 3. headings ----
ha, hb = [x for x in la if x.startswith('#')], [x for x in lb if x.startswith('#')]
EXPECTED_HEAD_CHANGE = {'## 5.5 從低整合接口到企業決策介面': '## 5.5 從低整合接口到企業決策機制'}
hard['headings_same_count'] = len(ha) == len(hb)
hard['headings_only_expected_changes'] = all((x == y) or (EXPECTED_HEAD_CHANGE.get(x) == y) for x, y in zip(ha, hb))
res['headings_changed'] = [[x, y] for x, y in zip(ha, hb) if x != y]

# ---- 4. G rows, tables 3-4 / 3-4A ----
GROW = re.compile(r'^\|\s*G(?:0[1-9]|1[0-6])\b')
ga, gb = [x for x in la if GROW.match(x)], [x for x in lb if GROW.match(x)]
res['G_table_rows'] = [len(ga), len(gb)]
hard['G_rows_identical_ordered'] = ga == gb
GM = re.compile(r'G\d\d\s*[→／/]\s*M\d')
hard['GM_arrow_tokens_identical'] = Counter(GM.findall(A)) == Counter(GM.findall(B))
hard['no_new_G_code'] = len(re.findall(r'\bG(1[7-9]|[2-9]\d)\b', B)) == len(re.findall(r'\bG(1[7-9]|[2-9]\d)\b', A))


def table_block(lines, cap):
    i = lines.index(cap)
    j = i + 1
    while j < len(lines) and not lines[j].startswith('|'):
        j += 1
    k = j
    while k < len(lines) and lines[k].startswith('|'):
        k += 1
    note = k + 1 if k + 1 < len(lines) and lines[k + 1].startswith('表註') else k
    return lines[i:note + 1]


for cap in ['**表 3-4：G01–G16 的研究者轉譯結果**', '**表 3-4A：G01–G16 → M1–M4 的逐格追溯鏈（研究者裁決；人類構念效度驗證待完成）**']:
    ta, tb = table_block(la, cap), table_block(lb, cap)
    hard['table_rows_and_note_identical_' + cap[3:10]] = ta == tb
    ia, ib = la.index(cap), lb.index(cap)
    hard['table_v186_heuristic_window_identical_' + cap[3:10]] = la[ia:ia + 25] == lb[ib:ib + 25]
    hard['table_identical_to_59a_' + cap[3:10]] = table_block(l59, cap) == tb

# Appendix C.1-C.9 verbatim vs V1.8.6 and 59a
cs = '## 附錄 C　模型規格補充：帳本、命題與證明草稿'
ce = '### C.10 Q1 理論補充（v1.8.6 新增；非 v2.2 原文）'
hard['appendix_C1_C9_identical_to_v186'] = la[la.index(cs):la.index(ce)] == lb[lb.index(cs):lb.index(ce)]
hard['appendix_C1_C9_identical_to_59a'] = l59[l59.index(cs):l59.index('## 附錄 D　研究文件、程式與資料樣板對照表')] == lb[lb.index(cs):lb.index(ce)]


# ---- 5. P1-P8 ----
def pbullets(lines):
    s = lines.index('### 3.12.4 命題與治理價值分解')
    return {re.match(r'- \*\*(P\d)\*\*', x).group(1): x for x in lines[s:s + 15] if re.match(r'- \*\*P\d\*\*', x)}


pa, pb, p59 = pbullets(la), pbullets(lb), pbullets(l59)
res['P_bullets_found'] = sorted(pb)
hard['P1_P8_bullets_identical_to_v186'] = pa == pb and sorted(pb) == ['P1', 'P2', 'P3', 'P4', 'P5', 'P7', 'P8'] and '**P6**' in pb['P5']  # P6 shares the P5 bullet
CUT = '即 DL = 0。'
hard['P2_formal_statement_identical_to_59a_and_v186'] = pb['P2'].split(CUT)[0] == p59['P2'].split(CUT)[0] == pa['P2'].split(CUT)[0]
hard['P1_P3_P8_identical_to_59a'] = all(pb[k] == p59[k] for k in pb if k != 'P2')
res['P2_remark_v186_kept'] = pb['P2'].split(CUT)[1]
hard['P2_remark_kept_from_v186'] = pb['P2'].split(CUT)[1] == pa['P2'].split(CUT)[1]
# C.6 verbatim propositions (P1-P8 in Appendix C.6) inside C.1-C.9 check above.
STRONG = ['P1–P8 的陳述不變', 'P1–P8 不變', '命題 P1–P8 的陳述', 'P1–P8 與 51 的所有計算數值皆不變', 'P1-P8 unchanged', 'P1–P8 unchanged']
res['strong_provenance_phrase_hits_v186'] = {s: A.count(s) for s in STRONG if A.count(s)}
res['strong_provenance_phrase_hits_v186a'] = {s: B.count(s) for s in STRONG if B.count(s)}
hard['no_strong_P1_P8_provenance_phrase'] = not res['strong_provenance_phrase_hits_v186a']
STD = 'P1–P8 的形式陳述與數學語意不變；說明性備註可能含非實質的精確化修訂'
res['standard_phrase_count'] = B.count(STD)
hard['standard_phrase_present_ge_4'] = B.count(STD) >= 4

# ---- 6. Study 1 numbers ----
PRIMARY_PHRASES = ['保留 6,499 筆分析記錄', '其中 3,125 筆的人工智慧端與決策端皆完成分類', '形成 2,180 筆功能配對邊',
                   '辨識出 47 個', '32 個配對在四種分析下皆顯著且方向一致，其中 16 個高於期望、16 個低於期望',
                   '主要分析最後留下 3,125 筆兩端皆完成分類的證據記錄，涵蓋 783 篇文獻；去除同篇文獻內的重複配對後，形成 2,180 筆文獻層級邊',
                   '凍結的 32 組（16 過度、16 不足）仍為正式推論基準', '| L2 主要穩健集合 |', '| L1 主要零模型顯著 |',
                   '6,499 strict analytical records; 3,125 were fully mapped', 'yielding 2,180 document-level',
                   'identified 47 cells', 'comprising 16 enrichments and 16 depletions']
res['primary_phrase_counts'] = {p: [A.count(p), B.count(p)] for p in PRIMARY_PHRASES}
hard['study1_primary_phrases_unchanged'] = all(v[0] == v[1] and v[0] >= 1 for v in res['primary_phrase_counts'].values())
PRIM_TOK = ['6,499', '3,125', '783', '2,180', '2,118', '26,501', '.561', '.647', '68.3%', '1,729', '1,104', '47', '32', '29', '0.12', '44.93', '162/400', '367/400']
cnt = lambda t, s: len(re.findall(r'(?<![\d,./])' + re.escape(t) + r'(?![\d,]|\.\d)', s))
res['study1_token_counts'] = {t: [cnt(t, A), cnt(t, B)] for t in PRIM_TOK}
hard['study1_tokens_unchanged'] = all(v[0] == v[1] for v in res['study1_token_counts'].values())
NUM = re.compile(r'(?<![\w.])(?:\d+(?:[.,:/\-]\d+)*|\.\d+)')
res['numeric_added_doc'] = dict(sorted((Counter(NUM.findall(B)) - Counter(NUM.findall(A))).items()))
res['numeric_removed_doc'] = dict(sorted((Counter(NUM.findall(A)) - Counter(NUM.findall(B))).items()))
hard['no_numeric_token_removed'] = not res['numeric_removed_doc']

# ---- 7. citations ----
CIT = [re.compile(r"[A-Z][A-Za-z'’\-]+(?: (?:&|and|與) [A-Z][A-Za-z'’\-]+)?(?: et al\.)?,\s*(?:19|20)\d\d[a-z]?"),
       re.compile(r"[A-Z][A-Za-z'’\-]+(?: 等人)?（(?:19|20)\d\d[a-z]?）"),
       re.compile(r"et al\."), re.compile(r"\b(?:19|20)\d\d[a-z]?\)"), re.compile(r"doi\.org|https?://")]
res['citation_pattern_counts_whole'] = [[len(c.findall(A)), len(c.findall(B))] for c in CIT]
hard['no_new_citation_keys'] = all(x == y for x, y in res['citation_pattern_counts_whole'])
YEAR = re.compile(r'(?<!\d)(?:19|20)\d\d(?!\d)')
res['years_in_new_text_not_in_old'] = sorted(set(YEAR.findall(NEWTXT)) - set(YEAR.findall(OLDTXT)))
hard['no_year_tokens_added_except_2026'] = all(x == '2026' for x in res['years_in_new_text_not_in_old'])
refs = lambda t: t.split('# 參考文獻')[1].split('# 附錄')[0]
hard['reference_list_identical'] = refs(A) == refs(B)
ANCH = ['類比', '前所未見', 'TO VERIFY', 'TO_VERIFY', '待查證', 'Armstrong', 'Vickers', 'Holmstr', 'Matouschek', 'Laffont', 'Manski',
        'Topkis', 'Milgrom', 'Chernoff', 'Stoye', 'Kouvelis', 'Averbakh', 'Loridan', 'Harris', 'Raviv', 'Howard', 'Raiffa', 'Jensen', 'Meckling']
res['unverified_anchor_names_in_new_text'] = {t: NEWTXT.count(t) for t in ANCH if NEWTXT.count(t)}
hard['no_unverified_anchor_names_added'] = not res['unverified_anchor_names_in_new_text']

# ---- 8. forbidden phrases ----
FORBID = ['最小充分', 'minimal sufficien', 'minimally sufficient', 'DL>0 iff', 'DL > 0 iff', 'DL > 0 若且唯若', 'DL 為正若且唯若',
          'DL 為正的充要條件', 'governance always', '治理總是', '治理恆能', '治理必然提高', '一般而言非單調', '普遍非單調',
          '構造例證明', '實證顯示', 'W5 證明', 'FULLY_VALIDATED', 'fully validated', '操作上可區辨且', '完備的機制分類', 'complete taxonomy']
res['forbidden_hits'] = {t: B.count(t) for t in FORBID if B.count(t)}
hard['no_forbidden_phrases'] = not res['forbidden_hits']
sent = re.split(r'(?<=[。；])', B)
s367 = [s for s in sent if '367/400' in s]
hard['W5_WIDE_367_only_as_sensitivity'] = len(s367) >= 2 and all('敏感度' in s and '主要報告' not in s for s in s367)
s162 = [s for s in sent if '162/400' in s]
hard['W5_162_reported_as_primary'] = len(s162) >= 2 and all('主要' in s for s in s162)
hard['M1_M4_bounded_phrasing_kept'] = '操作上的可區辨性由 V1 檢驗，尚未執行' in B and '其操作上的可區辨性待 V1 人類編碼檢驗' in B

# ---- 9. terminology ----
VERB = '為降低獨立編碼者的理解負擔，S1e 問卷採用『企業決策過程』作為 coder-facing wording；其所對應的理論構念仍為本文所稱之企業決策機制／組織決策安排，並不構成另一個不同構念。'
hard['verbatim_S1e_sentence_once'] = B.count(VERB) == 1
s393 = '\n'.join(lb[lb.index('### 3.9.3 V1 獨立盲編設計'):lb.index('### 3.9.4 AI 盲編 pilot 與爭議格')])
hard['verbatim_sentence_in_3_9_3_item4'] = VERB in s393 and s393.find(VERB) > s393.find('(4) **編碼工具（Q1–Q5）。**') > 0
res['3_9_3_terms'] = {k: s393.count(k) for k in ('企業決策介面', '企業決策過程', '企業決策機制', '介面')}
hard['3_9_3_no_enterprise_decision_interface'] = s393.count('企業決策介面') == 0 and s393.count('企業決策過程') >= 3
idx_first_S1e = B.find('S1e')
res['first_S1e_mention_line'] = B[:idx_first_S1e].count('\n') + 1
hard['first_body_S1e_mention_is_verbatim_sentence'] = B.find('S1e', B.find('# 第一章')) == B.find(VERB) + VERB.find('S1e')
TERM = ['企業決策介面', '企業決策過程', '企業決策機制', '組織決策安排', '介面']
res['term_counts'] = {k: [A.count(k), B.count(k)] for k in TERM}
hard['enterprise_decision_interface_kept_5'] = B.count('企業決策介面') == 5
TECH = ['使用者介面', 'API', '系統串接介面', '介面活化', '資料／介面門檻', '共用介面', '介面 I1', '平台介面', 'platform interfaces',
        'interface activation', 'Interface activation', '外部評估介面', '技術—治理介面', '轉譯介面', '未獲獨立支持的介面']
res['technical_or_model_interface_counts'] = {k: [A.count(k), B.count(k)] for k in TECH}
hard['technical_model_interface_terms_not_reduced'] = all(v[1] >= v[0] for v in res['technical_or_model_interface_counts'].values())
hard['table_3_4A_header_kept'] = '| 企業決策介面 | 機制（主／次；狀態） |' in B

# ---- 10. version / lineage ----
hard['status_line_V186a'] = all(x in lb[4] for x in ('V1.8.6a PRECISION HARMONIZATION + ERRATUM LINEAGE CLOSURE', 'SUBMISSION_READY = NO',
                                                     'THEORY PARTIAL', '不是新的理論版本', '不是實證版本', '不是模型修訂'))
hard['SUBMISSION_READY_NO_count_kept'] = B.count('SUBMISSION_READY = NO') >= A.count('SUBMISSION_READY = NO')
hard['appendix_D_row_V186a'] = '| v1.8.6a／01–05 |' in B and '`04_42A_ERRATUM.md`' in B and '`42a_CANONICAL_42_ERRATUM_V1_8_6.md`' in B
c109 = B.split('#### C.10.9')[1].split('## 附錄 D')[0]
hard['C10_9_lineage_record'] = '42a_CANONICAL_42_ERRATUM_V1_8_6.md' in c109 and '04_42A_ERRATUM.md' in c109

# ---- 11. read-only artefacts ----
def fsha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


canon = {'42': (os.path.join(REPO, '42_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md'), '0249e7b9'),
         '51': (os.path.join(REPO, '51_enterprise_portfolio_solver_v2_2.py'), '37f26a52')}
res['canonical_hashes'] = {k: fsha(v[0]) for k, v in canon.items()}
hard['canonical_42_51_unchanged'] = all(res['canonical_hashes'][k].startswith(v[1]) for k, v in canon.items())
PK = r'C:\NTUST_PAPER\outputs\00_CURRENT\03_V1_HUMAN_VALIDATION\04_CODER_PACKETS_S1E_ZH_TW_TEACHER_APPROVED_READY_TO_DISTRIBUTE'
pk = {'CODER_1_ZH_TW.xlsx': 'cbbbaa0a9741426a051168439ae4f8ce2d212c2878ed1990e444a9b1e2655a29',
      'CODER_2_ZH_TW.xlsx': '5925ead55daa2c9db99a084c4cce48441bd6a3c2994371b1e170562bac0e3f38',
      'CODER_3_ZH_TW.xlsx': '50d8c818950a33ea4644fe038c8f89e9cde70990afd0d70dc194012c620084a9'}
res['S1e_packet_hashes'] = {k: fsha(os.path.join(PK, k)) for k in pk}
hard['S1e_packets_unchanged_full_sha'] = all(res['S1e_packet_hashes'][k] == v for k, v in pk.items())
V186_01 = os.path.join(REPO, 'claude', 'r14_merge_v1_8_6_theory_integration', '01_V1_8_6_THEORY_INTEGRATED_MANUSCRIPT.md')
hard['v186_source_file_unchanged_on_disk'] = fsha(V186_01) == "94d41d5682818953912784d0e870d58d1e4c418e7261b619d5c73485dfee82f4"

res['hard_checks'] = hard
res['ALL_HARD_CHECKS_PASS'] = all(v is True for v in hard.values())
json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({'hard_checks': hard, 'ALL': res['ALL_HARD_CHECKS_PASS'], 'n_hard': len(hard),
                  'n_pass': sum(1 for v in hard.values() if v is True), 'term_counts': res['term_counts'],
                  'numeric_added': res['numeric_added_doc'], 'numeric_removed': res['numeric_removed_doc'],
                  'years_added': res['years_in_new_text_not_in_old'], 'headings_changed': res['headings_changed'],
                  'strong_v186': res['strong_provenance_phrase_hits_v186'], 'std_count': res['standard_phrase_count'],
                  'first_S1e_line': res['first_S1e_mention_line'], 'tech': res['technical_or_model_interface_counts']},
                 ensure_ascii=False, indent=0))
sys.exit(0 if res['ALL_HARD_CHECKS_PASS'] else 1)
