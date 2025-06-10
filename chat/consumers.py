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

class VoiceChannelConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_name_param = self.scope['url_route']['kwargs']['channel_name']
        self.group_name = f"voice_{self.channel_name_param}"
        self.username = None

        # Join the channel group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if self.username:
            users = active_users.get(self.group_name, set())
            if users:  # Check if users exist before modifying
                users.discard(self.username)
                active_users[self.group_name] = users
            await self.send_user_list()

        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg_type = data.get("type")
        sender = data.get("from")
        recipient = data.get("to")  # Get the recipient

        if msg_type == "join":
            self.username = sender
            users = active_users.get(self.group_name, set())
            if users is None:
                users = set()
            users.add(sender)
            active_users[self.group_name] = users
            await self.send_user_list()
        elif msg_type == "mute_status":
            # Broadcast mute status to other users
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "forward_message",
                    "message": data
                }
            )
        else:
            # Forward the message to the specified recipient
            if recipient:
                await self.channel_layer.send(
                    self.channel_name,  # Send to this specific instance
                    {
                        "type": "forward_message",
                        "message": data
                    }
                )
            else:
                print(f"Error: Recipient not specified for message type {msg_type}")

    async def forward_message(self, event):
        message = event["message"]
        # Don't send the message back to the sender
        if message.get("from") != self.username:
            await self.send(text_data=json.dumps(message))

    async def send_user_list(self):
        users = sorted(active_users.get(self.group_name, set()) or [])  # Handle None case
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "forward_message",
                "message": {
                    "type": "user_list",
                    "users": users
                }
            }
        )

