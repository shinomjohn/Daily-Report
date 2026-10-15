"""Telegram restart must never report success when systemctl was denied."""
import unittest
from unittest.mock import Mock, patch

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

    @patch("telegram_bot.requests.post")
    def test_complaint_dispatch_queues_instead_of_waiting_for_whatsapp(self, post):
        response = Mock(status_code=200)
        response.json.return_value = {"status": "QUEUED", "message": "Complaint dispatch queued."}
        post.return_value = response

        ok, message = telegram_bot.trigger_group_dispatch("kottayam")

        self.assertTrue(ok)
        self.assertIn("queued", message.lower())
        self.assertEqual(post.call_args.kwargs["timeout"], 15)
        self.assertTrue(post.call_args.kwargs["json"]["background"])

    @patch("telegram_bot.requests.post")
    def test_sr_dispatch_queues_instead_of_waiting_for_whatsapp(self, post):
        response = Mock(status_code=200)
        response.json.return_value = {"status": "QUEUED", "message": "SR dispatch queued."}
        post.return_value = response

        ok, message = telegram_bot.trigger_sr_dispatch("kottayam")

        self.assertTrue(ok)
        self.assertIn("queued", message.lower())
        self.assertEqual(post.call_args.kwargs["timeout"], 15)
        self.assertTrue(post.call_args.kwargs["json"]["background"])


if __name__ == "__main__":
    unittest.main()
