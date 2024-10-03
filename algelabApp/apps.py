from django.apps import AppConfig

class AlgelabAppConfig(AppConfig):
    name = 'algelabApp'

    def ready(self):
        import algelabApp.signals  # Ensure signals are imported
