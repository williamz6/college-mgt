from django.apps import AppConfig


class TursConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'turs'

    def ready(self):
        import turs.signals
