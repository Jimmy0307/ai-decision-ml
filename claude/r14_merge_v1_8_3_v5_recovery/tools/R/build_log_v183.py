"""Build 41_PATCH_LOG_v1_8_3.md and 41b_V182_TO_V183_SEGMENT_DIFF.md.
Usage: python -I build_log_v183.py <v1.8.2 md> <v1.8.3 md> <patches.json> <verify_out.json> <out_dir>"""
import sys, json, hashlib, difflib, os

A_P, B_P, PJ, VJ, OUT = sys.argv[1:6]
A = open(A_P, encoding='utf-8').read()
B = open(B_P, encoding='utf-8').read()
P = json.load(open(PJ, encoding='utf-8'))
V = json.load(open(VJ, encoding='utf-8'))
assert V['ALL_HARD_CHECKS_PASS'] is True, 'verification failed; no log built'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


for p in P:
    assert B.count(p['new']) == 1, p['id']
    p['v183_line'] = B[:B.find(p['new'])].count('\n') + 1

NUM_JUST = {
    'R02': '"35", "38", "37", "39", "40" = V1.8.3 file IDs 35–38 and 39–40; "37" (also) = count of V9 protected inputs (provenance count, unchanged baseline size); "256" = SHA-256.',
    'R03': 'Removed "12" = superseded "12 of 37 missing" provenance count. Added "256" = SHA-256; "13" = number of hash-pinned official outputs to reproduce (OUT 38 §2g). "37" retained.',
    'R05': 'Removed "12" = superseded "12 of 37 protected inputs are missing" (English abstract). "37" retained.',
    'R12': '"355" = byte length of the protected prefix of the append-only log (OUT 37 row 26); "256" = SHA-256; "37" = file ID 37.',
    'R13': '"37", "38" = V1.8.3 file IDs; "256" = SHA-256.',
    'R14': 'Removed "12" = superseded missing count. Added "256" = SHA-256. "37" retained.',
    'R15': '"74" = number of file-hash claims verified in the data-pack manifest (OUT 35 §1); "35" = file ID. The run id 20260922T010012Z is inside a single token (not split). "04_STAGE2_RUNTIME_SUMMARY" avoided as a token.',
    'R16': 'Removed "12" = superseded missing count. Added "256" = SHA-256.',
    'R24': 'Appendix D: file IDs 35, 36, 37, 38, 39, 40, 41 (and "1" from `_v1_8_3` file-name tail); section cross-references 3.8.3, 3.7.1, 3.7.4, 4.5.5, 5.8.9.',
    'R25': '"35" = file ID.',
    'R26': '"355" = protected prefix length; "256" = SHA-256; "37" = file ID.',
    'R27': '"37" (x2) = protected-input count and file ID 37; "35", "36" = file IDs; "256" = SHA-256. Old "37" and "12" (historical V1.8 package statement) retained verbatim.',
    'R28': '"256" = SHA-256.',
    'R29': '"35", "39" = file IDs 35–39.',
    'R30': 'Removed "12" = superseded missing count. Added "256" = SHA-256; "13" = pinned official outputs; "38" = file ID; "1", "2", "5" = V1.8.1 reason numbers (reason 1 lapsed; reasons 2–5 hold).',
    'R33': '"38" = file ID.',
}


def esc(s):
    return s.replace('|', '\\|').replace('\n', '⏎')


L = ['# 41 — Patch Log v1.8.2 → v1.8.3 (V5 PROVENANCE CANDIDATE)\n',
     f'- Input: `claude/r14_merge_v1_8_2_v1_prefreeze/32_MERGED_MASTER_THESIS_v1_8_2_V1_PREFREEZE_CANDIDATE.md` sha256 `{sha(A_P)}` (asserted by the patch script).',
     f'- Output: `41_MERGED_MASTER_THESIS_v1_8_3_V5_PROVENANCE_CANDIDATE.md` sha256 `{sha(B_P)}`.',
     f'- Method: `tools/R/patch_v183.py`, which applies {len(P)} exact old→new replacements. Each `old` is asserted to match exactly once in v1.8.2 and once at apply time.',
     '- Verification: `tools/R/verify_v183.py` → `tools/R/verify_out_v183.json`. This log is built by `tools/R/build_log_v183.py`, which refuses to run unless every hard check passes.',
     '- Scope: provenance and status wording only.',
     '  - Changed: the status line; every "12/37 protected inputs missing" statement; the official-core provenance; the V5 Data Pack provenance; the sidecar core and generator; the propagation rule; the HUMAN_AUDIT log hash wording; the full-reanalysis execution status; the E39/E40/E44/E48/E12 residual-limit text; and the Appendix D rows for 35–41.',
     '  - Unchanged: math, result numbers, G rows, Table 3-4/3-4A, headings, V1 design text (§3.9.3) and the Enterprise model.',
     '  - No DOCX was built.\n',
     '## Changes\n',
     '| ID | v1.8.2 line | v1.8.3 line | Section | Category | Source |', '|---|---|---|---|---|---|']
for p in P:
    L.append(f"| {p['id']} | {p['v182_line']} | {p['v183_line']} | {p['section']} | {p['category']} | {esc(p['source'])} |")
L.append('\n## Old → new text\n')
for p in P:
    L.append(f"### {p['id']} — {p['section']} (v1.8.2 L{p['v182_line']} → v1.8.3 L{p['v183_line']})\n")
    L.append(f"Source: {p['source']}\n")
    L.append('OLD:\n')
    L.append('```text\n' + p['old'] + '\n```\n')
    L.append('NEW:\n')
    L.append('```text\n' + p['new'] + '\n```\n')
L.append('## Verification summary (from verify_out_v183.json)\n')
for k, v in V['hard_checks'].items():
    L.append(f'- `{k}`: `{v}`')
for k in ['line_count', 'math_counts', 'headings', 'G_table_rows', 'G_token_counts', 'fenced_patches', 'fenced_blocks_changed',
          'term_NOT_EXECUTABLE_WITH_CURRENT_SOURCE_SET', 'term_EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION',
          'term_REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION', 'term_NOT_RECOMMENDED', 'term_PRIORITY_RATIONALE_REVIEW_REQUESTED',
          'term_RECOVERED_FROM_SIDECAR_POLICY', 'term_12 項未尋回', 'term_NOT_REQUIRED', 'term_AUTHOR TO CONFIRM']:
    L.append(f"- `{k}`: `{json.dumps(V[k], ensure_ascii=False)}`")
L.append('\nNotes:\n'
         '- The only fenced block that changed is the §3.1.1 flow diagram (R11). It changes one status phrase: "目前無法執行" → "執行條件待滿足". With R11 reversed, every fenced block is byte-identical.\n'
         '- The `[AUTHOR TO CONFIRM]` count is unchanged at 2. The §3.7.4 marker now asks whether the researcher adopts and predeclares the recovered rule, because predeclaration is still a researcher decision.\n'
         '- No result number, G token or M token changed in count.')
open(os.path.join(OUT, '41_PATCH_LOG_v1_8_3.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')

S = ['# 41b — v1.8.2 → v1.8.3 segment diff\n',
     f'Input sha256 `{sha(A_P)}`. Output sha256 `{sha(B_P)}`.\n',
     f'- Changed lines in v1.8.2: {V["changed_lines_v182"]}.',
     f'- Changed lines in v1.8.3: {V["changed_lines_v183"]}.\n',
     '## Invariants (script-verified; all must be `true`)\n']
for k, v in V['hard_checks'].items():
    S.append(f'- {k}: {v}')
S += ['\n## Numeric tokens added / removed (whole document)\n',
      f'- Added: `{json.dumps(V["numeric_added_doc"], ensure_ascii=False)}`',
      f'- Removed: `{json.dumps(V["numeric_removed_doc"], ensure_ascii=False)}`',
      f'- The per-patch deltas sum to the document delta: {V["hard_checks"]["numeric_patch_sum_matches_doc"]}.',
      f'- Added tokens outside the provenance allowlist: {V["numeric_added_not_in_allowlist"]}.\n',
      '| Patch | Added | Removed | Justification |', '|---|---|---|---|']
for pid, d in V['numeric_per_patch'].items():
    S.append(f"| {pid} | `{json.dumps(d['added'], ensure_ascii=False)}` | `{json.dumps(d['removed'], ensure_ascii=False)}` | {NUM_JUST.get(pid, 'CHECK')} |")
S.append('\nEvery added number is one of the following:\n'
         '- a file ID (35–41) or version label (1.8.2, 1.8.3);\n'
         '- "256" from "SHA-256";\n'
         '- a provenance count: 37 protected inputs, 13 pinned outputs, 74 data-pack hash claims, or the 355-byte prefix;\n'
         '- a V1.8.1 reason number (1, 2–5);\n'
         '- a section cross-reference.\n\n'
         'The only number removed is the superseded "12" (×5), from "12 of 37 missing". The historical V1.8 package statement in E39 (b) keeps its "12".\n\n'
         'No network, statistical, human-audit, synthetic or enterprise value was added or removed.\n')
S.append('## Segment diff (changed lines only)\n')
la, lb = A.split('\n'), B.split('\n')
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes():
    if tag == 'equal':
        continue
    S.append(f'### v1.8.2 L{i1 + 1}–{i2} → v1.8.3 L{j1 + 1}–{j2} ({tag})\n')
    if tag == 'insert':
        for b in lb[j1:j2]:
            S.append(f'- INSERTED: `{esc(b)}`')
    else:
        for a, b in zip(la[i1:i2], lb[j1:j2]):
            if a == b:
                continue
            for t, x1, x2, y1, y2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
                if t != 'equal':
                    S.append(f'- OLD: `{esc(a[x1:x2]) or "∅"}`\n  NEW: `{esc(b[y1:y2]) or "∅"}`')
        for b in lb[j1 + (i2 - i1):j2]:
            S.append(f'- INSERTED: `{esc(b)}`')
    S.append('')
open(os.path.join(OUT, '41b_V182_TO_V183_SEGMENT_DIFF.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(S) + '\n')
print('ok', sha(os.path.join(OUT, '41_PATCH_LOG_v1_8_3.md')), sha(os.path.join(OUT, '41b_V182_TO_V183_SEGMENT_DIFF.md')))
