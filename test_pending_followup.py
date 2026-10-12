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

        self.assertIn("ADL — 4-day pending: Aluva (Anu) is holding 2 tickets.", message)
        self.assertIn("ADTv — 5-day pending: Kottayam (Binu) is holding 3 tickets.", message)
        self.assertIn("ADTv — 3-day pending: Kottayam (Binu) [1], Manarcad (Chitra) [2].", message)
        self.assertNotIn("1-day", message)

    def test_uses_only_the_dispatched_tl_card_and_skips_acso(self):
        sections = {
            "adl_team": pd.DataFrame([{"CENTER": "Aluva", "Name": "Anu", "3 day": 1}]),
            "adtv_team": pd.DataFrame([{"CENTER": "Kottayam", "Name": "Binu", "3 day": 1}]),
        }

        self.assertIn("ADL", build_pending_followup_message(sections, report_type="adl_team"))
        self.assertNotIn("ADTv", build_pending_followup_message(sections, report_type="adl_team"))
        self.assertEqual("", build_pending_followup_message(sections, report_type="adl_acso"))

    def test_schedule_catches_up_after_short_restart_but_not_old_slots(self):
        now = datetime(2026, 10, 12, 10, 30)
        slot = {"id": 1, "is_enabled": 1, "run_time": "10:00", "last_run": ""}
        self.assertTrue(schedule_slot_is_due(slot, now))
        self.assertFalse(schedule_slot_is_due({**slot, "last_run": "2026-10-12 10:01:00"}, now))
        self.assertFalse(schedule_slot_is_due({**slot, "run_time": "07:00"}, now))


if __name__ == "__main__":
    unittest.main()
