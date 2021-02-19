from django.contrib import admin

#from .models import User, Follower, Message
from .models import Follower, Message, ProfileUser

admin.site.register(ProfileUser)
admin.site.register(Message)
admin.site.register(Follower)
