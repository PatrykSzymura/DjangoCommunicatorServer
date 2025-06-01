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
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):

        author = serializer.validated_data
        #print(author)
        if serializer.is_valid():
            serializer.save()

class MessagesUpdateView(generics.UpdateAPIView):

    def get_queryset(self):
        return m.Messages.objects.filter(id=self.kwargs['pk'])

    serializer_class = Messeges.MessageUpdateSerializer
    permission_classes = (AllowAny,)
