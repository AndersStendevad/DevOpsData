from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """ Django command to make sure that the base superuser exists"""

    def handle(self, *args, **kwargs):
        self.stdout.write("waiting admin to be created ...")
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            self.stdout.write("admin does not exists so creating it ...")
            User.objects.create_superuser(
                username="admin", email="admin@example.com", password="admin"
            )
