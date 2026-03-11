import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

app = Celery("currency_service")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(
    [
        "services.celery.currency_tasks",
    ]
)
