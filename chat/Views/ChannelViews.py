# Create your views here.
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from chat.Serializers import Channel
from chat import models as m



# View to list brief details of all channels accessible to the authenticated user
class AllBrief(generics.ListAPIView):
    queryset = m.Channel.objects.all()
    serializer_class = Channel.BriefChannelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        try:
            # Get the related ChatUser instance of the current user
            chat_user = self.request.user.chatuser
            # If user has the highest authority level, return all channels
            if chat_user.authorityLevel == 3:
               return m.Channel.objects.all()
            # Otherwise, return only channels the user is a member of
            return m.Channel.objects.filter(channelmembers__user=chat_user).distinct()
        except:
            # Raise permission denied if any error occurs (e.g., no chat user)
            raise PermissionDenied


# View to list detailed information of all channels (requires authentication)
class AllDetail(generics.ListAPIView):
    queryset = m.Channel.objects.all()
    serializer_class = Channel.DetailChannelSerializer
    permission_classes = (IsAuthenticated,)


# View to create a new channel with detailed information
class AddNew(generics.CreateAPIView):
    queryset = m.Channel.objects.all()
    serializer_class = Channel.DetailChannelSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        # Save the new channel if the data is valid, else print errors
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            raise ValidationError


# View to update an existing channel's details
class Update(generics.UpdateAPIView):
    queryset = m.Channel.objects.all()
    serializer_class = Channel.DetailChannelSerializer
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        # Save the changes if the data is valid, else raise a validation error
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValidationError


# View to delete a channel (only allowed for users with high authority)
class Delete(generics.DestroyAPIView):
    queryset = m.Channel.objects.all()
    serializer_class = Channel.BriefChannelSerializer
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, instance):
        # Only users with authority level 3 are allowed to delete a channel
        if self.request.user.chatuser.authorityLevel == 3:
            instance.delete()
        else:
            raise PermissionDenied

    def destroy(self, request, *args, **kwargs):
        # Perform deletion and return a custom success response
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Channel Deleted successfully"}, status=status.HTTP_200_OK)
