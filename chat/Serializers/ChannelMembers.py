from rest_framework import  serializers
from chat import models as m
from chat.Serializers.Channel import BriefChannelSerializer
from chat.Serializers.User import NicknameSerializer, ChatUserSerializer
from chat.models import ChatUser

# Serializer to represent a ChannelMembers object using nested serializers
class ChannelMemberSerializer(serializers.Serializer):
    user = NicknameSerializer()  # Nested serializer for user info
    channel = BriefChannelSerializer()  # Nested serializer for channel info

    class Meta:
        model = m.ChannelMembers
        fields = ['channel', 'user']

    def create(self, validated_data):
        # Create a new ChannelMembers instance from validated data
        return m.ChannelMembers.objects.create(**validated_data)

# Serializer to add a user to a channel using primary key references
class AddMemberSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=m.ChatUser.objects.all())
    channel = serializers.PrimaryKeyRelatedField(queryset=m.Channel.objects.all())

    def validate(self, data):
        # Ensure the user is not already a member of the specified channel
        if m.ChannelMembers.objects.filter(
            channel=data['channel'],
            user=data['user']
        ).exists():
            raise serializers.ValidationError("This user is already a member")
        return data

    def create(self, validated_data):
        # Create and return a new ChannelMembers entry
        return m.ChannelMembers.objects.create(
            channel=validated_data['channel'],
            user=validated_data['user']
        )

# Serializer to remove a user from a channel (used for validation and structure only)
class RemoveMemberSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=m.ChatUser.objects.all())
    channel = serializers.PrimaryKeyRelatedField(queryset=m.Channel.objects.all())

    class Meta:
        model = m.ChannelMembers
        fields = ['channel', 'user']