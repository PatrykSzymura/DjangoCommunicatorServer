from django.contrib.auth.password_validation import validate_password
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from chat import models as m
from chat.Serializers.Channel import BriefChannelSerializer
from chat.Serializers.User import NicknameSerializer, ChatUserSerializer
from chat.models import ChatUser


class Serializer(serializers.Serializer):
    user = NicknameSerializer()
    channel = BriefChannelSerializer()
    class Meta:
        model = m.ChannelMembers
        fields = ['channel', 'user']

    def create(self, validated_data):
        return m.ChannelMembers.objects.create(**validated_data)

class AddMemberSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=m.ChatUser.objects.all())
    channel = serializers.PrimaryKeyRelatedField(queryset=m.Channel.objects.all())

    def validate(self, data):
        if m.ChannelMembers.objects.filter(
            channel=data['channel'],
            user=data['user']
        ).exists():
            raise serializers.ValidationError("This user is already a member")
        return data

    def create(self, validated_data):
        return m.ChannelMembers.objects.create(
            channel=validated_data['channel'],
            user=validated_data['user']
        )

class RemoveMemberSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=m.ChatUser.objects.all())
    channel = serializers.PrimaryKeyRelatedField(queryset=m.Channel.objects.all())

    def validate(self, data):
        user = data.get('user')
        channel = data.get('channel')

        if not m.ChannelMembers.objects.filter(user=user, channel=channel).exists():
            raise serializers.ValidationError("This user is not a member of the specified channel.")
        return data