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

from chat.Serializers.ChannelMembers import Serializer, AddMemberSerializer
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



class DeleteMember(generics.DestroyAPIView):
    queryset = m.ChannelMembers.objects.all()
    serializer_class = Serializer
    permission_classes = (AllowAny,)

    def perform_destroy(self, instance):
        user =  self.request.user.chatuser.authorityLevel
        try:
            if user == 3:
                instance.delete()
            raise PermissionDenied
        except:
            raise PermissionDenied

    def get_object(self):
        user_id = self.request.data.get('user')
        channel_id = self.request.data.get('channel')

        if not user_id or not channel_id:
            raise ValidationError("Both 'user' and 'channel' must be provided.")

        try:
            return ChannelMembers.objects.get(user__id=user_id, channel__id=channel_id)
        except ChannelMembers.DoesNotExist:
            raise ValidationError("This user is not a member of the specified channel.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Access to channel revoked successfully"}, status=status.HTTP_200_OK)
