import sys
import unittest
from pathlib import Path

import networkx as nx
import numpy as np
import scipy.sparse as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import full_suite as fs  # noqa: E402


class Constraint(unittest.TestCase):
    def test_matches_networkx(self):
        G = nx.gnm_random_graph(60, 240, seed=2)
        rng = np.random.default_rng(2)
        for u, v in G.edges:
            G[u][v]["weight"] = float(rng.integers(1, 6))
        W = nx.to_scipy_sparse_array(G, weight="weight", format="csr")
        c, _ = fs.constraint_sparse(sp.csr_matrix(W), block=7)
        ref = nx.constraint(G, weight="weight")
        for k in G:
            if G.degree(k):
                self.assertAlmostEqual(c[k], ref[k], places=9)


class M06P(unittest.TestCase):
    def docs(self, n=400, seed=1):
        rng = np.random.default_rng(seed)
        out = []
        for d in range(n):
            R = frozenset(rng.choice(fs.ROWS[:4], rng.integers(1, 3), replace=False))
            C = frozenset(rng.choice(fs.COLS[:5], rng.integers(1, 3), replace=False))
            out.append((f"D{d}", R, C, [(r, c) for r in R for c in C]))
        return out

    def test_margins_kept_and_pvalues_valid(self):
        mean, p, diag = fs.m06p(self.docs(), samples=200)
        self.assertTrue(((p > 0) & (p <= 1)).all())
        self.assertEqual(diag["documents"], 400)
        self.assertGreater(diag["exchangeable_documents"], 300)

    def test_planted_block_depletion_detected(self):
        rng = np.random.default_rng(9)
        docs = [d for d in self.docs(n=3000, seed=4)
                if not ("G06N3" in d[1] and "RISK" in d[2] and rng.random() < 0.6)]
        rows, summ = fs.analyse(docs, R=5000, samples=2000)
        cell = next(r for r in rows if r["ai_family"] == "G06N3" and r["decision_family"] == "RISK")
        self.assertEqual(cell["m06p_dir"], "DEPLETED")
        self.assertTrue(cell["m06p_q05"] and cell["exact_q05"])


if __name__ == "__main__":
    unittest.main()
