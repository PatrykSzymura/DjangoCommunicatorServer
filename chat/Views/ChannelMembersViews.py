# Create your views here.
from django.http import HttpResponse
from django.utils.http import escape_leading_slashes
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from chat import models as m

from chat.Serializers.ChannelMembers import ChannelMemberSerializer, AddMemberSerializer, RemoveMemberSerializer
from chat.models import ChatUser, Channel, ChannelMembers
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class GetMembersList(generics.ListAPIView):
    def get_queryset(self):
        return m.ChannelMembers.objects.filter(channel=self.kwargs['pk'])
    serializer_class = ChannelMemberSerializer
    permission_classes = (AllowAny,)

class GetMyChannel(generics.ListAPIView):
    def get_queryset(self):
        c = m.ChannelMembers.objects.filter(user=self.request.user.id)
        return c
    serializer_class = ChannelMemberSerializer
    permission_classes = (IsAuthenticated,)




class AddMember(generics.CreateAPIView):
    queryset = ChannelMembers.objects.all()
    serializer_class = AddMemberSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        if serializer.is_valid():
            member = serializer.save()
            channel_id = member.channel.id

            # Notify users in the channel
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"channel_{channel_id}",
                {
                    "type": "notify",
                    "message": f"New user added to channel {channel_id}",
                    "data": {
                        "event": "user_added",
                        "user_id": member.user.id,
                        "channel_id": channel_id
                    }
                }
            )

            async_to_sync(channel_layer.group_send)(
                f"user_{member.user.id}",
                {
                    "type": "notify",
                    "message": "You were added to a new channel.",
                    "data": {
                        "event": "added_you",
                        "channel_id": channel_id
                    }
                }
            )
        else:
            print(serializer.errors)
class DeleteMember(generics.RetrieveDestroyAPIView):
    serializer_class = RemoveMemberSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        user_id = self.request.query_params.get('user_id')
        channel_id = self.request.query_params.get('channel_id')

        if not user_id or not channel_id:
            raise NotFound("Both 'user_id' and 'channel_id' must be provided.")

        try:
            chat_user = ChatUser.objects.get(user__id=user_id)
            channel_member = ChannelMembers.objects.get(user=chat_user, channel__id=channel_id)
            return channel_member
        except ChatUser.DoesNotExist:
            raise NotFound("ChatUser with the given user_id does not exist.")
        except ChannelMembers.DoesNotExist:
            raise NotFound("ChannelMember with the given user_id and channel_id does not exist.")

    def destroy(self, request, *args, **kwargs):
        channel_member = self.get_object()
        channel_id = channel_member.channel.id
        chat_user = channel_member.user
        user_id = chat_user.user.id  # Django auth User ID

        # Delete member from channel
        channel_member.delete()

        # Prepare channel layer
        channel_layer = get_channel_layer()

        # Notify all remaining members in the channel
        async_to_sync(channel_layer.group_send)(
            f"channel_{channel_id}",
            {
                "type": "notify",
                "message": f"{chat_user.nickname} was removed from the channel.",
                "data": {
                    "event": "user_removed",
                    "user_id": user_id,
                    "channel_id": channel_id
                }
            }
        )

        # Notify the affected user directly
        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {
                "type": "notify",
                "message": f"You were removed from channel {channel_id}.",
                "data": {
                    "event": "removed_you",
                    "channel_id": channel_id
                }
            }
        )

        return Response(status=status.HTTP_200_OK)

