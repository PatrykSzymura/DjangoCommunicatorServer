from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

from chat import models as m

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.User
        fields = ('id', 'username','password', 'first_name', 'last_name', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = m.ChatUser.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password', None)
            instance.set_password(password)
        return super().update(instance, validated_data)

class ChatUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = m.ChatUser
        fields = '__all__'
        extra_kwargs = {"password": {"write_only": True}}

class ChatUserMinimumDataSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = m.ChatUser
        fields = ('user','nickname')
        extra_kwargs = {"password": {"write_only": True}}

class ChatUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.ChatUser
        fields = ['nickname', 'authorityLevel']

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password    = serializers.CharField(write_only=True,required=True, validators=[validate_password])
    new_password_1  = serializers.CharField(write_only=True,required=True)
    new_password_2  = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password','new_password_1', 'new_password_2')

    def validate(self, attrs):
        if attrs['new_password_1'] != attrs['new_password_1']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect password")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password_1'])
        print(instance)
        print(validated_data)
        return instance

