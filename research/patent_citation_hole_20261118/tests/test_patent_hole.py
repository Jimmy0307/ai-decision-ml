import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import patent_hole as ph  # noqa: E402

REF = [f"G06F{k}" for k in range(1, 9)] + [f"H04L{k}" for k in range(1, 9)] + ["G06Q30", "G06Q40"]


def synth(n=6000, hole=1.0, seed=1, years=(2008, 2016)):
    """Synthetic universe: field-local citation with an optional AI–DEC suppression factor."""
    rng = np.random.default_rng(seed)
    pid = np.arange(1, n + 1, dtype=np.int64) + 9_000_000
    year = rng.integers(years[0], years[1] + 1, n).astype(np.int16)
    # primary field per patent: AI, DEC, or one of REF
    fields = ["AI", "DEC"] + REF
    prob = np.r_[0.08, 0.08, np.full(len(REF), 0.84 / len(REF))]
    f = rng.choice(len(fields), n, p=prob)
    rows = []
    for k in range(n):
        name = fields[f[k]]
        code = {"AI": "G06N3/08", "DEC": "G06Q10/0631"}.get(name, name + "/00")
        rows.append((str(pid[k]), code, "inventive"))
        if rng.random() < 0.05:   # some secondary codes
            other = fields[rng.integers(2, len(fields))]
            rows.append((str(pid[k]), other + "/02", "additional"))
    cpc = pd.DataFrame(rows, columns=["patent_id", "cpc_group", "cpc_type"])
    u = ph.Universe(pid=pid, year=year)
    ph.build_memberships(u, cpc)
    # citations: each patent cites 8 earlier-or-same-year patents, 60% same field, rest random
    ci, cj, cat = [], [], []
    by_field = {g: np.flatnonzero(f == g) for g in range(len(fields))}
    for k in range(n):
        for _ in range(8):
            if rng.random() < 0.6:
                j = rng.choice(by_field[f[k]])
            else:
                j = rng.integers(0, n)
            pair = {fields[f[k]], fields[f[j]]}
            if pair == {"AI", "DEC"} and rng.random() > hole:
                continue
            ci.append(k); cj.append(j); cat.append(rng.random() < 0.7)
    return u, np.array(ci, np.int32), np.array(cj, np.int32), np.array(cat)


class Basics(unittest.TestCase):
    def test_dec_definition(self):
        yes = ["G06Q10/04", "G06Q10/047", "G06Q10/06", "G06Q10/0631", "G06Q10/06375"]
        no = ["G06Q10/08", "G06Q10/10", "G06Q10/20", "G06Q30/02", "G06Q10/30"]
        self.assertTrue(all(ph.DEC_RE.match(x) for x in yes))
        self.assertFalse(any(ph.DEC_RE.match(x) for x in no))

    def test_inventional_label_and_chunks(self):
        u = ph.Universe(pid=np.array([1, 2, 3], np.int64), year=np.array([2012, 2012, 2013], np.int16))
        cpc = pd.DataFrame({"patent_id": ['"1"', '"2"', '"3"', '"3"'],
                            "cpc_group": ['"G06N3/08"', '"G06Q10/0631"', '"G06F16/24"', '"G06N20/00"'],
                            "cpc_type": ['"inventional"', '"additional"', '"inventional"', '"additional"']})
        ph.build_memberships(u, [cpc.iloc[:2], cpc.iloc[2:]])
        self.assertEqual(u.flags["AI"].tolist(), [True, False, True])
        self.assertEqual(u.flags["AI_inv"].tolist(), [True, False, False])
        self.assertEqual(u.flags["DEC"].tolist(), [False, True, False])
        self.assertEqual(u.flags["DEC_inv"].tolist(), [False, False, False])
        self.assertEqual(u.group_names, ["G06F16", "G06N20", "G06N3", "G06Q10"])

    def test_index_and_explode(self):
        u = ph.Universe(pid=np.array([5, 7, 9], np.int64), year=np.array([2010, 2011, 2012], np.int16))
        self.assertEqual(u.index(np.array([7, 8, 9, np.nan])).tolist(), [1, -1, 2, -1])
        csr = (np.array([0, 2, 2, 3]), np.array([0, 3, 1], np.int32))
        p, g = ph.explode(np.array([2, 0, 1]), csr)
        self.assertEqual(list(zip(p.tolist(), g.tolist())), [(0, 1), (1, 0), (1, 3)])

    def test_expectation_matches_brute_force(self):
        u, ci, cj, _ = synth(n=800, seed=3)
        c = ph.strata(u, ci, cj, 2008)
        M = np.bincount(c.s, minlength=c.n_strata)
        A, B = u.flags["AI"] & ~u.flags["DEC"], u.flags["DEC"] & ~u.flags["AI"]
        r = ph.oe_pair(c, A, B, M)
        e = 0.0
        for s in np.unique(c.s):
            m = c.s == s
            e += A[c.i[m]].sum() * B[c.j[m]].sum() / m.sum() + B[c.i[m]].sum() * A[c.j[m]].sum() / m.sum()
        self.assertAlmostEqual(r["E_ab"] + r["E_ba"], e, places=6)
        self.assertEqual(r["O_ab"], int(np.sum(A[ci] & B[cj])))

    def test_reference_vectorisation_matches_pairwise(self):
        u, ci, cj, _ = synth(n=1500, seed=4)
        c = ph.strata(u, ci, cj, 2008)
        M = np.bincount(c.s, minlength=c.n_strata)
        G = len(u.group_names)
        O, E, oe = ph.oe_vs_reference(c, u.flags["AI"], u.ref_csr["all"], G, M)
        indptr, groups = u.ref_csr["all"]
        for name in ["G06F3", "H04L5", "G06Q30"]:
            g = u.group_names.index(name)
            X = np.zeros(len(u.pid), bool)
            owner = np.repeat(np.arange(len(u.pid)), np.diff(indptr))
            X[owner[groups == g]] = True
            AI = u.flags["AI"]
            r = ph.oe_pair(c, AI & ~X, X & ~AI, M)
            self.assertEqual(int(O[g]), r["O_ab"] + r["O_ba"], name)
            self.assertAlmostEqual(float(E[g]), r["E_ab"] + r["E_ba"], places=6)


class Decisions(unittest.TestCase):
    def setUp(self):
        self._min = ph.REF_MIN_PATENTS
        ph.REF_MIN_PATENTS = 50

    def tearDown(self):
        ph.REF_MIN_PATENTS = self._min

    def spec(self):
        return dict(ph.SPECS["primary"], y0=2010)

    def test_planted_hole_detected(self):
        u, ci, cj, cat = synth(hole=0.15, seed=5)
        r, _, _ = ph.run_spec(u, ci, cj, cat, self.spec(), n_boot=200)
        self.assertLess(r["AI_DEC"]["OE"], r["reference"]["q25_AI"])
        self.assertTrue(r["H1a"])
        self.assertTrue(r["H1b"])
        self.assertEqual(r["verdict"], "HOLE_SUPPORTED")

    def test_no_hole_not_flagged(self):
        u, ci, cj, cat = synth(hole=1.0, seed=6)
        r, _, _ = ph.run_spec(u, ci, cj, cat, self.spec(), n_boot=200)
        self.assertNotEqual(r["verdict"], "HOLE_SUPPORTED")
        # field-local citing makes every cross-field OE < 1; without a hole AI–DEC
        # should sit near the comparison fields, which is why H1 is relative.
        self.assertLess(r["AI_DEC"]["OE"], 1.0)
        self.assertLess(abs(r["AI_DEC"]["OE"] / r["reference"]["median_AI"] - 1), 0.25)

    def test_bootstrap_reproducible_and_h2_present(self):
        u, ci, cj, cat = synth(hole=0.5, seed=7)
        r1, _, _ = ph.run_spec(u, ci, cj, cat, self.spec(), n_boot=100)
        r2, _, _ = ph.run_spec(u, ci, cj, cat, self.spec(), n_boot=100)
        self.assertEqual(r1["ratio_CI95"], r2["ratio_CI95"])
        self.assertIn(r1["H2"]["verdict"], {"CLOSING", "PERSISTENT", "NARROWING_BUT_OPEN"})
        self.assertEqual(len(r1["H2"]["by_year"]), 7)


class EndToEnd(unittest.TestCase):
    def test_main_on_patentsview_shaped_zips(self):
        u, ci, cj, cat = synth(n=1200, seed=8, years=(2006, 2016))
        d = Path(tempfile.mkdtemp())
        pat = pd.DataFrame({"patent_id": u.pid.astype(str), "patent_type": "utility",
                            "patent_date": [f"{y}-03-01" for y in u.year], "patent_title": 'A "quoted" title',
                            "withdrawn": "0"})
        pat.loc[len(pat)] = ["D900001", "design", "2015-01-01", "x", "0"]
        indptr, groups = u.ref_csr["all"]
        rows = []
        for k, p in enumerate(u.pid):
            if u.flags["AI"][k]:
                rows.append((p, "G06N3/08", "inventive"))
            if u.flags["DEC"][k]:
                rows.append((p, "G06Q10/0631", "inventive"))
            for g in groups[indptr[k]:indptr[k + 1]]:
                rows.append((p, u.group_names[g] + "/00", "additional"))
        cpc = pd.DataFrame(rows, columns=["patent_id", "cpc_group", "cpc_type"]).astype(str)
        cit = pd.DataFrame({"patent_id": u.pid[ci].astype(str), "citation_sequence": "1",
                            "citation_patent_id": u.pid[cj].astype(str),
                            "citation_category": np.where(cat, "cited by applicant", "cited by examiner")})
        for name, df in (("g_patent", pat), ("g_cpc_current", cpc), ("g_us_patent_citation", cit)):
            buf = io.StringIO()
            df.to_csv(buf, sep="\t", index=False)
            with zipfile.ZipFile(d / f"{name}.tsv.zip", "w", zipfile.ZIP_DEFLATED) as z:
                z.writestr(f"{name}.tsv", buf.getvalue())
        old = ph.REF_MIN_PATENTS
        ph.REF_MIN_PATENTS = 20
        try:
            ph.main(["--inputs", str(d), "--out", str(d / "out"), "--chunksize", "3000", "--n-boot", "50"])
        finally:
            ph.REF_MIN_PATENTS = old
        res = json.loads((d / "out" / "PATENT_HOLE_RESULTS.json").read_text(encoding="utf-8"))
        self.assertEqual(set(res["specs"]), set(ph.SPECS))
        self.assertIn(res["primary_verdict"], {"HOLE_SUPPORTED", "PARTIAL_NOT_CLAIMED", "HOLE_NOT_SUPPORTED"})
        self.assertEqual(len(res["provenance"]["g_patent"]["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
