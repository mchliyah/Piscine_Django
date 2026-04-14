import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import ChatMessage, ChatRoom


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get('user')
        self.room_slug = self.scope['url_route']['kwargs']['slug']

        if not user or user.is_anonymous:
            await self.close(code=4401)
            return

        self.room = await self.get_room(self.room_slug)
        if not self.room:
            await self.close(code=4404)
            return

        self.group_name = f'chat_{self.room_slug}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        join_content = f'{user.username} has joined the chat'
        join_payload = await self.create_system_message(self.room.id, join_content)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': join_payload,
            },
        )

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        try:
            payload = json.loads(text_data)
        except json.JSONDecodeError:
            return

        content = (payload.get('message') or '').strip()
        if not content:
            return

        user = self.scope['user']
        message_payload = await self.create_user_message(self.room.id, user.id, content)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message_payload,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    @database_sync_to_async
    def get_room(self, slug):
        try:
            return ChatRoom.objects.get(slug=slug)
        except ChatRoom.DoesNotExist:
            return None

    @database_sync_to_async
    def create_system_message(self, room_id, content):
        message = ChatMessage.objects.create(
            room_id=room_id,
            content=content,
            is_system=True,
        )
        return {
            'username': 'system',
            'content': message.content,
            'is_system': True,
        }

    @database_sync_to_async
    def create_user_message(self, room_id, user_id, content):
        message = ChatMessage.objects.create(
            room_id=room_id,
            user_id=user_id,
            content=content,
            is_system=False,
        )
        return {
            'username': message.user.username,
            'content': message.content,
            'is_system': False,
        }
