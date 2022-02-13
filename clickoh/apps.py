from django.apps import AppConfig


class ClickohConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clickoh'

    def ready(self):
        import clickoh.signals