from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class Ex01AuthFlowTests(TestCase):
    def test_register_login_logout_flow(self):
        user_model = get_user_model()
        user_model.objects.create_user(username="already_user", password="Pass1234!")

        duplicate = self.client.post(
            "/register/",
            {
                "username": "already_user",
                "password": "Pass1234!",
                "password_confirmation": "Pass1234!",
            },
        )
        self.assertEqual(duplicate.status_code, 200)
        self.assertIn("already", duplicate.content.decode().lower())

        mismatch = self.client.post(
            "/register/",
            {
                "username": "new_user",
                "password": "Pass1234!",
                "password_confirmation": "NoMatch",
            },
        )
        self.assertEqual(mismatch.status_code, 200)
        self.assertIn("match", mismatch.content.decode().lower())

        ok_register = self.client.post(
            "/register/",
            {
                "username": "new_user",
                "password": "Pass1234!",
                "password_confirmation": "Pass1234!",
            },
        )
        self.assertEqual(ok_register.status_code, 302)
        self.assertEqual(ok_register.headers["Location"], "/")

        home_logged = self.client.get("/").content.decode()
        self.assertIn("Hello new_user [0]!", home_logged)
        self.assertIn("Log out", home_logged)

        blocked_login = self.client.get("/login/")
        blocked_register = self.client.get("/register/")
        self.assertEqual(blocked_login.status_code, 302)
        self.assertEqual(blocked_register.status_code, 302)
        self.assertEqual(blocked_login.headers["Location"], "/")
        self.assertEqual(blocked_register.headers["Location"], "/")

        logout = self.client.get("/logout/")
        self.assertEqual(logout.status_code, 302)
        self.assertEqual(logout.headers["Location"], "/")

        bad_login = self.client.post("/login/", {"username": "new_user", "password": "wrong"})
        self.assertEqual(bad_login.status_code, 200)
        self.assertIn("wrong username/password", bad_login.content.decode().lower())

        ok_login = self.client.post("/login/", {"username": "new_user", "password": "Pass1234!"})
        self.assertEqual(ok_login.status_code, 302)
        self.assertEqual(ok_login.headers["Location"], "/")
