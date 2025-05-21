from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .User import ChatUserSerializer
from .Messeges import MessageSerializers

from chat import models as m

class BriefChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Channel
        fields = ['id', 'name']

class DetailChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Channel
        fields = ['id','name','description']
        extra_kwargs = {'description': {'required': False},'id': {'read_only': True}}


