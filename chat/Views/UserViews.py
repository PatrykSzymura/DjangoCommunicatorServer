# Create your views here.
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from chat.Serializers import User, Messeges, Token, Channel
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User as BaseUser
from chat import models as m



class GetUserData(generics.RetrieveAPIView):
    queryset = m.ChatUser.objects.all()
    serializer_class = User.ChatUserSerializer
    permission_classes = (IsAuthenticated,)

class RestrictedGetUserData(generics.RetrieveAPIView):
    def get_queryset(self):
        #print(F'{self.kwargs['pk']} {self.request.user.chatuser.id}')
        #return m.ChatUser.objects.filter(id=self.kwargs['pk'])
        return m.ChatUser.objects.all()

    def get_serializer_class(self):
        if self.request.user.chatuser.authorityLevel == 3:
            return User.AdminAccessUserSerializer
        else:
            return User.ChatUserMinimumDataSerializer

    permission_classes = (IsAuthenticated,)

class CreateUser(generics.CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = User.CreateAccountSerializer
    permission_classes = (AllowAny,)

class UpdateUser(generics.RetrieveUpdateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = User.UpdateAccountData
    permission_classes = (AllowAny,)

class DeleteUser(generics.DestroyAPIView):

    def get_queryset(self):
        return m.User.objects.all()

    serializer_class = User.BaseUserSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        try:
            if request.user.chatuser.authorityLevel == 3:
                instance = self.get_object()
                instance.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                raise PermissionDenied
        except:
            return PermissionDenied()

class UserList(generics.ListAPIView):
    queryset = m.ChatUser.objects.all()
    def get_serializer_class(self):
        try:
            if self.request.user.chatuser.authorityLevel == 3:
                return User.AdminAccessUserSerializer
            else:
                raise PermissionDenied
        except:
            raise PermissionDenied

    permission_classes = (AllowAny,)

class ChangePassword(generics.UpdateAPIView):
    queryset = m.User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = User.ChangePasswordSerializer

    def perform_update(self, serializer):
        try:
            if self.request.user.chatuser.authorityLevel == 3:
                serializer.save()
            elif self.request.user.id == self.kwargs['pk']:
                serializer.save()
            else:
                raise PermissionDenied
        except:
            raise PermissionDenied


    def update(self, request, *args, **kwargs):
        return self.perform_update(serializer=self.serializer_class)


