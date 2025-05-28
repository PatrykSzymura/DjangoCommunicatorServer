# Create your views here.
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from chat.Serializers import User, Messeges, Token, Channel
from chat import models as m

class AllBrief(generics.ListAPIView):
    queryset = m.Channel.objects.all()
    serializer_class = Channel.BriefChannelSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        chat_user = self.request.user.chatuser
        try:
            print(f"{m.ChannelMembers.objects.filter(user=chat_user)}")
            if chat_user.authorityLevel == 3:
               return m.Channel.objects.all()
            return m.Channel.objects.filter(channelmembers__user=chat_user).distinct()
        except:
            raise PermissionDenied

class AllDetail(generics.ListAPIView):
    queryset = m.Channel.objects.all()
    serializer_class = Channel.DetailChannelSerializer
    permission_classes = (AllowAny,)

class AddNew(generics.CreateAPIView):
    queryset = m.Channel.objects.all()
    serializer_class = Channel.DetailChannelSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

class Update(generics.UpdateAPIView):
    queryset = m.Channel.objects.all()
    serializer_class = Channel.DetailChannelSerializer
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        #userPermissions = self.request.user.chatuser.authorityLevel
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            raise PermissionDenied

class Delete(generics.DestroyAPIView):
    queryset = m.Channel.objects.all()
    serializer_class = Channel.BriefChannelSerializer
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, instance):
        if self.request.user.chatuser.authorityLevel == 3:
            instance.delete()
        else:
            raise PermissionDenied

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Channel Deleted successfully"}, status=status.HTTP_200_OK)