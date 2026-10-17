"""T8 falsification search (NOT a proof): Lemma E' and Lemma DL-1o/p under 51's exact tie rule
g(m) = m - TOL*max(1,|m|) (51 l.673), exact affordability, multi-BU, 2 pooled resources (negative
components allowed), coupled budget. Envelopes: exact product grid of plan coordinates (covers every
distinct affordable set), compared with E' = {a(x)}. Also: adversarial variant 'pick any tie element'
(42 l.476 proof sentence) to confirm it can fail, and 51's affordability slack variant.
Pure stdlib, deterministic."""
import itertools, random, sys
TOL = 1e-9

def g(m):
    return m - TOL * max(1.0, abs(m))

def br(plans, e, slack=0.0):
    S = [p for p in plans if all(p["a"][h] <= e[h] + slack for h in range(len(e)))]
    if not S:
        return None
    m = max(p["F"] for p in S)
    return [p for p in S if p["F"] >= g(m)]

def vals(T):
    return max(p["phi"] for p in T), min(p["phi"] for p in T)

def leader(units, bbar, env_sets, slack=0.0):
    best = {"opt": None, "pess": None}
    cands = []
    for plans, envs in zip(units, env_sets):
        c = []
        for e in envs:
            T = br(plans, e, slack)
            if T is not None:
                c.append((e, vals(T)))
        if not c:
            return best
        cands.append(c)
    for combo in itertools.product(*cands):
        if any(sum(c[0][h] for c in combo) > bbar[h] + 1e-12 for h in range(len(bbar))):
            continue
        for i, mode in enumerate(("opt", "pess")):
            v = sum(c[1][i] for c in combo)
            if best[mode] is None or v > best[mode]:
                best[mode] = v
    return best

def first_bests(units, bbar):
    sols, top = [], None
    for prof in itertools.product(*units):
        if any(sum(p["a"][h] for p in prof) > bbar[h] + 1e-12 for h in range(len(bbar))):
            continue
        v = sum(p["phi"] for p in prof)
        sols.append((v, prof))
        top = v if top is None or v > top else top
    return top, [p for v, p in sols if v == top]

def self_enf(prof, units, mode):
    for p, plans in zip(prof, units):
        T = br(plans, p["a"])
        if p not in T:
            return False
        if mode == "pess" and min(q["phi"] for q in T) < p["phi"]:
            return False
    return True

def rand_inst(rng):
    U = rng.choice([1, 2, 3])
    H = 2
    scale = rng.choice([1.0, 1e3, -1e3, 1e6, -1e6, 0.3, -0.7])
    units = []
    for u in range(U):
        n = rng.randint(2, 4)
        plans = []
        for k in range(n):
            a = tuple(rng.choice([-1, 0, 0, 1, 2]) for _ in range(H))
            F = scale + rng.choice([0, 0, 1, 2, -1, 3]) * 0.45e-9 * max(1.0, abs(scale)) + rng.choice([0, 0, 0, 5])
            plans.append(dict(id=(u, k), a=a, F=F, phi=rng.randint(-3, 3)))
        units.append(plans)
    bbar = tuple(rng.randint(0, 3 * U) for _ in range(H))
    return units, bbar

def grid(plans):
    cs = [sorted({p["a"][h] for p in plans}) for h in range(2)]
    return list(itertools.product(*cs))

def main(n=6000, seed=8):
    rng = random.Random(seed)
    viol_E, viol_DL, checked, pos = 0, 0, 0, {"opt": 0, "pess": 0}
    anytie_fail = 0
    for _ in range(n):
        units, bbar = rand_inst(rng)
        FB, fbs = first_bests(units, bbar)
        if FB is None:
            continue
        full = leader(units, bbar, [grid(p) for p in units])
        eprime = leader(units, bbar, [sorted({p["a"] for p in pl}) for pl in units])
        if full != eprime:
            viol_E += 1
            print("E' VIOLATION", units, bbar, full, eprime)
        for mode in ("opt", "pess"):
            if full[mode] is None:
                continue
            checked += 1
            dl0 = abs(FB - full[mode]) < 1e-12
            if not dl0:
                pos[mode] += 1
            se = any(self_enf(f, units, mode) for f in fbs)
            if dl0 != se:
                viol_DL += 1
                print("DL-1 VIOLATION", mode, units, bbar, FB, full)
            assert full[mode] <= FB + 1e-12, "P1 violated"
    # adversarial: single unit, any-tie-element shrink (42 l.476 sentence)
    xt = dict(id="top", a=(2, 0), F=10.0, phi=10)
    xh = dict(id="hat", a=(1, 0), F=10.0 - 0.6e-8, phi=10)
    xl = dict(id="low", a=(0, 0), F=10.0 - 1.5e-8, phi=-100)
    T_e = br([xt, xh, xl], (2, 0)); T_h = br([xt, xh, xl], xh["a"])
    if min(p["phi"] for p in T_e) == 10 and min(p["phi"] for p in T_h) == -100:
        anytie_fail = 1
    # 51 affordability slack: e=(1,0) (not in E') vs E'
    p1 = dict(id="x", a=(1 + 0.5e-9, 0), F=10.0, phi=5)
    p2 = dict(id="bad", a=(1 + 1.2e-9, 0), F=20.0, phi=-100)
    slack_full = leader([[p1, p2]], (1 + 2e-9, 0), [[(1, 0), p1["a"], p2["a"]]], slack=TOL)
    slack_ep = leader([[p1, p2]], (1 + 2e-9, 0), [[p1["a"], p2["a"]]], slack=TOL)
    print(f"instances={n} DL-checks={checked} DL>0 opt/pess={pos['opt']}/{pos['pess']} "
          f"E'_violations={viol_E} DL1_violations={viol_DL}")
    print(f"any-tie-element shrink fails (42 l.476 sentence, tolerant rule): {bool(anytie_fail)}")
    print(f"51 slack variant: sup incl. non-E' envelope={slack_full} vs E' only={slack_ep} -> "
          f"{'GAP (slack not covered)' if slack_full != slack_ep else 'no gap'}")

if __name__ == "__main__":
    main()
