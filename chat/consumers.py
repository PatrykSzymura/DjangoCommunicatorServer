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
    """
    Handles WebSocket connections for voice channels.
    """

    async def connect(self):
        # Channel name pulled from the URL
        self.channel_name = self.scope['url_route']['kwargs']['channel_name']
        self.group_name = f"voice_{self.channel_name}"

        # Join the voice channel
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the voice channel
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Handle incoming WebRTC signaling messages and broadcast.
        """
        # Broadcast message to the group
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "voice_message",
                "message": text_data,
            }
        )

    async def voice_message(self, event):
        """
        Handle messages sent to the group.
        """
        message = event["message"]
        await self.send(text_data=message)
