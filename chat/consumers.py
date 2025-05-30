from channels.generic.websocket import AsyncWebsocketConsumer
from asyncio import sleep
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    Handles WebSocket connections for user notifications.
    """

    async def connect(self):
        # Group name based on user ID
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.group_name = f"user_{self.user.id}"

            # Add the user to their group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            # Reject connection if the user is not authenticated
            await self.close()

    async def disconnect(self, close_code):
        # Remove the user from their group
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def send_notification(self, event):
        """
        Handles messages sent to the group.
        """
        message = event["message"]
        await self.send(text_data=json.dumps({
            "message": message
        }))


class VoiceChannelConsumer(AsyncWebsocketConsumer):
    channels_users = {}  # channel_id -> set of nicknames

    async def connect(self):
        self.channel_id = self.scope['url_route']['kwargs']['channel_name']
        self.group_name = f"voice_{self.channel_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        self.nickname = None

    async def disconnect(self, close_code):
        if self.nickname and self.nickname in self.__class__.active_users:
            del self.__class__.active_users[self.nickname]
            await self.broadcast_users()
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if text_data and text_data.startswith("JOIN|"):
            _, nick, _ = text_data.split("|", 2)
            self.nickname = nick
            self.__class__.active_users[nick] = True
            await self.broadcast_users()

        elif bytes_data:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "voice_binary",
                    "data": bytes_data
                }
            )

    async def broadcast_users(self):
        msg = "USERS|" + "|".join(sorted(self.__class__.active_users.keys()))
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "voice_message",
                "message": msg,
            }
        )

    async def voice_message(self, event):
        await self.send(text_data=event["message"])

    async def voice_binary(self, event):
        await self.send(bytes_data=event["data"])
