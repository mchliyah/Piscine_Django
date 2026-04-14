from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class ChatRoom(models.Model):
	name = models.CharField(max_length=80, unique=True)
	slug = models.SlugField(max_length=80, unique=True)

	def __str__(self):
		return self.name


class ChatMessage(models.Model):
	room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	content = models.TextField()
	is_system = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['created_at', 'id']

	def __str__(self):
		return f'{self.room.slug}::{self.content[:40]}'

# Create your models here.
