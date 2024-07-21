import random
import string
import sys
from typing import Any

from django.core.management import BaseCommand, CommandError

from pro.models import Enterprise
from pro.tests.factories.factory_enterprise import EnterpriseFactory
from user.models import User


class Command(BaseCommand):
    help = "Create N mock agencies"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            dest="number",
            default=1,
            help="Specifies the number of users to create.",
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        number = options.get("number")

        for _ in range(int(number)):
            enterprise = EnterpriseFactory()
            enterprise.save()

        sys.stdout.write(self.style.SUCCESS(f"Successfully created {number} agencies.\n"))
