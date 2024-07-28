import random
import string
import sys
from typing import Any

from django.core.management import BaseCommand, CommandError

from pro.models import Enterprise
from pro.tests.factories.factory_enterprise_member import EnterpriseMemberFactory
from user.models import User


class Command(BaseCommand):
    help = "Assign users to enterprises, self-employed"

    def handle(self, *args: Any, **options: Any) -> str | None:
        number = options.get("number")

        _users = User.objects.exclude(role__group="GR-ADM").exclude(role__group="GR-USR")

        for _user in _users:
            if _user.role.group.code == "GR-AGY":
                enterprise_member = EnterpriseMemberFactory(
                    user=_user,
                    enterprise=random.choices(Enterprise.objects.all(), k=1)[0],
                )
                enterprise_member.save()

            # elif _user.role.name == "RO-SEL":
            #     selfemployed = random.choices(SelfEmployed.objects.all(), k=1)
            #     _user.selfemployed = selfemployed[0]
            #     _user.save()
            # else:
            #     sys.stdout.write(self.style.ERROR(f"User {_user.username} is not an employee or self-employed.\n"))

        sys.stdout.write(self.style.SUCCESS(f"Successfully assigned {len(_users)} users.\n"))
