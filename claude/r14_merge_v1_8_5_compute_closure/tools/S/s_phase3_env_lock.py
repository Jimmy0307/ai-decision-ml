"""Write 49_BASELINE_ENVIRONMENT_LOCK.json. Usage: python -I -B s_phase3_env_lock.py <work_dir> <run_ts> <out_json>"""
import hashlib
import importlib.metadata as md
import json
import platform
import re
import sys
from pathlib import Path


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    work, ts, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    rec = json.loads((work / f"baseline_{ts}_RUN_RECORD.json").read_text(encoding="utf-8"))
    code = work / f"code_baseline_{ts}"
    consts = {}
    pat = re.compile(r"^(SEED|N_NULL|DOCUMENT_NULL_REPLICATES|DOCUMENT_NULL_SEED|BURN_IN_ATTEMPTS_PER_EDGE|"
                     r"BETWEEN_SAMPLE_ATTEMPTS_PER_EDGE|EXPECTED_M|EXPECTED_ROBUST_CORE|EXPECTED_CELLS)\s*=\s*(\S+)", re.M)
    for p in sorted((code / "patched").glob("*.py")):
        consts[p.name] = dict(pat.findall(p.read_text(encoding="utf-8")))
    inp = work / "inputs_S_20261014T040934Z"
    lock = {
        "artifact": "V1_8_5_BASELINE_ENVIRONMENT_LOCK", "run_ts": ts,
        "python": {"executable": sys.executable, "version": sys.version, "implementation": platform.python_implementation(),
                   "invocation": "python -I -B -X utf8 <patched script>; cwd=<run_dir>; env PYTHONDONTWRITEBYTECODE=1 (ignored under -I; -B used)",
                   "visible_distributions_under_-I": sorted(f"{d.metadata['Name']}=={d.version}" for d in md.distributions()),
                   "stage_script_imports": "stdlib only: csv, hashlib, json, math, random, collections, datetime, pathlib, __future__"},
        "os": {"platform": platform.platform(), "machine": platform.machine(), "release": platform.release()},
        "seeds_reps_and_gate_constants_in_patched_code": consts,
        "freeze_reference_document_null_chain": {"path": str(inp / r"FREEZE\08_STATISTICAL_ANALYSIS\DOCUMENT_NULL_CHAIN_PARAMETERS.json"),
                                                 "sha256": sha(inp / r"FREEZE\08_STATISTICAL_ANALYSIS\DOCUMENT_NULL_CHAIN_PARAMETERS.json")},
        "input_hashes_stage10_freeze_copy": rec["freeze_input_hashes"],
        "freeze_input_root": rec["freeze_input_root"],
        "post_run_freeze_input_hashes_ok": rec["post_run_freeze_input_hashes_ok"],
        "code_hashes": rec["scripts"],
        "run_dir": rec["run_dir"], "code_dir": rec["code_dir"], "stages": rec["stages"],
        "run_record": {"path": str(work / f"baseline_{ts}_RUN_RECORD.json"), "sha256": sha(work / f"baseline_{ts}_RUN_RECORD.json")},
        "runner_scripts": {n: sha(Path(__file__).parent / n) for n in ("s_phase3_run_baseline.py", "s_phase3_compare.py", "s_phase3_env_lock.py", "s_v5_untouched_check.py")},
    }
    out.write_text(json.dumps(lock, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(consts))


if __name__ == "__main__":
    main()
