"""Move-only reorganization of C:\\NTUST_PAPER (2026-10-14). Nothing is deleted or overwritten.

Usage:
  python -I reorg_move.py plan      -> prints the plan and checks every source exists / no destination exists
  python -I reorg_move.py execute   -> performs the moves, verifies content before/after,
                                       writes MOVE_MANIFEST_20261014.csv and ROLLBACK_20261014.py next to this script

Files: SHA-256 before and after must match. Directories: file count and total bytes before and after must match.
"""
import csv
import hashlib
import os
import sys

ROOT = r"C:\NTUST_PAPER"
OUT = os.path.join(ROOT, "outputs")
HERE = os.path.dirname(os.path.abspath(__file__))

CONTENT_HASH_UTILS = [
    "CONTENT_HASH_IMPLEMENTATION.md", "CONTENT_HASH_USAGE_GUIDE.md", "SESSION_SUMMARY.md", "GPU_STATUS_REPORT.md",
    "CLASSIFICATION_COMPLETE.md", "backfill_content_hash.py", "backfill_content_hash_quiet.py",
    "migrate_add_content_hash.py", "dry_run_test.py", "integration_test.py", "test_deduplication.py",
    "test_single_pdf.py", "verify_content_hash_system.py", "verify_schema.py", "check2.py", "check_db.py",
    "check_db_status.py", "check_schema.py", "analyze_remaining.py", "analyze_unclassified.py",
    "deep_analyze_tags.py", "final_readiness.py", "final_workflow_verification.py", "refine_normalized_db.py",
    "discover_and_download_extensions.py", "pipeline_output.txt", "upgrade_round2.log",
]
LEGACY_MAY = [
    "TASK2B_EXTERNAL_VALIDATION.md", "TASK2B_EXTERNAL_VALIDATION_RESULTS.csv", "TASK2B_SUMMARY.json",
    "TASK3_RANK_COMPARISON.csv", "TASK3_SUMMARY.json", "TASK3_TEMPORAL_PREDICTION.md",
    "TASK3_TEMPORAL_PREDICTION_RESULTS.csv", "TASK_B_AND_C_COMPLETION_REPORT.md", "task1_analysis.py",
    "task2_arxiv_collection.py", "task2_internal_validation.py", "task2b_arxiv_external_validation.py",
    "task3_temporal_prediction.py", "simple_task1.py", "COMPLETION_REPORT_2026-05-06.md",
    "FINAL_COMPLETION_REPORT_2026-05-06.md", "FINAL_VALIDATION_SUMMARY_2026-05-06.md",
    "PRE_SUBMISSION_VERIFICATION_2026-05-06.md", "CHAPTER_3_METHODOLOGY_COMPLETE.md",
    "complete_thesis_sections_4_2_4_3.md", "generate_obsidian_vault.py",
    "generate_enhanced_obsidian_visualization.py", "regenerate_backbone_visualization.py",
]
PIPELINE_DOCS = ["PIPELINE_CORE_EXTRACTION.md", "PIPELINE_USAGE_GUIDE.md", "PROJECT_HANDOFF.md", "C_WORKSPACE_GUIDE.md"]
CAMERA_READY_0921 = ["V7_CONFERENCE_CAMERA_READY_DECISION_ORCHESTRATION_PROSE_REVISED_20260921.docx",
                     "V9_CONFERENCE_CAMERA_READY_FULL_CHINESE_BODY_20260921.docx"]
V9_CANDIDATES_1004 = [
    "V9_FINAL_SUBMISSION_CANDIDATE_20261004.docx", "V9_FINAL_SUBMISSION_CANDIDATE_20261005_R7_VERIFIED.docx",
    "V9_FINAL_SUBMISSION_CANDIDATE_20261005_R8_VERIFIED.docx", "V9_FINAL_SUBMISSION_CANDIDATE_20261005_R9_VERIFIED.docx",
    "V9_FINAL_PATCH_REPORT_20261004.md", "V9_FINAL_SUBMISSION_AUDIT_20261004.md",
    "V9_R3_FIGURES_TABLES_CHANGELOG_20261004.md", "V9_RESULTS_SENSITIVITY_R2_CHANGELOG_20261004.md",
]


def plan():
    moves = []
    def add(names, src_dir, dst_dir):
        for n in names:
            moves.append((os.path.join(src_dir, n), os.path.join(dst_dir, n)))
    add(CONTENT_HASH_UTILS, ROOT, os.path.join(ROOT, "ARCHIVE", "2026-04_content_hash_and_db_utilities"))
    add(["paper_kb_software.zip", "paper_kb_software (2).zip"], ROOT, os.path.join(ROOT, "ARCHIVE", "2026-04_paper_kb_software_old_zips"))
    add(PIPELINE_DOCS, ROOT, os.path.join(ROOT, "docs", "pipeline_2026-04"))
    add(LEGACY_MAY, ROOT, os.path.join(OUT, "99_LEGACY", "02_STRUCTURAL_HOLE_THESIS_ROOT_FILES_2026-05"))
    add(["Enterprise_AI_Decision_100_Papers_2021_2026.xlsx", "legacy_pdf_path_audit.csv"], ROOT,
        os.path.join(OUT, "80_HISTORY_2026", "08_AUG", "ROOT_FILES_2026-08"))
    add(CAMERA_READY_0921, ROOT, os.path.join(OUT, "80_HISTORY_2026", "09_SEP", "ROOT_CAMERA_READY_DOCX_20260921"))
    add(V9_CANDIDATES_1004, ROOT, os.path.join(OUT, "80_HISTORY_2026", "10_OCT", "ROOT_V9_FINAL_SUBMISSION_CANDIDATES_20261004"))
    add(["AI_DECISION_V1_8_REQUIRED_INPUTS_BUNDLE_20261014.zip"], ROOT, os.path.join(OUT, "10_CANONICAL_EVIDENCE", "00_INPUT_BUNDLES"))
    add(["20260911_AI_DECISION_V5_PRODUCTION"], OUT, os.path.join(OUT, "10_CANONICAL_EVIDENCE", "04_V5_PRODUCTION_FREEZE"))
    add(["20260907_submission_package_v4"], OUT, os.path.join(OUT, "80_HISTORY_2026", "09_SEP"))
    return moves


def fingerprint(path):
    if os.path.isfile(path):
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for block in iter(lambda: fh.read(1 << 20), b""):
                h.update(block)
        return "file", h.hexdigest(), os.path.getsize(path)
    count, total = 0, 0
    for dp, _, fn in os.walk(path):
        for f in fn:
            count += 1
            total += os.path.getsize(os.path.join(dp, f))
    return "dir", f"files={count}", total


def check(moves):
    problems = []
    for src, dst in moves:
        if not os.path.exists(src):
            problems.append(f"MISSING SOURCE {src}")
        if os.path.exists(dst):
            problems.append(f"DESTINATION EXISTS {dst}")
    return problems


def main():
    mode = sys.argv[1]
    moves = plan()
    # resumable: a move is pending (src only), done (dst only) or a conflict (both exist / neither exists)
    problems = [f"CONFLICT {s}" for s, d in moves if os.path.exists(s) and os.path.exists(d)] + \
        [f"MISSING {s}" for s, d in moves if not os.path.exists(s) and not os.path.exists(d)]
    for src, dst in moves:
        print(f"{os.path.relpath(src, ROOT)}  ->  {os.path.relpath(dst, ROOT)}")
    print(f"moves={len(moves)} problems={len(problems)}")
    for p in problems:
        print(p)
    if mode != "execute" or problems:
        return
    rows = []
    for src, dst in moves:
        if not os.path.exists(src) and os.path.exists(dst):
            kind, after, size_after = fingerprint(dst)
            rows.append([os.path.relpath(src, ROOT), os.path.relpath(dst, ROOT), kind, "NOT_RECORDED(rename in earlier run)", "",
                         after, size_after, "DONE_EARLIER_RUN"])
            continue
        kind, before, size_before = fingerprint(src)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        try:
            os.rename(src, dst)
        except PermissionError as exc:
            rows.append([os.path.relpath(src, ROOT), os.path.relpath(dst, ROOT), kind, before, size_before, "", "",
                         f"NOT_MOVED_LOCKED({exc.winerror})"])
            print("LOCKED, left in place:", src)
            continue
        _, after, size_after = fingerprint(dst)
        ok = before == after and size_before == size_after
        rows.append([os.path.relpath(src, ROOT), os.path.relpath(dst, ROOT), kind, before, size_before, after, size_after,
                     "OK" if ok else "MISMATCH"])
        if not ok:
            print("MISMATCH", src)
    with open(os.path.join(HERE, "MOVE_MANIFEST_20261014.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["old_path", "new_path", "kind", "fingerprint_before", "bytes_before", "fingerprint_after", "bytes_after", "verify"])
        w.writerows(rows)
    with open(os.path.join(HERE, "ROLLBACK_20261014.py"), "w", encoding="utf-8") as fh:
        fh.write('"""Reverse the 2026-10-14 reorganization: moves every file/folder back. Run: python -I ROLLBACK_20261014.py"""\n')
        fh.write("import os\nROOT = r'C:\\NTUST_PAPER'\nMOVES = [\n")
        for r in rows:
            if not r[7].startswith(("OK", "DONE")):
                continue
            fh.write(f"    ({r[1]!r}, {r[0]!r}),\n")
        fh.write("]\nfor new, old in MOVES:\n    s, d = os.path.join(ROOT, new), os.path.join(ROOT, old)\n"
                 "    if os.path.exists(d):\n        print('SKIP (exists)', d); continue\n"
                 "    os.makedirs(os.path.dirname(d), exist_ok=True); os.rename(s, d); print('restored', old)\n")
    from collections import Counter
    print("status", dict(Counter(r[7] for r in rows)))


if __name__ == "__main__":
    main()
