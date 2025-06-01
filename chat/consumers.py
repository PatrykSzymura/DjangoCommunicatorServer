from channels.generic.websocket import AsyncWebsocketConsumer
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
    async def connect(self):
        self.channel_id = self.scope['url_route']['kwargs']['channel_name']
        self.group_name = f"voice_{self.channel_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        self.nickname = None

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        typ = data.get("type")

        if typ == "join":
            self.nickname = data.get("nickname")
            await self.send_users_list()
        elif typ in {"offer", "answer", "ice"}:
            # Przekaż do innych użytkowników w tym kanale
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "webrtc.signal",
                    "sender": self.channel_name,
                    "data": data
                }
            )

    async def webrtc_signal(self, event):
        if self.channel_name != event["sender"]:
            await self.send(text_data=json.dumps(event["data"]))

    async def send_users_list(self):
        # możesz też dodać bazę danych lub pamięć do trzymania nicków
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "users.update",
                "sender": self.channel_name,
                "usernames": [self.nickname] if self.nickname else []
            }
        )

    async def users_update(self, event):
        if self.channel_name != event["sender"]:
            await self.send(text_data=json.dumps({
                "type": "users",
                "usernames": event["usernames"]
            }))
