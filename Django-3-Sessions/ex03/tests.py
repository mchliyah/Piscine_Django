from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from ex02.models import Tip


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class Ex03VotesTests(TestCase):
	def test_vote_toggle_and_switch(self):
		author = get_user_model().objects.create_user(username="author_user", password="Pass1234!")
		voter = get_user_model().objects.create_user(username="voter_user", password="Pass1234!")
		tip = Tip.objects.create(content="vote_target_tip", author=author)

		anon_upvote = self.client.post(f"/tips/{tip.id}/upvote/")
		self.assertEqual(anon_upvote.status_code, 302)
		tip.refresh_from_db()
		self.assertEqual(tip.upvoters.count(), 0)
		self.assertEqual(tip.downvoters.count(), 0)

		self.client.force_login(voter)

		self.client.post(f"/tips/{tip.id}/upvote/")
		tip.refresh_from_db()
		self.assertEqual(tip.upvoters.count(), 1)
		self.assertEqual(tip.downvoters.count(), 0)

		self.client.post(f"/tips/{tip.id}/upvote/")
		tip.refresh_from_db()
		self.assertEqual(tip.upvoters.count(), 0)
		self.assertEqual(tip.downvoters.count(), 0)

		self.client.post(f"/tips/{tip.id}/upvote/")

		for helper in range(3):
			helper_user = get_user_model().objects.create_user(username=f"helper_{helper}", password="Pass1234!")
			self.client.force_login(helper_user)
			self.client.post(f"/tips/{tip.id}/upvote/")

		for rep_helper in range(3):
			rep_helper_user = get_user_model().objects.create_user(username=f"voter_rep_{rep_helper}", password="Pass1234!")
			voter_tip = Tip.objects.create(content=f"voter_tip_{rep_helper}", author=voter)
			self.client.force_login(rep_helper_user)
			self.client.post(f"/tips/{voter_tip.id}/upvote/")

		self.client.force_login(voter)
		self.client.post(f"/tips/{tip.id}/downvote/")
		tip.refresh_from_db()
		self.assertEqual(tip.upvoters.count(), 3)
		self.assertEqual(tip.downvoters.count(), 1)

	def test_delete_requires_reputation_or_author(self):
		author = get_user_model().objects.create_user(username="author_perm", password="Pass1234!")
		moderator = get_user_model().objects.create_user(username="moderator_user", password="Pass1234!")
		tip = Tip.objects.create(content="permission_target_tip", author=author)

		self.client.force_login(moderator)
		forbidden = self.client.post(f"/tips/{tip.id}/delete/")
		self.assertEqual(forbidden.status_code, 403)

		for helper in range(6):
			helper_user = get_user_model().objects.create_user(username=f"rep_helper_{helper}", password="Pass1234!")
			helper_tip = Tip.objects.create(content=f"helper_tip_{helper}", author=moderator)
			self.client.force_login(helper_user)
			self.client.post(f"/tips/{helper_tip.id}/upvote/")

		self.client.force_login(moderator)
		allowed = self.client.post(f"/tips/{tip.id}/delete/")
		self.assertEqual(allowed.status_code, 302)
		self.assertFalse(Tip.objects.filter(id=tip.id).exists())

	def test_downvote_requires_reputation_or_author(self):
		author = get_user_model().objects.create_user(username="author_downvote", password="Pass1234!")
		plain_user = get_user_model().objects.create_user(username="plain_user", password="Pass1234!")
		tip = Tip.objects.create(content="downvote_rule_tip", author=author)

		self.client.force_login(plain_user)
		forbidden = self.client.post(f"/tips/{tip.id}/downvote/")
		self.assertEqual(forbidden.status_code, 403)
		tip.refresh_from_db()
		self.assertEqual(tip.downvoters.count(), 0)

		self.client.force_login(author)
		author_downvote = self.client.post(f"/tips/{tip.id}/downvote/")
		self.assertEqual(author_downvote.status_code, 302)
		tip.refresh_from_db()
		self.assertTrue(tip.downvoters.filter(id=author.id).exists())

		target_tip = Tip.objects.create(content="target_tip", author=author)
		for helper in range(3):
			helper_user = get_user_model().objects.create_user(username=f"down_rep_{helper}", password="Pass1234!")
			helper_tip = Tip.objects.create(content=f"rep_tip_{helper}", author=plain_user)
			self.client.force_login(helper_user)
			self.client.post(f"/tips/{helper_tip.id}/upvote/")

		self.client.force_login(plain_user)
		allowed = self.client.post(f"/tips/{target_tip.id}/downvote/")
		self.assertEqual(allowed.status_code, 302)
		target_tip.refresh_from_db()
		self.assertTrue(target_tip.downvoters.filter(id=plain_user.id).exists())

	def test_reputation_drops_when_tip_deleted(self):
		user = get_user_model().objects.create_user(username="rep_user", password="Pass1234!")
		tip = Tip.objects.create(content="rep_tip", author=user)

		for helper in range(3):
			helper_user = get_user_model().objects.create_user(username=f"repdel_{helper}", password="Pass1234!")
			self.client.force_login(helper_user)
			self.client.post(f"/tips/{tip.id}/upvote/")

		user.refresh_from_db()
		self.assertEqual(user.reputation, 15)

		self.client.force_login(user)
		self.client.post(f"/tips/{tip.id}/delete/")

		user.refresh_from_db()
		self.assertEqual(user.reputation, 0)
