"""Tests for persistent, region-specific complaint follow-up text preferences."""

import unittest
from unittest.mock import patch

import db_manager


class PendingFollowupSettingsTests(unittest.TestCase):
    def test_defaults_are_adl_two_days_and_adtv_three_days(self):
        with patch("db_manager.get_setting", return_value=""):
            settings = db_manager.get_pending_followup_settings("kottayam")

        self.assertTrue(settings["adl_enabled"])
        self.assertTrue(settings["adtv_enabled"])
        self.assertEqual(settings["adl_minimum_days"], 2)
        self.assertEqual(settings["adtv_minimum_days"], 3)

    def test_settings_are_normalized_and_stored_per_region(self):
        with patch("db_manager.set_setting", return_value=True) as set_setting:
            settings = db_manager.set_pending_followup_settings("thrissur", {
                "adl_enabled": False,
                "adtv_enabled": "yes",
                "adl_minimum_days": 0,
                "adtv_minimum_days": 99,
                "adl_template": "ADL {holders}",
                "adtv_template": "ADTv {holders}",
            })

        self.assertFalse(settings["adl_enabled"])
        self.assertTrue(settings["adtv_enabled"])
        self.assertEqual(settings["adl_minimum_days"], 1)
        self.assertEqual(settings["adtv_minimum_days"], 10)
        self.assertEqual(set_setting.call_args.args[0], "pending_followup_settings:thrissur")


if __name__ == "__main__":
    unittest.main()
