from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class AccountAjaxTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='password123')
        self.client = Client(enforce_csrf_checks=True)

    def test_page_shows_login_form_when_anonymous(self):
        response = self.client.get(reverse('account:page'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log in')
        self.assertIn('csrftoken', response.cookies)

    def test_ajax_login_and_logout_flow(self):
        page = self.client.get(reverse('account:page'))
        csrftoken = page.cookies['csrftoken'].value

        login_response = self.client.post(
            reverse('account:ajax_login'),
            {'username': 'alice', 'password': 'password123'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_X_CSRFTOKEN=csrftoken,
        )

        self.assertEqual(login_response.status_code, 200)
        login_payload = login_response.json()
        self.assertTrue(login_payload['success'])
        self.assertEqual(login_payload['username'], 'alice')
        self.assertIn('Logged as', login_payload['logged_in_html'])

        self.assertTrue('_auth_user_id' in self.client.session)

        logout_response = self.client.post(
            reverse('account:ajax_logout'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_X_CSRFTOKEN=self.client.cookies['csrftoken'].value,
        )

        self.assertEqual(logout_response.status_code, 200)
        logout_payload = logout_response.json()
        self.assertTrue(logout_payload['success'])
        self.assertIn('id="login-form"', logout_payload['login_form_html'])

    def test_ajax_login_returns_form_errors(self):
        page = self.client.get(reverse('account:page'))
        csrftoken = page.cookies['csrftoken'].value

        response = self.client.post(
            reverse('account:ajax_login'),
            {'username': 'alice', 'password': 'wrong-password'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_X_CSRFTOKEN=csrftoken,
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('Please enter a correct username and password', response.content.decode())
