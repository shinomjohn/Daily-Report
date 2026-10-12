"""Regression tests for the directory's user-facing center display name."""

import unittest
from unittest.mock import patch

import report_layout


class CenterDisplayNameTests(unittest.TestCase):
    def test_display_name_is_used_for_both_platform_report_centers(self):
        team_leader = {
            "center_name": "Kottayam Central",
            "name": "Anoop",
            "adtv_center": "KOTTAYAM (DA01)",
            "adtv_name": "Anoop",
            "pd_adl_name_key": "ANOOP CRM",
            "pd_adtv_name_key": "ANOOP CRM",
            "pp_adl_emp_code": "1001",
            "pp_adtv_emp_code": "1001",
        }
        acso = {
            "center_name": "Kottayam Central",
            "adl_center_display": "Kottayam ADL CRM",
            "adtv_center_display": "KOTTAYAM (DA01)",
            "acso_name": "Officer Rajesh",
            "adtv_acso_name": "Officer Rajesh",
            "pd_adl_center_key": "Kottayam ADL CRM",
            "pd_adtv_center_key": "KOTTAYAM (DA01)",
            "pp_adl_center_key": "KOTTAYAM PP",
            "pp_adtv_center_key": "KOTTAYAM PP",
        }

        with patch("db_manager.get_team_leaders", return_value=[team_leader]), patch(
            "db_manager.get_acsos", return_value=[acso]
        ):
            tls, acsos = report_layout.get_layout_for_region("kottayam")

        self.assertEqual((tls[0].adl_center, tls[0].adtv_center), ("Kottayam Central", "Kottayam Central"))
        self.assertEqual((acsos[0].adl_center, acsos[0].adtv_center), ("Kottayam Central", "Kottayam Central"))
        self.assertEqual(acsos[0].pd_adtv_center_key, "KOTTAYAM (DA01)")


if __name__ == "__main__":
    unittest.main()
