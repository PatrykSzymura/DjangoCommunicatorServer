from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.messages.context_processors import messages
from django.contrib.messages.storage.cookie import MessageSerializer
from django.db.models import QuerySet
from django.shortcuts import render
from django.template.loader import render_to_string

# Create your views here.
from django.http import HttpResponse
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from .Serializers import User, Messeges, Token, Channel
from chat import models as m



def index(request):
    rendered = render_to_string("sus.html")
    return HttpResponse(rendered)

from rest_framework_simplejwt.views import TokenObtainPairView

class MessagesView(generics.ListAPIView):
    def get_queryset(self):
        return m.Messages.objects.filter(channelId=self.kwargs['pk'])
    serializer_class = Messeges.MessageSerializers
    permission_classes = (AllowAny,)

class MessagesCreateView(generics.CreateAPIView):
    serializer_class = Messeges.CreateSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        instance = serializer.save()

        author = serializer.validated_data
        #print(author)
        channel_id = instance.channelId.id
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"channel_{channel_id}",
            {
                "type": "notify",
                "message": "New Messege",
                "data": {"Channel_id": channel_id, "Author": author.id},
            }
        )

class MessagesUpdateView(generics.UpdateAPIView):
    serializer_class = Messeges.MessageUpdateSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return m.Messages.objects.filter(id=self.kwargs['pk'])

    def perform_update(self, serializer):
        instance = serializer.save()
        channel_id = instance.channelId.id

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"channel_{channel_id}",
            {
                "type": "notify",
                "message": "Message updated in your channel",
                "data": {"message_id": instance.id}
            }
        )
