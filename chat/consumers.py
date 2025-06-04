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

        # ✅ Personal user group
        self.user_group = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.user_group, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(self.channel_group, self.channel_name)
        except:
            print("user is not in channel group")
        await self.channel_layer.group_discard(self.user_group, self.channel_name)

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




class VoiceChannelConsumer(AsyncWebsocketConsumer):
    channels_users = {}  # channel_id -> set of nicknames

    async def connect(self):
        self.channel_id = self.scope['url_route']['kwargs']['channel_name']
        self.group_name = f"voice_{self.channel_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        self.nickname = None

        if self.channel_id not in self.__class__.channels_users:
            self.__class__.channels_users[self.channel_id] = set()

        await self.broadcast_users()

    async def disconnect(self, close_code):
        if self.nickname:
            self.__class__.channels_users[self.channel_id].discard(self.nickname)
            await self.broadcast_users()
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if text_data and text_data.startswith("JOIN|"):
            try:
                _, nick, _ = text_data.strip().split("|", 2)
                self.nickname = nick.strip().lower()
            except Exception as e:
                print("[WS] Błąd JOIN:", e)
                return

            if self.channel_id not in self.__class__.channels_users:
                self.__class__.channels_users[self.channel_id] = set()

            self.__class__.channels_users[self.channel_id].add(nick)
            await self.broadcast_users()

        elif bytes_data:
            if bytes_data.startswith(b"AUDIO|"):
                try:
                    _, nick, audio = bytes_data.split(b"|", 2)
                    nick = nick.decode("utf-8")

                    await self.channel_layer.group_send(
                        self.group_name,
                        {
                            "type": "voice_binary",
                            "data": audio,
                            "sender_nick": nick
                        }
                    )
                except Exception as e:
                    print("[WS] Błąd dekodowania AUDIO:", e)

    async def broadcast_users(self):
        users = self.__class__.channels_users.get(self.channel_id, set())
        msg = "USERS|" + "|".join(sorted(users))
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "voice_message",
                "message": msg,
            }
        )

    async def voice_message(self, event):
        try:
            await self.send(text_data=event["message"])
        except Exception as e:
            print("[WS] Błąd wiadomości:", e)

    async def voice_binary(self, event):
        try:
            if not self.nickname:
                return  # Nie znam jeszcze własnego nicku — ignoruję
            sender_nick = event.get("sender_nick", "").strip().lower()
            if self.nickname.strip().lower() == sender_nick:
                return  # Nie wysyłaj audio do siebie
            packet = b"AUDIO|" + sender_nick.encode("utf-8") + b"|" + event["data"]
            await self.send(bytes_data=packet)
        except Exception as e:
            print("[WS] Błąd audio:", e)
