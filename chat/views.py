from django.shortcuts import render
from django.template.loader import render_to_string

# Create your views here.
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from chat import models as m
from chat import serializers as s


def index(request):
    rendered = render_to_string("sus.html")
    return HttpResponse(rendered)

class CreateChatView(generics.CreateAPIView):
    queryset = m.ChatUser.objects.all()
