from django.shortcuts import render
from django.template.loader import render_to_string

# Create your views here.
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from chat.serializers import MyTokenObtainPairSerializer, ChatUserSerializer
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