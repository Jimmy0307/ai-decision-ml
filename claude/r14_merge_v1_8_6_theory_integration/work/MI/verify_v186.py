"""Verify v1.8.6 (01) vs v1.8.5a (59a).
Usage: python -I verify_v186.py <59a md> <01 md> <patches.json> <numeric_sources.json> <repo root> <out json>
Exit code 1 if any hard invariant fails."""
import sys, re, json, difflib, hashlib, os
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
A = open(sys.argv[1], encoding='utf-8').read()
B = open(sys.argv[2], encoding='utf-8').read()
PATCHES = json.load(open(sys.argv[3], encoding='utf-8'))
NUMSRC = json.load(open(sys.argv[4], encoding='utf-8'))
REPO = sys.argv[5]
OUT = sys.argv[6]
la, lb = A.split('\n'), B.split('\n')
res = {'sha256_59a': hashlib.sha256(A.encode()).hexdigest(), 'sha256_01': hashlib.sha256(B.encode()).hexdigest(),
       'line_count': [len(la), len(lb)], 'patch_count': len(PATCHES)}
hard = {}
hard['source_sha_expected'] = res['sha256_59a'] == "bf4379a4d492d762ef2dbdd293b41c574e475b7368d210b6a129274cd61381bd"
NEWTXT = '\n'.join(p['new'] for p in PATCHES)
OLDTXT = '\n'.join(p['old'] for p in PATCHES)

# ---- 1. diff confinement + reverse replay ----
sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
ca, ops = [], []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal':
        ca += list(range(i1 + 1, i2 + 1))
        ops.append([tag, i1 + 1, i2, j1 + 1, j2])
res['diff_opcodes'] = ops
patched = set()
for p in PATCHES:
    s = p['line_59a']
    patched |= set(range(s, s + p['old'].count('\n') + 1))
res['changed_lines_59a'] = sorted(set(ca))
hard['changed_lines_subset_of_patched_lines'] = set(ca) <= patched
Brev = B
for p in reversed(PATCHES):
    assert Brev.count(p['new']) == 1, p['id']
    Brev = Brev.replace(p['new'], p['old'], 1)
hard['reverse_replay_reproduces_59a'] = Brev == A


# ---- 2. math spans ----
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
hard['no_dollar_or_latex_in_patch_new_text'] = not any(re.search(r'\$|\\frac|\\sum|\\tag|\\begin', p['new'])
                                                        for p in PATCHES)
FA, FB = re.findall(r'```.*?```', A, flags=re.S), re.findall(r'```.*?```', B, flags=re.S)
hard['fenced_code_blocks_identical'] = FA == FB

# ---- 3. headings ----
ha, hb = [x for x in la if x.startswith('#')], [x for x in lb if x.startswith('#')]
it = iter(hb)
hard['existing_headings_preserved_in_order'] = all(any(h == x for x in it) for h in ha)
added_h = list((Counter(hb) - Counter(ha)).elements())
res['headings_count'] = [len(ha), len(hb)]
res['headings_added'] = added_h
EXPECTED_ADDED = ['### 3.9.6 M1–M4 的範圍、非冗餘性與充分性狀態（v1.8.6 新增）',
                  '### 4.9.1 合成驗證的三類區分與構造例（v1.8.6 新增；SIMULATED_ONLY）',
                  '### 5.8.10 理論結果的未證明部分（v1.8.6 新增）',
                  '### C.10 Q1 理論補充（v1.8.6 新增；非 v2.2 原文）'] + \
                 [x for x in hb if x.startswith('#### C.10.')]
hard['headings_added_exactly_expected'] = sorted(added_h) == sorted(EXPECTED_ADDED) and len(added_h) == 4 + 9
hard['no_heading_removed'] = not (Counter(ha) - Counter(hb))
CAP = re.compile(r'^\*\*(表|圖) ')
capa, capb = [x for x in la if CAP.match(x)], [x for x in lb if CAP.match(x)]
res['captions_added'] = [x for x in capb if x not in capa]
hard['captions_only_4_20D_added'] = res['captions_added'] == ['**表 4-20D：理論補充的構造例（SIMULATED_ONLY；構造例，非證明）**'] \
    and [x for x in capb if x in capa] == capa

# ---- 4. G rows / G->M / protected sections ----
GROW = re.compile(r'^\|\s*G(?:0[1-9]|1[0-6])\b')
ga, gb = [x for x in la if GROW.match(x)], [x for x in lb if GROW.match(x)]
res['G_table_rows'] = [len(ga), len(gb)]
hard['G_rows_identical_ordered'] = ga == gb
GM = re.compile(r'G\d\d\s*[→／/]\s*M\d')
hard['GM_arrow_tokens_identical'] = Counter(GM.findall(A)) == Counter(GM.findall(B))
hard['no_G17_or_new_G_code'] = len(re.findall(r'\bG(1[7-9]|[2-9]\d)\b', B)) == len(re.findall(r'\bG(1[7-9]|[2-9]\d)\b', A))
res['G01_G16_token_counts'] = [len(re.findall(r'G(?:0[1-9]|1[0-6])\b', A)), len(re.findall(r'G(?:0[1-9]|1[0-6])\b', B))]


def section(lines, s_pat, e_pat=r'^#'):
    s = next(i for i, x in enumerate(lines) if re.search(s_pat, x))
    e = next(i for i in range(s + 1, len(lines)) if re.search(e_pat, lines[i]))
    return lines[s:e]


for name, sp in [('3_9_1', r'^### 3\.9\.1'), ('3_9_2_tables_3_4_3_4A', r'^### 3\.9\.2'), ('3_9_3_V1_design', r'^### 3\.9\.3'),
                 ('3_9_4', r'^### 3\.9\.4'), ('3_9_5', r'^### 3\.9\.5'), ('3_11_x', r'^### 3\.11\.1'),
                 ('3_11_2', r'^### 3\.11\.2'), ('3_11_3', r'^### 3\.11\.3'), ('3_11_4', r'^### 3\.11\.4'),
                 ('3_12_1', r'^### 3\.12\.1'), ('3_12_2', r'^### 3\.12\.2'), ('3_12_3', r'^### 3\.12\.3'),
                 ('3_12_5', r'^### 3\.12\.5'), ('3_12_7', r'^### 3\.12\.7'), ('4_1_to_4_8', r'^## 4\.1 '),
                 ('4_10', r'^## 4\.10'), ('4_11', r'^## 4\.11')]:
    if name == '4_1_to_4_8':
        sa, sb = section(la, sp, r'^## 4\.9'), section(lb, sp, r'^## 4\.9')
    elif name in ('4_10',):
        sa, sb = section(la, sp, r'^## 4\.11'), section(lb, sp, r'^## 4\.11')
    elif name == '4_11':
        sa, sb = section(la, sp, r'^# 第五章'), section(lb, sp, r'^# 第五章')
    else:
        sa, sb = section(la, sp), section(lb, sp)
    hard['section_' + name + '_identical'] = sa == sb
    res['section_' + name + '_lines'] = len(sa)
for name, sp, ep in [('chapter2', r'^# 第二章', r'^# 第三章'), ('3_1_to_3_8', r'^## 3\.1 ', r'^## 3\.9 '),
                     ('5_1_to_5_5', r'^## 5\.1 ', r'^## 5\.6 '), ('5_8_1_to_5_8_9', r'^### 5\.8\.1 ', r'^## 5\.9 '),
                     ('references', r'^# 參考文獻', r'^# 附錄'), ('appendix_A_B', r'^## 附錄 A', r'^## 附錄 C'),
                     ('appendix_E_F_except_E51', r'^## 附錄 E', r'\Z')]:
    s = next(i for i, x in enumerate(la) if re.search(sp, x))
    e = next((i for i in range(s + 1, len(la)) if re.search(ep, la[i])), len(la))
    sa = la[s:e]
    s2 = next(i for i, x in enumerate(lb) if re.search(sp, x))
    if name == '5_8_1_to_5_8_9':
        e2 = next(i for i in range(s2 + 1, len(lb)) if re.search(r'^### 5\.8\.10', lb[i]))
    else:
        e2 = next((i for i in range(s2 + 1, len(lb)) if re.search(ep, lb[i])), len(lb))
    sb = lb[s2:e2]
    if name == 'appendix_E_F_except_E51':
        sb = [x for x in sb if not x.startswith('| E51 |')]
    hard['section_' + name + '_identical'] = sa == sb
    res['section_' + name + '_lines'] = [len(sa), len(sb)]
# 5.8.1-5.8.9 body: allowed none; note "九類" lives in 5.8 intro, outside this slice.

# Table 3-4 / 3-4A explicit
for cap in ['**表 3-4：G01–G16 的研究者轉譯結果**', '**表 3-4A：G01–G16 → M1–M4 的逐格追溯鏈（研究者裁決；人類構念效度驗證待完成）**']:
    ia, ib = la.index(cap), lb.index(cap)
    ta = la[ia:ia + 25]
    tb = lb[ib:ib + 25]
    hard['table_identical_' + cap[3:10]] = ta == tb

# Appendix C.1-C.9 verbatim
ca_s, ca_e = la.index('## 附錄 C　模型規格補充：帳本、命題與證明草稿'), la.index('## 附錄 D　研究文件、程式與資料樣板對照表')
cb_s = lb.index('## 附錄 C　模型規格補充：帳本、命題與證明草稿')
cb_e = lb.index('### C.10 Q1 理論補充（v1.8.6 新增；非 v2.2 原文）')
hard['appendix_C1_C9_verbatim'] = la[ca_s:ca_e] == lb[cb_s:cb_e]
res['appendix_C1_C9_lines'] = [ca_e - ca_s, cb_e - cb_s]

# ---- 5. P1-P8 statements ----
def pbullets(lines):
    s = lines.index('### 3.12.4 命題與治理價值分解')
    return {re.match(r'- \*\*(P\d)\*\*', x).group(1): x for x in lines[s:s + 15] if re.match(r'- \*\*P\d\*\*', x)}


pa, pb = pbullets(la), pbullets(lb)
res['P_bullets_found'] = [sorted(pa), sorted(pb)]
same = {k: pa[k] == pb[k] for k in pa}
res['P_bullet_identical'] = same
P2CUT = '即 DL = 0。'
hard['P1_P3_to_P8_bullets_identical'] = all(same[k] for k in pa if k != 'P2') and sorted(pa) == sorted(pb)
hard['P2_formal_statement_identical'] = pa['P2'].split(P2CUT)[0] == pb['P2'].split(P2CUT)[0]
res['P2_remark_change'] = {'old': pa['P2'].split(P2CUT)[1], 'new': pb['P2'].split(P2CUT)[1]}
hard['P2_only_remark_changed_by_T07'] = pa['P2'].split(P2CUT)[1].strip() == next(p['old'] for p in PATCHES if p['id'] == 'T07')
# Lemma E' and Lemma R statements in appendix untouched (inside C.1-C.9 check); C.6 P1-P8 included.

# ---- 6. Study 1 primary numbers unchanged ----
PRIMARY_PHRASES = ['保留 6,499 筆分析記錄', '其中 3,125 筆的人工智慧端與決策端皆完成分類', '形成 2,180 筆功能配對邊',
                   '辨識出 47 個', '32 個配對在四種分析下皆顯著且方向一致，其中 16 個高於期望、16 個低於期望',
                   '主要分析最後留下 3,125 筆兩端皆完成分類的證據記錄，涵蓋 783 篇文獻；去除同篇文獻內的重複配對後，形成 2,180 筆文獻層級邊',
                   '凍結的 32 組（16 過度、16 不足）仍為正式推論基準', '| L2 主要穩健集合 |', '| L1 主要零模型顯著 |',
                   '6,499 strict analytical records; 3,125 were fully mapped', 'yielding 2,180 document-level',
                   'identified 47 cells', 'comprising 16 enrichments and 16 depletions']
res['primary_phrase_counts'] = {p: [A.count(p), B.count(p)] for p in PRIMARY_PHRASES}
hard['study1_primary_phrases_unchanged'] = all(v[0] == v[1] and v[0] >= 1 for v in res['primary_phrase_counts'].values())
PRIM_TOK = ['6,499', '3,125', '783', '2,180', '2,118', '26,501', '.561', '.647', '68.3%']
res['study1_token_counts'] = {t: [len(re.findall(r'(?<![\d,])' + re.escape(t) + r'(?![\d,])', A)),
                                  len(re.findall(r'(?<![\d,])' + re.escape(t) + r'(?![\d,])', B))] for t in PRIM_TOK}
hard['study1_tokens_unchanged'] = all(v[0] == v[1] for v in res['study1_token_counts'].values())

# ---- 7. numeric traceability ----
NUM = re.compile(r'(?<![\w.])(?:\d+(?:[.,:/\-]\d+)*|\.\d+)')
na, nb = Counter(NUM.findall(A)), Counter(NUM.findall(B))
res['numeric_added_doc'] = dict(sorted((nb - na).items()))
res['numeric_removed_doc'] = dict(sorted((na - nb).items()))
per = {}
tot = Counter()
for p in PATCHES:
    a, b = Counter(NUM.findall(p['old'])), Counter(NUM.findall(p['new']))
    tot.update(b)
    tot.subtract(a)
    if a != b:
        per[p['id']] = {'added': dict(b - a), 'removed': dict(a - b)}
res['numeric_per_patch'] = per
doc = Counter(nb)
doc.subtract(na)
hard['numeric_patch_sum_matches_doc'] = {k: v for k, v in tot.items() if v} == {k: v for k, v in doc.items() if v}
res['numeric_added_unmapped'] = {k: v for k, v in res['numeric_added_doc'].items() if k not in NUMSRC}
hard['numeric_added_all_traceable'] = not res['numeric_added_unmapped']
res['numeric_added_sources'] = {k: NUMSRC[k] for k in res['numeric_added_doc'] if k in NUMSRC}
REMOVABLE = {'2026-10-14'}
res['numeric_removed_unexpected'] = {k: v for k, v in res['numeric_removed_doc'].items() if k not in REMOVABLE}
hard['numeric_removed_only_status_date'] = not res['numeric_removed_unexpected']

# ---- 8. citations: no new citation keys ----
CIT = [re.compile(r"[A-Z][A-Za-z'’\-]+(?: (?:&|and|與) [A-Z][A-Za-z'’\-]+)?(?: et al\.)?,\s*(?:19|20)\d\d[a-z]?"),
       re.compile(r"[A-Z][A-Za-z'’\-]+(?: 等人)?（(?:19|20)\d\d[a-z]?）"),
       re.compile(r"et al\."), re.compile(r"\b(?:19|20)\d\d[a-z]?\)"), re.compile(r"doi\.org|https?://")]
body_a, body_b = A.split('# 參考文獻')[0], B.split('# 參考文獻')[0]
res['citation_pattern_counts_main_text'] = [[len(c.findall(body_a)), len(c.findall(body_b))] for c in CIT]
hard['no_new_citation_keys_main_text'] = all(x == y for x, y in res['citation_pattern_counts_main_text'])
res['citation_pattern_counts_whole'] = [[len(c.findall(A)), len(c.findall(B))] for c in CIT]
hard['no_new_citation_keys_whole_document'] = all(x == y for x, y in res['citation_pattern_counts_whole'])
YEAR = re.compile(r'(?<!\d)(?:19|20)\d\d(?!\d)')
res['years_in_patch_new_text'] = sorted(set(YEAR.findall(NEWTXT)) - set(YEAR.findall(OLDTXT)))
hard['no_year_tokens_added_except_status_date'] = all(x == '2026' for x in res['years_in_patch_new_text'])
REFS_A = re.findall(r'^[^\n]+$', A.split('# 參考文獻')[1].split('# 附錄')[0], flags=re.M)
REFS_B = re.findall(r'^[^\n]+$', B.split('# 參考文獻')[1].split('# 附錄')[0], flags=re.M)
hard['reference_list_identical'] = REFS_A == REFS_B
VERIFY_TOKENS = ['類比', '前所未見', '引文查證', '委任', '資本預算', '選單依賴', 'TO VERIFY', 'TO_VERIFY', '待查證', 'Armstrong', 'Vickers', 'Holmstr', 'Matouschek', 'Laffont', 'Manski',
                 'Topkis', 'Milgrom', 'Chernoff', 'Stoye', 'Kouvelis', 'Averbakh', 'Loridan', 'Harris', 'Raviv', 'Howard',
                 'Raiffa', 'Jensen', 'Meckling', 'Braess']
res['unverified_anchor_names_in_new_text'] = {t: NEWTXT.count(t) for t in VERIFY_TOKENS if NEWTXT.count(t)}
hard['no_unverified_anchor_names_added'] = not res['unverified_anchor_names_in_new_text']

# ---- 9. forbidden phrases ----
FORBID = {'minimal sufficient (claim)': ['最小充分', 'minimal sufficien', 'MINIMAL_SUFFICIENCY', 'minimally sufficient'],
          'DL>0 iff': ['DL>0 iff', 'DL > 0 iff', 'DL > 0 ⇔', 'DL>0 ⇔', 'DL > 0 若且唯若', 'DL>0 若且唯若', 'DL 為正若且唯若', 'DL 為正的充要條件'],
          'governance always': ['governance always', '治理總是', '治理恆能', '治理永遠', '治理必然提高', '治理一定'],
          'generally non-monotone': ['generally non-monotone', '一般而言非單調', '普遍非單調', '一般非單調', 'Model C 一般'],
          'enterprise evidence for synthetic': ['構造例證明', '合成結果顯示企業', '企業證據顯示', '實證顯示', 'W5 證明', '證明了企業'],
          'FULLY_VALIDATED': ['FULLY_VALIDATED', 'fully validated']}
res['forbidden_hits_01'] = {k: {t: B.count(t) for t in v if B.count(t)} for k, v in FORBID.items()}
res['forbidden_hits_59a'] = {k: {t: A.count(t) for t in v if A.count(t)} for k, v in FORBID.items()}
res['forbidden_hits_patch_new_text'] = {k: {t: NEWTXT.count(t) for t in v if NEWTXT.count(t)} for k, v in FORBID.items()}
hard['no_forbidden_phrases_in_01'] = not any(res['forbidden_hits_01'].values())
# 367/400 never primary: every sentence containing it must carry sensitivity labelling and not "主要報告"
sent = re.split(r'(?<=[。；])', B)
s367 = [s for s in sent if '367/400' in s]
res['sentences_367_400'] = s367
hard['W5_WIDE_367_only_as_sensitivity'] = len(s367) >= 2 and all(('敏感度' in s) and ('主要報告' not in s) for s in s367)
s162 = [s for s in sent if '162/400' in s]
res['sentences_162_400'] = s162
hard['W5_162_reported_as_primary'] = len(s162) >= 2 and all(('主要' in s) for s in s162)
res['sentences_with_充要_in_patch_text'] = [s for s in re.split(r'(?<=[。；])', NEWTXT) if '充要' in s]
hard['every_充要_in_new_text_scoped_or_negated'] = all(any(k in s for k in ('唯一首佳', '不能構成', '沒有', '未證明', '不包含', '不宣稱', 'NOT_PROVEN', '只有', '不是'))
                                                     for s in res['sentences_with_充要_in_patch_text'])
res['sentences_iff_positive_in_new_text'] = [s for s in re.split(r'(?<=[。；])', NEWTXT) if '若且唯若' in s and '為正' in s]
hard['every_positive_iff_scoped_to_unique_first_best'] = all(('唯一首佳' in s or 'H0' in s) for s in res['sentences_iff_positive_in_new_text'])
s491 = B.split('### 4.9.1')[1].split('## 4.10')[0]
hard['4_9_1_footnote_present'] = '這些合成案例只建立計算一致性、形式存在性或反例，不是企業實證證據。' in s491
hard['4_9_1_ABC_present'] = all(x in s491 for x in ('**A. 實作驗證', '**B. 形式性質回歸', '**C. 構造例與反例'))
hard['4_9_1_W1_W7_rows'] = all(('| W%d |' % i) in s491 for i in range(1, 8))
hard['governance_sentence_present'] = '在特定的雙層錯位與可分離性條件下，治理可能具有正的篩選價值' in B
hard['M1_M4_scope_sentence_TA_MAJOR1'] = '以決策對象判準界定、且在 T1–T4 型別定義下對 v2.2 屬性結構非冗餘的 mechanism decomposition（操作上的可區辨性由 V1 檢驗，尚未執行）' in B and '操作上可區辨且' not in B
hard['synthetic_analytic_counterexample_label'] = B.count('SYNTHETIC ANALYTIC COUNTEREXAMPLE') >= 3
hard['W_IA_NDV_not_in_chapter4'] = 'W_IA_NDV' not in B.split('# 第四章')[1].split('# 第五章')[0]

# ---- 10. status line, V1 term ----
hard['status_line_L5_v186'] = 'v1.8.6 THEORY INTEGRATION CANDIDATE' in lb[4] and 'SUBMISSION_READY = NO' in lb[4]
res['SUBMISSION_READY_NO_counts'] = [A.count('SUBMISSION_READY = NO'), B.count('SUBMISSION_READY = NO')]
hard['SUBMISSION_READY_NO_kept'] = B.count('SUBMISSION_READY = NO') >= A.count('SUBMISSION_READY = NO')
v193 = '\n'.join(section(lb, r'^### 3\.9\.3'))
res['V1_3_9_3_term_counts'] = {'企業決策介面': v193.count('企業決策介面'), '企業決策過程': v193.count('企業決策過程')}
res['V1_term_mismatch_with_S1e'] = v193.count('企業決策介面') > 0 and v193.count('企業決策過程') == 0
res['erratum_C10_9_present'] = '#### C.10.9 勘誤：Lemma E′ 悲觀情形的證明用語（只改用語）' in B
hard['erratum_present_and_C2_verbatim'] = res['erratum_C10_9_present'] and \
    '*證明：* 任取 envelope `e_u`' in B and 'Pessimistic leader：取任一 `x ∈ T`' in B

# ---- 11. canonical files and coder packets untouched (read-only hashing) ----
def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


canon = {'42': (os.path.join(REPO, '42_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md'), '0249e7b9'),
         '51': (os.path.join(REPO, '51_enterprise_portfolio_solver_v2_2.py'), '37f26a52')}
res['canonical_hashes'] = {k: sha(v[0]) for k, v in canon.items()}
hard['canonical_42_51_unchanged'] = all(res['canonical_hashes'][k].startswith(v[1]) for k, v in canon.items())
PK = r'C:\NTUST_PAPER\outputs\00_CURRENT\03_V1_HUMAN_VALIDATION\04_CODER_PACKETS_S1E_ZH_TW_TEACHER_APPROVED_READY_TO_DISTRIBUTE'
pk = {'CODER_1_ZH_TW.xlsx': 'cbbbaa0a', 'CODER_2_ZH_TW.xlsx': '5925ead5', 'CODER_3_ZH_TW.xlsx': '50d8c818'}
res['S1e_packet_hashes'] = {k: sha(os.path.join(PK, k)) for k in pk}
hard['S1e_packets_unchanged'] = all(res['S1e_packet_hashes'][k].startswith(v) for k, v in pk.items())

res['hard_checks'] = hard
res['ALL_HARD_CHECKS_PASS'] = all(v is True for v in hard.values())
json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({'hard_checks': hard, 'ALL': res['ALL_HARD_CHECKS_PASS'], 'unmapped': res['numeric_added_unmapped'],
                  'removed_unexpected': res['numeric_removed_unexpected'], 'headings_added': added_h,
                  'forbidden_01': res['forbidden_hits_01'], 'cit': res['citation_pattern_counts_main_text'],
                  'iffs': res['sentences_with_充要_in_patch_text'], 'years': res['years_in_patch_new_text'],
                  'anchors': res['unverified_anchor_names_in_new_text'], 'V1term': res['V1_3_9_3_term_counts']},
                 ensure_ascii=False, indent=0))
sys.exit(0 if res['ALL_HARD_CHECKS_PASS'] else 1)
