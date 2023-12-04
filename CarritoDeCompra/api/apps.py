from django.apps import AppConfig
from django.conf import settings


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self) -> None:
        if settings.SCHEDULER_AUTOSTART:
            from api.scheduler import scheduler

            scheduler.start()
        return super().ready()
