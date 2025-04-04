# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


import datetime
from django.contrib.auth.models import User, Permission


#user profile
class ChatUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nickname = models.CharField(max_length=30,default="")
    authorityLevel =  models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Chat Users"