import sys
from typing import Any

from django.core.management import BaseCommand, CommandError, call_command


class Command(BaseCommand):
    help = "Prepare the application for usage according to environment."

    def add_arguments(self, parser):
        pass
        # parser.add_argument(
        #     "--number",
        #     dest="number",
        #     default=1,
        #     help="Specifies the number of users to create.",
        # )
        # parser.add_argument(
        #     "--admin",
        #     dest="admin",
        #     default=False,
        #     help="Specifies the role of the user.",
        # )

    def handle(self, *args: Any, **options: Any) -> str | None:
        sys.stdout.write(self.style.NOTICE("Install is now executing.\n"))
        call_command("makemigrations")
        call_command("load_all_fixtures")
        call_command("create_super_user", "--username", "root", "--password", "root", "--email", "r@r.com", "--noinput")
        call_command("create_dev_users")
