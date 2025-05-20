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
from chat import models as m

from chat.Serializers.ChannelMembers import Serializer

class GetMembersList(generics.ListAPIView):
    def get_queryset(self):
        return m.ChannelMembers.objects.filter(channelId=self.kwargs['pk'])
    serializer_class = Serializer
    permission_classes = (AllowAny,)

class AddMember(generics.CreateAPIView):
    queryset = m.ChannelMembers.objects.all()
    serializer_class = Serializer
    permission_classes = (AllowAny,)
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()