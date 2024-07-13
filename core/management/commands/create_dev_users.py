import random
import string
import sys
from typing import Any

from django.core.management import BaseCommand, CommandError

from user.models import Role, User


def generate_username() -> str:
    username_length = random.randint(5, 10)
    username = "".join(random.choices(string.ascii_lowercase, k=username_length))
    return username


def generate_email() -> str:
    email = f"{generate_username()}@{generate_username()}.com"
    return email


def pick_random_role(admin_allowed) -> str:
    return random.randint(1 if admin_allowed else 2, 3)


USERS = [
    {
        "username": "admin",
        "email": "adm@adm.com",
        "password": "admin",
        "is_superuser": False,
        "is_staff": True,
        "first_name": "Jadmin",
        "last_name": "Doe",
        "role": "RO-ADM"
    },
    {
        "username": "manager",
        "email": "mng@mng.com",
        "password": "manager",
        "is_superuser": False,
        "is_staff": True,
        "first_name": "Manage",
        "last_name": "Doe",
        "role": "RO-MNG"
    },
    {
        "username": "user",
        "email": "usr@usr.com",
        "password": "user",
        "is_superuser": False,
        "is_staff": False,
        "first_name": "Juser",
        "last_name": "Doe",
        "role": "RO-USR"
    },
    {
        "username": "agencydirector",
        "email": "drc@drc.com",
        "password": "agencydirector",
        "is_superuser": False,
        "is_staff": False,
        "first_name": "Director",
        "last_name": "Doe",
        "role": "RO-DRC"
    },
    {
        "username": "agencymanager",
        "email": "man@man.com",
        "password": "agencymanager",
        "is_superuser": False,
        "is_staff": False,
        "first_name": "Manager",
        "last_name": "Doe",
        "role": "RO-MAN"
    },
    {
        "username": "agencyemployee",
        "email": "emp@emp.com",
        "password": "agencyemployee",
        "is_superuser": False,
        "is_staff": False,
        "first_name": "Employee",
        "last_name": "Doe",
        "role": "RO-EMP"
    }
]


class Command(BaseCommand):
    help = "Create users for dev purposes"

    def add_arguments(self, parser):
        pass

    def handle(self, *args: Any, **options: Any) -> str | None:
        # number = options.get("number")
        # admin = options.get("admin")

        for user in USERS:
            _user = User.objects.filter(username=user["username"]).first()
            if _user:
                _user.delete()
                
            _user = User.objects.create_user(
                username=user["username"],
                password=user["password"],
                email=user["email"],
                is_superuser=user["is_superuser"],
                is_staff=user["is_staff"],
                first_name=user["first_name"],
                last_name=user["last_name"],
            )
            
            _user.role = Role.objects.get(code=user["role"])
            _user.save()
            
            sys.stdout.write(self.style.SUCCESS(f"Successfully create {user["username"]}.\n"))
