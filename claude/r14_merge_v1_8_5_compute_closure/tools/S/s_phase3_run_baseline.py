"""V1.8.5 sub-agent S, Phase 3: baseline reproduction of stages 10-13 with ORIGINAL MODEL LABELS.

No label substitution. Path-only patches (BASE root for all 4 scripts; FREEZE_ROOT for stage 10).
No hash/count/seed/rep constant is touched.
Usage: python -I s_phase3_run_baseline.py <inputs_dir> <work_dir> <cc_baseline_root> <run_ts>
"""
import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

OLD_BASE = rb'r"C:\NTUST_PAPER\outputs\20260911_AI_DECISION_V5_PRODUCTION"'
OLD_FREEZE_ROOT = b'FREEZE_ROOT = (\r\n    BASE / "09_ANALYTICAL_FREEZE"\r\n)'  # source files use CRLF
SCRIPTS = {  # name: (stage, pinned sha256)
    "DOCUMENT_DEDUP_10X12_MATRIX_ACCEPTED.py": ("10", "a3892528ecac135839681429916d8d6607f1ef4685456d9663373b49a1175cd7"),
    "NULL_MODEL_NETWORK_ANALYSIS_ACCEPTED.py": ("11", "cd96c48d685fe05d23d526638bf3d0ab7201a115f3c9cab0d908277c1d0b12e3"),
    "ROBUSTNESS_SENSITIVITY_ACCEPTED.py": ("12", "7700d98c934db95ff28dc7aba19be1ce6558fff2957bc79bff54f63a63087c19"),
    "FINAL_RESULTS_FREEZE_ACCEPTED.py": ("13", "9af8c4393fec761d0104562d6de0086a4d577e395cdcb965e3f5a2d4495fc303"),
}
FREEZE_DIR = "analytical_freeze_v2_20260918T132206Z"
FREEZE_HASHES = {
    "ANALYTICAL_FREEZE_RECORD_LEVEL.csv": "fbb5f59286d308771d5db77b176abebab8ef851a896652a3807ebf6a4b335a8f",
    "ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv": "9ee5fd537fed2819c0ac7998d6a786cc8f90dd008ebc1758bb92c8e7487c2e92",
    "ANALYTICAL_FREEZE_CANONICAL.json": "9a4e8fc2ca2a49642ac801888e571b44c157a6bd5b06fe5c1cbd9ff1a891867a",
    "ANALYTICAL_FREEZE_MANIFEST_V2.json": "69c7a7dfaabd54081b8278945a9c50f74afe89961e60813e99a5b78106385e79",
    "ANALYTICAL_FREEZE_SIDE_LEVEL.csv": "7704e743610492961ee5e7342595096cc8bfaa500dbd1d9684e70c72a4d8574a",
    "ANALYTICAL_PAIR_EXCLUDED_RECORDS.csv": "d53c5e955f4dec1e23a21250542a3879cd8a5fa1bb5109bfdedc12df615161f4",
    "ANALYTICAL_FREEZE_SUMMARY_V2.md": "e4d0a638d1e4193238835bcd0120ac25b56dc37c71eddbd52a644e53ca5a951f",
}


def sha_b(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha(p: Path) -> str:
    return sha_b(p.read_bytes())


def main():
    inp, work, cc_root, ts = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
    run_dir = cc_root / ts
    code_dir = work / f"code_baseline_{ts}"
    fin_root = work / f"run_inputs_baseline_{ts}" / "09_ANALYTICAL_FREEZE"
    logs = work / "logs"
    for d in (run_dir, code_dir, fin_root.parent):
        if d.exists():
            sys.exit(f"refusing to reuse existing dir {d}")
    run_dir.mkdir(parents=True)
    (code_dir / "original").mkdir(parents=True)
    (code_dir / "patched").mkdir()
    (code_dir / "diffs").mkdir()
    logs.mkdir(exist_ok=True)
    # 1. stage-10 input: copy of the frozen analytical freeze (from hash-verified WORK copy)
    src_fz = inp / "V5" / "09_ANALYTICAL_FREEZE" / FREEZE_DIR
    dst_fz = fin_root / FREEZE_DIR
    dst_fz.mkdir(parents=True)
    for n, h in FREEZE_HASHES.items():
        shutil.copyfile(src_fz / n, dst_fz / n)
        if sha(src_fz / n) != h or sha(dst_fz / n) != h:
            sys.exit(f"freeze copy hash mismatch {n}")
    (fin_root / "LATEST_ANALYTICAL_FREEZE_V2.txt").write_text(str(dst_fz), encoding="utf-8")
    # 2. code copies + path-only patches
    new_base = ('r"' + str(run_dir) + '"').encode("utf-8")
    new_freeze = ('FREEZE_ROOT = (\r\n    Path(r"' + str(fin_root) + '")\r\n)').encode("utf-8")
    record = {"run_ts": ts, "run_dir": str(run_dir), "code_dir": str(code_dir), "freeze_input_root": str(fin_root),
              "freeze_input_hashes": FREEZE_HASHES, "scripts": {}, "stages": []}
    for name, (stage, pin) in SCRIPTS.items():
        orig = (inp / "V5" / "work" / "stage2_strict_v102" / name).read_bytes()
        if sha_b(orig) != pin:
            sys.exit(f"script hash mismatch {name}")
        (code_dir / "original" / name).write_bytes(orig)
        if orig.count(OLD_BASE) != 1:
            sys.exit(f"BASE literal count != 1 in {name}")
        patched = orig.replace(OLD_BASE, new_base)
        if stage == "10":
            if patched.count(OLD_FREEZE_ROOT) != 1:
                sys.exit("FREEZE_ROOT block not found exactly once")
            patched = patched.replace(OLD_FREEZE_ROOT, new_freeze)
        (code_dir / "patched" / name).write_bytes(patched)
        diff = difflib.unified_diff(orig.decode("utf-8").splitlines(keepends=True), patched.decode("utf-8").splitlines(keepends=True),
                                    fromfile=f"V5/work/stage2_strict_v102/{name}", tofile=f"WORK/code_baseline_{ts}/patched/{name}")
        (code_dir / "diffs" / (name + ".diff")).write_text("".join(diff), encoding="utf-8")
        record["scripts"][name] = {"stage": stage, "original_sha256": pin, "patched_sha256": sha_b(patched)}
    # 3. run stages
    env = {k: v for k, v in os.environ.items()}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    for name, (stage, _) in SCRIPTS.items():
        cmd = [sys.executable, "-I", "-B", "-X", "utf8", str(code_dir / "patched" / name)]
        t0 = time.time()
        proc = subprocess.run(cmd, cwd=str(run_dir), capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
        log = logs / f"baseline_{ts}_stage{stage}.log"
        log.write_text(f"CMD: {cmd}\nEXIT: {proc.returncode}\nELAPSED: {time.time()-t0:.1f}s\n--- STDOUT ---\n{proc.stdout}\n--- STDERR ---\n{proc.stderr}",
                       encoding="utf-8")
        record["stages"].append({"stage": stage, "script": name, "exit": proc.returncode, "elapsed_s": round(time.time() - t0, 1), "log": str(log)})
        print(f"stage {stage} exit={proc.returncode} {time.time()-t0:.1f}s")
        if proc.returncode:
            break
    record["post_run_freeze_input_hashes_ok"] = all(sha(dst_fz / n) == h for n, h in FREEZE_HASHES.items())
    (work / f"baseline_{ts}_RUN_RECORD.json").write_text(json.dumps(record, indent=1), encoding="utf-8")
    if any(s["exit"] for s in record["stages"]) or len(record["stages"]) != 4:
        sys.exit(2)


if __name__ == "__main__":
    main()
