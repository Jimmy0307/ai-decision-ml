import importlib.util
from pathlib import Path
import random
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("burt",ROOT/"src"/"burt_six_sources.py")
burt=importlib.util.module_from_spec(spec)
spec.loader.exec_module(burt)

def fixture_rows():
    return [{"project_id":p,"organisation_id":org} for p,orgs in
            [("P1",["a","b","c"]),("P2",["b","d"]),("P3",["c","e"]),("P4",["d","e"])]
            for org in orgs]

class BurtSixSourcesTests(unittest.TestCase):
    def test_triangle_constraint_is_oneish(self):
        g=burt.build_graph([("a","b"),("b","c"),("a","c")])
        x=burt.score_graph(g)
        self.assertAlmostEqual(x["a"]["constraint"],1.125)  # direct 1/2, indirect 1/4 per neighbor
    def test_triangle_effective_size(self):
        g=burt.build_graph([("a","b"),("b","c"),("a","c")])
        self.assertAlmostEqual(burt.score_graph(g)["a"]["effective_size"],1.)
    def test_star_center_no_indirect(self):
        g=burt.build_graph([("a","b"),("a","c"),("a","d")])
        x=burt.score_graph(g)["a"]
        self.assertAlmostEqual(x["constraint"],1/3)
        self.assertAlmostEqual(x["indirect_excess"],0)
        self.assertAlmostEqual(x["effective_size"],3)
    def test_edges_dedup_and_loops_ignored(self):
        g=burt.build_graph([("a","b"),("b","a"),("a","a")])
        self.assertEqual(g,{"a":{"b"},"b":{"a"}})
    def test_projection_creates_triangle(self):
        g,counts,meta=burt.project_affiliations(fixture_rows())
        self.assertEqual(counts[("a","b")],1)
        self.assertEqual(meta["edges"],6)
        self.assertEqual(len(g),5)
    def test_projection_backbone(self):
        rows=fixture_rows()+[{"project_id":"P5","organisation_id":"b"},
                             {"project_id":"P5","organisation_id":"c"}]
        _,count,meta=burt.project_affiliations(rows,min_shared=2)
        self.assertEqual(meta["edges"],1)
        self.assertEqual(count[("b","c")],2)
    def test_projection_cap(self):
        g,_,meta=burt.project_affiliations(fixture_rows(),max_project_size=2)
        self.assertEqual(meta["excluded_oversize_projects"],1)
        self.assertNotIn("a",g)
    def test_bh_monotone(self):
        self.assertEqual([round(v,2) for v in burt.fdr_bh([.01,.02,.5])],[.03,.03,.5])
    def test_bh_empty(self):
        self.assertEqual(burt.fdr_bh([]),[])
    def test_betweenness_chain(self):
        g=burt.build_graph([("a","b"),("b","c")])
        x=burt.betweenness_landmarks(g,n_sources=3)
        self.assertGreater(x["scores"]["b"],x["scores"].get("a",0))
    def test_removal_chain_disconnects(self):
        g=burt.build_graph([("a","b"),("b","c")])
        self.assertEqual(burt.retained_alter_reachability(g,"b")["reachable_fraction"],0.)
    def test_removal_triangle_remains_reachable(self):
        g=burt.build_graph([("a","b"),("b","c"),("a","c")])
        self.assertEqual(burt.retained_alter_reachability(g,"b")["reachable_fraction"],1.)
    def test_swap_degree_marginals_preserved(self):
        rows=fixture_rows()
        actual,n=burt.shuffled_affiliation(rows,random.Random(123),swaps=250)
        self.assertGreater(n,0)
        from collections import Counter
        self.assertEqual(Counter(r["project_id"] for r in rows),
                         Counter(r["project_id"] for r in actual))
        self.assertEqual(Counter(r["organisation_id"] for r in rows),
                         Counter(r["organisation_id"] for r in actual))
        self.assertEqual(len({(r["project_id"],r["organisation_id"]) for r in actual}),len(actual))
    def test_swap_deterministic(self):
        a,_=burt.shuffled_affiliation(fixture_rows(),random.Random(42),100)
        b,_=burt.shuffled_affiliation(fixture_rows(),random.Random(42),100)
        self.assertEqual(a,b)
    def test_two_mode_indirect_is_degenerate(self):
        rows=fixture_rows()
        g=burt.build_graph([(r["project_id"],"ORG_"+r["organisation_id"]) for r in rows])
        scores=burt.score_graph(g)
        self.assertTrue(all(abs(x["indirect_excess"])<1e-10 for x in scores.values()))
    def test_null_repetitions_have_no_confirmatory_language(self):
        rows=fixture_rows()
        g,_,_=burt.project_affiliations(rows)
        scores=burt.score_graph(g)
        x=burt.null_degree_preserving(rows,["b"],scores,reps=2)
        self.assertEqual(x["reps"],2)
        self.assertIsNone(x["tested"][0]["bh_q"])
    def test_cordis_fixture_not_confirmatory(self):
        data={"cordis_bulk_profile":{"exploratory_ai_decision":{
            "derived_affiliations":fixture_rows(),
            "alternate_affiliations":fixture_rows(),
            "selected_project_metadata":{"P1":{"startDate":"2016-01-01"},
                "P2":{"startDate":"2018-01-01"},"P3":{"startDate":"2019-01-01"},"P4":{"startDate":"2020-01-01"}}}}}
        r=burt.cordis_round(data,reps=0)
        self.assertEqual(r["two_mode"]["project_org_edges"],9)
        self.assertIn("NO_CONFIRMED",r["verdict"])
        self.assertEqual(r["degree_preserving_null"]["reps"],0)
    def test_openalex_fixture(self):
        inp={"source_status":{"OpenAlex":{"parsed":{"work_memberships":[
            {"work_id":"W1","authors":["A","B"],"institutions":["I1","I2"]},
            {"work_id":"W2","authors":["B","C"],"institutions":["I2","I3"]}]}}}}
        r=burt.other_sources_round(inp)["OpenAlex"]
        self.assertEqual(r["author_graph"]["edges"],2)
        self.assertEqual(r["institution_graph"]["edges"],2)
    def test_sec_is_not_applicable(self):
        self.assertIn("NOT_APPLICABLE",burt.other_sources_round({})["SEC"]["verdict"])
    def test_uk_no_tenderers_abstains(self):
        inp={"source_status":{"OCDS_REAL_UK":{"parsed":{"releases_in_package":1,
            "real_buyer_supplier_edges":[]}}}}
        r=burt.other_sources_round(inp)["OCDS"]
        self.assertEqual(r["buyer_supplier_edges"],0)
        self.assertEqual(r["verdict"],"OBSERVED_AWARDS_NOT_INDEPENDENT_BROKERAGE")
    def test_real_awards_stable_ids_only(self):
        inp={"source_status":{"OCDS_REAL_UK":{"parsed":{
             "releases_in_package":5,"award_count":3,"notices_with_global_buyer_id":5,
             "verified_scheme_id_buyer_supplier_edges":[["GB:BUYER","GB:SUP1"],
                  ["GB:BUYER","GB:SUP2"],["GB:OTHER","GB:SUP2"]]}}}}
        r=burt.other_sources_round(inp)["OCDS"]
        self.assertEqual(r["buyer_supplier_edges"],3)
        self.assertEqual(r["buyer_supplier_two_mode"]["edges"],3)
        self.assertEqual(r["supplier_projection"]["edges"],1)
        self.assertEqual(r["buyer_supplier_two_mode"]["n_with_indirect_excess"],0)
    def test_grid_without_edges_is_not_falsely_analyzed(self):
        r=burt.other_sources_round({"grid_stats":{"nodes":3,"edges":2}})["PyPSA_Eur"]
        self.assertIsNone(r["network"])
    def test_coauthor_is_two_mode_projection(self):
        r=burt.paper_memberships([{"work_id":"W1","authors":["A","B"]}],"authors")
        self.assertEqual(len(r),2)

if __name__=="__main__":unittest.main()
