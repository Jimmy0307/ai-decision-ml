import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import firm_null as fn  # noqa: E402


def toy():
    year = np.full(20, 2015, np.int16)
    year[10:] = 2016
    ai = {k: [("G06N3/08", True)] for k in range(0, 12)}
    dec = {k: [("G06Q10/0635", True)] for k in range(8, 20)}       # 8-11 are bridges
    owners = {0: {"a1"}, 1: {"a1"}, 2: {"a2"}, 3: {"a2", "a3"}, 4: {"a3"}, 8: {"m1"}, 9: {"m1"},
              12: {"d1"}, 13: {"d1"}, 14: {"d2"}, 15: {"d2"}, 16: {"m1"}, 17: {"d3"}}
    ci = np.array([0, 2, 3, 12, 14, 8, 16, 4, 13, 1, 17])
    cj = np.array([2, 3, 4, 14, 15, 0, 12, 9, 16, 12, 0])
    return dict(year=year, ai=ai, dec=dec, owners=owners, ci=ci, cj=cj, cat=np.ones(len(ci), bool),
                names={})


class FirmNull(unittest.TestCase):
    def test_weights_match_manual(self):
        M = fn.FirmModel(toy())
        W = M.weights().toarray()
        f = {n: k for k, n in enumerate(M.firms)}
        # 3 is owned by {a2,a3}: citation 2->3 gives a2-a3 once (a2-a2 self excluded)
        self.assertEqual(W[f["a2"], f["a3"]], 2)                # 2->3 and 3->4 (a2->a3)
        self.assertEqual(W[f["d1"], f["d2"]], 1)
        self.assertEqual(W[f["m1"], f["a1"]], 1)
        self.assertEqual(W[f["a1"], f["d1"]], 1)
        self.assertTrue((W == W.T).all())
        self.assertEqual(M.group[f["m1"]], "MIXED")
        self.assertEqual(M.group[f["a1"]], "AI_FIRM")
        self.assertEqual(M.group[f["d3"]], "DEC_FIRM")

    def test_permutation_preserves_portfolios(self):
        M = fn.FirmModel(toy())
        rng = np.random.default_rng(0)
        for _ in range(20):
            perm = np.arange(len(M.S))
            for g in M.strata["primary"]:
                perm[g] = rng.permutation(g)
            self.assertEqual(M.firm_counts(perm), M.firm_counts(np.arange(len(M.S))))

    def test_null_runs_and_summarises(self):
        M = fn.FirmModel(toy())
        obs = M.stats(M.weights())
        res = fn.summarise(obs, M.null("primary", 30))
        self.assertIn(res["verdict"], {"ORGANISATIONAL_HOLE_BEYOND_PORTFOLIO", "PARTIAL", "PORTFOLIO_ARTEFACT"})
        self.assertTrue(0 < res["T1"]["p_lower"] <= 1)


if __name__ == "__main__":
    unittest.main()
