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
from chat.Views import ChannelMembersViews, ChannelViews, UserViews, MessegesViews

urlpatterns = [
    # USER RELATED ENDPOINTS
    path('user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register/', UserViews.CreateUser.as_view(), name='register_user'),
    path('user/resetpassword/<int:pk>/', UserViews.ChangePassword.as_view(), name='password_reset'),
    path('user/profile/<int:pk>/',UserViews.UpdateUser.as_view(), name='user_profile'),
    path('user/delete/<int:pk>/', UserViews.DeleteUser.as_view(), name='delete_user'),
    path('user/get/current/<int:pk>/', UserViews.RestrictedGetUserData.as_view(), name='get_current_user'),
    path('user/get/list/', UserViews.UserList.as_view(), name='get_user_list'),

    # CHAT-CHANNELS RELATED ENDPOINTS
    path('channel/create/new/', ChannelViews.AddNew.as_view(), name='create_chat_channel'),
    path('channel/get/list/brief/', ChannelViews.AllBrief.as_view() , name='get_chat_channels'),
    path('channel/get/list/detail/', ChannelViews.AllDetail.as_view() , name='get_chat_channels'),
    path('channel/update/<int:pk>/', ChannelViews.Update.as_view(), name='update_chat_channel'),
    path('channel/delete/<int:pk>/', ChannelViews.Delete.as_view(), name='delete_chat_channel'),

    # CHANNEL-MEMBERS RELATED ENDPOINTS
    path('channel/members/get/',ChannelMembersViews.GetMyChannel.as_view(), name='get_my_chat_channel_members'),
    path('channel/members/get/<int:pk>/', ChannelMembersViews.GetMembersList.as_view(), name='get_chat_channel_members'),
    path('channel/members/add/', ChannelMembersViews.AddMember.as_view(), name='add_chat_channel_member'),
    path('channel/members/delete/', ChannelMembersViews.DeleteMember.as_view(), name='delete_chat_channel_member'),

    #MESSAGES RELATED ENDPOINTS
    path('messages/get/all/<int:pk>/', MessegesViews.Get.as_view(), name='get_all_messages_for_chat'),
    path('messages/post/', MessegesViews.Create.as_view(), name='post_messege'),
    path('messages/edit/<int:pk>/', MessegesViews.Update.as_view(), name='edit_messege'),

]
urlpatterns += websocket_urlpatterns
