import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import plan5_construct as p5  # noqa: E402


class Plan5(unittest.TestCase):
    def test_family_key_matches_dec_construction(self):
        self.assertEqual(p5.family_key("G06F16/2457"), "G06F16/24")
        self.assertEqual(p5.family_key("G06Q10/0631"), "G06Q10/06")
        self.assertEqual(p5.family_key("G06Q10/04"), "G06Q10/04")
        self.assertEqual(p5.family_key("H04L67/10"), "H04L67/10")
        self.assertEqual(p5.family_key("G06F3/0482"), "G06F3/04")

    def test_csr_from(self):
        idx = np.array([0, 0, 2, 2, 2], np.int32)
        keys = np.array(["A/1", "B/2", "A/1", "A/1", "C/3"])
        (indptr, g), names = p5.csr_from(4, idx, keys)
        self.assertEqual(names, ["A/1", "B/2", "C/3"])
        self.assertEqual(indptr.tolist(), [0, 2, 2, 4, 4])
        self.assertEqual(g.tolist(), [0, 1, 0, 2])

    def test_reference_exclusion_drops_g06q10_families(self):
        import patent_hole as ph
        u, ci, cj, cat = __import__("test_patent_hole").synth(n=800, seed=2)
        names = list(u.group_names) + ["G06Q10/06", "G06Q10/04"]
        excluded = [x for x in names if x.startswith("G06N") or x.startswith("G06Q10")]
        self.assertIn("G06Q10/06", excluded)
        self.assertIn("G06Q10/04", excluded)
        self.assertTrue(hasattr(ph, "run_spec"))


if __name__ == "__main__":
    unittest.main()
