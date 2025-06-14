# Generated by Django 5.1.6 on 2025-06-10 17:19

import chat.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=30)),
                ('description', models.TextField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ChatUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(default='', max_length=30)),
                ('authorityLevel', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Chat Users',
            },
        ),
        migrations.CreateModel(
            name='ChannelMembers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.channel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chatuser')),
            ],
            options={
                'verbose_name_plural': 'Channel Members',
            },
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('was_edited', models.BooleanField(default=False)),
                ('edit_date', models.DateTimeField(auto_now=True)),
                ('message', models.TextField(max_length=500)),
                ('author', models.ForeignKey(on_delete=models.SET(chat.models.get_deleted_user), to='chat.chatuser')),
                ('channelId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.channel')),
            ],
            options={
                'verbose_name_plural': 'Messages',
            },
        ),
    ]
