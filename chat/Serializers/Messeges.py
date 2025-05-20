from rest_framework import serializers
from chat import models as m

class MessageSerializers(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=m.ChatUser.objects.all())
    class Meta:
        model = m.Messages
        fields = ['id', 'date', 'was_edited', 'edit_date', 'message', 'author', 'channelId']

class CreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=m.ChatUser.objects.all())
    class Meta:
        model = m.Messages
        fields = ['id', 'message', 'author', 'channelId']

    def perform_create(self, serializer):
        self.instance.was_edited = False
        self.instance.edit_date = None
        self.instance.date = self.instance.date.strftime("%Y-%m-%d %H:%M:%S")
        if serializer.is_valid():
            serializer.save()

class MessageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Messages
        fields = ['message','was_edited']

    def validate(self, attrs):
        if attrs['was_edited'] == None or attrs['was_edited'] == False:
           attrs['was_edited'] = True
        return attrs

    def perform_update(self, serializer):

        self.instance.was_edited = True
        self.instance.edit_date = self.instance.date

        if serializer.is_valid():
            serializer.save()
