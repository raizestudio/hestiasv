from django.contrib.auth.management.commands.createsuperuser import (
    Command as CreateSuperUserCommand,
)
from django.core.management import CommandError
from django.utils.translation import gettext as _


from django.utils import timezone


from django.utils.translation import gettext as _

from user.models import Role, UserPreferences, UserSecurity


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
            user.set_first_name("John")
            user.set_last_name("Doe")
            user.role = Role.objects.get(code="RO-ADM")
            user.save()

            UserPreferences.objects.get_or_create(user=user, defaults={"language": "fr", "theme": "primary"})

            UserSecurity.objects.get_or_create(
                user=user,
                defaults={
                    "is_phone_verified": False,
                    "is_two_factor_enabled": False,
                    "anti_phishing_code": "",
                    "email_validation_code_sent_at": timezone.now(),
                    "email_validation_code_confirmed_at": timezone.now(),
                },
            )

            self.stdout.write(self.style.SUCCESS(f"Superuser {username} created successfully with the specified password."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser {username} created successfully without specified password."))
