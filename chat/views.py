from django.contrib.messages.context_processors import messages
from django.db.models import QuerySet
from django.shortcuts import render
from django.template.loader import render_to_string

# Create your views here.
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from chat.serializers import MyTokenObtainPairSerializer, ChatUserSerializer, ChannelSerializer, ChannelDetailSerializer
from chat import models as m
from chat import serializers as s


def index(request):
    rendered = render_to_string("sus.html")
    return HttpResponse(rendered)

from rest_framework_simplejwt.views import TokenObtainPairView


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



class ChannelViewDetails(generics.ListAPIView):
    serializer_class = ChannelDetailSerializer

    def get_queryset(self):
        x : QuerySet = m.Messages.objects.filter(channelId=self.kwargs['pk'])
        y : QuerySet = m.ChannelMembers.objects.filter(channelId=self.kwargs['pk'])
        z = x | y

        print(z)
        return m.Channel.objects.filter(id=self.kwargs['pk'])