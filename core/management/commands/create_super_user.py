from django.contrib.auth.management.commands.createsuperuser import (
    Command as CreateSuperUserCommand,
)
from django.core.management import CommandError
from django.utils.translation import gettext as _

from user.models import UserPreferences, UserSecurity


class Command(CreateSuperUserCommand):
    help = "Create a superuser, and allow password to be provided"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("--password", help="Specifies the password for the superuser.")

    def handle(self, *args, **options):
        password = options.get("password")
        username = options.get("username")
        email = options.get("email")
        database = options.get("database")

        if password and not username:
            raise CommandError("--username is required if specifying --password")

        super().handle(*args, **options)

        if password:
            user = self.UserModel._default_manager.db_manager(database).get(username=username)
            user.set_password(password)
            user.set_email(email)
            user.save()

            UserPreferences.objects.get_or_create(user=user, defaults={"language": "fr", "theme": "primary"})

            UserSecurity.objects.get_or_create(
                user=user, defaults={"is_email_verified": True, "is_phone_verified": False, "is_two_factor_enabled": False, "anti_phishing_code": ""}
            )

            self.stdout.write(self.style.SUCCESS(f"Superuser {username} created successfully with the specified password."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser {username} created successfully without specified password."))
