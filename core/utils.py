from django.core.cache import cache

from core.models import AppSetting

SETTINGS_CACHE_KEY = 'app_settings'
CACHE_TIMEOUT = 60 * 60  # 1 hour


def get_app_settings():
    settings = cache.get(SETTINGS_CACHE_KEY)
    if not settings:
        settings = {setting.key: setting.value for setting in AppSetting.objects.all()}
        cache.set(SETTINGS_CACHE_KEY, settings, CACHE_TIMEOUT)
    return settings
