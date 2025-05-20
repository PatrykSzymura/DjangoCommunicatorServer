from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .User import ChatUserSerializer
from .Messeges import MessageSerializers

from chat import models as m

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Channel
        fields = ['id', 'name']

class ChannelDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializers(many=True, read_only=True)
    users    = ChatUserSerializer(many=True, read_only=True)
    class Meta:
        model = m.Channel
        fields = ['id','name']

class ChannelMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.ChannelMembers
        fields = '__all__'
