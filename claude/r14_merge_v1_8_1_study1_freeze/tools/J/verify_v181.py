"""Verify v1.8.1 vs v1.8. Usage: python -I verify_v181.py <v1.8 md> <v1.8.1 md> <patches.json> <out json>"""
import sys, re, json, difflib
from collections import Counter

A = open(sys.argv[1], encoding='utf-8').read()
B = open(sys.argv[2], encoding='utf-8').read()
PATCHES = json.load(open(sys.argv[3], encoding='utf-8'))
la, lb = A.split('\n'), B.split('\n')
res = {'line_count': [len(la), len(lb)]}

# ---- line alignment ----------------------------------------------------------
sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
pairs, inserted, deleted = [], [], []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    if tag == 'replace' and (i2 - i1) == (j2 - j1):
        pairs += [(i + 1, j1 + (i - i1) + 1) for i in range(i1, i2)]
    elif tag == 'insert':
        inserted += list(range(j1 + 1, j2 + 1))
    elif tag == 'replace' and (j2 - j1) > (i2 - i1):
        # changed line followed by inserted lines
        pairs += [(i + 1, j1 + (i - i1) + 1) for i in range(i1, i2)]
        inserted += list(range(j1 + (i2 - i1) + 1, j2 + 1))
    else:
        deleted += list(range(i1 + 1, i2 + 1))
res['changed_line_pairs_v18_v181'] = pairs
res['inserted_lines_v181'] = inserted
res['deleted_lines_v18'] = deleted
assert not deleted, 'lines deleted'


# ---- 1. math ------------------------------------------------------------------
def math_spans(t):
    blocks = re.findall(r'\$\$.*?\$\$', t, flags=re.S)
    t2 = re.sub(r'\$\$.*?\$\$', '', t, flags=re.S)
    inline = re.findall(r'(?<!\\)\$[^$\n]+?\$', t2)
    brk = re.findall(r'\\\[.*?\\\]', t, flags=re.S)
    envs = re.findall(r'\\begin\{.*?\\end\{[^}]*\}', t, flags=re.S)
    return {'$$': blocks, '$inline': inline, '\\[\\]': brk, 'begin_env': envs}


ma, mb = math_spans(A), math_spans(B)
res['math_counts_v18'] = {k: len(v) for k, v in ma.items()}
res['math_counts_v181'] = {k: len(v) for k, v in mb.items()}
res['math_identical_ordered'] = {k: ma[k] == mb[k] for k in ma}
MATHMARK = re.compile(r'\$|\\\(|\\\[|\\begin|\\frac|\\sum|_\{|\^\{')
res['changed_lines_with_math_markers'] = [a for a, b in pairs if MATHMARK.search(la[a - 1]) or MATHMARK.search(lb[b - 1])]


def fences(t):
    return re.findall(r'```.*?```', t, flags=re.S)


fa, fb = fences(A), fences(B)
res['fenced_blocks'] = [len(fa), len(fb)]
res['fenced_changed_index'] = [i for i, (x, y) in enumerate(zip(fa, fb)) if x != y]

# ---- 2. headings ----------------------------------------------------------------
ha = [x for x in la if x.startswith('#')]
hb = [x for x in lb if x.startswith('#')]
res['headings'] = {'v18': len(ha), 'v181': len(hb), 'identical': ha == hb}

# ---- 3. G lines -------------------------------------------------------------------
G = re.compile(r'G(?:0[1-9]|1[0-6])\b')


def bracket_spans(s):
    spans, stack = [], []
    for i, ch in enumerate(s):
        if ch == '〔':
            stack.append(i)
        elif ch == '〕' and stack:
            spans.append((stack.pop(), i))
    return spans


def segs(a, b):
    m = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return [(t, i1, i2, j1, j2) for t, i1, i2, j1, j2 in m.get_opcodes() if t != 'equal']


glines = [i + 1 for i, x in enumerate(la) if G.search(x)]
res['G_lines_total_v18'] = len(glines)
gchk = []
for a, b in pairs:
    if not G.search(la[a - 1]) and not G.search(lb[b - 1]):
        continue
    old, new = la[a - 1], lb[b - 1]
    sp = bracket_spans(old)
    ops = segs(old, new)
    in_bracket = all(any(s < i1 and i2 <= e + 1 for s, e in sp) for _, i1, i2, _, _ in ops)
    gchk.append(dict(v18_line=a, v181_line=b, tokens_identical=Counter(G.findall(old)) == Counter(G.findall(new)),
                     all_changes_inside_provenance_bracket=in_bracket,
                     segments=[dict(OLD=old[i1:i2], NEW=new[j1:j2]) for _, i1, i2, j1, j2 in ops]))
res['G_lines_changed'] = gchk
res['G_in_inserted_lines'] = [n for n in inserted if G.search(lb[n - 1])]
res['G_token_counts'] = [len(G.findall(A)), len(G.findall(B))]
M = re.compile(r'G\d\d\s*→\s*M\d')
res['GM_arrow_tokens_identical'] = Counter(M.findall(A)) == Counter(M.findall(B))
for kw in ['VCP', 'VSC', 'DL', 'NEV', 'SIMULATED_ONLY', 'EMPIRICAL RESULT PENDING', 'HUMAN RESULT PENDING', 'UNIDENTIFIED']:
    res['count_' + kw] = [len(re.findall(r'\b' + re.escape(kw) + r'\b', A)), len(re.findall(r'\b' + re.escape(kw) + r'\b', B))]

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
# cross-check: sum of per-patch deltas equals doc delta
tot_add, tot_rem = Counter(), Counter()
for v in per.values():
    tot_add.update(v['added']); tot_rem.update(v['removed'])
res['numeric_patch_sum_matches_doc'] = (tot_add - tot_rem) == (nb - na) - (na - nb) or (
    dict(tot_add - tot_rem) == dict(nb - na) and dict(tot_rem - tot_add) == dict(na - nb))

# ---- 5. forbidden / remaining strings ---------------------------------------------
forbid = ['2026-09-29 紀錄，待核', 'FULL_REANALYSIS_NOT_REQUIRED', 'not required', 'Not required', 'NOT_REQUIRED',
          '不需要完整重分析', '無需完整重分析', '不須完整重分析', '2026-09-29']
res['forbidden_hits_v181'] = {f: [i + 1 for i, x in enumerate(lb) if f in x] for f in forbid}
ctx = {}
for p in ['待核', '研究者待決事項', '尚待執行', '待執行', 'AUTHOR TO CONFIRM', '工作環境中']:
    hits = []
    for i, x in enumerate(lb):
        for m in re.finditer(re.escape(p), x):
            hits.append((i + 1, x[max(0, m.start() - 60): m.end() + 60]))
    ctx[p] = hits
res['remaining_hits_v181'] = ctx
res['legacy_zip_mentions'] = {'v18': A.count('完整資料來源'), 'v181': B.count('完整資料來源')}
res['full_reanalysis_codes_v181'] = {c: B.count(c) for c in ['REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION',
                                                             'NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET', 'NOT_RECOMMENDED',
                                                             'FULL_REANALYSIS_REQUIRED']}
json.dump(res, open(sys.argv[4], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
summary = {k: v for k, v in res.items() if k not in ('remaining_hits_v181', 'G_lines_changed')}
summary['G_lines_changed_brief'] = [(g['v18_line'], g['tokens_identical'], g['all_changes_inside_provenance_bracket']) for g in gchk]
print(json.dumps(summary, ensure_ascii=False, indent=0)[:8000])
