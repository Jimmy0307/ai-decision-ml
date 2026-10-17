"""Power check for t8_tie_fuzz: how often does the OLD pess (=>) step (phi-minimizer of BR(e), then shrink)
fail while the repaired F-maximal step succeeds? Single-unit, product-grid envelopes. Stdlib, deterministic."""
import random, itertools
from t8_tie_fuzz import br, rand_inst, grid
rng = random.Random(9); old_fail = rep_fail = cases = 0
for _ in range(20000):
    units, _b = rand_inst(rng)
    for plans in units:
        for e in grid(plans):
            T = br(plans, e)
            if not T or len(T) < 2: continue
            cases += 1; mu = min(p["phi"] for p in T)
            xm = min(T, key=lambda p: (p["phi"], p["F"]))  # old choice (adversarial among phi-minimizers)
            if min(p["phi"] for p in br(plans, xm["a"])) < mu: old_fail += 1
            xt = max(T, key=lambda p: p["F"])
            if min(p["phi"] for p in br(plans, xt["a"])) < mu: rep_fail += 1
print(f"multi-element tie sets={cases} old-step failures={old_fail} repaired-step failures={rep_fail}")
