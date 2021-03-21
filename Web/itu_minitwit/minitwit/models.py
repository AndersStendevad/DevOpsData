from django.db import models
from django.contrib.auth.models import AbstractUser
from django_prometheus.models import ExportModelOperationsMixin

class Profile(ExportModelOperationsMixin("profile"), AbstractUser):
    class Meta:
        db_table = "profiles"


class Follower(ExportModelOperationsMixin("follower"), models.Model):
    source_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="who_id"
    )
    target_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="whom_id"
    )

    class Meta:
        db_table = "followers"

    def __str__(self):
        return f"follow from user id: {self.source_user} to user id: {self.target_user}"


class Message(ExportModelOperationsMixin("message"), models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="author_id"
    )
    content = models.TextField("text")
    publication_date = models.DateField("pub_date", auto_now_add=True)
    number_of_flags = models.IntegerField("flagged", default=0)

    class Meta:
        db_table = "messages"
