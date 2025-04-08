# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth import get_user_model

import datetime
from django.contrib.auth.models import User, Permission

def get_deleted_user():
    return get_user_model().objects.get_or_create(username='deleted-user')[0]

#user profile
class ChatUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nickname = models.CharField(max_length=30,default="")
    authorityLevel =  models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Chat Users"

class Channel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,default="")
    description = models.TextField(max_length=255, default="")

    def __str__(self):
        return self.name

class ChannelMembers(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(ChatUser,on_delete=models.CASCADE)

class Messages(models.Model):
    id = models.AutoField(primary_key=True)
    channelId = models.ForeignKey(Channel,on_delete=models.CASCADE)
    userId = models.ForeignKey(ChatUser,on_delete=models.SET(get_deleted_user))
    date = models.DateTimeField(auto_now_add=True)
    was_edited = models.BooleanField(default=False)
    edit_date = models.DateTimeField(auto_now=True)
    message = models.TextField(max_length=500)

    def __str__(self):
        author = ChatUser.objects.get(id=self.userId.id)
        log = str(self.date) + " Send by " + str(author) + " on "+ str(self.channelId) + "\n " + self.message

        if self.was_edited:
            log += "\n Was Edited on " + str(self.edit_date)
        return log

    class Meta:
        verbose_name_plural = "Messages"

