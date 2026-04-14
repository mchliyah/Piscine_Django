from django.contrib import admin

from .models import ChatMessage, ChatRoom


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')
	search_fields = ('name', 'slug')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
	list_display = ('room', 'user', 'is_system', 'created_at')
	list_filter = ('room', 'is_system')
	search_fields = ('content', 'user__username')

# Register your models here.
