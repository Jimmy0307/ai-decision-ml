"""Recompute V9.1 re-segmentation figures and G01-G16 S1/S2 status from raw rows.

Usage: python -I recompute_seg.py <V9_PACKAGE_DIR> <G01_G16_CSV> <W132_CSV> <OUT_JSON>
Read-only on all inputs; writes one machine-readable JSON and prints a summary.
"""
import csv
import glob
import hashlib
import json
import os
import sys
from collections import Counter

METHODS = ('main_mc', 'exact', 'document_null', 'raw')


def rows(path):
    with open(path, encoding='utf-8-sig', newline='') as fh:
        return list(csv.DictReader(fh))


def sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def is_true(value):
    return str(value).strip().lower() == 'true'


def cell(row):
    return (row['ai_family'], row['decision_family'])


def one(seg, pattern):
    hits = glob.glob(os.path.join(seg, pattern))
    if len(hits) != 1:
        raise SystemExit('expected exactly 1 match for %s, got %r' % (pattern, hits))
    return hits[0]


def variant_summary(s, cells, res, edge_counts, core):
    base_core = core['baseline']
    changed = [c for c in cells if edge_counts[s].get(c, 0) != edge_counts['baseline'].get(c, 0)]
    dirchg = [c for c in cells if res[s][c]['main_mc_direction'] != res['baseline'][c]['main_mc_direction']]
    retained = [c for c in base_core if c in core[s]]
    return {
        'observed_count_changed_cells': len(changed),
        'main_direction_changed_cells': len(dirchg),
        'core_size': len(core[s]),
        'core_enriched': sum(v == 'ENRICHED' for v in core[s].values()),
        'core_depleted': sum(v == 'DEPLETED' for v in core[s].values()),
        'baseline_core_retained': len(retained),
        'baseline_enriched_retained': sum(base_core[c] == 'ENRICHED' for c in retained),
        'baseline_depleted_retained': sum(base_core[c] == 'DEPLETED' for c in retained),
        'retained_direction_reversals': sum(core[s][c] != base_core[c] for c in retained),
        'entered': [' x '.join(c) for c in sorted(set(core[s]) - set(base_core))],
        'exited': [' x '.join(c) for c in sorted(set(base_core) - set(core[s]))],
        'q05_counts_main_exact_doc_raw': {m: sum(is_true(res[s][c][m + '_q05']) for c in cells) for m in METHODS},
        'jaccard_vs_baseline': round(len(retained) / len(set(base_core) | set(core[s])), 3),
        'edges': sum(edge_counts[s].values()),
    }


def main():
    v9, gcsv, w132_path, outj = sys.argv[1:5]
    seg = os.path.join(v9, 'V9_1_SEGMENTATION_SENSITIVITY')
    files = {
        'baseline_edges': one(seg, '_baseline_reproduction/10_DOCUMENT_DEDUP_MATRIX/*/DOCUMENT_PAIR_EDGES_DEDUP.csv'),
        'baseline_120': one(seg, '_baseline_reproduction/12_ROBUSTNESS_SENSITIVITY/*/ROBUSTNESS_COMPARISON_120.csv'),
        'baseline_null': one(seg, '_baseline_reproduction/11_NULL_MODEL_NETWORK/*/CELL_NULL_MODEL_RESULTS_120.csv'),
        'baseline_core32': one(seg, '_baseline_reproduction/13_RESULTS_FREEZE/*/FINAL_ROBUST_CORE_32.csv'),
        'S1_edges': os.path.join(seg, 'S1_DOCUMENT_EDGES.csv'),
        'S2_edges': os.path.join(seg, 'S2_DOCUMENT_EDGES.csv'),
        'S1_120': os.path.join(seg, 'S1_120_CELL_RESULTS.csv'),
        'S2_120': os.path.join(seg, 'S2_120_CELL_RESULTS.csv'),
        'cell_diff': os.path.join(seg, 'SEGMENTATION_CELL_COUNT_DIFF.csv'),
        'cand_manifest': os.path.join(seg, 'SEGMENTATION_CANDIDATE_MANIFEST.csv'),
        'local_label_sens': os.path.join(v9, 'ROBUST_CORE_LOCAL_SENSITIVITY.csv'),
        'g01_g16': gcsv,
        'w132': w132_path,
    }
    out = {'inputs': {k: {'path': p, 'sha256': sha(p)} for k, p in files.items()}}

    edge_counts = {lab: Counter(cell(r) for r in rows(files[lab + '_edges'])) for lab in ('baseline', 'S1', 'S2')}
    res = {lab: {cell(r): r for r in rows(files[lab + '_120'])} for lab in ('baseline', 'S1', 'S2')}
    cells = sorted(res['baseline'])
    if len(cells) != 120 or any(len(res[s]) != 120 for s in res):
        raise SystemExit('120-cell invariant violated')
    out['edge_vs_120_check'] = {
        lab: {'edges_total': sum(edge_counts[lab].values()),
              'cells_120_vs_edges_mismatch': sum(int(res[lab][c]['dedup_observed']) != edge_counts[lab].get(c, 0) for c in cells)}
        for lab in res}

    core = {lab: {c: res[lab][c]['main_mc_direction'] for c in cells if is_true(res[lab][c]['full_sensitivity_robust'])}
            for lab in res}
    summary = {s: variant_summary(s, cells, res, edge_counts, core) for s in ('S1', 'S2')}
    base_core = core['baseline']
    summary['baseline'] = {
        'core_size': len(base_core), 'edges': sum(edge_counts['baseline'].values()),
        'core_enriched': sum(v == 'ENRICHED' for v in base_core.values()),
        'q05_counts_main_exact_doc_raw': {m: sum(is_true(res['baseline'][c][m + '_q05']) for c in cells) for m in METHODS}}
    summary['persistent_all_3_same_direction'] = sum(
        1 for c in base_core if core['S1'].get(c) == base_core[c] and core['S2'].get(c) == base_core[c])
    summary['S1_vs_S2_jaccard'] = round(len(set(core['S1']) & set(core['S2'])) / len(set(core['S1']) | set(core['S2'])), 3)
    core32 = {cell(r): r['direction'] for r in rows(files['baseline_core32'])}
    summary['baseline_core_equals_frozen_core32_file'] = core32 == base_core
    diff = {cell(r): r for r in rows(files['cell_diff'])}
    summary['packaged_diff_file_check'] = {s: {
        'count_changed_from_diff': sum(int(diff[c][s.lower() + '_count_delta']) != 0 for c in cells),
        'dir_changed_from_diff': sum(is_true(diff[c][s.lower() + '_direction_changed']) for c in cells)}
        for s in ('S1', 'S2')}
    cand = rows(files['cand_manifest'])
    summary['candidates'] = {'strict_records': len(cand), 'candidate_true': sum(is_true(r['candidate']) for r in cand)}
    out['summary'] = summary

    w132 = {r['G ID']: r for r in rows(files['w132'])}
    nul = {cell(r): r for r in rows(files['baseline_null'])}
    loc = {cell(r): r for r in rows(files['local_label_sens'])}
    gout = {}
    for g in rows(files['g01_g16']):
        c = (g['AI_Family'], g['Decision_Family'])
        w = w132[g['Gap_ID']]
        lr = loc[c]
        d = {
            'pair': ' x '.join(c),
            'w132_pair_match': (w['AI family'], w['Decision family']) == c,
            'w132_persistence_tag': w['Evidence-unit persistence'],
            'frozen_O': g['Observed'], 'frozen_E': g['E_analytic'], 'frozen_OE': g['O_E_Ratio'],
            'frozen_q_main_exact_doc_raw': [g['q_primary_BH'], g['q_exact'], g['q_document_preserving'], g['q_raw_record']],
            'baseline_recomputed_O_from_edges': edge_counts['baseline'].get(c, 0),
            'baseline_E_independence': nul[c]['independence_expected'],
            'baseline_core': c in base_core, 'baseline_dir': base_core.get(c),
            'baseline_q': {m: res['baseline'][c][m + '_q'] for m in METHODS},
            'official_v9_local_csv': {k: lr[k] for k in (
                'official_observed', 'official_main_direction', 'official_core_member', 'official_core_direction',
                'official_main_q', 'official_exact_q', 'official_document_q', 'official_raw_q')},
            'local_label_sidecar': {k: lr[k] for k in (
                'sidecar_observed', 'sidecar_core_member', 'sidecar_core_direction', 'sidecar_main_q',
                'sidecar_exact_q', 'sidecar_document_q', 'sidecar_raw_q', 'core_membership_changed')},
        }
        for s in ('S1', 'S2'):
            r = res[s][c]
            d[s] = {'O_from_edges': edge_counts[s].get(c, 0), 'raw_observed': r['raw_observed'],
                    'core': c in core[s], 'core_dir': core[s].get(c),
                    'q': {m: r[m + '_q'] for m in METHODS},
                    'directions': {m: r[m + '_direction'] for m in METHODS},
                    'methods_q_gt_05': [m for m in METHODS if not is_true(r[m + '_q05'])]}
        gout[g['Gap_ID']] = d
    out['G'] = gout
    out['G_not_in_core'] = {s: [k for k, v in gout.items() if not v[s]['core']] for s in ('S1', 'S2')}
    with open(outj, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(json.dumps({'edge_vs_120_check': out['edge_vs_120_check'], 'summary': summary,
                      'G_not_in_core': out['G_not_in_core']}, ensure_ascii=False, indent=1))
    for k in ('G07', 'G15'):
        print(k, json.dumps(gout[k], ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
