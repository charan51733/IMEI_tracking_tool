from django.apps import AppConfig


class DeviceConfig(AppConfig):
    name = 'device'

    def ready(self):
        from django.conf import settings
        from django.contrib import auth
        auth.REDIRECT_FIELD_NAME = '?next=/device/device/'
