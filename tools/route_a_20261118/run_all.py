"""Regenerate all route-A outputs in dependency order (about 25 minutes; step 3b dominates)."""
import subprocess, sys, os, time

STEPS = ["step0_lineage.py", "step3_pipeline_validation.py", "step3b_seed_stability.py", "step4_exclusion_bias.py",
         "step4e_sensitivity.py", "step5_track_sensitivity.py", "step6_temporal_validity.py", "step1_taxonomy.py",
         "step2_reliability_design.py", "build_codebook.py", "build_master_table.py"]
here = os.path.dirname(os.path.abspath(__file__))
for s in STEPS:
    t = time.time()
    print(f"== {s}", flush=True)
    r = subprocess.run([sys.executable, os.path.join(here, s)], cwd=here, stdout=subprocess.DEVNULL)
    print(f"   exit {r.returncode} in {time.time() - t:.0f}s", flush=True)
    if r.returncode:
        sys.exit(r.returncode)
r = subprocess.run([sys.executable, "-m", "unittest", "test_route_a", "-v"], cwd=here)
sys.exit(r.returncode)
