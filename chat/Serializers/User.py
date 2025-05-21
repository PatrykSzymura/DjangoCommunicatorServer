from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.models import User

from chat import models as m
from chat.models import ChatUser


class BaseUserSerializer(serializers.ModelSerializer):
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

class DynamicBaseUserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class ChatUserSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = m.ChatUser
        fields = ('user','nickname','authorityLevel')
        extra_kwargs = {"password": {"write_only": True}}

class ChatUserMinimumDataSerializer(serializers.ModelSerializer):
    user = DynamicBaseUserSerializer(fields=['id','username'],read_only=True)
    class Meta:
        model = m.ChatUser
        fields = ('user','nickname')
        extra_kwargs = {"password": {"write_only": True}}

class NicknameSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.ChatUser
        fields = ('id','nickname',)

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
        if attrs['new_password_1'] != attrs['new_password_2']:
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

#TEST FIELD

class AdminAccessUserSerializer(serializers.ModelSerializer):
    user = DynamicBaseUserSerializer(fields=['id','username','last_name', 'email', 'first_name'],read_only=True)
    class Meta:
        model = m.ChatUser
        fields = ('user','nickname','authorityLevel')