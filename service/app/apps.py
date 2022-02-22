from django.apps import AppConfig as AppConfigLib


class AppConfig(AppConfigLib):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
