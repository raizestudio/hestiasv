import sys

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

ORDERED_MODELS = [
    "core.menu",
    "core.menuitem",
    "geosys.streetlabel",
    "geosys.street",
]

EXLUDED_APPS = [
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "admin",
]

EXCLUDED_MODELS = []


class Command(BaseCommand):
    """Load all fixtures based on exclusion rules defined in EXLUDED_APPS and EXCLUDED_MODELS

    Args:
        BaseCommand (class): Django BaseCommand class
    """

    help = "Loads all fixtures"

    def handle(self, *args, **options):
        models_to_retry = []

        call_command("flush", "--noinput")
        call_command("migrate")

        for model_name in ORDERED_MODELS:
            model = apps.get_model(model_name)
            sys.stdout.write(f"Loading fixtures for {model.__name__}. - ")
            res = self.load_fixtures_for_model(model)
            if res:
                models_to_retry.append({"app_label": model_name.split(".")[0], "model": res})
                res = None

        app_configs = apps.get_app_configs()
        for app_config in app_configs:
            if app_config.name.lower() not in EXLUDED_APPS:
                for model in app_config.models.values():
                    if model.__name__.lower() not in EXCLUDED_MODELS:
                        sys.stdout.write(f"Loading fixtures for {model.__name__}. - ")
                        res = self.load_fixtures_for_model(model)
                        if res:
                            models_to_retry.append({"app_label": app_config.name.lower(), "model": res})
                            res = None

        for _m in models_to_retry:
            sys.stdout.write(f"Retrying fixtures for {_m['model']}. - ")
            self.load_fixtures_for_model(apps.get_model(f"{_m['app_label']}.{_m['model']}"))

    def load_fixtures_for_model(self, model):

        model_name = model.__name__.lower()
        try:
            call_command("loaddata", model_name)

        except CommandError as ce:
            sys.stdout.write(self.style.ERROR(f"No fixtures found for {model.__name__}: {ce}.\n"))

        except IntegrityError as ie:
            sys.stdout.write(self.style.ERROR(f"Integrity error for {model.__name__}: {ie}.\n"))
            return model_name

        except Exception as e:
            sys.stdout.write(self.style.ERROR(f"Unexpected error for {model.__name__}: {e}.\n"))

        return None
