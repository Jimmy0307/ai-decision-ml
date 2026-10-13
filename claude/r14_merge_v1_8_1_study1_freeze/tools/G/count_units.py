"""Row counts for V9.1 unit/eligibility files. Usage: python -I count_units.py <SEG_DIR>"""
import csv, os, sys
seg = sys.argv[1]
csv.field_size_limit(10**9)
for s in ('S1', 'S2'):
    for name in ('SEGMENT_CORPUS', 'ANALYTICAL_PAIR_ELIGIBLE_RECORDS'):
        p = os.path.join(seg, '%s_%s.csv' % (s, name))
        with open(p, encoding='utf-8-sig', newline='') as fh:
            r = csv.DictReader(fh)
            rows = list(r)
        extra = ''
        if name == 'SEGMENT_CORPUS':
            cols = r.fieldnames
            extra = ' cols=%s' % cols[:12]
        print(s, name, len(rows), extra)
