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

from chat.Serializers.ChannelMembers import Serializer, AddMemberSerializer, RemoveMemberSerializer
from chat.models import ChatUser, Channel, ChannelMembers


class GetMembersList(generics.ListAPIView):
    def get_queryset(self):
        return m.ChannelMembers.objects.filter(channel=self.kwargs['pk'])
    serializer_class = Serializer
    permission_classes = (AllowAny,)

class GetMyChannel(generics.ListAPIView):
    def get_queryset(self):
        c = m.ChannelMembers.objects.filter(user=self.request.user.id)
        return c
    serializer_class = Serializer
    permission_classes = (IsAuthenticated,)


class AddMember(generics.CreateAPIView):
    queryset = ChannelMembers.objects.all()
    serializer_class = AddMemberSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
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
        except ChatUser.DoesNotExist:
            raise NotFound("ChatUser with the given user_id does not exist.")
        except ChannelMembers.DoesNotExist:
            raise NotFound("ChannelMember with the given user_id and channel_id does not exist.")

        return channel_member

    def destroy(self, request, *args, **kwargs):
        channel_member = self.get_object()
        channel_member.delete()
        return Response(status=status.HTTP_200_OK)


