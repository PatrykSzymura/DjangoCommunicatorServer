from django.contrib.messages.context_processors import messages
from django.db.models import QuerySet
from django.shortcuts import render
from django.template.loader import render_to_string

# Create your views here.
from django.http import HttpResponse
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from chat.serializers import MyTokenObtainPairSerializer, ChatUserSerializer, ChannelSerializer, \
    ChannelDetailSerializer, ChannelMembersSerializer
from chat import models as m
from chat import serializers as s


def index(request):
    rendered = render_to_string("sus.html")
    return HttpResponse(rendered)

from rest_framework_simplejwt.views import TokenObtainPairView

class UserDataViewSet(generics.ListAPIView):
    def get_queryset(self):
        return m.User.objects.filter(id=self.kwargs['pk'])

    serializer_class = s.UserSerializer
    permission_classes = [AllowAny]

class CreateChatView(generics.CreateAPIView):
    queryset = m.ChatUser.objects.all()

class ListChatUsersView(generics.ListAPIView):
    queryset = m.ChatUser.objects.all()
    serializer_class = ChatUserSerializer
    permission_classes = (AllowAny,)




# CHANNEL VIEWS
class ChannelView(generics.ListAPIView):
    queryset = m.Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = (AllowAny,)

class ChannelCreateView(generics.CreateAPIView):
    queryset = m.Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

class ChannelMembersView(generics.RetrieveAPIView):
    def get_queryset(self):
        queryset = m.ChannelMembers.objects.all()
    serializer_class = ChannelMembersSerializer
    permission_classes = (AllowAny,)


class MessagesView(generics.ListAPIView):
    def get_queryset(self):
        return m.Messages.objects.filter(channelId=self.kwargs['pk'])
    serializer_class = s.MessageSerializers
    permission_classes = (AllowAny,)