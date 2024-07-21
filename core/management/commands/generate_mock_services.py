import random
import string
import sys
from typing import Any

from django.core.management import BaseCommand, CommandError

from core.models import Category, Tag
from service.tests.factories.factory_service import ServiceFactory
from user.models import User


class Command(BaseCommand):
    help = "Create N mock users"

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
            _user = random.choices(User.objects.all(), k=1)
            service = ServiceFactory(
                created_by=_user[0],
                updated_by=_user[0],
            )
            _tags = random.choices(Tag.objects.all(), k=random.randint(1, 2))
            _categories = random.choices(Category.objects.all(), k=random.randint(1, 2))
            service.tags.set(_tags)
            service.categories.set(_categories)
            service.save()

        sys.stdout.write(self.style.SUCCESS(f"Successfully create {number} services.\n"))
