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
 def test_non_zip_rejected(self):
  with self.assertRaises(zipfile.BadZipFile):m.parse_zip(b"random")
 def test_official_url_pinned(self):
  self.assertTrue(m.OFFICIAL_PINNED_URL.startswith("https://leidata.gleif.org/"))
if __name__=="__main__":unittest.main()
