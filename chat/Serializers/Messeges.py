from rest_framework import serializers
from chat import models as m

class MessageSerializers(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=m.ChatUser.objects.all())
    class Meta:
        model = m.Messages
        fields = ['id', 'date', 'was_edited', 'edit_date', 'message', 'author', 'channelId']

    def perform_create(self, serializer):
        pass
    def create(self, validated_data):
        message = m.Messages.objects.create(**validated_data)
        return message

class MessageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Messages
        fields = ['message']

    def perform_update(self, serializer):

        self.instance.was_edited = True
        self.instance.edit_date = self.instance.date

        if serializer.is_valid():
            serializer.save()
