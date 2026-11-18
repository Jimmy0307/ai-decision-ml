import importlib.util
import math
from pathlib import Path
import unittest

HERE=Path(__file__).resolve().parents[1]/"src"/"full_round.py"
sp=importlib.util.spec_from_file_location("round2",HERE)
mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod)

def dummy():
    return {
      "timestamp":"fixture","mode":"live",
      "source_status":{"CORDIS":{"status":"FETCHED"},"OpenAlex":{"status":"FETCHED"},
                       "OCDS_REAL_UK":{"status":"FETCHED_PARSED","parsed":{"tenderer_count_observed":0}}},
      "cordis_bulk_profile":{
        "status":"BOUNDED_BULK_READ_SUCCESS","project_rows":2,
        "organisation_rows":3,"organisation_rows_with_matched_project_id":3,
        "unique_participant_organisation_ids":2,"full_organisation_funding_missing":{"totalCost":0},
        "exploratory_ai_decision":{
          "selected_project_metadata":{"P1":{"ecMaxContribution":"75","totalCost":"100","startDate":"2019-01-01"}},
          "derived_affiliations":[{"project_id":"P1","organisation_id":"O1"},
                                 {"project_id":"P1","organisation_id":"O2"}],
          "derived_allocations":[
            {"project_id":"P1","organisation_id":"O1","role":"coordinator",
              "ecContribution":40,"netEcContribution":40,"totalCost":60},
            {"project_id":"P1","organisation_id":"O2","role":"participant",
              "ecContribution":35,"netEcContribution":35,"totalCost":40}]}}}

class FullRoundTests(unittest.TestCase):
    def test_decimal_comma(self):self.assertEqual(mod.money("4.639.086,25"),4639086.25)
    def test_zero_is_observed(self):self.assertEqual(mod.money("0"),0.)
    def test_nonfinite_excluded(self):self.assertIsNone(mod.money("NaN"))
    def test_money_bad(self):self.assertIsNone(mod.money("unknown"))
    def test_reconcile_cost_and_ec(self):
        c=mod.profile_cordis(dummy()["cordis_bulk_profile"])["reconciliation"]
        self.assertEqual(c["ec_comparable_projects"],1)
        self.assertEqual(c["ec_gap_le_1percent"],1)
        self.assertEqual(c["cost_gap_le_1percent"],1)
        self.assertEqual(c["ec_gap_gt_5percent"],0)
    def test_projected_graph_no_broker_claim(self):
        c=mod.profile_cordis(dummy()["cordis_bulk_profile"])["projected_graph"]
        self.assertEqual(c["one_mode_edges"],1)
        self.assertEqual(c["single_project_orgs"],2)
        self.assertTrue("clique" in c["warning"])
        self.assertEqual(c["top_ten_low_constraint"][0]["constraint"],1)
    def test_coordinator(self):
        c=mod.profile_cordis(dummy()["cordis_bulk_profile"])
        self.assertEqual(c["selected_keyword"]["coordinator_role_counts"]["coordinator"],1)
    def test_leader_not_automatically_valid(self):
        c=mod.profile_cordis(dummy()["cordis_bulk_profile"])["readiness"]
        self.assertTrue(c["can_calibrate_resource_shares"])
        self.assertFalse(c["identifiable_stackelberg_equilibrium"])
    def test_assess_does_not_claim_positive_burt(self):
        z=mod.assess(dummy())
        self.assertIn("NO_CONFIRMED_BURT",z["decision"])
    def test_openalex_sample_not_linked(self):
        z=mod.eligible_grade(dummy())["OpenAlex"]
        self.assertFalse(z["checks"]["cordis_identity_linkage"])
    def test_ocds_missing_tenderers_blocks_utility(self):
        z=mod.eligible_grade(dummy())["OCDS_REAL_UK"]
        self.assertFalse(z["checks"]["observed_bidders"])
    def test_funding_missing_share(self):
        c=mod.profile_cordis(dummy()["cordis_bulk_profile"])
        self.assertEqual(c["selected_keyword"]["funding_missing_share"]["ecContribution"],0)
if __name__=="__main__":unittest.main()
