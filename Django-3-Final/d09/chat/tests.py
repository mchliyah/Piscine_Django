from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import ChatMessage, ChatRoom


class ChatViewsTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='alice', password='password123')
		self.room = ChatRoom.objects.get(slug='general')
		ChatMessage.objects.create(room=self.room, user=self.user, content='hello world')

	def test_room_list_requires_authentication(self):
		response = self.client.get(reverse('chat:room_list'))
		self.assertEqual(response.status_code, 302)

	def test_room_list_displays_rooms(self):
		self.client.login(username='alice', password='password123')
		response = self.client.get(reverse('chat:room_list'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'General')

	def test_room_detail_requires_authentication(self):
		response = self.client.get(reverse('chat:room_detail', args=['general']))
		self.assertEqual(response.status_code, 302)

	def test_room_detail_shows_persistent_messages(self):
		self.client.login(username='alice', password='password123')
		response = self.client.get(reverse('chat:room_detail', args=['general']))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'hello world')


class ChatMessageOrderingTests(TestCase):
	def test_messages_order_by_creation(self):
		user = User.objects.create_user(username='bob', password='password123')
		room = ChatRoom.objects.create(name='Dev', slug='dev')
		first = ChatMessage.objects.create(room=room, user=user, content='first')
		second = ChatMessage.objects.create(room=room, user=user, content='second')

		ordered = list(ChatMessage.objects.filter(room=room))
		self.assertEqual(ordered[0].id, first.id)
		self.assertEqual(ordered[1].id, second.id)
