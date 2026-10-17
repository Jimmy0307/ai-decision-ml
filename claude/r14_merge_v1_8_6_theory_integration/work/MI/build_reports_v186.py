"""Build OUT/02_V1_8_6_CHANGELOG.md and OUT/03_V1_8_6_DIFF_SUMMARY.md from patches + verify output.
Usage: python -I build_reports_v186.py <59a md> <01 md> <patches.json> <verify_out.json> <OUT dir>"""
import sys, json, difflib, os
from collections import Counter

A = open(sys.argv[1], encoding='utf-8').read()
B = open(sys.argv[2], encoding='utf-8').read()
P = json.load(open(sys.argv[3], encoding='utf-8'))
V = json.load(open(sys.argv[4], encoding='utf-8'))
OUT = sys.argv[5]
la, lb = A.split('\n'), B.split('\n')

DECISIONS = [
    ("RD-1", "V1 coder-facing term mismatch (NOT changed)",
     "§3.9.3 (V1 design text, protected) still uses 「企業決策介面」 (count in §3.9.3 = %d; 「企業決策過程」 = %d), while the teacher-approved "
     "S1e coder packets use 「企業決策過程」 (S1E_PROCESS_WORDING_CHANGELOG.md). Per brief, §3.9.3 was NOT rewritten. Researcher to decide "
     "whether §3.9.3 (and Q1 description, Table 3-14 V1 row, Appendix E6) should adopt the S1e wording in a separate V1-text pass."
     % (V['V1_3_9_3_term_counts']['企業決策介面'], V['V1_3_9_3_term_counts']['企業決策過程'])),
    ("RD-2", "P2 bullet remark sentence edited (P2 formal statement unchanged)",
     "R-2 fix (5) (plan 10 §0 D-e) requires changing the remark sentence that sits inside the P2 bullet at 59a l.1138. The P2 formal "
     "statement (text up to 「即 DL = 0。」) is byte-identical (hard check P2_formal_statement_identical); P1, P3–P8 bullets are byte-identical; "
     "C.6 (verbatim v2.2) is untouched. If the researcher reads 'P1–P8 text unchanged' as covering the remark too, revert T07 and keep the "
     "precise wording only in the 3.12.4 classification block and §5.6 (T08, T20)."),
    ("RD-3", "R-1 erratum applied as manuscript wording only",
     "Lemma E′ pessimistic proof wording corrected in §3.12.6 (T10) and recorded as erratum C.10.9 (T26). C.2 (verbatim v2.2) keeps 「取任一 x ∈ T」 "
     "as the historical record; 42 and the 51 `envelopes_lemmaE` docstring are not edited (frozen; hashes verified unchanged). Decide when to "
     "carry the erratum into the next canonical 42 version."),
    ("RD-4", "Label collisions kept with disambiguation notes",
     "Theory-pack final labels are used verbatim, but several collide with existing manuscript labels: typing axioms T1–T4 vs Model D triggers "
     "T1–T5; missingness Props G1–G8 / Remark G7 vs gaps G01–G16; Thm D1/Prop D4–D6 vs Appendix C.8 D1–D9, M5 (D1)(D2) and org dimensions "
     "D01–D12; Thm R1–R5 vs resource constraints (R1)(R2); Prop E.1–E.10 vs Appendix E rows. Disambiguation sentences were added (3.9.6, 3.12.4 "
     "block, 3.13, C.10 intro). Researcher may prefer a prefixed renaming (e.g., MG1–MG8) in a later pass."),
    ("RD-5", "Out-of-scope locations not updated (consistency follow-ups)",
     "Not edited in this pass (outside the brief's scope list): Abstract / English Abstract (still say 'proof sketches indicate …'), Table 1-1 "
     "RQ4–RQ6 status cells (plan 10 rows 1.2–1.4), §2.13 'model implications' sentence (plan 10 row 2.1), Table 4-33 RQ6 VOI qualifier "
     "('對固定候選集合'), §4.10.3 interpretation bullet, §5.8.4/§5.8.5 pointers (NONE/AMBIGUOUS; IA sidecar) and §3.12.5 Q2/Q4/Q7 rows. "
     "All are consistent-but-less-precise; none is contradicted by the new text."),
    ("RD-6", "R-4 confirmation",
     "W5 (162/400 at ±5%%) is reported as PRIMARY/canonical everywhere robustness is mentioned (4.9.1 note, C.10.4); W5_WIDE (367/400) only "
     "as SENSITIVITY / expanded witness, never as primary (hard checks W5_162_reported_as_primary, W5_WIDE_367_only_as_sensitivity)."),
    ("RD-7", "Citation positioning deferred (R-3) + orchestrator note after reference verification",
     "No citation was added and no existing citation sentence was altered. Per the orchestrator note, the draft §5.7 sentence "
     "'這些結果也不宣稱其機制在既有文獻中前所未見，與既有理論的對應關係待引文查證完成後另行界定，本稿不據以主張新穎性。' (alluding to unverified "
     "analogue literature) was REMOVED from main text (T23) and replaced by a neutral, name-free Appendix E row E51 (T28). No analogue-literature "
     "names or fields (optimal delegation, delegated project choice, capital-budget ceilings, minimax-regret menu dependence, information complementarity, "
     "principal–agent) appear anywhere in 01. Note: the term 「部分識別」 is kept in §3.13 only as the brief-required method label "
     "('partial-identification methodology'), with no literature claim — researcher may reword. Placeholder anchors are in this changelog only."),
    ("RD-8", "Auditor TA follow-up applied (T29–T50)",
     "TA's fixes from OUT 05 and OUT 11 §B were applied verbatim as layered patches, each asserted to match once. MAJOR-1 → T29 (l.113) and T30 (l.775). "
     "MAJOR-2 → T31 (l.779; §3.9.3 itself not edited; RD-1 stays open). m1 → T32; m2 → T33 and T34; m3 → T35; m4 → T36; m5 → T37; "
     "m6 → T38 and T39; m7 and m13 → T40; m8 → T41 and T42; m9 → T43 and T44; m10 → T45; m11 → T46 (zh Abstract) and T47 (EN Abstract); "
     "m12 → T48 (TA's second option); m14 → T49; m15 → T50. The edits to the Abstract and to C.10.2 are the only extra areas this changes. "
     "Not verbatim: (a) T47, because TA gave no English text, so MI mirrored the zh fix; "
     "(b) T40 adds a closing 「。」 after TA's m7 and m13 phrases; (c) m12 used TA's alternative wording instead of moving the paragraph. "
     "RD-5's Abstract item is now partly resolved (only the screening clause was changed)."),
]

PLACEHOLDERS = [
    "<!-- ANCHOR-PLACEHOLDER §3.12.4 DL / §5.7(1): optimal delegation / permitted-set design and delegated project choice (pack 02 §7, 11 A10) — insert only if VERIFIED -->",
    "<!-- ANCHOR-PLACEHOLDER §3.12.4 DL-6: capital budgeting with spending ceilings (pack 02 §7) — insert only if VERIFIED -->",
    "<!-- ANCHOR-PLACEHOLDER §3.12.4 governance screening / §5.7(2): delegation-set literature (pack 03 §10) — insert only if VERIFIED -->",
    "<!-- ANCHOR-PLACEHOLDER §3.12.4 shared capability / §5.7(3): 'more options can hurt' / monotone comparative statics (pack 04 §8) — insert only if VERIFIED -->",
    "<!-- ANCHOR-PLACEHOLDER §3.13 VOI / §5.7(4): minimax-regret menu dependence; complementarity of information value; interval minmax regret (pack 05 §7, 06 §6) — insert only if VERIFIED -->",
    "<!-- ANCHOR-PLACEHOLDER §3.13 missingness / §5.7(5): partial identification (pack 07 §8) — insert only if VERIFIED -->",
    "<!-- ANCHOR-PLACEHOLDER §3.12.4 / C.10.2: pessimistic bilevel selection (pack 02 §7, 06 §6; Wiesemann et al. 2013 already in list may suffice — researcher to decide) -->",
]

hc = V['hard_checks']
cats = Counter(p['category'].split(' ')[0] for p in P)
with open(os.path.join(OUT, '02_V1_8_6_CHANGELOG.md'), 'w', encoding='utf-8') as f:
    f.write("# 02 — v1.8.6 THEORY INTEGRATION CANDIDATE: change log\n\n")
    f.write("- Base: `59a_MERGED_MASTER_THESIS_v1_8_5a_CANONICAL.md` sha256 `%s` (asserted before patching)\n" % V['sha256_59a'])
    f.write("- Output: `01_V1_8_6_THEORY_INTEGRATED_MANUSCRIPT.md` sha256 `%s`\n" % V['sha256_01'])
    f.write("- Method: `work/MI/patch_v186.py` — %d exact old→new replacements/insertions, each asserted to match exactly once in 59a "
            "and once at apply time; verification `work/MI/verify_v186.py` → `work/MI/verify_out.json` (ALL_HARD_CHECKS_PASS = %s, %d/%d).\n"
            % (len(P), V['ALL_HARD_CHECKS_PASS'], sum(1 for v in hc.values() if v is True), len(hc)))
    f.write("- Status: `v1.8.6 THEORY INTEGRATION CANDIDATE`; `SUBMISSION_READY = NO`. No git commit/push (orchestrator).\n")
    f.write("- Sources: theory pack `REPO/claude/r14_merge_q1_theory_upgrade_v1/` 01–15 (FINAL labels from 12/14/15), witnesses 09; "
            "common_v186.txt fixed decisions R-1, R-2, R-3, R-4.\n\n")
    f.write("## Summary table\n\n| id | 59a line | section | category | source |\n|---|---|---|---|---|\n")
    for p in P:
        f.write("| %s | %d | %s | %s | %s |\n" % (p['id'], p['line_59a'], p['section'], p['category'], p['source']))
    f.write("\n## Researcher-decision items\n\n")
    for i, t, d in DECISIONS:
        f.write("- **%s — %s.** %s\n" % (i, t, d))
    f.write("\n## Citation placeholders (changelog only; NOT in manuscript)\n\n```\n" + "\n".join(PLACEHOLDERS) + "\n```\n")
    f.write("\n## New headings (existing headings preserved in order)\n\n" + "\n".join("- `%s`" % h for h in V['headings_added']) + "\n")
    f.write("\n## Full old → new text per change\n\n")
    for p in P:
        f.write("### %s — %s (%s)\n\n- source: %s\n- 59a line: %d\n\n**old**\n\n```text\n%s\n```\n\n**new**\n\n```text\n%s\n```\n\n"
                % (p['id'], p['section'], p['category'], p['source'], p['line_59a'], p['old'], p['new']))

# ---------------- 03 diff summary
sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
segs = []
n_rep = n_ins = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    if tag == 'replace' and (i2 - i1) == (j2 - j1):
        for k in range(i2 - i1):
            a, b = la[i1 + k], lb[j1 + k]
            s2 = difflib.SequenceMatcher(None, a, b, autojunk=False)
            parts = []
            for t2, x1, x2, y1, y2 in s2.get_opcodes():
                if t2 == 'equal':
                    continue
                parts.append((t2, a[x1:x2], b[y1:y2]))
            segs.append(('changed', i1 + k + 1, j1 + k + 1, parts))
            n_rep += 1
    else:
        for k in range(i1, i2):
            segs.append(('replaced (old line; new text in following insertion)', k + 1, None, [('delete', la[k], '')]))
        if j2 > j1:
            segs.append(('inserted', i1, j1 + 1, [('insert', '', '\n'.join(lb[j1:j2]))]))
            n_ins += (j2 - j1)
with open(os.path.join(OUT, '03_V1_8_6_DIFF_SUMMARY.md'), 'w', encoding='utf-8') as f:
    f.write("# 03 — v1.8.5a (59a) → v1.8.6 (01): segment diff summary\n\n")
    f.write("## Summary counts\n\n")
    f.write("| item | value |\n|---|---|\n")
    f.write("| patches | %d |\n" % len(P))
    f.write("| line count 59a → 01 | %d → %d |\n" % tuple(V['line_count']))
    f.write("| 59a lines changed in place | %d |\n" % n_rep)
    f.write("| new lines inserted | %d |\n" % n_ins)
    f.write("| 59a lines replaced by multi-line segments (no content deleted; see segments) | %d |\n"
            % sum(1 for s in segs if s[0].startswith('replaced')))
    f.write("| characters 59a → 01 | %d → %d |\n" % (len(A), len(B)))
    f.write("| headings added | %d (existing %d preserved in order) |\n" % (len(V['headings_added']), V['headings_count'][0]))
    f.write("| captions added | %s |\n" % '; '.join(V['captions_added']))
    f.write("| math spans ($$ / inline $) | %s / %s (identical: %s) |\n" % (V['math_counts']['$$'], V['math_counts']['$inline'], hc['math_spans_identical_ordered']))
    f.write("| G01–G16 table rows | %s (identical: %s) |\n" % (V['G_table_rows'], hc['G_rows_identical_ordered']))
    f.write("| citation-pattern counts main text (before/after) | %s |\n" % V['citation_pattern_counts_main_text'])
    f.write("| ALL_HARD_CHECKS_PASS | %s |\n\n" % V['ALL_HARD_CHECKS_PASS'])
    f.write("## Hard checks\n\n" + "\n".join("- %s: %s" % (k, v) for k, v in hc.items()) + "\n\n")
    f.write("## Protected-region verification\n\n")
    f.write("- Math spans identical (ordered): %s; equation tags identical: %s; fenced blocks identical: %s.\n"
            % (hc['math_spans_identical_ordered'], hc['equation_tags_identical'], hc['fenced_code_blocks_identical']))
    f.write("- Existing headings preserved in order: %s; added headings: %s.\n" % (hc['existing_headings_preserved_in_order'], len(V['headings_added'])))
    f.write("- §3.9.1–§3.9.5 byte-identical (incl. Tables 3-4/3-4A and V1 design §3.9.3): %s; all M1–M4 scope sentences were placed in new §3.9.6 "
            "(no sentence added inside §3.9.2–§3.9.5).\n" % all(hc['section_%s_identical' % s] for s in ('3_9_1', '3_9_2_tables_3_4_3_4A', '3_9_3_V1_design', '3_9_4', '3_9_5')))
    f.write("- P1, P3–P8 bullets identical: %s; P2 formal statement identical: %s; P2 remark changed only by T07: %s.\n"
            % (hc['P1_P3_to_P8_bullets_identical'], hc['P2_formal_statement_identical'], hc['P2_only_remark_changed_by_T07']))
    f.write("  - P2 remark old: `%s`\n  - P2 remark new: `%s`\n" % (V['P2_remark_change']['old'], V['P2_remark_change']['new']))
    f.write("- Appendix C.1–C.9 verbatim: %s; Chapter 2, §3.1–3.8, §3.11, §3.12.1–3.12.3/3.12.5/3.12.7, §4.1–4.8, §4.10, §4.11, §5.1–5.5, §5.8.1–5.8.9, "
            "references, Appendices A/B/E/F identical: %s.\n" % (hc['appendix_C1_C9_verbatim'], all(v for k, v in hc.items() if k.startswith('section_'))))
    f.write("- Study 1 phrases/tokens unchanged: %s / %s. Canonical 42/51 unchanged: %s (%s). S1e packets unchanged: %s.\n"
            % (hc['study1_primary_phrases_unchanged'], hc['study1_tokens_unchanged'], hc['canonical_42_51_unchanged'],
               ', '.join('%s %s…' % (k, v[:8]) for k, v in V['canonical_hashes'].items()), hc['S1e_packets_unchanged']))
    f.write("- No new citation keys (main text and whole document, 5 reference-like patterns; reference list identical; no unverified anchor names): %s / %s / %s / %s.\n"
            % (hc['no_new_citation_keys_main_text'], hc['no_new_citation_keys_whole_document'], hc['reference_list_identical'], hc['no_unverified_anchor_names_added']))
    f.write("- Forbidden-phrase grep on 01 (minimal sufficient, DL>0 iff, governance always, generally non-monotone, enterprise-evidence-for-synthetic, FULLY_VALIDATED): %s; "
            "59a had: %s.\n" % (V['forbidden_hits_01'], V['forbidden_hits_59a']))
    f.write("- Every '充要' sentence in new text is scoped/negated: %s; every 'X 為正若且唯若' sentence is scoped to a unique first best: %s.\n"
            % (hc['every_充要_in_new_text_scoped_or_negated'], hc['every_positive_iff_scoped_to_unique_first_best']))
    f.write("- 367/400 only as sensitivity: %s; 162/400 as primary: %s.\n\n" % (hc['W5_WIDE_367_only_as_sensitivity'], hc['W5_162_reported_as_primary']))
    f.write("## Numeric tokens\n\n### Added (token: count — source)\n\n")
    for k, v in V['numeric_added_doc'].items():
        f.write("- `%s`: +%d — %s\n" % (k, v, V['numeric_added_sources'].get(k, 'UNMAPPED')))
    f.write("\n### Removed (token: count)\n\n" + ("\n".join("- `%s`: −%d (status-line date replaced by 2026-10-18)" % (k, v) for k, v in V['numeric_removed_doc'].items()) or "- none") + "\n")
    f.write("\nNo Study 1 number, model number or witness number from 59a was removed or changed; the R-1 erratum changes wording only.\n\n")
    f.write("## Segment diff per changed line\n\n")
    for kind, la_no, lb_no, parts in segs:
        f.write("### %s — 59a l.%s%s\n\n" % (kind, la_no, (" → 01 l.%s" % lb_no) if lb_no else ""))
        for t2, a, b in parts:
            if t2 in ('replace', 'delete') and a:
                f.write("- ⊖ `%s`\n" % a.replace('`', 'ˋ').replace('\n', ' ⏎ '))
            if t2 in ('replace', 'insert') and b:
                f.write("- ⊕ `%s`\n" % b.replace('`', 'ˋ').replace('\n', ' ⏎ '))
        f.write("\n")
print('ok', n_rep, n_ins)
