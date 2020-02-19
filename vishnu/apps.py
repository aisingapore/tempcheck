from django.apps import AppConfig


class VishnuConfig(AppConfig):
    name = 'vishnu'
    verbose_name = "Vishnu"

    def ready(self):
        from vishnu.scheduler import start_scheduler

        start_scheduler()
