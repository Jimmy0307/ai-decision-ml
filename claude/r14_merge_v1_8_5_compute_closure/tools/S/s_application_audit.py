"""Independent audit of the 50-record propagation (stdlib; imports no pipeline/applier code).

Usage: python -I -B s_application_audit.py <manifest44> <baseline_freeze_dir> <revised_freeze_dir> <out_csv>
Raw-row comparison: every non-target record row must be byte-identical (raw CSV text span) to the baseline freeze.
Exit 2 if any count differs from the policy (TARGETED=MATCHED=REPLACED=50, UNMATCHED=DUPLICATE_JOIN=UNAUTHORIZED=0).
"""
import csv
import hashlib
import io
import json
import sys
from pathlib import Path

FIELDS = ["analytical_pair_eligible", "left_final_family", "right_final_family", "left_final_status",
          "right_final_status", "mapping_completeness", "analytical_exclusion_reason"]


def raw_rows(p: Path):
    lines = io.StringIO(p.read_bytes().decode("utf-8-sig"), newline="").readlines()
    buf = []

    def gen():
        for ln in lines:
            buf.append(ln)
            yield ln
    out = []
    for row in csv.reader(gen()):
        out.append((row, "".join(buf)))
        buf.clear()
    return out


def keyed(p: Path):
    rr = raw_rows(p)
    hdr = rr[0][0]
    i = hdr.index("record_id")
    d = {}
    for row, raw in rr[1:]:
        d.setdefault(row[i], []).append((dict(zip(hdr, row)), raw))
    return hdr, rr[0][1], d


def main():
    man_p, base, rev, out = (Path(a) for a in sys.argv[1:5])
    man = list(csv.DictReader(man_p.open(encoding="utf-8", newline="")))
    targets = {m["record_id"]: m for m in man}
    rows, s = [], {}
    b_hdr, b_hraw, b = keyed(base / "ANALYTICAL_FREEZE_RECORD_LEVEL.csv")
    r_hdr, r_hraw, r = keyed(rev / "ANALYTICAL_FREEZE_RECORD_LEVEL.csv")
    s["HEADER_IDENTICAL"] = b_hraw == r_hraw
    s["TARGETED"] = len(targets)
    s["MATCHED"] = sum(1 for k in targets if len(r.get(k, [])) == 1)
    s["UNMATCHED"] = sum(1 for k in targets if k not in r)
    s["DUPLICATE_JOIN"] = sum(1 for k in r if len(r[k]) > 1) + sum(1 for k in b if len(b[k]) > 1)
    s["RECORD_SET_EQUAL"] = set(b) == set(r)
    applied, changed, other_field_changes, recs = 0, 0, 0, []
    for k, m in targets.items():
        rv = r[k][0][0]
        bv = b[k][0][0]
        ok = all(rv[f] == m[f"final_{f}"] for f in FIELDS) and all(bv[f] == m[f"old_model_{f}"] for f in FIELDS)
        applied += ok
        ch = [f for f in FIELDS if rv[f] != bv[f]]
        changed += bool(ch)
        oth = [f for f in r_hdr if f not in FIELDS and rv[f] != bv[f]]
        other_field_changes += bool(oth)
        recs.append({"row_type": "RECORD", "key": k, "value": m["translation_action"], "expected": m["precedence_class"],
                     "status": "APPLIED" if ok and not oth else "FAIL", "detail": "changed=" + "|".join(ch) + ("; NON_LABEL_FIELD_CHANGED=" + "|".join(oth) if oth else "")})
    s["REPLACED_HUMAN_LABEL_APPLIED"] = applied
    s["FIELD_CHANGING_RECORDS"] = changed
    s["TARGET_NON_LABEL_FIELD_CHANGES"] = other_field_changes
    non_target_diff = [k for k in b if k not in targets and (k not in r or b[k][0][1] != r[k][0][1])]
    s["UNAUTHORIZED_REPLACEMENT"] = len(non_target_diff) + other_field_changes
    s["NON_TARGET_ROWS_BYTE_IDENTICAL"] = sum(1 for k in b if k not in targets and k in r and b[k][0][1] == r[k][0][1])
    # eligible file: non-target rows byte-identical and order preserved
    _, eh_b, eb = keyed(base / "ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv")
    _, eh_r, er = keyed(rev / "ANALYTICAL_PAIR_ELIGIBLE_RECORDS.csv")
    s["ELIGIBLE_BEFORE"], s["ELIGIBLE_AFTER"] = len(eb), len(er)
    s["ELIGIBLE_NON_TARGET_UNAUTHORIZED"] = sum(1 for k in set(eb) | set(er) if k not in targets and (eb.get(k, [[None, None]])[0][1] != er.get(k, [[None, None]])[0][1]))
    # canonical: non-target records parsed-equal
    cb = {x["record_id"]: x for x in json.loads((base / "ANALYTICAL_FREEZE_CANONICAL.json").read_text(encoding="utf-8"))["records"]}
    cr = {x["record_id"]: x for x in json.loads((rev / "ANALYTICAL_FREEZE_CANONICAL.json").read_text(encoding="utf-8"))["records"]}
    s["CANONICAL_NON_TARGET_UNAUTHORIZED"] = sum(1 for k in cb if k not in targets and cb[k] != cr.get(k))
    for n in ("ANALYTICAL_FREEZE_SIDE_LEVEL.csv", "ANALYTICAL_PAIR_EXCLUDED_RECORDS.csv", "ANALYTICAL_FREEZE_SUMMARY_V2.md"):
        s[f"UNCHANGED_{n}"] = hashlib.sha256((base / n).read_bytes()).hexdigest() == hashlib.sha256((rev / n).read_bytes()).hexdigest()
    expect = {"TARGETED": 50, "MATCHED": 50, "UNMATCHED": 0, "DUPLICATE_JOIN": 0, "REPLACED_HUMAN_LABEL_APPLIED": 50,
              "FIELD_CHANGING_RECORDS": 37, "UNAUTHORIZED_REPLACEMENT": 0, "ELIGIBLE_NON_TARGET_UNAUTHORIZED": 0,
              "CANONICAL_NON_TARGET_UNAUTHORIZED": 0, "TARGET_NON_LABEL_FIELD_CHANGES": 0}
    summ = []
    for k, v in s.items():
        e = expect.get(k, True if isinstance(v, bool) else "")
        summ.append({"row_type": "SUMMARY", "key": k, "value": v, "expected": e, "status": "PASS" if (e == "" or v == e) else "FAIL", "detail": ""})
    defs = {"REPLACED_HUMAN_LABEL_APPLIED": "records whose 7 pipeline fields equal the manifest final_* values (human label applied per rule, incl. LEAVE = model value retained by rule)",
            "FIELD_CHANGING_RECORDS": "records with >=1 pipeline field differing from the baseline freeze",
            "UNAUTHORIZED_REPLACEMENT": "non-target rows not byte-identical to baseline + target rows with a non-label field changed"}
    for x in summ:
        x["detail"] = defs.get(x["key"], "")
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["row_type", "key", "value", "expected", "status", "detail"], lineterminator="\n")
        w.writeheader()
        w.writerows(summ + recs)
    fails = [x for x in summ + recs if x["status"] == "FAIL"]
    print(json.dumps({x["key"]: x["value"] for x in summ}))
    if fails:
        print("FAILS:", [x["key"] for x in fails])
        sys.exit(2)


if __name__ == "__main__":
    main()
