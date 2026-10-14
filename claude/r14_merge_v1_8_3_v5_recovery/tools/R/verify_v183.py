"""Verify v1.8.3 vs v1.8.2. Usage: python -I verify_v183.py <v1.8.2 md> <v1.8.3 md> <patches.json> <out json>
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

sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
ca, cb = [], []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal':
        ca += list(range(i1 + 1, i2 + 1))
        cb += list(range(j1 + 1, j2 + 1))
res['changed_lines_v182'], res['changed_lines_v183'] = ca, cb
res['patched_lines_v182'] = sorted({p['v182_line'] for p in PATCHES})
hard['changed_lines_subset_of_patched_lines'] = set(ca) <= set(res['patched_lines_v182'])


def math_spans(t):
    blocks = re.findall(r'\$\$.*?\$\$', t, flags=re.S)
    t2 = re.sub(r'\$\$.*?\$\$', '', t, flags=re.S)
    return {'$$': blocks, '$inline': re.findall(r'(?<!\\)\$[^$\n]+?\$', t2),
            '\\[\\]': re.findall(r'\\\[.*?\\\]', t, flags=re.S),
            'begin_env': re.findall(r'\\begin\{.*?\\end\{[^}]*\}', t, flags=re.S)}


ma, mb = math_spans(A), math_spans(B)
res['math_counts'] = {k: [len(ma[k]), len(mb[k])] for k in ma}
hard['math_identical_ordered'] = all(ma[k] == mb[k] for k in ma)
FA, FB = re.findall(r'```.*?```', A, flags=re.S), re.findall(r'```.*?```', B, flags=re.S)
res['fenced_blocks_changed'] = [i for i, (x, y) in enumerate(zip(FA, FB)) if x != y]
res['fenced_patches'] = [p['id'] for p in PATCHES if any(p['old'] in x for x in FA)]
B_rev = B
for p in PATCHES:
    if p['id'] in res['fenced_patches']:
        B_rev = B_rev.replace(p['new'], p['old'], 1)
# fenced (diagram) blocks may differ only by the listed status-wording patches
hard['fenced_blocks_identical_except_listed_status_patches'] = re.findall(r'```.*?```', B_rev, flags=re.S) == FA and len(FA) == len(FB)
TAG = re.compile(r'\\tag\{[^}]*\}')
hard['equation_tags_identical'] = TAG.findall(A) == TAG.findall(B)
MATHMARK = re.compile(r'\$|\\\(|\\\[|\\begin|\\frac|\\sum|\\tag')
hard['no_math_markers_in_patch_text'] = not [p['id'] for p in PATCHES if MATHMARK.search(p['old'] + p['new'])]

ha, hb = [x for x in la if x.startswith('#')], [x for x in lb if x.startswith('#')]
res['headings'] = [len(ha), len(hb)]
hard['headings_identical'] = ha == hb
CAP = re.compile(r'^\*\*(表|圖) ')
hard['table_figure_captions_identical'] = [x for x in la if CAP.match(x)] == [x for x in lb if CAP.match(x)]

GROW = re.compile(r'^\|\s*G(?:0[1-9]|1[0-6])\b')
ga, gb = [x for x in la if GROW.match(x)], [x for x in lb if GROW.match(x)]
res['G_table_rows'] = [len(ga), len(gb)]
hard['G_rows_identical_ordered'] = ga == gb
G = re.compile(r'G(?:0[1-9]|1[0-6])\b')
res['G_token_counts'] = [len(G.findall(A)), len(G.findall(B))]
hard['G_token_count_unchanged'] = res['G_token_counts'][0] == res['G_token_counts'][1]
hard['GM_arrow_tokens_identical'] = Counter(re.findall(r'G\d\d\s*[→／/]\s*M\d', A)) == Counter(re.findall(r'G\d\d\s*[→／/]\s*M\d', B))


def section(lines, s_pat, e_pat):
    s = next(i for i, x in enumerate(lines) if re.search(s_pat, x))
    e = next(i for i in range(s + 1, len(lines)) if re.search(e_pat, lines[i]))
    return lines[s:e]


for name, sp, ep in [('3_9_2_tables_3_4_3_4A', r'^### 3\.9\.2', r'^### 3\.9\.3'),
                     ('3_9_3_V1_design', r'^### 3\.9\.3', r'^### 3\.9\.4'),
                     ('3_9_4', r'^### 3\.9\.4', r'^### 3\.9\.5'),
                     ('3_9_5', r'^### 3\.9\.5', r'^## 3\.10'),
                     ('3_12_enterprise_math', r'^## 3\.12', r'^## 3\.13'),
                     ('4_4_results', r'^## 4\.4', r'^## 4\.5'),
                     ('4_7_V1_results', r'^## 4\.7', r'^## 4\.8')]:
    try:
        sa, sb = section(la, sp, ep), section(lb, sp, ep)
        hard['section_' + name + '_identical'] = sa == sb
        res['section_' + name + '_lines'] = len(sa)
    except StopIteration:
        res['section_' + name + '_identical'] = 'SECTION_NOT_FOUND'

for kw in ['VCP', 'VSC', 'DL', 'NEV', 'Enterprise', 'SIMULATED_ONLY', 'EMPIRICAL RESULT PENDING', 'SUBMISSION_READY',
           'FULL_REANALYSIS_REQUIRED', 'UNIDENTIFIED', 'M1', 'M2', 'M3', 'M4', 'M5', 'REAL EVIDENCE']:
    res['count_' + kw] = [len(re.findall(r'\b' + re.escape(kw) + r'\b', A)), len(re.findall(r'\b' + re.escape(kw) + r'\b', B))]
    if kw != 'FULL_REANALYSIS_REQUIRED':
        hard['count_unchanged_' + kw] = res['count_' + kw][0] == res['count_' + kw][1]
res['count_HUMAN_RESULT_PENDING'] = [A.count('[HUMAN RESULT PENDING]'), B.count('[HUMAN RESULT PENDING]')]
hard['count_unchanged_HUMAN_RESULT_PENDING'] = res['count_HUMAN_RESULT_PENDING'][0] == res['count_HUMAN_RESULT_PENDING'][1]

# status vocabulary
for t in ['NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET', 'EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION',
          'REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION', 'NOT_RECOMMENDED', 'PRIORITY_RATIONALE_REVIEW_REQUESTED',
          'RECOVERED_FROM_SIDECAR_POLICY', '以目前的來源集無法執行', '以目前來源集無法執行', '12 項未尋回',
          'NOT_REQUIRED', 'AUTHOR TO CONFIRM', 'v1.8.3 V5 PROVENANCE CANDIDATE']:
    res['term_' + t] = [A.count(t), B.count(t)]
hard['no_stale_not_executable'] = B.count('NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET') == 0 and B.count('以目前的來源集無法執行') == 0 \
    and B.count('以目前來源集無法執行') == 0 and B.count('12 項未尋回') == 0
hard['no_NOT_REQUIRED'] = B.count('NOT_REQUIRED') == 0
hard['method_status_unchanged'] = res['term_REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION'][0] == res['term_REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION'][1]
hard['priority_status_unchanged_or_added'] = B.count('NOT_RECOMMENDED') >= A.count('NOT_RECOMMENDED')

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
# provenance-only numeric tokens (file numbers, version labels, byte/file counts, run id, section refs)
ALLOWED_NUM = {'1.8.3', '1.8.2', '35', '36', '37', '38', '39', '40', '41', '35-36', '35-38', '39-40', '37-38', '35-39',
               '256', '355', '74', '13', '20260922', '3.7.1', '3.7.4', '3.8.3', '4.5.5', '5.8.9', '1', '2', '5', '32'}
res['numeric_added_not_in_allowlist'] = {k: v for k, v in res['numeric_added_doc'].items() if k not in ALLOWED_NUM}
hard['numeric_added_all_allowlisted'] = not res['numeric_added_not_in_allowlist']
res['numeric_removed_not_expected'] = {k: v for k, v in res['numeric_removed_doc'].items() if k not in {'12'}}
hard['numeric_removed_only_12'] = not res['numeric_removed_not_expected']

RESULT_PAT = [r'[ακ]\s*=\s*[-−]?\.?\d', r'q\s*[=<≤]\s*\.?\d', r'O/E', r'p_BH', r'[−-]18\b', r'\d+／\d+（']
hits = {}
for p in PATCHES:
    for pat in RESULT_PAT:
        if len(re.findall(pat, p['new'])) > len(re.findall(pat, p['old'])):
            hits.setdefault(p['id'], []).append(pat)
res['result_like_tokens_added'] = hits
hard['no_result_like_tokens_added'] = not hits

res['hard_checks'] = hard
res['ALL_HARD_CHECKS_PASS'] = all(v is True for v in hard.values())
json.dump(res, open(sys.argv[4], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in res.items() if not k.startswith('changed_lines')}, ensure_ascii=False, indent=0))
sys.exit(0 if res['ALL_HARD_CHECKS_PASS'] else 1)
