from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from chat.Serializers import Messeges
from chat import models as m

class Get(generics.ListAPIView):
    def get_queryset(self):
        return m.Messages.objects.filter(channelId=self.kwargs['pk'])
    serializer_class = Messeges.MessageSerializer
    permission_classes = (IsAuthenticated,)

class Create(generics.CreateAPIView):
    serializer_class = Messeges.CreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        instance = serializer.save()

        author = serializer.validated_data
        #print(author)
        channel_id = instance.channelId.id
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"channel_{channel_id}",
            {
                "type": "notify",
                "message": "New Messege",
                "data": {
                    "event": "new_messege",
                    "Channel_id": channel_id,
                    "Author": instance.author.nickname},
            }
        )

class Update(generics.UpdateAPIView):
    serializer_class = Messeges.MessageUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return m.Messages.objects.filter(id=self.kwargs['pk'])

    def perform_update(self, serializer):
        instance = serializer.save()
        channel_id = instance.channelId.id

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"channel_{channel_id}",
            {
                "type": "notify",
                "message": "Message updated in your channel",
                "data": {"message_id": instance.id}
            }
        )
