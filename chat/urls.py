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
    #path('channel/create/new/'),
    path('channel/get/list/', v.ChannelView.as_view(), name='get_chat_channels'),
    path('channel/get/members/<int:pk>', v.ChannelMembersView.as_view(), name='get_chat_channel_data'),
    path('channel/update/<int:pk>/', v.ChannelView.as_view(), name='update_chat_channel'),
    path('channel/delete/<int:pk>/', v.ChannelView.as_view(), name='delete_chat_channel'),

    #MESSAGES management ENDPOINTS
    path('messages/get/all/<int:pk>', v.MessagesView.as_view(), name='get_all_messages_for_chat'),
    path('messages/post/', v.MessagesCreateView.as_view(), name='post_messege'),

    #path('messages/post/', v.MessagesViewSet.as_view({'get': 'list'}), name='get_all_messages'),

]
urlpatterns += websocket_urlpatterns
