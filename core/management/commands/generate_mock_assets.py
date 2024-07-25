import random
import string
import sys
from typing import Any

from django.core.management import BaseCommand, CommandError

from asset.tests.factories.factory_asset import AssetFactory
from core.models import Category, Tag
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
            try:
                asset = AssetFactory(
                    author=_user[0],
                    updated_by=_user[0],
                )
                _tags = random.choices(Tag.objects.all(), k=random.randint(1, 2))
                _categories = random.choices(Category.objects.all(), k=random.randint(1, 2))
                asset.tags.set(_tags)
                asset.categories.set(_categories)
                asset.save()
            except Exception as e:
                pass
        sys.stdout.write(self.style.SUCCESS(f"Successfully create {number} assets.\n"))
