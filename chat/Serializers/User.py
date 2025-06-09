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

class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True,required=True, validators=[validate_password])

    class Meta:
        model = m.User
        fields = ('password','new_password',)

    def validate_old_password(self, password):
        user = self.context['request'].user
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password")
        return password


    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


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
        #extra_kwargs = {"password": {"write_only": True}}

class NicknameSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.ChatUser
        fields = ('id','nickname',)

class ChatUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.ChatUser
        fields = ['nickname', 'authorityLevel']

class AdminAccessUserSerializer(serializers.ModelSerializer):
    user = DynamicBaseUserSerializer(fields=['id','username','last_name', 'email', 'first_name'],read_only=True)
    class Meta:
        model = m.ChatUser
        fields = ('user','nickname','authorityLevel')

class CreateAccountSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(max_length=30, required=False, default="")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'email', 'nickname']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        nickname = validated_data.pop('nickname', '')

        # Create user
        user = User.objects.create_user(**validated_data)

        # Create linked ChatUser
        ChatUser.objects.create(user=user, nickname=nickname, authorityLevel=1)

        return user

    def update(self, instance, validated_data):
        # Update related ChatUser nickname if provided
        nickname = validated_data.pop('nickname', None)

        # Update User fields
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        # Update ChatUser nickname
        if nickname is not None:
            try:
                chat_user = ChatUser.objects.get(user=instance)
                chat_user.nickname = nickname
                chat_user.save()
            except ChatUser.DoesNotExist:
                # Create one if it doesn't exist (optional fallback)
                ChatUser.objects.create(user=instance, nickname=nickname, authorityLevel=1)

        return instance



class UpdateAccountData(serializers.ModelSerializer):
    nickname = serializers.CharField(source='chatuser.nickname', required=False)

    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'nickname']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Aktualizacja ChatUser
        chatuser_data = validated_data.get('chatuser', {})
        if chatuser_data:
            chatuser = instance.chatuser
            chatuser.nickname = chatuser_data.get('nickname', chatuser.nickname)
            chatuser.save()

        return instance
