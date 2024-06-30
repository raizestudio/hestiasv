import random
import string
import sys
from typing import Any

from django.core.management import BaseCommand, CommandError

from users.models import BaseUser, UserPreference, UserSecurity


def generate_username() -> str:
    username_length = random.randint(5, 10)
    username = "".join(random.choices(string.ascii_lowercase, k=username_length))
    return username


def generate_email() -> str:
    email = f"{generate_username()}@{generate_username()}.com"
    return email


def pick_random_role(admin_allowed) -> str:
    return random.randint(1 if admin_allowed else 2, 3)


class Command(BaseCommand):
    help = "Create N mock users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            dest="number",
            default=1,
            help="Specifies the number of users to create.",
        )
        parser.add_argument(
            "--admin",
            dest="admin",
            default=False,
            help="Specifies the role of the user.",
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        number = options.get("number")
        admin = options.get("admin")

        for _ in range(int(number)):
            _user = BaseUser.objects.create_user(username=generate_username(), password=generate_username(), email=generate_email(), role=pick_random_role(admin))

            UserPreference.objects.create(user=_user, language="fr", theme="primary")
            UserSecurity.objects.create(user=_user, is_email_verified=False, is_phone_verified=False, is_two_factor_enabled=False)

        sys.stdout.write(self.style.SUCCESS(f"Successfully create {number} users.\n"))
