from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
import json

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.http.request import RAISE_ERROR

from .models import Channel, ChannelMembers, ChatUser

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if not self.user or self.user.is_anonymous:
            await self.close()
            return

        self.channel_id = self.scope["url_route"]["kwargs"]["channel_id"]
        is_member = await self.user_in_channel(self.user.id, self.channel_id)

        if not is_member:
            await self.close()
            return

        # Channel group
        self.channel_group = f"channel_{self.channel_id}"
        await self.channel_layer.group_add(self.channel_group, self.channel_name)

        # Personal user group
        self.user_group = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.user_group, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(self.channel_group, self.channel_name)
            await self.channel_layer.group_discard(self.user_group, self.channel_name)
        except:
            print("user is not in channel group")

    async def receive(self, text_data):
        # Optional: handle messages sent from frontend
        pass

    async def notify(self, event):
        print(f"Notifying user {self.user.id} | event: {event}")
        await self.send(text_data=json.dumps({
            "type": "notification",
            "message": event.get("message"),
            "data": event.get("data", {})
        }))

    @database_sync_to_async
    def user_in_channel(self, user_id, channel_id):
        try:
            chat_user = ChatUser.objects.get(user__id=user_id)
            return ChannelMembers.objects.filter(user=chat_user, channel__id=channel_id).exists()
        except ChatUser.DoesNotExist:
            return False
            
active_users = {}  # {channel_name: set(usernames)}

# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class VoiceChannelConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        peer_id = text_data_json.get('peer_id', 'unknown_peer')

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'peer_id': peer_id
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        peer_id = event['peer_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'peer_id': peer_id
        }))
