"""Verify v1.8 vs v1.7. Usage: python -I verify_v18.py <v1.7 md> <v1.8 md> <out json>"""
import sys, re, json
from collections import Counter

A = open(sys.argv[1], encoding='utf-8').read()
B = open(sys.argv[2], encoding='utf-8').read()
la, lb = A.split('\n'), B.split('\n')
res = {}
res['line_count'] = [len(la), len(lb)]
assert len(la) == len(lb), 'line count changed'
changed = [i + 1 for i, (x, y) in enumerate(zip(la, lb)) if x != y]
res['changed_lines'] = changed

# 1. math
def math_spans(t):
    blocks = re.findall(r'\$\$.*?\$\$', t, flags=re.S)
    t2 = re.sub(r'\$\$.*?\$\$', '', t, flags=re.S)
    inline = re.findall(r'(?<!\\)\$[^$\n]+?\$', t2)
    envs = re.findall(r'\\begin\{.*?\\end\{[^}]*\}', t, flags=re.S)
    brk = re.findall(r'\\\[.*?\\\]', t, flags=re.S)
    return blocks, inline, envs, brk
ma, mb = math_spans(A), math_spans(B)
res['math_counts_v17'] = [len(x) for x in ma]
res['math_counts_v18'] = [len(x) for x in mb]
res['math_identical'] = all(Counter(x) == Counter(y) for x, y in zip(ma, mb))
# fenced code blocks
def fences(t):
    return re.findall(r'```.*?```', t, flags=re.S)
res['fenced_blocks'] = [len(fences(A)), len(fences(B))]
res['fenced_identical'] = fences(A) == fences(B)
MATHMARK = re.compile(r'\$|\\\(|\\\[|\\begin|\\frac|\\sum|\\max|\\min|_\{|\^\{|```')
eqlike = re.compile(r'(?:=|≤|≥|∑|∈)')
res['changed_lines_with_math_markers'] = [n for n in changed if MATHMARK.search(la[n-1]) or MATHMARK.search(lb[n-1])]
# equation-like lines (contain = and code/math chars) unchanged check: any line in v1.7 that looks like an equation is unchanged
eq_lines = [i+1 for i, x in enumerate(la) if MATHMARK.search(x)]
res['math_marker_lines_v17'] = len(eq_lines)
res['math_marker_lines_changed'] = [n for n in eq_lines if la[n-1] != lb[n-1]]
# '=' occurrences within changed lines: compare segments
def eq_tokens(s):
    return re.findall(r'[A-Za-z_κ][\w′ ]{0,30}=\s?[^，；。|)）]{0,25}', s)
res['changed_line_eq_tokens_added'] = {}
res['changed_line_eq_tokens_removed'] = {}
for n in changed:
    ca, cb = Counter(eq_tokens(la[n-1])), Counter(eq_tokens(lb[n-1]))
    add, rem = cb - ca, ca - cb
    if add: res['changed_line_eq_tokens_added'][n] = list(add.elements())
    if rem: res['changed_line_eq_tokens_removed'][n] = list(rem.elements())

# 2. numeric tokens
NUM = re.compile(r'(?<![\w.])(?:\d+(?:[.,:/\-]\d+)*|\.\d+)')
na, nb = Counter(NUM.findall(A)), Counter(NUM.findall(B))
res['numeric_added'] = dict(nb - na)
res['numeric_removed'] = dict(na - nb)
# per changed line
per = {}
for n in changed:
    a, b = Counter(NUM.findall(la[n-1])), Counter(NUM.findall(lb[n-1]))
    if a != b:
        per[n] = {'added': dict(b - a), 'removed': dict(a - b)}
res['numeric_per_line'] = per
# G lines
G = re.compile(r'G(0[1-9]|1[0-6])\b')
glines = [i+1 for i, x in enumerate(la) if G.search(x)]
res['G_lines_total'] = len(glines)
res['G_lines_changed'] = [n for n in glines if la[n-1] != lb[n-1]]
res['G_table_rows_changed'] = [n for n in glines if la[n-1].lstrip().startswith('|') and la[n-1] != lb[n-1]]
res['G_tokens_identical_in_changed_lines'] = all(Counter(G.findall(la[n-1])) == Counter(G.findall(lb[n-1])) for n in changed)
res['G_token_counts'] = [sum(len(G.findall(x)) for x in la), sum(len(G.findall(x)) for x in lb)]
# M mapping tokens
M = re.compile(r'G\d\d\s*→\s*M\d')
res['GM_arrow_tokens'] = [Counter(M.findall(A)) == Counter(M.findall(B))]
for kw in ['VCP', 'VSC', 'DL', 'NEV']:
    res['count_' + kw] = [len(re.findall(r'\b' + kw + r'\b', A)), len(re.findall(r'\b' + kw + r'\b', B))]

# 3. remaining flags
pats = ['2026-09-29', '20260929', '待核', '依作者回報', '工作環境中', 'AUTHOR TO CONFIRM', 'pending verification',
        '作者回報', '推得', '人工調和後的標籤替換', '人工調和標籤替換', '原始檔案未在', '只來自作者']
rem = {}
for p in pats:
    hits = [i+1 for i, x in enumerate(lb) if p in x]
    if hits:
        rem[p] = hits
res['remaining_flag_hits_v18'] = rem
res['remaining_flag_contexts'] = {p: [(n, lb[n-1][max(0, lb[n-1].find(p)-60): lb[n-1].find(p)+80]) for n in v] for p, v in rem.items()}

# 4. headings
ha = [x for x in la if x.startswith('#')]
hb = [x for x in lb if x.startswith('#')]
res['headings'] = [len(ha), len(hb), ha == hb]
json.dump(res, open(sys.argv[3], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ('remaining_flag_contexts',)}, ensure_ascii=False)[:6000])
