"""Build 40_STUDY1_FREEZE_HASHES_v1_8_3.csv (same columns as V1.8.1 18_STUDY1_FREEZE_HASHES.csv).
Re-verifies every 18 row at its current path, replaces NOT_RECOVERED rows with recovered files, adds V5 chain
anchors and V1.8.3 evidence files. Read-only on all inputs; stdlib only.
Usage: python -I build_hashes_v183.py <repo root> <out csv> <summary json>"""
import sys, csv, json, hashlib, os

REPO, OUT_CSV, OUT_JSON = sys.argv[1:4]
W = r"C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\03_R14_STUDY1\01_SOURCE_CLOSURE_V1_8"
V5 = r"C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\04_V5_PRODUCTION_FREEZE\20260911_AI_DECISION_V5_PRODUCTION"
SC = r"C:\NTUST_PAPER\outputs\10_CANONICAL_EVIDENCE\01_V9_HUMAN_VALIDATION\20261003_V9_HUMAN_AUDIT_FINAL_CONVERGENCE_SIDECAR_20261003T192417"
OLD_R14_DOCX = r"C:\NTUST_PAPER\V9_FINAL_SUBMISSION_CANDIDATE_20261004.docx"
NEW_R14_DOCX = r"C:\NTUST_PAPER\outputs\80_HISTORY_2026\10_OCT\ROOT_V9_FINAL_SUBMISSION_CANDIDATES_20261004\V9_FINAL_SUBMISSION_CANDIDATE_20261004.docx"
L18 = os.path.join(REPO, 'claude', 'r14_merge_v1_8_1_study1_freeze', '18_STUDY1_FREEZE_HASHES.csv')
C37 = os.path.join(REPO, 'claude', 'r14_merge_v1_8_3_v5_recovery', '37_PROTECTED_INPUT_RECOVERY.csv')
OUTD = 'claude/r14_merge_v1_8_3_v5_recovery'
COLS = ['artifact', 'path', 'layer', 'status', 'sha256', 'bytes', 'note']


def resolve(p):
    if p.startswith('repo:'):
        return os.path.join(REPO, *p[5:].split('/'))
    if p.startswith('W:'):
        return os.path.join(W, *p[2:].split('/'))
    return p


def h(path, nbytes=None):
    d = hashlib.sha256()
    n = 0
    with open(path, 'rb') as f:
        while True:
            want = 1 << 20 if nbytes is None else min(1 << 20, nbytes - n)
            if want <= 0:
                break
            b = f.read(want)
            if not b:
                break
            d.update(b)
            n += len(b)
    return d.hexdigest(), n


rows, checks = [], []


def emit(artifact, path, layer, status, real, expect=None, note='', prefix=None):
    sha, n = h(real, prefix)
    ok = True
    if expect:
        ok = sha.startswith(expect)
    checks.append(dict(artifact=artifact, ok=ok, expect=expect, sha256=sha))
    rows.append(dict(artifact=artifact, path=path, layer=layer, status=status if ok else 'MISMATCH', sha256=sha, bytes=n,
                     note=note if ok else f'MISMATCH vs expected {expect}; ' + note))


# ---- A. carry over the 18 rows ----------------------------------------------------
old = list(csv.DictReader(open(L18, encoding='utf-8')))
replaced = []
for r in old:
    if r['status'] == 'NOT_RECOVERED':
        replaced.append(r)
        continue
    p = r['path']
    if p == OLD_R14_DOCX:
        emit(r['artifact'], NEW_R14_DOCX, r['layer'], r['status'], NEW_R14_DOCX, r['sha256'],
             'path moved by V1.8.2a reorganization (33 §2); re-verified v1.8.3; ' + r['note'])
        continue
    note = 're-verified v1.8.3 at current path' + ('; W = ' + W + ' (moved by V1.8.2a, 33 §2)' if p.startswith('W:') else '')
    if r['note']:
        note += '; ' + r['note']
    emit(r['artifact'], p, r['layer'], r['status'], resolve(p), r['sha256'], note)
    assert int(r['bytes']) == rows[-1]['bytes'], r['artifact']

# ---- B. replacements for NOT_RECOVERED rows ------------------------------------------------
core = V5 + r"\13_RESULTS_FREEZE\results_freeze_v1_20260919T080120Z\FINAL_ROBUST_CORE_32.csv"
emit('Official final core file (R14/V9 freeze)', core, 'UPSTREAM_CANONICAL', 'CONFIRMED', core,
     'a43b4b5897bb8b1dabfe251aa52b95da8f35b6951c98ada7c92663291770bd50',
     'was NOT_RECOVERED/PROBABLE in 18; V5 13_RESULTS_FREEZE (LATEST run 080120Z); full SHA-256 = recorded value; manifest chain verified (35 §2); 16 identical copies (37)')
for r in replaced:
    if r['artifact'].startswith('r14/04_G01_G16_FROZEN'):
        rows.append(dict(r, note=r['note'] + '; unchanged in v1.8.3: outside recovery scope; name search of C:\\NTUST_PAPER found no file'))
        checks.append(dict(artifact=r['artifact'], ok=True, expect=None, sha256=''))
    elif r['artifact'].startswith('R14 canonical docx'):
        rows.append(dict(r, note=r['note'] + '; unchanged in v1.8.3; identity candidate = V9_FINAL_SUBMISSION_CANDIDATE_20261004.docx row above (full sha f4252f76…3ff6)'))
        checks.append(dict(artifact=r['artifact'], ok=True, expect=None, sha256=''))

prot = list(csv.DictReader(open(C37, encoding='utf-8')))
for r in prot:
    if r['row'] == 'S1':
        continue
    if r['v1_8_status'].startswith('NOT_RECOVERED'):
        name = r['baseline_path'].split('/')[-1]
        emit(f"V9 protected input row {r['row']}: {name}", r['primary_path'], 'V9_PROTECTED_INPUT', 'CONFIRMED',
             r['primary_path'], r['sha256'],
             'one of the 12/37 NOT_RECOVERED in V1.8 02 §5 / 18; full SHA-256 = PROTECTED_ARTIFACTS_BASELINE_20261003.csv value (37)')
    elif r['row'] == '26':
        logp = W + r"\02_V9_HUMAN_VALIDATION\20260929_V9_HUMAN_VALIDATION\HUMAN_AUDIT_APPEND_ONLY_LOG.csv"
        emit('V9 protected input row 26: HUMAN_AUDIT_APPEND_ONLY_LOG.csv (protected state)', logp, 'V9_PROTECTED_INPUT', 'CONFIRMED',
             logp, r['sha256'],
             'sha256/bytes are of byte prefix [0,355) of the current 625-byte append-only log (whole-file sha 151cf3d0…); protected state verified as prefix of append-only log; V9 LEGACY_AUDIT_LOG_INTEGRITY=UNVERIFIED is historical (37 §3)',
             prefix=int(r['bytes']))
sidecar_core = SC + r"\V5_CORRECTED\13_RESULTS_FREEZE\results_freeze_v1_20261003T115651Z\FINAL_ROBUST_CORE_32.csv"
emit('Sidecar core file', sidecar_core, 'V9_SIDECAR', 'CONFIRMED', sidecar_core,
     '4e412a07af1f5c9e2f304408875fc1fc47018c9ff501a17dee437bea880e95a0',
     'was NOT_SHIPPED/NOT_RECOVERED; full SHA-256 = V9 FINAL_STATUS.json sidecar_core_sha256; 32 = 15 enriched + 17 depleted (37 §6)')
emit('Sidecar generator script', SC + r"\prepare_and_run_corrected_sidecar.py", 'V9_SIDECAR', 'PROBABLE',
     SC + r"\prepare_and_run_corrected_sidecar.py", '021e3d10c8a1085bdae57df9a964a9416a61b4cf68acb1e33360448fd6463ef3',
     'was NOT_RECOVERED; location and self-consistent outputs fit, but no V9 artifact pins this script hash (38 §2e); not executed')
emit('Sidecar label-handling policy (propagation rule E48)', SC + r"\LOCAL_HUMAN_CORRECTION_POLICY.md", 'V9_SIDECAR', 'PROBABLE',
     SC + r"\LOCAL_HUMAN_CORRECTION_POLICY.md", '33d4d44c2d1940dc34498cbe1a13266ad20d9b668d3e420d1c4de1840200940a',
     'PROPAGATION_RULE=RECOVERED_FROM_SIDECAR_POLICY_PENDING_PREDECLARATION; rule re-derived 50/50 actions, pair-eligible delta -18 (38 §2f); file hash not pinned by V9')
emit('Sidecar correction map (50 rows)', SC + r"\HUMAN_AUDIT_LOCAL_CORRECTION_MAP.csv", 'V9_SIDECAR', 'CONFIRMED',
     SC + r"\HUMAN_AUDIT_LOCAL_CORRECTION_MAP.csv", 'd09db24472c060e723f52acf6ef7ea26918368d9189f288efb6b8ce94d493313',
     '= corrections_map_sha256 pinned in CORRECTED_SIDECAR_OUTPUTS.json (38 §2e)')

# ---- C. V5 chain anchors (not already listed) ---------------------------------------------
listed = {r['path'] for r in rows}
AF = V5 + r"\09_ANALYTICAL_FREEZE\analytical_freeze_v2_20260918T132206Z"
anchors = [
    ('V5 06 evidence freeze report', V5 + r"\06_STATUS\V5_EVIDENCE_FREEZE_REPORT.json", 'faecdf67', 'verdict V5_EVIDENCE_CORPUS_FROZEN; cited by 07 and 14 (35 §2)'),
    ('V5 07 analytical scope manifest (stage 2)', V5 + r"\07_FSC_STAGE2_STRICT_V102\ANALYTICAL_SCOPE_MANIFEST.json", '80a953ff', 'formal_scope payload f763039d recomputed (35 §1a)'),
    ('V5 09 analytical freeze canonical', AF + r"\ANALYTICAL_FREEZE_CANONICAL.json", '9a4e8fc2', 'chain 09 -> 10 (35 §2)'),
    ('V5 09 analytical freeze manifest v2', AF + r"\ANALYTICAL_FREEZE_MANIFEST_V2.json", '69c7a7df', 'lineage pins source DB, stage-2 sqlite, definitions'),
    ('V5 09 analytical freeze record level (6,499 strict records)', AF + r"\ANALYTICAL_FREEZE_RECORD_LEVEL.csv", 'fbb5f592', '6,499 / 3,125 / 783 recomputed (36 §A)'),
    ('V5 09 pair-eligible records (3,125)', AF + r"\ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv", '9ee5fd53', '36 §A'),
    ('V5 10 dedup matrix canonical', V5 + r"\10_DOCUMENT_DEDUP_MATRIX\matrix_v1_20260918T132505Z\DOCUMENT_DEDUP_MATRIX_CANONICAL.json", 'd816f34a', 'chain 10 -> 11, 12'),
    ('V5 10 dedup matrix manifest', V5 + r"\10_DOCUMENT_DEDUP_MATRIX\matrix_v1_20260918T132505Z\DOCUMENT_DEDUP_MATRIX_MANIFEST.json", None, 'manifest: 3/3 verified (35 §1)'),
    ('V5 10 document pair edges dedup (M = 2,180)', V5 + r"\10_DOCUMENT_DEDUP_MATRIX\matrix_v1_20260918T132505Z\DOCUMENT_PAIR_EDGES_DEDUP.csv", '3ba370c1', 'not manifest-hashed; edge set = canonical (36 §A); pinned by sidecar baseline reproduction'),
    ('V5 11 null model canonical', V5 + r"\11_NULL_MODEL_NETWORK\null_model_v1_20260918T132933Z\NULL_MODEL_NETWORK_CANONICAL.json", '682a58f7', 'chain 11 -> 12, 13'),
    ('V5 11 null model manifest', V5 + r"\11_NULL_MODEL_NETWORK\null_model_v1_20260918T132933Z\NULL_MODEL_NETWORK_MANIFEST.json", None, 'manifest: 3/3 verified; seed 20260918, 10,000 replicates'),
    ('V5 12 robustness canonical', V5 + r"\12_ROBUSTNESS_SENSITIVITY\robustness_v1_20260918T133618Z\ROBUSTNESS_SENSITIVITY_CANONICAL.json", '8c0441ce', 'chain 12 -> 13'),
    ('V5 12 robustness manifest', V5 + r"\12_ROBUSTNESS_SENSITIVITY\robustness_v1_20260918T133618Z\ROBUSTNESS_SENSITIVITY_MANIFEST.json", None, 'manifest: 5/5 verified'),
    ('V5 13 results freeze canonical', V5 + r"\13_RESULTS_FREEZE\results_freeze_v1_20260919T080120Z\FINAL_RESULTS_FREEZE_CANONICAL.json", 'b1d8b5ee', 'chain 13 -> 14'),
    ('V5 13 results freeze manifest', V5 + r"\13_RESULTS_FREEZE\results_freeze_v1_20260919T080120Z\FINAL_RESULTS_FREEZE_MANIFEST.json", 'f156f775', 'manifest: 5/5 verified; also V9 protected row 16'),
    ('V5 13 robust depleted (G01-G16 set)', V5 + r"\13_RESULTS_FREEZE\results_freeze_v1_20260919T080120Z\FINAL_ROBUST_DEPLETED.csv", '6e25d75c', '16 = G01-G16 set (36 §B)'),
    ('V5 14 manuscript data pack manifest (LATEST 010012Z)', V5 + r"\14_MANUSCRIPT_DATA_PACK\data_pack_v1_20260922T010012Z\MANUSCRIPT_DATA_PACK_MANIFEST.json", '28c5b631', 'REAL_V5_DATA_PACK=RECOVERED; 74/74 claims verified (35 §1); superseded 081003Z pack not used'),
    ('V5 14 manuscript data pack zip (LATEST 010012Z)', V5 + r"\14_MANUSCRIPT_DATA_PACK\AI_DECISION_V5_MANUSCRIPT_DATA_PACK_20260922T010012Z.zip", 'fdf7cd89', 'all members equal directory files (35 §3)'),
    ('V5 14 stage-2 runtime summary (model digest 7cdf5a01...)', V5 + r"\14_MANUSCRIPT_DATA_PACK\data_pack_v1_20260922T010012Z\04_STAGE2_RUNTIME_SUMMARY.json", 'a4111914', 'manifest-listed; qwen2.5:14b digest cited in manuscript 3.8.3'),
]
for art, p, exp, note in anchors:
    if p in listed:
        continue
    emit(art, p, 'V5_PRODUCTION_CHAIN', 'CONFIRMED', p, exp, note + '; manifest chain VERIFIED 201/203 (2 superseded-pack re-saves off core path)')

# ---- D. V1.8.3 evidence files --------------------------------------------------------------
ev = ['35_V5_MANIFEST_CHAIN_VERIFICATION.md', '35_V5_MANIFEST_CHAIN.csv', '35_v5_manifest_chain_raw.json',
      '36_V5_BASELINE_RECOMPUTATION.md', '36_V5_BASELINE_RECOMPUTATION.json', '37_PROTECTED_INPUT_RECOVERY.md',
      '37_PROTECTED_INPUT_RECOVERY.csv', '38_FULL_REANALYSIS_FEASIBILITY.md', '39_STUDY1_FREEZE_PROVENANCE_ADDENDUM_v1_8_3.md',
      '41_MERGED_MASTER_THESIS_v1_8_3_V5_PROVENANCE_CANDIDATE.md', '41_PATCH_LOG_v1_8_3.md', '41b_V182_TO_V183_SEGMENT_DIFF.md',
      'tools/R/patch_v183.py', 'tools/R/verify_v183.py', 'tools/R/build_log_v183.py', 'tools/R/build_hashes_v183.py',
      'tools/R/verify_out_v183.json']
for f in ev:
    p = 'repo:' + OUTD + '/' + f
    emit(f'V1.8.3 {f}', p, 'V1_8_3_EVIDENCE', 'PRESENT', resolve(p), None, 'this round (uncommitted at hashing time)')

with open(OUT_CSV, 'w', encoding='utf-8', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=COLS, lineterminator='\n')
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, '') for k in COLS})
summary = dict(rows=len(rows), carried_from_18=len(old) - len(replaced), replaced_not_recovered=len(replaced),
               mismatches=[c for c in checks if not c['ok']],
               status_counts={s: sum(1 for r in rows if r['status'] == s) for s in sorted({r['status'] for r in rows})},
               layer_counts={s: sum(1 for r in rows if r['layer'] == s) for s in sorted({r['layer'] for r in rows})})
json.dump(summary, open(OUT_JSON, 'w', encoding='utf-8'), indent=1)
print(json.dumps(summary, indent=1))
sys.exit(1 if summary['mismatches'] else 0)
