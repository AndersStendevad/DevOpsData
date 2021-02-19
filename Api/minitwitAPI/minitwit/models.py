from django.db import models
from django.contrib import auth
# Create your models here.

class ProfileUser(auth.models.User):
    class Meta:
        db_table = 'profile_users'


class Follower(models.Model):
    source_user = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name='who_id')
    target_user = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name='whom_id')

    class Meta:
        db_table = 'followers'

    def __str__(self):
        return f"follow from user id: {self.source_user} to user id: {self.target_user}"

class Message(models.Model):
    author = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name='author_id')
    content = models.TextField('text')
    publication_date = models.DateField('pub_date')
    number_of_flags = models.IntegerField('flagged', default = 0)

    class Meta:
        db_table = 'messages'
