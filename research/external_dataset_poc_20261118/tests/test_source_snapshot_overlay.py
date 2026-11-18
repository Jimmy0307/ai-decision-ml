import importlib.util
from pathlib import Path
import unittest
p=Path(__file__).resolve().parents[1]/"src"/"source_snapshot_overlay.py"
spec=importlib.util.spec_from_file_location("cached",p)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
snap={"source_run":"https://github.com/example/actions/runs/123","raw_response_sha256":"ABC",
      "raw_query":"https://api.openalex.org/works?per-page=8",
      "work_memberships":[{"work_id":str(i),"doi":str(i),"year":2021,
                            "authors":["A"+str(i)],"institutions":["I"+str(i)]} for i in range(8)]}
class SnapshotTests(unittest.TestCase):
    def test_cached_when_live_rate_limited(self):
        got=mod.overlay({"source_status":{"OpenAlex":{"status":"FETCH_FAILED","error":"HTTPError","message":"429"}}},snap)
        x=got["source_status"]["OpenAlex"]
        self.assertEqual(x["status"],"CACHED_HISTORICAL_WORK_SAMPLE")
        self.assertEqual(x["original_fetch_status"]["status"],"FETCH_FAILED")
        self.assertEqual(x["parsed"]["works"],8)
    def test_never_overwrite_live_work_response(self):
        o={"source_status":{"OpenAlex":{"status":"FETCHED","parsed":{"work_memberships":[{"work_id":"live"}]}}}}
        got=mod.overlay(o,snap)
        self.assertEqual(got["source_status"]["OpenAlex"]["parsed"]["work_memberships"][0]["work_id"],"live")
        self.assertEqual(got["source_status"]["OpenAlex"]["status"],"FETCHED")
    def test_wrong_pinned_size_fails(self):
        s=dict(snap);s["work_memberships"]=s["work_memberships"][:7]
        with self.assertRaises(ValueError):mod.overlay({"source_status":{}},s)
    def test_history_not_upgraded_to_new_fetch(self):
        x=mod.overlay({"source_status":{}},snap)["source_status"]["OpenAlex"]
        self.assertNotEqual(x["status"],"FETCHED")
        self.assertIn("PRIOR",x["analysis_provenance"])
if __name__=="__main__":unittest.main()
