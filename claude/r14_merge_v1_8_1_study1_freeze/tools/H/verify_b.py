import sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
hist, ca, logp = sys.argv[1:4]
log = json.load(open(logp, encoding='utf-8'))
pat = re.compile(r'ABSENT|不在本?工作環境|不在環境|缺件|待核|2026-09-29|09-29|依作者回報|使用者陳述|使用者稱|作者陳述|USER-REPORTED|ARTIFACT PENDING|not in workspace|FULL_REANALYSIS_REQUIRED|完整重分析|未回報|NOT_REQUIRED|待以原始檔案')
M = 'SUPERSEDED_BY_V1_8_SOURCE_CLOSURE'
for f in sorted({e['file'] for e in log}):
    dst = next(e['current_copy'] for e in log if e['file'] == f)
    a = open(__import__('os').path.join(hist, f), encoding='utf-8').read().split('\n')
    b = open(__import__('os').path.join(ca, dst), encoding='utf-8').read().split('\n')
    hdr = b.index('> **CURRENT COPY (V1.8.1, 2026-10-14) — current copy; history preserved.**')
    body = b[hdr + 7:]
    assert len(body) == len(a), (f, len(body), len(a))
    changed = {i + 1 for i, (x, y) in enumerate(zip(a, body)) if x != y}
    planned = {e['line'] for e in log if e['file'] == f}
    print(f, 'changed lines', sorted(changed), 'eq planned', changed == planned)
    for i, y in enumerate(body, 1):
        for m in pat.finditer(y):
            pass
        hits = sorted(set(pat.findall(y)))
        if hits:
            print('  L%d %s %s %s' % (i, 'EDITED' if i in changed else 'unchanged', 'MARKER' if M in y else '', hits))
    print('  NOT_REQUIRED anywhere:', 'FULL_REANALYSIS_NOT_REQUIRED' in '\n'.join(b))
