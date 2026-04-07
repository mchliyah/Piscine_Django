from django.test import TestCase, override_settings


class Ex03TableTests(TestCase):
    def test_ex03_page_renders_table(self):
        with override_settings(ALLOWED_HOSTS=["localhost", "127.0.0.1", "testserver"]):
            response = self.client.get("/ex03")

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertEqual(content.count("<tr>"), 51)
        self.assertEqual(content.count("<th"), 4)
        self.assertEqual(content.count("<td"), 200)
        self.assertIn("noir", content)
        self.assertIn("rouge", content)
        self.assertIn("bleu", content)
        self.assertIn("vert", content)

    def test_ex03_shades_are_unique_per_column(self):
        with override_settings(ALLOWED_HOSTS=["localhost", "127.0.0.1", "testserver"]):
            response = self.client.get("/ex03")

        self.assertEqual(response.status_code, 200)
        context_columns = response.context["columns"]
        for column in context_columns:
            self.assertEqual(len(column["shades"]), 50)
            self.assertEqual(len(set(column["shades"])), 50)
