from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # WebSocket route for live notifications
    re_path(r"ws/notifications/$", consumers.NotificationConsumer.as_asgi()),

    # WebSocket route for voice channels
    re_path(r"ws/voice/(?P<channel_name>\w+)/$", consumers.VoiceChannelConsumer.as_asgi()),
]

