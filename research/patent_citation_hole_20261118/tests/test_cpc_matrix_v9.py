import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import cpc_matrix_v9 as cm  # noqa: E402
import ra_lib  # noqa: E402


class CellRules(unittest.TestCase):
    def test_rows(self):
        self.assertEqual(cm.assign_row("G06N3/08"), "G06N3")
        self.assertEqual(cm.assign_row("G06N20/00"), "G06N20")
        self.assertEqual(cm.assign_row("G06N10/40"), "G06N10")
        self.assertEqual(cm.assign_row("G06N99/00"), "G06N_OTHER")
        self.assertIsNone(cm.assign_row("G06Q10/04"))

    def test_columns_first_match(self):
        cases = {"G06Q10/04": "FORECAST_OPTIMISE", "G06Q10/047": "FORECAST_OPTIMISE",
                 "G06Q10/06311": "RESOURCE_SCHEDULING", "G06Q10/0633": "WORKFLOW",
                 "G06Q10/0635": "RISK", "G06Q10/0637": "STRATEGY", "G06Q10/06398": "PERFORMANCE",
                 "G06Q10/06": "MGMT_GENERAL", "G06Q10/063": "MGMT_GENERAL", "G06Q10/067": "MGMT_GENERAL",
                 "G06Q10/08": None, "G06Q30/02": None}
        for sym, want in cases.items():
            self.assertEqual(cm.assign_col(sym), want, sym)

    def test_pairs_dedup_and_raw(self):
        e, r = cm.pairs_for("P1", ["G06N3/08", "G06N3/04", "G06N20/00"], ["G06Q10/0631", "G06Q10/06315"])
        self.assertEqual(sorted(e), [("P1", "G06N20", "RESOURCE_SCHEDULING"), ("P1", "G06N3", "RESOURCE_SCHEDULING")])
        self.assertEqual(len(r), 6)

    def test_part_b_excludes_bridge_and_orients(self):
        ai = {1: ["G06N3/08"], 3: ["G06N20/00"]}
        dec = {2: ["G06Q10/0635"], 3: ["G06Q10/04"]}       # 3 is a bridge patent
        ci, cj = np.array([1, 2, 3, 1]), np.array([2, 1, 2, 3])
        E, _ = cm.build_part_b(ai, dec, ci, cj)
        self.assertEqual(E, [("C0", "G06N3", "RISK"), ("C1", "G06N3", "RISK")])


class EngineOnPlantedMatrix(unittest.TestCase):
    def test_planted_depletion_is_core(self):
        rng = np.random.default_rng(3)
        edges = []
        for d in range(1500):
            r = cm.ROWS[rng.integers(0, 3)]
            c = cm.COLS[rng.integers(0, 3)]
            if (r, c) == ("G06N3", "RISK") or ((r, c) == ("G06N3", "FORECAST_OPTIMISE") and rng.random() < 0.85):
                continue
            edges.append((f"D{d}", r, c))
            if rng.random() < 0.5:                       # second edge so documents are exchangeable
                r2, c2 = cm.ROWS[rng.integers(0, 3)], cm.COLS[rng.integers(0, 3)]
                if (r2, c2) not in {("G06N3", "FORECAST_OPTIMISE"), ("G06N3", "RISK")} and (f"D{d}", r2, c2) not in edges:
                    edges.append((f"D{d}", r2, c2))
        rows, summary = ra_lib.analyze(edges, edges, cm.ROWS, cm.COLS, R=500, doc_samples=300)
        cell = next(x for x in rows if x["ai_family"] == "G06N3" and x["decision_family"] == "FORECAST_OPTIMISE")
        self.assertEqual(cell["main_dir"], "DEPLETED")
        self.assertTrue(cell["main_q05"] and cell["exact_q05"])


if __name__ == "__main__":
    unittest.main()
