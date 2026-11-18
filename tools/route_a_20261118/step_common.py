"""Shared reliability statistics (standard library only)."""
from collections import Counter


def kappa(a, b):
    """Unweighted Cohen's kappa."""
    n = len(a)
    if n == 0:
        return float("nan")
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)


def alpha_nominal(pairs):
    """Krippendorff's alpha, nominal metric, two coders, no missing data.
    alpha = 1 - D_o / D_e using the coincidence matrix (Krippendorff 2004)."""
    values = [v for p in pairs for v in p]
    n = len(values)
    if n < 2:
        return float("nan")
    o = Counter()
    for x, y in pairs:
        o[(x, y)] += 1
        o[(y, x)] += 1
    nc = Counter(values)
    do = sum(v for (x, y), v in o.items() if x != y) / n
    de = sum(nc[c] * nc[k] for c in nc for k in nc if c != k) / (n * (n - 1))
    return float("nan") if de == 0 else 1 - do / de
