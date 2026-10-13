"""Check full_sensitivity_robust flag == (all four q<=.05 and same direction) for baseline/S1/S2.
Usage: python -I verify_membership_rule.py <V9_1_SEGMENTATION_SENSITIVITY_DIR>"""
import csv, glob, os, sys
seg = sys.argv[1]
paths = {'baseline': glob.glob(os.path.join(seg, '_baseline_reproduction/12_ROBUSTNESS_SENSITIVITY/*/ROBUSTNESS_COMPARISON_120.csv'))[0],
         'S1': os.path.join(seg, 'S1_120_CELL_RESULTS.csv'), 'S2': os.path.join(seg, 'S2_120_CELL_RESULTS.csv')}
M = ('main_mc', 'exact', 'document_null', 'raw')
for lab, p in paths.items():
    with open(p, encoding='utf-8-sig', newline='') as fh:
        rs = list(csv.DictReader(fh))
    bad_flag = bad_q = 0
    n = 0
    for r in rs:
        rule = all(float(r[m + '_q']) <= 0.05 for m in M) and len({r[m + '_direction'] for m in M}) == 1
        n += rule
        bad_flag += rule != (r['full_sensitivity_robust'].lower() == 'true')
        bad_q += sum((float(r[m + '_q']) <= 0.05) != (r[m + '_q05'].lower() == 'true') for m in M)
    print(lab, 'rule_core', n, 'flag_mismatch', bad_flag, 'q05_flag_mismatch', bad_q)
