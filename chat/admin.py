from django.contrib import admin

# Register your models here.
from django.contrib import admin
from chat import models as m

admin.site.register(m.ChatUser)
admin.site.register(m.Channel)
admin.site.register(m.Messages)
admin.site.register(m.ChannelMembers)
