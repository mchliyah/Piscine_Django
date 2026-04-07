from pathlib import Path
from tempfile import TemporaryDirectory

from django.test import TestCase, override_settings


class Ex02FormHistoryTests(TestCase):
    def test_get_ex02_displays_empty_history(self):
        with TemporaryDirectory() as tmp_dir:
            log_path = Path(tmp_dir) / "history.log"
            with override_settings(EX02_LOG_PATH=log_path):
                response = self.client.get("/ex02")

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "No history yet.")

    def test_post_ex02_writes_log_and_displays_history(self):
        with TemporaryDirectory() as tmp_dir:
            log_path = Path(tmp_dir) / "history.log"
            with override_settings(EX02_LOG_PATH=log_path):
                response = self.client.post("/ex02", {"text": "hello piscine"}, follow=True)

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "hello piscine")
                self.assertTrue(log_path.exists())
                log_content = log_path.read_text(encoding="utf-8")
                self.assertIn("hello piscine", log_content)

    def test_history_is_persistent_after_new_request(self):
        with TemporaryDirectory() as tmp_dir:
            log_path = Path(tmp_dir) / "history.log"
            with override_settings(EX02_LOG_PATH=log_path):
                self.client.post("/ex02", {"text": "first entry"}, follow=True)

                # New request cycle should still read data from the log file.
                response = self.client.get("/ex02")

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "first entry")
