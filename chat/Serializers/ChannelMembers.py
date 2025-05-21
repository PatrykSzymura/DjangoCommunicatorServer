from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from chat import models as m
from chat.Serializers.Channel import ChannelSerializer
from chat.Serializers.User import NicknameSerializer


class Serializer(serializers.Serializer):
    userId = NicknameSerializer()
    channelId = ChannelSerializer()
    class Meta:
        model = m.ChannelMembers
        fields = ['channelId, userId']

    def create(self, validated_data):
        return m.ChannelMembers.objects.create(**validated_data)
