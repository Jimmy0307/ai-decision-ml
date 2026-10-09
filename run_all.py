from pathlib import Path
import json, subprocess, sys

ROOT = Path(__file__).resolve().parent

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def normalize_solver(d):
    d = dict(d)
    d.pop("runtime_seconds", None)
    return d

def main():
    print("=== AI x Decision x MLP v1.0 LOCAL VALIDATION ===")

    p1 = subprocess.run(
        [sys.executable, str(ROOT / "04_solver_v1_0.py")],
        cwd=ROOT, capture_output=True, text=True, check=True
    )
    (ROOT / "LOCAL_solver_results.json").write_text(p1.stdout, encoding="utf-8")
    actual_solver = json.loads(p1.stdout)
    expected_solver = load_json(ROOT / "05_solver_results_v1_0.json")
    solver_match = normalize_solver(actual_solver) == normalize_solver(expected_solver)
    print("[1/4] Solver reproduction:", "PASS" if solver_match else "FAIL")

    p2 = subprocess.run(
        [sys.executable, str(ROOT / "06_reimplementation_consistency_check_v1_0.py")],
        cwd=ROOT, capture_output=True, text=True, check=True
    )
    (ROOT / "LOCAL_consistency_results.json").write_text(p2.stdout, encoding="utf-8")
    check = json.loads(p2.stdout)

    nine = bool(check.get("official_all_pass"))
    domain = check.get("generator_vs_canonical_domain_check", {})
    constraints = bool(check.get("returned_solution_constraints_all_pass"))
    mutation = actual_solver.get("mutation_sensitivity_check", {})

    print("[2/4] 9-scenario reproduction:", "PASS" if nine else "FAIL")
    print("[3/4] Domain conformance:",
          "PASS" if domain.get("pass") and domain.get("mismatch_cases") == 0 else "FAIL",
          f"(cases={domain.get('cases')}, states={domain.get('canonical_feasible_states_counted_with_repetition')}, mismatches={domain.get('mismatch_cases')})")
    print("[4/4] Returned-solution constraints:", "PASS" if constraints else "FAIL")
    print("Mutation regression:",
          "PASS" if mutation.get("pass") else "FAIL",
          f"({mutation.get('detected_mismatch_cases')}/{mutation.get('cases')} detected)")

    ok = (
        solver_match and nine and constraints
        and domain.get("pass") and domain.get("mismatch_cases") == 0
        and mutation.get("pass")
    )
    print()
    print("FINAL LOCAL VERDICT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
