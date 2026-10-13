"""Build 32_PATCH_LOG_v1_8_2.md and 32b_V181_TO_V182_SEGMENT_DIFF.md.
Usage: python -I build_log_v182.py <v1.8.1 md> <v1.8.2 md> <patches.json> <verify_out.json> <out_dir>"""
import sys, json, hashlib, difflib, os

A_P, B_P, PJ, VJ, OUT = sys.argv[1:6]
A = open(A_P, encoding='utf-8').read()
B = open(B_P, encoding='utf-8').read()
P = json.load(open(PJ, encoding='utf-8'))
V = json.load(open(VJ, encoding='utf-8'))
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
for p in P:
    assert B.count(p['new']) == 1, p['id']
    p['v182_line'] = B[:B.find(p['new'])].count('\n') + 1

NUM_JUST = {
    'K01': 'version label 1.8.2 / 1.8.1 (no numeric delta beyond labels).',
    'K02': '"19", "21" = v1.8.1 file IDs 19–21; "24", "25", "30" = v1.8.2 file IDs 24 and 25–30 (design parameters / artifact IDs).',
    'K05': '"24", "29" = file IDs 24–29; "256" = SHA-256; "32" = 32-cell scope statement (D-14); "53" (x5) = protocol name 53B (OA-2 wording, continuity metric names); '
           '"6", "7", "8" = new enumerated design items (6)–(8); "3.9.4" = cross-reference. Removed: one ".800" and one ".667" (old "(.800／.667 兩個門檻依 Krippendorff, 2004 ...)" provenance clause, replaced by research-convention statement; thresholds still stated once each), '
           'one "2004" (same clause; Krippendorff 2004 citation retained for α). Retained from old: 16, 5,000, 95, .800, .667, 1960, 2004.',
    'K06': '"16" (x2), "13" = 16-item vs 13-item sensitivity design (29 §6.1).',
    'K07': '"16" = 16 items; "95" = 95% bootstrap CI; ".667" = α < .667 UNRESOLVED/NOT_ACCEPTABLE threshold (D-7). Removed "2004" = threshold attribution "依 Krippendorff, 2004" replaced by research-convention label (29 §3); α citation Krippendorff 2004 retained.',
    'K12': '"1", "2", "3" = coder labels in pairwise pairs 1–2, 1–3, 2–3; "53" (x2) = 53B continuity section name. Removed "60" = superseded analyzer filename prefix.',
    'K13': '"1", "2", "3" = coder column labels. Removed "4" = old "manifest stage 4"; "60" = superseded analyzer.',
    'K14': 'Removed "60" = superseded analyzer filename prefix.',
    'K15': '"53" (x3) = 53B (section name + OA-2 verbatim sentence); "4-13" = cross-reference to Table 4-13.',
    'K18': 'file IDs 24–30, 32, 20 (20_MASTER_PACKET_v1_8_2.xlsx); "2", "3" = decision labels OA-2／OA-3; section refs 3.9.3, 4.7.3.',
    'K19': '"25", "26", "29" = v1.8.2 file IDs.',
}


def esc(s):
    return s.replace('|', '\\|').replace('\n', '⏎')


L = []
L.append('# 32 — Patch Log v1.8.1 → v1.8.2 (V1 PREFREEZE CANDIDATE)\n')
L.append(f'- Input: `claude/r14_merge_v1_8_1_study1_freeze/16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.md` sha256 `{sha(A_P)}` (asserted).')
L.append(f'- Output: `32_MERGED_MASTER_THESIS_v1_8_2_V1_PREFREEZE_CANDIDATE.md` sha256 `{sha(B_P)}`.')
L.append(f'- Method: `tools/K/patch_v182.py` — {len(P)} exact old→new replacements, each asserted to match exactly once in v1.8.1 and once at apply time. Verification: `tools/K/verify_v182.py` → `tools/K/verify_out.json`. This log: `tools/K/build_log_v182.py`.')
L.append('- Scope: V1 design/status wording only. No equation, network value, G01–G16 row, G→M researcher assignment, VCP/VSC/DL/NEV, enterprise model, Study 1 freeze statement, heading, or result was changed. No human result, simulated value or expected α/κ was inserted. No DOCX built.\n')
L.append('## Changes\n')
L.append('| ID | v1.8.1 line | v1.8.2 line | Section | Category | Source |')
L.append('|---|---|---|---|---|---|')
for p in P:
    L.append(f"| {p['id']} | {p['v181_line']} | {p['v182_line']} | {p['section']} | {p['category']} | {esc(p['source'])} |")
L.append('\n## Old → new text\n')
for p in P:
    L.append(f"### {p['id']} — {p['section']} (v1.8.1 L{p['v181_line']} → v1.8.2 L{p['v182_line']})\n")
    L.append(f"Source: {p['source']}\n")
    L.append('OLD:\n')
    L.append('```text\n' + p['old'].rstrip('\n') + '\n```\n')
    L.append('NEW:\n')
    L.append('```text\n' + p['new'].rstrip('\n') + '\n```\n')
L.append('## Verification summary (from verify_out.json)\n')
keys = ['line_count', 'math_identical_ordered', 'fenced_blocks_identical', 'equation_tags_identical', 'changed_lines_with_math_markers',
        'headings', 'table_figure_captions_identical', 'G_table_rows', 'section_3_9_2_tables_3_4_and_3_4A_identical',
        'section_4_7_1_table_4_11_identical', 'section_4_7_2_table_4_12_identical', 'section_4_7_4_EAX_identical',
        'section_3_9_5_identical', 'EAX_paragraph_3_9_3_unchanged', 'G_token_counts', 'G_tokens_per_patch',
        'GM_arrow_tokens_identical', 'count_VCP', 'count_VSC', 'count_DL', 'count_NEV', 'count_Enterprise', 'count_Study 1',
        'count_M5', 'count_HUMAN_RESULT_PENDING', 'result_like_tokens_added', 'oa2_sentence_count_v182',
        'leak_item_ids_v182', 'leak_seed_like_v182', 'numeric_patch_sum_matches_doc', 'numeric_added_not_in_allowlist']
for k in keys:
    L.append(f"- `{k}`: `{json.dumps(V[k], ensure_ascii=False)}`")
L.append('\nNotes: `G_token_counts` rises by 3 only because K06 adds the sentence naming G04、G10、G11 as predeclared sensitivity targets (allowed edit 3); no G row or G→M assignment changed. '
         '`count_M5` falls by 2 because the old §3.9.3 instrument text "M1–M5" (twice) was replaced by the v1.8.2 flat Q2 categories (M1–M4, LONGITUDINAL, …); M5 elsewhere is unchanged. '
         '`count_HUMAN_RESULT_PENDING` rises by 3 because Table 4-13/4-14 placeholders were restructured to the 3-coder design (all cells pending).')
open(os.path.join(OUT, '32_PATCH_LOG_v1_8_2.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')

# ---- 32b segment diff ----
S = ['# 32b — v1.8.1 → v1.8.2 segment diff\n',
     f'Input sha256 `{sha(A_P)}`; output sha256 `{sha(B_P)}`. Changed lines v1.8.1: {V["changed_lines_v181"]}; v1.8.2: {V["changed_lines_v182"]}.\n',
     '## Invariants (script-verified)\n',
     f'- Math spans byte-identical (ordered, $$ / inline $ / \\[\\] / begin-env): {V["math_identical_ordered"]}; equation \\tag set identical: {V["equation_tags_identical"]}; changed lines with math markers: {V["changed_lines_with_math_markers"]}.',
     f'- Heading list identical: {V["headings"]}.',
     f'- G-table rows (`| G01`…`| G16`) identical in order: {V["G_table_rows"]}.',
     f'- §3.9.2 (Tables 3-4 and 3-4A) byte-identical: {V["section_3_9_2_tables_3_4_and_3_4A_identical"]}; Table 4-11 section identical: {V["section_4_7_1_table_4_11_identical"]}; G→M arrow tokens identical: {V["GM_arrow_tokens_identical"]}.',
     f'- §3.9.5, §4.7.2 (AI pilot table), §4.7.4 (EA-X) and the §3.9.3 EA-X paragraph unchanged: {V["section_3_9_5_identical"]}, {V["section_4_7_2_table_4_12_identical"]}, {V["section_4_7_4_EAX_identical"]}, {V["EAX_paragraph_3_9_3_unchanged"]}.',
     f'- VCP/VSC/DL/NEV/Enterprise/Study 1 counts unchanged: VCP {V["count_VCP"]}, VSC {V["count_VSC"]}, DL {V["count_DL"]}, NEV {V["count_NEV"]}, Enterprise {V["count_Enterprise"]}, Study 1 {V["count_Study 1"]}.',
     f'- No human result inserted: result-like tokens added = {V["result_like_tokens_added"]}; all new V1 result cells are `[HUMAN RESULT PENDING]`.',
     f'- Public-repo sealing: ITEM-ID tokens in manuscript = {V["leak_item_ids_v182"]}; no item↔G pairing, order list or seed.',
     f'- OA-2 verbatim sentence occurrences: {V["oa2_sentence_count_v182"]} (§3.9.3 item 6; §4.7.3 Table 4-15 rule).\n',
     '## Numeric tokens added / removed (whole document)\n',
     f'- Added: `{json.dumps(V["numeric_added_doc"], ensure_ascii=False)}`',
     f'- Removed: `{json.dumps(V["numeric_removed_doc"], ensure_ascii=False)}`',
     f'- Sum of per-patch deltas equals document delta: {V["numeric_patch_sum_matches_doc"]}. Tokens outside the design-parameter allowlist: {V["numeric_added_not_in_allowlist"]}.\n',
     '| Patch | Added | Removed | Justification |', '|---|---|---|---|']
for pid, d in V['numeric_per_patch'].items():
    S.append(f"| {pid} | `{json.dumps(d['added'], ensure_ascii=False)}` | `{json.dumps(d['removed'], ensure_ascii=False)}` | {NUM_JUST.get(pid, '')} |")
S.append('\nAll added numbers are design parameters (3 coders, 16 items, 13-item sensitivity, .800/.667, 95%, 5,000), file/artifact IDs (19–32), protocol names (53B), SHA-256, coder labels 1–3, or cross-references. No empirical, synthetic or network value was added or removed.\n')
S.append('## Remaining "兩位編碼者" / two-coder mentions (all intentional; none is a V1 design statement)\n')
S.append('| Pattern | v1.8.2 line | Context | Why kept |')
S.append('|---|---|---|---|')
why = {591: 'Study 1 literature human audit (V9), not V1', 946: 'ORG-V study (organization coding), not V1',
       948: 'ORG-V study, not V1', 1559: 'Study 1 audit agreement', 2264: 'Study 1 audit discussion', 2326: 'Study 1 audit limitation',
       2995: 'ORG-V coder A/B templates (Appendix D), not V1'}
for pat, hits in V['two_coder_mentions_v182'].items():
    for n, ctx in hits:
        w = why.get(n, 'C6 continuity-label rule (≥ 2 clean coders, plan 29 §6.3), not a coder-count design statement' if '至少兩位' == pat else 'CHECK')
        S.append(f'| {pat} | {n} | {esc(ctx)} | {w} |')
S.append('\n## Segment diff (changed lines only)\n')
la, lb = A.split('\n'), B.split('\n')
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes():
    if tag == 'equal':
        continue
    S.append(f'### v1.8.1 L{i1 + 1}–{i2} → v1.8.2 L{j1 + 1}–{j2} ({tag})\n')
    for a, b in zip(la[i1:i2] + [''] * max(0, (j2 - j1) - (i2 - i1)), lb[j1:j2] + [''] * max(0, (i2 - i1) - (j2 - j1))):
        if a == b:
            continue
        for t, x1, x2, y1, y2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if t != 'equal':
                S.append(f'- OLD: `{esc(a[x1:x2]) or "∅"}`\n  NEW: `{esc(b[y1:y2]) or "∅"}`')
    S.append('')
open(os.path.join(OUT, '32b_V181_TO_V182_SEGMENT_DIFF.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(S) + '\n')
print('ok', sha(os.path.join(OUT, '32_PATCH_LOG_v1_8_2.md')), sha(os.path.join(OUT, '32b_V181_TO_V182_SEGMENT_DIFF.md')))
