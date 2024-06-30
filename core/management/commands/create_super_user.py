from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError

# from user.models import UserPreference, UserSecurity


# usage: python manage.py create_user --username root --password root --noinput --email r@r.com
class Command(createsuperuser.Command):
    help = "Create a superuser, and allow password to be provided"

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

    def handle(self, *args, **options):
        password = options.get("password")
        username = options.get("username")
        database = options.get("database")

        if password and not username:
            # raise CommandError("--username is required if specifying --password")
            username = "root"
            password = "root"

        super(Command, self).handle(*args, **options)

        if password:
            user = self.UserModel._default_manager.db_manager(database).get(username=username)
            # user.set_password(password)
            # user.set_role(1)
            user.save()

            # UserPreference.objects.create(user=user, language="fr", theme="primary")
            # UserSecurity.objects.create(user=user, is_email_verified=True, is_phone_verified=False, is_two_factor_enabled=False)
