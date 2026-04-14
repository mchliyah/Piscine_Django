from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from ex02.models import Tip


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class Ex02TipsTests(TestCase):
    def test_tip_creation_permissions_and_listing(self):
        Tip.objects.filter(content="anon_tip").delete()
        Tip.objects.filter(content="auth_tip").delete()

        anon_post = self.client.post("/", {"content": "anon_tip"})
        self.assertEqual(anon_post.status_code, 200)
        self.assertFalse(Tip.objects.filter(content="anon_tip").exists())

        user = get_user_model().objects.create_user(username="tip_user", password="Pass1234!")
        self.client.force_login(user)

        auth_post = self.client.post("/", {"content": "auth_tip"})
        self.assertEqual(auth_post.status_code, 200)
        self.assertTrue(Tip.objects.filter(content="auth_tip", author=user).exists())

        page = self.client.get("/").content.decode()
        self.assertIn("auth_tip", page)
        self.assertIn("Author: tip_user", page)
        self.assertIn("Date:", page)
