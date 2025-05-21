from django.contrib.messages.context_processors import messages
from django.contrib.messages.storage.cookie import MessageSerializer
from django.db.models import QuerySet
from django.shortcuts import render
from django.template.loader import render_to_string

# Create your views here.
from django.http import HttpResponse
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from chat import models as m

from chat.Serializers.ChannelMembers import Serializer

class GetMembersList(generics.ListAPIView):
    def get_queryset(self):
        return m.ChannelMembers.objects.filter(channelId=self.kwargs['pk'])
    serializer_class = Serializer
    permission_classes = (AllowAny,)

class GetMyChannel(generics.ListAPIView):
    def get_queryset(self):
        c = m.ChannelMembers.objects.filter(userId=self.request.user.id)
        return c
    serializer_class = Serializer
    permission_classes = (IsAuthenticated,)

class AddMember(generics.CreateAPIView):
    queryset = m.ChannelMembers.objects.all()
    serializer_class = Serializer
    permission_classes = (AllowAny,)
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()

class DeleteMember(generics.DestroyAPIView):
    queryset = m.ChannelMembers.objects.all()
    serializer_class = Serializer
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, instance):
        if self.request.user.chatuser.authorityLevel == 3:
            instance.delete()
        else:
            raise PermissionDenied

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Access to channel revoked successfully"}, status=status.HTTP_200_OK)
