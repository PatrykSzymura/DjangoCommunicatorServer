from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as TopSerializer
from django.contrib.auth.models import User
from chat import models as m

from rest_framework_simplejwt.views import TokenObtainPairView as Top, TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['value'] = "komunikat"

        
        return token