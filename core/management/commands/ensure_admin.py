import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Idempotently create/update the staff admin account from env vars (safe to run on every deploy)."

    def handle(self, *args, **options):
        username = os.getenv("ADMIN_USERNAME", "abasse")
        password = os.getenv("ADMIN_PASSWORD")
        email = os.getenv("ADMIN_EMAIL", "admin@abasseniang.fr")

        if not password:
            self.stdout.write("ADMIN_PASSWORD not set, skipping admin account setup.")
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )
        user.is_staff = True
        user.is_superuser = True
        user.email = email
        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(
            f"Admin account '{username}' {'created' if created else 'updated'}."
        ))
