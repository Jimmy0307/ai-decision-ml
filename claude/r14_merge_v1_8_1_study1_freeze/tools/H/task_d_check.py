"""Task D check: REANALYSIS_CANDIDATES labels vs first-coder vs reconciled FINAL. Usage: python -I task_d_check.py <V9_DIR>"""
import sys, csv, os, json
sys.stdout.reconfigure(encoding='utf-8')
d = sys.argv[1]
rd = lambda f: list(csv.DictReader(open(os.path.join(d, f), encoding='utf-8-sig')))
cand = {r['record_id']: r for r in rd('REANALYSIS_CANDIDATES_FROM_HUMAN_AUDIT.csv')}
fc = {r['record_id']: r for r in rd('FIRST_CODER_50_FINAL_FROZEN.csv')}
rec = {r['record_id']: r for r in rd('HUMAN_RECONCILED_20.csv')}
print('cand rows', len(cand), 'fc', len(fc), 'rec', len(rec))
print('rec cols', [c for c in list(rec.values())[0].keys() if 'FINAL' in c or 'C3' in c or 'C4' in c][:20])
eq_fc = sum(1 for k, r in cand.items() if r['human_ai_family'] == fc[k]['human_ai_family'] and r['human_decision_family'] == fc[k]['human_decision_family'])
print('cand ai/dec == first-coder:', eq_fc, '/', len(cand))
diff = 0; incand = 0
for k, r in rec.items():
    f = fc[k]
    keys = [('FINAL_C1', 'human_evidence_valid'), ('FINAL_C3', 'human_ai_family'), ('FINAL_C4', 'human_decision_family'), ('FINAL_C5', 'human_include')]
    fk = {c for c in r if c.startswith('FINAL_C')}
    def g(prefix):
        m = [c for c in fk if c.startswith(prefix)]
        return r[m[0]] if m else None
    d1 = any(g(a) is not None and g(a) != f[b] for a, b in keys)
    diff += d1; incand += k in cand
print('reconciled records whose FINAL differs from first-coder (C1/C3/C4/C5):', diff, '/', len(rec), '; reconciled in candidates:', incand)
