"""V1.8.5 sub-agent S, Phase B: revised audited-label reanalysis under the DUAL-MODE GUARD policy.

Usage: python -I -B s_revised_run.py <ts>
Sequence: apply 50 substitutions -> application audit -> [recount -> pin -> run] for stages 10, 11, 12, 13.
Guards re-pinned only when (1) previous-stage revised output and (2) independent recount agree.
Writes RPT\\REVISED_GUARD_DIFF.csv and WORK\\revised_<ts>_RUN_RECORD.json. Exit 2 = STOP.
"""
import csv
import difflib
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(r"C:\NTUST_PAPER\outputs\00_CURRENT\06_COMPUTE_CLOSURE_V1_8_5")
WORK = ROOT / "work"
RPT = Path(r"C:\NTUST_PAPER\outputs\00_CURRENT\02_STUDY1_FREEZE\02_STUDY1_FREEZE_V1_8_1\repo\claude\r14_merge_v1_8_5_compute_closure")
TOOLS = RPT / "tools" / "S"
BASE_TS = "20261014T041645Z"
BASE_CODE = WORK / f"code_baseline_{BASE_TS}" / "patched"
BASE_RUN = ROOT / "compute_closure" / "baseline_reproduction" / BASE_TS
SRC_FREEZE = WORK / f"run_inputs_baseline_{BASE_TS}" / "09_ANALYTICAL_FREEZE" / "analytical_freeze_v2_20260918T132206Z"
MANIFEST44 = RPT / "44_PROPAGATION_RECORD_MANIFEST.csv"
MANIFEST44_SHA = "fbc043e8d8db451db284e72a009001147515b69e02851192386e3b160fb5531a"
APPLIER_SHA = "02d141acee10dd3fa4987379247741508d2531892bb99b5c6985750fcabfbfee"
S10, S11, S12, S13 = ("DOCUMENT_DEDUP_10X12_MATRIX_ACCEPTED.py", "NULL_MODEL_NETWORK_ANALYSIS_ACCEPTED.py",
                      "ROBUSTNESS_SENSITIVITY_ACCEPTED.py", "FINAL_RESULTS_FREEZE_ACCEPTED.py")
GUARDS = []


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def stop(msg):
    print("STOP:", msg)
    write_guards()
    sys.exit(2)


def py(args, log=None, cwd=None):
    cmd = [sys.executable, "-I", "-B", "-X", "utf8"] + [str(a) for a in args]
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=cwd)
    if log:
        log.write_text(f"CMD: {cmd}\nEXIT: {p.returncode}\nELAPSED: {time.time()-t0:.1f}s\n--- STDOUT ---\n{p.stdout}\n--- STDERR ---\n{p.stderr}", encoding="utf-8")
    return p, round(time.time() - t0, 1)


def recount(*args):
    p, _ = py([TOOLS / "s_independent_recount.py", *args])
    if p.returncode:
        stop(f"recount failed {args}: {p.stderr}")
    return json.loads(p.stdout)


class Src:
    def __init__(self, name, run_dir):
        self.name = name
        self.text = (BASE_CODE / name).read_bytes().decode("utf-8")
        self.nl = "\r\n" if "\r\n" in self.text else "\n"
        old_base = 'r"' + str(BASE_RUN) + '"'
        self.sub(old_base, 'r"' + str(run_dir) + '"', "PATH", "run root BASE -> revised run dir")

    def sub(self, old, new, kind, why):
        if self.text.count(old) != 1:
            stop(f"{self.name}: target not found exactly once: {old[:60]!r}")
        self.text = self.text.replace(old, new)

    def repin_hash(self, guard, old, new, stage_src, src_sha, check):
        for k in range(1, 64):
            m = re.search('"' + old[:k] + '"' + r'(\r?\n\s*)' + '"' + old[k:] + '"', self.text)
            if m:
                if len(re.findall('"' + old[:k] + '"' + r'\r?\n\s*' + '"' + old[k:] + '"', self.text)) != 1:
                    stop(f"{self.name}: hash literal {guard} not unique")
                self.text = self.text[:m.start()] + '"' + new[:k] + '"' + m.group(1) + '"' + new[k:] + '"' + self.text[m.end():]
                GUARDS.append(dict(script=self.name, guard_name=guard, guard_type="LINEAGE_REPINNED", baseline_value=old, revised_value=new,
                                   source_stage=stage_src, source_sha256=src_sha, independent_check=check,
                                   action="REPINNED" if old != new else "UNCHANGED_VALUE_CONFIRMED", reason="previous-stage revised output sha (handoff integrity)"))
                return
        stop(f"{self.name}: hash literal {guard} not found")

    def repin_int(self, guard, old_line, new_line, old_v, new_v, stage_src, src_sha, check, reason):
        self.sub(old_line, new_line, "LINEAGE", guard)
        GUARDS.append(dict(script=self.name, guard_name=guard, guard_type="LINEAGE_REPINNED", baseline_value=old_v, revised_value=new_v,
                           source_stage=stage_src, source_sha256=src_sha, independent_check=check,
                           action="REPINNED" if old_v != new_v else "UNCHANGED_VALUE_CONFIRMED", reason=reason))

    def write(self, code_dir):
        (code_dir / "revised" / self.name).write_bytes(self.text.encode("utf-8"))
        base = (BASE_CODE / self.name).read_bytes().decode("utf-8")
        d = difflib.unified_diff(base.splitlines(keepends=True), self.text.splitlines(keepends=True),
                                 fromfile=f"code_baseline_{BASE_TS}/patched/{self.name}", tofile=f"code_revised/revised/{self.name}")
        (code_dir / "diffs" / (self.name + ".diff")).write_text("".join(d), encoding="utf-8")


def structural(script, name, value, check, src="", src_sha=""):
    GUARDS.append(dict(script=script, guard_name=name, guard_type="STRUCTURAL_INVARIANT", baseline_value=value, revised_value=value,
                       source_stage=src, source_sha256=src_sha, independent_check=check, action="UNCHANGED_HARD_FAIL", reason="structural invariant"))


def write_guards():
    if not GUARDS:
        return
    with (RPT / "REVISED_GUARD_DIFF.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["script", "guard_name", "guard_type", "baseline_value", "revised_value", "source_stage",
                                          "source_sha256", "independent_check", "action", "reason"], lineterminator="\n")
        w.writeheader()
        w.writerows(GUARDS)


def latest(run_dir, stage_dir):
    return Path(next((run_dir / stage_dir).glob("LATEST_*.txt")).read_text(encoding="utf-8").strip())


def run_stage(code_dir, run_dir, name, tag, rec):
    p, el = py([code_dir / "revised" / name], WORK / "logs" / f"revised_{rec['ts']}_stage{tag}.log", cwd=run_dir)
    rec["stages"].append({"stage": tag, "script": name, "exit": p.returncode, "elapsed_s": el,
                          "revised_sha256": sha(code_dir / "revised" / name)})
    print(f"stage {tag} exit={p.returncode} {el}s")
    if p.returncode:
        stop(f"stage {tag} failed; see log")


def main():
    ts = sys.argv[1]
    run_dir = ROOT / "compute_closure" / "revised_audited_label_analysis" / ts
    code_dir = WORK / f"code_revised_{ts}"
    if run_dir.exists() or code_dir.exists():
        stop("run/code dir exists")
    for sub in ("from_baseline", "revised", "diffs"):
        (code_dir / sub).mkdir(parents=True)
    for n in (S10, S11, S12, S13):
        (code_dir / "from_baseline" / n).write_bytes((BASE_CODE / n).read_bytes())
    rec = {"ts": ts, "run_dir": str(run_dir), "code_dir": str(code_dir), "stages": [], "recounts": {}}
    # ---- 1. apply 50 substitutions
    if sha(TOOLS / "s_apply_propagation.py") != APPLIER_SHA or sha(MANIFEST44) != MANIFEST44_SHA:
        stop("applier or manifest 44 hash differs from pre-registered value (45)")
    fz_root = run_dir / "09_ANALYTICAL_FREEZE"
    fz = fz_root / "analytical_freeze_v2_BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1"
    p, el = py([TOOLS / "s_apply_propagation.py", MANIFEST44, MANIFEST44_SHA, SRC_FREEZE, fz], WORK / "logs" / f"revised_{ts}_apply.log")
    if p.returncode:
        stop("applier failed: " + p.stdout[-500:])
    apply_rep = json.loads((fz_root / (fz.name + "_APPLY_REPORT.json")).read_text(encoding="utf-8"))
    (fz_root / "LATEST_ANALYTICAL_FREEZE_V2.txt").write_text(str(fz), encoding="utf-8")
    p, _ = py([TOOLS / "s_application_audit.py", MANIFEST44, SRC_FREEZE, fz, RPT / "51_PROPAGATION_APPLICATION_AUDIT.csv"],
              WORK / "logs" / f"revised_{ts}_application_audit.log")
    if p.returncode:
        stop("application audit failed: " + p.stdout[-800:])
    rec["apply_report"] = apply_rep
    # ---- 2. stage 10 guards
    fr = recount("freeze", fz)
    rec["recounts"]["freeze"] = fr
    agree = (fr["canonical_sha256"] == apply_rep["outputs"]["ANALYTICAL_FREEZE_CANONICAL.json"] and fr["eligible_rows_file"] == apply_rep["eligible_after"]
             and fr["eligible_rows_flag"] == fr["eligible_rows_file"] and fr["eligible_ids_file_eq_flag"] and fr["excluded"] == apply_rep["excluded_after"]
             and fr["eligible_unique_documents"] == apply_rep["eligible_documents_after"] and fr["record_rows"] == 6499 and fr["strict_unique_documents"] == 1104
             and fr["ai_families"] == 10 and fr["decision_families"] == 12 and fr["eligible_all_fully_mapped"])
    if not agree:
        stop(f"stage-10 guard recount disagreement {fr} vs {apply_rep}")
    s10 = Src(S10, run_dir)
    old_fr = 'FREEZE_ROOT = (' + s10.nl + '    Path(r"' + str(SRC_FREEZE.parent) + '")' + s10.nl + ')'
    s10.sub(old_fr, 'FREEZE_ROOT = (' + s10.nl + '    Path(r"' + str(fz_root) + '")' + s10.nl + ')', "PATH", "freeze root -> revised freeze")
    cs = sha(fz / "ANALYTICAL_FREEZE_CANONICAL.json")
    ck = "s_independent_recount.py freeze == s_apply_propagation APPLY_REPORT"
    s10.repin_hash('EXPECTED["freeze_sha256"]', "9a4e8fc2ca2a49642ac801888e571b44c157a6bd5b06fe5c1cbd9ff1a891867a", fr["canonical_sha256"], "09 revised freeze (applier)", cs, ck)
    s10.repin_int('EXPECTED["pair_eligible_records"]', '"pair_eligible_records": 3125,', f'"pair_eligible_records": {fr["eligible_rows_file"]},', 3125, fr["eligible_rows_file"],
                  "09 revised freeze", sha(fz / "ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv"), ck, "pair-eligible count from revised freeze")
    s10.repin_int('EXPECTED["pair_excluded_records"]', '"pair_excluded_records": 3374,', f'"pair_excluded_records": {fr["excluded"]},', 3374, fr["excluded"],
                  "09 revised freeze", sha(fz / "ANALYTICAL_FREEZE_RECORD_LEVEL.csv"), ck, "pair-excluded = strict - eligible from revised freeze")
    s10.repin_int('EXPECTED["pair_eligible_unique_documents"]', '"pair_eligible_unique_documents": 783,', f'"pair_eligible_unique_documents": {fr["eligible_unique_documents"]},',
                  783, fr["eligible_unique_documents"], "09 revised freeze", sha(fz / "ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv"), ck, "unique-document count from revised freeze")
    for g, v in (('EXPECTED["strict_records"]', 6499), ('EXPECTED["strict_unique_documents"]', 1104), ('EXPECTED["ai_family_count"]', 10),
                 ('EXPECTED["decision_family_count"]', 12), ("matrix_shape_exact", "10x12"), ("long_table_cell_count_exact", 120)):
        structural(S10, g, v, f"recount: records={fr['record_rows']}, strict_docs={fr['strict_unique_documents']}, ai={fr['ai_families']}, dec={fr['decision_families']}")
    s10.write(code_dir)
    run_stage(code_dir, run_dir, S10, "10", rec)
    # ---- 3. stage 11 guards
    d10 = latest(run_dir, "10_DOCUMENT_DEDUP_MATRIX")
    mr = recount("matrix", d10, fz)
    rec["recounts"]["matrix"] = mr
    if not (mr["canonical_sha256"] == mr["manifest_dedup_canonical_sha256"] and mr["edges_file_rows"] == mr["edges_recount_from_freeze"] == mr["manifest_M"]
            and mr["edge_set_equal"] and mr["raw_matrix_total"] == mr["manifest_raw_M"] == mr["raw_recount_from_freeze"] == fr["eligible_rows_file"]
            and mr["edge_unique_documents"] == mr["manifest_eligible_unique_documents"] == fr["eligible_unique_documents"]
            and mr["sum_source_record_count"] == mr["raw_recount_from_freeze"] and mr["manifest_verdict"] == "DOCUMENT_DEDUP_10X12_MATRIX_ACCEPTED"):
        stop(f"stage-11 guard recount disagreement {mr}")
    ck = "s_independent_recount.py matrix (edges recounted from revised freeze rows) == stage-10 manifest"
    s11 = Src(S11, run_dir)
    s11.repin_hash("EXPECTED_MATRIX_SHA256", "d816f34aef49b893ab7583662ac2db65640ea4cf2916fca583b1350aa04371b5", mr["canonical_sha256"], "10 revised matrix", mr["canonical_sha256"], ck)
    s11.repin_int("EXPECTED_M", "EXPECTED_M = 2180", f'EXPECTED_M = {mr["edges_file_rows"]}', 2180, mr["edges_file_rows"], "10 revised matrix",
                  sha(d10 / "DOCUMENT_PAIR_EDGES_DEDUP.csv"), ck, "document-edge count M from revised stage-10 output")
    for g, v in (("EXPECTED_AI", 10), ("EXPECTED_DECISION", 12), ("EXPECTED_CELLS", 120), ("SEED", 20260918), ("N_NULL", 10000), ("null_replicates_exact", 10000)):
        structural(S11, g, v, "unchanged literal; verified in self-audit diff")
    s11.write(code_dir)
    run_stage(code_dir, run_dir, S11, "11", rec)
    # ---- 4. stage 12 guards
    d11 = latest(run_dir, "11_NULL_MODEL_NETWORK")
    nr = recount("null", d11)
    rec["recounts"]["null"] = nr
    if not (nr["canonical_sha256"] == nr["manifest_null_model_sha256"] and nr["rows"] == 120 == nr["unique_cells"]
            and nr["manifest_verdict"] == "NULL_MODEL_NETWORK_ANALYSIS_ACCEPTED"):
        stop(f"stage-12 guard recount disagreement {nr}")
    ck = "s_independent_recount.py null/matrix == stage-10/11 manifests"
    s12 = Src(S12, run_dir)
    s12.repin_hash('EXPECTED["matrix_sha256"]', "d816f34aef49b893ab7583662ac2db65640ea4cf2916fca583b1350aa04371b5", mr["canonical_sha256"], "10 revised matrix", mr["canonical_sha256"], ck)
    s12.repin_hash('EXPECTED["null_sha256"]', "682a58f71595836cf4a297357e49c863625e38424d690a298105c792fd789b66", nr["canonical_sha256"], "11 revised null", nr["canonical_sha256"], ck)
    s12.repin_int('EXPECTED["dedup_M"]', '"dedup_M": 2180,', f'"dedup_M": {mr["edges_file_rows"]},', 2180, mr["edges_file_rows"], "10 revised matrix",
                  sha(d10 / "DOCUMENT_PAIR_EDGES_DEDUP.csv"), ck, "document-edge count M")
    s12.repin_int('EXPECTED["raw_M"]', '"raw_M": 3125,', f'"raw_M": {mr["raw_matrix_total"]},', 3125, mr["raw_matrix_total"], "10 revised matrix",
                  sha(d10 / "MATRIX_RAW_RECORD_COUNTS_10X12.csv"), ck, "raw-record M = pair-eligible count")
    s12.repin_int('EXPECTED["documents"]', '"documents": 783,', f'"documents": {mr["edge_unique_documents"]},', 783, mr["edge_unique_documents"], "10 revised matrix",
                  sha(d10 / "DOCUMENT_PAIR_EDGES_DEDUP.csv"), ck, "unique documents among edges")
    for g, v in (('EXPECTED["ai_families"]', 10), ('EXPECTED["decision_families"]', 12), ('EXPECTED["cells"]', 120), ("comparison_cells_exact", 120),
                 ("DOCUMENT_NULL_SEED", 20260919), ("DOCUMENT_NULL_REPLICATES", 5000), ("BURN_IN_ATTEMPTS_PER_EDGE", 20), ("BETWEEN_SAMPLE_ATTEMPTS_PER_EDGE", 2)):
        structural(S12, g, v, "unchanged literal; verified in self-audit diff")
    s12.write(code_dir)
    run_stage(code_dir, run_dir, S12, "12", rec)
    # ---- 5. stage 13 guards + OBSERVED_RESULT conversion
    d12 = latest(run_dir, "12_ROBUSTNESS_SENSITIVITY")
    rr = recount("robust", d12)
    rec["recounts"]["robust"] = rr
    if not (rr["canonical_sha256"] == rr["manifest_robustness_sha256"] and rr["manifest_null_sha256"] == nr["canonical_sha256"]
            and rr["comparison_rows"] == 120 and rr["manifest_verdict"] == "ROBUSTNESS_SENSITIVITY_ACCEPTED"):
        stop(f"stage-13 guard recount disagreement {rr}")
    ck = "s_independent_recount.py robust/null == stage-11/12 manifests"
    s13 = Src(S13, run_dir)
    s13.repin_hash("EXPECTED_ROBUST_SHA256", "8c0441cee3777dc9284e106579b5a1a8d9811c7aaa7c9c770ede8cb6ab639993", rr["canonical_sha256"], "12 revised robustness", rr["canonical_sha256"], ck)
    s13.repin_hash("EXPECTED_NULL_SHA256", "682a58f71595836cf4a297357e49c863625e38424d690a298105c792fd789b66", nr["canonical_sha256"], "11 revised null", nr["canonical_sha256"], ck)
    nl = s13.nl
    s13.sub("EXPECTED_CELLS = 120" + nl, "EXPECTED_CELLS = 120" + nl
            + "# V1.8.5 revised mode (DUAL-MODE GUARD policy): scientific results are recorded, never abort constants." + nl
            + 'OBSERVED_RESULT_CHECKS = {"robust_input_count_exact", "final_core_count_exact", "robust_keys_unique", "partition_exact"}' + nl,
            "OBSERVED", "observed-result set")
    old_v = ('    verdict = (' + nl + '        "FINAL_RESULTS_FREEZE_ACCEPTED"' + nl + '        if all(' + nl + '            checks.values()' + nl + '        )')
    new_v = ('    verdict = (' + nl + '        "FINAL_RESULTS_FREEZE_ACCEPTED"' + nl + '        if all(' + nl
             + '            ok for name, ok in checks.items() if name not in OBSERVED_RESULT_CHECKS' + nl + '        )')
    s13.sub(old_v, new_v, "OBSERVED", "verdict excludes observed-result checks")
    anchor = '        "full_sensitivity_set_matches_structural_set":'
    add = ('        "robust_keys_unique_structural":' + nl + '            len(robust_core_keys)' + nl + '            == len(final_rows),' + nl + nl
           + '        "final_core_matches_robust_input_structural":' + nl + '            len(final_rows)' + nl + '            == len(robust_rows),' + nl + nl
           + '        "partition_complete_structural":' + nl + '            len(enriched) + len(depleted)' + nl + '            == len(final_rows),' + nl + nl)
    s13.sub(anchor, add + anchor, "OBSERVED", "structural replacements without preset count")
    for g in ("robust_input_count_exact", "final_core_count_exact", "robust_keys_unique", "partition_exact"):
        GUARDS.append(dict(script=S13, guard_name=g, guard_type="OBSERVED_RESULT", baseline_value="EXPECTED_ROBUST_CORE=32 (blocking)",
                           revised_value="recorded in manifest checks; excluded from verdict", source_stage="13 (computed)", source_sha256="",
                           independent_check="57 re-applies predicate from q/direction columns", action="CONVERTED_TO_OBSERVED_RESULT_CHECK",
                           reason="scientific to-be-observed result must not abort revised run"))
    for g, chk in (("robust_keys_unique_structural", "len(keys)==len(final_rows)"), ("final_core_matches_robust_input_structural", "len(final_rows)==len(robust_rows)"),
                   ("partition_complete_structural", "len(enriched)+len(depleted)==len(final_rows)")):
        GUARDS.append(dict(script=S13, guard_name=g, guard_type="STRUCTURAL_INVARIANT", baseline_value="(implied by ==32 checks)", revised_value=chk,
                           source_stage="13 (computed)", source_sha256="", independent_check="hard-fail in stage 13", action="ADDED_HARD_FAIL_NO_PRESET_COUNT",
                           reason="retain uniqueness/partition/join integrity without preset result"))
    for g, v in (("EXPECTED_CELLS", 120), ("taxonomy_shape_exact", "10x12"), ("unexpected_direction_zero", 0), ("duplicate_null_keys_zero", 0),
                 ("duplicate_robust_keys_zero", 0), ("join_errors_zero", 0), ("input_errors_zero", 0), ("all_main/exact/document/raw_q05", "q<=0.05 predicate")):
        structural(S13, g, v, "unchanged; hard-fail")
    s13.write(code_dir)
    run_stage(code_dir, run_dir, S13, "13", rec)
    rec["results_dir"] = str(latest(run_dir, "13_RESULTS_FREEZE"))
    rec["dirs"] = {"10": str(d10), "11": str(d11), "12": str(d12), "13": rec["results_dir"], "freeze": str(fz)}
    write_guards()
    (WORK / f"revised_{ts}_RUN_RECORD.json").write_text(json.dumps(rec, indent=1), encoding="utf-8")
    print("REVISED_RUN=COMPLETE")


if __name__ == "__main__":
    main()
