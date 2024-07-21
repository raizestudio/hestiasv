import random
import string
import sys
from typing import Any

from django.core.management import BaseCommand, CommandError

from user.models import Role, User
from user.tests.factories.factory_base_user import UserFactory


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
        # admin = options.get("admin")

        for _ in range(int(number)):
            role = random.choices(Role.objects.all(), k=1)
            user = UserFactory(role=role[0])
            user.save()

        sys.stdout.write(self.style.SUCCESS(f"Successfully create {number} users.\n"))
