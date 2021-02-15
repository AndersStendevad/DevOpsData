from django.contrib import admin

from .models import User, Follower, Message

admin.site.register(User)
admin.site.register(Message)
admin.site.register(Follower)
