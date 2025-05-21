from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
import chat.views as v
from .routing import websocket_urlpatterns
from chat.Views import ChannelMembers, Channel

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # USERS ENDPOINTS
    path('user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/get/all/', v.ListChatUsersView.as_view(), name='get_chat_users'),
    path('user/get/<int:pk>/', v.UserDataViewSet.as_view(), name='get_chat_users'),
    #path('user/create/'),
    #path('user/update/'),

    # CHAT-CHANNELS ENDPOINTS
    path('channel/create/new/', Channel.AddNew.as_view(), name='create_chat_channel'),
    path('channel/get/list/brief', Channel.AllBrief.as_view() , name='get_chat_channels'),
    path('channel/get/list/detail', Channel.AllDetail.as_view() , name='get_chat_channels'),
    path('channel/update/<int:pk>/', Channel.Update.as_view(), name='update_chat_channel'),
    path('channel/delete/<int:pk>/', Channel.Delete.as_view(), name='delete_chat_channel'),

    # CHANNEL-MEMBERS ENDPOINTS
    path('channel/members/get/',ChannelMembers.GetMyChannel.as_view(), name='get_my_chat_channel_members'),
    path('channel/members/get/<int:pk>/', ChannelMembers.GetMembersList.as_view(), name='get_chat_channel_members'),
    path('channel/members/add/<int:pk>/', ChannelMembers.AddMember.as_view(), name='add_chat_channel_member'),
    path('channel/members/delete/<int:pk>/', ChannelMembers.DeleteMember.as_view(), name='delete_chat_channel_member'),



    #MESSAGES management ENDPOINTS
    path('messages/get/all/<int:pk>', v.MessagesView.as_view(), name='get_all_messages_for_chat'),
    path('messages/post/', v.MessagesCreateView.as_view(), name='post_messege'),
    path('messages/edit/<int:pk>', v.MessagesUpdateView.as_view(), name='edit_messege'),
    #path('messages/delete/<int:pk>', v.MessagesViewSet.as_view(), name='delete_messege'),

]
urlpatterns += websocket_urlpatterns
