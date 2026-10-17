#!/usr/bin/env python3
"""q1_theory_witnesses.py -- Q1 THEORY UPGRADE: consolidated computational witnesses (integrator T5).

STANDALONE, deterministic, pure Python standard library. SIMULATED_ONLY.
Assembled from the four witness parts written by theory agents T1-T4
(witness_parts/w_dl_gov.py, w_mono_rob_miss.py, w_voi.py, w_mech.py); their code is copied in below
verbatim except for (i) removal of each part's __main__ block and ALL_* list and (ii) the rename of T1's
witness_W5 -> witness_W_DL_AL3 (id clash with T2's delta witness). Nothing is imported from witness_parts
or from 51_enterprise_portfolio_solver_v2_2.py; every witness re-implements the minimal v2.2 logic it needs
from the definitions in 42_ENTERPRISE_PORTFOLIO_MODEL_v2_2.md.

STATUS OF EVERY RESULT PRINTED HERE: computational witnesses / constructive examples on hand-built algebraic
instances. A witness establishes existence or refutes a universal claim; it is NOT a proof of a general
theorem (the proofs, where they exist, are in Q/01-08). No enterprise data, no human coder data, no V7 claim.

Randomness: none of the witnesses draws random numbers (all searches are exhaustive over fixed finite
grids). The fixed seed below is declared for the contract only. Hashed data are canonicalised (sorted keys,
sorted set elements), so results do not depend on PYTHONHASHSEED.

Usage:  python q1_theory_witnesses.py            (full report + summary + verdict)
        python q1_theory_witnesses.py --hashes   (one line per witness: id sha256 PASS/FAIL)
"""
import hashlib as _q1_hashlib
import json as _q1_json
import os as _q1_os
import random as _q1_random
import sys as _q1_sys
from fractions import Fraction as _Q1Fr

Q1_FIXED_SEED = 20261014
_q1_random.seed(Q1_FIXED_SEED)

# @@PARTS@@
# ====================================================================================================
# INTEGRATOR HARNESS (T5)
# ====================================================================================================
# (namespaced id, function, part, original part id, canonical?, demonstrates)
Q1_REGISTRY = [
    # ---------------- required canonical set ----------------
    ("W1", witness_W1, "T1", "W1", True, "aligned ledgers: B = C = 30, DL = 0 (T-ORC-8 aligned)"),
    ("W2", witness_W2, "T1", "W2", True, "misaligned but envelope-blockable: B = C = 15, DL = 0"),
    ("W3", witness_W3, "T1", "W3", True, "misaligned and envelope-unblockable: B = 15, C = 10, DL = 5"),
    ("W4", witness_W4, "T1", "W4", True, "P8 governance screening 10 -> 15"),
    ("W5", witness_W5_delta, "T2", "W5", True, "Model C build decision non-monotone in reuse delta (1 -> 0 -> 1)"),
    ("W6", witness_W6, "T3", "W6", True, "vertex-conditioned VOI overstatement (vertex 1, true 1/2)"),
    ("W7", witness_W7, "T2", "W7", True, "element-level robustness counterexample (vertex ROBUST, interior FRAGILE)"),
    # ---------------- supplementary ----------------
    ("W3m", witness_W3m, "T1", "W3m", False, "minimal DL > 0 (1 BU, 1 resource, 2 plans)"),
    ("W3b", witness_W3b, "T1", "W3b", False, "DL_opt = 0 < DL_pess = 1 from a follower tie"),
    ("W3c", witness_W3c, "T1", "W3c", False, "pairwise primitives do not determine the sign of DL"),
    ("W4b", witness_W4b, "T1", "W4b", False, "screening in the opposite direction 15 -> 10"),
    ("W4c", witness_W4c, "T1", "W4c", False, "screening removes DL = 5 but price of requirement PR_B = 8"),
    ("W4d", witness_W4d, "T1", "W4d", False, "pairwise screening insufficient (worse x^M becomes best response)"),
    ("W4e", witness_W4e, "T1", "W4e", False, "GSV_pess > 0 = GSV_opt without strict reversal"),
    ("W_DL_AL3", witness_W_DL_AL3, "T1", "W5", False, "DL > 0 with F_u == F_E via a unit-only constraint (AL3)"),
    ("W5b", witness_W5b_delta, "T2", "W5b", False, "Model B monotone in delta; source-indexing assumption load-bearing"),
    ("W6b", witness_W6b, "T3", "W6b", False, "adaptive candidate set: Theta shrinkage raises MMR, VOI = -1"),
    ("W6c", witness_W6c, "T3", "W6c", False, "grid refinement: nested monotone, non-nested / edge-only not"),
    ("W6d", witness_W6d, "T3", "W6d", False, "Theta-independent benchmark: monotone but not vertex-exact"),
    ("W6e", witness_W6e, "T3", "W6e", False, "myopic VOI complementarity (single VOIs 0, joint removes regret)"),
    ("W6f", witness_W6f, "T3", "W6f", False, "no termination guarantee without discretised evidence"),
    ("W8a", witness_W8a, "T2", "W8a", False, "feasibility-changing missingness (zero-fill fabricates feasibility)"),
    ("W8b", witness_W8b, "T2", "W8b", False, "decision-changing missingness via objective (lambda, ledger split, status-quo cell)"),
    ("W8c", witness_W8c, "T2", "W8c", False, "decision-invariant but epistemically relevant missingness"),
    ("W_MECH_ABL", witness_mech_ablation, "T4", "mech_ablation", False, "M1-M4 ablation fibres (each mechanism separately decision-relevant)"),
    ("W_IA_NDV", witness_ia_ndv_sign, "T4", "ia_ndv_sign", False, "information-asymmetry sidecar: NDV sign can be + or - (NOT canonical v2.2)"),
]

# Embedded canonical anchors: exact substrings of Q/baseline/BASELINE_V2_2_RUN_STDOUT.txt (51 run, VERDICT PASS)
Q1_BASELINE_ANCHORS = {
    "T-ORC-8": "PASS T-ORC-8: aligned B=C=30; blockable B=C=15, DL=0; unblockable B=15, C=10, DL=5, VSC=15, NEV=10",
    "REG-P8": "P8 screening (10->15)",
    "T-SEN-8": "C: y_c* sequence ['1', '1', '1', '1', '0', '0', '0', '1'] over delta [0.0, 1.0, 2.0, 2.9, 3.0, 3.5, 4.0, 5.0]",
    "T-SEN-7": "vertex-conditioned VOI_v = 1 (overstated), grid VOI_v = 0.5 = true value",
    "T-SEN-3": "element-level counterexample: vertex-only classification says ROBUST, adding interior points gives FRAGILE",
}


def _q1_dumps(obj):
    return _q1_json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def _q1_canon(x):
    """Canonical JSON-serialisable form: sorted dict keys (non-str keys -> canonical JSON text), tuples -> lists,
    sets sorted by canonical text, Fraction -> 'p/q' string; rejects callables and non-finite floats."""
    if isinstance(x, bool) or x is None or isinstance(x, (int, str)):
        return x
    if isinstance(x, float):
        if x != x or x in (float("inf"), float("-inf")):
            raise ValueError("non-finite float in witness data")
        return x
    if isinstance(x, _Q1Fr):
        return "%d/%d" % (x.numerator, x.denominator) if x.denominator != 1 else "%d" % x.numerator
    if isinstance(x, dict):
        out = {}
        for k, v in x.items():
            ks = k if isinstance(k, str) else _q1_dumps(_q1_canon(k))
            if ks in out:
                raise ValueError("canonical key collision: %r" % ks)
            out[ks] = _q1_canon(v)
        return out
    if isinstance(x, (list, tuple)):
        return [_q1_canon(v) for v in x]
    if isinstance(x, (set, frozenset)):
        return sorted((_q1_canon(v) for v in x), key=_q1_dumps)
    raise TypeError("non-canonical object in witness data: %r" % type(x))


def _q1_run_one(nid, fn, part, orig, canonical):
    raw = fn()
    if raw.get("id") != orig:
        raise AssertionError("part id mismatch for %s: %r != %r" % (nid, raw.get("id"), orig))
    for key in ("id", "title", "source_test", "inputs", "rankings", "choices", "outputs", "expected", "pass",
                "minimality"):
        if key not in raw:
            raise AssertionError("%s: contract key %r missing" % (nid, key))
    data = dict(raw)
    data["id"] = nid
    data["part"] = part
    data["part_id"] = orig
    data["set"] = "CANONICAL" if canonical else "SUPPLEMENTARY"
    data["status"] = "SIMULATED_ONLY computational witness / constructive example (not a proof)"
    canon = _q1_canon(data)
    sha = _q1_hashlib.sha256(_q1_dumps(canon).encode("ascii")).hexdigest()
    return canon, sha


def _q1_run_all():
    return [(nid, part, canonical, demo) + _q1_run_one(nid, fn, part, orig, canonical)
            for nid, fn, part, orig, canonical, demo in Q1_REGISTRY]


def _q1_cross_checks(res):
    by = {r[0]: r[4] for r in res}
    w1, w2, w3, w4 = (by[k]["outputs"] for k in ("W1", "W2", "W3", "W4"))
    w5, w6, w7 = by["W5"], by["W6"]["outputs"], by["W7"]["outputs"]
    return [
        ("T-ORC-8 aligned B=C=30, DL=0 (W1)",
         w1["B"] == 30 and w1["C_opt"] == 30 and w1["C_pess"] == 30 and w1["DL_opt"] == 0 and w1["DL_pess"] == 0),
        ("T-ORC-8 blockable B=C=15, DL=0 (W2)",
         w2["B"] == 15 and w2["C_opt"] == 15 and w2["C_pess"] == 15 and w2["DL_opt"] == 0 and w2["DL_pess"] == 0),
        ("T-ORC-8 unblockable B=15, C=10, DL=5, VSC=15, NEV=10 (W3)",
         w3["B"] == 15 and w3["C_opt"] == 10 and w3["C_pess"] == 10 and w3["DL_opt"] == 5 and w3["DL_pess"] == 5
         and w3["VSC"] == 15 and w3["NEV_opt"] == 10 and w3["NEV_pess"] == 10),
        ("REG P8 screening 10 -> 15 (W4)",
         w4["C_opt_loose"] == 10 and w4["C_opt_strict"] == 15 and w4["C_pess_loose"] == 10
         and w4["C_pess_strict"] == 15),
        ("T-SEN-8 C sequence 1,1,1,1,0,0,0,1 over delta [0,1,2,2.9,3,3.5,4,5] (W5)",
         w5["outputs"]["seq_pess_strict"] == ["1", "1", "1", "1", "0", "0", "0", "1"]
         and w5["inputs"]["delta_grid"] == [0.0, 1.0, 2.0, 2.9, 3.0, 3.5, 4.0, 5.0]),
        ("T-SEN-7 vertex VOI_v = 1, true VOI_v = 1/2 (W6)",
         w6["VOI_v vertex"] == "1" and w6["VOI_v exact"] == "1/2"),
        ("T-SEN-3 element-level vertex ROBUST / interior FRAGILE (W7)",
         w7["B_element_vertex_class"] == "ROBUST" and w7["B_element_grid_class"] == "FRAGILE"),
    ]


def _q1_baseline_file_check():
    here = _q1_os.path.dirname(_q1_os.path.abspath(__file__))
    p = _q1_os.path.join(here, "baseline", "BASELINE_V2_2_RUN_STDOUT.txt")
    if not _q1_os.path.exists(p):
        return "NOT_FOUND (embedded anchors used; not counted as FAIL)", True
    with open(p, encoding="utf-8") as fh:
        txt = fh.read()
    missing = [k for k, s in Q1_BASELINE_ANCHORS.items() if s not in txt]
    if missing:
        return "MISMATCH: anchors not found verbatim: %s" % missing, False
    return "MATCH: all %d anchors found verbatim in baseline/BASELINE_V2_2_RUN_STDOUT.txt" % len(Q1_BASELINE_ANCHORS), True


def _q1_block(label, obj):
    txt = _q1_json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False)
    return "  %s:\n" % label + "\n".join("    " + line for line in txt.splitlines())


def _q1_print_witness(nid, part, demo, canon, sha):
    print("")
    print("-" * 110)
    print("[%s] %s   (%s; part %s, part id %s)" % (nid, canon["title"], canon["set"], part, canon["part_id"]))
    print("-" * 110)
    print("  demonstrates: " + demo)
    print("  source test mapping: " + str(canon["source_test"]))
    for label, key in (("inputs (algebraic)", "inputs"), ("rankings", "rankings"), ("choices", "choices"),
                       ("outputs", "outputs"), ("expected", "expected")):
        print(_q1_block(label, canon[key]))
    print("  minimality: " + str(canon["minimality"]))
    print("  result: " + ("PASS" if canon["pass"] else "FAIL"))
    print("  witness_sha256: " + sha)


def main(argv):
    res1 = _q1_run_all()
    res2 = _q1_run_all()       # second in-process run (determinism)
    det_ok = [(r[0], r[5]) for r in res1] == [(r[0], r[5]) for r in res2]
    if "--hashes" in argv:
        for nid, part, canonical, demo, canon, sha in res1:
            print("%-11s %s %s" % (nid, sha, "PASS" if canon["pass"] else "FAIL"))
        print("IN_PROCESS_DETERMINISM:", "PASS" if det_ok else "FAIL")
        return 0
    print("=" * 110)
    print("Q1 THEORY WITNESSES -- consolidated computational witnesses (integrator T5)")
    print("SIMULATED_ONLY. Constructive examples / computational witnesses on algebraic instances; NOT proofs of")
    print("general theorems; no enterprise data, no human coder data, no V7 / empirical validity claim. Model: 42 v2.2.")
    print("Fixed seed (declared; no witness draws random numbers): %d" % Q1_FIXED_SEED)
    print("Hash = SHA-256 of canonical JSON (sorted keys, separators (',',':'), ASCII) of the full witness record.")
    print("Bounded search inside W5: 3 exhaustive single-follower families (sizes printed in W5 outputs.search).")
    print("=" * 110)
    for nid, part, canonical, demo, canon, sha in res1:
        _q1_print_witness(nid, part, demo, canon, sha)
    checks = _q1_cross_checks(res1)
    bstat, bok = _q1_baseline_file_check()
    print("")
    print("=" * 110)
    print("CROSS-CHECK AGAINST CANONICAL 51 BASELINE (Q/baseline/BASELINE_V2_2_RUN_STDOUT.txt)")
    for k, s in Q1_BASELINE_ANCHORS.items():
        print("  anchor %-8s %s" % (k, s))
    for name, ok in checks:
        print("  %-4s %s" % ("PASS" if ok else "FAIL", name))
    print("  baseline file: " + bstat)
    print("")
    print("SUMMARY TABLE")
    print("  %-11s %-13s %-4s %-6s %-64s %s" % ("id", "set", "part", "result", "sha256", "demonstrates"))
    for nid, part, canonical, demo, canon, sha in res1:
        print("  %-11s %-13s %-4s %-6s %-64s %s" % (nid, canon["set"], part, "PASS" if canon["pass"] else "FAIL",
                                                   sha, demo))
    n = len(res1)
    npass = sum(1 for r in res1 if r[4]["pass"])
    ncan = sum(1 for r in res1 if r[2])
    setsha = _q1_hashlib.sha256("".join(r[0] + ":" + r[5] + "\n" for r in res1).encode("ascii")).hexdigest()
    print("")
    print("  witnesses: %d (canonical %d, supplementary %d); PASS %d / FAIL %d" % (n, ncan, n - ncan, npass, n - npass))
    print("  cross-checks: %d/%d PASS" % (sum(1 for c in checks if c[1]), len(checks)))
    print("  IN_PROCESS_DETERMINISM (2 runs, identical per-witness hashes): " + ("PASS" if det_ok else "FAIL"))
    print("  witness_set_sha256: " + setsha)
    verdict = npass == n and all(c[1] for c in checks) and bok and det_ok
    print("Q1_WITNESS_VERDICT: " + ("PASS" if verdict else "FAIL"))
    return 0 if verdict else 1


if __name__ == "__main__":
    _q1_sys.exit(main(_q1_sys.argv[1:]))
