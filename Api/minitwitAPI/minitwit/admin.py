from django.contrib import admin

from .models import Follower, Message, Profile

admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Follower)
