"""Verify v1.8.5 vs v1.8.3. Usage: python -I verify_v185.py <v1.8.3 md> <v1.8.5 md> <patches.json> <out json>
Exit code 1 if any hard invariant fails."""
import sys, re, json, difflib, hashlib
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
A = open(sys.argv[1], encoding='utf-8').read()
B = open(sys.argv[2], encoding='utf-8').read()
PATCHES = json.load(open(sys.argv[3], encoding='utf-8'))
la, lb = A.split('\n'), B.split('\n')
res = {'sha256': [hashlib.sha256(A.encode()).hexdigest(), hashlib.sha256(B.encode()).hexdigest()],
       'line_count': [len(la), len(lb)], 'patch_count': len(PATCHES)}
hard = {}
hard['source_sha_expected'] = res['sha256'][0] == "0da8cec1521dbeff900ffa1fa9a1de0a31b0cdfa34b82c03531eba2111d7f740"

# ---- 1. diff confinement ----
sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
ca, cb, ops = [], [], []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal':
        ca += list(range(i1 + 1, i2 + 1))
        cb += list(range(j1 + 1, j2 + 1))
        ops.append([tag, i1 + 1, i2, j1 + 1, j2])
res['changed_lines_v183'], res['changed_lines_v185'], res['diff_opcodes'] = ca, cb, ops
res['patched_lines_v183'] = sorted({p['v183_line'] for p in PATCHES})
hard['changed_lines_subset_of_patched_lines'] = set(ca) <= set(res['patched_lines_v183'])
# replay: reversing every patch on B must give A exactly
Brev = B
for p in reversed(PATCHES):
    assert Brev.count(p['new']) == 1, p['id']
    Brev = Brev.replace(p['new'], p['old'], 1)
hard['reverse_replay_reproduces_v183'] = Brev == A


# ---- 2. math ----
def math_spans(t):
    blocks = re.findall(r'\$\$.*?\$\$', t, flags=re.S)
    t2 = re.sub(r'\$\$.*?\$\$', '', t, flags=re.S)
    return {'$$': blocks, '$inline': re.findall(r'(?<!\\)\$[^$\n]+?\$', t2),
            '\\[\\]': re.findall(r'\\\[.*?\\\]', t, flags=re.S),
            'begin_env': re.findall(r'\\begin\{.*?\\end\{[^}]*\}', t, flags=re.S)}


ma, mb = math_spans(A), math_spans(B)
res['math_counts'] = {k: [len(ma[k]), len(mb[k])] for k in ma}
hard['math_identical_ordered'] = all(ma[k] == mb[k] for k in ma)
TAG = re.compile(r'\\tag\{[^}]*\}')
hard['equation_tags_identical'] = TAG.findall(A) == TAG.findall(B)
MATHMARK = re.compile(r'\$|\\\(|\\\[|\\begin|\\frac|\\sum|\\tag')
hard['no_math_markers_in_patch_text'] = not [p['id'] for p in PATCHES if MATHMARK.search(p['old'] + p['new'])]
FA, FB = re.findall(r'```.*?```', A, flags=re.S), re.findall(r'```.*?```', B, flags=re.S)
res['fenced_patches'] = [p['id'] for p in PATCHES if any(p['old'] in x for x in FA)]
B_rev = B
for p in PATCHES:
    if p['id'] in res['fenced_patches']:
        B_rev = B_rev.replace(p['new'], p['old'], 1)
hard['fenced_blocks_identical_except_listed_status_patches'] = re.findall(r'```.*?```', B_rev, flags=re.S) == FA and len(FA) == len(FB)

# ---- 3. headings / captions ----
ha, hb = [x for x in la if x.startswith('#')], [x for x in lb if x.startswith('#')]
res['headings'] = [len(ha), len(hb)]
hard['headings_identical_in_order_none_added'] = ha == hb
CAP = re.compile(r'^\*\*(表|圖) ')
capa, capb = [x for x in la if CAP.match(x)], [x for x in lb if CAP.match(x)]
res['captions_added'] = [x for x in capb if x not in capa]
res['captions_removed'] = [x for x in capa if x not in capb]
hard['captions_only_4_9B_added'] = (res['captions_removed'] == [] and
                                     res['captions_added'] == ['**表 4-9B：主要分析（凍結基準）與稽核標籤替代敏感度分析的比較**']
                                     and [x for x in capb if x in capa] == capa)

# ---- 4. G rows / G->M / protected sections ----
GROW = re.compile(r'^\|\s*G(?:0[1-9]|1[0-6])\b')
ga, gb = [x for x in la if GROW.match(x)], [x for x in lb if GROW.match(x)]
res['G_table_rows'] = [len(ga), len(gb)]
hard['G_rows_identical_ordered'] = ga == gb
G = re.compile(r'G(?:0[1-9]|1[0-6])\b')
res['G_token_counts_v183_v185'] = [len(G.findall(A)), len(G.findall(B))]
res['G_tokens_added_by_patch'] = {p['id']: len(G.findall(p['new'])) - len(G.findall(p['old'])) for p in PATCHES
                                  if len(G.findall(p['new'])) != len(G.findall(p['old']))}
GM = re.compile(r'G\d\d\s*[→／/]\s*M\d')
hard['GM_arrow_tokens_identical'] = Counter(GM.findall(A)) == Counter(GM.findall(B))
hard['no_G17_or_new_G_code'] = not re.search(r'\bG(1[7-9]|[2-9]\d)\b', B.replace(A, '')) and \
    len(re.findall(r'\bG1[7-9]\b', B)) == len(re.findall(r'\bG1[7-9]\b', A))


def section(lines, s_pat, e_pat):
    s = next(i for i, x in enumerate(lines) if re.search(s_pat, x))
    e = next(i for i in range(s + 1, len(lines)) if re.search(e_pat, lines[i]))
    return lines[s:e]


for name, sp, ep in [('3_9_1', r'^### 3\.9\.1', r'^### 3\.9\.2'),
                     ('3_9_2_tables_3_4_3_4A', r'^### 3\.9\.2', r'^### 3\.9\.3'),
                     ('3_9_3_V1_design', r'^### 3\.9\.3', r'^### 3\.9\.4'),
                     ('3_9_4', r'^### 3\.9\.4', r'^### 3\.9\.5'),
                     ('3_9_5', r'^### 3\.9\.5', r'^## 3\.10'),
                     ('3_10_to_3_14_enterprise', r'^## 3\.10', r'^# 第四章'),
                     ('4_1_to_4_4_primary_results', r'^## 4\.1 ', r'^## 4\.5'),
                     ('4_5_1_to_4_5_4', r'^### 4\.5\.1', r'^### 4\.5\.5'),
                     ('4_6_G_handoff', r'^## 4\.6', r'^## 4\.7'),
                     ('4_7_to_4_10_V1_enterprise', r'^## 4\.7', r'^## 4\.11'),
                     ('appendix_C_math', r'^## 附錄 C', r'^## 附錄 D')]:
    sa, sb = section(la, sp, ep), section(lb, sp, ep)
    hard['section_' + name + '_identical'] = sa == sb
    res['section_' + name + '_lines'] = len(sa)

for kw in ['VCP', 'VSC', 'DL', 'NEV', 'Enterprise', 'SIMULATED_ONLY', 'EMPIRICAL RESULT PENDING', 'SUBMISSION_READY',
           'UNIDENTIFIED', 'M1', 'M2', 'M3', 'M4', 'M5', 'REAL EVIDENCE']:
    res['count_' + kw] = [len(re.findall(r'\b' + re.escape(kw) + r'\b', A)), len(re.findall(r'\b' + re.escape(kw) + r'\b', B))]
    hard['count_unchanged_' + kw] = res['count_' + kw][0] == res['count_' + kw][1]
res['count_HUMAN_RESULT_PENDING'] = [A.count('[HUMAN RESULT PENDING]'), B.count('[HUMAN RESULT PENDING]')]
hard['count_unchanged_HUMAN_RESULT_PENDING'] = res['count_HUMAN_RESULT_PENDING'][0] == res['count_HUMAN_RESULT_PENDING'][1]
hard['SUBMISSION_READY_NO_kept'] = B.count('SUBMISSION_READY = NO') == A.count('SUBMISSION_READY = NO') >= 1

# ---- 5. status vocabulary ----
STALE = ['執行條件尚待滿足', '執行條件待滿足', 'EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION',
         'REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION', '日後是否重跑', '日後是否及何時重跑', 'PRIORITY_RATIONALE_REVIEW_REQUESTED',
         '開放驗證行動', '開放的驗證行動', 'NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET', '以目前來源集無法執行']
NEWV = ['v1.8.5 COMPUTE CLOSURE CANDIDATE', 'COMPUTATIONAL_VALIDATION_STATUS = CLOSED_WITH_BOUNDED_HUMAN_VALIDITY',
        'SATISFIED_AS_AUDITED_LABEL_SENSITIVITY_ANALYSIS', 'FULL_REANALYSIS_EXECUTED = YES', 'AUDITED_LABEL_SENSITIVITY_ANALYSIS',
        'PRIMARY_BASELINE_REPLACED = NO', 'CORPUS_WIDE_HUMAN_VALIDITY = NOT_ESTABLISHED', 'BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1',
        'STABLE_UNDER_FULL_AUDITED_LABEL_REANALYSIS', '13/13 逐位元組相同',
        '主要分析維持預先凍結之 V5/R14 基準；另以 50 筆目標人工稽核標籤進行有界替代，完整重跑所有標籤相依分析，以評估結論對語意標籤修訂的敏感性',
        'FULL_REANALYSIS_REQUIRED', 'NOT_RECOMMENDED', 'AUTHOR TO CONFIRM', 'SUBMISSION_READY = NO']
for t in STALE + NEWV:
    res['term_' + t] = [A.count(t), B.count(t)]
hard['no_stale_pending_wording'] = all(B.count(t) == 0 for t in STALE)
hard['status_line_L5_v185'] = lb[4].count('v1.8.5 COMPUTE CLOSURE CANDIDATE') == 1 and \
    'COMPUTATIONAL_VALIDATION_STATUS = CLOSED_WITH_BOUNDED_HUMAN_VALIDITY' in lb[4] and 'SUBMISSION_READY = NO' in lb[4]
hard['corpus_wide_limitation_present'] = B.count('CORPUS_WIDE_HUMAN_VALIDITY = NOT_ESTABLISHED') >= 4 and B.count('全語料的人類效度') >= 6
hard['primary_baseline_replaced_NO_present'] = B.count('PRIMARY_BASELINE_REPLACED = NO') >= 4

# ---- 6. forbidden claims ----
FORBID = ['human validation confirmed corpus taxonomy', 'full reanalysis solved low kappa',
          'human labels validated all 6,499 records', 'human labels validated all 6499 records', 'FULLY_VALIDATED',
          '人類驗證確認了語料分類', '人工驗證確認全語料', '完整重分析解決了低', '人工標籤驗證了全部 6,499']
res['forbidden_hits'] = {t: B.lower().count(t.lower()) for t in FORBID}
hard['no_forbidden_claims'] = not any(res['forbidden_hits'].values())

# ---- 7. primary-baseline numbers unchanged ----
PRIMARY_PHRASES = ['保留 6,499 筆分析記錄', '其中 3,125 筆的人工智慧端與決策端皆完成分類', '形成 2,180 筆功能配對邊',
                   '辨識出 47 個', '32 個配對在四種分析下皆顯著且方向一致，其中 16 個高於期望、16 個低於期望',
                   '主要分析最後留下 3,125 筆兩端皆完成分類的證據記錄，涵蓋 783 篇文獻；去除同篇文獻內的重複配對後，形成 2,180 筆文獻層級邊',
                   '凍結的 32 組（16 過度、16 不足）仍為正式推論基準', '| L2 主要穩健集合 |', '| L1 主要零模型顯著 |',
                   '6,499 strict analytical records; 3,125 were fully mapped', 'yielding 2,180 document-level',
                   'identified 47 cells', 'comprising 16 enrichments and 16 depletions']
res['primary_phrase_counts'] = {p: [A.count(p), B.count(p)] for p in PRIMARY_PHRASES}
hard['primary_phrases_unchanged'] = all(v[0] == v[1] and v[0] >= 1 for v in res['primary_phrase_counts'].values())
PRIM_TOK = ['6,499', '3,125', '783', '2,180']
res['primary_token_counts'] = {t: [len(re.findall(r'(?<![\d,])' + re.escape(t) + r'(?![\d,])', A)),
                                   len(re.findall(r'(?<![\d,])' + re.escape(t) + r'(?![\d,])', B))] for t in PRIM_TOK}
hard['primary_tokens_not_removed'] = all(v[1] >= v[0] for v in res['primary_token_counts'].values())
# sensitivity-only values must never appear outside a sensitivity-labelled context
SENS_TOK = ['3,107', '781', '2,181', '15／17', '15 過度、17 不足', '.0325', '.0610', '.0405', '.0298', '.0223', '.0567', '.0434',
            '15 enrichments and 17 depletions']
t49b_s = lb.index('**表 4-9B：主要分析（凍結基準）與稽核標籤替代敏感度分析的比較**')
t49b_e = next(i for i in range(t49b_s + 2, len(lb)) if lb[i].strip() == '')
viol = []
SET_A = set(la)
for i, line in enumerate(lb):
    if t49b_s <= i < t49b_e:
        continue
    for t in SENS_TOK:
        if t in line and line not in SET_A and not any(k in line for k in ('敏感度', 'sensitivity', '替換後', '替換')):
            viol.append([i + 1, t])
res['sensitivity_token_outside_labelled_context'] = viol
hard['sensitivity_numbers_labelled'] = not viol
hdr = lb[t49b_s + 2]
hard['table_4_9B_columns_separate_primary_vs_sensitivity'] = ('主要分析' in hdr and '敏感度分析' in hdr and '不取代主要分析' in hdr)

# ---- 8. numeric traceability ----
NUM = re.compile(r'(?<![\w.])(?:\d+(?:[.,:/\-]\d+)*|\.\d+)')
na, nb = Counter(NUM.findall(A)), Counter(NUM.findall(B))
res['numeric_added_doc'] = dict(sorted((nb - na).items()))
res['numeric_removed_doc'] = dict(sorted((na - nb).items()))
per, tot = {}, Counter()
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
SRC = json.load(open(sys.argv[3].replace('patches_v185.json', 'numeric_sources_v185.json'), encoding='utf-8'))
res['numeric_added_unmapped'] = {k: v for k, v in res['numeric_added_doc'].items() if k not in SRC}
hard['numeric_added_all_traceable'] = not res['numeric_added_unmapped']
res['numeric_sources'] = {k: SRC[k] for k in res['numeric_added_doc'] if k in SRC}
REMOVABLE = {'04', '07', '2', '256', '37', '38', '5', '8'}
res['numeric_removed_unexpected'] = {k: v for k, v in res['numeric_removed_doc'].items() if k not in REMOVABLE}
hard['numeric_removed_only_status_wording_tokens'] = not res['numeric_removed_unexpected']

res['hard_checks'] = hard
res['ALL_HARD_CHECKS_PASS'] = all(v is True for v in hard.values())
json.dump(res, open(sys.argv[4], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in res.items() if not k.startswith(('changed_lines', 'diff_opcodes', 'numeric_sources'))},
                 ensure_ascii=False, indent=0))
sys.exit(0 if res['ALL_HARD_CHECKS_PASS'] else 1)
