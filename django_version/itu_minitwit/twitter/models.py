from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField('user', max_length=70)
    email = models.CharField('email', max_length=70)
    pwd_hash = models.CharField('pwd_hash', max_length=150)

    class Meta:
        db_table = 'twiiter_users'

    def __str__(self):
        return f"username: {self.username}, email: {self.email}"

class Follower(models.Model):
    source_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='who_id')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='whom_id')

    class Meta:
        db_table = 'followers'

    def __str__(self):
        return f"follow from user id: {self.source_user} to user id: {self.target_user}"

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_id')
    content = models.TextField('text')
    publication_date = models.DateField('pub_date')
    number_of_flags = models.IntegerField('flagged', default = 0)

    class Meta:
        db_table = 'messages'