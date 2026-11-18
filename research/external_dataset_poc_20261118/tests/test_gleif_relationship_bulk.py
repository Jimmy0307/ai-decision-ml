import importlib.util
import io
from pathlib import Path
import unittest
import zipfile

p=Path(__file__).resolve().parents[1]/"src"/"gleif_relationship_bulk.py"
sp=importlib.util.spec_from_file_location("gleif_bulk",p)
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

XML="""<?xml version="1.0"?>
<rr:RelationshipData xmlns:rr="urn:gleif:rr:2.1">
 <rr:RelationshipRecords>
   <rr:RelationshipRecord><rr:Relationship>
     <rr:StartNode><rr:NodeID>A</rr:NodeID></rr:StartNode>
     <rr:EndNode><rr:NodeID>B</rr:NodeID></rr:EndNode>
     <rr:RelationshipType>IS_DIRECTLY_CONSOLIDATED_BY</rr:RelationshipType>
     <rr:RelationshipStatus>ACTIVE</rr:RelationshipStatus>
   </rr:Relationship></rr:RelationshipRecord>
   <rr:RelationshipRecord><rr:Relationship>
     <rr:StartNode><rr:NodeID>C</rr:NodeID></rr:StartNode>
     <rr:EndNode><rr:NodeID>B</rr:NodeID></rr:EndNode>
     <rr:RelationshipType>IS_DIRECTLY_CONSOLIDATED_BY</rr:RelationshipType>
   </rr:Relationship></rr:RelationshipRecord>
   <rr:RelationshipRecord><rr:Relationship>
     <rr:StartNode><rr:NodeID>A</rr:NodeID></rr:StartNode>
     <rr:EndNode><rr:NodeID>D</rr:NodeID></rr:EndNode>
     <rr:RelationshipType>IS_ULTIMATELY_CONSOLIDATED_BY</rr:RelationshipType>
   </rr:Relationship></rr:RelationshipRecord>
 </rr:RelationshipRecords>
</rr:RelationshipData>"""
class GleifBulkTests(unittest.TestCase):
 def test_xml_namespace(self):
  out=m.parse_xml_stream(io.BytesIO(XML.encode()))
  self.assertEqual(out["record_rows"],3)
  self.assertEqual(out["direct_unique_edges"],2)
  self.assertEqual(out["ultimate_unique_edges"],1)
 def test_degree_hubs(self):
  out=m.parse_xml_stream(io.BytesIO(XML.encode()))
  self.assertEqual(out["global_direct_parent_child_degree"]["parent_max_children"],2)
 def test_no_inference_of_social_ties(self):
  out=m.parse_xml_stream(io.BytesIO(XML.encode()))
  self.assertIn("NOT_KNOWLEDGE_BROKERAGE",out["source_scope"])
 def test_zip(self):
  buf=io.BytesIO()
  with zipfile.ZipFile(buf,"w") as z:z.writestr("relationships.xml",XML)
  out=m.parse_zip(buf.getvalue())
  self.assertEqual(out["record_rows"],3)
  self.assertEqual(len(out["zip_members"]),1)
 def test_active_parent_is_separate_from_inactive_records(self):
  x=m.parse_xml_stream(io.BytesIO(XML.encode()))
  g=x["active_multilayer_legal_graph"]
  self.assertEqual(g["direct_active_edges"],1)
  self.assertEqual(g["ultimate_active_edges"],0)
  self.assertEqual(g["role_coded_two_mode"]["affiliation_edges"],1)
  self.assertEqual(x["active_relationship_type_rows"]["IS_DIRECTLY_CONSOLIDATED_BY"],1)
 def test_active_layer_intersection(self):
  x=m.legal_graph_profile({
      "IS_DIRECTLY_CONSOLIDATED_BY":{("A","B"),("C","B")},
      "IS_ULTIMATELY_CONSOLIDATED_BY":{("A","B"),("A","D")}},sample_limit=8)
  self.assertEqual(x["direct_ultimate_active_edge_overlap"],1)
  self.assertEqual(x["direct_ultimate_active_union_edges"],3)
  self.assertEqual(x["role_coded_two_mode"]["consolidating_parent_entities"],1)
 def test_active_legal_network_bounded_sample(self):
  x=m.legal_graph_profile({
      "IS_DIRECTLY_CONSOLIDATED_BY":{("A","B"),("A","C"),("B","C")}},
      sample_limit=3,max_ego_degree=2)
  self.assertEqual(x["bounded_ego_constraint_sample"]["sample_size"],3)
  self.assertAlmostEqual(x["bounded_ego_constraint_sample"]["constraint"]["median"],1.125)
 def test_multiplex_is_legal_not_social(self):
  x=m.legal_graph_profile({"IS_DIRECTLY_CONSOLIDATED_BY":{("A","B")}})
  self.assertIn("not confirmatory",x["bounded_ego_constraint_sample"]["not_a_population_estimate"])
 def test_non_zip_rejected(self):
  with self.assertRaises(zipfile.BadZipFile):m.parse_zip(b"random")
 def test_official_url_pinned(self):
  self.assertTrue(m.OFFICIAL_PINNED_URL.startswith("https://leidata.gleif.org/"))
if __name__=="__main__":unittest.main()
