"""Unit tests for the 2026-11-18 review tools (standard library unittest).

    python -I -m unittest discover -s tools/review_20261117 -p "test_*.py"
"""
import json
import math
import os
import sys
import tempfile
import unittest
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import audit_recompute as ar  # noqa: E402
import qa_site as qa  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))


class KappaTests(unittest.TestCase):
    def test_hand_computed_example(self):
        # 2x2: a=[Y,Y,Y,N,N,N,Y,N,Y,Y], b=[Y,Y,N,N,N,Y,Y,N,Y,N]
        a = list("YYYNNNYNYY")
        b = list("YYNNNYYNYN")
        po = Fraction(7, 10)
        pe = Fraction(6 * 5 + 4 * 5, 100)
        expected = float((po - pe) / (1 - pe))
        self.assertAlmostEqual(ar.cohen_kappa(a, b), expected, places=12)

    def test_perfect_and_degenerate(self):
        self.assertEqual(ar.cohen_kappa(list("ABAB"), list("ABAB")), 1.0)
        self.assertTrue(math.isnan(ar.cohen_kappa(list("AAAA"), list("AAAA"))))
        with self.assertRaises(ValueError):
            ar.cohen_kappa([], [])


class CoreRuleTests(unittest.TestCase):
    def row(self, q=(0.01, 0.02, 0.03), d=("DEPLETED",) * 3):
        r = {}
        for m, qq, dd in zip(("main", "exact", "document"), q, d):
            r[f"official_{m}_q"] = str(qq)
            r[f"official_{m}_direction"] = dd
        return r

    def test_all_significant_same_direction(self):
        self.assertTrue(ar.structural_core_member(self.row(), "official"))

    def test_one_not_significant(self):
        self.assertFalse(ar.structural_core_member(self.row(q=(0.01, 0.2, 0.03)), "official"))

    def test_direction_disagreement(self):
        self.assertFalse(ar.structural_core_member(self.row(d=("DEPLETED", "ENRICHED", "DEPLETED")), "official"))

    def test_boundary_q_equal_005_counts(self):
        self.assertTrue(ar.structural_core_member(self.row(q=(0.05, 0.05, 0.05)), "official"))


class QaDetectorTests(unittest.TestCase):
    def parse_text(self, text):
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(text)
        try:
            return qa.parse(f.name)
        finally:
            os.unlink(f.name)

    def test_duplicate_ids_and_unwrapped_table(self):
        p = self.parse_text('<html lang="x"><body><section id="a"><table id="a"><tbody><tr><td>1</td></tr></tbody></table></section></body></html>')
        self.assertEqual([i for i in p.ids if p.ids.count(i) > 1], ["a", "a"])
        self.assertEqual(p.tables_unwrapped, ["a"])
        self.assertEqual(p.tables["a"], 1)

    def test_unclosed_div(self):
        p = self.parse_text("<html><body><div><span>x</span></body></html>")
        self.assertTrue(any("div" in e for e in p.errors))

    def test_overclaim_negation_window(self):
        self.assertTrue(qa.overclaims("結論：16 個 Burt holes 已確認"))
        self.assertFalse(qa.overclaims("不可說：16 depleted 就是 16 個 Burt holes"))
        self.assertTrue(qa.overclaims("Pages 已部署成功"))
        self.assertFalse(qa.overclaims("本紀錄沒有宣稱 Pages 已部署成功"))


    def test_secret_and_path_guards(self):
        import re
        bs = chr(92)
        hits = lambda s: {k for k, v in qa.SECRET_PATTERNS.items() if re.search(v, s)}
        self.assertEqual(hits("C:" + bs + "Users" + bs + "someone" + bs + "x"), {"local-user-path"})
        self.assertEqual(hits("D:/Users/someone/x"), {"local-user-path"})
        self.assertEqual(hits("name@jpcco.com"), {"work-email"})
        self.assertEqual(hits("USER_REPORTED evidence"), set())


class PublishedArtifactTests(unittest.TestCase):
    """Consistency of committed outputs (no private archives required)."""

    def test_recompute_identities(self):
        p = os.path.join(REPO, "docs/review/20261117/RECOMPUTE_RESULTS.json")
        with open(p, encoding="utf-8") as fh:
            r = json.load(fh)
        f, c = r["funnel_machine_output"], r["cells_120"]
        self.assertTrue(f["identity_strict_eq_mapped_partial_unresolved"])
        self.assertEqual(f["mapped_endpoints_2x_full_plus_partial"], 8751)
        self.assertEqual(c["official_observed_nonzero_cells"] + c["official_zero_cells"], 120)
        self.assertEqual(c["official_core_by_direction"], {"ENRICHED": 16, "DEPLETED": 16})
        self.assertEqual(c["sidecar_core_by_direction"], {"ENRICHED": 15, "DEPLETED": 17})
        self.assertEqual(c["zero_cells_inside_core"], 0)
        self.assertTrue(c["rule_matches_published_flags"])
        self.assertEqual(r["human_reliability"]["dimensions"]["C3"]["cohen_kappa"], 0.0476)
        self.assertEqual(r["human_reliability"]["dimensions"]["C4"]["cohen_kappa"], 0.1398)

    def test_metric_audit_has_no_mismatch(self):
        import csv
        p = os.path.join(REPO, "docs/review/20261117/METRIC_AUDIT_90.csv")
        with open(p, encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.DictReader(fh))
        self.assertEqual(len(rows), 90)
        self.assertFalse([r["metric_id"] for r in rows if r["result"] == "MISMATCH"])
        grades = {g: sum(r["evidence_grade"] == g for r in rows) for g in ("DIRECT", "HISTORICAL", "USER_REPORTED", "SYNTHETIC")}
        self.assertEqual(grades, {"DIRECT": 55, "HISTORICAL": 16, "USER_REPORTED": 17, "SYNTHETIC": 2})


if __name__ == "__main__":
    unittest.main()
