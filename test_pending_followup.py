"""Tests for the complaint-report WhatsApp pending follow-up text."""
import unittest
from datetime import datetime

import pandas as pd

from report_engine import build_pending_followup_message
from scheduler_utils import schedule_slot_is_due


class PendingFollowupTests(unittest.TestCase):
    def test_lists_only_three_day_and_older_tl_buckets(self):
        sections = {
            "adl_team": pd.DataFrame([
                {"CENTER": "Aluva", "Name": "Anu", "1 day": 9, "3 day": 0, "4 day": 2},
            ]),
            "adtv_team": pd.DataFrame([
                {"CENTER": "Kottayam", "Name": "Binu", "3 day": 1, "4 day": 0, "5 day": 3},
                {"CENTER": "Manarcad", "Name": "Chitra", "3 day": 2, "4 day": 0, "5 day": 0},
            ]),
        }

        message = build_pending_followup_message(sections)

        self.assertIn("In ADL Team Anu holding 4 day pending.", message)
        self.assertIn("In ADTv Team Binu holding 5 day pending.", message)
        self.assertIn("Team Binu & Team Chitra holding 3 day pending.", message)
        self.assertNotIn("In ADTv Team Binu & Team Chitra", message)
        self.assertNotIn("1 day", message)

    def test_uses_only_the_dispatched_card_style(self):
        sections = {
            "adl_team": pd.DataFrame([{"CENTER": "Aluva", "Name": "Anu", "3 day": 1}]),
            "adtv_team": pd.DataFrame([{"CENTER": "Kottayam", "Name": "Binu", "3 day": 1}]),
            "adtv_acso": pd.DataFrame([{"CENTER": "Kunnamkulam", "Name": "Officer", "3 day": 1}]),
        }

        self.assertIn("Team Anu", build_pending_followup_message(sections, report_type="adl_team"))
        self.assertNotIn("ADTv", build_pending_followup_message(sections, report_type="adl_team"))
        acso_message = build_pending_followup_message(sections, report_type="adtv_acso")
        self.assertEqual("In ADTv Kunnamkulam holding 3 day pending.", acso_message)
        self.assertNotIn("Team", acso_message)

    def test_adl_two_day_text_can_be_enabled_independently_of_adtv(self):
        sections = {
            "adl_team": pd.DataFrame([
                {"CENTER": "Aluva", "Name": "Anu", "2 day": 1, "3 day": 2},
            ]),
            "adtv_team": pd.DataFrame([
                {"CENTER": "Kottayam", "Name": "Binu", "3 day": 4},
            ]),
        }
        settings = {
            "adl_enabled": True,
            "adtv_enabled": False,
            "adl_minimum_days": 2,
            "adl_template": "{intro}{holders} requires action for {days}.",
        }

        message = build_pending_followup_message(sections, followup_settings=settings)

        self.assertEqual(
            "In ADL Team Anu requires action for 3 day.\nTeam Anu requires action for 2 day.",
            message,
        )
        self.assertNotIn("Binu", message)

    def test_schedule_catches_up_after_short_restart_but_not_old_slots(self):
        now = datetime(2026, 10, 12, 10, 30)
        slot = {"id": 1, "is_enabled": 1, "run_time": "10:00", "last_run": ""}
        self.assertTrue(schedule_slot_is_due(slot, now))
        self.assertFalse(schedule_slot_is_due({**slot, "last_run": "2026-10-12 10:01:00"}, now))
        self.assertFalse(schedule_slot_is_due({**slot, "run_time": "07:00"}, now))


if __name__ == "__main__":
    unittest.main()
