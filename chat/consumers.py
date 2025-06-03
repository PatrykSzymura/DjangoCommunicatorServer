from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("notifications", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications", self.channel_name)

    async def notify(self, event):
        await self.send(text_data=json.dumps({
            "type": "notification",
            "message": event["message"],
            "data": event.get("data", {})
        }))




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
