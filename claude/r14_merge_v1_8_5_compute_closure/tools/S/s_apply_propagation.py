"""V1.8.5 BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1 applier (pre-registered; NOT executed in Phase 1-3).

Applies exactly the 50 rows of 44_PROPAGATION_RECORD_MANIFEST.csv to a COPY of the V5 analytical freeze
(stage-09 output). Every other record is written back unchanged (ORIGINAL_MODEL label). No inference,
extrapolation, imputation or rule-based relabelling of any other record.

Field writes mirror the reference implementation prepare_and_run_corrected_sidecar.py lines 365-434
(sha256 021e3d10...6ef3): record-level CSV, pair-eligible CSV, canonical JSON record fields and counts,
manifest counts. SIDE_LEVEL / EXCLUDED / SUMMARY files are carried over unchanged, as in the reference.

Usage: python -I s_apply_propagation.py <manifest_csv> <manifest_sha256> <freeze_copy_dir> <out_freeze_dir>
Exit 2 = STOP (hash mismatch, row-count mismatch, old-label mismatch, out dir exists).
"""
import csv
import hashlib
import json
import shutil
import sys
from pathlib import Path

EXPECTED_FREEZE = {
    "ANALYTICAL_FREEZE_RECORD_LEVEL.csv": "fbb5f59286d308771d5db77b176abebab8ef851a896652a3807ebf6a4b335a8f",
    "ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv": "9ee5fd537fed2819c0ac7998d6a786cc8f90dd008ebc1758bb92c8e7487c2e92",
    "ANALYTICAL_FREEZE_CANONICAL.json": "9a4e8fc2ca2a49642ac801888e571b44c157a6bd5b06fe5c1cbd9ff1a891867a",
    "ANALYTICAL_FREEZE_MANIFEST_V2.json": "69c7a7dfaabd54081b8278945a9c50f74afe89961e60813e99a5b78106385e79",
    "ANALYTICAL_FREEZE_SIDE_LEVEL.csv": "7704e743610492961ee5e7342595096cc8bfaa500dbd1d9684e70c72a4d8574a",
}
FIELDS = ["analytical_pair_eligible", "left_final_family", "right_final_family", "left_final_status",
          "right_final_status", "mapping_completeness", "analytical_exclusion_reason"]
TRUE = ("true", "1", "yes")


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def readcsv(p: Path):
    with p.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def writecsv(p: Path, rows, fields):
    with p.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def stop(msg):
    print("STOP:", msg)
    sys.exit(2)


def main():
    man_p, man_sha, src, out = Path(sys.argv[1]), sys.argv[2].lower(), Path(sys.argv[3]), Path(sys.argv[4])
    if sha(man_p) != man_sha:
        stop("manifest sha256 differs from pre-registered value")
    if out.exists():
        stop(f"output exists: {out}")
    for n, h in EXPECTED_FREEZE.items():
        if sha(src / n) != h:
            stop(f"freeze copy hash mismatch: {n}")
    manifest = list(csv.DictReader(man_p.open(encoding="utf-8", newline="")))
    classes = sorted(r["precedence_class"] for r in manifest)
    if len(manifest) != 50 or len({r["record_id"] for r in manifest}) != 50 or \
            classes.count("RECONCILED_FINAL") != 20 or classes.count("FIRST_CODER") != 30:
        stop("manifest is not exactly 20 RECONCILED_FINAL + 30 FIRST_CODER unique records")
    shutil.copytree(src, out)
    rec_p, elig_p = out / "ANALYTICAL_FREEZE_RECORD_LEVEL.csv", out / "ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv"
    can_p, mf_p = out / "ANALYTICAL_FREEZE_CANONICAL.json", out / "ANALYTICAL_FREEZE_MANIFEST_V2.json"
    base = readcsv(rec_p)
    fieldnames = list(base[0])
    by_id = {r["record_id"]: r for r in manifest}
    new_rows, touched = [], 0
    for row in base:
        m = by_id.get(row["record_id"])
        if m is None:
            new_rows.append(row)
            continue
        if any(row[k] != m[f"old_model_{k}"] for k in FIELDS):
            stop(f"old model label in freeze differs from manifest: {row['record_id']}")
        out_row = dict(row)
        for k in FIELDS:
            out_row[k] = m[f"final_{k}"]
        new_rows.append(out_row)
        touched += 1
    if touched != 50 or len(new_rows) != len(base):
        stop("join did not touch exactly 50 records")
    unchanged_other = sum(1 for a, b in zip(base, new_rows) if a["record_id"] not in by_id and a == b)
    if unchanged_other != len(base) - 50:
        stop("a non-audited record changed")
    writecsv(rec_p, new_rows, fieldnames)
    eligible = [r for r in new_rows if r["analytical_pair_eligible"].strip().lower() in TRUE]
    writecsv(elig_p, eligible, fieldnames)
    docs = len({r["document_id"] for r in eligible if r["document_id"]})
    canonical = json.loads(can_p.read_text(encoding="utf-8"))
    canon_by = {r["record_id"]: r for r in canonical["records"]}
    for r in new_rows:
        c = canon_by[r["record_id"]]
        c["left_family"], c["right_family"] = r["left_final_family"], r["right_final_family"]
        c["left_status"], c["right_status"] = r["left_final_status"], r["right_final_status"]
        c["mapping_completeness"] = r["mapping_completeness"]
        c["pair_eligible"] = r["analytical_pair_eligible"].strip().lower() in TRUE
    canonical["pair_eligible_records"] = len(eligible)
    canonical["pair_excluded_records"] = len(new_rows) - len(eligible)
    canonical["local_sensitivity_derivative"] = {
        "scope": "BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1", "baseline_canonical_sha256": EXPECTED_FREEZE["ANALYTICAL_FREEZE_CANONICAL.json"],
        "baseline_record_level_sha256": EXPECTED_FREEZE["ANALYTICAL_FREEZE_RECORD_LEVEL.csv"], "human_audit_record_count": 50,
        "reconciled_overlap_count": 20, "unaudited_records_changed": 0, "relation_dimension_changed": False,
        "propagation_manifest_sha256": man_sha}
    can_p.write_text(json.dumps(canonical, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    mf = json.loads(mf_p.read_text(encoding="utf-8"))
    mf["canonical_sha256"] = sha(can_p)
    mf["pair_eligible_records"] = len(eligible)
    mf["pair_excluded_records"] = len(new_rows) - len(eligible)
    mf["local_sensitivity_derivative"] = canonical["local_sensitivity_derivative"]
    mf_p.write_text(json.dumps(mf, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = {"records": len(new_rows), "touched": touched, "eligible_after": len(eligible),
              "eligible_documents_after": docs, "excluded_after": len(new_rows) - len(eligible),
              "outputs": {p.name: sha(p) for p in sorted(out.iterdir()) if p.is_file()}}
    (out.parent / (out.name + "_APPLY_REPORT.json")).write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
