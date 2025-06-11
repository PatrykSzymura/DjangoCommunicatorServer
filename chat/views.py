from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
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

