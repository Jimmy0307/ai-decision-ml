"""Offline deterministic QA. No public network dependency for PR gate."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("poc",ROOT/"src"/"poc.py")
poc=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(poc)

class FeasibilityTests(unittest.TestCase):
 def test_fixture_no_live_calls(self):
  r=poc.run("fixture")
  self.assertEqual(len(r["source_status"]),9)
  self.assertTrue(all(x["status"]=="NOT_RETRIEVED_FIXTURE_MODE" for x in r["source_status"].values()))
 def test_grid_fixture_nodes(self):
  r=poc.run("fixture")["fixture"]["pypsa"]
  self.assertEqual(r["nodes"],4)
 def test_grid_fixture_edges(self):
  self.assertEqual(poc.run("fixture")["fixture"]["pypsa"]["edges"],4)
 def test_grid_triangle(self):
  self.assertEqual(poc.run("fixture")["fixture"]["pypsa"]["triangles"],1)
 def test_grid_schema_rejects_malformed(self):
  with self.assertRaises(ValueError):
   poc.grid_stats("wrong,columns\n1,2\n","link_id,bus0,bus1\n")
 def test_grid_empty(self):
  z=poc.grid_stats("transformer_id,bus0,bus1\n","link_id,bus0,bus1\n")
  self.assertEqual(z["components"],0)
 def test_ocds_labels_not_empirical(self):
  self.assertIn("FICTIONAL",poc.run("fixture")["fixture"]["ocds"]["scope"])
 def test_ocds_winners(self):
  self.assertEqual(poc.run("fixture")["fixture"]["ocds"]["winners"],1)
 def test_openalex(self):
  z=poc.openalex_stats({"results":[{"authorships":[{"author":{"id":"A1"},"institutions":[{"id":"I1"}]},{"author":{"id":"A2"},"institutions":[]}]}]})
  self.assertEqual((z["works"],z["authors"],z["institutions"]),(1,2,1))
 def test_gleif_not_parent_confirmed(self):
  z=poc.gleif_stats({"data":{"id":"LEI_FAKE","relationships":{"direct-parent":{}}}})
  self.assertEqual(z["returned_relationship_keys"],["direct-parent"])
  self.assertIn("NOT_VERIFIED",z["scope"])
 def test_sec_accounts_not_ai(self):
  z=poc.sec_stats({"cik":123,"tag":"Assets","units":{"USD":[1,2,3]}})
  self.assertEqual(z["financial_observations"],3)
  self.assertIn("NOT_AI",z["scope"])
 def test_mlp_cap_constraints(self):
  z=poc.toy_mlp()
  self.assertLessEqual(sum(z["leader"]["capacity"]),z["budget"])
  for x,c in zip(z["leader"]["best_responses"],z["leader"]["capacity"]):
   self.assertLessEqual(x,c)
 def test_mlp_not_empirical(self):
  self.assertEqual(poc.toy_mlp()["evidence"],"SYNTHETIC_TOY")
 def test_gne_shared_cap(self):
  z=poc.gne_shared_capacity(3)
  self.assertTrue(z["equilibria"])
  self.assertTrue(all(sum(y)<=3 for y in z["equilibria"]))
 def test_deterministic(self):
  self.assertEqual(poc.toy_mlp(),poc.toy_mlp())
 def test_budget_bounds(self):
  with self.assertRaises(ValueError):poc.toy_mlp(100)
 def test_https(self):
  with self.assertRaises(ValueError):poc.bounded_get("http://example.com")
 def test_catalog_provenance(self):
  for key in ("CORDIS","OpenAlex","OCDS_REAL","GLEIF","SEC","PyPSA_Transformers"):
   self.assertTrue(poc.SOURCES[key].startswith("https://"))
if __name__=="__main__":
 unittest.main()
