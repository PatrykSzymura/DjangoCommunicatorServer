from django.utils import timezone
from rest_framework import serializers
from chat import models as m

# Serializer to retrieve message details including author and channel reference
class MessageSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=m.ChatUser.objects.all())
    class Meta:
        model = m.Messages
        fields = ['id', 'date', 'was_edited', 'edit_date', 'message', 'author', 'channelId']

# Serializer used when creating a new message
class CreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=m.ChatUser.objects.all())
    class Meta:
        model = m.Messages
        fields = ['id', 'message', 'author', 'channelId']
    #Create method ensure was_edited is False and edit_date is None
    def create(self, validated_data):
        validated_data['was_edited'] = False
        validated_data['edit_date'] = None
        return m.Messages.objects.create(**validated_data)

# Serializer used to update an existing message (usually only the message text)
class MessageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Messages
        fields = ['message','was_edited']

    def update(self, instance, validated_data):
        instance.message = validated_data.get('message', instance.message)
        #Setting edit parmeters
        instance.was_edited = True
        instance.edit_date = timezone.now()  # Use current timestamp
        #Saving changes
        instance.save()
        return instance
