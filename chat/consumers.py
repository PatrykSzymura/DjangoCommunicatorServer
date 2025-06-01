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
    channels_users = {}  # kanał: set(nicków)

    async def connect(self):
        self.channel_id = self.scope['url_route']['kwargs']['channel_name']
        self.group_name = f"voice_{self.channel_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        self.nickname = None

    async def disconnect(self, close_code):
        if self.nickname:
            VoiceChannelConsumer.channels_users[self.channel_id].discard(self.nickname)
            await self.send_user_list()
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        typ = data.get("type")

        if typ == "join":
            self.nickname = data.get("nickname")
            VoiceChannelConsumer.channels_users.setdefault(self.channel_id, set()).add(self.nickname)
            await self.send_user_list()

        elif typ in {"offer", "answer", "ice"}:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "signal",
                    "data": data,
                    "sender": self.channel_name
                }
            )
            
        elif typ == "mute":
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "broadcast_mute",
                    "nickname": data.get("nickname"),
                    "muted": data.get("muted")
                }
            )

    async def signal(self, event):
        if self.channel_name != event["sender"]:
            await self.send(text_data=json.dumps(event["data"]))

    async def send_user_list(self):
        user_list = list(VoiceChannelConsumer.channels_users.get(self.channel_id, []))
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "users.update",
                "usernames": user_list,
                "sender": self.channel_name
            }
        )

    async def users_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "users",
            "usernames": event["usernames"]
        }))
        
    async def broadcast_mute(self, event):
        await self.send(text_data=json.dumps({
            "type": "mute",
            "nickname": event["nickname"],
            "muted": event["muted"]
        }))
