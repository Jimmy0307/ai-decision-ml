"""Study 1 freeze: recompute primary baseline counts from the V9 official columns.
Usage: python -I baseline_check.py <ROBUST_CORE_LOCAL_SENSITIVITY.csv> <G01_G16 csv> <out.json>"""
import csv, sys, json, hashlib
p, gp, outp = sys.argv[1:4]
rows = list(csv.DictReader(open(p, encoding='utf-8-sig')))
T = lambda v: str(v).strip().lower() in ('true', '1', 'yes')
ai = sorted({r['ai_family'] for r in rows}); dec = sorted({r['decision_family'] for r in rows})
res = {}
for side in ('official', 'sidecar'):
    core = [r for r in rows if T(r[f'{side}_core_member'])]
    res[side] = dict(
        cells=len(rows), q05=sum(T(r[f'{side}_main_q05']) for r in rows),
        q01=sum(T(r[f'{side}_main_q01']) for r in rows),
        core=len(core),
        enriched=sum(r[f'{side}_core_direction'].upper().startswith('ENR') for r in core),
        depleted=sum(r[f'{side}_core_direction'].upper().startswith('DEP') for r in core),
        doc_edges=sum(int(float(r[f'{side}_observed'])) for r in rows),
        raw_records=sum(int(float(r[f'{side}_raw_observed'])) for r in rows),
        depleted_pairs=sorted(f"{r['ai_family']} x {r['decision_family']}" for r in core if r[f'{side}_core_direction'].upper().startswith('DEP')))
g = list(csv.DictReader(open(gp, encoding='utf-8-sig')))
res['n_ai'] = len(ai); res['n_dec'] = len(dec); res['ai'] = ai; res['dec'] = dec
res['g_cols'] = list(g[0].keys()); res['g_rows'] = len(g)
res['sha256_csv'] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
json.dump(res, open(outp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for s in ('official', 'sidecar'):
    print(s, {k: v for k, v in res[s].items() if k != 'depleted_pairs'})
print(res['n_ai'], res['n_dec'], res['g_rows'], res['g_cols'][:8])
