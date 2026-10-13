"""Build 16_PATCH_LOG_v1_8_1.md and 16b_V18_TO_V181_SEGMENT_DIFF.md.
Usage: python -I build_log.py <v1.8 md> <v1.8.1 md> <patches.json> <verify_out.json> <out_dir>"""
import sys, json, hashlib, difflib, os

A_P, B_P, PJ, VJ, OUT = sys.argv[1:6]
A = open(A_P, encoding='utf-8').read()
B = open(B_P, encoding='utf-8').read()
la, lb = A.split('\n'), B.split('\n')
P = json.load(open(PJ, encoding='utf-8'))
V = json.load(open(VJ, encoding='utf-8'))
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
v18_to_v181 = {}
offset = len(V['inserted_lines_v181'])
first_ins = min(V['inserted_lines_v181']) if V['inserted_lines_v181'] else 10 ** 9


def map_line(n):
    return n if n < first_ins else n + offset


def merged_segments(a, b, gap=6):
    ops = [o for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()]
    groups, cur = [], None
    for t, i1, i2, j1, j2 in ops:
        if t == 'equal':
            if cur and (i2 - i1) < gap and not (i2 == len(a) and j2 == len(b)):
                cur['pending'] = (i1, i2, j1, j2)
            else:
                if cur:
                    groups.append(cur)
                cur = None
            continue
        if cur is None:
            cur = dict(i1=i1, i2=i2, j1=j1, j2=j2, pending=None)
        else:
            cur.update(i2=i2, j2=j2, pending=None)
    if cur:
        groups.append(cur)
    return [(a[g['i1']:g['i2']], b[g['j1']:g['j2']]) for g in groups]


NUM_JUST = {
    'J01': '"1" = Study 1; "17", "19", "21" = V1.8.1 file numbers (17 evidence freeze; 19–21 V1 packet). Labels, not network/empirical values.',
    'J02': '"12", "37" = 12 of 37 protected V9 inputs not recovered (V1.8 02 §5; already stated in v1.8 E39(b)). Provenance count, not a network/empirical value.',
    'J04': 'same as J02 (12 of 37 protected inputs).',
    'J11': 'same as J02.',
    'J13': 'same as J02.',
    'J20': '"12", "37" as J02; "04", "07", "15", "17" = file numbers; "8" = memo §8.',
    'J22': '"2026-10-03" = V9.1 run date (13 §3); "4.6.2", "4.6.3" = R14 section numbers.',
    'J23': '"84/120", "85/120", "12/120", "11/120" repeat the unchanged Table 4-8 values on the same table (v1.8 L1600–1601; recomputed from raw rows in 13 §2); "2026-10-03" = V9.1 date; "7" = R14 Table 7.',
    'J24': '"4-8" = table reference.',
    'J25': '"4.5.2", "4.5.3" = section references.',
    'J26': '"4.5.2" = section reference.',
    'J27': '"3.7.3", "4.5" = section references; "2026-10-03" V9.1 date; "2026-10-04" first manuscript import of V9.1 (13 §3); "2026-09-20" = inherited docProps timestamp (13 §1.4).',
    'J28': '"3.7.3", "4.5" = section references.',
    'J29': 'File numbers 08/13/16/17/19/20/21, "1" (Study 1), section references 4.5.2/4.5.3/5.4.2/5.8.3/4.7.3.',
}

o = []
w = o.append
w('# 16 — Patch log: v1.8 → v1.8.1 CLEANUP CANDIDATE (sub-agent J)')
w('')
w('Date: 2026-10-14. No new analysis; no network, empirical, taxonomy, G01–G16, G→M, Enterprise-model or equation change. `SUBMISSION_READY = NO` is kept. No DOCX was built.')
w('')
w(f'- **Input:** `claude/r14_merge_v1_8_source_closure/08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md`, sha256 `{sha(A_P)}` (asserted equal to the expected `1515b0f2…7ad58` before patching; unchanged).')
w(f'- **Output:** `claude/r14_merge_v1_8_1_study1_freeze/16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.md`, sha256 `{sha(B_P)}`. Lines {V["line_count"][0]} → {V["line_count"][1]} (5 rows inserted in the Appendix D table after the 137 row; no line deleted). UTF-8, LF, no BOM.')
w(f'- **Method:** {len(P)} exact old→new replacements, each asserted to occur exactly once in v1.8 and at apply time (`tools/J/patch_v181.py`). Verification: `tools/J/verify_v181.py` → `tools/J/verify_out.json`. This log and 16b: `tools/J/build_log.py`. Run with `python -I`.')
w('- **Authorities used:** 13 (segmentation attribution, §4 wording), 14 (G07/G15 WORDING_CONFIRMED), 12 (stale status), 15 (reanalysis governance), 17 (Study 1 freeze), 19 (V1 status READY_TO_RUN), V1.8 08_PATCH_LOG / 02 / 07.')
w('')
w('## 1. Change list')
w('')
w('| id | v1.8 line | v1.8.1 line | section | category | source |')
w('|---|---|---|---|---|---|')
for p in P:
    w(f"| {p['id']} | {p['v18_line']} | {map_line(p['v18_line'])} | {p['section']} | {p['category']} | {p['source']} |")
w('')
for p in P:
    w(f"### {p['id']} — v1.8 L{p['v18_line']} (v1.8.1 L{map_line(p['v18_line'])}) — {p['section']}")
    w(f"- **Category:** {p['category']}")
    w(f"- **Source:** {p['source']}")
    w('- **Old:**')
    for x in p['old'].rstrip('\n').split('\n'):
        w('  > ' + x)
    w('- **New:**')
    for x in p['new'].rstrip('\n').split('\n'):
        w('  > ' + x)
    w('')

w('## 2. Verification (script output: `tools/J/verify_out.json`)')
w('')
w('### 2.1 Math, fences, headings')
w(f"- `$$` blocks {V['math_counts_v18']['$$']} → {V['math_counts_v181']['$$']}; inline `$…$` {V['math_counts_v18']['$inline']} → {V['math_counts_v181']['$inline']}; `\\[…\\]` {V['math_counts_v18']['\\[\\]']} → {V['math_counts_v181']['\\[\\]']}. Byte-identical in order: {V['math_identical_ordered']}.")
w(f"- Changed lines containing math markers: {V['changed_lines_with_math_markers'] or 'none'}.")
w(f"- Fenced blocks {V['fenced_blocks'][0]} → {V['fenced_blocks'][1]}; changed fence index {V['fenced_changed_index']} = the text flow chart at v1.8 L407–418 (J10, L412, status words only; no equation). All other fences identical.")
w(f"- Headings: {V['headings']['v18']} → {V['headings']['v181']}, identical in order and text: {V['headings']['identical']}.")
w('')
w('### 2.2 G01–G16 lines')
w(f"- v1.8 lines containing a G01–G16 token: {V['G_lines_total_v18']}. Whole-document G-token count {V['G_token_counts'][0]} → {V['G_token_counts'][1]}. `G## → M#` tokens identical: {V['GM_arrow_tokens_identical']}. Inserted Appendix D rows contain no G token: {not V['G_in_inserted_lines']}.")
for kw in ['VCP', 'VSC', 'DL', 'NEV', 'SIMULATED_ONLY', 'EMPIRICAL RESULT PENDING', 'HUMAN RESULT PENDING', 'UNIDENTIFIED']:
    w(f"- `{kw}` count {V['count_' + kw][0]} → {V['count_' + kw][1]}")
w('- Changed G-token lines (segment diff):')
for g in V['G_lines_changed']:
    w(f"  - **v1.8 L{g['v18_line']}** — G tokens identical: {g['tokens_identical']}; all changes inside a provenance bracket 〔…〕: {g['all_changes_inside_provenance_bracket']}.")
    if g['v18_line'] == 5:
        w('    - L5 is the manuscript status line, which the task mandates rewriting (allowed changes 2 and 3: version label, FULL_REANALYSIS status, Study 1 freeze, V1 READY_TO_RUN). Its G-token segment 「或 G01–G16 凍結值」 is byte-identical; no G content, membership or assignment is touched. This is the only G-line change outside a provenance bracket. Merged segments:')
    a, b = la[g['v18_line'] - 1], lb[g['v181_line'] - 1]
    for so, sn in merged_segments(a, b):
        w(f"    - OLD: 「{so}」 → NEW: 「{sn}」")
w('')
w('### 2.3 Numeric tokens')
w(f"- Removed from the document: {V['numeric_removed_doc'] or 'none'}.")
w(f"- Added to the document (multiset): `{json.dumps(V['numeric_added_doc'], ensure_ascii=False)}`. Per-patch sum equals document delta: {V['numeric_patch_sum_matches_doc']}.")
w('- Justification per patch (no network or empirical number was added, removed or changed):')
for pid, d in V['numeric_per_patch'].items():
    w(f"  - **{pid}** +{json.dumps(d['added'], ensure_ascii=False)} −{json.dumps(d['removed'], ensure_ascii=False)}: {NUM_JUST.get(pid, '')}")
w('')
w('### 2.4 Forbidden and remaining strings (v1.8.1)')
for k, v in V['forbidden_hits_v181'].items():
    w(f"- `{k}`: {len(v)} hits {v if v else ''}")
w(f"- `完整資料來源` (legacy zip): v1.8 {V['legacy_zip_mentions']['v18']}, v1.8.1 {V['legacy_zip_mentions']['v181']} — the manuscript never names the legacy zip (confirms V1.8 §2.8 and 12 Task C), so no legacy-identity edit.")
w(f"- Full-reanalysis codes in v1.8.1: {V['full_reanalysis_codes_v181']}. `FULL_REANALYSIS_REQUIRED` is kept only as the V9 package's own label (L5, L1629, L2362, E39, E40).")
w('- Remaining `待核` and related markers:')
REASON = {
    '待核': '「Vial, 2019 的內容待核對」 (E21; reference verification, outside V9/segmentation scope; OPEN_SOURCE_NOT_FOUND in V1.8). Kept.',
    'AUTHOR TO CONFIRM': 'E48 residual: label→pair-eligibility propagation rule UNRESOLVED and sidecar generator NOT_RECOVERED (V1.8 04 Q4; 15 §3 PROPAGATION_RULE_STATUS=UNRESOLVED_MUST_BE_PREDECLARED). Kept.',
    '工作環境中': 'L651 V5 Data Pack original (REAL_V5_DATA_PACK=NOT_RECOVERED, 12 Task C) and E46 submission-format files (OPEN_SOURCE_NOT_FOUND). Both still true; kept.',
}
for k, v in V['remaining_hits_v181'].items():
    w(f"  - `{k}`: {len(v)} hits at v1.8.1 lines {[n for n, _ in v]}" + (f" — {REASON[k]}" if k in REASON and v else ''))
w('')
w('## 3. Deliberately not changed')
w('1. **L158 body text** (「完整重分析是否執行仍待研究者決定」) is on a G-token line; only its provenance bracket was extended with a pointer to E40 (J07), per the G-line rule. The body clause is not contradicted by the current status (future rerun remains a researcher decision).')
w('2. **Conditional / methodological uses** of 完整重分析 (v1.8 L605, L607, L619, L645, L1638, L1640, L2268, L3063, L3072) describe what the full reanalysis is or what holds *until* it is done; they state no execution status and are consistent with METHOD_STATUS=REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION. L645 and L1638 also carry G tokens.')
w('3. **Re-segmentation numbers**: 84/85 of 120, 12/11, 29/32, 30/32, 31 (15/16), 3,112/6,499, 742/765, q-counts — unchanged. Only attribution was added (J22, J23, J25, J26, J27, J28). 742/765 are not recomputed (13 §5); the tag at J22 claims verification only for the observed- and direction-change counts.')
w('4. **G07/G15** (14: both WORDING_CONFIRMED): no wording change; one source pointer added next to the Table 4-9 reference (J24). The optional precision sentence in 14 §5 was not added (it would add new numeric tokens).')
w('5. **Appendix F** is a block of preserved status paragraphs for v1.0–v1.6, not a version table, and its heading 「v1.0–v1.6」 must stay identical. Following the V1.8 precedent (08_PATCH_LOG §4 item 8), F is unchanged; v1.8 and v1.8.1 were added as rows in the Appendix D artifact/version table (J29), and the status line now says where v1.7+ versions are listed.')
w('6. **L651** (V5 Data Pack provenance) stays OPEN; consistent with REAL_V5_DATA_PACK=NOT_RECOVERED. No `完整資料來源` mention exists.')
w('7. **Typos**: the scan (`tools/J/typo_scan.py`: doubled characters, doubled punctuation, unbalanced brackets) found one real typo, v1.8 L869 missing 「）」 (J30). Other hits were false positives (e.g., 直接接口, 驗證證據, 出版版本, interval notation `(0, 1]`, wrapped ASCII diagram brackets).')
w('8. 132 / 128 / 131 / 133 / 137 artifacts and the V1.8 folder are not edited.')
w('')
w('## 4. STOP conditions')
w('None triggered: all replacements matched exactly once; no 84–85/120 number-vs-source conflict (13 §2); no G07/G15 or G01–G16 conflict (14); no κ or enterprise-model change.')
open(os.path.join(OUT, '16_PATCH_LOG_v1_8_1.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(o) + '\n')

d = ['# 16b — Changed-line segment diff (v1.8 → v1.8.1)', '',
     'Character-level diff merged across equal runs shorter than 6 characters. Line numbers: v1.8 / v1.8.1.', '']
for a, b in V['changed_line_pairs_v18_v181']:
    d.append(f'## v1.8 L{a} / v1.8.1 L{b}')
    for so, sn in merged_segments(la[a - 1], lb[b - 1]):
        d.append(f'- OLD: 「{so}」')
        d.append(f'  NEW: 「{sn}」')
    d.append('')
d.append(f"## Inserted lines (v1.8.1 L{V['inserted_lines_v181'][0]}–L{V['inserted_lines_v181'][-1]}, after v1.8 L{first_ins - 1})")
for n in V['inserted_lines_v181']:
    d.append(f'- NEW: 「{lb[n - 1]}」')
open(os.path.join(OUT, '16b_V18_TO_V181_SEGMENT_DIFF.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(d) + '\n')
print('ok')
