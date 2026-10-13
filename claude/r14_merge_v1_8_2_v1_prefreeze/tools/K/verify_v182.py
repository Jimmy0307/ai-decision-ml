"""Verify v1.8.2 vs v1.8.1. Usage: python -I verify_v182.py <v1.8.1 md> <v1.8.2 md> <patches.json> <out json>"""
import sys, re, json, difflib
sys.stdout.reconfigure(encoding="utf-8")
from collections import Counter

A = open(sys.argv[1], encoding='utf-8').read()
B = open(sys.argv[2], encoding='utf-8').read()
PATCHES = json.load(open(sys.argv[3], encoding='utf-8'))
la, lb = A.split('\n'), B.split('\n')
res = {'line_count': [len(la), len(lb)]}

# ---- line alignment ----------------------------------------------------------
sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
changed_a, changed_b = [], []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal':
        changed_a += list(range(i1 + 1, i2 + 1))
        changed_b += list(range(j1 + 1, j2 + 1))
res['changed_lines_v181'] = changed_a
res['changed_lines_v182'] = changed_b


# ---- 1. math ------------------------------------------------------------------
def math_spans(t):
    blocks = re.findall(r'\$\$.*?\$\$', t, flags=re.S)
    t2 = re.sub(r'\$\$.*?\$\$', '', t, flags=re.S)
    inline = re.findall(r'(?<!\\)\$[^$\n]+?\$', t2)
    brk = re.findall(r'\\\[.*?\\\]', t, flags=re.S)
    envs = re.findall(r'\\begin\{.*?\\end\{[^}]*\}', t, flags=re.S)
    return {'$$': blocks, '$inline': inline, '\\[\\]': brk, 'begin_env': envs}


ma, mb = math_spans(A), math_spans(B)
res['math_counts_v181'] = {k: len(v) for k, v in ma.items()}
res['math_counts_v182'] = {k: len(v) for k, v in mb.items()}
res['math_identical_ordered'] = {k: ma[k] == mb[k] for k in ma}
fa, fb = re.findall(r'```.*?```', A, flags=re.S), re.findall(r'```.*?```', B, flags=re.S)
res['fenced_blocks_identical'] = fa == fb
TAG = re.compile(r'\\tag\{[^}]*\}')
res['equation_tags_identical'] = TAG.findall(A) == TAG.findall(B)
MATHMARK = re.compile(r'\$|\\\(|\\\[|\\begin|\\frac|\\sum|\\tag')
res['changed_lines_with_math_markers'] = [n for n in changed_a if MATHMARK.search(la[n - 1])] + \
                                         [n for n in changed_b if MATHMARK.search(lb[n - 1])]
res['patch_text_math_markers'] = [p['id'] for p in PATCHES if MATHMARK.search(p['old']) or MATHMARK.search(p['new'])]

# ---- 2. headings ----------------------------------------------------------------
ha = [x for x in la if x.startswith('#')]
hb = [x for x in lb if x.startswith('#')]
res['headings'] = {'v181': len(ha), 'v182': len(hb), 'identical': ha == hb}
CAP = re.compile(r'^\*\*(表|圖) ')
res['table_figure_captions_identical'] = [x for x in la if CAP.match(x)] == [x for x in lb if CAP.match(x)]

# ---- 3. G rows / G->M ------------------------------------------------------------
GROW = re.compile(r'^\|\s*G(?:0[1-9]|1[0-6])\b')
ga, gb = [x for x in la if GROW.match(x)], [x for x in lb if GROW.match(x)]
res['G_table_rows'] = {'v181': len(ga), 'v182': len(gb), 'identical_ordered': ga == gb}


def section(lines, start_pat, stop_pat):
    s = next(i for i, x in enumerate(lines) if re.search(start_pat, x))
    e = next(i for i in range(s + 1, len(lines)) if re.search(stop_pat, lines[i]))
    return lines[s:e]


t34a = section(la, r'^### 3\.9\.2', r'^### 3\.9\.3')
t34b = section(lb, r'^### 3\.9\.2', r'^### 3\.9\.3')
res['section_3_9_2_tables_3_4_and_3_4A_identical'] = t34a == t34b
res['section_3_9_2_line_count'] = len(t34a)
t411a, t411b = section(la, r'^### 4\.7\.1', r'^### 4\.7\.2'), section(lb, r'^### 4\.7\.1', r'^### 4\.7\.2')
res['section_4_7_1_table_4_11_identical'] = t411a == t411b
t412a, t412b = section(la, r'^### 4\.7\.2', r'^### 4\.7\.3'), section(lb, r'^### 4\.7\.2', r'^### 4\.7\.3')
res['section_4_7_2_table_4_12_identical'] = t412a == t412b
eaxa, eaxb = section(la, r'^### 4\.7\.4', r'^## 4\.8'), section(lb, r'^### 4\.7\.4', r'^## 4\.8')
res['section_4_7_4_EAX_identical'] = eaxa == eaxb
s395a, s395b = section(la, r'^### 3\.9\.5', r'^## 3\.10'), section(lb, r'^### 3\.9\.5', r'^## 3\.10')
res['section_3_9_5_identical'] = s395a == s395b
eax_par = [x for x in la if x.startswith('EA-X（解釋可用性）是唯一由缺口新提出的候選構念')]
res['EAX_paragraph_3_9_3_unchanged'] = len(eax_par) == 1 and eax_par[0] in lb
G = re.compile(r'G(?:0[1-9]|1[0-6])\b')
res['G_token_counts'] = [len(G.findall(A)), len(G.findall(B))]
res['G_tokens_per_patch'] = {p['id']: [len(G.findall(p['old'])), len(G.findall(p['new']))] for p in PATCHES
                             if G.findall(p['old']) or G.findall(p['new'])}
M = re.compile(r'G\d\d\s*[→／/]\s*M\d')
res['GM_arrow_tokens_identical'] = Counter(M.findall(A)) == Counter(M.findall(B))
for kw in ['VCP', 'VSC', 'DL', 'NEV', 'Enterprise', 'Study 1', 'SIMULATED_ONLY', 'EMPIRICAL RESULT PENDING',
           'SUBMISSION_READY', 'FULL_REANALYSIS_REQUIRED', 'UNIDENTIFIED', 'M5']:
    res['count_' + kw] = [len(re.findall(r'\b' + re.escape(kw) + r'\b', A)), len(re.findall(r'\b' + re.escape(kw) + r'\b', B))]
res['count_HUMAN_RESULT_PENDING'] = [A.count('[HUMAN RESULT PENDING]'), B.count('[HUMAN RESULT PENDING]')]

# ---- 4. numeric tokens ------------------------------------------------------------
NUM = re.compile(r'(?<![\w.])(?:\d+(?:[.,:/\-]\d+)*|\.\d+)')
na, nb = Counter(NUM.findall(A)), Counter(NUM.findall(B))
res['numeric_added_doc'] = dict(sorted((nb - na).items()))
res['numeric_removed_doc'] = dict(sorted((na - nb).items()))
per = {}
for p in PATCHES:
    a, b = Counter(NUM.findall(p['old'])), Counter(NUM.findall(p['new']))
    if a != b:
        per[p['id']] = {'added': dict(b - a), 'removed': dict(a - b)}
res['numeric_per_patch'] = per
tot = Counter()
for p in PATCHES:
    tot.update(Counter(NUM.findall(p['new'])))
    tot.subtract(Counter(NUM.findall(p['old'])))
doc = Counter(nb)
doc.subtract(na)
res['numeric_patch_sum_matches_doc'] = {k: v for k, v in tot.items() if v} == {k: v for k, v in doc.items() if v}
ALLOWED_NUM = {'1', '2', '3', '13', '16', '24', '25', '26', '27', '28', '29', '30', '32', '53', '95', '5,000',
               '.800', '.667', '1.8.1', '1.8.2', '1960', '2004', '4.7.3', '3.9.3', '3.9.4', '4', '6', '8', '1.8', '2.3',
               '60', '182', '19', '21', '20', '5', '7', '1.0', '256', '4-13'}
res['numeric_added_not_in_allowlist'] = {k: v for k, v in res['numeric_added_doc'].items() if k not in ALLOWED_NUM}

# ---- 5. no human result inserted ------------------------------------------------
RESULT_PAT = [r'[ακ]\s*=\s*[-−]?\.?\d', r'\d+\s*／\s*16(?!\s*項)', r'\b\d+/16\b', r'V1_PASS_HUMAN_C6\s*=\s*(YES|PASS|TRUE)',
              r'RELIABILITY_COMPUTED', r'KEY_COMPARED', r'ADJUDICATION_IMPORTED', r'CI\s*[=\[]\s*\.?\d']
hits = {}
for p in PATCHES:
    for pat in RESULT_PAT:
        for m in re.finditer(pat, p['new']):
            if not re.search(pat, p['old']) or len(re.findall(pat, p['new'])) > len(re.findall(pat, p['old'])):
                hits.setdefault(p['id'], []).append(m.group(0))
res['result_like_tokens_added'] = hits
res['oa2_sentence_count_v182'] = B.count('V1_PASS_HUMAN_C6 is a continuity label under the earlier 53B protocol, '
                                         'not evidence that the amended Q1–Q5 instrument is identical to 53B.')
for code in ['CURRENT_INSTRUMENT_RELIABILITY', '53B_CONTINUITY_RELIABILITY', 'UNRESOLVED/NOT_ACCEPTABLE', 'IMPRECISE',
             '研究慣例', '不主張完美的盲性', '不檢驗 32 格的成員資格']:
    res['count_v182_' + code] = B.count(code)

# ---- 6. leakage (public repo rule) -----------------------------------------------
res['leak_item_ids_v182'] = len(re.findall(r'ITEM-[A-Z]\d\d', B))
res['leak_seed_like_v182'] = 'SECRET_SEED' in B

# ---- 7. remaining two-coder design statements --------------------------------------
ctx = {}
for pat in ['兩位編碼者', '雙人盲編', '人類雙人', '至少兩位', '兩位人類', '兩份封包', 'A vs B', '編碼者 A']:
    ctx[pat] = [(i + 1, x[max(0, x.find(pat) - 70): x.find(pat) + 70]) for i, x in enumerate(lb) if pat in x]
res['two_coder_mentions_v182'] = ctx
json.dump(res, open(sys.argv[4], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
brief = {k: v for k, v in res.items() if k not in ('two_coder_mentions_v182', 'changed_lines_v181', 'changed_lines_v182')}
print(json.dumps(brief, ensure_ascii=False, indent=0))
print('TWO-CODER MENTIONS:')
for k, v in ctx.items():
    for n, s in v:
        print(' ', k, 'L', n, s)
