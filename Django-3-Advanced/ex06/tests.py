from django.contrib.auth.models import User
from django.test import TestCase

from ex00.models import Article, UserFavouriteArticle


class Ex06AccessControlTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='alice',
			password='password123',
		)
		self.other_user = User.objects.create_user(
			username='bob',
			password='password123',
		)
		self.article_1 = Article.objects.create(
			title='Article 1',
			synopsis='Synopsis 1',
			content='Content 1',
			author=self.user,
		)
		self.article_2 = Article.objects.create(
			title='Article 2',
			synopsis='Synopsis 2',
			content='Content 2',
			author=self.user,
		)

	def test_publications_view_is_only_accessible_by_registered_users(self):
		response = self.client.get('/en/publications/')

		self.assertEqual(response.status_code, 302)
		self.assertIn('/en/login/', response['Location'])

		self.client.login(username='alice', password='password123')
		response = self.client.get('/en/publications/')

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'publications.html')

	def test_publish_view_is_only_accessible_by_registered_users(self):
		response = self.client.get('/en/publish/')

		self.assertEqual(response.status_code, 302)
		self.assertIn('/en/login/', response['Location'])

		self.client.login(username='alice', password='password123')
		response = self.client.get('/en/publish/')

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'publish.html')

	def test_favourites_view_is_only_accessible_by_registered_users(self):
		response = self.client.get('/en/favourites/')

		self.assertEqual(response.status_code, 302)
		self.assertIn('/en/login/', response['Location'])

		self.client.login(username='alice', password='password123')
		response = self.client.get('/en/favourites/')

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'favourites.html')

	def test_register_view_is_not_accessible_by_registered_users(self):
		self.client.login(username='alice', password='password123')
		response = self.client.get('/en/register/')

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['Location'], '/en/')

	def test_adding_same_article_twice_does_not_duplicate_favourite(self):
		self.client.login(username='alice', password='password123')

		response = self.client.post(
			f'/en/detail/{self.article_1.id}/favourite/',
			{'article': self.article_1.id},
		)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(
			UserFavouriteArticle.objects.filter(
				user=self.user,
				article=self.article_1,
			).count(),
			1,
		)

		response = self.client.post(
			f'/en/detail/{self.article_1.id}/favourite/',
			{'article': self.article_1.id},
		)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(
			UserFavouriteArticle.objects.filter(
				user=self.user,
				article=self.article_1,
			).count(),
			1,
		)
