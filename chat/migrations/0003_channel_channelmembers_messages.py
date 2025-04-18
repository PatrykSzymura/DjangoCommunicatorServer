# Generated by Django 5.1.6 on 2025-04-08 15:08

import chat.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatuser_nickname'),
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
            name='ChannelMembers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chatuser')),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField(max_length=500)),
                ('channelId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.channel')),
                ('userId', models.ForeignKey(on_delete=models.SET(chat.models.get_deleted_user), to='chat.chatuser')),
            ],
        ),
    ]
