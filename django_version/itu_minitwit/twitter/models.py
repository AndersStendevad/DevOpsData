from django.db import models

class User(models.Model):
    username = models.CharField('user', max_length=70)
    email = models.CharField('email',max_length=70)
    pwd_hash = models.CharField('pwd_hash'max_length=70)

    def __str__(self):
        return f"username: {self.username}, email: {self.email}, password hash: retracted"

class Follower(models.Model):
    source_user = models.ForeignKey('who_id',User, on_delete=models.CASCADE)
    target_user = models.IntegerField('whom_id')

    def __str__(self):
        return f"follow from user id: {self.soure_user} to user id: {self.target_user}"

class Message(models.Model):
    author = models.ForeignKey('author_id',User, on_delete=models.CASCADE)
    content = models.TextField('text')
    publication_date = models.DateField('pub_date')
    number_of_flags = models.IntegerField('flagged',default=0)
    
    def __str__(self):
        return f"message by user id: {self.author}, on {publication_date}, with content: {self.content}\nmessage has been flagged {self.number_of_flags} times."

