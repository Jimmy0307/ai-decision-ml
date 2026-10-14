"""Write 59_PATCH_LOG_v1_8_5.md and 59b_V183_TO_V185_SEGMENT_DIFF.md from patches + verify output.
Usage: python -I build_log_v185.py <patches.json> <verify_out.json> <numeric_sources.json> <log md out> <segdiff md out>"""
import sys, json, difflib

P = json.load(open(sys.argv[1], encoding='utf-8'))
V = json.load(open(sys.argv[2], encoding='utf-8'))
S = json.load(open(sys.argv[3], encoding='utf-8'))
LOG, SEG = sys.argv[4], sys.argv[5]


def esc(t):
    return str(t).replace('|', '\\|').replace('\n', ' ⏎ ')


h = V['hard_checks']
L = []
L.append('# 59 — Patch log: v1.8.3 → v1.8.5 COMPUTE CLOSURE CANDIDATE (sub-agent U)\n')
L.append('Date: 2026-10-14. Built by exact, asserted-once replacements (`tools\\U\\patch_v185.py`), verified by '
         '`tools\\U\\verify_v185.py`. No DOCX built. No commit.\n')
L.append('| Item | Value |\n|---|---|')
L.append(f"| Source | `claude\\r14_merge_v1_8_3_v5_recovery\\41_MERGED_MASTER_THESIS_v1_8_3_V5_PROVENANCE_CANDIDATE.md` sha256 `{V['sha256'][0]}` (asserted) |")
L.append(f"| Output | `59_MERGED_MASTER_THESIS_v1_8_5_COMPUTE_CLOSURE_CANDIDATE.md` sha256 `{V['sha256'][1]}` |")
L.append(f"| Lines | {V['line_count'][0]} → {V['line_count'][1]} |")
L.append(f"| Patches | {V['patch_count']} (each `old` occurs exactly once in v1.8.3 and at apply time; reverse replay reproduces v1.8.3: {h['reverse_replay_reproduces_v183']}) |")
L.append(f"| v1.8.3 lines touched | {len(V['changed_lines_v183'])}: {', '.join(map(str, V['changed_lines_v183']))} |")
L.append(f"| Hard checks | {sum(1 for v in h.values() if v is True)}/{len(h)} PASS → ALL_HARD_CHECKS_PASS = {V['ALL_HARD_CHECKS_PASS']} |\n")

L.append('## 1. Patches\n')
L.append('| ID | Section | v1.8.3 line | Category | Evidence source |\n|---|---|---:|---|---|')
for p in P:
    L.append(f"| {p['id']} | {esc(p['section'])} | {p['v183_line']} | {esc(p['category'])} | {esc(p['source'])} |")
L.append('\nFull old/new text of every patch: `59b_V183_TO_V185_SEGMENT_DIFF.md`.\n')

L.append('## 2. Verification (hard checks)\n')
L.append('| Check | Result |\n|---|---|')
for k, v in h.items():
    L.append(f"| `{k}` | {'PASS' if v is True else 'FAIL'} |")

L.append('\n## 3. Required verification items\n')
L.append(f"- **Math identical:** {h['math_identical_ordered']} (counts v1.8.3/v1.8.5: {V['math_counts']}); equation tags identical: {h['equation_tags_identical']}; no math markers in any patch: {h['no_math_markers_in_patch_text']}.")
L.append(f"- **Headings:** {V['headings'][0]} → {V['headings'][1]}, identical and in the same order; **no heading added or changed** ({h['headings_identical_in_order_none_added']}). The new content sits inside the existing §3.7.4 and §4.5.5 as paragraphs with bold run-in labels.")
L.append(f"- **Captions:** one caption added — {', '.join(V['captions_added'])} (in §4.5.5); none removed or reordered ({h['captions_only_4_9B_added']}).")
L.append(f"- **G table rows:** {V['G_table_rows'][0]} → {V['G_table_rows'][1]}, identical and ordered ({h['G_rows_identical_ordered']}); G→M arrow tokens identical ({h['GM_arrow_tokens_identical']}); no new G code ({h['no_G17_or_new_G_code']}). G-token mentions in prose {V['G_token_counts_v183_v185'][0]} → {V['G_token_counts_v183_v185'][1]} (added by: {V['G_tokens_added_by_patch']}); these are prose references (\"G01–G16 移除 0\" etc. and G07/G14/G16 boundary values), not numbering or row changes.")
L.append('- **Protected sections identical:** ' + '; '.join(f"{k[8:-10]}={v}" for k, v in h.items() if k.startswith('section_')) + '.')
L.append(f"- **Primary-baseline numbers unchanged:** fixed primary phrases (abstract, §1.5, Abstract, Table 3-3 L1/L2) all present with unchanged counts ({h['primary_phrases_unchanged']}); primary tokens never removed {V['primary_token_counts']} ({h['primary_tokens_not_removed']}); §4.1–§4.4 identical. The added occurrences of 6,499/3,125/783/2,180 are the primary column of the new Table 4-9B and E40/abstract labelling only.")
L.append(f"- **Primary vs sensitivity separation:** Table 4-9B header separates the two columns ({h['table_4_9B_columns_separate_primary_vs_sensitivity']}); every sensitivity-only value (3,107 / 781 / 2,181 / 15／17 / q values) outside Table 4-9B sits in a sentence explicitly labelled 敏感度／sensitivity／替換 ({h['sensitivity_numbers_labelled']}; violations: {V['sensitivity_token_outside_labelled_context']}).")
L.append(f"- **Forbidden phrases:** {V['forbidden_hits']} → none ({h['no_forbidden_claims']}).")
L.append(f"- **Stale pending wording removed:** " + ', '.join(f"`{k[5:]}` {v[0]}→{v[1]}" for k, v in V.items() if k.startswith('term_') and k[5:] in (
    '執行條件尚待滿足', '執行條件待滿足', 'EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION', 'REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION',
    '日後是否重跑', '日後是否及何時重跑', 'PRIORITY_RATIONALE_REVIEW_REQUESTED', '開放驗證行動', '開放的驗證行動')) + '.')
L.append('- **New vocabulary counts (v1.8.3→v1.8.5):** ' + ', '.join(f"`{k[5:]}` {v[0]}→{v[1]}" for k, v in V.items() if k.startswith('term_') and k[5:] in (
    'v1.8.5 COMPUTE CLOSURE CANDIDATE', 'COMPUTATIONAL_VALIDATION_STATUS = CLOSED_WITH_BOUNDED_HUMAN_VALIDITY',
    'SATISFIED_AS_AUDITED_LABEL_SENSITIVITY_ANALYSIS', 'FULL_REANALYSIS_EXECUTED = YES', 'PRIMARY_BASELINE_REPLACED = NO',
    'CORPUS_WIDE_HUMAN_VALIDITY = NOT_ESTABLISHED', 'BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1', 'STABLE_UNDER_FULL_AUDITED_LABEL_REANALYSIS',
    '13/13 逐位元組相同', 'FULL_REANALYSIS_REQUIRED', 'NOT_RECOMMENDED', 'AUTHOR TO CONFIRM', 'SUBMISSION_READY = NO')) + '.')
L.append("  - `NOT_RECOMMENDED` 4→1: the priority flag survives only in E40 as the historical v1.8.3 judgement, superseded by researcher approval.")
L.append("  - `AUTHOR TO CONFIRM` 2→1: the §3.7.4 tag was removed (E48 resolved); E48 still names it as removed.")
L.append(f"  - The suggested semantics sentence appears {V.get('term_主要分析維持預先凍結之 V5/R14 基準；另以 50 筆目標人工稽核標籤進行有界替代，完整重跑所有標籤相依分析，以評估結論對語意標籤修訂的敏感性', ['', '?'])[1]} times (status line, abstract, §3.7.4, §4.5.5, §5.8.9).")

L.append('\n## 4. Every added numeric token and its source\n')
L.append(f"Net document token change = sum of per-patch changes: {h['numeric_patch_sum_matches_doc']}. All added tokens mapped: {h['numeric_added_all_traceable']}.\n")
L.append('| Token | Net added | Source |\n|---|---:|---|')
for k, v in V['numeric_added_doc'].items():
    L.append(f"| `{k}` | {v} | {esc(S.get(k, 'UNMAPPED'))} |")
L.append('\nRemoved numeric tokens (status wording only; no result value): ' + ', '.join(f"`{k}`×{v}" for k, v in V['numeric_removed_doc'].items())
         + ' — from the deleted v1.8.3 pending-status text (37 protected inputs; V1.8 檔案 04/07 §8; V1.8.1 檔案 15; 理由 2–5; SHA-256; V1.8.3 檔案 38).')
L.append('\nPer-patch numeric changes:\n')
L.append('| Patch | Added | Removed |\n|---|---|---|')
for pid, d in V['numeric_per_patch'].items():
    L.append(f"| {pid} | {esc(d['added'])} | {esc(d['removed'])} |")

L.append('\n## 5. Scope statement\n')
L.append('- Changed: status line L5 (v1.8.5 label, compute-closure summary, COMPUTATIONAL_VALIDATION_STATUS, triplet), abstract/Abstract, '
         '§1.4/1.5/1.6, §3.1.1, §3.7.4 (rule preregistered; new procedure paragraph), §3.8.1 (L2′ provenance + Table 3-3 role cell), '
         '§3.8.2 rule 6 (wording only; G list unchanged), §3.8.3 (baseline reproduction sentence), ch.4 intro, §4.5.5 (status + new sensitivity block + Table 4-9B), '
         '§4.11 (two cells), §5.3.2 table cell, §5.4.2, §5.8.9, §5.9, §5.10, Appendix D (rows 43–61), Appendix E39(c)/E40/E44/E48.')
L.append('- Unchanged (verified): all math, §3.9.1–§3.9.5 incl. Tables 3-4/3-4A and V1 design text, §3.10–§3.14 enterprise model, '
         '§4.1–§4.4 primary results, §4.5.1–§4.5.4, §4.6 G handoff table, §4.7–§4.10, Appendix C, all G rows, all headings.')
L.append('- Appendix D: rows 60–61 are reserved placeholders (files do not exist at build time); row 56 records that no decision memo was required (OUT 55).')
L.append('\n```\nMANUSCRIPT=v1.8.5 COMPUTE CLOSURE CANDIDATE\nSOURCE_SHA256=' + V['sha256'][0] + '\nOUTPUT_SHA256=' + V['sha256'][1]
         + f"\nPATCHES={V['patch_count']}\nHARD_CHECKS={sum(1 for v in h.values() if v is True)}/{len(h)} PASS\nHEADINGS_ADDED=0\nCAPTIONS_ADDED=1 (表 4-9B)\n"
         'PRIMARY_BASELINE_NUMBERS_CHANGED=0\nFORBIDDEN_PHRASES=0\nSUBMISSION_READY=NO\nDOCX=NOT_BUILT\n```\n')
open(LOG, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))

D = ['# 59b — v1.8.3 → v1.8.5 segment diff (sub-agent U)\n',
     f"Source sha256 `{V['sha256'][0]}` → output sha256 `{V['sha256'][1]}`. One block per patch, in application order. "
     "`old` = exact v1.8.3 text (asserted to occur once); `new` = v1.8.5 text. ⏎ in the inline diff marks an inserted line break.\n"]
for p in P:
    D.append(f"## {p['id']} — {p['section']} (v1.8.3 line {p['v183_line']}) — {p['category']}\n")
    D.append(f"Source: {p['source']}\n")
    D.append('```diff\n- ' + p['old'].replace('\n', '\n- ') + '\n+ ' + p['new'].replace('\n', '\n+ ') + '\n```\n')
    sm = difflib.SequenceMatcher(None, p['old'], p['new'], autojunk=False)
    parts = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            seg = p['old'][i1:i2]
            parts.append(seg if len(seg) <= 40 else seg[:18] + '…' + seg[-18:])
        else:
            if i2 > i1:
                parts.append('[-' + p['old'][i1:i2].replace('\n', '⏎') + '-]')
            if j2 > j1:
                parts.append('{+' + p['new'][j1:j2].replace('\n', '⏎') + '+}')
    D.append('Inline: ' + ''.join(parts) + '\n')
open(SEG, 'w', encoding='utf-8', newline='\n').write('\n'.join(D))
print('log', LOG)
print('seg', SEG)
