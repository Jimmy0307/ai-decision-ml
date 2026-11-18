import importlib.util
from pathlib import Path
import unittest

p=Path(__file__).resolve().parents[1]/"src"/"multinetwork_six_sources.py"
spec=importlib.util.spec_from_file_location("multisrc",p)
import sys
sys.path.insert(0,str(p.parent))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def live_sample():
    return {"cordis_bulk_profile":{"exploratory_ai_decision":{
        "derived_affiliations":[{"project_id":"P1","organisation_id":o} for o in ["A","B","C"]]+
        [{"project_id":"P2","organisation_id":o} for o in ["B","C","D"]],
        "alternate_affiliations":[{"project_id":"P1","organisation_id":o} for o in ["A","B","C"]]+
        [{"project_id":"P2","organisation_id":o} for o in ["B","C","D"]],
        "selected_project_metadata":{"P1":{"startDate":"2016-09-01"},
                                    "P2":{"startDate":"2019-09-01"}},
        "derived_allocations":[{"project_id":"P1","organisation_id":"A","role":"coordinator"},
                               {"project_id":"P1","organisation_id":"B","role":"participant"},
                               {"project_id":"P1","organisation_id":"C","role":"participant"},
                               {"project_id":"P2","organisation_id":"B","role":"coordinator"},
                               {"project_id":"P2","organisation_id":"C","role":"participant"},
                               {"project_id":"P2","organisation_id":"D","role":"participant"}]
    }},"source_status":{
       "OpenAlex":{"parsed":{"work_memberships":[
           {"work_id":"W1","authors":["A","B"],"institutions":["I1","I2"],"year":2017},
           {"work_id":"W2","authors":["B","C"],"institutions":["I2","I3"],"year":2021}
       ]}},
       "OCDS_REAL_UK":{"parsed":{"releases_in_package":2,"award_count":2,
                      "verified_scheme_id_buyer_supplier_edges":[["B1","S1"],["B1","S2"]]}}
    },"grid_stats":{"rows":{"transformer":1,"dc_link":1,"ac_line":1},
             "derived_edges":[{"u":"1","v":"2","kind":"transformer"},
                              {"u":"1","v":"2","kind":"ac_line"},
                              {"u":"2","v":"3","kind":"dc_link"}]}}

class MultiNetworkTests(unittest.TestCase):
    def test_two_mode_no_indirect(self):
        z=m.two_mode([{"pid":"P1","org":"O1"},{"pid":"P1","org":"O2"}],"pid","org")
        self.assertEqual(z["strict_bipartite_indirect_term_nonzero"],0)
    def test_two_mode_unique_rows(self):
        rows=[{"pid":"P1","org":"O1"}]*2
        x=m.two_mode(rows,"pid","org")
        self.assertEqual(x["original_rows"],2)
        self.assertEqual(x["unique_affiliation_edges"],1)
    def test_weighted_single_star(self):
        x=m.weighted_constraint({("A","B"):2,("A","C"):1,("A","D"):1})
        self.assertAlmostEqual(x["A"],(.5**2)+(.25**2)+(.25**2))
    def test_weighted_triangle_direct_and_indirect(self):
        x=m.weighted_constraint({("A","B"):1,("A","C"):1,("B","C"):1})
        self.assertAlmostEqual(x["A"],1.125)
    def test_layer_overlap(self):
        x=m.undirected_layers({"a":[("1","2"),("2","3")],"b":[("1","2")]})
        self.assertEqual(x["union"]["edges"],2)
        self.assertEqual(x["shared_edges_across_layers"],1)
        self.assertEqual(x["edge_overlap"]["a__b"]["overlapping_edges"],1)
    def test_layers_not_merged_across_namespaces(self):
        x=m.undirected_layers({"a":[("A","B")],"b":[("X","Y")]})
        self.assertEqual(x["union"]["edges"],2)
    def test_cordis_temporal_and_role(self):
        x=m.cordis(live_sample())
        self.assertEqual(x["two_mode"]["unique_affiliation_edges"],6)
        self.assertEqual(x["one_mode_unweighted"]["edges"],5)
        self.assertIn("2014-2017",x["time_layers"])
        self.assertIn("2018-2020",x["time_layers"])
        self.assertEqual(x["at_least_two_projects_backbone"]["edges"],1)
        self.assertIn("coordinator",x["by_role_two_mode"])
    def test_cordis_weighted_constraint_exists(self):
        x=m.cordis(live_sample())
        self.assertEqual(x["one_mode_shared_project_count_weighted_constraint"]["n"],4)
    def test_openalex_two_mode_author_institution(self):
        x=m.openalex(live_sample())
        self.assertEqual(x["layers"]["authors"]["two_mode"]["left_nodes"],2)
        self.assertEqual(x["layers"]["authors"]["one_mode"]["edges"],2)
        self.assertEqual(x["layers"]["institutions"]["one_mode"]["edges"],2)
    def test_openalex_time_layers(self):
        x=m.openalex(live_sample())["author_time_multilayer"]
        self.assertEqual(len(x["layers"]),2)
    def test_ocds_supplier_projection_not_collaboration(self):
        x=m.ocds(live_sample())
        self.assertEqual(x["two_mode_buyer_supplier"]["unique_affiliation_edges"],2)
        self.assertEqual(x["supplier_one_mode_common_buyer"]["edges"],1)
        self.assertIn("not",x["note"].lower())
    def test_pypsa_incidence_keeps_duplicated_physical_type(self):
        x=m.gridkit(live_sample())
        self.assertEqual(x["bus_asset_incidence_two_mode"]["right_nodes"],3)
        self.assertEqual(x["physical_bus_network"]["union"]["edges"],2)
        self.assertEqual(x["physical_bus_network"]["shared_edges_across_layers"],1)
    def test_gleif_directed_abstention(self):
        self.assertEqual(m.gleif(live_sample())["verdict"],
          "PARENT_RELATIONSHIP_MAY_BE_TOPOLOGICALLY_VALID_NOT_BURT_EVIDENCE")
    def test_sec_abstention(self):
        self.assertEqual(m.sec(live_sample())["verdict"],"ABSTAIN")
    def test_whole_six_sources_and_semantic_gate(self):
        r=m.run(live_sample())
        self.assertEqual(set(["CORDIS","OpenAlex","OCDS","GLEIF","SEC","PyPSA"])-set(r),set())
        self.assertIn("NOT_CONSTRUCTED",r["cross_source_multiplex"])
    def test_projected_edges_not_true_social_ties(self):
        self.assertIn("cliques",m.cordis(live_sample())["note"])
    def test_three_node_line_no_triangle(self):
        x=m.sgraph_stats(m.build_graph([("A","B"),("B","C")]))
        self.assertEqual(x["edges"],2)
        self.assertGreater(x["constraint"]["median"],0.)
if __name__=="__main__":
    unittest.main()
