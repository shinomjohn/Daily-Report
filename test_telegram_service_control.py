"""Telegram restart must never report success when systemctl was denied."""
import unittest
from unittest.mock import patch

import telegram_bot


class TelegramServiceControlTests(unittest.TestCase):
    def test_restart_fails_when_no_noninteractive_systemctl_permission(self):
        with patch.object(telegram_bot.sys, "platform", "linux"), patch(
            "telegram_bot.run_shell_command",
            side_effect=[(1, "", "sudo: a password is required"), (1, "", "access denied")],
        ):
            ok, message = telegram_bot._exec_service_command("restart")

        self.assertFalse(ok)
        self.assertIn("access denied", message)

    def test_service_unit_is_explicit_for_the_restricted_sudoers_rule(self):
        self.assertTrue(telegram_bot._service_unit_name().endswith(".service"))


if __name__ == "__main__":
    unittest.main()
