"""Unit tests for route A (run: python -m unittest test_route_a -v). Synthetic data are used ONLY here."""
import os, random, unittest
import numpy as np
import ra_lib as L
from step_common import alpha_nominal, kappa
import score_reliability as S


class StatsTests(unittest.TestCase):
    def test_alpha_hand_computed(self):
        # values a=3, b=5 (n=8); Do = 2/8; De = (3*5+5*3)/(8*7) -> alpha = 1 - 0.25/(30/56)
        pairs = [("a", "a"), ("a", "b"), ("b", "b"), ("b", "b")]
        self.assertAlmostEqual(alpha_nominal(pairs), 1 - 0.25 / (30 / 56), places=12)

    def test_alpha_perfect(self):
        self.assertEqual(alpha_nominal([("x", "x"), ("y", "y"), ("z", "z")]), 1.0)

    def test_bh_matches_definition(self):
        p = np.array([0.01, 0.04, 0.03, 0.20])
        q = L.bh(p)
        # sorted: .01,.03,.04,.20 -> raw .04,.06,.0533,.20 -> monotone .04,.0533,.0533,.20
        np.testing.assert_allclose(q, [0.04, 0.0533333333, 0.0533333333, 0.20], rtol=1e-8)

    def test_exact_hyper_margins(self):
        m = np.array([[5, 1], [1, 5]])
        exp, p = L.exact_hyper(m)
        np.testing.assert_allclose(exp, [[3, 3], [3, 3]])
        self.assertTrue(np.all(p <= 1) and p[0, 0] == p[1, 1])

    def test_doc_null_preserves_degrees(self):
        rng = random.Random(1)
        ai, de = ["A1", "A2", "A3"], ["D1", "D2", "D3"]
        pairs = L.dedup([(f"doc{rng.randint(0, 9)}", rng.choice(ai), rng.choice(de)) for _ in range(80)])
        _, _, diag = L.doc_null(pairs, ai, de, samples=50, burn=500, thin=50, seed=3)
        self.assertTrue(diag["degrees_preserved"])
        self.assertGreater(diag["accepted"], 0)


class GateTests(unittest.TestCase):
    def sheets(self, p_agree, same_coder=False, seed=0):
        rng = random.Random(seed)
        fams_a, fams_d = L.AI_FAMS + ["NONE"], L.DEC_FAMS + ["NONE"]
        key, A, B = [], [], []
        for i in range(200):
            iid = f"RS-{i:03d}"
            ta, td = rng.choice(fams_a), rng.choice(fams_d)
            key.append({"item_id": iid, "model_ai_family": ta, "model_decision_family": td})
            def code(cid):
                return {"item_id": iid, "C1_evidence_valid": "VALID", "C2_relation_type": "ENABLES",
                        "C3_ai_family": ta if rng.random() < p_agree else rng.choice(fams_a),
                        "C4_decision_family": td if rng.random() < p_agree else rng.choice(fams_d), "coder_id": cid}
            A.append(code("SYN_A")); B.append(code("SYN_A" if same_coder else "SYN_B"))
        return A, B, key

    def test_high_agreement_go_firm(self):
        self.assertEqual(S.score(*self.sheets(0.97))["gate"], "GO_FIRM")

    def test_low_agreement_no_go(self):
        self.assertEqual(S.score(*self.sheets(0.40))["gate"], "NO_GO")

    def test_same_coder_invalid(self):
        self.assertEqual(S.score(*self.sheets(0.97, same_coder=True))["gate"], "INVALID_SAME_CODER")


if __name__ == "__main__":
    unittest.main()
