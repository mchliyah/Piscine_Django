import re

from django.conf import settings
from django.test import TestCase, override_settings


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class Ex00AnonymousSessionTests(TestCase):
    def test_anonymous_name_persists_then_refreshes(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        match = re.search(r"Hello\s+([^!<]+)!", response.content.decode())
        self.assertIsNotNone(match)
        first_name = match.group(1).strip()
        self.assertIn(first_name, settings.USER_NAMES)

        response_again = self.client.get("/")
        match_again = re.search(r"Hello\s+([^!<]+)!", response_again.content.decode())
        self.assertIsNotNone(match_again)
        self.assertEqual(first_name, match_again.group(1).strip())

        session = self.client.session
        session["user_name"] = "FORCED_OLD_NAME"
        session["timestamp"] = 0
        session.save()

        refreshed = self.client.get("/")
        refreshed_match = re.search(r"Hello\s+([^!<]+)!", refreshed.content.decode())
        self.assertIsNotNone(refreshed_match)
        refreshed_name = refreshed_match.group(1).strip()
        self.assertIn(refreshed_name, settings.USER_NAMES)
        self.assertNotEqual(refreshed_name, "FORCED_OLD_NAME")
